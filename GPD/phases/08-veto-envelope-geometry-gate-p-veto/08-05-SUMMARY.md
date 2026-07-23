---
phase: 08-veto-envelope-geometry-gate-p-veto
plan: 5
plan_contract_ref: GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-05-PLAN.md#/contract
title: "VALD-09 discharged NO FIT on the sign-robust coverage basis (-4.3684 cm, mounting-conditional), all five success criteria mapped with two flagged deviations, the milestone premise reported VOID, Phases 10 and 11 identified as site-independent survivors, and control returned to the user"
date: 2026-07-22
status: complete
depth: full
completed: 2026-07-22
one_liner: "Discharged the VALD-09 gating stop-condition with a NO FIT verdict routed through the coverage comparison -- a face-parallel wafer needs a cap crystal of sqrt(2)*10.16 = 14.3684 cm against a published COV cap outer diameter of 10.0 cm (arXiv:2508.02488v1 Sect. 2, corroborated arXiv:1905.10258 Fig. 8), clearance -4.3684 cm, the cap 30.4% smaller than required and the requirement 43.7% larger than the cap, sign-preserved at every published rounding endpoint (+/-0.05 -> [-4.418, -4.318]; +/-0.10 -> [-4.468, -4.268]; the wide 1-s.f. +/-0.50 -> [-4.868, -3.868]) and flipping only at a cap diameter of 14.3684 cm -- while carrying BOTH premises with the number rather than beneath it (the cap must cover the wafer footprint; the wafer is mounted face-parallel) and stating in the same paragraph that -4.37 cm is robust to dimension rounding but NOT to orientation, since the orientation-invariant projection floor sqrt(a^2+t^2) = 10.1620 cm gives only -0.1620 cm which is not sign-robust, so neither leg of the argument is simultaneously premise-free and sign-robust and no downstream artifact may present -4.37 cm as a purely geometric result; reported the premise-free edge comparison (-0.1600 cm) as corroboration only with its explicit flip threshold of a 10.16 cm cap and the published 1-significant-figure reading 'a diameter of 10 cm' under which it becomes +0.340 cm, and reported the +2.3316 cm LOOSE cavity bound prominently rather than suppressing it because it is exactly why the loose route cannot carry a verdict; labelled both cavity shortfalls (-5.1600 and -9.3684 cm) as estimates resting on an unverified cap-rim premise, confirmed that no clearance on any of the four named bases came out positive so the escalation condition was not triggered, and stated what the 4.37 cm margin does license (a confident no-fit under the mounting premise) and does not (a purely geometric no-fit, any statement about the unconstrained vertical cavity axis, or any quantitative claim about how much phi_post would change); disclosed the evidence-route amendment in full -- ROADMAP Success Criterion 1 as literally worded cannot be discharged because EPJC 86,29 Fig. 1 was confirmed by direct inspection of all six panels of the frozen 1875x2613 image to carry no scale bar, no ruler, no dimension leader and no numeric dimension callout, and the paper states no envelope, cavity, inner-diameter or clearance dimension anywhere in either the arXiv v1 or the published journal version -- and disclosed that the substituted load-bearing source arXiv:2508.02488 was promoted to a Phase-8 anchor during execution, is ABSENT from the ROADMAP anchor list, and describes the TUM commissioning setup with only one of six COV crystals installed rather than Chooz; mapped all five success criteria to named discharging artifacts, sections and acceptance tests with the SC1 evidence-route amendment and the SC2 binary-to-three-tier L1* extension both flagged as deviations from the criteria as written, SC3 showing the two separately reported acceptances (A_self_direct = 1.000000000000 / 0.999971887382 / 0.997858048250 at 10 eV / 1 keV / 100 keV against A_self_induced = 0.0 exactly) and never a lumped one, and SC4 citing the unit-tested eps_mult(1) == 0.0 early-return identity asserted under exact identity comparison and shown model-independent, together with NUCLEUS's own 'very marginal' counterpoint which makes the absolute cost of that zero handle small and cuts against this project's framing; attached the footprint basis label to every quotation of VALD-09's area comparison (2.25 cm^2 published crystal basis giving 45.9x versus the ~9 cm^2 project holder-scale estimate giving 11.5x, the latter not a NUCLEUS number) and flagged as an open follow-up that GPD/REQUIREMENTS.md and the ROADMAP anchor line still carry the unlabelled figure, without editing either file; reported the milestone premise as VOID with its component-level physical chain -- a wafer this size forces a redesign of the cryogenic outer veto, the copper support structure and the nearly-4pi 4 cm B4C liner, and plausibly the 29.7 cm internal shielding and the 43.0 cm cryostat bore, which are exactly the components shaping the fields around the target, so phi_post at the detector position is no longer NUCLEUS's phi_post and essentially nothing beyond room-level environmental quantities transfers -- with the explicit honesty condition that this reasoning is physically well-motivated but is NOT QUANTIFIED anywhere in the phase; gave a per-phase disposition for all of Phases 9 through 16 argued from each phase's stated Depends-on and Anchor-coverage rows rather than the dependency arrows, surfacing that Phases 10 and 11 carry NO NUCLEUS anchor at all in their contract rows and survive intact (grid extension, response matrices, the 0.5 eV trigger sigmoid; omega-bar and the Debye-Waller convention from the Ge VDOS and the IA broadening) despite the ROADMAP drawing an 8 -> 10 arrow which the ROADMAP itself concedes is scheduling policy rather than physics, and naming the recoverable fragments of the six non-surviving phases including the fact that Phase 15's L1 environmental inputs (2.92 m.w.e. overburden, 1.41 attenuation, measured 5.03 cm^-2 s^-1 VNS gamma ambience) DO transfer; named all nine surviving deliverables individually; asserted both locked prohibitions with their 2026-07-22 user-decision attribution and verified by sweep that no veto credit other than exactly 1.0 appears in any Phase-8 output and that resized-veto vocabulary occurs only inside the two prohibition statements themselves, with the guard's known blind spot (an anonymous inline literal) stated so it is not mistaken for a proof; and closed by returning control to the user with four candidate re-scope directions and their tradeoffs listed and NONE adopted, quoting the REQUIREMENTS.md statement that revisiting the wafer format is a stop-condition rather than an optimization trigger and stating what the unobtained Goupy thesis would resolve (the rectangular COV crystal dimensions and the copper support geometry, converting the cavity from bounded to read) alongside the realistic expectation that even so it would have to show larger CAP crystals to touch the verdict."
provides:
  - "GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-05-GATE-VERDICT.md -- the Phase-8 gate verdict: the determination with both premises and its sign-robustness table, the mounting-conditionality statement with the -0.16 cm orientation-invariant floor, all five clearance bases including the one positive (non-excluding) loose bound, the margin's licensing statement, the limits paragraph and the six overturning conditions, the five-criterion coverage map with two flagged deviations, the footprint basis labels and the REQUIREMENTS/ROADMAP discrepancy flag, the premise-void statement with its unquantified-magnitude caveat, the per-phase disposition of Phases 9-16, the nine surviving deliverables, the two prohibitions with their sweep result, and four candidate re-scope directions listed without adoption"
