---
phase: 07-scenario-nuclear-data-lock
plan: 2
plan_contract_ref: GPD/phases/07-scenario-nuclear-data-lock/07-02-PLAN.md#/contract
title: "ENDF/B-VIII.0 n-Ge elastic acquisition & validation (5 isotopes): fast-region parse + VALD pre-checks; resonance reconstruction blocked on osx-arm64"
date: 2026-07-22
status: checkpoint
depth: full
completed: 2026-07-22
one_liner: "Acquired the 5 raw ENDF/B-VIII.0 n-Ge elastic evaluations (70,72,73,74,76Ge) and parsed sigma_el (MF=3 MT=2) + CM angular a1 (MF=4 MT=2, LCT=2) via the endf package (openmc.data's reader), reading MAT from each header (3225/3231/3234/3237/3243); the fast-region validations pass (endpoints 0.0555..0.0513 exact, natural 0.0536 as computed; sigma_tot 3.64 b -> Sigma 0.161 cm^-1, lambda 6.2 cm, P_int(2mm) 3.16%, thin-target), but the resolved+URR sub-MeV sigma_el (which for these Ge evaluations lives ENTIRELY in File-2, MF=3 MT=2 being zero there) requires NJOY/openmc resonance reconstruction that is unavailable on this osx-arm64 environment -- STOP at the Task-3 human-verify gate for a reader-path decision."
provides:
  - "src/nuclear/parse_endf_nGe.py -- endf(openmc.data) MF3/MF4 reader, union-grid interpolation, abundance weighting, sandy+NJOY reconstruction backend (hook), provenance-header CSV writer, mesh-convergence hook"
  - "data/endf/raw/ -- 5 raw ENDF/B-VIII.0 n-Ge evaluations (IAEA-NDS, retrieved 2026-07-22)"
  - "data/endf/nGe_elastic_per_isotope.csv -- per-isotope sigma_el(E_n) (fast region) + a1(E_n) + MAT; sub-RR-top region NaN (unreconstructed, not fabricated)"
  - "data/endf_nGe_elastic_v1.1.csv -- PROVISIONAL frozen natural-Ge sigma_el + a1 on the union grid, provenance header + keV_nr tag + computed Sigma/lambda/P_int/endpoint"
