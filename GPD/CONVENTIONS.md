# Conventions Ledger

**Project:** QPD Particle-Physics Potential — Stage-1 Reconstructed-Energy Spectra
**Created:** 2026-07-20
**Last updated:** 2026-07-20 (Phase 1)
**Authoritative lock:** `GPD/state.json` -> `convention_lock`
**Projection status:** synced

> This file is a human-readable projection of `state.json.convention_lock`, not the source
> of truth. When a convention changes, update the lock through `gpd convention set ...`,
> then refresh this projection with rationale, test values, and supersession notes. Do not
> hand-edit this file into disagreement with the lock.

**Provenance:** These conventions were proposed in an interactive-mode pass (subfield: reactor
CEvNS + cosmic-ray muons + superconducting quasiparticle sensors — a detector/nuclear-physics
pipeline, NOT relativistic field theory) and are now USER-APPROVED. They satisfy requirement
CONV-01 and Phase-1 success criteria in `GPD/ROADMAP.md`.

**Subfield note:** This project is a detector-response / rate-calculation pipeline. The standard
QFT convention categories (metric signature, Fourier transform pair, gamma-matrix basis,
gauge/covariant-derivative sign, generator normalization) do **not** arise — there is no
relativistic field-theory computation anywhere in the chain. They are recorded explicitly as
"N/A" (Section H) so their absence is auditable rather than merely omitted.

---

## A. Unit System

### A.1 Input/Output units (detector practical)

| Field            | Value                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------- |
| **Convention**   | Energies in eV / keV / MeV; differential rate in counts·kg⁻¹·day⁻¹·keV⁻¹; time in s; length in cm / µm |
| **Introduced**   | Phase 1                                                                                  |
| **Rationale**    | Matches the benchmark literature (Billard 2017, CONUS+, PDG) and how detector spectra are reported |
| **Test value**   | A reactor-CEvNS differential rate is quoted as e.g. 0.76 counts·kg⁻¹·day⁻¹ above 50 eV_nr (Billard Table 1 form) |

### A.2 Internal units (cross section)

| Field            | Value                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------- |
| **Convention**   | Natural units ħ = c = 1 used internally for the CEvNS cross section only                 |
| **Introduced**   | Phase 1                                                                                  |
| **Conversion**   | (ħc)² = 3.894×10⁻²⁸ GeV²·cm²  (equivalently 1 GeV⁻² = 3.894×10⁻²⁸ cm²)                    |
| **Rationale**    | G_F is naturally expressed in GeV⁻²; the cross section comes out in GeV⁻² and must be converted to cm² with (ħc)². Dropping (ħc)² is the single most common CEvNS bug. |
| **Test value**   | σ expressed as G_F²Q_W²E_ν²/4π in GeV⁻², multiplied by (ħc)² = 3.894×10⁻²⁸ GeV²·cm², yields cm² |

### A.3 Boltzmann constant

| Field            | Value                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------- |
| **Convention**   | k_B kept **explicit** (NOT set to 1)                                                     |
| **Introduced**   | Phase 1                                                                                  |
| **Rationale**    | Superconducting gaps and temperatures appear directly (mK / µeV); keeping k_B explicit avoids conflating temperature and energy in the QP-dynamics bookkeeping |
| **Test value**   | Temperatures/gaps carried in mK / µeV; k_B appears explicitly in factors such as K ≈ 16 E_J k_B T/(𝒩Δh) |

**Dimension map (I/O, SI-practical):** energy, time, length, temperature are all independent
dimensioned quantities. Natural units (ħ = c = 1, so [length] = [time] = [energy]⁻¹) are used
ONLY inside the cross-section evaluation and are converted back to cm² before any rate is formed.

---

## B. Unified Energy-Scale Chain (core of CONV-01)

