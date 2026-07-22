# QPD Particle-Physics Potential

## What This Is

A study of the particle-physics potential of a Quantum Parity Detector (QPD) based experiment: sensitivity projections for reactor CEvNS and, in a later milestone, light dark matter. The first stage delivers a rough estimate of three channels in *reconstructed* energy for a 4″×4″×2 mm single-sided Ge wafer (~110 g) read out by QPDs: the reactor-CEvNS signal, the cosmic-ray muon background, and the environmental-gamma Compton background. It uses an analytic/Monte-Carlo response chain (no G4CMP). Expected deliverables: figures, code, and an assumptions note.

## Core Research Question

What are the reactor-CEvNS, cosmic-ray-muon, and environmental-gamma Compton differential rate spectra in reconstructed energy for a 4″×4″×2 mm single-sided Ge wafer read out by QPDs with Ta→Al and Al→Hf trapping designs, given the stated efficiency and bandwidth assumptions?

## Scoping Contract Summary

### Contract Coverage

- **CEvNS spectrum (claim-cevns):** dR/dE_rec for both trapping designs; success = reproduce Billard Table 1 (~20%) and total rate agrees with published Ge reactor predictions (rescaled) within ~factor 2.
- **Muon spectrum (claim-muon):** sea-level muon spectrum in E_rec with thin-wafer chord-length geometry and the bandwidth-saturation regime made explicit; success = integral rate matches PDG sea-level flux through the wafer within ~30%.
- **Compton spectrum (claim-compton):** electron-recoil spectrum from a representative environmental radiogenic gamma background in E_rec, showing Compton continua/edges on the unified phonon scale; success = edges at Klein-Nishina energies and interaction rate within ~factor 2 of flux×cross-section.
- **Energy response (claim-response):** E_rec vs E_dep per design including saturation from the 25 kHz maximum resolvable tunneling rate; success = low-energy limit E_rec ≈ 0.5·E_dep and saturation onset both reproduced.
- **False progress to reject:** spectra in deposited energy only; muon spectrum without saturation/chord-length geometry; gamma channel as full-energy photopeaks instead of Compton continuum.

### User Guidance To Preserve

- **User-stated observables:** CEvNS, muon, and Compton spectra *in terms of reconstructed energy*.
- **User-stated deliverables:** rough first-stage spectra (figures + pipeline code); response curve with saturation onset.
- **Must-have references / prior outputs:** QPD design paper (Ramanathan et al., APS Open Science 1, 000013 (2026), DOI 10.1103/kqd2-spb1, arXiv:2405.17192); the EMG pulse template in the `qpd` repo (`/Users/lanqingyuan/Documents/GitHub/qpd/src/qpd/simulator/quasiparticle_bursts.py`).
- **Stop / rethink conditions:** CEvNS reconstructed spectrum entirely below effective threshold for both designs; muon/gamma pileup makes quiescent reconstruction impossible at 50 kHz bandwidth.

### Scope Boundaries

**In scope**

- Reactor CEvNS spectrum: 3 GW_th commercial reactor at 25 m standoff, 4-isotope Huber–Mueller-like antineutrino spectrum with an explicit sub-1.8 MeV treatment, Freedman cross section with Helm form factor on natural Ge.
- Cosmic-ray muon deposit spectrum (sea level, no overburden) for the thin wafer, including chord-length geometry (short vertical crossings, long near-horizontal chords) and Landau-Vavilov straggling.
- Environmental-gamma Compton electron-recoil spectrum: representative radiogenic background (U/Th chains + ⁴⁰K lines + continuum), thin-target single-scatter dominated, on Ge.
- Response chain: E_dep → ~50% to signal (100% phonon collection × ph→QP losses) → trapped QP number → EMG-profiled tunneling burst → 50 kHz bandwidth-limited reconstruction, perfect tunneling identification.
- Both trapping designs: Ta absorber → Al trap/junction and Al absorber → Hf trap/junction.
- Detector geometry: 4″×4″×2 mm Ge wafer (~110 g), single instrumented face at 1/mm² QPD density (~10,300 sensors).

**Out of scope**

- G4CMP phonon-transport simulation (deferred).
- Dark-matter sensitivity projections (later milestone).
- Imperfect tunneling identification and readout-noise modeling.
- Neutron-induced nuclear-recoil backgrounds and backgrounds beyond cosmic muons and environmental-gamma Compton.
- Detector geometry / sensor-layout optimization.

### Active Anchor Registry

- **ref-qpd-paper**: K. Ramanathan et al., APS Open Science 1, 000013 (2026), DOI 10.1103/kqd2-spb1, arXiv:2405.17192
  - Why it matters: QPD concept, efficiency chain (η_ph, η_pb, η_tr), pulse model Eq. (4), tunneling-rate formulation, Table II device parameters
  - Carry forward: planning | execution | verification — Required action: read | use | cite
