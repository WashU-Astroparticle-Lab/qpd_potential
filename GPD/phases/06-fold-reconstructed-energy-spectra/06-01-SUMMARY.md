---
phase: 06-fold-reconstructed-energy-spectra
plan: "01"
plan_contract_ref: GPD/phases/06-fold-reconstructed-energy-spectra/06-01-PLAN.md#/contract
title: "Fold pipeline: reconstructed-energy spectra dR/dE_rec (CEvNS + muon + Compton, both designs) via the non-paralyzable response matrix"
date: 2026-07-21
status: completed
depth: full
completed: 2026-07-21
one_liner: "Folded the frozen CEvNS, muon, and Compton deposited-energy spectra through the non-paralyzable response matrix R(E_rec|E_dep) for both designs to produce reconstructed-energy spectra dR/dE_rec, conserving counts per channel to ~1e-16 (CEvNS rebin to <1e-4), with the muon MeV deposits correctly saturating to a bounded ~18.8/15.0 keV plateau and the CEvNS 5-10.14 eV low edge retained via E_rec=0.5*E_dep."
provides:
  - "qpd_potential.fold — counts-conserving CEvNS rebin onto the shared E_dep grid + non-paralyzable fold of all three channels into dR/dE_rec for both designs"
  - "Reconstructed-energy spectra CSVs reconstructed_spectra_{TaAl,AlHf}.csv (per-channel dR/dE_rec + bands + total)"
  - "tests/ fold acceptance suite (counts conservation, E_rec axis, CEvNS rebin, low-edge retained)"
