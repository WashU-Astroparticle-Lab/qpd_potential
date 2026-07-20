# Methods Research

**Domain:** Reactor CEvNS + cosmic-muon spectra in reconstructed energy for a 1 kg Ge crystal read out by Quantum Parity Detectors (QPDs)
**Researched:** 2026-07-20
**Confidence:** HIGH (core formulas verified against primary sources); MEDIUM where flagged inline
**Research mode:** balanced (methods dimension)

**Anchor:** Ramanathan et al., "Quantum parity detectors: a qubit-based particle-detection scheme with meV thresholds for rare-event searches," APS Open Science 1, 000013 (2026), DOI 10.1103/kqd2-spb1, arXiv:2405.17192. The pulse model, tunneling-rate model, and efficiency chain quoted below were verified directly against the arXiv HTML of this paper.

**Conventions used throughout:** natural units for cross sections (ħ = c = 1, convert with 1 GeV⁻² = 3.894 × 10⁻²⁸ cm²); recoil kinetic energy `T` in keV_nr; neutrino energy `E_ν` in MeV; muon energy in GeV; sensor-side energies in meV/µeV. sin²θ_W = 0.23857 (low-energy MS-bar, PDG). Ge: Z = 32, ⟨A⟩ = 72.63, ρ = 5.323 g/cm³, natural isotopes 70/72/73/74/76 (rate calculations should sum over isotopes, not use ⟨A⟩, since Q_W² ∝ N² weights the isotope mix).

---

## Recommended Methods

### Domain 1: CEvNS Differential Rate (analytical, deterministic quadrature)

**Cross section — Freedman (Standard Model, tree level + radiative-corrected couplings):**

```
dσ/dT (E_ν, T) = (G_F² M / 4π) · Q_W² · [1 − M T / (2 E_ν²)] · F²(q²)
```

with `Q_W = N − (1 − 4 sin²θ_W) Z` (≈ N − 0.0457 Z; the proton coupling is accidentally suppressed, so the rate is ∝ N² to ~0.5%), `M` the nuclear mass, `q² = 2 M T`, and kinematic limits

```
T_max(E_ν) = 2 E_ν² / (M + 2 E_ν),      E_ν,min(T) = (T + √(T² + 2 M T)) / 2 ≈ √(M T / 2).
```

Subleading terms `−T/E_ν + T²/(2E_ν²)` exist in the full expression but are O(T/E_ν) ~ 10⁻³ at reactor energies; the form above is the standard choice (used by CONUS+, TEXONO analyses, e.g. arXiv:2501.18550). Use it, but state the truncation.

**Form factor:** Helm parameterization,

```
F_Helm(q) = 3 j₁(q R₀)/(q R₀) · exp(−q² s² / 2),
R₀² = c² + (7/3)π²a² − 5s²,  c = (1.23 A^{1/3} − 0.60) fm,  a = 0.52 fm,  s = 0.9 fm
```

