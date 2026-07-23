---
phase: 08-veto-envelope-geometry-gate-p-veto
plan: 4
plan_contract_ref: GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-04-PLAN.md#/contract
title: "The binding L1 / L1* / L2 rejection taxonomy: 19 verbatim-quoted rows all at credit 1.0, the L1* tier introduced as a documented extension of ROADMAP SC2, the credits placed in code as named 1.0 sentinels behind a two-rule guard demonstrated to fire on both violation types, and the factor-5 / footprint / Fig.-8 errors corrected in PITFALLS.md"
date: 2026-07-22
status: complete
depth: full
completed: 2026-07-22
one_liner: "Wrote GPD/analysis/VETO-TAXONOMY.md as the binding three-tier classification of every NUCLEUS rejection and attenuation statement Phase 8 catalogued -- 19 rows, each carrying a verbatim quoted sentence, its section, its 08-01 evidence-block id, its tier, what does transfer, a rejection credit of exactly 1.0, a credit basis, and a one-line swap-test justification -- with all 25 recorded grep commands re-run against the frozen sources and 25/25 reproducing their quoted string; introduced L1* (passive but payload-geometry-coupled) as an EXPLICITLY LABELLED extension of ROADMAP Success Criterion 2's binary split, assigned the nearly-4pi 4 cm B4C liner and the internal shielding to it with the argument that the published ~5x suppression is quoted for a liner in the direct vicinity of a centimetre-scale payload against a wafer face 45.9x larger on the crystal basis (11.5x on the holder basis), stated plainly that promoting them to L1 would flatter the background budget at exactly the point where the wafer's size is the disputed quantity, and recorded the reviewer's counter-argument and the observation that would collapse L1* into L1 rather than suppressing them; kept the three distinct factor-5 statements of section 5.2.1 as three separate rows in three different roles -- the passive B4C attenuation (L1*), the COV anti-coincidence (L2, the genuine rejection), and the Geant4 deposited-energy downscaling (L2, credit basis not-a-rejection-factor, the statement an LLM summarizer returned when asked for 'factor 5' during research); marked row-b02-multiplicity-cut's credit of 1.0 as BY DERIVATION rather than by policy default, citing Plan 08-02's eps_mult(1) == 0.0 early-return counting identity and its model-independence, and made veto_credit.multiplicity_rejection_is_zero() CONSUME that derivation by calling wafer_self_veto.mult_rejection(1) rather than restating the zero; placed L2_CREDIT = L1STAR_CREDIT = L1_REJECTION_CREDIT = 1.0 in src/qpd_potential/veto_credit.py as named module-level floats with PEP-258 attribute docstrings citing Phase 8 and VALD-09 and stating that 1.0 means the background is UNCHANGED, behind a frozen TaxonomyRow dataclass whose __post_init__ raises on any credit != 1.0 and a credit_for() that raises KeyError on any uncatalogued statement, so a rejection factor cannot be obtained without naming a classified statement and receiving 1.0; built the repository guard from two decidable rules -- a tokenize-based NUMBER-token denylist on 99.8/0.998 (a string in a docstring is a STRING token and is correctly excluded) and a namespace naming rule requiring every module-level numeric constant matching *CREDIT*/*REJECTION*/*VETO_FACTOR* to equal exactly 1.0 -- and DEMONSTRATED it rather than assumed it: it fires on an injected 0.998 literal (naming file and line), on an injected COV_REJECTION = 5.0, and on an injected partial L2_CREDIT = 0.2, and stays silent on Plan 08-03's COV_CRYSTAL_THICKNESS_CM = 2.5, B4C_THICKNESS_CM = 4.0 and the wafer's LZ = 0.20 both in a fixture and in the real veto_envelope.py and wafer_geometry.py; named the Phase-16 baseline 'NUCLEUS's shielding without NUCLEUS's vetoes', stated it is a different and WORSE configuration than either NUCLEUS or an independently optimized shield and never a conservative subset, quoting the section 5.2.2 trade-off sentence (newly quoted by this plan, command recorded and re-run) whose leg (ii) is explicitly 'when combined with the COV', with an automated check that every occurrence of the word conservative in the taxonomy is either inside the verbatim NUCLEUS quote or inside the prohibition sentence; and made three dated, sourced, in-place corrections to GPD/literature/PITFALLS.md -- every factor-5 occurrence now carries an [F5-a]/[F5-b]/[F5-c] label naming which of the three section-5.2.1 statements it is, the ~9 cm^2 array footprint is labelled a project holder-scale estimate and explicitly disowned as a NUCLEUS number alongside the published 2.25 cm^2 crystal footprint with its two mass closures (4.996 mm and 5.008 mm edges), every area ratio now carries a basis label, and a cross-phase handoff records the Fig. 8 caption evidence that the left panels are passive-only and the right panels are the veto detectors, instructing Phase 9 to digitize the passive-only trace because reading a post-veto curve as pre-veto would import an L2 credit through the digitization -- all verified by 32 new tests with the full suite at 310/310 and no regressions."
provides:
  - "GPD/analysis/VETO-TAXONOMY.md -- the binding three-tier taxonomy: tier definitions and the swap test, the ROADMAP SC2 extension statement, 19 classified rows with verbatim quotes, the L1* justification with its counter-argument, the multiplicity row's derivation, the L2-off baseline framing, all 25 reproduction commands, and the carried uncertainty markers"
  - "src/qpd_potential/veto_credit.py -- L2_CREDIT / L1STAR_CREDIT / L1_REJECTION_CREDIT = 1.0 with attribute docstrings citing Phase 8 and VALD-09; a frozen TaxonomyRow dataclass that raises on any credit != 1.0; TAXONOMY keyed by the 19 stable row ids; lookup/tier_of/credit_for/rows_in_tier; and multiplicity_rejection_is_zero() consuming Plan 08-02's derivation"
  - "tests/test_veto_credit.py -- 32 tests: credit sentinels under exact comparison, attribute-docstring citation checks, taxonomy/code id round-trip, per-row schema checks, verbatim re-grep of eight sampled rows spanning all three tiers plus a re-run of every recorded command, the two-rule repository guard with three fire demonstrations and two silence demonstrations, the L1* documentation check, the conservative-word check, and the three PITFALLS correction checks"
  - "GPD/literature/PITFALLS.md -- three dated Phase-8 corrections in place: the factor-5 disambiguation with [F5-a]/[F5-b]/[F5-c] labels on every occurrence, the basis-labelled array footprint with the published 2.25 cm^2 value, and the Fig. 8 trace-selection handoff to Phase 9"
