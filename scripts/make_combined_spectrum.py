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
visible as the gap between them. The dotted is the intrinsic spectrum (linear response,
no saturation, no trigger); the solid has both applied.
The 50%% point sits near 0.25 eV RECONSTRUCTED because E50 = 0.5 eV is defined on the DEPOSIT
axis and the deposit->reconstructed slope is ~0.5.
"""
import csv
import os

import matplotlib
import numpy as np
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
from qpd_potential import trigger  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, "artifacts", "v2.0")

ROI_LO, ROI_HI = 10.0e-3, 100.0e-3   # keV; the 10-100 eV reconstructed RoI
# Bandwidth saturation is NOT added by this script: it is already inside the response
# matrices as R_non_paralyzable (25 kHz non-paralyzable censoring, CONVENTIONS Sect. F).
# These are the per-design onsets carried in the npz, drawn so the effect is visible.
SAT_ONSET_EDEP_eV = {"TaAl": 52.90739510057845, "AlHf": 32.12999702464278}


def _deposit(channel):
    """(E_dep [eV], dR/dE_dep [counts/kg/day/keV]) for one channel, on the extended grid."""
    if channel == "cevns":
        r = _rows_dep("cevns_dRdT_ext.csv"); return _c(r, "T_eV_nr"), _c(r, "dRdT_total")
    if channel == "neutron":
        r = _rows_dep("neutron_dRdT_ge_ext.csv"); return _c(r, "T_eV_nr"), _c(r, "dRdT")
    r = _rows_dep(f"{channel}_dRdEdep_ext.csv")
    return _c(r, "E_dep_keV[keV]") * 1e3, _c(r, "dRdEdep[counts/kg/day/keV]")


def _rows_dep(path):
    with open(os.path.join(ART, path)) as fh:
        return list(csv.DictReader(x for x in fh if not x.startswith("#")))


def _c(rows, name):
    return np.array([float(r[name]) for r in rows])


def unsaturated(channel, design):
    """The INTRINSIC spectrum: linear response, no saturation, no analysis efficiency.

    The linear-response limit is E_rec = C * E_dep, with C read from the response
    matrix's own low-energy behaviour (0.4972 Ta->Al) rather than assumed.
    dR/dE_rec = (dR/dE_dep)/C, both already per keV.

    The trigger (analysis-efficiency) weighting is DELIBERATELY NOT applied here
    (user request 2026-07-23). So the dotted curve is the underlying physical
    spectrum, and the gap to the solid shows BOTH instrumental effects: the
    trigger rolloff below ~1 eV and bandwidth saturation above the onset.
    """
    z = np.load(os.path.join(ART, f"response_matrix_{design}_ext.npz"), allow_pickle=True)
    Ed_m, med = z["E_dep_centers_eV"], z["E_rec_median_non_paralyzable_eV"]
    C = float(np.interp(1.0, Ed_m, med)) / 1.0
    E, dRdE = _deposit(channel)
    return E * C, dRdE / C


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
# ASSUMED per-channel suppression, set to NUCLEUS's published factors
# (user decision 2026-07-23). This deliberately OVERRIDES the locked Phase-8
# decision: NUCLEUS's ~5/~50/>99.8% are event-rate reductions IN CaWO4 (they
# embed a target response that is not germanium's) and most come from the COV/MV
# active veto the wafer does NOT geometrically fit. The user accepts both: the
# premise is "a real experiment will build shielding of similar performance".
#   muon    /500  = MV+COV reject >99.8% of muon-induced backgrounds (EPJC 86,29 sec.5.2.1)
#   compton /50   = 5 cm Pb, factor ~50 reduction (sec.5.2.1)
#   neutron /25   = 4 cm B4C (~5) x COV anti-coincidence (~5) (sec.5.2.1)
# The neutron factor is applied to all THREE neutron-driven channels (elastic,
# prompt (n,gamma) capture, 71Ge EC) since they share the incident fluence.
SUPP = {"cevns": 1.0, "muon": 500.0, "compton": 50.0, "neutron": 25.0}
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
        dict(label="CEvNS signal", key="cevns", c="#1f77b4", lw=2.5, z=6,
             d=read(f"cevns_dRdErec_ext_{design}.csv", "E_rec_keV", "dRdErec_trigger_weighted"),
             raw=read(f"cevns_dRdErec_ext_{design}.csv", "E_rec_keV", "dRdErec_central")),
        dict(label=f"Neutron elastic  /{SUPP['neutron']:.0f}", key="neutron", c="#d62728", lw=1.9, z=5,
             d=read(f"neutron_dRdErec_ext_{design}.csv", "E_rec_keV", "dRdErec_trigger_weighted"),
             raw=read(f"neutron_dRdErec_ext_{design}.csv", "E_rec_keV", "dRdErec_central")),
        dict(label=f"Compton ($\\gamma$ ambient)  /{SUPP['compton']:.0f}", key="compton", c="#2ca02c", lw=1.7, z=4,
             d=read(f"em_dRdErec_ext_{design}.csv", "E_rec_keV[keV]",
                    "compton_dRdErec_triggered[counts/kg/day/keV]"),
             raw=read(f"em_dRdErec_ext_{design}.csv", "E_rec_keV[keV]",
                      "compton_dRdErec_untriggered[counts/kg/day/keV]")),
        dict(label=f"Cosmic muons  /{SUPP['muon']:.0f}", key="muon", c="#9467bd", lw=1.7, z=4,
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
        f = SUPP[ch["key"]]
        E, y = ch["d"]; y = y / f
        # dotted = the INTRINSIC spectrum: linear response, no saturation, no trigger.
        # The gap to the solid shows both instrumental effects -- trigger rolloff
        # below ~1 eV and bandwidth saturation above the onset.
        Er, yr = unsaturated(ch["key"], design); yr = yr / f
        mr = yr > 0
        if mr.any():
            # Er is already in eV (unsaturated() returns E*C with E in eV); the axis is
            # eV, so plot Er directly. Multiplying by 1e3 -- as the solid curves do, whose
            # column is in keV -- shifted the dotted 1000x to the right. Fixed 2026-07-23.
            ax.loglog(Er[mr], yr[mr], color=ch["c"], lw=1.1, ls=":", alpha=0.75,
                      zorder=ch["z"] - 1)
        m = y > 0
        if m.any():
            ax.loglog(E[m] * 1e3, y[m], color=ch["c"], lw=ch["lw"], label=ch["label"], zorder=ch["z"])

    # 71Ge EC M line -- discrete, 1-2 bins, a BOUND at saturation
    E, y = read(f"ge71_ec_dRdErec_{design}.csv", "E_rec_keV", "dRdErec_bound")
    m = y > 0
    if m.any():
        ax.vlines(E[m] * 1e3, 1e-6, y[m] / SUPP["neutron"], color="#8c564b", lw=2.6, zorder=7,
                  label=f"$^{{71}}$Ge EC M line /{SUPP['neutron']:.0f}  [BOUND, sat.]")

    # prompt (n,gamma) capture -- integrated bound only, NO spectral shape exists
    lvl = CAPTURE_BOUND / SUPP["neutron"] / (ROI_HI - ROI_LO)
    ax.fill_between([ROI_LO * 1e3, ROI_HI * 1e3], lvl * 0.86, lvl * 1.16,
                    color="#ff7f0e", alpha=0.55, hatch="///", edgecolor="#ff7f0e",
                    zorder=2, label=f"Prompt (n,$\\gamma$) capture /{SUPP['neutron']:.0f}  [BOUND,\nno spectral shape derived]")

    # Vertical guide lines (grid floor, sub-eV boundary, saturation onset) and the
    # grey RoI window removed by user request 2026-07-23 to declutter. The pink
    # saturated-band shading is kept -- it carries the saturation the curves show.
    on_dep, on_rec, pl_dep, pl_rec = sat_marks(design)
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
        f = SUPP[ch["key"]]
        E, y = ch["d"]
        v = bin_integrate(E, y / f, ROI_LO, ROI_HI)
        if ch["label"].startswith("CEvNS"):
            sig = v
        else:
            bg += v
    E, y = read(f"ge71_ec_dRdErec_{design}.csv", "E_rec_keV", "dRdErec_trigger_weighted")
    bg_b = bin_integrate(E, y / SUPP["neutron"], ROI_LO, ROI_HI) + CAPTURE_BOUND / SUPP["neutron"]
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
from matplotlib.lines import Line2D  # noqa: E402
_h, _l = axes[0].get_legend_handles_labels()
_h.append(Line2D([0], [0], color="0.35", ls=":", lw=1.4))
_l.append("intrinsic: no saturation, no trigger\n(linear $E_{\\rm rec}$ = 0.497 $E_{\\rm dep}$)")
axes[0].legend(_h, _l, loc="lower left", fontsize=8.0, framealpha=0.94)

axes[1].text(0.985, 0.02,
             "pink band: bandwidth-saturated\n"
             "below 1 eV the reported observable\n"
             "is $P_{\\rm trig}$, not $dR/dE$",
             transform=axes[1].transAxes, ha="right", va="bottom", fontsize=8,
             bbox=dict(fc="white", ec="0.7", alpha=0.92))

_supp_suffix = "NUCLEUS-equivalent suppression: muon ÷{:.0f}, γ ÷{:.0f}, n ÷{:.0f}".format(
    SUPP['muon'], SUPP['compton'], SUPP['neutron'])
fig.suptitle(r"QPD Ge wafer, 3 GW$_{\rm th}$ at 25 m — surface backgrounds with ASSUMED " + _supp_suffix,
             fontsize=11.5, y=0.986)
fig.text(0.5, 0.050,
         "Per-channel factors are NUCLEUS's own published values (>99.8% muon-induced, Pb ÷50, "
         "B$_4$C×COV ÷25), ASSUMED achievable by a future shield/veto — NOT rigorous credit:",
         ha="center", fontsize=8.4, style="italic")
fig.text(0.5, 0.032,
         "they are CaWO$_4$ event-rate reductions and most need the COV/MV veto the wafer does not geometrically fit (Phase 8).",
         ha="center", fontsize=8.4, style="italic")
fig.text(0.5, 0.014,
         "Dotted = the intrinsic spectrum: linear $E_{\\rm rec}$ = 0.497 $E_{\\rm dep}$, NO saturation and NO trigger. The solid-to-dotted gap is the trigger rolloff below ~1 eV and saturation above the onset. "
         "Dotted curves are spikier because $R$ smooths the deposit spectra's MC noise -- that is sampling scatter, not structure.",
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
    print(f"{design}   10-100 eV RoI, TRIGGER-WEIGHTED, NUCLEUS per-channel suppression "
          f"(muon/{SUPP['muon']:.0f}, gamma/{SUPP['compton']:.0f}, n/{SUPP['neutron']:.0f})")
    est = 0.0
    for ch in continua(design):
        f = SUPP[ch["key"]]
        E, y = ch["d"]
        v = bin_integrate(E, y / f, ROI_LO, ROI_HI)
        raw = bin_integrate(*ch["raw"], ROI_LO, ROI_HI)
        if ch["label"].startswith("CEvNS"):
            sig = v
        else:
            est += v
        print(f"   {ch['label']:<34s} {v:10.3f}   (untrig., unsupp. {raw:10.3f})")
    E, y = read(f"ge71_ec_dRdErec_{design}.csv", "E_rec_keV", "dRdErec_trigger_weighted")
    m71 = bin_integrate(E, y / SUPP["neutron"], ROI_LO, ROI_HI)
    capt = CAPTURE_BOUND / SUPP["neutron"]
    nf = SUPP["neutron"]
    print("   {:<34s} {:10.3f}".format(f"71Ge EC M line [BOUND] /{nf:.0f}", m71))
    print("   {:<34s} {:10.3f}".format(f"prompt (n,g) capture [BOUND] /{nf:.0f}", capt))
    print(f"   -> S/B estimates only          {sig/est:.4f}")
    print(f"   -> S/B incl. bounds (LOWER bd) {sig/(est+m71+capt):.4f}\n")
