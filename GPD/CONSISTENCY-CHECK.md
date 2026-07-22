# Stage-1 Milestone (v1.0) — Cross-Phase Consistency Check

**Scope:** milestone (Phases 01–06, full scoped chain)
**Checker:** gpd-consistency-checker (between-phase coherence only; within-phase correctness is the verifier's domain)
**Date:** 2026-07-21
**Overall verdict:** **CONSISTENT** — one genuine cross-artifact inconsistency (LOW, documentation/auditability only), plus several already-documented scoped caveats. No notation conflicts, no parameter mismatches, no broken reasoning chains.

Route on `gpd_return.status` at the end of this file; the headings here are presentation only.

---

## 1. End-to-end narrative coherence

The six phases tell one complete, single-scale story, and each boundary is numerically traceable:

convention (P1) → flux Φ(E_ν) (P2) → CEvNS dR/dT (P3) → muon+Compton dR/dE_dep (P4) → response R(E_rec|E_dep) (P5) → reconstructed dR/dE_rec (P6).

The load-bearing physical thread — **a single unified phonon energy scale with NO ionization quenching** (CONVENTIONS §B) — holds unbroken end to end. CEvNS nuclear-recoil deposits (labeled `eV_nr`), muon and Compton electron-recoil deposits (phonon eV) all enter the **same** E_dep grid and are folded through the **same** response matrix with **no scale conversion**. `grep` confirms no active Lindhard / quenching / keVee code path anywhere in `src/`. This is the central cross-phase coherence point and it is sound.

---

## 2. Load-bearing cross-phase transfers (meaning / units / test value / convention)

| # | Producer → Consumer | Physical meaning | Units | Concrete test value | Convention | Verdict |
|---|---|---|---|---|---|---|
| T1 | P2 Φ(E_ν) → P3 CEvNS fold | reactor ν̄ flux folded against dσ/dT | ν̄·cm⁻²·s⁻¹·MeV⁻¹ | flagship ∫Φ dE = 7.50e12 (P2) consumed by P3; Billard variant 4.586e12 consumed with k=0.0111 | same 3 GW_th/25 m normalization (§D) | ✓ |
| T2 | P3 dR/dT (`eV_nr`, deposited, no quenching) → P6 fold | CEvNS deposited-recoil spectrum onto shared phonon grid | counts·kg⁻¹·day⁻¹ | 67.752 >50 eV (P3) → rebinned 67.67 (0.12%); full-spectrum 109.6 | eV_nr mapped 1:1 to phonon eV — unified scale, no keVee (§B) | ✓ |
| T3 | P4 muon/Compton dR/dE_dep → P5 R and P6 fold | ER deposits on the shared no-quench grid | counts·kg⁻¹·day⁻¹ | muon 1.366 Hz → 1.0739e6 (matches 1.073e6); Compton 0.26846 Hz → 2.107e5 (matches 2.110e5), mass 0.1099 kg | phonon scale, zero Frenkel for ER (§B) | ✓ |
| T4 | P1 energy_scale chain → P5 response.py | forward chain reused, E_rec estimator replaces the P1 stub | eV / Hz | E_rec/E_dep = 0.498/0.497 low-E; non-par plateau ~34.8/26.8 keV @197 MeV | E_rec≈0.5·E_dep, 25 kHz ceiling (§B/§E/§F) | ✓ |
| T5 | P5 R(E_rec|E_dep) npz → P6 fold | bandwidth-limited transfer matrix | probability (columns sum to 1) | counts conserved to ~1e-16; grid seam guarded at runtime (fold raises on mismatch) | non-paralyzable only folded (§F resolved) | ✓ |
| T6 | `params.py` → all phases | frozen shared constants | (mixed) | ε=0.5, τ_d=40µs⇒25.0 kHz, 8.29e24 atoms/kg, 109.9 g/0.1099 kg, 3 GW_th/25 m, N_sens=10300 | single source of truth; P3 verifier confirmed no hardcoded convention constants | ✓ |

**Grid identity (T3/T5):** `shared_energy_grid()` has a single definition in `muon_deposit.py` (584 bins, 10 eV→200 MeV top edge; first bin center 10.14 eV, highest center ~197 MeV). `compton_deposit.py` and `deposited_spectra.py` import it (byte-identical; P4 recorded `np.array_equal True`). `response_matrix.py` reads the same grid centers from `data/combined_dRdEdep.csv`; `fold.py` reuses the npz `E_dep_edges/centers` and asserts each channel matches to `<1e-6` at runtime. No divergent grid anywhere.

---

## 3. Active-convention audit (CONVENTIONS.md §A–§H against milestone scope)

| Convention (machine label) | Applies to scope | Status |
|---|---|---|
| I/O units counts·kg⁻¹·day⁻¹·keV⁻¹ (§A.1) | all output phases | ✓ used uniformly |
| `natural_units` internal-CEvNS-only + (ħc)² (§A.2) | P3 only | ✓ P3-verified; other phases correctly SI-practical |
| k_B explicit (§A.3) | P1/P5 QP dynamics | ✓ (irrelevant to P2/P3/P4/P6 outputs — marked irrelevant) |
| Unified phonon scale, no quenching (§B, `energy_scale_chain`) | every channel | ✓ central coherence point; no quenching in `src/` |
| `coupling_convention` CEvNS /4π, sin²θ_W=0.2387, Q_W (§C) | P3 only | ✓ P3-verified (σ(72Ge,4MeV)=1.0026e-40) |
| Detector normalization 110 g + per-kg (§D, `detector_normalization`) | P2–P6 | ✓ consistent dual bookkeeping (per-kg rates; 0.1099 kg for Hz) |
| `efficiency_mapping` ε≈0.5 (§E) | P5/P6 | ✓ `calibrate_C` reads `params.EPSILON`; ~0.483 MC median at floor is a disclosed ~3% nuance |
| Bandwidth censoring non-paralyzable (§F) | P5/P6 | ✓ physics consistent; **machine lock stale — see Finding F1** |
| Symbol registry (§G) | all | ✓ notation consistent (see §4) |
| QFT categories N/A (§H) | none | ✓ irrelevant by subfield (marked, not skipped) |

---

## 4. Notation consistency

No silent redefinitions. `E_dep`, `E_rec`, `T ≡ E_nr`, `ε`, `Γ_in`, `τ_d`, `N_qp`, `n_qp` are used per the §G registry across all phases. Two clarifications (neither a conflict):

- **`n_qp` (density, µm⁻³) vs `N_qp` (count) vs `expected_n_qp`:** distinct and consistent. Phase 5 deliberately **repurposes the external qpd-repo variable name `expected_n_qp`** to carry the tunneling-**event** count ∫Γ_in dt = K·τ_qp·N_qp/V_tr, **not** the trapped-QP count — the documented "Pitfall-1" mapping, applied consistently in `response.py`/`response_matrix.py`. Repurposing an external library's name (not a project symbol) is documented, not a drift.
- **`T` (CEvNS nuclear recoil, §G) vs `T_e` (Compton electron recoil, P4):** disambiguated by subscript; no collision.

---

## 5. Approximation-regime compatibility

- **Non-paralyzable censoring** adopted project-wide at the Phase-5 review (user decision 2026-07-21). P5 computed both variants; P6 folds **only** `R_non_paralyzable` into deliverables (paralyzable retained as labeled sensitivity). `params.DEFAULT_CENSORING = "non_paralyzable"` matches. No phase relies on the paralyzable limit in a deliverable. ✓
- **Unified phonon, no quenching** applied identically in CEvNS (NR) and muon/Compton (ER) channels; no phase applies a limit another contradicts. ✓
- **Form-factor regime:** P3's "F² > 0.998" (sub-200 eV dominant regime) vs "0.964 at 2 keV endpoint" was explicitly reconciled in P3 to avoid a downstream misflag — the two numbers describe different recoil regimes, not a contradiction. ✓

---

## 6. Findings

### F1 — Stale machine convention-lock for `bandwidth_censoring` (severity: LOW; documentation/auditability, NOT physics)

`state.json → convention_lock.custom_conventions.bandwidth_censoring` still reads:

> "…paralyzable-vs-non-paralyzable AND merge-vs-drop kept as EXPLICIT CODE SWITCH (not fixed); OPEN QUESTION BLOCKS Phase 5; both variants must be implementable"

This contradicts the **RESOLVED → non-paralyzable** decision (2026-07-21) that is correctly recorded in CONVENTIONS.md §F + Change Log, the `state.json` decisions array, `params.DEFAULT_CENSORING`, and Phase 6. CONVENTIONS.md declares `state.json → convention_lock` the **"Authoritative lock,"** and its header still says **"Projection status: synced / Last updated 2026-07-20 (Phase 1)"** — both stale for §F.

- **Producer:** Phase 1 (lock author) / Phase 5 (resolver). **Consumer:** any convention audit that reads the authoritative machine lock.
- **Downstream physics impact:** **none.** Code and Phases 5/6 consistently use non-paralyzable; the pipeline is coherent. The impact is that an auditor trusting the declared source-of-truth would read the switch as still OPEN/blocking.
- **Not my authority to edit** (convention-authoring / shared-state writes are out of scope). Recommend `gpd:validate-conventions` to re-sync the lock string and the CONVENTIONS.md header metadata.

### F2 — REQUIREMENTS.md CALC-01 flux wording vs convention target (severity: LOW; requirements wording)

`REQUIREMENTS.md` CALC-01 quotes "~1×10¹³ ν/cm²/s"; CONVENTIONS.md §D target is 7–8×10¹². Phase 2 used the honest 7.50×10¹² and surfaced the discrepancy for the orchestrator. All downstream consumes 7.5e12 — no cross-phase break; a requirements-wording reconciliation remains open (orchestrator bookkeeping).

### F3 — Plan-text `claim-band` "20–25%" superseded by computed 6–10% (severity: INFO; bookkeeping)

The 03-02 plan text guessed a 20–25% low-recoil flux band; the rigorous rate-weighted propagation gives 3.5%→6.2%→9.8% (200/50/20 eV) with sub-1.8-MeV rate fraction 18–34%. The **corrected** value is what propagated (STATE decisions, ASSUMPTIONS.md, P6 all use 6–10% / 18–34%); only the original plan wording is stale. Orchestrator reword pending; no physics impact.

### F4 — CEvNS sub-10 eV data retained vs user 10 eV plot-floor (severity: INFO; display advisory)

Phase 6 correctly **retains** the CEvNS 5–10.14 eV low edge in the data CSV (7.27 counts/kg/day, mapped E_rec≈2.5–5.0 eV; `fp-drop-lowE-cevns` guarded). This is below the user's "never display below 10 eV" plot-floor memory. Data retention is correct; whether the deliverable figure `reconstructed_energy_spectra.pdf` floors the **displayed** axis at 10 eV could not be verified from artifact metadata alone. Advisory for the plot-floor convention only — the CEvNS peak (~42 eV) sits well above the floor, and this is not a cross-phase physics inconsistency.

---

## 7. Classification of the two known caveats (as requested)

**(a) Sub-1.8 MeV reactor-flux placeholder — ACCEPTABLY SCOPED, not a consistency problem.** Consistently flagged in Phase 2, and its uncertainty band is consistently propagated Phase 2 → 3 → 6 with the corrected magnitude (6–10% below 95 eV; 18–34% sub-1.8 rate fraction). It touches only low-recoil CEvNS bins and is within the phase goal ("modeled extension with an explicit band"). The meaning of the placeholder does not change between phases; the band is carried, not dropped or silently re-interpreted. This is a bounded modeling limitation, not a between-phase disagreement.

**(b) Phase-2/3 "expert_needed" verification status — ACCEPTABLY SCOPED, verifier-domain, not a consistency problem.** `expert_needed` is a within-phase verification verdict about domain-expert judgment on placeholder adequacy (and the eV_ee CONUS+ caveat) — the gpd-verifier's territory, not between-phase coherence. The Billard geometry rescale k=0.0111 is internally consistent (two derivations agree to 0.25%; reproduces Table 1 to <2.5%; without-k overshoot = exactly 1/k). No two phases disagree on its meaning, units, or value.

---

## 8. What was checked and found clean

- Parameter values (T6): every value the task named (3 GW_th/25 m, 110 g / 8.29e24 atoms/kg, N_sens≈10,300, ε=0.5, τ_d=40 µs ⇒ 25.0 kHz ceiling, the two Table-II trap designs) matches `params.py`; no phase substitutes a different value.
- Rate-unit coherence: Hz → counts·kg⁻¹·day⁻¹ conversions reproduce the P6 numbers exactly using mass 0.1099 kg; per-kg-vs-110 g dual bookkeeping is consistent, no double-count.
- No keVee/keVnr mixing; no quenching applied on the phonon scale in any channel.
- CEvNS convention factors (/4π, (ħc)², sin²θ_W=0.2387, Q_W) internally and downstream consistent (P3 independently re-derived).
- The "1 kg crystal" framing flagged STALE in §D is not propagated into any phase's active normalization.

---

## Machine return

```yaml
gpd_return:
  status: completed
  files_written: [GPD/CONSISTENCY-CHECK.md]
  issues:
    - "F1 (LOW, documentation): state.json convention_lock.custom_conventions.bandwidth_censoring is STALE — still says the paralyzable/non-paralyzable switch is an OPEN code switch that BLOCKS Phase 5, contradicting the RESOLVED->non_paralyzable decision (2026-07-21) in CONVENTIONS.md Section F, params.DEFAULT_CENSORING, and Phase 6. CONVENTIONS.md header 'Projection status: synced / Last updated 2026-07-20' is likewise stale. No physics impact; auditability only. Fix is out of my authority."
    - "F2 (LOW, requirements wording): REQUIREMENTS.md CALC-01 '~1e13' vs CONVENTIONS.md D target 7-8e12; Phase 2 used 7.5e12 and all downstream consumes it. Reconciliation pending (orchestrator)."
    - "F3 (INFO): 03-02 plan-text claim-band '20-25%' superseded by computed 6-10% (sub-1.8 rate fraction 18-34%); downstream consistently uses the corrected value. Orchestrator reword pending; no physics impact."
    - "F4 (INFO, display advisory): Phase 6 correctly retains CEvNS 5-10.14 eV data (E_rec ~2.5-5.0 eV), below the user 10 eV plot-floor memory; whether the deliverable figure floors the displayed axis at 10 eV was not verifiable from artifact metadata."
  next_actions:
    - "gpd:validate-conventions"
    - "gpd:suggest-next"
  phase_checked: "Stage-1 milestone (Phases 01-06)"
  checks_performed: 24
  issues_found: 4
```
