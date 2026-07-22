# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
#
# Closed-form CEvNS total cross-section BENCHMARK HOOK for Phase 3.
#
# CONVENTIONS Section C (LOCKED):
#   Q_W       = N - (1 - 4 sin^2 theta_W) Z
#   sigma_tot = G_F^2 * Q_W^2 * E_nu^2 / (4 pi) * (hbar c)^2
#
# The /(4 pi) prefactor (NOT /8 pi) and the (hbar c)^2 = 3.894e-28 GeV^2*cm^2
# conversion are BOTH mandatory. Dropping (hbar c)^2 leaves sigma ~1e28x too
# large (in GeV^-2); using /8 pi is a factor-of-2 error. Both are forbidden
# proxies (fp-prefactor).
#
# SCOPE: this is the total, mass-independent closed form used only as the
# Phase-3 benchmark anchor. The differential dsigma/dT, the Helm form factor,
# and reactor-flux folding are Phase 3, NOT here.

from __future__ import annotations

import math
import os

import numpy as np
from scipy.integrate import quad
from scipy.interpolate import PchipInterpolator
from scipy.special import spherical_jn

from . import params

# Bare numeric values pulled once from the provenance-tagged registry.
_G_F = params.G_F.value                              # GeV^-2
_ONE_MINUS_4SIN2 = params.ONE_MINUS_4SIN2THETAW.value  # dimensionless (= 1 - 4 sin^2 theta_W)
_HBARC2 = params.HBARC2.value                        # GeV^2 * cm^2
_PREFACTOR_DENOM = params.CEVNS_PREFACTOR_DENOM.value  # 4 * pi
_GE_ATOMS_PER_KG = params.GE_ATOMS_PER_KG.value      # atoms/kg
_GE_ISOTOPES = params.GE_ISOTOPES                    # 5-isotope natural-Ge table

_MEV_PER_GEV = 1.0e-3  # 1 MeV = 1e-3 GeV
_KEV_PER_GEV = 1.0e6   # 1 GeV = 1e6 keV
_MEV_PER_KEV = 1.0e-3  # 1 keV = 1e-3 MeV
_SECONDS_PER_DAY = 86400.0

# Helm parameters (Lewin-Smith).
_HELM_A = params.HELM_A_FM
_HELM_S = params.HELM_S_FM
_HBARC_MEV_FM = params.HBAR_C_MEV_FM

# Default frozen Phase-2 flagship flux.
_DEFAULT_FLUX_CSV = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "flux", "reactor_flux_v1.0.csv"
)


def weak_charge(Z: int, N: int) -> float:
    """Standard-Model weak nuclear charge Q_W = N - (1 - 4 sin^2 theta_W) Z.

    Dimensionless. The proton coupling (1 - 4 sin^2 theta_W) = 0.0452 nearly
    vanishes, so Q_W ~ N and the rate scales as N^2 to ~0.5%.
    """
    return N - _ONE_MINUS_4SIN2 * Z


def sigma_tot(E_nu_GeV: float, Z: int, N: int) -> float:
    """Total CEvNS cross section in cm^2 (closed form, E_nu in GeV).

    sigma_tot = G_F^2 * Q_W^2 * E_nu^2 / (4 pi) * (hbar c)^2

    [G_F^2] = GeV^-4, [E_nu^2] = GeV^2  ->  bracket is GeV^-2;
    * (hbar c)^2 [GeV^2*cm^2]           ->  cm^2.
    """
    Q_W = weak_charge(Z, N)
    sigma_GeV_inv2 = _G_F**2 * Q_W**2 * E_nu_GeV**2 / _PREFACTOR_DENOM  # GeV^-2
    return sigma_GeV_inv2 * _HBARC2  # -> cm^2


def sigma_tot_MeV(E_nu_MeV: float, Z: int, N: int) -> float:
    """Convenience wrapper: total CEvNS cross section in cm^2, E_nu in MeV."""
    return sigma_tot(E_nu_MeV * _MEV_PER_GEV, Z, N)


# =========================================================================== #
# Phase 3, Plan 03-01: Helm form factor, per-isotope dsigma/dT, flux fold      #
# =========================================================================== #
#
# Differential (CONVENTIONS Section C, LOCKED):
#   dsigma/dT = (G_F^2 M / 4pi) Q_W^2 (1 - M T / (2 E_nu^2)) F^2(q) * (hbar c)^2
# with /4pi (NOT /8pi), Q_W = N - (1 - 4 sin^2 theta_W) Z, and F the Helm form
# factor with F(0) = 1. The 73Ge spin-dependent / axial term is ~1/N^2 suppressed
# relative to the coherent N^2 term and is NOT modeled here (stated assumption).


