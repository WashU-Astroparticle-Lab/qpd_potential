# Phase 8 — VALD-09 Gate Verdict and Milestone Disposition

**Deliverable:** `deliv-gate-verdict`
**Plan:** 08-05 · **Produced:** 2026-07-22
**Requirement discharged:** VALD-09 (GATING — v2.0 milestone stop-condition)
**Authority of this document:** it determines fit against *published* geometry and reports the
consequent disposition. It does **not** choose a re-scope direction, redesign the experiment, or
assign any veto credit above 1.0.

**Assembled, not computed.** Every number below traces to a completed Phase-8 artifact. No
quantity was generated in this plan. Where a number would have been useful and no upstream plan
produced it, that is recorded as a gap rather than filled.

**Sign convention (inherited from Plan 08-03):** clearance `C = D_available − W_required` in cm;
`C < 0` is a shortfall of `|C|`.

---

## 1. The verdict

> **NO FIT.**
>
> On the **coverage** comparison: with the wafer face mounted parallel to the cryogenic-outer-veto
> (COV) cap plane, a circular cap crystal must have a diameter of **√2 × 10.16 = 14.3684 cm** to
> cover the wafer's projected footprint. The published COV cap-crystal outer diameter is
> **10.0 cm** — arXiv:2508.02488v1 §2 "Cryogenic Outer Veto" ("100 mm diameter"), independently
> corroborated by arXiv:1905.10258 (EPJC 79, 1018 (2019)) Fig. 8 caption ("a diameter of 10 cm").
> The clearance is **C = −4.3684 cm**. The cap is **30.4 % smaller than required**; equivalently
> the requirement is **43.7 % larger** than the published cap.

**Both premises, stated with the verdict rather than beneath it:**

1. **Coverage premise** — a COV cap crystal must *cover* the wafer footprint. Licensed by the
   paper's own description of the COV as one that "hermetically covers the cryogenic target
   detectors" (08-01 evidence block A.11). Weaker than any cavity assumption, but not premise-free.
2. **Face-parallel mounting premise** — the wafer face lies parallel to the cap plane, as in every
   planar cryogenic detector stack and as implied by the wafer's single instrumented face
   (~10,300 sensors at 1/mm² on one face, `GPD/CONVENTIONS.md` §D). This is an **assumption**.

**Sign-robustness across the published dimension's precision interval** (Plan 08-03 §4, each
clearance re-evaluated at the interval endpoints, not asserted):

| Reading of the published cap diameter | Half-width | Coverage clearance interval | Sign |
|---|---|---|---|
| "100 mm diameter" (2 s.f.) | ±0.05 cm | [−4.418, −4.318] | preserved |
| widened | ±0.10 cm | [−4.468, −4.268] | preserved |
| "a diameter of 10 cm" (1 s.f.) | ±0.50 cm | [−4.868, −3.868] | preserved |

The coverage clearance changes sign only at a cap diameter of **14.3684 cm**, a rounding
half-width of **4.3684 cm**. No published reading of either source approaches that.

### 1.1 The clearance is mounting-conditional — this is part of the verdict

**−4.37 cm is not a purely geometric result, and must never be presented as one.**

The orientation-invariant coverage requirement — the one that holds with *no* mounting assumption
— is the edge-on projection floor √(a² + t²) = **10.1620 cm**, which against 10.0 cm gives only
**−0.1620 cm**, and that clearance is **not** sign-robust (it flips at a cap diameter of
10.1620 cm, a half-width of 0.162 cm, which the 1-significant-figure published reading spans).

| Coverage requirement | Value | C vs D = 10.0 | Robust to rounding? | Needs a mounting premise? |
|---|---|---|---|---|
| Face-parallel, √2·a | 14.3684 cm | **−4.3684** | **Yes**, by 4.37 cm | **Yes** |
| Orientation-invariant floor, √(a²+t²) | 10.1620 cm | **−0.1620** | **No** | **No** |

**The coverage basis's robustness comes from the mounting premise, not from geometry alone.**

### 1.2 All bases, with the one positive number reported rather than suppressed

| Basis | W_required (cm) | D_available (cm) | **C (cm)** | Sign-robust? |
|---|---|---|---|---|
| **COVERAGE (verdict basis)**, √2·a, face-parallel | 14.3684 | 10.0 | **−4.3684** | **Yes** to dimension rounding; **No** to orientation |
| Coverage, orientation-invariant floor, √(a²+t²) | 10.1620 | 10.0 | −0.1620 | No (flips at half-width 0.1620 cm) |
| EDGE (premise-free corroboration), a | 10.1600 | 10.0 | −0.1600 | **No** under the published 1-s.f. reading |
| CAVITY, in-plane *(ESTIMATE)* | 10.1600 | 5.0 | −5.1600 | Rounding yes; **premise unverified** |
| CAVITY, diagonal *(ESTIMATE)* | 14.3684 | 5.0 | −9.3684 | Rounding yes; **premise unverified** |
| *Loose cavity bound, for contrast* | 14.3684 | 16.7 | **+2.3316** | — **does NOT exclude the wafer** |

**No clearance on any of the four named bases came out positive.** The escalation condition in the
plan's `stop_and_rethink_conditions` — a positive coverage clearance, or one that loses its sign
inside its stated interval — was therefore **not triggered**, and this document is written for the
no-fit branch.

The **single positive number anywhere in the determination** is the loose cavity bound of
+2.3316 cm (Plan 08-03 §5: `D_cavity ≤ 29.7 − 8.0 − 5.0 = 16.7 cm`). It is reported here
prominently rather than buried, because it is precisely *why* the loose route cannot carry a
verdict: it is an explicitly non-excluding upper bound. It is the reason the verdict is routed
through the coverage comparison against the published cap outer diameter, which needs **no cavity
assumption at all**. The tight and loose cavity bounds differ by more than a factor of three and
only one of them excludes the wafer; Plan 08-03 keeps them as two separately named constants and a
test asserts no merged cavity constant exists.

### 1.3 The premise-free minimal statement, and why it is not the verdict basis

