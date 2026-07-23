---
phase: 10-sub-ev-grid-extension-and-the-trigger-observable-p-grid
plan: 04
status: complete
one_liner: "Both matrices regenerated on the 744-column axis with count conservation at 3.331e-16 and zero off-grid mass; the overlap is BIT-IDENTICAL to a same-code v1.0-range rebuild (max diff 0.0), all 32 emitted anchors reproduce with zero CHECK flags -- the claimed 24 is unsourced -- and the double-count verdict is that P(zero counts) is 2e-4 or exactly 0 against 1-P_trig of 0.998/0.512/0.056, so they may be multiplied, for this model."
plan_contract_ref: GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-04-PLAN.md#/contract

contract_results:
  claims:
    claim-regenerated:
      status: passed
      summary: "R(E_rec|E_dep) regenerated for both designs and BOTH censoring variants on the 744-column extended axis, written to artifacts/v2.0/. Maximum |column sum - 1| including the underflow bin is 3.331e-16 (Ta->Al non_paralyzable) and 2.220e-16 elsewhere -- thirteen orders of magnitude inside the 1e-3 requirement, i.e. at machine precision rather than merely under tolerance. Zero samples fell off either end of the E_rec grid, counted BEFORE histogramming. Shape (161, 744), zero NaN, zero negative entries, per-cell relative MC error stored for every populated cell."
      linked_ids: [deliv-R-taal, deliv-R-alhf, deliv-R-tests, test-conservation, test-column-normalisation, test-no-mass-off-grid]
      evidence:
        - verifier: gpd-executor
          method: direct column-sum measurement plus an independent off-grid counter
          confidence: high
          claim_id: claim-regenerated
          deliverable_id: deliv-R-taal
          acceptance_test_id: test-no-mass-off-grid
          reference_id: ref-roadmap-stop
          forbidden_proxy_id: fp-renormalised-conservation
          evidence_path: GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-04-ANCHOR-AUDIT.md
    claim-overlap-intact:
      status: passed
      summary: "BITWISE: a same-code v1.0-range rebuild reproduces the corresponding 584 columns of the extended build exactly -- np.array_equal True, max |difference| 0.0, median curve identical -- for both designs. Plan 10-03's energy-keyed sub-seed took. STATISTICAL vs the archived matrices: the raw all-cells fraction beyond 3 sigma is 2.65% / 2.30%, seven to eight times the ~0.34% Gaussian expectation, and that excess was chased down rather than reported and left: restricted to cells with >= 1000 archived counts it collapses to 0.32% / 0.48%, straddling expectation. The worst Ta->Al cell holds 1 archived count against 8 new, giving |d|/sigma = 7 exactly. Per-column total variation has median exactly 0.0 and maximum 0.0632."
      linked_ids: [deliv-R-taal, deliv-R-alhf, deliv-R-tests, test-overlap-bitwise, test-overlap-vs-archived]
    claim-subev-diagnosed:
      status: passed
      summary: "Measured at 0.1, 0.5 and 1 eV for both designs. N_obs = 7.980 / 10.158 at 0.1 eV and 39.019 / 49.100 at 0.5 eV (roadmap 39.4 / 49.9, agreeing to -0.97% / -1.60%). P(zero counts) = 2e-4 at 0.1 eV for Ta->Al and exactly 0 everywhere else measured. FINDING: n_distinct is 228 / 359 out of 5000, NOT the small integer lattice the plan expected -- the mechanism was traced to fractional sensor-class populations (12.566371 and 10287.433629) plus mean-pinning rescales of 1.0515 and 1.0879. FINDING: at 0.1 eV the Al->Hf actual spread 0.2746 is 12.5% BELOW its 1/sqrt(N) label 0.3138."
      linked_ids: [deliv-R-tests, deliv-anchor-audit, test-subev-diagnostics, test-double-count-check]
    claim-anchors:
      status: passed
      summary: "The notebook executed end to end with zero error outputs and emitted 32 anchor lines, ALL within tolerance, ZERO carrying '<-- CHECK'. The count is 32, not the 24 asserted in GPD/MILESTONES.md line 41 and the v1.0 milestone audit; the reconciliation 22 literal call sites -> 32 emitted lines via loop expansion is written out, three candidate origins for '24' are examined and none reproduces it from any present artifact, and the milestone documents are flagged as carrying an unsourced count rather than the count being adjusted. The 197 MeV endpoint anchor recomputed from the NEW v2.0 matrices gives 34.7635 keV (-0.105%) and 26.8449 keV (+0.167%) against a 3% tolerance."
      linked_ids: [deliv-anchor-audit, test-anchor-rerun, test-anchor-count-audit]
  deliverables:
    deliv-R-taal:
      status: passed
      path: artifacts/v2.0/response_matrix_TaAl_ext.npz
      summary: "Ta->Al on the 744-bin extended deposit axis, same key layout as the v1.0 npz plus plan-10-04 diagnostics (N_obs_mean, P_zero_count, n_distinct_Erec, rel_spread, n_offgrid_high/low per variant). Provenance header records grid_version, the energy-keyed seed scheme, N_s = 5000, M_pool = 2000, EC_EMG_MAX = 2000, the git SHA, the sub-eV regime note, the v1-comparison note, and the linear-yield extrapolation caveat with its 6.8 ueV / 190 ueV / 0.018 quasiparticle numbers."
      linked_ids: [claim-regenerated, claim-overlap-intact]
    deliv-R-alhf:
      status: passed
      path: artifacts/v2.0/response_matrix_AlHf_ext.npz
      summary: "Al->Hf, same layout and provenance. Both censoring variants regenerated -- the paralyzable sensitivity was not dropped for runtime."
      linked_ids: [claim-regenerated, claim-overlap-intact]
    deliv-R-tests:
      status: passed
      path: tests/test_response_matrix_extended.py
      summary: "28 tests: conservation per design per variant, shapes/positivity/MC-error storage, off-grid mass, both-variants-present, provenance-header content, v1.0-artifacts-untouched via git, bitwise overlap against a same-code rebuild, statistical overlap restricted to well-populated cells, sub-eV diagnostics against the roadmap N_obs, the non-integer-lattice finding pinned as a test, the double-count inequality, trigger-not-folded-in, and the 197 MeV endpoint from the v2.0 matrices."
      linked_ids: [claim-regenerated, claim-overlap-intact, claim-subev-diagnosed]
    deliv-anchor-audit:
      status: passed
      path: GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-04-ANCHOR-AUDIT.md
      summary: "The literal nbconvert command and the extraction snippet; all 32 raw anchor lines verbatim; the 22 -> 32 reconciliation and the confrontation of the unsourced 24; the conservation and off-grid table; both overlap comparisons with the 3-sigma-versus-cell-count breakdown that resolves the apparent excess; the sub-eV diagnostic tables for both designs; the non-integer-count finding with its measured mechanism; the 1/sqrt(N)-versus-actual-spread comparison; and the double-count verdict with its inverting caveat."
      linked_ids: [claim-anchors, claim-subev-diagnosed]
  acceptance_tests:
    test-conservation:
      status: passed
      summary: "max |column sum - 1| over all 744 columns: 3.331e-16 (Ta->Al non_paralyzable), 2.220e-16 (the other three matrices). Requirement <= 1e-3. The test asserts < 1e-12 as well, because a value merely under 1e-3 would be a warning sign for a normalised column construction, not a pass."
      linked_ids: [claim-regenerated, deliv-R-taal, deliv-R-alhf, deliv-R-tests]
    test-column-normalisation:
      status: passed
      summary: "R shape (161, 744) both designs; deposit centres strictly increasing with first centre 0.1013838 eV; zero NaN; zero negative entries; per-cell relative MC error finite on every populated cell and NaN on every empty one."
      linked_ids: [claim-regenerated, deliv-R-taal, deliv-R-alhf]
    test-no-mass-off-grid:
      status: passed
      summary: "ZERO samples above the 1e5 eV ceiling and zero below the grid, counted before histogramming, across all 744 columns of all four matrices. Without this counter the conservation test would be measuring the col = h/h.sum() division rather than the physics."
      linked_ids: [claim-regenerated, deliv-R-tests]
    test-overlap-bitwise:
      status: passed
      summary: "Full 584-column comparison for both designs: np.array_equal(R_rebuild, R_ext[:, 160:]) is True with max |difference| exactly 0.0, and the median curves are array_equal too. The committed test re-runs a 10-column subset in seconds; the full comparison was run once and is reported here."
      linked_ids: [claim-overlap-intact, deliv-R-tests, deliv-R-taal]
    test-overlap-vs-archived:
      status: passed
      summary: "Ta->Al: 756 cells, median 0.000, mean 0.432, p95 2.204, max 7.00, fraction > 3 sigma 0.0265. Al->Hf: 738 cells, median 0.000, mean 0.369, p95 2.054, max 7.07, fraction 0.0230. Both are ~8x the ~0.34% Gaussian expectation for a difference of two independent estimates -- REPORTED, then resolved: at archived count >= 1000 the fractions are 0.0032 and 0.0048. Per-column total variation median exactly 0.0, max 0.0572 / 0.0632. No bit-identity is claimed."
      linked_ids: [claim-overlap-intact, deliv-R-tests, deliv-R-taal, deliv-R-alhf]
    test-subev-diagnostics:
      status: passed
      summary: "All four quantities tabulated at 0.1, 0.5 and 1 eV (and 10, 100 eV for reference) for both designs. Measured N_obs at 0.5 eV: 39.019 (Ta->Al) and 49.100 (Al->Hf), which plan 10-05 must use in place of the roadmap's 39.4 / 49.9."
      linked_ids: [claim-subev-diagnosed, deliv-anchor-audit, deliv-R-tests]
    test-double-count-check:
      status: passed
      summary: "Comparison made and verdict written with numbers. P(no counts registered) = 2.0e-4 (Ta->Al at 0.1 eV) and exactly 0.0 at every other measured point, against 1 - P_trig = 0.99831, 0.51244, 0.055784. Three to four orders of magnitude apart where both are nonzero, incommensurable where the first is zero. VERDICT: different physics, may be multiplied -- with the stated caveat that this holds only because the yield model has no pair-breaking threshold."
      linked_ids: [claim-subev-diagnosed, deliv-anchor-audit]
    test-anchor-rerun:
      status: passed
      summary: "jupyter nbconvert --to notebook --execute --inplace, timeout 1800 s. Zero error outputs from any cell. 32 anchor lines emitted, ZERO carrying '<-- CHECK'. The ROADMAP line-435 stop-condition was therefore NOT triggered."
      linked_ids: [claim-anchors, deliv-anchor-audit]
    test-anchor-count-audit:
      status: passed
      summary: "Counted: 32 emitted lines from 22 literal check(...) call sites, all 32 label strings distinct. The claimed figure 24 is NOT reproduced by any counting rule the audit could construct (call sites give 22; sections and groups give neither). GPD/MILESTONES.md line 41 and GPD/milestones/v1.0-MILESTONE-AUDIT.md lines 17 and 77 are flagged as carrying an unsourced count. Nothing was adjusted to reach 24."
      linked_ids: [claim-anchors, deliv-anchor-audit]
  references:
    ref-roadmap-p10-sc1:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Criterion 1's second half -- R regenerated for both designs on the extended axis with count conservation to <= 1e-3 and the v1.0/v1.1 anchors still reproducing -- is discharged: 3.331e-16 conservation, zero off-grid mass, 32/32 anchors clean."
    ref-roadmap-stop:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "ROADMAP line 435 is quoted at the head of the audit and its status stated explicitly: NOT TRIGGERED. Nothing was proceeded-with-and-compensated-downstream."
    ref-conventions-f:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "non-paralyzable is the canonical variant and is what every diagnostic in this plan reports. The paralyzable sensitivity was regenerated as well rather than dropped for runtime, so it remains a retained alternative and not a silently closed switch."
    ref-phase5-response:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "Compared and found NOT to transfer, which is the informative outcome. Phase 5's <= ~1.8% peak-well-populated-cell error at N_s = 5000 was measured on columns above 10.14 eV; the best per-cell relative MC error at 0.1 eV is 3.84% / 3.43%, roughly twice that, because the column's mass spreads over 24 and 22 occupied bins instead of 1-3. The v1.0 convergence result is explicitly not cited as evidence about sub-eV columns. The stable-crc32 sub-seeding requirement was preserved and strengthened by plan 10-03."
    ref-anchor-notebook:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "Executed by a recorded command; all 32 emitted lines reproduced verbatim in the audit. Compared against the claimed 24 in GPD/MILESTONES.md line 41 and GPD/milestones/v1.0-MILESTONE-AUDIT.md lines 17 and 77; the discrepancy is explained rather than absorbed."
  forbidden_proxies:
    fp-overwrite-v1-matrices:
      status: rejected
      notes: "The regenerated matrices are written to NEW paths under artifacts/v2.0/ with _ext suffixes. git status --porcelain artifacts/stage1/ shows zero tracked modifications, asserted by test_v1_artifacts_are_untouched. The anchor notebook still loads the frozen v1.0 files, so its run is a genuine independent check rather than a circular one."
    fp-renormalised-conservation:
      status: rejected
      notes: "Off-grid samples are counted BEFORE histogramming, separately from the underflow bin, and stored per column in the npz. Zero, across all 744 columns of all four matrices. Without this the reported 3.331e-16 would only be measuring the col = h / h.sum() division."
    fp-smooth-subev:
      status: rejected
      notes: "The 0.1 eV columns were characterised by measurement, not presented as smooth. The measurement produced a finding that cuts AGAINST the plan's own expectation: the column is neither smooth nor a small integer lattice -- it takes 228 / 359 distinct non-integer values, and the mechanism (fractional sensor-class populations plus mean-pinning rescales of 1.0515 and 1.0879) is traced and recorded."
    fp-anchor-count-restated:
      status: rejected
      notes: "The number was counted (32) and reported as such. The unsourced 24 is confronted directly, three candidate origins are examined and rejected, and the milestone documents are flagged. MILESTONES.md was not edited, per scope."
    fp-trigger-applied-here:
      status: rejected
      notes: "No trigger curve was folded into any matrix. test_trigger_curve_is_not_folded_into_the_matrix asserts the sub-eV columns still sum to 1 to 1e-12 and that the provenance header states the exclusion. Keeping them separate is what made the Section 6 double-count question answerable at all."
  uncertainty_markers:
    weakest_anchors:
      - "The quasiparticle yield is exactly linear with no pair-breaking threshold. MEASURED at a 0.1 eV deposit: 6.89 ueV of energy per off-spot sensor against an Al trap gap of 190 ueV, and the model assigns 0.018132 quasiparticles to that sensor. The bottom two decades of both matrices are a mean-field continuum extrapolation two decades below where the chain was ever validated. This plan can only label it, and does so in the npz provenance header so the caveat travels with the artifact."
      - "The double-count verdict 'may be multiplied' rests entirely on P(zero counts) being ~0, which is itself a consequence of that same linear yield. A model with a real pair-breaking threshold would have a large zero-count probability at 0.1 eV and the verdict could invert. Stated in the audit in the same breath as the verdict."
      - "f_prompt (0.3, range 0.1-0.5) and r (2.0 sensors, range 1-5) are LOW-confidence exposed parameters with no thin-wafer QPD measurement behind them, and they set how much energy reaches the on-spot sensors at 0.1 eV."
      - "The Phase-5 convergence result does not transfer to sub-eV columns: 3.84% / 3.43% best per-cell error at 0.1 eV versus the <= 1.8% v1.0 benchmark. Reported rather than inherited."
      - "The archived matrices sit on CSV-round-tripped deposit centres (4.918e-07 offset) AND used the ordinal seeding, so the statistical comparison against them has an irreducible mismatch beneath the Monte Carlo noise."
    unvalidated_assumptions:
      - "That the E_rec grid floor of 1e-3 eV and its underflow bin are adequate at 0.1 eV deposits. The reconstructed energy there is ~0.048-0.050 eV, comfortably inside the grid, and the underflow bin carries essentially no mass -- but 'essentially no mass' is itself the linear-yield artefact flagged above."
      - "That EC_EMG_MAX = 2000, chosen for the v1.0 range, is the right branch point for sub-eV columns. It is: at 0.1 eV both classes take the EMG branch (ec = 0.19 on-spot, 5.4e-4 off-spot), far from the split. Recorded because the plan raised it."
      - "That the mean-pinning rescale (sums *= mu_analytic / mu_pool) is a harmless normalisation. At the few-count level it is not harmless to the column SHAPE -- it is why the registered count is not an integer."
    competing_explanations:
      - "The 2.3-2.7% all-cells 3-sigma excess could be read as a genuine regression against v1.0. The cell-count breakdown rules that out: at >= 1000 archived counts the fraction is 0.0032 / 0.0048, i.e. at expectation, and the worst cell holds a single archived count. Both readings are shown so a reader can check the resolution rather than accept it."
      - "The 32-versus-24 anchor discrepancy could be read as anchors having been added since v1.0 closed rather than as a miscount. That is examined as candidate origin 1 in the audit and is not decidable from present artifacts, so neither reading is asserted."
    disconfirming_observations:
      - "DID NOT OCCUR: 'count conservation exceeds 1e-3 in any column' -- it is 3.331e-16. 'Samples fall off the top of the E_rec grid' -- zero. The ROADMAP line-435 stop-condition was NOT triggered."
      - "DID NOT OCCUR: 'any anchor stops reproducing' -- 32 of 32 clean, zero CHECK flags."
      - "DID NOT OCCUR: 'the overlapping columns are not bit-identical to a same-code v1.0-range rebuild' -- array_equal True, max difference 0.0. Plan 10-03's seed fix took."
      - "DID NOT OCCUR: 'the zero-count probability at 0.5 eV is comparable to 1 - P_trig(0.5 eV) = 0.5' -- it is exactly 0.0 for both designs across all 5000 realizations."
      - "DID OCCUR: the counted anchor total is NOT 24. It is 32, and the milestone documents carry an unsourced count."
      - "DID OCCUR: the estimator does NOT produce an integer registered count. 228 / 359 distinct non-integer values at 0.1 eV, traced to fractional sensor-class populations and mean-pinning rescales. The plan predicted a small integer lattice and explicitly named a large number as a finding."
      - "DID OCCUR: at 0.1 eV the Al->Hf actual column spread (0.2746) is 12.5% BELOW its 1/sqrt(N_obs) label (0.3138). Plan 10-05 must not quote 1/sqrt(N) there as though it described the column."
