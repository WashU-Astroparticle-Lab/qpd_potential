# 13-03 — The Ge Neutron NR Spectrum in Reconstructed Energy, and the Phase-13 Closeout

**Plan:** 13-03 (wave 3) · **accuracy_label = `order_of_magnitude`** on every quantity below.
**Interpreter:** `/opt/anaconda3/bin/python3`. **Tests:** `tests/test_neutron_fold.py` (22 passed).
**Modules:** `src/qpd_potential/fold.py` (appended neutron-only extended path),
`src/qpd_potential/neutron_recoil.py` (appended 13-03 section).

**Reproduce:**
```
PYTHONPATH=src /opt/anaconda3/bin/python3 -c "from qpd_potential import neutron_recoil as n; \
  n.write_ext_dRdT_table(); n.write_ext_spectrum('Ta->Al'); n.write_ext_spectrum('Al->Hf'); \
  n.write_error_budget(); n.make_spectra_figure()"
PYTHONPATH=src /opt/anaconda3/bin/python3 -m pytest -q tests/test_neutron_fold.py
```

---

## 1. The chain, and where each guard sits

```
native dR/dT (Plan 13-01, UNBROADENED, broadened_provenance = false)
   |
   |-- fold.read_broadened_provenance  -> DoubleBroadeningError if the table says
   |     "true", or says NOTHING.  Phase 12 recorded that nothing in the codebase
   |     caught this; the guard is now code, and it is tested by trying it.
   v
IA Gaussian broadening on the RECOIL axis, applied EXACTLY ONCE
   |    omega_bar = 1.7859677040e-02 eV, the LOCKED harmonic VDOS mean.
   |    ia_broadening.BROADENING_DEFAULT is still False; broaden=True at this call
   |    site only.  The rate is NEVER multiplied by exp(-2W).
   v
counts-conserving log-log rebin onto the 744-bin extended DEPOSIT grid
   |    744-column shape guard; floor coverage asserted on the bottom bin EDGE.
   v
R(E_rec|E_dep), the Phase-10 extended response matrices
   |    R's columns sum to 1, so the fold conserves counts exactly.
   v
trigger P(E) = 1/(1+(E50/E)^k), E50 = 0.5 eV, on the DEPOSIT axis, MULTIPLYING eps
```

**`shared_energy_grid` still DEFAULTS to `v1.0`.** `DEFAULT_GRID_VERSION` is authoritative and
reads `"v1.0"`; the `muon_deposit.shared_energy_grid` docstring calling `v2.0-ext` "the default"
is **wrong** and is recorded here rather than silently relied on. The extended axis is opt-in and
is taken from the `_ext.npz` matrices, which is what the 744-column guard checks.

**A floor detail, reported rather than smoothed over.** The Phase-10 deposit floor is exactly
`0.09993504432008875 eV`; the value quoted throughout the project, and used to build the native
recoil axis, is the rounded `0.0999350 eV`. The native axis's bottom bin edge therefore sits
`4.4×10⁻⁸ eV` (4.4×10⁻⁷ relative) **below** the deposit floor — the safe direction, so the
floor-coverage assertion passes on the EDGE.

**IA applicability, stated rather than assumed.** The IA width is a NUCLEAR-recoil width. Neutron
elastic recoils are nuclear recoils, so the kernel applies here on the same footing as CEvNS. That
is **asserted from the shared nuclear-recoil character**; the Phase-11 derivation was carried out
for the CEvNS channel and is not re-derived here. Phase 15's **electron**-recoil channels are a
separate question and are not settled by this.

**No resample was needed, and that is measured.** The Plan 13-01 native axis was already built as
log bins whose bottom EDGE is the extended-grid floor with knots at the geometric bin centres, so
`ia_broadening.native_edges` of those knots reproduces the axis edges exactly. Re-gridding onto a
coarser axis would only have discarded the resonance resolution SC3 rests on.

