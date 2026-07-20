# Roadmap: QPD Particle-Physics Potential — Stage-1 Reconstructed-Energy Spectra

## Overview

This stage-1 study computes the reactor-CEvNS, cosmic-ray-muon, and environmental-gamma Compton differential rate spectra in **reconstructed energy** for a 4″×4″×2 mm single-sided Ge wafer (~110 g) read out by Quantum Parity Detectors, for both Ta→Al and Al→Hf trapping designs. The six phases follow the physics dependency backbone: an energy-scale/convention foundation precedes everything; the reactor-flux and muon/Compton deposit tracks are independent and parallelizable; both feed a shared, bandwidth-limited QPD response matrix R(E_rec | E_dep); folding is last. The decisive outputs are spectra on the unified phonon scale in reconstructed energy (never deposited-energy-only), a response curve with an explicit 25 kHz saturation onset, the pipeline code, and an assumptions note.

## Contract Overview

| Contract Item | Advanced By Phase(s) | Status |
| ------------- | -------------------- | ------ |
| claim-cevns (CEvNS spectrum, rate within ~2× of Ge predictions) | Phase 2, Phase 3, Phase 6 | Planned |
| claim-muon (muon spectrum with chord geometry + saturation) | Phase 4, Phase 5, Phase 6 | Planned |
| claim-compton (Compton electron-recoil continuum on phonon scale) | Phase 4, Phase 6 | Planned |
| claim-response (E_rec vs E_dep with 25 kHz saturation) | Phase 1, Phase 5 | Planned |
| obs-cevns-spectrum | Phase 3, Phase 6 | Planned |
| obs-muon-spectrum | Phase 4, Phase 6 | Planned |
| obs-compton-spectrum | Phase 4, Phase 6 | Planned |
| obs-energy-response | Phase 1, Phase 5 | Planned |
| deliv-fig-spectra (all 3 channels, both designs, counts/kg/day/keV) | Phase 6 | Planned |
| deliv-fig-response (saturation onset marked, both designs) | Phase 5 | Planned |
| deliv-code (spectra + response pipeline) | Phase 3, Phase 4, Phase 5, Phase 6 | Planned |
| deliv-note (ASSUMPTIONS.md: efficiency, bandwidth, geometry, gamma-bkg) | Phase 1, Phase 6 | Planned |
| test-cevns-benchmark (Billard Table 1 ~20%, rescaled ~2×) | Phase 3 | Planned |
| test-muon-flux (PDG sea-level flux ~30%) | Phase 4 | Planned |
| test-compton-edges (Klein-Nishina edges; rate ~2×) | Phase 4 | Planned |
| test-response-limits (E_rec≈0.5·E_dep low-E; saturation >25 kHz) | Phase 5 | Planned |
| ref-qpd-paper (must-read; efficiency chain, pulse model, Table II) | Phase 1, Phase 5 | Planned |
| ref-qpd-repo (must-use EMG burst template) | Phase 5 | Planned |
| ref-huber (reactor ν̄ spectrum) | Phase 2, Phase 3 | Planned |
| ref-cevns-benchmark (Billard Ge rates) + CONUS+ baseline | Phase 3 | Planned |
| ref-pdg-muon (sea-level muon flux) | Phase 4 | Planned |
| ref-environmental-gamma (Heusser radiogenic lines/flux) | Phase 4 | Planned |
| **Forbidden proxies:** fp-deposited-only, fp-no-saturation, fp-full-absorption, keVee/keVnr mixing, ionization quenching on phonon scale | Guarded across Phase 1, 4, 5, 6 | — |

## Phases

- [x] **Phase 1: Conventions & Energy-Scale Foundation** — Fix the T→E_ph→E_dep→E_rec bookkeeping (no quenching), CEvNS prefactor/units, and the bandwidth-censoring convention. ✓ verified passed (15/15)
- [ ] **Phase 2: Reactor Flux Model** — Frozen Φ(E_ν) table: Huber–Mueller >2 MeV + summation/n-capture <1.8 MeV with an explicit uncertainty band.
- [ ] **Phase 3: CEvNS Cross Section & Rate** — Per-isotope-summed dR/dT_dep on Ge, benchmarked against Billard Table 1 and the closed-form total cross section.
- [ ] **Phase 4: Muon & Compton Deposited-Energy Spectra** — Muon (Gaisser–Guan ⊗ chord ⊗ Landau–Vavilov) and Compton (Klein–Nishina continuum) deposited-energy spectra, validated against flux anchors.
- [ ] **Phase 5: QPD Response Chain & Energy Reconstruction** — Per-design response matrix R(E_rec | E_dep) spanning linear and saturated regimes; locate the crossover deposit energy.
- [ ] **Phase 6: Fold & Produce Reconstructed-Energy Spectra** — Fold all three deposit spectra through R to deliver the reconstructed-energy figures for both designs.

