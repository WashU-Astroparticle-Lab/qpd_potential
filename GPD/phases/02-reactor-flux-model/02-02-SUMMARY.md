---
phase: 02-reactor-flux-model
plan: "02"
title: "Absolute reactor antineutrino flux Phi(E_nu) at 3 GW_th / 25 m: frozen versioned CSV with split above/below-2-MeV band and a Billard-2017 closure variant"
date: 2026-07-20
status: completed
depth: full
completed: 2026-07-20
one_liner: "Normalized the Plan 02-01 per-fission spectrum to an absolute detector flux via R_f = P_th/<E_f> (3 GW_th, effective-thermal <E_f>=205.8 MeV Ma-2013, NOT total Q) and 1/(4 pi d^2) at d=2500 cm, applied exactly once: R_f=9.10e19 fissions/s, int Phi dE=7.50e12 nu-bar/cm2/s (authoritative 7-8e12 band), emission=1.96e20 nu-bar/s/GW_th (Hayes-Vogel ~2e20). Froze data/flux/reactor_flux_v1.0.csv (7-col schema, additive components, per-bin SPLIT band 2-5% >2 MeV -> 20-25% <1.8 MeV, region flags, version/git-sha/provenance header), an overlay vs published Huber 235U (agree to <4.4% >2 MeV within band), and a distinct Billard-variant table (HM constant <2 MeV, fractions 55.6/32.6/7.1/4.7). Sub-1.8 MeV shape CITED to Kopeikin 2012 (consistent model) but kept a flagged placeholder: no machine-readable Kopeikin-2012 table was sourceable in-environment, honestly covered by the wide low-E band. 22/22 new tests pass, full suite 57/57."
provides:
  - "src/flux/normalization.py -- R_f=P_th/<E_f>, Phi=[sum_i f_i S_i + S_capture]*R_f*1/(4 pi d^2) with dimensioned asserts; effective-thermal <E_f> (Ma 2013), single R_f+geometry multiplication; forbidden-proxy guards"
  - "src/flux/build_flux_table.py -- frozen CSV writer (split band, region flags, provenance header), Billard-2017 closure variant (HM constant below 2 MeV), overlay figure"
  - "data/flux/reactor_flux_v1.0.csv -- FROZEN versioned flux table (deliv-frozen-csv)"
  - "data/flux/reactor_flux_billard_variant.csv -- Billard closure variant for the Phase-3 Table-1 reproduction"
  - "GPD/phases/02-reactor-flux-model/figures/flux_overlay.png -- Phi(E_nu) + split band vs published Huber 235U (deliv-overlay-fig)"
  - "tests/test_flux_normalization.py (10) + tests/test_flux_table.py (12) -- 22 acceptance/guard tests"
plan_contract_ref: GPD/phases/02-reactor-flux-model/02-02-PLAN.md#/contract

conventions:
  units: "Phi(E_nu) in nu-bar cm^-2 s^-1 MeV^-1; R_f in fissions s^-1 (Phase-1 CONVENTIONS Sec A, D, G)"
  normalization: "P_th = 3 GW_th (THERMAL); d = 25 m point source 1/(4 pi d^2); <E_f> = sum_i f_i E_i effective thermal (Ma 2013 202.4/205.9/211.1/213.6 MeV), NOT total Q; per-fission spectrum multiplied by R_f and geometry ONCE"
  target_flux: "Authoritative integral-flux target 7-8e12 nu-bar cm^-2 s^-1 (Phase-1 lock); REQUIREMENTS.md CALC-01 '~1x10^13' is loose order-of-magnitude rounding, NOT a tighter target"
  fission_fractions: "Flagship 235U:238U:239Pu:241Pu = 0.58:0.07:0.30:0.05; Billard switch 235/239/238/241 = 55.6/32.6/7.1/4.7 (isotope-labelled)"

