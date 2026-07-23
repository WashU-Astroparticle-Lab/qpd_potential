---
phase: 16-s-b-particle-assembly-lee-overlay-and-the-signal-side-conus-check-p-sb
plan: 02
title: "S/B_particle = 1.33e-02 (estimates-only) / 7.29e-03 (estimates-plus-bounds, a LOWER bound) for Ta->Al in the 10-100 eV RoI and 1.32e-02 / 7.27e-03 for Al->Hf, at order_of_magnitude, veto credit exactly 1.0 BY CONSTRUCTION, from a seven-channel inventory whose every headline reproduced before it entered the sum and whose two double-count candidates were resolved by reaction and by event time."
date: 2026-07-23
status: complete
depth: full
completed: 2026-07-23
provides:
  - "src/qpd_potential/sb_assembly.py -- NEW module: bands declared once above the integrator, the band integrator validated against five published headlines before use, the inventory builder, the written double-count audit, the two-layer denominator, the leave-one-out sweep and the trigger-k discharge with its own gap named"
  - "artifacts/v2.0/channel_inventory.csv -- 14 rows (7 channels x 2 designs) with class, scenario, label, re-integrated band rates, published headline and reproduction residual, and the double-count resolution in writing"
  - "artifacts/v2.0/channel_omissions.csv -- 6 named omissions with un-netted bias directions, including the >20 MeV in-RoI and total-rate bounds carried SEPARATELY"
  - "artifacts/v2.0/sb_particle.csv -- 8 rows: both designs x both bands x both denominator layers, veto_credit 1.0 BY CONSTRUCTION and configuration NUCLEUS's-shielding-absent on every row"
  - "artifacts/v2.0/sb_leave_one_out.csv -- 40 rows: 32 in-layer removals plus 8 inelastic-addition rows, with the monotonicity check that applies to each"
  - "tests/test_sb_assembly.py -- 18 tests covering all 13 contract acceptance tests plus a recomputation guard"
  - "GPD/phases/16-.../16-02-SB-ASSEMBLY.md -- the assembly record with the six-row caveat table and the checkpoint recorded in full"
  - "artifacts/v2.0/legacy_grid_disposition.csv -- disposition rows for the four new tracked artifacts (77 register rows)"
one_liner: "CALC-22 is discharged and the milestone's headline number exists: S/B_particle = 1.33e-02 (estimates-only) / 7.29e-03 (estimates-plus-bounds) for Ta->Al and 1.32e-02 / 7.27e-03 for Al->Hf in the 10-100 eV reconstructed RoI, with the sub-eV band at 1.05e-03 / 4.11e-04, all at the assembled label order_of_magnitude whose stated propagation rule renders as the multiplicative band [10^-0.5, 10^+0.5] so that a percent-level quotation would fail a test rather than merely be discouraged; the number is essentially design-independent and it is POOR, and it is reported as computed with no target value carried and nothing adjusted to improve it, because for an unshielded surface wafer at veto credit exactly 1.0 BY CONSTRUCTION a ratio of order 1e-2 is the expected physics; the band integrator was VALIDATED BEFORE USE against every channel's own published headline and reproduced all five to between 7.0e-08 and 1.2e-05 relative against a 1e-4 tolerance declared first, so no channel was blocked; the CEvNS numerator was COMPUTED at 72.9214 / 73.1441 rather than substituted from the 118.73 whole-axis TOTAL, which is 1.63x larger and which now appears only under TOTAL-labelled fields; the capture channel entered as the FULL BAND 4399.777 rather than its thermal 3365.536 component, whose 23.51% non-thermal remainder is itself ~8.7x the entire CEvNS total and whose omission would have understated the channel by 1.31x; the 71Ge M line entered at its RECONSTRUCTED image 65.0 / 63.0 eV rather than its 158.7 eV DEPOSIT energy, as a BOUND carrying both scenarios side by side (130.8197 at saturation against 7.697512 at t = 1 d, a 17.0x spread); both double-count candidates were resolved in writing by reaction channel AND by event time and neither is a double count; the omission list is non-empty with six named rows and un-netted bias directions, five flattering and one -- 71Ge K-line X-ray escape near the wafer face, from a line carrying 87.59% of the EC branching -- penalizing; every in-layer leave-one-out removal of a contributing channel strictly increased the ratio with the neutron channel ranking first in the RoI (x2.188) and the capture bound first in the sub-eV band, and the ONE exception was separated rather than waived: the 71Ge M line contributes EXACTLY zero below 1 eV, so its rows are checked for an exact no-op instead; the inelastic exclusion is justified by a MEASURED -21.049% move against a nuclear-recoil scale 3.356 decades above the RoI top, with the honest correction that a 3-decade MOVE was never arithmetically available on a 1e4 denominator and that at order_of_magnitude the 21% move is INSIDE the band, so the exclusion is not load-bearing for the headline; the trigger-k obligation is discharged on the sub-eV rows with its own gap NAMED -- no committed reconstructed-axis k-scan exists for the CEvNS or neutron channels and the neutron channel dominates the sub-eV denominator, so the emitted spread is a LOWER BOUND on the true k-sensitivity; and the six-row caveat table travels with the number, including the resonance-imprint washout at 3.383 / 3.598 against its own threshold of 5.0, the Landau-Vavilov floor at 4111.82 eV indicting 209 of 584 published v1.0 bins (35.79%), the 100 meV bin's 48.98% / 49.728% axis-attached kernel leakage and 0.590 skewness, the muon sign's anchor-leg dependence, Phase 13's conditional Ge-vs-CaWO4 reversal, and the standing absence of any external validation of the ratio."
plan_contract_ref: GPD/phases/16-s-b-particle-assembly-lee-overlay-and-the-signal-side-conus-check-p-sb/16-02-PLAN.md#/contract

