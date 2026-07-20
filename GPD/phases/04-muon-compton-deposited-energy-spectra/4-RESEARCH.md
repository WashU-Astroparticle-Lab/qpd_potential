# Phase 4: Muon & Compton Deposited-Energy Spectra - Research

**Researched:** 2026-07-20
**Domain:** Cosmic-ray muon energy loss (Landau–Vavilov straggling), detector geometry / chord-length sampling, environmental-gamma Compton scattering (Klein–Nishina), Ge phonon calorimetry
**Depth:** standard
**Confidence:** HIGH (muon channel — textbook/benchmark-grade); MEDIUM (Compton channel — method is standard but the gamma-flux normalization and line intensities are a tunable, site-dependent input that the plan must source, not invent)

<user_constraints>

## User Constraints (from CONTEXT.md)

**No CONTEXT.md exists for this phase** (`gpd:discuss-phase` was not run). All decisions at agent's discretion, constrained by the project contract (`GPD/state.json`), `GPD/REQUIREMENTS.md`, `GPD/ROADMAP.md` Phase 4, and the Phase-1 locked conventions (`GPD/CONVENTIONS.md`). Those constraints are treated as binding and are summarized in **Active Anchor References** below.

</user_constraints>

## Active Anchor References

These are contract-critical inputs (mandatory, not background reading). Every one must be honored by the planner.

| Anchor | Content this phase MUST use | Where it binds |
| --- | --- | --- |
| **Phase-1 unified phonon scale** (`CONVENTIONS.md` §B, §G) | BOTH muon (electron-recoil) and Compton (electron-recoil) deposits land on the **same phonon `E_dep` scale** as CEvNS nuclear recoils. **NO ionization quenching, NO keVee/keVnr split, NO Lindhard.** Frenkel-defect storage is NR-only → **zero correction** for muon and Compton (both ER). Deliverable is `dR/dE_dep`, NOT reconstructed energy (that is Phase 5). | Energy axis of both output spectra |
| **Wafer geometry** (`CONVENTIONS.md` §D) | 4″×4″×2 mm = 10.16 × 10.16 × 0.20 cm; ρ = 5.323 g/cm³; V = 20.65 cm³; m ≈ 110 g; 8.29×10²⁴ Ge atoms/kg; Z = 32, ⟨A⟩ = 72.63, natural isotopes. Keep per-kg normalization (counts·kg⁻¹·day⁻¹·keV⁻¹) for output. | Chord model, interaction rate, normalization |
| **ref-pdg-muon** | I_v ≈ 70 m⁻²s⁻¹sr⁻¹ (E_μ > 1 GeV/c, vertical); horizontal-surface flux J ≈ 1 muon·cm⁻²·min⁻¹; mean E_μ ≈ 4 GeV; Cauchy mean chord ⟨ℓ⟩ = 4V/S for a convex body under isotropic flux. VALD-02: integral rate through wafer within ~30 %. | Muon flux normalization + validation |
| **ref-environmental-gamma** (Heusser-type) | Representative radiogenic line list (²³⁸U/²³²Th chains + ⁴⁰K + continuum) with a lab-background integral flux. **The flux normalization and line intensities are a documented TUNABLE input** — source them, do not invent (see Open Questions). | Compton source spectrum |
| **Klein–Nishina** | Per-electron Compton differential cross section; VALD-03 edge positions E_edge = 2E_γ²/(m_ec² + 2E_γ). | Compton cross section + validation |
| **⟨dE/dx⟩ in Ge** (`CONVENTIONS.md` §G) | Minimum-ionizing ⟨dE/dx⟩ = 1.370 MeV·cm²·g⁻¹ (≈ 7.29 MeV/cm). **Use the straggling distribution (MPV), NOT the mean, per chord.** | Muon deposit per chord |
| **Downstream (Phase 5)** | Phase 5 folds `dR/dE_dep` through R(E_rec\|E_dep). The muon channel drives the **saturated** regime (large deposits), so the muon `dR/dE_dep` **must extend to the tens-of-MeV deposits from long near-horizontal chords.** | Energy-grid upper bound |

**Forbidden proxies (MUST be guarded in the plan):**
- **fp-full-absorption** — modeling photopeaks / full-energy absorption instead of the single-scatter Compton continuum in a thin 2 mm wafer. The wafer is optically thin to MeV gammas (interaction probability ~4–6 % per crossing, below), so the scattered photon almost always escapes → the deposit is the Compton **electron** recoil, a continuum up to each edge, NOT a photopeak.
- **Chord geometry omitted / mean-vs-MPV** — using ⟨dE/dx⟩×length instead of sampling chord length AND Landau–Vavilov straggling. The Landau distribution is highly skewed; the peak is the MPV Δ_p, well below the mean.
- **Angular-pdf bias** — wrong muon zenith distribution → wrong chord-length mix (silent ~30 % error). The horizontal-flux sampling pdf ∝ cosⁿθ·cosθ·sinθ in θ, not cosⁿθ.

<research_summary>

## Summary

This phase computes two background **deposited-energy** spectra `dR/dE_dep` for the thin 110 g Ge wafer, both on the Phase-1 unified phonon scale (no quenching). Neither channel involves new physics — both are textbook energy-loss / scattering calculations — so the work is a small, well-anchored custom Monte Carlo plus an analytic Compton continuum, entirely on a laptop in NumPy/SciPy. The scientific care is entirely in the bookkeeping: getting the thin-wafer geometry, the Landau–Vavilov MPV (not the mean), the angular-flux weighting, and the thin-target single-scatter Compton continuum (not photopeaks) right.

**Muon channel (CALC-03/VALD-02):** sample sea-level muons from the modified-Gaisser ("Gaisser–Guan", arXiv:1509.06176) angular/energy flux, weighted onto the wafer surfaces with the correct cosθ projection; compute the analytic ray–box chord length ℓ (thin slab: ~2 mm for vertical muons up to ~14.4 cm for near-horizontal space-diagonal chords); draw the per-chord deposit from the **Landau–Vavilov** straggling distribution using the PDG most-probable-value Δ_p and width ξ (NOT the mean, NOT Moyal for the final); histogram to `dR/dE_dep`. Validate against the Cauchy invariant ⟨ℓ⟩ = 4V/S and the PDG integral flux (~1–2 Hz through the wafer). The long-chord high-E tail (tens of MeV) is the deliverable that feeds the Phase-5 saturation regime.

