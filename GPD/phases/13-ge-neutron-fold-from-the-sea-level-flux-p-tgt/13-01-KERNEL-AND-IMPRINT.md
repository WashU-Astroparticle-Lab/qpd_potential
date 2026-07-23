# 13-01 — Kernel, Quadrature and Resonance Imprint

**Plan:** 13-01 (wave 1) · **accuracy_label = `order_of_magnitude`** on every quantity below
(inherited at the point of definition from `09-02-NEUTRON-DECLARATION.md` §3.4).
**Interpreter:** `/opt/anaconda3/bin/python3` (numpy 1.26.4, scipy 1.17.1, NCrystal 4.4.6).
**Module:** `src/qpd_potential/neutron_recoil.py` · **Tests:** `tests/test_neutron_recoil.py` (25 passed).

> **Axis discipline.** `E_n` is INCIDENT NEUTRON KINETIC ENERGY. `T` is NUCLEAR RECOIL energy.
> A 1 MeV neutron does not deposit 1 MeV. `T` is keV_nr on the unified phonon scale — no
> Lindhard, no quenching (`CONVENTIONS.md` §B).

---

## 0. What was computed

```
dR/dT(T) = N_Ge * INT_{E_min(T)}^{E_top} phi_default(E_n) sigma_el(E_n) / (f E_n) dE_n ,
           E_min(T) = T / f
```

| input | value | where it was READ from (not transcribed) |
|---|---|---|
| `f = T_max/E_n` (natural Ge) | **0.0536** | `data/endf_nGe_elastic_v1.1.csv` header, `T_max/E_n natural (abundance-weighted, AS COMPUTED) = 0.0536`, parsed by `neutron_recoil.elastic_header()` |
| `N_Ge` | **8.291565×10²⁴ atoms/kg** | derived as `4.4136e22 atoms/cm^3 / 5.323 g/cm^3 × 1000 g/kg` from the same header. `CONVENTIONS.md` §D quotes 8.29×10²⁴; they agree to 0.02% |
| `sigma_el` | 23 155-point union grid, ENDF/B-VIII.0 + LANL Lib80x @ 293.6 K | the same file, columns `E_eV, sigma_el_natural_b, a1_natural`; frozen `git_sha = f742c63` |
| `E_top` | **2×10⁷ eV** (the ENDF ceiling) | last row of the frozen table. Never extrapolated above |
| `phi_default` | pinned PARMA v4.10 / Sato-2015 driver, commit `6ff37ca…`, `k = 1.09610` | `src/qpd_potential/parma_neutron_flux.py`, evaluated **directly** at every quadrature node |

`phi_lo` is **not selectable**: `neutron_recoil.neutron_flux_cm2_s_MeV(..., column="phi_lo")`
raises `FluxColumnError`. Tested (`test_phi_lo_and_band_midpoint_raise`).

**Reproduce everything below:**
```
PYTHONPATH=src /opt/anaconda3/bin/python3 -c "from qpd_potential import neutron_recoil as n; \
  n.write_flux_continuity_table(); n.write_dRdT_table()"
PYTHONPATH=src /opt/anaconda3/bin/python3 -m pytest -q tests/test_neutron_recoil.py
```

---

## 1. Dimensional check (`test-dimensions`)

| factor | units | conversion applied | named constant |
|---|---|---|---|
| `N_Ge` | kg⁻¹ | — | — |
| `phi_default` | cm⁻² s⁻¹ MeV⁻¹ | ÷ 10⁶ → cm⁻² s⁻¹ eV⁻¹ | `EV_PER_MEV = 1.0e6` |
| `sigma_el` | barn | × 10⁻²⁴ → cm² | `BARN_TO_CM2 = 1.0e-24` |
| `1/(f E_n)` | eV⁻¹ | — | — |
| `dE_n` | eV | — | — |
| **product** | **kg⁻¹ s⁻¹ eV⁻¹** | × 86400 → kg⁻¹ day⁻¹ eV⁻¹ | `SECONDS_PER_DAY = 86400.0` |
| | | × 1000 → **counts kg⁻¹ day⁻¹ keV⁻¹** | `EV_PER_KEV = 1.0e3` |

Those four are the only numerical conversion constants in the module, and
`test_conversion_constants_are_named` asserts their values. The executable half of the check
(`test_dimensional_scaling_of_the_fold`) verifies that `N_Ge` and `sigma_el` each enter
**linearly** to 10⁻¹² relative, and `test_oracle_derivation_is_scale_linear` verifies that `C`
and `sigma` enter linearly and `T` as `1/T`.

