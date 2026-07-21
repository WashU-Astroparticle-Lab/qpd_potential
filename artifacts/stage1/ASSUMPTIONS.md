# Stage-1 Assumptions Note

**Project:** QPD Particle-Physics Potential — Stage-1 Reconstructed-Energy Spectra
**Seeded:** 2026-07-20 (Phase 1, Plan 01-02)
**Deliverable:** `deliv-note` (contract deliverable for Phase 1)
**Authoritative lock:** `GPD/CONVENTIONS.md` + `GPD/state.json` → `convention_lock`

> This is a **concise stage-1 assumptions note**, not a rewrite of `CONVENTIONS.md`.
> `CONVENTIONS.md` is the authoritative lock; this note records the *modeling
> assumptions and their confidence flags* that the energy-scale chain and the
> Phase-5 response model rest on. All numbers are cross-referenced to
> `qpd_potential.params` (Table II registry) and `CONVENTIONS.md`. Where a value
> is an assumption rather than a measurement, its confidence is flagged
> (HIGH / MEDIUM / LOW) and, for the weakest ones, EXPOSED as a scannable parameter.

---

## 1. Unified no-quenching energy-scale chain (CONVENTIONS Section B)

A fieldless phonon calorimeter has a **single unified phonon energy scale with no ionization quenching**
for BOTH nuclear-recoil (CEvNS) and electron-recoil (muon, Compton) deposits:

```
T ≡ E_nr  →  E_ph  →  E_dep  →  E_rec
```

- `T ≡ E_nr` — nuclear-recoil kinetic energy (CEvNS); `T` and `E_nr` are the same.
- `E_ph = E_dep − E_stored(defects)`; **defect (Frenkel) storage = 0 for stage 1**,
  so `E_ph = E_dep` for all channels (see §5). Zero for muons/Compton by construction.
- `E_dep` — full recoil/ionization energy delivered to the lattice (no quenching).
- `E_rec` — reconstructed energy, the observable axis; low-energy limit
  `E_rec ≈ 0.5·E_dep` (linear, unsaturated regime).

**FORBIDDEN proxies (must be rejected):**
- Any mixing of `keVee` / `keVnr` scales.
- Applying Lindhard or any ionization/quenching factor on this phonon scale
  (would suppress CEvNS ~5–7× and is physically wrong for a phonon calorimeter).

---

## 2. E_dep → per-sensor yield / efficiency (CONVENTIONS Section E)

**Yield map (lumped linear):**

```
N_qp    = ε · E_sensor / Δ_tr          # quasiparticle COUNT per sensor
n_qp    = N_qp / V_tr                   # per-sensor QP density [µm⁻³]
Γ_in    = K · n_qp = K·ε·E_sensor/(Δ_tr·V_tr)   # plateau tunneling rate [Hz]
```

- **ε ≈ 0.5** — imposed deposited-to-signal efficiency (a forward-model
  *definition*, not a derived quantity). Lumps phonon collection + pair-breaking
  + trapping + the Δ_abs/Δ_tr down-conversion multiplication. **SAME baseline for
  both designs**, carrying a **±10–20% design-dependent band** [confidence: MEDIUM].
  The paper's physical estimate η_ce ≈ 0.3 is an INDEPENDENT cross-reference, NOT
  the baseline. Per-design ε split is a Phase-5 refinement (Deferred).
- **The quantum is the TRAP gap Δ_tr** (Al 190 µeV, Hf 40 µeV) — standard trapping
  physics. If the effective quantum were nearer Δ_abs, the Hf advantage would
  shrink [unvalidated assumption].

---

## 3. Localized + diffuse per-sensor energy sharing (CONVENTIONS-consistent; CONTEXT decision A)

**Model:** a fraction `f_prompt` of a deposit's phonon energy is absorbed near the
impact point, spread over a spot of ~π·r² sensors; the remaining `(1 − f_prompt)`
spreads diffusely (≈uniform) across all ~10 300 sensors:

```
E_sensor(on spot)  = f_prompt·E_dep/(π r²) + (1 − f_prompt)·E_dep/N_sensors
E_sensor(off spot) =                          (1 − f_prompt)·E_dep/N_sensors
```

| Parameter | Default | Range | Confidence |
| --- | --- | --- | --- |
| `f_prompt` (prompt fraction) | **0.3** | 0.1 – 0.5 | **LOW — EXPOSED, not derived** |
| `r` (spot radius, sensors) | **2** | 1 – 5 | **LOW — EXPOSED, not derived** |

