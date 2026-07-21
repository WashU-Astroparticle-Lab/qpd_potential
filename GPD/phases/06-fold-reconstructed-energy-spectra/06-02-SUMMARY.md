# Plan 06-02 SUMMARY — Deliverable figure + finalized assumptions note (STAGE-1 CLOSE)

**Phase:** 06-fold-reconstructed-energy-spectra · **Plan:** 02 · **Status:** completed (Task 2 checkpoint:human-verify self-assessed satisfied pending orchestrator/researcher review; autonomous run). **This plan closes the stage-1 milestone.**

## One-liner

Rendered the stage-1 deliverable figure `reconstructed_energy_spectra.pdf` — dR/dE_rec vs **reconstructed** energy (log-log, counts/kg/day/keV) for all three channels (CEvNS, muon, Compton) and both designs, with the saturation region delimited on the E_rec axis (muon shown reconstructed entirely in the plateau band) and a true→reconstructed mapping panel reusing the Phase-5 curve — and finalized `ASSUMPTIONS.md` (deliv-note): the censoring OPEN switch is retired to the RESOLVED non-paralyzable convention, with a Phase-6 fold addendum and the four standing caveats consolidated.

## What was done

**Task 1 — deliv-fig-spectra** (`fold.py::make_spectra_figure`, `artifacts/stage1/reconstructed_energy_spectra.pdf`)
- Four-panel figure from the committed Plan 06-01 `reconstructed_spectra_{TaAl,AlHf}.csv` + Phase-5 `response_matrix_{TaAl,AlHf}.npz` mapping arrays (no fold re-run):
  - (a,b) Spectra per design: CEvNS/muon/Compton + total, dR/dE_rec vs **E_rec** (log-log), counts/kg/day/keV. CEvNS 1σ flux band, Compton factor-2 site band, muon ±30% band shaded; muon ±30% noted in the caveat box.
  - **Saturation delimited** (fp-no-saturation-mark): on-spot onset (E_dep ~52.9/32.1 eV → E_rec ~23/14 eV) light shade; whole-array plateau (E_dep ~18.6/11.3 keV → E_rec ~4.1/2.5 keV) darker shade; muon pile-up marked at **E_rec ~18.8/15.0 keV** with an annotated arrow — the muon lands inside the plateau band, i.e. reconstructed **entirely under saturation**.
  - (c) True→reconstructed mapping: `E_rec_median_non_paralyzable_eV` vs `E_dep_centers_eV` for both designs (reused from the Phase-5 curve, same content as `energy_response.pdf`), with the `E_rec=0.5·E_dep` linear-calibration line and the onset/plateau E_dep markers.
  - (d) Honest-caveat box: E_rec (not deposited) axis; NO saturated-regime literature anchor (limiting-cases-only); muon pile-up is an instrument artifact, not a spectral line; CEvNS reconstructs to tens of eV; bands legend + non-paralyzable resolved note.
- x-axis is reconstructed energy, not deposited (fp-deposited-only); only the non-paralyzable deliverable is drawn, no paralyzable overlay (fp-paralyzable-swap).
- +2 acceptance tests (`test_make_spectra_figure_renders`, `test_saturation_erec_images_ordered`): full suite **205 passed** (188 prior + 15 fold + 2 new).

**Task 2 — Researcher review checkpoint (checkpoint:human-verify)**
- Autonomous run: self-assessed against the deliverable acceptance and rendered/inspected the PDF. All elements present — 3 channels + total, both designs, counts/kg/day/keV, E_rec axis, saturation delimited, mapping panel, no-anchor caveat, correct physical landing (CEvNS tens of eV, muon saturated tens of keV). Recorded **satisfied pending orchestrator/researcher review**; did not block.

