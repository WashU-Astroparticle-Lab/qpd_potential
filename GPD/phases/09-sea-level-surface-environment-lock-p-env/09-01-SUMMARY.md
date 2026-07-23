---
phase: 09-sea-level-surface-environment-lock-p-env
plan: 01
plan_contract_ref: GPD/phases/09-sea-level-surface-environment-lock-p-env/09-01-PLAN.md#/contract
title: "v1.0 muon and environmental-gamma inputs re-declared numerically identical, verified by direct comparison against the frozen artifacts"
date: 2026-07-22
status: complete
depth: full
completed: 2026-07-22
tasks_completed: 3
tasks_total: 3
one_liner: "Re-declared the two v1.0 particle-background channels as the muon and gamma inputs of the unshielded sea-level surface environment and PROVED identity rather than asserting it: integral_muon_rate_Hz = 1.3659 +/- 0.0003 and the first tabulated E_dep = 1.014497e-02 keV parsed out of data/muon_dRdEdep.csv, total_single_scatter_rate_Hz = 2.6747e-01 (BOUND incoherent) parsed out of data/compton_dRdEdep.csv and kept distinct from the free-KN 2.6846e-01, the VALD-03 anchor 2.7305e-01 and the paper's rounded 0.267; the three deterministic muon scalars re-derived from the COMMITTED modules as <ell> = 0.384848 cm (-0.039%), xi = 0.072069 MeV (-0.043%) and Delta_p = 1.230614 MeV (-0.137%) with Delta_p < mean 1.458502 MeV strictly and kappa = 6.73e-5; the three Compton edges recomputed in closed form from data/gamma_lines.csv as 1243.3573 / 1541.3115 / 2381.7571 keV, all within 0.05 keV, with ZERO non-zero content in any bin whose lower edge exceeds the highest edge and exactly 0.0 at the 2614.511 keV line; a recorded correction that 1.014497e-02 keV is the first log-bin CENTRE of the v1.0 shared grid rather than its first EDGE (1.0e-2 keV exactly), with the whole E_dep column reproducing sqrt(edges[:-1]*edges[1:]) to rtol 1e-6; a shielded-token scan over both channels' full import closure returning ONE hit, allow-listed with justification as the NIST XCOM photon mass-attenuation coefficient of the germanium TARGET; and a directional-bias record putting the muon rate 20.61% BELOW the PDG 'one muon per cm^2 per minute' anchor (1.7204 Hz) -> flatters_SB, with the honest disclosure that the PDG I_v = 70 m^-2 s^-1 sr^-1 cos^2 leg gives 1.1350 Hz i.e. +20.34%, so the anchor's own two legs BRACKET the adopted value, while the gamma normalization sits AT its LABChico anchor -> neutral with the factor-2 band carried unnarrowed."
provides:
  - "GPD/phases/09-sea-level-surface-environment-lock-p-env/09-01-MUON-GAMMA-DECLARATION.md -- provenance-headed two-channel re-declaration: nine artifact SHA-256 values at the pinned revision, every committed scalar next to its extraction command, closed-form re-derivation of the deterministic scalars, the zero-overburden scenario statement, the executed no-renormalization scan with its allow-list justification, and the per-channel signed directional-bias rows"
  - "tests/test_env_v1_identity.py -- 13 executable identity tests, plus the module-level shielded-token machinery (SHIELDED_TOKENS, SHIELDED_TOKENS_EXTRA, SHIELDED_ALLOWLIST, SHIELDED_FILE_ALLOWLIST, NOT_APPLIED_MARKERS, normalize_unicode, scan_text, scan_paths, import_closure_files) that Plans 09-02 and 09-03 import rather than re-type"
