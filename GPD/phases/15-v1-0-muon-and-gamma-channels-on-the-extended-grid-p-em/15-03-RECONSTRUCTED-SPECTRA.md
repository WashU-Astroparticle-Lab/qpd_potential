# 15-03 — Reconstructed-energy spectra for both electron-recoil channels, both designs

**Plan:** 15-03 · **Phase:** 15 · **Date:** 2026-07-23
**Interpreter:** `/opt/anaconda3/bin/python3` (numpy 1.26.4, scipy 1.17.1, matplotlib 3.8.0)
**Repo HEAD at execution:** `53ed2d6`

Figure: `artifacts/v2.0/em_subev_spectra.pdf`

---

## 1. The electron-recoil fold path and its five guards

`fold.run_em_fold_extended(channel, design, ...)`, appended to `fold.py` so no
earlier line number moved, modelled structurally on `run_neutron_fold_extended`.

**The one structural difference:** these channels are **already on the deposit
axis**. There is no recoil-to-deposit rebin, so the neutron path's recoil-table
floor-coverage assertion is replaced by a **direct grid-identity assertion** of the
input's 744 centres against the matrix's own `E_dep_centers_eV` (1e-6 relative).

| # | Guard | Behaviour | Test |
|---|---|---|---|
| 1 | **744-column shape check** | raises naming 584 and 744 | `test_shape_check_raises` |
| 2 | **Applicability** — Plan 15-01 verdict read from `em_recoil` **at fold time**, not hard-coded | raises `ElectronRecoilBroadeningError` carrying the verdict, the reason and `fp-transplant-nuclear-width` | `test_applicability_guard_raises` |
| 3 | **Double broadening** — `read_broadened_provenance` + `DoubleBroadeningError`; a table declaring **nothing** raises too | raises | `test_double_broaden_raises` |
| 4 | **Non-finite input** — `NonFiniteDepositError` unless an explicit policy is passed | raises; the policied call records the excluded count in the output header | `test_nan_guard_raises` |
| 5 | **Grid identity** (replaces floor-coverage) | raises on a bin-count or centre mismatch | `test_shape_check_raises` |

Plus `test_columns_sum_to_one`: the matrices' columns are asserted to sum to 1
**before** folding, so the conservation residual is a real numerical check on the
fold rather than a measurement of the matrix.

**No `np.nan_to_num` anywhere in the path.** The module names it twice — in the
guard message and in the docstring — precisely so the prohibition is discoverable
at the point of temptation, and `test_no_nan_to_num_in_the_fold_path` scans every
executable line. `NO_SUPPORT_POLICIES` is `("raise", "exclude_and_record")`; there
is **no zero-fill member and there never will be**, and the test asserts that.

### 1.1 Counts budget

| channel | design | deposit counts | reconstructed counts | `residual_fold` | excluded bins |
|---|---|---|---|---|---|
| muon | Ta→Al | 1073206.424523 | 1073206.424523 | **0.000e+00** | 35 |
| muon | Al→Hf | 1073206.424523 | 1073206.424523 | **2.169e-16** | 35 |
| Compton | Ta→Al | 210277.108948 | 210277.108948 | **1.384e-16** | 69 |
| Compton | Al→Hf | 210277.108948 | 210277.108948 | **1.384e-16** | 69 |

ROADMAP SC2 requires ≤ 1e-3. The measured residuals are at floating-point level,
**thirteen decades inside** the bar.

**`residual_retained_plus_leaked` and `residual_retained_only` are both 0.0, and
they COINCIDE BY CONSTRUCTION** — no broadening is applied to an electron-recoil
channel (Plan 15-01 verdict `does_not_apply`), so there is no kernel leakage for a
retained-only residual to miss by. The budget carries the explicit field
`residuals_coincide_because_no_broadening = True` so the coincidence is stated
rather than presented as two independent confirmations. This is the one place where
the electron-recoil path *should* look different from the neutron path, where the
retained-only residual must miss by −7.663e-3.

**The excluded bins are the Plan 15-02 NaN no-support bins** (35 muon, 69 Compton).
They are dropped from the fold under the recorded policy `exclude_and_record` and
their count is written into both output headers. They are never zero-filled: that
would convert an absence of measurement into a measured absence, spread by a dense
`R` across every reconstructed bin.

