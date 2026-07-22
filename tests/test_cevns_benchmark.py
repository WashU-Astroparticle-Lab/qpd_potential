"""CEvNS closed-form benchmark: sigma(72Ge, 4 MeV) ~= 1.0e-40 cm^2 (full Q_W).

Guards the #1 CEvNS unit bug. If sigma comes out ~1e-42 or ~1e-13, the (hbar c)^2
or /4pi factor is wrong -> fail loudly. The N-only quick-check ~1.08e-40 cm^2 is
a ~20% coarse cross-check, NOT the primary target.
"""

import math

from qpd_potential import cevns
from qpd_potential import params as p

# 72Ge benchmark isotope.
Z, N = 32, 40
E_NU_MEV = 4.0


def test_weak_charge_full():
    # Q_W = N - (1 - 4 sin^2 theta_W) Z = 40 - 0.0452*32 = 38.5536
    Q_W = cevns.weak_charge(Z, N)
    assert math.isclose(Q_W, 40 - 0.0452 * 32, rel_tol=1e-9)
    assert math.isclose(Q_W, 38.5536, abs_tol=1e-4)


def test_sigma_full_QW_benchmark():
    # PRIMARY target: full Q_W within +/-5% of 1.0e-40 cm^2.
    sigma = cevns.sigma_tot_MeV(E_NU_MEV, Z, N)
    assert math.isclose(sigma, 1.0e-40, rel_tol=0.05), f"sigma={sigma:.4e} cm^2"


def test_sigma_N_only_quickcheck():
    # N-only quick-check: replace Q_W -> N. Within +/-20% of 1.08e-40 cm^2.
    # Evaluate directly with the closed form using Q_W = N.
    E_GeV = E_NU_MEV * 1e-3
    sigma_N = (
        p.G_F.value**2 * N**2 * E_GeV**2 / p.CEVNS_PREFACTOR_DENOM.value
    ) * p.HBARC2.value
    assert math.isclose(sigma_N, 1.08e-40, rel_tol=0.20), f"sigma_N={sigma_N:.4e} cm^2"


def test_units_are_cm2_not_GeV_inverse2():
    # The returned magnitude must be ~1e-40 (cm^2), proving (hbar c)^2 was applied.
    # A bare GeV^-2 result would be ~2.6e-13; forbid that regime.
    sigma = cevns.sigma_tot_MeV(E_NU_MEV, Z, N)
    assert 1e-41 < sigma < 1e-39, f"sigma={sigma:.4e} out of cm^2 CEvNS range"
    # Explicitly reject the two classic bugs:
    #   - GeV^-2 left unconverted (~1e-13)
    #   - /8pi factor-of-2 error would give ~0.5e-40 (still ~1e-40 band, but
    #     the +/-5% full-Q_W test above catches it).
    assert sigma < 1e-30  # not left in GeV^-2


def test_rate_scales_as_N_squared_approx():
    # Full Q_W vs N-only differ only by (Q_W/N)^2 ~ 0.929.
    sigma_full = cevns.sigma_tot_MeV(E_NU_MEV, Z, N)
    E_GeV = E_NU_MEV * 1e-3
    sigma_N = (
        p.G_F.value**2 * N**2 * E_GeV**2 / p.CEVNS_PREFACTOR_DENOM.value
    ) * p.HBARC2.value
    Q_W = cevns.weak_charge(Z, N)
    assert math.isclose(sigma_full / sigma_N, (Q_W / N) ** 2, rel_tol=1e-9)