The most compact statement needing **no premise of any kind** is: *the wafer's 10.16 cm edge is
wider than the entire 10.0 cm cap crystal.* Clearance **−0.1600 cm**.

**This is corroboration, not the verdict.** Its margin is smaller than its own input precision. It
flips sign at a cap diameter of 10.16 cm (half-width 0.16 cm), and the 2019 paper's published
1-significant-figure "a diameter of 10 cm" implies ±0.5 cm, giving the interval
[−0.660, **+0.340**] — an explicit, published reading of the source under which this clearance is
**positive**. Plan 08-03 §4.1 also corrected an anticipated ±0.1 cm flip that the arithmetic does
not support: at ±0.1 the interval is [−0.26, −0.06], sign preserved but by less than the
half-width. Staking a milestone-gating stop-condition on a 0.16 cm margin drawn from a
1-to-2-significant-figure source would be `fp-unstated-precision`.

**Neither leg of the argument is simultaneously premise-free and sign-robust.** The coverage leg is
sign-robust but needs a coverage premise and a mounting premise. The edge leg needs no premise at
all but is not sign-robust. Stated in exactly those terms so that no downstream artifact can
recover a false certainty from either.

The two cavity comparisons (−5.16 cm and −9.37 cm) are **estimates** resting on the unverified
premise that the four rectangular 2.5 cm slabs sit inside the 10 cm cap rim. The verdict rests on
neither.

### 1.4 What the margin's size does and does not license

**Size of the margin:** 4.3684 cm on the verdict basis. Overturning the verdict requires a
published Chooz cap crystal of **at least 14.3684 cm** diameter — **more than 43 % larger** than
the published 100 mm. Plan 08-03 §9 item 3 quantifies the consequence: a cap 43 % larger in
diameter is 2.06× in area and, at the published 2.5 cm thickness, would mass **2.06 kg** rather
than the independently published "a mass of 1 kg" — a change that would be visible in any published
mass statement.

**What the margin licenses:**

- A confident no-fit determination **under the face-parallel mounting premise**, robust to every
  rounding interval either published source can support.
- Treating the VALD-09 stop-condition as **triggered**.

**What the margin does NOT license:**

- Claiming a purely geometric no-fit. Geometry alone delivers **−0.16 cm**, which is not
  sign-robust. (Plan 08-03 §9 item 5 identifies a published statement that the wafer would be
  mounted other than face-parallel as *the single most efficient way to disconfirm the current
  framing*: under such a mounting the coverage determination becomes **inconclusive**, not no-fit.)
- Any statement about the cavity's **vertical** axis, which is entirely unconstrained by available
  sources.
- Any quantitative claim about **how much** the post-shield fluence would change under a redesign.
  Nothing in this phase computed that (see §4).
- Treating the estimated cavity shortfalls (−5.16, −9.37 cm) as measured.

---

## 2. The limits of this verdict — carried next to it, not in a footnote

A gate that forces a milestone re-scope must carry its own uncertainty where the decision-maker
will see it.

**2.1 Provenance: the load-bearing dimension comes from a commissioning paper outside the anchor
list.** `arXiv:2508.02488` is **NOT in the `GPD/ROADMAP.md` Phase-8 anchor list.** It was promoted
to a Phase-8 anchor during execution (record: 08-01 §D; carry-forward: 08-03 §1.2). Two facts
travel with every number taken from it:

- **It describes the TUM commissioning setup, not Chooz.** In that setup, "only one of the six
  crystals is installed directly above the target detectors" (08-01 A.1). It is not a Chooz
  engineering drawing.
- **It is the single load-bearing geometric source of this phase** — the 10.0 cm cap diameter, the
  29.7 cm internal shielding and the 43.0 cm bore all come from it.

What licenses the 100 mm read: the mass closure ρ_Ge · π · (5.0 cm)² · (2.5 cm) = **1045.17 g** at
ρ_Ge = 5.323 g/cm³ against the paper's independently published "a mass of 1 kg" (08-01 §C.1). This
is reported as **consistent with a 1-significant-figure "1 kg"** — *not* as "within 5 %": the
margin against a naive ±5 % band is only 4.8 g, and at ρ_Ge = 5.35 the naive band fails.

**2.2 The strongest independent evidence was never obtained.** The **Goupy 2024 thesis**
(NNT 2024UNIP7170 / HAL tel-05298505) is the only genuinely independent third route to the COV
internal cavity and the copper support geometry. It is unobtainable by any scripted route
(`data/external/nucleus/MANIFEST.md` §4 records the live anti-bot challenge signature; the
acquisition was recorded as a failure rather than faked). **What that costs the determination:**
no independent corroboration of the cavity exists at all. The Fig. 1(e) pixel measurement of
08-03 §7 is explicitly **not** a third route — it takes its scale from the same published numbers
(anchor A uses the same 100 mm cylinder; anchor B uses a different number but the same paper).

**2.3 The weakest anchor in the phase is the ~5 cm COV internal cavity claim.** It rests on the
unverified premise that the rectangular 2.5 cm slabs sit inside the cap rim, and it could fail if
the rectangular crystals are larger than the caps.

**What stands independently of that weakest anchor:**

- The **verdict itself** — the coverage comparison is against the published cap *outer diameter*
  and makes no cavity assumption whatsoever.
- The **three-tier taxonomy** (`GPD/analysis/VETO-TAXONOMY.md`) — a classification of published
  statements, correct either way, as its own §"This taxonomy stands independently of the
  geometry-fit verdict" records.
- The **multiplicity identity** `ε_mult(1) ≡ 0` — a counting identity, not a geometry claim.
- The **self-veto decomposition** (`A_self_direct`, `A_self_induced`) — derived from the wafer's own
  frozen chord × Landau–Vavilov deposit distribution.

**2.4 Additional carried caveats.** The vertical axis of the cavity is unconstrained.
`08-RESEARCH.md` §F1's orientation lemma was found **false** during Plan 08-03 and retracted in
place (with dated corrections at §F1, Pitfall 7, the SC1 starting-point table and Caveat 2);
anything else in that document resting on it should be treated as suspect until re-checked. It was
wrong **in the direction that favoured the project's expected conclusion**.

