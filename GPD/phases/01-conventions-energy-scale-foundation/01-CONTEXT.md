# Phase 1: Conventions & Energy-Scale Foundation - Context

**Gathered:** 2026-07-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Fix the stage-1 bookkeeping so every downstream phase shares one consistent foundation: the unified T ≡ E_nr → E_ph → E_dep → E_rec energy chain (no ionization quenching), the CEvNS cross-section convention and units, the E_dep→n_qp yield mapping, the per-sensor energy-sharing model, and the 50 kHz/25 kHz bandwidth-censoring rule — recorded in `CONVENTIONS.md` (already written and locked) and seeded into the assumptions note. This phase clarifies the *modeling choices* the earlier convention lock left open; it does not compute any spectrum.

Requirements: CONV-01

**Note:** The canonical convention lock (unified no-quenching phonon scale, CEvNS `/4π` + Q_W + (ħc)² units, σ(Ge,4 MeV) benchmark target, ε≈0.5, 40 µs resolving time, censoring-as-switch, detector normalization) was established during project init and lives in `GPD/CONVENTIONS.md` and `GPD/state.json`. This CONTEXT.md records the *additional* modeling decisions made in discussion that those locks did not yet fix.

</domain>

<contract_coverage>
## Contract Coverage

- **claim-response (foundation):** the energy-scale chain and the saturation *definition* (per-sensor peak Γ_in vs 25 kHz) are fixed so Phase 5 has an unambiguous response model. Success = definitions consistent and dimensionally correct.
- **obs-energy-response (axis):** Phase 1 defines the E_rec axis and the meaning of saturation onset.
- **deliv-note seed:** `artifacts/stage1/ASSUMPTIONS.md` seeded with energy-scale, sharing, yield, defect, efficiency, and bandwidth assumptions.
- **Acceptance signal:** conventions dimensionally checked against ref-qpd-paper; the per-sensor energy model makes saturation *physically possible* (not assumed away).
- **False progress to reject:** any keVee/keVnr mixing; applying Lindhard/ionization quenching to the phonon scale; an energy-sharing model in which nothing can ever saturate (would trivially void the muon-response physics).

</contract_coverage>

<user_guidance>
## User Guidance To Preserve

- **User-stated observables:** CEvNS, muon, and Compton spectra in **reconstructed** energy (never deposited-only); the E_rec(E_dep) response with saturation onset marked.
- **User-stated deliverables:** rough stage-1 spectra (figures) + pipeline code + assumptions note.
- **Must-have references / prior outputs:** QPD paper (Ramanathan et al. 2026, DOI 10.1103/kqd2-spb1); the `qpd` repo EMG burst template.
- **Stop / rethink conditions:** CEvNS reconstructed spectrum entirely below effective threshold for both designs; muon/gamma pileup makes quiescent reconstruction impossible at 50 kHz.

</user_guidance>

<decisions>
## Methodological Decisions

### Per-sensor energy sharing (A)

- **Model: localized-near-hit + diffuse tail.** A prompt fraction of a deposit's energy is absorbed near the impact point (a small spot of sensors, position-dependent); the remainder spreads diffusely across the wafer. This is chosen over the paper's global equal-split because equal-split among ~10,300 sensors would make per-sensor deposits so small that essentially nothing saturates — voiding the muon-response physics the study is meant to expose.
- **Muon channel: same model as point deposits.** A muon's total E_dep is collapsed to a point and passed through the same localized+diffuse sharing (the ~cm track is *not* spread along a line in stage 1).
- **Localization scale: parametrized, researcher picks defaults.** Expose a prompt fraction `f_prompt` and a spot radius `r` (in sensors) with literature-motivated defaults; keep them scannable so stage 1 stays honest about this unknown.

### E_dep → n_qp yield mapping (B)

