# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
#
# Landau-Vavilov most-probable-value (MPV) deposit per chord and assembly of the
# sea-level muon deposited-energy spectrum dR/dE_dep for the thin Ge wafer
# (Plan 04-01, CALC-03 / VALD-02).
#
# ENERGY SCALE: unified phonon E_dep scale, NO ionization quenching, NO
# keVee/keVnr split (CONVENTIONS Section B; the muon deposit is an electron
# recoil with zero Frenkel-defect correction). Guards fp-quenching-muon.
#
# KEY PHYSICS (guards the forbidden proxies):
#  * Per-chord deposit sampled from the LANDAU-VAVILOV distribution using the
#    most-probable value Delta_p (NOT the mean <dE/dx>*ell, NOT Moyal).
#    Guards fp-mean-not-mpv / RESEARCH Pitfall 2.
#  * Landau formulas use MASS THICKNESS x = rho*ell [g/cm^2], carried explicitly.
#    Guards RESEARCH Pitfall 4.
#  * Surface-flux measure I(theta)*A_proj*sin(theta) (muon_flux/wafer_geometry),
#    NOT bare cos^2(theta). Guards fp-angular-bias / RESEARCH Pitfall 3.
#  * Near-horizontal long chords resolved by sampling zenith uniformly in
#    [0, pi/2] (oversamples the horizon relative to the physical sin*cos^2
#    measure) so the tens-of-MeV Phase-5 saturation tail is populated.
#
# Delta_p is COMPUTED here from the PDG "Passage of Particles Through Matter"
# formula; nothing is hard-coded from memory. The custom Landau sampler is a
# numerical inverse-CDF of the Landau density built from its integral definition
# (mode lambda = -0.22278, textbook/PDG value) and is validated against the PDG
# Delta_p and xi(vertical) ~= 0.072 MeV. pylandau is an optional second opinion.

from __future__ import annotations

import warnings
from dataclasses import dataclass

import numpy as np
from scipy import integrate

from . import muon_flux, wafer_geometry

# --------------------------------------------------------------------------- #
# Physical constants (PDG)                                                     #
# --------------------------------------------------------------------------- #
M_MU = 105.6583745      # muon mass [MeV]
M_E = 0.51099895        # electron mass [MeV]
K_MEV = 0.307075        # 4 pi N_A r_e^2 m_e c^2 [MeV mol^-1 cm^2] (PDG K)
Z_OVER_A_GE = 0.4406    # Ge <Z/A> = 32 / 72.63
I_GE = 350.0e-6         # Ge mean excitation energy I [MeV] (350 eV)
J_LANDAU = 0.200        # PDG MPV constant j
DEDX_MEAN = 1.370       # Ge minimum-ionizing <dE/dx> [MeV cm^2/g] (CONVENTIONS G)

RHO = wafer_geometry.RHO  # 5.323 g/cm^3

# Sternheimer density-effect parameters for germanium
# (Sternheimer, Berger & Seltzer, At. Data Nucl. Data Tables 30, 261 (1984);
#  ICRU-37 elemental table). MEDIUM confidence: standard tabulated coefficients;
#  the density effect is a modest (<~ few) correction to the MPV log-bracket.
_STERN = dict(x0=0.3376, x1=3.6096, a=0.07188, m=3.3306, cbar=5.3299, d0=0.14)
_LAM_MODE = -0.22278  # mode of the standard Landau density phi(lambda)


# --------------------------------------------------------------------------- #
# Kinematics and Landau-Vavilov MPV / width                                   #
# --------------------------------------------------------------------------- #
def beta_gamma(e_mu_gev: np.ndarray) -> np.ndarray:
    """beta*gamma from the muon TOTAL energy E_mu [GeV]."""
    g = np.asarray(e_mu_gev, dtype=float) * 1000.0 / M_MU  # gamma = E/m
    g = np.maximum(g, 1.0 + 1e-9)
    return np.sqrt(g * g - 1.0)


def density_effect(bg: np.ndarray) -> np.ndarray:
    """Sternheimer density-effect correction delta(beta*gamma) for Ge."""
    p = _STERN
    x = np.log10(np.asarray(bg, dtype=float))
    # clip (x1 - x) to >= 0 so the fractional power is never evaluated on a
    # negative base (that branch is only selected for x0 <= x < x1 anyway).
    x1_minus = np.clip(p["x1"] - x, 0.0, None)
    d = np.where(
        x >= p["x1"],
        2.0 * np.log(10.0) * x - p["cbar"],
        np.where(
            x >= p["x0"],
            2.0 * np.log(10.0) * x - p["cbar"] + p["a"] * x1_minus ** p["m"],
            p["d0"] * 10.0 ** (2.0 * (x - p["x0"])),
        ),
    )
    return np.clip(d, 0.0, None)


