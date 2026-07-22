# Prior Work: Reactor CEvNS + Cosmic Muons in Low-Threshold Ge with Quasiparticle-Tunneling Sensors

**Surveyed:** 2026-07-20
**Domain:** Neutrino physics (CEvNS), reactor antineutrino fluxes, cosmic-ray muons, superconducting quantum sensors
**Confidence:** HIGH overall (each entry carries its own level; derived estimates are labeled DERIVED)

**Project framing this survey serves:** differential rate spectra in *reconstructed* energy for reactor CEvNS and sea-level cosmic muons in a 1 kg monolithic Ge crystal read out by quantum parity detectors (QPDs; Ta absorber→Al trap and Al absorber→Hf trap), commercial 3 GW_th reactor at 25 m standoff, no overburden.

---

## Key Results

| Result | Expression / Value | Conditions | Source | Year | Confidence |
| --- | --- | --- | --- | --- | --- |
| SM CEvNS differential cross section | dσ/dE_R = (G_F²/4π) M Q_W² (1 − M E_R/2E_ν²) F²(q²), Q_W = N − Z(1 − 4 sin²θ_W) | E_ν ≲ 50 MeV (full coherence for reactor ν̄); F(q²) ≈ 1 at reactor energies | Freedman, PRD 9, 1389 (1974); form as used in Billard et al., J. Phys. G 44, 105101 (2017) | 1974 | HIGH |
| Max Ge recoil energy from reactor ν̄ | E_R^max = 2E_ν²/M ≈ 1.9 keV_nr for E_ν = 8 MeV on ⁷²·⁶Ge (M ≈ 67.6 GeV) | kinematic endpoint; most recoils ≪ 1 keV_nr | kinematics (DERIVED, standard) | — | HIGH |
| Predicted Ge CEvNS rate (phonon/recoil energy, no quenching) | 0.76 / 0.51 / 0.26 counts kg⁻¹ day⁻¹ above 50 / 100 / 200 eV_nr | 8.54 GW_th (two Chooz cores), 400 m standoff; Huber ²³⁵U,²³⁹Pu,²⁴¹Pu + Mueller ²³⁸U flux; fission fractions 55.6/32.6/7.1/4.7%; ν̄ spectrum taken constant below 2 MeV; ±5% rate uncertainty assumed | Billard et al., J. Phys. G 44, 105101 (2017), Table 1; arXiv:1612.09035 | 2017 | HIGH |
| Scaled to this project's scenario | ×(3/8.54)(400/25)² ≈ ×90 → ≈ 68 / 46 / 23 counts kg⁻¹ day⁻¹ above 50 / 100 / 200 eV_nr | 3 GW_th at 25 m, same flux model; pure 1/r² + power scaling, ignores core geometry and fuel-cycle differences | DERIVED from Billard Table 1 | 2026 | MEDIUM (derived anchor, must be recomputed in-project) |
| First reactor CEvNS observation (Ge) | 395 ± 106 events observed vs 347 ± 59 predicted (SM); 3.7σ | CONUS+, Leibstadt KKL, 3.6 GW_th at 20.7 m; 3 of 4 HPGe PPC detectors (total fiducial 3.73 ± 0.02 kg), thresholds 160–180 eVee; 119 live days reactor-on | Ackermann et al. (CONUS+), Nature 643, 1229 (2025); arXiv:2501.05206 | 2025 | HIGH |
| Implied CONUS+ signal rate | ≈ 1.0 counts kg⁻¹ day⁻¹ above ≈160 eVee (ionization energy) | 347 predicted / 119 d / ~2.8 kg used; ionization (quenched) energy scale, Lindhard-type yield | DERIVED from CONUS+ numbers above | 2026 | MEDIUM (derived) |
| CONUS upper limit (pre-observation) | < 85 CEvNS events (90% CL) in ROI | Brokdorf, 3.9 GW_th at 17.1 m; 248.7 kg·d ON / 58.8 kg·d OFF; quenching parameter k = 0.18 | Bonet et al. (CONUS), PRL 126, 041804 (2021) | 2021 | HIGH |
| Dresden-II "suggestive evidence" | > 3σ preference for CEvNS, only with elevated (Fef) quenching model | NCC-1701, 2.924 kg PPC HPGe, ~10 m from 2.96 GW_th Dresden-II BWR; signal region ≲ 0.4 keVee; contested (see Open Questions) | Colaresi et al., PRL 129, 211802 (2022) | 2022 | MEDIUM (claim is contested) |
| TEXONO/Kuo-Sheng limit | σ < 4.7 × SM (90% CL) at Lindhard k = 0.162 | electro-cooled p-type PPC Ge, 200 eVee threshold; 242 kg·d ON / 357 kg·d OFF at Kuo-Sheng reactor | arXiv:2411.18812 (TEXONO) | 2024 | MEDIUM-HIGH (arXiv, established group) |
| Ricochet detector performance | 30 eVee ionization resolution demonstrated; 40 eVee baseline at ILL site; science phase started July 2025 | 42 g Ge cryogenic bolometers (CryoCube), ILL research reactor, ν̄ flux ~10¹² cm⁻² s⁻¹ | Ricochet Collab., EPJ C 84 (2024); arXiv:2507.22751 (PRD 2025) | 2024–25 | HIGH |
| NUCLEUS status | ~20 eV nuclear-recoil thresholds in 10 g CaWO₄/Al₂O₃ gram-scale calorimeters; TUM commissioning complete, installing at Chooz | Chooz-B, between two 4.25 GW_th cores; first measurement targeted from ~2025–26 | NUCLEUS Collab., arXiv:2508.02488 (PRD 2025); arXiv:2211.04189 | 2025 | HIGH (status), MEDIUM (schedule) |
| Reactor ν̄ yield | ≈ 6 ν̄ per fission, ≈ 2 × 10²⁰ ν̄ s⁻¹ GW_th⁻¹ | standard fission ν̄ accounting; all energies | Hayes & Vogel, Ann. Rev. Nucl. Part. Sci. 66, 219 (2016), arXiv:1605.02047 | 2016 | HIGH |
| Flux at this project's detector | ~7–8 × 10¹² ν̄ cm⁻² s⁻¹ | 3 GW_th at 25 m, point-source 1/4πr² | DERIVED (consistent with CONUS+ ~1.4×10¹³ at 20.7 m / 3.6 GW) | 2026 | MEDIUM (derived) |
| Below-IBD-threshold ν̄ component | ²³⁸U(n,γ)²³⁹U (Q = 1.26 MeV) → ²³⁹Np (Q = 0.72 MeV) → ²³⁹Pu adds ~0.6 capture per fission; sizeable flux below 1.8 MeV never measured | equilibrium power reactor; component contributes at low E_ν only, hence only to lowest recoil energies | Kopeikin et al., Phys. At. Nucl. 67, 1892 (2004), hep-ph/0308186; Huber & Jaffke, PRL 116, 122503 (2016); Liao, Liu & Marfatia, PRD 108, 033002 (2023), arXiv:2302.10460 | 2004–23 | HIGH (existence), MEDIUM (spectral shape) |
| Sea-level vertical muon intensity | I_v ≈ 70 m⁻² s⁻¹ sr⁻¹ above 1 GeV/c ("~1 cm⁻² min⁻¹" through a horizontal surface); recent data favor 10–15% lower normalization; angular distribution ∝ cos²θ; mean E_μ ≈ 4 GeV | sea level, geomagnetic mid-latitudes, solar-cycle averaged | PDG Review of Particle Physics, "Cosmic Rays" (e.g., rpp2024) | ongoing | HIGH |
| Muon stopping power in Ge | ⟨dE/dx⟩_min = 1.370 MeV cm² g⁻¹; ρ = 5.323 g cm⁻³ → ≈ 7.3 MeV cm⁻¹; muon critical energy 298 GeV | minimum-ionizing muons (~0.3–100 GeV); restricted losses/straggling need Landau-Vavilov treatment | PDG Atomic & Nuclear Properties of Materials (Ge) | ongoing | HIGH |
| Typical muon deposit in cm-scale Ge | tens of MeV per through-going muon (e.g., ~40 MeV for ~5.7 cm vertical chord of a 1 kg cube); Landau-distributed with MPV below mean | sea-level spectrum; geometry-dependent chord distribution | DERIVED from PDG dE/dx; consistent with Ge γ-spectrometry background literature (e.g., Dortmund LBF, arXiv:1512.01824) | 2026 | MEDIUM (derived; exact spectrum is a project deliverable) |
| Muon rate through 1 kg Ge crystal | O(0.3–0.6) Hz | 1 kg Ge ≈ 188 cm³; e.g., cube face ~33 cm² × ~1 μ cm⁻² min⁻¹ with cos²θ acceptance and side entries; no overburden | DERIVED order-of-magnitude; project must compute properly with angular flux + chord geometry | 2026 | LOW-MEDIUM (derived; to be computed) |
| QPD concept and projected threshold | Charge-parity flip of a qubit-like element from quasiparticle tunneling bursts; meV-scale thresholds projected, sub-eV deposit thresholds on stated R&D path; readout, energy reconstruction, multiplexing schemes given | phonon-mediated sensing in crystalline substrate; sensor-array operation | Ramanathan et al., APS Open Science 1, 000013 (2026), DOI 10.1103/kqd2-spb1; arXiv:2405.17192 | 2026 | HIGH (published; thresholds are *projections*, not demonstrations) |
| QPD device demonstration | Quiescent quasiparticle density 1.8 ± 0.8 μm⁻³ measured in ion-milled phonon-mediated QPD; multi-step JJ fabrication without parasitic junctions | single prototype device; no energy threshold demonstrated yet | Sandoval et al., arXiv:2509.18637 | 2025 | MEDIUM-HIGH |
| SQUAT projected sensitivity | Sensitivity to 1 meV phonons in substrate and single THz photons predicted, μs timescale | transmon + quasiparticle-amplification stage; predictions, first demonstration in progress (FERMILAB-PUB-26-0007) | Fink et al., PRApplied 22, 054009 (2024), arXiv:2310.01345 | 2024 | HIGH (published projection) |
| QCD demonstrated single-photon sensitivity | Single 1.5 THz photons (~6 meV) counted; NEP < 10⁻²⁰ W Hz⁻¹ᐟ² | antenna-coupled quantum capacitance detector (photon-coupled, not phonon-mediated in massive crystal) | Echternach et al., Nat. Astron. 2, 90 (2018) | 2018 | HIGH |

