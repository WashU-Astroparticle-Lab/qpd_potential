# Phase 1: Conventions & Energy-Scale Foundation - Research

**Researched:** 2026-07-20
**Domain:** Superconducting quasiparticle (parity) detector device parameters; dead-time/bandwidth counting statistics; athermal-phonon energy sharing
**Depth:** standard (tightly scoped to the open quantitative inputs; canonical conventions are already locked)
**Confidence:** MEDIUM-HIGH (Table II device values HIGH from the anchor paper; Ta absorber gap MEDIUM; phonon-sharing defaults LOW by construction)

> Scope note: The canonical conventions (unified no-quenching phonon scale, CEvNS `/4π` + Q_W + (ħc)² units, σ(Ge,4 MeV) benchmark, ε≈0.5, 40 µs resolving time, censoring-as-switch, detector normalization) are ALREADY WRITTEN and LOCKED in `GPD/CONVENTIONS.md` and `GPD/state.json`. This file does NOT re-derive them. It pins down only the still-open quantitative inputs Phase 1 must seed into `ASSUMPTIONS.md`: (1) the Table II device parameters for the yield and tunneling-rate map, (2) the design→parameter mapping, (3) the two censoring-switch variant definitions, (4) the localized+diffuse phonon-sharing default + range.

<user_constraints>

## User Constraints (from CONTEXT.md)

See `01-CONTEXT.md` for full locked decisions. Constraints binding on this research:

### Locked Decisions

- **Energy sharing model = localized-near-hit + diffuse tail.** Prompt fraction `f_prompt` near the impact point (a spot of sensors, position-dependent), remainder spreads diffusely. Chosen over global equal-split so per-sensor deposits can saturate. Muon deposit collapsed to a point and passed through the SAME model (no along-track line spread in stage 1).
- **Yield map = N_qp = ε·E_sensor/Δ_tr**, ε≈0.5 (imposed, lumps phonon collection + pair-breaking + trapping + Δ_abs/Δ_tr multiplication), quantum = trap gap Δ_tr. Tunneling rate Γ_in = K·n_qp, n_qp = N_qp/V_tr, K and V_tr per design from Table II. Peak Γ_in vs 25 kHz defines saturation.
- **Frenkel-defect storage = 0** for stage 1 (E_ph = E_dep for all channels); documented as a few-% NR-only systematic to revisit.
- **Default censoring variant = non-paralyzable** (fixed 40 µs dead window, arrivals during it dropped, window not extended) for headline plots; paralyzable and merge-vs-drop remain as explicit code switches.
- **E_rec estimator deferred to Phase 5.** Phase 1 fixes only the E_rec axis and the saturation *definition*.

### Agent's Discretion (recommendations delivered below)

- Localization defaults (`f_prompt`, `r`) — literature-motivated default + range recommended in this file (Section: Phonon-Sharing Model).
- Γ_in = K·n_qp parameters (K, V_tr per design) — resolved from Table II below.
- E_rec estimator definition — OUT OF SCOPE (Phase 5).

### Deferred Ideas (OUT OF SCOPE — do NOT research or plan)

- Along-track (line) muon energy sharing; per-design efficiency split; localization-scale sensitivity scan; full G4CMP position-dependent phonon-collection model.
</user_constraints>

<active_anchor_references>

## Active Anchor References

Contract-critical inputs (mandatory, not background):

- **ref-qpd-paper — Ramanathan et al. (2026), APS Open Sci. 1, 000013, DOI 10.1103/kqd2-spb1 / arXiv:2405.17192.** Table II (read directly from the PDF, p. 14) is the source for every device parameter below. The pulse model Eq. (4), Γ_in = K·n_qp, S_avg Eq. (14), and the Fano/residual-QP noise definitions were read from pp. 14-15. **Required action: use and cite Table II verbatim; do not paraphrase values from memory.**
- **ref-qpd-repo — `qpd/src/qpd/simulator/quasiparticle_bursts.py`.** EMG burst template (`QuasiparticleBurstModel`: N~Poisson(expected_n_qp); offsets = Normal(µ,σ) + Exp(τ); absolute times = t0 + offsets). This realizes the per-event tunneling time profile that the censoring model operates on. **Required action: reuse verbatim in Phase 5; Phase 1 only needs its parametrization to define "peak instantaneous rate."**
- **GPD/CONVENTIONS.md** — locked canonical conventions; every value here must stay consistent (Section G symbol registry, Section E ε≈0.5, Section F 40 µs / 25 kHz).
- **`qpd/src/qpd/theory/materials.yaml`** — gap/DOS database. Contains Al, AlMn, Hf, Nb, TiN. **Confirmed: NO tantalum entry** — this is a genuine gap flagged below.
</active_anchor_references>

<research_summary>

## Summary

