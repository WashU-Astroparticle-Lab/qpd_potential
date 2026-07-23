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
from . import interp_guard as ig

# --------------------------------------------------------------------------- #
# Data locations                                                              #
# --------------------------------------------------------------------------- #
_DATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data")
)
GAMMA_LINES_CSV = os.path.join(_DATA_DIR, "gamma_lines.csv")
GE_XCOM_CSV = os.path.join(_DATA_DIR, "ge_xcom_mu.csv")
GE_SF_CSV = os.path.join(_DATA_DIR, "ge_incoherent_S.csv")

# hc in keV.Angstrom (photon wavelength lambda[A] = HC_KEV_ANG / E_gamma[keV]).
HC_KEV_ANG = 12.39842

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

# Plan 10-01 declared evaluation domain, in keV (the units of mu_over_rho's OWN
# abscissa; the frozen table's abscissa is MeV and is converted explicitly).
#
# THIS DOMAIN IS WIDER THAN THE TABLE ON BOTH SIDES, WITH TWO NAMED WITNESSES:
#   below the 600 keV table floor : the Pb-214 241.997 keV line in
#       data/gamma_lines.csv, the lowest-energy line the v1.0 Compton channel
#       folds; the frozen mild slope extrapolation gives mu/rho = 0.11879 cm^2/g
#       there, and tests/test_compton_source.py::
#       test_xcom_extrapolation_monotone_and_reasonable already asserts ~0.107
#       at 295 keV, i.e. an existing v1.0 anchor sits inside this extension.
#   above the 2000 keV table ceiling : the Tl-208 2614.511 keV line, the highest
#       line in the same table; mu/rho = 0.036065 cm^2/g there, and the same
#       v1.0 test asserts 0.034 < mu/rho < 0.038 at 2614.5 keV.
#
# The declared bounds 200 / 3000 keV bracket those two witnesses with a small
# margin and stop at 200 keV because BELOW ~200 keV photoabsorption in Ge
# (Z = 32) turns up steeply and a log-log linear continuation of the
# Compton-dominated 0.6-2.0 MeV interval would be badly wrong, not mildly so.
# This is an EXTRAPOLATION made explicit -- the guard makes it visible, it does
# not make it validated.
XCOM_DOMAIN = ig.register_domain(ig.Domain(
    quantity="Ge mu/rho (NIST XCOM)",
    lo=200.0, hi=3000.0, units="keV",
    table=GE_XCOM_CSV,
    table_lo=float(_XCOM_E[0]) * 1.0e3, table_hi=float(_XCOM_E[-1]) * 1.0e3,
    witness_lo="Pb-214 241.997 keV line (data/gamma_lines.csv); "
               "tests/test_compton_source.py::test_xcom_extrapolation_monotone_and_reasonable "
               "evaluates 295.0 keV",
    witness_hi="Tl-208 2614.511 keV line (data/gamma_lines.csv); the same v1.0 test "
               "asserts 0.034 < mu/rho(2614.5 keV) < 0.038",
    note="Deliberate log-log slope extrapolation outside the four frozen NIST points.",
))


def mu_over_rho(e_kev):
    """NIST XCOM Ge mu/rho [cm^2/g] at photon energy e_kev [keV].

    Log-log interpolation between the four frozen NIST points; log-log LINEAR
    extrapolation (mild) outside [0.6, 2.0] MeV using the nearest interval slope.
    Documented in data/ge_xcom_mu.csv -- not additional data.

    Plan 10-01: raises ``InterpolationDomainError`` outside ``XCOM_DOMAIN``
    (200-3000 keV). Previously the slope extrapolation ran to arbitrarily low
    energy, so a call at, say, 10 keV would silently return a Compton-regime
    mu/rho where Ge is in fact photoabsorption-dominated.
    """
    ig.check_domain(e_kev, XCOM_DOMAIN)
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
# Incoherent (Compton) scattering function S(x,Z): frozen Hubbell (1975) table  #
# + log-log interpolation. Binds the low-recoil Compton continuum.             #
# --------------------------------------------------------------------------- #
def load_incoherent_sf(path: str = GE_SF_CSV):
    """Load the frozen Ge incoherent scattering function -> (x, S) arrays.

    x is the momentum-transfer variable [Angstrom^-1]; S(x,Z=32) is the Hubbell
    (1975) incoherent scattering function (provenance in data/ge_incoherent_S.csv).
    """
    x, s = [], []
    with open(path, newline="") as f:
        reader = csv.DictReader(row for row in f if not row.startswith("#"))
        for r in reader:
            x.append(float(r["x_inv_angstrom"]))
            s.append(float(r["S_incoherent"]))
    return np.asarray(x), np.asarray(s)


