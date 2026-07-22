# Roadmap: QPD Particle-Physics Potential

## Milestones

- Done: **v1.0 Reconstructed-Energy Spectra** — Phases 1–6 (completed 2026-07-22). Reactor-CEvNS, cosmic-muon, and environmental-gamma Compton differential rate spectra in reconstructed energy for a ~110 g QPD Ge wafer, both trapping designs. Full detail: [`milestones/v1.0-ROADMAP.md`](milestones/v1.0-ROADMAP.md); digest: [`milestones/v1.0/RESEARCH-DIGEST.md`](milestones/v1.0/RESEARCH-DIGEST.md).
- Active: **v1.1 Neutron & Radiogenic Backgrounds** — Phases 7–12. In-band (CEvNS-band) background budget in reconstructed energy — neutron-induced nuclear recoils (ambient cosmogenic, local muon-induced, radiogenic) + detector-material radioactivity (Ge-bulk + housing) — for both trapping designs, folded through the v1.0 response chain and compared to the v1.0 reactor-CEvNS signal.
- Planned: **Manuscript / Sensitivity** — MANU-01 (round-1 peer-review revision), SENS-01 (quantitative CEvNS discovery/exclusion sensitivity). Deferred; enabled by the v1.1 budget.

## Overview

v1.1 extends the completed v1.0 forward-model/response chain to the in-band background suite. Every background channel is produced in reconstructed energy on the **unified phonon scale (no ionization quenching)** and folded through the existing `R(E_rec|E_dep)` matrices (both designs, non-paralyzable 25 kHz). On this axis a fast-neutron elastic recoil and a CEvNS recoil of the same energy `T` are kinematically indistinguishable, so neutron elastic scattering is the defining irreducible background of this milestone. The physics is a single laptop-scale analytic pipeline (thin-target single-scatter flat-box fold; no G4CMP/MCNP): the three leading terms are input-gated, not compute-gated, so a prerequisite phase (Phase 7) fixes the three external normalizations as **representative cited defaults with an explicit uncertainty band** and acquires the ENDF/B-VIII.0 n-Ge elastic data before any fold. Phases 8→9 build the neutron chain, Phases 10 (parallel) and 11 build the radioactivity chain, and Phase 12 folds everything to reconstructed energy and compares against the v1.0 CEvNS signal.

## Contract Overview

| Contract Item | Advanced By Phase(s) | Status |
| ------------- | -------------------- | ------ |
| φ(E_n) neutron source terms, 3 sources, provenance + keV_nr-axis tagged (CALC-05) | Phase 8 | Planned |
| Neutron dR/dE_dep on the phonon scale via flat-box single-scatter fold (CALC-06) | Phase 9 | Planned |
| Radiogenic detector-material **electron-recoil** dR/dE_dep (Ge-bulk + housing) (CALC-07) | Phase 10 | Planned |
| Radiogenic **neutron** NR from (α,n)+²³⁸U SF (CALC-08) | Phase 10 | Planned |
| Cosmogenic-activation A(t) inventory + in-band ER templates (CALC-09) | Phase 11 | Planned |
| Combined in-band dR/dE_rec budget vs. v1.0 CEvNS, both designs (CALC-10) | Phase 12 | Planned |
| Single-scatter/escape MC cross-check + >1 MeV a₁ tail correction (SIMU-04) | Phase 9 | Planned |
| Recoil kinematics T_max/E_n = 0.0538 per isotope (VALD-05) | Phase 9 | Planned |
| Interaction probability ~3–4% in 2 mm Ge; count-conservation (VALD-06) | Phase 9 | Planned |
| Source-term anchors (Gordon flux, ²³⁸U SF yield, ³H production) (VALD-07) | Phase 11 (sub-anchors exercised in 8/10) | Planned |
| Peer in-band cross-check vs. NUCLEUS ~250 dru (VALD-08) | Phase 12 | Planned |
| **Anchor** Gordon 2004 sea-level neutron flux | Phase 7, 8 | Planned |
| **Anchor** ENDF/B-VIII.0 n-Ge elastic | Phase 7, 9 | Planned |
| **Anchor** Mei–Zhang–Hime ²³⁸U SF yield; (α,n) yield tables | Phase 8, 10, 11 | Planned |
| **Anchor** CDMSlite/EDELWEISS ³H/⁶⁸Ge/⁶⁵Zn production rates | Phase 7, 11 | Planned |
| **Anchor** Heusser 1995; ENSDF/DDEP; NIST XCOM | Phase 10 | Planned |
| **Anchor** NUCLEUS arXiv:2509.03559 (~250 dru in-band lower bound) | Phase 12 | Planned |
| **Prior output** v1.0 shared_energy_grid(); R(E_rec|E_dep) matrices; Gaisser–Guan muon flux; Klein–Nishina Compton machinery; CONVENTIONS §B/§F | Phase 7–12 | Planned |

