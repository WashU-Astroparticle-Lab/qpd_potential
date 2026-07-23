# Requirements: QPD Particle-Physics Potential — v2.0 QPD at the NUCLEUS Chooz Very-Near-Site

**Defined:** 2026-07-22
**Core Research Question:** What are the reactor-CEvNS signal and the full in-band particle-background budget, in reconstructed energy down to 100 meV, for a ~110 g QPD Ge wafer deployed at the NUCLEUS Chooz Very-Near-Site behind the NUCLEUS shielding — and what signal-to-background does that give?

> **Milestone scope note.** v2.0 replaces v1.1's premise. Instead of projecting backgrounds from *surface, unshielded* ambient fluxes at a generic 3 GW_th / 25 m site, the detector is assumed to sit at the Chooz VNS behind the NUCLEUS shielding, and that experiment's **measured environment and shielding attenuation are adopted as input** while the **target response is re-folded for Ge**. Scaling their CaWO₄/Al₂O₃ residuals by a mass argument is forbidden (it discards the target dependence their own paper emphasizes); full Geant4 transport is out of scope (their p. 21 reports "tens, even hundreds, millions of hours of computing time" and states variance reduction will be required).
>
> ~~Locked scenario change (CONVENTIONS §D): 2 × 4.25 GW_th at 72 m and 102 m, ∫Φ = 2.1×10¹² ν̄/cm²/s, 80% duty, overburden 2.92 m.w.e. — replacing 3 GW_th / 25 m / 7.5×10¹². Signal drops ~3.6×.~~
>
> **CORRECTED 2026-07-22 — this lock was never applied.** `CONVENTIONS.md` §D still reads **3 GW_th / 25 m**, and there is **no VNS flux table** in `data/flux/` (only `reactor_flux_v1.0.csv` at 3 GW_th / 25 m, ∫Φ = 7.5×10¹², and `reactor_flux_billard_variant.csv`). Under the 2026-07-22 re-scope this is the right answer rather than a gap to close: **the paper's 3 GW_th / 25 m surface scenario is the milestone's primary normalization**, used unmodified, and §D stands as written. The NUCLEUS VNS siting is an **optional secondary line only** — a labelled scalar rescale of the primary result by 2.1×10¹² / 7.5×10¹² ≈ **0.28** — not a separate pipeline run and not a locked scenario. The overburden 2.92 m.w.e. is **not** applied anywhere: the configuration is an unshielded surface wafer.
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
- [ ] **CALC-25** *(the milestone's decisive signal deliverable; **text needs re-wording after the 2026-07-22 re-scope** — the primary normalization is now the paper's ∫Φ = 7.5×10¹² ν̄/cm²/s at 3 GW_th / 25 m surface, taken unmodified from the frozen table, and the VNS enters only as an optional labelled scalar rescale ≈0.28 of the finished result, not as a derivation)*: Produce the reactor-CEvNS differential rate dR/dE_rec ~~at the VNS normalization (∫Φ = 2.1×10¹² ν̄/cm²/s, two Chooz-B cores at 72 m and 102 m, 80% duty declared exactly once)~~, both trapping designs, from **100 meV** upward — with the CALC-15 impulse-approximation broadening applied *before* the response chain and the CALC-16 trigger curve applied on top of ε ≈ 0.5. Quantify the drop relative to the v1.0 3 GW_th / 25 m flagship (~3.6×). *(Added 2026-07-22 after the roadmapper correctly flagged that the headline signal output was implied by CALC-15/16/17 + VALD-10 but owned by no requirement ID.)*

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