The one paper this phase depends on is Ramanathan et al. (2026); its Table II tabulates four hypothetical devices — Aluminum and Hafnium traps, each in CPB and OCS styles — with the exact parameters the yield/tunneling-rate map needs (V_tr, Δ, K, n_0, τ_qp, τ_inj, Γ_out, Fano F). All values below were read directly from the PDF (p. 14) and are internally BCS-consistent with their tabulated T_c. The critical resolution for planning is the **design→parameter mapping**: Table II is indexed by TRAP material (the paper states it only tracks absorbed energy E_abs and treats "trap material choices (aluminum versus hafnium)"), so the project's "Ta→Al" design uses the **Aluminum** column for junction parameters (K, V_tr, Δ_tr) with tantalum supplying only the absorber gap Δ_abs, and "Al→Hf" uses the **Hafnium** column with aluminum as absorber. Both designs satisfy the Δ_abs/Δ_tr ≳ 2-4 trapping requirement (Ta→Al: 3.6; Al→Hf: 4.75).

Two quantitative findings matter for planning. **(1)** The tantalum absorber gap is genuinely absent from the local database and not tabulated in the paper; it must be supplied as an assumption — bulk α-Ta (T_c ≈ 4.48 K) gives Δ_Ta ≈ 0.68 meV via BCS, but thin-film Ta (α vs β phase) varies widely, so this is a stated assumption with MEDIUM confidence, not a device measurement. **(2)** The Hf-vs-Al saturation asymmetry is real but ~3×, not the 5-10× that the `N_qp ∝ 1/Δ_tr` argument alone suggests: Table II gives Hf a 10× larger V_tr and 6.7× larger K, which partly offset the 4.75× gap advantage, leaving a net Γ_in-per-eV ratio of ~3.2. The saturation-onset per-sensor energy is ~0.1 eV (Hf) vs ~0.32 eV (Al) at the plateau (raised ~4× once the two-exponential peak factor is applied) — order-eV, so muon deposits (tens of MeV, localized) saturate deeply while spread-out CEvNS deposits stay linear. Saturation is physically reachable, satisfying the CONTEXT acceptance signal.

For censoring, the standard dead-time references (Knoll Ch. 4; Usman & Patil review 2018) give clean closed forms for both switch variants at τ_d = 40 µs; both are unambiguously specified below. The localized+diffuse sharing defaults (`f_prompt`, `r`) have no direct thin-wafer QPD measurement — the CDMS/SuperCDMS athermal-phonon position-dependence literature motivates the *structure* (prompt/ballistic near-hit vs. thermalized diffuse) but not the numbers; defaults are geometric-argument estimates exposed as scannable parameters with LOW confidence, exactly as CONTEXT requests.

**Primary recommendation:** Seed `ASSUMPTIONS.md` with the Table II parameter table below (indexed by trap material), the Δ_abs assumptions (Ta ≈ 0.68 meV FLAGGED as gap-filled, Al = 0.19 meV from Table II), the two censoring-variant definitions, and `f_prompt = 0.3` (range 0.1-0.5) / `r = 2` sensors (range 1-5) as exposed parameters. Add a tantalum entry to a project-local materials note with the BCS-derived gap and a citation, marked as an assumption to firm up in Phase 5.
</research_summary>

<device_parameters>

## Device Parameters (Table II, Ramanathan et al. 2026, read from PDF p. 14)

Transcribed verbatim. "Style" columns CPB / OCS; material blocks Aluminum / Hafnium. Values that span a material block (a single value under both CPB and OCS) are noted as "(per material)". Style-only values (same across materials) are noted as "(per style)".

| Parameter | Al-CPB | Al-OCS | Hf-CPB | Hf-OCS | Applies to | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| V_tr (trap volume) | 100 µm³ | 50 µm³ (×2) | 1000 µm³ | 500 µm³ (×2) | per style; **effective total 100 (Al) / 1000 (Hf) µm³** either way | HIGH |
| T_c | 1.2 K | 1.2 K | 0.25 K | 0.25 K | per material | HIGH |
| T_opr (operating) | 0.1 K | 0.1 K | 0.025 K | 0.025 K | per material | HIGH |
| Δ (trap gap Δ_tr) | 190 µeV | 190 µeV | 40 µeV | 40 µeV | per material | HIGH |
| E_abs (example deposit) | 200 meV | 200 meV | 40 meV | 40 meV | per material (illustrative only) | HIGH |
| n_0 (quiescent QP density) | 0.3 µm⁻³ | 0.3 µm⁻³ | 0.03 µm⁻³ | 0.03 µm⁻³ | per material | HIGH |
| E_J/h | 4.9 GHz | 6.14 GHz | 4.9 GHz | 6.14 GHz | per style | HIGH |
| E_C/h | 11.1 GHz | 356 MHz | 11.1 GHz | 356 MHz | per style | HIGH |
| ξ (E_J/E_C proxy) | 0.5 | 17 | 0.5 | 17 | per style | HIGH |
| Fano factor F | 0.2 | 0.2 | 0.2 | 0.2 | global | HIGH (paper flags "to be experimentally validated") |
| τ_qp (recomb. lifetime) | 1 ms | 1 ms | ~400 µs | ~400 µs | Al = 1 ms (table); **Hf ≈ 400 µs (caption/lit [92], not the 1 ms table cell)** | HIGH (Al) / MEDIUM (Hf) |
| τ_inj (injection) | 2 ms | 2 ms | 2 ms | 2 ms | global | HIGH |
| K (tunneling proportionality) | 3 kHz·µm³ | 3 kHz·µm³ | 20 kHz·µm³ | 20 kHz·µm³ | per material | HIGH |
| Γ_out (back-tunneling) | 2 kHz | n/a | 10 kHz | n/a | CPB only; n/a for OCS | HIGH |

