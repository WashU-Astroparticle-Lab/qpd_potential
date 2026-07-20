---
phase: 01-conventions-energy-scale-foundation
plan: "02"
title: "Energy-scale/response-definition module (yield->rate->censoring, both variants, E_rec Phase-5 stub) + seeded stage-1 ASSUMPTIONS.md, with four limiting-case tests passing on the corrected physics"
date: 2026-07-20
status: completed
depth: full
completed: 2026-07-20
one_liner: "Built qpd_potential.energy_scale — the unified no-quenching chain E_dep->E_sensor (localized+diffuse)->N_qp=eps*E/Delta_tr->n_qp->Gamma_in=K*n_qp->peak Gamma_in=p*K*N_qp/V_tr, both dead-time censoring variants at tau_d=40us as a switch, and an E_rec Phase-5 stub — and seeded artifacts/stage1/ASSUMPTIONS.md; 4/4 limiting-case tests pass with the CORRECTED physics (25 kHz ceiling, Gamma_in Hf/Al ~3.17x ordering, equal-split flips keV-scale saturation off while muons still saturate). 14 new tests, 26/26 total."
provides:
  - "qpd_potential.energy_scale — yield/density/tunneling-rate chain, two-exponential peak factor, localized+diffuse sharing, both censoring variants (non_paralyzable default), saturation predicate, E_rec Phase-5 stub; importable by Phase 5"
  - "Saturation DEFINITION fixed: peak Gamma_in > 25 kHz (= 1/tau_d, tau_d=40us); onsets ~1.27 eV (Al) / ~0.77 eV (Hf)"
  - "artifacts/stage1/ASSUMPTIONS.md (deliv-note) — 10-section stage-1 assumptions note cross-referenced to CONVENTIONS.md + params.py"
  - "tests/test_energy_scale.py — four contract acceptance tests (test-lowrate, test-saturation, test-ordering, test-equalsplit) on the corrected physics (14 tests)"
plan_contract_ref: GPD/phases/01-conventions-energy-scale-foundation/01-02-PLAN.md#/contract

conventions:
  units: "I/O eV/keV/MeV, s, um; Gamma_in and observed rate m in Hz; densities um^-3; k_B explicit"
  metric: "N/A (no relativistic field theory; CONVENTIONS Section H)"
  coupling: "N/A for this module (CEvNS convention pointer only; sigma_tot lives in qpd_potential.cevns)"

