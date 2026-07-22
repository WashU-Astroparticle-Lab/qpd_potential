# QPD Particle-Physics Potential

## What This Is

A study of the particle-physics potential of a Quantum Parity Detector (QPD) based experiment: sensitivity projections for reactor CEvNS and, in a later milestone, light dark matter. The first stage delivers a rough estimate of three channels in *reconstructed* energy for a 4″×4″×2 mm single-sided Ge wafer (~110 g) read out by QPDs: the reactor-CEvNS signal, the cosmic-ray muon background, and the environmental-gamma Compton background. It uses an analytic/Monte-Carlo response chain (no G4CMP). Expected deliverables: figures, code, and an assumptions note.

## Core Research Question

What are the reactor-CEvNS, cosmic-ray-muon, and environmental-gamma Compton differential rate spectra in reconstructed energy for a 4″×4″×2 mm single-sided Ge wafer read out by QPDs with Ta→Al and Al→Hf trapping designs, given the stated efficiency and bandwidth assumptions?

## Current Milestone: v2.0 QPD at the NUCLEUS Chooz Very-Near-Site

**Goal:** Compute the reactor-CEvNS signal and the full in-band background budget in reconstructed energy for the ~110 g QPD Ge wafer **deployed at the NUCLEUS Very-Near-Site (VNS) behind the NUCLEUS shielding**, adopting that experiment's measured environment and shielding attenuation as input while re-folding the target response for Ge, and extending every spectrum down to **100 meV**.

**Target results:**

- Reactor-CEvNS dR/dE_rec at the VNS normalization (∫Φ = 2.1×10¹² ν̄/cm²/s; two Chooz-B cores, 4.25 GW_th each, at 72 m and 102 m; 80% duty), replacing the v1.0/v1.1 3 GW_th / 25 m scenario — signal drops ~3.6×.
- Residual background dR/dE_rec for Ge behind the NUCLEUS shielding: atmospheric neutrons (dominant), environmental gammas, atmospheric muons, and material radioactivity — each adopted from NUCLEUS's measured normalizations and attenuations, but folded through **Ge** cross sections and kinematics, not scaled from their CaWO₄/Al₂O₃ residuals.
- All spectra extended from the current 10.14 eV grid floor down to 100 meV, including the sub-eV regime below the per-sensor saturation onsets (~1.27 eV Ta→Al, ~0.77 eV Al→Hf), with the modeling validity of the unified phonon scale re-examined there.
- Signal-to-background in the 10–100 eV RoI and below, with the LEE carried as an explicit parameterized input, compared against NUCLEUS's published CaWO₄ (S/B ≈ 1.2) and Al₂O₃ (S/B ≈ 0.13) benchmarks.

**Headline risk (surfaced up front, not deferred):** Ge's CEvNS rate per kg is **2.31× below CaWO₄** in the 10–100 eV RoI — 176.8 vs 407.7 counts/kg/day/keV at 100% duty, both folded in *our own* pipeline at the VNS normalization, so the ratio is free of cross-source normalization error. Meanwhile the neutron background is only ~1.2–1.8× below, because Ge's T_max/E_n = 0.0536 vs W's 0.0215 spreads neutron recoils ~2.5× wider. Expected S/B ≈ 0.65–1.2 — at best ~1, plausibly below.

**Signal-side closure test (already passed):** our CaWO₄ fold reproduces NUCLEUS Table 5's CaWO₄ CEvNS entry (218.2 mcpd → 356.5 counts/kg/day/keV) to **14%**, consistent with the ~5% flux-shape residual of the VALD-02 anchor plus W-specific form-factor and kinematic differences. *Correction to an earlier claim: the compound N²/A for CaWO₄ is 44.2 (not 65.8, which is pure W), giving a naive scaling ratio of 1.95 against Ge's 22.7 — close to but not the same as the folded 2.31, so the naive ratio must not be used as the benchmark.*

**Which NUCLEUS number to anchor on (RESOLVED):** their §2 prose quotes 280 counts/kg/day/keV for CaWO₄ while their own Table 5 entry converts to 356.5 at their stated 6.8 g mass and 90 eV RoI — a factor 1.27. The rendered table has exactly one value per column, so this is not an extraction artifact. Our independent fold sits at 407.7, i.e. 1.14× the table value and 1.46× the prose value, so **Table 5 at 100% duty is the correct anchor**; the prose 280 is the 80%-duty number (356.5 × 0.8 = 285). Note their prose is internally inconsistent about this: the Al₂O₃ prose value (20) matches its table entry at *100%* duty (20.7), not 80%. Anchoring on the prose would have flattered our Ge S/B by ~27%.

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