---

## 2. The trigger, and the composition proof

`P_trig` is applied on the **deposit** axis, column-wise on `N_dep` before `R` acts,
because the analysis efficiency is a per-event property of the deposit. It
**multiplies** ε ≈ 0.5, which lives inside the un-triggered quantity through
`energy_scale.n_qp_yield` and `response.calibrate_C`; it never replaces it.

**Composition proved, not assumed.** With `p_trig_override` of all ones:

| channel | design | max \|triggered − untriggered\| | `np.array_equal` |
|---|---|---|---|
| muon | Ta→Al | **0.0** | True |
| muon | Al→Hf | **0.0** | True |
| Compton | Ta→Al | **0.0** | True |
| Compton | Al→Hf | **0.0** | True |

Bit-identical, for the counts array and the differential alike.

**CONVENTIONS §I hand values reproduce exactly** at k = 4: `P(0) = 0.0`,
`P(0.25 eV) = 1/17 = 0.058823529411764705`, `P(0.5 eV) = 0.5`,
`P(1.0 eV) = 16/17 = 0.9411764705882353`. And `P(E50) = 1/2` holds at **k = 1, 4
and 12** — structural, not tuned.

**Regime boundary imported, never a literal.** `trigger.SUBEV_REGIME_BOUNDARY_eV`
= 1 eV **deposited**, imaged onto each design's reconstructed axis by the response
matrix's **own median mapping curve** (`fold.subev_boundary_Erec_eV`), never assumed
to be 0.5 × anything:

* Ta→Al: **0.497240 eV** reconstructed
* Al→Hf: **0.495855 eV** reconstructed

Both happen to land near half the deposit boundary, but the test asserts the value
is the interpolated one and *not* `0.5 × 1.0 eV` — the near-coincidence is a
property of the response chain at that energy, not an assumption fed into it.

---

## 3. k-sensitivity — every triggered quantity, over the declared range

`artifacts/v2.0/em_trigger_k_sensitivity.csv`, 12 rows (2 designs × 2 channels × 3
quantities), each evaluated at **k = 1, 2, 3, 4, 6, 8, 10, 12** spanning
`params.TRIGGER_SHARPNESS_RANGE = [1.0, 12.0]`. The spread is reported as a
**range**, never as a plus-or-minus: a symmetric error bar would misrepresent an
unmeasured *chosen* parameter as a measured one.

| design | channel | quantity | un-triggered | range over k ∈ [1, 12] | hi/lo |
|---|---|---|---|---|---|
| Ta→Al | muon | total | 1.0732e+06 | 1.0732e+06 … 1.0732e+06 | 1.000 |
| Ta→Al | muon | sub-eV | 1.4695e-02 | 6.6602e-03 … 7.3203e-03 | **1.099** |
| Ta→Al | muon | RoI 10–100 eV | 7.4656e+00 | 7.4272e+00 … 7.4656e+00 | 1.005 |
| Ta→Al | Compton | total | 2.1028e+05 | 2.1028e+05 … 2.1028e+05 | 1.000 |
| Ta→Al | Compton | sub-eV | 2.8587e-03 | 1.7426e-03 … 2.4033e-03 | **1.379** |
| Ta→Al | Compton | RoI 10–100 eV | 3.4248e+01 | 3.4098e+01 … 3.4248e+01 | 1.004 |
| Al→Hf | muon | total | 1.0732e+06 | 1.0732e+06 … 1.0732e+06 | 1.000 |
| Al→Hf | muon | sub-eV | 1.4744e-02 | 6.6947e-03 … 7.3694e-03 | **1.101** |
| Al→Hf | muon | RoI 10–100 eV | 7.7231e+00 | 7.6844e+00 … 7.7231e+00 | 1.005 |
| Al→Hf | Compton | total | 2.1028e+05 | 2.1028e+05 … 2.1028e+05 | 1.000 |
| Al→Hf | Compton | sub-eV | 3.0152e-03 | 1.8476e-03 … 2.5597e-03 | **1.385** |
| Al→Hf | Compton | RoI 10–100 eV | 3.5862e+01 | 3.5709e+01 … 3.5862e+01 | 1.004 |

