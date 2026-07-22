# ASSERT_CONVENTION: natural_units=io_MeV, flux_units=nubar_per_cm2_per_s_per_MeV, power=GW_thermal, standoff_cm=2500
"""
Freeze the absolute reactor antineutrino flux Phi(E_nu) as a versioned, provenance-tagged
CSV, attach the split above/below-2-MeV uncertainty band and region flags, emit the
validation overlay figure, and provide the Billard-2017 closure variant.

Deliverables (Plan 02-02):
    * data/flux/reactor_flux_v1.0.csv          -- frozen flagship table (deliv-frozen-csv)
    * GPD/.../figures/flux_overlay.png         -- Phi vs published Huber, band shown
    * data/flux/reactor_flux_billard_variant.csv -- Billard closure variant (test-billard-variant)

Split band (guards fp-uniform-band): the >2 MeV region is data-anchored (Huber-Mueller,
~2-5%); the never-measured sub-1.8 MeV region is model-only and carries a WIDE band
(20-25%) that honestly covers the Estienne-Fallot-vs-CONFLUX model spread and the fact
that the sub-1.8 MeV summation SHAPE is a Kopeikin-2012-consistent MODEL PLACEHOLDER
(a primary digitized Kopeikin-2012 per-isotope table was not machine-sourceable
in-environment -- see SUMMARY 02-02).
"""
from __future__ import annotations

import datetime as _dt
import os
import subprocess

import numpy as np

from .assemble_spectrum import (
    assemble,
    build_energy_grid,
    AssembledSpectrum,
    FISSION_FRACTIONS_DEFAULT,
    FISSION_FRACTIONS_BILLARD,
    SEAM_LO,
    SEAM_HI,
)
from .huber_mueller import ISOTOPES, load_coefficients, hm_spectrum
from . import normalization as norm

_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
_DATADIR = os.path.join(_ROOT, "data", "flux")
_FIGDIR = os.path.join(_ROOT, "GPD", "phases", "02-reactor-flux-model", "figures")

VERSION = "v1.0"


def _git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=_ROOT, text=True
        ).strip()
    except Exception:
        return "unknown"


# --------------------------------------------------------------------------------
# Split uncertainty band (fp-uniform-band guard)
# --------------------------------------------------------------------------------
def rel_uncertainty(E: np.ndarray) -> np.ndarray:
    """Per-bin relative uncertainty, WIDENING across the ~1.8-2 MeV seam.

    >=2.0 MeV   : data-anchored Huber-Mueller, 2.5% -> 5% (grows with energy).
    1.8-2.0 MeV : seam / transition, 10%.
    1.0-1.8 MeV : model-only summation region, 20%.
    <1.0 MeV    : deepest model extrapolation + n-capture power-correlation caveat, 25%.
    """
    E = np.asarray(E, dtype=float)
    u = np.empty_like(E)
    above = E >= SEAM_HI
    seam = (E >= SEAM_LO) & (E < SEAM_HI)
    mid = (E >= 1.0) & (E < SEAM_LO)
    low = E < 1.0
    u[above] = np.clip(0.025 + 0.005 * (E[above] - 2.0), 0.02, 0.05)
    u[seam] = 0.10
    u[mid] = 0.20
    u[low] = 0.25
    return u


def region_flag(E: np.ndarray) -> np.ndarray:
    E = np.asarray(E, dtype=float)
    flags = np.where(E >= SEAM_HI, "above_2MeV",
                     np.where(E < SEAM_LO, "below_1p8MeV", "seam"))
    return flags


# --------------------------------------------------------------------------------
# Flagship frozen table
# --------------------------------------------------------------------------------
def build_flux_components(spec: AssembledSpectrum,
                          p_th_w: float = norm.P_TH_DEFAULT_W,
                          d_cm: float = norm.D_CM_DEFAULT):
    """Return (E, total, fission_HM, fission_summation, ncapture) fluxes [nu/cm2/s/MeV].

    Additive by construction: fission_HM + fission_summation + ncapture == total.
    HM column carries the data-anchored region (E>=1.8, incl. the seam blend); the
    summation column carries the model-only region (E<1.8).
    """
    E = spec.E
    K, _ = norm.normalization_constant(spec.fractions, p_th_w=p_th_w, d_cm=d_cm)
    fission = spec.fission_weighted() * K
    ncap = spec.ncapture * K
    hm = np.where(E >= SEAM_LO, fission, 0.0)
    summ = np.where(E < SEAM_LO, fission, 0.0)
    total = fission + ncap
    return E, total, hm, summ, ncap