contract_results:
  claims:
    claim-frozen-flux:
      status: passed
      summary: "The frozen Phi(E_nu) table (data/flux/reactor_flux_v1.0.csv) normalizes to int Phi dE = 7.50e12 nu-bar cm^-2 s^-1 at 3 GW_th and 25 m (inside the authoritative 7-8e12 band), via R_f = P_th/<E_f> = 9.10e19 fissions/s with <E_f> = 205.8 MeV effective thermal (Ma 2013, not total Q) and a single 1/(4 pi d^2) geometry factor at d=2500 cm. It carries a per-bin uncertainty band SPLIT at ~1.8-2 MeV (2-5% data-anchored above 2 MeV; 10% at the seam; 20-25% model-only below 1.8 MeV) with region_flag in {above_2MeV, seam, below_1p8MeV}; the above-2-MeV computed 235U flux agrees with the published Huber 235U tabulation to <4.4% (within band) over 2-7 MeV; and the Billard-variant switch (HM held constant below 2 MeV, fission fractions 55.6/32.6/7.1/4.7 isotope-labelled) emits a distinct table (4.59e12) ready for the Phase-3 Billard Table-1 reproduction. Absolute normalization independently cross-checked against Hayes-Vogel: emission = 1.96e20 nu-bar s^-1 GW_th^-1 (~2e20). CAVEAT (does not fail the claim): the sub-1.8 MeV fission SHAPE remains a seam-anchored MODEL PLACEHOLDER cited to Kopeikin 2012 as the consistent reference model; a machine-readable Kopeikin-2012 per-isotope table was not sourceable in-environment, honestly covered by the wide (20-25%) below-1.8 band."
      linked_ids: [deliv-frozen-csv, deliv-normalization-code, deliv-overlay-fig, test-normalization, test-csv-schema, test-band-split, test-billard-variant, ref-huber, ref-cevns-benchmark, ref-ma, ref-hayes-vogel]
      evidence:
        - verifier: gpd-executor
          method: "dimensioned normalization chain + integral flux (pytest test-normalization)"
          confidence: high
          claim_id: claim-frozen-flux
          deliverable_id: deliv-normalization-code
          acceptance_test_id: test-normalization
          reference_id: ref-ma
        - verifier: gpd-executor
          method: "Hayes-Vogel emission-rate cross-check ~2e20 nu-bar/s/GW_th"
          confidence: high
          claim_id: claim-frozen-flux
          deliverable_id: deliv-normalization-code
          acceptance_test_id: test-normalization
          reference_id: ref-hayes-vogel
        - verifier: gpd-executor
          method: "overlay of computed 235U flux vs published Huber 235U tabulation, <4.4% >2 MeV within band"
          confidence: high
          claim_id: claim-frozen-flux
          deliverable_id: deliv-overlay-fig
          acceptance_test_id: test-band-split
          reference_id: ref-huber
        - verifier: gpd-executor
          method: "Billard-variant closure (constant below 2 MeV + Billard fractions) distinct table (pytest test-billard-variant)"
          confidence: high
          claim_id: claim-frozen-flux
          deliverable_id: deliv-normalization-code
          acceptance_test_id: test-billard-variant
          reference_id: ref-cevns-benchmark
  deliverables:
    deliv-frozen-csv:
      status: passed
      path: data/flux/reactor_flux_v1.0.csv
      summary: "Frozen versioned table, 7 columns (E_nu_MeV, flux_nu_per_cm2_per_s_per_MeV, flux_fission_HM, flux_fission_summation, flux_ncapture_238U, rel_uncertainty, region_flag), 101 rows on the Plan 02-01 grid. Components additive to the total (max residual 3e-7). Header documents version v1.0, generation date, git sha, normalization (3 GW_th, 25 m, <E_f>=205.8 MeV, fission fractions), per-source provenance (Huber/Mueller/summation-Kopeikin2012/n-capture), and the integral checks (grand total 6.48/fission, above-1.8 1.88/fission, int Phi 7.50e12, emission 1.96e20/GW_th). Split band widens across the seam: 2-5% (>2 MeV) -> 10% (seam) -> 20% (1-1.8) -> 25% (<1 MeV)."
      linked_ids: [claim-frozen-flux, test-csv-schema, test-band-split]
    deliv-normalization-code:
      status: passed
      path: src/flux/normalization.py
      summary: "R_f = P_th/<E_f> with <E_f> effective thermal (Ma 2013) via effective_energy_per_fission (asserts 195-220 MeV, rejecting total-Q); fission_rate with power-relative dimensioned assert; geometry_factor 1/(4 pi d^2) at d=2500 cm; absolute_flux multiplies the already-per-fission spectrum by R_f and geometry exactly once; emission_rate_per_gwth for the Hayes-Vogel anchor. All forbidden-proxy traps guarded in tests/test_flux_normalization.py (10 tests)."
      linked_ids: [claim-frozen-flux, test-normalization]
    deliv-overlay-fig:
      status: passed
      path: GPD/phases/02-reactor-flux-model/figures/flux_overlay.png
      summary: "Phi(E_nu) total (log-y) with the shaded split band, the computed 235U flux contribution (dashed), and the published Huber 235U tabulation (points) overlaid; the seam band 1.8-2.0 MeV marked. Points sit on the computed 235U curve above 2 MeV; the band visibly widens below 1.8 MeV."
      linked_ids: [claim-frozen-flux, test-band-split, ref-huber]
  acceptance_tests:
    test-normalization:
      status: passed
      summary: "R_f = 9.098e19 fissions/s (~9e19); int Phi dE = 7.503e12 nu-bar cm^-2 s^-1 (inside 7-8e12, well within +-15%); Hayes-Vogel emission 1.964e20 nu-bar s^-1 GW_th^-1 (~2e20). Uses 3 GW_th and effective-thermal <E_f>, not GW_e or total Q. Dimensioned asserts pass; GW_e (3x low), total-Q, and x6 double-count traps explicitly rejected in tests."
      linked_ids: [claim-frozen-flux, deliv-normalization-code, ref-ma, ref-hayes-vogel]
    test-csv-schema:
      status: passed
      summary: "All seven columns present in order; 101 rows; region_flag in {above_2MeV, seam, below_1p8MeV}; rel_uncertainty populated (0<u<1) every row; header documents version/git-sha/normalization/per-source provenance/integral checks. Components additive to total (3e-7)."
      linked_ids: [deliv-frozen-csv]
    test-band-split:
      status: passed
      summary: "rel_uncertainty is 2-5% for above_2MeV bins and 20-25% for below_1p8MeV bins (strictly wider below the seam; max/min spread >=3x -> demonstrably non-uniform, fp-uniform-band rejected). Above 2 MeV the computed 235U flux agrees with published Huber 235U to <4.4% over 2-7 MeV, within the band."
      linked_ids: [claim-frozen-flux, deliv-frozen-csv, deliv-overlay-fig, ref-huber]
    test-billard-variant:
      status: passed
      summary: "The Billard variant holds each isotope's HM spectrum CONSTANT below 2 MeV (verified flat) and uses Billard fractions 235U/239Pu/238U/241Pu = 55.6/32.6/7.1/4.7 % correctly isotope-labelled (239Pu 0.326 > 238U 0.071, NO 238U<->239Pu swap). Its integral flux 4.59e12 is materially distinct from the flagship 7.50e12 (>20% apart), ready for the Phase-3 Billard Table-1 reproduction."
      linked_ids: [claim-frozen-flux, deliv-normalization-code, ref-cevns-benchmark]
  references:
    ref-huber:
      status: completed
      completed_actions: [compare, cite]
      missing_actions: []
      summary: "Overlaid the computed 235U flux contribution against the published Huber 235U tabulation (arXiv:1106.0687, from data/flux/huber_U235_benchmark.csv) in flux_overlay.png; agreement <4.4% over 2-7 MeV within band. Cited in the CSV provenance header and the figure."
    ref-cevns-benchmark:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "Reproduced Billard (2017, arXiv:1612.09035) flux ASSUMPTIONS as a closure variant: Huber-Mueller held constant below 2 MeV, fission fractions 55.6/32.6/7.1/4.7 (235/239/238/241). Emitted data/flux/reactor_flux_billard_variant.csv, distinct from the flagship; cited in its header."
    ref-ma:
      status: completed
      completed_actions: [use, cite]
      missing_actions: []
      summary: "Used the Ma et al. (PRC 88,014605 (2013)) effective thermal energies per fission (202.4/205.9/211.1/213.6 MeV for 235/238/239/241) as <E_f> in R_f = P_th/<E_f>; encoded in normalization.E_EFF_MEV and cited in the CSV header. Guards the total-Q trap."
    ref-hayes-vogel:
      status: completed
      completed_actions: [compare, cite]
      missing_actions: []
      summary: "Cross-checked the absolute normalization against the Hayes & Vogel (ARNPS 66,219 (2016)) ~2e20 nu-bar s^-1 GW_th^-1 emission-rate anchor: obtained 1.96e20. Cited in the CSV header and the normalization docstring."
  forbidden_proxies:
    fp-loose-1e13:
      status: rejected
      notes: "The normalization was NOT tuned to the loose ~1e13 from REQUIREMENTS.md CALC-01. The honest chain lands at 7.50e12 (~25% below 1e13); test_guard_fp_loose_1e13_not_a_tighter_target asserts the flux stays <9e12 and >20% away from 1e13. The 7-8e12 Phase-1 lock is the authoritative target; the CALC-01 wording is surfaced for the orchestrator as an order-of-magnitude rounding, not a tighter target."
    fp-norm-chain-traps:
      status: rejected
      notes: "GW_e vs GW_th: P_th defaults to 3e9 W thermal; test shows the GW_e trap collapses the flux exactly 3x (to <3e12), out of band. Total-Q vs effective thermal: <E_f> uses Ma-2013 effective thermal (~205.8 MeV) with an assert rejecting values outside 195-220 MeV (total Q incl. neutrinos would be ~215+). Double-count: the already-per-fission spectrum is multiplied by R_f and geometry exactly once; test shows a x6 re-multiply inflates the flux 6x out of band."
    fp-uniform-band:
      status: rejected
      notes: "The band is genuinely split, not uniform: 2-5% above 2 MeV vs 20-25% below 1.8 MeV, widening across the seam, with max/min spread >=3x (test_fp_uniform_band_rejected). The never-measured sub-1.8 MeV region is honestly flagged model-only via region_flag and the wide band; the low-recoil bins are NOT misrepresented as data-anchored."
  uncertainty_markers:
    weakest_anchors:
      - "The sub-1.8 MeV fission SHAPE is a seam-anchored MODEL PLACEHOLDER cited to Kopeikin 2012 (Phys. At. Nucl. 75, 143) as the consistent reference model, NOT a digitized Kopeikin table -- a machine-readable per-isotope Kopeikin-2012 table was not sourceable in-environment (Springer-only; no arXiv table). Covered by the wide 20-25% below-1.8 band; drives the low-recoil CEvNS bins, not the integral normalization."
      - "The absolute integral rests on ~6 nu-bar/fission and ~205 MeV/fission (good to a few %) plus the point-source 1/(4 pi d^2) approximation; these are the well-anchored pieces, and the real residual risk is the sub-IBD SHAPE, not the integral."
    unvalidated_assumptions:
      - "Point-source 1/(4 pi d^2) at 25 m is adequate at the contract's ~2x rate tolerance; finite-core / near-field geometry is neglected (noted as an out-of-scope systematic)."
      - "The Billard variant excludes n-capture and holds HM flat below 2 MeV, matching Billard's stated flux assumption; whether Billard's own low-E treatment matches to <10% is a Phase-3 comparison, not verified here."
    disconfirming_observations:
      - "Integral flux off from ~7-8e12 by >2x, a constant (non-widening) band across the seam, components not summing to the total, or the Billard fractions mislabelled (238U<->239Pu swap) -- none observed (7.50e12; band 2-5%->25%; additivity 3e-7; 239Pu 0.326 > 238U 0.071)."

