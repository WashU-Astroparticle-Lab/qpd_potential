---
phase: 09-sea-level-surface-environment-lock-p-env
plan: 03
plan_contract_ref: GPD/phases/09-sea-level-surface-environment-lock-p-env/09-03-PLAN.md#/contract
title: "The unshielded sea-level surface environment frozen as one three-channel set, with both audits executed and the directional-bias audit returning a mixed, falsifiable result"
date: 2026-07-22
status: complete
depth: full
completed: 2026-07-22
tasks_completed: 3
tasks_total: 3
one_liner: "Assembled the muon, gamma and neutron declarations into ONE frozen provenance-headed environment set -- data/surface_environment_v2.0.csv (20 rows, all three channels, every required column populated, every stored SHA-256 recomputed and matching), docs/v2.0-surface-environment.md and a loader src/qpd_potential/surface_environment.py that returns each quantity ONLY together with its per-channel accuracy label and exposes no combined-band accessor at all -- and then ran both audits rather than asserting them: AUDIT A resolved the loader's import closure to 8 modules and scanned them plus the registry and the declaration, finding 57 raw token hits and ZERO APPLIED, with two exemptions recorded rather than silent (the Plan 09-01 line-level entry for the NIST XCOM mu/rho of the germanium TARGET, and one whole-file entry for veto_credit.py, the Phase-8 taxonomy whose job is to NAME shielded statements in order to fix their credit at 1.0), while every reachable sentinel returned exactly 1.0 -- L2_CREDIT, L1STAR_CREDIT, L1_REJECTION_CREDIT, credit_for() over all 19 catalogued rows, multiplicity_rejection_is_zero() True, and surface_environment.veto_credit() whose docstring states the 1.0 is BY CONSTRUCTION because there is no veto, not a policy default a later phase could relax; AUDIT B returned a MIXED and therefore informative result -- muon -20.61% below its PDG anchor -> flatters_SB, gamma sitting AT its LABChico anchor -> neutral, neutron on the outdoor phi_hi leg and the Gordon midpoint with a site assumption that errs upward -> penalizes_SB, i.e. 1 of 3 channels on the flattering side and NOT all three -- with a numeric COMPOUNDED-EFFECT FACTOR of 1.2171 (replacing the single flattering choice by its anchor would RAISE the declared muon+gamma background by 21.7%), the neutron channel explicitly excluded from that factor because it has no fold yet and reported separately along with the factor-5 phi_lo move that was NOT taken, the honest disclosure that the two PDG legs bracket the muon value so on Leg B the factor would instead be 0.8586, and falsifiability DEMONSTRATED by five mutations (sign dropped, sign flipped, relabelled neutral, factor made qualitative, factor set to a wrong number) each failing test_bias_audit_complete and the restored document passing."
provides:
  - "data/surface_environment_v2.0.csv -- the frozen registry: 20 rows across muon/gamma/neutron with channel, quantity, value, units, artifact_path, artifact_sha256, source_citation, accuracy_label, bias_direction, signed_deviation and notes, above a header block stating unshielded surface / sea level / zero overburden / 3 GW_th at 25 m / veto credit 1.0 by construction, and carrying no combined-band field"
  - "docs/v2.0-surface-environment.md -- the human-readable declaration: per-channel physics chain and provenance, per-channel accuracy WITH direction, the thermal disposition, the executed scan output pasted as evidence, the sentinel results, the three-row directional-bias audit with its numeric compounded-effect factor, the five-mutation falsifiability record, the declared omissions, the weakest anchor unsoftened, and the researcher checkpoint content"
  - "src/qpd_potential/surface_environment.py -- the single loader for Phases 13/14/15: EnvironmentQuantity carries the accuracy label inseparably, accuracy_label() is per-channel only, veto_credit() returns exactly 1.0 with a by-construction docstring, and shielded_token_guard() IMPORTS the Plan 09-01 token list rather than re-typing it"
  - "tests/test_surface_environment.py -- 9 executable tests: registry completeness, artifact hash agreement, per-channel label separation and the absence of any combined-band field or accessor, independent re-derivation of every headline scalar from its frozen artifact, the SC5 token scan over the import closure, the credit sentinels, the bias-audit completeness check including a recomputation of the compounded factor, the falsifiability demonstration, and the declared-omissions check"
