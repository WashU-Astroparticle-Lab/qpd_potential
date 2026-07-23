---
phase: 13-ge-neutron-fold-from-the-sea-level-flux-p-tgt
plan: 02
title: "ROADMAP SC4 adjudicated by measurement — the kinematic factor cancels identically out of the flat-box fold, the operative mechanism is atoms per kg, and the Ge-vs-CaWO4 statement the roadmap actually makes reverses direction; plus the >20 MeV omission bounded at the surface with the continuation's conservatism measured, and CALC-24 deferred on the measured number rather than on the void premise"
date: 2026-07-23
status: complete
depth: full
completed: 2026-07-23
provides:
  - "src/qpd_potential/neutron_recoil.py (13-02 section, APPENDED so no earlier line number moved) — ComparisonTarget with per-material atoms/kg, COMPARISON_TARGETS for Ge/W/Ca/O/CaWO4, target_dRdT, pure_epithermal_flux, lethargy_flatness, f_cancellation_residual, target_comparison with the three-way attribution, sigma_slope_at_ceiling, high_energy_omission_bound with two continuations, ceiling_subsumption, calc24_disposition, and both artifact writers"
  - "artifacts/v2.0/neutron_compression_targets.csv — five targets x six matched recoil energies: each material's own atoms/kg, its kinematic factors, the pure-1/E control ratio, the real-flux ratio, and the attribution split into atoms-per-kg / flux-shape / kinematic parts"
  - "artifacts/v2.0/neutron_highE_omission_bound.csv — two sigma_el continuations above the 20 MeV ceiling, each with the driver flux above the ceiling and the in-RoI and total-rate omission fractions as SEPARATE columns, elastic_only = true, direction flatters_SB"
  - "GPD/phases/13-.../13-02-COMPRESSION-AND-OMISSIONS.md — the SC4 derivation and verdict, the CaWO4 substitution with its directional consequence, the numerical degeneracy that makes SC4 look confirmed, the slope measurement, the two omission fractions, the ceiling-subsumption analysis and the CALC-24 disposition with its own falsifier"
  - "tests/test_neutron_kinematics.py — 20 tests covering all 10 contract acceptance tests, tolerances declared as module constants before any check runs"
  - "artifacts/v2.0/legacy_grid_disposition.csv — disposition rows for the two new tracked .csv files"
one_liner: "ROADMAP SC4 is SUPERSEDED BY MEASUREMENT: substituting E = (T/f)x in the flat-box fold gives dR/dT = n (C/T) INT_1^inf sigma((T/f)x) x^-2 dx, so the 1/f prefactor cancels against the T/f lower limit for ANY cross section and f survives only inside sigma's argument — it selects which part of sigma(E_n) a recoil samples (which is the resonance edge Plan 13-01 measured at T = f E_res) and never scales the rate; for constant sigma it vanishes entirely, measured at 4.1997e-8 spread across f in {0.0215, 0.0536, 0.0952, 0.2215}, and the real sea-level flux is flat in lethargy to 1.3901 over 1 eV - 10 keV (reproducing 09-02's recorded 1.390) so the RoI sits close to that limit; the matched-T Ge/W ratio of 2.29-2.46 per kg across the RoI is accounted for ENTIRELY by atoms per kg (2.53339) with a -3% to -9% flux-shape correction and a kinematic part of at most 1.4e-4 that is the finite-20-MeV-ceiling truncation rather than compression, and the near-coincidence of SC4's f ratio 2.4925 with the true atoms/kg ratio 2.5334 is an algebraic near-identity of mass number (both track A_W/A_Ge) rather than a corroboration; the Ge-vs-CaWO4 statement the roadmap actually makes REVERSES — oxygen is 66.67% of CaWO4's atom count with f = 0.2215, 4.13x germanium's, giving CaWO4 1.51x more atoms per kg, so Ge/CaWO4 = 0.673-0.692 and Ge is the BETTER target per kg by ~1.45x, conditional on the common-constant-sigma assumption that is this plan's weakest input; and the >20 MeV omission is bounded at 1.35e-5 to 2.55e-5 of the in-RoI rate against 8.91% to 16.87% of the T-integrated total — a factor ~6600 apart, which is why one number would not have done — with the flat continuation's conservatism measured (OLS slope -2.667e-3 b/MeV over the top decade, -1.068e-1 over the last half-decade, but the decade is NOT monotone so a second upper continuation at the band maximum 2.317 b is reported too), the 197 MeV flux-table ceiling shown SUBSUMED and in fact not an independent omission at all because the pinned driver reaches 10 GeV, and CALC-24's deferral SUSTAINED on the measured bound with an 11.85x margin and its own falsifier attached."
plan_contract_ref: GPD/phases/13-ge-neutron-fold-from-the-sea-level-flux-p-tgt/13-02-PLAN.md#/contract

