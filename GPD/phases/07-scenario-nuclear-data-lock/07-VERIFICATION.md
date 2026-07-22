---
phase: 07-scenario-nuclear-data-lock
verified: "2026-07-22T19:40:00Z"
status: gaps_found
score: "19/22"
plan_contract_ref: GPD/phases/07-scenario-nuclear-data-lock/07-01-PLAN.md#/contract
contract_results:
  claims:
    claim-ambient-flux:
      status: partial
      summary: "The committed table is real, grid-exact and honestly labelled, but the decisive normalization number is not reproducible from any committed artifact. INDEPENDENTLY CONFIRMED: 584 rows, 0 NaN, reconstructed 585-edge vector is byte-identical to shared_energy_grid() (np.array_equal True with float_precision='round_trip'); phi_hi == phi_default and phi_lo == phi_default/5 exactly (one-sided-downward band); on-grid integrals reproduce the header to 4 digits (broad 10.14 eV-197 MeV = 9.0518e-03 vs 9.052e-03; 10-197 MeV = 2.8196e-03 vs 2.820e-03); the omitted fraction is 20.57%, matching the header's '~21%'; the evaporation hump peaks at 1.91 MeV and the cascade peak at 121 MeV (E*phi), both canonical. NOT CONFIRMED: Phi(10 MeV-10 GeV)=3.550e-03 and Phi(thermal->10 GeV)=1.317e-02 are full-range PARMA integrals evaluated OFF the committed grid; no PARMA build/eval script was committed, so neither number can be recomputed in-repo. The anchor VALUE is externally corroborated (see comparison_verdicts ref-gordon), and the internal arithmetic is self-consistent (3.239e-03 x k=1.09610 = 3.5504e-03), but the artifact-to-anchor step rests on assertion."
      linked_ids: [deliv-ambient-flux, deliv-scenario-note, test-ambient-integrals, ref-gordon]
    claim-radiopurity:
      status: passed
      summary: "Independently recomputed all three assay conversions from specific activities and isotopic abundances: 238U spec. act. = 12436 Bq/g -> 1 ppb U = 12.44 mBq/kg (header 12.44, exact); 232Th = 4057 Bq/g -> 1 ppb Th = 4.057 mBq/kg (header 4.057, exact); 238U SF neutron yield recomputed as 1.34-1.40e-11 n/g/s/ppb depending on (branching ratio, nu), bracketing the recorded Mei-Zhang-Hime 1.353e-11. Every per-component ppb/ppm entry round-trips against its mBq/kg default to the quoted 2 significant figures (e.g. housing U 5.0e-2/12.4 = 0.0040 ppb; PCB Th 1.0/4.06 = 0.246 ppb; PCB K 10/31 = 0.323 ppm). Exactly one representative default per component with lo/hi band, gamma (CALC-07) and (alpha,n)+SF (CALC-08) routing columns present with low-Z flags, Ge bulk flagged context_only and not summed. Residual: nat-K 31.03 Bq/g requires the older T_1/2(40K)=1.277e9 yr; the current evaluated 1.248e9 yr gives 31.72 Bq/g (+2.3%), so the header's '<1%' re-derivation claim is half-life-choice dependent - immaterial against the >2-order assay band."
      linked_ids: [deliv-radiopurity, deliv-scenario-note, test-radiopurity-conversions, ref-majorana, ref-mzh]
    claim-activation-scenario:
      status: passed
      summary: "Recomputed A = R(1-exp(-lambda t_exp))exp(-lambda t_cool) from scratch with lambda = ln2/t_half and t_yr = 365.25 d. Every committed number reproduces: satfrac(1 yr) = 0.0547 / 0.6074 / 0.6458 and A = 4.048 / 18.221 / 10.979 dec/kg/day for 3H / 68Ge / 65Zn (committed 0.0547/0.6074/0.6458 and 4.05/18.22/10.98); band endpoints 1.034 (3H, 0.25 yr, CDMSlite) and 12.735 / 66.703 / 101.291 (3 yr, EDELWEISS) reproduce 1.03 / 12.74 / 66.70 / 101.29. Substituting the current evaluated half-lives (68Ge 270.95 d, 65Zn 243.93 d) changes A by <0.04%. The executor's FINDING is CORRECT and the PLAN text was wrong: at t_exp = 1 yr 68Ge and 65Zn are at 60.7% and 64.6% of R, NOT saturated at ~30 and ~17 as test-activation-band's pass_condition asserted. The CSV carries as-deployed activity, not saturation activity, so fp-saturation-3H is rejected in its strong form (all three isotopes, not just 3H)."
      linked_ids: [deliv-activation, deliv-scenario-note, test-activation-band, ref-cdmslite, ref-edelweiss]
    claim-axis-discipline:
      status: passed
      summary: "Grepped all seven committed Phase-7 artifacts (3 scenario CSVs, 2 ENDF CSVs, the assumptions note, both src/nuclear modules) for keVee / Lindhard / quench / QF / NUCLEUS / CONUS / RELICS: every hit is a prohibition or guard sentence, zero are applications. No recoil kernel, no dsigma/dT transform, no spectrum fold and no response fold exists anywhere in the phase - confirmed by grep and by the phase commit file list (78f7728..HEAD touches only the 3 scenario CSVs, the note, the 2 ENDF CSVs, 5 raw ENDF .dat files, and 2 src/nuclear modules). The flux table is correctly tagged as an INCIDENT-NEUTRON-ENERGY (E_n) axis, not keV_nr, with an explicit E_n != E_nr warning - this deviates from ROADMAP criterion 5's literal 'keV_nr axis tag' wording and is the physically correct choice. No underground/shielded residual is used as the surface baseline; the surface value is explicitly the upper case."
      linked_ids: [deliv-ambient-flux, deliv-radiopurity, deliv-activation, deliv-scenario-note, test-axis-grep, ref-conventions-B]
  deliverables:
    deliv-ambient-flux:
      status: passed
      path: data/ambient_neutron_flux_v1.1.csv
      summary: "Exists, 584 data rows + 68 header lines, 0 NaN, monotone edges, grid byte-identical to shared_energy_grid(). Carries every must_contain item: PARMA/Sato-2015 shape source with repository commit 6ff37ca and Sato 2015 DOI, the documented Gordon->PARMA reference-model change, (depth=surface/0 m.w.e.; shielding=none-outdoor + downward building band; site=sea-level NYC) provenance tag, the E_n axis tag with the keV_nr/no-quenching pointer, explicit phi_lo/phi_hi band columns, and both integral labels with the on-grid subset separately reported. Reproducibility caveat recorded under Discrepancies: no generator script committed."
      linked_ids: [claim-ambient-flux, claim-axis-discipline, test-ambient-integrals]
    deliv-radiopurity:
      status: passed
      path: data/radiopurity_budget_v1.1.csv
      summary: "Exists, 15 component-nuclide rows over 5 components, provenance-headed. All must_contain items present: representative default + lo(electroformed-Cu 3e-4 mBq/kg)/hi(commercial) band per component, the three conversion constants plus p_gamma(1460.8 keV)=0.1067, the gamma vs (alpha,n)+SF channel split with the 1.353e-11 n/g/s/ppb SF yield and per-component low-Z flags. Not a bare open bracket: a single default exists on every row."
      linked_ids: [claim-radiopurity, test-radiopurity-conversions]
    deliv-activation:
      status: passed
      path: data/activation_scenario_v1.1.csv
      summary: "Exists, 3 isotope rows, provenance-headed. Carries t_exp=1 yr / t_cool=0, per-isotope R with CDMSlite and EDELWEISS provenance, t_half, lambda, saturation fraction, as-deployed A (not saturation), the t_exp in [0.25, 3] yr band, and an explicit saturating_flag column recording 3H as never_saturates_linear."
      linked_ids: [claim-activation-scenario, test-activation-band]
    deliv-scenario-note:
      status: passed
      path: docs/v1.1-scenario-assumptions.md
      summary: "Exists with one section per gating input, each carrying default + band + citation + provenance tag + axis tag. Contains the CONVENTIONS Sec.B FORBIDDEN guard verbatim-in-intent, the surface-vs-underground non-transferability guard naming NUCLEUS/CONUS/RELICS as post-shield residuals, the block/scope-repair trigger, and the documented Gordon->PARMA reference-model change with its USER DECISION provenance."
      linked_ids: [claim-axis-discipline]
  acceptance_tests:
    test-ambient-integrals:
      status: partial
      summary: "Reproduced everything that is on-grid; could not reproduce the decisive off-grid anchor. Executed: on-grid broad = 9.0518e-03 and on-grid 10-197 MeV = 2.8196e-03 cm^-2 s^-1, both matching the header; the two range labels ARE explicitly reconciled in the header and in the note, and the ~21% cascade-tail omission is disclosed honestly rather than buried; (depth,shielding) and axis tags present; shape coefficients sourced from open PARMA code with a pinned commit, not from memory. Not executed: Phi(10 MeV-10 GeV)=3.550e-03 and Phi(0.01 eV-10 GeV)=1.317e-02 require a PARMA evaluation above the 197 MeV grid ceiling, and no PARMA driver was committed. A naive power-law extrapolation of the committed table's last decade (log-slope -0.72) is not a usable substitute because the spectrum is still at its cascade peak at the grid ceiling. Hence partial, not passed."
      linked_ids: [claim-ambient-flux, deliv-ambient-flux, ref-gordon]
    test-radiopurity-conversions:
      status: passed
      summary: "Round-trip executed for U, Th and K from first principles (NA, half-lives, molar masses, isotopic abundances) and against every committed per-component row. U and Th reproduce exactly; SF yield reproduces to within the branching-ratio/nu spread; nat-K reproduces to 2.3% under the current evaluated 40K half-life. A single representative default per component with a lo/hi band and the full gamma vs (alpha,n)+SF split is present."
      linked_ids: [claim-radiopurity, deliv-radiopurity, ref-majorana, ref-mzh]
    test-activation-band:
      status: passed
      summary: "Executed independently for all three isotopes at t_exp in {0.25, 1, 3} yr with t_cool = 0; all nine committed activities reproduce to the quoted precision. Limiting cases hold: A->0 as t_exp->0, A->R for 68Ge/65Zn as t_exp->inf, and 3H stays at 5.5% of R at 1 yr growing near-linearly. The plan's own pass_condition ('68Ge -> R (~30) and 65Zn -> R (~17) saturate within ~1 yr') is FALSE and the executor corrected it in the deliverable; the corrected physics is what was committed."
      linked_ids: [claim-activation-scenario, deliv-activation, ref-cdmslite, ref-edelweiss]
    test-axis-grep:
      status: passed
      summary: "Executed. Zero applied QF/Lindhard/keVee tokens across all committed Phase-7 artifacts; every occurrence is a guard. Energy-axis bin identity re-verified programmatically against shared_energy_grid() (exact float equality on all 585 edges once the CSV is parsed with round-trip float precision; the apparent 9e-15 mismatch under default pandas parsing is a parser ULP artifact, not an artifact defect). No shielded/underground residual used as the surface baseline."
      linked_ids: [claim-axis-discipline, deliv-ambient-flux, deliv-radiopurity, deliv-activation, deliv-scenario-note, ref-conventions-B]
  references:
    ref-gordon:
      status: missing
      completed_actions: [use, compare, cite]
      missing_actions: [read]
      summary: "The Gordon 2004 IEEE TNS paper itself was never read - it is paywalled and its differential coefficients were correctly declared unsourceable rather than reconstructed from memory. Its role was re-scoped by USER DECISION to integral normalization benchmark only, and in that role it is used, compared and cited (both in the CSV header and the note). The required 'read' action is therefore genuinely incomplete, but the substitution is documented in the artifact header, the assumptions note and the SUMMARY, and the decisive number is independently corroborated (see comparison_verdicts). Non-blocking; recorded for honesty."
    ref-majorana:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Electroformed-Cu <0.3 uBq/kg U/Th is the lo anchor on every housing/mount row and the commercial mBq-Bq/kg range is the hi anchor; both cited in the CSV header and the note. The quoted electroformed-Cu figure matches the standard MAJORANA assay value."
    ref-mzh:
      status: completed
      completed_actions: [use, cite]
      missing_actions: []
      summary: "The 238U SF yield 1.353e-11 n/g/s/ppb is recorded in the radiopurity header and cited to NIMA 606, 651 (2009) / arXiv:0812.4307. Independently recomputed as 1.34-1.40e-11 from the 238U specific activity, the SF branching ratio and nu, so the cited constant is consistent rather than merely transcribed."
    ref-cdmslite:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "3H 74+-9, 65Zn 17+-5, 68Ge 30+-18 atoms/kg/day used as the central production rates, cited to arXiv:1806.07043 in the CSV provenance column, and compared against the computed as-deployed activities (see comparison_verdicts)."
    ref-edelweiss:
      status: completed
      completed_actions: [compare, cite]
      missing_actions: []
      summary: "3H 82+-21, 65Zn 106+-13, 68Ge >71 atoms/kg/day used as the upper band anchor and cited to arXiv:1607.04560. The 68Ge entry is correctly flagged as a lower limit in the provenance column, so the upper band edge for 68Ge is honestly labelled as a bound rather than a measurement."
    ref-conventions-B:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "CONVENTIONS.md Sec.B is quoted in intent in the assumptions note (no keVee<->keVnr mixing; no Lindhard/QF on the phonon scale; QF only ever used to un-quench an imported keVee number) and every committed artifact carries the corresponding axis guard."
    ref-gamma-header:
      status: completed
      completed_actions: [use]
      missing_actions: []
      summary: "All three scenario CSVs follow the data/gamma_lines.csv documented-tunable-input pattern: '#'-prefixed provenance block separating WHAT IS FIXED from WHAT IS TUNABLE, explicit citations, then a machine-readable columns line."
  forbidden_proxies:
    fp-quenching:
      status: rejected
      notes: "No Lindhard or QF factor appears anywhere as an applied operation; all occurrences of the tokens are prohibitions. Verified by grep across all seven committed artifacts."
    fp-underground-import:
      status: rejected
      notes: "NUCLEUS/CONUS/RELICS appear only in the note's explicit non-transferability guard. The committed normalization is an unshielded outdoor sea-level PARMA spectrum anchored to Gordon, and the surface case is set as the upper anchor. This proxy is also the documented reason Input 1 was blocked rather than back-filled."
    fp-open-bracket:
      status: rejected
      notes: "Every component-nuclide row carries a single activity_default_mBq_kg value; the >2-order electroformed<->commercial spread survives only in the activity_lo/activity_hi columns."
    fp-saturation-3H:
      status: rejected
      notes: "Rejected more strongly than the contract required. The CSV quotes as-deployed A per isotope with its own lambda; I independently confirmed that 68Ge and 65Zn are also NOT saturated at 1 yr (60.7% and 64.6% of R), so the phase avoided the saturation proxy for all three isotopes rather than only for 3H."
  uncertainty_markers:
    weakest_anchors:
      - "Phi(10 MeV-10 GeV) = 3.55e-3 cm^-2 s^-1 is asserted from an off-grid PARMA evaluation with no committed driver script; only the on-grid subset and the internal k-scaling arithmetic are reproducible in-repo."
      - "sigma_tot(1-2 MeV) = 3.729 b, which sets Sigma/lambda/P_int, is recorded only in a header - no total cross-section column is committed. Recomputing it from the (gitignored) ACE MT=1 gives 3.6916 b under log-grid quadrature, a 1.0% quadrature-definition spread."
      - "The sub-MeV sigma_el exists ONLY in the gitignored 58 MB ACE binaries: MF=3 MT=2 in the committed raw ENDF text is identically zero through each isotope's resolved+URR region, so a clean clone cannot regenerate the resonance data without network access."
      - "Gordon 2004 itself was never read (paywalled); its integral reaches the project through secondary open sources."
    unvalidated_assumptions:
      - "Log-log interpolation is applied to NJOY-linearised pointwise data whose ENDF-defined interpolation law is lin-lin."
      - "The 293.6 K ACE processing is used as the baseline for a mK cryogenic target; only band integrals were shown insensitive."
      - "A scalar factor-of-5 building-shielding band stands in for indoor spectral-shape moderation."
      - "sigma_tot is treated as a flat band-mean over 1-2 MeV for the mean-free-path check."
    competing_explanations:
      - "The +6.0% offset of the committed epithermal plateau against the NIST free-atom value could be the bound->free correction plus low-lying resonance tails (expected physics) or a small thermal-region normalization difference; the committed data do not separate them."
    disconfirming_observations:
      - "The plan's literal mesh-halving criterion fails: node decimation of the union grid shifts the 0.1 keV-1 MeV integral by 1.817%, against a <0.5% pass condition. I reproduced this number exactly."
      - "The substituted union-vs-native metric is identically 0.000000% under lin-lin interpolation for all five isotopes, so the reported 0.0458-0.1117% measures interpolation-scheme mismatch, not mesh convergence or resonance clipping."
      - "sigma_el falls to ~2.0 b over 2-10 MeV, outside the plan's stated 3-7 b fast band; the ledger verdict for that comparison is recorded as pass against a '3-7 b across 0.1-10 MeV' threshold the data does not meet as literally written."
      - "The committed n-Ge elastic table stops at 20 MeV while the committed flux table runs to 197 MeV; 26.9% of the on-grid ambient flux (86.4% of the on-grid >10 MeV flux) has no elastic cross section, and this mismatch is not flagged in any Phase-7 artifact."
      - "REQUIREMENTS.md CALC-06/VALD-05 and ROADMAP still carry T_max/E_n = 0.0538 while the computed values are 0.0536 (mass-number form) and 0.0541 (mass-ratio form); the executor flagged the discrepancy but did not propagate a correction."