contract_results:
  claims:
    claim-single-environment-set:
      status: passed
      summary: "The environment is declared once. data/surface_environment_v2.0.csv holds 20 rows covering all three channels (muon 4, gamma 8, neutron 8) with no empty cell in any required column, every artifact_path resolving on disk and every stored SHA-256 recomputing to match. The registry is not trusted as a transcription: tests/test_surface_environment.py::test_registry_values_rederived_from_artifacts INDEPENDENTLY re-derives every headline scalar from its own frozen artifact -- the muon rate and MC error parsed from data/muon_dRdEdep.csv's header, the grid floor checked against sqrt(edges[0]*edges[1]) of the explicitly pinned v1.0 shared grid, the gamma rate parsed with 'BOUND incoherent' present in the same line, all three Compton edges recomputed in closed form from data/gamma_lines.csv, Phi_th parsed from the sub-eV table header and asserted strictly positive, and k plus all three neutron integrals located in the v1.1 header. src/qpd_potential/surface_environment.py returns each quantity as a frozen EnvironmentQuantity that carries its accuracy label -- there is NO accessor returning a bare float -- and the test scans the entire public API for any name containing 'combined', 'overall' or 'average' as well as scanning the CSV for any combined-band column, so a consumer cannot obtain a single phase-level band."
      linked_ids: [deliv-env-registry, deliv-env-doc, deliv-env-module, deliv-env-tests, test-registry-complete, test-hash-match, test-labels-separate, ref-roadmap-p9, ref-paper-backgrounds]
    claim-no-shielded-quantity:
      status: passed
      summary: "Executed, not asserted. The loader's import closure resolved to 8 modules (surface_environment, veto_credit, muon_deposit, muon_flux, compton_source, compton_deposit's dependencies, wafer_geometry, params, interp_guard) and was scanned together with the registry and the declaration using the Plan 09-01 token list plus the Plan 09-03 additions dru / Table 5 / residual: 29 raw hits in the source closure, 8 in the registry, 20 in the declaration, and ZERO APPLIED in all three. Two exemptions are recorded rather than silent -- the Plan 09-01 line-level entry for the NIST XCOM photon mass-attenuation coefficient of the germanium TARGET, and one WHOLE-FILE entry for src/qpd_potential/veto_credit.py, the Phase-8 NUCLEUS rejection/attenuation taxonomy whose entire purpose is to name every shielded statement in order to fix its transferable credit at exactly 1.0. That exemption is not taken on trust: every credit the module exposes is separately called and asserted. L2_CREDIT = L1STAR_CREDIT = L1_REJECTION_CREDIT = 1.0; credit_for() = 1.0 for ALL 19 catalogued rows; multiplicity_rejection_is_zero() returns True; and surface_environment.veto_credit() returns exactly 1.0 with a docstring the test parses and requires to contain BY CONSTRUCTION and 'no veto' -- so a 1.0 arrived at as a policy default, which a later phase could quietly relax, would FAIL. The registry header carries the same by-construction statement."
      linked_ids: [deliv-env-module, deliv-env-tests, deliv-env-doc, test-no-shield-scan, test-veto-credit-unity, ref-project-contract, ref-gate-verdict]
    claim-directional-audit:
      status: passed
      summary: "The audit was executed honestly and returned a MIXED result, which is what makes it a check rather than a formality. muon: 1.3659 Hz against the PDG Leg A anchor (~1 muon cm^-2 min^-1 x A_top = 1.7204 Hz), signed deviation -20.61%, direction flatters_SB because less background raises S/B. gamma: 2.6747e-1 Hz sits AT the measured LABChico anchor, i.e. the CENTRE of its factor-2 band and not either edge, so +0.00% and neutral, with the low edge (x0.5 -> 0.1337 Hz) named as the flattering one and confirmed unused. neutron: the channel adopts the OUTDOOR phi_hi leg and the Gordon MIDPOINT rather than any low edge, and the NYC evaluation point errs low for a higher-altitude or higher-cutoff site, so the direction is penalizes_SB -- the choice costs S/B rather than buying it. Channels on the flattering side: 1 of 3, NOT all three, so the adverse reading (systematic selection pressure across the input set) is not what the evidence shows, and the benign reading is invoked BECAUSE the audit came out mixed. COMPOUNDED EFFECT, given as a number: replacing the one flattering choice by its anchor takes the declared muon+gamma through-wafer background from 1.63337 Hz to 1.98787 Hz, a factor 1.2171 -- a 21.7% RISE in background and an equal fall in S/B. The neutron channel is explicitly excluded from that factor because at this phase it is an incident flux with no fold and therefore no rate, and is reported separately together with the factor-5 phi_lo move that was NOT taken and the two flatters_SB truncation omissions carried to Phase 13. The audit's own weakest point is disclosed rather than hidden: the two PDG statements bracket the adopted muon value (Leg B gives +20.34%, penalizes_SB, and a compounded factor of 0.8586), so the flatters_SB label rests on the anchor leg the v1.0 paper itself invokes. FALSIFIABILITY was demonstrated on the live document: five mutations -- sign dropped, sign flipped, muon relabelled neutral, the factor made qualitative, the factor replaced by a wrong number 1.5000 -- each FAILED test_bias_audit_complete, and the restored document PASSED. The last of those matters most: the test recomputes (muon_anchor + gamma)/(muon + gamma) from the registry and the parsed deviation and requires agreement to 5e-4, so a plausible-looking but unsupported factor cannot survive."
      linked_ids: [deliv-env-doc, deliv-env-registry, deliv-env-tests, test-bias-audit-complete, test-bias-audit-reviewed, ref-gate-verdict, ref-roadmap-p9]
  deliverables:
    deliv-env-registry:
      status: passed
      path: data/surface_environment_v2.0.csv
      summary: "20 rows, 11 columns, all three channels, no empty required cell, every SHA-256 recomputed and matching. Header block states the unshielded-surface / sea-level / zero-overburden / 3 GW_th at 25 m scenario and veto credit 1.0 by construction, records that the v1.0 paper omitted neutrons entirely and that this set adds them, keeps the three accuracy labels separate with an explicit statement that there is no combined field, and points at the per-channel declarations. Neutron rows all carry accuracy_label = order_of_magnitude; the phi_lo row is present precisely so that it is on the record as NOT USED."
      linked_ids: [claim-single-environment-set, claim-directional-audit, test-registry-complete, test-hash-match, test-labels-separate]
    deliv-env-doc:
      status: passed
      path: docs/v2.0-surface-environment.md
      summary: "Frozen set in one table; per-channel physics chains matching backgrounds.tex for muon and gamma and disclosing that the neutron channel is new; thermal disposition with bounds, cutoff convention and cutoff sensitivity; the SC5 scan output pasted verbatim as evidence with the two exemptions justified; the sentinel results; the three-row bias audit with the numeric compounded-effect factor, the Leg-A/Leg-B disclosure and the separately-reported directional omissions; the five-mutation falsifiability table; the muon-induced-neutron omission stated as an omission rather than as negligible; the weakest anchor stated without softening; and the researcher checkpoint content."
      linked_ids: [claim-single-environment-set, claim-no-shielded-quantity, claim-directional-audit, test-no-shield-scan, test-bias-audit-complete]
    deliv-env-module:
      status: passed
      path: src/qpd_potential/surface_environment.py
      summary: "load(), get(), accuracy_label(), bias_audit(), header_lines(), sha256_of(), veto_credit() and shielded_token_guard(). Every quantity is returned as a frozen EnvironmentQuantity carrying its accuracy label; there is no bare-float accessor and no combined-band accessor. accuracy_label() takes a single channel and raises on anything else. veto_credit() returns exactly 1.0 with a docstring stating the by-construction reasoning. shielded_token_guard() IMPORTS SHIELDED_TOKENS and SHIELDED_TOKENS_EXTRA from tests/test_env_v1_identity.py -- deliberately, because two divergent copies of a guard list is how a guard silently stops guarding -- and the test asserts object identity, not just equality."
      linked_ids: [claim-single-environment-set, claim-no-shielded-quantity, test-labels-separate, test-no-shield-scan, test-veto-credit-unity]
    deliv-env-tests:
      status: passed
      path: tests/test_surface_environment.py
      summary: "9 tests, all green: registry completeness with the scenario header assertions, artifact hash recomputation, per-channel label separation plus the API and CSV sweeps for any combined band, independent re-derivation of every headline scalar from its frozen artifact, the SC5 token scan over the resolved import closure and both documents, the credit sentinels including the by-construction docstring parse, bias-audit completeness with the compounded-factor recomputation to 5e-4, the falsifiability demonstration, and the declared-omissions check."
      linked_ids: [claim-single-environment-set, claim-no-shielded-quantity, claim-directional-audit]
  acceptance_tests:
    test-registry-complete:
      status: passed
      summary: "20 rows; channels present = {muon, gamma, neutron}; no empty cell in any of the 11 required columns; every bias_direction is either a member of {flatters_SB, penalizes_SB, neutral} or the explicit '-' placeholder for non-headline rows. Header block asserted to contain ZERO OVERBURDEN, BY CONSTRUCTION, 'VETO CREDIT = 1.0 EXACTLY' and '3 GW_th at 25 m'. A missing neutron row would fail outright."
      linked_ids: [claim-single-environment-set, deliv-env-registry, deliv-env-tests]
    test-hash-match:
      status: passed
      summary: "For all 20 rows the artifact_path resolves on disk and the recomputed SHA-256 equals the stored value. Zero mismatches, zero missing paths."
      linked_ids: [claim-single-environment-set, deliv-env-registry, deliv-env-tests]
    test-labels-separate:
      status: passed
      summary: "Exactly one accuracy label per channel and each equals the loader's CHANNEL_ACCURACY entry; all 8 neutron rows are order_of_magnitude. The CSV was swept for combined_band / combined_uncertainty / phase_uncertainty / overall_band / average_band / total_uncertainty (none present) and the entire public loader API was swept for any name containing combined / overall / average (none present). se.get('neutron','Phi_th') returns an EnvironmentQuantity carrying order_of_magnitude, so the tag cannot be separated from the number."
      linked_ids: [claim-single-environment-set, deliv-env-registry, deliv-env-module, deliv-env-tests]
    test-no-shield-scan:
      status: passed
      summary: "Import closure resolved to 8 modules and verified to contain surface_environment.py and veto_credit.py. Scan with SHIELDED_TOKENS + SHIELDED_TOKENS_EXTRA: source closure 29 raw hits / 0 applied; registry 8 raw / 0 applied; declaration 20 raw / 0 applied. TOTAL APPLIED = 0. The guard list is asserted to be the SAME OBJECT as Plan 09-01's, not a copy."
      linked_ids: [claim-no-shielded-quantity, deliv-env-module, deliv-env-tests, deliv-env-doc]
    test-veto-credit-unity:
      status: passed
      summary: "L2_CREDIT == L1STAR_CREDIT == L1_REJECTION_CREDIT == 1.0 exactly; credit_for(row_id) == 1.0 for every one of the 19 catalogued taxonomy rows; multiplicity_rejection_is_zero() is True (which itself consumes the Plan 08-02 derivation rather than restating it); surface_environment.veto_credit() == 1.0. The by-construction requirement is enforced by parsing the docstring for 'BY CONSTRUCTION' and 'no veto' and by asserting the registry header carries the same statement -- so a 1.0 that arrived as a default would fail even though its numeric value is correct."
      linked_ids: [claim-no-shielded-quantity, deliv-env-module, deliv-env-tests, ref-gate-verdict]
    test-bias-audit-complete:
      status: passed
      summary: "Three complete rows parsed from the declaration, each with a SIGNED deviation (Unicode-normalized first, so a U+2212 minus is not misread as a missing sign) and a direction from the closed vocabulary; the all-neutral case is explicitly rejected; the parsed directions are cross-checked against the registry's bias_direction column and must agree; the muon deviation is required to be negative and between 15% and 25%; the factor-2 gamma band and the factor-5 phi_lo move are required to be named; and the compounded-effect factor is required to be a NUMBER which the test then RECOMPUTES from the registry values and the parsed deviation, requiring agreement to 5e-4. The explicit '1 of 3' flattering count is also asserted present."
      linked_ids: [claim-directional-audit, deliv-env-doc, deliv-env-registry, deliv-env-tests]
    test-bias-audit-reviewed:
      status: partial
      summary: "The human-review content was PREPARED AND PRESENTED IN FULL, but no researcher answer has been recorded, so this test is honestly partial rather than passed. Under the standing session directive to run the roadmap to completion without per-step discussion, the checkpoint was treated as a documentation obligation: all six required presentation items appear in docs/v2.0-surface-environment.md and in the Researcher Checkpoint section of this summary -- (1) the frozen set in one table, (2) the thermal disposition stated plainly as a named value Phi_th = 2.767075e-3 cm^-2 s^-1 over 0.01-0.5 eV rather than a gap, (3) the three-row bias audit with the compounded-effect factor 1.2171 and the explicit count of 1 of 3 channels on the flattering side, (4) the weakest anchor stated without softening and verified textually against the declaration, (5) the one configuration question this phase cannot settle, and (6) what is NOT in the set. The [Y/n/e] prompt is presented. NO Phase 13/14/15 artifact was created. The researcher's answer is NOT recorded because none was given; this is the one open item of the phase and it is a judgement call, not a computation."
      linked_ids: [claim-directional-audit, deliv-env-doc, deliv-env-registry]
  references:
    ref-roadmap-p9:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "SC1 and SC5 used as the definition of done. SC5's specific demand that veto credit be 1.0 BY CONSTRUCTION rather than by policy default is enforced executably by a docstring parse and a header assertion, not only in prose."
    ref-paper-backgrounds:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "Both re-declared physics chains were written against backgrounds.tex and compared clause by clause. The declaration also discloses explicitly what the paper does NOT contain: it omitted neutrons entirely, and this set adds them."
    ref-project-contract:
      status: completed
      completed_actions: [read, avoid]
      missing_actions: []
      summary: "fp-inherited-shielding avoided and proved avoided by the executed scan (0 applied hits) and the sentinel sweep (all exactly 1.0). fp-second-vns-run avoided: no VNS pipeline, flux table or spectral shape was built; the VNS is recorded in the declaration only as a labelled scalar rescale of a finished result."
    ref-gate-verdict:
      status: completed
      completed_actions: [read, compare]
      missing_actions: []
      summary: "The Phase-8 NO-FIT verdict is the reason the veto credit is 1.0 by construction, and its recorded error pattern -- three of four errors pointing toward the expected conclusion -- is the reason the directional-bias audit exists and the reason its falsifiability was demonstrated by mutation rather than claimed."
  forbidden_proxies:
    fp-shielded-quantity-leak:
      status: rejected
      notes: "Executed scan over the registry, the declaration, the loader and its 8-module import closure: 57 raw token hits, 0 APPLIED. Two exemptions recorded with written justifications, one line-level and one whole-file, the latter backed by an independent assertion that all 19 credits in that file are exactly 1.0."
    fp-second-vns-run:
      status: rejected
      notes: "No second environment set, flux table or spectral shape for the VNS was built. The VNS appears in the declaration only as a labelled scalar (~0.28) applied to a finished primary result, in the 'what is NOT in this set' section."
    fp-silent-neutron-omission:
      status: rejected
      notes: "Eight neutron rows are present and populated; test_registry_complete fails outright on a missing neutron row. The declaration states in its own words that the v1.0 paper omitted neutrons entirely and that this set adds them."
    fp-combined-band:
      status: rejected
      notes: "No combined field in the CSV and no accessor in the loader API; both are swept by test_labels_separate. accuracy_label() takes exactly one channel and raises otherwise."
    fp-audit-as-formality:
      status: rejected
      notes: "Every row carries a signed deviation; the all-neutral case is explicitly rejected by the test; and five distinct mutations were applied to the live document and each observed to FAIL, including a wrong-but-plausible compounded factor, which the test catches by recomputing the arithmetic."
    fp-declaration-without-execution:
      status: rejected
      notes: "Every scan, hash comparison and sentinel call reported in the declaration was run, and the scan output is pasted into the declaration verbatim with the real raw-hit counts (29 / 8 / 20) rather than a tidy all-zero table."
  uncertainty_markers:
    weakest_anchors:
      - "The neutron channel's spectral shape, whose only independent cross-check is a single >10 MeV integral agreeing to ~8.8% untuned -- it dominates the uncertainty of the assembled set and is why the labels are per-channel rather than combined"
      - "The absolute environmental-gamma normalization: factor-2 site band, 238U-chain contribution set by an assumed chain balance rather than a measured line intensity"
      - "The Gaisser-Guan absolute muon normalization: 30-35% inter-experiment spread, named in the v1.0 paper itself as the weakest anchor of that channel"
      - "The muon row's flatters_SB LABEL itself: the two PDG statements bracket the adopted value, so the sign of the muon channel's directional bias is anchor-leg dependent even though its magnitude (~20%) is not"
      - "Whether the wafer is genuinely outdoors -- a configuration statement none of the three channels can settle, which moves the neutron flux by a factor ~5"
    unvalidated_assumptions:
      - "That the three ambient fields can be declared as independent incident inputs with no cross-channel coupling -- in particular that muon-induced neutron production in the wafer and its housing is out of scope rather than negligible; nothing here bounds it"
      - "That a registry frozen now will still describe the artifacts three phases later; the hash check converts this from an assumption into a test, but only at the moment the test is run"
      - "That the through-wafer interaction rate of the muon and gamma channels is a meaningful proxy for 'total background' in the compounded-effect factor; it is the only common currency that exists before the Phase-13 fold, and the neutron channel is excluded from it for exactly that reason"
    competing_explanations:
      - "If all three channels had sat on the flattering side, the benign reading would have been coincidence across three independent evidence bases and the adverse reading a systematic selection pressure in how the inputs were chosen. The audit came out 1 flattering / 1 neutral / 1 penalizing, so the benign reading is the one invoked -- and it is invoked BECAUSE the result is mixed, not in spite of it."
      - "The muon channel's flatters_SB label could be an artifact of anchor choice rather than a real bias: on PDG Leg B the same rate is +20.34% and the compounded factor becomes 0.8586. Both are reported; the label follows the leg the v1.0 paper itself invokes."
    disconfirming_observations:
      - "A shielded-token hit outside an explicit not-applied statement -- none found across 57 raw hits"
      - "A veto, coincidence or multiplicity sentinel returning anything other than exactly 1.0 -- none; all 19 catalogued rows plus the three module constants plus the loader accessor return 1.0"
      - "A registry SHA-256 failing to match its artifact on disk -- none across 20 rows"
      - "All three channels labelled flatters_SB, which would have required re-examination before any S/B is computed -- did not occur (1 of 3)"
      - "The neutron row absent, empty, or labelled with a percentage band -- none of these; 8 rows, all order_of_magnitude"
      - "STILL OPEN: the researcher has not signed off the frozen set. test-bias-audit-reviewed is partial, not passed."