**Task 3 — Finalize ASSUMPTIONS.md (deliv-note)** (`artifacts/stage1/ASSUMPTIONS.md`)
- **Section 4** censoring: OPEN switch **retired → RESOLVED non-paralyzable** (USER DECISION 2026-07-21, CONVENTIONS §F closed); paralyzable = retained sensitivity only. The Phase-5 05-01 addendum limitation (i) inline-flagged **[SUPERSEDED → RESOLVED]** so no live OPEN switch remains in the deliverable framing (fp-note-stale).
- New **Phase-4 gamma-background note**: sourced radiogenic lines (LABChico-anchored, DDEP intra-chain ratios, documented Φ_U=Φ_Th), thin-target single-scatter Compton continuum to the kinematic edges (no photopeaks), factor-2 site band; edges HIGH / total-rate MEDIUM.
- New **Phase-6 fold addendum**: counts-conserving fold through R_non_paralyzable (rel ≤2.2e-16); CEvNS log-log rebin (9.6e-5, above-50-eV 0.12%) + exact 5–10.14 eV low-edge retention via E_rec=0.5·E_dep; uncertainty carry-through (CEvNS 1σ, Compton factor-2, muon ±30%, sub-1.8 MeV ~6–10%); reconstructed landing + report-don't-force verdict; four standing caveats; compact stage-1 results.
- Grep-verified all deliv-note must_contain items present (efficiency ε=0.5, bandwidth non-paralyzable 25 kHz/40 µs, wafer 110 g/per-kg, gamma-background, four caveats, Phase-6 addendum).

## Conventions

| Item | Value |
|---|---|
| Axis | RECONSTRUCTED energy E_rec (keV), NOT deposited (fp-deposited-only) |
| Censoring | non-paralyzable (CONVENTIONS §F, RESOLVED 2026-07-21, canonical); paralyzable sensitivity only |
| Units | dR/dE_rec in counts/kg/day/keV (per-kg; CONVENTIONS A) |
| Energy scale | unified phonon, no quenching; E_rec(low-E)=0.5·E_dep |
| Mapping | reused Phase-5 `E_rec_median_non_paralyzable_eV` vs `E_dep_centers_eV` (not recomputed) |

## Key results (from committed artifacts; figure reads them directly)

| Channel | Ta→Al peak E_rec | Al→Hf peak E_rec | Integrated rate (cts/kg/day) |
|---|---|---|---|
| CEvNS | ~42 eV | ~42 eV | 109.6 |
| muon | 18.8 keV (saturated) | 15.0 keV (saturated) | 1.07×10⁶ |
| Compton | 16.8 keV | 13.3 keV | 2.11×10⁵ |

- Saturation E_rec images ordered per design: onset (~23/14 eV) < plateau (~4.1/2.5 keV) < muon pile-up (18.8/15.0 keV) — a real, ordered band on the E_rec axis. **[CONFIDENCE: HIGH]** — interpolated from the Phase-5 median curve, tested (`test_saturation_erec_images_ordered`).
- Figure regenerates deterministically (byte-identical content) from the committed CSVs + npz. **[CONFIDENCE: HIGH]**.
- Muon lands entirely in saturation; the tens-of-keV pile-up is an instrument artifact with NO saturated-regime literature anchor. **[CONFIDENCE: MEDIUM]** — inherited Phase-5 limiting-cases-only caveat, carried explicitly on the figure and in the note.

## Deviations

None. All guards pass (fp-deposited-only, fp-no-saturation-mark, fp-paralyzable-swap, fp-note-stale). No physics recomputed — figure and note consume frozen Phase-5/06-01 artifacts.

## Files

- `src/qpd_potential/fold.py` (added `make_spectra_figure`; deliv-fig-code)
- `tests/test_fold.py` (+2 tests; 17/17 fold, 205/205 suite)
- `artifacts/stage1/reconstructed_energy_spectra.pdf` (deliv-fig-spectra)
- `artifacts/stage1/ASSUMPTIONS.md` (deliv-note, finalized)

## Self-Check: PASSED

