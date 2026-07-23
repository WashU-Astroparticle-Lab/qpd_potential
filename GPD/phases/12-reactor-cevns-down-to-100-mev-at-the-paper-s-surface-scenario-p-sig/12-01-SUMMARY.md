---
phase: 12-reactor-cevns-down-to-100-mev-at-the-paper-s-surface-scenario-p-sig
plan: 01
title: "Sub-eV CEvNS validity gates: the CALC-17 sub-100-keV flux-truncation bound with its conservatism proved from the frozen table's own slope, and the VALD-10 plateau leg against an independently computed analytic flat-box T->0 limit"
date: 2026-07-23
status: complete
depth: full
completed: 2026-07-23
provides:
  - "src/qpd_potential/cevns_subev.py — truncation_bound, isotope_zero_point_eV, e_min_reconciliation, flux_floor_slope, integral_flux, analytic_plateau, plateau_profile and the two artifact writers; no path reads, writes or extends the flux table"
  - "artifacts/v2.0/cevns_truncation_bound.csv — 480 rows from the 0.0999350 eV extended-grid floor to 3200 eV: per-isotope E_min and missing contribution, totals, bound fraction, the one-sided additive band, and the E^2-continuation comparison"
  - "artifacts/v2.0/cevns_plateau_profile.csv — 240 rows spanning the full ROADMAP SC2 window 0.0999350-10 eV: dR/dT, the analytic plateau, ratio, deficit, local log-log slope"
  - "GPD/phases/12-reactor-cevns-down-to-100-mev-at-the-paper-s-surface-scenario-p-sig/12-01-SUBEV-GATES.md — the gates report with the clause-by-clause SC2/SC4 verdict table and the recorded checkpoint content"
  - "tests/test_cevns_subev.py — 14 tests covering all 11 contract acceptance tests"
  - "The two numbers plan 12-02 annotates its spectra with: analytic plateau 2372.3683 counts/kg/day/keV and truncation bound 0.8027% (additive band 19.0177 counts/kg/day/keV) at the axis floor"
one_liner: "CALC-17 reproduces at 0.8027% at the 0.0999350 eV grid floor against the roadmap's <=0.81%, and its flat continuation is PROVED conservative from the frozen table's own slope (d log Phi/d log E = +0.0635...+0.0763 across the lowest knots, so Phi falls toward the floor and a constant continuation over-estimates the missing flux; the E^2 continuation gives 0.5804%, strictly smaller) -- the phase's primary non-identity disconfirming check, PASSED; the VALD-10 plateau leg passes with dR/dT(floor)/plateau = 0.99069 against an analytic flat-box plateau 2372.3683 counts/kg/day/keV built independently from the frozen intPhi = 7.495760e12, with both failure modes excluded by assertion; ROADMAP SC2's 'flat to within a few percent from 100 meV to 10 eV' clause is SUPERSEDED BY MEASUREMENT at a 44.30% deficit at 10 eV, reported without narrowing the window; SC4's 'exactly zero above 0.29 eV' is PARTIAL -- the isotope-resolved zero point is 0.3067 eV set by 70Ge -- and planning finding F2 is CORRECTED: the 0.29 eV residual is carried by FOUR still-open isotopes, not by 70Ge alone."
plan_contract_ref: GPD/phases/12-reactor-cevns-down-to-100-mev-at-the-paper-s-surface-scenario-p-sig/12-01-PLAN.md#/contract

