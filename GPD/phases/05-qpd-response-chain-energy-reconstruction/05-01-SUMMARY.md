---
phase: 05-qpd-response-chain-energy-reconstruction
plan: 01
plan_contract_ref: GPD/phases/05-qpd-response-chain-energy-reconstruction/05-01-PLAN.md#/contract
title: "QPD response chain: count-integral E_rec estimator (replacing the Phase-1 stub) + forward realization + per-design crossover band; VALD-04 limits validated"
date: 2026-07-21
status: completed
depth: full
completed: 2026-07-21
one_liner: "Count-integral E_rec estimator replaces the Phase-1 stub: low-E E_rec=0.5*E_dep by calibration, high-E plateau (non_paralyzable, ~27-35 keV at 197 MeV) / rollover (paralyzable, ~2.6-3.3 keV); per-design crossover reported as a band (default ~53/32 eV, equal-split anchor ~13/7.9 keV, Hf first); Ta binary trapping gate asserted."
provides:
  - "qpd_potential.response — forward single-deposit realization (sharing->yield->EMG burst->censoring->summed censored count) + calibrated count-integral E_rec estimator replacing the Phase-1 stub; both censoring variants selectable; importable by Plan 05-02"
  - "Count-integral E_rec estimator E_rec=C*sum_i N_obs,i, single global per-design C fixed to slope 0.5; low-E linear, high-E plateau (non_paralyzable) / rollover (paralyzable)"
  - "Event-count mapping expected_n_qp = INT Gamma_in dt = K*tau_qp*N_qp/V_tr (NOT trapped N_qp) into the MUST-USE QuasiparticleBurstModel EMG template"
  - "Per-design crossover band (SIMU-01): default ~52.9/32.1 eV, equal-split anchor ~13.1/7.9 keV, whole-array plateau ~18.6/11.3 keV, Hf first; Ta binary trapping gate assert"
  - "tests/test_response_chain.py — 36 acceptance tests (VALD-04 limits, crossover band, Hf-first, Ta gate, stop-condition); artifacts/stage1/ASSUMPTIONS.md Phase-5 append"
