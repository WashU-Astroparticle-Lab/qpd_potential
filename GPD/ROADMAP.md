# Roadmap: QPD Particle-Physics Potential

## Milestones

- Done: **v1.0 Reconstructed-Energy Spectra** — Phases 1–6 (completed 2026-07-22). Reactor-CEvNS, cosmic-muon, and environmental-gamma Compton differential rate spectra in reconstructed energy for a ~110 g QPD Ge wafer, both trapping designs. Full detail: [`milestones/v1.0-ROADMAP.md`](milestones/v1.0-ROADMAP.md); digest: [`milestones/v1.0/RESEARCH-DIGEST.md`](milestones/v1.0/RESEARCH-DIGEST.md).
- Superseded: **v1.1 Neutron & Radiogenic Backgrounds** — Phase 7 executed and **carried forward**; Phases 8–12 **withdrawn** (2026-07-22). Rationale in [`MILESTONES.md`](MILESTONES.md); the v1.1 roadmap text is in git history at `40804a5`.
- Active: **v2.0 QPD at the NUCLEUS Chooz Very-Near-Site** — Phases 8–16. Reactor-CEvNS signal and the full in-band particle-background budget in reconstructed energy down to 100 meV for the ~110 g Ge wafer deployed at the Chooz VNS behind the NUCLEUS shielding, with that experiment's measured environment adopted as input and the target response re-folded for Ge.
- Planned: **Manuscript / Sensitivity** — MANU-01 (round-1 peer-review revision), SENS-01 (quantitative CEvNS discovery/exclusion sensitivity). Deferred; enabled by the v2.0 background budget.

## Overview

v2.0 answers a single question: what signal-to-background does a ~110 g QPD Ge wafer achieve at the NUCLEUS Chooz Very-Near-Site, in reconstructed energy, down to 100 meV? The structural premise — established by all four v2.0 scouts and the synthesis — is that **only the target-independent fluence φ(E) at the detector position transfers from NUCLEUS to us**; every deposit spectrum, residual rate, and veto factor they publish is a `φ ⊗ kernel ⊗ payload` product that must be re-folded, never rescaled. The roadmap therefore opens with the one question that can void that premise (does the wafer even fit their veto envelope?), then locks and inverts their published environment, then extends the pipeline two decades below its validated floor where a genuinely new physics input — impulse-approximation quantum broadening — becomes comparable to the detector's own counting-statistics floor, and only then re-folds each channel through Ge and assembles `S/B_particle` behind a hard CONUS+ reproduction gate.