comparison_verdicts:
  - subject_id: test-normalization
    subject_kind: acceptance_test
    subject_role: decisive
    reference_id: ref-hayes-vogel
    comparison_kind: benchmark
    metric: emission_rate_per_GWth
    threshold: "1.7e20 - 2.3e20 nu-bar s^-1 GW_th^-1"
    verdict: pass
    notes: "Emission 1.964e20 nu-bar s^-1 GW_th^-1 vs Hayes-Vogel ~2e20; integral flux 7.50e12 in the 7-8e12 band."
  - subject_id: claim-frozen-flux
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-huber
    comparison_kind: benchmark
    metric: relative_error
    threshold: "<= band (~2-5% above 2 MeV)"
    verdict: pass
    notes: "Computed 235U flux vs published Huber 235U tabulation: <4.4% over 2-7 MeV, within the data-anchored band."
  - subject_id: claim-frozen-flux
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-cevns-benchmark
    comparison_kind: prior_work
    metric: variant_distinctness
    threshold: "constant below 2 MeV + Billard fractions labelled; distinct from flagship"
    verdict: pass
    notes: "Billard variant flat below 2 MeV, fractions 55.6/32.6/7.1/4.7 correctly isotope-labelled, integral 4.59e12 distinct from flagship 7.50e12."
