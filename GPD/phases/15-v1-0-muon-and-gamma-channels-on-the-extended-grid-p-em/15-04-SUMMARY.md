---
phase: 15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em
plan: 04
title: "Phase-15 closure: zero applied relocation quantities over a 31-file import closure with all 11 enumerated by name and value as REMOVED, both accuracy bands carried forward unnarrowed with the muon sign never travelling without its anchor leg, and the v1.0 in-band dominance conclusion CONFIRMED on the ordering but REFINED on the muon's in-band presence"
date: 2026-07-23
status: complete
depth: full
completed: 2026-07-23
provides:
  - "artifacts/v2.0/em_rescope_audit.csv -- 17 rows: 11 retired relocation quantities named by value with disposition and reason, the veto-credit sentinel, and the five normalization factors each individually unity"
  - "artifacts/v2.0/em_accuracy_labels.csv -- the machine-readable per-channel accuracy object Phase 16 propagates, reusing the 09-01 Section 5 directional-bias schema"
  - "artifacts/v2.0/em_inband_dominance.csv -- 322 rows, the re-checked muon/Compton ordering with the Phase-12 CEvNS curve alongside for orientation only, both accuracy labels on every row"
  - "tests/test_em_rescope_audit.py -- 15 tests covering all 12 contract acceptance tests"
  - "GPD/phases/15-.../15-04-RESCOPE-AUDIT.md -- the audit, the carry-forward, the dominance re-check and the phase closure statement"
  - "artifacts/v2.0/legacy_grid_disposition.csv -- disposition rows for the three new tracked artifacts (62 register rows)"
one_liner: "ROADMAP Phase 15 SC4 and SC5 are both discharged and Phase 15 closes with all five success criteria MET as written. THE AUDIT: the Phase-9 token list is IMPORTED via surface_environment.shielded_token_guard rather than re-typed -- and that mattered, because an ad-hoc substring scan written earlier in this phase false-positived the germanium lattice constant 5.658 A on the 5.65 Bq/kg 238U ambience while the imported guard's digit-boundary matching did not -- and scanning the full 18-file import closure plus 10 emitted artifacts and 6 emitted documents returns 35 token hits of which 34 are the explicit NOT-APPLIED enumeration SC4 demands, 1 is the single Phase-9 allowlist entry (the NIST XCOM photon mass-attenuation coefficient of the germanium TARGET, which multiplies no normalization), and 0 are applied quantities; the *-PLAN.md files and 15-CONTEXT.md are deliberately OUT of scope and the exclusion is stated rather than silent, because they quote every retired quantity BECAUSE THEY COMMAND THIS AUDIT; all 11 retired quantities are enumerated by name AND retired value -- 2.92 m.w.e., 1.41, 5.03 cm^-2 s^-1, 40K 59.6 / 232Th 3.28 / 238U 5.65 Bq/kg, factor ~50, buildup, MV+COV 99.8%, COV ~5 at 1 keV_ee, Table 5 < 14 mcpd -- each with a disposition 'removed by the 2026-07-22 re-scope' and a reason it no longer applies; the veto credit sentinel is exactly 1.0 recorded as BY CONSTRUCTION rather than as a policy default; every one of the five multiplicative normalization factors is asserted exactly 1.0 INDIVIDUALLY because a product can be unity by cancellation, with the end-to-end numeric evidence independent of the enumeration (muon 1.365914 Hz against the frozen 1.3659, Compton 2.6747e-01 against 2.6747e-01); the forbidden configuration adjective appears ZERO times, one earlier occurrence in 15-01 having described a physical CHOICE rather than the configuration and having been reworded because a text check that must reason about attachment is a weak check; and the audit states plainly which of the two competing readings it establishes -- that no relocation quantity survived under a RECOGNISED name or value, NOT that none survived at all, since neither a token scan nor an attribute-walk import closure can see a quantity re-entering under a new name or a dynamically imported module. THE CARRY-FORWARD: the muon band x0.65..x1.35 is the 30-35% Gaisser-Guan spread and ENCLOSES the PDG Leg A / Leg B bracket x0.8309..x1.2595 so it narrows nothing, the gamma band is the v1.0 x0.5..x2 exactly, and every occurrence of -20.61% in every emitted artifact and document is verified within a four-line window to carry both Leg A and Leg B. THE DOMINANCE RE-CHECK, recomputed from the Plan 15-03 artifacts rather than quoted: the Compton continuum exceeds the muon channel in the 10-100 eV RoI by 4.587x (Ta->Al) and 4.643x (Al->Hf), CONFIRMING the v1.0 ordering, with the CEvNS orientation curve cross-checked by its own total 118.7286 / 118.7292 against Phase 12's 118.730 -- but the v1.0 phrasing that muons land ABOVE the CEvNS band is REFINED as too strong, because the muon channel carries 7.4656 / 7.7231 counts/kg/day in the RoI, about 10% of the CEvNS rate there, so it is subdominant WITHIN the band rather than absent from it; and nothing in the table bounds the total background, since the Phase-13 neutron channel alone is 5430.29 / 5485.15 counts/kg/day in the same band, 159x and 153x the Compton channel, on an order_of_magnitude label."
plan_contract_ref: GPD/phases/15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em/15-04-PLAN.md#/contract