contract_results:
  claims:
    claim-truncation-bound:
      status: passed
      summary: "Computed, not quoted. Per isotope, missing = N_i int_{E_min,i(T)}^{0.1 MeV} Phi_flat dsigma_i/dT dE with Phi_flat = Phi(0.1 MeV) = 3.445974e12 held constant as a LABELLED continuation constant, against tabulated = the pipeline's own integral (verified equal to cevns.differential_rate to 1e-9 relative). Bound fraction 0.8027% at the 0.0999350 eV extended-grid floor and 0.8020% at exactly 100 meV, both under the roadmap's 0.81%; 0.3825% at 0.15 eV; 8.84e-6 at 0.29 eV; EXACTLY 0.0 above 0.3067 eV. The zero point is isotope-resolved and set by the LIGHTEST isotope 70Ge (T_i = 2E^2/(M_i+2E) at E = 0.1 MeV, closed form, no scan): 76Ge 0.282511, 74Ge 0.290146, 73Ge 0.294121, 72Ge 0.298206, 70Ge 0.306726 eV. The roadmap's 0.29 eV is almost exactly 74Ge's OWN zero point. E_min(100 meV) reported under all three circulating masses -- 58.1914 keV (Phase-7 abundance-weighted nuclear mass 6.7724551e10 eV, ADOPTED), 58.1612 keV (CONVENTIONS Section D molar mass 72.63 u, which is the roadmap's 58.16 keV, REPRODUCED not quoted), 58.7072 keV (74Ge alone) -- spread 0.936%, entirely the mass spread. The flux table was NOT extended: 101 knots, floor 0.1 MeV, data rows byte-identical to HEAD, and a source scan finds no write/append/synthetic-knot path with the single sub-floor flux value confined to one labelled helper."
      linked_ids: [deliv-subev-module, deliv-truncation-table, deliv-gates-report, test-bound-magnitude, test-bound-vanishes, test-flat-continuation-is-upper-bound, test-emin-reconciliation, test-table-not-extended, ref-flux-frozen, ref-methods-truncation, ref-roadmap-p12]
      evidence:
        - verifier: gpd-executor
          method: "per-isotope quadrature of the project's own dsigma_dT against a labelled flat continuation, with the conservatism direction MEASURED from the frozen table's own local slope rather than assumed"
          confidence: high
          claim_id: claim-truncation-bound
          deliverable_id: deliv-truncation-table
          acceptance_test_id: test-bound-magnitude
          reference_id: ref-flux-frozen
          forbidden_proxy_id: fp-extend-flux-table
          evidence_path: artifacts/v2.0/cevns_truncation_bound.csv
    claim-plateau:
      status: passed
      summary: "The analytic flat-box T->0 plateau is 2372.3683 counts/kg/day/keV, built as sum_i N_i (G_F^2 M_i/4pi) Q_W_i^2 (hbar c)^2 x intPhi x 86400 with (1 - MT/2E^2) -> 1 and the Helm form factor OFF, from intPhi = 7.495760e12 nubar/cm^2/s integrated knot by knot over the frozen table's own span. It is INDEPENDENT of the fold: it never calls differential_rate and is rebuilt a second way in test_plateau_is_not_an_extrapolation_of_the_fold, so agreement is evidence rather than an identity (fp-plateau-by-extrapolation). Measured approach: dR/dT(0.0999350 eV) = 2350.274, ratio 0.99069, deficit 0.9313% -- inside the stated 1.5% gate. Both failure modes excluded by ASSERTION, not inspection: dR/dT is monotonically non-increasing across the whole 0.0999350-10 eV window with every local log-log slope <= 0 and never exceeds the plateau (so it does not rise, which would be a flux-extrapolation artifact); and there are no zero bins, ratio at the floor 0.9907 > 0.9, and no neighbour ratio above 10 (so it does not collapse, which would be a silently reached table floor). The deficit SHRINKS monotonically toward the floor and grows by a factor 47.6 out to 10 eV, which separates the kinematic explanation from a flat normalization offset."
      linked_ids: [deliv-subev-module, deliv-plateau-table, deliv-gates-report, test-plateau-value, test-does-not-rise, test-does-not-fall-to-zero, test-approaches-from-below, ref-flux-frozen, ref-conventions-c]
      evidence:
        - verifier: gpd-executor
          method: "analytic T->0 limit constructed from the integral flux and the locked cross-section prefactor, compared against the pipeline's own dR/dT over the full SC2 window"
          confidence: high
          claim_id: claim-plateau
          deliverable_id: deliv-plateau-table
          acceptance_test_id: test-plateau-value
          reference_id: ref-conventions-c
          forbidden_proxy_id: fp-plateau-by-extrapolation
          evidence_path: artifacts/v2.0/cevns_plateau_profile.csv
    claim-sc2-verdict:
      status: passed
      summary: "SC2's 'dR/dT is flat from 100 meV to 10 eV to within a few percent' is adjudicated SUPERSEDED BY MEASUREMENT with the numbers beside it: deficits 0.9313% / 1.7248% / 3.9437% / 12.8171% / 44.3018% at 0.0999 / 0.15 / 0.29 / 1.0 / 10.0 eV, i.e. a monotone 44.30% fall across the window, because E_min(T) rises as sqrt(T) and progressively cuts low-energy flux out of the fold -- the physically correct behaviour. The window was NOT narrowed: the emitted profile spans the full 0.0999350-10 eV interval and test_window_not_narrowed asserts it, and 'a few percent' was not restated as anything looser (fp-narrow-the-window). What PASSES is stated separately as the decisive content of the VALD-10 plateau leg: approach to the independently computed analytic plateau within 0.93% at the axis floor, monotone, neither rising nor collapsing. Every tolerance in tests/test_cevns_subev.py is a stated ROADMAP or recorded-planning target written before the artifacts were regenerated, not a value read off the output."
      linked_ids: [deliv-gates-report, deliv-plateau-table, test-sc2-adjudicated, test-window-not-narrowed, ref-roadmap-p12]
  deliverables:
    deliv-subev-module:
      status: passed
      path: src/qpd_potential/cevns_subev.py
      summary: "truncation_bound (per-isotope missing/tabulated under a labelled flat or E^2 continuation, with the missing term skipped ENTIRELY -- exactly 0.0, not a residual -- once E_min_i >= 0.1 MeV), isotope_zero_point_eV (closed-form per-isotope zero points, no scan), e_min_reconciliation (three masses, named, one adopted), flux_floor_slope (the disconfirming check, read straight off the CSV knots), integral_flux (knot-by-knot), analytic_plateau (fold-independent), plateau_profile, and the two artifact writers. No function reads, writes or extends the flux table, and ReactorFlux.flux() is never evaluated below its own floor."
      linked_ids: [claim-truncation-bound, claim-plateau]
    deliv-truncation-table:
      status: passed
      path: artifacts/v2.0/cevns_truncation_bound.csv
      summary: "480 rows on a log recoil axis whose first point is EXACTLY the 0.0999350 eV extended-grid floor, running to 3200 eV. Columns: T_eV, per-isotope E_min in keV, per-isotope missing contribution, missing_total, tabulated_total, bound_fraction, the one-sided ADDITIVE band in counts/kg/day/keV (METHODS.md 3.4's recommended form, shipped alongside the percentage), and the E^2-continuation bound for comparison. Header records the flat-continuation assumption, the measured slope evidence for its conservatism, the isotope-resolved zero point, the E_min reconciliation, and an explicit line stating the flux table was not extended."
      linked_ids: [claim-truncation-bound]
    deliv-plateau-table:
      status: passed
      path: artifacts/v2.0/cevns_plateau_profile.csv
      summary: "240 rows spanning the FULL ROADMAP SC2 window 0.0999350 eV to 10 eV with exact endpoints. Columns: T_eV, dRdT, analytic_plateau, ratio, deficit, local log-log slope. Emitted regardless of the verdict, and it is the evidence the SUPERSEDED verdict rests on."
      linked_ids: [claim-plateau, claim-sc2-verdict]
    deliv-gates-report:
      status: passed
      path: GPD/phases/12-reactor-cevns-down-to-100-mev-at-the-paper-s-surface-scenario-p-sig/12-01-SUBEV-GATES.md
      summary: "Carries every deliv-gates-report.must_contain item: the adopted E_min(100 meV) with all three masses named; the isotope-resolved zero point 0.3067 eV reconciled against the roadmap's 0.29 eV; the frozen table's own slope as the conservatism evidence; an explicit statement that the flux table was NOT extended; the measured plateau deficits at all five SC2 checkpoints; and a clause-by-clause PASS / SUPERSEDED / PARTIAL verdict table on SC2 and SC4. Also records the Task-3 checkpoint content in full with no fabricated approval."
      linked_ids: [claim-truncation-bound, claim-plateau, claim-sc2-verdict]
  acceptance_tests:
    test-bound-magnitude:
      status: passed
      summary: "0.8027% at the 0.0999350 eV floor -- under the ROADMAP SC4 target 0.81% and within 0.03% relative of the recorded planning value 0.803%, well inside the 1% relative gate. Cross-checked against the emitted artifact at the same energy to 1e-9."
      linked_ids: [claim-truncation-bound, deliv-truncation-table, ref-roadmap-p12]
    test-bound-vanishes:
      status: passed
      summary: "The bound is the number 0.0 -- not 'small' -- for every T above the isotope-resolved threshold 0.30673 eV, with all five isotopes flagged kinematically closed; every artifact row above that threshold is exactly 0.0. At exactly 0.29 eV the residual is 8.84e-6 of the total, non-zero and below the 1e-4 gate. REFINEMENT RECORDED: four isotopes (70, 72, 73, 74Ge) are still open at 0.29 eV, not 70Ge alone as planning finding F2 stated; 70Ge carries 70.8% of the residual and sets the threshold but does not exhaust it."
      linked_ids: [claim-truncation-bound, deliv-truncation-table, deliv-gates-report]
    test-flat-continuation-is-upper-bound:
      status: passed
      summary: "THE PHASE'S PRIMARY NON-IDENTITY DISCONFIRMING CHECK, and it passed. d log Phi / d log E across the frozen table's lowest five knots is +0.0635, +0.0673, +0.0717, +0.0763 -- all positive, so Phi DECREASES as E falls toward the 0.1 MeV floor and a constant continuation at Phi(0.1 MeV) over-estimates the missing flux. The E^2 (allowed-beta-branch) continuation gives 0.5804% at the floor, strictly smaller than the flat 0.8027%, as it must be. Had the slope run the other way the <=0.81% figure would not have been an upper bound and CALC-17's bound language would have had to be withdrawn."
      linked_ids: [claim-truncation-bound, deliv-truncation-table, ref-flux-frozen]
    test-emin-reconciliation:
      status: passed
      summary: "All three values reproduced from their masses and all three masses NAMED: 58.1914 keV (Phase-7 frozen abundance-weighted nuclear mass, adopted), 58.1612 keV (CONVENTIONS Section D molar mass 72.63 u -- this reproduces the roadmap's 58.16 keV rather than quoting it), 58.7072 keV (74Ge alone). Spread 0.936%, under the 1% gate and entirely accounted for by the mass spread. The adopted value is independently checked to equal cevns.E_min_MeV on the Phase-7 mass to 1e-12."
      linked_ids: [claim-truncation-bound, deliv-subev-module, deliv-gates-report]
    test-table-not-extended:
      status: passed
      summary: "The frozen table's DATA ROWS are byte-identical to HEAD (the provenance header stamp is excluded because the suite's own flux regeneration rewrites it -- pre-existing documented churn, reverted before commit); 101 knots with min(E_nu) = 0.1 MeV exactly and no knot below it. Source scan: no open() for writing on any data/flux path, no np.append / np.clip / fill_value / extrapolate=True idiom, and sub-floor Phi appears in exactly one labelled helper with one definition and one call site."
      linked_ids: [claim-truncation-bound, deliv-subev-module, ref-flux-frozen]
    test-plateau-value:
      status: passed
      summary: "Analytic plateau 2372.3683 counts/kg/day/keV against the stated target 2372.4 (2e-4 relative gate); intPhi 7.495760e12 against the recorded 7.4958e12. dR/dT(0.0999350 eV)/plateau = 0.99069, deficit 0.9313%, inside the 1.5%-below gate and matching the recorded planning value 0.93%. The plateau is built from the integral flux and the cross-section prefactor, never by extrapolating dR/dT downward."
      linked_ids: [claim-plateau, deliv-plateau-table, ref-flux-frozen, ref-conventions-c]
    test-does-not-rise:
      status: passed
      summary: "np.all(np.diff(dRdT) <= 0) over the whole 0.0999350-10 eV window, dR/dT < plateau at every point, and every local log-log slope <= 0. The spectrum falls monotonically; it does not rise anywhere, so no flux extrapolation below the table floor has crept past the max(E_min, flux.E_min) clamp."
      linked_ids: [claim-plateau, deliv-plateau-table]
    test-does-not-fall-to-zero:
      status: passed
      summary: "No zero bins anywhere in the window; dR/dT(floor)/plateau = 0.9907 > 0.9; the largest neighbour ratio is well under 10, so there is no order-of-magnitude discontinuity. The table floor is not being reached silently."
      linked_ids: [claim-plateau, deliv-plateau-table]
    test-approaches-from-below:
      status: passed
      summary: "The fractional deficit shrinks monotonically as T falls (np.all(np.diff(deficit) > 0) on the ascending-T axis), reaches 0.93% at the floor, and is NOT flat -- it grows by a factor 47.6 out to 10 eV. A flat deficit would have indicated a normalization offset masquerading as a kinematic approach; that competing explanation is excluded."
      linked_ids: [claim-plateau, deliv-plateau-table, deliv-gates-report]
    test-sc2-adjudicated:
      status: passed
      summary: "The gates report carries the verdict word SUPERSEDED against SC2's flatness clause with the measured 44.30% deficit at 10 eV beside it, and states separately what PASSES (approach to the analytic plateau within 0.93% at the axis floor; both failure modes excluded). The five SC2 deficit checkpoints are additionally asserted numerically in test_sc2_deficits_are_the_measured_ones so the verdict rests on recomputed numbers rather than on prose."
      linked_ids: [claim-sc2-verdict, deliv-gates-report, deliv-plateau-table]
    test-window-not-narrowed:
      status: passed
      summary: "The emitted plateau profile spans T from exactly 0.0999350 eV to exactly 10.0 eV with 240 points. Every tolerance in tests/test_cevns_subev.py is a named module-level constant sourced from ROADMAP SC2/SC4 or from the recorded planning measurements, not fitted to the output."
      linked_ids: [claim-sc2-verdict, deliv-plateau-table, deliv-subev-module]
  references:
    ref-flux-frozen:
      status: completed
      completed_actions: [read, use, compare]
      missing_actions: []
      summary: "Read: its lowest five knots were parsed directly off the CSV to measure d log Phi / d log E. Used: as the primary and only normalization, unmodified, for both the bound's denominator and the analytic plateau's intPhi. Compared: the current file's data rows against git HEAD (byte-identical), and its own local slope against the direction the flat continuation's upper-bound status requires."
    ref-roadmap-p12:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "SC2 and SC4 read verbatim from GPD/ROADMAP.md and adjudicated clause by clause in the gates report. SC4's <=0.81%, 0.29 eV zero point and 58.16 keV E_min are each REPRODUCED from the frozen table and compared against what was measured; SC2's flatness clause is compared against the measured 44.30% deficit and cited as SUPERSEDED."
    ref-methods-truncation:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "GPD/literature/METHODS.md section 3.4 read: it prescribes BOUNDING the unmeasured 58-100 keV band rather than modelling it, and recommends carrying it as an explicit additive uncertainty on dR/dT below 0.29 eV. Used: the truncation artifact ships the additive band in counts/kg/day/keV alongside the percentage, which is that recommended form. Section 3.4's independent statement that the CEvNS dR/dT plateaus rather than diverging as T -> 0 is the qualitative expectation the plateau leg then measures."
    ref-conventions-c:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "CONVENTIONS.md Section C's locked dsigma/dT form -- the /4pi prefactor, Q_W = N - (1-4 sin^2 theta_W) Z, the (1 - MT/2E^2) factor and (hbar c)^2 -- is what analytic_plateau takes the T -> 0 limit of, and it is reached through cevns.dsigma_dT rather than re-implemented. Section D's GE_ATOMS_PER_KG and the 3 GW_th / 25 m scenario fix the per-kg normalization; Section D is unchanged by this plan and is cited as such in the gates report."
  forbidden_proxies:
    fp-extend-flux-table:
      status: rejected
      notes: "No knot added below 0.1 MeV and no power-law or spline evaluation of Phi below its declared floor. The single sub-floor flux value in the module is the explicitly labelled _continuation_phi constant, held to one definition and one call site by test. The frozen table's data rows are byte-identical to HEAD after the run."
    fp-narrow-the-window:
      status: rejected
      notes: "SC2's flatness clause is reported SUPERSEDED with the measured 44.30% deficit rather than being made true. The plateau artifact spans the full 0.0999350-10 eV window and test_window_not_narrowed asserts both endpoints; 'a few percent' was not restated as a looser phrase."
    fp-plateau-by-extrapolation:
      status: rejected
      notes: "analytic_plateau never calls differential_rate and never uses dR/dT at the lowest bin. It is built from intPhi and the locked cross-section prefactor, and test_plateau_is_not_an_extrapolation_of_the_fold rebuilds it a second, independent way and asserts it differs from dR/dT(floor)."
    fp-bound-by-assertion:
      status: rejected
      notes: "0.81%, 58.16 keV, 0.29 eV and 2372.4 are all treated as TARGETS TO REPRODUCE, not sources. Each is recomputed here from the frozen table and the project's own cross section, and the tests compare the recomputed value against the roadmap figure rather than importing it."
  uncertainty_markers:
    weakest_anchors:
      - "The flat continuation of Phi below 100 keV. Its conservatism rests on the frozen table's own local slope over its lowest few knots -- a Huber-Mueller / summation hybrid whose sub-1.8 MeV region carries a declared 20-25% uncertainty and is a MODEL PLACEHOLDER. If that region's shape is wrong, the bound's DIRECTION, not just its size, is in question."
      - "The analytic plateau inherits the entire flux normalization. It is independent of the FOLD, not of Phi: a normalization error in the frozen table would move dR/dT and the plateau together and this comparison would not see it."
      - "The Helm form factor is taken as ~1 across the whole sub-eV window. True to far better than the bound at these momentum transfers, but assumed here rather than measured."
    unvalidated_assumptions:
      - "That cevns._fold_isotope's adaptive quad is accurate to well below 0.8% on the near-threshold integrand, where (1 - MT/2E^2) sweeps 0 to O(1) across the lowest decade of the flux. The single-call integral-flux quadrature emits a scipy roundoff warning; the knot-by-knot sum used here agrees with it to 4e-9, but the FOLD's per-isotope quadrature accuracy at the 0.8% level is still uncharacterised. METHODS.md 3.4 explicitly warns that adaptive quadrature under-resolves near-singular endpoint spikes."
      - "That reporting the truncation as a one-sided ADDITIVE band is the right form. It is what METHODS.md 3.4 recommends, but no downstream phase has yet declared how it wants to consume it, so both the band and the percentage ship."
    competing_explanations:
      - "A ~1% deficit from the analytic plateau at 100 meV could equally be a small normalization inconsistency between the plateau's integral-flux quadrature and the fold's per-isotope quadrature rather than the (1 - MT/2E^2) kinematic suppression. test-approaches-from-below separates them by requiring the deficit to SHRINK with falling T rather than sit flat -- it shrinks, and grows by a factor 47.6 out to 10 eV, so a constant offset is excluded."
      - "The truncation bound and the plateau share cevns.dsigma_dT and the frozen Phi. That shared dependence is a stated weakest anchor, NOT a cross-check: agreement between the two gates would not be evidence, so they are reported as two separate measurements against two separate targets."
    disconfirming_observations:
      - "MEASURED AND REPORTED: planning finding F2 is wrong on one point. The 0.29 eV residual is NOT attributable to 70Ge alone -- four of the five isotopes (70, 72, 73, 74Ge) still have E_min < 100 keV there and only 76Ge is closed. 70Ge carries 70.8% of it and sets the threshold, but does not exhaust it."
      - "MEASURED AND REPORTED: ROADMAP SC2's flatness clause is FALSE as literally written. dR/dT falls monotonically by 44.30% from 100 meV to 10 eV. Reported SUPERSEDED BY MEASUREMENT rather than narrowed."
      - "MEASURED AND REPORTED: SC4's 'exactly zero above 0.29 eV' does not hold at 0.29 eV. Exact zero requires T > 0.3067 eV, set by the lightest isotope. Reported PARTIAL with the reconciliation, not rounded to the roadmap figure."
      - "CHECKED AND DID NOT FIRE: Phi does not rise as E falls toward the 100 keV table floor. Had it risen, CALC-17's <=0.81% would not be an upper bound at all and the bound language would have had to be withdrawn."
      - "CHECKED AND DID NOT FIRE: dR/dT neither rises toward low T nor collapses to zero anywhere in the SC2 window."
      - "NOT CHECKED HERE, carried forward: whether the fold's per-isotope adaptive quadrature is itself accurate at the 0.8% level. This is the one place a systematic could sit under both the bound and the plateau deficit without either gate seeing it."