contract_results:
  claims:
    claim-muon-identical:
      status: passed
      summary: "The unshielded-surface muon input is the v1.0 Gaisser-Guan (x) ray-box chord (x) Landau-Vavilov MPV chain re-declared numerically identical, and identity was DEMONSTRATED, not asserted. integral_muon_rate_Hz = 1.3659 +/- 0.0003 and the first tabulated E_dep = 1.014497e-02 keV were parsed out of data/muon_dRdEdep.csv by recorded grep/sed commands. The three deterministic scalars were recomputed by CALLING the committed modules -- <ell> = 4V/S = 0.384848 cm (-0.039% vs the paper's 0.385), xi(vertical) = 0.072069 MeV (-0.043% vs 0.0721), Delta_p = 1.230614 MeV (-0.137% vs 1.2323) -- all inside their stated tolerances, with the Landau right-skew ordering Delta_p < <Delta> = 1.458502 MeV holding STRICTLY and kappa = xi/T_max = 6.73e-5 confirming the deep-Landau regime. Neither Monte Carlo was re-run and no data/ file was written. A wording correction is recorded rather than glossed: the committed 1.014497e-02 keV is the first log-bin CENTRE of the v1.0 shared grid, whose first EDGE is exactly 1.0e-2 keV; the whole 584-row E_dep column reproduces sqrt(edges[:-1]*edges[1:]) to rtol 1e-6, so the frozen table is on-grid and only the plan's word 'edge' was imprecise. Zero overburden, zero attenuation: the VNS 2.92 m w.e. and its factor 1.41 are NOT applied and not applicable."
      linked_ids: [deliv-mu-gamma-declaration, deliv-identity-tests, test-muon-identity, test-muon-scalars, test-no-renormalization, ref-muon-artifact, ref-paper-backgrounds, ref-pdg-muon]
    claim-gamma-identical:
      status: passed
      summary: "The unshielded-surface gamma input is the v1.0 Klein-Nishina (x) Hubbell bound-incoherent treatment re-declared numerically identical. total_single_scatter_rate_Hz = 2.6747e-01 was parsed from the committed header and is explicitly separated from the three other circulating values: the free-KN pre-binding 2.6846e-01, the VALD-03 independent anchor Phi*sigma_KN*N_e = 2.7305e-01 (ratio 0.980), and the paper's rounded 0.267, with f_bind = 0.9963. The three Compton edges were reproduced in CLOSED FORM from data/gamma_lines.csv independently of the sampler: 40K 1243.3573 keV (-0.043 vs committed), 214Bi 1541.3115 keV (+0.012), 208Tl 2381.7571 keV (-0.043) -- all inside 0.5 keV, and the module's own compton_edge_kev() agrees with the independent formula to rtol 1e-12. The thin-target single-scatter approximation was checked IN THE ARTIFACT and not just in the prose: over the full 16-line list the highest edge is 2381.7571 keV, and the number of non-zero bins whose LOWER edge exceeds it is 0. Exactly one non-zero bin has a centre above the edge (bin 430, edges [2375.5183, 2444.8947] keV) and the edge falls INSIDE that bin with 10.8% of the preceding bin's content -- a binning effect, quantified rather than waved through -- while the bin containing the full 2614.511 keV line energy carries exactly 0.0, so there is no photopeak. The factor-2 site band is carried forward UNNARROWED with the confidence split intact (edge positions HIGH, absolute normalization MEDIUM)."
      linked_ids: [deliv-mu-gamma-declaration, deliv-identity-tests, test-gamma-identity, test-compton-edges, test-no-renormalization, ref-gamma-artifact, ref-paper-backgrounds, ref-labchico]
    claim-accuracy-direction:
      status: passed
      summary: "Both channels carry their claimed accuracy together with the SIGNED direction it errs. Muon: the anchor rate was computed here rather than quoted -- PDG Leg A (the paper's own: ~1 muon cm^-2 min^-1 through a horizontal detector) x A_top 103.2256 cm^2 = 1.7204 Hz, so the adopted 1.3659 Hz sits at -20.61%, labelled flatters_SB because less background raises S/B. Gamma: the committed normalization IS the measured LABChico anchor, i.e. the CENTRE of its factor-2 band and not either edge, so the row is +0.00% and labelled neutral, with the low edge (x0.5 -> 0.1337 Hz) identified as the flattering one and explicitly not used. A disclosure that strengthens rather than weakens the audit is recorded: the two PDG statements ref-pdg-muon quotes are not mutually consistent at the +/-20% level and BRACKET the adopted value -- Leg B (I_v ~ 70 m^-2 s^-1 sr^-1 with I ~ cos^2 theta, J = pi I_v/2) gives 1.1350 Hz, i.e. +20.34%, which would be penalizes_SB. The flatters_SB label is therefore assigned on the anchor leg the v1.0 paper itself invokes, and the honest magnitude of the muon channel's directional bias is <~20% in EITHER direction, dominated by the 30-35% Gaisser-Guan inter-experiment spread that no in-repo artifact can narrow. Adding the wafer's side-entry faces raises either anchor by only +1.97% under a cos^2-weighted projected-area integral, so side entry does not resolve the discrepancy."
      linked_ids: [deliv-mu-gamma-declaration, test-accuracy-direction, ref-pdg-muon, ref-paper-backgrounds]
  deliverables:
    deliv-mu-gamma-declaration:
      status: passed
      path: GPD/phases/09-sea-level-surface-environment-lock-p-env/09-01-MUON-GAMMA-DECLARATION.md
      summary: "Nine-row artifact table with SHA-256 and byte count for both channels' CSVs and modules, each hash being the git blob at the pinned revision 72011f2 (the definition of the frozen v1.0 artifact). Every committed scalar appears next to the exact command that extracted it. The binding path correction is recorded with its ls output: src/muon/deposited_spectrum.py and data/muon/muon_dep_spectrum.csv DO NOT EXIST, are confirmed absent, and are cited nowhere -- with the consequence spelled out that the Phase-4 summary layer is not a trustworthy provenance source without a filesystem check. A concurrency note records, rather than smooths over, that Phase 10 modified src/qpd_potential/compton_source.py in this same working tree during execution, and shows by re-evaluation that the declared gamma numbers (ell_bar, mu*ell_bar, double-scatter fraction, E_edge) are bit-identical under that edit."
      linked_ids: [claim-muon-identical, claim-gamma-identical, claim-accuracy-direction, test-muon-identity, test-gamma-identity, test-accuracy-direction]
    deliv-identity-tests:
      status: passed
      path: tests/test_env_v1_identity.py
      summary: "13 tests, all green: header scalars, deterministic scalars against the committed modules, on-grid check against the explicitly pinned v1.0 grid, absence of the two non-existent paths, the four-way gamma rate distinction, closed-form Compton edges, the no-photopeak check, the import-closure token scan, the declaration prose scan, the declared-hash check against the pinned revision, a disclosure check for any declared artifact that moved since freeze, and the bias-direction parser. The shielded-token machinery is exported at module level so Plans 09-02 and 09-03 import it instead of re-typing a guard list -- two divergent copies of a guard is how a guard silently stops guarding."
      linked_ids: [claim-muon-identical, claim-gamma-identical, test-no-renormalization]
  acceptance_tests:
    test-muon-identity:
      status: passed
      summary: "integral_muon_rate_Hz parsed to exactly 1.3659 with uncertainty exactly 0.0003; the first tabulated E_dep parsed to exactly 1.014497e-02 keV; git status --porcelain returned empty for all nine declared paths at freeze time; every SHA-256 in the declaration equals the git blob hash at the pinned revision 72011f2."
      linked_ids: [claim-muon-identical, deliv-mu-gamma-declaration, deliv-identity-tests, ref-muon-artifact]
    test-muon-scalars:
      status: passed
      summary: "Recomputed from the committed modules: <ell> = 0.384848 cm vs 0.385 (-0.039%, tol 0.1%); xi = 0.072069 MeV vs 0.0721 (-0.043%, tol 0.5%); Delta_p = 1.230614 MeV vs 1.2323 (-0.137%, tol 0.5%); mean = 1.458502 MeV vs 1.4585 (+0.000%). Delta_p < mean holds strictly, so the MPV has not been silently replaced by the mean or by a Moyal approximation. kappa = 6.73e-5 < 0.07."
      linked_ids: [claim-muon-identical, deliv-identity-tests, ref-muon-artifact, ref-paper-backgrounds]
    test-gamma-identity:
      status: passed
      summary: "total_single_scatter_rate_Hz parsed to exactly 2.6747e-01 with 'BOUND incoherent' present in the same header line; all four circulating numbers named with their meanings in the declaration; all six gamma artifacts unmodified at freeze time with their hashes matching the pinned-revision blobs."
      linked_ids: [claim-gamma-identical, deliv-mu-gamma-declaration, deliv-identity-tests, ref-gamma-artifact]
    test-compton-edges:
      status: passed
      summary: "Closed-form edges 1243.3573 / 1541.3115 / 2381.7571 keV reproduce the committed 1243.4 / 1541.3 / 2381.8 to -0.043 / +0.012 / -0.043 keV, all inside 0.5 keV. Zero non-zero bins with lower edge above the highest edge; exactly 0.0 at the 2614.511 keV line. The single straddling bin is identified, quantified (10.8% of the preceding bin) and explained as binning rather than dismissed."
      linked_ids: [claim-gamma-identical, deliv-identity-tests, ref-gamma-artifact, ref-paper-backgrounds]
    test-no-renormalization:
      status: passed
      summary: "Scan over muon_deposit.py, muon_flux.py, compton_source.py, compton_deposit.py and their resolved import closure (plus wafer_geometry.py, params.py) returned exactly ONE hit: compton_source.py:147, the docstring of the NIST XCOM photon mass-attenuation coefficient of the germanium TARGET. It is allow-listed with a written justification -- it is a property of the wafer, not a shield, and it multiplies no normalization -- as a narrow (file, exact-line-substring, why) entry, so a NEW attenuation-like term would not match and would fail. Zero shielded-configuration hits; no numeric factor other than exactly 1.0 multiplies either channel."
      linked_ids: [claim-muon-identical, deliv-mu-gamma-declaration, deliv-identity-tests]
    test-accuracy-direction:
      status: passed
      summary: "Both rows present and complete with a SIGNED deviation and a direction label from the closed vocabulary. Falsifiability was demonstrated on the live document rather than claimed: dropping the muon sign (-20.61 % -> 20.61 %) FAILS the test, flipping it (-> +20.61 %) FAILS, and restoring PASSES. A Unicode gotcha was caught in the process and fixed -- the table's minus is U+2212, so an ASCII ^[+-] check wrongly reported the sign as dropped; the parser now normalizes U+2212/U+2013/U+2014 and the thin-space family, which is the same class of bug as the Phase-8 U+2009 finding."
      linked_ids: [claim-accuracy-direction, deliv-mu-gamma-declaration, ref-pdg-muon]
  references:
    ref-paper-backgrounds:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "paper/sections/backgrounds.tex read in full and used as the binding statement of what the environment is. Both re-declared physics chains match it clause by clause, including its own '~20%' PDG comparison, its 'weakest anchor' attribution to the 30-35% Gaisser-Guan spread, and its HIGH/MEDIUM confidence split."
    ref-muon-artifact:
      status: completed
      completed_actions: [read, use, compare]
      missing_actions: []
      summary: "data/muon_dRdEdep.csv header parsed for the rate and the MPV/mean pair; the data body read for the grid; both modules imported and CALLED to re-derive the deterministic scalars. Compared, not assumed."
    ref-gamma-artifact:
      status: completed
      completed_actions: [read, use, compare]
      missing_actions: []
      summary: "All four gamma CSVs and both modules hashed and compared; gamma_lines.csv read through compton_source.load_gamma_lines() for the independent edge reproduction; compton_dRdEdep.csv scanned bin-by-bin for content above the highest edge."
    ref-pdg-muon:
      status: completed
      completed_actions: [compare, cite]
      missing_actions: []
      summary: "Both PDG statements were turned into wafer rates and compared numerically: Leg A 1.7204 Hz (-20.61%) and Leg B 1.1350 Hz (+20.34%). The comparison surfaced that the anchor's two legs are mutually inconsistent at the +/-20% level and bracket the adopted value; that is recorded in the declaration rather than resolved by picking the convenient leg."
    ref-labchico:
      status: completed
      completed_actions: [compare, cite]
      missing_actions: []
      summary: "The LABChico measured anchor values (40K 1460.8 keV = 0.036 cm^-2 s^-1, 208Tl 2614.5 keV = 0.0016 cm^-2 s^-1) were located in data/gamma_lines.csv's own provenance header and in the loaded line objects, confirming the committed normalization sits AT the measured anchor rather than on a band edge. The factor-2 band is carried unnarrowed."
  forbidden_proxies:
    fp-mc-rerun-drift:
      status: rejected
      notes: "Neither Monte Carlo was executed. git status --porcelain -- data/ stayed clean for the whole plan and no data/ artifact was written."
    fp-wrong-muon-path:
      status: rejected
      notes: "Both non-existent paths confirmed absent by ls and by os.path.exists in the test; they appear in the declaration ONLY inside the Section-0 correction block that records their absence, enforced by a line-position assertion."
    fp-overburden-leak:
      status: rejected
      notes: "Executed token scan over the full import closure: zero shielded hits. The VNS 2.92 m w.e. and factor 1.41 appear only inside an explicit NOT-applied statement."
    fp-flattering-gamma-edge:
      status: rejected
      notes: "The committed normalization is the measured anchor itself, not the low edge. The band is reported as x0.5 ... x2 and is not narrowed; the low edge is named as the flattering one and marked not used."
    fp-rate-conflation:
      status: rejected
      notes: "All four numbers (2.6747e-01 bound, 2.6846e-01 free-KN, 2.7305e-01 VALD-03 anchor, 0.267 rounded) are tabulated with their distinct meanings, and the test asserts all four strings are present in the declaration."
    fp-assertion-not-comparison:
      status: rejected
      notes: "Every quoted number carries its extraction command, and every closed-form scalar was recomputed by calling the committed code. The declaration's own SHA-256 table is parsed by the test and re-checked against git blobs, so the declaration cannot claim a hash it does not have."
  uncertainty_markers:
    weakest_anchors:
      - "The Gaisser-Guan absolute normalization: 30-35% inter-experiment spread that no in-repo artifact can narrow, named as the weakest anchor by the paper itself"
      - "The PDG muon anchor is itself two mutually inconsistent statements that bracket the adopted value at -20.61% / +20.34%, so the flatters_SB label is anchor-leg dependent"
      - "The absolute environmental-gamma flux: MEDIUM confidence, factor-2 site band, with the 238U-chain contribution set by an ASSUMED chain balance rather than a measured line intensity"
      - "04-01-SUMMARY.md front-matter names two artifact paths that do not exist, so the summary layer cannot be trusted as a provenance source without a filesystem check"
    unvalidated_assumptions:
      - "That the deployment site's radiogenic ambience resembles LABChico's to within the stated factor 2"
      - "That the wafer is genuinely outdoors at zero overburden rather than inside a building -- a configuration question, not an uncertainty band"
      - "That a cos^2-theta angular distribution is the right way to convert the PDG vertical intensity into a wafer rate; it is what produces the +20.34% Leg B figure"
    competing_explanations:
      - "The sub-0.2% residuals on xi and Delta_p could be header rounding (benign) or a code/artifact disagreement (adverse). Distinguished in favour of the benign reading by EXECUTING the code path, not by assuming it: every scalar reproduces inside its stated tolerance and the strict Delta_p < mean ordering survives."
      - "The single non-zero bin above the highest Compton edge could be a photopeak (adverse) or the bin that straddles the edge (benign). Distinguished by checking bin EDGES rather than centres: zero non-zero bins lie entirely above the edge."
    disconfirming_observations:
      - "A recomputed Compton edge missing its committed value by more than 0.5 keV, or any deposit at 2614.5 keV -- neither occurred"
      - "Delta_p >= mean for the vertical chord, which would show the MPV had been replaced -- did not occur"
      - "Any multiplicative factor other than exactly 1.0 acting on either channel -- none found"
      - "STILL OPEN: no site measurement of the radiogenic ambience exists, so the factor-2 gamma band cannot be narrowed or confirmed by anything in this repository"
