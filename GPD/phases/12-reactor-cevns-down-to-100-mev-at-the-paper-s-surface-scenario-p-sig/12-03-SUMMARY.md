---
phase: 12-reactor-cevns-down-to-100-mev-at-the-paper-s-surface-scenario-p-sig
plan: 03
title: "Phase-12 closure: the VALD-10 regression against the frozen v1.0 CEvNS spectra on the preserved reconstructed-energy edge indices, the SC3 adjudication, the recomputed target-swap benchmark with its provenance gap, the labelled VNS scalar rescale, and the phase-level SC1-SC5 verdict table"
date: 2026-07-23
status: complete
depth: full
completed: 2026-07-23
provides:
  - "src/qpd_potential/cevns_subev.py — the plan-12-03 section: v1_regression (index-carry comparison with a broadening-off control), write_v1_regression_table, frozen_v1_recoil_support, compound_n2_over_a, closure_provenance_search (word-bounded), vns_rescale, write_vns_rescale_table"
  - "artifacts/v2.0/cevns_v1_regression.csv — 80 rows (40 per design) above 10 eV: E_rec, the v1.0 edge index, both rates, the relative deviation, and the same comparison with broadening OFF"
  - "artifacts/v2.0/cevns_vns_rescale.csv — the optional VNS context line: both candidate integral fluxes with their sources, both scalar factors, and the rescaled 10-100 eV RoI rate for both designs"
  - "GPD/phases/12-.../12-03-CLOSURE-AND-RESCALE.md — the closure report with the phase-level clause-by-clause SC1-SC5 verdict table"
  - "tests/test_cevns_subev_regression.py — 16 tests covering all 11 contract acceptance tests"
  - "The phase-level verdict: 13 PASS, 1 SUPERSEDED, 2 PARTIAL, 1 RESTATEMENT, 1 recorded ABSENCE"
one_liner: "The VALD-10 regression is PARTIAL and is reported as such: Ta->Al reproduces the frozen v1.0 reconstructed CEvNS spectrum to 0.7648% above 10 eV and PASSES, while Al->Hf reaches 3.7246% and FAILS the <1% target -- in exactly ONE bin, the last populated one at the 3.2 keV recoil kinematic endpoint where the rate is 7.9e-07 counts/kg/day/keV, with both designs inside the target below 900 eV; the decisive diagnostic is that turning the IA kernel OFF changes that maximum by 0.001 percentage points, so the residual is the Phase-10 RESPONSE-MATRIX REGENERATION (overlapping columns differ by up to 3.16e-02 and are independent MC samplings), not anything Phase 12 added, and the target was NOT relaxed; SC3's 'T = 0.290 eV reproduces the frozen v1.0 value' is adjudicated a RESTATEMENT with no frozen value behind it (the frozen recoil table floors at 5 eV, confirmed programmatically); the compound arithmetic is recomputed (Ge 22.729, CaWO4 44.193, ratio 1.944, pure W 65.627 / 184W 65.761) and 1.95 is rejected in favour of the same-pipeline 2.31; a word-bounded repository search confirms 407.7 exists ONLY in GPD prose, so the closure is cited as an unreproduced prior assertion, and the total absence of any background-side validation since VALD-11's deletion is carried to Phase 16 SC1; and the VNS line is ONE labelled multiplication carrying both 0.280158 (NUCLEUS-stated 2.1e12) and 0.244174 (the project's own geometric 1.830269e12), with cevns.nucleus_variant_flux() never called."
plan_contract_ref: GPD/phases/12-reactor-cevns-down-to-100-mev-at-the-paper-s-surface-scenario-p-sig/12-03-PLAN.md#/contract

