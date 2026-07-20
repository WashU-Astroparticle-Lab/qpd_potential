# Research State

## Project Reference

See: GPD/PROJECT.md

**Machine-readable scoping contract:** `GPD/state.json` field `project_contract`

**Core research question:** Reactor-CEvNS, cosmic-muon, and environmental-gamma Compton spectra in reconstructed energy for a 4"×4"×2mm single-sided Ge wafer read out by QPDs (Ta→Al and Al→Hf designs).
**Current focus:** Phase 1 — Conventions & Energy-Scale Foundation

## Current Position

**Current Phase:** 1
**Current Phase Name:** Conventions & Energy-Scale Foundation
**Total Phases:** 6
**Current Plan:** 01-01
**Total Plans in Phase:** 2
**Status:** Executing
**Last Activity:** Plan 01-01 executed (params + CEvNS benchmark hook)

**Progress:** [██████████] 100%

## Active Calculations

None yet.

## Intermediate Results

None yet.

## Open Questions

- What crystal area is instrumented (one face vs all faces), fixing N_sens from the 1/mm^2 sensor density?
- How should reconstruction behave in the saturated regime: simple Nyquist rate-clip or a dead-time model?
- How should the Ta->Al device tunneling parameters be mapped from the QPD paper's tabulated Al- and Hf-junction devices?
- How should reconstruction behave in the saturated regime: simple Nyquist rate-clip or a dead-time model (paralyzable vs non-paralyzable)?
- What absolute environmental gamma flux and line composition best represent a surface-level reactor-site deployment?

## Performance Metrics

| Label | Duration | Tasks | Files |
| ----- | -------- | ----- | ----- |
| -     | -        | -     | -     |

## Accumulated Context
| Phase 01 P01-01 | 900s | 3 tasks | 8 files |
| Phase 01 P01-02 | 330s | 3 tasks | 4 files |

### Decisions


- [Phase 01-conventions-energy-scale-foundation]: Design->parameter mapping locked in code: Ta->Al uses Table II Aluminum column, Al->Hf uses Hafnium column; absorber supplies only Delta_abs.
- [Phase 01-conventions-energy-scale-foundation]: Hf tau_qp = 400 us adopted (caption/lit) over the 1 ms table cell, flagged MEDIUM.
- [Phase 01-conventions-energy-scale-foundation]: Ta absorber gap encoded as bulk alpha-Ta BCS assumption 0.68 meV (MEDIUM), film phase flagged for Phase 5.
- [Phase 01-conventions-energy-scale-foundation]: Saturation ordering fixed as the plateau Gamma_in Hf/Al ratio (3.17x); the 4.75x N_qp-per-eV ratio is the raw yield, not the saturation driver.
- [Phase 01-conventions-energy-scale-foundation]: Per-design saturation onset energies (~1.27 eV Al / ~0.77 eV Hf) carry the two-exponential peak factor p (0.25 Al / 0.13 Hf); Hf saturates first.
- [Phase 01-conventions-energy-scale-foundation]: E_rec estimator implemented as an explicit Phase-5 stub (NotImplementedError by default; linear_placeholder=True returns 0.5*E_dep, valid only in the unsaturated regime).
- [Phase 01-conventions-energy-scale-foundation]: Both censoring variants exposed as a switch at tau_d=40us; the paralyzable-vs-non-paralyzable choice is preserved OPEN as a Phase-5 blocker, not silently chosen.

### Active Approximations

None yet.

**Convention Lock:**

- Metric signature: not_applicable — no relativistic field theory in this detector/rate pipeline
- Fourier convention: not_applicable
- Natural units: internal-only (hbar=c=1) for CEvNS cross section; k_B EXPLICIT (not =1); I/O in eV/keV/MeV, counts/kg/day/keV, s, cm/um; (hbar c)^2 = 3.894e-28 GeV^2 cm^2
- Gauge choice: not_applicable
- Regularization scheme: not_applicable
- Renormalization scheme: tree-level SM (no loops); only scheme-dependent input is sin2thetaW = 0.2387 (low-energy MS-bar)
- Coordinate system: Cartesian wafer frame: x,y in-plane 4in x 4in face, z through 2mm thickness; sensors on one z-face
- Spin basis: not_applicable
- State normalization: not_applicable
- Coupling convention: CEvNS dsigma/dT = (G_F^2 M/4pi) Q_W^2 (1 - M T/2 E_nu^2) F^2(q^2); prefactor /4pi NOT /8pi; Q_W = N-(1-4 sin2thetaW)Z; sin2thetaW=0.2387 (low-E MSbar); 1-4sin2thetaW=0.0452; Helm F, F(0)=1
- Index positioning: not_applicable
- Time ordering: not_applicable
- Commutation convention: not_applicable
- Levi-Civita sign: not_applicable
- Generator normalization: not_applicable
- Covariant derivative sign: not_applicable
- Gamma matrix convention: not_applicable
- Creation/annihilation order: not_applicable

*Custom conventions:*
- Energy Scale Chain: single unified phonon scale, NO ionization quenching, for BOTH NR (CEvNS) and ER (muon/Compton): T=E_nr -> E_ph -> E_dep -> E_rec; E_ph=E_dep-E_stored(defects) (few-% NR-only, 0 for muons/Compton); E_rec(low-E)~=0.5*E_dep; FORBIDDEN: keVee/keVnr mixing, Lindhard/ionization quenching
- Detector Normalization: Ge 8.29e24 atoms/kg, rho=5.323 g/cm^3, M=72.63 g/mol; wafer 4inx4inx2mm=20.65 cm^3~=110 g, ~10300 sensors 1/mm^2 one face; reactor 3 GW_th (thermal) at 25 m => ~7-8e12 nubar/cm^2/s; adopt 110 g geometry but KEEP per-kg (counts/kg/day) normalization; '1 kg' framing in SUMMARY.md is STALE
- Efficiency Mapping: eps~=0.5 deposited-to-signal, imposed forward-model definition, SAME baseline both designs with +/-10-20% design-dependent band; Ta->Al and Al->Hf may split to per-design numbers in Phase 5; paper physical estimate eta_ce~=0.3 is an independent cross-reference, NOT baseline
- Bandwidth Censoring: LOCKED resolving time: 25 kHz max resolvable tunneling rate => 40 us (Nyquist from 50 kHz bw); 20 us at 50 kHz sampling itself (state both); paralyzable-vs-non-paralyzable AND merge-vs-drop kept as EXPLICIT CODE SWITCH (not fixed); OPEN QUESTION BLOCKS Phase 5; both variants must be implementable
- Cevns Benchmark Target: Phase-3 unit test: FULL Q_W => sigma(Ge,4 MeV)~=1.0e-40 cm^2 (canonical); N-only quick-check ~1.1e-40 cm^2 (1.08e-40, ~20% tol); coefficient sigma~=4.22e-45 N^2 (E_nu/MeV)^2 cm^2; closed form sigma_tot=G_F^2 Q_W^2 E_nu^2/4pi; PITFALLS.md ~1e-42 value is WRONG (100x)

### Propagated Uncertainties

None yet.

### Pending Todos

None yet.

### Blockers/Concerns

None

## Session Continuity

**Last session:** none
**Stopped at:** none
**Resume file:** none
**Last result ID:** none
**Hostname:** none
**Platform:** none