contract_results:
  claims:
    claim-gate-discharged:
      status: passed
      summary: "The VALD-09 gate is discharged with a NO FIT verdict resting on the coverage comparison from Plan 08-03. Verdict section 1 names the comparison (required cap diameter versus published cap outer diameter), the source dimension with arXiv id and section (arXiv:2508.02488v1 Sect. 2 'Cryogenic Outer Veto', 100 mm, independently corroborated by arXiv:1905.10258 Fig. 8), BOTH premises (a cap crystal must cover the wafer footprint, licensed by evidence-block A.11's 'hermetically covers'; and face-parallel mounting), and the signed clearance -4.3684 cm. Sign-robustness is demonstrated by a table of the clearance re-evaluated at every published rounding endpoint, with the flip threshold stated as a cap diameter of 14.3684 cm (half-width 4.3684 cm). Section 1.1 states the mounting-conditionality in the same place and gives the orientation-invariant floor sqrt(a^2+t^2) = 10.1620 cm with its clearance of -0.1620 cm and the explicit statement that THAT number is not sign-robust. Section 1.3 carries the premise-free edge comparison as corroboration only, with the 1-s.f. interval [-0.660, +0.340] that makes it positive. Sections 1.2 and 1.3 label both cavity clearances as estimates and state that the verdict rests on neither. Section 1.4 states what the margin licenses and what it does not. Nothing is stated more confidently than Plan 08-03 established; several statements are weaker (e.g. the 1045.17 g mass closure is reported as consistent with a 1-s.f. '1 kg' rather than 'within 5%')."
      linked_ids: [deliv-gate-verdict, test-verdict-stated, test-verdict-falsifiability-carried, ref-fit-determination, ref-vald09]
    claim-sc-coverage:
      status: passed
      summary: "All five ROADMAP Phase 8 success criteria are mapped in verdict section 3 to a named discharging artifact, a named section, and named acceptance test ids drawn from the upstream plans. Criterion 1's row records the evidence-route amendment as a deviation, with section 3.1 reproducing the two Plan 08-01 determinations that force it (Fig. 1 carries no scale bar or dimension callout on any of six panels; the paper states no envelope/cavity/inner-diameter/clearance dimension anywhere, in both the arXiv v1 and the published version) and disclosing that the substituted source is an off-anchor-list TUM commissioning paper. Criterion 2's row records the L1* extension as a deviation, with section 3.2 explaining that the binary split has no slot for a payload-geometry-coupled passive liner and that forcing one would flatter the background budget at the disputed point. Criterion 3's row shows the two separately reported acceptances and section 3.3 gives them as four distinct numbers, never lumped. Criterion 4's row cites the unit-tested identity (early return, exact identity comparison, model-independence) rather than a description. Criterion 5 is discharged by this document's sections 4-8. Section 3.5 attaches the footprint basis label to VALD-09's area comparison in both bases and flags the REQUIREMENTS.md / ROADMAP discrepancy as an open follow-up without editing those files."
      linked_ids: [deliv-gate-verdict, test-sc-mapping-complete, ref-roadmap-phase8, ref-fit-determination, ref-taxonomy, ref-self-veto]
    claim-premise-void:
      status: passed
      summary: "Verdict section 4 reports the milestone premise as VOID with a five-step physical chain naming the specific components forced into redesign -- the cryogenic outer veto, the copper support structure, the nearly-4pi 4 cm boron carbide liner, and plausibly the 29.7 cm internal shielding and the 43.0 cm cryostat bore -- observing that these are exactly the components shaping the neutron and gamma fields immediately around the target position, and drawing the consequence that the post-shield fluence at the detector position is no longer NUCLEUS's post-shield fluence so essentially nothing beyond room-level environmental quantities transfers. The four surviving room-level quantities are named. The section closes with an explicit blocked-out honesty condition stating that the reasoning is physically well-motivated but is NOT QUANTIFIED anywhere in this phase: no one computed how much phi_post would change, the argument is component-level rather than a transport calculation, and a referee could reasonably demand the number."
      linked_ids: [deliv-gate-verdict, test-premise-statement, ref-fit-determination, ref-roadmap-phase8]
    claim-phase-disposition:
      status: passed
      summary: "Verdict section 5 gives a disposition row for each of Phases 9 through 16, each justified by quoting or citing that phase's stated ROADMAP Depends-on and Anchor-coverage entries rather than the dependency arrows. Phases 10 and 11 are identified as site-independent survivors with the argument made rather than asserted: neither carries a single NUCLEUS anchor in its Anchor-coverage row (Phase 10 lists only v1.0 grid and response machinery, CONVENTIONS E/F, the saturation onsets and the 24 v1.0/v1.1 anchors; Phase 11 lists NCrystal Ge_sg227, DarkELF, Sears, Campbell-Deem, SuperCDMS and frozen v1.0 spectra), and their deliverables are properties of germanium and the QPD response chain. The contradiction with the ROADMAP's 8 -> 10 arrow is surfaced explicitly, together with the ROADMAP's own concession that Phase 10's grid work is nominally site-independent and is merely not scheduled ahead of the gate. Phases 9, 13, 14 and 16 are VOID and Phases 12 and 15 do not survive in their current form, each with its stated dependency quoted; recoverable fragments are named for 12, 14 and 15, including the finding that Phase 15's L1 environmental anchors (overburden, attenuation, measured VNS gamma ambience) DO transfer because they are properties of the site."
      linked_ids: [deliv-gate-verdict, test-disposition-justified, ref-roadmap-phase8]
    claim-no-credit-no-redesign:
      status: passed
      summary: "Verdict section 7 states both prohibitions explicitly as block quotes and attributes both to the locked user decision of 2026-07-22, citing where it is recorded (ROADMAP Phase 8 forbidden proxies, Risk Register, Backtracking Triggers; REQUIREMENTS.md VALD-09). It states that the transferable credit remains exactly 1.0 and that this would remain true on a fit verdict, because a fit alone does not earn credit without a derived wafer-specific veto acceptance which no Phase-8 plan is scoped to produce. The automated sweep was executed over all seven Phase-8 outputs and its result is recorded in the same section: all 19 taxonomy credit cells read exactly 1.0; L2_CREDIT = L1STAR_CREDIT = L1_REJECTION_CREDIT = 1.0 in code with no other *CREDIT*/*REJECTION*/*VETO_FACTOR* constant holding another value; the sole textual occurrence of 99.8 is inside the verbatim B.9 quotation labelled not applied and is never a NUMBER token; and resized-veto vocabulary occurs in exactly two places, both of which are the prohibition being stated. The guard's known blind spot (an anonymous inline literal such as rate / 5) is stated so the sweep is not mistaken for a proof."
      linked_ids: [deliv-gate-verdict, test-no-credit-no-redesign, ref-taxonomy, ref-vald09]
    claim-control-returned:
      status: passed
      summary: "Verdict section 8 returns the decision to the user in the required order: the verdict in one sentence with its clearance and source; its single most important limitation (mounting-conditionality, with the secondary limitation of commissioning-paper provenance and the unobtained Goupy thesis); the surviving deliverables; and the disposition summary distinguishing the two surviving phases from the six that do not survive. Section 8.2 lists all four candidate re-scope directions in a tradeoff table with an explicit statement that none is adopted or recommended and that the choice is the user's. Direction 2 quotes the REQUIREMENTS.md Out-of-Scope entry verbatim, including its statement that VALD-09 showing incompatibility is a stop-condition rather than an optimization trigger, and notes that surfacing the option is not recommending it. Direction 4 states specifically what the Goupy thesis would resolve (the rectangular COV crystal dimensions and the copper support geometry, converting the cavity from bounded to read) and, so the option is not oversold, that it would additionally have to show larger cap crystals to touch the verdict. Section 8.3 records the halt: no Phase 9 work started, no downstream artifact created, no direction adopted, verdict not softened. The plan returns status checkpoint."
      linked_ids: [deliv-gate-verdict, test-control-returned, ref-vald09, ref-roadmap-phase8]
  deliverables:
    deliv-gate-verdict:
      status: passed
      path: GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-05-GATE-VERDICT.md
      summary: "The Phase-8 gate verdict document. Every must_contain item is present and was checked by grep: the verdict sentence with its comparison, source dimension, both premises and signed clearance (Sect. 1); the explicit robust-to-rounding-but-conditional-on-mounting statement with the -0.1620 cm orientation-invariant floor (Sect. 1.1, restated 1.2, 1.4, 2.6 item 5, 8.1); the margin's size and what it does and does not license (Sect. 1.4); the five-criterion coverage table with artifact, section and test per row (Sect. 3); both deviations flagged as deviations from the criteria as written (Sect. 3.1, 3.2); the premise-void statement with its physical reason and unquantified-magnitude caveat (Sect. 4); a per-phase disposition row for each of Phases 9 through 16 with justification (Sect. 5); the nine surviving deliverables named individually in a table (Sect. 6); the no-reduced-credit and no-resized-veto assertions with their sweep result (Sect. 7); and four candidate re-scope directions listed with tradeoffs and explicitly not adopted (Sect. 8.2). No number in the document originates outside a completed Phase-8 artifact."
      linked_ids: [claim-gate-discharged, claim-sc-coverage, claim-premise-void, claim-phase-disposition, claim-no-credit-no-redesign, claim-control-returned, test-verdict-stated, test-verdict-falsifiability-carried, test-sc-mapping-complete, test-premise-statement, test-disposition-justified, test-no-credit-no-redesign, test-control-returned]
  acceptance_tests:
    test-verdict-stated:
      status: passed
      summary: "PASS (hybrid). The verdict statement was compared line by line against Plan 08-03's Sect. 0, Sect. 3 clearance table, Sect. 4 sign-robustness table, Sect. 5 bound separation and Sect. 6 verdict. It names the coverage comparison, the source dimension with arXiv id and section, BOTH premises, and the signed clearance -4.3684 cm, and states that the sign survives the stated dimension-precision interval by reproducing the endpoint intervals rather than asserting robustness. It states the mounting-conditionality and gives the orientation-invariant floor of -0.1620 cm in the same section and again in the closing decision brief. It does not present an estimated cavity shortfall as the verdict basis: both cavity rows carry an (ESTIMATE) label and Sect. 1.2/1.3 state that the verdict rests on neither. It does not present the edge comparison as decisive: Sect. 1.3 is titled 'why it is not the verdict basis' and reproduces the [-0.660, +0.340] 1-s.f. interval. It does not present -4.37 cm as orientation-invariant anywhere; the sentence '-4.37 cm is not a purely geometric result' appears in bold at Sect. 1.1. Verified by grep: 'face-parallel' appears 6 times, '-0.1620' 5 times, '-4.3684' 4 times."
      linked_ids: [claim-gate-discharged, deliv-gate-verdict, ref-fit-determination]
    test-verdict-falsifiability-carried:
      status: passed
      summary: "PASS (hybrid). All six overturning conditions named in Plan 08-03 Sect. 9 are carried into verdict Sect. 2.6 with their scope preserved -- including that items 1, 2 and 4 touch only the cavity rows and not the verdict, that item 3 is quantified (a 43% larger cap implies 2.06 kg against the published 1 kg), that item 5 collapses the margin to the non-sign-robust -0.1620 cm and is the single most efficient disconfirming observation, and that item 6 was tested and did not occur (anchors agree to 6.6%). The unobtained Goupy 2024 thesis is named in Sect. 2.2 as the only genuinely independent third route, with what its absence costs stated explicitly (no independent corroboration of the cavity exists) and with the Fig. 1(e) pixel measurement explicitly denied the status of a third route. Sect. 2.3 identifies the approximately 5 cm cavity claim as the weakest anchor in the phase and then names what stands independently of it: the verdict itself (no cavity assumption), the taxonomy, the multiplicity identity, and the self-veto decomposition."
      linked_ids: [claim-gate-discharged, deliv-gate-verdict, ref-fit-determination]
    test-sc-mapping-complete:
      status: passed
      summary: "PASS (hybrid). All five criteria have a coverage row naming an artifact, a section and acceptance test ids; the test ids were taken from the upstream plan summaries rather than invented (08-01: test-fig1-silence; 08-03: test-four-bases, test-sign-robustness, test-dmin-arithmetic, test-bound-separation, test-orientation-invariance, test-amendment-documented, test-verdict-falsifiable; 08-02: test-normalization-closure, test-acceptance-monotone, test-split-reported, test-induced-zero-named, test-no-transferred-percentage, test-multiplicity-identity, test-counterpoint-recorded; 08-04: test-taxonomy-complete, test-verbatim-classification, test-credit-sentinel, test-no-orphan-veto-factor, test-l1star-documented). No criterion is marked discharged without a named artifact. Criterion 1's row and Sect. 3.1 record the evidence-route amendment as a deviation; Criterion 2's row and Sect. 3.2 record the L1* extension as a deviation; Criterion 3's row and Sect. 3.3 show four separate acceptance numbers and no lumped one; Criterion 4's row cites the unit-tested identity. Sect. 3.5 carries both footprint bases with their provenance (2.25 cm^2 published crystal basis -> 45.9x; ~9 cm^2 project holder-scale estimate -> 11.5x, disowned as a NUCLEUS number) and records as an open follow-up that GPD/REQUIREMENTS.md VALD-09 and the ROADMAP Phase-8 anchor line still carry the unlabelled figure. Neither file was edited."
      linked_ids: [claim-sc-coverage, deliv-gate-verdict, ref-roadmap-phase8, ref-fit-determination, ref-taxonomy, ref-self-veto]
    test-premise-statement:
      status: passed
      summary: "PASS (hybrid). The no-fit branch applies (the coverage clearance is negative and sign-robust), so the premise-void form of this section was written. Verdict Sect. 4 names the cryogenic outer veto, the copper support structure and the nearly-4pi 4 cm boron carbide liner as forced into redesign, and plausibly the internal shielding (29.7 cm) and the cryostat bore (43.0 cm), with a reason attached to each. It observes that these are exactly the components that shape the neutron and gamma fields immediately around the target, and draws the consequence that the post-shield fluence at the detector position is no longer NUCLEUS's, so essentially nothing beyond room-level environmental quantities transfers -- with those four surviving quantities named. The unquantified-magnitude caveat is a separate blocked statement rather than a clause."
      linked_ids: [claim-premise-void, deliv-gate-verdict]
    test-disposition-justified:
      status: passed
      summary: "PASS (hybrid). Every phase from 9 to 16 has a disposition row whose justification cites that phase's stated ROADMAP dependencies or anchors, quoted where the ROADMAP's own wording is decisive (Phase 9's Depends-on row says 'this phase is void' in the ROADMAP's own words; Phase 13's Anchor-coverage row names 'phi_post from Phase 9' directly; Phase 12's and Phase 15's Depends-on rows name Phase 9 for the normalization and the ambience respectively; Phase 16's names all four upstream phases). Phases 10 and 11 are identified as site-independent survivors with the germanium-VDOS / shared-grid / QPD-response-chain reason given, and the argument is made from the absence of any NUCLEUS anchor in their Anchor-coverage rows rather than asserted. The contradiction with the ROADMAP's dependency arrows is stated in a call-out above the table, together with the ROADMAP's own concession that Phase 10's grid work is nominally site-independent and merely not scheduled ahead of the gate. No disposition rests on the arrows alone."
      linked_ids: [claim-phase-disposition, deliv-gate-verdict, ref-roadmap-phase8]
    test-no-credit-no-redesign:
      status: passed
      summary: "PASS (automated). The sweep was run over all seven Phase-8 outputs: 08-05-GATE-VERDICT.md, 08-03-FIT-DETERMINATION.md, GPD/analysis/VETO-TAXONOMY.md, 08-01-SOURCE-EVIDENCE.md, and src/qpd_potential/{veto_envelope,wafer_self_veto,veto_credit}.py. (1) A regex sweep for any credit assigned a value other than 1.0 returned zero hits. (2) All 19 taxonomy credit cells were extracted and every one reads exactly '**1.0**' (19/19). (3) L2_CREDIT, L1STAR_CREDIT and L1_REJECTION_CREDIT are all literal 1.0 in veto_credit.py, and the only other matching identifier is the string tuple CREDIT_BASES, not a numeric constant. (4) The only textual occurrence of 99.8 or 0.998 across the three modules is wafer_self_veto.py line 183, inside the verbatim B.9 quotation in the A_SELF_INDUCED docstring, which the upstream tokenize-based test already proved is never a NUMBER token. (5) A sweep for resized/scaled-up/enlarged/hypothetical veto vocabulary returned hits only inside the two prohibition statements themselves (08-03 Sect. 10 and 08-05 Sect. 7) plus the Success-Criterion-5 restatement row. No proposed, scaled or hypothetical veto dimension exists anywhere. The verdict document states both prohibitions explicitly and attributes them to the locked user decision of 2026-07-22. Full repository suite: 310 passed."
      linked_ids: [claim-no-credit-no-redesign, deliv-gate-verdict, ref-taxonomy, ref-vald09]
    test-control-returned:
      status: passed
      summary: "PASS on its inspectable content; the human-review portion is discharged by the checkpoint this plan returns. Verdict Sect. 8.2 lists all four candidate directions in a tradeoff table -- adopt room-level environmental inputs only and design an independent shield; revisit the wafer format; retarget to a different host experiment whose envelope accommodates a 10.16 cm plate; obtain the Goupy thesis first -- with an explicit statement that none is adopted and that the choice is the user's. Direction 2 quotes the REQUIREMENTS.md Out-of-Scope entry verbatim including 'which is a stop-condition, not an optimization trigger', and adds that surfacing the option is not recommending it and that choosing it would require the user to reverse a recorded scoping decision. Direction 4 states what the thesis would resolve (rectangular COV crystal dimensions and copper support geometry; cavity from bounded to read) and states the realistic expectation that it would additionally have to show larger cap crystals to touch the verdict. Sect. 8.1 reproduces the verdict without softening. Sect. 8.3 records that no Phase 9 work was started and no downstream artifact created. The plan returns status checkpoint, not completed-and-continuing."
      linked_ids: [claim-control-returned, deliv-gate-verdict, ref-vald09]
  references:
    ref-fit-determination:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Read in full and used as the sole source of the verdict; cited by section number throughout (Sect. 0, 1, 1.2, 2.2, 3, 4, 4.1, 4.2, 5, 6, 7, 9, 10). Nothing was recomputed. Two places where the temptation to strengthen was resisted and the weaker upstream form kept: the mass closure is reported as consistent with a 1-significant-figure '1 kg' rather than 'within 5%' (the naive band is cleared by only 4.8 g and fails at rho_Ge = 5.35), and the Prince-Rupert bound is not quoted at all since it enters no clearance."
    ref-taxonomy:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Read in full and used for the Criterion 2 coverage row, the L1* deviation statement in Sect. 3.2, the component list in the premise-void chain (rows a09 and b04 for the liner), the Criterion 4 derivation row, and the surviving-deliverables table. Its credit constants are what the no-reduced-credit assertion was checked against: 19/19 rows read exactly 1.0, and src/qpd_potential/veto_credit.py's three module constants are literal 1.0. Cited as the deliverable Phase 16 requires for its mandatory L2-off baseline and as an artifact correct either way."
    ref-self-veto:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Read via 08-02-SUMMARY.md and used for the Criterion 3 and Criterion 4 coverage rows. The two-number acceptance split is shown as four distinct values in verdict Sect. 3.3 (A_self_direct at three thresholds plus A_self_induced = 0.0) with an explicit statement that they describe two different populations and are never merged; no single lumped acceptance appears anywhere in the verdict. The denominator closure (1.365237 Hz vs the frozen header 1.3659 Hz, -0.0485%) and the f_dead lower-bound labels are carried."
    ref-roadmap-phase8:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Read for the Phase 8 Success Criteria 1-5, the Phase Dependencies table, the wave schedule with its Phase-8 gate note, and every Phase 9-16 Goal / Depends-on / Requirements / Contract-Coverage / Success-Criteria block. Used to build both the five-criterion coverage map and the per-phase disposition, which is argued from the stated Depends-on and Anchor-coverage rows and quotes the ROADMAP where its own wording is decisive. Cited for the two prohibitions (Phase 8 forbidden proxies, Risk Register, Backtracking Triggers) and for the concession that Phase 10's grid work is nominally site-independent."
    ref-vald09:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Read in GPD/REQUIREMENTS.md and used as the gating stop-condition this plan discharges. Its area comparison is quoted with the basis label attached in both bases, and the fact that REQUIREMENTS.md still carries the unlabelled figure is flagged as an open follow-up rather than edited. The locked user decisions it carries are cited as the attribution for both prohibitions and for the return of control. The REQUIREMENTS.md Out-of-Scope entry stating that VALD-09 showing geometric incompatibility is a stop-condition rather than an optimization trigger is quoted verbatim in re-scope direction 2."
  forbidden_proxies:
    fp-veto-credit-transfer:
      status: rejected
      notes: "Rejected. No inherited veto credit is assigned anywhere in the verdict document. The COV factor 5, the >99.8% MV+COV figure and the multiplicity cut appear only as classified NUCLEUS statements being explained or as quantities being denied transfer -- never as a multiplicative factor. The sweep confirms no credit other than exactly 1.0 exists in any Phase-8 output."
    fp-reduced-credit:
      status: rejected
      notes: "Rejected and stated as a prohibition. No partial veto credit, no best-guess surviving rejection and no for-reference rejection value appears in the verdict. Sect. 7 states the prohibition explicitly, attributes it to the locked user decision of 2026-07-22, and gives the reason: a number placed in this artifact for reference would be reused as though established, and no derivation exists behind any partial value."
    fp-resized-veto:
      status: rejected
      notes: "Rejected and stated as a prohibition. No modified, resized, scaled-up, sketched or costed veto geometry is proposed or evaluated anywhere. The 14.3684 cm figure appears only as the threshold for overturning the verdict, explicitly labelled as such in Sect. 1.4, 2.6 item 3 and 7. The vocabulary sweep found resized-veto language only inside the two prohibition statements themselves."
    fp-continue-past-failed-gate:
      status: rejected
      notes: "Rejected. No Phase 9 work was begun -- no environment transcription, no digitization, no mcpd_to_dru, no inversion, no phi_post -- and no downstream artifact was created. No re-scope direction was adopted or recommended; all four are listed as options for the user with their tradeoffs. Sect. 8.3 records the halt explicitly and the plan returns status checkpoint."
    fp-verdict-overstatement:
      status: rejected
      notes: "Rejected structurally. The -4.37 cm clearance is never presented as orientation-invariant: Sect. 1.1 carries the bold statement that it is not a purely geometric result, and the mounting premise is restated at Sect. 1, 1.2, 1.4, 2.6 and 8.1. The estimated cavity shortfalls carry an (ESTIMATE) label in the clearance table and are explicitly excluded as verdict bases. The edge comparison is placed in a section titled 'why it is not the verdict basis' with its 1-s.f. positive interval reproduced. The commissioning-paper provenance of the load-bearing 100 mm dimension is disclosed in Sect. 2.1 and again in Sect. 3.1, including that arXiv:2508.02488 is absent from the ROADMAP anchor list."
  uncertainty_markers:
    weakest_anchors:
      - "The primary coverage clearance of -4.3684 cm holds only under a face-parallel mounting premise; the orientation-invariant floor sqrt(a^2+t^2) = 10.1620 cm gives only -0.1620 cm, so the verdict's robustness is partly a mounting assumption rather than pure geometry"
      - "The load-bearing 100 mm cap diameter comes from arXiv:2508.02488, a TUM commissioning paper that is NOT in the ROADMAP anchor list and describes a setup with only one of six COV crystals installed"
      - "Both published statements of the cap diameter are low-precision ('100 mm' at 2 s.f., 'a diameter of 10 cm' at 1 s.f.), so the premise-free edge comparison is not sign-robust and is carried only as corroboration"
      - "The claim that the COV internal cavity is approximately 5 cm is the weakest link in the phase; the verdict basis avoids depending on it, but the quoted cavity shortfalls of -5.16 and -9.37 cm do not"
      - "The Goupy 2024 thesis, the only genuinely independent third route to the cavity and the copper support geometry, was never obtained, so no independent corroboration exists"
      - "The site-independence of Phases 10 and 11 is a judgement argued from their stated inputs and the absence of NUCLEUS anchors in their Anchor-coverage rows; it is not a statement the ROADMAP makes, and the ROADMAP's dependency table draws an 8 -> 10 arrow that contradicts it on its face"
      - "The vertical axis of the COV cavity is entirely unconstrained by available sources; this determination speaks only to the in-plane, coverage and diagonal requirements"
    unvalidated_assumptions:
      - "That a forced veto redesign would materially change the post-shield fluence at the detector position -- physically well-motivated at the component level, but not quantified anywhere in this phase"
      - "That no downstream phase consumes a NUCLEUS-derived normalization not visible in its ROADMAP contract coverage; the disposition rests on the contract rows being complete descriptions of each phase's inputs"
      - "That the four rectangular 2.5 cm COV slabs sit inside the 10 cm cap rim, which is what the two cavity estimates depend on"
      - "That the commissioning COV crystal and the Chooz cap crystals are the same part, supported only by the matching 2.5 cm / 25 mm thickness and the 10 cm / 100 mm diameter agreement across three papers"
    competing_explanations:
      - "A reviewer could argue the wafer could be sited outside the COV envelope entirely, accepting the loss of the veto while retaining the passive shield -- which is close to re-scope direction 1 and is a decision for the user, not a finding this phase may adopt"
      - "A reviewer could argue the 100 mm crystal is commissioning-only and the Chooz caps are larger; this is weakened by the independent 2.5 cm thickness in the 2026 paper and the independent 10 cm in the 2019 paper, and quantified by the 2.06 kg mass consequence, but it is not excluded"
      - "A reviewer could argue that Phase 12 should be classed as surviving, since the reactor-CEvNS signal depends on site geometry rather than veto geometry; the disposition marks it as not surviving IN ITS CURRENT FORM because its stated Depends-on names Phase 9 for the normalization and duty lock, and the recoverable fragment is named rather than suppressed"
    disconfirming_observations:
      - "A published statement that the wafer would be mounted other than face-parallel would collapse the verdict's margin to the non-sign-robust -0.1620 cm and make the coverage determination INCONCLUSIVE rather than no-fit; this is the single most efficient way to disconfirm the current framing"
      - "The Goupy thesis being obtained and showing rectangular COV crystals giving a cavity of at least 10.16 cm in two axes would overturn both cavity clearances outright, though it would additionally have to show cap crystals of at least 14.3684 cm to touch the verdict itself"
      - "A published Chooz cap crystal of at least 14.3684 cm diameter -- more than 43% larger than the published 100 mm, implying about 2.06 kg against the published 1 kg -- would bring the coverage clearance to zero and overturn the verdict"
      - "A downstream phase marked void turning out to have no NUCLEUS-environment dependency, or a phase marked surviving turning out to consume one, would invalidate the corresponding disposition row"
      - "Had the Plan 08-03 coverage clearance come out positive, or lost its sign inside its stated precision interval, the plan's stop_and_rethink condition would have fired and the disposition and premise sections would have had to be rewritten for the fit branch; the clearance is -4.3684 cm and sign-preserved at every published endpoint, so this did not fire"
