# Plan 04-03 Summary — Phase-4 Deposited-Energy Spectra Assembly (muon + Compton)

**One-liner:** The Phase-4 muon (04-01) and Compton (04-02) deposited-energy spectra are co-added on the **byte-identical** shared log E_dep grid (584 bins, 0.01 keV → 197 MeV; max relative grid deviation **0.0**), each channel passes **count-rate energy closure** (∫dR/dE_dep dE = rate·86400/mass_kg → muon ratio **0.9993** within its 3.6×10⁻³ MC band, Compton **0.99997**), and the **50 kHz pileup stop-condition** is comfortably clear — total event rate **R_tot = 1.634 Hz** (muon 1.366 + Compton 0.268) gives occupancy **R·τ = 3.3×10⁻⁵** (20 µs sample) / **6.5×10⁻⁵** (40 µs resolving) ≪ 1 with mean inter-event spacing **0.61 s ≫ pulse**, so quiescent reconstruction is not precluded; the within-event muon ~197 MeV long-chord saturation tail is the flagged Phase-5 concern, not a Phase-4 stop-condition trigger.

**Status:** Task 1 (auto) complete and verified (13 new tests; **131/131** whole suite passes). Task 2 (`checkpoint:human-verify`) executed and **self-assessed satisfied, pending orchestrator review** per the autonomous-run directive — **not blocked**.

**Profile/mode:** numerical / balanced autonomy / code-heavy. Phase class: numerical.

---

## Conventions in effect (from `state.json` convention_lock + CONVENTIONS §B/§F)

| Quantity | Convention | Notes |
| --- | --- | --- |
| Energy scale | Single unified **phonon E_dep** scale, **NO quenching**, no keVee/keVnr | Both channels electron-recoil deposits (§B); combined table is deposited energy |
| Deliverable | **Deposited** dR/dE_dep only; **NO E_rec fold** | The QPD response R(E_rec\|E_dep) and reconstructed spectra are Phase 5 (guards fp-reconstructed-not-deposited) |
| Shared grid | log E_dep, 0.01 keV → 2×10⁵ keV, ~80 bins/decade, **584 bin centers** = geometric means of the shared edges | Identical to 04-01/04-02; `muon_deposit.shared_energy_grid()` is the single source |
| Normalization | counts·kg⁻¹·day⁻¹·keV⁻¹; rates in Hz (total 110 g wafer) | Wafer mass 0.1099 kg from `wafer_geometry.MASS_KG` |
| Bandwidth censoring | 50 kHz sampling / 20 µs slot; 25 kHz Nyquist / 40 µs resolving (§F) | Both occupancy definitions reported |
| Metric / gauge / Fourier | not_applicable | No relativistic field theory in this pipeline |

---

## Key results (with confidence)

