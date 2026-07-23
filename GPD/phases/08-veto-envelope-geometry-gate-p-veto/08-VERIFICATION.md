---
phase: 08-veto-envelope-geometry-gate-p-veto
verified: "2026-07-22T20:30:00Z"
status: gaps_found
score: "21/24"
plan_contract_ref: GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-05-PLAN.md#/contract
contract_results:
  claims:
    claim-gate-discharged:
      status: partial
      summary: "The verdict is stated, sourced, premised, interval-tested and falsifiability-carried, and every number in it reproduces independently. INDEPENDENTLY CONFIRMED: I re-grepped the load-bearing dimension from the frozen source myself - 2508.02488v1.txt line 225 reads verbatim 'It features a cylindrical geometry with 100 mm diameter and 25 mm height, and a mass of 1 kg', and 1905.10258.txt line 285 reads 'an outer veto (3) with a diameter of 10 cm'. All six clearances recompute exactly (coverage -4.3684, orientation-invariant -0.1620, edge -0.1600, cavity -5.1600 / -9.3684, loose cavity +2.3316). Independent multistart Nelder-Mead optimization over SO(3) reproduces every claimed orientation extremum to 6 decimals: min b2 = 7.325626 = (a+t)/sqrt(2), min projected diameter = 10.161968 = sqrt(a^2+t^2), and the zero-thickness Prince-Rupert value 9.578940 = a/(3sqrt(2)/4). The coverage requirement is confirmed to be the face-circumscribed circle sqrt(2)a = 14.368410 and is NOT confused with the space diagonal sqrt(2a^2+t^2) = 14.369802, which the module correctly renames and forbids. Mass closure reproduces: rho*pi*(5.0)^2*(2.5) = 1045.17 g at rho=5.323 and 1050.47 g at rho=5.35, so the artifact's refusal to state 'within 5%' is arithmetically correct. NOT CONFIRMED (the gap): the single-cap coverage premise is licensed in the verdict by an ASSEMBLY-level quote. The source sentence is 'The COV is an arrangement of two cylindrical and four rectangular 2.5 cm thick HPGe crystals... It hermetically covers the cryogenic target detectors' - the subject of 'hermetically covers' is the six-crystal arrangement, not one cap. No artifact derives the one-cap-must-cover requirement from the published 2-cylinder-plus-4-rectangle architecture. This is the phase's fourth error-candidate in the direction that favours the expected no-fit conclusion."
      linked_ids: [deliv-gate-verdict, test-verdict-stated, test-verdict-falsifiability-carried, ref-fit-determination, ref-vald09]
    claim-sc-coverage:
      status: passed
      summary: "All five ROADMAP Phase 8 success criteria are mapped to artifact, section and acceptance test, and the two deviations are flagged as deviations rather than absorbed. INDEPENDENTLY CONFIRMED: SC1's amendment justification holds - I re-ran the negative greps against both the arXiv and the published-journal frozen text and 'envelope', 'cavity', 'inner diameter', 'clearance' and '100 mm' all return zero counts in 2509.03559v1.txt AND in epjc_86_29.txt, so the named SC1 source really is dimensionally silent. SC2 verified in code, not markdown: veto_credit._ROWS has exactly 19 rows, tiers {L1: 6, L1*: 2, L2: 11}, the set of distinct credits is exactly {1.0} under identity comparison, L1* is a first-class member of TIERS rather than folded into L1, and row-b02-multiplicity-cut is the single row carrying credit_basis 'derivation'. The L2-off baseline is described in VETO-TAXONOMY.md section 6 as 'a different and worse configuration', with an explicit sentence refusing the word 'conservative'. SC3 recomputed from the frozen artifact: A_self_direct = 1.000000000000 / 0.999971887382 / 0.997858048250 at 10 eV / 1 keV / 100 keV, matching the reported values digit for digit, and an independent Simpson quadrature gives 0.997819 at 100 keV (agreement 3.9e-05, a quadrature-rule difference on the native log grid). Denominator closure 1.365237 Hz vs frozen header 1.3659 Hz = -0.0485%. SC4 confirmed as an identity: mult_rejection(1) == 0.0 is exactly True, and the occupancy model is verified to agree analytically at N=1 for every p."
      linked_ids: [deliv-gate-verdict, test-sc-mapping-complete, ref-roadmap-phase8]
    claim-premise-void:
      status: passed
      summary: "The premise-void reasoning chain is stated with its physical reason and carries an explicit HONESTY CONDITION that no transport calculation quantifies it. VERIFIER OBSERVATION that strengthens the conclusion beyond what the artifact claims: the milestone-void argument does not actually depend on the contested cap diameter. Its load-bearing input is the payload-scale mismatch, which I recomputed independently - wafer face area 103.2256 cm^2 against the published 3x3 array crystal footprint 9 x (5 mm)^2 = 2.25 cm^2 is a ratio of 45.88x, and this figure rests on the 2019 Fig. 8 '3 x 3 arrays' caption plus the (5 mm)^3 crystal statement, neither of which is touched by any cap-diameter dispute. A 45.9x payload-footprint change forces the copper support and the nearly-4pi B4C liner arrangement regardless of how the coverage comparison resolves."
      linked_ids: [deliv-gate-verdict, test-premise-statement, ref-roadmap-phase8]
    claim-phase-disposition:
      status: passed
      summary: "The Phase 9-16 disposition is argued from each phase's stated Depends-on and Anchor-coverage rows rather than from dependency arrows, and I spot-checked that reasoning against GPD/ROADMAP.md directly. Phase 9's own Depends-on row at ROADMAP line 127 literally reads 'if the wafer does not fit, phi_post is not NUCLEUS's phi_post and this phase is void', so the VOID disposition is the ROADMAP's own text and not an inference. The non-obvious survival call for Phases 10 and 11 is defensible: the ROADMAP itself concedes the 8->10 arrow is scheduling rather than physics. Recoverable fragments are named individually for 12, 14 and 15 rather than the phases being written off wholesale."
      linked_ids: [deliv-gate-verdict, test-disposition-justified, ref-roadmap-phase8]
    claim-no-credit-no-redesign:
      status: passed
      summary: "INDEPENDENTLY CONFIRMED by direct inspection of the modules rather than by trusting the artifact's own sweep. Module-level constants are L2_CREDIT = 1.0, L1STAR_CREDIT = 1.0, L1_REJECTION_CREDIT = 1.0 and no other CREDIT / REJECTION / VETO_FACTOR constant exists with any other value. All 19 taxonomy credits equal 1.0 under exact identity comparison. Grepping the three source modules for '99.8' returns exactly one hit, at wafer_self_veto.py line 183, inside the verbatim B.9 block quotation in the A_SELF_INDUCED docstring where it is explicitly labelled not applied. No candidate dimension for a modified veto appears anywhere. The artifact's own statement of the guard's blind spot (an anonymous inline literal such as rate/5 is undetectable by any decidable rule) is accurate and correctly prevents the guard being mistaken for a proof."
      linked_ids: [deliv-gate-verdict, test-no-credit-no-redesign]
    claim-control-returned:
      status: passed
      summary: "Section 8.3 halts explicitly, states that no Phase 9 work was started and no downstream artifact created, and section 8.2 lists four candidate re-scope directions with none adopted and none recommended. Direction 2 (revisit the wafer format) is surfaced together with the REQUIREMENTS.md out-of-scope text that forbids it, so the option set is complete without the phase quietly reversing a recorded scoping decision. Direction 4 is not oversold: it states plainly that even a larger cavity would overturn only the two cavity clearances."
      linked_ids: [deliv-gate-verdict, test-control-returned]
  deliverables:
    deliv-gate-verdict:
      status: passed
      path: GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-05-GATE-VERDICT.md
      summary: "Exists, 545 lines, substantive and non-placeholder. Carries the verdict, both premises stated with the verdict rather than beneath it, the sign-robustness table at three rounding half-widths, an explicit section 1.1 declaring the -4.37 cm figure not a purely geometric result, the single positive number (+2.3316 cm loose cavity bound) reported prominently rather than buried, the five-criterion coverage map with two flagged deviations, the premise-void chain with its honesty condition, the Phase 9-16 disposition, the surviving-deliverable inventory, the two prohibitions, and the return of control. Every quantity I sampled traces to an upstream artifact as the document claims."
      linked_ids: [claim-gate-discharged, claim-sc-coverage, claim-premise-void, claim-phase-disposition, claim-no-credit-no-redesign, claim-control-returned]
  acceptance_tests:
    test-verdict-stated:
      status: passed
      summary: "A single unambiguous NO FIT verdict is stated in section 1 with its basis, its source dimension, its clearance in cm, and both premises attached. The verdict is stated once and consistently; the same -4.3684 cm figure appears in 08-03-FIT-DETERMINATION.md section 0 and in 08-05-GATE-VERDICT.md sections 1, 1.2, 1.4 and 8.1 with no drift."
      linked_ids: [claim-gate-discharged, deliv-gate-verdict]
    test-verdict-falsifiability-carried:
      status: partial
      summary: "Six overturning conditions are carried from 08-03 section 9 into 08-05 section 2.6, each assessed, and the single most efficient disconfirming observation is named (a published statement of non-face-parallel mounting). Item 6 records a test that was actually run and did not fire (the two figure-scaling anchors agree to 6.6%). GAP: overturning item 3 quantifies the falsification as requiring a cap of at least 14.3684 cm implying about 2.06 kg against the published 1 kg, which would be visible in any published mass statement. That argument only closes the SINGLE-CAP route. Under the published 2-cylinder-plus-4-rectangle COV architecture, assembly-level hermetic coverage of a 10.16 cm square footprint by larger rectangular crystals would require no 14.37 cm cap and no 2.06 kg mass anywhere, so the falsification list is not exhaustive over the ways the coverage basis can fail. Second omission: the falsifiability list never engages arXiv:2508.02488's own sentence bounding what transfers to Chooz (see suggested_contract_checks)."
      linked_ids: [claim-gate-discharged, deliv-gate-verdict, ref-fit-determination]
    test-sc-mapping-complete:
      status: passed
      summary: "All five criteria mapped to a discharging artifact, a section, and named acceptance tests. Both deviations (SC1 evidence-route amendment, SC2 two-tier to three-tier extension) are flagged in the outcome column and given their own subsections rather than being smoothed into a clean pass. I confirmed the SC1 deviation is genuine and not an excuse by reproducing the zero-count greps against both frozen versions of the named source."
      linked_ids: [claim-sc-coverage, deliv-gate-verdict, ref-roadmap-phase8]
    test-premise-statement:
      status: passed
      summary: "Section 4 states the premise as void, gives the five-step physical chain, names the four-to-five components a redesign would touch, and closes with an explicit HONESTY CONDITION that the chain is component-level rather than a transport calculation and that a referee could reasonably demand the unavailable number."
      linked_ids: [claim-premise-void, deliv-gate-verdict]
    test-disposition-justified:
      status: passed
      summary: "Every one of Phases 9 through 16 has a disposition with a justification quoting that phase's own ROADMAP rows. Spot-checked Phase 9 (line 127) and Phase 10/11 anchor-coverage rows against GPD/ROADMAP.md directly; the quoted dependency text is accurate."
      linked_ids: [claim-phase-disposition, deliv-gate-verdict, ref-roadmap-phase8]
    test-no-credit-no-redesign:
      status: passed
      summary: "Verified by direct code and grep inspection rather than by accepting the reported sweep. 19/19 credits exactly 1.0, three module constants all 1.0, no other credit-like constant, the only 99.8 occurrence is inside a labelled not-applied verbatim quote, and resized-veto vocabulary appears only where the prohibition is being stated."
      linked_ids: [claim-no-credit-no-redesign, deliv-gate-verdict]
    test-control-returned:
      status: passed
      summary: "Section 8 constitutes the decision brief: verdict in one sentence, single most important limitation stated immediately after it, surviving deliverables, disposition summary, four candidate directions with costs, and an explicit halt. Control is returned without a recommendation."
      linked_ids: [claim-control-returned, deliv-gate-verdict]
  references:
    ref-fit-determination:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "08-03-FIT-DETERMINATION.md read in full and independently re-derived. Every closed form, every clearance and every sign-robustness interval endpoint reproduces. The gate verdict cites it by section throughout and does not compute any quantity of its own, as it claims."
    ref-taxonomy:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "GPD/analysis/VETO-TAXONOMY.md read and cross-checked against veto_credit._ROWS in code. The 6/2/11 tier split, the 19-row count, the uniform 1.0 credits and the 'different and worse' L2-off framing all verify in both the markdown and the module."
    ref-self-veto:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "src/qpd_potential/wafer_self_veto.py read and executed. A_self_direct is genuinely derived from data/muon_dRdEdep.csv (584-point frozen chord x Landau-Vavilov grid) with no NUCLEUS percentage entering as a value; A_SELF_INDUCED is a separate module-level constant with no merging function, column or table cell; eps_mult(1) is a literal early return under identity comparison. NUCLEUS's own 'very marginal' counterpoint is preserved verbatim in the module docstring, in mult_rejection's docstring, in the emitted CSV header, and in gate verdict section 3.4 - it cuts against the project's framing and was not suppressed."
    ref-roadmap-phase8:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "GPD/ROADMAP.md Phase 8 section read at lines 97-125. The goal and all five success criteria as literally written were compared against the coverage map; the two deviations the artifact declares are real deviations from the literal wording and are declared rather than hidden."
    ref-vald09:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "GPD/REQUIREMENTS.md VALD-09 read at line 49. The gate verdict closes it and additionally flags, as an open follow-up it deliberately does not act on, that the unlabelled '~9 cm^2' figure survives in REQUIREMENTS.md lines 49 and 114 and ROADMAP.md lines 105, 121 and 315. I confirmed all five occurrences persist. Recorded as a comparison verdict: VALD-09 asks whether the wafer PHYSICALLY FITS, while the sign-robust verdict basis answers a COVERAGE question."
  forbidden_proxies:
    fp-veto-credit-transfer:
      status: rejected
      notes: "No NUCLEUS rejection percentage enters any module as a value. Confirmed by grep across all three source modules: the only 99.8 occurrence is inside a labelled verbatim quotation. A_self_direct is computed from the wafer's own frozen deposit distribution and I reproduced all three values independently."
    fp-reduced-credit:
      status: rejected
      notes: "No partial, best-guess or for-reference rejection value appears in any Phase-8 output. All 19 catalogued credits are exactly 1.0 under identity comparison, and 1.0 is correctly documented as the EMPTY credit (background unchanged), not full credit."
    fp-resized-veto:
      status: rejected
      notes: "Resized-veto vocabulary occurs in exactly two places across the Phase-8 outputs and both are the prohibition being stated. The 14.3684 cm figure is used only as an overturning threshold. No candidate modified geometry is proposed, sized or costed."
    fp-continue-past-failed-gate:
      status: rejected
      notes: "Section 8.3 states that no Phase 9 work started, no environment transcription, no digitization, no inversion, no phi_post, and no downstream artifact was created. Nothing in the repository contradicts this."
    fp-verdict-overstatement:
      status: unresolved
      notes: "The mounting-conditionality disclosure is genuinely strong - section 1.1 is bold, unhedged, and repeated at sections 1.2, 1.4, 2.6 and 8.1, and the one positive clearance (+2.3316 cm) is reported prominently rather than buried. On the literal question of overstating the STATED premise, the proxy is rejected. It is left unresolved on a narrower point the artifact does not address: the verdict's coverage premise is licensed by a quote whose grammatical subject is the six-crystal COV arrangement, while the requirement is applied to one cylindrical cap. A reader is therefore told the premise is licensed by the published text when what the text licenses is assembly-level coverage. The premise is defensible from the separately published 2-cylinder-plus-4-rectangle architecture, but that derivation is nowhere written down."
  uncertainty_markers:
    weakest_anchors:
      - "The 100 mm cap diameter from arXiv:2508.02488v1 is the single load-bearing geometric number and comes from a TUM commissioning paper outside the ROADMAP anchor list, describing a setup in which only one of six COV crystals was installed"
      - "The COV internal cavity of ~5 cm rests on an unverified cap-rim premise; the loose bound of 16.7 cm does not exclude the wafer, and the two differ by more than a factor of three"
      - "The Goupy 2024 thesis, the only genuinely independent third route to the cavity and the copper support geometry, was never obtained; the acquisition failure is recorded rather than faked"
      - "The single-cap coverage requirement is licensed in the artifacts by an assembly-level quote and is never derived from the published 2-cylinder-plus-4-rectangle architecture"
      - "The orientation-invariant floor of -0.1620 cm is sign-robust only against the 2-significant-figure '100 mm' reading; it spans zero under the 2019 paper's 1-significant-figure 'a diameter of 10 cm'"
    unvalidated_assumptions:
      - "Face-parallel mounting of the wafer, on which the entire -4.3684 cm margin depends"
      - "That the commissioning 100 mm cylindrical crystal and the Chooz cap crystals are the same part"
      - "That a single cylindrical cap, rather than the six-crystal COV arrangement, must cover the wafer footprint"
      - "That the four rectangular 2.5 cm slabs sit inside the cap rim, on which both cavity clearances depend"
    competing_explanations:
      - "The rectangular COV crystals could be substantially larger than the cylindrical caps, giving a cavity above 5 cm and also permitting assembly-level coverage of a footprint no single cap could cover"
      - "The 100 mm crystal could be a commissioning-only part, with larger Chooz cylinders; the paper's own Chooz-identity statement is scoped to the passive shielding and conspicuously does not extend to the COV"
      - "The 2019 'an outer veto (3) with a diameter of 10 cm' may describe the outer-veto assembly rather than a cap crystal, in which case it is not a second statement of the same quantity"
    disconfirming_observations:
      - "arXiv:2508.02488v1 line 218 states that the PASSIVE SHIELDING is identical to the Chooz configuration with one exception, and makes no equivalent statement about the COV; this sentence appears nowhere in any Phase-8 artifact and bears directly on the phase's own named weak point"
      - "The loose cavity bound of +2.3316 cm does not exclude the wafer, and it is the only bound derived from a published Chooz-relevant dimension without a cap-rim premise"
      - "NUCLEUS themselves call the inner-veto-plus-single-hit benefit 'very marginal', which weakens the project's own 'we lose their multiplicity cut' framing; the phase preserves this rather than suppressing it"
      - "The sampled min b2 is reported as 7.3945 cm in 08-03-FIT-DETERMINATION.md but as 7.4210 cm in 08-RESEARCH.md, veto_envelope.py and test_veto_envelope.py, for an identically described run"
