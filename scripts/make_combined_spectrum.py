#!/usr/bin/env python3
"""Combined reconstructed-energy spectrum: CEvNS signal against every modelled background.

Milestone v2.0 produced a per-channel figure in each phase but never one showing the
signal and the full background budget on a single axis. This assembles them from the
committed per-channel CSVs; it re-reads frozen artifacts and does no physics of its own.

THREE THINGS THIS FIGURE IS CAREFUL ABOUT, because getting them wrong would misrepresent
the background budget:

  1. Prompt (n,gamma) capture is 44% of the RoI denominator but has NO dR/dE_rec artifact
     anywhere in the repository -- Phase 14 delivered it as an INTEGRATED BOUND only
     (<= 4399.78 counts/kg/day in-RoI, rigorous and cascade-free). It cannot be drawn as a
     curve without inventing a spectral shape. It is shown as a hatched band at
     bound / Delta_E_RoI, explicitly labelled as having no derived shape.
  2. The 71Ge EC M line is a DISCRETE line occupying 1-2 bins, not a continuum. Drawn as a
     stem. It is a BOUND at the saturation scenario; at t = 1 d it is 5.88% of this.
  3. Ge inelastic (<= 2666.83) is excluded, as in the Phase-16 assembly: its bound is loose
     by ~3 decades in the RoI, so summing it in would not be a rate estimate.

Curves are the CENTRAL (untriggered) dR/dE_rec on the shared 161-bin reconstructed axis.
"""
import csv
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, "artifacts", "v2.0")

ROI_LO, ROI_HI = 10.0e-3, 100.0e-3   # keV; the 10-100 eV reconstructed RoI
FLOOR = 0.0999350e-3                 # Phase-10 grid floor, 99.935 meV
SUBEV = 1.0e-3                       # below 1 eV, P_trig is the reported observable
CAPTURE_BOUND = 4399.78              # counts/kg/day, Phase 14, in-RoI, rigorous


def read(path, ecol, ycol):
    E, y = [], []
    with open(os.path.join(ART, path)) as fh:
        for r in csv.DictReader(x for x in fh if not x.startswith("#")):
            E.append(float(r[ecol]))
            y.append(float(r[ycol]))
    return np.asarray(E), np.asarray(y)


def continua(design):
    return [
        dict(label="CEvNS signal", c="#1f77b4", lw=2.5, z=6,
             d=read(f"cevns_dRdErec_ext_{design}.csv", "E_rec_keV", "dRdErec_central")),
        dict(label="Neutron elastic  (order-of-mag.)", c="#d62728", lw=1.9, z=5,
             d=read(f"neutron_dRdErec_ext_{design}.csv", "E_rec_keV", "dRdErec_central")),
        dict(label="Compton ($\\gamma$ ambient)", c="#2ca02c", lw=1.7, z=4,
             d=read(f"em_dRdErec_ext_{design}.csv", "E_rec_keV[keV]",
                    "compton_dRdErec_untriggered[counts/kg/day/keV]")),
        dict(label="Cosmic muons", c="#9467bd", lw=1.7, z=4,
             d=read(f"em_dRdErec_ext_{design}.csv", "E_rec_keV[keV]",
                    "muon_dRdErec_untriggered[counts/kg/day/keV]")),
    ]


def bin_integrate(E, y, lo, hi):
    """Sum y*dE over [lo, hi]. Uses bin widths, so a 1-bin spike is not lost
    the way a trapezoid rule over a single sample would lose it."""
    if E.size < 2:
        return 0.0
    logE = np.log(E)
    edges = np.empty(E.size + 1)
    edges[1:-1] = np.exp(0.5 * (logE[:-1] + logE[1:]))
    edges[0] = E[0] ** 2 / edges[1]
    edges[-1] = E[-1] ** 2 / edges[-2]
    w = np.clip(np.minimum(edges[1:], hi) - np.maximum(edges[:-1], lo), 0, None)
    return float(np.sum(y * w))


