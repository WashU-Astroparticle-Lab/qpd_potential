# 16-03 — The LEE Overlay Band, SC4's Adjudication, and the Phase-16 Closeout

**Plan:** 16-03 · **Phase:** 16 (terminal, milestone v2.0) · **Axis:** RECONSTRUCTED
**Artifacts:** `artifacts/v2.0/lee_overlay_band.csv`, `lee_crossover_amplitudes.csv`, `sb_particle_with_lee.pdf`
**Module:** `src/qpd_potential/lee_overlay.py` · **Tests:** `tests/test_lee_overlay.py`

---

## 1. ROADMAP Phase 16 SC4, evaluated **as literally written**

The criterion, quoted verbatim:

> **"the LEE amplitude at which S/B_particle = 1"**

It was evaluated **as written, first**, against the committed plan-16-02 assembly,
before any replacement quantity was computed. Both determinations were **computed**,
not asserted.

**Determination 1 — does `S/B_particle` depend on the LEE amplitude `A` at all?**
**No.** Demonstrated by **contrast**, not by repetition: the differently-named
`S/B_total` moves from **1.332628e-02** at A = 1e-06 dru to **6.866716e-06** at
A = 1e+06 dru — a factor 1.9407e+03 — while over the same range `S/B_particle` is
**1.332628e-02 at both**, because `sb_assembly.assemble()` takes no LEE amplitude and
its summed channel set (`compton_gamma`, `ge71_ec_M_line`, `muon_ionization`,
`neutron_elastic`, `prompt_ngamma_capture`) contains no LEE term. The `_particle`
subscript *defines* the LEE out of that denominator (ROADMAP SC3), so
**∂(S/B_particle)/∂A = 0 exactly.**

**Determination 2 — can `S/B_particle` reach 1 for any non-negative `A`?**
**No.** The supremum over the emitted layers is **1.332628e-02**, a factor **75.04
below 1** before any LEE is added. And under the charitable reading `S/B_total = 1`,
the required LEE band integral is `S − B_particle = 72.9214 − 5472.0006 =
−5399.0791` counts kg⁻¹ day⁻¹ — **negative** — so **no `A ≥ 0` satisfies it**, and
adding background can only lower the ratio further.

> ### **SC4 verdict: SUPERSEDED BY MEASUREMENT.**
> The criterion has no solution, for two independent measured reasons.

A finding that the criterion **is** solvable would have been an equally acceptable
outcome and would have refuted the planning note in `16-CONTEXT.md`. It came out
unsolvable, and both determinations are recorded with their numbers either way.

**Why the wording came to be.** The criterion was written when the milestone expected a
ratio near unity at the *shielded* VNS, where "S/B = 1" and "the LEE erases the signal"
nearly coincided. The 2026-07-22 re-scope withdrew that expectation and carried the
wording forward unchanged.

**FLAGGED FOR THE ORCHESTRATOR:** SC4's wording in `GPD/ROADMAP.md` and
`GPD/REQUIREMENTS.md` describes a quantity that does not exist under this milestone's
own definitions. **Neither file was edited here.**

---

## 2. The replacements, each under its **own** explicit name

`fp-sc4-silent-substitution` forbids shipping a replacement under the criterion's name.
SC4's phrasing appears on **exactly one** row of
`artifacts/v2.0/lee_crossover_amplitudes.csv` — the as-written evaluation — and nowhere
else. The two well-defined quantities are:

- **`lee_equals_B_particle`** — the **LEE-dominance crossover**: the amplitude at which
  the band-integrated LEE equals `B_particle`, i.e. the point beyond which the LEE
  rather than particles sets the denominator.
- **`lee_equals_S`** — the **signal-erasure level**: the amplitude at which the
  band-integrated LEE equals the signal `S`. **This is the formulation
  `GPD/literature/PITFALLS.md` Pitfall 7 actually specifies**, and it is **not** the
  same quantity as SC4's wording.

All amplitudes are in **dru at E₀ = 1 keV**, and every one is marked
`UNMEASURED_FOR_THIS_DETECTOR`.

### RoI 10–100 eV, Ta→Al (Al→Hf is within 1 %)

| quantity | layer | α = 1.000 | α = 1.4307 | α = 1.8614 |
|---|---|---|---|---|
| `lee_equals_B_particle` | estimates_only | 2376.5 | **515.5** | 103.5 |
| `lee_equals_B_particle` | estimates_plus_bounds | 4344.1 | **942.4** | 189.2 |
| `lee_equals_S` | — | 31.67 | **6.870** | 1.379 |

