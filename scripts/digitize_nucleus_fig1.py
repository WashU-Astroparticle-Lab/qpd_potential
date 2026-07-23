#!/usr/bin/env python3
"""Digitize the germanium curve of NUCLEUS (2019) Fig. 1 into a frozen CSV.

Source: G. Angloher et al. (NUCLEUS Collaboration), "Exploring CEvNS with
NUCLEUS at the Chooz nuclear power plant", Eur. Phys. J. C 79, 1018 (2019),
doi:10.1140/epjc/s10052-019-7454-4.  Figure 1, page 2, dash-dotted RED curve
(germanium).  Axes: x = E_R [eV] (log, 1e0..1e4), y = counts/(keV kg day)
(log, ~1e0..1e3+).

The paper is NOT redistributable, so it is not vendored into the repo; pass the
local PDF path on the command line.  The output CSV records the PDF sha256 so a
later re-run can be checked against the same source file.

Method: render page 2 at 300 dpi (pdftoppm), locate the plot box and the four
decade gridlines to calibrate both log axes, then take, for each pixel column,
the mean row of saturated-red pixels.  Columns whose red pixels span > 12 rows
are dropped (that is the dash-dot ink of a near-vertical segment, or overlap
with the legend swatch), as are all columns inside the legend box.

Digitization accuracy is limited by the printed line width (~3 px approx 3% in
rate) and by dash gaps; treat the output as good to ~5%, degrading above
~700 eV where the curve is steep and near the plot floor.

Usage:
    python scripts/digitize_nucleus_fig1.py ~/Downloads/s10052-019-7454-4.pdf
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

# Expected calibration landmarks in the 300-dpi render of page 2 (pixels).
# Auto-detected below; these are the assertions that the render matched.
_EXPECT_XSPINE = (416.5, 1097.5)      # columns of E_R = 1e0 and 1e4
_EXPECT_DECADES = (294.5, 394.0, 492.0, 589.0)   # rows of 1e3, 1e2, 1e1, 1e0
_TOL_PX = 3.0

_OUT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "data", "external", "nucleus2019_fig1_ge.csv",
)


def _render_page2(pdf_path: str, outdir: str) -> str:
    subprocess.run(
        ["pdftoppm", "-f", "2", "-l", "2", "-r", "300", "-png", pdf_path,
         os.path.join(outdir, "p2")],
        check=True,
    )
    pngs = [f for f in os.listdir(outdir) if f.endswith(".png")]
    if len(pngs) != 1:
        raise RuntimeError(f"expected 1 rendered page, got {pngs}")
    return os.path.join(outdir, pngs[0])


def _calibrate(a: np.ndarray):
    """Return (col_1eV, px_per_decade_x, row_1e3, px_per_decade_y)."""
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    dark = (r < 120) & (g < 120) & (b < 120)

    # Vertical spines of the plot box: the two columns with the most dark ink
    # in the figure region.
    region = dark[200:1000, 150:1350]
    colsum = region.sum(axis=0)
    spines = sorted(i + 150 for i, c in enumerate(colsum) if c > 300)
    x_lo = float(np.mean([c for c in spines if c < 700]))
    x_hi = float(np.mean([c for c in spines if c >= 700]))

    # Horizontal decade gridlines (gray, inside the box).
    box = a[230:625, 418:1096]
    br, bg, bb = box[:, :, 0], box[:, :, 1], box[:, :, 2]
    grid = (abs(br - bg) < 12) & (abs(bg - bb) < 12) & (br < 190)
    rows = [i + 230 for i, c in enumerate(grid.sum(axis=1)) if c > 400]
    # Cluster consecutive rows; drop the box top/bottom spines (extremes).
    clusters, cur = [], [rows[0]]
    for v in rows[1:]:
        if v - cur[-1] <= 2:
            cur.append(v)
        else:
            clusters.append(float(np.mean(cur)))
            cur = [v]
    clusters.append(float(np.mean(cur)))
    decades = clusters[1:-1]   # strip the frame lines

    if abs(x_lo - _EXPECT_XSPINE[0]) > _TOL_PX or abs(x_hi - _EXPECT_XSPINE[1]) > _TOL_PX:
        raise RuntimeError(f"x spines {x_lo},{x_hi} != expected {_EXPECT_XSPINE}")
    if len(decades) != 4 or max(
        abs(d - e) for d, e in zip(decades, _EXPECT_DECADES)
    ) > _TOL_PX:
        raise RuntimeError(f"y decades {decades} != expected {_EXPECT_DECADES}")

    dx = (x_hi - x_lo) / 4.0            # 1e0 -> 1e4
    dy = (decades[-1] - decades[0]) / 3.0   # 1e3 -> 1e0
    return x_lo, dx, decades[0], dy


def digitize(pdf_path: str):
    with tempfile.TemporaryDirectory() as td:
        png = _render_page2(pdf_path, td)
        a = np.array(Image.open(png).convert("RGB")).astype(int)

    x0, dx, y0, dy = _calibrate(a)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    red = (r > 150) & (g < 100) & (b < 100)

    E, R = [], []
    for c in range(int(x0) + 2, 1096):
        rows = [
            i for i in range(232, 618)
            if red[i, c] and not (c > 755 and i < 432)   # legend box exclusion
        ]
        if not rows or (max(rows) - min(rows)) >= 12:
            continue
        E.append(10.0 ** ((c - x0) / dx))
        R.append(10.0 ** (3.0 + (y0 - float(np.mean(rows))) / dy))
    return np.array(E), np.array(R), (x0, dx, y0, dy)


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    pdf_path = os.path.expanduser(sys.argv[1])
    sha = hashlib.sha256(open(pdf_path, "rb").read()).hexdigest()
    E, R, cal = digitize(pdf_path)

    os.makedirs(os.path.dirname(_OUT), exist_ok=True)
    with open(_OUT, "w") as fh:
        fh.write(
            "# Digitized germanium (dash-dotted red) curve of NUCLEUS Fig. 1.\n"
            "# Source: G. Angloher et al. (NUCLEUS Collab.), Eur. Phys. J. C 79, 1018 (2019),\n"
            "#   arXiv:1905.10258, doi:10.1140/epjc/s10052-019-7454-4, Fig. 1 (page 2).\n"
            f"# source_pdf_sha256: {sha}\n"
            f"# digitizer: scripts/digitize_nucleus_fig1.py (300 dpi pdftoppm render)\n"
            f"# axis calibration (px): col(1 eV)={cal[0]:.1f} dx/decade={cal[1]:.2f} "
            f"row(1e3)={cal[2]:.1f} dy/decade={cal[3]:.2f}\n"
            "# Columns: E_R in eV (nuclear recoil), dR/dE_R in counts/(keV kg day).\n"
            "# NOT primary data -- digitized from a printed figure; accurate to ~5%\n"
            "# below ~700 eV, worse above (steep curve, sparse dash-dot, plot floor).\n"
            "# NUCLEUS assumptions behind this curve (from the paper text):\n"
            "#   two Chooz-B cores, 4.25 GW_th each, at 72 m and 102 m;\n"
            "#   6 nu-bar/fission at 200 MeV/fission -> ~8e20 nu-bar/s per core;\n"
            "#   flux shape Tengblad Nucl. Phys. A 503, 136 (1989) as parameterized in\n"
            "#   A. Guetlein, Dissertation, TU Muenchen (2013);\n"
            "#   dsigma/dE_R = G_F^2/(4 pi) Q_W^2 F^2(q) m_N (1 - E_R/E_R^max)  [their Eq. 1].\n"
            "E_R_eV,dRdE_counts_per_keV_kg_day\n"
        )
        for e, v in zip(E, R):
            fh.write(f"{e:.6e},{v:.6e}\n")

    print(f"wrote {_OUT}: {len(E)} points, "
          f"E_R {E.min():.2f}-{E.max():.0f} eV, rate {R.max():.4g}-{R.min():.4g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