contract_results:
  claims:
    claim-response-def:
      status: passed
      summary: "energy_scale.py implements the unified no-quenching chain N_qp=eps*E_sensor/Delta_tr -> n_qp=N_qp/V_tr -> Gamma_in=K*n_qp with the localized+diffuse per-sensor split and the two-exponential peak factor p (0.25 Al / 0.13 Hf), exposes BOTH censoring variants (non_paralyzable m=Gamma/(1+Gamma*tau_d) default, paralyzable m=Gamma*exp(-Gamma*tau_d)) at tau_d=40us as a switch, and leaves E_rec an explicit Phase-5 stub. All four limiting cases hold: low-rate m~=Gamma within 1% only for Gamma<=250 Hz (~3.85-3.92% at 1 kHz) with E_rec_linear=0.5*E_dep; non-paralyzable ceiling ->25 kHz (monotone), paralyzable peaks at 25 kHz then rolls over; Gamma_in Hf/Al ratio 3.17x (NOT 5-10x), Hf onset 0.77 eV < Al onset 1.27 eV; equal-split (f_prompt->0) flips keV-scale saturation OFF (2 keV -> ~4-6 kHz/sensor) while a 1.5 MeV muon still saturates under equal-split (~146 eV/sensor, peak Gamma_in ~3-5 MHz)."
      claim_kind: result
      linked_ids: [obs-energy-response, deliv-energy-scale, test-lowrate, test-saturation, test-ordering, test-equalsplit, ref-qpd-paper, ref-qpd-repo]
      evidence:
        - verifier: gpd-executor
          method: automated limiting-case tests (pytest)
          confidence: high
          claim_id: claim-response-def
          deliverable_id: deliv-energy-scale
          acceptance_test_id: test-lowrate
        - verifier: gpd-executor
          method: automated limiting-case tests (pytest)
          confidence: high
          claim_id: claim-response-def
          deliverable_id: deliv-energy-scale
          acceptance_test_id: test-saturation
        - verifier: gpd-executor
          method: consistency check vs 01-RESEARCH Gamma_in ratio baseline
          confidence: high
          claim_id: claim-response-def
          deliverable_id: deliv-energy-scale
          acceptance_test_id: test-ordering
          reference_id: ref-qpd-paper
        - verifier: gpd-executor
          method: automated limiting-case tests (pytest)
          confidence: high
          claim_id: claim-response-def
          deliverable_id: deliv-energy-scale
          acceptance_test_id: test-equalsplit
    claim-assumptions:
      status: passed
      summary: "artifacts/stage1/ASSUMPTIONS.md is seeded with the unified no-quenching chain + forbidden keVee/keVnr + Lindhard proxies, localized+diffuse sharing (f_prompt=0.3 / r=2 flagged LOW + exposed), eps~=0.5 yield/efficiency, both censoring variants (default non-paralyzable) as an OPEN switch, defect=0, the Table II per-design parameter table, the flagged bulk alpha-Ta gap (MEDIUM), detector geometry (110 g / ~10300 sensors / per-kg normalization), BOTH design ratios (4.75x N_qp raw yield, 3.2x Gamma_in ordering driver), and the CEvNS convention pointer."
      claim_kind: other
      linked_ids: [deliv-note, test-assumptions-content]
      evidence:
        - verifier: gpd-executor
          method: content existence + numeric cross-check vs params.py / CONVENTIONS.md
          confidence: high
          claim_id: claim-assumptions
          deliverable_id: deliv-note
          acceptance_test_id: test-assumptions-content
  deliverables:
    deliv-energy-scale:
      status: passed
      path: src/qpd_potential/energy_scale.py
      summary: "Energy-scale/response-definition module: n_qp_yield, qp_density, tunneling_rate, peak_factor, peak_tunneling_rate, sensor_energy_split (localized+diffuse, f_prompt/r exposed), peak_gamma_in_from_{sensor_energy,deposit}, saturation_onset_energy, observed_rate (both variants switch), is_saturated (25 kHz), E_rec_estimator (Phase-5 stub). Constants imported from qpd_potential.params; nothing re-encoded."
      linked_ids: [claim-response-def, test-lowrate, test-saturation, test-ordering, test-equalsplit]
    deliv-note:
      status: passed
      path: artifacts/stage1/ASSUMPTIONS.md
      summary: "10-section stage-1 assumptions note (energy chain + forbidden proxies, yield/efficiency, localized+diffuse sharing, censoring switch, defect=0, geometry/normalization, Table II table + flagged Ta gap, design asymmetry with both ratios, CEvNS pointer, weakest anchors + disconfirming checks)."
      linked_ids: [claim-assumptions, test-assumptions-content]
  acceptance_tests:
    test-lowrate:
      status: passed
      summary: "Both variants give m~=Gamma within 1% for Gamma in {100,250} Hz (dev 0.40%/0.99%); at 1 kHz dev is 3.85% (non-par)/3.92% (par) -- asserted >1% AND <5% AND ~Gamma*tau_d (rel 0.2). E_rec linear placeholder = 0.5*E_dep; default E_rec_estimator raises NotImplementedError."
      linked_ids: [claim-response-def, deliv-energy-scale]
    test-saturation:
      status: passed
      summary: "Non-paralyzable m monotone increasing, <=25 kHz, ->25 kHz at large Gamma (max 24937.7 Hz over 1e2-1e7). Paralyzable argmax at Gamma=25.0 kHz, peak value 25kHz/e (~9197 Hz), decreasing after. Ceiling asserted = 1/40us = 25 kHz, explicitly NOT 50 kHz."
      linked_ids: [claim-response-def, deliv-energy-scale]
    test-ordering:
      status: passed
      summary: "Plateau Gamma_in Hf/Al ratio = 3.1667 (in [2.5,4.0], asserted <5); N_qp-per-eV ratio = 4.75 recorded as the RAW yield ratio. Saturation onset (peak Gamma_in=25 kHz): Hf 0.769 eV < Al 1.267 eV -> Hf saturates first."
      linked_ids: [claim-response-def, deliv-energy-scale]
    test-equalsplit:
      status: passed
      summary: "(1) keV-scale (2 keV) deposit: saturates under default f_prompt=0.3 (localized) but NOT under equal-split f_prompt->0 (both designs) -- localization flips saturation on/off. (2) Muon (1.5 MeV) still saturates under equal-split (~146 eV/sensor >> onset) for both designs -- localization sets degree not existence. Plus a guard that the DEFAULT sharing saturates keV deposits."
      linked_ids: [claim-response-def, deliv-energy-scale]
    test-assumptions-content:
      status: passed
      summary: "artifacts/stage1/ASSUMPTIONS.md exists and contains every required section: no-quenching chain + forbidden proxies, sharing (f_prompt/r flagged LOW), eps~=0.5, both censoring variants (default non-paralyzable), defect=0, Table II table, flagged Ta gap, geometry with per-kg normalization. Numbers cross-checked against params.py and CONVENTIONS.md."
      linked_ids: [claim-assumptions, deliv-note]
  references:
    ref-qpd-paper:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Table II device parameters (Delta_tr, V_tr, K, tau_qp, p) consumed via qpd_potential.params (verbatim from 01-RESEARCH PDF transcription), used in the yield/rate chain and peak factor, and cited in energy_scale.py + ASSUMPTIONS.md. The ~3.2x Gamma_in ordering and pulse-Eq.(4) peak factor derive from this reference."
    ref-qpd-repo:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "Read /Users/lanqingyuan/Documents/GitHub/qpd/src/qpd/simulator/quasiparticle_bursts.py directly (QuasiparticleBurstModel: N~Poisson(expected_n_qp); offsets=Normal(mu,sigma)+Exp(tau); absolute times=t0+offsets). Its parametrization fixes the 'peak instantaneous rate' definition that peak_tunneling_rate approximates via the two-exponential peak factor. Verbatim reuse of the generator is Phase 5 (carry-forward); Phase 1 needed only its parametrization."
  forbidden_proxies:
    fp-nosat:
      status: rejected
      notes: "Equal-split is NOT the default: default localized sharing (f_prompt=0.3) saturates keV-scale deposits (test_equalsplit_is_not_the_default_sharing_model). Equal-split is used only as the sanity knob that flips keV-scale saturation off; muon saturation degree is preserved by localization (muons still saturate even under equal-split, ~146 eV/sensor)."
    fp-derived-sharing:
      status: rejected
      notes: "f_prompt and r are function ARGUMENTS (default from params, range documented), flagged LOW/EXPOSED in the docstring and in ASSUMPTIONS.md section 3 as the weakest anchor; never presented as derived values."
    fp-20us:
      status: rejected
      notes: "tau_d=40e-6 s (params.TAU_D), ceiling=1/tau_d=25 kHz; test_saturation_ceiling_is_25kHz_not_50kHz asserts tau_d!=20us and |ceiling-50kHz|>1."
    fp-nqp-ordering:
      status: rejected
      notes: "Ordering uses the Gamma_in ratio 3.1667 (asserted in [2.5,4.0] and <5); the 4.75x N_qp-per-eV ratio is explicitly labeled the RAW yield ratio, not the saturation ordering."
  uncertainty_markers:
    weakest_anchors:
      - "f_prompt (0.3) and r (2 sensors) have no thin-wafer QPD measurement (LOW); the muon spectrum shape depends strongly on them"
      - "Muon deposit point-collapse over-states per-sensor saturation vs a real ~cm track"
      - "Ta absorber gap ~0.68 meV is a bulk alpha-Ta BCS assumption; film phase unverified (MEDIUM)"
      - "Two-exponential peak factor p (0.25 Al / 0.13 Hf) is MEDIUM; sets the onset energies but not the qualitative saturation conclusion"
    unvalidated_assumptions:
      - "Uniform diffuse spread of the (1-f_prompt) fraction across all ~10300 sensors"
      - "Trap-gap quantum (N_qp proportional to 1/Delta_tr) rather than an effective quantum nearer Delta_abs"
      - "Table II K and V_tr transfer to this wafer geometry"
    competing_explanations:
      - "The DEGREE of muon compression (how many sensors saturate) could be an artifact of point-collapse + localization; the equal-split limit isolates this -- muon saturation EXISTENCE is robust (survives equal-split), only the degree is model-dependent"
    disconfirming_observations:
      - "A keV-scale deposit saturating under equal-split (f_prompt->0) -- would show the sharing model is mis-specified (verified false: 2 keV -> ~4-6 kHz/sensor)"
      - "Non-paralyzable ceiling at 50 kHz instead of 25 kHz (verified 25 kHz)"
      - "Gamma_in Hf/Al ratio far from ~3 (e.g. 5-10x) -- an N_qp-only ordering error (verified 3.17x)"