_SF_X, _SF_S = load_incoherent_sf()
_LOG_SF_X = np.log(_SF_X)
_LOG_SF_S = np.log(_SF_S)
# Low-x log-log slope (S ~ x^p, physically p ~ 2 -> S -> 0 as x -> 0).
_SF_SLOPE_LO = (_LOG_SF_S[1] - _LOG_SF_S[0]) / (_LOG_SF_X[1] - _LOG_SF_X[0])

# Plan 10-01 declared evaluation domain for S(x, Z=32), in the dimensionless
# momentum-transfer variable x [Angstrom^-1].
#
# THIS DOMAIN IS UNBOUNDED ON BOTH SIDES, AND THAT IS AN HONEST OUTCOME RATHER
# THAN A CONVENIENT ONE. Both extensions carry witnesses:
#   below the 1.0e-3 table floor : EXACT FORWARD SCATTER gives x = 0 identically
#       (momentum_transfer_x(E, cos=1) == 0; tests/test_compton_source.py::
#       test_momentum_transfer_x asserts exactly that), and compton_deposit
#       evaluates S at every angular grid point including the forward one. No
#       positive floor could be declared without breaking the v1.0 Compton
#       channel, so the declared floor is 0.
#   above the 4.2646e4 table ceiling : tests/test_compton_source.py::
#       test_incoherent_S_limits evaluates x = 1e6, and there S(x) = Z = 32
#       EXACTLY by physics (electrons act free), so the "clamp" above the table
#       is the exact asymptote, not a truncation artefact.
#
# CONSEQUENCE, STATED PLAINLY: the bounds guard on this site is VACUOUS for all
# non-negative finite x. What it does catch is a NEGATIVE momentum transfer,
# which the pre-guard code silently mapped to x = 1e-300 via np.maximum and
# returned S = 0.0 for. That is the only silent failure this site actually had.
SF_DOMAIN = ig.register_domain(ig.Domain(
    quantity="Ge incoherent scattering function S(x, Z=32) (Hubbell 1975)",
    lo=0.0, hi=float("inf"), units="dimensionless x [1/Angstrom]",
    table=GE_SF_CSV,
    table_lo=float(_SF_X[0]), table_hi=float(_SF_X[-1]),
    witness_lo="exact forward scatter x = 0 (momentum_transfer_x(E, cos_theta=1)); "
               "tests/test_compton_source.py::test_incoherent_S_limits evaluates 1e-5",
    witness_hi="tests/test_compton_source.py::test_incoherent_S_limits evaluates x = 1e6, "
               "where S = Z = 32 exactly (free-electron asymptote)",
    note="Bounds guard is vacuous for all finite x >= 0 by construction; it catches "
         "negative x, which was previously clamped to 1e-300 and returned S = 0.",
))


def incoherent_S(x_inv_ang):
    """Incoherent scattering function S(x, Z=32) at momentum transfer x [A^-1].

    Log-log interpolation between the frozen Hubbell (1975) points. Below the
    tabulated x_min, log-log LINEAR extrapolation with the first-interval slope
    (S ~ x^2 -> 0, forward/low-recoil binding suppression); above x_max, clamp to
    S = Z = 32 (large recoil -> electrons act free, edges/bulk unchanged).

    Plan 10-01: raises ``InterpolationDomainError`` for negative or non-finite x
    (see ``SF_DOMAIN``). A negative momentum transfer is unphysical and was
    previously mapped silently to x = 1e-300, returning S = 0.0.
    """
    ig.check_domain(x_inv_ang, SF_DOMAIN)
    x = np.atleast_1d(np.asarray(x_inv_ang, dtype=float))
    lx = np.log(np.maximum(x, 1e-300))
    ly = np.interp(lx, _LOG_SF_X, _LOG_SF_S)          # np.interp clamps at ends
    below = lx < _LOG_SF_X[0]
    ly = np.where(below, _LOG_SF_S[0] + _SF_SLOPE_LO * (lx - _LOG_SF_X[0]), ly)
    # above x_max np.interp already clamps to _LOG_SF_S[-1] = ln(Z) -> S = Z.
    out = np.exp(ly)
    return out if out.size > 1 else float(out[0])


def momentum_transfer_x(e_gamma_kev, cos_theta):
    """Momentum-transfer variable x = E_gamma[keV]*sin(theta/2)/12.39842 [A^-1].

    sin(theta/2) = sqrt((1 - cos theta)/2). Forward scatter (cos->1) -> x->0
    (bound, suppressed); backscatter (cos->-1, the Compton edge) -> x maximal
    (free, S->Z).
    """
    e = np.asarray(e_gamma_kev, dtype=float)
    c = np.asarray(cos_theta, dtype=float)
    sin_half = np.sqrt(np.maximum(1.0 - c, 0.0) / 2.0)
    return e * sin_half / HC_KEV_ANG


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
