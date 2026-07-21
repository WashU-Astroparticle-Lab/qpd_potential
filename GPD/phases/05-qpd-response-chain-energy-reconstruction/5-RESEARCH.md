# Phase 5: QPD Response Chain & Energy Reconstruction - Research

**Researched:** 2026-07-21
**Domain:** Superconducting quasiparticle (parity) sensors; bandwidth-limited point-process readout; energy reconstruction under hard readout saturation
**Depth:** deep
**Confidence:** MEDIUM (the forward chain and its limits are HIGH; the saturated-regime response shape is a MODEL PREDICTION with NO literature anchor at any energy — this is the phase's defining difficulty and is stated repeatedly below)

<user_constraints>

## User Constraints (from CONTEXT.md)

**No CONTEXT.md exists** — `gpd:discuss-phase` was not run for this phase. There are therefore no user-locked decisions specific to Phase 5. Intent is inferred from the roadmap goal, `GPD/REQUIREMENTS.md` (SIMU-01, SIMU-02, VALD-04), the project contract in `GPD/state.json` (claim-response, obs-energy-response, deliv-fig-response, deliv-code, test-response-limits), `GPD/CONVENTIONS.md` Sections B/E/F/G, and the substantial Phase-1 scaffold already in `src/qpd_potential/`.

Two decisions were **deferred from Phase 1 to Phase 5** and are the agent's to make here, with justification (they are made below, not punted):

- **D-estimator:** which real `E_rec` estimator to implement (count-integral vs time-over-saturation vs hybrid auto-switch). The Phase-1 `E_rec_estimator` is a deliberate stub.
- **D-censoring:** the paralyzable-vs-non-paralyzable (and merge-vs-drop) censoring rule, recorded in CONVENTIONS Section F as an **OPEN SWITCH that must NOT be silently resolved**.

**All other decisions are at agent's discretion** and are exercised prescriptively below.
</user_constraints>

<active_anchor_references>

## Active Anchor References

Contract-critical anchors (mandatory inputs, not background reading):

| Anchor | What it is | How Phase 5 MUST use it |
| --- | --- | --- |
| **ref-qpd-paper** — Ramanathan et al., APS Open Sci. 1, 000013 (2026), DOI 10.1103/kqd2-spb1 / arXiv:2405.17192 | QPD concept paper. Pulse model **Eq. 4**, efficiency chain, `Γ_in = K·n_qp`, **Table II** device parameters. | Source of truth for the pulse shape and every device constant. Already transcribed verbatim into `src/qpd_potential/params.py` — **cite/reuse, do NOT re-transcribe from memory.** |
| **ref-qpd-repo** — `/Users/lanqingyuan/Documents/GitHub/qpd/src/qpd/simulator/quasiparticle_bursts.py` (**MUST-USE**) | `QuasiparticleBurstModel(times, tau, mu, sigma, expected_n_qp)` + `poisson_burst_times`, `BurstTruth`. Generates EMG-profiled bursts of tunneling events. | The **stochastic realization** of each sensor's tunneling-event train. Import via `sys.path.insert(0, '/Users/lanqingyuan/Documents/GitHub/qpd/src')`, submodule path only (top-level package pulls `qutip`). **See Pitfall 1 — the `expected_n_qp` argument must be fed the expected TUNNELING-EVENT count, not the trapped-QP count.** |
| **Phase-1 scaffold** — `src/qpd_potential/energy_scale.py`, `params.py` | Full forward chain already implemented (sharing → yield → density → tunneling rate → peak factor → saturation onset → censoring switch). `E_rec_estimator` is the Phase-5 stub. | **Build on it — do not re-derive.** Phase 5 implements the real `E_rec_estimator` and the MC response-matrix driver; everything upstream exists and is unit-tested. |
| **Phase-4 inputs** — `data/combined_dRdEdep.csv` (muon+Compton, to 197 MeV), `artifacts/stage1/cevns_dRdT.csv` (CEvNS, to ~3.2 keV_nr) | Deposited-energy spectra. | Define the **E_dep range R must span**: sub-keV (CEvNS/linear) to ~200 MeV (muon tail/deep-saturated). Grid is log, 0.01 keV → 2×10⁵ keV, ~80 bins/decade. |
| **CONVENTIONS.md B/E/F/G** | Locked energy chain (no quenching), ε≈0.5, the OPEN censoring switch, gaps. | Binding. Section F's open switch is the D-censoring decision below; Section B's no-quenching / unified scale is non-negotiable. |

Contract deliverables this phase advances: **deliv-fig-response** = `artifacts/stage1/energy_response.pdf` (E_rec vs E_dep, saturation onset marked, both designs); **deliv-code** = `src/` forward-chain + MC-response-matrix module.

**Forbidden proxy (fp-no-saturation):** no bandwidth-saturation modeling. Extrapolating the linear rate→energy map across the muon range fakes a peak at the ceiling. The saturation MUST be modeled explicitly. The recommended estimator satisfies this by construction (its plateau IS the modeled saturation).
</active_anchor_references>

<research_summary>

## Summary

Phase 5 turns the Phase-1 forward-chain scaffold into a working reconstructed-energy response. Almost every physical stage already exists and is unit-tested in `src/qpd_potential/energy_scale.py`: per-sensor energy sharing (`sensor_energy_split`), QP yield (`n_qp_yield`), tunneling rate `Γ_in = K·n_qp` (`tunneling_rate`), the two-exponential peak factor (`peak_factor`), the saturation-defining peak instantaneous rate (`peak_tunneling_rate`), the per-sensor saturation onset (`saturation_onset_energy`), and both dead-time censoring closed forms (`observed_rate`, non-paralyzable default + paralyzable). The **one genuinely missing piece** is the real `E_rec` estimator (a deliberate stub), plus the Monte-Carlo driver that assembles the response matrix `R(E_rec | E_dep)` per design.

The recommended estimator is the **count-integral (censored-tunneling-count) estimator**, calibrated so the low-energy linear slope equals ε = 0.5. In the linear regime the censored tunneling-event count summed over the array is proportional to E_dep, giving `E_rec ≈ 0.5·E_dep` (VALD-04 low-E limit — partly definitional through calibration). In the saturated regime the on-spot sensors' instantaneous tunneling rate exceeds the 25 kHz resolving ceiling, the censored count per sensor caps, and the summed count — hence E_rec — **plateaus**. That plateau is the physically correct, explicitly-modeled saturation (it satisfies fp-no-saturation; it is NOT a linear extrapolation faking a peak). A **time-over-saturation** estimator (`t_sat ≈ τ_qp·ln(Γ_peak/Γ_thr)`, logarithmic in E_dep) is recommended as a documented **secondary/optional response-matrix variant** that recovers slowly-rising high-E ordering, explicitly flagged as τ_qp-dependent and unvalidated — but the count-integral estimator is the honest deliverable because its plateau makes the saturation boundary visible rather than hiding it behind an auto-switch.

The dominant, repeated caveat: **the saturated regime has NO published result at any energy.** Validation is limiting-cases-only (low-E linearity by calibration; high-E plateau/saturation-onset). The response curve *shape between the limits is a model prediction, not validated against data.* Two further honest findings shape the plan: (1) the **crossover deposit energy** is dominated by the LOW-confidence sharing parameter `f_prompt` and must be reported as a wide band (~tens of eV localized → ~10 keV equal-split), not a single number; (2) the **Ta absorber gap** is not a smooth response-curve band but a **binary trapping gate** — the Ta→Al response is numerically independent of the Ta gap as long as α-phase Ta keeps Δ_abs/Δ_tr ≥ ~2, while β-phase Ta would invalidate the design premise.

**Primary recommendation:** Implement the **count-integral estimator calibrated to slope 0.5**, drive it with a per-sensor forward MC that reuses `QuasiparticleBurstModel` for the tunneling-event realization and the Phase-1 `observed_rate` censoring, and build `R(E_rec|E_dep)` per design **carrying BOTH censoring variants** and reporting the crossover E_dep as an `f_prompt`-band. Provide the time-over-saturation estimator as a labeled secondary variant. Stamp the no-literature-anchor caveat on every saturated-regime output.
</research_summary>

<literature_landscape>

## Literature Landscape

### Foundational Papers

| Paper | Authors | Year | Key Result | Relevance |
| --- | --- | --- | --- | --- |
| Quantum parity detectors (arXiv:2405.17192, DOI 10.1103/kqd2-spb1) | Ramanathan et al. | 2026 | QPD scheme; two-exponential pulse Eq. 4; `Γ_in = K·n_qp`, `K ≈ 16 E_J k_B T/(𝒩Δh)`; efficiency chain η_ph·η_pb·η_tr ≈ 0.32; Table II device params; CPB tunneling asymmetry (occupied island blocks entry) | THE anchor. Pulse shape + every device constant. Note the paper does **not** specify a saturated-regime reconstruction — that is exactly this project's novel computation. |
| Radiation Detection and Measurement, ch. 4 | Knoll | 2010 | Non-paralyzable `m = Γ/(1+Γτ_d)` (saturates at 1/τ_d) and paralyzable `m = Γ·e^{−Γτ_d}` (rolls over) dead-time models | Both closed forms already coded in `observed_rate`. The paralyzable/non-paralyzable choice is the OPEN switch (D-censoring). |
| Dead-time & pileup review, Nucl. Eng. Tech. 50, 1006 | Usman & Patil | 2018 | Systematic comparison of dead-time models; when each applies | Supports carrying both variants; confirms the choice is not decidable from electronics generalities. |
| Rothwarf–Taylor equations, PRL 19, 27 | Rothwarf & Taylor | 1967 | Coupled QP/phonon ODEs; phonon bottleneck; bimolecular recombination `n(t)=n₀/(1+R̃n₀t)`, τ_qp ∝ 1/n_qp at high density | Governs τ_qp in the muon regime. Relevant IF the estimator uses τ_qp (time-over-saturation variant); the baseline count-integral estimator does not require solving RT. |

### Recent Advances / Context

| Paper | Authors | Year | Key Result | Relevance |
| --- | --- | --- | --- | --- |
| QPD device characterization (arXiv:2509.18637) | Sandoval et al. | 2025 | Measured QPD device behavior | Tertiary; Ta film parameters **still absent** (checked in project literature). Not a saturated-regime reconstruction anchor. |
| Correlated radiation-induced QP bursts, Nature 594, 369 | Wilen et al. | 2021 | Muons/γ produce crystal-wide correlated phonon/parity bursts | Physics constraint that the on-spot + diffuse sharing model captures (localized spot + array-wide diffuse tail). Not needed for the response curve itself; matters for the Phase-6 background bookkeeping. |
| Time-over-threshold in saturated TES/SNSPD/PMT channels | (general instrumentation) | — | Above the rate cap, energy survives in duration `t_sat ∝ ln E` | The analogy underpinning the secondary time-over-saturation estimator. **Analogy only — no QPD-specific validation exists.** |

### Review Articles / Textbook Treatments

| Source | Coverage | Best For |
| --- | --- | --- |
| Knoll, *Radiation Detection and Measurement* (4th ed.), ch. 4 | Dead-time / counting statistics | The censoring closed forms and their regimes of validity. |
| Project `GPD/literature/METHODS.md` Domain 3–4, `PITFALLS.md` #8–10 | QP chain + reconstruction methods & pitfalls, already synthesized | Starting context — build on these; do not re-survey the whole domain. |

### Notation Conventions Across Sources

| Quantity | Anchor paper | qpd repo | This project (binding) | Notes |
| --- | --- | --- | --- | --- |
| Trapped-QP count per sensor | `N_qp^r` | `expected_n_qp` (arg name) | `N_qp` (`n_qp_yield`) | **Naming collision.** The repo arg is a Poisson mean for a burst of *tunneling events*; in this pipeline feed it the expected tunneling-event count, NOT `N_qp` trapped. See Pitfall 1. |
| Per-QP tunneling rate | `Γ_in = K·n_qp` | (not represented) | `tunneling_rate`, Hz | Parity-flip event rate per sensor. Peak value defines saturation. |
| Resolving/dead time | τ_d | `tau_d` (in censoring) | 40 µs (=1/25 kHz), LOCKED | CONVENTIONS F. Distinct from the 20 µs (50 kHz) sampling interval — state both. |
| EMG decay tail | (pulse τ_qp) | `tau` | map `tau ≈ τ_qp` | EMG (Normal+Exp) approximates the two-exp pulse; see Pitfall 1 mapping. |

**Key notational hazards:** (a) `expected_n_qp` (repo) is an *event-count* Poisson mean, not the trapped-QP number — mis-mapping mis-scales the entire saturation. (b) 40 µs vs 20 µs — the ceiling is 25 kHz (40 µs), NOT 50 kHz. (c) "peak Γ_in" (per-sensor instantaneous tunneling rate, the saturation quantity) vs "plateau Γ_in" (steady `K·n_qp`) — differ by the peak factor p (0.25 Al / 0.13 Hf).
</literature_landscape>

<methods_and_approaches>

## Methods and Approaches

### Standard Analytical / Computational Methods

| Method | When to Use | Limitations | Key Reference / Scaffold |
| --- | --- | --- | --- |
| Two-exponential pulse (Eq. 4) → peak factor p | Every deposit; gives peak instantaneous Γ_in from N_qp | Linear model; τ_qp fixed (valid at CEvNS scale; density-dependent at muon scale) | `peak_factor`, `peak_tunneling_rate` (scaffold) |
| Per-sensor energy sharing (localized spot + diffuse tail) | Map E_dep → E_sensor per sensor class | `f_prompt`, `r` are LOW-confidence EXPOSED params, not derived — dominate the crossover | `sensor_energy_split` (scaffold) |
| Inhomogeneous-Poisson tunneling-event realization via EMG burst | Stochastic per-sensor event train for censoring | EMG ≠ exact two-exp; mapping must preserve total count AND peak instantaneous rate | `QuasiparticleBurstModel` (qpd repo, MUST-USE) |
| Dead-time censoring (non-paralyzable / paralyzable) | Apply the 25 kHz ceiling to the event train | Choice not fixable from first principles → carry BOTH (D-censoring) | `observed_rate` (scaffold) |
| Count-integral estimator, calibrated to slope 0.5 | **BASELINE E_rec estimator** | Plateaus in saturation (that is the point); low-E limit is calibration-definitional | **NEW — this phase (D-estimator)** |
| Time-over-saturation estimator `t_sat ≈ τ_qp·ln(Γ_peak/Γ_thr)` | SECONDARY variant; recovers log-rising high-E ordering | Needs τ_qp (RT density-dependent → MEDIUM); no validation anchor | METHODS.md Domain 4; TES/SNSPD analogy |
| MC response matrix via uniform importance sampling in E_dep | Assemble `R(E_rec|E_dep)` decoupled from steep source spectra | Cost ∝ samples×grid; convergence is a Poisson floor | METHODS.md / COMPUTATIONAL.md |

### The forward chain per (E_dep, design) — build directly on the scaffold

```
E_dep
  → sensor_energy_split(E_dep, f_prompt, r, n_sensors)      # per-sensor E_sensor (on-spot vs off-spot)
  → n_qp_yield(E_sensor, design) = ε·E_sensor/Δ_tr           # trapped-QP count per sensor (Poisson mean)
  → two-exp pulse (τ_inj, τ_qp) → peak instantaneous Γ_in = p·K·N_qp/V_tr
  → QuasiparticleBurstModel(...).sample(rng)                 # EMG tunneling-event train (see Pitfall 1 mapping)
  → observed_rate / event-merge censoring at τ_d = 40 µs     # non_paralyzable AND paralyzable
  → E_rec_estimator(observed counts)                         # count-integral, calibrated to slope 0.5
```

Energy conservation check (already true of the scaffold): `Σ_sensors E_sensor = E_dep` (localized fraction f_prompt + diffuse fraction 1−f_prompt sum to 1). Therefore `Σ_sensors N_qp = ε·E_dep/Δ_tr`, and the count-integral summed over the array is ∝ E_dep in the linear regime — the basis of the slope-0.5 calibration.

### Recommended E_rec estimator (D-estimator decision) — count-integral, calibrated

Define `E_rec = C · Σ_i N_obs,i` where `N_obs,i` is the censored tunneling-event count on sensor i and `C` is a single calibration constant fixed once per design by requiring the low-E linear slope `dE_rec/dE_dep = ε = 0.5`. Justification:

- **It gives both required limits without extrapolation.** Low-E: no sensor saturates → `N_obs = N_true ∝ E_dep` → `E_rec = 0.5·E_dep`. High-E: on-spot (then, for muons, essentially all) sensors saturate → `N_obs` caps at ≈ window/τ_d per sensor → `Σ N_obs` and hence `E_rec` **plateau**. The plateau IS the modeled saturation → satisfies fp-no-saturation and VALD-04 high-E.
- **It is fully codeable from the scaffold** — only the summed-count → energy calibration is new.
- **It is the honest deliverable**: the plateau makes the saturation boundary visible on the response curve (deliv-fig-response requires the saturation onset marked). A silent hybrid auto-switch would *hide* where saturation begins — rejected for the primary deliverable.
- **Calibration honesty:** because C is fixed by the low-E slope, VALD-04's low-E test is largely a *calibration consistency check*, not an independent validation. The non-trivial validated content is (a) that saturation onset appears at the predicted crossover and (b) the plateau level — state this plainly.

**Secondary (optional) variant — time-over-saturation.** In the saturated regime energy survives in the duration the sensor stays above the resolving threshold: `t_sat ≈ τ_qp·ln(Γ_peak/Γ_thr)`, logarithmic in E_dep. Provide a second response matrix `R_tos(E_rec|E_dep)` from this estimator so a reader can see how much high-E ordering is recoverable. **Flag prominently:** it depends on τ_qp (density-dependent via Rothwarf–Taylor at muon densities → MEDIUM) and has NO validation anchor. Do NOT auto-switch between the two silently.

### Building R(E_rec|E_dep) (SIMU-02)

- **Sampling:** uniform importance sampling in `log E_dep` from ~10 eV (below the CEvNS floor; `cevns_dRdT` reaches down to sub-100 eV recoils) to 2×10⁵ keV (200 MeV muon tail), matching the Phase-4 grid (~80 bins/decade → ~600 E_dep columns over ~7.3 decades). Uniform-in-E_dep importance sampling decouples R from the steep physical spectra (direct event-by-event MC of O(1–100)/kg/day CEvNS is statistically useless — COMPUTATIONAL.md).
- **Per column:** draw `N_s` forward realizations; histogram the resulting E_rec into E_rec bins → one normalized column of R. Optimization: the ~10,287 off-spot sensors share one identical E_sensor, so their aggregate censored count can be sampled from one binomial/Poisson-with-censoring per realization rather than looping 10,300 sensors individually; only the ~πr² on-spot sensors need individual treatment.
- **Convergence (≤~3%/cell):** the per-cell error is a Poisson/√N_s floor. `N_s ≈ 1000–5000` realizations per E_dep column gives ≲3% on well-populated cells; report the per-cell MC error as a diagnostic (as Phase 4 already does with `total_mc_err`). Total cost ~10⁶–10⁷ forward evals → laptop-minutes (numpy-vectorized; `numba` only if needed).
- **Reproducibility:** one `numpy.random.default_rng(seed)` per (design, censoring variant); record seed + params (f_prompt, r, N_s, grid edges) in the output metadata header (mirror the Phase-4 CSV header style).

### Computational Tools

| Tool/Package | Version | Purpose | Why Standard |
| --- | --- | --- | --- |
| Python + NumPy/SciPy | ≥3.11 | Forward chain, MC, histogramming | Laptop-scale; matches whole project |
| `qpd.simulator.quasiparticle_bursts` | local repo | EMG tunneling-event realization (MUST-USE) | ref-qpd-repo contract anchor |
| `qpd_potential.energy_scale` / `params` | Phase-1 scaffold | Entire forward chain + censoring already implemented | Build-on, not re-derive |
| matplotlib | current | deliv-fig-response (E_rec vs E_dep) | Standard |
| numba (optional) | current | accelerate MC only if >10⁷ evals | Only if needed |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
| --- | --- | --- |
| Count-integral estimator (baseline) | Hybrid auto-switch count↔time-over-sat | Auto-switch hides the saturation boundary the deliverable must show; rejected as primary, offered as labeled secondary |
| `QuasiparticleBurstModel` EMG realization | Direct analytic thinning of inhomogeneous Poisson with rate `K·n_qp(t)` from the exact two-exp pulse | Analytic thinning is more faithful to the pulse shape but violates the MUST-USE contract; use it only as an internal cross-check of the EMG mapping |
| Fixed τ_qp | Rothwarf–Taylor density-dependent τ_qp | RT needed only if the time-over-saturation variant is pushed to muon densities; baseline count-integral does not need it |
| Per-sensor loop over 10,300 sensors | Aggregate off-spot ensemble analytically | Aggregate is far faster and exact for identical E_sensor; recommended |

### Package / Framework Reuse Decision

**Wrap-and-extend the Phase-1 scaffold + the qpd repo; write only the estimator and the MC driver bespoke.**

- **Reuse directly (no reimplementation):** `sensor_energy_split`, `n_qp_yield`, `qp_density`, `tunneling_rate`, `peak_factor`, `peak_tunneling_rate`, `saturation_onset_energy`, `observed_rate`, `is_saturated` (all in `energy_scale.py`), all Table II constants (`params.py`), and `QuasiparticleBurstModel`/`poisson_burst_times` (qpd repo, MUST-USE per contract).
- **Bespoke (new) code, and why:** (1) the real `E_rec_estimator` (count-integral, calibrated) — the scaffold intentionally stubs it; missing capability = the summed censored-count → energy calibration and the plateau logic. (2) The MC response-matrix driver (`R(E_rec|E_dep)` assembly, importance sampling, convergence bookkeeping, npz/CSV + figure output) — no existing module builds R; integration cost of forcing this into the qpd repo (which targets I/Q-waveform parity simulation, pulls `qutip`) is higher than writing a thin numpy driver in `src/qpd_potential/`.
- **Net:** ~2 new modules (estimator + response-matrix driver) in `src/qpd_potential/`, everything else imported. No new heavy dependency.
</methods_and_approaches>

<known_results>

## Known Results and Benchmarks

### Established Results (from the scaffold / anchor / conventions)

| Result | Value/Expression | Conditions | Source | Confidence |
| --- | --- | --- | --- | --- |
| Saturation ceiling | 25 kHz = 1/τ_d, τ_d = 40 µs | Locked | CONVENTIONS F; `SATURATION_CEILING_HZ` | HIGH |
| Per-sensor saturation onset (E_sensor) | Al ≈ **1.27 eV**, Hf ≈ **0.77 eV** | peak Γ_in = 25 kHz; `E_onset = ceiling·Δ_tr·V_tr/(p·K·ε)` | `saturation_onset_energy` (scaffold) | HIGH (given Table II) |
| Peak instantaneous rate | peak Γ_in = p·K·N_qp/V_tr | Two-exp pulse | `peak_tunneling_rate`; Eq. 4 | HIGH |
| Non-paralyzable censoring | m = Γ/(1+Γτ_d) → 25 kHz as Γ→∞ | Monotone | `observed_rate`, Knoll ch.4 | HIGH |
| Paralyzable censoring | m = Γ·e^{−Γτ_d}, peaks at Γ=1/τ_d then rolls over | Non-monotone | `observed_rate`, Knoll ch.4 | HIGH |
| Trapping ratios | Ta→Al = 3.58, Al→Hf = 4.75 | Δ_abs/Δ_tr ≥ ~2 required | `params.trapping_ratio` | HIGH (α-Ta); see gate below |
| Array-level deadtime is negligible | pileup occupancy ≈ 3.3×10⁻⁵, deadtime frac ≈ 6.5×10⁻⁵ | 1.63 Hz total event rate, 40 µs | `combined_dRdEdep.csv` header | HIGH → saturation is a per-sensor LOCAL effect, not an array-rate effect |

### Limiting Cases (VALD-04 — the ONLY validation available)

| Limit | Expected Behavior | Expression | Source |
| --- | --- | --- | --- |
| E_dep → low (unsaturated, all sensors linear) | `E_rec ≈ 0.5·E_dep` | `E_rec = ε·E_dep`, ε=0.5 | CONVENTIONS B/E; `E_rec_estimator` placeholder |
| peak Γ_in on-spot crosses 25 kHz | Response begins to bend (onset of saturation) | E_dep,cross = E_onset(E_sensor)/[f_prompt/(πr²)+(1−f_prompt)/n_sensors] | scaffold + sharing model |
| E_dep → high (all sensors saturated) | `E_rec` plateaus at ≈ C·n_sensors·(window/τ_d) | count-integral plateau | this phase (model prediction) |
| f_prompt → 0 (equal-split sanity knob) | On-spot = off-spot; crossover moves to keV scale | E_sensor = E_dep/n_sensors | `sensor_energy_split` docstring |

### Crossover deposit energy (SIMU-01) — report as a BAND, not a number

The crossover E_dep (on-spot peak Γ_in = 25 kHz) is set by the on-spot per-sensor share, whose coefficient is `f_prompt/(πr²) + (1−f_prompt)/n_sensors`. With the LOW-confidence defaults (f_prompt=0.3, r=2 → πr²≈12.57, n_sensors=10300): coefficient ≈ 0.0239, so:

| Design | E_sensor onset | Crossover E_dep (default f_prompt=0.3) | Equal-split limit (f_prompt→0) |
| --- | --- | --- | --- |
| Ta→Al (Al trap) | 1.27 eV | ≈ **53 eV_dep** | ≈ **13 keV_dep** (1.27 eV × 10300) |
| Al→Hf (Hf trap) | 0.77 eV | ≈ **32 eV_dep** | ≈ **7.9 keV_dep** (0.77 eV × 10300) |

**These are DERIVED (this file) from the scaffold formula; recompute in-code.** The ~3-orders-of-magnitude spread (tens of eV → ~10 keV) is driven entirely by `f_prompt`, the least-constrained parameter in the pipeline. **The crossover E_dep MUST be reported as an f_prompt∈[0.1,0.5], r∈[1,5] band per design, with the equal-split limit as the upper anchor.** Hf saturates before Al (lower onset) in every case — that ordering is robust.

**Two distinct saturation scales (state both on the figure):** (1) *onset of bending* — on-spot sensors (~πr² of them, carrying f_prompt of the energy) saturate → E_rec bends by ≤ f_prompt; (2) *full plateau* — even the diffuse per-sensor share `(1−f_prompt)·E_dep/n_sensors` reaches onset, so all ~10,300 sensors saturate: E_dep ≈ E_onset·n_sensors/(1−f_prompt) ≈ **18.7 keV (Al) / 11.3 keV (Hf)** at default f_prompt. For a 40 MeV muon every sensor is deep in saturation → the muon reconstructed spectrum piles up at the plateau ceiling (the central, honest prediction; see stop condition).

**Key insight:** the response has a *two-scale* structure — a shallow bend at tens of eV (on-spot) and a hard plateau at ~10–20 keV (whole array) — both f_prompt-dependent. This is the shape the deliverable must show and the shape no experiment has ever measured.
</known_results>

<dont_rederive>

## Don't Re-derive

| Problem | Don't derive from scratch | Use instead | Why |
| --- | --- | --- | --- |
| Two-exponential pulse / peak factor | Re-integrate Eq. 4 | `peak_factor`, `peak_tunneling_rate` (scaffold) | Already implemented; p=0.25 Al / 0.13 Hf recorded from Eq. 4 |
| Tunneling rate `Γ_in = K·n_qp` | Re-derive K | `tunneling_rate` + Table II K (scaffold/params) | Verbatim from anchor Table II |
| Per-sensor saturation onset | Re-solve peak Γ_in = ceiling | `saturation_onset_energy` (scaffold) | Closed form already coded (1.27 eV Al / 0.77 eV Hf) |
| Dead-time censoring m(Γ) | Re-derive paralyzable/non-paralyzable | `observed_rate` (scaffold) | Both Knoll closed forms coded and switchable |
| EMG tunneling-event burst | Re-write an EMG sampler | `QuasiparticleBurstModel` (qpd repo) | MUST-USE per contract; reuse verbatim |
| Table II device constants | Re-transcribe from the paper | `params.py` | Already transcribed verbatim + provenance-tagged; re-typing risks errors |
| Energy chain / no-quenching | Re-argue the phonon scale | CONVENTIONS B (locked) | NR and ER share one scale; Lindhard forbidden |
| CEvNS & muon+Compton deposit spectra | Recompute inputs | `cevns_dRdT.csv`, `combined_dRdEdep.csv` (Phases 3–4) | Frozen upstream deliverables; Phase 5 only folds through R (that fold is Phase 6/SIMU-03) |

**Key insight:** almost the entire physics of Phase 5 is already implemented and unit-tested. The error-prone novelty is narrow: (a) the summed-censored-count → energy calibration and plateau logic, (b) the `expected_n_qp` event-count mapping (Pitfall 1), and (c) not letting the low-E calibration masquerade as independent validation.
</dont_rederive>

<common_pitfalls>

## Common Pitfalls

### Pitfall 1: Feeding trapped-QP count into `expected_n_qp` (event-count mis-scaling)

**What goes wrong:** `QuasiparticleBurstModel.expected_n_qp` is the Poisson mean of the number of **tunneling events (parity flips)** in the burst — NOT the number of trapped quasiparticles `N_qp`. The two differ: the event count over the pulse is `∫Γ_in(t)dt = (K/V_tr)∫N_qp(t)dt`, while `N_qp` is the trapped population. Passing `N_qp` directly conflates a population with an integrated rate and mis-scales the censored count (hence the whole saturation onset and plateau level).
**Why it happens:** the argument is literally named `expected_n_qp`, and the scaffold's `n_qp_yield` returns `N_qp` — an inviting but wrong 1:1 wiring.
**How to avoid:** map the two-exp pulse to the EMG so that (i) `expected_n_qp` = expected tunneling-event count `∫Γ_in dt`, and (ii) the EMG temporal params (`tau≈τ_qp`, `mu,sigma` from the τ_inj onset) reproduce the **peak instantaneous rate** `p·K·N_qp/V_tr` = `peak_tunneling_rate(N_qp)`. Preserve *both* the integral (drives the count-integral estimator) and the peak (drives censoring). Cross-check against an analytic inhomogeneous-Poisson thinning of `K·n_qp(t)` on a few test deposits.
**Warning signs:** saturation onset E_dep disagrees with `saturation_onset_energy` mapped through the sharing model; censored count per sensor does not cap near `window/τ_d`; E_rec plateau level scales with τ_qp in an unphysical way.

### Pitfall 2: Letting the low-E calibration masquerade as validation

**What goes wrong:** the count-integral constant C is fixed by requiring `E_rec = 0.5·E_dep` at low E, so VALD-04's low-E test passes *by construction*. Reporting it as an independent validation overstates confidence.
**Why it happens:** the low-E limit is both the calibration target and a VALD-04 acceptance criterion.
**How to avoid:** state explicitly that low-E linearity is a calibration consistency check; the genuine tests are (a) saturation onset at the predicted crossover E_dep and (b) the plateau level, neither of which is tuned. Keep the calibration to a single global constant per design (do not per-bin tune).
**Warning signs:** more than one free constant in the estimator; low-E residuals suspiciously exactly zero across all bins including the bend region.

### Pitfall 3: Silently picking a censoring variant (violating the OPEN switch)

**What goes wrong:** choosing non-paralyzable (or paralyzable) as "the" model and reporting a single R. CONVENTIONS F forbids this. The two differ *qualitatively* in saturation: non-paralyzable m saturates at 25 kHz (bounded plateau); paralyzable m **rolls over toward zero** for Γ ≫ 25 kHz, so a deeply-saturated sensor reports *near-zero* events — the muon plateau could collapse rather than flatten. The muon-end shape depends on this choice.
**Why it happens:** non-paralyzable is the coded default; one variant is easier to plot.
**How to avoid:** carry BOTH variants through R and report both crossover E_dep and both response curves (or a switch). Discuss — and conclude — that the choice CANNOT be closed from electronics first principles (Usman & Patil; the resolving time is Nyquist-fixed but the recovery behavior is not). Do NOT invent an electronics argument to break the tie.
**Warning signs:** only one response matrix produced; muon plateau presented without the paralyzable rollover alternative.

### Pitfall 4: Treating the Ta gap as a smooth response-curve band

**What goes wrong:** carrying the Ta-film gap uncertainty (±) as a continuous band on the Ta→Al response curve. It is not: Δ_abs (Ta) enters the response arithmetic *nowhere* — `n_qp_yield`, `peak_tunneling_rate`, and `saturation_onset_energy` all use the **trap** gap Δ_tr = Al = 190 µeV. The Ta gap only sets the **trapping gate** Δ_abs/Δ_tr ≥ ~2. So the Ta→Al response is numerically INDEPENDENT of the exact Ta gap as long as trapping holds; the uncertainty is a **binary gate**, not a band.
**Why it happens:** the film-phase warning in `params.DELTA_ABS_TA` (α vs β, T_c shifts 5–9×) looks like a continuous systematic.
**How to avoid:** keep the cited bulk-α-Ta value (0.68 meV, T_c=4.48 K) as baseline; state that the response curve does not depend on it. Report the gate: trapping needs Δ_abs ≥ 2·Δ_tr = 380 µeV → T_c ≥ 380µeV/(1.764 k_B) ≈ **2.5 K**. α-Ta (4.48 K) ✓; β-Ta (T_c ~0.5–2.7 K) marginal/fails → design premise invalid. Frame β-phase as a design-invalidating RISK, not a response band. Any QP-multiplication effect of the large Ta gap is already absorbed into the CONVENTIONS-E ε=0.5 ±10–20% band, shared by both designs — do NOT double-count it as a second axis. Do NOT invent a Ta-film gap value.
**Warning signs:** a Ta→Al response curve that visibly shifts when Δ_abs is varied within α-phase; a fabricated β-Ta film gap appearing in params.

### Pitfall 5: Reading the saturation-ceiling pile-up as a physical spectral peak

**What goes wrong:** the muon reconstructed spectrum piles up at the plateau ceiling; interpreting that pile-up as a Landau-like physical feature. It is an instrument artifact of the modeled saturation.
**Why it happens:** the pile-up looks like a peak.
**How to avoid:** delimit the saturated region on every figure; plot the true→reconstructed mapping alongside the spectrum; label the ceiling. (This is the *correct* modeled behavior — the forbidden proxy fp-no-saturation is the opposite error of extrapolating linearly and faking a peak *at a higher* energy.)
**Warning signs:** muon E_rec extends linearly to tens of MeV (bug: censoring not applied / Pitfall 1); or a sharp "line" at the ceiling reported as physics.

### Pitfall 6: `f_prompt`/`r` treated as known instead of scanned

**What goes wrong:** reporting a single crossover E_dep and a single response curve using the default f_prompt=0.3, r=2 as if they were measured.
**Why it happens:** the scaffold provides defaults.
**How to avoid:** these are EXPOSED, LOW-confidence params (no thin-wafer QPD measurement exists). Scan f_prompt∈[0.1,0.5], r∈[1,5]; report the crossover as a band; include the equal-split limit (f_prompt→0) as the robust upper anchor. The response *shape* (two-scale bend+plateau) is qualitatively robust; the *scale* is not.
**Warning signs:** crossover quoted to 2 sig figs with no band; response curve insensitive to f_prompt (indicates the sharing model is not actually wired in).
</common_pitfalls>

<key_derivations>

## Key Derivations and Formulas

### Per-sensor saturation onset and crossover deposit energy

```
# Source: energy_scale.saturation_onset_energy (scaffold), CONVENTIONS F
peak Γ_in(E_sensor) = p · K · ε · E_sensor / (Δ_tr · V_tr)          # = peak_tunneling_rate(n_qp_yield(E_sensor))
E_onset (E_sensor at ceiling) = ceiling · Δ_tr · V_tr / (p · K · ε)  # Al 1.27 eV, Hf 0.77 eV
E_sensor,on-spot = E_dep · [ f_prompt/(π r²) + (1−f_prompt)/n_sensors ]   # sensor_energy_split, on_spot=True
=> E_dep,crossover = E_onset / [ f_prompt/(π r²) + (1−f_prompt)/n_sensors ]
```
**Valid when:** the on-spot sensor is the first to saturate (monotone sharing). **Breaks down when:** f_prompt→0 (equal split) — then E_dep,crossover = E_onset·n_sensors.

### Count-integral estimator (baseline)

```
# Source: this phase (D-estimator). Calibration constant C fixed once per design.
E_rec = C · Σ_i N_obs,i          # N_obs,i = censored tunneling-event count on sensor i
C chosen s.t. dE_rec/dE_dep = ε = 0.5 in the unsaturated (linear) regime
Linear regime : Σ_i N_obs,i = Σ_i N_true,i ∝ Σ_i E_sensor,i = E_dep  ⇒  E_rec = 0.5·E_dep
Saturated     : N_obs,i → window/τ_d (capped)  ⇒  E_rec → C·n_sat·(window/τ_d)  (plateau)
```
**Valid when:** parity flips resolvable, C globally constant. **Breaks down when:** used to claim high-E energy *resolution* — the plateau erases E_dep ordering (that is the physical saturation, not a fixable defect).

### Time-over-saturation estimator (secondary, unvalidated)

```
# Source: METHODS.md Domain 4; TES/SNSPD/PMT analogy (NO QPD validation)
t_sat ≈ τ_qp · ln(Γ_peak / Γ_thr)      # duration above resolving threshold
E_rec,tos = monotone_calib(t_sat)       # logarithmic in E_dep ⇒ slowly rising in saturation
```
**Valid when:** a secondary estimate of high-E ordering is wanted. **Breaks down when:** τ_qp is taken fixed at muon densities (RT bimolecular: τ_qp ∝ 1/n_qp) — MEDIUM confidence; and there is no benchmark to calibrate `monotone_calib` against.

### EMG ↔ two-exp pulse mapping (for QuasiparticleBurstModel)

```
# Source: qpd repo docstring + anchor Eq. 4. Preserve TWO invariants:
(1) expected_n_qp  = ∫ Γ_in(t) dt              # total tunneling-event count (NOT trapped N_qp)
(2) N·max(EMG_pdf) = p·K·N_qp/V_tr             # peak instantaneous rate = peak_tunneling_rate
tau ≈ τ_qp (decay tail);  mu,sigma from τ_inj onset spread
```
**Valid when:** the EMG width is chosen to hit invariant (2). **Breaks down when:** the Normal+Exp EMG is forced to match the exact difference-of-exponentials shape (it cannot exactly; matching the two invariants is sufficient for count-integral + censoring).
</key_derivations>

<open_questions>

## Open Questions

1. **Paralyzable vs non-paralyzable censoring (D-censoring / CONVENTIONS F).**
   - What we know: both closed forms coded; resolving time 40 µs Nyquist-fixed; they differ qualitatively in saturation (bounded plateau vs rollover-to-zero).
   - What's unclear: which the actual electronics realize — NOT decidable from first principles.
   - Recommendation: carry BOTH through R; report both crossover and both curves; state explicitly it cannot be closed now. Do not silently pick.

2. **Sharing parameters f_prompt, r (LOW confidence, no thin-wafer measurement).**
   - What we know: geometric-argument defaults 0.3 / 2 sensors; scaffold exposes them as scannable.
   - What's unclear: true prompt-localization fraction for a 2 mm wafer with 1/mm² sensors.
   - Recommendation: scan; report crossover as a band; equal-split limit as robust anchor.

3. **Saturated-regime response SHAPE has no literature anchor at any energy.**
   - What we know: limits are pinned (0.5·E_dep low-E by calibration; plateau high-E).
   - What's unclear: everything between the limits (the bend region and plateau approach) is a model prediction.
   - Recommendation: publish R and the true→reconstructed mapping with the saturated region delimited and a NO-BENCHMARK caveat; never present the mid-curve as validated.

4. **Ta film phase (α vs β).**
   - What we know: bulk α-Ta gap 0.68 meV cited; response is Ta-gap-independent within α-phase; β-phase would break trapping.
   - What's unclear: the actual deposited film phase — `materials.yaml` has no Ta entry; a Ta-film citation would need measured T_c (or gap) for the specific sputtered film/stress condition.
   - Recommendation: baseline α-Ta; report the T_c ≥ 2.5 K trapping gate; flag β-phase as design-invalidating; do NOT fabricate a film value.

5. **τ_qp at muon densities (only if time-over-saturation variant pursued).**
   - What we know: Table II τ_qp (1 ms Al / ~0.4 ms Hf) is the low-density value; RT gives τ_qp ∝ 1/n_qp at high density.
   - What's unclear: the effective τ_qp in the deep-saturated muon burst.
   - Recommendation: baseline count-integral estimator avoids this dependence; if time-over-saturation is reported, use the RT bimolecular form and label MEDIUM.
</open_questions>

<not_found>

## What Was NOT Found

- **Any published QPD (or analogous parity-sensor) energy-reconstruction result in the saturated regime, at any energy.** Confirmed absent across the project literature synthesis (SUMMARY/METHODS/PITFALLS all state this explicitly) and the anchor paper (which specifies the pulse and device but not a saturated reconstruction). This is a genuine knowledge gap — validation is limiting-cases-only.
- **Tantalum thin-film superconducting parameters (T_c, gap, phase) for the QPD absorber.** Absent from the qpd repo `materials.yaml` and not in Sandoval et al. (arXiv:2509.18637) at the level needed. Only the bulk α-Ta value (via T_c=4.48 K) is citable.
- **An experimental cross-check for the muon-end reconstructed spectrum morphology.** None exists (Cross-Validation Matrix in SUMMARY.md: the QPD-saturated row has no experiment). Not searched beyond the project synthesis, which already flags it as the highest-risk cell.
- **A first-principles determination of the paralyzable-vs-non-paralyzable behavior of the QPD readout.** The literature (Knoll, Usman & Patil) gives both models but no QPD-specific selection.
</not_found>

<sources>

## Sources

### Primary (HIGH)

- Ramanathan et al., APS Open Sci. 1, 000013 (2026), DOI 10.1103/kqd2-spb1 / arXiv:2405.17192 — pulse Eq. 4, `Γ_in = K·n_qp`, efficiency chain, Table II. *Transcribed verbatim into `params.py`; verified present in project literature.*
- `src/qpd_potential/energy_scale.py`, `params.py` (Phase-1 scaffold) — full forward chain + censoring + saturation onset, unit-tested. *Read directly this session.*
- `/Users/lanqingyuan/Documents/GitHub/qpd/src/qpd/simulator/quasiparticle_bursts.py` — `QuasiparticleBurstModel` EMG burst generator (MUST-USE). *Read directly this session.*
- `GPD/CONVENTIONS.md` Sections B/E/F/G — energy chain (no quenching), ε=0.5, OPEN censoring switch, symbol registry. *Read directly.*
- `GPD/REQUIREMENTS.md` (SIMU-01/02, VALD-04), `GPD/state.json` (claim-response, deliv-fig-response path `artifacts/stage1/energy_response.pdf`, deliv-code `src/`, test-response-limits). *Read directly.*
- Knoll, *Radiation Detection and Measurement* (4th ed.), ch. 4 — dead-time models (both coded in `observed_rate`). *Background knowledge; closed forms cross-checked against scaffold.*

### Secondary (MEDIUM)

- `GPD/literature/METHODS.md` (Domains 3–4), `PITFALLS.md` (#8–10), `SUMMARY.md` — project synthesis of QP chain + reconstruction methods, pitfalls, and the no-anchor caveat. *Starting context, verified against scaffold.*
- Usman & Patil, Nucl. Eng. Tech. 50, 1006 (2018) — dead-time model comparison. *Via project synthesis.*
- Rothwarf & Taylor, PRL 19, 27 (1967) — density-dependent τ_qp (needed only for the time-over-saturation variant). *Via project synthesis.*
- Phase-4 outputs `data/combined_dRdEdep.csv`, `artifacts/stage1/cevns_dRdT.csv` — E_dep range and grid for R. *Read directly (headers + endpoints).*

### Tertiary (LOW — needs validation)

- Sandoval et al., arXiv:2509.18637 — QPD device characterization; Ta film params still absent. *Not fetched this session; per project synthesis.*
- Time-over-threshold analogy from saturated TES/SNSPD/PMT channels — supports the secondary estimator only; NO QPD-specific validation. *Analogy, flagged.*
- Bulk α-Ta gap 0.68 meV (1.764 k_B T_c, T_c=4.48 K) — citable baseline; film phase unverified. *In `params.DELTA_ABS_TA` with MEDIUM confidence + film-phase flag.*
</sources>

<metadata>

## Metadata

**Research scope:**
- Physics subfield: superconducting quasiparticle/parity sensors; bandwidth-limited point-process readout; saturated energy reconstruction.
- Methods explored: count-integral vs time-over-saturation vs hybrid estimators; EMG burst realization; dead-time censoring (both variants); MC response-matrix assembly.
- Known results catalogued: saturation ceiling/onset, crossover E_dep band, two-scale saturation structure, censoring closed forms, trapping-gate for Ta.
- Pitfalls: event-count mapping, calibration-as-validation, silent censoring choice, Ta-gap-as-gate, ceiling pile-up misread, f_prompt sensitivity.

**Confidence breakdown:**
- Literature coverage: MEDIUM — the relevant literature *is* the anchor paper + project synthesis; the saturated regime is genuinely unpublished (honest gap, not a search failure).
- Methods: HIGH for the forward chain and estimator construction (scaffold is complete and unit-tested); MEDIUM for the saturated-regime shape (model prediction).
- Known results: HIGH for the limits and device constants; MEDIUM for the crossover scale (f_prompt-dominated); the mid-curve is a prediction, not a known result.
- Pitfalls: HIGH — grounded in the scaffold's own flags and the conventions' OPEN switch.

**Research date:** 2026-07-21
**Valid until:** 2026-08-20 (30 days; stable — depends on frozen scaffold + conventions, not a fast-moving field).
</metadata>

---

_Phase: 05-qpd-response-chain-energy-reconstruction_
_Research completed: 2026-07-21_
_Ready for planning: yes_