comparison_verdicts:
  - subject_id: claim-muon-identical
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-muon-artifact
    comparison_kind: benchmark
    metric: committed_scalar_and_recomputed_scalar_agreement
    threshold: "rate and grid floor exact; <ell> within 0.1%; xi and Delta_p within 0.5%; Delta_p < mean strictly"
    verdict: pass
    recommended_action: "Carry the recorded grid-floor correction forward: 1.014497e-02 keV is the first log-bin CENTRE of the v1.0 grid, whose first EDGE is 1.0e-2 keV. Downstream grid checks must pin version='v1.0'."
    notes: "integral_muon_rate_Hz parsed to exactly 1.3659 +/- 0.0003 and the first tabulated E_dep to exactly 1.014497e-02 keV. Recomputed from the committed modules: <ell> 0.384848 cm (-0.039%), xi 0.072069 MeV (-0.043%), Delta_p 1.230614 MeV (-0.137%), mean 1.458502 MeV (+0.000%), kappa 6.73e-5. Delta_p < mean holds strictly. All nine declared artifact hashes equal the git blobs at the pinned revision 72011f2."
  - subject_id: claim-gamma-identical
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-gamma-artifact
    comparison_kind: benchmark
    metric: compton_edge_position_and_committed_rate_agreement
    threshold: "rate exact; each edge within 0.5 keV; zero non-zero bins with lower edge above the highest edge"
    verdict: pass
    recommended_action: "Keep the four circulating Compton rates distinct downstream; the rate of record is the BOUND 2.6747e-01 Hz."
    notes: "total_single_scatter_rate_Hz parsed to exactly 2.6747e-01 with 'BOUND incoherent' in the same header line. Closed-form edges 1243.3573 / 1541.3115 / 2381.7571 keV vs committed 1243.4 / 1541.3 / 2381.8 -> -0.043 / +0.012 / -0.043 keV. Zero non-zero bins entirely above the highest edge; exactly 0.0 at the 2614.511 keV line. The single straddling bin (edges 2375.5183-2444.8947 keV) carries 10.8% of the preceding bin, consistent with a sharp edge cutting into a log bin."
  - subject_id: claim-accuracy-direction
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-pdg-muon
    comparison_kind: benchmark
    metric: signed_fractional_deviation_from_pdg_sea_level_anchor
    threshold: "|deviation| < 30% (VALD-02 tolerance), sign carried"
    verdict: pass
    recommended_action: "Treat the muon channel's flatters_SB label as anchor-leg dependent. Any downstream S/B statement that leans on it must cite Leg A explicitly, and the 30-35% Gaisser-Guan spread remains the honest width."
    notes: "PDG Leg A (~1 muon cm^-2 min^-1 x A_top 103.2256 cm^2) = 1.7204 Hz -> adopted 1.3659 Hz is -20.61%, flatters_SB. PDG Leg B (I_v = 70 m^-2 s^-1 sr^-1 with cos^2, J = pi I_v/2) = 1.1350 Hz -> +20.34%, penalizes_SB. The anchor's two legs are mutually inconsistent at the +/-20% level and BRACKET the adopted value; side-entry faces move either anchor by only +1.97%. Both legs are recorded rather than the convenient one selected."
  - subject_id: claim-gamma-identical
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-labchico
    comparison_kind: benchmark
    metric: adopted_normalization_position_within_the_factor_2_site_band
    threshold: "adopted value must sit at the measured anchor, not on a band edge; band not narrowed"
    verdict: pass
    recommended_action: "Carry the factor-2 band forward unnarrowed into Phases 13-16; no site measurement exists that could narrow it."
    notes: "The committed per-line fluxes are the LABChico measured anchor values (40K 1460.8 keV = 0.036 cm^-2 s^-1, 208Tl 2614.5 keV = 0.0016 cm^-2 s^-1) as recorded in data/gamma_lines.csv's own provenance header, so the adopted normalization is the CENTRE of the factor-2 band, giving a +0.00% signed deviation and a neutral direction. The low edge (x0.5) is identified as the flattering one and is not used. The 238U-chain contribution rests on an assumed chain balance (flux_unc_frac = 1.0), which is why the band is MEDIUM confidence and stays a factor 2."
