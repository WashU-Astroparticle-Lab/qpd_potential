# 15-02 — Both electron-recoil channels on the 744-bin extended axis

**Plan:** 15-02 · **Phase:** 15 · **Date:** 2026-07-23
**Interpreter:** `/opt/anaconda3/bin/python3` (numpy 1.26.4, scipy 1.17.1)
**Repo HEAD at execution:** `de3f5a4`

---

## 1. The route decision — made by measurement

### 1.1 The structural claim, tested at small N before spending a production run

`em_extended.bit_identity_probe()` runs each Monte Carlo twice at a small sample
count — once on `shared_energy_grid('v1.0')`, once on `shared_energy_grid('v2.0-ext')`
— at identical `(n, seed, batch_size)`, and compares bins `160..743` with
`np.array_equal`, **never** `np.allclose`.

```
/opt/anaconda3/bin/python3 -c "import sys;sys.path.insert(0,'src')
from qpd_potential import em_extended as e; print(e.bit_identity_probe())"
```

| Check | Result |
|---|---|
| `np.array_equal(ext_edges[160:], v1_edges)` | **True**, max abs difference **exactly 0.0** |
| muon `dRdE[160:]` vs v1.0 run | **array_equal True** |
| muon `mc_err[160:]`, `mc_entries[160:]`, `rate_hz` | **array_equal / equal True** |
| Compton `dRdE[160:]`, `mc_err[160:]`, `mc_entries[160:]`, `rate_hz` | **array_equal / equal True** |

The RNG stream is independent of the histogram edges in both drivers — every draw
in `_mc_batch` and in `sample_electron_recoil` precedes `np.histogram` — so the
retained bins reproduce **exactly**.

### 1.2 Production cost, measured and extrapolated before launching

Required by the plan rather than assumed. Measured on this machine:

| Channel | probe | extrapolated to production | **actual** |
|---|---|---|---|
| muon | 5e6 samples in 2.399 s | 1e9 → **8.0 min** | **512.2 s = 8.5 min** |
| Compton | 4e5/line in 1.397 s | 4e7/line → **2.3 min** | **147.4 s = 2.5 min** |

**No reduction of N was needed and none was made.** Both channels were run at the
frozen v1.0 sample counts (`n_samples = 1e9`, `n_per_line = 4e7`), the frozen seed
`20260720` and the frozen `batch_size = 5e6`, so there is **no statistical penalty
to record**.

### 1.3 Do the frozen v1.0 artifacts reproduce? — **Yes, exactly**

This had never been executed before. The extended run's retained bins were compared
bin by bin against the committed CSVs:

| Channel | bins identical at the frozen file's own `%.6e` | max relative difference | at bin |
|---|---|---|---|
| muon | **584 / 584** | 4.376023e-07 | 412 (1.435415e+03 keV) |
| Compton | **584 / 584** | 4.632438e-07 | 51 (4.403934e-02 keV) |

Zero bins where the frozen file is 0 and the extension is not, and zero the other
way. The residual ~4.6e-07 is the **CSV's own six-significant-figure round-trip**,
not a computational difference: at the precision the files are written to, every
one of the 584 bins is identical.

**Finding, recorded because it had never been established:** the frozen v1.0
deposit artifacts **are** regenerable from committed code at their recorded
settings. That is a positive result about the v1.0 record, and it is the one that
licenses the exact-re-drive route.

### 1.4 Route selected

```
route = exact_redrive_identical_stream
route_selected_by = small-N np.array_equal on bins 160..743 for BOTH channels
                    (PASS), plus reproduction of both frozen v1.0 CSVs at their
                    recorded settings (muon PASS, compton PASS)
```

Recorded in both emitted table headers. The `index_carry_frozen_bins` alternative
was not needed; had either test failed, it would have been taken and the failure
recorded as a finding about the v1.0 artifacts rather than worked around.

### 1.5 Docstring defect fixed

`muon_deposit.shared_energy_grid`'s docstring called `v2.0-ext` "the default".
`DEFAULT_GRID_VERSION` is authoritative and reads `"v1.0"`. Fixed. Both drivers now
take an explicit `grid_version` parameter **defaulting to `"v1.0"`**, so the Plan
10-03 caller pin survives as the parameter default: a caller that does not name a
version still gets the v1.0 axis and the frozen `data/` files can never be silently
re-binned.

---

## 2. ROADMAP Phase 15 SC1 — the invariants

Frozen in `artifacts/v2.0/em_v1_regression.csv` (1168 per-bin rows + a scalar
header block).