contract_results:
  claims:
    claim-compression-adjudicated:
      status: passed
      summary: "SC4 adjudicated by measurement and found SUPERSEDED BY MEASUREMENT in its mechanism. THE DERIVATION, re-done in the report rather than quoted: substituting E = (T/f)x in dR/dT = n INT_{T/f}^inf phi sigma/(f E) dE gives dR/dT = n INT_1^inf phi((T/f)x) sigma((T/f)x) x^-1 dx, and for phi = C/E this is n (C/T) INT_1^inf sigma((T/f)x) x^-2 dx. The 1/f prefactor cancels against the T/f lower limit for ANY sigma; f survives ONLY inside sigma's argument, where it selects which part of sigma(E_n) a given recoil T samples — that is the kinematic edge at T = f E_res Plan 13-01 measured, and it moves features along T rather than scaling the rate. For constant sigma even that vanishes. MEASURED: spread across f in {0.0215 (W), 0.0536 (Ge), 0.0952 (Ca), 0.2215 (O)} under a pure 1/E flux is 4.1997e-8, deviation from the closed form 4.6512e-8, both against the 1e-5 pass condition and both below the Plan 13-01 quadrature convergence tolerance. The real flux's lethargy flatness over 1 eV - 10 keV is recomputed independently from the pinned driver at 1.3901, reproducing 09-02 Section 5's recorded 1.390. ATTRIBUTION with each part sized, verified to close to 1e-6: for Ge vs W the matched-T ratio is 2.4637 / 2.4927 / 2.4554 / 2.3973 / 2.2942 / 1.9925 at T = 0.1 / 1 / 10 / 31.6 / 100 / 1000 eV, decomposing as atoms/kg 2.53339 (the entire leading effect) x flux-shape -2.75% to -21.46% x kinematic part +1.4e-7 to +1.4e-3. Under a pure 1/E flux the ratio equals the atoms/kg ratio to five significant figures at every T for every target — the decisive mechanism measurement. The residual kinematic term is not the compression mechanism at all: it is the finite-20-MeV-ceiling truncation, since a box ending at f x E_top differs by target when E_top is finite. THE NUMERICAL DEGENERACY IS NAMED: f_Ge/f_W = 2.4925 and n_Ge/n_W = 2.53339 differ by 1.6% because both track A_W/A_Ge (n ~ 1000 N_A/A and f = 4A/(1+A)^2 ~ 4/A), so SC4's ~2.5x is numerically right for the wrong reason. LEG QUALITY LABELLED: every ratio leg uses a COMMON CONSTANT sigma = 1 b for every target including Ge, because comparing a resonance-resolved Ge against a smooth W would produce 'Ge has more structure' BY CONSTRUCTION; Ge's own resonance-structure factor (8.88 to 12.14 across the probe set) is reported separately and enters no ratio. The consequence is stated: these legs settle the mechanism, not the absolute direction."
      linked_ids: [deliv-compression-table, deliv-compression-report, deliv-kinematics-tests, test-f-cancellation, test-target-ratio-measured, test-cawo4-not-w, test-sc4-verdict-recorded, ref-roadmap-sc4, ref-elastic-table, ref-neutron-decl]
      evidence:
        - verifier: gpd-executor
          method: "an analytic identity re-derived from the fold, then confirmed numerically at four kinematic factors, then decomposed against a pure-1/E control in which the answer is known exactly"
          confidence: high
          claim_id: claim-compression-adjudicated
          deliverable_id: deliv-compression-table
          acceptance_test_id: test-f-cancellation
          reference_id: ref-roadmap-sc4
          forbidden_proxy_id: fp-assert-compression
          evidence_path: GPD/phases/13-ge-neutron-fold-from-the-sea-level-flux-p-tgt/13-02-COMPRESSION-AND-OMISSIONS.md
    claim-highE-bound:
      status: passed
      summary: "The >20 MeV omission is bounded separately for the in-RoI integrated rate and the T-integrated total. CONSERVATISM MEASURED BEFORE USE, not assumed: over the top decade of the frozen table (2-20 MeV, 421 points) sigma_el runs 1.998519 b -> 1.222782 b with an OLS slope of -2.667195e-3 b/MeV, and over the last half-decade -1.068209e-1 b/MeV. The trend approaching the ceiling is decreasing, which licenses a flat continuation as an estimate. BUT THE MEASUREMENT ALSO REFUTED THE PLAN'S IMPLICIT PREMISE: the decade is NOT monotone — sigma_el peaks at 2.316993 b at 8 MeV before falling, and 34.0% of the steps rise — so flat-at-the-ceiling is not on its own an upper bound. TWO continuations are therefore reported rather than one: flat_at_ceiling (1.222782 b, the trend-justified estimate) and flat_at_band_max (2.316993 b, which bounds from above even if the trend reversed). Flux above the ceiling from the pinned driver out to 10 GeV: 3.181822e-3 cm^-2 s^-1. Against baselines of 4.418963e3 counts/kg/day in-RoI and 3.129873e4 total: in-RoI omission fraction 1.3482e-5 to 2.5546e-5, total-rate omission fraction 8.905% to 16.874% — a factor ~6600 apart, which is exactly what fp-single-omission-number exists to prevent being collapsed, and which follows from the flat-box height falling as 1/E_n so that a 1 GeV neutron spreads its recoil over a 53.6 MeV-wide box and deposits almost nothing in a 90 eV RoI. Both omissions carry direction flatters_SB in the 09-02 Section 7 schema, and the elastic-only restriction is declared as a further understatement in the same direction because nonelastic and spallation channels above 20 MeV are comparable to elastic and produce larger recoils. Nothing is netted against the channel's penalizes_SB central value."
      linked_ids: [deliv-omission-table, deliv-compression-report, deliv-kinematics-tests, test-sigma-slope-measured, test-omission-split, test-omission-direction, test-ceiling-subsumption, ref-elastic-table, ref-neutron-decl, ref-phase12-precedent]
      evidence:
        - verifier: gpd-executor
          method: "slope measured over the top decade AND the last half-decade before any continuation was used, then the bound computed under two continuations bracketing the non-monotonicity"
          confidence: medium
          claim_id: claim-highE-bound
          deliverable_id: deliv-omission-table
          acceptance_test_id: test-sigma-slope-measured
          reference_id: ref-phase12-precedent
          forbidden_proxy_id: fp-unchecked-continuation
          evidence_path: artifacts/v2.0/neutron_highE_omission_bound.csv
    claim-calc24-disposition:
      status: passed
      summary: "CALC-24's disposition is decided against the measured bound. The worst-case in-RoI fraction is 2.5546e-5 and the worst-case total-rate fraction 0.16874, against the channel's own order-of-magnitude label read as a factor ~3, i.e. a 2.0 fractional excursion — the same reading Plan 13-01's escalation rule used. Both sit inside it, so the branch taken is DEFERRAL SUSTAINED ON THE MEASURED BOUND, with the replacement rationale written explicitly: the elastic-only restriction would have to understate the bound by more than 11.85x for the total-rate omission to reach the label, and by ~7.8e4 for the in-RoI one. The Phase-7 rationale is recorded VOID and is used as a justification nowhere: an EXECUTED grep over the module, both artifacts and the report finds zero occurrences of shield attenuation, the ~5-7x figure, overburden or building moderation on any line that does not also carry a void/not-applied marker. THE BRANCH IS STATED WITH ITS OWN FALSIFIER: if nonelastic channels above 20 MeV multiply the elastic-only bound by more than ~12 the branch flips, and this project cannot measure that multiplier with the elastic-only data it holds. The two declared omissions of 09-02 Section 6 are resolved against each other: the ~197 MeV committed-flux-table ceiling sits ABOVE the 20 MeV sigma_el ceiling so every neutron above it is also above 20 MeV — SUBSUMED — and 20.55% of the >10 MeV flux lies above it, reproducing the recorded 21%. It is not an independent omission here at all, because this channel never reads that table for the fold: the pinned driver is evaluated directly at every quadrature node and reaches 10 GeV."
      linked_ids: [deliv-compression-report, test-calc24-conditional, test-void-rationale-not-reused, ref-neutron-decl, ref-requirements-calc24]
      evidence:
        - verifier: gpd-executor
          method: "explicit two-branch evaluation of the measured bound against the channel's own accuracy label, with the void rationale excluded by an executed grep rather than by intention"
          confidence: medium
          claim_id: claim-calc24-disposition
          deliverable_id: deliv-compression-report
          acceptance_test_id: test-calc24-conditional
          reference_id: ref-requirements-calc24
          forbidden_proxy_id: fp-inherit-void-rationale
          evidence_path: GPD/phases/13-ge-neutron-fold-from-the-sea-level-flux-p-tgt/13-02-COMPRESSION-AND-OMISSIONS.md
  deliverables:
    deliv-compression-table:
      status: passed
      path: artifacts/v2.0/neutron_compression_targets.csv
      summary: "Thirty rows: five targets (Ge, W, Ca, O, CaWO4) x six matched recoil energies from 0.1 eV to 1 keV. Columns carry each material's OWN molar mass and atoms/kg (never germanium's), its atom-count-weighted effective f, the pure-1/E control ratio in which f provably cancels, the real-flux ratio, the atoms/kg ratio, and the attribution split into residual_after_atoms_per_kg / flux_shape_part / kinematic_part, plus Ge's own resonance-structure factor as a separate column that enters no ratio. f per nuclide is computed as 4A/(1+A)^2 with A the dominant natural isotope's mass number, and those values reproduce the roadmap's own 0.0215 / 0.0952 / 0.2215 to better than 5e-5. Header states the derivation, the measured cancellation residual, the lethargy flatness, the leg-quality caveat and the N_A source."
      linked_ids: [claim-compression-adjudicated, test-f-cancellation, test-target-ratio-measured, test-cawo4-not-w]
    deliv-omission-table:
      status: passed
      path: artifacts/v2.0/neutron_highE_omission_bound.csv
      summary: "Two rows, one per continuation. Columns: sigma_b_used, flux_above_ceiling_cm2_s from the pinned driver out to 10 GeV, delta_dRdT, added_in_roi_counts_kg_day, omission_fraction_in_roi, added_total_counts_kg_day, omission_fraction_total, the measured top-decade slope, elastic_only = true and direction = flatters_SB. The in-RoI and total-rate fractions are SEPARATE columns by construction. Header carries the full slope measurement including the non-monotonicity that forced the second continuation, the elastic-only understatement declaration, and the ceiling-subsumption analysis."
      linked_ids: [claim-highE-bound, test-omission-split, test-omission-direction, test-sigma-slope-measured]
    deliv-compression-report:
      status: passed
      path: GPD/phases/13-ge-neutron-fold-from-the-sea-level-flux-p-tgt/13-02-COMPRESSION-AND-OMISSIONS.md
      summary: "Nine sections: the substitution derivation showing f cancels for any sigma and survives only in sigma's argument; the attribution tables with leg quality stated first; the CaWO4-vs-W substitution with its measured directional reversal; the atoms/kg-vs-f numerical degeneracy named and explained; the SC4 verdict split by component; the slope measurement with its non-monotonicity finding; the two omission fractions with the 6600x separation explained physically; the 09-02 Section 7 directional-bias rows un-netted; the ceiling-subsumption resolution; the CALC-24 branch with its replacement rationale and its own falsifier; and a closing section on what still cuts against the result."
      linked_ids: [claim-compression-adjudicated, claim-highE-bound, claim-calc24-disposition]
    deliv-kinematics-tests:
      status: passed
      path: tests/test_neutron_kinematics.py
      summary: "20 tests, all passing. Tolerances declared as module constants before any check runs: F_CANCELLATION_TOL 1e-5, PLAN_13_01_CONVERGENCE_TOL 5e-3, ATOMS_PER_KG_CROSSCHECK_TOL 1e-3, KINEMATIC_PART_TOL 5e-3, LETHARGY_FLATNESS_RECORDED 1.390 with tolerance 5e-3, the three roadmap f values with tolerance 5e-5, and RECORDED_ABOVE_197MEV_FRACTION 0.21 with tolerance 0.02. Includes an attribution-closure test asserting the three parts multiply back to the measured ratio to 1e-6, a direction test asserting Ge/W > 1 and Ge/CaWO4 < 1 across the RoI, and an executed void-rationale grep. The grep deliberately excludes its own file, because the two lines defining its search pattern would match themselves and say nothing about whether the rationale is used as a justification."
      linked_ids: [claim-compression-adjudicated, claim-highE-bound, claim-calc24-disposition]
  acceptance_tests:
    test-f-cancellation:
      status: passed
      summary: "Relative spread across f in {0.0215, 0.0536, 0.0952, 0.2215} under a pure 1/E flux with constant sigma is 4.1997e-8 against the <=1e-5 pass condition, and below the Plan 13-01 quadrature convergence tolerance of 5e-3 by five orders of magnitude, so it is not a numerical artefact masquerading as physics. Deviation from the closed form is 4.6512e-8."
      linked_ids: [claim-compression-adjudicated, deliv-compression-table, deliv-kinematics-tests]
    test-target-ratio-measured:
      status: passed
      summary: "The ratio is reported with its full T dependence over four decades and attributed to three named causes, each sized: atoms/kg (2.53339 for Ge/W, 0.66088 for Ge/CaWO4 — the entire leading effect), departure of the flux from 1/E (-2.75% to -21.46% for W, +1.78% to +14.29% for CaWO4), and the kinematic factor (<=1.4e-3, and identified as the finite-ceiling truncation rather than compression). The decomposition closes to 1e-6. Under a pure 1/E flux the ratio equals the atoms/kg ratio to 5 significant figures at every T for every target. Leg quality is labelled: a common constant sigma is used for every target because only Ge has a resonance-resolved cross section here, and the specific artefact risk — 'Ge has more structure' by construction — is named and avoided rather than noted."
      linked_ids: [claim-compression-adjudicated, deliv-compression-table, deliv-compression-report]
    test-cawo4-not-w:
      status: passed
      summary: "Oxygen is 66.67% of CaWO4's atom count against 16.67% each for Ca and W, and carries the largest kinematic factor in the compound at 0.221453, which is 4.13x germanium's. CaWO4 therefore has 1.25458e25 atoms/kg against Ge's 8.29134e24 — 1.51x more. THE SUBSTITUTION CHANGES THE DIRECTION, and that is reported as a finding: Ge/W = 2.29-2.46 across the RoI (Ge worse) while Ge/CaWO4 = 0.673-0.692 (Ge BETTER, by ~1.45x). The roadmap's supporting number is a Ge-vs-W statement standing in for a Ge-vs-CaWO4 one, and the two point opposite ways."
      linked_ids: [claim-compression-adjudicated, deliv-compression-table, deliv-compression-report]
    test-sc4-verdict-recorded:
      status: passed
      summary: "SC4 verdict: SUPERSEDED BY MEASUREMENT, stated in the Phase-12 vocabulary with the measurement attached and split by component — mechanism SUPERSEDED BY MEASUREMENT (f cancels; measured 4.2e-8), direction vs W CONFIRMED but for a different reason (atoms/kg, not compression), direction vs CaWO4 REVERSED under measurement. No band was narrowed: the comparison band is the full 10-100 eV RoI with probes spanning four decades either side. The verdict does not restate the f ratio as if it were the finding; instead it names the 1.6% numerical degeneracy between the f ratio 2.4925 and the atoms/kg ratio 2.5334 and explains why both track A_W/A_Ge."
      linked_ids: [claim-compression-adjudicated, deliv-compression-report, ref-roadmap-sc4]
    test-sigma-slope-measured:
      status: passed
      summary: "Measured and reported BEFORE any continuation was used. Top decade 2-20 MeV, 421 points: sigma_el 1.998519 b -> 1.222782 b, OLS slope -2.667195e-3 b/MeV; last half-decade slope -1.068209e-1 b/MeV. The trend approaching the ceiling is decreasing. The measurement also showed the decade is NOT monotone (peak 2.316993 b at 8 MeV, 34.0% of steps rising), so flat-at-the-ceiling is not on its own an upper bound and a second continuation at the band maximum was added rather than the finding being suppressed. The Phase-12 conclusion was NOT carried over; only its method was."
      linked_ids: [claim-highE-bound, deliv-omission-table, deliv-kinematics-tests, ref-phase12-precedent]
    test-omission-split:
      status: passed
      summary: "Both fractions reported as separate numbers and as separate CSV columns. In-RoI 1.3482e-5 (flat at ceiling) and 2.5546e-5 (flat at band max); T-integrated total 8.905% and 16.874%. They differ by a factor of ~6600, which is the physical result: the flat-box height falls as 1/E_n, so a 1 GeV neutron spreads its recoil over a 53.6 MeV-wide box and deposits almost nothing in a 90 eV-wide RoI while contributing its full cross section to the total."
      linked_ids: [claim-highE-bound, deliv-omission-table, deliv-compression-report]
    test-omission-direction:
      status: passed
      summary: "Two rows in the 09-02 Section 7 schema, both flatters_SB and neither netted: the >20 MeV elastic omission itself (-1.35e-5 to -2.55e-5 in-RoI, -8.91% to -16.87% total), and the elastic-only restriction as a further understatement in the same direction, unquantifiable with the data this project holds because the frozen set is MF=3 MT=2 elastic. The artifact carries elastic_only = true and direction = flatters_SB on every row, and the header names fp-net-omissions and the penalizes_SB central value they are NOT netted against."
      linked_ids: [claim-highE-bound, deliv-omission-table, deliv-compression-report]
    test-ceiling-subsumption:
      status: passed
      summary: "Stated with numbers rather than assumed either way. The committed flux-table top edge is 2.0e8 eV and the sigma_el ceiling 2.0e7 eV, so every neutron above the flux-table ceiling is also above the sigma_el ceiling — SUBSUMED, no double-count. 20.55% of the >10 MeV flux lies above the flux-table ceiling, reproducing 09-02 Section 6.2's recorded 21%, and that is 22.93% of what lies above the sigma_el ceiling. Nothing is dropped either, because the flux-table ceiling is not an independent omission in this channel at all: the fold never reads that table, and the pinned driver reaches 10 GeV."
      linked_ids: [claim-highE-bound, deliv-compression-report, ref-neutron-decl]
    test-calc24-conditional:
      status: passed
      summary: "Evaluated, not skipped, and one branch taken explicitly. Worst total-rate fraction 0.16874 against a label of 2.0 (a factor ~3), so the branch is DEFERRAL SUSTAINED ON THE MEASURED BOUND with a margin of 11.85x. The replacement rationale is written out and cites only the measurement. The branch carries its own falsifier: if nonelastic channels above 20 MeV multiply the elastic-only bound by more than ~12, the branch flips, and this project cannot measure that multiplier."
      linked_ids: [claim-calc24-disposition, deliv-omission-table, deliv-compression-report, ref-requirements-calc24]
    test-void-rationale-not-reused:
      status: passed
      summary: "EXECUTED grep over the report, both artifacts and the module for shield attenuation, the ~5-7x figure, overburden, building moderation and post-shield quantities. Zero hits on any line that does not also carry a void / not-applied / never-used marker, i.e. zero uses as a JUSTIFICATION. The void rationale appears only as a record that it is void."
      linked_ids: [claim-calc24-disposition, deliv-compression-report, deliv-kinematics-tests]
  references:
    ref-roadmap-sc4:
      status: completed
      completed_actions: [read, compare, cite]
      summary: "Read as a REQUIREMENT TO EXHIBIT, not as a pre-established direction — its own wording is 'exhibited, not asserted'. Compared against the measurement: its quoted kinematic factors 0.0215 / 0.0952 / 0.2215 are reproduced from 4A/(1+A)^2 with the dominant natural isotope's mass number to better than 5e-5, and its ~2.5x is reproduced as f_Ge/f_W = 2.4925. Cited in the verdict, which records SUPERSEDED BY MEASUREMENT for the mechanism on the Phase-12 precedent."
      linked_ids: [claim-compression-adjudicated]
    ref-neutron-decl:
      status: completed
      completed_actions: [read, use, cite]
      summary: "Section 5's lethargy-flatness factor 1.390 over 1 eV - 10 keV is recomputed here independently from the pinned driver at 1.3901 and used to establish that the RoI-feeding band sits close to the limit where f provably has no effect. Section 6.2's 21% above the ~197 MeV grid ceiling is reproduced at 20.55% and used in the subsumption analysis; its record that the CALC-24 deferral rationale is VOID at the surface is cited as a record and never as a justification. Section 7's directional-bias schema is the format both omission rows are written in."
      linked_ids: [claim-compression-adjudicated, claim-highE-bound, claim-calc24-disposition]
    ref-elastic-table:
      status: completed
      completed_actions: [read, use, compare]
      summary: "The only sigma_el this project owns. Used for the slope measurement at the ceiling (421 points over the top decade), for both continuation values (1.222782 b at the ceiling, 2.316993 b at the band maximum), and for the Ge resonance-structure factor that is reported separately from every ratio. Compared: its 20 MeV ceiling IS the omission being bounded, and its non-monotonicity over the top decade is what forced a second continuation."
      linked_ids: [claim-highE-bound, claim-compression-adjudicated]
    ref-phase12-precedent:
      status: completed
      completed_actions: [read, use]
      summary: "The METHOD is reused — measure the slope of the quantity approaching the boundary before claiming a flat continuation bounds it — and the CONCLUSION is re-measured rather than carried over. Re-measuring produced a different answer from Phase 12's: there the frozen table was decreasing toward its floor and the flat continuation was conservative outright, whereas here the top decade is decreasing in trend but NOT monotone, so a single flat continuation is not an upper bound and two are reported."
      linked_ids: [claim-highE-bound]
    ref-requirements-calc24:
      status: completed
      completed_actions: [read, cite]
      summary: "Read, and its record that the deferral survives on a DIFFERENT rationale from the void one is what this plan supplies the measurement for. Cited in the disposition, which writes the replacement rationale explicitly against the measured bound and attaches its own falsifier."
      linked_ids: [claim-calc24-disposition]
  forbidden_proxies:
    fp-assert-compression:
      status: rejected
      notes: "The 2.49 ratio is never quoted as the exhibition. It appears only in two places: as the criterion's stated INPUT, and in the section that names it as a 1.6% numerical near-identity with the atoms/kg ratio 2.5334 because both track A_W/A_Ge. The exhibition is the substitution derivation plus the four-f cancellation measurement plus the three-way attribution."
    fp-net-omissions:
      status: rejected
      notes: "The >20 MeV omission and the elastic-only understatement are written as two separate flatters_SB rows in the 09-02 Section 7 schema and are carried alongside the channel's penalizes_SB central value, never subtracted from it. The artifact header names fp-net-omissions explicitly and a test asserts both the flatters_SB and penalizes_SB tokens are present."
    fp-inherit-void-rationale:
      status: rejected
      notes: "Enforced by an executed grep over the report, both artifacts and the module. Zero occurrences of shield attenuation, the ~5-7x figure, overburden or building moderation on any line not also carrying a void / not-applied marker. The replacement rationale cites only the measured bound and the 11.85x margin."
    fp-unchecked-continuation:
      status: rejected
      notes: "The slope was measured before the continuation was used, and the measurement changed the plan: the top decade is not monotone, so a single flat-at-the-ceiling continuation is NOT an upper bound and a second continuation at the band maximum 2.316993 b was added. Reported rather than resolved by taking the smaller number."
    fp-single-omission-number:
      status: rejected
      notes: "In-RoI and total-rate fractions are separate columns in the artifact and separate rows in the report, and they differ by a factor of ~6600. A test asserts both are present and that their ratio exceeds 1e3."
    fp-precision-inflation:
      status: rejected
      notes: "accuracy_label = order_of_magnitude is in both artifact headers and on every emitted row. The many-digit numbers are quadrature reproducibility figures, and the report's conclusions are stated at the level the label supports: 'the kinematic factor contributes nothing at leading order', 'Ge is ~2.3-2.5x worse than W per kg', 'Ge is ~1.45x better than CaWO4 per kg', 'the total-rate omission is under 17%'."
    fp-mass-scaled-target:
      status: rejected
      notes: "Vacuous by construction and asserted anyway: no NUCLEUS residual, no CaWO4 or Al2O3 measured rate, and no target-swap rescale enters this pipeline anywhere. Every target's rate is computed from first principles with that material's own atoms/kg and its own kinematic factors, from the same incident flux. A test asserts the token does not appear in the artifacts or the module except in a negation."
  uncertainty_markers:
    weakest_anchors:
      - "The comparison targets. This repository owns a resonance-resolved sigma_el for Ge only, so every W, Ca, O and CaWO4 leg rests on a common constant cross section. Germanium's own effective sigma_el in this weighting is 8.9-12.1 b and varies by ~20% across the band; an element-dependent factor of that size would move any direction reported here. This is the weakest input in the plan and it cannot be strengthened in this environment."
      - "Everything above the 20 MeV ceiling. There is no cross-section data there at all, and the bound rests entirely on a continuation argument about a quantity measured only below the ceiling — where it is not even monotone."
      - "The elastic-only restriction. Above 20 MeV nonelastic channels are comparable to elastic and produce larger recoils, so the bound understates by an amount this project cannot quantify with the data it holds."
      - "The eV-keV differential shape of the flux, inherited from Plan 13-01. It sets both baselines the omission fractions are divided by."
    unvalidated_assumptions:
      - "That a flat sigma_el continuation is conservative above 20 MeV. The slope below the ceiling is a trend, not a measurement of the continuation, and the top decade contains a local maximum at 8 MeV that shows the trend is not stable over a decade."
      - "That the sea-level flux is close enough to 1/E over the RoI-feeding band for the analytic cancellation to be the dominant effect. The measured lethargy flatness is 1.390, not 1.000, and the flux-shape correction reaches -21% at T = 1 keV."
      - "That mass number is an adequate stand-in for molar mass in the atoms/kg calculation for W, Ca and O. It is exact for the ratio's leading behaviour and wrong by well under 1% for natural abundances, but it was not checked against a frozen table because none exists here for those elements."
    competing_explanations:
      - "A measured Ge-vs-W difference could arise from atoms/kg rather than from kinematics or resonances. It DOES: the pure-1/E control shows the ratio equalling the atoms/kg ratio to five significant figures, so atoms/kg alone accounts for the whole leading-order effect."
      - "It could also arise from the comparison legs being computed with cross sections of unequal quality. That artefact is removed by construction — a common constant sigma is used for every target including Ge — and the size of the term that is therefore missing is reported separately as Ge's own resonance-structure factor."
      - "The in-RoI omission being tiny could reflect either a genuinely small high-energy contribution or a mis-set RoI. It is the former, and the mechanism is stated: the flat-box height falls as 1/E_n, which is checkable independently from the total-rate fraction being 6600x larger."
    disconfirming_observations:
      - "SC4's stated MECHANISM has no leading-order effect at all: the kinematic factor cancels identically out of the fold. Reported as SUPERSEDED BY MEASUREMENT rather than explained away, and it is the fifth roadmap clause of this milestone to fall under measurement."
      - "The Ge-vs-CaWO4 comparison — the statement the roadmap actually makes — comes out in the OPPOSITE direction: Ge is the BETTER neutron target per kg by ~1.45x under a common constant cross section, because oxygen dominates CaWO4's atom count. Reported as a finding, with its conditionality on the constant-sigma assumption stated rather than buried."
      - "sigma_el is NOT monotone over the top decade approaching the ceiling: it peaks at 2.316993 b at 8 MeV and 34.0% of the steps rise. A single flat continuation at the ceiling value is therefore not an upper bound, contrary to what the plan anticipated, and a second continuation was added rather than the finding being suppressed."
      - "The >20 MeV total-rate omission reaches 16.87% under the upper continuation. That is inside the channel's own label, but only by 11.85x on an elastic-only bound whose understatement factor this project cannot measure. The CALC-24 branch is therefore stated with its own falsifier attached rather than as settled."