comparison_verdicts:
  - subject_id: claim-gate-discharged
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-fit-determination
    comparison_kind: cross_method
    metric: absolute_difference_cm
    threshold: "<= 1e-4 cm"
    verdict: pass
    recommended_action: "No action. Independent multistart Nelder-Mead optimization over SO(3) and independent closed-form arithmetic reproduce every orientation extremum and every clearance in 08-03-FIT-DETERMINATION.md to 6 decimal places."
    notes: "min b2 7.325626 vs (a+t)/sqrt(2) 7.325626; min projected diameter 10.161968 vs sqrt(a^2+t^2) 10.161968; zero-thickness bound 9.578940 vs a/(3sqrt(2)/4) 9.578940; coverage 14.368410 confirmed as the face-circumscribed circle and distinct from the space diagonal 14.369802. The retracted lemma min b2 = a is confirmed FALSE by construction, so the retraction was correct."
  - subject_id: ref-vald09
    subject_kind: reference
    subject_role: decisive
    comparison_kind: baseline
    metric: requirement_scope_match
    threshold: "verdict basis answers the question VALD-09 asks"
    verdict: tension
    recommended_action: "Record in the gate verdict that VALD-09's 'physically fits' question is answered only by the containment comparisons, which are estimates, and that the sign-robust basis is a coverage rather than a containment result."
    notes: "VALD-09 asks whether the wafer PHYSICALLY FITS the COV/IV envelope. The sign-robust verdict basis (-4.3684 cm) is a COVERAGE comparison against a cap outer diameter, not a containment comparison against a cavity. The containment comparisons (-5.1600 and -9.3684 cm) are labelled estimates resting on an unverified premise, and the only containment bound free of that premise is the loose 16.7 cm bound, which gives +2.3316 cm and does not exclude the wafer. The artifact discloses each piece but does not state that the requirement's own question is left resting on estimates."
  - subject_id: ref-self-veto
    subject_kind: reference
    subject_role: decisive
    comparison_kind: cross_method
    metric: absolute_difference
    threshold: "<= 1e-3"
    verdict: pass
    recommended_action: "No action. The wafer's own self-veto quantities reproduce independently."
    notes: "Recomputed A_self_direct directly from data/muon_dRdEdep.csv. Module trapezoid values 1.000000000000 / 0.999971887382 / 0.997858048250 at 10 eV / 1 keV / 100 keV reproduce the reported figures digit for digit, and an independent Simpson quadrature over the same frozen grid gives 0.997819079 at 100 keV, agreeing to 3.9e-05 - a quadrature-rule difference on a 584-point native log grid, not a discrepancy. Denominator closure 1.365237 Hz vs the frozen header 1.3659 Hz is -0.0485%, inside the 1% gate. mult_rejection(1) == 0.0 is exactly True and the occupancy model agrees analytically at N=1 for every p, confirming the identity is model-independent. No NUCLEUS percentage enters as a value."
  - subject_id: claim-sc-coverage
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-roadmap-phase8
    comparison_kind: baseline
    metric: criteria_discharged
    threshold: "5 of 5 with deviations declared"
    verdict: pass
    recommended_action: "No action on the mapping itself."
    notes: "5 of 5 criteria mapped. SC1's evidence-route amendment is justified and independently confirmed: the named source is dimensionally silent, verified by reproducing zero-count greps for 'envelope', 'cavity', 'inner diameter', 'clearance' and '100 mm' against both the arXiv and the published-journal frozen text. SC2's three-tier extension, SC3's derived two-acceptance split and SC4's counting identity all verify in code."
  - subject_id: claim-premise-void
    subject_kind: claim
    subject_role: supporting
    reference_id: ref-roadmap-phase8
    comparison_kind: baseline
    metric: quantified_fluence_change
    threshold: "a computed change in phi_post"
    verdict: inconclusive
    recommended_action: "None within Phase 8. Full Geant4 transport is out of scope by explicit user decision; the artifact already states this as an honesty condition rather than papering over it."
    notes: "The premise-void chain is component-level and physically well-motivated but unquantified, exactly as the artifact declares. The verifier notes independently that the chain's strongest input is the 45.88x payload footprint ratio (103.2256 cm^2 vs the published 2.25 cm^2 array crystal footprint), which is untouched by any cap-diameter dispute."