comparison_verdicts:
  - subject_id: claim-single-environment-set
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-paper-backgrounds
    comparison_kind: cross_method
    metric: assembled_set_vs_v1_0_manuscript_background_treatment
    threshold: "muon and gamma chains match backgrounds.tex clause by clause; any channel the paper omits must be disclosed, not silently added"
    verdict: pass
    recommended_action: "When Phases 13-16 write, cite backgrounds.tex for the muon and gamma chains and state explicitly that the neutron channel is new relative to v1.0."
    notes: "The muon chain (Gaisser-Guan with cos theta*, ray-box chord under the inward-projection measure, Landau-Vavilov MPV, mean and Moyal explicitly not used) and the gamma chain (Klein-Nishina x Hubbell S(x,Z=32), pinned Cauchy mean chord, optically thin single scatter, continuum not photopeak, HIGH/MEDIUM confidence split) match backgrounds.tex. The set DIFFERS from the paper in exactly one disclosed way: the paper omitted neutrons entirely and this set adds them, which is stated in the registry header, the declaration and the summary rather than absorbed silently."
  - subject_id: claim-no-shielded-quantity
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-gate-verdict
    comparison_kind: cross_method
    metric: applied_shielded_token_count_and_credit_sentinel_values
    threshold: "zero APPLIED shielded-token hits across the set and its import closure; every credit sentinel exactly 1.0 and documented as by construction"
    verdict: pass
    recommended_action: "Keep the veto credit at exactly 1.0 by construction in Phases 13-16. Any later phase proposing a non-unity credit must first change the configuration, not the default."
    notes: "Import closure resolved to 8 modules. 57 raw token hits total (29 source closure, 8 registry, 20 declaration) and ZERO APPLIED. Two exemptions recorded with written justifications: the Plan 09-01 line-level entry for the NIST XCOM mu/rho of the germanium TARGET, and one whole-file entry for veto_credit.py, the Phase-8 taxonomy that names shielded statements in order to refuse them -- backed by an independent assertion that all 19 catalogued credits are exactly 1.0. L2_CREDIT, L1STAR_CREDIT, L1_REJECTION_CREDIT, credit_for() over all 19 rows and surface_environment.veto_credit() all return exactly 1.0; multiplicity_rejection_is_zero() is True. The by-construction wording is enforced by a docstring parse and a registry-header assertion, so a 1.0 arrived at as a policy default would fail despite being numerically correct."
