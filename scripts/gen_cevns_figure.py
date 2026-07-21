#!/usr/bin/env python
# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Generate artifacts/stage1/cevns_dRdT_deposited.pdf (Phase 3, Plan 03-02).

Flagship (3 GW_th / 25 m) CEvNS differential rate dR/dT versus DEPOSITED
nuclear-recoil energy T_nr, with:
  * the propagated flux 1-sigma uncertainty band shaded (from the 03-01 CSV
    dRdT_band_1sigma column),
  * the sub-1.8-MeV-zeroed curve (toggle) overlaid to show the placeholder's
    influence is confined below ~95 eV_nr,
  * the T approx 95 eV_nr band-widening boundary (E_min(95 eV) approx 1.78 MeV)
    marked,
  * a lower panel with the fractional band and the sub-1.8-MeV sensitivity
    fraction, making the honest low-recoil systematic explicit.

Deposited energy only -- NO quenching, NO detector response (Phase 5).
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from qpd_potential import cevns  # noqa: E402

CSV = os.path.join(
    os.path.dirname(__file__), "..", "artifacts", "stage1", "cevns_dRdT.csv"
)
OUT = os.path.join(
    os.path.dirname(__file__), "..", "artifacts", "stage1", "cevns_dRdT_deposited.pdf"
)

T_BOUNDARY_EV = 95.0  # E_min(95 eV) approx 1.78 MeV band-widening boundary


def load_csv():
    rows = []
    with open(CSV) as fh:
        for line in fh:
            if line.startswith("#") or line.startswith("T_eV"):
                continue
            rows.append([float(x) for x in line.split(",")])
    arr = np.array(rows)
    return arr[:, 0], arr[:, 6], arr[:, 7]  # T_eV, dRdT_total, dRdT_band_1sigma


def main() -> None:
    T_eV, total, band = load_csv()

    # Toggle + fractional curves on a coarser grid (the fold is the expensive step).
    f = cevns.ReactorFlux()
    f_cut = cevns.ReactorFlux(f.csv_path, e_min_cut_MeV=1.8)
    Tg = np.logspace(np.log10(T_eV[0]), np.log10(T_eV[-1]), 90)
    dr_full = np.array([cevns.differential_rate(t * 1e-3, f) for t in Tg])
    dr_cut = np.array([cevns.differential_rate(t * 1e-3, f_cut) for t in Tg])
    frac_band = np.array([cevns.fractional_band(t * 1e-3, f) for t in Tg])
    sub18 = np.array([cevns.sub18_sensitivity_fraction(t * 1e-3, f) for t in Tg])

    fig, (ax, ax2) = plt.subplots(
        2, 1, figsize=(7.2, 7.6), sharex=True,
        gridspec_kw={"height_ratios": [2.4, 1.0], "hspace": 0.08},
    )

    # ---- top panel: dR/dT with band + toggle ----
    ax.fill_between(
        T_eV, total - band, total + band, color="C0", alpha=0.28,
        label=r"$\pm1\sigma$ flux band (propagated)",
    )
    ax.plot(T_eV, total, color="C0", lw=2.0, label="total dR/dT (flagship, 3 GW$_{th}$/25 m)")
    ax.plot(
        Tg, dr_cut, color="C3", lw=1.6, ls="--",
        label=r"flux zeroed below 1.8 MeV (sub-1.8 toggle)",
    )
    ax.axvline(T_BOUNDARY_EV, color="0.4", lw=1.2, ls=":")
    ax.text(
        T_BOUNDARY_EV * 1.05, total.max() * 0.30,
        r"$T\!\approx\!95$ eV$_{nr}$" "\n" r"($E_{min}\!\approx\!1.78$ MeV)",
        fontsize=8.5, color="0.3", va="center",
    )
    ax.axvspan(T_eV[0], T_BOUNDARY_EV, color="0.85", alpha=0.35, zorder=0)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylabel(r"$dR/dT$  [counts kg$^{-1}$ day$^{-1}$ keV$^{-1}$]")
    ax.set_ylim(total[total > 0].min() * 0.5, total.max() * 2.0)
    ax.set_title(
        "Reactor CEvNS on natural Ge — deposited nuclear-recoil spectrum\n"
        "(no quenching, no detector response; Phase 5)", fontsize=10.5,
    )
    ax.legend(fontsize=8.5, loc="upper right", framealpha=0.95)
    ax.grid(True, which="both", alpha=0.2)

    # ---- bottom panel: fractional band + sub-1.8 sensitivity ----
    ax2.plot(Tg, 100 * frac_band, color="C0", lw=1.8,
             label=r"fractional $1\sigma$ band")
    ax2.plot(Tg, 100 * sub18, color="C3", lw=1.6, ls="--",
             label="sub-1.8-MeV rate fraction")
    ax2.axvline(T_BOUNDARY_EV, color="0.4", lw=1.2, ls=":")
    ax2.axvspan(T_eV[0], T_BOUNDARY_EV, color="0.85", alpha=0.35, zorder=0)
    ax2.axhspan(2.0, 5.0, color="C2", alpha=0.12)
    ax2.set_xlabel(r"deposited nuclear-recoil energy  $T_{nr}$  [eV$_{nr}$]")
    ax2.set_ylabel("percent [%]")
    ax2.set_ylim(0, 40)
    ax2.legend(fontsize=8.5, loc="upper right", framealpha=0.95)
    ax2.grid(True, which="both", alpha=0.2)
    ax2.annotate(
        "band widens below ~95 eV; well-anchored 2-5% above ~200 eV",
        xy=(0.02, 0.90), xycoords="axes fraction", fontsize=8, color="0.3",
    )

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")
    print(f"wrote {OUT}")
    print(f"  band(50eV)={cevns.fractional_band(0.05,f):.3f}  "
          f"band(200eV)={cevns.fractional_band(0.2,f):.3f}  "
          f"sub18(50eV)={cevns.sub18_sensitivity_fraction(0.05,f):.3f}")


if __name__ == "__main__":
    main()
