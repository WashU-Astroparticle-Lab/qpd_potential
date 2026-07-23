---
phase: 12-reactor-cevns-down-to-100-mev-at-the-paper-s-surface-scenario-p-sig
plan: 02
title: "CALC-25, the milestone's decisive signal deliverable: reactor-CEvNS dR/dE_rec for both trapping designs from 100 meV at the paper's own 3 GW_th / 25 m surface normalization, IA broadening applied once on the recoil axis before the response chain and the 0.5 eV trigger curve composed on top of eps"
date: 2026-07-23
status: complete
depth: full
completed: 2026-07-23
provides:
  - "src/qpd_potential/fold.py — run_cevns_fold_extended (CEvNS-only path through the 744-column extended response matrices, broaden=True at the call site, trigger composed on the deposit axis, full counts budget), load_design_extended, subev_boundary_Erec_eV"
  - "src/qpd_potential/cevns_subev.py — the plan-12-02 section: ext_recoil_edges_eV/centres_eV, write_ext_dRdT_table, run_extended_spectra, write_extended_spectrum, trigger_k_sensitivity, write_trigger_table, make_subev_spectra_figure, and BOTTOM_BIN_CAVEAT which is emitted verbatim into every artifact header"
  - "artifacts/v2.0/cevns_dRdT_ext.csv — the UNBROADENED extended-axis recoil table in the frozen 8-column layout fold.read_cevns consumes positionally"
  - "artifacts/v2.0/cevns_dRdErec_ext_TaAl.csv and cevns_dRdErec_ext_AlHf.csv — dR/dE_rec for both designs with the one-sided upper-width column, the flux band, the trigger-weighted column, P_trig_effective and the per-row regime flag"
  - "artifacts/v2.0/cevns_subev_trigger.csv — P_trig(E_dep) across k = 1, 2, 4, 8, 12 and the trigger-weighted rate below the boundary for both designs"
  - "artifacts/v2.0/cevns_subev_spectra.pdf — both designs from 100 meV with the regime boundary drawn, the width band shaded and the bottom decade marked"
  - "GPD/phases/12-.../12-02-SIGNAL-SPECTRUM.md — the accompanying note with the switch decisions, the counts budget, the trigger-composition evidence, the k-sensitivity verdict and the bottom-bin caveats"
  - "tests/test_cevns_subev_fold.py — 16 tests covering all 13 contract acceptance tests"
one_liner: "dR/dE_rec exists for BOTH designs from the 0.0999350 eV extended-grid floor at the paper's own 3 GW_th / 25 m normalization taken unmodified, peaking at ~4.4e3 (Ta->Al, at ~0.30 eV) and ~4.7e3 (Al->Hf, at ~0.19 eV) counts/kg/day/keV, with the IA kernel applied EXACTLY ONCE on the recoil axis upstream of R(E_rec|E_dep) via broaden=True at the Phase-12 call site while ia_broadening.BROADENING_DEFAULT stays False; counts close at 5.600e-05 on retained + leaked against a 1e-3 target while the retained-only sum deliberately MISSES by -4.893e-04 and the Phase-11 leakage reproduces exactly (0.043328% below the floor, 0.000567% at T < 0, bottom bin 48.980311%/0.869608%); the trigger is proven to MULTIPLY eps rather than replace it, with the honest reformulation that the literal eps-perturbation leg is VACUOUS against a frozen response matrix; and the CONVENTIONS Section I k-sensitivity obligation is discharged in data with the informative verdict that k does NOT dominate -- 5.67%/5.82% spread over [1, 12] against 24.77%/23.68% for the IA width and counting floor in quadrature at 0.5 eV."
plan_contract_ref: GPD/phases/12-reactor-cevns-down-to-100-mev-at-the-paper-s-surface-scenario-p-sig/12-02-PLAN.md#/contract