| Field            | Value                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------- |
| **Convention**   | A **single unified phonon energy scale with NO ionization quenching** for BOTH nuclear-recoil (CEvNS) and electron-recoil (muon, Compton) deposits |
| **Chain**        | T ≡ E_nr  →  E_ph  →  E_dep  →  E_rec                                                    |
| **Introduced**   | Phase 1                                                                                  |
| **Rationale**    | A fieldless phonon calorimeter has no ionization channel and no Luke gain, so the full recoil thermalizes to phonons. NR and ER deposits therefore land on the SAME scale. Applying Lindhard/ionization quenching would suppress CEvNS ~5–7× and is physically wrong here. |

**Chain definitions:**

- **T ≡ E_nr** — nuclear-recoil kinetic energy (CEvNS). `T` and `E_nr` are the same quantity.
- **E_ph = E_dep − E_stored(defects)** — phonon energy. Defect (Frenkel) storage is a few-%
  NR-only correction, and is **ZERO for muons and Compton (electron-recoil) deposits**.
- **E_dep** — deposited energy delivered to the lattice (full recoil/ionization energy; no quenching).
- **E_rec** — reconstructed energy, the output of the QPD estimator and the project's observable axis.
  Low-energy limit: **E_rec ≈ 0.5·E_dep**.

**FORBIDDEN (guarded proxies):**
- Any mixing of keVee / keVnr scales.
- Applying Lindhard or any ionization/quenching factor on this phonon scale.

**Test value:** A 1 keV nuclear recoil and a 1 keV electron recoil land at the SAME E_dep.
In the low-energy limit, E_rec(1 keV E_dep) = 0.5 keV for both.

---

## C. CEvNS Cross-Section Convention

| Field            | Value                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------- |
| **Differential**| dσ/dT = (G_F² M / 4π) · Q_W² · (1 − M T / 2E_ν²) · F²(q²)                                  |
| **Prefactor**    | **/4π** (NOT /8π) — the /8π form is a factor-of-2 error                                   |
| **Weak charge**  | Q_W = N − (1 − 4 sin²θ_W) Z                                                              |
| **Mixing angle** | sin²θ_W = 0.2387 (low-energy MS-bar value; NOT 0.2312 at M_Z)                            |
| **Proton coupling** | 1 − 4 sin²θ_W = 0.0452 (near-vanishing → rate ∝ N² to ~0.5%)                          |
| **Form factor**  | F(q²) = Helm; q = √(2MT); F(0) = 1. At reactor q for Ge, F² > 0.998 (form-factor-independent regime) |
| **Closed form**  | σ_tot = G_F² Q_W² E_ν² / 4π                                                              |
| **Introduced**   | Phase 1                                                                                  |
| **Rationale**    | Freedman (1974) SM cross section with Helm form factor; the /4π prefactor and low-energy sin²θ_W are the standard reactor-CEvNS choices used by the benchmark literature |

**CANONICAL Phase-3 unit-test target (contradiction C2 resolved):**
- **Primary target (FULL Q_W):** σ(Ge, E_ν = 4 MeV) ≈ **1.0×10⁻⁴⁰ cm²** using the full weak charge
  Q_W = N − (1 − 4 sin²θ_W) Z.
- **N-only quick-check:** σ(Ge, 4 MeV) ≈ **1.1×10⁻⁴⁰ cm²** (specifically 1.08×10⁻⁴⁰ with Q_W → N = 40),
  with a ~20% tolerance. This is a coarse cross-check, not the primary target.
- **Coefficient form:** σ ≈ **4.22×10⁻⁴⁵ N² (E_ν/MeV)² cm²**.

> Contradiction note: an earlier research file (PITFALLS.md) quoted a ~10⁻⁴² cm² "ballpark"
> — that is off by ~100× and must NOT be used as a validation target (it would "validate" a
> code that is 100× too low). The first-principles value above is correct.