---

# Plan 13-02 — Summary

Full evidence record: **`13-02-COMPRESSION-AND-OMISSIONS.md`**.

## Headline numbers

| quantity | value |
|---|---|
| `f`-cancellation spread across `f ∈ {0.0215, 0.0536, 0.0952, 0.2215}` | **4.1997×10⁻⁸** (tol 10⁻⁵) |
| lethargy flatness, 1 eV – 10 keV (recomputed) | **1.3901** (09-02 records 1.390) |
| Ge/W matched-T ratio across the RoI | **2.29 – 2.46** |
| — attributable to atoms/kg | **2.53339** (the whole leading effect) |
| — attributable to flux shape | −3.1% to −9.5% |
| — attributable to the kinematic factor | ≤ 1.4×10⁻⁴ (and it is finite-ceiling truncation) |
| Ge/CaWO₄ matched-T ratio across the RoI | **0.673 – 0.692** — Ge is **better** |
| `f_Ge/f_W` vs `n_Ge/n_W` | 2.4925 vs **2.53339** (1.6% apart; both track `A_W/A_Ge`) |
| σ_el slope, top decade / last half-decade | −2.667×10⁻³ / −1.068×10⁻¹ b/MeV |
| σ_el monotone over the top decade? | **No** — peak 2.316993 b at 8 MeV |
| Φ(>20 MeV), pinned driver to 10 GeV | 3.181822×10⁻³ cm⁻² s⁻¹ |
| >20 MeV omission, **in-RoI** | **1.35×10⁻⁵ – 2.55×10⁻⁵** |
| >20 MeV omission, **T-integrated total** | **8.91% – 16.87%** |
| Φ above the 197 MeV table ceiling / Φ(>10 MeV) | 20.55% (09-02 records 21%) |
| CALC-24 margin to the label | **11.85×** |