contract_results:
  claims:
    claim-estimator:
      status: passed
      summary: "Count-integral estimator E_rec=C*sum_i N_obs,i, single global per-design C fixed to slope eps=0.5, reproduces E_rec~=0.5*E_dep at low E and PLATEAUS (non_paralyzable) / ROLLS OVER (paralyzable) in saturation for both designs; the plateau is the explicitly-modeled saturation, not a linear extrapolation. expected_n_qp fed the event count INT Gamma_in dt (=K*tau_qp*N_qp/V_tr), not the trapped N_qp."
      linked_ids: [deliv-response-code, deliv-crossover-note, test-low-e-linear, test-high-e-plateau, test-eventcount-mapping, ref-qpd-paper, ref-qpd-repo]
    claim-crossover:
      status: passed
      summary: "Crossover deposit energy reported as an f_prompt in [0.1,0.5], r in [1,5] band: default ~52.9 eV (Ta->Al) / ~32.1 eV (Al->Hf), scan span ~8 eV-0.93 keV, equal-split upper anchor ~13.1/7.9 keV; Hf saturates before Al at every scan point; two saturation scales stated (on-spot bend ~tens of eV, whole-array plateau ~18.6 keV Al / ~11.3 keV Hf)."
      linked_ids: [deliv-crossover-note, deliv-response-code, test-crossover-band, test-hf-first, ref-qpd-paper]
    claim-ta-gate:
      status: passed
      summary: "Ta->Al response is numerically invariant to Delta_abs(Ta) within alpha-phase (arithmetic uses the Al trap gap Delta_tr everywhere; verified for Delta_abs in {0.5,0.68,0.9} meV); the only Ta-gap dependence is the binary trapping gate Delta_abs/Delta_tr>=2 (ratio 3.58, T_c 4.48 K >= 2.5 K gate), asserted in code; beta-Ta would fail the gate and invalidate the design. No film value fabricated."
      linked_ids: [deliv-response-code, deliv-crossover-note, test-ta-gate, ref-qpd-paper]
  deliverables:
    deliv-response-code:
      status: passed
      path: src/qpd_potential/response.py
      summary: "Forward single-deposit realization (sharing->yield->EMG burst->censoring->summed censored count) + calibrated count-integral E_rec estimator replacing the Phase-1 stub; both censoring variants selectable; event-count mapping and Ta trapping-gate assert included. 167/167 tests pass (36 new)."
      linked_ids: [claim-estimator, claim-crossover, claim-ta-gate, test-low-e-linear, test-high-e-plateau, test-eventcount-mapping]
    deliv-crossover-note:
      status: passed
      path: artifacts/stage1/ASSUMPTIONS.md
      summary: "Phase-5 append: per-design crossover band + two saturation scales, Hf-first ordering, Ta binary trapping gate (not a smooth band, no fabricated film value), and the explicit NO-literature-anchor caveat on the saturated-regime shape. Default point flagged as SIMU-01's explicit design number."
      linked_ids: [claim-crossover, claim-ta-gate, test-crossover-band]
  acceptance_tests:
    test-low-e-linear:
      status: passed
      summary: "E_rec/E_dep = 0.5 within 1% for both designs and both variants at deeply-linear deposits (0.02-0.1 eV), LABELED as calibration-consistency (C is fixed by this slope), not independent validation."
      linked_ids: [claim-estimator, deliv-response-code]
    test-high-e-plateau:
      status: passed
      summary: "VARIANT-SPECIFIC and both non-linear at 197 MeV: non_paralyzable summed count caps -> E_rec monotone plateau (~27-35 keV, <2x over the top decade, ratio to 0.5*E_dep ~3.5e-4); paralyzable count rolls over -> E_rec peaks ~keV then declines (~2.6-3.3 keV, ratio ~3e-5). Neither tracks the linear 0.5*E_dep line. Stop-condition checked (plateau present where peak Gamma_in >> 25 kHz) with a no-censoring teeth check."
      linked_ids: [claim-estimator, deliv-response-code, deliv-crossover-note]
    test-eventcount-mapping:
      status: passed
      summary: "expected_n_qp == INT Gamma_in dt == K*tau_qp*N_qp/V_tr (verified numerically) and emphatically != N_qp (0.03x Al / 0.008x Hf); realization saturation onset matches saturation_onset_energy through sensor_energy_split (peak Gamma_in=25 kHz at crossover); QuasiparticleBurstModel realized total count reproduces the Poisson mean within MC. Guards Pitfall 1."
      linked_ids: [claim-estimator, deliv-response-code, ref-qpd-repo]
    test-crossover-band:
      status: passed
      summary: "In-code crossover E_dep=E_onset/[f_prompt/(pi r^2)+(1-f_prompt)/n_sensors] reproduces the default point ~52.9/32.1 eV within 10% and the equal-split anchor ~13.1/7.9 keV within 10%; reported as a band (scan max/min ratio >10, equal-split above the scan)."
      linked_ids: [claim-crossover, deliv-crossover-note, deliv-response-code]
    test-hf-first:
      status: passed
      summary: "Al->Hf per-sensor onset (0.77 eV) and crossover E_dep are below Ta->Al (1.27 eV) everywhere in the f_prompt/r scan grid."
      linked_ids: [claim-crossover, deliv-response-code]
    test-ta-gate:
      status: passed
      summary: "Trapping gate Delta_abs/Delta_tr>=2 holds for both cited baselines (Ta->Al 3.58, T_c gate 2.5 K); assert fires on a sub-gate (beta-Ta) ratio; Ta->Al crossover and E_rec invariant to Delta_abs within alpha-phase."
      linked_ids: [claim-ta-gate, deliv-response-code]
  references:
    ref-qpd-paper:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Ramanathan et al. (2026) pulse Eq. 4 / Gamma_in=K*n_qp / Table II reused verbatim via params.py; two-exponential pulse verified consistent with the recorded peak factors; cited in response.py docstrings and this summary. The saturated-regime reconstruction is this phase's novelty (not in the paper)."
    ref-qpd-repo:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "QuasiparticleBurstModel EMG burst template read fully and used as the MUST-USE tunneling-event realization, with expected_n_qp fed the event-count integral (Pitfall 1)."
  forbidden_proxies:
    fp-no-saturation:
      status: rejected
      notes: "The estimator plateau (non_paralyzable) / rollover (paralyzable) IS the modeled saturation; E_rec at 197 MeV is ~3.5e-4 (np) / ~3e-5 (par) of the linear 0.5*E_dep line. A no-censoring scratch run gives exactly 0.5*E_dep (no plateau), confirming the plateau is due to censoring."
    fp-eventcount:
      status: rejected
      notes: "expected_n_qp is fed INT Gamma_in dt = K*tau_qp*N_qp/V_tr, asserted != N_qp; conflating them would mis-scale the saturation onset/plateau."
    fp-calib-as-validation:
      status: rejected
      notes: "Low-E linearity is explicitly labeled calibration-consistency (C fixed by that slope); the genuinely validated content is the saturation onset and plateau/rollover level."
    fp-crossover-point:
      status: rejected
      notes: "Crossover reported as an f_prompt/r band with the equal-split upper anchor, not a single measured number; the ~3-order spread is f_prompt-dominated."
    fp-ta-band:
      status: rejected
      notes: "Delta_abs(Ta) enters the response arithmetic nowhere; carried as a binary trapping gate, not a continuous response band; no beta-Ta film value fabricated."
  uncertainty_markers:
    weakest_anchors:
      - "The saturated-regime response SHAPE has NO literature anchor at any energy; validation is limiting-cases-only"
      - "f_prompt / r are LOW-confidence unmeasured sharing parameters that dominate the crossover scale (~3 orders)"
      - "EMG (Normal+Exp) is not the exact two-exponential pulse; only the count and peak-rate invariants are preserved (Hf peak factor 0.1337 vs recorded 0.13)"
    unvalidated_assumptions:
      - "Single global calibration constant C per design captures the whole linear branch"
      - "Bulk alpha-Ta gap applies to the deposited film (T_c >= 2.5 K trapping gate)"
      - "Analytic censored-integral (deliverable estimator) vs EMG event-train realization diverge O(10-30%) in deep saturation (closed-form renewal vs microphysical dead-window)"
    competing_explanations:
      - "Paralyzable vs non-paralyzable censoring (CONVENTIONS F) is an OPEN switch, carried not closed; the muon-tail shape (plateau vs rollover) depends on it"
      - "A secondary time-over-saturation estimator would recover slow log-rising high-E ordering (deferred; unvalidated, tau_qp-dependent)"
    disconfirming_observations:
      - "peak Gamma_in >> 25 kHz at the 197 MeV muon tail but no plateau/rollover would mean the saturation model is wrong -> HALT (checked: does NOT trigger)"
      - "The Ta->Al response curve shifting when Delta_abs varies within alpha-phase would indicate the gate is mis-modeled (checked: invariant)"
      - "The crossover E_dep being insensitive to f_prompt would indicate the sharing model is not wired in (checked: spans ~3 orders)"
