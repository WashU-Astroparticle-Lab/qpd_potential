---
phase: 14-ge-only-thermal-capture-channels-p-geonly
plan: 01
title: "Ge (n,gamma) capture frozen from the already-local ENDF/ACE with the MF=3 MT=102 zero asserted as the trap it is, folded and band-decomposed to 4399.78 counts/kg/day, and stated as a rigorous cascade-independent in-RoI bound beside the five single-gamma ceilings and the SC5 inelastic bound"
date: 2026-07-23
status: complete
depth: full
completed: 2026-07-23
provides:
  - "src/qpd_potential/capture_channel.py — a NEW module (no existing line numbers moved): the ACE MT=102 and MT=51..91 readers, the MF=3 MT=102 trap probe, the QM-field Q_cap reader, the band-decomposed spectral fold, the Westcott-type comparison, the Doppler and self-shielding checks, the rigorous cascade-free bound and the EGAF cascade-completeness check"
  - "artifacts/v2.0/ge_capture_xs.csv — per-isotope and natural sigma_(n,gamma) plus the summed inelastic, on a stated 100/decade log grid, with a provenance header that states the MF=3 trap in words and carries a VALIDATION block computed at generation time"
  - "artifacts/v2.0/capture_rate_bands.csv — the reaction rate decomposed into four incident-energy bands, per isotope and natural, with the naive-product row labelled NAIVE_PRODUCT_NOT_THE_ANSWER, the 0.1 K vs 293.6 K Doppler rows, the self-shielding rows, the Biffl ratio and the node-doubling figure"
  - "artifacts/v2.0/capture_recoil_bounds.csv — every row carrying RIGOROUS_BOUND or CONDITIONAL_ESTIMATE: the cascade-free in-RoI bound, the five single-gamma ceilings, the symbolic T_max/N row, the EGAF completeness and recoil brackets, the inelastic rate and its placement"
  - "data/egaf/{71,73,74,75,77}GE_EGAF.ens + MANIFEST.md — the EGAF prompt capture-gamma line lists, RETRIEVED and integrity-checked (curl command, byte counts, SHA-256), which planning had recorded as unavailable"
  - "data/ge71_ec/livechart_71ge_*.csv — the IAEA Live Chart 71Ge retrieval (ground state, X-ray and Auger line lists), frozen here and consumed by Plan 14-02"
  - "GPD/phases/14-.../14-01-CAPTURE-BOUNDS.md — the evidence record: the trap, the fold, the thermal-dominance verdict, the Westcott comparison, the Doppler and self-shielding numbers, the bounds and their derivations, the EGAF disposition, the Biffl comparison and the un-netted nine-row directional-bias table"
  - "tests/test_capture_channel.py — 20 tests, all tolerances declared as module constants before any check runs"
  - "artifacts/v2.0/legacy_grid_disposition.csv — six disposition rows for the new tracked .csv files"
  - "GPD/phases/10-.../10-01-INTERPOLATOR-INVENTORY.md — three new rows for the capture_channel.py interpolation sites, with the closure count bumped 41 -> 44"
one_liner: "Ge (n,gamma) capture is frozen from the already-committed Lib80x ACE set rather than from MF=3 MT=102, whose identical zero through the resolved-resonance region is now ASSERTED by execution for all five isotopes so the one-line route to the forbidden 'capture is zero' result is proved real rather than described; natural sigma_th falls out unfitted at 2.211522 b with 73Ge at 14.7009 b carrying 51.52% of the natural thermal capture from 7.75% of the atoms, reproducing the ROADMAP's independently stated ~2.2 b / ~15 b; the spectral fold over the outdoor sea-level flux gives 4399.78 counts/kg/day total — the same order as Phase 13's elastic in-RoI 5430.29/5485.15 and 37.1x the Phase-12 CEvNS total of 118.73, so this channel is not a rounding correction — decomposed into thermal 3365.54 / epithermal 857.08 / intermediate 167.75 / fast 9.41 that sum to the total at residual 2.07e-16 with node doubling moving it 1.19e-5 and 232 quadrature nodes in the 1-10.14 eV table gap evaluated BIT-IDENTICALLY by the pinned PARMA driver; the thermal-dominance verdict is THERMAL FRAMING SURVIVES at 76.49% against a threshold declared before the number was computed, but 23.51% of the channel is NOT thermal and that 1034.24 counts/kg/day remainder is itself ~8.7x the whole CEvNS total, so a budget that took the phase title literally would understate this channel by a factor 1.31; the naive Phi_th x sigma_2200 product 4383.92 DIFFERS from the folded thermal band by +30.26% — the pass condition, since agreement would mean the fold collapsed — while its ratio to the TOTAL is 0.9964, which looks like corroboration and is exactly the trap, and sqrt(pi)/2 = 0.8862 is neither the measured ratio nor substituted for it; the Phase-9 mK caveat is answered with +0.01016% on the epithermal band from the committed 0.1 K ACE set with the resonance-integral-conservation mechanism stated so it is not read as a null check, while the thin-target formula is found NOT to hold at the 102.59 eV resonance where P_capture(2 mm) = 73.6% and the epithermal band is bounded as overstated by <= 11.00% (penalizes_SB); the in-RoI contribution is stated as the RIGOROUS cascade-independent bound R_RoI <= R_capture, proved invariant by execution under nine varied multiplicity / partition / angular-correlation settings, beside the five single-gamma ceilings 415.77 / 338.30 / 754.11 / 302.87 / 257.07 eV read from the ENDF QM field — the maximum belonging to 73Ge, which also dominates the rate, and exceeding the ROADMAP's illustrative '473 eV at 8 MeV' rather than being reconciled to it — with the multiplicity-N mean left symbolic; EGAF was RETRIEVED against planning's expectation and frozen with its integrity record, discharging SC1's acquisition half, but a completeness check shows the observed cascade carries only 60-71% of Q_cap so the sharpening gap SURVIVES as a number rather than an absence, and the only thing taken from it is a rigorous <T> upper bracket that tightens the 73Ge ceiling from 754.1 to 408.9 eV without assuming any multiplicity; and the SC5 inelastic channel is bounded at 2666.83 counts/kg/day with its two recoils separated — the 227.2 keV nuclear recoil ~3 decades ABOVE the RoI making the rate bound very loose there, against the 2.577 eV (74Ge 596 keV) and 5.185 eV (72Ge 834 keV) gamma-emission recoils that are the part landing near the band — and with the >20 MeV omission RE-LABELLED flatters_SB for inelastic because its top-decade fraction is 73.55%, so Phase 13's 11.85x elastic margin is explicitly not reused."
plan_contract_ref: GPD/phases/14-ge-only-thermal-capture-channels-p-geonly/14-01-PLAN.md#/contract