comparison_verdicts:
  - subject_id: claim-gate-discharged
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-fit-determination
    comparison_kind: benchmark
    metric: signed_clearance_agreement
    threshold: "exact restatement of the Plan 08-03 clearance with no strengthening of its confidence"
    verdict: pass
    recommended_action: "Treat VALD-09 as discharged NO FIT and halt the milestone pending the user's re-scope decision. Do not carry the -4.37 cm figure downstream without its face-parallel mounting premise attached."
    notes: "Every clearance quoted in the verdict document matches 08-03-FIT-DETERMINATION.md exactly: coverage -4.3684 cm, orientation-invariant floor -0.1620 cm, edge -0.1600 cm, cavity estimates -5.1600 and -9.3684 cm, loose bound +2.3316 cm, ratios 30.4% and 43.7%, endpoint intervals [-4.418, -4.318] / [-4.468, -4.268] / [-4.868, -3.868] and [-0.660, +0.340]. Nothing was recomputed and nothing was strengthened; two statements were deliberately kept weaker than a naive reading of the source would allow (the 1-s.f. mass-closure framing, and the omission of the Prince-Rupert bound which enters no clearance)."
  - subject_id: claim-sc-coverage
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-self-veto
    comparison_kind: benchmark
    metric: acceptance_values_reproduced
    threshold: "the two acceptances reported separately and matching data/wafer_self_veto.csv exactly"
    verdict: pass
    recommended_action: "Carry A_self_direct forward as the wafer's only derived muon-rejection number if any re-scope retains a muon channel; never pair it with an inherited veto credit and never merge it with A_self_induced."
    notes: "A_self_direct = 1.000000000000 / 0.999971887382 / 0.997858048250 at 10 eV / 1 keV / 100 keV and A_self_induced = 0.0 are reproduced in the verdict's Criterion 3 row as four separate values with no lumped acceptance anywhere, together with the -0.0485% denominator closure against the frozen header."