comparison_verdicts:
  - subject_id: claim-response-def
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-qpd-paper
    comparison_kind: consistency
    metric: relative_error
    threshold: "<= 0.10"
    verdict: pass
    recommended_action: "Import qpd_potential.energy_scale into the Phase-5 response matrix; resolve the paralyzable/non-paralyzable switch before finalizing Phase-5 saturation numbers."
    notes: "Plateau Gamma_in Hf/Al ratio computed 3.1667 vs the 01-RESEARCH baseline 3.17 (=(20/3)(190/40)(100/1000)); relative error <0.2%. Onsets 1.27 eV (Al) / 0.77 eV (Hf) match RESEARCH's ~1.3 eV / ~0.8 eV. 25 kHz ceiling matches CONVENTIONS Section F."
---

# Plan 01-02 Summary — Energy-Scale / Response-Definition Module + Stage-1 Assumptions Note

## What this plan established

Turned the locked conventions and the Plan-01 parameter foundation into a small,
tested **energy-scale / response-DEFINITION module** and seeded the stage-1
assumptions note. This fixes the `E_dep -> per-sensor yield -> tunneling-rate ->
bandwidth-censoring` chain and the **saturation DEFINITION** (peak Gamma_in vs
25 kHz) so Phase 5 has an unambiguous, physically-reachable response model —
**without computing any spectrum**. Constants are IMPORTED from
`qpd_potential.params`; nothing is re-encoded.

