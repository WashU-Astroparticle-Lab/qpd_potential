# Research Summary — v1.1 Neutron & Radiogenic Backgrounds

**Project:** QPD Particle-Physics Potential — In-band (CEvNS-band) background budget for a 4″×4″×2 mm (~110 g) single-sided QPD Ge wafer, both trapping designs (Ta→Al, Al→Hf)
**Milestone:** v1.1 — neutron-induced nuclear recoils + detector-material radioactivity, reconstructed energy, on the unified phonon scale (NO ionization quenching)
**Domain:** Low-background surface detector physics — cosmogenic/radiogenic neutron NR, cosmogenic activation, material radioassay
**Researched:** 2026-07-21 · **Synthesized:** 2026-07-21
**Confidence:** HIGH on the physics framing and the recommended method; MEDIUM on absolute normalizations (all three leading terms are gated by user-supplied scenario inputs, not by the calculation)

> This is the v1.1 milestone survey. The v1.0 survey (CEvNS/muon/Compton reconstructed spectra, 1 kg→110 g framing) is the prior `SUMMARY.md` content archived in git and at `GPD/milestones/v1.0/`. The v1.0 forward model — `shared_energy_grid()`, the `R(E_rec|E_dep)` response matrices, non-paralyzable 25 kHz censoring, and the Klein–Nishina Compton machinery — is **reused, not re-researched**. Everything below is the new background physics.

## Executive Summary

v1.1 adds the in-band background budget to the existing v1.0 QPD-Ge forward model. The four research files are unusually convergent, and their combined verdict is opinionated and clear: **for an unshielded surface wafer, ambient cosmogenic fast-neutron elastic scattering is the leading irreducible in-band nuclear-recoil background, and the cosmogenic ³H β continuum (18.6 keV endpoint) is the headline in-band electron-recoil background.** On the QPD unified phonon scale there is no keVnr/keVee distinction: a fast neutron elastically scattering off Ge deposits its full recoil energy `T` as phonons and lands on the *same axis* as a CEvNS recoil of the same `T`. Neutron elastic scattering is therefore kinematically indistinguishable from signal — the defining background of this milestone.

The recommended method is a single, laptop-scale analytic pipeline that every neutron channel collapses onto. Because the 2 mm wafer is optically thin to fast neutrons (elastic mean free path λ ≈ 5–6 cm ≫ 0.2 cm, so interaction probability ~3–4% and multiple-scatter ≪1%), no transport code is needed. Each channel reduces to a thin-target single-scatter flat-box fold, `dR/dT = N_Ge ∫ φ(E_n)·(σ_el/T_max) dE_n` with `T_max ≈ 0.0538·E_n` for Ge, using ENDF/B-VIII.0 n-Ge elastic data read with `openmc.data`. Detector radioactivity reuses the v1.0 Klein–Nishina Compton continuum for U/Th/⁴⁰K γ (thin wafer ⇒ Compton-dominated, MeV peaks escape) plus full-energy bulk deposits for intrinsic ³H/⁶⁸Ge/⁶⁵Zn (built with `radioactivedecay` + ENSDF lines), with (α,n)+SF neutron source terms from published yield tables. Every channel folds through the same `R(E_rec|E_dep)` matrices for both designs. The whole computation is seconds-to-minutes.

The principal risks are convention/bookkeeping, not compute. In priority order: (1) the **keV_nr vs keV_ee axis-tagging hazard** — the single sharpest pitfall: neutron-NR literature is usually quenched to keV_ee (Ge QF ≈ 0.16–0.23), but this project's phonon scale takes the full recoil with NO Lindhard quenching; mixing axes misplaces the NR background ~5× low and mis-normalizes dR/dE by ~1/QF (~4–6×). (2) **Surface-vs-underground is an inverted regime** — peer radiogenic/muon-induced-dominance numbers are underground residuals and must not be transferred; the unshielded surface sees ambient cosmogenic neutrons ~10⁶× higher. (3) **Muon-induced-neutron double counting** — the Gordon ambient flux already contains atmospheric-muon-cascade neutrons, so the muon-induced channel is LOCAL wafer+housing production only (~10⁻⁶/muon, subdominant), never a re-count of the v1.0 muon deposits. Two external assumptions are prerequisites, not derivations, and must be user-supplied: a housing/materials U/Th/⁴⁰K radiopurity budget, and a Ge surface-exposure/cool-down scenario (which sets the ³H/activation normalization).

## Unified Notation

Convention: detector/particle-physics practical units (energies eV/keV/MeV; rates counts kg⁻¹ d⁻¹ keV⁻¹ = "dru"; times s; lengths cm). All spectra live on the v1.0 `shared_energy_grid()` (~584 log bins, 10 eV→197 MeV, ~80/decade) and the unified phonon `E_dep` scale with **no ionization quenching**. No metric/Fourier issues (no field theory). Binding downstream.