def t_max(bg: np.ndarray) -> np.ndarray:
    """Max single-collision energy transfer T_max [MeV] (PDG)."""
    bg = np.asarray(bg, dtype=float)
    g = np.sqrt(bg * bg + 1.0)
    r = M_E / M_MU
    return 2.0 * M_E * bg * bg / (1.0 + 2.0 * g * r + r * r)


def xi_width(x_gcm2: np.ndarray, beta2: np.ndarray) -> np.ndarray:
    """Landau width xi = (K/2)(Z/A)(x/beta^2) [MeV], x = rho*ell in g/cm^2."""
    return 0.5 * K_MEV * Z_OVER_A_GE * np.asarray(x_gcm2, dtype=float) / beta2


def mpv_deposit(x_gcm2: np.ndarray, bg: np.ndarray):
    """Most-probable energy loss Delta_p [MeV] and width xi [MeV] (PDG formula).

    Delta_p = xi[ ln(2 m_e c^2 beta^2 gamma^2 / I) + ln(xi/I) + j - beta^2 - delta ].
    """
    bg = np.asarray(bg, dtype=float)
    g2 = bg * bg + 1.0
    beta2 = (bg * bg) / g2
    xi = xi_width(x_gcm2, beta2)
    delta = density_effect(bg)
    dp = xi * (
        np.log(2.0 * M_E * bg * bg / I_GE)
        + np.log(xi / I_GE)
        + J_LANDAU
        - beta2
        - delta
    )
    return dp, xi


def kappa(x_gcm2: np.ndarray, bg: np.ndarray) -> np.ndarray:
    """Vavilov regime parameter kappa = xi / T_max (Landau <~0.01, Gaussian >~10)."""
    bg = np.asarray(bg, dtype=float)
    beta2 = (bg * bg) / (bg * bg + 1.0)
    return xi_width(x_gcm2, beta2) / t_max(bg)


# --------------------------------------------------------------------------- #
# Custom Landau sampler: numerical inverse-CDF of the standard Landau density  #
#   phi(lambda) = (1/pi) int_0^inf exp(-t ln t - lambda t) sin(pi t) dt        #
# built once and cached. Tail phi ~ 1/lambda^2 -> F ~ 1 - c/lambda.            #
# --------------------------------------------------------------------------- #
_LANDAU_TABLE = None


def _phi_landau(lam: float) -> float:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        val, _ = integrate.quad(
            lambda t: np.exp(-t * np.log(t) - lam * t) * np.sin(np.pi * t),
            0.0, 60.0, limit=400,
        )
    return max(val / np.pi, 0.0)


def _build_landau_table():
    global _LANDAU_TABLE
    if _LANDAU_TABLE is not None:
        return _LANDAU_TABLE
    lam_hi = 300.0
    grid = np.concatenate([np.linspace(-4.0, 20.0, 700),
                           np.linspace(20.5, lam_hi, 300)])
    pdf = np.array([_phi_landau(l) for l in grid])
    cdf = np.concatenate([[0.0], integrate.cumulative_trapezoid(pdf, grid)])
    c_tail = lam_hi * (1.0 - cdf[-1])  # match F = 1 - c/lambda beyond the grid
    _LANDAU_TABLE = (grid, cdf, lam_hi, c_tail)
    return _LANDAU_TABLE


def sample_standard_landau(u: np.ndarray) -> np.ndarray:
    """Sample the standard Landau variate lambda (mode -0.22278) from uniforms u."""
    grid, cdf, lam_hi, c_tail = _build_landau_table()
    lam = np.interp(u, cdf, grid)
    hi = u > cdf[-1]
    lam = np.where(hi, c_tail / np.clip(1.0 - u, 1e-12, None), lam)
    return lam


