# 11-03 — Impulse-limit justification (ROADMAP SC5)

> **This is a BOUNDED artifact and NOT A MILESTONE PILLAR.** ROADMAP SC5 requires the impulse-limit
> justification be a one-off demonstration, and the milestone-wide accuracy expectation was
> explicitly lowered on 2026-07-22. Scope: five recoil energies, one FFT each, no coherent-crystal
> `S(q,ω)` backbone, no phonon-order multiphonon expansion.

**Plan:** 11-03 · **Deliverables:** `deliv-impulse-module`, `deliv-moments-table`, `deliv-justification`
**Reproduce:** `/opt/anaconda3/bin/python3 -m pytest tests/test_impulse_limit.py -q`

---

## 1. Method

Harmonic **incoherent** (self) response by the T→0 cumulant route:

    γ(t) = (ħ²q²/2m_N) ∫ g(ω)/ω · e^(−iωt) dω          (T→0, n_B = 0)
    2W   = γ(0) = q²⟨u_x²⟩                              ← ties back to CONVENTIONS.md §J
    S(q,ω) = (1/2π) ∫ e^(+iωt) exp(−2W + γ(t)) dt

Sign convention fixed by requiring the one-phonon term at **positive** energy transfer: expanding
`exp(γ) ≈ 1 + γ` gives `S₁(ω) = e^(−2W) E_R g(ω)/ω` for ω > 0, and the zero-phonon term gives
`e^(−2W)δ(ω)`. Using `e^(−iωt)` instead would place the one-phonon line at negative ω.

**Every constant cancels.** With `q² = 2m_N E_R`, `ħ²q²/(2m_N) = E_R` exactly, so

    γ(t) = E_R ∫ g(ω)/ω · e^(−iωt) dω        and        2W = E_R/ω̄_u

The harmonic S is fixed by E_R and the VDOS alone — no mass, no ħ survives. This is also why 2W and
every shape parameter below are **mass-free**, consistent with plan 11-01.

### 1.1 Exact cumulants — the analytic backbone

`ln F = −2W + γ(t)`, and with `F(t) = ⟨e^(−iωt)⟩` the cumulants are `κ_n = iⁿ γ^(n)(0)`. Since
`γ^(n)(0) = E_R ∫ (g/ω)(−iω)ⁿ dω = E_R (−i)ⁿ ⟨ω^(n−1)⟩` and `(−i)ⁿ iⁿ = 1`:

    **κ_n = E_R · ⟨ω^(n−1)⟩_g   for every n ≥ 1**, exactly, for the FULL S including the elastic line

| n | κ_n | value |
|---|---|---|
| 1 | E_R ⟨ω⁰⟩ = **E_R** | the f-sum rule — exact for any interaction |
| 2 | E_R ⟨ω⟩ = **E_R · ω̄_p** | the **ARITHMETIC** VDOS mean, not the locked harmonic one |
| 3 | E_R ⟨ω²⟩ | skewness = ⟨ω²⟩/(√E_R ⟨ω⟩^{3/2}) ∝ 1/√(2W) |
| 4 | E_R ⟨ω³⟩ | excess kurtosis ∝ 1/(2W) |

Frozen-VDOS moments: `⟨1/ω⟩ = 55.99205 eV⁻¹`, `⟨ω⟩ = 24.195532 meV`, `⟨ω²⟩ = 7.027393×10⁻⁴ eV²`,
`⟨ω³⟩ = 2.231237×10⁻⁵ eV³`.

The numerical FFT below is therefore a **check on these closed forms**, not the only route — which
is also the analytic-moment fallback the plan required be available.

### 1.2 Two analytic subtractions before the transform (still one FFT)

Whatever `F(t)` fails to decay to becomes ringing across the *entire* ω grid, and the third moment —
which weights by `(ω − E_R)³` out to several eV — is dominated by that ringing rather than by
physics. Both non-decaying pieces are removed in closed form:

* **Zero-phonon:** `F(t) → e^(−2W)` as t → ∞. Carried as a delta at ω = 0.
* **One-phonon:** the remainder still behaves as `e^(−2W)γ(t)`, and γ decays only as a power law
  because the VDOS has hard edges. But that piece transforms *exactly* to `e^(−2W) E_R g(ω)/ω`,
  which has compact support on the VDOS band, and is added back on the ω grid.

What is transformed is `e^(−2W)(e^γ − 1 − γ) ~ e^(−2W)γ²/2` — four orders of magnitude smaller at
the truncation point. **This was not cosmetic:** before the one-phonon subtraction the 100 meV
skewness came out anywhere between −2.8 and +0.7 depending on grid parameters, and did not converge.
Afterwards it converges to 0.590457 against the exact 0.590461.

