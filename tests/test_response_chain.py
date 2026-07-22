# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
#
# Plan 05-01 acceptance tests for the QPD forward response chain + count-integral
# E_rec estimator (qpd_potential.response). Covers the contract acceptance tests:
#   test-low-e-linear      -> test_low_e_linear_*          (calibration-consistency)
#   test-high-e-plateau    -> test_high_e_plateau_*        (VARIANT-SPECIFIC)
#   test-eventcount-mapping-> test_eventcount_mapping_*     (Pitfall 1)
#   test-crossover-band    -> test_crossover_band          (SIMU-01 band)
#   test-hf-first          -> test_hf_first
#   test-ta-gate           -> test_ta_gate_*               (binary gate)
# plus the ROADMAP Phase-5 stop-condition (test_stop_condition_*) and the
# pulse/event-count invariants that underpin them.

import dataclasses
import math

import numpy as np
import pytest

from qpd_potential import response as R
from qpd_potential import energy_scale as es
from qpd_potential import params

DESIGN_NAMES = ("Ta->Al", "Al->Hf")
VARIANTS = params.CENSORING_VARIANTS
CEILING = R.SATURATION_CEILING_HZ  # 25 kHz
MUON_TAIL_eV = 1.97e8              # 197 MeV muon deposit tail (Phase-4 range)


# --------------------------------------------------------------------------- #
# Pulse-shape / event-count invariants (foundation of the estimator)          #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("name", DESIGN_NAMES)
def test_pulse_unit_area_and_peak_factor(name):
    """INT g dt = 1 and tau_qp*max(g) = recorded two-exponential peak factor p.

    The EXACT two-exponential peak factor is 0.2500 (Al) and 0.1337 (Hf); the
    scaffold records these to 2 sig figs as 0.25 / 0.13. 0.1337 rounds to 0.13,
    so a 3% tolerance covers the recorded rounding (immaterial vs the LOW-
    confidence f_prompt band that dominates the crossover scale).
    """
    d = es.resolve_design(name)
    assert R.pulse_shape_integral(name) == pytest.approx(1.0, abs=1e-3)
    p = d.tau_qp.value * R.pulse_peak_value(name)
    p_recorded = es.peak_factor(name)
    assert p == pytest.approx(p_recorded, rel=0.03)


# --------------------------------------------------------------------------- #
# test-eventcount-mapping (Pitfall 1 / fp-eventcount)                          #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("name", DESIGN_NAMES)
def test_eventcount_mapping_is_integral_not_Nqp(name):
    """expected_n_qp fed to the EMG = INT Gamma_in dt, NOT the trapped count N_qp."""
    d = es.resolve_design(name)
    N_qp = es.n_qp_yield(1.0, name)              # trapped count at 1 eV
    ec = R.expected_event_count(N_qp, name)      # event count = INT Gamma_in dt

    # (a) event count is the integral of Gamma_in(t), verified numerically.
    t_grid = R._default_time_grid(d)
    integral = np.trapz(R.gamma_in_of_t(t_grid, N_qp, name), t_grid)
    assert ec == pytest.approx(integral, rel=1e-3)

    # (b) it is emphatically NOT N_qp: they differ by K*tau_qp/V_tr.
    expected_ratio = d.K.value * d.tau_qp.value / d.v_tr.value
    assert ec == pytest.approx(expected_ratio * N_qp, rel=1e-12)
    assert not math.isclose(ec, N_qp, rel_tol=0.5)  # 0.03x (Al) / 0.008x (Hf)

    # (c) the peak of Gamma_in(t) equals the scaffold peak_tunneling_rate
    #     (to 3%: the exact pulse peak factor 0.1337 (Hf) vs the recorded 0.13).
    peak = R.gamma_in_of_t(t_grid, N_qp, name).max()
    assert peak == pytest.approx(es.peak_tunneling_rate(N_qp, name), rel=3e-2)


@pytest.mark.parametrize("name", DESIGN_NAMES)
def test_eventcount_mapping_onset_matches_scaffold(name):
    """Realization saturation onset E_dep matches saturation_onset_energy via sharing."""
    E_dep_cross = R.onset_deposit_energy(name, params.F_PROMPT.value, params.R_SPOT.value)
    # On-spot peak Gamma_in at the crossover deposit must equal the 25 kHz ceiling.
    peak = es.peak_gamma_in_from_deposit(
        E_dep_cross, name, on_spot=True
    )
    assert peak == pytest.approx(CEILING, rel=1e-6)
    # And E_sensor at crossover equals the scaffold per-sensor onset.
    E_sensor = es.sensor_energy_split(E_dep_cross, on_spot=True)
    assert E_sensor == pytest.approx(es.saturation_onset_energy(name), rel=1e-6)


