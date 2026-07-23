---
phase: 15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em
plan: 03
title: "Muon and Compton dR/dE_rec for both trapping designs on the extended axis with five guards that raise, counts conserved to 2e-16, the v1.0 saturation shown to survive as a 77x-101x instrumental compression, the sub-eV observable measured NOT to be dominated by the unmeasured trigger sharpness -- and the v1.0 pile-up occupancy corrected by a factor 2 as a 20 us / 40 us conflation"
date: 2026-07-23
status: complete
depth: full
completed: 2026-07-23
provides:
  - "src/qpd_potential/fold.py (15-03 section, APPENDED so no earlier line number moved) -- run_em_fold_extended with five guards that all RAISE, NonFiniteDepositError, NO_SUPPORT_POLICIES with no zero-fill member, read_em_deposit_table, EM_EXT_CSV, EM_EXT_RECON_FILE"
  - "artifacts/v2.0/em_dRdErec_ext_TaAl.csv and em_dRdErec_ext_AlHf.csv -- both channels, untriggered and trigger-weighted, with bands, regime flags and per-row accuracy labels"
  - "artifacts/v2.0/em_trigger_k_sensitivity.csv -- every triggered quantity at k = 1,2,3,4,6,8,10,12, spread as a RANGE"
  - "artifacts/v2.0/em_subev_spectra.pdf -- both channels, both designs, regime boundary marked, saturation annotated as INSTRUMENTAL, accuracy labels on the figure"
  - "tests/test_em_fold.py -- 21 tests covering all 15 contract acceptance tests"
  - "GPD/phases/15-.../15-03-RECONSTRUCTED-SPECTRA.md -- the fold results, the composition proof, the k-sensitivity, the saturation statement and what the sub-eV region supports"
  - "artifacts/v2.0/legacy_grid_disposition.csv -- disposition rows for the three new tracked artifacts (59 register rows)"
one_liner: "The electron-recoil extended fold path exists with FIVE guards that all raise and are all exercised by tests that try them -- the 744-column shape check, the Plan 15-01 applicability guard reading the verdict from em_recoil AT FOLD TIME rather than hard-coding a branch, the double-broadening guard that raises on an UNLABELLED table as well as a true one, a non-finite-input guard that RAISES unless the caller passes an explicit recorded policy because R is dense and one NaN would poison every reconstructed bin, and a direct grid-identity assertion replacing the neutron path's floor-coverage check since these channels are already on the deposit axis; counts conserve at residual_fold <= 2.169e-16 against ROADMAP SC2's 1e-3, with residual_retained_plus_leaked and residual_retained_only both exactly 0.0 and the budget carrying an explicit residuals_coincide_because_no_broadening flag so the coincidence is ONE statement rather than two confirmations; P_trig identically 1 reproduces the untriggered spectrum BIT-IDENTICALLY (np.array_equal, max difference exactly 0.0) for both channels and both designs and the CONVENTIONS Section I hand values reproduce with P(E50) = 1/2 at k = 1, 4 AND 12; the 1.0 eV regime boundary is imported from trigger.SUBEV_REGIME_BOUNDARY_eV and imaged onto each design's reconstructed axis by the response matrix's OWN median mapping curve at 0.497240 eV (Ta->Al) and 0.495855 eV (Al->Hf) rather than assumed to be 0.5x anything; the v1.0 SATURATION SURVIVES and is INSTRUMENTAL -- the deposit spectrum peaks at 1.4354 MeV but the reconstructed peak sits at 18.8365 keV (Ta->Al) and 14.9624 keV (Al->Hf), compressions of 77.1x and 101.3x onto the ceiling set by the 40 us non-paralyzable resolving time, and the feature is named instrumental with its mechanism in the report, both table headers and the figure annotation; the k-sensitivity obligation is discharged over the full declared range and ANSWERS the question rather than assuming it, the sub-eV triggered rate varying by only 1.099x-1.101x (muon) and 1.379x-1.385x (Compton) so the sub-eV observable is NOT dominated by the unmeasured k; and one disconfirming observation FIRED -- the recomputed pile-up occupancy is 6.533538e-05, a factor of exactly 2 above the v1.0 quoted ~3e-5, because the v1.0 figure is the 20 us SAMPLING occupancy (3.266768e-05) and not the 40 us resolving-time occupancy, precisely the conflation CONVENTIONS Section F's Numerical Factor Registry names by row, reported as a finding with both numbers and their exact factor-2 relation asserted in code rather than reconciled silently."
plan_contract_ref: GPD/phases/15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em/15-03-PLAN.md#/contract

