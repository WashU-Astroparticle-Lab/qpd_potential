# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Phase-3 Plan 03-01 differential CEvNS tests.

Covers: closed-form identity int dsigma/dT dT (F=1) = sigma_tot (<0.1%),
sigma(72Ge,4 MeV) anchor, Helm F(0)=1 + endpoint magnitude, rate-closure
int(dR/dT)dT vs direct Sum_i N_i int Phi sigma_tot,i (<1%), per-isotope vs
lumped-A distinctness, and grid/quadrature convergence.
"""

import math

import numpy as np
import pytest
from scipy.integrate import quad

from qpd_potential import cevns
from qpd_potential import params as p

GE = p.GE_ISOTOPES
BENCH = {iso.name: iso for iso in GE}["72Ge"]


# --------------------------------------------------------------------------- #
# Helm form factor                                                             #
# --------------------------------------------------------------------------- #


def test_helm_F0_is_one():
    # F(0) = 1 exactly (limit 3 j1(x)/x -> 1).
    for iso in GE:
        assert math.isclose(cevns.helm_form_factor(0.0, iso.A), 1.0, abs_tol=1e-12)


def test_helm_q_is_dimensionless_fm_inv():
    # q from sqrt(2 M T) must be O(0.01-0.1) fm^-1 at reactor recoils, NOT O(MeV).
    q = cevns.momentum_transfer_fm_inv(0.2, BENCH.M_MeV)  # T = 200 eV
    assert 0.001 < q < 0.5, f"q={q} fm^-1 out of physical range"


def test_helm_F2_at_200eV_above_099():
    # Dominant recoil regime: F^2 > 0.99 at T = 200 eV.
    q = cevns.momentum_transfer_fm_inv(0.2, BENCH.M_MeV)
    F2 = cevns.helm_form_factor(q, BENCH.A) ** 2
    assert F2 > 0.99, f"F^2(200 eV)={F2}"


def test_helm_F2_near_endpoint_recorded():
    # Endpoint tail (~2 keV): F^2 dips to ~0.95, still O(1). Record it.
    q = cevns.momentum_transfer_fm_inv(2.0, BENCH.M_MeV)  # T = 2 keV
    F2 = cevns.helm_form_factor(q, BENCH.A) ** 2
    assert 0.9 < F2 < 0.99, f"F^2(2 keV)={F2}"


# --------------------------------------------------------------------------- #
# Closed-form identity: int dsigma/dT dT (F=1) = sigma_tot                      #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("E_nu_MeV", [2.0, 4.0, 8.0])
def test_closedform_identity_all_isotopes(E_nu_MeV):
    for iso in GE:
        T_max = cevns.T_max_keV(E_nu_MeV, iso.M_MeV)

        def integrand(T_keV, iso=iso):
            return cevns.dsigma_dT(
                E_nu_MeV, T_keV, iso.Z, iso.N, iso.M_MeV, iso.A,
                use_form_factor=False,
            )

        num, _ = quad(integrand, 0.0, T_max, limit=200)
        closed = cevns.sigma_tot_MeV(E_nu_MeV, iso.Z, iso.N)
        rel = abs(num - closed) / closed
        assert rel < 1e-3, f"{iso.name} E={E_nu_MeV}: rel={rel:.2e}"


def test_sigma_anchor_72Ge_4MeV():
    # CONVENTIONS Sec C primary anchor: sigma(72Ge, 4 MeV) ~ 1.0e-40 cm^2.
    sigma = cevns.sigma_tot_MeV(4.0, BENCH.Z, BENCH.N)
    assert math.isclose(sigma, 1.0e-40, rel_tol=0.20), f"sigma={sigma:.4e}"


# --------------------------------------------------------------------------- #
# Rate closure + per-isotope + convergence                                     #
# --------------------------------------------------------------------------- #


@pytest.fixture(scope="module")
def flux():
    return cevns.ReactorFlux()


def test_flux_interp_nonnegative(flux):
    Es = np.linspace(flux.E_min, flux.E_max, 2000)
    vals = np.array([flux.flux(E) for E in Es])
    assert np.all(vals >= 0.0), "PCHIP log-flux produced a negative value"


def test_rate_closure(flux):
    # int (dR/dT) dT (F=1) must equal the direct Sum_i N_i int Phi sigma_tot,i.
    # Fine grid + low floor so trapz truncation of the T integral is < 1%.
    T_eV = cevns.recoil_grid_eV(n=2000, T_min_eV=0.1, T_max_eV=3300.0)
    dRdT = np.array(
        [cevns.differential_rate(T * 1e-3, flux, use_form_factor=False) for T in T_eV]
    )
    # integrate over T in keV
    T_keV = T_eV * 1e-3
    integ = np.trapz(dRdT, T_keV)
    direct = cevns.integrated_rate_direct(flux, use_form_factor=False)
    rel = abs(integ - direct) / direct
    assert rel < 0.01, f"closure rel={rel:.3e} (path={integ:.4e}, direct={direct:.4e})"


def test_per_isotope_vs_lumped_A(flux):
    # Near the endpoint, the 5-isotope sum has isotopes switched off above their
    # own T_max, while a lumped A=72.63 nucleus has a single endpoint.
    # 76Ge (heaviest) has the lowest T_max; 70Ge (lightest) the highest.
    E = flux.E_max
    tmax = {iso.name: cevns.T_max_keV(E, iso.M_MeV) for iso in GE}
    assert tmax["70Ge"] > tmax["76Ge"], "endpoint ordering wrong"
    # Choose T between the heaviest-isotope endpoint and the lightest.
    T_between_keV = 0.5 * (tmax["76Ge"] + tmax["70Ge"])
    d = cevns.differential_rate_per_isotope(T_between_keV, flux, use_form_factor=True)
    # At this T, at least one isotope is kinematically closed (0) and at least
    # one is open (>0): the stepped structure.
    open_iso = [k for k, v in d.items() if v > 0.0]
    closed_iso = [k for k, v in d.items() if v == 0.0]
    assert open_iso and closed_iso, f"no step structure: {d}"

    # Lumped-A shortcut: single nucleus with A=72.63 differs measurably.
    M_lump = 72.63 * 931.494
    Z_lump, N_lump = 32, 41  # A=72.63 -> N~40.63; use representative
    lumped = cevns._fold_isotope(
        T_between_keV,
        p.GeIsotope(73, Z_lump, N_lump, 1.0, M_lump, "lumpedA"),
        flux,
        use_form_factor=True,
    )
    summed = sum(d.values())
    # They should not coincide near the endpoint (lumped has different T_max).
    assert not math.isclose(summed, lumped, rel_tol=0.02), (
        f"summed={summed:.3e} lumped={lumped:.3e} indistinguishable"
    )


def test_convergence_above_50eV(flux):
    # Integrated rate above 50 eV stable < 1% under grid + quad refinement.
    def integ_rate(n):
        T_eV = cevns.recoil_grid_eV(n=n, T_min_eV=50.0, T_max_eV=3200.0)
        dRdT = np.array(
            [cevns.differential_rate(T * 1e-3, flux, use_form_factor=True) for T in T_eV]
        )
        return np.trapz(dRdT, T_eV * 1e-3)

    coarse = integ_rate(120)
    fine = integ_rate(240)
    rel = abs(fine - coarse) / fine
    assert rel < 0.01, f"convergence rel={rel:.3e}"


def test_total_rate_physical_magnitude(flux):
    # Physical-scale guard for the flagship 3 GW_th / 25 m flux. The steeply
    # falling reactor-CEvNS spectrum gives ~68 counts/kg/day above 50 eV, falling
    # to ~13-23 at a realistic 200-300 eV threshold and ~1 only above ~700 eV.
    # This "tens above 50 eV" is the first-principles value from the LOCKED cross
    # section (sigma(72Ge,4MeV)=1.0e-40, exact) and the frozen flux -- NOT a bug.
    # The absolute-normalization comparison to Billard/CONUS+ is Plan 03-02.
    T_eV = cevns.recoil_grid_eV(n=240, T_min_eV=50.0, T_max_eV=3300.0)
    dRdT = np.array(
        [cevns.differential_rate(T * 1e-3, flux, use_form_factor=True) for T in T_eV]
    )
    rate = np.trapz(dRdT, T_eV * 1e-3)
    assert 1.0 < rate < 500.0, f"integrated rate above 50 eV = {rate:.3e} counts/kg/day"


def test_dsigma_units_cm2_per_keV():
    # dsigma/dT * dT (keV) accumulates to cm^2-scale sigma; a single value at a
    # mid recoil is ~1e-38 cm^2/keV order (sigma~1e-40 over ~1e-2 keV window).
    ds = cevns.dsigma_dT(4.0, 0.2, BENCH.Z, BENCH.N, BENCH.M_MeV, BENCH.A)
    assert 1e-42 < ds < 1e-35, f"dsigma/dT={ds:.3e} cm^2/keV out of range"
