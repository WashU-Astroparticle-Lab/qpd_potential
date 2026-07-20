# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
#
# Limiting-case tests for the Plan 01-02 energy-scale / response-definition
# module. Four contract acceptance tests (test-lowrate, test-saturation,
# test-ordering, test-equalsplit), each reflecting the CORRECTED physics from
# 01-CONTEXT / 01-RESEARCH:
#   1. low-rate linearity holds within 1% ONLY for Gamma <= 250 Hz (not 1 kHz);
#   2. BOTH censoring variants saturate at the 25 kHz ceiling (NOT 50 kHz);
#   3. Hf-before-Al ordering is the Gamma_in-based ~3.2x result (NOT 5-10x);
#   4. equal-split flips keV-scale saturation on/off (the binary discriminator),
#      while a genuine muon deposit still saturates even under equal-split
#      (localization sets the DEGREE, not the EXISTENCE, of muon saturation).

import math

import numpy as np
import pytest

from qpd_potential import energy_scale as es
from qpd_potential import params

DESIGN_NAMES = ("Ta->Al", "Al->Hf")
TAU_D = params.TAU_D.value          # 40e-6 s
CEILING = 1.0 / TAU_D               # 25 kHz


# --------------------------------------------------------------------------- #
# Dimensional / chain sanity (units in the derivation match units in code)     #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("name", DESIGN_NAMES)
def test_chain_dimensional_consistency(name):
    """N_qp dimensionless count; n_qp um^-3; Gamma_in Hz; peak = p * plateau."""
    N_qp = es.n_qp_yield(1.0, name)               # eps*E/Delta_tr, 1 eV
    n_qp = es.qp_density(N_qp, name)              # um^-3
    gamma = es.tunneling_rate(n_qp, name)        # Hz
    peak = es.peak_tunneling_rate(N_qp, name)    # Hz
    d = params.DESIGNS[name]
    # N_qp = 0.5 / Delta_tr (per eV): Al 0.5/190e-6, Hf 0.5/40e-6
    assert N_qp == pytest.approx(params.EPSILON.value / d.delta_tr.value)
    assert n_qp == pytest.approx(N_qp / d.v_tr.value)
    assert gamma == pytest.approx(d.K.value * n_qp)
    # peak Gamma_in is exactly the peak factor times the plateau rate
    assert peak == pytest.approx(es.peak_factor(name) * gamma)


# --------------------------------------------------------------------------- #
# Test 1 (test-lowrate): low-rate linearity with a rate-dependent tolerance    #
# --------------------------------------------------------------------------- #


def test_lowrate_linearity():
    """m ~= Gamma within ~1% ONLY for Gamma <= 250 Hz (Gamma*tau_d <= 0.01).

    At 1 kHz Gamma*tau_d = 0.04 and BOTH variants already deviate ~3.85-3.92%
    from Gamma -- so we do NOT assert 1% there; we assert ~5% AND that the
    deviation is genuinely larger than 1% (over-claiming 1% at 1 kHz is
    arithmetically wrong). The leading censoring correction is ~Gamma*tau_d.
    """
    for variant in params.CENSORING_VARIANTS:
        # <= 250 Hz: strict 1% linearity
        for G in (100.0, 250.0):
            m = es.observed_rate(G, variant)
            assert abs(m - G) / G < 0.01, (variant, G, m)
        # 1 kHz: deviation is ~Gamma*tau_d = 0.04 -> between 1% and 5%
        G = 1000.0
        m = es.observed_rate(G, variant)
        dev = abs(m - G) / G
        assert dev > 0.01, (variant, "must NOT be within 1% at 1 kHz", dev)
        assert dev < 0.05, (variant, "should be within ~5% at 1 kHz", dev)
        # deviation tracks the leading-order censoring correction Gamma*tau_d
        assert dev == pytest.approx(G * TAU_D, rel=0.2)


def test_lowrate_erec_linear_placeholder():
    """E_rec linear placeholder ~= 0.5*E_dep; default estimator is a Phase-5 stub."""
    for E_dep in (10.0, 100.0, 1000.0):
        assert es.E_rec_estimator(E_dep, linear_placeholder=True) == pytest.approx(
            0.5 * E_dep
        )
    # Default behaviour is the deliberate Phase-5 stub (not a real estimator).
    with pytest.raises(NotImplementedError):
        es.E_rec_estimator(1000.0)


# --------------------------------------------------------------------------- #
# Test 2 (test-saturation): 25 kHz ceiling, both variants                       #
# --------------------------------------------------------------------------- #


def test_saturation_ceiling_is_25kHz_not_50kHz():
    """Ceiling is 1/tau_d = 25 kHz (tau_d = 40 us), NOT 50 kHz (20 us sampling)."""
    assert CEILING == pytest.approx(25_000.0)
    assert es.SATURATION_CEILING_HZ == pytest.approx(25_000.0)
    # Guard against the 20 us -> 50 kHz conflation (forbidden proxy fp-20us).
    assert TAU_D == pytest.approx(40e-6)
    assert TAU_D != pytest.approx(20e-6)
    assert abs(CEILING - 50_000.0) > 1.0


def test_saturation_non_paralyzable_monotone_to_ceiling():
    """Non-paralyzable m monotone increasing, bounded by and -> 25 kHz."""
    G = np.logspace(2, 7, 4000)
    m = es.observed_rate(G, "non_paralyzable")
    assert np.all(np.diff(m) > 0)                 # strictly monotone increasing
    assert np.all(m <= CEILING + 1e-6)            # never exceeds 25 kHz
    assert m[-1] == pytest.approx(CEILING, rel=1e-2)  # -> 25 kHz at large Gamma