def write_frozen_csv(spec: AssembledSpectrum, path: str,
                     p_th_w: float = norm.P_TH_DEFAULT_W,
                     d_cm: float = norm.D_CM_DEFAULT) -> dict:
    E, total, hm, summ, ncap = build_flux_components(spec, p_th_w=p_th_w, d_cm=d_cm)
    u = rel_uncertainty(E)
    flags = region_flag(E)

    _, diag = norm.normalization_constant(spec.fractions, p_th_w=p_th_w, d_cm=d_cm)
    y = spec.integral_yields()
    F = norm.integral_flux(E, total)
    rate = norm.emission_rate_per_gwth(y["grand_total_per_fission"], spec.fractions, p_th_w=p_th_w)

    checks = {
        "grand_total_per_fission": y["grand_total_per_fission"],
        "above_1p8_per_fission": y["above_1p8_per_fission"],
        "integral_flux": F,
        "emission_per_GWth": rate,
    }

    with open(path, "w") as f:
        f.write(f"# QPD Phase-2 Plan 02-02 -- FROZEN reactor antineutrino flux Phi(E_nu), version {VERSION}\n")
        f.write(f"# generated: {_dt.date.today().isoformat()}   git_sha: {_git_sha()}\n")
        f.write("# Units: flux in nu-bar cm^-2 s^-1 MeV^-1 ; E_nu in MeV.\n")
        f.write(f"# Normalization: P_th = {p_th_w/1e9:.3g} GW_th (THERMAL, not electric), standoff d = {d_cm/100:.0f} m,\n")
        f.write(f"#   point source 1/(4 pi d^2); <E_f> = {diag['E_f_MeV']:.3f} MeV effective thermal per fission\n")
        f.write("#   (Ma et al. PRC 88,014605 (2013): 202.4/205.9/211.1/213.6 MeV for 235/238/239/241; NOT total Q).\n")
        f.write(f"#   R_f = {diag['R_f_fissions_per_s']:.4e} fissions/s ; 1/(4 pi d^2) = {diag['geometry_cm^-2']:.4e} cm^-2.\n")
        f.write(f"# Fission fractions (isotope-labelled): {dict(spec.fractions)}\n")
        f.write("# Component provenance:\n")
        f.write("#   flux_fission_HM (E>=1.8 MeV): SOURCED Huber arXiv:1106.0687 (235U/239Pu/241Pu) +\n")
        f.write("#     Mueller arXiv:1101.2663 (238U); reconstructed 235U within 0.73%/0.13% of published Huber.\n")
        f.write("#   flux_fission_summation (E<1.8 MeV): MODEL PLACEHOLDER, seam-anchored, Kopeikin-2012-CONSISTENT\n")
        f.write("#     (Kopeikin, Phys. At. Nucl. 75, 143 (2012)); a primary digitized Kopeikin-2012 per-isotope\n")
        f.write("#     table was NOT machine-sourceable in-environment -- covered by the wide (20-25%) below-1.8 band.\n")
        f.write("#   flux_ncapture_238U: 238U(n,gamma) allowed-beta shape (AME2020 Q-values) normalized to\n")
        f.write("#     0.6 nu-bar/fission (Kopeikin 2004 / Huber-Jaffke PRL 116,122503 (2016)).\n")
        f.write("# Uncertainty band (SPLIT, not uniform): ~2-5% above 2 MeV (data-anchored); 10% at the seam;\n")
        f.write("#   20% on 1.0-1.8 MeV; 25% below 1.0 MeV (model-only, EF-vs-CONFLUX spread + n-capture caveat).\n")
        f.write(f"# Integral checks: grand total = {checks['grand_total_per_fission']:.3f} nu-bar/fission;\n")
        f.write(f"#   above-1.8 = {checks['above_1p8_per_fission']:.3f} nu-bar/fission;\n")
        f.write(f"#   int Phi dE = {F:.4e} nu-bar cm^-2 s^-1 (authoritative target 7-8e12);\n")
        f.write(f"#   emission = {rate:.4e} nu-bar s^-1 GW_th^-1 (Hayes-Vogel ~2e20).\n")
        cols = ["E_nu_MeV", "flux_nu_per_cm2_per_s_per_MeV", "flux_fission_HM",
                "flux_fission_summation", "flux_ncapture_238U", "rel_uncertainty", "region_flag"]
        f.write(",".join(cols) + "\n")
        for k, e in enumerate(E):
            row = [f"{e:.6g}", f"{total[k]:.6e}", f"{hm[k]:.6e}",
                   f"{summ[k]:.6e}", f"{ncap[k]:.6e}", f"{u[k]:.4f}", str(flags[k])]
            f.write(",".join(row) + "\n")
    return checks