**Forbidden proxies (must stay visible milestone-wide):** `fp-deposited-only` (deposited-energy-only spectra), `fp-no-saturation` (skipping the 25 kHz censoring), `fp-full-absorption` (full-energy photopeaks instead of Compton continuum in the thin wafer), keVee↔keVnr axis mixing / Lindhard-QF on the phonon scale, and muon-induced-neutron double-counting of the v1.0 muon deposit.

## Phases

<details>
<summary>Done: v1.0 Reconstructed-Energy Spectra (Phases 1–6) — COMPLETED 2026-07-22</summary>

- [x] Phase 1: Conventions & Energy-Scale Foundation (2/2 plans) — verified passed
- [x] Phase 2: Reactor Flux Model (2/2 plans) — sub-1.8 MeV band-covered
- [x] Phase 3: CEvNS Cross Section & Rate (2/2 plans) — Billard within 2.4%
- [x] Phase 4: Muon & Compton Deposited-Energy Spectra (3/3 plans) — VALD-02/03 met
- [x] Phase 5: QPD Response Chain & Energy Reconstruction (2/2 plans) — non-paralyzable adopted
- [x] Phase 6: Fold & Produce Reconstructed-Energy Spectra (2/2 plans) — deliverables shipped

Milestone audit: PASS with open questions ([`milestones/v1.0-MILESTONE-AUDIT.md`](milestones/v1.0-MILESTONE-AUDIT.md)). Cross-phase consistency: CONSISTENT ([`CONSISTENCY-CHECK.md`](CONSISTENCY-CHECK.md)).

</details>

### Active: v1.1 Neutron & Radiogenic Backgrounds (Phases 7–12)

**Milestone Goal:** Compute the in-band (CEvNS-band) background budget in reconstructed energy — neutron-induced Ge nuclear recoils from three fast-neutron sources plus detector-material radioactivity (Ge-bulk + housing) — for both trapping designs on the unified phonon scale, folded through the v1.0 `R(E_rec|E_dep)` matrices, and compared against the v1.0 reactor-CEvNS signal with a peer in-band cross-check. Analytic/Monte-Carlo only; no G4CMP.

- [ ] **Phase 7: Scenario & Nuclear-Data Lock** — fix the three external gating inputs (+ band) and acquire/validate ENDF/B-VIII.0 n-Ge elastic data before any fold
- [ ] **Phase 8: Neutron Source Terms (P-NSRC)** — assemble φ(E_n) for all three neutron sources, provenance + keV_nr-axis tagged, double-count-guarded
- [ ] **Phase 9: Neutron Transport & Recoil Fold (P-NTRANS)** — produce labeled neutron dR/dE_dep via the flat-box single-scatter fold, kinematics + thin-target validity verified
- [ ] **Phase 10: Detector Radioactivity Budget (P-RAD)** — Ge-bulk + housing electron-recoil spectrum and radiogenic neutron NR for the assumed radiopurity budget
- [ ] **Phase 11: Cosmogenic Activation Inventory (P-COSMO)** — isotope-specific A(t) inventory and in-band ER templates (³H β, EC X-ray lines)
- [ ] **Phase 12: Response Fold & Combined In-Band Budget (P-FOLD)** — fold every channel to E_rec and compare the combined in-band budget to the v1.0 CEvNS signal

