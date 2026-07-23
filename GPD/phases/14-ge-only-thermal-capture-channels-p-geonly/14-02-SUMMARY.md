---
phase: 14-ge-only-thermal-capture-channels-p-geonly
plan: 02
title: "71Ge EC lines with P_K derived from K-vacancy conservation rather than recalled, the M line folded through the extended response chain with no IA broadening and its reconstructed image MEASURED at 65.0/63.0 eV entirely inside the RoI, and Phase 14 closed with five adjudicated success criteria"
date: 2026-07-23
status: complete
depth: full
completed: 2026-07-23
provides:
  - "src/qpd_potential/capture_channel.py (14-02 section, APPENDED) — the frozen-retrieval readers for the 71Ge ground state and its X-ray/Auger line lists, the K-vacancy-conservation derivation of P_K, the Ga-edge line-energy check, the activation law, the electron-recoil IA criterion evaluated at this line, the monochromatic-line fold with its five raising guards, the shared-reconstructed-axis comparison and the bounds figure"
  - "artifacts/v2.0/ge71_ec_lines.csv — the M/L/K inventory with the Ga-edge check, the four activation scenarios, per-line rates at each with SOURCED/BOUNDED status, the coincident neutrino recoil and the IA criterion"
  - "artifacts/v2.0/ge71_ec_dRdErec_TaAl.csv and ge71_ec_dRdErec_AlHf.csv — the M line's reconstructed image on the 161-bin axis, untriggered and trigger-weighted, with headers carrying the counts budget, the deposit-vs-reconstructed measurement and the no-IA statement with its number"
  - "artifacts/v2.0/capture_channel_bounds.pdf — both designs on the SHARED reconstructed axis against the Phase-12 CEvNS and Phase-13 neutron spectra, RoI shaded, sub-eV boundary drawn, deposit-vs-reconstructed annotated, accuracy_label in a box ON the figure (written uncompressed so the audit can read it out of the file)"
  - "data/ge71_ec/{livechart_71ge_*.csv, xraylib_edges.dat, MANIFEST.md} — the integrity-checked 71Ge decay-scheme and Ga binding-energy retrievals"
  - "GPD/phases/14-.../14-02-EC-AND-CLOSEOUT.md — the phase closeout: inventory, activation, branching, the no-IA argument with its number, the measured placement and the SC3 adjudication, the shared-axis comparisons, five SC verdicts, the phi_th statement, the twelve-row un-netted directional-bias table, the declared omissions and the Phase-16 hand-off"
  - "tests/test_ge71_ec.py — 16 tests covering all thirteen contract acceptance tests"
  - "artifacts/v2.0/legacy_grid_disposition.csv — three more disposition rows (71 total)"
one_liner: "The 71Ge EC M line lands ENTIRELY inside the reconstructed RoI — in-RoI fraction 1.000000 for both designs — but at E_rec 65.049 eV (Ta->Al) and 62.964 eV (Al->Hf), not at its 158.7 eV deposit energy, because the measured mapping slope at this energy is 0.4099 / 0.3967 and NOT the ~0.5 the 1 eV image would have suggested (0.5056 / 0.5032, consistent with Phase 13's median-based 0.497240 / 0.495855), so ROADMAP SC3's 'landing inside the RoI' clause is CONFIRMED BY MEASUREMENT and would have been REFUTED had the slope exceeded ~0.63, which nothing in the criterion's own text reveals; P_K = 0.8759 +/- 0.0043 is DERIVED from K-vacancy conservation on an integrity-checked IAEA Live Chart retrieval — every K hole is filled by a Ga K X-ray (45.284/100) or a K Auger electron (42.306/100), the two channels being exhaustive and mutually exclusive — which makes the M and L bounds 1 - P_K = 0.1241 rather than the trivial 1 and is 8.06x tighter, so the bound is not vacuous; the M-line bound is 130.82 counts/kg/day at SATURATION, 1.794x (Ta->Al) and 1.789x (Al->Hf) the Phase-12 CEvNS rate INSIDE the RoI on the shared reconstructed axis and 1.102x the CEvNS total, but only 7.70 at t = 1 d, which is why fp-saturation-unstated is a real proxy and not a formality; A_sat = 1054.1472 counts/kg/day is the Plan 14-01 70Ge row and carrying its 0.2057 abundance factor was a LIVE BUG caught by cross-checking — the bare-cross-section fold gave 5124.68, the rate for an isotopically pure 70Ge wafer, 4.86x too large; the Ga-shell identification is CHECKED rather than marked UNVERIFIED against a separately retrieved edge table, with M/L/K matching the Ga M1(3s)/L1(2s)/K(1s) binding energies to +0.38%/+0.062%/+0.012% and the M line inside its own stated +/-1.4 eV; the no-IA-broadening exclusion is argued with a number and the number comes out the OTHER WAY — 2W_e = 250.02 at 158.7 eV SATISFIES the electron-side validity condition that Phase 15 measured failing at 0.1574 on the grid floor, so inheriting Phase 15's sentence would have been wrong here and the exclusion instead rests on the frozen kernel carrying the NUCLEAR omega_bar (transplant understates by 5.9616x) and on an atomic relaxation energy not being a recoil at all, with the stake measured at sigma_e = 10.0366 eV = 0.518 reconstructed bins rather than dismissed as small; the response image is intrinsically NARROWER than one bin (rel_spread 0.93% vs an 11.5% bin) so its apparent width is the binning, the counts budget closes exactly with the two residuals coinciding by construction and that coincidence STATED rather than counted twice, P_trig == 1 reproduces the untriggered spectrum bit-identically and the k-sensitivity over [1,12] is 0.31%; and all five ROADMAP criteria carry verdicts — SC1 CONFIRMED (EGAF retrieved against expectation), SC2 PARTIALLY CONFIRMED because both of the criterion's own illustrative numbers are superseded on Ge (473 eV -> 754.11 eV, and 'tens of eV' against EGAF-sourced cascade means of 149.5-186.5 eV at observed multiplicities 1.66-4.25), SC3 CONFIRMED by measurement, SC4 CONFIRMED on branch (a) with Phi_th = 2.767075e-3 named as PHASE 9's product and 3.95x ABOVE Biffl's requirement, SC5 CONFIRMED — with no window narrowed, no threshold lowered and the RoI not moved."
plan_contract_ref: GPD/phases/14-ge-only-thermal-capture-channels-p-geonly/14-02-PLAN.md#/contract

