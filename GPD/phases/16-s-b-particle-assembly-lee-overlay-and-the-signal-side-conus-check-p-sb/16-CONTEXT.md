# Phase 16: S/B_particle Assembly, LEE Overlay, and the Signal-Side CONUS+ Check (P-SB) — Context

**Gathered:** 2026-07-23
**Status:** Ready for planning
**Terminal phase of milestone v2.0.**

## Provenance of this file

**No `/gpd:discuss-phase` session was run for this phase and no user decisions were
elicited while writing it.** The user issued a standing session directive to run the
roadmap to completion without per-phase discussion unless a genuine blocker arises;
this file follows the precedent set by `08-CONTEXT.md`, which records the same thing.

Everything below is transcribed from artifacts that already existed before this
planning session began: `GPD/ROADMAP.md` (the 2026-07-22 re-scope banner and the
Phase 16 section), `GPD/REQUIREMENTS.md`, `GPD/CONVENTIONS.md`, `GPD/state.json`
`project_contract`, and the four input phase summaries (12-03, 13-03, 14-02, 15-04).
**No user decision is invented here.** Where this file records a judgement made during
planning rather than transcribed from an artifact, it says so explicitly and marks it
as a planning observation to be verified in execution, not as a settled result.

<domain>
## Phase Boundary

Terminal assembly. Three things, in this order:

1. **Check the signal chain** against CONUS+'s SM CEvNS expectation (VALD-12 as
   restated 2026-07-22 to its signal-side leg), and **write the cost of the
   restatement onto the deliverable**.
2. **Assemble `S/B_particle`** in the 10–100 eV reconstructed RoI and below, both
   designs, trigger applied, at a veto credit of **exactly 1.0 by construction**,
   from the channels Phases 12–15 produced — with every input's accuracy label
   surviving into the assembled band.
3. **Carry the LEE as an explicit overlay band** on the `E_rec` axis, never folded
   through `R(E_rec|E_dep)` and never summed into the headline, and report the
   decisive falsifiable LEE amplitude.

Requirements: **CALC-21**, **CALC-22**, **VALD-12** *(restated — ROADMAP Phase 16 SC1)*.

Nothing is re-computed upstream. Every channel arrives as a committed artifact on the
shared 161-bin reconstructed axis. This phase integrates, audits, combines, labels,
and adjudicates.

</domain>

<contract_coverage>
## Contract Coverage

**Decisive outputs**

- **VALD-12 signal-side factor.** Rescaling the pipeline to CONUS+'s 3.6 GW_th /
  20.7 m and their 0.4–1 keV_ee window reproduces their SM-expected CEvNS rate
  (**347 ± 59 events in 327 kg·d**) within a **stated** factor.
- **The restatement's cost, written on the deliverable.** Reproducing CONUS+'s *S/B*
  is not a coherent test for this pipeline — they sit at 7.4 m.w.e. behind a shield
  this project does not model, so matching their ratio would require inventing a model
  of their shield. **Consequence: the milestone carries no external validation of the
  ratio `S/B_particle` itself, only of its numerator.** That sentence, or its
  equivalent, must appear on the headline deliverable.
- **`S/B_particle`**, both designs, in the 10–100 eV RoI and in a sub-eV band defined
  once and applied identically to every channel.
- **The channel inventory**, complete and non-double-counted, with the channels that
  are *not* in it enumerated by name and bias direction.
- **The LEE `(A, α)` overlay band** spanning both contradictory scalings, and the
  decisive falsifiable LEE amplitude (see the Skeptical Review — the criterion as
  literally written appears to be ill-posed at this S/B and must be adjudicated, not
  silently substituted).

**Acceptance signals**

- Every channel's headline number is **re-integrated from its committed artifact and
  reproduced** before it enters the sum. Phase 14 established this pattern: the band
  integrator is validated by reproducing CEvNS 118.73 and neutron 5430.287 / 5485.152
  before being used.