contract_results:
  claims:
    claim-v1-regression:
      status: partial
      summary: "MEASURED AND REPORTED AS PARTIAL, not converted to a pass. 40 bins per design from 10.59 to 944.1 eV of reconstructed energy, selected by INDEX on an edge set that is bit-identical between the v1.0 and extended response matrices (np.array_equal True, max difference exactly 0.0). Ta->Al: max |deviation| 0.7648% at 473.2 eV, mean 0.2304%, 0 bins above the 1% target -- PASSES. Al->Hf: max |deviation| 3.7246% at 944.1 eV, mean 0.2786%, 1 bin above target -- FAILS the <1% VALD-10 target. The failing bin is the SINGLE highest populated one, at the 3.2 keV recoil kinematic endpoint, where the v1.0 rate is 7.88e-07 counts/kg/day/keV, about nine decades below the peak; below 900 eV both designs are inside the target at 0.7648% and 0.5557%. Non-vacuous: the minimum |deviation| is 2.29e-05, so the extended pipeline recomputes rather than echoes. THE DECISIVE DIAGNOSTIC: switching the IA kernel OFF gives 0.7688% / 3.7234%, i.e. the broadening moves the residual by ~0.001 percentage points. The residual is the Phase-10 response-matrix REGENERATION -- the archived and regenerated matrices are independent Monte Carlo samplings whose overlapping columns differ by up to 2.86e-02 (Ta->Al) and 3.16e-02 (Al->Hf) in matrix elements, amplified in a tail bin fed by a handful of deposit columns. Phase 12's own additions leave the validated results untouched to well inside 1%; what fails is a Phase-10 inheritance, and that attribution is recorded rather than assigned to the wrong phase."
      linked_ids: [deliv-regression-table, deliv-closure-report, test-regression-under-1pct, test-regression-non-vacuous, test-index-carry-not-interpolation, test-trigger-off-above-boundary, ref-v1-frozen, ref-roadmap-p12-sc35]
      evidence:
        - verifier: gpd-executor
          method: "bin-by-bin index-carry comparison against the frozen v1.0 spectra, with a broadening-OFF control run that isolates the cause of the residual"
          confidence: high
          claim_id: claim-v1-regression
          deliverable_id: deliv-regression-table
          acceptance_test_id: test-regression-under-1pct
          reference_id: ref-v1-frozen
          forbidden_proxy_id: fp-regression-by-interpolation
          evidence_path: artifacts/v2.0/cevns_v1_regression.csv
    claim-sc3-adjudicated:
      status: passed
      summary: "Adjudicated, not asserted. artifacts/stage1/cevns_dRdT.csv has 320 rows with support 5 - 3200 eV, confirmed programmatically: its floor is 5 eV and it does NOT cover 0.290 eV, so there is no frozen v1.0 value there to compare against. No comparison at 0.290 eV is claimed anywhere in the phase, and a test walks every phase markdown file asserting that none is. Recomputing dR/dT at 0.290 eV with the same code and calling the agreement a regression would be an identity dressed as a check, and it was not done. The clause's physical content -- nothing changes above 0.29 eV -- restates SC4's truncation zero-point rather than corroborating it independently, and is recorded as a RESTATEMENT in the style of Phase 11's three superseded-as-evidence clauses. Note additionally that plan 12-01 measured the zero-point at 0.3067 eV rather than 0.29 eV, so even the restated clause needs its own correction."
      linked_ids: [deliv-closure-report, test-sc3-restatement-recorded, test-no-fabricated-comparison, ref-v1-frozen, ref-roadmap-p12-sc35]
    claim-benchmark-documented:
      status: passed
      summary: "The compound arithmetic is RECOMPUTED here from CIAAW standard atomic weights, not quoted: natural Ge 22.729, CaWO4 compound (Ca + W + 4 O) 44.193, naive ratio 1.944, pure W 65.627 at the standard atomic weight and 65.761 for 184W. The literature's 65.8 is therefore the 184W value, named as such, and it describes a DIFFERENT material that must never stand in for the CaWO4 compound 44.2. 2.31 is stated as the same-pipeline benchmark and 1.95 is explicitly REJECTED, with the physical reason: the naive ratio omits the Helm form factor, the kinematic T_max/E_nu compression, and the per-isotope threshold structure -- worth the ~19% difference between them. The 407.7 dru closure is CITED, not re-run, against NUCLEUS Table 5 at 100% duty (356.5), never the Section-2 prose 280, with BOTH its physical scope (flux x cross-section x target chain only; nothing about any environment or background) AND its provenance gap: a WORD-BOUNDED repository-wide search returns only GPD prose documents, so no code, test, notebook or artifact reproduces it and the citation is labelled an unreproduced prior assertion. The word boundary matters -- a bare substring search matches by coincidence inside a dozen committed numeric CSVs and would have manufactured a reproducible source that does not exist. No CaWO4 or Al2O3 target model was added; the pre-existing veto_envelope/veto_credit Al2O3 mentions are NUCLEUS's own (5 mm)^3 cryodetector cubes from the Phase-8 geometry gate and are recorded as such. The absence of ANY background-side target-swap validation since VALD-11's deletion is stated and carried to Phase 16 SC1."
      linked_ids: [deliv-closure-report, test-compound-arithmetic-recomputed, test-naive-ratio-rejected, test-closure-cited-with-provenance-gap, test-closure-not-rerun, ref-nucleus-table5, ref-literature-closure]
      evidence:
        - verifier: gpd-executor
          method: "independent recomputation of the compound N^2/A arithmetic plus a word-bounded repository search whose result is recorded rather than predicted"
          confidence: medium
          claim_id: claim-benchmark-documented
          deliverable_id: deliv-closure-report
          acceptance_test_id: test-compound-arithmetic-recomputed
          reference_id: ref-literature-closure
          forbidden_proxy_id: fp-closure-as-reproduced
          evidence_path: GPD/phases/12-reactor-cevns-down-to-100-mev-at-the-paper-s-surface-scenario-p-sig/12-03-CLOSURE-AND-RESCALE.md
    claim-vns-rescale-labelled:
      status: passed
      summary: "The line IS reported, as a single labelled scalar multiplication of the finished primary result. Exact proportionality on every bin: the bin-to-bin ratio spread is 2.2e-16, the float division round-trip, so no bin-dependent difference and therefore no second fold. BOTH candidate integral fluxes are carried with their sources named: the NUCLEUS-stated 2.100000e12 (EPJC 86, 29 (2026), arXiv:2509.03559) giving factor 0.280158, and the project's own geometric 1.830269e12 reconstructed by cevns.nucleus_flux_normalization() from NUCLEUS's own 4.25 GW_th per core, 6 nubar/fission, 200 MeV/fission at 72 m and 102 m (EPJC 79, 1018 (2019)) giving 0.244174 -- a ~15% gap already recorded in state.json. No bare unqualified 0.28 appears anywhere. Their 2019 prose 3e12 is named as a third number, 1.639x the geometric reconstruction and a locked forbidden proxy. Rescaled 10-100 eV RoI rates on the finished plan-12-02 spectra: 20.430 / 17.806 (Ta->Al) and 20.492 / 17.860 (Al->Hf) counts/kg/day against primaries 72.921 and 73.144. cevns.nucleus_variant_flux() was NEVER called, asserted by an AST walk of both modules rather than by grep -- the name appears in prose in both, because naming the trap is the point. data/flux/ is unchanged from the phase's starting commit."
      linked_ids: [deliv-rescale-table, deliv-closure-report, test-rescale-is-multiplication, test-rescale-carries-both-fluxes, test-no-variant-flux-call, ref-nucleus-2019, ref-nucleus-table5]
      evidence:
        - verifier: gpd-executor
          method: "scalar multiplication of the finished primary spectrum with exact bin-to-bin proportionality asserted, and an AST walk proving the variant-flux entry point is never called"
          confidence: high
          claim_id: claim-vns-rescale-labelled
          deliverable_id: deliv-rescale-table
          acceptance_test_id: test-rescale-is-multiplication
          reference_id: ref-nucleus-2019
          forbidden_proxy_id: fp-second-vns-run
          evidence_path: artifacts/v2.0/cevns_vns_rescale.csv
  deliverables:
    deliv-regression-table:
      status: passed
      path: artifacts/v2.0/cevns_v1_regression.csv
      summary: "80 rows, 40 per design, above 10 eV of reconstructed energy. Columns: design, E_rec_eV, the v1.0 edge INDEX (ascending, demonstrating the comparison is an index carry rather than an interpolation), the v1.0 rate, the extended rate, the relative deviation, and the same two with broadening OFF so the cause of the residual is in the artifact and not only in the prose. Header records the per-design maxima, the non-vacuity minimum, the bins above target, P_trig(100 eV) = 0.999999999375, and the statement that the archived and regenerated response matrices are independent MC samplings."
      linked_ids: [claim-v1-regression]
    deliv-rescale-table:
      status: passed
      path: artifacts/v2.0/cevns_vns_rescale.csv
      summary: "Four rows, two designs x two candidate integral fluxes. Columns: design, candidate, candidate integral flux, the project's own integral flux 7.495760e12, the rescale factor, the primary 10-100 eV RoI counts, and the rescaled RoI counts. Header states that no second pipeline run, flux table or spectral shape was produced, names the 2019 prose 3e12 as the third number it is, and carries the total-rate-only / shape-assumption / 2.92 m.w.e.-overburden caveats."
      linked_ids: [claim-vns-rescale-labelled]
    deliv-closure-report:
      status: passed
      path: GPD/phases/12-reactor-cevns-down-to-100-mev-at-the-paper-s-surface-scenario-p-sig/12-03-CLOSURE-AND-RESCALE.md
      summary: "Carries every deliv-closure-report.must_contain item: the maximum relative deviation above 10 eV for BOTH designs with the index-carry evidence; the explicit statement that SC3's 0.290 eV clause restates SC4's zero-point and has no frozen v1.0 value behind it; the independently recomputed compound N^2/A values with the naive ratio explicitly rejected; the 407.7 closure cited with BOTH its physical scope and its provenance gap; the statement that the milestone has NO background-side target-swap validation since VALD-11's deletion, carried to Phase 16 SC1; the VNS rescale factor with both candidate integral fluxes named; and the clause-by-clause PASS / SUPERSEDED / PARTIAL verdict table for ROADMAP Phase 12 SC1-SC5 pulling in plans 12-01 and 12-02. Also records the Task-3 checkpoint content in full with no fabricated approval."
      linked_ids: [claim-v1-regression, claim-sc3-adjudicated, claim-benchmark-documented, claim-vns-rescale-labelled]
  acceptance_tests:
    test-regression-under-1pct:
      status: partial
      summary: "Ta->Al 0.7648% PASSES the <1% target with 0 bins above it. Al->Hf 3.7246% FAILS it, in exactly 1 bin. The test pins BOTH the pass and the failure so neither can drift, and it does NOT widen the target. The failing bin is the last populated one at the kinematic endpoint, at 7.88e-07 counts/kg/day/keV; a separate assertion records that below 900 eV both designs are inside the target, as a characterisation of WHERE the failure lives rather than as the verdict."
      linked_ids: [claim-v1-regression, deliv-regression-table, ref-v1-frozen]
    test-regression-non-vacuous:
      status: passed
      summary: "40 bins compared per design, all deviations finite, minimum |deviation| 7.61e-05 (Ta->Al) and 2.29e-05 (Al->Hf) -- small but NOT identically zero, so the extended pipeline is recomputing rather than returning the frozen numbers."
      linked_ids: [claim-v1-regression, deliv-regression-table]
    test-index-carry-not-interpolation:
      status: passed
      summary: "np.array_equal True on the v1.0 and extended reconstructed-energy edge sets with maximum difference EXACTLY 0.0, for both designs, and a source scan of the comparison path finds no np.interp, interp1d, PchipInterpolator or np.allclose. The emitted artifact carries the ascending v1.0 edge index per row."
      linked_ids: [claim-v1-regression, deliv-regression-table, ref-v1-frozen]
    test-trigger-off-above-boundary:
      status: passed
      summary: "The compared object is the un-triggered dRdErec column (source-asserted: the regression path reads ['dRdErec'] and never dRdErec_trigger), and P_trig(100 eV) = 0.999999999375, i.e. 1 - P_trig = 6.3e-10, far inside the 1% regression tolerance. Comparing a trigger-suppressed spectrum against un-triggered v1.0 numbers would have manufactured a deviation that is not a pipeline change."
      linked_ids: [claim-v1-regression, deliv-regression-table]
    test-sc3-restatement-recorded:
      status: passed
      summary: "The closure report states explicitly that SC3's 0.290 eV clause restates SC4's zero-point, that the frozen table floors at 5 eV, and that it is NOT independent corroboration. Checked by needle on the written report."
      linked_ids: [claim-sc3-adjudicated, deliv-closure-report, ref-roadmap-p12-sc35]
    test-no-fabricated-comparison:
      status: passed
      summary: "artifacts/stage1/cevns_dRdT.csv confirmed at 320 rows with T_min = 5.0 eV exactly and covers_0p290_eV False. Every markdown file in the phase directory (excluding the PLANs, which are the specification being adjudicated) is walked and asserted not to claim a comparison against a frozen v1.0 value at 0.290 eV."
      linked_ids: [claim-sc3-adjudicated, deliv-closure-report, ref-v1-frozen]
    test-compound-arithmetic-recomputed:
      status: passed
      summary: "Ge 22.729 (target 22.7), CaWO4 compound 44.193 (target 44.2), naive ratio 1.944 (target 1.95), pure W 65.627 at the standard atomic weight and 65.761 for 184W -- which is the literature's 65.8, identified as a DIFFERENT quantity more than 1.4x the compound value. All recomputed from atomic weights held in the module, none quoted from GPD/literature/."
      linked_ids: [claim-benchmark-documented, deliv-closure-report, ref-literature-closure]
    test-naive-ratio-rejected:
      status: passed
      summary: "The report names 2.31 as the benchmark, rejects 1.95 explicitly, and gives the physical reason in terms of what the naive ratio omits: the Helm form factor, the kinematic T_max/E_nu compression, and the per-isotope threshold structure. Checked by needle on the written report."
      linked_ids: [claim-benchmark-documented, deliv-closure-report]
    test-closure-cited-with-provenance-gap:
      status: passed
      summary: "The word-bounded search git grep -lE '(^|[^0-9.])407[.]7([^0-9]|$)' was RUN and its result recorded: only GPD prose documents, no code, test, notebook or committed data artifact. has_reproducible_source is False. The test is written so that FINDING a reproducible source would fail it and force the citation to be re-checked -- an informative outcome in the opposite direction. The citation carries both the scope (flux x cross-section x target chain only) and the gap (unreproduced prior assertion)."
      linked_ids: [claim-benchmark-documented, deliv-closure-report, ref-literature-closure]
    test-closure-not-rerun:
      status: passed
      summary: "No CaWO4 or Al2O3 target model, fold or pipeline was added. The three pre-existing files that mention Al2O3 (veto_envelope.py, veto_credit.py, test_veto_credit.py) are enumerated explicitly rather than allow-listed by pattern: they describe NUCLEUS's own (5 mm)^3 cryodetector cubes from the Phase-8 geometry gate. The closure is also NOT rescaled to the primary normalization, which would destroy the comparison since it was folded at the NUCLEUS/VNS site against their Table 5."
      linked_ids: [claim-benchmark-documented, deliv-closure-report]
    test-rescale-is-multiplication:
      status: passed
      summary: "The bin-to-bin ratio of rescaled to primary has a spread of 2.2e-16 -- the float division round-trip -- so the ratio is the SAME on every bin and no bin-dependent difference exists. The RoI numbers in the artifact are verified to be exactly that multiplication of the primary RoI counts to 1e-12."
      linked_ids: [claim-vns-rescale-labelled, deliv-rescale-table]
    test-rescale-carries-both-fluxes:
      status: passed
      summary: "Both integral fluxes named with sources and both factors given: 2.100000e12 -> 0.280158 and 1.830269e12 -> 0.244174, with the ~15% gap between them asserted to lie in [10%, 20%]. The artifact header carries both numbers, both factors, fp-second-vns-run and fp-unlabelled-rescale. No bare unqualified 0.28 appears."
      linked_ids: [claim-vns-rescale-labelled, deliv-rescale-table, ref-nucleus-2019]
    test-no-variant-flux-call:
      status: passed
      summary: "hasattr(cevns, 'nucleus_variant_flux') is asserted first, so the trap is confirmed real rather than hypothetical, and then an AST walk of cevns_subev.py and fold.py asserts no Name or Attribute node with that identifier exists. A grep would have failed: the name appears in prose in both modules because naming the trap is the point. data/flux/ tracked contents are compared against the phase's starting commit rather than against a hand-maintained allow-list, and no VNS or NUCLEUS flux file exists."
      linked_ids: [claim-vns-rescale-labelled, deliv-rescale-table]
  references:
    ref-v1-frozen:
      status: completed
      completed_actions: [read, compare]
      missing_actions: []
      summary: "artifacts/stage1/reconstructed_spectra_{TaAl,AlHf}.csv read and compared bin by bin against the extended pipeline on the preserved reconstructed-energy edge indices, 40 bins per design above 10 eV. artifacts/stage1/cevns_dRdT.csv read to confirm its 5 eV support floor programmatically, which is what makes SC3's 0.290 eV clause unanswerable as written."
    ref-nucleus-table5:
      status: completed
      completed_actions: [compare, cite]
      missing_actions: []
      summary: "NUCLEUS EPJC 86, 29 (2026), arXiv:2509.03559, Table 5 at 100% duty (CaWO4 CEvNS 356.5 counts/kg/day/keV in the 10-100 eV RoI) is the anchor the cited 407.7 closure was folded against, ratio 1.14. Cited with its scope; the Section-2 prose 280 (the 80%-duty value, 356.5 x 0.8 = 285) is named as fp-nucleus-prose-280 and is not used. The comparison is CITED rather than re-run, per the roadmap's instruction, and is not rescaled."
    ref-literature-closure:
      status: completed
      completed_actions: [read, cite]
      missing_actions: []
      summary: "GPD/literature/SUMMARY.md read as the source of 407.7, ratio 1.14, the same-pipeline 2.31, and the naive compound figures. The compound arithmetic was then RECOMPUTED independently rather than quoted, and the 407.7 closure is cited with the provenance gap the word-bounded repository search confirms: it exists only in GPD prose."
    ref-nucleus-2019:
      status: completed
      completed_actions: [compare, cite]
      missing_actions: []
      summary: "NUCLEUS EPJC 79, 1018 (2019), arXiv:1905.10258 Sect. 2 supplies the VNS site geometry -- two Chooz-B cores, 4.25 GW_th each at 72 m and 102 m, six nubar per fission, 200 MeV per fission -- from which cevns.nucleus_flux_normalization() reconstructs 1.830269e12. Compared against the 2026 paper's stated 2.1e12 (a ~15% gap) and against their own 2019 prose 3e12 (1.639x the geometric value, a locked forbidden proxy). All three are named in the artifact and the report."
    ref-roadmap-p12-sc35:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "ROADMAP Phase 12 success criteria 1, 3 and 5 read verbatim and adjudicated clause by clause in the closure report's SC1-SC5 verdict table, which also pulls in plans 12-01's SC2/SC4 verdicts and 12-02's SC1 verdicts so the phase closes in one place. SC3-a is recorded PARTIAL against its measured numbers and SC3-b a RESTATEMENT."
  forbidden_proxies:
    fp-second-vns-run:
      status: rejected
      notes: "cevns.nucleus_variant_flux() was never called, asserted by AST walk rather than grep. No VNS flux table exists and data/flux/ is unchanged from the phase's starting commit. The VNS line is one scalar multiplication of the finished primary result with bin-to-bin ratio spread 2.2e-16."
    fp-unlabelled-rescale:
      status: rejected
      notes: "Both candidate integral fluxes are named with their sources in the artifact header, the artifact rows and the report, and both factors (0.280158 and 0.244174) are given. No bare unqualified 0.28 appears anywhere; the ~15% gap between the NUCLEUS-stated and project-geometric fluxes is stated as the reason both are carried."
    fp-nucleus-prose-280:
      status: rejected
      notes: "The closure is anchored on Table 5 at 100% duty (356.5 counts/kg/day/keV). The Section-2 prose 280 is named only as the 80%-duty value it is (356.5 x 0.8 = 285) and as the ~27% S/B flattery it would cause. It is not used as an anchor."
    fp-naive-compound-ratio:
      status: rejected
      notes: "1.944 was recomputed here specifically in order to be REJECTED as the Ge/CaWO4 benchmark, with the physical reason stated. 2.31 is named as the benchmark. The pure-tungsten values 65.627 / 65.761 are identified as a DIFFERENT material and are never substituted for the CaWO4 compound 44.193."
    fp-closure-as-reproduced:
      status: rejected
      notes: "The 407.7 closure and the 1.14 ratio are cited as an UNREPRODUCED PRIOR ASSERTION, with the word-bounded search result recorded. The citation states the closure covers the flux x cross-section x target chain ONLY and says nothing about any environment or background, and the total absence of any background-side validation since VALD-11's deletion is stated and carried to Phase 16 SC1."
    fp-regression-by-interpolation:
      status: rejected
      notes: "np.array_equal on the overlapping reconstructed-energy edges, maximum difference exactly 0.0, and a source scan of the comparison path confirming no np.interp / interp1d / PchipInterpolator / np.allclose. Bins are selected by index and the artifact carries the index per row."
  uncertainty_markers:
    weakest_anchors:
      - "The 407.7 dru CaWO4 closure. It is the milestone's ONLY signal-side target-swap validation and it has NO reproducible artifact anywhere in this repository -- a word-bounded search returns GPD prose alone. Everything the phase says about the flux x cross-section x target chain being validated rests on an assertion this repository cannot re-run. The same applies to the 2.31 ratio, which rests on the same unreproduced fold."
      - "The VNS rescale factor. The NUCLEUS-stated 2.1e12 and the project's own geometric reconstruction 1.830269e12 differ by ~15%, and their 2019 prose says 3e12 (1.639x the geometric value, a locked forbidden proxy). The line is optional precisely because its own normalization is this uncertain, and both factors ship for that reason."
      - "The <1% regression target rests on the frozen v1.0 spectra being the right comparison object on the preserved edge set -- a Phase-10 result used here rather than re-established. It also rests on a response matrix that Phase 10 REGENERATED, which is what the residual actually measures."
      - "The milestone has NO background-side target-swap validation at all since VALD-11 was deleted. The signal-side closure does not substitute for it and must not be presented as if it did."
    unvalidated_assumptions:
      - "That the VNS spectral shape is the project's Phase-2 shape, which is what makes a scalar rescale meaningful at all. The project already assumes this elsewhere, but it is an assumption and the rescale inherits it. The rescale is also valid for the total rate normalization ONLY: it says nothing about duty cycle, and nothing about the 2.92 m.w.e. of overburden the VNS carries and the surface background treatment does not."
      - "That 2.31 as quoted was folded in the same pipeline at a single normalization. This is stated in GPD/literature/SUMMARY.md and PROJECT.md but, like 407.7, is not reproducible here."
      - "That comparing the v1.0 spectra against a REGENERATED response matrix is the comparison VALD-10 intended. The archived and extended matrices are independent Monte Carlo samplings, so some residual is guaranteed by construction; the target was written as if the comparison were against the same matrix."
    competing_explanations:
      - "A clean <1% regression could be produced by the extended pipeline effectively returning the v1.0 numbers rather than recomputing them. test-regression-non-vacuous requires the deviation to be small but NOT identically zero; the measured minimum is 2.29e-05, so that explanation is excluded."
      - "The regression could equally reflect the extended axis being an exact INDEX CARRY of the v1.0 edges rather than the new sub-eV physics being correct. Above 10 eV the broadening is genuinely sub-bin, so this regression tests the PLUMBING far more than the physics, and the report says so explicitly."
      - "The Al->Hf endpoint-bin failure could be a real physics change from the broadening or a Monte Carlo artefact of the regenerated response matrix. The broadening-OFF control separates them decisively: the kernel moves the maximum by 0.001 percentage points, so it is the matrix."
    disconfirming_observations:
      - "MEASURED AND REPORTED: the folded regression above 10 eV EXCEEDS 1% for Al->Hf, at 3.7246%. The VALD-10 leg is reported PARTIAL rather than passed, and the tolerance was not widened."
      - "MEASURED AND REPORTED: the residual is NOT caused by anything Phase 12 added. Turning the IA kernel off changes it by ~0.001 percentage points; the archived and regenerated response matrices differ by up to 3.16e-02 in matrix elements. The failure is a Phase-10 inheritance and is attributed there rather than to this phase."
      - "CHECKED AND DID NOT FIRE: np.array_equal on the overlapping reconstructed-energy edges is True with maximum difference exactly 0.0, so the comparisons in this phase against v1.0 are valid."
      - "CHECKED AND DID NOT FIRE: the deviation is not identically zero anywhere; the extended pipeline recomputes rather than echoes."
      - "CHECKED AND DID NOT FIRE: the recomputed compound arithmetic DOES reproduce ~22.7 / ~44.2 / ~1.95, so the survey's rejected-benchmark numbers are themselves right and what is being rejected is what the roadmap says it is. The one refinement: 65.8 is the 184W value, not the standard-atomic-weight tungsten value 65.63."
      - "CHECKED AND DID NOT FIRE IN THE HOPEFUL DIRECTION: the repository search did NOT find a reproducible source for 407.7. Had it done so the provenance gap would have closed and the closure citation would have strengthened."
      - "CHECKED AND DID NOT FIRE: the rescaled VNS spectrum IS exactly proportional to the primary on every bin, so no second pipeline run happened."
      - "NOT CHECKED ANYWHERE IN PHASE 12, carried forward: the bottom decade of the sub-eV spectrum against any independent object. Both regressions available to this phase live above 10 eV, where the broadening is sub-bin."

