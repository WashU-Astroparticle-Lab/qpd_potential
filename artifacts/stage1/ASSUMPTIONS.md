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

## 4. Bandwidth / dead-time censoring (CONVENTIONS Section F — RESOLVED non-paralyzable 2026-07-21)

- **Resolving time τ_d = 40 µs (= 1/25 kHz Nyquist), LOCKED.** This is the 25 kHz
  maximum resolvable tunneling rate. **NOT the 20 µs (= 1/50 kHz) sampling
  interval** — conflating them puts the ceiling at 50 kHz (forbidden proxy
  `fp-20us`). Saturation ceiling = **25 kHz**.
- **Saturation definition:** `saturated ⇔ peak Γ_in > 25 kHz`, where peak Γ_in ≈
  p·K·N_qp/V_tr uses the two-exponential pulse **peak factor** p ≈ 0.25 (Al) /
  0.13 (Hf) [paper Eq. 4; confidence MEDIUM].
- **Censoring variant — RESOLVED to non-paralyzable (canonical, project-wide):**

  | Variant | Observed rate m(Γ) | Behavior | Status |
  | --- | --- | --- | --- |
  | **non-paralyzable** | `m = Γ/(1 + Γ τ_d)` | monotone → 25 kHz ceiling | **CANONICAL DELIVERABLE** |
  | paralyzable | `m = Γ·e^(−Γ τ_d)` | peaks at Γ = 25 kHz, then rolls over | retained as a labeled SENSITIVITY only |

  Event-handling sub-switch: **drop** (default) vs merge.

> ✅ **RESOLVED 2026-07-21 (USER DECISION, CONVENTIONS §F closed).** After Phase 5
> computed **both** variants, the user accepted Phase 5 and chose **non-paralyzable**
> as the single canonical convention for the rest of the project. `params.DEFAULT_CENSORING
> = "non_paralyzable"`; Phase 6 and all downstream deliverables fold **only** `R_non_paralyzable`.
> The paralyzable `R` matrices are retained in `response_matrix_*.npz` as a **sensitivity, not a
> live switch** (forbidden proxy `fp-paralyzable-swap`). The operative high-E response is the
> **plateau** (~34.8/26.8 keV muon tail), never the paralyzable rollover. No OPEN switch remains
> in the deliverable framing.

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

---

## Addendum (Phase 5, Plan 05-01) — QPD response chain, count-integral E_rec estimator, crossover band

Phase 5 turns the Phase-1 forward-chain scaffold into a working per-design
reconstructed-energy response (`src/qpd_potential/response.py`). It implements
the deliberately-stubbed `E_rec` estimator as a **calibrated count-integral
estimator** and reports the linear→saturated crossover as a **band**. All numbers
below are recomputed in-code (`response.crossover_band`, `response.sweep_E_rec`),
not transcribed.

### Estimator (D-estimator decision, exercised)

`E_rec = C · Σ_i N_obs,i`, where `N_obs,i` is the censored tunneling-**event**
count on sensor `i` and `C` is a **single global per-design constant** fixed once
by requiring `dE_rec/dE_dep = ε = 0.5` on a deeply-linear deposit (default
`E_dep_cal = 0.01 eV`, no sensor saturated). Consequences:

- **Low-E linearity is calibration-consistency, NOT independent validation**
  (Pitfall 2 / `fp-calib-as-validation`): the low-E test passes by construction
  because `C` is fixed by that same slope. The genuinely tested content is the
  saturation onset and the plateau/rollover level.
- **Event-count mapping (Pitfall 1 / `fp-eventcount`):** the value fed to the
  MUST-USE `QuasiparticleBurstModel.expected_n_qp` is the tunneling-**event**
  count `∫Γ_in dt = K·τ_qp·N_qp/V_tr` (0.03·N_qp for Al, 0.008·N_qp for Hf),
  **not** the trapped-QP count `N_qp`. The two-exponential pulse is verified
  self-consistent with the recorded peak factors: `∫g dt = 1` and
  `τ_qp·max(g) = p` (0.2500 Al, 0.1337 Hf ≈ recorded 0.13).
- **The plateau IS the modeled saturation (`fp-no-saturation`):** the estimator
  is NOT a linear rate→energy extrapolation.

### VALD-04 limiting cases (the ONLY validation available — no saturated-regime benchmark exists)

