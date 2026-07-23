---
phase: 15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em
plan: 01
title: "The Phase-11 nuclear IA broadening does NOT apply to either electron-recoil channel, decided by evaluating the electron-side Compton-profile analogue rather than by asserting that electrons are not nuclei; plus the Landau-Vavilov validity floor at 4111.82 eV, which indicts 209 of the 584 v1.0 bins"
date: 2026-07-23
status: complete
depth: full
completed: 2026-07-23
provides:
  - "src/qpd_potential/em_recoil.py — the machine-readable per-channel IA verdict (IA_APPLICABILITY, ia_verdict), the guard assert_nuclear_kernel_use that RAISES ElectronRecoilBroadeningError, the Landau-Vavilov floor and chord map on the committed muon_deposit path, the I-sensitivity study, the Compton x/S(x,Z) readout from the committed Hubbell table, the Ge pair-creation floor, and the electron-side IA scale bracket"
  - "artifacts/v2.0/em_validity_floors.csv — 6 rows, unit-bearing headers, the floors Plans 15-02 and 15-03 flag bins against"
  - "GPD/phases/15-.../15-01-BROADENING-APPLICABILITY.md — the written determination with the electron-side analogue evaluated, the disconfirming bin count, and the falsifiers"
  - "tests/test_em_recoil.py — 20 tests covering all 10 contract acceptance tests"
  - "artifacts/v2.0/legacy_grid_disposition.csv — disposition row for em_validity_floors.csv (53 register rows, closure guard green)"
one_liner: "Both electron-recoil channels get verdict does_not_apply for the Phase-11 nuclear width sigma_E = sqrt(E_R omega_bar), and the verdict is reached by EVALUATING the one mechanism that could have overturned it rather than by the lazily-correct 'electrons are not nuclei': the electron-side impulse approximation has the IDENTICAL form sigma_T = sqrt(T omega_bar_e) with omega_bar_e = 2 sigma_pz^2/m_e, and its RIGOROUS lower bound from the uncertainty principle over the Ge covalent bond (2.449986 A, derived from the committed lattice constant alone) is 0.634740 eV — 35.540x the nuclear omega_bar = 17.8597 meV, so the transplant would understate the width by at least 5.96x and by up to 362.98x under the core-inclusive envelope; one declared disconfirming observation FIRED, in that the electron-side width is 252.02% of the deposit at the 0.0999350 eV extended floor, 86.3 extended grid bins, so 'no broadening because it would be unresolvable' would have been a FALSE argument, and the analogue is excluded instead on its OWN validity criterion 2W_e = T/omega_bar_e = 0.1574 < 1 at that floor, being carried to Phase 16 as a named gap; the muon channel is additionally excluded on double-counting, since the Landau-Vavilov density IS the fluctuation of that deposit and its width xi = 0.072069 MeV at the vertical chord exceeds any candidate IA width by six decades; the SECOND disconfirming observation ALSO FIRED and is reported without softening — the Landau-Vavilov validity criterion xi <= I with I = 350 eV read from the committed muon_deposit.I_GE puts the floor at Delta_p = 4111.8165 eV, a chord of 9.712913 um, which is 405.31x ABOVE the 10.14 eV v1.0 grid floor and indicts 209 of the 584 bins (35.79%) the v1.0 manuscript already published, up to 4042.199 eV, with the count running only 204-213 over a +/-14% swing in I so no plausible I makes it zero; the chord needed for a 100 meV most-probable deposit is 1.0574 nm = 1.869 Ge lattice constants, a path of roughly two atomic layers; and the Compton channel is NOT blocked — x at the extended floor is 1.288806e-02 A^-1, inside the committed S(x,Z=32) domain with a 12.888x margin, giving S/Z = 2.185858e-03 (457.49x suppression) against 0.1235564 (8.093x) at 10.14 eV, but that number is separated in prose from the adopted physical floor of 0.73955 eV (Ge indirect gap at T->0 less the free-exciton binding), which sits 7.400x ABOVE the extended grid floor and excludes 70 of the 744 extended bins."
plan_contract_ref: GPD/phases/15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em/15-01-PLAN.md#/contract

