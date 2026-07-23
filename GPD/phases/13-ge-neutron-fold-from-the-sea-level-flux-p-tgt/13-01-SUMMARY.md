---
phase: 13-ge-neutron-fold-from-the-sea-level-flux-p-tgt
plan: 01
title: "Anchored flat-box Ge neutron elastic fold to a native-axis dR/dT reaching 100 meV, with the closed-form epithermal oracle reproduced to 4.7e-8 and the kinematic factor cancelling exactly, the 1 eV - 10.14 eV flux gap closed by the pinned PARMA driver, the 102.59 eV resonance imprint demonstrated against a smoothed-sigma control that fails, and the sub-5 eV kernel spliced to NCrystal Ge_sg227"
date: 2026-07-23
status: complete
depth: full
completed: 2026-07-23
provides:
  - "src/qpd_potential/neutron_recoil.py — the Ge neutron elastic recoil fold: frozen-header parsing (f, N_Ge, resonance peak, validation block), the operative phi_default flux with an explicit phi_lo refusal path, the E_min(T)-anchored piecewise-power-law quadrature, the sub-5 eV route switch with an executed free-atom tripwire counter, the closed-form epithermal oracle, the smoothed-sigma control, the imprint statistic, the per-isotope edge cross-check, the anchor-loss diagnostic, and both artifact writers"
  - "artifacts/v2.0/neutron_dRdT_ge.csv — 2812-bin native-axis dR/dT from the 0.0999350 eV floor to 1.072e6 eV, UNBROADENED, with the smoothed-sigma control and the Route-B truncated leg as separate columns and accuracy_label = order_of_magnitude in the header"
  - "artifacts/v2.0/neutron_flux_continuity.csv — pinned-driver vs both committed flux tables on their own nodes, plus 121 driver values inside the 1 eV - 10.14 eV gap neither table covers"
  - "GPD/phases/13-.../13-01-KERNEL-AND-IMPRINT.md — the evidence record: oracle, convergence, anchor loss, imprint with its control, edge measurement, 293.6 K line-shape verdict, sub-5 eV stake table, a1 forward-peaking report, dimensional-check table"
  - "tests/test_neutron_recoil.py — 25 tests covering all 12 contract acceptance tests, tolerances declared as module constants before any check runs"
  - "artifacts/v2.0/legacy_grid_disposition.csv — disposition rows for the two new tracked .csv files"
one_liner: "The Ge neutron nuclear-recoil spectrum exists on a native axis reaching the 0.0999350 eV extended-grid floor, at 1.390e7 counts/kg/day/keV in the bottom bin and 4.419e3 counts/kg/day integrated over the 10-100 eV RoI — 5.9e3 times the Phase-12 CEvNS recoil spectrum at 100 meV (2.3499e3 counts/kg/day/keV) -- a factor of a few thousand, measured rather than rounded up to four orders of magnitude; a background far above the signal is the expected result for an unshielded outdoor surface wafer and it means this channel, not CEvNS, sets S/B; the E_min(T)-anchored quadrature reproduces the closed-form epithermal oracle dR/dT = N sigma C / T to 4.65e-8 with the kinematic factor f cancelling to 4.20e-8 across f in {0.0215, 0.0536, 0.0952, 0.2215}, confirming in code the analytic result Plan 13-02's SC4 adjudication rests on; node doubling moves the real fold by 1.35e-4 against a 0.5% tolerance; an unanchored quadrature costs a median -1.14e-3 and up to -14.6% for the plain-log-grid form, signed negative i.e. flatters_SB; the 1 eV - 10.14 eV gap between the two committed flux tables — which feeds every recoil below 0.544 eV and was recorded nowhere before this phase — is closed by evaluating the pinned PARMA driver directly at every quadrature node, and that driver reproduces both committed tables to 3.88e-6 and 3.88e-12 median, the former being exactly the known anchor-scalar rounding; ROADMAP SC3 is discharged with a slope-excursion statistic of 32.16 against a pre-declared threshold of 5.0 at T = 5.5092 eV while a resonance-integral-preserving smoothed control scores 1.14 and FAILS, a 28x separation stable across 200/400/800 bins per decade; the edge is NOT the anticipated +/-4% isotope-smeared band because 73Ge carries 98.84% of the natural 669.1 b peak alone, so the physically correct edge is 5.4705 eV and the single natural f = 0.0536 misplaces it high by +0.52%, confirmed by an independent five-box per-isotope fold; and the sub-5 eV kernel is spliced to NCrystal Ge_sg227 at 293.6 K with a measured -5.4244% seam step, chosen because truncation would instead drop 57.9% of the bottom bin, with the ENDF free-atom 1/v upturn (59.43 b) provably never evaluated below 5 eV by an executed counter."
plan_contract_ref: GPD/phases/13-ge-neutron-fold-from-the-sea-level-flux-p-tgt/13-01-PLAN.md#/contract