contract_results:
  claims:
    claim-fold-conserves:
      status: passed
      summary: "Folding the frozen CEvNS/muon/Compton deposited spectra through the non-paralyzable response matrix R(E_rec|E_dep) for both designs conserves counts per channel to ~1e-16 (CEvNS counts-conserving rebin to <1e-4: total 109.587 vs trapezoidal 109.597, rel 9.6e-5; above-50-eV 67.67 vs frozen 67.752, 0.12%); the muon MeV deposits saturate to a bounded ~18.8/15.0 keV plateau. Only the non-paralyzable R is folded (CONVENTIONS Sec F canonical); paralyzable retained only as a labeled sensitivity."
      linked_ids: [deliv-fold-code, deliv-recon-csv-taal, deliv-recon-csv-alhf, deliv-fold-tests, test-counts-conservation, test-erec-axis, test-cevns-rebin]
    claim-cevns-lowedge:
      status: passed
      summary: "The CEvNS 5-10.14 eV low edge is retained (7.27 counts/kg/day, not dropped) and reconstructed via the exact linear E_rec=0.5*E_dep mapping (E_rec ~ 2.5-5.0 eV), since these deposits lie far below the ~52.9/32.1 eV crossover onset."
      linked_ids: [deliv-fold-code, deliv-recon-csv-taal, deliv-recon-csv-alhf, deliv-fold-tests, test-cevns-rebin, test-lowedge-retained]
  deliverables:
    deliv-fold-code:
      status: passed
      path: src/qpd_potential/fold.py
      summary: "Fold pipeline: counts-conserving CEvNS rebin (piecewise log-log power-law), non-paralyzable fold N_rec = R @ N_dep of all three channels for both designs, band propagation."
      linked_ids: [claim-fold-conserves, claim-cevns-lowedge]
    deliv-recon-csv-taal:
      status: passed
      path: artifacts/stage1/reconstructed_spectra_TaAl.csv
      summary: "Ta->Al reconstructed-energy spectra: E_rec_keV + per-channel dR/dE_rec + bands + total (counts/kg/day/keV) with provenance header."
      linked_ids: [claim-fold-conserves, claim-cevns-lowedge]
    deliv-recon-csv-alhf:
      status: passed
      path: artifacts/stage1/reconstructed_spectra_AlHf.csv
      summary: "Al->Hf reconstructed-energy spectra: E_rec_keV + per-channel dR/dE_rec + bands + total (counts/kg/day/keV) with provenance header."
      linked_ids: [claim-fold-conserves, claim-cevns-lowedge]
    deliv-fold-tests:
      status: passed
      path: tests/test_fold.py
      summary: "Fold acceptance suite: counts conservation, E_rec axis, CEvNS rebin closure, low-edge retention."
      linked_ids: [claim-fold-conserves, claim-cevns-lowedge]
  acceptance_tests:
    test-counts-conservation:
      status: passed
      summary: "Per-channel counts are conserved through the non-paralyzable fold to ~1e-16 (N_rec sum == N_dep sum)."
      linked_ids: [claim-fold-conserves, deliv-fold-code]
    test-erec-axis:
      status: passed
      summary: "The output spectra are on the reconstructed-energy axis E_rec (dR/dE_rec), not the deposited axis."
      linked_ids: [claim-fold-conserves, deliv-fold-code]
    test-cevns-rebin:
      status: passed
      summary: "CEvNS dR/dT rebinned onto the shared E_dep grid conserves counts to <1e-4 (109.587 vs 109.597, rel 9.6e-5; above-50-eV 67.67 vs 67.752, 0.12%)."
      linked_ids: [claim-fold-conserves, claim-cevns-lowedge, deliv-fold-code]
    test-lowedge-retained:
      status: passed
      summary: "The CEvNS 5-10.14 eV low edge (7.27 counts/kg/day) is retained and mapped via E_rec=0.5*E_dep, not dropped."
      linked_ids: [claim-cevns-lowedge, deliv-fold-code]
  forbidden_proxies:
    fp-deposited-only:
      status: rejected
      notes: "The output spectra are on the reconstructed E_rec axis (dR/dE_rec) via the response matrix, not left on the deposited scale."
    fp-drop-lowE-cevns:
      status: rejected
      notes: "The CEvNS 5-10.14 eV low edge (7.27 counts/kg/day) is explicitly retained via E_rec=0.5*E_dep, not truncated."
    fp-paralyzable-swap:
      status: rejected
      notes: "Only the non-paralyzable R (CONVENTIONS Sec F canonical) is folded into the deliverables; paralyzable is retained only as a labeled sensitivity, not swapped in."
  uncertainty_markers:
    weakest_anchors:
      - "The saturated-regime muon plateau (~18.8/15.0 keV) has no literature anchor; validated by limiting cases only"
      - "The CEvNS low-recoil bins inherit the Phase-2 sub-1.8 MeV flux placeholder"
    unvalidated_assumptions:
      - "The non-paralyzable censoring convention is canonical (paralyzable carried only as sensitivity)"
    competing_explanations:
      - "A paralyzable response would roll the muon deposits over rather than plateau, changing the high-E_rec pileup shape"
    disconfirming_observations:
      - "Non-conservation of counts through the fold, or the CEvNS low edge being dropped, would break the pipeline (checked false: ~1e-16 conservation, low edge retained)"
---

# Plan 06-01 SUMMARY — Fold pipeline: reconstructed-energy spectra

**Phase:** 06-fold-reconstructed-energy-spectra · **Plan:** 01 · **Status:** completed (Task 3 checkpoint self-assessed satisfied pending orchestrator/researcher review; autonomous run)

## One-liner

Folded the frozen CEvNS, muon, and Compton **deposited**-energy spectra through the non-paralyzable response matrix R(E_rec|E_dep) for both designs to produce **reconstructed**-energy spectra dR/dE_rec, conserving counts per channel to ~1e-16 (CEvNS rebin to <1e-4), with the muon MeV deposits correctly saturating to a bounded ~18.8/15.0 keV plateau and the CEvNS 5–10.14 eV low edge retained via E_rec=0.5·E_dep.

## What was done