comparison_verdicts:
  - subject_id: test-regression-under-1pct
    subject_kind: acceptance_test
    subject_role: decisive
    reference_id: ref-v1-frozen
    comparison_kind: benchmark
    metric: max_relative_deviation_above_10eV_vs_frozen_v1_reconstructed_spectra
    threshold: "< 1% (ROADMAP SC3)"
    verdict: tension
    recommended_action: "Report VALD-10's regression leg PARTIAL. Attribute the exceedance to the Phase-10 response-matrix regeneration, not to Phase 12, and decide at milestone level whether the <1% gate should be re-stated as a same-matrix comparison. Do not widen the tolerance."
    notes: "Ta->Al 0.7648% PASSES; Al->Hf 3.7246% FAILS, in exactly one bin -- the last populated one at the 3.2 keV kinematic endpoint, at 7.88e-07 counts/kg/day/keV. Below 900 eV both designs are inside the target. Broadening OFF gives 3.7234%, so the IA kernel contributes ~0.001 percentage points and the residual is the regenerated response matrix."
  - subject_id: ref-nucleus-table5
    subject_kind: reference
    subject_role: decisive
    reference_id: ref-nucleus-table5
    comparison_kind: benchmark
    metric: our_CaWO4_fold_vs_NUCLEUS_Table5_at_100pct_duty
    threshold: "the already-passed 14% closure, cited not re-run"
    verdict: inconclusive
    recommended_action: "Decide before Phase 16 leans on it whether the CaWO4 fold should be reconstructed so the closure has a reproducible artifact. Until then keep the unreproduced-prior-assertion label attached."
    notes: "407.7 vs 356.5 counts/kg/day/keV, ratio 1.14. INCONCLUSIVE as a comparison this repository can stand behind: a word-bounded repository-wide search finds 407.7 only in GPD prose -- no code, test, notebook or committed artifact reproduces it, so there is no reproducible command. Anchored on Table 5 at 100% duty, never the Section-2 prose 280."
  - subject_id: claim-benchmark-documented
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-literature-closure
    comparison_kind: cross_method
    metric: same_pipeline_Ge_over_CaWO4_ratio_vs_naive_compound_N2_over_A
    threshold: "the same-pipeline 2.31 is the benchmark; the naive 1.95 is rejected"
    verdict: pass
    recommended_action: "Use 2.31 as the target-swap benchmark in Phase 16 and never the naive 1.95 or the pure-tungsten 65.8."
    notes: "Recomputed independently: Ge 22.729, CaWO4 compound 44.193, naive ratio 1.944, pure W 65.627 (standard atomic weight) / 65.761 (184W, which is the literature's 65.8 and a DIFFERENT material). The ~19% gap between 1.944 and 2.31 is what the form factor, the kinematic compression and the per-isotope threshold structure are worth."
  - subject_id: ref-nucleus-2019
    subject_kind: reference
    subject_role: decisive
    reference_id: ref-nucleus-2019
    comparison_kind: benchmark
    metric: VNS_integral_flux_NUCLEUS_stated_vs_project_geometric_reconstruction
    threshold: "both must be named, or the line is not reported"
    verdict: tension
    recommended_action: "Carry BOTH factors on any VNS-labelled number downstream. Never quote a bare 0.28."
    notes: "NUCLEUS-stated 2.100000e12 gives 0.280158; the project's own reconstruction from NUCLEUS's own site numbers gives 1.830269e12 and 0.244174 -- a ~15% gap the project's arithmetic does not close. Their 2019 prose 3e12 is a third number, 1.639x the geometric value and a locked forbidden proxy."
  - subject_id: ref-roadmap-p12-sc35
    subject_kind: reference
    subject_role: decisive
    reference_id: ref-roadmap-p12-sc35
    comparison_kind: benchmark
    metric: ROADMAP_Phase12_SC1_SC3_SC5_clauses_vs_measurement
    threshold: "every clause adjudicated PASS / SUPERSEDED / PARTIAL / RESTATEMENT with its measured number"
    verdict: tension
    recommended_action: "Carry the phase-level table into the milestone record as written. Re-state SC3-a's <1% gate as a same-matrix comparison, or accept a PARTIAL, before Phase 16 depends on it; do not widen it."
    notes: "SC1 all four clauses PASS. SC3-a PARTIAL (Ta->Al 0.7648% passes, Al->Hf 3.7246% fails in one endpoint bin, cause traced to the Phase-10 response-matrix regeneration). SC3-b a RESTATEMENT with no frozen v1.0 value behind it (the frozen recoil table floors at 5 eV). SC5 both clauses PASS, the closure carrying a named provenance gap. Combined with plan 12-01's SC2 SUPERSEDED and SC4-c PARTIAL, the phase closes at 13 PASS / 1 SUPERSEDED / 2 PARTIAL / 1 RESTATEMENT / 1 recorded ABSENCE."