contract_results:
  claims:
    claim-native-fold:
      status: passed
      summary: "dR/dT(T) = N_Ge INT_{T/f}^{2e7 eV} phi_default(E_n) sigma_el(E_n)/(f E_n) dE_n is computed on a 2812-bin native recoil axis whose bottom bin EDGE is exactly 0.0999350 eV, with E_min(T) an EXACT quadrature node for every T and the 23155-point resonance-resolved union grid carried in as exact nodes as well. f = 0.0536 and N_Ge = 8.291565e24 atoms/kg are PARSED from data/endf_nGe_elastic_v1.1.csv's own header (N_Ge derived as 4.4136e22 atoms/cm^3 / 5.323 g/cm^3 x 1000 g/kg; CONVENTIONS D's 8.29e24 agrees to 0.02%), not transcribed. The closed-form epithermal oracle dR/dT = N sigma C / T is reproduced to a worst 4.651e-8 relative at T = 0.1, 10 and 1000 eV, and the kinematic factor cancels to 4.200e-8 across f in {0.0215, 0.0536, 0.0952, 0.2215} — exact rather than merely small because the quadrature integrates a piecewise power law analytically and the epithermal integrand IS a power law. Node doubling 200 -> 400 nodes/decade moves the REAL fold by 1.346e-4 against the 0.5% tolerance. The spectrum is strictly positive and monotonically non-increasing, as a suffix integral of a positive integrand must be. Rates: 1.390e7 counts/kg/day/keV at T = 0.10022 eV, 1.947e5 at 10.025 eV, 2.110e4 at 100.27 eV; 4.419e3 counts/kg/day integrated over the 10-100 eV RoI, 3.130e4 over the full axis."
      linked_ids: [deliv-module, deliv-dRdT-table, deliv-kernel-report, deliv-tests, test-oracle, test-convergence, test-anchor-loss, test-dimensions, ref-elastic-table, ref-flux-table, ref-conventions-B]
      evidence:
        - verifier: gpd-executor
          method: "closed-form oracle reproduction with an analytic derivation re-done in the report, plus node-doubling convergence and an anchored-vs-unanchored differential that must not vanish"
          confidence: high
          claim_id: claim-native-fold
          deliverable_id: deliv-dRdT-table
          acceptance_test_id: test-oracle
          reference_id: ref-elastic-table
          forbidden_proxy_id: fp-unanchored-quadrature
          evidence_path: GPD/phases/13-ge-neutron-fold-from-the-sea-level-flux-p-tgt/13-01-KERNEL-AND-IMPRINT.md
    claim-resonance-imprint:
      status: passed
      summary: "ROADMAP SC3 discharged on the recoil axis. The statistic is the log-log slope EXCURSION, max|dln(dR/dT)/dlnT| - median|...| over T in [1, 5.6] eV, with threshold 5.0 declared as a module constant BEFORE the run and justified analytically (in the pure epithermal limit dR/dT ~ 1/T, slope exactly -1, excursion exactly 0). REAL spectrum: 32.160 at T = 5.5092 eV -> PASS. CONTROL, the same fold against a sigma_el smoothed by a normalised Gaussian of lethargy width 0.35 applied to sigma*E in ln E, preserving INT sigma dE over 0.1 keV-1 MeV to +1.034%: 1.143 -> FAILS, as it must. Separation 28.1x, and the verdict is identical at 200, 400 and 800 bins/decade (real 25.99/32.16/33.89 converging from below as the ~1.9%-wide edge resolves; control flat at 1.142/1.143/1.143), which excludes the binning-artefact explanation. A curvature statistic was tried first and REJECTED because its absolute magnitude scales as 1/(Delta ln T); a boxcar smoother was rejected because it created its own window-edge structure. EDGE MEASURED, NOT ASSERTED, and the plan's anticipation of a +/-4% smearing band is REFUTED: 73Ge carries 8533.0 b of the 669.096 b abundance-weighted natural peak, i.e. 98.84% of it, so the edge is a single line and not a smeared band. Physically correct edge = 73Ge's own 4A/(1+A)^2 = 0.053324 x 102.59 eV = 5.4705 eV; the single natural f = 0.0536 places it at 5.4988 eV, high by +0.52%. An independent five-box per-isotope fold locates 5.4854 eV against the single-f fold's 5.5171 eV at 800 bins/decade — the edge moves DOWN by 0.32% in the predicted direction and by the predicted amount. Reconstructing 669.096 b from the per-isotope file x IUPAC abundances against the natural header's 669.10 b agrees to 6e-6, an independent cross-check on both frozen files. The 293.6 K line-shape question is ANSWERED: the line is natural-width dominated (observed FWHM 1.923 eV vs Doppler width sqrt(4 E kT/A) = 0.377 eV at 293.6 K, 0.0070 eV at 0.1 K), the statistic's amplitude is set by INT sigma dE which Doppler conserves to 2.54e-4%, and its location by E_res which Doppler does not move — so the 293.6 K set is ADEQUATE for an existence claim, and a 0.1 K re-derivation would only SHARPEN the edge and RAISE the excursion, making 32.16 the conservative value. It would NOT be adequate for a claim about the edge's width."
      linked_ids: [deliv-module, deliv-dRdT-table, deliv-kernel-report, deliv-tests, test-imprint-present, test-imprint-rejects-smooth, test-edge-smearing, ref-elastic-table, ref-per-isotope]
      evidence:
        - verifier: gpd-executor
          method: "falsifiable statistic evaluated on the real spectrum and on a resonance-integral-preserving smoothed control folded through the identical chain, at three grid resolutions"
          confidence: high
          claim_id: claim-resonance-imprint
          deliverable_id: deliv-kernel-report
          acceptance_test_id: test-imprint-rejects-smooth
          reference_id: ref-per-isotope
          forbidden_proxy_id: fp-imprint-unfalsifiable
          evidence_path: artifacts/v2.0/neutron_dRdT_ge.csv
    claim-sub5ev-disposition:
      status: passed
      summary: "ROADMAP SC5 first half discharged. EXACTLY ONE route is declared — Route A, the NCrystal 4.4.6 Ge_sg227 bound-atom splice at 5 eV — in the module constant SUB5EV_ROUTE_DECLARED, in the emitted table header (sub5eV_disposition = ncrystal_splice) and in the report. MEASURED seam discontinuity at 5.0 eV: ENDF free-atom 8.843837 b vs NCrystal bound 8.364108 b, step -5.4244%. NCrystal is evaluated at 293.6 K to MATCH the frozen ENDF set's own processing temperature, so the seam step is a free-vs-bound step and not a temperature step. THE ARGUMENT IS FROM MEASURED STAKES: truncation at the seam (Route B) would drop 57.88% of the bottom bin, 32.31% of the 0.1002-0.268 eV band and 1.487% of the full-axis rate; Route A's residual model uncertainty — bound vs free-atom sigma over the only band that matters, E_n in [1.87, 5] eV — moves the bottom bin by +3.49% and the full-axis rate by +0.09%. The escalation rule was EVALUATED, not skipped: the fraction of the 10-100 eV in-RoI rate carried by sub-5 eV neutrons is EXACTLY ZERO by kinematics (a neutron below 5 eV cannot make a recoil above f x 5 eV = 0.268 eV), so the ~3x escalation criterion is not triggered on its stated terms; the informative number reported alongside it is Route B's 57.9% bottom-bin loss, a factor 2.37 that is comparable to but below the channel's own order-of-magnitude label. fp-free-gas-below-5ev is enforced in CODE: every evaluation of the raw ENDF interpolator below 5 eV increments a module counter, an executed test asserts it is 0 under both admissible routes and >0 under the forbidden one, so the guard is shown non-vacuous. The tripwire is measured, not quoted: the free-atom 1/v upturn reaches 59.4274 b at the bottom of the frozen table. Flat-box consistency with a bound cross section is argued from the axis itself: the lowest incident energy any recoil on this axis needs is E_min(0.0999350 eV) = 1.8645 eV, whose T_max = 0.0999 eV is 5.6x the locked omega_bar = 17.8597 meV, so the impulse approximation holds throughout and CONVENTIONS J's crystal-coherent regime (<~21 meV) lies entirely below the grid floor. The rate is never multiplied by exp(-2W)."
      linked_ids: [deliv-module, deliv-kernel-report, deliv-tests, test-no-freegas-below-5ev, test-sub5ev-route-declared, test-sub5ev-band-bound, ref-elastic-table, ref-ncrystal, ref-conventions-J]
      evidence:
        - verifier: gpd-executor
          method: "all three routes folded end to end and integrated over four bands before the route was chosen, plus an executed evaluation counter on the forbidden path"
          confidence: high
          claim_id: claim-sub5ev-disposition
          deliverable_id: deliv-module
          acceptance_test_id: test-no-freegas-below-5ev
          reference_id: ref-ncrystal
          forbidden_proxy_id: fp-free-gas-below-5ev
          evidence_path: GPD/phases/13-ge-neutron-fold-from-the-sea-level-flux-p-tgt/13-01-KERNEL-AND-IMPRINT.md
    claim-flux-continuity:
      status: passed
      summary: "The gap is REAL and was recorded nowhere before this phase: data/ambient_neutron_thermal_v2.0.csv's top node is 1.0 eV and data/ambient_neutron_flux_v1.1.csv's lowest bin EDGE is 10.0 eV (first centre 10.144972680282425 eV). Zero nodes of either committed table lie strictly inside it — asserted, not assumed. Recoils below T = f x 10.145 eV = 0.54377 eV are fed partly from inside the gap. It is closed by evaluating the pinned PARMA driver (commit 6ff37ca, k = 1.09610) DIRECTLY at every quadrature node; neither committed table is interpolated or extrapolated across it, and the committed tables are used only as cross-checks. Driver vs v1.1 at its own 584 bin centres: median -3.876e-6, max|.| 3.883e-6, 0 bins above 1% or 5%. Driver vs thermal_v2.0 at its own 201 nodes: median -3.885e-12, max|.| 3.483e-10. Both inside the 09-02 Section 3.3 tolerances of 1% median / 5% max, reused unchanged. The v1.1 deviation is UNIFORM and matches the recorded 3.88e-6 anchor-scalar rounding explanation (committed table built with the unrounded k = 1.0961043 against the module's 1.09610) to better than 20%, and the module asserts that pattern rather than smoothing it over; the thermal residual is CSV round-trip only because this driver wrote that table."
      linked_ids: [deliv-continuity-table, deliv-kernel-report, deliv-tests, test-flux-overlap, test-gap-closed, ref-neutron-decl, ref-flux-table]
      evidence:
        - verifier: gpd-executor
          method: "pointwise recomputation of the pinned driver at both committed tables' own nodes, with the deviation pattern classified rather than only bounded"
          confidence: high
          claim_id: claim-flux-continuity
          deliverable_id: deliv-continuity-table
          acceptance_test_id: test-flux-overlap
          reference_id: ref-neutron-decl
          forbidden_proxy_id: fp-indoor-band-as-central
          evidence_path: artifacts/v2.0/neutron_flux_continuity.csv
  deliverables:
    deliv-module:
      status: passed
      path: src/qpd_potential/neutron_recoil.py
      summary: "E_min(T) = T/f with f parsed from the frozen table header by elastic_header(); quadrature_nodes() puts E_min(T) and the 23155 union-grid points in as exact nodes; neutron_flux_cm2_s_MeV() selects phi_default BY NAME and raises FluxColumnError for phi_lo, phi_lo_cm2_s_MeV, indoor, midpoint, band_midpoint, phi_mid, phi_band_midpoint and geometric_mean; epithermal_oracle_dRdT() and fold_synthetic_epithermal() are the callable oracle pair for the test suite; loglog_segment_integrals() integrates a piecewise power law in the numerically stable (y2 x2 - y1 x1)/(p+1) form that never constructs the overflowing prefactor. Also carries the sub-5 eV route switch with its evaluation counter, the smoothed-sigma control, the imprint statistic, the per-isotope edge fold, the anchor-loss diagnostic, the a1 forward-peaking report, flux_above_ceiling() for Plan 13-02, and both artifact writers."
      linked_ids: [claim-native-fold, claim-resonance-imprint, claim-sub5ev-disposition, claim-flux-continuity]
    deliv-dRdT-table:
      status: passed
      path: artifacts/v2.0/neutron_dRdT_ge.csv
      summary: "2812 log bins at 400 bins/decade, bottom bin EDGE exactly 0.0999350 eV and top edge f x 2e7 eV = 1.072e6 eV, knots at the geometric bin centres so ia_broadening.native_edges reproduces the edges. Columns T_eV_nr, dRdT, dRdT_smoothed_control (the SC3 control, explicitly labelled NOT a result), dRdT_sub5eV_truncated (the Route-B leg kept for the omission bound), accuracy_label. Header carries accuracy_label = order_of_magnitude, flux_column = phi_default (outdoor) with phi_lo NOT USED, f = 0.0536 with its parsed provenance line and the per-isotope values, both truncation energies, sub5eV_disposition = ncrystal_splice with the measured -5.4244% seam step, the imprint result with its control, the carrying isotope, and the git sha. UNBROADENED by construction."
      linked_ids: [claim-native-fold, claim-resonance-imprint, test-imprint-present]
    deliv-continuity-table:
      status: passed
      path: artifacts/v2.0/neutron_flux_continuity.csv
      summary: "785 overlap rows (201 thermal + 584 v1.1) carrying driver value, committed-table value and their relative deviation, plus 121 driver-only rows spanning 1 eV - 10.145 eV where neither committed table has data. Header states the gap, why it matters (recoils below 0.54377 eV), how it was closed, and the full overlap statistics against the 09-02 Section 3.3 tolerances."
      linked_ids: [claim-flux-continuity, test-flux-overlap, test-gap-closed]
    deliv-kernel-report:
      status: passed
      path: GPD/phases/13-ge-neutron-fold-from-the-sea-level-flux-p-tgt/13-01-KERNEL-AND-IMPRINT.md
      summary: "Complete evidence record in 11 sections: dimensional-check table with the four named conversion constants, the oracle derivation re-done plus its four-f reproduction table, the three-step convergence ladder, the four-variant anchor-loss table with per-T detail and both degenerate cases explained, the flux-gap and overlap tables, the spectrum table with band integrals and the order-of-magnitude comparison against Phase-12 CEvNS, the imprint section including what was tried and rejected, the per-isotope edge measurement with its independent five-box cross-check, the 293.6 K line-shape verdict with measured widths, the three-route sub-5 eV stake table with the escalation rule evaluated, the a1 forward-peaking table with its bias direction, the acceptance-test discharge table, and a closing section on what still cuts against the result."
      linked_ids: [claim-native-fold, claim-resonance-imprint, claim-sub5ev-disposition, claim-flux-continuity]
    deliv-tests:
      status: passed
      path: tests/test_neutron_recoil.py
      summary: "25 tests, all passing. Every tolerance is a module constant declared at the top before any check runs — ORACLE_REL_TOL 1e-3, ORACLE_F_SPREAD_TOL 1e-5, CONVERGENCE_TOL 5e-3, ANCHOR_LOSS_MIN_MAGNITUDE 1e-4, FLUX_MEDIAN_TOL 0.01, FLUX_MAX_TOL 0.05, CONTROL_RESONANCE_INTEGRAL_TOL 0.05, SUB5EV_ESCALATION_FACTOR 3.0, DIMENSIONAL_SCALING_TOL 1e-12 — and none was loosened afterwards. Includes a non-vacuity test on the free-atom counter, a resolution-stability test on the imprint verdict, an independent per-isotope edge fold, and a reuse of the Phase-9 shielded-token machinery from tests/test_env_v1_identity.py rather than a private token list."
      linked_ids: [claim-native-fold, claim-resonance-imprint, claim-sub5ev-disposition, claim-flux-continuity]
  acceptance_tests:
    test-oracle:
      status: passed
      summary: "Synthetic phi = C/E with constant sigma reproduces dR/dT = N_Ge sigma C / T to a worst 4.651e-8 relative at T = 0.1, 10, 1000 eV, against the <=1e-3 pass condition. Max spread across f in {0.0215, 0.0536, 0.0952, 0.2215} is 4.200e-8 against the <=1e-5 f-cancellation condition — the residual is the finite-E_top truncation term T/(f E_top), the only f-dependence the construction can have, held below 1e-7 by taking E_top = 1e12 eV for the synthetic leg."
      linked_ids: [claim-native-fold, deliv-module, deliv-tests, deliv-kernel-report]
    test-convergence:
      status: passed
      summary: "Real inputs, 60 log T points from the floor to 10 keV. Max relative change 6.887e-5 (100->200 nodes/decade), 1.346e-4 (200->400), 1.374e-5 (400->800), against the 0.5% tolerance. Production runs at 200/decade on top of the 23155 frozen union-grid nodes."
      linked_ids: [claim-native-fold, deliv-module, deliv-tests, deliv-kernel-report]
    test-anchor-loss:
      status: passed
      summary: "Signed (unanchored - anchored)/anchored is NOT zero: median -1.138e-3 with the union nodes retained at 200/decade, worst point -9.544e-3; median -2.197e-2 and worst -1.464e-1 for the plain log grid at 50 nodes/decade with the union nodes also dropped. The sign is systematically negative, so an unanchored quadrature UNDERSTATES this background — a flatters_SB direction. Two degenerate points are reported rather than hidden: at T = 0.1 eV the difference is ~1e-11 because E_min there is the node set's own lower bound and is a node under either rule, and the plain-grid variant can overshoot by up to +1.0% where it straddles a resonance, which is a second failure mode of the same forbidden proxy."
      linked_ids: [claim-native-fold, deliv-kernel-report, deliv-tests]
    test-dimensions:
      status: passed
      summary: "kg^-1 x (cm^-2 s^-1 MeV^-1 / EV_PER_MEV) x (barn x BARN_TO_CM2) x eV^-1 x eV = kg^-1 s^-1 eV^-1, then x SECONDS_PER_DAY x EV_PER_KEV = counts/kg/day/keV. Those four are the only numerical conversion constants in the module and their values are asserted. The executable half verifies that N_Ge and sigma_el each enter linearly to 1e-12 relative, and that C and sigma enter linearly and T as 1/T in the oracle."
      linked_ids: [claim-native-fold, deliv-kernel-report]
    test-imprint-present:
      status: passed
      summary: "Slope excursion 32.160 against the pre-declared threshold 5.0, located at T = 5.5092 eV, inside the isotope window [5.2601, 5.6983] eV. Verdict unchanged at 200, 400 and 800 bins/decade."
      linked_ids: [claim-resonance-imprint, deliv-dRdT-table, deliv-tests, deliv-kernel-report]
    test-imprint-rejects-smooth:
      status: passed
      summary: "The resonance-integral-preserving smoothed control scores 1.143 and FAILS the same threshold the real spectrum passes at 32.160 — a 28.1x separation, stable at all three grid resolutions. The control is fair: same flux, same fold, same sub-5 eV route, and INT sigma dE over 0.1 keV-1 MeV preserved to +1.034% against the declared 5% tolerance."
      linked_ids: [claim-resonance-imprint, deliv-tests, deliv-kernel-report]
    test-edge-smearing:
      status: passed
      summary: "The report quotes the edge as a measured band and names the carrier: 73Ge, 8533.0 b, 98.84% of the 669.096 b abundance-weighted natural peak. Because a single isotope carries the line the anticipated +/-4% smearing is NOT the physical width of the feature — the physically correct edge is 5.4705 eV from 73Ge's own f = 0.053324 and the single natural f = 0.0536 misplaces it high by +0.52%; the [5.2601, 5.6983] eV window is the systematic scale of the single-f stand-in, not a line width. An independent five-box per-isotope fold at 800 bins/decade locates 5.4854 eV against the single-f 5.5171 eV, moving down by 0.32% in the predicted direction."
      linked_ids: [claim-resonance-imprint, deliv-kernel-report, deliv-tests]
    test-no-freegas-below-5ev:
      status: passed
      summary: "EXECUTED guard, not inspection. A module counter increments on every evaluation of the raw ENDF free-atom interpolator below 5 eV. The production fold under ncrystal_splice and under truncate leaves it at exactly 0; the forbidden free_gas route drives it above 0, so the guard is demonstrated non-vacuous. The tripwire constant is measured from the frozen table rather than quoted: 59.4274 b at the bottom of its range."
      linked_ids: [claim-sub5ev-disposition, deliv-tests, deliv-module]
    test-sub5ev-route-declared:
      status: passed
      summary: "Exactly one route declared — ncrystal_splice — in SUB5EV_ROUTE_DECLARED, in the emitted table header and in the report, with the seam discontinuity reported as a number: ENDF 8.843837 b vs NCrystal 8.364108 b at 5.0 eV, step -5.4244%. The argument cites in-phase measurements (Route B drops 57.9% of the bottom bin; Route A's bound-vs-free residual is +3.49% there) rather than convenience."
      linked_ids: [claim-sub5ev-disposition, deliv-dRdT-table, deliv-kernel-report]
    test-sub5ev-band-bound:
      status: passed
      summary: "The T < 0.268 eV band's contribution to the 10-100 eV in-RoI rate is EXACTLY ZERO by kinematics, so the ~3x escalation criterion is not met and no escalation is warranted on its stated terms. Because that answer is true but uninformative for a sub-eV milestone, the operative numbers are reported with their sign: Route B would remove 57.88% of the bottom bin, 32.31% of the 0.1002-0.268 eV band, 12.44% of the sub-eV band and 1.487% of the full-axis rate, all flatters_SB; Route A's residual bound-vs-free-atom model uncertainty is +3.49% at the bottom bin and +0.09% on the full axis."
      linked_ids: [claim-sub5ev-disposition, deliv-kernel-report, deliv-tests]
    test-flux-overlap:
      status: passed
      summary: "Driver vs v1.1 at 584 bin centres: median -3.876e-6, max|.| 3.883e-6, 0 bins over 1% or 5%. Driver vs thermal_v2.0 at 201 nodes: median -3.885e-12, max|.| 3.483e-10, 0 over either bound. Both inside the reused 09-02 Section 3.3 tolerances. The v1.1 pattern is uniform and IS the known anchor-scalar rounding; that identification is asserted in code, not left as prose."
      linked_ids: [claim-flux-continuity, deliv-continuity-table, deliv-tests, ref-neutron-decl]
    test-gap-closed:
      status: passed
      summary: "Zero nodes of either committed table lie strictly inside 1-10 eV, so no interpolation of either table could span the gap without extrapolating both. The driver returns finite positive flux across the whole gap. For every T on the axis below 0.544 eV, E_min(T) itself lands inside the gap, and the production node set carries more than ten driver nodes there. The emitted table header names the gap and how it was closed."
      linked_ids: [claim-flux-continuity, deliv-continuity-table, deliv-module, deliv-tests]
  references:
    ref-neutron-decl:
      status: completed
      completed_actions: [read, use, cite]
      summary: "Sections 3.3, 3.4, 4, 5 and 6 read and used. Section 3.3's 1%/5% tolerances and its 3.88e-6 k-rounding explanation are reused verbatim as this plan's flux-overlap pass condition and as an asserted deviation pattern. Section 3.4's argument is the reason accuracy_label = order_of_magnitude appears on every artifact header. Section 4's phi_lo-is-an-indoor-leg semantics are implemented as an explicit refusal path. Section 5's lethargy-flatness factor 1.390 over 1 eV - 10 keV is what makes the epithermal cancellation the leading-order behaviour, which Plan 13-02 acts on."
      linked_ids: [claim-native-fold, claim-flux-continuity, claim-sub5ev-disposition]
    ref-elastic-table:
      status: completed
      completed_actions: [read, use, compare]
      summary: "f = 0.0536, the per-isotope 4A/(1+A)^2 set, N_Ge = 4.4136e22 atoms/cm^3 with rho = 5.323 g/cm^3, the 1.031e-05 eV validity floor, the 669.10 b / 102.59 eV resonance peak, the 293.6 K processing temperature, the mesh/Doppler/ACE validation numbers and git_sha f742c63 are ALL parsed from this file's own header by elastic_header(). The 23155-point union grid is used as exact quadrature nodes. Compared: the reconstructed abundance-weighted peak 669.096 b against the header's 669.10 b agrees to 6e-6, and each parsed per-isotope f against 4A/(1+A)^2 to better than 5e-5."
      linked_ids: [claim-native-fold, claim-resonance-imprint, claim-sub5ev-disposition]
    ref-per-isotope:
      status: completed
      completed_actions: [read, compare]
      summary: "Read to identify which isotope carries the 102.59 eV resonance and to run an independent five-box per-isotope fold. Result: 73Ge, 8533.0 b, 98.84% of the natural peak — which REFUTES the plan's premise that the edge is smeared by +/-4% across five box widths, and replaces it with a measured +0.52% single-f misplacement confirmed by the independent fold."
      linked_ids: [claim-resonance-imprint]
    ref-flux-table:
      status: completed
      completed_actions: [read, use]
      summary: "Both committed tables read at their own nodes for the overlap comparison, and their supports measured to establish the gap (thermal top 1.0 eV, v1.1 lowest edge 10.0 eV, lowest centre 10.144972680282425 eV). Neither is used as the fold's flux source: the pinned driver is evaluated directly. read_flux_v11 deliberately does not return phi_lo."
      linked_ids: [claim-native-fold, claim-flux-continuity]
    ref-conventions-B:
      status: completed
      completed_actions: [read, use]
      summary: "The recoil axis is keV_nr on the unified phonon scale with no Lindhard and no quenching, restated in the module header and in every emitted artifact header. Section D's per-kg normalization is used, with N_Ge derived from the frozen table's own numbers and cross-checked against the 8.29e24 test value to 0.02%."
      linked_ids: [claim-native-fold]
    ref-conventions-J:
      status: completed
      completed_actions: [read, avoid]
      summary: "Read to bound what the NCrystal route may claim. Used to establish that the crystal-coherent regime (<~21 meV) lies entirely below the 0.0999350 eV grid floor: the lowest incident energy any recoil on this axis needs is 1.8645 eV, whose T_max = 0.0999 eV is 5.6x the locked omega_bar = 17.8597 meV, so the impulse approximation holds throughout and splicing a bound cross section under a free-atom flat box is consistent. AVOIDED: the rate is never multiplied by exp(-2W) anywhere in this plan."
      linked_ids: [claim-sub5ev-disposition]
    ref-ncrystal:
      status: completed
      completed_actions: [read, use]
      summary: "NCrystal 4.4.6 verified present and loaded as Ge_sg227.ncmat;temp=293.6K — the temperature chosen to MATCH the frozen ENDF set's own 293.6 K processing so the measured seam step is free-vs-bound and not free-vs-cold. Used as the declared sub-5 eV kernel, giving 8.364108 b at the 5 eV seam against ENDF's 8.843837 b."
      linked_ids: [claim-sub5ev-disposition]
  forbidden_proxies:
    fp-unanchored-quadrature:
      status: rejected
      notes: "E_min(T) is an exact quadrature node for every T by construction in quadrature_nodes(). The cost of the proxy is a measured number rather than a warning: median -1.14e-3 for the endpoint effect alone and up to -14.6% for the plain log-substituted grid, signed negative throughout, so the proxy would have understated this background."
    fp-indoor-band-as-central:
      status: rejected
      notes: "phi_lo, phi_lo_cm2_s_MeV, indoor, midpoint, band_midpoint, phi_mid, phi_band_midpoint and geometric_mean all raise FluxColumnError. Tested. read_flux_v11 does not even return the phi_lo column. A line-level scan asserts phi_lo appears in the module and artifacts only inside a definition or a refusal."
    fp-free-gas-below-5ev:
      status: rejected
      notes: "Enforced by an executed evaluation counter, not by discipline: 0 free-atom evaluations below 5 eV reach the emitted spectrum under either admissible route, and >0 under the forbidden route so the counter is demonstrated non-vacuous. The 1/v upturn it protects against is measured at 59.4274 b."
    fp-smooth-as-result:
      status: rejected
      notes: "The 23155-point resonance-resolved union grid is carried into the quadrature as exact nodes, and the emitted spectrum shows a slope excursion of 32.16 at the 5.5092 eV kinematic edge. The smoothed spectrum exists in the artifact only as an explicitly labelled CONTROL column, and the header says so."
    fp-imprint-unfalsifiable:
      status: rejected
      notes: "The control FAILS the statistic the real spectrum passes, by 28.1x, at three grid resolutions. A curvature statistic that both would have passed in resolution-dependent absolute terms was REPLACED rather than reinterpreted, and that replacement is recorded in the report."
    fp-quote-from-prose:
      status: rejected
      notes: "0.0536, 669.10 b, 102.59 eV, 59.43 b and 8.29e24 are all parsed or derived from frozen artifacts by elastic_header(), free_atom_tripwire_b() and n_ge_per_kg(). A test asserts the parsed strings are literally present in the frozen file and that the derived N_Ge matches CONVENTIONS D."
    fp-shielded-quantity-leak:
      status: rejected
      notes: "The Phase-9 shielded-token machinery (SHIELDED_TOKENS, is_not_applied) from tests/test_env_v1_identity.py is run over the module and both artifacts and returns zero APPLIED hits. No NUCLEUS attenuation factor, post-shield fluence, overburden depth, buildup factor, veto credit or multiplicity credit appears; veto credit is exactly 1.0 by construction."
    fp-precision-inflation:
      status: rejected
      notes: "accuracy_label = order_of_magnitude appears in both artifact headers and on every emitted row, and the report states at the top and at the bottom that everything inherits it from a flux whose eV-keV differential shape has no independent validation. The many-digit numbers quoted here are REPRODUCIBILITY figures for the quadrature and the parsing, explicitly not accuracy figures — the same distinction 09-02 Section 3.4 draws."
  uncertainty_markers:
    weakest_anchors:
      - "The eV-keV differential shape of the sea-level neutron flux. It carries no independent validation, none is obtainable in this environment, and it is precisely the band that sets the in-RoI Ge recoil rate. Two spectra can share the >10 MeV Gordon integral and differ badly here."
      - "The 1 eV - 10.14 eV band, reachable only through the PARMA driver, which feeds every recoil below 0.544 eV — the sub-eV region this milestone exists to reach. The driver reproduces both committed tables where they exist, but nothing checks it where they do not."
      - "The isotropic-CM flat box. a1 is carried but not applied; contribution-weighted <a1> is 3.4e-3 at T = 100 eV but 0.55 at T = 1e5 eV, so the flat box overstates the high-T end of each box three decades above the RoI."
      - "The 293.6 K free-gas processing against a mK cryogenic target. Adequate for the imprint EXISTENCE claim (measured in-phase) and inadequate for any claim about the edge's width."
      - "NCrystal's bound kernel is used only in its 1.87-5 eV tail. It is the right cross section there, but it is a different evaluation from the ENDF set above the seam, and the -5.42% seam step is the honest measure of that."
    unvalidated_assumptions:
      - "That a single abundance-weighted f = 0.0536 adequately represents five isotopes with distinct box widths. Measured consequence: the kinematic edge is biased high by +0.52%, confirmed by an independent per-isotope fold. Not corrected, because correcting it would abandon the frozen Phase-7 kernel."
      - "That the Gordon >10 MeV integral anchor, applied as an energy-independent scalar k, is an acceptable normalization for the epithermal band where the RoI rate is actually generated."
      - "That linear interpolation of sigma_el between the frozen union-grid nodes is the correct reconstruction. It matches NJOY's own lin-lin linearisation to err = 1e-3, but that is an argument from the producer's convention rather than a measurement."
    competing_explanations:
      - "Structure below 5.5 eV could originate in quadrature node placement or flux-table handling rather than in the Ge resonance. Separated by the smoothed-sigma control, which is folded through the identical chain and fails; and by the resolution-stability check, which leaves the verdict unchanged at 200, 400 and 800 bins/decade."
      - "The located edge could be a coincidence of binning rather than the kinematic threshold. Separated by the independent five-box per-isotope fold, which moves the edge to 5.4854 eV in the direction and by the amount 73Ge's own f predicts."
    disconfirming_observations:
      - "REFUTED IN-PHASE: the plan's premise that the kinematic edge is smeared by +/-4% across five isotope box widths. 73Ge carries 98.84% of the natural peak alone, so the edge is a single line; the +/-4% window is the systematic scale of the single-f stand-in, not a physical width. Reported as a finding rather than absorbed."
      - "The sub-5 eV band's contribution to the in-RoI rate is exactly zero, so test-sub5ev-band-bound's stated escalation criterion cannot fire at all. The criterion was answered on its own terms and then supplemented with the number that actually matters (57.9% of the bottom bin under Route B), rather than the zero being reported as if it settled the question."
      - "The anchor-loss check returns ~1e-11 at T = 0.1 eV, which in isolation would look like the failure condition the plan names. It is a degenerate point — E_min there is the node set's own lower bound — and is reported as such rather than dropped from the table."
      - "This neutron channel sits 5.9e3 times the Phase-12 CEvNS recoil spectrum at 100 meV (2.3499e3 counts/kg/day/keV) -- a factor of a few thousand, measured rather than rounded up to four orders of magnitude. If that survives Plan 13-03's response chain, S/B in the sub-eV region is set by neutrons and not by the signal, which is a harder result for the milestone's headline than the RoI-only comparison would suggest."
