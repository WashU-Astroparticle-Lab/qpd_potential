# 12-01 — Sub-eV CEvNS Validity Gates (CALC-17 and the VALD-10 plateau leg)

**Phase:** 12 — Reactor CEvNS down to 100 meV at the Paper's Surface Scenario (P-SIG)
**Plan:** 12-01 (wave 1)
**Scope:** the **unbroadened recoil spectrum only**. No IA broadening, no response matrix,
no trigger curve, no `dR/dE_rec` — plan 12-02 owns all four.

**Normalization (primary and only):** frozen `data/flux/reactor_flux_v1.0.csv`,
3 GW_th at 25 m, surface, unshielded, used **unmodified**. `CONVENTIONS.md` §D stands
unchanged.

**Reproduction environment:** `/opt/anaconda3/bin/python3` — numpy 1.26.4, scipy 1.17.1,
pytest 7.4.0. No random seeds are involved: every number below is a deterministic
quadrature of frozen tables.

**Reproducing command for every number in this report:**

```
PYTHONPATH=src /opt/anaconda3/bin/python3 -m qpd_potential.cevns_subev
/opt/anaconda3/bin/python3 -m pytest tests/test_cevns_subev.py -q
```

---

## 1. CALC-17 — the sub-100-keV flux-truncation bound

### 1.1 What was computed, and what was *not*

The frozen reactor flux table floors at `E_nu = 0.1 MeV`. `cevns._fold_isotope` clamps
its lower integration limit with `max(E_min(T), flux.E_min)`, so rate that would come
from `E_nu < 0.1 MeV` is simply **absent** from `dR/dT`. CALC-17 bounds that absence.

For each of the five natural-Ge isotopes:

- **missing**  = `N_i ∫_{E_min,i(T)}^{0.1 MeV} Φ_flat · dσ_i/dT dE`, with
  `Φ_flat ≡ Φ(0.1 MeV) = 3.445974e12` ν̄/cm²/s/MeV held constant — a **labelled
  continuation constant, not an extrapolation of the interpolator**;
- **tabulated** = `N_i ∫_{max(E_min,i(T), 0.1)}^{E_max} Φ(E) · dσ_i/dT dE` — the same
  integral the pipeline performs, verified equal to `cevns.differential_rate` to 1e-9
  relative (`test_bound_uses_the_pipeline_cross_section`);
- both use `cevns.dsigma_dT` with the **same `(1 − MT/2E²)` kinematic factor and the same
  Helm form factor** the pipeline uses (CONVENTIONS §C, LOCKED);
- both carry `x_i · GE_ATOMS_PER_KG · 86400`, so every quantity is counts/kg/day/keV.

**The flux table was NOT extended.** `data/flux/reactor_flux_v1.0.csv` still has 101 knots
with `min(E_nu) = 0.1 MeV` exactly, and its data rows are byte-identical to `HEAD`
(`test_table_not_extended`). `ReactorFlux.flux()` is never evaluated below its own floor
anywhere in `cevns_subev.py`; the one sub-floor flux value in the module is the single
labelled `_continuation_phi` helper, asserted to have exactly one definition and one call
site. This is the locked forbidden proxy `fp-extend-flux-table` held shut by test rather
than by intention.

### 1.2 The bound

| `T` | missing [cts/kg/day/keV] | tabulated | **bound fraction** | roadmap target |
|---|---|---|---|---|
| 0.0999350 eV (extended-grid floor) | 19.0177 | 2350.274 | **0.8027 %** | ≤ 0.81 % ✅ |
| 0.100 eV (100 meV exactly) | 19.0004 | 2350.250 | 0.8020 % | ≤ 0.81 % ✅ |
| 0.150 eV | 8.9527 | 2331.449 | 0.3825 % | — |
| 0.290 eV | 0.020149 | 2278.808 | 0.000884 % | — |
| 0.30673 eV and above | **0.0 exactly** | — | **0.0 exactly** | "exactly zero" |