comparison_verdicts:
  - subject_id: ref-gordon
    subject_kind: reference
    subject_role: decisive
    reference_id: ref-gordon
    comparison_kind: benchmark
    metric: Phi_10MeV_to_10GeV_cm2_s
    threshold: "3.5-3.6e-3 cm^-2 s^-1 (sea-level, NYC vertical cutoff)"
    verdict: pass
    notes: "The anchor VALUE is externally corroborated by an independent literature check performed during this verification: Gordon et al. 2004 give 3.5-3.6e-3 cm^-2 s^-1 for the 10 MeV-10 GeV integral at sea-level NYC, and EXPACS/PARMA is independently reported at ~3.3e-3 for the same range. That second number corroborates the artifact's un-tuned PARMA native integral of 3.239e-3 and therefore its k=1.09610 anchor factor as a genuine ~10% adjustment rather than a large fudge."
  - subject_id: claim-ambient-flux
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-gordon
    comparison_kind: benchmark
    metric: Phi_10MeV_to_10GeV_cm2_s
    threshold: "committed table must reproduce 3.5-3.6e-3 cm^-2 s^-1"
    verdict: inconclusive
    recommended_action: "Commit the PARMA evaluation driver (or a frozen full-range PARMA phi table extending to 10 GeV) so the >10 MeV and broad anchor integrals can be recomputed from repository contents alone."
    notes: "Integrating the committed table gives 2.8196e-03 cm^-2 s^-1 over 10-197 MeV. The claimed 3.550e-03 is a full-range integral evaluated off-grid in PARMA; no committed artifact permits its recomputation. The 20.57% shortfall I measured matches the header's disclosed ~21% cascade-tail omission exactly, so the labelling is honest and internally consistent - but the comparison itself remains undischarged in-repo."
  - subject_id: claim-activation-scenario
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-cdmslite
    comparison_kind: benchmark
    metric: as_deployed_activity_dec_kg_day
    threshold: "A = R(1-exp(-lambda t_exp)) at t_exp = 1 yr, t_cool = 0"
    verdict: pass
    notes: "Recomputed independently: 4.048 / 18.221 / 10.979 dec/kg/day for 3H / 68Ge / 65Zn versus committed 4.05 / 18.22 / 10.98. Saturation fractions 0.0547 / 0.6074 / 0.6458 confirm the executor's correction that 68Ge and 65Zn are NOT saturated at 1 yr, contradicting the plan's own pass_condition. Robust to the half-life update (<0.04% change)."
  - subject_id: claim-radiopurity
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-mzh
    comparison_kind: benchmark
    metric: ppb_to_activity_and_SF_neutron_yield
    threshold: "1 ppb U = 12.4 mBq/kg, 1 ppb Th = 4.06 mBq/kg, SF = 1.353e-11 n/g/s/ppb"
    verdict: pass
    notes: "12.436 and 4.057 mBq/kg reproduced from specific activities to better than 0.1%; SF yield recomputed as 1.34-1.40e-11 n/g/s/ppb from the 238U specific activity times branching ratio times nu, bracketing the cited constant. nat-K is the one soft spot: 31.72 Bq/g with the current 40K half-life versus the header's 31.03 Bq/g (+2.3%, not <1%)."
  - subject_id: ref-majorana
    subject_kind: reference
    subject_role: decisive
    reference_id: ref-majorana
    comparison_kind: benchmark
    metric: radiopurity_bracket_uBq_kg
    threshold: "electroformed Cu < 0.3 uBq/kg U/Th as the optimistic anchor; commercial materials mBq-Bq/kg as the pessimistic anchor"
    verdict: pass
    notes: "Read directly off the committed CSV: the housing U238/Th232 lo anchors are 3.0e-4 mBq/kg = 0.30 uBq/kg exactly, reproducing the MAJORANA electroformed-Cu figure, and the hi anchors span 2.0 mBq/kg (Cu) to 1.0e2 mBq/kg (FR4), i.e. the commercial mBq-Bq/kg range. The bracket is used only as the band; every row carries a single representative default between the anchors."
  - subject_id: ref-edelweiss
    subject_kind: reference
    subject_role: decisive
    reference_id: ref-edelweiss
    comparison_kind: benchmark
    metric: production_rate_atoms_kg_day
    threshold: "3H 82+-21, 65Zn 106+-13, 68Ge >71 atoms/kg/day as the upper band anchor"
    verdict: pass
    notes: "The three EDELWEISS-III rates appear verbatim in R_EDELWEISS_atoms_kg_day and drive the upper band. I recomputed the resulting activities: 4.486 / 43.124 / 68.459 dec/kg/day at 1 yr and 12.735 / 66.703 / 101.291 at 3 yr, reproducing the committed A_EDELWEISS_1yr and A_band_hi_EDELWEISS_3yr columns. The 68Ge entry is correctly flagged as a lower limit in the provenance column, so that band edge is labelled as a bound rather than a measurement."
