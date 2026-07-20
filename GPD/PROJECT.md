# QPD Particle-Physics Potential

## What This Is

A study of the particle-physics potential of a Quantum Parity Detector (QPD) based experiment: sensitivity projections for reactor CEvNS and, in a later milestone, light dark matter. The first stage delivers a rough estimate of the reactor-CEvNS spectrum and the cosmic-ray muon spectrum in *reconstructed* energy for a 1 kg germanium target read out by QPDs, using an analytic/Monte-Carlo response chain (no G4CMP). Expected deliverables: figures, code, and an assumptions note.

## Core Research Question

What are the reactor-CEvNS and cosmic-ray-muon differential rate spectra in reconstructed energy for a 1 kg monolithic Ge crystal read out by QPDs with Ta→Al and Al→Hf trapping designs, given the stated efficiency and bandwidth assumptions?

## Scoping Contract Summary

### Contract Coverage

- **CEvNS spectrum (claim-cevns):** dR/dE_rec for both trapping designs; success = total rate agrees with published Ge reactor predictions (Billard et al. 2017, rescaled) within ~factor 2.
- **Muon spectrum (claim-muon):** sea-level muon spectrum in E_rec with the bandwidth-saturation regime made explicit; success = integral rate matches PDG sea-level flux through the crystal within ~30%.
- **Energy response (claim-response):** E_rec vs E_dep per design including saturation from the 25 kHz maximum resolvable tunneling rate; success = low-energy limit E_rec ≈ 0.5·E_dep and saturation onset both reproduced.
- **False progress to reject:** spectra reported in deposited energy only; muon spectrum without the 50 kHz bandwidth-saturation model.

### User Guidance To Preserve

- **User-stated observables:** CEvNS spectrum and muon spectrum *in terms of reconstructed energy*.
- **User-stated deliverables:** rough first-stage spectra (figures + pipeline code); response curve with saturation onset.
- **Must-have references / prior outputs:** QPD design paper (Ramanathan et al., APS Open Science 1, 000013 (2026), DOI 10.1103/kqd2-spb1); the exponentially-modified-Gaussian (EMG) pulse template in the `qpd` repo (`/Users/lanqingyuan/Documents/GitHub/qpd/src/qpd/simulator/quasiparticle_bursts.py`).
- **Stop / rethink conditions:** CEvNS reconstructed spectrum entirely below effective threshold for both designs; sea-level muon pileup makes quiescent reconstruction impossible at 50 kHz bandwidth.

### Scope Boundaries

**In scope**

- Reactor CEvNS spectrum: 3 GW_th commercial reactor at 25 m standoff, 4-isotope Huber–Mueller-like antineutrino spectrum, Freedman cross section with Helm form factor on natural Ge.
- Sea-level cosmic-ray muon deposit spectrum for a single monolithic 1 kg Ge crystal (no overburden).
- Response chain: E_dep → ~50% to signal (100% phonon collection × ph→QP losses) → trapped QP number → EMG-profiled tunneling burst → 50 kHz bandwidth-limited reconstruction, perfect tunneling identification.
- Both trapping designs: Ta absorber → Al trap/junction and Al absorber → Hf trap/junction.
- QPD sensor density of 1 per mm² on the crystal surface.

**Out of scope**

- G4CMP phonon-transport simulation (deferred).
- Dark-matter sensitivity projections (later milestone).
- Imperfect tunneling identification and readout-noise modeling.
- Backgrounds other than cosmic-ray muons.
- Detector geometry / sensor-layout optimization.

### Active Anchor Registry

- **ref-qpd-paper**: K. Ramanathan et al., APS Open Science 1, 000013 (2026), DOI 10.1103/kqd2-spb1
  - Why it matters: defines the QPD concept, efficiency chain (η_ph, η_pb, η_tr), pulse model Eq. (4), tunneling-rate formulation, Table II device parameters
  - Carry forward: planning | execution | verification
  - Required action: read | use | cite