The recorded planning value 0.803 % reproduces to 0.8027 %. The bound is reported both as
a percentage **and** as the one-sided additive band `missing` in counts/kg/day/keV
(`METHODS.md` §3.4's recommended form) — the artifact carries both columns for every row.

### 1.3 The conservatism argument — *measured, not assumed*

The flat continuation bounds the missing rate from **above** only if `Φ` is non-increasing
as `E` falls toward the floor. That is a property of the frozen table, so it is checkable.
Read straight off the table's own lowest five knots:

| `E_nu` [MeV] | 0.100000 | 0.107984 | 0.108118 | 0.116606 | 0.116895 |
|---|---|---|---|---|---|
| `Φ` [ν̄/cm²/s/MeV] | 3.445974e12 | 3.462811e12 | 3.463100e12 | 3.481928e12 | 3.482586e12 |
| `d log Φ / d log E` | +0.0635 | +0.0673 | +0.0717 | +0.0763 | |

All four local slopes are **positive**: `Φ` *decreases* as `E` falls toward the floor. A
constant continuation at `Φ(0.1 MeV)` therefore **over-estimates** the missing flux, and
`bound_fraction` is a genuine upper bound.

**This is the plan's primary non-identity disconfirming check and it PASSED.** Had the
slope run the other way, ≤0.81 % would not have been an upper bound at all and CALC-17's
bound language would have had to be *withdrawn*, not restated. Corroborating the direction:
the physically motivated allowed-β-branch continuation `Φ(E) = Φ(0.1)(E/0.1)²` gives
**0.5804 %** at the grid floor — strictly smaller than the flat 0.8027 %, as it must be.

### 1.4 `E_min(100 meV)` — three values, three masses, one adopted

| label | mass | `E_min(100 meV)` |
|---|---|---|
| `phase7_natural` — **ADOPTED** | Phase-7 frozen abundance-weighted nuclear mass `m_N c² = 6.7724551e10 eV` (= 67724.551 MeV) | **58.1914 keV** |
| `conventions_molar` | `CONVENTIONS.md` §D natural-Ge molar mass 72.63 u × 931.494 MeV/u = 67654.409 MeV | **58.1612 keV** — this is the roadmap's **58.16 keV** |
| `ge74_only` | ⁷⁴Ge alone, 74 u × 931.494 MeV/u = 68930.556 MeV | **58.7072 keV** — the project-frozen ⁷⁴Ge figure |

Total spread **0.936 %**, i.e. entirely accounted for by the 0.94 % spread in the three
masses. None of the three is wrong; they answer three different questions. The phase adopts
`phase7_natural` because it is the project's own frozen abundance-weighted value, and it
reproduces the roadmap's 58.16 keV from the §D molar mass rather than quoting it.

### 1.5 The zero point — isotope-resolved, and a measured refinement of planning finding F2

The missing term vanishes for an isotope once `E_min,i(T) ≥ 0.1 MeV`, i.e. above
`T_i = 2E²/(M_i + 2E)` with `E = 0.1 MeV` — closed form, no scan, no tolerance:

| isotope | ⁷⁶Ge | ⁷⁴Ge | ⁷³Ge | ⁷²Ge | ⁷⁰Ge |
|---|---|---|---|---|---|
| `T_i` [eV] | 0.282511 | 0.290146 | 0.294121 | 0.298206 | **0.306726** |

The bound is identically `0.0` — *the number zero, not a small residual* — only above
**T = 0.3067 eV**, set by the **lightest** isotope ⁷⁰Ge. Two reconciliations:

- The roadmap's **0.29 eV** is almost exactly **⁷⁴Ge's own** zero point, 0.290146 eV. Read
  as the natural-mean-mass statement it is also close: the abundance-weighted mass gives
  0.2953 eV. Either way it is **below** the isotope-resolved threshold, so at 0.29 eV a
  small non-zero residual survives — 8.84e-6 of the total, well under the 1e-4 gate.
- **Correction to planning finding F2.** F2 attributes the 0.29 eV residual to ⁷⁰Ge
  *alone*. Measured, that is not right: **four** of the five isotopes are still kinematically
  open at 0.29 eV (⁷⁰, ⁷², ⁷³, ⁷⁴Ge), and only ⁷⁶Ge is closed:

  | isotope | `E_min(0.29 eV)` [keV] | missing [cts/kg/day/keV] |
  |---|---|---|
  | ⁷⁰Ge | 97.235 | 1.4255e-2 (70.8 %) |
  | ⁷²Ge | 98.615 | 5.4665e-3 (27.1 %) |
  | ⁷³Ge | 99.297 | 4.2415e-4 (2.1 %) |
  | ⁷⁴Ge | 99.975 | 2.7666e-6 (0.01 %) |
  | ⁷⁶Ge | 101.317 | **0.0** (closed) |

  ⁷⁰Ge *dominates* (71 %) and is the isotope that sets the threshold, but it does not
  exhaust the residual. Recorded here rather than rounded over, and pinned by
  `test_bound_vanishes`.

---

## 2. VALD-10 — the plateau leg

### 2.1 The analytic plateau, built independently of the fold

```
plateau = Σ_i N_i · (G_F² M_i / 4π) Q_W,i² (ħc)² · ∫Φ dE · 86400
```

i.e. `dσ_i/dT` in the `T → 0` limit where `(1 − MT/2E²) → 1` and the Helm form factor
`F(q) → 1`, so the neutrino-energy dependence factorises out of the fold entirely and only
`∫Φ dE` survives.

- `∫Φ dE = 7.495760e12` ν̄/cm²/s, integrated **knot by knot** over the table's own
  0.1–10 MeV span. (A single adaptive `quad` call over the whole span emits a scipy
  roundoff warning; the piecewise sum agrees with it to 4e-9 relative, far below anything
  claimed here. The table header's own `7.5029e12` is the *emission-side* bookkeeping
  figure and is not the same quantity as this quadrature of the tabulated `Φ`.)
- **Analytic plateau = 2372.3683 counts/kg/day/keV.**

It is built from `∫Φ` and the locked cross-section prefactor and **never** by extrapolating
the computed `dR/dT` downward — that would make the comparison an identity
(`fp-plateau-by-extrapolation`). `test_plateau_is_not_an_extrapolation_of_the_fold`
rebuilds it a second, independent way and asserts it differs from `dR/dT(floor)`.

**Weakest-anchor statement, carried forward.** The plateau is independent of the *fold*,
not of `Φ`. A normalization error in the frozen table would move `dR/dT` and the plateau
together and this comparison would not see it.

### 2.2 The approach, and both failure modes excluded

| `T` | `dR/dT` [cts/kg/day/keV] | ratio to plateau | **deficit** |
|---|---|---|---|
| 0.0999350 eV (grid floor) | 2350.274 | 0.99069 | **0.9313 %** |
| 0.0999 eV | 2350.287 | 0.99069 | 0.9308 % |
| 0.15 eV | 2331.449 | 0.98275 | 1.7248 % |
| 0.29 eV | 2278.808 | 0.96056 | 3.9437 % |
| 1.0 eV | 2068.300 | 0.87183 | 12.8171 % |
| 10.0 eV | 1321.367 | 0.55698 | **44.3018 %** |

Asserted, not eyeballed (`tests/test_cevns_subev.py`):

1. **Approaches from below, by ~1 % at the axis floor** — `dR/dT(floor)/plateau = 0.99069`,
   deficit 0.93 %, inside the stated 1.5 % gate (`test_plateau_value`).
2. **Does not rise toward low `T`** — `np.all(np.diff(dRdT) <= 0)` across the whole window,
   and `dR/dT < plateau` at every point, and every local log-log slope ≤ 0
   (`test_does_not_rise`). A spectrum that rose toward low `T` would be the power-law
   flux-extrapolation artifact `PITFALLS.md` flags.
3. **Does not collapse to zero** — no zero bins, `dR/dT(floor)/plateau = 0.9907 > 0.9`, and
   no neighbour ratio exceeds 10 (`test_does_not_fall_to_zero`). A collapse at the bottom
   would be a silently reached table floor.
4. **The deficit shrinks monotonically as `T` falls** and is *not* flat: it grows by a
   factor 47.6 from the floor to 10 eV (`test_approaches_from_below`). This is the test that
   separates the kinematic explanation from the competing one — a constant normalization
   offset would give a *flat* deficit.

The physical mechanism is `E_min(T) ∝ √T`: as `T` rises, the lower limit of the
neutrino-energy integral rises with it and progressively cuts low-energy flux out of the
fold. The plateau is what remains when that cut is removed entirely.

---

## 3. Clause-by-clause verdicts on ROADMAP Phase 12 SC2 and SC4

| # | Clause (verbatim intent) | Verdict | Measured |
|---|---|---|---|
| SC2-a | "`dR/dT` is **flat** from 100 meV to 10 eV to within a few percent" | **SUPERSEDED BY MEASUREMENT** | The spectrum falls **monotonically by 44.30 %** across that window (0.93 % deficit at the floor → 44.30 % at 10 eV). |
| SC2-b | "…and equals the analytic `T→0` plateau computed from the frozen `∫Φ` with the flat-box `dσ/dT`" | **PASS** (restated to what is decisive) | `dR/dT(0.0999350 eV)/plateau = 0.99069`, i.e. within **0.93 %** of the independently computed **2372.3683** counts/kg/day/keV. |
| SC2-c | "A spectrum that *rises* toward low `T` is an extrapolation artifact… unit-tested, not eyeballed" | **PASS** | Monotone non-increasing over the whole window and bounded above by the plateau everywhere; asserted in `test_does_not_rise`. |
| SC2-d | "…one that *falls to zero* is a table floor… unit-tested, not eyeballed" | **PASS** | No zero bins, ratio at the floor 0.9907, no order-of-magnitude neighbour step; asserted in `test_does_not_fall_to_zero`. |
| SC4-a | Bound "**computed** with the project's own Φ (flat continuation at its 100 keV value, including the `(1 − MT/2E²)` factor)" | **PASS** | Computed per isotope from the frozen table and `cevns.dsigma_dT`; nothing quoted from the roadmap or from `GPD/literature/`. |
| SC4-b | "reproducing **≤ 0.81 % at `T` = 100 meV**" | **PASS** | **0.8027 %** at the 0.0999350 eV grid floor; **0.8020 %** at exactly 100 meV. |
| SC4-c | "**and exactly zero above 0.29 eV**" | **PARTIAL — reconciled, not rounded** | Exactly `0.0` only above **0.3067 eV**, set by ⁷⁰Ge. At 0.29 eV a residual of **8.84e-6** of the total survives, carried by four still-open isotopes. The roadmap's 0.29 eV is essentially ⁷⁴Ge's own zero point (0.290146 eV). |
| SC4-d | "The flux table is **not** extended" | **PASS** | 101 knots, floor 0.1 MeV, data rows byte-identical to `HEAD`; source scan finds no write/append/synthetic-knot path. |
| SC4-e | "`E_min(100 meV)` = **58.16 keV** (natural-Ge mean mass) is adopted and reconciled against the project-frozen 58.7 keV (⁷⁴Ge-only)" | **PASS — with the adoption changed and stated** | All three reproduced: 58.1914 (Phase-7 abundance-weighted, **adopted**), 58.1612 (§D molar mass — the roadmap's figure), 58.7072 (⁷⁴Ge only). Spread 0.936 %. The phase adopts the project-frozen abundance-weighted mass and *names* the mass behind the roadmap's number rather than adopting the number blind. |
| — | Conservatism of the flat continuation (the plan's disconfirming check) | **PASS** | `d log Φ / d log E` = +0.0635 … +0.0763 across the lowest knots ⇒ Φ non-increasing toward the floor. `E²` continuation gives 0.5804 % < 0.8027 %. |

### Why SC2-a is reported SUPERSEDED rather than narrowed

The measured 44.30 % deficit at 10 eV is not a defect: it is `E_min(T) ∝ √T` doing exactly
what the kinematics require. The clause as written asserted flatness over a window across
which the physics *cannot* be flat. Two escapes were available and both are forbidden
proxies, so neither was taken:

- **`fp-narrow-the-window`** — evaluating flatness only over 0.1–0.3 eV (where the deficit
  really is 0.9–3.9 %) and calling SC2 passed. The emitted artifact spans the full
  0.0999350–10 eV window and `test_window_not_narrowed` asserts it.
- Restating "a few percent" as "within a factor of two." Not done.

What survives, and is stated as the decisive content of the VALD-10 plateau leg:
**`dR/dT` approaches the independently computed analytic plateau within ~1 % at the axis
floor, falls monotonically thereafter for the physically correct reason, and neither rises
nor collapses.** All three are asserted, not inspected.

---

## 4. Deliverables and their disposition rows

| deliverable | path | disposition row |
|---|---|---|
| `deliv-subev-module` | `src/qpd_potential/cevns_subev.py` | n/a (code) |
| `deliv-truncation-table` | `artifacts/v2.0/cevns_truncation_bound.csv` | `native_to_extended_axis`, floor 0.0999350 eV |
| `deliv-plateau-table` | `artifacts/v2.0/cevns_plateau_profile.csv` | `native_to_extended_axis`, floor 0.0999350 eV |
| `deliv-gates-report` | this file | n/a (report) |
| tests | `tests/test_cevns_subev.py` | n/a |

---

## 5. Checkpoint record (Task 3, `checkpoint:human-verify`)

**Status: recorded, NOT approved.** The user issued a standing session-level directive
(2026-07-22) to run the roadmap to completion without per-phase discussion unless a genuine
blocker arises. No blocker arose. The checkpoint content is therefore recorded here in full
and execution continued. **No approval was given and none is recorded.** Resume-signal idiom
that *would* have been presented: `[Y/n/e]` (Enter = Y).

**One-line summary presented:** CALC-17 reproduces at 0.8027 % with its conservatism proved
from the frozen table's own slope; the VALD-10 plateau leg passes at 0.93 % below an
independently computed 2372.3683 counts/kg/day/keV; ROADMAP SC2's flatness clause is
SUPERSEDED BY MEASUREMENT at 44.30 %.

**Review question put to the researcher (unanswered):**

> *"SC2 asked for a flat `dR/dT` from 100 meV to 10 eV; the spectrum in fact falls by 44 %
> across that window for a physically correct reason. Is 'approaches the analytic plateau
> within 1 % at the axis floor, monotone, neither rising nor collapsing' the right
> restatement of the VALD-10 plateau gate, or do you want the gate re-drawn?"*

**Items flagged for attention:**

1. SC2-a is **SUPERSEDED**, not passed. The window was not narrowed.
2. SC4-c is **PARTIAL**: the zero point is 0.3067 eV (⁷⁰Ge), not 0.29 eV, and the residual
   at 0.29 eV is carried by *four* isotopes, not one — a correction to planning finding F2.
3. The adopted `E_min` is the Phase-7 abundance-weighted 58.1914 keV, **not** the roadmap's
   58.16 keV; the roadmap's value is reproduced and attributed to the §D molar mass.

---

## 6. Standing caveats and open items carried out of this plan

- **Shared dependence is not a cross-check.** The truncation bound and the plateau are
  independent gates but share `cevns.dsigma_dT` and the frozen `Φ`. Agreement between them
  would not be evidence; they are reported as two separate measurements against two separate
  targets.
- **The `Φ` sub-1.8 MeV region carries a declared 20–25 % uncertainty** and is a
  summation-model placeholder. The conservatism argument in §1.3 rests on its *local slope*
  near 0.1 MeV. If that region's shape is wrong, the bound's **direction**, not merely its
  size, is in question. This is the weakest anchor of CALC-17 and it is not repaired here.
- **Quadrature tolerance is asserted, not characterised.** `cevns._fold_isotope` uses
  adaptive `quad` on a near-threshold integrand where `(1 − MT/2E²)` sweeps 0 → O(1) across
  the lowest decade of the flux. The single-call `∫Φ` quadrature emits a scipy roundoff
  warning; the knot-by-knot sum used here agrees to 4e-9, but the *fold's* per-isotope
  quadrature accuracy at the 0.8 % level has not been independently characterised.
- **The Helm form factor is taken as ≈1 across the whole sub-eV window.** True to far better
  than the bound at these momentum transfers, but assumed rather than measured here.
- **The additive-band form is a choice.** `METHODS.md` §3.4 recommends carrying the
  truncation as a one-sided additive band on `dR/dT` below 0.29 eV; no downstream phase has
  yet declared how it wants to consume it. Both the percentage and the additive band ship.
