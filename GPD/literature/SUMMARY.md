# Research Summary — v2.0 QPD at the NUCLEUS Chooz Very-Near-Site

**Project:** QPD Particle-Physics Potential — reactor-CEvNS signal and full in-band background budget in reconstructed energy for a ~110 g (4″×4″×2 mm) single-sided QPD Ge wafer
**Milestone:** v2.0 — deployment at the NUCLEUS Chooz Very-Near-Site (VNS) behind the NUCLEUS shielding, environment adopted / target response re-folded for Ge, all spectra extended to **100 meV**
**Domain:** Shielded rare-event cryogenic-detector background transfer; sub-eV nuclear recoil in a crystal; reactor antineutrino flux below the IBD threshold
**Researched:** 2026-07-22 · **Synthesized:** 2026-07-22
**Confidence:** MEDIUM-HIGH overall. HIGH on the flux/response factorization, the NUCLEUS anchor arithmetic, the impulse-regime kinematics, and the tooling verdicts. MEDIUM on the sub-eV quantum-broadening magnitude (framework textbook, Ge numbers derived in-survey). LOW on the LEE amplitude — irreducibly a scenario input.

> This replaces the v1.1 survey (archived at `GPD/milestones/v1.1/literature/SUMMARY.md`). The v1.0/v1.1 validated physics — Freedman/Helm CEvNS, Huber–Mueller flux, Gaisser–Guan ⊗ chord ⊗ Landau, Klein–Nishina, the 25 kHz non-paralyzable `R(E_rec|E_dep)` chain, and the frozen ENDF/B-VIII.0 n-Ge elastic set with `T_max/E_n = 0.0536` — is **reused, not re-surveyed**.

## Executive Summary

The four scouts converge on one structural statement that should govern the whole milestone: **only the target-independent fluence `φ(E)` at the detector position transfers from NUCLEUS to us; every deposit spectrum, residual rate, and veto factor they publish is a `φ ⊗ kernel ⊗ payload` product and must not be rescaled to Ge.** NUCLEUS's headline ~250 d⁻¹kg⁻¹keV⁻¹ residual is a property of their *setup* — a 6.8 g CaWO₄ array inside a cryogenic outer veto, an inner veto, a 4 cm B₄C liner, and a multiplicity cut — not of the VNS site. Our 4″×4″ wafer has ~11× the footprint (≈103 vs ≈9 cm²), is a single monolithic detector with no multiplicity handle, and carries ~10,300 sensor films. The correct posture is a two-layer adoption: **L1 (environmental — overburden 2.92 m.w.e., Table 4 fluxes, passive external-shield attenuation) transfers; L2 (payload-coupled — COV factor 5, IV, multiplicity) defaults to 1.0 and must be earned.** Whether the wafer even fits the COV/IV envelope is the gating question of the milestone, because if it forces a shield change then `φ` at the detector position is no longer NUCLEUS's `φ` and *nothing* transfers.

The anchor arithmetic is settled and should not be relitigated. Anchor on NUCLEUS **Table 5 at 100% duty**, not the §2 prose: the rendered PDF has one value per column (CEvNS 218.2 / 60.7 / 8.4 / –), 218.2 mcpd ÷ (6.8 g × 0.09 keV) = **356.5** d⁻¹kg⁻¹keV⁻¹, and our independent CaWO₄ fold gives **407.7** (ratio 1.14) against the prose 280 (ratio 1.46). The prose 280 is the 80%-duty value (356.5 × 0.8 = 285) and the paper is internally inconsistent about it — the Al₂O₃ prose value (20) matches its table entry at *100%* duty (20.7). The signal-side closure test therefore **passes at 14%**. Same-pipeline, 10–100 eV, 100% duty, Ge gives **176.8** vs CaWO₄ **407.7**, a ratio of **2.31**; the naive compound N²/A ratio is 1.95 (CaWO₄ compound N²/A = 44.2, *not* 65.8, which is pure W) and must not be used as the benchmark. With the neutron background only ~1.2–1.8× below CaWO₄ — because Ge's `T_max/E_n = 0.0536` spreads recoils ~2.5× wider than W's 0.0215 — the expected **S/B_particle ≈ 0.65–1.2**, at best ~1.

The 100 meV extension is not a plotting change and not a numerics problem (744 vs 584 bins). It is a physics-regime change with one dominant new input. Sub-100-keV flux truncation is **not** gating (bound ≤ 0.81% at T = 100 meV, exactly zero above 0.29 eV; `E_min(100 meV) = 58.16 keV`) — report the bound, do not extend the table. The unified phonon scale is *strengthened* in-window by the SuperCDMS Ge displacement threshold. What is genuinely new and load-bearing is **impulse-approximation quantum broadening**: at `2W = E_R/ω̄ ≈ 4.7–8.3` at 100 meV the recoil is not a delta at `E_R` but a distribution of fractional width `1/√(2W)` ≈ 35–46%, falling to 15.5–20.5% at the newly-adopted 0.5 eV threshold. That is **comparable to the detector's own resolution floor** — which this project has never parameterized, and which is emergent counting statistics only: `total_N_obs` = 39.4 (Ta→Al) / 49.9 (Al→Hf) at 0.5 eV gives a Poisson floor of 15.9%/14.2%, best case with no baseline, amplifier, phonon-collection, position, or readout noise. **Two comparable smearing mechanisms sit at the analysis threshold and only one of them is in the model.** In quadrature they give ~22–26%, which acts directly on a steeply-varying trigger curve at 0.5 eV and therefore moves the effective threshold and the counted rate — this is the single highest-value physics addition of v2.0. Behind it, the largest *irreducible* uncertainty is the LEE, which for a QPD is design-dependent (Romani's Al-film dislocation model scales with film area; we have ~10,300 films emitting meV–eV phonons) and therefore cannot be inherited from NUCLEUS or shielded against.

## Unified Notation

The three files agree on the physics and differ only in how they label the phonon scale. Binding choices for all downstream work:

| Symbol | Quantity | Units | Convention (binding) |
|---|---|---|---|
| `T` | Nuclear recoil energy (CEvNS/neutron kinematics) | eV | v1.0 convention retained; `E_R` used only when quoting the phonon literature |
| `E_dep` | Deposited (phonon) energy | eV | **In the multiphonon regime `E_dep ≠ T` event-by-event.** This distinction did not exist in v1.0 |
| `E_rec` | Reconstructed energy | eV | `E_rec ≈ 0.5·E_dep` at low E; unified phonon scale, **no ionization quenching** |
| `q` | Momentum transfer | keV/c | `q = √(2 M_Ge T)`; `q(100 meV) = 116 keV/c` = 58.9 Å⁻¹ |
| `⟨u_x²⟩` | **1-D** mean-square displacement | Å² | Quote `B = 8π²⟨u_x²⟩` alongside. Debye T→0: 1.34×10⁻³ Å²; experimental `B` band: 2.4–3.0×10⁻³ Å² |
| `2W` | Debye–Waller exponent | — | **`2W = q²⟨u_x²⟩` (1-D)**. The `/3` appears *only* with the 3-D sum. Classic factor-3 trap |
| `ω̄` | Effective phonon energy | meV | **`ω̄ ≡ ħ/(2 m_N ⟨u_x²⟩)` = 12–21 meV.** Only this definition makes `2W = E_R/ω̄` exact and `σ_E = √(E_R ω̄)` consistent |
| `σ_E` | IA quantum broadening | eV | `σ_E = √(E_R ω̄)`; `σ_E/E_R = 1/√(2W)` |
| dru | Rate unit | d⁻¹kg⁻¹keV⁻¹ | 1 dru = 1 count/(keV·kg·d). Never mix with mcpd in a formula |
| `φ(E)` | Fluence at detector position | cm⁻²s⁻¹eV⁻¹ | Digitized figures are `E·dΦ/dE` (per lethargy); **divide by E once, in one place** |
| `S/B_particle` | Signal-to-background | — | Never bare "S/B". LEE excluded by definition, not by caveat |

**Reconciled conflict (notation, not physics).** METHODS quotes `ω̄ ≈ 20–37 meV` (Debye `k_BΘ_D = 32 meV`, optical 37 meV) giving `E_R/ω̄ ≈ 2.7–5` at 100 meV; PRIOR-WORK quotes `ω̄ = 12–21 meV` giving `2W = 4.7–8.3`; COMPUTATIONAL computes `2W = q²⟨u²⟩_1D = 4.7` from `⟨u²⟩_1D = 1.3×10⁻³ Å²`. **All three are the same number.** PRIOR-WORK's Debye `⟨u_x²⟩ = 1.34×10⁻³ Å²` reproduces COMPUTATIONAL's 4.7 exactly; METHODS' 8.7 uses the experimental-`B` end of the same band. The only real disagreement is the *label* `ω̄`, and the `⟨u²⟩`-derived definition wins because it is the one that makes the two formulas we actually use self-consistent. **Pin `ω̄` from the real Ge VDOS (NCrystal `Ge_sg227.ncmat`, Nelin & Nilsson 1972; cross-checked against DarkELF `Ge_pDoS.dat`), not from the Debye model** — both `2W` and `σ_E` scale linearly with it, so a 2–3× ω̄ ambiguity propagates directly into the headline broadening.

