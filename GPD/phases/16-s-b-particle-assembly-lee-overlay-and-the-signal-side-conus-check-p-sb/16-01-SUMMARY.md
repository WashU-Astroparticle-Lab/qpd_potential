---
phase: 16-s-b-particle-assembly-lee-overlay-and-the-signal-side-conus-check-p-sb
plan: 01
title: "VALD-12 signal-side leg: PARTIALLY CONFIRMED and WINDOW-CONDITIONAL. The pre-registered 0.4-1 keV_ee window FAILS by 3.28 decades; the declared 160 eV_ee alternate passes at central quenching; the ratio spans 4.504 decades across candidates and 65% of the pre-registered window lies above our own kinematic endpoint."
date: 2026-07-23
status: complete
depth: full
completed: 2026-07-23
provides:
  - "src/qpd_potential/conus_check.py -- NEW module (no file:line inventory key moved); pre-registered window and pre-declared factor as module constants ABOVE the integrator; BRACKETED Lindhard window-boundary map; kinematic-support measurement; window integral with the 1/1000 written out"
  - "artifacts/v2.0/conus_window_sensitivity.csv -- 9 rows, the FULL ratio-versus-window curve INCLUDING the failures and the three above-endpoint zeros"
  - "artifacts/v2.0/conus_signal_side_check.csv -- the determination with the restatement cost, the geometric rescale factor by factor, the measured IA omission, and the Billard-route leverage measurement"
  - "tests/test_conus_signal_side.py -- 9 tests covering all 9 contract acceptance tests"
  - "GPD/phases/16-.../16-01-CONUS-SIGNAL-SIDE.md -- the VALD-12 determination, the restatement cost, the checkpoint recorded in full, and three findings flagged for the orchestrator"
  - "artifacts/v2.0/legacy_grid_disposition.csv -- disposition rows for the two new tracked artifacts (73 register rows)"
  - "GPD/phases/10-.../10-01-INTERPOLATOR-INVENTORY.md -- one new row registering conus_check.py:218; the closure count bumped 44 -> 45, the only sanctioned response"
one_liner: "VALD-12's restated signal-side leg is discharged as PARTIALLY CONFIRMED and explicitly WINDOW-CONDITIONAL, with the pre-registered leg reported as a FAIL rather than rescued: rescaling the committed recoil-axis CEvNS spectrum by the geometric factor 1.7503325632 (P_c/P_v = 1.2 and (d_v/d_c)^2 = 1.4586104693 written out separately because a product can be right by cancellation) and integrating over the 0.4-1 keV_ee window PRE-REGISTERED from ROADMAP.md/REQUIREMENTS.md gives 5.278664e-04 against CONUS+'s SM expectation 347/327 = 1.0611620795 counts/kg/day, i.e. 3.28 decades short of a factor declared as 2.0 in source BEFORE any ratio existed; the declared 160 eV_ee alternate from GPD/literature/SUMMARY.md gives 8.333761e-01 at central quenching and 4.012535e-01 .. 1.764657e+00 across the Lindhard-k bracket, so this project's own documents give opposite verdicts and the full curve spans 4.504 decades plus three exact zeros; the cause is localized but not dissolved -- the keV_ee -> keV_nr map rests on a quenching model that is BRACKETED and NOT SOURCED because none is frozen in this repository, and only 34.85% of the pre-registered window lies inside the non-zero support of our own dR/dT, whose kinematic endpoint is MEASURED at 3031.6858 eV_nr from the artifact rather than transcribed, so 65% of that window sits where dR/dT is exactly zero and the comparison is structurally unable to test the chain; the independent Billard route agrees on the absolute rate scale to 0.87% (ratio 0.991302) but this report MEASURES how far that reaches instead of leaning on it and finds only 4.722893e-06 of its weight above the pre-registered lower edge and 7.456330e-03 above the alternate's, so it constrains the bulk normalization and says essentially nothing about the 2-5 keV_nr tail; the IA omission is measured rather than asserted small at sigma_E/E_R = 2.904884e-03 and 1.940585e-03 at the two window edges; quenching is proved by AST parse to touch window boundaries only and never a rate array; and the restatement's cost is written on the deliverable -- reproducing CONUS+'s S/B would require modelling their 7.4 m.w.e. shield, so the milestone carries external validation of S/B_particle's NUMERATOR ONLY and none of the ratio, with no background-side target-swap validation at all since VALD-11's deletion and the 407.7 dru CaWO4 closure cited with its provenance gap, neither re-run nor rescaled."
plan_contract_ref: GPD/phases/16-s-b-particle-assembly-lee-overlay-and-the-signal-side-conus-check-p-sb/16-01-PLAN.md#/contract