(all in counts kg⁻¹ day⁻¹)

**The question the plan required an answer to — is the sub-eV observable dominated
by the unmeasured k? — is ANSWERED, and the answer is NO.** The sub-eV
trigger-weighted rate varies by **1.10×** (muon) and **1.39×** (Compton) across the
full declared range, well under the order of magnitude that would make it a
parameter scan rather than a prediction. This is a measurement, not an assumption:
the disconfirming observation "the trigger-weighted sub-eV spectrum varies by more
than an order of magnitude across k" was checked and **did not fire**.

**Why the totals are insensitive:** both spectra are overwhelmingly dominated by
deposits far above E50 = 0.5 eV, where `P_trig → 1` for every k. The trigger costs
essentially nothing on the total and only a factor ~2 on the sub-eV rate.

**No triggered quantity is quoted anywhere without its k.** Both emitted tables'
headers state `trigger k = 4.0 (DEFAULT)`, that k is fixed by no project artifact,
that every triggered number is a one-parameter family over `[1, 12]`, and that a
triggered quantity quoted without its k is `fp-hardcoded-width`. The figure's
legend carries `k=4, range [1,12]` on every trigger-weighted curve.

---

## 4. Saturation — preserved, and **instrumental**

**The muon reconstructed peak is an INSTRUMENTAL pile-up feature. It is not a physical line.** Its mechanism is the **40 µs non-paralyzable resolving time**
(`deposited_spectra.RESOLVE_TIME_S = 4e-5 s`, the 25 kHz Nyquist of the 50 kHz
bandwidth; CONVENTIONS §F, resolved by user decision at the Phase-5 review).

| design | muon peak `E_rec` | dominant deposit | median `E_rec` of that deposit | **compression** | ceiling: `E_rec` at the top deposit bin (197 MeV) |
|---|---|---|---|---|---|
| Ta→Al | **18.8365 keV** | 1.4354 MeV | 18.6140 keV | **77.1×** | 34.7635 keV |
| Al→Hf | **14.9624 keV** | 1.4354 MeV | 14.1659 keV | **101.3×** | 26.8449 keV |

The deposit spectrum peaks at **1.44 MeV** — the Landau MPV of a near-vertical
chord. A linear ε ≈ 0.5 map would place that at ~0.7 MeV reconstructed. It appears
at **18.8 / 15.0 keV** instead: compressed by 77× and 101×. The whole 197 MeV top
of the deposit axis maps to only 34.8 / 26.8 keV. **The reconstructed peak does not
track the deposit energy** — that is exactly what `test_saturation_peak` asserts,
and it is the check that would catch the saturation being lost in the re-grid.

Per-design saturation onsets from the Phase-10 matrices: **52.9074 eV** (Ta→Al) and
**32.1300 eV** (Al→Hf) deposited, with whole-array plateaus at 18.638 keV and
11.319 keV. The Ta→Al onset is the higher of the two, as the design implies.

**The feature is described as instrumental with its mechanism named in the report,
in both table headers, and in the figure annotation. It is nowhere presented as a
physical line or as a spectral feature of the muon channel** (`fp-saturation-as-line`,
ROADMAP SC2).

### 4.1 Pile-up occupancy — recomputed, and it **differs from the v1.0 quote**

Recomputed with `deposited_spectra.pileup_occupancy` from the through-wafer rates
(muon 1.365914 Hz, Compton 0.2674705 Hz) rather than quoted:

```
R      = 1.633385 Hz        (muon + Compton, through-wafer, ABSOLUTE)
tau_d  = 4.0e-05 s          (40 us, the CANONICAL non-paralyzable resolving time)
R*tau  = 6.533538e-05       <-- recomputed
stop_condition_triggered = False
```

**This is a finding and is reported rather than reconciled silently.** The v1.0
manuscript quotes `Rτ ≈ 3×10⁻⁵`. The recomputed value with the canonical τ = 40 µs
is **6.5335e-05**, a factor of exactly **2** above it. The reason is identifiable
and is not a discrepancy in the rate: with the **20 µs sampling** time instead,
`R × 2e-5 = 3.266768e-05 ≈ 3×10⁻⁵`. **The v1.0 ~3e-5 is the sampling-time
occupancy, not the resolving-time occupancy** — precisely the conflation
CONVENTIONS §F's Numerical Factor Registry names by row: *"Resolving time | 40 µs
(25 kHz Nyquist) | 20 µs (50 kHz sampling) conflated"*.

