# Known Pitfalls Research

**Domain:** Reactor CEvNS + sea-level muon rate prediction in reconstructed energy for a 1 kg Ge crystal read out by quasiparticle-poisoning detectors (QPDs; Ta→Al and Al→Hf designs)
**Researched:** 2026-07-20
**Confidence:** HIGH (reactor flux, CEvNS conventions, muon flux); MEDIUM (defect-loss magnitudes, QPD saturation behavior — anchor paper does not fully specify saturation model)

Scope note: this file covers pitfalls in four areas: (1) reactor CEvNS rate prediction, (2) recoil-energy bookkeeping in phonon detectors, (3) QP-sensor response modeling, (4) sea-level muon estimates. Project constants assumed: 3 GW_th reactor at 25 m, natural Ge, sensor density 1/mm², ~50% deposited-energy-to-signal efficiency, 50 kHz bandwidth (max resolvable tunneling rate ~25 kHz), EMG-profiled bursts, no G4CMP.

## Critical Pitfalls

### Pitfall 1: Using a conversion-method reactor spectrum (Huber-Mueller) below the IBD threshold

**What goes wrong:**
The Huber/Mueller conversion spectra are constructed from ILL beta-spectrum measurements and are only defined/validated for E_nu ≳ 2 MeV. Most reactor antineutrinos (~60-70% by number) have E_nu < 1.8 MeV and have never been directly measured. Naively extrapolating conversion spectra to low energy, or truncating at 1.8 MeV, corrupts the low-recoil CEvNS prediction — exactly where a meV-threshold QPD detector has its rate.

**Why it happens:**
Huber-Mueller is the "default" reactor flux in most CEvNS codes and papers because IBD experiments never needed the sub-threshold part.

**How to avoid:**
Use a summation (ab initio) calculation for E_nu < 2 MeV (e.g., the approach in arXiv:2302.10460 / PRD 108, 033002 (2023), or the CONFLUX framework, arXiv:2503.18966), and explicitly add the non-fission components: beta decays following neutron capture on ²³⁸U (²³⁹U, ²³⁹Np chains, E_nu ≲ 1.3 MeV) and captures on accumulated fission fragments. Assign a generous (≳10-20%) uncertainty band to the sub-2-MeV region; it is model, not data.

**Warning signs:**
Predicted spectrum has a discontinuity or hard cutoff near E_nu = 1.8-2 MeV; low-recoil CEvNS rate insensitive to the neutron-capture component; quoted flux uncertainty below 5% at low E_nu.

**Kinematic quantification for this project:** E_nu,min(T) ≈ sqrt(M T/2). For natural Ge (M ≈ 67.7 GeV), a 10 eV recoil requires only E_nu ≳ 0.58 MeV, and neutrinos below the 1.8 MeV IBD threshold populate all recoils T ≲ 96 eV (T_max = 2E_nu²/(M+2E_nu)). The sub-IBD flux dominates the lowest reconstructed-energy bins that QPDs are designed to reach.

**Phase to address:** Reactor flux model phase.

---

### Pitfall 2: Flux-per-fission normalization chain errors (thermal power → fission rate → flux)

**What goes wrong:**
Order-1 errors from any of: (a) using electric instead of thermal power (~×3); (b) wrong energy-per-fission; (c) double-counting "~6 neutrinos per fission" on top of a spectrum already normalized per fission; (d) MeV↔J unit slips; (e) 1/(4πL²) with L in the wrong unit or with diameter instead of radius.

**Why it happens:**
The normalization is a chain of 4-5 conversions, each with a convention.

**How to avoid:**
- Fission rate R_f = P_th / Σ_i f_i ⟨E_f⟩_i where f_i are fission fractions and ⟨E_f⟩_i is the *effective thermal* energy release per fission (includes neutron-capture gammas in reactor materials, excludes the ~9 MeV carried away by antineutrinos). Standard values (Kopeikin-type / Ma et al. evaluations): ≈202 MeV (²³⁵U), ≈206 MeV (²³⁸U), ≈210-211 MeV (²³⁹Pu), ≈214 MeV (²⁴¹Pu). Do not use the *total* Q-value (~207-215 MeV including neutrinos) here.
- The summation/conversion spectra S_i(E_nu) are in neutrinos per fission per MeV; their integral is already ~6-7 nu/fission. Never multiply by 6 again.
- Sanity anchor: a 3 GW_th core emits ~6×10²⁰ nu/s; at 25 m, Φ ≈ 6×10²⁰/(4π(2500 cm)²) ≈ 7-8×10¹² nu/cm²/s. Any pipeline result far from this is wrong.
- Use burnup-averaged fission fractions (typical PWR mid-cycle: f_235 ≈ 0.55-0.60, f_239 ≈ 0.28-0.30, f_238 ≈ 0.07-0.08, f_241 ≈ 0.05) and state them.

**Warning signs:**
Flux differs from the 7×10¹² cm⁻²s⁻¹ anchor by more than ~2×; rate predictions differ from published Ge-at-reactor predictions (CONUS/NUCLEUS-type configurations, scaled by power/distance) by more than a factor ~2.