# --------------------------------------------------------------------------------
# Billard-2017 closure variant (HM + constant below 2 MeV, Billard fractions)
# --------------------------------------------------------------------------------
def billard_variant_perisotope(E: np.ndarray) -> dict:
    """Per-isotope S_i(E): Huber-Mueller for E>=2 MeV, held CONSTANT below 2 MeV.

    This is the Billard (2017) flux assumption (arXiv:1612.09035): the HM spectra are
    used above 2 MeV and held flat below, instead of the flagship summation extension.
    """
    coeffs = load_coefficients()
    out = {}
    for iso in ISOTOPES:
        a = coeffs[iso]
        S = hm_spectrum(E, a)
        S_at_2 = float(hm_spectrum(SEAM_HI, a))
        out[iso] = np.where(E >= SEAM_HI, S, S_at_2)   # constant below 2 MeV
    return out


def write_billard_variant_csv(path: str,
                              grid: np.ndarray | None = None,
                              p_th_w: float = norm.P_TH_DEFAULT_W,
                              d_cm: float = norm.D_CM_DEFAULT) -> dict:
    """Freeze the Billard-assumption variant flux (distinct from the flagship)."""
    if grid is None:
        grid = build_energy_grid()
    E = grid
    fr = dict(FISSION_FRACTIONS_BILLARD)
    per_iso = billard_variant_perisotope(E)
    fission_pf = np.zeros_like(E)
    for iso, fval in fr.items():
        fission_pf += fval * per_iso[iso]
    K, diag = norm.normalization_constant(fr, p_th_w=p_th_w, d_cm=d_cm)
    flux = fission_pf * K
    F = norm.integral_flux(E, flux)

    with open(path, "w") as f:
        f.write(f"# QPD Phase-2 Plan 02-02 -- BILLARD-2017 CLOSURE VARIANT (validation, NOT the flagship)\n")
        f.write(f"# generated: {_dt.date.today().isoformat()}   git_sha: {_git_sha()}\n")
        f.write("# Billard et al., J. Phys. G 44, 105101 (2017), arXiv:1612.09035.\n")
        f.write("# Assumptions reproduced: Huber-Mueller spectra held CONSTANT below 2 MeV; fission\n")
        f.write("#   fractions 235U/239Pu/238U/241Pu = 55.6/32.6/7.1/4.7 % (isotope-labelled).\n")
        f.write(f"#   Fractions used: {fr}\n")
        f.write(f"# Normalization: {p_th_w/1e9:.3g} GW_th, {d_cm/100:.0f} m, <E_f> = {diag['E_f_MeV']:.3f} MeV,\n")
        f.write(f"#   R_f = {diag['R_f_fissions_per_s']:.4e} fissions/s. int Phi dE = {F:.4e} nu-bar cm^-2 s^-1.\n")
        f.write("# NOTE: n-capture excluded and sub-2 MeV held flat, matching Billard's flux assumption;\n")
        f.write("#   ready for the Phase-3 Billard Table 1 reproduction. Do NOT use as the flagship flux.\n")
        cols = ["E_nu_MeV", "flux_nu_per_cm2_per_s_per_MeV"] + [f"S_{iso}_constbelow2" for iso in ISOTOPES] + ["region_flag"]
        f.write(",".join(cols) + "\n")
        for k, e in enumerate(E):
            reg = "above_2MeV" if e >= SEAM_HI else "constant_below_2MeV"
            row = [f"{e:.6g}", f"{flux[k]:.6e}"] + [f"{per_iso[iso][k]:.6g}" for iso in ISOTOPES] + [reg]
            f.write(",".join(row) + "\n")
    return {"integral_flux": F, "E_f_MeV": diag["E_f_MeV"], "fractions": fr}