---

# Plan 02-02 Summary: Absolute reactor antineutrino flux Phi(E_nu), frozen at v1.0

## What was built

The Plan 02-01 component-wise per-fission spectrum was normalized to an **absolute
detector flux** and frozen as a versioned, provenance-tagged CSV:

```
R_f     = P_th / <E_f>                                  = 9.10e19 fissions/s
<E_f>   = sum_i f_i E_i (Ma 2013, effective thermal)    = 205.8 MeV   (NOT total Q)
Phi(E)  = [ sum_i f_i S_i + S_capture ] * R_f / (4 pi d^2),  d = 2500 cm
int Phi dE = 7.50e12 nu-bar cm^-2 s^-1                  (authoritative target 7-8e12)
emission   = 1.96e20 nu-bar s^-1 GW_th^-1              (Hayes-Vogel ~2e20)
```

The per-fission spectrum already integrates to ~6/fission, so **R_f and the geometry
factor are applied exactly once** (the x6 double-count is guarded and tested).

## Key numbers (self-assessment against the acceptance tests)

| Acceptance test | Verdict | Evidence |
|---|---|---|
| **test-normalization** | **PASS** | R_f = 9.10e19 fissions/s (~9e19); int Phi dE = 7.50e12 (7-8e12); Hayes-Vogel 1.96e20/s/GW_th (~2e20); dimensioned asserts pass |
| **test-csv-schema** | **PASS** | 7 columns in order, 101 rows, region_flag in {above_2MeV, seam, below_1p8MeV}, rel_uncertainty every row, full version/git-sha/normalization/provenance/integral-check header, components additive (3e-7) |
| **test-band-split** | **PASS** | band 2-5% (>2 MeV) -> 10% (seam) -> 20-25% (<1.8 MeV), max/min >=3x (non-uniform); computed 235U vs published Huber <4.4% over 2-7 MeV within band |
| **test-billard-variant** | **PASS** | HM held constant below 2 MeV; fractions 55.6/32.6/7.1/4.7 (235/239/238/241) correctly labelled (239Pu 0.326 > 238U 0.071, no swap); integral 4.59e12 distinct from flagship 7.50e12 |

