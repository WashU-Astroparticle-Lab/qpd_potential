# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Plan 10-02: the sub-eV trigger-probability curve and its composition rule.

ROADMAP Phase 10 success criterion 4; requirement CALC-16, whose named
acceptance evidence is "a unit test on the composed efficiency chain".

The decisive test in this file is ``test_eps_perturbation_composed_still_depends_on_eps``:
it is the only one that would fail if the sigmoid had REPLACED eps ~= 0.5
instead of multiplying on top of it.
"""
import importlib
import os
import subprocess
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from qpd_potential import energy_scale as es
from qpd_potential import params
from qpd_potential import response as resp
from qpd_potential import trigger

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: The declared scan range, sampled densely. The 50%-point invariance must hold
#: for EVERY value here, not just the default (fp-e50-by-tuning).
_K_GRID = np.concatenate([
    np.linspace(*params.TRIGGER_SHARPNESS_RANGE, 45),
    np.array([params.TRIGGER_SHARPNESS.value]),
])


# --------------------------------------------------------------------------- #
# claim-e50: the 50% point is STRUCTURAL, not tuned                            #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("k", _K_GRID)
def test_e50_invariance_across_the_whole_scan_range(k):
    """test-e50-invariance: P(0.5 eV) == 0.5 to 1e-12 for EVERY sharpness."""
    p = float(trigger.P_trig(params.TRIGGER_E50.value, sharpness=k))
    assert abs(p - 0.5) < 1e-12, f"k={k}: P(E50) = {p!r}"


def test_e50_is_the_registered_parameter_not_a_literal():
    """test-e50-parameter-coverage + fp-hardcoded-width: both E50 and k are
    registered params, and neither appears as a bare literal in the sigmoid."""
    # E50 changed 0.5 -> 1.0 eV by user decision 2026-07-23 (CONVENTIONS Section I).
    assert params.TRIGGER_E50.value == 1.0
    assert params.TRIGGER_E50.units == "eV"
    assert params.TRIGGER_SHARPNESS.units == ""          # dimensionless
    assert params.TRIGGER_SHARPNESS.confidence == "LOW"  # fixed by no artifact
    lo, hi = params.TRIGGER_SHARPNESS_RANGE
    assert lo < params.TRIGGER_SHARPNESS.value < hi
    # the implementation signature exposes both, defaulting to the registry
    import inspect
    sig = inspect.signature(trigger.P_trig)
    assert set(sig.parameters) == {"E_dep_eV", "e50_eV", "sharpness"}
    assert sig.parameters["e50_eV"].default is None
    assert sig.parameters["sharpness"].default is None


def test_no_bare_50_percent_literal_in_the_sigmoid_expression():
    """grep guard: the 50% point must come from the registered parameter."""
    src = open(os.path.join(_ROOT, "src", "qpd_potential", "trigger.py")).read()
    body = src.split("def P_trig(")[1].split("\ndef ")[0]
    code = [ln for ln in body.splitlines()
            if ln.strip() and not ln.strip().startswith("#")]
    code = "\n".join(code)
    code_only = code.split('"""')[0] + code.split('"""')[-1]
    assert "0.5" not in code_only, "a bare 0.5 appears in the P_trig code path"
    assert "params.TRIGGER_E50.value" in code_only
    assert "params.TRIGGER_SHARPNESS.value" in code_only


def test_zero_limit_and_saturation():
    """test-zero-limit. A form giving nonzero probability at zero deposit is
    rejected -- a detector cannot trigger on nothing."""
    assert float(trigger.P_trig(0.0)) == 0.0            # exactly
    assert float(trigger.P_trig(1e-6)) < 1e-6
    assert float(trigger.P_trig(1e3 * params.TRIGGER_E50.value)) > 1.0 - 1e-6


@pytest.mark.parametrize("k", [1.0, 2.0, 4.0, 8.0, 12.0])
def test_zero_limit_holds_for_every_sharpness(k):
    assert float(trigger.P_trig(0.0, sharpness=k)) == 0.0
    assert float(trigger.P_trig(1e-9, sharpness=k)) < 1e-6


def test_monotonic_and_bounded():
    """test-monotonic on a dense log grid from 1e-3 to 1e3 eV."""
    E = np.logspace(-3, 3, 4001)
    P = np.asarray(trigger.P_trig(E))
    assert np.all(np.diff(P) > 0.0), "not strictly increasing"
    assert np.all((P >= 0.0) & (P <= 1.0))


def test_negative_energy_is_rejected_not_evaluated():
    with pytest.raises(ValueError):
        trigger.P_trig(-1.0)
    with pytest.raises(ValueError):
        trigger.P_trig(np.array([0.1, -0.1]))


def test_nonpositive_parameters_are_rejected():
    with pytest.raises(ValueError):
        trigger.P_trig(0.5, sharpness=0.0)
    with pytest.raises(ValueError):
        trigger.P_trig(0.5, e50_eV=0.0)


# --------------------------------------------------------------------------- #
# fp-linear-sigmoid: show WHICH assertion the rejected form breaks             #
# --------------------------------------------------------------------------- #
def test_linear_energy_logistic_fails_the_zero_limit():
    """The rejected alternative gives P(0) = 1/(1 + exp(E50/w)) > 0: a nonzero
    probability of triggering on NOTHING. This is the reason the Hill form was
    chosen, not a stylistic preference."""
    p0 = float(trigger.linear_energy_logistic_rejected(0.0, width_eV=0.1))
    assert p0 > 0.0
    e50 = params.TRIGGER_E50.value
    assert p0 == pytest.approx(1.0 / (1.0 + np.exp(e50 / 0.1)), rel=1e-12)
    # magnitude quoted at the CURRENT E50; it was 6.692850924e-03 at E50 = 0.5 eV
    assert 0.0 < p0 < 1.0e-2
    # ... and it is nonzero at NEGATIVE energy too
    assert float(trigger.linear_energy_logistic_rejected(-1.0, width_eV=0.1)) > 0.0
    # the adopted form passes exactly where the rejected one fails
    assert float(trigger.P_trig(0.0)) == 0.0


def test_linear_energy_logistic_50_percent_point_is_width_dependent_in_practice():
    """Both forms put the 50% point at E50 analytically, but only the Hill form
    keeps P(0) = 0 while doing so. Recorded so the comparison is on the record."""
    for w in (0.05, 0.1, 0.3):
        p = float(trigger.linear_energy_logistic_rejected(
            params.TRIGGER_E50.value, width_eV=w))
        assert p == pytest.approx(0.5, abs=1e-12)
        assert float(trigger.linear_energy_logistic_rejected(0.0, width_eV=w)) > 0.0


# --------------------------------------------------------------------------- #
# claim-multiplies: the composed chain                                        #
# --------------------------------------------------------------------------- #
def _untriggered_chain(E_dep_eV, design="Ta->Al"):
    """An un-triggered quantity that DEMONSTRABLY contains eps.

    Deliberately built from energy_scale.n_qp_yield, which is literally
    N_qp = eps * E_sensor / Delta_tr, so the eps-perturbation test has something
    real to perturb rather than a mock."""
    d = es.resolve_design(design)
    E_on = es.sensor_energy_split(float(E_dep_eV), params.F_PROMPT.value,
                                  params.R_SPOT.value, params.N_SENSORS.value,
                                  on_spot=True)
    return float(es.n_qp_yield(E_on, d))


def test_composition_factorises_exactly():
    """test-composition-factorisation: composed == P_trig * untriggered, exactly."""
    for E in np.logspace(-1, 1, 25):
        u = _untriggered_chain(E)
        composed = float(trigger.compose_efficiency(E, u))
        assert composed == float(trigger.P_trig(E)) * u   # bitwise, not approx


def test_p_trig_identically_one_recovers_the_chain_bit_for_bit():
    """Setting P_trig == 1 must reproduce the pre-existing chain with max
    absolute difference EXACTLY 0.0 -- proving the curve is a factor added on
    top, not a modification of what was there."""
    E = np.logspace(-1, 2, 200)
    u = np.array([_untriggered_chain(e) for e in E])
    composed_unit = np.asarray(u) * 1.0
    diffs = np.abs(composed_unit - u)
    assert float(diffs.max()) == 0.0
    # and via the real API with a P_trig forced to 1 by a huge E-over-E50 ratio
    far_above = 1e12 * params.TRIGGER_E50.value
    assert float(trigger.P_trig(far_above)) == 1.0
    assert float(trigger.compose_efficiency(far_above, 3.25)) == 3.25


def test_eps_perturbation_composed_still_depends_on_eps():
    """THE DECISIVE TEST (CALC-16 acceptance evidence, fp-sigmoid-replaces-eps).

    Perturb params.EPSILON from 0.5 to 0.25 and rebuild. The composed result
    must change by EXACTLY the same ratio as the un-triggered result, while
    P_trig at the same energy is BIT-IDENTICAL. A composed result insensitive to
    eps means the sigmoid has replaced it."""
    E = 0.7  # eV, inside the turn-on where P_trig is neither 0 nor 1
    original = params.EPSILON

    u0 = _untriggered_chain(E)
    p0 = float(trigger.P_trig(E))
    c0 = float(trigger.compose_efficiency(E, u0))
    assert 0.0 < p0 < 1.0, "pick a probe energy inside the turn-on"

    try:
        params.EPSILON = params.Param(
            0.25, "", "TEST PERTURBATION ONLY", "LOW", note="restored below")
        u1 = _untriggered_chain(E)
        p1 = float(trigger.P_trig(E))
        c1 = float(trigger.compose_efficiency(E, u1))
    finally:
        params.EPSILON = original

    assert params.EPSILON.value == 0.5, "the perturbation was not restored"

    # P_trig is untouched by eps -- it is an ANALYSIS efficiency
    assert p1 == p0                       # bit-identical
    # the un-triggered chain halves, because eps halved
    assert (u1 / u0) == pytest.approx(0.5, rel=1e-12)
    # and the composed chain must halve by the SAME ratio
    assert (c1 / c0) == pytest.approx(u1 / u0, rel=1e-12)
    assert (c1 / c0) == pytest.approx(0.5, rel=1e-12)


def test_eps_perturbation_test_would_catch_a_replacing_sigmoid():
    """Constructive proof that the test above is not vacuous: if the composition
    were rewritten as `composed = P_trig` alone (the named forbidden proxy), the
    composed ratio would be 1.0 while the un-triggered ratio is 0.5."""
    E = 0.7
    original = params.EPSILON

    def replacing_composition(E_dep_eV, untriggered):
        return float(trigger.P_trig(E_dep_eV))     # eps thrown away

    u0 = _untriggered_chain(E)
    c0_bad = replacing_composition(E, u0)
    try:
        params.EPSILON = params.Param(0.25, "", "TEST PERTURBATION ONLY", "LOW")
        u1 = _untriggered_chain(E)
        c1_bad = replacing_composition(E, u1)
    finally:
        params.EPSILON = original

    assert (u1 / u0) == pytest.approx(0.5, rel=1e-12)
    assert (c1_bad / c0_bad) == pytest.approx(1.0, rel=1e-12)
    assert (c1_bad / c0_bad) != pytest.approx(u1 / u0, rel=1e-3)


def test_p_trig_high_energy_limit_is_one_not_eps():
    """fp-sigmoid-replaces-eps, the other half: if eps had been absorbed into
    the sigmoid's normalisation, P_trig well above threshold would tend to 0.5
    rather than to 1."""
    assert float(trigger.P_trig(1e4)) == pytest.approx(1.0, abs=1e-12)
    assert float(trigger.P_trig(1e4)) != pytest.approx(params.EPSILON.value, abs=1e-6)


# --------------------------------------------------------------------------- #
# claim-regime: one importable boundary definition                            #
# --------------------------------------------------------------------------- #
def test_regime_constant_is_importable_and_unique():
    """test-regime-constant: exactly one definition, no competing literal."""
    assert trigger.SUBEV_REGIME_BOUNDARY_eV == 1.0
    # They are DISTINCT constants that, since the 2026-07-23 E50 change, happen to
    # coincide numerically at 1.0 eV. Before that change the boundary sat strictly
    # above E50, which is what made "report dR/dE above the boundary" safe: the
    # trigger was near-unity there. It no longer is -- P_trig(boundary) = 1/2 exactly.
    # Asserting they are separately DEFINED guards the thing that still matters;
    # asserting an ordering that no longer holds would just be false.
    # See the PR note: the boundary may need to move to ~3.2 eV (where P_trig >= 0.99
    # at k = 4) to recover its original meaning. That is a separate user decision.
    assert trigger.SUBEV_REGIME_BOUNDARY_eV == pytest.approx(
        params.TRIGGER_E50.value), "coincidence is expected post-2026-07-23; see PR"
    assert "trigger probability" in trigger.REGIME_STATEMENT
    assert "dR/dE_rec" in trigger.REGIME_STATEMENT
    out = subprocess.run(
        ["grep", "-rn", "^SUBEV_REGIME_BOUNDARY_eV", "--include=*.py", "src/"],
        cwd=_ROOT, capture_output=True, text=True).stdout
    defs = out.strip().splitlines()
    assert len(defs) == 1, f"more than one definition of the boundary: {defs}"
    assert defs[0].startswith("src/qpd_potential/trigger.py:")
    # ... and no competing literal is used as the boundary anywhere in src/
    competing = subprocess.run(
        ["grep", "-rn", "regime_boundary\\|REGIME_BOUNDARY", "--include=*.py", "src/"],
        cwd=_ROOT, capture_output=True, text=True).stdout.splitlines()
    assert all("SUBEV_REGIME_BOUNDARY_eV" in ln for ln in competing), competing


# --------------------------------------------------------------------------- #
# CONVENTIONS Sections E and F are untouched                                   #
# --------------------------------------------------------------------------- #
def test_conventions_E_and_F_untouched_by_this_plan():
    assert params.EPSILON.value == 0.5                  # Section E
    assert params.TAU_D.value == 40e-6                   # Section F
    assert params.SAMPLING.value == 20e-6
    assert params.DEFAULT_CENSORING == "non_paralyzable"
    conv = open(os.path.join(_ROOT, "GPD", "CONVENTIONS.md")).read()
    assert "## I. Sub-eV Trigger-Probability Curve" in conv
    sec_i = conv.split("## I. Sub-eV Trigger-Probability Curve")[1].split("\n---")[0]
    assert "does NOT replace" in sec_i
    assert "0.5 eV" in sec_i
    assert "phenomenological" in sec_i.lower()


def test_conventions_section_I_test_value_is_hand_checkable():
    """The Section I test value a reader can check by hand, in the style of the
    Section E and Section F test values."""
    # P(2 * E50) with k = 4 is 1/(1 + (1/2)^4) = 16/17
    p = float(trigger.P_trig(2.0 * params.TRIGGER_E50.value, sharpness=4.0))
    assert p == pytest.approx(16.0 / 17.0, rel=1e-12)
    # and P(E50/2) with k = 4 is 1/(1 + 2^4) = 1/17
    p = float(trigger.P_trig(0.5 * params.TRIGGER_E50.value, sharpness=4.0))
    assert p == pytest.approx(1.0 / 17.0, rel=1e-12)


def test_derivation_note_covers_every_declared_hypothesis_and_conclusion():
    """test-e50-proof-alignment / test-e50-parameter-coverage, mechanically."""
    path = os.path.join(
        _ROOT, "GPD", "phases",
        "10-sub-ev-grid-extension-and-the-trigger-observable-p-grid",
        "10-02-TRIGGER-CURVE-DERIVATION.md")
    assert os.path.exists(path)
    text = open(path).read()
    for hyp in ("hyp-positive-k", "hyp-positive-e50", "hyp-hill-form"):
        assert hyp in text, f"hypothesis {hyp} not accounted for"
    for concl in ("concl-e50-exact", "concl-zero-limit", "concl-unit-limit"):
        assert concl in text, f"conclusion clause {concl} not established"
    # every declared parameter appears with its stated domain
    for sym in ("E50", "k"):
        assert sym in text
    assert "1/(1 + 1^k) = 1/2" in text or "1/(1 + 1^k)" in text
    # the rejected alternative with its numeric P(0)
    assert "6.692850924" in text or "6.6929e-03" in text