contract_results:
  claims:
    claim-xs-frozen:
      status: passed
      summary: "A provenance-headed capture cross-section artifact is frozen from the already-committed ENDF/B-VIII.0 raw files (QM field only) and the Lib80x ACE set (pointwise sigma). Natural sigma_(n,gamma)(0.0253 eV) = 2.211522 b and 73Ge = 14.7009 b, both inside 20% of the ROADMAP's independently stated ~2.2 b and ~15 b with NOTHING fitted or scaled; 73Ge carries 51.52% of the natural thermal capture from 7.75% of the atoms. THE MF=3 MT=102 TRAP IS ASSERTED BY EXECUTION: the probe returns exactly 0.0 at 0.0253 eV, 1 eV, 100 eV and 1 keV for ALL FIVE isotopes, np.array_equal against zeros, and the artifact header states in words that the RRR capture cross section lives in File 2 while File 3 carries only the background. The switch to ACE is recorded, not silent. All five Q_cap values are READ from the QM field and re-verified against a fresh endf.Material read in test. EGAF DISPOSITION: retrieved, contrary to planning's expectation, and frozen at data/egaf/ with curl command, byte counts and SHA-256 in MANIFEST.md."
      linked_ids: [deliv-capture-xs, deliv-bounds-report, deliv-capture-tests, test-xs-anchor, test-mf3-zero-recorded, test-egaf-disposition, ref-elastic-acq, ref-roadmap-14, fp-capture-as-zero]
      evidence:
        - verifier: gpd-executor
          method: "the forbidden result is REPRODUCED deliberately and asserted, so the trap is shown real rather than described; the anchor is then reproduced from a different section of the same frozen data with nothing fitted"
          confidence: high
          claim_id: claim-xs-frozen
          deliverable_id: deliv-capture-xs
          acceptance_test_id: test-mf3-zero-recorded
          reference_id: ref-elastic-acq
          forbidden_proxy_id: fp-capture-as-zero
          evidence_path: artifacts/v2.0/ge_capture_xs.csv
    claim-capture-rate:
      status: passed
      summary: "R = N_Ge INT phi sigma dE over 0.01 eV - 20 MeV on 24298 nodes (ACE native union + 200/decade + band edges) gives 4399.78 counts/kg/day, decomposed thermal 3365.54 / epithermal 857.08 / intermediate 167.75 / fast 9.41, summing to the total at residual 2.07e-16 with node doubling moving it 1.19e-5. The 1-10.14 eV gap between the two committed flux tables holds 232 quadrature nodes whose flux is BIT-IDENTICAL to a direct parma.differential_flux call, so nothing interpolated across either table's edge. The bound lands at the same order as Phase 13's elastic in-RoI 5430.29/5485.15 and 37.1x Phase 12's CEvNS total 118.73 — NOT negligible. The naive Phi_th x sigma(0.0253 eV) product = 4383.92 and DIFFERS from the folded thermal band by +30.26%, which is the pass condition; its ratio to the TOTAL is 0.9964, the near-cancellation trap, reported as such. Thermal-dominance verdict: SURVIVES at 76.49% against a 60% threshold declared before the number was computed, with the 23.51% non-thermal remainder named and carried forward."
      linked_ids: [deliv-capture-rate, deliv-bounds-report, deliv-capture-tests, test-rate-fold-bands, test-westcott-not-identity, test-thermal-dominance, test-doppler-sensitivity, ref-neutron-decl, ref-phase13, ref-biffl, fp-westcott-product, fp-phi-lo-as-central]
      evidence:
        - verifier: gpd-executor
          method: "a comparison whose FAILURE condition is agreement, plus a band decomposition that must close, plus a bit-identity assertion on the gap flux — three ways for a collapsed or double-counted fold to be caught"
          confidence: high
          claim_id: claim-capture-rate
          deliverable_id: deliv-capture-rate
          acceptance_test_id: test-westcott-not-identity
          reference_id: ref-neutron-decl
          forbidden_proxy_id: fp-westcott-product
          evidence_path: artifacts/v2.0/capture_rate_bands.csv
    claim-cascade-bound:
      status: passed
      summary: "R_RoI <= R_capture = 4399.78 counts/kg/day, derived in one line from 'every capture yields exactly one recoiling nucleus' and NOT by integrating a spectrum. It holds on the recoil, deposit and reconstructed axes alike because R's columns sum to 1. Its cascade-independence is asserted by EXECUTION: nine variants spanning multiplicity 1/3/5/17, four explicit gamma-energy partitions and three angular-correlation labels all return the identical float. The five single-gamma ceilings T_max = Q^2/(2 M_(A+1) c^2) are 415.77 / 338.30 / 754.11 / 302.87 / 257.07 eV; 73Ge sets the maximum AND dominates the rate at 58.0%; the ROADMAP's generic '473 eV at 8 MeV' is treated as an illustration and the higher Ge maximum is reported rather than reconciled to it. Sum(E^2) != (Sum E)^2 is shown with numbers (ratio 0.3425 for an explicit 3-gamma partition) and the multiplicity-N mean is written as T_max/N with N SYMBOLIC and no numeric value in the artifact."
      linked_ids: [deliv-recoil-bounds, deliv-bounds-report, deliv-capture-tests, test-cascade-ceiling, test-bound-is-cascade-free, test-multiplicity-statement, ref-roadmap-14, ref-biffl, fp-single-gamma-as-cascade, fp-assumed-multiplicity]
      evidence:
        - verifier: gpd-executor
          method: "invariance asserted by trying to move it: nine cascade parameter settings fed through the same entry point, with exact float equality required rather than a tolerance"
          confidence: high
          claim_id: claim-cascade-bound
          deliverable_id: deliv-recoil-bounds
          acceptance_test_id: test-bound-is-cascade-free
          reference_id: ref-roadmap-14
          forbidden_proxy_id: fp-single-gamma-as-cascade
          evidence_path: artifacts/v2.0/capture_recoil_bounds.csv
    claim-inelastic-named:
      status: passed
      summary: "Summed MT=51..91 folded over the same flux: 2666.83 counts/kg/day natural (74Ge 1014.66, 72Ge 708.63, 70Ge 446.47, 73Ge 278.86, 76Ge 218.16), 94.42% from the 1-20 MeV band. The placement statement separates the two recoils that would otherwise be conflated: the NUCLEAR recoil is set by the fast incident neutron, f_nat x <E_n> = 227.2 keV at the rate-weighted mean incident energy 4.238 MeV, ~3 decades ABOVE the 100 eV RoI top, which is why the rate bound is very loose there; the part landing near the band is the separate GAMMA-EMISSION recoil E_gamma^2/(2Mc^2) = 2.577 eV for the 74Ge 596 keV level and 5.185 eV for the 72Ge 834 keV level, both named explicitly. The top-decade (2-20 MeV) fraction is 73.55%, far above the 10% trigger, so Phase 13's measured 11.85x >20 MeV elastic margin is NOT reused and the inelastic >20 MeV omission is labelled flatters_SB."
      linked_ids: [deliv-recoil-bounds, deliv-bounds-report, deliv-capture-tests, test-inelastic-named, ref-roadmap-14]
      evidence:
        - verifier: gpd-executor
          method: "the two recoil mechanisms are computed separately and compared against the RoI top, so a bare rate cannot pass as a placement"
          confidence: medium
          claim_id: claim-inelastic-named
          deliverable_id: deliv-recoil-bounds
          acceptance_test_id: test-inelastic-named
          reference_id: ref-roadmap-14
          forbidden_proxy_id: fp-precision-inflation
          evidence_path: artifacts/v2.0/capture_recoil_bounds.csv
  deliverables:
    deliv-capture-xs:
      status: passed
      path: artifacts/v2.0/ge_capture_xs.csv
      summary: "931 rows on a stated 100/decade log grid, 0.01 eV - 20 MeV: per-isotope sigma_(n,gamma), natural sigma_(n,gamma), summed MT=51..91 natural, accuracy_label per row. Header carries MATs read from the file headers, raw and ACE SHA-256 heads, ACE ZAIDs and temperature keys, IUPAC abundances from params.GE_ISOTOPES, N_Ge, git sha, the reproduce command, the MF=3 trap stated in words with the measured zeros printed, the five Q_cap values and ceilings, the 73Ge share, the NCrystal reduction with its reason, and a MESH note reporting that the FOLD does not use this grid (artifact-vs-native resonance-band integral differ by -2.87%, stated so the artifact's coarseness cannot be mistaken for the fold's)."
      linked_ids: [claim-xs-frozen, test-xs-anchor, test-mf3-zero-recorded]
    deliv-capture-rate:
      status: passed
      path: artifacts/v2.0/capture_rate_bands.csv
      summary: "36 rows: four bands x (natural + five isotopes) plus totals, the NAIVE_PRODUCT_NOT_THE_ANSWER row with its measured ratio, two DOPPLER_CHECK rows and their signed difference, two SELF_SHIELDING_CHECK rows including the resonance-peak value that is NOT << 1, the BIFFL_COMPARISON ratio, and the NODE_DOUBLING convergence figure. accuracy_label on every row. Header carries the flux-leg statement, the gap-coverage measurement, the convergence figures, the thermal-dominance verdict, the Westcott explanation including the near-cancellation trap, the Doppler mechanism, the per-band slab-vs-thin bound and the Biffl direction."
      linked_ids: [claim-capture-rate, test-rate-fold-bands, test-westcott-not-identity, test-thermal-dominance, test-doppler-sensitivity]
    deliv-recoil-bounds:
      status: passed
      path: artifacts/v2.0/capture_recoil_bounds.csv
      summary: "31 rows, each carrying evidence_class RIGOROUS_BOUND or CONDITIONAL_ESTIMATE and its own units column: the cascade-free in-RoI bound and its ratio to the CEvNS total, the five single-gamma ceilings with their parsed Q values, the symbolic T_max/N row with an EMPTY value cell, the sum-of-squares demonstration, the EGAF completeness / observed mean / rigorous upper bracket per isotope with 76Ge explicitly excluded and why, the natural and per-isotope inelastic rates, the inelastic nuclear-recoil scale and the two named gamma-emission recoils."
      linked_ids: [claim-cascade-bound, claim-inelastic-named, test-cascade-ceiling, test-multiplicity-statement, test-inelastic-named]
    deliv-bounds-report:
      status: passed
      path: GPD/phases/14-ge-only-thermal-capture-channels-p-geonly/14-01-CAPTURE-BOUNDS.md
      summary: "Seven sections: acquisition and its two traps (MF=3, and the three-dataset EGAF parse), the fold with its gap-coverage and convergence evidence, the thermal-dominance verdict, the Westcott comparison with the near-cancellation trap spelled out, the Doppler and self-shielding numbers, the Biffl comparison with its direction, the four bound categories with their derivations, the inelastic placement, the un-netted nine-row directional-bias table, and the recorded EGAF-sharpening checkpoint with its default."
      linked_ids: [claim-xs-frozen, claim-capture-rate, claim-cascade-bound, claim-inelastic-named]
    deliv-capture-tests:
      status: passed
      path: tests/test_capture_channel.py
      summary: "20 tests, all passing. Tolerances declared as module constants BEFORE any check: XS_ANCHOR_REL_TOL 0.20, BAND_SUM_REL_TOL 5e-3, NODE_DOUBLING_REL_TOL 5e-3, WESTCOTT_MIN_RELATIVE_DIFFERENCE 0.05, THERMAL_DOMINANCE_THRESHOLD 0.60, CASCADE_INVARIANCE_REL_TOL 0.0 (exact). Includes the phi_lo refusal test, a line-level phi_lo scan over the module, and CSV parsing through the csv module rather than split(',') so a quoted basis field cannot silently shift a column."
      linked_ids: [claim-xs-frozen, claim-capture-rate, claim-cascade-bound, claim-inelastic-named]
    deliv-disposition-rows-01:
      status: passed
      path: artifacts/v2.0/legacy_grid_disposition.csv
      summary: "Six rows added: ge_capture_xs.csv as bounded_native_axis with floor 0.01 eV on its own INCIDENT-NEUTRON axis and a reason recording that the fold does not use that grid; capture_rate_bands.csv and capture_recoil_bounds.csv as not_a_spectrum with reasons naming what they actually are; and the three data/ge71_ec/ Live Chart retrievals as not_a_spectrum. The register's own enumeration test passes with no unregistered artifact."
      linked_ids: [claim-xs-frozen, claim-capture-rate, claim-cascade-bound]
  acceptance_tests:
    test-xs-anchor:
      status: passed
      summary: "natural sigma_(n,gamma)(0.0253 eV) = 2.211522 b vs the ROADMAP's independently stated 2.2 b (+0.52%, inside 20%); 73Ge = 14.7009 b vs ~15 b (-1.99%, inside 20%). Nothing fitted or scaled. The 73Ge share of natural thermal capture, 51.52%, is asserted to exceed 5x its 0.0775 abundance share AND to be present in the artifact header."
      linked_ids: [claim-xs-frozen, deliv-capture-xs, deliv-capture-tests]
    test-mf3-zero-recorded:
      status: passed
      summary: "PASSES ON THE ZERO ASSERTION for all five isotopes at four energies, via np.array_equal against a zeros array, so the trap is proved real rather than hypothesised. The operative ACE source is asserted non-zero at the same energy, the fold's source path is asserted to be the .800nc ACE file, and the artifact header is asserted to contain 'MF=3 MT=102', 'IDENTICALLY 0.0', 'FILE 2', 'pre-reconstructed' and 'FORBIDDEN PROXY'. A silent switch to ACE would fail."
      linked_ids: [claim-xs-frozen, deliv-capture-xs, deliv-capture-tests]
    test-egaf-disposition:
      status: passed
      summary: "PASSED ON THE ACQUISITION BRANCH, which planning did not expect. All five Ge capture-product .ens files are frozen; MANIFEST.md carries the curl command, byte counts and each file's full SHA-256, and the test re-computes every SHA-256 and requires it to appear in the manifest. WebFetch was not used. The test additionally requires the completeness deficit to be reported, so acquisition cannot be presented as sharpening."
      linked_ids: [claim-xs-frozen, deliv-bounds-report, deliv-capture-tests]
    test-rate-fold-bands:
      status: passed
      summary: "band-sum residual 2.07e-16 against 5e-3; node doubling 200 -> 400/decade moves the total by 1.19e-5 against 5e-3; 232 quadrature nodes inside the 1-10.14 eV gap with flux BIT-IDENTICAL (np.array_equal) to a direct parma.differential_flux call. Every band rate and the total are asserted strictly positive, discharging the never-zero rule for this channel by execution."
      linked_ids: [claim-capture-rate, deliv-capture-rate, deliv-capture-tests]
    test-westcott-not-identity:
      status: passed
      summary: "AGREEMENT IS THE FAILURE CONDITION AND IT DID NOT OCCUR. The measured ratio naive/folded = 1.3026, a +30.26% difference against the 5% minimum. The ratio is additionally asserted to differ from sqrt(pi)/2 = 0.8862 by more than 0.05, so the Westcott factor cannot have been substituted for the measurement, and the four-digit ratio is asserted present in the artifact so it is reported rather than merely computed."
      linked_ids: [claim-capture-rate, deliv-capture-rate, deliv-bounds-report, deliv-capture-tests]
    test-thermal-dominance:
      status: passed
      summary: "THE PLAN'S PRIMARY NON-IDENTITY DISCONFIRMING CHECK. Thermal fraction = 76.49% against the 60% threshold, which is asserted equal between the module constant and the test constant so it cannot drift. VERDICT: THERMAL FRAMING SURVIVES. The test requires the fraction, the verdict string AND the 23.51% non-thermal remainder to appear in both the artifact and the report, so reporting only the total would fail."
      linked_ids: [claim-capture-rate, deliv-capture-rate, deliv-bounds-report, deliv-capture-tests]
    test-doppler-sensitivity:
      status: passed
      summary: "Epithermal band recomputed with the committed 0.1 K .805nc set: +0.01016% signed relative difference (0.1 K higher), total +0.00013%. The test first asserts the two ACE sets report DIFFERENT temperature keys ('294K' vs '0K'), so the check cannot be vacuous, and then requires the signed number to appear in the artifact. The mechanism — Doppler convolution conserves the resonance integral — is stated so a near-zero shift is not read as a null cross-check."
      linked_ids: [claim-capture-rate, deliv-capture-rate, deliv-capture-tests]
    test-cascade-ceiling:
      status: passed
      summary: "All five ceilings computed from PARSED QM values and re-derived independently inside the test to 1e-12 relative, each between 100 and 1000 eV, each using the A+1 product mass. The maximum is asserted to belong to the largest Q (73Ge) AND to coincide with the isotope dominating the capture rate, computed separately from the per-isotope fold. The maximum is asserted to EXCEED the ROADMAP's illustrative 473 eV rather than being reconciled to it."
      linked_ids: [claim-cascade-bound, deliv-recoil-bounds, deliv-capture-xs, deliv-capture-tests]
    test-bound-is-cascade-free:
      status: passed
      summary: "Nine cascade-parameter settings — multiplicity 1/3/5/17, four explicit gamma-energy partitions, angular correlation isotropic / fully aligned / anti-aligned, and one combined setting — all return the bound with EXACT float equality (tolerance declared 0.0, not a relative tolerance). The bound is also asserted equal to the total capture rate and its derivation string is asserted to contain 'exactly one recoiling nucleus', so it cannot have been obtained by integrating a spectrum."
      linked_ids: [claim-cascade-bound, deliv-recoil-bounds, deliv-bounds-report, deliv-capture-tests]
    test-multiplicity-statement:
      status: passed
      summary: "Sum(E^2) = 1.8837e13 eV^2 != (Sum E)^2 = 5.4996e13 eV^2 for an explicit 3-gamma partition, ratio 0.3425. Every artifact row is asserted to carry an evidence_class in {RIGOROUS_BOUND, CONDITIONAL_ESTIMATE}, parsed with the csv module. The multiplicity_N_mean row is asserted to exist exactly once, to carry 'N SYMBOLIC' in its expression, to be labelled CONDITIONAL_ESTIMATE, and to have an EMPTY value cell."
      linked_ids: [claim-cascade-bound, deliv-recoil-bounds, deliv-capture-tests, ref-roadmap-14]
    test-inelastic-named:
      status: passed
      summary: "Natural inelastic rate 2666.83 counts/kg/day exists and is positive. The nuclear-recoil scale is asserted to exceed 1000x the 100 eV RoI top (227.2 keV vs 100 eV), while both gamma-emission recoils are asserted to lie between 0.1 and 100 eV. Both named levels (596, 834) and the word ABOVE are asserted present in the artifact and the report. Because the measured top-decade fraction is 73.55% > 10%, the test additionally requires the string flatters_SB in the artifact."
      linked_ids: [claim-inelastic-named, deliv-recoil-bounds, deliv-bounds-report, deliv-capture-tests]
  references:
    ref-neutron-decl:
      status: completed
      completed_actions: [read, use, cite]
      summary: "Phi_th = 2.767075e-3 cm^-2 s^-1 (0.01-0.5 eV, cadmium cutoff) is consumed as PHASE 9's product, named as such in the module constant, in the artifact header and in the report, and NOT re-derived. The order_of_magnitude label is carried onto every emitted rate. The phi_lo-is-indoor semantics are enforced in code by neutron_recoil's refusal, tested here. The mK caveat handed forward by Section 5 is ANSWERED with the 0.1 K recomputation rather than restated. The Section 7 directional-bias row schema is used for the nine-row table."
      linked_ids: [claim-capture-rate]
    ref-elastic-acq:
      status: completed
      completed_actions: [read, use, cite]
      summary: "data/endf_nGe_elastic_v1.1.csv's provenance-header pattern is followed: source line, retrieval, per-isotope MATs read from the file headers, ACE ZAIDs with SHA-256 heads, reader version, processing temperature, IUPAC abundances, git sha, reproduce command, and a VALIDATION block computed at generation time. It is also the precedent for preferring the pre-reconstructed ACE set over MF=3 in the resonance region — the same resolution reached here for the same reason, and stated as inherited rather than rediscovered."
      linked_ids: [claim-xs-frozen]
    ref-roadmap-14:
      status: completed
      completed_actions: [read, use]
      summary: "The two named forbidden proxies are both discharged by construction and by test. The generic '473 eV at 8 MeV' single-gamma figure is treated as an ILLUSTRATION: the Ge ceilings are computed from the actual QM values, the maximum comes out HIGHER at 754.11 eV, and the difference is explained by the Q values rather than reconciled away. SC1's 'new acquisition' turned out to be mostly already discharged by Phase 7 for the cross sections, and newly discharged here for EGAF."
      linked_ids: [claim-xs-frozen, claim-cascade-bound, claim-inelastic-named]
    ref-biffl:
      status: completed
      completed_actions: [read, compare, cite]
      summary: "The comparison is made explicitly and with its direction: Phi_th adopted / Biffl requirement = 3.95, ABOVE, so this unshielded sea-level configuration does NOT meet the stated Phi_th < 7e-4 n/cm^2/s. Biffl's statement that capture recoils strongly overlap the CEvNS signal for recoils <~ 100 eV is the regime this bound lands in. Cited from the ROADMAP's own anchor entry; the paper itself was not retrieved in this environment, so the two quoted statements are carried as the ROADMAP records them."
      linked_ids: [claim-capture-rate, claim-cascade-bound]
    ref-phase13:
      status: completed
      completed_actions: [read, compare, use]
      summary: "The elastic in-RoI 5430.287 / 5485.152 counts/kg/day are the comparison this bound sits beside, and the capture bound 4399.78 lands at 0.81 / 0.80 of them — the same order. The three-part flux path is used in its committed form, which evaluates the pinned PARMA driver at EVERY node rather than interpolating the tables at all, and the gap coverage is measured rather than inherited. The demonstrated-UNBOUNDED eV-keV flux shape term is carried into the directional-bias table with its direction left undetermined rather than assigned."
      linked_ids: [claim-capture-rate]
  forbidden_proxies:
    fp-capture-as-zero:
      status: rejected
      notes: "Rejected by REPRODUCING it deliberately and asserting it. mf3_mt102_probe_b exists solely so the test can show MF=3 MT=102 returns exactly 0.0 for all five isotopes at four energies; nothing in the fold path calls it. The operative ACE source returns 2.211522 b natural at the same energy, every band rate is asserted strictly positive, and the artifact header states the File-2 mechanism in words rather than merely switching source."
    fp-single-gamma-as-cascade:
      status: rejected
      notes: "Every ceiling row is labelled RIGOROUS_BOUND with the expression T_max = Q^2/(2 M_(A+1) c^2) written out, and the artifact header, the report and the module docstring all state that the ceiling is not the cascade answer. Sum(E^2) != (Sum E)^2 is demonstrated numerically beside them (ratio 0.3425), and the reported in-RoI bound is the RATE, which does not use the ceiling at all."
    fp-westcott-product:
      status: rejected
      notes: "The naive product is emitted only as a row literally named NAIVE_PRODUCT_NOT_THE_ANSWER, and the test makes AGREEMENT the failure condition. Measured ratio 1.3026. The near-cancellation trap — naive/TOTAL = 0.9964, which looks like corroboration — is reported explicitly in both the artifact header and the report so it cannot be mistaken for a cross-check. sqrt(pi)/2 is quoted for context only and the test asserts it differs from the measured ratio."
    fp-precision-inflation:
      status: rejected
      notes: "accuracy_label = order_of_magnitude on every row of all three artifacts, asserted by a parametrised test that parses the label column through the csv module, and in the report header. The report opens by stating the result is a BOUND, not a quantification. Many-digit values appear only as reproducibility figures for the quadrature (band-sum residual, node doubling) and for the parsing, and are labelled as such."
    fp-phi-lo-as-central:
      status: rejected
      notes: "The flux comes exclusively from neutron_recoil.neutron_flux_cm2_s_MeV on its default OUTDOOR column; the test asserts that both 'phi_lo' and 'band_midpoint' RAISE FluxColumnError. A line-level scan over capture_channel.py requires every phi_lo occurrence to be a comment or a prose string literal — a definition or a refusal, never a use. Zero uses found."
    fp-assumed-multiplicity:
      status: rejected
      notes: "No multiplicity is assigned. The T_max/N row carries an empty value cell and the literal 'N SYMBOLIC', asserted in test. The only multiplicity numbers anywhere (2.233 / 1.662 / 4.245 / 2.027) are the OBSERVED EGAF intensity sums from an integrity-checked retrieval, labelled CONDITIONAL_ESTIMATE, reported with their 60-71% completeness deficit, and used for no reported rate."
  uncertainty_markers:
    weakest_anchors:
      - "The eV-keV differential shape of the sea-level neutron flux, inherited unchanged. Phase 13 CONSTRUCTED two perturbations invisible to the channel's only independent cross-check that moved the in-RoI elastic rate by +41.33% and -16.31%. The epithermal 19.48% of this capture rate inherits that term directly and it is UNBOUNDED, not merely large. Nothing in this plan improves it."
      - "The in-RoI FRACTION of the bound. The rate bound is rigorous; converting it into an in-RoI number needs the cascade, and the EGAF completeness check shows the observed cascade carries only 60-71% of Q_cap. The bound is therefore loose by an unknown factor <= 1, and the retrieval did not close that."
      - "The thin-target formula. It is checked rather than assumed, and it FAILS at the 102.59 eV resonance where P_capture(2 mm) = 73.6%. The 11.00% epithermal overstatement is bounded by a normal-incidence slab comparison with no scattering and no angular distribution, which is indicative rather than a transport result."
      - "The 20 MeV ENDF ceiling for INELASTIC. The top-decade fraction is 73.55%, so the integrand is peaked near the ceiling and Phase 13's measured 11.85x elastic margin does not transfer. The omission is labelled and carried unquantified rather than bounded."
      - "EGAF's own normalisation for 76Ge: sigma_0 = 0.06 b against the ENDF/ACE 0.1546 b, with only 9 gammas listed and a completeness of 5.02. The row is excluded and the inconsistency reported; 76Ge carries 0.54% of the natural thermal capture so nothing downstream depends on it."
    unvalidated_assumptions:
      - "That the 293.6 K ACE processing is adequate against a mK crystal. Measured to matter at the +0.010% level for the epithermal BAND INTEGRAL, with the resonance-integral-conservation mechanism stated so the near-zero is not read as a null check. It is NOT settled for anything resolving individual resonance line shapes, and that distinction is the answer rather than a caveat."
      - "That the isotropic-cascade cross terms average to zero. True for the MEAN, and irrelevant to the rigorous rate bound, but it says nothing about the DISTRIBUTION that an in-RoI fraction would need."
      - "That the outdoor flux leg is the operative configuration. Inherited from Phase 9 as a configuration choice, not an uncertainty this plan can settle."
      - "That EGAF's per-capture intensities are internally consistent with the ENDF/ACE thermal cross sections. Verified only to the extent that four of five completeness values land in (0,1); the fifth does not, and is excluded."
    competing_explanations:
      - "A capture rate landing near the elastic in-RoI rate could be real physics or an arithmetic conflation. Separated three ways: the bands sum to the total at 2.07e-16 so nothing is double-counted across the flux tables; the 1-10.14 eV gap flux is bit-identical to the direct driver so no table edge was extrapolated; and the naive product is kept as a separately labelled row that MUST differ, which it does by 30.26%."
      - "A thermal fraction near 1 could be genuine 1/v dominance or a fold that never reached above the sub-eV table. Separated by reporting all four band rates, all non-zero, and by the gap-coverage assertion."
      - "A near-agreement between the naive product and the TOTAL (0.9964) could look like corroboration. It is not: the product overstates the thermal BAND by 30% while knowing nothing about the ~1034 counts of non-thermal capture. Two errors nearly cancelling, reported as such."
    disconfirming_observations:
      - "23.51% OF THE 'THERMAL-CAPTURE' CHANNEL IS NOT THERMAL. The verdict survives the 60% threshold at 76.49%, but the non-thermal remainder is 1034.24 counts/kg/day — itself ~8.7x the entire Phase-12 CEvNS total — so a Phase-16 budget that took the phase title literally and folded only the thermal component would understate this channel by a factor 1.31. Reported rather than absorbed into the thermal label."
      - "THE THIN-TARGET FORMULA DOES NOT HOLD EVERYWHERE. P_capture(2 mm) = 73.6% at the 102.59 eV resonance: the wafer is nearly black to capture there. The formula is used anyway and the resulting <= 11.00% epithermal overstatement is labelled penalizes_SB. This was not anticipated by the plan, whose approximation block asked only for the thermal-peak check."
      - "EGAF WAS RETRIEVABLE AND IT STILL DOES NOT CLOSE THE CASCADE. Planning recorded the line lists as unavailable and treated failure as an acceptable named gap; the retrieval succeeded, which would have looked like the gap closing. The completeness check shows the observed cascade carries only 60-71% of Q_cap, so the in-RoI fraction remains unobtainable. The gap moved from 'no data' to a measured deficit, which is a smaller claim than 'EGAF acquired' would have suggested."
      - "THE ROADMAP'S ILLUSTRATIVE 473 eV IS EXCEEDED, NOT MATCHED. The 73Ge ceiling is 754.11 eV, 59% higher, and 73Ge is also the isotope dominating the rate. Reported as the honest reading rather than reconciled to the illustration."
      - "THE ADOPTED Phi_th IS 3.95x ABOVE BIFFL'S STATED REQUIREMENT. The configuration does not meet it, and that direction is stated rather than skipped."
      - "A NAIVE WHOLE-FILE EGAF PARSE INFLATES THE PER-CAPTURE INTENSITY ~3x, because each .ens file carries three datasets with separate normalisations. It was caught by the completeness check, not by inspection, and the first parse DID produce multiplicities of 91-607 gammas per capture before the check fired."