---

# Plan 09-01 Summary

**One-liner:** see frontmatter.

## What was done

Three tasks, all complete. The muon and gamma sections of
`09-01-MUON-GAMMA-DECLARATION.md` were written with parsed-not-typed scalars, the deterministic
scalars were re-derived by calling the committed modules, the Compton edges were reproduced in
closed form, and `tests/test_env_v1_identity.py` was written so that every prose claim is
re-checkable by running the suite.

## Key results

| Quantity | Recomputed / parsed | Committed | Signed deviation | Verdict |
|---|---|---|---|---|
| `integral_muon_rate_Hz` | 1.3659 ± 0.0003 | 1.3659 ± 0.0003 | exact | PASS |
| first tabulated `E_dep` | 1.014497e-02 keV | 1.014497e-02 keV | exact | PASS |
| ⟨ℓ⟩ = 4V/S | 0.384848 cm | 0.385 cm | −0.039 % | PASS (tol 0.1 %) |
| ξ (vertical) | 0.072069 MeV | 0.0721 MeV | −0.043 % | PASS (tol 0.5 %) |
| Δ_p (vertical) | 1.230614 MeV | 1.2323 MeV | −0.137 % | PASS (tol 0.5 %) |
| ⟨Δ⟩ | 1.458502 MeV | 1.4585 MeV | +0.000 % | PASS |
| Δ_p < ⟨Δ⟩ | 1.230614 < 1.458502 | strict | — | PASS |
| `total_single_scatter_rate_Hz` | 2.6747e-01 | 2.6747e-01 | exact | PASS |
| E_edge ⁴⁰K / ²¹⁴Bi / ²⁰⁸Tl | 1243.3573 / 1541.3115 / 2381.7571 keV | 1243.4 / 1541.3 / 2381.8 | −0.043 / +0.012 / −0.043 keV | PASS (tol 0.5 keV) |