- [x] **VALD-09** *(GATING — milestone stop-condition; **DISCHARGED NO FIT 2026-07-22**, see `phases/08-veto-envelope-geometry-gate-p-veto/08-05-GATE-VERDICT.md`)*: Determine whether a 4″×4″×2 mm, ~110 g Ge wafer physically fits the NUCLEUS COV/IV veto envelope, which is dimensioned for 6.8 g CaWO₄ and 4.5 g Al₂O₃ 3×3 arrays. **Footprint comparison, basis-labelled (corrected 2026-07-22 — the earlier unlabelled "~11× the footprint (103 vs ~9 cm²)" was wrong to state without a basis):** the wafer face is **103.2256 cm²**; on the **published NUCLEUS array-crystal basis** the reference footprint is **2.25 cm² = 9 × (5 mm)²** (arXiv:1905.10258 Fig. 8 + §3.2.1, the 5 mm edge independently confirmed by two mass closures), giving **45.9×**; on **this project's own holder-scale estimate** of ~9 cm² — **not a NUCLEUS number and not traceable to any NUCLEUS publication** — it is **11.5×**. The two bases differ by exactly a factor of 4 and neither may be quoted without its label (`fp-unlabelled-area-ratio`; `veto_envelope.area_ratio()` raises unless a basis is named). Being monolithic, the wafer has **no multiplicity handle at all**. Inherited veto credit defaults to **zero** unless earned. **If the wafer does not fit, STOP and re-scope with the user** (user decision 2026-07-22) — a forced shield/veto redesign means φ_post at the detector position is no longer NUCLEUS's φ_post and essentially nothing transfers. Must be resolved before the background chain is built on top of it.
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
| CALC-25 | Primary = frozen v1.0 flux used unmodified; broadening before response; trigger on top of eps; any VNS line is a labelled scalar rescale | Regression vs frozen v1.0 above 10 eV (<1%, VALD-10); VNS rescale factor 2.1/7.5 = 0.28 quoted as a label, not re-derived |
| CALC-17 | Bound computed, not estimated | Flat-continuation integral with the (1 − MT/2E²) factor; established ≤0.81% |
| CALC-18 | Target-swap closure factor ≲1.5; break condition >2 | Reproduce NUCLEUS's own CaWO₄/Al₂O₃ residuals with our pipeline before swapping in the Ge kernel |
| CALC-22 | S/B reported with and without inherited veto credit | L2-off baseline mandatory alongside any L2-credited number |
| VALD-10 | <1% deviation from frozen v1.0 above 10 eV | Direct comparison against committed v1.0 CSVs |
| VALD-11 | Both ratios (1.81, 1.20) from one normalization | Two-band calibration against Table 5 |
| VALD-12 | CONUS+ S/B ≈ 0.03 reproduced within a factor ~2 | Rescale our pipeline to 3.6 GW_th / 20.7 m / 7.4 m.w.e. and compare |

## Contract Coverage

| Requirement | Decisive Output / Deliverable | Anchor / Benchmark | Prior Inputs / Baselines | False Progress To Reject |
| ----------- | ----------------------------- | ------------------ | ------------------------ | ------------------------ |
| ~~CALC-11/12~~ **CALC-11 (re-pointed); CALC-12 unmet by design** | Frozen **sea-level surface** environment set — v1.0 muon + gamma re-declared unchanged, plus a rough sea-level neutron flux, order-of-magnitude labelled | **Source to be retrieved and verified in Phase 9**; candidates only (Gordon et al. IEEE TNS 51, 3427 (2004); ICRU/JEDEC-class spectra) — none asserted | v1.0 `paper/sections/backgrounds.tex` treatment; Phase-7 frozen n-Ge elastic set | `fp-shielded-quantity-leak`; `fp-precision-inflation`; quoting a sea-level neutron flux from memory rather than a retrieved source; lethargy/per-energy confusion |
| CALC-13/14/15/16 | Sub-eV spectra + trigger-probability curve | Campbell-Deem PRD 106, 036019; Sears PRB 35, 2038 | v1.0 `R(E_rec\|E_dep)` | `fp-poisson-as-resolution`; applying e^(−2W) to the total rate (it suppresses only the zero-phonon channel) |
| CALC-18/23 | Ge neutron + capture dR/dE_rec | Frozen ENDF/B-VIII.0 n-Ge elastic; ENDF MT=102 + EGAF; NCrystal | Phase 7 (carried forward), T_max/E_n = 0.0536 | `fp-mass-scaled-target`; reporting the capture channel as zero when φ_th is simply unobtained |
| CALC-19/20 | Compton + muon dR/dE_rec at the VNS | NUCLEUS Table 2; overburden 2.92 m.w.e., attenuation 1.41 | v1.0 Klein–Nishina and Gaisser–Guan machinery | Retaining the v1.0 sea-level muon flux or the Heusser gamma normalization after relocation |
| CALC-21/22 | S/B_particle + LEE-erasure amplitude | NUCLEUS Table 5 @ **100% duty** (356.5, not the prose 280) | Our CaWO₄ closure fold (407.7, ratio 1.14) | `fp-veto-credit-transfer`; `fp-lee-omission`; `fp-nucleus-prose-280` (flatters S/B by 27%) |
| VALD-09 **(discharged NO FIT)** | Geometry-fit determination | arXiv:2508.02488 COV cap 100 mm (**sole load-bearing geometric source**; TUM commissioning setup, not Chooz), corroborated by arXiv:1905.10258; EPJC 86,29 Fig. 1e/f established **dimensionally silent** | Wafer face **103.2256 cm²** vs the **published array-crystal 2.25 cm² = 9 × (5 mm)²** → **45.9×** (published-array-crystal basis). The project's own ~9 cm² holder-scale estimate → **11.5×**; **not a NUCLEUS number** | `fp-unlabelled-area-ratio` (quoting either ratio without its basis); proceeding past a failed gate on a premise already known false |
| VALD-12 **(restated 2026-07-22)** | CONUS+ **signal-side** reproduction — their SM CEvNS rate, not their S/B | Nature 643, 1229 (2025): SM expectation **347 ± 59** in 327 kg·d at 3.6 GW_th / 20.7 m, 0.4–1 keV_ee | v1.0 CONUS+ rate-scale check (factor 0.99) | Presenting the restated signal-side check as though it still validated the **ratio**; carrying the withdrawn 0.65–1.2 expectation in any form |