---

# Plan 13-01 — Summary

## What was done

Built `src/qpd_potential/neutron_recoil.py` and folded the operative outdoor sea-level neutron
flux against the frozen resonance-resolved n-Ge elastic set through the Phase-7 flat-box kernel,
onto a native recoil axis reaching the Phase-10 extended-grid floor at 0.0999350 eV.

Full evidence record: **`13-01-KERNEL-AND-IMPRINT.md`**.

## Headline numbers

| quantity | value |
|---|---|
| dR/dT at the bottom bin (T = 0.10022 eV) | **1.390×10⁷ counts kg⁻¹ day⁻¹ keV⁻¹** |
| dR/dT at T = 10.025 eV | 1.947×10⁵ |
| dR/dT at T = 100.27 eV | 2.110×10⁴ |
| integrated 10–100 eV RoI | **4.419×10³ counts kg⁻¹ day⁻¹** |
| integrated over the whole axis | 3.130×10⁴ counts kg⁻¹ day⁻¹ |
| oracle reproduction / `f`-cancellation | 4.651×10⁻⁸ / 4.200×10⁻⁸ |
| node-doubling convergence | 1.346×10⁻⁴ (tolerance 0.5%) |
| unanchored-quadrature cost | median −1.14×10⁻³, worst −14.6% |
| imprint statistic, real vs smoothed control | **32.160 vs 1.143** (threshold 5.0) |
| kinematic edge, 73Ge's own `f` vs single natural `f` | 5.4705 eV vs 5.4988 eV (+0.52%) |
| 5 eV seam step, NCrystal bound vs ENDF free-atom | **−5.4244%** |
| Route-B truncation cost at the bottom bin | **−57.88%** |
| driver vs committed flux tables (median) | −3.876×10⁻⁶ (v1.1), −3.885×10⁻¹² (thermal) |

