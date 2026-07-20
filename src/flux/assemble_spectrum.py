# ASSERT_CONVENTION: natural_units=io_MeV, energy_input=MeV, spectrum_units=nubar_per_fission_per_MeV
"""
Assemble the component-wise per-fission reactor antineutrino spectrum S_i(E_nu) on a
fixed log energy grid (0.1-10 MeV), stitching:

    * Huber-Mueller (data-anchored, SOURCED coefficients)   for E_nu >= 2.0 MeV
    * seam-matched summation extension (MODEL PLACEHOLDER)   for E_nu <= 1.8 MeV
    * a C1 monotone blend                                    across 1.8-2.0 MeV
    * the 238U(n,gamma) capture component kept as a SEPARATE additive column.

Seam match:  c_i = integral_{2-3 MeV} S_i^HM / integral_{2-3 MeV} S_i^sum   (per isotope).
Blend:       quintic smoothstep in log-flux (C1: value and first derivative continuous).
Interp:      summation tabulated coarsely then PCHIP-interpolated in LOG-flux (monotone;
             guards fp-negative-spline -> no ringing / no negative flux).

Forbidden proxies actively guarded:
    fp-truncate-ibd   : sub-1.8 MeV flux is populated (not dropped / not power-law HM).
    fp-invented-coeffs: HM coefficients loaded from the provenance-tagged CSV.
    fp-negative-spline: PCHIP-in-log interpolation; non-negativity asserted on the grid.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict

import numpy as np
from scipy.interpolate import PchipInterpolator

from .huber_mueller import (
    ISOTOPES,
    load_coefficients,
    hm_spectrum,
    hm_log_slope,
)
from .summation_ncapture import (
    ncapture_spectrum,
    summation_shape_placeholder,
)

SEAM_LO = 1.8       # MeV, bottom of the blend / top of pure-summation region
SEAM_HI = 2.0       # MeV, top of the blend / bottom of pure-HM region
OVERLAP = (2.0, 3.0)  # MeV, window for the per-isotope seam-scale c_i

# Default cycle-averaged PWR fission fractions (isotope-labelled explicitly).
FISSION_FRACTIONS_DEFAULT: Dict[str, float] = {"235U": 0.58, "238U": 0.07, "239Pu": 0.30, "241Pu": 0.05}
# Billard 2017 benchmark set (235/239/238/241 = 55.6/32.6/7.1/4.7 %), isotope-labelled.
FISSION_FRACTIONS_BILLARD: Dict[str, float] = {"235U": 0.556, "239Pu": 0.326, "238U": 0.071, "241Pu": 0.047}


def build_energy_grid(e_lo=0.1, e_hi=10.0, per_decade=25, dense_below=2.0, extra=40) -> np.ndarray:
    """Log grid 0.1-10 MeV (>=20 pts/decade) with extra density below 2 MeV."""
    n = int(np.ceil(per_decade * np.log10(e_hi / e_lo)))
    base = np.logspace(np.log10(e_lo), np.log10(e_hi), max(n, 60))
    dense = np.logspace(np.log10(e_lo), np.log10(dense_below), extra)
    grid = np.unique(np.concatenate([base, dense, [SEAM_LO, SEAM_HI, OVERLAP[0], OVERLAP[1]]]))
    return grid[(grid >= e_lo) & (grid <= e_hi)]


def _smoothstep5(t):
    """Quintic smoothstep: 0->1 with zero 1st and 2nd derivative at t=0,1 (C1+ blend)."""
    t = np.clip(t, 0.0, 1.0)
    return t * t * t * (t * (6 * t - 15) + 10)


@dataclass
class AssembledSpectrum:
    E: np.ndarray
    per_isotope: Dict[str, np.ndarray]        # seam-joined S_i(E) (fission), by isotope
    hm_component: Dict[str, np.ndarray]        # HM-only contribution (>=2 MeV region)
    summation_component: Dict[str, np.ndarray] # seam-matched summation contribution (<2 MeV)
    ncapture: np.ndarray                       # 238U(n,gamma), additive, per fission
    fractions: Dict[str, float] = field(default_factory=lambda: dict(FISSION_FRACTIONS_DEFAULT))

    def fission_weighted(self) -> np.ndarray:
        """sum_i f_i S_i(E)  (fission component only, no n-capture)."""
        out = np.zeros_like(self.E)
        for iso, f in self.fractions.items():
            out = out + f * self.per_isotope[iso]
        return out

    def total(self) -> np.ndarray:
        """Fission-weighted spectrum + n-capture (n-capture is not fission-fraction weighted)."""
        return self.fission_weighted() + self.ncapture

    def integral_yields(self) -> Dict[str, float]:
        E = self.E
        fw = self.fission_weighted()
        total_fission = float(np.trapz(fw, E))
        above = E >= SEAM_LO
        above_18 = float(np.trapz(fw[above], E[above]))
        cap = float(np.trapz(self.ncapture, E))
        return {
            "total_fission_per_fission": total_fission,
            "above_1p8_per_fission": above_18,
            "below_1p8_per_fission": total_fission - above_18,
            "ncapture_per_fission": cap,
            "grand_total_per_fission": total_fission + cap,
        }


def assemble(fractions: Dict[str, float] | None = None, grid: np.ndarray | None = None) -> AssembledSpectrum:
    if fractions is None:
        fractions = dict(FISSION_FRACTIONS_DEFAULT)
    if grid is None:
        grid = build_energy_grid()
    E = grid
    coeffs = load_coefficients()

    per_iso, hm_only, sum_only = {}, {}, {}
    # coarse tabulation grid for the summation placeholder (to exercise PCHIP-in-log)
    E_tab = np.logspace(np.log10(0.1), np.log10(3.0), 40)

    for iso in ISOTOPES:
        a = coeffs[iso]
        S_hm = hm_spectrum(E, a)

        # summation placeholder shape uses this isotope's HM log-slope at the seam (C1 anchor)
        slope2 = float(hm_log_slope(SEAM_HI, a))
        s_tab = summation_shape_placeholder(E_tab, slope2)
        # PCHIP in log-flux (monotone -> no negative flux / ringing; fp-negative-spline guard)
        pchip_log = PchipInterpolator(E_tab, np.log(s_tab), extrapolate=True)
        S_sum_raw = np.exp(pchip_log(E))

        # per-isotope seam scale c_i on the 2-3 MeV overlap
        mask = (E >= OVERLAP[0]) & (E <= OVERLAP[1])
        c_i = float(np.trapz(S_hm[mask], E[mask]) / np.trapz(S_sum_raw[mask], E[mask]))
        S_sum = c_i * S_sum_raw

        # piecewise assembly with C1 quintic-smoothstep blend in log-flux across the seam
        S = np.empty_like(E)
        below = E <= SEAM_LO
        above = E >= SEAM_HI
        blend = (~below) & (~above)
        S[below] = S_sum[below]
        S[above] = S_hm[above]
        t = (E[blend] - SEAM_LO) / (SEAM_HI - SEAM_LO)
        w = _smoothstep5(t)
        S[blend] = np.exp((1 - w) * np.log(S_sum[blend]) + w * np.log(S_hm[blend]))

        assert np.all(S > 0), f"negative/zero flux for {iso}"
        per_iso[iso] = S
        # component bookkeeping: HM contribution above seam, summation contribution below
        hm_only[iso] = np.where(E >= SEAM_HI, S, 0.0)
        sum_only[iso] = np.where(E <= SEAM_LO, S, 0.0)

    cap = ncapture_spectrum(E)
    assert np.all(cap >= 0)

    return AssembledSpectrum(
        E=E, per_isotope=per_iso, hm_component=hm_only, summation_component=sum_only,
        ncapture=cap, fractions=dict(fractions),
    )


def write_component_csv(spec: AssembledSpectrum, path: str) -> None:
    """Write the component-wise per-fission spectrum with a provenance header."""
    E = spec.E
    fw = spec.fission_weighted()
    with open(path, "w") as f:
        f.write("# QPD Phase-2 Plan 02-01 -- component-wise PER-FISSION antineutrino spectrum\n")
        f.write("# Units: nu-bar / fission / MeV ; E_nu in MeV. Grid: log 0.1-10 MeV, dense below 2 MeV.\n")
        f.write("# Components: HM fission (>2 MeV, SOURCED Huber arXiv:1106.0687 / Mueller arXiv:1101.2663);\n")
        f.write("#   summation fission (<1.8 MeV, seam-matched) = MODEL PLACEHOLDER (EF/CONFLUX table not\n")
        f.write("#   sourced in-environment -- SOURCING GAP, replace in Plan 02-02); C1 blend on 1.8-2.0 MeV.\n")
        f.write("#   ncapture_238U = 238U(n,gamma) allowed-beta shape (AME2020 Q-values) normalized to\n")
        f.write("#   0.6 nu-bar/fission (Kopeikin 2004 / Huber-Jaffke 2016).\n")
        f.write(f"# Fission fractions (isotope-labelled): {spec.fractions}\n")
        cols = ["E_nu_MeV", "fission_weighted"] + [f"S_{iso}" for iso in ISOTOPES] + ["ncapture_238U", "region_flag"]
        f.write(",".join(cols) + "\n")
        for k, e in enumerate(E):
            region = "above_2MeV" if e >= SEAM_HI else ("below_1p8MeV" if e <= SEAM_LO else "seam")
            row = [f"{e:.6g}", f"{fw[k]:.6g}"] + [f"{spec.per_isotope[iso][k]:.6g}" for iso in ISOTOPES]
            row += [f"{spec.ncapture[k]:.6g}", region]
            f.write(",".join(row) + "\n")


if __name__ == "__main__":
    spec = assemble()
    y = spec.integral_yields()
    for k, v in y.items():
        print(f"{k:32s} {v:.3f}")
    out = os.path.join(os.path.dirname(__file__), "..", "..", "data", "flux", "perfission_spectrum.csv")
    write_component_csv(spec, os.path.normpath(out))
    print("wrote", os.path.normpath(out))