comparison_verdicts:
  - subject_id: test-bound-magnitude
    subject_kind: acceptance_test
    subject_role: decisive
    reference_id: ref-roadmap-p12
    comparison_kind: benchmark
    metric: bound_fraction_at_100meV
    threshold: "<= 0.0081 and within 1% relative of 0.00803"
    verdict: pass
    recommended_action: "Carry the 0.8027% bound and its additive band into plan 12-02's spectra as an annotation; do not re-derive it there."
    notes: "0.8027% at the 0.0999350 eV extended-grid floor, 0.8020% at exactly 100 meV. Reproduced from the frozen table and the project's own cross section, not quoted from the roadmap."
  - subject_id: ref-flux-frozen
    subject_kind: reference
    subject_role: decisive
    reference_id: ref-flux-frozen
    comparison_kind: benchmark
    metric: d_log_Phi_d_log_E_across_the_lowest_knots
    threshold: ">= 0 everywhere (Phi non-increasing as E falls toward the 0.1 MeV floor)"
    verdict: pass
    recommended_action: "Treat the flat-continuation bound as a genuine UPPER bound in all downstream use; re-run this check if the flux table is ever revised."
    notes: "+0.0635, +0.0673, +0.0717, +0.0763 across the five lowest knots. This is the phase's primary non-identity disconfirming check. The E^2 continuation gives a strictly smaller bound (0.5804% vs 0.8027%), corroborating the direction."
  - subject_id: ref-roadmap-p12
    subject_kind: reference
    subject_role: decisive
    reference_id: ref-roadmap-p12
    comparison_kind: benchmark
    metric: SC2_flatness_deficit_over_100meV_to_10eV
    threshold: "'within a few percent' as stated by ROADMAP SC2"
    verdict: fail
    recommended_action: "Report SC2's flatness clause SUPERSEDED BY MEASUREMENT and carry the restated gate -- approach to the analytic plateau within 1% at the axis floor, monotone, neither rising nor collapsing -- into the phase-level SC1-SC5 table in plan 12-03. Do not narrow the window."
    notes: "Measured deficit 0.9313% at the floor rising monotonically to 44.3018% at 10 eV. The FAIL is against the clause as literally written; the physics is correct (E_min(T) proportional to sqrt(T) cuts low-energy flux out of the fold). The decisive content of the VALD-10 plateau leg PASSES separately and is recorded under claim-plateau."
  - subject_id: claim-plateau
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-conventions-c
    comparison_kind: benchmark
    metric: dRdT_at_grid_floor_over_analytic_plateau
    threshold: "within 1.5% BELOW the independently computed plateau"
    verdict: pass
    recommended_action: "Use 2372.3683 counts/kg/day/keV as the reference plateau when annotating the plan-12-02 spectra."
    notes: "Ratio 0.99069, deficit 0.9313%, against an analytic plateau 2372.3683 counts/kg/day/keV built from intPhi = 7.495760e12 and the locked CONVENTIONS Section C prefactor with the form factor off. Independent of the fold, so the agreement is evidence rather than an identity."