**Dimensional check:** [G_F²] = GeV⁻⁴, [M] = GeV, [E_ν²] = GeV², so [G_F² M E_ν²] = GeV⁻¹ =
[dσ/dT]·[T] consistency after the (ħc)² conversion → cm². Q_W², the kinematic factor, and F²
are dimensionless. ✓

**Test value:** With Q_W → N = 40, E_ν = 4 MeV: 4.22×10⁻⁴⁵ × 40² × 4² = 4.22×10⁻⁴⁵ × 1600 × 16
= 1.08×10⁻⁴⁰ cm². With the full Q_W (Q_W = 40 − 0.0452×32 = 38.55, Q_W²/N² = 0.929): ≈ 1.00×10⁻⁴⁰ cm². ✓

---

## D. Detector / Normalization Constants

| Quantity                    | Value                            | Notes                                         |
| --------------------------- | -------------------------------- | --------------------------------------------- |
| Ge atoms per kg             | 8.29×10²⁴ atoms/kg               | 1000 g / 72.63 g·mol⁻¹ × N_A                   |
| Ge density                  | 5.323 g/cm³                      |                                               |
| Ge molar mass               | 72.63 g/mol                      | natural isotopic abundance                    |
| Wafer dimensions            | 4″×4″×2 mm                        | = 20.65 cm³ ≈ 110 g                            |
| Wafer mass                  | ≈ 110 g                          | 20.65 cm³ × 5.323 g/cm³                        |
| Sensors                     | ~10,300                          | 1/mm² on ONE instrumented face                |
| Reactor thermal power       | 3 GW_th (thermal, NOT electric)  | GW_e vs GW_th is a ~×3 trap                    |
| Standoff distance           | 25 m                             |                                               |
| Reactor ν̄ flux at detector  | ~7–8×10¹² ν̄·cm⁻²·s⁻¹              | DERIVED, consistent with CONUS+ scaling       |

**Geometry normalization convention:**
- Adopt the **110 g wafer geometry everywhere** for the physical detector.
- **KEEP per-kg rate normalization** (counts·kg⁻¹·day⁻¹) for benchmark comparison against
  Billard/CONUS+ predictions.
- The "1 kg crystal" framing that appears in `GPD/literature/SUMMARY.md` header is **STALE** —
  do not propagate it. (SUMMARY.md predates the geometry revision; PROJECT.md/ROADMAP.md are current.)

**Test value:** 1000 g ÷ 72.63 g/mol × 6.022×10²³ = 8.29×10²⁴ Ge atoms/kg.
Wafer: 10.16 cm × 10.16 cm × 0.2 cm = 20.65 cm³; × 5.323 g/cm³ = 109.9 g ≈ 110 g. ✓

---

## E. Efficiency Mapping (E_dep → n_qp) — contradiction C3 resolved

| Field            | Value                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------- |
| **Convention**   | ε ≈ 0.5 deposited-to-signal efficiency, imposed as a forward-model definition            |
| **Design dependence** | SAME baseline value (0.5) for both designs, carrying a ±10–20% design-dependent band |
| **Refinement**   | Ta→Al and Al→Hf MAY be refined to distinct per-design numbers in Phase 5 if the tunneling-parameter mapping warrants |
| **Cross-reference** | The paper's physical estimate η_ce ≈ 0.3 (f_loss ~ 0.35) is documented as an INDEPENDENT cross-reference, NOT the baseline |
| **Introduced**   | Phase 1                                                                                  |
| **Rationale**    | ε = 0.5 is a project-imposed definition (100% phonon collection × ph→QP losses), not a derived quantity. It is distinct from the paper's physical η_ce ≈ 0.3 — this is definitional, not a conflict. |

> Consistency note vs ROADMAP.md success criterion 3: the roadmap phrases this as "Ta→Al and
> Al→Hf do not share one efficiency." The approved resolution is compatible: both designs START
> from the same ε ≈ 0.5 baseline carrying a ±10–20% design-dependent band, and MAY diverge to
> distinct per-design values in Phase 5. The band, not a single shared number, is the binding object.