files_created:
  - artifacts/v2.0/response_matrix_TaAl_ext.npz
  - artifacts/v2.0/response_matrix_AlHf_ext.npz
  - tests/test_response_matrix_extended.py
  - GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-04-ANCHOR-AUDIT.md
files_modified:
  - src/qpd_potential/response_matrix.py
  - GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-03-GRID-CONSTRUCTION.md
---

# Plan 10-04 Summary --- Regenerated Response on the Extended Axis

## STOP-CONDITION STATUS: **NOT TRIGGERED**

ROADMAP line 435 requires revisiting the grid extension if conservation breaks
(>1e-3) or any anchor stops reproducing. Neither happened.

## Count conservation and off-grid mass

| Design | variant | max \|column sum − 1\| | off-grid high | off-grid low |
|---|---|---|---|---|
| Ta→Al | non_paralyzable | **3.331e-16** | **0** | 0 |
| Ta→Al | paralyzable | 2.220e-16 | 0 | 0 |
| Al→Hf | non_paralyzable | **2.220e-16** | **0** | 0 |
| Al→Hf | paralyzable | 2.220e-16 | 0 | 0 |

Requirement ≤ 1e-3; realised at machine precision. **The off-grid counter is what
makes this mean anything** — a column divided by its own sum always sums to 1.

