# Phase 8 — Fit Determination (Success Criterion 1)

**Deliverable:** `deliv-fit-determination`
**Plan:** 08-03 · **Produced:** 2026-07-22
**Question:** Does a 10.16 × 10.16 × 0.20 cm, 110 g Ge wafer fit inside the NUCLEUS
cryogenic-outer-veto internal envelope, and on what published dimension, with what bound and
what uncertainty, does that determination rest?

**Computation:** `src/qpd_potential/veto_envelope.py`, exercised by
`tests/test_veto_envelope.py` (21 tests, all passing; full repository suite 242 passed).
Every clearance in this document was computed by `veto_envelope.clearance()` and
`veto_envelope.clearance_sign_robust()`. None was transcribed from an expectation.

**Sign convention:** clearance `C = D_available − W_required` in cm; `C < 0` is a shortfall of
`|C|`.

---

## 0. Verdict, in one paragraph

**NO FIT.** With the wafer face mounted parallel to the cryogenic-outer-veto (COV) cap plane, a
circular cap crystal must have a diameter of **√2 × 10.16 = 14.3684 cm** to cover the wafer's
projected footprint. The published COV cap-crystal outer diameter is **10.0 cm**
(arXiv:2508.02488v1 §2, "100 mm diameter"; independently corroborated by arXiv:1905.10258 Fig. 8,
"a diameter of 10 cm"). The clearance is **−4.3684 cm**: the cap is **30.4 % smaller than
required**, equivalently the requirement is **43.7 % larger than the published cap**. This
clearance keeps its sign across every rounding interval the published dimensions can support — it
would change sign only at a cap diameter of 14.37 cm, a rounding half-width of 4.37 cm.

**Two qualifications are part of the verdict, not footnotes to it.**

1. The −4.3684 cm figure is robust to *dimension rounding* but is **conditional on mounting**. The
   orientation-invariant coverage requirement — the one that holds with no mounting assumption at
   all — is the edge-on projection floor √(a²+t²) = 10.1620 cm, which against 10.0 cm gives only
   **−0.1620 cm**, and that clearance is **not sign-robust**.
2. **Neither leg of the argument is simultaneously premise-free and sign-robust.** The coverage
   leg is sign-robust but needs a coverage premise and a mounting premise. The edge leg needs no
   premise at all but is not sign-robust. This is stated here in these terms so that no downstream
   artifact can present −4.37 cm as a purely geometric result.

No clearance on any of the four named bases came out positive. The one positive clearance
anywhere in this determination is the **loose** cavity bound (§5), which is an explicitly
non-excluding upper bound and is not a verdict basis.

---

## 1. Evidence-route amendment — this is an amendment, not the criterion's original route

ROADMAP Phase 8 **Success Criterion 1** names *EPJC 86, 29 (2026) Fig. 1(e)/(f)* as the evidence
route for the veto-envelope dimensions.

**That route is dimensionally silent, and the criterion as literally written cannot be discharged
from it.** Plan 08-01 established this by direct inspection of the frozen image, not by inference.
Quoting `08-01-SOURCE-EVIDENCE.md` §F.6 verbatim:

> **Determination.** EPJC 86, 29 (2026) (arXiv:2509.03559v1) Figure 1 carries **no scale bar, no
> ruler, no dimension leader, and no numeric dimension callout on any of panels (a)–(f)**. It is an
> unannotated rendered schematic, self-described in its own caption as a "Simplified schematic
> view". The complete set of numerals appearing anywhere on the figure is the six panel letters
> (a)–(f), the reactor labels B1 and B2, and the array multiplicity "3 × 3" on panel (f) — no
> length, no unit, no scale reference. This was established by direct inspection of the frozen
> 1875 × 2613 px image at full resolution across all six panels.

and §F.8 verbatim:

> **Determination.** arXiv:2509.03559v1 (EPJC 86, 29 (2026)) states **no internal envelope, cavity,
> or clearance dimension for the cryogenic outer veto or the inner veto, anywhere in the document**.
> The only COV dimension it gives is a **2.5 cm crystal thickness** (A.10, B.8). The words
> "envelope", "cavity", "inner diameter" and "clearance" do not occur in the text at all. This was
> established by exhaustive enumeration of every `cm`/`mm` numeric token in the frozen file, not by
> a targeted search.

Both findings hold in **both** the arXiv v1 and the published journal version: 08-01 §F.8 records
that the same enumeration run against the retrieved open-access EPJC HTML returns the same token
set and the same zero counts. Plan 08-01 also verified that the four load-bearing L2 statements
agree word-for-word between the two versions (§E.2).