suggested_contract_checks:
  - check: single_cap_coverage_premise_derivation
    reason: "The verdict's coverage premise is applied to one cylindrical cap but licensed by a sentence whose subject is the six-crystal COV arrangement ('The COV is an arrangement of two cylindrical and four rectangular 2.5 cm thick HPGe crystals... It hermetically covers the cryogenic target detectors'). A decisive check is missing that derives the one-cap requirement from the published 2-cylinder-plus-4-rectangle architecture, and that re-derives the overturning threshold under assembly-level coverage, where a cap of 14.3684 cm and a mass of 2.06 kg would not be required."
    suggested_subject_kind: claim
    suggested_subject_id: claim-gate-discharged
    evidence_path: GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-05-GATE-VERDICT.md
  - check: chooz_transfer_scope_sentence
    reason: "arXiv:2508.02488v1 contains a sentence bounding what its geometry transfers to Chooz - 'the passive shielding described above - and commissioned in this work - is identical to the configuration planned for Chooz, with just one exception: an additional boron carbide (B4C) layer surrounding the target detectors'. It appears in no Phase-8 artifact, is not in the 34-quote evidence block, and is the sharpest available evidence on the phase's own named weak point. It licenses the 29.7 cm and 43.0 cm numbers for Chooz and conspicuously does not extend to the COV, which is where the load-bearing 100 mm lives."
    suggested_subject_kind: claim
    suggested_subject_id: claim-gate-discharged
    evidence_path: data/external/nucleus/2508.02488v1.txt
  - check: outer_veto_vs_cap_crystal_identity
    reason: "veto_envelope._COV_CRYSTAL_DIAMETER's note calls the 2019 'an outer veto (3) with a diameter of 10 cm' and the 2508 '100 mm diameter' 'two published statements of the same quantity'. The 2019 caption attributes the diameter to the outer veto, which the same paper defines as the surrounding kg-scale detector system, not to a cap crystal. A decisive check establishing or retiring the identity is missing. The direction is conservative for the verdict - an assembly reading implies a cavity strictly smaller than 10 cm - but the 'same quantity' framing is unsupported."
    suggested_subject_kind: claim
    suggested_subject_id: claim-gate-discharged
    evidence_path: data/external/nucleus/1905.10258.txt