---

## Foundational Work

### Freedman (1974) — Coherent neutrino-nucleus scattering

**Key contribution:** Predicted CEvNS in the SM: neutral-current elastic scattering off the whole nucleus with cross section ∝ Q_W² ≈ N² (sin²θ_W suppression of the proton contribution).
**Method:** Tree-level SM neutral-current calculation.
**Limitations:** None relevant at reactor energies; nuclear form factor F(q²) ≈ 1 (deviation ≲1% for Ge at reactor recoil energies).
**Relevance:** This is the signal cross section for the project. On natural Ge, sum over the five stable isotopes weighted by abundance (N varies 38–44).

### Billard et al. (2017) — Ge/Zn bolometers at Chooz (arXiv:1612.09035, J. Phys. G 44, 105101) — **project benchmark anchor**

**Key contribution:** End-to-end reactor-CEvNS sensitivity study for cryogenic *phonon* detectors, i.e., rates in true nuclear-recoil energy with **no ionization quenching** — the same energy variable a QPD-instrumented Ge crystal measures. Table 1 gives Ge: 0.76/0.51/0.26 counts kg⁻¹ day⁻¹ above 50/100/200 eV_nr for 8.54 GW_th at 400 m. Also provides a complete background budget template (Compton γ, cosmogenic fast neutrons, ²¹⁰Pb/³H/²⁰⁶Pb internal, ν̄–e⁻ scattering ~10⁻⁵ kg⁻¹ day⁻¹).
**Method:** Huber (²³⁵U, ²³⁹Pu, ²⁴¹Pu) + Mueller (²³⁸U) flux; spectrum approximated constant below 2 MeV; GEANT4 background propagation; reactor-on/off correlation analysis.
**Limitations:** 140 m.w.e. overburden site (our scenario has none — cosmogenics dominate differently); constant-below-2-MeV flux approximation is crude exactly where a low-threshold detector gains events; fixed fission fractions.
**Relevance:** Primary numerical validation anchor. Our scenario (3 GW_th, 25 m) is a ×~90 flux rescale of their Table 1 (DERIVED: ≈ 68/46/23 counts kg⁻¹ day⁻¹ above 50/100/200 eV_nr). Any in-project rate calculation should reproduce their Table 1 under their stated assumptions before rescaling.