**Phase to address:** Reactor flux model phase (unit-tested normalization function).

---

### Pitfall 3: CEvNS cross-section convention traps (Q_w definition, factor 4 vs 8, sin²θ_W value)

**What goes wrong:**
Factor-of-2/4 errors from mixing conventions. The standard form is
dσ/dT = (G_F² M / 4π) · Q_w² · (1 − T/E_nu − M T / (2E_nu²)) · F²(q²), with Q_w = N − (1 − 4 sin²θ_W) Z.
Some references instead write G_F² M/(8π) with Q_w defined including an extra factor of 2, or absorb Q_w²/4 into a "weak charge" with different normalization. Mixing the two gives ×4 or ×1/4 rate errors. A second trap: using sin²θ_W(M_Z) = 0.2312 vs the low-energy running value ≈0.2387 (small here, since the proton coupling nearly vanishes either way, but be consistent when comparing to precision analyses such as arXiv:2605.27121).

**Why it happens:**
Literature genuinely uses both conventions; the kinematic factor also appears in truncated form (1 − MT/2E_nu²), which is fine at reactor energies but differs at percent level.

**How to avoid:**
Fix ONE convention in a conventions document. Validate the implemented dσ/dT against two independent anchors: (a) the coherent total cross section σ ≈ G_F² Q_w² E_nu² / (4π) in the E_nu ≪ M limit; (b) a published number, e.g., reproduce the predicted Ge CEvNS rate from a published reactor-Ge analysis (CONUS+ / Dresden-II predictions) within stated flux differences.
Unit discipline: with G_F = 1.1664×10⁻⁵ GeV⁻², multiply by (ħc)² = 0.3894 GeV²·mbarn = 3.894×10⁻²⁸ GeV²·cm² to get cm². Omitting (ħc)² is the single most common CEvNS unit bug.

**Warning signs:**
Total σ at E_nu = 4 MeV not in the ~1×10⁻⁴⁰ cm² ballpark for Ge (first-principles: σ = G_F²Q_w²E²/4π ≈ 4.2×10⁻⁴⁵·N²·(E_ν/MeV)² cm² → ≈1.1×10⁻⁴⁰ cm² for Ge at 4 MeV; an earlier draft of this note mistakenly quoted ~10⁻⁴², which is 100× too low — do not use it as the validation target); rate off by exactly 4× from a published benchmark signals a Q_w /4π-vs-/8π convention slip.

**Phase to address:** Cross-section implementation phase (dimensioned unit tests).

---

### Pitfall 4: "N² scaling" misuse and lumped-A treatment of natural germanium

**What goes wrong:**
Two related errors. (a) Treating the per-kg rate as ∝ N²: the cross section per nucleus scales ~N², but atoms per kg ∝ 1/A and the recoil endpoint T_max ≈ 2E_nu²/M ∝ 1/A, so above a fixed detector threshold the per-mass rate scaling is much weaker than N² and can even invert. (b) Computing the Ge spectrum with a single averaged A = 72.63 instead of abundance-weighting the five isotopes: ⁷⁰Ge (20.5%), ⁷²Ge (27.4%), ⁷³Ge (7.8%), ⁷⁴Ge (36.5%), ⁷⁶Ge (7.7%). Each isotope has different N (38-44, ~±8% in Q_w²… actually ~±15% in N²) and a different endpoint (e.g., at E_nu = 8 MeV: T_max ≈ 1.96 keV for ⁷⁰Ge vs 1.81 keV for ⁷⁶Ge). Lumped-A smooths real per-isotope endpoint structure and biases the near-endpoint and near-threshold spectrum.

**Why it happens:**
The "coherent N² enhancement" slogan; averaged atomic masses are convenient.

**How to avoid:**
Compute dR/dT per isotope (correct N_i, Z, M_i, atoms/kg_i = x_i N_A ×1000/A_bulk with x_i the number abundance) and sum. Number of Ge atoms per kg natural Ge: 8.29×10²⁴. ⁷³Ge spin: the axial/spin-dependent contribution is ~1/N² suppressed and negligible for rate prediction — state this rather than silently ignoring it.

**Warning signs:**
Spectrum endpoint is a single sharp cutoff instead of a stepped superposition; claimed rate advantage over lighter targets quoted as (N_Ge/N_Si)² without threshold discussion.

**Phase to address:** Cross-section/target-model phase.

---

### Pitfall 5: Over- or under-worrying about the nuclear form factor and neutron radius

**What goes wrong:**
Two opposite failure modes. (a) Spending effort on Helm vs Klein-Nystrand vs neutron-skin modeling: at reactor energies q = sqrt(2MT) ≲ 16 MeV (T ≲ 2 keV in Ge), F²(q²) deviates from 1 by well under 1%, and form-factor/neutron-radius uncertainties are demonstrated to be irrelevant for reactor CEvNS (arXiv:1902.07398, JHEP 06 (2019) 141: relevant only for q ≳ 20-50 MeV). (b) Importing a form-factor routine tuned for COHERENT (stopped-pion, q ~ 30-70 MeV) with a wrong q-unit convention (fm⁻¹ vs MeV vs GeV) — a wrong-unit form factor CAN produce a large spurious suppression even at reactor energies.