| Regime | non_paralyzable | paralyzable |
| --- | --- | --- |
| Low E (below onset) | `E_rec ≈ 0.5·E_dep` (calibration-consistency) | same |
| 197 MeV muon tail | E_rec **plateaus** (monotone, bounded): ≈ **35 keV (Ta→Al) / 27 keV (Al→Hf)**, growing only logarithmically | E_rec **rolls over**: peaks ~keV then declines to ≈ **3.3 keV / 2.6 keV** |
| vs linear line | `E_rec/(0.5·E_dep) ≈ 3.5×10⁻⁴` at 197 MeV | `≈ 3×10⁻⁵` |

In BOTH variants `E_rec` does **not** track the linear `0.5·E_dep` line into the
tens-of-MeV range. The **stop-condition** (ROADMAP Phase-5) is checked and does
**not** trigger: at 197 MeV `peak Γ_in` exceeds the 25 kHz ceiling by ~10⁶–10⁷×
and the count-integral **does** saturate. A no-censoring scratch run confirms the
plateau has teeth (uncensored `E_rec = 0.5·E_dep` exactly, no plateau).

### Crossover deposit energy = a BAND per design, NOT a single number (SIMU-01; `fp-crossover-point`)

The crossover `E_dep` (on-spot `peak Γ_in = 25 kHz`) is dominated by the
LOW-confidence sharing parameters `f_prompt ∈ [0.1,0.5]`, `r ∈ [1,5]`:

| Design | E_sensor onset | **Default point** (f_prompt=0.3, r=2) — *SIMU-01 "explicit design number"* | Scan band [0.1,0.5]×[1,5] | **Equal-split upper anchor** (f_prompt→0) | Whole-array plateau (default) |
| --- | --- | --- | --- | --- | --- |
| Ta→Al (Al trap) | 1.27 eV | **≈ 53 eV** | 8.0 eV – 0.93 keV | ≈ **13.1 keV** | ≈ 18.6 keV |
| Al→Hf (Hf trap) | 0.77 eV | **≈ 32 eV** | 4.8 eV – 0.57 keV | ≈ **7.9 keV** | ≈ 11.3 keV |

**The default point (~53/32 eV) is SIMU-01's explicit design number; the ~3-order
band is the honest uncertainty.** **Hf saturates before Al** (lower onset) at
every point in the scan. **Two saturation scales** (both stated on any response
figure): (1) the *on-spot bend* at tens of eV (the ~πr² on-spot sensors saturate;
`E_rec` bends by ≤ f_prompt); (2) the *whole-array plateau* at ~10–20 keV (even
the diffuse per-sensor share reaches onset → all ~10,300 sensors saturated →
muon deposits pile up at the plateau/rollover ceiling — an **instrument artifact
of the modeled saturation, not a physical spectral line**).

### Ta absorber gap = a BINARY trapping gate, NOT a smooth response band (`fp-ta-band`)

`Δ_abs(Ta)` enters the response arithmetic **nowhere** — yield, rate, and onset
all use the **Al trap gap** `Δ_tr = 190 µeV`. The Ta→Al response is therefore
numerically **invariant** to `Δ_abs` within α-phase (verified: crossover and
`E_rec` unchanged for `Δ_abs ∈ {0.5, 0.68, 0.9} meV`). The only Ta-gap dependence
is the **binary trapping gate** `Δ_abs/Δ_tr ≥ 2` (asserted in code), i.e.
`T_c ≥ 380 µeV/(1.764 k_B) ≈ 2.5 K`. The cited bulk **α-Ta** baseline
(`Δ_abs = 0.68 meV`, ratio **3.58**, `T_c = 4.48 K`) passes; **β-Ta**
(`T_c ~0.5–2.7 K`) would fail and **invalidate the design premise**. This is a
design-invalidating risk, **not** a continuous ± band, and **no β-Ta film gap
value is fabricated** (`materials.yaml` has no Ta film entry).

### Weakest anchor / no-benchmark caveat (carried honestly)

