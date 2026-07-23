# Phase 12 Context — Reactor CEvNS down to 100 meV at the Paper's Surface Scenario (P-SIG)

**Status:** No `/gpd:discuss-phase` session was run for this phase.
**Recorded:** 2026-07-22, during autonomous roadmap execution.

## Provenance of this file

This file is **not** a transcript of a discussion with the user. It exists to record,
honestly and auditably, what the binding intent for Phase 12 actually is, given that the
user issued a standing session directive to run the roadmap to completion without
per-phase discussion unless a genuine blocker arises.

**No new user decisions were collected while writing this file.** Everything in the
*Decisions* section below is transcribed from artifacts that already existed before this
session's planning began — principally `GPD/ROADMAP.md` (the 2026-07-22 re-scope banner and
the Phase 12 section), `GPD/REQUIREMENTS.md`, `GPD/CONVENTIONS.md` §D/§I/§J, and
`GPD/state.json` `project_contract`. The *Planning findings* section below is new, and is
labelled as such: it was produced by running the project's own code during planning, not by
consulting the user.

<domain>
## Phase Boundary

Produce the reactor-CEvNS differential rate `dR/dE_rec` for **both** trapping designs
(Ta→Al, Al→Hf) from **100 meV** upward at the **primary** normalization — the paper's own
3 GW_th / 25 m surface scenario, `∫Φ = 7.5×10¹² ν̄/cm²/s`, taken from the frozen
`data/flux/reactor_flux_v1.0.csv` **unmodified** — with the Phase-11 impulse-approximation
broadening applied *before* the response chain and the Phase-10 0.5 eV trigger curve applied
*on top of* ε ≈ 0.5. Deliver alongside it the computed sub-100-keV flux-truncation bound, the
sub-eV validity gates, the plateau and regression reports, and (optionally) the NUCLEUS VNS
siting as a single **labelled scalar rescale** of the finished primary result.

Requirements: **CALC-17**, **CALC-25**, **VALD-10**

</domain>

<contract_coverage>
## Contract Coverage

Advances project-contract claim `claim-cevns`. This is the milestone's decisive **signal**
deliverable.

- **CALC-25 (decisive):** `dR/dE_rec`, both designs, 100 meV upward, primary normalization,
  broadening before the response chain, trigger on top of ε. Success = the spectra exist as
  committed artifacts with the sub-eV regime boundary labelled on every one of them.
- **CALC-17:** the sub-100-keV truncation bound is **computed** with the project's own Φ under
  a flat continuation at the 100 keV table value, including the `(1 − MT/2E²)` factor. Success
  = a number with a stated conservatism argument. **The flux table is not extended.**
- **VALD-10 (plateau):** `dR/dT` approaches the analytic flat-box `T→0` plateau computed
  independently from the frozen `∫Φ`. Success = the plateau value matched at the bottom of the
  axis *and* the two failure modes excluded by assertion, not by inspection.
- **VALD-10 (regression):** above ~10 eV the extended pipeline reproduces the committed frozen
  v1.0 CEvNS artifacts to **<1%**.
- **Benchmark:** the Ge/CaWO₄ same-pipeline ratio **2.31** documented, with the naive compound
  N²/A ratio **1.95** explicitly rejected.
- **False progress to reject:** see *Forbidden proxies* below. The two that bite hardest here
  are `fp-second-vns-run` (the VNS is a multiplication or it is not reported) and extending the
  reactor flux table below 100 keV (report the bound instead).

</contract_coverage>

<user_guidance>
## User Guidance To Preserve

- **Standing directive (session-level, 2026-07-22):** run the roadmap to completion without
  per-phase discussion unless a genuine blocker arises. Checkpoints are still placed and their
  content recorded in full; no approval is fabricated. This follows the Phase 8 and Phase 11
  precedent.
- **Re-scope decision, verbatim (2026-07-22):** *"Just take the approximation as was done in
  the paper. I don't need a very accurate result."* "The paper" is this project's own v1.0
  manuscript. Accuracy is explicitly **not** required: prefer closed-form folds and bounded
  estimates over regularized inversion, digitization campaigns, or over-determination tests.
- **Display floor (2026-07-22):** spectra run **down to 100 meV**. The earlier "never display
  below 10 eV" rule is **retracted** and must not be reintroduced as a physics statement.