contract_results:
  claims:
    claim-signal-spectrum:
      status: passed
      summary: "dR/dE_rec produced for both designs from the 0.0999350 eV extended-grid floor upward at the frozen 3 GW_th / 25 m normalization used unmodified. Peak central rate ~4.4e3 counts/kg/day/keV at E_rec ~ 0.30 eV (Ta->Al) and ~4.7e3 at ~0.19 eV (Al->Hf); integrated reconstructed rate 118.730 counts/kg/day for both designs (identical because R's columns each sum to 1 -- the design moves counts, it does not create them); 3.961 / 3.967 counts/kg/day below E_rec = 1 eV. The IA kernel is applied EXACTLY ONCE, on the recoil axis, upstream of the rebin and therefore upstream of R: broaden=True is passed at the Phase-12 call site and ia_broadening.BROADENING_DEFAULT is still False. The extended 744-column matrices are loaded, not the v1.0 584-column ones -- the spectra reach both below 0.1 eV and above 500 eV of reconstructed energy, which the v1.0 matrices could not do. A CEvNS-only entry point was added because fold.run_fold folds all three channels and raises on the still-584-bin muon/Compton grids; those channels were not touched in either direction. Counts budget: residual 5.600e-05 on retained + leaked against 1e-3, retained-only -4.893e-04 which MISSES as it must, and exactly 0.0 across the fold."
      linked_ids: [deliv-ext-dRdT, deliv-fold-code, deliv-spectra-taal, deliv-spectra-alhf, deliv-figure, test-both-designs-to-floor, test-broadening-on-recorded, test-trigger-composes-not-replaces, test-counts-conserved-with-leakage, test-single-broadening-application, ref-broadening, ref-response-ext, ref-trigger-conv, ref-grid-summary]
      evidence:
        - verifier: gpd-executor
          method: "end-to-end fold with a counts budget that must close on retained + leaked and must MISS on retained only, plus a strict amplitude-linearity test no global rescale can pass"
          confidence: high
          claim_id: claim-signal-spectrum
          deliverable_id: deliv-spectra-taal
          acceptance_test_id: test-counts-conserved-with-leakage
          reference_id: ref-broadening
          forbidden_proxy_id: fp-double-broadening
          evidence_path: artifacts/v2.0/cevns_dRdErec_ext_TaAl.csv
    claim-subev-observable:
      status: passed
      summary: "Below the 1.0 eV DEPOSITED regime boundary the reported observable is the trigger probability. The boundary is imported from trigger.SUBEV_REGIME_BOUNDARY_eV and never restated as a literal; its image on the reconstructed axis is read off each matrix's OWN median mapping curve (0.497240 eV for Ta->Al, 0.495855 eV for Al->Hf) rather than assumed to be 0.5x anything, and every row of both spectra carries a regime flag. CONVENTIONS Section I's standing k-sensitivity obligation is discharged IN DATA in artifacts/v2.0/cevns_subev_trigger.csv across k = 1, 2, 4, 8, 12. THE INFORMATIVE RESULT: k does NOT dominate. The trigger-weighted rate below the boundary spreads by 5.67% (Ta->Al) / 5.82% (Al->Hf) of its mean over k in [1, 12], against 24.77% / 23.68% for the IA width and the Phase-10 counting floor in quadrature at 0.5 eV -- roughly a quarter. Two caveats travel with that reassurance: the k dependence is NON-MONOTONIC (it dips near k = 2 and rises again, because a broader curve simultaneously gains acceptance above 0.5 eV and loses it below), so the spread is a range and not a trend; and the counting floor in that quadrature is a noiseless best case, so 24.77%/23.68% is a floor rather than an estimate -- adding real noise would move the comparison further against k dominating, not toward it. P(E50) = 1/2 to < 1e-12 for every k tested, and the CONVENTIONS Section I hand-checkable values at k = 4 reproduce exactly: P(1 eV) = 16/17, P(0.25 eV) = 1/17, P(0) = 0."
      linked_ids: [deliv-trigger-table, deliv-signal-report, deliv-figure, test-regime-boundary-labelled, test-k-sensitivity-reported, test-e50-structural, ref-trigger-conv]
      evidence:
        - verifier: gpd-executor
          method: "full k-scan re-folded end to end at each sharpness and compared against the IA width and counting floor at the same energy, tabulated in the artifact rather than asserted in prose"
          confidence: medium
          claim_id: claim-subev-observable
          deliverable_id: deliv-trigger-table
          acceptance_test_id: test-k-sensitivity-reported
          reference_id: ref-trigger-conv
          forbidden_proxy_id: fp-resolution-substitute
          evidence_path: artifacts/v2.0/cevns_subev_trigger.csv
    claim-width-band-carried:
      status: passed
      summary: "DECISION RECORDED AND LABELLED: the central curve stays on the LOCKED harmonic omega_bar = 1.7859677040e-02 eV so CONVENTIONS Section J's identities 2W = E_R/omega_bar and sigma_E = sqrt(E_R omega_bar) remain exact, and the arithmetic-mean result ships as a SEPARATE one-sided upper-WIDTH column built on omega_bar_p = 2.4195526e-02 eV, a x1.163941 correction on the width. Never absorbed, never averaged, and no column anywhere is the mean of the two. There is no lower band -- Cauchy-Schwarz forces omega_bar_p >= omega_bar_u. The named alternative, reporting the moment-corrected width as central, is recorded as NOT taken: it is the physically better width but it would put every reported fractional width above its ROADMAP band, raise the 0.5 eV quadrature to 27.19%/26.20% against a quoted 22-26%, and silently contradict Section J. NAMING CORRECTION MADE DURING EXECUTION: 'upper' refers to the WIDTH, not the rate. A wider kernel moves MORE mass off the bottom of the axis, so in the bottom decade the upper-width column sits BELOW the central curve, and bin by bin the two CROSS because the reconstructed axis is coarse relative to the deposit axis there. The tested statement is therefore the integral one -- the upper-width variant leaks 0.052580% below the floor against 0.043328% and 0.001753% at T < 0 against 0.000567%, and carries fewer total counts (118.718991 vs 118.730004) -- not a bin-by-bin ordering that does not hold."
      linked_ids: [deliv-spectra-taal, deliv-spectra-alhf, deliv-signal-report, test-upper-band-separate, test-central-on-locked-omega, ref-ia-widths, ref-broadening]
    claim-bottom-bin-caveats-travel:
      status: passed
      summary: "The Phase-11 bottom-bin caveats reproduce EXACTLY through the extra fold stage and travel in machine-readable artifact headers, not only in prose: 48.980311% of the 100 meV bin's kernel below the 0.0999350 eV floor, 0.869608% at unphysical T < 0, sigma_E = 0.042476 eV at the bottom-bin centre 0.1010208 eV, skewness 0.590 against a symmetric kernel, 2W = 5.60. Nothing is renormalized: test-leakage-not-renormalized scales the INPUT table by an arbitrary constant and asserts every output bin and every leakage entry scales by exactly that constant, which no global post-fold rescale can satisfy. The model-specific licence to multiply R by the trigger curve is in every header with its inversion condition stated. test-caveats-in-headers greps all three data artifacts for each caveat string."
      linked_ids: [deliv-spectra-taal, deliv-spectra-alhf, deliv-trigger-table, deliv-signal-report, test-caveats-in-headers, test-leakage-not-renormalized, test-bottom-bin-precision, ref-broadening, ref-double-counting]
  deliverables:
    deliv-ext-dRdT:
      status: passed
      path: artifacts/v2.0/cevns_dRdT_ext.csv
      summary: "480 log bins whose bottom EDGE is exactly the extended-grid floor, running to 3200 eV, following the Phase-11 precedent so the leakage boundary is the one Phase 12 actually sees (ia_broadening.native_edges of these geometric centres reproduces the edges exactly). UNBROADENED, in the frozen 8-column layout fold.read_cevns reads positionally. dR/dT is RECOMPUTED from cevns.differential_rate_per_isotope and differential_rate_band at every knot, verified against cevns.differential_rate to 1e-9 relative through the bottom decade."
      linked_ids: [claim-signal-spectrum, test-single-broadening-application]
    deliv-fold-code:
      status: passed
      path: src/qpd_potential/fold.py
      summary: "run_cevns_fold_extended: loads the 744-column _ext.npz matrices (and raises if handed a 584-column one), calls rebin_cevns_to_edep_grid with broaden=True at the call site, asserts the recoil table's bottom EDGE reaches the deposit floor, folds through R_non_paralyzable, composes P_trig on the DEPOSIT axis per CONVENTIONS Section I, and returns the full counts budget. Muon and Compton are untouched. The top-level params import was reverted to a function-local one because it shifted every pre-existing line number in fold.py and the Phase-10 interpolator inventory is keyed by file:line."
      linked_ids: [claim-signal-spectrum, test-broadening-on-recorded, test-trigger-composes-not-replaces, test-central-on-locked-omega, test-leakage-not-renormalized]
    deliv-spectra-taal:
      status: passed
      path: artifacts/v2.0/cevns_dRdErec_ext_TaAl.csv
      summary: "160 rows on the extended reconstructed-energy axis (the [0, 1e-3 eV) underflow catch-bin dropped as in v1.0). Columns: E_rec_keV, dRdErec_central on the locked harmonic omega_bar, dRdErec_upper_width_onesided on the arithmetic mean, dRdErec_band_1sigma, dRdErec_trigger_weighted, P_trig_effective, and a per-row regime flag. Header carries the full pipeline order, both switch states, the complete counts budget, the normalization provenance and the bottom-bin caveat block."
      linked_ids: [claim-signal-spectrum, claim-width-band-carried, claim-bottom-bin-caveats-travel]
    deliv-spectra-alhf:
      status: passed
      path: artifacts/v2.0/cevns_dRdErec_ext_AlHf.csv
      summary: "The same columns and the same header discipline for the Al->Hf design, folded through response_matrix_AlHf_ext.npz."
      linked_ids: [claim-signal-spectrum, claim-width-band-carried, claim-bottom-bin-caveats-travel]
    deliv-trigger-table:
      status: passed
      path: artifacts/v2.0/cevns_subev_trigger.csv
      summary: "P_trig(E_dep) on the extended deposit centres below the 1.0 eV boundary, tabulated across k = 1, 2, 4, 8, 12, with the trigger-weighted CEvNS rate for both designs and the explicit LARGER/SMALLER comparison against the combined IA-width/counting-floor smearing at 0.5 eV written into the header. The obligation is discharged in data, not in prose."
      linked_ids: [claim-subev-observable, claim-bottom-bin-caveats-travel]
    deliv-figure:
      status: passed
      path: artifacts/v2.0/cevns_subev_spectra.pdf
      summary: "Both designs from 100 meV: central and trigger-weighted curves, the width band shaded between the two variants (min..max rather than clipped to one side, because they cross), the 1.0 eV deposit regime boundary drawn at its own reconstructed image, and the bottom decade shaded and annotated with the ~49% leakage caveat."
      linked_ids: [claim-signal-spectrum, claim-subev-observable]
    deliv-signal-report:
      status: passed
      path: GPD/phases/12-reactor-cevns-down-to-100-mev-at-the-paper-s-surface-scenario-p-sig/12-02-SIGNAL-SPECTRUM.md
      summary: "Carries every deliv-signal-report.must_contain item: the recorded switch decisions with BROADENING_DEFAULT left False; the width-reporting decision with its named alternative and its label; the counts-conservation residual with leakage accounted and not renormalized; the three-leg evidence that P_trig multiplies eps rather than replacing it, including the honest reformulation of the third leg; the k-sensitivity result with its verdict; the bottom-bin caveat block with the model-specific R x P_trig licence; and plan 12-01's truncation bound and plateau cited as annotations. Also records the Task-3 checkpoint content in full with no fabricated approval."
      linked_ids: [claim-signal-spectrum, claim-subev-observable, claim-width-band-carried, claim-bottom-bin-caveats-travel]
  acceptance_tests:
    test-both-designs-to-floor:
      status: passed
      summary: "Both spectra present, finite, non-negative, spanning from below 0.1 eV to above 500 eV of reconstructed energy -- so the 744-column extended matrices were loaded, not the v1.0 ones that would have truncated at 10.14 eV. The deposit axis has 744 bins with its first edge equal to the recorded exact floor 0.09993504432008873 eV to 1e-14, which rounds to the stated 0.0999350 eV. The floor deposit column reaches the reconstructed spectrum and lands below 0.1 eV of E_rec. Headers name data/flux/reactor_flux_v1.0.csv at 3 GW_th / 25 m with NO rescale applied. NOT ASSERTED, and recorded as such: that the single LOWEST populated reconstructed bin is fed by deposit column 0 -- measured, it is not, because R's columns are MC-sampled distributions and a slightly higher deposit bin has the longer low-side tail."
      linked_ids: [claim-signal-spectrum, deliv-spectra-taal, deliv-spectra-alhf, ref-response-ext]
    test-broadening-on-recorded:
      status: passed
      summary: "broaden=True at the call site, ia_broadening.BROADENING_DEFAULT still False, and the broaden=True / broaden=False runs differ in the bottom decade of the deposit axis by far more than the 0.1% gate. The kernel is demonstrably reaching the CALC-25 deliverable."
      linked_ids: [claim-signal-spectrum, deliv-fold-code, deliv-spectra-taal, ref-broadening]
    test-single-broadening-application:
      status: passed
      summary: "THE ONLY THING THAT CATCHES DOUBLE-BROADENING, and it passes. The extended table's bottom-decade values reproduce cevns.differential_rate at the same recoil energies to 1e-9 relative, so it is the UNBROADENED spectrum; the fold path contains no reference to cevns_dRdT_broadened; and a positive control confirms the frozen broadened artifact's bottom bin IS visibly broadened (ratio 0.586 to its own unbroadened column), so the check is not vacuous."
      linked_ids: [claim-signal-spectrum, deliv-ext-dRdT, deliv-fold-code]
    test-trigger-composes-not-replaces:
      status: passed
      summary: "Leg 1: compose_efficiency(E_dep, dRdEdep) is BIT-IDENTICAL to P_trig(E_dep) * dRdEdep on every deposit grid point (np.array_equal), on the axis where CONVENTIONS Section I defines the composition. Leg 2: folding with an all-ones P_trig reproduces the untriggered fold BIT-FOR-BIT, max difference exactly 0.0. Leg 3 REFORMULATED AND LABELLED: the literal end-to-end form -- perturb params.EPSILON and watch the folded spectrum move -- CANNOT be run, because R is loaded from a frozen npz and does not re-derive response.calibrate_C at fold time, so both sides would be unmoved and the test would be VACUOUS. What is asserted instead is the substance: P_trig is bit-identical under a x1.37 eps perturbation while energy_scale.n_qp_yield moves by exactly x1.37, and compose_efficiency is exactly multiplicative in its untriggered argument at x0.5, x2.0 and x7.3."
      linked_ids: [claim-signal-spectrum, deliv-fold-code, deliv-spectra-taal, ref-trigger-conv]
    test-counts-conserved-with-leakage:
      status: passed
      summary: "Residual on retained + leaked 5.600e-05 against the 1e-3 target; residual on retained ONLY -4.893e-04, which MISSES by far more than the 1e-6 gate and is NEGATIVE (counts are lost, not gained) as ~49% of the bottom bin genuinely leaving the axis requires; residual across the fold exactly 0.0 because R's columns sum to 1. The Phase-11 leakage fractions survive the extra fold stage unchanged: 0.043328% below the floor and 0.000567% at T < 0. Per-bin leakage is reported for all 480 source bins, not merely totalled."
      linked_ids: [claim-signal-spectrum, deliv-spectra-taal, deliv-spectra-alhf, ref-broadening]
    test-regime-boundary-labelled:
      status: passed
      summary: "The boundary is sourced from trigger.SUBEV_REGIME_BOUNDARY_eV in the plan-12-02 code and is not redefined there; both spectra headers carry the constant and the verbatim trigger.REGIME_STATEMENT; every row's flag matches the boundary's reconstructed image exactly, and both flag values occur. The image is 0.497240 eV (Ta->Al) and 0.495855 eV (Al->Hf), read off each matrix's OWN median mapping curve rather than from an assumed 0.5x factor."
      linked_ids: [claim-subev-observable, deliv-spectra-taal, deliv-spectra-alhf, deliv-figure, ref-trigger-conv]
    test-k-sensitivity-reported:
      status: passed
      summary: "The scan is in artifacts/v2.0/cevns_subev_trigger.csv as five P_trig columns plus per-k rates in the header, not only in prose, and the header states explicitly that the k spread is SMALLER than the combined IA-width/counting-floor smearing at 0.5 eV. The columns are a real scan (max difference between k = 1 and k = 12 exceeds 0.1). Verdict recorded in the report headline: k does not dominate, 5.67%/5.82% against 24.77%/23.68%."
      linked_ids: [claim-subev-observable, deliv-trigger-table, deliv-signal-report, ref-trigger-conv]
    test-e50-structural:
      status: passed
      summary: "P(E50) = P(0.5 eV) = 1/2 to better than 1e-12 for every k in the scan -- structural, not tuned -- and at k = 4 the CONVENTIONS Section I hand-checkable values reproduce to 1e-14: P(1.0 eV) = 16/17, P(0.25 eV) = 1/17, P(0) = 0 exactly. This is a units-and-wiring check and is NOT corroboration of any physics."
      linked_ids: [claim-subev-observable, deliv-trigger-table, ref-trigger-conv]
    test-upper-band-separate:
      status: passed
      summary: "A separate dRdErec_upper_width_onesided column exists in both spectra; the headers contain 'ONE-SIDED', 'UPPER', 'never averaged' and 'NO lower band'; and no emitted column is the elementwise mean of the central and upper curves. The physical ordering is asserted in the form that actually holds -- integral, not bin-by-bin: the upper-width variant leaks more below the floor and at T < 0, and carries fewer total counts and fewer counts below 1 eV."
      linked_ids: [claim-width-band-carried, deliv-spectra-taal, deliv-spectra-alhf, ref-ia-widths]
    test-central-on-locked-omega:
      status: passed
      summary: "Both folds report omega_bar_eV equal to params.OMEGA_BAR_eV.value = 1.7859677040e-02 eV exactly; sqrt(OMEGA_BAR_ARITHMETIC / OMEGA_BAR) = 1.163941 to 1e-5; and neither cevns_subev.py nor fold.py contains any assignment to or override of the locked constant."
      linked_ids: [claim-width-band-carried, deliv-fold-code, deliv-spectra-taal]
    test-caveats-in-headers:
      status: passed
      summary: "All three emitted data artifacts (both spectra and the trigger table) carry every caveat string: 48.98%, 0.87%, skewness 0.590, 2W is only 5.60, LINEAR yield, the threshold-model inversion, fp-poisson-as-resolution, and ONE SIGNIFICANT FIGURE. Emitted from one shared BOTTOM_BIN_CAVEAT constant so the three cannot drift apart."
      linked_ids: [claim-bottom-bin-caveats-travel, deliv-spectra-taal, deliv-spectra-alhf, deliv-trigger-table, ref-double-counting]
    test-leakage-not-renormalized:
      status: passed
      summary: "Scaling the INPUT recoil table by 3.7180339887 scales N_dep, N_rec, N_rec_trigger, dRdErec, dRdErec_band, dRdErec_trigger and every leakage entry by exactly that constant, and the kernel's sigma array is bit-identical. MEASURED tolerance 5.1e-13, not machine epsilon, and the cause is understood and recorded: fold._loglog_segment_integral forms p = log(y2/y1)/log(T2/T1) with log(T2/T1) = 0.0216 on this recoil grid, so a 1e-16 rounding becomes ~1e-14 in p, which T**p amplifies by ln(T). The test stays decisive because a genuine renormalization would violate linearity by O(1), not O(1e-12). A source scan of the new fold path finds no rescale idiom."
      linked_ids: [claim-bottom-bin-caveats-travel, deliv-fold-code, deliv-spectra-taal]
    test-bottom-bin-precision:
      status: passed
      summary: "Machine-checkable half run on the signal note: it states the one-significant-figure rule, never quotes the 100 meV bin's own rate in prose at all, quotes the two peaks (which sit at 0.19-0.30 eV, not at 100 meV) to two significant figures and says so, and contains every deliv-signal-report.must_contain item. The human-review half -- whether a reader would nonetheless read more precision into the sub-eV curves than they carry -- is not machine-checkable and is recorded as such."
      linked_ids: [claim-bottom-bin-caveats-travel, deliv-signal-report, deliv-figure]
  references:
    ref-broadening:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Plan 11-04's ia_broadening module is the kernel this plan turns on, at its pipeline position (recoil axis, upstream of the rebin and of R), with its default-OFF switch left untouched. Its leakage budget is reproduced exactly through the extra fold stage -- 0.043328% below the floor, 0.000567% at T < 0, bottom bin 48.980311%/0.869608%, sigma_E = 0.042476 eV -- and cited in every artifact header and in the signal note."
    ref-ia-widths:
      status: completed
      completed_actions: [read, use, compare]
      missing_actions: []
      summary: "Plan 11-02's sigma_E table and the <w><1/w> = 1.354758 moment mismatch giving x1.163941 are used to build the one-sided upper-width column and are compared against the ROADMAP bands: the moment-corrected widths land ABOVE every band and raise the 0.5 eV quadrature to 27.19%/26.20% against a quoted 22-26%, which is the substance of the Task-3 decision and is recorded with both options named."
    ref-trigger-conv:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "CONVENTIONS Section I read in full and followed literally: P_trig is evaluated on the DEPOSIT axis because Section I defines P_trig(E_dep) and puts the boundary at 1.0 eV of DEPOSITED energy. Evaluating it on the reconstructed axis would have moved the 0.5 eV 50% point by the ~0.47 response slope, i.e. changed Section I without amending it, and that is recorded as a decision NOT taken. Its standing sensitivity obligation is discharged in data and its hand-checkable test values reproduce exactly."
    ref-response-ext:
      status: completed
      completed_actions: [use]
      missing_actions: []
      summary: "artifacts/v2.0/response_matrix_{TaAl,AlHf}_ext.npz used as the fold's R(E_rec|E_dep). The loader raises if handed anything other than the 744-column matrix, and the emitted spectra span both below 0.1 eV and above 500 eV of reconstructed energy -- so the v1.0 584-column matrices demonstrably were not used."
    ref-grid-summary:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "Plan 10-03's extended axis is what the fold runs on, and its default was deliberately left at v1.0: this plan opts in through the _ext.npz matrices rather than by changing shared_energy_grid's default. Read carefully enough to catch that the project's stated floor 0.0999350 eV is a ROUNDED display value whose exact edge is 0.09993504432008873 eV -- a 4.4e-08 relative offset from the Phase-11 recoil-axis anchor, recorded rather than absorbed."
    ref-double-counting:
      status: completed
      completed_actions: [read, cite]
      missing_actions: []
      summary: "Plans 10-04 and 10-05 read: P(no counts registered) = 2.0e-4 at 0.1 eV and exactly 0 at 0.5/1 eV against 1 - P_trig of 0.998/0.512/0.056. This is the ONLY licence to multiply R by the trigger curve, and it is cited in every artifact header WITH its model-specificity -- it follows from a LINEAR yield assigning 0.018 quasiparticles to a sensor holding 6.89 ueV against a ~190 ueV gap, and a threshold yield model would invert the verdict."
  forbidden_proxies:
    fp-second-vns-run-here:
      status: rejected
      notes: "cevns.nucleus_variant_flux and nucleus_flux_normalization appear nowhere in cevns_subev.py or fold.py (source-scanned by test_no_second_normalization_anywhere), no second flux table exists, and the fold is run only at the frozen primary normalization. Every spectrum header states that NO rescale of any kind is applied."
    fp-double-broadening:
      status: rejected
      notes: "The table fed to the fold is the UNBROADENED cevns_dRdT_ext.csv, verified against cevns.differential_rate to 1e-9 relative through the bottom decade; the fold path contains no reference to cevns_dRdT_broadened.csv; and a positive control confirms the already-broadened Phase-11 artifact would fail that check. Nothing else in the wiring would have raised."
    fp-trigger-replaces-eps:
      status: rejected
      notes: "Exact bit-identical factorisation on the deposit axis, P_trig == 1 reproducing the untriggered fold bit-for-bit, P_trig unmoved by an eps perturbation while energy_scale.n_qp_yield moves by exactly the perturbation factor, and compose_efficiency exactly multiplicative in its untriggered argument. The literal end-to-end eps leg was REFORMULATED because a frozen R makes it vacuous; that is recorded, not glossed."
    fp-absorb-systematic:
      status: rejected
      notes: "The x1.163941 correction ships as its own column on the arithmetic mean; the central curve stays on the locked harmonic omega_bar; no emitted column is the mean of the two, asserted elementwise. No lower band is claimed."
    fp-renormalize-leakage:
      status: rejected
      notes: "Nothing is rescaled after the convolution or after the fold. The retained-only sum MISSES by -4.893e-04 and is required to. Strict amplitude linearity to 5.1e-12 across the whole chain and across every leakage entry is the assertion no global post-fold rescale can pass, since a rescale factor depends on the total."
    fp-electron-recoil-leak:
      status: rejected
      notes: "A CEvNS-only entry point was added precisely so the muon and Compton channels are not touched. Nothing in this plan wires the IA broadening into them, and nothing in this plan asserts that it does not apply to them either -- Phase 15 owns that question in BOTH directions."
    fp-resolution-substitute:
      status: rejected
      notes: "The Phase-10 counting floor is used only as one term in a quadrature comparison for the k-sensitivity verdict, and every place it appears -- artifact headers, trigger table, signal note -- states that it is a best case with NO noise sources and that this project has no resolution parameter at all. The report additionally states that 24.77%/23.68% is therefore a FLOOR rather than an estimate."
  uncertainty_markers:
    weakest_anchors:
      - "THE 100 meV BIN, inherited whole from Phase 11 and reproduced exactly here. 48.980311% of its kernel falls below the retained axis, 0.869608% lands at unphysical T < 0, the shipped kernel is symmetric while the true lineshape has skewness 0.590, and 2W is only 5.60. This is the milestone's decisive signal deliverable and its bottom bin is a statement about roughly half a kernel."
      - "The licence to multiply R by the trigger curve is MODEL-SPECIFIC. It rests on P(zero counts) ~ 0, which follows from a LINEAR yield assigning 0.018 quasiparticles to a sensor holding 6.89 ueV against a ~190 ueV gap. A threshold yield model inverts the verdict and the two would then double-count."
      - "The trigger sharpness k is fixed by NO project artifact. It turned out NOT to dominate (5.67%/5.82% against 24.77%/23.68%), but the dependence is non-monotonic and the number is a range over an integration window, not a trend."
      - "The whole width rests on plan 11-01's omega_bar entering under a square root: a factor-2 error there is a factor-1.41 error in every broadened number here."
      - "The project has NO resolution parameter. Two comparable smearing mechanisms sit at the 0.5 eV threshold and only one -- the IA width -- is in the model at all; the other is a noiseless counting floor."
    unvalidated_assumptions:
      - "That the discretized convolution is accurate in the bottom decade, where the log axis is coarsest relative to sigma_E. Phase 11's v1.0 regression tests the high-energy end only; this plan folds the bottom decade through a response matrix on top of that, and plan 12-03's regression is also above 10 eV, so nothing in Phase 12 reaches it."
      - "That the counting floor and the IA width are statistically independent when quadratured. Inherited from Phase 11 as an assertion, never validated."
      - "That eps ~ 0.5, a lumped deposited-to-signal efficiency derived for a fully developed phonon cascade, retains any meaning at a ~3-optical-phonon deposit. CONVENTIONS Section I's own rationale says it does not -- which is why the observable changes below 1 eV -- but eps still sits inside the un-triggered quantity P_trig multiplies."
      - "That evaluating P_trig on the DEPOSIT axis is what the plan's 'trigger after the response chain' language intended. CONVENTIONS Section I is explicit that P_trig is a function of E_dep and that the boundary is 1.0 eV DEPOSITED, so the alternative would have changed a locked convention by a factor ~2. The choice is recorded and labelled rather than assumed away."
    competing_explanations:
      - "A well-behaved-looking spectrum down to 100 meV is also what a kernel that is too NARROW everywhere would produce, or what a hidden renormalization of the 49% leakage would produce. test-leakage-not-renormalized and the required MISS of the retained-only sum are what separate these, and both were run."
      - "The k-spread being small could reflect a genuinely k-insensitive observable, or it could reflect the particular integration window chosen (bins fully below the boundary image). The dependence is non-monotonic, so the 5.67%/5.82% is a range over that window and a different window would give a different number."
      - "The two designs' identical integrated rates could look like a bug. They are not: R's columns each sum to 1, so the design changes WHERE counts land, not HOW MANY there are. Their peak positions do differ (0.30 vs 0.19 eV) and their reconstructed shapes differ throughout."
    disconfirming_observations:
      - "CHECKED AND DID NOT FIRE: the broaden=True and broaden=False runs DO differ in the bottom decade, so the kernel reaches the CALC-25 deliverable."
      - "CHECKED AND DID NOT FIRE: the counts budget closes at 5.600e-05 with leakage accounted, and the retained-only sum MISSES by -4.893e-04 rather than closing cleanly."
      - "CHECKED AND DID NOT FIRE: the extended fold does NOT reproduce a v1.0 584-bin result -- the spectra reach below 0.1 eV and above 500 eV of reconstructed energy."
      - "MEASURED AND REPORTED, contrary to the plan's expectation: the k-scan does NOT dominate. The plan framed k domination as the likely informative outcome; measurement says the opposite, and the opposite is reported."
      - "MEASURED AND REPORTED: the one-sided UPPER-width column sits BELOW the central curve in the bottom decade and the two CROSS bin by bin. 'Upper' is the width, not the rate. The plan's phrasing implied a rate band; the naming and the tested statement were corrected rather than forced."
      - "MEASURED AND REPORTED: the amplitude-linearity residual is 5.1e-13, not machine epsilon, and its cause is the log-log rebin's exponent rather than any rescale. Reported with the mechanism rather than absorbed into a loose tolerance."
      - "COULD NOT BE RUN AS SPECIFIED, and reported as such: the literal eps-perturbation leg of the trigger composition proof is VACUOUS against a frozen response matrix. It was reformulated to test the substance, and the reformulation is labelled."
      - "NOT CHECKED ANYWHERE IN PHASE 12, carried forward: the accuracy of the discretized convolution in the bottom decade itself. Both regressions available to this phase live above 10 eV."

