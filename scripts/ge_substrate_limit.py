"""What-if: heavy-mediator DM-nucleus sensitivity of a Ge SUBSTRATE search, 0.5 eV threshold, reactor-site background.

Exploratory only (not in the EXP statement). Notes and results: notebooks/ge_substrate_dm_limit.ipynb. Run in conda straxion (DarkELF needs its numpy/scipy):
    /opt/anaconda3/envs/straxion/bin/python scripts/ge_substrate_limit.py [threshold_eV]   (default 0.5; 5 -> *_5eV files)
0.5 eV: 90% CL curves for 1 kg day / 1 kg yr (+ S = B in the wide plot). Any other threshold: S = B only
(signal rate in ROI = background rate in ROI, exposure-independent, the QPD convention), plotted against the
0.5 eV S = B curve; run the 0.5 eV case first.

Background: neutron-elastic curve only (solid = reconstructed, trigger-weighted), taken AS PLOTTED, i.e. the
assumed-shield scenario: '/200' in the legend is the assumed neutron-shield suppression factor of the qpd_potential
paper, not a plotting scale (x200 would give the unshielded surface-wafer rate). Digitized from
background_spectrum_2607.05834.webp (a slide plot citing arXiv:2607.05834; the paper itself has no sub-keV
tables). Signal and background both integrated over the fixed ROI threshold - 1 keV.
Signal: DarkELF Ge multiphonon (incl. impulse approximation), same halo as the QPD panel; the single coherent
phonon term is zero above the 37 meV Ge optical phonon, so it is not needed at a 0.5 eV threshold.
Limit: background-limited counting, 90% CL expected (one-sided), N_90 = 1.2816 sqrt(B) (B >> 1 here);
efficiency 50% on signal only (as in the QPD panel); exposures 1 kg day and 1 kg yr; sigma scales as 1/sqrt(exposure).
"""
import contextlib
import io
import os
import sys
import warnings

import numpy as np
import pandas as pd
from PIL import Image
from scipy import ndimage

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA = os.path.join(ROOT, 'data', 'ge_substrate')  # inputs + derived CSVs
FIGS = os.path.join(ROOT, 'figs', 'ge_substrate')
QD = os.path.join(DATA, 'qpd_reference')  # QPD / existing-limit curves of EXP Fig 1(b), copied from QMIT
DARKELF_ROOT = '/Users/lanqingyuan/Documents/GitHub/DarkELF'
E_THR = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5  # eV
E_MAX = 1000.0  # eV, ROI upper edge
SUF = '' if E_THR == 0.5 else f'_{E_THR:g}eV'  # 0.5 eV outputs keep their original names
EFF = 0.5
Z90 = 1.2816
SIGMA_REF = 1e-25
EXPOSURES = {"1 kg day": 1.0, "1 kg yr": 365.25}  # kg day

# ---------------- 1. digitize the neutron-elastic (solid) curve ----------------
# Axis calibration from the major tick marks of the webp (pixels): x 172.5 -> 1e-1 eV ... 1196.5 -> 1e5 eV;
# y 63.5 -> 1e5 ... 693.5 -> 1e-2 counts/(kg day keV).
X0, XPD = 172.5, (1196.5 - 172.5) / 6
Y0, YPD = 63.5, (693.5 - 63.5) / 7
NEUTRON_RGB = (65, 38, 106)
SCALE = 1  # plotted curve = shielded background (neutron suppression 200 already applied); 200 -> unshielded