---

# Plan 05-01 Summary — QPD Response Chain & Count-Integral E_rec Estimator

## What was done

Turned the Phase-1 forward-chain scaffold into a working per-design reconstructed-energy
response (`src/qpd_potential/response.py`), implementing the deliberately-stubbed `E_rec`
estimator as a **calibrated count-integral estimator** and reporting the linear->saturated
crossover as a **band**. Everything upstream (sharing, yield, tunneling rate, peak factor,
saturation onset, both censoring closed forms) is imported from the scaffold; the MUST-USE
qpd `QuasiparticleBurstModel` EMG template realizes the tunneling-event train.

**Task 1 (`implement`, `f71d092`):** forward realization + estimator.
**Task 2 (`validate`, `5720532`):** 36 acceptance tests + Phase-5 ASSUMPTIONS.md append.
**Task 3 (checkpoint:human-verify):** self-assessed against all acceptance tests below;
**satisfied, pending orchestrator/researcher review** (autonomous run — not blocked).

## Conventions in effect

| Item | Value |
| --- | --- |
| Units | energy eV; time s; length um; rate Hz (CONVENTIONS A) |
| Energy scale | single unified phonon scale, NO quenching; E_rec(low-E)~=0.5*E_dep (CONVENTIONS B) |
| Efficiency | eps=0.5 deposited-to-signal baseline (CONVENTIONS E) |
| Saturation | 40 us resolving time = 25 kHz ceiling LOCKED (CONVENTIONS F) |
| Censoring | paralyzable AND non_paralyzable BOTH carried (OPEN switch, CONVENTIONS F) |

