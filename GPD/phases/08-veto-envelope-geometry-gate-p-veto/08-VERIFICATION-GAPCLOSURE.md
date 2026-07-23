<!-- ASSERT_CONVENTION: metric_signature=not_applicable — no relativistic field theory in this detector/rate pipeline, fourier_convention=not_applicable, natural_units=internal-only (hbar=c=1) for CEvNS cross section; k_B EXPLICIT (not =1); I/O in eV/keV/MeV, counts/kg/day/keV, s, cm/um -->

# Phase 8 — Verification Gap Closure

**Closes:** the six gaps of `08-VERIFICATION.md` §10 (D1–D6 / G1–G6).
**Date:** 2026-07-22 · **Scope:** bounded correction pass. Not new physics, not a re-plan.
**Authority:** corrects Phase-8 artifacts and code. Does **not** change the verdict, does not choose
a re-scope direction, does not assign veto credit above 1.0, does not propose a modified veto.

---

## 0. Bottom line, stated first because a re-scope decision is pending

| Question | Answer |
|---|---|
| Did the **verdict** change? | **No.** NO FIT, coverage basis, C = −4.3684 cm. |
| Did the verdict's **direction** change? | **No.** Every clearance, every closed form and every sign-robustness endpoint is byte-identical to before this pass. |
| Did the **milestone-void argument** change? | **No** — and it is now stated on its actual foundation. Its load-bearing input is the **45.88× payload-footprint change** (103.2256 cm² wafer vs the published 2.25 cm² array-crystal footprint), which **none of the six gaps touches**. |
| What *did* change? | **How hard the verdict is to overturn.** The "a 43 %-larger cap would mass 2.06 kg, which would be visible in a published mass statement" argument closes **one of two routes**. The assembly-level route is **not closed by any published statement**, and the user was previously not told that. |
| Net effect on the re-scope decision | **The decision is still safe to make, and it is now safe for the right reason.** It should rest on the 45.88× payload-footprint argument, which is untouched, rather than on the coverage margin alone. |

**One honest caveat about this pass itself.** Two of the six corrections (G1, G3) *weaken* claims the
phase previously made. Neither weakens any *number*. G1 weakens a falsifiability claim; G3 weakens a
corroboration claim in a direction that is conservative for the verdict. Nothing in this pass
strengthened a claim in the direction of the expected conclusion.

---

## 1. Gap dispositions

### G1 — the single-cap vs assembly-level coverage premise **(significant) — CLOSED, by restatement plus re-derivation**

**Finding accepted in full.** 08-01 A.11's grammatical subject is the six-crystal COV arrangement:
*"**The COV is an arrangement of two cylindrical and four rectangular 2.5 cm thick HPGe
crystals**... **It** hermetically covers the cryogenic target detectors."* Applying that requirement
to one cylindrical cap was an unwritten additional step.

**What was done — both halves of the fix the verifier offered, not one or the other.**

**(a) The single-cap requirement is now derived, with its inferential step marked**
(`08-03-FIT-DETERMINATION.md` §3.1, new). The derivation uses one piece of already-frozen evidence
the phase had never exploited — **A.1's placement clause**, not just its diameter:

| Step | Statement | Status |
|---|---|---|
| 1 | Six crystals give nearly-4π coverage of the target detectors | **published** (new evidence entry **A.20**, arXiv:2508.02488v1 §2) |
| 2 | Two are cylindrical, four rectangular, all 2.5 cm thick | **published** (A.10) |
| 3 | The crystal installed **"directly above the target detectors"** is a **cylinder** | **published** (A.1 — the clause the phase had quoted only for its diameter) |
| 4 | The two cylinders are the enclosure's top and bottom; the four rectangles are its lateral walls, none overhanging | **INFERENCE — no published sentence states it** |
| 5 | ⇒ only the top cap covers the wafer's top face ⇒ requirement √2·a = 14.3684 cm | follows from 1–4 |

Step 4 is the **same** unpublished assignment the tight cavity bound already rests on
(`D_cavity ≈ D_cyl − 2 t_rect`). The material discovery is that **row 1 — the verdict basis —
depends on it too**, which the earlier text did not say. It is now carried as an explicit **third
premise** on the verdict (gate verdict §1 premise 2) and as an unvalidated assumption in both
§10 blocks.

**(b) The overturning threshold is re-derived into two routes** (08-03 §9 item 3, gate verdict §1.4):

