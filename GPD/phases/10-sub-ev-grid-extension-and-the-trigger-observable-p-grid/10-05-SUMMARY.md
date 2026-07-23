---
phase: 10-sub-ev-grid-extension-and-the-trigger-observable-p-grid
plan: 05
status: complete
one_liner: "30 archived artifacts registered with dispositions and guarded floors; the three shared-grid spectra carry onto the extended axis bit-for-bit (max difference 0.0) while the archived response matrices deliberately do NOT; the counting floor re-derived from the pipeline agrees with the roadmap to <3% and the 100 eV saturation check comes out sub-linear (ratios 0.842/0.818) as it should; the display rule is retracted everywhere except paper/HANDOFF.md, which scope forbids editing."
plan_contract_ref: GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-05-PLAN.md#/contract

contract_results:
  claims:
    claim-disposition:
      status: passed
      summary: "30 tracked .csv/.npz artifacts enumerated by a recorded command, 30 register rows (the register itself is listed as a self-referential row rather than special-cased in the guard), closed disposition vocabulary, every row with a non-empty written reason, every bounded row with a numeric validity floor RE-READ from the frozen file at test time. The guard raises LegacyArtifactError below a recorded floor, reporting the value, the floor, the native axis, the units and the disposition; arrays are rejected wholesale and non-finite input is out of domain. The three shared-grid deposit spectra carry onto the extended axis by INDEX with max difference exactly 0.0, and the test also verifies they genuinely sit on those bins so the carry check is not a tautology."
      linked_ids: [deliv-register, deliv-register-code, deliv-register-tests, deliv-disposition-note, test-register-closure, test-guard-raises, test-carry-without-reinterp]
      evidence:
        - verifier: gpd-executor
          method: mechanical enumeration, run-time floor re-reading, and an index-carry bit-identity check with a non-tautology guard
          confidence: high
          claim_id: claim-disposition
          deliverable_id: deliv-register
          acceptance_test_id: test-carry-without-reinterp
          reference_id: ref-roadmap-sc2
          forbidden_proxy_id: fp-silent-carry
          evidence_path: GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-05-ARTIFACT-DISPOSITION.md
    claim-floor:
      status: passed
      summary: "N_obs extracted from the plan 10-04 extended matrices and the floor computed as 100/sqrt(N_obs): 35.399% / 31.375% at 0.1 eV, 16.009% / 14.271% at 0.5 eV, 3.596% / 3.219% at 10 eV, 1.235% / 1.117% at 100 eV. All eight agree with the roadmap figures to within 3%, and the measured N_obs at 0.5 eV (39.019 / 49.100) corroborates the note's 39.4 / 49.9 to -0.97% / -1.60%. The 100 eV saturation check comes out SUB-LINEAR (ratios 0.8416 / 0.8182), so the informative failure did not occur. The document carries the best-case framing, the five omitted noise sources, the no-resolution-parameter statement, the Phase-11 quadrature comparison, and the 1/sqrt(N)-versus-actual-spread verdict."
      linked_ids: [deliv-floor-note, test-floor-rederived, test-floor-saturation-signature, test-floor-not-resolution]
    claim-labelling:
      status: partial
      summary: "The regime boundary is imported from trigger.SUBEV_REGIME_BOUNDARY_eV = 1 eV in both sub-eV deliverables, with the trigger-probability-not-dR/dE_rec statement. The retracted display rule was converted from a live statement to dated retracted history in five places: the notebook's final cell, src/qpd_potential/fold.py, and three GPD/literature files, plus GPD/CONSISTENCY-CHECK.md. PARTIAL because ONE live occurrence remains that this plan is explicitly forbidden to fix: paper/HANDOFF.md line 33 states 'Display rule: nothing below 10 eV on any figure ... Keep this for any new/regenerated figure.' Plan 10-05's scope forbids editing anything under paper/, and its own verification requires git diff to touch nothing there. Recorded as an open follow-up rather than silently excluded."
      linked_ids: [deliv-notebook-fix, deliv-floor-note, deliv-disposition-note, test-retraction, test-regime-labelled]
  deliverables:
    deliv-register:
      status: passed
      path: artifacts/v2.0/legacy_grid_disposition.csv
      summary: "30 rows: path, native_axis, axis_units, validity_floor, disposition, reason. Header records the enumeration command and the closed disposition vocabulary. Tally by row: 16 bounded_native_axis, 7 not_a_spectrum, 3 carried_onto_extended_axis_without_reinterpolation, 2 bounded_superseded, 2 native_to_extended_axis."
      linked_ids: [claim-disposition]
    deliv-register-code:
      status: passed
      path: src/qpd_potential/legacy_grid.py
      summary: "Register loader with a closed disposition vocabulary that raises on an unknown tag or an empty reason; check_evaluation_point raising LegacyArtifactError below a recorded floor; carried_onto_extended_axis performing the index carry and filling the lower 160 bins with NaN rather than zero, because the artifact carries no data there and a zero would read as a measured absence."
      linked_ids: [claim-disposition]
    deliv-register-tests:
      status: passed
      path: tests/test_legacy_grid_disposition.py
      summary: "30 tests: register closure, floors re-read from files, guard raises, guard message content, unregistered artifact raises, the three carry checks with the non-tautology half, carry rejects a non-v1.0-grid quantity, the response-matrices-are-NOT-carried finding, frozen-header non-rewrite with the documented suite churn handled explicitly, the retraction grep, the notebook check, the regime label, eight floor re-derivations, the two saturation-signature checks, and the floor-document framing checks including the measured-numbers-are-present check."
      linked_ids: [claim-disposition, claim-floor, claim-labelling]
    deliv-disposition-note:
      status: passed
      path: GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-05-ARTIFACT-DISPOSITION.md
      summary: "The wide-versus-narrow reading of 'archived v1.x spectrum' with the choice justified; the sidecar principle; the enumeration command; the closed vocabulary; why the carry is not a tautology; the response-matrix finding; the guard's raise behaviour with a sample message; the full 30-row table; the unresolved paper/HANDOFF.md occurrence; the before/after retraction table; and four stated weakest points."
      linked_ids: [claim-disposition, claim-labelling]
    deliv-floor-note:
      status: passed
      path: GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-05-COUNTING-FLOOR.md
      summary: "Opens with the best-case / not-a-resolution framing and the table of five omitted noise sources before any number appears. Derived floors for both designs at all four energies beside the roadmap figures with percentage differences; the 100 eV saturation check with the linear extrapolation, the ratio and the outcome stated either way; the 1/sqrt(N)-versus-actual-spread table with a verdict; the Phase-11 quadrature comparison; four inherited weaknesses; and a provenance table for every number."
      linked_ids: [claim-floor]
    deliv-notebook-fix:
      status: passed
      path: notebooks/paper_calculations.ipynb
      summary: "The final cell no longer prints the retracted rule as a project rule. It prints a dated RETRACTED 2026-07-22 line, the 100 meV floor with the 744-bin grid parameters, and the 1 eV regime boundary imported from trigger.SUBEV_REGIME_BOUNDARY_eV together with trigger.REGIME_STATEMENT. The notebook re-executes end to end with zero error outputs, 32 anchor lines, zero CHECK flags."
      linked_ids: [claim-labelling]
  acceptance_tests:
    test-register-closure:
      status: passed
      summary: "30 enumerated artifacts == 30 register rows, set equality both ways. No empty disposition, no reason shorter than 40 characters, every bounded row carrying a positive numeric floor. Floors independently re-read from the frozen files and compared to 1e-12 relative."
      linked_ids: [claim-disposition, deliv-register, deliv-disposition-note]
    test-guard-raises:
      status: passed
      summary: "LegacyArtifactError raised for the CEvNS table at 0.1 eV (floor 5 eV), the muon deposit spectrum at 1e-4 keV (floor 1.014497e-02 keV), a mixed array containing one below-floor entry, and a NaN. Exactly AT the floor returns a finite value. The message carries the units, the native axis, the disposition and the explicit 'this is an error, not a clamp'."
      linked_ids: [claim-disposition, deliv-register-code, deliv-register-tests]
    test-carry-without-reinterp:
      status: passed
      summary: "For all three shared-grid spectra: max |carried[160:] - original| EXACTLY 0.0, and the lower 160 bins are NaN rather than zero. The non-tautology half also passes: each artifact's 584-row energy column matches the extended axis's centres 160-743 to within 5e-7, so the index carry is genuinely the right operation rather than a statement about array assignment."
      linked_ids: [claim-disposition, deliv-register-tests]
    test-floor-rederived:
      status: passed
      summary: "Eight parametrised cases, all within 3% of the roadmap. Ta->Al: 35.399/35.6, 16.009/15.9, 3.596/3.6, 1.235/1.2. Al->Hf: 31.375/31.6, 14.271/14.2, 3.219/3.2, 1.117/1.1. Derived from N_obs read out of the plan 10-04 matrices, never copied."
      linked_ids: [claim-floor, deliv-floor-note]
    test-floor-saturation-signature:
      status: passed
      summary: "THE informative check, and it came out the informative way. Measured N_obs at 98.603 eV is 6557.1 (Ta->Al) and 8021.3 (Al->Hf) against linear extrapolations of 7791.1 and 9804.1 -- ratios 0.8416 and 0.8182, i.e. sub-linear, consistent with the ~52.9 and ~32.1 eV saturation onsets. The derived floors 1.235% / 1.117% land on the roadmap's 1.2% / 1.1% and are closer to them than the naive linear 1.133% / 1.010% are, for both designs. Reproducing the linear values would have been a finding; it did not happen."
      linked_ids: [claim-floor, deliv-floor-note]
    test-floor-not-resolution:
      status: passed
      summary: "Human-review test discharged by self-assessment plus a machine-checkable component. The document opens with the best-case / no-resolution-parameter framing BEFORE any number, tabulates the five omitted noise sources, names fp-poisson-as-resolution, carries the Phase-11 quadrature comparison, and repeats a best-case parenthetical under every numeric table. A test asserts all ten required framing strings and the measured N_obs values are present. Recorded as pending researcher review."
      linked_ids: [claim-floor, deliv-floor-note]
    test-retraction:
      status: partial
      summary: "The grep is scoped to statements of the DISPLAY rule (a hit must also contain display/plot/shown/figure), which removes three false positives that merely mention the energy range. Zero live statements remain in src/, tests/, notebooks/ or GPD/ outside the closed milestone archives. PARTIAL because paper/HANDOFF.md line 33 still states the rule as a live instruction and plan 10-05 is forbidden from editing anything under paper/; a dedicated test asserts that occurrence still exists AND that it is recorded in the disposition note, so it cannot be forgotten."
      linked_ids: [claim-labelling, deliv-notebook-fix]
    test-regime-labelled:
      status: passed
      summary: "Both sub-eV deliverables contain the literal SUBEV_REGIME_BOUNDARY_eV, the value '1 eV' formatted from the imported constant, and both 'trigger probability' and 'dR/dE_rec'. No competing literal."
      linked_ids: [claim-labelling, deliv-floor-note, deliv-disposition-note]
  references:
    ref-roadmap-sc2:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Criterion 2 is quoted at the head of the disposition note and drives the register, the 10.14 eV validity floor on the shared-grid products, and the bit-for-bit carry proof. The note also states which reading of 'archived v1.x spectrum' was adopted, because the criterion does not define it."
    ref-roadmap-sc5:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "All eight roadmap percentages are tabulated beside the pipeline-derived values with percentage differences, as comparison targets rather than inputs. Agreement is within 3% throughout."
    ref-fp-poisson:
      status: completed
      completed_actions: [read, avoid, cite]
      missing_actions: []
      summary: "Named explicitly in the counting-floor document's opening block and asserted present by a test. The best-case qualifier is repeated under every numeric table so a value cannot be lifted out of its framing."
    ref-user-decision-floor:
      status: completed
      completed_actions: [read, cite]
      missing_actions: []
      summary: "The STATE.md USER DECISION 2026-07-22 is the origin of the not-a-resolution position, the N_obs = 39.4 / 49.9 figures, and the best-case-with-no-noise-sources framing. Cited as the source of the comparison targets, with the explicit rule that if the pipeline and the note disagree the pipeline wins."
    ref-phase11-broadening:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "Phase 11's 15.5-20.5% at the 0.5 eV threshold is compared directly against the measured counting floors and added in quadrature: 22.3-26.0% (Ta->Al) and 21.1-25.0% (Al->Hf), matching the roadmap's ~22-26%. The document states the consequence: the counting floor alone understates the width from the two known contributions by ~40%, before any noise source."
  forbidden_proxies:
    fp-poisson-as-resolution:
      status: rejected
      notes: "The counting-floor document opens with the best-case and no-resolution-parameter statements BEFORE any number appears, tabulates the five omitted noise sources, repeats a best-case parenthetical under every numeric table, and names the Phase-11 broadening as comparable and absent. A test asserts all of that machine-checkably."
    fp-floor-quoted-not-derived:
      status: rejected
      notes: "N_obs was extracted from artifacts/v2.0/response_matrix_*_ext.npz and the floors computed as 100/sqrt(N_obs). The roadmap percentages appear only in a comparison column with explicit percentage differences, and a provenance table labels them as targets originating in a STATE.md orchestrator note."
    fp-silent-carry:
      status: rejected
      notes: "The carry is an INDEX operation with the lower 160 bins filled with NaN, not zero -- 'that absence is the tag, not a gap to fill'. Bounded artifacts raise below their floor rather than returning an interpolated value. The archived response matrices are deliberately NOT tagged carried, because their CSV-round-tripped centres would make it a genuine 5e-7 re-mapping."
    fp-retracted-rule-retained:
      status: unresolved
      notes: "Converted to dated retracted history in the notebook, src/qpd_potential/fold.py, three GPD/literature files and GPD/CONSISTENCY-CHECK.md. UNRESOLVED for paper/HANDOFF.md line 33, which states it as a live instruction ('Keep this for any new/regenerated figure') and which this plan is explicitly forbidden to edit. Recorded in the disposition note section 10 with a named follow-up owner rather than excluded from the grep."
    fp-header-rewrite:
      status: rejected
      notes: "No frozen artifact's provenance header was edited. The register is a sidecar CSV. The test verifies this with git status and, for the two flux tables that the test suite itself regenerates, verifies that the ONLY changed lines are the 'generated:/git_sha:' provenance stamps -- pre-existing churn, not a header rewrite by this plan."
  uncertainty_markers:
    weakest_anchors:
      - "The roadmap N_obs = 39.4 / 49.9 figures come from an orchestrator note in STATE.md, not a verified deliverable. They are treated as comparison targets; the pipeline gives 39.019 / 49.100 and the pipeline wins. The agreement is close enough that the note is corroborated rather than replaced."
      - "The counting floor inherits every weakness of the sub-eV response: a linear quasiparticle yield with no pair-breaking threshold (6.89 ueV per off-spot sensor against a 190 ueV Al trap gap, 0.018132 quasiparticles assigned), and the LOW-confidence f_prompt and r sharing parameters. A tighter-looking floor at low energy is a longer extrapolation, not a better detector."
      - "The wide reading of 'archived v1.x spectrum' is a judgement call. A reader taking criterion 2 to mean only shared-grid products would find 24 of the 29 rows unnecessary."
      - "The register's validity floors are first-tabulated-abscissa values, not validated support limits. reconstructed_spectra_*.csv have a floor of 1.059254e-06 keV simply because that is where their axis starts."
      - "'not_a_spectrum' is the weakest tag: it records that no re-gridding applies, which is true, but it provides no enforcement against misuse of a scalar registry."
    unvalidated_assumptions:
      - "That a fractional width is a meaningful summary of the sub-eV response column at all. Plan 10-04 measured the column to be a two-class lattice of independently-rescaled sums taking 228 / 359 distinct non-integer values at 0.1 eV -- neither a Poisson staircase nor a Gaussian. 1/sqrt(N_obs) is a label attached to it, not a description derived from it."
      - "That the v1.0 figure's 1e-2 keV axis floor is now justified purely by artifact support rather than by the retracted rule. The number did not change; only its stated justification did. Phases 12-15 own the v2.0 figures."
    competing_explanations:
      - "The 1/sqrt(N) versus actual-spread mismatch could be read as Monte Carlo noise rather than a real inadequacy of the Gaussian label. Against that: the mismatch is ~13% at 0.1 eV AND at 0.5 eV for Al->Hf, and it changes SIGN between them, which noise at N_s = 5000 would not produce systematically."
    disconfirming_observations:
      - "DID NOT OCCUR: 'the measured N_obs at 0.5 eV differs materially from 39.4 / 49.9'. It is 39.019 / 49.100, -0.97% / -1.60%."
      - "DID NOT OCCUR: 'the measured N_obs at 100 eV matches the naive linear extrapolation'. It is 0.8416 / 0.8182 of it, i.e. sub-linear, so saturation IS entering the response above the onsets."
      - "DID NOT OCCUR: 'an artifact whose disposition was carried turns out not to be bit-identical'. All three are, with max difference exactly 0.0."
      - "DID OCCUR: '1/sqrt(N_obs) disagrees with the actual column spread at 0.1 eV'. For Al->Hf the label overstates the spread by 12.5% (31.375% against 27.458%), and at 0.5 eV it understates it by 11.6%. The floor should not be quoted there as a single number without that attached."
      - "DID OCCUR, and is unresolved: one live statement of the retracted display rule survives in paper/HANDOFF.md line 33, which this plan may not edit."