- **Shared-grid identity (guards fp-grid-mismatch).** The muon and Compton E_dep grids are **exactly equal** (`np.array_equal` True; max relative deviation **0.0**), and both match the canonical `shared_energy_grid()` geometric-mean centers to **5×10⁻⁷** (6-sig-fig CSV rounding). Span 0.01 keV → 197.1 MeV, 584 bins. **[CONFIDENCE: HIGH]** — exact equality plus an independent reconstruction of the centers from the canonical edges.
- **Energy closure, muon.** ∫dR/dE_dep dE = **1.0729×10⁶** counts/kg/day vs the independently-computed rate·86400/mass_kg = **1.0737×10⁶** → **ratio 0.99928** (±3.6×10⁻³ MC). The 0.07% shortfall is within the MC band and consistent with the rare sub-grid-floor grazing-corner deposits noted in 04-01. **[CONFIDENCE: HIGH]** — the differential histogram reproduces the scalar MC/analytic rate (independent object).
- **Energy closure, Compton.** ∫dR/dE_dep dE = **2.1105×10⁵** vs expected **2.1105×10⁵** → **ratio 0.99997**. **[CONFIDENCE: HIGH]** — matches the 04-02 closure to ~10⁻⁵ (sub-0.01 keV forward-scatter deposits drop below the grid floor, one-directional).
- **Deposited-power first moment (physical diagnostic).** ⟨E_dep⟩ = ∫E·dR/dE_dep dE / ∫dR/dE_dep dE = **2.33 MeV (muon)**, **589 keV (Compton)**. The muon mean sits **above** the 1.459 MeV vertical-chord mean (04-01) because inclined chords are longer — a correct angular-average sanity check; the Compton mean sits below its 2382 keV max edge. **[CONFIDENCE: MEDIUM]** — physically consistent, but derived from the same histogram (a self-consistency, not an independent power measurement; stated as such).
- **Pileup stop-condition (guards fp-pileup-unchecked).** R_tot = **1.634 Hz**; occupancy R·τ = **3.27×10⁻⁵** (20 µs) / **6.54×10⁻⁵** (40 µs); R/50 kHz = **3.27×10⁻⁵**; non-paralyzable dead-time fraction **6.5×10⁻⁵**, paralyzable live fraction **0.999935**; mean inter-event interval **0.612 s** ≈ 1.5×10⁴ resolving times. **Stop-condition NOT triggered** (occupancy ≪ 1% threshold). **[CONFIDENCE: HIGH]** — arithmetic on the two independently-anchored channel rates; the flag correctly flips ON in the unit test at a hypothetical 15 kHz rate.
- **Combined table + figure.** `data/combined_dRdEdep.csv` (muon, Compton, total, total_mc_err on the shared grid) and `figs/phase4_deposited_spectra.png` (log-log; Compton dominates ≲2.4 MeV with the ⁴⁰K/²¹⁴Bi/²⁰⁸Tl edges marked, muon dominates above and carries the ~197 MeV tail; total = exact co-add). Deposited-energy axis only. **[CONFIDENCE: HIGH]**.

---

## Acceptance-test outcomes (self-assessed)

| Test | Procedure | Result | Verdict |
| --- | --- | --- | --- |
| **test-shared-grid** | Compare muon vs Compton E_dep grids | Byte-identical (max rel dev 0.0); both match canonical centers to 5×10⁻⁷; span 0.01 keV–197 MeV, 584 bins | **PASS** |
| **test-energy-closure** | ∫dR/dE_dep dE vs rate·86400/mass_kg per channel | muon 0.99928 (±3.6e-3), Compton 0.99997; total-spectrum closure 0.9994; per-kg mass 0.1099 kg confirmed | **PASS** |
| **test-pileup** | R_tot·τ vs 50 kHz occupancy; note within-event saturation | occ 3.3e-5 / 6.5e-5 ≪ 1; R/50kHz 3.3e-5; stop-condition NOT triggered; muon ~197 MeV saturation flagged for Phase 5 | **PASS** |

Forbidden proxies rejected: **fp-grid-mismatch** (explicit exact shared-grid assertion before any co-addition; a perturbed grid raises in the unit test), **fp-reconstructed-not-deposited** (no E_rec mapping; the raw ~197 MeV muon deposited tail survives intact, asserted >100 MeV), **fp-pileup-unchecked** (occupancy computed against the 50 kHz bandwidth with both 20/40 µs definitions and paralyzable/non-paralyzable dead-time, never asserted).

---

## Method notes / decisions (balanced-autonomy, in-scope)