**Reading notes:**
- **K units are kHz·µm³**, so Γ_in [Hz] = K [Hz·µm³] · n_qp [µm⁻³]. This is dimensionally consistent with paper Eq. (14) S_avg = (K/V_tr)·N_qp^r·τ_qp (a dimensionless count).
- **V_tr effective total is style-independent:** Al 100 µm³ (CPB) = 50×2 µm³ (OCS); Hf 1000 µm³ = 500×2 µm³. The "×2" is the two-junction OCS split. **Phase 1's yield/rate map therefore does NOT need to pick CPB vs OCS** — use effective V_tr = 100 µm³ (Al) / 1000 µm³ (Hf) and K per material. E_J/E_C/ξ differ by style but enter only a full χ_{i,p} readout model (out of scope for Phase 1).
- **τ_qp for Hf:** the table cell reads "1 ms" (footnote b, positioned in the Al block); the caption explicitly states Hf thin-film QP lifetimes are ~400 µs from literature [92] with "no serious R&D effort" to extend them. Recommend τ_qp = 1 ms (Al), τ_qp ≈ 400 µs (Hf) as the design values, flagged as the paper's own caveat.
- **BCS consistency check (verified):** Δ = 1.764 k_B T_c gives 182 µeV (Al, T_c=1.2K) vs tabulated 190; 38 µeV (Hf, T_c=0.25K) vs tabulated 40. Both within thin-film enhancement — the table is internally consistent.
</device_parameters>

<design_mapping>

## Design → Parameter Mapping Resolution

The paper (Sec. IV, p. 13) states it investigates "different trap material choices (aluminum versus hafnium)" and "only deal[s] with absorbed energy E_abs bounds" to avoid absorber-specific phonon-coupling and diffusion effects. **Therefore Table II is indexed by TRAP/junction material; the absorber is abstracted into E_abs and is NOT a Table II column.** This confirms the CONTEXT reading:

| Project design | Trap/junction (→ Table II column) | Absorber (→ Δ_abs, external) | Δ_tr | Δ_abs | Δ_abs/Δ_tr | K | V_tr (eff.) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Ta→Al** | Al ⇒ **Aluminum** column | Ta | 190 µeV | ≈0.68 meV (assumed) | ≈3.6 | 3 kHz·µm³ | 100 µm³ |
| **Al→Hf** | Hf ⇒ **Hafnium** column | Al | 40 µeV | 190 µeV (Table II Al) | ≈4.75 | 20 kHz·µm³ | 1000 µm³ |

- **"Ta→Al" = Ta absorber + Al trap/junction.** Junction params (K, V_tr, Δ_tr, n_0, T_opr, Γ_out) are the **Aluminum** Table II values. Tantalum supplies ONLY Δ_abs and the Δ_abs/Δ_tr down-conversion multiplication (already lumped into ε≈0.5 per CONVENTIONS Section E). **Confirmed reading.**
- **"Al→Hf" = Al absorber + Hf trap/junction.** Junction params are the **Hafnium** Table II values. Aluminum supplies Δ_abs = 190 µeV (Table II Al gap). Note Al plays the trap role in design 1 and the absorber role in design 2 — same gap (0.19 meV) in both roles.
- **Both designs satisfy the trapping requirement Δ_abs/Δ_tr ≳ 2-4** (Ta→Al: 3.6; Al→Hf: 4.75), so QPs relax into the trap and cannot return — the gap hierarchy is valid for both.

**Finding — the design asymmetry is ~3×, not 5-10×.** The CONTEXT expectation ("Hf yields ~5-10× more QP/eV") is correct for N_qp alone (N_qp ∝ 1/Δ_tr → 190/40 = 4.75×). But the *tunneling rate* Γ_in = K·ε·E/(Δ_tr·V_tr) also carries K and V_tr:
`Γ_in^Hf / Γ_in^Al = (K_Hf/K_Al)·(Δ_Al/Δ_Hf)·(V_Al/V_Hf) = (20/3)·(190/40)·(100/1000) ≈ 3.2`.
The 10× larger Hf trap volume and 6.7× larger K partly cancel the gap advantage. **Hf saturates at ~3× lower per-sensor energy than Al — a real but milder asymmetry than the 1/Δ_tr argument implies.** The planner should state the saturation ordering as a Γ_in-based result (not an N_qp-based one).
</design_mapping>

<censoring_variants>

## Bandwidth / Dead-Time Censoring — Two Switch Variants

Standard dead-time counting statistics (Knoll, *Radiation Detection and Measurement* 4th ed. Ch. 4; Usman & Patil, *Nucl. Eng. Tech.* 50, 1006 (2018), DOI 10.1016/j.net.2018.06.014). Resolving time **τ_d = 40 µs** (= 1/25 kHz, the Nyquist resolving time; NOT the 20 µs sampling interval — see CONVENTIONS Section F). Both variants must be implementable; the DEFAULT is non-paralyzable.