Both censoring variants regenerated (paralyzable not dropped for runtime).
N_s = 5000, M_pool = 2000, EC_EMG_MAX = 2000, all at their v1.0 values. Build time
~594 s total. `artifacts/stage1/` untouched, verified by `git status`.

## The overlap — two questions, two answers

**Bitwise, against a same-code v1.0-range rebuild** — "did adding 160 columns disturb
the 584 already there?"

| Design | `array_equal` | max \|difference\| | median curve |
|---|---|---|---|
| Ta→Al | **True** | **0.0** | identical |
| Al→Hf | **True** | **0.0** | identical |

**Plan 10-03's energy-keyed sub-seed took.** Under the old ordinal scheme this
comparison would have been impossible.

**Statistically, against the archived matrices** — bit-identity neither expected nor
claimed (CSV-round-tripped centres, 4.918e-07, plus different seeding).

| Design | cells | median | p95 | max | fraction > 3σ |
|---|---|---|---|---|---|
| Ta→Al | 756 | 0.000 | 2.204 | 7.00 | **0.0265** |
| Al→Hf | 738 | 0.000 | 2.054 | 7.07 | **0.0230** |

**That looks like a failure** — ~8× the 3.4e-3 Gaussian expectation — so it was
chased down rather than reported and left:

| archived count ≥ | Ta→Al frac > 3σ | Al→Hf frac > 3σ |
|---|---|---|
| 1 | 0.0265 | 0.0230 |
| 100 | 0.0206 | 0.0150 |
| **1000** | **0.0032** | **0.0048** |

