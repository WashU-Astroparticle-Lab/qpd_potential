---
phase: 15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em
plan: 02
title: "Both electron-recoil channels on the 744-bin extended axis from 100 meV by exact re-drive with the identical sample stream, the frozen v1.0 CSVs shown regenerable in all 584 bins, every SC1 invariant reproduced -- and the muon sub-eV region reported as a bounded absence because not one of its 160 new bins reaches adequate statistics"
date: 2026-07-23
status: complete
depth: full
completed: 2026-07-23
provides:
  - "src/qpd_potential/em_extended.py -- route selection by executed measurement, the bit-identity probe, statistical adequacy labelling, validity-floor flagging from the Plan 15-01 table, the NaN no-support discipline with its one narrow kinematic exception, the writers, the closed-form Compton edges and the SC1 regression"
  - "src/qpd_potential/muon_deposit.py and compton_deposit.py -- a grid_version parameter DEFAULTING to v1.0 with the Plan 10-03 literal pin kept as the default branch; per-bin raw mc_entries accumulators; the shared_energy_grid docstring defect fixed"
  - "artifacts/v2.0/muon_dRdEdep_ext.csv and compton_dRdEdep_ext.csv -- 744 rows each with per-bin mc_err, raw mc_entries, statistical adequacy label, below_validity_floor flag and the channel accuracy label, declaring broadened_provenance = false"
  - "artifacts/v2.0/em_v1_regression.csv -- 1168 per-bin rows plus the SC1 scalar invariant block"
  - "tests/test_em_extended.py -- 21 tests covering all 12 contract acceptance tests"
  - "GPD/phases/15-.../15-02-EXTENDED-DEPOSIT-SPECTRA.md -- the route evidence, the SC1 table, and an honest account of the 160 new bins"
  - "artifacts/v2.0/legacy_grid_disposition.csv -- disposition rows for the three new artifacts (56 register rows)"
  - "GPD/phases/10-.../10-03-GRID-CONSTRUCTION.md -- 14 new version-pin rows plus two re-pointed producer rows, so the Phase-10 grep-count guard stays closed"
one_liner: "Route decided by MEASUREMENT and not assertion: at small N the RNG stream is provably independent of the histogram edges in both drivers, so bins 160..743 reproduce with np.array_equal True for dR/dE, mc_err, raw entries AND the integral rate in both channels, licensing route exact_redrive_identical_stream; the production cost was measured on a batch and extrapolated BEFORE launching (muon 8.0 min predicted / 8.5 min actual at 1e9 samples, Compton 2.3 min predicted / 2.5 min actual at 4e7 per line) so no sample count was reduced and there is no statistical penalty to record; the never-before-executed question of whether the frozen v1.0 CSVs are regenerable is answered YES -- both reproduce in 584/584 bins at the files' own %.6e precision, the residual 4.376e-07 (muon) and 4.632e-07 (Compton) being the CSV round-trip rather than the physics; every SC1 invariant reproduces, with the three closed-form Compton edges at 1243.3573 / 1541.3115 / 2381.7571 keV to better than 1e-3 keV, the through-wafer muon rate 1.365914 +/- 0.000308 Hz inside the frozen 1.3659 +/- 0.0003, the Compton bound-incoherent rate of record 2.6747e-01 Hz and the energy closure 2.102771e+05 counts/kg/day, and the max extended-versus-frozen relative difference four decades inside the 1% bar; no photopeak survives -- 153 bins lie above the highest Compton edge and none carries content, the 2614.511 keV bin carries exactly 0.0, and assemble_channel RAISES if an entry is ever found there; and the honest finding about the 160 new bins is that for the MUON channel they are a BOUNDED ABSENCE rather than a spectrum, with 35 bins carrying no MC support at all, ZERO bins reaching adequate_mc_support, a median relative MC error of 0.868, and all 160 sitting below the Plan 15-01 Landau-Vavilov validity floor of 4111.82 eV, while the Compton channel does slightly better with 7 adequate and 31 marginal bins but has 70 of its 160 below the 0.73955 eV Ge pair-creation floor where the S(x,Z) machinery returns a number that is not a physical rate."
plan_contract_ref: GPD/phases/15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em/15-02-PLAN.md#/contract