---

## Moments

Five recoil energies. `m₀`, `m₁`, `κ₂` and skewness columns are the **numerical FFT** values;
"exact" columns are the closed-form cumulants. Convergence ladder: 60 → 240 → 960 → 3840 points per
σ, stopping when `|m₀ − 1| < 10⁻⁶`. Only the bottom bin needed the last rung.

| E_R | q [Å⁻¹] | q [keV/c] | 2W | e^(−2W) | m₀ − 1 | m₁/E_R − 1 | κ₂/(E_R⟨ω⟩) − 1 | skewness (num) | skewness (exact) | 1/√(2W) | skew·√(2W) | excess kurtosis | σ_exact/E_R | pts/σ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **0.1 eV** | 58.980 | 116.383 | **5.599205** | **3.7008×10⁻³** | +2.1×10⁻⁷ | +1.9×10⁻⁸ | +5.1×10⁻⁷ | **0.590457** | **0.590461** | 0.422607 | 1.3972 | 0.381132 | **49.189 %** | 3840 |
| 0.5 eV | 131.882 | 260.239 | 27.996027 | 6.9419×10⁻¹³ | −1.7×10⁻¹² | −8.7×10⁻¹³ | −4.9×10⁻¹¹ | 0.264062 | 0.264062 | 0.188996 | 1.3972 | 0.076226 | 21.998 % | 60 |
| 1 eV | 186.510 | 368.034 | 55.992054 | 4.8190×10⁻²⁵ | −9.9×10⁻¹⁵ | +2.0×10⁻¹⁵ | +1.3×10⁻¹² | 0.186720 | 0.186720 | 0.133640 | 1.3972 | 0.038113 | 15.555 % | 60 |
| 10 eV | 589.796 | 1163.826 | 559.920539 | 6.75×10⁻²⁴⁴ | −4.7×10⁻¹⁴ | −2.4×10⁻¹⁵ | +4.3×10⁻¹¹ | 0.059046 | 0.059046 | 0.042261 | 1.3972 | 0.003811 | 4.919 % | 60 |
| 100 eV | 1865.098 | 3680.341 | 5599.205393 | 0 (underflow; ≈10⁻²⁴³²) | −3.4×10⁻¹³ | −3.0×10⁻¹³ | −4.8×10⁻¹⁰ | 0.018672 | 0.018672 | 0.013364 | 1.3972 | 0.000381 | 1.556 % | 60 |

**Matched-Gaussian off-grid weights** (centred at 100 meV):

| Gaussian | σ | weight at ω < 0 | weight below the 0.0999350 eV grid floor | E_R/σ |
|---|---|---|---|---|
| locked ω̄, centred 0.1 eV | 42.261 meV | **0.898 %** | **49.939 %** | 2.3663 |
| locked ω̄, centred at the first bin centre 0.1013838 eV | 42.552 meV | 0.860 % | **48.642 %** | 2.3826 |
| **true width √(E_R ω̄_p)**, centred 0.1 eV | 49.189 meV | **2.103 %** | 49.947 % | 2.0330 |

---

## 2. Sum rules — and the honest convergence verdict

| Check | Requirement | Result | Verdict |
|---|---|---|---|
| Zeroth moment `∫S dω = 1` | < 10⁻⁶ | 2.1×10⁻⁷ (100 meV) to 3.4×10⁻¹³ (100 eV) | **PASS at all five q** |
| f-sum rule `∫ωS dω = q²/2m_N` | < 10⁻⁴ rel. | 1.9×10⁻⁸ (100 meV) to 3.0×10⁻¹³ | **PASS at all five q** |
| `γ(0) = q²⟨u_x²⟩` (§J lock) | numerical tolerance | 7.3×10⁻¹² at every q | **PASS** |
| Second central moment vs `E_R ω̄_p` | < 10⁻³ rel. | 5.1×10⁻⁷ to 4.8×10⁻¹⁰ | **PASS** |

The f-sum rule holds for *any* interaction, so its passing at all five q is an implementation
verdict, not a physics one. The `γ(0) = 2W` reduction is the tie back to the Section J lock: two
independent quadratures over the same frozen VDOS agree to 7×10⁻¹², so the `S(q,ω)` route and the
`⟨u_x²⟩` route are computing the same thing.

### 2.1 Does S converge onto δ(ω − q²/2M)? — and how far is the bottom bin?

The exact fractional width `σ/E_R = √(ω̄_p/E_R)` falls as `1/√E_R` exactly, i.e. exactly as
`1/√(2W)`: 49.19 % → 21.998 % → 15.555 % → 4.919 % → 1.556 %. Monotone, with the ratio between
consecutive decades equal to √10 to 10⁻¹².

