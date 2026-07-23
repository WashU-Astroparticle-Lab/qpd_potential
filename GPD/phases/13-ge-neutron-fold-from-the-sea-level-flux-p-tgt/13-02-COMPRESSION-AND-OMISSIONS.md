# 13-02 — Kinematic Compression Adjudicated, and the High-Energy Omissions Bounded

**Plan:** 13-02 (wave 2) · **accuracy_label = `order_of_magnitude`** on every quantity below.
**Interpreter:** `/opt/anaconda3/bin/python3`. **Module:** `src/qpd_potential/neutron_recoil.py`
(appended below Plan 13-01's section). **Tests:** `tests/test_neutron_kinematics.py` (20 passed).

> **Axis discipline.** `E_n` is INCIDENT NEUTRON KINETIC ENERGY; `T` is NUCLEAR RECOIL energy.
> The recoil axis is keV_nr, no quenching.

**Reproduce:**
```
PYTHONPATH=src /opt/anaconda3/bin/python3 -c "from qpd_potential import neutron_recoil as n; \
  n.write_compression_table(); n.write_omission_table()"
PYTHONPATH=src /opt/anaconda3/bin/python3 -m pytest -q tests/test_neutron_kinematics.py
```

---

## 1. The derivation SC4 has to survive

ROADMAP SC4 asserts that `T_max/E_n = 0.0536` for natural Ge against `0.0215` for W is *why*
germanium is the worse neutron target — "the same incident flux produces a ~2.5× wider recoil
spread in Ge than in CaWO₄". SC4's own wording is **"exhibited, not asserted"**, so the ratio is
the criterion's INPUT and cannot be its output (`fp-assert-compression`).

**Re-derived here rather than quoted from the plan.** Start from the flat-box fold with a general
cross section and substitute `E = (T/f)·x`, `dE = (T/f) dx`:

```
dR/dT = n INT_{T/f}^{inf} phi(E) sigma(E) / (f E) dE
      = n INT_{1}^{inf} phi((T/f)x) sigma((T/f)x) / (f (T/f) x) (T/f) dx
      = n INT_{1}^{inf} phi((T/f)x) sigma((T/f)x) x^{-1} dx .
```

For the epithermal `phi(E) = C/E`:

```
dR/dT = n INT_{1}^{inf} (C f /(T x)) sigma((T/f)x) x^{-1} dx * (1/f) * f
      = n (C/T) INT_{1}^{inf} sigma((T/f) x) x^{-2} dx .
```

**Two statements follow, and they are different:**

1. **The `1/f` prefactor cancels against the `T/f` lower limit for ANY `sigma(E)`.** The
   kinematic factor never multiplies the rate.
2. **`f` survives only inside `sigma`'s argument.** It selects *which part of `sigma(E_n)`* a
   given recoil `T` samples. That is exactly the physics of the resonance edge Plan 13-01
   measured at `T = f·E_res`. It moves features **along T**; it does not scale the rate.

For **constant** `sigma` the surviving dependence disappears too, and
`dR/dT = n sigma C / T` — **`f` has no effect at all.**

**Measured, at four kinematic factors under a pure `1/E` flux:**

| quantity | value | tolerance |
|---|---|---|
| max relative spread across `f ∈ {0.0215, 0.0536, 0.0952, 0.2215}` | **4.1997×10⁻⁸** | ≤ 10⁻⁵ |
| max deviation from the closed form `N σ C / T` | 4.6512×10⁻⁸ | ≤ 10⁻⁵ |

**How close is the real flux to that limit?** Recomputed independently from the pinned driver:
`E·phi` over 1 eV – 10 keV is flat to a factor **1.3901**, reproducing `09-02` §5's recorded
1.390. So the band that feeds the RoI sits close to the limit in which `f` provably does nothing.

---

## 2. What actually differs between targets

Every leg uses the **same incident flux** and each material's **own atoms/kg**.

### 2.1 Leg quality, stated first

This repository owns a resonance-resolved `sigma_el` for **germanium alone**. Every ratio leg
below therefore uses a **common constant `sigma = 1 b` for every target including Ge**. Its value
cancels identically from any target-to-target ratio, and holding it common is deliberate:
comparing a resonance-resolved Ge against a smooth W would produce *"Ge has more structure"*
**by construction**. Germanium's own resonance-structure term is reported separately and enters
**no** ratio.

> **The consequence, stated rather than buried:** these legs settle the **mechanism**, not the
> absolute direction. Real `sigma_el` is element-dependent and this project holds no cross
> section for W, Ca or O. Any direction below is conditional on `sigma` being element-independent,
> which it is not.

Size of the term that is missing for the other targets: germanium's real `sigma_el` against the
common 1 b gives a factor **8.88 (T=0.1 eV), 12.14 (1 eV), 11.23 (10 eV), 9.54 (31.6 eV),
10.83 (100 eV), 7.79 (1 keV)** — i.e. Ge's contribution-weighted effective cross section is
~8–12 b and varies by ~±20% across the band. An element-dependent factor of that size in the
other legs would be enough to move any direction below.

### 2.2 Atoms per kg — each material's own

`N_A = 6.022×10²³` from `CONVENTIONS.md` §D's test-value line. Cross-check: `1000/72.63 × N_A =
8.291340×10²⁴` against the frozen table's `N_Ge/rho` derivation `8.291565×10²⁴` — **0.003%**.

| target | M [g/mol] | atoms/kg | `f` per species | atom fractions |
|---|---|---|---|---|
| Ge | 72.63 | 8.29134×10²⁴ | 0.053600 (frozen header) | — |
| W | 184 | 3.27283×10²⁴ | 0.021505 | — |
| Ca | 40 | 1.50550×10²⁵ | 0.095181 | — |
| O | 16 | 3.76375×10²⁵ | 0.221453 | — |
| **CaWO₄** | 288 | **1.25458×10²⁵** | Ca 0.095181, W 0.021505, **O 0.221453** | Ca 16.67%, W 16.67%, **O 66.67%** |

The mass numbers are the dominant natural isotope's, and `4A/(1+A)²` reproduces the roadmap's own
quoted factors: 0.021505 (A=184), 0.095181 (A=40), 0.221453 (A=16) against 0.0215, 0.0952, 0.2215.

### 2.3 Matched-T ratios, `dR/dT(Ge) / dR/dT(target)`

| target | atoms/kg ratio | ratio, pure `1/E` | ratio, real flux at T = 0.1 / 1 / 10 / 31.6 / 100 / 1000 eV |
|---|---|---|---|
| W | **2.53339** | 2.53339 → 2.53692 | 2.4637, 2.4927, **2.4554, 2.3973, 2.2942**, 1.9925 |
| Ca | 0.55074 | 0.55074 → 0.55051 | 0.5664, 0.5565, 0.5587, 0.5639, 0.5747, 0.6218 |
| O | 0.22029 | 0.22029 → 0.22014 | 0.2437, 0.2266, 0.2273, 0.2313, 0.2402, 0.2848 |
| **CaWO₄** | **0.66088** | 0.66088 → 0.66068 | **0.7060, 0.6726, 0.6728, 0.6787, 0.6918**, 0.7551 |

(bold = inside the 10–100 eV RoI.)

**Under the pure `1/E` flux the ratio equals the atoms/kg ratio to 5 significant figures at every
T.** That is the decisive mechanism measurement: with `f` cancelling, nothing but target number
density is left.

### 2.4 Attribution, each contribution sized

Decomposition `ratio_real = (atoms/kg ratio) × (1 + flux-shape part) × (1 + kinematic part)`,
verified to close to 10⁻⁶ (`test_target_ratio_is_attributed_and_the_parts_sum`).

**Ge vs W:**

| T [eV] | atoms/kg | flux-shape part | kinematic part | resonance structure |
|---|---|---|---|---|
| 0.1 | 2.53339 | −2.75% | +1.4×10⁻⁷ | not computable for W |
| 10 | 2.53339 | −3.08% | +1.4×10⁻⁵ | " |
| 31.6 | 2.53339 | **−5.38%** | +4.4×10⁻⁵ | " |
| 100 | 2.53339 | −9.46% | +1.4×10⁻⁴ | " |
| 1000 | 2.53339 | −21.46% | +1.4×10⁻³ | " |

**Ge vs CaWO₄:**

| T [eV] | atoms/kg | flux-shape part | kinematic part |
|---|---|---|---|
| 0.1 | 0.66088 | +6.83% | −3.1×10⁻⁸ |
| 10 | 0.66088 | +1.80% | −3.1×10⁻⁶ |
| 31.6 | 0.66088 | +2.70% | −9.7×10⁻⁶ |
| 100 | 0.66088 | +4.68% | −3.1×10⁻⁵ |
| 1000 | 0.66088 | +14.29% | −3.1×10⁻⁴ |

**The kinematic part is not the compression mechanism.** It is ≤ 1.4×10⁻³ everywhere and ≤
1.4×10⁻⁴ inside the RoI, and its origin is the **finite 20 MeV ceiling**: a box that ends at
`f·E_top` differs by target because `E_top` is finite. The compression mechanism itself
contributes **exactly zero**, as §1 derives.

**So the attribution is:** atoms/kg accounts for the *entire* leading-order effect; the flux's
departure from `1/E` supplies a −1.6% to −9.5% correction across the RoI for W and +1.8% to +4.7%
for CaWO₄; the kinematic factor supplies nothing; and the resonance-structure term — the only one
that would genuinely be target-specific — cannot be computed for any target but germanium.

---

## 3. The CaWO₄-vs-W substitution, and its directional consequence

The roadmap's SC4 sentence is about **CaWO₄** but supplies **tungsten's** kinematic factor. They
are not the same statement.

- **Oxygen, not tungsten, dominates CaWO₄'s atom count:** 4 O per formula unit = **66.67%** of
  the atoms, against 16.67% each for Ca and W.
- **Oxygen carries the largest kinematic factor** in the compound, `f = 0.221453`, which is
  **4.13× germanium's** 0.0536 — the opposite sense of the roadmap's premise.
- **CaWO₄ has 1.51× MORE atoms per kg than Ge** (1.25458×10²⁵ vs 8.29134×10²⁴), precisely because
  it is two-thirds oxygen by atom count.

**The substitution changes the direction of the comparison.** Under the common constant `sigma`:

| comparison | in-RoI ratio Ge/target | reading |
|---|---|---|
| Ge vs **W** | **2.29 – 2.46** | Ge is the **worse** target per kg |
| Ge vs **CaWO₄** | **0.673 – 0.692** | **Ge is the BETTER target per kg**, by ~1.45× |

That is a finding, not a footnote: the statement the roadmap actually makes (Ge vs CaWO₄) points
the **opposite way** from the number it supplies to support it (Ge vs W), and the reason is
oxygen's low mass, which raises CaWO₄'s atoms/kg — the very mechanism §2 identifies as operative.

**Caveat carried with it:** this direction is conditional on the common-constant-`sigma`
assumption (§2.1). Germanium's own effective `sigma_el` is ~8–12 b in this weighting; if oxygen's
is materially smaller, the CaWO₄ leg falls and the direction could revert. This project cannot
settle that with the data it holds, and no direction is claimed beyond what the common-`sigma`
legs support.

---

## 4. The numerical degeneracy that makes SC4 look confirmed

`f_Ge / f_W = 0.0536 / 0.021505 = **2.4925**`.
`n_Ge / n_W  = **2.53339**`.

**These are near-degenerate for a reason, and the reason is not that they are the same physics.**
For large A,

```
n(A) = 1000 N_A / M ~ 1000 N_A / A            ->  n_Ge/n_W = A_W/A_Ge = 184/72.63 = 2.5334
f(A) = 4A/(1+A)^2                             ->  f_Ge/f_W = (A_W/A_Ge)((1+A_W)/(1+A_Ge))^-2 ... 
                                                          ~ A_W/A_Ge  to O(1/A)
```

Both track `A_W/A_Ge`. They differ by **1.6%**, which is far inside this channel's accuracy label.
So a "~2.5× effect" is present and its magnitude matches SC4's number — but the ~2.5× that
actually produces it is **target number density per unit mass**, not kinematic compression. The
agreement of 2.49 with 2.533 is an algebraic near-identity of mass number, not a corroboration.

This is the pattern the phase was told to watch for, and it is the fifth roadmap clause of the
milestone to come under measurement.

---

## 5. SC4 verdict

> **SC4 verdict: SUPERSEDED BY MEASUREMENT.**

Split into its two components, because they resolve differently:

| component of SC4 | verdict | measurement |
|---|---|---|
| **Mechanism** — that Ge's 2.5× larger `T_max/E_n` "spreads recoils wider" and thereby raises the neutron background | **SUPERSEDED BY MEASUREMENT** | The kinematic factor cancels analytically for any `sigma` and exactly for constant `sigma`; measured spread across four `f` values is 4.2×10⁻⁸. Inside the RoI its residual effect is ≤ 1.4×10⁻⁴, and that residual is the finite-20-MeV-ceiling truncation, not compression. |
| **Direction vs W** — that Ge is worse | **CONFIRMED, but for a different reason** | Ge/W = 2.29–2.46 per kg in the RoI. Attribution: 2.533× from atoms/kg, −3% to −9% from flux shape, ~0 from `f`. |
| **Direction vs CaWO₄** — the statement actually made | **REVERSED under measurement** | Ge/CaWO₄ = 0.673–0.692 per kg in the RoI. Ge is the **better** target by ~1.45×, because oxygen dominates CaWO₄'s atom count and CaWO₄ carries 1.51× more atoms per kg. |

**No band was narrowed to make anything true.** The comparison band is the full 10–100 eV RoI and
the probe set spans four decades of `T` either side of it. The reversal is reported as a finding.

**What would overturn this verdict:** an element-resolved `sigma_el` for W, Ca and O. If oxygen's
effective elastic cross section over the RoI-feeding band were ≲ 0.67× germanium's, the Ge-vs-CaWO₄
direction would revert to SC4's. That is a real possibility and it is why the direction claims
here are labelled conditional while the **mechanism** claim is not — the mechanism result is an
identity of the fold and holds for any cross section.

---

## 6. The >20 MeV omission, bounded at the surface

### 6.1 The continuation's conservatism — measured before it was used

`fp-unchecked-continuation` forbids using a flat continuation without measuring the slope. The
Phase-12(c) **method** is reused; its **conclusion** is re-measured.

Top decade of the frozen table, 2 – 20 MeV, 421 points:

| quantity | value |
|---|---|
| `sigma_el` at 2 MeV → at 20 MeV | 1.998519 b → **1.222782 b** |
| OLS slope over the decade | **−2.667195×10⁻³ b/MeV** |
| OLS slope over the last half-decade (10–20 MeV) | **−1.068209×10⁻¹ b/MeV** |
| maximum in the decade | **2.316993 b, at 8 MeV** |
| strictly non-increasing over the decade? | **No** — 34.0% of steps rise |
| is `sigma(20 MeV)` the band maximum? | **No** |

**The trend approaching the ceiling is decreasing** — the slope is negative over the decade and
five times more steeply negative over the last half-decade, and `sigma` falls monotonically from
2.212 b at 10 MeV to 1.223 b at 20 MeV. That licenses a flat continuation at `sigma(20 MeV)` as an
**estimate**.

**But it does not on its own make that an upper bound**, because the decade is not monotone: there
is a local maximum of 2.317 b at 8 MeV. So **two** continuations are reported rather than one:

- `flat_at_ceiling` — `sigma = 1.222782 b`, the trend-justified estimate;
- `flat_at_band_max` — `sigma = 2.316993 b`, which bounds from above even if the trend reversed
  above 20 MeV.

This is a departure from the plan's expectation of a single flat continuation, and it is reported
rather than resolved by picking the smaller number.

### 6.2 Two fractions, not one

Flux above the ceiling from the pinned driver out to 10 GeV:
**Φ(>20 MeV) = 3.181822×10⁻³ cm⁻² s⁻¹**.

Baselines: in-RoI (10–100 eV) **4.418963×10³ counts kg⁻¹ day⁻¹**; T-integrated total
**3.129873×10⁴ counts kg⁻¹ day⁻¹**.

| continuation | σ used | Δ(dR/dT) added [c/kg/day/keV] | added in-RoI | **in-RoI fraction** | added total | **total-rate fraction** |
|---|---|---|---|---|---|---|
| `flat_at_ceiling` | 1.222782 b | 0.66194 | 0.059575 | **1.3482×10⁻⁵** | 2787.24 | **8.905%** |
| `flat_at_band_max` | 2.316993 b | 1.25429 | 0.112886 | **2.5546×10⁻⁵** | 5281.42 | **16.874%** |

**The two fractions differ by a factor of ~6600.** That IS the result, and it is exactly what
`fp-single-omission-number` exists to prevent being collapsed: the flat-box height falls as
`1/E_n`, so a 1 GeV neutron spreads its recoil over a box `f × 1 GeV = 53.6 MeV` wide and deposits
almost nothing inside a 90 eV-wide RoI, while contributing its full cross section to the
T-integrated total. Quoting the in-RoI number alone would have made a 17% total-rate omission look
like a 2.6×10⁻⁵ one.

The same structure as the now-void Phase-7 argument, but derived at the surface from data this
project holds rather than from a shielding configuration that does not exist here.

### 6.3 Direction and the elastic-only understatement

`09-02` §7 schema row for this omission:

| channel | quantity | signed deviation | **direction** | why |
|---|---|---|---|---|
| neutron | `E_n > 20 MeV` elastic recoils, omitted by the frozen `sigma_el` ceiling | −1.35×10⁻⁵ to −2.55×10⁻⁵ of the in-RoI rate; −8.91% to −16.87% of the T-integrated total | **`flatters_SB`** | Truncating the cross section REMOVES background from the fold, so the reported rate is low and S/B correspondingly high. |
| neutron | the elastic-only restriction on that bound | not quantifiable with the data this project holds | **`flatters_SB` (further)** | The frozen set is MF=3 MT=2 elastic only. Above ~20 MeV nonelastic and spallation channels are comparable to or larger than elastic **and** produce larger recoils per interaction, so an elastic-only bound UNDERSTATES the true impact. |

**Nothing is netted** (`fp-net-omissions`). Both rows are carried openly alongside the channel's
`penalizes_SB` central value (the outdoor leg with the Gordon midpoint) rather than subtracted
from it.

### 6.4 The two declared omissions of `09-02` §6, resolved against each other

| | value |
|---|---|
| `sigma_el` ceiling | 2.0×10⁷ eV |
| committed flux-table top edge | 2.0×10⁸ eV |
| **subsumed?** | **YES** — the flux-table ceiling is *above* the `sigma_el` ceiling, so every neutron above it is also above 20 MeV |
| Φ above the flux-table ceiling / Φ(>10 MeV) | **20.55%** (reproduces `09-02` §6.2's recorded 21%) |
| Φ above the flux-table ceiling / Φ above the `sigma_el` ceiling | 22.93% |

**And the flux-table ceiling is not an independent omission here at all.** This channel never
reads the committed flux table for the fold: the pinned PARMA driver is evaluated directly at
every quadrature node and reaches 10 GeV. What remains is the single 20 MeV `sigma_el` ceiling,
which subsumes it. Treating them as two additive omissions would double-count; merging them
without checking would have dropped the fact that the driver removes one of them outright.

---

## 7. CALC-24 disposition — decided against the measured number

**The Phase-7 deferral rationale is recorded VOID and is not re-used.** It rested on shielding
attenuating the >10 MeV tail; `09-02` §6.2 records it void at the surface (there is no shield).
It appears in this phase only as a record that it is void (`fp-inherit-void-rationale`), and an
executed grep over the module and both artifacts confirms it is used as a justification nowhere
(`test_void_rationale_is_never_used_as_a_justification`).

**The evaluation:**

| quantity | value |
|---|---|
| worst-case in-RoI omission fraction | 2.5546×10⁻⁵ |
| worst-case total-rate omission fraction | **0.16874** |
| the channel's own label, as a fractional excursion | 2.0 (a factor ~3) |
| inside the label? | **YES** |
| understatement multiplier needed to break it | **11.85×** |

> **Branch taken: DEFERRAL SUSTAINED ON THE MEASURED BOUND.**
>
> **Replacement rationale (new, not inherited):** the >20 MeV omission is bounded at
> 2.6×10⁻⁵ of the in-RoI integrated rate and 16.9% of the T-integrated total rate under an
> *upper* continuation whose conservatism was established by measuring the cross-section slope at
> the ceiling. Both sit inside the channel's own order-of-magnitude label, and the elastic-only
> restriction would have to understate the bound by more than **11.9×** for the total-rate
> omission to reach that label. The TENDL-2023 splice therefore remains follow-up scope, on this
> measurement rather than on any premise about the detector's surroundings.

**What would flip this branch.** If nonelastic channels above 20 MeV multiply the elastic-only
bound by more than ~12, the total-rate omission reaches the label and CALC-24 stops being
defensibly deferrable. This project cannot measure that multiplier with the data it holds — the
frozen set is elastic only — so the branch is stated with its own falsifier attached rather than
as a settled fact. The in-RoI branch has an enormous margin (a multiplier of ~7.8×10⁴ would be
needed), so the risk is confined to the T-integrated total rate, which no milestone deliverable
currently reports as a headline.

---

## 8. Discharge table for Plan 13-02

| acceptance test | outcome | evidence |
|---|---|---|
| `test-f-cancellation` | **PASS** | §1 — spread 4.1997×10⁻⁸ across four `f` (≤10⁻⁵), below the 13-01 quadrature tolerance |
| `test-target-ratio-measured` | **PASS** | §2.3–2.4 — ratios with their T dependence, attributed to atoms/kg, flux shape and `f`, each sized; leg quality labelled |
| `test-cawo4-not-w` | **PASS** | §3 — O is 66.67% of the atom count with `f` 4.13× Ge's; the substitution REVERSES the direction, reported as a finding |
| `test-sc4-verdict-recorded` | **PASS** | §5 — SUPERSEDED BY MEASUREMENT for the mechanism, with the direction split by comparison basis |
| `test-sigma-slope-measured` | **PASS** | §6.1 — slope −2.667×10⁻³ b/MeV over the decade, −1.068×10⁻¹ over the last half-decade, non-monotonicity reported, two continuations used |
| `test-omission-split` | **PASS** | §6.2 — 1.35–2.55×10⁻⁵ in-RoI against 8.91–16.87% total, a factor ~6600 apart |
| `test-omission-direction` | **PASS** | §6.3 — `flatters_SB`, elastic-only understatement declared, nothing netted |
| `test-ceiling-subsumption` | **PASS** | §6.4 — subsumed; 20.55% reproduces the recorded 21%; the flux ceiling is not independent here |
| `test-calc24-conditional` | **PASS** | §7 — branch taken explicitly, 0.16874 against a 2.0 label, 11.85× margin |
| `test-void-rationale-not-reused` | **PASS** | §7 — executed grep over the module and both artifacts, zero uses as a justification |

---

## 9. What still cuts against this result

- **The comparison legs are constant-`sigma`.** They settle the mechanism, not the absolute
  direction. Germanium's own effective `sigma_el` is ~8–12 b in this weighting and varies by ±20%
  across the band; an element-dependent factor of that size would move any direction reported here.
  This is the weakest input in the plan and it cannot be strengthened in this environment.
- **Nothing above 20 MeV is measured at all.** The bound rests on a continuation argument about a
  quantity measured only below the ceiling, and the band below the ceiling is not monotone.
- **The elastic-only restriction is unquantifiable here.** Its direction is known
  (`flatters_SB`); its magnitude is not.
- **Ge inelastic channels** (⁷⁴Ge 596 keV, ⁷²Ge 834 keV) are Phase 14's, and they bias this
  bound in the same `flatters_SB` direction: omitting them removes background.
- **The lethargy flatness is 1.390, not 1.000.** The exact cancellation is a limit, and the real
  flux departs from it by up to −21% (W) and +14% (CaWO₄) at T = 1 keV. Inside the RoI the
  departure is ≤ 9.5%, which is why the mechanism conclusion holds there.
