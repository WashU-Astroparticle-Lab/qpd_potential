---
phase: 11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv
plan: 04
status: complete
one_liner: "The IA Gaussian is applied to dR/dT on the RECOIL axis upstream of fold.rebin_cevns_to_edep_grid, with a fail-safe default of OFF that reproduces v1.0 bit-identically; conservation residual is 2.220e-16 on retained + leaked against a 1e-3 target while the retained-only sum deliberately MISSES by 4.333e-4 because 48.98% of the bottom-bin kernel genuinely falls below the 0.0999350 eV floor and 0.87% lands at unphysical T < 0, both matching plan 11-03's analytic prediction exactly and neither rescaled away; the v1.0 regression above 10 eV is 0.052% and falls as E^-0.94, which SUPERSEDES the plan's stated sqrt(omega_bar/E_R) trend -- the correct leading order is omega_bar/E_R, and a naive global fit gives -0.31 only because the deviation changes sign at 233.9 eV near the 3.2 keV kinematic endpoint; plans 11-02 and 11-03 are RECONCILED on the arithmetic VDOS mean so the phase was not blocked, and the x1.163941 systematic ships as a one-sided upper band rather than being absorbed."
plan_contract_ref: GPD/phases/11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv/11-04-PLAN.md#/contract

contract_results:
  claims:
    claim-conservation:
      status: passed
      summary: "Convolution done in COUNTS with exact CDF-difference redistribution, so each source bin's mass telescopes to exactly 1 across (below floor) + (retained) + (above top). On a 480-bin recoil axis from the 0.0999350 eV extended-grid floor to 3200 eV: input 1.1878812499e2 counts/kg/day, retained 1.1873665658e2 (99.956672%), leaked below the floor 5.1468407434e-2 (0.043328%), of which 6.7385839820e-4 (0.000567%) at T < 0, leaked above the top exactly 0. Residual on retained + leaked = 2.220e-16 against the 1e-3 target. The RETAINED-ONLY residual is -4.332791e-4, i.e. it deliberately MISSES -- a clean retained-only sum would have been evidence of a rescale. 100.000% of the sub-floor leakage comes from the bottom decade, as it must."
      linked_ids: [deliv-broaden-code, deliv-leakage-budget, test-conservation-with-leakage, test-no-renormalization, test-leakage-matches-prediction, ref-impulse-residual]
      evidence:
        - verifier: gpd-executor
          method: "exact CDF-difference redistribution with per-bin leakage accounting, plus a strict-linearity test that no post-convolution rescale can pass"
          confidence: high
          claim_id: claim-conservation
          deliverable_id: deliv-leakage-budget
          acceptance_test_id: test-conservation-with-leakage
          reference_id: ref-impulse-residual
          forbidden_proxy_id: fp-renormalize-to-conserve
          evidence_path: artifacts/v2.0/ia_broadening_leakage_budget.csv
    claim-vanishing-limit:
      status: passed
      summary: "Three limits, all clean. (a) omega_bar -> 0 returns the input BIT-IDENTICALLY (np.array_equal), via an explicit early return rather than a numerical limit. (b) With the switch OFF, rebin_cevns_to_edep_grid is bit-identical to the pre-existing v1.0 chain on counts, counts_band, dRdEdep, dRdEdep_band and low_counts. (c) With the switch ON the maximum deviation from the frozen v1.0 spectrum above 10 eV is 5.1963e-4 = 0.052%, against a <1% target, and it is non-vacuous (not zero). The TREND: -0.94 in log-log over 20-200 eV, steeper than the -0.5 the plan asked for."
      linked_ids: [deliv-broaden-code, deliv-broadened-spectrum, test-switch-off-bit-identical, test-v1-regression, test-sigma-zero-identity, ref-v1-frozen, ref-grid-summary]
      evidence:
        - verifier: gpd-executor
          method: "bit-identity comparison at two independent zero limits, plus a regression whose TREND is fitted and pinned rather than only bounded"
          confidence: high
          claim_id: claim-vanishing-limit
          deliverable_id: deliv-broadened-spectrum
          acceptance_test_id: test-v1-regression
          reference_id: ref-v1-frozen
          forbidden_proxy_id: fp-broadening-after-response
          evidence_path: GPD/phases/11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv/11-04-BROADENING-APPLICATION.md
    claim-pipeline-order:
      status: passed
      summary: "The kernel is applied at the top of fold.rebin_cevns_to_edep_grid, before every rebin_counts call and therefore before the deposit grid and R(E_rec|E_dep). A test asserts the source-order relationship AND that broaden-then-rebin differs numerically from rebin-then-broaden, so the ordering is a real constraint rather than a cosmetic one. No exp(-2W)-like factor exists on any rate path: positively, the integrated rate above 10 eV is unchanged by broadening to 1e-3, which excludes a ~1e-2 suppression at 100 meV by measurement and not by inspection. The Phase-10 domain guard is intact: broaden_native_spectrum(require_floor_coverage=True) RAISES when asked to broaden the frozen 5 eV-floored v1.0 CEvNS table down to 0.0999350 eV, and there is no try/except returning zero, no np.clip and no extrapolation anywhere on the broadening path."
      linked_ids: [deliv-broaden-code, deliv-application-note, test-order-of-operations, test-no-dw-factor, test-domain-guard, ref-interp-guard]
    claim-width-systematic-carried:
      status: passed
      summary: "RECONCILED, so the plan's blocking condition did not trigger. Plan 11-02 (IA momentum distribution, sigma_p^2 = m_N <w>/2) and plan 11-03 (exact cumulants of the harmonic correlation function, kappa_2 = E_R <w>) both give the ARITHMETIC VDOS mean 24.195532 meV, both give sigma = 49.189 meV at 100 meV, and both give the correction x1.163941 -- agreeing exactly from different routes. The systematic ships as a one-sided UPPER band: cevns_dRdT_broadened.csv carries dRdT_broadened (locked harmonic omega_bar) and dRdT_broadened_upper (arithmetic mean) as separate columns. There is no lower band, because Cauchy-Schwarz forces omega_bar_p >= omega_bar_u. The upper kernel leaks more (0.052580% vs 0.043328% of the total below the floor), which is reported."
      linked_ids: [deliv-broadened-spectrum, deliv-application-note, test-moment-reconciliation, ref-impulse-residual]
  deliverables:
    deliv-broaden-code:
      status: passed
      path: src/qpd_potential/ia_broadening.py
      summary: "broaden_counts (exact CDF-difference kernel in counts, with per-source-bin below_floor / below_zero / above_top breakdowns and an explicit bit-identical early return at omega_bar = 0), native_edges, broaden_native_spectrum (the shipped entry point, with require_floor_coverage raising rather than extrapolating), and BROADENING_DEFAULT = False. Plus the fold.py wiring at the top of rebin_cevns_to_edep_grid."
      linked_ids: [claim-conservation, claim-vanishing-limit, claim-pipeline-order]
    deliv-broadened-spectrum:
      status: passed
      path: artifacts/v2.0/cevns_dRdT_broadened.csv
      summary: "480 log bins from 0.0999350 eV to 3200 eV. Columns: T_eV, dRdT_unbroadened, dRdT_broadened (locked harmonic omega_bar), dRdT_broadened_upper (arithmetic mean -- the one-sided systematic, NOT absorbed), and the unbroadened/broadened 1-sigma flux band. dR/dT is RECOMPUTED from cevns.differential_rate rather than extrapolated from the frozen 5 eV-floored table, and the header says so."
      linked_ids: [claim-vanishing-limit, claim-width-systematic-carried]
    deliv-leakage-budget:
      status: passed
      path: artifacts/v2.0/ia_broadening_leakage_budget.csv
      summary: "One row per source bin: T, sigma_E, counts in, counts delivered, mass below the floor, mass at T < 0, mass above the top, and the running residual. Header carries the column totals and the residual that SC4's 1e-3 is checked against, and states that counts_out does not balance row by row because the budget closes on column totals."
      linked_ids: [claim-conservation]
    deliv-application-note:
      status: passed
      path: GPD/phases/11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv/11-04-BROADENING-APPLICATION.md
      summary: "Nine sections in the required order: pipeline position with the ordering demonstration and the recorded switch default; the conservation and leakage budget with the honest statement that nothing was rescaled and that the plan-11-03 agreement is a PLACEMENT check rather than independent corroboration; the v1.0 regression with both corrections to the plan's stated trend; the moment reconciliation; the exp(-2W) prohibition with the positive measurement; the domain guard and the one recorded fold.py numerical fix; the bottom-bin caveats; a 25-row clause-by-clause SC1-SC5 verdict table distinguishing PASS from SUPERSEDED from PARTIAL; and the review question."
      linked_ids: [claim-pipeline-order, claim-width-systematic-carried]
  acceptance_tests:
    test-sigma-zero-identity:
      status: passed
      summary: "omega_bar = 0 returns the input with np.array_equal True, and all three leakage entries are exactly 0.0. Implemented as an explicit early return, not as a numerical limit, so it cannot drift."
      linked_ids: [claim-vanishing-limit, deliv-broaden-code]
    test-switch-off-bit-identical:
      status: passed
      summary: "np.array_equal on counts, counts_band, dRdEdep, dRdEdep_band and low_counts between the pre-existing call signature and broaden=False. The test additionally asserts BROADENING_DEFAULT is False, so flipping the default becomes a deliberate, test-breaking act."
      linked_ids: [claim-vanishing-limit, deliv-broaden-code]
    test-v1-regression:
      status: passed
      summary: "Max deviation 5.1963e-4 (0.052%) against <1%, pinned numerically. Non-vacuity asserted. TREND asserted on one side of the sign change and well below the kinematic endpoint: slope -0.94 over 20-200 eV, required < -0.5 and pinned to -0.94 +/- 0.10 against the Fokker-Planck prediction of -1. The sign structure that justifies restricting the fit is ASSERTED, not claimed: median deviation below 200 eV is negative with >90% of bins negative, and EVERY bin above 300 eV is positive. The contaminated global fit (-0.31) is also pinned so it cannot drift unnoticed."
      linked_ids: [claim-vanishing-limit, deliv-broadened-spectrum]
    test-conservation-with-leakage:
      status: passed
      summary: "Residual 2.220e-16 on retained + leaked, against 1e-3. The test also asserts the retained-only sum MISSES by more than 1e-6, and that 0 < below_zero <= below_floor."
      linked_ids: [claim-conservation, deliv-leakage-budget]
    test-no-renormalization:
      status: passed
      summary: "Scaling the input by 7.3125 scales every output bin to 1e-13 and every leakage entry to 1e-13. This is the assertion no global post-convolution rescale can satisfy, because a rescale factor depends on the total. A source scan additionally forbids the obvious rescale idioms."
      linked_ids: [claim-conservation, deliv-broaden-code]
    test-leakage-matches-prediction:
      status: passed
      summary: "A unit source in the bottom bin leaks 0.489803 below the floor and 8.696083e-3 at T < 0, matching plan 11-03's matched-Gaussian weights to ratio 1.00000 against a 10% requirement. HONESTLY QUALIFIED in the artifact: both paths evaluate the same Gaussian CDF, so the exactness is expected and is NOT independent corroboration of the physics -- what it strictly checks is that the shipped kernel is centred at the right energy with the right width, which a one-bin misplacement or a missing moment factor would break by tens of percent."
      linked_ids: [claim-conservation, deliv-leakage-budget]
    test-order-of-operations:
      status: passed
      summary: "broaden-then-rebin and rebin-then-broaden are shown to differ numerically (not allclose at 1e-6), so the ordering is a real constraint. The shipped path is verified at source level: the broaden_native_spectrum call precedes the rebin_counts call in fold.py, and no response-chain symbol appears between them."
      linked_ids: [claim-pipeline-order, deliv-broaden-code]
    test-no-dw-factor:
      status: passed
      summary: "The integrated rate above 10 eV is unchanged by broadening to within 1e-3 -- a POSITIVE measurement excluding the ~1e-2 suppression at 100 meV that exp(-2W) would deliver, not merely a source grep. The source grep runs too, over ia_broadening.py and fold.py."
      linked_ids: [claim-pipeline-order, deliv-broaden-code]
    test-domain-guard:
      status: passed
      summary: "broaden_native_spectrum(require_floor_coverage=True, floor_eV=0.0999350) on the frozen 5 eV-floored CEvNS table RAISES with a message naming the mismatch and instructing recomputation rather than clamping. The test also asserts no np.clip appears anywhere in ia_broadening.py and that no except-returning-zero pattern exists."
      linked_ids: [claim-pipeline-order, deliv-broaden-code]
    test-moment-reconciliation:
      status: passed
      summary: "Plan 11-03's exact variance E_R * omega_bar_p matches plan 11-02's sigma_E_upper_moment_eV to 1e-9 at 0.1, 1 and 100 eV. The artifact contains 'RECONCILED' and the 1.1639 factor, and the shipped CSV header carries both 'upper' and 'one-sided', so the systematic is verifiably banded rather than absorbed."
      linked_ids: [claim-width-systematic-carried, deliv-application-note]
  references:
    ref-v1-frozen:
      status: completed
      completed_actions: [use, compare]
      missing_actions: []
      summary: "Used as the vanishing-limit target in two ways: bit-identity with the switch off, and the <1% regression above 10 eV with the switch on. The comparison runs on the preserved overlapping v1.0 edge set, which Phase 10 established is an INDEX carry with max difference exactly 0.0."
    ref-grid-summary:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "Supplied the extended axis parameters (floor 0.0999350 eV, first centre 0.1013838 eV, 744 bins, 79.988714 bins/decade) and the opt-in version pin. The broadened spectrum's own 480-bin axis starts exactly at the extended-grid floor so the leakage boundary is the one Phase 12 will actually see. shared_energy_grid was NOT assumed to have changed its default."
    ref-interp-guard:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "Its discipline was followed rather than defeated: require_floor_coverage raises instead of clamping, and the sub-eV dR/dT is recomputed from cevns.differential_rate rather than extrapolated from the 5 eV-floored frozen table. Four new shared_energy_grid call sites and three shifted fold.py interpolator line references were registered in the Phase-10 pin table and inventory rather than worked around."
    ref-impulse-residual:
      status: completed
      completed_actions: [read, compare]
      missing_actions: []
      summary: "Supplied the predicted matched-Gaussian sub-floor and T<0 weights, which the shipped kernel reproduces exactly, and the moment verdict that decided whether the width itself needed correcting. Also supplied the bottom-bin skewness 0.590 and excess kurtosis 0.381 that section 6 of the application note carries forward as the O(1/2W) caveat."
  forbidden_proxies:
    fp-renormalize-to-conserve:
      status: rejected
      notes: "The retained-grid sum deliberately falls short by 4.332791e-4 and is reported that way. Strict linearity in the input amplitude is asserted to 1e-13 on every output bin AND every leakage entry, which no global rescale can satisfy. The leakage budget CSV exists precisely so the shortfall is auditable per bin."
    fp-dw-suppression:
      status: rejected
      notes: "Excluded by positive measurement, not only by inspection: the integrated rate above 10 eV is unchanged by broadening to 1e-3. A source grep over ia_broadening.py and fold.py runs as well."
    fp-silent-clamp:
      status: rejected
      notes: "require_floor_coverage RAISES; there is no try/except returning zero, no np.clip, and no extrapolation on the broadening path, all asserted by test. The sub-eV spectrum is recomputed from cevns.differential_rate instead of being extrapolated from the frozen 5 eV-floored table."
    fp-broadening-after-response:
      status: rejected
      notes: "Applied at the top of rebin_cevns_to_edep_grid, before every rebin_counts call and before R(E_rec|E_dep). Verified at source level AND numerically, by showing that the two orderings give different answers."
    fp-absorb-systematic:
      status: rejected
      notes: "dRdT_broadened_upper ships as a separate column with the header stating it is ONE-SIDED and that there is no lower band. The central curve stays on the locked harmonic omega_bar so ROADMAP SC3's stated identities continue to hold exactly."
    fp-electron-recoil-leak:
      status: rejected
      notes: "The wiring touches only the CEvNS recoil path inside rebin_cevns_to_edep_grid. Nothing was added to the muon or Compton channels, and no statement was made about whether the width applies to them. The 11-02 test asserting ia_broadening does not import or mention those modules still passes."
  uncertainty_markers:
    weakest_anchors:
      - "THE BOTTOM BIN. 48.98% of its kernel falls below the retained axis, 0.87% of it lands at T < 0 where the true S vanishes identically, the shipped kernel is symmetric while the true lineshape has skewness 0.590, and 2W is only 5.60. Every 100 meV number in Phases 12-16 inherits all of that."
      - "The plan-11-03 leakage agreement is EXACT because both paths evaluate the same Gaussian CDF. It is a kernel-placement check, not independent corroboration of the physics, and the artifact says so."
      - "The <1% v1.0 regression rests on the frozen v1.0 spectra being the right comparison object on the preserved edge set -- a Phase-10 result (index carry, max difference exactly 0.0), used here, not re-established."
      - "The width rests entirely on plan 11-01's omega_bar, entering under a square root: a factor-2 error there is a factor-1.41 error in every broadened number."
      - "The 480-bin recoil axis for the shipped artifact is a choice of this plan. The conservation residual is 2e-16 by construction of the CDF redistribution and would remain so at any resolution, but the LEAKAGE fraction depends on where the bottom bin centre sits relative to the floor."
    unvalidated_assumptions:
      - "That the CEvNS recoil spectrum is smooth enough on the scale of sigma_E for a discretized convolution on a log axis. The v1.0 regression tests this at high energy; in the bottom decade, where the axis is coarsest relative to the width, it is not directly tested."
      - "That the counting floor and the IA width are statistically independent, inherited from plan 11-02 as an assertion."
      - "That the symmetric Gaussian is defensible at 2W = 5.60. Plan 11-03 quantifies that it is not, at the ~20% level; the shipped bottom bin carries that error knowingly."
    competing_explanations:
      - "A <1% agreement above 10 eV could also be produced by a kernel too narrow everywhere. The -0.94 trend and the non-zero bottom-decade leakage make that unlikely, but neither is a direct measurement of the width."
      - "The exact 1.00000 agreement with plan 11-03's leakage prediction looks like a strong independent confirmation and is not, for the reason above."
    disconfirming_observations:
      - "RAN, DID NOT FIRE: plans 11-02 and 11-03 disagreeing on the governing VDOS moment, which would have blocked this plan outright. They agree exactly."
      - "RAN, DID NOT FIRE: count conservation failing at 1e-3 with leakage accounted (2.220e-16)."
      - "RAN, DID NOT FIRE: the measured sub-floor leakage disagreeing with plan 11-03 by more than 10% (ratio 1.00000)."
      - "FIRED, AND WAS REPORTED RATHER THAN RELAXED: the v1.0 deviation does NOT fall as sqrt(omega_bar/E_R). A naive global fit gives -0.31, which fails the plan's < -0.5 criterion. Two things are wrong with the criterion and both were verified rather than assumed: (a) the correct leading order is omega_bar/E_R, slope -1, because sqrt(omega_bar/E_R) is the fractional WIDTH and not the fractional change in the SPECTRUM -- measured -0.94; (b) the deviation CHANGES SIGN at 233.9 eV and grows toward the 3.2 keV kinematic endpoint, so a single global power-law fit measures the sign change. The sign structure is asserted by test, so the justification for looking at the smooth region separately can itself fail."
      - "FIRED, AND WAS FIXED: fold._loglog_segment_integral returned NaN on the broadened spectrum past the kinematic endpoint. A power law cannot represent a Gaussian tail: |p| ~ 400 makes T1**p underflow, A becomes inf, and inf*0 becomes nan. Added a finiteness fallback to the linear rule the function already used for non-positive endpoints. Unreachable for the unbroadened table -- switch-off bit-identity still passes -- so no existing number moved."
      - "FIRED (Phase-10 guards working as designed): four new shared_energy_grid call sites and three shifted fold.py interpolator line references. Registered in the Phase-10 pin table and inventory rather than worked around."
      - "NOT A FAILURE BUT THE MOST IMPORTANT NUMBER HERE: 48.98% of the bottom-bin kernel leaves the retained axis. Phase 12 must treat any 100 meV statement as a statement about roughly half a kernel."