---

# Plan 09-03 Summary

**One-liner:** see frontmatter.

## Audit A — no shielded quantity (SC5), executed

```
import closure files scanned: 8
    src/qpd_potential/compton_source.py      src/qpd_potential/params.py
    src/qpd_potential/interp_guard.py        src/qpd_potential/surface_environment.py
    src/qpd_potential/muon_deposit.py        src/qpd_potential/veto_credit.py
    src/qpd_potential/muon_flux.py           src/qpd_potential/wafer_geometry.py

scan target                          raw hits   APPLIED
src import closure (8 files)              29         0
data/surface_environment_v2.0.csv          8         0
docs/v2.0-surface-environment.md          20         0
TOTAL APPLIED                                        0
```

Sentinels: `L2_CREDIT = L1STAR_CREDIT = L1_REJECTION_CREDIT = 1.0`; `credit_for()` = 1.0 for all
**19** catalogued rows; `multiplicity_rejection_is_zero()` True; `surface_environment.veto_credit()`
= 1.0 with a **by-construction** docstring the test parses.

## Audit B — directional bias

| channel | central | anchor | signed deviation | direction |
|---|---|---|---|---|
| muon | 1.3659 Hz | PDG Leg A 1.7204 Hz | **−20.61 %** | **`flatters_SB`** |
| gamma | 2.6747e−1 Hz | LABChico measured anchor (= the adopted value) | **+0.00 %** | **`neutral`** |
| neutron | 3.550e−3 cm⁻²s⁻¹, outdoor `phi_hi` | Gordon midpoint | **+0.00 %** (untuned **−8.77 %**) | **`penalizes_SB`** |