- **Must-have references / prior outputs:** the frozen `data/flux/reactor_flux_v1.0.csv`;
  `CONVENTIONS.md` §D (3 GW_th / 25 m, **unchanged**), §I (trigger curve), §J (phonon scale);
  the Phase-10 744-bin extended axis and regenerated `R(E_rec|E_dep)`; the Phase-11 IA
  broadening and its leakage budget; the frozen v1.0 CEvNS artifacts in `artifacts/stage1/`.
- **Evidence discipline (project-standing):** every quoted number must be traceable to a
  locally frozen artifact via a recorded, reproducible command. `WebFetch` is not a quote
  source — two verified factual errors came from it in Phase 8.

</user_guidance>

<decisions>
## Decisions (LOCKED — carried from prior artifacts, not newly elicited)

### 1. The five ROADMAP Phase 12 success criteria are binding verbatim

See `GPD/ROADMAP.md`, section *"### Phase 12: Reactor CEvNS down to 100 meV at the Paper's
Surface Scenario (P-SIG)"*. They are the definition of done. Where a success criterion is
found to conflict with what the code actually produces, the resolution is to **report the
supersession with numbers**, following the Phase-11 precedent — never to tune a tolerance
until the criterion passes. See *Planning findings* below, where exactly this has already
happened once.

### 2. Normalization

- **Primary and only pipeline normalization:** the frozen `data/flux/reactor_flux_v1.0.csv`
  at 3 GW_th / 25 m, surface, unshielded, used **as-is**. `CONVENTIONS.md` §D stands unchanged;
  no CONVENTIONS amendment is needed for this milestone's normalization.
- **The NUCLEUS VNS line is optional and is a scalar multiplication** of the finished primary
  result, carrying its factor as a visible label. It is never a second pipeline run, never a
  second flux table, never a second spectral shape. `cevns.nucleus_variant_flux()` exists in
  the codebase and **must not be called on this line**.
- `REQUIREMENTS.md` cites a "Locked scenario change (CONVENTIONS §D): 2 × 4.25 GW_th at 72 m
  and 102 m". That lock **never happened**. It is a live discrepancy flagged for the
  orchestrator; it is **not** a licence to treat the VNS scenario as locked, and no plan in
  this phase edits `REQUIREMENTS.md`.

### 3. Physics inputs inherited and not re-decided here

- **Phonon scale (CONVENTIONS §J, locked in Phase 11):** `ω̄ = 17.8597 meV` (harmonic VDOS
  mean), `⟨u_x²⟩ = 1.6096194483e-3 Å²`, `2W = q²⟨u_x²⟩`. Never re-chosen in this phase.
- **The rate is never multiplied by `e^(−2W)`.** Milestone-wide prohibition.
- **Trigger curve (CONVENTIONS §I):** Hill form, `E50 = 0.5 eV` exactly, sharpness `k` default
  4.0 with a declared scan range `[1, 12]`, regime boundary `1.0 eV`. `P_trig` multiplies on
  top of ε ≈ 0.5 and never replaces it. §I imposes a **standing sensitivity obligation**: every
  downstream result computed with this curve must be reported together with its sensitivity to
  `k` over `[1, 12]`. Phase 12 is the first such result, so the obligation lands here.
- **Grid:** Phase-10 extended axis, 744 bins, floor `0.0999350 eV`, first centre
  `0.1013838 eV`. `shared_energy_grid` still **defaults to `v1.0`**; the extended axis is
  opt-in via `version="v2.0-ext"`.
- **Broadening switch:** `ia_broadening.BROADENING_DEFAULT = False`. **Phase 12 must turn it
  on deliberately**, and record that it did.

### 4. Ordering

Broadening acts on `dR/dE_R` on the **recoil** axis, upstream of
`fold.rebin_cevns_to_edep_grid` and therefore upstream of `R(E_rec|E_dep)`. The trigger curve
acts **after** the response chain, as an analysis efficiency. Neither ordering is negotiable.

### 5. Agent's Discretion

- Module decomposition, test design, artifact layout, and figure styling.
- The recoil-axis resolution used to build the extended `dR/dT` table, provided the leakage
  boundary sits at the extended-grid floor so it is the boundary Phase 12 actually sees.
- How to structure the truncation-bound calculation, provided the bound is *computed* from the
  project's own Φ and the flux table is not extended.
- Whether the VNS secondary line is reported at all. If it is, its form is fixed (a labelled
  scalar rescale of the finished primary result).

</decisions>

<planning_findings>
## Planning Findings (NEW — produced during planning by running the project's own code)

These were not known when the roadmap was written. Each is reproducible with
`/opt/anaconda3/bin/python3` against the committed source and frozen tables.