def helm_form_factor(q_fm_inv: float, A: int) -> float:
    """Lewin-Smith Helm nuclear form factor F(q) (dimensionless, F(0) = 1).

    F(q) = 3 j1(q R_0) / (q R_0) * exp(-(q s)^2 / 2),
    R_0^2 = c^2 + (7/3) pi^2 a^2 - 5 s^2, c = 1.23 A^{1/3} - 0.60 fm,
    a = 0.52 fm, s = 0.90 fm.

    q_fm_inv must be the momentum transfer in fm^-1 (NOT MeV). Feeding a
    MeV-valued q here would produce a huge spurious suppression -- build q with
    momentum_transfer_fm_inv().
    """
    c = 1.23 * A ** (1.0 / 3.0) - 0.60
    R0 = math.sqrt(c**2 + (7.0 / 3.0) * math.pi**2 * _HELM_A**2 - 5.0 * _HELM_S**2)
    x = q_fm_inv * R0
    if x < 1e-8:
        # lim_{x->0} 3 j1(x)/x = 1 exactly (F(0) = 1).
        shape = 1.0
    else:
        shape = 3.0 * spherical_jn(1, x) / x
    return shape * math.exp(-((q_fm_inv * _HELM_S) ** 2) / 2.0)


def momentum_transfer_fm_inv(T_keV: float, M_MeV: float) -> float:
    """Momentum transfer q = sqrt(2 M T) converted to fm^-1.

    q[MeV] = sqrt(2 * M[MeV] * T[MeV]); q[fm^-1] = q[MeV] / (hbar c = 197.327 MeV fm).
    """
    T_MeV = T_keV * _MEV_PER_KEV
    q_MeV = math.sqrt(2.0 * M_MeV * T_MeV)
    return q_MeV / _HBARC_MEV_FM


def T_max_keV(E_nu_MeV: float, M_MeV: float) -> float:
    """Maximum nuclear recoil kinetic energy [keV]: T_max = 2 E_nu^2 / (M + 2 E_nu)."""
    T_max_MeV = 2.0 * E_nu_MeV**2 / (M_MeV + 2.0 * E_nu_MeV)
    return T_max_MeV / _MEV_PER_KEV


def E_min_MeV(T_keV: float, M_MeV: float) -> float:
    """Minimum neutrino energy [MeV] able to produce recoil T (exact kinematics).

    Inverting T = 2 E^2 / (M + 2 E): E_min = (T + sqrt(T^2 + 2 M T)) / 2.
    """
    T_MeV = T_keV * _MEV_PER_KEV
    return 0.5 * (T_MeV + math.sqrt(T_MeV**2 + 2.0 * M_MeV * T_MeV))


def dsigma_dT(
    E_nu_MeV: float,
    T_keV: float,
    Z: int,
    N: int,
    M_MeV: float,
    A: int,
    use_form_factor: bool = True,
) -> float:
    """Per-isotope Freedman differential CEvNS cross section dsigma/dT [cm^2/keV].

    dsigma/dT = (G_F^2 M / 4pi) Q_W^2 (1 - M T / (2 E_nu^2)) F^2(q) * (hbar c)^2.

    Internal cross-section arithmetic is in natural GeV units (dsigma/dT is then
    cm^2/GeV after the (hbar c)^2 factor); the *1e-6 converts cm^2/GeV -> cm^2/keV.
    Returns 0 outside the physical window 0 < T <= T_max(E_nu).
    """
    if T_keV <= 0.0:
        return 0.0
    if T_keV > T_max_keV(E_nu_MeV, M_MeV):
        return 0.0

    E_GeV = E_nu_MeV * _MEV_PER_GEV
    T_GeV = T_keV / _KEV_PER_GEV
    M_GeV = M_MeV * _MEV_PER_GEV

    Q_W = weak_charge(Z, N)
    kin = 1.0 - M_GeV * T_GeV / (2.0 * E_GeV**2)
    if kin < 0.0:  # numerical guard at the endpoint
        kin = 0.0

    if use_form_factor:
        q = momentum_transfer_fm_inv(T_keV, M_MeV)
        F2 = helm_form_factor(q, A) ** 2
    else:
        F2 = 1.0

    # cm^2 / GeV
    dsig_per_GeV = _G_F**2 * M_GeV / _PREFACTOR_DENOM * Q_W**2 * kin * F2 * _HBARC2
    return dsig_per_GeV * 1.0e-6  # cm^2 / keV