contract_results:
  claims:
    claim-ec-inventory:
      status: passed
      summary: "The M/L/K inventory is written at 158.7 +/- 1.4 / 1298.5 / 10368.3 eV DEPOSITED with the ROADMAP CONUS+ anchor named, and the physical identification is CHECKED rather than marked UNVERIFIED: an EC line energy is the binding energy of the captured shell in the DAUGHTER, and allowed EC captures s-electrons, so K/L/M are Ga(Z=31) K(1s)/L1(2s)/M1(3s). Against a separately retrieved, integrity-checked edge table the differences are +0.60 eV (+0.3795%, inside the stated +/-1.4), +0.80 eV (+0.0616%) and +1.20 eV (+0.0116%). A_sat = 1054.1472 counts/kg/day from the Plan 14-01 70Ge row over the FULL incident band, with the 0.2057 abundance factor (a first implementation omitted it and returned 5124.68, the pure-70Ge rate, 4.86x too large; caught by cross-check). A(t) is tabulated at 1 d / 11.43 d / 30 d / saturation and EVERY rate row carries its scenario. P_K = 0.8759 +/- 0.0043 is SOURCED-DERIVED by K-vacancy conservation; P_L and P_M are BOUNDED by 1 - P_K = 0.1241, 8.06x tighter than the trivial bound, with the L/M split left undetermined. T_nu = Q_EC^2/(2Mc^2) = 0.408569 eV = 0.2574% of the M line = 0.0211 reconstructed bins."
      linked_ids: [deliv-ec-lines, deliv-ec-report, deliv-ec-tests, test-ec-energies, test-activation-law, test-branching-sourced-or-bounded, test-nu-recoil-named, ref-roadmap-14-sc3, ref-conventions-IJ, fp-saturation-unstated, fp-assert-branching]
      evidence:
        - verifier: gpd-executor
          method: "a branching fraction DERIVED from a conservation law on integrity-checked data rather than recalled, and a line-energy identification checked against an independently retrieved table rather than asserted"
          confidence: high
          claim_id: claim-ec-inventory
          deliverable_id: deliv-ec-lines
          acceptance_test_id: test-branching-sourced-or-bounded
          reference_id: ref-roadmap-14-sc3
          forbidden_proxy_id: fp-assert-branching
          evidence_path: artifacts/v2.0/ge71_ec_lines.csv
    claim-ec-fold:
      status: passed
      summary: "The M line is folded as a monochromatic deposit through the Phase-10 744-column extended chain for both designs with NO IA broadening, and the exclusion is argued on the Phase-15 criterion EVALUATED WITH A NUMBER FOR THIS LINE — where it comes out the other way: 2W_e = 250.02 SATISFIES the electron-side validity condition that Phase 15 measured failing at 0.1574 on the 0.1 eV grid floor, so inheriting the sentence would have been wrong. The exclusion rests instead on the frozen kernel carrying the NUCLEAR omega_bar (transplant understates by 5.9616x) and on the deposit being an atomic relaxation energy rather than a recoil; the stake is measured at sigma_e = 10.0366 eV = 0.518 reconstructed bins. MEASURED PLACEMENT: matrix unbinned E_rec mean 65.049 eV (Ta->Al) / 62.964 eV (Al->Hf), mapping slope 0.4099 / 0.3967, in-RoI fraction 1.000000 for both, sub-eV fraction 0. The image is narrower than one bin (rel_spread 0.93% vs 11.52%), so its apparent width is the binning. Counts close exactly with the two residuals coinciding BY CONSTRUCTION and stated as such. P_trig == 1 reproduces the untriggered spectrum bit-identically; k-sensitivity 0.31%. All comparisons are on the shared reconstructed axis, computed from committed artifacts whose headline numbers the band integrator reproduces."
      linked_ids: [deliv-ec-erec-TaAl, deliv-ec-erec-AlHf, deliv-ec-figure, deliv-ec-report, deliv-ec-tests, test-no-ia-on-electron-recoil, test-line-placement-measured, test-counts-budget-ec, test-trigger-composition-ec, test-shared-axis-comparison, ref-phase15-ia, ref-phase12-cevns, ref-phase13-neutron, fp-deposit-as-reconstructed, fp-ia-on-electron-recoil]
      evidence:
        - verifier: gpd-executor
          method: "the placement is measured from the response matrix's own unbinned statistics rather than inferred from the deposit energy, and the band integrator is validated by reproducing the committed CEvNS and neutron headline numbers before being used"
          confidence: high
          claim_id: claim-ec-fold
          deliverable_id: deliv-ec-erec-TaAl
          acceptance_test_id: test-line-placement-measured
          reference_id: ref-phase15-ia
          forbidden_proxy_id: fp-deposit-as-reconstructed
          evidence_path: artifacts/v2.0/ge71_ec_dRdErec_TaAl.csv
    claim-phase-closeout:
      status: passed
      summary: "All five ROADMAP Phase-14 criteria carry a verdict with its evidence located: SC1 CONFIRMED (ENDF MT=102 frozen from the already-committed set; EGAF retrieved and integrity-checked against planning's expectation of failure), SC2 PARTIALLY CONFIRMED, SC3 CONFIRMED by measurement, SC4 CONFIRMED on branch (a), SC5 CONFIRMED. SC2 is PARTIAL for a measured reason, not a shortfall: the shape of the answer is delivered exactly as required, but BOTH of the criterion's own illustrative numbers are superseded on Ge — '473 eV at 8 MeV' against a 754.11 eV 73Ge ceiling, and 'tens of eV for a realistic multi-gamma cascade' against EGAF-sourced isotropic means of 149.5-186.5 eV on observed multiplicities of 1.66-4.25. Phi_th = 2.767075e-3 cm^-2 s^-1 (0.01-0.5 eV, cadmium cutoff) is named as PHASE 9's product, SC4 discharges on branch (a), the Biffl ratio 3.95 is reported ABOVE the requirement, and nothing derived in the phase is reported as zero. The twelve-row un-netted directional-bias table, the declared omissions and the Phase-16 hand-off are written, and CALC-23's stale wording plus the ROADMAP checkboxes are flagged for the orchestrator rather than edited."
      linked_ids: [deliv-ec-report, deliv-disposition-rows-02, deliv-ec-tests, test-sc-verdicts-14, test-phi-th-disposition, test-label-and-shielded-audit, test-disposition-rows-02, ref-phase9-decl, ref-roadmap-14-sc3, fp-precision-inflation-02, fp-capture-channel-as-zero-02]
      evidence:
        - verifier: gpd-executor
          method: "each criterion adjudicated against a measured number rather than against its own wording, with two of the criterion's illustrative figures found to be superseded and reported rather than reconciled"
          confidence: high
          claim_id: claim-phase-closeout
          deliverable_id: deliv-ec-report
          acceptance_test_id: test-sc-verdicts-14
          reference_id: ref-phase9-decl
          forbidden_proxy_id: fp-capture-channel-as-zero-02
          evidence_path: GPD/phases/14-ge-only-thermal-capture-channels-p-geonly/14-02-EC-AND-CLOSEOUT.md
  deliverables:
    deliv-ec-lines:
      status: passed
      path: artifacts/v2.0/ge71_ec_lines.csv
      description: "20 rows: three LINE_ENERGY rows with the Ga-edge comparison and CHECKED status, four ACTIVITY rows, twelve LINE_RATE rows (three shells x four scenarios) each with SOURCED or BOUNDED status and its scenario label, the NU_RECOIL row and the IA_CRITERION row. accuracy_label on every row. Header carries the axis tag, the Ga identification with its check, the activation law with the abundance-factor warning, the K-vacancy derivation of P_K, the neutrino recoil as a bin fraction and the no-IA argument with all its numbers."
      linked_ids: [claim-ec-inventory, test-ec-energies, test-activation-law, test-branching-sourced-or-bounded, test-nu-recoil-named]
    deliv-ec-erec-TaAl:
      status: passed
      path: artifacts/v2.0/ge71_ec_dRdErec_TaAl.csv
      description: "160 rows on the 161-bin reconstructed axis (bin 0, the [0, 1e-3 eV) underflow catch-bin, dropped exactly as the Phase-12/13 writers do). Columns E_rec_keV, dRdErec_bound, dRdErec_trigger_weighted, P_trig_effective, regime, accuracy_label. Header carries the deposit-vs-reconstructed measurement (matrix mean, median, p16/p84, rel_spread, mapping slope, populated-bin count, bin width, in-RoI and sub-eV fractions), the counts budget with both residuals and the statement that they coincide by construction, the no-IA argument with its number, and the trigger composition."
      linked_ids: [claim-ec-fold, test-line-placement-measured, test-counts-budget-ec, test-no-ia-on-electron-recoil]
    deliv-ec-erec-AlHf:
      status: passed
      path: artifacts/v2.0/ge71_ec_dRdErec_AlHf.csv
      description: "The same chain, same columns and same label for Al->Hf. Total reconstructed counts are identical to Ta->Al because R's columns each sum to 1 — the design moves counts, it does not create them. The image occupies two reconstructed bins here against one for Ta->Al, at a lower mapping slope."
      linked_ids: [claim-ec-fold, test-line-placement-measured, test-counts-budget-ec]
    deliv-ec-figure:
      status: passed
      path: artifacts/v2.0/capture_channel_bounds.pdf
      description: "Two panels, one per design, all three channels on the SHARED reconstructed axis, log-log, RoI shaded, each design's own sub-eV regime boundary drawn and labelled as the E_rec image of a 1 eV deposit, accuracy_label and the BOUND/scenario/no-IA statement in a box, and a red annotation box on each panel giving the measured DEPOSIT->RECONSTRUCTED mapping and stating that 158.7 eV is not a position on this axis. Written with pdf.compression = 0 so the label audit reads the text out of the file rather than settling for 'the figure exists'. The connector arrow was removed deliberately: a long diagonal across a log-log spectrum panel reads as a curve, which is the misreading the annotation exists to stop."
      linked_ids: [claim-ec-fold, test-line-placement-measured, test-label-and-shielded-audit]
    deliv-ec-report:
      status: passed
      path: GPD/phases/14-ge-only-thermal-capture-channels-p-geonly/14-02-EC-AND-CLOSEOUT.md
      description: "Nine sections: the inventory with the Ga check and the activation scenario, the branching disposition with its derivation, the no-IA argument restated with its number and its reversal, the measured line placement and the SC3 adjudication, the counts budget and trigger composition, the shared-axis comparison, the five SC verdicts with SC2's PARTIAL reasoned, the twelve-row un-netted directional-bias table, the phi_th statement with the Biffl direction, the Phase-16 hand-off with three items flagged for the orchestrator, the audit table and the recorded closeout checkpoint."
      linked_ids: [claim-ec-inventory, claim-ec-fold, claim-phase-closeout]
    deliv-ec-tests:
      status: passed
      path: tests/test_ge71_ec.py
      description: "16 tests, all passing, tolerances declared as module constants before any check runs: HALF_LIFE_LIMIT_TOL 1e-9, TRIGGER_E50_TOL 1e-12, COUNTS_CLOSURE_TOL 1e-3, FOLD_RESIDUAL_TOL 1e-12, GA_EDGE_REL_TOL 0.01, NU_RECOIL_MAX_BIN_FRACTION 1.0, EREC_BIN_WIDTH_FRACTION 0.12202. Reuses the Phase-9 shielded-token machinery by import. The no-IA scan is an AST scan of the parsed module, so a mention in a docstring cannot be mistaken for a use and a use cannot hide in prose."
      linked_ids: [claim-ec-inventory, claim-ec-fold, claim-phase-closeout]
    deliv-disposition-rows-02:
      status: passed
      path: artifacts/v2.0/legacy_grid_disposition.csv
      description: "Three rows added: ge71_ec_lines.csv as not_a_spectrum with a reason recording that its line energies are DEPOSITED and not reconstructed-axis positions, and the two ge71_ec_dRdErec_*.csv as bounded_native_axis on the RECONSTRUCTED axis with floor 1.059254e-06 keV. 71 rows total; the register's own enumeration test passes with no unregistered artifact across both plans."
      linked_ids: [claim-phase-closeout, test-disposition-rows-02]
  acceptance_tests:
    test-ec-energies:
      status: passed
      summary: "All three energies recorded with the ROADMAP anchor named, and the Ga-binding identification CHECKED rather than marked UNVERIFIED: M 158.7 vs Ga M1 158.1 (+0.3795%, inside the stated +/-1.4 eV), L 1298.5 vs Ga L1 1297.7 (+0.0616%), K 10368.3 vs Ga K 10367.1 (+0.0116%). The shell mapping K/L1/M1 is asserted in code, since allowed EC captures s-electrons. The Ga table's SHA-256 is asserted present in the artifact. Provenance honesty recorded: the edge table is xraylib's own compilation, retrieved and integrity-checked as a file, so this establishes consistency with a standard compilation rather than with a primary measurement."
      linked_ids: [claim-ec-inventory, deliv-ec-lines, deliv-ec-tests]
    test-activation-law:
      status: passed
      summary: "A(0) = 0 exactly, A(inf) = A_sat exactly, A(11.43 d) = 0.5 A_sat to 1e-9 A_sat, A(1 d)/A_sat = 5.88%. Every rate row in the artifact is asserted to carry a scenario label that is neither empty nor 'n/a', and all four declared scenarios are asserted present. A single rate quoted without its t would fail."
      linked_ids: [claim-ec-inventory, deliv-ec-lines, deliv-ec-tests]
    test-branching-sourced-or-bounded:
      status: passed
      summary: "P_K carries status SOURCED with a retrieval record; P_L and P_M carry BOUNDED. P_K is asserted to equal (I_Kx + I_KAuger)/100 rather than being trusted, and BOTH component decompositions are asserted to close first (Kbeta'1 + Kbeta'2 = Kbeta; KLL + KLX + KXY = K-Auger), so a leaves-plus-totals double count would fail. The bound is asserted to be more than 2x tighter than the trivial one. Every retrieval's SHA-256 is asserted present in data/ge71_ec/MANIFEST.md alongside a curl command."
      linked_ids: [claim-ec-inventory, deliv-ec-lines, deliv-ec-report, deliv-ec-tests]
    test-nu-recoil-named:
      status: passed
      summary: "T_nu = 0.408569 eV, re-derived inside the test to 1e-12 relative from the SOURCED Q_EC, asserted genuinely sub-eV, and expressed as 0.0211 of one 12.202% reconstructed bin. Asserted present in both the artifact and the report. Omitting the companion, or asserting negligibility without the fraction, would fail."
      linked_ids: [claim-ec-inventory, deliv-ec-lines, deliv-ec-report, deliv-ec-tests]
    test-no-ia-on-electron-recoil:
      status: passed
      summary: "The criterion is evaluated WITH A NUMBER for this line and Phase 15's own numbers are reproduced first so the comparison is real: omega_bar_e = 0.634740 eV, 35.540x the nuclear scale, 2W_e at the 0.1 eV grid floor = 0.1574. At 158.7 eV 2W_e = 250.02 and the condition is SATISFIED — reported as a finding, not absorbed. broaden=True RAISES on this path rather than defaulting to off. An AST scan of the parsed module asserts ia_broadening, gaussian_broaden and native_edges are neither imported nor called, and np.nan_to_num is absent. Excluding IA on grounds of smallness would fail: the electron-side width is 0.518 reconstructed bins."
      linked_ids: [claim-ec-fold, deliv-ec-erec-TaAl, deliv-ec-erec-AlHf, deliv-ec-tests, ref-phase15-ia]
    test-line-placement-measured:
      status: passed
      summary: "Peak, mapping slope and in-RoI fraction reported as measured numbers for both designs: E_rec mean 65.049 / 62.964 eV, slope 0.4099 / 0.3967, in-RoI fraction 1.000000 / 1.000000. The test asserts the reconstructed image is below 0.6x the deposit energy, that the slope lies in (0.3, 0.6), that the image is inside the reconstructed RoI AND that the deposit energy is outside it — which is precisely what makes the ROADMAP clause a cross-axis assertion. SC3 is adjudicated CONFIRMED in the report with the measured numbers behind it."
      linked_ids: [claim-ec-fold, deliv-ec-erec-TaAl, deliv-ec-erec-AlHf, deliv-ec-figure, deliv-ec-report, deliv-ec-tests]
    test-counts-budget-ec:
      status: passed
      summary: "residual_retained_plus_leaked = 0 against the 1e-3 pass condition; residual_fold = 0 against 1e-12, which is exact because R's columns each sum to 1; reconstructed counts equal input counts to 1e-12 relative. The two residuals COINCIDE BY CONSTRUCTION here because no broadening is applied and the monochromatic input lies strictly inside the deposit axis, and both artifact headers are asserted to carry that phrase — so the coincidence is stated rather than presented as two independent confirmations. Nothing is rescaled."
      linked_ids: [claim-ec-fold, deliv-ec-erec-TaAl, deliv-ec-erec-AlHf, deliv-ec-tests, ref-phase13-neutron]
    test-trigger-composition-ec:
      status: passed
      summary: "P_trig == 1 reproduces the untriggered spectrum BIT-IDENTICALLY under np.array_equal on both N_rec_trigger and dRdErec_trigger, for both designs. P(0.5 eV) = 1/2 to 1e-12 on the deposit axis. P_trig at the line's deposit bin = 0.999999999907, essentially 1 as expected 2.5 decades above E50 — no finding about the curve. k-sensitivity over the declared [1, 12] range on the in-RoI rate: 0.31%, reported in the closeout."
      linked_ids: [claim-ec-fold, deliv-ec-erec-TaAl, deliv-ec-erec-AlHf, deliv-ec-tests, ref-conventions-IJ]
    test-shared-axis-comparison:
      status: passed
      summary: "Every comparison is computed from the committed reconstructed-axis artifacts and the axis tag travels with each operand; the test asserts both operands of every comparison carry axis == RECONSTRUCTED. The band integrator is VALIDATED before use by reproducing the committed headline numbers: CEvNS total 118.7286 / 118.7292 against the quoted 118.73, neutron in-RoI 5430.2866 / 5485.1515 against 5430.287 / 5485.152 to 1e-5. Results: the M-line bound is 1.794x / 1.789x the CEvNS in-RoI rate and 0.0241 / 0.0239 of the neutron elastic in-RoI rate."
      linked_ids: [claim-ec-fold, deliv-ec-report, deliv-ec-figure, deliv-ec-tests, ref-phase12-cevns, ref-phase13-neutron]
    test-sc-verdicts-14:
      status: passed
      summary: "All five criteria present with a verdict in the Phase-12/13 vocabulary and an evidence path named for each. SC1 CONFIRMED, SC2 PARTIALLY CONFIRMED, SC3 CONFIRMED, SC4 CONFIRMED on branch (a), SC5 CONFIRMED. SC2's 'bounded, not quantified' shape is honoured and the PARTIAL is reasoned from two measured supersessions of the criterion's own illustrative figures rather than from a shortfall in the deliverable. No window was narrowed, no threshold lowered and the RoI was not moved."
      linked_ids: [claim-phase-closeout, deliv-ec-report, deliv-ec-tests]
    test-phi-th-disposition:
      status: passed
      summary: "Phi_th = 2.767075e-3 cm^-2 s^-1 named with its cadmium-cutoff convention and attributed to PHASE 9, SC4 recorded as discharged on branch (a), the Biffl ratio 3.95 reported with direction ABOVE, and the string 'Phase 13's product' asserted absent. Nothing derived is zero: every capture band rate, the total, the 71Ge production rate and the M-line bound are asserted strictly positive. The one exact zero in the phase — the thermal and epithermal INELASTIC rate — is a thresholded-reaction zero and is explained as such in the closeout."
      linked_ids: [claim-phase-closeout, deliv-ec-report, deliv-ec-tests, ref-phase9-decl]
    test-label-and-shielded-audit:
      status: passed
      summary: "accuracy_label = order_of_magnitude present in all six data artifacts, both reports, and ON the figure — read out of the PDF's own text stream by rejoining the TJ kerning arrays (matplotlib splits the token as 'or' + 'der_of_magnitude', so a naive byte search would have passed vacuously or failed spuriously), with the figure written uncompressed to make that read possible. Zero APPLIED shielded-token hits over the module, both reports and all artifacts, with one narrow named exemption recorded: SHIELDED_TOKENS_EXTRA's 'residual' means a residual dose rate AFTER shielding in Plan 09-03, while here it is a counts-CONSERVATION residual; 'dru' and 'Table 5' carry no such collision and remain live. Zero phi_lo uses. Veto credit exactly 1.0 by construction, not imported."
      linked_ids: [claim-phase-closeout, deliv-ec-report, deliv-ec-figure, deliv-ec-tests]
    test-disposition-rows-02:
      status: passed
      summary: "All nine new tracked .csv files of the phase carry disposition rows with a non-empty disposition from the closed vocabulary and a reason longer than 40 characters. The register's own git ls-files enumeration is re-run inside the test and asserted to leave no unregistered artifact. 71 rows total."
      linked_ids: [deliv-disposition-rows-02, deliv-ec-tests]
  references:
    ref-roadmap-14-sc3:
      status: completed
      completed_actions: [read, compare, use]
      summary: "SC3's three line energies are used as the inventory's source and named as such. Its clause 'with the M-shell line landing inside the RoI' is treated as a TESTABLE cross-axis assertion and adjudicated by measurement: false on the deposit axis, CONFIRMED on the reconstructed axis at in-RoI fraction 1.000000, with the reason (mapping slope ~0.40) supplied by this plan rather than by the criterion. SC1, SC2, SC4 and SC5 are carried here for the closeout verdicts, and SC2's two illustrative figures are reported as superseded rather than reconciled."
      linked_ids: [claim-ec-inventory, claim-phase-closeout]
    ref-phase15-ia:
      status: completed
      completed_actions: [read, use, cite]
      summary: "Both of Phase 15's numbers are REPRODUCED here before being used, so the comparison is real rather than a citation: omega_bar_e >= 0.634740 eV = 35.540x the nuclear scale, and 2W_e = 0.1574 at the 0.1 eV extended-grid floor. Evaluated at 158.7 eV the same criterion gives 250.02 and is SATISFIED, so Phase 15's verdict does NOT transfer to this line and the exclusion is re-argued on the kernel's identity and on the deposit not being a recoil. Phase 15's finding that the smallness shortcut would be false is honoured: the electron-side width is measured at 0.518 reconstructed bins rather than dismissed."
      linked_ids: [claim-ec-fold]
    ref-conventions-IJ:
      status: completed
      completed_actions: [read, use, avoid]
      summary: "Section I: P_trig is composed on the DEPOSIT centres before R acts, MULTIPLYING eps rather than replacing it, with E50 = 0.5 eV exactly (asserted to 1e-12) and the k in [1, 12] sensitivity obligation discharged at 0.31% on the in-RoI rate. Section J: the rate is never multiplied by exp(-2W); an AST scan asserts the nuclear kernel is neither imported nor called on this path, and broaden=True raises."
      linked_ids: [claim-ec-inventory, claim-ec-fold]
    ref-phase12-cevns:
      status: completed
      completed_actions: [read, compare]
      summary: "artifacts/v2.0/cevns_dRdErec_ext_{TaAl,AlHf}.csv read directly and re-integrated rather than quoted: the band integrator reproduces the 118.73 total to 118.7286 / 118.7292, which validates it before the in-RoI comparison is made. In-RoI CEvNS 72.92 / 73.14 counts/kg/day, against which the M-line bound at saturation is 1.794x / 1.789x."
      linked_ids: [claim-ec-fold]
    ref-phase13-neutron:
      status: completed
      completed_actions: [read, compare, use]
      summary: "The counts-budget pattern with retained-only and retained+leaked kept separate is followed, and the fact that they coincide here is stated rather than counted twice. The E_rec image of a 1 eV deposit is recomputed on the same chain (0.5056 / 0.5032 mean, against Phase 13's median-based 0.497240 / 0.495855 sub-eV boundaries — the same curve, a different statistic) and used to show that the mapping slope is NOT constant: it falls to 0.4099 / 0.3967 by 158.7 eV. The neutron in-RoI 5430.287 / 5485.152 is reproduced from the committed artifact to 1e-5 and used as the comparison denominator. Phase 13's self-caught cross-axis error is the reason every comparison here carries an asserted axis tag."
      linked_ids: [claim-ec-fold, claim-phase-closeout]
    ref-phase9-decl:
      status: completed
      completed_actions: [read, use, cite]
      summary: "Section 5's Phi_th = 2.767075e-3 cm^-2 s^-1 (0.01-0.5 eV, cadmium cutoff) is named as PHASE 9's product in the closeout and SC4 is recorded as discharged on branch (a); attributing it to Phase 13 is asserted absent in test. Section 7's un-netted directional-bias row schema is used for the twelve-row phase table. Section 3.4's reasoning is why every rate here carries order_of_magnitude."
      linked_ids: [claim-phase-closeout]
  forbidden_proxies:
    fp-deposit-as-reconstructed:
      status: rejected
      notes: "The reconstructed placement is MEASURED from the response matrix's own unbinned statistics: 65.049 eV (Ta->Al) and 62.964 eV (Al->Hf) against a 158.7 eV deposit, mapping slope 0.4099 / 0.3967. The artifact headers, the report and the figure all carry the axis distinction explicitly, and the figure's annotation states that 158.7 eV is not a position on that axis. The test asserts the image is below 0.6x the deposit energy and that the deposit energy lies OUTSIDE the reconstructed RoI while the image lies inside — the two facts that make the ROADMAP clause a cross-axis assertion."
    fp-ia-on-electron-recoil:
      status: rejected
      notes: "broaden=True RAISES on this path. An AST scan of the parsed module asserts ia_broadening, gaussian_broaden and native_edges are neither imported nor called. The exclusion is argued on the criterion evaluated with a number — and reported when that number came out the OTHER way at this energy — and on the kernel's nuclear identity, NOT on smallness: the electron-side width would be 0.518 reconstructed bins, which is measured and reported rather than dismissed."
    fp-saturation-unstated:
      status: rejected
      notes: "Every rate row in the artifact carries a scenario label, asserted in test to be neither empty nor 'n/a', and all four scenarios are present. The closeout quotes the M-line bound at saturation (130.82) and at t = 1 d (7.70) side by side and states that the scenario is the difference between the channel dominating the CEvNS in-RoI rate at 1.79x and sitting at ~11% of it."
    fp-assert-branching:
      status: rejected
      notes: "No branching fraction is written from recollection. P_K is DERIVED from K-vacancy conservation on an integrity-checked retrieval, with both component decompositions checked to close before use and the derivation re-verified arithmetically in test. P_L and P_M are BOUNDED by 1 - P_K, and the L/M split is explicitly left undetermined. Every retrieval's SHA-256 is asserted present in the manifest. WebFetch was not used."
    fp-precision-inflation-02:
      status: rejected
      notes: "accuracy_label = order_of_magnitude on all six data artifacts, in both reports and ON the figure, read out of the PDF text stream. Both reports open by stating the channel is delivered as a BOUND, not a quantification. The M and L line rates are labelled BOUNDED on every row, and the closeout says plainly which part of the bound carries little information (the L/M split) rather than presenting the whole as a result."
    fp-capture-channel-as-zero-02:
      status: rejected
      notes: "Phase 16 receives six numbered bounds with their scenarios and caveats attached, not a blank. Every derived capture and EC quantity is asserted strictly positive in test. The single exact zero in the phase — the thermal and epithermal inelastic rate — is identified as a thresholded-reaction zero (no discrete level is open below ~600 keV) and is distinguished in the closeout from a manufactured omission."
  uncertainty_markers:
    weakest_anchors:
      - "The L/M capture-shell split. P_K is derived rigorously, but nothing in the retrieved data separates P_L from P_M, so both carry the same 1 - P_K = 0.1241 bound and only the M line is inside the RoI. The M-line number is therefore the one carrying all of the remaining looseness, and how much is unknown."
      - "The exposure history. Saturation is a genuine upper bound for any history, but it is 17x the one-day value, and the difference decides whether this channel dominates the CEvNS in-RoI rate (1.79x) or sits well below it. The project does not own the scenario."
      - "The 71Ge production rate inherited from Plan 14-01, which inherits the Phase-9 flux whose eV-keV differential shape Phase 13 demonstrated to be UNBOUNDED."
      - "The response matrix's own mapping slope and its ~11.5%-per-bin resolution near 65 eV. These set where the line lands and how wide its image is, and they are Phase-10 properties, not properties of this channel. The image is narrower than one bin, so the reported width is the binning."
      - "The Ga edge table's own provenance. It is retrieved and integrity-checked as a FILE, but it is xraylib's compilation and the underlying tabulation is not traced further, so the line-energy check establishes consistency with a standard compilation rather than with a primary measurement."
    unvalidated_assumptions:
      - "Full containment of the atomic relaxation energy. Sound for the M line, whose Auger products have sub-micron ranges. The K-line X-ray escape near a surface is a DECLARED, unmodelled omission with its direction labelled flatters_SB."
      - "That the line is monochromatic before the response chain. Checked as a fraction rather than assumed: the coincident neutrino recoil is 0.0211 of one reconstructed bin, and any intrinsic atomic width is far narrower still."
      - "That no impulse-approximation broadening applies. The criterion that Phase 15 used FAILS to justify this at 158.7 eV; the exclusion rests instead on the kernel's identity and on the deposit not being a recoil, which is a physical argument rather than a measured one. The stake if it is wrong is 0.518 reconstructed bins."
      - "That the EGAF-sourced cascade means used to grade SC2 are representative, given the 60-71% completeness measured in Plan 14-01."
    competing_explanations:
      - "A large in-RoI fraction could reflect genuine physics or a fold error, a wrong response matrix, or a cross-axis conflation. Separated by reporting the matrix's own unbinned statistics beside the binned result, by the counts budget, by asserting in test that both operands of every comparison carry the same axis tag, and by validating the band integrator against the committed CEvNS and neutron headline numbers before using it."
      - "An EC rate comparable to the CEvNS rate could be real, or could come from quoting saturation activity while the comparison spectra are steady-state. Separated by carrying the scenario label on every rate row and by quoting the t = 1 d value beside the saturation value in the closeout."
      - "The exactly-zero counts residuals could indicate a correct fold or a trivially degenerate one. They are exact because the input is a single populated deposit column and R's columns sum to 1; that is stated as the reason rather than presented as a strong check, and the non-trivial checks are elsewhere."
    disconfirming_observations:
      - "THE PHASE-15 CRITERION COMES OUT THE OTHER WAY AT THIS ENERGY. 2W_e = 250.02 at 158.7 eV SATISFIES the electron-side IA validity condition that Phase 15 measured failing at 0.1574 on the 0.1 eV grid floor. Inheriting Phase 15's sentence — which the plan's own approximation block invited — would have been wrong. The exclusion had to be re-argued on different grounds, and the width that was not applied is 0.518 reconstructed bins, i.e. comparable to the binning rather than negligible."
      - "THE MAPPING SLOPE IS NOT ~0.5 AT THIS ENERGY. The planning finding extrapolated Phase 13's 1 eV image (~0.497) to predict ~75 eV. The measured slope at 158.7 eV is 0.4099 / 0.3967 and the image lands at 65.0 / 63.0 eV — 12% and 16% below the pre-registered estimate. The SC3 conclusion is unchanged, but it is unchanged BY MEASUREMENT: had the slope run the other way past ~0.63 the clause would have been REFUTED."
      - "SC2's OWN ILLUSTRATIVE NUMBERS DO NOT SURVIVE CONTACT WITH GE. '473 eV at 8 MeV' against a 754.11 eV 73Ge ceiling (+59%), and 'tens of eV for a realistic multi-gamma cascade' against EGAF-sourced isotropic means of 149.5-186.5 eV on observed multiplicities of only 1.66-4.25. Reported as supersessions rather than reconciled, and the criterion graded PARTIALLY CONFIRMED as a result."
      - "THE 71Ge PRODUCTION RATE WAS WRONG BY 4.86x IN A FIRST IMPLEMENTATION, because the 70Ge abundance factor was omitted and the bare cross section was folded against N_Ge — the rate for an isotopically pure 70Ge wafer. It was caught only by cross-checking against the Plan 14-01 per-isotope row, which already carried the weight. Nothing in the plan's own dimensional_check block would have caught it."
      - "THE M-LINE BOUND EXCEEDS THE CEvNS SIGNAL INSIDE THE RoI, at 1.794x (Ta->Al) and 1.789x (Al->Hf) at saturation, and lands there ENTIRELY. That supports the phase's premise more strongly than the roadmap states — but it is a bound at a scenario the project does not own, and at t = 1 d it falls to ~11% of the CEvNS in-RoI rate."
      - "THE ADOPTED Phi_th IS 3.95x ABOVE BIFFL'S STATED REQUIREMENT and this configuration does not meet it."