## Module API (`qpd_potential.energy_scale`)

| Function | Returns | Formula / role |
|---|---|---|
| `n_qp_yield(E_sensor_eV, design)` | N_qp (count) | `eps * E_sensor / Delta_tr` |
| `qp_density(N_qp, design)` | n_qp [um^-3] | `N_qp / V_tr` |
| `tunneling_rate(n_qp, design)` | Gamma_in [Hz] | `K * n_qp` (plateau) |
| `peak_factor(design)` | p | 0.25 (Al) / 0.13 (Hf), paper Eq. 4 |
| `peak_tunneling_rate(N_qp, design)` | peak Gamma_in [Hz] | `p * K * N_qp / V_tr` |
| `sensor_energy_split(E_dep, f_prompt, r, n_sensors, on_spot)` | E_sensor [eV] | `f_prompt*E/(pi r^2) + (1-f_prompt)*E/N_sens` |
| `saturation_onset_energy(design)` | E_sensor [eV] | E where peak Gamma_in = 25 kHz |
| `observed_rate(Gamma, variant, tau_d)` | m [Hz] | non_paralyzable (default) / paralyzable switch |
| `is_saturated(peak_Gamma_in)` | bool | `peak > 25 kHz` |
| `E_rec_estimator(E_dep, linear_placeholder)` | E_rec [eV] | **Phase-5 STUB** (raises; or `0.5*E_dep` placeholder) |

`f_prompt` and `r` are exposed as arguments (defaults from params, LOW confidence).

## Four limiting-case results (all PASS on the corrected physics)

| Test | Result | Corrected-physics point |
|---|---|---|
| **Low-rate linearity** | 100 Hz: 0.40% dev; 250 Hz: 0.99%; **1 kHz: 3.85% (non-par) / 3.92% (par)** | m~=Gamma within 1% ONLY for Gamma<=250 Hz; ~5% at 1 kHz — did NOT over-claim 1% at 1 kHz. E_rec_linear=0.5*E_dep. [CONFIDENCE: HIGH] |
| **Saturation ceiling** | non-par -> 25 kHz (max 24937.7, monotone); par peaks at Gamma=25.0 kHz (value 25kHz/e~=9197) then rolls over | Ceiling is **25 kHz = 1/40us**, NOT 50 kHz. Both variants. [CONFIDENCE: HIGH] |
| **Hf-before-Al ordering** | Gamma_in Hf/Al = **3.1667** (NOT 5-10x); onsets Hf 0.77 eV < Al 1.27 eV | Gamma_in-based ~3.2x ordering; 4.75x is the RAW N_qp yield ratio, partly cancelled by Hf's 10x V_tr & 6.7x K. [CONFIDENCE: HIGH] |
| **Equal-split sanity** | 2 keV: saturates localized (~0.94-1.56 MHz/sensor), NOT equal-split (~3.8-6.3 kHz); 1.5 MeV: saturates even equal-split (~2.9-4.7 MHz, ~146 eV/sensor) | keV scale is the binary on/off discriminator; muons saturate regardless of localization — localization sets DEGREE not existence. [CONFIDENCE: HIGH] |