> ⚠️ **WEAKEST ANCHOR.** `f_prompt` and `r` have **no direct thin-wafer QPD
> measurement**; the CDMS/SuperCDMS athermal-phonon literature motivates the
> *structure* (prompt/ballistic near-hit vs. thermalized diffuse) but not the
> numbers. They MUST be presented as scanned assumptions, never derived values
> (forbidden proxy `fp-derived-sharing`). The muon spectrum shape depends
> strongly on them.

**Why localized+diffuse and not global equal-split:** equal-split among ~10 300
sensors makes per-sensor keV-scale deposits fall below the ~1 eV saturation onset,
erasing the localization-driven keV-scale saturation on/off behavior (forbidden
proxy `fp-nosat`). The **equal-split limit `f_prompt → 0` is the required sanity
knob**: it flips keV-scale saturation OFF (the binary discriminator). NOTE: a
genuine muon deposit (≳1.5 MeV) still saturates even under equal-split
(~150 eV/sensor ≫ ~1 eV onset), so equal-split is wrong as the *default model*,
not because muons stop saturating — localization sets the DEGREE of muon
saturation, not its existence.

**Muon track collapsed to a point** for stage 1 (no along-track line spread). This
*overstates* per-sensor muon saturation (conservative); a real ~cm track spreads
over a line of sensors, lowering the peak per-sensor rate [documented systematic;
along-track sharing is a Deferred Idea, out of scope].

---

## 4. Bandwidth / dead-time censoring (CONVENTIONS Section F — OPEN switch)

- **Resolving time τ_d = 40 µs (= 1/25 kHz Nyquist), LOCKED.** This is the 25 kHz
  maximum resolvable tunneling rate. **NOT the 20 µs (= 1/50 kHz) sampling
  interval** — conflating them puts the ceiling at 50 kHz (forbidden proxy
  `fp-20us`). Saturation ceiling = **25 kHz**.
- **Saturation definition:** `saturated ⇔ peak Γ_in > 25 kHz`, where peak Γ_in ≈
  p·K·N_qp/V_tr uses the two-exponential pulse **peak factor** p ≈ 0.25 (Al) /
  0.13 (Hf) [paper Eq. 4; confidence MEDIUM].
- **Two censoring variants kept as an EXPLICIT SWITCH:**

  | Variant | Observed rate m(Γ) | Behavior |
  | --- | --- | --- |
  | **non-paralyzable (DEFAULT)** | `m = Γ/(1 + Γ τ_d)` | monotone → 25 kHz ceiling |
  | paralyzable | `m = Γ·e^(−Γ τ_d)` | peaks at Γ = 25 kHz, then rolls over |

  Event-handling sub-switch: **drop** (default) vs merge.

> ⚠️ **OPEN QUESTION — BLOCKS Phase 5.** The paralyzable-vs-non-paralyzable and
> merge-vs-drop choice is an explicit switch, **not** a decision. Both variants
> MUST be implementable; neither is silently chosen. This must be resolved before
> the Phase-5 saturation definition is finalized.

---

## 5. Sub-dominant correction: defect storage = 0 (CONVENTIONS Section B)

Frenkel-defect energy storage is set to **zero** for stage 1 (`E_ph = E_dep` for
all channels). This is a **few-% NR-only (CEvNS) systematic** to revisit later; it
matters only at the lowest CEvNS recoil bins. Keeps the unified scale exact.

---

## 6. Detector geometry / normalization (CONVENTIONS Section D)

| Quantity | Value | Notes |
| --- | --- | --- |
| Wafer | 4″×4″×2 mm = **20.65 cm³ ≈ 110 g** | physical detector geometry adopted everywhere |
| Sensors | **~10 300** at 1/mm² | ONE instrumented face |
| Ge atoms/kg | **8.29×10²⁴** | 1000 g / 72.63 g·mol⁻¹ × N_A |
| Ge density | 5.323 g/cm³ | |
| Reactor power | **3 GW_th** (thermal, NOT electric) | GW_e vs GW_th is a ~×3 trap |
| Standoff | 25 m | |
| ν̄ flux | ~7–8×10¹² ν̄·cm⁻²·s⁻¹ | DERIVED (CONUS+ scaling) |