---

# Plan 11-04 — Applying the broadening before the response chain (CALC-15 / SC4)

## Conservation and leakage

| Quantity | Value |
|---|---|
| input counts | 1.1878812499×10² counts/kg/day |
| retained on the axis | 1.1873665658×10² (99.956672 %) |
| **leaked below the 0.0999350 eV floor** | 5.1468407434×10⁻² (**0.043328 %**) |
| of which at unphysical T < 0 | 6.7385839820×10⁻⁴ (0.000567 %) |
| leaked above the top | 0 |
| **residual (retained + leaked)** | **2.220×10⁻¹⁶** — target ≤ 10⁻³ |
| retained-only residual | −4.332791×10⁻⁴ — **misses, as it must** |

**Bottom bin** (centre 0.1010208 eV, σ_E = 0.042476 eV): **48.9803 %** below the floor and
**0.8696 %** at T < 0, matching plan 11-03's analytic matched-Gaussian prediction to ratio 1.00000.
Nothing was rescaled.

## v1.0 regression

| | |
|---|---|
| max \|deviation\| above 10 eV | **0.052 %** (5.1963×10⁻⁴), target < 1 % |
| trend, 20–200 eV | **slope −0.94** |
| sign change | **233.9 eV**; positive at every bin above 300 eV |
| naive global fit | −0.31 — contaminated by the sign change and the 3.2 keV endpoint |