### F1. ROADMAP SC2's flatness clause is FALSE as literally written — 44%, not "a few percent"

SC2 asserts *"dR/dT is **flat** from 100 meV to 10 eV to within a few percent"*. Measured
against the analytic flat-box `T→0` plateau `2372.368` counts/kg/day/keV (computed here from
the frozen `∫Φ = 7.4958×10¹²` with the form factor off and the `(1 − MT/2E²)` factor dropped):

| T | dR/dT | /plateau | deficit |
|---|---|---|---|
| 0.0999 eV | 2350.274 | 0.9907 | **0.93%** |
| 0.15 eV | 2331.449 | 0.9828 | 1.72% |
| 0.29 eV | 2278.808 | 0.9606 | 3.94% |
| 1.0 eV | 2068.300 | 0.8718 | 12.82% |
| 10.0 eV | 1321.367 | 0.5570 | **44.30%** |

The spectrum is monotonically **falling** with T across the whole window, which is the
physically correct behaviour: `E_min(T)` rises as `√T`, progressively cutting the low-energy
flux out of the integral. The plateau is *approached* below ~0.15 eV, not held to 10 eV.

**What is actually decisive and does hold:** `dR/dT` at the bottom of the axis sits within
**0.93%** of the independently computed analytic plateau; it does **not rise** toward low T
(which would be an extrapolation artifact); and it does **not fall to zero** (which would be a
table floor). Those three are the real physics content of VALD-10's plateau leg, and all three
are checkable. SC2's "few percent to 10 eV" clause must be reported **SUPERSEDED BY
MEASUREMENT** with these numbers, in the Phase-11 style — not narrowed silently until it
passes, and not restated with a widened tolerance.

### F2. The truncation bound reproduces, and its zero-point is isotope-resolved

Computed per isotope under a flat continuation of Φ at its 100 keV value including
`(1 − MT/2E²)`: **0.803%** at `T = 0.0999350 eV` (roadmap: ≤0.81% ✓), falling to 0.383% at
0.15 eV and **0.001%** at 0.29 eV. It is **not** exactly zero at 0.29 eV: the lightest isotope
⁷⁰Ge (M = 65204.58 MeV) still has `E_min < 100 keV` there. Exact zero requires `E_min > 100 keV`
for *every* isotope, which happens near **T ≈ 0.307 eV**. The roadmap's "exactly zero above
0.29 eV" is the natural-mean-mass statement; the isotope-resolved threshold is slightly higher
and must be reconciled rather than rounded over.

### F3. `E_min(100 meV)` — three values in circulation, all reconcilable

- **58.19 keV** from the project's own frozen abundance-weighted natural mass
  (`m_N c² = 6.7724551×10¹⁰ eV`, Phase-7 lock) via `cevns.E_min_MeV`.
- **58.16 keV** as quoted by the roadmap — corresponds to `M = 72.63 u`, the *molar-mass*
  natural Ge of `CONVENTIONS.md` §D, a 0.05% different mass.
- **58.7 keV** the project-frozen ⁷⁴Ge-only value.

None is wrong; they are three different masses. The phase must state which one it adopts and
show the other two are consistent with it, rather than asserting one.

### F4. The flat-continuation conservatism claim is checkable from the frozen table itself

The bound is only an *upper* bound if Φ does not rise as E falls below 100 keV. The frozen
table shows Φ **decreasing** toward the floor — 3.5046×10¹² at 0.1259 MeV, 3.4628×10¹² at
0.1080 MeV, 3.4460×10¹² at 0.1000 MeV — so a flat continuation at Φ(100 keV) over-estimates
the missing flux and the bound is genuinely conservative. **This is a real disconfirming check,
not an identity:** had the local slope run the other way, the ≤0.81% figure would not be an
upper bound at all and CALC-17 would need restating.

### F5. SC3's `T = 0.290 eV` clause is very close to a restatement of SC4

SC3 asks that `T = 0.290 eV` *"reproduces the frozen v1.0 value exactly"*. But (a) the frozen
`artifacts/stage1/cevns_dRdT.csv` support **starts at 5 eV**, so there is no frozen v1.0 value
at 0.290 eV to compare against; and (b) the physical content of the clause — that nothing
changes above 0.29 eV — is the *same statement* as SC4's "the truncation bound is exactly zero
above 0.29 eV". Phase 11 found three such roadmap "cross-checks" that were algebraic identities.
This is a fourth candidate. It must be reported as a restatement with its scope, not counted as
independent corroboration.

