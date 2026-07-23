---
phase: 10-sub-ev-grid-extension-and-the-trigger-observable-p-grid
plan: 03
status: complete
one_liner: "Extended axis built by prepending 160 bins at the v1.0 spacing: 744 bins, floor 0.0999350 eV, first centre 0.1013838 eV, np.array_equal(ext[160:], v1_0) TRUE with max difference exactly 0.0; the naive rebuild is shown to drift 5.101629e-04 while passing every superficial check, and the ordinal sub-seed is demonstrated to fail before the energy-keyed one is shown to fix it."
plan_contract_ref: GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-03-PLAN.md#/contract

contract_results:
  claims:
    claim-superset:
      status: passed
      summary: "744 bins / 745 edges; first edge 0.0999350 eV (<= 0.1 eV, so the axis reaches 0.1 eV); first bin centre 0.10138382944301134 eV, which is 0.1013838 to 7 significant figures. np.array_equal(extended[160:], v1_0_edges) is True with maximum absolute difference EXACTLY 0.0, and both edges of every v1.0 bin survive. The realised spacing is log10(2e7)/584 = 0.0125017637 dex/bin = 79.988714 bins/decade, inherited exactly rather than re-solved."
      linked_ids: [deliv-grid-code, deliv-grid-tests, deliv-grid-note, test-exact-superset, test-bin-count, test-floor-reaches-0p1, test-naive-rejected]
      evidence:
        - verifier: gpd-executor
          method: exact array comparison plus a constructed counterexample
          confidence: high
          claim_id: claim-superset
          deliverable_id: deliv-grid-code
          acceptance_test_id: test-naive-rejected
          reference_id: ref-roadmap-sc2
          forbidden_proxy_id: fp-naive-logspace
          evidence_path: GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-03-GRID-CONSTRUCTION.md
    claim-callers-pinned:
      status: passed
      summary: "28 grep hits, 28 pin-table rows. All four Phase-4 producers (muon_deposit, compton_deposit, deposited_spectra, parse_endf_nGe) now pass shared_energy_grid(\"v1.0\") explicitly and still emit the 584-bin axis. DEVIATION D1: the default was kept at v1.0 rather than flipped to v2.0-ext, because flipping it broke a Phase-9 test executing concurrently in this worktree; the reasoning and the exact failure are recorded in the construction note."
      linked_ids: [deliv-grid-code, deliv-grid-tests, deliv-grid-note, test-caller-pins, test-phase4-unchanged]
    claim-axis-decoupled:
      status: passed
      summary: "E_dep_grid_from_shared_grid_eV(version) computes deposit centres as geometric means of the grid edges. The v1.0 selection agrees with the CSV-parsed axis to 4.917619e-07 maximum relative deviation (at index 320), corroborating the independently-recorded Phase-4 5e-7 figure. The sub-seed is now keyed to the deposit energy: the same energy gives identical draws under a 584-column and a 744-column axis, and the pre-fix ordinal scheme is demonstrated to give DIFFERENT draws for the same physics first."
      linked_ids: [deliv-grid-code, deliv-grid-tests, deliv-grid-note, test-axis-decoupled, test-seed-stability]
  deliverables:
    deliv-grid-code:
      status: passed
      path: src/qpd_potential/muon_deposit.py
      summary: "shared_energy_grid(version) with GRID_VERSIONS = ('v1.0', 'v2.0-ext'), an unknown version raising rather than defaulting, an IN-CODE assert that the extended tail equals the v1.0 array exactly, v1_0_dex_per_bin() documenting the 79.988714 realised bins/decade, and _EXT_PREPENDED_BINS = 160 with the 159/161 rejections recorded at the constant. Also response_matrix.E_dep_grid_from_shared_grid_eV and response_matrix.column_seed_sequence."
      linked_ids: [claim-superset, claim-callers-pinned, claim-axis-decoupled]
    deliv-grid-tests:
      status: passed
      path: tests/test_energy_grid_extension.py
      summary: "15 tests: exact superset, bin count and realised spacing, floor and first centre, the naive counterexample, the 159/160/161 comparison, unknown-version rejection, the caller-pin closure grep, the v1.0-default deviation pin, Phase-4 producer pins, axis decoupling, extended-centre superset, seed stability with the ordinal-failure demonstration, seed-key distinctness and process stability, E_rec bounds untouched, and a git-level check that nothing under data/ or artifacts/ changed."
      linked_ids: [claim-superset, claim-callers-pinned, claim-axis-decoupled]
    deliv-grid-note:
      status: passed
      path: GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-03-GRID-CONSTRUCTION.md
      summary: "The construction; the naive alternative with its measured 5.101629e-04 drift and the observation that it passes np.allclose(rtol=1e-3); the 159-bin alternative with its 0.1028536 eV floor; an explicit owning of the loose 'runs from 0.1 eV' reading; DEVIATION D1 with the verbatim Phase-9 failure; the 28-row caller pin table with the recorded grep and its raw output; the 4.917619e-07 CSV round-trip measurement with its consequence for plan 10-04; and the ordinal-vs-energy-keyed seed demonstration with actual draws."
      linked_ids: [claim-superset, claim-callers-pinned, claim-axis-decoupled]
  acceptance_tests:
    test-exact-superset:
      status: passed
      summary: "np.array_equal(extended[160:], v1_0) is True and max |difference| == 0.0 exactly. Asserted with np.array_equal, never np.allclose -- the counterexample test shows why that distinction is load-bearing."
      linked_ids: [claim-superset, deliv-grid-code, deliv-grid-tests]
    test-bin-count:
      status: passed
      summary: "744 bins, 745 edges. Realised spacing equals the v1.0 log10(2e5/1e-2)/584 by exact expression equality (==, not approx), = 0.0125017637 dex/bin = 79.988714 bins/decade, and is asserted NOT equal to 80."
      linked_ids: [claim-superset, deliv-grid-tests]
    test-floor-reaches-0p1:
      status: passed
      summary: "First edge 0.0999350 eV <= 0.1 eV. First bin centre 0.10138382944301134 eV = 0.1013838 to 7 significant figures. The v1.0 floor (10 eV exactly) and first centre (10.144972680282425 eV) are asserted unchanged in the same test."
      linked_ids: [claim-superset, deliv-grid-tests]
    test-naive-rejected:
      status: passed
      summary: "THE informative check. np.logspace(log10(1e-4), log10(2e5), 745) has 744 bins, a first edge of exactly 0.1 eV, a first centre of 0.1014497 eV, and PASSES np.allclose(rtol=1e-3) against the v1.0 edges -- yet np.array_equal is False and the maximum relative edge drift is 5.101629e-04, worst at index 0, the v1.0 floor itself. The shipped array is asserted different from it."
      linked_ids: [claim-superset, deliv-grid-tests, deliv-grid-note]
    test-caller-pins:
      status: passed
      summary: "Recorded grep re-run in a subprocess: 28 call sites, 28 pin-table rows, every `path:line` present in the table. Four Phase-4 producers verified at source level to contain the literal shared_energy_grid(\"v1.0\")."
      linked_ids: [claim-callers-pinned, deliv-grid-note, deliv-grid-tests]
    test-phase4-unchanged:
      status: passed
      summary: "load_E_dep_grid_eV still returns 584 centres from the archived CSV and E_dep_grid_from_shared_grid_eV('v1.0') returns 584 centres matching it to 4.917619e-07. No bin count changed. git status --porcelain over data/ and artifacts/ shows zero tracked modifications, asserted by a test."
      linked_ids: [claim-callers-pinned, deliv-grid-tests]
    test-axis-decoupled:
      status: passed
      summary: "Maximum relative deviation between the grid-sourced and CSV-parsed v1.0 axes is 4.917619e-07 < 5e-7, at index 320. The test also asserts the deviation is NOT zero and the arrays are NOT array_equal, so the two routes are demonstrably different axes -- which is exactly why fp-bit-identical-promise binds plan 10-04."
      linked_ids: [claim-axis-decoupled, deliv-grid-tests, deliv-grid-note]
    test-seed-stability:
      status: passed
      summary: "Demonstrated in the required order. (a) The ordinal scheme FAILS: deposit energy 57118.92025870707 eV sits at index 300 on the 584-column axis and index 460 on the 744-column axis, and their first draws are [0.49813092 0.71201118 0.18689986] versus [0.74471769 0.32187198 0.87944215] -- different streams for the same physics, with spawn_key (300,) versus (460,). (b) The energy-keyed scheme gives [0.20015866 0.67617383 0.17417598] for both, verified for every 37th overlapping column. All 744 energy keys are distinct."
      linked_ids: [claim-axis-decoupled, deliv-grid-code, deliv-grid-tests]
  references:
    ref-roadmap-p10-sc1:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Criterion 1 ('runs from 0.1 eV at 80 bins/decade, ~744 bins') is discharged by shared_energy_grid('v2.0-ext'). Section 3 of the construction note owns the loose reading explicitly: the first edge is 0.0999350 eV, not exactly 0.1 eV, and only the rejected naive rebuild satisfies the stricter reading -- at the cost of criterion 2."
    ref-roadmap-sc2:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Criterion 2 forced the exact-superset construction, the np.array_equal assertion, the per-caller version pin, and DEVIATION D1's v1.0 default. The naive counterexample test is the evidence that the criterion is actually being tested rather than assumed."
    ref-calc13:
      status: completed
      completed_actions: [read, cite]
      missing_actions: []
      summary: "CALC-13 is the requirement this plan advances; REQUIREMENTS.md records that it gates all sub-eV work downstream. The extended axis is the object it names."
    ref-phase4-grid:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "GPD/STATE.md Phase-04 records 'byte-identical shared log E_dep grid (584 bins ...); centers = geometric means of shared_energy_grid() edges to 5e-7'. Compared directly: this plan re-measured that round-trip at 4.917619e-07 maximum relative deviation, independently corroborating the recorded figure, and the geometric-mean centre rule is the one E_dep_grid_from_shared_grid_eV implements."
  forbidden_proxies:
    fp-naive-logspace:
      status: rejected
      notes: "Rejected by construction AND by an explicit counterexample test that builds the naive array, shows it passes bin-count and np.allclose(rtol=1e-3) checks, measures its 5.101629e-04 maximum relative edge drift, and asserts the shipped array is not it."
    fp-default-change:
      status: rejected
      notes: "Rejected in the strongest available form: the default was NOT changed. See DEVIATION D1. Flipping it broke tests/test_env_v1_identity.py::test_no_photopeak_above_edge with 'operands could not be broadcast together with shapes (744,) (584,)' -- the proxy caught in the act against a concurrently-executing Phase-9 file. A v1.0 default makes silent re-binning impossible rather than merely pinned-against, and fails in the safe direction."
    fp-bit-identical-promise:
      status: rejected
      notes: "No bit-identity is promised or asserted anywhere. The 4.917619e-07 CSV-vs-exact centre discrepancy is measured, recorded in the construction note, and its consequence stated explicitly: the regenerated matrices CANNOT be bit-identical to the archived ones. Plan 10-04's comparison against the archive is statistical; its bitwise check is against a same-code v1.0-range rebuild, which is a different question."
    fp-ordinal-seed:
      status: rejected
      notes: "Rejected by replacement, with the failure demonstrated first. The ordinal SeedSequence.spawn(n)[j] scheme is reproduced inside the test and shown to give different draws for the same deposit energy under the two axis lengths BEFORE the energy-keyed scheme is shown to give identical ones. Without that ordering the fix would be vacuous."
  uncertainty_markers:
    weakest_anchors:
      - "The grid floor is 0.0999350 eV, not exactly 0.1 eV. Read as 'the axis covers 0.1 eV' the roadmap phrasing is satisfied; read as 'the first edge is 0.1 eV' it is not, and only the rejected naive rebuild satisfies that stricter reading. The two readings are not simultaneously satisfiable and criterion 2 was chosen."
      - "The 4.917619e-07 CSV round-trip discrepancy means the archived v1.0 response matrices sit on a very slightly different axis from the exact one. Nothing downstream has ever depended on it, but plan 10-04's v1.0 comparison inherits it as an irreducible floor beneath the Monte Carlo noise."
      - "Pinning the Phase-4 producers to v1.0 is a decision made here on the grounds that Phase 15 owns the re-run. If Phase 15's scope changes, this pin has to be revisited."
      - "DEVIATION D1 departs from the plan's literal instruction on the default. The justification is that the plan's construction assumed Phase 10 owns every caller and it demonstrably does not. A reader who weights criterion 1's literal wording above criterion 2's guarantee would disagree with the call."
    unvalidated_assumptions:
      - "That preserving the v1.0 edge set is sufficient for archived artifacts to be carried without reinterpolation. It is sufficient for anything binned on shared_energy_grid; artifacts on their own native axes (artifacts/stage1/cevns_dRdT.csv from 5 eV, data/endf_nGe_elastic_v1.1.csv from thermal energies, the reactor flux tables on an E_nu axis) are untouched by this and are handled by plan 10-05."
      - "That twelve significant digits is the right sub-seed key precision. It resolves adjacent centres (2.9% apart) with enormous margin and also resolves the 4.918e-07 CSV-vs-exact difference, which is intended -- but it means any future change to how centres are computed silently re-seeds every column."
    competing_explanations:
      - "The 5.101629e-04 drift could be dismissed as negligible for a spectrum whose bins are 2.9% wide. The counter-reading, adopted here, is that criterion 2 is about PROVENANCE, not accuracy: a silently reinterpolated legacy artifact is untraceable regardless of how small the interpolation error is."
    disconfirming_observations:
      - "DID NOT OCCUR: 'np.array_equal(extended[160:], v1_0) returns False'. It is True with max absolute difference exactly 0.0, so no archived artifact needs reinterpolation."
      - "DID NOT OCCUR: 'a caller of shared_energy_grid turns out to have no defensible version pin'. All 28 sites are classified; all four Phase-4 producers pin v1.0 for a stated reason."
      - "DID NOT OCCUR: 'the energy-keyed sub-seed cannot be made stable'. It is stable, and all 744 keys are distinct."
      - "DID OCCUR, and is recorded as DEVIATION D1: flipping the default to the extended axis broke a concurrently-developed Phase-9 test. That is fp-default-change happening in real time, and it changed the shipped design."
