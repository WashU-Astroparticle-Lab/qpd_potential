# 12-03 — Closure: the v1.0 regression, the target-swap benchmark, and the VNS rescale

**Phase:** 12 — Reactor CEvNS down to 100 meV at the Paper's Surface Scenario (P-SIG)
**Plan:** 12-03 (wave 3) — the audit. **Nothing here produces a new spectrum.**

**Reproducing command:**

```
PYTHONPATH=src /opt/anaconda3/bin/python3 -m qpd_potential.cevns_subev 12-03
/opt/anaconda3/bin/python3 -m pytest tests/test_cevns_subev_regression.py -q
```

---

## 1. VALD-10, regression leg — **PARTIAL**

### 1.1 The comparison is an index carry, proved

The reconstructed-energy edge sets of `artifacts/stage1/response_matrix_*.npz` and
`artifacts/v2.0/response_matrix_*_ext.npz` are **identical under `np.array_equal`, with
maximum difference exactly 0.0**. Bins are therefore selected by **index**. Neither
spectrum is interpolated onto the other, and the comparison path contains no `np.interp`,
no `interp1d`, no `PchipInterpolator` and no `np.allclose`
(`fp-regression-by-interpolation`). A tolerance-based axis check would have let Phase-10's
`fp-naive-logspace` drift — up to 5.1 × 10⁻⁴ relative — through unnoticed.

The compared object is the **un-triggered** extended spectrum: the trigger is an analysis
efficiency and the v1.0 numbers carry none. `P_trig(100 eV) = 0.999999999375`, so that
choice cannot be hiding a real deviation.

### 1.2 The measurement

40 bins per design, `E_rec` from 10.59 eV to 944.1 eV.

| design | max \|deviation\| | at `E_rec` | mean | min | bins > 1 % | verdict |
|---|---|---|---|---|---|---|
| **Ta→Al** | **0.7648 %** | 473.2 eV | 0.2304 % | 7.61 × 10⁻⁵ | **0** | **PASS** |
| **Al→Hf** | **3.7246 %** | 944.1 eV | 0.2786 % | 2.29 × 10⁻⁵ | **1** | **FAIL, in one bin** |

**The <1 % target was not relaxed.** Al→Hf exceeds it, and that is reported as an exceedance
rather than absorbed.

Where the failure lives, characterised (this is *characterisation*, not the verdict — the
verdict is taken on the full compared range):

- It is the **single highest populated reconstructed bin**, at the 3.2 keV recoil kinematic
  endpoint, where the rate is **7.88 × 10⁻⁷** counts/kg/day/keV — about nine decades below
  the peak.
- Below 900 eV, **both** designs are inside the target: 0.7648 % (Ta→Al) and 0.5557 %
  (Al→Hf).
- The deviation is small but **not identically zero** anywhere (minimum 2.3 × 10⁻⁵), so the
  extended pipeline is genuinely recomputing rather than echoing the frozen numbers.

### 1.3 The decisive diagnostic: the residual is **not** the broadening

Switching the IA kernel **off** and re-running the same comparison:

| design | max \|deviation\|, broadening ON | broadening OFF |
|---|---|---|
| Ta→Al | 0.7648 % | 0.7688 % |
| Al→Hf | 3.7246 % | 3.7234 % |

The kernel moves the residual by ~0.001 percentage points. **Nothing Phase 12 added causes
it.** The cause is the **Phase-10 response-matrix regeneration**: the archived v1.0
`R_non_paralyzable` and the regenerated extended one are *independent Monte Carlo samplings*
and are not bit-identical on their overlapping deposit columns — maximum absolute difference
**2.86 × 10⁻²** (Ta→Al) and **3.16 × 10⁻²** (Al→Hf) in matrix elements. In the extreme tail,
where a single reconstructed bin is fed by a handful of deposit columns at a rate ~10⁻⁶, that
MC noise is amplified into a few percent.

**Two honest consequences.**

1. Phase 12's own additions — the extended axis, the IA broadening, the trigger composition
   — leave the validated v1.0 results untouched to well inside 1 %. That is the substance
   VALD-10 was asking about, and it holds.