---

## 2. Closed-form oracle (`test-oracle`) — and the exact cancellation of `f`

**Derivation** (re-derived here, not quoted). For `phi(E) = C/E` and constant `sigma`:

```
INT_{T/f}^{inf} (C/E) * sigma/(f E) dE = (C sigma / f) INT_{T/f}^{inf} E^-2 dE
                                       = (C sigma / f) * (f / T)
                                       = C sigma / T .
```

**The kinematic factor `f` cancels exactly.** `dR/dT = N_Ge sigma C / T`, independent of `f`.

Driving the production quadrature with the synthetic input (`C = 2.24×10⁻⁴ cm⁻² s⁻¹`,
`sigma = 8.9 b`, `E_top = 10¹² eV` so the finite-top term `T/(f E_top)` is < 10⁻⁷):

| `f` | target | max relative deviation from `N sigma C / T` at T = 0.1, 10, 1000 eV |
|---|---|---|
| 0.0215 | W | **4.651×10⁻⁸** |
| 0.0536 | natural Ge | **1.866×10⁻⁸** |
| 0.0952 | Ca | **1.050×10⁻⁸** |
| 0.2215 | O | **4.515×10⁻⁹** |

**Max spread across the four `f` values: 4.200×10⁻⁸**, against the plan's ≤ 10⁻³ oracle
tolerance and the ≤ 10⁻⁵ `f`-cancellation tolerance. The residual is the finite-`E_top`
truncation term, which is the only `f`-dependence the construction can have.

The deviations are *exact* rather than merely small because `loglog_segment_integrals`
integrates a piecewise power law analytically, and the epithermal integrand `∝ E⁻²` **is** a
power law. This is the analytic backbone Plan 13-02's SC4 adjudication rests on: an
`f`-dependence appearing here would have invalidated that plan too. It did not appear.

---

## 3. Convergence (`test-convergence`)

Real inputs, `T` on 60 log points from the 0.0999350 eV floor to 10 keV. `per_decade` counts
the **supplemental** log nodes added on top of the 23 155 frozen union-grid nodes.

| refinement | max relative change in dR/dT |
|---|---|
| 100 → 200 nodes/decade | 6.887×10⁻⁵ |
| **200 → 400 nodes/decade** | **1.346×10⁻⁴** |
| 400 → 800 nodes/decade | 1.374×10⁻⁵ |

Tolerance (module constant `CONVERGENCE_TOL`, declared before the run): **0.5%**. Passed by
more than three orders of magnitude. Production uses 200/decade.

---

## 4. Anchored vs unanchored quadrature (`test-anchor-loss`) — what `fp-unanchored-quadrature` costs

Signed `(unanchored − anchored)/anchored`, over the same 60-point `T` set:

| node set | median | most negative | most positive |
|---|---|---|---|
| union grid + 200/decade, lower limit snapped up | **−1.138×10⁻³** | −9.544×10⁻³ | −7.93×10⁻⁹ |
| union grid + 50/decade, lower limit snapped up | −1.831×10⁻³ | −3.061×10⁻² | +1.007×10⁻⁴ |
| plain log grid, 200/decade, no union nodes | −4.852×10⁻³ | −1.021×10⁻² | −3.79×10⁻⁵ |
| **plain log grid, 50/decade, no union nodes** | **−2.197×10⁻²** | **−1.464×10⁻¹** | +1.033×10⁻² |

Per-`T` detail at 200/decade with union nodes:

| T [eV] | 0.1 | 1 | 10 | 100 | 1000 | 10⁴ |
|---|---|---|---|---|---|---|
| rel. difference | −6.5×10⁻¹² | −4.48×10⁻⁵ | −8.35×10⁻⁵ | −8.33×10⁻⁵ | −2.48×10⁻⁴ | −3.03×10⁻⁴ |

**The difference is not zero everywhere** — the failure condition the plan names is not met, so
the check proved something. The sign is systematically **negative**: dropping the endpoint
segment removes positive integrand, i.e. an unanchored quadrature **under**states this
background, which is a `flatters_SB` direction.