**Two rebin implementations, kept from drifting.** `rebin_recoil_arrays_to_edep_grid` takes arrays
rather than the fixed 8-column CEvNS CSV layout. `test_array_rebin_reproduces_the_cevns_path_bit_identically`
asserts it reproduces `rebin_cevns_to_edep_grid` **bit-identically** on the Phase-12 CEvNS table.

---

## 2. Counts budget — ROADMAP SC1

Identical for both designs, because `R`'s columns each sum to 1: the design moves counts, it does
not create them.

| quantity | value |
|---|---|
| `input_counts` | **31 303.03** counts kg⁻¹ day⁻¹ |
| `leaked_below_floor` | 238.008 (**0.760335%** of input) |
| `leaked_below_zero` (a SUBSET) | 3.246 (**0.010370%**) |
| `leaked_above_top` | 0.000 |
| `deposit_counts` | 31 063.15 |
| `reconstructed_counts` | 31 063.15 |
| **`residual_retained_plus_leaked`** | **5.969166×10⁻⁵** — **CLOSES**, against SC1's 10⁻³ |
| **`residual_retained_only`** | **−7.663038×10⁻³** — **MISSES**, as it must |
| `residual_fold` | **0.000000** — exact |

**SC1's budget ambiguity, resolved explicitly rather than glossed.** ROADMAP SC1 asks for "count
conservation ≤ 1e-3 through the fold and the response chain" without naming a budget. It **cannot**
hold as literally read on a retained-only budget: Phase 11 established that roughly half the 100 meV
bin's kernel genuinely leaves the axis, and this channel's spectrum reaches that bin. It is
therefore discharged on **retained + leaked**, and the retained-only miss is reported alongside it.

**A retained-only residual that also closed would be evidence of a hidden rescale, not of
conservation** (`fp-renormalize-leakage`). The miss is checked against the leakage rather than
merely observed: `−(leaked_below + leaked_above)/input = −7.603×10⁻³` against the measured
`−7.663×10⁻³`, agreeing to 0.79% — the residual difference being the quadrature gap between the
native-edge sum used for `input_counts` and the exact CDF convolution.

**Nothing is renormalized, and that is enforced by a test no post-hoc rescale can pass:**
scaling the input by an arbitrary 3.7 scales every output bin and every leakage entry by exactly
3.7, to 4.9×10⁻¹⁰ (`test_leakage_is_reported_not_renormalized`).

**Bottom-bin record (CONVENTIONS §J: the least reliable number in the milestone).**

| quantity | this axis | CONVENTIONS §J / Phase 11 (480-bin CEvNS axis) |
|---|---|---|
| bottom-bin kernel leakage below the floor | **49.728332%** | 48.980311% |
| bottom-bin leakage to unphysical `T < 0` | **0.892049%** | 0.869608% |
| `sigma_E` at the bottom-bin centre | 0.042308 eV at 0.1002231 eV | 0.042476 eV at 0.1010208 eV |

The two are **not** expected to agree digit for digit and the difference is explained rather than
absorbed: this axis has 400 bins/decade (0.577%/bin) against the Phase-11/12 axis's ~68/decade, so
the bottom bin is narrower, its centre sits lower, and a larger fraction of its symmetric Gaussian
falls below the same floor. The magnitude and the skewness caveat carry over unchanged.

---

## 3. The trigger composes, it does not replace — ROADMAP SC1 / CONVENTIONS §I

`P_trig == 1` reproduces the untriggered spectrum **bit-identically** for both designs
(`np.array_equal`, not `allclose`), which is what proves the trigger multiplies `eps` rather than
replacing it (`fp-trigger-replaces-eps`). The curve is evaluated on the **DEPOSIT** axis, before
`R` acts, per the Phase-12 composition lock; evaluating it on the reconstructed axis would silently
move the 0.5 eV 50% point by the ~0.47 response slope, i.e. amend CONVENTIONS §I without saying so.