### Variant A — Non-paralyzable (DEFAULT, headline plots)

- **Rule:** after a registered tunneling event, impose a fixed dead window of τ_d = 40 µs. Events arriving within the window are DROPPED and do NOT extend the window; the detector re-arms exactly τ_d after the last *registered* event.
- **Observed rate:** `m = Γ / (1 + Γ τ_d)`, monotonic, **saturating at 1/τ_d = 25 kHz** as Γ → ∞.
- **Event handling:** "drop" (default) — dropped events simply lost. The "merge" sub-switch instead counts one registered event per dead window (still one count, but timestamp = window start).

### Variant B — Paralyzable

- **Rule:** every arriving event (even one during dead time) RESETS/extends the dead window by τ_d. The detector is "live" to register a new count only after a full τ_d gap with no arrivals.
- **Observed rate:** `m = Γ · e^{−Γ τ_d}`, non-monotonic — **peaks at Γ = 1/τ_d = 25 kHz then DECREASES** (rolls over) at higher input rate. This is the qualitatively important difference: a paralyzable readout mis-reads very high Γ as a *low* count rate, aliasing deep-saturation muons toward low reconstructed energy unless the time-over-saturation estimator (Phase 5) is used.

### Peak instantaneous rate definition (feeds both variants)

Saturation is defined by **peak Γ_in vs 25 kHz**, so "peak" must be unambiguous. Two consistent definitions:
- **Analytic (expected intensity):** Γ_in(t) = K·δn_qp,trap(t) with the paper Eq. (4) two-exponential pulse δn_qp,trap(t) = (N_qp^r/V_tr)·(τ_qp/(τ_inj−τ_qp))·(e^{−t/τ_inj} − e^{−t/τ_qp}). Peak of the shape factor at t* = [τ_inj τ_qp/(τ_inj−τ_qp)]·ln(τ_inj/τ_qp). For Al (τ_inj=2 ms, τ_qp=1 ms) the peak shape factor ≈ 0.25; for Hf (τ_inj=2 ms, τ_qp≈0.4 ms) ≈ 0.13. So **peak Γ_in ≈ p·K·N_qp/V_tr** with p ≈ 0.25 (Al) / 0.13 (Hf).
- **Stochastic (EMG realization):** the `QuasiparticleBurstModel` draws N~Poisson(expected_n_qp) events with offsets Normal(µ,σ)+Exp(τ); peak instantaneous rate = max event density over a τ_d-width sliding window of the sorted `event_times`. Use `expected_n_qp = N_qp` and (µ,σ,τ) tied to (τ_inj, τ_qp). This is the Phase-5 MC realization the censoring step operates on.

**Rough saturation-onset per-sensor energy (illustrative sanity, NOT a Phase-1 deliverable):** setting plateau Γ_in = K·N_qp/V_tr = 25 kHz gives E_sensor = 25 kHz·Δ_tr·V_tr/(K·ε) ≈ **0.32 eV (Al) / 0.10 eV (Hf)**; applying the two-exponential peak factor raises these ~4-8× to order **1 eV**. Muon deposits (tens of MeV, localized to a few sensors) exceed this by ≫10⁶ → deep saturation; spread CEvNS deposits (sub-keV over many sensors) stay ≪ this → linear. **Confirms saturation is physically reachable — the CONTEXT acceptance signal.** Exact crossover per design is a Phase-5 number.
</censoring_variants>

<phonon_sharing>

## Localized + Diffuse Phonon-Sharing Model — Default + Range

**Status: LOW confidence by construction.** No direct thin-wafer QPD measurement of the prompt fraction or localization scale exists. The CDMS/SuperCDMS athermal-phonon literature (CDMS-II ZIP position dependence; Phonon-Based Position Determination in SuperCDMS iZIP, arXiv:1405.4215) establishes the *structure* — phonon collection is position-dependent, with a prompt/ballistic component absorbed near the hit and a thermalized/quasi-diffusive component that homogenizes over many surface reflections — but not the numbers for this 2 mm Ge wafer with one instrumented face at 1/mm².

**Model:** a deposit at position **x** deposits a fraction `f_prompt` of its collected phonon energy locally, distributed over a spot of characteristic radius `r` (in sensor pitches) centered on the projection of **x** onto the instrumented face; the remaining `(1 − f_prompt)` spreads diffusely (≈ uniform) across all ~10,300 sensors. Both `f_prompt` and `r` are exposed as scannable parameters.

**Recommended defaults (geometric-argument, expose as parameters):**

| Parameter | Default | Range | Motivation |
| --- | --- | --- | --- |
| `f_prompt` | 0.3 | 0.1 – 0.5 | Prompt/ballistic fraction before homogenization; minority-but-substantial in athermal-phonon detectors (CDMS position-dependence magnitude). Honest wide band. |
| `r` (spot radius) | 2 sensors | 1 – 5 sensors | Lateral spread of ballistic phonons crossing a 2 mm wafer before first hitting the instrumented face ≈ wafer thickness ≈ 2 mm ≈ 2 sensor pitches (1 mm pitch). Spot ≈ π r² ≈ 3–30 sensors. |