contract_results:
  claims:
    claim-broadening-verdict:
      status: passed
      summary: "Per-channel verdict does_not_apply, recorded in em_recoil.IA_APPLICABILITY as frozen IAVerdict dataclasses carrying channel, verdict from the closed vocabulary, recoiling_body, initial_state_momentum_distribution, reason, consequence_for_spectra and falsifier — no field may be empty (enforced in __post_init__) and there is no accessor returning a bare boolean. MUON: the recoiling body is an atomic ELECTRON in each ionizing collision; the nucleus is only the static binding potential fixing the oscillator strengths behind I. Excluded on TWO independent grounds, either sufficient — (a) scale, the electron-side IA scale is >= 35.5x the nuclear omega_bar; (b) double counting, the Landau-Vavilov density IS the fluctuation of this deposit, sampled as dep = Delta_p + xi(lambda - lambda_mode), and its width xi = 0.072069 MeV at the vertical chord exceeds a candidate nuclear IA width of 0.0422 eV at 100 meV by six decades. COMPTON: the recoiling body is a bound atomic electron and its initial-state distribution is the Compton profile J(p_z) — the exact electron-side analogue, EVALUATED not dismissed. The IA decomposition T = q^2/(2m) + p.q/m was applied to the electron directly, giving sigma_T = q sigma_pz/m = sqrt(T omega_bar_e) with omega_bar_e = 2 sigma_pz^2/m_e: IDENTICAL form, different body, different scale. omega_bar_e bracketed by three estimators — RIGOROUS lower bound 0.634740 eV from the uncertainty principle over the Ge covalent bond a*sqrt(3)/4 = 2.449986 A (derived from the committed GE_LATTICE_CONSTANT_ANGSTROM = 5.658 and nothing external), valence virial 16.80 eV, whole-atom envelope 2353.06 eV, the latter two marked [UNVERIFIED - training data] and the verdict resting on the lower bound alone. Ratio to nuclear omega_bar = 35.540; energy-independent width ratio sqrt(omega_bar_e/omega_bar) = 5.9616x to 362.98x, so the transplant is the wrong NUMBER by 0.8-2.6 decades, not merely the wrong justification. Excluded additionally on its own IA validity criterion, the electron analogue of the Campbell-Deem condition Phase 11 used: 2W_e = T/omega_bar_e = 0.1574 at the extended floor under the MOST favourable bound and 4.247e-05 under the envelope, both below 1. Neither verdict is undecidable, so the ROADMAP Phase-15 backtracking trigger does not fire. NO Section-J algebraic identity is cited as evidence anywhere, machine-checked by a test that requires every occurrence of an identity form to sit within three lines of a disclaimer."
      linked_ids: [deliv-applicability-report, deliv-em-module, deliv-em-tests, test-verdict-declared, test-verdict-argued, test-electron-analogue-evaluated, test-guard-raises, ref-conventions-J, ref-phase11-summary, ref-neutron-fold-docstring]
      evidence:
        - verifier: gpd-executor
          method: "the electron-side analogue derived from the same IA momentum decomposition and evaluated numerically with a rigorous bound, then excluded on its own validity criterion rather than on the convenient one"
          confidence: high
          claim_id: claim-broadening-verdict
          deliverable_id: deliv-applicability-report
          acceptance_test_id: test-electron-analogue-evaluated
          reference_id: ref-phase11-summary
          forbidden_proxy_id: fp-unexamined-no
          evidence_path: GPD/phases/15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em/15-01-BROADENING-APPLICABILITY.md
    claim-muon-validity-floor:
      status: passed
      summary: "THE DISCONFIRMING CHECK FIRED AND IS REPORTED WITHOUT SOFTENING. Criterion: xi <= I, the published boundary below which a continuous straggling density is not the correct energy-loss distribution because the loss is dominated by a few discrete collisions (PDG 'Passage of Particles Through Matter', energy loss in thin absorbers; Bichsel RMP 60, 663). The committed chain already guards the THIN end via kappa = 6.727e-05; this guards the other. I = 350.0 eV read from src/qpd_potential/muon_deposit.py::I_GE, i.e. the SAME I that produced every v1.0 Delta_p — read from the code, never re-typed; the external PDG value is [UNVERIFIED - not re-fetched]. Computed on the committed path at E_mu = 4.0 GeV (beta*gamma = 37.844651), the reference point of the 09-01 Sec 2.3 scalars, and the reference reproduces them: xi(0.20 cm) = 0.072069 MeV, Delta_p = 1.230614 MeV, kappa = 6.7267e-05, Delta_p < <Delta> = 1.458502 MeV. RESULT: xi = I at ell* = 9.712913e-04 cm = 9.712913 um, floor Delta_p = 4111.8165 eV = 4.1118 keV, which is 405.31x ABOVE the 10.144973 eV v1.0 grid floor. INDICTED: 209 of the 584 frozen v1.0 bins (35.79%), reaching up to a centre of 4042.199 eV, the lowest surviving centre being 4160.251 eV; 369 of the 744 extended bins. Nothing was tuned: the I-sensitivity study varies I CONSISTENTLY in the criterion and the Delta_p bracket via a re-expression verified to reproduce muon_deposit.mpv_deposit to rel diff 0.0 at I = I_GE, and gives 204 bins at I=300, 206 at 322, 209 at 350, 213 at 400 — no plausible I makes the count zero, and the stricter reading xi/I >= 10 would put the floor at 49.18 keV and indict far more, so 209 is the LOOSEST defensible count. Chord map on the same committed path: 10.144973 eV needs 4.428417e-06 cm = 44.28 nm = 78.268 lattice constants; 0.0999350 eV needs 1.057434e-07 cm = 1.0574 nm = 1.869 lattice constants, stated in words as a path of roughly two atomic layers. Competing explanations distinguished rather than picked: the tabulated Landau inverse-CDF clamps at lambda = -4, giving a hard minimum dep = Delta_p - 3.777 xi = +0.958 MeV at the vertical chord, so the clamp alone cannot manufacture sub-eV entries; a sub-eV deposit at full chord length would need lambda - lambda_mode = -17.1, far below the table; therefore sub-eV content is the JOINT tail of a short corner-clipping chord AND a left-tail Landau draw, and in both limbs the deposit sits far below xi ~ I, i.e. outside the model's domain either way."
      linked_ids: [deliv-applicability-report, deliv-em-module, deliv-floors-table, deliv-em-tests, test-muon-floor-computed, test-chord-map-lattice, test-floor-reported-against-v1-bins, test-dimensions, ref-mu-gamma-declaration, ref-muon-module]
      evidence:
        - verifier: gpd-executor
          method: "published criterion applied to the committed code path at the reference point that reproduces the verified v1.0 scalars, with a consistency-checked I-sensitivity study that cannot drive the count to zero"
          confidence: high
          claim_id: claim-muon-validity-floor
          deliverable_id: deliv-floors-table
          acceptance_test_id: test-floor-reported-against-v1-bins
          reference_id: ref-muon-module
          forbidden_proxy_id: fp-floor-softened
          evidence_path: artifacts/v2.0/em_validity_floors.csv
    claim-compton-validity-floor:
      status: passed
      summary: "The machinery DOES return a number at 100 meV and the number is separated in prose from the physics. x at the extended floor is 1.288806e-02 A^-1, INSIDE the committed data/ge_incoherent_S.csv domain [1.0e-3, 4.2646e4] with a margin of 12.888x above the table floor, so no interpolator raises anywhere on the extended axis — verified over all 744 extended centres. This is NOT a blocking finding for Plan 15-02, and the declared disconfirming observation that it might be did not occur. Two structural checks make the mapping trustworthy rather than merely computed: x is INDEPENDENT of line energy at small transfer, all sixteen data/gamma_lines.csv lines giving 1.288806e-02 A^-1 to seven digits, as a momentum transfer must be; and 4 pi x a_0 = sqrt(2 m_e T) in atomic units to 1.3e-8, so x really IS the momentum transfer. Suppression read from the committed table: S/Z = 2.185858e-03 at 0.0999350 eV (457.49x against free Klein-Nishina) and 0.1235564 at 10.144973 eV (8.093x). PHYSICAL FLOOR, adopted and NAMED rather than assumed: the Ge indirect band gap at T -> 0 (0.7437 eV, the operative value because the detector sits at the CONVENTIONS Section J T -> 0 evaluation point) less the free-exciton binding 4.15 meV, giving 0.73955 eV; the 300 K gap 0.661 eV is the named alternative, and both sit 7.400x and 6.614x above the extended grid floor so the verdict does not turn on the choice. Provenance [UNVERIFIED - training data]: no repository artifact carries a Ge band gap, recorded as a weakest anchor. 70 of the 744 extended bins lie below the adopted floor. THE DISTINCTION IS WRITTEN OUT: at 0.0999350 eV the table RETURNS a finite positive S/Z and the machinery will produce a rate from it, but the deposit is 7.40x below the energy at which Ge can create an electron-hole pair at all, and independently the electron-side IA validity parameter 2W_e = 0.157 < 1 there. Two criteria of different origin — a thermodynamic pair-creation threshold at 0.73955 eV and a kinematic IA validity scale at 0.6347 eV — land within a factor 1.2 of each other, and nothing forced them to."
      linked_ids: [deliv-applicability-report, deliv-em-module, deliv-floors-table, deliv-em-tests, test-S-domain-covers-floor, test-S-suppression-computed, test-compton-physical-floor-stated, test-dimensions, ref-compton-module, ref-conventions-B]
  deliverables:
    deliv-applicability-report:
      status: produced
      path: GPD/phases/15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em/15-01-BROADENING-APPLICABILITY.md
      summary: "Nine sections. The verdict table; what Phase 11 actually derived and for what body; the muon double-counting determination; the electron-side analogue derived, bracketed, shown NOT to be negligible, and excluded on its own validity criterion; the Compton S-domain and the physical floor with the number-versus-physics distinction written out; the Landau floor with the 209-bin indictment and the I-sensitivity table; the two competing explanations for the lowest v1.0 muon bins distinguished by numbers; instructions carried forward so Plans 15-02/15-03 re-derive nothing; four falsifiers; uncertainty markers naming which disconfirming observations fired; and a verification ledger."
      linked_ids: [claim-broadening-verdict, claim-muon-validity-floor, claim-compton-validity-floor]
    deliv-em-module:
      status: produced
      path: src/qpd_potential/em_recoil.py
      summary: "IA_VERDICT_VOCABULARY, IAVerdict (frozen, empty-field-rejecting), IA_APPLICABILITY, ia_verdict, ElectronRecoilBroadeningError, assert_nuclear_kernel_use; reference_beta_gamma, xi_coefficient_MeV_per_cm, xi_eV_of_chord_cm, deposit_eV_of_chord_cm, chord_cm_of_deposit_eV, chord_in_lattice_constants, landau_validity_floor, _mpv_deposit_with_I, landau_floor_sensitivity_to_I, indicted_v1_bins; compton_x_of_recoil_inv_angstrom, compton_S_suppression, compton_physical_floor; electron_ia_scale_eV, electron_side_sigma_T_eV, electron_side_summary; validity_floor_rows. It applies no broadening and multiplies no rate by exp(-2W)."
      linked_ids: [claim-broadening-verdict, claim-muon-validity-floor, claim-compton-validity-floor]
    deliv-floors-table:
      status: produced
      path: artifacts/v2.0/em_validity_floors.csv
      summary: "6 rows, one per channel per criterion, every column header unit-bearing. Muon: landau_vavilov_xi_le_I (4111.8165 eV, 209 v1.0 bins, 369 ext bins), chord_map_v1_grid_floor, chord_map_ext_grid_floor. Compton: ge_pair_creation_threshold (0.73955 eV, 70 ext bins), S_suppression_at_ext_grid_floor, S_suppression_at_v1_grid_floor. The header carries the verdict, the reproduction command, the repo HEAD, the I provenance and its sensitivity table, the electron-side bracket, and an explicit statement that no relocation quantity is present."
      linked_ids: [claim-muon-validity-floor, claim-compton-validity-floor]
    deliv-em-tests:
      status: produced
      path: tests/test_em_recoil.py
      summary: "20 tests. Verdict declaration and closed vocabulary; guard raises with the verdict and reason in the message and returns on a consistent call; guard is not a warning or a clamp; the electron analogue evaluated with the rigorous bound reproduced and asserted BIGGER than the nuclear scale; no Section-J identity cited without a disclaimer within three lines; the report names the recoiling body, J(p_z), a falsifier and the named gap; the shielded-token guard IMPORTED from the Phase-9 single definition site rather than re-typed; the reference point reproduces the 09-01 scalars; the I-exposed re-expression reproduces the committed mpv_deposit to 1e-14; the floor, the 209-bin count, the I-sensitivity, the chord map in lattice constants; the S domain over all 744 centres; 4 pi x a_0 = sqrt(2 m_e T) as an independent check that x is the momentum transfer; the S suppressions; the named physical floor; dimensions and unit-bearing headers; and the disposition row."
      linked_ids: [claim-broadening-verdict, claim-muon-validity-floor, claim-compton-validity-floor]
    deliv-disposition-row:
      status: produced
      path: artifacts/v2.0/legacy_grid_disposition.csv
      summary: "One row for artifacts/v2.0/em_validity_floors.csv, disposition not_a_spectrum (a registry of named criteria, no bins to re-grid), with a reason recording the verdict and the 209-bin indictment. Register now 53 rows; tests/test_legacy_grid_disposition.py::test_register_closure green."
      linked_ids: [claim-muon-validity-floor, claim-compton-validity-floor]
  acceptance_tests:
    test-verdict-declared:
      status: passed
      summary: "Both channels carry a vocabulary verdict with every field non-empty and longer than 40 characters. A verdict outside the vocabulary and an empty field each raise at construction. ia_verdict('neutron') raises KeyError — the absence of a verdict is not a default to does_not_apply."
      linked_ids: [claim-broadening-verdict, deliv-em-module, deliv-em-tests]
    test-verdict-argued:
      status: passed
      summary: "The report names the recoiling body and the initial-state momentum distribution per channel, derives the electron-side analogue from the IA decomposition rather than asserting a difference, and states four falsifiers including the one route by which omega_bar could legitimately enter an electron channel (a phonon-bath-induced momentum distribution for the struck electron), which is recorded as residual uncertainty rather than dismissed. Machine-checked for the required tokens."
      linked_ids: [claim-broadening-verdict, deliv-applicability-report]
    test-electron-analogue-evaluated:
      status: passed
      summary: "The Compton profile analogue is evaluated with a number AND a rigorous bound: omega_bar_e >= 0.634740 eV from the uncertainty principle over the Ge covalent bond, 35.540x the nuclear omega_bar, giving an energy-independent width ratio of 5.9616x to 362.98x. Its size on the DEPOSIT axis is stated: 252.02% of the deposit at the extended floor, 86.3 extended grid bins, i.e. NOT unresolvable — the plan's declared disconfirming observation FIRED and is reported as such. It is excluded on 2W_e < 1 rather than on unresolvability."
      linked_ids: [claim-broadening-verdict, deliv-applicability-report, deliv-em-module]
    test-guard-raises:
      status: passed
      summary: "assert_nuclear_kernel_use(channel, True) raises ElectronRecoilBroadeningError for both channels, with the verdict, the recoiling body, the reason, the consequence and fp-transplant-nuclear-width in the message; assert_nuclear_kernel_use(channel, False) returns the verdict object itself, so a caller that passes the guard has necessarily received the reason. A separate test asserts the module contains no warnings.warn and no np.clip, so the guard cannot have degraded into a warning or a clamp."
      linked_ids: [claim-broadening-verdict, deliv-em-module, deliv-em-tests]
    test-muon-floor-computed:
      status: passed
      summary: "The frozen floor reproduces from the committed code path exactly (rel 1e-6, far better than the required 1%), xi at the crossing equals I to 1e-12, and I carries a named source pointing at muon_deposit.I_GE and the PDG table. The reference point independently reproduces the three verified 09-01 vertical-chord scalars."
      linked_ids: [claim-muon-validity-floor, deliv-floors-table, deliv-em-module, deliv-em-tests]
    test-chord-map-lattice:
      status: passed
      summary: "Both chords computed by inverting Delta_p(ell) on the committed path and verified by round trip to rel 1e-9: 78.268 lattice constants at the v1.0 floor, 1.8689 at the extended floor. Since the extended-floor chord is under 10 lattice constants the report states in words that it is a path of roughly two atomic layers, and the test asserts that sentence is present."
      linked_ids: [claim-muon-validity-floor, deliv-floors-table, deliv-applicability-report]
    test-floor-reported-against-v1-bins:
      status: passed
      summary: "209 of 584 v1.0 bins and 369 of 744 extended bins below the floor, recorded in the table, in the CSV header, and in the report in words. The test asserts the floor is ABOVE the v1.0 grid floor and that 'fp-floor-softened' appears in the report, and a separate test asserts the I-sensitivity count never reaches zero. This is the plan's disconfirming check and it FIRED."
      linked_ids: [claim-muon-validity-floor, deliv-floors-table, deliv-applicability-report, deliv-em-tests]
    test-S-domain-covers-floor:
      status: passed
      summary: "x = 1.288806e-02 A^-1 at the extended floor is inside the committed table domain with a 12.888x margin above the table floor, and S is finite and positive at every one of the 744 extended centres, so no interpolator raises. Not a blocking finding for Plan 15-02."
      linked_ids: [claim-compton-validity-floor, deliv-em-module, deliv-em-tests]
    test-S-suppression-computed:
      status: passed
      summary: "S/Z = 2.185858e-03 (457.49x) at 0.0999350 eV and 0.1235564 (8.093x) at 10.144973 eV, reproducing from the committed table to rel 1e-5 and frozen in the table to better than 1%."
      linked_ids: [claim-compton-validity-floor, deliv-floors-table, deliv-em-tests]
    test-compton-physical-floor-stated:
      status: passed
      summary: "The adopted floor 0.73955 eV is stated with its source and its named alternatives, its provenance is marked UNVERIFIED, and the number-versus-physics distinction is written out explicitly rather than left to the reader — 'a number the S table returns here is not the same object as a rate the physics supports: a suppressed rate is not a rate'."
      linked_ids: [claim-compton-validity-floor, deliv-applicability-report]
    test-dimensions:
      status: passed
      summary: "Every non-label CSV column header carries its units in brackets and the units are checked by name: floor_eV[eV], xi_at_floor_eV[eV], chord_at_floor_cm[cm], x_inv_angstrom[1/angstrom], S_over_Z[dimensionless], I_eV[eV]. sigma scales as sqrt, xi is linear in the chord and equals the coefficient at ell = 1 cm to 1e-12, and xi_coefficient_MeV_per_cm = 0.3603450."
      linked_ids: [claim-muon-validity-floor, deliv-floors-table, deliv-em-module, deliv-em-tests]
  references:
    ref-conventions-J:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Read in full including the 'Two algebraic identities - neither is corroboration' block. The locked omega_bar = 17.8597 meV is the number the electron-side scale is compared AGAINST, and the never-multiply-by-exp(-2W) prohibition is restated in the module docstring and enforced by the absence of any exp(-2W) in the code. The identity block's own failure mode is guarded by a test that requires every occurrence of an identity form in the module or the report to sit within three lines of a disclaimer."
    ref-phase11-summary:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "11-02-SUMMARY.md claim-sigma-derivation quoted verbatim in Section 1 of the report: w = q^2/(2 m_N) + q.p/m_N, sigma_p^2 = m_N omega_bar/2 FROM THE ZERO-POINT OSCILLATOR. That is what fixes the recoiling body as the nucleus, and the generic form of the decomposition is what makes the electron-side analogue a real question. Phase 11's own fp-electron-recoil-leak note (Section 7 of its derivation artifact declined to answer in either direction) is the handoff this plan discharges."
    ref-neutron-fold-docstring:
      status: completed
      completed_actions: [read, cite]
      missing_actions: []
      summary: "run_neutron_fold_extended's APPLICABILITY paragraph read and cited: it states verbatim that the neutron applicability follows from its nuclear-recoil character and that 'Phase 15's ELECTRON-recoil channels are a separate question and are not settled by this'. Discharged."
    ref-mu-gamma-declaration:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "Section 2.3 supplied the reference point E_mu = 4 GeV and the three vertical-chord scalars, all three of which the committed path reproduces here (xi 0.072069 MeV, Delta_p 1.230614 MeV, kappa 6.7267e-05, Delta_p < <Delta> = 1.458502 MeV). Sections 2.5 and 3.4 supplied the accuracy labels, carried into every row of the frozen table with the muon Leg A citation and the Leg A / Leg B bracketing disclosure attached and never narrowed."
    ref-muon-module:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "xi_width, mpv_deposit, kappa, RHO, I_GE, beta_gamma, density_effect and shared_energy_grid all called directly. The floor, the chord map and the I-sensitivity are computed ON this path; the only re-expression (_mpv_deposit_with_I, needed because I is hard-wired) is asserted to reproduce mpv_deposit to rel diff 0.0 at the committed I."
    ref-compton-module:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "incoherent_S, momentum_transfer_x, HC_KEV_ANG, M_E_KEV, Z_GE and the frozen _SF_X/_SF_S arrays used directly for the domain check and both suppression factors. The exact Compton kinematics were inverted at fixed line energy and cross-checked against the small-transfer closed form and against 4 pi x a_0 = sqrt(2 m_e T)."
    ref-conventions-B:
      status: completed
      completed_actions: [read, cite]
      missing_actions: []
      summary: "Cited in the module docstring: 'electron recoil' here names the INTERACTION — which particle absorbs the momentum transfer — and never licenses a keVee axis. The unified phonon scale is untouched by this plan, which emits no spectrum."
  forbidden_proxies:
    fp-transplant-nuclear-width:
      status: rejected
      notes: "The kernel is not applied anywhere, and the guard raises on a request to apply it. Beyond avoidance, the SIZE of the error the transplant would make is quantified: 5.96x to 362.98x understatement of the electron-side width."
    fp-unexamined-no:
      status: rejected
      notes: "Section 3 of the report derives the electron-side analogue from the same IA momentum decomposition, brackets omega_bar_e with a RIGOROUS lower bound requiring no external number, tabulates sigma_T/T at four energies, and reports that the analogue is NOT negligible against the response chain — 86.3 extended grid bins at the extended floor. The comfortable argument ('too small to see') is explicitly identified as FALSE and is not used. The exclusion rests on 2W_e < 1 instead."
    fp-identity-as-corroboration:
      status: rejected
      notes: "No Section-J identity is cited as evidence. Machine-enforced by test_no_section_J_identity_is_cited_as_evidence, which requires every occurrence of sigma_E/E_R = 1/sqrt(2W) or 2W = E_R/omega_bar in the module or the report to sit within three lines of an explicit disclaimer."
    fp-floor-softened:
      status: rejected
      notes: "The criterion xi <= I is published, I is READ FROM THE COMMITTED CODE rather than chosen, and the I-sensitivity study varies it consistently across 300-400 eV giving 204-213 indicted bins. No value makes the count zero. The stricter reading xi/I >= 10 would indict far more, so the reported 209 is the loosest defensible count, not the most convenient one."
    fp-suppressed-means-valid:
      status: rejected
      notes: "The S readout and the physical floor are separate functions returning separate objects and separate CSV rows, and the report devotes Section 4.2 to writing the distinction out. The adopted physical floor 0.73955 eV sits 7.400x above the extended grid floor, so the S number at 100 meV is explicitly labelled as a number the table returns rather than a rate the physics supports."
    fp-shielded-quantity-leak:
      status: rejected
      notes: "Enforced by importing the Phase-9 token list via test_env_v1_identity rather than re-typing it, with its digit-boundary matching — which is what keeps the Ge lattice constant 5.658 from false-positiving on the 5.65 Bq/kg 238U ambience, a false positive an ad-hoc substring scan produced and this guard did not. Zero applied hits over em_recoil.py and em_validity_floors.csv. The one deliberate exclusion (the 'residual' token, scoped by its own docstring to the assembled environment set and appearing here only as the Phase-12 counts-budget field name and as an English word in a falsifier) is written out with its justification, and Plan 15-04 applies the full list including 'residual' and 'Table 5' where it belongs."
  uncertainty_markers:
    weakest_anchors:
      - "I = 350 eV is not a named constant in params.py; its provenance is the committed muon_deposit.I_GE and the external PDG value was NOT re-fetched in this phase. The floor scales with it; the sensitivity is reported and the finding survives +/-14%."
      - "No measurement of a sub-eV energy-loss distribution exists for either channel in this repository or its anchor registry. The determination is published physics applied to committed numbers, not a fit."
      - "The Ge band gap adopted as the Compton physical floor is [UNVERIFIED - training data]; no repository artifact carries one. The exciton correction is applied and named; a band-structure threshold would be a different named choice."
      - "The valence-virial and whole-atom estimators of omega_bar_e are [UNVERIFIED - training data]. The verdict rests on the rigorous lower bound alone, which needs nothing external."
    unvalidated_assumptions:
      - "That the two channels can share a verdict. They were determined SEPARATELY on different grounds — muon on double-counting plus scale, Compton on scale plus its own IA validity — and happen to agree; the verdicts are recorded per channel for that reason."
      - "REFUTED rather than assumed: that a small electron-side IA width would be unresolvable against the response chain. It is 86.3 extended grid bins wide at the extended floor."
      - "That no phonon-bath mechanism gives the struck ELECTRON an initial-state momentum distribution of nuclear scale. This is the one route by which omega_bar could legitimately enter an electron-recoil channel; it is not what Phase 11 derived, it would be new physics, and it is recorded as the residual uncertainty in the verdict rather than dismissed."
    disconfirming_observations:
      - "FIRED: the Landau-Vavilov validity floor lands at 4111.82 eV, ABOVE the 10.14 eV v1.0 grid floor, indicting 209 of the 584 bins the v1.0 manuscript published. Reported with its count, not suppressed and not fixed by softening the criterion."
      - "FIRED: the electron-side Compton-profile analogue produces a width that is NOT negligible against the response chain (252.02% of the deposit at 100 meV, 86.3 extended bins), so 'no broadening because it is unresolvable' would have been a false argument. The verdict is reached on a different ground."
      - "DID NOT FIRE: x at the extended floor is INSIDE the committed S(x,Z) domain with a 12.888x margin, so the Compton channel can be evaluated at 100 meV without extrapolation and Plan 15-02 is not blocked."