**Saturation-onset order of magnitude:** ~1.27 eV (Al) / ~0.77 eV (Hf) per sensor
(peak Gamma_in = 25 kHz). Muon deposits (>= MeV, localized) exceed this by many
orders of magnitude -> deep saturation; spread CEvNS/Compton deposits (sub-keV over
many sensors) stay below -> linear. **Saturation is physically reachable** (the
CONTEXT acceptance signal), and NOT trivially assumed away.

## Dimensional consistency

`Gamma_in = K[Hz*um^3] * n_qp[um^-3] = Hz`; `N_qp = eps*E_sensor[eV]/Delta_tr[eV]`
dimensionless; `m` in Hz; `peak Gamma_in = p * (plateau Gamma_in)` exactly (unit
test `test_chain_dimensional_consistency`). Verified for both designs.

## ASSUMPTIONS.md seed (deliv-note)

`artifacts/stage1/ASSUMPTIONS.md` — 10 sections, cross-referenced to CONVENTIONS.md
and params.py: (1) unified no-quenching chain + forbidden keVee/keVnr + Lindhard
proxies; (2) yield/efficiency (eps~=0.5, trap-gap quantum); (3) localized+diffuse
sharing (f_prompt/r LOW + exposed, weakest anchor); (4) censoring switch (tau_d=40us,
both variants, non-par default, OPEN question blocking Phase 5); (5) defect=0;
(6) geometry/normalization (110 g / ~10300 sensors / per-kg); (7) Table II per-design
table + flagged bulk alpha-Ta gap (MEDIUM) + trapping margins 3.58/4.75 (both valid,
lower-bound >= 2) + BOTH design ratios (4.75x N_qp, 3.2x Gamma_in ordering driver);
(8) CEvNS convention pointer; (9) weakest anchors + disconfirming checks; (10) out of
scope (Deferred Ideas).

## Task 3 — authored checkpoint work done by executor (researcher should confirm at wave gate)

This plan's authored `checkpoint:human-verify` (Task 3) was performed by the executor
under a **supervised one-shot handoff**. The following are **recorded for researcher
confirmation, NOT fabricated approval** — resume signal `[Y/n/e]` remains with the
orchestrator/researcher:

- **(a) Four limiting-case results** — low-rate linearity (m~=Gamma within 1% only
  <=250 Hz; E_rec~=0.5*E_dep), 25 kHz ceiling (non-par monotone to 25 kHz; paralyzable
  rollover peaking at 25 kHz), Gamma_in-based Hf-before-Al ordering (**3.17x, explicitly
  NOT 5-10x**), and the equal-split sanity (keV-scale f_prompt->0 flips saturation off;
  a genuine muon still saturates under equal-split). All 14 tests pass.
- **(b) keV vs muon saturation gating** — keV-scale (CEvNS/Compton) saturation is
  localization-gated (spread -> linear, localized -> saturates); muon saturation is
  robust regardless of sharing (the corrected CONTEXT acceptance signal). Verified
  numerically (2 keV and 1.5 MeV, both designs).
- **(c) ASSUMPTIONS.md seed** — especially the LOW-confidence flags on f_prompt/r and
  the MEDIUM Ta gap, and that the censoring switch is preserved as an **OPEN question
  blocking Phase 5** (paralyzable vs non-paralyzable NOT silently chosen).

**Suggested researcher spot-check:** the LOW f_prompt/r defaults (the muon-spectrum-shape
driver) and the MEDIUM Ta gap; and confirm the paralyzable/non-paralyzable switch should
remain open into Phase 5.

## Scope discipline

No spectrum computed; no per-design crossover energy (Phases 3-6). E_rec estimator is a
deliberate Phase-5 stub (NotImplementedError by default). No Deferred Ideas implemented
(along-track muon sharing, per-design eps split, localization sensitivity scan,
position-dependent phonon model). No keVee/keVnr or Lindhard/ionization quenching.

## Reproducibility

- Python 3.11.7 (Anaconda); numpy 1.26.4; pytest (declared >=7.4 in pyproject).
- No RNG (deterministic closed-form arithmetic; the EMG generator's stochastic peak-rate
  realization is Phase 5).