contract_results:
  claims:
    claim-taxonomy-binding:
      status: passed
      summary: "GPD/analysis/VETO-TAXONOMY.md classifies 19 statements into L1 (6), L1* (2) and L2 (11). Every row carries a verbatim quoted sentence, a section reference, its 08-01-SOURCE-EVIDENCE.md id, a tier, what does transfer, a rejection credit of exactly 1.0, a credit basis, and a one-line swap-test justification. Coverage of evidence-block section B is machine-checked: every B.n heading in 08-01-SOURCE-EVIDENCE.md is either a taxonomy row or is explicitly recorded in section 3.1 as carrying no row with the reason. Exactly one entry falls in the latter class -- B.13, the NUCLEUS payload masses, which is a payload-mass statement rather than a rejection or attenuation statement and is the object the swap test replaces. Rows sourced from evidence-block section A (A.8 external shield stack, A.9 internal shielding, A.12 the IV's purpose) are included because the plan's coverage list requires them; the remaining section-A entries are geometry statements consumed by Plan 08-03. No statement appears twice (19 distinct quote cells, 19 distinct row ids, matching the 19 keys of veto_credit.TAXONOMY)."
      linked_ids: [deliv-taxonomy, test-taxonomy-complete, test-verbatim-classification, ref-evidence-block-tax, ref-nucleus-2026-tax, ref-roadmap-sc2]
    claim-l1star-tier:
      status: passed
      summary: "L1* is defined as 'passive but payload-geometry-coupled', its credit is 1.0 alongside L2, and both members -- row-a09-internal-shielding-b4c and row-b04-b4c-attenuation-factor5 -- are assigned to it. The justification is argued rather than asserted: the published ~5x suppression is quoted for a nearly-4pi liner in the direct vicinity of a centimetre-scale payload, the published 3x3 crystal footprint is 2.25 cm^2 against the wafer's 103.2256 cm^2 face (45.9x on the crystal basis, 11.5x on the holder basis), and the quoted value is an event-rate reduction in CaWO4 detectors, so it embeds a target response as well as a geometry. The document states explicitly that ROADMAP Success Criterion 2 specifies a binary split, quotes SC2's own wording, declares that this document EXTENDS it to three tiers, and says plainly that promoting these rows to L1 would flatter the background budget at exactly the point where the wafer's size is the disputed quantity. The competing explanation is recorded rather than suppressed -- a reviewer could argue 4 cm of B4C attenuates neutrons regardless of what sits behind it -- together with the response that the PUBLISHED value is geometry-coupled and that L1* records the disagreement rather than deciding it by fiat, and with the disconfirming observation that would collapse L1* into L1. A recomputation of the liner's attenuation for the wafer's own geometry would be a derived L1 quantity and would not require reclassifying the row; that route is stated explicitly."
      linked_ids: [deliv-taxonomy, deliv-credit-module, test-l1star-documented, ref-research-08-tax, ref-nucleus-2026-tax]
    claim-credit-in-code:
      status: passed
      summary: "L2_CREDIT, L1STAR_CREDIT and L1_REJECTION_CREDIT are module-level floats equal to exactly 1.0 in src/qpd_potential/veto_credit.py, asserted under exact comparison (value == 1.0, type is float, repr == '1.0') rather than a tolerance. Each carries a PEP-258 attribute docstring -- extracted by ast in the test, not by grep -- citing Phase 8 and VALD-09 and stating the reason; L2_CREDIT and L1STAR_CREDIT both state that 1.0 MEANS THE BACKGROUND IS UNCHANGED so nobody reads 1.0 as full credit. The module docstring states that changing either constant away from 1.0 requires a wafer-specific veto geometry and a documented argument and is expected to appear as a reviewable diff. TAXONOMY covers all 19 row ids with no gaps or extras (set equality against the markdown, both directions), credit_for() returns 1.0 for every one, tier_of() and the credit basis round-trip against the markdown cells, and credit_for() on an uncatalogued id raises KeyError naming the taxonomy. The frozen TaxonomyRow dataclass raises ValueError on any credit != 1.0, so a partial credit is refused by the constructor and not only by the tests. veto_credit.py contains no occurrence of the NUCLEUS rejection percentage at all, in any form, which is asserted separately. The repository guard's two rules pass on the current tree and are demonstrated to fire; see test-no-orphan-veto-factor."
      linked_ids: [deliv-credit-module, deliv-credit-tests, test-credit-sentinel, test-no-orphan-veto-factor, ref-research-08-tax, ref-roadmap-sc2]
    claim-l2off-not-conservative:
      status: passed
      summary: "Section 6 of the taxonomy names the baseline 'NUCLEUS's shielding without NUCLEUS's vetoes' and states it is NOT a conservative subset of NUCLEUS but a different and WORSE configuration than either NUCLEUS or an independently optimized shield. The section 5.2.2 trade-off reasoning is QUOTED, not paraphrased: the optimal Pb amount 'results from a trade-off between (i) the production of secondary particles when exposed to cosmic ray-induced neutrons and muons ... and (ii) the total reduction of ambient gamma-ray backgrounds when combined with the COV'. This sentence is newly quoted by Plan 08-04 (it is not in the 08-01 evidence block); its grep command is recorded in taxonomy section 7 as Q-tradeoff and was re-run in the same pass. It is paired with row-b11's 'essential role of the COV' sentence and with evidence-block A.11's statement that the COV complements 'the relatively modest attenuation of the NUCLEUS passive shielding to external gamma rays'. Read together they establish that the passive gamma shield is deliberately thin BECAUSE the COV compensates for it, so nobody would design a 5 cm lead shield for an unvetoed detector. The word 'conservative' occurs in the document only inside the verbatim NUCLEUS quote of row-b03 ('a crude but conservative approximation', which describes a Geant4 approximation, not this configuration) and inside the prohibition sentence itself; an automated allow-list check enforces this. The one sense in which the baseline bounds anything is stated precisely: at FIXED shield it is an arithmetic lower bound on S/B, and it is not a bound on what an optimized independent design would achieve."
      linked_ids: [deliv-taxonomy, test-l2off-framing, ref-nucleus-2026-tax, ref-research-08-tax]
    claim-pitfalls-corrected:
      status: passed
      summary: "Three dated, sourced, in-place corrections to GPD/literature/PITFALLS.md, each marked 'PHASE-8 CORRECTION n', dated 2026-07-22, and citing 08-01-SOURCE-EVIDENCE.md. CORRECTION 1 replaces the bare COV factor-5 entry with the three disambiguated statements, each quoted verbatim with its section reference and given a label: [F5-a] the passive B4C attenuation (L1*), [F5-b] the COV anti-coincidence (L2), [F5-c] the Geant4 deposited-energy downscaling, marked NOT A REJECTION FACTOR, with the concrete failure mode recorded (an LLM summarizer asked for 'factor 5' returned [F5-c], which would have converted a Monte Carlo caveat into a claimed veto factor). Every one of the nine surviving factor-5 occurrences elsewhere in the file now carries an [F5-x] label; an automated check exempts only the correction block itself and fails on any bare occurrence. CORRECTION 2 supplies the published 2.25 cm^2 crystal footprint with its two independent mass closures referenced (CaWO4 array-crystal edge 4.996 mm at -0.09%, Al2O3 5.008 mm at +0.17%), labels ~9 cm^2 a PROJECT holder-scale estimate, states explicitly that it is not a NUCLEUS number and must not be attributed to NUCLEUS, and requires every area ratio to carry a basis label. The two unlabelled ~11x ratios in the file were replaced with basis-labelled forms (45.9x crystal / 11.5x holder), and an automated check fails on any line quoting 45.9 or 11.5 without the word basis. The diff touches only these three corrections and the [F5-x] annotations; no unrelated content was restructured."
      linked_ids: [deliv-pitfalls-correction, test-pitfalls-factor5, test-pitfalls-footprint, ref-pitfalls, ref-evidence-block-tax]
    claim-phase9-handoff:
      status: passed
      summary: "PHASE-8 CORRECTION 3 in GPD/literature/PITFALLS.md records the cross-phase finding inside Pitfall 6, where Phase 9's digitization work will read it, and Pitfall 6 item 4 now points at it. The Fig. 8 caption is quoted verbatim -- 'The left panels show the impact of sequentially adding passive shielding layers. The right panels show how using the different veto detectors complements the passive shields. The \"all vetoes\" selection criteria apply all possible anti-coincidence criteria for the rejection of background events.' -- newly quoted by this plan from the frozen data/external/nucleus/2509.03559v1.txt, with its command recorded in taxonomy section 7 as Q-fig8 and re-run there and again in a dedicated test. The caption's further statements (top panels neutrons, bottom panels muons, histograms are rates in the CaWO4 array between 0 and 1 keV) are recorded alongside. The instruction is explicit: Phase 9 must digitize a trace from the LEFT passive-only family if it wants a fluence, because reading a post-veto curve as pre-veto would import an L2 credit through the digitization -- the same forbidden proxy arriving by a route that no code review of the veto module would catch, since no veto factor would ever appear in the code. The consequence if a post-veto trace is used anyway is stated: the inverted object is a veto-survival-weighted phi_post that transfers only under a veto acceptance Phase 8 has determined the wafer does not have."
      linked_ids: [deliv-pitfalls-correction, deliv-taxonomy, test-phase9-handoff-recorded, ref-evidence-block-tax]
  deliverables:
    deliv-taxonomy:
      status: passed
      path: GPD/analysis/VETO-TAXONOMY.md
      summary: "Nine sections. (1) What the credit column means, with the closed credit-basis vocabulary and the statement that 1.0 is the EMPTY credit. (2) Tier definitions generated by the swap test, plus 2.1, the labelled extension of ROADMAP SC2 with SC2's own binary wording quoted. (3) The 19-row table with columns ID, verbatim statement, section, evidence-block id, tier, transfers-as, rejection credit, credit basis, swap test; plus 3.1, the one section-B entry that deliberately carries no row. (4) The multiplicity row's derivation with all three of Plan 08-02's checks and the counterpoint that its consequence is small. (5) Why the B4C liner and internal shielding stay in L1*, with the reviewer's counter-argument and the collapsing observation. (6) The baseline framing with the section 5.2.2 trade-off quote. (7) All 25 reproduction commands with their evidence-block ids and the two new-quote markers. (8) Where the credits live in code, including an explicit statement of what the guard does NOT catch. (9) Uncertainty markers. Required content confirmed present: tier definitions with the swap test, one row per catalogued statement with a verbatim quote and a section reference, a credit column and a credit-basis column distinguishing policy from derivation, the L1* justification, the not-conservative statement, and the note that the taxonomy stands independently of the fit verdict and is required by Phase 16."
      linked_ids: [claim-taxonomy-binding, claim-l1star-tier, claim-l2off-not-conservative, claim-phase9-handoff, test-taxonomy-complete, test-verbatim-classification, test-l1star-documented, test-l2off-framing]
    deliv-credit-module:
      status: passed
      path: src/qpd_potential/veto_credit.py
      summary: "Carries the project ASSERT_CONVENTION line. Module docstring states the purpose, that 1.0 means the background is unchanged, that changing a constant away from 1.0 requires a wafer-specific veto geometry and a documented argument and will appear as a reviewable diff, that a reduced or partial credit is not permitted either (explicit user decision 2026-07-22), the three tier definitions, that the three-tier split is an extension of ROADMAP SC2, that no NUCLEUS rejection percentage or factor appears as a value anywhere in the module, and that one row's credit is derived rather than defaulted. Contains L2_CREDIT = L1STAR_CREDIT = L1_REJECTION_CREDIT = 1.0 with attribute docstrings; the closed vocabularies TIERS and CREDIT_BASES; a frozen TaxonomyRow dataclass validating tier, basis and credit in __post_init__; a private _row() helper that does not accept a credit argument at all, so 1.0 cannot be varied row by row; TAXONOMY over 19 rows; lookup(), tier_of(), credit_for(), rows_in_tier(); and multiplicity_rejection_is_zero(), which imports wafer_self_veto and compares mult_rejection(1) to 0.0 under identity so the two modules cannot drift apart silently. The verbatim quotes are deliberately NOT stored here -- keeping them in the markdown is what keeps every NUCLEUS rejection number out of the package namespace and makes the guard decidable."
      linked_ids: [claim-credit-in-code, claim-l1star-tier, test-credit-sentinel, test-no-orphan-veto-factor]
    deliv-credit-tests:
      status: passed
      path: tests/test_veto_credit.py
      summary: "32 tests, all passing; full repository suite 310/310 with no regressions (baseline 278). Sentinel and docstring checks; taxonomy/code id round-trip in both directions; per-row schema checks (verbatim quote present, section reference, evidence id, tier in the closed vocabulary, credit exactly 1.0, basis in the closed vocabulary, swap-test justification longer than 30 characters, transfers-as non-empty); no-duplicate check; both plan-named credit bases present; the three factor-5 statements confirmed to be three separate rows in three roles; evidence-block section-B coverage; verbatim re-grep of eight sampled rows spanning all three tiers against the frozen source (returncode and stdout both checked, so a paraphrase is a hard failure) plus a re-run of every recorded command in the taxonomy; the two-rule guard on the whole package; three FIRE demonstrations (injected 0.998 literal, injected COV_REJECTION = 5.0, injected partial L2_CREDIT = 0.2) and two SILENCE demonstrations (a fixture replicating Plan 08-03's geometry constants, and the real veto_envelope.py and wafer_geometry.py); the L1* documentation check; the conservative-word allow-list check; and the three PITFALLS correction checks. The module docstring states what the guard does not catch."
      linked_ids: [claim-credit-in-code, test-credit-sentinel, test-no-orphan-veto-factor, test-pitfalls-factor5, test-pitfalls-footprint, test-phase9-handoff-recorded]
    deliv-pitfalls-correction:
      status: passed
      path: GPD/literature/PITFALLS.md
      summary: "Three blockquoted correction blocks, each headed 'PHASE-8 CORRECTION n', dated 2026-07-22, and carrying its source. Correction 1 sits immediately after the verified-anchor table where the bare factor-5 entry lived; correction 2 sits at the end of Pitfall 3's discussion where the ~9 cm^2 ratio was used; correction 3 sits inside Pitfall 6, where Phase 9's digitization guidance lives. The anchor table's own rows were annotated in place ([F5-b] on the COV entry, 'muon-INDUCED' made explicit on the >99.8% entry, the threshold-sensitivity row labelled as the sensitivity of [F5-b] rather than an independent factor). Nine further factor-5 occurrences across Pitfall 3, the shortcut table, the looks-correct checklist, the pitfall-to-phase table and the sources list were annotated with their [F5-x] labels. Correction 2 was placed after the numbered list rather than inside it so the existing list numbering is not broken. No unrelated content was restructured, no sections were reordered, and no other pitfall text was rewritten."
      linked_ids: [claim-pitfalls-corrected, claim-phase9-handoff, test-pitfalls-factor5, test-pitfalls-footprint, test-phase9-handoff-recorded]
  acceptance_tests:
    test-taxonomy-complete:
      status: passed
      summary: "PASS. Every B.n heading in 08-01-SOURCE-EVIDENCE.md section B (B.1-B.13) was extracted by regex and cross-checked against the taxonomy: twelve are taxonomy rows (B.1-B.12) and B.13 is explicitly recorded in taxonomy section 3.1 as carrying no row, with the reason (a payload-mass statement, not a rejection or attenuation statement). Seven further rows carry evidence ids from sections A and E as the plan's coverage list requires. Each of the 19 rows was parsed as a 9-cell table row and checked field by field: a verbatim quoted fragment of at least 15 characters is present, the section cell contains a section marker, the evidence cell is non-empty, the tier is one of L1 / L1* / L2, the credit is exactly the string 1.0, the credit basis is in the closed vocabulary, the swap-test cell exceeds 30 characters, and the transfers-as cell is non-empty. Row ids are unique, quote cells are unique, and the count matches veto_credit.TAXONOMY exactly."
      linked_ids: [claim-taxonomy-binding, deliv-taxonomy, ref-evidence-block-tax]
    test-verbatim-classification:
      status: passed
      summary: "PASS. Eight rows spanning all three tiers were sampled (row-e11-overburden and row-b10-pb-factor-50 for L1; row-b04-b4c-attenuation-factor5 and row-a09-internal-shielding-b4c for L1*; row-b05-cov-neutron-anticoincidence, row-b09-mv-cov-muon-induced, row-b03-geant4-quenching-downscale and row-b02-multiplicity-cut for L2), exceeding the required five, and the sample was asserted to cover the full tier set. Every quoted fragment in each sampled row's statement cell was passed to grep -o -F against the frozen data/external/nucleus/2509.03559v1.txt; both the exit code and the returned string were checked, so a paraphrase fails hard rather than passing on a substring. Separately, all 25 recorded commands in taxonomy section 7 were extracted from the document and re-run in the frozen directory: 25/25 exited 0 and returned their quoted string. The two commands added by this plan (Q-tradeoff, Q-fig8) are included in that count and the Fig. 8 caption has its own dedicated verbatim test, since its typographic double quotes make it the most fragile of the set."
      linked_ids: [claim-taxonomy-binding, deliv-taxonomy, ref-evidence-block-tax]
    test-l1star-documented:
      status: passed
      summary: "PASS. The taxonomy defines L1* as 'passive but payload-geometry-coupled', assigns credit 1.0, and assigns both row-a09-internal-shielding-b4c and row-b04-b4c-attenuation-factor5 to it (checked in the markdown and independently in veto_credit.rows_in_tier('L1*'), which returns exactly those two). The justification states that the ~5x suppression is quoted for a nearly-4pi liner in the direct vicinity of a centimetre-scale payload and is therefore coupled to the payload size under dispute. The document states that ROADMAP Success Criterion 2 specifies a binary split (quoting SC2's own wording), that this document extends it to three tiers, and that promoting these rows to L1 would flatter the background budget. The counter-argument a reviewer could make is present. All of these are checked by string assertions on the file rather than by inspection alone."
      linked_ids: [claim-l1star-tier, deliv-taxonomy, ref-research-08-tax, ref-roadmap-sc2]
    test-credit-sentinel:
      status: passed
      summary: "PASS. L2_CREDIT == 1.0, L1STAR_CREDIT == 1.0 and L1_REJECTION_CREDIT == 1.0 under exact comparison, with type float and repr '1.0' asserted for each. Attribute docstrings were extracted with ast (the assignment's following string-literal expression) and each was checked to contain 'Phase 8' and 'VALD-09' and a stated reason; L2_CREDIT and L1STAR_CREDIT were additionally checked to contain '1.0 means the background is unchanged'. The module docstring was checked for 'wafer-specific veto geometry', 'documented argument' and 'reviewable diff'. The 19 markdown row ids and the 19 TAXONOMY keys were compared as sets in both directions with no gaps and no extras, and for every id the code's credit, tier and credit basis were compared against the parsed markdown cells. credit_for() on an uncatalogued id raises KeyError naming the taxonomy file. The TaxonomyRow constructor raises ValueError when handed a credit of 0.2."
      linked_ids: [claim-credit-in-code, deliv-credit-module, deliv-credit-tests, deliv-taxonomy]
    test-no-orphan-veto-factor:
      status: passed
      summary: "PASS on both rules, and demonstrated rather than assumed. RULE 1 (literal denylist): every .py file under src/qpd_potential/ was tokenized and every NUMBER token compared against 99.8 and 0.998; zero violations across all 15 modules. Tokenizing is what makes the plan's 'outside a docstring or comment' phrasing decidable -- any occurrence of 99.8 in a Python file is either a NUMBER token or is inside a STRING or COMMENT token, so restricting to NUMBER tokens is exactly the intended rule; a fixture with 99.8 in a docstring and 0.998 in a comment is correctly passed. RULE 2 (naming convention): every module was imported and its namespace inspected; every module-level int/float whose name matches CREDIT, REJECTION or VETO_FACTOR case-insensitively was required to equal exactly 1.0; zero violations. FIRE DEMONSTRATIONS, all three producing exactly one violation naming the file and line: an injected SURVIVING_FRACTION = 0.998 (rule 1, orphan_literal.py:3); an injected COV_REJECTION = 5.0 (rule 2, orphan_named.py:4); and an injected partial L2_CREDIT = 0.2 (rule 2), which is what makes the ban on a reduced credit structural rather than only textual. SILENCE DEMONSTRATIONS: a fixture defining COV_CRYSTAL_THICKNESS_CM = 2.5, B4C_THICKNESS_CM = 4.0, COV_CRYSTAL_DIAMETER_CM = 10.0, LZ = 0.20, ARRAY_CRYSTAL_FOOTPRINT_CM2 = 2.25 and HOLDER_SCALE_FOOTPRINT_CM2 = 9.0 produces zero violations under both rules, and so do the real veto_envelope.py and wafer_geometry.py, whose values were separately asserted to be the ones the plan names. STATED LIMITATION: an anonymous inline literal such as 'rate / 5' inside a function body is invisible to both rules, because no decidable rule can separate it from a legitimate arithmetic constant; this is recorded in both the test module docstring and taxonomy section 8 so the guard is not mistaken for a completeness proof."
      linked_ids: [claim-credit-in-code, deliv-credit-tests, deliv-credit-module]
    test-l2off-framing:
      status: passed
      summary: "PASS. The taxonomy contains the exact phrase 'NUCLEUS's shielding without NUCLEUS's vetoes', the phrase 'different and worse configuration', and the section 5.2.2 trade-off sentence quoted verbatim including its leg (ii) 'when combined with the COV'. Every line containing the string 'conservativ' (case-insensitive) was checked against an allow-list of two contexts: 'crude but conservative', which occurs only inside the verbatim NUCLEUS quote of row-b03 and inside that row's recorded grep command and describes a Geant4 approximation rather than this configuration; and 'does not use that word to', the explicit prohibition sentence. Three lines matched, all allowed, zero offending. The document therefore nowhere describes the L2-off configuration as conservative."
      linked_ids: [claim-l2off-not-conservative, deliv-taxonomy, ref-nucleus-2026-tax]
    test-pitfalls-factor5:
      status: passed
      summary: "PASS. Every line of GPD/literature/PITFALLS.md matching the regex factor[ ~-]*5 was enumerated. The lines inside the PHASE-8 CORRECTION 1 block are exempted by computing the block's line range (from its heading to the end of its blockquote), because that block is where the three statements are quoted and disambiguated. Every remaining occurrence -- nine of them, in the anchor table, Pitfall 3 item 1, Pitfall 3's adopting sentence, the L1/L2 split guidance, the warning-signs list, the shortcut table, the looks-correct checklist, the pitfall-to-phase table and the sources list -- was required to contain an [F5- label; zero offending. The correction block itself was checked to be dated 2026-07-22, to cite 08-01-SOURCE-EVIDENCE.md, to contain all three labels, to quote all three statements verbatim, to carry exactly three '§5.2.1, evidence block' attributions, to mark [F5-c] NOT A REJECTION FACTOR, and to record the summarizer failure mode."
      linked_ids: [claim-pitfalls-corrected, deliv-pitfalls-correction, ref-evidence-block-tax]
    test-pitfalls-footprint:
      status: passed
      summary: "PASS. PHASE-8 CORRECTION 2 is present with the published 2.25 cm^2 crystal footprint, both mass-closure edges (4.996 mm and 5.008 mm) referencing Plan 08-01, the phrase 'holder-scale estimate', the explicit statement 'It is not a NUCLEUS number', and 'must not be attributed to NUCLEUS'. Every line quoting 45.9 or 11.5 was required to contain the word 'basis'; zero offending. The two previously unlabelled ~11x ratios (Pitfall 3 item 1 and the shortcut table's 11x-larger payload) were replaced with basis-labelled forms. The only surviving bare 11x in the file is in the Pitfall 1 heading, where it refers to the RoI-width conversion error and not to an area ratio, and it was deliberately left untouched as out of scope."
      linked_ids: [claim-pitfalls-corrected, deliv-pitfalls-correction, ref-evidence-block-tax]
    test-phase9-handoff-recorded:
      status: passed
      summary: "PASS. PHASE-8 CORRECTION 3 is present inside Pitfall 6 (the digitization pitfall Phase 9 owns), and Pitfall 6 item 4 now points at it. The caption evidence is present and checked string by string: 'left panels show the impact of sequentially adding passive shielding layers', 'right panels show how using the different veto detectors complements', 'all vetoes', and 'apply all possible anti-coincidence criteria'. The instruction is present ('passive-only', 'Phase 9'), as is the consequence ('would import an **L2**' credit through the digitization) and the named forbidden proxy (fp-veto-credit-transfer). A separate test re-greps the full caption sentence against the frozen source and requires exit 0, which is what licenses quoting it at all since it is newly quoted by this plan rather than carried from the 08-01 evidence block."
      linked_ids: [claim-phase9-handoff, deliv-pitfalls-correction, ref-evidence-block-tax]
  references:
    ref-evidence-block-tax:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Read in full. Every one of the 19 taxonomy rows carries an evidence-block section id (A.8, A.9, A.12, B.1-B.12, E.1.1-E.1.3) and its quote is reproduced from the block's own recorded command. Section B's headings were extracted programmatically and cross-checked against the rows so that coverage is machine-verified rather than asserted. The block's three-way separation of the factor-5 statements (B.3/B.4/B.5) is what makes correction 1 in PITFALLS.md possible, and its C.2/C.3 mass closures are what make correction 2's 2.25 cm^2 defensible. Cited by name in the taxonomy header, in every row, in veto_credit.py's TaxonomyRow docstring, and in all three PITFALLS corrections."
    ref-nucleus-2026-tax:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "Read directly from the frozen data/external/nucleus/2509.03559v1.txt, not from a summarizer. Compared: all 25 recorded grep commands were re-run against the frozen file and 25/25 reproduced their quoted string exactly, including the two sentences newly quoted by this plan. Sections 2, 4.1, 5.1, 5.2.1, 5.2.2 and Table 4 are all represented in the taxonomy. The section 5.2.2 trade-off sentence -- the one that makes the L2-off configuration worse rather than a subset -- was located by searching the frozen file for 'trade-off' rather than assumed from the research document's paraphrase, and the paraphrase turned out to be accurate. Cited throughout the taxonomy and in the PITFALLS corrections."
    ref-pitfalls:
      status: completed
      completed_actions: [read, compare]
      missing_actions: []
      summary: "Read in full before editing. Compared against the evidence block: the bare 'COV factor ~5' anchor row was found not to say which of the three section-5.2.1 statements it meant, and the '~9 cm^2 [COMPUTED]' footprint was found to be a project estimate rather than a published NUCLEUS number, with the derived ~11x ratio propagating from it unlabelled. Both were corrected in place with dated, sourced blocks, and every downstream occurrence was annotated. The Fig. 8 handoff was added to Pitfall 6 where the file already warns about digitizing the wrong trace, so the new evidence lands next to the existing warning rather than in a new section."
    ref-roadmap-sc2:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "ROADMAP Phase 8 Success Criterion 2 and REQUIREMENTS VALD-09 were both read. SC2's binary L1/L2 wording is quoted verbatim in taxonomy section 2.1 before the three-tier extension is introduced, so the extension is visibly an extension and not a restatement. VALD-09's default-to-zero rule and its statement that L2 may not appear in any downstream code path without wafer geometry behind it are cited in all three credit-constant docstrings and are what the repository guard implements."
    ref-research-08-tax:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "08-RESEARCH.md's SC2 classification table was used as the starting proposal and its Pitfalls 1, 4, 5, 6 and 10 were carried into the deliverables. The proposed table was extended rather than copied: it listed 13 rows, this taxonomy has 19, adding the veto thresholds, the Geant4 downscaling as its own row, the IV-plus-one-hit marginality assessment, the IV's gamma insensitivity, and a separate row for the measured VNS gamma ambience. Its binding implementation constraint -- that the credit live in code and not only in a markdown table -- is discharged by src/qpd_potential/veto_credit.py."
  forbidden_proxies:
    fp-veto-credit-transfer:
      status: rejected
      notes: "No credit other than 1.0 exists anywhere. The dataclass constructor raises on any other value, credit_for() can only return 1.0, and the repository guard is demonstrated to fire on an injected partial credit of 0.2 as well as on a full factor of 5.0. veto_credit.py contains no NUCLEUS rejection number in any form. The stated residual exposure is an anonymous inline literal inside a function body, which no decidable rule can catch; that limitation is recorded rather than hidden."
    fp-l1star-promotion:
      status: rejected
      notes: "The B4C liner and the internal shielding are in L1*, not L1, with the geometry-coupling argument stated and the reviewer's counter-argument recorded alongside. rows_in_tier('L1*') is asserted to return exactly those two ids, so a silent promotion would fail a test rather than pass unnoticed."
    fp-markdown-only-credit:
      status: rejected
      notes: "The credits are named module-level constants in src/qpd_potential/veto_credit.py with attribute docstrings, and the markdown and the code are cross-checked in both directions by a test, so neither can drift from the other."
    fp-l2off-as-conservative:
      status: rejected
      notes: "The baseline is named 'NUCLEUS's shielding without NUCLEUS's vetoes' and stated to be a different and worse configuration than either alternative, with the section 5.2.2 trade-off sentence quoted. An allow-list check on the word 'conservative' enforces that it never describes this configuration."
    fp-paraphrased-classification:
      status: rejected
      notes: "Every row's classification rests on a quoted sentence, and every quote is re-greped against the frozen source. Eight rows spanning all three tiers were sampled with both exit code and returned text checked, and all 25 recorded commands were re-run: 25/25 reproduced. The two sentences newly quoted by this plan were located in the frozen file directly rather than carried from a research-document paraphrase."
  uncertainty_markers:
    weakest_anchors:
      - "The L1 / L1* boundary is a judgement about geometry coupling, not a statement any source makes; row-b04-b4c-attenuation-factor5 is the contested row and is argued in taxonomy section 5 rather than assumed"
      - "The L1 rows for the overburden, the attenuation factor and the Table 4 uncertainties inherit Plan 08-01's verdicts; all are VERIFIED VERBATIM, but the Table 4 numeric body is verified against arXiv v1 only because the published EPJC HTML serves it behind a 'Full size table' link"
      - "All classified quotes are from arXiv v1; the published EPJC 86, 29 (2026) text is the version of record, and only four load-bearing statements plus the overburden, the attenuation factor and the B4C factor were cross-checked against it"
      - "The section 5.2.2 trade-off sentence and the Fig. 8 caption are newly quoted by this plan and were not part of Plan 08-01's re-verification pass; they were verified by this plan's own recorded commands and by a dedicated test, but they carry one fewer independent check than the 23 carried quotes"
    unvalidated_assumptions:
      - "That the bulk passive attenuation factors of row-a08 and row-b10 transfer as material attenuation independent of the target; they are published as event-rate reductions in CaWO4 detectors, which embeds a target response, and both rows are labelled 'material attenuation only' for that reason"
      - "That the tier assignment is stable under a different payload; the swap test is applied by reasoning, not by recomputation"
      - "That a two-rule guard is sufficient structural defence; an anonymous inline literal in a function body defeats both rules and no decidable rule can catch it"
    competing_explanations:
      - "A reviewer could argue that 4 cm of B4C attenuates neutrons regardless of what sits behind it, so row-b04 is close enough to pure material attenuation to be L1, which would raise the transferable credit; the response is that the published value is geometry-coupled, that no wafer-specific recomputation exists, and that L1* records the disagreement rather than deciding it"
      - "A reviewer could argue that Phase 8 overstates the loss from the multiplicity cut, since NUCLEUS themselves call the IV-plus-one-hit benefit 'very marginal'; that counterpoint is recorded in row-b07 and in taxonomy section 4 rather than suppressed, and it cuts against this project's own framing"
    disconfirming_observations:
      - "A source statement showing the B4C ~5x suppression quoted for a payload-independent configuration would collapse L1* into L1 and raise the transferable credit"
      - "The published EPJC version stating a different rejection factor or a different section structure than arXiv v1 would invalidate a classified quote; four load-bearing statements were checked and agree word for word, but the check was not exhaustive"
      - "A statement in the evidence block resisting classification under all three tiers would mean the tier definitions are wrong; none was found, and the one section-B entry carrying no row is a category question (a payload mass is not a rejection statement) rather than a classification failure"
      - "A future contributor reintroducing a veto factor as an anonymous inline literal would pass both guard rules; that is the guard's known blind spot and is stated in the test module docstring and in taxonomy section 8"