suggested_contract_checks:
  - check: "committed reproducibility path for the ambient-flux normalization anchor"
    reason: "The decisive Phi(>10 MeV) and broad integrals are asserted from an off-grid PARMA evaluation with no committed driver, so the artifact-to-anchor step cannot be re-executed from the repository."
    suggested_subject_kind: acceptance_test
    suggested_subject_id: test-ambient-integrals
    evidence_path: data/ambient_neutron_flux_v1.1.csv
  - check: "cross-artifact energy-range consistency between phi(E_n) and sigma_el(E_n)"
    reason: "The frozen n-Ge elastic table ends at 20 MeV while the frozen flux table runs to 197 MeV; 26.9% of the on-grid ambient flux has no elastic cross section and no Phase-7 artifact records this, so Phase 9 (CALC-06) would silently truncate or silently extrapolate."
    evidence_path: data/endf_nGe_elastic_v1.1.csv
  - check: "interpolation-law consistency for ENDF pointwise cross sections"
    reason: "sigma_el is mapped native->union by log-log interpolation while NJOY linearises the grid for lin-lin interpolation; the committed values deviate from the ENDF-defined lin-lin interpolant by up to 4.0% pointwise in the resonance band."
    evidence_path: src/nuclear/parse_endf_nGe.py
  - check: "a valid mesh-refinement criterion for the union grid"
    reason: "The reported union-vs-native metric is identically zero under lin-lin interpolation and therefore cannot detect resonance clipping or quantify quadrature error; the literal decimation test gives 1.817% against a <0.5% pass condition."
    evidence_path: data/endf_nGe_elastic_v1.1.csv
  - check: "propagate the corrected natural-Ge recoil endpoint into REQUIREMENTS/ROADMAP"
    reason: "REQUIREMENTS.md CALC-06 and VALD-05 and ROADMAP still specify T_max/E_n = 0.0538 while the computed values are 0.0536 (4A/(1+A)^2) and 0.0541 (mass-ratio form); Phase 9's VALD-05 check would be run against a stale label."
    evidence_path: GPD/REQUIREMENTS.md