- Every comparison operand carries an asserted **axis tag**. Phase 13 caught itself
  making a cross-axis error once already.
- The assembled band is **never tighter than its loosest input label** — the neutron
  and capture channels are `order_of_magnitude` and dominate the denominator.
- A **text check** confirms the word "conservative" attaches nowhere to this
  configuration, and that the observable is named `S/B_particle` everywhere, never
  bare "S/B".

**False progress to reject**

- Summing the **inelastic bound** (≤ 2666.83 counts kg⁻¹ day⁻¹) as though it were a
  rate estimate. Its nuclear recoils sit ~3 decades above the RoI; it is loose by ~3
  decades there and would corrupt the denominator.
- Folding the **thermal capture component alone** instead of the full capture band.
  23.51 % of that channel (1034.24 counts kg⁻¹ day⁻¹ — itself ~8.7× the whole CEvNS
  total) is non-thermal; taking the Phase-14 title literally understates the channel
  by 1.31×.
- Substituting the CEvNS **total** 118.73 for the **in-RoI** signal. 118.73 is a
  total over the whole reconstructed axis; the in-RoI numerator must be computed.
- Quoting the ⁷¹Ge M-line bound **without its scenario**. 130.82 at saturation versus
  7.70 at t = 1 d is a 17× spread that a bare number hides.
- Any veto credit other than exactly 1.0; any "reduced", "partial", or "for-reference"
  credit; describing the shield-absent configuration as "conservative".
- Reporting `S/B_particle` without the LEE band (`fp-lee-omission`), or folding the
  LEE through the response matrix.
- Assembling without the neutron channel or its bound (`fp-silent-neutron-omission`).

</contract_coverage>

<user_guidance>
## User Guidance To Preserve

These are standing directives already recorded in project artifacts, restated here
because they bind this phase. **None was newly elicited.**

- **"Just take the approximation as was done in the paper. I don't need a very
  accurate result."** (user, 2026-07-22). Bounded estimates and closed-form folds.
  The lowered accuracy expectation is load-bearing here: it is *why* the neutron and
  capture channels are `order_of_magnitude`, and that label propagates into this
  phase's band and forbids a tighter headline.
- **Spectra extend to 100 meV; the earlier 10 eV display floor is RETRACTED**
  (user, 2026-07-22).
- **No reduced veto credit is assumed and no resized veto is invented**
  (explicit user decision, 2026-07-22, ROADMAP Phase 8 lock).
- **Standing session directive:** run the roadmap without per-phase discussion unless
  a genuine blocker arises. Checkpoint tasks are therefore *recorded in full with the
  default taken*, and no approval is ever fabricated — the precedent set by 12-03 §6,
  13-03, and 14-02 §8.

**Must-have references / prior outputs**

- `artifacts/v2.0/cevns_dRdErec_ext_{TaAl,AlHf}.csv` — signal, Phase 12
- `artifacts/v2.0/neutron_dRdErec_ext_{TaAl,AlHf}.csv` — neutron elastic, Phase 13
- `artifacts/v2.0/ge71_ec_dRdErec_{TaAl,AlHf}.csv`, `ge71_ec_lines.csv`,
  `capture_recoil_bounds.csv`, `capture_rate_bands.csv` — capture channels, Phase 14
- `artifacts/v2.0/em_dRdErec_ext_{TaAl,AlHf}.csv`, `em_accuracy_labels.csv`,
  `em_validity_floors.csv`, `em_inband_dominance.csv` — muon and Compton, Phase 15
- `CONUS+ Collab., Nature 643, 1229 (2025), arXiv:2501.05206` — SM expectation
  347 ± 59 in 327 kg·d at 3.6 GW_th / 20.7 m, 0.4–1 keV_ee
