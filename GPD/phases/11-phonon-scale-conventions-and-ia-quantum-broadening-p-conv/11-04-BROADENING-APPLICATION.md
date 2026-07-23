# 11-04 — Applying the IA broadening before the response chain

**Plan:** 11-04 (CALC-15 / ROADMAP SC4) · **Deliverable:** `deliv-application-note` · 2026-07-23
**Reproduce:**

```bash
/opt/anaconda3/bin/python3 scripts/make_broadened_cevns.py
/opt/anaconda3/bin/python3 -m pytest tests/test_ia_broadening.py -q
```

---

## 1. Where the convolution sits, and why the ordering is not cosmetic

The kernel is applied to `dR/dT` on the **nuclear-recoil** axis inside
`fold.rebin_cevns_to_edep_grid`, at the top of the function, **before every `rebin_counts` call** and
therefore before the deposited-energy grid and before `R(E_rec|E_dep)`:

```
read_cevns  →  ia_broadening.broaden_native_spectrum   ←  HERE
            →  rebin_counts(T, y, E_dep_edges_eV)
            →  dR/dE_dep  →  R(E_rec|E_dep)  →  reconstructed spectra
```

The IA width is a property of the **nucleus**, not of the sensor. Applying it to `E_rec`, to
`E_dep`, or folding it into `R` would double-count the response and mislabel a nuclear effect as a
detector effect (`fp-broadening-after-response`).

**The ordering is measurably real.** Broaden-then-rebin and rebin-then-broaden give numerically
different answers on the v1.0 deposit grid — asserted in `test_order_of_operations`, which fails if
they ever agree. They differ because the deposit grid is coarser than the native recoil knots near
the floor, so convolving after binning discretizes the kernel differently.

**Switch and recorded default.** `rebin_cevns_to_edep_grid(..., broaden=...)`, defaulting to
`ia_broadening.BROADENING_DEFAULT`.

> **RECORDED DEFAULT FOR PHASE 12: `BROADENING_DEFAULT = False` (OFF).**

Reasoning, and it is the Phase-10 precedent: Phase 10 left `shared_energy_grid` defaulting to
`v1.0` because a fail-safe default makes a silent change of physics impossible. The same argument
applies with more force here, because broadening changes the *values*, not just the axis. With the
switch off the function is **bit-identical** to v1.0 on every returned array
(`test_switch_off_bit_identical` checks `counts`, `counts_band`, `dRdEdep`, `dRdEdep_band` and
`low_counts` with `np.array_equal`). Turning it on is a deliberate Phase-12 act, not something every
existing call site inherits.

---

## 2. Conservation and the leakage budget — nothing was rescaled

Kernel: Gaussian of width `σ_E(T) = √(T·ω̄)` with the locked `ω̄ = 17.859677 meV`, applied to
**counts** (rate × bin width), so conservation is a sum and not a quadrature artefact. Each source
bin's redistribution is an exact CDF difference, so its mass telescopes to exactly 1 across
(below floor) ∪ (retained) ∪ (above top).

Axis: 480 log bins, extended-grid floor **0.0999350 eV** to 3200 eV.

| Quantity | Value | Fraction of input |
|---|---|---|
| input counts | 1.1878812499×10² counts/kg/day | 100 % |
| retained on the axis | 1.1873665658×10² | 99.956672 % |
| **leaked below the floor** | **5.1468407434×10⁻²** | **0.043328 %** |
| of which at **T < 0** (unphysical by construction) | 6.7385839820×10⁻⁴ | 0.000567 % |
| leaked above the top | 0 | 0 % |
| **residual, (retained + leaked)/input − 1** | **2.220×10⁻¹⁶** | target ≤ 10⁻³ — **PASS** |
| retained-only residual | **−4.332791×10⁻⁴** | **must MISS, and does** |

**Nothing was rescaled after the convolution.** The retained-grid sum deliberately falls short by
4.33×10⁻⁴; making it close would require manufacturing counts the physics does not produce. Strict
linearity in the input amplitude is asserted (`test_no_renormalization`): scaling the input by an
arbitrary constant scales every output bin and every leakage entry by exactly that constant, which
no global post-convolution rescale can satisfy.

**100.000 % of the sub-floor leakage comes from the bottom decade** (T < 1 eV), as it must: above
1 eV the Gaussian is many σ away from the floor.