---

<!-- ASSERT_CONVENTION: metric_signature=not_applicable — no relativistic field theory in this detector/rate pipeline, fourier_convention=not_applicable, natural_units=internal-only (hbar=c=1) for CEvNS cross section; k_B EXPLICIT (not =1); I/O in eV/keV/MeV, counts/kg/day/keV, s, cm/um; (hbar c)^2 = 3.894e-28 GeV^2 cm^2 -->

**Convention lock asserted for this phase** : *natural units* are internal-only (ħ=c=1) for the CEvNS cross section; k_B is EXPLICIT (not =1); I/O in eV/keV/MeV, counts/kg/day/keV, s, cm/µm; (ħc)² = 3.894e-28 GeV²·cm². This matches `GPD/STATE.md` § Convention Lock verbatim. Phase-7-specific axis discipline: incident-neutron tables carry an E_n axis tag (explicitly *not* keV_nr), recoil quantities carry keV_nr, and no ionization quenching is applied anywhere (CONVENTIONS §B).

# Phase 7 Verification — Scenario & Nuclear-Data Lock (v1.1)

**Mode:** initial verification (no prior `07-VERIFICATION.md`).
**Scope:** the phase goal and the five ROADMAP success criteria, spanning both plans (07-01 scenario lock, 07-02 ENDF acquisition).
**Ledger scope note:** the frontmatter ledger is bound to `07-01-PLAN.md#/contract` (the lead plan, which owns 4 of the 5 ROADMAP criteria), following the project's existing single-ref convention for multi-plan phases. Plan 07-02's contract is verified with equal rigour in **§ Plan 07-02 Contract Coverage** below, and its open items are carried as unbound `suggested_contract_checks`.
**Verdict:** `gaps_found` — **the phase goal is substantially achieved**; every gating number I could recompute reproduced, and several are stronger than claimed. The gaps are evidence-quality and cross-artifact-consistency issues, none of which invalidate a committed number.

---

## Per-Criterion Verdicts (ROADMAP Phase 7)

| # | Success criterion | Verdict | Basis |
|---|---|---|---|
| 1 | Ambient-neutron normalization fixed to a cited default, factor-of-a-few band, (depth,shielding) tag | **PARTIAL** | Table, grid identity, band and tags all verified; the decisive off-grid anchor integral is not reproducible in-repo |
| 2 | Radiopurity budget fixed to representative assays + band, ppb↔activity recorded | **PASS** | U/Th conversions recomputed exactly; single default per component; γ vs (α,n)+SF split present; nat-K 2.3% soft |
| 3 | Exposure/cool-down scenario fixed, 3H/68Ge/65Zn band consistent with CDMSlite/EDELWEISS | **PASS** | All nine activities recomputed and reproduced; plan's saturation error found and corrected by the executor |
| 4 | ENDF/B-VIII.0 σ_el for 5 isotopes, published values on a resonance-resolved union grid, λ ~ 5–6 cm | **PASS (with noted marginals)** | σ_el reproduced from raw ENDF and ACE independently; union grid proven complete; λ = 6.076 cm just above the stated band because σ_tot is data-derived, not the assumed 4 b |
| 5 | Every fixed input keV_nr-tagged; no keVee/Lindhard anywhere | **PASS** | Zero applied quenching tokens; flux table correctly tagged E_n (not keV_nr) with an explicit E_n ≠ E_nr warning — a deviation from the literal wording that is physically correct |

**Overall phase verdict: goal achieved with gaps.** Four of five criteria pass; criterion 1 is partial on reproducibility, not on correctness.

---

## Computational Verification Details

All checks below were executed in this session against the committed artifacts and the locally present ACE/ENDF files. Every number labelled "recomputed" was produced by code run here, not read from a header.

### Check 1 — Grid identity and ambient-flux integrals

```python
import numpy as np, pandas as pd, sys
sys.path.insert(0,'src')
from qpd_potential.muon_deposit import shared_energy_grid
df = pd.read_csv('data/ambient_neutron_flux_v1.1.csv', comment='#', float_precision='round_trip')
edges = shared_energy_grid()
rec = np.concatenate([df.E_n_lo_keV.values, [df.E_n_hi_keV.values[-1]]])
print('byte-identical:', np.array_equal(rec, edges))
dE = (df.E_n_hi_keV.values - df.E_n_lo_keV.values)/1e3
phi = df.phi_default_cm2_s_MeV.values
print('broad on-grid %.5e' % np.sum(phi*dE))
print('>10MeV on-grid %.5e' % np.sum((phi*dE)[df.E_n_lo_keV.values >= 1e4]))
print('phi_hi==default:', np.allclose(df.phi_hi_cm2_s_MeV, phi),
      ' phi_lo==default/5:', np.allclose(df.phi_lo_cm2_s_MeV, phi/5))
print('missing frac of >10MeV anchor:', 1 - 2.81956e-3/3.55e-3)
```

**Output:**

```output
byte-identical: True
broad on-grid 9.05178e-03
>10MeV on-grid 2.81956e-03
phi_hi==default: True  phi_lo==default/5: True
missing frac of >10MeV anchor: 0.2057464788732395
```

**PASS** for grid identity, band structure and on-grid integrals (header: 9.052e-03, 2.820e-03, ~21%). Note: the header's "byte-identical" claim only reproduces with `float_precision='round_trip'`; default pandas parsing shows a 9e-15 ULP drift on 215 of 585 edges. That is a parser artifact, not an artifact defect, but anyone re-checking this claim must use round-trip parsing.

**INCONCLUSIVE** for the full-range anchor: Φ(10 MeV–10 GeV) = 3.550e-03 lives above the 197 MeV grid ceiling and no PARMA driver is committed. Attempting a power-law extrapolation of the last decade gives a log-slope of −0.72 (still on the cascade peak), which diverges upward and is unusable — recorded so the failure to substitute is explicit rather than papered over.

### Check 2 — Activation A(t), fully independent recomputation

```python
import numpy as np
ln2, yr = np.log(2), 365.25
for name, th, R_c, R_e in [('3H',4499.9,74,82), ('68Ge',270.8,30,71), ('65Zn',243.9,17,106)]:
    lam = ln2/th
    sat = 1-np.exp(-lam*yr)
    print('%-5s lam=%.5e satfrac=%.4f A_cdms=%.3f A_edw=%.3f lo(0.25yr)=%.3f hi(3yr)=%.3f'
          % (name, lam, sat, R_c*sat, R_e*sat,
             R_c*(1-np.exp(-lam*0.25*yr)), R_e*(1-np.exp(-lam*3*yr))))
```

**Output:**

```output
3H    lam=1.54036e-04 satfrac=0.0547 A_cdms=4.048 A_edw=4.486 lo(0.25yr)=1.034 hi(3yr)=12.735
68Ge  lam=2.55963e-03 satfrac=0.6074 A_cdms=18.221 A_edw=43.124 lo(0.25yr)=6.253 hi(3yr)=66.703
65Zn  lam=2.84193e-03 satfrac=0.6458 A_cdms=10.979 A_edw=68.459 lo(0.25yr)=3.886 hi(3yr)=101.291
```

