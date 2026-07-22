#!/usr/bin/env python
# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Generate artifacts/stage1/cevns_dRdT.csv (Phase 3, Plan 03-01).

Folds the frozen Phase-2 flagship flux (data/flux/reactor_flux_v1.0.csv, total
column) against the per-isotope Freedman dsigma/dT with the Helm form factor,
summed over the five natural-Ge isotopes on their own kinematic domains.

Output axis is DEPOSITED nuclear-recoil energy T = E_nr in eV_nr (NO ionization
quenching, NO detector response -- that is Phase 5). Rates in counts/kg/day/keV.
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from qpd_potential import cevns  # noqa: E402
from qpd_potential import params as p  # noqa: E402

OUT = os.path.join(
    os.path.dirname(__file__), "..", "artifacts", "stage1", "cevns_dRdT.csv"
)

N_GRID = 320


def main() -> None:
    flux = cevns.ReactorFlux()
    T_eV, per_iso, total, band = cevns.build_dRdT_table(flux, n_grid=N_GRID)

    # Closure/anchor diagnostics for the provenance header.
    direct = cevns.integrated_rate_direct(flux, use_form_factor=False)
    path = np.trapz(
        [cevns.differential_rate(t * 1e-3, flux, use_form_factor=False)
         for t in cevns.recoil_grid_eV(n=2000, T_min_eV=0.1, T_max_eV=3300.0)],
        cevns.recoil_grid_eV(n=2000, T_min_eV=0.1, T_max_eV=3300.0) * 1e-3,
    )
    sigma_anchor = cevns.sigma_tot_MeV(4.0, 32, 40)
    q200 = cevns.momentum_transfer_fm_inv(0.2, p.GE_ISOTOPES[1].M_MeV)
    F2_200 = cevns.helm_form_factor(q200, 72) ** 2
    q2k = cevns.momentum_transfer_fm_inv(2.0, p.GE_ISOTOPES[1].M_MeV)
    F2_2k = cevns.helm_form_factor(q2k, 72) ** 2

    # Integrated rate above 50 eV (with Helm F) for the header sanity line.
    Tg = cevns.recoil_grid_eV(n=2000, T_min_eV=50.0, T_max_eV=3300.0)
    rate_50 = np.trapz(
        [cevns.differential_rate(t * 1e-3, flux, use_form_factor=True) for t in Tg],
        Tg * 1e-3,
    )

    iso_names = [iso.name for iso in p.GE_ISOTOPES]
    header_cols = ["T_eV_nr"] + [f"dRdT_{n}" for n in iso_names] + [
        "dRdT_total", "dRdT_band_1sigma"
    ]

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        fh.write("# QPD Phase-3 Plan 03-01 -- CEvNS differential rate dR/dT on natural Ge\n")
        fh.write("# Deposited NUCLEAR-RECOIL energy axis (T = E_nr), NO quenching, NO response (Phase 5).\n")
        fh.write("# Rates: counts/kg/day/keV. Columns: per-isotope (5) + total + 1-sigma flux band.\n")
        fh.write("# Convention (CONVENTIONS Sec C, LOCKED): dsigma/dT = (G_F^2 M/4pi) Q_W^2 (1-MT/2E^2) F^2(q) (hbar c)^2;\n")
        fh.write("#   /4pi (not /8pi); Q_W = N-(1-4 sin^2thetaW)Z; sin^2thetaW=0.2387; (hbar c)^2=3.894e-28 GeV^2 cm^2.\n")
        fh.write("# Helm F (Lewin-Smith 1996): F(0)=1; F^2(200 eV,72Ge)=%.5f; F^2(2 keV,72Ge)=%.5f (endpoint tail).\n" % (F2_200, F2_2k))
        fh.write("# Flux: data/flux/reactor_flux_v1.0.csv v1.0 (FROZEN, git_sha eb7da23), total column,\n")
        fh.write("#   int Phi dE = 7.50e12 nu cm^-2 s^-1, 3 GW_th / 25 m; band from rel_uncertainty column.\n")
        fh.write("# Ge isotopes (Z=32): A=70/72/73/74/76, N=38/40/41/42/44,\n")
        fh.write("#   number-abundances 0.2057/0.2745/0.0775/0.3650/0.0773 (IUPAC/CIAAW), M_i=A*931.494 MeV,\n")
        fh.write("#   N_target,i = x_i * 8.29e24 /kg (sum = 8.29e24 /kg).\n")
        fh.write("# Closed-form closure: int(dR/dT)dT (F=1) = %.5f vs direct Sum_i N_i int Phi sigma_tot,i = %.5f counts/kg/day (rel %.2e).\n" % (path, direct, abs(path - direct) / direct))
        fh.write("# sigma(72Ge,4 MeV, full Q_W) = %.4e cm^2 (CONVENTIONS anchor ~1.0e-40).\n" % sigma_anchor)
        fh.write("# Integrated rate above 50 eV (with Helm F) = %.3f counts/kg/day (steeply falling; ~13-23 at 200-300 eV threshold).\n" % rate_50)
        fh.write("# Grid: %d log-spaced points, %.3g - %.4g eV_nr.\n" % (N_GRID, T_eV[0], T_eV[-1]))
        fh.write(",".join(header_cols) + "\n")
        for k in range(len(T_eV)):
            row = [f"{T_eV[k]:.6e}"]
            row += [f"{per_iso[n][k]:.6e}" for n in iso_names]
            row += [f"{total[k]:.6e}", f"{band[k]:.6e}"]
            fh.write(",".join(row) + "\n")

    print(f"wrote {OUT}: {len(T_eV)} rows")
    print(f"closure rel = {abs(path-direct)/direct:.2e}; sigma(72Ge,4MeV)={sigma_anchor:.4e}")
    print(f"F^2(200eV)={F2_200:.5f}  F^2(2keV)={F2_2k:.5f}  rate>50eV={rate_50:.3f}/kg/day")


if __name__ == "__main__":
    main()