---

# Plan 08-05 Summary — VALD-09 discharged: NO FIT, milestone premise void, control returned

## The one-sentence result

**The wafer does not fit.** A face-parallel 10.16 cm wafer needs a COV cap crystal of 14.3684 cm to
be covered; the published cap is 10.0 cm; the clearance is **−4.3684 cm** and keeps its sign across
every rounding interval either published source can support — but that robustness comes from the
**mounting premise**, not from geometry, which alone delivers only −0.1620 cm and is *not*
sign-robust.

## Key results

| Quantity | Value | Status |
|---|---|---|
| **Verdict** | **NO FIT** | VALD-09 discharged; stop-condition triggered |
| Verdict basis | COVERAGE: √2·a = 14.3684 cm vs D = 10.0 cm | face-parallel + coverage premises |
| **Signed clearance** | **−4.3684 cm** | `[CONFIDENCE: HIGH]` for the sign under the mounting premise; sign preserved at every published endpoint |
| Orientation-invariant floor | √(a²+t²) = 10.1620 cm → **−0.1620 cm** | `[CONFIDENCE: LOW]` for the sign — flips at half-width 0.162 cm |
| Edge (premise-free corroboration) | 10.1600 vs 10.0 → −0.1600 cm | `[CONFIDENCE: LOW]` — positive under the published 1-s.f. reading |
| Cavity in-plane / diagonal | −5.1600 / −9.3684 cm | **ESTIMATES** — unverified cap-rim premise |
| Loose cavity bound | +2.3316 cm | the one positive number; **does not exclude the wafer** |
| Cap deficit | 30.4 % smaller than required; requirement 43.7 % larger | from the coverage ratio 0.6960 |
| Transferable veto credit | **exactly 1.0** | unchanged; would be 1.0 on a fit verdict too |
| Downstream phases surviving | **2 of 8** (Phases 10, 11) | site-independent by their contract rows |

