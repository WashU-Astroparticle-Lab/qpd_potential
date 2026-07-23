---
phase: 16-s-b-particle-assembly-lee-overlay-and-the-signal-side-conus-check-p-sb
plan: 03
title: "ROADMAP Phase 16 SC4 is SUPERSEDED BY MEASUREMENT -- the criterion has no solution, for two independently computed reasons -- and the LEE is carried as an (A, alpha) overlay band whose two device scalings turn out to disagree by only ~2x in dru once the volume model's x118 mass factor is seen to cancel in a mass-normalized unit. Phase 16 closes with all four success criteria verdicted."
date: 2026-07-23
status: complete
depth: full
completed: 2026-07-23
provides:
  - "src/qpd_potential/lee_overlay.py -- NEW module: the power-law overlay with E0 declared once, alpha DERIVED from the RED20 above-ground anchors and carried as a range, both device scalings as named edges, the closed-form crossover solver, the SC4-as-written evaluator, and the terminal figure"
  - "artifacts/v2.0/lee_overlay_band.csv -- 936 rows: the overlay evaluated on the committed reconstructed axis from 100 meV, both band edges x three alpha values, every row UNMEASURED_FOR_THIS_DETECTOR and not_folded_through_response"
  - "artifacts/v2.0/lee_crossover_amplitudes.csv -- 37 rows: one SC4-as-written adjudication row plus 36 crossover rows under their own explicit names"
  - "artifacts/v2.0/sb_particle_with_lee.pdf -- the terminal figure, pdf.compression = 0, annotation machine-read out of its own text stream"
  - "tests/test_lee_overlay.py -- 14 tests covering all 8 contract acceptance tests plus a bracket-recording check and a target-value guard"
  - "GPD/phases/16-.../16-03-LEE-AND-CLOSEOUT.md -- the LEE determination, the SC4 adjudication, all four SC verdicts, the caveat table and the milestone hand-off"
  - "artifacts/v2.0/legacy_grid_disposition.csv -- disposition rows for the two new tracked artifacts (79 register rows)"
one_liner: "CALC-21 is discharged and Phase 16 closes. ROADMAP SC4's decisive number -- 'the LEE amplitude at which S/B_particle = 1' -- was evaluated AS LITERALLY WRITTEN FIRST and is SUPERSEDED BY MEASUREMENT, with both determinations computed rather than asserted: S/B_particle does not depend on the LEE amplitude at all, demonstrated by CONTRAST rather than repetition (the differently-named S/B_total moves from 1.332628e-02 at A = 1e-06 dru to 6.866716e-06 at A = 1e+06 dru, a factor 1.94e+03, while S/B_particle is bit-identical at both because assemble() takes no amplitude and its summed channel set contains no LEE term); and it cannot reach 1 for any non-negative A, because its supremum is 1.332628e-02, a factor 75.04 below unity before any LEE is added, and even under the charitable S/B_total = 1 reading the required LEE band integral is S - B_particle = -5399.0791 counts/kg/day, negative; a finding of SOLVABLE would have been equally acceptable and would have refuted the planning note, and the outcome is recorded either way with the criterion quoted verbatim and its wording flagged for the orchestrator without editing ROADMAP.md or REQUIREMENTS.md; the two well-defined replacements are computed under their OWN names -- lee_equals_B_particle at 942.4 dru at E0 = 1 keV (RoI, estimates-plus-bounds, central alpha) and lee_equals_S at 6.870 dru, the latter being what PITFALLS.md Pitfall 7 actually specifies -- against extrapolated LEE amplitudes of 1.000e+04 to 2.042e+04 dru, i.e. 10.6x to 21.7x above LEE dominance and 1456x to 2972x above signal erasure, so on every extrapolation available the LEE would dominate both the particle background and the signal by one to three orders of magnitude while remaining a prediction of nothing; alpha = 1.430677 is DERIVED from the EDELWEISS RED20 ABOVE-GROUND germanium anchors 1e5 / 1e4 dru at 200 eV / 1 keV and carried over [1.0000, 1.8614] from a declared factor-2 bracket on the anchor ratio; A FINDING THAT CUTS AGAINST THE SURVEY'S OWN FRAMING is reported rather than repaired -- dru is already mass-normalized, so a VOLUME-scaling model predicts a dru INVARIANT under mass extrapolation and Chang's x118.28 factor CANCELS, making that band edge exactly 1.000 and the two models' disagreement only ~2x in dru rather than the two orders of magnitude the survey's x120 framing implies, with the real width coming from the 3.301-to-5.301-decade alpha extrapolation instead; the two scalings are found NOT to strictly bracket the RED20 anchor, which coincides with the volume edge by construction, and that is recorded rather than quietly widened; the LEE is proven never folded by AST parse and never summed by byte-identity of sb_particle.csv against its committed state; the terminal figure carries its annotation, the accuracy label, both band-edge names and the sub-eV boundary drawn as the E_rec IMAGE of a 1 eV deposit, all read OUT of the PDF text stream with the TJ kerning arrays rejoined; and all four ROADMAP success criteria carry verdicts -- SC1 PARTIALLY CONFIRMED (window-conditional, its pre-registered leg a FAIL), SC2 CONFIRMED, SC3 CONFIRMED, SC4 SUPERSEDED BY MEASUREMENT -- with no window narrowed, no threshold lowered and no band tightened to make any of them true."
plan_contract_ref: GPD/phases/16-s-b-particle-assembly-lee-overlay-and-the-signal-side-conus-check-p-sb/16-03-PLAN.md#/contract

