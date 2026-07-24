#!/usr/bin/env python3
# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Combined reconstructed-energy spectrum with the ANALYTIC muon/Compton channels
and the (n,gamma) capture RECOIL spectrum.

This is a SEPARATE producer from ``scripts/make_combined_spectrum.py`` and does not
touch it, the user-owned ``notebooks/paper_calculations.ipynb``, or any frozen
artifact. It reads the frozen CEvNS / neutron / 71Ge deliverables and recomputes
three channels deterministically at run time:

  * muon      -- muon_analytic.run_muon_analytic  (no Monte-Carlo sampling)
  * Compton   -- compton_deposit.run_compton_analytic (closed-form dsigma/dT)
  * capture   -- capture_recoil.recoil_spectrum (nrCascadeSim cascade tables)

It writes only ``figs/analytic_combined_spectrum.png``. Reproducible:
    /opt/anaconda3/bin/python3 scripts/make_analytic_combined_spectrum.py

The per-channel suppression factors match make_combined_spectrum.py (500/100/100),
the ASSUMED NUCLEUS-equivalent scenario; they are NOT earned veto credit. See that
script's header and GPD/HANDOVER.md for the standing caveat.
"""
from __future__ import annotations

import csv
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from qpd_potential import capture_recoil as cr        # noqa: E402
from qpd_potential import compton_deposit as cd       # noqa: E402
from qpd_potential import muon_analytic as ma         # noqa: E402
from qpd_potential import muon_deposit as md          # noqa: E402
from qpd_potential import fold as F                   # noqa: E402
from qpd_potential import trigger as TR               # noqa: E402

ART = os.path.join(ROOT, "artifacts", "v2.0")
FIG = os.path.join(ROOT, "figs", "analytic_combined_spectrum.png")

ROI_LO, ROI_HI = 10.0e-3, 100.0e-3                     # keV
SUPP = {"cevns": 1.0, "muon": 500.0, "compton": 100.0, "neutron": 100.0}
CAPTURE_BOUND = 4399.78                                # Phase-14 in-RoI capture bound
DESIGN = "Ta->Al"


def read(path, ecol, ycol):
    E, y = [], []
    with open(os.path.join(ART, path)) as fh:
        for r in csv.DictReader(x for x in fh if not x.startswith("#")):
            E.append(float(r[ecol])); y.append(float(r[ycol]))
    return np.asarray(E), np.asarray(y)


def fold(dRdE_keV, design=DESIGN):
    d = F.load_design_extended(design)
    N = F.dep_counts_from_dRdEdep(dRdE_keV, d["E_dep_edges_eV"])
    P = np.asarray(TR.P_trig(d["E_dep_centers_eV"]), float)
    dErec = np.diff(d["E_rec_edges_eV"]) / 1e3
    return d["E_rec_centers_eV"], F.fold_counts(N * P, d["R_non_paralyzable"]) / dErec


def integ(E_keV, y, lo, hi):
    lE = np.log(E_keV); ed = np.empty(E_keV.size + 1)
    ed[1:-1] = np.exp(0.5 * (lE[:-1] + lE[1:]))
    ed[0] = E_keV[0] ** 2 / ed[1]; ed[-1] = E_keV[-1] ** 2 / ed[-2]
    w = np.clip(np.minimum(ed[1:], hi) - np.maximum(ed[:-1], lo), 0, None)
    return float((y * w).sum())


def main():
    edges = md.shared_energy_grid("v2.0-ext")
    mu = ma.run_muon_analytic("v2.0-ext")
    co = cd.run_compton_analytic("v2.0-ext")
    cap = {m: cr.recoil_spectrum(edges, mode=m, n_per_cascade=200_000)
           for m in ("slow", "fast")}
    cov = cap["fast"].coverage_fraction
    unresolved = (1.0 - cov) * CAPTURE_BOUND

    Erec, mu_r = fold(mu.dRdE)
    _, co_r = fold(co.dRdE)
    cap_r = {m: fold(cap[m].dRdT)[1] for m in cap}

    lv_dep = 4111.816513779805
    d = F.load_design_extended(DESIGN)
    lv_rec = float(np.interp(lv_dep, d["E_dep_centers_eV"],
                             d["E_rec_median_non_paralyzable_eV"]))

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(15.6, 6.8))

    # ---- left: full budget on E_rec -------------------------------------- #
    sig = bg = 0.0
    for lab, key, c, lw, (E, y) in [
            ("CEvNS signal", "cevns", "#1f77b4", 2.5,
             read(f"cevns_dRdErec_ext_{_d(DESIGN)}.csv", "E_rec_keV",
                  "dRdErec_trigger_weighted")),
            (f"Neutron elastic /{SUPP['neutron']:.0f}", "neutron", "#d62728", 1.9,
             read(f"neutron_dRdErec_ext_{_d(DESIGN)}.csv", "E_rec_keV",
                  "dRdErec_trigger_weighted"))]:
        y = y / SUPP[key]
        v = integ(E, y, ROI_LO, ROI_HI)
        sig, bg = (v, bg) if key == "cevns" else (sig, bg + v)
        m = y > 0
        axL.loglog(E[m] * 1e3, y[m], color=c, lw=lw, label=lab, zorder=6)

    for lab, key, c, yv in ((f"Compton /{SUPP['compton']:.0f} (analytic)", "compton",
                             "#2ca02c", co_r),
                            (f"Cosmic muons /{SUPP['muon']:.0f} (analytic)", "muon",
                             "#9467bd", mu_r)):
        y = yv / SUPP[key]
        bg += integ(Erec / 1e3, y, ROI_LO, ROI_HI)
        m = y > 0
        axL.loglog(Erec[m], y[m], color=c, lw=1.8, label=lab, zorder=5)

    y_f = cap_r["fast"] / SUPP["neutron"]
    y_s = cap_r["slow"] / SUPP["neutron"]
    k = (y_f > 0) | (y_s > 0)
    axL.fill_between(Erec[k], np.minimum(y_f, y_s)[k] + 1e-30, np.maximum(y_f, y_s)[k],
                     color="#ff7f0e", alpha=0.35, zorder=3,
                     label="Prompt (n,$\\gamma$) capture /100 — RESOLVED\n"
                           "cascades, slow–fast bracket")
    axL.loglog(Erec[y_f > 0], y_f[y_f > 0], color="#ff7f0e", lw=1.9, zorder=4)
    bg += integ(Erec / 1e3, y_f, ROI_LO, ROI_HI)

    E71, y71 = read(f"ge71_ec_dRdErec_{_d(DESIGN)}.csv", "E_rec_keV", "dRdErec_bound")
    m = y71 > 0
    axL.vlines(E71[m] * 1e3, 1e-2, y71[m] / SUPP["neutron"], color="#8c564b", lw=2.4,
               zorder=7, label="$^{71}$Ge EC M line /100 [BOUND]")
    bg_b = integ(E71, y71 / SUPP["neutron"], ROI_LO, ROI_HI)

    lvl = unresolved / SUPP["neutron"] / (ROI_HI - ROI_LO)
    axL.fill_between([ROI_LO * 1e3, ROI_HI * 1e3], lvl * 0.86, lvl * 1.16,
                     color="#7f7f7f", alpha=0.45, hatch="///", edgecolor="#7f7f7f",
                     zorder=2, label=f"UNRESOLVED capture ({1-cov:.0%}) /100\n"
                                     "[BOUND, no shape]")
    bg_b += unresolved / SUPP["neutron"]

    axL.axvline(lv_rec, color="0.4", ls="--", lw=1.0, zorder=1)
    axL.set_xlabel("Reconstructed energy  $E_{\\rm rec}$   [eV]")
    axL.set_ylabel(r"$dR/dE_{\rm rec}$   [counts kg$^{-1}$ day$^{-1}$ keV$^{-1}$]")
    axL.set_title(f"Full budget, Ta$\\rightarrow$Al   $S/B$ = {sig/bg:.3f} (est.) / "
                  f"{sig/(bg+bg_b):.3f} (incl. bounds)", fontsize=11)
    axL.set_xlim(0.09, 1.2e5); axL.set_ylim(1e-2, 3e6)
    axL.grid(True, which="major", alpha=0.28); axL.grid(True, which="minor", alpha=0.08)
    axL.legend(fontsize=7.2, loc="lower left", framealpha=0.94)

    # ---- right: the capture recoil spectrum on the recoil axis ------------ #
    cols = {"slow": "#8c564b", "fast": "#ff7f0e"}
    lbl = {"slow": "SLOW limit (ion stops): $T=\\sum E_i^2/2Mc^2$",
           "fast": "FAST limit (no slowing): $T=|\\sum\\vec p_i|^2/2Mc^2$"}
    for m in ("fast", "slow"):
        y = cap[m].dRdT; kk = y > 0
        axR.loglog(cap[m].centers_keV[kk] * 1e3, y[kk], color=cols[m], lw=1.9,
                   label=lbl[m], ds="steps-mid" if m == "slow" else "default")
    axR.axvspan(10, 100, color="#1f77b4", alpha=0.13, zorder=0)
    axR.annotate("10–100 eV RoI", xy=(31, 3e4), fontsize=8.5, color="#1f77b4",
                 ha="center")
    axR.set_xlabel("Nuclear recoil energy  $T$   [eV$_{\\rm nr}$]")
    axR.set_ylabel(r"$dR/dT$   [counts kg$^{-1}$ day$^{-1}$ keV$^{-1}$]")
    axR.set_title(f"(n,$\\gamma$) capture recoil, resolved cascades ({cov:.1%} of "
                  "captures)\ncascade tables: nrCascadeSim (Villano+ 2022), "
                  "$S_n$ from ENDF", fontsize=10.5)
    axR.set_xlim(5, 2e3); axR.set_ylim(1e-1, 1e5)
    axR.grid(True, which="major", alpha=0.28); axR.grid(True, which="minor", alpha=0.08)
    axR.legend(fontsize=8.0, loc="upper left", framealpha=0.95)
    axR.text(0.98, 0.02,
             f"mean $T$ = {cap['fast'].mean_recoil_keV*1e3:.0f} eV (mode-independent)\n"
             "slow limit: discrete lines 182–671 eV, none below 100 eV",
             transform=axR.transAxes, ha="right", va="bottom", fontsize=7.6,
             bbox=dict(fc="white", ec="0.7", alpha=0.93))

    fig.suptitle("QPD Ge wafer, 3 GW$_{\\rm th}$ at 25 m — analytic muon/Compton + "
                 "(n,$\\gamma$) capture recoil spectrum", fontsize=12, y=0.985)
    fig.tight_layout(rect=[0, 0.02, 1, 0.94])
    os.makedirs(os.path.dirname(FIG), exist_ok=True)
    fig.savefig(FIG, dpi=150)
    print(f"wrote {FIG}")
    print(f"S/B = {sig/bg:.4f} (est.) / {sig/(bg+bg_b):.4f} (incl. bounds)")


def _d(design):
    return {"Ta->Al": "TaAl", "Al->Hf": "AlHf"}[design]


if __name__ == "__main__":
    main()