comparison_verdicts:
  - subject_id: claim-taxonomy-binding
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-nucleus-2026-tax
    comparison_kind: prior_work
    metric: verbatim_quote_reproduction
    threshold: "25/25 recorded commands exit 0 and return their quoted string"
    verdict: pass
    recommended_action: "Re-run taxonomy section 7's command block whenever the frozen sources are refreshed, and re-check the four load-bearing statements against the published EPJC text if a v2 appears."
    notes: "All 25 commands re-run against data/external/nucleus/2509.03559v1.txt in a single pass; 25/25 reproduced exactly. Eight sampled rows spanning all three tiers were additionally checked with both exit code and returned text."
  - subject_id: claim-pitfalls-corrected
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-pitfalls
    comparison_kind: prior_work
    metric: error_count_found_and_corrected
    threshold: "both identified errors corrected in place, no unrelated edits"
    verdict: pass
    recommended_action: "Correct the same unlabelled ~9 cm^2 footprint in GPD/ROADMAP.md and GPD/REQUIREMENTS.md VALD-09; Plan 08-05 owns flagging it and no Phase-8 plan edits those files."
    notes: "The pre-edit file's bare COV factor-5 entry and its ~9 cm^2 [COMPUTED] footprint were compared against 08-01-SOURCE-EVIDENCE.md sections B.3/B.4/B.5 and C.2/C.3/C.6. Both errors confirmed and corrected with dated, sourced blocks; nine downstream factor-5 occurrences and two unlabelled area ratios annotated. The diff contains only the three corrections and their annotations."