**Test value:** E_rec(low-E) ≈ ε · E_dep = 0.5 · E_dep, i.e. a 1 keV deposit → ~0.5 keV
reconstructed in the linear regime.

---

## F. Bandwidth-Censoring Convention — contradiction C1 (partially resolved; OPEN switch)

| Field            | Value                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------- |
| **Resolving time (LOCKED)** | 25 kHz maximum resolvable tunneling rate ⇒ **40 µs** (Nyquist from 50 kHz bandwidth). The 50 kHz sampling itself corresponds to **20 µs** — state BOTH clearly. |
| **Censoring rule (OPEN SWITCH)** | Paralyzable-vs-non-paralyzable AND merge-vs-drop kept as an EXPLICIT CODE SWITCH — NOT fixed now |
| **Introduced**   | Phase 1                                                                                  |
| **Rationale**    | The resolving time is fixed by the electronics (Nyquist). The dead-time model (paralyzable vs non-paralyzable) and event-handling (merge vs drop) cannot be fixed from electronics reasoning alone, so both variants must remain implementable rather than silently chosen. |

> ⚠️ **OPEN QUESTION — BLOCKS Phase 5.** The paralyzable-vs-non-paralyzable and merge-vs-drop
> choice is recorded as an explicit switch, not a decision. Both variants MUST be implementable
> in the Phase-5 response-matrix code. This open question must be resolved before the Phase-5
> saturation definition can be finalized. Do NOT silently pick one. (Matches ROADMAP.md Phase-1
> risk and backtracking trigger, and SUMMARY.md open question "censoring rule".)

**Time values:** 1 / 25 kHz = 40 µs (Nyquist resolving time); 1 / 50 kHz = 20 µs (sampling interval).

**Test value:** A tunneling-rate transient whose peak Γ exceeds 25 kHz enters the saturated
regime; below 25 kHz the linear count-based estimator applies. The crossover deposit energy
(where peak Γ = 25 kHz) is a Phase-5 design number to be computed per design.

---

## G. Symbol Registry (binding notation dictionary)

Adopted **verbatim** from the `GPD/literature/SUMMARY.md` "Unified Notation" table as the binding
symbol dictionary for all downstream work.

