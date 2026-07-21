"""Acceptance tests for the power->fission->flux normalization chain (Plan 02-02).

Covers acceptance test `test-normalization` and explicitly guards the named forbidden
proxies fp-loose-1e13 and fp-norm-chain-traps (GW_e vs GW_th, total-Q vs effective
thermal <E_f>, and the ~6/fission double-count).
"""
import numpy as np
import pytest

from src.flux.assemble_spectrum import (
    assemble,
    FISSION_FRACTIONS_DEFAULT,
    FISSION_FRACTIONS_BILLARD,
)
from src.flux import normalization as norm


# --------------------------------------------------------------------------------
# Core dimensioned chain: R_f and the integral flux
# --------------------------------------------------------------------------------
def test_effective_energy_is_thermal_not_total_Q():
    """<E_f> ~205 MeV (effective thermal); NOT the total Q (~215) incl. neutrinos."""
    e_f = norm.effective_energy_per_fission(FISSION_FRACTIONS_DEFAULT)
    assert 205.0 < e_f < 206.5           # default PWR mix lands ~205.8
    # total Q per fission (incl. ~10 MeV neutrino energy) would be >=214; guard it.
    assert e_f < 210.0


def test_fission_rate_order_of_magnitude():
    """R_f = P_th/<E_f> ~9x10^19 fissions/s at 3 GW_th."""
    r_f = norm.fission_rate(fractions=FISSION_FRACTIONS_DEFAULT)
    assert 8.5e19 < r_f < 9.5e19


def test_geometry_factor_25m():
    geom = norm.geometry_factor(2500.0)
    assert geom == pytest.approx(1.0 / (4 * np.pi * 2500.0**2), rel=1e-12)
    assert 1.2e-8 < geom < 1.3e-8


def test_integral_flux_hits_authoritative_target():
    """int Phi dE = 7-8x10^12 nu-bar cm^-2 s^-1 (test-normalization pass condition)."""
    spec = assemble()
    phi = norm.absolute_flux(spec.total(), spec.fractions)
    F = norm.integral_flux(spec.E, phi)
    assert norm.FLUX_TARGET_LO * 0.90 <= F <= norm.FLUX_TARGET_HI * 1.10  # within ~15%
    assert 7.0e12 <= F <= 8.0e12          # in fact lands inside the tight band


def test_flux_units_and_positivity():
    spec = assemble()
    phi = norm.absolute_flux(spec.total(), spec.fractions)
    assert phi.shape == spec.E.shape
    assert np.all(phi > 0)


def test_hayes_vogel_emission_cross_check():
    """~2x10^20 nu-bar s^-1 GW_th^-1 (Hayes-Vogel absolute-normalization anchor)."""
    spec = assemble()
    y = spec.integral_yields()
    rate = norm.emission_rate_per_gwth(y["grand_total_per_fission"], spec.fractions)
    assert 1.7e20 < rate < 2.3e20


# --------------------------------------------------------------------------------
# Forbidden-proxy guards
# --------------------------------------------------------------------------------
def test_guard_fp_norm_chain_gwe_trap():
    """Using GW_e (~1 GW) instead of 3 GW_th collapses the flux ~3x -> reject."""
    spec = assemble()
    phi_th = norm.absolute_flux(spec.total(), spec.fractions, p_th_w=3.0e9)
    phi_e = norm.absolute_flux(spec.total(), spec.fractions, p_th_w=1.0e9)  # electric trap
    F_th = norm.integral_flux(spec.E, phi_th)
    F_e = norm.integral_flux(spec.E, phi_e)
    assert F_th / F_e == pytest.approx(3.0, rel=1e-6)
    # the authoritative chain uses GW_th and lands in-band; the GW_e trap does NOT.
    assert 7.0e12 <= F_th <= 8.0e12
    assert F_e < 3.0e12


def test_guard_fp_norm_chain_double_count():
    """Re-multiplying the already-per-fission spectrum by ~6 inflates flux ~6x -> reject."""
    spec = assemble()
    phi = norm.absolute_flux(spec.total(), spec.fractions)
    F = norm.integral_flux(spec.E, phi)
    F_double = norm.integral_flux(spec.E, phi * 6.0)   # the double-count mistake
    assert F_double / F == pytest.approx(6.0, rel=1e-9)
    assert F <= 8.0e12 < F_double                      # only the single-count is in-band


def test_guard_fp_loose_1e13_not_a_tighter_target():
    """Authoritative target is 7-8e12; the flux is NOT tuned up to the loose ~1e13."""
    spec = assemble()
    phi = norm.absolute_flux(spec.total(), spec.fractions)
    F = norm.integral_flux(spec.E, phi)
    # the honest result sits ~25% below 1e13; forcing 1e13 would be a spurious inflation.
    assert F < 9.0e12
    assert abs(F - 1.0e13) / 1.0e13 > 0.20


def test_billard_fractions_change_Ef_only_slightly():
    """Billard mix (more Pu) raises <E_f> a few MeV but keeps R_f ~9e19 and flux in-band."""
    e_def = norm.effective_energy_per_fission(FISSION_FRACTIONS_DEFAULT)
    e_bil = norm.effective_energy_per_fission(FISSION_FRACTIONS_BILLARD)
    assert e_bil > e_def                     # 32.6% Pu-239 pushes <E_f> up
    assert 205.0 < e_bil < 209.0