---

# Plan 08-04 Summary — The Binding L1 / L1\* / L2 Taxonomy and the Credit Sentinels

## What was established

**The taxonomy is written, binding, and built entirely from quoted sentences.**
`GPD/analysis/VETO-TAXONOMY.md` classifies 19 NUCLEUS statements: 6 L1, 2 L1\*, 11 L2. Every row
carries the verbatim sentence, its section, its `08-01-SOURCE-EVIDENCE.md` id, its tier, what does
transfer, a rejection credit of exactly 1.0, a credit basis, and a one-line swap-test
justification. Every quote reproduces from the frozen sources by a recorded command; all 25
commands were re-run and 25/25 returned their quoted string.

**The credit column means one thing, and the document says so before the table.** A credit of 1.0
means the background is **unchanged** — 1.0 is the empty credit, not full credit. That every row
carries 1.0 is the result, not a formatting accident; what differs between tiers is *what does
transfer*, which is a separate column.

**L1\* is an extension, and is labelled as one.** ROADMAP SC2's binary wording is quoted before
the three-tier split is introduced. The B₄C liner and the internal shielding are passive, which
reads L1; their published suppression is quoted for a nearly-4π liner beside a centimetre-scale
payload, which reads L2. Promoting them to L1 would flatter the budget at exactly the point where
the wafer's size is the disputed quantity. The counter-argument a reviewer would make is recorded,
along with the observation that would collapse L1\* into L1.

