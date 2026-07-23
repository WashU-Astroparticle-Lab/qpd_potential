# 16-01 — VALD-12, Signal-Side Leg: the CONUS+ Check, its Window, and what the Restatement Gives Up

**Plan:** 16-01 · **Phase:** 16 (terminal, milestone v2.0) · **Axis:** RECOIL throughout
**Interpreter:** `/opt/anaconda3/bin/python3` (numpy 1.26.4, scipy 1.17.1)
**Artifacts:** `artifacts/v2.0/conus_signal_side_check.csv`, `artifacts/v2.0/conus_window_sensitivity.csv`
**Module:** `src/qpd_potential/conus_check.py` · **Tests:** `tests/test_conus_signal_side.py`

---

## 0. The verdict, first

> **VALD-12 (signal-side leg) = PARTIALLY CONFIRMED — and the verdict is WINDOW-CONDITIONAL.**
>
> On the **pre-registered** window (0.4-1 keV_ee, ROADMAP/REQUIREMENTS) the ratio is
> **5.278664e-04** against a **pre-declared factor of 2.0**. **That leg is a FAIL**:
> VALD-12's signal-side leg is **not discharged on the window this project pre-registered**,
> and it misses by **3.28 decades**.
>
> On the **declared alternate** (160 eV_ee, `GPD/literature/SUMMARY.md`) the ratio at
> central quenching is **8.333761e-01** — inside the factor. Across the declared
> Lindhard-`k` bracket the alternate spans **4.012535e-01 … 1.764657e+00**, so two of
> its three rows pass and one fails.
>
> The full ratio spans **4.504 decades** across candidates, plus three rows at exactly
> zero. **This project's own documents do not agree on which window is CONUS+'s**, and
> the verdict is set by that disagreement rather than by the physics chain.

Nothing below rescues this. The pre-registered leg failed; that is reported as the
result, and the ROADMAP Phase-16 backtracking trigger is treated as live in §7.

---

## 1. Pre-registration, and the live internal discrepancy

The window and the pass/fail factor are declared as module constants in
`src/qpd_potential/conus_check.py` **physically above** every function that integrates
anything. `test_window_preregistered` asserts that ordering from the parsed AST — it is
the structural defence against `fp-window-tuned-to-pass`, which forbids choosing the
window after seeing which choice lands nearest unity.

| candidate | window | source | status |
|---|---|---|---|
| `preregistered_roadmap_requirements` | **0.4-1 keV_ee** | `GPD/ROADMAP.md` Phase-16 anchor line; `GPD/REQUIREMENTS.md` VALD-12 | **PRE_REGISTERED** |
| `alternate_literature_survey` | **160 eV_ee** (0.160-1 keV_ee) | `GPD/literature/SUMMARY.md`, twice: the risk entry and the validation row | declared alternate |
| `kinematic_probe_above_endpoint` | 1-2 keV_ee | declared in this plan; **not** a CONUS+ window | probe |

**The discrepancy is FLAGGED FOR THE ORCHESTRATOR and no file was edited.**
`ROADMAP.md` and `REQUIREMENTS.md` state **0.4-1 keV_ee**; `GPD/literature/SUMMARY.md`
states the limiting case at **160 eV_ee / 7.4 m.w.e.** These are not the same window and
they do not give the same verdict. The reason for pre-registering the former is stated
in terms of what the documents *are*, not what they *yield*: `ROADMAP.md` and
`REQUIREMENTS.md` are the project's authoritative scoping documents; the literature
survey is a survey. The choice was committed in source before any integral ran.

The probe candidate exists so that the `above_kinematic_endpoint` flag is exercised on
real data rather than asserted in prose — `test_kinematic_support_checked` fails if no
candidate lands above the endpoint and fails if no candidate is partially outside it.

---

## 2. The keV_ee → keV_nr conversion: **BRACKETED, not SOURCED**

No germanium ionization-quenching model is frozen anywhere under `data/` in this
repository, and none could be retrieved and integrity-checked in this environment —
`GPD/literature/SUMMARY.md` records that no NUCLEUS, CONUS/CONUS+ or RICOCHET arXiv
record carries ancillary data, each checked individually. Writing a recalled calibration
number would fabricate a sourced input, so the conversion is carried as an **explicit
bracket** and labelled `BRACKETED` on **every** emitted row.

**Declared model form** (written down so it can be challenged; not read from any frozen
artifact, not claimed as sourced):