contract_results:
  claims:
    claim-lee-band-carried:
      status: passed
      summary: "dR/dE_LEE = A (E/E0)^(-alpha) with E0 = 1 keV declared once as a module constant and stated on every artifact row and on the figure. alpha DERIVED inside the module from the two EDELWEISS RED20 ABOVE-GROUND germanium anchors (the /3 underground values are not used) and re-derived independently inside the test rather than transcribed; carried as the range [1.0000, 1.8614] from a declared factor-2 bracket on the anchor ratio, labelled DECLARED not sourced. Both contradictory device scalings are carried as named edges with their extrapolation factors written out, and a test asserts neither is ever emitted without the other in any artifact or on the figure. Evaluated directly on the committed reconstructed axis; never folded through the response, proven by AST parse shown non-vacuous three ways; never summed into any headline, proven by git byte-identity of sb_particle.csv against its committed state. Every amplitude row carries UNMEASURED_FOR_THIS_DETECTOR and no LEE-free or phonon-scale-avoids claim appears anywhere."
      linked_ids: [deliv-lee-band, deliv-lee-figure, deliv-closeout-report, deliv-lee-tests, test-lee-not-folded, test-both-scalings-present, test-no-lee-prediction-claimed, test-lee-not-summed-into-headline, ref-roadmap-16-sc34, ref-lee-anchors, ref-pitfalls-lee]
      evidence:
        - verifier: gpd-executor
          method: "AST scan for imports, attribute references, calls and path strings of response / response_matrix / fold / trigger, shown non-vacuous by asserting the LEE evaluation exists and is called; git diff --name-only against HEAD for the byte-identity proof; alpha re-derived in test from the two anchor points"
          confidence: high
          claim_id: claim-lee-band-carried
          deliverable_id: deliv-lee-band
    claim-sc4-adjudicated:
      status: passed
      summary: "SC4's criterion was evaluated AS LITERALLY WRITTEN, first, with its wording quoted verbatim beside the evaluation. Determination 1 (does S/B_particle depend on A?) is answered by CONTRAST rather than by repetition: S/B_total moves by a factor 1.94e+03 across A in [1e-06, 1e+06] dru while S/B_particle is unchanged, and the reason is structural -- assemble() has no amplitude parameter and its summed channel set has no LEE term. Determination 2 (can it reach 1?) is answered by solving: the supremum is 1.332628e-02 and the required LEE band integral under the charitable reading is -5399.0791 counts/kg/day, negative. VERDICT: SUPERSEDED BY MEASUREMENT, recorded either way -- a finding of solvable would have refuted the planning note and was an equally acceptable outcome. The two replacements are computed under their OWN names for both bands, both designs and both denominator layers, reproduced independently in test to 1e-6, with the Romani, Chang and RED20 placements emitted as ratios and the CONVENTIONS Section I trigger-probability caveat on every sub-eV row. SC4's phrasing appears on exactly one row."
      linked_ids: [deliv-crossovers, deliv-closeout-report, deliv-lee-tests, test-sc4-evaluated-as-written, test-replacements-named-separately, test-crossovers-computed, ref-roadmap-16-sc34, ref-sb-particle, ref-pitfalls-lee]
      evidence:
        - verifier: gpd-executor
          method: "both determinations computed against the committed 16-02 artifact; the S/B_total contrast independently recomputed in test and asserted to move by more than 10x; every crossover re-solved in test from an independently written closed-form integral to 1e-6 relative"
          confidence: high
          claim_id: claim-sc4-adjudicated
          deliverable_id: deliv-crossovers
    claim-phase-closeout-16:
      status: passed
      summary: "All four ROADMAP Phase 16 success criteria carry verdicts in the Phase-12/13/14 vocabulary with an evidence path named for each: SC1 PARTIALLY CONFIRMED (window-conditional; its pre-registered leg is a FAIL by 3.28 decades), SC2 CONFIRMED, SC3 CONFIRMED, SC4 SUPERSEDED BY MEASUREMENT. The no-narrowing statement is located by an executed check. The terminal figure's annotation, accuracy label, both band-edge names, the axis tag, the unmeasured status and the sub-eV boundary as the E_rec IMAGE of a 1 eV deposit are all read OUT of the PDF's own text stream with the TJ kerning arrays rejoined -- the figure is written with pdf.compression = 0 to make that a real read. The six-row caveat table from 16-02 and the numerator-only statement from 16-01 are both on the terminal deliverable, with zero bare occurrences of the muon signed deviation and the NUCLEUS / CONUS+ ratios present only as shielded-experiment context. The milestone hand-off names eight open items for the orchestrator and edits none of their files."
      linked_ids: [deliv-closeout-report, deliv-lee-figure, deliv-lee-tests, deliv-disposition-16-03, test-four-sc-verdicts, test-figure-annotation, test-caveats-reach-terminal-deliverable, test-disposition-rows-16-03, ref-roadmap-16-sc34, ref-sb-particle, ref-conventions-I]
      evidence:
        - verifier: gpd-executor
          method: "four SC table rows parsed and each asserted to carry a vocabulary verdict and an evidence path; 16-needle executed scan of the caveat table; PDF text-stream read with kerning rejoin; the disposition register's own git ls-files enumeration re-run inside the test"
          confidence: high
          claim_id: claim-phase-closeout-16
          deliverable_id: deliv-closeout-report
  deliverables:
    deliv-lee-band:
      status: produced
      path: artifacts/v2.0/lee_overlay_band.csv
      summary: "The overlay evaluated on the committed reconstructed axis from the 100 meV grid floor, for both named band edges across three alpha values. E0, the axis tag, the not_folded flag, the UNMEASURED status, the written-out extrapolation factors and both extrapolation spans in decades are on every row. The header carries the alpha derivation, the dru-invariance finding, and the recorded answer to whether the two scalings bracket the RED20 anchor."
      linked_ids: [claim-lee-band-carried]
    deliv-crossovers:
      status: produced
      path: artifacts/v2.0/lee_crossover_amplitudes.csv
      summary: "One row flagged is_sc4_as_written carrying the verbatim criterion, both determinations with their numbers, the solvability verdict and the reason; plus 36 rows of lee_equals_B_particle and lee_equals_S under their own names, each with the Romani, Chang and RED20 placements as ratios and, on the sub-eV rows, the CONVENTIONS Section I caveat that the reported observable there is a trigger probability."
      linked_ids: [claim-sc4-adjudicated]
    deliv-lee-figure:
      status: produced
      path: artifacts/v2.0/sb_particle_with_lee.pdf
      summary: "All particle channels plus the CEvNS signal on the shared reconstructed axis from 100 meV, the LEE as a SHADED BAND between its two named edges, the RoI shaded, both designs' sub-eV boundaries drawn and labelled as the E_rec IMAGE of a 1 eV deposit, and a note that the capture bound is a total reaction rate rather than a spectrum so it is not drawn. Written with pdf.compression = 0; the annotation, the accuracy label, both edge names, the axis tag, the unmeasured status and the decade span are all machine-read back out of the file."
      linked_ids: [claim-lee-band-carried, claim-phase-closeout-16]
    deliv-closeout-report:
      status: produced
      path: GPD/phases/16-s-b-particle-assembly-lee-overlay-and-the-signal-side-conus-check-p-sb/16-03-LEE-AND-CLOSEOUT.md
      summary: "Nine sections: SC4 as written with both determinations, the two replacements under their own names, where the extrapolations sit, the band and what it is and is not (including the dru-invariance finding and the failed bracket), the terminal figure, the four SC verdicts, the caveat table carried forward, the milestone hand-off with eight orchestrator flags, and the checkpoint recorded in full."
      linked_ids: [claim-lee-band-carried, claim-sc4-adjudicated, claim-phase-closeout-16]
    deliv-lee-tests:
      status: produced
      path: tests/test_lee_overlay.py
      summary: "14 tests with CROSSOVER_REL and ALPHA_REL declared as module constants before any check runs. The forbidden LEE-free phrasings, the forbidden configuration adjective and the withdrawn expectation are all built at runtime."
      linked_ids: [claim-lee-band-carried, claim-sc4-adjudicated, claim-phase-closeout-16]
    deliv-lee-module:
      status: produced
      path: src/qpd_potential/lee_overlay.py
      summary: "A NEW module carrying the power-law overlay, the two device scalings, the crossover solver, the SC4-as-written evaluator, the differently-named sb_total_with_lee that exists only so SC4 could be evaluated, and the terminal figure. No new interpolation site."
      linked_ids: [claim-lee-band-carried, claim-sc4-adjudicated]
    deliv-disposition-16-03:
      status: produced
      path: artifacts/v2.0/legacy_grid_disposition.csv
      summary: "Two rows: the overlay band as bounded_native_axis with its 100 meV floor recorded, and the crossover register as not_a_spectrum. Both reasons over 40 characters. The register's own git ls-files closure re-runs inside the test and passes."
      linked_ids: [claim-phase-closeout-16]
  acceptance_tests:
    test-lee-not-folded:
      status: passed
      summary: "AST parse of the module: zero imports, zero attribute references, zero calls and zero path strings for response, response_matrix, fold or trigger. Non-vacuity asserted by requiring lee_dRdE to exist AND be called. Every row of both emitted tables carries not_folded_through_response = True and axis = RECONSTRUCTED."
      linked_ids: [claim-lee-band-carried, deliv-lee-module, deliv-lee-tests]
    test-both-scalings-present:
      status: passed
      summary: "Both edges present in the band table for EVERY alpha value, so no single-scaling emission exists; both present as ratio columns on every crossover row; both names read out of the figure's text stream. The extrapolation factors 1950, 955, 10300 and 118.28 are asserted present as numbers in the artifact header."
      linked_ids: [claim-lee-band-carried, deliv-lee-band, deliv-lee-figure, deliv-lee-tests]
    test-no-lee-prediction-claimed:
      status: passed
      summary: "UNMEASURED_FOR_THIS_DETECTOR on every amplitude row of both tables; the non-prediction statement located in the report by an executed check; zero LEE-free claims outside an explicit refusal and zero phonon-scale-avoids claims, with both phrasings assembled at runtime."
      linked_ids: [claim-lee-band-carried, deliv-lee-band, deliv-closeout-report, deliv-lee-tests]
    test-lee-not-summed-into-headline:
      status: passed
      summary: "git diff --name-only HEAD -- artifacts/v2.0/sb_particle.csv returns empty, so S/B_particle was overlaid upon and not modified. No channels_summed field contains a LEE term. The module is asserted to define sb_total_with_lee and NOT to define any S/B_particle quantity of its own."
      linked_ids: [claim-lee-band-carried, deliv-crossovers, deliv-lee-tests]
    test-sc4-evaluated-as-written:
      status: passed
      summary: "Both determinations recorded with digits; the criterion quoted verbatim in the artifact header and in the report; an explicit verdict present in both. The contrast underpinning determination 1 is INDEPENDENTLY recomputed in test and asserted to move by more than 10x, and S/B_particle is asserted equal to the small-amplitude S/B_total limit. Determination 2's required LEE contribution is asserted negative. FLAGGED FOR THE ORCHESTRATOR is asserted present."
      linked_ids: [claim-sc4-adjudicated, deliv-crossovers, deliv-closeout-report]
    test-replacements-named-separately:
      status: passed
      summary: "Exactly one row flagged is_sc4_as_written and it is the only row carrying SC4's phrasing; every other row is named lee_equals_B_particle or lee_equals_S; both names and the Pitfall 7 attribution are asserted present in the report."
      linked_ids: [claim-sc4-adjudicated, deliv-crossovers, deliv-closeout-report, deliv-lee-tests]
    test-crossovers-computed:
      status: passed
      summary: "Every crossover reproduced to 1e-6 relative by a closed-form integral written out independently inside the test; all three anchor placements present and positive on every row; the trigger-probability caveat asserted on every sub-eV row; the dominance crossover asserted to cover both designs, both bands and both denominator layers."
      linked_ids: [claim-sc4-adjudicated, deliv-crossovers, deliv-lee-tests]
    test-four-sc-verdicts:
      status: passed
      summary: "Exactly four SC table rows, each asserted to carry a verdict from the closed vocabulary and an evidence path; the no-narrowing statement located by an executed check. SC1 is graded PARTIALLY CONFIRMED and SC4 SUPERSEDED BY MEASUREMENT because the measurements say so, not to reconcile them."
      linked_ids: [claim-phase-closeout-16, deliv-closeout-report, deliv-lee-tests]
    test-figure-annotation:
      status: passed
      summary: "The annotation 'particle backgrounds only; LEE not modelled in the headline' is read OUT of the PDF's own text stream with the TJ kerning arrays rejoined, together with order_of_magnitude, both band-edge names, RECONSTRUCTED, UNMEASURED_FOR_THIS_DETECTOR, the word BAND, the word IMAGE and the numeric sub-eV boundary 0.497240."
      linked_ids: [claim-phase-closeout-16, deliv-lee-figure, deliv-lee-tests]
    test-caveats-reach-terminal-deliverable:
      status: passed
      summary: "All 16 caveat needles located on the terminal report by an executed scan; zero bare occurrences of the muon signed deviation under the Phase-15 four-line window check across all three emitted files; the NUCLEUS and CONUS+ ratios present only under a shielded-context label with an explicit not-as-targets statement; the forbidden configuration adjective absent under the attachment-aware scan with the word built at runtime."
      linked_ids: [claim-phase-closeout-16, deliv-closeout-report]
    test-disposition-rows-16-03:
      status: passed
      summary: "Both new tracked artifacts carry disposition rows from the closed vocabulary with reasons over 40 characters, and the register's own git ls-files enumeration is re-run inside the test and matches the register exactly across all three plans of this phase."
      linked_ids: [claim-phase-closeout-16, deliv-disposition-16-03, deliv-lee-tests]
  references:
    ref-roadmap-16-sc34:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "SC3's overlay-band requirement, its prohibition on folding, the per-figure annotation and SC4's decisive number are all discharged. SC4's wording is REPORTED as a defect in the criterion and flagged for the orchestrator; ROADMAP.md and REQUIREMENTS.md are NOT edited. The risk-register row on LEE design-dependence is carried into the report's statement that the LEE is neither shieldable nor inheritable."
    ref-lee-anchors:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Romani JAP 136, 124502 (area scaling, meV-eV phonons, ~10,300 films) and Chang APL 127, 263502 (bulk volume, eps = 0.68 +/- 0.38 meV, 0.93 g -> 110 g) are the two band edges; the EDELWEISS RED20 above-ground germanium anchors from Adari et al. SciPost Phys. Proc. 9, 001 (2022) supply alpha. All are PROSE-SOURCED survey citations and are labelled as such -- the same class of provenance as the Phase-12 closure figure, though used here as an overlay parameter space rather than as a validation."
    ref-pitfalls-lee:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "Pitfall 7's own formulation -- the LEE level that would ERASE the signal -- is computed as lee_equals_S under that name, and the report states explicitly that it is NOT the same quantity as SC4's wording. Pitfall 7's prohibitions are honoured: no LEE-free claim, no implication that the unified phonon scale escapes the LEE, and the observable is named S/B_particle."
    ref-sb-particle:
      status: completed
      completed_actions: [read, use, compare]
      missing_actions: []
      summary: "Every crossover is defined against the committed plan-16-02 assembly, which this plan reads and leaves byte-identical. Its two denominator layers, its order_of_magnitude band and its six-row caveat table all travel onto the terminal deliverable."
    ref-conventions-I:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "The sub-eV regime boundary is drawn on the figure as the E_rec IMAGE of a 1 eV deposit (0.497240 / 0.495855 eV) and explicitly labelled as an image rather than as a literal, and the caveat that the reported observable below it is a trigger probability is carried on every sub-eV crossover row."
  forbidden_proxies:
    fp-lee-omission-16:
      status: rejected
      notes: "The LEE is on the terminal figure as a shaded band, in its own artifact, and as two named crossover amplitudes on the terminal report. It is not in a footnote."
    fp-lee-folded-through-response:
      status: rejected
      notes: "Proven by AST parse: zero imports, attribute references, calls or path strings for response, response_matrix, fold or trigger, with the scan shown non-vacuous by asserting the evaluation exists and is called."
    fp-lee-single-value:
      status: rejected
      notes: "Both edges present for every alpha value in every artifact and both names read out of the figure's text stream; alpha itself is a range, not a point. A single-scaling emission would fail the test."
    fp-lee-free-claim:
      status: rejected
      notes: "Zero LEE-free claims outside an explicit refusal, and zero claims that the phonon scale avoids the LEE, with both phrasings assembled at runtime. The report states positively that the LEE mechanism and the QPD signal mechanism are the same phenomenon."
    fp-sc4-silent-substitution:
      status: rejected
      notes: "SC4 was evaluated as literally written FIRST, its outcome recorded either way with both determinations computed, and its phrasing appears on exactly one row. Neither replacement is ever labelled with SC4's wording."
    fp-nucleus-sb-as-target:
      status: rejected
      notes: "NUCLEUS's CaWO4 1.2 and Al2O3 0.13 and CONUS+'s 0.03 appear only under an explicit shielded-experiment context label with a not-as-targets statement, and the report states that the milestone carries no replacement expectation at all."
    fp-precision-inflation-lee:
      status: rejected
      notes: "The crossover artifact header states that the many digits are reproducibility figures for the closed-form solve and that the denominator they are measured against carries order_of_magnitude and an UNBOUNDED flux systematic on its largest term. The report quotes the crossovers to four significant figures at most and states the sub-eV ones are the least meaningful numbers in the plan."
  uncertainty_markers:
    weakest_anchors:
      - "The LEE amplitude for a QPD-instrumented germanium wafer, which is UNMEASURED. No LEE measurement exists below ~10 eV in germanium or at 100 meV in any material; the lowest genuine dataset anywhere is CRESST-III from 29.6 eV on CaWO4, a different target."
      - "The single power law extrapolated 3.301 decades below the lowest germanium LEE measurement to the figure floor, and 5.301 decades to the reconstructed-axis floor the sub-eV band integral actually uses. The functional form is specified by the roadmap, not established by data at these energies."
      - "The two device scalings, neither defensible as a prediction -- and, as this plan measured, disagreeing by only ~2x in dru once the volume model's mass factor is seen to cancel. The band is the span between two incompatible MODELS, not an uncertainty interval on a known quantity."
      - "The particle-side denominator the crossovers are measured against, whose largest term carries an UNBOUNDED flux systematic and whose loosest label is order_of_magnitude, and whose numerator's one external check FAILED on its pre-registered window."
      - "The EDELWEISS RED20 anchors themselves, which are prose-sourced from GPD/literature/SUMMARY.md rather than from a locally frozen artifact, and which are quoted to one significant figure -- which is why alpha is carried as a range."
    unvalidated_assumptions:
      - "That the Romani area mechanism and the Chang volume mechanism bracket the truth for this wafer. They might both be wrong, in the same direction -- and they are now known NOT to strictly bracket even the one germanium anchor that exists."
      - "That the LEE spectral shape is separable from its amplitude, so a single alpha can be carried across the whole band."
      - "That the LEE anchors' reconstructed-energy axis is commensurate with this project's. Both are 'measured energy', but they are different detectors with different response chains and the identification is an assumption."
      - "That overlaying rather than summing is the right presentation. It is what the roadmap requires and what Pitfall 7 recommends, but it means the reported headline deliberately excludes a background that -- on every extrapolation computed here -- would dominate it."
      - "That a factor-2 bracket on the anchor RATIO is the right way to turn two one-significant-figure amplitudes into an alpha range. It is a declared choice, written down so it can be challenged."
    competing_explanations:
      - "SC4 having no solution could mean the criterion is ill-posed, OR that S/B_particle was mis-assembled in 16-02. Separated by evaluating the criterion against the committed 16-02 artifact, whose own leave-one-out and headline-reproduction checks passed independently, and by the fact that determination 1 is a DEFINITIONAL result that does not depend on the assembled value at all."
      - "A crossover amplitude far below the extrapolated LEE could mean the LEE dominates this detector, OR that the extrapolation is meaningless three to five decades out. Both readings are reported; neither is asserted."
      - "The LEE band lying above the particle background everywhere could be a real physical statement or an artefact of extrapolating an above-ground surface-detector anchor onto a different geometry. The extrapolation span in decades is on the figure so the reader can weigh it."
    disconfirming_observations:
      - "The two device scalings turned out NOT to strictly bracket the EDELWEISS RED20 above-ground germanium anchor: the volume edge coincides with it exactly. Reported rather than widened."
      - "Chang's x118.28 mass extrapolation CANCELS in dru, because dru is already mass-normalized. The survey's x120 framing implies an amplitude factor that does not exist, and the true model disagreement is only ~2x. This cuts against the plan's own framing of the band and is reported as such."
      - "The sub-eV crossover amplitudes swing by four orders of magnitude across the declared alpha range while the RoI ones swing by ~23x, because the sub-eV band integral is dominated by the unmeasured bottom five decades of the axis. They are labelled the least meaningful numbers in the plan rather than presented alongside the RoI values as equals."
      - "SC4 came out unsolvable, which CONFIRMS the planning note in 16-CONTEXT.md. That is the weaker of the two possible outcomes as evidence, and the test was written so that a finding of solvable would have been recorded just as readily."