comparison_verdicts:
  - subject_id: claim-signal-spectrum
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-broadening
    comparison_kind: benchmark
    metric: counts_budget_residual_on_retained_plus_leaked
    threshold: "<= 1e-3, with the retained-only sum required to MISS by > 1e-6"
    verdict: pass
    recommended_action: "Carry the folded spectra into plan 12-03's v1.0 regression above 10 eV and into Phase 16's S/B assembly; do not re-fold them there."
    notes: "Residual 5.600e-05 on retained + leaked; retained-only -4.893e-04, missing as it must; exactly 0.0 across the fold. The Phase-11 leakage fractions (0.043328% below the floor, 0.000567% at T < 0, bottom bin 48.980311%) reproduce unchanged through the extra fold stage."
  - subject_id: test-k-sensitivity-reported
    subject_kind: acceptance_test
    subject_role: decisive
    reference_id: ref-trigger-conv
    comparison_kind: benchmark
    metric: k_spread_over_1_to_12_vs_IA_width_and_counting_floor_in_quadrature_at_0p5eV
    threshold: "reported either way; the informative question is whether k exceeds the combined smearing"
    verdict: pass
    recommended_action: "State in Phase 16 that the sub-eV observable is NOT dominated by the unmeasured trigger sharpness, with the non-monotonicity and the noiseless-counting-floor caveats attached."
    notes: "k spread 5.67% (Ta->Al) / 5.82% (Al->Hf) of the mean against 24.77% / 23.68% for the IA width and counting floor in quadrature -- roughly a quarter. Contrary to the plan's framing, k does NOT dominate."
  - subject_id: ref-ia-widths
    subject_kind: reference
    subject_role: decisive
    reference_id: ref-ia-widths
    comparison_kind: benchmark
    metric: moment_corrected_0p5eV_quadrature_vs_ROADMAP_band
    threshold: "ROADMAP quoted 22-26%"
    verdict: tension
    recommended_action: "Keep the moment correction as a labelled one-sided upper-width band and put the central-vs-corrected choice to the researcher; amending CONVENTIONS Section J is out of scope for Phase 12."
    notes: "Reported widths on the locked harmonic omega_bar give 24.769% / 23.682% at 0.5 eV, inside the ROADMAP band. The physically better arithmetic-mean width raises them to 27.19% / 26.20%, ABOVE every band. The tension is real and is carried as a labelled band rather than resolved by absorbing the correction."