**Compton channel (CALC-04/VALD-03):** take a representative radiogenic line list (well-known line energies from the ²³⁸U/²³²Th chains + ⁴⁰K, plus a continuum) with a lab-background integral flux (Heusser-type, TUNABLE and to be sourced). Confirm thin-target single scatter from Ge attenuation data (NIST XCOM: μ/ρ ≈ 0.057 cm²/g at 1 MeV → interaction probability ≈ 6 % per 2 mm crossing; double-scatter ≲ 0.3 %). For each line E_γ, the deposit is the Compton **electron** kinetic energy T_e, distributed per Klein–Nishina up to the edge E_edge = 2E_γ²/(m_ec² + 2E_γ); sum over lines weighted by flux × Compton cross section. Validate edge positions against the closed form and total rate against flux × Ge Compton cross section (within factor ~2).

**Primary recommendation:** Build a single small NumPy MC. Muon deposit = Gaisser–Guan flux ⊗ analytic ray–box chord ⊗ Landau/Vavilov (`pylandau` or a validated custom sampler). Compton deposit: for robustness, **sample the Klein–Nishina scattering angle from dσ/dΩ and compute T_e kinematically** (avoids the error-prone dσ/dT_e change-of-variables), thin-target single-scatter, continuum-only. Both spectra output as `dR/dE_dep` [counts·kg⁻¹·day⁻¹·keV⁻¹] on a shared log grid spanning ~sub-keV to ≳100 MeV. Freeze the muon MC seed for reproducibility.

</research_summary>

<literature_landscape>

## Literature Landscape

### Foundational Papers / Sources

| Source | Authors | Year | Key Result | Relevance |
| --- | --- | --- | --- | --- |
| Modified Gaisser sea-level muon flux | Guan, Chu, Wang, Yu (arXiv:1509.06176) | 2015 | Analytic dI/dE_μdΩ valid at all zenith and down to ~GeV via effective angle cosθ* | Muon flux sampler (baseline) — parameters P₁–P₅ verified in project METHODS.md |
| PDG "Passage of Particles Through Matter" | Particle Data Group | current | Bethe ⟨dE/dx⟩; Landau–Vavilov MPV Δ_p and width ξ; κ = ξ/T_max regime selector | Per-chord deposit; MPV formula; κ check |
| PDG "Cosmic Rays" review | Particle Data Group | current | I_v ≈ 70 m⁻²s⁻¹sr⁻¹, J ≈ 1 cm⁻²min⁻¹, ⟨E_μ⟩ ≈ 4 GeV, cos²θ domain | VALD-02 flux anchors |
| Cauchy's mean-chord theorem | Cauchy / standard geometric probability | — | ⟨ℓ⟩ = 4V/S for a convex body under isotropic flux | Chord-MC unit test |
| Klein–Nishina cross section | Klein & Nishina | 1929 | dσ/dΩ per free electron; Compton kinematics; edge at θ = π | Compton deposit continuum |
| "Low-radioactivity background techniques" (Heusser) | G. Heusser, Annu. Rev. Nucl. Part. Sci. 45, 543 | 1995 | Standard review of environmental radiogenic gamma backgrounds (U/Th/K lines, lab fluxes) | ref-environmental-gamma — line list + flux normalization source |
| NIST XCOM / X-Ray Mass Attenuation Coefficients (Ge, Z=32) | NIST | current | μ/ρ(Ge): 0.0573 cm²/g @1 MeV, 0.0409 @2 MeV, 0.0745 @0.6 MeV | Thin-target single-scatter proof; Compton-fraction of μ |

### Recent Advances / Cross-checks

| Source | Authors | Year | Key Result | Relevance |
| --- | --- | --- | --- | --- |
| "A comparison of muon flux models at sea level" | Front. Energy Res. 9, 750159 | 2021 | Gaisser–Guan agrees with sea-level data; plain Gaisser overestimates low-E | Confidence in flux baseline; angular-shape caveat |
| Cecchini & Spurio, "Atmospheric muons" (arXiv:1208.1171) | — | 2012 | Angular-distribution energy dependence; 30–35 % inter-experiment normalization spread | Sets the honest muon-flux uncertainty band |
| Signatures of the differential Klein–Nishina electronic cross section (arXiv:1306.0418) | — | 2013 | Discusses dσ/dT_e (electron recoil energy) form explicitly | Reference for the closed-form Compton electron spectrum |
| Environmental γ-flux measurements (LNGS Hall C arXiv:2605.09835; LABChico EPJP 2022; underground HPGe surveys) | various | 2015–2026 | Integral γ-flux 0.1–0.5 cm⁻²s⁻¹ (underground); per-line fluxes (⁴⁰K ~0.036, ²⁰⁸Tl ~0.0016 cm⁻²s⁻¹ at one site) | Order-of-magnitude anchor for the tunable Compton normalization; surface labs are higher |

### Notation Conventions

| Quantity | Common notation | Our convention (Phase-1 §G) | Notes |
| --- | --- | --- | --- |
| Muon deposited energy | ΔE, E_loss | **E_dep** | phonon scale, no quenching |
| Muon differential flux | dI/dE_μdΩ, Φ_μ | **dI/dE_μ dΩ** [cm⁻²s⁻¹sr⁻¹GeV⁻¹] | track sr explicitly |
| Chord length | L, t, x | **ℓ** (cm); path mass **x = ρℓ** (g/cm²) | Landau formulas use x in g/cm² |
| Landau MPV | Δ_p, MPV | **Δ_p** | NOT the mean ⟨Δ⟩ |
| Compton electron recoil | T, E_e, T_e | **T_e** → maps to **E_dep** | deposit = T_e (scattered γ escapes) |
| Incident gamma energy | E_γ, hν | **E_γ** | |

