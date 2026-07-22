# Requirements: QPD Particle-Physics Potential — v1.1 Neutron & Radiogenic Backgrounds

**Defined:** 2026-07-21
**Core Research Question:** What is the in-band (CEvNS-band) background budget in reconstructed energy — from neutron-induced nuclear recoils and detector-material radioactivity — for the ~110 g QPD Ge wafer (Ta→Al and Al→Hf designs), and how does it compare against the v1.0 reactor-CEvNS signal?

> **Milestone scope note.** v1.1 extends the v1.0 forward-model/response chain to the in-band background suite. All spectra are produced in reconstructed energy on the **unified phonon scale (no ionization quenching)** and folded through the existing `R(E_rec|E_dep)` matrices (both designs, non-paralyzable 25 kHz). Analytic/Monte-Carlo only; **no G4CMP**. The three external normalization inputs (surface ambient-neutron flux; housing/materials U/Th/⁴⁰K radiopurity budget; Ge surface-exposure/cool-down history) are handled by **representative cited defaults with an explicit uncertainty band** (the v1.0 environmental-gamma pattern), fixed and documented in Phase 7. IDs continue from the v1.0 milestone (last used: CALC-04, SIMU-03, VALD-04, CONV-01).

## Primary Requirements

Requirements for the v1.1 in-band background budget. Each maps to exactly one roadmap phase (7–12).

### Calculations

- [ ] **CALC-05**: Assemble the incident fast-neutron flux φ(E_n) for all three sources — ambient cosmogenic sea-level (Gordon-2004), local muon-induced (driven by the v1.0 Gaisser–Guan muon population × local wafer+housing production, explicitly guarded against double-counting the v1.0 muon deposits), and radiogenic (α,n)+²³⁸U spontaneous fission — each provenance-tagged and keV_nr-axis-tagged, on the shared energy grid.
- [ ] **CALC-06**: Compute the neutron-induced Ge nuclear-recoil deposited-energy spectrum dR/dE_dep via the isotropic-CM flat-box recoil-kernel single-scatter fold (dσ/dT = σ_el/T_max, T_max = 4A/(1+A)²·E_n = 0.0536·E_n for natural Ge, abundance-weighted; per-isotope exact 0.0555/0.0540/0.0533/0.0526/0.0513 for Ge-70/72/73/74/76) over ENDF/B-VIII.0 n-Ge elastic cross sections, on the unified phonon scale (no quenching), for the thin 2 mm wafer.
- [ ] **CALC-07**: Compute the detector-material radiogenic **electron-recoil** spectrum dR/dE_dep — Ge-crystal-bulk + housing/nearby-component U/Th/⁴⁰K gammas as a Compton continuum (reuse v1.0 Klein–Nishina machinery) with self-shielding and solid-angle/attenuation, plus intrinsic β/EC full-energy deposits — for the assumed representative radiopurity budget.
- [ ] **CALC-08**: Compute the radiogenic **neutron** nuclear-recoil contribution from (α,n) reactions and ²³⁸U spontaneous fission for the assumed material assay, folded through the CALC-06 recoil kernel.
- [ ] **CALC-09**: Build the cosmogenic-activation isotope inventory A(t) (³H, ⁶⁸Ge/⁶⁸Ga, ⁶⁵Zn, ⁶⁰Co, ⁵⁷Co, …) for the assumed Ge surface-exposure/cool-down scenario and produce the in-band electron-recoil templates (³H β-continuum to the 18.6 keV endpoint; EC K/L X-ray lines).
- [ ] **CALC-10**: Fold every background channel through the v1.0 R(E_rec|E_dep) response (both trapping designs, non-paralyzable 25 kHz) to reconstructed energy and assemble the combined in-band background budget, compared against the v1.0 reactor-CEvNS signal in the flagship reconstructed-energy band.

### Simulations

- [ ] **SIMU-04**: Cross-check the thin-target single-scatter approximation with a bespoke single-scatter/escape Monte-Carlo (or analytic multiple-scatter estimate) for 2 mm Ge: quantify the multi-scatter and escape fractions and the >1 MeV a₁ forward-peaking (File-4 Legendre) tail correction to the flat-box kernel.

### Validations