files_created:
  - artifacts/v2.0/legacy_grid_disposition.csv
  - src/qpd_potential/legacy_grid.py
  - tests/test_legacy_grid_disposition.py
  - GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-05-ARTIFACT-DISPOSITION.md
  - GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-05-COUNTING-FLOOR.md
files_modified:
  - notebooks/paper_calculations.ipynb
  - src/qpd_potential/fold.py
  - GPD/literature/PITFALLS.md
  - GPD/literature/COMPUTATIONAL.md
  - GPD/literature/METHODS.md
  - GPD/CONSISTENCY-CHECK.md
---

# Plan 10-05 Summary — Disposition, the Counting Floor, and the Retraction

## The disposition register

**30 tracked `.csv`/`.npz` artifacts enumerated, 30 register rows.** Closed vocabulary,
every row with a written reason, every bounded row with a numeric floor **re-read from
the frozen file** at test time.

The register adopts the **wide** reading of "archived v1.x spectrum" — every tracked
artifact, not only shared-grid products — because the narrow reading would leave
untagged exactly the tables a sub-eV plot is most likely to be silently extended
through (the CEvNS dR/dT table stops at 5 eV). Criterion 2's *purpose* demands the wide
reading; its *letter* does not name it. Stated, not assumed.

It is a **sidecar**: no frozen artifact's provenance header was edited
(`fp-header-rewrite`).