| Route | What it requires | Closed by published evidence? |
|---|---|---|
| **A — single cap** | a published Chooz cap ≥ **14.3684 cm** ⇒ 2.06× area ⇒ **2.06 kg** vs a published 1 kg | **Yes, effectively.** A doubled crystal mass would be visible in the one published COV crystal mass statement (A.1). *Unchanged by this pass.* |
| **B — assembly-level** | the rectangular crystals projecting over the payload's top face, filling **24.6858 cm²** (23.91 % of the wafer face) out to a corner radius of 7.1842 cm — a **2.1842 cm** radial reach beyond the published cap rim | **NO. Nothing published excludes it.** |

**Why route B is not closed, stated as evidence rather than assertion.** The **only** published
dimension of the rectangular COV crystals is their **2.5 cm thickness** (A.10). No source gives
their length, width, placement, or mass; **no total COV mass is published**; the only published
per-crystal mass is the 1 kg of the single commissioning **cylinder**. A redistribution of germanium
into larger rectangles leaves **no signature in any published mass statement** — which is precisely
the argument route A depends on.

**Arithmetic, computed not transcribed:**

```output
wafer face area                       103.2256 cm^2
published 10.0 cm cap disc             78.5398 cm^2   (r=5.00 < half-edge 5.08 -> disc lies inside)
residual uncovered (centred cap)        24.6858 cm^2  = 23.91 % of the face
corner reach sqrt(2)*a/2                 7.184205 cm
cap rim reach                            5.000000 cm
radial shortfall                         2.184205 cm
single-cap threshold sqrt(2)*a          14.368410 cm ; area ratio 2.0645
```

**Honest weighing, recorded so this is not read as a retraction of the verdict.** Two published
facts push *against* route B (A.1 places a cylinder directly above the payload; six crystals for a
nearly-4π enclosure most naturally means four lateral walls). Two push *for* it (the Chooz payload
is 18 targets + 6 COV crystals, not one commissioning detector; and G2's finding that the paper's
own Chooz-transfer claim stops short of the COV). **Published text cannot settle it.** Flagged for
expert verification.

**What G1 does NOT change.** Rows 1b (orientation-invariant floor, −0.1620 cm) and 2 (edge,
−0.1600 cm) compare the wafer against the published crystal's *own* diameter and ask nothing about
what covers what. They are untouched. **The verdict direction is unaffected.**

**`fp-resized-veto` compliance.** The 24.6858 cm² and 2.1842 cm figures are overturning
**thresholds**, computed from the published cap and the wafer, exactly as the 14.3684 cm figure is.
No modified veto geometry is proposed, sized or costed; no rectangular-crystal dimension is
invented; no mass is assigned to a hypothetical crystal.

**Artifacts changed:** `08-03-FIT-DETERMINATION.md` §0 (third qualification), §3 row 1, §3.1 (new),
§6.1, §9 item 3 (3a/3b), §10; `08-05-GATE-VERDICT.md` header, §1 premises, §1.3, §1.4, §2.3, §2.6
item 3b, §8.1, §8.2 direction 4; `src/qpd_potential/veto_envelope.py` `comparison_bases()` coverage
premise; new test `test_coverage_premise_is_stated_as_assembly_level_with_the_single_cap_inference`.

---

### G2 — the missed disconfirming Chooz-transfer sentence **(significant) — CLOSED**

**Finding accepted in full.** `data/external/nucleus/2508.02488v1.txt` line 218 appeared in no
Phase-8 artifact. Re-verified from the frozen file by a recorded command:

```bash
cd data/external/nucleus
grep -o -F "It is important to note that the passive shielding described above – and commissioned in this work – is identical to the configuration planned for Chooz, with just one exception: an additional boron carbide (B4C) layer surrounding the target detectors." 2508.02488v1.txt
```

The grammatical subject was confirmed **mechanically**, not asserted:

```bash
grep -o -E "[^.]{0,130}is identical to the configuration planned for Chooz" 2508.02488v1.txt
# -> It is important to note that the passive shielding described above – and commissioned in this
#    work – is identical to the configuration planned for Chooz
```

and a negative check confirms no equivalent statement exists for the COV (annotated expectation
`0`; `grep -c` exits 1):

```bash
grep -c -E "(COV|outer veto)[^.]{0,200}identical to the configuration planned for Chooz" 2508.02488v1.txt   # 0
```

**Both directions recorded, as the verifier required:**