contract_results:
  claims:
    claim-em-fold-path:
      status: passed
      summary: "fold.run_em_fold_extended appended to fold.py, modelled structurally on run_neutron_fold_extended so the two extended paths cannot drift apart silently, with ONE stated structural difference: these channels are ALREADY on the deposit axis, so there is no recoil-to-deposit rebin and the neutron path's floor-coverage assertion on the bottom bin EDGE is replaced by a DIRECT GRID-IDENTITY assertion of the input's 744 centres against the matrix's own E_dep_centers_eV at 1e-6 relative. FIVE GUARDS, ALL RAISING, ALL EXERCISED BY TESTS THAT TRY THEM. (1) 744-column shape check, message naming both 584 and 744. (2) Applicability: em_recoil.assert_nuclear_kernel_use(channel, broaden) is called at fold time, so the verdict is READ rather than a hard-coded branch and a later change to it cannot leave a stale branch here; a contradicting request raises ElectronRecoilBroadeningError carrying the verdict, the recoiling body, the reason, the consequence and fp-transplant-nuclear-width, and the returned dict reports broadening_verdict and broadening_reason so a caller that passed the guard has necessarily received them. (3) Double broadening: read_broadened_provenance + the rule that a table declaring NOTHING raises too, tested with both a true-declaring and a silent fixture. (4) Non-finite input: NonFiniteDepositError unless the caller passes an explicit no_support_policy from the closed vocabulary ('raise', 'exclude_and_record'); there is NO zero-fill member and a test asserts none exists. The policy and the excluded-bin count are written into the output header. np.nan_to_num appears in no executable line of fold.py -- it is named twice, in the guard message and in the docstring, precisely so the prohibition is discoverable at the point of temptation. (5) Grid identity. Additionally the matrices' columns are asserted to sum to 1 BEFORE folding, so residual_fold is a real numerical check on the fold rather than a measurement of the matrix. COUNTS BUDGET: deposit 1073206.424523 (muon) and 210277.108948 (Compton) for both designs; residual_fold 0.000e+00, 2.169e-16, 1.384e-16, 1.384e-16 -- thirteen decades inside ROADMAP SC2's 1e-3. residual_retained_plus_leaked and residual_retained_only are both exactly 0.0 and COINCIDE BY CONSTRUCTION because no broadening is applied, and the budget carries the explicit boolean residuals_coincide_because_no_broadening so this is reported as ONE statement rather than as two independent confirmations."
      linked_ids: [deliv-fold-path, deliv-fold-tests, test-shape-check-raises, test-applicability-guard-raises, test-double-broaden-raises, test-nan-guard-raises, test-counts-conservation, test-columns-sum-to-one, ref-neutron-fold, ref-ext-matrices, ref-applicability]
      evidence:
        - verifier: gpd-executor
          method: "each guard exercised by attempting the forbidden call and asserting the named exception, plus a source-level scan for np.nan_to_num over every executable line"
          confidence: high
          claim_id: claim-em-fold-path
          deliverable_id: deliv-fold-path
          acceptance_test_id: test-nan-guard-raises
          reference_id: ref-neutron-fold
          forbidden_proxy_id: fp-nan-to-num
          evidence_path: tests/test_em_fold.py
    claim-reconstructed-spectra:
      status: passed
      summary: "Both channels have dR/dE_rec on the extended reconstructed axis (161 bins) for both trapping designs, untriggered and trigger-weighted, at the v1.0 sea-level zero-overburden normalization with veto credit exactly 1.0. THE TRIGGER MULTIPLIES rather than replaces eps: it is applied on the DEPOSIT axis column-wise on N_dep before R acts, because the analysis efficiency is a per-event property of the deposit, and eps ~ 0.5 stays inside the untriggered quantity through energy_scale.n_qp_yield and response.calibrate_C. COMPOSITION PROVED RATHER THAN ASSUMED: with p_trig_override of all ones the maximum absolute difference against the untriggered spectrum is EXACTLY 0.0 and np.array_equal is True, for the counts array and the differential alike, for both channels and both designs. CONVENTIONS Section I hand values reproduce exactly at k = 4 -- P(0) = 0.0, P(0.25 eV) = 1/17, P(0.5 eV) = 1/2, P(1.0 eV) = 16/17 -- and P(E50) = 1/2 holds at k = 1 and k = 12 as well as at 4, which is structural rather than tuned. REGIME BOUNDARY: imported from trigger.SUBEV_REGIME_BOUNDARY_eV and never written as a literal; its reconstructed-axis image is read off the response matrix's OWN median mapping curve via fold.subev_boundary_Erec_eV, giving 0.497240 eV (Ta->Al) and 0.495855 eV (Al->Hf), and a test asserts these are the interpolated values and NOT 0.5 x the deposit boundary -- the near-coincidence is a property of the response chain, not an assumption fed into it. The emitted per-row regime flags are verified to agree bin for bin with the imported boundary. BOTH DESIGNS emitted, verified not to be copies of each other, with the per-design saturation onsets 52.9074 eV (Ta->Al) and 32.1300 eV (Al->Hf) reflected in the mapping. BANDS carried UNNARROWED: the muon band x0.65..x1.35 is the 30-35% inter-experiment Gaisser-Guan spread, deliberately chosen because it ENCLOSES the PDG Leg A / Leg B bracket x0.8309..x1.2595 and therefore narrows nothing; the Compton band is the x0.5..x2 site band. Every row carries both accuracy labels in full, with the muon label always containing Leg A, Leg B, -20.61%, +20.34% and the word BRACKET."
      linked_ids: [deliv-rec-taal, deliv-rec-alhf, deliv-figure, deliv-rec-report, test-ptrig-identity-one, test-ptrig-test-values, test-regime-boundary-imported, test-both-designs, test-dimensions, ref-conventions-I, ref-conventions-E, ref-ext-deposit-tables]
    claim-saturation-preserved:
      status: passed
      summary: "The v1.0 saturation behaviour survives the grid extension and is demonstrably INSTRUMENTAL. The muon deposit spectrum peaks at 1.4354 MeV -- the Landau MPV of a near-vertical chord -- and a linear eps ~ 0.5 map would place that near 0.7 MeV reconstructed. It appears instead at 18.8365 keV (Ta->Al) and 14.9624 keV (Al->Hf): COMPRESSIONS OF 77.1x AND 101.3x. The entire 197 MeV top of the deposit axis maps to only 34.7635 keV and 26.8449 keV. test_saturation_peak asserts the dominant deposit is of order MeV, that the reconstructed peak is below the ceiling, that peak/deposit < 0.05, that the compression exceeds 50x, and that the peak is not at a reconstructed energy proportional to the deposit -- any one of which would fail if the saturation had been lost in the re-grid. The mechanism is the 40 us NON-PARALYZABLE resolving time (deposited_spectra.RESOLVE_TIME_S = 4e-5 s, the 25 kHz Nyquist of the 50 kHz bandwidth, CONVENTIONS Section F, user decision at the Phase-5 review), and the feature is named INSTRUMENTAL with that mechanism in the report, in both emitted table headers and in the figure annotation. It is nowhere presented as a physical line (fp-saturation-as-line). PILE-UP OCCUPANCY RECOMPUTED, NOT QUOTED, AND IT DIFFERS: deposited_spectra.pileup_occupancy from the through-wafer rates (muon 1.365914 Hz, Compton 0.2674705 Hz, total 1.633385 Hz) with tau_d = 40 us gives R*tau = 6.533538e-05, a factor of EXACTLY 2 above the v1.0 quoted ~3e-5. The cause is identified rather than papered over: with the 20 us SAMPLING time instead, R*tau = 3.266768e-05 ~ 3e-5, so the v1.0 figure is the sampling-time occupancy and not the resolving-time occupancy -- precisely the conflation CONVENTIONS Section F's Numerical Factor Registry names by row ('Resolving time | 40 us (25 kHz Nyquist) | 20 us (50 kHz sampling) conflated'). Both numbers and their exact factor-2 relation are asserted in the test so neither can drift and the distinction cannot be lost again. The physical conclusion is unchanged: at 6.5e-05 the occupancy is four decades below the 1e-2 stop threshold, so muon pile-up does not preclude quiescent operation."
      linked_ids: [deliv-rec-taal, deliv-rec-alhf, deliv-rec-report, deliv-figure, test-saturation-peak, test-pileup-occupancy, test-peak-not-physical-line, ref-conventions-F, ref-deposited-spectra-module]
      evidence:
        - verifier: gpd-executor
          method: "the reconstructed peak located directly and compared against BOTH the instrumental ceiling and the deposit energy that dominates, so a peak that tracked the deposit would fail; the occupancy recomputed at both candidate timescales and their ratio asserted"
          confidence: high
          claim_id: claim-saturation-preserved
          deliverable_id: deliv-rec-report
          acceptance_test_id: test-pileup-occupancy
          reference_id: ref-deposited-spectra-module
          forbidden_proxy_id: fp-saturation-as-line
          evidence_path: GPD/phases/15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em/15-03-RECONSTRUCTED-SPECTRA.md
    claim-k-sensitivity:
      status: passed
      summary: "Every triggered quantity this plan emits is reported with its sensitivity to k over the DECLARED range params.TRIGGER_SHARPNESS_RANGE = [1.0, 12.0], evaluated at k = 1, 2, 3, 4, 6, 8, 10, 12 and frozen in artifacts/v2.0/em_trigger_k_sensitivity.csv as 12 rows: three quantities (total, sub-eV, 10-100 eV RoI trigger-weighted counts) for each of two channels and two designs, each with the untriggered value alongside for comparison. THE SPREAD IS REPORTED AS A RANGE, NOT AS A PLUS-OR-MINUS, and the header says why: a symmetric error bar would misrepresent an unmeasured CHOSEN parameter as a measured one. THE PLAN'S QUESTION IS ANSWERED BY MEASUREMENT RATHER THAN ASSUMED: the sub-eV triggered rate varies by 1.099x (muon Ta->Al), 1.101x (muon Al->Hf), 1.379x (Compton Ta->Al) and 1.385x (Compton Al->Hf) across the full range -- well under the order of magnitude that would make the sub-eV observable a parameter scan rather than a prediction. The named disconfirming observation 'the trigger-weighted sub-eV spectrum varies by more than an order of magnitude across k in [1,12]' was CHECKED and DID NOT FIRE, and the CSV carries an explicit varies_by_an_order_of_magnitude_or_more boolean per row that reads False everywhere. The totals are insensitive (ratio 1.000) because both spectra are dominated by deposits far above E50 = 0.5 eV where P_trig -> 1 for every k, and that explanation is stated rather than left as a coincidence. NO BARE TRIGGERED NUMBER: both emitted table headers state the default k, that k is fixed by no project artifact, that every triggered number is a one-parameter family over the declared range, and that a triggered quantity quoted without its k is fp-hardcoded-width; the figure legend carries 'k=4, range [1,12]' on every trigger-weighted curve; and the report quotes no triggered value without its k."
      linked_ids: [deliv-k-sensitivity, deliv-rec-report, deliv-figure, test-k-range-covered, test-no-bare-triggered-number, ref-conventions-I]
  deliverables:
    deliv-fold-path:
      status: produced
      path: src/qpd_potential/fold.py
      summary: "The 15-03 section, APPENDED so no earlier line number moved (fold.py line numbers are keyed by the Phase-10 interpolator inventory). Adds EM_EXT_CSV, EM_EXT_RECON_FILE, NO_SUPPORT_POLICIES, NonFiniteDepositError, read_em_deposit_table (leading-numeric parse so the trailing labels cannot be skipped) and run_em_fold_extended with its five guards and its counts budget."
      linked_ids: [claim-em-fold-path]
    deliv-rec-taal:
      status: produced
      path: artifacts/v2.0/em_dRdErec_ext_TaAl.csv
      summary: "161 rows. Columns: E_rec_keV, muon untriggered / triggered / band_lo / band_hi, compton untriggered / triggered / band_lo / band_hi, regime_flag, muon_accuracy_label, gamma_accuracy_label. Header records the design, the matrix file, the broadening verdict applied and where it was read from, k with the one-parameter-family statement and the pointer to the k-sensitivity table, the no-support policy with its excluded-bin counts per channel, the imported regime boundary and its reconstructed image, the band definitions with the statement that the muon band encloses the PDG bracket, the normalization statement, and the counts budget."
      linked_ids: [claim-reconstructed-spectra, claim-saturation-preserved]
    deliv-rec-alhf:
      status: produced
      path: artifacts/v2.0/em_dRdErec_ext_AlHf.csv
      summary: "161 rows, same columns and same provenance discipline, folded through its own extended matrix. Verified not to be a copy of the Ta->Al table."
      linked_ids: [claim-reconstructed-spectra, claim-saturation-preserved]
    deliv-k-sensitivity:
      status: produced
      path: artifacts/v2.0/em_trigger_k_sensitivity.csv
      summary: "12 rows x 8 k values, with the untriggered value, the range low and high, the hi/lo spread ratio and an explicit varies_by_an_order_of_magnitude_or_more boolean. Header states that k is fixed by no project artifact, that the spread is a RANGE and why, and that P(E50) = 1/2 for every k."
      linked_ids: [claim-k-sensitivity]
    deliv-figure:
      status: produced
      path: artifacts/v2.0/em_subev_spectra.pdf
      summary: "Two panels, one per design, both channels, untriggered solid and trigger-weighted dashed with k and its range in the legend, per-channel bands shaded, the regime boundary marked with its deposited value AND its reconstructed image and a note that the image is read off the matrix's own median mapping curve, the sub-eV region shaded with the trigger-probability regime statement, the muon peak annotated as an INSTRUMENTAL pile-up feature with the 40 us non-paralyzable mechanism named and the words 'NOT a physical line', and both accuracy labels with the muon bracketing disclosure printed on the figure itself."
      linked_ids: [claim-reconstructed-spectra, claim-saturation-preserved, claim-k-sensitivity]
    deliv-fold-tests:
      status: produced
      path: tests/test_em_fold.py
      summary: "21 tests. All five guards attempted and asserted to raise; columns sum to 1; counts conservation with the coincidence flag; P_trig identity leg by np.array_equal; Section I values including P(E50) at k = 1 and 12; regime boundary imported, interpolated and not 0.5x, with the emitted flags cross-checked; both designs distinct with their onsets; dimensions including dRdErec * dE == N_rec; no computed exp(-2W); saturation peak against both the ceiling and the deposit energy; pile-up occupancy at both timescales with their ratio; the instrumental naming in report and figure; k range covered with the range-not-plus-minus check; no bare triggered number; the sub-eV k spread measured; labels and bands unnarrowed with the PDG bracket enclosure asserted; disposition rows; and the Phase-9 token scan."
      linked_ids: [claim-em-fold-path, claim-reconstructed-spectra, claim-saturation-preserved, claim-k-sensitivity]
    deliv-rec-report:
      status: produced
      path: GPD/phases/15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em/15-03-RECONSTRUCTED-SPECTRA.md
      summary: "Nine sections: the fold path and its five guards with the counts budget; the trigger composition proof and the imported regime boundary; the full k-sensitivity table with the answer to the plan's question; the saturation statement with the compression factors and the pile-up finding; what the sub-eV reconstructed region does and does not support once both the Plan 15-01 floors and the Plan 15-02 adequacy labels are applied; bands and labels; the in-band orientation numbers handed to Plan 15-04; the verification ledger; and uncertainty markers naming which disconfirming observations fired."
      linked_ids: [claim-em-fold-path, claim-reconstructed-spectra, claim-saturation-preserved, claim-k-sensitivity]
    deliv-disposition-rows:
      status: produced
      path: artifacts/v2.0/legacy_grid_disposition.csv
      summary: "Three rows: the two reconstructed tables as native_to_extended_axis with validity_floor 1.059254e-06 keV, and the k-sensitivity table as not_a_spectrum. Register now 59 rows; the closure guard passes."
      linked_ids: [claim-reconstructed-spectra, claim-k-sensitivity]
  acceptance_tests:
    test-shape-check-raises:
      status: passed
      summary: "The 744-column requirement raises with a message naming both 584 and 744, and a 584-bin deposit vector is rejected by the grid-identity guard with the same numbers in the message."
      linked_ids: [claim-em-fold-path, deliv-fold-path, deliv-fold-tests]
    test-applicability-guard-raises:
      status: passed
      summary: "broaden=True raises er.ElectronRecoilBroadeningError for both channels and both designs, with does_not_apply, REASON: and fp-transplant-nuclear-width in the message. The verdict is verified to be READ at fold time: the returned dict's broadening_verdict and broadening_reason equal em_recoil.ia_verdict(channel)'s, and the source is asserted to contain the fold-time call rather than a hard-coded branch."
      linked_ids: [claim-em-fold-path, deliv-fold-path, deliv-fold-tests, ref-applicability]
    test-double-broaden-raises:
      status: passed
      summary: "A fixture declaring broadened_provenance = true and a fixture declaring NOTHING both raise; read_broadened_provenance returns True and None respectively, confirming the fixtures are what they claim. The real tables return exactly False, so the guard would not misfire if the verdict ever changed."
      linked_ids: [claim-em-fold-path, deliv-fold-path, deliv-fold-tests, ref-neutron-fold]
    test-nan-guard-raises:
      status: passed
      summary: "The unpolicied call raises NonFiniteDepositError with 'dense' and 'nan_to_num' in the message; the policied call returns, records the policy and the excluded counts (35 muon, 69 Compton), and produces a fully finite reconstructed axis. NO_SUPPORT_POLICIES is asserted to be exactly ('raise', 'exclude_and_record') with no zero-fill member."
      linked_ids: [claim-em-fold-path, deliv-fold-path, deliv-fold-tests]
    test-counts-conservation:
      status: passed
      summary: "residual_fold 0.000e+00 / 2.169e-16 / 1.384e-16 / 1.384e-16 against ROADMAP SC2's 1e-3, and asserted below 1e-12 as well so a real conservation failure could not hide inside the contract tolerance. The two leakage residuals are present as separate fields, both 0.0, with residuals_coincide_because_no_broadening = True."
      linked_ids: [claim-em-fold-path, deliv-rec-taal, deliv-rec-alhf, deliv-fold-tests]
    test-columns-sum-to-one:
      status: passed
      summary: "Both extended matrices' columns sum to 1 to atol 1e-9, asserted in the test and again inside the fold BEFORE the multiplication, so residual_fold is a check on the fold rather than on the matrix."
      linked_ids: [claim-em-fold-path, deliv-fold-tests, ref-ext-matrices]
    test-ptrig-identity-one:
      status: passed
      summary: "np.array_equal on both the counts array and the differential, and max absolute difference EXACTLY 0.0, for both channels and both designs."
      linked_ids: [claim-reconstructed-spectra, deliv-fold-tests, ref-conventions-I]
    test-ptrig-test-values:
      status: passed
      summary: "P(0) = 0.0 exactly, P(0.25 eV) = 1/17, P(0.5 eV) = 1/2, P(1.0 eV) = 16/17 at k = 4; and P(E50) = 1/2 at k = 1, 4 and 12, which is a property of the functional form rather than of any width."
      linked_ids: [claim-reconstructed-spectra, deliv-fold-tests, ref-conventions-I]
    test-regime-boundary-imported:
      status: passed
      summary: "The boundary is imported at every use; its reconstructed image equals a fresh log-log interpolation of the matrix's own median mapping curve to 1e-12 and is asserted NOT to equal 0.5 x the deposit boundary; the emitted per-row regime flags are verified to agree bin for bin; and the 15-03 code section is scanned for hard-coded boundary literals."
      linked_ids: [claim-reconstructed-spectra, deliv-rec-taal, deliv-rec-alhf, deliv-fold-tests]
    test-both-designs:
      status: passed
      summary: "Both tables exist with 161 rows, each header names its own matrix file, the muon columns are asserted NOT to be equal between designs, and the per-design saturation onsets 52.9074 eV (Ta->Al) and 32.1300 eV (Al->Hf) are reproduced with the expected ordering."
      linked_ids: [claim-reconstructed-spectra, deliv-rec-taal, deliv-rec-alhf, deliv-fold-tests]
    test-saturation-peak:
      status: passed
      summary: "Muon reconstructed peak 18.8365 keV (Ta->Al) and 14.9624 keV (Al->Hf) against a dominant deposit of 1.4354 MeV: compression 77.1x and 101.3x. Asserted that the dominant deposit is of order MeV, that the peak is below the instrumental ceiling, that peak/deposit < 0.05, that the compression exceeds 50x, and that the peak is far below what a linear eps ~ 0.5 map would give -- so a peak that tracked the deposit energy would fail."
      linked_ids: [claim-saturation-preserved, deliv-rec-taal, deliv-rec-alhf, deliv-fold-tests, ref-conventions-F]
    test-pileup-occupancy:
      status: passed
      summary: "RECOMPUTED, not quoted: R = 1.633385 Hz, tau_d = 40 us, R*tau = 6.533538e-05, stop_condition False. IT DIFFERS MATERIALLY FROM THE v1.0 ~3e-5 BY A FACTOR OF EXACTLY 2, and the cause is identified: the 20 us sampling occupancy is 3.266768e-05 ~ 3e-5, so the v1.0 figure belongs to the sampling time and not the resolving time -- the conflation CONVENTIONS Section F's Numerical Factor Registry names by row. Both occupancies and their exact 2:1 relation are asserted, and the report carries both numbers."
      linked_ids: [claim-saturation-preserved, deliv-rec-report, deliv-fold-tests, ref-deposited-spectra-module]
    test-peak-not-physical-line:
      status: passed
      summary: "The report names the feature instrumental, names the 40 us non-paralyzable mechanism, and states in words that it is not a physical line; the figure exists and carries the same annotation on the peak. No caption or table label anywhere implies a physical spectral feature."
      linked_ids: [claim-saturation-preserved, deliv-rec-report, deliv-figure]
    test-k-range-covered:
      status: passed
      summary: "12 rows covering both channels and both designs at k = 1, 2, 3, 4, 6, 8, 10, 12, with min(k) and max(k) asserted to equal params.TRIGGER_SHARPNESS_RANGE and the recorded range_lo / range_hi asserted to equal the actual min and max of the evaluated series. The header's 'RANGE, NOT AS A PLUS-OR-MINUS' statement is asserted present and no plus-or-minus appears after it."
      linked_ids: [claim-k-sensitivity, deliv-k-sensitivity, deliv-fold-tests, ref-conventions-I]
    test-no-bare-triggered-number:
      status: passed
      summary: "Both emitted headers carry the k value, the one-parameter-family statement and fp-hardcoded-width; the report carries k = 4 and the range [1, 12] and names fp-hardcoded-width; the figure legend carries k and its range on every trigger-weighted curve."
      linked_ids: [claim-k-sensitivity, deliv-rec-taal, deliv-rec-alhf, deliv-figure, deliv-rec-report]
    test-dimensions:
      status: passed
      summary: "Every non-label column header carries its units; every rate column is [counts/kg/day/keV]; dRdErec * dE_rec reproduces N_rec to rtol 1e-12, so the counts-versus-differential distinction is exact and explicit; N_rec has 161 entries and N_dep has 744; P_trig lies in [0, 1]."
      linked_ids: [claim-reconstructed-spectra, deliv-rec-taal, deliv-rec-alhf, deliv-fold-tests]
  references:
    ref-neutron-fold:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "run_neutron_fold_extended read in full and followed structurally: same guard ordering, same counts-budget field names, same separation of the two leakage residuals, same appended-not-inserted discipline. Its APPLICABILITY paragraph -- which states verbatim that Phase 15's electron-recoil channels are a separate question -- is what Plan 15-01 discharged and this path enforces. read_broadened_provenance and DoubleBroadeningError are REUSED rather than re-implemented."
    ref-conventions-I:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "E50 = 0.5 eV exactly, the Hill form, the composition rule that P_trig multiplies eps, the P_trig identically 1 bit-identity requirement, the 1.0 eV regime boundary as an importable constant, and the standing k-sensitivity obligation -- all four used and all four tested. The hand-checkable values reproduce exactly."
    ref-conventions-E:
      status: completed
      completed_actions: [read, cite]
      missing_actions: []
      summary: "eps ~ 0.5 with its +/-10-20% design-dependent band lives inside the untriggered quantity through energy_scale.n_qp_yield and response.calibrate_C. The trigger is applied on top of it on the deposit axis and never in place of it; the P_trig identically 1 test is what would detect the substitution."
    ref-conventions-F:
      status: completed
      completed_actions: [read, cite]
      missing_actions: []
      summary: "Non-paralyzable censoring with tau_d = 40 us is the mechanism that produces the pile-up ceiling the MeV muon deposits compress onto, and it is named as such in the report, both headers and the figure. Its Numerical Factor Registry row -- '40 us (25 kHz Nyquist) | 20 us (50 kHz sampling) conflated' -- is what identified the v1.0 pile-up discrepancy as a timescale conflation rather than a rate error."
    ref-ext-matrices:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "Both 744-column extended matrices loaded via load_design_extended; their columns are asserted to sum to 1 before folding, which is what makes residual_fold a genuine check. Their E_dep_centers_eV is the grid-identity target and their E_rec_median_non_paralyzable_eV is the mapping curve the regime boundary's image and the saturation ceiling are read from."
    ref-ext-deposit-tables:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Both Plan 15-02 tables read through read_em_deposit_table, which parses only the leading numeric tokens so the trailing labels cannot be skipped. Their NaN no-support bins are what the non-finite guard exists for, their broadened_provenance = false is what the double-broaden guard reads, and their validity-floor flags and adequacy labels are what Section 5 of the report applies to decide what the sub-eV reconstructed region supports."
    ref-validity-floors:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Applied in Section 5 of the report to decide which reconstructed bins may be quoted at all, independently of whether the estimator produced a number: all 160 sub-eV muon deposit bins lie below the 4111.82 eV Landau floor, and 70 of 160 Compton bins lie below the 0.73955 eV pair-creation floor."
    ref-applicability:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "em_recoil.assert_nuclear_kernel_use is called AT FOLD TIME, so the branch is not baked in and a later change to the verdict cannot leave a stale one here. The returned dict reports the verdict and the reason it read, and a source-level test asserts the fold-time call is present."
    ref-deposited-spectra-module:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "deposited_spectra.pileup_occupancy used directly with the extended-chain through-wafer rates rather than quoting the v1.0 prose value, which is what surfaced the factor-2 timescale conflation."
  forbidden_proxies:
    fp-nan-to-num:
      status: rejected
      notes: "No executable occurrence anywhere in fold.py. The name appears exactly twice, in the guard message and in the docstring, so the prohibition is discoverable at the point of temptation, and the test excludes only those two forms while scanning every other line. The policy vocabulary has no zero-fill member and a test asserts none exists."
    fp-transplant-nuclear-width:
      status: rejected
      notes: "Not attempted and not attemptable: the guard raises, and it raises because the verdict is READ from em_recoil at fold time rather than because a branch was written to avoid it. All four (channel, design) combinations were tried."
    fp-trigger-replaces-efficiency:
      status: rejected
      notes: "P_trig is applied column-wise on N_dep on the DEPOSIT axis before R acts, and P_trig identically 1 reproduces the untriggered chain BIT-IDENTICALLY (np.array_equal, max difference exactly 0.0) for both channels and both designs -- which is the test that would detect eps having been displaced."
    fp-hardcoded-width:
      status: rejected
      notes: "Every triggered quantity is frozen across k = 1..12 in em_trigger_k_sensitivity.csv with the spread as a RANGE; both table headers, the figure legend and the report carry k and its range; and the question of whether the sub-eV observable is k-dominated is answered by measurement (1.10x, 1.39x) rather than assumed."
    fp-exp-minus-2W:
      status: rejected
      notes: "No np.exp(-2 anywhere in the 15-03 section and no Debye-Waller reference in it. The only occurrences of the string exp(-2W) in the emitted headers are the prohibition itself, and a test asserts every such line carries 'never', 'NOT' or 'prohibition'."
    fp-saturation-as-line:
      status: rejected
      notes: "The feature is named INSTRUMENTAL with the 40 us non-paralyzable mechanism in the report, in both table headers and in the figure annotation, which additionally contains the words 'NOT a physical line'. The test asserts all of that, and separately asserts by measurement that the peak does not track the deposit energy."
    fp-shielded-quantity-leak:
      status: rejected
      notes: "Phase-9 token list imported rather than re-typed and scanned over both reconstructed tables and the k-sensitivity table; zero applied hits. Veto credit is exactly 1.0 by construction and is stated as such in both headers."
  uncertainty_markers:
    weakest_anchors:
      - "The trigger sharpness k is fixed by no project artifact and no measurement of this device exists; only E50 = 0.5 eV carries a decision. Now quantified rather than merely flagged: the sub-eV observable moves by 1.10x (muon) and 1.39x (Compton) over the full declared range."
      - "The muon channel has NO external benchmark on the reconstructed axis at all. The NUCLEUS Table 5 comparison was removed by the 2026-07-22 re-scope and the removal note states the consequence plainly."
      - "eps ~ 0.5 is a project-imposed forward-model definition with a +/-10-20% design-dependent band, not a derived quantity, and it sits underneath every reconstructed number here."
      - "Whatever sub-eV content survives is folded through response-matrix columns that were themselves built two decades below the v1.0 validated range."
    unvalidated_assumptions:
      - "That the sub-eV deposit bins were worth folding at all. Plan 15-01's floors and Plan 15-02's adequacy labels together exclude the muon sub-eV region ENTIRELY and the Compton region below 0.73955 eV, so the fold's job there was to make the exclusion visible rather than to produce a curve, and Section 5 of the report records exactly that."
      - "CHECKED rather than assumed: that the saturation feature's position is stable under the re-grid. It is, at 77.1x and 101.3x compression."
    competing_explanations:
      - "A sub-eV reconstructed rate as genuine leakage of the deposit tail through the response chain, versus the matrix's own sub-eV columns redistributing counts from bins with no support, versus the trigger shoulder shaping noise. The third is now EXCLUDED by measurement -- the k-sensitivity is only 1.10x-1.39x -- while the first two remain entangled and the validity floors exclude the region regardless. The honest position, stated in the report, is that the regime flag, the adequacy label and the k-sensitivity together are what a consumer must read before quoting a sub-eV number."
    disconfirming_observations:
      - "DID NOT FIRE: the counts residual is 2.169e-16, not above 1e-3, so ROADMAP SC2 holds as written."
      - "DID NOT FIRE: the muon reconstructed peak stays at the instrumental ceiling with 77.1x / 101.3x compression and does not track the deposit energy, so the saturation survived the re-grid."
      - "DID NOT FIRE: P_trig identically 1 DOES reproduce the untriggered chain bit-for-bit, so the trigger multiplies eps rather than displacing it."
      - "DID NOT FIRE: the trigger-weighted sub-eV spectrum varies by only 1.10x-1.39x across k in [1, 12], so the sub-eV observable is not dominated by the unmeasured parameter."
      - "FIRED: the recomputed pile-up occupancy is 6.533538e-05, a factor of exactly 2 above the v1.0 quoted ~3e-5, because the v1.0 figure is the 20 us SAMPLING occupancy (3.266768e-05) rather than the 40 us resolving-time occupancy. Reported as a finding with both numbers, their cause and their exact relation asserted in code, rather than reconciled silently. The physical conclusion -- that muon pile-up does not preclude quiescent operation -- is unchanged, since 6.5e-05 is still four decades below the 1e-2 stop threshold."
      - "NOT YET EVALUATED HERE, handed to Plan 15-04: whether the environmental-gamma continuum still overlaps the CEvNS region the way the v1.0 manuscript concluded. The two orientation numbers are stated (10-100 eV E_rec: muon 7.4656 / 7.7231, Compton 34.248 / 35.862 counts/kg/day) so 15-04 does not re-derive them, but the dominance verdict against the Phase-12 CEvNS and Phase-13 neutron numbers is 15-04's deliverable."