### The carry, and why it is not a tautology

For the three shared-grid deposit spectra the carry is an **index** operation, legitimate
only because plan 10-03 made `np.array_equal(ext_edges[160:], v1_0_edges)` true with max
difference 0.0. Asserting `out[160:] == values` alone would prove nothing about
assignment, so the test checks **both**:

1. **max |difference| = exactly 0.0**, and
2. each artifact's 584-row energy column **really matches** the extended axis's centres
   160–743 to within the recorded **4.918e-07** CSV round-trip precision.

Lower 160 bins are **NaN, not zero** — the artifact carries no data there, and a zero
would read as a measured absence rather than an absence of measurement.

### FINDING — the archived response matrices are **not** tagged "carried"

Their deposit centres are the **CSV round-tripped** values, 4.918e-07 from the extended
axis's exact geometric means. Placing them on the extended axis would be a genuine — if
tiny — **re-mapping**, not an index copy. Calling it "carried" would be the silent
reinterpolation criterion 2 forbids, at the 5e-7 level. They are `bounded_superseded`.

## The counting floor — derived, not copied

| E_dep | Ta→Al N_obs | floor | roadmap | Δ | Al→Hf N_obs | floor | roadmap | Δ |
|---|---|---|---|---|---|---|---|---|
| 0.10138 eV | 7.980 | **35.399 %** | 35.6 % | −0.56 % | 10.158 | **31.375 %** | 31.6 % | −0.71 % |
| 0.49382 eV | 39.019 | **16.009 %** | 15.9 % | +0.69 % | 49.100 | **14.271 %** | 14.2 % | +0.50 % |
| 10.145 eV | 773.399 | **3.596 %** | 3.6 % | −0.12 % | 965.113 | **3.219 %** | 3.2 % | +0.59 % |
| 98.603 eV | 6557.064 | **1.235 %** | 1.2 % | +2.91 % | 8021.322 | **1.117 %** | 1.1 % | +1.50 % |

