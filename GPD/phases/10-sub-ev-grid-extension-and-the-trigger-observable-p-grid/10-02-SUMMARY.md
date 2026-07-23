---
phase: 10-sub-ev-grid-extension-and-the-trigger-observable-p-grid
plan: 02
status: complete
one_liner: "Sub-eV observable installed as a Hill-form trigger probability whose 50% point is exactly 0.5 eV for all 46 sharpness values across the declared [1,12] range; the eps-perturbation test shows the composed chain halves with eps while P_trig stays bit-identical, and a constructive counter-test shows a replacing sigmoid would give ratio 1.0 instead of 0.5."
plan_contract_ref: GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-02-PLAN.md#/contract

contract_results:
  claims:
    claim-e50:
      status: passed
      summary: "For P(E) = 1/(1 + (E50/E)^k): P(E50) = 1/2 to better than 1e-12 for all 46 sharpness values tested across [1, 12]; P(0) = 0.0 exactly; P(1e-6 eV) = 1.6e-23; P(500 eV) = 0.999999999999; strictly increasing with all values in [0,1] on a 4001-point log grid from 1e-3 to 1e3 eV. The k-independence enters at 1^k = 1, so k never reaches the arithmetic and the 50% point is a property of the functional form, not of any width."
      linked_ids: [deliv-trigger, deliv-trigger-tests, deliv-e50-derivation, test-e50-invariance, test-zero-limit, test-monotonic, test-e50-proof-alignment, test-e50-parameter-coverage]
      proof_audit:
        completeness: incomplete
        reviewed_at: "2026-07-22T00:00:00Z"
        reviewer: gpd-executor
        summary: "Self-audited by the executor, not by gpd-check-proof. All three conclusion clauses are derived in 10-02-TRIGGER-CURVE-DERIVATION.md, all three hypotheses are used and their use is stated, all three declared parameters appear with their domains, and each clause is independently verified numerically. Marked incomplete because no adversarial proof-redteam artifact exists and no independent reviewer has run; the derivation is elementary algebra and one derivative, so the residual risk is low but it is not zero and is not laundered as complete."
        proof_artifact_path: GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-02-TRIGGER-CURVE-DERIVATION.md
        covered_hypothesis_ids: [hyp-positive-k, hyp-positive-e50, hyp-hill-form]
        missing_hypothesis_ids: []
        covered_parameter_symbols: [E, E50, k]
        missing_parameter_symbols: []
        uncovered_quantifiers: []
        uncovered_conclusion_clause_ids: []
        quantifier_status: matched
        scope_status: matched
        counterexample_status: none_found
        stale: false
      evidence:
        - verifier: gpd-executor
          method: parametrised numerical evaluation across the declared scan range plus symbolic derivation
          confidence: high
          claim_id: claim-e50
          deliverable_id: deliv-e50-derivation
          acceptance_test_id: test-e50-invariance
          reference_id: ref-roadmap-p10-sc4
          forbidden_proxy_id: fp-e50-by-tuning
          evidence_path: GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-02-TRIGGER-CURVE-DERIVATION.md
    claim-multiplies:
      status: passed
      summary: "composed(E) == P_trig(E) * untriggered(E) bitwise on 25 log-spaced deposits. Perturbing params.EPSILON 0.5 -> 0.25 changes the un-triggered chain by exactly 0.5 and the composed chain by exactly the same 0.5, while P_trig(0.7 eV) is bit-identical across the perturbation. The non-vacuity of that test is proved constructively: a composition rewritten as `composed = P_trig` alone gives a composed ratio of 1.0 against an un-triggered ratio of 0.5."
      linked_ids: [deliv-trigger, deliv-trigger-tests, deliv-conventions-entry, test-eps-perturbation, test-composition-factorisation]
    claim-regime:
      status: passed
      summary: "trigger.SUBEV_REGIME_BOUNDARY_eV = 1.0 eV is the single importable definition; a grep over src/ finds exactly one top-level assignment and no competing REGIME_BOUNDARY literal. trigger.REGIME_STATEMENT carries the one-sentence framing so downstream deliverables import it rather than paraphrase it."
      linked_ids: [deliv-trigger, deliv-conventions-entry, test-regime-constant]
  deliverables:
    deliv-trigger:
      status: passed
      path: src/qpd_potential/trigger.py
      summary: "P_trig (Hill form, numerically stable logistic in log energy so that (E50/E)^k cannot overflow four decades below E50), compose_efficiency (the composition point, created here because none existed), SUBEV_REGIME_BOUNDARY_eV, REGIME_STATEMENT, and linear_energy_logistic_rejected kept only so its defect stays testable. Module docstring states the phenomenological status and the rejection of the linear-energy form."
      linked_ids: [claim-e50, claim-multiplies, claim-regime]
    deliv-trigger-tests:
      status: passed
      path: tests/test_trigger_efficiency.py
      summary: "68 tests: 46 parametrised 50%-point invariance cases across the declared scan range, the zero-deposit and saturation limits, monotonicity, the factorisation identity, the eps-perturbation non-replacement test and its constructive counter-test, the regime-constant uniqueness grep, and the derivation-note coverage check."
      linked_ids: [claim-e50, claim-multiplies, claim-regime]
    deliv-e50-derivation:
      status: passed
      path: GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-02-TRIGGER-CURVE-DERIVATION.md
      summary: "The one-line algebra P(E50) = 1/(1 + 1^k) = 1/2 with the k-independence located explicitly at 1^k = 1; the E -> 0+ power-law approach and the E -> inf limit; dP/dE written out with both minus signs tracked; the rejected linear-energy logistic with P(0) = 6.692850924e-03 evaluated at w = 0.1 eV; the 10-90% span table; and five stated weaknesses of the construction."
      linked_ids: [claim-e50]
    deliv-conventions-entry:
      status: passed
      path: GPD/CONVENTIONS.md
      summary: "New Section I appended after Section H and before the Numerical Factor Registry, plus one Change Log line and one Numerical Factor Registry row. Records the curve, the decided 50% point, the exposed sharpness and its range, the 1.0 eV regime boundary, the explicit 'does NOT replace Section E's eps ~= 0.5 and does not modify Section F', the phenomenological status, three hand-checkable test values, and a standing sensitivity obligation on k."
      linked_ids: [claim-multiplies, claim-regime]
  acceptance_tests:
    test-e50-invariance:
      status: passed
      summary: "P_trig(0.5 eV) == 0.5 to better than 1e-12 for 46 sharpness values spanning [1, 12] plus the default 4.0. Structurally exact, not tuned."
      linked_ids: [claim-e50, deliv-trigger, deliv-trigger-tests]
    test-zero-limit:
      status: passed
      summary: "P_trig(0) == 0.0 exactly (implemented as an exact zero, not a floating-point limit); P_trig(1e-6 eV) = 1.6e-23 < 1e-6; P_trig(500 eV) = 0.9999999999990 > 1 - 1e-6. Also verified at k = 1, 2, 4, 8, 12 individually."
      linked_ids: [claim-e50, deliv-trigger, deliv-trigger-tests]
    test-monotonic:
      status: passed
      summary: "Strictly increasing (np.diff > 0 everywhere, not merely non-decreasing) with all values in [0, 1] on a 4001-point log grid from 1e-3 to 1e3 eV."
      linked_ids: [claim-e50, deliv-trigger-tests]
    test-e50-proof-alignment:
      status: passed
      summary: "All three conclusion clauses derived; all three hypotheses used with their use stated (hyp-positive-k is noted as NOT actually needed for concl-e50-exact, since 1^k = 1 holds for all real k, and that is said rather than glossed); the derivation states explicitly that the k-independence enters at 1^k = 1. Mechanically checked by test_derivation_note_covers_every_declared_hypothesis_and_conclusion."
      linked_ids: [claim-e50, deliv-e50-derivation]
    test-e50-parameter-coverage:
      status: passed
      summary: "E, E50 and k all appear in the derivation with their stated domains. The implemented signature P_trig(E_dep_eV, e50_eV=None, sharpness=None) exposes both parameters, defaulting to the registry. A source-level grep asserts no bare 0.5 appears in the P_trig code path and that both params.TRIGGER_E50.value and params.TRIGGER_SHARPNESS.value are read there."
      linked_ids: [claim-e50, deliv-e50-derivation, deliv-trigger]
    test-eps-perturbation:
      status: passed
      summary: "CALC-16's named acceptance evidence. At E_dep = 0.7 eV (inside the turn-on, P_trig = 0.9219, neither 0 nor 1): eps 0.5 -> 0.25 gives untriggered ratio 0.5 to 1e-12, composed ratio 0.5 to 1e-12, and P_trig bit-identical (p1 == p0 exactly). The un-triggered quantity is built from energy_scale.n_qp_yield, which is literally N_qp = eps * E_sensor / Delta_tr, so the perturbation acts on real code rather than on a mock."
      linked_ids: [claim-multiplies, deliv-trigger, deliv-trigger-tests]
    test-composition-factorisation:
      status: passed
      summary: "composed(E) == P_trig(E) * untriggered(E) with bitwise equality (==, not approx) on 25 log-spaced deposits from 0.1 to 10 eV. The P_trig == 1 limit reproduces the pre-existing chain with max absolute difference EXACTLY 0.0 over 200 grid points, and P_trig(1e12 * E50) == 1.0 exactly so compose_efficiency(E, 3.25) returns 3.25 unchanged."
      linked_ids: [claim-multiplies, deliv-trigger, deliv-trigger-tests]
    test-regime-constant:
      status: passed
      summary: "Exactly one top-level assignment of SUBEV_REGIME_BOUNDARY_eV in src/, in trigger.py; every other REGIME_BOUNDARY grep hit in src/ refers to that same name; no competing numeric literal."
      linked_ids: [claim-regime, deliv-trigger, deliv-conventions-entry]
  references:
    ref-roadmap-p10-sc4:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Success criterion 4 drove the exact-50%-point requirement and the composed-chain unit test as the named evidence; the forbidden-proxy line on treating the sigmoid as a replacement for eps drove the eps-perturbation test and its constructive counter-test. Cited in the module docstring, the derivation note and CONVENTIONS Section I."
    ref-calc16:
      status: completed
      completed_actions: [read, cite]
      missing_actions: []
      summary: "CALC-16's verification row names 'unit test on the composed efficiency chain' as the acceptance evidence; test_eps_perturbation_composed_still_depends_on_eps is that test, and test_eps_perturbation_test_would_catch_a_replacing_sigmoid proves it would fail if the sigmoid replaced eps."
    ref-conventions-ef:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Section E's eps ~= 0.5 is the efficiency this curve multiplies; Section F's non-paralyzable / 40 us censoring is untouched. git diff GPD/CONVENTIONS.md contains ZERO deletion lines, so Sections E and F are byte-identical; the diff is 35 added lines only. Pinned by test_conventions_E_and_F_untouched_by_this_plan."
    ref-user-decision:
      status: completed
      completed_actions: [read, cite]
      missing_actions: []
      summary: "GPD/STATE.md line 133, USER DECISION 2026-07-22, is quoted as the origin of both the 0.5 eV 50% point and the multiplies-not-replaces rule, and its reasoning (dR/dE_rec presupposes the lumped 50% collection efficiency, not defensible for a ~3-optical-phonon-quantum deposit in Ge) is carried verbatim into trigger.REGIME_STATEMENT and the module docstring."
  forbidden_proxies:
    fp-sigmoid-replaces-eps:
      status: rejected
      notes: "Rejected two ways. (1) The eps-perturbation test: composed ratio equals un-triggered ratio to 1e-12 while P_trig is bit-identical. (2) test_p_trig_high_energy_limit_is_one_not_eps asserts P_trig(1e4 eV) == 1.0 exactly and NOT 0.5, closing the other half of the proxy where eps is absorbed into the sigmoid's normalisation."
    fp-hardcoded-width:
      status: rejected
      notes: "The sharpness is params.TRIGGER_SHARPNESS (default 4.0, confidence LOW) with declared range params.TRIGGER_SHARPNESS_RANGE = (1, 12). A source-level grep asserts no bare 0.5 in the P_trig code path and that both parameters are read from the registry. CONVENTIONS Section I carries a standing obligation to report k-sensitivity with every downstream sub-eV result."
    fp-linear-sigmoid:
      status: rejected
      notes: "Rejected with a number, not an assertion: P_lin(0) = 1/(1 + e^{E50/w}) = 6.692850924e-03 at w = 0.1 eV, and P_lin(-1 eV) = 3.06e-07 > 0. The rejected form is retained in trigger.py as linear_energy_logistic_rejected solely so test_linear_energy_logistic_fails_the_zero_limit can demonstrate which assertion it breaks. It is never used as the project's curve."
    fp-e50-by-tuning:
      status: rejected
      notes: "The 50% point is verified at 46 sharpness values across the whole declared scan range, not at the default alone. The derivation locates the k-independence at 1^k = 1, so it is structural."
  uncertainty_markers:
    weakest_anchors:
      - "ONLY the 50% point is anchored. The functional form is chosen and the sharpness k is fixed by no measurement whatsoever -- no trigger threshold has ever been measured for this device. The default k = 4 was chosen because a factor-of-three 10-90% turn-on 'looks like a plausible detector threshold', and that is the entire justification."
      - "eps ~= 0.5 is itself an imposed forward-model definition (CONVENTIONS Section E), not a derived quantity, and the paper's own physical estimate is eta_ce ~= 0.3. The composition test proves the trigger curve multiplies eps; it does not make eps right."
      - "The composed chain treats the trigger as a function of DEPOSITED energy. If the real trigger acts on the reconstructed COUNT instead -- which for a counting detector is arguably the more natural readout-level statement -- the composition point is wrong even though the factorisation test passes. The factorisation test cannot detect this."
      - "The regime boundary 1.0 eV is a rounding of the roadmap's '~1 eV'. Nothing measures it; it is a labelling convention chosen so that one importable constant exists."
    unvalidated_assumptions:
      - "That a single scalar trigger probability, with no dependence on event position on the wafer or on which sensors fire, is adequate at 0.5 eV where the deposit is a few optical-phonon quanta and the LOW-confidence f_prompt / r sharing parameters govern which sensors see anything at all."
      - "That the trigger is well described by any smooth monotone curve at all, rather than by a discrete count threshold. Plan 10-04 measures the sub-eV response columns to be sparse and discrete; a count threshold would give a staircase, not a Hill curve."
    competing_explanations:
      - "The 50%-point invariance could be read as trivially true of any homogeneous-in-(E/E50) form, which it is. That is not a weakness -- it is exactly why the form was chosen -- but it does mean the invariance test constrains the FORM FAMILY, not the physics."
    disconfirming_observations:
      - "DID NOT OCCUR: 'perturbing params.EPSILON leaves the composed efficiency unchanged'. The composed ratio tracked the un-triggered ratio to 1e-12."
      - "DID NOT OCCUR: 'P_trig(0.5 eV) differs from 0.5 for some sharpness in the declared range'. All 46 values agreed to better than 1e-12."
      - "DID NOT OCCUR: 'setting P_trig == 1 does not reproduce the pre-existing chain bit-for-bit'. Max absolute difference exactly 0.0 over 200 grid points."
      - "STILL OPEN, handed to plan 10-04: the response matrix already puts finite probability on 'no counts registered' while this curve puts 1 - P_trig on 'not triggered'. Phases 12 and 15 will multiply them. Whether that double-counts non-detection is not answered here."