**The saturated-regime response SHAPE has NO literature anchor at any energy.**
Validation is **limiting-cases-only** (low-E linearity by calibration; high-E
plateau/rollover). The mid-curve (bend region and plateau approach) is a **model
prediction**. Two further honest limitations: (i) the paralyzable-vs-non-
paralyzable censoring choice (CONVENTIONS F) was an OPEN switch here at Plan
05-01 — both curves are reported — **[SUPERSEDED 2026-07-21 → RESOLVED
non-paralyzable, CONVENTIONS §F CLOSED; paralyzable is a sensitivity only]**;
(ii) the analytic censored-integral (the
deliverable estimator, used for the muon-tail sweep) and the EMG event-train
realization agree to ~1% up to mild saturation but diverge by O(10–30%) in deep
saturation (closed-form renewal vs microphysical dead-window), an additional
unvalidated-shape uncertainty consistent with the no-benchmark caveat _(**[SUPERSEDED
2026-07-21 → RESOLVED non-paralyzable]**, see the box below)_. This phase
does **not** fold any spectrum (Phase 6) and does **not** build the full response
matrix `R(E_rec|E_dep)` (Plan 05-02).

> **[SUPERSEDED 2026-07-21]** Limitation (i) above (the censoring OPEN switch)
> reflects the state at Plan 05-01. It is **now CLOSED**: the user resolved
> CONVENTIONS §F to **non-paralyzable** project-wide (see §4 and the Phase-6
> addendum). Only the non-paralyzable curve is a deliverable; paralyzable is a
> retained sensitivity. No live OPEN censoring switch remains.

_Phase-5 addendum authored under Plan 05-01; does not supersede the Phase-1 lock._

---

## Addendum (Phase 4, Plan 04-02) — environmental gamma-background assumptions

The Compton background channel is a **thin-target single-scatter** electron-recoil
continuum, NOT a full-absorption spectrum:

- **Sourced radiogenic lines (nuclear data, not invented):** line energies + DDEP
  emission probabilities from the ⁴⁰K, ²³²Th, and ²³⁸U chains. Absolute flux is
  anchored to the cited **LABChico (EPJP 2022) measured surface spectrum**
  (⁴⁰K 0.036, ²⁰⁸Tl 2614.5 keV 0.0016 cm⁻²·s⁻¹); Th-chain siblings scaled by
  intra-chain DDEP ratios; the U chain via a documented `Φ_U = Φ_Th` assumption.
  Forbidden proxy `fp-invented-flux` rejected.
- **Thin-target single scatter:** each Compton electron recoil `T_e = E_γ − E'`
  is deposited; the scattered photon **escapes** the optically-thin 2 mm wafer
  (`μ·ℓ̄ ≈ 0.12/0.08 at 1/2 MeV`, double-scatter ~1.4%), so there are **NO
  photopeaks** — the continuum runs up to each self-validating Compton edge
  `E_edge = 2E_γ²/(m_ec² + 2E_γ)` (⁴⁰K→1243.4, ²⁰⁸Tl→2381.8, ²¹⁴Bi→1541.3 keV).
  Forbidden proxies `fp-full-absorption`, `fp-electron-not-photon` rejected.
- **Unified phonon scale, no quenching** (deposits are electron recoils; zero
  Frenkel correction). **Total single-scatter rate 0.268 Hz** vs an independent
  `Φ·σ_KN·N_e` anchor 0.273 Hz (ratio 0.983, within the VALD-03 factor-2 band).
- **Confidence:** edges HIGH (kinematic, exact); absolute total rate **MEDIUM**,
  carried with a **factor-2 site-dependent flux band** (0.5×/2×). The gamma flux
  is a **documented tunable input**, not a measurement of any specific site.