### 2.1 Bottom bin, against plan 11-03's independent prediction

Bottom bin centre 0.1010208 eV, `σ_E = 0.042476 eV`:

| | measured by the shipped convolution | plan 11-03 analytic | ratio |
|---|---|---|---|
| fraction below the 0.0999350 eV floor | **0.489803** | 0.489803 | 1.00000 |
| fraction at T < 0 | **8.696083×10⁻³** | 8.696083×10⁻³ | 1.00000 |

Requirement was 10 %; the agreement is exact.

**How much credit this deserves — less than it looks.** Both paths evaluate the same matched-Gaussian
CDF, so exact agreement is expected and is *not* an independent confirmation of the physics. What it
does check, and check strictly, is that the shipped kernel is **centred at the right energy with the
right width**: a kernel misplaced by one bin or misscaled by the moment factor would change these
numbers by tens of percent. Read it as a placement check, not as corroboration.

**~49 % of a bottom-bin kernel falls off the retained axis.** That is the headline caveat for
Phase 12: any statement about the 100 meV bin is a statement about roughly half a kernel.

---

## 3. The v1.0 regression above 10 eV

With broadening ON, on the preserved v1.0 edge set:

| | |
|---|---|
| **maximum \|deviation\| above 10 eV** | **5.1963×10⁻⁴ = 0.052 %** — target < 1 %, **PASS** |
| non-vacuous? | yes: the deviation is ~5×10⁻⁴, not zero |
| trend, 20–200 eV (smooth region) | **slope −0.94** in log-log |
| sign change | **at 233.9 eV**; negative below, positive at *every* bin above 300 eV |
| naive global fit, 10 eV → top of axis | slope −0.31 — **contaminated, not the right statistic** |

### 3.1 Two corrections to the plan's stated expectation, both verified rather than assumed

**(a) The correct trend is steeper than `√(ω̄/E_R)`, not equal to it.** The plan asked that the
deviation fall as `√(ω̄/E_R)`, i.e. slope −0.5. But `√(ω̄/E_R)` is the fractional **width**, which is
a different quantity from the fractional change in the **spectrum**. For a mass-conserving kernel
with `σ² = ω̄E`, the second-moment (Fokker–Planck) expansion gives

    Δf = ½ d²/dE² [ σ²(E) f(E) ] = (ω̄/2) d²/dE² [ E f(E) ]   ⟹   Δf/f ∝ ω̄/E   (slope −1)

for a power-law spectrum. Measured: **−0.94** over 20–200 eV. The plan's −0.5 is satisfied *and
exceeded*; the test requires slope < −0.5 and additionally pins −0.94 ± 0.10, so a kernel that were
merely "small everywhere" would fail.

**(b) A single global power-law fit is the wrong statistic, and the reason is asserted, not
claimed.** The deviation **changes sign at 233.9 eV** and grows again toward the ~3.2 keV kinematic
endpoint, where the CEvNS spectrum cuts off and is not a power law at all — broadening moves mass
*past* the endpoint, so the sign of the curvature term flips. Fitting across the sign change
measures the sign change, not the broadening, and returns −0.31.

`test_v1_regression` asserts the sign structure directly: the median deviation below 200 eV is
negative and >90 % of those bins are negative, while **every** bin above 300 eV is positive. If that
structure ever fails, the justification for looking at the smooth region separately fails with it,
and the test fails.

**What this does not rule out.** The plan warned that "<1 % above 10 eV could also be produced by a
kernel that is too narrow everywhere". The −0.94 trend and the non-zero bottom-decade leakage
together make that unlikely, but neither is a direct measurement of the width. The width itself rests
on plan 11-01's ω̄ and enters under a square root.

---

## 4. Moment reconciliation — RECONCILED

Plans 11-02 and 11-03 were required to agree on which VDOS moment governs the width, or this plan
would be **blocked**. They agree, from genuinely different directions:

| | plan 11-02 | plan 11-03 | agree? |
|---|---|---|---|
| route | IA momentum distribution, `σ_E = qσ_p/m_N` with `σ_p² = m_N⟨ω⟩/2` | exact cumulants of the harmonic correlation function, `κ₂ = E_R⟨ω⟩` | — |
| governing mean | **arithmetic** ⟨ω⟩ = 24.195532 meV | **arithmetic** ⟨ω⟩ = 24.195532 meV | **yes** |
| σ at 100 meV | 49.189 meV | 49.189 meV | **yes, exactly** |
| correction over the locked ω̄ | **×1.163941** | **×1.163941** | **yes, exactly** |

**RECONCILED. Plan 11-04 is not blocked.**

Caveat on how independent this is: both compute the same arithmetic mean from the same frozen VDOS
table, so a VDOS-level error would move both together. What is independent is the **route**, not the
input.

**The systematic is carried as a band, never absorbed** (`fp-absorb-systematic`).
`cevns_dRdT_broadened.csv` ships `dRdT_broadened` (locked ω̄) **and** `dRdT_broadened_upper`
(arithmetic mean). It is **one-sided**: there is no lower band, because Cauchy–Schwarz forces
`ω̄_p ≥ ω̄_u`. The upper kernel leaks more: **0.052580 %** of the total below the floor against
0.043328 % for the central one, and the retained integrated counts differ by 9.3×10⁻⁵.

---

## 5. The rate is never multiplied by e^(−2W)

No path in `ia_broadening.py` or `fold.py` applies an `exp(−2W)`-like multiplicative factor to a
rate; a machine test greps for it. Positively: the integrated rate above 10 eV is **unchanged by
broadening to 1×10⁻³** (`test_no_dw_factor`). A suppression of ~10⁻² at 100 meV or ~10⁻²⁰ at 1 eV —
which is what `e^(−2W)` would deliver — is excluded by that measurement, not just by inspection.
Plan 11-03 quantifies why it would be wrong: `e^(−2W)` is the zero-phonon weight alone, and the
inelastic continuum it would discard carries **100 %** of the f-sum rule.

## 5.1 The domain guard is intact

`broaden_native_spectrum(..., require_floor_coverage=True)` **RAISES** when asked to broaden the
frozen v1.0 CEvNS table down to the 0.0999350 eV floor, because that table's support starts at 5 eV
and it carries no data below it. There is **no `try/except` returning zero, no `np.clip`, and no
extrapolation** on the broadening path — both asserted by `test_domain_guard`. Defeating the guard
would also make the leakage silently vanish and would defeat the conservation check with it.

The sub-eV spectrum is instead **recomputed** from `cevns.differential_rate`, which is a
recomputation of the same physics on a wider axis, not an extension of a frozen artifact
(`fp-silent-carry`).

### 5.2 One numerical fix to `fold.py`, recorded

`_loglog_segment_integral` acquired a finiteness fallback. A power law cannot represent a **Gaussian**
tail: past the ~3.2 keV kinematic endpoint the broadened rate falls super-exponentially, giving
`|p| ≈ 400`, so `T1**p` underflows, `A` becomes `inf`, and `inf × 0` becomes `nan`. When the result
is not finite the function now falls back to the same linear rule it already used for non-positive
endpoints. It is unreachable for every segment of the unbroadened v1.0 table — switch-off
bit-identity is tested and passes — so no existing number moved.

---

## 6. Bottom-bin caveats inherited from plan 11-03

**The 100 meV point is the least reliable number in the milestone.** Concretely, and all of it
applies to that one bin:

| | |
|---|---|
| `2W` | 5.60 — the IA criterion is met by a factor 5.6, not comfortably |
| exact fractional width of the true `S(q,ω)` | **49.19 %** — half its own mean |
| **skewness** | **0.590** (a Gaussian has 0); `= 1.39718/√(2W)` exactly |
| excess kurtosis | 0.381 (a Gaussian has 0) |
| Gaussian weight at unphysical `T < 0` | **0.87 %** measured here, 0.90 % predicted |
| Gaussian mass falling off the retained axis | **≈ 49 %** |

The shipped kernel is a **symmetric** Gaussian; the true `S` is skewed toward **high** energy
transfer. So the shipped bottom bin has too little weight on the high side and too much on the low
side, and about half of it is off the axis. Plan 11-03's verdict stands: *the impulse approximation
at 100 meV is supported at the order-of-magnitude level, not at the ~20 % level.* Phases 12–16 must
carry `skewness = 0.590` as the O(1/2W) caveat on every 100 meV number, and should not quote the
bottom bin to better than one significant figure.

