# Research Digest: v1.0 Reconstructed-Energy Spectra

Generated: 2026-07-22
Milestone: v1.0
Phases: 1–6

## Narrative Arc

Stage-1 asks what the three dominant surface-detector channels — reactor CEvNS, cosmic-ray muons, and environmental-gamma Compton — look like in *reconstructed* energy for a thin (~110 g) single-sided germanium wafer read out by Quantum Parity Detectors, and how a bandwidth-limited tunneling readout reshapes them. The work builds a single unified phonon energy scale with no ionization quenching (Phase 1), fixes the CEvNS cross-section convention and the 25 kHz dead-time censoring rule there, then computes each deposited-energy spectrum on that shared scale: a frozen reactor antineutrino flux (Phase 2) folded through the Freedman cross section to the CEvNS recoil spectrum benchmarked against Billard (Phase 3), and the two backgrounds — Gaisser–Guan⊗chord⊗Landau muons and Klein–Nishina Compton — against PDG and edge-kinematics anchors (Phase 4). All three deposited spectra are folded through a Monte-Carlo QPD response matrix R(E_rec|E_dep) with an explicit saturation onset (Phase 5) to yield the reconstructed-energy spectra for both trapping designs (Phase 6). The decisive finding: reactor CEvNS reconstructs to tens of eV (the flagship band), while the MeV-scale muon deposits all compress onto a single tens-of-keV pile-up that is an instrumental artifact of the bandwidth ceiling, not a physical line.

## Key Results

| Phase | Result | Equation / Value | Validity Range | Confidence |
|-------|--------|------------------|----------------|------------|
| 1 | Unified phonon scale + CEvNS convention fixed | dσ/dT = (G_F²M/4π)Q_W²(1−MT/2E_ν²)F²(q)(ħc)² | all channels, no quenching | HIGH |
| 2 | Frozen reactor flux | ∫Φ dE_ν = 7.5×10¹² ν̄/cm²/s at 3 GW_th, 25 m | E_ν 0.1–10 MeV; sub-1.8 MeV placeholder | HIGH (>1.8 MeV), band below |
| 3 | CEvNS deposited rate + benchmark | σ(⁷²Ge,4 MeV)=1.0026×10⁻⁴⁰ cm² (0.26%); Billard 0.742/0.501/0.257 (within 2.4%); 67.8 cts/kg/day >50 eV_nr | reactor recoils ≲3 keV_nr | HIGH |
| 4 | Muon + Compton deposited spectra | muon 1.366 Hz; ξ(MIP)=0.072 MeV, MPV 1.23 MeV; Compton 0.267 Hz, edges 1243/1541/2382 keV | thin-wafer single-scatter | HIGH edges; MEDIUM muon-norm/γ-flux |
| 5 | Response matrix + saturation | onset 1.27/0.77 eV; crossover ~53/32 eV; plateau ~18.6/11.3 keV; endpoint E_rec 34.8/26.8 keV | linear + saturated limits only | HIGH limits; model-only between |
| 6 | Reconstructed spectra | CEvNS peak ~42 eV (~85% <100 eV); muon pile-up 18.8/15.0 keV; Compton peak 16.8/13.3 keV; in-wafer rate 1.63 Hz, occupancy 3.3×10⁻⁵ | both designs | HIGH (folds validated) |

## Methods Employed

- **Phase 1:** Convention/dimensional foundation — unified phonon scale, (ħc)² unit discipline, dead-time censoring model (non-paralyzable / paralyzable switch).
- **Phase 2:** Reactor-flux modeling — Huber–Mueller conversion fits >2 MeV, seam-matched summation + ²³⁸U(n,γ) <1.8 MeV, monotone log-PCHIP interpolation, split uncertainty band.
- **Phase 3:** CEvNS fold — Freedman cross section, Lewin–Smith Helm form factor, per-isotope 5-isotope Ge sum, closed-form benchmark, Billard geometry+power k-rescale.
- **Phase 4:** Muon MC — Gaisser–Guan angular flux, ray–box chord sampling (Cauchy 4V/S), Landau–Vavilov MPV straggling; Compton MC — Klein–Nishina ⊗ Hubbell incoherent S(x,Z) binding, thin-target single-scatter.
- **Phase 5:** Forward QPD response — count-integral E_rec estimator, EMG tunneling-burst template (qpd repo), MC response matrix with crc32 sub-seeding, crossover-band scan.
- **Phase 6:** Counts-conserving log-log rebin + matrix fold; landing report; deliverable figures.