def sample_deposit(x_gcm2: np.ndarray, bg: np.ndarray, rng: np.random.Generator):
    """Sample the per-chord energy deposit [MeV] from Landau-Vavilov straggling.

    Landau/mild-Vavilov (kappa < 10): deposit = Delta_p + xi*(lambda - lambda_mode)
    with lambda ~ standard Landau, so the mode sits exactly at Delta_p.
    Gaussian (kappa >= 10): deposit ~ Normal(mean, sqrt(xi*T_max*(1-beta^2/2))).
    Each deposit is capped at the muon kinetic energy (energy conservation).
    """
    x_gcm2 = np.asarray(x_gcm2, dtype=float)
    bg = np.asarray(bg, dtype=float)
    n = x_gcm2.shape[0]
    dp, xi = mpv_deposit(x_gcm2, bg)
    kap = kappa(x_gcm2, bg)

    u = rng.random(n)
    lam = sample_standard_landau(u)
    dep = dp + xi * (lam - _LAM_MODE)

    # Gaussian (thick-absorber) branch for the rare kappa >= 10 chords.
    gauss = kap >= 10.0
    if np.any(gauss):
        beta2 = (bg * bg) / (bg * bg + 1.0)
        mean = DEDX_MEAN * x_gcm2
        sigma = np.sqrt(np.clip(xi * t_max(bg) * (1.0 - beta2 / 2.0), 0.0, None))
        dep_g = rng.normal(mean, sigma)
        dep = np.where(gauss, dep_g, dep)

    # Physical bounds: 0 < deposit <= muon kinetic energy.
    e_kin_mev = (bg * bg + 1.0) ** 0.5 * M_MU - M_MU
    dep = np.clip(dep, 0.0, e_kin_mev)
    return dep


# --------------------------------------------------------------------------- #
# Shared logarithmic deposited-energy grid (identical to the Compton plan)     #
# --------------------------------------------------------------------------- #
def shared_energy_grid(e_lo_kev: float = 1.0e-2, e_hi_kev: float = 2.0e5,
                       bins_per_decade: int = 80):
    """Log E_dep grid edges [keV]: 0.01 keV -> 200 MeV, ~80 bins/decade."""
    n_dec = np.log10(e_hi_kev / e_lo_kev)
    nbins = int(round(n_dec * bins_per_decade))
    return np.logspace(np.log10(e_lo_kev), np.log10(e_hi_kev), nbins + 1)


# --------------------------------------------------------------------------- #
# Full Monte-Carlo assembly of dR/dE_dep                                       #
# --------------------------------------------------------------------------- #
@dataclass
class MuonSpectrum:
    edges_kev: np.ndarray      # (Nb+1,) bin edges [keV]
    centers_kev: np.ndarray    # (Nb,) log-bin centers [keV]
    dRdE: np.ndarray           # (Nb,) counts / kg / day / keV
    dRdE_err: np.ndarray       # (Nb,) MC statistical error, same units
    rate_hz: float             # integral muon rate through the wafer [Hz]
    rate_err_hz: float         # MC error on the rate [Hz]
    vertical_mpv_mev: float    # sampled MPV for near-vertical chords [MeV]
    vertical_mean_mev: float   # mean deposit for the vertical chord [MeV]
    n_samples: int