### Huber (2011) & Mueller et al. (2011) — Conversion reactor ν̄ spectra

**Key contribution:** The standard "Huber–Mueller" (HM) reactor ν̄ spectrum model: conversion of the ILL measured fission-β spectra for ²³⁵U, ²³⁹Pu, ²⁴¹Pu (Huber, PRC 84, 024617, arXiv:1106.0687) plus summation-anchored ²³⁸U (Mueller et al., PRC 83, 054615, arXiv:1101.2663).
**Method:** Virtual-β-branch conversion of measured aggregate β spectra; per-fission spectra above ~2 MeV.
**Limitations:** (i) Defined only above ≈ 1.8–2 MeV — silent exactly where CEvNS with sub-100-eV thresholds gains rate; (ii) ~6% flux excess vs. data ("reactor antineutrino anomaly", Mention et al., PRD 83, 073006 (2011)), now largely attributed to a biased ILL ²³⁵U/²³⁹Pu β-ratio normalization (Kopeikin, Skorokhvatov & Titov, PRD 104, L071301 (2021), arXiv:2103.01684 — "KI" model) and supported by Daya Bay fuel-evolution data (PRL 118, 251801 (2017)); (iii) ~10% spectral distortion at 5–7 MeV ("bump") relative to HM.
**Relevance:** Use HM (or HM×KI-corrected normalization) above 2 MeV; the model choice is a leading systematic on the predicted CEvNS normalization (~5% level) and should be a stated assumption of the project's rate table.