- `GPD/literature/SUMMARY.md` — the LEE anchor set (Romani JAP 136, 124502; Chang
  APL 127, 263502; NUCLEUS arXiv:2603.07687 k = 0.59 ± 0.06; EDELWEISS RED20
  10⁵ / 10⁴ dru at 200 eV / 1 keV **above ground**)

**Stop / rethink conditions** (ROADMAP Phase 16 backtracking triggers, verbatim in force)

- If the restated VALD-12 signal-side check cannot reproduce CONUS+'s SM CEvNS
  expectation within its stated factor, **treat the failure as evidence about our own
  flux × cross-section × target chain, not about CONUS+, and claim no headline until
  it is understood.**
- If the assembled band comes out **tighter than the loosest input label**, the labels
  have been dropped somewhere in the propagation — re-propagate before reporting.
- If any deliverable describes the shield-absent configuration as **"conservative"**,
  stop and correct it.

</user_guidance>

<decisions>
## Methodological Decisions (LOCKED — carried from prior artifacts, not newly elicited)

### Configuration and veto credit

1. **There is exactly ONE baseline.** The configuration carries no passive shielding
   and no veto, so the veto credit is **1.0 by construction** — not a reduced credit,
   not an assumed one, not a policy default. `surface_environment.veto_credit()`
   already returns exactly 1.0 with `BY CONSTRUCTION` in its own docstring
   (Phase 15 `test-veto-credit-sentinel`).
2. **It is described as "NUCLEUS's-shielding-absent" and NEVER as "conservative".**
   An L2-off, shield-absent configuration is a *different and worse* configuration
   than NUCLEUS's, not a conservative subset. Phase 8 locked this; Phase 15 already
   runs an attachment-aware text check that finds zero occurrences, and this phase
   inherits that check rather than writing a weaker one.

### Normalization and scenario

3. **Primary scenario is the paper's own: 3 GW_th at 25 m, ∫Φ = 7.5 × 10¹² ν̄/cm²/s,
   surface, unshielded**, from the frozen `data/flux/reactor_flux_v1.0.csv`, matching
   `CONVENTIONS.md` §D unchanged. This is the scenario every input channel was
   produced at.