## Convention Evolution

| Phase | Convention | Description | Status |
|-------|-----------|-------------|--------|
| 1 | unified phonon scale, no quenching | T≡E_nr→E_ph→E_dep→E_rec, one axis for NR and ER | Active |
| 1 | CEvNS /4π + (ħc)² | prefactor and unit conversion locked | Active |
| 1 | bandwidth censoring switch | non-paralyzable vs paralyzable recorded as switch | Superseded by §F |
| 5 (§F) | non-paralyzable adopted | project-wide canonical; paralyzable = sensitivity | Active |
| — | display floor 10 eV | nothing below 10 eV shown on any figure | Active |

**Known bookkeeping drift:** `state.json` convention lock still marks `bandwidth_censoring` OPEN/"BLOCKS Phase 5" — resolve via `/gpd:validate-conventions` (LOW, zero physics impact).

## Figures and Data Registry

| File | Phase | Description | Paper-ready? |
|------|-------|-------------|--------------|
| paper/figures/reconstructed_energy_spectra.pdf | 6 | Fig. 1 — reconstructed + deposited overlay, both designs | Yes |
| paper/figures/true_reconstructed_mapping.pdf | 5/6 | Fig. 3 — E_rec(E_dep) mapping | Yes |
| paper/figures/energy_response.pdf | 5 | Fig. 2 — response matrix | Yes |
| paper/figures/cevns_dRdT_deposited.pdf | 3 | Fig. 4 — deposited CEvNS spectrum + band | Yes |
| artifacts/stage1/response_matrix_{TaAl,AlHf}.npz | 5 | committed response matrices | data |
| artifacts/stage1/reconstructed_spectra_{TaAl,AlHf}.csv | 6 | reconstructed spectra | data |
| data/{combined,muon,compton}_dRdEdep.csv, cevns_dRdT.csv | 3/4 | deposited spectra | data |
| notebooks/paper_calculations.ipynb | all | reproduces all 24 anchors end-to-end | Yes |

## Open Questions

1. Nuclear-recoil backgrounds (cosmic-ray & muon-induced neutrons, radiogenic (α,n)) land in the flagship CEvNS band with no NR/ER discrimination on the phonon scale — omitted in v1.0.
2. Detector-material intrinsic radioactivity and Ge cosmogenic activation (³H, ⁶⁸Ge, ⁶⁵Zn) — omitted.
3. ε=0.5 is a definitional efficiency ~40% above the paper's own η_ce≈0.3; all E_rec values scale linearly with it.
4. Saturated-regime response shape has no literature anchor (validated by limiting cases only).
5. No sensitivity/S:B or exposure-to-detection metric yet (deferred).
6. Manuscript needs the round-1 peer-review revisions (completeness scope caveat, citations incl. RELICS, venue prl→prd, affiliation).

## Dependency Graph

    Phase 1 (conventions/energy scale)  → enables 2, 4
    Phase 2 (reactor flux)              → 3
    Phase 3 (CEvNS dR/dT)              → 5
    Phase 4 (muon + Compton dR/dE_dep) → 5   [parallel with 2,3]
    Phase 5 (response matrix R)        → 6
    Phase 6 (fold → reconstructed spectra) → deliverables

Critical path: 1 → 2 → 3 → 5 → 6 (Phase 4 parallel).

## Mapping to Original Objectives

| Requirement | Status | Fulfilled by | Key Result |
|-------------|--------|--------------|------------|
| CONV-01 | Complete | Phase 1 | unified scale + convention |
| CALC-01 | Complete | Phase 2 | flux 7.5×10¹² (sub-1.8 MeV band) |
| CALC-02 | Complete | Phase 3 | dR/dT; σ 0.26% |
| CALC-03 | Complete | Phase 4 | muon 1.366 Hz |
| CALC-04 | Complete | Phase 4 | Compton 0.267 Hz, edges |
| SIMU-01 | Complete | Phase 5 | crossover band |
| SIMU-02 | Complete | Phase 5 | R(E_rec\|E_dep) |
| SIMU-03 | Complete | Phase 6 | reconstructed spectra |
| VALD-01 | Complete | Phase 3 | Billard 2.4% |
| VALD-02 | Complete | Phase 4 | muon flux ~20% |
| VALD-03 | Complete | Phase 4 | KN edges + rate |
| VALD-04 | Complete | Phase 5 | E_rec≈0.5·E_dep + saturation |