### Sub-eV band, `E_rec` ≤ 1 eV, Ta→Al

| quantity | layer | α = 1.000 | α = 1.4307 | α = 1.8614 |
|---|---|---|---|---|
| `lee_equals_B_particle` | estimates_only | 412.9 | **3.373** | 0.01672 |
| `lee_equals_B_particle` | estimates_plus_bounds | 1049.8 | **8.576** | 0.04252 |
| `lee_equals_S` | — | 0.4316 | **0.003526** | 1.748e-05 |

**The sub-eV crossovers are the least meaningful numbers in this plan and are labelled
as such.** The band integral runs down to the reconstructed-axis floor, **5.301 decades**
below the lowest germanium LEE measurement, and for α > 1 the integral is dominated by
exactly that unmeasured bottom. That is why they swing by four orders of magnitude
across the declared α range while the RoI crossovers swing by only ~23×. On the sub-eV
rows the `CONVENTIONS.md` §I caveat also applies: below the `E_rec` image of a 1 eV
deposit the reported observable is a **trigger probability, not dR/dE_rec**.

---

## 3. Where the extrapolations sit — the finding

Placing the two device-scaling extrapolations and the EDELWEISS RED20 above-ground
germanium anchor against the RoI crossovers, as ratios (central α):

| crossover | RED20 anchor / A | Chang volume / A | Romani area / A |
|---|---|---|---|
| `lee_equals_B_particle`, estimates_plus_bounds | **10.6×** | 10.6× | **21.7×** |
| `lee_equals_B_particle`, estimates_only | 19.4× | 19.4× | 39.6× |
| `lee_equals_S` | **1456×** | 1456× | **2972×** |

**On every one of these extrapolations the LEE would dominate both the particle
background and the signal, by one to three orders of magnitude.** That is the honest
reading — and it is emphatically **not a prediction**. See §4.

---

## 4. The band, and what it is and is not

`dR/dE_LEE = A (E/E₀)^(−α)`, with **E₀ = 1 keV declared once** and stated on every
artifact row and on the figure.

**α is DERIVED, never quoted.** From the two EDELWEISS RED20 **above-ground** germanium
anchors — 1e5 dru at 200 eV and 1e4 dru at 1 keV (the survey's ÷3 underground values are
*not* the relevant ones for a surface wafer):

```
alpha = ln(A1/A2) / ln(E2/E1) = ln(10) / ln(5) = 1.430677
```

α is carried as a **range**, not a point: **[1.0000, 1.8614]**, from a declared factor-2
bracket on the anchor *ratio*, because the anchors are quoted to one significant figure.
**DECLARED, not sourced.**

**Both contradictory device scalings are carried as named band edges, and neither is
ever emitted without the other:**

| edge | scaling | extrapolation factor, written out | dru factor | A(E₀) |
|---|---|---|---|---|
| `romani_al_film_area` | AREA (Al-film dislocation relaxation) | surface-to-mass 1950 cm²/kg (wafer) / 955 cm²/kg (6.8 g CaWO₄ crystal) = 2.0419, **before** counting the ~10,300 films | 2.0419 | 2.042e+04 dru |
| `chang_bulk_volume` | VOLUME (bulk-substrate bursts, ε = 0.68 ± 0.38 meV) | mass 0.93 g → 110 g = ×118.28 | **1.000** | 1.000e+04 dru |

### 4.1 A finding that cuts against the survey's own framing

**dru is already mass-normalized** (counts kg⁻¹ day⁻¹ keV⁻¹). A model in which the LEE
scales with **volume** therefore predicts a rate *per unit mass* that is **invariant**
under the mass extrapolation — so **Chang's ×118.28 factor cancels in dru** and that band
edge is exactly **1.000**. The "×120" the literature survey quotes is a **total-rate**
extrapolation, **not an amplitude factor**, and treating it as one would have inflated
this band by two orders of magnitude.

**Consequence, reported rather than repaired:** the disagreement between the two models
is only a factor **~2 in dru** — far narrower than the survey's framing suggests. The
real width of this overlay comes from the α extrapolation across more than three decades
and from the factor-2 uncertainty on the anchors themselves, not from the device-scaling
disagreement.

### 4.2 Do the two scalings bracket the RED20 anchor?

**No — they do not strictly bracket it.** The volume-scaling edge **coincides exactly**
with the anchor, by construction, because volume scaling leaves a mass-normalized rate
unchanged. The band therefore *contains* the anchor but does not *strictly bracket* it.
**Recorded, not quietly widened.**