2. But the <1 % gate as literally written is measured against a matrix that was itself
   resampled, so what fails is a **Phase-10 inheritance**, not a Phase-12 change. This is
   recorded and carried forward rather than silently attributed to the wrong phase.

> **Competing explanation, acknowledged:** above 10 eV the broadening is genuinely negligible
> (σ_E/E_R is sub-bin above ~21 eV), so this regression tests the *plumbing* far more than
> the new sub-eV physics. It is not evidence that the 100 meV end is right. Nothing in
> Phase 12 tests the bottom decade against an independent object, and that gap is stated in
> both 12-02 and here.

---

## 2. ROADMAP SC3's `T = 0.290 eV` clause — **RESTATEMENT, not corroboration**

SC3 asks that *"T = 0.290 eV reproduces the frozen v1.0 value exactly"*.

**Confirmed programmatically:** `artifacts/stage1/cevns_dRdT.csv` has 320 rows with support
**5 eV to 3200 eV**. Its floor is **5 eV**. **There is no frozen v1.0 value at 0.290 eV to
compare against.** No comparison at 0.290 eV is claimed anywhere in this phase, and a test
asserts that no phase document makes such a claim.

Recomputing `dR/dT` at 0.290 eV with the same code and calling the agreement a regression
would be an identity dressed as a check.

**And the clause's physical content restates SC4's zero-point.** "Nothing changes above
0.29 eV" and "the truncation bound is exactly zero above 0.29 eV" are the *same statement*.
It is therefore **not independent corroboration** and is not counted as a second check.
Phase 11 found three such roadmap "cross-checks" that were algebraic identities; this is a
fourth, in the same style, and it is recorded as such.

(Plan 12-01 additionally measured that the zero-point is not at 0.29 eV at all but at
**0.3067 eV**, set by ⁷⁰Ge — so even the restated clause needs its own correction. See §4,
SC4-c.)

---

## 3. The target-swap benchmark (SC5)

### 3.1 The compound arithmetic, recomputed

`Σ N_i² / Σ A_i`, from CIAAW standard atomic weights held in this module — **recomputed
here, not quoted from `GPD/literature/`**, because this is the one part of the benchmark
this repository can actually reproduce:

| quantity | atoms | recomputed | literature figure |
|---|---|---|---|
| natural Ge | Ge (72.630 u, Z=32) | **22.729** | 22.7 |
| CaWO₄ **compound** | Ca + W + 4 O | **44.193** | 44.2 |
| naive ratio CaWO₄/Ge | | **1.944** | 1.95 |
| pure W, standard atomic weight | W (183.84 u) | **65.627** | — |
| pure ¹⁸⁴W | (184 u) | **65.761** | **65.8** |

Two things worth pinning:

- The literature's **65.8** is the **¹⁸⁴W** value, not the standard-atomic-weight tungsten
  value (65.63). Both are reported here with their masses named.
- **65.8 describes a different material** and must never stand in for the CaWO₄ compound
  **44.2**. Using it would inflate the target-swap ratio by ~1.5×.

### 3.2 The verdict: **2.31 is the benchmark; 1.95 is REJECTED**

The **same-pipeline** Ge/CaWO₄ ratio **2.31** (Ge 176.8 vs CaWO₄ 407.7 counts/kg/day/keV,
10–100 eV, 100 % duty) is the documented benchmark. The naive compound ratio **1.95** is
explicitly rejected, for a stated physical reason: it omits

1. the **Helm form factor**, which suppresses the heavier target more at the same recoil
   energy;
2. the **kinematic `T_max/E_ν` compression** — for a heavier nucleus a given neutrino energy
   produces a smaller maximum recoil, so the RoI captures a different part of the spectrum;
3. the **per-isotope threshold structure**, since `E_min,i(T)` differs isotope by isotope and
   the compound has three elements with very different mass numbers.

`N²/A` counts coherent scattering strength per unit mass and nothing else. The same-pipeline
fold includes all three of the above; the 2.31 / 1.95 difference (~19 %) is what they are
worth.

### 3.3 The closure citation — with its scope **and** its provenance gap