```
Q(E_nr) = k·g(ε) / (1 + k·g(ε)),   g(ε) = 3ε^0.15 + 0.7ε^0.6 + ε,
ε = 11.5 (E_nr/keV) Z^(−7/3),      Z = 32 (germanium)
```

`k` is bracketed over **[0.130, 0.200]** with central **0.157**, the Lindhard analytic
`k = 0.133 Z^(2/3) A^(−1/2)` for natural Ge. Both bracket endpoints are extra rows of the
sensitivity table, so the bracket's width is on the deliverable rather than hidden inside
a point value.

**The one legal use of a quenching factor.** `CONVENTIONS.md` §B locks a single unified
phonon scale with **no ionization quenching**. Converting **their** window boundaries is
a coordinate change on **their** ionization axis and is legal. Multiplying **our** dR/dT
by a quenching factor is the milestone-wide forbidden proxy
`fp-quenching-on-phonon-scale` and does not happen. `test_no_quenching_on_our_spectrum`
proves it by **parsing** the module's AST — it collects every name bound from the
quenching call, asserts each is a window-boundary name, and asserts no multiplication or
division anywhere pairs such a name with a rate array. The scan is shown non-vacuous by
asserting the function exists, is called, and is called inside the boundary map. Parsing
rather than grepping is required here because the words "quenching" and "Lindhard" *must*
appear in this prose: naming the trap is the point.

Converted windows at central `k = 0.157`:

| window (keV_ee) | → keV_nr | Q(lo) | Q(hi) |
|---|---|---|---|
| 0.4 - 1.0 | **2.1165 - 4.7425** | 0.18899 | 0.21086 |
| 0.160 - 1.0 | **0.9430 - 4.7425** | 0.15851 | 0.21086 |

`test_window_in_both_scales` asserts both scales on every row, `E_ee < E_nr` strictly,
`Q ∈ (0,1)` strictly, and re-solves the boundary map inside the test rather than reading
it back.

---

## 3. The kinematic support — measured before anything was integrated

The committed `artifacts/v2.0/cevns_dRdT_ext.csv` runs to 3165.6057 eV_nr, but the
largest `T` at which `dR/dT` is **non-zero** is

> **kinematic support edge = 3031.6858 eV_nr**

re-derived inside the test from the artifact rather than transcribed. Reactor-CEvNS on
germanium reaches its kinematic endpoint inside the keV range, and the pre-registered
window straddles it:

| candidate | k | keV_nr window | support fraction | above endpoint | ratio | within factor 2.0 |
|---|---|---|---|:-:|---|:-:|
| preregistered | 0.130 | 2.4265 - 5.4159 | 0.2025 | no | 5.523721e-05 | **no** |
| **preregistered** | **0.157** | **2.1165 - 4.7425** | **0.3485** | no | **5.278664e-04** | **no** |
| preregistered | 0.200 | 1.7857 - 4.0228 | 0.5570 | no | 5.361286e-03 | **no** |
| alternate | 0.130 | 1.0847 - 5.4159 | 0.4495 | no | 4.012535e-01 | **no** |
| alternate | 0.157 | 0.9430 - 4.7425 | 0.5497 | no | 8.333761e-01 | yes |
| alternate | 0.200 | 0.7921 - 4.0228 | 0.6932 | no | 1.764657e+00 | yes |
| probe | 0.130 | 5.4159 - 9.9147 | 0.0000 | **yes** | 0.000000e+00 | no |
| probe | 0.157 | 4.7425 - 8.7128 | 0.0000 | **yes** | 0.000000e+00 | no |
| probe | 0.200 | 4.0228 - 7.4258 | 0.0000 | **yes** | 0.000000e+00 | no |

**Only 34.85 % of the pre-registered window lies inside the support of our own
spectrum.** The remaining 65 % is above the endpoint, where `dR/dT` is exactly zero — so
in that region the check is not testing the flux × cross-section × target chain at all;
it is testing where our reactor flux table runs out. A window lying wholly above the
endpoint records a **zero rate with an explicit flag**, never a silently truncated
integral (`fp-silent-endpoint-truncation`), and **no table was extended** to make any
window reachable.

---

## 4. The integral, the rescale, and the comparison

Units are written out rather than buried: `dR/dT` is in counts kg⁻¹ day⁻¹ **keV⁻¹** and
`T` is tabulated in **eV**, so the quadrature carries an explicit factor 1/1000.

**Geometric rescale, factors reported individually** (`fp-product-instead-of-factors` —
a product can be right by cancellation):

