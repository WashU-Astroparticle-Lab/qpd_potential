# ASSERT_CONVENTION: natural_units=io_MeV, power=GW_thermal, standoff_cm=2500, energy_per_fission=effective_thermal_Ma2013
"""
Absolute-flux normalization of the per-fission reactor antineutrino spectrum.

Chain (Phase-1 CONVENTIONS Sections A, D, G):

    R_f     = P_th / <E_f>                               [fissions s^-1]
    <E_f>   = sum_i f_i E_i                              effective THERMAL energy/fission
    Phi(E)  = [ sum_i f_i S_i(E) + S_capture(E) ] * R_f * 1/(4 pi d^2)
                                                        [nu-bar cm^-2 s^-1 MeV^-1]

Authoritative inputs (do NOT substitute the common traps):
    * P_th = 3 GW_th  (THERMAL, not electric -- GW_e is a ~x3 trap).
    * <E_f> = effective thermal energy per fission, Ma et al. PRC 88, 014605 (2013):
        235U 202.4, 238U 205.9, 239Pu 211.1, 241Pu 213.6 MeV.
      This is the energy DEPOSITED in the core; it is NOT the total Q that includes
      the ~10 MeV carried off by the antineutrinos (using total Q is a trap).
    * d = 2500 cm (25 m), point source 1/(4 pi d^2).
    * The per-fission spectrum from Plan 02-01 already integrates to ~6/fission, so
      R_f and the geometry factor are applied EXACTLY ONCE (no re-multiply by ~6).

Authoritative normalization TARGET: integral flux ~7-8x10^12 nu-bar cm^-2 s^-1
(Phase-1 lock + verified arithmetic). The '~1x10^13' in REQUIREMENTS.md CALC-01 is a
loose order-of-magnitude rounding, NOT a tighter target -- do not tune to it
(forbidden proxy fp-loose-1e13).

Cross-check anchor: emission rate ~2x10^20 nu-bar s^-1 GW_th^-1 (Hayes & Vogel,
ARNPS 66, 219 (2016)).
"""
from __future__ import annotations

from typing import Dict, Mapping, Tuple

import numpy as np

# --- Sourced physical constants ---------------------------------------------------
MEV_TO_J = 1.602176634e-13          # J per MeV (exact, CODATA 2018 elementary charge)

# Effective THERMAL energy released per fission per isotope [MeV], Ma et al. (2013).
# NOTE: effective thermal (deposited) energy, NOT total Q including neutrino energy.
E_EFF_MEV: Dict[str, float] = {
    "235U": 202.4,
    "238U": 205.9,
    "239Pu": 211.1,
    "241Pu": 213.6,
}

# Authoritative detector/normalization constants (CONVENTIONS Section D).
P_TH_DEFAULT_W = 3.0e9              # 3 GW_th (THERMAL). GW_e would be ~x3 too small.
D_CM_DEFAULT = 2500.0              # 25 m standoff, in cm.

# Authoritative normalization target band (nu-bar cm^-2 s^-1).
FLUX_TARGET_LO = 7.0e12
FLUX_TARGET_HI = 8.0e12


def effective_energy_per_fission(fractions: Mapping[str, float]) -> float:
    """<E_f> = sum_i f_i E_i / sum_i f_i  [MeV], effective thermal (Ma et al.).

    Normalizing by sum f_i guards against fraction sets that do not sum to exactly 1.
    Guards the total-Q trap: the returned value is ~200-214 MeV (thermal), never the
    ~210-224 MeV total Q that includes antineutrino energy.
    """
    num = 0.0
    den = 0.0
    for iso, f in fractions.items():
        if iso not in E_EFF_MEV:
            raise KeyError(f"No effective thermal energy for isotope {iso!r}")
        num += f * E_EFF_MEV[iso]
        den += f
    if den <= 0:
        raise ValueError("Fission fractions must have positive sum")
    e_f = num / den
    # dimensioned sanity: effective thermal energy per fission is ~200-214 MeV
    assert 195.0 < e_f < 220.0, f"<E_f> = {e_f} MeV outside physical thermal range"
    return e_f


def fission_rate(p_th_w: float = P_TH_DEFAULT_W,
                 e_f_mev: float | None = None,
                 fractions: Mapping[str, float] | None = None) -> float:
    """R_f = P_th / <E_f>  [fissions s^-1].

    p_th_w in Watts (J/s); <E_f> supplied in MeV or derived from ``fractions``.
    Dimensioned check: [J/s] / [J/fission] = [fissions/s]; expect R_f ~9x10^19 at 3 GW_th.
    """
    if e_f_mev is None:
        if fractions is None:
            raise ValueError("Provide either e_f_mev or fractions")
        e_f_mev = effective_energy_per_fission(fractions)
    e_f_joule = e_f_mev * MEV_TO_J                     # J per fission
    r_f = p_th_w / e_f_joule                           # (J/s)/(J/fission) = fissions/s
    # dimensioned sanity: R_f must correspond to <E_f> in the physical 195-220 MeV band
    # for whatever power was supplied (power-relative, so it stays valid off 3 GW_th and
    # still flags a nonsense <E_f>). At 3 GW_th this pins R_f ~9x10^19 fissions/s.
    r_f_lo = p_th_w / (220.0 * MEV_TO_J)
    r_f_hi = p_th_w / (195.0 * MEV_TO_J)
    assert r_f_lo <= r_f <= r_f_hi, f"R_f = {r_f:.3e} fissions/s implies <E_f> outside 195-220 MeV"
    return r_f