## Key physics results

- **Two-exponential pulse self-consistency [CONFIDENCE: HIGH]:** `INT g dt = 1` and
  `tau_qp*max(g) = p` reproduce the recorded peak factors exactly (0.2500 Al; 0.1337 Hf,
  = recorded 0.13 to 2 sig figs). Hence `event_count = INT Gamma_in dt = K*tau_qp*N_qp/V_tr`
  and `peak Gamma_in = p*K*N_qp/V_tr` are both preserved (Pitfall 1 mapping).
- **Low-E slope [CONFIDENCE: HIGH, calibration-consistency]:** `E_rec/E_dep = 0.5` to <1%
  for both designs/variants below onset. This is definitional (C fixed by it), not
  independent validation.
- **High-E, 197 MeV muon tail [CONFIDENCE: MEDIUM — model prediction, no benchmark]:**
  - non_paralyzable: E_rec PLATEAUS, monotone, ~35 keV (Ta->Al) / ~27 keV (Al->Hf), only
    logarithmic growth; `E_rec/(0.5*E_dep) ~ 3.5e-4`.
  - paralyzable: E_rec ROLLS OVER (peaks ~keV, declines to ~3.3 keV / ~2.6 keV);
    `~3e-5` of the linear line.
  - Neither tracks 0.5*E_dep into the MeV range (guards fp-no-saturation on both branches).
- **Crossover band (SIMU-01) [CONFIDENCE: MEDIUM — f_prompt-dominated]:**

  | Design | Onset E_sensor | Default (f=0.3,r=2) | Scan band | Equal-split anchor | Whole-array plateau |
  | --- | --- | --- | --- | --- | --- |
  | Ta->Al | 1.27 eV | ~52.9 eV | 8.0 eV-0.93 keV | ~13.1 keV | ~18.6 keV |
  | Al->Hf | 0.77 eV | ~32.1 eV | 4.8 eV-0.57 keV | ~7.9 keV | ~11.3 keV |

  Hf saturates first everywhere. Default point = SIMU-01's explicit design number; band =
  honest uncertainty.
- **Ta trapping gate [CONFIDENCE: HIGH]:** ratio 3.58 >= 2 (T_c 4.48 K >= 2.5 K gate);
  response invariant to Delta_abs within alpha-phase; beta-Ta invalidating; binary gate,
  not a response band; no fabricated film value.

## Stop condition

Checked and **does not trigger**: at 197 MeV `peak Gamma_in` exceeds the 25 kHz ceiling by
~10^6-10^7x and the count-integral DOES saturate (plateau/rollover). A no-censoring scratch
run yields exactly `E_rec = 0.5*E_dep` (no plateau), confirming the plateau assertion has teeth.

## Deviations