**The three factor-5 statements are three rows in three roles**, never merged: passive B₄C
attenuation (L1\*), COV anti-coincidence (L2, the genuine rejection), and the Geant4
deposited-energy downscaling (credit basis `not-a-rejection-factor`). The third is the one an LLM
summarizer returned when asked for "factor 5" during this project's research.

**One row's 1.0 is derived, not defaulted.** `row-b02-multiplicity-cut` cites Plan 08-02's
`eps_mult(1) == 0.0` early-return counting identity, its model-independence, and its backing
module. `veto_credit.multiplicity_rejection_is_zero()` calls `wafer_self_veto.mult_rejection(1)`
rather than restating the zero, so the two cannot drift apart silently.

**The credits are in code, and the guard has been demonstrated to fire.** Rule 1 tokenizes every
module and rejects `99.8`/`0.998` as NUMBER tokens; Rule 2 imports every module and requires every
module-level numeric constant matching `*CREDIT*`/`*REJECTION*`/`*VETO_FACTOR*` to equal exactly
1.0. The guard fires on an injected `0.998` literal, on `COV_REJECTION = 5.0`, and on a *partial*
`L2_CREDIT = 0.2`, naming file and line each time; it stays silent on Plan 08-03's
`COV_CRYSTAL_THICKNESS_CM = 2.5`, `B4C_THICKNESS_CM = 4.0` and the wafer's `LZ = 0.20`, both in a
fixture and in the real modules.

