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

Solid curves are the TRIGGER-WEIGHTED dR/dE_rec -- the actual observable. The faint dotted
ghost behind each is the untriggered spectrum, so the sub-eV trigger-efficiency rolloff is
visible as the gap between them (P_trig = 0.092 at 0.12 eV, 0.36 at 0.21 eV, ~1 above 2 eV).
The 50%% point sits near 0.25 eV RECONSTRUCTED because E50 = 0.5 eV is defined on the DEPOSIT
axis and the deposit->reconstructed slope is ~0.5.
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
# Bandwidth saturation is NOT added by this script: it is already inside the response
# matrices as R_non_paralyzable (25 kHz non-paralyzable censoring, CONVENTIONS Sect. F).
# These are the per-design onsets carried in the npz, drawn so the effect is visible.
SAT_ONSET_EDEP_eV = {"TaAl": 52.90739510057845, "AlHf": 32.12999702464278}


def sat_marks(design):
    """Saturation onset and whole-array plateau, mapped deposit -> RECONSTRUCTED
    through the response matrix's OWN measured median, not an assumed slope.

    An earlier version of this figure multiplied the deposit-axis onset by a
    hand-picked 0.5. That is the cross-axis error this project has hit twice
    (Phase 13 caught itself; Phase 14 wrote a forbidden proxy for it). The
    measured mapping gives 23.4 eV rec for Ta->Al, not the 26.5 the 0.5 slope
    produced.
    """
    z = np.load(os.path.join(ART, f"response_matrix_{design}_ext.npz"), allow_pickle=True)
    Ed, med = z["E_dep_centers_eV"], z["E_rec_median_non_paralyzable_eV"]
    to_rec = lambda e: float(np.interp(e, Ed, med))
    return (float(z["saturation_onset_Edep_eV"]), to_rec(float(z["saturation_onset_Edep_eV"])),
            float(z["whole_array_plateau_Edep_eV"]), to_rec(float(z["whole_array_plateau_Edep_eV"])))
FLOOR = 0.0999350e-3                 # Phase-10 grid floor, 99.935 meV
SUBEV = 1.0e-3                       # below 1 eV, P_trig is the reported observable
CAPTURE_BOUND = 4399.78              # counts/kg/day, Phase 14, in-RoI, rigorous

