# Requirements: QPD Particle-Physics Potential — v2.0 QPD at the NUCLEUS Chooz Very-Near-Site

**Defined:** 2026-07-22
**Core Research Question:** What are the reactor-CEvNS signal and the full in-band particle-background budget, in reconstructed energy down to 100 meV, for a ~110 g QPD Ge wafer deployed at the NUCLEUS Chooz Very-Near-Site behind the NUCLEUS shielding — and what signal-to-background does that give?

> **Milestone scope note.** v2.0 replaces v1.1's premise. Instead of projecting backgrounds from *surface, unshielded* ambient fluxes at a generic 3 GW_th / 25 m site, the detector is assumed to sit at the Chooz VNS behind the NUCLEUS shielding, and that experiment's **measured environment and shielding attenuation are adopted as input** while the **target response is re-folded for Ge**. Scaling their CaWO₄/Al₂O₃ residuals by a mass argument is forbidden (it discards the target dependence their own paper emphasizes); full Geant4 transport is out of scope (their p. 21 reports "tens, even hundreds, millions of hours of computing time" and states variance reduction will be required).
>
> Locked scenario change (CONVENTIONS §D): 2 × 4.25 GW_th at 72 m and 102 m, ∫Φ = 2.1×10¹² ν̄/cm²/s, 80% duty, overburden 2.92 m.w.e. — replacing 3 GW_th / 25 m / 7.5×10¹². Signal drops ~3.6×.
>
> All spectra extend to **100 meV**, two decades below the v1.0 10.14 eV grid floor. The earlier "never display below 10 eV" rule is **retracted** (user, 2026-07-22). Below ~1 eV deposit the reported observable is a **trigger-probability curve**, not dR/dE_rec.
>
> IDs continue from v1.1 (last used: CALC-10, SIMU-04, VALD-08). Phase 7 of v1.1 is **carried forward**; Phases 8–12 are **withdrawn**.

## Primary Requirements

### Calculations

**A. Environment adoption and fluence recovery**

- [ ] **CALC-11**: Digitize and freeze the NUCLEUS VNS inputs as provenance-headed artifacts: the Fig. 4 VNS-room neutron spectrum (plotted as E·dΦ/dE on a log-E axis), Table 2 gamma ambience (5.03 cm⁻²s⁻¹; ⁴⁰K 59.6, ²³²Th 3.28, ²³⁸U 5.65 Bq/kg), Table 3 material screening (12 components), Table 4 normalizations and uncertainties (μ 25%, n 30%, γ 20%, materials 30%), and Table 5 residual benchmarks. Lethargy-vs-per-energy and integral-conserving rebinning must be explicit acceptance tests, not assumptions.
- [ ] **CALC-12**: Recover the post-shield neutron fluence φ_post(E_n) at the target position by inverting NUCLEUS's published component-resolved CaWO₄ and Al₂O₃ deposit spectra through the flat-box recoil kernel. Two published targets over-determine the inversion, giving a built-in consistency test. Differentiating digitized data requires regularized differentiation, not finite differences. Must first establish whether their Figs. 8–11 are pre- or post-veto.

**B. Sub-eV extension**

- [ ] **CALC-13**: Extend `shared_energy_grid()` from 10.14 eV down to 0.1 eV (~744 bins at 80/decade) and regenerate the `R(E_rec|E_dep)` matrices for both designs on the extended grid. Every archived v1.x spectrum must be re-gridded or explicitly tagged valid-only-above-10.14 eV.
- [ ] **CALC-14**: Fix ω̄ and the Debye–Waller convention in `CONVENTIONS.md` **before** any sub-eV spectrum is produced. The ⟨u²⟩-derived 12–21 meV and the 37 meV optical-phonon energy differ by 2–3× and both 2W and σ_E scale linearly with it; the 2W = q²⟨u_x²⟩ vs q²⟨u²⟩/3 convention must be pinned at the same time.
- [ ] **CALC-15**: Implement impulse-approximation quantum broadening — free-nucleus recoil convolved with a Gaussian of width σ_E = √(E_R·ω̄), applied **before** the response chain. Fractional width ≈ 35–46% at 100 meV, 15.5–20.5% at 0.5 eV, 11–15% at 1 eV, negligible above ~100 eV. This is the largest new physics input and is absent from the v1.0 model.
- [ ] **CALC-16**: Implement the analysis trigger-probability curve: a sigmoid efficiency with its **50% point at 0.5 eV**, multiplied on top of *all* other efficiencies including the existing ε ≈ 0.5 deposited-to-signal collection efficiency (it does not replace it). Below ~1 eV deposit this curve, not dR/dE_rec, is the reported observable.
- [ ] **CALC-17**: Evaluate and report the sub-100 keV flux truncation bound with the project's own Φ. Established: ≤ 0.81% at T = 100 meV, exactly zero above 0.29 eV, under a conservative flat continuation of Φ at its 100 keV value including the (1 − MT/2E²) factor. **Report the bound; do not extend the flux table.**