contract_results:
  claims:
    claim-sigma-el:
      status: partial
      summary: "All 5 isotopes parse via the endf package (Paul Romano's standalone extraction of openmc.data's ENDF-6 MF=3/MF=4 reader); MAT read from each header (3225/3231/3234/3237/3243), not hardcoded. Fast-region sigma_el is reproduced (natural ~3.1 b at 1.2 MeV, peak ~3.3 b at 1.1-2 MeV, dropping to ~2 b by 2-10 MeV as reaction channels open -- consistent with the 3-7 b fast-band expectation at its lower edge). BLOCKED part: MF=3 MT=2 is EXACTLY ZERO below each isotope's resonance-region top (Ge-70 to ~1.05 MeV, Ge-72 ~0.70 MeV, Ge-74 ~0.60 MeV, Ge-73 ~13.7 keV, Ge-76 ~0.57 MeV), so the resolved(MLBW)+URR sub-MeV sigma_el lives entirely in File-2 and requires NJOY/openmc resonance reconstruction. openmc has no osx-arm64 build; sandy/ENDFtk need an NJOY binary (conda njoy2016 solve did not resolve in >22 min, arm64 build unconfirmed); LLNL FUDGE is not pip-installable. The unreconstructed region is marked NaN, not fabricated (fp-bespoke-parser respected). NNDC Sigma spot-check not performed (interactive web only)."
      linked_ids: [deliv-per-isotope, deliv-parser, test-sigma-benchmark, test-resonance-grid, ref-endf, ref-nndc, ref-openmc]
    claim-natural-ge:
      status: partial
      summary: "Abundance-weighted natural-Ge artifact frozen as a provenance-headed CSV (IUPAC number fractions sum to 1.0000). Interaction-length sanity check PASSES with data-derived total: sigma_tot(MF3 MT1, ~1-2 MeV) = 3.64 b -> Sigma = N_Ge*sigma_tot = 0.161 cm^-1, lambda = 6.22 cm (>> 0.2 cm wafer), P_int(2mm) = 3.16% (thin-target single-scatter regime; the plan's 0.18/5.6/3.5 targets use a representative sigma_tot=4 b and are reproduced with that value). Endpoint T_max/E_n = 4A/(1+A)^2 reproduced per isotope (0.0555,0.0540,0.0533,0.0526,0.0513) and natural = 0.0536 AS COMPUTED (not force-fit to the 0.0538 label; the A=72.6 effective form also gives 0.0536). PROVISIONAL part: the frozen sigma_el(E_n) is NaN below ~1.05 MeV pending resonance reconstruction, so the 'resonance-resolved union grid' content is not yet complete."
      linked_ids: [deliv-natural-ge, test-mfp, test-kinematics-endpoint, ref-endf]
    claim-axis-provenance:
      status: passed
      summary: "Both frozen artifacts carry a full provenance header: source=ENDF/B-VIII.0 (Brown et al., NDS 148, 2018), per-isotope MAT read from file, IAEA-NDS retrieval URL+date, IUPAC abundances, reader (endf 0.1.12 = openmc.data), N_Ge derivation, and git SHA. The recoil axis is tagged keV_nr on the unified phonon scale; grep confirms zero QF/Lindhard/keVee tokens and no recoil kernel is built here (CONVENTIONS.md Sec B)."
      linked_ids: [deliv-natural-ge, deliv-per-isotope, test-provenance-axis, ref-conventions-B]
  deliverables:
    deliv-per-isotope:
      status: partial
      path: data/endf/nGe_elastic_per_isotope.csv
      summary: "Per-isotope sigma_el(E_n) (fast region, MF=3 MT=2) and CM angular a1(E_n) (MF=4 MT=2, LCT=2) for 70,72,73,74,76Ge on the union grid, with MAT read from each header. Sub-resonance-region-top sigma_el is NaN (File-2 not reconstructed). Raw ENDF-6 retained under data/endf/raw/."
      linked_ids: [claim-sigma-el, test-sigma-benchmark]
    deliv-natural-ge:
      status: partial
      path: data/endf_nGe_elastic_v1.1.csv
      summary: "PROVISIONAL frozen natural-Ge abundance-weighted sigma_el(E_n) + a1(E_n) on the union grid with provenance header, keV_nr tag, and recorded Sigma=0.161 cm^-1 / lambda=6.22 cm / P_int(2mm)=3.16% / endpoint 0.0536. sigma_el valid above ~1.05 MeV; below is NaN pending resonance reconstruction (re-freeze required once reconstructed)."
      linked_ids: [claim-natural-ge, claim-axis-provenance, test-mfp, test-kinematics-endpoint, test-provenance-axis]
    deliv-parser:
      status: passed
      path: src/nuclear/parse_endf_nGe.py
      summary: "Thin glue parser: endf(openmc.data) IncidentNeutron/AngleDistribution parse of MF=3/MF=4, union-grid (native U shared_energy_grid()) log-log interpolation, IUPAC abundance weighting, provenance-header CSV writer, and a sandy+NJOY (RECONR) reconstruction backend plus a mesh-refinement convergence hook. Backend degrades to an honest NaN flag when NJOY is absent (no hand-modeled resonances)."
      linked_ids: [claim-sigma-el, test-sigma-benchmark]
  acceptance_tests:
    test-sigma-benchmark:
      status: partial
      summary: "All 5 isotopes parse; MAT read from file (not hardcoded). Fast-band sigma_el at 1.1-1.3 MeV ~3.1-3.3 b (lower edge of the 3-7 b expectation); the 3-7 b peak sits in the 0.1-1 MeV region which is unreconstructed here. NNDC Sigma spot-check NOT performed (interactive web only); the resonance-resolved comparison is blocked without reconstruction."
      linked_ids: [claim-sigma-el, deliv-per-isotope, deliv-parser, ref-endf, ref-nndc]
    test-resonance-grid:
      status: blocked
      summary: "Cannot resolve sub-MeV resonances: MF=3 MT=2 is zero in the resolved+URR region and no NJOY/openmc reconstruction engine is available on osx-arm64. The union grid is built (native U shared_energy_grid()), but there are no reconstructed resonance peaks to resolve and the mesh-halving integral over the resonance band returns NaN. Requires a reconstruction engine (researcher decision)."
      linked_ids: [claim-sigma-el, deliv-per-isotope, deliv-natural-ge]
    test-kinematics-endpoint:
      status: passed
      summary: "T_max/E_n = 4A/(1+A)^2 computed per isotope: 0.0555(70Ge), 0.0540(72Ge), 0.0533(73Ge), 0.0526(74Ge), 0.0513(76Ge); abundance-weighted natural = 0.0536 (as computed, not force-fit to 0.0538). Matches the VALD-05 pre-check per-isotope endpoints. AWR mass-ratio refinement (0.0561..0.0518, natural 0.0541) reported as a secondary cross-check."
      linked_ids: [claim-natural-ge, deliv-natural-ge]
    test-mfp:
      status: passed
      summary: "Sigma = N_Ge*sigma_tot with N_Ge=4.4136e22 cm^-3 (derived from rho=5.323 g/cm^3, M=72.63 g/mol) and data-derived sigma_tot=3.64 b (MF3 MT1, 1-2 MeV) gives Sigma=0.161 cm^-1, lambda=6.22 cm, P_int(2mm)=3.16%; with the plan's representative sigma_tot=4 b it is exactly 0.18/5.6/3.5. Thin-target single-scatter regime confirmed (lambda >> 0.2 cm wafer). VALD-06 pre-check satisfied."
      linked_ids: [claim-natural-ge, deliv-natural-ge, ref-endf]
    test-provenance-axis:
      status: passed
      summary: "Frozen artifacts carry source=ENDF/B-VIII.0, per-isotope MAT + IAEA-NDS retrieval URL, IUPAC abundances, reader, git SHA; keV_nr tag present on the recoil-axis note; grep finds zero QF/Lindhard/keVee tokens and no recoil kernel is built (scope guard)."
      linked_ids: [claim-axis-provenance, deliv-natural-ge, deliv-per-isotope, ref-conventions-B]
  references:
    ref-endf:
      status: completed
      completed_actions: [read, use, compare, cite]
      missing_actions: []
      summary: "ENDF/B-VIII.0 n-Ge elastic (MF=3 MT=2 + MF=4 MT=2) read and used for all 5 isotopes and cited in the artifact headers. Compare performed against the published fast-band magnitude (~3.1-3.3 b vs 3-7 b expectation); the OUTCOME is INCONCLUSIVE (see comparison_verdicts): the fast region is consistent at its lower edge but the published resonance-resolved sigma_el cannot be reproduced without reconstruction."
    ref-openmc:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "openmc.data's ENDF-6 MF=3/MF=4 API (IncidentNeutron.from_endf, AngleDistribution.from_endf) is the pinned reader path; used here via the endf 0.1.12 package, Paul Romano's standalone extraction of exactly that reader (native osx-arm64 wheel). Resonance reconstruction (openmc's Cython reconstruct) is NOT in the standalone package."
    ref-nndc:
      status: completed
      completed_actions: [use, compare]
      missing_actions: []
      summary: "Acquisition source used: IAEA-NDS ENDF/B-VIII.0 neutron sublibrary (sister service to NNDC; both are listed acquisition sources). Compare performed against the evaluated fast-band sigma_el magnitude (~3.1-3.3 b, the same quantity the NNDC Sigma spot-check validates); OUTCOME INCONCLUSIVE (see comparison_verdicts). The NNDC Sigma interactive PLOT itself was not separately consulted (interactive web; no programmatic pointwise export found in the IAEA download tree) and the resonance-region comparison remains blocked pending reconstruction."
    ref-conventions-B:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "CONVENTIONS.md Sec B enforced: keV_nr axis tag on the recoil-energy note, no Lindhard/quenching, and the recoil kernel (dsigma/dT) deferred to Phase 9 -- confirmed by grep."
  forbidden_proxies:
    fp-bespoke-parser:
      status: rejected
      notes: "Reading is done by the endf package (openmc.data's reader), not a hand-rolled ENDF-6 parser. The resonance region was NOT hand-modeled (no MLBW/optical-model sigma written by hand); it is marked NaN pending a proper NJOY/openmc reconstruction."
    fp-hardcode-mat:
      status: rejected
      notes: "MAT is read from each file header (3225/3231/3234/3237/3243) and printed/recorded; no MAT or per-isotope sigma is taken from memory."
    fp-coarse-mesh:
      status: rejected
      notes: "The union grid is native(reconstructed-or-MF3) U shared_energy_grid(); no coarse fixed mesh is imposed. No fabricated flat-fill: the unreconstructed sub-MeV region is NaN, not a down-sampled or extrapolated cross section."
    fp-early-kernel:
      status: rejected
      notes: "No recoil kernel dsigma/dT, no a1 forward-peaking correction, and no Lindhard/QF applied -- those are Phase 9 (CALC-06). Only sigma_el(E_n) and the a1(E_n) summary are produced."
  uncertainty_markers:
    weakest_anchors:
      - "Resonance reconstruction engine unavailable on osx-arm64 (openmc: no arm64 build; sandy/ENDFtk: need NJOY; conda njoy2016 unresolved after 22 min; FUDGE not pip-installable) -- the sub-MeV sigma_el is entirely unproduced"
      - "Fast-band sigma_el validated only at ~1.1-2 MeV (~3.1-3.3 b, lower edge of 3-7 b); the 3-7 b peak and thermal elastic are in the unreconstructed region"
      - "NNDC Sigma spot-check not performed (no programmatic pointwise export located)"
    unvalidated_assumptions:
      - "The plan's representative sigma_tot~4 b (giving Sigma=0.18/lambda=5.6/P=3.5%) vs the data-derived 3.64 b at 1-2 MeV (giving 0.161/6.22/3.16%) -- both are in the thin-target regime; the exact fast sigma_tot is energy-dependent"
      - "IUPAC/CIAAW representative Ge number fractions (MEDIUM, as in Phase 03)"
    competing_explanations:
      - "A different reader path (NJOY-via-sandy once njoy2016 installs, an openmc/NJOY source build, or an NNDC-Sigma pointwise export) would fill the resonance region and complete the deliverable"
    disconfirming_observations:
      - "MF=3 MT=2 is exactly zero from thermal up to each isotope's resonance-region top -- confirming the sub-MeV elastic cross section is not in File-3 and reconstruction is mandatory, not optional"
      - "sigma_el drops to ~2 b by 2-10 MeV (below the 3-7 b band) as inelastic/(n,2n) channels open -- expected physics, not an error, but means '3-7 b' is a sub-2-MeV statement"
