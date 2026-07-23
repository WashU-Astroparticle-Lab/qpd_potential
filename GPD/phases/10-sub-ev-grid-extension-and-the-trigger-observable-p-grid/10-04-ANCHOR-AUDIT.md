# Plan 10-04 --- Anchor Audit, Sub-eV Diagnostics, and the Double-Count Verdict

**Phase:** 10 --- Sub-eV Grid Extension and the Trigger Observable (P-GRID)
**Discharges:** `claim-anchors`, `claim-subev-diagnosed`; ROADMAP Phase 10 success
criterion 1 (second half) and the line-435 stop-condition.
**Interpreter:** `/opt/anaconda3/bin/python3` --- numpy 1.26.4, scipy 1.17.1, pytest 7.4.0.

> **STOP-CONDITION STATUS: NOT TRIGGERED.** Count conservation is at machine
> precision (max |column sum − 1| = 3.331e-16), zero probability mass falls off the
> E_rec grid, and every emitted anchor reproduces with zero `<-- CHECK` flags.

---

## 1. The anchor re-run

### 1.1 The literal command

```bash
cd <repo root>
/opt/anaconda3/bin/jupyter nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.timeout=1800 notebooks/paper_calculations.ipynb
```

Anchor lines were then extracted from the executed notebook's stream outputs:

```python
import json
nb = json.load(open('notebooks/paper_calculations.ipynb'))
lines = [l for c in nb['cells'] if c['cell_type'] == 'code'
           for o in c.get('outputs', []) if o.get('output_type') == 'stream'
           for l in ''.join(o['text']).splitlines()]
anchors = [l for l in lines if 'computed=' in l and 'paper=' in l]
```

`check()` appends `<-- CHECK` when a value falls outside its stated tolerance, so a
clean run is a run with zero such flags. **Zero error outputs were produced by any
cell.**

*(The in-place execution was reverted afterwards so this plan's diff stays scoped;
plan 10-05 re-runs the notebook after removing the retracted display rule.)*

### 1.2 The raw emitted anchor lines

```
  1   integrated flux [nu/cm^2/s]                    computed=     7.5e+12  paper=     7.5e+12  (+0.04%)
  2   REACTOR_FLUX param [nu/cm^2/s]                 computed=     7.5e+12  paper=     7.5e+12  (+0.00%)
  3   sigma(72Ge, 4 MeV) [cm^2]                      computed=  1.0026e-40  paper=  1.0000e-40  (+0.26%)
  4   integral dR/dT above 50 eV_nr [/kg/day]        computed=       67.75  paper=        67.8  (-0.07%)
  5   k factor                                       computed=     0.01112  paper=     0.01112  (-0.00%)
  6   Cauchy mean chord 4V/S [cm]                    computed=       0.385  paper=       0.385  (-0.04%)
  7   xi width [MeV]                                 computed=      0.0720  paper=      0.0720  (+0.03%)
  8   total muon rate [Hz]                           computed=        1.37  paper=       1.366  (+0.29%)
  9   vertical MPV deposit [MeV]                     computed=       1.216  paper=        1.23  (-1.16%)
 10   vertical mean deposit [MeV]                    computed=       1.459  paper=        1.46  (-0.10%)
 11   edge(40K 1461) [keV]                           computed=        1243  paper=        1243  (+0.03%)
 12   edge(214Bi 1764) [keV]                         computed=        1541  paper=        1541  (+0.02%)
 13   edge(208Tl 2615) [keV]                         computed=        2382  paper=        2382  (-0.01%)
 14   bound single-scatter rate [Hz]                 computed=       0.268  paper=       0.267  (+0.55%)
 15   Phi*sigma_KN*N_e anchor [Hz]                   computed=       0.273  paper=       0.273  (+0.02%)
 16   double-scatter fraction @1 MeV                 computed=      0.0138  paper=      0.0140  (-1.58%)
 17   E_onset (Ta->Al)                               computed=        1.27  paper=        1.27  (-0.26%)
 18   E_onset (Al->Hf)                               computed=        0.77  paper=        0.77  (-0.10%)
 19     crossover default point [eV]                 computed=       52.91  paper=        52.9  (+0.01%)
 20     whole-array plateau [eV]                     computed=   1.864e+04  paper=    1.86e+04  (+0.20%)
 21     crossover default point [eV]                 computed=       32.13  paper=        32.1  (+0.09%)
 22     whole-array plateau [eV]                     computed=   1.132e+04  paper=    1.13e+04  (+0.17%)
 23     E_rec endpoint (Ta->Al) [keV]                computed=        34.8  paper=        34.8  (-0.10%)
 24     E_rec endpoint (Al->Hf) [keV]                computed=        26.8  paper=        26.8  (+0.17%)
 25     cevns peak E_rec [keV]                       computed=      0.0422  paper=       0.042  (+0.40%)
 26     muon peak E_rec [keV]                        computed=        18.8  paper=        18.8  (+0.19%)
 27     compton peak E_rec [keV]                     computed=        16.8  paper=        16.8  (-0.07%)
 28     cevns peak E_rec [keV]                       computed=      0.0422  paper=       0.042  (+0.40%)
 29     muon peak E_rec [keV]                        computed=          15  paper=          15  (-0.25%)
 30     compton peak E_rec [keV]                     computed=        13.3  paper=        13.3  (+0.26%)
 31   mean inter-event time [s]                      computed=        0.61  paper=        0.61  (+0.39%)
 32   pileup occupancy R*tau @20 us                  computed=     3.3e-05  paper=     3.3e-05  (-1.03%)
```

