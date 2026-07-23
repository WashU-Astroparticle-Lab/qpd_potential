# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Plan 11-02, Task 2: IA width table and the counting-floor comparison figure.

Writes artifacts/v2.0/ia_broadening_widths.csv and
artifacts/v2.0/ia_width_vs_counting_floor.png.  Run with /opt/anaconda3/bin/python3.
"""
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from qpd_potential import ia_broadening as ia          # noqa: E402
from qpd_potential import muon_deposit as md           # noqa: E402
from qpd_potential import params as p                  # noqa: E402
from qpd_potential import phonon_scale as ps           # noqa: E402
from qpd_potential import trigger                      # noqa: E402

OUT = os.path.join(ROOT, "artifacts", "v2.0")
ROADMAP_ENERGIES = (0.1, 0.5, 1.0, 10.0, 100.0)
SC3_BANDS = {0.1: (0.35, 0.46), 0.5: (0.155, 0.205), 1.0: (0.11, 0.15), 100.0: (0.011, 0.015)}


def main():
    means = ia.vdos_means()
    corr = means["sigma_correction"]

    edges = md.shared_energy_grid("v2.0-ext") * 1e3          # keV -> eV
    centres = np.sqrt(edges[:-1] * edges[1:])
    energies = np.unique(np.concatenate([np.array(ROADMAP_ENERGIES), centres]))

    path = os.path.join(OUT, "ia_broadening_widths.csv")
    with open(path, "w") as fh:
        fh.write("# Impulse-approximation quantum broadening widths (plan 11-02, CALC-15).\n")
        fh.write("# sigma_E = sqrt(E_R * omega_bar) with the LOCKED omega_bar = %.10e eV\n"
                 % p.OMEGA_BAR_eV.value)
        fh.write("# (CONVENTIONS.md Section J; harmonic mean of the measured Ge VDOS).\n")
        fh.write("# frac_width = sigma_E/E_R = sqrt(omega_bar/E_R) = 1/sqrt(2W) -- an ALGEBRAIC\n")
        fh.write("# IDENTITY once 2W = E_R/omega_bar, NOT a cross-check (fp-identity-as-evidence).\n")
        fh.write("# frac_width_upper_moment uses the ARITHMETIC VDOS mean omega_bar_p = %.10e eV\n"
                 % means["omega_bar_p_eV"])
        fh.write("# which is what actually governs <p_x^2>; it is a ONE-SIDED correction of\n")
        fh.write("# x%.6f on every width, and it can only make the broadening LARGER.\n" % corr)
        fh.write("# counting_floor_* are the Phase-10 PIPELINE-DERIVED floors at %.5f eV\n"
                 % ia.COUNTING_FLOOR_ENERGY_eV)
        fh.write("# (16.009%% Ta->Al, 14.271%% Al->Hf), held CONSTANT across the table because\n")
        fh.write("# Phase 10 evaluated them only at that energy; they are NOT extrapolated.\n")
        fh.write("# %s\n" % ia.COUNTING_FLOOR_CAVEAT)
        fh.write("# quadrature_* = sqrt(frac_width^2 + floor^2), NEVER a linear sum; the two\n")
        fh.write("# mechanisms are ASSERTED independent (sensor counting statistics vs nuclear\n")
        fh.write("# zero-point motion), not proven so.\n")
        fh.write("# One extended-grid bin = %.10f fractional width; sigma_E/E_R falls below it\n"
                 % ia.ONE_BIN_FRACTIONAL_WIDTH)
        fh.write("# at E_R = %.6f eV.\n" % ia.sub_bin_crossing_energy_eV())
        fh.write("E_R_eV,sigma_E_eV,frac_width,two_W,frac_width_upper_moment,"
                 "counting_floor_TaAl,counting_floor_AlHf,quadrature_TaAl,quadrature_AlHf,"
                 "is_roadmap_energy\n")
        for E in energies:
            f = float(ia.fractional_width(E))
            fh.write("%.10e,%.10e,%.10e,%.10e,%.10e,%.6e,%.6e,%.10e,%.10e,%d\n" % (
                E, float(ia.sigma_E_eV(E)), f,
                float(ps.two_W_from_omega_bar(E, p.OMEGA_BAR_eV.value)),
                f * corr,
                ia.COUNTING_FLOOR_05eV["Ta->Al"], ia.COUNTING_FLOOR_05eV["Al->Hf"],
                ia.quadrature_with_counting_floor(f, "Ta->Al"),
                ia.quadrature_with_counting_floor(f, "Al->Hf"),
                int(any(abs(E - r) < 1e-12 for r in ROADMAP_ENERGIES)),
            ))
    print("wrote", path, len(energies), "rows")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    E = np.logspace(-1, 3, 800)
    f = ia.fractional_width(E)
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    ax.fill_between(E, f * 100, f * corr * 100, color="tab:blue", alpha=0.18,
                    label=r"moment systematic $\sqrt{\bar\omega_p/\bar\omega_u}=%.3f$ (ONE-SIDED, upward)" % corr)
    ax.loglog(E, f * 100, color="tab:blue", lw=2.2,
              label=r"IA width $\sigma_E/E_R=\sqrt{\bar\omega/E_R}$ (locked $\bar\omega=17.86$ meV)")
    ax.loglog(E, f * corr * 100, color="tab:blue", lw=1.0, ls=":")
    for d, c in (("Ta->Al", "tab:red"), ("Al->Hf", "tab:orange")):
        ax.plot(ia.COUNTING_FLOOR_ENERGY_eV, ia.COUNTING_FLOOR_05eV[d] * 100, "o", color=c, ms=7,
                label="Phase-10 counting floor %s = %.3f%% (BEST CASE, no noise sources)"
                      % (d, ia.COUNTING_FLOOR_05eV[d] * 100))
    ax.axhline(ia.ONE_BIN_FRACTIONAL_WIDTH * 100, color="grey", ls="--", lw=1.0)
    ax.text(300, ia.ONE_BIN_FRACTIONAL_WIDTH * 100 * 1.08,
            "one extended-grid bin (%.3f%%)" % (ia.ONE_BIN_FRACTIONAL_WIDTH * 100),
            fontsize=7.5, color="grey", ha="right")
    xc = ia.sub_bin_crossing_energy_eV()
    ax.plot([xc], [ia.ONE_BIN_FRACTIONAL_WIDTH * 100], "k*", ms=11)
    ax.annotate("sub-bin above\n%.1f eV" % xc, (xc, ia.ONE_BIN_FRACTIONAL_WIDTH * 100),
                textcoords="offset points", xytext=(6, -26), fontsize=7.5)
    ax.axvline(p.TRIGGER_E50.value, color="k", ls="-.", lw=1.0)
    ax.text(p.TRIGGER_E50.value * 1.06, 1.4, "trigger 50%% point %.1f eV" % p.TRIGGER_E50.value,
            rotation=90, fontsize=7.5, va="bottom")
    ax.axvline(trigger.SUBEV_REGIME_BOUNDARY_eV, color="k", ls=":", lw=1.0)
    ax.text(trigger.SUBEV_REGIME_BOUNDARY_eV * 1.06, 1.4,
            "sub-eV regime boundary %.1f eV" % trigger.SUBEV_REGIME_BOUNDARY_eV,
            rotation=90, fontsize=7.5, va="bottom")
    # where the IA width overtakes each floor
    for d, c in (("Ta->Al", "tab:red"), ("Al->Hf", "tab:orange")):
        Ex = p.OMEGA_BAR_eV.value / ia.COUNTING_FLOOR_05eV[d] ** 2
        ax.plot([Ex], [ia.COUNTING_FLOOR_05eV[d] * 100], "v", color=c, ms=6)
        ax.annotate("IA width = %s floor\nat %.2f eV" % (d, Ex),
                    (Ex, ia.COUNTING_FLOOR_05eV[d] * 100), textcoords="offset points",
                    xytext=(8, 8 if d == "Ta->Al" else -22), fontsize=7, color=c)
    ax.set_xlabel(r"nuclear recoil energy $E_R$ [eV]  (phonon scale, no quenching)")
    ax.set_ylabel(r"fractional width  $\sigma/E$  [%]")
    ax.set_title("IA quantum broadening vs the Phase-10 counting floor (Ge)", fontsize=10)
    ax.set_xlim(0.1, 1e3)
    ax.set_ylim(0.5, 80)
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=6.6, loc="upper right", framealpha=0.92)
    fig.tight_layout()
    figpath = os.path.join(OUT, "ia_width_vs_counting_floor.png")
    fig.savefig(figpath, dpi=160)
    print("wrote", figpath)

    print("\nSC3 verdicts (headline, locked omega_bar):")
    for E in ROADMAP_ENERGIES:
        f = float(ia.fractional_width(E))
        b = SC3_BANDS.get(E)
        v = "-" if b is None else ("IN BAND" if b[0] <= f <= b[1] else "OUT OF BAND")
        print("  %6.1f eV  %7.3f %%   band %s  -> %s   | moment-corrected %7.3f %% -> %s"
              % (E, 100 * f, b, v, 100 * f * corr,
                 "-" if b is None else ("in" if b[0] <= f * corr <= b[1] else "ABOVE BAND")))


if __name__ == "__main__":
    main()