contract_results:
  claims:
    claim-rescope-audit:
      status: passed
      summary: "SCOPE: the full IMPORT CLOSURE of every module this phase touches -- 18 files computed by walking module attributes as Plan 09-01 did (compton_deposit, compton_source, em_extended, em_recoil, energy_scale, fold, ia_broadening, interp_guard, legacy_grid, muon_deposit, muon_flux, params, phonon_scale, response, response_matrix, surface_environment, trigger, wafer_geometry) -- plus 10 emitted artifact files and 6 emitted phase documents, 31 files in total at audit time. NOT SCANNED, and the exclusion is STATED rather than silent: the *-PLAN.md files and 15-CONTEXT.md, which are inputs authored upstream and which quote every retired quantity by name and value BECAUSE THEY COMMAND THIS AUDIT; scanning them would flag the instruction as the violation. RESULT: 35 token hits, 34 explicit NOT-APPLIED / enumeration declarations, 1 allowlist entry, ZERO applied quantities. THE TOKEN LIST IS IMPORTED, NOT RE-TYPED, via surface_environment.shielded_token_guard(), and a test asserts identity (ST is ev.SHIELDED_TOKENS) rather than equality so a copy would fail. THAT MATTERED IN PRACTICE: an ad-hoc substring scan written earlier in this phase false-positived the germanium lattice constant 5.658 angstrom on the 5.65 Bq/kg 238U ambience; the imported guard's digit-boundary regex did not, and the test now asserts that regex rejects 1.4150 and 1.4585 while accepting 1.41. ALLOWLIST: exactly one entry, src/qpd_potential/compton_source.py's 'Linear attenuation coefficient mu = (mu/rho) * rho' -- the NIST XCOM photon mass-attenuation coefficient of the germanium TARGET WAFER, a property of the target rather than of any shield, which multiplies no normalization. Same single entry Plan 09-01 exempted, by name, with its written justification asserted to exceed 80 characters so a future reader can audit it rather than trust it. A local extension to the Phase-9 NOT_APPLIED_MARKERS was required and is documented rather than hidden, because SC4 REQUIRES the enumeration and the enumeration necessarily contains the tokens; prose is scanned in a +/-3-line window and CODE line by line, justified on the ground that an applied factor in a .py file is a single assignment or multiplication and cannot hide behind a neighbouring line. ENUMERATION: em_rescope_audit.csv carries one row per retired quantity with its retired NUMERIC VALUE, the token searched, the scope size, the applied-hit count, the disposition 'removed by the 2026-07-22 re-scope' and the reason it no longer applies -- 2.92 m.w.e. overburden, the 1.41 omnidirectional attenuation, the NUCLEUS Table 2 ambience 5.03 cm^-2 s^-1 with 40K 59.6, 232Th 3.28 and 238U 5.65 Bq/kg, the 'factor ~50' passive reduction, buildup factors, MV+COV > 99.8%, the COV factor ~5 at 1 keV_ee, and the Table 5 muon residual < 14 mcpd. VETO CREDIT SENTINEL: surface_environment.veto_credit() returns exactly 1.0, recorded as BY CONSTRUCTION rather than as a policy default, with the distinction spelled out -- a 1.0 arrived at as a default is something a later phase could quietly relax, a 1.0 that follows from the ABSENCE OF THE APPARATUS cannot be relaxed without first changing the configuration. NUMERIC COMPLEMENT: each of the five multiplicative normalization factors is asserted exactly 1.0 INDIVIDUALLY, never as a product, because a product can be unity by cancellation between two wrong factors; and the end-to-end evidence is independent of the enumeration, the through-wafer muon rate reproducing 1.365914 Hz against the frozen 1.3659 and the Compton bound-incoherent rate 2.6747e-01 Hz against 2.6747e-01, which no surviving factor other than 1.0 could produce. FORBIDDEN CONFIGURATION ADJECTIVE: zero occurrences over the scanned scope. One occurrence existed in an earlier draft of 15-01, describing a PHYSICAL CHOICE (the band-gap reading) rather than the configuration; it was reworded because a text check that has to reason about attachment is a weak check. WHICH READING THIS ESTABLISHES, stated plainly in both the CSV header and the report: a clean token scan establishes that no relocation quantity survived UNDER A RECOGNISED NAME OR VALUE; it does NOT establish that none survived under a new name with a new value, and an attribute-walk closure cannot see a dynamically imported module either. Together with the numeric enumeration this is a STRONG CHECK, NOT A PROOF, and the audit says so."
      linked_ids: [deliv-audit-table, deliv-audit-report, deliv-audit-tests, test-token-scan-clean, test-retired-quantities-named, test-factors-are-unity, test-veto-credit-sentinel, test-no-conservative-word, ref-roadmap-sc4, ref-token-guard, ref-veto-credit]
      evidence:
        - verifier: gpd-executor
          method: "the Phase-9 guard imported by identity rather than re-typed, applied over a computed import closure, with each retired quantity enumerated by value and each normalization factor asserted individually rather than as a product"
          confidence: high
          claim_id: claim-rescope-audit
          deliverable_id: deliv-audit-table
          acceptance_test_id: test-token-scan-clean
          reference_id: ref-token-guard
          forbidden_proxy_id: fp-absence-without-enumeration
          evidence_path: artifacts/v2.0/em_rescope_audit.csv
    claim-accuracy-carried:
      status: passed
      summary: "em_accuracy_labels.csv reuses the Plan 09-01 Section 5 directional-bias schema and carries, per channel, the accuracy label, the bias direction from the closed vocabulary, the SIGNED deviation with its anchor leg NAMED, the bracketing disclosure, the band multipliers, the underlying limit and the artifact paths the label appears in -- complete enough that Phase 16 need not re-derive any of it. MUON: pdg_within_20pct_vald02_tol_30pct, flatters_SB, -20.61% against PDG Leg A (~1 muon cm^-2 min^-1 x A_top = 1.7204 Hz), with the disclosure that PDG Leg B (I_v ~ 70 m^-2 s^-1 sr^-1, cos^2 theta -> 1.1350 Hz) gives +20.34% i.e. penalizes_SB, so the two legs BRACKET the adopted 1.3659 Hz from opposite sides and the ~20% MAGNITUDE is solid while the SIGN is not; band x0.65..x1.35; underlying limit the 30-35% inter-experiment Gaisser-Guan spread which no in-repo artifact can narrow, plus the standing fact that this channel has NO external benchmark on the reconstructed axis at all since the NUCLEUS Table 5 comparison was removed by the re-scope. GAMMA: site_band_factor_2, neutral, +0.00% against the LABChico measured survey which IS the adopted normalization, band x0.5..x2 with the note that the LOW edge is the flattering one and is not used, and the weakest component named as the U-238 chain whose per-line flux rests on the documented assumption Phi_U = Phi_Th rather than a measured line intensity. NOTHING NARROWED: the gamma band is exactly the v1.0 factor-2 band, and the muon band is asserted to ENCLOSE the PDG leg bracket x0.8309..x1.2595 and to be at least the 30% spread, so choosing it cannot be a narrowing; the emitted 15-03 spectra are checked bin by bin to use that same band and not a tighter one. THE SIGN NEVER TRAVELS ALONE: every occurrence of -20.61% in every emitted artifact and document is verified within a four-line window to carry BOTH the Leg A citation and the Leg B bracketing, so a bare -20.61% or a bare flatters_SB would fail. LABELS REACH THE ARTIFACTS: all 744 rows of each Plan 15-02 deposit table and all 161 rows of each Plan 15-03 reconstructed table carry a per-row accuracy label matching this file, and every one of the three tables checked exposes an accuracy_label column so no rate can be read out without it."
      linked_ids: [deliv-accuracy-table, deliv-audit-report, deliv-audit-tests, test-bands-not-narrowed, test-sign-carries-anchor-leg, test-labels-reach-artifacts, test-dimensions, ref-mu-gamma-declaration, ref-roadmap-sc4]
    claim-inband-dominance:
      status: passed
      summary: "RECOMPUTED FROM THE PLAN 15-03 ARTIFACTS, NOT QUOTED, and the test re-runs the fold and asserts the table reproduces it to rtol 1e-5. em_inband_dominance.csv, 322 rows (161 reconstructed bins x 2 designs), every row carrying BOTH contributing channels' accuracy labels. INTEGRATED OVER E_rec 10-100 eV: muon 7.4656 (Ta->Al) / 7.7231 (Al->Hf), Compton 34.2484 / 35.8616, CEvNS 72.9214 / 73.1441 for orientation only. Below 10 eV: muon 0.6681 / 0.6787, Compton 0.9448 / 0.9851, CEvNS 29.2236 / 29.7991. The CEvNS orientation curve is cross-checked by its own total over the whole reconstructed axis, 118.7286 / 118.7292 against Phase 12's 118.730, so it is demonstrably the right curve and was not mis-read. VERDICT, PART ONE -- CONFIRMED: the Compton continuum overlaps the CEvNS region and is the larger of the two electron-recoil channels there by 4.587x and 4.643x. The v1.0 ordering is unchanged. VERDICT, PART TWO -- REFINED, AND STATED AS A DEPARTURE: the v1.0 phrasing that muon deposits land ABOVE the CEvNS band is too strong on the extended reconstructed axis. The muon channel carries 7.47 / 7.72 counts/kg/day in the RoI, about 10% of the CEvNS rate there, and 0.67 / 0.68 below 10 eV. It is not absent from the band, it is SUBDOMINANT WITHIN it. What survives of the v1.0 statement is that the channel's BULK is far above the band (its reconstructed peak is at 18.8 / 15.0 keV) and that it is the smaller of the two electron-recoil backgrounds in-band; what does not survive is the implication that it can be neglected there. ORDERING CROSSOVERS at E_rec = 0.5309, 0.7499, 1.059, 1.189, 2.661 eV and again at 1.884e+04 eV (Ta->Al) / 1.334e+04 eV (Al->Hf); the sub-eV crossings sit where both Plan 15-01 floors exclude the muon channel and Plan 15-02 recorded no adequate support for it, so they are explicitly flagged as NOT to be read as physics, while the high-energy crossing is the real saturation feature. WHAT THIS DOES NOT BOUND, stated in the CSV header and the report: nothing here bounds the total background. Only two of the milestone's channels appear, and the Phase-13 neutron channel alone is 5430.29 / 5485.15 counts/kg/day in the same 10-100 eV band -- 158.6x and 153.0x the Compton channel -- on an order_of_magnitude label, with the neutron-capture channel not in scope either. NO QUANTITY HERE IS NAMED AS A SIGNAL-TO-BACKGROUND RATIO and a text scan over all emitted artifacts and documents finds zero occurrences of that name."
      linked_ids: [deliv-dominance-table, deliv-audit-report, test-dominance-recomputed, test-not-named-sb, test-labels-on-every-ratio, ref-rec-spectra, ref-cevns-ext, ref-mu-gamma-declaration]
      evidence:
        - verifier: gpd-executor
          method: "the fold re-run inside the test and compared against the frozen table, plus an independent cross-check of the orientation curve against the Phase-12 integrated total"
          confidence: high
          claim_id: claim-inband-dominance
          deliverable_id: deliv-dominance-table
          acceptance_test_id: test-dominance-recomputed
          reference_id: ref-cevns-ext
          forbidden_proxy_id: fp-sb-by-another-name
          evidence_path: artifacts/v2.0/em_inband_dominance.csv
  deliverables:
    deliv-audit-table:
      status: produced
      path: artifacts/v2.0/em_rescope_audit.csv
      summary: "17 rows: 11 retired relocation quantities each with its retired numeric value, the token searched, the 31-file scope, a zero applied-hit count, the disposition 'removed by the 2026-07-22 re-scope' and a reason it no longer applies; the veto-credit sentinel recorded as exactly 1.0 BY CONSTRUCTION; and the five normalization factors each recorded as exactly 1.0 asserted INDIVIDUALLY. The header records the imported token list and why it is imported, the scope and the stated exclusion of the input documents, the single justified allowlist entry, the local marker extension with its justification, and which of the two competing readings a clean scan establishes."
      linked_ids: [claim-rescope-audit]
    deliv-accuracy-table:
      status: produced
      path: artifacts/v2.0/em_accuracy_labels.csv
      summary: "Two rows reusing the 09-01 Section 5 schema, with the accuracy label, bias direction, signed deviation, anchor leg, bracketing disclosure, band multipliers, underlying limit, artifact paths and v1.0 source per channel. The machine-readable object Phase 16 propagates."
      linked_ids: [claim-accuracy-carried]
    deliv-dominance-table:
      status: produced
      path: artifacts/v2.0/em_inband_dominance.csv
      summary: "322 rows: per reconstructed bin per design, the muon and Compton rates, their ratio, the Phase-12 CEvNS rate for orientation only, an in-RoI flag, an ordering-crossover flag and BOTH accuracy labels. The header states what the file is not, and that nothing in it bounds the total background."
      linked_ids: [claim-inband-dominance]
    deliv-audit-tests:
      status: produced
      path: tests/test_em_rescope_audit.py
      summary: "15 tests. Token list imported BY IDENTITY with its digit-boundary regex exercised on 1.41 / 1.4150 / 1.4585; token scan clean over the computed closure with the allowlist and the prose-window rule justified in comments; every retired quantity enumerated by value with a disposition and a >40-character reason; each normalization factor individually unity plus the end-to-end rate evidence; the veto sentinel with its BY CONSTRUCTION docstring; the forbidden adjective with an attachment-aware window; bands not narrowed with the PDG-bracket enclosure asserted; the muon sign carrying both legs in a four-line window over every emitted file; labels reaching all four Plan 15-02/15-03 tables; the dominance table verified against a live re-run of the fold and against the Phase-12 CEvNS total; the forbidden ratio name absent; both labels on all 322 rows; dimensions; disposition rows; and an assertion that the audit states what a token scan can and cannot establish."
      linked_ids: [claim-rescope-audit, claim-accuracy-carried, claim-inband-dominance]
    deliv-audit-report:
      status: produced
      path: GPD/phases/15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em/15-04-RESCOPE-AUDIT.md
      summary: "Five sections: the SC4 audit with its scope, result, enumeration, sentinel, numeric complement, adjective scan and the two-readings statement; the SC5 carry-forward table; the dominance re-check with the confirmed ordering, the stated refinement and the crossovers; the phase closure with all five SC verdicts, the four findings that fired, the two that did not, what Phase 16 receives and six named gaps; and the verification ledger."
      linked_ids: [claim-rescope-audit, claim-accuracy-carried, claim-inband-dominance]
    deliv-disposition-rows:
      status: produced
      path: artifacts/v2.0/legacy_grid_disposition.csv
      summary: "Three rows: the audit and accuracy tables as not_a_spectrum, the dominance table as native_to_extended_axis with validity_floor 1.059254e-06 keV. Register now 62 rows; the git-ls-files closure guard passes."
      linked_ids: [claim-rescope-audit, claim-accuracy-carried, claim-inband-dominance]
  acceptance_tests:
    test-token-scan-clean:
      status: passed
      summary: "Zero applied hits over the 18-file import closure plus 10 emitted artifacts and 6 emitted documents; exactly one allowlist entry, in compton_source.py, with its justification asserted to exceed 80 characters; and the enumeration itself asserted non-empty so a scan that found nothing at all because it scanned nothing would fail."
      linked_ids: [claim-rescope-audit, deliv-audit-table, deliv-audit-tests]
    test-retired-quantities-named:
      status: passed
      summary: "Every quantity in the deliverable's must_contain block is present as its own row -- 2.92, m.w.e, 1.41, 5.03, 59.6, 3.28, 5.65, ~50, buildup, 99.8, ~5, 14, mcpd -- with 11 rows carrying the re-scope disposition, a zero applied-hit count, a scope of at least 30 files and a reason longer than 40 characters."
      linked_ids: [claim-rescope-audit, deliv-audit-table, deliv-audit-tests]
    test-factors-are-unity:
      status: passed
      summary: "Each of the five factors asserted 1.0 ONE AT A TIME, never as a product, and each present in the audit CSV with 'INDIVIDUALLY' in its disposition. Backed by end-to-end numeric evidence independent of the enumeration: the emitted muon header carries 1.3659 +/- 0.0003 Hz and the Compton header 2.6747e-01 Hz, which no surviving factor other than 1.0 could produce."
      linked_ids: [claim-rescope-audit, deliv-audit-table, deliv-audit-tests]
    test-veto-credit-sentinel:
      status: passed
      summary: "Exactly 1.0, a float, with 'BY CONSTRUCTION' asserted present in the function's own docstring and in the audit row's disposition. Every audit row whose token is veto_credit is either the sentinel at 1.0 or a retired rejection percentage with zero applied hits, and no emitted artifact carries a veto credit of any other value."
      linked_ids: [claim-rescope-audit, deliv-audit-table, deliv-audit-tests, ref-veto-credit]
    test-no-conservative-word:
      status: passed
      summary: "Zero occurrences attached to this configuration over the scanned scope. The check is attachment-aware -- an occurrence is allowed only inside a statement ABOUT the prohibition (a text scan, a zero count, the proxy id, the Phase-8 lock, the 'different and worse' phrasing) -- so the word could not appear as a description of the configuration and pass."
      linked_ids: [claim-rescope-audit, deliv-audit-tests, deliv-audit-report, ref-veto-credit]
    test-bands-not-narrowed:
      status: passed
      summary: "Gamma band exactly x0.5..x2.0 as v1.0 carried. Muon band x0.65..x1.35 asserted to ENCLOSE the PDG Leg A / Leg B bracket x0.8309..x1.2595 and to be at least the 30% spread, with '30-35%' and 'Gaisser-Guan' asserted present in the underlying_limit field. The emitted 15-03 band columns are checked bin by bin to use that same band and not a tighter one."
      linked_ids: [claim-accuracy-carried, deliv-accuracy-table, deliv-audit-tests, ref-mu-gamma-declaration]
    test-sign-carries-anchor-leg:
      status: passed
      summary: "Every occurrence of -20.61% in every emitted artifact and document is verified within a four-line window to carry BOTH 'Leg A' and 'Leg B'. The label row itself is checked for the signed deviation's sign character, the Leg A anchor, the Leg B disclosure, the +20.34 figure and the word BRACKET."
      linked_ids: [claim-accuracy-carried, deliv-accuracy-table, deliv-audit-report, deliv-audit-tests, ref-mu-gamma-declaration]
    test-labels-reach-artifacts:
      status: passed
      summary: "All 744 rows of each Plan 15-02 deposit table carry a single accuracy label matching this file's bias direction, with Leg A and Leg B present for the muon; all 161 rows of each Plan 15-03 reconstructed table carry both labels; and three representative tables are checked to expose an accuracy_label column so a rate cannot be read out without it."
      linked_ids: [claim-accuracy-carried, deliv-accuracy-table, deliv-audit-tests]
    test-dominance-recomputed:
      status: passed
      summary: "The test RE-RUNS the fold and asserts the frozen table reproduces it to rtol 1e-5, so the values are recomputed rather than quoted. Compton exceeds muon in the RoI by a ratio asserted to lie in (4.0, 5.5); the CEvNS orientation total is asserted to reproduce 118.730 to rel 1e-4; and the REFINEMENT is asserted numerically -- the muon RoI rate exceeds 1 count/kg/day and sits between 5% and 20% of the CEvNS rate, so 'muons land above the band' is measurably too strong. The report is asserted to contain the refinement, the neutron orientation figures 5430 / 5485 and the order_of_magnitude label."
      linked_ids: [claim-inband-dominance, deliv-dominance-table, deliv-audit-report, ref-rec-spectra, ref-cevns-ext]
    test-not-named-sb:
      status: passed
      summary: "Zero occurrences of the forbidden ratio name in any emitted artifact or document. The test constructs the string at runtime so the test file itself does not contain it. The dominance header is additionally asserted to say ORIENTATION ONLY, to name Phase 16 as the terminal owner, and to state that nothing in the file bounds the total background."
      linked_ids: [claim-inband-dominance, deliv-dominance-table, deliv-audit-tests, deliv-audit-report]
    test-labels-on-every-ratio:
      status: passed
      summary: "All 322 rows carry flatters_SB with both Leg A and Leg B for the muon and neutral with the x0.5 .. x2 band for the gamma. A ratio quoted without the labels of its inputs would invite a precision they do not support."
      linked_ids: [claim-inband-dominance, deliv-dominance-table, deliv-audit-tests]
    test-dimensions:
      status: passed
      summary: "Every non-label column header in all three emitted tables carries its units in brackets; the veto credit is dimensionless and exactly 1.0; every signed deviation carries a sign character AND a non-empty anchor leg; and the CEvNS column is named orientation_only in the header itself."
      linked_ids: [claim-accuracy-carried, deliv-audit-table, deliv-accuracy-table, deliv-dominance-table, deliv-audit-tests]
  references:
    ref-roadmap-sc4:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "SC4's requirement that each retired quantity be recorded as REMOVED rather than merely absent is what drives the 17-row enumeration; an audit reporting 'no hits' without naming what it searched for cannot distinguish deliberate removal from accidental omission. SC5's requirement that the labels be carried forward unchanged, and that no deliverable imply the axis extension improved a normalization, is enforced by the band-enclosure assertion and by the bin-by-bin check of the emitted band columns."
    ref-token-guard:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "surface_environment.shielded_token_guard() imported and asserted BY IDENTITY, not by equality, so a re-typed copy would fail the test. Its digit-boundary matching is exercised directly on 1.41 / 1.4150 / 1.4585 -- and it earned its keep: an ad-hoc substring scan written earlier in this phase false-positived the germanium lattice constant 5.658 A on the 5.65 Bq/kg 238U ambience, which this guard does not."
    ref-veto-credit:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "veto_credit() called and asserted to return exactly 1.0, with 'BY CONSTRUCTION' asserted present in its own docstring so the distinction from a policy default cannot be lost. The Phase-8 gate verdict's lock that this configuration is never described with the forbidden adjective is enforced by an attachment-aware text scan."
    ref-mu-gamma-declaration:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "Section 5's directional-bias schema is reused column for column in em_accuracy_labels.csv; Sections 2.5 and 3.4 supply both accuracy labels, the signed deviations, the anchor legs and the bracketing disclosure, all carried forward unnarrowed and cited as the v1_0_source field of each row."
    ref-rec-spectra:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "The Plan 15-03 reconstructed tables are the source of the dominance comparison, and the test re-runs run_em_fold_extended and asserts the frozen dominance table reproduces it, so nothing was transcribed."
    ref-cevns-ext:
      status: completed
      completed_actions: [read, compare]
      missing_actions: []
      summary: "The Phase-12 extended CEvNS reconstructed spectra are overlaid FOR ORIENTATION ONLY. Their axis is verified to be the same 161-bin reconstructed axis less the [0, 0.001] eV underflow bin, which is padded with 0.0 and the padding stated; and their integrated total is cross-checked at 118.7286 / 118.7292 against Phase 12's 118.730, so the right curve was read. They are NOT combined into any ratio named as a signal-to-background quantity."
  forbidden_proxies:
    fp-shielded-quantity-leak:
      status: rejected
      notes: "Zero applied hits over the full import closure plus every emitted artifact and document, with the token list imported by identity and the one allowlist entry justified in writing."
    fp-absence-without-enumeration:
      status: rejected
      notes: "17 rows, each naming a retired quantity WITH ITS RETIRED NUMERIC VALUE, the token searched, the scope, the hit count, the disposition and the reason it no longer applies. The audit does not merely report a clean scan."
    fp-product-instead-of-factors:
      status: rejected
      notes: "Each of the five factors is asserted 1.0 individually in code and recorded individually in the CSV, with 'INDIVIDUALLY' in the disposition column. The product is never used as the evidence."
    fp-reduced-credit:
      status: rejected
      notes: "Exactly 1.0 BY CONSTRUCTION, asserted from the function and from its docstring. No partial credit, no for-reference credit, and no modified veto geometry is proposed, sized or costed anywhere in this phase."
    fp-conservative-label:
      status: rejected
      notes: "Zero occurrences attached to this configuration. The one earlier occurrence described a physical CHOICE rather than the configuration and was reworded anyway, because a text check that must reason about attachment is a weak check; the check is now attachment-aware and would fail on a genuine description."
    fp-narrowed-band:
      status: rejected
      notes: "The gamma band is exactly v1.0's x0.5..x2. The muon band x0.65..x1.35 is asserted to ENCLOSE the PDG leg bracket rather than to sit inside it, and the emitted 15-03 band columns are checked bin by bin against it. No deliverable of this phase implies the axis extension improved a normalization."
    fp-bare-sign:
      status: rejected
      notes: "Every occurrence of -20.61% in every emitted artifact and document is machine-verified to carry both the Leg A citation and the Leg B bracketing within a four-line window."
    fp-sb-by-another-name:
      status: rejected
      notes: "The quantity computed here is a channel-magnitude comparison between two backgrounds, explicitly labelled orientation-only, with the CEvNS curve present so the overlap question can be asked and with the Phase-13 neutron channel named in the header as the reason nothing in the file bounds the total background. The forbidden name appears nowhere, and the test builds the string at runtime so the test file itself is clean."
  uncertainty_markers:
    weakest_anchors:
      - "The token scan is a STRONG CHECK, NOT A PROOF: a retired quantity re-entering under a NEW name with a NEW value is invisible to it, and an attribute-walk import closure cannot see a dynamically imported module. The individual-factor enumeration is the complement and the audit states both limitations in its own header rather than presenting the scan as complete coverage."
      - "The muon channel's directional-bias SIGN flips between the two PDG anchor legs and is therefore carried with its bracketing disclosure rather than as a settled direction."
      - "The gamma factor-2 band rests on the LABChico measured survey with the U-chain set by an assumed Phi_U = Phi_Th chain balance rather than a measured line intensity."
      - "The dominance comparison uses only two of the milestone's background channels. The Phase-13 neutron channel is 159x / 153x the Compton channel in the same band on an order_of_magnitude label, and the capture channel is not in scope, so NOTHING HERE BOUNDS THE TOTAL BACKGROUND."
    unvalidated_assumptions:
      - "RE-CHECKED rather than assumed: the v1.0 in-band dominance conclusion. The ordering is confirmed and the muon's in-band presence is refined."
      - "That every module reachable from this phase's artifacts is captured by the import-closure walk. The walk is over module attributes, as Plan 09-01 did; a dynamically imported module would escape it, none is used here, and the limitation is recorded rather than assumed away."
    competing_explanations:
      - "A clean token scan means no relocation quantity survived, versus a clean token scan means none survived UNDER A RECOGNISED NAME. The audit states in its own header and in the report that it has established the SECOND, not the first, and names the numeric-factor enumeration as the complement that partially closes the gap."
    disconfirming_observations:
      - "DID NOT FIRE: no shielded-configuration hit outside the named allowlist, so the Phase-9 re-scope-integrity trigger does not apply."
      - "DID NOT FIRE: no normalization factor other than exactly 1.0 appears anywhere between the frozen v1.0 rate and the emitted reconstructed spectrum, confirmed both by individual enumeration and by the end-to-end rates reproducing the frozen values."
      - "DID NOT FIRE: no accuracy band in any Phase-15 artifact is narrower than the v1.0 band it inherited."
      - "PARTIALLY FIRED: the extension does NOT change which channel dominates in the region of interest -- the Compton continuum remains the larger of the two electron-recoil backgrounds by 4.59x / 4.64x, confirming v1.0 -- but the v1.0 phrasing that muons land ABOVE the CEvNS band is measurably too strong, since the muon channel carries about 10% of the CEvNS rate within the band. Reported as a departure and a refinement, not reconciled away."