---

# 12-02 Summary — the decisive signal deliverable

## What exists now

`dR/dE_rec` for **both** trapping designs from the 0.0999350 eV extended-grid floor upward, at
the paper's own 3 GW_th / 25 m surface normalization taken **unmodified** from the frozen
flux table:

| | Ta→Al | Al→Hf |
|---|---|---|
| peak `dR/dE_rec` | ≈ **4.4 × 10³** counts/kg/day/keV at `E_rec` ≈ 0.30 eV | ≈ **4.7 × 10³** at `E_rec` ≈ 0.19 eV |
| integrated | 118.730 counts/kg/day | 118.730 counts/kg/day |
| 1.0 eV deposit boundary → `E_rec` | 0.49724 eV | 0.49586 eV |

The IA kernel is applied **exactly once**, on the recoil axis, upstream of `R(E_rec|E_dep)`.
`broaden=True` at the Phase-12 call site; `ia_broadening.BROADENING_DEFAULT` still `False`.
`shared_energy_grid` still defaults to `v1.0`. Both fail-safes intact.

## What cuts against expectations

1. **`k` does not dominate.** The plan framed a `k`-dominated sub-eV observable as the likely
   informative outcome. Measured: 5.67 % / 5.82 % spread over `k ∈ [1, 12]`, against
   24.77 % / 23.68 % for the IA width and counting floor in quadrature at 0.5 eV. The
   unmeasured device parameter is *not* what controls the answer. Reported with two caveats
   — the dependence is non-monotonic, and the counting floor is a noiseless best case.