### 4.3 The extrapolation span

The lowest germanium LEE amplitude measurement available anywhere is at **200 eV**.

- **3.301 decades** below it to the 100 meV grid floor, where the figure starts.
- **5.301 decades** below it to the reconstructed-axis floor, where the sub-eV band
  integral ends.

No LEE measurement exists below ~10 eV in germanium, or at 100 meV in **any** material;
the lowest genuine LEE dataset anywhere is CRESST-III from 29.6 eV, on **CaWO₄** — a
different target.

### 4.4 What is not claimed

**The LEE is UNMEASURED for this detector, and no amplitude here is a prediction, in
either direction.** Every emitted row carries `UNMEASURED_FOR_THIS_DETECTOR`.

This report does **not** claim the QPD architecture is free of the LEE — there is no
evidence either way — and it does not imply the unified phonon scale escapes it. Worse:
**the LEE mechanism and the QPD signal mechanism are the same phenomenon —
quasiparticle poisoning.** Chang et al. identify bulk-substrate phonon bursts at
ε = 0.68 ± 0.38 meV as a significant source of quasiparticle poisoning in
superconducting qubits, and a QPD's *signal* **is** quasiparticle poisoning. The LEE is
therefore a **direct competitor to the readout mechanism**, not merely a background, and
it is **not shieldable** — it is a property of the wafer and its ~10,300 Al films, and
the surface deployment does not change that.

### 4.5 The LEE is never folded and never summed

- **Never folded** through `R(E_rec|E_dep)`: the anchors are quoted in *measured*
  (reconstructed) energy, so a detector response is already inside them. Folding would
  apply one twice and would move amplitude across the sub-eV regime boundary where the
  reported observable itself changes. Proven by **AST parse** of the module — `response`,
  `response_matrix`, `fold` and `trigger` are neither imported, referenced nor called on
  this path, and the scan is shown non-vacuous by asserting the LEE evaluation exists and
  is called.
- **Never summed** into any headline: `artifacts/v2.0/sb_particle.csv` is asserted
  **byte-identical** to its committed state, so `S/B_particle` was overlaid upon and not
  modified. The only LEE-inclusive ratio in the code carries a **different name**
  (`sb_total_with_lee`), and it exists solely so SC4 could be evaluated as written.

---

## 5. The terminal figure

`artifacts/v2.0/sb_particle_with_lee.pdf`. All particle channels plus the CEvNS signal
on the shared reconstructed axis from 100 meV, with the LEE as a **shaded band** between
its two named edges (never a single curve), the RoI shaded, and each design's sub-eV
regime boundary drawn and labelled as the **`E_rec` IMAGE of a 1 eV DEPOSIT**
(0.497240 / 0.495855 eV) rather than as a literal 1 eV line.

Written with `pdf.compression = 0` so the audit reads the annotation **out of the
file's own text stream**, with matplotlib's TJ kerning arrays rejoined — a naive byte
search either passes vacuously or fails spuriously. Read back and asserted present:
the annotation **"particle backgrounds only; LEE not modelled in the headline"**,
`order_of_magnitude`, both band-edge names, `RECONSTRUCTED`,
`UNMEASURED_FOR_THIS_DETECTOR`, and the extrapolation span in decades.

The two channels that enter `S/B_particle` as **bounds** are annotated on the figure:
the prompt (n,γ) capture bound is a total reaction rate, not a spectrum, so it is not
drawn as a curve.

---

## 6. The four ROADMAP Phase 16 success criteria

| criterion | verdict | evidence |
|---|---|---|
| **SC1** — VALD-12 restated to its signal-side leg, with the restatement's cost written on the deliverable | **PARTIALLY CONFIRMED** *(window-conditional)* | `16-01-CONUS-SIGNAL-SIDE.md`; `artifacts/v2.0/conus_signal_side_check.csv`; `artifacts/v2.0/conus_window_sensitivity.csv` |
| **SC2** — CALC-22: `S/B_particle` assembled, both designs, one baseline, veto credit 1.0 by construction, named `S/B_particle`, never the forbidden adjective | **CONFIRMED** | `16-02-SB-ASSEMBLY.md`; `artifacts/v2.0/sb_particle.csv`; `artifacts/v2.0/channel_inventory.csv` |
| **SC3** — CALC-21: the LEE as an `(A, α)` overlay band on the `E_rec` axis, both contradictory scalings, never folded, never summed | **CONFIRMED** | `artifacts/v2.0/lee_overlay_band.csv`; `artifacts/v2.0/sb_particle_with_lee.pdf`; §4 above |
| **SC4** — "the LEE amplitude at which `S/B_particle` = 1", plus the band discipline | **SUPERSEDED BY MEASUREMENT** | `artifacts/v2.0/lee_crossover_amplitudes.csv`; §1 above |