---

<!-- ASSERT_CONVENTION: metric_signature=not_applicable — no relativistic field theory in this detector/rate pipeline, fourier_convention=not_applicable, natural_units=internal-only (hbar=c=1) for CEvNS cross section; k_B EXPLICIT (not =1); I/O in eV/keV/MeV, counts/kg/day/keV, s, cm/um; (hbar c)^2 = 3.894e-28 GeV^2 cm^2 -->

# Phase 8 Verification — Veto-Envelope Geometry Gate (P-VETO)

**Mode:** initial verification (no prior `08-VERIFICATION.md` existed).
**Contract referenced:** `08-05-PLAN.md#/contract` (the terminal gate plan). Contract IDs from Plans
08-01 through 08-04 are project-local to this ledger and are assessed in the body below.

**Bottom line.** The NO-FIT direction is correct and every number supporting it reproduces
independently. The verdict is not an artifact of a mistaken reading, a wrong constant, or agents
agreeing with each other — I re-grepped the load-bearing dimension from the frozen source myself,
re-derived the orientation minima by independent numerical optimization over SO(3), and re-ran the
test suite. Three gaps remain, all of them about *what the verdict licenses* rather than about
whether it points the right way. None of them would make a re-scope decision wrong; one of them
(the falsification threshold) would make a re-scope decision *under-informed*.

---

## 1. Contract Coverage

| ID | Kind | Status | Basis |
|---|---|---|---|
| `claim-gate-discharged` | claim | **partial** | All arithmetic confirmed; single-cap premise licensing is unestablished |
| `claim-sc-coverage` | claim | passed | All 5 criteria mapped; both deviations declared; SC2/3/4 verified in code |
| `claim-premise-void` | claim | passed | Chain stated with honesty condition; strongest input is untouched by the dispute |
| `claim-phase-disposition` | claim | passed | Dispositions traced to ROADMAP's own dependency text |
| `claim-no-credit-no-redesign` | claim | passed | Verified by direct code inspection, not by the reported sweep |
| `claim-control-returned` | claim | passed | Explicit halt; four options, none adopted |
| `deliv-gate-verdict` | deliverable | passed | Substantive, non-placeholder, internally consistent |
| `test-verdict-falsifiability-carried` | test | **partial** | Overturning list not exhaustive over assembly-level coverage |
| 6 remaining acceptance tests | test | passed | See frontmatter |
| 5 references | reference | completed | All read, used and cited |
| `fp-verdict-overstatement` | proxy | **unresolved** | See §5 |
| 4 remaining forbidden proxies | proxy | rejected | See frontmatter |

**Score: 21/24.**

---

## 2. Computational Verification Details

### 2.1 Independent SO(3) optimization — the retracted lemma and its replacements

The false lemma `min_R b₂(R) = a` was caught during planning. I did not check whether the
retraction was written down; I checked whether the *corrected* values are true, by optimizing over
SO(3) from 400 random starts rather than by uniform sampling.

```python
import numpy as np, math
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation as Rot

a, t = 10.16, 0.20
V = np.array([[sx*a/2, sy*a/2, sz*t/2] for sx in (-1,1) for sy in (-1,1) for sz in (-1,1)])

def bbox_sides(p):
    W = V @ Rot.from_rotvec(p).as_matrix().T
    return np.sort(W.max(0)-W.min(0))[::-1]          # b1 >= b2 >= b3

def proj_diam(p):                                     # shadow diameter on the xy (cap) plane
    W = (V @ Rot.from_rotvec(p).as_matrix().T)[:, :2]
    return max(np.linalg.norm(W[i]-W[j]) for i in range(8) for j in range(i+1,8))

rng = np.random.default_rng(7)
def globalmin(f, n=400):
    best = np.inf
    for _ in range(n):
        x0 = Rot.random(random_state=int(rng.integers(1<<30))).as_rotvec()
        r = minimize(f, x0, method="Nelder-Mead",
                     options=dict(xatol=1e-12, fatol=1e-14, maxiter=20000, maxfev=20000))
        best = min(best, r.fun)
    return best

print("min b2   =", globalmin(lambda p: bbox_sides(p)[1]), " claimed", (a+t)/math.sqrt(2))
print("min b1   =", globalmin(lambda p: bbox_sides(p)[0]), " PR bound", a/(3*math.sqrt(2)/4))
print("min proj =", globalmin(proj_diam),                  " claimed", math.hypot(a, t))
print("sqrt2*a  =", math.sqrt(2)*a, " space diag", math.sqrt(2*a*a+t*t))
```