# --------------------------------------------------------------------------- #
# Frozen-flux loading + PCHIP log interpolation                                #
# --------------------------------------------------------------------------- #


class ReactorFlux:
    """Frozen Phase-2 flagship flux Phi(E_nu) with monotone log interpolation.

    Uses the 'flux_nu_per_cm2_per_s_per_MeV' (total) column and the
    'rel_uncertainty' column. log-flux PCHIP interpolation is monotone and
    guarantees a non-negative, ring-free flux between the ~5 MeV bump and the
    threshold; rel_uncertainty is piecewise so it is linearly interpolated.
    """

    def __init__(
        self,
        csv_path: str = _DEFAULT_FLUX_CSV,
        scale: float = 1.0,
        e_min_cut_MeV: float | None = None,
        rel_col: int = 5,
    ):
        """Load a frozen flux CSV.

        scale         : multiplicative renormalization of Phi (e.g. the Billard
                        k approx 0.0111 geometry+power rescale of the variant flux).
        e_min_cut_MeV : if set, Phi is forced to 0 below this E_nu (the sub-1.8-MeV
                        toggle for the band test); does NOT affect E_min/E_max.
        rel_col       : column index of the fractional flux uncertainty; the
                        Billard-variant CSV has no rel_uncertainty column, so pass
                        rel_col=None to zero it (band is not used for that fold).
        """
        E, phi, rel = [], [], []
        with open(csv_path) as fh:
            for line in fh:
                if line.startswith("#") or line.startswith("E_nu"):
                    continue
                line = line.strip()
                if not line:
                    continue
                cols = line.split(",")
                E.append(float(cols[0]))
                phi.append(float(cols[1]))
                rel.append(0.0 if rel_col is None else float(cols[rel_col]))
        self.E = np.asarray(E)
        self.phi = np.asarray(phi)
        self.rel = np.asarray(rel)
        self.csv_path = csv_path
        self.scale = scale
        self.e_min_cut_MeV = e_min_cut_MeV
        self.E_min = float(self.E.min())
        self.E_max = float(self.E.max())
        if np.any(self.phi <= 0.0):
            raise ValueError("flux total column has non-positive entries; cannot log-interp")
        self._log_phi = PchipInterpolator(self.E, np.log(self.phi), extrapolate=False)

    def flux(self, E_nu_MeV: float) -> float:
        """Phi(E_nu) [nu cm^-2 s^-1 MeV^-1]; 0 outside the grid or below the cut."""
        if E_nu_MeV < self.E_min or E_nu_MeV > self.E_max:
            return 0.0
        if self.e_min_cut_MeV is not None and E_nu_MeV < self.e_min_cut_MeV:
            return 0.0
        return self.scale * float(np.exp(self._log_phi(E_nu_MeV)))

    def rel_uncertainty(self, E_nu_MeV: float) -> float:
        """Fractional flux uncertainty at E_nu (linear interp of the split band)."""
        return float(np.interp(E_nu_MeV, self.E, self.rel))


# --------------------------------------------------------------------------- #
# Per-isotope differential rate dR/dT (deposited nuclear-recoil energy)        #
# --------------------------------------------------------------------------- #


def _fold_isotope(T_keV, iso, flux, use_form_factor, weight_rel=False):
    """Sum_i integrand: N_target,i * int Phi (* rel) * dsigma_i/dT dE_nu.

    Returns counts/kg/day/keV (or the absolute band contribution if weight_rel).
    Integrates on the isotope's own [E_min^(i)(T), E_max] kinematic domain.
    """
    e_lo = max(E_min_MeV(T_keV, iso.M_MeV), flux.E_min)
    e_hi = flux.E_max
    if e_lo >= e_hi:
        return 0.0

    def integrand(E_nu_MeV):
        phi = flux.flux(E_nu_MeV)
        if phi <= 0.0:
            return 0.0
        ds = dsigma_dT(E_nu_MeV, T_keV, iso.Z, iso.N, iso.M_MeV, iso.A, use_form_factor)
        val = phi * ds
        if weight_rel:
            val *= flux.rel_uncertainty(E_nu_MeV)
        return val

    val, _ = quad(integrand, e_lo, e_hi, limit=200)
    N_target = iso.abundance * _GE_ATOMS_PER_KG
    return N_target * val * _SECONDS_PER_DAY  # counts/kg/day/keV