- Run: `python3 -m pytest -q` from repo root (conftest path shim). **26 passed** (12 prior + 14 new).

## Commits

| Hash | Task |
|---|---|
| ae9dba1 | Task 1 — energy_scale.py module + 4 limiting-case tests (14 tests) |
| b01f49f | Task 2 — artifacts/stage1/ASSUMPTIONS.md seed (deliv-note) |

## Deviations

None. No deviation rules triggered. One design clarification recorded (documented below,
not a deviation): the ~3.2x Hf/Al ordering is the **plateau** Gamma_in ratio (peak-factor-
independent, the paper's saturation-driving quantity), while the per-design saturation
**onset energies** carry the per-design peak factor p (0.25 Al / 0.13 Hf). Both are
correct and mutually consistent (onset ratio differs from 3.2x because p differs by design).

## Self-Check: PASSED

All created files exist; both task commits (ae9dba1, b01f49f) present; `pytest -q`
reproduces 26 passed; ASSERT_CONVENTION lines present in module + tests; the embedded
`gpd_return` YAML parses (status=completed, phase=01, plan=01-02, 4 files, no top-level
`blockers`). Contract coverage: both claims, both deliverables, all five acceptance
tests, both must-surface references (ref-qpd-paper, ref-qpd-repo — read directly), and
all four forbidden proxies have explicit ledger entries.

## Machine return

```yaml
gpd_return:
  status: completed
  phase: "01"
  plan: "01-02"
  files_written:
    - src/qpd_potential/energy_scale.py
    - tests/test_energy_scale.py
    - artifacts/stage1/ASSUMPTIONS.md
    - GPD/phases/01-conventions-energy-scale-foundation/01-02-SUMMARY.md
  issues:
    - "Task 3 authored human-verify checkpoint performed by executor under supervised one-shot handoff; researcher should confirm the four limiting-case results, the keV-vs-muon saturation gating, and that the paralyzable/non-paralyzable censoring switch stays OPEN into Phase 5. Not fabricated approval."
    - "Weakest anchors carried forward (LOW): f_prompt=0.3 / r=2 sensors have no thin-wafer QPD measurement and drive the muon spectrum shape; Ta gap ~0.68 meV is a MEDIUM bulk alpha-Ta assumption."
  next_actions:
    - "Phase 5: resolve the paralyzable-vs-non-paralyzable (and merge-vs-drop) censoring switch — the OPEN question blocking final saturation numbers — before building the response matrix."
    - "Phase 5: implement the real E_rec estimator (count-integral vs time-over-saturation vs hybrid), replacing the linear_placeholder stub; reuse quasiparticle_bursts.QuasiparticleBurstModel verbatim for the stochastic peak-instantaneous-rate realization."
  state_updates:
    advance_plan: false
    update_progress: false
    record_metric:
      phase: "01"
      plan: "01-02"
      duration: 330
      tasks: 3
      files: 4
  contract_updates:
    claims_passed: [claim-response-def, claim-assumptions]
    deliverables_passed: [deliv-energy-scale, deliv-note]
    acceptance_tests_passed: [test-lowrate, test-saturation, test-ordering, test-equalsplit, test-assumptions-content]
    references_completed: [ref-qpd-paper, ref-qpd-repo]
    forbidden_proxies_rejected: [fp-nosat, fp-derived-sharing, fp-20us, fp-nqp-ordering]
  decisions:
    - summary: "Saturation ordering fixed as the plateau Gamma_in Hf/Al ratio (3.17x); the 4.75x N_qp-per-eV ratio is the raw yield, not the saturation driver."
      phase: "01-conventions-energy-scale-foundation"
    - summary: "Per-design saturation onset energies (~1.27 eV Al / ~0.77 eV Hf) carry the two-exponential peak factor p (0.25 Al / 0.13 Hf); Hf saturates first."
      phase: "01-conventions-energy-scale-foundation"
    - summary: "E_rec estimator implemented as an explicit Phase-5 stub (NotImplementedError by default; linear_placeholder=True returns 0.5*E_dep, valid only in the unsaturated regime)."
      phase: "01-conventions-energy-scale-foundation"
    - summary: "Both censoring variants exposed as a switch at tau_d=40us; the paralyzable-vs-non-paralyzable choice is preserved OPEN as a Phase-5 blocker, not silently chosen."
      phase: "01-conventions-energy-scale-foundation"
```