(Lewin & Smith parameters, Astropart. Phys. 6, 87 (1996)). **Key simplification:** at reactor energies q_max = √(2 M T_max) ≲ 8 MeV/c → qR₀ ≪ 1 → F² > 0.998 for Ge. Implement Helm anyway (it is nearly free and makes the code reusable for higher-energy sources), but document that the reactor result is form-factor independent — this is explicitly noted in the CONUS+/TEXONO analysis literature (arXiv:2501.18550). Klein–Nystrand (F_KN(q) = [3 j₁(qR_A)/(qR_A)] · 1/(1 + a_k²q²), a_k = 0.7 fm, R_A = 1.23 A^{1/3} fm; COHERENT's convention) is an equally valid alternative; do not spend effort choosing between them for this problem.

**Reactor flux model:** Use the hybrid standard:

- **2–8 MeV:** Huber (235U, 239Pu, 241Pu conversion; PRC 84, 024617, arXiv:1106.0687) + Mueller (238U summation; PRC 83, 054615, arXiv:1101.2663) — the "Huber–Mueller" model. Note the known ~5% normalization tension (reactor antineutrino anomaly); the Kurchatov Institute (Kopeikin et al. 2021, arXiv:2103.01684) re-measured the 235U/239Pu β-ratio and favors a lower 235U flux consistent with rate data. **Recommendation:** implement Huber–Mueller as baseline, carry a ±5% flux normalization systematic, optionally offer the KI rescaling as a switch.
- **Below 1.8 MeV (below IBD threshold, where conversion data do not exist):** Huber–Mueller is undefined here, and this region contributes substantially to the lowest recoil bins. Use a summation-based tabulation (e.g., the Estienne–Fallot summation model, PRL 123, 022502) or the standard low-energy tabulations used by CONUS/TEXONO; a crude but common fallback is the Vogel–Engel analytic form `dN/dE ∝ exp(a₀ + a₁E + a₂E²)` per isotope (PRD 39, 3378). Also include antineutrinos from neutron capture ²³⁸U(n,γ)²³⁹U → β decays, a known low-energy contribution.
- **Normalization:** fissions/s = P_th / ⟨E_f⟩ with per-isotope energy release ≈ {235U: 202.36, 238U: 205.99, 239Pu: 211.12, 241Pu: 213.60} MeV/fission (Ma et al., PRC 88, 014605), ⟨E_f⟩ = Σ fᵢ Eᵢ. Rule of thumb for validation: ~1.8–2 × 10²⁰ ν̄/s per GW_th, i.e. ~6 × 10²⁰ ν̄/s at 3 GW_th; flux at 25 m ≈ 6×10²⁰/(4π·(2500 cm)²) ≈ 8 × 10¹² ν̄ cm⁻² s⁻¹. [MEDIUM: numbers are standard textbook anchors; recompute, don't copy.]

**Isotope evolution:** For a spectrum-shape project (not a rate-vs-time measurement), **do not build a burnup code.** Use static cycle-averaged PWR fission fractions (typical: f₂₃₅ ≈ 0.58, f₂₃₈ ≈ 0.07, f₂₃₉ ≈ 0.29, f₂₄₁ ≈ 0.06 — Daya Bay convention, PRL 130, 211801) and quantify sensitivity by evaluating begin-of-cycle vs end-of-cycle fractions as a band. The 239Pu spectrum is softer than 235U, so the effect on the CEvNS recoil spectrum shape is a few percent at most.

**Rate folding (deterministic, not MC):**

```
dR/dT = N_T · (1 / 4πL²) · Σ_isotopes fᵢ/⟨E_f⟩ · P_th · ∫_{E_min(T)}^{E_max} dE_ν  (dNᵢ/dE_ν)(E_ν) · dσ/dT(E_ν, T)
```

with N_T = targets/kg summed over Ge isotopes. Use adaptive quadrature (`scipy.integrate.quad`) or fixed high-order Gauss–Legendre on a log grid in T; the integrand is smooth. This 1D folding is cheap (< seconds); reserve Monte Carlo only for the detector-response stage.

**Recoil energy → phonon energy (no quenching needed, one correction to discuss):** In a pure phonon calorimeter with no applied field there is no ionization channel and no Luke–Neganov gain, so the ionization quenching factor (Lindhard) is **irrelevant** — do not import it. The full recoil energy thermalizes to phonons **except** for energy stored in stable lattice defects (Frenkel pairs): recoil energy = phonon energy + defect-storage energy. For Ge this is measured/estimated at the few-percent level and grows in relative importance at low recoil energy (displacement threshold ~O(20 eV)); see SuperCDMS ²⁰⁶Pb defect-loss study (arXiv:1805.09942) and Ionel Lazanu's defect-production notes (arXiv:0907.0342). **Recommendation:** compute spectra assuming 100% recoil→phonon, then apply/quote a few-percent defect-storage systematic on the energy scale for nuclear recoils; electron recoils (muons) have no such correction.

### Domain 2: Sea-Level Muon Energy Deposits in a Small Crystal (Monte Carlo)

**Flux model — modified Gaisser ("Gaisser–Guan"), verified against arXiv:1509.06176:**

```
dI/dE_μ = 0.14 · [ (E_μ/GeV) · (1 + 3.64 GeV / (E_μ (cos θ*)^1.29)) ]^{−2.7}
          · [ 1/(1 + 1.1 E_μ cos θ*/115 GeV) + 0.054/(1 + 1.1 E_μ cos θ*/850 GeV) ]
          [cm⁻² s⁻¹ sr⁻¹ GeV⁻¹]
```

with the Earth-curvature effective angle

```
cos θ* = √[ (cos²θ + P₁² + P₂ cos^{P₃}θ + P₄ cos^{P₅}θ) / (1 + P₁² + P₂ + P₄) ],
P₁ = 0.102573, P₂ = −0.068287, P₃ = 0.958633, P₄ = 0.0407253, P₅ = 0.817285.
```

This extends plain Gaisser (valid only E ≳ 100/cosθ GeV, θ < 70°) to all zenith angles and to ~GeV energies; plain Gaisser overestimates the low-energy flux. Comparisons against sea-level data (Frontiers in Energy Research 9, 750159) show good agreement. **Recommendation:** Gaisser–Guan as baseline; below ~1 GeV it is still an extrapolation — since sub-GeV muons are a small fraction of the through-going rate and still deposit ~MeV/mm, the spectral-shape error there is a second-order effect on the deposit spectrum. Do not use plain Gaisser alone; do not pull in CRY/CORSIKA (overkill for a 1 kg crystal, and CRY is known to undershoot at large zenith angles).

**Geometry sampling (MC):** Sample muons on a bounding surface (hemisphere or box faces) with the flux-weighted angular measure `dI/dE · cosθ_n dΩ dA` (θ_n = angle to surface normal); compute the chord length ℓ through the crystal analytically (box/cylinder intersection). Validation invariant: for an isotropic-per-solid-angle flux the mean chord obeys Cauchy's theorem ⟨ℓ⟩ = 4V/S; for the actual cos-weighted muon flux the MC mean chord should be checked against a direct numerical integral. Total-rate anchors: vertical intensity ≈ 70 m⁻² s⁻¹ sr⁻¹, integrated flux through a horizontal surface ≈ 1 muon cm⁻² min⁻¹ (PDG Cosmic Rays review) — for a 1 kg Ge crystal (~188 cm³, top face ~30–35 cm² if roughly cubic) expect an O(0.5–1) Hz muon rate. [HIGH for anchors; recompute geometry factor.]

**Energy deposit — restricted energy loss + straggling (PDG Ch. "Passage of particles through matter"):**

- Mean loss: Bethe ⟨dE/dx⟩; for Ge, a minimum-ionizing muon deposits ≈ 1.37 MeV cm²/g × 5.323 g/cm³ ≈ 7.3 MeV/cm [MEDIUM: recompute from PDG muon tables for Ge, do not trust the memorized number]. A vertical ~5.7 cm traversal deposits ~40 MeV.
- **Do not use the mean.** For a finite absorber the observable is the straggling distribution. Use the PDG most-probable-value formula
  `Δ_p = ξ [ ln(2mc²β²γ²/I) + ln(ξ/I) + j − β² − δ ]`, ξ = (K/2)⟨Z/A⟩(x/β²) MeV (x in g/cm²), j = 0.200,
  and sample fluctuations from **Vavilov** (κ = ξ/T_max decides the regime: κ ≲ 0.01 → Landau; κ ≳ 10 → Gaussian). For cm-scale Ge and GeV muons you are in the Landau/Vavilov regime — the deposit spectrum per chord is a Landau-like peak with a long high tail. Practical implementation: sample per-chord energy loss from the Landau (or Moyal-approximation only for quick checks — Moyal underestimates the tail) with the PDG MPV and width ξ; `scipy.stats.levy_stable`-based Landau or the `pylandau` package are adequate.
- **What is deliberately dropped (state it):** δ-ray escape from the crystal surface (reduces deposits by ~% at cm scale), radiative losses (negligible below ~100 GeV in cm of Ge for the deposit spectrum shape), muon stopping/decay in the crystal (the sub-GeV stopping population adds a small Michel/capture component — flag as a known omission or add a stopped-muon subsample if the low-energy reconstructed spectrum matters), and secondary shower particles accompanying the muon (no shielding/veto is specified; document as out of scope).

**Method class:** This domain should be a **small custom Monte Carlo** (sample E, θ, entry point → chord → Landau-fluctuated deposit), not Geant4. The problem is 1 volume, 1 material, 1 particle species; Geant4 adds weeks of setup for percent-level gains the QPD response chain will wash out.

### Domain 3: Quasiparticle Dynamics in the QPD Sensor Chain (analytical ODE model, per anchor paper)

**Use the Ramanathan et al. model verbatim as the baseline** (all items below verified against arXiv:2405.17192):

- **Pulse model (paper Eq. 4):**
  `δn_qp,trap(t) = (N_qp^r / V_tr) · (τ_qp/(τ_inj − τ_qp)) · (e^{−t/τ_inj} − e^{−t/τ_qp})`
  where τ_inj is an effective injection time (subsuming phonon transport in the crystal, absorption, absorber diffusion) and τ_qp is the trap recombination lifetime (0.1–10 ms in Al, quiescent-density dependent).
- **Tunneling rate:** `Γ_in ≈ K · n_qp`, with `K ≈ 16 E_J k_B T / (𝒩 Δ h)` for the OCS architecture (K depends on Josephson energy, gap, temperature, and QP density of states).
- **QP yield:** `N_qp^r = E_abs · η_tr · η_pb,tr / Δ_tr`, with the efficiency chain η_ph ≈ 0.65 (phonon collection at 4% areal coverage), η_pb ≈ 0.4–0.6 (pair-breaking), η_tr ≈ 0.4–0.7 (trapping); combined ≈ 0.32 in the paper, and the project spec's ~50% deposited-energy-to-signal efficiency sits inside this range. QP creation costs ~2Δ per pair; each QP carries ≥ Δ_trap.
- **Energy sharing across the 1/mm² sensor array:** phonons from a point deposit spread over the crystal; with no G4CMP, model per-sensor absorbed energy as `E_abs = E_dep · η_ph · w_i` with weights w_i from a lumped model. Recommended lumped model: exponential phonon collection with time constant τ_collect = 4V/(⟨v_g⟩ A_abs η̄_abs) (standard surface-absorption/phonon-collection formula from the CDMS/TES design literature) and, at the balanced level, **uniform partition w_i = A_i/ΣA** after a few crystal-crossing times — justified because ballistic phonons in high-purity Ge at mK randomize over many surface reflections before absorption. Position dependence is then a systematic, not a model feature.

**Underlying microphysics (use for parameter values and regime checks, not for simulation):**

- Kaplan et al., PRB 14, 4854 (1976): QP and phonon lifetimes in superconductors — source for τ_qp scalings with gap and temperature.
- Kozorezov et al., PRB 61, 11807 (2000) "Quasiparticle-phonon downconversion in nonequilibrium superconductors": the pair-breaking cascade; the canonical downconversion efficiency is η_pb ≈ 0.57–0.6 for thick films (energy lost to sub-2Δ phonons), consistent with the anchor's 0.4–0.6 range. [HIGH for the framework; MEDIUM on the exact 0.57 figure — verify against Kozorezov when fixing η_pb.]
- **Rothwarf–Taylor equations** (PRL 19, 27 (1967)) for coupled QP/phonon populations:
  `dN/dt = I_qp + 2 N_ω/τ_B − R N²`, `dN_ω/dt = I_ph + R N²/2 − N_ω/τ_B − N_ω/τ_γ`
  (N = QP density, N_ω = 2Δ-phonon density, R = recombination coefficient, τ_B = pair-breaking time, τ_γ = phonon escape time). These produce the phonon-bottleneck: recombination phonons re-break pairs, extending the effective τ_qp. **When you need them:** only if QP densities get high enough that recombination is nonlinear (τ_qp ∝ 1/n_qp) — which *will* happen for muon deposits (~40 MeV → ~10¹¹ QPs system-wide). **Recommendation:** implement the anchor's linear two-exponential model for CEvNS-scale deposits; for muon-scale deposits promote τ_qp to density-dependent form (solve the RT ODEs or use the known bimolecular-decay solution n(t) = n₀/(1 + R̃ n₀ t)) and document the transition deposit energy where linearity fails.
- **Gap engineering (Ta→Al and Al→Hf):** trapping works when Δ_absorber/Δ_trap ≳ 2–4 so QPs relax into the trap and cannot return. Reference gap anchors: Δ = 1.764 k_B T_c gives Δ_Ta ≈ 700 µeV (T_c 4.48 K), Δ_Al ≈ 180 µeV bulk (thin films up to ~2×), Δ_Hf ≈ 20–60 µeV (T_c ~0.13–0.4 K, film dependent) [MEDIUM: thin-film gaps vary by fab; treat as parameters, not constants]. The anchor paper's Al/Hf numbers (~400 µeV absorber film / ~100 µeV trap, ratio ~4) illustrate that film values differ from bulk. Lower Δ_trap → more QPs per eV (N ∝ 1/Δ_tr) and lower threshold, but shorter τ_qp margins and stricter T_base requirements.

**Method class:** closed-form/ODE evaluation per event — no per-phonon MC. The whole response chain is (deposit energy, position) → per-sensor E_abs → n_qp(t) template → Γ_in(t) = K n_qp(t). This is exactly what "no G4CMP" implies and matches the anchor paper's own methodology.

### Domain 4: Energy Reconstruction from Bandwidth-Limited Tunneling Telegraph Signals (point-process statistics + MC)

**Signal model:** tunneling events are an **inhomogeneous Poisson point process** with rate Γ_in(t) = K n_qp(t) per sensor; the project adds an EMG (exponentially modified Gaussian) arrival-time profile for bursts — i.e., the effective intensity is the pulse template convolved with Normal(µ,σ) ⊛ Exp(τ) jitter. With perfect tunneling identification, the data per sensor is a timestamp list, censored by finite bandwidth.

**Bandwidth/saturation model — this is the central methods decision.** A 50 kHz readout that cannot resolve events closer than τ_d = 1/50 kHz = 20 µs is a **dead-time problem**. Standard models (Knoll, *Radiation Detection and Measurement*, ch. 4; Usman & Patil review, Nucl. Eng. Tech. 50, 1006 (2018)):

- Non-paralyzable: observed rate m = Γ/(1 + Γτ_d), saturates at 1/τ_d = 50 kHz.
- Paralyzable: m = Γ e^{−Γτ_d}, *rolls over* and decreases above Γ = 1/τ_d.
- **Binned-Bernoulli (recommended here):** a bandwidth-limited digitizer effectively reports "≥1 event" per resolvable window Δt: m = (1/Δt)(1 − e^{−ΓΔt}). This matches the "max resolvable tunneling rate ~25 kHz" spec (mean observed rate at Γ→∞ is 1/Δt; the *unambiguously invertible* range ends near Γ ≈ 1/(2Δt) ≈ 25 kHz where the exponential flattens). **Recommendation:** implement the observation model as an explicit MC censoring step (merge events within τ_d) so the paralyzable/non-paralyzable choice is *derived* from the stated electronics behavior rather than assumed; then fit with the matching analytic inverse Γ̂ = −ln(1 − m̂Δt)/Δt.

**Energy estimators (implement both, compare):**

1. **Count-based (linear regime):** Ê ∝ N_observed with the dead-time correction above; variance from Poisson statistics plus template-shape uncertainty. Valid while peak Γ ≲ 25 kHz — i.e., for the low-energy (CEvNS) part of the spectrum. Fisher-information analysis of the inhomogeneous-Poisson likelihood `ln L = Σ ln Γ(t_i;E) − ∫Γ(t;E)dt` gives the optimal template fit and the resolution floor (σ_E/E ~ 1/√N for pure counting).
2. **Time-over-saturation (nonlinear regime):** for muon-scale deposits Γ_peak ≫ 25 kHz and counts saturate; energy information survives in the *duration* of saturation. Since n_qp decays ~exponentially (τ_qp), t_sat ≈ τ_qp ln(Γ_peak/Γ_thr) — a **logarithmic energy estimator**, exactly analogous to time-over-threshold reconstruction in saturated TES/SNSPD/PMT channels. Resolution comes from τ_qp knowledge and the fluctuation of the decay; multi-sensor redundancy (1/mm² array → most sensors saturated for muons) improves it as √N_sensors. Note interaction with Domain 3: in this regime τ_qp is itself density-dependent (Rothwarf–Taylor), so the estimator must use the nonlinear decay solution, not a fixed exponential.

**Pileup between physical events:** at O(1 Hz) muons and ≪1 Hz CEvNS with ms-scale pulses, event-to-event pileup probability is ~10⁻³ — handle with a simple exclusion window; no pileup deconvolution machinery needed. Within-event pileup *is* the saturation problem above.

**EMG handling:** the EMG jitter smears the template Γ(t;E); since EMG has closed-form pdf and cdf, fold it analytically into the template (convolution of the two-exponential pulse with EMG is analytic term-by-term) rather than sampling it only in MC — this keeps the likelihood fit consistent with the generator.

**Method class:** forward MC (sample deposits from Domains 1–2 → per-sensor Poisson event trains → bandwidth censoring → reconstruction) plus analytic likelihood cross-check on the estimator bias/variance. The final deliverable — dR/dE_reconstructed — is the forward-MC histogram; the analytic response matrix R(E_rec|E_dep) built from the same model is the cheap way to iterate.

---

## Computational Tools

| Tool | Version | Purpose | Notes |
| --- | --- | --- | --- |
| Python + NumPy/SciPy | ≥3.11 / current | quadrature (flux folding), ODEs, stats | `scipy.integrate.quad`, `solve_ivp` for RT equations |
| pylandau (or custom Landau sampler) | current | Landau/Vavilov straggling sampling | validate against PDG MPV formula before trusting |
| numba (optional) | current | accelerate event-level MC loops | only if >10⁷ events needed |
| matplotlib | current | spectra | — |

No Geant4, no G4CMP, no CRY — per project spec and per the "small custom MC" recommendations above. Reactor spectrum tables (Huber, Mueller, summation) are published as digitized tables in the source papers/supplements; store them as CSV inputs with provenance noted.

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
| --- | --- | --- |
| Huber–Mueller + summation below 1.8 MeV | Full summation model (Estienne–Fallot) everywhere | If low-recoil shape systematics dominate the conclusions; summation has no conversion-anomaly baggage but larger per-branch uncertainties |
| Gaisser–Guan analytic flux | CRY / CORSIKA / PARMA-EXPACS | If secondaries, altitude/latitude dependence, or showers matter; PARMA is the best drop-in if a site-specific flux is later required |
| Landau/Vavilov sampling per chord | Geant4 full transport | If δ-ray escape or muon-induced secondaries in the crystal must be quantified |
| Anchor-paper linear pulse model | Full Rothwarf–Taylor ODEs | Mandatory for muon-scale deposits (nonlinear recombination); optional elsewhere |
| Binned-Bernoulli censoring derived from MC | Pure paralyzable/non-paralyzable analytic formulas | Fine for quick sensitivity scans; do not use for the final response matrix |

## What NOT to Use

| Avoid | Why | Use Instead |
| --- | --- | --- |
| Lindhard/ionization quenching factor | No ionization channel in a pure phonon calorimeter; importing QF double-counts | Direct recoil→phonon with few-% defect-storage systematic |
| Plain Gaisser at E < 100/cosθ GeV | Overestimates low-energy flux, wrong at large zenith | Gaisser–Guan modified formula (exact form above) |
| Mean dE/dx for per-event deposits | Straggling dominates the deposit spectrum shape in cm-scale absorbers | Landau/Vavilov MPV + fluctuation sampling |
| Moyal approximation for the final result | Underestimates the Landau high-energy tail | True Landau/Vavilov |
| Fixed τ_qp for muon deposits | Recombination is bimolecular at high n_qp; fixed τ biases time-over-saturation energy scale | Density-dependent decay (RT solution) |
| Assuming non-paralyzable dead time a priori | The stated electronics behavior may be paralyzable-like; wrong model biases rates near 25 kHz by O(10%) | Derive censoring from an explicit event-merging MC |

## Method Selection by Problem Type

**CEvNS spectrum (deposits ~10 eV–few keV):** deterministic flux folding (Domain 1) → linear QPD pulse model (Domain 3) → count-based estimator (Domain 4, regime 1). Everything analytic except the final censoring MC.

**Muon spectrum (deposits ~5–100+ MeV):** flux+geometry+straggling MC (Domain 2) → nonlinear (RT) QP dynamics (Domain 3) → time-over-saturation estimator (Domain 4, regime 2). The reconstructed-energy axis for muons is effectively logarithmically compressed — expect this to dominate the reconstructed-spectrum morphology.

**Joint reconstructed spectrum:** build one response matrix R(E_rec|E_dep) spanning both regimes from the same forward model; apply to both source spectra. The crossover region (roughly where peak Γ_in crosses ~25 kHz; back out the corresponding E_dep from K, the efficiency chain, and Δ_tr early — it is a key design number) needs the most careful treatment.

## Validation Strategy by Method

| Method | Validation Approach | Key Benchmarks |
| --- | --- | --- |
| Freedman cross section | Closed-form total σ in the M ≫ E limit: σ_tot(E_ν) = G_F² Q_W² E_ν²/(4π); check code integral against it to <0.1% | σ(Ge, 4 MeV) ~ 10⁻⁴⁰ cm² order-of-magnitude; E² scaling |
| Full rate folding | Compare integrated counts/kg/day above threshold with published CONUS+ Ge predictions (3.6 GW_th at 20.7 m; Nature 2025 / arXiv:2501.05206 and arXiv:2501.18550), rescaled by P_th/L² | O(10) counts/kg/day scale, threshold-dependent |
| Helm form factor | F(0) = 1; F² > 0.998 at reactor q for Ge (turning it off must not change the answer) | Lewin–Smith parameterization |
| Gaisser–Guan flux | Vertical intensity ≈ 70 m⁻²s⁻¹sr⁻¹; horizontal-surface flux ≈ 1 cm⁻²min⁻¹; overlay against data compilation in Frontiers 9:750159 | PDG cosmic-ray review |
| Chord MC | Cauchy ⟨ℓ⟩ = 4V/S under isotropic flux (unit test); crystal muon rate ~O(0.5–1) Hz | analytic chord distribution for a box |
| Straggling | MPV of sampled deposits vs PDG Δ_p formula; κ-regime check (Vavilov vs Landau) | PDG Passage-of-Particles review, Bichsel |
| QPD pulse model | Reproduce anchor-paper example: 200 meV deposit, η ≈ 0.3, Δ_tr = 100 µeV → ~600 trapped QPs; peak-time and area of two-exponential vs closed form | Ramanathan et al. Eq. 4 and Fig-level numbers |
| RT nonlinearity | Linear-model limit recovered as n₀ → 0; bimolecular decay n(t) = n₀/(1+R̃n₀t) reproduced by ODE solver | Rothwarf–Taylor 1967 limits |
| Censoring/dead-time | MC event-merging vs analytic m(Γ) curves for all three models; estimator bias vs true Γ across 1–100 kHz | Knoll ch. 4; saturation at 50 kHz, invertibility to ~25 kHz |
| End-to-end | Inject δ-function E_dep lines, verify R(E_rec|E_dep) is normalized and its linear-regime diagonal matches the 50% efficiency spec | closure test |

## Sources

**Verified directly this session (fetched):**
- Ramanathan et al., APS Open Science 1, 000013 (2026), DOI 10.1103/kqd2-spb1 / arXiv:2405.17192 — pulse model, Γ_in = K n_qp with K ≈ 16 E_J k_B T/(𝒩Δh), efficiency chain values, Al/Hf trapping design, Kaplan-based downconversion assumptions.
- Guan et al., arXiv:1509.06176 — modified Gaisser formula, exact parameters P₁–P₅ as quoted above.

**Verified via search results (titles/abstracts confirmed; equations cross-checked against background knowledge):**
- De Romeri et al., arXiv:2501.18550 — CONUS+/TEXONO Ge CEvNS framework; form-factor insensitivity at reactor energies.
- Huber, PRC 84, 024617 (arXiv:1106.0687); Mueller et al., PRC 83, 054615 (arXiv:1101.2663); Kopeikin et al., arXiv:2103.01684; flux-model reviews arXiv:2110.06820, arXiv:2310.13070.
- Daya Bay fuel evolution, PRL 130, 211801.
- PDG "Passage of Particles Through Matter" (rpp2022) — Bethe, MPV/Landau/Vavilov formulas; Landau-history review arXiv:2209.06387.
- Muon flux model comparison: Frontiers in Energy Research 9, 750159.
- SuperCDMS defect energy loss, arXiv:1805.09942; defect-production notes arXiv:0907.0342; Ge QF measurement arXiv:2202.03754 (context only — QF not used).
- Rothwarf & Taylor, PRL 19, 27 (1967); Kaplan et al., PRB 14, 4854 (1976); Kozorezov et al., downconversion (PRB 61, 11807) — framework confirmed via secondary literature this session.
- Dead time/pileup: Usman & Patil, Nucl. Eng. Tech. 50, 1006 (2018) (ScienceDirect S1738573318302596); Knoll, *Radiation Detection and Measurement* (4th ed.), ch. 4 [textbook, background knowledge].

**Background knowledge, flagged for phase-level verification:**
- Lewin & Smith Helm parameters; per-isotope fission energies (Ma et al. PRC 88, 014605); Vogel–Engel PRD 39, 3378; bulk gap values for Ta/Al/Hf; Ge dE/dx numeric value; 2×10²⁰ ν̄/s/GW_th anchor.

---

_Methods research for: reactor-CEvNS + muon reconstructed-energy spectra in a QPD-instrumented 1 kg Ge crystal_
_Researched: 2026-07-20_