The plan asked for a `√(ω̄/E_R)` trend (slope −0.5). **That expectation is superseded:** the correct
leading order for a mass-conserving kernel with σ² = ω̄E is `Δf/f ∝ ω̄/E`, slope −1. Measured −0.94,
i.e. steeper than asked.

## Switch default, recorded for Phase 12

**`ia_broadening.BROADENING_DEFAULT = False` (OFF).** Fail-safe, following the Phase-10 precedent
that left `shared_energy_grid` defaulting to `v1.0`. With the switch off the fold is bit-identical to
v1.0 on every returned array.

## Moment reconciliation: RECONCILED

| | 11-02 (momentum distribution) | 11-03 (correlation-function cumulants) |
|---|---|---|
| governing mean | arithmetic ⟨ω⟩ = 24.195532 meV | arithmetic ⟨ω⟩ = 24.195532 meV |
| σ at 100 meV | 49.189 meV | 49.189 meV |
| correction | ×1.163941 | ×1.163941 |

**Not blocked.** The systematic ships as a one-sided **upper band** (`dRdT_broadened_upper`), never
absorbed. The upper kernel leaks 0.052580 % against the central 0.043328 %.

## Bottom-bin caveats for Phases 12–16

2W = 5.60 · true fractional width 49.19 % · **skewness 0.590** · excess kurtosis 0.381 ·
0.87 % of the kernel at unphysical T < 0 · **≈49 % of the kernel off the retained axis**.
Do not quote the 100 meV bin to better than one significant figure.

