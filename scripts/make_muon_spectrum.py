#!/usr/bin/env python3
# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Generate the muon deposited-energy spectrum dR/dE_dep (Plan 04-01).

Runs the Gaisser-Guan (x) ray-box chord (x) Landau-Vavilov MPV Monte Carlo with a
FIXED seed, writes data/muon_dRdEdep.csv on the shared log E_dep grid, and (if
matplotlib is available) a log-log check figure figs/muon_dep_check.png.

Reproducible: python scripts/make_muon_spectrum.py
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from qpd_potential import muon_deposit as md  # noqa: E402
from qpd_potential import wafer_geometry as g  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_PATH = os.path.join(ROOT, "data", "muon_dRdEdep.csv")
FIG_PATH = os.path.join(ROOT, "figs", "muon_dep_check.png")

# N raised from 4e6 -> 1e9 (statistics refinement, 2026-07-21): the muon
# deposited-energy spectrum is now well-sampled across the full plotted range so
# the sparse low-deposit tail (which feeds the low-E_rec deliverable tail) is no
# longer ~1-event-per-bin Poisson noise. run_muon_mc accumulates in memory-bounded
# batches with per-batch child seeds spawned from SEED, so this is reproducible.
# Physics, weighting, shared grid, and Landau/chord/flux models are UNCHANGED --
# only the sample count and the batched accumulation changed.
#
# Achieved per-bin MC error (see 04-01 refinement note): the dominant deposited
# spectrum (E_dep ~4 keV -> 200 MeV, where the pile-up + physics live) is <~4%;
# the FOLDED deliverable muon E_rec curve (fold.py) is <~15% across the plotted
# 0.02-2 keV low tail (was ~100% at 4e6 -> visibly jagged). The rare sub-4 keV
# DEPOSITED tail carries only ~1e-4 of the flux, so its per-E_dep-bin error is
# still ~20% even here -- that residual is what the ~8 min 1e9 run buys down
# vs 4e8; the fold aggregates many E_dep bins per E_rec bin so the plotted curve
# is smooth. Runtime ~8 min (batched numpy). Tradeoff logged explicitly.
SEED = 20260720
N = 1_000_000_000


def main() -> None:
    spec = md.run_muon_mc(n_samples=N, seed=SEED)
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    md.write_csv(spec, CSV_PATH)

    total = float((spec.dRdE * np.diff(spec.edges_kev)).sum())
    print(f"integral muon rate   = {spec.rate_hz:.4f} +/- {spec.rate_err_hz:.4f} Hz")
    print(f"vertical-chord MPV   = {spec.vertical_mpv_mev:.4f} MeV "
          f"(mean {spec.vertical_mean_mev:.4f} MeV)")
    print(f"int dR/dE_dep        = {total:.1f} counts/kg/day")
    c, y = spec.centers_kev, spec.dRdE
    print(f"max E_dep with signal= {c[y > 0].max() / 1e3:.1f} MeV")
    print(f"wrote {CSV_PATH}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover - plotting optional
        print(f"[skip figure] matplotlib unavailable: {exc}")
        return

    mask = y > 0
    fig, ax = plt.subplots(figsize=(7.5, 5.0))
    ax.errorbar(c[mask] / 1e3, y[mask], yerr=spec.dRdE_err[mask], fmt="o", ms=2.2,
                lw=0.6, color="#1f5fb4", ecolor="#9bb8e0", label="muon dR/dE_dep (MC)")
    ax.axvline(spec.vertical_mpv_mev, color="#d1495b", ls="--", lw=1.2,
               label=f"vertical MPV {spec.vertical_mpv_mev:.2f} MeV")
    ax.axvline(spec.vertical_mean_mev, color="#2e2e2e", ls=":", lw=1.2,
               label=f"vertical mean {spec.vertical_mean_mev:.2f} MeV (NOT used)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("deposited (phonon) energy  E_dep  [MeV]  -- no quenching")
    ax.set_ylabel(r"dR/dE$_{\rm dep}$  [counts kg$^{-1}$ day$^{-1}$ keV$^{-1}$]")
    ax.set_title(f"Sea-level muon deposited-energy spectrum, 110 g Ge wafer\n"
                 f"integral rate {spec.rate_hz:.2f} Hz (PDG ~1.5-2 Hz), "
                 f"tail to {c[mask].max() / 1e3:.0f} MeV")
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, which="both", alpha=0.25)
    fig.tight_layout()
    os.makedirs(os.path.dirname(FIG_PATH), exist_ok=True)
    fig.savefig(FIG_PATH, dpi=140)
    print(f"wrote {FIG_PATH}")


if __name__ == "__main__":
    main()