**Verdict, stated at the level the numbers support and no higher.** Convergence toward the
free-nucleus delta is demonstrated. But **"the impulse approximation is reached by ~100 meV" is
supported only at the ORDER-OF-MAGNITUDE level in the bottom bin, not at the ~20 % level.** At
E_R = 100 meV the harmonic S has

* fractional width **49.2 %** (not 42.3 % — that is the *locked-ω̄* Gaussian, which is the narrower,
  harmonic-mean version; the true harmonic S is wider),
* skewness **0.590**, where a Gaussian has 0,
* excess kurtosis **0.381**, where a Gaussian has 0,
* and 2W = 5.60, so `1/2W = 0.179`.

A distribution half as wide as its own mean, with an O(1) skewness, is not a delta function. It is
in the impulse *regime* — the free-recoil centroid is exact and the shape is single-peaked — but the
bottom bin remains the least reliable point in the milestone. Declaring the limit reached because
2W > 1 is `fp-ia-overclaim`, and this artifact does not do it.

---

## 3. The O(1/2W) residual in the bottom bin

**Skewness scales exactly as 1/√(2W)**, with a constant of proportionality fixed by the VDOS:

    skewness = [ ⟨ω²⟩ / (⟨ω⟩^{3/2} √ω̄_u) ] × 1/√(2W) = **1.39718 / √(2W)**

verified constant to 4 decimal places at all five energies. So the plan's expectation "skewness
scales as 1/√(2W) within a factor of a few" is met with the factor being 1.397, not merely of
order one.

**The number to carry forward: skewness = 0.590 at 100 meV** (excess kurtosis 0.381, 1/2W = 0.179).
That is the quantified `O(1/2W)` residual ROADMAP SC5 asks for, and it must travel as a caveat on
every 100 meV result in Phases 12–16. Practically: at 100 meV the symmetric Gaussian is good to
roughly the 20 % level in shape, not better, and the true S has more weight on the **high**-energy
side than the Gaussian does.

**What the symmetric Gaussian gets wrong, concretely.** The true T→0 S vanishes for ω < 0 — there
are no phonons to absorb at zero temperature — but the matched Gaussian centred at 100 meV puts
**0.898 %** of its weight there (2.103 % if matched to the true, wider σ). That weight is unphysical
by construction.

**Handed to plan 11-04:** the same Gaussian puts **49.9 %** of its weight below the extended-grid
floor 0.0999350 eV when centred at 100 meV, and **48.6 %** when centred at the first bin centre
0.1013838 eV. The floor sits essentially *at* the centre of the bottom bin, so roughly half of a
bottom-bin kernel falls off the retained grid. **A clean ≤10⁻³ count-conservation residual on the
retained grid would therefore be evidence of hidden renormalization, not of a correct convolution.**
Leaked mass must be non-zero and reported per bin.

---

## 4. Why the rate is NEVER multiplied by e^(−2W)

`lim_{t→∞} F(q,t) = e^(−2W)` by Riemann–Lebesgue on γ. So **e^(−2W) is the weight of the
zero-phonon (elastic) line at ω = 0 and nothing else.** The strength partition, computed not
asserted:

| E_R | zero-phonon `e^(−2W)` | one-phonon `2W·e^(−2W)` | multiphonon `1 − (1+2W)e^(−2W)` | elastic + inelastic |
|---|---|---|---|---|
| 100 meV | 0.370 % | 2.072 % | **97.558 %** | 1.000000 (to 2×10⁻⁶) |
| 0.5 eV | 6.9×10⁻¹¹ % | 1.9×10⁻⁹ % | ≈ 100 % | 1.000000 |
| 1 eV | 4.8×10⁻²³ % | 2.7×10⁻²¹ % | ≈ 100 % | 1.000000 |

And the elastic delta sits at ω = 0, so it contributes **exactly zero** to the first moment:
**the inelastic continuum alone carries the entire f-sum rule** `∫ωS dω = q²/2m_N`, verified
numerically to 10⁻⁸ or better at every q.

**Therefore:** multiplying the CEvNS rate by `e^(−2W)` would discard the continuum that carries
100 % of the energy-weighted strength — **99.63 % of the total weight at 100 meV and effectively all
of it at 1 eV (a suppression by 4.8×10⁻²⁵)**. That is erasing a real signal, not correcting one.
The strength does not disappear when the Debye–Waller factor gets small; it **moves into the
multiphonon continuum**, whose centroid is exactly `q²/2M`. Locked forbidden proxy
`fp-dw-rate-suppression`; a machine test asserts that no module in this phase applies `e^(−2W)` as a
multiplicative rate factor.