**How to avoid:**
Include the Helm form factor with standard Ge parameters for completeness, verify F²(q_max) > 0.99 across the reactor-recoil domain, and freeze it. Unit-test that F(0) = 1 and that q is built as sqrt(2 M T) in consistent units.

**Warning signs:**
Form factor differing from 1 by >1% below 2 keV recoil; sensitivity of the predicted rate to R_n at the >0.1% level.

**Phase to address:** Cross-section implementation phase.

---

### Pitfall 6: Applying ionization quenching (Lindhard) to a phonon-only energy scale

**What goes wrong:**
Multiplying the nuclear-recoil energy by a Lindhard ionization yield (~0.15-0.25) to get the "detected" energy. In an *unbiased* phonon calorimeter (this project: QPDs read athermal phonons; no Neganov-Trofimov-Luke bias), essentially the full recoil energy thermalizes into phonons regardless of the electronic/nuclear partition — the electron-hole pairs recombine and return their energy to the phonon system. Applying Lindhard suppresses the predicted nuclear-recoil spectrum by ~5-7× and shifts the CEvNS energy scale disastrously. Conversely, the *muon* (electron-recoil) and CEvNS (nuclear-recoil) deposits land on the *same* phonon energy scale here — do not put muons in "keVee" and recoils in "keVnr."

**Why it happens:**
Most Ge CEvNS literature (CONUS, Dresden-II, TEXONO) uses ionization detectors where the quenching factor is central, and the keVee/keVnr distinction is deeply embedded in the field. Note also that the Ge quenching factor itself is contested at low energy (arXiv:2202.03754 vs comment arXiv:2203.00750; anomalously high yield at 254 eVnr, arXiv:2405.10405; cryogenic-temperature deviations) — a further reason not to import it where it does not belong.

**How to avoid:**
Define one energy bookkeeping chain: true recoil energy T → phonon energy E_ph = T − E_stored(defects) → sensor signal = η(position, E) × E_ph. Quenching enters nowhere. Only use Lindhard if cross-checking against published ionization-detector spectra (then convert *their* eVee axis, not yours).

**Warning signs:**
Any appearance of "eVee" in the CEvNS pipeline; predicted CEvNS rate ~5× below a phonon-detector benchmark.

**Phase to address:** Detector-response phase; energy-scale definition must be written down before any spectrum is produced.

---

### Pitfall 7: Ignoring (or over-modeling) Frenkel-defect energy storage at the lowest recoil energies

**What goes wrong:**
A nuclear recoil can store part of its energy in lattice defects (Frenkel pairs), which never appears as phonons. Displacement threshold energies in Ge span ~7-30 eV (direction-dependent). MD-based studies (arXiv:2210.01550; PRD 106, 063012 (2022); SuperCDMS ²⁰⁶Pb result arXiv:1805.09942) find the *fractional* stored energy is largest — up to ~10-20% — for recoils of tens of eV to ~1 keV, exactly the reactor-CEvNS window, and drops to zero below the displacement threshold (sub-threshold recoils give 100% of energy to phonons). Ignoring this biases the reconstructed-energy mapping for CEvNS recoils; conversely, treating it as a precise known function overstates knowledge — MD values carry large model spread.

**Why it happens:**
The effect is invisible in ionization measurements and only ~percent-to-tens-of-percent in phonon energy, so it's often dropped.

**How to avoid:**
Include a defect-loss term as a *systematic band* (e.g., 0-15% loss for 20 eV-2 keV recoils, zero below ~2×E_d), not a point estimate. Also note the reverse process: delayed relaxation of stress/defects can *release* energy later (low-energy-excess hypothesis, arXiv:2112.14495; stress-induced phonon bursts, Nature Comm. 15, 6444 (2024); neutron-damage phonon bursts, arXiv:2603.17964) — a candidate background at the lowest energies, not a signal.

**Warning signs:**
CEvNS reconstructed-energy spectrum claimed to <5% accuracy below 100 eV without a defect-loss systematic; unexplained low-energy event excess treated as CEvNS.

**Phase to address:** Detector-response phase (energy bookkeeping); uncertainty budget phase.

---

### Pitfall 8: Treating the 50% deposited-energy-to-signal efficiency as constant (position, energy, and time independent)

**What goes wrong:**
Phonon collection efficiency in phonon-mediated detectors is not a constant: it is set by competition between absorption in active sensors vs losses to mounting contacts, "dead" (non-instrumented) metal, and surface down-conversion of phonons below the pair-breaking threshold 2Δ of the absorber film. The QPD anchor paper (Ramanathan et al., APS Open Science 1, 000013 (2026), DOI 10.1103/kqd2-spb1 / arXiv:2405.17192) itself estimates η_ce ≈ 0.3 dominated by mounting losses (f_loss ~ 0.35), with a literature range η ~ 0.1-0.4, and warns that "care must be taken to properly understand the f_loss term across different architectures." Position dependence: events near the instrumented surface feed sensors before down-conversion; events near mounting points lose more. A flat 50% is a *definition* for this project's forward model, but presenting reconstructed spectra without an efficiency-variation systematic misstates the resolution and energy-scale uncertainty.