## Phase Details

### Phase 7: Scenario & Nuclear-Data Lock

**Goal:** The three external gating inputs are fixed as representative cited defaults with an explicit uncertainty band, and the ENDF/B-VIII.0 n-Ge elastic cross sections are acquired and validated, so every downstream fold starts from provenance-tagged, axis-consistent, surface-appropriate inputs.
**Depends on:** v1.0 outputs (complete) — entry point for v1.1.
**Requirements:** None standalone (prerequisite setup phase); **gates** CALC-05, CALC-06, CALC-07, CALC-08, CALC-09.
**Contract Coverage:**
- Advances: the representative-defaults+band decision that unblocks the three input-gated leading terms; ENDF n-Ge elastic acquisition.
- Deliverables: scenario/assumptions note documenting the three gating inputs + uncertainty band with provenance; parsed ENDF/B-VIII.0 n-Ge elastic tables (5 isotopes) on a resonance-resolved grid.
- Anchor coverage: Gordon 2004 (surface ambient neutron); ENDF/B-VIII.0 (openmc.data MF=3/MF=4); CDMSlite/EDELWEISS production rates; electroformed-Cu (<0.3 µBq/kg) and GERDA Ge-bulk (µBq/kg) radiopurity benchmarks; v1.0 `shared_energy_grid()`; CONVENTIONS §B.
- Forbidden proxies: importing underground / post-shield residuals as the surface baseline (surface-vs-underground regime inversion); keVee↔keVnr mixing; any Lindhard/QF on the phonon scale.
**Success Criteria** (what must be TRUE):

1. The surface ambient-neutron normalization is fixed to a cited default (Gordon-2004 sea-level, indoor/outdoor tagged) with an explicit factor-of-a-few band and a documented (depth, shielding) provenance tag.
2. The housing/materials U/Th/⁴⁰K radiopurity budget is fixed to representative cited assays with an uncertainty band (ppb↔µBq/kg conversion recorded: 1 ppb U ≈ 12.4 mBq/kg, 1 ppb Th ≈ 4.06 mBq/kg).
3. The Ge surface-exposure/cool-down scenario is fixed (exposure time + cool-down), yielding a ³H/⁶⁸Ge/⁶⁵Zn normalization band consistent with CDMSlite/EDELWEISS rates.
4. ENDF/B-VIII.0 n-Ge elastic cross sections for all 5 Ge isotopes are parsed via `openmc.data`, reproduce published σ_el on a union (native ∪ flux) grid resolving sub-MeV resonances, and give λ ~ 5–6 cm (Σ ~ 0.18 cm⁻¹) as a sanity check.
5. Every fixed input carries a keV_nr axis tag; no keVee/Lindhard quenching is introduced anywhere in the locked inputs.

**Plans:** TBD (run `gpd:plan-phase 7` to break down)

### Phase 8: Neutron Source Terms (P-NSRC)

**Goal:** The incident fast-neutron flux φ(E_n) for all three sources — ambient cosmogenic sea-level, local muon-induced, and radiogenic (α,n)+²³⁸U SF — is assembled on the shared energy grid, each provenance- and keV_nr-axis-tagged, with the muon-induced channel explicitly guarded against double-counting the v1.0 muon deposits.
**Depends on:** Phase 7 (locked scenario inputs + ENDF data).
**Requirements:** CALC-05.
**Contract Coverage:**
- Advances: CALC-05 (provenance-tagged φ(E_n) tables, 3 sources).
- Deliverables: three provenance-headed φ(E_n) CSVs on `shared_energy_grid()`.
- Anchor coverage: Gordon 2004; Wang-2001 muon-induced yield; Mei–Zhang–Hime ²³⁸U SF; v1.0 Gaisser–Guan muon flux; shared grid.
- Forbidden proxies: muon-induced neutrons re-counting the v1.0 muon deposit (`fp-muon-neutron-double-count`); untagged keVee flux; transferring underground fluxes to the surface baseline.
**Success Criteria** (what must be TRUE):