### 1.1 The substituted route

| Dimension | Value | Substituted source |
|---|---|---|
| COV cap-crystal outer diameter | **100 mm = 10.0 cm** | arXiv:2508.02488v1 §2 "Cryogenic Outer Veto" (08-01 A.1) |
| COV crystal thickness | **25 mm = 2.5 cm** | arXiv:2508.02488v1 §2 (A.1); *independently* arXiv:2509.03559v1 §2 "2.5 cm thick HPGe crystals" (A.10) |
| Internal shielding cylinder | **297 mm = 29.7 cm** | arXiv:2508.02488v1 §2 "Passive shielding" (08-01 A.2) |
| Cryostat bore | **430 mm = 43.0 cm** | arXiv:2508.02488v1 §2 "Passive shielding" (08-01 A.3) |
| Outer-veto diameter, independent corroboration | **10 cm** | arXiv:1905.10258 (EPJC 79, 1018 (2019)) Fig. 8 caption (08-01 A.13) |
| B₄C layer thickness | **4 cm** | arXiv:2509.03559v1 §2 (08-01 A.9) |

**Justification for the substitution.** The criterion's purpose is to determine fit against
*published NUCLEUS geometry*. Its named source contains exactly one COV dimension — a thickness —
and no envelope at all. Substituting sources that do carry the needed dimensions preserves the
criterion's purpose; quoting a callout the named figure does not carry would not. This is
`fp-fig1e-quoted-clearance`, and it is avoided: **no dimension entering any clearance, any bound,
or the verdict is attributed to Fig. 1(e) or Fig. 1(f).** The only use made of Fig. 1(e) is a
*relative* pixel measurement scaled against externally published anchors (§7), which is
corroborative, is labelled as such, and carries no verdict weight. The envelope estimate reported
in §7 enters no clearance in §3, §4, §5 or §6.

### 1.2 Anchor promotion, stated rather than smoothed over

**arXiv:2508.02488 is NOT in the `GPD/ROADMAP.md` Phase-8 anchor list.** It is promoted to a
Phase-8 anchor, with 08-01 §D as the written record of that promotion and this section as its
carry-forward. Two facts about it must travel with every number taken from it:

1. **It describes the TUM commissioning setup, not Chooz.** In that setup, per A.1, "only one of
   the six crystals is installed directly above the target detectors." It is not a Chooz
   engineering drawing.
2. **It is the single load-bearing geometric source of this phase.** The 10.0 cm cap diameter,
   the 29.7 cm internal shielding and the 43.0 cm bore all come from it.

**What licenses the 100 mm read.** Plan 08-01 §C.1 computed the mass closure
ρ_Ge · π · (5.0 cm)² · (2.5 cm) = **1045.17 g** at ρ_Ge = 5.323 g/cm³, against the paper's
independently published **"a mass of 1 kg"**. A dimension read that reproduces an independently
published mass is not a mis-read.

> **Carry the V1 precision caveat exactly as 08-01 wrote it.** This closure is reported as
> **consistent with a 1-significant-figure "1 kg"**, with ρ_Ge named. It is **not** to be reported
> as "within 5 %": the margin against a naive ±5 % band is only **4.8 g**, and at ρ_Ge = 5.35 the
> computed mass is 1050.5 g and the naive band **fails**.

**Corroboration, and its limit (V10).** The 2019 paper's independent "a diameter of 10 cm"
(A.13) and the 2026 paper's independent "2.5 cm thick" (A.10) are genuine cross-checks from
different papers. But the Fig. 1(e) pixel measurement of §7 is **not** a third independent route —
it takes its scale from the same published numbers. A genuinely independent third route requires
the Goupy 2024 thesis, which is unobtainable by any scripted route (MANIFEST.md §4).

> **Trap, flagged so a later reader does not fall into it.** The strings `10.16 cm` and `1.27 cm`
> **do** appear in arXiv:2509.03559v1 — in §4.2.1, as **Bonner-sphere Pb shell converter**
> dimensions ("an outer diameter of 10.16 cm and a thickness of 1.27 cm"), alongside the 20.32 cm
> and 22.86 cm sphere diameters. The coincidence with the QPD wafer's 10.16 cm edge is
> **accidental and unrelated to the veto envelope**. Neither may be cited as a veto dimension.

---

## 2. The requirement, and what reorientation does and does not buy