**2.5 A trap, flagged.** The strings `10.16 cm` and `1.27 cm` **do** appear in arXiv:2509.03559v1 —
in §4.2.1, as **Bonner-sphere Pb shell converter** dimensions. The coincidence with the wafer's
10.16 cm edge is accidental and unrelated to the veto envelope. Neither may ever be cited as a veto
dimension.

### 2.6 What would overturn this verdict (carried from Plan 08-03 §9)

1. **The Goupy 2024 thesis showing rectangular COV crystals large enough for a cavity of at least
   10.16 cm in two axes.** Overturns the two *cavity* clearances outright. Does **not** touch the
   verdict, which makes no cavity assumption. Status: unobtained.
2. **A published NUCLEUS upgrade geometry with a materially larger cavity.** Same scope. To touch
   the verdict it would additionally have to enlarge the **cap crystals**.
3. **Evidence that the 100 mm crystal is commissioning-only, with larger Chooz cylinders.**
   Weakened qualitatively by arXiv:2509.03559v1's independent 2.5 cm COV thickness (matching the
   commissioning 25 mm) and by the 2019 paper's independent "10 cm" from a setup generation six
   years earlier; quantified above (43 % larger ⇒ 2.06 kg vs published 1 kg).
4. **A source stating the COV internal cavity dimension directly.** Replaces the cavity rows with a
   measurement; does not touch the coverage or edge rows.
5. **A published statement that the wafer would be mounted other than face-parallel.** Does not
   overturn the verdict but **collapses its margin** to the orientation-invariant −0.1620 cm, which
   is not sign-robust — the determination would become **inconclusive on the coverage basis**. This
   is the single most efficient disconfirming observation.
6. **The two figure-scaling anchors disagreeing by more than ~30 %.** Tested: they agree to 6.6 %.
   Did not occur.

---

## 3. The five ROADMAP Phase 8 Success Criteria — coverage map

Two rows carry **documented deviations from the criterion as literally written**. They are flagged
here as deviations, not absorbed.

| # | Criterion (abbreviated) | Discharging artifact | Section | Acceptance test(s) | Outcome |
|---|---|---|---|---|---|
| **1** | Read COV/IV envelope from EPJC 86,29 Fig. 1(e)/(f), record provenance, compare against the wafer's 103 cm² × 2 mm footprint as an explicit fit/no-fit determination quoting the clearance in cm | `08-03-FIT-DETERMINATION.md` (with `08-01-SOURCE-EVIDENCE.md` §F.6/§F.8 establishing the amendment); `src/qpd_potential/veto_envelope.py` | §0 verdict; §1 amendment; §3 four clearances; §4 sign robustness | `test-four-bases`, `test-sign-robustness`, `test-dmin-arithmetic`, `test-bound-separation`, `test-orientation-invariance`, `test-amendment-documented`, `test-verdict-falsifiable`, `test-fig1-silence` | **DISCHARGED — with a documented evidence-route amendment (see 3.1)** |
| **2** | Binding L1/L2 taxonomy; L1 (environmental) transfers, L2 (payload-coupled) defaults to 1.0 and may not appear downstream without wafer geometry behind it | `GPD/analysis/VETO-TAXONOMY.md`; `src/qpd_potential/veto_credit.py` | §2 tier definitions & swap test; §2.1 the extension statement; §3 the 19 rows; §8 credits in code | `test-taxonomy-complete`, `test-verbatim-classification`, `test-credit-sentinel`, `test-no-orphan-veto-factor`, `test-l1star-documented` | **DISCHARGED — extended from two tiers to three (see 3.2)** |
| **3** | The wafer's own muon-veto acceptance is **derived** from its own chord-length distribution using the v1.0 Gaisser–Guan ⊗ chord machinery; no NUCLEUS rejection percentage transferred as a number | `src/qpd_potential/wafer_self_veto.py`; `data/wafer_self_veto.csv` | `a_self_direct()`; `A_SELF_INDUCED`; CSV rows 1–4 | `test-normalization-closure`, `test-acceptance-monotone`, `test-split-reported`, `test-induced-zero-named`, `test-no-transferred-percentage` | **DISCHARGED — two separately reported acceptances (see 3.3)** |
| **4** | The monolithic single-readout wafer carries **no multiplicity handle at all**; NUCLEUS's multiplicity cut contributes exactly zero rejection, stated explicitly and not absorbed into a lumped factor | `src/qpd_potential/wafer_self_veto.py` `mult_rejection()`; consumed by `veto_credit.multiplicity_rejection_is_zero()`; documented in `VETO-TAXONOMY.md` §4 | the `N = 1` early-return identity, asserted under **exact identity comparison** `== 0.0`, not a tolerance | `test-multiplicity-identity` (plus `test-counterpoint-recorded`) | **DISCHARGED — by unit-tested identity (see 3.4)** |
| **5** | Stop-condition discharged: on a no-fit verdict, report the milestone premise as void, return control to the user for re-scope; no reduced veto credit assumed, no resized veto invented | **this document** | §1 (verdict), §4 (premise void), §5 (phase disposition), §6 (surviving deliverables), §7 (prohibitions), §8 (return of control) | `test-verdict-stated`, `test-verdict-falsifiability-carried`, `test-premise-statement`, `test-disposition-justified`, `test-no-credit-no-redesign`, `test-control-returned` | **DISCHARGED — see §8** |

### 3.1 Deviation on Criterion 1 — the evidence route was amended

**The criterion as literally worded cannot be discharged.** It names EPJC 86, 29 (2026) Fig. 1(e)/(f)
as the evidence route. That route is **dimensionally silent**, established by direct inspection
rather than inference:

- Figure 1 carries **no scale bar, no ruler, no dimension leader, and no numeric dimension callout
  on any of panels (a)–(f)**. The complete set of numerals anywhere on the figure is the six panel
  letters, the reactor labels B1 and B2, and the array multiplicity "3 × 3" on panel (f). Verified
  at full resolution on the frozen 1875 × 2613 px image across all six panels (08-01 §F.6).