**Why it happens:**
Constant efficiency makes convolution trivially separable.

**How to avoid:**
Keep η = 0.5 as the baseline per the project spec, but propagate a position/energy-dependent variation (e.g., ±10-20% event-to-event spread) as a resolution-like smearing term and as an energy-scale systematic. Note the Ta/Al/Hf gap hierarchy: phonons that down-convert below 2Δ_absorber are lost; Al (Δ ≈ 0.18 meV) collects lower-energy phonons than Ta (Δ ≈ 0.7 meV), so the two designs do NOT share one efficiency number by default.

**Warning signs:**
Reconstructed-energy resolution reported as purely statistical (counting) with no collection-variance term; identical response assumed for Ta→Al and Al→Hf designs.

**Phase to address:** Detector-response phase.

---

### Pitfall 9: Quasiparticle-poisoning background treated as independent per-sensor Poisson noise

**What goes wrong:**
Quiescent QP tunneling in superconducting devices has two components: a steady poisoning rate (residual density n₀ ~ 0.01-1 μm⁻³ in Al per the qubit literature; the QPD paper shows even n₀ = 0.05 μm⁻³ in the absorber concentrates to ~0.15 μm⁻³ in the trap) and *correlated bursts* from environmental radioactivity — muons and gammas depositing energy in the substrate produce phonon bursts that elevate tunneling rates across MANY sensors simultaneously (Wilen et al., Nature 594, 369 (2021); Cardani et al., Nat. Comm. 12, 2733 (2021); McEwen et al., Nat. Phys. 18, 107 (2022); gamma-irradiation study arXiv:2503.07354; phonon-only correlated poisoning arXiv:2503.09554). Modeling background as independent per-sensor Poisson noise underestimates the low-energy background pile-down from muon/gamma events and misses that at sea level, the muon "background" and the QP-poisoning burst background are largely the SAME events entering through different bookkeeping.

**Why it happens:**
Independence is the natural first model; correlations require event-level simulation.

**How to avoid:**
Simulate backgrounds at event level: each muon/gamma deposit creates a crystal-wide phonon burst → correlated multi-sensor tunneling. Use multi-sensor coincidence as the discriminator (this is also what makes the muon spectrum measurable). Keep a separate steady n₀ term for true quiescent poisoning (IR photons, residual sources — cf. arXiv:2606.07339 for how low shielded baselines can go).

**Warning signs:**
Background model with zero inter-sensor correlation; sea-level quiescent rates taken from underground/shielded qubit measurements without rescaling.

**Phase to address:** Sensor-response phase + background-model phase (shared event generator with muon phase).

---

### Pitfall 10: Saturation and aliasing of the tunneling-rate energy estimator at high energy (the muon end of the spectrum)

**What goes wrong:**
The project's energy estimator is a tunneling rate capped at ~25 kHz per sensor (50 kHz bandwidth). A through-going muon deposits ~40 MeV mean in a ~5.7 cm Ge path (MIP ⟨dE/dx⟩ ≈ 1.37 MeV cm²/g × 5.32 g/cm³ ≈ 7.3 MeV/cm) — some 10⁷-10⁸ times a CEvNS recoil. Even spread over ~3×10³ sensors (1/mm² on a ~33 cm² face), per-sensor tunneling rates during the burst vastly exceed 25 kHz: rates above the cap alias/censor to the ceiling, so reconstructed energy compresses. Naive forward models produce a fake "peak" at the saturation ceiling that is an instrument artifact, not a Landau feature. Additional subtleties from the anchor paper: CPB-style devices have asymmetric tunneling (an occupied island blocks further entry — a per-sensor dead-time/occupancy effect), and QP recombination is quadratic in density, so signal vs energy is sublinear at high density even below the rate cap.

**Why it happens:**
Linear rate→energy conversion validated at low energy gets extrapolated seven orders of magnitude.

**How to avoid:**
Build the rate→energy response as an explicit saturating function per sensor (EMG burst amplitude × occupancy/dead-time × 25 kHz cap), and forward-fold. Present the muon spectrum in reconstructed energy with the saturation region clearly delimited; validate the estimator's linear range and quote where it ends. Check limiting cases: at low energy the response must reduce to linear; at high energy total reconstructed energy must plateau near (N_sensors_hit × cap × burst duration × energy-per-tunnel).

**Warning signs:**
Reconstructed muon spectrum extends linearly to tens of MeV; no plateau/pile-up feature despite a hard 25 kHz cap; mean and MPV of the muon deposit used interchangeably (Landau mean > MPV; use the full straggling + path-length distribution, not ⟨dE/dx⟩ × length).

