# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
#
# Environmental-gamma Compton SOURCE for the Phase-4 thin-Ge-wafer channel
# (Plan 04-02, CALC-04 / VALD-03).
#
# This module owns the sourced, provenance-tagged inputs of the Compton channel:
#   * the radiogenic gamma line list (energies = nuclear data; intensities/flux =
#     sourced tunable input) loaded from data/gamma_lines.csv,
#   * the frozen NIST XCOM Ge mu/rho table (data/ge_xcom_mu.csv) with log-log
#     interpolation, and
#   * the thin-target SINGLE-SCATTER bookkeeping (interaction probability, double-
#     scatter estimate, rate path length) on ONE pinned path length: the Cauchy
#     mean chord ell_bar = 4V/S = 0.385 cm (physically correct for an ~isotropic
#     environmental gamma flux). The SAME ell_bar is used in P, in the double-
#     scatter estimate, and in the VALD-03 rate normalization.
#
# ENERGY SCALE: the deposit (built in compton_deposit.py) is the Compton ELECTRON
# recoil T_e on the unified phonon E_dep scale, NO quenching (CONVENTIONS Section
# B). Guards fp-quenching-compton, fp-electron-not-photon, fp-full-absorption.
#
# The 0.2 cm normal-incidence optical depth mu*t (t = wafer thickness) is provided
# ONLY as a labelled "optically thin" demonstration -- it is NOT the rate path
# length (that is ell_bar).

from __future__ import annotations

import csv
import os
from dataclasses import dataclass

import numpy as np

from . import wafer_geometry

# --------------------------------------------------------------------------- #
# Data locations                                                              #
# --------------------------------------------------------------------------- #
_DATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data")
)
GAMMA_LINES_CSV = os.path.join(_DATA_DIR, "gamma_lines.csv")
GE_XCOM_CSV = os.path.join(_DATA_DIR, "ge_xcom_mu.csv")

# --------------------------------------------------------------------------- #
# Physical constants                                                          #
# --------------------------------------------------------------------------- #
M_E_KEV = 510.99895     # electron rest energy m_e c^2 [keV] (CODATA; matches params)
R_E_CM = 2.8179403262e-13   # classical electron radius [cm] (CODATA)

# Wafer geometry / mass reused (NOT re-invented) from wafer_geometry / params.
RHO = wafer_geometry.RHO                 # 5.323 g/cm^3
MASS_KG = wafer_geometry.MASS_KG         # 0.1099 kg
V_GEOM = wafer_geometry.V_GEOM           # ~20.645 cm^3
S_SURFACE = wafer_geometry.S_SURFACE     # ~214.6 cm^2
THICKNESS_CM = wafer_geometry.LZ         # 0.20 cm (2 mm) -- normal-incidence demo only

# ONE pinned path length for the whole channel (Cauchy mean chord, isotropic flux).
ELL_BAR_CM = wafer_geometry.cauchy_mean_chord()   # 4V/S = 0.385 cm

# Ge electron content for the flux x cross-section x N_e rate cross-check.
Z_GE = 32
GE_ATOMS_PER_KG = 8.29e24                # CONVENTIONS Section D (params.GE_ATOMS_PER_KG)
N_E_WAFER = Z_GE * GE_ATOMS_PER_KG * MASS_KG   # total electrons in the wafer


# --------------------------------------------------------------------------- #
# Gamma line list (sourced, provenance-tagged)                                #
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class GammaLine:
    energy_keV: float
    isotope: str
    chain: str
    p_gamma: float
    p_gamma_source: str
    flux_cm2_s: float
    flux_unc_frac: float
    flux_source: str


def load_gamma_lines(path: str = GAMMA_LINES_CSV) -> list[GammaLine]:
    """Load the provenance-tagged radiogenic gamma line list from the frozen CSV."""
    lines: list[GammaLine] = []
    with open(path, newline="") as f:
        reader = csv.DictReader(row for row in f if not row.startswith("#"))
        for r in reader:
            lines.append(
                GammaLine(
                    energy_keV=float(r["energy_keV"]),
                    isotope=r["isotope"],
                    chain=r["chain"],
                    p_gamma=float(r["p_gamma"]),
                    p_gamma_source=r["p_gamma_source"],
                    flux_cm2_s=float(r["flux_cm2_s"]),
                    flux_unc_frac=float(r["flux_unc_frac"]),
                    flux_source=r["flux_source"],
                )
            )
    return lines


# --------------------------------------------------------------------------- #
# NIST XCOM Ge mu/rho: frozen table + log-log interpolation                    #
# --------------------------------------------------------------------------- #
def load_xcom(path: str = GE_XCOM_CSV):
    """Load the frozen NIST XCOM Ge mu/rho table -> (E_MeV, mu_over_rho) arrays."""
    e, mor = [], []
    with open(path, newline="") as f:
        reader = csv.DictReader(row for row in f if not row.startswith("#"))
        for r in reader:
            e.append(float(r["energy_MeV"]))
            mor.append(float(r["mu_over_rho_cm2_g"]))
    return np.asarray(e), np.asarray(mor)