**Why these and not equal-split:** equal-split among ~10,300 sensors makes per-sensor CEvNS deposits ~10⁻⁴ eV and per-sensor muon deposits ~keV — well below the ~1 eV saturation onset for muons too — so NOTHING saturates and the muon compression feature vanishes. `f_prompt` ≳ 0.1 with `r` ≲ 5 puts localized muon deposits at ≫ eV per sensor, restoring saturation. The **equal-split limit (`f_prompt → 0`) is the required sanity knob**: turning localization off must remove the muon saturation feature (CONTEXT disconfirming check).

**Honesty flag for the planner:** `f_prompt` and `r` are the least-constrained numbers in the entire pipeline and the muon spectrum shape depends strongly on them. They MUST be presented as assumptions with a scan range, never as derived values. This is the phase's weakest anchor (matches CONTEXT skeptical review).
</phonon_sharing>

<known_results>

## Known Results and Benchmarks (to leverage, not re-derive)

### Existing Results to Leverage

| Result | Value / Expression | Source | Confidence |
| --- | --- | --- | --- |
| Yield map | N_qp^r = E_abs·η_tr·η_pb,tr/Δ_tr (paper) ≡ N_qp = ε·E_sensor/Δ_tr (project, ε≈0.5 lumps the η chain) | Ramanathan Sec. IV; CONVENTIONS Section E | HIGH |
| Tunneling rate | Γ_in = K·n_qp, n_qp = N_qp/V_tr | Ramanathan Table II + text; CONVENTIONS Section G | HIGH |
| Pulse shape | δn_qp,trap(t) two-exponential, Eq. (4) | Ramanathan Eq. (4) | HIGH |
| Expected total transitions | S_avg = (K/V_tr)·N_qp^r·τ_qp, Eq. (14) | Ramanathan Eq. (14) | HIGH |
| Al trap gap | Δ_Al = 190 µeV (T_c 1.2 K) | Table II; materials.yaml (1.89e-4 eV) | HIGH |
| Hf trap gap | Δ_Hf = 40 µeV (T_c 0.25 K, thin film) | Table II | HIGH (design value); materials.yaml uses 22.5 µeV (bulk T_c 0.128 K) — see Open Questions |
| Ta absorber gap | Δ_Ta ≈ 0.68 meV (bulk α-Ta, T_c 4.48 K, BCS 1.764 k_B T_c) | BCS + PDG/standard Ta T_c; **NOT in materials.yaml** | MEDIUM (bulk); film phase-dependent |
| Dead-time laws | non-paralyzable m=Γ/(1+Γτ_d); paralyzable m=Γe^{−Γτ_d} | Knoll Ch. 4; Usman & Patil 2018 | HIGH |
| EMG burst generator | N~Poisson; offsets Normal(µ,σ)+Exp(τ) | `quasiparticle_bursts.py` | HIGH |

### Don't Re-Derive

| Problem | Use Instead | Why |
| --- | --- | --- |
| Superconducting gaps from T_c | Table II tabulated Δ (Al 190, Hf 40 µeV); BCS 1.764 k_B T_c only for Ta | Table II already gives design gaps; re-deriving risks bulk-vs-film confusion (materials.yaml Hf 22.5 µeV ≠ Table II 40 µeV) |
| Dead-time observed-rate curves | Closed forms above | Textbook results; re-deriving invites the paralyzable/non-paralyzable sign-of-slope error |
| Pulse peak time / shape factor | t* and p≈0.25(Al)/0.13(Hf) above | Standard two-exponential extremum; error-prone by hand with τ_inj>τ_qp ordering |
| ε efficiency chain | ε≈0.5 imposed (CONVENTIONS Section E) | Locked; the paper's physical η_ce≈0.3 is a cross-reference only, NOT the baseline |

**Key insight:** every number Phase 1 needs already exists in Table II or a locked convention — the phase is bookkeeping and mapping, not computation. The only value that must be *supplied* (not read) is the Ta absorber gap.
</known_results>

<common_pitfalls>

## Common Pitfalls

### Pitfall 1: Treating the Hf advantage as N_qp-scaled (5-10×) instead of Γ_in-scaled (~3×)

**What goes wrong:** quoting Hf saturating 5-10× lower than Al, using only N_qp ∝ 1/Δ_tr.
**Why it happens:** ignoring that Table II gives Hf a 10× larger V_tr and 6.7× larger K, which enter Γ_in = K·N_qp/V_tr.
**How to avoid:** compute the saturation ordering from Γ_in, not N_qp. Net ratio ≈ 3.2×.
**Warning signs:** a stated Hf/Al crossover-energy ratio far from ~3.

### Pitfall 2: Using the 20 µs sampling interval as the dead time

**What goes wrong:** setting τ_d = 20 µs → non-paralyzable saturation at 50 kHz, not 25 kHz.
**Why it happens:** conflating the 50 kHz sampling (20 µs) with the 25 kHz resolving time (40 µs).
**How to avoid:** τ_d = 40 µs for both censoring variants (CONVENTIONS Section F).
**Warning signs:** saturation ceiling comes out at 50 kHz.

### Pitfall 3: Inventing a tantalum gap or importing the wrong film phase