- **[v2.0]** Reactor CEvNS spectrum at the **Chooz Very-Near-Site**: two Chooz-B cores, 4.25 GW_th each, at 72 m and 102 m, ∫Φ = 2.1×10¹² ν̄/cm²/s, 80% duty; 4-isotope Huber–Mueller-like antineutrino spectrum with an explicit sub-1.8 MeV treatment, Freedman cross section with Helm form factor on natural Ge. *(Supersedes the v1.0/v1.1 3 GW_th / 25 m scenario, which remains valid under its own stated premise.)*
- **[v2.0]** Residual particle backgrounds behind the **NUCLEUS shielding** (5 cm plastic-scintillator muon veto + 5 cm low-activity Pb + 20 cm 5%-borated HDPE; internal Pb/PE + ~4π 4 cm B₄C + cold muon veto; HPGe cryogenic outer veto at 1 keV_ee; Si inner veto), with NUCLEUS's measured normalizations and attenuations adopted and the **target response re-folded for Ge**.
- **[v2.0]** All spectra extended down to **100 meV**, two decades below the current 10.14 eV shared-grid floor and below the per-sensor saturation onsets (~1.27 eV Ta→Al, ~0.77 eV Al→Hf).
- Cosmic-ray muon deposit spectrum for the thin wafer at the VNS overburden (2.92 m.w.e., attenuation 1.41), including chord-length geometry (short vertical crossings, long near-horizontal chords) and Landau-Vavilov straggling.
- Environmental-gamma Compton electron-recoil spectrum driven by the **measured VNS gamma ambience** (5.03 cm⁻²s⁻¹; ⁴⁰K 59.6, ²³²Th 3.28, ²³⁸U 5.65 Bq/kg), thin-target single-scatter dominated, on Ge.
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
  - **[v2.0] SUPERSEDED as the absolute normalization** by the measured VNS ambience (ref-nucleus-bkg Table 2); retained for line composition and as a site-to-site sanity band.
- **ref-nucleus-bkg** *(v2.0, front-of-milestone INPUT)*: H. Abele et al. (NUCLEUS Collab.), Eur. Phys. J. C 86, 29 (2026), doi:10.1140/epjc/s10052-025-15168-9, arXiv:2509.03559
  - Why it matters: supplies the entire adopted environment — overburden 2.92 m.w.e., muon attenuation 1.41, VNS neutron spectrum (Fig. 4), gamma ambience (Table 2), material screening (Table 3), normalization uncertainties (Table 4), and the residual background benchmarks (Table 5)
  - Carry forward: planning | execution | verification — Required action: read | use | compare | cite
- **ref-nucleus-cevns** *(v2.0)*: G. Angloher et al. (NUCLEUS Collab.), Eur. Phys. J. C 79, 1018 (2019), doi:10.1140/epjc/s10052-019-7454-4, arXiv:1905.10258
  - Why it matters: Fig. 1 Ge CEvNS curve — reproduced to 5% under their own assumptions by the VALD-02 anchor (`tests/test_cevns_nucleus.py`); establishes the VNS site geometry
  - Carry forward: execution | verification — Required action: compare | cite

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

- [RESOLVED v1.0 Phase 5] Saturated-regime reconstruction — non-paralyzable dead-time model, user decision 2026-07-21.
- [RESOLVED v1.0 Phase 5] Ta→Al tunneling parameters — Table II Al-trap column; Ta absorber gap is a binary trapping gate.
- [RESOLVED v2.0] Absolute environmental gamma flux — the measured VNS ambience (5.03 cm⁻²s⁻¹, ref-nucleus-bkg Table 2) replaces the Heusser factor-2 band.
- **[v2.0 OPEN, gating]** Does a 4″×4″×2 mm, ~110 g Ge wafer fit the NUCLEUS COV/IV veto envelope, which is dimensioned for 6.8 g CaWO₄ / 4.5 g Al₂O₃ 3×3 arrays? If not, the adopted veto rejection factors do not transfer and the milestone premise must be revisited. **Must be checked before the background chain is built on top of it.**
- **[v2.0 OPEN, gating]** Reaching 100 meV recoil requires ν̄ down to **58.7 keV**, but the frozen flux table floors at 100 keV — which only feeds recoils ≥ 0.290 eV. Extending it enters a region where the reactor ν̄ spectrum is a model placeholder with no measurement, weaker even than the existing sub-1.8 MeV placeholder. How is the sub-100 keV flux to be bounded, and with what uncertainty?
- **[v2.0 OPEN]** Is the unified phonon scale (no quenching, E_rec ≈ 0.5·E_dep) still defensible between 100 meV and ~20 eV? Ge nuclear recoils there sit below the ~15–20 eV displacement threshold and approach the ~37 meV optical-phonon scale, so the recoiling-free-nucleus picture that underlies the CEvNS kinematics does not obviously apply.
- **[v2.0 OPEN]** What LEE amplitude and spectral shape should be carried? It is absent from the NUCLEUS particle-background budget yet is plausibly dominant below ~100 eV on a phonon-only device.

## Research Questions