**The baseline is named honestly.** "NUCLEUS's shielding without NUCLEUS's vetoes" is a different
and **worse** configuration than either NUCLEUS or an independently optimised shield, and the
word "conservative" never describes it. The §5.2.2 trade-off sentence whose leg (ii) is "when
combined with the COV" is quoted, not paraphrased.

## Deviations and judgement calls

| # | What | Rule | Why |
|---|---|---|---|
| 1 | Two sentences were **newly quoted** from the frozen source rather than carried from the 08-01 evidence block: the §5.2.2 trade-off sentence and the Fig. 8 caption. | 4 (missing component) | Both are required by the plan's own text and neither is in the evidence block. Fabricating them was not an option; locating them in the frozen file and recording their commands was. Both are marked as new quotes in taxonomy §7, and both are re-greped by tests. |
| 2 | The credit-basis vocabulary was **extended** beyond the acceptance test's `policy` / `derivation` to include `not-a-rejection-factor` and `context`. | 4 (missing component) | Four L1 environmental rows and the Geant4 downscaling row are not rejection factors at all, and two rows qualify another row's factor rather than being independent. Forcing them into `policy` would have implied a rejection was declined where none exists. Both plan-named bases are present and distinguished; the extension is documented at the head of the table. |
| 3 | The taxonomy has **19 rows** where 08-RESEARCH proposed 13. | 4 (missing component) | The plan's Task-1 coverage list plus complete coverage of evidence-block §B required rows for the veto thresholds, the Geant4 downscaling, the IV-plus-one-hit marginality, the IV's gamma insensitivity, the internal shielding as a structure statement, and the VNS gamma ambience separately from the Table 4 fluxes. |
| 4 | `PITFALLS.md` correction 2 was placed **after** Pitfall 3's numbered list rather than inside it. | routine | A blockquote inserted between list items breaks the list numbering in every markdown renderer. The correction is still adjacent to the text it corrects, and item 1 points at it. |
| 5 | The evidence block's §B.13 (payload masses) carries **no taxonomy row**. | routine | It is not a rejection or attenuation statement; it is the object the swap test replaces. Its exclusion is recorded explicitly in taxonomy §3.1 so that its absence cannot be read as an omission, and a test enforces that any uncovered §B entry must be explicitly recorded. |