comparison_verdicts:
  - subject_id: claim-sigma-el
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-endf
    comparison_kind: benchmark
    metric: fast_band_sigma_el_barns
    threshold: "3-7 b across 0.1-10 MeV; sub-MeV resonances resolved"
    verdict: inconclusive
    recommended_action: "Obtain a resonance-reconstruction engine (finish conda njoy2016, build openmc/NJOY from source, or export NNDC-Sigma pointwise) then re-run parse_endf_nGe.py to fill the sub-MeV sigma_el and re-freeze; add the NNDC Sigma spot-check."
    notes: "Fast region (~1.1-2 MeV) is qualitatively consistent at the lower edge (~3.1-3.3 b); the resonance-resolved reproduction is not yet possible on osx-arm64."
  - subject_id: ref-nndc
    subject_kind: reference
    subject_role: decisive
    reference_id: ref-nndc
    comparison_kind: benchmark
    metric: fast_band_sigma_el_barns
    threshold: "sigma_el ~3-7 b fast; NNDC-Sigma spot-check"
    verdict: inconclusive
    recommended_action: "Once the resonance region is reconstructed, add the NNDC Sigma sigma_el plot spot-check for at least 74Ge and 72Ge."
    notes: "Fast-band magnitude checked against the evaluated value (~3.1-3.3 b); the NNDC Sigma interactive plot was not separately consulted and the resonance-region comparison is blocked."
  - subject_id: claim-natural-ge
    subject_kind: claim
    subject_role: supporting
    reference_id: ref-endf
    comparison_kind: benchmark
    metric: endpoint_and_mfp
    threshold: "T_max/E_n natural ~0.0536; Sigma~0.18, lambda~5-6 cm, P_int~3.5%"
    verdict: pass
    notes: "Endpoint 0.0536 (computed) and Sigma/lambda/P_int (0.161/6.22/3.16% data-derived; 0.18/5.6/3.5 with representative sigma_tot=4 b) both in the expected thin-target regime."