**[CONFIDENCE: HIGH]** for the identity claims — three genuinely independent check families were
used (file-header parsing, closed-form recomputation from the committed code, and artifact-hash
comparison against git blobs), and the Compton edges were additionally cross-checked against the
module's own kinematics function to rtol 1e-12.

**[CONFIDENCE: MEDIUM]** for the muon directional-bias label. The magnitude (~20 %) is solid, but
the *sign* depends on which PDG statement is taken as the anchor, and the two bracket the adopted
value. This is stated in the declaration and in `uncertainty_markers` rather than resolved by
choosing the convenient leg.

## Deviations

- **[Rule 4 — missing component] Grid-floor wording.** The plan calls `1.014497e-02` keV the
  "first grid edge". It is the first log-bin **centre**; the first edge is exactly `1.0e-2` keV.
  Corrected inline and made executable; the frozen table is on-grid either way.
- **[Rule 4 — missing component] Allow-list for the XCOM attenuation coefficient.** The scan
  returns one legitimate hit (`compton_source.py:147`, the germanium mass-attenuation
  coefficient). Rather than edit a frozen module or weaken the token list, a narrow
  `(file, exact-line, justification)` allow-list entry was added.
- **[Rule 1 — code bug, in this plan's own test] Unicode minus.** The first version of the
  bias-direction parser used an ASCII `^[+-]` check and reported the sign as dropped for a
  U+2212 MINUS SIGN. Fixed with a `normalize_unicode` helper; this is the same class of bug as
  the Phase-8 U+2009 thin-space finding and is now guarded for downstream plans.
- **Concurrency, not a deviation but recorded:** Phase 10 executed in the same working tree and
  modified `src/qpd_potential/compton_source.py` (and later the shared energy grid) during this
  plan. The identity check was re-pointed at the git blob **at the revision the declaration
  itself pins**, and the grid check was re-pointed at `shared_energy_grid(version="v1.0")`. Both
  are the correct semantics for a frozen v1.0 artifact; neither weakens the check.

## Self-Check: PASSED

- `GPD/phases/09-.../09-01-MUON-GAMMA-DECLARATION.md` — FOUND
- `tests/test_env_v1_identity.py` — FOUND, 13 tests, all pass
- Commit `2bb81c7` — FOUND
- `git status --porcelain -- data/` — clean for the whole plan