Both numbers are asserted in `test_pileup_occupancy_is_recomputed_not_quoted`
together with their exact factor-2 relation, so neither can drift and the
distinction cannot be lost again.

**The physical conclusion is unchanged:** at 6.5e-05 the occupancy is still four
decades below the 1e-2 stop threshold, so muon pile-up does not preclude quiescent
operation. What changed is the number, and which timescale it belongs to.

---

## 5. The sub-eV reconstructed region — what it does and does not support

Applying **both** Plan 15-01's validity floors and Plan 15-02's adequacy labels:

**Muon.** Plan 15-02 recorded that not one of the 160 sub-eV deposit bins reaches
`adequate_mc_support`, that 35 have no support at all, and that **all 160 lie below
the Landau–Vavilov validity floor of 4111.82 eV** — indeed 369 of the 744 extended
bins do. Folding that through `R` does not create information. **The muon sub-eV
reconstructed region supports nothing that may be quoted as a rate.** Its
trigger-weighted content is 1.47e-02 counts/kg/day (Ta→Al) — a number the fold
produces from deposit bins that are simultaneously outside the model's domain and
statistically empty. It is carried into Phase 16 as a **named gap**, not as a
background estimate.

**Compton.** 91 of 160 sub-eV deposit bins have support, 7 reach
`adequate_mc_support`, and **70 of 160 lie below the adopted Ge pair-creation floor
of 0.73955 eV**. Between 0.73955 eV and 10.14 eV the physics is in-domain and the
estimator has partial support, so a *bounded* statement is possible there; below
0.73955 eV nothing may be quoted as a physical rate whatever the estimator returned
(Plan 15-01 §4.2, `fp-suppressed-means-valid`).

**The three competing explanations for a sub-eV reconstructed rate** — genuine
leakage of the deposit tail through the response chain, the matrix's own sub-eV
columns redistributing counts from unsupported bins, and the trigger shoulder
shaping noise — are **not resolved by the fold**, and the honest position is that
the regime flag, the adequacy label and the k-sensitivity together are what a
consumer must read before quoting one. The k-sensitivity is now measured (1.10×,
1.39×), so the third explanation is *not* dominant; the first two remain
entangled, and the validity floors exclude the region regardless.

---

## 6. Bands and labels, carried forward unnarrowed

Both tables carry, on every row: `muon_accuracy_label` and `gamma_accuracy_label`
in full, plus per-channel band columns.

* **muon band = ×0.65 … ×1.35** — the **30–35 % inter-experiment Gaisser–Guan
  normalization spread**, named in the v1.0 manuscript as this channel's weakest
  anchor. It **encloses** the PDG Leg A / Leg B bracket ×0.8309 … ×1.2595, so
  choosing it narrows nothing. Asserted in `test_labels_and_bands_reach_the_reconstructed_tables`.
* **Compton band = ×0.5 … ×2** — the factor-2 site band, with the note that the low
  edge is the flattering one and is not used.
* The muon label always carries **Leg A, Leg B, −20.61 %, +20.34 % and the word
  BRACKET**; a bare −20.61 % appears nowhere (`fp-bare-sign`).

---

## 7. In-band orientation (handed to Plan 15-04, not concluded here)

Un-triggered reconstructed rates over `E_rec` 10–100 eV:

| | Ta→Al | Al→Hf |
|---|---|---|
| muon | 7.4656 | 7.7231 |
| Compton | 34.248 | 35.862 |

(counts kg⁻¹ day⁻¹). The Compton continuum exceeds the muon channel by ~4.6× in
that band, consistent in direction with the v1.0 conclusion. **The dominance
re-check with the CEvNS and neutron comparisons is Plan 15-04's deliverable and is
not concluded here**; these two numbers are stated so 15-04 does not re-derive them.

---

## 8. Verification ledger