## Task 3 checkpoint — `checkpoint:decision`, recorded and continued

The plan marks Task 3 as a decision checkpoint. Under the standing session directive it is
recorded here and execution continued with the recommended option.

**Decision: Route A — NCrystal `Ge_sg227` splice at 5 eV.**

| | Route A (NCrystal splice) | Route B (truncate) | forbidden (free-gas) |
|---|---|---|---|
| bottom-bin dR/dT | 1.390×10⁷ | 5.855×10⁶ | 1.439×10⁷ |
| bottom-bin cost vs Route A | — | **−57.88%** | +3.49% |
| 0.1002–0.268 eV band cost | — | −32.31% | +1.91% |
| full-axis cost | — | −1.487% | +0.088% |
| in-RoI (10–100 eV) cost | — | **exactly 0** | exactly 0 |
| its own reported defect | seam step −5.4244% | a 57.9% documented omission at the floor | uses a data-format artefact as physics |

Route A costs a −5.42% discontinuity in the cross section at one energy. Route B costs 57.9% of
the rate in the bottom bin — a factor 2.37, comparable to the channel's own order-of-magnitude
label, in exactly the region this milestone exists to reach. Route A is taken. The escalation
rule was evaluated: on its stated in-RoI criterion nothing escalates, because sub-5 eV neutrons
cannot reach a 10–100 eV RoI at all.