---

# Plan 15-03 Summary

## The fold path

`fold.run_em_fold_extended`, appended to `fold.py`, with **five guards that all
raise and are all exercised by tests that try them**: 744-column shape, Plan 15-01
applicability (verdict read from `em_recoil` **at fold time**), double broadening
(undeclared raises too), non-finite input (`NonFiniteDepositError` unless an
explicit recorded policy is passed), and a direct grid-identity assertion that
replaces the neutron path's floor-coverage check because these channels are already
on the deposit axis.

`residual_fold` ≤ **2.169e-16** against ROADMAP SC2's 1e-3. The two leakage
residuals are both 0.0 and **coincide by construction** — no broadening is applied
— and the budget says so with an explicit flag rather than presenting them as two
confirmations.

**`np.nan_to_num` appears in no executable line.** `NO_SUPPORT_POLICIES` has no
zero-fill member.

## Trigger

`P_trig ≡ 1` reproduces the un-triggered spectrum **bit-identically** (max
difference exactly 0.0, `np.array_equal` True) for both channels and both designs.
§I hand values exact; `P(E50) = 1/2` at k = 1, 4 and 12. The regime boundary is
imported and its reconstructed image (**0.497240 / 0.495855 eV**) is read off the
matrix's own median mapping curve, asserted not to be `0.5 ×` anything.

## Saturation — survives, and is instrumental

Deposit peaks at **1.4354 MeV**; reconstructed peak at **18.8365 keV** (Ta→Al) and
**14.9624 keV** (Al→Hf) — compressions of **77.1×** and **101.3×** onto the ceiling
set by the 40 µs non-paralyzable resolving time. Named instrumental with its
mechanism in the report, both headers and the figure.

## k-sensitivity — the question is answered, not assumed

Sub-eV triggered rate varies by only **1.10×** (muon) and **1.39×** (Compton) over
k ∈ [1, 12]. **The sub-eV observable is not dominated by the unmeasured parameter.**

## The finding that fired

**Recomputed pile-up occupancy = 6.533538e-05, a factor of exactly 2 above the v1.0
quoted ~3e-5.** The v1.0 figure is the **20 µs sampling** occupancy
(3.266768e-05), not the **40 µs resolving-time** occupancy — precisely the
conflation `CONVENTIONS` §F's Numerical Factor Registry names by row. Both numbers
and their exact 2:1 relation are asserted in code so the distinction cannot be lost
again. The physical conclusion is unchanged: 6.5e-05 is four decades below the
1e-2 stop threshold.

## Deviations

None. No deviation rule was applied.