- **ref-qpd-repo**: `/Users/lanqingyuan/Documents/GitHub/qpd/src/qpd/simulator/quasiparticle_bursts.py`
  - Why it matters: canonical EMG tunneling-burst template (Normal(µ,σ) + Exponential(τ) arrival times)
  - Carry forward: planning | execution
  - Required action: read | use
- **ref-huber**: P. Huber, Phys. Rev. C 84, 024617 (2011), arXiv:1106.0687
  - Why it matters: reactor antineutrino spectrum input
  - Carry forward: execution
  - Required action: use | cite
- **ref-cevns-benchmark**: J. Billard et al., J. Phys. G 44, 105101 (2017), arXiv:1612.09035
  - Why it matters: published Ge CEvNS reactor rate prediction — normalization cross-check
  - Carry forward: execution | verification
  - Required action: compare | cite
- **ref-pdg-muon**: Particle Data Group, Review of Particle Physics, cosmic-rays section (sea-level muon flux)
  - Why it matters: anchor for the integral sea-level muon rate
  - Carry forward: execution | verification
  - Required action: compare | cite

### Carry-Forward Inputs

- `/Users/lanqingyuan/Desktop/QPD.pdf` — local copy of the QPD design paper (user-supplied)
- `qpd` repo EMG burst model and materials database (`src/qpd/theory/materials.yaml`)
- No prior project-local outputs yet (fresh project)

### Skeptical Review

- **Weakest anchor:** the lumped ~50% deposited-energy-to-signal efficiency replaces the paper's design-dependent efficiency chain; Ta→Al device tunneling parameters (K, Γ_out, τ_qp) are extrapolated, not tabulated in the QPD paper (Table II covers Al- and Hf-junction devices).
- **Unvalidated assumptions:** perfect quasiparticle-tunneling identification; uniform phonon-energy sharing among QPD sensors; qpd-repo EMG template parameters apply to a 1 kg Ge crystal.
- **Competing explanation:** none identified yet.
- **Disconfirming observation:** computed total CEvNS rate off published Ge reactor predictions by more than an order of magnitude; response chain shows no saturation despite tunneling rates far above the 25 kHz Nyquist limit.
- **False progress to reject:** deposited-energy-only spectra; muon spectrum without saturation modeling.

### Open Contract Questions

- What crystal area is instrumented (one face vs all faces), fixing N_sens from the 1/mm² sensor density?
- How should reconstruction behave in the saturated regime: simple Nyquist rate-clip or a dead-time model?
- How should the Ta→Al device tunneling parameters be mapped from the paper's tabulated Al- and Hf-junction devices?

## Research Questions

### Answered

(None yet — investigate to answer)

### Active

- [ ] What does the reactor CEvNS spectrum look like in reconstructed energy for the two trapping designs?
- [ ] What does the sea-level muon spectrum look like in reconstructed energy, and where does bandwidth saturation dominate?
- [ ] What is the E_rec(E_dep) response, effective threshold, and saturation onset for each design?

### Out of Scope

- Dark-matter sensitivity projections — later milestone of this project.
- Full phonon-transport (G4CMP) detector response — deferred to a later stage.

## Research Context

### Physical System

A 1 kg monolithic high-purity Ge crystal instrumented on its surface with QPDs (superconducting charge-parity qubit sensors) at 1/mm² density. Energy deposits create phonons that break Cooper pairs in surface absorber films; quasiparticles trap into a lower-gap junction region and tunnel across a Josephson junction, flipping charge parity. The tunneling-event rate transient encodes the deposited energy.

### Theoretical Framework

Neutrino–nucleus coherent elastic scattering (standard-model Freedman cross section, Helm form factor); cosmic-ray muon energy loss (Bethe dE/dx, ~7.3 MeV/cm in Ge); superconducting quasiparticle dynamics (pair-breaking, trapping, tunneling per Ramanathan et al.); Poisson point-process pulse modeling with EMG arrival-time profile.

### Key Parameters and Scales