---

## 7. ROADMAP Phase 11 SC1–SC5, clause by clause

| SC | Clause | Verdict |
|---|---|---|
| **SC1** | ω̄ and ⟨u_x²⟩ pinned from the **real Ge VDOS**, not the Debye model | **PASS** — 17.8597 meV, 1.6096×10⁻³ Å² |
| SC1 | `2W = q²⟨u_x²⟩` locked; `q²⟨u²⟩/3` explicitly rejected | **PASS** — CONVENTIONS §J, machine-parsed |
| SC1 | `B = 8π²⟨u_x²⟩` quoted alongside | **PASS** — 0.12709 Å² |
| SC1 | one number / one convention / one citation, no range | **PASS** |
| **SC2** | VDOS ceiling 37.79 meV | **PASS** — 37.78966 meV |
| SC2 | VDOS ⟨u_x²⟩ within ~1.5× of the Debye 1.34×10⁻³ Å² | **PASS** — ratio 1.2030 |
| SC2 | 2W(100 meV) in 4.7–8.3 | **PASS** — 5.5992, untuned |
| SC2 | "consistent with the independent momentum-transfer route q = 116 keV/c = 58.9 Å⁻¹" | **PASS as a UNITS IDENTITY, and the clause is SUPERSEDED as evidence.** 116.383 keV/c = 58.980 Å⁻¹ reproduced, but `2W = q²⟨u_x²⟩` and `2W = E_R/ω̄` are the same expression; the route is not independent (`fp-q-route-as-independent`) |
| **SC3** | `σ_E = √(E_R ω̄)` re-derived in-phase | **PASS** — from the IA momentum distribution, `⟨ω⟩ = E_R` exact, `m_N` cancelling |
| SC3 | `σ_E/E_R = 1/√(2W)` reproduced | **PASS as an IDENTITY, superseded as evidence** — true by construction for any ω̄ |
| SC3 | 35–46 % at 100 meV | **PASS** — 42.261 % |
| SC3 | 15.5–20.5 % at 0.5 eV | **PASS** — 18.900 % |
| SC3 | 11–15 % at 1 eV | **PASS** — 13.364 % |
| SC3 | 1.1–1.5 % at 100 eV | **PASS** — 1.336 % |
| SC3 | quadrature with the Phase-10 counting floor ≈ 22–26 % at 0.5 eV | **PASS** — 24.769 % (Ta→Al), 23.682 % (Al→Hf); floor is a **best case with no noise sources** |
| SC3 | *(new)* moment-corrected widths | **SUPERSEDED UPWARD** — with the physically correct arithmetic mean every width exceeds the upper edge of its band (49.19 / 22.00 / 15.56 / 1.555 %) and the 0.5 eV quadrature becomes 27.19 % / 26.20 %, above 22–26 % |
| **SC4** | convolution applied to `dR/dE_R` **before** the response chain | **PASS** — upstream of `rebin_cevns_to_edep_grid`, ordering shown to matter |
| SC4 | counts conserved to ≤10⁻³ | **PASS** — residual 2.220×10⁻¹⁶ on retained + leaked; retained-only misses by 4.33×10⁻⁴, as it must |
| SC4 | vanishes correctly: v1.0 reproduced above ~10 eV to <1 % | **PASS** — 0.052 % max, falling as E^(−0.94) in the smooth region |
| SC4 | *(plan clause)* deviation falls as `√(ω̄/E_R)` | **SUPERSEDED** — the correct leading order is `ω̄/E_R` (slope −1); measured −0.94, i.e. steeper than asked. A single global fit gives −0.31 and is contaminated by the 233.9 eV sign change and the 3.2 keV endpoint |
| **SC5** | f-sum rule demonstrates `S(q,ω) → δ(ω − q²/2M)` | **PASS** — zeroth moment ≤2.1×10⁻⁷, f-sum rule ≤1.9×10⁻⁸ at all five q |
| SC5 | residual O(1/2W) quantified in the bottom bin | **PASS** — skewness 0.590, excess kurtosis 0.381, 1/2W = 0.179 |
| SC5 | "the IA is reached by ~100 meV" | **QUALIFIED PASS — order-of-magnitude only.** The bottom-bin width is 49 % of its own mean with O(1) skewness. Not upgraded (`fp-ia-overclaim`) |
| SC5 | why the rate is never multiplied by `e^(−2W)` | **PASS** — zero-phonon weight only; the inelastic continuum carries 100 % of the f-sum rule; would discard 99.63 % at 100 meV |
| SC5 | *(clause)* `e^(−2W)` reproduces the survey ~10⁻² at 100 meV and ~10⁻²⁰ at 1 eV | **PARTIAL — 100 meV PASS (3.70×10⁻³, factor 2.7), 1 eV FAIL (4.82×10⁻²⁵ vs ~10⁻²⁰).** Explained and tested: the survey used the Debye ω̄ ≈ 21.5 meV. Reported, not absorbed. No conclusion changes |
| SC5 | bounded, "without becoming a milestone pillar" | **PASS** — five q values, one FFT each, no tracked artifact, no coherent backbone |