### Kopeikin, Mikaelyan & Sinev (2004) + Huber & Jaffke (2016) — Below-IBD-threshold ν̄ emission

**Key contribution:** Catalogued the six components of reactor ν̄ emission including non-fission ν̄ from neutron capture: ²³⁸U(n,γ)²³⁹U (β, Q = 1.26 MeV, t₁/₂ = 23.5 min) → ²³⁹Np (β, Q = 0.72 MeV, t₁/₂ = 2.3 d), at ~0.6 capture per fission in a power reactor — a large ν̄ population entirely below the 1.8 MeV IBD threshold, plus capture on accumulated fission fragments (Phys. At. Nucl. 67, 1892, hep-ph/0308186; PRL 116, 122503).
**Method:** Summation from nuclear databases; reactor-physics capture rates.
**Limitations:** Never measured; summation carries database uncertainties (10%+ at low E_ν); component reaches equilibrium on the ²³⁹Np lifetime (days), so it correlates imperfectly with instantaneous reactor power.
**Relevance:** For a detector with eV–meV-scale thresholds, the sub-1.8 MeV flux contributes real rate at the lowest recoil energies (E_R ≲ 50 eV region). Liao, Liu & Marfatia (PRD 108, 033002 (2023), arXiv:2302.10460) show low-threshold CEvNS is the *only* way to probe this region and that establishing the neutron-capture component is hard even for NUCLEUS. The project must decide explicitly whether to include a below-2-MeV component (recommended: summation-based or the Kopeikin parametrization, stated as an assumption) since Billard et al. simply froze the spectrum below 2 MeV.

### Gaisser (1990, updated) + PDG Cosmic-Ray Review — Sea-level muon flux