---

# 12-01 Summary — Sub-eV CEvNS Validity Gates (CALC-17, VALD-10 plateau leg)

## What was established

Two independent gates on the **unbroadened** recoil spectrum, run first and alone so that
nothing downstream inherits a spectrum that is already wrong at the bottom of the axis.

**CALC-17.** The rate the frozen flux table cannot carry below its own 100 keV floor is
**0.8027 %** of `dR/dT` at the 0.0999350 eV extended-grid floor and **0.8020 %** at exactly
100 meV, both under the roadmap's ≤0.81 %. It falls to 0.3825 % at 0.15 eV, 8.84e-6 at
0.29 eV, and is **exactly 0.0** above **0.3067 eV**. Computed per isotope from the project's
own `dσ/dT`; nothing quoted.

**The conservatism argument is measured, not assumed.** `d log Φ / d log E` across the frozen
table's lowest five knots is `+0.0635, +0.0673, +0.0717, +0.0763` — all positive, so `Φ`
*decreases* as `E` falls toward the floor and a constant continuation over-estimates the
missing flux. The `E²` continuation gives 0.5804 %, strictly smaller. **This was the phase's
primary non-identity disconfirming check, and it passed.**

**VALD-10 plateau leg.** The analytic flat-box `T → 0` plateau, built independently of the
fold from `∫Φ = 7.495760e12` and the locked cross-section prefactor, is **2372.3683
counts/kg/day/keV**. `dR/dT` at the axis floor is 2350.274, a ratio of **0.99069** — 0.93 %
below, approaching from below. Both failure modes are excluded by assertion: monotone
non-increasing everywhere and never above the plateau (no rise); no zero bins, ratio 0.9907,
no order-of-magnitude step (no collapse).