files_created:
  - src/qpd_potential/trigger.py
  - tests/test_trigger_efficiency.py
  - GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-02-TRIGGER-CURVE-DERIVATION.md
files_modified:
  - src/qpd_potential/params.py
  - GPD/CONVENTIONS.md
---

# Plan 10-02 Summary --- The Sub-eV Trigger Observable

## The curve

```
P_trig(E) = 1 / (1 + (E50 / E)^k),      P_trig(0) := 0
E50 = 0.5 eV   (params.TRIGGER_E50,      DECIDED, USER DECISION 2026-07-22)
k   = 4.0      (params.TRIGGER_SHARPNESS, EXPOSED, range [1, 12], MEASURED BY NOTHING)
```

Regime boundary: `trigger.SUBEV_REGIME_BOUNDARY_eV = 1.0` eV, one importable definition.

## The 50% point is structural, not tuned

`P(E50) = 1/(1 + 1^k) = 1/2`. The k-independence enters at `1^k = 1`, so `k` never reaches
the arithmetic. Verified at **46 sharpness values** spanning the whole declared scan range,
each to `|P - 1/2| < 1e-12` --- not at the default alone (`fp-e50-by-tuning`).

| probe | measured |
|---|---|
| P(0.5 eV), any k in [1,12] | 0.5 to <1e-12 |
| P(0) | **0.0 exactly** |
| P(1e-6 eV), k=4 | 1.6e-23 |
| P(500 eV) | 0.9999999999990 |
| P(1.0 eV), k=4 | 16/17 = 0.9411764705882353 |
| P(0.25 eV), k=4 | 1/17 = 0.0588235294117647 |