| design | untriggered | trigger-weighted | sub-eV boundary (E_rec image of 1 eV deposited) |
|---|---|---|---|
| Ta→Al, `E_rec` 10–100 eV | **5430.287** | 5430.286 | 0.497240 eV |
| Ta→Al, `E_rec` < 1 eV | 5121.316 | **2852.040** | " |
| Ta→Al, total | 31 063.151 | 28 790.977 | " |
| Al→Hf, `E_rec` 10–100 eV | **5485.152** | 5485.151 | 0.495855 eV |
| Al→Hf, `E_rec` < 1 eV | 5126.231 | **2856.909** | " |
| Al→Hf, total | 31 063.151 | 28 790.977 | " |

(counts kg⁻¹ day⁻¹.) The trigger costs **44.3%** of the sub-eV rate and **7.3%** of the total, and
essentially nothing in the 10–100 eV RoI, where `P_trig → 1`.

---

## 4. Error budget — ROADMAP SC2, established by measurement on both sides

### 4.1 Kernel side — numbers that exist

`sigma_el` enters the fold **linearly**, so a uniform fractional perturbation moves the in-RoI rate
by exactly that fraction. These rows are identities of the fold, and they are checked as such.

| term | perturbation | source | in-RoI relative change | bounded? |
|---|---|---|---|---|
| σ_el mesh convergence | 0.1117% uniform | frozen table header, max over isotopes, 0.1 keV–1 MeV | **+1.117×10⁻³** | bounded |
| σ_el Doppler sensitivity | 2.54×10⁻⁴% | frozen table header, 293.6 K vs 0.1 K | +2.540×10⁻⁶ | bounded |
| σ_el ACE vs MF=3 MT=2 | 3.96×10⁻⁵% | frozen table header, 1.1–20 MeV | +3.960×10⁻⁷ | bounded |
| ω̄ harmonic → arithmetic (Ta→Al) | 1.785968×10⁻² → 2.419553×10⁻² eV | CONVENTIONS §J locked band | **−1.089×10⁻⁶** | bounded |
| ω̄ harmonic → arithmetic (Al→Hf) | " | " | −4.400×10⁻⁵ | bounded |

(The ω̄ rows are real re-folds through broadening, the rebin and the response chain, not scalings.
Their total-rate leg is −1.256×10⁻³, and the wider kernel raises the below-floor leakage from
238.008 to 277.074 counts kg⁻¹ day⁻¹ — "upper" refers to the WIDTH, not to the rate.)

**Every kernel-side term lands between 4×10⁻⁷ and 1.1×10⁻³.**

### 4.2 Flux side — a number that does not exist, demonstrated rather than asserted

Two **explicit** shape perturbations were constructed, each multiplying `phi` by a factor that is
**exactly 1 above 10 MeV**, so the >10 MeV Gordon integral is preserved identically and the only
independent cross-check this channel owns is blind to them by construction.

| perturbation | construction | in-RoI rate change | >10 MeV integral change | detectable? |
|---|---|---|---|---|
| `bump` | ×(1 + lognormal centred at 100 eV, `sigma_lnE = 2`, amplitude +100%), below 10 MeV | **+41.33%** | **+0.000×10⁰** | **no** |
| `tilt` | ×(lethargy tilt `E^{−0.05}` ramped to 1 at 10 MeV) | **−16.31%** | **+0.000×10⁰** | **no** |

The Gordon range's own half-width is **1.41%** (3.5–3.6×10⁻³ cm⁻² s⁻¹), so a perturbation would
have to move that integral by more than 1.41% before the cross-check could even in principle see
it. These move it by **zero**.

The two point in **opposite directions**, so this is not a one-sided artefact of one construction.

### 4.3 The asymmetry IS the finding

This is not a budget of two numbers where one is bigger.

- The **kernel** term is **BOUNDED** at 4×10⁻⁷ – 1.1×10⁻³ by measurements this project performed
  and that live in the frozen table's own validation block.
- The **flux** term is **UNBOUNDED by available evidence**. `09-02` §3.4 records that Gordon's
  differential coefficients are paywalled, that no differential validation of the eV–keV shape
  exists, and that two spectra can share the >10 MeV integral and differ badly there. The two
  perturbations above are **lower witnesses**, not an estimate: their amplitudes were *chosen*, and
  nothing in the evidence bounds them.