**Zero lines carry `<-- CHECK`.** Every anchor reproduces within its tolerance.

---

## 2. THE ANCHOR COUNT --- measured, and it is not 24

| Quantity | Value |
|---|---|
| Literal `check(...)` call sites in the notebook's code cells | **22** |
| **Anchor lines actually emitted at runtime** | **32** |
| Distinct label strings among them | **32** |
| Figure asserted in `GPD/MILESTONES.md` line 41 and `GPD/milestones/v1.0-MILESTONE-AUDIT.md` lines 17 / 77 | **24** |

**The count is 32, not 24.** It is not adjusted to 24 to make the roadmap phrase
"all 24 v1.0/v1.1 anchors still reproducing" read cleanly --- doing so would launder
an unsourced number through a phase gate (`fp-anchor-count-restated`).

### 2.1 Reconciling 22 → 32

Ten of the emitted lines come from loop expansion over the two trapping designs at
six call sites:

| Loop-expanded label | designs | lines |
|---|---|---|
| `E_onset (...)` | Ta→Al, Al→Hf | 2 |
| `crossover default point [eV]` | Ta→Al, Al→Hf | 2 |
| `whole-array plateau [eV]` | Ta→Al, Al→Hf | 2 |
| `E_rec endpoint (...) [keV]` | Ta→Al, Al→Hf | 2 |
| `cevns / muon / compton peak E_rec [keV]` | Ta→Al, Al→Hf | 6 |
| `edge(...) [keV]` | three gamma lines | 3 |

### 2.2 Where 24 could have come from --- and why none of it is checkable

**No enumerated list of the 24 exists anywhere in the repository.** The figure
appears only as prose in two milestone documents. Candidate explanations, none of
which reproduces 24 from any artifact now present:

1. **A count taken before some anchors were added.** Plausible: `MILESTONES.md`
   line 41 predates the Phase-6/7 additions. Not checkable without the notebook's
   state at that commit.
2. **A count of call sites rather than emitted lines.** Gives 22, not 24.
3. **A count of *sections* or of *anchor groups*.** Not reproducible from any
   grouping in the notebook that this audit could construct.

**Verdict: `GPD/MILESTONES.md` line 41 and `GPD/milestones/v1.0-MILESTONE-AUDIT.md`
lines 17 and 77 carry an UNSOURCED anchor count.** This audit reports the measured
number, 32, and flags the discrepancy. Per the plan's scope, `MILESTONES.md` is not
edited here.

### 2.3 What the notebook run does and does not prove