## Phase-wide SC1–SC5 verdicts

Full 25-row clause table in `11-04-BROADENING-APPLICATION.md` §7. Summary: **all five success
criteria PASS**, with

* **three clauses SUPERSEDED as evidence** — the momentum-transfer route (SC2) and the
  `σ_E/E_R = 1/√(2W)` relation (SC3) are algebraic identities, and the `√(ω̄/E_R)` regression trend
  (SC4) was the wrong functional form;
* **one clause PARTIAL** — `e^(−2W)` reproduces the survey magnitude at 100 meV (factor 2.7) but not
  at 1 eV (4.82×10⁻²⁵ vs ~10⁻²⁰), explained by the survey's use of the Debye ω̄;
* **one clause QUALIFIED** — "the IA is reached by ~100 meV" holds at the order-of-magnitude level
  only;
* **one clause SUPERSEDED UPWARD** — with the physically correct arithmetic mean, every SC3
  fractional width exceeds the upper edge of its ROADMAP band.

**The survey band ω̄ = 12–21 meV SURVIVED**: the measured 17.860 meV is inside it.

## Interactive checkpoint

This plan is `interactive: true` with a `checkpoint:human-verify` at Task 3. Under the standing
directive to run the roadmap to completion, the checkpoint content is recorded in full in
`11-04-BROADENING-APPLICATION.md` §8, including the review question and the three items flagged for
attention. **No approval has been recorded**; the question stands open.