Two honest caveats. (i) At `T = 0.1 eV` the difference is ~10⁻¹¹ *by construction*: `E_min(T)`
there is the node set's own lower bound, so it is a node under either rule. That degenerate
point is reported, not hidden. (ii) The realistic proxy — a plain log-substituted grid that also
loses the resonance-resolved union nodes — is an order of magnitude worse (median −2.2%, worst
−14.6%) and, unlike the pure endpoint effect, can also overshoot (+1.0%) where it straddles a
resonance. Both failure modes belong to the same forbidden proxy.

---

## 5. Flux continuity across the 1 eV – 10.14 eV gap (`test-flux-overlap`, `test-gap-closed`)

**The gap is real and was not recorded anywhere before this phase.**

| quantity | value |
|---|---|
| top node of `data/ambient_neutron_thermal_v2.0.csv` | **1.0 eV** |
| lowest bin EDGE of `data/ambient_neutron_flux_v1.1.csv` | **10.0 eV** |
| lowest bin CENTRE of the same table | **10.144972680282425 eV** |
| recoils below … are fed partly from inside the gap | **T < f × 10.145 eV = 0.54377 eV** |
| recoils below … have *no* table coverage at all | T < f × 1 eV = 0.0536 eV (below the 0.0999350 eV axis floor, so unreachable) |
| nodes of either committed table strictly inside the gap | **0** (asserted) |

**How it is closed:** the pinned PARMA driver is evaluated **directly at every quadrature node**,
with the same anchor scalar `k` the committed tables carry. Neither committed table is
interpolated or extrapolated across the gap — they are used only as *cross-checks*.

**Driver vs both committed tables**, pointwise at each table's own nodes (tolerances reused
unchanged from `09-02` §3.3: median ≤ 1%, max ≤ 5%):

| table | n | median rel. | max abs. rel. | >1% | >5% | pattern |
|---|---|---|---|---|---|---|
| `ambient_neutron_flux_v1.1.csv` | 584 | **−3.876×10⁻⁶** | 3.883×10⁻⁶ | 0 | 0 | the KNOWN uniform anchor-scalar rounding (`k = 1.0961043` unrounded in the committed table vs `1.09610` in the module) |
| `ambient_neutron_thermal_v2.0.csv` | 201 | −3.885×10⁻¹² | 3.483×10⁻¹⁰ | 0 | 0 | CSV round-trip only — this driver *wrote* that table |

The v1.1 deviation pattern is reported, not smoothed over: it is uniform, it matches the
recorded 3.88×10⁻⁶ `k`-rounding explanation of `09-02` §3.3 to better than 20%, and
`flux_overlap_check()["v1.1"]["consistent_with_k_rounding"]` is asserted `True`. No other
deviation pattern is present.

Artifact: **`artifacts/v2.0/neutron_flux_continuity.csv`** (785 overlap rows + 121 driver rows
inside the gap).

---

## 6. The spectrum

Native axis: **2812 log bins at 400 bins/decade**, bottom bin **EDGE exactly 0.0999350 eV** (the
Phase-10 extended-grid floor), top edge `f × 2×10⁷ eV = 1.072×10⁶ eV`. Knots are the geometric
bin centres, so `ia_broadening.native_edges` reproduces the edges exactly — the Phase-12
construction, so the Plan 13-03 floor-coverage assertion holds on the EDGE.

| T [eV] | dR/dT [counts kg⁻¹ day⁻¹ keV⁻¹] |
|---|---|
| 0.10022 | 1.390×10⁷ |
| 0.29923 | 5.311×10⁶ |
| 1.0024 | 2.009×10⁶ |
| 4.9955 | 8.800×10⁵ |
| 10.025 | 1.947×10⁵ |
| 49.963 | 4.222×10⁴ |
| 100.27 | 2.110×10⁴ |
| 1002.9 | 2.155×10³ |
| 9972.6 | 2.479×10² |
| 9.976×10⁵ | 3.325×10⁻² |

Band integrals: **10–100 eV RoI: 4.419×10³ counts kg⁻¹ day⁻¹**; 0.1–1 eV: 3.739×10³;
full axis: 3.130×10⁴.

**Order-of-magnitude context, stated plainly.** The Phase-12 CEvNS spectrum on the same axis is
~2.35×10³ counts kg⁻¹ day⁻¹ keV⁻¹ at 0.1 eV. This neutron channel is **~4 orders of magnitude
larger there**. For an unshielded outdoor surface wafer that is the expected result, not a bug —
but it means the neutron channel, not CEvNS, sets S/B, and Phase 16 must receive it with its
`order_of_magnitude` label attached (`fp-silent-neutron-omission`).