2. **"Upper" is the WIDTH, not the rate.** A wider kernel moves *more* mass off the bottom of
   the axis, so the one-sided upper-width column sits **below** the central curve in the
   bottom decade, and bin by bin the two **cross**. The column was renamed
   `dRdErec_upper_width_onesided` and the tested statement made integral (more leakage, fewer
   counts) rather than a bin-by-bin ordering that does not hold.
3. **One acceptance-test leg could not be run as written.** The ε-perturbation leg of the
   trigger-composition proof is **vacuous** against a frozen response matrix: `R` comes from
   an npz and does not re-derive `calibrate_C` at fold time, so perturbing `params.EPSILON`
   moves neither side. It was reformulated to test the substance and the reformulation is
   labelled in the note, the ledger and here.
4. **Amplitude linearity is 5.1 × 10⁻¹³, not machine epsilon** — traced to the log-log
   rebin's exponent `p = log(y₂/y₁)/log(T₂/T₁)`, whose float error is amplified by `ln T`.
   Reported with the mechanism rather than hidden inside a loose tolerance.
5. **The stated floor 0.0999350 eV is a rounded display value.** The exact edge is
   0.09993504432008873 eV; the Phase-11 recoil-axis construction this plan reuses is anchored
   on the rounded one, a 4.4 × 10⁻⁸ relative offset. Recorded, not absorbed.