- The paper states **no internal envelope, cavity, or clearance dimension for the COV or the IV
  anywhere in the document.** The only COV dimension it gives is a 2.5 cm crystal thickness. The
  words "envelope", "cavity", "inner diameter" and "clearance" do not occur in the text at all.
  Established by exhaustive enumeration of every `cm`/`mm` numeric token, not a targeted search
  (08-01 §F.8).
- Both findings hold in **both** the arXiv v1 and the published journal version; the same
  enumeration against the retrieved open-access EPJC HTML returns the same token set and the same
  zero counts.

**Substituted route:** the COV cap-crystal outer diameter of 100 mm from **arXiv:2508.02488v1 §2**,
independently corroborated by arXiv:1905.10258 Fig. 8. **Justification:** the criterion's *purpose*
is to determine fit against published NUCLEUS geometry; its named source contains one COV
dimension (a thickness) and no envelope. Substituting sources that carry the needed dimensions
preserves the purpose; quoting a callout the named figure does not carry would not.

**Disclosure that must travel with the amendment:** arXiv:2508.02488 is (a) promoted to a Phase-8
anchor during execution, (b) **absent from the ROADMAP anchor list**, and (c) a description of the
**TUM commissioning setup, not Chooz**. **No dimension entering any clearance, any bound, or the
verdict is attributed to Fig. 1(e) or Fig. 1(f).** The only use of Fig. 1(e) is a relative pixel
measurement scaled against externally published anchors (08-03 §7), labelled corroborative,
carrying no verdict weight, and entering no clearance.

### 3.2 Deviation on Criterion 2 — the binary split was extended to three tiers

The criterion specifies a **binary** L1/L2 split. `VETO-TAXONOMY.md` §2.1 extends it to three
tiers, **presented as an extension rather than as the criterion's original wording**.

**Why the binary split has no slot for the liner:** the nearly-4π 4 cm boron carbide liner and the
internal shielding are *passive materials*, which reads L1 — but the published suppression factor
attached to the liner is quoted for a nearly-4π geometry in the direct vicinity of a
centimetre-scale payload, which reads L2. Forced into the binary split they would go to L1, because
"passive" is the more visible property. **That is the wrong answer:** promoting them to L1 would
flatter the background budget at precisely the point where the wafer's size is the disputed
quantity.

**L1\*** (passive but payload-geometry-coupled) records the disagreement rather than resolving it
by fiat. Its credit is **1.0**, the same as L2. The reviewer's counter-argument (4 cm of B₄C
attenuates neutrons whether the object behind it is 2.25 cm² or 103 cm², so the liner is arguably
close enough to pure attenuation to be L1) is recorded in taxonomy §5 rather than suppressed, along
with the observation that would collapse L1\* into L1 — none was found in either version.

Final tier counts: **6 L1, 2 L1\*, 11 L2 = 19 rows.** Every L1\*/L2 credit is exactly 1.0; every L1
row also carries 1.0, because 1.0 is the *empty* credit (background unchanged), not full credit.

### 3.3 Criterion 3 — two acceptances, never lumped

| Quantity | Value | Note |
|---|---|---|
| `A_self_direct` @ 10 eV | **1.000000000000** | at the 10.14 eV table floor — edge of support, stated not extrapolated |
| `A_self_direct` @ 1 keV | **0.999971887382** | complement 2.784e−05 ± 1.20e−06 (MC) |
| `A_self_direct` @ 100 keV | **0.997858048250** | complement 2.115e−03 ± 1.08e−05 (MC) |
| `A_self_induced` | **0.0** exactly | no parent-muon handle; a defensible **floor**, not an impossibility proof |

These are **two different numbers about two different populations** and are never merged
(`fp-lumped-acceptance`). The near-unity direct acceptance is the physically expected outcome of a
1.2323 MeV vertical-chord Landau MPV against eV-to-100-keV thresholds — the half of the problem that
was never the difficulty — and reporting it alone would mask `A_self_induced = 0`, which is exactly
the class NUCLEUS's vetoes suppress and the wafer cannot touch. Denominator closure (gate V6):
1.365237 Hz against the frozen header 1.3659 Hz, **−0.0485 %**, inside the 1 % criterion.

Live-time cost, for completeness: `R_mu(2.92 m w.e.) = 0.968723 Hz`, `f_dead = 3.874894e−05` at
40 µs and `1.937447e−05` at 20 µs — both labelled **first-order lower bounds**.

### 3.4 Criterion 4 — the unit-tested identity, cited rather than described

```
eps_mult(N) = 1 − P(exactly one of N target channels above threshold)
```

For a single-readout monolithic target, `N = 1`. Any event that triggers at all triggers the one
and only channel, so `P(exactly one) = 1` and **`eps_mult(1) = 0` exactly**. `mult_rejection(1)`
returns `0.0` through an early return of the literal, asserted under **identity comparison
(`== 0.0`)**, not a tolerance. The binomial-conditional occupancy model used for `N > 1` *itself*
returns 0 at `N = 1` for every `p_hit ∈ (0, 1]` — `N p (1−p)⁰ / (1 − (1−p)) = p/p = 1` — so the
identity does not depend on the occupancy model at all; the early return **agrees with** the model
rather than substituting for it. The transferable credit is therefore `1 − 0 = 1.0` **by
derivation**, the one row in the taxonomy whose 1.0 is not a policy default.

**Counterpoint, reported because it cuts against this project's own framing.** NUCLEUS themselves
call the benefit of the inner-veto-plus-single-hit conjunction "**very marginal**" (verbatim,
§5.2.1, evidence-block B.7). Read plainly: because the handle *they* gain from that cut is small,
the **absolute background cost of the wafer's identically-zero multiplicity handle is also small.**
That weakens the "we lose their multiplicity cut" framing. Both statements stand together: the
rejection is exactly zero, **and** its consequence is small.

### 3.5 VALD-09's area comparison — basis label attached, and a discrepancy flagged