| Symbol | Quantity | Units | Convention notes (reconciled across files) |
| --- | --- | --- | --- |
| `T ≡ E_R ≡ E_nr` | Nuclear-recoil kinetic energy | keV/eV | METHODS uses `T_r`; PRIOR-WORK/PITFALLS use `E_R`/`E_nr`. Unified `T`. **On phonon scale `E_dep = T` (no QF)**, minus few-% NR-only Frenkel storage. |
| `E_n` | Incident neutron energy | MeV | Source-spectrum variable. |
| `T_max` | Max Ge elastic recoil | keV | `T_max = 4A/(1+A)²·E_n ≈ 0.0538·E_n` (A≈72.6). 1 MeV n → ≤54 keV_nr. |
| `dσ_el/dT` | Elastic recoil kernel | b/keV | s-wave (isotropic-CM): **flat box** `= σ_el/T_max`, 0→T_max. `a₁` Legendre correction only for `E_n ≳ 1 MeV`. |
| `φ(E_n)`, `Φ_n` | Neutron flux (differential / integral) | cm⁻² s⁻¹ (MeV⁻¹) | Gordon-2004 native units. Tag every flux with (depth, shielding) provenance. |
| `Y` | Radiogenic neutron yield | n g⁻¹ s⁻¹ per ppb U/Th | Mei–Zhang–Hime convention. ²³⁸U SF material-independent. |
| `QF` | Ge ionization quenching factor | dimensionless | ≈0.16–0.23 over 0.4–8.5 keV_nr (Lindhard k≈0.162). **Used ONLY to un-quench keV_ee imports — NEVER applied to the phonon scale.** |
| `A(t)` | Cosmogenic activity | Bq or decays kg⁻¹ d⁻¹ | `A = R·N·[1−e^{−λt_exp}]·e^{−λt_cool}`; isotope-specific — never a blanket saturation value. |
| U/Th contamination | radiopurity | ppb ↔ µBq/kg | 1 ppb U ≈ 12.4 mBq/kg; 1 ppb Th ≈ 4.06 mBq/kg. Assays quote Bq/kg, yield codes want ppb. |
| `dru` | differential rate | counts keV⁻¹ kg⁻¹ d⁻¹ | Peer unit (NUCLEUS/CONUS/RELICS). Retain per-kg despite 110 g geometry. |
| `R(E_rec|E_dep)` | v1.0 response matrix | — | Non-paralyzable 25 kHz (40 µs). Fold every channel, both designs. `E_rec ≈ 0.5·E_dep` (linear). |

**Notation reconciliation resolved (documented, not a physics conflict):** METHODS.md labels the Gordon `~1.3×10⁻² cm⁻²s⁻¹` figure as ">1 MeV" while PRIOR-WORK.md labels it "total broad (all E)"; the ">10 MeV" integral is `3.5–3.6×10⁻³`. Web-verified: `3.5×10⁻³` is the >10 MeV number, `~1.3×10⁻²` is the broad thermal→GeV integral. The fold uses the full parametrization, so this is a labeling fix (address at the P-NSRC provenance table), not a numeric discrepancy.

## Key Findings

### Prior Work Landscape (from PRIOR-WORK.md — HIGH)

**Must-reproduce benchmarks (in-band):**
- **Gordon (2004) sea-level fast-neutron flux:** `Φ_n(>10 MeV) = 3.50×10⁻³ cm⁻²s⁻¹` (NYC, mid-solar), broad flux ~`1.3×10⁻²`. *Independently web-verified.* This IS the surface number — directly transferable (state indoor/outdoor).
- **³H cosmogenic production (sea level):** `74±9` (CDMSlite) / `82±21` (EDELWEISS-III) atoms kg⁻¹ d⁻¹; ⁶⁵Zn `17±5`/`106±13`; ⁶⁸Ge `30±18`/`>71`. *Web-verified.* ³H β continuum 0→18.6 keV is the headline in-band ER background — no line to subtract.
- **²³⁸U spontaneous-fission yield:** `1.353×10⁻¹¹ n g⁻¹ s⁻¹ per ppb U`, material-independent, ⟨E_n⟩≈2 MeV (Watt).
- **Ge bulk radiopurity:** ~µBq/kg U/Th (GERDA) — intrinsic radiogenic term is tiny. **Electroformed Cu housing benchmark:** <0.3 µBq/kg U/Th; common structural materials mBq–Bq/kg.
- **Surface-like peer benchmark:** NUCLEUS shallow reactor site — residual 10–100 eV background *strongly dominated by cosmic-ray neutrons*, ~250 dru predicted residual against a ~100 dru target after >2 orders-of-magnitude rejection. *Web-verified (qualitative dominance HIGH; exact dru MEDIUM, and it is a shielded lower bound for our unshielded case).*

**Second neutron channel:** thermal/epithermal capture-γ-cascade recoils overlap CEvNS ≲100 eV (Biffl/Villano 2023); thermal-flux ceiling `7×10⁻⁴ n cm⁻²s⁻¹`. Distinct from elastic; populates the flagship bins.

**Do-NOT-transfer:** underground radiogenic/muon-induced dominance (inverted regime); NUCLEUS/CONUS post-shield residuals (import as shielded lower bounds only, back-corrected).

### Methods and Tools (from METHODS.md — MEDIUM-HIGH)