The notebook loads the **frozen** `artifacts/stage1/response_matrix_*.npz`. Its clean
run therefore proves that **the Phase-10 grid, guard and seeding work did not break
v1.0** --- it does *not* exercise the regenerated matrices at all.

The anchor that does exercise them is recomputed independently below.

### 2.4 The 197 MeV endpoint anchor, recomputed from `artifacts/v2.0/`

Notebook tolerance for this anchor is `tol_pct = 3`.

| Design | Paper | Notebook (frozen v1.0 npz) | **Recomputed from v2.0 `_ext` npz** | difference |
|---|---|---|---|---|
| Ta→Al | 34.8 keV | 34.8 keV (−0.10%) | **34.7635 keV** | **−0.105%** |
| Al→Hf | 26.8 keV | 26.8 keV (+0.17%) | **26.8449 keV** | **+0.167%** |

Both well inside the 3% tolerance. The regenerated matrices reproduce the endpoint
anchor independently of the archive.

---

## 3. Count conservation and off-grid mass

| Design | variant | max \|column sum − 1\| | samples off the TOP of the E_rec grid | samples below |
|---|---|---|---|---|
| Ta→Al | non_paralyzable | **3.331e-16** | **0** | 0 |
| Ta→Al | paralyzable | 2.220e-16 | 0 | 0 |
| Al→Hf | non_paralyzable | **2.220e-16** | **0** | 0 |
| Al→Hf | paralyzable | 2.220e-16 | 0 | 0 |

Requirement is ≤ 1e-3. The realised value is **thirteen orders of magnitude
tighter**, which is what a correctly normalised column construction should give; a
value merely under 1e-3 would have been a warning sign, not a pass.

**The off-grid counter is what makes this mean anything** (`fp-renormalised-conservation`).
`np.histogram` silently discards samples above the top edge and `col = h / h.sum()`
then renormalises whatever survives, so a column always sums to 1 no matter how much
was thrown away. Off-grid samples are therefore counted **before** histogramming.
Zero, in all four matrices, across all 744 columns.

`R` shape (161, 744) for both designs; deposit centres strictly increasing; zero NaN;
zero negative entries; per-cell relative Monte Carlo error stored for every populated
cell. **Both censoring variants were regenerated** --- the paralyzable sensitivity was
not dropped for runtime (`fp-single-censoring`). Total build time ~594 s for the two
designs × two variants at N_s = 5000, M_pool = 2000, EC_EMG_MAX = 2000, i.e. all
three at their v1.0 values so the comparison is like for like.

---

## 4. The overlap above 10.14 eV --- two comparisons answering two questions

### 4.1 BITWISE, against a same-code v1.0-range rebuild

This is the question "did adding 160 columns disturb the 584 that were already
there?", and it is answerable exactly because plan 10-03 keyed the sub-seed to the
deposit energy.

| Design | `np.array_equal(R_rebuild, R_ext[:, 160:])` | max \|difference\| | median curve identical |
|---|---|---|---|
| Ta→Al | **True** | **0.0** | **True** |
| Al→Hf | **True** | **0.0** | **True** |

Full 584-column comparison, `non_paralyzable`. **Plan 10-03's energy-keyed sub-seed
took.** Under the pre-10-03 ordinal scheme this would have been impossible and every
v1.0 comparison in this phase would have collapsed to statistics.

### 4.2 STATISTICAL, against the archived v1.0 matrices

Different question, and **bit-identity is neither expected nor claimed**: the archived
matrices were built on CSV-round-tripped deposit centres differing by 4.918e-07
(`fp-bit-identical-promise`), and under a different (ordinal) seeding, so the samples
are independent draws.

Differences are normalised by the **absolute** per-cell Monte Carlo error stored in
the archived npz, `sigma = R_arch × err_arch`.

| Design | cells | median | mean | p95 | max | **fraction > 3σ** |
|---|---|---|---|---|---|---|
| Ta→Al | 756 | 0.000 | 0.432 | 2.204 | 7.00 | **0.0265** |
| Al→Hf | 738 | 0.000 | 0.369 | 2.054 | 7.07 | **0.0230** |