- **Electron-binding correction — incoherent scattering function `S(x,Z)` (refinement):**
  the angular sampling now uses the **bound**-electron incoherent cross section
  `dσ_incoh/dΩ = (dσ_KN/dΩ)·S(x,Z=32)` (the standard bound-Compton correction),
  replacing the pure free-electron Klein–Nishina angular weight. Here
  `x = E_γ[keV]·sin(θ/2)/12.39842` [Å⁻¹] is the momentum-transfer variable.
  `S(x,Z)` is **sourced, not invented** (`data/ge_incoherent_S.csv`): the Hubbell,
  Veigele, Briggs, Brown, Cromer & Howerton tabulation, *J. Phys. Chem. Ref. Data*
  **4**, 471 (1975), retrieved verbatim from the xraylib `data/SF.dat` Z=32 block
  (xraylib: Schoonjans et al., *Spectrochim. Acta B* **66**, 776 (2011)), fetched
  2026-07-21; interpolated **log-log** in `x`. This **fixes the unphysical
  free-KN low edge**: because `S(x→0)→0`, the near-forward / low-recoil
  continuum is strongly suppressed, so the Compton `dR/dE_dep` (and the folded
  `dR/dE_rec`) now **rolls off smoothly toward zero** at low energy instead of a
  flat continuum hard-cut at the grid floor — the roll-off completes near
  ~30–50 eV `E_dep` (~15–25 eV `E_rec`), **above** the 10 eV shared-grid floor
  (< 10⁻⁴ of counts below 50 eV `E_dep`), so the reconstructed floor sits in the
  fully binding-suppressed region (no separate sub-floor extension needed).
  Because `S(x→∞)→Z=32`, the **Compton edges** (backscatter, large `x`) and the
  **bulk continuum above ~keV** (`S/Z≈1`) are **UNCHANGED** — VALD-03 edge
  targets (⁴⁰K→1243.4, ²⁰⁸Tl→2381.7, ²¹⁴Bi→1541.3 keV) still self-validate.
  The per-line rate is recomputed with the bound total cross section
  `σ_incoh = ∫(dσ_KN/dΩ)·S(x,Z) dΩ` per atom (binding factor
  `f_bind = σ_incoh/(Z·σ_KN) ∈ [0.979, 0.999]` across the line band): the total
  Compton rate drops **slightly**, from **0.2685 Hz (free-KN)** to
  **0.2675 Hz (bound)**. The free-KN `Φ·σ_KN·N_e = 0.273 Hz` remains the labeled
  VALD-03 anchor; the bound/anchor ratio is **0.980** (still within the factor-2
  band). `S(x,Z)` changes the **cross section, not the energy scale** — unified
  phonon deposit, no quenching (guard `fp-quenching-compton` intact). Muon,
  CEvNS, and the response matrix `R` are untouched.

_Phase-4 gamma-background note consolidated into the stage-1 assumptions record under Plan 06-02._

---

## Addendum (Phase 6, Plan 06-02) — fold to reconstructed energy + stage-1 finalization

This is the **final stage-1 addendum**. It records the Phase-6 fold that turns the
frozen **deposited**-energy spectra into **reconstructed**-energy spectra dR/dE_rec
(the decisive stage-1 output; `deliv-fig-spectra` =
`artifacts/stage1/reconstructed_energy_spectra.pdf`), and consolidates the standing
caveats and key results. All numbers are recomputed in-code
(`qpd_potential.fold`), not transcribed.

### Fold method (counts-conserving, non-paralyzable)

- **Only `R_non_paralyzable` is folded** (CONVENTIONS §F RESOLVED, canonical; §4
  above). `N_dep[i] = dR/dE_dep[i]·ΔE_dep[i]`; `N_rec[j] = Σ_i R[j,i]·N_dep[i]`;
  `dR/dE_rec[j] = N_rec[j]/ΔE_rec[j]`. Because each `R` column sums to 1, counts
  are conserved per channel per design: **muon/Compton rel ≤ 2.2×10⁻¹⁶, CEvNS
  rel ≤ 1.3×10⁻¹⁶** (exact algebraic consequence, verified numerically).
- **CEvNS rebin:** `cevns_dRdT.csv` (320-pt recoil grid, 5–3200 eV_nr) is rebinned
  onto the shared 584-bin E_dep grid by a **piecewise log-log power-law integral**
  (exact for a steeply-falling spectrum), conserving counts: total **9.6×10⁻⁵** vs
  trapezoid, above-50-eV **67.67 vs 67.752** (0.12%).
- **CEvNS low edge (5 → 10.14 eV, below the grid floor): retained, NOT dropped**
  (`fp-drop-lowE-cevns`). These deposits sit far below the ~52.9/32.1 eV crossover
  onset where the response is exactly linear, so they are reconstructed via the
  exact `E_rec = 0.5·E_dep` mapping (E_rec ≈ 2.5–5 eV) and carried into the matching
  E_rec bins (7.27 counts/kg/day). The Phase-5 MC median at the lowest bins is
  ~0.483 (~3% below 0.5) — a small documented calibration nuance on the sub-floor band.

### Uncertainty carry-through (bands shown on the figure)