**Output:**

```output
min b2   = 7.325626184067847  claimed 7.325626184025336
min b1   = 9.666922560731102  PR bound 9.578939985844491
min proj = 10.161968116308225  claimed 10.161968116308225
sqrt2*a  = 14.368410083008046  space diag 14.369802365172598
```

**PASS.** Three separate confirmations:

1. `min b₂ = (a+t)/√2 = 7.3256 cm` is exact to 11 digits, and it is *attained*, not merely
   approached — so the retracted lemma `min b₂ = a = 10.16 cm` is definitively false and the
   retraction was correct.
2. `min over SO(3) of the projected footprint diameter = √(a²+t²) = 10.161968 cm` is exact to full
   precision. The orientation-invariant floor is right.
3. The Prince-Rupert value `a/(3√2/4) = 9.5789 cm` is correctly labelled a **zero-thickness lower
   bound**: my optimizer reaches **9.6669 cm** for the physical `t = 0.20 cm` plate, strictly above
   9.5789 and strictly below the artifacts' "sampling reaches only ≈9.71–9.72". The artifacts'
   bracket `[9.5789, ≲9.72]` is therefore true but loose. This quantity enters no clearance.

### 2.2 The coverage requirement is the right geometric object

This was a named risk: `√2·a = 14.3684` (circumscribed circle of the *face*) versus
`√(2a²+t²) = 14.3698` (circumscribed *sphere*). Both appear in the artifacts.

The face-parallel shadow is exactly a `10.16 × 10.16` square; a circle covering it must have
diameter equal to that square's diagonal, `√2·a = 14.368410`. Confirmed above. `veto_envelope.py`
renames the space diagonal to `space_diagonal()`, its docstring forbids using it as a coverage
requirement, and `comparison_bases()` calls `cover_diameter_face_parallel()`. **No confusion
occurred.** The two differ by 0.0014 cm, which the artifacts correctly identify as why the original
misnomer survived unnoticed.

### 2.3 All six clearances and the sign-robustness endpoints

```output
COVERAGE face-parallel       C = -4.3684   (D=10.0,  W=14.3684)
COVERAGE orient-invariant    C = -0.1620   (D=10.0,  W=10.1620)
EDGE                         C = -0.1600   (D=10.0,  W=10.1600)
CAVITY in-plane              C = -5.1600   (D=5.0,   W=10.1600)
CAVITY diagonal              C = -9.3684   (D=5.0,   W=14.3684)
LOOSE cavity                 C = +2.3316   (D=16.7,  W=14.3684)
coverage ratio 10.0/14.3684 = 0.6960 -> cap 30.4% smaller
requirement/cap = 1.4368 -> 43.7% larger
tight cavity 10.0 - 2*2.5 = 5.0 ;  loose cavity 29.7 - 8.0 - 5.0 = 16.7
area ratios: 103.2256/2.25 = 45.88 ; 103.2256/9 = 11.47
```

**PASS.** Every figure in the gate verdict's §1.2 table reproduces exactly, including the sign of
the single positive number. The §4 endpoint intervals follow arithmetically and I confirmed the two
corrections in §4.1: at ±0.1 cm the EDGE interval is `[−0.26, −0.06]` (sign preserved, by less than
the half-width), and the flip is at `D = 10.16` exactly, giving `+0.04` at `D = 10.2`.

### 2.4 The mass closure that licenses the 100 mm read

```output
volume = pi*(5.0)^2*(2.5) = 196.3495 cm^3
  rho=5.323: m = 1045.17 g  (+4.52% vs 1 kg)
  rho=5.35 : m = 1050.47 g  (+5.05% vs 1 kg)
```

**PASS, and the artifacts' refusal to overclaim is arithmetically correct.** The margin against a
naive ±5 % band is `1050 − 1045.17 = 4.83 g`, and at `ρ_Ge = 5.35` the naive band genuinely fails
(+5.05 %). Both 08-01 and 08-03 state this as "consistent with a 1-significant-figure '1 kg'" and
explicitly forbid "within 5 %". That is the honest statement and it is the one they make.

### 2.5 SC3 and SC4 recomputed from the frozen artifact

```output
grid pts 584   floor 0.01014497 keV   ceiling 197142.0 keV
closure 1.365237318 Hz vs frozen header 1.3659 Hz -> -0.0485%
A_self_direct(0.010 keV) = 1.000000000000
A_self_direct(1.0   keV) = 0.999971887382
A_self_direct(100.0 keV) = 0.997858048250
independent Simpson A(100 keV) = 0.997819079  (vs trapezoid 0.997858048)
A_SELF_INDUCED = 0.0
mult_rejection(1) = 0.0 ; is exactly 0.0: True ; mult_rejection(18) = 0.3757
R_mu = 0.968723 Hz ; f_dead(40us) = 3.87489e-05 ; f_dead(20us) = 1.93745e-05
occupancy model at N=1: eps = 8.9e-16 (p=0.01), 7.8e-16 (p=0.05), 0.0 (p=0.5), 0.0 (p=1.0)
```

**PASS on all four SC3/SC4 questions asked of this verification:**

- `A_self_direct` **is** genuinely derived from the wafer's own chord × Landau–Vavilov deposit
  distribution. The numerator and denominator are both integrals of `data/muon_dRdEdep.csv`. No
  NUCLEUS percentage enters as a value anywhere; an independent Simpson quadrature agrees to
  3.9e-05, which is a quadrature-rule difference on a 584-point log grid, not a discrepancy.
- `A_self_induced ≡ 0` is kept **structurally** separate — a module-level constant with no merging
  function, no merging column, and no merging CSV row. The `fp-lumped-acceptance` guard is real.
- `ε_mult(1) ≡ 0` is a **counting identity**, returned by an early return of the literal and
  asserted under `== 0.0`. The occupancy model's independent agreement at `N = 1` is analytically
  exact (the float evaluation lands at ~1e-15 for small `p`, which is the expected rounding of an
  exact identity). It is derived from "a hit in one and only one of the target detectors", not
  asserted, and the `N = 18` contrast is deliberately kept out of the data table.
- NUCLEUS's own **"very marginal"** assessment — which cuts *against* the project's framing — is
  preserved verbatim in four places: the module docstring, `mult_rejection`'s docstring, the emitted
  CSV header, and gate verdict §3.4. It is not softened and not buried.

### 2.6 Source integrity and quote re-verification

I did not trust the evidence block's claims about itself.

```output
SHA-256 verified against MANIFEST.md:
  OK  1905.10258.html          OK  2401.09837v1.html
  OK  2508.02488v1.html        OK  2509.03559v1.html
  OK  epjc_86_29.html          OK  2509.03559v1_Figure1.png

52 grep commands extracted from 08-01-SOURCE-EVIDENCE.md and re-run:
  46 returned matches; 6 returned nothing — all six are the deliberately
  zero-match commands whose annotated expectation is "# 0" / "no match"
```

**PASS.** The frozen cache is intact and every grep reproduces its annotated expectation. I
independently confirmed the two load-bearing quotes:

- `2508.02488v1.txt:225` — *"It features a cylindrical geometry with 100 mm diameter and 25 mm
  height, and a mass of 1 kg."* The 10.0 cm cap diameter is **real and correctly read.**
- `1905.10258.txt:285` — *"an inner veto (2) and an outer veto (3) with a diameter of 10 cm."*
- `2509.03559v1.txt` and `epjc_86_29.txt` — *"It hermetically covers the cryogenic target
  detectors"*, verbatim and identical in both versions. The coverage premise's licensing quote is
  genuine.
- The Bonner-sphere trap is real and correctly flagged: `2509.03559v1.txt:391` carries
  *"an outer diameter of 10.16 cm and a thickness of 1.27 cm"* for a **Pb shell converter**. It is
  cited nowhere as a veto dimension.

**Minor documentation inaccuracy.** Gate verdict §6 describes the evidence block as "52 grep
commands, all re-running and exiting 0". Six of them exit 1 by design (`grep -c` with zero matches
returns 1). The substance is correct — all 52 reproduce their annotated expectations, including the
zero-count ones that carry the SC1 amendment.

### 2.7 Test suite, run by the verifier

```output
310 passed, 1 warning in 44.12s          (full repository suite)
 89 passed in 2.03s                      (test_veto_envelope + test_wafer_self_veto + test_veto_credit)
```

**PASS.** The claimed "310 passed" is accurate.

### 2.8 SC2 verified in code, not in markdown

```output
n rows = 19 ; tiers = {'L1': 6, 'L1*': 2, 'L2': 11}
distinct credits = [1.0] ; all exactly 1.0 under identity comparison: True
TIERS = ('L1', 'L1*', 'L2')
credit_basis counts = {'policy': 11, 'not-a-rejection-factor': 5, 'context': 2, 'derivation': 1}
module constants: L2_CREDIT=1.0, L1STAR_CREDIT=1.0, L1_REJECTION_CREDIT=1.0
```

**PASS on all three SC2 questions.** All 19 credits are exactly 1.0 *in code*, not only in markdown.
`L1*` is a first-class member of `TIERS` and is **not** folded into `L1`. The single
`credit_basis: derivation` row is `row-b02-multiplicity-cut`, matching the gate verdict's claim that
exactly one row's 1.0 is derived rather than a policy default. `VETO-TAXONOMY.md` §6 describes the
L2-off baseline as *"a different and worse configuration"* and contains an explicit sentence
refusing the word "conservative".

---

## 3. What actually stands, and what does not

This is the question the re-scope decision turns on, so it is stated without hedging.

**Stands without any premise beyond reading the published text:**

- At **every** orientation, the wafer's projected footprint has diameter ≥ 10.1620 cm. Confirmed by
  independent optimization. Reorientation genuinely helps and genuinely does not rescue it.
- The published COV crystal in the commissioning setup is 100 mm × 25 mm, 1 kg, and the arithmetic
  closes.
- The wafer face area is 45.88× the published 3×3 array crystal footprint (103.2256 vs 2.25 cm²).

**Stands under the coverage + face-parallel premises, sign-robust to every published rounding
interval:** the −4.3684 cm coverage shortfall against a single cap.

**Does NOT stand:**

- **Physical containment — the question VALD-09 literally asks.** The tight cavity (5.0 cm) is an
  estimate on an unverified cap-rim premise. The only cavity bound free of that premise is the loose
  16.7 cm bound, which gives **+2.3316 cm and does not exclude the wafer.** The Goupy thesis, the
  only independent route, was never obtained. **Without the cavity estimate, there is no
  sign-robust containment result at all.** The phase says each of these things; it does not assemble
  them into the sentence "the requirement's own question rests on estimates".
- The 43 %-larger-cap falsification argument, as a complete falsification (see §4).

---

## 4. Discrepancies Found

### D1 — The single-cap coverage premise is licensed by an assembly-level quote **(significant)**

This is the fourth item in the direction that favours the expected conclusion, which the objective
asked me to look for specifically.

The source sentence, verified verbatim in both frozen versions, is:

> "The COV is an arrangement of two cylindrical and four rectangular 2.5 cm thick HPGe crystals
> mechanically held within a Cu support structure... **It** hermetically covers the cryogenic target
> detectors"

The grammatical subject of "hermetically covers" is **the six-crystal arrangement**. The gate
verdict (§1, premise 1) and `comparison_bases()`'s `coverage` premise string apply the requirement to
**one cylindrical cap**. No Phase-8 artifact derives the one-cap requirement from the published
2-cylinder-plus-4-rectangle architecture — and the evidence block is aware of that architecture
(A.10) and even notes elsewhere that a cylindrical-crystal statement "does *not* license anything
about the four rectangular COV crystals".

The premise is **defensible**: with two cylinders and four rectangles, the top of a face-parallel
wafer is plausibly covered only by the top cap. But it is defensible from the *architecture*, not
from the *hermeticity* sentence, and that derivation is nowhere written down.

**Material consequence for the re-scope decision.** Gate verdict §1.4 and §2.6 item 3 tell the user
that overturning the verdict requires a published cap of ≥ 14.3684 cm, implying ~2.06 kg against the
published 1 kg, "a change that would be visible in any published mass statement". **That argument
closes only the single-cap route.** Under assembly-level coverage, a Chooz COV whose four
rectangular crystals extend past the cap rim could hermetically cover a 10.16 cm footprint with **no
14.37 cm cap and no 2.06 kg mass anywhere**. The falsification list is therefore not exhaustive over
the ways the coverage basis can fail, and the user is being told the verdict is harder to overturn
than it is.

### D2 — The paper's own Chooz-transfer sentence is absent from every Phase-8 artifact **(significant)**

`data/external/nucleus/2508.02488v1.txt` line 218 reads:

> "It is important to note that the passive shielding described above – and commissioned in this
> work – is identical to the configuration planned for Chooz, with just one exception: an additional
> boron carbide (B4C) layer surrounding the target detectors."

I grepped every Phase-8 artifact, the evidence block, the taxonomy and the three modules. **This
sentence appears nowhere.** It is not among the 34 quotes. It bears directly on §2.1 — the phase's
own named weak point, "does a TUM commissioning paper legitimately constrain the Chooz payload?" —
and it cuts both ways:

- It **licenses** the 29.7 cm internal shielding and 43.0 cm bore for Chooz explicitly. The phase
  left that corroboration unclaimed.
- It **conspicuously does not extend to the COV.** The paper takes care to draw a Chooz-identity
  boundary around the passive shielding and does not draw one around the cryogenic outer veto — in
  the same section that says only one of six COV crystals was installed. That is the sharpest
  available evidence on whether the load-bearing 100 mm transfers, and it points *against* the
  transfer.

This is a missed **disconfirming** check, not a confirmation-pressure error. It does not overturn
the verdict — the 2019 "10 cm" and the 2026 Chooz paper's independent 2.5 cm thickness still
support the transfer — but the phase's central caveat should have been argued from this sentence
rather than from the general observation that the paper is about TUM.

### D3 — "Outer veto diameter" is registered as a cap-crystal diameter **(minor)**

`veto_envelope._COV_CRYSTAL_DIAMETER.note` calls the 2019 "a diameter of 10 cm" and the 2508
"100 mm" *"two published statements of the same quantity"*. The 2019 caption attributes the 10 cm to
**the outer veto**, which the same paper defines as "a surrounding kg-scale cryogenic detector used
as outer veto" — i.e. plausibly the assembly, not one crystal.