VALD-09 as written states the wafer has "**~11× the footprint (103 vs ~9 cm²)**". That comparison
requires a basis label, because the two available bases differ by exactly a factor of 4:

| Basis | Reference footprint | Ratio | Provenance |
|---|---|---|---|
| **Published array-crystal footprint** | **2.25 cm²** = 9 × (5 mm)² | **45.9×** | arXiv:1905.10258 Fig. 8 + §3.2.1; the 5 mm edge independently confirmed by two mass closures (CaWO₄ 4.996 mm, Al₂O₃ 5.008 mm) |
| **Project holder-scale estimate** | **~9 cm²** | **11.5×** | **THIS PROJECT'S OWN NOTES.** Not a NUCLEUS number; not traceable to any NUCLEUS publication |

Wafer face area **103.2256 cm²**. `veto_envelope.area_ratio()` raises `ValueError` unless a basis
is named explicitly (`fp-unlabelled-area-ratio`).

> **OPEN FOLLOW-UP, flagged for the user and deliberately not acted on.** Plan 08-04 corrected
> `GPD/literature/PITFALLS.md` only. **`GPD/REQUIREMENTS.md` (VALD-09) and the `GPD/ROADMAP.md`
> Phase-8 anchor line ("wafer 103 cm² vs their ~9 cm²") still carry the unlabelled figure**, so the
> requirement text and this gate verdict would otherwise silently disagree. Editing those two files
> is out of scope for Phase 8 by the phase-context decision; the discrepancy is recorded here so it
> is visible rather than resolved by drift.

---

## 4. The milestone premise is VOID

**On a no-fit verdict the v2.0 structural premise does not survive.**

The premise, as the ROADMAP states it: *only the target-independent fluence φ(E) at the detector
position transfers from NUCLEUS to us*, with that experiment's measured environment and passive
attenuation adopted as input while the target response is re-folded for Ge.

**The physical reasoning chain:**

1. A wafer of this size **cannot occupy the published envelope** (§1).
2. Deploying it there therefore **forces a redesign** of:
   - the **cryogenic outer veto** — the cap crystals cannot cover the footprint;
   - the **copper support structure** — it must hold a 103.2256 cm² plate rather than gram-scale
     3 × 3 arrays in a TES-instrumented silicon holder;
   - the **nearly-4π 4 cm boron carbide liner** — its arrangement is set by what it encloses
     (taxonomy `row-a09`, `row-b04`);
   - and **plausibly the internal shielding and the cryostat bore** (published at 29.7 cm and
     43.0 cm respectively), since the internal shield "follows the same layer arrangement as the
     external shielding" *inside* the cryostat, arranged around the target.
3. **Those are exactly the components that shape the neutron and gamma fields immediately around
   the target position.**
4. Therefore **the post-shield fluence at the detector position is no longer NUCLEUS's post-shield
   fluence.** φ_post is not transferable.
5. Consequently **essentially nothing beyond room-level environmental quantities transfers** — the
   2.92 ± 0.01 m.w.e. overburden, the 1.41 ± 0.02 omnidirectional muon attenuation, the Table 4
   surface flux normalizations, and the measured 5.03 cm⁻²s⁻¹ VNS gamma ambience. Those are
   properties of the site and the incident field, not of what sits in the cryostat.

> **HONESTY CONDITION — this reasoning is physically well-motivated but is NOT QUANTIFIED anywhere
> in this phase.** No one has computed how much φ_post would change under a redesign. The claim is
> that it changes materially, and the argument is a component-level one, not a transport
> calculation. A referee could reasonably demand the number; this phase does not have it, and full
> Geant4 transport of the NUCLEUS geometry is out of scope by explicit user decision.

---

## 5. Phase-by-phase disposition, Phases 9 through 16

Each disposition is argued from that phase's **stated Depends-on and Anchor-coverage rows** in
`GPD/ROADMAP.md`, **not** from the dependency arrows.

> **The non-obvious result: Phases 10 and 11 are physically site-independent and survive intact,
> even though the ROADMAP's Phase Dependencies table draws arrows 8 → 10 and the wave schedule puts
> Phase 10 behind the gate.** The ROADMAP itself concedes the arrow is scheduling, not physics:
> *"Phase 10's grid work is nominally site-independent and could technically start before the gate
> closes, but it is not scheduled ahead of it."* The arrow encodes a policy about not building on a
> premise under review; it does not encode a physical dependency.