No deviation-rule-5 or -6 condition arose. No checkpoint was required.

## What this does not establish

- The guard does not prove no rejection factor can enter. An anonymous inline literal —
  `rate / 5` inside a function body — defeats both rules, and no decidable rule can separate it
  from a legitimate arithmetic constant. Stated in the test module docstring and taxonomy §8.
- The swap test is applied by reasoning, not by recomputation. The tier assignments are arguments,
  not measurements.
- The L1/L1\* boundary is this project's judgement, not a distinction any source makes. `row-b04`
  is the contested row.
- The unlabelled "~9 cm²" also appears in `GPD/ROADMAP.md` and `GPD/REQUIREMENTS.md` VALD-09.
  No Phase-8 plan edits those files; Plan 08-05 owns flagging it.

## Verification

| Check | Result |
|---|---|
| New tests | **32 passed** (`tests/test_veto_credit.py`) |
| Full repository suite | **310 passed**, 0 failed (baseline before this plan: 278) |
| Recorded grep commands re-run | **25 / 25** exit 0 and return their quoted string |
| Taxonomy ↔ code row ids | set equality, both directions, 19 = 19 |
| Guard rule 1 / rule 2 on `src/qpd_potential/` | 0 violations across 15 modules |
| Guard fire demonstrations | 3 / 3 (literal, named constant, partial credit) |
| Guard silence demonstrations | 2 / 2 (fixture, and real `veto_envelope.py` + `wafer_geometry.py`) |
| Bare factor-5 occurrences surviving in `PITFALLS.md` | **0** |
| Area ratios without a basis label in `PITFALLS.md` | **0** |
| "conservative" describing the L2-off configuration | **0** occurrences |

---

_Phase 8 (Veto-Envelope Geometry Gate, P-VETO), Plan 08-04. Discharges ROADMAP Phase 8 Success
Criterion 2 and the taxonomy half of VALD-09. Consumed by Phase 16 (`CALC-22`) and, through the
`PITFALLS.md` handoff, by Phase 9 (`CALC-11`/`CALC-12`)._