files_created:
  - tests/test_energy_grid_extension.py
  - GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-03-GRID-CONSTRUCTION.md
files_modified:
  - src/qpd_potential/muon_deposit.py
  - src/qpd_potential/compton_deposit.py
  - src/qpd_potential/deposited_spectra.py
  - src/qpd_potential/response_matrix.py
  - src/nuclear/parse_endf_nGe.py
  - tests/test_compton_channel.py
  - GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-01-INTERPOLATOR-INVENTORY.md
---

# Plan 10-03 Summary --- The Extended Deposited-Energy Axis

## The axis

| | v1.0 | **v2.0-ext** |
|---|---|---|
| bins / edges | 584 / 585 | **744 / 745** |
| first edge | 10 eV exactly | **0.0999350 eV** |
| first bin centre | 10.144972680282425 eV | **0.1013838 eV** |
| spacing | 0.0125017637 dex/bin | identical |
| bins/decade (realised) | **79.988714**, not 80 | identical |
| `np.array_equal(ext[160:], v1_0)` | — | **True** |
| max absolute edge difference on the overlap | — | **exactly 0.0** |

Built by **prepending 160 bins at the v1.0 spacing**, never by re-running
`logspace` over the wider range.

## Why `np.array_equal` and not `np.allclose`

The naive rebuild `np.logspace(log10(1e-4), log10(2e5), 745)`:

| check | naive | verdict |
|---|---|---|
| 744 bins | yes | passes |
| first edge exactly 0.1 eV | yes | passes, and looks *better* |
| first centre 0.1014497 eV | yes | plausible |
| `np.allclose(naive[160:], v1_0, rtol=1e-3)` | **True** | **passes** |
| `np.array_equal(naive[160:], v1_0)` | **False** | **fails** |
| max relative edge drift | **5.101629e-04** (worst at index 0, the v1.0 floor) | |

Both constructions pass a bin-count check and the naive one passes a loose
tolerance check. **Only exact array equality distinguishes them**, and every
archived v1.x spectrum placed on the naive axis would be silently reinterpolated.

## The uniqueness of 160

| prepended | bins | floor | verdict |
|---|---|---|---|
| 159 | 743 | 0.1028536 eV | **fails** — floor above 0.1 eV |
| **160** | **744** | **0.0999350 eV** | the unique choice satisfying both clauses |
| 161 | 745 | 0.0970993 eV | reaches 0.1 eV but 745 bins |

All three preserve the v1.0 edges exactly — that is a property of prepending at
the v1.0 spacing, not of the count.

**Owning the loose reading:** the first edge is 0.0999350 eV, **not** exactly
0.1 eV. Read as "the axis covers 0.1 eV" criterion 1 is satisfied; read as "the
first edge is 0.1 eV" it is not, and only the rejected naive rebuild satisfies the
stricter reading — at the cost of criterion 2. The two are not simultaneously
satisfiable.