---

# Plan 15-01 Summary

## What was determined

**Verdict, both channels: `does_not_apply`.** The Phase-11 nuclear-recoil width
`σ_E = √(E_R ω̄)` is not applied to the muon-ionization or Compton channels. Neither
verdict is `undecidable`, so the ROADMAP backtracking trigger does not fire.

**How the verdict was reached matters more than the verdict.** The plan forbade the
lazily-correct route. The electron-side analogue — the same IA formalism with the
bound-electron momentum distribution replacing the nucleus's — was derived, bracketed
and evaluated:

```
σ_T = q σ_pz/m_e = √(T · ω̄_e),    ω̄_e ≡ 2 σ_pz²/m_e
ω̄_e ≥ 0.634740 eV   (rigorous, uncertainty principle over the Ge covalent bond)
     = 35.540 × ω̄   →  the nuclear transplant understates by 5.96× … 362.98×
```

One of the plan's declared disconfirming observations **fired**: that width is
**252 % of the deposit at 100 meV — 86 extended grid bins**, so "no broadening
because it would be unresolvable" would have been a *false* argument. The analogue is
excluded instead on its own validity criterion, `2W_e = T/ω̄_e = 0.157 < 1` at the
extended floor, and is handed to Phase 16 as a **named gap**.

## The disconfirming finding