**Channels on the flattering side: 1 of 3.**
**Compounded-effect factor = 1.2171** — replacing the one flattering choice by its anchor raises
the declared muon+gamma background from 1.63337 Hz to 1.98787 Hz, i.e. **+21.7 %**, with S/B
falling by the same factor. On PDG Leg B the muon becomes `penalizes_SB` and the factor would be
**0.8586**; both are reported.

Reported separately, not netted in: the factor-5 `phi_lo` move that was **not** taken, and the two
`flatters_SB` truncation omissions carried to Phase 13 (21 % of the >10 MeV flux above ~197 MeV;
σ_el truncated at 20 MeV).

**Falsifiability demonstrated:** sign dropped → FAIL, sign flipped → FAIL, muon relabelled
`neutral` → FAIL, factor made qualitative → FAIL, factor set to a wrong `1.5000` → FAIL, restored
→ PASS.

## Researcher Checkpoint (Task 3) — content presented, answer NOT recorded

Per the standing directive to run the roadmap to completion without per-step discussion, this
checkpoint was executed as a **documentation obligation** and the phase continued. **No researcher
answer was given, so `test-bias-audit-reviewed` is recorded `partial`, not `passed`.**

1. **The frozen set** — muon 1.3659 Hz (`pdg_within_20pct_vald02_tol_30pct`); gamma 2.6747×10⁻¹ Hz
   (`site_band_factor_2`); neutron Φ(10 MeV–10 GeV) = 3.550×10⁻³ cm⁻²s⁻¹ (`order_of_magnitude`).