def geometry_factor(d_cm: float = D_CM_DEFAULT) -> float:
    """1/(4 pi d^2)  [cm^-2], point-source dilution at standoff d."""
    if d_cm <= 0:
        raise ValueError("Standoff distance must be positive")
    return 1.0 / (4.0 * np.pi * d_cm * d_cm)


def normalization_constant(fractions: Mapping[str, float],
                           p_th_w: float = P_TH_DEFAULT_W,
                           d_cm: float = D_CM_DEFAULT) -> Tuple[float, Dict[str, float]]:
    """K = R_f * 1/(4 pi d^2) [fissions s^-1 cm^-2], applied ONCE to the per-fission spectrum.

    Returns (K, diagnostics) where diagnostics carries <E_f>, R_f, geometry, and the
    per-GW_th emission-rate cross-check for Hayes-Vogel.
    """
    e_f = effective_energy_per_fission(fractions)
    r_f = fission_rate(p_th_w=p_th_w, e_f_mev=e_f)
    geom = geometry_factor(d_cm)
    K = r_f * geom
    diagnostics = {
        "E_f_MeV": e_f,
        "R_f_fissions_per_s": r_f,
        "geometry_cm^-2": geom,
        "K_fissions_per_s_per_cm2": K,
        "emission_per_GWth": r_f / (p_th_w / 1.0e9),   # nu-bar/fission-scaled below
        "P_th_W": p_th_w,
        "d_cm": d_cm,
    }
    return K, diagnostics


def absolute_flux(spectrum_total_per_fission: np.ndarray,
                  fractions: Mapping[str, float],
                  p_th_w: float = P_TH_DEFAULT_W,
                  d_cm: float = D_CM_DEFAULT) -> np.ndarray:
    """Phi(E) = spectrum_total_per_fission(E) * R_f * 1/(4 pi d^2).

    ``spectrum_total_per_fission`` MUST be the already-per-fission spectrum
    [nu-bar/fission/MeV] = sum_i f_i S_i + S_capture (Plan 02-01). It is multiplied by
    R_f and geometry EXACTLY ONCE (the ~6/fission normalization is already baked in;
    re-multiplying by ~6 is the forbidden double-count trap).

    Returns Phi in nu-bar cm^-2 s^-1 MeV^-1.
    """
    K, _ = normalization_constant(fractions, p_th_w=p_th_w, d_cm=d_cm)
    return np.asarray(spectrum_total_per_fission, dtype=float) * K


def integral_flux(E: np.ndarray, phi: np.ndarray) -> float:
    """int Phi dE over the grid  [nu-bar cm^-2 s^-1]."""
    return float(np.trapz(np.asarray(phi, dtype=float), np.asarray(E, dtype=float)))


def emission_rate_per_gwth(total_per_fission_yield: float,
                           fractions: Mapping[str, float],
                           p_th_w: float = P_TH_DEFAULT_W) -> float:
    """Total nu-bar emission rate per GW_th [nu-bar s^-1 GW_th^-1] for Hayes-Vogel.

    = (nu-bar/fission) * R_f / (P_th in GW_th). Expect ~2x10^20.
    """
    r_f = fission_rate(p_th_w=p_th_w, fractions=fractions)
    p_gwth = p_th_w / 1.0e9
    return total_per_fission_yield * r_f / p_gwth


if __name__ == "__main__":
    from .assemble_spectrum import assemble, FISSION_FRACTIONS_DEFAULT

    spec = assemble()
    K, diag = normalization_constant(spec.fractions)
    phi = absolute_flux(spec.total(), spec.fractions)
    F = integral_flux(spec.E, phi)
    y = spec.integral_yields()
    rate = emission_rate_per_gwth(y["grand_total_per_fission"], spec.fractions)
    print(f"<E_f>        = {diag['E_f_MeV']:.3f} MeV")
    print(f"R_f          = {diag['R_f_fissions_per_s']:.3e} fissions/s")
    print(f"1/(4 pi d^2) = {diag['geometry_cm^-2']:.3e} cm^-2")
    print(f"grand total  = {y['grand_total_per_fission']:.3f} nu-bar/fission")
    print(f"integral Phi = {F:.3e} nu-bar/cm^2/s   (target 7-8e12)")
    print(f"emission     = {rate:.3e} nu-bar/s/GW_th   (Hayes-Vogel ~2e20)")
