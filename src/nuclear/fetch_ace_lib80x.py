# ASSERT_CONVENTION: units_sigma=barn, units_En=eV, data=ENDF/B-VIII.0_ACE_Lib80x_NJOY2016.68_293.6K
"""
Acquire PRE-RECONSTRUCTED (NJOY-processed) continuous-energy ACE files for the
five natural Ge isotopes (Plan 07-02, milestone v1.1).

WHY THIS EXISTS
---------------
In the ENDF/B-VIII.0 n-Ge evaluations, MF=3 MT=2 (elastic) is a *background*
that is EXACTLY ZERO throughout the resolved-resonance + unresolved-resonance
region (Ge-70 up to ~1.05 MeV, Ge-72 ~0.70, Ge-73 ~13.7 keV, Ge-74 ~0.60,
Ge-76 ~0.57 MeV): the sub-MeV elastic cross section lives entirely in File 2
(resonance parameters) and must be RECONSTRUCTED to pointwise form.

NJOY/openmc will not build on this osx-arm64 machine, so instead of
reconstructing locally (and instead of hand-modelling resonances, which is the
forbidden proxy fp-bespoke-parser) we download ACE files in which the
reconstruction has ALREADY been performed by NJOY 2016.68, from the LANL
Lib80x distribution (LA-UR-18-24034).

SOURCE
------
    Lib80x -- "Release of ENDF/B-VIII.0-Based ACE Data Files",
    Conlin, Haeck, Neudecker, Parsons, White (2018), LA-UR-18-24034.
    https://nucleardata.lanl.gov/ace/lib80x/
    archive: https://nucleardata.lanl.gov/lib/Lib80x.zip  (7.05 GB)

BANDWIDTH NOTE (why partial download, not the 7 GB tarball)
-----------------------------------------------------------
The archive is only distributed whole, but the server advertises
`Accept-Ranges: bytes`.  We therefore mount the remote ZIP through an
HTTP-Range-backed seekable file object and let the PYTHON STANDARD LIBRARY
`zipfile` module read its central directory and inflate only the five members
we need (~5 MB of range requests instead of 7 GB).  No bespoke ZIP or ACE
parsing is done here -- `zipfile` handles the container, and the `endf`
package handles the ACE tables downstream.

TEMPERATURE / ZAID EXTENSION
----------------------------
Lib80x ZAID extensions:  .800nc = 293.6 K (room temperature)  <-- USED
                         .801nc = 600 K, .802nc = 900 K, .803nc = 1200 K,
                         .804nc = 2500 K, .805nc = 0.1 K, .806nc = 250 K
293.6 K is the correct choice for a room-temperature Ge wafer.
"""
from __future__ import annotations

import hashlib
import io
import os
import urllib.request
import zipfile

LIB80X_URL = "https://nucleardata.lanl.gov/lib/Lib80x.zip"
LIB80X_DOC = "https://nucleardata.lanl.gov/ace/lib80x/  (LA-UR-18-24034)"
NJOY_VERSION = "NJOY 2016.68"
ACE_TEMPERATURE_K = 293.6
ACE_SUFFIX = "800nc"  # 293.6 K

# ZAID = 1000*Z + A, Z=32 for Ge.  Members live at Lib80x/Lib80x/Ge/<ZAID>.<ext>
ZAIDS = {70: 32070, 72: 32072, 73: 32073, 74: 32074, 76: 32076}

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, "..", ".."))
ACE_DIR = os.path.join(_ROOT, "data", "endf", "ace")


class HTTPRangeFile(io.RawIOBase):
    """Minimal seekable read-only file over HTTP byte ranges.

    Exists solely so the stdlib `zipfile` can seek inside a remote archive;
    it implements no archive format logic of its own."""

    def __init__(self, url, chunk=1 << 20):
        self.url = url
        self.chunk = chunk
        self._pos = 0
        self._cache = {}
        self.bytes_fetched = 0
        with urllib.request.urlopen(
            urllib.request.Request(url, method="HEAD"), timeout=60
        ) as r:
            self.size = int(r.headers["Content-Length"])
            if r.headers.get("Accept-Ranges", "").lower() != "bytes":
                raise RuntimeError(f"{url} does not support byte ranges")

    def seekable(self):
        return True

    def readable(self):
        return True

    def tell(self):
        return self._pos

    def seek(self, off, whence=0):
        if whence == 0:
            self._pos = off
        elif whence == 1:
            self._pos += off
        else:
            self._pos = self.size + off
        return self._pos

    def _get_chunk(self, idx):
        if idx in self._cache:
            return self._cache[idx]
        start = idx * self.chunk
        end = min(start + self.chunk, self.size) - 1
        if start > end:
            return b""
        req = urllib.request.Request(
            self.url, headers={"Range": f"bytes={start}-{end}"}
        )
        last = None
        for _ in range(4):
            try:
                with urllib.request.urlopen(req, timeout=180) as r:
                    data = r.read()
                break
            except Exception as exc:  # transient network -> retry
                last = exc
        else:
            raise RuntimeError(f"range fetch failed: {last}")
        self.bytes_fetched += len(data)
        if len(self._cache) > 512:
            self._cache.clear()
        self._cache[idx] = data
        return data

    def read(self, n=-1):
        if n is None or n < 0:
            n = self.size - self._pos
        n = min(n, self.size - self._pos)
        out = bytearray()
        while n > 0:
            data = self._get_chunk(self._pos // self.chunk)
            if not data:
                break
            off = self._pos % self.chunk
            take = data[off:off + n]
            if not take:
                break
            out += take
            self._pos += len(take)
            n -= len(take)
        return bytes(out)

    def readinto(self, b):
        data = self.read(len(b))
        b[: len(data)] = data
        return len(data)


def ace_path(A, suffix=ACE_SUFFIX):
    return os.path.join(ACE_DIR, f"{ZAIDS[A]}.{suffix}")


def fetch_all(force=False, suffix=ACE_SUFFIX):
    """Download the 5 Ge ACE tables; returns {A: (path, sha256, nbytes)}.

    `suffix` selects the processing temperature (see module docstring);
    "800nc" = 293.6 K is the baseline, "805nc" = 0.1 K is used only for the
    Doppler-sensitivity cross-check."""
    os.makedirs(ACE_DIR, exist_ok=True)
    need = [A for A in ZAIDS if force or not os.path.exists(ace_path(A, suffix))]
    info = {}
    if need:
        remote = HTTPRangeFile(LIB80X_URL)
        zf = zipfile.ZipFile(remote)
        for A in sorted(need):
            member = f"Lib80x/Lib80x/Ge/{ZAIDS[A]}.{suffix}"
            data = zf.read(member)
            with open(ace_path(A, suffix), "wb") as fh:
                fh.write(data)
            print(f"  fetched {member}  ({len(data)/1e6:.2f} MB uncompressed)")
        print(f"  total range traffic: {remote.bytes_fetched/1e6:.1f} MB "
              f"(archive is {remote.size/1e9:.2f} GB)")
    for A in sorted(ZAIDS):
        p = ace_path(A, suffix)
        raw = open(p, "rb").read()
        info[A] = (p, hashlib.sha256(raw).hexdigest(), len(raw))
    return info


if __name__ == "__main__":
    import sys
    sfx = sys.argv[1] if len(sys.argv) > 1 else ACE_SUFFIX
    for A, (p, sha, n) in fetch_all(suffix=sfx).items():
        print(f"Ge-{A}  ZAID={ZAIDS[A]}.{sfx}  {n/1e6:6.2f} MB  sha256={sha[:16]}...")