---

# 14-01 Summary — Ge prompt (n,γ) capture: cross sections, fold, and bounds

**Status:** complete · **Suite:** green (see 14-02 for the final full-suite count)
**Report:** `GPD/phases/14-ge-only-thermal-capture-channels-p-geonly/14-01-CAPTURE-BOUNDS.md`

## Headline numbers

| quantity | value | class |
|---|---:|---|
| natural σ_(n,γ)(0.0253 eV) | **2.211522 b** | measured, unfitted |
| ⁷³Ge σ_(n,γ)(0.0253 eV) | **14.7009 b** (51.52 % of natural capture from 7.75 % of atoms) | measured, unfitted |
| **total capture rate** | **4399.78 counts kg⁻¹ day⁻¹** | folded |
| bands (thermal / epi / inter / fast) | 3365.54 / 857.08 / 167.75 / 9.41 | folded |
| **thermal dominance** | **76.49 %** — SURVIVES; 23.51 % is not thermal | verdict |
| naive Φ_th × σ₂₂₀₀ | 4383.92, ratio to folded thermal **1.3026 (+30.26 %)** | comparison, must differ |
| **rigorous in-RoI bound** | **≤ 4399.78 counts kg⁻¹ day⁻¹** = **37.1×** CEvNS total | RIGOROUS |
| single-γ ceilings | 415.77 / 338.30 / **754.11** / 302.87 / 257.07 eV | RIGOROUS |
| EGAF ⟨T⟩ bracket, ⁷³Ge | 186.5 – **408.9** eV (vs 754.1 ceiling) | RIGOROUS upper |
| inelastic rate (SC5) | **2666.83 counts kg⁻¹ day⁻¹**; recoils 227 keV ≫ RoI; γ-recoils 2.577 / 5.185 eV | RIGOROUS rate |
| Φ_th vs Biffl requirement | **3.95× ABOVE** — not met | comparison |