**Retracted, not open:** the standing "never display QPD spectra below 10 eV" rule is **withdrawn by the user**; 100 meV is the floor. Three scouts flagged it as needing escalation — it does not. What survives from it is a *labelled regime boundary*, not a plotting ban: below ~1 eV deposit the reported observable is a **trigger-probability curve**, not `dR/dE_rec`.

## Key Findings

### Environment adoption and the anchors (from PITFALLS.md, PRIOR-WORK.md)

- **HIGH** — mcpd → dru conversion has three silent failure modes worth 9.06× (crystal vs 6.8 g array mass), 11% (0.09 not 0.1 keV RoI width), and 1.51× (6.8 vs 4.5 g). The recipe is validated by the Al₂O₃ column, which closes exactly (8.4 mcpd → **20.7** vs prose "about 20"); the CaWO₄ background total converts to **235.3** against the abstract's **~250** (abstract independently verified).
- **HIGH** — Neutron target scaling is a *ratio of ratios* that crude models get badly wrong. A flat-in-T single-scatter estimate gives CaWO₄/Al₂O₃ ≈ 1.1 in the RoI; NUCLEUS's Geant4 result is **1.81** (10–100 eV) and **1.20** (0.1–1 keV). Any model producing a band-independent ratio has lost the kinematic-compression physics. **Calibrate on those four numbers from one normalization before pointing anything at Ge.**
- **HIGH** — NUCLEUS's own systematics (30% neutron, 25% muon, 20% γ, 30% material, propagated min/max) produce their **S/B band [0.9–1.5] at 68% CL**. The VNS absolute neutron flux **has never been measured**, and neutrons are 91% of the RoI budget. Our band can never be tighter than theirs.
- **HIGH** — Veto credit does not transfer (see Executive Summary). Report S/B twice: L2 = 1 (honest lower bound) and with an argued L2.

### The sub-eV regime (from PRIOR-WORK.md, COMPUTATIONAL.md, METHODS.md)

- **HIGH** — **No crystal-wide coherent enhancement exists anywhere in the window.** `q·a ≈ 144` at 100 meV, `q/q_BZ ≈ 53`; coherence would need `E_R ≲ 30 μeV`. The CEvNS `N²` is intranuclear and unaffected. Explicitly rebut the "neutrino couples coherently to the whole crystal" misconception in the writeup.
- **HIGH** — Single-phonon CEvNS events deposit at most ~37 meV (Ge VDOS ends at **37.79 meV**, measured) and lie entirely below the 100 meV floor. This *justifies* the floor choice.
- **HIGH** — **Never multiply the CEvNS rate by `e^{−2W}`.** `e^{−2W} ≈ 10⁻²` at 100 meV suppresses the *zero-phonon* channel; the strength moves into the multiphonon/quasi-free continuum. Applying it would erase a real signal.
- **MEDIUM-HIGH** — **IA quantum broadening is the headline new physics.** `σ_E = √(E_R ω̄)`: 35–46% at 100 meV, 15.5–20.5% at 0.5 eV, 11–15% at 1 eV, 1.1–1.5% at 100 eV, negligible above. Framework is Sears-class deep-inelastic-neutron-scattering theory; the Ge numbers are DERIVED in-survey and must be re-derived in-phase.
- **HIGH** — Unified phonon scale is *strengthened* in-window: Ge displacement threshold **19.7 ⁺⁰·⁶₋₀·₅ eV** measured, defect energy loss **6.08 ± 0.18%**, and **no defect formation possible below ~6 eV**. Adopt `f_phonon = 1` below 6 eV, ramping to `1 − 0.061` above ~100 eV.
- **HIGH** — Flux truncation is bounded and not gating: `E_min(100 meV) = 58.16 keV`; truncation error **≤ 0.81%** at 100 meV and **exactly 0 above 0.29 eV**, under a conservative flat continuation of Φ at 100 keV with the `(1 − MT/2E²)` factor. Every allowed β branch gives `dN/dE_ν ∝ E_ν²`, so the true error is far smaller. **Report the bound; do not extend the table.** Also note v1.0 was already extrapolating — Huber–Mueller is fitted only over 2–8 MeV — so v2.0 crosses no new boundary here.
- **HIGH** — `dR/dT` for CEvNS **plateaus** as `T → 0` (flat-box `dσ/dT`). A spectrum that *rises* toward low T is an extrapolation artifact; one that falls to zero is a table floor. Make this an assertion, not an inspection.

### Ge-specific channels CaWO₄/Al₂O₃ are blind to (from METHODS.md, PRIOR-WORK.md, PITFALLS.md)

- **HIGH that it matters, LOW on magnitude** — **Thermal-neutron capture.** Behind 20 cm borated HDPE + 4 cm B₄C the surviving field is thermalized, and Ge has a large capture cross section (natural σ_th ≈ 2.2 b; ⁷³Ge ≈ 15 b). Two in-band signatures: prompt `(n,γ)` cascade recoils (single-γ limit 473 eV at 8 MeV, tens of eV for a multi-γ cascade) and the **⁷¹Ge EC M-shell line at 158.7 ± 1.4 eV** (measured by CONUS+). Capture recoils "strongly overlap the CEvNS signal for recoils ≲ 100 eV" (Biffl et al., PRD 107, 092011). **Blocking input: the in-shield thermal flux `φ_th`, which NUCLEUS does not publish and which the deposit-spectrum inversion cannot recover** (CaWO₄/Al₂O₃ are blind to it). If `φ_th` cannot be obtained, report this channel as an unquantified gap — not as zero.
- **MEDIUM** — Also missing from an elastic-only channel list: Ge inelastic (⁷⁴Ge 596 keV, ⁷²Ge 834 keV) and the B₄C ¹⁰B(n,α)⁷Li **478 keV γ line**, which NUCLEUS calls harmless *because their COV vetoes it* — an L2 statement. We would inherit the line and fail to reject it.
- **HIGH** — Sub-10 eV neutron recoils must show resonance structure: the natural-Ge **669.1 b peak at 102.6 eV** feeds recoils up to **5.5 eV**. A smooth sub-10 eV neutron NR spectrum is a bug.

### Validation gates and prior work (from PRIOR-WORK.md)

- **HIGH** — **The only measured Ge-at-a-reactor S/B is CONUS+'s ≈ 0.03** (0.4–1 keV_ee, 7.4 m.w.e., 40 counts/kg/d background vs 1.21 counts/kg/d signal; 395 ± 106 observed vs SM 347 ± 59 in 327 kg·d, 3.7σ — independently verified). Our predicted 0.65–1.2 is **more than an order of magnitude better than the published state of the art.** It may well be right (10³× lower threshold, more overburden, no quenching) but **CONUS+ must be reproduced as a limiting case at 160 eV_ee / 7.4 m.w.e. before the claim is made.**
- **MEDIUM** — LEE: no measurement exists below ~10 eV in Ge, or at 100 meV in any material. Best available time law is NUCLEUS's `R(t) = A(t−t₀)^{−k}`, `k = 0.59 ± 0.06`, `t₀` = 4 K crossing (adopt over CRESST's exponential — more recent, spans both targets, agrees with Romani's `1/t` and with Chang et al.'s independently measured `κ = 0.635 ± 0.009` in bulk Si). Ge amplitude anchors: EDELWEISS RED20 **10⁵ / 10⁴ dru at 200 eV / 1 keV** above ground, ÷3 underground.
- **MEDIUM** — The LEE is **design-dependent for a QPD specifically.** Romani (JAP 136, 124502 — verified) models it as Al-film dislocation relaxation scaling with film *area*, predicting **meV–eV phonons**; a wafer with ~10,300 films is exactly that geometry. Our surface-to-mass is ~1950 cm²/kg vs ~955 for a 6.8 g CaWO₄ crystal — ~2× worse before counting films. Chang et al.'s bulk-substrate bursts scale with *volume*, and 0.93 g → 110 g is a ×120 extrapolation that is **not defensible as a prediction**. Carry the LEE as a `(A, α)` scan with an explicit break-even amplitude, never as a single number, and never folded through `R(E_rec|E_dep)` (it is measured in reconstructed energy).

