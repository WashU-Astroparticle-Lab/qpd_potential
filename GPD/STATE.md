# Research State

## Project Reference

See: GPD/PROJECT.md (updated 2026-07-20)

**Machine-readable scoping contract:** `GPD/state.json` field `project_contract`

**Core research question:** What are the reactor-CEvNS, cosmic-ray-muon, and environmental-gamma Compton differential rate spectra in reconstructed energy for a 4″×4″×2 mm single-sided Ge wafer read out by QPDs with Ta→Al and Al→Hf trapping designs, given the stated efficiency and bandwidth assumptions?
**Current focus:** Phase 1 — Conventions & Energy-Scale Foundation

## Current Position

**Current Phase:** 1
**Current Phase Name:** Conventions & Energy-Scale Foundation
**Total Phases:** 6
**Current Plan:** 1
**Total Plans in Phase:** TBD
**Status:** Ready to plan
**Last Activity:** 2026-07-20
**Last Activity Description:** Roadmap created (shallow mode): Phase 1 fully detailed, Phases 2–6 stubbed; 12/12 requirements mapped, all contract items surfaced.

**Progress:** [░░░░░░░░░░] 0%

## Active Calculations

None yet — Phase 1 not yet planned.

## Intermediate Results

None yet.

## Open Questions

- [Contract] How should reconstruction behave in the saturated regime: simple Nyquist rate-clip or a dead-time model (paralyzable vs non-paralyzable)? (blocks Phase 5; convention must be fixed in Phase 1)
- [Contract] How should the Ta→Al device tunneling parameters be mapped from the QPD paper's tabulated Al- and Hf-junction devices? (blocks Phase 5)
- [Contract] What absolute environmental gamma flux and line composition best represent a surface-level reactor-site deployment? (feeds Phase 4)
- [Setup] What crystal area is instrumented (one face vs all faces), fixing N_sens from the 1/mm² sensor density? (contract: single instrumented face, ~10,300 sensors — confirm in Phase 1)

## Performance Metrics

| Label | Duration | Tasks | Files |
| ----- | -------- | ----- | ----- |
| -     | -        | -     | -     |

## Accumulated Context

### Decisions

Full log: `GPD/DECISIONS.md`

**Recent high-impact:**
- [Scoping]: Interpret the two designs as Ta→Al and Al→Hf (absorber→trap); trapping requires Δ_trap < Δ_absorber. Confirmed by user.
- [Scoping]: 3 GW_th commercial reactor at 25 m; sea-level muon flux with no overburden; 4″×4″×2 mm single-sided wafer (~110 g). Confirmed by user.
- [Scoping]: Added environmental-gamma Compton channel (representative radiogenic background). Confirmed by user.

### Active Approximations

| Approximation | Validity Range | Controlling Parameter | Current Value | Status |
| ------------- | -------------- | --------------------- | ------------- | ------ |
| Unified phonon scale, no ionization quenching | fieldless phonon calorimeter | — | — | To be locked in Phase 1 |
| ε ≈ 0.5 deposited-to-signal efficiency (imposed) | forward-model definition, per design | ε | 0.5 (±10–20%) | To be locked in Phase 1 |
| Freedman SM CEvNS cross section + Helm form factor | E_ν ≲ 50 MeV, reactor recoils | q = √(2MT) | F² > 0.998 | Planned (Phase 3) |
| Huber–Mueller flux >2 MeV; summation + n-capture <1.8 MeV | data-anchored >2 MeV; model-only <1.8 MeV | E_ν | — | Planned (Phase 2) |
| Landau/Vavilov straggling (not Moyal for final) | κ-regime dependent | κ | — | Planned (Phase 4) |
| Bandwidth censoring at 50 kHz / 25 kHz Nyquist | peak tunneling rate | Γ_peak | 25 kHz cap | To be defined in Phase 1, applied in Phase 5 |

**Convention Lock:**

- Natural units: internal cross section ħ=c=1, (ħc)² = 3.894×10⁻²⁸ GeV²·cm² (to be locked Phase 1)
- Coupling convention: dσ/dT = (G_F² M/4π) Q_W² (1−MT/2E_ν²) F²; Q_W = N−(1−4 sin²θ_W)Z; sin²θ_W = 0.2387 (low-E MS-bar) (to be locked Phase 1)
- Unit system: detector practical units (eV/keV/MeV, cm, s, counts/kg/day/keV) for I/O
- Energy scale: unified phonon scale, no ionization quenching (to be locked Phase 1)

### Propagated Uncertainties

| Quantity | Current Value | Uncertainty | Last Updated (Phase) | Method |
| -------- | ------------- | ----------- | -------------------- | ------ |
| -        | -             | -           | -                    | -      |

### Pending Todos

None yet.

### Blockers/Concerns

- [Phase 5, HIGH risk] QPD saturated-regime reconstruction has no literature anchor at any energy; Ta superconductor parameters (Δ, DOS, T_c) absent from `materials.yaml` — must be added with citation. Run `gpd:research-phase` before planning Phase 5.
- [Phase 2] Sub-1.8 MeV reactor flux is never-measured; needs a summation-dataset decision and a separate ≳10–20% uncertainty band.
- [Phase 1] Censoring convention (merge vs drop; paralyzable vs non-paralyzable) must be fixed before the Phase-5 response matrix is built.

## Session Continuity

**Last session:** 2026-07-20
**Stopped at:** Roadmap created; awaiting Phase 1 planning
**Resume file:** GPD/ROADMAP.md
**Last result ID:** none
**Hostname:** —
**Platform:** darwin