**Cited, not re-run.** The already-passed signal-side closure is: our CaWO₄ fold **407.7**
counts/kg/day/keV against **NUCLEUS Table 5 at 100 % duty, 356.5** counts/kg/day/keV
(EPJC **86**, 29 (2026), arXiv:2509.03559) — ratio **1.14**, i.e. a 14 % closure.

**Its scope, stated:** it closes the **flux × cross-section × target chain**. It says
**nothing** about any environment, any background, any shielding or any site. Anchoring on
the §2 prose value **280** instead of Table 5 at 100 % duty would be `fp-nucleus-prose-280`
— 280 is the 80 %-duty figure (356.5 × 0.8 = 285) and using it flatters Ge S/B by ~27 %.

**Its provenance gap, stated.** A word-bounded repository-wide search was run:

```
git grep -lE '(^|[^0-9.])407[.]7([^0-9]|$)' | sort
```

It returns **only GPD prose documents** — `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`,
`STATE.md`, `state.json`, `literature/SUMMARY.md`, the Phase-8 gate verdict, and this
phase's own PLAN and CONTEXT. **No CaWO₄ module, no test, no notebook cell, no committed
data artifact reproduces 407.7.** There is no reproducible command for it. Under the
project's own evidence discipline the citation therefore carries the label
**unreproduced prior assertion** (`fp-closure-as-reproduced`).

(The word boundary matters: a bare substring search for `407.7` matches by coincidence
inside long numeric fields of a dozen committed CSVs. Using it would have manufactured a
reproducible source that does not exist.)

**Neither re-run nor rescaled.** The closure was folded at the **NUCLEUS/VNS**
normalization — our fold against *their* Table 5 at *their* site. Rescaling it to the
primary 3 GW_th / 25 m normalization would destroy the comparison. No CaWO₄ or Al₂O₃ target
model was added; a test asserts it. (The pre-existing `veto_envelope.py` / `veto_credit.py`
mentions of Al₂O₃ are NUCLEUS's own (5 mm)³ cryodetector cubes from the Phase-8 geometry
gate, not a target model.)

The ratio **2.31 is normalization-independent** and is unaffected by that gap in a way the
407.7 absolute number is not — but 2.31 rests on the same unreproduced fold, so it inherits
the same label.

### 3.4 The milestone has **no background-side target-swap validation at all**

`VALD-11` was deleted by the 2026-07-22 re-scope. The signal-side closure above does **not**
substitute for it and must not be presented as if it did. This is a **real loss**, and it is
carried forward explicitly to **Phase 16 SC1** rather than papered over here.

---

## 4. The optional VNS context line (SC1) — **REPORTED, as a labelled scalar rescale**

It is **one multiplication applied to the finished primary result**. No second pipeline run,
no second flux table, no second spectral shape. `cevns.nucleus_variant_flux()` exists in the
codebase and is exactly the trap — it would have produced a physically reasonable second
spectrum and silently violated `fp-second-vns-run`. **It was not called**, and an AST walk of
both modules asserts that no call to it exists (a grep would not do: the name appears in
prose, because naming the trap is the point).

**Two candidate integral fluxes, both carried, because the project's own arithmetic does not
reproduce the NUCLEUS-stated one.**

| candidate | ∫Φ [ν̄/cm²/s] | rescale factor | source |
|---|---|---|---|
| **NUCLEUS-stated (2026)** | 2.100000 × 10¹² | **0.280158** | NUCLEUS Collab., EPJC **86**, 29 (2026), arXiv:2509.03559 — stated VNS integral flux |
| **project geometric** | 1.830269 × 10¹² | **0.244174** | `cevns.nucleus_flux_normalization()`, reconstructed from NUCLEUS's **own** 4.25 GW_th per core, 6 ν̄/fission, 200 MeV/fission at 72 m and 102 m (EPJC **79**, 1018 (2019), arXiv:1905.10258 §2) |

Project ∫Φ = **7.495760 × 10¹²** ν̄/cm²/s, from the frozen `reactor_flux_v1.0.csv`.