**What goes wrong:** silently using a memorized Ta gap, or a β-Ta film value (T_c ~0.5-1 K) where bulk α-Ta (4.48 K) is intended.
**Why it happens:** materials.yaml has no Ta entry; α vs β Ta differ by ~5-9× in T_c.
**How to avoid:** state Δ_Ta ≈ 0.68 meV as an ASSUMPTION (bulk α-Ta, BCS) with a citation; flag film-phase sensitivity; add a Ta entry to a project materials note marked "assumption."
**Warning signs:** Δ_abs/Δ_tr ratio for Ta→Al falling outside ~2-4 (would break trapping).

### Pitfall 4: Presenting f_prompt / r as derived

**What goes wrong:** the muon spectrum looks precise but rests on unmeasured localization numbers.
**Why it happens:** the localized+diffuse model has no thin-wafer QPD measurement.
**How to avoid:** always expose f_prompt, r as scanned parameters; include the equal-split (f_prompt→0) limit as a sanity check that must kill the muon feature.
**Warning signs:** a muon compression feature that is stable under large f_prompt/r variation (should be strongly dependent) — or one that survives f_prompt→0 (would be an artifact).
</common_pitfalls>

<validation_strategies>

## Validation Strategies

- **BCS gap consistency:** Δ = 1.764 k_B T_c must reproduce Table II Δ within thin-film enhancement (verified: Al 182 vs 190, Hf 38 vs 40, Ta 681 µeV). Any project materials note for Ta must pass this.
- **Trapping check:** Δ_abs/Δ_tr ∈ [2,4]-ish for both designs (Ta→Al 3.6 ✓; Al→Hf 4.75 ✓). If a chosen gap breaks this, trapping is invalid.
- **Dimensional check on Γ_in:** K [kHz·µm³] · n_qp [µm⁻³] → kHz; and K/V_tr·N_qp·τ_qp → dimensionless count (Eq. 14). Both must hold.
- **Saturation reachability:** with the recommended f_prompt/r, per-sensor muon deposit ≫ ~1 eV crossover (saturates) AND per-sensor CEvNS deposit ≪ crossover (linear). If either fails, the sharing or yield map is mis-specified.
- **Equal-split limit:** f_prompt → 0 must remove muon saturation (turns off the compression feature). Required disconfirming check.
- **Low-E linearity:** E_rec ≈ 0.5·E_dep must hold for unsaturated (CEvNS, most Compton) events (CONVENTIONS Section B/E test value).
- **Censoring limits:** non-paralyzable m(Γ) → 25 kHz as Γ→∞; paralyzable m(Γ) peaks at 25 kHz then rolls over. Unit-test both curves against the closed forms.
</validation_strategies>

<key_equations>

## Key Equations and Starting Points

```
# Yield (CONVENTIONS Section E; Ramanathan Sec. IV)
N_qp   = ε · E_sensor / Δ_tr          # ε ≈ 0.5 lumps η_ph·η_pb·η_tr + Δ_abs/Δ_tr multiplication
n_qp   = N_qp / V_tr                  # per-sensor QP density

# Tunneling rate (Ramanathan Table II + text)
Γ_in   = K · n_qp = K · ε · E_sensor / (Δ_tr · V_tr)

# Pulse shape (Ramanathan Eq. 4) — defines peak instantaneous rate
δn_qp,trap(t) = (N_qp^r / V_tr) · (τ_qp/(τ_inj − τ_qp)) · (e^{−t/τ_inj} − e^{−t/τ_qp})
t*     = [τ_inj τ_qp/(τ_inj − τ_qp)] · ln(τ_inj/τ_qp)
peak Γ_in ≈ p · K · N_qp / V_tr       # p ≈ 0.25 (Al: τ_inj=2ms,τ_qp=1ms); ≈ 0.13 (Hf: τ_qp≈0.4ms)

# Saturation definition (CONVENTIONS Section F)
saturated  ⇔  peak Γ_in > 25 kHz  (= 1/40 µs)

# Censoring switch (Knoll Ch.4; Usman & Patil 2018), τ_d = 40 µs
non-paralyzable (DEFAULT):  m = Γ / (1 + Γ τ_d)        # → 25 kHz ceiling
paralyzable:                m = Γ · e^{−Γ τ_d}          # peaks at 25 kHz, rolls over

# Per-design parameters (Table II, indexed by TRAP material)
Ta→Al:  Δ_tr=190 µeV, V_tr=100 µm³,  K=3  kHz·µm³, τ_qp=1 ms,  Δ_abs≈0.68 meV (Ta, assumed)
Al→Hf:  Δ_tr=40  µeV, V_tr=1000 µm³, K=20 kHz·µm³, τ_qp≈0.4 ms, Δ_abs=190 µeV (Al)

# Phonon sharing (localized + diffuse) — exposed parameters
f_prompt = 0.3 (range 0.1–0.5);  r = 2 sensors (range 1–5)
E_sensor = f_prompt · E_dep · (localized weight on spot) + (1−f_prompt) · E_dep / N_sensors
```

### Package / Framework Reuse Decision