contract_results:
  claims:
    claim-window-preregistered:
      status: passed
      summary: "The window is declared as a module constant with its source cited in the same statement and placed physically ABOVE the integrator; test_window_preregistered asserts that ordering from the parsed AST rather than trusting it. Both of this project's conflicting statements are carried as named rows -- 0.4-1 keV_ee from ROADMAP.md/REQUIREMENTS.md (PRE_REGISTERED, exactly one row) and 160 eV_ee from GPD/literature/SUMMARY.md (declared alternate) -- plus a 1-2 keV_ee kinematic probe that exists to exercise the above-endpoint flag on real data. The reason for the choice is stated in terms of what the documents ARE (authoritative scoping documents vs a survey), not what they yield, and was committed in source before any integral ran. The keV_ee -> keV_nr map is emitted with the model named and labelled BRACKETED, never SOURCED: no germanium ionization-quenching model is frozen anywhere under data/ and none could be retrieved and integrity-checked here, so k is bracketed over [0.130, 0.200] about the Lindhard analytic 0.157 and both endpoints become extra sensitivity rows."
      linked_ids: [deliv-window-sensitivity, deliv-conus-report, deliv-conus-module, test-window-preregistered, test-window-in-both-scales, test-no-quenching-on-our-spectrum, ref-conus-nature, ref-roadmap-16-sc1, ref-conventions-B, ref-literature-summary]
      evidence:
        - verifier: gpd-executor
          method: "AST assertion that the window constant and the stated factor are declared above both the integrator and the evaluator; exactly-one-PRE_REGISTERED-row assertion on the emitted table; at-least-one-failing-candidate assertion; boundary map re-solved inside the test rather than read back"
          confidence: high
          claim_id: claim-window-preregistered
          deliverable_id: deliv-window-sensitivity
    claim-signal-side-ratio:
      status: passed
      summary: "PRE-REGISTERED WINDOW: ratio 5.278664e-04 against the PRE-DECLARED factor 2.0 -- a FAIL by 3.28 decades, reported as such. DECLARED ALTERNATE: 8.333761e-01 at central k (inside the factor), 4.012535e-01 at bracket-low (outside), 1.764657e+00 at bracket-high (inside). PROBE: three rows at exactly zero, flagged above_kinematic_endpoint. Spread across candidates: 4.504 decades. Every ratio is RECOMPUTED inside the test from the committed recoil table to 1e-6 relative, not transcribed. The kinematic support edge 3031.6858 eV_nr is re-derived in test from the artifact; the support fraction is a column on every row and is 0.3485 for the pre-registered window, so 65% of it sits where dR/dT is exactly zero. IA omission MEASURED at both edges: 2.904884e-03 and 1.940585e-03. Billard-route cross-check recorded either way: ratio 0.991302 (0.87% agreement) -- AND the leverage of that agreement is measured, finding only 4.722893e-06 of its weight above the pre-registered lower edge, which is stated as a limit on what the agreement can support."
      linked_ids: [deliv-conus-table, deliv-conus-report, deliv-conus-tests, deliv-window-sensitivity, test-ratio-against-sm-expectation, test-kinematic-support-checked, test-recoil-axis-only, test-ia-omission-measured, ref-conus-nature, ref-cevns-recoil, ref-conventions-B]
      evidence:
        - verifier: gpd-executor
          method: "independent in-test re-quadrature of every emitted ratio to 1e-6; AST proof that no response/response_matrix/trigger/ia_broadening/fold entry point is imported, called or referenced and that no reconstructed-axis path string appears; support-fraction column asserted non-vacuous in both directions"
          confidence: high
          claim_id: claim-signal-side-ratio
          deliverable_id: deliv-conus-table
    claim-restatement-cost-written:
      status: passed
      summary: "Located in the written report by executed needle checks, not by inspection: the numerator-only sentence; that reproducing CONUS+'s S/B would require modelling their 7.4 m.w.e. shield, which is out of scope, so the background-side leg is a real loss disclosed rather than quietly dropped; that since VALD-11's deletion the milestone has NO background-side target-swap validation at all; the 407.7 dru closure with its word-bounded provenance gap, neither re-run nor rescaled; the 0.4-1 keV_ee versus 160 eV_ee discrepancy flagged for the orchestrator with neither file edited; and an explicit VALD-12 verdict in the Phase-12/13/14 vocabulary with its number and its pre-declared factor. The withdrawn pre-re-scope expectation is asserted absent from every emitted file except inside an explicit withdrawal statement, with the search strings built at runtime."
      linked_ids: [deliv-conus-report, test-restatement-cost-on-deliverable, test-no-withdrawn-expectation, ref-roadmap-16-sc1, ref-phase12-closure]
      evidence:
        - verifier: gpd-executor
          method: "13-needle executed scan over the report plus a runtime-constructed scan for the withdrawn band and the withdrawn comparative claim across the module, both tables, the report and the test file itself"
          confidence: high
          claim_id: claim-restatement-cost-written
          deliverable_id: deliv-conus-report
  deliverables:
    deliv-conus-table:
      status: produced
      path: artifacts/v2.0/conus_signal_side_check.csv
      summary: "9 rows, axis = RECOIL on every one. Header carries the restatement cost, the geometric rescale with P_c, P_v, d_c, d_v and the factor written out individually, the SM expectation as events AND as a rate with the division shown, the measured kinematic support edge, the measured IA fractional widths at both pre-registered edges, the Billard route with its measured leverage, and the verdict with its pre-declared factor. Columns carry both energy scales, the quenching model with its bracket, the support fraction, the above-endpoint flag and the ratio."
      linked_ids: [claim-signal-side-ratio, claim-restatement-cost-written]
    deliv-window-sensitivity:
      status: produced
      path: artifacts/v2.0/conus_window_sensitivity.csv
      summary: "The full ratio-versus-window curve: 3 candidates x 3 Lindhard-k bracket positions = 9 rows, of which 7 FAIL the pre-declared factor and 3 are exact zeros above the kinematic endpoint. Exactly one row flagged PRE_REGISTERED. The header states the measured spread (4.504 decades) and records the ROADMAP/REQUIREMENTS vs literature-survey window discrepancy as a finding for the orchestrator."
      linked_ids: [claim-window-preregistered, claim-signal-side-ratio]
    deliv-conus-report:
      status: produced
      path: GPD/phases/16-s-b-particle-assembly-lee-overlay-and-the-signal-side-conus-check-p-sb/16-01-CONUS-SIGNAL-SIDE.md
      summary: "Ten sections: the verdict first, the pre-registration and the internal discrepancy, the BRACKETED conversion, the measured kinematic support, the integral and rescale, the independent route and how far it reaches, the measured IA omission, the verdict against the backtracking trigger with what is and is not understood, the restatement's cost, the checkpoint recorded in full with no fabricated approval, and three orchestrator flags."
      linked_ids: [claim-window-preregistered, claim-signal-side-ratio, claim-restatement-cost-written]
    deliv-conus-tests:
      status: produced
      path: tests/test_conus_signal_side.py
      summary: "9 tests, one per contract acceptance test, with RECOMPUTE_REL and QUENCH_REL declared as module constants before any check runs. Two tests are AST parses rather than greps, because the words 'quenching' and 'Lindhard' must appear in the module's prose."
      linked_ids: [claim-window-preregistered, claim-signal-side-ratio, claim-restatement-cost-written]
    deliv-conus-module:
      status: produced
      path: src/qpd_potential/conus_check.py
      summary: "A NEW module so that no line number in cevns.py moves and no tests/test_interpolator_bounds.py file:line key shifts. Constants first, integrator second, by construction."
      linked_ids: [claim-window-preregistered, claim-signal-side-ratio]
    deliv-disposition-16-01:
      status: produced
      path: artifacts/v2.0/legacy_grid_disposition.csv
      summary: "Two rows, both not_a_spectrum with written reasons over 40 characters: each row of these tables is a named quantity over a stated analysis window on the RECOIL axis, not a differential rate on any binned axis. Register closure re-runs its own git ls-files enumeration and passes at 73 rows."
      linked_ids: [claim-signal-side-ratio]
  acceptance_tests:
    test-window-preregistered:
      status: passed
      summary: "Exactly one PRE_REGISTERED row; the window constant and the stated factor both asserted (by AST line number) to be declared above the integrator AND above the evaluator; 7 of 9 candidates FAIL the factor so the curve is not a set of passing points; both document candidates present as named rows; the discrepancy located in the artifact header as a flagged finding."
      linked_ids: [claim-window-preregistered, deliv-window-sensitivity, deliv-conus-module]
    test-window-in-both-scales:
      status: passed
      summary: "Both scales on every row of both tables; quenching model named and provenance asserted BRACKETED; bracket endpoints ordered; E_ee < E_nr strictly and Q in (0,1) strictly on every row; the boundary map and Q re-solved inside the test to 1e-9 rather than read back."
      linked_ids: [claim-window-preregistered, deliv-window-sensitivity, deliv-conus-table]
    test-no-quenching-on-our-spectrum:
      status: passed
      summary: "AST scan, not grep. Non-vacuity asserted three ways: the quenching function is defined, is called, and is called inside the window-boundary map. Every name bound from the quenching call is asserted to be a boundary name; no Mult or Div anywhere pairs such a name with a rate-array name; no rate-array name is ever passed as an argument to the quenching function."
      linked_ids: [claim-window-preregistered, deliv-conus-module, deliv-conus-tests]
    test-ratio-against-sm-expectation:
      status: passed
      summary: "Every emitted ratio reproduced by an independent in-test quadrature to 1e-6 relative; the geometric factor reproduced to 1e-12 from params; the stated factor asserted equal to the module constant on every row; the verdict asserted present in the artifact header together with the sentence that the pre-registered leg itself is a FAIL."
      linked_ids: [claim-signal-side-ratio, deliv-conus-table, deliv-conus-tests]
    test-kinematic-support-checked:
      status: passed
      summary: "Support-fraction column present and in [0,1] on every row of both tables; the support edge 3031.6858 eV_nr re-derived in test from the artifact to 1e-15 and asserted present in the report; a window whose lower edge is above the edge asserted to carry the flag AND a zero rate; two non-vacuity assertions -- at least one candidate above the endpoint and at least one partially outside it."
      linked_ids: [claim-signal-side-ratio, deliv-conus-table, deliv-window-sensitivity, deliv-conus-report]
    test-recoil-axis-only:
      status: passed
      summary: "AST scan asserts response, response_matrix, trigger, ia_broadening and fold are neither imported nor referenced as attributes, and that no string constant contains a _dRdErec_ or response_matrix_ path. axis == RECOIL asserted on every emitted row of both tables."
      linked_ids: [claim-signal-side-ratio, deliv-conus-module, deliv-conus-table, deliv-conus-tests]
    test-ia-omission-measured:
      status: passed
      summary: "sigma_E/E_R recomputed in test from the CONVENTIONS Section J locked omega_bar and asserted equal to the emitted values to 1e-12; both numbers asserted present in the artifact header AND in the report; the report asserted to say the omission is not asserted small."
      linked_ids: [claim-signal-side-ratio, deliv-conus-report, deliv-conus-table]
    test-restatement-cost-on-deliverable:
      status: passed
      summary: "13 needles located in the report by an executed scan, including the numerator-only sentence, the shield-modelling reason, 7.4 m.w.e., VALD-11, the absent background-side target-swap validation, 407.7, word-bounded, neither re-run nor rescaled, both windows, the orchestrator flag and VALD-12. The verdict, its ratio to six significant figures and the pre-declared factor are all asserted present, together with the checkpoint marker and the no-fabricated-approval statement."
      linked_ids: [claim-restatement-cost-written, deliv-conus-report]
    test-no-withdrawn-expectation:
      status: passed
      summary: "Zero occurrences outside an explicit withdrawal statement across the module, both tables, the report and the test file itself. The forbidden band and the forbidden comparative phrase are both assembled at runtime so the test file does not carry them as bare text."
      linked_ids: [claim-restatement-cost-written, deliv-conus-report, deliv-conus-table, deliv-conus-tests]
  references:
    ref-conus-nature:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "CONUS+ Collab., Nature 643, 1229 (2025), arXiv:2501.05206. The SM expectation 347 +/- 59 in 327 kg.d is carried as events AND divided to a rate with the division shown; the observed 395 +/- 106 at 3.7 sigma is cited; their measured S/B ~ 0.03 is recorded as CONTEXT for a shielded experiment and explicitly not as a gate and not as a target. Every number is a citation: no CONUS+ ancillary data exists to download and none was invented."
    ref-cevns-recoil:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "artifacts/v2.0/cevns_dRdT_ext.csv read directly and integrated. Its non-zero support edge, MEASURED at 3031.6858 eV_nr rather than taken from the table's last abscissa 3165.6057, IS the kinematic endpoint that decides whether the converted window is reachable -- and it is not, for 65% of the pre-registered window."
    ref-roadmap-16-sc1:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "SC1's restatement, its requirement that the cost be written on the deliverable, and its backtracking trigger are all discharged in the report Section 7, which states what is understood about the failure and, separately, what is not. ROADMAP.md was NOT edited; the window discrepancy it participates in is flagged instead."
    ref-conventions-B:
      status: completed
      completed_actions: [read, use, avoid]
      missing_actions: []
      summary: "The single unified phonon scale with no ionization quenching is what makes converting THEIR window legal and converting OUR spectrum forbidden. The avoid action is discharged by AST parse, not by prose."
    ref-literature-summary:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "The other side of the window discrepancy: the 160 eV_ee / 7.4 m.w.e. limiting case, carried as a named alternate row rather than discarded, and the record that no CONUS/CONUS+ arXiv entry carries ancillary data, which is why the quenching model is BRACKETED."
    ref-phase12-closure:
      status: completed
      completed_actions: [read, cite, avoid]
      missing_actions: []
      summary: "Carried forward verbatim in intent: the milestone has NO background-side target-swap validation since VALD-11's deletion, and the 407.7 dru CaWO4 closure exists only in GPD prose under a word-bounded search. It is cited with its provenance gap and is neither re-run nor rescaled -- the avoid action."
  forbidden_proxies:
    fp-window-tuned-to-pass:
      status: rejected
      notes: "The window and the factor are module constants declared above the integrator and the ordering is asserted from the parsed AST. The FULL curve is emitted with 7 of 9 candidates failing. The pre-registered leg is reported as a FAIL rather than replaced by the passing alternate, and the alternate's own bracket-low row is reported as failing too."
    fp-quenching-on-phonon-scale:
      status: rejected
      notes: "Proved by AST parse: every name bound from the quenching call is a boundary name, no Mult/Div pairs one with a rate array, and no rate array is ever an argument to it. The scan is shown non-vacuous three ways."
    fp-reconstructed-axis-comparison:
      status: rejected
      notes: "AST scan finds zero imports, attribute references or path strings for response, response_matrix, trigger, ia_broadening or fold. axis = RECOIL on every emitted row."
    fp-silent-endpoint-truncation:
      status: rejected
      notes: "Support fraction is a column on every row; the above-endpoint candidate records a ZERO rate with an explicit flag; no table was extended to make any window reachable. The test asserts a candidate exists in each state, so the guard cannot pass vacuously."
    fp-restatement-as-equivalent:
      status: rejected
      notes: "The report states in Section 0 that the pre-registered leg is a FAIL, and in Section 8 that the milestone carries external validation of the numerator only and none of the ratio. Section 5 additionally measures how far the one independent cross-check reaches and states that it does not reach the window."
  uncertainty_markers:
    weakest_anchors:
      - "The analysis window itself. This project's own documents disagree (0.4-1 keV_ee in ROADMAP.md/REQUIREMENTS.md; 160 eV_ee in GPD/literature/SUMMARY.md) and the two give opposite verdicts. The measured spread across candidates is 4.504 decades -- larger than everything else in this plan combined."
      - "The germanium ionization-quenching model, which is BRACKETED and NOT SOURCED because none is frozen in this repository. It enters only as a coordinate change on CONUS+'s axis, but the coordinate change is where the decades live: within the pre-registered window alone the bracket moves the ratio by a factor 97."
      - "The reactor antineutrino flux above ~8 MeV, which sets the 2-5 keV_nr tail the pre-registered window probes. The one independent handle available carries under 5e-06 of its weight there, so it does not constrain this region at all."
      - "The assumption of a common antineutrino spectral shape at 3 GW_th / 25 m and at CONUS+'s Leibstadt core. Fission-fraction differences are not modelled and are not quantifiable with what this project holds; recorded as a named, unquantified systematic rather than folded in as a guess."
      - "The 407.7 dru CaWO4 closure, cited here as the only prior signal-side target-swap validation, which has no reproducible artifact in this repository under a word-bounded search."
    unvalidated_assumptions:
      - "That a point-source 1/d^2 rescale with a common spectral shape is adequate between the two sites."
      - "That CONUS+'s quoted SM expectation uses a form factor and radius compatible with our Freedman + Helm implementation. If it does not, part of any residual is theirs and not ours, and nothing here could distinguish the two."
      - "That omitting IA broadening is right for this comparison because their SM expectation contains no such kernel. The size of the omission is measured (2.9e-03 and 1.9e-03 fractional width); the CHOICE remains an argument."
      - "That the Lindhard-Robinson form with a k bracket is the right family for a sub-keV germanium ionization yield. The form is written down so it can be challenged; it is not read from a frozen artifact."
    competing_explanations:
      - "The pre-registered leg failing could mean our flux x cross-section x target chain is wrong at 2-5 keV_nr, OR that the window as this project states it is not CONUS+'s window, OR that the quenching bracket is misplaced. The three are partially separated by the support-fraction column and by the alternate window passing, but they are NOT fully separated, and the report says so."
      - "The 0.87% Billard agreement could mean the chain is validated, OR that it is validated only where its weight is -- below ~1 keV_nr. MEASURED: 4.7e-06 of its weight sits above the pre-registered lower edge, so the second reading is the correct one."
      - "The alternate window passing could mean it is the right window, OR that a 4.5-decade-wide family of candidates will contain a passing one by construction. Separated only in part: the alternate was DECLARED before the integral and its own bracket-low row fails."
    disconfirming_observations:
      - "The pre-registered ratio landed 3.28 decades below the pre-declared factor. Under the ROADMAP backtracking trigger this forbids treating VALD-12 as discharged on its pre-registered window, and that is how it is reported."
      - "65% of the pre-registered window lies ABOVE the non-zero support of our own dR/dT. The check as specified therefore cannot test the chain it was written to test over most of its range."
      - "The two candidate windows in this project's own documents give OPPOSITE verdicts, so VALD-12's verdict is window-dominated and is reported as conditional on a window this project cannot settle."
      - "The IA fractional widths came out SMALL (2.9e-03, 1.9e-03) rather than large. Recorded as measured; this is the one place where the expected-small answer survived checking, and it is reported as such rather than as a general licence."