```
P_c = 3.6 GW_th,  P_v = 3.0 GW_th   →  P_c/P_v          = 1.2000000000
d_c = 20.7 m,     d_v = 25.0 m      →  (d_v/d_c)²       = 1.4586104693
                                       factor            = 1.7503325632
```

Assumed: a point source, rate linear in thermal power, and the **same antineutrino
spectral shape** at both sites. The fission-fraction difference between the 3 GW_th
reference core and CONUS+'s Leibstadt core is a **named, unquantified systematic** —
this project holds nothing that could quantify it, and no guessed correction is folded in.

**CONUS+'s SM expectation as a rate**, division shown rather than quoted:

```
347 / 327 = 1.0611620795 counts kg⁻¹ day⁻¹,  uncertainty 59 / 327 = 0.1804281346
```

CONUS+ Collaboration, *Nature* **643**, 1229 (2025), arXiv:2501.05206; observed
395 ± 106 at 3.7σ. Every CONUS+ number here is a **citation**, never a download.

`test_ratio_against_sm_expectation` recomputes every emitted ratio independently inside
the test, from the committed recoil table, to 1e-6 relative — the numbers are
recomputed, not transcribed.

---

## 5. The independent route, and how far it reaches

`cevns.conus_rescale_check()` compares our flagship flux model against Billard's
independently normalized one at the CONUS+ geometry. It is not an algebraic identity of
this plan, so agreement is information:

```
R_ours_at_conus = 1.185887e+02      R_billard_at_conus = 1.196293e+02
ratio = 0.991302   →  the two routes agree on the absolute rate scale to 0.87 %
```

**That agreement does not reach the window, and this report says so rather than letting
the reader assume it does.** `conus_rescale_check` integrates from a 50 eV recoil floor,
and that integral is overwhelmingly low-`T`. Measured, not assumed:

| quantity | value |
|---|---|
| rate above the 50 eV floor | 67.760571 counts kg⁻¹ day⁻¹ |
| fraction of it above the **pre-registered** lower edge (2.1165 keV_nr) | **4.722893e-06** |
| fraction of it above the **alternate** lower edge (0.9430 keV_nr) | 7.456330e-03 |

So the 1 %-level Billard agreement constrains the **bulk** normalization and says
essentially **nothing** about the 2-5 keV_nr tail the pre-registered window probes. It is
evidence that the chain's overall scale is sound; it is **not** evidence that the
endpoint region is right, and it must not be read as the latter. The high-`T` tail is set
by the ≳ 8 MeV part of the reactor antineutrino spectrum, which is the least-constrained
part of the flux input this milestone owns.

---

## 6. The IA omission, measured rather than asserted

CONUS+'s SM expectation is a Freedman + Helm calculation with no impulse-approximation
kernel in it, so the like-for-like comparison object is our **unbroadened** dR/dT. The
size of the omission is **measured** at both edges of the pre-registered window with the
`CONVENTIONS.md` §J locked ω̄ = 1.7859677040e-02 eV, `σ_E/E_R = √(ω̄/E_R)`:

| window edge | E_R (eV_nr) | σ_E/E_R |
|---|---|---|
| pre-registered lower | 2116.49 | **2.904884e-03** |
| pre-registered upper | 4742.51 | **1.940585e-03** |

Phase 15 established that this project's "too small to matter" arguments have been
**false** when actually checked, so this is measured and reported, **not asserted small**.
Direction: a symmetric kernel on a steeply falling spectrum near an endpoint moves counts
both ways across a window edge; at ~0.3 % and ~0.2 % fractional width the effect is orders
below the decades the window choice moves, which is why it is not the story here. It
would matter if the window sat near 100 meV, where the fractional width is comparable to
the window itself. It does not.

---

## 7. VALD-12 verdict, and the backtracking trigger

**Verdict: PARTIALLY CONFIRMED, window-conditional.** Pre-registered ratio
**5.278664e-04** against the pre-declared factor **2.0**; the pre-registered leg is a
**FAIL**. The declared alternate's central row passes; its bracket-low row does not.

The ROADMAP Phase-16 backtracking trigger is in force: *"treat the failure as evidence
about our own flux × cross-section × target chain, not about CONUS+, and claim no
headline until it is understood."* What is understood, and what is not:

**Understood.**
1. The window mapping is where the decades live. The ratio moves 4.504 decades across
   candidates whose lower edges differ by about a factor two in nuclear-recoil energy,
   and the mapping itself rests on a quenching model this project could not source.
2. 65 % of the pre-registered window lies **above our spectrum's kinematic endpoint**
   (3031.6858 eV_nr). In that region the comparison is structurally unable to test the
   chain, whatever the chain is.
