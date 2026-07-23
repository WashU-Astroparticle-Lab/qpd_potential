# Phase 7: Scenario & Nuclear-Data Lock — Context

_Recorded 2026-07-22. Phase 7 was planned directly (discuss-phase skipped by user: "No need to discuss"). This file persists the already-established decisions so the alignment gate and resume machinery function; it is not a new discussion._

## Locked Decisions (USER DECISION 2026-07-21 / 2026-07-22)

- **Gating-input strategy:** the three external normalization inputs are fixed as **representative cited defaults with an explicit uncertainty band** (the v1.0 environmental-gamma pattern). NOT a best/worst bracket; a single representative default + band per input.
- **Milestone scope (v1.1):** neutron-induced nuclear-recoil background (muon-induced local + cosmogenic sea-level ambient + radiogenic (α,n)/SF) and detector-material radioactivity (Ge crystal bulk + housing/nearby components). QPD-film radioactivity is OUT of scope this milestone.
- **Execution approval:** user approved proceeding into execution including the `openmc`/`sandy` install + NNDC/IAEA network data download for the ENDF acquisition (07-02).
- **Autonomy:** supervised; both plans are `interactive` with a human-verify checkpoint on the three discretionary defaults.

## Agent's Discretion (recommend one, with a band)

- The specific representative value chosen within each cited band (ambient neutron flux level given the surface/building-shielding tag; the single housing-material radiopurity default within the electroformed-Cu ↔ commercial bracket; the exposure/cool-down default, research recommends t_exp = 1 yr, t_cool = 0).
- ENDF reader path (openmc.data preferred; sandy/ENDFtk/NNDC-Sigma fallback).

## Deferred / Out of Scope (this phase)

- Recoil-kernel construction and neutron dR/dE_dep fold → Phase 9 (CALC-06).
- Radiogenic spectra → Phase 10; cosmogenic A(t) inventory & ER templates → Phase 11.
- Any spectrum folding to reconstructed energy → Phase 12.

## Convention Discipline (from CONVENTIONS §B/§F)

- Unified phonon scale, **no ionization quenching**; every locked input carries a **keV_nr** axis tag; FORBIDDEN: keVee↔keVnr mixing / Lindhard QF on the phonon scale.
- Surface deployment: no underground/shielded-residual number imported as the surface baseline.
- Every flux/rate/activity carries a provenance tag: (depth, shielding) / (material, assay) / (exposure, cool-down).