Central recommendation: **every neutron channel = one flat-box fold** `dR/dT = N_Ge ∫ φ(E_n)·σ_el/T_max dE_n`, exact for `E_n ≲ 0.5–1 MeV` (s-wave), with an `a₁` Legendre forward-peaking correction above ~1 MeV. Thin-target single-scatter justified analytically (t/λ ≈ 3–4%). Channel-specific source terms:
1. **Ambient cosmogenic** (highest priority): Gordon φ(E_n) × flat-box.
2. **Muon-induced local**: Wang-2001 yield `N_n ≈ 4.14×10⁻⁶ E_μ^0.74 n/(µ·g·cm⁻²)`, normalized to the v1.0 Gaisser–Guan muon flux, **restricted to wafer+housing production** (~10⁻⁶/muon in-wafer) — bounded subdominant correction.
3. **Radiogenic (α,n)+SF**: published per-material yield tables + ²³⁸U Watt spectrum × solid-angle × flat-box.
4. **Radiogenic γ/β ER**: reuse v1.0 Klein–Nishina Compton (U/Th/⁴⁰K lines + XCOM attenuation) + bulk full-energy β/EC deposits for intrinsic ³H, ⁶⁸Ge/⁶⁸Ga, ⁶⁵Zn.
5. **Cosmogenic activation inventory**: measured sea-level rates × assumed exposure/cooldown → source normalization for #4.

### Computational Approaches (from COMPUTATIONAL.md — MEDIUM-HIGH)

Stack reuses the v1.0 numpy/scipy pipeline. New pieces: `openmc.data.IncidentNeutron.from_endf` (pure-Python ENDF MF=3/MF=4 reader — no NJOY, no multi-GB HDF5 library; only the 5 Ge isotope evaluations), two-body kinematics + Jacobian → per-isotope recoil kernels → single-scatter flux fold; `radioactivedecay` (Bateman activities) + curated ENSDF/DDEP lines; `xraylib`/frozen NIST XCOM for photon attenuation. All outputs are provenance-headed CSVs on `shared_energy_grid()`, folded through the existing `R` matrices with count-conservation asserts. Fallbacks (sandy, ENDFtk, NJOY2016, SOURCES-4C, ACTIVIA, EXPACS/PARMA) are cross-checks only. **No G4CMP/Geant4/MCNP.** Convergence care: integrate on the union of the ENDF native grid and the flux grid so sub-MeV Ge(n,el) resonances are resolved.

### Critical Pitfalls (from PITFALLS.md — HIGH on the top four)

1. **Quenching confusion (keV_nr vs keV_ee) — the sharpest hazard.** Transfer NR on keV_nr = E_dep (no QF). If a source gives keV_ee, un-quench with `E_nr = E_ee/QF(E_nr)` and the Jacobian `dE_nr/dE_ee`. Guard against any Lindhard factor on the phonon scale (CONVENTIONS §B). Failure signature: NR background peaks ~5× low, dR/dE off ~1/QF.
2. **Muon–neutron double counting.** Keep the muon-induced-neutron source term independent; normalize to surrounding-converter mass + transport, NOT to wafer-crossing muons; verify the v1.0 muon spectrum is byte-identical with the neutron channel on/off.
3. **Thin-wafer single-scatter/escape.** Deposit ≤5.4% of E_n per interaction (sampled from the angular distribution), P_int ≈ nσt ~3–6%; sum the ≲1% multi-site events into one E_dep (no position/veto handle). Never deposit full neutron energy.
4. **Surface vs underground flux.** Tag every flux with (depth, shielding); surface baseline uses raw Gordon/sea-level with no shield; RELICS/NUCLEUS residuals are back-corrected cross-checks only.
5. **Self-shielding inverted (P-RAD).** 2 mm is optically thin to MeV γ (λ~3 cm): internal γ *peaks escape* (Compton edge only), but low-E X-rays/Augers/β (⁶⁸Ge/⁷¹Ge EC ~1.3/10.4 keV, ³H β) *deposit fully* — these are the in-band killers. External sources need activity×(Ω/4π)×self-abs×path-atten×μt, not full-peak efficiency.
6. **Cosmogenic history dependence.** Isotope-specific `A(t)`; ⁶⁸Ge/⁶⁵Zn saturate (~1 yr), **³H (12.3 yr) never saturates — carries the exposure-time dependence**.
7. **(α,n) material dependence.** Per-material yields (low-Z content dominates; α range ~tens of µm; thin-film α-escape); pure Ge yields ~nothing.
8. **Deposited-energy-only reporting.** Fold every channel to E_rec through R for both designs; evaluate CEvNS-band overlap in E_rec (MeV deposits saturate and leak downward). Honor the 10 eV display floor.

## Approximation Landscape

| Method | Valid regime | Breaks down when | Controlled? | Complements |
| --- | --- | --- | --- | --- |
| Isotropic-CM flat-box recoil kernel | `E_n ≲ 0.5–1 MeV` (s-wave) | `E_n ≳ 1 MeV` (forward-peaking) | Yes — `a₁` Legendre expansion parameter | ENDF File-4 angular fold |
| Thin-target single-scatter fold | 2 mm wafer, fast n (λ~5–6 cm) | thick targets / thermalization | Yes — expansion in t/λ~3–4% | Bespoke single-scatter MC (cross-check) |
| Watt ²³⁸U SF spectrum | fast SF neutrons | — (parameter-set spread ~10%) | Partly — pin one (a,b) set | SOURCES-4C/NeuCBOT |
| Klein–Nishina thin-target Compton (reused) | MeV γ, optically-thin wafer | thick crystal (full peaks) | Yes | Bulk full-energy β/EC deposits |
| Bulk full-energy deposit (β/EC) | range ≪ mm (low-E) | MeV γ (escapes) | Yes | XCOM attenuation for γ |
| Solid-angle × exp-attenuation (external) | small solid angle, standoff | near-contact geometry | Yes | per-material assay input |
| Isotope-specific Bateman `A(t)` | any exposure/cooldown | secular-eq edge cases | Yes (analytic) | measured production rates |