**A naive reading of this is a failure.** A difference of two *independent* estimates
has σ_diff ≈ √2 σ, so the Gaussian expectation for |Δ|/σ > 3 is ≈ 3.4e-3. The measured
2.3–2.7% is **seven to eight times that**. Reporting it and stopping there would be
the honest-but-incomplete answer, so the excess was chased down.

**It is low-count Poisson discreteness, not a regression.** Restricting to
well-populated cells, where a Gaussian 3σ criterion actually applies:

| archived cell count ≥ | Ta→Al: n / frac > 3σ / max | Al→Hf: n / frac > 3σ / max |
|---|---|---|
| 1 | 756 / **0.0265** / 7.00 | 738 / **0.0230** / 7.07 |
| 10 | 716 / 0.0251 / 5.70 | 708 / 0.0212 / 7.07 |
| 100 | 679 / 0.0206 / 5.70 | 666 / 0.0150 / 7.07 |
| **1000** | 625 / **0.0032** / 4.25 | 620 / **0.0048** / 4.57 |

At ≥ 1000 counts the fraction collapses to **0.0032 / 0.0048**, straddling the
3.4e-3 expectation for two independent samples. The worst cell in Ta→Al is the
mechanism in plain sight: **archived count = 1, new count = 8**, so
σ = √1/5000 and |Δ|/σ = 7 exactly. A Gaussian tail criterion applied to a cell
holding one count is meaningless.

**How much probability mass actually disagrees:** per-column total variation
Σ|R_ext − R_arch|: **median exactly 0.0000**, p95 0.0195 / 0.0147, max 0.0572 / 0.0632.
Most columns agree exactly (deep-saturation deltas landing in one bin); the worst
column moves under 6.4% of its mass, consistent with Monte Carlo resampling at
N_s = 5000 where a typical populated column has ~13 occupied bins.

**Verdict: consistent with independent Monte Carlo sampling.** The raw all-cells 3σ
fraction is reported above rather than suppressed, because a reader who computes it
themselves must find it already explained.

---

## 5. Sub-eV column diagnostics --- measured, not assumed smooth

`non_paralyzable`. `N_obs` is the mean registered count; `P(0 counts)` the probability
of zero registered counts; `n_distinct` the number of distinct reconstructed-energy
values among the 5000 realizations; `n_pop` the number of occupied E_rec bins.

### Ta→Al

| target | E_dep (eV) | N_obs | P(0 counts) | n_distinct | rel. spread | 1/√N_obs | E_rec median (eV) | best cell MC err | n_pop |
|---|---|---|---|---|---|---|---|---|---|
| 0.1 eV | 0.10138 | **7.980** | **2e-4** | **228** | 0.3662 | 0.3540 | 0.048002 | 0.0384 | 24 |
| 0.5 eV | 0.49382 | **39.019** | **0** | 1205 | 0.1622 | 0.1601 | 0.24601 | 0.0278 | 13 |
| 1 eV | 1.0142 | 79.782 | 0 | 2173 | 0.1216 | 0.1120 | 0.50395 | 0.0241 | 9 |
| 10 eV | 10.145 | 773.399 | 0 | 4800 | 0.0346 | 0.0360 | 4.8975 | 0.0163 | 3 |
| 100 eV | 98.603 | 6557.064 | 0 | 4984 | 0.0116 | 0.0123 | 41.534 | 0.0141 | 1 |

### Al→Hf

| target | E_dep (eV) | N_obs | P(0 counts) | n_distinct | rel. spread | 1/√N_obs | E_rec median (eV) | best cell MC err | n_pop |
|---|---|---|---|---|---|---|---|---|---|
| 0.1 eV | 0.10138 | **10.158** | **0** | **359** | 0.2746 | 0.3138 | 0.050332 | 0.0343 | 22 |
| 0.5 eV | 0.49382 | **49.100** | **0** | 1459 | 0.1615 | 0.1427 | 0.2442 | 0.0277 | 13 |
| 1 eV | 1.0142 | 100.651 | 0 | 2413 | 0.1230 | 0.0997 | 0.50209 | 0.0242 | 10 |
| 10 eV | 10.145 | 965.113 | 0 | 4820 | 0.0311 | 0.0322 | 4.8239 | 0.0150 | 3 |
| 100 eV | 98.603 | 8021.322 | 0 | 4976 | 0.0105 | 0.0112 | 40.12 | 0.0162 | 2 |