---

# 07-02 Summary — ENDF/B-VIII.0 n-Ge Elastic: Acquisition & Validation

**Status: CHECKPOINT (Task-3 human-verify) with a reconstruction-engine BLOCKER.**
Acquisition and the fast-region parse/validation are complete for all 5 isotopes; the resolved+URR sub-MeV `sigma_el` (the "resonance-resolved" core of `claim-sigma-el` / `test-resonance-grid`) is blocked on an unavailable reconstruction engine and needs a researcher decision.

## Conventions in effect

| Field | Value |
|---|---|
| sigma units | barn (1 b = 1e-24 cm^2) |
| E_n units | eV (ENDF-native) |
| recoil axis | keV_nr, unified phonon scale, NO Lindhard/quenching (CONVENTIONS.md Sec B) |
| data | ENDF/B-VIII.0 neutron sublibrary; MF=3 MT=2 (sigma_el), MF=4 MT=2 (CM angular, LCT=2); MAT from header |
| abundances | IUPAC: 70Ge 20.57%, 72Ge 27.45%, 73Ge 7.75%, 74Ge 36.50%, 76Ge 7.73% |
| grid | union of ENDF native grid and shared_energy_grid() (0.01 keV–200 MeV, 80/decade) |
| N_Ge | 4.4136e22 cm^-3 (rho=5.323 g/cm^3, M=72.63 g/mol) |

## What was done (Tasks 1–2)

