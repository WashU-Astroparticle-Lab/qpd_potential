# 12-02 — The Signal Spectrum: reactor CEvNS `dR/dE_rec` from 100 meV (CALC-25)

**Phase:** 12 — Reactor CEvNS down to 100 meV at the Paper's Surface Scenario (P-SIG)
**Plan:** 12-02 (wave 2) — **the milestone's decisive signal deliverable**

**Normalization (primary and only):** frozen `data/flux/reactor_flux_v1.0.csv`, 3 GW_th at
25 m, surface, unshielded, used **unmodified**. No rescale of any kind is applied — not a
VNS rescale, not a duty cycle, not a shielding or overburden credit.

**Reproducing command:**

```
PYTHONPATH=src /opt/anaconda3/bin/python3 -m qpd_potential.cevns_subev 12-02
/opt/anaconda3/bin/python3 -m pytest tests/test_cevns_subev_fold.py -q
```

Environment: `/opt/anaconda3/bin/python3`, numpy 1.26.4, scipy 1.17.1, pytest 7.4.0. The
whole chain is deterministic — the Monte Carlo lives in the frozen Phase-10 response
matrices, not here, so no seed is drawn at run time.

---

## 1. Pipeline position and the recorded switch decisions

```
cevns.differential_rate                       (frozen Phi, unmodified)
        |
        v   artifacts/v2.0/cevns_dRdT_ext.csv   -- UNBROADENED, 480 bins,
        |                                          bottom bin EDGE = 0.0999350 eV
        v   IA Gaussian kernel, sigma_E = sqrt(E_R * omega_bar)   <-- ON THE RECOIL AXIS
        |                                                             APPLIED EXACTLY ONCE
        v   rebin onto the 744-bin extended DEPOSIT grid
        |
        v   R(E_rec|E_dep) from response_matrix_{TaAl,AlHf}_ext.npz  (161 x 744)
        |
        v   P_trig(E_dep) as an ANALYSIS efficiency, on top of eps
        |
        v   artifacts/v2.0/cevns_dRdErec_ext_{TaAl,AlHf}.csv
```

### Switch decisions, recorded

| switch | state in Phase 12 | global default | how |
|---|---|---|---|
| IA broadening | **ON** | `ia_broadening.BROADENING_DEFAULT` is still **`False`** | `broaden=True` passed at the Phase-12 call site in `fold.run_cevns_fold_extended`. The global default was **not** flipped: a Phase-11 test asserts it, and that fail-safe is the reason turning the kernel on had to be a deliberate act. |
| extended axis | **ON** | `muon_deposit.shared_energy_grid` still defaults to `v1.0` | the 744-bin axis arrives through the `_ext.npz` response matrices, not through a changed default. |

A separate `fold.run_cevns_fold_extended` entry point exists because `fold.run_fold` folds
all three channels and **raises** if the muon/Compton deposit grids do not match the
response matrix's `E_dep` centres — and those two channels are still on the 584-bin v1.0
axis, where **Phase 15** will move them. Phase 12 does not touch them in either direction
(`fp-electron-recoil-leak`).

### Where `P_trig` is evaluated, and why it matters

`CONVENTIONS.md` §I defines **`P_trig(E_dep)`** and puts the regime boundary at
**1.0 eV of deposited energy**. It is therefore evaluated on the **deposit** axis, and the
trigger-weighted reconstructed spectrum is `R @ (P_trig(E_dep) · N_dep)` — literally the
"multiply the response matrix by the trigger curve" operation whose licence Phase 10
established.

Evaluating `P_trig` on the *reconstructed* axis instead would have moved the 0.5 eV 50 %
point by the ≈0.47 response slope — i.e. changed §I without amending it. Not done.

Consequence, stated rather than hidden: the trigger-weighted **`dR/dE_rec`** column is not
`P_trig × dR/dE_rec` bin-by-bin, because the fold mixes deposits into each reconstructed
bin. The exact factorisation `composed = P_trig × untriggered` is asserted on the deposit
axis, where §I defines it. The spectra CSVs therefore carry `P_trig_effective =
dRdErec_trigger_weighted / dRdErec_central` — an exact ratio of two quantities this fold
actually produced, **not** an interpolation of `P_trig` onto the reconstructed axis (which
would need a mapping the response matrix does not provide below its first median, and
clamping there is exactly the silent-extrapolation failure the Phase-10 guards exist
against).

### The 4.4e-08 axis offset, recorded rather than absorbed