*(Best-case floors, no noise sources — see below.)*

All eight within 3 %. Measured N_obs at 0.5 eV **39.019 / 49.100** vs the note's
39.4 / 49.9. **The roadmap figures are corroborated by the pipeline, not echoed.**

### The 100 eV saturation check came out the informative way

| Design | measured N_obs | linear extrapolation | ratio | floor (measured) | floor if linear | roadmap |
|---|---|---|---|---|---|---|
| Ta→Al | **6557.1** | 7791.1 | **0.8416** | **1.235 %** | 1.133 % | 1.2 % |
| Al→Hf | **8021.3** | 9804.1 | **0.8182** | **1.117 %** | 1.010 % | 1.1 % |

**Sub-linear for both**, consistent with the ~52.9 / ~32.1 eV Phase-5 onsets. The
measured floors land on the roadmap's 1.2 % / 1.1 % and are **closer to them than the
naive linear values are**. Reproducing the linear values would have been a finding;
**it did not happen**.

### FINDING — 1/√N is a marginal description at and below 0.5 eV

| Design | E_dep | actual std/mean | 1/√N label | label/actual |
|---|---|---|---|---|
| Ta→Al | 0.1 eV | 36.625 % | 35.399 % | 0.967 |
| **Al→Hf** | **0.1 eV** | **27.458 %** | **31.375 %** | **1.143** |
| **Al→Hf** | **0.5 eV** | **16.150 %** | **14.271 %** | **0.884** |