## Phase Dependencies

| Phase | Depends On | Enables | Critical Path? |
|-------|-----------|---------|:-:|
| 1 — Conventions & Energy-Scale Foundation | — | 2, 4 | Yes |
| 2 — Reactor Flux Model | 1 | 3 | Yes |
| 3 — CEvNS Cross Section & Rate | 2 (1 conventions) | 5 | Yes |
| 4 — Muon & Compton Deposited-Energy Spectra | 1 | 5 | No (parallel with 2, 3) |
| 5 — QPD Response Chain & Energy Reconstruction | 3, 4 | 6 | Yes |
| 6 — Fold & Produce Reconstructed-Energy Spectra | 5 (3, 4) | — | Yes |

**Critical path:** 1 → 2 → 3 → 5 → 6 (5 sequential phases, minimum duration)
**Parallelizable:** Phase 4 (muon + Compton deposit track) runs concurrently with Phases 2 and 3.

**Wave schedule (for `gpd:execute-phase`):**
- Wave 1: Phase 1
- Wave 2: Phase 2, Phase 4 (parallel)
- Wave 3: Phase 3 (after Phase 2; Phase 4 may still be running)
- Wave 4: Phase 5 (after Phases 3 and 4)
- Wave 5: Phase 6

## Risk Register

| Phase | Top Risk | Probability | Impact | Mitigation |
|-------|---------|:-:|:-:|-----------|
| 1 | Censoring rule (paralyzable vs non-paralyzable) unresolvable from electronics reasoning | MEDIUM | HIGH | Record both variants as an explicit switch; flag as open question blocking Phase 5, do not silently pick one |
| 2 | Sub-1.8 MeV flux model choice carries ≳10–20% shape uncertainty | MEDIUM | MEDIUM | Freeze a versioned CSV with a separate below-2-MeV error band; run `gpd:research-phase` to pick the summation dataset |
| 3 | Cross-section unit/convention traps ((ħc)² omission, /4π vs /8π) | MEDIUM | HIGH | Dimensioned unit test against σ(Ge, 4 MeV) ≈ 1.1×10⁻⁴⁰ cm² fixed in Phase 1; backtrack if benchmark off by >20% |
| 4 | Photopeaks instead of Compton continuum; mean vs MPV dE/dx; angular pdf bias | MEDIUM | MEDIUM | Thin-target single-scatter check; Landau/Vavilov (not Moyal) for final; validate Klein-Nishina edge positions and PDG flux |
| 5 | Saturated-regime reconstruction has NO literature anchor at any energy; Ta parameters absent | HIGH | HIGH | Isolate as the risk-bearing phase; validate low-E linearity + high-E plateau in limiting cases only; add Ta params with citation; run `gpd:research-phase` |
| 6 | Deposited-energy-only spectra presented as the deliverable | LOW | HIGH | Deliverable acceptance requires E_rec axis and saturation region delimited; fp-deposited-only guarded |

## Phase Details

### Phase 1: Conventions & Energy-Scale Foundation

**Goal:** The stage-1 bookkeeping is fixed and dimensionally consistent — a single unified phonon energy scale with no ionization quenching, the CEvNS cross-section convention and units, the E_dep→n_qp mapping, and the 50 kHz/25 kHz bandwidth-censoring rule — recorded in `CONVENTIONS.md` and seeded into the assumptions note.
**Depends on:** Nothing (entry point)
**Requirements:** CONV-01
**Contract Coverage:**
- Advances: claim-response (energy-scale + saturation-definition foundation), obs-energy-response (defines its axis)
- Deliverables: `CONVENTIONS.md`; seeds `deliv-note` (`artifacts/stage1/ASSUMPTIONS.md`) with the energy-scale, efficiency, and bandwidth assumptions
- Anchor coverage: ref-qpd-paper (must-read: efficiency chain η_ph/η_pb/η_tr, pulse model Eq. 4, tunneling-rate formulation, Table II device parameters); unified phonon scale with no quenching; benchmark target σ(Ge, 4 MeV) ≈ 1.1×10⁻⁴⁰ cm²
- Forbidden proxies: mixing keVee/keVnr scales; applying ionization (Lindhard) quenching to a fieldless phonon calorimeter (suppresses CEvNS ~5–7×)
**Success Criteria** (what must be TRUE):