At well-populated cells it sits at expectation. The worst Ta→Al cell holds **1**
archived count against 8 new: σ = √1/5000, |Δ|/σ = 7 exactly. **Low-count Poisson
discreteness, not a regression.** Per-column total variation: median exactly 0.0,
max 0.0632.

## Anchors: **32 emitted, 0 CHECK flags — and the claimed 24 is unsourced**

| | |
|---|---|
| literal `check(...)` call sites | 22 |
| **anchor lines emitted at runtime** | **32** |
| distinct labels | 32 |
| asserted in `MILESTONES.md` line 41 and the v1.0 audit | **24** |

The 22 → 32 expansion is loop iteration over designs and gamma lines. **No counting
rule reproduces 24**: call sites give 22; no section or group structure in the
notebook gives 24; and no enumerated list exists anywhere in the repository. The
milestone documents carry an **unsourced count**, reported as such and not adjusted
(`fp-anchor-count-restated`). `MILESTONES.md` was not edited, per scope.

The notebook loads the **frozen** v1.0 matrices, so its clean run proves the Phase-10
work did not break v1.0 — it does not exercise the new matrices. The anchor that does:

| Design | paper | **from `artifacts/v2.0/`** | diff (tol 3%) |
|---|---|---|---|
| Ta→Al | 34.8 keV | **34.7635 keV** | **−0.105%** |
| Al→Hf | 26.8 keV | **26.8449 keV** | **+0.167%** |