def run_muon_mc(n_samples: int = 2_000_000, seed: int = 20260720,
                e_min_gev: float = 0.2, e_max_gev: float = 1.0e5) -> MuonSpectrum:
    """Fold Gaisser-Guan flux (x) ray-box chord (x) Landau-Vavilov MPV deposit
    into the muon dR/dE_dep on the shared grid [counts/kg/day/keV].

    Importance-sampling measure:
      integrand of R = int I(E,theta) A_proj(Omega) sin(theta) dtheta dphi dE
      proposal q = q(theta) q(phi) q(E), q(theta)=2/pi (uniform in [0,pi/2],
      oversamples the horizon), q(phi)=1/2pi, q(E) ~ E^{-2.7}.
      weight W_i = I A_proj sin(theta) / q  -> R = mean(W_i) [Hz].
    Each muon deposits D_i(ell_i) [MeV]; the W_i-weighted histogram is dR/dE_dep.
    """
    rng = np.random.default_rng(seed)

    # --- sample (theta, phi, E) from the proposal ------------------------- #
    theta = rng.uniform(0.0, np.pi / 2.0, n_samples)  # q_theta = 2/pi
    phi = rng.uniform(0.0, 2.0 * np.pi, n_samples)     # q_phi = 1/2pi
    E, pdfE = muon_flux.sample_energy(n_samples, rng, e_min_gev, e_max_gev)

    cth = np.cos(theta)
    sth = np.sin(theta)
    directions = wafer_geometry.direction_from_angles(theta, phi)

    intensity = muon_flux.dI_dE(E, cth)            # cm^-2 s^-1 sr^-1 GeV^-1
    a_proj = wafer_geometry.projected_area(directions)  # cm^2

    q = (2.0 / np.pi) * (1.0 / (2.0 * np.pi)) * pdfE
    weight = intensity * a_proj * sth / q          # Hz per sample

    # --- chord and deposit ------------------------------------------------- #
    ell = wafer_geometry.sample_entry_and_chord(directions, rng)  # cm
    x_gcm2 = RHO * ell
    bg = beta_gamma(E)
    dep_mev = sample_deposit(x_gcm2, bg, rng)      # MeV

    valid = (ell > 0) & (dep_mev > 0) & np.isfinite(weight)
    weight = weight[valid]
    dep_kev = dep_mev[valid] * 1.0e3
    theta_v = theta[valid]
    ell_v = ell[valid]

    # --- integral rate ----------------------------------------------------- #
    rate_hz = float(weight.sum() / n_samples)
    rate_err_hz = float(np.sqrt((weight ** 2).sum()) / n_samples)

    # --- histogram -> dR/dE_dep [counts/kg/day/keV] ----------------------- #
    edges = shared_energy_grid()
    centers = np.sqrt(edges[:-1] * edges[1:])
    dwidth = np.diff(edges)
    per_sample = 86400.0 / (n_samples * wafer_geometry.MASS_KG)  # Hz -> cts/kg/day

    sumw, _ = np.histogram(dep_kev, bins=edges, weights=weight)
    sumw2, _ = np.histogram(dep_kev, bins=edges, weights=weight ** 2)
    dRdE = sumw * per_sample / dwidth
    dRdE_err = np.sqrt(sumw2) * per_sample / dwidth

    # --- near-vertical MPV (theta < 5 deg -> chord ~ 0.20 cm) -------------- #
    near_vert = theta_v < np.deg2rad(5.0)
    if np.count_nonzero(near_vert) > 1000:
        dv = dep_kev[near_vert] / 1.0e3  # MeV
        # Fine histogram over the peak region + light smoothing for a stable mode.
        hist, be = np.histogram(dv, bins=400, range=(0.3, 2.5))
        bc = 0.5 * (be[1:] + be[:-1])
        kernel = np.ones(7) / 7.0
        smooth = np.convolve(hist, kernel, mode="same")
        vertical_mpv = float(bc[np.argmax(smooth)])
    else:
        vertical_mpv = float("nan")
    vertical_mean = DEDX_MEAN * RHO * wafer_geometry.CHORD_VERTICAL  # 1.46 MeV

    return MuonSpectrum(
        edges_kev=edges,
        centers_kev=centers,
        dRdE=dRdE,
        dRdE_err=dRdE_err,
        rate_hz=rate_hz,
        rate_err_hz=rate_err_hz,
        vertical_mpv_mev=vertical_mpv,
        vertical_mean_mev=vertical_mean,
        n_samples=n_samples,
    )


def write_csv(spec: MuonSpectrum, path: str) -> None:
    """Write dR/dE_dep to CSV: E_dep_keV, dRdEdep_cts_per_kg_day_keV, mc_err."""
    import csv

    header_lines = [
        "# Muon deposited-energy spectrum dR/dE_dep for the 4in x 4in x 2mm Ge wafer",
        "# Plan 04-01 (CALC-03/VALD-02). Gaisser-Guan flux (x) ray-box chord (x)",
        "# Landau-Vavilov MPV deposit. UNIFIED PHONON SCALE, NO quenching (CONVENTIONS B).",
        f"# integral_muon_rate_Hz = {spec.rate_hz:.4f} +/- {spec.rate_err_hz:.4f}",
        f"# vertical_chord_MPV_MeV = {spec.vertical_mpv_mev:.4f} "
        f"(mean = {spec.vertical_mean_mev:.4f}; MPV < mean by construction)",
        f"# n_mc_samples = {spec.n_samples}; seed fixed for reproducibility",
        "# units: E_dep_keV [keV]; dRdEdep [counts/kg/day/keV]; mc_err [counts/kg/day/keV]",
        "# grid: shared log E_dep, 0.01 keV -> 2e5 keV (200 MeV), ~80 bins/decade",
    ]
    with open(path, "w", newline="") as f:
        for line in header_lines:
            f.write(line + "\n")
        w = csv.writer(f)
        w.writerow(["E_dep_keV", "dRdEdep_cts_per_kg_day_keV", "mc_err"])
        for c, y, e in zip(spec.centers_kev, spec.dRdE, spec.dRdE_err):
            w.writerow([f"{c:.6e}", f"{y:.6e}", f"{e:.6e}"])