**Key notational hazards:** (1) "flux" (J, cm⁻²s⁻¹, through a surface) vs "intensity" (I_v, cm⁻²s⁻¹sr⁻¹, per solid angle) — off by the ∫cosθ projection. (2) Landau formulas take path length as **mass thickness x = ρℓ in g/cm²**, not cm. (3) In the Compton channel, the DEPOSIT is the electron energy T_e, not the scattered photon energy and not E_γ.

</literature_landscape>

<methods_and_approaches>

## Methods and Approaches

### Standard Analytical / Numerical Methods

| Method | When to Use | Limitations | Key Reference |
| --- | --- | --- | --- |
| Gaisser–Guan flux rejection sampler | Sample (E_μ, θ) for all zenith, E_μ ≳ 1 GeV | Extrapolation below ~1 GeV (small rate fraction; still deposits MIP); no altitude/secondaries | Guan arXiv:1509.06176 |
| Analytic ray–box (slab) intersection | Chord length ℓ per sampled muon through the 10.16×10.16×0.20 cm box | Assumes straight track (valid: multiple scattering negligible over cm of Ge for GeV muons) | Standard AABB slab method |
| Landau / Vavilov straggling sampling | Per-chord deposit in a thin absorber (κ = ξ/T_max ≲ 0.01 → Landau) | Ignores δ-ray escape (~% at cm scale), radiative loss (negligible < ~100 GeV) | PDG Passage of Particles; `pylandau` |
| Klein–Nishina angle sampling + kinematic T_e | Compton electron-recoil continuum per line (RECOMMENDED — robust) | Per-free-electron (binding negligible at MeV for Ge) | Klein–Nishina 1929; Knoll ch.2 |
| Closed-form dσ/dT_e (Compton continuum) | Direct electron-energy spectrum per line | Change-of-variables coefficients error-prone — **verify against source before use** | arXiv:1306.0418; Turner/Knoll |
| Thin-target single-scatter weighting | Weight each line by interaction prob P = 1−e^(−μℓ̄) ≈ μℓ̄ | Valid only while μℓ ≪ 1 (holds: ~0.06) — multiple scatter dropped | NIST XCOM μ/ρ(Ge) |

### Computational Tools

| Tool/Package | Version | Purpose | Why Standard |
| --- | --- | --- | --- |
| Python + NumPy/SciPy | ≥3.11 | rejection sampling, ray–box, histogramming, quadrature | project-wide choice (COMPUTATIONAL.md); no HPC needed |
| pylandau (or validated custom Landau) | current | Landau/Vavilov straggling per chord | validate against PDG Δ_p before trusting |
| matplotlib | current | dR/dE_dep spectra | — |

### Supporting Tools

| Tool/Package | Version | Purpose | When to Use |
| --- | --- | --- | --- |
| NIST XCOM Ge μ/ρ table | current | attenuation / Compton fraction vs E_γ | single-scatter check, rate normalization; store as CSV with provenance |
| numba (optional) | current | accelerate MC loop | only if >10⁷ muons needed (unlikely) |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
| --- | --- | --- |
| Small custom NumPy MC | Geant4 / G4CMP / MUSIC / CRY / EcoMug | Weeks of setup for percent-level gains washed out by the Phase-5 QPD response; project spec forbids Geant4. Reject. |
| Gaisser–Guan analytic flux | CRY / CORSIKA / PARMA-EXPACS | Only if secondaries/showers/altitude matter; CRY undershoots at large zenith. Reject for baseline. |
| Landau/Vavilov sampling | Moyal approximation | Moyal underestimates the high-E tail (which sets the Phase-5 saturation morphology). Moyal ONLY for quick sanity checks. |
| KN angle-sample + kinematics | closed-form dσ/dT_e | Closed form is faster but the T_e change-of-variables is a coefficient trap; angle-sampling is self-validating (edge falls out automatically). |
| Analytic chord-length pdf | MC chord sampling | For a slab the chord pdf has a known analytic structure; use it as a cross-check but MC is simpler for the flux-weighted mix. |

**Installation / Setup:**

```bash
uv add numpy scipy matplotlib pylandau   # pylandau optional if custom Landau sampler is validated
```

### Package / Framework Reuse Decision

**Decision: bespoke code (a small custom NumPy Monte Carlo), NOT a heavyweight framework.** This matches the project-wide "small custom MC, no Geant4/G4CMP/CRY" decision (COMPUTATIONAL.md, METHODS.md Domain 2). Justification:
- **Missing capability in frameworks:** the deliverable is `dR/dE_dep` on the **unified phonon scale with no quenching** into a **specific thin-slab geometry**, feeding a downstream QPD response — general-purpose transport codes (Geant4) add weeks of setup and their extra physics (δ-ray transport, secondaries) is washed out by the Phase-5 response and is explicitly out of scope.
- **Control requirement:** the phase must expose the chord-length pdf, the Landau MPV, and the angular weighting as inspectable, unit-testable objects (Cauchy invariant, PDG Δ_p, J_horiz). A framework hides these.
- **Reuse where it counts:** use `pylandau` (or a validated custom Landau sampler) for the one non-trivial numerical primitive, and NIST XCOM Ge attenuation as a frozen CSV input. The Gaisser–Guan flux is a ~50-line rejection sampler; the ray–box chord is a standard analytic slab intersection; Klein–Nishina angle sampling is textbook. No wrapping of EcoMug/CRY/CORSIKA.

</methods_and_approaches>

<known_results>

## Known Results and Benchmarks

### Established Results