Full suite: **57/57** (35 prior + 10 normalization + 12 table).

## Sub-1.8 MeV grounding (honest accounting per the autonomous-run directive)

The citable primary reference for the sub-1.8 MeV / sub-3.5 MeV per-isotope reactor
antineutrino spectrum is **Kopeikin (2012), Phys. At. Nucl. 75, 143-152**. I made a
genuine sourcing attempt (arXiv API search for Kopeikin antineutrino spectra): the 2012
paper is **Springer-only with no arXiv table**, and the closest arXiv work is
hep-ph/0308186 (Kopeikin 2004, already used for the n-capture normalization). **No
machine-readable Kopeikin-2012 per-isotope table was obtainable in-environment, and none
was fabricated.**

Following the directive's documented-fallback branch, the existing seam-anchored,
non-negative placeholder shape is retained, now **cited to Kopeikin 2012 as the
reference model it is qualitatively consistent with** (rising toward low E, bounded).
The model dependence is honestly covered by a **wide split band** (20% on 1.0-1.8 MeV,
25% below 1.0 MeV), and the limitation is stated in the CSV header, in this SUMMARY, and
in a Phase-2 addendum to `artifacts/stage1/ASSUMPTIONS.md`. The forbidden proxy
`fp-truncate-ibd` stays discharged (sub-1.8 MeV is populated), and `fp-loose-1e13` stays
guarded (normalized to the verified 7-8e12, not the loose ~1e13). This is
`ref-summation` (a Plan 02-01 contract reference) upgraded to **surfaced-with-caveat
naming Kopeikin 2012**; it is not a 02-02 contract reference and no fake sourced entry
was created.

