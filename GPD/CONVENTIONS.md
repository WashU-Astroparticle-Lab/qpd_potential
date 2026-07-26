# Conventions Ledger

**Project:** QPD Particle-Physics Potential — Stage-1 Reconstructed-Energy Spectra
**Created:** 2026-07-20
**Last updated:** 2026-07-25 (Section E.1, energy-scale calibration slope — USER DECISION)
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
  It is an **estimator of E_dep**, not the collected signal. Low-energy limit:
  **E_rec ≈ E_dep** (unit calibration slope, §E.1, revised 2026-07-25; was 0.5·E_dep).
  Above the saturation onset E_rec is genuinely sub-linear and is never unfolded back.

**FORBIDDEN (guarded proxies):**
- Any mixing of keVee / keVnr scales.
- Applying Lindhard or any ionization/quenching factor on this phonon scale.

**Test value:** A 1 keV nuclear recoil and a 1 keV electron recoil land at the SAME E_dep.
In the low-energy (unsaturated) limit, E_rec(E_dep) = E_dep for both — e.g. a 10 eV deposit
reconstructs at ~10 eV. (A 1 keV deposit is already past the 32 eV saturation onset and lands
lower; the unit slope is a statement about the *linear* regime only. See §E.1.)

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
| **Convention**   | ε ≈ 0.5 deposited-to-signal efficiency, imposed as a forward-model definition. **ε is a PHYSICAL conversion fraction, not the energy scale — see §E.1 (revised 2026-07-25).** |
| **Design dependence** | SAME baseline value (0.5) for both designs, carrying a ±10–20% design-dependent band |
| **Refinement**   | Ta→Al and Al→Hf MAY be refined to distinct per-design numbers in Phase 5 if the tunneling-parameter mapping warrants |
| **Cross-reference** | The paper's physical estimate η_ce ≈ 0.3 (f_loss ~ 0.35) is documented as an INDEPENDENT cross-reference, NOT the baseline |
| **Introduced**   | Phase 1                                                                                  |
| **Rationale**    | ε = 0.5 is a project-imposed definition (100% phonon collection × ph→QP losses), not a derived quantity. It is distinct from the paper's physical η_ce ≈ 0.3 — this is definitional, not a conflict. |

> Consistency note vs ROADMAP.md success criterion 3: the roadmap phrases this as "Ta→Al and
> Al→Hf do not share one efficiency." The approved resolution is compatible: both designs START
> from the same ε ≈ 0.5 baseline carrying a ±10–20% design-dependent band, and MAY diverge to
> distinct per-design values in Phase 5. The band, not a single shared number, is the binding object.

### E.1 Energy-scale calibration slope — ε is NOT the energy scale (REVISED 2026-07-25)

| Field            | Value                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------- |
| **Convention**   | `params.CALIB_SLOPE` = **1.0** = dE_rec/dE_dep in the **linear** regime                  |
| **Supersedes**   | The Phase-1 calibration slope = ε = 0.5, and the former §E test value "a 1 keV deposit → ~0.5 keV reconstructed" |
| **Introduced**   | **USER DECISION 2026-07-25**                                                             |
| **Applies at**   | `response.calibrate_C` (the single global count→energy constant C), `energy_scale.E_rec_estimator` |
| **Rationale**    | E_rec is an **estimator of the deposited energy**, not the collected signal. ε is the *physical* deposit→quasiparticle conversion fraction; a real detector is calibrated on a known line, and that calibration **absorbs ε into C**. A 10 eV deposit must reconstruct at 10 eV. |
| **What ε still does** | ε keeps its full physical role in the forward chain: `energy_scale.n_qp_yield`, `saturation_onset_energy`, and the trigger all still use `params.EPSILON` = 0.5. Only the *energy scale* is decoupled from it. |
| **Guard**        | `fp-unfold-saturation` — the slope corrects the **scale only**. The sub-linear response **above** the saturation onset is genuine information loss and is **NEVER** unfolded away. Calibration makes the linear regime 1:1; it does not make E_rec = E_dep everywhere. |