@pytest.mark.parametrize("name", DESIGN_NAMES)
def test_eventcount_mapping_realized_count(name):
    """QuasiparticleBurstModel realization reproduces the event-count Poisson mean."""
    rng = np.random.default_rng(2024)
    N_qp = es.n_qp_yield(0.5, name)
    ec = R.expected_event_count(N_qp, name)
    counts = np.array([R.realize_event_train(N_qp, name, rng).size for _ in range(300)])
    # sample mean within ~4 standard errors of the Poisson mean
    se = np.sqrt(ec / counts.size)
    assert abs(counts.mean() - ec) < 4.0 * se
    # analytic inhomogeneous-Poisson thinning agrees on the mean count too
    thin = np.array([R.analytic_thinning_train(N_qp, name, rng).size for _ in range(300)])
    assert abs(thin.mean() - ec) < 4.0 * math.sqrt(ec / thin.size)


@pytest.mark.parametrize("name", DESIGN_NAMES)
@pytest.mark.parametrize("variant", VARIANTS)
def test_realized_matches_analytic_unsaturated(name, variant):
    """EMG-realized censored count == analytic censored integral in the linear regime."""
    rng = np.random.default_rng(7)
    N_qp = es.n_qp_yield(0.3, name)  # below on-spot onset -> mild/no saturation
    analytic = R.censored_count(N_qp, name, variant)
    realized = np.array(
        [R.realized_censored_count(N_qp, name, rng, variant) for _ in range(400)]
    )
    se = realized.std() / math.sqrt(realized.size)
    assert abs(realized.mean() - analytic) < max(0.03 * analytic, 5 * se)


# --------------------------------------------------------------------------- #
# test-low-e-linear (CALIBRATION-CONSISTENCY, not independent validation)      #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("name", DESIGN_NAMES)
@pytest.mark.parametrize("variant", VARIANTS)
def test_low_e_linear_calibration_consistency(name, variant):
    """E_rec/E_dep = 0.5 well below onset. LABEL: calibration-consistency (Pitfall 2).

    C is fixed by the low-E slope, so this passes BY CONSTRUCTION; it is a
    consistency check, not independent validation. The genuine tests are the
    saturation onset and the plateau level (below).
    """
    C = R.calibrate_C(name, variant)
    for E_dep in (0.02, 0.05, 0.1):  # deeply linear (peak Gamma_in << 25 kHz)
        ratio = R.E_rec(E_dep, name, variant, C=C) / E_dep
        assert ratio == pytest.approx(0.5, rel=0.01)


@pytest.mark.parametrize("name", DESIGN_NAMES)
def test_single_global_calibration_constant(name):
    """C is a SINGLE global per-design constant (no per-bin tuning, Pitfall 2)."""
    # Recalibrating on different (linear) deposits yields the same C.
    C1 = R.calibrate_C(name, "non_paralyzable", E_dep_cal_eV=0.005)
    C2 = R.calibrate_C(name, "non_paralyzable", E_dep_cal_eV=0.02)
    assert C1 == pytest.approx(C2, rel=2e-3)


# --------------------------------------------------------------------------- #
# test-high-e-plateau (VARIANT-SPECIFIC; guards fp-no-saturation on BOTH)      #
# --------------------------------------------------------------------------- #


def _sweep(name, variant):
    grid = np.geomspace(10.0, MUON_TAIL_eV, 40)
    return R.sweep_E_rec(grid, name, variant)


@pytest.mark.parametrize("name", DESIGN_NAMES)
def test_high_e_plateau_non_paralyzable(name):
    """non_paralyzable: summed count caps -> E_rec PLATEAUS (monotone, bounded)."""
    s = _sweep(name, "non_paralyzable")
    E_dep, E_rec = s["E_dep"], s["E_rec"]
    # (a) monotone non-decreasing (bounded plateau, never turns over)
    assert np.all(np.diff(E_rec) >= -1e-9 * E_rec.max())
    # (b) NOT the linear 0.5*E_dep line at the muon tail (guards fp-no-saturation)
    assert E_rec[-1] < 1e-3 * (0.5 * E_dep[-1])
    # (c) genuinely plateaued: <2x change over the top decade of E_dep
    top = E_dep >= E_dep[-1] / 10.0
    assert E_rec[top].max() / E_rec[top].min() < 2.0
    # (d) plateau scale is the ~10-40 keV whole-array level, not MeV
    assert 5e3 < E_rec[-1] < 1e5