The spectrum is strictly positive and **monotonically non-increasing**, as a suffix integral of a
positive integrand must be. Asserted (`test_spectrum_is_positive_monotone_and_reaches_the_floor`).

Artifact: **`artifacts/v2.0/neutron_dRdT_ge.csv`** (2812 rows; columns `T_eV_nr`, `dRdT`,
`dRdT_smoothed_control`, `dRdT_sub5eV_truncated`, `accuracy_label`). **UNBROADENED** — the IA
kernel is applied downstream, exactly once, in Plan 13-03.

---

## 7. Resonance imprint — ROADMAP SC3 (`test-imprint-present`, `test-imprint-rejects-smooth`)

### 7.1 The statistic and its threshold

```
excursion  =  max_{T in [1, 5.6] eV} |d ln(dR/dT)/d ln T|  -  median_{same band} |...|
```

**Threshold `IMPRINT_EXCURSION_THRESHOLD = 5.0`, declared as a module constant before the run.**
Its justification is analytic, not tuned: in the pure epithermal limit `dR/dT ∝ 1/T`, the slope
is exactly −1 everywhere and the excursion is exactly 0; a smoothly varying flux or cross
section moves the slope smoothly and keeps the excursion of order unity. An excursion above 5
decades-per-decade means the spectrum loses a finite fraction of its integrand inside a small
fraction of a decade, which only a **resolved narrow feature** can do.

### 7.2 Result, and the control that must fail

| spectrum | excursion | max\|slope\| | median\|slope\| | located at | verdict |
|---|---|---|---|---|---|
| **real** | **32.160** | 32.680 | 0.520 | **T = 5.5092 eV** | **PASS** |
| **smoothed-σ control** | **1.143** | 1.788 | 0.645 | 5.573 eV | **FAIL (as it must)** |

Ratio **28.1×**. The control is a *fair* one: it is the same fold, same flux, same sub-5 eV
route, against a σ_el smoothed by a normalised Gaussian of lethargy width 0.35 applied to
`σ·E` in `ln E`. Measured resonance-integral preservation over 0.1 keV – 1 MeV:
∫σ dE = 5.364620×10⁶ → 5.420088×10⁶ b·eV, **+1.034%**, against the declared
`CONTROL_RESONANCE_INTEGRAL_TOL = 5%`.

**Resolution stability** (excludes "the structure is a binning artefact"):

| bins/decade | real | control |
|---|---|---|
| 200 | 25.990 | 1.1419 |
| 400 | 32.160 | 1.1429 |
| 800 | 33.890 | 1.1431 |

The real excursion converges from below (26 → 32 → 34) as the ~1.9%-wide edge is resolved; the
control is flat at 1.14 at every resolution. The verdict is identical at all three
(`test_imprint_statistic_is_resolution_stable`).

**What was tried and rejected.** A log-log **curvature** statistic
`max |d² ln y / d(ln T)²|` gave real = 2242, control = 80.6 with a boxcar smoother — a 28×
separation, but both numbers scale as `1/Δ ln T`, i.e. they are grid-resolution artefacts in
absolute magnitude. It was replaced with the slope excursion, which is resolution-stable. A
boxcar (rather than Gaussian) smoother was also rejected: it left the control with its own
sharp window edges (excursion 1.14 → but slope ≈ −3.2 with visible window structure) and
preserved the resonance integral only to +0.085% while creating spurious local features.

### 7.3 The kinematic edge — measured, not asserted

**73Ge carries the resonance.** At E = 102.59 eV:

| isotope | σ_el [b] | IUPAC abundance | abundance-weighted [b] | own `f = 4A/(1+A)²` | own edge `f·E_res` [eV] |
|---|---|---|---|---|---|
| 70Ge | 11.53 | 0.2057 | 2.372 | 0.055545 | 5.6983 |
| 72Ge | 8.25 | 0.2745 | 2.263 | 0.054044 | 5.5444 |
| **73Ge** | **8533.0** | 0.0775 | **661.31** | **0.053324** | **5.4705** |
| 74Ge | 6.90 | 0.3650 | 2.520 | 0.052622 | 5.3985 |
| 76Ge | 8.20 | 0.0773 | 0.634 | 0.051273 | 5.2601 |
| **sum** | | | **669.096** (header: 669.10) | | |