---

# 12-03 Summary — Phase-12 closure

## What was established

**VALD-10 regression leg — PARTIAL, and reported as such.** On the preserved
reconstructed-energy edge indices (`np.array_equal` True, max difference exactly 0.0),
40 bins per design above 10 eV:

| design | max \|deviation\| | verdict |
|---|---|---|
| Ta→Al | **0.7648 %** at 473.2 eV | PASS |
| Al→Hf | **3.7246 %** at 944.1 eV | **FAIL**, in one bin |

The `<1 %` target was **not relaxed**. The Al→Hf exceedance is the single highest populated
bin, at the kinematic endpoint, at 7.9 × 10⁻⁷ counts/kg/day/keV; below 900 eV both designs
are inside the target.

**The decisive diagnostic:** turning the IA kernel **off** changes that maximum by ~0.001
percentage points. The residual is the **Phase-10 response-matrix regeneration** — the
archived and regenerated matrices are independent Monte Carlo samplings differing by up to
3.16 × 10⁻² in matrix elements — not anything Phase 12 added.

**SC3's 0.290 eV clause — a RESTATEMENT.** The frozen recoil table floors at 5 eV
(programmatically confirmed), so there is no frozen v1.0 value to compare against; and the
clause's content restates SC4's zero-point. Not counted as independent corroboration, and no
comparison was fabricated.