**Reuse `quasiparticle_bursts.py` directly (verbatim import) for the EMG per-event time profile; wrap it with a thin bespoke censoring/yield layer.** The burst generator (`QuasiparticleBurstModel`, `poisson_burst_times`) is numpy-only and exactly realizes the per-event tunneling process the censoring model needs — no reason to reimplement. The **missing capabilities** that justify a thin bespoke layer (Phase 5, not Phase 1): (1) the dead-time censoring step (merge/drop, paralyzable/non-paralyzable) operating on `event_times`; (2) the E_dep→N_qp→expected_n_qp yield map with the Table II per-design parameters; (3) the localized+diffuse per-sensor sharing weights. All three are small and project-specific. For Phase 1 itself (a bookkeeping/definition phase) **no code is written** — the deliverable is `CONVENTIONS.md` updates + `ASSUMPTIONS.md`; the reuse decision is recorded for Phase 5.
</key_equations>

<open_questions>

## Open Questions

1. **Tantalum absorber gap for the Ta→Al design.**
   - What we know: bulk α-Ta T_c ≈ 4.48 K → Δ_Ta ≈ 0.68 meV (BCS). Gives Δ_abs/Δ_tr ≈ 3.6, valid trapping.
   - What's unclear: thin-film Ta phase (α vs β) shifts T_c from ~4.5 K (α) down to ~0.5-1 K (β); the fabricated film phase is unspecified. materials.yaml has NO Ta entry.
   - Recommendation: adopt Δ_Ta ≈ 0.68 meV (bulk α-Ta) as a STATED ASSUMPTION with citation; add a Ta entry to a project materials note flagged "assumption, firm up in Phase 5"; carry film-phase as a systematic. Do NOT invent a film-specific number.

2. **Hf trap gap: 40 µeV (Table II) vs 22.5 µeV (materials.yaml).**
   - What we know: Table II design uses T_c=0.25 K → 40 µeV; materials.yaml uses bulk T_c=0.128 K → 22.5 µeV.
   - What's unclear: which the project intends. CONVENTIONS says "Hf ~20-40 µeV" (spans both).
   - Recommendation: use the Table II design value Δ_Hf = 40 µeV for the yield map (it is the anchor-paper device); note materials.yaml lower value as the low end of a systematic band.

3. **CPB vs OCS style.**
   - What we know: effective V_tr and K are style-independent for the yield/rate map; only E_J/E_C/ξ and Γ_out differ.
   - What's unclear: which style the full Phase-5 readout model adopts.
   - Recommendation: Phase 1 needs no choice (map is style-independent). Flag for Phase 5; if forced, CPB has the fuller Table II (Γ_out defined).

4. **τ_qp for Hf (400 µs) vs the "1 ms" table cell.**
   - What we know: caption states Hf ~400 µs (lit [92]); table cell reads 1 ms (Al-side footnote b).
   - Recommendation: τ_qp = 1 ms (Al), ≈400 µs (Hf); treat as the paper's own flagged uncertainty.
</open_questions>

<not_found>

## What Was NOT Found

- **Tantalum in `qpd/src/qpd/theory/materials.yaml`** — confirmed absent (only Al, AlMn, Hf, Nb, TiN). No local Ta gap/DOS/T_c. Must be supplied as an assumption.
- **Direct thin-wafer QPD measurement of f_prompt or r** — none exists (checked anchor paper, Sandoval et al. 2025, and CDMS position-dependence literature). CDMS/SuperCDMS confirm the *structure* (position dependence, prompt vs. thermalized) but give no transferable number for a 2 mm Ge wafer at 1/mm² single-face instrumentation.
- **A single K value split by CPB/OCS** — Table II gives K per material only (3 / 20 kHz·µm³); no style-resolved K. Treated as per-material.
- **Published high-rate (multi-MeV) QPD saturation/reconstruction data** — none (consistent with SUMMARY open question); the crossover energy is a Phase-5 computation with no external anchor.
</not_found>

<sources>

## Sources

### Primary (HIGH)

- **Ramanathan et al., APS Open Sci. 1, 000013 (2026), DOI 10.1103/kqd2-spb1 / arXiv:2405.17192** — Table II device parameters (read directly from `/Users/lanqingyuan/Desktop/QPD.pdf` p. 14); pulse Eq. (4), S_avg Eq. (14), Γ_in=K·n_qp, Fano F=0.2, residual-QP σ²=16 n_0 V, Sec. IV trap-material framing (p. 13). The design→trap-material indexing is verified against the paper's own text.
- **`qpd/src/qpd/simulator/quasiparticle_bursts.py`** — EMG burst generator (read directly); parametrization of per-event time profile.
- **`qpd/src/qpd/theory/materials.yaml`** — Al/Hf/Nb/TiN gaps (read directly); Ta absence confirmed.
- **GPD/CONVENTIONS.md** — locked conventions (ε≈0.5, 40 µs/25 kHz, symbol registry, yield map).
- **Knoll, *Radiation Detection and Measurement* (4th ed.), Ch. 4** — paralyzable/non-paralyzable dead-time models [textbook, background knowledge].

### Secondary (MEDIUM)