**Forbidden proxies (milestone-wide):** `fp-deposited-only`, `fp-no-saturation`, `fp-full-absorption`, keVee↔keVnr mixing / Lindhard quenching on the phonon scale, `fp-lumped-A`, `fp-gwe-gwth`, `fp-nucleus-3e12` (folding at the 2019 prose flux), **`fp-nucleus-prose-280`** (anchoring on the §2 prose CEvNS value instead of Table 5), **`fp-veto-credit-transfer`** (inheriting gram-scale veto rejection for a 110 g monolithic wafer), **`fp-lee-omission`** (reporting S/B without the LEE band), **`fp-mass-scaled-target`** (scaling CaWO₄/Al₂O₃ residuals to Ge by mass), **`fp-poisson-as-resolution`** (quoting the emergent counting floor as a resolution model).

## Traceability

Mapped by the roadmapper 2026-07-22. Every v2.0 primary requirement maps to **exactly one** primary phase; v2.0 phases are numbered 8–16 (v1.1's withdrawn Phases 8–12 free those numbers for reuse). Follow-up requirements deliberately carry no phase.

| Requirement | Phase | Status |
| ----------- | ----- | ------ |
| VALD-09 *(GATING stop-condition)* | Phase 8 — Veto-Envelope Geometry Gate (P-VETO) | **Discharged NO FIT 2026-07-22** |
| CALC-11 *(re-pointed; text needs re-wording)* | Phase 9 — Sea-Level Surface Environment Lock (P-ENV) | Pending — **object list void** (NUCLEUS VNS digitization set → sea-level surface set) |
| CALC-12 | ~~Phase 9~~ | **Unmet by design (2026-07-22 re-scope)** — no shield, so no post-shield fluence to recover; regularized inversion also excluded by the lowered accuracy expectation |
| VALD-11 *(gate on the Ge swap)* | ~~Phase 9~~ | **Unmet by design (2026-07-22 re-scope)** — it licensed swapping NUCLEUS's two-target residuals onto Ge, and no NUCLEUS residual is used any more. The kinematic-compression physics it protected is retained as ROADMAP Phase 13 SC4 |
| CALC-13 | Phase 10 — Sub-eV Grid & Trigger Observable (P-GRID) | Pending |
| CALC-16 | Phase 10 — Sub-eV Grid & Trigger Observable (P-GRID) | Pending |
| CALC-14 *(must precede CALC-15; own early plan)* | Phase 11 — Phonon Conventions & IA Broadening (P-CONV) | Pending |
| CALC-15 | Phase 11 — Phonon Conventions & IA Broadening (P-CONV) | Pending |
| CALC-17 | Phase 12 — CEvNS at the VNS to 100 meV (P-SIG) | Pending |
| CALC-25 *(re-pointed; text needs re-wording)* | Phase 12 — CEvNS at the Paper's Surface Scenario (P-SIG) | Pending — primary normalization is the paper's 3 GW_th / 25 m surface scenario; VNS demoted to an optional scalar rescale |
| VALD-10 | Phase 12 — CEvNS at the VNS to 100 meV (P-SIG) | Pending |
| CALC-18 *(re-pointed; text needs re-wording)* | Phase 13 — Ge Neutron Fold from the Sea-Level Flux (P-TGT) | Pending — input changes from φ_post to the rough sea-level flux; channel labelled order-of-magnitude |
| CALC-23 | Phase 14 — Ge-Only Capture Channels (P-GEONLY) | Pending — reduced to bounds |
| CALC-19 *(re-pointed; text needs re-wording)* | Phase 15 — v1.0 Muon & Gamma on the Extended Grid (P-EM) | Pending — the "replacing the v1.0 Heusser band" clause is **void**; v1.0 normalization stands |
| CALC-20 *(re-pointed; text needs re-wording)* | Phase 15 — v1.0 Muon & Gamma on the Extended Grid (P-EM) | Pending — the "replacing the v1.0 sea-level/no-overburden assumption" clause is **void**; v1.0 normalization stands |
| CALC-21 | Phase 16 — S/B Assembly, LEE, Signal-Side CONUS+ Check (P-SB) | Pending — unchanged by the re-scope |
| CALC-22 *(terminal)* | Phase 16 — S/B Assembly, LEE, Signal-Side CONUS+ Check (P-SB) | Pending — one baseline only; veto credit 1.0 by construction |
| VALD-12 *(restated 2026-07-22)* | Phase 16 — S/B Assembly, LEE, Signal-Side CONUS+ Check (P-SB) | Pending — **restated to its signal-side leg** (reproduce CONUS+'s SM CEvNS rate, not their S/B); the ratio now has no external validation, which must be disclosed on the deliverable |
| CALC-24 | — (follow-up, not in the v2.0 roadmap) | Deferred — **deferral rationale void** (it rested on VNS shield attenuation of the >10 MeV flux, which does not exist at the surface); deferral itself still stands under the lowered accuracy expectation |
| SIMU-05 | — (follow-up, not in the v2.0 roadmap) | Deferred |
| RADX-01 | — (follow-up, not in the v2.0 roadmap) | Deferred |
| MANU-01 | — (follow-up, not in the v2.0 roadmap) | Deferred |
| SENS-01 | — (follow-up, not in the v2.0 roadmap) | Deferred |

**Coverage (revised 2026-07-22 re-scope):** **15/17** primary requirements mapped, no duplicates. **2 orphaned by design** — CALC-12 and VALD-11, both listed above with their reason. Neither requirement text has been deleted; disposition (formally retire, defer to a follow-up milestone, or leave as a recorded non-goal) is the orchestrator's call. 5/5 follow-up requirements remain explicitly unmapped by design.

**Requirement texts needing re-wording after the re-scope (flagged, not edited):** CALC-11, CALC-18, CALC-19, CALC-20, CALC-25 — each named in its traceability row above with what specifically no longer matches.

> **Soft spot in the traceability, stated rather than papered over.** Phase 9's re-pointed deliverable — the frozen sea-level surface environment set, and specifically the rough sea-level neutron flux, the one genuinely new input of the re-scope — is carried under **CALC-11** provisionally, but CALC-11's literal text is the NUCLEUS VNS digitization set. Either re-word CALC-11 or add a new ID and re-map Phase 9. Until then Phase 9's coverage is nominal, not clean.

**Ordering constraints encoded in the roadmap dependency DAG (revised 2026-07-22):** VALD-09 (Phase 8) is **discharged**; ~~CALC-11 → CALC-12 → VALD-11 within Phase 9, and VALD-11 before Phase 13~~ — **removed with CALC-12 and VALD-11**; CALC-13 (Phase 10) still gates all sub-eV work; CALC-14 must still complete before CALC-15 inside Phase 11; CALC-25 (Phase 12) no longer depends on Phase 9; the restated VALD-12 must still pass before any headline claim in Phase 16.

~~**Coverage note (open):** no CALC ID explicitly owns "produce the CEvNS dR/dE_rec at the VNS normalization"…~~ **Closed:** CALC-25 owns the decisive signal deliverable and is mapped to Phase 12. Under the 2026-07-22 re-scope that deliverable is at the **paper's 3 GW_th / 25 m surface normalization**, not the VNS; CALC-25's text still says otherwise and is on the re-wording list above.

**Coverage note (open):** Ge inelastic (⁷⁴Ge 596 keV, ⁷²Ge 834 keV) and the B₄C ¹⁰B(n,α)⁷Li 478 keV γ line are carried as adjacent-scope deliverables in Phase 14 without a dedicated ID.