- **Rates parsed from the CSV headers, not hard-coded.** `_parse_rate_Hz` reads `integral_muon_rate_Hz = 1.3657` and `total_single_scatter_rate_Hz = 2.6846e-01` from the channel headers, so the closure check consumes exactly the value each upstream plan produced (robust to a future channel re-run).
- **Closure quadrature uses the linear bin widths of the shared log edges.** The CSV stores geometric-mean centers; the original histograms normalized by dE = edge_{i+1}−edge_i, so ∫dR/dE dE = Σ dRdEdep_i·dE_i reproduces the counts. Edges/centers/widths all come from the single canonical `shared_energy_grid()`.
- **Two closure statements, clearly separated.** The **count-rate closure** (∫dR/dE_dep dE = rate) is the INDEPENDENT conservation cross-check (ties the differential histogram to the independently-computed scalar rate). The **first-moment power integral** (∫E·dR/dE_dep dE, hence ⟨E_dep⟩) is reported as a physical diagnostic derived from the same histogram — explicitly NOT an independent power measurement, to avoid over-claiming.
- **Pileup reported with both censoring conventions and both dead-time models.** 20 µs (50 kHz sample slot) and 40 µs (25 kHz Nyquist resolving); non-paralyzable R·τ/(1+R·τ) and paralyzable exp(−R·τ). At R·τ ~ 6.5×10⁻⁵ they agree to first order, as the unit test checks. The paralyzable-vs-non-paralyzable choice remains the OPEN Phase-5 switch (CONVENTIONS §F) — not decided here.
- **Combined figure masks non-positive bins** (log axis) and marks the three Klein–Nishina electron-recoil edges plus the muon high-E tail; the annotation states closure ratios, R_tot, occupancy, and "no E_rec fold (Phase 5)".

## Deviations / issues

- **No deviations.** Task 1 executed as planned; all three acceptance tests pass on the first assembly. The muon closure 0.07% shortfall is a documented, expected sub-grid-floor effect from 04-01 (rare grazing-corner ~zero deposits), one-directional (integral ≤ rate), within the MC band — not an error.
- **Pre-existing unrelated working-tree changes** to `data/flux/reactor_flux_v1.0.csv` and `reactor_flux_billard_variant.csv` were present before this plan and were **NOT** staged or touched (out of scope for 04-03).
- **Within-event muon saturation is a rate-level flag only.** The ~197 MeV long-chord deposits will saturate the QPD within a single pulse; the quantitative impact is a Phase-5 response result, not modeled here.

## Reproducibility

- Deterministic post-processing (no new MC): regenerate with `PYTHONPATH=src python -m qpd_potential.deposited_spectra`. Inputs `data/muon_dRdEdep.csv` (seed 20260720) and `data/compton_dRdEdep.csv` (seed 20260720). NumPy 1.26.4, matplotlib 3.8.0, Python 3.11. Grid via `muon_deposit.shared_energy_grid()` (single source, guaranteed identical to 04-01/04-02).

## Deliverables

- `src/qpd_potential/deposited_spectra.py` — load, shared-grid assertion, co-add, closure, pileup, combined table + figure
- `tests/test_deposited_spectra_closure.py` (13 tests: 3 grid, 5 closure, 4 pileup, 1 deposited-not-reconstructed)
- `data/combined_dRdEdep.csv` — muon + Compton + total dR/dE_dep on the shared grid
- `figs/phase4_deposited_spectra.png` — combined log-log deposited-energy spectra

## Self-Check: PASSED

All deliverable files exist; atomic commit `0e2ec36` recorded; 13 new + 131/131 total tests pass; combined table + figure regenerated deterministically; every contract claim, acceptance test, and forbidden proxy has an explicit outcome above.