contract_results:
  claims:
    claim-route-decided:
      status: passed
      summary: "Decided by an executed test, with the evidence recorded in both emitted headers. STRUCTURAL LEG, run at small N before any production time was spent: em_extended.bit_identity_probe runs each Monte Carlo twice at identical (n, seed, batch_size), once on shared_energy_grid('v1.0') and once on shared_energy_grid('v2.0-ext'), and compares bins 160..743 with np.array_equal -- never np.allclose. All eight comparisons return True (muon dR/dE, mc_err, raw entries, integral rate; Compton the same four), and the edge join itself is np.array_equal True with max absolute difference exactly 0.0. The reason is structural and was verified by reading the drivers: every random draw in muon_deposit._mc_batch and in compton_deposit.sample_electron_recoil precedes np.histogram, and the Compton driver spawns per-(line, batch) child streams from SeedSequence(seed), so the stream cannot depend on the edge array. COST LEG, required by the plan and executed before launching: 5e6 muon samples in 2.399 s extrapolating to 8.0 min at 1e9, and 4e5 Compton samples per line in 1.397 s extrapolating to 2.3 min at 4e7; actual 512.2 s and 147.4 s. Both are practical, so NO sample count was reduced, the frozen counts n_samples = 1e9 and n_per_line = 4e7 with seed 20260720 and batch_size 5e6 were used verbatim, and there is no statistical penalty to record. FROZEN-REPRODUCTION LEG, never executed before this plan: both frozen CSVs reproduce in 584/584 bins at their own %.6e precision, max relative difference 4.376023e-07 (muon, bin 412, 1.435415e+03 keV) and 4.632438e-07 (Compton, bin 51, 4.403934e-02 keV), with zero bins where one is zero and the other is not. The residual is the six-significant-figure CSV round-trip, not a computational difference. THE FROZEN v1.0 DEPOSIT ARTIFACTS ARE THEREFORE REGENERABLE FROM COMMITTED CODE AT THEIR RECORDED SETTINGS -- a positive finding about the v1.0 record, recorded because the plan required the answer either way. Route selected: exact_redrive_identical_stream. The index_carry_frozen_bins alternative was not needed; had either leg failed it would have been taken and the failure written up as a finding rather than worked around."
      linked_ids: [deliv-extended-module, deliv-spectra-report, deliv-extended-tests, test-smallN-bit-identity, test-frozen-reproduction, test-route-recorded, ref-muon-module, ref-compton-module, ref-grid-extension]
      evidence:
        - verifier: gpd-executor
          method: "np.array_equal at small N on four independent arrays per channel, then a full production re-drive compared bin by bin against the committed CSVs at their own written precision"
          confidence: high
          claim_id: claim-route-decided
          deliverable_id: deliv-extended-module
          acceptance_test_id: test-smallN-bit-identity
          reference_id: ref-grid-extension
          forbidden_proxy_id: fp-silent-reinterpolation
          evidence_path: GPD/phases/15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em/15-02-EXTENDED-DEPOSIT-SPECTRA.md
    claim-extended-deposit-spectra:
      status: passed
      summary: "Both channels have a 744-row dR/dE_dep table in artifacts/v2.0/ reaching the 0.0999350 eV floor, produced with the v1.0 machinery unchanged at the v1.0 sea-level zero-overburden normalization. Bin centres match sqrt(edges[:-1]*edges[1:]) of shared_energy_grid('v2.0-ext') to rtol 1e-6 and the edge join is np.array_equal with max difference exactly 0.0. Every row carries the bin centre in keV, dR/dE_dep, mc_err in the same units, the raw mc_entries count, the relative MC error, a below_validity_floor flag read from the Plan 15-01 table (muon floor 4111.82 eV, 369 of 744 flagged; Compton floor 0.73955 eV, 70 of 744 flagged), a statistical adequacy label from a closed vocabulary, and the channel accuracy label -- the three labels trailing so that a plain numeric parse of a row stops after five fields and a rate cannot be read out without them. Both tables declare broadened_provenance = false and fold.read_broadened_provenance returns exactly False, not None. NaN DISCIPLINE: bins with zero raw entries are written NaN and labelled no_mc_support, never 0.0, and no supported bin is NaN. ONE NARROW EXCEPTION, argued rather than assumed: the 153 Compton bins whose LOWER EDGE exceeds the highest Compton edge 2381.7571 keV are written 0.0 and labelled kinematically_forbidden, because there the reasoning behind fp-zero-for-no-data INVERTS -- the thin-target single-scatter model positively forbids content, so 0.0 is the model's PREDICTION and NaN would say 'unmeasured' about a region the model excludes, while fp-full-absorption requires the approximation intact IN THE ARTIFACT. The exception is asserted to equal exactly edges[:-1] > 2381.7571, asserted to be Compton-only, and assemble_channel RAISES if any entry is ever found above that ceiling. NORMALIZATION: every multiplicative factor is enumerated individually in both headers and is exactly 1.0 -- overburden_attenuation, shield_attenuation, veto_credit (by construction), buildup_factor, ambience_rescale -- because a product can be unity by cancellation. No data/ file was written: SHA-256 of all five frozen files matches git show HEAD, and tests/test_env_v1_identity.py is re-executed inside the test and passes."
      linked_ids: [deliv-muon-ext-table, deliv-compton-ext-table, deliv-extended-module, deliv-spectra-report, deliv-extended-tests, test-grid-shape, test-no-frozen-file-written, test-unbroadened-declared, test-labels-inseparable, test-no-support-not-zero, test-dimensions, ref-grid-extension, ref-validity-floors, ref-mu-gamma-declaration]
      evidence:
        - verifier: gpd-executor
          method: "a per-bin cross-check of the emitted value against the raw MC entry count in every one of the 744 bins, plus a source-level check that no nan_to_num call exists in the path"
          confidence: high
          claim_id: claim-extended-deposit-spectra
          deliverable_id: deliv-muon-ext-table
          acceptance_test_id: test-no-support-not-zero
          reference_id: ref-disposition-register
          forbidden_proxy_id: fp-zero-for-no-data
          evidence_path: artifacts/v2.0/muon_dRdEdep_ext.csv
    claim-sc1-invariants:
      status: passed
      summary: "Every v1.0-validated invariant reproduces on the extended axis. COMPTON EDGES, recomputed IN CLOSED FORM from data/gamma_lines.csv independently of the sampler: K-40 1243.3573, Bi-214 1541.3115, Tl-208 2381.7571 keV, all three to better than 1e-3 keV against a 0.5 keV tolerance, matching 09-01 Section 3.3 exactly. MUON RATE: 1.365914 +/- 0.000308 Hz against the frozen 1.3659 +/- 0.0003, |difference| 1.4e-5, inside the frozen uncertainty -- written into the header explicitly flagged as an ABSOLUTE through-wafer rate in Hz and NOT a per-kg quantity, because a units slip there would be invisible in the shape and fatal in the normalization. COMPTON RATES: the four-way distinction carried verbatim and NOT collapsed -- bound incoherent 2.6747e-01 Hz is the rate of record, free-KN 2.6846e-01, VALD-03 anchor 2.7305e-01, f_bind 0.9963 -- with the energy closure 2.102771e+05 counts/kg/day reproducing the frozen 2.1028e+05 and equal to rate * 86400 / mass_kg. REGRESSION: the per-bin relative difference over all 584 retained bins is frozen in artifacts/v2.0/em_v1_regression.csv with the maximum flagged per channel; the maxima are 4.376023e-07 and 4.632438e-07, four decades inside the 1% bar, and the test asserts BOTH the 1% contract bound and the tighter 1e-6 statement so a real re-grid drift could not hide inside the contract tolerance. NO PHOTOPEAK: 153 bins have a lower edge above 2381.7571 keV and zero of them carry content; the bin containing 2614.511 keV (index 593, centre 2627.3296 keV) carries exactly 0.0 with zero raw entries; and the muon channel is asserted NOT to have acquired a kinematic ceiling it should not have."
      linked_ids: [deliv-regression-table, deliv-spectra-report, deliv-extended-tests, test-compton-edges, test-muon-rate, test-v1-regression-1pct, test-no-photopeak, ref-mu-gamma-declaration, ref-disposition-register]
  deliverables:
    deliv-muon-ext-table:
      status: produced
      path: artifacts/v2.0/muon_dRdEdep_ext.csv
      summary: "744 rows. Header records route = exact_redrive_identical_stream with the evidence that selected it, n_mc_samples = 1000000000, seed 20260720, batch_size 5000000, grid_version v2.0-ext with the exact edge-join statement, repo HEAD, broadened_provenance = false with the Plan 15-01 verdict quoted, the five individually-unity normalization factors, integral_muon_rate_Hz = 1.3659 +/- 0.0003 flagged ABSOLUTE not per-kg, the validity floor and its 369 flagged bins, the no-support discipline with its counts, and the accuracy label. 35 bins NaN with no_mc_support; no kinematically_forbidden bins."
      linked_ids: [claim-extended-deposit-spectra, claim-sc1-invariants]
    deliv-compton-ext-table:
      status: produced
      path: artifacts/v2.0/compton_dRdEdep_ext.csv
      summary: "744 rows, same columns and provenance discipline. Header carries the four-way rate distinction verbatim, the energy closure, and the kinematic-ceiling exception with its count. 69 bins NaN with no_mc_support; 153 bins 0.0 with kinematically_forbidden; 70 bins flagged below_validity_floor."
      linked_ids: [claim-extended-deposit-spectra, claim-sc1-invariants]
    deliv-regression-table:
      status: produced
      path: artifacts/v2.0/em_v1_regression.csv
      summary: "1168 per-bin rows (584 per channel) with the frozen value, the extended value, the relative difference and an is_max_for_channel flag, above a header block of ten named scalar invariants each with its value, units, target and verdict."
      linked_ids: [claim-sc1-invariants]
    deliv-extended-module:
      status: produced
      path: src/qpd_potential/em_extended.py
      summary: "ROUTE_VOCABULARY, STAT_ADEQUACY_VOCABULARY, bit_identity_probe, read_frozen_csv, frozen_reproduction, select_route, stat_adequacy_label, below_validity_floor_flags, ExtendedChannel, assemble_channel, write_channel_csv, read_channel_csv, closed_form_compton_edges, v1_regression, write_regression_csv, NORMALIZATION_FACTORS, MUON_ACCURACY_LABEL, GAMMA_ACCURACY_LABEL. Contains no nan_to_num, no ia_broadening import and no computed exp(-2W)."
      linked_ids: [claim-route-decided, claim-extended-deposit-spectra, claim-sc1-invariants]
    deliv-extended-tests:
      status: produced
      path: tests/test_em_extended.py
      summary: "21 tests. Small-N bit identity on four arrays per channel; frozen reproduction recorded; route recorded with its evidence; grid shape with np.array_equal on the edge join; frozen-file immutability by SHA-256 against HEAD plus a re-run of the Phase-9 identity suite; broadened_provenance exactly False; no computed exp(-2W) and no ia_broadening import, with the em_recoil guard exercised; labels inseparable including the muon Leg A and bracketing text and a demonstration that a numeric parse stops at five fields; no-support-not-zero with the kinematic exception bounded exactly; no nan_to_num in the path; the adequacy label failing rather than ranking low; validity-floor flags read from Plan 15-01 rather than re-chosen; each normalization factor individually 1.0; the three closed-form edges; the muon rate; the regression at both the 1% and the 1e-6 level; no photopeak; dimensions and the energy closure; disposition rows; the Phase-9 token scan; and the report's honesty tokens."
      linked_ids: [claim-route-decided, claim-extended-deposit-spectra, claim-sc1-invariants]
    deliv-spectra-report:
      status: produced
      path: GPD/phases/15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em/15-02-EXTENDED-DEPOSIT-SPECTRA.md
      summary: "Six sections: the route decision with the structural, cost and frozen-reproduction legs each executed and tabulated; the SC1 invariant table with the normalization enumeration and the frozen-file check; a per-channel account of the 160 new bins with the label histograms, the entry counts, the relative-error quartiles and the floor counts, concluding that the muon sub-eV region is a bounded absence; the NaN discipline and its one argued exception; the accuracy labels in full; the verification ledger; and uncertainty markers naming which disconfirming observations fired."
      linked_ids: [claim-route-decided, claim-extended-deposit-spectra, claim-sc1-invariants]
    deliv-disposition-rows:
      status: produced
      path: artifacts/v2.0/legacy_grid_disposition.csv
      summary: "Three rows, all native_to_extended_axis with validity_floor 0.0000999350 keV for the two spectra and not_a_spectrum for the regression table. Register now 56 rows; the git-ls-files closure guard passes."
      linked_ids: [claim-extended-deposit-spectra]
  acceptance_tests:
    test-smallN-bit-identity:
      status: passed
      summary: "np.array_equal True on bins 160..743 for dR/dE, mc_err and raw entries in BOTH channels, plus exact equality of the integral rates, plus the edge join itself array_equal with max absolute difference 0.0. np.allclose is never used. The exact-re-drive route is licensed."
      linked_ids: [claim-route-decided, deliv-extended-tests, deliv-spectra-report]
    test-frozen-reproduction:
      status: passed
      summary: "Attempted and recorded, with a positive outcome: 584/584 bins identical at the frozen files' own %.6e precision for both channels, max relative difference 4.376e-07 and 4.632e-07, zero sign-of-support mismatches. The frozen v1.0 artifacts ARE regenerable at their recorded settings."
      linked_ids: [claim-route-decided, deliv-spectra-report, deliv-regression-table]
    test-route-recorded:
      status: passed
      summary: "Both headers name exactly one route from ROUTE_VOCABULARY and carry route_selected_by naming the executed test and its PASS verdicts."
      linked_ids: [claim-route-decided, deliv-muon-ext-table, deliv-compton-ext-table, deliv-extended-tests]
    test-grid-shape:
      status: passed
      summary: "744 rows per table, centres matching the extended grid to rtol 1e-6, and np.array_equal(edges[160:], v1_edges) with max absolute difference exactly 0.0 -- the check that excludes the Plan 10-03 5.101629e-04 silent-reinterpolation drift that np.allclose would pass."
      linked_ids: [claim-extended-deposit-spectra, deliv-muon-ext-table, deliv-compton-ext-table, deliv-extended-tests]
    test-no-frozen-file-written:
      status: passed
      summary: "SHA-256 of data/muon_dRdEdep.csv, data/compton_dRdEdep.csv, data/gamma_lines.csv, data/ge_incoherent_S.csv and data/ge_xcom_mu.csv each match git show HEAD:<path>, and tests/test_env_v1_identity.py is re-executed as a subprocess inside the test and returns 0."
      linked_ids: [claim-extended-deposit-spectra, deliv-extended-tests]
    test-unbroadened-declared:
      status: passed
      summary: "fold.read_broadened_provenance returns exactly False for both tables. A None return would have failed, because the downstream guard treats an undeclared table as UNKNOWN rather than as unbroadened, and that would block Plan 15-03."
      linked_ids: [claim-extended-deposit-spectra, deliv-muon-ext-table, deliv-compton-ext-table, deliv-extended-tests]
    test-labels-inseparable:
      status: passed
      summary: "All three labels present on all 744 rows of both tables, every adequacy value drawn from the closed vocabulary, and the muon accuracy label carrying Leg A, Leg B, -20.61%, +20.34%, the word BRACKET and the 30-35% Gaisser-Guan spread. Demonstrated rather than asserted: a plain float() parse of a row stops after exactly five fields, so a consumer meets the labels before it can finish reading a rate."
      linked_ids: [claim-extended-deposit-spectra, deliv-muon-ext-table, deliv-compton-ext-table, deliv-extended-tests, ref-mu-gamma-declaration]
    test-no-support-not-zero:
      status: passed
      summary: "Every zero-entry bin outside the kinematic ceiling is NaN and labelled no_mc_support; none is 0.0; and no supported bin is NaN. The exception set is asserted to equal exactly edges[:-1] > 2381.7571 keV, to carry zero entries, to carry exactly 0.0, and to be Compton-only. A source-level test asserts nan_to_num appears in no executable line of the module."
      linked_ids: [claim-extended-deposit-spectra, deliv-muon-ext-table, deliv-compton-ext-table, deliv-extended-tests, ref-disposition-register]
    test-compton-edges:
      status: passed
      summary: "1243.3573 / 1541.3115 / 2381.7571 keV from the closed form 2E^2/(m_e c^2 + 2E) applied to data/gamma_lines.csv, asserted at 0.5 keV as the contract requires AND re-asserted at 1e-3 keV so a drift could not hide inside the contract tolerance."
      linked_ids: [claim-sc1-invariants, deliv-regression-table, deliv-extended-tests, ref-mu-gamma-declaration]
    test-muon-rate:
      status: passed
      summary: "1.365914 +/- 0.000308 Hz read back from the emitted header, inside the frozen 1.3659 +/- 0.0003, with the header asserted to carry the words 'ABSOLUTE through-wafer rate in Hz, NOT a per-kg quantity'."
      linked_ids: [claim-sc1-invariants, deliv-muon-ext-table, deliv-extended-tests, ref-mu-gamma-declaration]
    test-v1-regression-1pct:
      status: passed
      summary: "584 rows per channel in em_v1_regression.csv; maxima 4.376023e-07 and 4.632438e-07, both below the 1% contract bound and below the tighter 1e-6 six-significant-figure round-trip bound. Under the exact-re-drive route the computational difference is zero and what remains is the CSV format."
      linked_ids: [claim-sc1-invariants, deliv-regression-table, deliv-extended-tests, ref-grid-extension]
    test-no-photopeak:
      status: passed
      summary: "153 bins have a lower edge above the highest Compton edge; all are finite and all are exactly 0.0. The bin containing 2614.511 keV is index 593 and carries 0.0 with zero raw entries. The muon channel is asserted to carry no kinematically_forbidden label at all."
      linked_ids: [claim-sc1-invariants, deliv-compton-ext-table, deliv-extended-tests, ref-mu-gamma-declaration]
    test-dimensions:
      status: passed
      summary: "Every column header carries its units; mc_err carries the same dimension as the quantity it bounds; the Compton energy closure 2.102771e+05 counts/kg/day reproduces the frozen value and equals rate * 86400 / mass_kg to 2e-3; all four Compton rate tokens are present in the header; and the muon header carries the ABSOLUTE flag so a Hz quantity cannot be read as per-kg."
      linked_ids: [claim-extended-deposit-spectra, deliv-muon-ext-table, deliv-compton-ext-table, deliv-extended-tests]
  references:
    ref-grid-extension:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "shared_energy_grid and GRID_VERSIONS used directly; the 160-prepended-bins construction is what makes np.array_equal(new[160:], old) true and therefore what makes an exact regression possible at all. The docstring defect flagged twice in prior phase contexts -- it called v2.0-ext the default when DEFAULT_GRID_VERSION reads v1.0 -- is FIXED by this plan."
    ref-disposition-register:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "The two frozen CSVs' existing rows were read and their statement that 're-running the Phase-4 deposit Monte Carlo onto the extended axis is Phase 15's job' is what this plan discharges. carried_onto_extended_axis's NaN-not-zero discipline was carried over verbatim into the new tables and is what the no-support labelling implements. Three new rows added; register closure guard green at 56 rows."
    ref-mu-gamma-declaration:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "Section 3.3's three Compton edges and the no-photopeak demonstration reproduced; Section 2.3's muon rate reproduced; the four-way Compton rate distinction carried verbatim; the accuracy labels of Sections 2.5 and 3.4 carried onto every row with the PDG anchor-leg caveat attached and never narrowed."
    ref-muon-module:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "run_muon_mc, _mc_batch and write_csv read in full. The machinery is unchanged: the only edits are a grid_version parameter defaulting to v1.0 with the literal Plan 10-03 pin kept as the default branch, a raw mc_entries accumulator that consumes no random numbers, and the docstring fix. The RNG-stream-independence-from-edges the route decision rests on was verified by reading the draw order and then by measurement."
    ref-compton-module:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "run_compton_mc, write_csv and compton_source read in full, including the deliberate v1.0 call-site pin protecting data/compton_dRdEdep.csv, which is preserved, and the SeedSequence(seed).spawn(len(lines) * n_batches_per_line) child-stream construction that makes the per-(line, batch) stream independent of the edges."
    ref-validity-floors:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "em_validity_floors.csv is read at assembly time via em_recoil.validity_floor_rows, so the flag is the Plan 15-01 floor rather than a threshold re-chosen here, and a test asserts the emitted flags equal a fresh evaluation of that table. 369 of 744 muon bins and 70 of 744 Compton bins are flagged."
  forbidden_proxies:
    fp-silent-reinterpolation:
      status: rejected
      notes: "No interpolation of any kind. The edge join is asserted with np.array_equal and its maximum absolute difference is exactly 0.0; the retained bins come from the same sample stream re-histogrammed on an edge array whose tail IS the v1.0 array. np.allclose appears nowhere in the join check."
    fp-zero-for-no-data:
      status: rejected
      notes: "Zero-entry bins are NaN and labelled, verified bin by bin over all 744 bins of both tables, and nan_to_num appears in no executable line of em_extended.py. The single exception is argued from physics rather than convenience, is bounded to exactly the set edges[:-1] > 2381.7571 keV, is Compton-only, and is accompanied by a raise if an entry is ever found there."
    fp-mc-rerun-drift:
      status: rejected
      notes: "No data/ file was written. All five frozen files' SHA-256 match git show HEAD, no provenance header was edited even to add a tag, and tests/test_env_v1_identity.py is re-executed inside the test suite and passes."
    fp-improved-normalization:
      status: rejected
      notes: "Sample counts, seed, batch size and every physics constant are the frozen v1.0 values. Nothing was raised to make a band look tighter, no flux parametrization was changed, and both accuracy labels are byte-identical in content to the v1.0 statements. The plan's own instruction to reduce N and record the penalty if the cost were impractical did not apply: the cost was measured at 8.5 and 2.5 minutes."
    fp-full-absorption:
      status: rejected
      notes: "Enforced in code rather than checked after the fact: assemble_channel raises if any Compton entry appears above the highest closed-form Compton edge. The artifact shows 153 bins of exact 0.0 above the ceiling and 0.0 in the 2614.511 keV bin, so the thin-target single-scatter approximation is intact IN THE ARTIFACT and not merely in the prose."
    fp-shielded-quantity-leak:
      status: rejected
      notes: "The Phase-9 token list is IMPORTED via test_env_v1_identity rather than re-typed, with its digit-boundary matching, and scanned over both emitted tables, the regression table and em_extended.py. Zero applied hits. Separately, every multiplicative factor on each normalization is enumerated INDIVIDUALLY in both headers and asserted to be exactly 1.0 one at a time, because a product can be unity by cancellation."
  uncertainty_markers:
    weakest_anchors:
      - "The muon normalization's ~20%-vs-PDG standing whose SIGN is anchor-leg dependent -- Leg A puts the adopted 1.3659 Hz 20.61% BELOW, Leg B puts it 20.34% ABOVE, and the two bracket it. Carried on every row with the disclosure attached."
      - "The 30-35% inter-experiment Gaisser-Guan normalization spread, named in the v1.0 manuscript as this channel's weakest anchor, which no in-repo artifact can narrow."
      - "The gamma factor-2 site band, anchored at LABChico with the U-chain set by an assumed Phi_U = Phi_Th chain balance rather than a measured line intensity."
      - "The sub-10.14 eV content of both channels has no external validation of any kind and, per Plan 15-01, lies outside both deposit models' validity domains -- entirely for the muon channel, and below 0.73955 eV for the Compton channel."
    unvalidated_assumptions:
      - "RESOLVED by execution rather than assumed: the frozen v1.0 CSVs ARE reproducible from committed code at their recorded settings, 584/584 bins at the files' own precision, for both channels."
      - "That the per-bin Monte Carlo error means anything in the sub-eV bins. It does not where the entry count is of order one, which is why stat_adequacy_label demotes any bin with fewer than 10 raw entries regardless of what sqrt(sum w^2)/y evaluates to, and why the ADEQUACY LABEL rather than the error bar is the operative statement there."
    competing_explanations:
      - "Sub-eV muon content as genuine short-chord corner-clipping geometry, versus the tabulated Landau inverse-CDF's left tail against the zero clip, versus Monte Carlo noise at entry counts too low to mean anything. Plan 15-01 Section 5.5 showed the first two are a JOINT tail and that both limbs sit far below xi ~ I; this plan adds the third measurement -- 572 raw entries across 160 bins, no bin reaching adequate statistics -- so all three readings agree that no sub-eV muon rate may be quoted."
    disconfirming_observations:
      - "DID NOT FIRE: the frozen v1.0 CSVs reproduce in 584/584 bins for both channels, so the v1.0 artifacts are regenerable and the exact-re-drive route is honest."
      - "DID NOT FIRE: bins 160..743 ARE bit-identical under re-histogramming; the RNG stream is not coupled to the edge array anywhere."
      - "DID NOT FIRE: the maximum extended-versus-frozen relative difference is 4.6e-07, four decades inside the 1% bar, so no re-grid bug exists."
      - "FIRED: a large fraction of the 160 new bins have no or inadequate support. For the MUON channel not one bin reaches adequate_mc_support, 35 have no support at all, the median relative error is 0.868 and all 160 lie below the Plan 15-01 validity floor -- so the honest deliverable there is a BOUNDED ABSENCE and it is reported as such rather than smoothed over."
