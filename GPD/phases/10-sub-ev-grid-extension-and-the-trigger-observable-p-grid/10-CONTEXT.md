# Phase 10 Context — Sub-eV Grid Extension and the Trigger Observable (P-GRID)

**Status:** No `/gpd:discuss-phase` session was run for this phase.
**Recorded:** 2026-07-22, during autonomous roadmap execution.

## Provenance of this file

This file is **not** a transcript of a discussion with the user. It exists to record,
honestly and auditably, what the binding intent for Phase 10 actually is, given that the
user issued a standing session directive to run the roadmap to completion without
per-phase discussion unless a genuine blocker arises.

**No new user decisions were collected while writing this file.** Everything below is
transcribed from artifacts that already existed before this session's planning began
(`GPD/ROADMAP.md`, `GPD/REQUIREMENTS.md`, `GPD/CONVENTIONS.md`, `GPD/STATE.md`,
`GPD/state.json`) or is a numerical fact re-derived from the repository during planning
and labelled as such.

## Decisions (LOCKED — carried from prior artifacts, not newly elicited)

1. **The five ROADMAP Phase 10 success criteria are binding verbatim.** See
   `GPD/ROADMAP.md`, section "### Phase 10: Sub-eV Grid Extension and the Trigger
   Observable (P-GRID)" (lines 200–218). They are the definition of done for this phase.

2. **Phase 10 is untouched by the 2026-07-22 re-scope, deliberately.** The ROADMAP
   re-scope banner states that Phases 10 and 11 are "**Untouched, deliberately** … their
   Goal, Depends-on, Requirements, Contract Coverage, and Success Criteria are unchanged
   byte-for-byte", because the Phase-8 verifier established that neither carries a single
   NUCLEUS anchor. Phase 10's anchors are all project-local or convention-local:
   the v1.0 `shared_energy_grid()` and `R(E_rec|E_dep)` matrices, CONVENTIONS §E/§F
   (ε ≈ 0.5; 25 kHz non-paralyzable, τ_d = 40 µs), the per-sensor saturation onsets
   1.27 eV (Ta→Al) / 0.77 eV (Al→Hf), and the v1.0/v1.1 anchor set.
   **Therefore this phase must not be re-scoped, must not fold in surface/shielding
   considerations, and must not depend on Phase 9.** Its only roadmap dependency is
   Phase 8 (the gate, now discharged); it runs in parallel with Phase 9.

3. **Requirements CALC-13 and CALC-16** are the requirements this phase advances. See
   `GPD/REQUIREMENTS.md` lines 27 and 30. CALC-13 gates all sub-eV work downstream
   (`REQUIREMENTS.md` ordering constraints, line 157).

4. **Spectra run down to 100 meV.** The earlier "never display below 10 eV" project
   display rule is **retracted**; retracting it is the point of this phase, not something
   to re-litigate. The retracted rule survives verbatim in
   `notebooks/paper_calculations.ipynb` (final cell) and must be removed or restated
   as history, never carried forward as a physics statement.

5. **Forbidden proxies are binding**, from the same ROADMAP section:
   - `fp-poisson-as-resolution` — the counting-statistics floor is an emergent best case,
     not a resolution model. The project has **no resolution parameter anywhere**.
   - Silent clamping or extrapolation at a table floor.
   - Treating the trigger sigmoid as a *replacement* for ε ≈ 0.5 rather than a factor
     multiplied on top of it.
   - Retaining the retracted "never display below 10 eV" rule as a physics statement.

6. **Stop-condition (ROADMAP line 435).** If the regenerated `R(E_rec|E_dep)` breaks
   count conservation (>1e-3) or any v1.0/v1.1 anchor stops reproducing, revisit the
   grid extension **before any spectrum is produced on it**. Do not proceed and
   compensate downstream.

7. **Evidence discipline (carried from Phase 8).** Every quoted number must be traceable
   to a locally frozen artifact via a recorded, reproducible command. `WebFetch` produced
   two verified factual errors during Phase 8 and **must not be used as a quote source**
   in this phase. Phase 10 is in any case fully local: it needs no external retrieval.

## Numerical facts established during planning (re-derived, not asserted)

These were computed from the repository while writing the plans and are recorded here so
the executor does not have to rediscover them. Each is reproducible from
`src/qpd_potential/muon_deposit.py::shared_energy_grid`.

- The v1.0 grid is `shared_energy_grid(e_lo_kev=1e-2, e_hi_kev=2e5, bins_per_decade=80)`
  → `nbins = round(log10(2e7) * 80) = 584`, 585 edges, floor exactly 10 eV, **first bin
  centre 10.144973 eV** (this is the "10.14 eV" quoted throughout the project).
  The realised spacing is `log10(2e7)/584 = 0.0125017637` dex/bin = **79.9887 bins/decade**,
  not exactly 80 — the `round()` makes "80/decade" nominal.
- **The naive extension `shared_energy_grid(e_lo_kev=1e-4)` gives the right bin count
  (744) but is NOT a superset of the v1.0 grid.** Its spacing is
  `log10(2e9)/744 = 0.0125013844` dex/bin, and the overlapping edges drift from the v1.0
  edges by up to **5.102e-4 relative**. Any archived v1.x spectrum placed on that axis
  would be silently reinterpolated — which ROADMAP success criterion 2 forbids.