def differential_rate_per_isotope(T_keV, flux, use_form_factor=True):
    """dict name -> dR/dT_i [counts/kg/day/keV] for each natural-Ge isotope."""
    return {
        iso.name: _fold_isotope(T_keV, iso, flux, use_form_factor)
        for iso in _GE_ISOTOPES
    }


def differential_rate(T_keV, flux=None, use_form_factor=True):
    """Total isotope-summed dR/dT [counts/kg/day/keV] at deposited recoil T."""
    if flux is None:
        flux = ReactorFlux()
    return sum(
        _fold_isotope(T_keV, iso, flux, use_form_factor) for iso in _GE_ISOTOPES
    )


def differential_rate_band(T_keV, flux):
    """Absolute 1-sigma flux-uncertainty band on dR/dT [counts/kg/day/keV].

    band(T) = Sum_i N_target,i * int Phi(E) * rel(E) * dsigma_i/dT dE * 86400,
    i.e. the propagated flux rel_uncertainty (folding Phi*(1+rel) minus Phi*1).
    """
    return sum(
        _fold_isotope(T_keV, iso, flux, use_form_factor=True, weight_rel=True)
        for iso in _GE_ISOTOPES
    )


def integrated_rate_direct(flux=None, use_form_factor=False, T_floor_keV=0.0):
    """Direct total rate [counts/kg/day] = Sum_i N_i int Phi sigma_tot,i dE_nu.

    Independent normalization for the differential closure test. With
    use_form_factor=False it uses the closed-form sigma_tot,i (F=1). A T_floor
    (keV) restricts to recoils above a threshold by capping each E_nu below the
    E that can produce T_floor (used only for the >50 eV convergence sanity).
    """
    if flux is None:
        flux = ReactorFlux()
    total = 0.0
    for iso in _GE_ISOTOPES:
        e_lo = flux.E_min
        if T_floor_keV > 0.0:
            e_lo = max(e_lo, E_min_MeV(T_floor_keV, iso.M_MeV))
        if e_lo >= flux.E_max:
            continue

        def integrand(E_nu_MeV, iso=iso):
            phi = flux.flux(E_nu_MeV)
            if phi <= 0.0:
                return 0.0
            return phi * sigma_tot_MeV(E_nu_MeV, iso.Z, iso.N)

        val, _ = quad(integrand, e_lo, flux.E_max, limit=200)
        N_target = iso.abundance * _GE_ATOMS_PER_KG
        total += N_target * val * _SECONDS_PER_DAY
    return total


def recoil_grid_eV(n=300, T_min_eV=5.0, T_max_eV=3200.0):
    """Log-spaced deposited nuclear-recoil energy grid [eV_nr]."""
    return np.logspace(np.log10(T_min_eV), np.log10(T_max_eV), n)


# =========================================================================== #
# Phase 3, Plan 03-02: Billard (2017) Table-1 reproduction (VALD-01)           #
# =========================================================================== #
#
# The frozen billard_variant.csv carries Billard's SPECTRAL SHAPE at OUR
# 3 GW_th / 25 m normalization (int Phi = 4.586e12). Billard's Table 1 is at
# Chooz's 8.54 GW combined thermal power at ~400 m (two cores at 355.39 &
# 468.76 m, 4.27 GW each). Folding the variant AS-STORED overshoots Table 1 by
# ~90x (forbidden proxy fp-billard-norm). It MUST first be renormalized by
#   k = (P_B/P_v) * (G_B/G_v),  G = point-source 1/(4 pi d^2) geometry factor.
# Both powers are THERMAL (GW_th, not GW_e); fp-gwe-gwth.

_BILLARD_VARIANT_CSV = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "flux",
    "reactor_flux_billard_variant.csv",
)

# Billard Table 1 targets: counts/kg/day above 50 / 100 / 200 eV_nr.
BILLARD_TABLE1 = {50.0: 0.76, 100.0: 0.51, 200.0: 0.26}