| Invariant | Reproduced | Target | Verdict |
|---|---|---|---|
| K-40 Compton edge | **1243.3573 keV** | 1243.3573 ± 0.5 | **PASS** (< 1e-3 keV) |
| Bi-214 Compton edge | **1541.3115 keV** | 1541.3115 ± 0.5 | **PASS** |
| Tl-208 Compton edge | **2381.7571 keV** | 2381.7571 ± 0.5 | **PASS** |
| through-wafer muon rate | **1.365914 ± 0.000308 Hz** | 1.3659 ± 0.0003 | **PASS** (\|Δ\| = 1.4e-5) |
| Compton bound-incoherent rate | **2.6747e-01 Hz** | 2.6747e-01 (rate of record) | **PASS** |
| Compton energy closure | **2.102771e+05 counts/kg/day** | 2.1028e+05 | **PASS** |
| muon max rel. diff above 10.14 eV | **4.376023e-07** | < 1e-2 | **PASS** |
| Compton max rel. diff above 10.14 eV | **4.632438e-07** | < 1e-2 | **PASS** |

The edges are computed in **closed form** from `data/gamma_lines.csv` via
`E_edge = 2E²/(m_e c² + 2E)`, independently of the sampler, so agreement with the
spectrum's edge structure is a check and not a tautology.

The muon rate is written into the header explicitly flagged as an **ABSOLUTE
through-wafer rate in Hz, NOT a per-kg quantity** — a units slip there would be
invisible in the shape and fatal in the normalization.

The Compton four-way rate distinction is carried **verbatim** because these are
four different numbers and are not interchangeable: bound incoherent
**2.6747e-01 Hz** (the rate of record), free-KN 2.6846e-01, VALD-03 anchor
2.7305e-01, `f_bind` 0.9963.

**No photopeak.** 153 bins have a lower edge above the highest Compton edge
2381.7571 keV; **zero of them carry content**, and the bin containing the full
Tl-208 line energy 2614.511 keV (index 593, centre 2627.3296 keV) carries **exactly
0.0** with zero raw entries. `assemble_channel` **raises** if a Compton entry is
ever found above that ceiling, so `fp-full-absorption` is enforced in code, not
only checked after the fact.

### 2.1 Normalization — every factor exactly 1.0, enumerated individually

Written into both headers as separate lines, because a product can be unity by
cancellation:

```
overburden_attenuation = 1.0   (no overburden in this configuration)
shield_attenuation     = 1.0   (no shield in this configuration)
veto_credit            = 1.0   (exactly 1.0 BY CONSTRUCTION -- surface_environment.veto_credit())
buildup_factor         = 1.0   (no shield, so no buildup)
ambience_rescale       = 1.0   (the v1.0 sea-level normalization stands unchanged)
```

### 2.2 Frozen files untouched

SHA-256 of all five frozen `data/` files matches `git show HEAD:<path>`, and
`tests/test_env_v1_identity.py` is re-run inside `test_no_frozen_file_written` and
passes. Nothing under `data/` was written.

---

## 3. What is actually in the 160 new bins

Both tables declare `broadened_provenance = false`
(`fold.read_broadened_provenance` returns exactly `False`, not `None`), per Plan
15-01's per-channel verdict `does_not_apply`.

### 3.1 Muon — a **bounded absence**, not a spectrum

Sub-eV region = bins 0..159, centres 0.101384 … 9.8571 eV.

| | muon |
|---|---|
| bins with ≥ 1 raw MC entry | **125 / 160** |
| bins with **no** MC support (NaN, labelled `no_mc_support`) | **35** |
| total raw entries across all 160 bins | **572** (max 18 in any one bin) |
| bins with ≥ 10 entries | **18** |
| relative MC error over supported bins | min 0.449, **median 0.868**, max 1.000 |
| `adequate_mc_support` | **0** |
| `marginal_mc_support` | 6 |
| `insufficient_mc_support` | 119 |
| **bins below the Plan 15-01 validity floor** | **160 / 160** (the floor is 4111.82 eV) |
| integrated over bins 0..159 (NaN bins excluded) | 3.3195e-01 counts/kg/day |

**Stated plainly: the muon sub-eV region is a bounded absence, not a spectrum.**
Every one of the 160 bins is (i) below the Landau–Vavilov validity floor, so
outside the deposit model's domain, and (ii) statistically inadequate — not one bin
reaches `adequate_mc_support`, the median relative error is 87 %, and 35 bins have
no estimator support at all. Two independent reasons, either sufficient. **No
sub-eV muon rate may be quoted from this table as a prediction.**