## Confidence, calibrated

- `[CONFIDENCE: HIGH]` — **the direction of the result under the face-parallel premise.** Three
  independent checks: the clearance keeps its sign at every endpoint of both published precision
  intervals; the 100 mm read is corroborated by a second paper six years earlier and by an
  independent mass closure (1045.17 g vs a published "1 kg"); and overturning it would require a
  2.06 kg cap crystal against a published 1 kg.
- `[CONFIDENCE: MEDIUM]` — **the no-fit conclusion as a statement about the physical apparatus.**
  Unchecked failure mode: the mounting premise. Remove it and the determination becomes
  *inconclusive*, not a fit. The load-bearing dimension is also from a commissioning paper outside
  the anchor list, and no independent third source was obtained.
- `[CONFIDENCE: LOW]` — **the cavity shortfalls (−5.16, −9.37 cm).** They rest on an unverified
  cap-rim premise and the verdict deliberately rests on neither.
- `[CONFIDENCE: MEDIUM]` — **the phase disposition.** Argued from the ROADMAP's stated contract
  rows, which is the best available evidence, but it assumes those rows completely describe each
  phase's inputs.

## What was NOT established, stated plainly

1. **How much φ_post would actually change under a forced redesign.** Nobody computed it. The
   premise-void argument is component-level and physically well-motivated; it is not a transport
   calculation, and full Geant4 transport is out of scope by user decision.