1. Ambient cosmogenic φ(E_n) reproduces the Gordon-2004 >10 MeV integral 3.5×10⁻³ cm⁻²s⁻¹ (broad thermal→GeV ~1.3×10⁻²), with the ">10 MeV" vs "broad" labeling reconciled and (depth, shielding) tags attached.
2. The local muon-induced source is normalized to the v1.0 Gaisser–Guan muon flux via the Wang-2001 yield, restricted to wafer+housing production (~10⁻⁶/muon), and shown subdominant; a channel on/off toggle proves the v1.0 muon deposit spectrum is byte-identical (double-count guard passes).
3. The radiogenic (α,n)+²³⁸U SF source is assembled as a ²³⁸U Watt spectrum × the assumed assay, with the SF yield 1.353×10⁻¹¹ n/g/s per ppb U.
4. All three φ(E_n) tables live on `shared_energy_grid()` with provenance headers and carry a keV_nr axis tag (no keVee).

**Plans:** TBD (run `gpd:plan-phase 8` to break down)

### Phase 9: Neutron Transport & Recoil Fold (P-NTRANS)

**Goal:** The neutron-induced Ge nuclear-recoil deposited-energy spectrum dR/dE_dep is produced for all three channels via the isotropic-CM flat-box single-scatter fold over ENDF elastic data, on the unified phonon scale, with recoil kinematics and thin-target validity quantitatively verified.
**Depends on:** Phase 8 (φ(E_n) source terms); Phase 7 (ENDF elastic data).
**Requirements:** CALC-06, SIMU-04, VALD-05, VALD-06.
**Contract Coverage:**
- Advances: CALC-06 (neutron dR/dE_dep), SIMU-04 (MC cross-check + a₁ tail), VALD-05 (kinematics), VALD-06 (interaction probability + count-conservation).
- Deliverables: labeled three-channel neutron dR/dE_dep on `shared_energy_grid()`; single-scatter/escape MC report; kinematics and interaction-probability validation notes.
- Anchor coverage: ENDF/B-VIII.0 n-Ge elastic; two-body recoil kinematics; v1.0 shared grid; CONVENTIONS §B.
- Forbidden proxies: applying Lindhard/QF on the phonon scale; keVnr-vs-keVee mixing; depositing full neutron energy instead of ≤5.4% recoil per interaction.
**Success Criteria** (what must be TRUE):

1. dR/dE_dep is produced for all three neutron channels on `shared_energy_grid()`, labeled, on the unified phonon scale with NO quenching (no Lindhard/QF anywhere).
2. **VALD-05:** T_max/E_n = 4A/(1+A)² = 0.0538 for natural Ge is reproduced per contributing isotope, and the flat-box kernel integrates to σ_el·N_Ge.
3. **VALD-06:** the fast-neutron interaction probability in 2 mm Ge is 3–4% (λ ~ 5–6 cm, Σ ~ 0.18 cm⁻¹), and count-conservation is preserved through the recoil fold (≤1e-3).
4. **SIMU-04:** a bespoke single-scatter/escape MC (or analytic multiple-scatter estimate) quantifies the multi-scatter and escape fractions (≲1%) and the >1 MeV a₁ forward-peaking (File-4 Legendre) tail correction to the flat-box kernel.

**Plans:** TBD (run `gpd:plan-phase 9` to break down)

### Phase 10: Detector Radioactivity Budget (P-RAD)