| Symbol            | Quantity                                | Units / Dimensions                | Convention notes                                                            |
| ----------------- | --------------------------------------- | --------------------------------- | -------------------------------------------------------------------------- |
| T ≡ E_nr          | Nuclear-recoil kinetic energy           | keV_nr / eV_nr                    | T = E_nr (unified). Never map to keVee without an explicit quenching model (forbidden here). |
| E_dep             | Deposited energy in crystal             | MeV (muons), keV/eV (CEvNS)       | Full recoil/ionization energy delivered to the lattice.                    |
| E_ph              | Phonon energy                           | same as E_dep                     | E_ph = E_dep − E_stored(defects); defect storage few-% NR-only, ZERO for muons/Compton. |
| E_rec             | Reconstructed energy                    | eV/keV/MeV                        | QPD estimator output; the observable axis. Low-E limit E_rec ≈ 0.5·E_dep.  |
| dσ/dT             | CEvNS differential cross section        | cm²/keV                           | (G_F²M/4π)Q_W²(1 − MT/2E_ν²)F²(q²). Prefactor /4π, not /8π.                 |
| Q_W               | Weak nuclear charge                     | dimensionless                     | Q_W = N − (1 − 4 sin²θ_W)Z; proton coupling ~vanishes → rate ∝ N².          |
| sin²θ_W           | Weak mixing angle                       | dimensionless                     | Low-energy value 0.2387 (MS-bar), not 0.2312 (M_Z). State scheme when comparing to precision fits. |
| F(q²)             | Helm nuclear form factor                | dimensionless                     | q = √(2MT); F(0) = 1; F² > 0.998 at reactor q for Ge.                       |
| Φ(E_ν)            | Reactor ν̄ flux                          | ν̄·cm⁻²·s⁻¹·MeV⁻¹                  | per-fission spectra × fission rate × 1/(4πL²).                              |
| dI/dE_μ dΩ        | Muon differential flux                  | cm⁻²·s⁻¹·sr⁻¹·GeV⁻¹               | Gaisser–Guan; track sr explicitly. I_v ≈ 70 m⁻²s⁻¹sr⁻¹.                     |
| ⟨dE/dx⟩           | Muon stopping power in Ge               | 1.370 MeV·cm²·g⁻¹ (≈7.3 MeV/cm)   | Use the straggling distribution, not the mean, for the deposit spectrum.    |
| ℓ                 | Chord length through crystal            | cm                                | Cauchy ⟨ℓ⟩ = 4V/S under isotropic flux (unit-test invariant).              |
| n_qp, Γ_in        | QP density; tunneling rate per sensor   | µm⁻³; Hz                          | Γ_in ≈ K·n_qp, K ≈ 16 E_J k_B T/(𝒩Δh).                                     |
| τ_inj, τ_qp       | QP injection / recombination times      | s (µs–ms)                         | Two-exponential pulse (paper Eq. 4); τ_qp density-dependent at muon scale.  |
| Δ_abs, Δ_tr       | Absorber / trap superconducting gaps    | µeV                               | Ta≈700, Al≈180–190, Hf≈20–60; trapping needs Δ_abs/Δ_tr ≳ 2–4. Film gaps as parameters. |
| ε, η              | Deposit→signal efficiency               | dimensionless                     | Baseline ε ≈ 0.5 (imposed); paper physical estimate η_ce ≈ 0.3 (cross-ref).  |
| τ_d, Δt           | Readout dead / resolving time           | 20 µs (=1/50 kHz), 40 µs (=1/25 kHz) | Saturation ceiling; see Section F for the 20 µs vs 40 µs distinction.     |

---

## H. QFT Convention Categories — N/A (no field-theory computation)

The canonical field-theory convention categories are recorded as N/A so their absence is
auditable. This is a detector/rate-calculation pipeline with no relativistic field theory,
no propagators, no spinors, and no gauge fields.

| Category                    | Status | Note                                                              |
| --------------------------- | ------ | ----------------------------------------------------------------- |
| Metric signature            | N/A    | No relativistic field theory; CEvNS kinematics uses non-relativistic recoil relations. |
| Fourier convention          | N/A    | No momentum-space field computation. (FFTs in signal processing, if any, are DSP conventions, not field-theory Fourier pairs.) |
| Gamma-matrix basis          | N/A    | No Dirac spinors in the pipeline.                                 |
| Gauge / covariant-derivative sign | N/A | No gauge fields.                                                |
| Generator normalization     | N/A    | No non-abelian algebra.                                           |
| Regularization scheme       | N/A    | Tree-level SM cross section; no loops.                            |
| Renormalization scheme      | N/A (partial) | Tree-level SM. The only scheme-dependent input is sin²θ_W, fixed to the low-energy MS-bar value 0.2387 (see Section C). |

---

## Numerical Factor Registry

Factors whose value depends on a convention choice; the consistency-checker uses these to verify
derivations.

| Factor Source | Correct value here | Common error | Determined by |
| ------------- | ------------------ | ------------ | ------------- |
| CEvNS prefactor | /4π | /8π (×2 too small) | Section C cross-section convention |
| (ħc)² conversion | 3.894×10⁻²⁸ GeV²·cm² | omitted (cross section left in GeV⁻²) | Section A.2 unit system |
| Weak mixing angle | sin²θ_W = 0.2387 (low-E) | 0.2312 (M_Z) → wrong Q_W | Section C |
| Proton coupling | 1 − 4 sin²θ_W = 0.0452 | using ≈0 or wrong sin²θ_W | Section C |
| Reactor power | 3 GW_th | GW_e (×~3 too small) | Section D |
| Efficiency | ε ≈ 0.5 (baseline) | η_ce ≈ 0.3 used as baseline | Section E |
| Low-E reconstruction | E_rec ≈ 0.5·E_dep | E_rec = E_dep (no ε) | Sections B, E |
| Resolving time | 40 µs (25 kHz Nyquist) | 20 µs (50 kHz sampling) conflated | Section F |
| Recoil scale | keV_nr (phonon scale, no quenching) | keVee (Lindhard applied) → CEvNS ×5–7 too small | Section B |