2. **The COV internal cavity as a read dimension.** It remains bounded between an unverified ~5 cm
   tight estimate and a 16.7 cm loose bound that differ by more than a factor of three and only one
   of which excludes the wafer. The Goupy thesis was never obtained.
3. **The cavity's vertical axis.** Entirely unconstrained by available sources.
4. **Whether the Chooz cap crystals are the same part as the commissioning crystal.** Supported
   only by matching thickness and diameter statements across three papers.

## Two things that cut against this project's own framing

Reported because they are true, not despite it:

1. **NUCLEUS call the multiplicity cut "very marginal."** The wafer's multiplicity rejection is
   exactly zero — but because the handle *they* gain from that cut is itself very marginal, the
   **absolute background cost of losing it is small.** That weakens the "we lose their multiplicity
   cut" argument.
2. **`A_self_direct` ≈ 1 is the easy half.** The wafer being an excellent self-tagger for
   through-going muons follows from a 1.2323 MeV MPV against eV-scale thresholds. It is not an
   achievement, and it does not offset `A_self_induced` = 0.

## Deviations

**None of Rules 1–6 was triggered by this plan.** Two deviations are *reported* rather than
introduced — both were made upstream and are carried into the verdict as flagged deviations from
the ROADMAP criteria as written:

- **Success Criterion 1's evidence route was amended** (Plan 08-03 §1). The named source is
  dimensionally silent, established by direct inspection of all six panels of the frozen figure and
  by exhaustive token enumeration of both the arXiv and published versions. The substituted
  load-bearing source, arXiv:2508.02488, was promoted to a Phase-8 anchor during execution, is
  **absent from the ROADMAP anchor list**, and describes the **TUM commissioning setup, not Chooz**.