**Goal:** The detector-material radiogenic backgrounds — Ge-bulk + housing electron recoils (Compton continuum + intrinsic β/EC) and radiogenic neutron NR from (α,n)+²³⁸U SF — are computed as dR/dE_dep for the assumed representative radiopurity budget, with correct thin-wafer self-shielding and solid-angle/attenuation treatment.
**Depends on:** Phase 7 (radiopurity budget) for the CALC-07 ER work; Phase 9 (validated recoil kernel) for the CALC-08 neutron-NR sub-fold. The ER portion may begin as soon as Phase 7 completes; the neutron-NR portion rejoins after Phase 9.
**Requirements:** CALC-07, CALC-08.
**Contract Coverage:**
- Advances: CALC-07 (radiogenic ER dR/dE_dep, Ge-bulk + housing), CALC-08 (radiogenic neutron NR dR/dE_dep).
- Deliverables: ER spectrum (Compton continuum + β/EC bulk deposits) and radiogenic-neutron NR spectrum on `shared_energy_grid()`.
- Anchor coverage: Heusser 1995; ENSDF/DDEP; NIST XCOM; Mei–Zhang–Hime SF yield; (α,n) yield tables; v1.0 Klein–Nishina Compton machinery; Phase 9 recoil kernel.
- Forbidden proxies: full-energy photopeaks instead of the Compton continuum in the thin 2 mm wafer (`fp-full-absorption`); generic (α,n) yield ignoring material light-element content.
**Success Criteria** (what must be TRUE):

1. The CALC-07 ER spectrum treats Ge-bulk + housing U/Th/⁴⁰K gammas as a Compton continuum (reusing v1.0 Klein–Nishina machinery; MeV peaks escape → Compton edge only) plus intrinsic β/EC full-energy bulk deposits, with external sources weighted by activity×(Ω/4π)×self-absorption×path-attenuation, not full-peak efficiency.
2. The CALC-08 radiogenic neutron NR is folded through the validated Phase 9 recoil kernel using the ²³⁸U Watt SF spectrum + per-material (α,n) yields (low-Z content dominates; pure-Ge (α,n) yields ~nothing).
3. Thin-wafer self-shielding is handled correctly: MeV γ optically thin (peaks escape, edge retained), while low-E X-rays/Augers/β (e.g., ⁶⁸Ge/⁷¹Ge EC ~1.3/10.4 keV, ³H β) deposit fully.
4. All spectra are on `shared_energy_grid()`, unified phonon scale, and pass an energy-closure check.

**Plans:** TBD (run `gpd:plan-phase 10` to break down)

### Phase 11: Cosmogenic Activation Inventory (P-COSMO)

**Goal:** The cosmogenic-activation isotope inventory A(t) is built for the assumed Ge exposure/cool-down scenario and converted into in-band electron-recoil templates (³H β continuum to the 18.6 keV endpoint; EC K/L X-ray lines).
**Depends on:** Phase 7 (exposure/cool-down scenario). Parallel with Phases 8–10; feeds the Phase 12 fold (and shares the intrinsic-activity framing with Phase 10).
**Requirements:** CALC-09, VALD-07.
**Contract Coverage:**
- Advances: CALC-09 (cosmogenic ER templates + A(t) inventory), VALD-07 (source-term normalization anchors).
- Deliverables: isotope-specific A(t) inventory; ³H β continuum + EC X-ray line ER templates on `shared_energy_grid()`.
- Anchor coverage: CDMSlite/EDELWEISS ³H/⁶⁸Ge/⁶⁵Zn production rates; ENSDF; Mei–Zhang–Hime ²³⁸U SF yield (VALD-07 also exercises the Gordon flux anchor in Phase 8).
- Forbidden proxies: quoting saturation activity as as-deployed activity; a blanket (non-isotope-specific) activity value.
**Success Criteria** (what must be TRUE):

1. Isotope-specific A(t) is computed via Bateman (`radioactivedecay`), NOT a blanket saturation value; ³H (12.3 yr) is shown non-saturating and carrying the exposure-time dependence, while ⁶⁸Ge/⁶⁵Zn saturate (~1 yr).
2. **VALD-07** anchors are reproduced within stated tolerances: ³H production 74–82 atoms/kg/day (CDMSlite/EDELWEISS); ⁶⁵Zn 17, ⁶⁸Ge 30 atoms/kg/day; ²³⁸U SF yield 1.353×10⁻¹¹ n/g/s per ppb U.
3. In-band ER templates are produced: ³H β continuum 0→18.6 keV endpoint (exact), plus EC K/L X-ray lines, on `shared_energy_grid()`.
4. The as-deployed activity (not saturation activity) is quoted for the stated exposure/cool-down history and documented.