**Coverage gaps (no reliable in-project method):** (a) **Low-Energy Excess (LEE)** below ~100 eV — every phonon detector shows an unmodeled rising excess; the modeled in-band floor is a strict *lower bound*. (b) Exact single/multiple-scatter *spectral shape* in 2 mm at the highest E_n (a light MCNP/Geant4 run would confirm the ≲1% tail — out of scope, flag as the thing to confirm). (c) (α,n) yields for the specific QPD film/adhesive materials absent from published tables (needs assay + NeuCBOT).

## Theoretical Connections

- **One kernel, three neutron sources (established).** Cosmogenic, muon-induced, and radiogenic neutrons differ only in `φ(E_n)`; all fold through the identical flat-box kernel and the same `R(E_rec|E_dep)`. Build the fold once, feed three source terms.
- **v1.0 ↔ v1.1 machinery reuse (established).** The v1.1 γ-ER channel is the v1.0 environmental-Compton channel with an extended line list; the response fold, censoring, and shared grid are identical. Cross-validation: v1.1 must reproduce the v1.0 Compton spectrum when given the v1.0 line list.
- **Double-counting partition (established, load-bearing).** Gordon ambient ⊇ atmospheric-muon-cascade neutrons ⇒ muon-induced channel = LOCAL production only; the v1.0 direct-ionization muon deposit and the neutron recoil are two independent deposits with different geometric acceptance.
- **Surface/underground duality (established).** The regime inverts which term dominates (ambient cosmogenic at surface ↔ radiogenic/μ-induced underground). Peer numbers carry a (depth, shielding) tag that determines transferability.
- **NR/ER unification on the phonon axis (established).** No discrimination: CEvNS, neutron NR, and every ER land undiscriminated on one E_rec axis — the entire rationale for the in-band budget.

## Critical Claim Verification

| # | Claim | Source | Verification | Result |
| --- | --- | --- | --- | --- |
| 1 | Gordon sea-level `Φ_n(>10 MeV)=3.5×10⁻³ cm⁻²s⁻¹` | PRIOR-WORK/METHODS/PITFALLS | WebSearch: Gordon 2004 integral flux | **CONFIRMED** (3.5×10⁻³; 3.6×10⁻³ over 10 MeV–10 GeV) |
| 2 | Surface reactor-CEvNS in-band floor is cosmic-neutron-dominated | PRIOR-WORK (NUCLEUS) | WebSearch: NUCLEUS background 2026 | **CONFIRMED** (dominant residual cosmic-ray fast-neutron term in 10–100 eV ROI) |
| 3 | Ge QF ≈0.16–0.23, Lindhard k≈0.162, used only to un-quench | PITFALLS | WebSearch: Bonhomme 2022 / Collar | **CONFIRMED** (k=0.162±0.004; **but sub-keV QF is contested — Collar–Lewis comment**) |
| 4 | ³H production 74±9 / 82±21 atoms kg⁻¹d⁻¹ sea level | PRIOR-WORK/METHODS | WebSearch: CDMSlite/EDELWEISS | **CONFIRMED** (74±9 CDMSlite, 82±21 EDELWEISS) |
| 5 | ⁶⁵Zn 17±5, ⁶⁸Ge 30±18 atoms kg⁻¹d⁻¹ (CDMSlite) | PRIOR-WORK | WebSearch: CDMSlite cosmogenic | **CONFIRMED** |
| 6 | `T_max=4A/(1+A)²·E_n≈0.0538 E_n` for Ge | METHODS | Textbook two-body kinematics | CONFIRMED (analytic) |
| 7 | Thin-target λ~5–6 cm, P_int~3–4% in 2 mm | METHODS/COMPUTATIONAL/PITFALLS | Consistent across 3 files; Σ≈0.18 cm⁻¹ | CONFIRMED (internally consistent) |

## Cross-Validation Matrix

|  | Analytic fold | Bespoke MC | Published peer data | Nuclear-data lib |
| --- | :---: | :---: | :---: | :---: |
| **Ambient neutron NR** | — | single-scatter fraction, geometry | NUCLEUS ~250 dru (shielded lower bound), RELICS residual (back-corrected) | ENDF vs JEFF-3.3 σ_el |
| **Muon-induced local NR** | flat-box | — | Wang-2001 N_n norm; CONUS 80% (24 m.w.e., not transferable) | — |
| **(α,n)+SF NR** | Watt/table fold | — | Mei–Zhang–Hime yields | SOURCES-4C/NeuCBOT cross-check |
| **γ/β ER (radiogenic)** | KN reuse | — | RELICS ER ~0.31 dru (geometry-corrected) | ENSDF lines; XCOM/xraylib |
| **Cosmogenic ³H/activation** | A(t) Bateman | — | CDMSlite/EDELWEISS rates | radioactivedecay |

**High-risk (weak independent cross-check):** the *absolute ambient-neutron normalization* (site-dependent; verifiable only against Gordon integral + a shielded peer lower bound) and the *(α,n) budget* (gated by an unknown assay). Both are input-limited, not method-limited.

## Input Quality → Roadmap Impact