**Key contribution:** Standard analytic sea-level muon spectrum: Gaisser's formula (Cosmic Rays and Particle Physics, CUP), valid for θ < 70°, E_μ > ~100/cosθ GeV; PDG canonical numbers: I_v ≈ 70 m⁻² s⁻¹ sr⁻¹ above 1 GeV/c (≈1 cm⁻² min⁻¹ horizontal), cos²θ zenith dependence near E_μ ~ 3 GeV, mean sea-level energy ≈ 4 GeV, with recent measurements favoring 10–15% lower normalization.
**Method:** Analytic cascade solution to atmospheric production; compilation of spectrometer data.
**Limitations:** Plain Gaisser fails at low energy (< few GeV) and large zenith angle — exactly the region carrying most of the sea-level rate. Use the modified Gaisser parametrization of Guan et al. (arXiv:1509.06176), which corrects both regimes.
**Relevance:** The muon differential rate in the 1 kg crystal is (flux model) ⊗ (chord-length distribution) ⊗ (Landau-Vavilov restricted energy-loss straggling at ⟨dE/dx⟩ ≈ 7.3 MeV/cm in Ge). All three pieces are established physics; the composition for this specific geometry/readout is the project's deliverable. Low-background Ge γ-spectrometry literature confirms through-muon deposits of tens of MeV in cm-scale HPGe (e.g., Dortmund Low Background Facility, arXiv:1512.01824).

### Ramanathan et al. (2026) — Quantum Parity Detectors (APS Open Science 1, 000013; DOI 10.1103/kqd2-spb1; arXiv:2405.17192) — **project design anchor**