- [ ] **VALD-05**: Neutron recoil kinematics — reproduce the maximum recoil fraction T_max/E_n = 4A/(1+A)² per contributing isotope (exact: 0.0555/0.0540/0.0533/0.0526/0.0513 for Ge-70/72/73/74/76), giving abundance-weighted natural Ge = 0.0536 as computed. (Corrected 2026-07-22 from a stale 0.0538 label, which matches neither the mass-number form 0.0536 nor the AWR mass-ratio form 0.0541.)
- [ ] **VALD-06**: Interaction consistency — fast-neutron interaction probability in 2 mm Ge ~3–4% (λ ~ 5–6 cm, Σ ~ 0.18 cm⁻¹ = 1/(N_Ge σ_tot)); count-conservation preserved through the recoil fold and the response fold.
- [ ] **VALD-07**: Source-term normalization anchors — Gordon-2004 >10 MeV sea-level flux 3.5×10⁻³ cm⁻²s⁻¹; ²³⁸U spontaneous-fission yield 1.353×10⁻¹¹ n/g/s per ppb U; ³H cosmogenic production 74–82 atoms/kg/day — reproduced within stated tolerances.
- [ ] **VALD-08**: Peer-experiment in-band cross-check — modeled 10–100 eV in-band nuclear-recoil rate compared against the NUCLEUS ~250 dru shielded lower bound; the unshielded surface result must exceed it (consistency direction, not equality).

## Follow-up Requirements

Deferred to future milestones. Tracked but not in the v1.1 roadmap.

### Manuscript / Payoff

- **MANU-01**: Manuscript revision per the round-1 internal peer review (completeness scope caveat, ε vs η_ce distinction, citations, venue).
- **SENS-01**: Quantitative CEvNS discovery/exclusion sensitivity (signal vs. summed in-band backgrounds) — enabled by the v1.1 background budget.

### Extended Backgrounds

- **RADX-01**: QPD-film / substrate / wafer-surface radioactivity (Ta/Al/Hf films, surface contamination) — deferred this milestone.
- **NCAP-01**: Reactor-correlated thermal/epithermal neutron-capture NR at 25 m unshielded (reactor on/off separable, unlike ambient) — flagged MEDIUM in the survey.
- **LEEX-01**: Low-Energy Excess below ~100 eV — the modeled in-band floor is a lower bound only.

## Out of Scope

| Topic | Reason |
| ------- | -------------------------------------------------------------------------------- |
| G4CMP phonon-transport detector response | Deferred project-wide; thin wafer is optically thin, analytic single-scatter suffices |
| Dark-matter sensitivity projections | Later milestone of this project |
| QPD-film/surface radioactivity | Explicitly deselected for v1.1 (Ge-bulk + housing only) |
| Imperfect tunneling identification / readout-noise | Idealized readout retained from v1.0 stage-1 assumptions |
| Ionization quenching / Lindhard / keVee↔keVnr conversion | Unified phonon scale (CONVENTIONS §B); neutron NR deposits full recoil energy as phonons |
| Full Geant4/FLUKA/MCNP shower simulation | Too heavy for a rough estimate; parametrized flux/yield + analytic transport instead |
| Detector geometry / sensor-layout optimization | Fixed 4″×4″×2 mm single-sided wafer from v1.0 |

## Accuracy and Validation Criteria

| Requirement | Accuracy Target | Validation Method |
| ----------- | ------------------------------ | ------------------------------------------- |
| CALC-05 | Flux normalizations to cited-source precision; each source axis- and provenance-tagged | VALD-07 anchor reproduction; double-count guard vs. v1.0 muon channel |
| CALC-06 | Endpoint T_max exact per isotope; count-conservation ≤1e-3 through the fold | VALD-05, VALD-06; limiting cases |
| CALC-07 | Compton edges exact; self-shielding/solid-angle to ~factor-2 (representative assay) | Reuse v1.0 KN edge validation; energy-closure check |
| CALC-08 | (α,n)+SF yield within cited spread (20–50%); folded on the validated CALC-06 kernel | VALD-07 (SF yield); material-yield provenance |
| CALC-09 | Isotope activities within cited production-rate errors; ³H endpoint 18.6 keV exact | VALD-07 (³H rate); exposure-scenario documented |
| CALC-10 | Count-conservation through the response fold ≤1e-3 per channel per design | Mirror v1.0 fold-closure tests; both designs |
| SIMU-04 | Multi-scatter & escape fractions with MC statistical error < a few % | Consistency with the analytic ~3–4% interaction estimate (VALD-06) |
| VALD-08 | Order-of-magnitude / direction consistency (unshielded > shielded lower bound) | Comparison to NUCLEUS ~250 dru |