## Checkpoint recorded

Task 3's `checkpoint:decision` (EGAF sharpening) is recorded in
`14-01-CAPTURE-BOUNDS.md` §6 with its default (**option 1, stop at the bound**) taken under
the standing session directive, together with the two facts that changed the evidence: option
2's precondition became true, and it still does not deliver what option 2 was for.

## Deviations

- **Rule 1 (guard bug).** `tests/test_energy_grid_extension.py` and
  `tests/test_legacy_grid_disposition.py` flagged *newly added* files as "frozen artifact
  modified". A file that did not exist before cannot have had its header rewritten. Both
  predicates narrowed to exclude `A ` status while keeping `M`/`D`/`R` caught, with the reason
  recorded inline.
- **Rule 4 (missing component).** Three `np.interp` sites in the new module required rows in
  the Phase-10 interpolator inventory; added, with the closure count bumped 41 → 44 and each
  row justified (notably `left=0.0` on the two inelastic maps, which is the physics — an
  inelastic partial is exactly zero below its own threshold — and is why the thermal and
  epithermal inelastic band rates are exactly 0.0).
- **Scope note (not a deviation).** The EGAF retrieval succeeded where planning expected
  failure. Handled inside the plan's contract: the artifact is frozen and the disposition
  test passes on its acquisition branch, but no cascade Monte Carlo was run
  (`forbidden_estimator_families`) and no multiplicity was adopted.
