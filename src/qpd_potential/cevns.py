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

from . import params

# Bare numeric values pulled once from the provenance-tagged registry.
_G_F = params.G_F.value                              # GeV^-2
_ONE_MINUS_4SIN2 = params.ONE_MINUS_4SIN2THETAW.value  # dimensionless (= 1 - 4 sin^2 theta_W)
_HBARC2 = params.HBARC2.value                        # GeV^2 * cm^2
_PREFACTOR_DENOM = params.CEVNS_PREFACTOR_DENOM.value  # 4 * pi

_MEV_PER_GEV = 1.0e-3  # 1 MeV = 1e-3 GeV


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