## Contract Coverage

| Requirement | Decisive Output / Deliverable | Anchor / Benchmark / Reference | Prior Inputs / Baselines | False Progress To Reject |
| ----------- | ----------------------------- | ------------------------------ | ------------------------ | ------------------------ |
| CALC-05 | Provenance-tagged φ(E_n) tables (3 sources) | Gordon 2004; Wang/Mei–Hime; SOURCES4/Watt | v1.0 Gaisser–Guan muon flux; shared grid | Muon-induced neutrons re-counting the v1.0 muon deposit; untagged keVee flux |
| CALC-06 | Neutron dR/dE_dep on the phonon scale | ENDF/B-VIII.0 n-Ge elastic; two-body kinematics | v1.0 shared_energy_grid, CONVENTIONS §B | Applying Lindhard/QF; deposited spectrum in keVnr-vs-keVee mix |
| CALC-07 | Radiogenic ER dR/dE_dep (Ge-bulk + housing) | Heusser 1995; ENSDF/DDEP; NIST XCOM | v1.0 Klein–Nishina Compton machinery | Full-energy photopeaks instead of Compton continuum (thin wafer) |
| CALC-08 | Radiogenic neutron NR dR/dE_dep | Mei-Zhang-Hime SF yield; (α,n) yield tables | CALC-06 recoil kernel | Generic (α,n) yield ignoring material light-element content |
| CALC-09 | Cosmogenic ER templates + A(t) inventory | CDMSlite/EDELWEISS production rates; ENSDF | Ge exposure/cool-down assumption | Quoting saturation activity as as-deployed activity |
| CALC-10 | Combined in-band dR/dE_rec vs. CEvNS (both designs) | v1.0 CEvNS signal; NUCLEUS in-band | v1.0 R(E_rec|E_dep) matrices | Deposited-energy-only spectra; skipping the 25 kHz saturation |
| VALD-08 | In-band budget vs. peer comparison note | NUCLEUS arXiv:2509.03559 (~250 dru) | v1.0 flagship CEvNS band | Claiming agreement where only a lower-bound direction is testable |

## Traceability

Phase mapping **finalized by the roadmapper** (2026-07-21); phases continue from v1.0's phase 6. See `GPD/ROADMAP.md` for phase detail, success criteria, dependency DAG, and risk register.

| Requirement | Phase | Status |
| ----------- | -------------------- | ------- |
| CALC-05 | Phase 8: Neutron Source Terms | Pending |
| CALC-06 | Phase 9: Neutron Transport & Recoil Fold | Pending |
| SIMU-04 | Phase 9: Neutron Transport & Recoil Fold | Pending |
| VALD-05 | Phase 9: Neutron Transport & Recoil Fold | Pending |
| VALD-06 | Phase 9: Neutron Transport & Recoil Fold | Pending |
| CALC-07 | Phase 10: Detector Radioactivity Budget | Pending |
| CALC-08 | Phase 10: Detector Radioactivity Budget | Pending |
| CALC-09 | Phase 11: Cosmogenic Activation Inventory | Pending |
| VALD-07 | Phase 11: Cosmogenic Activation Inventory | Pending |
| CALC-10 | Phase 12: Response Fold & Combined In-Band Budget | Pending |
| VALD-08 | Phase 12: Response Fold & Combined In-Band Budget | Pending |

> Phase 7 (Scenario & Nuclear-Data Lock) is a prerequisite setup phase: it fixes the three representative gating inputs (+ band) and acquires the ENDF/B-VIII.0 n-Ge elastic data. It carries no standalone CALC/SIMU/VALD requirement but gates CALC-05/06/07/08/09.

**Coverage:**

- Primary requirements: 11 total
- Mapped to phases: 11
- Unmapped: 0

---

_Requirements defined: 2026-07-21_
_Last updated: 2026-07-21 after v1.1 roadmap finalization (Phases 7–12; mapping locked by the roadmapper)_