def panel(ax, design, title):
    for ch in continua(design):
        E, y = ch["d"]
        m = y > 0
        if m.any():
            ax.loglog(E[m] * 1e3, y[m], color=ch["c"], lw=ch["lw"], label=ch["label"], zorder=ch["z"])

    # 71Ge EC M line -- discrete, 1-2 bins, a BOUND at saturation
    E, y = read(f"ge71_ec_dRdErec_{design}.csv", "E_rec_keV", "dRdErec_bound")
    m = y > 0
    if m.any():
        ax.vlines(E[m] * 1e3, 1e-6, y[m], color="#8c564b", lw=2.6, zorder=7,
                  label="$^{71}$Ge EC M line  [BOUND, saturation]")

    # prompt (n,gamma) capture -- integrated bound only, NO spectral shape exists
    lvl = CAPTURE_BOUND / (ROI_HI - ROI_LO)
    ax.fill_between([ROI_LO * 1e3, ROI_HI * 1e3], lvl * 0.86, lvl * 1.16,
                    color="#ff7f0e", alpha=0.55, hatch="///", edgecolor="#ff7f0e",
                    zorder=2, label="Prompt (n,$\\gamma$) capture  [BOUND,\nno spectral shape derived]")

    ax.axvspan(ROI_LO * 1e3, ROI_HI * 1e3, color="0.85", alpha=0.4, zorder=0)
    ax.axvline(FLOOR * 1e3, color="0.35", ls=":", lw=1.1, zorder=1)
    ax.axvline(SUBEV * 1e3, color="0.55", ls="-.", lw=1.0, zorder=1)
    ax.set_xlabel("Reconstructed energy  $E_{\\rm rec}$   [eV]")
    ax.set_title(title, fontsize=11.5)
    ax.grid(True, which="major", alpha=0.28)
    ax.grid(True, which="minor", alpha=0.09)
    ax.set_xlim(0.09, 3.0e3)
    ax.set_ylim(1e-3, 3e6)


fig, axes = plt.subplots(1, 2, figsize=(14.2, 6.4), sharey=True)
panel(axes[0], "TaAl", r"Ta$\rightarrow$Al     $S/B_{\rm particle} = 1.33\times10^{-2}$")
panel(axes[1], "AlHf", r"Al$\rightarrow$Hf     $S/B_{\rm particle} = 1.32\times10^{-2}$")
axes[0].set_ylabel(r"$dR/dE_{\rm rec}$   [counts kg$^{-1}$ day$^{-1}$ keV$^{-1}$]")
axes[0].legend(loc="lower left", fontsize=8.2, framealpha=0.94)

axes[1].text(0.985, 0.02,
             "shaded band: 10–100 eV RoI\n"
             "dotted: grid floor 99.9 meV\n"
             "dash-dot: below 1 eV the reported\n"
             "observable is $P_{\\rm trig}$, not $dR/dE$",
             transform=axes[1].transAxes, ha="right", va="bottom", fontsize=8,
             bbox=dict(fc="white", ec="0.7", alpha=0.92))

fig.suptitle("QPD Ge wafer — unshielded surface, 3 GW$_{\\rm th}$ at 25 m — reconstructed-energy spectra, "
             "veto credit 1.0 by construction", fontsize=12.5, y=0.986)
fig.text(0.5, 0.007,
         "Bounds are not estimates: summing them makes $S/B_{\\rm particle}$ a LOWER bound (7.3×10$^{-3}$). "
         "Ge inelastic (≤ 2666.83) excluded — loose by ~3 decades in the RoI. LEE carried as a band, never summed in.",
         ha="center", fontsize=8.3, style="italic")

fig.tight_layout(rect=[0, 0.027, 1, 0.955])
fig.savefig(os.path.join(ART, "combined_spectrum_v2.0.png"), dpi=155)
fig.savefig(os.path.join(ART, "combined_spectrum_v2.0.pdf"))
print("wrote combined_spectrum_v2.0.png\n")

for design in ("TaAl", "AlHf"):
    print(f"{design}  integrated over the 10-100 eV RoI  [counts/kg/day]")
    tot = 0.0
    for ch in continua(design):
        E, y = ch["d"]
        v = bin_integrate(E, y, ROI_LO, ROI_HI)
        if ch["label"].startswith("CEvNS"):
            sig = v
        else:
            tot += v
        print(f"   {ch['label']:<40s} {v:11.4f}")
    E, y = read(f"ge71_ec_dRdErec_{design}.csv", "E_rec_keV", "dRdErec_bound")
    m71 = bin_integrate(E, y, ROI_LO, ROI_HI)
    print(f"   {'71Ge EC M line [BOUND]':<40s} {m71:11.4f}")
    print(f"   {'prompt (n,gamma) capture [BOUND]':<40s} {CAPTURE_BOUND:11.4f}")
    print(f"   -> S/B estimates only          {sig / tot:.4e}")
    print(f"   -> S/B incl. bounds (LOWER bd) {sig / (tot + m71 + CAPTURE_BOUND):.4e}\n")