3. This project's own scoping documents and its own literature survey state **different
   windows**, and the verdict follows the choice.

**Not understood, and not claimed to be.**
4. Whether the 2-5 keV_nr tail of our spectrum is right. The one independent handle
   available (the Billard route) carries under 5e-06 of its weight there.
5. Whether CONUS+'s quoted SM expectation uses a form factor and radius compatible with
   our Freedman + Helm implementation. If not, part of any residual is theirs, not ours.

**Consequence for plans 16-02 and 16-03, per the plan's own escalation rule.** The two
downstream plans may **compute** `S/B_particle`, and they do. But the unresolved gate
travels onto every downstream deliverable: **`S/B_particle`'s numerator has one external
check, and that check passes only on a window this project cannot settle.**

---

## 8. What the restatement gives up — written on the deliverable

The 2026-07-22 restatement retired VALD-12's background-side leg. That is a real loss and
it is disclosed here rather than quietly dropped.

- **Reproducing CONUS+'s S/B is not a coherent test for this pipeline.** They sit at
  **7.4 m.w.e.** behind a shield this project does not model. Matching their ratio would
  require **modelling their shield**, which is out of scope for an unshielded-surface
  pipeline. Producing a matching ratio could only be done by inventing one.
- **Consequence: the milestone carries no external validation of the ratio
  `S/B_particle` itself — it has external validation of its NUMERATOR only.** That
  sentence travels onto the headline deliverable (plans 16-02 and 16-03).
- **Since VALD-11's deletion there is no background-side target-swap validation at all.**
  Not a weak one — none.
- The one signal-side closure the milestone ever had, the **407.7 dru** CaWO₄ fold (ratio
  1.14 to NUCLEUS Table 5 at 100 % duty), has **no reproducible artifact** in this
  repository. A **word-bounded** search (`git grep -lE '(^|[^0-9.])407[.]7([^0-9]|$)'`)
  returns GPD prose alone; a naive substring search falsely matches a dozen committed
  numeric CSVs. It was folded at the NUCLEUS/VNS normalization, so it is
  **neither re-run nor rescaled** here, and it is cited as an **unreproduced prior
  assertion**.
- **CONUS+'s measured S/B ≈ 0.03 is retained as context for a shielded experiment**,
  explicitly **not** as a gate and **not** as a target.
- The pre-re-scope S/B expectation and the accompanying claim of being far better than
  the published state of the art are **WITHDRAWN** by the 2026-07-22 re-scope, and **no
  replacement expectation** is asserted anywhere in this phase.

---

## 9. Checkpoint (Task 3), recorded in full

Standing session directive: run the roadmap without per-phase discussion unless a genuine
blocker arises. The checkpoint's content is recorded here **in full** and the default was
taken. **No approval was given and none is fabricated** — the precedent of 12-03 §6,
13-03 and 14-02 §8.

> **VALD-12 signal-side verdict: PARTIALLY CONFIRMED, ratio 5.278664e-04 against a
> pre-declared factor 2.0, on the 0.4-1 keV_ee window (ROADMAP.md / REQUIREMENTS.md).**
> The pre-registered leg is a FAIL; the declared 160 eV_ee alternate gives 8.333761e-01
> at central quenching. The verdict's dependence on the window is 4.504 decades across
> the candidates. Proceed to the `S/B_particle` assembly (16-02) on these terms?
> **[Y/n/e]** (Enter = Y)

**Escalation taken, not defaulted.** Because the pre-registered leg failed, the gate is
recorded as unresolved and travels onto every downstream deliverable. Plans 16-02 and
16-03 compute `S/B_particle`; the unresolved signal-side gate and the numerator-only
statement are carried on their reports and artifacts.

---

## 10. Findings flagged for the orchestrator (no file edited)

1. **The CONUS+ analysis window is a live internal discrepancy.** `GPD/ROADMAP.md` and
   `GPD/REQUIREMENTS.md` say 0.4-1 keV_ee; `GPD/literature/SUMMARY.md` says the limiting
   case is at 160 eV_ee. They give opposite VALD-12 verdicts. **Neither file was edited.**
2. **No germanium ionization-quenching model is frozen in this repository.** VALD-12's
   verdict depends on one. The conversion is `BRACKETED`, and it should stay labelled
   that way until a model is retrieved and integrity-checked.
3. **The 407.7 dru closure still has no reproducible artifact.** Phase 12's
   `comparison_verdicts` recommended deciding this before Phase 16 leaned on it; this
   phase's disposition is to cite it with its provenance gap attached.
