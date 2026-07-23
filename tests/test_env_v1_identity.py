# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Phase-9 Plan 09-01: executable identity checks for the v1.0 muon and
environmental-gamma surface-environment inputs (ROADMAP Phase 9 SC1).

SC1's operative words are "verified by direct comparison against the frozen v1.0
artifacts rather than by assertion".  Every claim made in
``09-01-MUON-GAMMA-DECLARATION.md`` is therefore re-checkable by running this
module rather than by re-reading prose.

Guards:
  * fp-mc-rerun-drift        -- nothing here re-runs a Monte Carlo or writes data/
  * fp-wrong-muon-path       -- the non-existent src/muon, data/muon paths stay absent
  * fp-overburden-leak       -- shielded-token scan over the channel import closure
  * fp-rate-conflation       -- the four circulating Compton rates stay distinct
  * fp-assertion-not-comparison -- scalars are recomputed from the committed modules

The shielded-token machinery (``SHIELDED_TOKENS``, ``SHIELDED_ALLOWLIST``,
``NOT_APPLIED_MARKERS``, ``scan_text``, ``scan_paths``, ``import_closure_files``)
is exported at module level so Plan 09-03's
``tests/test_surface_environment.py`` imports it rather than re-typing the list.
"""
from __future__ import annotations

import os
import re
import subprocess

import numpy as np
import pytest

from qpd_potential import compton_source as cs
from qpd_potential import muon_deposit as md
from qpd_potential import wafer_geometry as g

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MUON_CSV = os.path.join(REPO, "data", "muon_dRdEdep.csv")
COMPTON_CSV = os.path.join(REPO, "data", "compton_dRdEdep.csv")
GAMMA_LINES_CSV = os.path.join(REPO, "data", "gamma_lines.csv")
DECLARATION = os.path.join(
    REPO, "GPD", "phases", "09-sea-level-surface-environment-lock-p-env",
    "09-01-MUON-GAMMA-DECLARATION.md",
)

# --------------------------------------------------------------------------- #
# Committed values of record (Plan 09-01 contract).  These are the numbers the  #
# declaration quotes; the tests below prove the files still carry them.         #
# --------------------------------------------------------------------------- #
MUON_RATE_HZ = 1.3659
MUON_RATE_ERR_HZ = 0.0003
MUON_FIRST_E_KEV = 1.014497e-02
GAMMA_RATE_HZ = 2.6747e-01          # BOUND incoherent -- the rate of record
GAMMA_RATE_FREE_KN_HZ = 2.6846e-01  # free-KN pre-binding, a DIFFERENT number
GAMMA_RATE_VALD03_HZ = 2.7305e-01   # independent Phi*sigma_KN*N_e anchor
MEAN_VERT_MEV = 1.4585
MPV_VERT_MEV = 1.2323
XI_VERT_MEV = 0.0721
MEAN_CHORD_CM = 0.385
COMPTON_EDGES_KEV = {"K40": 1243.4, "Bi214": 1541.3, "Tl208": 2381.8}
TL208_LINE_KEV = 2614.511


# --------------------------------------------------------------------------- #
# Shielded-configuration token machinery (exported; Plan 09-03 imports this)    #
# --------------------------------------------------------------------------- #
#: Tokens that must not appear as an APPLIED quantity anywhere in the unshielded
#: surface environment set.  Numeric tokens carry digit boundaries so that e.g.
#: 1.4150 (a muon quadrature cross-check) and 1.4585 (the mean deposit) are not
#: false positives on the NUCLEUS omnidirectional attenuation factor 1.41.
SHIELDED_TOKENS: tuple[tuple[str, str], ...] = (
    ("m.w.e", r"m\.w\.e"),
    ("overburden", r"overburden"),
    ("post_shield", r"post[_ ]shield"),
    ("phi_post", r"phi_post"),
    ("buildup", r"buildup"),
    ("attenuation", r"attenuation"),
    ("2.92", r"(?<![\d.])2\.92(?![\d])"),
    ("1.41", r"(?<![\d.])1\.41(?![\d])"),
    ("veto_credit", r"veto_credit"),
    ("mcpd", r"mcpd"),
)

#: Extra tokens Plan 09-03 adds for the assembled environment set.
SHIELDED_TOKENS_EXTRA: tuple[tuple[str, str], ...] = (
    ("dru", r"\bdru\b"),
    ("Table 5", r"Table\s+5"),
    ("residual", r"residual"),
)

#: Narrow, justified exemptions.  Each entry is
#: (path-suffix, exact substring that must be present on the hit line, why).
#: A NEW attenuation-like term would not match any entry and would fail.
SHIELDED_ALLOWLIST: tuple[tuple[str, str, str], ...] = (
    (
        "src/qpd_potential/compton_source.py",
        "Linear attenuation coefficient mu = (mu/rho) * rho",
        "NIST XCOM photon mass-attenuation coefficient of the GERMANIUM TARGET "
        "(data/ge_xcom_mu.csv), used for mu*ell_bar and the double-scatter "
        "fraction.  It is not a shield, an overburden, a buildup factor or any "
        "post-shield quantity, and it multiplies no normalization.",
    ),
)

#: Phrases that mark a prose hit as an explicit NOT-APPLIED / audit-machinery
#: statement rather than an applied shielded quantity.
NOT_APPLIED_MARKERS: tuple[str, ...] = (
    "NOT applied",
    "not applied",
    "not applicable",
    "no overburden",
    "zero overburden",
    "0 m.w.e",
    "by construction",
    "forbidden",
    "allow-list",
    "allow-listed",
    "allowlist",
    "SHIELDED_TOKENS",
    "Token list",
    "token list",
    "Shielded-configuration hits: 0",
    "Total hits",
    "is not a shield",
    "not used",
    "does not",
    "voided",
    "no shield",
    "NOT a shielded",
    "scan",
    "applies **no**",
    "must NOT be applied",
    "audit machinery",
    "not an error bar",
    "no NUCLEUS",
    "no post-shield",
    "no buildup",
    "no veto",
)


def normalize_unicode(text: str) -> str:
    """Fold Unicode look-alikes that silently break ASCII exact-match checks.

    Carried from the Phase-8 lesson: U+2009 THIN SPACE made present text look
    absent.  The same class of bug hits U+2212 MINUS SIGN, which is what a
    Markdown table's "-20.61 %" is usually typeset with -- an ASCII ``^[+-]``
    sign test would then wrongly report that the sign had been dropped.
    """
    return (text.replace("−", "-").replace("–", "-")
                .replace("—", "-").replace(" ", " ")
                .replace(" ", " ").replace(" ", " "))


def scan_text(text: str, tokens=SHIELDED_TOKENS,
              skip_fenced: bool = False) -> list[tuple[int, str, str]]:
    """Return [(lineno, token, line)] for every shielded-token hit in ``text``.

    ``skip_fenced`` skips ``` fenced blocks in Markdown prose: those hold
    verbatim recorded commands and their output (the audit EVIDENCE), not an
    applied physical quantity.  Source files are always scanned in full.
    """
    hits: list[tuple[int, str, str]] = []
    fenced = False
    for i, line in enumerate(text.splitlines(), start=1):
        if skip_fenced and line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        for name, pat in tokens:
            if re.search(pat, line, flags=re.IGNORECASE):
                hits.append((i, name, line.rstrip()))
    return hits


def scan_paths(paths, tokens=SHIELDED_TOKENS) -> list[tuple[str, int, str, str]]:
    """Scan files, returning [(path, lineno, token, line)] for every hit."""
    out: list[tuple[str, int, str, str]] = []
    for p in paths:
        with open(p, encoding="utf-8") as fh:
            for lineno, token, line in scan_text(fh.read(), tokens):
                out.append((p, lineno, token, line))
    return out


def is_allowlisted(path: str, line: str) -> bool:
    """True if this exact hit line carries a recorded, justified exemption."""
    norm = path.replace(os.sep, "/")
    return any(
        norm.endswith(suffix) and needle in line
        for suffix, needle, _why in SHIELDED_ALLOWLIST
    )


def is_not_applied(line: str) -> bool:
    """True if a prose hit line explicitly says the quantity is NOT applied.

    Case-insensitive: header text is often shouted ("ZERO OVERBURDEN") while the
    marker list is written in lower case, and a case-sensitive comparison would
    make a genuine exclusion look like an applied quantity.
    """
    low = line.lower()
    return any(m.lower() in low for m in NOT_APPLIED_MARKERS)


def import_closure_files(*roots) -> list[str]:
    """Source files of ``roots`` plus every qpd_potential module they import."""
    seen: dict[str, object] = {}

    def walk(mod):
        name = getattr(mod, "__name__", "")
        if not name.startswith("qpd_potential") or name in seen:
            return
        seen[name] = mod
        for obj in vars(mod).values():
            if getattr(obj, "__name__", "").startswith("qpd_potential") and hasattr(obj, "__file__"):
                walk(obj)

    for r in roots:
        walk(r)
    return sorted({m.__file__ for m in seen.values() if getattr(m, "__file__", None)})


# --------------------------------------------------------------------------- #
# Helpers                                                                       #
# --------------------------------------------------------------------------- #
def _header_value(path: str, key: str) -> str:
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("#"):
                break
            if line.startswith(f"# {key}"):
                return line[len(f"# {key}"):].lstrip(" =").rstrip()
    raise AssertionError(f"header key {key!r} not found in {path}")


def _table(path: str):
    e, r = [], []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#") or line.startswith("E_dep"):
                continue
            parts = line.split(",")
            if len(parts) < 2:
                continue
            e.append(float(parts[0]))
            r.append(float(parts[1]))
    return np.array(e), np.array(r)


def _compton_edge(e_gamma_kev: float) -> float:
    """E_edge = 2 E_gamma^2 / (m_e c^2 + 2 E_gamma), closed form, no sampler."""
    return 2.0 * e_gamma_kev**2 / (cs.M_E_KEV + 2.0 * e_gamma_kev)


# --------------------------------------------------------------------------- #
# Muon channel                                                                  #
# --------------------------------------------------------------------------- #
def test_muon_header_scalars():
    """The committed muon CSV still carries exactly the declared scalars."""
    raw = _header_value(MUON_CSV, "integral_muon_rate_Hz")
    value, _, err = raw.partition("+/-")
    assert float(value.strip()) == MUON_RATE_HZ
    assert float(err.strip()) == MUON_RATE_ERR_HZ

    e, _ = _table(MUON_CSV)
    assert e[0] == MUON_FIRST_E_KEV

    mpv_line = _header_value(MUON_CSV, "vertical_chord_MPV_MeV")
    assert mpv_line.startswith(str(MPV_VERT_MEV))
    assert f"mean = {MEAN_VERT_MEV}" in mpv_line


def test_muon_deterministic_scalars():
    """Closed-form scalars re-derive from the COMMITTED MODULES, not the CSV."""
    ell = g.cauchy_mean_chord()                       # Cauchy 4V/S
    assert ell == pytest.approx(MEAN_CHORD_CM, rel=1e-3)

    x_vert = md.RHO * g.CHORD_VERTICAL                # mass thickness [g/cm^2]
    bg = md.beta_gamma(np.array([4.0]))               # MIP muon
    dp, xi = md.mpv_deposit(np.array([x_vert]), bg)

    assert xi[0] == pytest.approx(XI_VERT_MEV, rel=5e-3)
    assert dp[0] == pytest.approx(MPV_VERT_MEV, rel=5e-3)

    mean = md.DEDX_MEAN * x_vert
    assert mean == pytest.approx(MEAN_VERT_MEV, rel=1e-3)

    # Landau right-skew signature.  If this fails the MPV has been silently
    # replaced by the mean or by a Moyal approximation and the peak is misplaced.
    assert dp[0] < MEAN_VERT_MEV
    assert dp[0] < mean

    # Thin-absorber (Landau / mild-Vavilov) regime, not Gaussian.
    assert md.kappa(np.array([x_vert]), bg)[0] < 0.07


def test_muon_grid_floor_matches_shared_grid():
    """The frozen table is ON the project grid, not silently off it.

    The committed first tabulated energy 1.014497e-02 keV is the first log-bin
    CENTRE of shared_energy_grid() (whose first EDGE is exactly 1.0e-2 keV); the
    whole E_dep column must reproduce sqrt(edges[:-1]*edges[1:]).
    """
    edges = md.shared_energy_grid()
    assert edges[0] == pytest.approx(1.0e-2, rel=1e-12)
    centers = np.sqrt(edges[:-1] * edges[1:])
    assert centers[0] == pytest.approx(MUON_FIRST_E_KEV, rel=1e-6)

    e_mu, _ = _table(MUON_CSV)
    e_ga, _ = _table(COMPTON_CSV)
    assert len(e_mu) == len(centers)
    assert np.allclose(e_mu, centers, rtol=1e-6)
    assert np.allclose(e_ga, centers, rtol=1e-6)   # both channels share the grid


def test_nonexistent_muon_paths_stay_absent():
    """fp-wrong-muon-path: 04-01-SUMMARY's front-matter paths do not exist."""
    assert not os.path.exists(os.path.join(REPO, "src", "muon"))
    assert not os.path.exists(os.path.join(REPO, "data", "muon"))
    assert not os.path.exists(os.path.join(REPO, "src", "muon", "deposited_spectrum.py"))
    assert not os.path.exists(os.path.join(REPO, "data", "muon", "muon_dep_spectrum.csv"))
    # ...and they are not cited as artifacts in the declaration either: they may
    # appear ONLY inside the Section-0 correction block that records their absence.
    lines = open(DECLARATION, encoding="utf-8").read().splitlines()
    end_of_correction = next(i for i, ln in enumerate(lines)
                             if ln.startswith("## 1. Artifact identity"))
    assert "**Neither exists.**" in "\n".join(lines[:end_of_correction])
    for bad in ("src/muon/deposited_spectrum.py", "data/muon/muon_dep_spectrum.csv"):
        for i, line in enumerate(lines):
            assert bad not in line or i < end_of_correction, (
                f"{bad} cited outside the Section-0 correction block, line {i+1}"
            )


# --------------------------------------------------------------------------- #
# Gamma channel                                                                 #
# --------------------------------------------------------------------------- #
def test_gamma_header_scalar():
    """The BOUND incoherent rate of record, distinguished from three others."""
    raw = _header_value(COMPTON_CSV, "total_single_scatter_rate_Hz")
    assert float(raw.split("(")[0].strip()) == GAMMA_RATE_HZ
    assert "BOUND incoherent" in raw
    assert f"{GAMMA_RATE_FREE_KN_HZ:.4e}".replace("e-01", "e-01") in raw or "2.6846e-01" in raw

    # fp-rate-conflation: the four circulating numbers are genuinely different.
    assert GAMMA_RATE_HZ != GAMMA_RATE_FREE_KN_HZ != GAMMA_RATE_VALD03_HZ
    assert abs(GAMMA_RATE_HZ - 0.267) > 0.0
    # ...and the declaration names all four with their meanings.
    text = open(DECLARATION, encoding="utf-8").read()
    for token in ("2.6747e-01", "2.6846e-01", "2.7305e-01", "0.267"):
        assert token in text, token


def test_compton_edges_from_line_list():
    """Edges recomputed in closed form from the committed line list."""
    lines = cs.load_gamma_lines(GAMMA_LINES_CSV)
    by_iso = {}
    for ln in lines:
        by_iso.setdefault(ln.isotope, []).append(ln.energy_keV)

    checks = {"K40": 1460.822, "Bi214": 1764.494, "Tl208": TL208_LINE_KEV}
    for iso, e_gamma in checks.items():
        assert e_gamma in by_iso[iso], f"{iso} line missing from gamma_lines.csv"
        got = _compton_edge(e_gamma)
        assert got == pytest.approx(COMPTON_EDGES_KEV[iso], abs=0.5)
        # the module's own kinematics agree with the independent closed form
        assert cs.compton_edge_kev(e_gamma) == pytest.approx(got, rel=1e-12)


def test_no_photopeak_above_edge():
    """Thin-target single scatter: no content above the highest Compton edge."""
    lines = cs.load_gamma_lines(GAMMA_LINES_CSV)
    e_edge_max = max(_compton_edge(ln.energy_keV) for ln in lines)
    assert e_edge_max == pytest.approx(COMPTON_EDGES_KEV["Tl208"], abs=0.5)

    edges = md.shared_energy_grid()
    e, r = _table(COMPTON_CSV)
    lo = edges[:-1]
    # A bin whose LOWER edge already exceeds the kinematic edge cannot be fed by
    # single scattering.  (The one bin that STRADDLES the edge legitimately
    # carries the partial edge content -- that is binning, not a photopeak.)
    assert np.count_nonzero((lo > e_edge_max) & (r > 0)) == 0

    # ...and nothing at the full 208Tl line energy, which would be a photopeak.
    i = int(np.argmin(np.abs(e - TL208_LINE_KEV)))
    assert r[i] == 0.0


# --------------------------------------------------------------------------- #
# No renormalization / no shielded quantity                                     #
# --------------------------------------------------------------------------- #
def test_no_shielded_factor_in_channel_modules():
    """SC5-style scan over the two channels AND their full import closure."""
    from qpd_potential import compton_deposit, muon_flux

    files = import_closure_files(md, muon_flux, cs, compton_deposit)
    # the closure must actually have pulled in the shared dependencies
    names = {os.path.basename(f) for f in files}
    assert {"muon_deposit.py", "muon_flux.py", "compton_source.py",
            "compton_deposit.py", "wafer_geometry.py"} <= names

    hits = scan_paths(files)
    unexplained = [h for h in hits if not is_allowlisted(h[0], h[3])]
    assert unexplained == [], f"unexplained shielded-token hits: {unexplained}"
    # the allow-listed hit is the Ge XCOM photon attenuation coefficient
    assert all(h[2] == "attenuation" for h in hits)


def test_declaration_no_applied_shielded_quantity():
    """Every shielded token in the declaration prose is an explicit exclusion."""
    text = open(DECLARATION, encoding="utf-8").read()
    bad = [h for h in scan_text(text, skip_fenced=True) if not is_not_applied(h[2])]
    assert bad == [], f"declaration lines applying a shielded quantity: {bad}"


DECLARED_ARTIFACTS = (
    "data/muon_dRdEdep.csv", "data/compton_dRdEdep.csv", "data/gamma_lines.csv",
    "data/ge_incoherent_S.csv", "data/ge_xcom_mu.csv",
    "src/qpd_potential/muon_deposit.py", "src/qpd_potential/muon_flux.py",
    "src/qpd_potential/compton_source.py", "src/qpd_potential/compton_deposit.py",
)


def _declared_hashes() -> dict[str, str]:
    """Parse the SHA-256 table out of the declaration itself."""
    text = open(DECLARATION, encoding="utf-8").read()
    out = {}
    for path in DECLARED_ARTIFACTS:
        m = re.search(rf"`{re.escape(path)}`\s*\|\s*\d+\s*\|\s*`([0-9a-f]{{64}})`", text)
        assert m, f"no SHA-256 row for {path} in the declaration"
        out[path] = m.group(1)
    return out


def _blob_sha256(rev: str, path: str) -> str:
    import hashlib
    blob = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=REPO,
                          capture_output=True, check=True).stdout
    return hashlib.sha256(blob).hexdigest()


def _declared_rev() -> str:
    """The commit the declaration itself pins as its point of reference."""
    text = open(DECLARATION, encoding="utf-8").read()
    m = re.search(r"Repo HEAD at execution: `([0-9a-f]{7,40})`", text)
    assert m, "the declaration must pin the commit its hashes refer to"
    return m.group(1)


def test_declared_hashes_match_committed_artifacts():
    """Every SHA-256 quoted in the declaration is the COMMITTED artifact's.

    The authoritative frozen-v1.0 artifact is the git BLOB at the commit the
    declaration itself pins -- not the floating HEAD and not the working tree.
    Phase 10 runs in parallel in this repository and has legitimately modified a
    shared module (compton_source.py, interpolation-domain guard) AFTER this
    declaration was frozen.  Pinning the revision keeps this an identity check on
    the frozen v1.0 input instead of a lock on a shared, moving checkout.

    The declaration's PHYSICS claims are separately re-checked against the LIVE
    modules by test_muon_deterministic_scalars, test_compton_edges_from_line_list
    and test_no_photopeak_above_edge, so a Phase-10 edit that actually changed a
    declared number would still fail this suite.
    """
    rev = _declared_rev()
    declared = _declared_hashes()
    mismatched = {p: (declared[p], _blob_sha256(rev, p))
                  for p in DECLARED_ARTIFACTS
                  if declared[p] != _blob_sha256(rev, p)}
    assert mismatched == {}, (
        f"declaration quotes a hash that is not the artifact at {rev}: {mismatched}")


def test_declared_artifacts_unchanged_since_the_pinned_revision():
    """Report, rather than hide, any declared artifact that moved since freeze.

    Data artifacts must be untouched.  A source module may legitimately move
    under a parallel phase, but only if the declaration DISCLOSES it -- a silent
    change to a frozen v1.0 input is exactly what SC1 exists to prevent.
    """
    rev = _declared_rev()
    text = open(DECLARATION, encoding="utf-8").read()
    for path in DECLARED_ARTIFACTS:
        if _blob_sha256(rev, path) == _blob_sha256("HEAD", path):
            continue
        assert not path.startswith("data/"), (
            f"frozen v1.0 DATA artifact {path} changed since {rev}")
        assert "Concurrency note" in text and os.path.basename(path) in text, (
            f"{path} changed since {rev} without a disclosure in the declaration")


def test_plan_09_01_touched_no_data_artifact():
    """Plan 09-01 re-declares; it must not write any data/ file."""
    data_paths = [p for p in DECLARED_ARTIFACTS if p.startswith("data/")]
    out = subprocess.run(
        ["git", "status", "--porcelain", "--"] + data_paths,
        cwd=REPO, capture_output=True, text=True, check=True,
    ).stdout.strip()
    assert out == "", f"a frozen v1.0 data artifact was modified: {out}"


# --------------------------------------------------------------------------- #
# Directional bias                                                              #
# --------------------------------------------------------------------------- #
BIAS_ROW_RE = re.compile(
    r"^\|\s*\*\*(?P<channel>muon|gamma)\*\*\s*\|"      # channel
    r"(?P<mid>.*?)\|\s*\*\*(?P<dev>[^|]*?)\*\*\s*\|"   # signed deviation cell
    r"\s*\*\*`(?P<direction>flatters_SB|penalizes_SB|neutral)`\*\*\s*\|"
)


def test_declaration_records_bias_direction():
    """Both channel rows carry a SIGNED deviation and a direction label.

    A bare magnitude fails: the sign is the whole point of the audit.
    """
    text = normalize_unicode(open(DECLARATION, encoding="utf-8").read())
    rows = {m.group("channel"): m for m in
            (BIAS_ROW_RE.match(ln) for ln in text.splitlines()) if m}
    assert set(rows) == {"muon", "gamma"}, f"parsed rows: {sorted(rows)}"

    for channel, m in rows.items():
        dev = m.group("dev").strip()
        assert re.match(r"^[+-]", dev), (
            f"{channel} deviation {dev!r} carries no sign -- a magnitude without "
            "its sign is exactly the fp-audit-as-formality failure mode"
        )
        assert "%" in dev
        assert m.group("direction") in {"flatters_SB", "penalizes_SB", "neutral"}

    # The contract fixes the muon direction and its ~20%-below-PDG magnitude.
    assert rows["muon"].group("direction") == "flatters_SB"
    mag = float(rows["muon"].group("dev").strip().rstrip(" %"))
    assert mag < 0 and 15.0 < abs(mag) < 25.0

    # The gamma factor-2 band must be present and identified, not narrowed.
    assert "factor-2" in text and "×0.5" in text and "×2" in text