contract_results:
  claims:
    claim-inventory-complete-and-disjoint:
      status: passed
      summary: "Seven channels enumerated from the committed reconstructed-axis artifacts. The band integrator was validated BEFORE use and reproduced every published headline: CEvNS TOTAL 118.728595 / 118.729156 vs 118.73; CEvNS in-RoI 72.921435 / 73.144065 vs 72.9214 / 73.1441; neutron in-RoI 5430.286621 / 5485.151456 vs 5430.287 / 5485.152; Compton 34.248436 / 35.861630; muon 7.465639 / 7.723080. Worst residual 1.18e-05 against a 1e-4 tolerance declared as a module constant first. Zero channels blocked. Both double-count candidates resolved in writing by reaction channel AND by event time, with a structural backstop asserting no two rows share both a source artifact and a deposit mechanism -- which fired once during execution on muon vs Compton, both of which read the same em artifact, and was resolved by making the two deposit mechanisms specific rather than by relaxing the check. The omission list is non-empty with six named rows, un-netted, five flatters_SB and one penalizes_SB."
      linked_ids: [deliv-inventory, deliv-omissions, deliv-assembly-report, deliv-assembly-tests, test-integrator-reproduces-headlines, test-no-double-count, test-omission-list-nonempty, test-axis-tag-on-every-operand, test-full-capture-band, ref-phase13-handoff, ref-phase14-handoff, ref-phase15-labels, ref-phase12-cevns-ext]
      evidence:
        - verifier: gpd-executor
          method: "per-channel headline reproduction executed before the sum with a blocking gate; AST-free structural disjointness check on (source artifact, deposit mechanism); executed needle checks for both written double-count arguments in the artifact and in the report"
          confidence: high
          claim_id: claim-inventory-complete-and-disjoint
          deliverable_id: deliv-inventory
    claim-sb-particle-assembled:
      status: passed
      summary: "S/B_particle assembled for both designs, both bands and both denominator layers at veto credit exactly 1.0 BY CONSTRUCTION with exactly one baseline. RoI 10-100 eV: 1.332628e-02 / 7.290250e-03 (Ta->Al) and 1.322980e-02 / 7.271264e-03 (Al->Hf). Sub-eV E_rec <= 1 eV: 1.045309e-03 / 4.111043e-04 and 1.045685e-03 / 4.116806e-04. The numerator is COMPUTED, not substituted. Both bands are declared once as module constants above the integrator and every channel is re-integrated on them. The two layers are never collapsed and the estimates_plus_bounds layer is asserted strictly larger. Leave-one-out is monotone on every contributing removal, with the one exact-zero channel separated rather than waived. The inelastic exclusion is justified by a measured -21.049% move plus a 3.356-decade recoil-scale argument, and the report states plainly that a 3-decade MOVE was never arithmetically available and that the 21% move is inside the assembled band."
      linked_ids: [deliv-sb-table, deliv-leave-one-out, deliv-assembly-report, deliv-assembly-tests, test-single-baseline-credit-one, test-numerator-computed-not-substituted, test-one-band-definition, test-two-layer-denominator, test-leave-one-out-monotone, test-inelastic-exclusion-measured, test-trigger-k-sensitivity, ref-roadmap-16-sc2, ref-veto-credit, ref-conventions-I]
      evidence:
        - verifier: gpd-executor
          method: "every emitted ratio recomputed inside the test from the committed channel artifacts to 1e-9 relative; AST line-number assertion that the band constants precede both the integrator and the assembler; monotonicity asserted per row against the check that applies to it"
          confidence: high
          claim_id: claim-sb-particle-assembled
          deliverable_id: deliv-sb-table
    claim-labels-survive-into-the-band:
      status: passed
      summary: "The propagation rule is written into the sb_particle.csv header and asserted present by test: assembled_label = the loosest label among the SUMMED channels, and order_of_magnitude renders as the multiplicative band [10^-0.5, 10^+0.5]. The assembled label is order_of_magnitude from the neutron and capture channels, and every emitted band is asserted at least a full decade wide, so emitting a percent-level band would FAIL rather than merely be discouraged. Every occurrence of the muon signed deviation in every emitted artifact and document carries both PDG Leg A and the Leg B bracketing within a four-line window, checked with the Phase-15 window check rather than a weaker one. The configuration is NUCLEUS's-shielding-absent on every row and the forbidden adjective attaches nowhere under the attachment-aware scan, whose search word is built at runtime. The observable is named S/B_particle everywhere; the bare form is permitted only on lines that name someone else's published ratio."
      linked_ids: [deliv-sb-table, deliv-assembly-report, deliv-assembly-tests, test-band-not-tighter-than-loosest, test-caveats-travel, test-no-conservative-word, test-named-sb-particle, ref-phase15-labels, ref-phase13-handoff, ref-roadmap-16-sc2]
      evidence:
        - verifier: gpd-executor
          method: "17-needle executed scan of the caveat table; four-line-window anchor-leg check over four artifacts and one document; Phase-9 token guard imported BY IDENTITY; runtime-constructed forbidden-word and bare-name scans"
          confidence: high
          claim_id: claim-labels-survive-into-the-band
          deliverable_id: deliv-sb-table
  deliverables:
    deliv-inventory:
      status: produced
      path: artifacts/v2.0/channel_inventory.csv
      summary: "14 rows, axis = RECONSTRUCTED on every one. Header carries the full reproduction residual table, the band definitions with the reason re-integration was necessary, the capture full-band decomposition with its 1.31x figure, the statement that 118.73 is a TOTAL and appears only under TOTAL-labelled columns, the statement that 158.7 eV is a DEPOSIT energy appearing only in deposit_energy_eV_DEPOSITED, and the label propagation rule."
      linked_ids: [claim-inventory-complete-and-disjoint]
    deliv-omissions:
      status: produced
      path: artifacts/v2.0/channel_omissions.csv
      summary: "Six named rows with bias directions from the Phase-9 Section-5 closed vocabulary: muon-induced neutrons, muon-induced secondary gammas, cosmogenic 71Ge/68Ge/65Zn activation, 71Ge K-line X-ray escape (the one penalizes_SB row), neutron elastic above the 20 MeV ENDF ceiling with in-RoI and total-rate bounds in SEPARATE columns four decades apart, and the LEE as excluded BY CONSTRUCTION. Explicitly un-netted."
      linked_ids: [claim-inventory-complete-and-disjoint]
    deliv-sb-table:
      status: produced
      path: artifacts/v2.0/sb_particle.csv
      summary: "8 rows = 2 designs x 2 bands x 2 denominator layers. veto_credit 1.0 with disposition BY CONSTRUCTION and configuration NUCLEUS's-shielding-absent on every row; layer_direction states which layer makes S/B_particle a LOWER bound; the assembled label and its band multipliers with the propagation rule in the header; the trigger-k columns with the k_scan_gap field naming what the discharge does not cover."
      linked_ids: [claim-sb-particle-assembled, claim-labels-survive-into-the-band]
    deliv-leave-one-out:
      status: produced
      path: artifacts/v2.0/sb_leave_one_out.csv
      summary: "40 rows: 32 in-layer removals plus 8 rows ADDING the excluded inelastic bound. Each removal carries its in-band contribution, the monotonicity check that applies to it (STRICT_INCREASE_REQUIRED or EXACT_NO_OP_REQUIRED for a zero-contribution channel), and a rank. No-op removals are not emitted, so the monotonicity assertion cannot pass vacuously."
      linked_ids: [claim-sb-particle-assembled]
    deliv-assembly-report:
      status: produced
      path: GPD/phases/16-s-b-particle-assembly-lee-overlay-and-the-signal-side-conus-check-p-sb/16-02-SB-ASSEMBLY.md
      summary: "Ten sections: the headline with its band, the pre-use integrator validation, the band definitions with the measured re-integration difference, the inventory with both double-count resolutions argued by reaction and by event time, the omission list, the two-layer denominator with its LOWER-bound direction, the three disconfirming checks, the six-row caveat table, the re-scope integrity statement, and the checkpoint recorded in full."
      linked_ids: [claim-inventory-complete-and-disjoint, claim-sb-particle-assembled, claim-labels-survive-into-the-band]
    deliv-assembly-tests:
      status: produced
      path: tests/test_sb_assembly.py
      summary: "18 tests, one per contract acceptance test plus a recomputation guard, with HEADLINE_REL, RECOMPUTE_REL and the capture-understatement tolerance declared as module constants before any check runs. The Phase-9 shielded-token guard is imported by identity; the forbidden adjective and the bare ratio name are both built at runtime."
      linked_ids: [claim-inventory-complete-and-disjoint, claim-sb-particle-assembled, claim-labels-survive-into-the-band]
    deliv-assembly-module:
      status: produced
      path: src/qpd_potential/sb_assembly.py
      summary: "A NEW module so no file:line inventory key moves. Bands and tolerances first, integrator second, assembler third, by construction. No new interpolation site, so the Phase-10 interpolator closure count is untouched by this plan."
      linked_ids: [claim-sb-particle-assembled]
    deliv-disposition-16-02:
      status: produced
      path: artifacts/v2.0/legacy_grid_disposition.csv
      summary: "Four rows, all not_a_spectrum with written reasons over 40 characters. Register closure re-runs its own git ls-files enumeration and passes at 77 rows."
      linked_ids: [claim-sb-particle-assembled]
  acceptance_tests:
    test-integrator-reproduces-headlines:
      status: passed
      summary: "All five published headlines reproduced for both designs, worst residual 1.18e-05 against the 1e-4 tolerance. Residual recorded per channel in the inventory and the full table written into the artifact header. Zero channels blocked; the blocking path exists and is asserted empty rather than absent."
      linked_ids: [claim-inventory-complete-and-disjoint, deliv-inventory, deliv-assembly-tests]
    test-no-double-count:
      status: passed
      summary: "Both resolutions present with by-reaction and by-event-time arguments over 40 characters each; both located in the inventory rows and in the report; MT=2, MT=102 and the 11.43 d half-life all asserted present in the report. The structural check on (source artifact, deposit mechanism) FIRED during execution on muon vs Compton and was fixed by making the mechanisms specific, not by relaxing the check."
      linked_ids: [claim-inventory-complete-and-disjoint, deliv-inventory, deliv-assembly-report, deliv-assembly-tests]
    test-omission-list-nonempty:
      status: passed
      summary: "Non-empty; all five named must_contain entries present plus the LEE; a bias direction from the closed vocabulary on every row; reasons over 40 characters; the >20 MeV in-RoI and total-rate fractions asserted to differ by more than three decades and carried in separate columns; both bias signs present so the list is demonstrably un-netted."
      linked_ids: [claim-inventory-complete-and-disjoint, deliv-omissions, deliv-assembly-report]
    test-axis-tag-on-every-operand:
      status: passed
      summary: "axis == RECONSTRUCTED on every row of the inventory, the headline table and the sweep table. 158.7 eV asserted absent from every field except deposit_energy_eV_DEPOSITED and explicitly prose-labelled fields; the 71Ge row's reconstructed image asserted to be 65.0 or 63.0 eV; the line asserted 100% in-RoI by comparing its RoI integral against its whole-axis integral."
      linked_ids: [claim-inventory-complete-and-disjoint, deliv-inventory, deliv-sb-table, deliv-assembly-tests]
    test-full-capture-band:
      status: passed
      summary: "The value entering the sum is 4399.777, asserted NOT equal to the thermal 3365.536 and asserted equal to thermal + non-thermal. Non-thermal fraction 0.2351 and full/thermal 1.3073 both asserted. The denominator difference between the two layers is asserted equal to the capture bound plus the M-line bound, so the full band is provably what was summed. 1.31, 23.51 and 1034 all asserted present in the report."
      linked_ids: [claim-inventory-complete-and-disjoint, deliv-inventory, deliv-assembly-report]
    test-single-baseline-credit-one:
      status: passed
      summary: "veto_credit() returns exactly 1.0 as a float with BY CONSTRUCTION in its docstring; every emitted row carries 1.0 with that disposition; exactly 8 rows for 8 distinct (design, band, layer) keys, so there is no second veto-credited baseline; configuration is NUCLEUS's-shielding-absent on every row."
      linked_ids: [claim-sb-particle-assembled, deliv-sb-table, deliv-assembly-tests]
    test-numerator-computed-not-substituted:
      status: passed
      summary: "The in-RoI numerator reproduces 72.9214 / 73.1441 to 1e-4 and is asserted more than 1.0 counts/kg/day away from 118.73. Every inventory field containing 118.7 is asserted to be a TOTAL-labelled column or the prose note. No S row carries 118.73 as its numerator."
      linked_ids: [claim-sb-particle-assembled, deliv-inventory, deliv-sb-table]
    test-one-band-definition:
      status: passed
      summary: "AST line numbers assert all five band constants precede both band_integral and assemble; each band constant is assigned exactly once in the module; every spectral channel is present in SPECTRAL_SOURCES and therefore re-integrated here; the report is asserted to record both upstream band definitions as the reason re-integration was necessary."
      linked_ids: [claim-sb-particle-assembled, deliv-assembly-module, deliv-sb-table, deliv-assembly-report]
    test-two-layer-denominator:
      status: passed
      summary: "Both layers present and separately labelled for all four (design, band) pairs; estimates_plus_bounds asserted strictly larger in B and strictly smaller in S/B_particle; the LOWER BOUND direction asserted present both in the layer_direction column and in the report."
      linked_ids: [claim-sb-particle-assembled, deliv-sb-table, deliv-assembly-report, deliv-assembly-tests]
    test-leave-one-out-monotone:
      status: passed
      summary: "Every STRICT_INCREASE_REQUIRED row asserted to have ratio > 1.0. The two EXACT_NO_OP_REQUIRED rows -- the 71Ge M line in the sub-eV band -- are asserted to have exactly zero in-band contribution and exactly ratio 1.0. The rank-1 channel is asserted to be the largest in-band contributor in that layer, which is the neutron channel in the RoI and the capture bound in the sub-eV band; asserting a fixed name would have been wrong and was corrected during execution. The sweep covers every summed channel."
      linked_ids: [claim-sb-particle-assembled, deliv-leave-one-out, deliv-assembly-tests]
    test-inelastic-exclusion-measured:
      status: passed
      summary: "Move measured at -21.049% in the RoI and -26.887% in the sub-eV band, emitted as rows of the sweep table; the 3.356-decade recoil-scale figure asserted; the inventory row asserted in_sum=False with EXCLUDED_FROM_SUM; the two gamma-emission recoil energies asserted present in the sweep header; the measured move asserted present in the report."
      linked_ids: [claim-sb-particle-assembled, deliv-leave-one-out, deliv-inventory, deliv-assembly-report]
    test-trigger-k-sensitivity:
      status: passed
      summary: "The declared range is READ from params.TRIGGER_SHARPNESS_RANGE and asserted equal on every sub-eV row; five numeric k columns present on every sub-eV row; the P_trig == 1 value asserted DIFFERENT from the triggered value so the limit is a real computation; the k_scan_gap field asserted to contain the words LOWER BOUND, i.e. the gap is named rather than implied."
      linked_ids: [claim-sb-particle-assembled, deliv-sb-table]
    test-band-not-tighter-than-loosest:
      status: passed
      summary: "Assembled label asserted order_of_magnitude; the band multiplier asserted to span at least a full decade; every emitted S/B_particle band asserted to contain its central value and to span at least a decade; an explicit anti-precision assertion that would fail on a percent-level band; the propagation rule asserted present verbatim in the artifact header."
      linked_ids: [claim-labels-survive-into-the-band, deliv-sb-table, deliv-assembly-report]
    test-caveats-travel:
      status: passed
      summary: "All 17 caveat needles located in the report by an executed scan: 3.383 / 3.598 against the 5.0 threshold with the over-reading warning, 4111.8 / 209 / 584 / 35.79, 100 meV with 48.98 and 0.590, -20.61 with +20.34 and both anchor legs, the constant-sigma conditionality, and the no-external-validation-of-the-ratio statement. Zero bare occurrences of the muon signed deviation across four artifacts and the report under the four-line window check."
      linked_ids: [claim-labels-survive-into-the-band, deliv-assembly-report, deliv-sb-table]
    test-no-conservative-word:
      status: passed
      summary: "The Phase-9 token guard is asserted imported BY IDENTITY (is, not ==) for both token tuples. Zero occurrences of the forbidden adjective attached to this configuration across four artifacts, the report, the module and the test file, with the search word built at runtime so the test file itself carries no literal. Zero APPLIED shielded-quantity hits in the module -- one FIRED during execution on the phrase 'X-ray attenuation length' in the K-line escape reason and was reworded to 'X-ray absorption depth' rather than exempted."
      linked_ids: [claim-labels-survive-into-the-band, deliv-sb-table, deliv-assembly-report, deliv-assembly-tests]
    test-named-sb-particle:
      status: passed
      summary: "Zero bare unqualified occurrences of the ratio name across all four artifacts and the report, except on lines that explicitly name CONUS+'s or NUCLEUS's own published ratio. The forbidden string is assembled at runtime. Every headline column header carries the qualified name and the module constant is asserted equal to it."
      linked_ids: [claim-labels-survive-into-the-band, deliv-sb-table, deliv-assembly-report, deliv-assembly-tests]
  references:
    ref-roadmap-16-sc2:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "SC2's single baseline at credit 1.0 by construction, the NUCLEUS's-shielding-absent description with its text check, the S/B_particle naming rule and the band discipline are all discharged and tested. The withdrawal of the pre-re-scope expectation is honoured: no target value appears anywhere and a runtime-built scan asserts it."
    ref-phase13-handoff:
      status: completed
      completed_actions: [read, use, compare, cite]
      missing_actions: []
      summary: "The neutron channel enters as the largest denominator term with its order_of_magnitude label, its demonstrated-UNBOUNDED flux term (+41.33% / -16.31% under perturbations invisible to its only cross-check), its un-netted directional-bias context and its separately carried in-RoI and total-rate omission bounds. The imprint WASHOUT verdict (3.383 / 3.598 vs a pre-declared 5.0) is caveat 1 of the table that travels with the headline."
    ref-phase14-handoff:
      status: completed
      completed_actions: [read, use, compare, cite]
      missing_actions: []
      summary: "The prompt capture bound enters as the FULL band 4399.777 with its 23.51% non-thermal fraction and the 1.31x understatement figure recorded; the 71Ge M line enters at its reconstructed image with BOTH scenarios attached; K and L lines are outside the RoI and are not summed; the inelastic bound is present as an EXCLUDED_FROM_SUM row with a measured exclusion cost."
    ref-phase15-labels:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "The machine-readable label object is propagated: the muon band x0.65..x1.35 that ENCLOSES the PDG leg bracket, the anchor-leg dependence of the sign, and the record that the muon channel has no external reconstructed-axis benchmark at all. The Landau-Vavilov floor and the muon sign are caveats 2 and 4 of the travelling table. The committed em k-scan supplies the only reconstructed-axis k-sensitivity available, and what it does NOT cover is named."
    ref-phase12-cevns-ext:
      status: completed
      completed_actions: [read, use, compare]
      missing_actions: []
      summary: "The numerator. The integrator reproduces the 118.73 whole-axis TOTAL to 118.728595 / 118.729156 -- the validation Phase 14 performed and this plan repeats before use -- and the in-RoI value is then COMPUTED as a different number."
    ref-veto-credit:
      status: completed
      completed_actions: [read, use, avoid]
      missing_actions: []
      summary: "veto_credit() is called, never re-typed, and its BY CONSTRUCTION docstring is asserted. The avoid action -- the forbidden adjective -- is discharged by an attachment-aware scan whose search word is built at runtime."
    ref-conventions-I:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "P_trig multiplies eps and does not replace it; the P_trig == 1 assembly is emitted as a separate column and asserted different from the triggered one; the [1, 12] range is read from params. The obligation is discharged AND its uncovered part is named in the k_scan_gap field rather than left implicit."
  forbidden_proxies:
    fp-silent-neutron-omission-16:
      status: rejected
      notes: "The neutron channel is present, is the largest denominator term, carries order_of_magnitude, and its separately carried in-RoI and total-rate omission bounds appear as their own columns in the omission register, never netted."
    fp-thermal-only-capture:
      status: rejected
      notes: "The full band 4399.777 is what enters the sum, asserted by comparing the inter-layer denominator difference against the sum of the two bounds. The thermal-only value is present only as a labelled decomposition column."
    fp-total-as-in-roi:
      status: rejected
      notes: "The numerator is computed at 72.9214 / 73.1441 and asserted more than 1.0 counts/kg/day away from 118.73; 118.7 appears only under TOTAL-labelled fields."
    fp-inelastic-summed-as-rate:
      status: rejected
      notes: "Excluded from the headline sum with an EXCLUDED_FROM_SUM flag, and the exclusion justified by a MEASURED move rather than by assertion -- together with the correction that the 3-decade figure describes the bound's looseness in the band, not the size of the move, and that at order_of_magnitude the move is inside the band."
    fp-collapsed-bound-layers:
      status: rejected
      notes: "Two separately labelled layers on every row, never collapsed, with layer_direction naming which one makes the ratio a LOWER bound. A test asserts the bounds layer is strictly larger."
    fp-precision-inflation-16:
      status: rejected
      notes: "Assembled label order_of_magnitude with a band of one full decade, and a test that fails if any emitted band is narrower than a factor 1.25. The report states in words that the many digits are reproducibility figures for the quadrature."
    fp-reduced-credit-16:
      status: rejected
      notes: "Exactly 1.0 BY CONSTRUCTION read from the function; exactly one baseline; zero rows carrying any other credit; the forbidden adjective absent under the attachment-aware scan."
    fp-rescued-headline:
      status: rejected
      notes: "The M-line scenario used in the headline layer is SATURATION, the larger and less flattering of the two, and both travel together. No band was narrowed, no bound dropped, no VNS rescale reached for, and no target value carried. The poor result is reported as computed."
  uncertainty_markers:
    weakest_anchors:
      - "The eV-keV differential shape of the sea-level neutron flux. It sets the largest denominator term in the RoI, has NO independent validation, and Phase 13 demonstrated by explicit construction that perturbations invisible to its only cross-check move the in-RoI rate by +41.33% and -16.31% while moving that cross-check by exactly zero. Every number in this plan inherits it."
      - "The 71Ge M-line exposure scenario: 130.8197 at saturation against 7.697512 at t = 1 d is a 17.0x spread on a channel that lands 100% inside the RoI, and the project does not own the exposure history."
      - "The completeness of the inventory. Muon-induced neutrons, muon-induced secondary gammas and cosmogenic activation are absent from the whole milestone, and the 71Ge K-line X-ray escape fraction for a 110 g wafer is computed nowhere. The omission list makes the gap visible; it does not close it."
      - "The prompt-capture bound's looseness. It is rigorous and cascade-independent but loose by an unknown factor <= 1, and it is 44% of the estimates_plus_bounds denominator, so that layer is an upper bound of unknown tightness."
      - "The absence of ANY external validation of the ratio, carried from plan 16-01 -- where the numerator's one external check came back window-conditional and FAILED on its pre-registered window."
      - "The trigger-k discharge covers muon and Compton only. No committed reconstructed-axis k-scan exists for the CEvNS or neutron channels, and the neutron channel dominates the sub-eV denominator, so the emitted sub-eV k spread is a LOWER BOUND on the real one."
    unvalidated_assumptions:
      - "That the seven inventory channels are mutually exclusive as energy deposits. Checked explicitly for the two live candidates by reaction and by event time; not provable in general."
      - "That an accuracy label propagates through a RATIO by taking the loosest input. This is a STATED rule, not a derived one, and it is written into the artifact header precisely so it can be challenged."
      - "That rendering order_of_magnitude as the multiplicative band [10^-0.5, 10^+0.5] is the right rendering. One decade of total span is a choice; a reader who means a factor 10 each way would widen it."
      - "That the sub-eV band top at a literal E_rec = 1 eV is the right definition. It spans the E_rec image of the 1 eV deposit regime boundary, so the observable changes character inside the band; the alternative, a design-dependent band top, would have made the two designs non-comparable."
      - "That the committed reconstructed-axis artifacts are all on the SAME axis with the same underflow convention. Asserted per artifact by dropping everything below 1e-3 eV rather than assumed -- the em tables carry the underflow row and the others do not."
    competing_explanations:
      - "A poor S/B_particle could be the physics of an unshielded surface wafer -- the expected result -- or an assembly bug. Separated by the leave-one-out sweep, the per-channel headline reproduction before the sum, the axis-tag assertions and the measured inelastic sensitivity. None of the four found a bug."
      - "A denominator dominated by one channel could reflect real physics or a units error in that channel's re-integration. Separated by requiring every channel's own published headline to reproduce before it enters the sum; all five did, to better than 1.2e-05."
      - "The two denominator layers differing by a factor 1.83 could mean the bounded channels are genuinely large, or that the bounds are simply loose. Both readings are reported, and the capture bound's looseness is explicitly stated as an unknown factor <= 1."
    disconfirming_observations:
      - "The structural no-double-count check FIRED during execution on the muon and Compton rows, which read the same em artifact and both carried the generic mechanism 'electron recoil, prompt'. It was fixed by making the two mechanisms specific, not by relaxing the check."
      - "The Phase-9 shielded-token guard FIRED during execution on the phrase 'X-ray attenuation length' in the K-line escape omission reason. It was reworded to 'X-ray absorption depth' rather than exempted, even though the physics was a genuine in-crystal absorption length and not a shielded quantity."
      - "The leave-one-out sweep found a channel that does NOT strictly increase the ratio when removed: the 71Ge M line contributes exactly zero below 1 eV. Rather than waive the check, those rows were re-classified to require an EXACT no-op, which is a real check on where that line was placed."
      - "Including the inelastic bound moves S/B_particle by 21%, NOT by the ~3 decades a naive reading of its looseness would suggest. The report states why a 3-decade move was never arithmetically available on a 1e4 denominator, and concedes that at order_of_magnitude the exclusion is therefore not load-bearing for the headline."
      - "The assembled label came out order_of_magnitude and the band is a full decade wide, which means the two designs' central values (1.33e-02 vs 1.32e-02) are NOT distinguishable by this milestone. That is reported rather than presented as a design comparison."