---

# Plan 16-03 Summary — LEE Overlay, SC4 Adjudication, Phase-16 Closeout

## SC4, as literally written

> **"the LEE amplitude at which S/B_particle = 1"** → **SUPERSEDED BY MEASUREMENT**

| determination | answer | numbers |
|---|---|---|
| does `S/B_particle` depend on `A`? | **No** | `S/B_total` moves 1.332628e-02 → 6.866716e-06 across A ∈ [1e-6, 1e6] dru; `S/B_particle` is identical at both |
| can it reach 1 for any `A ≥ 0`? | **No** | supremum 1.332628e-02, a factor 75.04 below 1; required LEE integral `S − B` = −5399.0791 counts kg⁻¹ day⁻¹ |

## The named replacements (RoI, Ta→Al, central α = 1.4307)

| quantity | layer | A (dru at E₀ = 1 keV) | RED20 anchor / A | Romani area / A |
|---|---|---|---|---|
| `lee_equals_B_particle` | estimates_only | 515.5 | 19.4× | 39.6× |
| `lee_equals_B_particle` | estimates_plus_bounds | **942.4** | **10.6×** | **21.7×** |
| `lee_equals_S` | — | **6.870** | **1456×** | **2972×** |

## The four success criteria

| SC | verdict |
|---|---|
| SC1 (VALD-12 signal-side + restatement cost) | **PARTIALLY CONFIRMED**, window-conditional; pre-registered leg a FAIL |
| SC2 (CALC-22 `S/B_particle`) | **CONFIRMED** |
| SC3 (CALC-21 LEE overlay band) | **CONFIRMED** |
| SC4 (the decisive LEE amplitude) | **SUPERSEDED BY MEASUREMENT** |

## The finding that cuts against the plan's own framing

`dru` is already mass-normalized, so **Chang's ×118.28 mass extrapolation cancels** and
its band edge is exactly **1.000**. The survey's "×120" is a *total-rate* extrapolation,
not an amplitude factor. The two models therefore disagree by only **~2× in dru**, not by
two orders of magnitude — and the two edges consequently **do not strictly bracket** the
one germanium anchor that exists, because the volume edge sits exactly on it. Both facts
are reported rather than repaired.