The mismatch is ~13 % **and changes sign** between 0.1 and 0.5 eV for the same design —
not something Monte Carlo noise at N_s = 5000 would produce systematically. Mechanically
this follows plan 10-04's finding that the registered count is **not an integer**
(228 / 359 distinct non-integer values), so the distribution is neither a Poisson
staircase nor a Gaussian. **1/√N is a label attached to the column, not a description
derived from it.**

### The framing, written so it cannot be quoted away

The document opens — **before any number** — with: best case, no noise sources, the
project has **no resolution parameter anywhere**, and the five omitted sources
(baseline, amplifier, phonon-collection, position dependence, readout). Every numeric
table repeats the best-case parenthetical.

**The Phase-11 broadening is comparable and absent**: 15.5–20.5 % at 0.5 eV, adding in
quadrature to **22.3–26.0 % (Ta→Al)** and **21.1–25.0 % (Al→Hf)**. The counting floor
alone understates the width from the two *known* contributions by ~40 %, before any
noise source is added.

## The retraction — and the one place it could not reach

Converted from live statement to **dated retracted history** in five files:

| File | Was | Now |
|---|---|---|
| `notebooks/paper_calculations.ipynb` | *"Nothing below 10 eV is displayed on any spectrum (project display rule)."* | dated **RETRACTED 2026-07-22**, the 100 meV floor, the 744-bin parameters, and the 1 eV boundary imported from `trigger.SUBEV_REGIME_BOUNDARY_eV` |
| `src/qpd_potential/fold.py` | *"Do NOT display anything below 10 eV … (user directive)"* | dated retraction **plus the real reason** the v1.0 figure's axis stops where it does: the v1.0 artifacts it draws have no data below 10.14 eV |
| `GPD/literature/PITFALLS.md` / `COMPUTATIONAL.md` / `METHODS.md` | live standing instruction | marked retracted history with the date |
| `GPD/CONSISTENCY-CHECK.md` | restated the plot-floor memory | marked retracted history with the date |