2. **Thermal disposition — a named value, not a gap.** **Φ_th = 2.767075×10⁻³ cm⁻² s⁻¹** over
   **0.01 eV → 0.5 eV** (cadmium cutoff), on `data/ambient_neutron_thermal_v2.0.csv`, off the
   shared grid. This is what Phase 14 will consume. It is never zero.
3. **Bias audit** — as above. **1 of 3** channels flattering; **compounded factor 1.2171**.
4. **Weakest anchor, unsoftened** — the neutron spectral shape has **no independent validation**.
   Its only cross-check is a single >10 MeV integral agreeing to ~8.8 % untuned, which constrains
   **nothing** about the eV–keV shape that actually sets the Ge recoil rate in the CEvNS RoI. That
   is why the channel is order-of-magnitude, and why no downstream test may demand better.
5. **The configuration question this phase cannot settle** — whether the wafer is genuinely
   **outdoors**. It moves the neutron flux by a factor ~5 and reshapes it non-uniformly. It is a
   configuration statement, not an uncertainty band.
6. **What is NOT in the set** — muon-induced neutron production (in *neither* channel, recorded as
   an omission, not as negligible); the >20 MeV σ_el region; the >197 MeV flux tail (21 % of the
   >10 MeV flux); any veto credit whatsoever.