# --------------------------------------------------------------------------------
# Overlay validation figure
# --------------------------------------------------------------------------------
def make_overlay_figure(spec: AssembledSpectrum, path: str,
                        p_th_w: float = norm.P_TH_DEFAULT_W,
                        d_cm: float = norm.D_CM_DEFAULT) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    E, total, hm, summ, ncap = build_flux_components(spec, p_th_w=p_th_w, d_cm=d_cm)
    u = rel_uncertainty(E)
    K, _ = norm.normalization_constant(spec.fractions, p_th_w=p_th_w, d_cm=d_cm)
    f235 = spec.fractions["235U"]

    # computed 235U flux contribution and published-Huber-235U scaled to the same quantity
    computed_235 = spec.per_isotope["235U"] * f235 * K
    bench_rows = []
    with open(os.path.join(_DATADIR, "huber_U235_benchmark.csv")) as bf:
        for line in bf:
            if line.startswith("#") or line.startswith("E_nu"):
                continue
            parts = line.strip().split(",")
            if len(parts) == 2:
                bench_rows.append((float(parts[0]), float(parts[1])))
    bench_rows = np.array(bench_rows)
    Eb = bench_rows[:, 0]
    pub_235_flux = bench_rows[:, 1] * f235 * K

    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    ax.fill_between(E, total * (1 - u), total * (1 + u), color="C0", alpha=0.25,
                    label="total flux band (split: 2-5% >2 MeV, 20-25% <1.8 MeV)")
    ax.plot(E, total, color="C0", lw=2.0, label=r"$\Phi(E_\nu)$ total (flagship)")
    ax.plot(E, computed_235, color="C1", lw=1.4, ls="--",
            label=r"computed $^{235}$U flux contribution")
    ax.plot(Eb, pub_235_flux, "k.", ms=7, label="published Huber $^{235}$U (arXiv:1106.0687)")
    ax.axvspan(SEAM_LO, SEAM_HI, color="grey", alpha=0.15)
    ax.axvline(SEAM_HI, color="grey", ls=":", lw=1)
    ax.set_xlabel(r"$E_\nu$ [MeV]")
    ax.set_ylabel(r"$\Phi$ [$\bar\nu\,\mathrm{cm^{-2}\,s^{-1}\,MeV^{-1}}$]")
    ax.set_yscale("log")
    ax.set_xlim(0.1, 8.0)
    ax.set_ylim(1e9, 5e12)
    ax.set_title("Absolute reactor $\\bar\\nu$ flux at 3 GW$_{th}$, 25 m\n"
                 "flagship vs published Huber $^{235}$U (>2 MeV), split band")
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, which="both", alpha=0.2)
    fig.tight_layout()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=140)
    plt.close(fig)


def build_all():
    spec = assemble()  # default PWR fractions
    os.makedirs(_DATADIR, exist_ok=True)
    frozen = os.path.join(_DATADIR, "reactor_flux_v1.0.csv")
    checks = write_frozen_csv(spec, frozen)
    billard = os.path.join(_DATADIR, "reactor_flux_billard_variant.csv")
    bchecks = write_billard_variant_csv(billard, grid=spec.E)
    fig = os.path.join(_FIGDIR, "flux_overlay.png")
    make_overlay_figure(spec, fig)
    return frozen, billard, fig, checks, bchecks


if __name__ == "__main__":
    frozen, billard, fig, checks, bchecks = build_all()
    print("wrote", frozen)
    print("wrote", billard)
    print("wrote", fig)
    for k, v in checks.items():
        print(f"  {k:28s} {v:.4e}" if isinstance(v, float) else f"  {k}: {v}")
    print(f"  billard integral flux       {bchecks['integral_flux']:.4e}")