| Acceptance test | Outcome | Evidence |
|---|---|---|
| `test-shape-check-raises` | **PASS** | raises naming 584 and 744 |
| `test-applicability-guard-raises` | **PASS** | named exception, verdict read at fold time |
| `test-double-broaden-raises` | **PASS** | `true` and undeclared both raise |
| `test-nan-guard-raises` | **PASS** | unpolicied raises; policied records 35 / 69 excluded |
| `test-counts-conservation` | **PASS** | residual_fold ≤ 2.2e-16 vs the 1e-3 bar |
| `test-columns-sum-to-one` | **PASS** | both matrices, atol 1e-9 |
| `test-ptrig-identity-one` | **PASS** | exactly zero difference, `np.array_equal` |
| `test-ptrig-test-values` | **PASS** | §I values exact; `P(E50)=1/2` at k = 1, 4, 12 |
| `test-regime-boundary-imported` | **PASS** | imported; image read off the median curve; flags agree |
| `test-both-designs` | **PASS** | both exist, not copies, onsets 52.91 / 32.13 eV |
| `test-saturation-peak` | **PASS** | peak 18.84 / 14.96 keV vs 1.44 MeV deposit; 77×/101× |
| `test-pileup-occupancy` | **PASS (finding: 6.5335e-05, not ~3e-5)** | §4.1 |
| `test-peak-not-physical-line` | **PASS** | named instrumental in report, headers and figure |
| `test-k-range-covered` | **PASS** | k = 1…12, spread as a range |
| `test-no-bare-triggered-number` | **PASS** | headers, figure legend and report all carry k |
| `test-dimensions` | **PASS** | `dRdErec * dE == N_rec` to 1e-12; P_trig ∈ [0,1] |

**Forbidden proxies.** `fp-nan-to-num` rejected (no executable occurrence; the
policy is explicit and recorded on the output). `fp-transplant-nuclear-width`
rejected (the guard raises and the verdict is read, not baked in).
`fp-trigger-replaces-efficiency` rejected (`P_trig ≡ 1` reproduces the chain
bit-for-bit; the trigger acts on the deposit axis). `fp-hardcoded-width` rejected
(k-sensitivity frozen, no bare triggered number). `fp-exp-minus-2W` rejected (no
`np.exp(-2` in the section; the only mentions are prohibitions).
`fp-saturation-as-line` rejected (§4). `fp-shielded-quantity-leak` rejected
(Phase-9 token scan over both tables and the k-sensitivity table, zero applied
hits).

---

## 9. Uncertainty markers

**Weakest anchors.** k is fixed by no project artifact and no trigger threshold has
ever been measured for this device — now quantified: the sub-eV observable moves by
1.10×/1.39× over the full declared range. The muon channel has **no external
benchmark on the reconstructed axis at all** (the NUCLEUS Table 5 comparison was
removed by the re-scope). ε ≈ 0.5 is a project-imposed forward-model definition with
a ±10–20 % design-dependent band sitting underneath every number here. Whatever
sub-eV content survives is folded through response-matrix columns themselves built
two decades below the v1.0 validated range.

**Unvalidated assumptions.** Whether the sub-eV deposit bins were worth folding at
all: Plan 15-01's floors and Plan 15-02's adequacy labels together exclude the muon
sub-eV region entirely and the Compton region below 0.73955 eV, so the fold's job
there was to make the exclusion visible rather than to produce a curve, and that is
what §5 records. Saturation stability under the re-grid was **checked, not assumed**.

**Disconfirming observations.**
* ❌ did not fire — the counts residual is 2e-16, not above 1e-3.
* ❌ did not fire — the muon peak stays at the instrumental ceiling (77×/101×
  compression) and does not track the deposit energy.
* ❌ did not fire — `P_trig ≡ 1` reproduces the un-triggered chain bit-for-bit.
* ❌ did not fire — the sub-eV triggered rate varies by only 1.10×/1.39× across
  k ∈ [1, 12], so it is not dominated by the unmeasured parameter.
* ✅ **FIRED** — the recomputed pile-up occupancy is **6.5335e-05**, a factor 2
  above the v1.0 quoted ~3e-5, because the v1.0 figure is the **20 µs sampling**
  occupancy rather than the **40 µs resolving-time** occupancy. Reported as a
  finding with both numbers and their exact relation asserted.