`GPD/milestones/v1.0/**` and `v1.1/**` are closed archives — history by location, left alone.

### UNRESOLVED

```
paper/HANDOFF.md:33: **Display rule: nothing below 10 eV** on any figure ...
                     Keep this for any new/regenerated figure.
```

**This plan is explicitly forbidden to edit anything under `paper/`**, and its own
verification requires `git diff` to touch nothing there. So `claim-labelling` and
`fp-retracted-rule-retained` are reported **partial / unresolved**, not passed. A
dedicated test asserts the occurrence still exists **and** that it is recorded in the
disposition note, so it cannot be quietly dropped.

That file also carries a second staleness: it says the rule is "enforced in
`src/qpd_potential/fold.py` xlim". That comment has been rewritten; the 1e-2 keV limit
survives but is now justified by artifact support, not by the retracted rule. The v1.0
figure's axis was **deliberately not changed** — changing it would alter a v1.0
deliverable, and Phases 12–15 own the v2.0 figures.

## Checkpoint (Task 3, `checkpoint:human-verify`) — self-assessed, pending review

Run autonomously under the standing directive. The four interpretation-bearing outputs,
each with the strongest reason a careful reader could object:

**1. The counting-floor table and its framing.**
*Objection:* the floors are quoted to four significant figures from a Monte Carlo with
N_s = 5000 on a model whose sub-eV yield is a two-decade linear extrapolation. The
precision implies a confidence the physics does not support.
*Response:* the precision is reported because it is what the pipeline produced and it
must be reproducible; the framing block, repeated under every table, is what carries the
confidence statement. **Self-assessment: satisfied.**