- **ref-qpd-repo**: `/Users/lanqingyuan/Documents/GitHub/qpd/src/qpd/simulator/quasiparticle_bursts.py`
  - Why it matters: canonical EMG tunneling-burst template
  - Carry forward: planning | execution — Required action: read | use
- **ref-huber**: P. Huber, Phys. Rev. C 84, 024617 (2011), arXiv:1106.0687 — reactor antineutrino spectrum input — use | cite
- **ref-cevns-benchmark**: J. Billard et al., J. Phys. G 44, 105101 (2017), arXiv:1612.09035 — Ge CEvNS reactor rate normalization cross-check — compare | cite
- **ref-pdg-muon**: PDG, PTEP 2022, 083C01 (2022), Cosmic Rays review — integral sea-level muon rate anchor — compare | cite
- **ref-environmental-gamma**: G. Heusser, Annu. Rev. Nucl. Part. Sci. 45, 543 (1995) — environmental radiogenic gamma lines/flux for the Compton channel — use | cite

### Carry-Forward Inputs

- `/Users/lanqingyuan/Desktop/QPD.pdf` — local copy of the QPD design paper (user-supplied)
- `qpd` repo EMG burst model and materials database (`src/qpd/theory/materials.yaml`)
- CONUS+ (Nature 643, 1229 (2025), arXiv:2501.05206): observed reactor CEvNS on Ge at 3.6 GW_th, 20.7 m — secondary cross-check
- No prior project-local outputs yet (fresh project)

### Skeptical Review

- **Weakest anchor:** lumped ~50% deposited-to-signal efficiency replaces the paper's design-dependent chain; Ta→Al device tunneling parameters extrapolated (Table II covers Al- and Hf-junction devices); environmental gamma flux normalization is a representative assumption, not a site measurement.
- **Unvalidated assumptions:** perfect tunneling identification; uniform phonon-energy sharing among ~10,300 sensors; qpd-repo EMG template applies to a Ge wafer; thin-wafer single-Compton-scatter dominance.
- **Competing explanation:** none identified yet.
- **Disconfirming observation:** total CEvNS rate off published Ge predictions by >1 order of magnitude; no saturation despite tunneling rates ≫25 kHz; Compton edges at energies inconsistent with Klein-Nishina.
- **False progress to reject:** deposited-energy-only spectra; muon spectrum without saturation/geometry; gamma photopeaks instead of Compton continuum.

### Open Contract Questions

- How should reconstruction behave in the saturated regime: Nyquist rate-clip or a dead-time model (paralyzable vs non-paralyzable)?
- How should the Ta→Al device tunneling parameters be mapped from the paper's tabulated Al- and Hf-junction devices?
- What absolute environmental gamma flux/line composition best represents a surface-level reactor-site deployment?

## Research Questions

### Answered

(None yet — investigate to answer)

### Active

- [ ] What does the reactor CEvNS spectrum look like in reconstructed energy for the two trapping designs?
- [ ] What does the sea-level muon spectrum look like in reconstructed energy, given thin-wafer chord geometry and where bandwidth saturation dominates?
- [ ] What does the environmental-gamma Compton spectrum look like in reconstructed energy in this thin wafer?
- [ ] What is the E_rec(E_dep) response, effective threshold, and saturation onset for each design?

### Out of Scope

- Dark-matter sensitivity projections — later milestone of this project.
- Full phonon-transport (G4CMP) detector response — deferred to a later stage.

## Research Context

### Physical System

A 4″×4″×2 mm (~110 g) high-purity Ge wafer instrumented on one face with QPDs (superconducting charge-parity qubit sensors) at 1/mm² density (~10,300 sensors). Energy deposits create phonons that break Cooper pairs in surface absorber films; quasiparticles trap into a lower-gap junction region and tunnel across a Josephson junction, flipping charge parity. The tunneling-event rate transient encodes the deposited energy. Three deposit channels are studied: nuclear-recoil CEvNS, through-going/near-horizontal muons, and Compton electron recoils from environmental gammas — all on one unified phonon energy scale (no ionization quenching).

### Theoretical Framework

Neutrino–nucleus coherent elastic scattering (Freedman cross section, Helm form factor); cosmic-ray muon energy loss (Bethe dE/dx ~7.3 MeV/cm in Ge, Landau-Vavilov straggling, Gaisser-Guan angular flux); Compton scattering (Klein-Nishina) of environmental gammas; superconducting quasiparticle dynamics (pair-breaking, trapping, tunneling per Ramanathan et al.); Poisson point-process pulse modeling with EMG arrival-time profile.

### Key Parameters and Scales