**Plans:** TBD (run `gpd:plan-phase 11` to break down)

### Phase 12: Response Fold & Combined In-Band Budget (P-FOLD)

**Goal:** Every background channel is folded through the v1.0 `R(E_rec|E_dep)` response (both designs, non-paralyzable 25 kHz) to reconstructed energy, and the combined in-band background budget is assembled and compared against the v1.0 reactor-CEvNS signal in the flagship band, with a peer in-band cross-check.
**Depends on:** Phase 9 (neutron dR/dE_dep), Phase 10 (radiogenic ER + neutron NR), Phase 11 (cosmogenic ER templates).
**Requirements:** CALC-10, VALD-08.
**Contract Coverage:**
- Advances: CALC-10 (combined in-band dR/dE_rec vs. CEvNS), VALD-08 (peer in-band cross-check).
- Deliverables: combined in-band dR/dE_rec budget (both designs) vs. the v1.0 CEvNS signal; NUCLEUS in-band comparison note.
- Anchor coverage: v1.0 `R(E_rec|E_dep)` matrices; v1.0 CEvNS signal + flagship band; NUCLEUS arXiv:2509.03559 (~250 dru).
- Forbidden proxies: deposited-energy-only spectra (`fp-deposited-only`); skipping the 25 kHz saturation (`fp-no-saturation`); claiming agreement where only a lower-bound direction is testable.
**Success Criteria** (what must be TRUE):

1. All channels (three neutron NR + radiogenic ER + cosmogenic ER) are folded through `R(E_rec|E_dep)` for both designs with count-conservation ≤1e-3 per channel per design; the v1.0 muon spectrum reproduces byte-identical when given the v1.0 line list (machinery-reuse invariant).
2. The combined in-band dR/dE_rec budget is assembled versus the v1.0 CEvNS signal in the flagship reconstructed-energy band; the 10 eV display floor is honored; no deposited-energy-only reporting.
3. **VALD-08:** the modeled 10–100 eV in-band nuclear-recoil rate is compared against the NUCLEUS ~250 dru shielded lower bound and the unshielded surface result exceeds it (direction consistency, not equality).
4. The in-band floor is stated as a lower bound (LEE below ~100 eV unmodeled; reactor-correlated thermal-capture NR flagged as a deferred addend).

**Plans:** TBD (run `gpd:plan-phase 12` to break down)

## Phase Dependencies

| Phase | Depends On | Enables | Critical Path? |
|-------|-----------|---------|:-:|
| 7 – Scenario & Nuclear-Data Lock | v1.0 (done) | 8, 9, 10, 11 | Yes |
| 8 – Neutron Source Terms | 7 | 9 | Yes |
| 9 – Neutron Transport & Recoil Fold | 7, 8 | 10 (kernel), 12 | Yes |
| 10 – Detector Radioactivity Budget | 7, 9 | 12 | Yes |
| 11 – Cosmogenic Activation Inventory | 7 | 12 | No (parallel with 8–10) |
| 12 – Response Fold & Combined Budget | 9, 10, 11 | — | Yes |

**Critical path:** 7 → 8 → 9 → 10 → 12 (5 sequential phases).
**Parallelizable:** Phase 11 runs concurrently with Phases 8–10 (only depends on Phase 7). The Phase 10 electron-recoil (CALC-07) work can also begin right after Phase 7 in parallel with the neutron chain; only its CALC-08 neutron-NR sub-fold waits on the Phase 9 kernel.

## Risk Register