- Ratio at the smallest witness: **16.31% / 0.1117% ≈ 146×**, and against the largest ω̄ leg
  (4.4×10⁻⁵) it is ~3700×.

The CSV marks the flux row **UNBOUNDED** rather than carrying a plausible-looking figure, and **no
integral-level number is entered as a differential error bar** — in particular the untuned
PARMA-vs-Gordon offset, which is an integral agreement above 10 MeV, appears nowhere in the budget
as an uncertainty (`fp-manufactured-flux-uncertainty`).

**The disconfirming outcome did not occur, and is recorded anyway.** Plan 13-03's contract names
"the Gordon-preserving perturbations barely move the in-RoI rate" as an observation that would
*undermine* `claim-flux-dominates` and suggest the order-of-magnitude label is more conservative
than the evidence requires. It was checked and it is false: the rate moves by tens of percent under
perturbations the cross-check cannot see.

---

## 5. Does the resonance imprint survive onto the reported observable?

The real spectrum and the smoothed-σ CONTROL were folded through the **identical chain**, so a
difference between them cannot be a chain artefact. The statistic and its threshold are the
**Plan 13-01 ones, unchanged**: slope excursion, threshold 5.0.

| stage | bin width | real excursion | verdict | control | contrast max\|real/ctrl − 1\| |
|---|---|---|---|---|---|
| recoil axis, unbroadened | 0.577% | **32.160** at 5.5092 eV | PASS | 1.143 FAIL | 54.5% |
| recoil axis, after IA broadening | 0.577% | **6.531** at 5.5730 eV | PASS | 1.128 FAIL | 40.2% |
| deposit axis (744 bins) | 2.920% | **6.113** at 5.5426 eV | PASS | 1.123 FAIL | 39.7% |
| **reconstructed axis (161 bins)** | **12.202%** | **3.383** (Ta→Al) / **3.598** (Al→Hf) at 2.6607 eV | **FAIL** | 1.091 / 0.973 FAIL | 33.4% / 34.6% |

> **Verdict: the imprint SURVIVES broadening and the deposit rebin, and is WASHED OUT on the
> RECONSTRUCTED axis by the pre-declared statistic.**

**The washout is quantified, not asserted.** Statistic: 32.160 → 3.383, a factor **9.51×**
(Ta→Al) / **8.94×** (Al→Hf). Amplitude contrast: 54.5% → 33.4%, a factor **1.64×** / **1.58×**.

**The three causes, each with its own number:**
1. IA broadening: `sigma_E/E = sqrt(E ω̄)/E = 5.70%` at the 5.5 eV edge, against a feature whose
   own FWHM is 1.87% of its energy. This alone costs a factor 4.9 of the statistic (32.16 → 6.53).
2. The deposit rebin: 2.920%/bin. Costs 6.53 → 6.11, i.e. almost nothing.
3. The response chain onto a 161-bin reconstructed axis at **12.202%/bin**. Costs 6.11 → 3.38 —
   the dominant term, and it is a **resolution** effect, not a physical erasure.

**Why "washed out" and not "gone".** The amplitude contrast against the control is still **33–35%**
on the reconstructed axis, and the feature is visible in
`artifacts/v2.0/neutron_subev_spectra.pdf` as a step near `E_rec ≈ 2.66 eV` — the response image of
the 5.50 eV kinematic edge. What fails is the *pre-declared slope statistic*, because a 12.2%-wide
bin cannot resolve a 1.9%-wide edge. **No band was narrowed and no threshold was lowered to make
the criterion pass** (`fp-narrow-the-window`). The recoil-axis result is **not** quoted as if it
were the reconstructed one.

The control **fails at every stage**, which is what keeps the statistic meaningful: it never
measures anything but resolved structure.

---

## 6. ROADMAP Phase 13 success criteria — all five adjudicated