| Phase | Disposition | Justification from stated dependencies and anchor coverage |
|---|---|---|
| **9** — VNS Environment Lock & Fluence Recovery (P-ENV) | **VOID** | Its own ROADMAP Depends-on row says it: *"Phase 8 (the gate must close — if the wafer does not fit, φ_post is not NUCLEUS's φ_post and this phase is void)."* Every anchor is a NUCLEUS-environment object: Figs. 4 and 8–11, Tables 2–5, Table 5 at 100 % duty. Its decisive deliverable (CALC-12, φ_post at the target position) is precisely the quantity §4 shows does not transfer. Its SC3 additionally hinges on a pre-vs-post-veto determination whose transfer condition is *"same veto acceptance — which Phase 8 has already shown we do not have."* |
| **10** — Sub-eV Grid & Trigger Observable (P-GRID) | **SURVIVES** | **Not one NUCLEUS anchor appears in its Anchor-coverage row.** It lists only v1.0 `shared_energy_grid()`, the v1.0 `R(E_rec\|E_dep)` matrices, CONVENTIONS §E/§F (ε ≈ 0.5, 25 kHz non-paralyzable), the per-sensor saturation onsets 1.27 eV (Ta→Al) / 0.77 eV (Al→Hf), and the 24 v1.0/v1.1 anchors. Its deliverables — the 0.1 eV grid at 80 bins/decade, regenerated response matrices, the 0.5 eV trigger sigmoid, the interpolator-raises guard, the counting-statistics floor — are properties of the **wafer and its QPD response chain**, not of the site. Every acceptance criterion (count conservation ≤1e-3, anchors still reproducing, sigmoid 50 % exactly at 0.5 eV, multiplies ε rather than replacing it) is checkable without any NUCLEUS input. |
| **11** — Phonon Conventions & IA Broadening (P-CONV) | **SURVIVES** | Depends on Phase 10 only. Its anchors are NCrystal `Ge_sg227.ncmat` (Nelin & Nilsson), DarkELF `Ge_pDoS.dat`, Sears PRB 35 2038, Campbell-Deem PRD 106 036019, SuperCDMS APL 113 092101, and frozen v1.0 spectra above 10 eV — **no NUCLEUS anchor**. Both deliverables are statements about **germanium**: ω̄ and ⟨u_x²⟩ pinned from the real Ge VDOS with `2W = q²⟨u_x²⟩` locked, and σ_E = √(E_R ω̄) applied before the response chain. Its validity gates (VDOS ceiling 37.79 meV, ⟨u²⟩ agreeing with the Debye value within ~1.5×, <1 % reproduction of frozen v1.0 above ~10 eV) are all internal. Site-independent by inspection of its inputs. |
| **12** — CEvNS at the VNS to 100 meV (P-SIG) | **DOES NOT SURVIVE in its current form** | Stated Depends-on: *"Phase 9 (normalization and duty-cycle lock), Phase 11."* Phase 9 is void, so the normalization leg is unavailable as written. Its anchor row is NUCLEUS Table 5 at 100 % duty (356.5 dru) and the NUCLEUS 2019 Fig. 1 Ge curve. **Honest nuance:** the signal physics is *reactor-site* geometry (2 × 4.25 GW_th at 72 m and 102 m, ∫Φ = 2.1×10¹² ν̄/cm²/s), not *veto* geometry, and the already-passed CaWO₄ closure fold (407.7 vs 356.5, 14 %) is a comparison against a published number rather than an inherited environment. Much of this phase would be recoverable under a re-scope that keeps the Chooz VNS location. It is nevertheless not executable against its ROADMAP contract as written. |
| **13** — Ge Neutron Re-Fold (P-TGT) | **VOID** | Stated Depends-on: *"Phase 9 (φ_post **and** the VALD-11 gate passing), Phase 10, Phase 11."* Its Anchor-coverage row names *"φ_post from Phase 9"* directly, and its SC5 requires that the Ge number derive **only** from φ_post ⊗ Ge kernel with an explicit provenance check. With φ_post void, the phase has no input. The Phase-7 frozen ENDF/B-VIII.0 n-Ge elastic set and T_max/E_n = 0.0536 survive as data, but they are a kernel with nothing to fold. |
| **14** — Ge-Only Capture Channels (P-GEONLY) | **VOID** | Stated Depends-on: *"Phase 13 (the neutron chain and φ_post; the capture channel is the same fluence through a different reaction)."* Its SC4 is explicitly gated on the **in-shield thermal flux φ_th**, a NUCLEUS-shield quantity the ROADMAP already flags as unpublished and unrecoverable by inversion. Its SC5 inherits the B₄C 478 keV line *unvetoed* — a consequence that only has meaning inside NUCLEUS's shield. **Honest nuance:** two sub-deliverables are site-independent as data acquisitions — ENDF MT=102 for the five Ge isotopes plus EGAF capture-γ line lists, and the ⁷¹Ge EC line inventory (M 158.7 ± 1.4 / L 1298.5 / K 10368.3 eV). Those would carry into any re-scope. |
| **15** — Gamma & Muon Re-Fold at the VNS (P-EM) | **DOES NOT SURVIVE in its current form** | Stated Depends-on: *"Phase 9 (Table 2 ambience, Table 4 uncertainties, passive attenuation), Phase 10."* Its SC2 requires reproducing NUCLEUS's stated *"factor ~50"* **passive gamma reduction** through their shield stack — void under a redesign. **Honest nuance, and it matters for the re-scope decision:** its other anchors are **L1 environmental quantities** by this phase's own taxonomy — the 2.92 ± 0.01 m.w.e. overburden, the 1.41 ± 0.02 omnidirectional attenuation, and the measured 5.03 cm⁻²s⁻¹ VNS gamma ambience (taxonomy rows `row-e11`, `row-e12`, `row-e13-*`). Those **do** transfer: they are properties of the rock and the room. The muon leg (CALC-20) is therefore almost entirely recoverable; the gamma leg's *ambience* survives while its *shielded attenuation* does not. |
| **16** — S/B Assembly, LEE, CONUS+ Gate (P-SB) | **VOID** | Terminal; stated Depends-on is *"Phase 12 (signal), Phase 13 (neutrons), Phase 14 (capture channel or its quantified gap), Phase 15 (gammas and muons)."* Three of the four are void or non-surviving, and neutrons are ~91 % of the RoI budget. Its mandatory L2-off baseline is defined by the Phase-8 taxonomy, which **survives** — so the input Phase 16 needs *from this phase* exists; what does not exist is the background budget it would be applied to. The CONUS+ reproduction gate (VALD-12) and the LEE overlay (CALC-21) are themselves site-independent pieces of machinery and would carry forward. |

**Summary:** **2 of 8 downstream phases survive intact** (10, 11). Six do not survive in their
current form, three of them with named recoverable fragments (12, 14, 15).

---

## 6. Surviving deliverables

Named individually, so the re-scope decision is made against what Phase 8 actually produced rather
than against an impression of it.