---

# Plan 16-01 Summary — VALD-12 Signal-Side Leg

## Result

**VALD-12 (signal-side leg) = PARTIALLY CONFIRMED, and explicitly WINDOW-CONDITIONAL.**

| quantity | value |
|---|---|
| pre-registered window | 0.4-1 keV_ee (`ROADMAP.md`, `REQUIREMENTS.md`) |
| pre-declared factor | **2.0**, declared in source above the integrator |
| pre-registered ratio | **5.278664e-04** — a **FAIL**, short by 3.28 decades |
| declared alternate | 160 eV_ee (`GPD/literature/SUMMARY.md`) |
| alternate ratio, central k | **8.333761e-01** — inside the factor |
| alternate ratio, k bracket | 4.012535e-01 … 1.764657e+00 (one of three fails) |
| spread across candidates | **4.504 decades**, plus 3 exact zeros |
| kinematic support edge (measured) | **3031.6858 eV_nr** |
| pre-registered window support fraction | **0.3485** — 65 % is above the endpoint |
| geometric rescale | 1.7503325632 = 1.2000000000 × 1.4586104693 |
| CONUS+ SM expectation as a rate | 347/327 = 1.0611620795 ± 0.1804281346 counts kg⁻¹ day⁻¹ |
| Billard-route cross-check | ratio 0.991302 (0.87 %) — but only 4.722893e-06 of its weight is in the window |
| IA omission at window edges | 2.904884e-03 and 1.940585e-03 |