## What cuts against expectations

Three things were measured that contradict what was written down, and all three are reported
rather than smoothed:

1. **ROADMAP SC2's flatness clause is false as written.** The spectrum falls monotonically by
   **44.30 %** from 100 meV to 10 eV. **SUPERSEDED BY MEASUREMENT.** The escape —
   narrowing the window to 0.1–0.3 eV where the deficit really is 0.9–3.9 % — is
   `fp-narrow-the-window` and was not taken; the artifact spans the full window and a test
   asserts it.
2. **SC4's "exactly zero above 0.29 eV" is PARTIAL.** Exact zero needs `T > 0.3067 eV`, set
   by the lightest isotope ⁷⁰Ge. The roadmap's 0.29 eV is essentially ⁷⁴Ge's own zero point
   (0.290146 eV).
3. **Planning finding F2 is corrected.** F2 says the 0.29 eV residual is ⁷⁰Ge alone. It is
   not: **four** isotopes (⁷⁰, ⁷², ⁷³, ⁷⁴Ge) are still kinematically open there and only ⁷⁶Ge
   is closed. ⁷⁰Ge carries 70.8 % of the residual and sets the threshold, but does not
   exhaust it.

`E_min(100 meV)` is adopted as **58.1914 keV** (Phase-7 abundance-weighted nuclear mass), not
the roadmap's 58.16 keV — which is reproduced here and attributed to the §D molar mass 72.63 u.
The ⁷⁴Ge-only 58.7072 keV is the third. Spread 0.936 %, entirely the mass spread.