**Measured N_obs at 0.5 eV: 39.019 (Ta→Al) and 49.100 (Al→Hf)**, against the
roadmap's 39.4 / 49.9 --- agreement to −0.97% and −1.60%. These are the numbers plan
10-05 must use; the roadmap figures come from an orchestrator note, not a verified
deliverable.

**N_obs ≈ 8–10 at 0.1 eV is reproduced** (7.980 / 10.158).

### 5.1 FINDING --- the registered count is NOT an integer

The plan's verify step said: *"the number of distinct reconstructed values at 0.1 eV
should be small and of order the spread of a count near N_obs ~ 10, not hundreds; if
it is large, the estimator is not what Phase 5 documented and that is a finding."*

**It is hundreds: 228 (Ta→Al) and 359 (Al→Hf) distinct values from 5000 samples**, and
they are not integers times C. Measured range for Ta→Al at 0.1 eV: N_obs from 0.0000
to **20.3066**, quantiles [0, 3.2637, 7.579, 12.9822, 20.3066].

**Mechanism, measured directly rather than inferred:**

1. **Both sensor classes carry FRACTIONAL populations.** `n_spot = π r² = 12.566371`
   (fractional part 0.566371) and `n_off = 10287.433629` (fractional part 0.433629).
   `class_sum_samples` handles this as `floor(n)` aggregate **plus** `frac × extra`,
   which adds a non-integer piece to each class sum.
2. **Each class sum is then rescaled to pin its mean to the analytic estimator:**
   `sums *= mu_analytic / mu_pool`. At 0.1 eV for Ta→Al those factors are
   **1.0515394934** (on-spot) and **1.0879140042** (off-spot) --- different, and
   neither an integer.

Consequence: the on-spot class sum takes 28 distinct values, the off-spot 16, and the
total 228 --- a two-dimensional lattice of two independently-rescaled quantities.
`np.allclose(total, round(total))` is **False**.

**Why this matters.** At N_obs ≈ 8 a real counting detector produces an integer
number of registered tunneling events and a visible Poisson staircase. The estimator
as implemented smooths that into a quasi-continuum. It is a defensible ensemble
approximation --- the class means are exact --- but it is **not** what "E_rec = C ×
total_N_obs" implies, and it means the sub-eV column's *shape* at the few-count level
is a property of the aggregation scheme rather than of counting statistics.

### 5.2 The 1/√N label versus the actual column spread at 0.1 eV

| Design | actual std/mean | 1/√N_obs | agreement |
|---|---|---|---|
| Ta→Al | **0.3662** | 0.3540 | +3.4% |
| Al→Hf | **0.2746** | 0.3138 | **−12.5%** |

For **Al→Hf the Gaussian 1/√N label overstates the actual spread by 12.5%** at
0.1 eV. Plan 10-05 must carry this rather than quote 1/√N_obs as though it described
the column. (Above 10 eV the two agree to a few percent, as the table in Section 5
shows.)

### 5.3 The convergence benchmark does NOT transfer

Phase 5 measured ≤ ~1.8% relative error in the peak well-populated cell at
N_s = 5000 --- **on columns above 10.14 eV**. The sub-eV columns are a different
regime: the best per-cell relative MC error at 0.1 eV is **3.84% (Ta→Al) / 3.43%
(Al→Hf)**, roughly twice the v1.0 benchmark, because the column's mass is spread over
24 and 22 occupied bins instead of 1–3. The v1.0 convergence result is **not**
evidence about these columns and is not cited as though it were.

---

## 6. THE DOUBLE-COUNT VERDICT --- with numbers, before anything multiplies them

The response matrix already places finite probability on **"no counts were
registered"**. The plan 10-02 trigger curve places **1 − P_trig** on **"the event was
not triggered"**. Phases 12 and 15 will multiply them.