Nine phases (8–16). The signal-side target-swap closure test has **already passed** (our independent CaWO₄ fold gives 407.7 vs NUCLEUS Table 5's 356.5 at 100% duty, closure 14%), so this roadmap does not repeat it — it requires the **background-side** equivalent instead (VALD-11, the two-band CaWO₄/Al₂O₃ neutron ratio calibration). No phase carries an OpenMC, MCNP, Geant4, or G4CMP dependency: OpenMC is unbuildable on osx-arm64 (established v1.1, re-confirmed by the computational scout) and full Geant4 transport of the NUCLEUS geometry is out of scope by explicit user decision. Any transport fallback is SIMU-05, which is follow-up scope.

## Contract Overview

| Contract Item | Advanced By Phase(s) | Status |
| ------------- | -------------------- | ------ |
| **Stop-condition** Wafer-vs-COV/IV envelope fit determination (VALD-09) | Phase 8 | Planned |
| L1/L2 rejection taxonomy; L2-off (zero inherited veto credit) baseline | Phase 8 (defines), Phase 16 (reports) | Planned |
| Digitized + frozen NUCLEUS VNS input set, provenance-headed (CALC-11) | Phase 9 | Planned |
| φ_post(E_n) post-shield fluence at the target position (CALC-12) | Phase 9 | Planned |
| **Gate** Two-band CaWO₄/Al₂O₃ neutron ratio calibration, 1.81 & 1.20 from one normalization (VALD-11) | Phase 9 | Planned |
| Extended `shared_energy_grid()` to 0.1 eV + regenerated `R(E_rec\|E_dep)` (CALC-13) | Phase 10 | Planned |
| Trigger-probability curve, sigmoid 50% at 0.5 eV, multiplying ε ≈ 0.5 (CALC-16) | Phase 10 | Planned |
| ω̄ + Debye–Waller convention pinned in CONVENTIONS.md (CALC-14) | Phase 11 | Planned |
| IA quantum broadening σ_E = √(E_R ω̄) applied before the response chain (CALC-15) | Phase 11 | Planned |
| Sub-100 keV flux truncation bound reported, table NOT extended (CALC-17) | Phase 12 | Planned |
| Sub-eV validity gates: <1% v1.0 regression above 10 eV; flat dR/dT plateau (VALD-10) | Phase 12 | Planned |
| CEvNS dR/dE_rec at the VNS normalization down to 100 meV, both designs | Phase 12 | Planned |
| Ge neutron NR dR/dE_rec re-folded from φ_post (CALC-18) | Phase 13 | Planned |
| Ge-only thermal capture: prompt (n,γ) recoils + ⁷¹Ge EC M-shell 158.7 eV (CALC-23) | Phase 14 | Planned |
| Compton ER dR/dE_rec from the **measured** VNS ambience (CALC-19) | Phase 15 | Planned |
| Muon dR/dE_rec at 2.92 m.w.e., attenuation 1.41 (CALC-20) | Phase 15 | Planned |
| LEE (A, α) overlay band + break-even amplitude at S/B_particle = 1 (CALC-21) | Phase 16 | Planned |
| **Terminal** S/B_particle, both designs, with mandatory L2-off baseline (CALC-22) | Phase 16 | Planned |
| **Hard gate** CONUS+ limiting-case reproduction, S/B ≈ 0.03 (VALD-12) | Phase 16 | Planned |
| **Anchor** NUCLEUS EPJC 86, 29 (2026) arXiv:2509.03559 — Figs. 4, 8–11; Tables 2–5 | Phases 8, 9, 13, 15, 16 | Planned |
| **Anchor** NUCLEUS **Table 5 at 100% duty** (CaWO₄ 356.5 dru) — *never* the §2 prose 280 | Phases 9, 12, 16 | Planned |
| **Anchor** NUCLEUS EPJC 79, 1018 (2019) arXiv:1905.10258 — VNS site geometry, Fig. 1 Ge curve | Phases 8, 12 | Planned |
| **Anchor** CONUS+ Nature 643, 1229 (2025) — only measured Ge-at-a-reactor S/B | Phase 16 | Planned |
| **Anchor** Campbell-Deem PRD 106, 036019; Sears PRB 35, 2038 — IA framework | Phase 11 | Planned |
| **Anchor** NCrystal `Ge_sg227.ncmat` (Nelin & Nilsson PRB 5, 3151) — Ge VDOS, bound-atom kernel | Phases 11, 13 | Planned |
| **Anchor** SuperCDMS APL 113, 092101 — Ge displacement threshold 19.7 eV, no defect below ~6 eV | Phase 11 | Planned |
| **Anchor** Romani JAP 136, 124502; NUCLEUS arXiv:2603.07687 (k = 0.59 ± 0.06) — LEE | Phase 16 | Planned |
| **Anchor** Biffl et al. PRD 107, 092011; ENDF MT=102 + EGAF — capture recoils | Phase 14 | Planned |
| **Prior output** Phase 7 frozen ENDF/B-VIII.0 n-Ge elastic (23,155-pt grid, 293.6 K), T_max/E_n = 0.0536, λ = 6.076 cm, P_int(2 mm) = 3.24% | Phases 9, 13, 14 | Planned |
| **Prior output** v1.0 `shared_energy_grid()`, `R(E_rec\|E_dep)` matrices, Klein–Nishina and Gaisser–Guan ⊗ chord ⊗ Landau machinery, CONVENTIONS §B/§E/§F | Phases 10, 12, 15 | Planned |
| **Prior output** Our CaWO₄ closure fold 407.7 dru (ratio 1.14 to Table 5) — signal-side closure **already passed** | Phase 12 (cited, not re-run) | Planned |
| **Prior output** Ge/CaWO₄ same-pipeline ratio 2.31 (176.8 vs 407.7) | Phase 12 | Planned |

**Forbidden proxies (must stay visible milestone-wide):** `fp-deposited-only`, `fp-no-saturation`, `fp-full-absorption`, keVee↔keVnr mixing / Lindhard quenching on the phonon scale, `fp-lumped-A`, `fp-gwe-gwth`, `fp-nucleus-3e12` (folding at the 2019 prose flux), **`fp-nucleus-prose-280`** (anchoring on the §2 prose CEvNS value instead of Table 5 — flatters S/B by 27%), **`fp-veto-credit-transfer`** (inheriting gram-scale veto rejection for a 110 g monolithic wafer), **`fp-lee-omission`** (reporting S/B without the LEE band), **`fp-mass-scaled-target`** (scaling CaWO₄/Al₂O₃ residuals to Ge by mass), **`fp-poisson-as-resolution`** (quoting the emergent counting floor as a resolution model).

**Milestone-wide additional prohibitions:** never multiply the CEvNS rate by e^(−2W) (it suppresses the zero-phonon channel only; the strength moves into the multiphonon continuum); never use the naive compound N²/A ratio 1.95 as the Ge/CaWO₄ benchmark (the same-pipeline fold gives 2.31); never quote a Ge uncertainty band tighter than the NUCLEUS band it is anchored to.

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

<details>
<summary>Superseded: v1.1 Neutron & Radiogenic Backgrounds — Phase 7 carried forward, Phases 8–12 withdrawn 2026-07-22</summary>

- [x] Phase 7: Scenario & Nuclear-Data Lock (2/2 plans) — **carried forward into v2.0.** Frozen ENDF/B-VIII.0 + Lib80x n-Ge elastic table (thermal→20 MeV, 23,155-point resonance-resolved union grid, 293.6 K free-gas), natural resonance peak 669.1 b at 102.6 eV, σ_tot(1–2 MeV) = 3.729 b, Σ = 0.1646 cm⁻¹, λ = 6.076 cm, P_int(2 mm) = 3.24%, abundance-weighted natural T_max/E_n = 0.0536. Verified 19/22 with gaps; gap D1 (20 MeV ENDF ceiling) carried forward.
- Withdrawn: Phases 8 (P-NSRC), 9 (P-NTRANS), 10 (P-RAD), 11 (P-COSMO), 12 (P-FOLD) — all premised on surface/unshielded fluxes at a generic 3 GW_th / 25 m site. Their physics content is re-scoped inside v2.0 against the shielded VNS environment. **The v2.0 phase numbers 8–12 reuse those retired numbers.**

</details>

### Active: v2.0 QPD at the NUCLEUS Chooz Very-Near-Site (Phases 8–16)

**Milestone Goal:** Compute the reactor-CEvNS signal and the full in-band particle-background budget in reconstructed energy, from 100 meV upward, for the ~110 g QPD Ge wafer at the Chooz VNS behind the NUCLEUS shielding — adopting NUCLEUS's measured environment and passive attenuation as input while re-folding every target response through Ge — and report `S/B_particle` in the 10–100 eV RoI and below, with the LEE as an explicit overlay band and a mandatory zero-veto-credit baseline.

- [ ] **Phase 8: Veto-Envelope Geometry Gate (P-VETO)** — **GATING STOP-CONDITION.** Determine whether the 110 g wafer fits the NUCLEUS COV/IV envelope and fix which rejection transfers; if it does not fit, STOP and re-scope with the user
- [ ] **Phase 9: VNS Environment Lock and Post-Shield Fluence Recovery (P-ENV)** — transcribe and freeze the NUCLEUS inputs, invert their deposit spectra for φ_post(E_n), and pass the two-band neutron-ratio calibration that licenses the Ge swap
- [ ] **Phase 10: Sub-eV Grid Extension and the Trigger Observable (P-GRID)** — extend the shared grid to 0.1 eV, regenerate the response matrices, and install the 0.5 eV trigger-probability curve as the sub-eV observable
- [ ] **Phase 11: Phonon-Scale Conventions and IA Quantum Broadening (P-CONV)** — pin ω̄ and the Debye–Waller convention from the real Ge VDOS, then apply the impulse-approximation broadening before the response chain
- [ ] **Phase 12: Reactor CEvNS at the VNS Normalization down to 100 meV (P-SIG)** — produce the signal spectrum at ∫Φ = 2.1×10¹² ν̄/cm²/s with the flux-truncation bound reported and the sub-eV validity gates passed
- [ ] **Phase 13: Ge Neutron Re-Fold (P-TGT)** — fold φ_post through the frozen Ge elastic kernel with the resonance structure intact, never by mass-scaling their residuals
- [ ] **Phase 14: Ge-Only Thermal-Capture Channels (P-GEONLY)** — bound the prompt (n,γ) cascade recoils and the ⁷¹Ge EC lines that CaWO₄/Al₂O₃ are structurally blind to; a quantified gap is an acceptable outcome, zero is not
- [ ] **Phase 15: Gamma and Muon Re-Fold at the VNS (P-EM)** — re-drive the Compton and muon channels from the measured VNS ambience and the 2.92 m.w.e. overburden, retiring the v1.0 surface normalizations
- [ ] **Phase 16: S/B_particle Assembly, LEE Overlay, and the CONUS+ Gate (P-SB)** — **TERMINAL.** Reproduce CONUS+ as a limiting case, then assemble S/B_particle with an L2-off baseline and the LEE erasure amplitude

## Phase Details

### Phase 8: Veto-Envelope Geometry Gate (P-VETO)

**Goal:** It is established, from published geometry rather than assumption, whether a 4″×4″×2 mm ~110 g Ge wafer can occupy the NUCLEUS COV/IV veto envelope built around gram-scale 3×3 arrays — and, if it can, exactly which layers of rejection survive the swap and which do not.
**Depends on:** Nothing in v2.0 (entry point). Consumes v1.0 wafer geometry and the v1.0 Gaisser–Guan ⊗ chord machinery.
**Requirements:** VALD-09.
**Contract Coverage:**
- Advances: VALD-09 (geometry-fit determination); defines the L1/L2 taxonomy and the L2-off baseline that Phase 16 must report.
- Deliverables: fit / no-fit determination with clearances in cm and figure-panel provenance; written L1/L2 rejection taxonomy; the wafer's own muon-veto acceptance derived from its own chord distribution.
- Anchor coverage: NUCLEUS EPJC 86, 29 (2026) Fig. 1e/f and §5.2.1 (MV+COV > 99.8%, COV factor ~5 at 1 keV_ee); NUCLEUS EPJC 79, 1018 (2019) VNS site geometry; Goupy 2024 thesis (NNT 2024UNIP7170) where the paper is silent; wafer 103 cm² vs their ~9 cm².
- Forbidden proxies: `fp-veto-credit-transfer` — inheriting gram-scale rejection factors for a 110 g monolithic wafer; **inventing a resized veto or continuing with a reduced veto credit if the gate fails** (explicit user decision 2026-07-22); proceeding past a failed gate on a premise already known false.
**Success Criteria** (what must be TRUE):

1. The COV/IV internal envelope dimensions are read directly from NUCLEUS Fig. 1e/f (supplemented by the Goupy thesis where the paper is silent), recorded with panel/figure provenance, and compared against the wafer's 103 cm² × 2 mm footprint as an explicit fit / no-fit determination quoting the clearance (or the shortfall) in cm.
2. The L1/L2 taxonomy is written down and binding: **L1** (environmental — 2.92 ± 0.01 m.w.e. overburden, Table 4 surface fluxes, passive external 5 cm Pb + 20 cm borated HDPE attenuation) transfers; **L2** (payload-coupled — COV factor ~5, MV+COV > 99.8%, 3×3 multiplicity) defaults to **1.0** and may not appear in any downstream code path without wafer geometry behind it.
3. The wafer's own muon-veto acceptance is *derived* from its own chord-length distribution using the v1.0 Gaisser–Guan ⊗ chord machinery — no NUCLEUS rejection percentage is transferred as a number.
4. The monolithic single-readout wafer is shown to carry **no multiplicity handle at all**, so NUCLEUS's multiplicity cut contributes exactly zero rejection, and this is stated explicitly rather than absorbed into a lumped factor.
5. **Stop-condition discharged:** if the wafer does not fit, the phase reports the milestone premise as void — a forced shield/veto redesign means φ_post at the detector position is no longer NUCLEUS's φ_post and essentially nothing transfers — and returns control to the user for re-scope. No reduced veto credit is assumed and no resized veto is invented.

**Status:** COMPLETE 2026-07-22 — **gate discharged NO FIT**. See `08-05-GATE-VERDICT.md`.
Milestone premise reported VOID; awaiting user re-scope decision.
SC1 evidence-route amendment: EPJC 86,29 Fig. 1 was confirmed to carry no scale bar or dimension
callout, so SC1 as literally worded is not dischargeable from it; the verdict rests on
arXiv:2508.02488 (promoted to a Phase-8 anchor during execution; describes the TUM commissioning
setup, not Chooz) corroborated by arXiv:1905.10258.

**Plans:** 5 plans

Plans:
- [x] 08-01-PLAN.md -- Freeze and integrity-check the primary NUCLEUS sources; emit the grep-verified verbatim evidence block; establish that EPJC 86,29 Fig. 1 carries no scale bar or dimension callout
- [x] 08-02-PLAN.md -- Derive the wafer's own muon self-veto acceptance as two separate numbers (A_self_direct, A_self_induced = 0) and establish the multiplicity rejection as exactly zero
- [x] 08-03-PLAN.md -- Amend SC1's evidence route with justification and compute the fit determination on three bases with tight/loose bounds and stated uncertainty
- [x] 08-04-PLAN.md -- Write the binding L1/L1*/L2 taxonomy, place L2 and L1* credits in code as 1.0 sentinels, correct the factor-5 and ~9 cm^2 errors in PITFALLS.md
- [x] 08-05-PLAN.md -- Discharge the VALD-09 gate, report the premise and phase-by-phase disposition, return control to the user for re-scope

### Phase 9: VNS Environment Lock and Post-Shield Fluence Recovery (P-ENV)

**Goal:** The NUCLEUS environment is transcribed once, correctly, with a single validated unit conversion and a single duty-cycle declaration; the post-shield neutron fluence φ_post(E_n) at the target position is recovered by regularized inversion of their published deposit spectra; and the transfer machinery is proven on their own two published targets before any Ge number is attempted.
**Depends on:** Phase 8 (the gate must close — if the wafer does not fit, φ_post is not NUCLEUS's φ_post and this phase is void).
**Requirements:** CALC-11, CALC-12, VALD-11.
**Contract Coverage:**
- Advances: CALC-11 (frozen digitized input set), CALC-12 (φ_post recovery), VALD-11 (two-band neutron-ratio calibration — the checkpoint that licenses the Ge swap).
- Deliverables: provenance-headed digitizations of Fig. 4 (VNS-room neutron spectrum, plotted as E·dΦ/dE on a log-E axis) and Figs. 8–11 (component-resolved deposit spectra); transcribed Tables 2–5 with Table 4 uncertainties (μ 25%, n 30%, γ 20%, materials 30%) wired in; one `mcpd_to_dru()` with named cited constants; φ_post(E_n) artifact with a ζ error budget; pre-vs-post-veto determination for Figs. 8–11.
- Anchor coverage: NUCLEUS EPJC 86, 29 (2026) Figs. 4, 8–11 and Tables 2–5; **Table 5 at 100% duty** (CaWO₄ CEvNS 218.2 mcpd → 356.5 dru; Al₂O₃ 8.4 mcpd → 20.7 dru; CaWO₄ total 144 mcpd → 235.3 dru vs abstract ~250); the VALD-02 digitizer (reproduced a published Ge curve to 5%); Phase 7 frozen flat-box recoil kernel and T_max/E_n = 0.0536.
- Forbidden proxies: `fp-nucleus-prose-280` (the §2 prose 280 is the 80%-duty value: 356.5 × 0.8 = 285); `fp-nucleus-3e12`; lethargy-vs-per-energy confusion (divide by E exactly once, in one place); reading post-veto curves as pre-veto; finite-difference differentiation of digitized data.
**Success Criteria** (what must be TRUE):

1. A single `mcpd_to_dru()` with named, cited constants (6.8 g CaWO₄ / 4.5 g Al₂O₃ array masses, **0.09 keV** RoI width) reproduces the Al₂O₃ CEvNS column at **20.7** dru against the prose "about 20" and the CaWO₄ total at **235.3** dru against the abstract's ~250. The duty cycle is applied exactly once in the call graph, every CEvNS entry carries a duty-cycle label, and the anchor is **Table 5 at 100% duty (356.5)** — never the prose 280.
2. Every digitized curve carries panel / trace / cut / axis provenance in a machine-readable header (Phase-7 precedent); the lethargy → per-energy division happens exactly once; integral-conserving rebinning preserves the integral to <1%; and the digitized integrals close against the printed totals. Digitization accuracy is ~5% outside the steep region, with the steep-region degradation stated rather than hidden.
3. Whether NUCLEUS Figs. 8–11 are plotted **pre- or post-veto** is determined from the captions and text and recorded as a finding. The inverted object is labelled accordingly — a fluence if pre-veto, a **veto-survival-weighted** fluence if post-veto — and if post-veto, the condition under which it transfers (same veto acceptance) is stated explicitly, which Phase 8 has already shown we do not have.
4. φ_post(E_n) is recovered by **regularized** differentiation (Tikhonov/TV, never finite differences) through the flat-box recoil kernel `φσ = −(f²E/N)G′(fE)`, is non-negative everywhere, and the CaWO₄-derived and Al₂O₃-derived solutions agree within a factor ≲1.5 — the built-in over-determination test that two published targets provide. A δ-function flux input returns an exact flat box of height σ/(fE₀).
5. **VALD-11 gate (licenses the Ge swap):** both published CaWO₄/Al₂O₃ neutron rate ratios — **1.81** in 10–100 eV and **1.20** in 0.1–1 keV — are reproduced from a **single** normalization. A band-independent ratio (the crude flat-box estimate gives ≈1.1, ~60% low on a ratio where normalization cancels) means the kinematic-compression physics has been lost and the gate fails; Phase 13 does not start until it passes.

**Plans:** TBD (run `gpd:plan-phase 9` to break down)

### Phase 10: Sub-eV Grid Extension and the Trigger Observable (P-GRID)

**Goal:** The pipeline's energy axis reaches 0.1 eV with every response matrix regenerated and every legacy artifact either re-gridded or explicitly bounded, and the *observable itself* is redefined below ~1 eV — where a differential rate is not the right object — as a trigger-probability curve with a fixed 0.5 eV midpoint.
**Depends on:** Phase 8 (gate). Independent of Phase 9 — runs in parallel with it.
**Requirements:** CALC-13, CALC-16.
**Contract Coverage:**
- Advances: CALC-13 (extended grid + regenerated `R(E_rec|E_dep)`), CALC-16 (trigger-probability curve).
- Deliverables: `shared_energy_grid()` from 0.1 eV (~744 bins at 80/decade); regenerated `R(E_rec|E_dep)` for both designs; the sigmoid analysis-efficiency curve; a re-grid / tag disposition for every archived v1.x spectrum; the emergent counting-resolution floor documented as best-case-only.
- Anchor coverage: v1.0 `shared_energy_grid()` and `R(E_rec|E_dep)` matrices; CONVENTIONS §E/§F (ε ≈ 0.5, 25 kHz non-paralyzable); per-sensor saturation onsets 1.27 eV (Ta→Al) / 0.77 eV (Al→Hf); the 24 v1.0/v1.1 anchors.
- Forbidden proxies: `fp-poisson-as-resolution` — the counting floor is an emergent best case, not a resolution model; silent clamping or extrapolation at a table floor; treating the sigmoid as a *replacement* for ε ≈ 0.5; retaining the retracted "never display below 10 eV" rule as a physics statement.
**Success Criteria** (what must be TRUE):

1. `shared_energy_grid()` runs from **0.1 eV** at 80 bins/decade (~744 bins) and `R(E_rec|E_dep)` is regenerated for **both** designs on it, with count conservation preserved to ≤1e-3 and all 24 v1.0/v1.1 anchors still reproducing.
2. Every archived v1.x spectrum is either re-gridded onto the extended axis or explicitly tagged **valid only above 10.14 eV**; no legacy artifact is silently reinterpolated onto the new grid.
3. Every interpolator **raises** outside its evaluated range — no clamping, no silent extrapolation, no returning zero at a table floor — unit-tested at each table's actual floor. (This is the guard against a kinematic threshold silently falling below a tabulated floor and yielding zero instead of an error.)
4. The trigger-probability sigmoid has its **50% point exactly at 0.5 eV** and is **multiplied on top of all other efficiencies including ε ≈ 0.5**, verified by a unit test on the composed efficiency chain showing it does not replace ε. Below ~1 eV deposit, this curve — not dR/dE_rec — is the reported observable, and the regime boundary is labelled on every sub-eV deliverable.
5. The emergent counting-statistics floor is documented as a **best case with no noise sources** (15.9% / 14.2% at 0.5 eV from N_obs = 39.4 / 49.9; 35.6% / 31.6% at 0.1 eV; 3.6% / 3.2% at 10 eV; 1.2% / 1.1% at 100 eV) and is explicitly *not* presented as the detector's resolution — the project has no resolution parameter, and the comparable unmodelled IA broadening arrives in Phase 11.

**Plans:** TBD (run `gpd:plan-phase 10` to break down)

### Phase 11: Phonon-Scale Conventions and IA Quantum Broadening (P-CONV)

**Goal:** The effective phonon energy ω̄ and the Debye–Waller convention are pinned from the real Ge vibrational density of states — closing a 2–3× ambiguity that propagates linearly into everything sub-eV — and the recoil spectrum stops being a delta function: impulse-approximation quantum broadening, the largest new physics input of this milestone, is applied before the response chain.
**Depends on:** Phase 10 (extended grid and regenerated response matrices).
**Requirements:** CALC-14, CALC-15.
**Ordering constraint (binding):** CALC-14 must be its **own early plan** (11-01) and must complete before CALC-15 (11-02) begins. Both 2W and σ_E scale **linearly** with ω̄, and the ⟨u²⟩-derived 12–21 meV and the 37 meV optical-phonon value differ by 2–3×. This is a CONVENTIONS.md decision, not an implementation detail, and it must not be buried inside the broadening implementation.
**Contract Coverage:**
- Advances: CALC-14 (ω̄ + Debye–Waller convention locked in CONVENTIONS.md), CALC-15 (IA Gaussian broadening).
- Deliverables: CONVENTIONS.md entry fixing ω̄ ≡ ħ/(2 m_N ⟨u_x²⟩) and 2W = q²⟨u_x²⟩ (1-D); ω̄ and ⟨u_x²⟩ computed from the Ge VDOS; the IA convolution applied to dR/dE_R before the response chain; a bounded one-off impulse-limit justification artifact.
- Anchor coverage: NCrystal `Ge_sg227.ncmat` (Nelin & Nilsson, PRB 5, 3151 (1972)) cross-checked against DarkELF `Ge_pDoS.dat`; Sears PRB 35, 2038 (1987) IA/final-state framework; Campbell-Deem et al. PRD 106, 036019 (IA criterion q ≫ √(2 m_d ω̄_d)); SuperCDMS APL 113, 092101 (displacement threshold 19.7 ⁺⁰·⁶₋₀·₅ eV, no defect below ~6 eV — strengthens the unified phonon scale in-window); frozen v1.0 spectra above 10 eV.
- Forbidden proxies: multiplying the rate by e^(−2W) — it suppresses only the zero-phonon channel and would erase a real signal; the 3-D/1-D factor-3 trap (q²⟨u²⟩/3 instead of q²⟨u_x²⟩); quoting the survey's derived Ge numbers instead of re-deriving them in-phase; building a coherent-crystal S(q,ω) backbone (rejected in synthesis — the coherent channel is extinct, e^(−2W) ≈ 10⁻² at 100 meV and ~10⁻²⁰ at 1 eV).
**Success Criteria** (what must be TRUE):

1. **[CALC-14, first]** ω̄ and ⟨u_x²⟩ are pinned in CONVENTIONS.md from the real Ge VDOS — not from the Debye model — with `2W = q²⟨u_x²⟩` (1-D MSD) locked and the `q²⟨u²⟩/3` form explicitly rejected; `B = 8π²⟨u_x²⟩` is quoted alongside. One number, one convention, one citation; the 12–21 vs 37 meV ambiguity is closed by an argued choice, not carried as a range.
2. The VDOS reproduces the measured ceiling **37.79 meV**, the VDOS-integral ⟨u²⟩ agrees with the Debye value (1.34×10⁻³ Å²) within ~1.5×, and the resulting 2W at 100 meV lands at ≈4.7–8.3 — consistent with the independent momentum-transfer route q(100 meV) = 116 keV/c = 58.9 Å⁻¹.
3. **[CALC-15]** σ_E = √(E_R ω̄) is **re-derived in-phase** (the survey's Ge numbers are derived, not literature-quoted) and reproduces σ_E/E_R = 1/√(2W): 35–46% at 100 meV, **15.5–20.5% at the 0.5 eV threshold**, 11–15% at 1 eV, 1.1–1.5% at 100 eV, negligible above. The quadrature sum with the Phase-10 counting floor (~22–26% at 0.5 eV) is reported, since both act on the trigger sigmoid at the same energy.
4. The Gaussian convolution is applied to dR/dE_R **before** the response chain, conserves counts to ≤1e-3, and vanishes in the correct limit: the broadened spectrum reproduces the frozen v1.0 result above ~10 eV to **<1%**.
5. The rate is never multiplied by e^(−2W); a bounded justification artifact demonstrates via the f-sum rule that S(q,ω) → δ(ω − q²/2M) is reached by ~100 meV and quantifies the residual O(1/2W) correction in the bottom bin, without becoming a milestone pillar.

**Plans:** TBD (run `gpd:plan-phase 11` to break down)

### Phase 12: Reactor CEvNS at the VNS Normalization down to 100 meV (P-SIG)

**Goal:** The reactor-CEvNS signal spectrum in reconstructed energy exists at the VNS normalization from 100 meV upward, with quantum broadening and the trigger curve applied, and its low-energy behaviour is *proven* correct — flat where it must be flat, unchanged where it was already validated, and bounded where the input table runs out.
**Depends on:** Phase 9 (normalization and duty-cycle lock), Phase 11 (ω̄ and the IA broadening). Runs in parallel with Phase 13.
**Requirements:** CALC-17, CALC-25, VALD-10.
**Contract Coverage:**
- Advances: CALC-17 (flux-truncation bound), VALD-10 (sub-eV validity gates); produces the milestone's decisive **signal** deliverable — CEvNS dR/dE_rec at the VNS normalization, both designs, to 100 meV.
- Deliverables: dR/dE_rec at ∫Φ = 2.1×10¹² ν̄/cm²/s (two Chooz-B cores, 4.25 GW_th each, 72 m and 102 m, 80% duty declared once); the trigger-probability curve below ~1 eV; the computed truncation bound; the plateau and regression test reports.
- Anchor coverage: **NUCLEUS Table 5 at 100% duty (356.5 dru)**; our already-passed CaWO₄ closure fold **407.7** dru (ratio 1.14, closure 14%) — cited, **not re-run**; Ge/CaWO₄ same-pipeline ratio **2.31** (176.8 vs 407.7, 10–100 eV, 100% duty); frozen v1.0 CEvNS CSVs; NUCLEUS 2019 Fig. 1 Ge curve (reproduced to 5% by the VALD-02 anchor); frozen ∫Φ and the Huber–Mueller + sub-1.8 MeV band.
- Forbidden proxies: `fp-nucleus-prose-280`; `fp-gwe-gwth`; extending the reactor flux table below 100 keV (report the bound instead); the naive compound N²/A ratio 1.95 as the Ge/CaWO₄ benchmark; repeating the signal-side closure test in place of the background-side one (VALD-11, Phase 9).
**Success Criteria** (what must be TRUE):

1. CEvNS dR/dE_rec is produced at ∫Φ = 2.1×10¹² ν̄/cm²/s for both designs from 100 meV, with the IA broadening applied before the response chain and the 0.5 eV trigger curve applied on top of ε ≈ 0.5; the duty cycle is declared exactly once at the pipeline top, and the drop relative to the v1.0 3 GW_th / 25 m flagship (~3.6×) is quantified.
2. **VALD-10 plateau (asserted, not inspected):** dR/dT is **flat** from 100 meV to 10 eV to within a few percent and equals the analytic T→0 plateau computed from the frozen ∫Φ with the flat-box dσ/dT. A spectrum that *rises* toward low T is an extrapolation artifact; one that *falls to zero* is a table floor. Both failure modes are unit-tested, not eyeballed.
3. **VALD-10 regression:** above ~10 eV the extended pipeline reproduces the committed frozen v1.0 CEvNS CSVs to **<1%** — no silent change to validated results — and T = 0.290 eV reproduces the frozen v1.0 value exactly.
4. **CALC-17:** the sub-100 keV flux-truncation bound is **computed** with the project's own Φ (flat continuation of Φ at its 100 keV value, including the (1 − MT/2E²) kinematic factor), reproducing **≤0.81% at T = 100 meV and exactly zero above 0.29 eV**. The flux table is **not** extended. E_min(100 meV) = **58.16 keV** (natural-Ge mean mass) is adopted and reconciled against the project-frozen 58.7 keV (⁷⁴Ge-only, ~1% abundance weighting).
5. The Ge/CaWO₄ same-pipeline ratio **2.31** is documented with the naive compound N²/A ratio **1.95** explicitly rejected as a benchmark (CaWO₄ compound N²/A = 44.2, not 65.8 which is pure W); the already-passed 14% signal-side closure against Table 5 is cited as prior evidence rather than recomputed.

**Plans:** TBD (run `gpd:plan-phase 12` to break down)

### Phase 13: Ge Neutron Re-Fold (P-TGT)

**Goal:** The dominant background — neutrons are ~91% of the NUCLEUS RoI budget — exists as a Ge nuclear-recoil spectrum in reconstructed energy, derived from the recovered fluence through Ge's own kinematics and resonance structure, with the kinematic compression that makes Ge worse than CaWO₄ visible rather than assumed away.
**Depends on:** Phase 9 (φ_post **and** the VALD-11 gate passing), Phase 10 (extended grid), Phase 11 (IA broadening for the sub-eV part).
**Requirements:** CALC-18.
**Contract Coverage:**
- Advances: CALC-18 (Ge neutron NR dR/dE_rec from φ_post).
- Deliverables: Ge neutron NR dR/dE_rec, both designs, on the extended grid, unified phonon scale; the sub-5 eV kernel disposition (NCrystal splice or documented truncation); the >20 MeV omission bound at the VNS.
- Anchor coverage: **Phase 7 frozen ENDF/B-VIII.0 + Lib80x n-Ge elastic set** (23,155-point union grid, 293.6 K free-gas, thermal→20 MeV), natural resonance peak **669.1 b at 102.6 eV**, Σ = 0.1646 cm⁻¹, λ = 6.076 cm, P_int(2 mm) = 3.24%, **T_max/E_n = 0.0536** (vs W's 0.0215, a ~2.5× wider spread); NCrystal `Ge_sg227` bound-atom kernel below 5 eV; φ_post from Phase 9.
- Forbidden proxies: **`fp-mass-scaled-target`** — scaling NUCLEUS's CaWO₄/Al₂O₃ residuals to Ge by mass is the exact shortcut this milestone exists to avoid; the free-gas 1/v upturn to 20.6 b used as physics below 5 eV; extrapolating σ_el above the 20 MeV ENDF ceiling; a log-substituted quadrature not anchored at E_min(T), which silently loses the 1/E² endpoint spike.
**Success Criteria** (what must be TRUE):

1. Ge neutron NR dR/dE_rec is produced for both designs from φ_post ⊗ the frozen Ge elastic kernel, with the resonance-resolved grid preserved, on the unified phonon scale with no quenching, and count conservation ≤1e-3 through the fold and the response chain.
2. **Resonance imprint is present:** the natural-Ge 669.1 b peak at 102.6 eV produces visible structure in the recoil spectrum below 5.5 eV (T_max/E_n = 0.0536). A smooth sub-10 eV neutron NR spectrum is a bug, not a result, and is unit-tested as such.
3. The sub-5 eV kernel is handled explicitly: either the NCrystal `Ge_sg227` bound-atom cross section is spliced at 5 eV with the discontinuity measured and reported, **or** the channel is truncated at the last defended energy with the omission documented (Phase-7 gap-D1 precedent). The ENDF free-atom σ_el is never used as physics below 5 eV.
4. The 20 MeV ENDF ceiling is carried forward as an explicit, quantified omission — the TENDL splice (CALC-24) is follow-up scope — and its impact is bounded at the VNS, where the building plus shield cut the >10 MeV flux by ~5–7× relative to v1.1's surface premise.
5. The Ge number derives **only** from φ_post ⊗ Ge kernel, licensed by the Phase-9 VALD-11 pass; no CaWO₄/Al₂O₃ residual is rescaled to Ge anywhere in the call graph, and this is asserted by an explicit provenance check on the result.

**Plans:** TBD (run `gpd:plan-phase 13` to break down)

### Phase 14: Ge-Only Thermal-Capture Channels (P-GEONLY)

**Goal:** The backgrounds that NUCLEUS's published budget structurally cannot contain — because CaWO₄ and Al₂O₃ are blind to them — are either quantified or honestly bounded: prompt (n,γ) cascade recoils and the ⁷¹Ge electron-capture lines, which land directly inside the CEvNS RoI.
**Depends on:** Phase 13 (the neutron chain and φ_post; the capture channel is the same fluence through a different reaction).
**Requirements:** CALC-23.
**Contract Coverage:**
- Advances: CALC-23 (Ge-only thermal-capture channel).
- Deliverables: frozen ENDF MT=102 for the five Ge isotopes plus EGAF capture-γ line lists (new acquisition — Phase 7 obtained elastic only); prompt (n,γ) cascade recoil spectrum or bound; ⁷¹Ge EC line inventory; an explicit φ_th determination-or-gap statement carried into Phase 16.
- Anchor coverage: Biffl et al. PRD 107, 092011 (capture recoils "strongly overlap the CEvNS signal for recoils ≲ 100 eV"; Φ_th < 7×10⁻⁴ n/cm²·s requirement as context); ⁷¹Ge EC lines M **158.7 ± 1.4 eV** / L 1298.5 eV / K 10368.3 eV (CONUS+ sub-keV calibration); natural Ge σ_th ≈ 2.2 b, ⁷³Ge ≈ 15 b; NCrystal for the sub-5 eV neutron kernel (no Ge thermal scattering law exists in ENDF/B-VIII.0).
- Forbidden proxies: **reporting the capture channel as zero when φ_th is simply unobtained**; treating the single-γ recoil limit as the cascade answer; inheriting NUCLEUS's "harmless" verdict on the B₄C ¹⁰B(n,α)⁷Li 478 keV γ line, which is an **L2 statement** — harmless *because their COV vetoes it*, which we have shown (Phase 8) we cannot do.
**Success Criteria** (what must be TRUE):

1. ENDF MT=102 for all five Ge isotopes and the EGAF capture-γ line lists are acquired and frozen as provenance-headed artifacts, on the Phase-7 acquisition pattern.
2. The prompt (n,γ) cascade recoil spectrum is computed with an isotropic-cascade bound as the internal consistency check that substitutes for the absent external validation (single-γ kinematic limit 473 eV at 8 MeV; tens of eV for a realistic multi-γ cascade, since Σ E_γ²/2Mc² is not Σ(E_γ)²/2Mc²).
3. The ⁷¹Ge EC line inventory reproduces the M / L / K lines at **158.7 ± 1.4 / 1298.5 / 10368.3 eV**, with the M-shell line landing inside the RoI and folded through the response chain.
4. **φ_th disposition is explicit:** a documented attempt is made to obtain the in-shield thermal flux (NUCLEUS does not publish it, and the deposit-spectrum inversion cannot recover it since CaWO₄/Al₂O₃ are blind to it). If it cannot be obtained, the channel is reported as a **quantified gap** with a bounding statement against the Biffl requirement — **never as zero** — and that gap is carried as an explicit named addend into the Phase-16 assembly.
5. The adjacent capture-induced γ channels are at least bounded and named rather than silently omitted: Ge inelastic (⁷⁴Ge 596 keV, ⁷²Ge 834 keV) and the B₄C 478 keV line, which we would inherit **unvetoed**. *(Coverage note: no CALC ID owns these; they are carried here as adjacent-scope deliverables because they are the same fluence-through-a-different-reaction physics.)*

**Plans:** TBD (run `gpd:plan-phase 14` to break down)

### Phase 15: Gamma and Muon Re-Fold at the VNS (P-EM)

**Goal:** The two channels that v1.0 already solved are re-driven from the VNS environment rather than the surface — the measured gamma ambience replaces a representative literature band, and 2.92 m.w.e. of overburden replaces no overburden — with the underlying validated machinery left untouched so that any change is attributable to the relocation alone.
**Depends on:** Phase 9 (Table 2 ambience, Table 4 uncertainties, passive attenuation), Phase 10 (extended grid). Runs in parallel with Phases 11–13.
**Requirements:** CALC-19, CALC-20.
**Contract Coverage:**
- Advances: CALC-19 (Compton ER at the measured VNS ambience), CALC-20 (muon deposits at the VNS overburden).
- Deliverables: Compton electron-recoil dR/dE_rec and muon deposit dR/dE_rec, both designs, on the extended grid from 100 meV.
- Anchor coverage: NUCLEUS Table 2 gamma ambience (**5.03 cm⁻²s⁻¹**, 20% unc.; ⁴⁰K 59.6, ²³²Th 3.28, ²³⁸U 5.65 Bq/kg) and their stated "**factor ~50**" passive gamma reduction; overburden **2.92 ± 0.01 m.w.e.**, omnidirectional attenuation **1.41 ± 0.02** (25% muon unc.); NUCLEUS Table 5 muon entry (< 14 mcpd); v1.0 Klein–Nishina machinery with validated edges 1243 / 1541 / 2382 keV; v1.0 Gaisser–Guan ⊗ chord ⊗ Landau–Vavilov chain (1.366 Hz sea level, within ~20% of PDG); Heusser 1995 retained only as a site-to-site sanity band.
- Forbidden proxies: retaining the v1.0 sea-level muon flux or the Heusser gamma normalization after relocation; bare e^(−μx) gamma attenuation without buildup (under-predicts by factors of several); `fp-full-absorption` — full-energy photopeaks instead of the Compton continuum in a 2 mm wafer; inheriting the MV+COV > 99.8% muon rejection (an L2 factor).
**Success Criteria** (what must be TRUE):

1. The Compton ER spectrum is recomputed from the **measured** VNS ambience with the v1.0 Klein–Nishina machinery unchanged; the Heusser-1995 factor-2 band is retired as the absolute normalization and retained only as a site-to-site sanity check. The v1.0-validated Compton edges reproduce at 1243 / 1541 / 2382 keV (machinery-reuse invariant).
2. Passive gamma attenuation uses point-kernel + buildup (ANS-6.4.3 class, 10–30% documented accuracy) and reproduces NUCLEUS's stated "factor ~50" passive reduction within that accuracy; a bare exponential is shown to be insufficient rather than assumed adequate.
3. The muon deposit spectrum is recomputed at 2.92 ± 0.01 m.w.e. by applying the scalar omnidirectional attenuation 1.41 ± 0.02 to an otherwise byte-identical v1.0 Gaisser–Guan ⊗ chord ⊗ Landau–Vavilov chain; the v1.0 sea-level normalization appears nowhere in the v2.0 call graph.
4. Both channels land on the extended grid from 100 meV, fold through the regenerated `R(E_rec|E_dep)` for both designs with count conservation ≤1e-3, and preserve the v1.0 saturation behaviour (MeV muon deposits still compress onto the instrumental pile-up feature, not a physical line).
5. The muon result is compared against NUCLEUS's Table 5 muon entry (< 14 mcpd) using **L1 credit only** — the > 99.8% MV+COV rejection is not inherited, and the resulting discrepancy is reported as an expected consequence of the Phase-8 L2-off baseline rather than as a modelling failure.

**Plans:** TBD (run `gpd:plan-phase 15` to break down)

### Phase 16: S/B_particle Assembly, LEE Overlay, and the CONUS+ Gate (P-SB)

**Goal:** The milestone's headline number exists and is defensible: `S/B_particle` for a QPD Ge wafer at the VNS, reported with zero inherited veto credit alongside any credited number, with the low-energy excess carried as a band rather than buried, and only after the machinery has reproduced the one measured Ge-at-a-reactor S/B that exists.
**Depends on:** Phase 12 (signal), Phase 13 (neutrons), Phase 14 (capture channel or its quantified gap), Phase 15 (gammas and muons). **Terminal phase.**
**Requirements:** CALC-21, CALC-22, VALD-12.
**Contract Coverage:**
- Advances: VALD-12 (CONUS+ limiting-case reproduction — hard gate), CALC-22 (terminal S/B_particle with mandatory L2-off baseline), CALC-21 (LEE overlay band and the break-even amplitude).
- Deliverables: CONUS+ reproduction report; S/B_particle in the 10–100 eV RoI and below, both designs, reported **twice** (L2 = 1 and argued L2); min/max systematics band; the (A, α) LEE overlay and the **LEE amplitude at which S/B_particle = 1**; the four-state duty-cycle statement for the two-core site.
- Anchor coverage: **CONUS+ Nature 643, 1229 (2025)** — S/B ≈ 0.03 in 0.4–1 keV_ee at 7.4 m.w.e., 395 ± 106 observed vs SM 347 ± 59 in 327 kg·d, 3.7σ; NUCLEUS CaWO₄ **S/B ≈ 1.2** and Al₂O₃ **≈ 0.13** benchmarks and their published band **[0.9–1.5] at 68% CL**; Table 4 systematics (μ 25%, n 30%, γ 20%, materials 30%); Romani JAP 136, 124502 (Al-film area scaling, meV–eV phonons); Chang et al. APL 127, 263502 (bulk-volume scaling); NUCLEUS arXiv:2603.07687 LEE time law R(t) = A(t−t₀)^(−k), k = 0.59 ± 0.06; EDELWEISS RED20 Ge amplitude anchors (10⁵ / 10⁴ dru at 200 eV / 1 keV above ground, ÷3 underground).
- Forbidden proxies: **`fp-lee-omission`** (S/B without the LEE band); **`fp-veto-credit-transfer`** (no L2-off baseline); folding the LEE through `R(E_rec|E_dep)` — it is measured in reconstructed energy; quoting a bare "S/B" without the `_particle` qualifier; quoting a Ge band tighter than the CaWO₄ band it is anchored to; claiming 0.65–1.2 before VALD-12 passes.
**Success Criteria** (what must be TRUE):

1. **VALD-12 hard gate (must pass before any headline is claimed):** rescaling the pipeline to 3.6 GW_th / 20.7 m / 7.4 m.w.e. and a 0.4–1 keV_ee analysis window reproduces CONUS+'s measured **S/B ≈ 0.03** within a factor ~2. Until it does, no headline S/B is reported — our predicted 0.65–1.2 is more than an order of magnitude better than the only measured Ge-at-a-reactor value in existence, and that claim is unvalidated without this.
2. **CALC-22:** `S/B_particle` is assembled in the 10–100 eV RoI and below, for both designs, with the trigger curve applied, and reported **twice**: an **L2-off baseline carrying zero inherited veto credit** (the honest lower bound, mandatory) alongside any veto-credited number with its argument stated. The observable is named `S/B_particle` everywhere — never bare "S/B" — and is compared against NUCLEUS's CaWO₄ 1.2 and Al₂O₃ 0.13 benchmarks.
3. Systematics are propagated min/max as NUCLEUS does (μ 25%, n 30%, γ 20%, materials 30%); the same machinery applied to CaWO₄ reproduces their published **[0.9–1.5] at 68% CL**; and the Ge band is never quoted tighter than that. The VNS absolute neutron flux has never been measured and neutrons are ~91% of the RoI budget, so the 30% neutron term does not shrink under any treatment.
4. **CALC-21:** the LEE is carried as an explicitly parameterized `dR/dE_LEE = A(E/E₀)^(−α)` **overlay band on the E_rec axis** — never folded through the response matrix, never folded into a headline number. Both contradictory scalings are carried as the band (Romani Al-film **area** with ~10,300 films and surface-to-mass ~1950 cm²/kg vs ~955 for a 6.8 g CaWO₄ crystal; Chang bulk **volume** with a ×120 mass extrapolation), and neither is claimed as a prediction.
5. **CALC-21 decisive deliverable:** the **LEE amplitude at which S/B_particle = 1** (the erasure/break-even amplitude) is reported as the falsifiable, computable number that replaces an undefendable predicted LEE rate. "Particle backgrounds only; LEE not modelled in the headline" is annotated on every deliverable figure, and the four-state duty-cycle model is stated for the two-core site (genuine both-off periods are rare, so ON/OFF is not clean).

**Plans:** TBD (run `gpd:plan-phase 16` to break down)

## Phase Dependencies

| Phase | Depends On | Enables | Critical Path? |
|-------|-----------|---------|:-:|
| 8 – Veto-Envelope Geometry Gate (P-VETO) | — (v1.0/Phase-7 outputs) | 9, 10 (and, as a stop-condition, everything) | Yes |
| 9 – VNS Environment Lock & Fluence Recovery (P-ENV) | 8 | 12, 13, 15 | No (parallel with 10) |
| 10 – Sub-eV Grid & Trigger Observable (P-GRID) | 8 | 11, 13, 15 | Yes |
| 11 – Phonon Conventions & IA Broadening (P-CONV) | 10 | 12, 13 | Yes |
| 12 – CEvNS at the VNS to 100 meV (P-SIG) | 9, 11 | 16 | No (parallel with 13) |
| 13 – Ge Neutron Re-Fold (P-TGT) | 9, 10, 11 | 14, 16 | Yes |
| 14 – Ge-Only Capture Channels (P-GEONLY) | 13 | 16 | Yes |
| 15 – Gamma & Muon Re-Fold (P-EM) | 9, 10 | 16 | No (parallel with 11–14) |
| 16 – S/B Assembly, LEE, CONUS+ Gate (P-SB) | 12, 13, 14, 15 | — | Yes |

**Critical path:** 8 → 10 → 11 → 13 → 14 → 16 (6 sequential phases).

**Wave schedule (for `gpd:execute-phase`):**
- Wave 1: **8** (sole entry point; gating stop-condition — nothing else is scheduled until it closes)
- Wave 2: **9, 10** (parallel)
- Wave 3: **11, 15** (parallel)
- Wave 4: **12, 13** (parallel)
- Wave 5: **14**
- Wave 6: **16**

*Note on the Phase-8 gate:* Phase 10's grid work is nominally site-independent and could technically start before the gate closes, but it is **not** scheduled ahead of it. A failed gate triggers a milestone re-scope, and re-scoped work should not be built on top of a premise under review.

## Risk Register

| Phase | Top Risk | Probability | Impact | Mitigation |
|-------|---------|:-:|:-:|-----------|
| 8 | **Milestone stop-condition:** the 110 g wafer (103 cm², ~11× NUCLEUS's ~9 cm² footprint, monolithic, no multiplicity handle) does not fit the COV/IV envelope. A forced shield/veto redesign means φ_post at the detector position is no longer NUCLEUS's φ_post and **essentially nothing transfers** | MEDIUM | **CRITICAL** | **STOP and re-scope with the user** (explicit user decision 2026-07-22). Do NOT continue with a reduced veto credit; do NOT invent a resized veto. Gate is first, cheap, and blocking |
| 9 | **Pre-vs-post-veto ambiguity in NUCLEUS Figs. 8–11** determines whether the inverted quantity is a fluence or a veto-weighted fluence. If post-veto, the recovered φ transfers only under the same veto acceptance — which Phase 8 has shown we do not have | HIGH | HIGH | Resolve from captions/text before inverting; label the recovered object accordingly; if post-veto and irreducible, state the transfer condition explicitly and widen the band. Fallback (SIMU-05, hand-rolled 1-D multigroup) is follow-up scope — **no OpenMC** |
| 9 | The two-target over-determination fails: CaWO₄- and Al₂O₃-derived φ_post disagree by more than a factor 1.5, or VALD-11 cannot reproduce both 1.81 and 1.20 from one normalization | MEDIUM | HIGH | VALD-11 is a hard gate on Phase 13. If it fails, the transfer machinery has lost the kinematic-compression physics — backtrack to the kernel before touching Ge |
| 10 | A kinematic threshold falls below a tabulated floor and the interpolator returns zero rather than raising, silently zeroing a channel two decades below the validated range | MEDIUM | HIGH | Every interpolator raises outside its evaluated range; unit tests at each table's actual floor; the flat-plateau assertion in Phase 12 catches survivors |
| 11 | ω̄ is mis-pinned: the ⟨u²⟩-derived 12–21 meV and the 37 meV optical value differ 2–3×, and **both 2W and σ_E scale linearly with it**, so the threshold smearing moves by ~√3 | MEDIUM | HIGH | CALC-14 as its own first plan, pinned from the real Ge VDOS (not Debye) in CONVENTIONS.md, cross-checked NCrystal vs DarkELF, with the 1-D/3-D factor-3 convention locked at the same time |
| 12 | Sub-eV extrapolation artifacts masquerade as physics (rising dR/dT) or silently truncate (falling to zero) | LOW | HIGH | VALD-10 flat-plateau assertion + <1% v1.0 regression above 10 eV, both as unit tests rather than inspection |
| 13 | Free-gas σ_el used as physics below 5 eV (spurious 1/v rise to 20.6 b); or the 102.6 eV resonance smeared out, losing the sub-5.5 eV structure | MEDIUM | MEDIUM | NCrystal `Ge_sg227` splice at 5 eV with the discontinuity reported, **or** documented truncation on the Phase-7 gap-D1 precedent. Resonance-imprint unit test |
| 14 | **φ_th is unobtainable:** the in-shield thermal flux is not published by NUCLEUS, is not recoverable by inversion (CaWO₄/Al₂O₃ are blind to capture), and the only route left is transport we have rejected | HIGH | MEDIUM | **Report a quantified gap, never zero.** Bound against the Biffl Φ_th < 7×10⁻⁴ n/cm²·s requirement; carry the gap as a named addend into Phase 16; the isotropic-cascade bound substitutes for the absent external cross-check |
| 15 | Bare e^(−μx) gamma attenuation without buildup under-predicts by factors of several; or the v1.0 sea-level muon normalization survives the relocation | LOW | MEDIUM | Point-kernel + buildup validated against NUCLEUS's "factor ~50"; call-graph audit that no sea-level/Heusser normalization remains |
| 16 | **The LEE is design-dependent for a QPD specifically** — Romani models it as Al-film dislocation relaxation scaling with **film area**, and this wafer carries ~10,300 films emitting meV–eV phonons. It is therefore **neither inheritable from NUCLEUS nor shieldable**, and it is plausibly dominant below ~100 eV. Worse, the LEE mechanism and the QPD signal mechanism are the same phenomenon (quasiparticle poisoning) | HIGH | **HIGH** | Never a single number: carry an (A, α) band spanning **both** contradictory scalings (Romani area vs Chang volume, neither extrapolation defensible) and report the **break-even amplitude at S/B_particle = 1** as the falsifiable deliverable. Annotate every figure. Never fold the LEE through the response matrix |
| 16 | **Our predicted S/B 0.65–1.2 is > 1 order of magnitude better than the only measured Ge-at-a-reactor value** (CONUS+ ≈ 0.03). It may be right — 10³× lower threshold, more overburden, no quenching — but it is the kind of result that is usually an error | MEDIUM | **HIGH** | VALD-12 is a hard gate: reproduce CONUS+ within a factor ~2 before any headline. Report L2-off alongside L2-credited. Reproduce NUCLEUS's own [0.9–1.5] band on CaWO₄ with our machinery; never quote tighter than the source |

## Backtracking Triggers

- **Phase 8 (milestone-level):** If the wafer does not fit the COV/IV envelope, **STOP the milestone and re-scope with the user.** Do not proceed with a reduced veto credit and do not invent a resized veto. Nothing downstream is valid until this closes.
- **Phase 9:** If Figs. 8–11 turn out to be post-veto and the veto acceptance cannot be undone, revisit the Phase-8 L1/L2 split before inverting — the recovered object is then a veto-weighted fluence and transfers only under conditions we do not meet. If the CaWO₄/Al₂O₃ φ_post solutions disagree by > factor 1.5, or the recovered φ goes negative, the inversion is outside its s-wave validity regime (E_n ≳ 0.5–1 MeV forward-peaking) — revisit the kernel, do not regularize harder until the answer looks nice.
- **Phase 9 → 13 gate:** If **VALD-11** cannot reproduce both 1.81 (10–100 eV) and 1.20 (0.1–1 keV) from a single normalization, **do not start Phase 13.** A band-independent ratio means the kinematic-compression physics is missing and no Ge neutron number can be trusted.
- **Phase 10:** If the regenerated `R(E_rec|E_dep)` breaks count conservation (>1e-3) or any of the 24 v1.0/v1.1 anchors stops reproducing, revisit the grid extension before any spectrum is produced on it.
- **Phase 11:** If ω̄ cannot be pinned to a single defended value from the Ge VDOS, **block and request scope repair** — do not carry a 2–3× range into a quantity that both 2W and σ_E depend on linearly. If the broadened spectrum does not reproduce frozen v1.0 above 10 eV to <1%, the convolution is being applied in the wrong place in the chain.
- **Phase 12:** If dR/dT is not flat from 100 meV to 10 eV, diagnose before proceeding: a rising spectrum is an extrapolation artifact, a falling one is a table floor. Either way it is a bug, not a discovery.
- **Phase 13:** If the sub-10 eV neutron NR spectrum is smooth (no 102.6 eV resonance imprint below 5.5 eV recoil), the resonance grid has been lost — revisit the fold before the result enters the budget.
- **Phase 14:** If φ_th cannot be obtained, do **not** report zero and do **not** build a transport model to get it (SIMU-05 is follow-up scope, and OpenMC is unbuildable here). Report a quantified gap with a bound and carry it forward as a named addend.
- **Phase 16:** If **VALD-12** (CONUS+ ≈ 0.03 within a factor ~2) does not reproduce, **no headline S/B may be claimed.** Treat the failure as evidence about our own machinery, not about CONUS+. If the assembled S/B_particle band comes out tighter than NUCLEUS's [0.9–1.5], the systematics have been dropped — re-propagate before reporting.

## Progress

**Execution Order:** Phases execute in numeric order 8 → 9 → 10 → 11 → 12 → 13 → 14 → 15 → 16, with the wave schedule above enabling 9∥10, 11∥15, and 12∥13 once Phase 8 closes.

| Phase | Milestone | Plans Complete | Status | Completed |
| ----- | --------- | -------------- | ------ | --------- |
| 7. Scenario & Nuclear-Data Lock | v1.1 (carried forward) | 2/2 | Complete | 2026-07-22 |
| 8. Veto-Envelope Geometry Gate (P-VETO) | v2.0 | 0/TBD | Not started | - |
| 9. VNS Environment Lock & Fluence Recovery (P-ENV) | v2.0 | 0/TBD | Not started | - |
| 10. Sub-eV Grid & Trigger Observable (P-GRID) | v2.0 | 0/TBD | Not started | - |
| 11. Phonon Conventions & IA Broadening (P-CONV) | v2.0 | 0/TBD | Not started | - |
| 12. CEvNS at the VNS to 100 meV (P-SIG) | v2.0 | 0/TBD | Not started | - |
| 13. Ge Neutron Re-Fold (P-TGT) | v2.0 | 0/TBD | Not started | - |
| 14. Ge-Only Capture Channels (P-GEONLY) | v2.0 | 0/TBD | Not started | - |
| 15. Gamma & Muon Re-Fold (P-EM) | v2.0 | 0/TBD | Not started | - |
| 16. S/B Assembly, LEE, CONUS+ Gate (P-SB) | v2.0 | 0/TBD | Not started | - |

## Notes

**Phase numbering.** v1.0 = Phases 1–6 (shipped). v1.1 = Phases 7–12 planned, but only Phase 7 executed; Phases 8–12 were withdrawn, so v2.0 **reuses** those numbers starting at 8. Phase 7's frozen ENDF/B-VIII.0 n-Ge elastic table and T_max/E_n = 0.0536 kinematics are carried forward into v2.0.

**Coverage.** All 17 v2.0 primary requirements (CALC-11 … CALC-23, VALD-09 … VALD-12) map to exactly one primary phase each. Follow-up items — CALC-24 (TENDL splice), SIMU-05 (hand-rolled 1-D transport fallback), RADX-01 (QPD-film/surface radioactivity), MANU-01, SENS-01 — are deliberately **not** given phases; they are tracked in REQUIREMENTS.md.

**Tooling constraints.** No phase carries an OpenMC, MCNP, Geant4, or G4CMP dependency. OpenMC is unbuildable on osx-arm64 (established in v1.1, re-confirmed by the v2.0 computational scout); METHODS.md's OpenMC shield-transport recommendation was **overruled in synthesis**. Full Geant4 transport of the NUCLEUS geometry is out of scope by explicit user decision (their own p. 21 reports "tens, even hundreds, millions of hours of computing time"). Any transport fallback is SIMU-05, follow-up scope. The required stack is Python + numpy/scipy/matplotlib + NCrystal 4.4.6 (native osx-arm64 wheel) + the existing ENDF/ACE reader; every NUCLEUS input is a **digitization**, not a download (no NUCLEUS, CONUS/CONUS+, or RICOCHET arXiv record carries ancillary data).

**Retracted rules.** The standing "never display QPD spectra below 10 eV" rule is **withdrawn** (user, 2026-07-22). What survives is a labelled regime boundary, not a plotting ban: below ~1 eV deposit the reported observable is a trigger-probability curve, not dR/dE_rec.

**Conventions.** CONVENTIONS.md already exists from v1.0; the notation-coordinator handoff is skipped for this continuation. Phase 11 (CALC-14) **amends** it with ω̄ and the Debye–Waller convention, and that amendment gates every sub-eV spectrum in the milestone.

**Open coverage note.** No CALC requirement explicitly owns "produce the CEvNS dR/dE_rec at the VNS normalization" — the milestone's decisive signal deliverable. It is implied jointly by CALC-15, CALC-16, CALC-17 and VALD-10 and consumed by CALC-22. It is carried here as a Phase-12 deliverable rather than a new requirement ID; if the orchestrator prefers an explicit ID, add it to REQUIREMENTS.md and re-map to Phase 12.