Direction check: if the *whole* outer veto is 10 cm across, the cavity is strictly smaller and the
no-fit case is *stronger*. So this is **conservative**, not confirmation-pressure. But the "same
quantity" framing is unsupported and the corroboration is weaker than described.

### D4 — Two different sampled minima reported for the same run **(minor)**

`08-03-FIT-DETERMINATION.md` §2.1 reports the sampled `min b₂` as **7.3945** cm; `08-RESEARCH.md`
§F1, `veto_envelope.py:386` and `tests/test_veto_envelope.py:24` all report **7.4210** cm — for a
run described identically in both places (2 × 10⁵ uniform SO(3), seed 20260722). One is a
transcription slip. Non-load-bearing: both are one-sided sanity values above the exact infimum
7.325626, which I confirmed directly.

### D5 — The `min b₁` bracket's upper end is loose **(minor)**

The artifacts state the physical minimum lies in `[9.5789, ≲9.72]`. My optimizer reaches
**9.6669 cm**, so the bracket is true but not tight. Enters no clearance and no assertion, exactly as
the artifacts say.

### D6 — "all re-running and exiting 0" **(trivial)**

Six of the 52 grep commands exit 1 by design. See §2.6.

---

## 5. Forbidden Proxy Audit

| Proxy | Status | Finding |
|---|---|---|
| `fp-veto-credit-transfer` | rejected | No NUCLEUS percentage enters as a value. Only `99.8` occurrence is inside a labelled not-applied quote |
| `fp-reduced-credit` | rejected | 19/19 credits exactly 1.0; 1.0 correctly documented as the *empty* credit |
| `fp-resized-veto` | rejected | Resized-veto vocabulary appears only where the prohibition is stated |
| `fp-continue-past-failed-gate` | rejected | No Phase 9 work exists; §8.3 halt is accurate |
| `fp-verdict-overstatement` | **unresolved** | See below |
| `fp-lumped-acceptance` (08-02) | rejected | `A_self_direct` and `A_SELF_INDUCED` structurally unmergeable |
| `fp-multiplicity-softening` (08-02) | rejected | Exactly 0.0 under identity comparison; never called "small" in place of zero |
| `fp-presupposed-verdict` (08-03) | rejected | The `stop_and_rethink` escalation condition is real and would have fired on a positive coverage clearance |
| `fp-merged-cavity-number` (08-03) | rejected | Two separately named constants; test asserts no merged constant exists; both bounds reported |
| `fp-unlabelled-area-ratio` (08-03) | rejected | `area_ratio()` raises `ValueError` without a basis; verified by inspection |
| `fp-l2off-as-conservative` (08-04) | rejected | Taxonomy §6 explicitly refuses the word |

**On `fp-verdict-overstatement`.** The disclosure discipline here is unusually strong and I want to
say so plainly: §1.1 is bold and unhedged, the mounting premise is restated at five separate points,
the one positive clearance is given its own prominent paragraph rather than a footnote, and §1.3
puts the premise-free statement under a heading that says why it is *not* the verdict basis. A
reader of the gate verdict alone **cannot** reasonably mistake −4.37 cm for a purely geometric
result — the objective's check #4 comes back clean on the overclaim side, and clean on the
underclaim side too (the +2.3316 cm number is not buried; it is in §1.2's table, §1.2's prose and
§5).

I leave the proxy unresolved on the narrower point of D1 only: the reader is told the coverage
premise is licensed by the published text, and what the published text licenses is assembly-level
coverage.

---

## 6. Confirmation-Pressure Audit

The objective asked for a fourth error in the direction that favours no-fit. The three known ones
are the false F1 lemma, the unlabelled "~9 cm²" footprint, and the misattributed array-mass
provenance.

**Found: D1** — the single-cap coverage premise. It makes the requirement stronger than the source
sentence supports, and its downstream effect (the "43 % larger cap ⇒ 2.06 kg ⇒ would be visible"
falsification) makes the verdict look harder to overturn than it is. Same direction as the other
three.

**Checked and clean:**

- The 2019/2508 conflation (D3) runs the *other* way — it makes `D_available` generous.
- Using the weakest (1-s.f.) reading to downgrade the edge and orientation-invariant bases is
  conservative *against* the phase's own conclusion. Under the primary source's own 2-s.f. "100 mm",
  the orientation-invariant floor **is** sign-robust (`[−0.212, −0.112]`); the phase declines to
  claim that. That is anti-confirmation-pressure behaviour and it is worth crediting.
- §10's note that omitting a mounting/clamp allowance is "conservative **in the direction of a
  fit**" is correct.
- The +2.3316 cm loose bound is reported, not suppressed.
- D2 is a missed disconfirming check, i.e. the opposite failure mode.

---

## 7. Requirements Coverage

**VALD-09 (GATING).** Discharged, with one scope tension recorded as a comparison verdict: VALD-09
asks whether the wafer **physically fits**; the sign-robust verdict basis answers a **coverage**
question. The containment answer rests on estimates.

**Confirmed open follow-up.** The gate verdict flags that the unlabelled "~9 cm²" figure survives
outside PITFALLS.md. I verified all five occurrences persist: `GPD/REQUIREMENTS.md` lines 49 and
114, `GPD/ROADMAP.md` lines 105, 121 and 315. The flag is accurate and the decision not to edit them
in Phase 8 is a scope decision, not drift.

---

## 8. Expert Verification Required

1. **COV mechanical architecture** (cryogenic detector engineering). Whether a two-cylinder /
   four-rectangle HPGe arrangement can hermetically cover a 10.16 cm square footprint without a cap
   crystal of ≥ 14.37 cm. Decides whether D1 is cosmetic or material. No computational check can
   settle it; it needs either the Goupy thesis or someone who has seen the hardware.
2. **Chooz-vs-commissioning COV part identity** (NUCLEUS collaboration knowledge). Whether the
   100 mm cylinder is a commissioning part. D2 gives the sharpest textual evidence; a definitive
   answer needs the collaboration or the thesis.
3. **Whether coverage is the right efficacy criterion at all.** A veto's rejection power degrades
   continuously with partial coverage rather than failing at a geometric threshold. The
   binary "covers / does not cover" framing is a modelling choice this phase does not defend.

---

## 9. Confidence Assessment

| Item | Rating | Basis |
|---|---|---|
| Arithmetic and closed forms | **independently confirmed** | Reproduced to 6–11 digits by independent optimization and computation |
| The 10.0 cm cap diameter as a *read* | **independently confirmed** | Re-grepped from the frozen source; SHA-verified; mass closure reproduced |
| Orientation minima and the retraction | **independently confirmed** | Multistart SO(3) optimization, not sampling |
| SC2 / SC3 / SC4 | **independently confirmed** | Recomputed from the frozen artifact; code inspected directly |
| Test suite and source integrity | **independently confirmed** | 310 passed; 6/6 SHA-256 match; 52/52 greps reproduce |
| The 10.0 cm as a *Chooz* dimension | **structurally present only** | Rests on a commissioning paper whose Chooz-identity claim excludes the COV (D2) |
| Single-cap coverage premise | **unable to verify** | Not derivable from any published sentence I could find (D1) |
| Physical containment | **unable to verify** | Cavity is an estimate; the premise-free bound does not exclude |