## What this changes downstream

The pre-registered leg failed, so the ROADMAP Phase-16 backtracking trigger is live.
Plans 16-02 and 16-03 **compute** `S/B_particle` — the trigger's instruction is to claim
no headline until the failure is understood, and §7 of the determination report states
what is understood (the window mapping, the endpoint, the internal document disagreement)
and what is not (the 2-5 keV_nr tail, CONUS+'s own form-factor choice). The unresolved
gate and the **numerator-only** statement travel onto every downstream deliverable.

## Deviations

- **Deviation Rule 4 (missing component).** `conus_check.py` introduces one new
  `np.interp` site, which the Phase-10 interpolator-inventory closure guard correctly
  caught. The sanctioned response was taken: a full inventory row was added to
  `10-01-INTERPOLATOR-INVENTORY.md` and the closure count bumped 44 → 45, with the
  guarding argument written out (the clamp at the upper edge returns the table's own
  trailing exact zero, and the support fraction is emitted as a column).

## Pre-existing suite state (reported, not caused here)

The baseline in this worktree is **819 passed, 1 failed**, not the 820/0 the plans quote.
The single failure is `tests/test_legacy_grid_disposition.py::test_retraction_no_live_statement_of_the_display_rule`,
and it is triggered by `16-02-PLAN.md` line 346's own wording (the phrase "…figures are
not mixed into one ratio" places a display-rule keyword beside an energy range). It
predates this plan's execution, is caused by a contract document this executor must not
edit, and is flagged for the orchestrator.