## Sub-eV diagnostics (non-paralyzable)

| design | E_dep | N_obs | P(0 counts) | n_distinct | spread | 1/√N | best cell MC err | n_pop |
|---|---|---|---|---|---|---|---|---|
| Ta→Al | 0.10138 eV | **7.980** | **2e-4** | **228** | 0.3662 | 0.3540 | 3.84% | 24 |
| Ta→Al | 0.49382 eV | **39.019** | **0** | 1205 | 0.1622 | 0.1601 | 2.78% | 13 |
| Al→Hf | 0.10138 eV | **10.158** | **0** | **359** | 0.2746 | 0.3138 | 3.43% | 22 |
| Al→Hf | 0.49382 eV | **49.100** | **0** | 1459 | 0.1615 | 0.1427 | 2.77% | 13 |

Measured N_obs at 0.5 eV is **39.019 / 49.100** against the roadmap's 39.4 / 49.9
(−0.97% / −1.60%). **Plan 10-05 must use the measured numbers.**

### FINDING — the registered count is *not* an integer

The plan expected "C times an integer count" and named a large distinct-value count as
a finding. It is **228 / 359 non-integer values** out of 5000. Mechanism, measured:

1. Both sensor classes carry **fractional populations** — `n_spot = πr² = 12.566371`,
   `n_off = 10287.433629` — so `class_sum_samples` adds a `frac × extra` term.