**Overall confidence: MEDIUM.**

To be precise about what that rates, because a single word is not enough here:

- Confidence that **every number in the phase is correct as computed**: HIGH.
- Confidence that **the no-fit direction is right**: HIGH. Even collapsing D1 and D2 entirely, the
  wafer's every-orientation shadow exceeds the only published cap dimension, and the payload is
  45.9× the published crystal footprint.
- Confidence that **the −4.3684 cm figure means what the falsification section says it means**:
  MEDIUM. That is what D1 costs.
- Confidence that **the wafer physically does not fit the cavity**: LOW, and the phase says so.

**The re-scope decision is safe to make.** The milestone-void argument in §4 does not actually
depend on the contested cap diameter — its load-bearing input is the 45.9× payload-footprint change,
which forces the copper support and the B₄C liner arrangement to be redesigned regardless of how
the coverage comparison resolves. That is a stronger foundation than the one the gate verdict leans
on, and the user should know it.

---

## 10. Gaps Summary

| # | Subject | Severity | Fix |
|---|---|---|---|
| G1 | `claim-gate-discharged` / `test-verdict-falsifiability-carried` — single-cap premise (D1) | significant | Derive the one-cap requirement from the published 2-cyl + 4-rect architecture, or restate the premise as assembly-level; either way re-derive the overturning threshold, since the 2.06 kg argument does not close the assembly route |
| G2 | `claim-gate-discharged` — missing Chooz-transfer sentence (D2) | significant | Add `2508.02488v1.txt:218` to the evidence block; use it to license 29.7/43.0 cm for Chooz and to sharpen §2.1's caveat on the COV |
| G3 | Outer-veto vs cap-crystal identity (D3) | minor | Retire "two published statements of the same quantity" in `veto_envelope._COV_CRYSTAL_DIAMETER.note`, or establish the identity |
| G4 | Sampled `min b₂` inconsistency (D4) | minor | Reconcile 7.3945 vs 7.4210 |
| G5 | `min b₁` bracket loose (D5) | minor | Optional: tighten `≲9.72` to `≲9.67` |
| G6 | "all exiting 0" (D6) | minor | Reword to "all reproduce their annotated expectations" |

**Root-cause grouping.** G1 and G3 share a root cause: the phase treats published statements about
the COV *assembly* and about individual *crystals* as interchangeable. G1 is the harmful direction,
G3 the conservative one. Fixing the assembly/crystal distinction once addresses both.

---

## 11. Gap Closure — appended 2026-07-22

**All six gaps are closed.** The full disposition, with evidence and reproduced numbers, is
`GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-VERIFICATION-GAPCLOSURE.md`.

| # | Disposition | Evidence |
|---|---|---|
| **G1** | **CLOSED — both halves.** The single-cap requirement is derived in a new `08-03` §3.1 with its inferential step marked (the derivation newly uses A.1's *"directly above the target detectors"* placement clause, plus new evidence entry A.20), **and** the premise is restated as assembly-level with the overturning threshold **re-derived into two routes**. Route A (single cap ≥ 14.3684 cm ⇒ 2.06 kg) remains closed by published evidence. **Route B (assembly-level) is NOT closed: it needs only 24.6858 cm² of non-cap projection out to a 2.1842 cm radial reach beyond the cap rim, and no published source constrains the rectangular crystals' lateral dimensions, placement or mass.** The 2.06 kg argument is no longer presented as covering both. | `08-03` §0/§3/§3.1/§9 item 3; `08-05` §1/§1.4/§2.3/§2.6/§8.1/§8.2; `veto_envelope.comparison_bases()`; new unit test |
| **G2** | **CLOSED.** `2508.02488v1.txt:218` added as evidence entry **A.18** with three recorded commands (quote, mechanical subject extraction, negative COV check). Used in **both** directions: it licenses 29.7 / 43.0 cm for Chooz explicitly, and its conspicuous non-extension to the COV now carries the phase's central caveat. | `08-01` A.18; `08-03` §1.1/§1.2/§9/§10; `08-05` §2.1/§8.1; two constant notes in code |
| **G3** | **CLOSED by retirement.** New evidence entry **A.19** records the 2019 paper's own definition of component (3) as *"a surrounding kg-scale cryogenic detector"*. The "two published statements of the same quantity" note is retired; a unit test asserts the phrase survives only inside its retraction. Direction confirmed conservative. | `08-01` A.19; `08-03` §1.3; `veto_envelope._COV_CRYSTAL_DIAMETER.note` |
| **G4** | **CLOSED — and the diagnosis refined.** Not a transcription slip: **two different runs**, proven by the projected diameter (10.1623 vs 10.2039), which no transcription error can move. Canonical run re-run once and reproduced exactly: **min b₁ 9.7076, min b₂ 7.3945, min proj Ø 10.1623**. Propagated everywhere and pinned by assertion. | `08-03` §2.1; `08-RESEARCH` §F1 second addendum; `veto_envelope.py`; `tests/test_veto_envelope.py` |
| **G5** | **CLOSED — tightened to an ATTAINED value.** Multistart Nelder–Mead reproduces **9.666923 cm** at a **cubic** bounding box (PR zero-thickness bound 9.578940, excess +0.0880). Bracket `[9.5789, ≲9.72]` → "attains ≈ 9.667". Locked in by a new test. | `08-03` §2.1/§6.3; `08-RESEARCH` §F1; `veto_envelope.min_bbox_largest_side` |
| **G6** | **CLOSED.** Corrected to "all **57** commands reproduce their annotated expectations"; **7 exit 1 by design**. Warning added at the source in `08-01` §G so it cannot be reintroduced. Revised totals: **37 quotes / 57 commands**. | `08-05` §6/§8.1; `08-01` §G |

**Verdict status after closure: UNCHANGED.** NO FIT, coverage basis, C = −4.3684 cm. No clearance,
closed form or sign-robustness endpoint was recomputed differently. The two honesty conditions this
verification credited — the declined 2-s.f. sign-robustness claim, and the prominence of the single
positive +2.3316 cm — were checked after the edits and are intact.

**Milestone-void argument status: UNCHANGED, and now stated on its actual foundation.** This
verification's §9 observation — that the §4 chain's load-bearing input is the **45.88× payload
footprint change**, not the contested cap diameter — is now written into `08-05` §4 as a boxed
statement ahead of the chain, with its provenance table (103.2256 cm² vs the published 2.25 cm²
array-crystal footprint, the latter confirmed by two independent mass closures). None of G1–G6
touches it.

**Full repository test suite after closure: 313 passed** (was 310; three tests added, none removed
or weakened).

> **This section does NOT re-grade the verification.** The frontmatter ledger above
> (`status: gaps_found`, `score: 21/24`, and the `partial` / `unresolved` entries for
> `claim-gate-discharged`, `test-verdict-falsifiability-carried` and `fp-verdict-overstatement`) is
> the **verifier's own record of the state at verification time** and is deliberately left
> untouched by the correcting pass. Re-grading is a verification action, not an execution one. A
> re-verification of this phase should read §11 and
> `08-VERIFICATION-GAPCLOSURE.md` and reach its own conclusion — including on the two items where
> this pass **narrowed a claim rather than establishing one**: the single-cap premise is now
> *labelled* an inference rather than *shown* to be true (G1 step 4 remains unpublished), and the
> assembly-level overturning route is now *quantified and disclosed* rather than *excluded*.
