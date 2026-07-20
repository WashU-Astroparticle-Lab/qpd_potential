# Research Summary

**Project:** QPD Particle-Physics Potential — Reactor-CEvNS + Cosmic-Muon Reconstructed-Energy Spectra in a 1 kg Ge Crystal
**Domain:** Reactor CEvNS, sea-level cosmic-ray muons, superconducting quasiparticle (parity) sensors
**Researched:** 2026-07-20
**Confidence:** HIGH overall (physics inputs are textbook/benchmark-grade; the QPD saturation/reconstruction model is the one genuinely open MEDIUM element)

## Executive Summary

This project computes two differential rate spectra — reactor CEvNS and sea-level cosmic muons — in **reconstructed** energy for a 1 kg monolithic Ge crystal read out by Quantum Parity Detectors (QPDs), for two absorber→trap designs (Ta→Al, Al→Hf). The four research files are unusually coherent: the underlying physics of every stage (CEvNS cross section, reactor flux, muon flux/energy loss, quasiparticle dynamics) is established and benchmarked, and the entire calculation runs on a laptop in pure Python. The scientific novelty is *not* new physics inputs but the **forward response chain**: mapping deposited energy through a bandwidth-limited (50 kHz / ~25 kHz max resolvable rate) tunneling-count readout into reconstructed energy, where a hard readout saturation nonlinearly compresses the multi-MeV muon end of the spectrum.

The recommended path is a two-track forward model sharing one response matrix R(E_rec | E_dep). **CEvNS track:** deterministic flux-folded rate (Freedman SM cross section + Helm form factor, summed over the five Ge isotopes) → linear QPD pulse model → count-based energy estimator. This is entirely analytic except a final censoring MC and is directly benchmarkable against Billard et al. (2017) Table 1 and the CONUS+ first observation. **Muon track:** a small custom Monte Carlo (modified Gaisser–Guan flux → chord sampling → Landau/Vavilov straggling) → *nonlinear* Rothwarf–Taylor quasiparticle dynamics → time-over-saturation ("time-over-threshold"-analog) estimator. The muon reconstructed spectrum will be logarithmically compressed and is the project's central deliverable and its least-anchored piece.

The dominant risks are all pitfalls of energy bookkeeping and convention, not of computing power. In priority order: (1) **do not apply ionization quenching** — a pure phonon calorimeter measures the full recoil energy, so CEvNS (nuclear recoil) and muon (electron recoil) deposits land on the *same* phonon scale; importing Lindhard suppresses the CEvNS rate ~5–7×. (2) The reactor flux **below the 1.8 MeV IBD threshold** is never-measured and populates exactly the lowest reconstructed-energy bins QPDs are built for — it must be modeled by summation + neutron-capture components with a ≳10–20% band, not truncated. (3) The **saturation model** for the muon end is genuinely unspecified in the literature and must be built and validated in limiting cases, not extrapolated linearly. A cross-check of the CEvNS normalization caught a 100× error in one file's benchmark value (see Contradictions), underscoring that dimensioned unit tests against σ ≈ 4.2×10⁻⁴⁵ N²(E_ν/MeV)² cm² are mandatory early.

## Unified Notation

Convention choice: **detector/particle-physics practical units** for all inputs/outputs (energies in eV/keV/MeV, rates in counts kg⁻¹ day⁻¹ keV⁻¹, times in s, lengths in cm); **natural units** (ħ = c = 1) internally for the cross section, converted with (ħc)² = 3.894×10⁻²⁸ GeV² cm² (equivalently 1 GeV⁻² = 3.894×10⁻²⁸ cm²). No metric-signature or Fourier issues arise (no relativistic field theory in the pipeline). This table is binding for downstream work.