| SC | verdict | evidence |
|---|---|---|
| **SC1** — dR/dE_rec both designs, resonance-resolved grid preserved, unified phonon scale, no quenching, count conservation ≤1e-3 | **PARTIALLY CONFIRMED** | Both designs produced from 0.0999350 eV (§3, `artifacts/v2.0/neutron_dRdErec_ext_{TaAl,AlHf}.csv`); keV_nr with no Lindhard anywhere. Conservation **discharged on retained + leaked at 5.969×10⁻⁵** (§2). PARTIAL because the criterion as literally written does not name a budget and **cannot** hold on retained-only: 49.73% of the bottom bin's kernel genuinely leaves the axis, so `residual_retained_only = −7.663×10⁻³` MISSES and must. The resonance-resolved grid is preserved onto the deposit axis but not resolved on the reconstructed one — see SC3. |
| **SC2** — order-of-magnitude label everywhere; error budget attributes dominance to the input flux | **CONFIRMED** | §4. Label present on all eight data artifacts, on the figure and in this report (`test_label_audit_...`). Kernel side bounded at 4×10⁻⁷–1.1×10⁻³ from the frozen validation block; flux side demonstrated UNBOUNDED by two explicit Gordon-preserving perturbations moving the in-RoI rate by +41.33% and −16.31% while the only cross-check registers exactly zero. No integral-level figure used as a differential error bar. |
| **SC3** — resonance imprint present below 5.5 eV; a smooth sub-10 eV spectrum is a bug, unit-tested | **PARTIALLY CONFIRMED** | §5 and `13-01-KERNEL-AND-IMPRINT.md` §7. Present and unit-tested on the recoil axis (32.160 vs a resonance-integral-preserving control at 1.143, threshold 5.0, stable at 200/400/800 bins per decade), and it survives IA broadening and the deposit rebin (6.113). PARTIAL because on the **reported observable** the pre-declared statistic falls to 3.38/3.60, below its own threshold, washed out by the 12.2%-wide reconstructed binning. The 33–35% amplitude contrast survives and the step is visible in the figure at `E_rec ≈ 2.66 eV`. Carrier isotope named (⁷³Ge, 98.84% of the 669.1 b peak) and the edge measured as 5.4705 eV against the single-`f` 5.4988 eV. |
| **SC4** — kinematic compression exhibited, not asserted | **SUPERSEDED BY MEASUREMENT** | `13-02-COMPRESSION-AND-OMISSIONS.md` §1–5. The kinematic factor cancels identically out of the fold (measured spread 4.20×10⁻⁸ across four `f`); the operative mechanism is atoms/kg (2.53339 for Ge/W), and the roadmap's ~2.5× is a 1.6% numerical near-identity of mass number. The Ge-vs-CaWO₄ statement the roadmap actually makes **reverses**: Ge/CaWO₄ = 0.673–0.692 per kg across the RoI. |
| **SC5** — sub-5 eV kernel handled explicitly, free-atom σ never used below 5 eV; 20 MeV ceiling bounded at the surface | **CONFIRMED** | `13-01` §8: Route A (NCrystal `Ge_sg227` splice at 5 eV), measured seam step −5.4244%, chosen because truncation drops 57.88% of the bottom bin; free-atom evaluation below 5 eV provably zero by an executed counter. `13-02` §6: >20 MeV omission bounded at 1.35–2.55×10⁻⁵ in-RoI and 8.91–16.87% of the T-integrated total, with the flat continuation's conservatism established by a measured slope and a second upper continuation added when the top decade proved non-monotone. |

**Nothing was narrowed to make any criterion true.** Two criteria are reported PARTIALLY CONFIRMED
and one SUPERSEDED BY MEASUREMENT.

---

## 7. Directional-bias row for the finished channel — `09-02` §7 schema, un-netted

