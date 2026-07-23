# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Plan 11-04, Task 2: the IA-broadened CEvNS recoil spectrum and its leakage budget.

Writes artifacts/v2.0/cevns_dRdT_broadened.csv and
artifacts/v2.0/ia_broadening_leakage_budget.csv.  Run with /opt/anaconda3/bin/python3.

WHY dR/dT IS RECOMPUTED RATHER THAN READ.  The frozen v1.0 table
artifacts/stage1/cevns_dRdT.csv starts at T = 5 eV and carries NO DATA below it (its
disposition-register row records validity_floor = 5.0 eV).  Broadening it down to the
0.0999350 eV extended-grid floor would be extrapolation into a region the table never
covered -- exactly fp-silent-carry.  cevns.differential_rate is evaluated directly
instead: that is a RECOMPUTATION of the same physics on a wider axis, not an
extension of a frozen artifact.  ia_broadening.broaden_native_spectrum RAISES if
asked to do the other thing (require_floor_coverage=True).
"""
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from qpd_potential import cevns                       # noqa: E402
from qpd_potential import ia_broadening as ia         # noqa: E402
from qpd_potential import impulse_limit as il         # noqa: E402
from qpd_potential import params as p                 # noqa: E402

OUT = os.path.join(ROOT, "artifacts", "v2.0")
FLOOR = il.EXT_GRID_FLOOR_eV
TOP = 3200.0
N = 480


def main():
    edges = np.geomspace(FLOOR, TOP, N + 1)
    T = np.sqrt(edges[:-1] * edges[1:])
    dE_keV = np.diff(edges) / 1.0e3

    flux = cevns.ReactorFlux()
    y = np.array([cevns.differential_rate(t * 1e-3, flux) for t in T])
    band = np.array([cevns.differential_rate_band(t * 1e-3, flux) for t in T])

    counts_in = y * dE_keV
    band_in = band * dE_keV
    w_u = p.OMEGA_BAR_eV.value
    w_p = ia.vdos_means()["omega_bar_p_eV"]

    out_c, leak = ia.broaden_counts(edges, counts_in, omega_bar_eV=w_u)
    out_b, _ = ia.broaden_counts(edges, band_in, omega_bar_eV=w_u)
    out_up, leak_up = ia.broaden_counts(edges, counts_in, omega_bar_eV=w_p)

    total_in = counts_in.sum()
    total_out = out_c.sum() + leak["below_floor"] + leak["above_top"]
    residual = total_out / total_in - 1.0

    # ---------------- broadened spectrum ---------------- #
    path = os.path.join(OUT, "cevns_dRdT_broadened.csv")
    with open(path, "w") as fh:
        fh.write("# CEvNS dR/dT with impulse-approximation quantum broadening (plan 11-04, CALC-15).\n")
        fh.write("# Recoil (nuclear) energy axis on the unified phonon scale, NO quenching; never keVee.\n")
        fh.write("# %d log bins from the extended-grid floor %.7f eV to %.1f eV.\n" % (N, FLOOR, TOP))
        fh.write("# dR/dT RECOMPUTED from cevns.differential_rate, NOT extrapolated from the\n")
        fh.write("# frozen artifacts/stage1/cevns_dRdT.csv, whose support stops at 5 eV.\n")
        fh.write("# Kernel: Gaussian of width sigma_E(T) = sqrt(T * omega_bar), applied on the\n")
        fh.write("# RECOIL axis UPSTREAM of fold.rebin_cevns_to_edep_grid and of R(E_rec|E_dep).\n")
        fh.write("# CENTRAL column uses the LOCKED omega_bar = %.10e eV (harmonic VDOS mean,\n" % w_u)
        fh.write("# CONVENTIONS.md Section J).\n")
        fh.write("# The *_upper column is the ONE-SIDED moment systematic: sigma_E is really\n")
        fh.write("# governed by the ARITHMETIC VDOS mean omega_bar_p = %.10e eV (plan 11-02,\n" % w_p)
        fh.write("# independently confirmed by plan 11-03's exact second central moment of\n")
        fh.write("# S(q,omega)). The correction is x%.6f on the width and can only make the\n"
                 % np.sqrt(w_p / w_u))
        fh.write("# broadening LARGER, so it is carried as an upper band and is NOT absorbed\n")
        fh.write("# into the central value (fp-absorb-systematic). There is no lower band.\n")
        fh.write("# Counts are NOT rescaled after the convolution: mass leaving the axis is\n")
        fh.write("# reported in ia_broadening_leakage_budget.csv (fp-rescale-to-conserve).\n")
        fh.write("# The rate is NEVER multiplied by exp(-2W) (fp-dw-suppression).\n")
        fh.write("T_eV,dRdT_unbroadened,dRdT_broadened,dRdT_broadened_upper,"
                 "dRdT_band_unbroadened,dRdT_band_broadened\n")
        for i in range(len(T)):
            fh.write("%.10e,%.10e,%.10e,%.10e,%.10e,%.10e\n" % (
                T[i], y[i], out_c[i] / dE_keV[i], out_up[i] / dE_keV[i],
                band[i], out_b[i] / dE_keV[i]))
    print("wrote", path)

    # ---------------- leakage budget ---------------- #
    running = np.cumsum(out_c + leak["below_floor_per_bin"] + leak["above_top_per_bin"]
                        - counts_in)
    lpath = os.path.join(OUT, "ia_broadening_leakage_budget.csv")
    with open(lpath, "w") as fh:
        fh.write("# IA broadening leakage budget (plan 11-04, ROADMAP Phase 11 SC4).\n")
        fh.write("# Per SOURCE bin: the counts that entered, the kernel width used, and the\n")
        fh.write("# mass that left the axis at each end. counts_out is the mass DELIVERED to\n")
        fh.write("# the same-index target bin, so it does not balance row by row -- the budget\n")
        fh.write("# closes on the COLUMN totals, which is what SC4's <=1e-3 is checked against.\n")
        fh.write("# below_zero is a SUBSET of below_floor (the part at T < 0, where the true\n")
        fh.write("# T->0 S(q,omega) vanishes identically -- see plan 11-03).\n")
        fh.write("# NOTHING IS RESCALED. Leakage is accounted, not removed. A zero entry in the\n")
        fh.write("# bottom decade would be evidence of a clipped kernel or a hidden rescale.\n")
        fh.write("# TOTALS: input %.10e, retained %.10e, below_floor %.10e (%.6f%%),\n"
                 % (total_in, out_c.sum(), leak["below_floor"], 100 * leak["below_floor"] / total_in))
        fh.write("#         below_zero %.10e (%.6f%%), above_top %.10e, residual %.3e\n"
                 % (leak["below_zero"], 100 * leak["below_zero"] / total_in,
                    leak["above_top"], residual))
        fh.write("T_eV,sigma_E_eV,counts_in,counts_out,below_floor,below_zero,above_top,running_residual\n")
        for i in range(len(T)):
            fh.write("%.10e,%.10e,%.10e,%.10e,%.10e,%.10e,%.10e,%.10e\n" % (
                T[i], leak["sigma_eV"][i], counts_in[i], out_c[i],
                leak["below_floor_per_bin"][i], leak["below_zero_per_bin"][i],
                leak["above_top_per_bin"][i], running[i]))
    print("wrote", lpath)

    # ---------------- report ---------------- #
    bot = T < 1.0
    print("\nCONSERVATION")
    print("  input counts            %.10e counts/kg/day" % total_in)
    print("  retained on the axis    %.10e  (%.6f %%)" % (out_c.sum(), 100 * out_c.sum() / total_in))
    print("  leaked below the floor  %.10e  (%.6f %%)" % (leak["below_floor"], 100 * leak["below_floor"] / total_in))
    print("     of which at T < 0    %.10e  (%.6f %%)" % (leak["below_zero"], 100 * leak["below_zero"] / total_in))
    print("  leaked above the top    %.10e" % leak["above_top"])
    print("  RESIDUAL (retained+leaked)/input - 1 = %.3e   target <= 1e-3" % residual)
    print("  retained-ONLY residual               = %.6e  (must MISS)"
          % (out_c.sum() / total_in - 1.0))
    print("  bottom-decade share of the sub-floor leakage: %.6f %%"
          % (100 * leak["below_floor_per_bin"][bot].sum() / leak["below_floor"]))
    print("\nBOTTOM BIN (T = %.7f eV, sigma_E = %.6f eV)" % (T[0], leak["sigma_eV"][0]))
    pred = il.gaussian_offgrid_weights(T[0], floor_eV=FLOOR)
    print("  measured below_floor fraction %.6f   plan 11-03 analytic %.6f   ratio %.5f"
          % (leak["below_floor_per_bin"][0] / counts_in[0], pred["weight_below_floor"],
             (leak["below_floor_per_bin"][0] / counts_in[0]) / pred["weight_below_floor"]))
    print("  measured below_zero  fraction %.6e   plan 11-03 analytic %.6e   ratio %.5f"
          % (leak["below_zero_per_bin"][0] / counts_in[0], pred["weight_below_zero"],
             (leak["below_zero_per_bin"][0] / counts_in[0]) / pred["weight_below_zero"]))
    print("\nMOMENT BAND: upper/central integrated-count ratio on the retained axis = %.6f"
          % (out_up.sum() / out_c.sum()))
    print("  upper-kernel sub-floor leakage %.6f %% vs central %.6f %%"
          % (100 * leak_up["below_floor"] / total_in, 100 * leak["below_floor"] / total_in))


if __name__ == "__main__":
    main()