---

# Plan 15-02 Summary

## Route: `exact_redrive_identical_stream`, selected by measurement

The RNG stream is provably independent of the histogram edges in both drivers
(`np.array_equal` True on dR/dE, `mc_err`, raw entries and the integral rate, for
both channels, at small N before any production time was spent). Cost was measured
and extrapolated before launching: **8.0 min predicted / 8.5 min actual** for the
muon 1e9 run, **2.3 min predicted / 2.5 min actual** for the Compton 4e7/line run.
**No sample count was reduced; there is no statistical penalty to record.**

## The frozen v1.0 artifacts **are** regenerable — a first

Never executed before. Both frozen CSVs reproduce in **584/584 bins** at the files'
own `%.6e` precision. Max relative difference 4.376e-07 (muon) / 4.632e-07
(Compton) — the CSV round-trip, not the physics.

## SC1 invariants

All reproduce: edges **1243.3573 / 1541.3115 / 2381.7571 keV** (< 1e-3 keV), muon
rate **1.365914 ± 0.000308 Hz**, Compton rate of record **2.6747e-01 Hz**, closure
**2.102771e+05 counts/kg/day**, regression max **4.6e-07** (four decades inside the
1 % bar), **no photopeak** and exactly 0.0 in the 2614.511 keV bin.