| Input file | Quality | Affected recommendations | Impact if wrong |
| --- | --- | --- | --- |
| METHODS.md | good | Flat-box method, channel decomposition, double-count resolution | Method choice wrong → all neutron phases replanned (low likelihood — verified) |
| PRIOR-WORK.md | good | Benchmark fluxes/rates, surface-vs-underground verdict | Benchmark/normalization wrong → in-band budget mis-scaled |
| COMPUTATIONAL.md | good | Tooling (openmc.data, radioactivedecay), data flow | Tool substitution (sandy/ENDFtk fallbacks exist) |
| PITFALLS.md | good | Axis-tagging, saturation fold, self-shielding, all guards | Blind spots in every channel — this file is the guardrail |

All four inputs are substantive with explicit confidence markers. No file is thin or missing; no blocking contradiction. No preliminary hazard-survey phase needed (PITFALLS is comprehensive).

## Implications for Research Plan

Suggested phase structure (dependency-ordered; the roadmapper derives final phases from REQUIREMENTS objectives). Phase handles map to the PITFALLS suggested handles P-NSRC/P-NTRANS/P-RAD/P-COSMO/P-FOLD.

### Phase 1 — Scenario & Nuclear-Data Lock (prerequisite)
**Rationale:** Three leading terms are gated by user-supplied assumptions, not calculation. Lock them before folding.
**Delivers:** (a) site ambient-neutron normalization (indoor vs outdoor / building shielding) with provenance; (b) housing/materials U/Th/⁴⁰K radiopurity budget; (c) Ge surface-exposure/cool-down scenario; (d) acquired ENDF/B-VIII.0 n-Ge elastic (5 isotopes) parsed with `openmc.data`.
**Avoids:** Pitfall 7 (surface/underground provenance). **Needs research/user input:** YES — (a)(b)(c) are external inputs. **Risk:** MEDIUM.

### Phase 2 — Neutron Source Terms (P-NSRC)
**Rationale:** Assemble `φ(E_n)` for all three neutron sources with axis + depth/shielding provenance tags before any recoil physics.
**Delivers:** Gordon ambient spectrum; local muon-induced source (normalized to v1.0 muon flux, wafer+housing only); (α,n)+SF Watt source per assumed assay.
**Uses:** Gordon-2004, Wang-2001, Mei–Zhang–Hime, published (α,n) tables. **Avoids:** Pitfalls 1, 2, 7. **Risk:** MEDIUM (double-count discipline is the trap).

### Phase 3 — Neutron Transport & Recoil Fold (P-NTRANS)
**Rationale:** With source terms and cross sections in hand, apply the one flat-box single-scatter fold.
**Delivers:** neutron `dR/dE_dep` (three channels, labeled) on `shared_energy_grid()`; reported P_int~3–4% and multi-scatter ≲1%.
**Uses:** flat-box kernel + `a₁` correction; two-body kinematics. **Validates:** `T_max=0.0538 E_n`; box integrates to `σ_el·N_Ge`. **Avoids:** Pitfalls 1, 3. **Risk:** LOW (well-anchored physics).

### Phase 4 — Detector Radioactivity Budget (P-RAD) — *parallel with 2–3*
**Rationale:** Independent of the neutron fold; gated by the same assay input from Phase 1.
**Delivers:** Ge-bulk + housing γ-ER (KN reuse + XCOM/self-shielding), intrinsic β/EC bulk deposits, (α,n)+SF NR source into P-NTRANS.
**Uses:** reused Klein–Nishina, `radioactivedecay`, ENSDF/DDEP, xraylib. **Avoids:** Pitfalls 4, 6. **Risk:** MEDIUM (solid-angle/attenuation normalization).

### Phase 5 — Cosmogenic Activation Inventory (P-COSMO) — *feeds Phase 4*
**Rationale:** Sets the ³H/⁶⁸Ge/⁶⁵Zn source normalization via isotope-specific `A(t)`.
**Delivers:** activation inventory for the stated exposure/cooldown; ³H β continuum + EC X-ray lines as in-band ER templates.
**Uses:** CDMSlite/EDELWEISS rates × Bateman `A(t)`. **Validates:** ³H 74–82, ⁶⁵Zn 17, ⁶⁸Ge 30 atoms kg⁻¹d⁻¹. **Avoids:** Pitfall 5 (³H never saturates). **Risk:** MEDIUM (exposure-scenario dependent).

### Phase 6 — Response Fold & Combined In-Band Budget (P-FOLD)
**Rationale:** Everything converges to reconstructed energy; only here is the CEvNS-band overlap physical.
**Delivers:** all channels folded through `R(E_rec|E_dep)` (both designs, non-paralyzable 25 kHz); combined in-band budget vs the v1.0 CEvNS signal; peer normalization cross-checks (NUCLEUS/CONUS/RELICS back-corrected).
**Uses:** v1.0 `response.py`/`response_matrix.py` unchanged. **Validates:** v1.0 muon spectrum byte-identical (invariant); count conservation; 10 eV display floor. **Avoids:** Pitfall 8. **Risk:** LOW (reuses validated v1.0 fold).

### Phase Ordering Rationale
- Inputs (Phase 1) gate normalization for 3 of the 4 leading terms — lock first.
- Neutron chain (2→3) and radioactivity chain (4←5) are **parallelizable**; they converge only at the fold (Phase 6).
- Analytic folds precede any MC cross-check (single-scatter fraction, geometry) — MC validates, does not drive.