## Task 3 checkpoint (checkpoint:human-verify) — satisfied pending orchestrator review

Per the autonomous-run directive, the human-verify checkpoint was executed as a
self-assessment rather than a blocking stop. Review artifacts: `reactor_flux_v1.0.csv`
(frozen table + provenance header), `flux_overlay.png` (overlay + split band), the
`reactor_flux_billard_variant.csv` closure table, and the 22 encoded tests. All four
acceptance tests self-assess **PASS**. The authoritative 7-8e12 target (not 1e13) was
used; the sub-1.8 MeV band is wide and labelled model-only; the Billard fractions are
isotope-correct (no 238U<->239Pu swap). **Recommended orchestrator decision: accept and
freeze at v1.0** and hand off to Phase 3 as the CEvNS input flux.

## Note surfaced for the orchestrator (CALC-01 wording)

`REQUIREMENTS.md` CALC-01 phrases the flux as "~1x10^13"; the authoritative Phase-1 lock
+ verified arithmetic give 7-8e12. The frozen table uses 7-8e12 (our value 7.50e12 sits
~25% below 1e13). The CALC-01 "~1e13" is an order-of-magnitude rounding, **not** a
~30%-tighter target; flagged for the orchestrator to reconcile in REQUIREMENTS.md.

## Deviations

- **Rule 4 (missing component, auto):** the overlay needed a machine-readable published
  Huber 235U curve; reused the Plan 02-01 `data/flux/huber_U235_benchmark.csv`
  (arXiv:1106.0687 tabulation) rather than re-fetching.
- **Provenance note (documented):** the CSV header `git_sha` records the code commit the
  data was *built from* (the Task-2 builder commit), the standard build-time-sha
  convention, since the committing sha cannot be known before the commit exists.
- **Sourcing gap (Kopeikin 2012), documented not deviated:** handled via the directive's
  explicit fallback branch (retain placeholder, cite Kopeikin 2012, widen band); no
  fabrication.

## Files

- Code: `src/flux/normalization.py`, `src/flux/build_flux_table.py`
- Data: `data/flux/reactor_flux_v1.0.csv`, `data/flux/reactor_flux_billard_variant.csv`
- Figure: `GPD/phases/02-reactor-flux-model/figures/flux_overlay.png`
- Tests: `tests/test_flux_normalization.py` (10), `tests/test_flux_table.py` (12)
- Note: `artifacts/stage1/ASSUMPTIONS.md` (Phase-2 addendum on the sub-1.8 MeV limitation)

## Self-Check: PASSED

## Orchestrator Return Envelope