| Result | Value/Expression | Conditions | Source | Confidence |
| --- | --- | --- | --- | --- |
| Vertical muon intensity | I_v ≈ 70 m⁻²s⁻¹sr⁻¹ | E_μ > 1 GeV/c, sea level | PDG Cosmic Rays | HIGH |
| Horizontal-surface flux | J ≈ 1 muon·cm⁻²·min⁻¹ ≈ 167 m⁻²s⁻¹ | sea level, E_μ ≳ 1 GeV | PDG | HIGH |
| Zenith intensity shape | I(θ) ≈ I_v cos²θ | near ~3 GeV; steeper below, flatter above | PDG | HIGH |
| Horizontal flux from cosⁿθ | J_horiz = 2π I_v /(n+2); for n=2 → J = πI_v/2 | analytic angular integral | standard | HIGH |
| Ge minimum-ionizing ⟨dE/dx⟩ | 1.370 MeV·cm²·g⁻¹ = 7.29 MeV/cm | MIP muon | PDG Atomic/Nuclear Props; CONVENTIONS §G | HIGH |
| Cauchy mean chord | ⟨ℓ⟩ = 4V/S | convex body, isotropic flux | Cauchy | HIGH |
| Compton edge | E_edge = 2E_γ²/(m_ec² + 2E_γ) | free electron, backscatter θ=π | Klein–Nishina kinematics | HIGH |
| Ge total μ/ρ | 0.0745 (0.6), 0.0573 (1.0), 0.0510 (1.25), 0.0409 (2.0) cm²/g | Compton-dominated at these E | NIST XCOM (fetched) | HIGH |
| Environmental γ integral flux | ~0.1–0.5 cm⁻²s⁻¹ (underground); surface labs higher | 50–2700 keV band | LNGS/LABChico/HPGe surveys | MEDIUM (site-dependent) |

### Wafer-specific derived numbers (RECOMPUTE in-plan; shown for sanity)

| Quantity | Estimate | Basis | Confidence |
| --- | --- | --- | --- |
| Cauchy mean chord ⟨ℓ⟩ = 4V/S | ≈ 0.39 cm | V=20.65 cm³, S = 2(103.2 + 2×2.03) = 214.6 cm² → 4V/S = 82.6/214.6 | HIGH (arithmetic) |
| Longest chord (space diagonal) | ≈ 14.37 cm | √(10.16²+10.16²+0.20²) | HIGH |
| Vertical chord (thickness) | 0.20 cm; x = ρℓ ≈ 1.065 g/cm² | wafer thickness | HIGH |
| Landau width ξ (vertical chord) | ξ = (K/2)(Z/A)(x/β²) ≈ 0.072 MeV | K=0.307 MeV·mol⁻¹·cm², Z/A=0.4406, x=1.065, β≈1 | HIGH (formula), MEDIUM (numeric — recompute) |
| Mean deposit, vertical chord | ⟨Δ⟩ ≈ 7.29 MeV/cm × 0.2 cm ≈ 1.46 MeV | mean dE/dx × ℓ (do NOT use for spectrum) | HIGH |
| MPV deposit, vertical chord | Δ_p < ⟨Δ⟩ (order ~0.4–0.8 MeV) | PDG Δ_p formula — **compute, do not guess** | LOW (must compute) |
| Max mean deposit (long chord) | up to ~7.29 MeV/cm × 14.4 cm ≈ 100+ MeV | longest chord | MEDIUM |
| Muon rate through wafer | ~1.7 Hz (top face) + side faces → ~1.5–2 Hz | J≈1/cm²/min × 103.2 cm² = 1.72/s + inclined side flux | MEDIUM (VALD-02 anchor) |
| Compton interaction prob / crossing | ≈ 1−e^(−0.305×0.2) ≈ 6 % @1 MeV; ≈4 % @2 MeV | μ = (μ/ρ)ρ = 0.305 cm⁻¹ @1 MeV | HIGH |
| Double-scatter probability | ≲ (0.06)² ≈ 0.3 % | thin-target → single-scatter dominance CONFIRMED | HIGH |

### Compton edge positions (VALD-03 targets — compute exactly in-plan)

| Line (keV) | Isotope | E_edge = 2E_γ²/(511 + 2E_γ) (keV) |
| --- | --- | --- |
| 1460.8 | ⁴⁰K | ≈ 1243.5 |
| 2614.5 | ²⁰⁸Tl | ≈ 2381.7 |
| 1764.5 | ²¹⁴Bi | ≈ 1541.3 |
| 609.3 | ²¹⁴Bi | ≈ 429.3 |
| 583.2 | ²⁰⁸Tl | ≈ 405.5 |

### Limiting Cases

| Limit | Expected Behavior | Expression | Source |
| --- | --- | --- | --- |
| Isotropic flux (uniform per sr) | MC mean chord → Cauchy value | ⟨ℓ⟩ = 4V/S | Cauchy |
| Thin absorber (κ→0) | deposit pdf → Landau (skewed, long tail) | κ = ξ/T_max ≲ 0.01 | PDG |
| Thick absorber (κ→∞) | deposit pdf → Gaussian about mean | κ ≳ 10 | PDG/Vavilov |
| E_γ ≪ m_ec² | Compton edge → 0; T_e small | E_edge ≈ 2E_γ²/m_ec² | KN |
| E_γ ≫ m_ec² | edge → E_γ − m_ec²/2 | asymptotic | KN |
| Wafer optically thin | interaction prob → μℓ; deposit = T_e only | P ≈ μℓ ≪ 1 | Beer–Lambert |

**Key insight:** Every load-bearing number here is either textbook (flux anchors, ⟨dE/dx⟩, KN edges) or simple arithmetic on locked wafer constants (chord scales, interaction probability). The ONE quantity that must be honestly computed (not memorized) is the Landau MPV Δ_p per chord — it is the observable peak and is where the mean-vs-MPV pitfall bites.

</known_results>

<dont_rederive>

## Don't Re-derive