**PASS.** Committed values 4.05 / 18.22 / 10.98 and band 1.03 / 12.74 / 6.25 / 66.70 / 3.89 / 101.29 all reproduce. Repeating with the current evaluated half-lives (68Ge 270.95 d, 65Zn 243.93 d) changes A by <0.04%. **The plan's own acceptance-test text was wrong** — 68Ge and 65Zn are at 60.7% and 64.6% of R at 1 yr, not saturated — and the committed CSV carries the corrected as-deployed values. This is a case where the executor disconfirmed its own plan and recorded it; that is the right behaviour.

### Check 3 — Radiopurity conversions from first principles

```python
import numpy as np
NA, yr, ln2 = 6.02214076e23, 365.25*86400, np.log(2)
spec = lambda T_yr, M: ln2/(T_yr*yr)*NA/M          # Bq per gram of pure nuclide
a238, a232 = spec(4.468e9, 238.0508), spec(1.405e10, 232.0381)
print('1 ppb U  -> %.3f mBq/kg' % (a238*1e-6*1000))
print('1 ppb Th -> %.3f mBq/kg' % (a232*1e-6*1000))
for T, ab in [(1.248e9, 1.17e-4), (1.277e9, 1.17e-4)]:
    print('natK (T=%.3fe9 yr) = %.2f Bq/g' % (T/1e9, ln2/(T*yr)*NA/39.0983*ab))
for br, nu in [(5.45e-7, 2.07), (5.4e-7, 2.00)]:
    print('SF yield br=%.3g nu=%.2f -> %.4e n/g/s/ppb' % (br, nu, a238*1e-9*br*nu))
```

**Output:**

```output
1 ppb U  -> 12.436 mBq/kg
1 ppb Th -> 4.057 mBq/kg
natK (T=1.248e9 yr) = 31.72 Bq/g
natK (T=1.277e9 yr) = 31.00 Bq/g
SF yield br=5.45e-07 nu=2.07 -> 1.4030e-11 n/g/s/ppb
SF yield br=5.4e-07 nu=2.00 -> 1.3431e-11 n/g/s/ppb
```

**PASS.** U (12.44) and Th (4.057) match the header exactly; SF 1.353e-11 sits inside the recomputed 1.34–1.40e-11 spread. **Minor discrepancy:** the header's nat-K 31.03 Bq/g and its "<1%" re-derivation claim require the superseded T½(40K)=1.277e9 yr; the current evaluated 1.248e9 yr gives 31.72 Bq/g (+2.3%). Immaterial against a >2-order assay band, but the "<1%" wording is not defensible with current decay data.

### Check 4 — n-Ge σ_el reproduced independently from the ACE binaries

```python
import endf, numpy as np
ab = {70:0.2057, 72:0.2745, 73:0.0775, 74:0.3650, 76:0.0773}
tot, el = {}, {}
for A in ab:
    inc = endf.IncidentNeutron.from_ace(f'data/endf/ace/320{A}.800nc')
    tot[A] = inc.reactions[1].xs['294K']; el[A] = inc.reactions[2].xs['294K']
g = np.geomspace(1e6, 2e6, 4001)
st = sum(ab[A]*np.interp(g, tot[A].x, tot[A].y) for A in ab)
print('nat sigma_tot mean 1-2 MeV = %.4f b (header 3.729)' % (np.trapz(st, g)/1e6))
for e in [1.2e6, 2e6, 5e6, 1e7]:
    print(' E=%.3g eV sigma_el=%.4f' % (e, sum(ab[A]*np.interp(e, el[A].x, el[A].y) for A in ab)))
xx = el[73].x[(el[73].x>=1e2)&(el[73].x<=1e6)]; yy = el[73].y[(el[73].x>=1e2)&(el[73].x<=1e6)]
i = np.argmax(yy)
print('73Ge peak = %.1f b at %.4e eV' % (yy[i], xx[i]))
```

**Output:**

```output
nat sigma_tot mean 1-2 MeV = 3.6916 b (header 3.729)
 E=1.2e+06 eV sigma_el=3.0973
 E=2e+06 eV sigma_el=1.9985
 E=5e+06 eV sigma_el=2.0551
 E=1e+07 eV sigma_el=2.2121
73Ge peak = 8533.0 b at 1.0259e+02 eV
```

**PASS.** Every committed spot value reproduces exactly (1.2 MeV = 3.0973, 2 MeV = 1.9985, 5 MeV = 2.0551, 10 MeV = 2.2121 b), as does the 293.6 K Ge-73 resonance peak of 8533.0 b at 102.59 eV. Re-reading the 0.1 K `.805nc` table gives 9253.7 b at the same energy, exactly matching the header's Doppler statement. σ_tot(1–2 MeV) recomputes to 3.6916 b against the header's 3.729 b — a 1.0% quadrature-definition difference (log grid vs union-node trapezoid), not an error, but it means Σ/λ/P_int inherit a ~1% definitional wobble.

I also verified the recorded ACE SHA-256 heads: all five `.800nc` files hash to exactly the recorded 16-hex-digit prefixes.

### Check 5 — Union-grid completeness, endpoints and the mean free path

```python
import endf, numpy as np, pandas as pd
nat = pd.read_csv('data/endf_nGe_elastic_v1.1.csv', comment='#', float_precision='round_trip')
U, s = nat.E_eV.values, nat.sigma_el_natural_b.values
for A in [70,72,73,74,76]:
    x = endf.IncidentNeutron.from_ace(f'data/endf/ace/320{A}.800nc').reactions[2].xs['294K'].x
    idx = np.clip(np.searchsorted(U, x), 1, U.size-1)
    d = np.minimum(abs(U[idx]-x), abs(U[idx-1]-x))/np.maximum(x, 1e-30)
    print(A, 'native pts', x.size, ' nodes absent from union (rel gap>1e-6):', int((d>1e-6).sum()))
m = (U>=1e5)&(U<=1e6)
print('0.1-1 MeV: %d nodes, frac in 3-7 b = %.4f, median %.4f b' % (m.sum(), np.mean((s[m]>=3)&(s[m]<=7)), np.median(s[m])))
ab = {70:0.2057,72:0.2745,73:0.0775,74:0.3650,76:0.0773}
print('per-isotope 4A/(1+A)^2:', {A: round(4*A/(1+A)**2, 4) for A in ab})
print('abundance-weighted = %.6f' % sum(ab[A]*4*A/(1+A)**2 for A in ab))
N = 5.323*6.02214076e23/72.63; Sig = N*3.729e-24
print('N_Ge=%.4e Sigma=%.4f lambda=%.4f P_int(2mm)=%.3f%%' % (N, Sig, 1/Sig, 100*(1-np.exp(-Sig*0.2))))
```

**Output:**

```output
70 native pts 4247  nodes absent from union (rel gap>1e-6): 1
72 native pts 3508  nodes absent from union (rel gap>1e-6): 1
73 native pts 12165  nodes absent from union (rel gap>1e-6): 1
74 native pts 1776  nodes absent from union (rel gap>1e-6): 1
76 native pts 2920  nodes absent from union (rel gap>1e-6): 1
0.1-1 MeV: 172 nodes, frac in 3-7 b = 1.0000, median 5.0793 b
per-isotope 4A/(1+A)^2: {70: 0.0555, 72: 0.054, 73: 0.0533, 74: 0.0526, 76: 0.0513}
abundance-weighted = 0.053564
N_Ge=4.4136e+22 Sigma=0.1646 lambda=6.0760 P_int(2mm)=3.238%
```

**PASS.** This is the decisive resonance-clipping check and it is stronger than the one the executor reported: **every NJOY native node of all five isotopes is present in the committed union grid**, with the single exception of the lowest point at 1e−5 eV (the union floor is 1.03125e−5 eV) — irrelevant at 10 µeV. The union grid genuinely cannot clip resonances, by set containment.