## The honest finding about the 160 new bins

| | muon | Compton |
|---|---|---|
| bins with MC support | 125/160 | 91/160 |
| `no_mc_support` (NaN) | 35 | 69 |
| `adequate_mc_support` | **0** | 7 |
| median relative MC error | **0.868** | 0.470 |
| below the Plan 15-01 validity floor | **160/160** | 70/160 |

**The muon sub-eV region is a bounded absence, not a spectrum** — every bin is
outside the deposit model's domain *and* statistically inadequate, two independent
reasons. The Compton channel reaches further with usable statistics, but 70 of its
160 bins sit below the Ge pair-creation floor where the machinery returns a number
that is not a rate.

## Deviations

**One, documented rather than silent.** The plan's `test-no-photopeak` requires the
2614.511 keV bin to carry *exactly 0.0*, while `fp-zero-for-no-data` requires
zero-entry bins to be NaN. Above the highest Compton edge the single-scatter model
**positively forbids** content, so a measured absence is correct and 0.0 is the
model's prediction — NaN there would say "unmeasured" about a region the model
excludes, and would make `fp-full-absorption` untestable in the artifact. The
exception is confined to exactly `edges[:-1] > 2381.7571 keV`, labelled
`kinematically_forbidden`, asserted Compton-only, and backed by a `raise` if an
entry ever appears there. This is Deviation Rule 4 (missing component: the
distinction between a forbidden zero and an unsampled bin), applied inline.

Also inline: `10-03-GRID-CONSTRUCTION.md` gained 14 version-pin rows and two
re-pointed producer rows, because the Phase-10 grep-count guard obligates a row per
`shared_energy_grid(` call site. That is the guard working as designed.