## SC4 verdict

**SUPERSEDED BY MEASUREMENT** for the mechanism; **CONFIRMED for a different reason** against W;
**REVERSED** against CaWO₄, which is the comparison the roadmap sentence actually names.

## Task 2 checkpoint — `checkpoint:decision`, recorded and continued

The plan marks Task 2 as a decision checkpoint on CALC-24. Under the standing session directive it
is recorded here and execution continued with the recommended branch.

| branch | condition | measured | taken |
|---|---|---|---|
| deferral sustained on the measured bound | total-rate bound inside the order-of-magnitude label (≤ 2.0 fractional) | **0.16874** | **YES** |
| escalate to the user | bound exceeds the label | — | no |

**Replacement rationale (written, not inherited):** the omission is 2.6×10⁻⁵ of the in-RoI rate and
16.9% of the T-integrated total under an *upper* continuation whose conservatism was established by
measuring the cross-section slope at the ceiling; the elastic-only restriction would have to
understate it by more than **11.9×** to reach the label. The Phase-7 premise is recorded as void and
used as a justification nowhere — verified by an executed grep.

## Deviations

- **Rule 4 (missing component, added inline).** The plan assumed one flat continuation. Measuring
  the slope showed the top decade is **not monotone** (local maximum 2.316993 b at 8 MeV), so
  flat-at-the-ceiling is not an upper bound on its own. A second continuation at the band maximum
  was added and both are reported. This strengthens the bound rather than changing the plan's scope.