- **Lumped linear yield: N_qp = ε · E_sensor / Δ_tr**, where E_sensor is the sensor's share of the deposit (from the A model), ε ≈ 0.5 is the imposed deposited-to-signal efficiency (absorbing phonon collection, pair-breaking, trapping, and the Δ_abs/Δ_tr multiplication), and **the quantum is the trap gap Δ_tr** (Al ~180 µeV, Hf ~20–40 µeV).
- **Consequence (intended):** Hf traps yield ~5–10× more quasiparticles per eV than Al, so the two designs differ genuinely in both sensitivity and saturation onset — this asymmetry is a physical result, not a bug.
- **Tunneling rate:** Γ_in = K · n_qp with n_qp = N_qp/V_tr, using Table II K and V_tr per design (researcher's discretion, following the paper). Peak Γ_in vs 25 kHz defines saturation.

### Sub-dominant corrections (C)

- **Frenkel-defect energy storage set to zero** for stage 1: E_ph = E_dep for all three channels. Recorded as a documented few-% NR-only (CEvNS) systematic to revisit later. Keeps the unified scale exact.

### Reconstruction & censoring (D)

- **E_rec estimator: deferred to Phase 5.** Phase 1 fixes only the E_rec axis and the saturation *definition*; the choice of estimator (count-integral vs time-over-saturation vs hybrid auto-switch) is a Phase-5 research decision.
- **Default censoring variant: non-paralyzable** (fixed 40 µs dead window, arrivals during it dropped, window not extended) for headline plots. The paralyzable variant and the merge-vs-drop alternative remain available via the explicit code switch (locked in CONVENTIONS.md); resolving the physical variant remains an open question blocking Phase 5's final numbers.

### Agent's Discretion

- Localization defaults (`f_prompt`, `r`) — researcher chooses literature-motivated values.
- Γ_in = K·n_qp parameters (K, V_tr per design) — follow Table II of the paper.
- E_rec estimator definition — Phase 5.

</decisions>

<assumptions>
## Physical Assumptions

- **Localized+diffuse sharing:** Justified because a 2 mm wafer's athermal phonons are absorbed with position dependence before full homogenization | If phonons truly homogenize (equal-split limit), per-sensor saturation vanishes and the muon spectrum loses its compression feature — the whole response story changes.
- **Muon track collapsed to a point:** Simplifies stage 1 | This *overstates* per-sensor saturation for muons — a real ~cm track spreads its deposit over a line of sensors, lowering the peak per-sensor rate. Conservative (saturation-heavy) for a rough estimate; flagged for refinement.
- **Lumped ε absorbs the whole efficiency chain:** Matches the stated ~50% spec | If the true chain is strongly design- or energy-dependent, one ε with a ±10–20% band misrepresents the design gap; Phase 5 may split it.
- **Trap-gap quantum (N_qp ∝ 1/Δ_tr):** Standard trapping physics | If the effective quantum is nearer Δ_abs, the Hf advantage shrinks and both designs look more alike.
- **Defect storage = 0:** Few-% NR-only | Negligible for a rough estimate; only matters at the lowest CEvNS recoil bins.

</assumptions>

<limiting_cases>
## Expected Limiting Behaviors

- **Low deposited energy (per sensor):** peak Γ_in ≪ 25 kHz ⇒ no censoring ⇒ E_rec ≈ 0.5·E_dep (linear, unsaturated). Must hold for CEvNS and most Compton events.
- **High deposited energy (per sensor):** peak Γ_in > 25 kHz ⇒ censoring active ⇒ E_rec compresses / saturates. Must appear for the muon channel.
- **Equal-split limit (f_prompt → 0):** if all energy diffuses evenly, per-sensor rates fall below 25 kHz for almost all events ⇒ saturation should nearly disappear. A useful sanity knob: turning off localization should remove the muon compression feature.
- **Hf vs Al:** for the same E_sensor, Hf's smaller Δ_tr gives ~5–10× higher N_qp and Γ_in ⇒ Hf saturates at a lower deposited energy than Al. The crossover-energy ordering (E_cross^Hf < E_cross^Al) must come out of Phase 5.

</limiting_cases>

<anchor_registry>
## Active Anchor Registry

- **ref-qpd-paper** (Ramanathan et al. 2026, DOI 10.1103/kqd2-spb1)
  - Why it matters: efficiency chain, pulse model Eq. (4), Γ_in = K·n_qp, Table II (K, V_tr, Δ) — the source for the yield and tunneling-rate mapping
  - Carry forward: planning, execution, verification
  - Required action: read, use, cite
- **ref-qpd-repo** (`qpd/src/qpd/simulator/quasiparticle_bursts.py`)
  - Why it matters: EMG burst template that realizes the per-event tunneling time profile feeding the censoring model
  - Carry forward: execution (Phase 5)
  - Required action: read, use
- **GPD/CONVENTIONS.md** (this project)
  - Why it matters: the locked canonical conventions this CONTEXT extends; must stay consistent
  - Carry forward: planning, execution, verification
  - Required action: use

</anchor_registry>

<skeptical_review>
## Skeptical Review

- **Weakest anchor:** the localized+diffuse sharing model has no direct thin-wafer measurement behind it; `f_prompt` and `r` are the least-constrained numbers in the whole pipeline, and the muon spectrum shape depends strongly on them.
- **Unvalidated assumptions:** collapsing the muon track to a point (overstates saturation); lumped ε applying equally to both designs; trap-gap quantum; Table II K/V_tr transferring to this wafer.
- **Competing explanation:** an apparent muon "saturation feature" could be an artifact of the point-collapse + localization choice rather than real readout physics — the equal-split sanity limit must be checked to distinguish them.
- **Disconfirming check:** if turning localization off (equal-split limit) still shows strong saturation, or if turning it on shows none at plausible `f_prompt`, the sharing model is mis-specified.
- **False progress to reject:** a clean-looking muon compression feature that is actually driven entirely by the arbitrary point-collapse; reconstructed spectra shown before the low-E linearity limit (E_rec ≈ 0.5·E_dep) is verified.

</skeptical_review>

<deferred>
## Deferred Ideas

- **Along-track (line) muon energy sharing** instead of point-collapse — a fidelity upgrade for the muon channel; revisit in Phase 4/5 if the point-collapse conservatism dominates the result.
- **Per-design efficiency split** (distinct ε for Ta→Al vs Al→Hf) — Phase 5, if the tunneling-parameter mapping warrants.
- **Localization-scale sensitivity scan** (`f_prompt`, `r`) as a systematic study — future work once the baseline pipeline exists.
- **Full position-dependent phonon-collection model** — belongs to a later G4CMP-based stage (explicitly out of scope now).

None of these expand Phase 1 scope; captured so they are not lost.

---

_Phase: 01-conventions-energy-scale-foundation_
_Context gathered: 2026-07-20_