| Symbol | Quantity | Units/Dimensions | Convention notes (reconciled across files) |
| --- | --- | --- | --- |
| T ≡ E_nr | Nuclear-recoil kinetic energy | keV_nr / eV_nr | METHODS uses `T`; PRIOR-WORK/PITFALLS use E_R/E_nr. Unified: **T = E_nr**. Never map to keVee without an explicit quenching model. |
| E_dep | Deposited energy in crystal | MeV (muons), keV/eV (CEvNS) | Full recoil/ionization energy delivered to the lattice. |
| E_ph | Phonon energy | same as E_dep | E_ph = T − E_stored(defects); defect storage is a few-% NR-only correction, zero for muons. |
| E_rec | Reconstructed energy | eV/keV/MeV | Output of the QPD estimator; the project's observable axis. Low-energy limit E_rec ≈ 0.5·E_dep. |
| dσ/dT | CEvNS differential cross section | cm²/keV | (G_F²M/4π)Q_W²(1 − MT/2E_ν²)F²(q²). **Prefactor is /4π, not /8π** (Pitfall 3). |
| Q_W | Weak nuclear charge | dimensionless | Q_W = N − (1 − 4sin²θ_W)Z; proton coupling ~vanishes, so rate ∝ N² to ~0.5%. |
| sin²θ_W | Weak mixing angle | dimensionless | **Low-energy value 0.2387 (0.23857, MS-bar), not 0.2312 (M_Z).** State scheme when comparing to precision fits. |
| F(q²) | Helm nuclear form factor | dimensionless | q = √(2MT); F(0)=1, F² > 0.998 at reactor q for Ge (form-factor-independent regime). |
| Φ(E_ν) | Reactor ν̄ flux | ν̄ cm⁻² s⁻¹ MeV⁻¹ | From per-fission spectra (ν̄ fission⁻¹ MeV⁻¹) × fission rate × 1/(4πL²). |
| dI/dE_μ dΩ | Muon differential flux | cm⁻² s⁻¹ sr⁻¹ GeV⁻¹ | Gaisser–Guan (arXiv:1509.06176); track sr explicitly. I_v ≈ 70 m⁻²s⁻¹sr⁻¹. |
| ⟨dE/dx⟩ | Muon stopping power in Ge | 1.370 MeV cm² g⁻¹ (≈7.3 MeV/cm) | Use straggling distribution, not the mean, for the deposit spectrum. |
| ℓ | Chord length through crystal | cm | Cauchy ⟨ℓ⟩ = 4V/S under isotropic flux (unit-test invariant). |
| n_qp, Γ_in | QP density; tunneling rate per sensor | µm⁻³; Hz | Γ_in ≈ K·n_qp, K ≈ 16 E_J k_B T/(𝒩Δh) (Ramanathan Eq.-level). |
| τ_inj, τ_qp | QP injection / recombination times | s (µs–ms) | Two-exponential pulse (paper Eq. 4); τ_qp density-dependent at muon scale. |
| Δ_abs, Δ_tr | Absorber / trap superconducting gaps | µeV | Ta≈700, Al≈180, Hf≈20–60; trapping needs Δ_abs/Δ_tr ≳ 2–4. Treat film gaps as parameters. |
| ε, η | Deposit→signal efficiency | dimensionless | Project baseline ε ≈ 0.5 (imposed); anchor paper physical estimate η_ce ≈ 0.3 — see Contradictions. |
| τ_d, Δt | Readout dead/resolving time | 20 µs (=1/50 kHz) | Saturation ceiling; invertible to ~25 kHz. |

## Key Findings

### Computational Approaches (from COMPUTATIONAL.md — HIGH)

Pure Python (numpy/scipy/matplotlib) on a laptop; no HPC, Geant4, or G4CMP. The rate calculations are 1–2D integrals; the muon generator is an analytic-formula sampler; the readout chain is a vectorizable point-process MC. Heaviest step (the response matrix) is minutes.

**Core approach:**
- **Reuse the local `qpd` repo readout chain nearly verbatim** — `quasiparticle_bursts.py` (`QuasiparticleBurstModel`, EMG bursts: N~Poisson, offsets = Normal(µ,σ)+Exp(τ)) is exactly the EMG point-process generator; `expected_n_qp` is the energy-deposit hook. Import the submodule path (numpy-only), not the top-level package (pulls qutip).
- **Write CEvNS fresh (~150 lines), validate against `wimprates` (Helm FF to float precision) and `bradkav/CEvNS`** (SM rate benchmark with its CHOOZ flux). Copy formulas rather than importing (wimprates uses global `numericalunits` state).
- **Reimplement Gaisser–Guan muon flux as a ~50-line numpy rejection sampler**; do not wrap EcoMug/CRY/CORSIKA.
- **Fold via a response matrix R(E_rec | E_true)** built by importance-sampling uniformly in E_true — this decouples MC cost from the steeply falling physical spectra (direct event-by-event MC of O(1–100) counts/kg/day CEvNS is statistically useless).

### Prior Work Landscape (from PRIOR-WORK.md — HIGH)

**Must reproduce (benchmarks):**
- **Billard et al. (2017) Table 1 (Ge, phonon energy scale, no quenching):** 0.76 / 0.51 / 0.26 counts kg⁻¹ day⁻¹ above 50 / 100 / 200 eV_nr at 8.54 GW_th, 400 m. This is the *same energy variable* a QPD measures — the primary numerical anchor. Rescaled to this project (3 GW_th, 25 m; ×~90 flux) ≈ 68 / 46 / 23 counts kg⁻¹ day⁻¹ (DERIVED, MEDIUM — recompute in-project).
- **CONUS+ first observation (2025):** 395 ± 106 events, 3.7σ, 119 d, 3.73 kg HPGe, 160–180 eV_ee, 3.6 GW_th at 20.7 m → ≈1 count kg⁻¹ day⁻¹ above 160 eV_ee (ionization scale, needs a quenching model to compare). Closest existing configuration; **independently verified via Nature s41586-025-09322-2.**
- **PDG muon anchors:** vertical intensity I_v ≈ 70 m⁻²s⁻¹sr⁻¹ (>1 GeV/c), horizontal-surface flux ≈ 1 muon cm⁻²min⁻¹, mean E_μ ≈ 4 GeV; through a 1 kg Ge cube ≈ 0.5–1 Hz. **Independently verified via PDG cosmic-ray review.**
- **Ge stopping power:** ⟨dE/dx⟩_min = 1.370 MeV cm² g⁻¹ (7.3 MeV/cm) → ~40 MeV for a vertical 5.7 cm chord (mean-chord deposits ~25–30 MeV — see Contradictions), Landau-distributed with MPV below mean.
- **Max Ge recoil:** E_R^max ≈ 1.9 keV_nr at E_ν = 8 MeV (per-isotope endpoints 1.81–1.96 keV_nr).