---

# 14-02 Summary — ⁷¹Ge EC lines and the Phase-14 closeout

**Status:** complete · **Report:** `GPD/phases/14-ge-only-thermal-capture-channels-p-geonly/14-02-EC-AND-CLOSEOUT.md`

## Headline numbers

| quantity | Ta→Al | Al→Hf | class |
|---|---:|---:|---|
| M-line reconstructed image (matrix unbinned mean) | **65.049 eV** | **62.964 eV** | measured |
| mapping slope E_rec / 158.7 eV | **0.4099** | **0.3967** | measured |
| **in-RoI fraction (E_rec 10–100 eV)** | **1.000000** | **1.000000** | measured |
| response `rel_spread` vs bin width | 0.93 % vs 11.52 % | 0.85 % vs 11.52 % | measured |
| M-line bound, **saturation** | **130.82** | **130.82** counts kg⁻¹ day⁻¹ | BOUNDED |
| ratio to CEvNS **in-RoI** (72.92 / 73.14) | **1.794×** | **1.789×** | shared axis |
| M-line bound, t = 1 d | 7.70 | 7.70 | BOUNDED |
| A_sat (⁷⁰Ge → ⁷¹Ge, all E, abundance-weighted) | 1054.1472 counts kg⁻¹ day⁻¹ | | folded |
| **P_K** | **0.8759 ± 0.0043** | | SOURCED (derived) |
| P_L, P_M | ≤ 0.1241 (8.06× tighter than trivial) | | BOUNDED |
| Q_EC, T_ν | 232.47 ± 1.15 keV, **0.408569 eV** (0.0211 bins) | | SOURCED |
| 2W_e at 158.7 eV | **250.02 — condition SATISFIED** | | measured |