- **Corroboration previously unclaimed:** the **29.7 cm internal shielding** and **43.0 cm cryostat
  bore** are Chooz dimensions *by the paper's own explicit statement*. The single exception the
  sentence names (an added B₄C layer at Chooz) is already carried independently as A.9, so the two
  sources agree on what the exception is. This strengthens the loose cavity bound (+2.3316 cm), which
  is built from the 29.7 cm.
- **Disconfirming, and it points against the transfer the verdict relies on:** the boundary is drawn
  around the **passive shielding** and **not** around the COV — in the same section that says only
  one of six COV crystals was installed. **The load-bearing 10.0 cm sits outside the only explicit
  transfer claim its own source makes.**

**It does not overturn the 100 mm read.** The 2019 "10 cm" (with the new A.19 caveat), the
independent 2.5 cm COV thickness in arXiv:2509.03559v1, and the C.1 mass closure still support it.
What changes is that the phase's central caveat is now argued **from this sentence** rather than from
the general observation that the paper is about TUM.

**Artifacts changed:** `08-01-SOURCE-EVIDENCE.md` new **A.18** + uncertainty markers;
`08-03-FIT-DETERMINATION.md` §1.1 table, §1.2 (dated correction), §9 item 3, §10;
`08-05-GATE-VERDICT.md` §2.1 (dated addition), §8.1; `veto_envelope.py`
`_COV_CRYSTAL_DIAMETER.note` and `_INTERNAL_SHIELD_DIAMETER.note`; test
`test_cov_crystal_diameter_note_retires_the_same_quantity_claim` asserts A.18 travels with both.

---

### G3 — "outer veto diameter" registered as a cap-crystal diameter **(minor) — CLOSED, by retirement**

**Finding accepted.** The 2019 Fig. 8 caption attributes its 10 cm to component **(3)**, which the
same paper defines as *"a surrounding kg-scale cryogenic detector used as outer veto"* — recorded as
new evidence entry **A.19** with its own grep command. The 2508 "100 mm" describes **one cylindrical
crystal**. **Nothing published establishes that these are the same object**, and the "two published
statements of the same quantity" framing is **retired**.

**What replaces it (weaker, and what can honestly be said):** two papers, six years and two setup
generations apart, both place the outer veto's *characteristic* diameter at 10 cm. The 100 mm **cap**
read is licensed by the **C.1 mass closure** (1045.17 g against a published 1 kg), **not** by the
2019 caption.

**Direction check.** If the 2019 10 cm is the **assembly** extent, then the caps and the cavity are
**strictly smaller** than 10 cm and every clearance becomes **more** negative. The ambiguity is
**conservative for the verdict**: retiring the claim removes an overstated corroboration without
weakening any clearance. What it costs — the claim of *independent* corroboration — is recorded in
both §10 blocks.

**Artifacts changed:** `08-01-SOURCE-EVIDENCE.md` new **A.19**; `08-03-FIT-DETERMINATION.md` §1.1
table, new §1.3, §9 item 3, §10; `08-05-GATE-VERDICT.md` §1 verdict wording + corroboration
correction; `veto_envelope.py` `_COV_CRYSTAL_DIAMETER.note` and the `wider_half_width_cm` field
docstring; new test asserts the retired phrase survives only inside its own retraction.

---

### G4 — two sampled `min b₂` values **(minor) — CLOSED, and the verifier's diagnosis is refined**

**The verifier hypothesised "one is a transcription slip". It is not.** They are **two different
runs**, and the projected-diameter column proves it — a transcription slip cannot move a projected
diameter from 10.1623 to 10.2039.

| Sampled triple | min b₁ | min b₂ | min proj Ø | Where it appeared |
|---|---|---|---|---|
| **Plan-08-03 execution — CANONICAL** | 9.7076 | **7.3945** | **10.1623** | `08-03-FIT-DETERMINATION.md` §2.1, `08-03-SUMMARY.md` |
| Pre-execution planning reference run | 9.7185 | 7.4210 | 10.2039 | `08-RESEARCH.md` §F1, `08-03-PLAN.md`, `veto_envelope.py`, `tests/test_veto_envelope.py` |

**Re-run once during this pass**, with the sampling code actually in `tests/test_veto_envelope.py`
(`scipy.spatial.transform.Rotation.random(200_000, random_state=20260722)`), and reproduced exactly:

```output
REPRO seed 20260722, N=2e5:
  min b1 = 9.7076
  min b2 = 7.3945
  min proj = 10.1623
(numpy 1.26.4, scipy 1.17.1, Python 3.11.7, Darwin 25.3.0 arm64)
```