Endpoints: 0.0555 / 0.0540 / 0.0533 / 0.0526 / 0.0513 reproduce exactly, and the abundance-weighted natural value is **0.053564 → 0.0536**, confirming the executor did **not** force-fit to the 0.0538 label. The mass-ratio (AWR) form gives 0.05406 → 0.0541, also as recorded. The ROADMAP/REQUIREMENTS label 0.0538 matches *neither* form and is a stale number (see Discrepancies).

Σ = 0.1646 cm⁻¹, λ = 6.076 cm, P_int(2 mm) = 3.238% all reproduce to the digits quoted. P_int sits inside the 3–4% band the downstream single-scatter approximation relies on; λ = 6.08 cm is 1.3% above the literal "5–6 cm" of ROADMAP criterion 4 purely because σ_tot is data-derived (3.729 b) instead of the plan's rounded 4 b. The thin-target conclusion (λ ≫ 0.2 cm) is unaffected.

### Check 6 — The mesh-convergence test is measuring the wrong thing

```python
import endf, numpy as np, pandas as pd, sys
sys.path.insert(0,'src')
from nuclear.parse_endf_nGe import loglog_interp
nat = pd.read_csv('data/endf_nGe_elastic_v1.1.csv', comment='#', float_precision='round_trip')
U, lo, hi = nat.E_eV.values, 1e2, 1e6
for A in [70,72,73,74,76]:
    f = endf.IncidentNeutron.from_ace(f'data/endf/ace/320{A}.800nc').reactions[2].xs['294K']
    mn = (f.x>=lo)&(f.x<=hi); ref = np.trapz(f.y[mn], f.x[mn])
    mu = (U>=lo)&(U<=hi)
    ll  = np.trapz(loglog_interp(U, f.x, f.y)[mu], U[mu])
    lin = np.trapz(np.interp(U, f.x, f.y)[mu], U[mu])
    print('%dGe loglog-vs-native %.4f%%   linlin-vs-native %.6f%%'
          % (A, 100*abs(ll-ref)/ref, 100*abs(lin-ref)/ref))
s = nat.sigma_el_natural_b.values; m = (U>=lo)&(U<=hi)
full = np.trapz(s[m], U[m]); dec = np.trapz(s[m][::2], U[m][::2])
print('decimation dev = %.3f%%' % (100*abs(dec-full)/full))
```

**Output:**

```output
70Ge loglog-vs-native 0.0458%   linlin-vs-native 0.000000%
72Ge loglog-vs-native 0.0581%   linlin-vs-native 0.000000%
73Ge loglog-vs-native 0.1117%   linlin-vs-native 0.000000%
74Ge loglog-vs-native 0.0562%   linlin-vs-native 0.000000%
76Ge loglog-vs-native 0.0793%   linlin-vs-native 0.000000%
decimation dev = 1.817%
```