| # | quantity | signed deviation | direction | why |
|---|---|---|---|---|
| 1 | **central value**: `phi_default` = `phi_hi`, the OUTDOOR leg, with the Gordon **midpoint** 3.550×10⁻³ | +0.00% (anchored by construction; untuned PARMA sits at −8.77%) | **`penalizes_SB`** | The channel adopts the upper/outdoor leg of its own band and the midpoint of the Gordon range, not the low edge. `phi_lo = phi_default/5` would be a factor-5 `flatters_SB` move and is REFUSED in code. |
| 2 | `E_n > 20 MeV` elastic recoils, omitted by the frozen σ_el ceiling | −1.35×10⁻⁵ to −2.55×10⁻⁵ of the in-RoI rate; −8.91% to −16.87% of the T-integrated total | **`flatters_SB`** | Truncating the cross section removes background. |
| 3 | the **elastic-only** restriction on that bound | not quantifiable with the data this project holds | **`flatters_SB`** (further) | Above 20 MeV nonelastic and spallation channels are comparable to elastic and produce larger recoils. |
| 4 | sub-5 eV kernel | **not applicable** | — | Route A (NCrystal splice) was taken, so nothing is omitted there. Had Route B been taken it would have been a `flatters_SB` −57.88% of the bottom bin. The residual model uncertainty of Route A (bound vs free-atom σ over 1.87–5 eV) is +3.49% at the bottom bin, i.e. `penalizes_SB` if anything. |
| 5 | isotropic-CM flat box (`a1` carried, not applied) | contribution-weighted ⟨a1⟩ ≤ 3.4×10⁻³ in the RoI, 0.55 at T = 10⁵ eV | negligible in the RoI; `penalizes_SB` above ~10⁵ eV | Forward peaking tilts dσ/dT toward the low-T end of each box, so an isotropic flat box overstates the high-T end. |

**Rows 2–4 are carried alongside row 1, never netted against it** (`fp-net-omissions`). A net
figure would hide both the size of what was dropped and the fact that the central value's
conservatism was bought elsewhere.

---

## 8. Hand-off

**To Phase 16 (S/B assembly) — with the caveats attached** (`fp-silent-neutron-omission`):

- `artifacts/v2.0/neutron_dRdErec_ext_{TaAl,AlHf}.csv`, both designs, 161-bin reconstructed axis,
  untriggered / trigger-weighted / one-sided upper-width columns.
- **`accuracy_label = order_of_magnitude`.** Nothing derived from this channel may be quoted more
  precisely (`fp-precision-inflation`).
- The five directional-bias rows of §7, **un-netted**.
- The omission bounds of `13-02` §6, in-RoI and total-rate **separately**.
- **The headline number Phase 16 needs to see first**, measured on the SHARED reconstructed axis
  against `artifacts/v2.0/cevns_dRdErec_ext_TaAl.csv` rather than across axes:

  | `E_rec` | neutron | CEvNS | **ratio** |
  |---|---|---|---|
  | 0.094 eV | 1.135×10⁷ | 3.696×10³ | **3.07×10³** |
  | 0.473 eV | 4.229×10⁶ | 4.210×10³ | 1.00×10³ |
  | 0.944 eV | 2.803×10⁶ | 3.998×10³ | 7.01×10² |
  | 9.44 eV | 2.009×10⁵ | 2.258×10³ | **89** |
  | 94.4 eV | 3.706×10⁴ | 3.049×10² | **122** |

  (counts kg⁻¹ day⁻¹ keV⁻¹, Ta→Al, both untriggered.) So the honest statement is **a factor of a
  few thousand in the sub-eV region and roughly a factor 10² inside the 10–100 eV RoI** — not "four
  orders of magnitude", which would over-state it. For an unshielded outdoor surface wafer a
  background far above the signal is the expected result, not a bug, but it means the sub-eV S/B of
  this milestone is set by this background and not by the signal.

**To Phase 14 (thermal capture, (n,γ), ⁷¹Ge EC, Ge inelastic):**

- **Φ_th = 2.767075×10⁻³ cm⁻² s⁻¹** is **Phase 9's** product, not this phase's. It is the input to
  the capture channel and is unchanged by anything here.
- This phase computed the **elastic** channel only. Ge inelastic (⁷⁴Ge 596 keV, ⁷²Ge 834 keV) is
  Phase 14's, and omitting it here biases the `13-02` >20 MeV bound in the `flatters_SB` direction.
- The PARMA thermal term is a 293.6 K free-gas ambient Maxwellian; whether that is adequate for a
  mK cryogenic target's capture channel is an open assumption `09-02` §5 already flagged.