### 4.1 A disagreement with the survey magnitudes, reported not smoothed

`GPD/literature/COMPUTATIONAL.md` §3 quotes `e^(−2W) ≈ 10⁻²` at 100 meV and `≈ 10⁻²⁰` at 1 eV.

| E_R | survey | this phase | verdict |
|---|---|---|---|
| 100 meV | ~10⁻² | **3.70×10⁻³** | **agrees within a factor 2.7** |
| 1 eV | ~10⁻²⁰ | **4.82×10⁻²⁵** | **DOES NOT agree — 5 orders of magnitude low** |

The disagreement is fully explained and is not a bug: `e^(−2W)` is *exponentially* sensitive to ω̄.
The survey's 10⁻²⁰ corresponds to 2W ≈ 46, i.e. ω̄ ≈ 21.5 meV — the **Debye-model** value. Indeed
`exp(−1 eV / 21.5 meV) = 6.4×10⁻²¹ ≈ 10⁻²⁰`, reproduced by a test. The locked **measured** ω̄ =
17.86 meV gives 2W = 55.99 and `e^(−56) = 4.8×10⁻²⁵`. A 20 % shift in ω̄ is 4½ decades in `e^(−2W)`
at 1 eV.

"Within an order of magnitude" was never a well-posed acceptance criterion for an exponentially
sensitive quantity at 2W = 56, and this artifact records the miss rather than widening the tolerance
until it passes. **It changes no conclusion:** the coherent channel is extinct at 1 eV whether the
factor is 10⁻²⁰ or 10⁻²⁵.

---

## 5. What this artifact does NOT establish

1. **Sum rules constrain moments, not shape — they are necessary but nowhere near sufficient.** A
   completely wrong lineshape with the correct first four moments would pass every quantitative
   check in §2. The skewness and negative-energy-weight diagnostics exist precisely because the sum
   rules alone cannot detect that. This artifact establishes that the *moments* are right; it does
   not prove the lineshape is.
2. **The incoherent-only treatment is self-justified.** It is licensed by `e^(−2W)` being tiny in
   the window — but that smallness is computed *here*, from the same harmonic model. The argument is
   internally consistent, not externally validated.
3. **The harmonic approximation is inherited unchanged** from the `CONVENTIONS.md` §J lock and is
   not tested anywhere in this phase.
4. **No external benchmark exists.** There is no published Ge `S(q,ω)` at q = 59–1865 Å⁻¹ to compare
   against. The only external checks available are the sum rules, which are exact but weak.
5. **Nothing here is applied to the production spectrum.** This plan produces a bound and a caveat,
   not a corrected kernel. Plan 11-04 uses the symmetric Gaussian; the residual quantified above is
   the price of that choice, stated rather than removed.

---

## 6. Cross-check verdict for plan 11-02 — and for plan 11-04

**The decisive check: PASSED, confirming plan 11-02.**

The exact second central moment of the harmonic S is `E_R · ω̄_p` — the VDOS **arithmetic** mean —
reproduced numerically to 5×10⁻⁷ relative at 100 meV and to 5×10⁻¹⁰ at 100 eV. It is **not**
`E_R · ω̄_u`, which is 35.5 % smaller.

This is reached from an entirely different direction than plan 11-02: 11-02 argued from the
impulse-approximation momentum distribution `σ_E = q σ_p/m_N` with `σ_p² = m_N⟨ω⟩/2`; this plan
computed the cumulants of the harmonic correlation function. Both give the same answer.

| | plan 11-02 (momentum distribution) | plan 11-03 (correlation function) | agree? |
|---|---|---|---|
| governing mean | arithmetic ⟨ω⟩ | arithmetic ⟨ω⟩ | **yes** |
| width at 100 meV | 49.189 meV | 49.189 meV | **yes, exactly** |
| correction over locked ω̄ | ×1.163941 | ×1.163941 | **yes, exactly** |

**Plan 11-04 is NOT blocked** by a moment-route disagreement. It is, however, handed two binding
constraints: the ~49 % sub-floor leakage of §3, and the O(1/2W) shape caveat of §3 on every 100 meV
number.

---

## 7. Files

| File | Role |
|---|---|
| `src/qpd_potential/impulse_limit.py` | γ(t), exact cumulants, one FFT per q, elastic weight, Gaussian off-grid weights |
| `tests/test_impulse_limit.py` | 30 checks: the three exact sum rules at all five q, the second-moment cross-check, skewness scaling, off-grid weights, the e^(−2W) prohibition guard, and the bounded-scope guard |

No tracked `.csv`/`.npz` was added under `artifacts/v2.0/` by this plan; the Phase-10 disposition
register is untouched by it. Five rows do not warrant a tracked artifact.