### Tooling and data (from COMPUTATIONAL.md)

- **HIGH** — **No Ge thermal scattering law exists in ENDF/B-VIII.0.** NCrystal 4.4.6 (native osx-arm64 wheel, `Ge_sg227.ncmat`) is the only laptop-scale route to bound-atom Ge cross sections below ~5 eV. Splice at 5 eV and report the discontinuity.
- **HIGH** — TENDL-2023 covers n-Ge to 200 MeV as a direct per-nuclide download; measured **+1.35% step at the 20 MeV seam** for ⁷⁴Ge. **Splice, do not substitute** — substituting would discard the 23,155-point resonance-resolved v1.1 grid. No NJOY/OpenMC build needed: Lib80x/ENDF80SaB2 *are* the NJOY output, fetched by HTTP range from the existing reader.
- **HIGH** — **No NUCLEUS, CONUS/CONUS+, or RICOCHET arXiv record carries ancillary data** (each checked individually). Any phase needing the VNS background spectrum is a **digitization** phase, not a download. The Goupy 2024 thesis (73.7 MB, public) is the best public source of VNS detail and should be read *before* digitizing. CRESST-III arXiv:1905.07335v3 ancillary files are real event-level data from 29.6 eV — the one genuine LEE dataset available.
- **MEDIUM** — CONFLUX v1.1.3 (pure Python, MIT) can generate the sub-100-keV flux band as a labelled model; its runtime on a fine sub-MeV grid is unmeasured and needs a timing spike. Given the ≤0.81% truncation bound, this is optional polish, not a dependency.

## Resolved Contradiction: the S(q,ω) phase question

**The disagreement.** PRIOR-WORK §1.5 recommends a *dedicated phase* computing DarkELF's Ge `S(q,ω)` contracted with the CEvNS matrix element, on the grounds that no published reactor-CEvNS phonon-regime calculation for Ge exists. COMPUTATIONAL §3 says explicitly: **do not** plan a phase whose backbone is a coherent-crystal `S(q,ω)` calculation, because the crystal-coherent regime (`2W ≲ 1`) lives below ~21 meV — under the floor — with `q` 53 Brillouin zones out.

**Classification: methodological, not physical.** Both independently obtained `2W ≈ 4.7` at 100 meV from the same `⟨u_x²⟩`. They do not disagree about the crystal; they are talking about two different objects. COMPUTATIONAL is rejecting a *coherent-crystal* backbone, and it is right: `e^{−2W} ≈ 10⁻²` at the floor and ~10⁻²⁰ at 1 eV, so the coherent/zero-phonon channel is extinct across the entire band. PRIOR-WORK is objecting to a *delta-function free recoil*, and it is also right: `2W ≈ 5` is **not** `≫ 1`, so the IA carries `O(1/2W)` ≈ 15–20% corrections and the recoil peak has real width.

**Verdict (adopt the reconciliation).** Model the **impulse-approximation quantum broadening** — free-recoil `dR/dE_R` convolved with a Gaussian of `σ_E = √(E_R ω̄)`, applied *before* the QPD response chain — and use **NCrystal/DarkELF only as a bounded one-off justification** that the impulse limit applies: compute `⟨u²⟩` and `2W(q)` from the real Ge VDOS, demonstrate `S → δ(ω − q²/2M)` is reached by ~100 meV via the f-sum rule, and quantify the residual correction in the bottom bin. One or two plans, not a milestone pillar.

**Basis, in order of weight.** (1) *Trust the controlled expansion*: `1/2W` is an identified small parameter (≈0.12–0.21 at the floor), whereas the multiphonon expansion at `2W ≫ 1` needs many orders and is the wrong representation — COMPUTATIONAL says so and the DarkELF authors' own accuracy statements agree (two-phonon incoherent "within a factor ~5", up to an order of magnitude low with anharmonicity). (2) *Trust the method valid in the project's regime*: the project's operating point after the new user decision is the **0.5 eV threshold**, where `2W ≈ 24–42` and the Gaussian IA is solidly valid; 100 meV is the extreme edge, not the working point. (3) *A DarkELF×CEvNS contraction is original implementation work, not tool integration* — its public API is parameterized in DM kinematics and no CEvNS-to-phonon code exists. PRIOR-WORK's own fallback is exactly the Gaussian, and it explicitly forbids only the one option nobody is proposing: extending the v1.0 free-nucleus spectrum to 100 meV **with no broadening at all**.

**Rejected alternative.** A full multiphonon `S(q,ω)` × CEvNS phase is rejected as a *backbone* because it would recentre rather than remove the band (the underlying method is itself only O(1)/factor-few accurate), at a large cost, in a regime the milestone barely enters. Revisit only if a referee demands a number rather than a band at 100 meV.

### Other contradictions resolved