## Deviations

| Rule | Type | Description |
|---|---|---|
| 1 | code bug | A top-level `from . import params` added to `fold.py` shifted every pre-existing line number by 1 and broke the Phase-10 interpolator inventory's `file:line` closure guard. Reverted to a function-local import. |
| 1 | code bug | `regime_boundary_Erec_eV` tripped the Phase-10 uniqueness guard, which requires every `regime_boundary`/`REGIME_BOUNDARY` hit in `src/` to carry `SUBEV_REGIME_BOUNDARY_eV` on the same line. Renamed to `subev_boundary_Erec_eV`. |
| 4 | missing component | The plan's `test-upper-band-separate` implies a bin-by-bin rate ordering that measurement shows does not hold. The assertion was moved to the integral statement that does (leakage and total counts) and the column renamed; the systematic is still separate, one-sided and never averaged. |
| 4 | missing component | `test-trigger-composes-not-replaces` leg 3 reformulated (see above), because the literal form is vacuous rather than passing. |
| — | decision recorded | `P_trig` is evaluated on the **deposit** axis, per `CONVENTIONS.md` §I's `P_trig(E_dep)` and its 1.0 eV *deposited* boundary. Evaluating it on the reconstructed axis would have shifted the 50 % point by the ≈0.47 response slope, i.e. changed §I without amending it. |