### Answered

- [x] What does the reactor CEvNS spectrum look like in reconstructed energy for the two trapping designs? — **v1.0:** reconstructs to tens of eV (peak ~42 eV, ~85% of counts below 100 eV); linear E_rec≈0.5·E_dep mapping since all reactor recoils lie below the saturation onset. Absolute rate anchored to Billard within 2.4%.
- [x] What does the sea-level muon spectrum look like in reconstructed energy? — **v1.0:** the 1.5–197 MeV muon deposits all saturate the 25 kHz readout and pile up at a single ~18.8/15.0 keV reconstructed feature — an *instrumental artifact of the bandwidth ceiling*, not a physical line. Integral rate 1.366 Hz (within ~20% of PDG).
- [x] What does the environmental-gamma Compton spectrum look like in reconstructed energy? — **v1.0:** Klein–Nishina electron-recoil continuum reconstructing to a sub-keV–few-keV region; edges at 1243/1541/2382 keV; single-scatter rate 0.267 Hz (site-flux band ×2).
- [x] What is the E_rec(E_dep) response, effective threshold, and saturation onset for each design? — **v1.0:** MC response matrix R(E_rec|E_dep) with non-paralyzable censoring; per-sensor onset 1.27/0.77 eV, crossover band ~53/32 eV (default), whole-array plateau ~18.6/11.3 keV. Saturated-regime shape validated by limiting cases only (no literature anchor).

### Active (v2.0 — this milestone)

- [ ] What is the reactor-CEvNS spectrum in E_rec at the VNS normalization (2.1×10¹² ν̄/cm²/s, 80% duty), and how far does it fall relative to the v1.0 3 GW_th / 25 m flagship?
- [ ] What is the residual background in E_rec for a Ge wafer behind the NUCLEUS shielding — atmospheric neutrons (dominant), environmental gammas, atmospheric muons, material radioactivity — folded through Ge rather than transferred from CaWO₄/Al₂O₃?
- [ ] Does a ~110 g, 4″×4″×2 mm Ge wafer physically fit the NUCLEUS COV/IV veto envelope, which is built around gram-scale targets? If not, the adopted veto rejection factors are invalid and the milestone premise needs revisiting.
- [ ] What do all channels look like down to 100 meV, two decades below the current grid floor and below the per-sensor saturation onsets — and does the unified phonon scale (no quenching, E_rec ≈ 0.5·E_dep) still hold there?
- [ ] What is the achievable S/B in the 10–100 eV RoI and below, once the LEE is carried as an explicit parameterized input rather than omitted?

### Deferred (future milestones)

- [ ] Manuscript revision per the round-1 peer review (completeness scope caveat, ε vs η_ce, citations, venue) and a quantitative sensitivity/payoff.

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
| Reactor **[v2.0]** | P_th, L | 2 × 4.25 GW_th at 72 m / 102 m (Chooz VNS) | ∫Φ = 2.1×10¹² ν̄/cm²/s, 80% duty (was 3 GW_th at 25 m, 7.5×10¹²) |
| Overburden **[v2.0]** | m₀ | 2.92 ± 0.01 m.w.e. | muon attenuation 1.41 ± 0.02 (was sea level, none) |
| Spectrum floor **[v2.0]** | E_min | 100 meV | two decades below the v1.0 10.14 eV grid floor; needs ν̄ down to 58.7 keV |
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
| Adopt non-paralyzable dead-time censoring project-wide (CONVENTIONS §F) | Monotone, saturates cleanly at 1/τ_d; paralyzable retained only as a sensitivity | — Good (v1.0; user-verified in Phase 5) |
| Frame stage-1 as a feasibility forward model (no sensitivity/discovery claim) | Saturated-regime response has no literature anchor; keeps claims honest | — Good (v1.0; upheld by peer review) |
| **[v2.0] Relocate to the NUCLEUS Chooz VNS and assume the NUCLEUS shielding** | Self-projecting an unshielded surface background answers the wrong question; NUCLEUS's environment is measured, published, and 2–3 orders of magnitude lower | — Confirmed by user 2026-07-22 |
| **[v2.0] Adopt their environment, re-fold the target for Ge** | Scaling their CaWO₄/Al₂O₃ residuals by mass discards the target dependence the paper itself emphasizes; full Geant4 transport is out of scope for an analytic pipeline | — Confirmed by user 2026-07-22 |
| **[v2.0] Extend all spectra down to 100 meV** | Retracts the earlier 10 eV display floor; the sub-eV region is below both per-sensor saturation onsets and is where the QPD advantage and the LEE both live | — Confirmed by user 2026-07-22 |

Full log: `GPD/DECISIONS.md`

---

_Last updated: 2026-07-22 — started milestone v2.0 (QPD at the NUCLEUS Chooz Very-Near-Site); v1.1 Phases 8–12 superseded, Phase 7 carried forward_