_XCOM_E, _XCOM_MOR = load_xcom()
_LOG_E = np.log(_XCOM_E)
_LOG_MOR = np.log(_XCOM_MOR)


def mu_over_rho(e_kev):
    """NIST XCOM Ge mu/rho [cm^2/g] at photon energy e_kev [keV].

    Log-log interpolation between the four frozen NIST points; log-log LINEAR
    extrapolation (mild) outside [0.6, 2.0] MeV using the nearest interval slope.
    Documented in data/ge_xcom_mu.csv -- not additional data.
    """
    e_mev = np.atleast_1d(np.asarray(e_kev, dtype=float)) / 1.0e3
    lx = np.log(e_mev)
    # np.interp clamps at the ends; replace clamped regions with slope extrapolation.
    ly = np.interp(lx, _LOG_E, _LOG_MOR)
    slope_lo = (_LOG_MOR[1] - _LOG_MOR[0]) / (_LOG_E[1] - _LOG_E[0])
    slope_hi = (_LOG_MOR[-1] - _LOG_MOR[-2]) / (_LOG_E[-1] - _LOG_E[-2])
    below = lx < _LOG_E[0]
    above = lx > _LOG_E[-1]
    ly = np.where(below, _LOG_MOR[0] + slope_lo * (lx - _LOG_E[0]), ly)
    ly = np.where(above, _LOG_MOR[-1] + slope_hi * (lx - _LOG_E[-1]), ly)
    out = np.exp(ly)
    return out if out.size > 1 else float(out[0])


def mu_linear(e_kev):
    """Linear attenuation coefficient mu = (mu/rho) * rho [cm^-1]."""
    return np.asarray(mu_over_rho(e_kev)) * RHO


# --------------------------------------------------------------------------- #
# Thin-target single-scatter bookkeeping (ONE pinned path length ell_bar)      #
# --------------------------------------------------------------------------- #
def interaction_prob(e_kev, ell_cm: float = ELL_BAR_CM):
    """Single-crossing interaction probability P = 1 - exp(-mu(E) * ell_bar).

    Uses the pinned Cauchy mean chord ell_bar = 4V/S by default (isotropic flux).
    """
    mu = mu_linear(e_kev)
    return 1.0 - np.exp(-mu * ell_cm)


def optical_depth_mean_chord(e_kev):
    """mu * ell_bar on the pinned mean chord (~0.117 @1 MeV, ~0.084 @2 MeV)."""
    return mu_linear(e_kev) * ELL_BAR_CM


def double_scatter_fraction(e_kev):
    """Double-scatter estimate ~ (mu * ell_bar)^2 (single-scatter dominance if <<1)."""
    return optical_depth_mean_chord(e_kev) ** 2


def optical_depth_normal_incidence(e_kev):
    """LABELLED DEMONSTRATION ONLY: mu * t at normal incidence (t = 0.20 cm).

    ~0.06 at 1 MeV -- shows the wafer is optically thin. This is NOT the rate
    path length; the rate/interaction bookkeeping uses ell_bar = 4V/S instead.
    """
    return mu_linear(e_kev) * THICKNESS_CM


# --------------------------------------------------------------------------- #
# Klein-Nishina kinematics + total cross section (per free electron)           #
# --------------------------------------------------------------------------- #
def compton_edge_kev(e_gamma_kev):
    """Compton edge (max electron recoil) E_edge = 2E^2/(m_e c^2 + 2E) [keV]."""
    e = np.asarray(e_gamma_kev, dtype=float)
    return 2.0 * e * e / (M_E_KEV + 2.0 * e)


def sigma_kn(e_gamma_kev):
    """Total Klein-Nishina cross section per electron [cm^2].

    sigma_KN = 2 pi r_e^2 { (1+a)/a^2 [2(1+a)/(1+2a) - ln(1+2a)/a]
                            + ln(1+2a)/(2a) - (1+3a)/(1+2a)^2 },  a = E/m_e c^2.
    Thomson limit sigma_KN(a->0) -> 8 pi r_e^2 / 3 (verified in tests).
    """
    a = np.asarray(e_gamma_kev, dtype=float) / M_E_KEV
    t1 = (1.0 + a) / a**2 * (2.0 * (1.0 + a) / (1.0 + 2.0 * a) - np.log(1.0 + 2.0 * a) / a)
    t2 = np.log(1.0 + 2.0 * a) / (2.0 * a)
    t3 = (1.0 + 3.0 * a) / (1.0 + 2.0 * a) ** 2
    return 2.0 * np.pi * R_E_CM**2 * (t1 + t2 - t3)


SIGMA_THOMSON = 8.0 * np.pi * R_E_CM**2 / 3.0   # 6.6524e-25 cm^2