- **CEvNS:** 1σ reactor-flux band folded the same way (3.4% ≥95 eV_nr, rising to
  6.2%/9.8% at 50/20 eV_nr).
- **Compton:** factor-2 site-dependent γ-flux band (0.5×/2×).
- **Muon:** ±30% absolute-normalization band (Phase-4 VALD-02, ~15% vs PDG carried
  conservatively at 30%).
- **Sub-1.8 MeV CEvNS caveat:** the sub-IBD reactor-flux *shape* is a
  Kopeikin-2012-cited **model placeholder** (§Phase-2 addendum), contributing an
  additional **~6–10% on the CEvNS rate below ~95 eV_nr** (the sub-1.8 MeV rate
  fraction is 17.8%/33.8% at 50/20 eV_nr, ~0 above 95 eV).

### Reconstructed-energy landing (ROADMAP report-don't-force — verdict)

| Channel | Ta→Al peak E_rec | Al→Hf peak E_rec | Integrated rate (cts/kg/day) |
| --- | --- | --- | --- |
| CEvNS | **~42 eV** | ~42 eV | 109.6 |
| muon | **18.8 keV** | 15.0 keV | 1.07×10⁶ |
| Compton | 16.8 keV | 13.3 keV | 2.11×10⁵ |

- **CEvNS reconstructs to TENS OF eV** E_rec (`E_rec ≈ 0.5·E_dep`, down to ~2.5 eV):
  the flagship low-recoil signal sits very low on the observable axis (~85% of its
  reconstructed counts below 100 eV E_rec). It is **not** entirely below the
  10/50/100 eV reference thresholds for both designs, so the ROADMAP stop condition
  is **NOT triggered** — the spectrum is **surfaced honestly, not forced/reshaped**.
- **The muon channel (MeV–197 MeV deposits) is reconstructed ENTIRELY under
  saturation**, piling up at tens of keV E_rec — direct evidence the saturating
  response (not the deposit axis) is applied (`fp-deposited-only`). The pile-up is
  an **instrument artifact of the modelled ceiling, not a physical spectral line**.

### The four standing caveats (carried honestly into the deliverable)

1. **Sub-1.8 MeV reactor-flux model** — Kopeikin-2012-cited placeholder shape; no
   machine-readable table sourceable in-environment (none fabricated). ~6–10% on the
   CEvNS rate below 95 eV_nr; covered by the split flux band.
2. **Site-dependent environmental γ flux** — factor-2 band; Compton total-rate
   MEDIUM, edges HIGH.
3. **NO saturated-regime response anchor** — the saturated-regime E_rec *shape* has
   no literature anchor at any energy; validation is **limiting-cases-only**
   (low-E 0.5 slope by calibration; high-E bounded plateau). The muon spectrum is
   almost entirely in this regime.
4. **f_prompt/r crossover band** — the low-confidence sharing parameters
   (`f_prompt ∈ [0.1,0.5]`, `r ∈ [1,5]`) set the crossover onset as a **band**
   (~53/32 eV default point → 13.1/7.9 keV equal-split anchor → 18.6/11.3 keV
   whole-array plateau); the saturation-onset lines inherit that uncertainty.

### Key stage-1 results (compact)

- **Billard 2017 reproduced** within **2.4%** (0.7415/0.5009/0.2567 vs 0.76/0.51/0.26
  counts/kg/day above 50/100/200 eV_nr, with the derived rescale k = 0.0111).
- **CEvNS ~68 counts/kg/day above 50 eV_nr (deposited)** at OUR 3 GW_th / 25 m config
  (67.75; ~90× Billard, matching the power/distance ratio).
- **Muon 1.37 Hz** (Gaisser-Guan × ray-box chord × Landau-Vavilov MPV; within ~15%
  of PDG 1.5–2 Hz). **Compton 0.268 Hz.**
- **Pileup occupancy 3.3×10⁻⁵** (R·τ at 50 kHz sampling; 6.5×10⁻⁵ at 25 kHz
  resolving) — quiescent reconstruction not precluded.
- **Reconstructed CEvNS peaks at tens of eV E_rec** (~42 eV); muon saturates to
  tens of keV; Compton continuum near tens of keV.

_Phase-6 addendum authored under Plan 06-02; closes the stage-1 milestone. Does not
supersede the Phase-1 lock (`GPD/CONVENTIONS.md`)._