73Ge carries **98.84%** of the natural peak. Reconstructing 669.096 b from the per-isotope file
× IUPAC abundances against the natural table's own header value 669.10 b is an independent
consistency check on both files, and it passes to 6×10⁻⁶.

**Therefore the edge is NOT a ±4% smeared band.** The plan anticipated smearing across five
isotope box widths; the measurement says otherwise, because a single isotope carries the line:

- **Physically correct edge** (73Ge's own `f`): **5.4705 eV**.
- **Where the single natural `f = 0.0536` puts it**: **5.4988 eV** — high by **+0.52%**.
- The naive all-isotope window [5.2601, 5.6983] eV is the *systematic scale* of using a single
  abundance-weighted `f`, **not** a physical width of this feature.

**Cross-check by an independent fold** (`test_per_isotope_edge_fold_places_the_edge_at_the_carrier_energy`):
folding five per-isotope flat boxes, each with its own `f` and its own σ_el, and locating the
steepest slope at 800 bins/decade:

| fold | located edge | prediction |
|---|---|---|
| five per-isotope boxes | **5.4854 eV** | 5.4705 eV (73Ge) — agrees to 0.27%, i.e. within half a bin |
| single natural `f` (production) | **5.5171 eV** | 5.4988 eV — agrees to 0.33% |

The edge moves **down** by 0.32% when the single-`f` stand-in is replaced by per-isotope boxes,
in the predicted direction and by the predicted amount. The production spectrum's edge is
therefore biased **high by ≈ +0.5%**, i.e. ≈ +0.028 eV — a stated modelling artefact of the
frozen single-`f` flat box, well inside the channel's own accuracy label.

### 7.4 The 293.6 K line-shape question — answered, not deferred

The frozen table's own header warns that Doppler broadening at 293.6 K reshapes resonance PEAKS
while conserving their integrals (73Ge: 9253.7 b at 0.1 K → 8533.0 b at 293.6 K), and that any
downstream use resolving individual LINE SHAPES should re-derive from the 0.1 K `.805nc` set.

**Is this imprint statistic line-shape-sensitive? Measured:**

| quantity | value | source |
|---|---|---|
| observed FWHM of the natural line | **1.923 eV** (1.87% of E) | half-maximum crossings of the frozen table over 95–115 eV, baseline 13.96 b |
| Doppler width `Δ_D = sqrt(4 E kT/A)` at 293.6 K | **0.377 eV** | computed; `kT = 0.02530 eV` |
| the same at 0.1 K | **0.0070 eV** | computed |
| resonance-integral shift 0.1 K → 293.6 K, 0.1 keV–1 MeV | **2.54×10⁻⁴ %** | the frozen table's own validation block |

**Verdict: BAND-INTEGRATED, therefore the 293.6 K processing is ADEQUATE for this claim.**
Three reasons, each measured:

1. The line is **natural-width dominated**: 1.923 eV observed against a 0.377 eV Doppler width,
   so temperature contributes ≲ 4% in quadrature to the width.
2. The excursion's *amplitude* is set by the fraction of the suffix integral the resonance
   carries, i.e. by **∫σ dE**, which Doppler conserves to 2.54×10⁻⁴ %.
3. The excursion's *location* is set by `E_res`, which Doppler does not move at all.

**Direction of the residual sensitivity, stated:** a 0.1 K re-derivation would *narrow* the line
(0.377 → 0.007 eV Doppler contribution), making the edge **sharper** and the excursion
**larger**. The reported 32.16 is therefore the **conservative** value for an existence claim.
It would **not** be adequate for any future claim about the edge's WIDTH or the line SHAPE
itself; that use must re-derive from the 0.1 K set.

---

## 8. Sub-5 eV kernel disposition — ROADMAP SC5, first half

### 8.1 The stake, measured under all three routes before choosing

Incident neutrons below 5 eV produce recoils only below `T = f × 5 eV = 0.268 eV`.

| band | Route A `ncrystal_splice` | Route B `truncate` | forbidden `free_gas` | Route-B omission | free-gas vs Route A |
|---|---|---|---|---|---|
| bottom bin, T = 0.10022 eV (dR/dT) | 1.3900×10⁷ | 5.8548×10⁶ | 1.4385×10⁷ | **−57.88%** | +3.49% |
| T ∈ [0.1002, 0.268] eV | 1439.9 | 974.6 | 1467.4 | **−32.31%** | +1.91% |
| T ∈ [0.1002, 1] eV | 3739.3 | 3274.0 | 3766.8 | −12.44% | +0.74% |
| **T ∈ [10, 100] eV (RoI)** | 4418.963 | 4418.963 | 4418.963 | **exactly 0** | exactly 0 |
| full axis | 31298.7 | 30833.4 | 31326.3 | −1.487% | +0.088% |

(Band rates in counts kg⁻¹ day⁻¹; the RoI row is **identically zero** because the two routes
share the same quadrature node set by construction, so the difference is physics, not grid.)

### 8.2 The escalation rule, evaluated rather than skipped

`test-sub5ev-band-bound`'s pass condition asks for the fraction of the **in-RoI** rate carried
by sub-5 eV neutrons, with escalation if it exceeds ~3× (the channel's own label).

> **The in-RoI fraction is exactly 0, by kinematics rather than by approximation.** A neutron
> below 5 eV cannot produce a recoil above 0.268 eV, so it cannot enter a 10–100 eV RoI at all.
> The escalation rule is therefore not triggered on its stated criterion.

That is a true but uninformative answer for a milestone whose purpose is the sub-eV region, so
the informative number is reported alongside it: **under Route B the bottom bin would lose 57.9%
of its rate (a factor 2.37) and the 0.1–0.268 eV band 32.3%.** A factor 2.37 is *comparable to*
the channel's own order-of-magnitude label — not above it, but close enough that absorbing it
silently would be indefensible in exactly the region this milestone exists to reach.

### 8.3 Route declared: **A — NCrystal `Ge_sg227` splice at 5 eV**

Exactly one route is declared, in the module (`SUB5EV_ROUTE_DECLARED = "ncrystal_splice"`), in
the emitted table header (`sub5eV_disposition = ncrystal_splice`) and here.

**Measured seam discontinuity at 5 eV** (the number Route A is required to report):

| | σ_el at 5.0 eV |
|---|---|
| ENDF/B-VIII.0 free-atom natural | **8.843837 b** |
| NCrystal 4.4.6 `Ge_sg227.ncmat;temp=293.6K` bound-atom | **8.364108 b** |
| **step** | **−5.4244%** |

**The argument, from what was measured in-phase and not from what is convenient:**

1. Route B drops **57.9% of the bottom bin** — measured above, not assumed.
2. Route A's cost is a **−5.42% seam step**, an order of magnitude smaller and confined to the
   cross section rather than to the rate.
3. The residual *model* uncertainty of Route A — bound (NCrystal) versus free-atom (ENDF) σ in
   the only band that matters, `E_n ∈ [1.87, 5] eV` — moves the bottom bin by **+3.49%** and the
   full-axis rate by **+0.09%**. That is far inside the channel's label.
4. NCrystal is evaluated at **293.6 K, matching the frozen ENDF set's own processing
   temperature**, so the measured seam step is a free-vs-bound step and not a temperature step.

**Consistency of the flat box with a bound kernel, checked.** Splicing the *cross section* while
keeping free-atom recoil kinematics is legitimate here because the axis never reaches the
crystal-coherent regime: the lowest incident energy any recoil on this axis needs is
`E_min(0.0999350 eV) = 1.8645 eV`, whose `T_max = 0.0999 eV` is **5.6× the locked phonon scale
ω̄ = 17.8597 meV** (`CONVENTIONS.md` §J). The impulse approximation therefore holds throughout,
and §J's crystal-coherent regime (< ~21 meV) lies entirely **below** the 0.0999350 eV grid floor.
The rate is never multiplied by `exp(−2W)`.

### 8.4 The forbidden third route is provably unused

`fp-free-gas-below-5ev` is enforced in **code**, not by discipline. Every evaluation of the raw
ENDF free-atom interpolator below 5 eV increments a module counter, by any caller.
`test_no_free_atom_evaluation_below_the_seam_reaches_the_spectrum` executes the production fold
under both admissible routes and asserts the counter is **0**, then executes the forbidden route
and asserts the counter is **> 0** — so the guard is shown to be non-vacuous.

The tripwire it protects against is measured, not quoted: the ENDF free-atom 1/v upturn reaches
**59.4274 b** at the bottom of the frozen table (20.63 b already at 10⁻⁴ eV), against ~8.9 b in
the epithermal plateau.

---

## 9. Forward peaking `a1` — reported, never applied

The frozen kernel is the isotropic-CM flat box (Phase 7). `a1_natural` is carried in the frozen
table's third column and is **not** applied. Contribution-weighted `⟨a1⟩` over the integrand
above `E_min(T)`:

| T [eV] | E_min [eV] | contribution-weighted ⟨a1⟩ | max a1 above E_min |
|---|---|---|---|
| 0.1 | 1.87 | 6.04×10⁻⁵ | 0.860 |
| 10 | 187 | 4.15×10⁻⁴ | 0.860 |
| 100 | 1 866 | 3.35×10⁻³ | 0.860 |
| 1 000 | 1.87×10⁴ | 2.70×10⁻² | 0.860 |
| 10⁵ | 1.87×10⁶ | 0.551 | 0.860 |

Global max `a1 = 0.8601` at `E_n = 12 MeV`.

**Direction of the bias.** Forward peaking in the CM tilts `dσ/dT` toward the **low**-T end of
each box, so an isotropic flat box **overstates the high-T end** of every box. Over the RoI the
weighted `⟨a1⟩ ≤ 3.4×10⁻³` and the flat box is essentially exact; the approximation only becomes
material for `T ≳ 10⁵ eV`, three decades above the RoI, where `⟨a1⟩ = 0.55`. Since the flat box
overstates high-T recoils, dropping `a1` **overstates** background at high T — a `penalizes_SB`
direction there, and negligible in the RoI. Reported, not corrected.

---

## 10. Discharge table for Plan 13-01

| acceptance test | outcome | evidence |
|---|---|---|
| `test-oracle` | **PASS** | §2 — 4.65×10⁻⁸ worst deviation, `f`-spread 4.20×10⁻⁸ (≤10⁻³ / ≤10⁻⁵) |
| `test-convergence` | **PASS** | §3 — 1.35×10⁻⁴ on 200→400 (≤0.5%) |
| `test-anchor-loss` | **PASS** | §4 — median −1.14×10⁻³, signed, non-zero, worst-case −14.6% for the plain-grid proxy |
| `test-dimensions` | **PASS** | §1 — four named constants, linearity to 10⁻¹² |
| `test-imprint-present` | **PASS** | §7.2 — excursion 32.16 > 5.0, located at 5.5092 eV, inside [5.2601, 5.6983] eV |
| `test-imprint-rejects-smooth` | **PASS** | §7.2 — control 1.143 < 5.0; ratio 28.1×; control preserves ∫σ dE to +1.03% |
| `test-edge-smearing` | **PASS** | §7.3 — 73Ge named (98.84%), edge 5.4705 eV vs single-`f` 5.4988 eV, per-isotope fold confirms |
| `test-no-freegas-below-5ev` | **PASS** | §8.4 — executed counter = 0 on both admissible routes, > 0 on the forbidden one |
| `test-sub5ev-route-declared` | **PASS** | §8.3 — one route, seam step −5.4244% reported |
| `test-sub5ev-band-bound` | **PASS** | §8.2 — in-RoI fraction exactly 0; Route-B stake 57.9% of the bottom bin reported with sign |
| `test-flux-overlap` | **PASS** | §5 — median 3.88×10⁻⁶ / 3.88×10⁻¹², 0 bins over 1% or 5%, k-rounding pattern confirmed |
| `test-gap-closed` | **PASS** | §5 — 0 committed-table nodes inside the gap; driver covers it; `E_min(T)` for T ≤ 0.54 eV lands inside it |

---

## 11. What still cuts against this result

- **The eV–keV flux shape has no independent validation and none is obtainable here.** That band
  sets the whole spectrum. Everything above inherits `order_of_magnitude` from it. Plan 13-03's
  error budget must demonstrate this by measurement rather than restate it.
- **The single-`f` flat box biases the kinematic edge high by ≈ +0.5%.** Measured (§7.3), not
  corrected — correcting it would mean abandoning the frozen Phase-7 kernel.
- **293.6 K against a mK target.** Adequate for an existence claim about the imprint (§7.4),
  inadequate for any claim about the edge's width.
- **NCrystal's bound kernel is used only in its high-energy tail** (1.87–5 eV). It is the right
  cross section there, but it is a *different evaluation* from the ENDF set above the seam, and
  the −5.42% seam step is the honest measure of that.
- **The 20 MeV σ_el ceiling is still open here.** Plan 13-02 bounds it.