**Benchmark — 2.31 documented, 1.95 rejected.** Recomputed: Ge 22.729, CaWO₄ compound 44.193,
naive ratio 1.944, pure W 65.627 / ¹⁸⁴W 65.761 (which is where the literature's 65.8 comes
from, and it is a different material). The 407.7 closure is cited with its scope **and** its
provenance gap — a word-bounded search finds it **only** in GPD prose.

**VNS line — reported, as one labelled multiplication.** Factors 0.280158 (NUCLEUS-stated
2.1 × 10¹²) and 0.244174 (project geometric 1.830269 × 10¹²), both carried. Exact
proportionality to 2.2 × 10⁻¹⁶ on every bin. `nucleus_variant_flux()` never called.

**Phase-level verdict: 13 PASS, 1 SUPERSEDED, 2 PARTIAL, 1 RESTATEMENT, 1 recorded ABSENCE.**

## What cuts against expectations

1. **The regression FAILS for one design.** The plan expected a clean <1 %. It is reported as
   PARTIAL with the number, and traced to its actual cause.
2. **The cause is a Phase-10 inheritance.** The `<1 %` gate is being measured against a
   response matrix that was itself resampled, so some residual is guaranteed by construction.
   Flagged at milestone level rather than silently attributed to Phase 12.
3. **The regression tests the plumbing, not the sub-eV physics.** Above 10 eV the broadening
   is sub-bin. **Nothing in Phase 12 tests the bottom decade against an independent object.**