The project's stated extended-grid floor **0.0999350 eV** is a *rounded* display value; the
exact edge is **0.09993504432008873 eV**. Plan 11-04 anchored its 480-bin recoil axis on the
rounded value and this plan reuses that construction, so the recoil axis's bottom edge sits
**4.4×10⁻⁸ relative below** the deposit-grid floor. That is orders of magnitude below
anything this phase claims, and the floor-coverage check in `run_cevns_fold_extended` is
written on the bottom **edge** (not the first knot) so it passes for the right reason.

---

## 2. The spectra

| | Ta→Al | Al→Hf |
|---|---|---|
| peak `dR/dE_rec` (central) | **≈ 4.4 × 10³** counts/kg/day/keV | **≈ 4.7 × 10³** counts/kg/day/keV |
| at `E_rec` | ≈ 0.30 eV | ≈ 0.19 eV |
| peak trigger-weighted `dR/dE_rec` | ≈ 4.0 × 10³ | ≈ 4.1 × 10³ |
| at `E_rec` | ≈ 0.67 eV | ≈ 0.75 eV |
| integrated reconstructed rate | 118.730 counts/kg/day | 118.730 counts/kg/day |
| …trigger-weighted | 117.746 counts/kg/day | 117.746 counts/kg/day |
| counts below `E_rec` = 1 eV | 3.961 | 3.967 |
| 1.0 eV deposit boundary → `E_rec` image | 0.49724 eV | 0.49586 eV |

Both spectra span from a reconstructed energy of a few meV to ≈1 keV. The reconstructed axis
is *coarse relative to the deposit axis* in the bottom decade (161 `E_rec` bins against 744
deposit bins), so the sub-eV spectrum fluctuates bin to bin; that is the frozen response
matrix's binning, not structure in the physics.

The two designs carry **identical** integrated rates because `R`'s columns each sum to 1 —
the design changes *where* counts land, not how many there are.

### Precision discipline

Peak values are quoted to two significant figures and the 100 meV region to **one**
significant figure. Phase 11 was explicit: *do not quote the 100 meV bin to better than one
significant figure*. The artifacts carry full precision so the numbers are auditable; the
prose does not pretend to it.

---

## 3. The counts budget — closes on retained + leaked, misses on retained only

Identical for both designs (the budget is set upstream of `R`):

| quantity | counts/kg/day | fraction of input |
|---|---|---|
| input recoil counts | 118.78812499 | — |
| leaked **below the floor** | 0.051468407 | **0.043328 %** |
| …of which at unphysical `T < 0` | 0.00067386 | **0.000567 %** |
| leaked above the top | 0.0 | 0 |
| on the deposit grid | 118.73000441 | — |
| after folding through `R` | 118.73000441 | — |

- **Residual on retained + leaked: 5.600 × 10⁻⁵**, against the 1 × 10⁻³ target. ✅
- **Residual on retained ONLY: −4.893 × 10⁻⁴.** It **misses**, and it must: ~49 % of the
  bottom bin genuinely leaves the axis. A clean retained-only closure would be positive
  evidence of a hidden rescale.
- **Residual across the fold: exactly 0.0** — `R`'s columns sum to 1.

The Phase-11 leakage numbers survive the extra fold stage **unchanged**: the bottom bin
(centre 0.1010208 eV, `σ_E` = 0.042476 eV) puts **48.980311 %** of its kernel below the floor
and **0.869608 %** at `T < 0`. Nothing is renormalized (`fp-renormalize-leakage`), and
`test_leakage_not_renormalized` proves it the only way that cannot be faked: scaling the
input table by an arbitrary constant scales every output bin and every leakage entry by
exactly that constant. No global post-fold rescale can satisfy that, because a rescale
factor depends on the total.

**Measured numerical honesty note.** The amplitude-linearity deviation is **5.1 × 10⁻¹³**,
not machine epsilon. It is understood: `fold._loglog_segment_integral` forms the power-law
exponent `p = log(y₂/y₁)/log(T₂/T₁)`, and `log(T₂/T₁)` is only 0.0216 on this recoil grid, so
a 10⁻¹⁶ rounding in the scaled ratio becomes ~10⁻¹⁴ in `p`, which `T^p` then amplifies by
`ln T`. It is a property of the log-log rebin, not of any rescale — and the test stays
decisive because a genuine renormalization would violate linearity by O(1), not by
O(10⁻¹²).

---

## 4. The trigger composes, it does not replace ε — three legs