def billard_k_factor():
    """Derive the Billard geometry+power renormalization k, two ways.

    k = (P_B / P_v) * (G_B / G_v), with G the point-source 1/(4 pi d^2) factor.
    The 4 pi cancels in the ratio; distances only enter as (d_v / d_B)^2, so any
    consistent length unit works. Evaluated as:
      single-source : k = (P_B/P_v) * (d_v / d_B)^2               (8.54 GW at 400 m)
      two-core      : k = [P1/d1^2 + P2/d2^2] / [P_v / d_v^2]     (355.39 & 468.76 m)

    Returns dict with k_single, k_two_core, rel_diff (should be <1%), and the
    k-rescaled Billard integral flux (should be ~5.1e10 nu cm^-2 s^-1).
    """
    P_B = params.BILLARD_POWER_GW.value
    d_B = params.BILLARD_DISTANCE_M.value
    P_v = params.REACTOR_POWER.value      # 3.0 GW_th (our config)
    d_v = params.STANDOFF.value           # 25.0 m (our config)

    k_single = (P_B / P_v) * (d_v / d_B) ** 2

    d1, d2 = params.BILLARD_CORE_DISTANCES_M
    P_core = params.BILLARD_CORE_POWER_GW
    G_two = P_core / d1**2 + P_core / d2**2       # ~ two-core geometry factor
    G_v = P_v / d_v**2
    k_two_core = G_two / G_v

    rel_diff = abs(k_single - k_two_core) / k_two_core

    # Billard-variant stored integral flux at our config (from the CSV header).
    variant_int_flux = 4.5861e12
    return {
        "k_single": k_single,
        "k_two_core": k_two_core,
        "rel_diff": rel_diff,
        "rescaled_integral_flux": k_single * variant_int_flux,
    }


def billard_variant_flux(k: float | None = None):
    """ReactorFlux for the Billard-variant CSV, renormalized by k (default k_single).

    The variant CSV has no rel_uncertainty column, so rel is zeroed (the band is
    not used for the Billard fold).
    """
    if k is None:
        k = billard_k_factor()["k_single"]
    return ReactorFlux(_BILLARD_VARIANT_CSV, scale=k, rel_col=None)


def integrated_rate_above(
    flux, T_floor_eV, T_max_eV=3300.0, n=4000, use_form_factor=True
):
    """Integrated CEvNS rate above a deposited-recoil threshold [counts/kg/day].

    R(>T_floor) = int_{T_floor}^{T_max} (dR/dT) dT on a log-spaced T grid (trapz).
    T in eV_nr; dR/dT summed over the five Ge isotopes with the Helm form factor.
    """
    Tg = np.logspace(np.log10(T_floor_eV), np.log10(T_max_eV), n)
    dr = np.array(
        [differential_rate(t * 1e-3, flux, use_form_factor) for t in Tg]
    )
    return float(np.trapz(dr, Tg * 1e-3))


def reproduce_billard(thresholds=(50.0, 100.0, 200.0), n=2000):
    """Reproduce Billard Table 1 with and without the k-rescale.

    Returns dict: k, rates_with_k, rates_without_k, overshoot_factor (per
    threshold), and percent agreement vs BILLARD_TABLE1. The without-k run folds
    the variant at its stored 3 GW_th/25 m normalization to demonstrate the ~90x
    overshoot (the forbidden proxy fp-billard-norm, kept only as a regression).
    """
    kinfo = billard_k_factor()
    k = kinfo["k_single"]
    flux_k = billard_variant_flux(k)
    flux_nok = billard_variant_flux(1.0)

    rates_with_k, rates_without_k, overshoot, pct = {}, {}, {}, {}
    for T0 in thresholds:
        rk = integrated_rate_above(flux_k, T0, n=n)
        rn = integrated_rate_above(flux_nok, T0, n=n)
        rates_with_k[T0] = rk
        rates_without_k[T0] = rn
        overshoot[T0] = rn / rk
        if T0 in BILLARD_TABLE1:
            pct[T0] = 100.0 * (rk - BILLARD_TABLE1[T0]) / BILLARD_TABLE1[T0]
    return {
        "k": k,
        "k_info": kinfo,
        "rates_with_k": rates_with_k,
        "rates_without_k": rates_without_k,
        "overshoot_factor": overshoot,
        "percent_vs_billard": pct,
    }