## Deviations

| Rule | Type | Description |
|---|---|---|
| 4 | missing component | The plan and planning finding F2 both describe the 0.29 eV residual as ⁷⁰Ge alone. Measured, four isotopes contribute. The test written from F2 failed, was investigated rather than relaxed, and the correct four-isotope structure is now asserted and reported. Correctness fix, no scope change. |
| — | non-deviation, recorded | `integral_flux` integrates knot by knot rather than in a single adaptive `quad` call, because the single call emits a scipy roundoff warning on the PCHIP(log Φ) interpolant. The two agree to 4e-9 relative. Recorded because METHODS.md §3.4 warns specifically about adaptive quadrature on this class of integrand. |

## Verification

Full suite: **607 passed, 0 failed** (baseline 593 + 14 new tests in
`tests/test_cevns_subev.py`). The `data/flux/*.csv` provenance-header churn the suite produces
was reverted before commit and the frozen flux table is byte-identical to HEAD.

`tests/test_energy_grid_extension.py::test_no_frozen_artifact_was_modified_by_this_plan` is a
**working-tree-state** guard (`git status --porcelain data/ artifacts/`) and reports the new,
not-yet-committed `artifacts/v2.0/` files while they are staged. It passes once the plan is
committed. This is the closure guard working, not a regression.

## Checkpoint

Task 3 is `checkpoint:human-verify`. Under the standing session directive its content is
recorded **in full** in `12-01-SUBEV-GATES.md` §5 and execution continued. **No approval was
given and none is recorded.** The review question — whether "approaches the analytic plateau
within 1 % at the axis floor, monotone, neither rising nor collapsing" is the right restatement
of the VALD-10 plateau gate — is open and carried forward.

## Handoff to plan 12-02

- Use **2372.3683 counts/kg/day/keV** as the reference plateau when annotating the folded
  spectra, and **0.8027 %** (additive band 19.0177 counts/kg/day/keV) as the truncation bound
  at the axis floor.
- Do **not** re-derive either. Plan 12-02 annotates; it does not recompute.
- `cevns_subev.py` is the shared module; plans 12-02 and 12-03 extend it rather than forking it.