---

# Plan 16-02 Summary — the `S/B_particle` Assembly

## The headline

| design | band | estimates only | estimates + bounds (**LOWER bound**) |
|---|---|---|---|
| **Ta→Al** | RoI 10–100 eV | **1.33 × 10⁻²** | **7.29 × 10⁻³** |
| **Al→Hf** | RoI 10–100 eV | **1.32 × 10⁻²** | **7.27 × 10⁻³** |
| Ta→Al | sub-eV (E_rec ≤ 1 eV) | 1.05 × 10⁻³ | 4.11 × 10⁻⁴ |
| Al→Hf | sub-eV (E_rec ≤ 1 eV) | 1.05 × 10⁻³ | 4.12 × 10⁻⁴ |

At `order_of_magnitude`, band multiplier [10^−0.5, 10^+0.5]. **The two designs are not
distinguishable at this label.** The ratio is poor and is reported as computed.

## Denominator contributions, RoI 10–100 eV (Ta→Al), counts kg⁻¹ day⁻¹

| channel | value | share of `estimates_plus_bounds` |
|---|---|---|
| neutron elastic | 5430.29 | 54.3 % |
| prompt (n,γ) capture (**bound**) | ≤ 4399.78 | 44.0 % |
| ⁷¹Ge EC M line (**bound**, saturation) | ≤ 130.82 | 1.3 % |
| Compton γ | 34.25 | 0.34 % |
| muon ionization | 7.47 | 0.07 % |
| **total** | **10002.60** | |
| *(Ge discrete inelastic, EXCLUDED)* | *≤ 2666.83* | *−21.0 % on the ratio if added* |

## Three checks that fired during execution and were fixed rather than relaxed

1. The structural **no-double-count** check fired on muon vs Compton (same artifact,
   same generic mechanism string). Fixed by making both deposit mechanisms specific.
2. The **Phase-9 shielded-token guard** fired on "X-ray attenuation length" in the
   K-line escape reason. Reworded to "X-ray absorption depth" rather than exempted.
3. The **leave-one-out monotonicity** check fired on the ⁷¹Ge M line in the sub-eV band,
   where it contributes exactly zero. Re-classified to require an **exact no-op**, which
   is a real check on where that line sits, not a waiver.