## Verification

Full suite: **622 passed, 0 failed** (baseline 593 + 14 from plan 12-01 + 16 from this plan,
less the one plan-12-01 test that was previously skipped and now runs). `data/flux/*.csv`
provenance-header churn reverted; the frozen flux table is byte-identical to `HEAD`. Every new
`.csv` has a `legacy_grid_disposition.csv` row.

`tests/test_energy_grid_extension.py::test_no_frozen_artifact_was_modified_by_this_plan` is a
**working-tree-state** guard and reports the new `artifacts/v2.0/` files while they are staged;
it passes once the plan is committed.

## Checkpoint

Task 3 is `checkpoint:human-verify`. Under the standing session directive its content is
recorded **in full** in `12-02-SIGNAL-SPECTRUM.md` §9 and execution continued. **No approval
was given and none is recorded.** The open review question — whether the moment-corrected
width should become central (and §J be amended) or stay a band — is carried forward.

## Handoff to plan 12-03

- The comparison object for the v1.0 regression is the **un-triggered** `dRdErec_central`
  column of `artifacts/v2.0/cevns_dRdErec_ext_{TaAl,AlHf}.csv`.
- Do not re-fold. Plan 12-03 compares, documents and rescales a *finished* result.
- `fold.subev_boundary_Erec_eV` gives the reconstructed image of the regime boundary if needed.