Wafer: a = 10.16 cm in-plane edge, t = 0.20 cm thickness (`GPD/CONVENTIONS.md` §D, imported into
the module from `src/qpd_potential/wafer_geometry.py`, never restated). Closure re-verified in
test: 10.16 × 10.16 × 0.20 × 5.323 = **109.9 g**, face area **103.23 cm²**.

### 2.1 Reorientation DOES relax the bounding-box requirement — retraction of 08-RESEARCH §F1

`08-RESEARCH.md` §F1 asserted `min_{R∈SO(3)} b₂(R) = a`, i.e. that no orientation reduces the
requirement that the cavity have two orthogonal free dimensions of at least 10.16 cm.

**That lemma is FALSE and is retracted.** A 45° tilt about an in-plane axis leaves the first
extent at a and compresses both remaining extents to (a cos 45° + t sin 45°) = (a+t)/√2, giving a
bounding box of **10.160 × 7.326 × 7.326 cm**. The second-largest side is 7.33 cm, not 10.16 cm.
`08-RESEARCH.md` carries a dated correction at §F1 and at Pitfall 7; Pitfall 7 ("Could we reorient
it?") is therefore **not** discharged by lemma F1.

| Quantity | Closed form | Value | Attained at | Sampled minimum (2 × 10⁵ uniform SO(3), seed 20260722) |
|---|---|---|---|---|
| min b₂ (2nd-largest bbox side) | (a+t)/√2 | **7.3256 cm** | 45° tilt about an in-plane axis | 7.3945 |
| min b₁ (largest bbox side) | a/(3√2/4) — **zero-thickness Prince-Rupert bound** | **9.5789 cm** | *not* attained at t = 0.20 cm | 9.7076 |
| min projected-footprint diameter | √(a²+t²) | **10.1620 cm** | edge-on | 10.1623 |
| projected diameter, face-parallel | √2·a | **14.3684 cm** | face parallel to cap plane | — (exact check) |
| space diagonal (enclosing **sphere**) | √(2a²+t²) | **14.3698 cm** | — | — (matches `wafer_geometry.CHORD_DIAGONAL`) |

**Labelling that matters.** `a/(3√2/4) = 9.5789 cm` is the **t → 0 Prince-Rupert lower bound**, not
the attained minimum for the physical t = 0.20 cm plate. Sampling reaches only ≈ 9.71–9.72 cm, so
the true minimum lies in [9.5789, ≲ 9.72] cm. **The defensible statement is that the wafer fits
inside a cube of side ≲ 9.72 cm — not 9.58 cm.** This quantity enters no clearance and no
assertion; it is recorded only to state honestly how much reorientation buys.

**Sampling discipline.** Uniform SO(3) sampling approaches an attained infimum *from above* and
never reaches it, so `tests/test_veto_envelope.py` asserts **one-sided lower bounds**
(`min b₂ ≥ 7.3256 − 10⁻³` cm, `min proj Ø ≥ 10.1620 − 10⁻³` cm) plus **exact** evaluations at the
45° tilt and edge-on orientations. No equality-against-a-sampled-value assertion appears anywhere.
The retracted assertion `min(b₂) ≥ 10.16 − 10⁻⁶` appears nowhere; it would fail deterministically.

**Retired misnomer.** `√(2a²+t²) = 14.3698 cm` was labelled "wafer min-enclosing-cylinder
diameter" in `08-RESEARCH.md`. It is the enclosing-**sphere** diameter. The true minimum enclosing
**cylinder** (axis normal to the face) has the **face**-diagonal diameter 14.3684 cm. The two
differ by 0.0014 cm — which is how the misnomer survived unnoticed. The function is renamed
`space_diagonal()` and its docstring forbids its use as a coverage requirement; it is retained only
because it is independently unit-tested against `wafer_geometry.CHORD_DIAGONAL`.

**What survives orientation** is the *projection floor*: min over SO(3) of the projected-footprint
diameter is √(a²+t²) = 10.1620 cm, attained edge-on, rising continuously to √2·a = 14.3684 cm when
the face is parallel to the cap plane.

### 2.2 The face-parallel mounting premise

The verdict quantity 14.3684 cm assumes the **wafer face lies parallel to the COV cap plane**, as
in every planar cryogenic detector stack and as implied by the wafer's single instrumented face
(~10,300 sensors at 1/mm² on one face, CONVENTIONS §D). This premise is stated at every point in
this document where −4.37 cm appears. It is an assumption, and it is listed as such in §9.

---

## 3. The four clearances

Every row computed by `veto_envelope.comparison_bases()` and `clearance_sign_robust()`. Rows are
ordered by **premise strength**: weakest premise first.

| # | Basis | W_required (cm) | D_available (cm) | Source of D (arXiv + section) | Stated precision interval on D | **C (cm)** | Premise | Sign-robust? |
|---|---|---|---|---|---|---|---|---|
| 2 | **EDGE** — wafer in-plane edge vs published cap outer diameter | 10.1600 (= a) | 10.0 | arXiv:2508.02488v1 §2 "Cryogenic Outer Veto" (08-01 A.1); corroborated arXiv:1905.10258 Fig. 8 (A.13) | ±0.05 cm ("100 mm", 2 s.f.); ±0.5 cm ("10 cm", 1 s.f.) | **−0.1600** | **None.** The wafer is wider than an entire cap crystal. | **NO** — flips at D = 10.16 cm (half-width 0.16 cm), inside the 1-s.f. interval |
| 1 | **COVERAGE** — required cap diameter vs published cap outer diameter | 14.3684 (= √2·a) | 10.0 | as row 2 | as row 2 | **−4.3684** | Cap must **cover** the wafer footprint (COV "hermetically covers the cryogenic target detectors", 08-01 A.11) **and** face-parallel mounting | **YES** to rounding (flips only at D = 14.37 cm, half-width 4.37 cm); **NO** to orientation — see row 1b |
| 1b | **COVERAGE, orientation-invariant floor** — edge-on projection requirement vs same D | 10.1620 (= √(a²+t²)) | 10.0 | as row 2 | as row 2 | **−0.1620** | Cap must cover the footprint. **No mounting premise.** | **NO** — flips at D = 10.162 cm (half-width 0.162 cm) |
| 3 | **CAVITY, in-plane** — wafer edge vs *estimated* tight COV cavity | 10.1600 | 5.0 | DERIVED: 10.0 − 2 × 2.5, from A.1 and A.10 | ±0.15 cm (propagated) | **−5.1600** *(estimate)* | Rectangular 2.5 cm slabs sit inside the cap rim | YES to rounding, but the **premise** is unverified |
| 4 | **CAVITY, diagonal** — required cap diameter vs same estimated cavity | 14.3684 | 5.0 | as row 3 | ±0.15 cm | **−9.3684** *(estimate)* | As row 3, plus face-parallel mounting | YES to rounding, but the **premise** is unverified |

**Coverage ratio (row 1):** 10.0 / 14.3684 = **0.6960** — the cap is **30.4 %** smaller than
required. Equivalently 14.3684 / 10.0 = 1.4368: the requirement is **43.7 %** larger than the
published cap.

---

## 4. Precision intervals and sign robustness — computed at the interval endpoints

Published dimensions entering a clearance and their stated rounding intervals:

| Published value | As printed | s.f. | Rounding half-width |
|---|---|---|---|
| COV cap outer diameter | "100 mm diameter" (2508.02488v1 §2) | 2 | **±0.05 cm** |
| COV cap outer diameter | "an outer veto (3) with a diameter of 10 cm" (1905.10258 Fig. 8) | 1 | **±0.5 cm** |
| COV crystal thickness | "25 mm height" / "2.5 cm thick" | 2 | ±0.05 cm |
| Internal shielding diameter | "a diameter of 297 mm" | 3 | ±0.05 cm |
| B₄C layer thickness | "4-cm thick" | 1 | ±0.5 cm |

Each clearance re-evaluated at both endpoints of `D ± half-width`. **`Y` = sign preserved,
`N` = sign lost.**

| Basis | C nominal | ±0.05 cm | ±0.10 cm | ±0.50 cm | Half-width at which the sign flips |
|---|---|---|---|---|---|
| 1 COVERAGE (face-parallel) | −4.3684 | [−4.418, −4.318] **Y** | [−4.468, −4.268] **Y** | [−4.868, −3.868] **Y** | **4.3684 cm** (D = 14.3684) |
| 1b COVERAGE (orientation-invariant floor) | −0.1620 | [−0.212, −0.112] **Y** | [−0.262, −0.062] **Y** | [−0.662, **+0.338**] **N** | **0.1620 cm** (D = 10.1620) |
| 2 EDGE | −0.1600 | [−0.210, −0.110] **Y** | [−0.260, −0.060] **Y** | [−0.660, **+0.340**] **N** | **0.1600 cm** (D = 10.1600) |
| 3 CAVITY in-plane *(estimate)* | −5.1600 | [−5.210, −5.110] **Y** | [−5.260, −5.060] **Y** | [−5.660, −4.660] **Y** | 5.1600 cm |
| 4 CAVITY diagonal *(estimate)* | −9.3684 | [−9.418, −9.318] **Y** | [−9.468, −9.268] **Y** | [−9.868, −8.868] **Y** | 9.3684 cm |

### 4.1 Two corrections to expected values, computed rather than transcribed

The plan and its review notes anticipated that the EDGE clearance would be "not sign-robust at the
±0.1 cm reading, since a cap diameter of 10.2 cm would make it +0.04 cm". **The arithmetic does not
support the mapping.** Computed:

- At **±0.1 cm** the interval on D is [9.9, 10.1] and the clearance interval is [−0.26, −0.06]. The
  sign **is** preserved. It is preserved by only **0.06 cm**, which is *less than the half-width
  itself* — the clearance is smaller than its own input precision — but it does not flip.
- The clearance flips at **D = 10.16 cm exactly**, i.e. at a half-width of **0.16 cm**. A cap of
  10.2 cm does give **+0.04 cm** (verified), but 10.2 cm is not an endpoint of ±0.1 around 10.0.
- The reading that genuinely breaks the sign is the **1-significant-figure** interval implied by
  the 2019 paper's "a diameter of 10 cm": half-width **±0.5 cm**, giving [−0.66, **+0.34**].

This correction *strengthens* rather than weakens the conclusion that the edge basis must not carry
the verdict: it names an explicit, published reading of the source (1 s.f.) under which the
clearance is positive. The corrected threshold — flip at D = 10.16 cm — is the number to quote.
The same correction applies to row 1b with threshold D = 10.1620 cm.

### 4.2 The orientation axis of robustness, separately

Sign-robustness against wafer **orientation** is a different axis from rounding, and the coverage
basis behaves differently on the two:

| Coverage requirement | Value | C against D = 10.0 | Robust to rounding? | Requires a mounting premise? |
|---|---|---|---|---|
| Face-parallel, √2·a | 14.3684 cm | **−4.3684** | **Yes**, by 4.37 cm | **Yes** — face parallel to the cap plane |
| Orientation-invariant floor, √(a²+t²) | 10.1620 cm | **−0.1620** | **No** — flips at half-width 0.162 cm | **No** |

**Therefore: the coverage basis's robustness comes from the mounting premise, not from geometry
alone.** Stated plainly so it cannot be lost downstream: **−4.37 cm is not a purely geometric
result.** What geometry alone delivers is −0.16 cm, and that is not sign-robust.

---

## 5. Tight versus loose cavity bounds — reported separately, never merged

**Tight bound** (`COV_CAVITY_TIGHT_CM`):

```
D_cavity  <~  D_cyl − 2 t_rect  =  10.0 − 2(2.5)  =  5.0 cm
```

Assumption: the four rectangular 2.5 cm slabs sit **inside** the rim of the 10 cm cylindrical caps.
This could fail if the rectangular crystals are larger than the caps — plausible for hermetic
coverage of a stacked two-module payload — in which case the cavity could exceed 5 cm and rows 3
and 4 of §3 would be wrong.

**Loose bound** (`COV_CAVITY_LOOSE_CM`):

```
D_cavity  <=  D_int.shield − 2 t_B4C − 2 t_rect  =  29.7 − 8.0 − 5.0  =  16.7 cm
```

**The loose bound does NOT exclude the wafer.** Against the 14.3684 cm coverage requirement it
gives a clearance of **+2.3316 cm** — positive, i.e. headroom. This positive number is reported
rather than suppressed: it is what makes the loose route insufficient as a verdict basis, and it is
why the verdict is routed through the coverage comparison against the published cap outer diameter,
which needs **no cavity assumption at all**.

The two bounds differ by more than a factor of three and only one of them excludes the wafer.
`veto_envelope.py` carries them as two separately named constants; a test asserts that no merged
cavity constant exists (`fp-merged-cavity-number`). **Both cavity-based clearances (−5.16 cm and
−9.37 cm) are estimates, and the verdict rests on neither.**

---

## 6. The verdict, its mounting-conditionality, and the tilt path

### 6.1 The verdict

**With the wafer face mounted parallel to the COV cap plane, a COV cap crystal of 10.0 cm published
outer diameter cannot cover a wafer whose footprint requires a circle of 14.3684 cm. The clearance
is −4.3684 cm: the cap is about 30 % smaller than required.**

This survives the stated precision interval on the published diameter by a wide margin. At the
±0.05 cm endpoint the shortfall is −4.32 cm; at ±0.1 cm it is −4.27 cm; at the wide 1-s.f. ±0.5 cm
endpoint it is still −3.87 cm. At a cap diameter of 10.2 cm the shortfall is −4.17 cm. Overturning
it requires a published Chooz cap of **at least 14.37 cm**, i.e. **more than 43 % larger** than the
published 100 mm.

### 6.2 Mounting-conditionality, stated in the same place

The −4.3684 cm figure is robust to **dimension rounding** and conditional on **mounting**. The
orientation-invariant requirement is the edge-on projection floor of 10.1620 cm, giving a clearance
of only **−0.1620 cm**, which is **not** sign-robust (it flips at a cap diameter of 10.162 cm, and
the 1-s.f. reading of the published "10 cm" spans that). A reader must not come away believing
−4.37 cm is a purely geometric result.

### 6.3 The tilt path, closed explicitly

Reorientation is not impossible — it genuinely helps, and it still does not suffice:

- A 45° in-plane tilt reduces the bounding box to **10.160 × 7.326 × 7.326 cm**, and the wafer fits
  inside a cube of side ≲ 9.72 cm.
- That box still **exceeds every cavity bound available**: its largest side 10.160 cm exceeds the
  5.0 cm tight cavity estimate by 5.16 cm; and while the 16.7 cm loose bound would accommodate it,
  the loose bound does not exclude the untilted wafer either, so it discriminates nothing.
- The cap still cannot cover the tilted footprint: at **any** orientation the projected footprint
  diameter is at least √(a²+t²) = 10.1620 cm > 10.0 cm.

**So reorientation helps and still does not rescue the fit, and the no-fit direction is unchanged.**
That is the honest statement — not that reorientation is impossible.

### 6.4 The premise-free minimal statement, with its fragility stated

The most compact statement of the result that needs **no premise of any kind** is:
**the wafer's 10.16 cm edge is wider than the entire 10.0 cm cap crystal.** Clearance −0.1600 cm.

**It is retained as corroboration and is NOT the verdict basis**, because its margin is smaller
than its own input precision: it flips sign at a cap diameter of 10.16 cm, and the 1-significant-
figure published reading "a diameter of 10 cm" spans that value. Staking a milestone-gating
stop-condition on a 0.16 cm margin drawn from a 1-to-2-significant-figure source would be
`fp-unstated-precision`.

The two cavity comparisons (−5.16 cm, −9.37 cm) are **estimates** dependent on the cap-rim
assumption and are labelled as such wherever they appear.

**This document deliberately does not fall back on a vague direction-versus-magnitude formula.**
It states per basis, in §4, which clearances keep their sign across their stated intervals and
which do not, and the verdict rests only on the ones that do.

---

## 7. Figure 1(e) pixel measurement — corroborative only, and NOT independent

**Method.** File `data/external/nucleus/2509.03559v1_Figure1.png`, SHA-256
`bddf5c998b9f54b10a9ff1fbbe6e372c7ea2d579effabcaad6f861c4535c34da`, 1875 × 2613 px, RGB, PNG,
149.987 DPI, Pillow 10.2.0. Panel (e) "Cryostat volume" occupies the crop (0, 1680)–(960, 2613).
All coordinates below are **full-image** pixel coordinates. Edges were located by printing raw RGB
values across the transition and taking the midpoint of the antialiasing ramp; the pink callout box
was located programmatically by colour mask (r > 200, g < 110, 110 < b < 190).

| Measured distance | Pixel coordinate pair | Extent |
|---|---|---|
| COV germanium element, widest unoccluded rows (y = 2320 and y = 2345) | x = 269.5 → 377.5 | **108.0 px** |
| COV cylindrical cap disc (top), y = 2292–2302 | x = 279.5 → 375.5 | **96.0 px** |
| Internal shielding cylinder silhouette, y = 2060–2140 | x = 177.5 → 478.5 | **301.0 px** |
| "Inner detector modules" pink callout box, outer stroke | x = 303.5 → 355.5, y = 2308.5 → 2354.5 | **52.0 × 46.0 px** |
| "Inner detector modules" pink callout box, inner stroke | x = 307.5 → 351.5, y = 2312.5 → 2350.5 | **44.0 × 38.0 px** |

**Derived scales.**

| Anchor | Published size | Measured | Scale |
|---|---|---|---|
| A — COV germanium element = 100 mm | 10.0 cm | 108.0 px | **0.09259 cm/px** |
| A′ — COV cylindrical cap disc = 100 mm | 10.0 cm | 96.0 px | **0.10417 cm/px** |
| B — internal shielding = 297 mm | 29.7 cm | 301.0 px | **0.09867 cm/px** |

**Two-anchor comparison (the ~30 % criterion).** B/A = **+6.6 %**, B/A′ = **−5.3 %**. Both are far
inside ~30 %, so the two anchors are reported as **consistent**: this panel of the schematic is
drawn approximately to scale. Nothing is averaged away and neither anchor is silently preferred —
the spread between A and A′ (11 %, cap disc versus mid-plane element, a perspective/geometry
ambiguity in the render) is itself part of the uncertainty and is quoted.

**Resulting inner-detector-modules envelope estimate.**

| Anchor | Inner box | Outer box |
|---|---|---|
| A | 4.07 × 3.52 cm | 4.81 × 4.26 cm |
| A′ | 4.58 × 3.96 cm | 5.42 × 4.79 cm |
| B | 4.34 × 3.75 cm | 5.13 × 4.54 cm |

**Uncertainty and how it was estimated.** Edge-identification ambiguity was taken as **±2 px** on
each measured distance (the antialiasing ramp is 1–2 px wide, and the choice of which side of the
ramp to call the edge moves the result by about that much). Propagated in quadrature this is
**±4.6 to ±4.9 %**, i.e. ±0.20 cm on the inner-box width. To that must be added the **±11 %**
anchor ambiguity (A vs A′) and the **±9 %** stroke ambiguity (inner vs outer box). Combining, the
inner-detector-modules envelope is **≈ 4.1–5.4 cm across, with an overall uncertainty of roughly
±15 %**, i.e. a defensible range of **3.5–6.2 cm**.

**Non-independence statement (V10), explicit.** Anchor A takes its scale from the **same published
100 mm COV cylinder that the primary determination rests on**. It therefore **corroborates nothing
independently** and is nowhere counted as a second confirming source. Anchor B uses a different
number (297 mm) but the **same paper** (arXiv:2508.02488v1 §2), so it is not source-independent
either. A genuinely independent third route would require the **Goupy 2024 thesis, which is
unobtainable** (MANIFEST.md §4).

**Verdict weight: none.** This measurement is corroborative only. It is consistent with the 5.0 cm
tight cavity estimate of §5, and that consistency is the entirety of what it establishes. **No
dimension in §3, §4, §5 or §6 is derived from Fig. 1(e).**

---

## 8. Wafer-to-array area ratio — both bases labelled

Wafer face area **103.2256 cm²** (CONVENTIONS §D; 10.16 × 10.16). `veto_envelope.area_ratio()`
raises `ValueError` unless a basis is named explicitly.

| Basis | Reference footprint | Ratio | Provenance |
|---|---|---|---|
| **Published array-crystal footprint** | **2.25 cm²** = 9 × (5 mm)² | **45.9×** | arXiv:1905.10258 Fig. 8 ("two 3 × 3 arrays") + §3.2.1 ("(5 mm)³ Al₂O₃ cubic crystal"); the 5 mm edge is independently confirmed by the 08-01 C.2/C.3 mass closures (4.996 mm and 5.008 mm from the published 6.8 g and 4.5 g array totals) |
| **Project holder-scale estimate** | **~9 cm²** | **11.5×** | **THIS PROJECT'S OWN NOTES, marked as computed.** A holder-scale estimate repeated in `GPD/ROADMAP.md`. **NOT a NUCLEUS number and not traceable to any NUCLEUS publication.** |

The two bases differ by exactly a factor of **4**, which is why an unlabelled ratio carries false
provenance (`fp-unlabelled-area-ratio`). **No unlabelled area ratio appears in this document, and
the ~9 cm² figure is nowhere attributed to NUCLEUS.**

---

## 9. What would overturn this verdict

Named, and assessed quantitatively where possible.

1. **The Goupy 2024 thesis showing rectangular COV crystals large enough for a cavity of at least
   10.16 cm in two axes.** This would overturn the two *cavity* clearances (rows 3 and 4) outright.
   It would **not** touch the verdict, which rests on the coverage comparison against the cap outer
   diameter and makes no cavity assumption. Status: unobtainable by any scripted route
   (MANIFEST.md §4); the anti-bot challenge was not defeated.

2. **A published NUCLEUS upgrade geometry with a materially larger cavity.** Same scope as (1) for
   the cavity rows. To touch the verdict it would additionally have to enlarge the **cap crystals**,
   not merely the cavity.

3. **Evidence that the 100 mm crystal is commissioning-only, with larger Chooz cylinders.**
   Assessed two ways.
   *Qualitatively:* weakened by the fact that arXiv:2509.03559v1 §2 independently states a
   **2.5 cm** crystal thickness, matching the commissioning crystal's **25 mm** height — the two
   descriptions are consistent — and by the 2019 paper's independent "a diameter of 10 cm" from a
   different setup generation six years earlier.
   *Quantitatively:* a Chooz cap would need a diameter of **at least 14.3684 cm**, i.e. **more than
   43 % larger** than the published 100 mm, to bring the coverage clearance to zero. A cap 43 %
   larger in diameter is 2.06× in area and, at unchanged 2.5 cm thickness, **2.06 kg** rather than
   the published 1 kg — a change that would be visible in any published mass statement.

4. **A source stating the COV internal cavity dimension directly**, superseding the entire bounding
   argument of §5. This would replace rows 3 and 4 with a measurement; it would not touch rows 1,
   1b or 2.

5. **A published statement that the wafer would be mounted other than face-parallel** — e.g. edge-on
   or tilted. This does **not** overturn the verdict but it does collapse its margin: the
   orientation-invariant clearance is −0.1620 cm, which is not sign-robust, so under a non-planar
   mounting the determination would become **inconclusive on the coverage basis** rather than
   no-fit, and would rest only on the (also not sign-robust) edge comparison. **This is the single
   most efficient way to disconfirm the current framing**, and it is why the mounting premise is
   stated everywhere the −4.37 cm figure appears.

6. **The two figure-scaling anchors disagreeing by more than ~30 %**, which would have removed the
   corroborating measurement entirely. Tested: they agree to **6.6 %**. This did not occur.

---

## 10. Uncertainty markers carried forward

**Weakest anchors.**
- The 10.0 cm COV cap diameter comes from arXiv:2508.02488, a **TUM commissioning** paper not in
  the ROADMAP anchor list, describing a setup in which only one of the six crystals was installed.
- Both published statements of the cap diameter are low-precision — "100 mm" (2 s.f.) and "a
  diameter of 10 cm" (1 s.f.). The edge clearance of −0.16 cm is smaller than its own input
  precision and is retained only as a premise-free minimal statement.
- The ~5 cm COV internal cavity is the weakest link among the cavity clearances, which is why the
  verdict is routed through the coverage comparison instead.
- The coverage comparison depends on **two** premises: that a cap must cover the wafer footprint,
  and that the wafer is mounted face-parallel.
- `08-RESEARCH.md` §F1's orientation lemma was found false; anything else in that document resting
  on it should be treated as suspect until re-checked. §F1, Pitfall 7, the SC1 starting-point table
  and Caveat 2 have been corrected in place with dated notes.
- **The vertical axis of the cavity is entirely unconstrained** by available sources. This
  determination speaks only to the in-plane, coverage and diagonal requirements.

**Unvalidated assumptions.**
- Face-parallel mounting (the primary clearance depends on it).
- That the four rectangular 2.5 cm slabs sit inside the cap rim (rows 3 and 4 depend on it).
- That the commissioning COV crystal and the Chooz cap crystals are the same part — supported only
  by the matching 2.5 cm / 25 mm thickness and the 10 cm / 100 mm diameter agreement.
- That no mounting, clamp or Cu-support allowance need be added. Adding one would only make the
  shortfall larger, so this assumption is conservative **in the direction of a fit**.

**Competing explanations.**
- The rectangular COV crystals could be substantially larger than the cylindrical caps, giving a
  cavity above 5 cm. Rows 1, 1b and 2 survive this; rows 3 and 4 do not.
- The 100 mm crystal could be a commissioning-only part. Weakened by the independent 2.5 cm
  thickness statement in the 2026 paper and by the 2019 "10 cm"; quantified in §9 item 3.

**Scope statement (`fp-resized-veto`).** No modified, resized, scaled-up or hypothetical veto
geometry is proposed, sized, sketched or evaluated anywhere in this document. The 14.37 cm figure
in §9 item 3 is a **threshold for overturning the verdict**, not a proposed geometry. This phase
determines fit against the published geometry; it does not redesign the experiment.