**Task 1 — CEvNS counts-conserving rebin** (`src/qpd_potential/fold.py::rebin_cevns_to_edep_grid`)
- `cevns_dRdT.csv` (320-pt recoil grid, 5–3200 eV_nr) rebinned onto the shared 584-bin E_dep grid by integrating dR/dT over each shared bin with a **piecewise log-log power-law** interpolant (not linear-space), which re-partitions the integral and conserves counts.
- Cross-checks: total rebinned counts **109.587** vs trapezoidal reference **109.597** → rel **9.6e-5** (<1%); above-50-eV **67.67** vs frozen header **67.752** → **0.12%** (<2%).
- Low edge (5 → 10.0 eV grid floor): **7.27 counts/kg/day** retained (not dropped, fp-drop-lowE-cevns), reconstructed via the exact linear E_rec=0.5·E_dep mapping (E_rec ≈ 2.5–5.0 eV) since these deposits lie far below the ~52.9/32.1 eV crossover onset.

**Task 2 — Fold all 3 channels × both designs** (`fold.py::run_fold`, deliverable CSVs)
- N_dep[i] = dRdEdep[i]·dE_dep[i] (dE_dep from npz `E_dep_edges_eV`); N_rec = **R_non_paralyzable** @ N_dep; dR/dE_rec[j] = N_rec[j]/dE_rec[j]. Muon/Compton grids verified to match the npz E_dep centers to <1e-6 rel.
- Only the **non-paralyzable** R is folded (CONVENTIONS §F resolved canonical; paralyzable retained only as a labeled sensitivity — fp-paralyzable-swap guarded).
- Bands propagated: CEvNS 1σ flux band folded the same way; Compton factor-2 site-flux band (0.5×/2×); muon ±30% normalization band.
- CSVs written: `artifacts/stage1/reconstructed_spectra_{TaAl,AlHf}.csv` (E_rec_keV + per-channel dR/dE_rec + bands + total, counts/kg/day/keV, provenance header).

**Task 3 — Reconstructed-energy landing + report-don't-force check** (`fold.py::landing_report`)

| Channel | Design | Integrated rate (cts/kg/day) | Peak E_rec | Frac below 10 / 50 / 100 eV |
|---|---|---|---|---|
| CEvNS | Ta→Al | 109.6 | **42 eV** | 0.18 / 0.60 / 0.85 |
| CEvNS | Al→Hf | 109.6 | **42 eV** | 0.19 / 0.62 / 0.86 |
| muon | Ta→Al | 1.073e6 | **18.8 keV** | ~0 / ~0 / ~0 |
| muon | Al→Hf | 1.073e6 | **15.0 keV** | ~0 / ~0 / ~0 |
| Compton | Ta→Al | 2.110e5 | **16.8 keV** | ~0 / ~0 / ~0 |
| Compton | Al→Hf | 2.110e5 | **13.3 keV** | ~0 / ~0 / ~0 |