**SC1 is graded PARTIALLY CONFIRMED because the measurement says so**, not to reconcile
it: the pre-registered 0.4–1 keV_ee window gives a ratio of 5.278664e-04 against a
pre-declared factor of 2.0 — **a FAIL by 3.28 decades** — and only the declared 160 eV_ee
alternate lands inside the factor.

**SC4's band-discipline half is separately CONFIRMED:** the assembled band is
`order_of_magnitude`, one full decade wide, and a test fails if any narrower band is
emitted. The per-figure annotation requirement is discharged and machine-verified.

**No window was narrowed, no threshold was lowered and no band was tightened to make any
criterion true.** The window was pre-registered in source before any integral ran; the
pass/fail factor was declared before any ratio existed; the accuracy band was widened, not
narrowed, by the propagation rule; and the SC4 verdict is a supersession rather than a
reinterpretation.

---

## 7. The caveat table, carried onto the terminal deliverable

Carried from plan 16-02, unchanged, because these attach to the headline number and
must not be left behind in an intermediate report.

1. **The neutron resonance imprint WASHES OUT on the reconstructed axis** — the
   resolving statistic falls to **3.383 / 3.598** against Phase 13's **own** pre-declared
   threshold of **5.0**, a 9.5× / 8.9× washout from the 12.202 %-per-bin reconstructed
   binning acting on a 1.87 %-wide feature. **Anyone quoting germanium's resonance
   structure as a discriminating handle in reconstructed energy would be over-reading
   it.** The 33–35 % amplitude contrast survives; the resolving statistic does not.
2. **The Landau–Vavilov validity floor is 4111.82 eV**, above the 10.14 eV v1.0 grid
   floor, and it **indicts 209 of the 584 bins the v1.0 manuscript published — 35.79 %**.
   Varying `I` over 300–400 eV gives 204–213: no plausible value makes it zero. This is a
   fact about the **published v1.0 paper**, not only about this milestone.
3. **The 100 meV bin is the least reliable number in the milestone** (`CONVENTIONS.md`
   §J). Kernel leakage below the floor, with its axis attached: **48.98 %** on the
   Phase-11 480-bin axis, **49.728 %** on the Phase-13 744-bin axis — the difference is
   binning, not physics — plus **0.892 %** landing at unphysical `T < 0` and a lineshape
   **skewness of 0.590** against a symmetric Gaussian. Nothing was renormalized.
4. **The muon channel's signed bias label is anchor-leg dependent.** **-20.61 %** against
   **PDG Leg A** (~1 muon cm⁻² min⁻¹ × A_top = 1.7204 Hz); **BRACKETING DISCLOSURE: PDG
   Leg B** (I_v ~ 70 m⁻² s⁻¹ sr⁻¹ with cos²θ → 1.1350 Hz) gives **+20.34 %** on the same
   adopted 1.3659 Hz. The legs **bracket** it from opposite sides: **the ~20 % magnitude
   is solid, the SIGN is not**, and it must never travel without its Leg A citation and
   the Leg B bracketing.
5. **Phase 13's Ge-vs-CaWO₄ reversal is conditional** on a common-`constant-sigma`
   substitution; this repository owns a resonance-resolved `σ_el` for **germanium only**.
6. **There is no external validation of the ratio.** Carried from plan 16-01:
   `S/B_particle` has external validation of its **NUMERATOR** only — and that check is
   window-conditional and **fails on the window this project pre-registered**. Since
   VALD-11's deletion there is **no background-side target-swap validation at all**, and
   the one signal-side closure (407.7 dru CaWO₄) has no reproducible artifact.

**NUCLEUS's CaWO₄ S/B ≈ 1.2 and Al₂O₃ ≈ 0.13, and CONUS+'s ≈ 0.03, are context for
SHIELDED experiments and are explicitly not as targets** an unshielded surface wafer
should approach. The milestone carries **no replacement expectation** at all.

---

## 8. Milestone v2.0 hand-off

**What SENS-01 and MANU-01 receive:**