```yaml
gpd_return:
  status: completed
  phase: "04"
  plan: "03"
  tasks_completed: 2
  tasks_total: 2
  duration_seconds: 240
  files_written:
    - src/qpd_potential/deposited_spectra.py
    - tests/test_deposited_spectra_closure.py
    - data/combined_dRdEdep.csv
    - figs/phase4_deposited_spectra.png
    - GPD/phases/04-muon-compton-deposited-energy-spectra/04-03-SUMMARY.md
  issues:
    - "Task 2 is checkpoint:human-verify; per the autonomous directive it is recorded satisfied-pending-orchestrator-review, not blocked. Orchestrator to confirm: (a) both channels share the grid (max rel dev 0.0) and pass energy closure (muon 0.9993, Compton 0.99997), (b) the deliverable is deposited energy with no E_rec fold, (c) pileup occupancy 3.3e-5 << 1 (stop-condition NOT triggered), (d) within-event muon ~197 MeV saturation flagged for Phase 5."
    - "Deposited-power first moment (mean deposit muon 2.33 MeV, Compton 589 keV) is a physical diagnostic derived from the same histogram, NOT an independent power measurement; the INDEPENDENT conservation check is the count-rate closure int dR/dE_dep dE = rate*86400/mass_kg. Stated explicitly to avoid over-claiming."
    - "Absolute Compton rate (hence the exact pileup margin) inherits the site-dependent sourced-flux uncertainty band from 04-02; even a 10x flux increase keeps occupancy ~3e-4 << 1, so the stop-condition conclusion is robust."
    - "Pre-existing unrelated working-tree edits to data/flux/reactor_flux_v1.0.csv and reactor_flux_billard_variant.csv were NOT staged or touched (out of scope for 04-03)."
    - "Within-event muon saturation (long-chord tens-of-MeV to ~197 MeV deposits) is a rate-level Phase-5 flag; its quantitative reconstruction impact is a Phase-5 result, not modeled here."
  next_actions:
    - "Orchestrator: review figs/phase4_deposited_spectra.png and data/combined_dRdEdep.csv, then sign off the Phase-4 deposited-energy handoff (Task-2 checkpoint) before Phase 5."
    - "Phase 5: fold the combined dR/dE_dep (or per-channel) through R(E_rec|E_dep); the muon ~197 MeV long-chord tail is the saturated-regime input, and the paralyzable-vs-non-paralyzable + merge-vs-drop bandwidth-censoring switch (CONVENTIONS F, OPEN) must be resolved there."
    - "Phase 5: the two channels are co-addable and grid-consistent; no re-binning is needed."
  decisions:
    - summary: "Muon and Compton deposited-energy spectra assembled on the byte-identical shared log E_dep grid (584 bins, 0.01 keV -> 197 MeV; np.array_equal True, max rel dev 0.0; centers = geometric means of shared_energy_grid() edges to 5e-7). Combined table data/combined_dRdEdep.csv (muon+Compton+total) and figs/phase4_deposited_spectra.png emitted; deposited (phonon) energy only, NO E_rec fold. Guards fp-grid-mismatch, fp-reconstructed-not-deposited."
      phase: "04-muon-compton-deposited-energy-spectra"
    - summary: "Energy closure per channel: int dR/dE_dep dE = rate_Hz*86400/mass_kg (mass 0.1099 kg). Muon 1.0729e6 vs 1.0737e6 -> ratio 0.99928 (+/-3.6e-3 MC, 0.07% sub-grid-floor shortfall); Compton 2.1105e5 vs 2.1105e5 -> 0.99997; total-spectrum closure 0.9994. Rates parsed from CSV headers (1.3657 / 0.26846 Hz), not hard-coded. First-moment deposited power reported as a physical diagnostic (mean deposit muon 2.33 MeV > 1.46 MeV vertical, Compton 589 keV), explicitly not an independent number."
      phase: "04-muon-compton-deposited-energy-spectra"
    - summary: "Pileup stop-condition: R_tot=1.634 Hz (muon 1.366 + Compton 0.268), occupancy R*tau=3.27e-5 (20us/50kHz sample) / 6.54e-5 (40us/25kHz resolving), R/50kHz=3.27e-5; non-paralyzable dead-time 6.5e-5, paralyzable live fraction 0.999935; mean interval 0.612 s ~ 1.5e4 resolving times. Occupancy << 1 -> stop-condition NOT triggered, quiescent reconstruction not precluded. Within-event muon ~197 MeV saturation flagged for Phase 5. Guards fp-pileup-unchecked."
      phase: "04-muon-compton-deposited-energy-spectra"
  contract_updates:
    claims_passed: [claim-phase4-assembly, claim-pileup-stopcondition]
    acceptance_tests_passed: [test-shared-grid, test-energy-closure, test-pileup]
    forbidden_proxies_rejected: [fp-grid-mismatch, fp-reconstructed-not-deposited, fp-pileup-unchecked]
  state_updates:
    advance_plan: false
    update_progress: false
    record_metric:
      phase: "04"
      plan: "04-03"
      duration: 240
      tasks: 2
      files: 5
```