**C. Ge target re-fold**

- [ ] **CALC-18**: Re-fold the Ge nuclear-recoil background from the recovered φ_post(E_n) through the carried-forward frozen ENDF/B-VIII.0 n-Ge elastic set, on the unified phonon scale, both designs, to reconstructed energy.
- [ ] **CALC-23**: Compute the Ge-only thermal-capture channel that CaWO₄/Al₂O₃ are blind to — prompt (n,γ) cascade recoils and the ⁷¹Ge EC M-shell line at ~159 eV. Requires ENDF MT=102 for the five Ge isotopes plus EGAF capture-γ line lists (new acquisition; Phase 7 obtained elastic only). Sub-5 eV neutron kernel needs NCrystal, since no Ge thermal scattering law exists in ENDF/B-VIII.0. **Gated on the in-shield thermal flux φ_th, which NUCLEUS does not publish — if φ_th cannot be obtained, report this as a quantified gap, never as zero.** *(Supersedes v1.1's deferred NCAP-01, now at the VNS behind moderating shield rather than unshielded at 25 m.)*

**D. Other channels at the VNS**

- [ ] **CALC-19**: Recompute the environmental-gamma Compton electron-recoil spectrum driven by the **measured** VNS ambience (Table 2), replacing the v1.0 Heusser-1995 factor-2 band. Reuses the v1.0 Klein–Nishina machinery unchanged.
- [ ] **CALC-20**: Recompute the muon deposit spectrum at the VNS overburden (2.92 ± 0.01 m.w.e., omnidirectional attenuation 1.41 ± 0.02), replacing the v1.0 sea-level/no-overburden assumption. Reuses the v1.0 Gaisser–Guan ⊗ chord ⊗ Landau–Vavilov machinery unchanged.

**E. LEE and signal-to-background**

- [ ] **CALC-21**: Carry the low-energy excess as an explicitly parameterized **overlay band**, never folded into a headline number. It is absent from the NUCLEUS particle-background budget by their own statement, and is **design-dependent for a QPD specifically** (Romani, J. Appl. Phys. 136, 124502: Al-film dislocation relaxation scaling with film area, predicting meV–eV phonons; a QPD wafer carries ~10,300 films), so it can be neither inherited nor shielded against. Time law available: R(t) = A(t−t₀)^(−k), k = 0.59 ± 0.06 (Al₂O₃) / 0.73 ± 0.08 (CaWO₄), NUCLEUS arXiv:2603.07687. Report the **LEE amplitude at which S/B = 1** as the falsifiable, computable deliverable. *(Promotes v1.1's deferred LEEX-01 into scope.)*
- [ ] **CALC-22**: Assemble **S/B_particle** in the 10–100 eV RoI and below, both designs, with the trigger curve applied — reported alongside an **L2-off baseline** (no inherited veto credit). Compare against NUCLEUS's CaWO₄ (S/B ≈ 1.2) and Al₂O₃ (≈ 0.13) benchmarks.

### Validations

- [ ] **VALD-09** *(GATING — milestone stop-condition)*: Determine whether a 4″×4″×2 mm, ~110 g Ge wafer physically fits the NUCLEUS COV/IV veto envelope, which is dimensioned for 6.8 g CaWO₄ and 4.5 g Al₂O₃ 3×3 arrays. The wafer has ~11× the footprint (103 vs ~9 cm²) and, being monolithic, has **no multiplicity handle at all**. Inherited veto credit defaults to **zero** unless earned. **If the wafer does not fit, STOP and re-scope with the user** (user decision 2026-07-22) — a forced shield/veto redesign means φ_post at the detector position is no longer NUCLEUS's φ_post and essentially nothing transfers. Must be resolved before the background chain is built on top of it.
- [ ] **VALD-10**: Sub-eV validity gates. The extended pipeline must reproduce the frozen v1.0 spectrum above ~10 eV to < 1% (no silent change to validated results), and dR/dT must be **flat** from 100 meV to 10 eV, equal to the analytic T→0 plateau from the frozen ∫Φ. Guards against kinematic thresholds silently falling below a tabulated floor and returning zero rather than erroring.
- [ ] **VALD-11**: Neutron target-scaling calibration. Reproduce **both** published CaWO₄/Al₂O₃ neutron rate ratios from a single normalization — 1.81 in 10–100 eV and 1.20 in 0.1–1 keV — before any Ge neutron number is trusted. The band-dependence is driven by 1/T_max compression; a crude flat-box estimate gives ≈1.1, i.e. ~60% low on a ratio where normalization cancels.
- [ ] **VALD-12** *(hard gate on any S/B claim)*: Reproduce CONUS+ as a limiting case — S/B ≈ 0.03 in 0.4–1 keV_ee at 7.4 m.w.e. (Nature 643, 1229 (2025): 395 ± 106 events in 327 kg·d against SM 347 ± 59, 3.7σ). This is the **only measured Ge-at-a-reactor S/B in existence**, and our predicted 0.65–1.2 is more than an order of magnitude better. No headline S/B may be claimed until this reproduces.

## Follow-up Requirements

Deferred by explicit user scoping decision (2026-07-22). Tracked, not in the v2.0 roadmap.

### Nuclear data

- **CALC-24**: Splice TENDL-2023 n-Ge elastic above the 20 MeV ENDF/B-VIII.0 ceiling to close v1.1's carried-forward gap D1 (+1.35% step at the seam — splice, do not substitute; TENDL below 20 MeV is a TALYS calculation that would discard the resonance-resolved frozen table). *Deferred rationale:* the building plus shield cut the >10 MeV flux by ~5–7×, so the omission now bounds the high-energy tail and total rate, not the in-band result.

### Transport

- **SIMU-05**: 1-D spherical-shell multigroup/S_N shield-transport solver on Lib80x group constants, as a fallback if the CALC-12 inversion fails or proves ambiguous. **Must be hand-rolled — OpenMC is unbuildable on osx-arm64** (established in v1.1; the roadmap must not carry an OpenMC dependency). *Deferred rationale:* only worth building if the inversion turns out to be the milestone's single point of failure.

### Extended backgrounds

- **RADX-01**: QPD-film / substrate / wafer-surface radioactivity (Ta/Al/Hf films, surface contamination) — still deferred. Note this now partially overlaps CALC-21, since the Romani mechanism makes the Al film area a *background source*, not merely a contaminant carrier.

### Manuscript / payoff

- **MANU-01**: Manuscript revision per the round-1 internal peer review (completeness scope caveat, ε vs η_ce distinction, citations, venue).
- **SENS-01**: Quantitative CEvNS discovery/exclusion sensitivity — enabled by the v2.0 background budget.

## Out of Scope

| Topic | Reason |
| ----- | ------ |
| Full Geant4 transport of the NUCLEUS geometry | Their own p. 21 reports "tens, even hundreds, millions of hours of computing time" and states variance-reduction techniques will be required; out of reach for a laptop-scale analytic pipeline. Explicit user decision. |
| Scaling NUCLEUS's CaWO₄/Al₂O₃ residuals to Ge by a mass argument | Discards the target dependence the paper itself emphasizes, and is exactly the shortcut this milestone exists to avoid. Explicit user decision. |
| Coherent-crystal S(q,ω) modelling backbone | The crystal-coherent regime lives below ~21 meV, under the 100 meV floor (q ≈ 53–140 Brillouin zones out at 100 meV; e^(−2W) ≈ 10⁻² at the floor, ~10⁻²⁰ at 1 eV — the channel is extinct). NCrystal/DarkELF retained only as a bounded one-off justification that the impulse limit applies, and NCrystal separately for the sub-5 eV *neutron* kernel. |
| OpenMC for any transport step | Unbuildable on osx-arm64 (established in v1.1). Any transport fallback must be hand-rolled — see SIMU-05. |
| G4CMP phonon-transport detector response | Deferred project-wide since v1.0. |
| Dark-matter sensitivity projections | Later milestone of this project. |
| Extending the reactor flux table below 100 keV | Truncation bound is ≤0.81% at the very bottom bin (CALC-17); reporting the bound is the deliverable. v1.0 was already extrapolating — Huber–Mueller is fitted only over 2–8 MeV. |
| Ionization quenching / Lindhard / keVee↔keVnr conversion | Unified phonon scale (CONVENTIONS §B). *Strengthened* in-window by the SuperCDMS Ge displacement threshold 19.7 ⁺⁰·⁶₋₀·₅ eV with no defect formation below ~6 eV (Appl. Phys. Lett. 113, 092101). |
| Detector geometry / sensor-layout optimization | Fixed 4″×4″×2 mm single-sided wafer from v1.0 — and note VALD-09 may show this geometry is incompatible with the adopted veto envelope, which is a stop-condition, not an optimization trigger. |

## Accuracy and Validation Criteria

| Requirement | Accuracy Target | Validation Method |
| ----------- | --------------- | ----------------- |
| CALC-11 | Digitization ~5% below the steep region; integral conserved to <1% on rebinning | Lethargy-convention and integral-conservation acceptance tests; the VALD-02 digitizer reproduced a published Ge curve to 5% |
| CALC-12 | CaWO₄- and Al₂O₃-derived φ_post agree within a factor ≲1.5 | Over-determination: two independent published targets must yield the same fluence |
| CALC-14/15 | ω̄ fixed to a stated convention; σ_E re-derived in-phase | Ge broadening numbers are DERIVED in-survey, not literature-quoted — must be re-derived before use |
| CALC-16 | Sigmoid 50% point exactly 0.5 eV; multiplies ε, does not replace it | Unit test on the composed efficiency chain |
| CALC-17 | Bound computed, not estimated | Flat-continuation integral with the (1 − MT/2E²) factor; established ≤0.81% |
| CALC-18 | Target-swap closure factor ≲1.5; break condition >2 | Reproduce NUCLEUS's own CaWO₄/Al₂O₃ residuals with our pipeline before swapping in the Ge kernel |
| CALC-22 | S/B reported with and without inherited veto credit | L2-off baseline mandatory alongside any L2-credited number |
| VALD-10 | <1% deviation from frozen v1.0 above 10 eV | Direct comparison against committed v1.0 CSVs |
| VALD-11 | Both ratios (1.81, 1.20) from one normalization | Two-band calibration against Table 5 |
| VALD-12 | CONUS+ S/B ≈ 0.03 reproduced within a factor ~2 | Rescale our pipeline to 3.6 GW_th / 20.7 m / 7.4 m.w.e. and compare |

## Contract Coverage

| Requirement | Decisive Output / Deliverable | Anchor / Benchmark | Prior Inputs / Baselines | False Progress To Reject |
| ----------- | ----------------------------- | ------------------ | ------------------------ | ------------------------ |
| CALC-11/12 | φ_post(E_n) artifact + digitized VNS input set | NUCLEUS EPJC 86, 29 (2026) Figs. 4, 8–11; Tables 2–5 | VALD-02 digitizer | `fp-nucleus-3e12`; lethargy/per-energy confusion; reading post-veto curves as pre-veto |
| CALC-13/14/15/16 | Sub-eV spectra + trigger-probability curve | Campbell-Deem PRD 106, 036019; Sears PRB 35, 2038 | v1.0 `R(E_rec\|E_dep)` | `fp-poisson-as-resolution`; applying e^(−2W) to the total rate (it suppresses only the zero-phonon channel) |
| CALC-18/23 | Ge neutron + capture dR/dE_rec | Frozen ENDF/B-VIII.0 n-Ge elastic; ENDF MT=102 + EGAF; NCrystal | Phase 7 (carried forward), T_max/E_n = 0.0536 | `fp-mass-scaled-target`; reporting the capture channel as zero when φ_th is simply unobtained |
| CALC-19/20 | Compton + muon dR/dE_rec at the VNS | NUCLEUS Table 2; overburden 2.92 m.w.e., attenuation 1.41 | v1.0 Klein–Nishina and Gaisser–Guan machinery | Retaining the v1.0 sea-level muon flux or the Heusser gamma normalization after relocation |
| CALC-21/22 | S/B_particle + LEE-erasure amplitude | NUCLEUS Table 5 @ **100% duty** (356.5, not the prose 280) | Our CaWO₄ closure fold (407.7, ratio 1.14) | `fp-veto-credit-transfer`; `fp-lee-omission`; `fp-nucleus-prose-280` (flatters S/B by 27%) |
| VALD-09 | Geometry-fit determination | NUCLEUS Fig. 1e/f envelope | Wafer 103 cm² vs ~9 cm² | Proceeding past a failed gate on a premise already known false |
| VALD-12 | CONUS+ limiting-case reproduction | Nature 643, 1229 (2025) | v1.0 CONUS+ rate-scale check (factor 0.99) | Claiming 0.65–1.2 S/B without reproducing the only measured value |

**Forbidden proxies (milestone-wide):** `fp-deposited-only`, `fp-no-saturation`, `fp-full-absorption`, keVee↔keVnr mixing / Lindhard quenching on the phonon scale, `fp-lumped-A`, `fp-gwe-gwth`, `fp-nucleus-3e12` (folding at the 2019 prose flux), **`fp-nucleus-prose-280`** (anchoring on the §2 prose CEvNS value instead of Table 5), **`fp-veto-credit-transfer`** (inheriting gram-scale veto rejection for a 110 g monolithic wafer), **`fp-lee-omission`** (reporting S/B without the LEE band), **`fp-mass-scaled-target`** (scaling CaWO₄/Al₂O₃ residuals to Ge by mass), **`fp-poisson-as-resolution`** (quoting the emergent counting floor as a resolution model).

## Traceability

| Requirement | Phase | Status |
| ----------- | ----- | ------ |
| *(filled by the roadmapper)* | | |