def conus_rescale_check(T_floor_eV=50.0, flux=None):
    """Coarse factor-~2 CONUS+ cross-check of the flagship absolute rate scale.

    Rescales BOTH the flagship (flux v1.0, 3 GW_th/25 m) rate and Billard's
    Table-1 rate to the CONUS+ config (3.6 GW_th, 20.7 m) by (P/P')(d'/d)^2 and
    compares. Two INDEPENDENTLY-normalized flux models (our HM+summation+ncapture
    flagship vs Billard's HM-flat variant) predicting the same Ge CEvNS scale is
    the cross-check. CAVEAT: CONUS+ reports eV_ee (ionization) and needs a
    quenching model, so this is a coarse rate-scale check, NOT a direct match.
    """
    if flux is None:
        flux = ReactorFlux()  # flagship v1.0
    P_v = params.REACTOR_POWER.value
    d_v = params.STANDOFF.value
    P_c = params.CONUS_POWER_GW.value
    d_c = params.CONUS_DISTANCE_M.value

    R_flagship = integrated_rate_above(flux, T_floor_eV)
    geom_ours_to_conus = (P_c / P_v) * (d_v / d_c) ** 2
    R_ours_at_conus = R_flagship * geom_ours_to_conus

    P_B = params.BILLARD_POWER_GW.value
    d_B = params.BILLARD_DISTANCE_M.value
    geom_bill_to_conus = (P_c / P_B) * (d_B / d_c) ** 2
    R_billard_at_conus = BILLARD_TABLE1[T_floor_eV] * geom_bill_to_conus

    return {
        "R_flagship_ours": R_flagship,
        "R_ours_at_conus": R_ours_at_conus,
        "R_billard_at_conus": R_billard_at_conus,
        "ratio": R_ours_at_conus / R_billard_at_conus,
    }


# --------------------------------------------------------------------------- #
# Flux-band propagation + sub-1.8-MeV sensitivity (Plan 03-02 Task 2)          #
# --------------------------------------------------------------------------- #


def fractional_band(T_keV, flux):
    """Fractional 1-sigma flux-uncertainty band on dR/dT (dimensionless).

    band_frac(T) = differential_rate_band(T) / differential_rate(T), i.e. the
    flux-weighted propagation of the split rel_uncertainty column. This is the
    HONEST propagated band; it does NOT reach the per-E 20-25% sub-1.8-MeV width
    because the well-anchored (2-5%) >1.8 MeV flux dominates the rate integrand
    at every recoil energy (see sub18_sensitivity_fraction for the placeholder's
    actual weight in the rate).
    """
    tot = differential_rate(T_keV, flux, use_form_factor=True)
    if tot <= 0.0:
        return 0.0
    return differential_rate_band(T_keV, flux) / tot


def sub18_sensitivity_fraction(T_keV, flux=None):
    """Fraction of dR/dT(T) drawn from the sub-1.8-MeV placeholder flux.

    = 1 - dR/dT(E_nu >= 1.8 MeV) / dR/dT(all E_nu). This is the honest measure of
    how much the Phase-2 sub-1.8-MeV placeholder influences a given recoil bin:
    it is 0 for T where E_min(T) >= 1.8 MeV (T >~ 95 eV_nr) and grows below that.
    """
    if flux is None:
        flux = ReactorFlux()
    tot = differential_rate(T_keV, flux, use_form_factor=True)
    if tot <= 0.0:
        return 0.0
    flux_cut = ReactorFlux(
        flux.csv_path, scale=flux.scale, e_min_cut_MeV=1.8
    )
    above = differential_rate(T_keV, flux_cut, use_form_factor=True)
    return 1.0 - above / tot


def build_dRdT_table(flux=None, n_grid=300):
    """Compute the per-isotope + total + band dR/dT table on the recoil grid.

    Returns (T_eV array, dict name->array, total array, band array). All rates
    in counts/kg/day/keV; T axis is deposited nuclear-recoil energy in eV_nr
    (NO quenching, NO detector response -- that is Phase 5).
    """
    if flux is None:
        flux = ReactorFlux()
    T_eV = recoil_grid_eV(n=n_grid)
    per_iso = {iso.name: np.zeros_like(T_eV) for iso in _GE_ISOTOPES}
    total = np.zeros_like(T_eV)
    band = np.zeros_like(T_eV)
    for k, T in enumerate(T_eV):
        T_keV = T * 1e-3
        d = differential_rate_per_isotope(T_keV, flux, use_form_factor=True)
        for name, val in d.items():
            per_iso[name][k] = val
        total[k] = sum(d.values())
        band[k] = differential_rate_band(T_keV, flux)
    return T_eV, per_iso, total, band
