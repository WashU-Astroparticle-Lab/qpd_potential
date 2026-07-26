---
created: 2026-07-25T00:00:00.000000+00:00
title: Propagate the unit calibration slope through the milestone record and the paper
area: numerical
files:
  - artifacts/v2.0/em_dRdErec_ext_TaAl.csv
  - artifacts/v2.0/em_dRdErec_ext_AlHf.csv
  - artifacts/v2.0/sb_particle.csv
  - src/qpd_potential/sb_assembly.py
  - GPD/ROADMAP.md
  - GPD/STATE.md
  - paper/sections/response.tex
  - paper/sections/results.tex
---

## Problem

`params.CALIB_SLOPE` was introduced on 2026-07-25 (USER DECISION, CONVENTIONS §E.1) and set to
**1.0**, superseding the Phase-1 calibration slope `= EPSILON = 0.5`. `E_rec` is an **estimator of
the deposited energy**, not the collected signal: a real detector is calibrated on a known line and
that calibration absorbs the physical deposit→quasiparticle conversion fraction ε into the
count→energy constant `C`. Under the old convention a known 10 eV line reconstructed at 4.76 eV.

ε = 0.5 keeps its physical role (`energy_scale.n_qp_yield`, `saturation_onset_energy`, the trigger).
Only the energy **axis** was decoupled from it. Saturation above the onset is genuine information
loss and is **not** unfolded (`fp-unfold-saturation`).

### Done in that pass

- `params.CALIB_SLOPE`, `response.calibrate_C`, `energy_scale.E_rec_estimator`, and the
  `response_matrix` provenance strings.
- CONVENTIONS §B / §E.1 / §E.2 and the two contradiction tables; `state.json` `convention_lock`
  (`custom:energy_scale_calibration`, plus `energy_scale_chain` and `efficiency_mapping` amended).
- Rebuilt `artifacts/v2.0/response_matrix_{TaAl,AlHf}_ext.npz` (C exactly ×2; same seed, same
  forward counts; columns still sum to 1; no off-grid overflow), and regenerated
  `cevns_dRdErec_ext_*.csv`, `neutron_dRdErec_ext_*.csv`, `ge71_ec_dRdErec_*.csv` from their
  committed writers.
- `notebooks/paper_calculations.ipynb` combined-spectrum cell + a ⚠️ markdown cell warning that the
  notebook now carries TWO scales.
- Slope assertions in `tests/test_response_chain.py`, `test_response_matrix.py`, `test_energy_scale.py`.

### Done in the follow-up pass (branch claude/erec-recalibration-milestone-record)

- **Emitters written & committed** (they never existed): `fold.write_em_ext_spectrum`,
  `fold.write_em_dominance_table`. `em_dRdErec_ext_*` and `em_inband_dominance.csv` regenerated
  on the unit-slope axis. **sb_assembly is no longer mixing scales** — every channel CSV is now
  new-axis.
- **M line leaves the RoI (result change).** 158.7 eV_dep images at ~126–130 eV, above the RoI;
  in-RoI fraction 0. SC3's "M line inside the RoI" is REFUTED on the corrected axis. `14-02`
  §2/§2.1/§3 + SC3 row updated; `PHASE13_ELASTIC_INROI` → 4780.35 / 4832.43.
- **Endpoint anchor** test updated 34.8/26.8 → 69.53/53.69 keV. ge71 + em + regime-boundary +
  dominance-ratio tests updated around the corrected physics. Frozen-artifact exempt list updated.

### NOT done — needs a decision (below), then the headline work

- **S/B_particle headline.** Two coupled changes: (a) the signal numerator itself moved with the
  axis — CEvNS in-RoI 72.92 → 62.63; (b) `sb_assembly` still adds the ⁷¹Ge M-line's TOTAL bound
  (130.82) to the RoI denominator, but the line no longer lands in the RoI — **decision needed**:
  an out-of-RoI bound should contribute 0 to the RoI background. Once resolved: regenerate
  `sb_particle.csv` / `sb_leave_one_out.csv` / `channel_inventory.csv`, update the Phase-16 report
  numbers, ROADMAP/STATE headline S/B, and `test_sb_assembly` (5 tests).
- **v1.0-baseline comparisons** (`test_overlap_vs_archived` ×2, `test_cevns_subev_regression` ×2) —
  decision needed (re-anchor in deposit space vs rebuild stage1/).
- **The paper** — still on the old axis (`response.tex`, `results.tex`).

### Original enumeration (for reference)

**18 tests fail (891 pass), every one a real downstream consequence, none a code defect.**

1. **`artifacts/v2.0/em_dRdErec_ext_{TaAl,AlHf}.csv` are still on the OLD axis.**
   Blocking detail: **these two files have no committed writer.** `fold.run_em_fold_extended`
   computes everything, but the Phase-15-03 CSV emitter was never checked in, and the files carry
   several hundred lines of curated provenance prose that must not be lost. Write the emitter first,
   then regenerate. Affected: `test_em_fold::test_saturation_peak`, `test_sb_assembly::test_full_capture_band`,
   `test_em_rescope_audit::test_dominance_recomputed`, all four `test_sb_assembly` failures.

2. **Milestone headline numbers move.** The RoI is 10–100 eV; on the old axis, applying it to
   `E_rec` silently selected a **20–200 eV deposit** band. Measured on the new axis, the Phase-13
   in-RoI neutron rate goes **5430.287 → 4780.352** counts/kg/day. `S/B_particle` = 1.33e-2 and
   every "10–100 eV reconstructed RoI" rate in ROADMAP/STATE is an old-axis quantity.

3. **The 197 MeV endpoint plateau doubles**: paper-quoted 34.8 / 26.8 keV → **69.53 / 53.69 keV**
   (`test_response_matrix_extended::test_197MeV_endpoint_anchor`). These are *paper* numbers.

4. **The sub-eV regime boundary moves**: 1 eV deposited images at **0.4959 → 0.9945 eV_rec**
   (`test_cevns_subev_fold::test_regime_boundary_labelled`, `test_em_fold::test_regime_boundary_imported`).
   The old value is written into committed CSV headers.

5. **v1.0-baseline comparisons now disagree by ~2× BY CONSTRUCTION.**
   `artifacts/stage1/` was deliberately NOT rebuilt (`fp-overwrite-v1-matrices`), so
   `test_response_matrix_extended::test_overlap_vs_archived_is_consistent_with_monte_carlo_noise`
   and both `test_cevns_subev_regression` tests compare a new-scale product against an old-scale
   baseline. **Decide what these should assert** — rebuild v1.0 too, or re-anchor the comparison in
   deposit space where the scale cancels. Do not just widen the tolerance.

6. **`test_ge71_ec::test_line_placement_measured` encoded ε as if it were saturation.** It asserted
   the 158.7 eV M line images below `0.6 × 158.7 = 95.2 eV`; that only held because ε put it at
   79 eV. The physically correct new value is 130.1 eV (saturation alone). Rewrite the assertion
   around the saturation claim it meant to make.

7. **`test_ge71_ec::test_trigger_composition_ec` now divides by zero** because the ⁷¹Ge M line left
   the 10–100 eV RoI entirely (79 → 130 eV_rec). That is a real physics change, not a test bug.

8. **The paper is untouched** and still documents the 0.5 slope as a feature
   (`paper/sections/response.tex`), plus every E_rec number in `results.tex`.

## Why it matters

Until 1–2 are done, `sb_assembly` silently mixes new-axis (cevns, neutron) with old-axis (muon,
compton) curves and produces a meaningless ratio. That is the highest-priority item here.
