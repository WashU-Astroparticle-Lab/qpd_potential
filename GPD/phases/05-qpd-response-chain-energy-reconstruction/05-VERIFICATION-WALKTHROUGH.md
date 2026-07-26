# Phase 5 — Verification Walkthrough (single document)

**Phase:** QPD Response Chain & Energy Reconstruction
**Status:** executed, pending your verification
**Purpose:** one document to walk through and independently confirm the Phase-5 work. Everything below is runnable; numbers are re-derived from the committed code + artifacts, not copied from prose.

Run all commands from the project root:
`/Users/lanqingyuan/Documents/GitHub/qpd_potential/.claude/worktrees/qpd-cevns-muon-spectrum-aaa8da`

---

## 0. TL;DR — two commands

```bash
# (a) the full unit-test suite (Phase-5 tests are test_response_chain.py + test_response_matrix.py)
python3 -m pytest tests/test_response_chain.py tests/test_response_matrix.py -v

# (b) the headline-claims harness: re-derives every decisive number and prints PASS/FAIL
python3 scripts/verify_phase5.py
```

`verify_phase5.py` currently prints **24/24 checks passed** (exit 0). Its output is reproduced in §3. If you only have five minutes: run these two, then read the **Caveats** in §5 — those are the parts that need *judgment*, not just a passing test.

---

## 1. What Phase 5 was supposed to deliver (the contract)

From `GPD/ROADMAP.md` / `GPD/REQUIREMENTS.md`:

- **SIMU-01** — forward QPD response chain (E_dep → ~50% signal → trapped-QP → EMG tunneling burst → 50 kHz/25 kHz censoring → E_rec) for **both** designs (Ta→Al, Al→Hf); report the linear→saturated **crossover** deposit energy per design.
- **SIMU-02** — Monte-Carlo response matrix **R(E_rec | E_dep)** per design, convergence ≤~3%/cell, spanning threshold → saturated.
- **VALD-04** — limiting cases: **E_rec ≈ 0.5·E_dep** at low energy; **saturation onset** once the tunneling rate exceeds 25 kHz.
- **Forbidden proxy `fp-no-saturation`** — the saturation must be *modeled*; you must not linearly extrapolate rate→energy across the muon range and fake a peak at the ceiling.
- **Anchors:** `ref-qpd-paper` (arXiv:2405.17192 — pulse model, Table II) and `ref-qpd-repo` (the `qpd` repo EMG burst template — **must reuse**).

"Done" = both designs, both censoring variants, R built and normalized, the two limiting cases hold, the crossover reported, and saturation genuinely modeled — **with the honest caveat (§5) that the saturated-regime *shape* has no literature benchmark.**

---

## 2. Deliverables to inspect (artifact index)

| Artifact | What it is |
|---|---|
| `src/qpd_potential/response.py` | Forward chain + **count-integral E_rec estimator** (replaces the Phase-1 `NotImplementedError` stub) |
| `src/qpd_potential/response_matrix.py` | MC builder for R(E_rec\|E_dep) |
| `artifacts/stage1/response_matrix_TaAl.npz`, `..._AlHf.npz` | The response matrices — both censoring variants each |
| `artifacts/stage1/energy_response.pdf` | **deliv-fig-response**: E_rec vs E_dep, saturation onset marked, both designs × both variants |
| `artifacts/stage1/ASSUMPTIONS.md` (Phase-5 append) | The design-number/band statement + caveats |
| `tests/test_response_chain.py`, `tests/test_response_matrix.py` | 57 acceptance/unit tests for this phase (36 + 21) |
| `GPD/phases/05-.../05-01-SUMMARY.md`, `05-02-SUMMARY.md` | Per-plan self-reports with `uncertainty_markers` |
| `scripts/verify_phase5.py` | The harness in §3 |

---

## 3. Claim-by-claim verification

Each row: the claim, the expected result, the exact way to check it, and what a pass *proves*. The harness output (below) is the live evidence; each check is also a named pytest.