**FAIL (as an evidence claim); the physical conclusion nonetheless holds.** Both reported numbers reproduce exactly. But the linlin column is the diagnosis: because the union grid is a *superset* of the native grid, adding nodes to a lin-lin-interpolated function changes the trapezoid integral by **identically zero**. The reported 0.0458–0.1117% therefore measures the log-log-vs-lin-lin interpolation-scheme mismatch and nothing else — it cannot detect resonance clipping (the executor's stated purpose), and it cannot measure mesh convergence.

The literal decimation test (1.817%) *is* the honest reading of the plan's "halve the internal mesh, <0.5%" and it **fails**. The executor's argument that decimating an NJOY-linearised grid necessarily degrades it is *correct in principle* — but it does not make the substituted metric a convergence measure. The correct statement is: the union grid provably clips nothing (Check 5, by set containment), and a Richardson estimate from the 1.817% halving ratio puts the union-grid quadrature error over 0.1 keV–1 MeV at roughly 0.6%. That is small, but it is not "<0.5% verified", and the artifact header and SUMMARY report it as a passed convergence criterion.

### Check 7 — Interpolation-law mismatch (previously unflagged)

```python
import endf, numpy as np, pandas as pd
nat = pd.read_csv('data/endf_nGe_elastic_v1.1.csv', comment='#', float_precision='round_trip')
U, s = nat.E_eV.values, nat.sigma_el_natural_b.values
ab = {70:0.2057,72:0.2745,73:0.0775,74:0.3650,76:0.0773}
lin = sum(ab[A]*np.interp(U, *(lambda f:(f.x,f.y))(
    endf.IncidentNeutron.from_ace(f'data/endf/ace/320{A}.800nc').reactions[2].xs['294K'])) for A in ab)
rel = np.abs(s-lin)/np.maximum(lin, 1e-12)
for name,(a,b) in {'0.1keV-1MeV':(1e2,1e6), '1-20MeV':(1e6,2e7)}.items():
    m = (U>=a)&(U<=b)
    print('%-12s max pointwise dev %.3f%%  mean %.4f%%' % (name, 100*rel[m].max(), 100*rel[m].mean()))
i = np.argmax(rel); print('worst at E=%.4e eV: committed %.4f b vs lin-lin %.4f b' % (U[i], s[i], lin[i]))
```

**Output:**

```output
0.1keV-1MeV  max pointwise dev 3.998%  mean 0.0224%
1-20MeV      max pointwise dev 0.468%  mean 0.0417%
worst at E=3.0000e+04 eV: committed 9.8824 b vs lin-lin 10.2939 b
```

**WARNING.** ACE/NJOY pointwise data is linearised specifically so that **lin-lin** interpolation is accurate to the 1e−3 tolerance; the parser uses `loglog_interp`. At union nodes inserted between native nodes the committed σ_el therefore departs from the ENDF-defined interpolant by up to **4.0%** in the resonance band (mean 0.02%, band integrals ≤0.11%). Harmless for band integrals; potentially relevant for a Phase-9 pointwise σ(E)·φ(E) fold. Not disclosed in any artifact.

### Check 8 — Independent literature anchors

- **Gordon 2004.** Web literature check confirms the 10 MeV–10 GeV integral at sea-level NYC is 3.5–3.6×10⁻³ cm⁻² s⁻¹, and that EXPACS/PARMA independently gives ~3.3×10⁻³ over the same range. The artifact's un-tuned PARMA native integral of 3.239×10⁻³ is consistent with that, so the k = 1.09610 anchor factor is a genuine ~10% adjustment. **PASS** on the anchor value; the artifact-side reproduction remains inconclusive (Check 1).
- **NIST free-atom scattering.** Committed epithermal plateau (1–10 eV) median = 8.866 b; NIST bound scattering 8.60 b × (72.6/73.6)² = 8.368 b → **+5.95%**, reproducing the SUMMARY's "+6.0%". This is a genuinely ENDF-independent anchor and it holds at the expected few-percent level.
- **MF=3 vs File-2.** I confirmed directly from the committed raw ENDF text that MF=3 MT=2 is zero through each isotope's resolved+URR region (first non-zero at 1.054 MeV for ⁷⁰Ge, 604 keV for ⁷⁴Ge, 570 keV for ⁷⁶Ge, 13.68 keV for ⁷³Ge), so the ACE fill was **necessary**, not a shortcut, and the previous run's NaN region was a correct diagnosis rather than a parse failure.

### Check 9 — Angular distribution is real data, not a stub

Natural-Ge a₁ recomputed from the committed table: 5.5×10⁻⁵ at thermal, 0.0273 at 0.1 MeV, 0.233 at 1 MeV, 0.713 at 5 MeV, 0.851 at 10 MeV (⟨μ_cm⟩ = a₁/3 ≈ 0.28). Isotropic at low energy rising to strong forward peaking in the fast region is exactly the expected behaviour for a heavy nucleus. Per-isotope values at 5 MeV agree across isotopes to 1%. Abundance weighting of both σ_el and a₁ reproduces the natural columns to 7×10⁻⁷ relative.

---

## Plan 07-02 Contract Coverage

| Contract ID | Kind | Verdict | Evidence |
|---|---|---|---|
| `claim-sigma-el` | claim | **passed** | 5/5 isotopes parse, MATs read from headers, σ_el reproduced independently from ACE and cross-checked against raw MF=3; 0.1–1 MeV 100% in 3–7 b, median 5.079 b |
| `claim-natural-ge` | claim | **passed** | Endpoints and Σ/λ/P_int all recomputed exactly; abundance weighting verified to 7e−7 |
| `claim-axis-provenance` | claim | **passed** | Full ENDF + ACE provenance block present; SHA-256 heads verified; keV_nr tag present; zero applied quenching tokens |
| `deliv-per-isotope` | deliverable | **passed** | 23,155 rows × 11 columns, 0 NaN, E axis identical to the natural file |
| `deliv-natural-ge` | deliverable | **passed** | 23,155 rows, 0 NaN, 1.03e−5 eV → 20 MeV, all header validation numbers reproduce |
| `deliv-parser` | deliverable | **passed** | Real parser; uses `endf` (openmc.data reader) + ACE reader, no hand-rolled ENDF logic, honest NaN degradation path. One methodological defect: log-log interpolation (Check 7) |
| `test-sigma-benchmark` | acceptance test | **passed (scope narrowed)** | Holds for 0.1–1 MeV; σ_el falls to ~2 b over 2–10 MeV, correct physics but outside the plan's literal "3–7 b across 0.1–10 MeV" |
| `test-resonance-grid` | acceptance test | **partial** | Literal criterion fails (1.817% > 0.5%); substituted metric is vacuous (Check 6). The underlying guard (no clipping) is independently **proven** by set containment (Check 5) |
| `test-kinematics-endpoint` | acceptance test | **passed** | 0.0555…0.0513 and natural 0.053564 reproduced exactly, not force-fit to 0.0538 |
| `test-mfp` | acceptance test | **passed (marginal)** | 0.1646 / 6.076 cm / 3.238% reproduced; λ 1.3% above the literal "5–6 cm" because σ_tot is data-derived |
| `test-provenance-axis` | acceptance test | **passed** | All required header fields present; SHA-256 heads independently verified |
| `ref-endf` | reference | **completed** | Raw evaluations committed and independently re-parsed here |
| `ref-openmc` | reference | **completed** | `endf` 0.1.12 (the standalone extraction of openmc.data's reader) used; documented substitution |
| `ref-nndc` | reference | **completed with substitution** | NNDC Sigma interactive plot never consulted — honestly declared. Substituted by ACE-vs-File-3 (4e−7) and the ENDF-independent NIST anchor (+6.0%). I consider the substitution adequate and independently confirmed both |
| `ref-conventions-B` | reference | **completed** | Axis guard present in both artifacts and the parser docstring |
| `fp-bespoke-parser` | forbidden proxy | **rejected** | Only custom code is an HTTP-range file object; no ENDF/ACE/zip format logic |
| `fp-hardcode-mat` | forbidden proxy | **rejected** | MATs read from file (3225/3231/3234/3237/3243, confirmed against the raw filenames) |
| `fp-coarse-mesh` | forbidden proxy | **rejected** | Independently proven: no native node is absent from the union grid |
| `fp-early-kernel` | forbidden proxy | **rejected** | No dσ/dT, no a₁ correction applied, no fold anywhere in the phase commits |

**Ledger hygiene note:** `07-02-SUMMARY.md` declares a `deliv-ace` entry that does not exist in `07-02-PLAN.md`'s contract (its deliverables are `deliv-per-isotope`, `deliv-natural-ge`, `deliv-parser`). Invented ledger keys are schema-invalid. Separately, `07-01-SUMMARY.md` uses a list-of-dicts ledger shape with `outcome:` and `must_surface_refs:` rather than the canonical mapping schema. Neither affects the physics.

---

## Assessment of the Known Open Items

1. **Gordon → PARMA reference-model change.** Honestly and thoroughly recorded — in the CSV header, in the assumptions note (with the USER DECISION provenance), and in the SUMMARY. The substitution is *scientifically sound*: the shape source is now open-access and reproducible in principle, and Gordon is retained only in the role its published integral actually supports. The un-tuned agreement (3.239e−3 vs 3.5–3.6e−3) is an honest independent cross-check, and I confirmed the literature side of it. **Does not threaten the phase goal.** The residual weakness is reproducibility, not provenance.

2. **293.6 K ACE vs mK target.** Correctly flagged. I independently reproduced both peak values (8533.0 b at 293.6 K, 9253.7 b at 0.1 K) and the mechanism statement is right: Doppler broadening is a normalised convolution, so it conserves the resonance integral while reshaping peaks — the ~0 integral shift is the *expected* result and the artifact says so explicitly rather than presenting it as a null cross-check. The 0.1 K set is on disk and the caveat names the exact downstream condition (line-shape-resolving use). **Handled well; does not threaten the phase goal.**

3. **The "halve the mesh" wording.** The executor's reasoning is **half right and reported honestly, but the substitution does not survive scrutiny.** Correct: decimating an NJOY-linearised grid must degrade it, so 1.817% is not evidence of an under-resolved mesh. Incorrect: the substituted union-vs-native metric is identically zero under the ENDF-defined lin-lin interpolation, so it tests neither convergence nor clipping — it is a pure interpolation-scheme diagnostic that happens to be small. Reporting both numbers was the right instinct; labelling the substitute a passed convergence criterion was not. The physical guard survives because set containment proves it (Check 5). **Redefined test; conclusion still true.**

4. **197 MeV grid ceiling.** Disclosed clearly and quantified correctly (I measured 20.57% vs the stated ~21%), with the anchor explicitly defined on the full range. The disclosure is exemplary. **Does not threaten the phase goal** for Input 1 — but see the *new* cross-artifact issue below, which is more consequential and is not disclosed anywhere.

---

## Discrepancies Found

| # | Issue | Severity | Detail |
|---|---|---|---|
| D1 | Elastic table ends at 20 MeV; flux table runs to 197 MeV | **significant** | 26.9% of the on-grid ambient flux (86.4% of the on-grid >10 MeV flux) has no σ_el. Phase 9 (CALC-06) will silently truncate or silently extrapolate unless this is decided explicitly. Not mentioned in any Phase-7 artifact. This is the one finding that bears directly on the goal's "axis-consistent inputs for every downstream fold". |
| D2 | Ambient-flux anchor not reproducible in-repo | **significant** | No PARMA driver committed; the decisive 3.55e−3 and 1.317e−2 integrals cannot be recomputed. Contrast 07-02, which committed both a fetcher and a parser. |
| D3 | `test-resonance-grid` reported as passed on a vacuous metric | **significant** | Literal criterion fails at 1.817%; substitute is identically 0 under lin-lin. Conclusion (no clipping) is nevertheless true and independently proven here. |
| D4 | Log-log interpolation of lin-lin ENDF data | minor–significant | Up to 4.0% pointwise σ_el deviation in the resonance band; ≤0.11% on band integrals. Undisclosed. |
| D5 | `T_max/E_n = 0.0538` stale in REQUIREMENTS/ROADMAP | minor | Computed values are 0.0536 (mass-number form, as the requirement's own formula defines) and 0.0541 (mass-ratio form). 0.0538 matches neither. Phase 9's VALD-05 would test against a stale label. |
| D6 | nat-K 31.03 Bq/g claimed "<1%" | minor | Requires the superseded T½(40K)=1.277e9 yr; current 1.248e9 yr gives 31.72 Bq/g (+2.3%). |
| D7 | `test-sigma-benchmark` verdict recorded as `pass` against a "3–7 b across 0.1–10 MeV" threshold | minor | The prose is scrupulously honest that the band is a 0.1–1 MeV statement; the machine-readable verdict's `threshold` field is not. Ledger-honesty only — the physics (σ_el → ~2 b as inelastic/(n,2n) open) is correct and I confirmed it from the raw evaluations. |
| D8 | λ = 6.076 cm vs criterion "λ ~ 5–6 cm" | minor | Data-derived σ_tot = 3.729 b rather than the assumed 4 b. Honest and documented; thin-target conclusion unaffected. |
| D9 | `deliv-ace` is not a declared contract ID; 07-01-SUMMARY ledger shape non-canonical | minor | Schema hygiene only. |
| D10 | No regression tests for `src/nuclear/` | minor | Every v1.0 module has a `tests/test_*.py`; the two new Phase-7 modules have none. |
| D11 | "byte-identical" grid claim needs round-trip float parsing to reproduce | informational | Default pandas parsing shows 9e−15 ULP drift on 215/585 edges. Artifact is correct; the verification recipe needs the caveat. |
| D12 | `ASSERT_CONVENTION` headers in `src/nuclear/` omit `natural_units` | informational | They use domain keys (`units_sigma`, `recoil_axis`, `no_quenching`) consistent with `src/flux/` style but omit the canonical key every other module carries. |

**Root-cause grouping.** D1 + D2 share a root cause: the two frozen tables were validated *individually* against their own headers, never *jointly* against each other or against a committed re-execution path. D3 + D4 share a root cause: the interpolation law was chosen (log-log) without reference to the ENDF-declared interpolation scheme, which both introduced the 4% pointwise deviation and made the convergence metric non-zero and therefore superficially meaningful.

---

## Reproducibility Assessment

- **ACE binaries (gitignored, 58 MB).** Genuinely reproducible **in principle**: `src/nuclear/fetch_ace_lib80x.py` targets a stable public URL, verifies `Accept-Ranges`, uses only the stdlib `zipfile` over a range-backed file object, and records per-file SHA-256. I verified all five recorded 16-hex prefixes against the local files — they match. Caveats: only a 64-bit hash prefix is recorded (adequate against corruption, weak as a cryptographic pin), and reproducibility depends on LANL keeping `Lib80x.zip` byte-stable at that URL with range support.
- **Headers record everything required:** ACE library + LA-UR citation, retrieval URL and date, per-isotope ZAIDs, SHA-256 heads, NJOY 2016.68, temperature 293.6 K, ACE reader and version, plus the independent IAEA-NDS ENDF retrieval. **PASS.**
- **Residual gap:** the sub-MeV σ_el cannot be regenerated from committed files alone (MF=3 MT=2 is zero there), so a network-isolated clone depends on the frozen CSV as the artifact of record. Acceptable and documented.
- **Ambient flux:** no builder committed. **This is the weakest reproducibility link in the phase.**

---

## Requirements Coverage

Phase 7 has no standalone requirement; it **gates** CALC-05/06/07/08/09 and pre-checks VALD-05/06.

| Gated item | Ready? | Note |
|---|---|---|
| CALC-05 (φ(E_n) assembly) | Yes | Ambient source term locked, grid-compatible, band present |
| CALC-06 (recoil fold) | **Conditionally** | σ_el locked and validated, **but** D1 (20 MeV ceiling) and D5 (0.0538 label) must be resolved first |
| CALC-07 (γ ER budget) | Yes | γ channel column and per-component defaults present |
| CALC-08 ((α,n)+SF NR) | Yes | SF yield and low-Z flags present; awaits the CALC-06 kernel |
| CALC-09 (activation inventory) | Yes | As-deployed activities verified; exposure band documented |
| VALD-05 pre-check | Yes, with D5 | 0.0536/0.0541 computed; requirement text says 0.0538 |
| VALD-06 pre-check | Yes | P_int = 3.24% inside the 3–4% band |

---

## Anti-Patterns Scanned

- Placeholder / stub / hardcoded returns: **none found.** σ_el, a₁, activities and conversions are all real computed data; the parser degrades to an explicit NaN flag rather than fabricating a fill.
- Magic numbers: MATs, ZAIDs, AWRs read from files; abundances, half-lives and production rates are cited constants, not invented.
- Suppressed warnings / silent fallbacks: the parser's fallback chain (ACE → local NJOY → MF3-only-NaN) is explicit and documented.
- Unjustified approximations: the σ_tot band-mean and the scalar shielding band are both declared as approximations in the artifacts.
- Division-by-zero / float-equality hazards: `loglog_interp` guards non-positive values; no float equality used for physics decisions.
- Circular reasoning: **one near-miss** — the union-vs-native "convergence" test (D3) is circular in the sense that it cannot fail for the property it claims to test.
- Fabricated references: none. Every citation I spot-checked (Gordon integral, CDMSlite/EDELWEISS rates, MAJORANA electroformed-Cu, Mei–Zhang–Hime SF yield, NIST scattering length, Sato 2015 DOI) is real and correctly attributed. The one paywalled source was explicitly *not* reconstructed from memory — the correct behaviour.

---

## Expert Verification Required

1. **Indoor spectral-shape systematic** (cosmic-ray/atmospheric neutron transport). The factor-of-5 scalar building attenuation cannot represent roof/wall moderation, which reshapes the evaporation hump into thermal. A computational check cannot settle whether the scalar band is conservative for the *in-band* recoil rate; a transport specialist should judge whether the Phase-8/12 sensitivity deferral is adequate.
2. **Choice of representative housing assay** (low-background materials). The commercial-OFHC-Cu + FR4/connector middle is a discretionary pick inside a >2-order bracket. Its defensibility for a QPD device is a materials-engineering judgement, not a computation.
3. **20 MeV → 197 MeV cross-section extension** (nuclear data / high-energy transport). If Phase 9 must cover the 27% of flux above 20 MeV, the choice between truncation-with-quoted-omission, a high-energy library (e.g. an intranuclear-cascade evaluation), or an optical-model extrapolation is a nuclear-data judgement.
4. **Cryogenic resonance line shapes.** Whether the mK target requires the 0.1 K set depends on the eventual downstream estimator; the artifact defers this correctly but a decision is needed before any resonance-resolving fold.

---

## Confidence Assessment

**Overall: HIGH** for what was checked; the limiting factor is coverage, not agreement.

| Item | Status |
|---|---|
| Independently recomputed and reproduced | Activation A(t) (9 values), U/Th/SF conversions, per-component ppb round-trips, all endpoint fractions, Σ/λ/P_int, on-grid flux integrals, grid byte-identity, band structure, abundance weighting, union-grid completeness, σ_el spot values from ACE, σ_tot, Doppler peaks at both temperatures, resonance peak, epithermal plateau, ACE SHA-256, mesh metrics (both), a₁ energy dependence |
| Independently confirmed against external literature | Gordon 10 MeV–10 GeV integral, PARMA/EXPACS native normalization, NIST free-atom scattering anchor, MF=3-zero-in-RRR behaviour |
| Structurally present but not independently confirmed | Full-range PARMA integrals (off-grid, no driver), MAJORANA/CDMSlite/EDELWEISS source papers not re-read (values match well-known published figures) |
| Unable to verify | Whether `Lib80x.zip` remains byte-stable upstream; whether the PARMA build used the stated evaluation conditions |

Count: **19/22** bound contract targets verified; **19/19** distinct physics checks executed, of which **17** were independently reproduced and **2** (full-range flux integrals) could not be. All 19 Plan 07-02 contract targets assessed, 17 passed, 1 partial, 1 passed-with-narrowed-scope.

---

## Validation Note

`gpd` is not on `PATH` in this worktree; validation was run through the runtime CLI at `/Users/lanqingyuan/.gpd/venv/bin/python -m gpd.runtime_cli`. Results are recorded with the return envelope.

---

## Gaps Summary

The phase goal — three gating inputs fixed as cited defaults with explicit bands, plus acquired and validated ENDF n-Ge elastic data — **is achieved**. No committed number was found to be wrong. Every gap is about evidence quality or cross-artifact consistency:

- **Blocking Phase 9 specifically:** D1 (20 MeV vs 197 MeV) and D5 (stale 0.0538 label).
- **Weakening the record:** D2 (no committed flux reproduction path), D3 (vacuous convergence evidence), D4 (undisclosed interpolation-law mismatch).
- **Hygiene:** D6–D12.

Recommended next action: close D1 and D5 before Phase 9 begins; fold D2–D4 into a short Phase-7 addendum rather than re-opening the lock.