@pytest.mark.parametrize("name", DESIGN_NAMES)
def test_high_e_plateau_paralyzable_rollover(name):
    """paralyzable: censored count rolls over -> E_rec strictly sub-linear, turns over."""
    s = _sweep(name, "paralyzable")
    E_dep, E_rec = s["E_dep"], s["E_rec"]
    # (a) NOT linear at the muon tail (guards fp-no-saturation)
    assert E_rec[-1] < 1e-3 * (0.5 * E_dep[-1])
    # (b) genuine rollover: the peak E_rec occurs BELOW the muon tail and the
    #     tail value is below that peak.
    i_peak = int(np.argmax(E_rec))
    assert E_dep[i_peak] < 1e6           # peak well below the 197 MeV tail
    assert E_rec[-1] < E_rec[i_peak]     # rolled over


@pytest.mark.parametrize("name", DESIGN_NAMES)
def test_censoring_variants_differ_in_saturation(name):
    """Both variants are carried and differ qualitatively in deep saturation."""
    grid = np.array([50.0, MUON_TAIL_eV])
    np_tail = R.sweep_E_rec(grid, name, "non_paralyzable")["E_rec"][-1]
    p_tail = R.sweep_E_rec(grid, name, "paralyzable")["E_rec"][-1]
    # non_paralyzable plateau sits above the paralyzable rollover.
    assert np_tail > p_tail


# --------------------------------------------------------------------------- #
# ROADMAP Phase-5 stop condition                                              #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("name", DESIGN_NAMES)
@pytest.mark.parametrize("variant", VARIANTS)
def test_stop_condition_plateau_present(name, variant):
    """At 197 MeV peak Gamma_in >> 25 kHz AND a plateau/rollover exists.

    ROADMAP Phase-5 stop condition: if peak Gamma_in far exceeds the ceiling at
    the muon tail but the count-integral does NOT saturate, the model is wrong
    and we HALT. Here we assert the saturation IS present (does not trigger).
    """
    s = _sweep(name, variant)
    peak_tail = s["peak_gamma_on"][-1]
    assert peak_tail > 1e4 * CEILING              # far beyond the ceiling
    # saturation present: E_rec at the tail is >3 orders below the linear line
    assert s["E_rec"][-1] < 1e-3 * (0.5 * s["E_dep"][-1])


@pytest.mark.parametrize("name", DESIGN_NAMES)
def test_stop_condition_has_teeth(name):
    """WITHOUT censoring there is NO plateau -- confirms the plateau is real.

    Scratch check (Task-2 verify): an uncensored count-integral is exactly
    linear (E_rec = 0.5*E_dep at all energies), so it would FAIL the plateau
    assertion. The plateau in the censored estimator is therefore genuinely due
    to bandwidth censoring, not an artifact.
    """
    d = es.resolve_design(name)
    C = R.calibrate_C(name, "non_paralyzable")
    E_dep = MUON_TAIL_eV
    # Uncensored summed count = sum of event counts = linear in E_dep.
    fc = R.forward_counts(E_dep, name, "non_paralyzable")
    ec_on = R.expected_event_count(fc.N_qp_on, d)
    ec_off = R.expected_event_count(fc.N_qp_off, d)
    uncensored_total = fc.n_spot * ec_on + fc.n_off * ec_off
    E_rec_uncensored = C * uncensored_total
    # Uncensored tracks the linear 0.5*E_dep line (no plateau) -> would fail plateau.
    assert E_rec_uncensored == pytest.approx(0.5 * E_dep, rel=1e-3)
    # Censored E_rec is >1000x smaller -> the plateau assertion has teeth.
    assert R.E_rec(E_dep, name, "non_paralyzable", C=C) < 1e-3 * E_rec_uncensored


# --------------------------------------------------------------------------- #
# test-crossover-band (SIMU-01; guards fp-crossover-point)                     #
# --------------------------------------------------------------------------- #