2. Each class sum is then rescaled by `mu_analytic / mu_pool` = **1.0515394934**
   (on-spot) and **1.0879140042** (off-spot) to pin the class mean.

At N_obs ≈ 8 a real counting detector produces integers and a visible Poisson
staircase. The estimator smooths that into a quasi-continuum. Defensible as an
ensemble approximation — the class *means* are exact — but the column's *shape* at the
few-count level is a property of the aggregation scheme, not of counting statistics.

### FINDING — 1/√N overstates the Al→Hf spread at 0.1 eV by 12.5%

Actual std/mean **0.2746** vs 1/√N_obs **0.3138**. Plan 10-05 must carry this rather
than quote 1/√N as though it described the column. (Ta→Al agrees to +3.4%.)

### The Phase-5 convergence benchmark does not transfer

≤1.8% peak-cell error at N_s = 5000 was measured **above 10.14 eV**. At 0.1 eV the
best per-cell error is **3.84% / 3.43%** — roughly twice — because the mass spreads
over 24 and 22 bins instead of 1–3. Not cited as evidence about these columns.

## THE DOUBLE-COUNT VERDICT

| E_dep | P(no counts) Ta→Al | P(no counts) Al→Hf | 1 − P_trig |
|---|---|---|---|
| 0.10138 eV | **2.0e-4** | **0.0** | **0.99831** |
| 0.49382 eV | **0.0** | **0.0** | **0.51244** |
| 1.0142 eV | **0.0** | **0.0** | **0.055784** |