| Problem | Don't Derive From Scratch | Use Instead | Why |
| --- | --- | --- | --- |
| Sea-level muon flux spectrum & angular shape | Cascade/atmospheric-shower physics | Gaisser–Guan parametrization (arXiv:1509.06176), params P₁–P₅ (in METHODS.md) | Fully parametrized, data-validated; deriving would take months and be worse |
| Mean chord under isotropic flux | Geometric-probability integral over the box | Cauchy ⟨ℓ⟩ = 4V/S (unit test only) | Closed form; use it to VALIDATE the MC, not replace the flux-weighted mix |
| Landau/Vavilov straggling shape | Rutherford collision-integral convolution | PDG MPV Δ_p + width ξ formulas; `pylandau` | Classic; the MPV/width formulas are standard and the coefficient j=0.200 is fixed |
| Klein–Nishina cross section | QED calculation | dσ/dΩ (Klein–Nishina 1929); sample angle, get T_e kinematically | Textbook; re-deriving invites factor errors |
| dσ/dT_e (electron-energy Compton spectrum) | change of variables from dσ/dΩ by hand | angle-sampling + kinematics (primary), OR the published closed form (verify coefficients) | The dΩ→dT_e Jacobian is a known coefficient trap; angle-sampling sidesteps it |
| Ge photon attenuation / Compton fraction | Compute σ_Compton × Z × n_atom by hand | NIST XCOM μ/ρ(Ge) table (frozen CSV) | Tabulated to high accuracy incl. all processes; hand calc omits binding/incoherent corrections |
| Compton edge energy | re-derive from conservation | E_edge = 2E_γ²/(m_ec²+2E_γ) | One-line standard result; anchor for VALD-03 |

**Key insight:** Nothing in this phase is a novel derivation. Custom-code error risk is concentrated in (a) the angular sampling pdf (∝cosⁿθ·cosθ·sinθ, not cosⁿθ), (b) unit slips between ℓ [cm] and mass thickness x=ρℓ [g/cm²] in the Landau formulas, and (c) confusing scattered-photon vs electron energy in Compton. Guard these with unit tests, don't re-derive the physics.

</dont_rederive>

<common_pitfalls>

## Common Pitfalls

(Project pitfalls 10, 11, 12 from `GPD/literature/PITFALLS.md` apply directly; Compton-specific ones added.)

### Pitfall 1: Photopeaks instead of the Compton continuum (fp-full-absorption)

**What goes wrong:** Modeling the gamma deposit as full-energy absorption (photopeaks at E_γ), as a thick HPGe spectrometer would show.
**Why it happens:** Intuition from lab HPGe gamma spectroscopy, where crystals are cm-scale and photopeaks dominate.
**How to avoid:** The wafer is 2 mm and optically thin (interaction prob ~4–6 %, μℓ ≪ 1). The scattered photon escapes almost always → the deposit is the Compton **electron** recoil T_e, a **continuum up to E_edge**, not a line. Model single-scatter Compton only; drop photoabsorption (negligible at MeV in 2 mm Ge) and multiple scatter (≲0.3 %).
**Warning signs:** Peaks at E_γ in dR/dE_dep; any full-energy-absorption feature; edge not appearing at 2E_γ²/(m_ec²+2E_γ).

### Pitfall 2: Mean dE/dx instead of the Landau–Vavilov MPV

**What goes wrong:** Deposit = ⟨dE/dx⟩ × ℓ per chord → a delta-like deposit at the mean, missing the skew and the tail.
**Why it happens:** ⟨dE/dx⟩ = 1.37 MeV·cm²/g is the memorable number.
**How to avoid:** Sample from Landau/Vavilov with the PDG MPV Δ_p (which is BELOW the mean) and width ξ. Use κ = ξ/T_max to confirm the Landau regime. Use the mean only for a total-power cross-check.
**Warning signs:** MPV of the sampled deposits equals the mean; no long high-E tail; a spuriously narrow muon peak.

### Pitfall 3: Angular-pdf bias in the flux sampling

**What goes wrong:** Sampling zenith from ∝cos²θ instead of the horizontal-flux measure ∝cos²θ·cosθ·sinθ (the extra cosθ is the projection onto the surface, sinθ is the solid-angle Jacobian) → wrong chord-length mix (silent ~30 %).
**Why it happens:** "cos²θ" memorized without the projection/measure factors.
**How to avoid:** Derive the sampling pdf from dI/dE_μ·(n̂·Ω̂)dΩ dA for each face; validate the integrated rate against the analytic J_horiz = πI_v/2 for a cos²θ test flux before trusting the full Gaisser–Guan MC.
**Warning signs:** Muon rate off ~1.5–2 Hz by >2×; rate independent of wafer orientation; chord distribution missing the long-chord tail.

### Pitfall 4: Wrong mass-thickness units in Landau formulas

**What goes wrong:** Feeding ℓ [cm] where the formula expects x = ρℓ [g/cm²] (or vice versa) → ξ and Δ_p off by ρ = 5.323.
**Why it happens:** PDG formulas use mass thickness; geometry gives cm.
**How to avoid:** Carry x = ρℓ explicitly; unit-test ξ for the vertical chord (x≈1.065 g/cm² → ξ≈0.072 MeV).
**Warning signs:** Vertical-chord MPV off by ~×5; deposits scaling wrongly with wafer thickness.

### Pitfall 5: Gamma-flux normalization / line intensities invented

**What goes wrong:** Assigning per-line fluxes from memory → wrong Compton rate and wrong relative edge amplitudes.
**Why it happens:** Convenient to guess "typical" intensities.
**How to avoid:** Treat the integral flux and per-line intensities as a **documented tunable input** sourced from Heusser 1995 / a measured surface-lab spectrum, with a stated uncertainty band. Line **energies** are fixed nuclear data (HIGH); **intensities/flux** are site-dependent (source them). VALD-03 checks edge POSITIONS (robust) and total rate to factor ~2 (tolerant of flux uncertainty).
**Warning signs:** Compton rate quoted to <2× without a flux citation; per-line intensities with no provenance.

### Pitfall 6: Muon secondaries / stopped muons silently omitted or silently included

**What goes wrong:** Either ignoring the soft EM component and stopped-muon (Michel, ≤53 MeV) deposits without saying so, or half-including them inconsistently.
**Why it happens:** Small-detector "flux × area" defaults.
**How to avoid:** State scope explicitly. Baseline = through-going primaries with chord+Landau. Flag the soft component, δ-rays, stopped-muon Michel electrons, and muon-induced neutrons (which make CEvNS-like nuclear recoils) as explicit omissions. Neutron-induced recoils are the dominant real CEvNS background — out of scope but must be named.
**Warning signs:** No low-E muon tail below the Landau band; claims about the CEvNS-region background from muons alone.