## Why not a linear-energy logistic --- with the number

`P_lin(E) = 1/(1 + exp(-(E-E50)/w))` also puts its 50% point at E50, so on the headline
constraint it looks equally good. It fails the zero limit:

```
P_lin(0) = 1/(1 + exp(0.5/0.1)) = 1/(1 + e^5) = 6.692850924e-03
```

**A 0.67% probability of triggering on a deposit of exactly zero energy**, and
`P_lin(-1 eV) = 3.06e-07 > 0` as well. On an axis spanning four decades from 0.1 eV that floor
would sit under every sub-eV number this milestone produces. The rejected form is kept in
`trigger.py` as `linear_energy_logistic_rejected` purely so the test suite can demonstrate
which assertion it breaks; it is never the project's curve.

## The decisive composition test (CALC-16 acceptance evidence)

There was **no existing efficiency-composition point** in the codebase: ε enters inside
`energy_scale.n_qp_yield` as `N_qp = ε·E_sensor/Δ_tr` *and* again as the `response.calibrate_C`
calibration slope. So `compose_efficiency` creates one.

At E_dep = 0.7 eV (inside the turn-on, P_trig = 0.9219, deliberately neither 0 nor 1),
perturbing `params.EPSILON` 0.5 → 0.25:

| quantity | ratio after / before |
|---|---|
| un-triggered chain (`n_qp_yield` on-spot) | **0.5** to 1e-12 |
| composed chain | **0.5** to 1e-12 |
| `P_trig(0.7 eV)` | **bit-identical** (`p1 == p0`) |