> **Accept this frozen surface environment as the input for Phases 13, 14 and 15? [Y/n/e]**
> (Enter = Y; `n` = name the channel to change; `e` = edit the audit or the labels before freezing.)

**Answer recorded: none — the researcher has not responded.** No Phase 13/14/15 artifact was
created; the phase ends here regardless of the answer.

## Deviations

- **[Rule 4] Whole-file allow-list for `veto_credit.py`.** The Phase-8 taxonomy names every
  NUCLEUS attenuation statement by design. Rather than delete the token or weaken the scan, a
  **whole-file** exemption was added with a written justification and backed by an independent
  assertion that all 19 credits are exactly 1.0.
- **[Rule 4] `shielded_token_guard()` imports from `tests/`.** A `src` module importing from
  `tests` is unusual, but the plan's requirement — reuse the constant rather than re-type it — is
  the stronger consideration, and the test asserts **object identity**.
- **Concurrency:** Phase 10 landed the shared-grid extension (`v2.0-ext`, 744 bins, now the
  default) mid-plan. All Phase-9 grid checks were re-pointed at `version="v1.0"`, which is the
  correct semantics for a frozen v1.0 artifact.

## Self-Check: PASSED

- `data/surface_environment_v2.0.csv` (20 rows), `docs/v2.0-surface-environment.md`,
  `src/qpd_potential/surface_environment.py`, `tests/test_surface_environment.py` — all FOUND
- `pytest tests/test_surface_environment.py -v` — 9 passed
- Commit `e296dd5` — FOUND