| leg | result |
|---|---|
| **exact factorisation on every grid point** | `trigger.compose_efficiency(E_dep, dRdEdep)` is bit-identical to `P_trig(E_dep) × dRdEdep` (`np.array_equal`), on the deposit axis where CONVENTIONS §I defines the composition. ✅ |
| **`P_trig ≡ 1` reproduces the untriggered fold bit-for-bit** | folding with an all-ones `P_trig` gives `N_rec_trigger` bit-identical to `N_rec`; max difference **exactly 0.0**. The curve is a factor added on top, not a modification of the chain. ✅ |
| **ε perturbation** | `P_trig` is **bit-identical** under a ×1.37 perturbation of `params.EPSILON`, while `energy_scale.n_qp_yield` moves by exactly ×1.37; and `compose_efficiency` is exactly multiplicative in its `untriggered` argument at ×0.5, ×2.0 and ×7.3. ✅ |

**Honest scope note on the third leg.** The *literal* end-to-end form the plan asks for —
perturb `params.EPSILON`, watch the folded spectrum move — **cannot be run here**, because
`R` is loaded from a **frozen npz** and does not re-derive `response.calibrate_C` at fold
time. Perturbing ε at runtime moves neither `composed` nor `untriggered`, so the end-to-end
version would be **vacuous**: it would pass while testing nothing. What is tested instead is
the substance of the requirement — `P_trig` does not see ε, the response chain does, and the
composition is exactly multiplicative. This is recorded as a test that was *reformulated*,
not as one that passed as written.

**Structural checks** (`test_e50_structural`, a units-and-wiring check, **not** corroboration
of any physics): `P(0.5 eV) = 1/2` to < 10⁻¹² for **every** `k` in the scan; and at `k = 4`,
`P(1.0 eV) = 16/17`, `P(0.25 eV) = 1/17`, `P(0) = 0` exactly.

---

## 5. The `k`-sensitivity — CONVENTIONS §I's obligation discharged in data

`k` is fixed by **no project artifact**. Phase 12 is the first downstream result computed
with this curve, so §I's standing sensitivity obligation lands here. Discharged in
`artifacts/v2.0/cevns_subev_trigger.csv`, not in prose.

Trigger-weighted CEvNS rate below the regime boundary (counts/kg/day):

| `k` | Ta→Al | % of untriggered | Al→Hf | % of untriggered |
|---|---|---|---|---|
| 1 | 0.8202 | 47.35 % | 0.8191 | 47.29 % |
| 2 | 0.8007 | 46.22 % | 0.7990 | 46.13 % |
| 4 (default) | 0.8080 | 46.64 % | 0.8063 | 46.55 % |
| 8 | 0.8358 | 48.25 % | 0.8350 | 48.21 % |
| 12 | 0.8473 | 48.91 % | 0.8468 | 48.89 % |
| **spread over [1, 12]** | **5.67 %** of the mean | | **5.82 %** of the mean | |

Compared against the other two smearing mechanisms at 0.5 eV:

| mechanism at 0.5 eV | Ta→Al | Al→Hf |
|---|---|---|
| IA fractional width on the locked ω̄ | 18.900 % | 18.900 % |
| Phase-10 counting floor | 16.009 % | 14.271 % |
| **in quadrature** | **24.769 %** | **23.682 %** |
| `k` spread over [1, 12] | 5.67 % | 5.82 % |

### Verdict: **`k` does NOT dominate.**

The `k` spread is roughly **a quarter** of the combined IA-width/counting-floor smearing.
That is an informative result and it goes in the headline rather than a footnote — the plan
required it to be stated either way. The sub-eV observable is *not* controlled by the
unmeasured device parameter; it is controlled by the nuclear zero-point width and the
counting statistics, both of which the project does model.

Two caveats on that reassurance:

1. The dependence is **non-monotonic** — it dips at `k` ≈ 2 and rises again — because a
   broader curve simultaneously gains acceptance above 0.5 eV and loses it below. The
   "spread" is a range, not a trend, and a different integration window would give a
   different number.
2. The counting floor entering that quadrature is a **best case with no noise sources**, not
   a resolution model (`fp-poisson-as-resolution`). If real noise were included, the
   comparison would move *further* against `k` dominating, not toward it — so the verdict is
   robust in direction, but the 24.8 %/23.7 % figures are floors, not estimates.

---

## 6. The width-reporting decision — **RECORDED AND LABELLED**