### Phases Requiring Deeper Investigation
- **Phase 1** — external user inputs (site flux, radiopurity, exposure scenario); genuinely open, blocks normalization.
- **Phase 4** — (α,n) per-material for QPD films/adhesives may need NeuCBOT if absent from tables.
- **Genuinely open:** whether reactor-correlated thermal-capture NR at 25 m unshielded adds an in-band channel (Biffl/Villano); and the LEE below ~100 eV (unmodeled — floor is a lower bound).

Well-established (straightforward): **Phase 3** (textbook kinematics + ENDF), **Phase 6** (reuses v1.0).

## Confidence Assessment

| Area | Confidence | Notes |
| --- | --- | --- |
| Computational Approaches | HIGH | openmc.data/radioactivedecay/xraylib mature; laptop-scale analytic fold; reuses validated v1.0 |
| Prior Work | HIGH | Gordon/CDMSlite/EDELWEISS/GERDA all peer-reviewed; 5 claims independently web-verified |
| Methods | HIGH | Flat-box + thin-target single-scatter verified analytically and cross-file consistent |
| Pitfalls | HIGH | Comprehensive; grounded in CONVENTIONS §B/§F + published QF/activation/flux literature |

**Overall confidence:** HIGH on physics framing and method; MEDIUM on absolute in-band magnitudes (input-gated).

### Gaps to Address
- **Local ambient-neutron normalization** (indoor/outdoor/building shielding) — factor-of-a-few, the single largest uncertainty. Resolve in Phase 1.
- **Housing/materials radiopurity budget** — required user input; blocks P-RAD absolute rate.
- **Ge exposure/cool-down scenario** — required user input; sets ³H (never-saturating) normalization.
- **Sub-keV Ge QF controversy** (Bonhomme k=0.162 vs Collar–Lewis) — load-bearing ONLY if keV_ee NR numbers are imported; the keV_nr baseline avoids it. Document the QF(E) model + uncertainty if any un-quenching is done.
- **LEE below ~100 eV** — unmodeled; state the in-band floor as a lower bound.
- **Reactor-correlated thermal-capture NR** at 25 m unshielded — needs a scoped estimate; unlike ambient, it is reactor on/off separable.

## Sources

### Primary (HIGH)
- Gordon et al., IEEE TNS 51, 3427 (2004) — sea-level cosmic-ray neutron flux (verified). https://www.researchgate.net/publication/3139171
- Amman et al. (CDMSlite), Astropart. Phys. 105, 44 (2019), arXiv:1806.07043 — Ge cosmogenic ³H/⁶⁵Zn/⁶⁸Ge (verified). https://arxiv.org/abs/1806.07043
- Armengaud et al. (EDELWEISS-III), Astropart. Phys. 91, 51 (2017), arXiv:1607.04560 — Ge activation.
- Mei, Zhang & Hime, NIMA 606, 651 (2009), arXiv:0812.4307 — (α,n)+SF yields (²³⁸U SF 1.353×10⁻¹¹ n/g/s/ppb).
- NUCLEUS Collab., EPJC 86 (2026), arXiv:2509.03559 — surface-like cosmic-neutron-dominated in-band floor (verified). https://link.springer.com/article/10.1140/epjc/s10052-025-15168-9
- Agostini et al. (GERDA), Astropart. Phys. 91, 15 (2017), arXiv:1611.06884 — Ge bulk µBq/kg U/Th.
- ENDF/B-VIII.0 — Brown et al., Nucl. Data Sheets 148, 1 (2018).

### Secondary (MEDIUM)
- Bonhomme et al., EPJC 82, 815 (2022), arXiv:2202.03754 — Ge QF, Lindhard k=0.162 (verified); Collar & Lewis, arXiv:2203.00750 — sub-keV QF critique. https://arxiv.org/abs/2202.03754
- Biffl, Villano et al., PRD 107, 092011 (2023), arXiv:2212.14148 — thermal-capture NR overlap ≲100 eV.
- CONUS Collab., EPJC 79, 699 (2019) & arXiv:2112.09585 — μ-induced fraction, reactor thermal fluence (shielded, back-correct).
- Wang et al., arXiv:hep-ex/0101049 — muon-induced neutron yield.
- Cai et al. (RELICS), PRD 110, 072011 (2024) — same 3 GW/25 m config; post-shield residuals (cross-check only).
- Verbeke et al. UCRL-AR-228518 — ²³⁸U SF Watt parameters (spread noted).

### Tertiary (LOW / flags)
- LEE review, arXiv:2503.08859 — unmodeled near-threshold excess (floor is a lower bound).
- ENDF/B-VIII.1 (2024), arXiv:2511.03564 — sensitivity check, not baseline.
- SOURCES-4C / NeuCBOT (arXiv:1702.02465) — (α,n) cross-checks.

---

_Research analysis completed: 2026-07-21 · Ready for research plan: yes_