## Five ROADMAP verdicts

SC1 **CONFIRMED** · SC2 **PARTIALLY CONFIRMED** · SC3 **CONFIRMED** (by measurement) ·
SC4 **CONFIRMED** on branch (a) · SC5 **CONFIRMED**.

## Checkpoint recorded

Task 3's `checkpoint:human-verify` (Phase 14 closeout) is recorded in
`14-02-EC-AND-CLOSEOUT.md` §8 with its default taken under the standing session directive,
together with the update the reviewer needs on its point 3: the lines are **not** bounded
only by the total EC rate, because P_K was derived.

## Deviations

- **Rule 1 (own bug, caught by cross-check).** The ⁷¹Ge production rate initially omitted the
  ⁷⁰Ge abundance factor and returned 5124.68 instead of 1054.15 — 4.86× too large, the rate
  for an isotopically pure ⁷⁰Ge wafer. Fixed, and the module now returns the pure-⁷⁰Ge value
  alongside so the factor is visible rather than implicit.
- **Rule 4 (missing component).** `SHIELDED_TOKENS_EXTRA`'s `residual` token collides
  semantically with the counts-conservation residual. Scanned with one narrow, named
  exemption; `dru` and `Table 5` remain live.
- **Scope note.** The plan expected the ⁷¹Ge branching to be BOUNDED at ≤ 1 and the Ga
  identification to be marked UNVERIFIED. Both were improved by integrity-checked
  retrievals inside the plan's own contract (P_K derived; the Ga edges checked), and the
  improvement is recorded with its provenance limits rather than presented as certainty.