## Deviations

- **Rule 4 (missing component, added inline).** The plan defers the
  `artifacts/v2.0/legacy_grid_disposition.csv` rows to Plan 13-03. But
  `tests/test_legacy_grid_disposition.py` enumerates `git ls-files`, so committing the two new
  tracked `.csv` files without rows would break the suite at this commit. The two rows for
  `neutron_dRdT_ge.csv` and `neutron_flux_continuity.csv` were therefore written now. Plan 13-03
  adds the remaining rows for its own artifacts, as planned.
- **No physics deviation.** No deviation rule 1, 2, 3, 5 or 6 was applied.

## Findings that cut against the plan's own expectations

1. **The kinematic edge is not a ±4% smeared band.** 73Ge carries 98.84% of the natural 669.1 b
   peak, so the resonance edge is a single line at 5.4705 eV. The plan's anticipated smearing is
   the *systematic scale of the single-`f` stand-in*, not a physical width. Confirmed by an
   independent five-box per-isotope fold.
2. **`test-sub5ev-band-bound`'s escalation criterion cannot fire.** The in-RoI fraction is
   exactly zero by kinematics. Answered on its own terms, then supplemented with the number that
   actually matters.
3. **The neutron channel is ~10⁴ times the CEvNS signal at 100 meV.** Expected for an unshielded
   outdoor surface wafer, but it means the sub-eV headline of this milestone is set by this
   background, not by the signal. Carried to Plan 13-03 and to Phase 16.

## For Plan 13-02

- `neutron_recoil.fold_dRdT(..., f=..., sigma_b_fn=..., n_per_kg=...)` takes any kinematic
  factor, any cross-section callable and any material's own atoms/kg — the target comparison
  needs no new fold.
- `neutron_recoil.fold_synthetic_epithermal` + `epithermal_oracle_dRdT` are the `f`-cancellation
  legs, already verified to 4.2×10⁻⁸ across four `f` values including W's 0.0215 and O's 0.2215.
- `neutron_recoil.flux_above_ceiling()` returns the pinned driver's integral flux above the 20 MeV
  ENDF ceiling out to 10 GeV — the numerator for the omission bound.
- `elastic_table()` gives `(E_eV, sigma_b, a1)` for the slope-at-the-ceiling measurement.