**Decision taken: the central curve stays on the LOCKED harmonic ω̄ = 17.8597 meV, and the
×1.163941 arithmetic-mean moment correction ships as a SEPARATE one-sided upper-WIDTH
column.** Never absorbed, never averaged. There is no lower band — Cauchy–Schwarz forces
`ω̄_p ≥ ω̄_u`.

| option | what it gives | what it costs |
|---|---|---|
| **A — taken.** Central on the locked harmonic ω̄; arithmetic mean as a one-sided upper-width band. | `CONVENTIONS.md` §J's identities `2W = E_R/ω̄` and `σ_E = √(E_R ω̄)` stay **exact**; no convention changes mid-milestone; the systematic is visible and separable. | The central curve **knowingly understates** the smearing at the 0.5 eV threshold by ×1.164 in width. |
| **B — named, not taken.** Report the moment-corrected width as central. | The physically better width: `<p_x²>` is governed by the **arithmetic** VDOS mean, not the harmonic one. | Puts every reported fractional width **above** its ROADMAP band, raises the 0.5 eV quadrature to **27.19 % / 26.20 %** against a quoted 22–26 %, and silently contradicts §J without amending it. |

The choice is a *reporting* choice, and it is labelled as one in every artifact header. The
column name is `dRdErec_upper_width_onesided`: **"upper" refers to the WIDTH, not the rate.**
A wider kernel moves *more* mass off the bottom of the axis, so in the bottom decade this
column sits **below** the central curve. Measured:

| | central (ω̄ locked) | upper width (ω̄_p) |
|---|---|---|
| leaked below the floor | 0.043328 % | **0.052580 %** |
| leaked at `T < 0` | 0.000567 % | **0.001753 %** |
| total reconstructed counts | 118.730004 | 118.718991 |

Bin by bin the two curves **cross**, because the reconstructed axis is coarse relative to the
deposit axis in the bottom decade and the deposit→`E_rec` mapping is not monotone. The
tested statement is therefore the integral one — the upper-width variant leaks more and
carries fewer counts — not a bin-by-bin ordering that does not hold. The figure shades
between the two curves rather than clipping the band to one side.

---

## 7. The bottom-bin caveat block (travels in every artifact header)

- **48.98 %** of the 100 meV bin's kernel falls **below** the 0.0999350 eV grid floor, and
  **0.87 %** lands at unphysical `T < 0`. Accounted and reported; **never renormalized**.
- The shipped kernel is a **symmetric** Gaussian against a true lineshape with **skewness
  0.590** and excess kurtosis 0.381, and **`2W` is only 5.60** at the floor — the impulse
  approximation is satisfied, but not comfortably. **Do not quote the 100 meV bin to better
  than one significant figure.**
- **Model-specific licence.** Multiplying `R(E_rec|E_dep)` by the trigger curve is licensed
  **only for this yield model**. Phase 10 measured `P(no counts registered)` = 2.0 × 10⁻⁴ at
  0.1 eV and **exactly 0** at 0.5 and 1 eV, against `1 − P_trig` of 0.998 / 0.512 / 0.056 — so
  the two do not double-count. But that follows from a **linear** yield assigning 0.018
  quasiparticles to a sensor holding 6.89 µeV against a ~190 µeV gap. **A threshold yield
  model would invert the verdict** and the two *would* then double-count.
- The Phase-10 counting floor is a **best case with no noise sources**, not a resolution
  model; this project has **no resolution parameter at all** (`fp-poisson-as-resolution`).
- **`k` is fixed by no project artifact.** Every sub-eV number ships with its `k`-sensitivity
  over [1, 12].

`test_caveats_in_headers` greps every emitted artifact for each of these. A caveat that lives
only in this report does not travel with the data.

---

## 8. Plan 12-01's results, cited as annotations on these spectra

These are **annotations**, not re-derivations. Plan 12-01 owns them.

- **Truncation bound (CALC-17):** at the 0.0999350 eV axis floor, **0.8027 %** of `dR/dT` is
  missing because the frozen flux table stops at 100 keV — an additive one-sided band of
  **19.018 counts/kg/day/keV** on `dR/dT`. It falls to 0.3825 % at 0.15 eV and is **exactly
  zero** above 0.3067 eV. The flat continuation was *shown* conservative from the frozen
  table's own slope (`d log Φ/d log E` = +0.0635…+0.0763 across its lowest knots). **The flux
  table was not extended.**