```yaml
# --- ROADMAP INPUT (machine-readable, consumed by gpd-roadmapper) ---
synthesis_meta:
  project_title: "QPD Particle-Physics Potential — v1.1 Neutron & Radiogenic Backgrounds"
  synthesis_date: "2026-07-21"
  input_files: [METHODS.md, PRIOR-WORK.md, COMPUTATIONAL.md, PITFALLS.md]
  input_quality: {METHODS: good, PRIOR-WORK: good, COMPUTATIONAL: good, PITFALLS: good}

conventions:
  unit_system: "detector-practical (eV/keV/MeV; counts/kg/day/keV=dru; cm; s); natural units internal to cross sections only"
  energy_scale: "unified phonon E_dep, NO ionization quenching (CONVENTIONS B); E_dep = E_nr for NR minus few-percent Frenkel"
  forbidden: "keVee<->keVnr mixing; Lindhard/QF on the phonon scale"
  response: "R(E_rec|E_dep) both designs (Ta->Al, Al->Hf), non-paralyzable 25 kHz (40 us); E_rec ~= 0.5 E_dep linear"
  shared_grid: "shared_energy_grid() ~584 log bins, 10 eV -> 197 MeV, ~80/decade"
  display_floor: "never plot below 10 eV"

methods_ranked:
  - name: "Isotropic-CM flat-box recoil kernel fold (dsigma/dT = sigma_el/T_max)"
    regime: "E_n <~ 0.5-1 MeV (s-wave); all three neutron channels"
    confidence: HIGH
    cost: "1-D quadrature, <1 s"
    complements: "a1 Legendre angular fold above 1 MeV"
  - name: "Thin-target single-scatter transport (analytic, no MC)"
    regime: "2 mm wafer, fast n (lambda~5-6 cm, P_int~3-4%)"
    confidence: HIGH
    cost: "seconds"
    complements: "bespoke single-scatter MC for geometry/tail cross-check"
  - name: "ENDF/B-VIII.0 n-Ge elastic via openmc.data (MF=3/MF=4)"
    regime: "5 Ge isotopes, meV->GeV; resonance-resolved on union grid"
    confidence: HIGH
    cost: "<10 s/isotope"
    complements: "JEFF-3.3 / sandy / ENDFtk cross-check"
  - name: "Klein-Nishina thin-target Compton (reuse v1.0) + bulk full-energy beta/EC deposits"
    regime: "MeV gamma escape (Compton edge); low-E X-ray/Auger/beta deposit fully"
    confidence: HIGH
    cost: "seconds (reused)"
    complements: "xraylib/XCOM attenuation"
  - name: "radioactivedecay Bateman A(t) + ENSDF/DDEP lines"
    regime: "U/Th chains, 40K, 3H, 68Ge/68Ga, 65Zn isotope-specific activity"
    confidence: HIGH
    cost: "seconds (analytic)"
    complements: "measured CDMSlite/EDELWEISS production rates"
  - name: "Published (alpha,n) yield tables + 238U Watt SF spectrum"
    regime: "radiogenic neutrons per assumed U/Th assay, per material"
    confidence: MEDIUM
    cost: "table fold, seconds"
    complements: "NeuCBOT/SOURCES-4C for stack materials absent from tables"
  - name: "Gordon-2004 sea-level neutron flux (static parametrization)"
    regime: "surface, no overburden; indoor/outdoor caveat"
    confidence: HIGH
    cost: "static table"
    complements: "EXPACS/PARMA for site altitude/geomagnetic scaling"

phase_suggestions:
  - name: "Scenario & Nuclear-Data Lock"
    goal: "Fix the three external normalization inputs and acquire n-Ge elastic data before any fold."
    methods: ["ENDF/B-VIII.0 n-Ge elastic via openmc.data (MF=3/MF=4)", "Gordon-2004 sea-level neutron flux (static parametrization)"]
    depends_on: []
    needs_research: true
    risk: MEDIUM
    pitfalls: ["pitfall-7-surface-vs-underground"]
  - name: "Neutron Source Terms (P-NSRC)"
    goal: "Assemble ambient/muon-induced/radiogenic phi(E_n) with axis+depth/shielding provenance."
    methods: ["Gordon-2004 sea-level neutron flux (static parametrization)", "Published (alpha,n) yield tables + 238U Watt SF spectrum"]
    depends_on: ["Scenario & Nuclear-Data Lock"]
    needs_research: false
    risk: MEDIUM
    pitfalls: ["pitfall-1-quenching-axis", "pitfall-2-muon-neutron-double-count", "pitfall-7-surface-vs-underground"]
  - name: "Neutron Transport & Recoil Fold (P-NTRANS)"
    goal: "Produce labeled neutron dR/dE_dep via the flat-box single-scatter fold."
    methods: ["Isotropic-CM flat-box recoil kernel fold (dsigma/dT = sigma_el/T_max)", "Thin-target single-scatter transport (analytic, no MC)", "ENDF/B-VIII.0 n-Ge elastic via openmc.data (MF=3/MF=4)"]
    depends_on: ["Neutron Source Terms (P-NSRC)"]
    needs_research: false
    risk: LOW
    pitfalls: ["pitfall-1-quenching-axis", "pitfall-3-thin-wafer-single-scatter"]
  - name: "Detector Radioactivity Budget (P-RAD)"
    goal: "Ge-bulk + housing gamma-ER, intrinsic beta/EC deposits, and (alpha,n)+SF NR source."
    methods: ["Klein-Nishina thin-target Compton (reuse v1.0) + bulk full-energy beta/EC deposits", "radioactivedecay Bateman A(t) + ENSDF/DDEP lines", "Published (alpha,n) yield tables + 238U Watt SF spectrum"]
    depends_on: ["Scenario & Nuclear-Data Lock"]
    needs_research: false
    risk: MEDIUM
    pitfalls: ["pitfall-4-self-shielding-solid-angle", "pitfall-6-alpha-n-material-dependence"]
  - name: "Cosmogenic Activation Inventory (P-COSMO)"
    goal: "Isotope-specific A(t) sets 3H/68Ge/65Zn source normalization for the ER templates."
    methods: ["radioactivedecay Bateman A(t) + ENSDF/DDEP lines"]
    depends_on: ["Scenario & Nuclear-Data Lock"]
    needs_research: false
    risk: MEDIUM
    pitfalls: ["pitfall-5-cosmogenic-history-dependence"]
  - name: "Response Fold & Combined In-Band Budget (P-FOLD)"
    goal: "Fold every channel to E_rec (both designs) and compare the in-band budget to the v1.0 CEvNS signal."
    methods: ["Klein-Nishina thin-target Compton (reuse v1.0) + bulk full-energy beta/EC deposits"]
    depends_on: ["Neutron Transport & Recoil Fold (P-NTRANS)", "Detector Radioactivity Budget (P-RAD)", "Cosmogenic Activation Inventory (P-COSMO)"]
    needs_research: false
    risk: LOW
    pitfalls: ["pitfall-8-deposited-only-spectra"]

critical_benchmarks:
  - quantity: "Sea-level cosmic-ray fast-neutron flux >10 MeV"
    value: "3.5e-3 cm^-2 s^-1 (broad thermal->GeV ~1.3e-2)"
    source: "Gordon et al., IEEE TNS 51, 3427 (2004)"
    confidence: HIGH
  - quantity: "Ge elastic max recoil fraction T_max/E_n"
    value: "4A/(1+A)^2 = 0.0538 (A=72.6)"
    source: "two-body kinematics (textbook)"
    confidence: HIGH
  - quantity: "Fast-n elastic mean free path in Ge / interaction prob in 2 mm"
    value: "lambda ~5-6 cm; P_int ~3-4%; multi-scatter <~1%"
    source: "METHODS/COMPUTATIONAL/PITFALLS (Sigma~0.18 cm^-1)"
    confidence: HIGH
  - quantity: "238U spontaneous-fission neutron yield"
    value: "1.353e-11 n/g/s per ppb U; <E_n>~2 MeV (Watt)"
    source: "Mei, Zhang & Hime, NIMA 606, 651 (2009)"
    confidence: HIGH
  - quantity: "3H cosmogenic production in Ge (sea level); endpoint"
    value: "74(9) [CDMSlite] / 82(21) [EDELWEISS] atoms/kg/day; Q=18.6 keV"
    source: "Amman 2019 (arXiv:1806.07043); Armengaud 2017"
    confidence: HIGH
  - quantity: "65Zn / 68Ge cosmogenic production in Ge (sea level, CDMSlite)"
    value: "65Zn 17(5); 68Ge 30(18) atoms/kg/day"
    source: "Amman et al. (CDMSlite) 2019"
    confidence: MEDIUM
  - quantity: "Surface-like reactor-CEvNS in-band residual (shielded lower bound)"
    value: "~250 dru predicted, cosmic-neutron-dominated, 10-100 eV"
    source: "NUCLEUS Collab., arXiv:2509.03559 (2026)"
    confidence: MEDIUM
  - quantity: "Electroformed-Cu housing radiopurity"
    value: "<0.3 uBq/kg U and Th"
    source: "MAJORANA assay, OSTI 1481666"
    confidence: HIGH
  - quantity: "Ge ionization quenching factor (for un-quenching keV_ee imports only)"
    value: "0.16-0.23 over 0.4-6.3 keV_nr; Lindhard k=0.162(4)"
    source: "Bonhomme et al., EPJC 82, 815 (2022)"
    confidence: MEDIUM

open_questions:
  - question: "Local ambient-neutron flux normalization (indoor vs outdoor / building shielding) at the deployment"
    priority: HIGH
    blocks_phase: "Neutron Source Terms (P-NSRC)"
  - question: "Housing/materials U/Th/40K radiopurity budget (required user input)"
    priority: HIGH
    blocks_phase: "Detector Radioactivity Budget (P-RAD)"
  - question: "Ge surface-exposure/cool-down scenario (sets 3H/activation normalization; required user input)"
    priority: HIGH
    blocks_phase: "Cosmogenic Activation Inventory (P-COSMO)"
  - question: "Thin-wafer single/multiple-scatter and escape fraction spectral shape (a1 forward-peaking tail)"
    priority: MEDIUM
    blocks_phase: "Neutron Transport & Recoil Fold (P-NTRANS)"
  - question: "Reactor-correlated thermal-capture NR at 25 m unshielded (reactor on/off separable, unlike ambient)"
    priority: MEDIUM
    blocks_phase: "none"
  - question: "Muon-correlated vs uncorrelated neutron fraction at the surface (CONUS 80% is 24 m.w.e., not transferable)"
    priority: MEDIUM
    blocks_phase: "none"
  - question: "Low-Energy Excess below ~100 eV — modeled in-band floor is a lower bound only"
    priority: LOW
    blocks_phase: "none"

contradictions_unresolved:
  - claim_a: "Ge QF follows Lindhard with k=0.162 down through the sub-keV regime"
    claim_b: "Sub-keV QF is distorted by energy-scale non-linearity; Lindhard agreement is not established at the lowest recoils"
    source_a: "Bonhomme et al., EPJC 82, 815 (2022), arXiv:2202.03754"
    source_b: "Collar & Lewis, arXiv:2203.00750"
    investigation_needed: "Only load-bearing IF keV_ee NR numbers are imported and un-quenched near the CEvNS band; the keV_nr baseline avoids it. If un-quenching is used, propagate a QF(E) uncertainty band spanning both positions."
```