**One number is now used everywhere.** The planning-run figures were replaced in
`veto_envelope.py`, `tests/test_veto_envelope.py` and `08-RESEARCH.md` §F1, each with a dated note
explaining the two-run finding. `08-03-PLAN.md` retains them as **frozen historical planning text**
and is labelled as such rather than rewritten. The canonical triple is now **pinned by assertion**
in `test_so3_sampled_minima_are_bounded_below_by_the_true_infima`, so the planning figures cannot
silently reappear.

**Non-load-bearing, as the verifier said.** Both triples sit above the analytic infima; no clearance
uses a sampled value; every binding assertion remains a one-sided lower bound.

---

### G5 — the `min b₁` bracket's upper end was loose **(minor) — CLOSED, tightened to an ATTAINED value**

**Finding accepted and reproduced independently.** Multistart Nelder–Mead over SO(3) (400 random
starts, `xatol = 1e-12`, `fatol = 1e-14`):

```output
min b1 (multistart NM, physical t=0.20) = 9.666923
  full box at optimum: [9.666923 9.666923 9.666923]      <- a CUBE
  Prince-Rupert zero-thickness bound a/(3sqrt2/4) = 9.578940
  excess over PR bound = 0.087983 cm
```

The optimum's bounding box being a **cube** is the expected signature of a smallest-enclosing-cube
solution and is what makes 9.666923 an **attained** value rather than another loose sampled one.

| Quantity | Value | Label |
|---|---|---|
| `a/(3√2/4)` | **9.5789 cm** | Prince-Rupert **zero-thickness** lower bound; **not attained** at t = 0.20 cm |
| Attained minimum, physical plate | **9.6669 cm** | numerical, cubic bounding box |
| Uniform sampling (2 × 10⁵) | 9.7076 cm | approaches from above; **not** a tight upper bound |

**The defensible statement is now: the wafer fits inside a cube of side ≈ 9.667 cm, and cannot fit
inside a cube of side < 9.5789 cm.** Quote **9.667 cm** — not 9.72 cm, not 9.58 cm.

Locked in by a new test (`test_min_b1_attained_value_is_above_the_zero_thickness_prince_rupert_bound`)
which checks the strict ordering `9.5789 < 9.6669 < 9.7076` and verifies the recorded orientation
really gives a cube. The optimization itself is not re-run in the suite (slow, stochastic); the cubic
box at the recorded rotation vector is an exact, cheap, deterministic substitute.

**Enters no clearance and no verdict**, exactly as the artifacts already said.

---

### G6 — "all 52 grep commands exit 0" **(trivial) — CLOSED**