The Landau–Vavilov validity criterion `ξ ≤ I`, with `I = 350 eV` read from the
committed `muon_deposit.I_GE`, puts the floor at

```
ξ = I at ℓ* = 9.712913 µm  →  Δ_p = 4111.8165 eV = 4.1118 keV
```

**405× above the 10.14 eV v1.0 grid floor. 209 of the 584 frozen v1.0 bins (35.79 %)
lie below it**, reaching up to 4042.2 eV. Varying `I` consistently over 300–400 eV
gives 204–213; the stricter reading `ξ/I ≥ 10` would put the floor at 49.18 keV.
**No plausible criterion makes the count zero, and none was tried.**

This does not say the v1.0 spectrum is *wrong* below 4.11 keV; it says the
distribution used to generate it is outside the regime Landau–Vavilov theory
describes there, so those bins are an extrapolation of the model rather than a
prediction of it. The integral rate and the bulk of the channel are untouched — the
sub-4 keV deposited tail carries ~1e-4 of the flux.

## Handoff

* **15-02**: flag every emitted bin against these floors (`below_validity_floor`);
  emit the flag, never delete the row. Both tables `broadened_provenance = false`.
* **15-03**: `broaden=False` for both channels, read from `em_recoil` at fold time.
  The two counts residuals **coincide** — say so rather than presenting them as two
  confirmations.
* **Phase 16**: two named gaps — the neglected Compton-profile Doppler broadening,
  and the 209 indicted v1.0 muon bins.

## Deviations

None. No deviation rule was applied.