| Deliverable | Path | Why it survives |
|---|---|---|
| **The binding three-tier rejection taxonomy** — 19 rows (6 L1, 2 L1\*, 11 L2), each with a verbatim quoted sentence, its section, its evidence-block id, its tier, what transfers, a credit of exactly 1.0, a credit basis, and a swap-test justification | `GPD/analysis/VETO-TAXONOMY.md` | A classification of published statements. Correct either way — as its own text says, if the wafer fitted the L2 rejections would still not transfer without a wafer-specific veto acceptance; because it does not fit, they additionally have no envelope to live in. Required by Phase 16 for its mandatory L2-off baseline |
| **The credit constants in code** — `L2_CREDIT = L1STAR_CREDIT = L1_REJECTION_CREDIT = 1.0`, a frozen `TaxonomyRow` that raises on any credit ≠ 1.0, `credit_for()` raising on an uncatalogued statement, plus the two-rule repository guard (demonstrated to fire on three injected violations and stay silent on the real geometry constants) | `src/qpd_potential/veto_credit.py`, `tests/test_veto_credit.py` | Enforcement, not analysis. Independent of the verdict |
| **The wafer's own self-veto acceptance decomposition** — `A_self_direct` (three thresholds), `A_self_induced ≡ 0`, `R_mu`, `f_dead` at two resolving times | `src/qpd_potential/wafer_self_veto.py`, `data/wafer_self_veto.csv` | Derived entirely from the wafer's own frozen chord × Landau–Vavilov deposit distribution. Depends on no NUCLEUS geometry |
| **The multiplicity identity** `ε_mult(1) ≡ 0`, unit-tested under exact identity comparison and shown model-independent | same module; consumed by `veto_credit.multiplicity_rejection_is_zero()` | A counting identity about a single-readout target |
| **The frozen, integrity-checked source cache** — four NUCLEUS primary sources plus Figure 1 as raw HTML *and* probe-validated normalized text, with per-artifact curl command, UTC timestamp, byte size, SHA-256 and integrity verdict; plus the recorded failed Goupy acquisition | `data/external/nucleus/`, `MANIFEST.md`, `html_to_text.py` | An evidentiary asset usable by any future scope that cites NUCLEUS at all |
| **The verbatim evidence block** — 34 quotes / 52 grep commands, all re-running and exiting 0; the three separated factor-5 statements; four mass closures with ρ sensitivity; the Fig. 1 inspection record; the cross-version verdict table | `08-01-SOURCE-EVIDENCE.md` | Same |
| **The Phase-9 trace-selection handoff** — the Fig. 8 caption evidence that the left panels are passive-only and the right panels are the veto detectors, with the instruction to digitize the passive-only trace because reading a post-veto curve as pre-veto would import an L2 credit through the digitization | `GPD/literature/PITFALLS.md` (dated Phase-8 correction) | Applies to any future digitization of that figure, under any scope |
| **The geometry module with its sourced constants** — the four comparison bases, the true SO(3) orientation minima, the separately named tight and loose cavity constants, the basis-raising `area_ratio()` | `src/qpd_potential/veto_envelope.py`, `tests/test_veto_envelope.py` (21 tests) | The determination machinery itself, reusable against any other envelope |
| **The PITFALLS corrections** — every factor-5 occurrence labelled `[F5-a]`/`[F5-b]`/`[F5-c]` by which of the three §5.2.1 statements it is; the array footprint basis-labelled with the published 2.25 cm² value and its two mass closures; every area ratio carrying a basis label | `GPD/literature/PITFALLS.md` | Corrections to project-level errors, independent of the verdict |

Full repository test suite at the close of Phase 8: **310 passed**.

---

## 7. The two prohibitions, asserted explicitly

Both are attributed to the **locked user decision of 2026-07-22**, recorded in `GPD/ROADMAP.md`
Phase 8 forbidden proxies, the Risk Register, and the Backtracking Triggers, and in
`GPD/REQUIREMENTS.md` VALD-09.

> **1. No reduced veto credit is assumed.** Past a failed gate, no partial veto credit, no
> best-guess surviving rejection, and no "for reference" rejection value appears in any Phase-8
> output (`fp-reduced-credit`). A number placed in this artifact for reference would be reused as
> though it were established, and no derivation exists behind any partial value.
>
> **2. No resized veto is invented.** No modified, resized, scaled-up, sketched or costed veto
> geometry is proposed or evaluated anywhere, including as an illustration of what would be
> required (`fp-resized-veto`). The 14.3684 cm figure that appears in the overturning conditions is
> a **threshold for overturning the verdict**, not a proposed geometry.

**The transferable credit remains exactly 1.0** — and **this would remain true on a fit verdict
too.** A fit alone does not earn credit: it would still require a *derived wafer-specific veto
acceptance*, which this phase does not attempt and which no Phase-8 plan is scoped to produce.
Inherited veto credit defaults to zero unless earned by wafer geometry (VALD-09, locked user
decision 2026-07-22).

**Sweep result (acceptance test `test-no-credit-no-redesign`, automated).** Every Phase-8 output was
swept — this verdict, `08-03-FIT-DETERMINATION.md`, `VETO-TAXONOMY.md`, `08-01-SOURCE-EVIDENCE.md`,
and all three source modules (`veto_envelope.py`, `wafer_self_veto.py`, `veto_credit.py`):

- All 19 taxonomy credit cells read exactly `1.0`; no other value appears in that column.
- `L2_CREDIT = 1.0`, `L1STAR_CREDIT = 1.0`, `L1_REJECTION_CREDIT = 1.0` in code; no module-level
  constant matching `*CREDIT*` / `*REJECTION*` / `*VETO_FACTOR*` holds any other value.
- The only textual occurrence of `99.8` anywhere in the modules is inside the verbatim B.9
  quotation in the `A_SELF_INDUCED` docstring, explicitly labelled **not applied**; a
  tokenize-based test confirms it is never a NUMBER token, i.e. never evaluated as a value.
- Resized/scaled-veto vocabulary ("resized", "scaled-up", "enlarged", "hypothetical geometry")
  occurs in exactly two places across all Phase-8 outputs, and both are **the prohibition being
  stated**: `08-03-FIT-DETERMINATION.md` §10's `fp-resized-veto` scope statement, and §7 of this
  document. No candidate dimension for a modified veto is proposed anywhere.

**Known blind spot, stated so the guard is not mistaken for a proof:** an anonymous inline literal —
`rate / 5` inside a function body — is invisible to both guard rules, because no decidable rule can
separate it from a legitimate arithmetic constant without false-positiving on
`COV_CRYSTAL_THICKNESS_CM = 2.5`, `B4C_THICKNESS_CM = 4.0` or the wafer's `LZ = 0.20`. The guard
raises the cost of reintroducing a veto credit and makes the reviewable-diff path the path of least
resistance; it is not a proof that no rejection factor can enter.