**Phase to address:** Sensor-response phase (this is the project's central modeling deliverable); validation phase for limiting cases.

---

### Pitfall 11: Sea-level muon flux normalization and angular bookkeeping errors

**What goes wrong:**
Classic factor traps: (a) confusing vertical *intensity* I_v ≈ 70 m⁻²s⁻¹sr⁻¹ (E_μ > 1 GeV) with the *flux through a horizontal surface* J ≈ 1 muon cm⁻²min⁻¹ ≈ 170 m⁻²s⁻¹ — they differ by the ∫cos²θ·cosθ dΩ projection integral; (b) forgetting the cosθ projection factor when integrating I(θ) = I_v cos²θ over solid angle (for cosⁿθ intensity, J_horiz = 2πI_v/(n+2)); (c) counting only the top face of a small 3D crystal — for a ~5.7 cm cube the side faces add a non-negligible contribution from inclined muons; (d) using the Gaisser formula at low energy: it is valid only for E_μ ≳ 100/cosθ GeV and θ < 70°, and *overestimates* the flux in the few-GeV regime that dominates sea-level rates — use a modified parameterization (Guan et al., arXiv:1509.06176) or a data-driven model (see the model comparison in Front. Energy Res. 9, 750159 (2021)); (e) the cos²θ shape itself is only exact near ~3 GeV — steeper at lower E_μ, flatter at higher.

**Why it happens:**
"1 per cm² per minute" and "cos²θ" are memorized without their qualifiers.

**How to avoid:**
Monte Carlo the geometry: sample the horizontal-flux distribution correctly (pdf ∝ cosⁿθ · cosθ · sinθ in θ), track path lengths through the actual crystal shape, and cross-check the integrated rate: ~0.5-1 Hz through a 1 kg Ge cube is the sanity anchor (33 cm² top face × ~1/cm²/min ≈ 0.55 Hz plus side-face contributions).

**Warning signs:**
Muon rate on the crystal off from ~0.5-1 Hz by >2×; rate independent of crystal orientation; flux quoted in m⁻²s⁻¹ compared against numbers in m⁻²s⁻¹sr⁻¹.

**Phase to address:** Muon-flux phase (unit-tested angular integrals).

---

### Pitfall 12: Ignoring muon secondaries, showers, and coincident deposits

**What goes wrong:**
Counting only through-going primary muons. At sea level the electromagnetic soft component (electrons/photons, ~tens of MeV) has a number flux comparable to muons; muons also produce delta rays and bremsstrahlung in the cryostat, shielding, and crystal, giving (a) additional lower-energy deposits not on the muon Landau band, (b) *coincident* multi-deposit events (muon + delta ray, muon + shower fragment) that alter the reconstructed-energy spectrum shape, and (c) stopped muons (μ⁻ capture / μ⁺ decay, ~Michel electrons up to 53 MeV). For a QPD readout, any of these also acts as a correlated QP-poisoning burst (see Pitfall 9). Cryogenic detectors' long pulse/recovery times relative to a 0.5-1 Hz muon rate can also produce event pile-up in the reconstruction window.

**Why it happens:**
Small-detector estimates default to "muon flux × area."

**How to avoid:**
Include at minimum: path-length + Landau straggling for primaries, a soft-component/secondary term (either from a parametrized sea-level electron/photon flux or a conservative scaling), and a pile-up model given the burst duration and 0.5-1 Hz rate. State explicitly what is excluded (e.g., hadronic component, neutron-induced recoils — note neutrons produce *nuclear* recoils that fall exactly in the CEvNS signal region and are the dominant surface background for reactor CEvNS; if out of scope, say so prominently).

**Warning signs:**
Muon reconstructed spectrum has no low-energy tail below the Landau band; zero events between the CEvNS region and the muon band; background claims made for the CEvNS region based on muons alone.

**Phase to address:** Muon-flux phase; scope-definition in roadmap (neutron background in/out of scope must be an explicit decision).

---

## Approximation Shortcuts

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
| --- | --- | --- | --- |
| Truncate reactor spectrum at 1.8 MeV (IBD-validated region only) | Uses well-validated flux | Wipes out lowest-recoil CEvNS bins (T ≲ 96 eV), the QPD flagship region | Only for a "conservative floor" variant, clearly labeled |
| Single lumped A = 72.63 for Ge | One integral instead of five | Wrong endpoints, smoothed spectrum near threshold; ~% level rate error | Order-of-magnitude estimates only |
| F(q²) = 1 (no form factor) | Simpler code | <1% at reactor energies | Acceptable for reactor CEvNS if stated; NOT for any COHERENT cross-check |
| Constant η = 0.5 collection efficiency | Separable convolution | Underestimated resolution/energy-scale systematic | Baseline OK (project spec), but must carry a variation systematic |
| Zero defect-energy loss | Simpler energy bookkeeping | Up to ~10-20% energy-scale bias for 20 eV-1 keV recoils | Only with an explicit systematic band covering it |
| Linear tunneling-rate→energy map | Trivial reconstruction | Completely wrong above saturation; fake spectral features | Only below the validated linear range (low-energy CEvNS region) |
| ⟨dE/dx⟩ × path for muon deposits | No straggling sampling | Overestimates typical deposit (mean ≫ MPV for thin absorbers) | Never for spectrum shape; OK for total-power estimates |
| Gaisser formula at few GeV | Familiar closed form | Overestimates sea-level flux where it matters most | Never below ~100/cosθ GeV; use modified Gaisser (1509.06176) |
| Muons only (no secondaries/neutrons) | Small event generator | Missing low-energy tail; unquantified CEvNS-region background | Only with explicit scope statement |

## Convention Traps

| Convention Issue | Common Mistake | Correct Approach |
| --- | --- | --- |
| CEvNS prefactor and Q_w definition | Mixing G_F²M/4π with Q_w = N−(1−4s²_W)Z against G_F²M/8π forms with rescaled Q_w → ×4 or ×1/4 | Fix one convention; unit-test against σ ≈ G_F²Q_w²E_nu²/4π and one published Ge rate |
| Natural-unit conversion | Dropping (ħc)² when converting GeV⁻² → cm² | Multiply by (ħc)² = 3.894×10⁻²⁸ GeV²·cm²; assert σ units in tests |
| sin²θ_W value | Using 0.2312 (M_Z) in a low-energy analysis comparing to papers using 0.2387 | State the value and scheme; effect is small but must be consistent for precision comparisons |
| Kinematic factor | (1−MT/2E²) vs (1−T/E−MT/2E²) silently different between codes | Pick full form; document |
| q in form factor | q in fm⁻¹ fed to a routine expecting MeV (or vice versa) | Build q = sqrt(2MT) with explicit units; assert F(0)=1, F²>0.99 at 2 keV |
| Spectrum normalization | Multiplying per-fission spectrum (already ∫≈6 nu/fission) by 6 again | Spectrum is nu/fission/MeV; only multiply by fission rate and 1/4πL² |
| Energy per fission | Total Q (~207-215 MeV, incl. neutrinos) instead of effective thermal (~202-214 MeV, excl. neutrinos, incl. capture gammas) | Use effective thermal release per isotope, fission-fraction weighted |
| Reactor power | GW_e instead of GW_th (~×3) | 3 GW_th per project spec; label all powers |
| Per-nucleus vs per-kg | Using N_A/A with A in amu but mass in g without the ×1000; or per-mole-of-nucleons | 8.29×10²⁴ Ge atoms per kg natural Ge; unit-test this constant |
| eVnr vs eVee | Applying quenching to a phonon energy scale, or mixing muon (ER) and CEvNS (NR) scales | Single phonon-energy scale; quenching only for external ionization-detector comparisons |
| Muon flux vs intensity | Comparing J (m⁻²s⁻¹, horizontal surface) with I_v (m⁻²s⁻¹sr⁻¹) | Track sr explicitly; J_horiz = 2πI_v/(n+2) for cosⁿθ |
| "1/cm²/min" qualifier | Applying the E>1 GeV horizontal-surface number to all muons/all faces | State energy cutoff and surface orientation; MC the 3D geometry |

## Numerical Traps

| Trap | Symptoms | Prevention | When It Breaks |
| --- | --- | --- | --- |
| Coarse E_nu grid near the recoil threshold E_min(T)=sqrt(MT/2) | Jagged/biased dR/dT at low T | Log-spaced E_nu grid; adaptive quadrature near E_min | Steeply falling flux × threshold kinematics, i.e., everywhere below ~100 eV |
| Cubic-spline interpolation of tabulated summation spectra | Negative flux values between table points; ringing at the 5 MeV bump | Monotone (PCHIP) interpolation in log-flux | Sparse tables, spectrum kinks (bump, endpoint) |
| Per-isotope endpoints in a shared T grid | Spurious steps or smoothing at T_max,i | Integrate each isotope on its own kinematic domain, then sum | Near-endpoint region (1.8-2.0 keV) |
| Saturating-rate simulation with naive Poisson sampling | Rates > bandwidth produced then clipped inconsistently between sensors | Simulate parity flips in time domain with dead-time/occupancy; cap = detection, not generation | Any deposit ≳ keV-scale; all muon events |
| EMG burst convolution normalization | Total reconstructed energy depends on time-bin width | Normalize EMG to unit integral analytically; test energy closure on synthetic events | Fine time binning, long tails |
| Landau sampling for muons | Mean of sampled deposits ≫ MPV, spectrum shifted | Sample Landau/Vavilov (or Bichsel-like) straggling per path length; verify MPV against PDG | Thin paths (short chords through crystal corners) |
| Angular MC sampling | Using pdf ∝ cos²θ instead of ∝ cos²θ·cosθ·sinθ for horizontal-flux sampling | Derive the sampling pdf from the flux definition; validate against analytic J_horiz | Always (silent ~30% bias) |
| Rate closure across pipeline | Total predicted counts differ between differential and integrated code paths | Closure test: ∫dR/dT dT vs direct rate integral, per isotope | After any refactor |

## Interpretation Mistakes

| Mistake | Risk | Prevention |
| --- | --- | --- |
| Reading saturation-ceiling pile-up in the reconstructed muon spectrum as a physical peak | Fake "feature" reported; wrong dynamic-range conclusions | Delimit the saturated region; show true-vs-reconstructed mapping explicitly |
| Comparing this phonon-scale CEvNS spectrum to ionization-detector (eVee) spectra without conversion | Apparent 5-7× discrepancies; wrong validation verdict | Convert axes explicitly; document quenching model used for the *other* experiment |
| Treating the sub-IBD flux prediction as validated | Overconfident low-bin rates; ~10-20% model uncertainty presented as <5% | Carry separate uncertainty bands above/below 1.8 MeV |
| Attributing all low-energy background to QP poisoning noise | Misses correlated burst background = muons/gammas; double-counts when muon spectrum added | One shared event generator for muons feeding both "signal" (muon spectrum) and "background" (burst) channels |
| Ignoring that surface neutron-induced nuclear recoils mimic CEvNS exactly | CEvNS "detectability" claims that would not survive contact with data | Explicit scope statement; cite neutron background as dominant caveat (cf. arXiv:2212.14148) |
| Assuming Ta→Al and Al→Hf designs share one response | Wrong per-design spectra; gap hierarchy (Δ_Ta ≈ 0.7 meV, Δ_Al ≈ 0.18 meV, Δ_Hf ≈ 0.02 meV) changes phonon acceptance, trap depth, and burst kinetics | Separate response parameters per design from the start |
| 5 MeV bump treated as resolved physics or ignored entirely | Percent-level spectral shape bias in 4-7 MeV E_nu (recoil shape above ~500 eV) | Include as a shape systematic; note unresolved origin (NEOS/Daya Bay PRL 118, 042502) |

## Publication Pitfalls

| Pitfall | Impact | Better Approach |
| --- | --- | --- |
| Quoting one rate without the flux-model dependence | Result not comparable to CONUS/NUCLEUS-style predictions | Report with two flux models (summation baseline + HM-above-2MeV variant) |
| Not stating the energy-scale definition (phonon energy, no quenching) | Readers assume eVee; apparent factor ~5 disagreement | Conventions section defining T, E_ph, E_reconstructed and all efficiencies |
| Presenting reconstructed spectra without the response matrix | Irreproducible; unfolding temptation downstream | Publish/plot the true→reconstructed mapping and saturation boundary alongside spectra |
| Claiming CEvNS sensitivity without the neutron/secondary background caveat | Credibility risk with reactor-CEvNS community | Explicit background scope statement |
| Muon rate without geometry/orientation definition | Unreproducible ±50% differences | State crystal dimensions, orientation, flux model, and energy cutoff |

## "Looks Correct But Is Not" Checklist

- [ ] **CEvNS rate integral:** Often missing the (ħc)² conversion or double-counting nu/fission — verify total flux ≈ 7×10¹² cm⁻²s⁻¹ at 25 m from 3 GW_th, and rate against a published Ge prediction scaled by power/distance.
- [ ] **Low-recoil spectrum:** Often missing the sub-IBD and neutron-capture flux — verify the T < 96 eV bins respond when the sub-1.8 MeV flux is toggled.
- [ ] **Isotope sum:** Often missing per-isotope endpoints — verify five distinct T_max values appear (1.81-1.96 keV at E_nu = 8 MeV).
- [ ] **Energy bookkeeping:** Often quietly applies Lindhard — verify a 1 keV nuclear recoil and a 1 keV electron recoil reconstruct to the same energy (minus the NR defect-loss band).
- [ ] **Sensor response at high energy:** Often linear extrapolation — verify reconstructed energy plateaus for injected deposits ≫ saturation and reduces to linear at low energy.
- [ ] **Muon angular integral:** Often missing the cosθ projection — verify J_horiz = πI_v/2 analytically for cos²θ before trusting the MC.
- [ ] **Muon deposit spectrum:** Often uses mean dE/dx — verify the MPV of the simulated deposit distribution sits below the mean by the expected Landau offset.
- [ ] **Background correlation:** Often independent-Poisson sensors — verify a single injected muon lights up spatially correlated sensors in the sim.

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
| --- | --- | --- |
| Wrong cross-section convention discovered late | LOW | Single constant fix + rerun; prevented cheaply by early benchmark test |
| Quenching wrongly applied to phonon scale | MEDIUM | Redefine energy chain, regenerate all spectra; all downstream plots invalid |
| Flux truncated at IBD threshold | LOW-MEDIUM | Swap in summation table below 2 MeV; regenerate low-T bins |
| Linear response used for muons | HIGH | Requires building the time-domain saturation model that should have existed; all muon results redone |
| Muon angular bookkeeping error | LOW | Fix sampling pdf; rates shift ~30%, rerun MC |
| Uncorrelated background model | MEDIUM-HIGH | Restructure background sim around event-level generator shared with muon pipeline |

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
| --- | --- | --- |
| 1, 2 (flux model, normalization) | Reactor flux phase | Flux anchor test (7×10¹² cm⁻²s⁻¹); toggle test of sub-IBD component |
| 3, 4, 5 (cross-section conventions, isotopes, form factor) | Cross-section phase | Closed-form σ limit test; published-rate benchmark; per-isotope endpoint check |
| 6, 7 (energy bookkeeping, defects) | Detector-response phase (first deliverable: energy-scale definition doc) | ER/NR same-scale test; defect-band systematic in uncertainty budget |
| 8 (efficiency constancy) | Detector-response phase | Resolution budget includes collection-variance term; per-design (Ta/Al vs Al/Hf) parameters |
| 9 (correlated poisoning) | Sensor-response + background phase | Injected-muon correlation test across sensors |
| 10 (saturation/aliasing) | Sensor-response phase | Low-energy linearity + high-energy plateau limiting-case tests |
| 11, 12 (muon flux, secondaries) | Muon-flux phase | Analytic J_horiz check; 0.5-1 Hz crystal-rate anchor; scope statement for neutrons/secondaries |

## Sources

Reactor flux and CEvNS below IBD threshold:
- Hayen & Kostensalo (eds.) review: "Reactor antineutrino flux and anomaly," arXiv:2310.13070 (Prog. Part. Nucl. Phys. 2024) — anomaly status, HM vs summation, 5 MeV bump.
- "How to measure the reactor neutrino flux below the inverse beta decay threshold with CEvNS," arXiv:2302.10460, PRD 108, 033002 (2023) — sub-IBD spectrum modeling, neutron-capture component unobservability.
- Kopeikin et al., "Components of antineutrino emission in nuclear reactor," Phys. At. Nucl. 67, 1892 (2004) — six emission components incl. ²³⁹U/²³⁹Np capture chains.
- "Neutron capture and the antineutrino yield from nuclear reactors," PRL 116, 122503 (2016) — flux-dependent low-energy excess nuclides.
- CONFLUX flux framework, arXiv:2503.18966. Reevaluation of ²³⁵U/²³⁹Pu ratio: arXiv:2103.01684. NEOS/Daya Bay bump isotope analysis: PRL 118, 042502 (2017).

Cross-section, form factor, Ge parameters:
- Aristizabal Sierra, De Romeri, Rojas, "Impact of form factor uncertainties on CEvNS interpretations," JHEP 06 (2019) 141, arXiv:1902.07398 — form-factor irrelevance at reactor q.
- "Refined extraction of electroweak and nuclear parameters from germanium CEvNS data," arXiv:2605.27121 — Q_w/sin²θ_W conventions, Ge neutron radius.
- Neutron-capture recoil backgrounds at reactors: arXiv:2212.14148.

Quenching / recoil bookkeeping / defects:
- Bonhomme et al., Ge quenching measurement, EPJC 82, 815 (2022), arXiv:2202.03754; critical comment arXiv:2203.00750 — unresolved QF systematics.
- 254 eVnr ionization measurement (above-Lindhard yield), arXiv:2405.10405. CDMSlite photo-neutron yield: arXiv:2202.07043; ⁸⁸Y/Be: arXiv:1608.03588.
- SuperCDMS, "Energy loss due to defect formation from ²⁰⁶Pb recoils," arXiv:1805.09942, APL 113, 092101 (2018).
- "Energy loss due to defect creation in solid state detectors," arXiv:2210.01550; "Energy loss in low energy nuclear recoils in dark matter detector materials," PRD 106, 063012 (2022); low-energy excess from crystal defects, arXiv:2112.14495.
- Stress-induced phonon bursts and QP poisoning, Nat. Commun. 15 (2024), DOI 10.1038/s41467-024-50173-8; neutron-damage phonon bursts, arXiv:2603.17964.

QPD / quasiparticle sensors:
- Ramanathan et al., "Quantum parity detectors: a qubit-based particle-detection scheme with meV thresholds," APS Open Science 1, 000013 (2026), DOI 10.1103/kqd2-spb1, arXiv:2405.17192 — η_ce ≈ 0.3, f_loss ~ 0.35, n₀ trap concentration, QP injection burst model, Fano-factor caveat, CPB tunneling asymmetry. Follow-up device characterization: arXiv:2509.18637.
- Wilen et al., Nature 594, 369 (2021); Cardani et al., Nat. Commun. 12, 2733 (2021); McEwen et al., Nat. Phys. 18, 107 (2022) — correlated radiation-induced QP bursts.
- QP poisoning under active gamma irradiation, arXiv:2503.07354; phonon-only correlated poisoning, arXiv:2503.09554; IR-shielding suppression of poisoning, arXiv:2606.07339.

Muons:
- Guan et al., "A parametrization of the cosmic-ray muon flux at sea-level," arXiv:1509.06176 — modified Gaisser valid at low energy.
- Cecchini & Spurio, "Atmospheric muons: experimental aspects," arXiv:1208.1171 — angular distribution energy dependence, measurement systematics (30-35% inter-experiment spread).
- "A comparison of muon flux models at sea level," Front. Energy Res. 9, 750159 (2021).
- Synchronous cosmic-ray detection in qubit arrays, arXiv:2402.03208 — sea-level muon-qubit coincidence rates.
- PDG Cosmic Rays review (vertical intensity, 1 cm⁻²min⁻¹ anchor, cos²θ domain of validity).

---

_Known pitfalls research for: reactor CEvNS + muon spectra in reconstructed energy for QPD-instrumented Ge_
_Researched: 2026-07-20_