def digitize():
    a = np.array(Image.open(os.path.join(DATA, 'background_spectrum_2607.05834.webp')).convert('RGB')).astype(int)
    m = np.sqrt(((a - NEUTRON_RGB) ** 2).sum(2)) < 35
    m[:66], m[692:], m[:, :167], m[:, 1195:] = 0, 0, 0, 0
    m[60:320, 885:1190] = 0  # legend
    lab, _ = ndimage.label(m, structure=np.ones((3, 3)))
    sizes = ndimage.sum(m, lab, range(1, lab.max() + 1))
    m = np.isin(lab, 1 + np.where(sizes > 100)[0])  # drop dotted-line dots, keep long solid segments
    # track the solid line column by column from the left edge (only the solid curve is near y~430 there);
    # at the crossing with the dotted 'true' spectrum, follow the linear extrapolation of the last points
    xs, ys = [], []
    for x in range(167, 1100):
        col = np.where(m[:, x])[0]
        if not len(col):
            continue
        groups = np.split(col, np.where(np.diff(col) > 2)[0] + 1)
        cy = np.array([g.mean() for g in groups])
        if len(ys) < 5:
            guess = ys[-1] if ys else 429
        else:
            p = np.polyfit(xs[-5:], ys[-5:], 1)
            guess = np.polyval(p, x)
        j = np.argmin(abs(cy - guess))
        if abs(cy[j] - guess) < 8:
            xs.append(x)
            ys.append(cy[j])
    xs, ys = np.array(xs), np.array(ys)
    E = 10 ** ((xs - X0) / XPD - 1)
    R = 10 ** (5 - (ys - Y0) / YPD) * SCALE
    egrid = np.geomspace(E_THR, E_MAX, 141)  # 40 points/decade
    rgrid = 10 ** np.interp(np.log10(egrid), np.log10(E), np.log10(R))
    out = os.path.join(DATA, f'neutron_elastic_bkg_digitized{SUF}.csv')
    np.savetxt(out, np.c_[egrid, rgrid], delimiter=',', fmt='%.5e',
               header='E_rec_eV,dRdE_counts_per_kg_day_keV  neutron elastic, SOLID (reconstructed) curve as plotted '
                      '= assumed shield (n suppression 200); digitized from background_spectrum_2607.05834.webp, ROI ' + f'{E_THR:g} eV-1 keV')
    return egrid, rgrid, (E, R)


# ---------------- 2. DarkELF Ge signal ----------------
def ge_rates(masses):
    """Signal counts/(kg day) in [E_THR, E_MAX] at sigma_n = SIGMA_REF (no efficiency)."""
    cache = os.path.join(DATA, f'ge_rate_per_kg_day{SUF}.csv')
    if os.path.exists(cache):
        c = np.loadtxt(cache, delimiter=',')
        if len(c) == len(masses) and np.allclose(c[:, 0], masses):
            return c[:, 1]
    sys.path.insert(0, DARKELF_ROOT)
    warnings.filterwarnings('ignore')
    from darkelf import darkelf
    with contextlib.redirect_stdout(io.StringIO()):
        ge = darkelf(target='Ge', vesckms=544, vekms=240, v0kms=238)
    ge.rhoX = 0.45e9
    w = np.geomspace(E_THR, E_MAX, 600)
    per_kg_day = 1 / 365.25  # DarkELF rates are events/kg/yr/eV
    rate = []
    for mMeV in masses:
        ge.update_params(mX=mMeV * 1e6, mediator='massive')
        dr = np.array([ge._dR_domega_multiphonons_SI(x, sigman=SIGMA_REF) for x in w]) * per_kg_day
        rate.append(np.trapezoid(dr, w))
    rate = np.array(rate)
    np.savetxt(cache, np.c_[masses, rate], delimiter=',',
               header=f'm_MeV,counts_per_kg_day in [{E_THR},{E_MAX}] eV at sigma_n={SIGMA_REF} cm^2 '
                      '(DarkELF Ge multiphonon SI, massive mediator, no efficiency)')
    return rate


# ---------------- 3. QPD reference curves (identical to exp_fig1.py panel b) ----------------
def qpd_curves():
    ld = lambda f: np.loadtxt(os.path.join(QD, f), comments="#", delimiter=",")
    rd = lambda f: pd.read_csv(os.path.join(QD, f), header=None, names=["m", "s"]).sort_values("m")
    m_target = 110e-4 ** 2 * 7 * np.pi / 8 * 200e-7 * 2.7 * 1e9
    nr, nr3 = ld("nrhm_rate_per_ng_split.csv"), ld("nrhm_rate_per_ng_3meV.csv")
    nr_rate = {1: nr[:, 1] + nr[:, 2], 3: nr3[:, 1] + nr3[:, 2]}
    scen = {"Baseline": dict(Rd=2.0, Ethr=3, ls="-"), "Goal": dict(Rd=0.01, Ethr=1, ls="--")}
    sig = {k: (SIGMA_REF * v["Rd"] / (EFF * m_target * nr_rate[v["Ethr"]]), v["ls"]) for k, v in scen.items()}
    qroc, dd = rd("qrocodile_limit_nrhm.csv"), rd("dd_limit_nrhm.csv")
    a, b = rd("nrhm_tesseract_lower.csv"), rd("nrhm_tesseract_upper.csv")
    mt = np.geomspace(max(a.m.min(), b.m.min()), min(a.m.max(), b.m.max()), 300)
    return dict(m=nr[:, 0], qpd=sig, res=ld("qualiphide_nrhm_result_digitized.csv"),
                existing=pd.concat([qroc[qroc.m < 150], dd[dd.m > 150]]),
                tess=(mt, np.interp(mt, a.m, a.s), np.interp(mt, b.m, b.s)))