```
$ python3 scripts/verify_phase5.py
  PASS  [gate] Ta->Al trapping_gate_ok                 Delta_abs/Delta_tr >= 2.0
  PASS  [gate] Al->Hf trapping_gate_ok                 Delta_abs/Delta_tr >= 2.0
  PASS  [VALD-04 low-E] Ta->Al E_rec/E_dep@1eV         0.4981 (target 0.5)
  PASS  [VALD-04 low-E] Al->Hf E_rec/E_dep@1eV         0.4971 (target 0.5)
  PASS  [SIMU-01 crossover] Ta->Al default onset eV    default 52.9 eV in band [8.0, 930.9]
  PASS  [SIMU-01 crossover] Al->Hf default onset eV    default 32.1 eV in band [4.8, 565.4]
  PASS  [SIMU-01] Hf saturates before Ta->Al (default) Al->Hf 32.1 eV < Ta->Al 52.9 eV
  PASS  [SIMU-01] Hf-first across full f_prompt x r scan   25-point scan
  PASS  [fp-no-saturation] Ta->Al/non_paralyzable E_rec@197MeV  34.8 keV = 3.53e-04 x linear
  PASS  [fp-no-saturation] Ta->Al/paralyzable E_rec@197MeV       3.3 keV = 3.31e-05 x linear
  PASS  [fp-no-saturation] Al->Hf/non_paralyzable E_rec@197MeV  26.8 keV = 2.73e-04 x linear
  PASS  [fp-no-saturation] Al->Hf/paralyzable E_rec@197MeV       2.6 keV = 2.61e-05 x linear
  PASS  [variant divergence] ... paralyzable < non_paralyzable @tail (both designs)
  PASS  [stop-cond] Ta->Al peak Gamma_in >> 25 kHz @197 MeV   9.31e+10 Hz vs 25000 Hz
  PASS  [stop-cond] Al->Hf peak Gamma_in >> 25 kHz @197 MeV   1.53e+11 Hz vs 25000 Hz
  PASS  [Pitfall-1 eventcount] expected_event_count != N_qp (both designs)
  PASS  [SIMU-02 matrix] TaAl/AlHf both variants present + columns normalize + span
  24/24 checks passed
```

### 3.1 Low-energy linearity — VALD-04 low limit
- **Expected:** E_rec/E_dep → ε = 0.5 well below the saturation onset.
- **Check:** `python3 -c "import sys;sys.path.insert(0,'.');from src.qpd_potential import response as R;print(R.E_rec(1.0,'Ta->Al','non_paralyzable')/1.0)"` → **0.4981**. Test: `test_low_e_linear`.
- **Proves:** the estimator is correctly calibrated in the regime where reconstruction is trustworthy. *Note:* this is **calibration-consistency**, not an independent measurement — the single global constant `C` per design is *fixed* to make this slope 0.5 (see `calibrate_C`). It confirms the calibration is self-consistent, not that 0.5 is externally validated.

### 3.2 Saturation is modeled, not faked — `fp-no-saturation` (the key claim)
- **Expected:** at the 197 MeV muon tail, E_rec is **3–4 orders of magnitude below** the linear 0.5·E_dep line (= 98.5 MeV), for **both** variants:
  - non-paralyzable → **plateau** ~34.8 keV (Ta→Al) / ~26.8 keV (Al→Hf)
  - paralyzable → **rollover** ~3.3 keV / ~2.6 keV
- **Check:** `test_high_e_plateau`, `test_variant_divergence`; or the harness `[fp-no-saturation]` rows.
- **Proves:** the response does **not** ride the linear line up to a fake peak at the ceiling. The two variants diverge (~10×) exactly as the OPEN censoring switch predicts.

### 3.3 Stop-condition has teeth
- **Expected:** the on-spot peak Γ_in at 197 MeV exceeds the 25 kHz ceiling by ~10⁶–10⁷× (9.3×10¹⁰ / 1.5×10¹¹ Hz), and **with censoring turned off** the count-integral is exactly linear (0.5·E_dep, no plateau).
- **Check:** harness `[stop-cond]` rows; the "censoring OFF ⇒ exactly linear" scratch check is in `test_high_e_plateau` / 05-01 SUMMARY.
- **Proves:** the plateau/rollover is *caused by the censoring model*, not by a numerical artifact — and the roadmap stop-condition ("no saturation even when rates ≫ 25 kHz ⇒ model wrong") does **not** trigger.

### 3.4 The load-bearing pitfall — event-count mapping (Pitfall 1)
- **Expected:** the Poisson mean fed to `QuasiparticleBurstModel.expected_n_qp` is the **tunneling-event count** ∫Γ_in dt = K·τ_qp·N_qp/v_tr, **not** the trapped-QP count N_qp. (For N_qp=10⁴: event count 300 (Al) / 80 (Hf), i.e. the factor 0.03 / 0.008 — *not* 10⁴.)
- **Check:** `test_eventcount_mapping`; harness `[Pitfall-1]` rows; read `expected_event_count` in `response.py:216`.
- **Proves:** the saturation is scaled from the right quantity — feeding N_qp would mis-scale the entire response.

### 3.5 Crossover as a band — SIMU-01
- **Expected:** default onset **~52.9 eV (Ta→Al) / ~32.1 eV (Al→Hf)** at f_prompt=0.3, inside a band spanning ~5 eV to ~0.9 keV over the f_prompt∈[0.1,0.5], r∈[1,5] scan (equal-split anchor ~13/7.9 keV; whole-array plateau ~18.6/11.3 keV). **Hf saturates first everywhere.**
- **Check:** `test_crossover_band`, `test_hf_first`; harness `[SIMU-01]` rows.
- **Proves:** the crossover is reported honestly as an uncertainty band (it rides on the low-confidence sharing params f_prompt/r), with the default point as SIMU-01's "explicit design number." Hf-first is robust across the whole scan.