```yaml
gpd_return:
  status: completed
  phase: "02-reactor-flux-model"
  plan: "02"
  tasks_completed: 3
  tasks_total: 3
  files_written:
    - src/flux/normalization.py
    - src/flux/build_flux_table.py
    - data/flux/reactor_flux_v1.0.csv
    - data/flux/reactor_flux_billard_variant.csv
    - GPD/phases/02-reactor-flux-model/figures/flux_overlay.png
    - tests/test_flux_normalization.py
    - tests/test_flux_table.py
    - artifacts/stage1/ASSUMPTIONS.md
    - GPD/phases/02-reactor-flux-model/02-02-SUMMARY.md
  issues:
    - "Sub-1.8 MeV fission SHAPE remains a seam-anchored MODEL PLACEHOLDER cited to Kopeikin 2012 (Phys. At. Nucl. 75, 143) as the consistent reference model; no machine-readable Kopeikin-2012 per-isotope table was sourceable in-environment (Springer-only, no arXiv table). Not fabricated; honestly covered by the wide 20-25% below-1.8 band. ref-summation (02-01) upgraded to surfaced-with-caveat."
    - "REQUIREMENTS.md CALC-01 wording '~1x10^13' is looser than the authoritative 7-8e12 target (our 7.50e12 sits ~25% below 1e13); surfaced for the orchestrator to reconcile, NOT treated as a tighter target."
    - "Task 3 (checkpoint:human-verify) executed non-blocking per the autonomous-run directive; recorded satisfied-pending-orchestrator-review with all four acceptance tests self-assessed PASS."
  next_actions:
    - "Orchestrator: accept/freeze reactor_flux_v1.0.csv at v1.0 and hand off to Phase 3 as the CEvNS input flux."
    - "Phase 3: fold Phi(E_nu) against dsigma/dT on Ge; use reactor_flux_billard_variant.csv for the Billard Table-1 reproduction."
    - "If a digitized Kopeikin-2012 / Estienne-Fallot / CONFLUX sub-1.8 MeV per-isotope table becomes available, swap it into summation_spectra.csv and re-freeze (band should then narrow below 1.8 MeV)."
    - "Reconcile REQUIREMENTS.md CALC-01 '~1e13' wording to the authoritative 7-8e12."
  decisions:
    - summary: "Normalization chain R_f=P_th/<E_f>=9.10e19 fissions/s (3 GW_th, effective-thermal <E_f>=205.8 MeV Ma-2013 NOT total Q) x 1/(4 pi d^2) at d=2500 cm applied ONCE; int Phi dE=7.50e12 nu-bar/cm2/s, emission 1.96e20/s/GW_th (Hayes-Vogel ~2e20)."
      phase: "02-reactor-flux-model"
    - summary: "Frozen data/flux/reactor_flux_v1.0.csv with 7-col additive schema, SPLIT band (2-5% >2 MeV -> 20-25% <1.8 MeV, non-uniform), region flags, and version/git-sha/normalization/provenance/integral-check header."
      phase: "02-reactor-flux-model"
    - summary: "Billard-2017 closure variant (HM constant below 2 MeV, fractions 55.6/32.6/7.1/4.7 isotope-labelled, no 238U<->239Pu swap) emitted as a distinct table (4.59e12) for the Phase-3 Billard Table-1 reproduction."
      phase: "02-reactor-flux-model"
    - summary: "Sub-1.8 MeV shape kept as a Kopeikin-2012-cited placeholder (no machine-readable Kopeikin table sourceable; none fabricated), covered by the wide low-E band; limitation documented in CSV header, SUMMARY, and ASSUMPTIONS.md."
      phase: "02-reactor-flux-model"
  contract_updates:
    claims_passed: [claim-frozen-flux]
    acceptance_tests_passed: [test-normalization, test-csv-schema, test-band-split, test-billard-variant]
    forbidden_proxies_rejected: [fp-loose-1e13, fp-norm-chain-traps, fp-uniform-band]
  state_updates:
    advance_plan: false
    update_progress: false
    record_metric:
      phase: "02"
      plan: "02-02"
      duration: 3600
      tasks: 3
      files: 9
```