</common_pitfalls>

<key_derivations>

## Key Derivations and Formulas (Starting Points)

### Muon flux — Gaisser–Guan (baseline sampler)

```
# Source: Guan et al., arXiv:1509.06176 (params verified in GPD/literature/METHODS.md)
dI/dE_μ = 0.14 (E_μ/GeV)^-2.7
          × [ 1/(1 + 1.1 E_μ cosθ*/115 GeV) + 0.054/(1 + 1.1 E_μ cosθ*/850 GeV) ]
   with the extra low-E / large-angle factor and effective angle
cosθ* = sqrt[ (cos²θ + P1² + P2 cos^P3 θ + P4 cos^P5 θ) / (1 + P1² + P2 + P4) ]
   P1=0.102573, P2=-0.068287, P3=0.958633, P4=0.0407253, P5=0.817285
# units: cm^-2 s^-1 sr^-1 GeV^-1
```
**Valid when:** all zenith, E_μ ≳ 1 GeV. **Breaks down when:** E_μ < 1 GeV (extrapolation; small through-going fraction).
**NOTE:** the exact prefactor grouping of the plain-Gaisser term must be taken verbatim from METHODS.md Domain 2 / arXiv:1509.06176 — do not transcribe from memory.

### Surface-flux sampling measure (guards Pitfall 3)

```
dN/dt ∝ ∫∫ dI/dE_μ(E,θ) (n̂ · Ω̂) dΩ dA ,  (n̂·Ω̂) ≥ 0 (inward)
# per θ for a horizontal face: pdf(θ) ∝ I(θ) cosθ sinθ ; for I∝cosⁿθ → ∝ cos^{n+1}θ sinθ
# analytic check: J_horiz = ∫ I_v cos²θ cosθ dΩ = π I_v / 2   (n=2)
```

### Chord length — ray–box (AABB slab) intersection

```
# box [0,Lx]×[0,Ly]×[0,Lz], Lx=Ly=10.16, Lz=0.20 cm; ray (entry p, dir Ω̂)
t_enter = max_i( (min_i - p_i)/Ω_i , (max_i - p_i)/Ω_i sorted ) ; ℓ = t_exit - t_enter
# Cauchy invariant (isotropic test): ⟨ℓ⟩ = 4V/S = 4·20.65 / 214.6 ≈ 0.385 cm
```

### Per-chord deposit — Landau–Vavilov MPV (guards Pitfall 2, 4)

```
# Source: PDG "Passage of Particles Through Matter"
ξ   = (K/2)(Z/A)(x/β²)  MeV ,  K = 0.307 MeV mol^-1 cm² , x = ρℓ [g/cm²]
Δ_p = ξ [ ln(2 m_e c² β²γ² / I) + ln(ξ/I) + j − β² − δ(βγ) ] ,  j = 0.200
# κ = ξ / T_max selects regime: κ ≲ 0.01 Landau ; κ ≳ 10 Gaussian ; between → Vavilov
# I(Ge) ≈ 350 eV (mean excitation); δ = density-effect correction
```
**Valid when:** thin absorber, κ in Landau/Vavilov regime (true for cm-scale Ge, GeV muons).
**Breaks down when:** very long chords approach thick-absorber (Gaussian) regime — check κ per chord and switch Vavilov→Gaussian as needed. Sample fluctuations with `pylandau`/true Landau, **not Moyal** for the final.

### Compton — Klein–Nishina + kinematics (RECOMMENDED path, guards Pitfall 1)

```
# Source: Klein & Nishina 1929; Knoll ch.2
dσ/dΩ = (r_e²/2)(E'/E_γ)² (E'/E_γ + E_γ/E' − sin²θ) ,  r_e = 2.818e-13 cm
E'(θ) = E_γ / (1 + α(1−cosθ)) ,  α = E_γ/m_e c²
T_e   = E_γ − E'  →  DEPOSIT  (scattered photon escapes thin wafer)
E_edge = T_e(θ=π) = 2 E_γ² / (m_e c² + 2 E_γ)          # VALD-03
# Method: sample θ ∝ dσ/dΩ per line → T_e ; weight line by  flux_i × [1−e^{−μ(E_i)ℓ̄}] ≈ flux_i μ(E_i)ℓ̄
# thin-target single scatter: μ(E) from NIST XCOM Ge; μℓ ≪ 1 confirmed
```
**Valid when:** single-scatter, free-electron (binding ≪ MeV), scattered γ escapes (thin wafer).
**Breaks down when:** thick target / low E_γ where photoabsorption or multiple scatter matter — NOT the case here (verify μℓ per line).

### Closed-form electron-energy Compton spectrum (OPTIONAL — verify before use)

```
# Source: standard Compton-continuum form (e.g. arXiv:1306.0418, Turner, Knoll)
# dσ/dT_e per electron, with s = T_e/E_γ, α = E_γ/m_e c², 0 ≤ T_e ≤ E_edge :
#   dσ/dT_e = (π r_e² / (m_e c² α²)) × [ 2 + s²/(α²(1−s)²) + (s/(1−s))(s − 2/α) ]
# ⚠ COEFFICIENTS NOT INDEPENDENTLY VERIFIED THIS SESSION — the plan MUST cross-check
#   this against a primary source AND against the angle-sampling result before trusting it.
```
**Recommendation:** prefer the angle-sampling method above; use this closed form only as a cross-check after verifying its coefficients.

</key_derivations>

<validation_strategies>

## Validation Strategies