def test_saturation_paralyzable_rolls_over_at_ceiling():
    """Paralyzable m peaks at Gamma = 1/tau_d = 25 kHz then decreases (rolls over)."""
    G = np.logspace(2, 7, 4000)
    m = es.observed_rate(G, "paralyzable")
    G_peak = G[int(np.argmax(m))]
    assert 20_000.0 <= G_peak <= 30_000.0        # argmax at ~25 kHz
    # peak value is 1/(e*tau_d) = 25kHz/e ~= 9.2 kHz; and it rolls over after
    assert m.max() == pytest.approx(CEILING / math.e, rel=1e-2)
    assert m[-1] < m.max()                        # decreases at high input rate


# --------------------------------------------------------------------------- #
# Test 3 (test-ordering): Gamma_in-based Hf-before-Al ordering (~3.2x, not 5-10x)#
# --------------------------------------------------------------------------- #


def _plateau_gamma_per_eV(name):
    """Plateau Gamma_in per eV of E_sensor = K*eps/(Delta_tr*V_tr)."""
    return es.tunneling_rate(es.qp_density(es.n_qp_yield(1.0, name), name), name)


def test_ordering_gamma_in_ratio_is_about_3x():
    """Hf/Al plateau Gamma_in ratio ~3.2 (accept 2.5-4.0), NOT the 5-10x N_qp value."""
    ratio = _plateau_gamma_per_eV("Al->Hf") / _plateau_gamma_per_eV("Ta->Al")
    assert 2.5 <= ratio <= 4.0
    assert ratio == pytest.approx(3.1667, rel=1e-3)
    assert ratio < 5.0                            # explicitly NOT the 5-10x error
    # The 4.75x N_qp-per-eV ratio (Delta_Al/Delta_Hf) is the RAW yield ratio,
    # partly cancelled by Hf's 10x larger V_tr and 6.7x larger K -> ~3.2x rate.
    n_qp_ratio = es.n_qp_yield(1.0, "Al->Hf") / es.n_qp_yield(1.0, "Ta->Al")
    assert n_qp_ratio == pytest.approx(4.75, rel=1e-3)


def test_ordering_hf_saturates_at_lower_energy():
    """Peak Gamma_in hits 25 kHz at a smaller E_sensor for Hf than Al (Hf first)."""
    onset_al = es.saturation_onset_energy("Ta->Al")
    onset_hf = es.saturation_onset_energy("Al->Hf")
    assert onset_hf < onset_al
    # order-eV onsets, matching 01-RESEARCH (~1.3 eV Al, ~0.8 eV Hf)
    assert onset_al == pytest.approx(1.27, rel=0.05)
    assert onset_hf == pytest.approx(0.77, rel=0.05)
    # cross-check the onset is the energy where peak Gamma_in == ceiling
    for name, onset in (("Ta->Al", onset_al), ("Al->Hf", onset_hf)):
        assert es.peak_gamma_in_from_sensor_energy(onset, name) == pytest.approx(
            CEILING, rel=1e-6
        )


# --------------------------------------------------------------------------- #
# Test 4 (test-equalsplit): TWO parts -- keV-scale on/off + muon existence guard #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("name", DESIGN_NAMES)
def test_equalsplit_kev_scale_flips_saturation_off(name):
    """(1) keV-scale (CEvNS/Compton) deposit: saturates when LOCALIZED
    (f_prompt=0.3) but NOT when spread equally (f_prompt -> 0). This is the
    regime where localization genuinely flips saturation on/off -- the binary
    discriminator for the sharing model.
    """
    E_dep = 2000.0  # 2 keV, CEvNS/Compton-representative
    localized = es.peak_gamma_in_from_deposit(E_dep, name, f_prompt=0.3)
    equal_split = es.peak_gamma_in_from_deposit(E_dep, name, f_prompt=1e-6)
    assert es.is_saturated(localized), (name, "localized keV must saturate", localized)
    assert not es.is_saturated(equal_split), (
        name,
        "equal-split keV must NOT saturate (localization flips it off)",
        equal_split,
    )


@pytest.mark.parametrize("name", DESIGN_NAMES)
def test_equalsplit_muon_still_saturates(name):
    """(2) MUON existence guard: a genuine muon-scale deposit (>= ~1.5 MeV)
    STILL saturates even under equal-split (f_prompt -> 0). ~1.5 MeV over ~10300
    sensors is ~150 eV/sensor >> the ~0.8 eV (Hf) / ~1.3 eV (Al) onset, so
    muons saturate REGARDLESS of localization: localization sets the DEGREE
    (number of saturated sensors / compression factor), not the EXISTENCE.
    """
    E_dep = 1.5e6  # 1.5 MeV
    equal_split = es.peak_gamma_in_from_deposit(E_dep, name, f_prompt=1e-6)
    assert es.is_saturated(equal_split), (
        name,
        "muon must saturate even under equal-split",
        equal_split,
    )
    # sanity on the ~150 eV/sensor equal-split share >> ~1 eV onset
    E_sensor_eq = es.sensor_energy_split(E_dep, f_prompt=1e-6)
    assert E_sensor_eq == pytest.approx(1.5e6 / params.N_SENSORS.value, rel=1e-3)
    assert E_sensor_eq > 100.0
    assert E_sensor_eq > es.saturation_onset_energy(name)


def test_equalsplit_is_not_the_default_sharing_model():
    """Guard against forbidden proxy fp-nosat: the DEFAULT sharing is localized
    (f_prompt=0.3), under which the keV-scale deposit DOES saturate -- confirming
    equal-split is not silently the physical default."""
    E_dep = 2000.0
    for name in DESIGN_NAMES:
        default_share = es.peak_gamma_in_from_deposit(E_dep, name)  # params default
        assert es.is_saturated(default_share)