**And the test is not vacuous.** `test_eps_perturbation_test_would_catch_a_replacing_sigmoid`
constructs the forbidden composition `composed = P_trig` alone and measures it under the same
perturbation: composed ratio **1.0** against un-triggered ratio **0.5**. The test discriminates.

The other half of `fp-sigmoid-replaces-eps` --- ε absorbed into the sigmoid's normalisation so
that `P_trig(high E) → 0.5` --- is closed separately: `P_trig(1e4 eV) == 1.0` exactly.

Factorisation is bitwise (`==`, not `approx`) on 25 log-spaced deposits, and the `P_trig ≡ 1`
limit reproduces the pre-existing chain with **max absolute difference exactly 0.0** over 200
grid points.

## CONVENTIONS.md

New **Section I** appended after §H and before the Numerical Factor Registry, plus one Change
Log line and one registry row. `git diff GPD/CONVENTIONS.md` shows **35 added lines and zero
deleted lines**, so §E and §F are byte-identical.

## What this plan deliberately did not do

Nothing applies this curve to any spectrum. Phases 12 and 15 do that. No matrix, no rate, no
figure was produced here.

## The honest caveat, stated where it cannot be quoted away

Only the 50% point is anchored. The functional form is chosen and the sharpness is fixed by
**no measurement at all** --- `k = 4` was picked because a factor-of-three 10–90% turn-on
"looks like a plausible detector threshold", and that is the entire justification. It is
registered with confidence `LOW`, carries a declared scan range, and CONVENTIONS §I carries a
standing obligation that every downstream sub-eV result be reported with its sensitivity to k.

A sharper caveat that the factorisation test *cannot* catch: the composed chain treats the
trigger as a function of **deposited** energy. If the real trigger acts on the reconstructed
**count** instead — which for a counting detector is arguably the more natural readout-level
statement — the composition point is wrong even though every test here passes. Plan 10-04
measures the sub-eV columns to be sparse and discrete, which makes a count threshold (a
staircase) at least as plausible a description as a smooth Hill curve.

## Handed to plan 10-04

The response matrix already assigns finite probability to "no counts were registered"; this
curve assigns `1 - P_trig` to "not triggered". Phases 12 and 15 will multiply them. Whether
that double-counts non-detection is **not** answered here — plan 10-04 owes a written verdict
with numbers before anything multiplies them.