| Parameter | Symbol | Regime | Notes |
| --------- | ------ | ------- | ------- |
| Target mass | M | 1 kg Ge (~188 cm³, ~5.7 cm cube) | monolithic |
| Deposited→signal efficiency | ε | ~0.5 | 100% phonon collection × ph→QP losses |
| Signal bandwidth | f_bw | 50 kHz | max resolvable tunneling rate ~25 kHz (Nyquist) |
| Sensor density | n_s | 1 /mm² | N_sens = density × instrumented area (open question) |
| Trap gaps | Δ_tr | Al: ~180 µeV; Hf: ~20–40 µeV | design A: Ta→Al; design B: Al→Hf |
| Absorber gaps | Δ_abs | Ta: ~700 µeV; Al: ~190 µeV | Δ_abs/Δ_tr ≈ 4 both designs |
| Reactor | P_th, L | 3 GW_th at 25 m | ~1e13 ν/cm²/s |
| Muon flux | Φ_µ | ~1 /cm²/min (sea level) | no overburden |
| CEvNS recoil scale | E_R | ≲ few keV_nr for reactor ν on Ge | max recoil ~2E_ν²/M_N |

### Known Results

- QPD concept, efficiency chain, tunneling-rate model, and meV-scale absorbed-energy thresholds — Ramanathan et al., APS Open Science 1, 000013 (2026).
- Ge CEvNS rate predictions at a reactor — Billard et al., J. Phys. G 44, 105101 (2017).
- Reactor antineutrino spectra — Huber (2011), Mueller et al. (2011).

### What Is New

First estimate of what reactor CEvNS and cosmic muons look like in a QPD-instrumented kg-scale Ge detector *in reconstructed energy*, including the 50 kHz bandwidth saturation of the tunneling-rate readout — the first step toward CEvNS and dark-matter sensitivity projections for QPD arrays.

### Target Venue

Not yet chosen (internal projection study at this stage).

### Computational Environment

Local macOS workstation; Python (numpy/scipy/matplotlib); reuse of the `qpd` repo simulator components where useful. No cluster resources required at this stage.

## Notation and Conventions

See `GPD/CONVENTIONS.md` for all notation and sign conventions.

## Unit System

Detector/particle-physics practical units: energies in eV/keV/MeV, rates in counts/kg/day/keV, times in seconds, lengths in cm/µm. (No natural-units conversions needed at this stage.)

## Requirements

See `GPD/REQUIREMENTS.md` for the detailed requirements specification.

Key requirement categories: CALC (calculation), SIMU (simulation), VALD (validation)

## Key References

Mirror of the contract-critical anchors above: Ramanathan et al. (2026) [must-read], `qpd` repo EMG template [must-use], Huber (2011), Billard et al. (2017) [benchmark], PDG muon flux [benchmark].

## Constraints

- **Modeling fidelity**: analytic/Monte-Carlo response chain only — no G4CMP at this stage — because this is a rough first estimate.
- **Readout**: 50 kHz signal bandwidth — tunneling faster than ~25 kHz cannot be resolved — sets the saturation ceiling of the reconstruction.
- **Efficiency**: overall deposited-energy-to-signal efficiency fixed at ~50% by user specification.
- **Assumption**: perfect quasiparticle-tunneling identification — idealized readout for stage 1.

## Key Decisions

| Decision | Rationale | Outcome |
| -------- | --------- | --------- |
| Interpret designs as Ta→Al and Al→Hf (absorber→trap) | Trapping requires Δ_trap < Δ_absorber; matches the paper's two material combos | — Confirmed by user |
| Commercial 3 GW_th reactor at 25 m | Standard CONUS/Chooz-like scenario, highest reasonable flux | — Confirmed by user |
| Sea-level muon flux, no overburden | Conservative deployment assumption; muons then a dominant background | — Confirmed by user |
| Single monolithic 1 kg crystal | User choice over chip array; longer muon tracks, larger deposits | — Confirmed by user |
| Sensor density 1/mm² | User-specified | — Confirmed by user |

Full log: `GPD/DECISIONS.md`

---

_Last updated: 2026-07-20 after project initialization_