| Parameter | Symbol | Regime | Notes |
| --------- | ------ | ------- | ------- |
| Wafer | — | 4″×4″×2 mm ≈ 20.6 cm³ | ~110 g Ge (ρ=5.323 g/cm³) |
| Sensors | N_sens | ~10,300 | single face, 1/mm² |
| Deposited→signal efficiency | ε | ~0.5 | 100% phonon collection × ph→QP losses |
| Signal bandwidth | f_bw | 50 kHz | max resolvable tunneling rate ~25 kHz (Nyquist) |
| Trap gaps | Δ_tr | Al: ~180 µeV; Hf: ~20–40 µeV | design A: Ta→Al; design B: Al→Hf |
| Absorber gaps | Δ_abs | Ta: ~700 µeV; Al: ~190 µeV | Δ_abs/Δ_tr ≈ 4 both designs |
| Vertical muon deposit | — | ~1.5 MeV (MPV ~1 MeV) | 7.3 MeV/cm × 0.2 cm; long chords → tens of MeV |
| Reactor | P_th, L | 3 GW_th at 25 m | ~1e13 ν/cm²/s |
| Muon flux | Φ_µ | ~1 /cm²/min (sea level) | no overburden |
| Env. gamma | — | U/Th + ⁴⁰K lines + continuum | representative surface-lab flux |
| CEvNS recoil scale | E_R | ≲ few keV_nr for reactor ν on Ge | max recoil ~2E_ν²/M_N |

### Known Results

- QPD concept, efficiency chain, tunneling-rate model, meV-scale thresholds — Ramanathan et al. (2026).
- Reactor CEvNS on Ge observed — CONUS+ (Nature 643, 1229 (2025)); Ge rate predictions — Billard et al. (2017).
- Reactor antineutrino spectra — Huber (2011), Mueller et al. (2011); sub-1.8 MeV region unmeasured.
- Environmental radioactivity backgrounds — Heusser (1995).

### What Is New

First estimate of what reactor CEvNS, cosmic muons, and environmental-gamma Compton scattering look like in a QPD-instrumented thin Ge wafer *in reconstructed energy*, including the 50 kHz bandwidth saturation of the tunneling-rate readout — the first step toward CEvNS and dark-matter sensitivity projections for QPD arrays.

### Target Venue

Not yet chosen (internal projection study at this stage).

### Computational Environment

Local macOS workstation; Python (numpy/scipy/matplotlib); reuse of the `qpd` repo simulator components where useful. No cluster resources required at this stage.

## Notation and Conventions

See `GPD/CONVENTIONS.md` for all notation and sign conventions.

## Unit System

Detector/particle-physics practical units: energies in eV/keV/MeV, rates in counts/kg/day/keV, times in seconds, lengths in cm/µm. Natural units used internally for the cross section with (ħc)² = 3.894×10⁻²⁸ GeV²·cm².

## Requirements

See `GPD/REQUIREMENTS.md` for the detailed requirements specification.

Key requirement categories: CALC (calculation), SIMU (simulation), VALD (validation)

## Key References

Mirror of the contract-critical anchors above: Ramanathan et al. (2026) [must-read], `qpd` repo EMG template [must-use], Huber (2011), Billard et al. (2017) [benchmark], PDG muon flux [benchmark], Heusser (1995) [background].

## Constraints

- **Modeling fidelity**: analytic/Monte-Carlo response chain only — no G4CMP at this stage — because this is a rough first estimate.
- **Readout**: 50 kHz signal bandwidth — tunneling faster than ~25 kHz cannot be resolved — sets the saturation ceiling.
- **Efficiency**: overall deposited-energy-to-signal efficiency fixed at ~50% by user specification.
- **Geometry**: 4″×4″×2 mm single-sided wafer, 1/mm² sensors — thin target ⇒ short vertical muon chords and single-Compton-scatter dominance.
- **Assumption**: perfect quasiparticle-tunneling identification — idealized readout for stage 1.

## Key Decisions

| Decision | Rationale | Outcome |
| -------- | --------- | --------- |
| Interpret designs as Ta→Al and Al→Hf (absorber→trap) | Trapping requires Δ_trap < Δ_absorber; matches the paper's two material combos | — Confirmed by user |
| Commercial 3 GW_th reactor at 25 m | Standard CONUS/Chooz-like scenario, highest reasonable flux | — Confirmed by user |
| Sea-level muon flux, no overburden | Conservative deployment assumption; muons a dominant background | — Confirmed by user |
| 4″×4″×2 mm single-sided wafer (drop 1 kg framing) | Matches actual QPD wafer form factor; rates quoted per-detector and per-kg | — Confirmed by user |
| Add environmental-gamma Compton channel | User wants to see Compton from detector radiation in this geometry | — Confirmed by user (radiogenic bkg) |
| Sensor density 1/mm² on one face | User-specified | — Confirmed by user |

Full log: `GPD/DECISIONS.md`

---

_Last updated: 2026-07-20 after geometry revision and Compton-channel addition_