- `S/B_particle` = **1.33 × 10⁻² / 7.29 × 10⁻³** (Ta→Al) and **1.32 × 10⁻² / 7.27 × 10⁻³**
  (Al→Hf) in the 10–100 eV RoI, at `order_of_magnitude`, veto credit 1.0 by construction,
  NUCLEUS's-shielding-absent, with the two denominator layers and the six-row caveat
  table attached.
- The complete channel inventory with its reproduction residuals, its written
  double-count resolutions, and its **non-empty named omission list**.
- The LEE overlay band with both device scalings, and the two crossover amplitudes under
  their own names.
- The terminal figure with its machine-verified annotation.
- **Two findings that bear on the published v1.0 manuscript rather than on this
  milestone:** the Landau–Vavilov floor indicting 209 of 584 bins, and the resonance
  imprint washout on the reconstructed axis.

**Open items flagged for the orchestrator — none of these files was edited:**

1. **SC4's wording** in `GPD/ROADMAP.md` and `GPD/REQUIREMENTS.md` describes a quantity
   that does not exist under this milestone's own definitions (§1).
2. **The CONUS+ analysis window** is a live internal discrepancy: `ROADMAP.md` and
   `REQUIREMENTS.md` say 0.4–1 keV_ee, `GPD/literature/SUMMARY.md` says 160 eV_ee, and
   they give opposite VALD-12 verdicts.
3. **Stale `REQUIREMENTS.md` texts:** CALC-11, CALC-18, CALC-19, CALC-20, CALC-23 and
   CALC-25, plus the citation of a `CONVENTIONS.md` §D VNS lock that never happened.
   Flagged by Phases 13, 14, 15 and again here.
4. **VALD-10's `<1 %` gate** and its status as a same-matrix comparison — a
   milestone-level decision Phase 12 deferred.
5. **The ROADMAP Phase 13–16 plan checkboxes** are unticked.
6. **No germanium ionization-quenching model is frozen** in this repository, and
   VALD-12's verdict depends on one.
7. **The 407.7 dru CaWO₄ closure** still has no reproducible artifact.
8. **A pre-existing suite failure** predating this phase's execution:
   `tests/test_legacy_grid_disposition.py::test_retraction_no_live_statement_of_the_display_rule`
   is tripped by `16-02-PLAN.md`'s own line 346 wording. The baseline in this worktree is
   **819 passed / 1 failed**, not the 820/0 the plans quote. This executor did not edit a
   contract document to silence it.

---

## 9. Checkpoint (Task 3), recorded in full

Standing session directive: run the roadmap without per-phase discussion unless a genuine
blocker arises. The checkpoint's content is recorded here **in full** and the default was
taken. **No approval was given and none is fabricated** — the precedent of 12-03 §6,
13-03 and 14-02 §8.

> **Milestone v2.0 terminal result.** `S/B_particle` = **1.33 × 10⁻²** (estimates-only) /
> **7.29 × 10⁻³** (estimates-plus-bounds, a lower bound), RoI 10–100 eV, Ta→Al;
> 1.32 × 10⁻² / 7.27 × 10⁻³ for Al→Hf. At `order_of_magnitude`, veto credit **1.0 by
> construction**, NUCLEUS's-shielding-absent.
> **VALD-12 signal-side: PARTIALLY CONFIRMED, window-conditional — the pre-registered
> 0.4–1 keV_ee leg FAILS at ratio 5.278664e-04 against a pre-declared factor 2.0.**
> **SC4 as written: SUPERSEDED BY MEASUREMENT**, with `lee_equals_B_particle` = 942.4 dru
> (estimates-plus-bounds, RoI, central α) and `lee_equals_S` = 6.870 dru instead — against
> extrapolated LEE amplitudes of 1.00e+04 to 2.04e+04 dru at E₀ = 1 keV, i.e. 10.6× to
> 21.7× above LEE-dominance and 1456× to 2972× above signal erasure.
> The three things most worth a physicist's own judgement, in order:
> **(1)** the **SC4 adjudication** — is the criterion genuinely ill-posed at this
> `S/B_particle`, and is the replacement pair the right pair? **(2)** whether the two
> device scalings **bracket** anything real for this wafer, given that they span only ~2×
> in dru once the volume model's mass factor is seen to cancel, against a 3.3–5.3 decade
> extrapolation. **(3)** the two findings that bear on the **published v1.0 manuscript**
> rather than on this milestone — the Landau–Vavilov floor indicting 209 of 584 bins, and
> the resonance-imprint washout on the reconstructed axis.
> Accept the Phase-16 closeout and close milestone v2.0? **[Y/n/e]** (Enter = Y)