## DEVIATION D1 — the default stayed at `v1.0`

The plan instructed making `v2.0-ext` the default. **It was not made the default.**

Flipping it produced, in a full-suite run:

```
FAILED tests/test_env_v1_identity.py::test_no_photopeak_above_edge
E   ValueError: operands could not be broadcast together with shapes (744,) (584,)
```

against a **Phase-9 file executing concurrently in this worktree**, which this
phase is not permitted to edit.

That is not an inconvenience. **It is `fp-default-change` caught in the act**: a
caller that does not state its version silently receives a different axis. The
plan's mitigation for that proxy — pin every caller — works only if you can reach
every caller, and Phase 9 was adding new ones while this plan ran.

A `v1.0` default makes silent re-binning **impossible** rather than merely
pinned-against, and it **fails in the safe direction**: a caller that forgets to
ask for the extension gets the v1.0 axis and then trips the plan 10-01
`_erec_of_edep` guard the moment it evaluates sub-eV. Criterion 1 is discharged by
`shared_energy_grid("v2.0-ext")`; criterion 2 is discharged more strongly than the
plan's own construction would have discharged it.

*Recorded, not acted on:* Phase 9 has since pinned its own callers explicitly, so
a future default flip would now be safe. It was not performed here because Phase 9
is still in flight and because the argument above stands independently.