| Check | Target | Method | Requirement |
| --- | --- | --- | --- |
| Chord-MC Cauchy invariant | ⟨ℓ⟩ = 4V/S ≈ 0.385 cm under **isotropic** test flux | run MC with uniform-per-sr flux; compare mean chord | unit test (pre-physics) |
| Angular integral | J_horiz = πI_v/2 for a cos²θ test flux | analytic vs MC before Gaisser–Guan | guards Pitfall 3 |
| Muon integral rate | ~1.5–2 Hz through wafer; within **30 %** of PDG flatface estimate (J×A_top + side faces) | integrate sampled rate | **VALD-02 / test-muon-flux** |
| Muon MPV | vertical-chord Δ_p from sampled deposits matches PDG Δ_p formula | histogram vertical-crossing subset; compare MPV | guards Pitfall 2 |
| Landau width | ξ(vertical) ≈ 0.072 MeV | recompute from formula; compare to sampler | guards Pitfall 4 |
| High-E tail present | deposits extend to tens of MeV from long chords | inspect dR/dE_dep upper range | Phase-5 saturation input |
| Compton single-scatter | interaction prob ≈ 4–6 %/crossing; double-scatter ≲0.3 % | μℓ from NIST XCOM Ge | confirms thin-target |
| Compton edges | E_edge at 2E_γ²/(m_ec²+2E_γ) for each line (1243.5 keV for ⁴⁰K, 2381.7 keV for ²⁰⁸Tl, …) | locate edge in dR/dE_dep vs closed form | **VALD-03 / test-compton-edges** |
| Compton continuum, not peaks | NO photopeak at E_γ; continuum up to edge | inspect spectrum | guards fp-full-absorption |
| Compton total rate | flux × Ge Compton cross section within **factor ~2** | ∫ over lines vs Φ·σ_C·N_e | **VALD-03** |
| Pileup / stop-condition | total muon+γ event rate (few Hz) ≪ 50 kHz → no event-level pileup; within-event muon saturation flagged for Phase 5 | rate × pulse-duration occupancy | ROADMAP Phase 4/5 stop-condition |
| Energy closure & normalization | dR/dE_dep integrates to the total rate; per-kg normalization consistent | closure test | prevents unit slips |

</validation_strategies>

<open_questions>

## Open Questions

1. **Environmental gamma flux normalization and per-line intensities (ref-environmental-gamma).**
   - What we know: line ENERGIES are fixed nuclear data (⁴⁰K 1460.8, ²⁰⁸Tl 2614.5/583.2, ²¹⁴Bi 609.3/1764.5/1120.3, ²¹⁴Pb 351.9, ²²⁸Ac 911.2 keV, …); integral fluxes are ~0.1–0.5 cm⁻²s⁻¹ underground (LNGS/LABChico/HPGe surveys) and higher at surface.
   - What's unclear: the exact integral flux and per-line intensities for THIS (surface, unshielded) setting — Heusser 1995 is the canonical review but the numbers are site-dependent.
   - Recommendation: **the plan must source the line list + intensities + integral flux from Heusser (Annu. Rev. Nucl. Part. Sci. 45, 543, 1995) or a cited measured surface-lab spectrum, treat them as a TUNABLE input with an explicit uncertainty band, and NOT invent them.** VALD-03 (edge positions + factor-2 rate) is robust to this uncertainty.

2. **Continuum component of the radiogenic gamma environment.**
   - What we know: real environmental spectra have a Compton/scattered continuum under the lines, not just discrete lines.
   - What's unclear: whether to model only the discrete lines (simpler) or add a representative continuum.
   - Recommendation: start with the dominant discrete lines (drives the edge validation); add a parametrized continuum as a documented option. Flag as agent's discretion.

3. **Landau MPV numeric value per chord.**
   - What we know: Δ_p < mean; formula and inputs are fixed.
   - What's unclear: the exact Δ_p was not computed this session (needs I(Ge), δ(βγ), and the muon-energy distribution).
   - Recommendation: compute Δ_p in-plan from the PDG formula for the vertical chord as a unit test; do not hard-code a memorized value.

4. **Stopped-muon / soft-component contribution to the low-E deposit tail.**
   - What we know: sub-GeV stopped muons add a Michel-electron component (≤53 MeV); soft EM component adds ~tens-of-MeV deposits.
   - What's unclear: their magnitude for this thin wafer.
   - Recommendation: baseline = through-going primaries; flag stopped-muon/soft/δ-ray/neutron components as explicit scope omissions (Pitfall 6). Add a stopped-muon subsample only if the low-E reconstructed spectrum later needs it.

</open_questions>

<not_found>

## What Was NOT Found