**Key contribution:** Defines the QPD: phonons from particle interactions in a crystalline substrate drive a quasiparticle cascade in a surface-patterned superconducting element; single-quasiparticle tunneling across a coherent weak link flips the device charge parity — a binary, digital signature. Paper supplies readout schemes, energy-reconstruction methods (tunneling-rate/burst counting), multiplexing strategies for sensor arrays, and an R&D path to meV-scale thresholds and sub-eV deposit thresholds.
**Method:** Device modeling extending superconducting-qubit quasiparticle-poisoning physics (charge-parity switching) to deliberate particle detection.
**Limitations:** Thresholds are *projected*, not demonstrated; energy reconstruction saturates when the quasiparticle tunneling rate exceeds the readout bandwidth (the project's 50 kHz signal bandwidth / ~25 kHz max resolvable tunneling rate makes this the central reconstruction nonlinearity, especially for multi-MeV muon deposits); calibration of deposited-energy → tunneling-rate transfer function is design-dependent (Ta→Al vs Al→Hf gap hierarchies).
**Relevance:** This is the sensor model for the project. The reconstructed-energy spectrum calculation must implement this paper's rate-based energy estimator, including EMG-profiled burst pulse shapes and rate saturation, for both absorber/trap material stacks.

---

## Recent Developments

| Paper | Authors | Year | Advance | Impact on Our Work |
| --- | --- | --- | --- | --- |
| Nature 643, 1229; arXiv:2501.05206 | CONUS+ Collab. (Ackermann et al.) | 2025 | First direct observation of reactor CEvNS: 3.7σ, 395±106 events, 119 d, 3.73 kg HPGe fiducial, 160–180 eVee thresholds, 3.6 GW_th at 20.7 m | Closest existing experimental configuration to our scenario; anchors expected counts (~1 kg⁻¹ d⁻¹ above 160 eVee, DERIVED) and validates that commercial-reactor, ~20 m, few-kg Ge CEvNS is real and SM-consistent |
| arXiv:2407.11912; EPJ C 84 (2024) | CONUS+ Collab. | 2024 | Full setup description: 4 × ~1 kg PPC HPGe, shield design, site background at 20.7 m | Template for reactor-site backgrounds at shallow depth near a commercial core (though our scenario has *no* overburden) |
| PRL 133, 251802; arXiv:2401.07684 | CONUS Collab. | 2024 | Final Brokdorf limits (no signal at 210 eVee-class thresholds, 17.1 m, 3.9 GW_th) | Shows threshold, not flux, was the limiting factor pre-CONUS+ |
| PRL 134, 231801 (2025); arXiv:2406.13806 | COHERENT Collab. | 2024–25 | Evidence of CEvNS on natural Ge at the SNS (π-DAR source): 20.6 +7.1/−6.3 counts, 3.9σ, 1.5 keVee analysis threshold, 10.22 GWh·kg | Independent Ge quenching/cross-section cross-check; used in global Ge CEvNS fits (e.g., arXiv:2605.27121) |
| PRL 129, 211802 | Colaresi et al. (Dresden-II/NCC-1701) | 2022 | "Suggestive evidence" (>3σ) at ~10 m from 2.96 GW_th BWR with 2.924 kg PPC Ge | Contested — see Open Questions; matters to us mainly through the Ge ionization-yield controversy, which a phonon-based detector sidesteps |
| EPJ C 84 (2024) 12433; arXiv:2507.22751 (PRD 2025) | Ricochet Collab. | 2024–25 | 30 eVee ionization resolution; mini-CryoCube commissioning at ILL; science phase from July 2025 | State of the art for cryogenic Ge at a reactor; their reactor-on/off noise experience is directly relevant |
| arXiv:2508.02488 (PRD 2025) | NUCLEUS Collab. | 2025 | Full-system commissioning at TUM; moving to Chooz; ~20 eV thresholds in gram-scale crystals | Lowest demonstrated nuclear-recoil thresholds among reactor CEvNS experiments; sets the competitive context for meV-threshold projections |
| PRD 104, L071301; arXiv:2103.01684 | Kopeikin, Skorokhvatov, Titov | 2021 | Re-measured ²³⁵U/²³⁹Pu β ratio → 5% lower ²³⁵U flux (KI model), largely resolving the reactor antineutrino anomaly | Choose HM vs HM+KI normalization explicitly; ~5% normalization systematic on predicted rates |
| PRL 123, 022502 (2019), "Updated Summation Model: An Improved Agreement with the Daya Bay Antineutrino Fluxes" | Estienne, Fallot et al. | 2019 | Modern summation spectrum agreeing with measured Daya Bay IBD flux without anomaly | Candidate model for the below-2-MeV extension of the CEvNS flux |
| PRD 108, 033002; arXiv:2302.10460 | Liao, Liu, Marfatia | 2023 | Framework for probing the never-measured sub-1.8 MeV reactor flux with low-threshold CEvNS | Defines what our lowest reconstructed-energy bins are actually sensitive to |
| PRApplied 22, 054009; arXiv:2310.01345 | Fink et al. (SQUAT) | 2024 | Transmon + quasiparticle-amplification sensor; predicted 1 meV phonon sensitivity; first-demonstration paper in press (FERMILAB-PUB-26-0007) | Nearest-neighbor technology to QPDs; useful for cross-checking quasiparticle-cascade and threshold assumptions |
| arXiv:2509.18637 | Sandoval et al. | 2025 | Operated ion-milled phonon-mediated QPD; quiescent QP density 1.8±0.8 μm⁻³ as expected; parasitic-junction-free multi-step JJ process | Confirms baseline QP environment assumed in QPD energy reconstruction; still no demonstrated energy threshold |
| arXiv:2512.20309 | (QPD qubit-array study) | 2025 | Light-DM projections for QPD qubit arrays | Adjacent sensitivity study; check consistency of sensor-response modeling choices |
| Nature 594, 369 (2021) | Wilen et al. | 2021 | Cosmic rays/γs produce correlated charge-parity and phonon bursts across qubit chips | Direct experimental proof that ionizing radiation (including muons) drives exactly the parity-flip channel QPDs read out — i.e., our muon "background" signal is empirically established in qubit devices |

---

## Known Limiting Cases

| Limit | Known Result | Source | Verified By |
| --- | --- | --- | --- |
| F(q²) → 1 (reactor energies, Ge) | dσ/dE_R → (G_F²/4π) M Q_W² (1 − M E_R/2E_ν²); form-factor correction ≲ 1% | Billard et al. 2017; standard CEvNS reviews (e.g., arXiv:2203.07361) | COHERENT/CONUS+ SM consistency |
| Threshold → 0 | Total Ge CEvNS rate approaches flux-weighted total cross section; rate rises steeply below 100 eV_nr (≈50% gain from 100→50 eV in Billard Table 1) | Billard et al. 2017, Table 1 | — |
| Billard Table 1 reproduction | 0.76/0.51/0.26 kg⁻¹ d⁻¹ (Ge; 50/100/200 eV_nr; 8.54 GW; 400 m) | Billard et al. 2017 | required in-project validation target |
| CONUS+ counts | 347 ± 59 predicted events / 119 d / ~2.8 kg above 160–180 eVee (ionization scale, Lindhard-type quenching) | CONUS+ Nature 2025 | secondary in-project validation target (requires a quenching model to map from E_nr) |
| Muon MIP limit | ⟨dE/dx⟩ → 1.370 MeV cm² g⁻¹ in Ge (7.3 MeV/cm); deposit ≈ chord × 7.3 MeV/cm with Landau straggling | PDG Atomic & Nuclear Properties | — |
| Horizontal-detector muon rate | ≈ 1 cm⁻² min⁻¹ (with 10–15% downward revision) | PDG Cosmic Rays review | project geometry integral must reduce to this for a thin horizontal slab |

---

## Open Questions

1. **Dresden-II claim status** — The >3σ NCC-1701 result requires an ionization yield well above Lindhard below ~1.35 keV_nr (Fef model, YBe-calibrated). No single quenching model reconciles Dresden-II with COHERENT-Ge and CONUS+ simultaneously (e.g., arXiv:2605.27121); Migdal-effect explanations were examined and disfavored as a full explanation (arXiv:2307.12911). Community status: unconfirmed/contested. *Impact on us:* minimal for signal modeling (phonon readout has no ionization quenching), but it is the cautionary tale for low-energy energy-scale claims in Ge — our reconstructed-energy calibration assumptions deserve the same scrutiny.
2. **Reactor flux below 1.8 MeV** — Never measured; summation and neutron-capture components carry ≳10% shape uncertainty and imperfect power correlation (²³⁹Np equilibrium timescale). Determines the honest error band on our lowest reconstructed-energy bins.
3. **Ge quenching at E_nr < 1 keV** (relevant only if we ever compare to ionization-scale data) — Persistent measurement discrepancies; CONUS performed dedicated measurements; Lindhard k ≈ 0.16 vs k ≈ 0.18 choices shift ionization-scale predictions at the tens-of-% level near threshold.
4. **QPD energy reconstruction at high deposit energy** — No published demonstration of QPD energy reconstruction at any energy, let alone the multi-MeV muon regime where quasiparticle tunneling rates far exceed the ~25 kHz resolvable rate. The saturation/pile-up behavior of the rate-based estimator (with EMG burst shapes) is a genuinely open modeling question this project will answer in simulation; no literature result exists to anchor it (checked: arXiv:2405.17192, 2509.18637, 2310.01345 contain no high-energy saturation measurements).
5. **CONUS+ full-dataset significance** — Follow-ups (sub-keV ⁷¹Ge M-shell calibration, arXiv:2604.25748; parameter extractions, arXiv:2501.10355, 2501.17843, 2605.27121) are appearing; a higher-exposure CONUS+ result may sharpen the ~1 kg⁻¹ d⁻¹ anchor. Worth re-checking at phase-research time.

## Notation Conventions in the Literature

| Quantity | Standard Symbol(s) | Variations | Our Choice | Reason |
| --- | --- | --- | --- | --- |
| Nuclear recoil energy | E_R, E_nr, T | keV_nr vs keVee (ionization-equivalent) | E_nr in eV/keV_nr; reconstructed energy separately as E_rec | Phonon/QPD readout measures recoil energy; never mix with keVee without an explicit quenching model |
| Ionization-equivalent energy | E_ee (keVee) | "detected energy" in PPC papers | keVee, only when quoting CONUS+/TEXONO/Dresden-II | Their thresholds are ionization-scale |
| Quenching / ionization yield | Q(E_nr), Y, Lindhard k | k = 0.157–0.18 in Ge literature | not applied to signal model; k stated explicitly if mapping to keVee | Phonon detectors measure full recoil energy (no Luke gain either: no drift field) |
| Weak charge | Q_W = N − Z(1 − 4 sin²θ_W) | sign/factor conventions; sin²θ_W(0) ≈ 0.2387 vs on-shell | Billard et al. convention, low-E sin²θ_W | Match the benchmark anchor |
| Reactor ν̄ spectrum | dN/dE_ν per fission | per second per GW; per fission per MeV | per fission per MeV, weighted by fission fractions | HM/summation native units |
| Muon flux | dΦ/dE_μ dΩ | I_v (vertical intensity), J₁ (integrated) | differential in (E_μ, θ), Guan-modified Gaisser | Need low-E/large-θ validity for a surface detector |

## Sources

- Billard et al., J. Phys. G 44, 105101 (2017), arXiv:1612.09035 — benchmark Ge phonon-detector CEvNS rates (Table 1 read directly from the paper) and background budget template.
- Ackermann et al. (CONUS+), Nature 643, 1229–1233 (2025), arXiv:2501.05206; setup paper arXiv:2407.11912; background paper arXiv:2412.13707 — first reactor CEvNS observation, closest configuration to our scenario.
- Bonet et al. (CONUS), PRL 126, 041804 (2021); Ackermann et al., PRL 133, 251802 (2024), arXiv:2401.07684 — Ge limits at Brokdorf.
- Colaresi et al., PRL 129, 211802 (2022) — Dresden-II claim; critiques/global fits: arXiv:2202.10829, 2203.02414, 2208.13262, 2307.12911, 2605.27121.
- TEXONO, arXiv:2411.18812 — Kuo-Sheng PPC Ge limit (ρ < 4.7 SM at 200 eVee).
- Ricochet Collab., EPJ C 84 (2024) (30 eVee resolution); arXiv:2507.22751 (PRD 2025) — cryogenic Ge at ILL.
- NUCLEUS Collab., arXiv:2211.04189; arXiv:2508.02488 (PRD 2025) — gram-scale ~20 eV-threshold program at Chooz.
- Huber, PRC 84, 024617 (2011); Mueller et al., PRC 83, 054615 (2011); Mention et al., PRD 83, 073006 (2011); Kopeikin et al., PRD 104, L071301 (2021), arXiv:2103.01684; Estienne et al., PRL 123, 022502 (2019); Hayes & Vogel, ARNPS 66, 219 (2016), arXiv:1605.02047 — reactor flux models and anomaly status.
- Kopeikin, Mikaelyan, Sinev, Phys. At. Nucl. 67, 1892 (2004), hep-ph/0308186; Huber & Jaffke, PRL 116, 122503 (2016); Liao, Liu, Marfatia, PRD 108, 033002 (2023), arXiv:2302.10460 — below-IBD-threshold ν̄ components.
- PDG Review of Particle Physics, Cosmic Rays chapter; PDG Atomic & Nuclear Properties (Ge: 1.370 MeV cm²/g, ρ = 5.323 g/cm³, E_μc = 298 GeV); Gaisser, *Cosmic Rays and Particle Physics* (CUP); Guan et al., arXiv:1509.06176 — sea-level muon flux and energy loss.
- Ramanathan et al., APS Open Science 1, 000013 (2026), DOI 10.1103/kqd2-spb1, arXiv:2405.17192 — QPD concept, readout, energy reconstruction (project design anchor).
- Sandoval et al., arXiv:2509.18637 — QPD device operating characteristics (quiescent QP density).
- Fink et al., PRApplied 22, 054009 (2024), arXiv:2310.01345 (+ FERMILAB-PUB-26-0007) — SQUAT; Echternach et al., Nat. Astron. 2, 90 (2018) — QCD single-THz-photon counting.
- Wilen et al., "Correlated charge noise and relaxation errors in superconducting qubits", Nature 594, 369–373 (2021) — radiation-induced correlated charge/quasiparticle-poisoning events in qubit arrays (empirical basis for muon response of parity sensors).
