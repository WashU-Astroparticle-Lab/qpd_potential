# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
#
# Klein-Nishina angle-sampled electron-recoil CONTINUUM and assembly of the
# environmental-gamma Compton deposited-energy spectrum dR/dE_dep for the thin Ge
# wafer (Plan 04-02, CALC-04 / VALD-03).
#
# KEY PHYSICS (guards the forbidden proxies):
#  * DEPOSIT = Compton ELECTRON recoil T_e = E_gamma - E' (the scattered photon
#    escapes the optically-thin 2 mm wafer). NOT E_gamma, NOT E'. This is a
#    CONTINUUM up to each edge E_edge = 2E^2/(m_e c^2 + 2E), with NO photopeaks.
#    Guards fp-full-absorption, fp-electron-not-photon.
#  * The scattering angle theta is sampled from the Klein-Nishina dsigma/dOmega and
#    T_e follows KINEMATICALLY, so the Compton edge falls out automatically
#    (self-validating) -- no error-prone closed-form dsigma/dT_e change of variables.
#  * Each line is weighted by the thin-target SINGLE-SCATTER interaction rate
#    R_i = Phi_i * (S/4) * [1 - exp(-mu(E_i) * ell_bar)] on the ONE pinned Cauchy
#    mean chord ell_bar = 4V/S = 0.385 cm (compton_source). Cross-checked against
#    the independent anchor Phi_i * sigma_KN(E_i) * N_e (flux x Compton cross
#    section x electrons), agreeing to ~few % (VALD-03 factor-2).
#  * Unified phonon E_dep scale, NO quenching (CONVENTIONS Section B). The deposit
#    is an electron recoil with zero defect correction. Guards fp-quenching-compton.
#
# Output dR/dE_dep is on the SHARED log E_dep grid (muon_deposit.shared_energy_grid),
# counts/kg/day/keV, so the muon (04-01) and Compton channels co-add in Phase 5.

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from . import compton_source as cs
from .muon_deposit import shared_energy_grid   # SHARED grid (identical to 04-01)

M_E_KEV = cs.M_E_KEV
R_E_CM = cs.R_E_CM


# --------------------------------------------------------------------------- #
# Klein-Nishina differential cross section and angle sampling                  #
# --------------------------------------------------------------------------- #
def kn_dsigma_domega(e_gamma_kev: float, cos_theta: np.ndarray) -> np.ndarray:
    """Klein-Nishina dsigma/dOmega [cm^2/sr] per free electron vs cos(theta).

    dsigma/dOmega = (r_e^2/2)(E'/E)^2 (E'/E + E/E' - sin^2 theta),
      E'(theta) = E / (1 + alpha(1 - cos theta)),  alpha = E / m_e c^2.
    """
    alpha = e_gamma_kev / M_E_KEV
    ratio = 1.0 / (1.0 + alpha * (1.0 - cos_theta))   # E'/E
    sin2 = 1.0 - cos_theta**2
    return 0.5 * R_E_CM**2 * ratio**2 * (ratio + 1.0 / ratio - sin2)


def sample_electron_recoil(e_gamma_kev: float, n: int,
                           rng: np.random.Generator) -> np.ndarray:
    """Sample n electron-recoil energies T_e [keV] for a line E_gamma via
    rejection sampling of cos(theta) ~ dsigma/dOmega, then T_e = E_gamma - E'.

    The Compton edge T_e(theta=pi) = E_edge falls out kinematically (the max
    possible T_e), so the edge is self-validating and NEVER exceeds E_edge.
    """
    alpha = e_gamma_kev / M_E_KEV
    # Envelope: dsigma/dOmega is largest at forward scattering (cos=1) for these
    # alpha; bound it on a fine grid to be safe.
    cgrid = np.linspace(-1.0, 1.0, 4001)
    fmax = kn_dsigma_domega(e_gamma_kev, cgrid).max() * 1.02

    out = np.empty(n)
    filled = 0
    while filled < n:
        m = int((n - filled) * 1.6) + 64
        c = rng.uniform(-1.0, 1.0, m)
        f = kn_dsigma_domega(e_gamma_kev, c)
        acc = rng.uniform(0.0, fmax, m) < f
        c_acc = c[acc]
        take = min(c_acc.size, n - filled)
        cos_theta = c_acc[:take]
        e_prime = e_gamma_kev / (1.0 + alpha * (1.0 - cos_theta))
        out[filled:filled + take] = e_gamma_kev - e_prime   # T_e
        filled += take
    return out


# --------------------------------------------------------------------------- #
# Per-line single-scatter interaction rate (thin target, pinned mean chord)    #
# --------------------------------------------------------------------------- #
def line_interaction_rate_hz(flux_cm2_s: float, e_gamma_kev: float) -> float:
    """Single-scatter Compton interaction rate for one line in the whole wafer [s^-1].

    R = Phi * (S/4) * [1 - exp(-mu(E) * ell_bar)], the isotropic-flux entry rate
    Phi*S/4 times the single-crossing interaction probability on the pinned mean
    chord ell_bar = 4V/S. Consistent with the double-scatter and rate bookkeeping.
    """
    P = float(cs.interaction_prob(e_gamma_kev))          # 1 - exp(-mu ell_bar)
    return flux_cm2_s * (cs.S_SURFACE / 4.0) * P


def line_rate_anchor_hz(flux_cm2_s: float, e_gamma_kev: float) -> float:
    """Independent VALD-03 anchor: Phi * sigma_KN(E) * N_e (flux x Compton cross
    section x wafer electrons) [s^-1]. Uses the closed-form KN cross section."""
    return flux_cm2_s * float(cs.sigma_kn(e_gamma_kev)) * cs.N_E_WAFER