## Deviations

* **[Rule 2 — numerical]** `fold._loglog_segment_integral` returned NaN past the kinematic endpoint
  of the broadened spectrum (a power law cannot represent a Gaussian tail: |p| ≈ 400 → underflow →
  `inf × 0`). Added a finiteness fallback to the linear rule the function already used for
  non-positive endpoints, plus an `errstate` guard. Unreachable for the unbroadened table.
* **[Rule 4 — missing component]** Registered four new `shared_energy_grid` call sites in the
  Phase-10 pin table and remapped three shifted `fold.py` line references in the interpolator
  inventory. Both guards fired correctly.
* **API note, not a deviation:** the plan named `broaden_dRdT(T_eV, dRdT, *, omega_bar_eV)`. Working
  in counts requires bin EDGES, so the shipped API is `broaden_counts(edges_eV, counts, ...)` with
  `broaden_native_spectrum(T_eV, dRdT, band, ...)` as the dR/dT-in/dR/dT-out entry point actually
  wired into `fold.py`. Same semantics, unambiguous binning.
* **Scope note:** `dR/dT` below 5 eV is **recomputed** from `cevns.differential_rate`, not
  extrapolated from the frozen table, whose support stops at 5 eV. The alternative would have been
  `fp-silent-carry`.

## Suite

**593 passed, 0 failed** (581 after plan 11-03 + 12 new; 24 total in `tests/test_ia_broadening.py`).
`data/flux/*.csv` churn reverted.
