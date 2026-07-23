# Plan 10-02 --- Trigger-Curve Derivation

**Phase:** 10 --- Sub-eV Grid Extension and the Trigger Observable (P-GRID)
**Discharges:** claim `claim-e50`, proof deliverable `deliv-e50-derivation`.
**Advances:** ROADMAP Phase 10 success criterion 4; requirement CALC-16.

---

## 0. What is anchored and what is chosen

| Object | Status |
|---|---|
| The 50% point at **E50 = 0.5 eV** | **Decided.** USER DECISION 2026-07-22, `GPD/STATE.md` Accumulated Context. |
| The functional form (Hill / log-energy logistic) | **Chosen**, on the grounds derived in Section 4. |
| The sharpness **k** | **Fixed by no measurement and no project artifact.** Exposed as `params.TRIGGER_SHARPNESS`, default 4.0, declared scan range [1, 12]. |
| Whether the trigger acts on deposited energy at all | **Assumed.** See Section 6. |

**No trigger threshold has ever been measured for this device.** Only E50 carries a project
decision behind it. Everything else in this note is a construction chosen so that E50 is the
*only* thing a downstream result can inherit without a sensitivity scan.

---

## 1. Declared parameters and their domains

| Symbol | Domain | Aliases | Where it lives |
|---|---|---|---|
| `E` | positive real, deposited energy in eV (the CONVENTIONS A.1 deposited-energy scale, **not** reconstructed energy) | `E_dep`, `E_dep_eV` | the abscissa of the curve |
| `E50` | positive real, **fixed at 0.5 eV** | `TRIGGER_E50`, `e50_eV` | `params.TRIGGER_E50`; never a literal at the call site |
| `k` | positive real, **dimensionless** sharpness, exposed and scannable | `sharpness`, `TRIGGER_SHARPNESS` | `params.TRIGGER_SHARPNESS`, range `params.TRIGGER_SHARPNESS_RANGE` |

Dimensional check: `E` and `E50` both carry [energy] = eV, so `E50/E` is dimensionless,
`(E50/E)^k` is dimensionless for dimensionless `k`, and `P` is dimensionless in [0, 1].
Raising a dimensionful quantity to a non-integer power never occurs.

## 2. Hypotheses

- **`hyp-positive-k`** --- `k > 0`. **USED**, in every one of the three conclusions below:
  in `concl-e50-exact` only through `1^k = 1` (which actually holds for all real `k`), in
  `concl-zero-limit` and `concl-unit-limit` essentially, since `k < 0` reverses both limits
  and `k = 0` gives the constant `P == 1/2`.
- **`hyp-positive-e50`** --- `E50 > 0`, and `E50 = 0.5 eV` by the locked user decision.
  **USED**: `E50 > 0` is what makes `log E50` finite and the ratio `E50/E` positive, so the
  real power `(E50/E)^k` is defined. The specific value 0.5 eV is **not** used anywhere in
  the derivation --- that is the point of `concl-e50-exact`.
- **`hyp-hill-form`** --- `P(E) = 1 / (1 + (E50/E)^k)` for `E > 0`, with `P(0) := 0` by
  continuity. **USED** as the definition throughout.

## 3. The three conclusion clauses

### `concl-e50-exact` --- `P(E50) = 1/2` exactly, independent of `k`

Substitute `E = E50` into the Hill form. The ratio becomes `E50/E50 = 1`, so

```
P(E50) = 1 / (1 + (E50/E50)^k) = 1/(1 + 1^k) = 1/(1 + 1) = 1/2
```

**Where the k-independence enters:** at `1^k = 1`, which holds for every real `k`. `k` never
reaches the arithmetic. The 50% point is therefore a property of the FUNCTIONAL FORM, not a
consequence of any particular width, and not something that could be tuned into place.

This is the whole reason the Hill form was adopted rather than fitted. A form whose 50% point
landed at 0.5 eV only for one particular width would put the constraint on the width rather
than on the curve, and it would break silently the first time the width was scanned
(`fp-e50-by-tuning`).

Verified numerically for 46 values of `k` spanning the declared range [1, 12] plus the
default, each to `|P - 1/2| < 1e-12`
(`tests/test_trigger_efficiency.py::test_e50_invariance_across_the_whole_scan_range`).

### `concl-zero-limit` --- `P(E) -> 0` as `E -> 0+`, and `P(0) = 0`

For `E -> 0+` with `E50 > 0` and `k > 0`, the ratio `E50/E -> +inf`, hence
`(E50/E)^k -> +inf`, hence

```
P(E) = 1 / (1 + (E50/E)^k) -> 1/(1 + inf) = 0
```

More precisely, `P(E) ~ (E/E50)^k` as `E -> 0+`, so the approach is a power law of exponent
`k`. At `k = 4` and `E = 1e-6 eV` this gives `P = (2e-6)^4 = 1.6e-23`, which is the measured
value.

`P(0) = 0` is then the continuous extension, and it is implemented as an exact zero rather
than as the limit of a floating-point ratio.

### `concl-unit-limit` --- `P(E) -> 1` as `E -> inf`, and `P` is strictly increasing

For `E -> inf`, `E50/E -> 0+` and `(E50/E)^k -> 0`, so `P -> 1/(1 + 0) = 1`.