---

## 8. Return of control to the user

### 8.1 The decision brief

**The verdict, in one sentence.** A 10.16 × 10.16 × 0.20 cm, 110 g Ge wafer mounted face-parallel
requires a COV cap crystal of 14.3684 cm diameter to be covered; the published cap is 10.0 cm
(arXiv:2508.02488v1 §2, corroborated by arXiv:1905.10258 Fig. 8); the clearance is **−4.3684 cm**,
sign-robust across every published rounding interval — **NO FIT**.

**Its single most important limitation.** That clearance is **conditional on the face-parallel
mounting premise**. What geometry alone delivers, with no mounting assumption, is **−0.1620 cm**,
and *that* number is **not** sign-robust: under the 2019 paper's published 1-significant-figure
"a diameter of 10 cm" it spans zero. A published statement that the wafer would be mounted
otherwise would make the determination **inconclusive**, not a fit — but inconclusive is not no-fit.
(Secondary limitation: the load-bearing 10.0 cm comes from a **TUM commissioning paper outside the
ROADMAP anchor list**, and the only genuinely independent route — the Goupy thesis — was never
obtained.)

**Surviving deliverables.** The three-tier taxonomy and its 1.0 credit constants in code; the
wafer's own self-veto decomposition and the multiplicity identity; the frozen integrity-checked
source cache and the 34-quote evidence block; the Phase-9 trace-selection handoff; the geometry
module with its sourced constants; the PITFALLS corrections. (Detail: §6.)

**Disposition summary.** Phases **10** and **11** are physically site-independent and **survive
intact** — they depend on the germanium vibrational density of states, the shared energy grid and
the QPD response chain, and carry **no NUCLEUS anchor in their ROADMAP contract rows**. Phases
**9, 12, 13, 14, 15, 16** are premised on the environment transfer and **do not survive in their
current form**, with recoverable fragments named in §5 (notably: Phase 15's L1 environmental inputs
— the 2.92 m.w.e. overburden, the 1.41 attenuation and the measured 5.03 cm⁻²s⁻¹ VNS gamma
ambience — **do** transfer, because they are properties of the site rather than of the payload).

### 8.2 Candidate re-scope directions — for the user to choose among

**None of these is adopted. None is recommended. Phase 8's authority ends at determining fit and
reporting disposition; the choice is the user's.**

| # | Direction | What it retains | What it costs |
|---|---|---|---|
| **1** | **Adopt room-level environmental inputs only** — the 2.92 ± 0.01 m.w.e. overburden, the 1.41 ± 0.02 attenuation, the Table 4 surface flux normalizations, the measured 5.03 cm⁻²s⁻¹ VNS gamma ambience — and **design an independent shield** for the wafer | The site and its **measured** environment. These are exactly the L1 rows of the surviving taxonomy, so the classification work already done supports it directly. Phases 10, 11 carry over unchanged; Phase 15's muon leg is nearly intact | **Shield design work the milestone never scoped.** φ_post would have to be produced by our own shield model rather than by inverting NUCLEUS's deposit spectra, and the rejected transport options (OpenMC unbuildable on osx-arm64; full Geant4 out of scope by user decision) are exactly the tools that would normally do it. SIMU-05 (hand-rolled 1-D multigroup) is currently *follow-up* scope |
| **2** | **Revisit the wafer format** | Would potentially restore the entire v2.0 premise as written | **`GPD/REQUIREMENTS.md` explicitly places this out of scope.** Its Out-of-Scope table reads: *"Detector geometry / sensor-layout optimization — Fixed 4″×4″×2 mm single-sided wafer from v1.0 — and note **VALD-09 may show this geometry is incompatible with the adopted veto envelope, which is a stop-condition, not an optimization trigger**."* Surfacing this option is **not** the same as recommending it; it is listed because a complete option set is what the decision requires, and choosing it would require the user to reverse a recorded scoping decision |
| **3** | **Retarget to a different host experiment** whose envelope accommodates a 10.16 cm plate | Keeps the wafer geometry fixed and keeps the "adopt a measured environment" methodology, which is the milestone's real intellectual content | A new host means a new environment, new anchors, and a new literature survey. Every NUCLEUS-derived anchor in Phases 9 and 12–16 would be replaced. The Phase-8 machinery (`veto_envelope.py`, the taxonomy's tier definitions and swap test) is reusable against another envelope, but the numbers are not |
| **4** | **Obtain the Goupy 2024 thesis first**, before deciding anything | **The only route that could overturn the verdict.** What it would resolve: the **rectangular COV crystal dimensions** and the **copper support geometry** — converting the internal cavity from *bounded* (currently a tight estimate of ~5 cm and a loose bound of 16.7 cm that differ by more than a factor of three, only one of which excludes the wafer) into a *read* dimension. It is also the only genuinely independent third source on the envelope | Requires a **manual browser download by the user**: NNT 2024UNIP7170 / HAL tel-05298505, unobtainable by any scripted route (live anti-bot challenge recorded in `MANIFEST.md` §4). **Realistic expectation, stated so the option is not oversold:** even a cavity of ≥10.16 cm in two axes would overturn only the two *cavity* clearances. To touch the verdict it would additionally have to show **larger cap crystals** — at least 14.3684 cm, more than 43 % larger than the published 100 mm, implying ~2.06 kg against the published 1 kg |

### 8.3 Halt

**This phase does not choose among these directions, and no work proceeds until the user decides.**

- No Phase 9 work has been started. No environment transcription, no digitization, no `mcpd_to_dru`,
  no inversion, no φ_post.
- No downstream artifact has been created.
- No direction has been adopted, and the verdict has not been softened to make any direction look
  easier.

**Awaiting the user's re-scope decision.**

---

_Phase 8 (Veto-Envelope Geometry Gate, P-VETO), Plan 08-05. Discharges ROADMAP Phase 8 Success
Criterion 5 and closes requirement VALD-09. Assembled from Plans 08-01 through 08-04; no quantity
computed here._