**Normalization:** adopt the 110 g wafer geometry for the physical detector but
**KEEP per-kg rate normalization** (counts·kg⁻¹·day⁻¹) for benchmark comparison
against Billard/CONUS+. The "1 kg crystal" framing in `literature/SUMMARY.md` is
STALE — do not propagate.

---

## 7. Table II per-design parameter table (from `qpd_potential.params`, verbatim from Ramanathan et al. 2026)

Table II is indexed by **TRAP/junction material**; the absorber supplies only the
absorber gap Δ_abs. "Ta→Al" uses the **Aluminum** column; "Al→Hf" uses the
**Hafnium** column.

| Parameter | Ta→Al (Al trap) | Al→Hf (Hf trap) | Units | Confidence |
| --- | --- | --- | --- | --- |
| Δ_tr (trap gap) | 190 | 40 | µeV | HIGH |
| V_tr (eff. trap volume) | 100 | 1000 | µm³ | HIGH |
| K (tunneling proportionality) | 3 | 20 | kHz·µm³ | HIGH |
| τ_qp (recomb. lifetime) | 1 ms | ~400 µs | s | HIGH (Al) / MEDIUM (Hf) |
| τ_inj (injection) | 2 ms | 2 ms | s | HIGH |
| Γ_out (back-tunneling) | 2 | 10 | kHz | HIGH |
| n_0 (quiescent QP density) | 0.3 | 0.03 | µm⁻³ | HIGH |
| Fano F | 0.2 | 0.2 | — | HIGH (paper flags "to be validated") |
| T_opr (operating) | 0.1 | 0.025 | K | HIGH |
| Δ_abs (absorber gap) | ≈0.68 meV (Ta) | 190 µeV (Al) | eV | **MEDIUM (Ta)** / HIGH (Al) |
| p (two-exp peak factor) | 0.25 | 0.13 | — | MEDIUM |

- **τ_qp (Hf) = ~400 µs** adopted (caption/lit [92]) over the 1 ms table cell
  (Al-side footnote); the paper's own flagged uncertainty [MEDIUM].

### Ta absorber gap — flagged assumption

> **Δ_Ta ≈ 0.68 meV** is an ASSUMPTION, not a device measurement: bulk **α-Ta**
> BCS gap (Δ = 1.764 k_B T_c, T_c ≈ 4.48 K). `materials.yaml` has **NO Ta entry**.
> Thin-film Ta (α vs β phase) shifts T_c by ~5–9×, so the film phase is
> **UNVERIFIED** [confidence: MEDIUM]. Do NOT invent a film-specific number;
> carry film phase as a Phase-5 systematic (forbidden proxy `fp-ta-invented`).

### Trapping margins Δ_abs/Δ_tr — both valid

| Design | Δ_abs/Δ_tr | Status |
| --- | --- | --- |
| Ta→Al | **3.58** | ✓ ≥ 2 lower-bound margin |
| Al→Hf | **4.75** | ✓ ≥ 2 (a valid LARGER margin, NOT a ceiling violation) |

Trapping requires only a **LOWER bound** (Δ_abs/Δ_tr ≳ 2–4, CONVENTIONS Section G):
the absorber gap must exceed the trap gap by a comfortable margin so QPs relax into
the trap and cannot return. The Al→Hf ratio of 4.75 is a valid *larger* margin, not
a violation.

### Design asymmetry — record BOTH ratios (they are not contradictory)

- **Raw yield ratio (N_qp per eV):** `N_qp ∝ 1/Δ_tr` ⇒ Hf/Al = 190/40 = **4.75×**.
  This is the raw quasiparticle-count advantage, **not** the saturation ordering.
- **Saturation-driving ratio (Γ_in per eV):**
  `Γ_in^Hf/Γ_in^Al = (K_Hf/K_Al)·(Δ_Al/Δ_Hf)·(V_Al/V_Hf) = (20/3)·(190/40)·(100/1000) ≈ **3.2×**`.
  Hf's 10× larger V_tr and 6.7× larger K partly cancel the 4.75× gap advantage.

> **Γ_in (~3.2×) is the ORDERING DRIVER for saturation** — NOT the N_qp-only 4.75×
> (or the mistaken 5–10×) value (forbidden proxy `fp-nqp-ordering`). Consequence:
> Hf saturates first, at a **lower per-sensor onset (~0.77 eV)** than Al (~1.27 eV).

---

## 8. CEvNS convention pointer (CONVENTIONS Section C; Plan 01-01)