| Contradiction | Resolution |
|---|---|
| METHODS: NUCLEUS's CPU-cost statement "does not appear in the text… treat as project lore" vs orchestrator: it is on p. 21 | **METHODS is wrong; flag retracted.** The orchestrator read the rendered PDF; METHODS used partial text extraction — the exact failure mode METHODS itself warns about (Pitfall 6). Consequence unchanged: full Geant4 stays out of scope, a 1-D shield-only MC does not. |
| METHODS: use 1-D spherical **OpenMC** as the shield-transport fallback vs COMPUTATIONAL: openmc is **unbuildable on osx-arm64**, explicitly rejected | **COMPUTATIONAL wins** — it rests on an actual build attempt on this machine in a prior phase. If a spectral shield propagation is needed, it must be a hand-rolled multigroup/S_N solver on Lib80x-derived group constants (METHODS' own option (ii)), not OpenMC. The roadmapper must not inherit an OpenMC dependency. |
| COMPUTATIONAL: "don't plan a phase around the crystal codes" vs METHODS: NCrystal is *required* for the sub-5 eV neutron kernel | **Not a conflict — two distinct uses.** (i) NCrystal as the bound-atom **neutron** kernel below 5 eV is load-bearing and real (`E_min(100 meV) = 1.87 eV` neutron energy sits below the free-atom validity floor, and no Ge TSL exists). (ii) NCrystal/DarkELF as **CEvNS** crystal-response modelling is the bounded justification only. COMPUTATIONAL's warning applies to (ii) alone. Do not drop NCrystal from the stack. |
| PRIOR-WORK `E_min(100 meV) = 58.16 keV` vs project-frozen 58.7 keV | ~1% isotope-abundance weighting of `M_Ge`. **Adopt 58.16 keV** (natural-Ge mean mass, orchestrator-established); 58.7 keV is the ⁷⁴Ge-only value. Close it in the conventions lock. |

## Approximation Landscape

| Method | Valid regime | Breaks down when | Controlled? | Complements |
|---|---|---|---|---|
| Flux/response factorization `dR/dT = ΣᵢNᵢ∫φ dσᵢ/dT` | Optically thin target (`t/λ ≈ 3–4%`, multi-scatter ~0.1%) | Wafer perturbs the field, or geometry forces a shield change | Yes — `t/λ` | Nothing; this is the milestone's premise |
| Analytic flat-box inversion `φσ = −(f²E/N)G′(fE)` | `E_n ≲ 0.5–1 MeV` (s-wave) | Forward-peaking above ~1 MeV; recovered `φ` goes negative | Yes — Legendre `a₁` | Removal-XS fast-flux bound; 1-D multigroup |
| Removal cross-section `Φ = Φ₀e^{−Σ_R x}` | Fast-group **integral** only | Always, for spectra — produces no epithermal population | No | Must be paired with a spectral method |
| Point-kernel + buildup (γ) | A few mfp of Pb/PE | Bare `e^{−μx}` under-predicts by factors of several | Yes — 10–30% documented | NUCLEUS's own "factor ~50" statement |
| Free-nucleus recoil (impulse) | `E_R ≫ ω̄`; solid above ~1 eV | `2W ≲ few` — O(1/2W) ≈ 15–20% at 100 meV | Yes — `1/2W` | IA Gaussian broadening below ~1 eV |
| **IA Gaussian `σ_E = √(E_R ω̄)`** | `2W ≫ 1`; marginal at 100 meV | True `S(q,ω)` asymmetric at low `2W` | Partially — `O(1/2W)` ≈ 20% at the floor | DarkELF multiphonon (as a one-off check) |
| ENDF free-atom `σ_el` | `E_n ≳ 5 eV` | Chemical binding/lattice below; spurious free-gas 1/v rise to 20.6 b | No | NCrystal `Ge_sg227` spliced at 5 eV |
| Lumped `ε ≈ 0.5`, `E_rec ≈ 0.5·E_dep` | Fully developed cascade, ≳ 1 eV | ~3 optical-phonon quanta reach one sensor, not 10,300 | No — no literature anchor | Trigger-probability curve + 0.5 eV sigmoid |
| Poisson/multinomial counting resolution | All E; best case only | Any real noise source is added | No — it is a *floor*, not an estimate | IA broadening (comparable at threshold) |

**Coverage gaps — no reliable method exists.** (a) The in-shield **thermal** neutron flux `φ_th`: not published, not recoverable by inversion, and not obtainable without transport we have rejected. (b) The **LEE below ~10 eV**: unmeasured everywhere, two leading models with contradictory scalings (volume vs Al-film area). (c) The **response chain below ~1 eV**: no literature at all; this is our own detector-physics assumption, which is why the observable changes to trigger probability there.

## Theoretical Connections

1. **Kinematic compression is the same physics on both sides of S/B** *(established)*. `T_max/E_n = 4A/(A+1)²` sets both why Ge's CEvNS rate is 2.31× below CaWO₄ *and* why its neutron background is only 1.2–1.8× below. The S/B is a ratio of ratios in which most normalization cancels — which is exactly why the CaWO₄/Al₂O₃ two-band calibration (1.81 and 1.20) is a sharp test of the transfer machinery.
2. **The Debye–Waller exponent is the bridge between the two scouts' regimes** *(established)*. `2W = q²⟨u_x²⟩ = E_R/ω̄` simultaneously kills the coherent channel (`e^{−2W}`) and sets the IA broadening (`1/√(2W)`). One number, two consequences pointing in opposite directions — which is precisely why one scout said "no crystal modelling" and the other said "crystal modelling required."
3. **The trigger threshold is where the two smearing mechanisms meet** *(new, conjectured)*. At 0.5 eV the counting-statistics floor (15.9%/14.2%) and the IA broadening (15.5–20.5%) are the same size; neither dominates. Their quadrature sum (~22–26%) acts on a sigmoid trigger curve, so the *effective* threshold and the counted rate both depend on physics that is currently only half-modelled.
4. **A meV-threshold QPD is the instrument the sub-IBD flux literature asks for** *(established as a framing opportunity)*. Liao–Liu–Marfatia (PRD 108, 033002) show an ultra-low-threshold CEvNS detector can bound the unmeasured sub-1.8 MeV reactor flux by unfolding. Our `E_min(100 meV) = 58.16 keV` reach is a positive physics case, not just a systematic.
5. **The LEE mechanism and the QPD signal mechanism are the same phenomenon** *(conjectured, adverse)*. Chang et al. identify bulk-substrate phonon bursts at `ε = 0.68 ± 0.38 meV` as "a significant source of quasiparticle poisoning in superconducting qubits." A QPD's *signal* is quasiparticle poisoning. This is not merely a background — it is a direct competitor to the readout mechanism, and it is not shieldable.

### Cross-Validation Matrix

| | Independent fold | NUCLEUS published | Analytic limit | Experiment |
|---|:--:|:--:|:--:|:--:|
| **CEvNS at VNS** | CaWO₄ fold closes at 14% | Table 5 = 356.5 dru (100% duty) | `T→0` plateau; Helm `F→1` below 1 keV | CONUS+ 0.03 at 160 eV_ee (limiting case); NUCLEUS 2019 Fig. 1 Ge to 5% |
| **Neutron NR (Ge)** | Two-target inversion over-determined | CaWO₄/Al₂O₃ = 1.81 & 1.20 | δ-flux → exact flat box, height σ/(fE₀) | — (VNS flux **unmeasured**) |
| **Gamma / Compton** | v1.0 Klein–Nishina reused | "factor ~50" passive reduction | Klein–Nishina edges | VNS ambience 5.03 cm⁻²s⁻¹ measured |
| **Muons** | v1.0 chain, scalar attenuation 1.41 | Table 5 `< 14` mcpd | Landau MPV | PDG sea-level (v1.0, passed) |
| **Ge (n,γ) capture** | — | — | `Σ E_γ²/2Mc²` bound | ⁷¹Ge M-shell 158.7 eV (CONUS+) |
| **IA broadening** | — | — | `S → δ` f-sum rule at large q | — |
| **LEE** | — | excluded by NUCLEUS | break-even amplitude | CRESST-III event list from 29.6 eV (CaWO₄, not Ge) |

**High-risk rows (no independent cross-check):** IA broadening, Ge (n,γ) capture magnitude, and the LEE. Each needs an internal consistency check substituted for external validation — the f-sum rule, the isotropic-cascade bound, and the break-even amplitude respectively.

### Critical Claim Verification

| # | Claim | Source | Verification | Result |
|---|---|---|---|---|
| 1 | Ge displacement threshold 19.7 ⁺⁰·⁶₋₀·₅ eV; 6.08 ± 0.18% loss; no defect below ~6 eV | PRIOR-WORK | WebSearch → APL 113, 092101 / arXiv:1805.09942 | **CONFIRMED** verbatim |
| 2 | LEE as Al-film dislocation relaxation, area scaling, meV–eV phonons | PRIOR-WORK, PITFALLS | WebSearch → JAP 136, 124502, DOI 10.1063/5.0222654 / arXiv:2406.15425 | **CONFIRMED** (paper exists, thesis matches); area-scaling detail from the paper text, not re-read here |
| 3 | NUCLEUS ~250 dru in 10–100 eV, S/B ≳ 1, CaWO₄, rejection >2 orders | PITFALLS | WebFetch arXiv:2509.03559 abstract | **CONFIRMED** verbatim |
| 4 | CONUS+ 395 ± 106 vs SM 347 ± 59, 3.7σ, Leibstadt, HPGe | PRIOR-WORK | WebSearch → Nature 643, 1229 (2025) | **CONFIRMED**; the S/B ≈ 0.03 is DERIVED from two quoted rates, not quoted |
| 5 | IA criterion `q ≫ √(2m_dω̄_d)`; free recoil fails when `E_R` ~ a few × phonon energy | PRIOR-WORK, METHODS | WebSearch → PRD 106, 036019 / arXiv:2205.02250 | **CONFIRMED** (criterion + regime statement) |
| 6 | `σ_E = √(E_R ω̄)`, `σ_E/E_R = 1/√(2W)` for Ge | PRIOR-WORK | WebSearch (Sears PRB 35, 2038 exists; recoil-peak-width framework confirmed) | **PARTIAL** — framework confirmed, Ge numbers DERIVED in-survey; **re-derive in-phase before use** |
| 7 | No Ge thermal scattering law in ENDF/B-VIII.0 | COMPUTATIONAL, METHODS | WebFetch NNDC B-VIII.0 summary | **PARTIAL** — the 34-material TSL count is confirmed; the material names are not listed on that page. Ge absence rests on COMPUTATIONAL's direct read of the LANL ENDF80SaB2 list. Treat as MEDIUM-HIGH; a one-line IAEA/NNDC list check closes it |
| 8 | Table 5 CEvNS row has one value per column; prose 280 is the 80%-duty value | Orchestrator (rendered PDF) | Orchestrator-established; not re-litigated | **SETTLED** — anchor on Table 5 at 100% duty |

## Implications for Research Plan

### Phase 1: Environment lock and anchor closure (P-ENV)

**Rationale:** Every number downstream is a transcription of NUCLEUS's tables; three independent 9×/11%/1.5× errors are available before any physics happens.
**Delivers:** one `mcpd_to_dru()` with named, cited constants; duty cycle declared once at pipeline top; digitized Fig. 4 / Figs. 8–11 with panel/trace/cut provenance and a ζ error budget; Table 4 systematics wired in.
**Validates:** CaWO₄ total = 235.3 vs abstract ~250; Al₂O₃ CEvNS = 20.7 vs prose "about 20"; digitized integrals close against printed totals.
**Avoids:** Pitfalls 1, 2, 6. **Needs research:** no.

### Phase 2: Geometry fit and the L1/L2 split (P-VETO) — **gating**

**Rationale:** If the wafer does not fit the COV/IV envelope, the veto factors are void *and* `φ` at the detector position is no longer NUCLEUS's `φ` — the milestone premise itself fails. This must be answered before the background chain is built on top of it.
**Delivers:** wafer-in-envelope determination; the L1/L2 taxonomy; L2 = 1.0 baseline; the wafer's own muon-veto acceptance from its chord distribution.
**Validates:** no factor 5, no >99.8%, no multiplicity cut appears in code without wafer geometry behind it.
**Avoids:** Pitfall 3. **Needs research:** yes — the envelope dimensions must be read from arXiv:2509.03559 and the Goupy thesis.

### Phase 3: Grid extension, threshold, and the sub-eV observable (P-GRID)

**Rationale:** Everything binds to the grid; and the observable *changes* below ~1 eV, which is a definitional decision that must precede any spectrum.
**Delivers:** `shared_energy_grid()` to 0.1 eV (~744 bins); regenerated `R(E_rec|E_dep)` both designs; the **sigmoid analysis efficiency with its 50% point at 0.5 eV, multiplied on top of all other efficiencies including `ε ≈ 0.5`** (it does not replace it); trigger-probability observable below ~1 eV; the emergent counting-resolution floor documented as best-case (15.9%/14.2% at 0.5 eV, 35.6%/31.6% at 0.1 eV, 3.6%/3.2% at 10 eV, 1.2%/1.1% at 100 eV).
**Validates:** all 24 v1.0/v1.1 anchors still reproduce; every interpolator **raises** outside its evaluated range (no clamping, no extrapolation); count conservation on the regenerated matrix.
**Avoids:** Pitfall 5(c,d). **Needs research:** no.

### Phase 4: Phonon-scale conventions and IA broadening (P-CONV)

**Rationale:** `ω̄` gates both `2W` and `σ_E` linearly, and the 12–21 vs 37 meV ambiguity is 2–3×. Nothing sub-eV is defensible until it is pinned.
**Delivers:** `ω̄` and `⟨u_x²⟩` from the real Ge VDOS (NCrystal, cross-checked against DarkELF); `2W = q²⟨u_x²⟩` (1-D) locked in CONVENTIONS; the IA Gaussian convolution applied *before* the response chain; the bounded justification artifact that the impulse limit is reached by ~100 meV.
**Validates:** VDOS max = 37.79 meV; `⟨u²⟩` VDOS-integral vs Debye within ~1.5×; `S → δ(ω − q²/2M)` f-sum rule at large q; **v1.0 spectrum reproduced to <1% above ~10 eV** (the limit where broadening must vanish).
**Avoids:** the `e^{−2W}` multiplication error; the 3-D/1-D factor-3 trap. **Needs research:** yes — this is the milestone's genuinely new physics.

### Phase 5: CEvNS at the VNS normalization to 100 meV (P-SIG)

**Rationale:** Signal first — it is the only channel whose closure test has already passed, and it sets the denominator for everything else.
**Delivers:** `dR/dE_rec` at 2.1×10¹² ν̄/cm²/s with the duty cycle declared once; the ≤0.81% truncation bound reported (table **not** extended); Ge/CaWO₄ = 2.31 documented with the naive 1.95 explicitly rejected.
**Validates:** `T→0` plateau flat to a few % from 100 meV to 10 eV and equal to the analytic value from the frozen `∫Φ`; `T = 0.290 eV` reproduces the frozen v1.0 result exactly; **CONUS+ ≈ 0.03 reproduced at 160 eV_ee / 7.4 m.w.e.**
**Avoids:** Pitfall 5(c); the flux-extrapolation fabrication. **Needs research:** no.

### Phase 6: Neutron re-fold for Ge (P-TGT)

**Rationale:** Neutrons are 91% of the residual budget; the target dependence is the entire content of "re-fold for Ge."
**Delivers:** `φ_post(E_n)` by regularized inversion of NUCLEUS's deposit spectra (Tikhonov/TV, never finite differences), cross-checked by removal-XS attenuation of Fig. 4 for the fast integral; Ge flat-box fold with the resonance grid preserved; NCrystal splice at 5 eV (or documented truncation per the Phase-7 gap-D1 precedent); TENDL splice at 20 MeV with the +1.35% step reported.
**Validates:** recovered `φ` non-negative everywhere; **target-swap closure reproducing CaWO₄/Al₂O₃ = 1.81 and 1.20 from one normalization**; δ-flux returns an exact flat box; the 102.6 eV resonance imprints structure below 5.5 eV recoil.
**Avoids:** Pitfall 4; the log-substituted quadrature must be anchored at `E_min(T)` or the `1/E²` endpoint spike is silently missed. **Needs research:** yes — the inversion's applicability depends on whether Figs. 8–11 are pre- or post-veto.

### Phase 7: Ge-only channels (P-GEONLY)

**Rationale:** These are the backgrounds NUCLEUS's budget structurally cannot contain, and they land inside the RoI.
**Delivers:** prompt `(n,γ)` cascade recoils (EGAF lines, isotropic-cascade bound); ⁷¹Ge EC line inventory; Ge inelastic; the B₄C 478 keV Compton continuum in an unvetoed wafer.
**Validates:** ⁷¹Ge M/L/K reproduced at 158.7 / 1298.5 / 10368.3 eV.
**Blocked by:** `φ_th` inside the shield. If unobtainable, **report as an unquantified gap, not as zero.** **Needs research:** yes.

### Phase 8: Gamma and muon re-fold (P-EM) — parallel with 6–7

**Rationale:** The one channel that transfers cleanly (muons: scalar attenuation 1.41) and the one with a standard closed-form method (gammas: point-kernel + buildup).
**Validates:** against NUCLEUS's "factor ~50" passive gamma reduction. **Needs research:** no.

### Phase 9: LEE as a parameterized overlay (P-LEE)

**Rationale:** The LEE is the dominant sub-100 eV term, is unmeasured for this device class, and is *design-dependent* through Al film area — so it is also a design lever the milestone can advocate.
**Delivers:** `dR/dE_LEE = A(E/E₀)^{−α}` scan on the `E_rec` axis (never folded through the response); the **break-even amplitude** at which S/B_particle = 1; the Romani `A_Al` argument for ~10,300 films.
**Needs research:** no (the literature is exhausted; this is a scan). **Risk:** HIGH — unbounded.

### Phase 10: S/B assembly, systematics, framing (P-SB)

**Delivers:** `S/B_particle` reported twice (L2 = 1 and argued L2), min/max systematics propagated as NUCLEUS does, LEE as a separately flagged overlay band, "particle backgrounds only; LEE not modelled" on every deliverable figure.
**Validates:** our machinery applied to CaWO₄ returns **[0.9–1.5]**; the Ge band is never tighter than the CaWO₄ band it is anchored to.

### Phase Ordering Rationale

- **P-VETO is gating** because it can invalidate the fluence transfer itself, not merely the veto credit. It is cheap and must not sit behind the physics phases.
- **P-GRID precedes all spectra** because the observable definition changes below ~1 eV and every table binds to the grid.
- **P-CONV precedes P-SIG** because `ω̄` propagates linearly into the broadening that P-SIG must apply.
- **Signal (P-SIG) precedes background (P-TGT)** because its closure test has already passed at 14%, giving a validated denominator; the neutron chain has no such anchor.
- Phases 6, 8, 9 are mutually parallel once 1–3 are done. Phase 7 is strictly downstream of 6 (it needs `φ_th`, or the finding that `φ_th` is unavailable).

### Phases Requiring Deep Investigation

- **Phase 4 (P-CONV)** — genuinely new physics for this project; no published reactor-CEvNS phonon-regime calculation for Ge exists.
- **Phase 6 (P-TGT)** — the inversion's validity hinges on an unresolved question about NUCLEUS's figure captions.
- **Phase 7 (P-GEONLY)** — blocked on an input NUCLEUS does not publish.
- **Phase 2 (P-VETO)** — the answer may end the milestone as currently scoped.

**Established methodology, straightforward execution:** Phase 1 (transcription + closure tests), Phase 3 (grid extension is 27% more bins), Phase 5 (v1.0 machinery at a new normalization), Phase 8 (v1.0 machinery with a scalar attenuation).

## Confidence Assessment

| Area | Confidence | Notes |
|---|---|---|
| Computational Approaches | **HIGH** | Every URL, version, and file size probed live; two unmeasured runtimes flagged as timing spikes; osx-arm64 constraints honoured throughout |
| Prior Work | **MEDIUM-HIGH** | HIGH on fronts 1 and 4 (verified independently); MEDIUM on the LEE; several retrieval failures honestly declared and correctly excluded from citation |
| Methods | **MEDIUM-HIGH** | Downgraded from the file's own claim by one wrong flag (CPU cost) and one unusable recommendation (OpenMC), both now corrected |
| Pitfalls | **HIGH** | Grounded in verbatim NUCLEUS numbers and this repo's own frozen artifacts; bias direction annotated per pitfall, which is exactly right for a milestone whose headline is an uncomfortable S/B |

**Overall confidence: MEDIUM-HIGH** for the environment transfer and the CEvNS channel; **MEDIUM** for the neutron re-fold; **LOW** for anything below ~1 eV that is not explicitly banded.

### Input Quality → Roadmap Impact

| Input | Quality | Affected recommendations | Impact if wrong |
|---|---|---|---|
| METHODS.md | good (2 corrections applied) | Inversion strategy, digitization protocol, LEE parameterization | An OpenMC dependency would be unbuildable; the retracted CPU flag would have wrongly narrowed scope |
| PRIOR-WORK.md | good | IA broadening, LEE anchors, CONUS+ gate, phonon-scale strengthening | Broadening magnitude is DERIVED; if `ω̄` is wrong by 2–3× the threshold smearing changes by √3 |
| COMPUTATIONAL.md | good | Tool stack, data availability, splice seams, impulse-regime verdict | Ge-TSL absence is the weakest link; if a Ge TSL exists, NCrystal becomes optional rather than required |
| PITFALLS.md | good | Anchor arithmetic, veto transferability, systematics, observable naming | Its bias annotation is what keeps an S/B ≈ 1 result honest; without it every error flatters the headline |

### Gaps to Address

- **`φ_th` inside the shield** — not published, not invertible. Blocks Phase 7's magnitude. Handle: report as an unquantified gap with the Biffl `Φ_th < 7×10⁻⁴ n/cm²·s` requirement as context.
- **VNS absolute neutron flux is unmeasured** — inherited, unavoidable, and it dominates 91% of the RoI. Carry the 30% band; never quote tighter than the source.
- **Geant4 sub-keV reliability** — flagged by NUCLEUS's own authors as "a major question mark," and v2.0 goes two decades below where they flagged it.
- **Response chain below ~1 eV** — no literature. Mitigated, not solved, by switching the observable to trigger probability.
- **Two comparable smearing mechanisms at threshold, only one modelled** — the counting floor is best-case (no baseline/amplifier/position/readout noise) and the IA broadening is unimplemented. Neither alone is the resolution.
- **ON/OFF is not clean at a two-core site** — genuine both-off periods are rare; any sensitivity claim must state the four-state duty-cycle model.

## Sources

### Primary (HIGH — verified this synthesis or read verbatim by a scout)

- H. Abele *et al.* (NUCLEUS), *Eur. Phys. J. C* **86**, 29 (2026), arXiv:2509.03559 — the adopted environment; abstract verified verbatim (~250 dru, S/B ≳ 1, CaWO₄)
- G. Angloher *et al.* (NUCLEUS), *Eur. Phys. J. C* **79**, 1018 (2019), arXiv:1905.10258 — VNS geometry; Fig. 1 Ge curve reproduced to 5%
- CONUS+ Collab., *Nature* **643**, 1229 (2025), arXiv:2501.05206 — verified: 395 ± 106 vs SM 347 ± 59, 3.7σ, Leibstadt
- R. Agnese *et al.* (SuperCDMS), *Appl. Phys. Lett.* **113**, 092101 (2018), arXiv:1805.09942 — verified: `E_d` = 19.7 ⁺⁰·⁶₋₀·₅ eV, 6.08 ± 0.18%, no defect below ~6 eV
- B. Campbell-Deem, S. Knapen, T. Lin, E. Villarama, *Phys. Rev. D* **106**, 036019 (2022), arXiv:2205.02250 — verified: IA criterion and free-recoil breakdown statement
- R. K. Romani, *J. Appl. Phys.* **136**, 124502 (2024), arXiv:2406.15425 — verified: Al-relaxation LEE model
- A. J. Biffl *et al.*, *Phys. Rev. D* **107**, 092011 (2023), arXiv:2212.14148 — Ge (n,γ) recoils overlap CEvNS below ~100 eV
- ENDF/B-VIII.0 (Brown *et al.*, NDS **148**, 1 (2018)) + LANL Lib80x / ENDF80SaB2; TENDL-2023 n-Ge to 200 MeV (downloaded and parsed)
- K. Ramanathan *et al.*, APS Open Science **1**, 000013 (2026), arXiv:2405.17192 — QPD device model (carried forward)

### Secondary (MEDIUM)

- V. F. Sears, *Phys. Rev. B* **35**, 2038 (1987) — IA/final-state framework behind `σ_E = √(E_R ω̄)`; **the Ge numbers are DERIVED, not quoted**
- NUCLEUS Collab., arXiv:2603.07687 — LEE time law `k = 0.59 ± 0.06`, `t₀` = 4 K crossing, `p_LEE` = 0.025 ± 0.004
- P. Adari *et al.*, *SciPost Phys. Proc.* **9**, 001 (2022), arXiv:2202.05097 — cross-experiment LEE compilation (EDELWEISS Ge anchors)
- R. Anthony-Petersen *et al.*, *Nat. Commun.* **15**, 6444 (2024) — >100× glued vs suspended
- C. L. Chang *et al.*, *Appl. Phys. Lett.* **127**, 263502 (2025) — sub-meV bursts, volume scaling
- NCrystal (Cai & Kittelmann, *CPC* **246**, 106851 (2020)); DarkELF (Knapen *et al.*, *PRD* **105**, 015014 (2022)); CONFLUX (Zhang *et al.*, arXiv:2503.18966)
- G. Nelin & G. Nilsson, *Phys. Rev. B* **5**, 3151 (1972) — the Ge VDOS behind `Ge_sg227.ncmat` (itself a digitized figure)
- C. Goupy, PhD thesis, Univ. Paris Cité (2024), NNT 2024UNIP7170 — best public VNS background detail

### Tertiary (LOW — do not cite without retrieval)

- *J. Nucl. Sci. Technol.*, DOI 10.1080/00223131.2017.1291370 — sub-100 keV reactor ν̄; **HTTP 403 twice, unverified, lead only**
- Kopeikin *et al.*, *Phys. At. Nucl.* **67**, 1892 (2004) — paywalled, magnitudes unverified
- *PRD* **105**, 123002 (2022) `α = 3.43` semiconductor excess index — different device class; confirm before adopting
- Sun & Xiao, arXiv:2606.31345 — vector-figure extraction; title/date only

---

_Research analysis completed: 2026-07-22_
_Ready for research plan: yes_

```yaml
# --- ROADMAP INPUT (machine-readable, consumed by gpd-roadmapper) ---
synthesis_meta:
  project_title: "QPD Particle-Physics Potential — v2.0 QPD at the NUCLEUS Chooz Very-Near-Site"
  synthesis_date: "2026-07-22"
  input_files: [METHODS.md, PRIOR-WORK.md, COMPUTATIONAL.md, PITFALLS.md]
  input_quality: {METHODS: good, PRIOR-WORK: good, COMPUTATIONAL: good, PITFALLS: good}

conventions:
  unit_system: "detector/particle-physics practical: eV/keV/MeV, counts/kg/day/keV (dru), s, cm/um; (hbar c)^2 = 3.894e-28 GeV^2 cm^2"
  metric_signature: "not_applicable"
  fourier_convention: "not_applicable"
  coupling_convention: "dsigma/dT = (G_F^2 M/4pi) Q_W^2 (1 - M T / 2 E_nu^2) F^2(q^2); Q_W = N - (1-4 sin2thetaW) Z; sin2thetaW = 0.2387"
  renormalization_scheme: "tree-level SM; sin2thetaW low-energy MSbar"
  energy_scale: "single unified phonon scale, NO ionization quenching; f_phonon = 1 below 6 eV, ramping to 1-0.061 above ~100 eV"
  debye_waller: "2W = q^2 <u_x^2> with <u_x^2> the 1-D MSD (NOT q^2<u^2>/3); omega_bar = hbar/(2 m_N <u_x^2>) = 12-21 meV, to be pinned from the Ge VDOS"
  duty_cycle: "declare once at pipeline top; anchor NUCLEUS Table 5 at 100% duty; prose 280 is the 80% value"
  display_floor: "RETRACTED — 100 meV floor; below ~1 eV deposit the observable is a trigger-probability curve, not dR/dE_rec"
  threshold: "sigmoid analysis efficiency, 50% point at 0.5 eV, MULTIPLIED on top of all other efficiencies including eps ~= 0.5 (does not replace it)"

methods_ranked:
  - name: "Flux/response factorization + analytic flat-box inversion of NUCLEUS deposit spectra"
    regime: "E_n <~ 0.5-1 MeV (s-wave); optically thin wafer, t/lambda ~ 3-4%"
    confidence: HIGH
    cost: "seconds; one regularized derivative plus a downward march"
    complements: "removal-XS fast-flux bound; hand-rolled 1-D multigroup if the inversion fails"
  - name: "Free-nucleus recoil kernel convolved with IA Gaussian sigma_E = sqrt(E_R omega_bar)"
    regime: "solid above ~1 eV; O(1/2W) ~ 15-20% correction at 100 meV; 2W ~ 24-42 at the 0.5 eV threshold"
    confidence: MEDIUM-HIGH
    cost: "O(N_bins) convolution"
    complements: "NCrystal/DarkELF VDOS as a bounded one-off impulse-limit justification"
  - name: "NCrystal Ge_sg227 bound-atom neutron kernel below 5 eV, spliced to ENDF free-atom"
    regime: "E_n < 5 eV where free-atom sigma_el is not the right object; no Ge TSL exists in ENDF/B-VIII.0"
    confidence: MEDIUM-HIGH
    cost: "seconds; native osx-arm64 wheel"
    complements: "documented truncation (Phase-7 gap-D1 precedent) if the splice is rejected"
  - name: "Point-kernel gamma attenuation with ANS-6.4.3 buildup factors"
    regime: "a few mfp of Pb/PE; 10-30% accurate"
    confidence: HIGH
    cost: "microseconds"
    complements: "NUCLEUS's stated factor ~50 passive reduction"
  - name: "Two-parameter (A, alpha) LEE power-law overlay on the E_rec axis + break-even amplitude"
    regime: "all E; scenario input, never a prediction"
    confidence: LOW
    cost: "trivial"
    complements: "Romani A_Al design-lever argument; NUCLEUS time law k = 0.59 +- 0.06"
  - name: "TENDL-2023 splice above 20 MeV (splice, do not substitute)"
    regime: "20-200 MeV n-Ge"
    confidence: HIGH
    cost: "seconds; 5 x 3.4 MB direct download"
    complements: "frozen ENDF/B-VIII.0 resonance-resolved grid below 20 MeV"

phase_suggestions:
  - name: "P-ENV environment lock"
    goal: "Transcribe the NUCLEUS environment with one validated unit conversion, one duty-cycle declaration, and closure-tested digitization."
    methods: ["Flux/response factorization + analytic flat-box inversion of NUCLEUS deposit spectra"]
    depends_on: []
    needs_research: false
    risk: MEDIUM
    pitfalls: ["mcpd-to-dru-9x-11pct-1.5x", "cawo4-cevns-duty-cycle-anchor", "digitized-figure-provenance"]
  - name: "P-VETO geometry fit and L1/L2 split"
    goal: "Determine whether a 110 g 4-inch wafer fits the NUCLEUS COV/IV envelope and fix which rejection transfers."
    methods: ["Flux/response factorization + analytic flat-box inversion of NUCLEUS deposit spectra"]
    depends_on: []
    needs_research: true
    risk: HIGH
    pitfalls: ["payload-coupled-veto-credit"]
  - name: "P-GRID grid extension and sub-eV observable"
    goal: "Extend the shared grid to 0.1 eV, regenerate the response matrices, and install the 0.5 eV sigmoid trigger observable."
    methods: ["Free-nucleus recoil kernel convolved with IA Gaussian sigma_E = sqrt(E_R omega_bar)"]
    depends_on: ["P-ENV environment lock"]
    needs_research: false
    risk: LOW
    pitfalls: ["table-floor-clamp-vs-raise", "display-floor-regime-boundary"]
  - name: "P-CONV phonon conventions and IA broadening"
    goal: "Pin omega_bar and the Debye-Waller convention from the real Ge VDOS and apply the impulse-approximation quantum broadening."
    methods: ["Free-nucleus recoil kernel convolved with IA Gaussian sigma_E = sqrt(E_R omega_bar)", "NCrystal Ge_sg227 bound-atom neutron kernel below 5 eV, spliced to ENDF free-atom"]
    depends_on: ["P-GRID grid extension and sub-eV observable"]
    needs_research: true
    risk: MEDIUM
    pitfalls: ["debye-waller-1d-vs-3d-factor-3", "multiply-rate-by-exp-minus-2W"]
  - name: "P-SIG CEvNS at the VNS normalization to 100 meV"
    goal: "Produce dR/dE_rec at 2.1e12 nubar/cm2/s down to 100 meV with the flux-truncation bound reported."
    methods: ["Free-nucleus recoil kernel convolved with IA Gaussian sigma_E = sqrt(E_R omega_bar)"]
    depends_on: ["P-CONV phonon conventions and IA broadening", "P-ENV environment lock"]
    needs_research: false
    risk: LOW
    pitfalls: ["flux-extrapolation-below-table-floor", "T-to-zero-plateau"]
  - name: "P-TGT neutron re-fold for Ge"
    goal: "Recover phi_post(E_n) from NUCLEUS deposit spectra and re-fold it through the Ge kernel with the resonance grid intact."
    methods: ["Flux/response factorization + analytic flat-box inversion of NUCLEUS deposit spectra", "NCrystal Ge_sg227 bound-atom neutron kernel below 5 eV, spliced to ENDF free-atom", "TENDL-2023 splice above 20 MeV (splice, do not substitute)"]
    depends_on: ["P-ENV environment lock", "P-VETO geometry fit and L1/L2 split", "P-GRID grid extension and sub-eV observable"]
    needs_research: true
    risk: HIGH
    pitfalls: ["neutron-target-scaling-ratio-of-ratios", "free-gas-sub-eV-fiction", "endpoint-spike-quadrature"]
  - name: "P-GEONLY Ge-only capture and inelastic channels"
    goal: "Bound the prompt (n,gamma) cascade recoils, the 71Ge EC lines, Ge inelastic, and the B4C 478 keV Compton continuum."
    methods: ["NCrystal Ge_sg227 bound-atom neutron kernel below 5 eV, spliced to ENDF free-atom"]
    depends_on: ["P-TGT neutron re-fold for Ge"]
    needs_research: true
    risk: HIGH
    pitfalls: ["thermal-flux-phi-th-unavailable", "elastic-only-channel-list"]
  - name: "P-EM gamma and muon re-fold"
    goal: "Re-fold the measured VNS gamma ambience and the attenuated muon flux through Ge on the extended grid."
    methods: ["Point-kernel gamma attenuation with ANS-6.4.3 buildup factors"]
    depends_on: ["P-ENV environment lock", "P-GRID grid extension and sub-eV observable"]
    needs_research: false
    risk: LOW
    pitfalls: ["bare-exp-mu-x-without-buildup"]
  - name: "P-LEE parameterized low-energy excess overlay"
    goal: "Carry the LEE as an (A, alpha) scan on the E_rec axis and report the break-even amplitude that erases the signal."
    methods: ["Two-parameter (A, alpha) LEE power-law overlay on the E_rec axis + break-even amplitude"]
    depends_on: ["P-GRID grid extension and sub-eV observable"]
    needs_research: false
    risk: HIGH
    pitfalls: ["lee-folded-through-response-matrix", "lee-single-number-overclaim"]
  - name: "P-SB signal-to-background assembly and framing"
    goal: "Assemble S/B_particle with min/max systematics, dual L2 reporting, and the LEE as a separately flagged overlay."
    methods: ["Flux/response factorization + analytic flat-box inversion of NUCLEUS deposit spectra", "Two-parameter (A, alpha) LEE power-law overlay on the E_rec axis + break-even amplitude"]
    depends_on: ["P-SIG CEvNS at the VNS normalization to 100 meV", "P-TGT neutron re-fold for Ge", "P-EM gamma and muon re-fold", "P-LEE parameterized low-energy excess overlay"]
    needs_research: false
    risk: MEDIUM
    pitfalls: ["systematics-dropped-tighter-than-source", "S-over-B-without-particle-qualifier", "on-off-not-clean-two-core"]

critical_benchmarks:
  - quantity: "NUCLEUS CaWO4 CEvNS, Table 5 at 100% duty"
    value: "218.2 mcpd = 356.5 counts/kg/day/keV"
    source: "Abele et al., EPJC 86, 29 (2026), Table 5 (rendered PDF)"
    confidence: HIGH
  - quantity: "Our independent CaWO4 CEvNS fold (signal-side closure test)"
    value: "407.7 counts/kg/day/keV; ratio 1.14 to Table 5 (closure 14%)"
    source: "project pipeline, orchestrator-established 2026-07-22"
    confidence: HIGH
  - quantity: "Ge vs CaWO4 CEvNS ratio, same pipeline, 10-100 eV, 100% duty"
    value: "2.31 (Ge 176.8 vs CaWO4 407.7); naive compound N^2/A ratio 1.95 must NOT be used as the benchmark"
    source: "project pipeline, orchestrator-established 2026-07-22"
    confidence: HIGH
  - quantity: "NUCLEUS Al2O3 CEvNS (unit-conversion calibration column)"
    value: "8.4 mcpd = 20.7 counts/kg/day/keV vs prose 'about 20'"
    source: "Abele et al., EPJC 86, 29 (2026), Table 5 + Sect. 2"
    confidence: HIGH
  - quantity: "NUCLEUS CaWO4 total particle background, 10-100 eV"
    value: "144 mcpd = 235.3 counts/kg/day/keV vs abstract ~250"
    source: "Abele et al., EPJC 86, 29 (2026), Table 5 + abstract (verified)"
    confidence: HIGH
  - quantity: "CaWO4/Al2O3 neutron ratio (target-scaling calibration)"
    value: "1.81 in 10-100 eV; 1.20 in 0.1-1 keV"
    source: "derived from Abele et al. Table 5"
    confidence: HIGH
  - quantity: "NUCLEUS published S/B band"
    value: "[0.9 - 1.5] at 68% CL, 1 keV_ee COV threshold, 10-100 eV"
    source: "Abele et al., EPJC 86, 29 (2026), Sect. 5.3 / Fig. 12"
    confidence: HIGH
  - quantity: "CONUS+ measured Ge-at-a-reactor S/B (limiting-case gate)"
    value: "~0.03 in 0.4-1 keV_ee at 7.4 m.w.e.; 395 +- 106 obs vs SM 347 +- 59 in 327 kg.d, 3.7 sigma"
    source: "CONUS+ Collab., Nature 643, 1229 (2025) (verified)"
    confidence: HIGH
  - quantity: "Ge displacement threshold / no-defect energy"
    value: "19.7 +0.6/-0.5 eV; no defect formation below ~6 eV; 6.08 +- 0.18% loss at ~100 keV"
    source: "Agnese et al. (SuperCDMS), APL 113, 092101 (2018) (verified)"
    confidence: HIGH
  - quantity: "CEvNS kinematic floor at T = 100 meV"
    value: "E_min = 58.16 keV (natural-Ge mean mass); flux truncation error <= 0.81%, exactly 0 above 0.29 eV"
    source: "orchestrator-established 2026-07-22; PRIOR-WORK Sect. 3.2"
    confidence: HIGH
  - quantity: "IA quantum broadening in Ge"
    value: "sigma_E/E_R = 1/sqrt(2W): 35-46% at 100 meV, 15.5-20.5% at 0.5 eV, 11-15% at 1 eV, 1.1-1.5% at 100 eV"
    source: "Sears framework, PRB 35, 2038 (1987); Ge numbers DERIVED in PRIOR-WORK"
    confidence: MEDIUM
  - quantity: "Emergent counting-resolution floor (best case, no noise sources)"
    value: "15.9% / 14.2% at 0.5 eV (N_obs 39.4 Ta->Al / 49.9 Al->Hf); 35.6% / 31.6% at 0.1 eV; 3.6% / 3.2% at 10 eV; 1.2% / 1.1% at 100 eV"
    source: "orchestrator finding from project code, 2026-07-22"
    confidence: HIGH
  - quantity: "Ge natural elastic resonance and its recoil imprint"
    value: "669.1 b at 102.6 eV -> recoils up to 5.5 eV (T_max/E_n = 0.0536)"
    source: "frozen Phase-7 artifact, ENDF/B-VIII.0 + Lib80x"
    confidence: HIGH
  - quantity: "TENDL-2023 / ENDF-B-VIII.0 splice step at 20 MeV, 74Ge"
    value: "+1.35% (1.247550 b vs 1.264380 b)"
    source: "COMPUTATIONAL.md, measured this survey"
    confidence: HIGH
  - quantity: "71Ge EC M-shell line"
    value: "158.7 +- 1.4 eV (L 1298.5 eV, K 10368.3 eV)"
    source: "CONUS+ sub-keV calibration, arXiv:2604.25748"
    confidence: MEDIUM-HIGH
  - quantity: "Ge phonon VDOS ceiling"
    value: "37.79 meV"
    source: "NCrystal Ge_sg227.ncmat, from Nelin & Nilsson, PRB 5, 3151 (1972)"
    confidence: HIGH

open_questions:
  - question: "Does a 110 g, 4-inch x 4-inch x 2 mm Ge wafer fit the NUCLEUS COV/IV veto envelope built for gram-scale crystals? If not, phi(E) at the detector position is no longer NUCLEUS's phi and nothing transfers."
    priority: HIGH
    blocks_phase: "P-VETO geometry fit and L1/L2 split"
  - question: "Which omega_bar does the project adopt? The <u^2>-derived 12-21 meV and the 37 meV optical phonon differ 2-3x, and both 2W and sigma_E scale linearly with it. Pin the 2W = q^2<u_x^2> vs q^2<u^2>/3 convention at the same time."
    priority: HIGH
    blocks_phase: "P-CONV phonon conventions and IA broadening"
  - question: "Two comparable smearing mechanisms sit at the 0.5 eV threshold - the emergent counting-statistics floor (15.9%/14.2%, best case only) and the unmodelled IA quantum broadening (15.5-20.5%). Their quadrature sum ~22-26% acts on the trigger sigmoid. How much does this move the effective threshold and the counted rate?"
    priority: HIGH
    blocks_phase: "P-CONV phonon conventions and IA broadening"
  - question: "What is the in-shield thermal neutron flux phi_th at the VNS? NUCLEUS does not publish it and the deposit-spectrum inversion cannot recover it (CaWO4/Al2O3 are blind to it)."
    priority: HIGH
    blocks_phase: "P-GEONLY Ge-only capture and inelastic channels"
  - question: "Are NUCLEUS Figs. 8-11 plotted pre- or post-veto? If post-veto, the recovered phi is a veto-survival-weighted fluence and only transfers under the same veto acceptance."
    priority: HIGH
    blocks_phase: "P-TGT neutron re-fold for Ge"
  - question: "What LEE amplitude and shape should be carried for a QPD wafer with ~10,300 Al-class films? Romani predicts A_Al-area scaling with meV-eV phonons; no measurement exists below ~10 eV in Ge or at 100 meV in any material."
    priority: HIGH
    blocks_phase: "P-LEE parameterized low-energy excess overlay"
  - question: "Can the machinery reproduce CONUS+'s measured ~0.03 at 160 eV_ee and 7.4 m.w.e.? Until it does, the predicted 0.65-1.2 (more than an order of magnitude better than published state of the art) is unvalidated."
    priority: HIGH
    blocks_phase: "P-SIG CEvNS at the VNS normalization to 100 meV"
  - question: "Does E_rec ~= 0.5 E_dep hold at 100 meV, where the deposit is ~3 optical-phonon quanta reaching one sensor rather than the array? No literature addresses this; it is our own detector-physics assumption."
    priority: MEDIUM
    blocks_phase: "P-GRID grid extension and sub-eV observable"
  - question: "Confirm directly against the IAEA/NNDC TSL material list that no germanium thermal scattering law exists in ENDF/B-VIII.0 or VIII.1. If one exists, NCrystal becomes optional rather than required."
    priority: MEDIUM
    blocks_phase: "P-TGT neutron re-fold for Ge"
  - question: "Reconcile E_min(100 meV) = 58.16 keV (natural-Ge mean mass) with the project-frozen 58.7 keV (74Ge-only). ~1% and trivial, but the whole flux-extension argument is stated in terms of this number."
    priority: LOW
    blocks_phase: "none"

contradictions_unresolved:
  - claim_a: "The LEE can be suppressed by holder/mounting redesign - Anthony-Petersen et al. report >100x rate reduction going glued -> suspended in Si."
    claim_b: "Holder redesigns produce no measurable improvement - CRESST-III (Cu sticks, bronze clamps, foil removal) and RICOCHET (improved holding scheme) both report no significant impact."
    source_a: "Anthony-Petersen et al., Nat. Commun. 15, 6444 (2024)"
    source_b: "Angloher et al. (CRESST-III), SciPost Phys. Proc. 12, 013 (2023); RICOCHET CryoCube in arXiv:2202.05097"
    investigation_needed: "Possibly reconcilable - Anthony-Petersen changed the mounting topology while CRESST/RICOCHET made incremental changes (stick material, clamp area). Until resolved, the milestone must NOT claim that mounting 'fixes' the LEE, in either direction."
  - claim_a: "The LEE burst source scales with substrate VOLUME - the 4 mm Si detector's correlated noise is 4x the 1 mm detector's (0.932 g vs 0.233 g)."
    claim_b: "The LEE scales with aluminium FILM AREA times dislocation density, N = A_Al x rho_D."
    source_a: "Chang et al., APL 127, 263502 (2025)"
    source_b: "Romani, J. Appl. Phys. 136, 124502 (2024)"
    investigation_needed: "The two models predict different scalings to a 110 g wafer carrying ~10,300 films: volume scaling gives ~120-470x from Chang's devices, area scaling gives a different and design-controllable number. Neither extrapolation is defensible as a prediction. Resolve by reporting a break-even amplitude rather than a predicted rate, and carry both scalings as the band."
```