- **Analytic `T→0` plateau (VALD-10):** **2372.3683** counts/kg/day/keV, computed
  independently of the fold from `∫Φ = 7.495760 × 10¹²`. The unbroadened `dR/dT` sits
  **0.93 %** below it at the axis floor, approaching monotonically from below, neither rising
  nor collapsing.
- **ROADMAP SC2's flatness clause is SUPERSEDED BY MEASUREMENT** (44.30 % deficit at 10 eV).
  It is not a defect: `E_min(T) ∝ √T` cuts low-energy flux out of the fold as `T` rises.

Note that the *broadened, folded* `dR/dE_rec` reported here does **not** approach that plateau
at the bottom of the axis — it peaks near 0.2–0.3 eV and falls below it. That is the kernel
carrying ~49 % of the bottom bin off the axis plus the response mapping, and it is exactly
why the plateau gate was run on the **unbroadened recoil** spectrum in plan 12-01, before any
of this.

---

## 9. Checkpoint record (Task 3, `checkpoint:human-verify`)

**Status: recorded, NOT approved.** The user issued a standing session-level directive
(2026-07-22) to run the roadmap to completion without per-phase discussion unless a genuine
blocker arises. No blocker arose. The checkpoint content is recorded here in full and
execution continued. **No approval was given and none is recorded.** Resume-signal idiom that
*would* have been presented: `[Y/n/e]` (Enter = Y).

**One-line summary presented:** `dR/dE_rec` exists for both designs from 100 meV at the
paper's own normalization with broadening applied once before the response chain and the
trigger composed on top of ε; counts close to 5.6 × 10⁻⁵ on retained + leaked while the
retained-only sum deliberately misses by 4.9 × 10⁻⁴; and the `k`-sensitivity turns out to be
~5.7 %, about a quarter of the combined IA-width/counting-floor smearing, so the unmeasured
device parameter does **not** dominate the sub-eV observable.

**Review question put to the researcher (unanswered):**

> *"The central sub-eV width sits on the locked harmonic ω̄; the physically correct
> arithmetic-mean width is ×1.164 larger and ships as a one-sided upper band. Keeping it as a
> band preserves CONVENTIONS §J exactly but means the central curve knowingly understates the
> smearing at the 0.5 eV threshold. Is the band the right home for it, or should Phase 12
> report the moment-corrected width as central and amend §J?"*

**Three items flagged for attention:**

1. **The 100 meV bin is a statement about roughly half a kernel.** 48.98 % of it falls below
   the grid floor and 0.87 % at unphysical `T < 0`; the kernel is symmetric against a
   lineshape with skewness 0.590. One significant figure, and no more.
2. **The `k`-sensitivity result: `k` does not dominate** (5.67 % / 5.82 % against 24.77 % /
   23.68 % in quadrature) — but the dependence is non-monotonic, and the counting floor in
   that comparison is a noiseless best case, so the 24.8 % is a floor rather than an estimate.
3. **The licence to multiply `R` by `P_trig` is model-specific** and would invert under a
   threshold yield model. It rests on a linear yield assigning 0.018 quasiparticles to a
   sensor holding 6.89 µeV against a ~190 µeV gap.

**A fourth item, added by execution rather than by the plan:** the ε-perturbation leg of the
composition proof **could not be run as literally specified** (frozen `R`, so it would be
vacuous) and was reformulated. See §4.

---

## 10. Standing caveats carried out of this plan

- **The discretized convolution in the bottom decade remains directly untested.** Phase 11's
  v1.0 regression tests the high-energy end only; this plan folds the bottom decade through a
  response matrix on top of that. Plan 12-03's regression is also above 10 eV and therefore
  does not reach it either.
- **The counting floor and the IA width are assumed statistically independent** when
  quadratured. Inherited from Phase 11 as an assertion, never validated.
- **ε ≈ 0.5 is a lumped deposited-to-signal efficiency derived for a fully developed phonon
  cascade**, and CONVENTIONS §I's own rationale says it is not defensible at a
  ~3-optical-phonon deposit. That is *why* the reported observable changes below 1 eV — but ε
  still sits inside the un-triggered quantity `P_trig` multiplies.
- **The whole width rests on plan 11-01's ω̄ entering under a square root:** a factor-2 error
  there is a factor-1.41 error in every broadened number here.
- **A well-behaved-looking spectrum down to 100 meV is also what a kernel that is too narrow
  everywhere would produce.** What separates those is the strict amplitude-linearity test and
  the required *miss* of the retained-only sum, both of which are asserted here.