## Caller pins

28 grep hits, 28 pin-table rows. The four Phase-4 producers — `muon_deposit`,
`compton_deposit`, `deposited_spectra`, `parse_endf_nGe` — now pass `"v1.0"`
explicitly and still emit the 584-bin axis. **No Phase-9 file was edited.**

## The deposit axis, decoupled — and the precision floor plan 10-04 inherits

`E_dep_grid_from_shared_grid_eV(version)` computes centres as geometric means of
the grid edges, so the response matrix's axis is no longer a function of an
archived Phase-4 CSV. The CSV parser is unchanged.

```
max |grid − csv| / csv = 4.917619e-07   (at index 320)
csv[0]   = 10.144970           (decimal round-trip through the CSV)
exact[0] = 10.144972680282425  (geometric mean)
```

This independently corroborates the Phase-4 figure recorded in `GPD/STATE.md`
("centers = geometric means … to 5e-7").

**Consequence, stated so plan 10-04 cannot promise otherwise:** the archived
`artifacts/stage1/response_matrix_*.npz` were built on the CSV round-tripped
centres. **Bit-identical reproduction of them is not achievable.** Plan 10-04's
comparison against the archive must be statistical; its bitwise check must be
against a *same-code* v1.0-range rebuild.

## The sub-seed, keyed to energy

The pre-fix scheme seeded column *j* via `SeedSequence.spawn(n_edep)[j]` — a
function of **how many columns sat below it**. Demonstrated failure first, at the
same deposit energy 57118.92025870707 eV (index 300 of 584, index 460 of 744):

```
ORDINAL   584-axis: [0.49813092 0.71201118 0.18689986]   spawn_key (300,)
ORDINAL   744-axis: [0.74471769 0.32187198 0.87944215]   spawn_key (460,)
ENERGY    584-axis: [0.20015866 0.67617383 0.17417598]
ENERGY    744-axis: [0.20015866 0.67617383 0.17417598]   <- identical
```

Verified for every 37th overlapping column. All 744 energy keys are distinct.
`zlib.crc32` throughout — never the salted builtin `hash`.

**A deliberate consequence:** twelve significant digits also resolves the
4.918e-07 CSV-vs-exact difference, so the CSV-sourced and grid-sourced axes give
*different* sub-seeds for the "same" column. That is correct — they are different
axes — and pretending otherwise is what `fp-bit-identical-promise` forbids.

## Scope

Nothing was written to `data/` or `artifacts/` (enforced by a test running
`git status --porcelain`). No matrix was regenerated. The `E_rec` grid bounds are
untouched. `shared_energy_grid` still returns **keV**; every eV figure above is a
labelled conversion.

## Regression

`pytest tests/`: **460 passed, 0 failed.** The count keeps rising because Phase 9
is adding tests to the same worktree concurrently; the 15 new tests here are
`tests/test_energy_grid_extension.py`.