- **Rule 4.** Disposition rows for the two new tracked `.csv` files were written now rather than in
  Plan 13-03, for the same reason as in 13-01: the register's own test enumerates `git ls-files`.
- **No deviation rule 1, 2, 3, 5 or 6** was applied. No physics redirect and no scope change.

## Findings that cut against expectations

1. **SC4's mechanism has no leading-order effect.** `f` cancels identically. Fifth roadmap clause
   of this milestone to fall under measurement.
2. **The Ge-vs-CaWO₄ direction reverses.** Ge is the *better* neutron target per kg by ~1.45×,
   conditional on the common-σ assumption.
3. **σ_el is not monotone approaching the 20 MeV ceiling.** Reported; a second continuation added.
4. **SC4's ~2.5× is numerically right for the wrong reason.** `f_Ge/f_W = 2.4925` and
   `n_Ge/n_W = 2.5334` agree to 1.6% because both track `A_W/A_Ge`.

## For Plan 13-03

- The channel's directional-bias rows are written and un-netted: `penalizes_SB` central value
  (outdoor leg + Gordon midpoint), `flatters_SB` >20 MeV elastic omission, `flatters_SB`
  elastic-only understatement. Plan 13-03 adds the sub-5 eV row (`flatters_SB` only if truncated —
  Route A was taken, so it does not apply) and hands all of them to Phase 16.
- `neutron_recoil.high_energy_omission_bound()` and `calc24_disposition()` are callable for the
  closeout report's SC5 row.