---

# Plan 15-04 Summary

## SC4 — the audit

**Zero applied relocation quantities** over a 31-file scope: the full 18-file import
closure, plus 10 emitted artifacts and 6 emitted documents. 35 token hits, 34 of
them the explicit not-applied enumeration SC4 demands, 1 the single Phase-9
allowlist entry (the germanium **target's** photon mass-attenuation coefficient,
which multiplies no normalization).

The token list is **imported by identity**, not re-typed — and that mattered: an
ad-hoc substring scan written earlier in this phase false-positived the germanium
lattice constant **5.658 Å** on the **5.65 Bq/kg** ²³⁸U ambience. The imported
guard's digit-boundary regex did not.

**All 11 retired quantities enumerated by name AND value** as removed, with a reason
each. Veto credit **exactly 1.0 BY CONSTRUCTION**. Every one of the five
normalization factors asserted **individually** unity — a product can be unity by
cancellation. The forbidden configuration adjective: **zero occurrences**.

**Which reading this establishes, stated plainly:** no relocation quantity survived
*under a recognised name or value*. **Not** that none survived at all — a token scan
cannot see a new name, and an attribute-walk closure cannot see a dynamic import.
A strong check, not a proof.

## SC5 — accuracy carried forward

Muon band **×0.65 … ×1.35** (the 30–35 % Gaisser–Guan spread), which **encloses**
the PDG Leg A / Leg B bracket ×0.8309 … ×1.2595 and therefore narrows nothing.
Gamma band **×0.5 … ×2.0**, exactly v1.0's. **Every** occurrence of −20.61 % in
every emitted file carries both Leg A and Leg B.