### F6. `run_fold` cannot be reused unchanged — it needs all three channels

`fold.run_fold` folds CEvNS **and** muon **and** Compton, and raises if the muon/Compton
deposit grids do not match the response-matrix `E_dep` centres. Those channels are still on the
584-bin v1.0 axis; carrying them onto the extended axis is **Phase 15's** job. Phase 12
therefore needs a CEvNS-only extended fold entry point. Additionally
`rebin_cevns_to_edep_grid` reads the frozen 5 eV-floored `cevns_dRdT.csv` by default, and
`broaden_native_spectrum(require_floor_coverage=True)` correctly **raises** on that table at
the 0.0999350 eV floor — so Phase 12 must supply an extended-axis `dR/dT` table, in the frozen
8-column layout (`fold.read_cevns` reads columns 0, 6, 7), and must feed it **unbroadened** so
that the existing wiring applies the kernel exactly once.

### F7. The 407.7 dru CaWO₄ closure has no reproducible artifact in this repository

A repository-wide search finds `407.7` **only** in GPD prose documents (`literature/SUMMARY.md`,
`PROJECT.md`, `STATE.md`, `state.json`, `ROADMAP.md`, `REQUIREMENTS.md`, the Phase-8 gate
verdict). There is no CaWO₄ module, no test, no notebook cell, and no committed artifact that
produces it, so no reproducible command exists. The roadmap correctly says to **cite, not
re-run** it — but under the project's own evidence discipline the citation must carry that
provenance gap explicitly. Note also that the closure was folded at the **NUCLEUS/VNS**
normalization (comparing our fold to *their* Table 5 at *their* site); it must not be rescaled
to the primary normalization, which would destroy the comparison. The Ge/CaWO₄ ratio 2.31 is
normalization-independent and is unaffected by this.

### F8. The VNS rescale factor rests on a number the project's own arithmetic does not reproduce