- **The alignment-preserving construction works and is unique.** Prepending 160 bins at
  the *v1.0* spacing gives 744 bins / 745 edges, floor **0.0999350 eV** (≤ 0.1 eV, so the
  axis does reach 0.1 eV), first bin centre **0.1013838 eV**, and reproduces the v1.0
  edge array **exactly**: `np.array_equal(new_edges[160:], old_edges)` is `True`,
  max absolute difference `0.0`. 159 bins would put the floor at 0.10285 eV, above
  0.1 eV, and fail success criterion 1. This satisfies "runs from 0.1 eV at 80
  bins/decade (~744 bins)" literally while keeping success criterion 2 achievable.
- **`R(E_rec|E_dep)`'s deposit axis is currently read from an archived CSV, not from the
  grid function.** `response_matrix.load_E_dep_grid_eV()` parses
  `data/combined_dRdEdep.csv`. Regenerating `R` on the extended axis therefore requires
  decoupling that axis from the archived Phase-4 product; re-running the Phase-4 muon
  and Compton Monte Carlo is **Phase 15's** job, not Phase 10's.
- **The "24 anchors" count is not reproducible from a static read.**
  `notebooks/paper_calculations.ipynb` contains **22 literal `check(...)` call sites**,
  several of them inside loops over designs or gamma lines, so the number of anchor lines
  *emitted at runtime* is larger than 22. The figure "24" appears as a claim in
  `GPD/MILESTONES.md` line 41 and `GPD/milestones/v1.0-MILESTONE-AUDIT.md` lines 17/77,
  with no enumerated list anywhere. This must be resolved by running the notebook and
  counting emitted anchor lines, and any discrepancy reported — **not force-fitted to 24.**

## Agent's Discretion

- Module decomposition, file layout, and test design.
- The functional form and width of the trigger sigmoid, subject to the 50%-point
  constraint being exactly 0.5 eV. The width is **not** fixed by any project artifact and
  must be an exposed, documented, scannable parameter in the style of
  `params.F_PROMPT` / `params.R_SPOT`, never a silently hard-coded number.
- Which interpolators count as "every interpolator" for success criterion 3, provided the
  enumeration is produced mechanically (a recorded grep over `src/`), the inclusion or
  exclusion of each hit is justified in writing, and no tabulated-input interpolator that
  the extended grid can drive below its table floor is omitted.
- Where the regenerated response matrices are written, provided the v1.0
  `artifacts/stage1/response_matrix_*.npz` files are **not** overwritten (the anchor
  notebook loads them, and success criterion 2 forbids silent replacement of legacy
  artifacts).

## Deferred / Out of Scope

- Any Phase 11 work: ω̄, the Debye–Waller convention, and the impulse-approximation
  broadening σ_E = √(E_R ω̄). Phase 10 must **quote the Phase-11 broadening as absent and
  comparable in size**, and must not implement it.
- Producing any physics spectrum on the extended grid. Phase 10 builds and validates the
  axis, the response, and the observable definition; Phases 12–15 produce spectra on it.
- Re-running the Phase-4 deposited-energy Monte Carlo onto the extended grid (Phase 15).
- Any edit to the paper. Per the standing project note, `paper/qpd_reactor_cevns_spectra.tex`
  was hand-refactored and **`gpd paper-build` must not be re-run**.
- Any change to CONVENTIONS §E (ε ≈ 0.5) or §F (non-paralyzable, 40 µs). The trigger
  curve is a **new** analysis efficiency added alongside them, not a modification of them.

## Open items carried into execution

- **Confirmation pressure is a live failure mode here.** In Phase 8, three errors pointed
  in the direction that favoured the expected conclusion, and a fourth surfaced only when
  a verifier was explicitly told to hunt for one. The comfortable outcome for Phase 10 is
  "the grid extended cleanly and all anchors still reproduce." Every plan therefore
  carries at least one check whose *failure* is the informative result: the exact-superset
  assertion (10-03), the pre-fix witness test that the interpolators currently clamp
  (10-01), the ε-perturbation test that the sigmoid has not replaced ε (10-02), and the
  anchor-count audit against the unsourced "24" (10-04).
- **The deepest weakness of the extension is physical, not numerical, and Phase 10 cannot
  fix it — only label it.** `energy_scale.n_qp_yield` is exactly linear,
  `N_qp = ε·E_sensor/Δ_tr`, with no pair-breaking threshold and no discreteness. At a
  0.1 eV deposit the off-spot per-sensor share is ≈ 6.8 µeV, far below the Al trap gap
  Δ_tr ≈ 190 µeV, so the model assigns ≈ 0.018 quasiparticles to a sensor that could not
  energetically host one. The sub-eV response is therefore a mean-field continuum
  extrapolation two decades below where it was ever validated. This is precisely why the
  user chose a trigger-probability observable below ~1 eV, and it must appear as a stated
  limitation on every sub-eV deliverable rather than being quietly carried.
- **At 0.1 eV the counting floor rests on N_obs ≈ 8–10 events**, where the Gaussian
  1/√N label is itself marginal. The 35.6% / 31.6% figures should be reported with that
  caveat attached.