### 3.6 Ta gap = binary trapping gate (not a fabricated film value)
- **Expected:** `trapping_gate_ok` asserts Δ_abs/Δ_tr = 3.58 ≥ 2 (α-phase Ta, T_c ≥ ~2.5 K); the response is **numerically invariant** to the Ta absorber gap above the gate (yield/rate/onset all use the Al *trap* gap).
- **Check:** `test_ta_gate`; harness `[gate]` rows.
- **Proves:** the Phase-1 "Ta params absent" flag is handled correctly — kept as a cited bulk-α baseline with a guard, **no film value invented**, and the design's numbers don't secretly depend on it (β-phase Ta would trip the gate and invalidate the design premise, which the assert catches).

### 3.7 Response matrix R(E_rec|E_dep) — SIMU-02
- **Expected:** each `.npz` holds `R_non_paralyzable` **and** `R_paralyzable`, shape 161×584, every E_dep column sums to 1, E_dep span 10 eV → 197 MeV.
- **Check:** harness `[SIMU-02 matrix]` rows; `test_response_matrix.py` (`test_convergence`, `test_span`, `test_both_variants`, `test_repro`, `test_fig_content`, `test_variant_divergence`). Convergence: peak populated cell ≤~1.8% at N_s=5000, clean 1/√N scaling.
- **Proves:** the deliverable matrix is complete, normalized, reproducible, and carries both censoring variants (the OPEN switch is *not* silently closed).

### 3.8 The figure — `deliv-fig-response`
Open `artifacts/stage1/energy_response.pdf`. You should see E_rec vs E_dep for both designs, both censoring variants, with the saturation onset marked and the low-E 0.5·E_dep line for reference. `test_fig_content` asserts the figure's data content matches the matrices.

---

## 4. Reproduce from scratch (optional)

The matrices and figure regenerate deterministically (fixed, process-stable seeding):

```bash
python3 -m src.qpd_potential.response_matrix   # or: python3 scripts/<generator>  (see 05-02-SUMMARY.md "Files")
git status --porcelain                          # should be clean if regeneration is bit-stable
```

(If you regenerate, note: running the full `pytest tests/` suite currently re-stamps the `git_sha:` header of the two *frozen* Phase-2 flux CSVs — a known cosmetic quirk unrelated to Phase 5, already flagged as a separate cleanup task. `git checkout -- data/flux/*.csv` restores them.)

---

## 5. Caveats — the parts that need YOUR judgment (read these)

These are recorded in the SUMMARYs' `uncertainty_markers` and `ASSUMPTIONS.md`; they are **not** things a passing test can settle:

1. **No literature anchor for the saturated regime.** There is no published QPD response result at *any* energy in the saturated regime. Validation is therefore **limiting-cases + calibration-consistency only** (§3.1–3.3). The *shape of the response curve between the limits is a model prediction*, not a benchmarked result. This is inherent to the phase (your roadmap designated Phase 5 HIGH-risk for exactly this) — but it means the mid-curve should be read as "model says," not "measured."

2. **Deep-saturation fluctuation is modeled, not realized.** For very large deposits the EMG event train would be O(10⁸) events (computationally infeasible), so in that regime the per-sensor spread is drawn **Poisson about the analytic censored-count mean** (with the mean pinned to the validated 05-01 estimator). The spread there is ~10⁻³ of the column mean (immaterial to R), but it means the deep-saturation column *shape* is the analytic estimator, not a full microphysical MC. The `EC_EMG_MAX` split (real EMG train below it, Poisson approximation above) is documented in `response_matrix.py`.

3. **Crossover rides on low-confidence sharing parameters.** f_prompt and r have no thin-wafer QPD measurement; they set the crossover scale, hence the ~3-orders-of-magnitude band rather than a single number. The default point (52.9/32.1 eV) is a *choice of nominal*, not a measured value.

4. **The paralyzable vs non-paralyzable censoring switch — RESOLVED (2026-07-21).** It cannot be closed from first principles, but by user decision at this Phase-5 review the project now **lives in non-paralyzable** (CONVENTIONS §F; `params.DEFAULT_CENSORING = "non_paralyzable"`). Both variants were computed in Phase 5; the paralyzable R matrices remain in `response_matrix_*.npz` as a retained sensitivity/alternative, but Phase 6 and downstream use **non-paralyzable** as the single canonical variant. The plateau (~34.8/26.8 keV at the muon tail) is therefore the operative high-E response; the paralyzable rollover is no longer carried as a live switch.

If you're comfortable with these four being *documented model limitations of a stage-1 study* (not silent assumptions), Phase 5 is sound. If any of them needs to be tightened before you'd trust the deliverable, that's the place to push back.

---

## 6. Sign-off checklist

- [ ] `pytest tests/test_response_chain.py tests/test_response_matrix.py -v` → all pass
- [ ] `python3 scripts/verify_phase5.py` → 24/24
- [ ] `energy_response.pdf` shows plateau/rollover (not a linear ramp to a ceiling peak), both designs, both variants
- [ ] Read §5 caveats 1–4 and accept them as stage-1 limitations (or flag)
- [ ] (optional) spot-read `response.py:E_rec` and `expected_event_count` to confirm the estimator + event-count mapping