- **Exact dσ/dT_e closed-form coefficients** were not independently re-verified this session (angle-sampling recommended to avoid the trap; closed form flagged for in-plan verification against arXiv:1306.0418 / Knoll / Turner).
- **A surface-level (unshielded) environmental gamma integral flux specific to this setup** was not pinned down — measured values found are mostly underground (0.1–0.5 cm⁻²s⁻¹); the surface value is higher and site-dependent (must be sourced from Heusser or a local measurement).
- **Heusser (1995) primary line-intensity table** was not fetched directly (search surfaced the citation and secondary surveys, not the article's tables) — the plan must obtain it from the primary source.
- **Exact Landau MPV Δ_p for the wafer chords** — formula and inputs are in hand, but the number must be computed, not looked up.

</not_found>

<sources>

## Sources

### Primary (HIGH)

- **PDG "Cosmic Rays" review** — I_v ≈ 70 m⁻²s⁻¹sr⁻¹, J ≈ 1 cm⁻²min⁻¹, cos²θ, ⟨E_μ⟩≈4 GeV. (ref-pdg-muon)
- **PDG "Passage of Particles Through Matter"** — Bethe ⟨dE/dx⟩, Landau–Vavilov MPV Δ_p (j=0.200), width ξ, κ regime selector.
- **Guan et al., arXiv:1509.06176** — modified-Gaisser sea-level muon flux, params P₁–P₅ (verified in project METHODS.md).
- **NIST X-Ray Mass Attenuation Coefficients, Germanium (Z=32)** — μ/ρ = 0.0745/0.0573/0.0510/0.0409 cm²/g at 0.6/1.0/1.25/2.0 MeV (fetched this session). Confirms single-scatter (μℓ≈0.06).
- **Klein & Nishina (1929)** — Compton dσ/dΩ; edge E_edge = 2E_γ²/(m_ec²+2E_γ).
- **GPD/literature/METHODS.md, PITFALLS.md, SUMMARY.md** — project methods (Gaisser–Guan sampler, Landau/Vavilov not Moyal, chord MC, Cauchy invariant) and pitfalls 10/11/12; verified against primary sources by the project survey.
- **GPD/CONVENTIONS.md** — unified phonon scale (no quenching), wafer geometry, ⟨dE/dx⟩=1.370 MeV·cm²/g, symbol registry.

### Secondary (MEDIUM)

- **Heusser, Annu. Rev. Nucl. Part. Sci. 45, 543 (1995)** — canonical environmental radiogenic-gamma review (ref-environmental-gamma); line list + flux normalization TO BE SOURCED in-plan.
- **Front. Energy Res. 9, 750159 (2021)** — muon-flux model comparison; Gaisser–Guan vs data.
- **Cecchini & Spurio, arXiv:1208.1171** — muon angular distribution; 30–35 % inter-experiment normalization spread (honest flux band).
- **Environmental γ-flux surveys** — LNGS Hall C (arXiv:2605.09835, ~0.46 cm⁻²s⁻¹), LABChico (EPJP 2022; ⁴⁰K 0.036, ²⁰⁸Tl 0.0016 cm⁻²s⁻¹), underground HPGe (~0.124 cm⁻²s⁻¹) — order-of-magnitude anchors for the tunable normalization (underground; surface higher).

### Tertiary (LOW — needs validation at plan/execution)

- **arXiv:1306.0418** — differential Klein–Nishina electronic cross section dσ/dT_e; use to verify the closed-form electron-energy spectrum if that path is chosen.
- **pylandau** package — Landau/Vavilov sampling; validate against PDG Δ_p before trusting.
- **Knoll, *Radiation Detection and Measurement* (4th ed.), ch. 2** — Compton continuum / edge (textbook background knowledge).

</sources>

<metadata>

## Metadata

**Research scope:**
- Physics subfield: cosmic-ray muon energy loss + geometric probability (chords) + environmental-gamma Compton scattering, on a Ge phonon-calorimeter scale.
- Methods explored: Gaisser–Guan flux sampling, ray–box chord geometry, Landau–Vavilov straggling, Klein–Nishina angle-sampling vs closed-form dσ/dT_e, thin-target single-scatter weighting.
- Known results catalogued: PDG flux anchors, Cauchy ⟨ℓ⟩=4V/S, ⟨dE/dx⟩ Ge, NIST XCOM Ge μ/ρ, Compton edge positions, wafer-derived chord/rate/interaction numbers.
- Pitfalls: photopeaks-vs-continuum, mean-vs-MPV, angular-pdf bias, mass-thickness units, invented gamma intensities, secondaries scope.

**Confidence breakdown:**
- Literature coverage: HIGH (muon) / MEDIUM (Compton flux normalization is site-dependent, must be sourced).
- Methods: HIGH — all standard, laptop-scale, project-endorsed small-MC approach.
- Known results: HIGH for anchors/edges/attenuation; the muon MPV must be computed in-plan.
- Pitfalls: HIGH — the three contract-forbidden proxies map directly to guarded pitfalls with warning signs.

**Research date:** 2026-07-20
**Valid until:** 2026-08-19 (30 days — established detector/nuclear physics; the only volatile item is the tunable gamma-flux normalization).

</metadata>

---

## Caveats and Alternatives (adversarial self-critique)

- **Weakest anchor — the Compton flux normalization.** The Compton total rate (and the pileup assessment) hinges on an integral gamma flux that is site-dependent and NOT locked. I deliberately kept this a tunable input and made VALD-03 lean on edge POSITIONS (robust) plus a factor-2 rate tolerance. If the plan needs an absolute Compton rate, it must first source Heusser 1995 or a measured surface spectrum; do not let a memorized flux masquerade as an anchor. My underground-survey numbers (0.1–0.5 cm⁻²s⁻¹) are LOWER bounds for a surface setting.
- **Closed-form dσ/dT_e coefficients unverified.** I did not re-derive or independently verify the electron-energy Compton spectrum coefficients this session, so I recommend the angle-sampling method (self-validating via the automatically-correct edge) and flagged the closed form for in-plan verification. A planner who prefers the closed form MUST verify it against a primary source and against the angle-sampling histogram — this is a genuine coefficient trap.
- **Landau MPV not numerically evaluated.** I give the formula and the ξ value but explicitly did NOT produce Δ_p, because it needs I(Ge), the density-effect δ, and the muon-energy distribution folded per chord. Presenting a guessed MPV would itself be the mean-vs-MPV pitfall in disguise. The plan must compute it.
- **Straight-track assumption.** Chords assume undeflected muons. Multiple scattering over ≤14 cm of Ge for GeV muons is small but nonzero; for the longest near-edge chords the entry/exit geometry is sensitive to it. Acceptable at this phase's accuracy (the Phase-5 response washes out percent-level chord errors), but stated as an omission.
- **Long-chord tail statistics.** The tens-of-MeV deposits that drive Phase-5 saturation come from RARE near-horizontal chords through the thin slab. A naive MC will under-sample them. Recommend importance sampling / stratification in solid angle (or a dedicated long-chord subsample) so the high-E tail is statistically resolved — otherwise the single most Phase-5-relevant part of the spectrum is the noisiest.
- **Alternative worth noting:** an analytic thin-slab chord-length pdf exists and could replace the MC chord step entirely (cheaper, exact). I recommend MC for the flux-weighted mix but suggest using the analytic slab pdf as an independent cross-check of the MC chord distribution, beyond just the Cauchy mean.
- **Scope honesty.** Muon secondaries, stopped muons, δ-ray escape, and muon-induced neutrons are all dropped in the baseline. Neutron-induced nuclear recoils mimic CEvNS exactly and are the dominant real reactor-CEvNS background — out of scope here but MUST be named in any downstream sensitivity statement, not silently omitted.

---

_Phase: 04-muon-compton-deposited-energy-spectra_
_Research completed: 2026-07-20_
_Ready for planning: yes_