Honest landing (ROADMAP report-don't-force): the **CEvNS** channel reconstructs to **tens of eV** (E_rec ≈ 0.5·E_dep, down to ~2.5 eV from the low edge) — the flagship low-recoil signal sits very low on the E_rec axis; ~85% of its reconstructed counts fall below 100 eV E_rec, but it is **not** entirely below the 10/50/100 eV reference thresholds, so the stop condition is **NOT triggered** (spectrum surfaced, not forced/reshaped). The **muon** channel (MeV–197 MeV deposits) piles up at tens of keV — direct evidence the saturating response, not the deposit axis, is applied. **Compton** spans its continuum reconstructed near tens of keV.

## Conventions

| Item | Value |
|---|---|
| Censoring | non-paralyzable (CONVENTIONS §F, RESOLVED 2026-07-21, canonical) |
| Energy scale | unified phonon, no quenching; E_rec(low-E)=0.5·E_dep (CONVENTIONS B/E) |
| Units | eV internal, keV I/O; dR/dE_rec in counts/kg/day/keV |
| Grids | shared 584-bin E_dep (10.14 eV→197 MeV), 161 E_rec bins, from Phase-5 npz |

## Key results & confidence

- Counts conservation: muon/Compton rel ≤ 2.2e-16, CEvNS rel ≤ 1.3e-16 (both designs). **[CONFIDENCE: HIGH]** — exact algebraic consequence of unit-sum R columns, verified numerically.
- CEvNS rebin fidelity: total 9.6e-5, above-50-eV 0.12%. **[CONFIDENCE: HIGH]** — two independent integral cross-checks.
- Muon saturation landing ~18.8/15.0 keV. **[CONFIDENCE: MEDIUM]** — the saturated-regime R shape has NO literature anchor (inherited Phase-5 caveat); validated by limiting cases only.
- CEvNS low-edge 0.5 slope: Phase-5 MC response median at the lowest bins is ~0.483 (~3% below 0.5); using 0.5 for the sub-floor band is a small documented calibration nuance.

## Deviations

None. All acceptance tests and forbidden-proxy guards pass; full suite 203 passed (188 prior + 15 new).

## Files

- `src/qpd_potential/fold.py` (deliv-fold-code)
- `tests/test_fold.py` (deliv-fold-tests, 15 tests)
- `artifacts/stage1/reconstructed_spectra_TaAl.csv` (deliv-recon-csv-taal)
- `artifacts/stage1/reconstructed_spectra_AlHf.csv` (deliv-recon-csv-alhf)

## Self-Check: PASSED

- Files exist; commits 0d64ed8 (code+tests), 0ee26c1 (CSVs). Full suite green. Frozen `data/flux/*.csv` restored pristine.

```yaml
gpd_return:
  status: completed
  phase: "06"
  plan: "01"
  tasks_completed: 3
  tasks_total: 3
  files_written:
    - src/qpd_potential/fold.py
    - tests/test_fold.py
    - artifacts/stage1/reconstructed_spectra_TaAl.csv
    - artifacts/stage1/reconstructed_spectra_AlHf.csv
    - GPD/phases/06-fold-reconstructed-energy-spectra/06-01-SUMMARY.md
  issues:
    - "CEvNS reconstructs to tens of eV E_rec (0.5*E_dep, peak ~42 eV, ~85% below 100 eV E_rec) — very low; surfaced honestly (ROADMAP report-don't-force), stop condition NOT triggered (not entirely below the 10/50/100 eV reference thresholds for both designs)."
    - "Saturated-regime muon response shape has no literature anchor (inherited Phase-5 caveat); muon landing ~18.8/15.0 keV validated by limiting cases only."
    - "CEvNS sub-floor low edge uses E_rec=0.5*E_dep; Phase-5 MC median at lowest bins is ~0.483 (~3% calibration nuance)."
  next_actions:
    - "Plan 06-02: plot deliv-fig-spectra from the two reconstructed_spectra CSVs and finalize ASSUMPTIONS.md."
  decisions:
    - summary: "Fold conserves counts per channel per design: muon/Compton rel <=2.2e-16 (unit-sum R columns), CEvNS rel <=1.3e-16; CEvNS rebin total 9.6e-5 vs trapz, above-50-eV 67.67 vs 67.752 (0.12%)."
      phase: "06"
    - summary: "Reconstructed peaks (non-paralyzable): CEvNS ~42 eV (0.5*E_dep, sub-keV), muon 18.8/15.0 keV, Compton 16.8/13.3 keV (Ta->Al/Al->Hf); muon MeV deposits saturate to tens of keV (fp-deposited-only guarded)."
      phase: "06"
    - summary: "CEvNS 5-10.14 eV low edge retained (7.27 cts/kg/day) via exact E_rec=0.5*E_dep, not dropped (fp-drop-lowE-cevns); only R_non_paralyzable folded (fp-paralyzable-swap)."
      phase: "06"
  state_updates:
    record_metric:
      phase: "06"
      plan: "01"
      duration: 1500
      tasks: 3
      files: 5
  contract_updates:
    claims_passed:
      - claim-fold-conserves
      - claim-cevns-lowedge
    acceptance_tests_passed:
      - test-counts-conservation
      - test-erec-axis
      - test-cevns-rebin
      - test-lowedge-retained
    forbidden_proxies_rejected:
      - fp-deposited-only
      - fp-drop-lowE-cevns
      - fp-paralyzable-swap
```