The two differ by **~15 %**, a gap already recorded in `state.json`. A bare unqualified
**0.28** would be fake precision on an optional context line (`fp-unlabelled-rescale`), so it
does not appear anywhere without both numbers beside it. Their 2019 prose "about 3 × 10¹²" is
a **third** number, 1.639× the geometric reconstruction, and is a locked forbidden proxy
(`fp-nucleus-3e12`); it is named here only as the gap it is.

**The rescaled 10–100 eV RoI rate** (reconstructed energy, on the finished plan-12-02
spectra):

| design | primary [counts/kg/day] | × 0.280158 | × 0.244174 |
|---|---|---|---|
| Ta→Al | 72.921 | 20.430 | 17.806 |
| Al→Hf | 73.144 | 20.492 | 17.860 |

Exact proportionality on every bin is asserted: the bin-to-bin ratio spread is
2.2 × 10⁻¹⁶, i.e. the float division round-trip. Any bin-dependent difference would mean a
second fold happened.

**Caveats travelling with the line.** The rescale is valid for the **total rate
normalization only**. It assumes the VNS spectral *shape* is the project's Phase-2 shape,
says nothing about duty cycle, and says nothing about site-dependent backgrounds. The VNS
also carries **2.92 m.w.e. of overburden** that the surface background treatment does not
have — which is precisely why the re-scope demoted this to a context line
(`fp-inherited-shielding`).

---

## 5. Phase-level verdict table — ROADMAP Phase 12 SC1–SC5

Clause by clause, in the Phase-11 style, with the measured number beside every verdict.
Plans 12-01 and 12-02's verdicts are pulled in so the phase closes in one place.