- Files exist; commits 31f8186 (figure+tests+PDF), f9a0fcc (ASSUMPTIONS.md). Full suite 205 passed. Frozen `data/flux/*.csv` restored pristine; working tree clean. All deliv-note must_contain items grep-verified; no live OPEN censoring switch remains.

```yaml
gpd_return:
  status: completed
  phase: "06"
  plan: "02"
  tasks_completed: 3
  tasks_total: 3
  files_written:
    - src/qpd_potential/fold.py
    - tests/test_fold.py
    - artifacts/stage1/reconstructed_energy_spectra.pdf
    - artifacts/stage1/ASSUMPTIONS.md
    - GPD/phases/06-fold-reconstructed-energy-spectra/06-02-SUMMARY.md
  issues:
    - "Task 2 is checkpoint:human-verify — autonomous run: self-assessed satisfied pending orchestrator/researcher review; figure not yet human-approved."
    - "Muon channel reconstructs ENTIRELY under saturation (pile-up ~18.8/15.0 keV E_rec); tens-of-keV pile-up is an instrument artifact with NO saturated-regime literature anchor (inherited Phase-5, limiting-cases-only). Shown explicitly on the figure + note."
    - "CEvNS reconstructs to tens of eV E_rec (peak ~42 eV, ~85% below 100 eV); flagship signal sits very low — surfaced honestly (report-don't-force), not below the 10/50/100 eV thresholds for both designs so stop-condition NOT triggered."
  next_actions:
    - "Orchestrator/researcher: review reconstructed_energy_spectra.pdf against the deliverable acceptance to formally close Task 2 (Y/n/e)."
    - "Stage-1 milestone closed: fold + reconstructed-energy spectra figure + finalized ASSUMPTIONS.md delivered. No further Phase-6 plans."
  decisions:
    - summary: "deliv-fig-spectra rendered: dR/dE_rec vs E_rec (log-log, counts/kg/day/keV), CEvNS/muon/Compton + total, both designs, from the committed 06-01 CSVs; reconstructed axis not deposited (fp-deposited-only); non-paralyzable only, no paralyzable overlay (fp-paralyzable-swap)."
      phase: "06"
    - summary: "Saturation delimited on E_rec axis (fp-no-saturation-mark): onset (E_dep ~52.9/32.1 eV -> E_rec ~23/14 eV) + whole-array plateau (~18.6/11.3 keV E_dep -> ~4.1/2.5 keV E_rec) shaded; muon pile-up marked at 18.8/15.0 keV E_rec, inside the plateau band -> muon shown reconstructed entirely in saturation."
      phase: "06"
    - summary: "Mapping panel reuses Phase-5 E_rec_median_non_paralyzable vs E_dep_centers (both designs) with the 0.5*E_dep calibration line + onset/plateau markers; not recomputed."
      phase: "06"
    - summary: "ASSUMPTIONS.md finalized: censoring OPEN switch retired to RESOLVED non-paralyzable (CONVENTIONS F closed, USER 2026-07-21); Phase-4 gamma-background note + Phase-6 fold addendum added; four caveats + compact stage-1 results (Billard 2.4%, CEvNS ~68/kg/day >50 eV_nr dep, muon 1.37 Hz, pileup 3.3e-5); no live OPEN switch (fp-note-stale)."
      phase: "06"
    - summary: "Stage-1 milestone CLOSED by Plan 06-02."
      phase: "06"
  state_updates:
    record_metric:
      phase: "06"
      plan: "02"
      duration: 360
      tasks: 3
      files: 5
  contract_updates:
    claims_passed:
      - claim-fig-spectra
      - claim-note-final
    acceptance_tests_passed:
      - test-fig-content
      - test-saturation-delimited
      - test-note-content
    forbidden_proxies_rejected:
      - fp-deposited-only
      - fp-no-saturation-mark
      - fp-paralyzable-swap
      - fp-note-stale
```