For scale, the first *v1.0* bin is already marginal: at 10.144973 eV the value is
**16.011 ± 7.606 counts/kg/day/keV** (47.5 % relative error, 12 raw entries),
`marginal_mc_support`. The channel was MC-limited at the v1.0 floor and two more
decades at unchanged sample count made it worse, exactly as expected.

### 3.2 Compton — sparse, partly measurable, mostly below the physical floor

| | Compton |
|---|---|
| bins with ≥ 1 raw MC entry | **91 / 160** |
| bins with **no** MC support (NaN, labelled) | **69** |
| total raw entries across all 160 bins | **1415** (max 73 in any one bin) |
| relative MC error over supported bins | min 0.148, **median 0.470**, max 1.000 |
| `adequate_mc_support` | **7** |
| `marginal_mc_support` | 31 |
| `insufficient_mc_support` | 53 |
| **bins below the Plan 15-01 physical floor** | **70 / 160** (the floor is 0.73955 eV) |
| integrated over bins 0..159 (NaN bins excluded) | 2.7746e-01 counts/kg/day |
| lowest supported bin | index 20, centre 0.180303 eV, 1 raw entry |

The Compton channel does reach further down with usable statistics than the muon
channel — 7 bins reach `adequate_mc_support` — but **70 of the 160 bins lie below
the Ge pair-creation floor**, where the S(x, Z) machinery returns a number that is
not a physical electron-recoil rate (Plan 15-01 §4.2). Between 0.73955 eV and
10.14 eV the estimator has partial support and the physics is in-domain; below
0.73955 eV nothing may be quoted as a rate regardless of what the estimator did.

At the v1.0 floor the Compton bin is **47.661 ± 12.984 counts/kg/day/keV**
(27.2 % relative error, 75 raw entries), `marginal_mc_support`.

### 3.3 The NaN discipline, and its one narrow exception

**Zero-entry bins are written NaN and labelled `no_mc_support`, never 0.0**
(`fp-zero-for-no-data`). A zero reads as a measured absence of rate; the correct
statement is that the estimator has no support there. Verified by
`test_no_support_not_zero`: no zero-entry bin carries 0.0, and no supported bin
carries NaN.

**One exception, and it is a physics distinction rather than a convenience.** For
the Compton channel, the 153 bins whose **lower edge exceeds the highest Compton
edge** are written **0.0** with the label `kinematically_forbidden`. There the
reasoning behind `fp-zero-for-no-data` inverts: the thin-target single-scatter
model *positively forbids* content above `E_edge`, so 0.0 is the model's
**prediction**, and writing NaN would say "unmeasured" about a region the model
excludes — and would make `test-no-photopeak` untestable in the artifact, while
`fp-full-absorption` requires the approximation intact *in the artifact*, not
merely in the prose. The exception is confined to exactly that set
(`np.array_equal(forbidden, edges[:-1] > 2381.7571)`), is asserted to be
Compton-only, and the code raises if any entry is found there.

### 3.4 What Plan 15-03 may and may not do with this

* **May** fold both tables — they are 744-bin, unbroadened, and declared.
* **Must** call the fold with `broaden=False`, reading the verdict from
  `em_recoil` at fold time.
* **Must** pass an explicit no-support policy: the muon table has **35** NaN bins
  and the Compton table **69**, `R` is dense, and a single NaN poisons every
  reconstructed bin. `np.nan_to_num` is forbidden by name.
* **May not** report a sub-eV muon rate as a prediction; the honest deliverable
  there is a bounded absence carried into Phase 16 as a named gap.
* **May not** report a Compton rate below 0.73955 eV as a physical rate.

---

## 4. Accuracy labels, carried forward unnarrowed

On **every row** of both tables, following the Phase-13 pattern of trailing
non-numeric labels so a consumer cannot parse a rate out of the file without also
encountering them (a plain numeric parse of a row stops after 5 fields).

**Muon** — never the bare −20.61 % and never a bare `flatters_SB`:

```
flatters_SB | -20.61% vs PDG Leg A (~1 muon cm^-2 min^-1 x A_top = 1.7204 Hz)
| BRACKETING DISCLOSURE: PDG Leg B (I_v ~ 70 m^-2 s^-1 sr^-1 with cos^2 theta ->
1.1350 Hz) puts the same adopted 1.3659 Hz at +20.34%, i.e. penalizes_SB; the two
PDG statements BRACKET the adopted rate from opposite sides, so the ~20% MAGNITUDE
is solid and the SIGN is anchor-leg dependent
| underlying limit: 30-35% inter-experiment Gaisser-Guan normalization spread,
which no in-repo artifact can narrow
```