# ---------------------------------------------------------------------------
# ASSUMED neutron suppression. NOT derived, NOT transferred from NUCLEUS.
# A declared stage-one placeholder, user-set 2026-07-23. It is applied to ALL
# THREE neutron-driven channels -- elastic, prompt (n,gamma) capture, and the
# 71Ge EC line -- because all three scale with the same INCIDENT neutron
# fluence: 71Ge is produced by 70Ge(n,gamma) from that same field.
# NUCLEUS's published ~5 and ~50 are event-rate reductions IN CaWO4 and are
# deliberately NOT used: they embed a target response that is not germanium's.
N_SUPPRESSION = 100.0
# ---------------------------------------------------------------------------


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
             d=read(f"cevns_dRdErec_ext_{design}.csv", "E_rec_keV", "dRdErec_trigger_weighted"),
             raw=read(f"cevns_dRdErec_ext_{design}.csv", "E_rec_keV", "dRdErec_central")),
        dict(label=f"Neutron elastic  /{N_SUPPRESSION:.0f} (ASSUMED)", c="#d62728", lw=1.9, z=5, sup=True,
             d=read(f"neutron_dRdErec_ext_{design}.csv", "E_rec_keV", "dRdErec_trigger_weighted"),
             raw=read(f"neutron_dRdErec_ext_{design}.csv", "E_rec_keV", "dRdErec_central")),
        dict(label="Compton ($\\gamma$ ambient)", c="#2ca02c", lw=1.7, z=4,
             d=read(f"em_dRdErec_ext_{design}.csv", "E_rec_keV[keV]",
                    "compton_dRdErec_triggered[counts/kg/day/keV]"),
             raw=read(f"em_dRdErec_ext_{design}.csv", "E_rec_keV[keV]",
                      "compton_dRdErec_untriggered[counts/kg/day/keV]")),
        dict(label="Cosmic muons", c="#9467bd", lw=1.7, z=4,
             d=read(f"em_dRdErec_ext_{design}.csv", "E_rec_keV[keV]",
                    "muon_dRdErec_triggered[counts/kg/day/keV]"),
             raw=read(f"em_dRdErec_ext_{design}.csv", "E_rec_keV[keV]",
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
        f = N_SUPPRESSION if ch.get("sup") else 1.0
        E, y = ch["d"]; y = y / f
        Er, yr = ch["raw"]; yr = yr / f
        mr = yr > 0
        if mr.any():   # untriggered ghost -- the gap to the solid curve IS the trigger rolloff
            ax.loglog(Er[mr] * 1e3, yr[mr], color=ch["c"], lw=1.0, ls=":", alpha=0.5, zorder=ch["z"] - 1)
        m = y > 0
        if m.any():
            ax.loglog(E[m] * 1e3, y[m], color=ch["c"], lw=ch["lw"], label=ch["label"], zorder=ch["z"])

    # 71Ge EC M line -- discrete, 1-2 bins, a BOUND at saturation
    E, y = read(f"ge71_ec_dRdErec_{design}.csv", "E_rec_keV", "dRdErec_bound")
    m = y > 0
    if m.any():
        ax.vlines(E[m] * 1e3, 1e-6, y[m] / N_SUPPRESSION, color="#8c564b", lw=2.6, zorder=7,
                  label=f"$^{{71}}$Ge EC M line /{N_SUPPRESSION:.0f}  [BOUND, sat.]")

    # prompt (n,gamma) capture -- integrated bound only, NO spectral shape exists
    lvl = CAPTURE_BOUND / N_SUPPRESSION / (ROI_HI - ROI_LO)
    ax.fill_between([ROI_LO * 1e3, ROI_HI * 1e3], lvl * 0.86, lvl * 1.16,
                    color="#ff7f0e", alpha=0.55, hatch="///", edgecolor="#ff7f0e",
                    zorder=2, label=f"Prompt (n,$\\gamma$) capture /{N_SUPPRESSION:.0f}  [BOUND,\nno spectral shape derived]")

    ax.axvspan(ROI_LO * 1e3, ROI_HI * 1e3, color="0.85", alpha=0.4, zorder=0)
    ax.axvline(FLOOR * 1e3, color="0.35", ls=":", lw=1.1, zorder=1)
    ax.axvline(SUBEV * 1e3, color="0.55", ls="-.", lw=1.0, zorder=1)
    on_dep, on_rec, pl_dep, pl_rec = sat_marks(design)
    ax.axvline(on_rec, color="#e377c2", ls="--", lw=1.6, zorder=2)
    ax.annotate(f"saturation onset  {on_dep:.0f} eV dep = {on_rec:.0f} eV rec",
                xy=(on_rec, 2e6), fontsize=7.2, color="#e377c2",
                ha="right", rotation=90, va="top")
    # the saturated band: above the whole-array plateau the readout is bandwidth-limited
    ax.axvspan(pl_rec, 1.2e5, color="#e377c2", alpha=0.13, zorder=0)
    ax.annotate(f"bandwidth-saturated\n(plateau {pl_dep/1e3:.1f} keV dep = {pl_rec/1e3:.1f} keV rec)",
                xy=(pl_rec * 1.35, 2e6), fontsize=7.2, color="#c2559b",
                ha="left", rotation=90, va="top")
    ax.set_xlabel("Reconstructed energy  $E_{\\rm rec}$   [eV]")
    ax.set_title(title, fontsize=11.5)
    ax.grid(True, which="major", alpha=0.28)
    ax.grid(True, which="minor", alpha=0.09)
    # Full data range. The previous 3 keV limit cut off 100% of the muon channel's
    # counts and hid its pile-up peak at ~18.8 keV -- which IS the saturation
    # signature, i.e. the figure omitted exactly the effect it claimed to mark.
    ax.set_xlim(0.09, 1.2e5)
    ax.set_ylim(1e-2, 3e6)


def sb(design):
    """S/B on the TRIGGER-WEIGHTED observable, with the assumed suppression applied."""
    sig = bg = 0.0
    for ch in continua(design):
        f = N_SUPPRESSION if ch.get("sup") else 1.0
        E, y = ch["d"]
        v = bin_integrate(E, y / f, ROI_LO, ROI_HI)
        if ch["label"].startswith("CEvNS"):
            sig = v
        else:
            bg += v
    E, y = read(f"ge71_ec_dRdErec_{design}.csv", "E_rec_keV", "dRdErec_trigger_weighted")
    bg_b = bin_integrate(E, y / N_SUPPRESSION, ROI_LO, ROI_HI) + CAPTURE_BOUND / N_SUPPRESSION
    return sig, bg, bg_b

fig, axes = plt.subplots(1, 2, figsize=(14.2, 6.4), sharey=True)
SB = {}
for d in ("TaAl", "AlHf"):
    sg, bg, bgb = sb(d)
    SB[d] = (sg / bg, sg / (bg + bgb))
panel(axes[0], "TaAl", "Ta$\\rightarrow$Al     $S/B_{\\rm particle}$ = "
      f"{SB['TaAl'][0]:.3f}  (est.)   /   {SB['TaAl'][1]:.3f}  (incl. bounds)")
panel(axes[1], "AlHf", "Al$\\rightarrow$Hf     $S/B_{\\rm particle}$ = "
      f"{SB['AlHf'][0]:.3f}  (est.)   /   {SB['AlHf'][1]:.3f}  (incl. bounds)")
axes[0].set_ylabel(r"$dR/dE_{\rm rec}$   [counts kg$^{-1}$ day$^{-1}$ keV$^{-1}$]")
axes[0].legend(loc="lower left", fontsize=8.2, framealpha=0.94)

axes[1].text(0.985, 0.02,
             "shaded band: 10–100 eV RoI\n"
             "dotted: grid floor 99.9 meV\n"
             "dash-dot: below 1 eV the reported\n"
             "observable is $P_{\\rm trig}$, not $dR/dE$",
             transform=axes[1].transAxes, ha="right", va="bottom", fontsize=8,
             bbox=dict(fc="white", ec="0.7", alpha=0.92))

fig.suptitle(f"QPD Ge wafer — 3 GW$_{{\\rm th}}$ at 25 m — trigger-weighted spectra with an ASSUMED "
             f"{N_SUPPRESSION:.0f}× neutron suppression   (veto credit still 1.0)", fontsize=12.5, y=0.986)
fig.text(0.5, 0.050,
         f"The {N_SUPPRESSION:.0f}\u00d7 suppression is an ASSUMED placeholder \u2014 not derived, and deliberately NOT "
         "transferred from NUCLEUS,",
         ha="center", fontsize=8.4, style="italic")
fig.text(0.5, 0.032,
         "whose ~5 and ~50 are event-rate reductions in CaWO$_4$ that embed a target response which is not Ge's.",
         ha="center", fontsize=8.4, style="italic")
fig.text(0.5, 0.014,
         "Faint dotted = untriggered; the gap is the trigger-efficiency rolloff at the NEW $E_{50}$ = 1.0 eV (deposit). "
         "Saturation was always in $R$, not added here.",
         ha="center", fontsize=8.4, style="italic")

fig.tight_layout(rect=[0, 0.075, 1, 0.955])
fig.savefig(os.path.join(ART, "combined_spectrum_v2.0.png"), dpi=155)
# CreationDate=None makes the PDF byte-stable across runs. Without it matplotlib
# stamps the current time, so every regeneration dirtied a tracked artifact and
# tripped the Phase-10 frozen-artifact guard -- noise that would train a reader to
# ignore that guard.
fig.savefig(os.path.join(ART, "combined_spectrum_v2.0.pdf"),
            metadata={"CreationDate": None})
print("wrote combined_spectrum_v2.0.png\n")

for design in ("TaAl", "AlHf"):
    print(f"{design}   10-100 eV RoI, TRIGGER-WEIGHTED, {N_SUPPRESSION:.0f}x neutron suppression applied")
    est = 0.0
    for ch in continua(design):
        f = N_SUPPRESSION if ch.get("sup") else 1.0
        E, y = ch["d"]
        v = bin_integrate(E, y / f, ROI_LO, ROI_HI)
        raw = bin_integrate(*ch["raw"], ROI_LO, ROI_HI)
        if ch["label"].startswith("CEvNS"):
            sig = v
        else:
            est += v
        print(f"   {ch['label']:<34s} {v:10.3f}   (untrig., unsupp. {raw:10.3f})")
    E, y = read(f"ge71_ec_dRdErec_{design}.csv", "E_rec_keV", "dRdErec_trigger_weighted")
    m71 = bin_integrate(E, y / N_SUPPRESSION, ROI_LO, ROI_HI)
    capt = CAPTURE_BOUND / N_SUPPRESSION
    print(f"   {'71Ge EC M line [BOUND] /100':<34s} {m71:10.3f}")
    print(f"   {'prompt (n,g) capture [BOUND] /100':<34s} {capt:10.3f}")
    print(f"   -> S/B estimates only          {sig/est:.4f}")
    print(f"   -> S/B incl. bounds (LOWER bd) {sig/(est+m71+capt):.4f}\n")