**Test value:** E_rec(low-E) ≈ `CALIB_SLOPE` · E_dep = E_dep, i.e. a 1 keV deposit → ~1 keV
reconstructed **in the linear regime** (Al→Hf saturation onset = 32.1 eV_dep, so a 1 keV deposit is
already saturated and lands lower — the unit slope is asserted at low E, where no sensor saturates).

> **Consequence for frozen v2.0 artifacts.** Every E_rec-axis deliverable built before 2026-07-25
> carries the old ε=0.5 scale and is superseded: `artifacts/v2.0/response_matrix_*_ext.npz` and the
> `*_dRdErec_*` CSVs were rebuilt. `artifacts/stage1/` v1.0 matrices are **not** rebuilt — they are
> the frozen comparison baseline (`fp-overwrite-v1-matrices`). Milestone-record E_rec numbers in
> ROADMAP/STATE (RoI rates, band edges) were quoted on the old axis; see §E.2.

### E.2 What moved, measured

| Quantity | old axis (ε=0.5) | new axis (unit slope) |
| --- | --- | --- |
| 10 eV deposit reconstructs at | 4.76 eV | ~9.5 eV (5% of the shift is real onset roll-in, not calibration) |
| ⁷³Ge 102.59 eV resonance kinematic edge (5.50 eV_dep) | 2.67 eV_rec | ~5.35 eV_rec |
| ⁶⁸Ge K EC line (10.368 keV_dep) | 2.39 keV_rec | ~4.79 keV_rec (the residual factor ~2.2 is **real saturation**) |
| "10–100 eV reconstructed RoI" in deposit terms | 20–200 eV_dep | 10–100 eV_dep |