**To Phase 15 (muon and Compton onto this axis):** the IA-applicability argument used here rests on
neutron elastic recoils being **nuclear** recoils. It says nothing about electron recoils, which
Phase 15 must adjudicate separately.

---

## 9. Discharge table for Plan 13-03

| acceptance test | outcome | evidence |
|---|---|---|
| `test-counts-budget` | **PASS** | §2 — retained+leaked 5.969×10⁻⁵ ≤ 10⁻³; retained-only −7.663×10⁻³ MISSES and matches the leakage to 0.79%; fold residual exactly 0 |
| `test-broaden-once` | **PASS** | §1 — the guard raises on a `true`-labelled table AND on an unlabelled one; the production second moment matches a single application to 10⁻¹² and differs from a double application |
| `test-grid-744` | **PASS** | §1 — 744 centres, floor matched to 4.4×10⁻⁷ relative, v1.0 584-column matrix rejected, `DEFAULT_GRID_VERSION == "v1.0"` asserted |
| `test-imprint-survives` | **PASS** (verdict recorded: WASHED OUT on the reconstructed axis) | §5 — four stages, washout quantified at 9.51×/8.94× on the statistic and 1.64×/1.58× on the contrast; control fails at every stage |
| `test-trigger-composition` | **PASS** | §3 — `P_trig == 1` bit-identical for both designs; the curve is evaluated on the deposit centres |
| `test-kernel-perturbation` | **PASS** | §4.1 — every row sourced from the frozen validation block; linearity of σ_el verified to 10⁻⁶ |
| `test-flux-term-unbounded` | **PASS** | §4.2 — two explicit constructions, opposite signs, +41.33% and −16.31% in-RoI against exactly zero on the cross-check |
| `test-no-manufactured-uncertainty` | **PASS** | §4.3 — flux rows carry UNBOUNDED; no integral-level figure used as a differential error bar |
| `test-sc-verdicts` | **PASS** | §6 — all five carry a verdict with its evidence located; SC1's budget ambiguity resolved explicitly |
| `test-disposition-rows` | **PASS** | eight new tracked `.csv` files registered; `tests/test_legacy_grid_disposition.py` passes |
| `test-label-audit` | **PASS** | label on all eight artifacts, on the figure and in this report |
| `test-no-shielded-or-indoor` | **PASS** | Phase-9 shielded-token machinery over the module and all eight artifacts returns zero APPLIED hits; the `phi_lo` line scan returns zero uses |

---

## 10. What still cuts against this result

- **The eV–keV differential shape of the sea-level flux.** No independent validation, none
  obtainable here, and §4.2 shows concretely that perturbations the cross-check cannot see move the
  answer by tens of percent. Everything downstream inherits that.
- **The 100 meV bin.** 49.73% of its kernel leaves the axis on this binning, 0.89% to unphysical
  `T < 0`, a symmetric Gaussian fitted to an asymmetric lineshape with skewness 0.590. CONVENTIONS
  §J calls it the least reliable number in the milestone and this channel's spectrum reaches it.
- **The single-frequency IA width understates the true width by `sqrt(1.354758) = 1.1639`**, because
  ⟨u_x²⟩ is governed by the harmonic VDOS mean while ⟨p_x²⟩ is governed by the arithmetic one. The
  locked harmonic value is central and the arithmetic one ships as a separate upper-WIDTH column.
- **IA applicability to neutron recoils is asserted, not re-derived.** Both are nuclear recoils, so
  the physical basis is the same, but the Phase-11 derivation was performed for CEvNS.
- **The isotropic-CM flat box and the 293.6 K processing against a mK target**, both carried
  unchanged from Plans 13-01 and 07.
- **The imprint is washed out on the reported observable.** SC3 is satisfied on the recoil axis and
  on the deposit axis but not on `E_rec`. Anyone quoting "germanium's resonance structure is visible
  in the reconstructed spectrum" as a discriminating handle would be over-reading this result: the
  33–35% amplitude contrast is there, the slope statistic is not.