# --------------------------------------------------------------------------- #
# Full Compton dR/dE_dep assembly                                              #
# --------------------------------------------------------------------------- #
@dataclass
class ComptonSpectrum:
    edges_kev: np.ndarray
    centers_kev: np.ndarray
    dRdE: np.ndarray            # counts / kg / day / keV
    dRdE_err: np.ndarray        # per-bin MC statistical error, same units
    rate_hz: float              # total single-scatter interaction rate [Hz]
    rate_anchor_hz: float       # flux x sigma_KN x N_e cross-check [Hz]
    line_energies: np.ndarray   # E_gamma per line [keV]
    line_edges: np.ndarray      # E_edge per line [keV]
    line_edges_sampled: np.ndarray   # max sampled T_e per line [keV]
    line_rates_hz: np.ndarray   # R_i per line [Hz]
    n_per_line: int
    counts_per_kg_day: float    # integral of dR/dE_dep dE (energy closure)


def run_compton_mc(n_per_line: int = 400_000, seed: int = 20260720) -> ComptonSpectrum:
    """Assemble the Compton electron-recoil dR/dE_dep on the shared log E_dep grid.

    For each sourced line: sample T_e ~ Klein-Nishina (angle -> kinematics), weight
    by the single-scatter rate R_i, histogram onto the shared grid in counts/kg/day/keV.
    """
    rng = np.random.default_rng(seed)
    lines = cs.load_gamma_lines()

    edges = shared_energy_grid()
    centers = np.sqrt(edges[:-1] * edges[1:])
    dwidth = np.diff(edges)
    per_day = 86400.0 / cs.MASS_KG           # Hz -> counts/kg/day

    sumw = np.zeros(centers.size)
    sumw2 = np.zeros(centers.size)

    e_g, e_edge, e_edge_s, r_line = [], [], [], []
    total_rate = 0.0
    total_anchor = 0.0
    for ln in lines:
        R_i = line_interaction_rate_hz(ln.flux_cm2_s, ln.energy_keV)     # Hz
        A_i = line_rate_anchor_hz(ln.flux_cm2_s, ln.energy_keV)          # Hz (anchor)
        total_rate += R_i
        total_anchor += A_i

        te = sample_electron_recoil(ln.energy_keV, n_per_line, rng)      # keV
        w = R_i * per_day / n_per_line                                   # cts/kg/day per sample
        h, _ = np.histogram(te, bins=edges)
        h2 = h.astype(float)
        sumw += h2 * w
        sumw2 += h2 * w * w

        e_g.append(ln.energy_keV)
        e_edge.append(float(cs.compton_edge_kev(ln.energy_keV)))
        e_edge_s.append(float(te.max()))
        r_line.append(R_i)

    dRdE = sumw / dwidth
    dRdE_err = np.sqrt(sumw2) / dwidth
    counts_per_kg_day = float((dRdE * dwidth).sum())

    return ComptonSpectrum(
        edges_kev=edges,
        centers_kev=centers,
        dRdE=dRdE,
        dRdE_err=dRdE_err,
        rate_hz=float(total_rate),
        rate_anchor_hz=float(total_anchor),
        line_energies=np.asarray(e_g),
        line_edges=np.asarray(e_edge),
        line_edges_sampled=np.asarray(e_edge_s),
        line_rates_hz=np.asarray(r_line),
        n_per_line=n_per_line,
        counts_per_kg_day=counts_per_kg_day,
    )


def write_csv(spec: ComptonSpectrum, path: str) -> None:
    """Write dR/dE_dep to CSV: E_dep_keV, dRdEdep_cts_per_kg_day_keV, mc_err."""
    import csv as _csv

    header_lines = [
        "# Compton (environmental-gamma) deposited-energy spectrum dR/dE_dep,",
        "# 4in x 4in x 2mm Ge wafer. Plan 04-02 (CALC-04/VALD-03).",
        "# Klein-Nishina angle-sampled ELECTRON recoil T_e continuum (NO photopeaks,",
        "# scattered photon escapes the thin wafer), thin-target single-scatter on the",
        "# pinned Cauchy mean chord ell_bar = 4V/S = 0.385 cm. UNIFIED PHONON SCALE,",
        "# NO quenching (CONVENTIONS Section B). Gamma flux = sourced tunable input",
        "# (data/gamma_lines.csv, provenance).",
        f"# total_single_scatter_rate_Hz = {spec.rate_hz:.4e} "
        f"(flux x sigma_KN x N_e anchor = {spec.rate_anchor_hz:.4e}; "
        f"ratio {spec.rate_hz / spec.rate_anchor_hz:.3f})",
        f"# integral dR/dE_dep = {spec.counts_per_kg_day:.4e} counts/kg/day "
        f"(= total_rate * 86400 / mass_kg; energy closure)",
        f"# n_mc_samples_per_line = {spec.n_per_line}; seed fixed for reproducibility",
        "# units: E_dep_keV [keV]; dRdEdep [counts/kg/day/keV]; mc_err [counts/kg/day/keV]",
        "# grid: shared log E_dep, 0.01 keV -> 2e5 keV (200 MeV), ~80 bins/decade (matches 04-01)",
    ]
    with open(path, "w", newline="") as f:
        for line in header_lines:
            f.write(line + "\n")
        w = _csv.writer(f)
        w.writerow(["E_dep_keV", "dRdEdep_cts_per_kg_day_keV", "mc_err"])
        for c, y, e in zip(spec.centers_kev, spec.dRdE, spec.dRdE_err):
            w.writerow([f"{c:.6e}", f"{y:.6e}", f"{e:.6e}"])