| E_dep | **P(no counts registered)** Ta→Al | **P(no counts registered)** Al→Hf | **1 − P_trig** | ratio (Ta→Al) |
|---|---|---|---|---|
| 0.10138 eV | **2.0e-4** | **0.0** | **0.99831** | 2.0e-4 |
| 0.49382 eV | **0.0** | **0.0** | **0.51244** | 0 |
| 1.0142 eV | **0.0** | **0.0** | **0.055784** | 0 |

### VERDICT: **they describe different things and MAY be multiplied.**

At 0.5 eV the plan's own disconfirming observation was that P(zero counts) might be
"comparable to 1 − P_trig(0.5 eV) = 0.5". **It is not: it is exactly zero**, across
all 5000 realizations, for both designs. At 0.1 eV it is 2.0e-4 --- a single
realization out of 5000 for Ta→Al, and none for Al→Hf --- against 1 − P_trig = 0.998,
a ratio of 2.0e-4. The two quantities differ by three to four orders of magnitude
where they are both nonzero, and are incommensurable where the first is exactly zero.
There is no overlapping non-detection mass to double-count.

### The caveat that cuts against this verdict, stated in the same breath

**P(zero counts) ≈ 0 is itself a consequence of the model's weakest assumption.**
`energy_scale.n_qp_yield` is exactly linear with no pair-breaking threshold, so at a
0.1 eV deposit it assigns **0.018132 quasiparticles per off-spot sensor** against an
Al trap gap of **190 µeV** with only **6.89 µeV** of energy actually available per
off-spot sensor. The aggregate over ~10,287 sensors then lands at N_obs ≈ 8 with
essentially no chance of zero.

**A detector with a real pair-breaking threshold would have a large zero-count
probability at 0.1 eV**, and the verdict above could invert. So:

> The verdict "may be multiplied" holds **for this model**, and the reason it holds
> is precisely the assumption the model is least entitled to. Phases 12 and 15 may
> multiply R by P_trig, but they must re-ask this question if the linear yield is
> ever replaced by a threshold model.

---

## 7. The unfixable weakness, carried rather than hidden

`energy_scale.n_qp_yield` is exactly linear, `N_qp = ε·E_sensor/Δ_tr`, with no
pair-breaking threshold and no discreteness. Measured at a 0.1 eV deposit for Ta→Al:

| Quantity | Value |
|---|---|
| off-spot energy per sensor | **6.89 µeV** |
| Al trap gap Δ_tr | **190 µeV** |
| quasiparticles assigned per off-spot sensor | **0.018132** |

**The model assigns 0.018 quasiparticles to a sensor that could not energetically
host one.** The bottom two decades of these matrices are a **mean-field continuum
extrapolation two decades below where the chain was ever validated**. This plan can
label it; it cannot fix it.

This caveat is written into the provenance header of both npz files
(`meta_json["linear_yield_extrapolation_caveat"]`) and asserted by
`tests/test_response_matrix_extended.py::test_provenance_header_carries_the_required_caveats`,
so it travels with the artifact rather than living only in a document.

**A matrix that looks smooth at 0.1 eV is not evidence that the extrapolation is
valid.** It is evidence that the model is smooth.

Two further LOW-confidence inputs set how much energy reaches the on-spot sensors at
0.1 eV: `f_prompt` (0.3, range 0.1–0.5) and `r` (2.0 sensors, range 1–5). Neither has
a thin-wafer QPD measurement behind it.

---

## 8. Scope discipline

- The trigger curve was **not** folded into any matrix (`fp-trigger-applied-here`).
  It is an analysis efficiency on a rate, not part of the response kernel; baking it
  in would make it impossible for Phases 12 and 15 to report the un-triggered rate,
  and would have hidden the question Section 6 answers.
- The Phase-11 impulse-approximation broadening is **not** applied.
- **No physics spectrum was produced.**
- `artifacts/stage1/response_matrix_*.npz` are **unmodified** --- verified by
  `git status --porcelain artifacts/stage1/`, asserted by a test.