| Phase | Top Risk | Probability | Impact | Mitigation |
|-------|---------|:-:|:-:|-----------|
| 7 | No defensible representative default/band citable for a gating input | MEDIUM | HIGH | Reuse the v1.0 environmental-gamma cited-default+band pattern; if uncitable, block and request user scope repair before folding |
| 8 | Muon-induced neutrons re-count the v1.0 muon deposit (Gordon ambient already contains μ-cascade neutrons) | MEDIUM | HIGH | Restrict the channel to LOCAL wafer+housing production; byte-identical v1.0-muon on/off test as an acceptance gate |
| 9 | Flat-box single-scatter breaks down at E_n ≳ 1 MeV (forward-peaking / multi-scatter) | LOW | MEDIUM | SIMU-04 single-scatter MC + a₁ Legendre correction; backtrack if multi-scatter/escape exceeds a few % |
| 10 | Missing per-material (α,n) yields for QPD housing; self-shielding mis-normalization | MEDIUM | MEDIUM | NeuCBOT/SOURCES-4C cross-check + widen band; enforce activity×(Ω/4π)×attenuation, never full-peak efficiency |
| 11 | Exposure/cool-down history unknown → ³H normalization (never saturates) | MEDIUM | MEDIUM | Representative scenario + band from Phase 7; flag ³H exposure-time dependence explicitly |
| 12 | keVee↔keVnr axis mixing collapses the whole budget; surface pileup stop-condition | LOW | HIGH | Phonon-scale axis tags enforced upstream (Phases 7–9); count-conservation + muon-invariant asserts; re-check occupancy vs the 50 kHz pileup stop-condition |

## Backtracking Triggers

- **Phase 7:** If any of the three gating inputs cannot be pinned to a defensible cited default + band, block and request scope repair — do not improvise a normalization.
- **Phase 8:** If the muon-induced channel is not demonstrably independent of the v1.0 muon deposit (byte-identical on/off test fails), revisit the normalization before Phase 9.
- **Phase 9:** If the single-scatter/escape MC shows multi-scatter or the >1 MeV a₁ tail materially changing the recoil spectrum, revisit the flat-box single-scatter approximation before folding downstream.
- **Phase 10:** If the assumed assay cannot bound the housing (α,n) budget, flag for a NeuCBOT cross-check and widen the uncertainty band rather than reporting a false-precision rate.
- **Phase 11:** If the exposure/cool-down scenario is unbounded, widen the ³H normalization band and revisit the Phase 7 default.
- **Phase 12:** If any channel breaks count-conservation (>1e-3) or the v1.0 muon-invariant test fails, revisit the fold before assembling the budget. **Project stop-condition:** if the combined surface neutron+ER rate drives occupancy toward the 50 kHz pileup ceiling such that quiescent reconstruction is precluded, escalate as a stop/rethink condition.

## Progress

**Execution Order:** Phases execute in numeric order: 7 → 8 → 9 → 10 → 12, with 11 parallelizable after 7.

| Phase | Milestone | Plans Complete | Status | Completed |
| ----- | --------- | -------------- | ------ | --------- |
| 7. Scenario & Nuclear-Data Lock | v1.1 | 0/TBD | Not started | - |
| 8. Neutron Source Terms | v1.1 | 0/TBD | Not started | - |
| 9. Neutron Transport & Recoil Fold | v1.1 | 0/TBD | Not started | - |
| 10. Detector Radioactivity Budget | v1.1 | 0/TBD | Not started | - |
| 11. Cosmogenic Activation Inventory | v1.1 | 0/TBD | Not started | - |
| 12. Response Fold & Combined In-Band Budget | v1.1 | 0/TBD | Not started | - |

## Notes

Phase numbering continues across milestones (v1.0 = Phases 1–6; v1.1 = Phases 7–12). All v1.1 spectra live on the unified phonon scale (CONVENTIONS §B, no ionization quenching) and fold through the v1.0 non-paralyzable 25 kHz `R(E_rec|E_dep)` matrices (CONVENTIONS §F). The three external normalizations are representative cited defaults with an explicit band (fixed in Phase 7); the modeled in-band floor is a lower bound (LEE unmodeled). CONVENTIONS.md already exists from v1.0 — the notation-coordinator handoff is skipped for this continuation.