| # | Clause | Verdict | Measured | Owner |
|---|---|---|---|---|
| **SC1-a** | `dR/dE_rec` produced for both designs from 100 meV at the primary normalization, frozen `∫Φ` at 3 GW_th / 25 m surface, table **unmodified** | **PASS** | Both designs, `E_rec` from a few meV to ≈1 keV. Peaks ≈4.4 × 10³ (Ta→Al, 0.30 eV) and ≈4.7 × 10³ (Al→Hf, 0.19 eV) counts/kg/day/keV; 118.730 counts/kg/day integrated. Flux table byte-identical to `HEAD`. | 12-02 |
| **SC1-b** | IA broadening applied **before** the response chain | **PASS** | Applied once, on the recoil axis, upstream of the rebin and of `R`. `broaden=True` at the call site; `BROADENING_DEFAULT` still `False`. | 12-02 |
| **SC1-c** | 0.5 eV trigger curve applied **on top of** ε ≈ 0.5 | **PASS** | Exact factorisation on the deposit axis (bit-identical); `P_trig ≡ 1` reproduces the untriggered fold bit-for-bit; `P_trig` unmoved by an ε perturbation while `n_qp_yield` moves by exactly it. The literal end-to-end ε leg was **reformulated** (vacuous against a frozen `R`) and that is recorded. | 12-02 |
| **SC1-d** | If a VNS line is reported, it is a **single scalar rescale (≈0.28)** of the finished primary result, carries that factor as a visible label, never a second pipeline pass | **PASS** | One multiplication, exact proportionality to 2.2 × 10⁻¹⁶ on every bin. Both candidate factors carried: **0.280158** (NUCLEUS-stated 2.1 × 10¹²) and **0.244174** (project geometric 1.830269 × 10¹²). `nucleus_variant_flux()` never called (AST-asserted). | 12-03 |
| **SC2-a** | `dR/dT` is **flat** from 100 meV to 10 eV to within a few percent | **SUPERSEDED BY MEASUREMENT** | Falls **monotonically by 44.30 %** across that window. Deficits 0.93 % / 1.72 % / 3.94 % / 12.82 % / **44.30 %** at 0.0999 / 0.15 / 0.29 / 1.0 / 10.0 eV. Physically correct: `E_min(T) ∝ √T` cuts low-energy flux out of the fold. Window **not** narrowed. | 12-01 |
| **SC2-b** | …and equals the analytic `T→0` plateau computed from the frozen `∫Φ` with the flat-box `dσ/dT` | **PASS** | Analytic plateau **2372.3683** counts/kg/day/keV from `∫Φ = 7.495760 × 10¹²`, built independently of the fold. `dR/dT(0.0999350 eV)/plateau = 0.99069`. | 12-01 |
| **SC2-c/d** | Both failure modes (rising toward low `T`; falling to zero) unit-tested, not eyeballed | **PASS** | Monotone non-increasing and bounded above by the plateau everywhere; no zero bins, ratio 0.9907, no order-of-magnitude neighbour step. Asserted. | 12-01 |
| **SC3-a** | Above ~10 eV the extended pipeline reproduces the frozen v1.0 CEvNS CSVs to **<1 %** | **PARTIAL** | **Ta→Al 0.7648 %** — passes. **Al→Hf 3.7246 %** — **fails**, in exactly one bin: the last populated one, at the kinematic endpoint, at 7.9 × 10⁻⁷ counts/kg/day/keV. Below 900 eV both are inside the target (0.7648 % / 0.5557 %). The residual is the Phase-10 **response-matrix regeneration**, not the broadening: turning the kernel off changes it by 0.001 percentage points. Target **not** relaxed. | 12-03 |
| **SC3-b** | `T = 0.290 eV` reproduces the frozen v1.0 value **exactly** | **RESTATEMENT — not counted as independent corroboration** | The frozen recoil table's support **starts at 5 eV** (320 rows, 5–3200 eV), confirmed programmatically. No such frozen value exists; no comparison at 0.290 eV is claimed. The clause's physical content restates SC4's zero-point. | 12-03 |
| **SC4-a** | Truncation bound **computed** with the project's own Φ, flat continuation at 100 keV, including `(1 − MT/2E²)` | **PASS** | Computed per isotope from the frozen table and `cevns.dsigma_dT`; the flat continuation is **shown** conservative from the table's own slope, `d log Φ/d log E` = +0.0635…+0.0763. `E²` continuation gives 0.5804 % < 0.8027 %. | 12-01 |
| **SC4-b** | reproducing **≤0.81 % at `T` = 100 meV** | **PASS** | **0.8027 %** at the 0.0999350 eV grid floor; **0.8020 %** at exactly 100 meV. | 12-01 |
| **SC4-c** | **and exactly zero above 0.29 eV** | **PARTIAL — reconciled, not rounded** | Exactly `0.0` only above **0.3067 eV**, set by the lightest isotope ⁷⁰Ge. At 0.29 eV a residual of **8.84 × 10⁻⁶** survives, carried by **four** still-open isotopes (⁷⁰, ⁷², ⁷³, ⁷⁴Ge) — correcting planning finding F2, which attributed it to ⁷⁰Ge alone. The roadmap's 0.29 eV is essentially ⁷⁴Ge's own zero point, 0.290146 eV. | 12-01 |
| **SC4-d** | The flux table is **not** extended | **PASS** | 101 knots, floor 0.1 MeV, data rows byte-identical to `HEAD`; source scan finds no write/append/synthetic-knot path. | 12-01 |
| **SC4-e** | `E_min(100 meV)` = **58.16 keV** adopted, reconciled against 58.7 keV (⁷⁴Ge-only) | **PASS — with the adoption changed and stated** | All three reproduced from their masses: **58.1914** (Phase-7 abundance-weighted, **adopted**), **58.1612** (CONVENTIONS §D molar mass 72.63 u — the roadmap's figure), **58.7072** (⁷⁴Ge only). Spread 0.936 %, entirely the mass spread. | 12-01 |
| **SC5-a** | Ge/CaWO₄ same-pipeline ratio **2.31** documented, naive compound `N²/A` **1.95** explicitly rejected (CaWO₄ compound 44.2, **not** 65.8 which is pure W) | **PASS** | Recomputed independently: Ge **22.729**, CaWO₄ compound **44.193**, ratio **1.944**, pure W **65.627** (standard atomic weight) / **65.761** (¹⁸⁴W — which is where the literature's 65.8 comes from). 1.95 rejected with its physical reason. | 12-03 |
| **SC5-b** | The already-passed 14 % signal-side closure is **cited as prior evidence, not recomputed, with its scope stated** | **PASS — with a named provenance gap** | Cited against Table 5 at 100 % duty (356.5), never the §2 prose 280. Scope stated: flux × cross-section × target chain only, nothing about any environment or background. **Provenance gap:** a word-bounded repository search finds 407.7 **only** in GPD prose — no code, test, notebook or artifact reproduces it. Labelled an unreproduced prior assertion. | 12-03 |
| — | Background-side target-swap validation | **ABSENT — carried to Phase 16 SC1** | VALD-11 was deleted by the re-scope. The milestone has **none**, and the signal-side closure does not substitute for it. | 12-03 |

**Summary of the phase:** 13 PASS, 1 SUPERSEDED, 2 PARTIAL, 1 RESTATEMENT, 1 recorded
ABSENCE. Neither PARTIAL was converted into a PASS by widening a tolerance or narrowing a
window.

---

## 6. Checkpoint record (Task 3, `checkpoint:human-verify`)

**Status: recorded, NOT approved.** The user issued a standing session-level directive
(2026-07-22) to run the roadmap to completion without per-phase discussion unless a genuine
blocker arises. No blocker arose. The checkpoint content is recorded here in full and
execution continued. **No approval was given and none is recorded.** Resume-signal idiom that
*would* have been presented: `[Y/n/e]` (Enter = Y).

**One-line summary presented:** the extended pipeline leaves the validated v1.0 results
untouched to 0.765 % (Ta→Al) but exceeds the <1 % target in a single endpoint bin for Al→Hf
at 3.72 % — traced to the Phase-10 response-matrix regeneration, not to anything Phase 12
added; SC3's 0.290 eV clause is a restatement with no frozen value behind it; the compound
arithmetic reproduces and the naive 1.95 ratio is rejected in favour of 2.31; and the VNS
line is reported as one labelled multiplication carrying both 0.280158 and 0.244174.

**Review question put to the researcher (unanswered):**

> *"The milestone's only signal-side target-swap validation (CaWO₄ 407.7 dru, ratio 1.14) has
> no reproducible artifact in this repository, and since VALD-11 was deleted there is no
> background-side validation at all. Phase 12 cites the closure with that gap stated. Is
> citing-with-a-gap sufficient for the milestone's decisive signal deliverable, or should the
> CaWO₄ fold be reconstructed before Phase 16 leans on it?"*

**Items flagged for attention:**

1. **SC3-a is PARTIAL, not PASS.** Al→Hf exceeds <1 % in one endpoint bin. The cause is a
   Phase-10 inheritance (regenerated `R`), not a Phase-12 change — but the gate as written is
   not met and is not being reported as met.
2. **The regression tests plumbing, not the sub-eV physics.** Above 10 eV the broadening is
   sub-bin. **Nothing in Phase 12 tests the bottom decade against an independent object.**
3. **The 407.7 closure and the 2.31 ratio are unreproduced prior assertions** in this
   repository, and the milestone has **no** background-side validation at all.

---

## 7. Standing items carried out of Phase 12

- **To Phase 16 SC1:** the milestone has no background-side target-swap validation. State it;
  do not let the signal-side closure stand in for it.
- **To the orchestrator (not acted on here):** `REQUIREMENTS.md` cites a *"Locked scenario
  change (CONVENTIONS §D): 2 × 4.25 GW_th at 72 m and 102 m"*. **That lock never happened** —
  §D still locks 3 GW_th / 25 m and is unchanged. No plan in this phase edits
  `REQUIREMENTS.md` or `CONVENTIONS.md`.
- **Open review question from 12-02:** whether the ×1.164 moment-corrected width should become
  central (and §J be amended) or remain a one-sided upper band.
- **Open review question from 12-01:** whether "approaches the analytic plateau within 1 % at
  the axis floor, monotone, neither rising nor collapsing" is the right restatement of the
  VALD-10 plateau gate.
- **Unrepaired:** the bottom-decade convolution accuracy; the independence of the counting
  floor and the IA width; and the fold's per-isotope quadrature accuracy at the 0.8 % level.