None requiring researcher sign-off. One documented modeling note: the exact two-exponential
peak factor is 0.1337 for Hf vs the recorded 0.13 (2-sig-fig rounding); immaterial vs the
f_prompt band. The analytic censored-integral (the deliverable estimator, used for the
infeasible-to-realize muon-tail sweep) and the EMG event-train realization agree to ~1% up to
mild saturation and diverge O(10-30%) in deep saturation — an additional unvalidated-shape
uncertainty, carried in the note.

## Verification

167/167 tests pass (`pytest`), 36 new in `tests/test_response_chain.py`. Both censoring
variants selectable end-to-end; event-count mapping cross-checked against inhomogeneous-
Poisson thinning; crossover a band; Hf-first holds; Ta gate a binary assert; stop-condition
fails loudly if the plateau is absent.

## Machine-readable return

```yaml
gpd_return:
  status: completed
  phase: "05"
  plan: "01"
  tasks_completed: 3
  tasks_total: 3
  duration_seconds: 2700
  files_written:
    - src/qpd_potential/response.py
    - tests/test_response_chain.py
    - artifacts/stage1/ASSUMPTIONS.md
    - GPD/phases/05-qpd-response-chain-energy-reconstruction/05-01-SUMMARY.md
  contract_updates:
    claims_passed: [claim-estimator, claim-crossover, claim-ta-gate]
    acceptance_tests_passed:
      - test-low-e-linear
      - test-high-e-plateau
      - test-eventcount-mapping
      - test-crossover-band
      - test-hf-first
      - test-ta-gate
    forbidden_proxies_rejected:
      - fp-no-saturation
      - fp-eventcount
      - fp-calib-as-validation
      - fp-crossover-point
      - fp-ta-band
  decisions:
    - summary: "Count-integral estimator adopted (D-estimator): E_rec=C*sum N_obs with a single global per-design C fixed to slope 0.5; plateau IS the modeled saturation."
      phase: "05"
    - summary: "Event-count mapping locked (Pitfall 1): expected_n_qp = INT Gamma_in dt = K*tau_qp*N_qp/V_tr (0.03x N_qp Al / 0.008x Hf), NOT the trapped count."
      phase: "05"
    - summary: "Crossover reported as a band: default ~52.9 eV (Ta->Al) / ~32.1 eV (Al->Hf), equal-split anchor ~13.1/7.9 keV, whole-array plateau ~18.6/11.3 keV; Hf first."
      phase: "05"
    - summary: "Muon-tail E_rec: non_paralyzable plateau ~35 keV (Ta->Al)/~27 keV (Al->Hf); paralyzable rollover ~3.3/~2.6 keV; both >3 orders below the linear line."
      phase: "05"
    - summary: "Ta gap handled as a binary trapping gate (ratio 3.58>=2, T_c gate 2.5 K); response invariant to Delta_abs in alpha-phase; beta-Ta design-invalidating; no film value fabricated."
      phase: "05"
    - summary: "Task 3 checkpoint:human-verify self-assessed satisfied pending orchestrator/researcher review (autonomous run); stop-condition does NOT trigger."
      phase: "05"
  issues:
    - "Saturated-regime response SHAPE has NO literature anchor at any energy — validation is limiting-cases-only; mid-curve is a model prediction."
    - "Analytic censored-integral vs EMG event-train realization diverge O(10-30%) in deep saturation (closed-form renewal vs microphysical dead-window) — unvalidated-shape uncertainty."
    - "Paralyzable-vs-non-paralyzable censoring stays an OPEN switch (CONVENTIONS F); both curves carried, choice not closable from first principles."
  next_actions:
    - "Proceed to Plan 05-02: full Monte-Carlo response matrix R(E_rec|E_dep) per design (both variants) + deliv-fig-response, reusing response.py."
  state_updates:
    record_metric:
      phase: "05"
      plan: "01"
      duration: 2700
      tasks: 3
      files: 4
```