The rescale `2.1×10¹² / 7.5×10¹² ≈ 0.28` uses the NUCLEUS 2026 paper's stated VNS integral
flux. The project's own `cevns.nucleus_flux_normalization()` — built from NUCLEUS's own stated
4.25 GW_th per core, 6 ν̄/fission, 200 MeV/fission, at 72 m and 102 m — returns
**1.830269×10¹²**, which would give a rescale of ≈0.244 instead. Both numbers are already
recorded in `state.json` ("their own Fig. 1 follows the geometric 1.83e12 sum and the 2026
paper states 2.1e12"). If the VNS line is reported, it must carry both, or carry one with the
other named — a single unqualified 0.28 would be fake precision on an optional context line.

</planning_findings>

<assumptions>
## Physical Assumptions

- **The symmetric Gaussian IA kernel is adequate at 100 meV.** It is not, at the ~20% level:
  `2W = 5.60`, true fractional width 49.19%, skewness 0.590, excess kurtosis 0.381. | Breaks in
  the bottom bin only; every 100 meV number inherits it.
- **48.98% of the bottom-bin kernel genuinely leaves the retained axis** (plus 0.87% at
  unphysical `T < 0`). | This is physics plus axis truncation, not an error. It must be reported
  and **never renormalized away**.
- **The counting floor and the IA width are statistically independent** when quadratured. |
  Inherited from Phase 11 as an assertion, never validated.
- **The Phase-10 counting floor is a best case with no noise sources**, not a resolution model.
  The project has no resolution parameter. | `fp-poisson-as-resolution` fires if it is quoted
  as one.
- **The response matrix and the trigger curve may be multiplied**, because `P(no counts
  registered) = 2.0e-4` at 0.1 eV and exactly 0 at 0.5/1 eV versus `1 − P_trig` of
  0.998/0.512/0.056. | **Model-specific.** It follows from a *linear* yield assigning 0.018
  quasiparticles to a sensor holding 6.89 µeV against a ~190 µeV gap. A threshold model would
  invert the verdict. This caveat must travel with every sub-eV number.
- **The trigger sharpness `k` is fixed by no project artifact.** | `fp-hardcoded-width` fires if
  a single `k` is reported without its `[1, 12]` sensitivity.

</assumptions>

<limiting_cases>
## Expected Limiting Behaviors

- **T → 0:** `dR/dT` → the analytic flat-box plateau `N_Ge (G_F²/4π) Q_W² M ∫Φ dE` = **2372.368**
  counts/kg/day/keV. Measured 0.93% below it at the axis floor. It must **not rise** (power-law
  flux extrapolation artifact) and must **not fall to zero** (table floor).
- **T > ~0.307 eV:** the sub-100-keV truncation contribution is exactly zero for every isotope,
  so the bound must vanish identically there, not merely become small.
- **Broadening switch OFF:** the chain must reproduce the pre-existing v1.0 path bit-identically.
- **ω̄ → 0:** the broadening kernel must return its input bit-identically (Phase-11 early return).
- **E_rec above ~10 eV:** the extended pipeline must reproduce the frozen v1.0 CEvNS artifacts to
  <1%. Phase 11 measured 0.052% on `dR/dT`; the folded `dR/dE_rec` comparison is new here.
- **P_trig ≡ 1:** must reproduce the un-triggered spectrum bit-for-bit, proving the sigmoid is a
  factor on top of ε rather than a replacement for it.

</limiting_cases>

<anchor_registry>
## Active Anchor Registry

- **`data/flux/reactor_flux_v1.0.csv`** (frozen, 3 GW_th / 25 m, `∫Φ = 7.4958×10¹²`)
  - Why it matters: the primary and only pipeline normalization for CALC-25; also the source of
    the truncation bound's 100 keV floor.
  - Carry forward: planning, execution, verification, writing
  - Required action: use (unmodified) — and **avoid** extending it below 100 keV
- **`CONVENTIONS.md` §D / §I / §J**
  - Why it matters: scenario lock (unchanged), trigger curve and its `k`-sensitivity obligation,
    phonon scale and the `e^(−2W)` prohibition.
  - Carry forward: execution, verification
  - Required action: read, use, cite
- **Frozen v1.0 CEvNS artifacts, `artifacts/stage1/cevns_dRdT.csv` and
  `artifacts/stage1/reconstructed_spectra_{TaAl,AlHf}.csv`**
  - Why it matters: the <1% regression target of VALD-10 above 10 eV.
  - Carry forward: execution, verification
  - Required action: compare
- **Phase-10 extended axis and `artifacts/v2.0/response_matrix_{TaAl,AlHf}_ext.npz`**
  - Why it matters: the 744-bin deposit axis and the regenerated `R(E_rec|E_dep)` this phase
    folds through.
  - Carry forward: execution
  - Required action: use
- **Phase-11 `11-04-SUMMARY.md` and `11-02-IA-WIDTH-DERIVATION.md`**
  - Why it matters: the broadening this phase consumes, its leakage budget, the ×1.163941
    one-sided moment systematic, and the bottom-bin caveats.
  - Carry forward: execution, verification, writing
  - Required action: read, use, cite
- **NUCLEUS Table 5 at 100% duty (CaWO₄ CEvNS 356.5 counts/kg/day/keV)**, EPJC 86, 29 (2026),
  arXiv:2509.03559
  - Why it matters: the signal-side closure anchor. Retained through the re-scope because it
    validates the flux × cross-section × target chain, not the environment.
  - Carry forward: writing
  - Required action: cite — and **avoid** the §2 prose 280 (`fp-nucleus-prose-280`)
- **NUCLEUS EPJC 79, 1018 (2019), arXiv:1905.10258, Fig. 1 Ge curve**
  - Why it matters: reproduced to 5% by the VALD-02 anchor; the VNS siting context.
  - Carry forward: writing
  - Required action: cite

</anchor_registry>

<skeptical_review>
## Skeptical Review

- **Weakest anchor:** the **100 meV bin**. 48.98% of its kernel falls below the grid floor, 0.87%
  lands at unphysical `T < 0`, the shipped kernel is symmetric against a lineshape with skewness
  0.590, and `2W` is only 5.60. Phase 11 stated it plainly: *do not quote the 100 meV bin to
  better than one significant figure.* Every headline sub-eV number in this phase is a statement
  about roughly half a kernel.
- **Second weakest:** the trigger sharpness `k`, fixed by no measurement, sitting on a steeply
  varying curve exactly where the IA width and the counting floor both act.
- **Unvalidated assumptions:** that the discretized convolution is accurate in the bottom decade
  where the axis is coarsest relative to the width (the v1.0 regression tests only the high-E
  end); that the counting floor and the IA width are independent; that the response matrix and
  the trigger curve may be multiplied (true for the linear-yield model, invertible under a
  threshold model).
- **Competing explanation:** a clean `<1%` regression above 10 eV is *also* what a kernel that is
  too narrow everywhere would produce. Phase 11 mitigated this with a pinned `−0.94` trend and
  non-zero bottom-decade leakage; neither is a direct measurement of the width.
- **Disconfirming checks planned (failure of any is informative):**
  1. **Flat-continuation conservatism (F4).** If Φ rises as E falls through the table floor, the
     ≤0.81% figure is not an upper bound and CALC-17 must be restated. Measured from the frozen
     table's own local slope — not an algebraic identity of the bound.
  2. **Plateau failure modes.** `dR/dT` rising toward low T ⇒ extrapolation artifact; falling to
     zero ⇒ table floor reached silently. Asserted, not eyeballed.
  3. **Isotope-resolved zero-point (F2).** If the bound is not identically zero above ~0.307 eV,
     an isotope's kinematic threshold is misplaced.
  4. **`P_trig ≡ 1` bit-identity.** If the un-triggered spectrum is not reproduced bit-for-bit,
     the sigmoid has replaced ε rather than multiplying it.
  5. **`k`-sensitivity over `[1, 12]`.** If the sub-eV trigger-weighted rate moves by more than
     the IA width and counting floor combined, the reported observable is dominated by an
     unmeasured device parameter and must be labelled that way.
- **False progress to reject:**
  - A smooth-looking spectrum down to 100 meV whose bottom bin was produced by renormalizing the
    49% leakage back onto the axis.
  - Narrowing the plateau window until "flat to a few percent" becomes true, instead of reporting
    F1 as a supersession.
  - Extending the reactor flux table below 100 keV to make the truncation bound vanish.
  - Reporting the VNS line as a second spectrum rather than a labelled multiplication.
  - Quoting 407.7 dru or 2.31 as if this repository could reproduce them on demand (F7).

</skeptical_review>

<forbidden_proxies>
## Forbidden Proxies Binding On This Phase

From the ROADMAP Phase 12 section, the milestone-wide list, and `state.json`
`project_contract.forbidden_proxies`:

- **`fp-second-vns-run`** — building a second pipeline run, a second flux table, or a second
  spectral shape for the VNS line. It is a multiplication applied to the finished primary result
  or it is not reported. Quoting a VNS-rescaled number without its rescale label is the same
  failure.
- **`fp-inherited-shielding`** — any NUCLEUS attenuation, post-shield fluence, overburden, or
  veto credit entering under any name.
- **`fp-nucleus-prose-280`** — anchoring on the §2 prose CEvNS value instead of Table 5 at 100%
  duty. Still live, because the Table-5 anchor is still in use. Flatters S/B by ~27%.
- **`fp-gwe-gwth`** — GW_e vs GW_th is a ~×3 trap.
- **Extending the reactor flux table below 100 keV.** Report the bound instead.
- **The naive compound N²/A ratio 1.95** as the Ge/CaWO₄ benchmark. The same-pipeline fold gives
  2.31; CaWO₄ compound N²/A is 44.2, not 65.8 (which is pure W).
- **Repeating the signal-side closure test in place of the background-side one.** VALD-11 no
  longer exists, so there is no background-side closure test at all — that is a real loss and is
  carried into Phase 16 SC1, not papered over here.
- **`fp-poisson-as-resolution`** — quoting the emergent counting floor as a resolution model.
- **Never multiply the rate by `e^(−2W)`.**
- **Never describe the shield-absent configuration as "conservative."**

</forbidden_proxies>

<deferred>
## Deferred Ideas

- Carrying the muon and Compton channels onto the extended grid — **Phase 15** (P-EM). Phase 12
  touches only the CEvNS path.
- Whether the IA broadening applies to electron-recoil channels at all — **Phase 15**, by
  explicit project-contract assignment. Phase 12 must not wire it in either direction, and must
  not assert an answer.
- The neutron and thermal-capture channels — **Phases 13 and 14**.
- `S/B_particle` assembly, the LEE overlay, and the CONUS+ signal-side gate — **Phase 16**.
- Re-wording `CALC-25` and the `REQUIREMENTS.md` §D-lock citation. Flagged for the orchestrator;
  **no plan in this phase edits `REQUIREMENTS.md` or `CONVENTIONS.md`.**
- Recomputing the CaWO₄ closure fold to give 407.7 a reproducible artifact (F7). Out of scope by
  the roadmap's "cited, not re-run" instruction and by the lowered accuracy expectation; recorded
  as a named provenance gap instead.

</deferred>

---

_Phase: 12-reactor-cevns-down-to-100-mev-at-the-paper-s-surface-scenario-p-sig_
_Context recorded: 2026-07-22 (no discussion session; standing directive)_