- **Usman & Patil, *Nucl. Eng. Tech.* 50, 1006 (2018), DOI 10.1016/j.net.2018.06.014** — dead-time/pile-up review; confirms both idealized models and that model choice is not settled a priori (motivates the switch). Verified via search.
- **BCS gap relation Δ = 1.764 k_B T_c** with bulk Ta T_c ≈ 4.48 K (α-Ta) → Δ_Ta ≈ 0.68 meV. Ta α/β phase T_c behavior verified via search (α-Ta ~4.3-4.5 K; β-Ta lower/variable).
- **CDMS-II ZIP position dependence (NIST/AIP Conf. Proc. 605, 509); Phonon-Based Position Determination in SuperCDMS iZIP, arXiv:1405.4215** — motivates localized+diffuse structure (prompt/ballistic vs. thermalized); does NOT provide f_prompt/r for this geometry.

### Tertiary (LOW — needs validation in Phase 5)

- `f_prompt = 0.3` (0.1-0.5), `r = 2` sensors (1-5) — geometric-argument defaults, no direct measurement.
- Δ_Ta ≈ 0.68 meV — bulk α-Ta assumption; thin-film phase unverified for this device.
- Hf τ_qp ≈ 400 µs — paper caption literature value, "no serious R&D" caveat.
</sources>

<caveats_and_alternatives>

## Caveats and Alternatives (adversarial self-critique)

- **Am I sure Table II is indexed by trap, not absorber?** The paper explicitly frames Sec. IV as "trap material choices (aluminum versus hafnium)" and states it uses absorbed-energy E_abs bounds to avoid absorber-specific effects — so the columns are trap materials and the absorber is external. This is the natural reading and matches the project's gap hierarchy (both designs give valid Δ_abs/Δ_tr). Residual risk: if the paper's "Aluminum" device silently assumed an Al absorber too, then the project's Ta→Al swaps only the absorber, which is exactly what the mapping does — no inconsistency. Confidence HIGH.
- **The ~3× (not 5-10×) Hf finding depends on trusting Table II's 10× larger Hf V_tr and 6.7× larger K.** These are read directly from the table and are internally consistent (K ∝ E_J via K≈16 E_J k_B T/(𝒩Δh); Hf's lower Δ and T raise K). If the project chose to normalize V_tr equal across designs (a design choice, not the paper's), the asymmetry would revert toward ~5×. The planner should state the asymmetry as *conditional on Table II V_tr/K*, and expose them if a different device sizing is assumed.
- **The saturation-onset ~1 eV estimate is sensitive to the peak factor p and to ε.** p ranges 0.13-0.25 across designs and the two-exponential ordering; ε carries a ±10-20% band. The order-eV conclusion (muons saturate, CEvNS linear) is robust to these — the margins are many orders of magnitude — so the qualitative acceptance signal holds even if the exact crossover moves by ~10×.
- **The phonon-sharing defaults are the weakest link and I will not pretend otherwise.** The muon spectrum morphology is genuinely a function of f_prompt and r, which are unmeasured. The only defense is exposing them and enforcing the equal-split sanity limit. A competing explanation for any muon "compression feature" — that it is an artifact of the arbitrary point-collapse plus localization rather than real readout saturation — must be actively tested (CONTEXT disconfirming check), not assumed away. This is correctly a LOW-confidence, parameter-exposed input, not a result.
- **Alternative dead-time model considered and NOT adopted for the default:** the binned-Bernoulli / "≥1 event per resolvable window" model (m = (1/Δt)(1−e^{−ΓΔt})) from METHODS Domain 4 is a defensible third option that maps cleanly to "max resolvable rate." It is NOT the CONTEXT default (non-paralyzable) but should remain available as the same explicit switch; it interpolates between the two idealized limits and may be the most physical for a digitized readout. Flag for Phase 5, do not silently substitute.
</caveats_and_alternatives>

<metadata>

## Metadata

**Research scope:**
- Physics subfield: superconducting quasiparticle-tunneling detector device parameters; dead-time counting statistics; athermal-phonon energy sharing.
- Methods explored: direct Table II transcription (PDF); BCS gap consistency; dead-time closed forms; EMG burst parametrization; geometric phonon-spread argument.
- Known results catalogued: Table II (4 devices), yield/rate map, pulse peak factor, both censoring laws, design→trap mapping, Δ_abs/Δ_tr ratios.
- Pitfalls: N_qp-vs-Γ_in asymmetry, 20-vs-40 µs, Ta gap invention, unexposed sharing parameters.

**Confidence breakdown:**
- Device parameters (Table II): HIGH — read directly, BCS-consistent.
- Design→parameter mapping: HIGH — confirmed against paper text.
- Censoring variants: HIGH — textbook closed forms.
- Ta absorber gap: MEDIUM — bulk assumption, film phase unverified, absent from local DB.
- Phonon-sharing defaults: LOW — no measurement; exposed as parameters by design.

**Research date:** 2026-07-20
**Valid until:** 2026-08-19 (30 days — established device paper + textbook statistics; phonon-sharing numbers are placeholders regardless)

---

_Phase: 01-conventions-energy-scale-foundation_
_Research completed: 2026-07-20_
_Ready for planning: yes_
</metadata>