def test_crossover_band_default_and_anchor():
    """Default point ~53/32 eV within 10%; equal-split anchor ~13/7.9 keV; a BAND."""
    expected = {
        "Ta->Al": {"default": 53.0, "equal_split": 13.08e3, "plateau": 18.7e3},
        "Al->Hf": {"default": 32.0, "equal_split": 7.93e3, "plateau": 11.3e3},
    }
    for name, exp in expected.items():
        cb = R.crossover_band(name)
        assert cb["default_point_eV"] == pytest.approx(exp["default"], rel=0.10)
        assert cb["equal_split_anchor_eV"] == pytest.approx(exp["equal_split"], rel=0.10)
        assert cb["whole_array_plateau_default_eV"] == pytest.approx(exp["plateau"], rel=0.10)
        # It is a BAND, not a point: spans well over an order of magnitude.
        assert cb["band_max_eV"] / cb["band_min_eV"] > 10.0
        # equal-split limit is the upper anchor (above the [0.1,0.5]x[1,5] scan).
        assert cb["equal_split_anchor_eV"] > cb["band_max_eV"]


# --------------------------------------------------------------------------- #
# test-hf-first                                                                #
# --------------------------------------------------------------------------- #


def test_hf_first_everywhere():
    """Al->Hf onset and crossover are below Ta->Al across the whole f_prompt/r band."""
    # per-sensor onset
    assert es.saturation_onset_energy("Al->Hf") < es.saturation_onset_energy("Ta->Al")
    # crossover deposit energy across the scan grid
    fps = np.linspace(*params.F_PROMPT_RANGE, 7)
    rs = np.linspace(*params.R_SPOT_RANGE, 7)
    for fp in fps:
        for r in rs:
            hf = R.onset_deposit_energy("Al->Hf", fp, r)
            ta = R.onset_deposit_energy("Ta->Al", fp, r)
            assert hf < ta


# --------------------------------------------------------------------------- #
# test-ta-gate (binary gate, NOT a response band; guards fp-ta-band)           #
# --------------------------------------------------------------------------- #


def test_ta_gate_holds_for_both_designs():
    """Trapping gate Delta_abs/Delta_tr >= 2 holds for the cited baselines."""
    assert R.trapping_gate_ok("Ta->Al")
    assert R.trapping_gate_ok("Al->Hf")
    assert params.trapping_ratio("Ta->Al") == pytest.approx(3.58, rel=0.02)
    # Bulk alpha-Ta T_c gate: T_c >= 2.5 K (380 ueV / 1.764 k_B). alpha-Ta = 4.48 K.
    k_B_eV_per_K = 8.617333e-5
    T_c_gate = 2.0 * es.resolve_design("Ta->Al").delta_tr.value / (1.764 * k_B_eV_per_K)
    assert T_c_gate == pytest.approx(2.5, abs=0.2)


def test_ta_gate_asserts_on_sub_gate():
    """A sub-gate ratio (e.g. beta-Ta) fires the assert -- design premise invalid."""
    d = es.resolve_design("Ta->Al")
    beta = dataclasses.replace(
        d, delta_abs=params.Param(300e-6, "eV", "beta-Ta test (sub-gate)", "LOW")
    )
    with pytest.raises(AssertionError):
        R.assert_trapping_gate(beta)


def test_ta_response_invariant_to_delta_abs_in_alpha_phase():
    """Ta->Al response does NOT move with Delta_abs within alpha-phase (uses Delta_tr)."""
    d = es.resolve_design("Ta->Al")
    ref_cross = R.onset_deposit_energy(d, 0.3, 2.0)
    ref_erec = R.E_rec(10.0, d, "non_paralyzable")
    for da in (0.5e-3, 0.68e-3, 0.9e-3):  # all alpha-phase, all pass the gate
        dd = dataclasses.replace(
            d, delta_abs=params.Param(da, "eV", "alpha-Ta variation", "MEDIUM")
        )
        assert R.trapping_gate_ok(dd)
        assert R.onset_deposit_energy(dd, 0.3, 2.0) == pytest.approx(ref_cross, rel=1e-12)
        assert R.E_rec(10.0, dd, "non_paralyzable") == pytest.approx(ref_erec, rel=1e-12)


# --------------------------------------------------------------------------- #
# Scaffold stub left intact (estimator lives in response.py, not energy_scale) #
# --------------------------------------------------------------------------- #


def test_phase1_stub_left_intact():
    """The Phase-1 E_rec_estimator stub is unchanged (real estimator is in response.py)."""
    with pytest.raises(NotImplementedError):
        es.E_rec_estimator(1.0)
    assert es.E_rec_estimator(1.0, linear_placeholder=True) == pytest.approx(0.5)