**Gamma** — `neutral`, +0.00 % against the LABChico measured survey which *is* the
adopted normalization, factor-2 site band ×0.5 … ×2 with the note that the low edge
is the flattering one and is not used, and the `Phi_U = Phi_Th` chain-balance
assumption named as the weakest anchor.

**Nothing was narrowed.** Extending the energy axis does not improve a
normalization and no line of either table implies it did.

---

## 5. Verification ledger

| Acceptance test | Outcome | Evidence |
|---|---|---|
| `test-smallN-bit-identity` | **PASS** | `test_smallN_bit_identity`; §1.1 |
| `test-frozen-reproduction` | **PASS (positive finding: both reproduce)** | `test_frozen_reproduction_recorded`; §1.3 |
| `test-route-recorded` | **PASS** | `test_route_recorded`; both headers |
| `test-grid-shape` | **PASS** | `test_grid_shape` — `np.array_equal`, max diff 0.0 |
| `test-no-frozen-file-written` | **PASS** | `test_no_frozen_file_written` — SHA-256 vs HEAD + `test_env_v1_identity.py` re-run |
| `test-unbroadened-declared` | **PASS** | `read_broadened_provenance` returns exactly `False` for both |
| `test-labels-inseparable` | **PASS** | `test_labels_inseparable` — Leg A + bracketing present |
| `test-no-support-not-zero` | **PASS** | `test_no_support_not_zero`; §3.3 |
| `test-compton-edges` | **PASS** | `test_compton_edges` — all three to < 1e-3 keV |
| `test-muon-rate` | **PASS** | `test_muon_rate` — within the frozen uncertainty |
| `test-v1-regression-1pct` | **PASS** | max 4.6e-07, three decades inside 1 % |
| `test-no-photopeak` | **PASS** | `test_no_photopeak`; §2 |
| `test-dimensions` | **PASS** | `test_dimensions` — units in every header, closure reproduces |

**Forbidden proxies.** `fp-silent-reinterpolation` rejected (`np.array_equal`, max
difference exactly 0.0; no interpolation anywhere). `fp-zero-for-no-data` rejected
(§3.3, with the one exception argued and confined). `fp-mc-rerun-drift` rejected
(no `data/` file written; SHA-256 checked against HEAD). `fp-improved-normalization`
rejected (sample counts, seed, batch size and every physics constant unchanged; no
band narrowed). `fp-full-absorption` rejected (enforced by a raise, not only by a
check). `fp-shielded-quantity-leak` rejected (Phase-9 token list imported, zero
applied hits).

---

## 6. Uncertainty markers

**Weakest anchors.** The muon ~20 %-vs-PDG standing with its anchor-leg-dependent
sign; the 30–35 % Gaisser–Guan spread; the gamma factor-2 site band resting on the
assumed `Φ_U = Φ_Th` chain balance; and the sub-10.14 eV content of both channels,
which has no external validation of any kind and which Plan 15-01's floors place
outside both deposit models' validity domains.

**Unvalidated assumptions.** That the per-bin MC error means anything in the sub-eV
bins — it does not where the entry count is of order one, and there the **adequacy
label rather than the error bar** is the operative statement. This is why
`stat_adequacy_label` demotes any bin with fewer than 10 entries regardless of what
`sqrt(Σw²)/y` happens to evaluate to.

**Competing explanations for the muon sub-eV content**, distinguished in Plan
15-01 §5.5 rather than picked between: short-chord corner-clipping geometry versus
the tabulated Landau inverse-CDF's left tail against the zero clip. The numbers
support a **joint tail** of both, and in either limb the deposit sits far below
`ξ ≈ I`.

**Disconfirming observations.**
* ❌ did not fire — the frozen CSVs **do** reproduce (584/584 both channels).
* ❌ did not fire — bins 160..743 **are** bit-identical under re-histogramming.
* ❌ did not fire — the max regression is 4.6e-07, four decades inside the 1 % bar.
* ✅ **FIRED** — a large fraction of the 160 new bins have no or inadequate
  support. For the muon channel **not one bin** reaches `adequate_mc_support`, so
  the honest deliverable there is a **bounded absence**, reported as such rather
  than smoothed over.