**Novel predictions (this project's contribution):**
- CEvNS and muon spectra **in reconstructed energy** for a QPD-instrumented kg-scale Ge crystal, including 50 kHz bandwidth saturation — the first step toward CEvNS/dark-matter sensitivity for QPD arrays. Phonon readout sidesteps the contested Ge ionization-quenching controversy (Dresden-II) entirely.

**Defer (future / out of scope):** dark-matter sensitivity (later milestone), G4CMP phonon transport, non-muon backgrounds (neutron-induced recoils flagged as the dominant real CEvNS background but explicitly out of scope), imperfect tunneling ID.

### Methods and Tools (from METHODS.md — HIGH, verified against primary sources)

1. **CEvNS rate — deterministic quadrature:** Freedman dσ/dT + Helm FF, per-isotope sum, flux folded with `scipy.integrate.quad` on a log grid anchored at E_ν,min(T)=√(MT/2). Validate against closed-form σ_tot = G_F²Q_W²E_ν²/4π.
2. **Reactor flux — hybrid:** Huber–Mueller for 2–8 MeV (±5% normalization systematic; optional KI rescaling); **summation model below 1.8 MeV** (Estienne–Fallot / CONFLUX / arXiv:2302.10460) plus ²³⁸U(n,γ) neutron-capture ν̄.
3. **Muon deposits — small custom MC:** Gaisser–Guan flux (parameters P₁–P₅ verified against arXiv:1509.06176) → analytic ray-box chord → **Landau/Vavilov** MPV + straggling (`pylandau` / true Landau; **not Moyal for the final result**).
4. **QPD chain — analytic ODE per event:** Ramanathan two-exponential pulse (Eq. 4) with linear model for CEvNS; **Rothwarf–Taylor nonlinear (bimolecular) decay for muon-scale deposits** (~10¹¹ QPs system-wide). Efficiency chain η_ph≈0.65 × η_pb≈0.4–0.6 × η_tr≈0.4–0.7 ≈ 0.32.
5. **Reconstruction — point-process + censoring:** inhomogeneous Poisson tunneling with EMG jitter; bandwidth saturation as an **explicit MC event-merging step** (derive paralyzable vs non-paralyzable from electronics, don't assume); count-based estimator (linear/CEvNS) and time-over-saturation logarithmic estimator (nonlinear/muon).

### Critical Pitfalls (top 5 of 12 from PITFALLS.md)

1. **Ionization quenching applied to a phonon scale (Pitfall 6, CRITICAL).** No ionization channel, no Luke gain → full recoil thermalizes to phonons. Applying Lindhard suppresses CEvNS ~5–7×. CEvNS (NR) and muons (ER) share one phonon scale; never mix keVee/keVnr. *Recovery cost MEDIUM (all spectra invalid).*
2. **Reactor spectrum truncated/extrapolated at the 1.8 MeV IBD threshold (Pitfall 1, CRITICAL).** ~60–70% of ν̄ are sub-threshold and never measured; they dominate the lowest recoil bins (sub-IBD flux populates all T ≲ 96 eV). Use summation + neutron-capture with ≳10–20% band.
3. **Saturation/aliasing of the tunneling-rate estimator at the muon end (Pitfall 10, CRITICAL).** Linear rate→energy extrapolated 7 orders of magnitude produces a fake "peak" at the ceiling. Build an explicit saturating per-sensor response (EMG amplitude × occupancy/dead-time × 25 kHz cap); validate low-E linearity and high-E plateau. *Recovery cost HIGH.*
4. **Cross-section convention + unit traps (Pitfalls 2,3).** /4π vs /8π (×4), dropping (ħc)² (the single most common CEvNS bug), GW_e vs GW_th (×3), double-counting ~6 ν̄/fission. Fix conventions first; dimensioned unit tests against σ ≈ 4.2×10⁻⁴⁵ N²(E_ν/MeV)² cm².
5. **Correlated QP-poisoning treated as independent per-sensor noise (Pitfall 9).** Muons/γ produce crystal-wide phonon bursts elevating many sensors at once (Wilen et al. 2021) — the muon "signal" and the poisoning "background" are the *same events*. Use one shared event generator; multi-sensor coincidence is both the discriminator and what makes the muon spectrum measurable.

Also material: constant-η assumption (Pitfall 8; Ta→Al and Al→Hf do **not** share one efficiency — different gaps → different phonon acceptance), Frenkel-defect storage (Pitfall 7; 0–15% NR-only band at 20 eV–2 keV), muon angular bookkeeping (Pitfall 11; sampling pdf ∝ cos²θ·cosθ·sinθ, silent ~30% bias), per-isotope endpoints (Pitfall 4; no lumped A=72.63).

## Approximation Landscape

| Method | Valid regime | Breaks down when | Controlled? | Complements |
| --- | --- | --- | --- | --- |
| Freedman SM cross section (truncated kinematic factor) | E_ν ≲ 50 MeV (reactor) | O(T/E_ν)~10⁻³ terms matter at high precision | Yes — known subleading terms | Full kinematic form |
| Helm form factor / F=1 | q ≲ 16 MeV (reactor Ge), F²>0.998 | q ≳ 20–50 MeV (COHERENT) | Yes — Lewin–Smith params | Klein–Nystrand (COHERENT) |
| Huber–Mueller flux | E_ν ≳ 2 MeV | E_ν < 1.8 MeV (undefined); ~5% anomaly; 5 MeV bump | Partly (±5% + bump systematic) | Summation model below 2 MeV |
| Summation flux (sub-IBD) | E_ν < 2 MeV | ≳10–20% shape uncertainty; imperfect power correlation | No — model, not data | Never-measured; the coverage gap |
| Gaisser–Guan muon flux | all zenith, E_μ ≳ 1 GeV | E_μ < 1 GeV (extrapolation; small rate fraction) | Partly | Data-driven (Front. Energy Res. 9) |
| Landau/Vavilov straggling | κ-regime dependent (Landau κ≲0.01) | Moyal underestimates tail; mean ≫ MPV | Yes (κ selects Landau/Vavilov/Gaussian) | Geant4 (δ-ray escape) |
| Linear QPD pulse model | peak Γ ≲ 25 kHz (CEvNS scale) | muon deposits (n_qp high, recombination nonlinear) | Yes → RT ODEs | Rothwarf–Taylor bimolecular |
| Time-over-saturation estimator | peak Γ ≫ 25 kHz (muon) | crossover region near Γ ≈ 25 kHz | Weakly (log estimator, τ_qp-limited) | Count-based estimator |

**Coverage gaps (prime targets for in-project computation):** (a) the **sub-1.8 MeV reactor flux** has no data-anchored model — it is where the QPD gains rate and where the honest error band is widest; (b) **QPD energy reconstruction in the saturated regime** has *no published result at any energy*, let alone multi-MeV — the crossover E_dep (where peak Γ crosses 25 kHz) is a key design number to compute early; (c) the **crossover region itself** (CEvNS-to-muon dynamic range) needs the most careful joint treatment.

## Theoretical Connections

- **Shared readout physics of muon "signal" and poisoning "background" (Established).** Radiation-induced correlated charge-parity/phonon bursts across qubit chips (Wilen et al., Nature 594, 369 (2021)) are empirically the *same* channel QPDs read out — so the muon spectrum and the QP-poisoning background are one event generator seen through two bookkeeping paths. This is a physics constraint, not a modeling convenience.
- **Time-over-saturation ≡ time-over-threshold reconstruction (Established analogy).** Above the rate cap, energy information survives in the *duration* of saturation (t_sat ≈ τ_qp ln(Γ_peak/Γ_thr)) — the same logarithmic estimator used in saturated TES/SNSPD/PMT channels. Transfers resolution-scaling intuition (√N_sensors) directly.
- **One phonon energy scale unifies NR and ER deposits (Established).** Because a fieldless phonon calorimeter has no quenching, CEvNS nuclear recoils and muon electron recoils are directly comparable on the same axis — the cross-validation lever that lets the muon band and the CEvNS band be produced by one response matrix.
- **Rothwarf–Taylor bottleneck ↔ dead-time saturation (Established, two compounding nonlinearities).** At high n_qp the signal is sublinear *twice*: bimolecular QP recombination (τ_qp ∝ 1/n_qp) *and* the 25 kHz readout cap. The muon estimator must compose both, not treat saturation as purely electronic.
- **Cross-validation opportunity (Conjectured for this geometry):** the `qpd` repo I/Q-waveform chain (out of scope) could independently sanity-check the 50 kHz bandwidth limit against the count-level model if ever wanted.

### Cross-Validation Matrix

|  | Deterministic CEvNS | Muon MC | Analytical limit | Experiment |
| --- | :---: | :---: | :---: | :---: |
| **Deterministic CEvNS** | — | shared response matrix R(E_rec\|E_dep) | σ_tot = G_F²Q_W²E_ν²/4π; F(0)=1 | Billard 2017 Table 1 (phonon scale); CONUS+ (via quenching) |
| **Muon MC** | shared R + shared burst generator | — | Cauchy ⟨ℓ⟩=4V/S; PDG MPV Δ_p | PDG I_v≈70, ~1 cm⁻²min⁻¹; ~0.5–1 Hz rate |
| **QPD response** | count-based estimator (linear) | time-over-sat (nonlinear) | linear-model limit n₀→0; RT bimolecular n(t)=n₀/(1+R̃n₀t) | **none — high-E saturation unmeasured (highest-risk cell)** |

**High-risk:** the QPD saturated-response row has **no experimental cross-check** — validation is limited to internal limiting-case tests. This is the phase to treat with most care.

## Implications for Research Plan

Dependency backbone: a conventions/energy-scale foundation must precede everything; reactor-flux and muon-flux tracks are independent and parallelizable; both feed a shared QPD response matrix; folding is last.

### Phase 1: Conventions & Energy-Scale Definition
**Rationale:** Pitfalls 3, 6, 10 and every convention trap are cheapest to prevent by writing down the bookkeeping first. **Delivers:** `CONVENTIONS.md` fixing the T→E_ph→E_dep→E_rec chain (no quenching), /4π prefactor, sin²θ_W=0.2387, (ħc)² conversion, GW_th, per-kg constant 8.29×10²⁴ Ge atoms, and the **censoring convention** (merge vs drop; paralyzable vs non-paralyzable). **Avoids:** 3, 6, 8, 10. **Established procedure — low risk.**

### Phase 2: Reactor Flux Model  *(parallel with Phase 3)*
**Rationale:** Sub-IBD flux dominates the flagship low-E bins and is the widest systematic. **Delivers:** frozen versioned CSV Φ(E_ν) = Huber–Mueller (>2 MeV) + summation (<2 MeV) + ²³⁸U(n,γ), with above/below-2-MeV uncertainty bands. **Uses:** METHODS Domain-1 flux recipe. **Avoids:** 1, 2. **Needs research** (which summation dataset — CONFLUX vs published table) — MEDIUM risk.

### Phase 3: CEvNS Cross Section & Rate  *(parallel with Phase 2, needs its output to fold)*
**Rationale:** Analytic, cheap, and the most benchmarkable piece — establish it early as the pipeline's anchor. **Delivers:** dR/dT_true per isotope, summed, on a log grid. **Validates:** closed-form σ_tot to <0.1%; F(0)=1; Billard Table 1 under its assumptions before rescaling; σ(Ge,4 MeV)≈1.1×10⁻⁴⁰ cm². **Avoids:** 3, 4, 5. **Established — low risk** (dimensioned unit tests mandatory).

### Phase 4: Muon Flux + Geometry + Straggling MC  *(parallel with Phases 2–3)*
**Rationale:** Independent input track; produces dR/dE_dep for muons. **Delivers:** Gaisser–Guan sampler + ray-box chords + Landau/Vavilov deposits. **Validates:** I_v≈70 m⁻²s⁻¹sr⁻¹, ~1 cm⁻²min⁻¹, Cauchy ⟨ℓ⟩=4V/S, ~0.5–1 Hz crystal rate, MPV vs PDG Δ_p. **Avoids:** 11, 12. **Mostly established — low-medium risk** (angular pdf and Landau-vs-Moyal are the traps).

### Phase 5: QPD Response Chain & Energy Reconstruction
**Rationale:** The scientific core and highest-risk step — bandwidth saturation and nonlinear QP dynamics. **Delivers:** response matrix R(E_rec|E_dep) per design (Ta→Al, Al→Hf) spanning both regimes; the crossover E_dep. **Uses:** `qpd` repo burst model + fresh thinning/censoring; linear pulse (CEvNS) + Rothwarf–Taylor (muon) + time-over-saturation estimator. **Builds on:** Phase 1 scale, Phases 3–4 deposit spectra. **Avoids:** 8, 9, 10. **Needs research + genuinely open** (Ta superconductor parameters missing from `materials.yaml`; no literature anchor for high-E saturation) — **HIGH risk.**

### Phase 6: Fold & Produce Reconstructed-Energy Spectra
**Rationale:** Combine everything; the deliverable. **Delivers:** dR/dE_rec for CEvNS and muons, per design, with the saturation region delimited and the true→reconstructed mapping plotted alongside. **Builds on:** Phases 3, 4, 5. **Established once inputs exist — low risk.**

### Phase Ordering Rationale
- Conventions first because energy-scale errors (quenching, /8π, ħc²) are cheap to prevent and expensive to unwind (Pitfall recovery: MEDIUM–HIGH).
- Flux and muon tracks parallelize (no shared dependency until folding); CEvNS rate should be stood up early as the benchmarkable backbone.
- The QPD response (Phase 5) is deliberately isolated as the risk-bearing phase so its open questions don't block the well-established input phases.

### Phases Requiring Deep Investigation
- **Phase 5 (QPD saturation/reconstruction):** no published result at any energy; the saturation model, Ta parameters, and crossover energy are new computation. Run `gpd:research-phase`.
- **Phase 2 (sub-IBD flux):** model choice with ≳10–20% consequence; needs a decision on the summation dataset. Run `gpd:research-phase`.
- **Phases 1, 3, 4, 6:** established procedures with textbook/benchmark validation — straightforward execution.

## Contradictions Found and Resolved

1. **σ(Ge, 4 MeV) benchmark — 100× discrepancy (RESOLVED, important).** METHODS validation states σ ≈ 10⁻⁴⁰ cm²; PITFALLS Pitfall-3 warning sign states "~10⁻⁴² cm² ballpark." First-principles calculation (σ = (G_F²/4π)Q_W²E_ν² = 4.2×10⁻⁴⁵ N²(E_ν/MeV)² cm² → **1.08×10⁻⁴⁰ cm²** for Ge, N=40, 4 MeV) confirms **METHODS is correct; PITFALLS is off by ~100×.** This matters because it is a *validation target* — using 10⁻⁴² would "validate" a code that is 100× too low. Downstream: use σ(Ge,4 MeV) ≈ 1.1×10⁻⁴⁰ cm² and the coefficient form as the Phase-3 unit test.
2. **Straggling sampler — Moyal vs Landau/Vavilov (RESOLVED).** COMPUTATIONAL recommends `scipy.stats.moyal`; METHODS explicitly warns "Moyal underestimates the Landau high-energy tail — use true Landau/Vavilov"; PITFALLS concurs (sample Landau/Vavilov). Resolution (2-of-3 agreement + physics: the high tail sets the saturation morphology): **use true Landau/Vavilov (`pylandau`) for the final muon spectrum; Moyal only for quick sanity checks.**
3. **Efficiency ε ≈ 0.5 vs η_ce ≈ 0.3 (RESOLVED — definitional, not a conflict).** ε ≈ 0.5 is a project-imposed forward-model definition; the anchor paper's η_ce ≈ 0.3 (f_loss~0.35) is the physical estimate, and Ta→Al vs Al→Hf do not share one value. Use ε = 0.5 as baseline but carry a position/energy-dependent variation (±10–20%) as a resolution/energy-scale systematic, per design.
4. **Typical muon deposit ~40 MeV vs ~25–30 MeV (RESOLVED — chord definition).** ~40 MeV is the *vertical* 5.7 cm chord; ~25–30 MeV uses the angular *mean* chord (~3.8 cm). Both correct; the observable is the full chord+Landau distribution, not a single number.

No contradictions require user judgment; all resolved by convention/physics.

## Confidence Assessment

| Area | Confidence | Notes |
| --- | --- | --- |
| Computational Approaches | HIGH | Laptop-scale, local repos inspected directly, clear validation oracles (wimprates, bradkav/CEvNS). |
| Prior Work | HIGH | Benchmarks (Billard, CONUS+, PDG) are peer-reviewed; three of four independently re-verified this session. Derived rescalings MEDIUM. |
| Methods | HIGH | Core formulas verified against primary sources (Ramanathan, Guan) or first-principles; QPD saturation reconstruction MEDIUM. |
| Pitfalls | HIGH | Comprehensive 12-pitfall map with recovery costs; one benchmark value in it was wrong (caught and corrected above). |

**Overall confidence:** HIGH for inputs and pipeline; MEDIUM for the muon reconstructed-energy morphology (the one genuinely open modeling element).

### Gaps to Address
- **Sub-1.8 MeV reactor flux:** never measured; pick a summation dataset and carry a separate ≳10–20% band (Phase 2).
- **QPD saturated-regime reconstruction:** no literature anchor at any energy; build and validate in limiting cases only (Phase 5).
- **Tantalum superconductor parameters** (Δ, DOS, T_c) missing from `materials.yaml` — add with citation, not from memory (Phase 5).
- **Neutron-induced nuclear recoils** mimic CEvNS exactly and are the dominant real reactor background — out of scope, but must be stated prominently in any sensitivity claim.
- **Censoring convention** (merge vs drop; paralyzable vs non-paralyzable) must be fixed in Phase 1 before the response matrix is built.

## Sources

### Primary (HIGH)
- Ramanathan et al., APS Open Sci. 1, 000013 (2026), DOI 10.1103/kqd2-spb1 / arXiv:2405.17192 — QPD concept, pulse model Eq. 4, efficiency chain, K ≈ 16 E_J k_B T/(𝒩Δh). *Verified (existence/content).*
- Billard et al., J. Phys. G 44, 105101 (2017), arXiv:1612.09035 — Ge phonon-scale CEvNS benchmark Table 1. *Read directly by researcher; snippet paywalled.*
- Ackermann et al. (CONUS+), Nature 643, 1229 (2025), arXiv:2501.05206 — first reactor CEvNS observation. *Verified via Nature s41586-025-09322-2.*
- PDG Review — Cosmic Rays (I_v≈70, ~1 cm⁻²min⁻¹) and Atomic/Nuclear Properties (Ge dE/dx 1.370 MeV cm²/g). *Verified.*
- Guan et al., arXiv:1509.06176 — modified Gaisser flux. *Verified (params fetched by researcher).*
- Huber, PRC 84, 024617 (2011); Mueller et al., PRC 83, 054615 (2011) — reactor ν̄ spectra.
- Freedman, PRD 9, 1389 (1974) — SM CEvNS cross section.
- Local `qpd` and `wimprates` repos — inspected directly (COMPUTATIONAL.md).

### Secondary (MEDIUM)
- Liao, Liu, Marfatia, PRD 108, 033002 (2023), arXiv:2302.10460 — sub-IBD flux with CEvNS.
- Kopeikin et al., PRD 104, L071301 (2021) — KI ²³⁵U/²³⁹Pu re-measurement.
- Rothwarf & Taylor, PRL 19, 27 (1967); Kaplan et al., PRB 14, 4854 (1976); Kozorezov et al., PRB 61, 11807 (2000) — QP/phonon dynamics.
- Wilen et al., Nature 594, 369 (2021) — correlated radiation-induced QP bursts in qubits.
- Aristizabal Sierra et al., JHEP 06 (2019) 141, arXiv:1902.07398 — form-factor irrelevance at reactor q.
- bradkav/CEvNS (arXiv:1805.01798); CONFLUX (arXiv:2503.18966) — validation/flux tools.

### Tertiary (LOW / to verify at phase time)
- Sandoval et al., arXiv:2509.18637 — QPD device characteristics (Ta params still absent).
- SuperCDMS defect-loss arXiv:1805.09942; arXiv:2210.01550 — Frenkel-defect storage band.
- Colaresi et al., PRL 129, 211802 (2022) — Dresden-II (contested; not used for signal model).
- Ma et al., PRC 88, 014605; Lewin & Smith Helm params — background-knowledge constants.

---

_Research analysis completed: 2026-07-20_
_Ready for research plan: yes_

```yaml
# --- ROADMAP INPUT (machine-readable, consumed by gpd-roadmapper) ---
synthesis_meta:
  project_title: "QPD Particle-Physics Potential — Reactor-CEvNS + Cosmic-Muon Reconstructed-Energy Spectra in a 1 kg Ge Crystal"
  synthesis_date: "2026-07-20"
  input_files: [METHODS.md, PRIOR-WORK.md, COMPUTATIONAL.md, PITFALLS.md]
  input_quality: {METHODS: good, PRIOR-WORK: good, COMPUTATIONAL: good, PITFALLS: good}

conventions:
  unit_system: "mixed: detector practical units (eV/keV/MeV, cm, s, counts/kg/day) for I/O; natural units internally for cross section"
  coupling_convention: "dsigma/dT = (G_F^2 M/4pi) Q_W^2 (1 - M T/2 E_nu^2) F^2; Q_W = N-(1-4 sin2thetaW)Z; sin2thetaW=0.2387 (low-E MSbar); (hbar c)^2 = 3.894e-28 GeV^2 cm^2"
  renormalization_scheme: "N/A (tree-level SM); low-energy sin2thetaW"

methods_ranked:
  - name: "Deterministic flux-folded CEvNS rate (Freedman + Helm, per-isotope sum)"
    regime: "E_nu <~ 50 MeV; reactor recoils T <~ 2 keV_nr; form-factor-independent"
    confidence: HIGH
    cost: "O(n_Enu) per recoil point; <1 min total, laptop"
    complements: "QPD response MC (adds reconstructed-energy axis)"
  - name: "QPD response chain (Ramanathan linear pulse + Rothwarf-Taylor nonlinear + bandwidth censoring)"
    regime: "linear for peak Gamma <~ 25 kHz (CEvNS); nonlinear/saturated for muon deposits"
    confidence: MEDIUM
    cost: "O(N_samples x <N_qp>); minutes per design; switch to analytic counting stats when <N_qp> >~1e6"
    complements: "reuse of local qpd repo EMG burst generator"
  - name: "Muon flux+geometry+straggling MC (Gaisser-Guan + chord + Landau/Vavilov)"
    regime: "all zenith, E_mu >~ 1 GeV; cm-scale Ge (Landau/Vavilov regime)"
    confidence: HIGH
    cost: "~1-10 s for 1e6 muons, vectorized numpy"
    complements: "multi-sensor coincidence; shared burst generator with background model"
  - name: "Hybrid reactor flux (Huber-Mueller >2 MeV + summation + n-capture <2 MeV)"
    regime: ">2 MeV data-anchored (HIGH); <1.8 MeV model-only (MEDIUM)"
    confidence: MEDIUM
    cost: "one-off table generation; frozen CSV"
    complements: "sub-IBD band is the widest low-recoil systematic"

phase_suggestions:
  - name: "Conventions & Energy-Scale Definition"
    goal: "Fix the T->E_ph->E_dep->E_rec bookkeeping (no quenching), CEvNS prefactor/units, and the readout censoring convention."
    methods: []
    depends_on: []
    needs_research: false
    risk: LOW
    pitfalls: ["pitfall-3", "pitfall-6", "pitfall-8", "pitfall-10"]
  - name: "Reactor Flux Model"
    goal: "Produce a frozen Phi(E_nu) table with a data-anchored region above 2 MeV and a summation+n-capture extension below with an explicit uncertainty band."
    methods: ["Hybrid reactor flux (Huber-Mueller >2 MeV + summation + n-capture <2 MeV)"]
    depends_on: ["Conventions & Energy-Scale Definition"]
    needs_research: true
    risk: MEDIUM
    pitfalls: ["pitfall-1", "pitfall-2"]
  - name: "CEvNS Cross Section & Rate"
    goal: "Compute per-isotope-summed dR/dT_true and validate against Billard Table 1 and the closed-form total cross section."
    methods: ["Deterministic flux-folded CEvNS rate (Freedman + Helm, per-isotope sum)"]
    depends_on: ["Conventions & Energy-Scale Definition", "Reactor Flux Model"]
    needs_research: false
    risk: LOW
    pitfalls: ["pitfall-3", "pitfall-4", "pitfall-5"]
  - name: "Muon Flux + Geometry + Straggling MC"
    goal: "Produce dR/dE_dep for sea-level muons through the crystal, validated against PDG flux anchors and the Cauchy chord invariant."
    methods: ["Muon flux+geometry+straggling MC (Gaisser-Guan + chord + Landau/Vavilov)"]
    depends_on: ["Conventions & Energy-Scale Definition"]
    needs_research: false
    risk: MEDIUM
    pitfalls: ["pitfall-11", "pitfall-12"]
  - name: "QPD Response Chain & Energy Reconstruction"
    goal: "Build the per-design response matrix R(E_rec|E_dep) spanning linear (CEvNS) and saturated (muon) regimes and locate the crossover deposit energy."
    methods: ["QPD response chain (Ramanathan linear pulse + Rothwarf-Taylor nonlinear + bandwidth censoring)"]
    depends_on: ["Conventions & Energy-Scale Definition", "CEvNS Cross Section & Rate", "Muon Flux + Geometry + Straggling MC"]
    needs_research: true
    risk: HIGH
    pitfalls: ["pitfall-8", "pitfall-9", "pitfall-10"]
  - name: "Fold & Produce Reconstructed-Energy Spectra"
    goal: "Fold source spectra through the response matrix to deliver dR/dE_rec for CEvNS and muons per design with the saturation region delimited."
    methods: ["Deterministic flux-folded CEvNS rate (Freedman + Helm, per-isotope sum)", "QPD response chain (Ramanathan linear pulse + Rothwarf-Taylor nonlinear + bandwidth censoring)"]
    depends_on: ["CEvNS Cross Section & Rate", "Muon Flux + Geometry + Straggling MC", "QPD Response Chain & Energy Reconstruction"]
    needs_research: false
    risk: LOW
    pitfalls: ["pitfall-10"]

critical_benchmarks:
  - quantity: "Ge CEvNS rate above 50/100/200 eV_nr (phonon scale, 8.54 GW_th, 400 m)"
    value: "0.76 / 0.51 / 0.26 counts kg^-1 day^-1"
    source: "Billard et al., J. Phys. G 44, 105101 (2017), Table 1"
    confidence: HIGH
  - quantity: "Ge CEvNS rate rescaled to this project (3 GW_th, 25 m)"
    value: "~68 / 46 / 23 counts kg^-1 day^-1 above 50/100/200 eV_nr (factor ~2 target)"
    source: "DERIVED from Billard Table 1 (x~90 flux)"
    confidence: MEDIUM
  - quantity: "CEvNS total cross section on Ge at E_nu = 4 MeV"
    value: "~1.1e-40 cm^2 (coefficient 4.2e-45 N^2 (E_nu/MeV)^2 cm^2)"
    source: "First-principles (this synthesis); confirms METHODS.md, corrects PITFALLS.md 100x error"
    confidence: HIGH
  - quantity: "CONUS+ first reactor CEvNS observation"
    value: "395 +/- 106 events, 3.7 sigma, 119 d, 3.73 kg, 160-180 eV_ee (~1 count kg^-1 day^-1)"
    source: "Ackermann et al. (CONUS+), Nature 643, 1229 (2025)"
    confidence: HIGH
  - quantity: "Sea-level vertical muon intensity"
    value: "I_v ~ 70 m^-2 s^-1 sr^-1 (>1 GeV/c); ~1 muon cm^-2 min^-1 horizontal (10-15% lower recent)"
    source: "PDG Cosmic Rays review"
    confidence: HIGH
  - quantity: "Muon rate through 1 kg Ge crystal"
    value: "~0.5-1 Hz"
    source: "DERIVED from PDG flux + crystal geometry"
    confidence: MEDIUM
  - quantity: "Muon stopping power / typical deposit in Ge"
    value: "1.370 MeV cm^2 g^-1 (7.3 MeV/cm); ~40 MeV vertical chord / ~25-30 MeV mean chord, Landau MPV < mean"
    source: "PDG Atomic & Nuclear Properties (Ge)"
    confidence: HIGH
  - quantity: "Max Ge nuclear recoil at E_nu = 8 MeV"
    value: "E_R^max ~ 1.9 keV_nr (per-isotope 1.81-1.96 keV_nr)"
    source: "kinematics (standard)"
    confidence: HIGH
  - quantity: "Reactor flux at detector (3 GW_th, 25 m)"
    value: "~7-8e12 nu-bar cm^-2 s^-1"
    source: "DERIVED (consistent with CONUS+ scaling)"
    confidence: MEDIUM

open_questions:
  - question: "What is the QPD energy reconstruction (and its resolution) in the saturated regime for multi-MeV muon deposits? No published result at any energy."
    priority: HIGH
    blocks_phase: "QPD Response Chain & Energy Reconstruction"
  - question: "Which summation dataset models the never-measured sub-1.8 MeV reactor flux, and what uncertainty band does it carry?"
    priority: HIGH
    blocks_phase: "Reactor Flux Model"
  - question: "What are the tantalum superconductor parameters (Delta, DOS, T_c) for the Ta->Al design, absent from materials.yaml?"
    priority: MEDIUM
    blocks_phase: "QPD Response Chain & Energy Reconstruction"
  - question: "What censoring rule (merge vs drop; paralyzable vs non-paralyzable) does the 25 kHz limit follow?"
    priority: MEDIUM
    blocks_phase: "Conventions & Energy-Scale Definition"
  - question: "At what deposit energy does peak Gamma cross 25 kHz (the CEvNS-to-muon crossover)?"
    priority: MEDIUM
    blocks_phase: "QPD Response Chain & Energy Reconstruction"

contradictions_unresolved: []