**2. The double-count verdict (plan 10-04).**
*Objection:* "may be multiplied" was concluded from P(zero counts) ≈ 0, and that is a
direct consequence of the linear yield with no pair-breaking threshold — the model's
least defensible assumption. The verdict is therefore an artefact of the same weakness
it is being used to license.
*Response:* this is stated in the audit and in this summary in the same breath as the
verdict, with the explicit instruction that Phases 12/15 must re-ask if the yield model
changes. The objection is correct and is carried, not answered.
**Self-assessment: satisfied, with the objection recorded as binding.**

**3. The register's reading of "archived v1.x spectrum".**
*Objection:* the wide reading adds 24 rows the criterion does not compel, and some of
them (`not_a_spectrum`) carry no enforcement at all — bulk that could obscure the five
rows that matter.
*Response:* section 1 of the disposition note states the choice and the reason; the
alternative leaves the CEvNS table untagged, which is the artifact most likely to be
silently extended. **Self-assessment: satisfied.**

**4. The anchor-count reconciliation (plan 10-04).**
*Objection:* 32 ≠ 24 might mean anchors were *added* since v1.0 closed rather than that
the milestone documents miscounted, in which case "unsourced" is too strong.
*Response:* that is examined as candidate origin 1 in the audit and explicitly **not
decidable** from present artifacts; neither reading is asserted, only that no
enumerated list exists and 24 is not reproducible from anything now present.
**Self-assessment: satisfied.**

**Status: recorded as pending researcher review**, following the Phase-5 pattern.

## Verification

- `pytest tests/`: **518 passed, 0 failed.**
- Notebook re-executed after the retraction edit: **0 errors, 32 anchors, 0 CHECK flags.**
- `git status --porcelain paper/`: **empty**. Nothing under `paper/` modified.
- `gpd paper-build` **not run**.
- No frozen artifact header rewritten; the only `data/` churn is the two flux tables'
  `generated:`/`git_sha:` stamps, which the test suite itself rewrites and which the
  guard now verifies are header-only.