## The dominance re-check

| E_rec 10–100 eV | Ta→Al | Al→Hf |
|---|---|---|
| muon | 7.4656 | 7.7231 |
| **Compton** | **34.2484** | **35.8616** |
| CEvNS (orientation) | 72.9214 | 73.1441 |
| neutron (Phase 13, orientation) | 5430.29 | 5485.15 |

**CONFIRMED:** the Compton continuum is the larger of the two electron-recoil
channels in-band, by 4.59× / 4.64×, as v1.0 concluded.

**REFINED, and stated as a departure:** the v1.0 phrasing that muons land *above*
the CEvNS band is too strong. The muon channel carries ~10 % of the CEvNS rate
*inside* the band. It is subdominant there, not absent.

**Nothing here bounds the total background** — the neutron channel alone is 159× the
Compton channel in the same band.

## Phase closure

**All five success criteria MET as written.** No SC was superseded by measurement.
The four findings that fired (209 indicted v1.0 muon bins; the non-negligible
electron-side analogue; the factor-2 pile-up occupancy correction; the muon sub-eV
bounded absence) are about the **inherited record**, not about this phase's own
criteria. Six named gaps handed to Phase 16, including the standing flag that
`GPD/REQUIREMENTS.md` CALC-19/CALC-20 still carry their voided replacement clauses —
**for the orchestrator, not edited here**.

## Deviations

**One, documented.** The Phase-9 `NOT_APPLIED_MARKERS` needed a local extension and
prose needed a ±3-line scan window, because SC4 *requires* the enumeration and the
enumeration necessarily contains the tokens, often across a wrapped line. Source
files remain strictly line-scanned: an applied factor is a single assignment and
cannot hide behind a neighbour. Deviation Rule 4, applied inline with the
justification written into both the test and the audit header.