Recorded here as a pointer only (the CEvNS module lives in `qpd_potential.cevns`):

```
Q_W       = N − (1 − 4 sin²θ_W) Z,   sin²θ_W = 0.2387 (low-E MS-bar)
σ_tot     = G_F² Q_W² E_ν² / (4π) · (ħc)²      # prefactor /4π (NOT /8π)
(ħc)²     = 3.894×10⁻²⁸ GeV²·cm²                # dropping it is the #1 CEvNS bug
benchmark : σ(72Ge, E_ν = 4 MeV) ≈ 1.0×10⁻⁴⁰ cm²  (full Q_W; 01-01 gives 1.0026×10⁻⁴⁰)
```

---

## 9. Weakest anchors + disconfirming checks

**Weakest anchors (in decreasing severity):**
1. `f_prompt` (0.3) and `r` (2 sensors) — LOW, no thin-wafer measurement; muon
   spectrum shape depends strongly on them.
2. Muon deposit point-collapse — overstates per-sensor saturation vs a real ~cm track.
3. Ta absorber gap ≈ 0.68 meV — MEDIUM, bulk α-Ta assumption, film phase unverified.
4. Table II K and V_tr assumed to transfer to this wafer geometry.
5. Trap-gap quantum (N_qp ∝ 1/Δ_tr) rather than an effective quantum nearer Δ_abs.

**Disconfirming checks (any would show a mis-specification):**
- A **keV-scale** (CEvNS/Compton) deposit that saturates under equal-split
  (f_prompt → 0) — would show the sharing model is mis-specified. *(Verified false:
  a 2 keV deposit gives ~4–6 kHz/sensor under equal-split, below 25 kHz.)*
- Plausible `f_prompt`/`r` giving no localized enhancement of muon saturation degree.
- Non-paralyzable ceiling coming out at **50 kHz instead of 25 kHz**. *(Verified 25 kHz.)*
- Γ_in^Hf/Γ_in^Al landing far from ~3 (e.g. 5–10×) → an N_qp-only ordering error.
  *(Verified 3.17×.)*

---

## 10. Out of scope (Deferred Ideas — NOT assumed here)

Along-track (line) muon energy sharing; per-design ε split; localization-scale
sensitivity scan; full G4CMP position-dependent phonon-collection model; the E_rec
estimator definition (count-integral vs time-over-saturation vs hybrid — Phase 5);
any spectrum computation or per-design crossover energy (Phases 3–6).

---

---

## Addendum (Phase 2, Plan 02-02) — sub-1.8 MeV reactor-flux shape limitation

The frozen reactor flux `data/flux/reactor_flux_v1.0.csv` normalizes to
∫Φ dE = 7.50×10¹² ν̄·cm⁻²·s⁻¹ at 3 GW_th / 25 m (target 7–8×10¹²), with the >2 MeV
shape data-anchored to Huber/Mueller and cross-checked against published Huber ²³⁵U
within the band. **Open limitation, carried honestly:** the sub-1.8 MeV per-isotope
fission *summation* SHAPE remains a seam-anchored **MODEL PLACEHOLDER**. The citable
primary reference for this region is **Kopeikin, Phys. At. Nucl. 75, 143 (2012)**, and
the placeholder is qualitatively consistent with it (rising toward low E, bounded), but
a **machine-readable Kopeikin-2012 per-isotope table could not be sourced in-environment**
(the 2012 paper is Springer-only; no arXiv table; Huber/Mueller tabulations stop at 2 MeV).
No Kopeikin table was fabricated. The model dependence is covered by a **wide, split
uncertainty band** (2–5% above 2 MeV → 20% on 1.0–1.8 MeV → 25% below 1.0 MeV), NOT a
uniform band. The absolute *integral* rests on the well-anchored ~6 ν̄/fission and ~205 MeV/
fission (good to a few %); the real residual risk is the sub-IBD flux *shape*, which only
matters for the lowest-recoil CEvNS bins downstream. Replace with a digitized
Kopeikin-2012 / Estienne-Fallot / CONFLUX table when one becomes machine-sourceable.

_Phase-2 addendum authored under Plan 02-02; does not supersede the Phase-1 lock._

---

_Phase: 01-conventions-energy-scale-foundation · Plan 01-02 · Seeded 2026-07-20_
_Authoritative lock: `GPD/CONVENTIONS.md`. This note flags assumptions and confidence; it does not supersede the lock._