Monotonicity, by differentiation. Write `u(E) = (E50/E)^k = E50^k E^{-k}`, so
`du/dE = -k E50^k E^{-k-1} < 0` for `E > 0`, `k > 0`, `E50 > 0`. Then

```
dP/dE = -u'(E) / (1 + u)^2 = k E50^k E^{-k-1} / (1 + (E50/E)^k)^2   >   0
```

**Sign of dP/dE: strictly positive** for all `E > 0`. Every factor in the final expression is
positive: `k > 0` by `hyp-positive-k`, `E50^k > 0` by `hyp-positive-e50`, `E^{-k-1} > 0` for
`E > 0`, and the denominator is a square. The two minus signs cancel --- one from `du/dE`, one
from the quotient rule on `1/(1+u)` --- which is the only sign hazard in the derivation and
is the reason it is written out.

Verified on a 4001-point log grid from 1e-3 to 1e3 eV: strictly increasing, all values in
[0, 1].

---

## 4. The rejected alternative: a logistic in LINEAR energy

```
P_lin(E) = 1 / (1 + exp(-(E - E50)/w))
```

This form also puts its 50% point at `E = E50`, so on the headline constraint it looks
equally good. It fails on the zero limit:

```
P_lin(0) = 1 / (1 + exp(+E50/w))     >  0     for every finite w > 0
```

**Evaluated numerically at the width that would otherwise have been used**, `w = 0.1 eV`
(chosen to give a comparable turn-on sharpness to `k = 4`):

```
P_lin(0) = 1 / (1 + exp(0.5/0.1)) = 1 / (1 + e^5) = 1 / 149.4131591 = 6.692850924e-03
```

**A 0.67% probability of triggering on a deposit of exactly zero energy.** Worse, `P_lin` is
strictly positive at *negative* energy as well: `P_lin(-1 eV) = 1/(1 + e^{15}) = 3.06e-07`.

On an axis that spans four decades from 0.1 eV, a 0.67% floor at zero deposit is not a
rounding detail: it would sit underneath every sub-eV number this milestone produces, and it
would be a nonzero trigger rate for events that did not happen. That is why the Hill form was
adopted --- not as a stylistic preference (`fp-linear-sigmoid`).

The defect is pinned by
`tests/test_trigger_efficiency.py::test_linear_energy_logistic_fails_the_zero_limit`, which
asserts the exact number 6.692850924e-03 against the rejected form and 0.0 against the
adopted one. The rejected form is kept in `trigger.py` as
`linear_energy_logistic_rejected` for exactly that purpose and is never used as the project's
trigger curve.

---

## 5. What the sharpness does, and why it is exposed

At sharpness `k`, the 10%-to-90% rise spans a factor of `81^{1/k}` in deposited energy:

```
P = 0.1  =>  (E50/E)^k = 9   =>  E = E50 * 9^{-1/k}
P = 0.9  =>  (E50/E)^k = 1/9 =>  E = E50 * 9^{+1/k}
ratio    =  81^{1/k}
```

| k | 10-90% span factor | 10-90% range at E50 = 0.5 eV |
|---|---|---|
| 1 | 81.0 | 0.056 -- 4.5 eV |
| 2 | 9.00 | 0.167 -- 1.50 eV |
| **4 (default)** | **3.00** | **0.167 -- 1.50 eV**, i.e. 0.5/3 to 0.5x3 |
| 8 | 1.732 | 0.289 -- 0.866 eV |
| 12 | 1.520 | 0.329 -- 0.760 eV |

The default `k = 4` was chosen because a turn-on spanning a factor of three in deposited
energy looks like a plausible detector threshold. **"Looks plausible" is the entire
justification, and it is not a measurement.** That is why `k` is registered with confidence
`LOW`, carries a declared scan range, and is never written as a literal inside the sigmoid: a
buried width would be a fabricated device property that every downstream sub-eV result would
inherit without being able to test its sensitivity to it (`fp-hardcoded-width`).

**Every downstream result computed with this curve must be reported together with its
sensitivity to k.** Nothing in this project constrains it.

---

## 6. Weakest points of this construction

1. **Only E50 is anchored.** The form and the width are chosen. A reader is entitled to treat
   the entire curve except its 50% point as a placeholder.
2. **eps ~= 0.5 is itself an imposed forward-model definition** (CONVENTIONS Section E), not a
   derived quantity, and the paper's own physical estimate is `eta_ce ~= 0.3`. The composition
   test proves the trigger curve *multiplies* eps; it does not make eps right.
3. **The composed chain treats the trigger as a function of DEPOSITED energy.** If the real
   trigger acts on the reconstructed *count* instead --- which for a counting detector is the
   more natural readout-level statement --- then the composition point is wrong even though
   the factorisation test passes. The factorisation test cannot detect this.
4. **A single scalar trigger probability, with no dependence on event position on the wafer or
   on which sensors fire,** is assumed adequate at 0.5 eV, where the deposit is a few
   optical-phonon quanta and the on-spot / off-spot split (`f_prompt`, `r`, both LOW
   confidence) governs which sensors see anything at all.
5. **The response matrix already assigns finite probability to "no counts registered".**
   Phases 12 and 15 will multiply that by `1 - P_trig`. Whether that double-counts
   non-detection is answered with numbers in plan 10-04, not here.
