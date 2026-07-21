#!/usr/bin/env python3
# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Generate the environmental-gamma Compton deposited-energy spectrum dR/dE_dep
(Plan 04-02).

Runs the Klein-Nishina angle-sampled electron-recoil continuum with a FIXED seed,
writes data/compton_dRdEdep.csv on the SHARED log E_dep grid (identical to 04-01),
and (if matplotlib is available) a log-log check figure figs/compton_dep_check.png
with the located Compton edges marked against the computed Klein-Nishina positions.

Reproducible: python scripts/make_compton_spectrum.py
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from qpd_potential import compton_deposit as cd  # noqa: E402
from qpd_potential import compton_source as cs    # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_PATH = os.path.join(ROOT, "data", "compton_dRdEdep.csv")
FIG_PATH = os.path.join(ROOT, "figs", "compton_dep_check.png")

SEED = 20260720
N_PER_LINE = 400_000


def main() -> None:
    spec = cd.run_compton_mc(n_per_line=N_PER_LINE, seed=SEED)
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    cd.write_csv(spec, CSV_PATH)

    ratio = spec.rate_hz / spec.rate_anchor_hz
    print(f"total single-scatter rate = {spec.rate_hz:.4e} Hz "
          f"({spec.rate_hz * 86400:.3e} /day in the {cs.MASS_KG * 1e3:.0f} g wafer)")
    print(f"flux x sigma_KN x N_e anchor = {spec.rate_anchor_hz:.4e} Hz  "
          f"ratio = {ratio:.3f} (VALD-03 factor ~2)")
    print(f"int dR/dE_dep = {spec.counts_per_kg_day:.4e} counts/kg/day (energy closure)")
    print(f"single-scatter mu*ellbar @1MeV = {float(cs.optical_depth_mean_chord(1000)):.4f}, "
          f"@2MeV = {float(cs.optical_depth_mean_chord(2000)):.4f}; "
          f"double-scatter@1MeV = {float(cs.double_scatter_fraction(1000)):.4f}")
    print("VALD-03 edges (E_gamma -> E_edge keV):")
    for eg, ed in sorted(zip(spec.line_energies, spec.line_edges)):
        print(f"   {eg:8.1f} -> {ed:8.1f}")
    print(f"wrote {CSV_PATH}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover - plotting optional
        print(f"[skip figure] matplotlib unavailable: {exc}")
        return

    c, y, e = spec.centers_kev, spec.dRdE, spec.dRdE_err
    mask = y > 0
    fig, ax = plt.subplots(figsize=(8.0, 5.2))
    ax.errorbar(c[mask], y[mask], yerr=e[mask], fmt="o", ms=2.2, lw=0.6,
                color="#2a7f4f", ecolor="#a7d3b6",
                label="Compton dR/dE_dep (KN electron continuum)")
    # Mark the named VALD-03 edges.
    named = {1460.822: "$^{40}$K", 2614.511: "$^{208}$Tl", 1764.494: "$^{214}$Bi"}
    for eg, lab in named.items():
        ed = float(cs.compton_edge_kev(eg))
        ax.axvline(ed, color="#d1495b", ls="--", lw=1.1)
        ax.text(ed, ax.get_ylim()[1] if False else np.nanmax(y[mask]) * 0.5,
                f"{lab} edge\n{ed:.0f} keV", fontsize=7, color="#d1495b",
                ha="right", rotation=90, va="top")
    # Show that E_gamma of the top line has NO photopeak.
    ax.axvline(2614.511, color="#666666", ls=":", lw=1.0)
    ax.text(2614.511, np.nanmax(y[mask]) * 0.02, "  $E_\\gamma$(2614.5): no peak",
            fontsize=7, color="#666666", ha="left", va="bottom", rotation=90)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("deposited (phonon) energy  E_dep  [keV]  -- no quenching")
    ax.set_ylabel(r"dR/dE$_{\rm dep}$  [counts kg$^{-1}$ day$^{-1}$ keV$^{-1}$]")
    ax.set_title("Environmental-gamma Compton deposited-energy spectrum, 110 g Ge wafer\n"
                 f"electron-recoil continuum (no photopeaks); rate {spec.rate_hz:.3f} Hz "
                 f"(anchor {spec.rate_anchor_hz:.3f} Hz, ratio {ratio:.2f})")
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(True, which="both", alpha=0.25)
    fig.tight_layout()
    os.makedirs(os.path.dirname(FIG_PATH), exist_ok=True)
    fig.savefig(FIG_PATH, dpi=140)
    print(f"wrote {FIG_PATH}")


if __name__ == "__main__":
    main()