4. **65.8 is the ¹⁸⁴W value**, not standard-atomic-weight tungsten (65.63). Both reported.
5. **A bare substring search for `407.7` matches a dozen committed numeric CSVs by
   coincidence.** Only the word-bounded search gives the honest answer — the naive one would
   have manufactured a reproducible source that does not exist.

## Deviations

| Rule | Type | Description |
|---|---|---|
| 5-adjacent | measured contradiction, reported not escalated | The VALD-10 regression exceeds its target for Al→Hf. This is a *measurement contradicting a stated criterion*, which the phase's own precedent (Phase 11, plan 12-01) handles by reporting the supersession/partial with numbers rather than by redirecting the physics. The cause was isolated with a controlled broadening-off run before the verdict was written. No tolerance was widened and no window was narrowed. |
| 1 | code bug | The closure-provenance search initially used a bare substring match and returned 27 files including a dozen numeric CSVs — a false positive that would have *closed* the provenance gap incorrectly. Replaced with a word-bounded regex. |
| 4 | missing component | `test_closure_not_rerun` initially flagged three pre-existing Phase-8 files that mention Al₂O₃ (NUCLEUS's own cryodetector cubes). They are now enumerated explicitly rather than allow-listed by pattern, so the guard cannot rot. |
| 4 | missing component | `test_no_variant_flux_call` was rewritten from a grep to an AST walk: the name `nucleus_variant_flux` appears in prose in both modules because naming the trap is the point, so only parsing distinguishes a mention from a call. |

## Verification

Full suite: **639 passed, 0 failed** (baseline 593 + 14 + 16 + 16). `data/flux/*.csv`
provenance-header churn reverted; the frozen flux table byte-identical to `HEAD`. Every new
`.csv` has a `legacy_grid_disposition.csv` row.

## Checkpoint

Task 3 is `checkpoint:human-verify`. Under the standing session directive its content is
recorded **in full** in `12-03-CLOSURE-AND-RESCALE.md` §6 and execution continued. **No
approval was given and none is recorded.** The open review question — whether
citing-with-a-gap is sufficient for the milestone's decisive signal deliverable, or whether
the CaWO₄ fold should be reconstructed before Phase 16 leans on it — is carried forward.