`grep -c` **exits 1 when the count is zero**. Six commands were zero-match negative checks by design;
this pass added a seventh (A.18's COV check). Re-verified after the addendum:

```output
total commands: 57
nonzero exits: 7   (exactly the 7 annotated zero-match checks, and no others)
```

The six original ones establish the Success-Criterion-1 amendment (`envelope`, `cavity`,
`inner diameter`, `clearance`, `100 mm`, `m.w.e` all absent from `2509.03559v1.txt`) — i.e. those
nonzero exits are the *point* of one of the block's most load-bearing findings.

**Corrected wording, used in both places: "all 57 commands reproduce their annotated expectations."**
`08-01-SOURCE-EVIDENCE.md` §G now carries the warning at the source, so the error cannot be
reintroduced by a reader of the evidence block alone.

**Revised evidence-block totals: 37 quotes / 57 grep commands** (was 34 / 52). Updated in the gate
verdict §6 and §8.1.

---

## 2. Verification of this pass

### 2.1 Test suite — full repository, actually run

```output
313 passed, 1 warning in 44.38s
```

**310 → 313.** Three tests added, none removed, none weakened:

| New test | Gap | What it locks in |
|---|---|---|
| `test_min_b1_attained_value_is_above_the_zero_thickness_prince_rupert_bound` | G5 | the ordering 9.5789 < 9.6669 < 9.7076 and the cubic bounding box at the attaining orientation |
| `test_cov_crystal_diameter_note_retires_the_same_quantity_claim` | G3, G2 | the retired phrase appears only inside its retraction; A.18 and A.19 travel with the constants |
| `test_coverage_premise_is_stated_as_assembly_level_with_the_single_cap_inference` | G1 | the premise names "assembly-level", "inference", "no published sentence states", both overturning routes, and the 24.6858 cm² threshold |

Two assertions were also **added** to the existing SO(3) sampling test: the canonical triple is
pinned (G4), and the sampled `min b₁` is required to lie strictly above the attained 9.666923 (G5).
`tests/test_veto_envelope.py` goes from 21 to 24 tests.

### 2.2 Evidence-block integrity, re-run

```output
total commands: 57
nonzero exits: 7   (all annotated zero-match negative checks)
```

### 2.3 Nothing decisive was recomputed differently

Every clearance, closed form and sign-robustness endpoint is unchanged. The verifier's independent
confirmations stand as recorded: `min b₂ = 7.325626 = (a+t)/√2` attained, `min projected Ø =
10.161968 = √(a²+t²)` attained, coverage requirement `√2·a = 14.368410` distinct from the space
diagonal `14.369802`, mass closure `1045.17 g` at ρ = 5.323, and the six clearances
`−4.3684 / −0.1620 / −0.1600 / −5.1600 / −9.3684 / +2.3316`.

### 2.4 Honesty conditions preserved, checked explicitly

The verifier credited the phase for two things this pass was required not to erode. Both verified
present after the edits:

- **The declined sign-robustness claim.** Under the primary source's own 2-s.f. "100 mm" the
  orientation-invariant floor **is** sign-robust (`[−0.212, −0.112]`), and the phase still declines
  to claim it, downgrading on the 2019 paper's 1-s.f. reading instead. Unchanged.
- **The one positive number kept prominent.** `+2.3316 cm` still appears three times in the gate
  verdict — the §1.2 basis table, the §1.2 prose paragraph that gives it its own emphasis, and the
  new §2.1 correction — always labelled as **not excluding the wafer**. G2 *strengthens* it (the
  29.7 cm it is built from is now a Chooz dimension by the paper's own statement) and it was not
  demoted anywhere.

---

## 3. What remains open after this pass

| Item | Status | Why it cannot be closed here |
|---|---|---|
| **Whether route B is physically realizable** — can a 2-cylinder + 4-rectangle HPGe arrangement hermetically cover a 10.16 cm square footprint with no cap ≥ 14.37 cm? | **unresolved** | Needs the Goupy 2024 thesis or NUCLEUS collaboration knowledge. No computational check settles it. This is now the *most* material open item, because it governs how hard the verdict is to overturn. |
| **Whether the 100 mm cylinder is a commissioning-only part** | **unresolved, and G2 makes the question sharper** | A.18 gives the sharpest textual evidence and it points against the transfer; a definitive answer needs the collaboration or the thesis. |
| **Whether the wafer physically fits the cavity (what VALD-09 literally asks)** | **unresolved** | The tight cavity is an estimate on the same unpublished assignment as G1 step 4; the only premise-free bound (+2.3316 cm) does not exclude. Recorded by the verifier as a scope tension and not closed by this pass. |
| **Whether coverage is the right efficacy criterion at all** | **not addressed** | A veto's rejection power degrades continuously with partial coverage rather than failing at a geometric threshold. The binary framing is a modelling choice Phase 8 does not defend, and this pass does not defend it either. |
| The unlabelled "~9 cm²" figure in `GPD/REQUIREMENTS.md` and `GPD/ROADMAP.md` | **still open** | Out of scope for Phase 8 by the phase-context decision; flagged, not fixed. |

---

## 4. Prohibitions, re-asserted after the edits

Both locked user decisions of 2026-07-22 hold across every change in this pass:

- **No reduced veto credit.** No partial, best-guess or "for reference" rejection value was added.
  All 19 taxonomy credits remain exactly 1.0; `veto_credit.py` is untouched by this pass.
- **No resized veto invented.** The new quantities (24.6858 cm², 2.1842 cm) are **overturning
  thresholds** computed from the published cap and the wafer, in the same category as the pre-existing
  14.3684 cm threshold. No modified geometry is proposed, sized, sketched or costed; no rectangular
  crystal dimension is invented; no mass is assigned to any hypothetical crystal.

---

_Phase 8 (Veto-Envelope Geometry Gate, P-VETO), verification gap closure. Corrects
`08-01-SOURCE-EVIDENCE.md`, `08-03-FIT-DETERMINATION.md`, `08-05-GATE-VERDICT.md`,
`08-RESEARCH.md`, `src/qpd_potential/veto_envelope.py` and `tests/test_veto_envelope.py`.
The verdict, its direction and the milestone-void argument are unchanged._