def style():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    tg = "/usr/local/texlive/2026/texmf-dist/fonts/opentype/public/tex-gyre/"
    for f in ("regular", "bold", "italic", "bolditalic"):
        font_manager.fontManager.addfont(tg + f"texgyreschola-{f}.otf")
    plt.rcParams.update({"text.usetex": False, "font.family": "TeX Gyre Schola", "mathtext.fontset": "custom",
                         "mathtext.rm": "TeX Gyre Schola", "mathtext.it": "TeX Gyre Schola:italic",
                         "mathtext.bf": "TeX Gyre Schola:bold", "font.size": 9, "axes.linewidth": 0.6,
                         "xtick.major.width": 0.6, "ytick.major.width": 0.6, "xtick.direction": "in",
                         "ytick.direction": "in", "xtick.top": True, "ytick.right": True})
    return plt


if __name__ == '__main__':
    os.makedirs(FIGS, exist_ok=True)
    egrid, rgrid, raw = digitize()
    B_per_kg_day = np.trapezoid(rgrid / 1e3, egrid)  # counts/(kg day) in ROI
    masses = np.geomspace(0.1, 100, 121)
    S_ref = ge_rates(masses)  # counts/(kg day) at SIGMA_REF
    with np.errstate(divide='ignore'):
        sig_ge = {k: SIGMA_REF * Z90 * np.sqrt(B_per_kg_day * X) / (EFF * S_ref * X) for k, X in EXPOSURES.items()}
        sig_sb = SIGMA_REF * B_per_kg_day / (EFF * S_ref)  # S = B, the convention of the QPD curves
    if SUF:
        np.savetxt(os.path.join(DATA, f'ge_substrate_sigma_SB{SUF}.csv'), np.c_[masses, sig_sb], delimiter=',',
                   fmt='%.4e', header=f'm_MeV,sigma_S_eq_B [cm^2], ROI {E_THR:g} eV-1 keV, eff {EFF}; '
                                      'inf = no signal above threshold')
        d05 = np.loadtxt(os.path.join(DATA, 'ge_substrate_sigma90.csv'), delimiter=',')
        curves = [(masses, sig_sb, "-", f"Ge {E_THR:g} eV, S = B"), (d05[:, 0], d05[:, 3], ":", "Ge 0.5 eV, S = B")]
    else:
        np.savetxt(os.path.join(DATA, 'ge_substrate_sigma90.csv'),
                   np.c_[masses, sig_ge["1 kg day"], sig_ge["1 kg yr"], sig_sb], delimiter=',', fmt='%.4e',
                   header='m_MeV,sigma90_1kgday,sigma90_1kgyr,sigma_S_eq_B [cm^2]; inf = no signal above 0.5 eV')
        curves = [(masses, s, ls, f"Ge {k}") for (k, s), ls in zip(sig_ge.items(), (":", "-"))]

    q = qpd_curves()
    plt = style()
    GREY, C_RES, C_1S, DARK_BLUE, C_GE = "0.86", '#e6863b', "#8fd18f", '#08306b', '#a50f15'

    def panel(ax, ylim):
        ax.fill_between(q["existing"].m, q["existing"].s, 1e-18, color=GREY, lw=0, zorder=-2)
        ax.fill_between(*q["tess"], color="0.6", alpha=0.5, lw=0, zorder=-1)
        res = q["res"]
        ax.fill_between(res[:, 0], res[:, 1], 1e-18, color=C_RES, lw=0)
        ax.plot(res[:, 0], res[:, 1], color="0.2", lw=0.8)
        ax.fill_between(res[:, 0], res[:, 1] / 120, res[:, 1] / 50, color=C_1S, lw=0)
        for k, (s, ls) in q["qpd"].items():
            ax.plot(q["m"], s, color=DARK_BLUE, ls=ls, lw=1.1, zorder=3, label=f"QPD {k}")
        for m, s, ls, lab in curves:
            if (s < ylim[1]).any():
                ax.plot(m, s, color=C_GE, ls=ls, lw=1.1, zorder=4, label=lab)
            else:  # off the panel everywhere: say so instead of an invisible legend entry
                ax.text(0.04, 0.47, f"{lab}:\nno reach for m $\\leq$ 100 MeV", transform=ax.transAxes,
                        ha="left", va="top", color=C_GE, fontsize=5.5, linespacing=1.0)
        ax.set(xscale="log", yscale="log", xlim=(0.1, 100), ylim=ylim,
               xlabel=r"DM mass [MeV]", ylabel=r"$\bar\sigma_n$ [cm$^2$]")
        ax.set_xticks([0.1, 1, 10, 100])

    W, H = 2.55, 2.25
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0.55 / W, 0.45 / H, 1.88 / W, 1.68 / H])
    panel(ax, (1e-30, 1e-25))
    ax.set_yticks([1e-30, 1e-28, 1e-26])
    ax.legend(frameon=False, fontsize=6.5, loc="lower left", handlelength=1.6, handletextpad=0.5, borderaxespad=0.2)
    fig.savefig(os.path.join(FIGS, f'ge_substrate_limit{SUF}.pdf'))
    fig.savefig(os.path.join(FIGS, f'ge_substrate_limit{SUF}.png'), dpi=300)

    if not SUF:  # wider y range so the Ge minimum (far below 1e-30) is visible
        fig = plt.figure(figsize=(3.4, 2.6))
        ax = fig.add_axes([0.55 / 3.4, 0.45 / 2.6, 2.7 / 3.4, 2.05 / 2.6])
        panel(ax, (1e-42, 1e-18))
        ax.plot(masses, sig_sb, color=C_GE, ls="--", lw=0.8, zorder=4, label="Ge, S = B")
        ax.axhline(1e-25, color="0.4", lw=0.5, ls=(0, (1, 2)))
        ax.axhline(1e-30, color="0.4", lw=0.5, ls=(0, (1, 2)))
        ax.legend(frameon=False, fontsize=6.5, loc="lower left", handlelength=1.6, handletextpad=0.5)
        fig.savefig(os.path.join(FIGS, 'ge_substrate_limit_wide.pdf'))
        fig.savefig(os.path.join(FIGS, 'ge_substrate_limit_wide.png'), dpi=300)

    # ---- summary ----
    print(f"Neutron-elastic background in [{E_THR}, {E_MAX}] eV: {B_per_kg_day:.3e} counts/(kg day)")
    for e in [e for e in (0.5, 1, 2, 5, 10, 100, 1000) if e >= E_THR]:
        print(f"  dR/dE({e:g} eV) = {np.interp(np.log10(e), np.log10(egrid), rgrid):.3e} /(kg day keV)")
    for k, s in ([] if SUF else list(sig_ge.items())) + [("S = B", sig_sb)]:
        i = np.argmin(s)
        fin = masses[np.isfinite(s)]
        cr = lambda t: (f"{masses[s < t].min():.1f} MeV" if (s < t).any() else "never (m <= 100 MeV)")
        print(f"Ge {k}: min sigma {s[i]:.2e} at {masses[i]:.1f} MeV; signal > 0 from {fin.min():.1f} MeV; "
              f"below 1e-25 from {cr(1e-25)}; below 1e-30 from {cr(1e-30)}")
    for k, (s, _) in q["qpd"].items():
        i = np.argmin(s)
        print(f"QPD {k}: min sigma {s[i]:.2e} at {q['m'][i]:.1f} MeV")
    for mm in (10, 20, 30, 50, 100):
        i = np.argmin(abs(masses - mm))
        print(f"  m={masses[i]:.1f} MeV: S_ref={S_ref[i]:.3e}/(kg day); S=B {sig_sb[i]:.2e}"
              + ("" if SUF else f", 1kgd {sig_ge['1 kg day'][i]:.2e}, 1kgyr {sig_ge['1 kg yr'][i]:.2e}"))

    # free-nucleus kinematic edge: E_R,max = 2 mu^2 v_max^2 / m_N reaches the threshold at this DM mass
    mN = 72 * 0.9315e9  # eV (DarkELF Ge A = 72)
    vmax = (544 + 240) / 2.998e5
    mu = np.sqrt(E_THR * mN / (2 * vmax ** 2))
    print(f"Free-nucleus edge: E_R,max = {E_THR:g} eV at m = {mu * mN / (mN - mu) / 1e6:.0f} MeV "
          "(below this, reach comes only from the DarkELF impulse-approximation tail)")