---

## Reference Convention Maps

| Reference | Convention(s) used | Conversion needed |
| --------- | ------------------ | ----------------- |
| Freedman (1974), PRD 9, 1389 | SM CEvNS dσ/dT, /4π prefactor | None — matches Section C |
| Billard et al. (2017), Table 1 | Ge phonon energy scale, NO quenching, counts·kg⁻¹·day⁻¹ | None — same energy variable a QPD measures; rescale flux (3 GW_th, 25 m) only |
| CONUS+ (Nature 643, 1229 (2025)) | eV_ee (ionization scale) | Needs a quenching model to compare to our phonon scale — cross-check only, NOT a direct match |
| Huber (2011) / Mueller (2011) | ν̄ per-fission spectra, E_ν > 2 MeV | None for >2 MeV; sub-1.8 MeV requires summation + n-capture (Phase 2) |
| PDG Cosmic Rays review | I_v ≈ 70 m⁻²s⁻¹sr⁻¹, ~1 cm⁻²min⁻¹ | None — track sr explicitly |
| Ramanathan et al. (2026) | efficiency chain η_ph/η_pb/η_tr (η_ce ≈ 0.3), pulse Eq. 4 | η_ce ≈ 0.3 is a cross-reference; our baseline is the imposed ε ≈ 0.5 (Section E) |

---

## Cross-Convention Consistency Check

Verified interacting pairs (all within the detector/rate domain; no QFT pairs apply):

| Convention A | Convention B | Required relation | Status |
| ------------ | ------------ | ----------------- | ------ |
| Unified phonon scale (B) | Efficiency ε (E) | E_rec ≈ ε·E_dep = 0.5·E_dep at low E; both NR and ER deposits use the same map | ✓ consistent |
| Natural units internal (A.2) | CEvNS prefactor /4π (C) | σ in GeV⁻² → ×(ħc)² → cm²; dimensionally σ_tot = G_F²Q_W²E_ν²/4π · (ħc)² | ✓ consistent |
| sin²θ_W = 0.2387 (C) | Q_W = N − (1−4sin²θ_W)Z (C) | 1 − 4×0.2387 = 0.0452 | ✓ consistent |
| Per-kg normalization (D) | 110 g wafer geometry (D) | rates quoted per-kg for benchmark, physical detector is 110 g | ✓ consistent (dual bookkeeping, explicitly documented) |
| Resolving time 40 µs (F) | E_dep→E_rec saturation (B, F) | saturation onset when peak Γ > 25 kHz (1/40 µs) | ✓ consistent |
| k_B explicit (A.3) | QP tunneling K ∝ k_B T (G) | k_B appears explicitly in Γ_in ≈ K·n_qp | ✓ consistent |

No internal inconsistencies found. The one genuinely OPEN item is the paralyzable-vs-non-paralyzable /
merge-vs-drop switch (Section F), recorded as a switch and flagged as blocking Phase 5 — NOT an
inconsistency, but an undetermined choice preserved as an explicit code switch by design.

---

## Change Log

| Date | Change | Rationale |
| ---- | ------ | --------- |
| 2026-07-20 | Initial establishment (Phase 1, CONV-01). Sections A–H locked; C1 censoring switch left OPEN. | User-approved convention set from interactive-mode proposal. |