### **They describe different things and MAY be multiplied.**

The plan's disconfirming observation was that P(zero counts) at 0.5 eV might be
"comparable to 1 − P_trig = 0.5". **It is exactly zero**, across all 5000
realizations, both designs. Three to four orders of magnitude separate them where both
are nonzero. No overlapping non-detection mass.

### The caveat that could invert it

**P(zero counts) ≈ 0 is itself a consequence of the model's weakest assumption.** At
0.1 eV the linear yield gives **6.89 µeV** per off-spot sensor against a **190 µeV**
Al trap gap and assigns **0.018132 quasiparticles** to it; aggregating ~10,287 such
sensors lands at N_obs ≈ 8 with essentially no chance of zero. **A detector with a
real pair-breaking threshold would have a large zero-count probability at 0.1 eV and
this verdict could invert.**

> The verdict holds **for this model**, and it holds *because of* the assumption the
> model is least entitled to. Phases 12 and 15 may multiply R by P_trig, but must
> re-ask this question if the linear yield is replaced by a threshold model.

## The unfixable weakness, carried in the artifact

The linear-yield caveat with its 6.89 µeV / 190 µeV / 0.018132 numbers is written into
`meta_json["linear_yield_extrapolation_caveat"]` of **both** npz files and asserted by
a test, so it travels with the artifact rather than living only in a document.

**A matrix that looks smooth at 0.1 eV is not evidence that the extrapolation is
valid. It is evidence that the model is smooth.**

## Scope

No trigger curve folded in; no Phase-11 broadening; no physics spectrum produced;
`artifacts/stage1/` untouched.

## Regression

`pytest tests/`: **488 passed, 0 failed** (28 new here). The rising total reflects
Phase 9 adding tests to the same worktree concurrently.