4. **The NUCLEUS VNS line is a labelled scalar rescale only**, if reported at all:
   **0.280158** (from the NUCLEUS-stated 2.1 × 10¹²) *and* **0.244174** (from the
   project's own geometric reconstruction 1.830269 × 10¹²). The ~15 % gap between them
   is one the project's arithmetic does not close, so **both factors travel or neither
   does**; a bare unqualified 0.28 is forbidden. `fp-second-vns-run` forbids a second
   pipeline run, a second flux table, or a second spectral shape.

### VALD-12, restated

5. **VALD-12 is restated to its SIGNAL-SIDE leg only.** Reproduce CONUS+'s **SM CEvNS
   rate** within a stated factor (~2). Reproducing their **S/B ratio** is *not* a
   coherent gate for this pipeline and is not attempted.
6. **The loss is written onto the deliverable**, not quietly dropped: `S/B_particle`
   has external validation of its **numerator only**, and **no external validation of
   the ratio**. Their measured S/B ≈ 0.03 is retained as *context for the discussion*,
   explicitly not as a gate.

### Reporting discipline

7. **The observable is named `S/B_particle` everywhere**, never bare "S/B".
8. **The assembled band is never quoted tighter than its loosest input label.** The
   neutron channel (Phase 13) and the capture channel (Phase 14) both carry
   `accuracy_label = order_of_magnitude` and both are large fractions of the
   denominator, so a percent-level `S/B_particle` band is forbidden **regardless of
   how the arithmetic comes out** (`fp-precision-inflation`).
9. **No target value is carried.** The pre-re-scope expectation `S/B ≈ 0.65–1.2` is
   **withdrawn** and must not appear in this phase in any form. The ROADMAP explicitly
   asserts **no replacement expectation**: the number is to be computed, and the phase
   must not carry a target value it then reproduces. A poor `S/B_particle` is a valid,
   reportable outcome and is **not to be rescued**.

### LEE

10. **The LEE is carried as `dR/dE_LEE = A(E/E₀)^(−α)`, an overlay band on the `E_rec`
    axis** — never folded through `R(E_rec|E_dep)` (it is measured in reconstructed
    energy), never folded into a headline number, and never claimed as a prediction.
11. **Both contradictory scalings are carried as the band:** Romani Al-film **area**
    scaling (~10,300 films; surface-to-mass ~1950 cm²/kg vs ~955 for a 6.8 g CaWO₄
    crystal) and Chang bulk **volume** scaling (0.93 g → 110 g, a ×120 extrapolation).
    Neither extrapolation is defensible as a prediction, and neither is claimed as one.
12. **"Particle backgrounds only; LEE not modelled in the headline"** is annotated on
    every deliverable figure.

### Agent's Discretion

- Module decomposition, artifact layout, test design, figure composition.
- The exact definition of the sub-eV reporting band — **provided it is defined once
  and applied identically to every channel** (see Assumptions).
- How the two-layer bound structure of `B_particle` is presented, provided rate
  estimates and upper bounds are never silently mixed into one number.
- Whether the VNS scalar rescale line is reported at all in this phase; if it is,
  both factors travel with it.

</decisions>

<assumptions>
## Physical Assumptions

- **Channel additivity.** The seven inventory channels deposit independently and their
  reconstructed-axis rates add. | Justified because they are distinct primary
  interactions with distinct sources. | **Breaks if two entries describe the same
  deposit** — which is exactly what the no-double-count audit exists to test, and it
  must be *checked*, not assumed. The two live candidates: (a) neutron elastic (MT=2)
  vs prompt (n,γ) capture (MT=102) share the *same incident flux* but are different
  reactions; (b) the ⁷¹Ge EC line is the *delayed decay* of the nucleus produced by
  the *prompt* capture whose recoil is already counted — same parent, different events
  separated by ~11.43 d, so not the same deposit. Both must be verified.

- **Every channel is on the SAME reconstructed axis.** The 161-bin `E_rec` axis, less
  the `[0, 10⁻³ eV)` underflow catch-bin, which Phases 12/13/14/15 all drop
  identically. | **Breaks if any operand is a deposit-axis quantity.** The ⁷¹Ge M line
  is the standing trap: 158.7 eV is a **deposited** energy and its reconstructed image
  is at **65.0 / 63.0 eV** (mapping slope 0.4099 / 0.3967), not at 158.7 eV.

- **Band definitions must be re-derived, not inherited.** The inputs quote different
  sub-eV bands: Phase 13 gives the neutron channel at `E_rec < 1 eV`, while Phase 15
  gives muon / Compton / CEvNS at `E_rec < 10 eV`. | **Mixing them would produce a
  ratio whose numerator and denominator are integrated over different regions.** The
  sub-eV band must be defined once here and every channel re-integrated on it.

- **Summing upper bounds into the denominator produces a LOWER bound on
  `S/B_particle`, not an estimate.** Two of the seven channels arrive as bounds
  (prompt capture ≤ 4399.78; ⁷¹Ge M line ≤ 130.82 at saturation), not as rate
  estimates. | A single number that mixes bounds with estimates is neither. |
  **Breaks the interpretation if the two layers are collapsed** — the layers must stay
  separately reported.

- **The trigger curve's sharpness `k` is fixed by no project artifact.**
  `CONVENTIONS.md` §I imposes a standing obligation: every result computed with the
  trigger must be reported with its sensitivity to `k` over `[1, 12]`. That obligation
  reaches the sub-eV `S/B_particle`.

</assumptions>

<limiting_cases>
## Expected Limiting Behaviors

- **`P_trig ≡ 1` must reproduce the untriggered assembly bit-identically.** The trigger
  MULTIPLIES ε ≈ 0.5, it does not replace it (`CONVENTIONS.md` §I). Phases 13, 14 and
  15 each asserted this with `np.array_equal`; the assembly inherits the obligation.
- **Removing any single background channel must strictly increase `S/B_particle`.** A
  leave-one-out sweep that does not is an arithmetic or sign error, not a discovery.
- **Adding the inelastic bound to the denominator must move `S/B_particle` by roughly
  the ~3 decades by which that bound is loose in the RoI.** That measured move is the
  demonstration of *why* it is excluded; excluding it by assertion is weaker.
- **The band integrator must reproduce each channel's own published headline** before
  it is used: CEvNS total 118.73; neutron in-RoI 5430.287 / 5485.152; Compton in-RoI
  34.2484 / 35.8616; muon in-RoI 7.4656 / 7.7231; CEvNS in-RoI 72.9214 / 73.1441.
- **The VNS rescale, if reported, must be exactly proportional** on every bin — a
  bin-to-bin ratio spread at the float round-trip level (Phase 12 measured
  2.2 × 10⁻¹⁶). Any bin dependence means a second fold happened.

</limiting_cases>

<anchor_registry>
## Active Anchor Registry

- **CONUS+ Collab., Nature 643, 1229 (2025), arXiv:2501.05206**
  - Why it matters: the SM CEvNS expectation **347 ± 59 events in 327 kg·d** at
    3.6 GW_th / 20.7 m in 0.4–1 keV_ee — the only measured Ge-at-a-reactor CEvNS
    observation, and the *sole* external check this milestone's numerator gets.
    Their measured S/B ≈ 0.03 is **context only**, no longer a gate.
  - Carry forward: planning, execution, verification, writing
  - Required action: read, compare, cite

- **`artifacts/v2.0/cevns_dRdErec_ext_{TaAl,AlHf}.csv`** (Phase 12)
  - Why it matters: the signal numerator. **118.73 is a TOTAL, not in-RoI.**
  - Carry forward: execution, verification · Required action: read, use

- **`artifacts/v2.0/neutron_dRdErec_ext_{TaAl,AlHf}.csv`** (Phase 13)
  - Why it matters: 5430.29 / 5485.15 counts kg⁻¹ day⁻¹ in-RoI, the largest single
    denominator term, at `accuracy_label = order_of_magnitude`, with a flux term
    demonstrated **UNBOUNDED** (+41.33 % / −16.31 % under perturbations invisible to
    its only cross-check) and a five-row **un-netted** directional-bias table.
  - Carry forward: execution, verification, writing · Required action: read, use, cite

- **`GPD/phases/14-.../14-02-EC-AND-CLOSEOUT.md` §6 hand-off table** (Phase 14)
  - Why it matters: the six numbered capture bounds with their scenarios — prompt
    (n,γ) ≤ 4399.78 in-RoI (of which **1034.24, i.e. 23.51 %, is non-thermal**);
    ⁷¹Ge M line ≤ 130.82 at saturation / ≤ 7.70 at t = 1 d, **100 % in-RoI** at
    E_rec ≈ 65.0 / 63.0 eV; K and L lines outside the RoI; inelastic ≤ 2666.83,
    **very loose**.
  - Carry forward: execution, verification, writing · Required action: read, use, cite

- **`artifacts/v2.0/em_accuracy_labels.csv`** and `em_validity_floors.csv` (Phase 15)
  - Why it matters: the machine-readable label object Phase 16 was told to propagate,
    and the record of which bins may be quoted at all.
  - Carry forward: execution, verification · Required action: read, use

- **`GPD/literature/SUMMARY.md`** — LEE anchor set
  - Why it matters: Romani JAP 136, 124502 (Al-film **area** scaling, meV–eV phonons);
    Chang APL 127, 263502 (bulk **volume** scaling); NUCLEUS arXiv:2603.07687 time law
    `R(t) = A(t−t₀)^(−k)`, `k = 0.59 ± 0.06`; **EDELWEISS RED20 Ge amplitude anchors
    10⁵ / 10⁴ dru at 200 eV / 1 keV above ground** (÷3 underground — the above-ground
    values are the relevant ones for a surface wafer).
  - Carry forward: planning, execution, writing · Required action: read, use, cite

- **`GPD/CONVENTIONS.md` §I** (trigger) and **§J** (phonon scale / Debye–Waller)
  - Why it matters: `P_trig` multiplies ε on the DEPOSIT axis; `E50 = 0.5 eV` exactly;
    `k` unmeasured with a standing `[1, 12]` sensitivity obligation. §J's bottom-bin
    caveats and the standing prohibition on multiplying any rate by `exp(−2W)`.
  - Carry forward: execution, verification · Required action: read, use, avoid

- **NUCLEUS Collab., EPJC 86, 29 (2026), arXiv:2509.03559 — CaWO₄ S/B ≈ 1.2,
  Al₂O₃ ≈ 0.13**
  - Why it matters: **context for a shielded experiment ONLY**, explicitly *not*
    targets an unshielded surface wafer should approach.
  - Carry forward: writing · Required action: cite, avoid *(avoid as a target)*

- **Our 407.7 dru CaWO₄ closure fold (ratio 1.14 to Table 5 at 100 % duty)**
  - Why it matters: the milestone's ONLY signal-side target-swap validation — and it
    has **no reproducible artifact anywhere in this repository**. A word-bounded search
    (`git grep -lE '(^|[^0-9.])407[.]7([^0-9]|$)'`) returns GPD prose alone; a naive
    substring search falsely matches a dozen committed numeric CSVs. It was folded at
    the NUCLEUS/VNS normalization, so it must be **neither re-run nor rescaled**.
  - Carry forward: writing, verification · Required action: cite, avoid *(avoid
    presenting it as reproduced, and avoid rescaling it)*

</anchor_registry>

<skeptical_review>
## Skeptical Review

- **Weakest anchor: the eV–keV differential shape of the sea-level neutron flux.**
  It sets the largest term in the denominator, it has no independent validation, and
  Phase 13 demonstrated **concretely** — by constructing two perturbations that its
  only cross-check cannot see — that the in-RoI rate moves by **+41.33 %** and
  **−16.31 %** with the >10 MeV Gordon integral moving by exactly zero. The flux term
  is **UNBOUNDED**, not merely large. Every headline number of this phase inherits it.

- **Second weakest: the ⁷¹Ge M-line exposure scenario.** 130.82 at saturation versus
  7.70 at t = 1 d is a 17× spread on a channel that lands **100 % inside the RoI**,
  and the project does not own the exposure history.

- **Third: with VALD-11 deleted there is NO background-side target-swap validation at
  all**, and the one signal-side closure (407.7 dru) is an unreproduced prior
  assertion. Phase 12 carried this to Phase 16 SC1 deliberately. It must be *stated*,
  not absorbed.

- **Unvalidated assumptions**
  - That the seven-channel inventory is *complete* for an unshielded surface wafer.
    Muon-induced neutrons and muon-induced secondary gammas at the surface, and
    cosmogenic activation of ⁷¹Ge/⁶⁸Ge/⁶⁵Zn by the fast component (declared out of
    scope by Phase 14), are **not** in the inventory. Completeness must be claimed
    against a **named** omission list with bias directions, never against silence.
  - That the ⁷¹Ge EC line and the prompt (n,γ) recoil bound are not the same energy
    twice.
  - That `accuracy_label` propagation through a *ratio* behaves as the per-channel
    labels imply. A ratio of two labelled quantities is not automatically labelled.

- **Competing explanation.** A poor `S/B_particle` could reflect the physics of an
  unshielded surface wafer — the expected result — **or** an assembly bug: a channel
  double-counted, a bound summed as an estimate, a band mismatch, or a cross-axis
  conflation. These are separated by the leave-one-out sweep, the per-channel
  re-integration against each channel's own published headline, the axis-tag
  assertions, and the inelastic-bound sensitivity measurement.

- **Disconfirming checks (must be run, and their outcome recorded either way)**
  1. **Leave-one-out over the channel inventory.** Removing any background channel
     must strictly increase `S/B_particle`; the size of each move ranks the channels
     and would expose a double count as an implausibly large or small move.
  2. **Per-channel re-integration.** Each channel's committed artifact must reproduce
     its own published headline before it is allowed into the sum. This can fail.
  3. **Inelastic-bound sensitivity.** Measure how far including it moves the answer,
     rather than asserting that it is too loose to include.
  4. **The named omission list must be non-empty.** A completeness audit that returns
     "nothing missing" is either wrong or vacuous for a surface detector.

- **False progress to reject**
  - A tidy `S/B_particle` quoted to three significant figures. The loosest input label
    is `order_of_magnitude`.
  - "Nothing is missing from the inventory."
  - Any rescue of the headline — narrowing a band, dropping a bound, switching the
    M-line scenario, or reaching for the VNS rescale — to make the number look better.

### Planning observation to be verified in execution — NOT a settled result

**ROADMAP Phase 16 SC4's decisive number, "the LEE amplitude at which
`S/B_particle` = 1", appears to be ill-posed under this milestone's own definitions,
in two independent ways, and the phase must adjudicate it rather than silently
substitute something else.**

1. **By definition.** The `_particle` subscript exists precisely because the LEE is
   *excluded* from that denominator (SC3: the LEE is "never folded into a headline
   number"). So `S/B_particle` does not depend on the LEE amplitude `A` at all, and
   no value of `A` sets it to anything.
2. **By magnitude.** Even reading it charitably as `S/B_total = 1`: the in-RoI
   numerator is ≈ 72.9 / 73.1 counts kg⁻¹ day⁻¹ while the neutron channel **alone**
   contributes 5430.29 / 5485.15 to the denominator. `S/B` is already far below 1
   before any LEE is added, and adding background can only lower it further. There is
   no positive `A` that raises it to 1.

The criterion was written when the milestone expected `S/B ≈ 0.65–1.2` at the
shielded VNS, where "S/B = 1" and "the LEE erases the signal" nearly coincided. The
re-scope withdrew that expectation but the SC4 wording was carried forward unchanged.

**What the phase must do:** evaluate the criterion **as literally written first**,
determine whether it has a solution, and if it does not, report that as a
**SUPERSEDED BY MEASUREMENT** verdict in the established Phase-12/13/14 vocabulary,
with the numbers behind it — then compute the well-defined replacements under their
own explicit names, never under SC4's name:
- the LEE amplitude at which **LEE = B_particle** (the LEE-dominance crossover), and
- the LEE amplitude at which **LEE = S** (the signal-erasure level, which is the
  formulation `GPD/literature/PITFALLS.md` Pitfall 7 actually specifies), and
- where the Romani-area and Chang-volume extrapolations, and the EDELWEISS RED20
  above-ground anchors, sit relative to both.

This is recorded as a **planning observation**, flagged for verification. If execution
finds the criterion *is* satisfiable, that finding supersedes this note and the note
was wrong — which is the outcome the check exists to allow.

### Second planning observation — the VALD-12 result is window-dominated

**Uncommitted planning-time reconnaissance, disclosed because it changed the plan's
shape. It is not a result and it is not an artifact; execution must re-derive it.**

Integrating the committed `artifacts/v2.0/cevns_dRdT_ext.csv` (recoil axis, support
0.101 – 3165.6 eV_nr) and rescaling by the geometric factor
`(3.6/3.0)·(25/20.7)² = 1.7503` against CONUS+'s SM expectation
`347/327 = 1.0612 ± 0.1804` counts kg⁻¹ day⁻¹, the ratio moves by **more than three
decades** depending only on which nuclear-recoil window the `keV_ee` analysis window
is mapped to. A window whose lower edge sits near ~0.9 keV_nr lands within a few
percent of unity; a window whose lower edge sits near ~2.1 keV_nr — which is where a
Lindhard-type quenching factor sends **0.4 keV_ee** — lands ~3 decades low, because
our reactor-CEvNS Ge spectrum is at its **kinematic endpoint** there (`dR/dT` falls
from 4.7 × 10⁻³ at 2.0 keV to exactly 0.0 by 3.166 keV).

**Two consequences for the plan.**

1. **The window determination is the single highest-leverage step in VALD-12, and it
   is a live discrepancy inside this project's own documents.** `ROADMAP.md` and
   `REQUIREMENTS.md` both state the CONUS+ window as **0.4–1 keV_ee**;
   `GPD/literature/SUMMARY.md` separately records that CONUS+ "must be reproduced as a
   limiting case at **160 eV_ee**". Those are not the same window and they do not give
   the same verdict. The window must be fixed **from the anchor**, pre-registered
   before any integral is evaluated, and the discrepancy flagged for the orchestrator
   rather than resolved by picking the convenient one.

2. **A new forbidden proxy is required.** Selecting or adjusting the analysis window,
   the quenching model, or the flux tail so that the ratio lands near unity would be
   textbook confirmation pressure on a gate whose whole purpose is to be falsifiable.
   The plan therefore requires the **full ratio-versus-window sensitivity curve** on
   the deliverable — including the windows that fail — so that the window dependence
   is visible rather than hidden behind a single passing number.

**Do not treat the numbers above as the answer.** They were computed with a scratch
trapezoid quadrature on one column of one artifact, with no quenching model actually
sourced, and they are exactly the kind of first impression this project's record shows
should be checked rather than trusted.

</skeptical_review>

<deferred>
## Deferred Ideas

- **Muon-induced neutrons and muon-induced secondary gammas at the surface.** Not
  modelled anywhere in the milestone. Declared as a named omission with a bias
  direction; **not** computed here.
- **Cosmogenic activation of ⁷¹Ge / ⁶⁸Ge / ⁶⁵Zn by the fast component.** A real
  surface-detector effect, explicitly placed outside Phase 14 and not re-opened here.
- **RADX-01** — QPD-film / substrate / wafer-surface radioactivity. Still deferred,
  though it now partially overlaps CALC-21 because the Romani mechanism makes the Al
  film *area* a background source rather than a contaminant carrier.
- **Reconstructing the CaWO₄ closure fold** so that 407.7 dru has a reproducible
  artifact. Phase 12's `comparison_verdicts` recommends deciding this before Phase 16
  leans on it. This phase's disposition is to **cite it with its provenance gap
  attached** and to state the absence of any background-side validation; rebuilding
  the fold is not in scope.
- **Re-stating VALD-10's `<1 %` gate as a same-matrix comparison.** Phase 12 flagged
  that the Al→Hf 3.7246 % exceedance is a Phase-10 response-matrix regeneration
  artifact, not a Phase-12 defect. A milestone-level decision, not this phase's.
- **`REQUIREMENTS.md` re-wording.** CALC-11, CALC-18, CALC-19, CALC-20, CALC-23 and
  CALC-25 carry stale text, and `REQUIREMENTS.md` cites a `CONVENTIONS.md` §D VNS lock
  that never happened. Flagged for the orchestrator by Phases 13, 14 and 15; **no plan
  in this phase edits that file either.**
- **SENS-01 / MANU-01** — quantitative discovery sensitivity and the manuscript
  revision. Both enabled by this phase's output; neither is this phase.

</deferred>

---

_Phase: 16-s-b-particle-assembly-lee-overlay-and-the-signal-side-conus-check-p-sb_
_Context recorded: 2026-07-23 (no discussion session; standing directive)_