- **Success Criterion 2's binary L1/L2 split was extended to three tiers** (Plan 08-04 §2.1). The
  binary split has no slot for a payload-geometry-coupled passive liner.

One **open follow-up flagged, not fixed**: `GPD/REQUIREMENTS.md` (VALD-09) and the `GPD/ROADMAP.md`
Phase-8 anchor line still carry the unlabelled "~9 cm²" footprint figure, which is a project
holder-scale estimate and not a NUCLEUS number. Editing those files is out of scope for Phase 8 by
the phase-context decision; the verdict document records the discrepancy so the requirement and the
gate verdict do not silently disagree.

## Verification evidence

| Check | Result |
|---|---|
| `gpd validate plan-preflight 08-05-PLAN.md` | `validation_passed: True`, no blocking conditions, no warnings |
| Full repository test suite | **310 passed** |
| Prohibition sweep — credit ≠ 1.0 across all 7 Phase-8 outputs | 0 hits |
| Taxonomy credit column | 19/19 cells read exactly `**1.0**` |
| `L2_CREDIT` / `L1STAR_CREDIT` / `L1_REJECTION_CREDIT` | all literal `1.0` |
| `99.8` / `0.998` in the three modules | 1 hit, `wafer_self_veto.py:183`, inside the verbatim B.9 quotation labelled not-applied |
| Resized/scaled-veto vocabulary sweep | hits only inside the two prohibition statements themselves |
| Number provenance | every quantity in the verdict traced to an upstream Phase-8 artifact; none generated here |

## Reproducibility

- Python 3.11, pytest (repo default), macOS/Darwin 25.3.0. No random numbers drawn by this plan.
- No computation was performed. The sweep commands are plain `grep`/`pytest` invocations recorded
  in the acceptance-test summaries above.

## Status of the phase

**Phase 8 is content-complete and HALTED at its designed terminus.** All five ROADMAP success
criteria are discharged, all five plans have shipped their deliverables, and the plan returns
`status: checkpoint` with a `checkpoint:decision`. **No work proceeds until the user chooses a
re-scope direction.** The four candidate directions, with tradeoffs and none adopted, are in
`08-05-GATE-VERDICT.md` §8.2.