1. `CONVENTIONS.md` records the complete T ≡ E_nr → E_ph → E_dep → E_rec chain on a **single unified phonon scale with no ionization quenching** for both nuclear-recoil (CEvNS) and electron-recoil (muon, Compton) deposits, and explicitly forbids any keVee/keVnr mixing.
2. The CEvNS cross-section convention is fixed and dimensionally correct: dσ/dT = (G_F² M/4π) Q_W² (1 − M T/2E_ν²) F²(q²) with the **/4π** prefactor (not /8π), Q_W = N − (1−4 sin²θ_W) Z, sin²θ_W = 0.2387 (low-energy MS-bar), and (ħc)² = 3.894×10⁻²⁸ GeV²·cm²; the dimensioned unit-test target σ(Ge, 4 MeV) ≈ 1.1×10⁻⁴⁰ cm² (coefficient 4.2×10⁻⁴⁵ N²(E_ν/MeV)² cm²) is recorded for Phase 3.
3. The E_dep→n_qp mapping is defined with the ε ≈ 0.5 deposited-to-signal efficiency stated as an imposed forward-model definition carrying a ±10–20% design-dependent variation per design (Ta→Al and Al→Hf do **not** share one efficiency), and the per-kg Ge atom number (8.29×10²⁴ atoms/kg, ρ = 5.323 g/cm³, ~110 g / ~20.6 cm³ wafer, ~10,300 sensors on one face) is fixed.
4. The 50 kHz / 25 kHz bandwidth-censoring convention is written down as an explicit, testable rule (merge vs drop; paralyzable vs non-paralyzable), so that the Phase-5 response matrix has an unambiguous saturation definition; if the rule cannot be fixed physically, both variants are recorded as a switch and flagged as an open question blocking Phase 5.
5. All conventions are dimensionally checked and consistent with ref-qpd-paper efficiency-chain and pulse-model definitions; the unified-scale/no-quenching decision and bandwidth/efficiency assumptions are written into the assumptions note seed.

**Plans:** 2 plans

Plans:

- [x] 01-01-PLAN.md — Parameter foundation (Table II, gaps, constants, sharing defaults) + CEvNS closed-form benchmark hook + CONVENTIONS.md consistency verification
- [x] 01-02-PLAN.md — Energy-scale/response module (yield → Γ_in → both censoring variants switch, E_rec Phase-5 stub) + limiting-case tests + ASSUMPTIONS.md seed

### Phase 2: Reactor Flux Model

**Goal:** A frozen, versioned Φ(E_ν) table is produced — Huber–Mueller above 2 MeV plus a summation + ²³⁸U(n,γ) neutron-capture extension below 1.8 MeV — with explicit above/below-2-MeV uncertainty bands, normalized to 3 GW_th at 25 m (~7–8×10¹² ν̄/cm²/s).
**Objectives:** CALC-01
**Contract Coverage:** advances claim-cevns (flux input) | anchor ref-huber, sub-1.8 MeV region flagged | forbidden proxy: Huber–Mueller truncated/extrapolated at the 1.8 MeV IBD threshold (the sub-IBD flux populates the flagship low-recoil bins)
**Plans:** 0 plans

- [ ] TBD (run plan-phase 2 to break down)

### Phase 3: CEvNS Cross Section & Rate

**Goal:** The per-isotope-summed CEvNS differential rate dR/dT on natural Ge is computed in deposited nuclear-recoil energy (Freedman cross section + Helm form factor, folded with the Phase-2 flux) and validated against the closed-form total cross section and Billard et al. (2017) Table 1.
**Objectives:** CALC-02, VALD-01
**Contract Coverage:** advances claim-cevns, obs-cevns-spectrum (deposited-energy precursor), test-cevns-benchmark, deliv-code | anchors ref-cevns-benchmark (Billard Table 1: 0.76/0.51/0.26 counts/kg/day above 50/100/200 eV_nr), CONUS+ baseline, ref-huber | forbidden proxy: (ħc)² omission, /4π vs /8π, GW_e vs GW_th, lumped A instead of per-isotope endpoints
**Plans:** 0 plans

- [ ] TBD (run plan-phase 3 to break down)

### Phase 4: Muon & Compton Deposited-Energy Spectra

**Goal:** The two background deposit spectra are computed in deposited energy for the thin wafer — the sea-level muon spectrum (Gaisser–Guan angular flux ⊗ chord-length distribution ⊗ Landau–Vavilov straggling) and the environmental-gamma Compton electron-recoil spectrum (representative U/Th + ⁴⁰K radiogenic spectrum × Ge Compton cross section, thin-target single-scatter, Klein–Nishina continuum) — and validated against the PDG muon flux and Klein–Nishina edge positions.
**Objectives:** CALC-03, CALC-04, VALD-02, VALD-03
**Contract Coverage:** advances claim-muon, claim-compton, obs-muon-spectrum, obs-compton-spectrum, test-muon-flux, test-compton-edges, deliv-code (wafer geometry + chord model) | anchors ref-pdg-muon (I_v ≈ 70 m⁻²s⁻¹sr⁻¹, ~1 cm⁻²min⁻¹, Cauchy ⟨ℓ⟩ = 4V/S), ref-environmental-gamma (Heusser lines/flux), Klein–Nishina | forbidden proxies: fp-full-absorption (photopeaks instead of Compton continuum in a thin 2 mm wafer), chord geometry omitted / mean vs MPV dE/dx, angular-pdf bias
**Plans:** 0 plans