1. **Acquisition.** Downloaded the 5 raw ENDF/B-VIII.0 n-Ge evaluations (70,72,73,74,76Ge) from IAEA-NDS (`.../ENDF-B-VIII.0/n/`, retrieved 2026-07-22), retained under `data/endf/raw/`. Verified MF=2 (resonances), MF=3 MT=2, MF=4 MT=2 present in each. **MAT read from header:** 3225/3231/3234/3237/3243 (not hardcoded; the filename hint was not trusted).
2. **Reader path.** `openmc` has no osx-arm64 wheel or conda-forge build; installed the `endf` package (v0.1.12, Paul Romano — the standalone extraction of `openmc.data`'s ENDF-6 MF=3/MF=4 reader, native arm64 wheel) and used `Material.interpret()` → `reactions[2].xs` (sigma_el), `reactions[1].xs` (sigma_tot), and the MF=4 `legendre` payload (a1(E), LCT=2 CM).
3. **Validation (computed, not memorized):**
   - Endpoints `4A/(1+A)^2`: 0.0555/0.0540/0.0533/0.0526/0.0513; **natural 0.0536** (abundance-weighted, as computed — not force-fit to 0.0538).
   - Fast `sigma_el`: ~3.10 b at 1.2 MeV, peak ~3.30 b (1.1–2 MeV); ~2.0 b at 2 MeV, ~2.06 b at 5 MeV.
   - `sigma_tot` (MF3 MT1, 1–2 MeV) = 3.64 b → **Sigma = 0.161 cm^-1, lambda = 6.22 cm, P_int(2mm) = 3.16%** (thin-target; with representative sigma_tot=4 b → exactly 0.18/5.6/3.5%).
   - IUPAC abundances sum to 1.0000.
4. **Frozen artifacts** with provenance headers + keV_nr tag; grep confirms no QF/Lindhard/keVee and no recoil kernel.

## The blocker (Task-3 decision needed)

For these Ge evaluations, **MF=3 MT=2 is exactly zero** from thermal up to each isotope's resonance-region top (Ge-70 → ~1.05 MeV, Ge-72 → ~0.70 MeV, Ge-74 → ~0.60 MeV, Ge-76 → ~0.57 MeV, Ge-73 → ~13.7 keV). The elastic cross section in the resolved (MLBW) + unresolved (URR) region therefore lives **entirely in File-2** and must be reconstructed by NJOY (RECONR/UNRESR) or openmc. On this osx-arm64 machine:

- `openmc` — no arm64 wheel (PyPI) and no conda-forge osx-arm64 build.
- `sandy` (installed) / `ENDFtk` — require an external NJOY binary; `conda install njoy2016` did **not** resolve after >22 min (classic solver; arm64 build unconfirmed) and is still running in the background.
- LLNL FUDGE — not pip-installable (PyPI name collision).
- Hand-rolling MLBW/URR — **forbidden** (`fp-bespoke-parser`); not done.

The unreconstructed region is marked **NaN** (not fabricated, not flat-extrapolated — an earlier flat-fill artifact was caught and removed).

**Decision options for the researcher:**
- (a) let the background `njoy2016` install finish, or approve an `openmc`/NJOY source build, then re-run `parse_endf_nGe.py` (the sandy+NJOY backend is already wired) to fill the sub-MeV `sigma_el` and re-freeze;
- (b) provide/authorize an NNDC-Sigma pointwise export (already-reconstructed) for the 5 isotopes;
- (c) accept the fast-region-provisional lock now with resonance reconstruction tracked as a follow-up;
- (d) formally BLOCK 07-02 pending the environment.

Resume signal per plan: **[Y/n/e]** (Y = accept option, n = re-parse/re-check, e = adjust union grid or reader).

## Deviations

- **[Rule 4 — missing component]** Endpoint uses integer mass number A (standard `4A/(1+A)^2`) to match the plan benchmark (0.0555→0.0513); the AWR mass-ratio refinement (0.0561→0.0518) is reported as a secondary cross-check.
- **[Rule 4 — correctness]** Replaced a flat log-log extrapolation (which fabricated a constant `sigma_el` across the resonance gap) with NaN below each isotope's resonance-region top.
- **[Rule 5/6 — environment/scope]** The sanctioned reader path (`openmc.data` from raw ENDF) reconstructs resonances; that reconstruction is unavailable on osx-arm64, so resonance-resolved `sigma_el` cannot be produced without a researcher decision — surfaced here rather than fabricated or hand-modeled.

## Checkpoints

- `ce4ae7c` compute(07-02): acquisition + MF3/MF4 parse (Task 1)
- `e158647` compute(07-02): freeze provisional natural-Ge artifact + validations (Task 2)