**Superseded targets are marked superseded, not passed and not failed.** Three of them: the q-route
as independent evidence (SC2), the `1/√(2W)` identity as evidence (SC3), and the `√(ω̄/E_R)`
regression trend (SC4). One clause is a genuine partial: the 1 eV `e^(−2W)` magnitude.

The survey band **ω̄ = 12–21 meV survived**: the measured value 17.860 meV is inside it. Read with
care — the Debye value is 21.486 meV, essentially the band's top, so "inside the band" partly
restates "within 1.2× of Debye".

---

## 8. Review question

> Phase 11 has applied IA quantum broadening before the response chain. **Conservation residual
> 2.220×10⁻¹⁶** against a ≤10⁻³ target, with **48.98 % of the bottom-bin mass leaked below the axis
> floor** and **0.87 % placed at T < 0** — matching plan 11-03's independent analytic prediction
> exactly, and never rescaled away. The **v1.0 regression above 10 eV is 0.052 %**, falling as
> **E^(−0.94)** in the smooth region (the plan expected E^(−0.5); the correct leading order is
> E^(−1), and a naive global fit gives −0.31 because the deviation changes sign at 233.9 eV near the
> kinematic endpoint). The locked **ω̄ is 17.8597 meV, INSIDE** the survey's 12–21 meV band. The
> broadening switch **defaults OFF**, fail-safe, for Phase 12 to turn on deliberately.
>
> **Three things to look at before approving:**
> 1. **The 100 meV bin is the least reliable number in the milestone.** True width 49 % of its own
>    mean, skewness 0.590, ~49 % of its kernel off the axis, and the shipped kernel is symmetric
>    while the true lineshape is not.
> 2. **The moment systematic is one-sided and pushes every SC3 width ABOVE its ROADMAP band.** The
>    central curve uses the locked (harmonic) ω̄ so the stated identities hold; the physically correct
>    arithmetic mean is ×1.1639 wider and is shipped as an upper band, not absorbed.
> 3. **Three SC clauses are SUPERSEDED, not passed:** the q-route and the `1/√(2W)` relation are
>    algebraic identities rather than evidence, and the `√(ω̄/E_R)` regression trend was the wrong
>    functional form.
>
> Approve the phase as complete and hand the broadening to Phase 12? **[Y/n/e]** (Enter = Y)

**Checkpoint disposition.** This plan is marked `interactive: true` and Task 3 is a
`checkpoint:human-verify`. Under the standing session directive to run the roadmap to completion
without per-step discussion, the checkpoint content is recorded here in full and execution
continued. No approval has been recorded; the question above stands open for the researcher.

---

## 9. Files

| File | Role |
|---|---|
| `src/qpd_potential/ia_broadening.py` | `broaden_counts`, `native_edges`, `broaden_native_spectrum`, `BROADENING_DEFAULT` |
| `src/qpd_potential/fold.py` | the wiring, upstream of `rebin_counts`; the `_loglog_segment_integral` finiteness fallback |
| `tests/test_ia_broadening.py` | 24 checks, 11 of them written before the implementation existed |
| `artifacts/v2.0/cevns_dRdT_broadened.csv` | 480-bin broadened recoil spectrum with the one-sided upper band |
| `artifacts/v2.0/ia_broadening_leakage_budget.csv` | per-bin conservation budget |
| `scripts/make_broadened_cevns.py` | the generator |