- [ ] TBD (run plan-phase 4 to break down)

### Phase 5: QPD Response Chain & Energy Reconstruction

**Goal:** The forward QPD response chain is implemented for both Ta→Al and Al→Hf designs and the Monte-Carlo response matrix R(E_rec | E_dep) is built spanning the linear (CEvNS) and saturated (muon) regimes, with the linear→saturated crossover deposit energy (where peak tunneling rate hits 25 kHz) reported per design and the low-E/high-E limits validated.
**Objectives:** SIMU-01, SIMU-02, VALD-04
**Contract Coverage:** advances claim-response, obs-energy-response, deliv-fig-response (saturation onset marked, both designs), deliv-code, test-response-limits (E_rec ≈ 0.5·E_dep low-E; saturation once tunneling rate > 25 kHz) | anchors ref-qpd-paper (pulse model, efficiency chain, Table II), ref-qpd-repo (must-use EMG burst template) | forbidden proxy: fp-no-saturation (no bandwidth-saturation modeling; linear rate→energy extrapolated across the muon range fakes a peak at the ceiling)
**Risk:** HIGH — the saturated-regime reconstruction has no published result at any energy; Ta superconductor parameters are absent from `materials.yaml`. Run `gpd:research-phase` before planning.
**Plans:** 0 plans

- [ ] TBD (run plan-phase 5 to break down)

### Phase 6: Fold & Produce Reconstructed-Energy Spectra

**Goal:** The CEvNS, muon, and Compton deposit spectra are folded through the response matrix R to deliver the reconstructed-energy differential rate spectra (counts/kg/day/keV) for both trapping designs, with the saturation region delimited and the true→reconstructed mapping plotted, completing the deliverable figures and assumptions note.
**Objectives:** SIMU-03
**Contract Coverage:** advances deliv-fig-spectra (all three channels, both designs, counts/kg/day/keV normalization), deliv-code, deliv-note | anchors — (consumes upstream frozen inputs) | forbidden proxy: fp-deposited-only (reporting spectra in deposited energy only without the reconstruction/bandwidth model — the decisive output is reconstructed energy)
**Plans:** 0 plans

- [ ] TBD (run plan-phase 6 to break down)

## Backtracking Triggers

- **Phase 1:** If the censoring convention (paralyzable vs non-paralyzable) cannot be fixed from electronics reasoning, record both as a switch and flag as an open question that must be resolved before Phase 5 — do not silently choose.
- **Phase 3:** If the computed σ(Ge, 4 MeV) or the Billard Table 1 rates disagree with the Phase-1 benchmark by more than ~20%, halt and revisit the Phase-1 cross-section convention (units, /4π, (ħc)²) before folding.
- **Phase 3 (stop condition):** If the CEvNS reconstructed spectrum ends up entirely below the effective threshold for both designs (surfaced after Phase 5 folding), this is a contract stop-and-rethink condition — report, do not force a spectrum.
- **Phase 4:** If Compton edges do not appear at the Klein–Nishina energies E_edge = 2E_γ²/(m_ec² + 2E_γ), or the integral muon rate is off PDG flux by >30%, debug the geometry/cross-section before proceeding to folding.
- **Phase 4/5 (stop condition):** If muon- or gamma-induced pileup makes quiescent reconstruction impossible at 50 kHz bandwidth, this is a contract stop-and-rethink condition — report the pileup regime explicitly.
- **Phase 5:** If the response chain shows no saturation even when tunneling rates far exceed 25 kHz, the saturation model is wrong — revisit before building the response matrix. If Ta parameters cannot be sourced with citation, block rather than filling from memory.

## Progress

**Execution Order:**
Phases execute by dependency wave: 1 → {2, 4} → 3 → 5 → 6 (Phase 4 parallel with 2–3).

| Phase | Plans Complete | Status | Completed |
| ----- | -------------- | ------ | --------- |
| 1. Conventions & Energy-Scale Foundation | 2/2 | Complete ✓ | 2026-07-20 |
| 2. Reactor Flux Model | 0/TBD | Not started | - |
| 3. CEvNS Cross Section & Rate | 0/TBD | Not started | - |
| 4. Muon & Compton Deposited-Energy Spectra | 0/TBD | Not started | - |
| 5. QPD Response Chain & Energy Reconstruction | 0/TBD | Not started | - |
| 6. Fold & Produce Reconstructed-Energy Spectra | 0/TBD | Not started | - |