The last row is the substantive one: the project's RoI is natively a **deposit** window
(`neutron_recoil.ROI_LO_eV/ROI_HI_eV` = 10/100 eV on the recoil axis, GPD/PROJECT "the 10–100 eV
RoI"), and under the old scale applying it to E_rec silently selected a 20–200 eV deposit band. The
two windows now agree.

---

## F. Bandwidth-Censoring Convention — contradiction C1 (RESOLVED 2026-07-21: non-paralyzable)

| Field            | Value                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------- |
| **Resolving time (LOCKED)** | 25 kHz maximum resolvable tunneling rate ⇒ **40 µs** (Nyquist from 50 kHz bandwidth). The 50 kHz sampling itself corresponds to **20 µs** — state BOTH clearly. |
| **Censoring rule (RESOLVED)** | **non-paralyzable** dead-time model: m = Γ/(1 + Γ·τ_d), plateau at 1/τ_d = 25 kHz. This is the canonical convention for the rest of the project. |
| **Introduced**   | Phase 1 (as an OPEN switch)                                                              |
| **Resolved**     | Phase 5 review (2026-07-21) — user decision to adopt non-paralyzable project-wide.       |
| **Rationale**    | The dead-time model cannot be fixed from electronics reasoning alone (both paralyzable and non-paralyzable are defensible idealizations of the real bandwidth-limited readout). The user closed the choice by decision after seeing both variants computed in Phase 5: **non-paralyzable is the project baseline going forward.** |

> ✅ **RESOLVED (2026-07-21).** Was an OPEN switch blocking Phase 5. Both variants were implemented
> and computed in Phase 5 (`response.py`, `response_matrix.py`; the paralyzable R matrices remain in
> `artifacts/stage1/response_matrix_*.npz` as a computed alternative). By **user decision at the
> Phase-5 review**, the project now **lives in non-paralyzable** (`params.DEFAULT_CENSORING = "non_paralyzable"`,
> which already matched): Phase 6 and any downstream work use non-paralyzable as the single canonical
> variant. The paralyzable results are retained as a sensitivity/alternative, not carried as a live
> switch into the final deliverables. The separate merge-vs-drop event-handling question did not arise
> as load-bearing in Phase 5 (the count-integral estimator integrates observed events; no merge/drop
> ambiguity affected the response) — non-paralyzable count censoring is the operative rule.

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

## I. Sub-eV Trigger-Probability Curve — the reported observable below ~1 eV

| Field | Value |
| ----- | ----- |
| **Convention** | Below the regime boundary the reported observable is a **trigger probability** P_trig(E_dep), **not** dR/dE_rec. |
| **Functional form** | Hill / logistic-in-log-energy: **P(E) = 1 / (1 + (E50/E)^k)**, with P(0) := 0 by continuity. |
| **50% point (DECIDED)** | **E50 = 1.0 eV exactly** (`params.TRIGGER_E50`). Structural, not tuned: P(E50) = 1/(1 + 1^k) = 1/2 for **every** k > 0. **CHANGED 2026-07-23 by user decision, superseding the 0.5 eV value of 2026-07-22 and ROADMAP Phase 10 Success Criterion 4, which asserts the 50% point is 'exactly at 0.5 eV'.** |
| **Axis caution** | E50 is on the **DEPOSIT** axis. The deposit->reconstructed slope is ~0.5 (Phase 13 measured the E_rec image of a 1 eV deposit at 0.4972/0.4959 eV), so the half-point appears near **~0.5 eV RECONSTRUCTED**, not 1.0 eV. Quoting E50 against a reconstructed-energy axis is the cross-axis error Phase 14 flagged. |
| **Sharpness (EXPOSED, not measured)** | k, dimensionless (`params.TRIGGER_SHARPNESS`), default **4.0**, declared scan range **[1, 12]** (`params.TRIGGER_SHARPNESS_RANGE`). Fixed by **no** project artifact. |
| **Regime boundary** | **1.0 eV** deposited energy, defined once at `trigger.SUBEV_REGIME_BOUNDARY_eV`; every sub-eV deliverable imports it rather than restating a literal. |
| **Composition rule** | P_trig is an **ANALYSIS efficiency multiplied on top of** the un-triggered quantity: `composed = P_trig(E) × untriggered`. It **does NOT replace ε ≈ 0.5 in Section E** and **does not modify Section F**. ε remains inside the un-triggered quantity through `energy_scale.n_qp_yield` (N_qp = ε·E_sensor/Δ_tr) and the `response.calibrate_C` slope. Setting P_trig ≡ 1 reproduces the pre-existing chain bit-for-bit. |
| **Status** | **PHENOMENOLOGICAL.** No trigger threshold has ever been measured for this device. Only the 50% point carries a project decision; the functional form is chosen and the width is unconstrained. |
| **Introduced** | Phase 10 (Plan 10-02), from USER DECISION 2026-07-22. **Revised 2026-07-23:** E50 0.5 -> 1.0 eV. The frozen phase CSVs still carry `dRdErec_trigger_weighted` and `P_trig_effective` columns computed at E50 = 0.5 eV and are NOT regenerated by that change; they are superseded and listed in the revision PR. |
| **Rationale** | Below ~1 eV, dR/dE_rec presupposes the lumped ε ≈ 0.5 deposited-to-signal collection efficiency, which is not defensible for a deposit of ~3 optical-phonon quanta in Ge. The user chose to replace the reported object rather than patch the efficiency. |

> A logistic in **linear** energy, P = 1/(1 + exp(−(E − E50)/w)), was **rejected**: it gives
> P(0) = 1/(1 + e^{E50/w}) > 0, i.e. a nonzero probability of triggering on nothing —
> **6.6929 × 10⁻³ at w = 0.1 eV** — and a nonzero probability at negative energy. On an axis
> spanning four decades from 0.1 eV that floor would sit under every sub-eV number in the
> project. Derivation: `GPD/phases/10-.../10-02-TRIGGER-CURVE-DERIVATION.md`.

**Test values (hand-checkable, in the style of Sections E and F).** At the default k = 4:

- P(E50) = P(0.5 eV) = 1/(1 + 1⁴) = **1/2** — and this holds for every k, not just k = 4.
- P(2·E50) = P(2.0 eV) = 1/(1 + (1/2)⁴) = 1/(1 + 1/16) = **16/17 = 0.941176…**
- P(E50/2) = P(0.5 eV) = 1/(1 + 2⁴) = **1/17 = 0.058824…**

> The three ratios above are identities in E50 at k = 4 and are unchanged by the
> 2026-07-23 move; only the energies they sit at moved (0.25/0.5/1.0 eV -> 0.5/1.0/2.0 eV).
- P(0) = **0 exactly**.

**Sensitivity obligation.** Because k is fixed by no measurement, every downstream result
computed with this curve must be reported together with its sensitivity to k over
[1, 12]. A buried width would be a fabricated device property (`fp-hardcoded-width`).

---

## J. Phonon Energy Scale and Debye-Waller Convention

| Field | Value |
| ----- | ----- |
| **Definition** | **`omega_bar == hbar^2 / (2 m_N <u_x^2>)`**. Only this definition makes `2W = E_R/omega_bar` exact and `sigma_E = sqrt(E_R·omega_bar)` self-consistent. |
| **Debye-Waller convention** | **`2W = q^2 <u_x^2>`**, with `<u_x^2>` the **1-D** mean-square displacement and `q = sqrt(2 m_N E_R)`. |
| **Rejected alternative** | **`q^2<u^2>/3` is REJECTED.** The `/3` is the isotropic projection `<u_x^2> = <u^2>/3`, which for cubic Ge (spacegroup 227) is **exact by symmetry** and has **already been applied** in `<u_x^2>`. Applying it a second time inside `2W` is the factor-3 trap: it would divide `2W` by 3 and multiply `omega_bar` by 3, and every sub-eV width scales linearly with `omega_bar`. |
| **LOCKED `<u_x^2>`** | **1.6096e-3 angstrom^2** (`params.U_X_SQ_ANGSTROM2` = 1.6096194483e-3) |
| **LOCKED `omega_bar`** | **17.8597 meV** (`params.OMEGA_BAR_eV` = 1.7859677040e-2 eV) |
| **LOCKED `B = 8 pi^2 <u_x^2>`** | **0.12709 angstrom^2** (`params.DEBYE_WALLER_B_ANGSTROM2` = 0.1270904575) |
| **Evaluation point** | **`T -> 0`** zero-point limit, `coth(w/2k_BT) -> 1` taken EXACTLY. Justified by measurement, not assertion: at T = 10 mK the full `coth` form differs from the limit by **5e-9** relative. (The same quadrature at 300 K gives `<u_x^2>` = 7.067e-3, B = 0.5580 angstrom^2 — the regime where diffraction B factors are measured, and **not the same quantity** as the locked value.) |
| **Nuclear mass** | Natural abundance-weighted Ge, `m_N c^2 = 6.7724551e10` eV, from `params.GE_ISOTOPES` (Phase-7 nuclear-data lock). `omega_bar` and `2W` are **mass-free** (see below), so the 0.10 % ambiguity in mass averaging touches only `<u_x^2>` and `B`. |
| **Citation** | **G. Nelin and G. Nilsson, Phys. Rev. B 5, 3151 (1972)**, DOI 10.1103/PhysRevB.5.3151 — the measured Ge phonon spectrum, via NCrystal 4.4.6 `Ge_sg227.ncmat`, frozen at `data/external/ge_vdos/` with SHA-256. |
| **Status** | **MEASURED VDOS, DERIVED SCALARS.** `omega_bar`, `<u_x^2>` and `B` are computed in-phase from the frozen spectrum, never quoted from `GPD/literature/` (`fp-quote-survey-numbers`) and never from the Debye model (`fp-debye-substitute`). Residual uncertainty: a single 1972 measurement; two digitizations of it disagree by 1.9 %; the quadrature itself is exact to 1e-7. |
| **Introduced** | Phase 11 (Plan 11-01), CALC-14 / ROADMAP Phase 11 SC1. |

**The rate is NEVER multiplied by `exp(-2W)`.** `2W` is used to *size* the impulse-approximation
broadening and nothing else. `exp(-2W)` suppresses only the **zero-phonon (coherent)** channel,
whose strength has moved into the multiphonon continuum; with `exp(-2W) ~ 1e-2` at 100 meV and
`~1e-20` at 1 eV, applying it as a rate factor would erase a real signal. Milestone-wide
prohibition, restated here where it will actually be read.

**Two algebraic identities — neither is corroboration.**

1. `2W = q^2<u_x^2> = 2 m_N E_R <u_x^2> = E_R/omega_bar`. Substituting `q^2 = 2 m_N E_R` turns one
   expression into the other *by construction*. Reporting the momentum-transfer route as an
   independent confirmation of `2W` is forbidden proxy `fp-q-route-as-independent`; it is a
   units check. Likewise `2W(100 meV) ∈ [4.76, 8.33]` is the same statement as
   `omega_bar ∈ [12.0, 21.0] meV`, not a second constraint.
2. **`m_N` cancels out of `omega_bar`.** With `<u_x^2> = (hbar^2/2m_N)·I` and `I = ∫g(w)/w dw`,
   `omega_bar = 1/I` — the **harmonic mean** of the VDOS — and `2W = E_R·I` is mass-free.

**Moment mismatch, carried forward to CALC-15.** `<u_x^2>` is governed by the **harmonic** mean of
the VDOS; `<p_x^2>`, which sets the impulse-approximation Gaussian width, is governed by the
**arithmetic** mean. They coincide only for a single mode. Measured Ge: harmonic 17.8597 meV,
arithmetic **24.1955 meV** (`params.OMEGA_BAR_ARITHMETIC_eV`), ratio `<w><1/w> = 1.3548`. A
single-frequency `sigma_E = sqrt(E_R·omega_bar)` therefore **understates** the true IA width by
`sqrt(1.3548) = 1.1639`. For a Debye spectrum that factor is exactly `sqrt(9/8) = 1.0607`.

**Test values (hand-checkable, in the style of Sections E, F and I).**

- `q(100 meV) = sqrt(2 m_N E_R)` = **116.38 keV/c** = **58.98 angstrom^-1** (units check).
- `2W(100 meV)` = `58.98^2 x 1.6096e-3` = **5.599** = `0.1 eV / 17.8597 meV`. Same number twice.
- `2W(0.5 eV)` = **27.996**; `2W(1 eV)` = **55.992**; `2W(10 eV)` = **559.92**.
- `B = 8 pi^2 x 1.6096e-3` = **0.12709 angstrom^2**.
- Analytic oracle, independent of every Ge file: a Debye VDOS `g = 3w^2/w_D^3` at
  `theta_D = 374 K` returns `<u^2>_3D = 9 hbar^2/(4 m_N k_B theta_D)` = **4.0139e-3 angstrom^2**,
  `<u_x^2>` = **1.3380e-3 angstrom^2**. The measured VDOS sits **1.203x** above that.

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
| Low-E reconstruction | E_rec ≈ E_dep (unit calibration slope, from 2026-07-25; was 0.5·E_dep) | putting ε on the energy axis — E_rec ≈ 0.5·E_dep makes a known 10 eV line land at 5 eV | Section E.1 |
| Saturation | above the onset E_rec is genuinely sub-linear and stays that way | "calibrating" it back to E_rec = E_dep everywhere (`fp-unfold-saturation`) | Sections E.1, F |
| Resolving time | 40 µs (25 kHz Nyquist) | 20 µs (50 kHz sampling) conflated | Section F |
| Recoil scale | keV_nr (phonon scale, no quenching) | keVee (Lindhard applied) → CEvNS ×5–7 too small | Section B |
| Sub-eV trigger 50% point | E50 = 1.0 eV (from 2026-07-23; was 0.5 eV), exact for every k | a 50% point that holds only at one width | Section I |
| Debye-Waller exponent | 2W = q²⟨u_x²⟩ (1-D MSD) | q²⟨u²⟩/3 (double-counted isotropic projection) → 2W and ω̄ off by 3× | Section J |
| VDOS normalization | ∫g(ω)dω = 1, with the leading 3 in ⟨u²⟩_3D | ∫g dω = 3 while keeping the leading 3 → ⟨u_x²⟩ 3× too large | Section J |
| Effective phonon energy | ω̄ = 17.8597 meV (harmonic mean of the measured VDOS) | 37.79 meV (the zone-centre optical phonon — a different quantity, same symbol) | Section J |

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
| Unified phonon scale (B) | Efficiency ε (E) | E_rec ≈ E_dep at low E (unit calibration slope, §E.1); ε survives as the physical deposit→QP conversion fraction inside the forward chain, not on the energy axis; both NR and ER deposits use the same map | ✓ consistent |
| Natural units internal (A.2) | CEvNS prefactor /4π (C) | σ in GeV⁻² → ×(ħc)² → cm²; dimensionally σ_tot = G_F²Q_W²E_ν²/4π · (ħc)² | ✓ consistent |
| sin²θ_W = 0.2387 (C) | Q_W = N − (1−4sin²θ_W)Z (C) | 1 − 4×0.2387 = 0.0452 | ✓ consistent |
| Per-kg normalization (D) | 110 g wafer geometry (D) | rates quoted per-kg for benchmark, physical detector is 110 g | ✓ consistent (dual bookkeeping, explicitly documented) |
| Resolving time 40 µs (F) | E_dep→E_rec saturation (B, F) | saturation onset when peak Γ > 25 kHz (1/40 µs) | ✓ consistent |
| k_B explicit (A.3) | QP tunneling K ∝ k_B T (G) | k_B appears explicitly in Γ_in ≈ K·n_qp | ✓ consistent |
| Unified phonon scale (B) | Phonon energy scale ω̄ (J) | E_ph = E_dep must hold across the whole 0.1 eV – 6 eV window, i.e. no competing storage channel may open there. SuperCDMS (APL 113, 092101) puts the Ge displacement threshold at 19.7 ⁺⁰·⁶₋₀·₅ eV with no defect creation below ~6 eV, so no defect-storage channel opens in-window and Section B's identity survives everywhere Section J is used. Note ω̄ = 17.86 meV is the *phonon* scale, not a threshold; the two are 3 decades apart. | ✓ consistent |
| Debye-Waller 2W (J) | CEvNS recoil kinematics (C) | q² = 2m_N E_R must use the SAME abundance-weighted m_N as `params.GE_ISOTOPES`. It does — and 2W = E_R/ω̄ is mass-free anyway, so a mass slip cannot hide here. | ✓ consistent |

No internal inconsistencies found. The formerly-OPEN item — the paralyzable-vs-non-paralyzable /
merge-vs-drop switch (Section F) — was **RESOLVED at the Phase-5 review (2026-07-21)** by user decision
to adopt **non-paralyzable** project-wide. Both variants were computed in Phase 5; non-paralyzable is
now the single canonical convention for Phase 6 and downstream. No open convention items remain.

---

## Change Log

| Date | Change | Rationale |
| ---- | ------ | --------- |
| 2026-07-20 | Initial establishment (Phase 1, CONV-01). Sections A–H locked; C1 censoring switch left OPEN. | User-approved convention set from interactive-mode proposal. |
| 2026-07-21 | Section F censoring switch RESOLVED → **non-paralyzable** project-wide. | User decision at Phase-5 review after both variants were computed; closes the last OPEN convention item. |
| 2026-07-22 | **Section I added**: sub-eV trigger-probability curve, Hill form, 50% point fixed at 0.5 eV, exposed sharpness k (default 4, range 1–12), regime boundary 1.0 eV. Sections E and F unmodified. | Phase 10 / Plan 10-02, implementing USER DECISION 2026-07-22. The curve is an ANALYSIS efficiency multiplied on top of ε ≈ 0.5, never a replacement for it (ROADMAP Phase 10 success criterion 4; CALC-16). |
| 2026-07-22 | **Section J added**: phonon energy scale and Debye-Waller convention. ω̄ = 17.8597 meV, ⟨u_x²⟩ = 1.6096e-3 Å², B = 0.12709 Å², all at T→0 from the measured Ge VDOS; `2W = q²⟨u_x²⟩` locked and `q²⟨u²⟩/3` explicitly REJECTED; three Numerical Factor Registry rows and two Cross-Convention rows added. No prior section modified. | Phase 11 / Plan 11-01, CALC-14. Closes the 12–21 vs 37 meV ambiguity by an argued choice from the measured spectrum (Nelin & Nilsson 1972 via NCrystal `Ge_sg227.ncmat`) rather than carrying a range — both 2W and σ_E scale linearly with ω̄, so a range would propagate a 2–3× ambiguity into every sub-eV number in Phases 12–16. The ambiguity is largely a **notation collision**, not a physics dispute: 37 meV is the zone-centre optical phonon, a different quantity. |
