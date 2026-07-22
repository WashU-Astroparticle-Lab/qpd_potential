# Phase 7: Scenario & Nuclear-Data Lock — Research

**Researched:** 2026-07-21
**Domain:** Low-background surface-detector physics — ambient/radiogenic neutron normalization, material radioassay, cosmogenic activation history, evaluated nuclear-data (ENDF) acquisition
**Depth:** deep
**Confidence:** HIGH on the physics framing, conventions, and the ENDF recipe; MEDIUM on the three absolute normalizations (input-gated by design, hence the mandated cited-default + band treatment)

> This is a **prerequisite setup phase**. It carries **no standalone CALC/SIMU/VALD requirement** but **gates CALC-05/06/07/08/09**. Its whole job is to lock provenance-tagged, axis-consistent, surface-appropriate inputs so every downstream fold starts from a defensible, cited baseline. The v1.1 literature survey (`GPD/literature/*.md`) is complete and web-verified; this file **consolidates and grounds** it into concrete Phase-7-ready values (defaults + bands + provenance + the ENDF recipe), it does **not** re-run the survey.

<user_constraints>

## User Constraints

**No `CONTEXT.md` file exists** for this phase (`gpd:discuss-phase` was not run). However, an explicit **USER DECISION (2026-07-21)** is recorded in the task scope and in `GPD/ROADMAP.md`/`GPD/REQUIREMENTS.md`, and it binds this phase:

### Locked Decisions (USER DECISION 2026-07-21)

- **The three external gating inputs are fixed as REPRESENTATIVE CITED DEFAULTS with an EXPLICIT UNCERTAINTY BAND** — reusing the v1.0 environmental-gamma "documented tunable input + provenance + band" pattern (see `data/gamma_lines.csv` header). Do **not** improvise a normalization; every fixed number is anchored to a citation and carries a band.
- **Unified phonon energy scale, NO ionization quenching** (`CONVENTIONS.md §B`). Every locked input carries a **keV_nr axis tag**; keVee↔keVnr mixing and any Lindhard/QF factor on the phonon scale are FORBIDDEN.
- **Surface deployment, no overburden**, near a 3 GW_th reactor at 25 m; ~110 g (4″×4″×2 mm) natural-Ge wafer, ~10,300 QPD sensors, both trapping designs (Ta→Al, Al→Hf).
- **Every flux/rate carries a (depth, shielding) provenance tag**; underground / post-shield residuals are non-transferable to the unshielded surface baseline.
- **ENDF/B-VIII.0** is the baseline n-Ge elastic evaluation; parse with `openmc.data` reading raw ENDF-6 text (avoid the multi-GB HDF5 library). No G4CMP/Geant4/MCNP.

### Agent's Discretion (recommend one, with a band)

- The specific numeric default **within** each cited range: outdoor-vs-indoor ambient-neutron anchor; the representative housing radiopurity scenario (optimistic electroformed-Cu vs realistic commercial); the exposure/cool-down times (`t_exp`, `t_cool`).
- Whether to carry EXPACS/PARMA and JEFF-3.3/ENDF-B-VIII.1 as optional cross-checks (recommended: yes, as sensitivity checks only).

### Deferred Ideas (OUT OF SCOPE this milestone)

- QPD sensor-film (Ta/Al/Hf) intrinsic radiopurity as a background source — housing/mount/nearby-components only this milestone.
- Reactor-correlated thermal-capture NR at 25 m (reactor-on/off separable; flagged as a deferred addend for Phase 12).
- Low-Energy Excess (LEE) below ~100 eV — unmodeled; the in-band floor is a lower bound.
- Building a NeuCBOT/SOURCES-4C (α,n) run (that is Phase 10 if tables are insufficient).

</user_constraints>

<active_anchor_references>

## Active Anchor References (contract-critical — mandatory inputs)

| Anchor | What Phase 7 must do with it | Downstream gate |
| --- | --- | --- |
| **Gordon et al., IEEE TNS 51, 3427 (2004)** | Fix the surface ambient fast-neutron φ(E_n) default + factor-of-a-few band; reconcile the ">10 MeV" (3.5×10⁻³) vs "broad thermal→GeV" (~1.3×10⁻²) labeling | CALC-05, CALC-06 |
| **ENDF/B-VIII.0 n-Ge elastic (70,72,73,74,76Ge; MF=3 MT=2, MF=4 MT=2)** | Acquire raw ENDF-6, parse with `openmc.data`, validate σ_el and λ≈5–6 cm, resonance-resolve on a union grid | CALC-06, CALC-08, VALD-05/06 |
| **MAJORANA electroformed-Cu <0.3 µBq/kg U/Th (OSTI 1481666)** + commercial-material assay budget | Optimistic ↔ pessimistic bracket for the housing radiopurity scenario | CALC-07, CALC-08 |
| **GERDA Ge-bulk ~µBq/kg U/Th (arXiv:1611.06884)** | Confirm intrinsic Ge radiogenic term is negligible (context, not a housing budget) | CALC-07/08 |
| **CDMSlite (arXiv:1806.07043) & EDELWEISS-III (arXiv:1607.04560)** production rates | Anchor the ³H/⁶⁸Ge/⁶⁵Zn activation band for the exposure/cool-down scenario | CALC-09, VALD-07 |
| **Mei–Zhang–Hime, NIMA 606, 651 (2009)** ²³⁸U SF = 1.353×10⁻¹¹ n/g/s/ppb + (α,n) tables | Radiogenic-neutron source budget per assumed assay | CALC-08, VALD-07 |
| **v1.0 `shared_energy_grid()`; `CONVENTIONS.md §B/§F`; `data/gamma_lines.csv` provenance-header pattern** | Bin edges, axis discipline, and the CSV provenance-header format every locked input must follow | all downstream |
| **NUCLEUS arXiv:2509.03559 (~250 dru, shielded lower bound)** | Not used in Phase 7; noted so the surface baseline is set as an *upper* case relative to it | VALD-08 (Phase 12) |

**Missing/ambiguous anchor flags:** (a) The *exact* Gordon analytic coefficient set (the JEDEC JESD89 lognormal-type fit valid above ~0.4 MeV) is **not** reproduced from memory here — it must be read from the paper / JESD89A at plan time (see Open Questions). (b) The specific deployment (bare-outdoor vs inside-reactor-building) is **not fixed by the user**; recommend outdoor sea-level as the default anchor with a downward building-shielding band (see below).

</active_anchor_references>

<research_summary>

## Summary

Phase 7 fixes four things before any fold: (1) the surface ambient fast-neutron flux, (2) the housing/materials U/Th/⁴⁰K radiopurity budget, (3) the Ge surface-exposure/cool-down scenario, and (4) the ENDF/B-VIII.0 n-Ge elastic cross sections. The first three are **input-gated normalizations** — they are not computed, they are chosen as representative cited defaults with an explicit band (the locked USER DECISION), each carrying a (depth, shielding)/(exposure history)/(material) provenance tag and a keV_nr axis tag. The fourth is a concrete data-acquisition-and-validation task with a mature, laptop-scale toolchain (`openmc.data` reading raw ENDF-6 text).

The physics content is light but the **bookkeeping discipline is the whole point**: the single sharpest hazard for the milestone is the keV_nr-vs-keV_ee axis confusion, and the second is importing shielded/underground residuals as the unshielded surface baseline. Both are guarded at the input-lock stage here. The recommended defaults are: **outdoor sea-level Gordon-2004** ambient neutron flux (Φ(>10 MeV)=3.5×10⁻³, broad thermal→GeV ~1.3×10⁻² cm⁻²s⁻¹) with a factor-of-a-few *downward* building-shielding band; a housing radiopurity **bracket** from electroformed-Cu (<0.3 µBq/kg U/Th, optimistic) to commercial Cu/steel/PCB (mBq–Bq/kg U/Th/⁴⁰K, pessimistic) with a stated representative middle; and a **t_exp = 1 yr sea-level exposure, t_cool = 0** activation scenario (continuously-surface detector) giving saturated ⁶⁸Ge/⁶⁵Zn and a linearly-growing, never-saturating ³H term.

**Primary recommendation:** Lock each of the three normalizations as a provenance-headed CSV/table entry in the `data/` convention (documented-tunable-input header, cited anchor, explicit band, keV_nr tag), acquire the 5 Ge ENDF-6 evaluations from NNDC and parse them with `openmc.data.IncidentNeutron.from_endf` / `AngleDistribution.from_endf` onto a union (native ∪ flux) grid, and validate against σ_el ≈ 3–7 b fast and Σ ≈ 0.18 cm⁻¹ → λ ≈ 5–6 cm → P_int ≈ 3.5% in 2 mm. If any gating input cannot be pinned to a defensible cited default + band, **block and request scope repair** (do not improvise a normalization).

</research_summary>

<literature_landscape>

## Literature Landscape

### Foundational Papers

| Paper | Authors | Year | Key Result | Relevance |
| --- | --- | --- | --- | --- |
| Measurement of the flux and energy spectrum of cosmic-ray induced neutrons on the ground (IEEE TNS 51, 3427) | Gordon, Goldhagen, Rodbell, Zabel, Tang, Clem, Bailey | 2004 | Sea-level cosmic-ray neutron spectrum meV→GeV; analytic fit above ~0.4 MeV; Φ(10 MeV–10 GeV)=3.6×10⁻³ cm⁻²s⁻¹ (NYC); altitude/geomagnetic/solar scaling | THE surface ambient-neutron anchor (input 1) |
| Evaluation of (α,n) induced neutrons as a background for dark matter experiments (NIMA 606, 651) | Mei, Zhang, Hime | 2009 | ²³⁸U SF yield 1.353×10⁻¹¹ n/g/s/ppb (material-independent); per-material (α,n) yields | Radiogenic-neutron source budget (input 2 → CALC-08) |
| Production Rate Measurement of Tritium and Other Cosmogenic Isotopes in Ge (Astropart. Phys. 105, 44) | Amman et al. (CDMSlite/SuperCDMS) | 2019 | Sea-level Ge production: ³H 74±9, ⁶⁵Zn 17±5, ⁶⁸Ge 30±18 atoms/kg/day | Activation-scenario anchor (input 3 → CALC-09) |
| Cosmogenic activation of Ge detectors in EDELWEISS-III (Astropart. Phys. 91, 51) | Armengaud et al. | 2017 | ³H 82±21, ⁶⁵Zn 106±13, ⁶⁸Ge >71 atoms/kg/day | Upper-band activation anchor (input 3) |
| ENDF/B-VIII.0 (Nucl. Data Sheets 148, 1; OSTI 1427384) | Brown et al. | 2018 | 8th major evaluated nuclear-data release; n-Ge elastic MF=3/MF=4 | THE n-Ge elastic evaluation (input 4) |
| Limits on U/Th bulk content in GERDA Phase-I detectors (arXiv:1611.06884) | Agostini et al. (GERDA) | 2017 | Ge bulk ²²⁶Ra/²²⁸Th/²²⁷Ac ≈ µBq/kg | Confirms intrinsic Ge radiogenic term negligible (input 2 context) |
| MAJORANA contamination-control & assay (OSTI 1481666) | MAJORANA Collab. | 2016 | Electroformed Cu <0.3 µBq/kg U and Th; commercial materials mBq–Bq/kg | Housing radiopurity bracket (input 2) |

### Recent Advances / Cross-checks

| Paper | Authors | Year | Key Result | Relevance |
| --- | --- | --- | --- | --- |
| NUCLEUS particle-background prediction (EPJC 86; arXiv:2509.03559) | NUCLEUS Collab. | 2026 | ~250 dru cosmic-neutron-dominated 10–100 eV residual at a shallow *shielded* site | Shielded lower bound; Phase-7 surface baseline is the *unshielded upper* case |
| ENDF/B-VIII.1 (arXiv:2511.03564) | Brown et al. | 2024 | Newest evaluation | Ge(n,el) sensitivity check only; NOT the baseline until Ge changes confirmed |
| PARMA/EXPACS (Sato) | Sato | 2015+ | Location-scaled ground-level neutron flux | Optional site altitude/geomagnetic scaling cross-check for Gordon |

### Notation Conventions Across Papers

| Quantity | Literature variants | Our (locked) convention | Notes |
| --- | --- | --- | --- |
| Neutron recoil energy | T, E_R, E_nr; keVnr in quenched detectors | **T ≡ E_nr = E_dep on the phonon scale (no QF)** | `CONVENTIONS.md §B`; keV_nr axis tag mandatory |
| Neutron flux | Φ (cm⁻²s⁻¹), φ(E_n) (cm⁻²s⁻¹MeV⁻¹); cm⁻²d⁻¹ | Φ, φ(E_n) in cm⁻²s⁻¹ (MeV⁻¹), Gordon native units | Tag (depth, shielding) |
| U/Th contamination | ppb (mass), Bq/kg, µBq/kg, g/g | **µBq/kg (assay) ↔ ppb (yield code)**: 1 ppb U ≈ 12.4 mBq/kg, 1 ppb Th ≈ 4.06 mBq/kg | Assay DBs quote Bq/kg; (α,n)/SF codes want ppb |
| ⁴⁰K | ppm K, Bq/kg | natural-K specific activity ≈ **31 Bq per g of natural K** → 1 ppm natural K ≈ 31 mBq/kg ⁴⁰K; γ branch p(1460.8 keV)=0.1067 | See Key Equations |
| Cosmogenic production | R (atoms/kg/day), saturation activity | isotope-specific **A(t)=R·N·(1−e^{−λt_exp})·e^{−λt_cool}**, never a blanket saturation | `CONVENTIONS.md`; Pitfall 5 |

**Key notational hazards:** (1) a keV_ee-quoted NR number placed on the phonon axis lands ~5× too low and mis-normalizes dR/dE by ~1/QF≈4–6× — tag every imported number's native axis. (2) "Saturation activity" is right for ⁶⁸Ge/⁶⁵Zn but wrong for ³H (never saturates). (3) A shielded residual (NUCLEUS/CONUS/RELICS) is not a surface flux.

</literature_landscape>

<methods_and_approaches>

## Methods and Approaches

This phase is **input-lock + data-acquisition**, so "methods" means (a) how to represent each normalization defensibly and (b) how to acquire/validate the ENDF data. The physics folds themselves are Phases 8–11.

### Input-Lock Method (the v1.0 "documented tunable input + band" pattern)

Each of the three normalizations becomes a **provenance-headed table entry** mirroring `data/gamma_lines.csv`:
- A header block stating: WHAT IS FIXED (cited value), WHAT IS TUNABLE/SITE-DEPENDENT (band + provenance), the (depth, shielding)/(material)/(exposure) tag, and the **keV_nr axis tag**.
- A single recommended default **and** an explicit band (lo/hi), each with its citation.
- A guard note mirroring `CONVENTIONS.md §B` FORBIDDEN list (no keVee/keVnr mixing, no Lindhard).

### ENDF Acquisition & Parse

| Step | Tool / call | Output |
| --- | --- | --- |
| Acquire raw ENDF-6 (5 Ge isotopes) | NNDC ENDF retrieval / IAEA-NDS (n-sublibrary, ENDF/B-VIII.0) | 5 ENDF-6 text files (~10–40 MB total) |
| Parse σ_el(E_n) (MF=3, MT=2) | `openmc.data.IncidentNeutron.from_endf(path)` → `inc.reactions[2].xs['0K']` (or 294K) | pointwise σ_el(E_n) per isotope |
| Parse CM angular dist (MF=4, MT=2) | `openmc.data.AngleDistribution.from_endf(...)` / via the parsed reaction product | Legendre a_ℓ(E_n) or tabulated μ_cm |
| Abundance-weight & union-grid | numpy on native ∪ flux grid | natural-Ge σ_el(E_n), a₁(E_n) CSV |

**Isotopic abundances (natural Ge):** ⁷⁰Ge 20.57%, ⁷²Ge 27.45%, ⁷³Ge 7.75%, ⁷⁴Ge 36.50%, ⁷⁶Ge 7.73% (IUPAC). These weight the per-isotope σ_el into the natural-Ge macroscopic cross section. `openmc.data` reads the MAT number from the file header — do **not** hardcode MAT.

### Computational Tools

| Tool/Package | Version | Purpose | Why Standard |
| --- | --- | --- | --- |
| `openmc.data` | 0.15.x | Pure-Python ENDF MF=3/MF=4 reader (`IncidentNeutron.from_endf`, `AngleDistribution.from_endf`) | Reads raw ENDF-6 text; no NJOY, no multi-GB HDF5 library needed for File 3/4 |
| numpy / scipy | ≥1.26 / ≥1.11 | Abundance weighting, union-grid interpolation, integral checks | Reuse v1.0 stack |
| pandas | existing | Provenance-headed CSV I/O (matches `src/flux/build_flux_table.py`) | Same role as v1.0 |

### Supporting / Cross-check Tools

| Tool | Version | Purpose | When to use |
| --- | --- | --- | --- |
| `sandy` | latest PyPI | ENDF-6 → pandas; covariance sampling | If `openmc.data` mis-parses a File-4 section, or uncertainty bands wanted |
| ENDFtk | conda-forge `endftk` | Low-level ENDF-6 read mirroring the Formats Manual | Deep ENDF surgery / non-standard MT |
| JEFF-3.3 | — | Independent σ_el cross-check | Sensitivity: discrepancies below ~1 MeV expected small |
| ENDF/B-VIII.1 | 2024 | Newest evaluation | Sensitivity check only; confirm whether Ge(n,el) changed vs VIII.0 |
| EXPACS/PARMA | PARMA-4.0 | Site altitude/geomagnetic/solar scaling of the ground-level neutron flux | Optional cross-check of the Gordon default for the actual site |

### Package / Framework Reuse Decision

**Use existing packages directly; no bespoke ENDF parser.** `openmc.data` is a mature, pure-Python ENDF-6 File-3/File-4 reader that covers exactly this need (σ_el + CM angular distributions) without NJOY or the processed HDF5 cross-section library. Build-time only — it is **not** made a runtime dependency; the deliverable is provenance-headed CSVs committed to `data/`, consumed downstream by the v1.0 numpy/scipy pipeline. The **only** bespoke code in Phase 7 is thin glue: abundance-weighting, union-grid interpolation, and the provenance-header writer (which already has a template in `src/flux/build_flux_table.py` / `data/gamma_lines.csv`). The two-body kinematics recoil-kernel transform is **deferred to Phase 9** (CALC-06), not built here. No missing capability justifies new heavy code.

**Installation:**

```bash
# build-time only (ENDF -> CSV extraction); not a runtime dep
pip install openmc            # or conda-forge; provides openmc.data
# fallbacks if needed:
pip install sandy             # ENDF-6 -> pandas
# conda install -c conda-forge endftk
```

</methods_and_approaches>

<known_results>

## Known Results and Benchmarks — the concrete Phase-7 defaults + bands

### Input 1 — Surface ambient fast-neutron normalization (feeds CALC-05/06)

**Labeling reconciliation (resolved, web-verified):** the two Gordon integrals are over **different energy ranges of the same spectrum**, not a discrepancy:
- **Φ(>10 MeV) = 3.5×10⁻³ cm⁻²s⁻¹** (equivalently 3.6×10⁻³ over 10 MeV–10 GeV, NYC, mid-solar). This is the "fast/high-energy" integral.
- **Φ_broad(thermal→GeV) ≈ 1.3×10⁻² cm⁻²s⁻¹** — the total over the whole meV→GeV spectrum (thermal peak + epithermal 1/E + evaporation + cascade). METHODS.md at one point labeled this ">1 MeV"; the correct label is **broad thermal→GeV total**. The fold uses the full differential φ(E_n), so both are just integral cross-checks over different ranges (VALD-07 uses the >10 MeV number).

| Field | Recommended default | Band | Provenance tag |
| --- | --- | --- | --- |
| Ambient φ(E_n) | Gordon-2004 sea-level NYC, mid-solar, **outdoor, no overburden**; full meV→GeV differential | **Factor-of-a-few DOWNWARD** for indoor/building shielding: ~[Gordon/5, Gordon] (building roof/walls attenuate + moderate the fast flux); modest UPWARD via altitude/geomagnetic scaling if the site differs from sea-level NYC | (depth = surface / 0 m.w.e.; shielding = none-outdoor **or** building-attenuated; site = sea-level NYC reference) |
| Φ(>10 MeV) check | 3.5×10⁻³ cm⁻²s⁻¹ | 3.5–3.6×10⁻³ | VALD-07 anchor |
| Φ_broad check | ~1.3×10⁻² cm⁻²s⁻¹ | site/altitude/solar dependent | integral cross-check |

**Spectral shape / how to represent φ(E_n):** Gordon provides an **analytic fit valid above ~0.4 MeV** (JEDEC JESD89 lognormal-type functional form) plus a tabulated spectrum down to thermal. Recommendation: represent φ(E_n) as the digitized/parametrized full spectrum on `shared_energy_grid()` — thermal (Maxwellian peak ~25 meV), epithermal (~1/E), evaporation (~1–2 MeV lognormal hump), and the high-energy cascade tail. Commit as a provenance-headed CSV. **Do not fabricate the analytic coefficients from memory** — extract them from the paper / JESD89A at plan time (Open Question 1). EXPACS/PARMA is an optional site-scaling cross-check only.

### Input 2 — Housing/materials U/Th/⁴⁰K radiopurity budget (γ → CALC-07; (α,n)+SF → CALC-08)

Ge **bulk** intrinsic term is negligible (GERDA µBq/kg) and is **not** the housing budget. The housing/mount/nearby-components budget is a **bracket**:

| Scenario | U (²³⁸U) | Th (²³²Th) | ⁴⁰K | Source / provenance |
| --- | --- | --- | --- | --- |
| **Optimistic** (electroformed Cu) | <0.3 µBq/kg (<0.024 ppb) | <0.3 µBq/kg (<0.074 ppb) | low | MAJORANA, OSTI 1481666 |
| **Realistic/pessimistic** (commercial Cu / stainless / PCB / connectors) | ~mBq–Bq/kg (~0.1–100 ppb) | ~mBq–Bq/kg (~0.2–250 ppb) | ~mBq–Bq/kg | radioassay DBs (ILIAS/SNOLAB); MAJORANA |
| **Recommended representative default** | commercial OFHC Cu ~ tens of µBq/kg–~mBq/kg U/Th, with a PCB/connector sub-budget at mBq/kg, band spanning the full bracket above | — | state ⁴⁰K per component | pick a cited assay-DB value; carry the bracket as the band |

**ppb ↔ activity conversions (record in the header):**
- 1 ppb U (nat, secular eq) ≈ **12.4 mBq/kg**; 1 ppb Th ≈ **4.06 mBq/kg**.
- ⁴⁰K: natural-K specific activity ≈ **31 Bq per g of natural K** ⇒ 1 ppm natural K ≈ **31 mBq/kg** of ⁴⁰K activity; γ line 1460.8 keV with p_γ = **0.1067** per decay (the rest is β⁻/EC without the 1460 γ).

**Split the budget by channel (load-bearing):**
- **γ-emitting external budget → CALC-07:** U/Th chain γ lines (e.g. ²¹⁴Bi 609/1120/1764 keV, ²⁰⁸Tl 2615 keV) + ⁴⁰K 1461 keV → Compton continuum in the thin wafer (peaks escape). Needs activity × (Ω/4π) × self-absorption × path-attenuation × wafer thin-target μt.
- **(α,n)+SF neutron source budget → CALC-08:** same U/Th ppb → per-material (α,n) yield (low-Z content dominates; pure Ge ≈ nothing) + ²³⁸U SF 1.353×10⁻¹¹ n/g/s/ppb (⟨E_n⟩≈2 MeV Watt).

### Input 3 — Ge surface-exposure / cool-down scenario (feeds CALC-09/Phase 11)

**Production rates (sea level):** ³H 74±9 (CDMSlite) / 82±21 (EDELWEISS); ⁶⁵Zn 17±5 / 106±13; ⁶⁸Ge 30±18 / >71 atoms/kg/day. **Half-lives:** ³H 12.32 yr (Q=18.6 keV, β⁻, never saturates); ⁶⁸Ge 270.8 d (→⁶⁸Ga, EC); ⁶⁵Zn 243.9 d (EC).

**Recommended default scenario:** **t_exp = 1 yr** sea-level exposure (fabrication + storage + surface deployment), **t_cool = 0** (continuously-operating surface detector — no underground cool-down; this is the appropriate/worst-case surface framing). **Band:** t_exp ∈ [~0.25 yr (fresh, quick-deploy) … ~3 yr (aged at surface)]; CDMSlite rates central, EDELWEISS as the upper band.

**Resulting as-deployed activity band** (via A = R·(1−e^{−λ t_exp}), t_cool=0; per kg):

| Isotope | Behavior | A at t_exp = 1 yr (CDMSlite R) | Band (0.25–3 yr; +EDELWEISS upper) |
| --- | --- | --- | --- |
| ³H | **never saturates**, A ∝ ~linear in t_exp | ~4.1 decays/kg/day (2.4×10⁻⁵ Bq/kg·... see note) | ~1.0–13 decays/kg/day (up to ~14 with EDELWEISS R=82) |
| ⁶⁸Ge | saturates (~1 yr), A→R | ~30 decays/kg/day (≈3.5×10⁻⁴ Bq/kg) | ~26–71 decays/kg/day |
| ⁶⁵Zn | saturates (~1 yr), A→R | ~17 decays/kg/day (≈2.0×10⁻⁴ Bq/kg) | ~15–106 decays/kg/day |

(³H numeric: A = 74 × (1−e^{−0.0563·1}) = 74 × 0.0548 ≈ **4.1 decays/kg/day** at 1 yr; at 3 yr ≈ 11.5; grows ~linearly.) The ³H β continuum (0→18.6 keV) then carries an average in-band ER density of order **~0.2–0.6 dru** (≈ 4–12 decays/kg/day ÷ 18.6 keV), the headline in-band ER background with no line to subtract.

### Input 4 — ENDF/B-VIII.0 n-Ge elastic (feeds CALC-06/08, VALD-05/06)

| Quantity | Value/expression | Conditions | Source | Confidence |
| --- | --- | --- | --- | --- |
| Max recoil fraction | T_max/E_n = 4A/(1+A)² = **0.0538** (A=72.6) | natural Ge; per isotope 0.0555 (⁷⁰) → 0.0513 (⁷⁶) | two-body kinematics | HIGH |
| Fast elastic σ_el | ~**3–7 b** across the fast band | E_n ~ 0.1–10 MeV | ENDF/B-VIII.0 | HIGH |
| Macroscopic Σ / mfp | Σ = N_Ge σ_tot ≈ **0.18 cm⁻¹** ⇒ λ ≈ **5.6 cm** | N_Ge = 4.41×10²² cm⁻³, σ_tot ≈ 4 b fast | derived; cross-file consistent | HIGH |
| Interaction prob in 2 mm | P_int = 1−e^{−Σt} ≈ **3.5%** (t=0.2 cm) | thin-target single-scatter regime | derived | HIGH |
| Sub-MeV resonances | resolved elastic resonances below ~1 MeV | must integrate on **native ∪ flux** union grid | ENDF; COMPUTATIONAL.md | HIGH |

**Acquisition source/URL (concrete):** ENDF/B-VIII.0 neutron sublibrary evaluations for ⁷⁰,⁷²,⁷³,⁷⁴,⁷⁶Ge from the **NNDC ENDF retrieval / Sigma interface** (`https://www.nndc.bnl.gov/endf/`, Sigma at `https://www.nndc.bnl.gov/sigma/`) or **IAEA-NDS** (`https://www-nds.iaea.org/`). Download the 5 individual ENDF-6 text files (n + Ge-xx). The OpenMC ENDF/B-VIII.0 tarball (`https://openmc.org/data/`, Zenodo 8410375) also contains the raw evaluations — use the raw ENDF, **not** the processed multi-GB HDF5 library.

### Limiting Cases (guardrails)

| Limit | Expected behavior | Source |
| --- | --- | --- |
| Deep underground | ambient atmospheric neutrons negligible; radiogenic/µ-induced dominate — **DO NOT transfer** | Mei & Hime PRD 73, 053004 (2006) |
| U/Th → 0 in materials | radiogenic (α,n)+SF → 0; Ge bulk already µBq/kg | Mei–Zhang–Hime linear scaling |
| t_exp → 0 (no exposure) | activation → 0 (unphysical for surface; lower bound) | EDELWEISS/CDMSlite scaling |
| t_exp → ∞ | ⁶⁸Ge/⁶⁵Zn saturate; ³H keeps growing | A(t) Bateman |

</known_results>

<dont_rederive>

## Don't Re-derive

| Problem | Don't derive from scratch | Use instead | Why |
| --- | --- | --- | --- |
| Sea-level cosmic-ray neutron spectrum | Do NOT build a cosmic-ray cascade/EXPACS transport from scratch | Gordon-2004 parametrization (digitize/parametrize); optional EXPACS cross-check | Peer-reviewed, ~2% fit, web-verified integrals; re-deriving invites normalization errors |
| Ge cosmogenic production rates | Do NOT run ACTIVIA/Geant4+CRY to get R | CDMSlite/EDELWEISS measured R (atoms/kg/day) | Direct measurements exist and are the anchors; simulate only as a cross-check |
| ²³⁸U SF neutron yield | Do NOT recompute the SF branching/yield | 1.353×10⁻¹¹ n/g/s/ppb (Mei–Zhang–Hime), material-independent | Standard, material-independent constant |
| ppb↔activity, ⁴⁰K specific activity | Do NOT re-derive from half-lives each time | 1 ppb U ≈ 12.4 mBq/kg; 1 ppb Th ≈ 4.06 mBq/kg; ~31 Bq/g nat-K | Standard radioassay conversions; record once in the header |
| n-Ge elastic σ and angular dist | Do NOT hand-model resonances or optical-model σ | ENDF/B-VIII.0 via `openmc.data` | Evaluated, benchmarked nuclear data; parsing is a solved problem |
| ENDF-6 File-3/File-4 parsing | Do NOT write a bespoke ENDF reader | `openmc.data.IncidentNeutron.from_endf` / `AngleDistribution.from_endf` | Mature pure-Python reader; sandy/ENDFtk as fallbacks |

**Key insight:** every Phase-7 number is either a cited measurement or a standard conversion. The error-prone step is **transcription + tagging** (axis, depth/shielding, exposure, material), not derivation. Lock provenance, don't recompute.

</dont_rederive>

<common_pitfalls>

## Common Pitfalls (Phase-7-specific; full catalog in `GPD/literature/PITFALLS.md`)

### Pitfall 1: keV_ee imported onto the phonon (keV_nr = E_dep) axis, or "helpfully" applying Lindhard

**What goes wrong:** A neutron-NR background quoted in keV_ee (already ×QF≈0.16–0.23) treated as the phonon E_dep axis lands ~5× too low and mis-normalizes dR/dE by ~1/QF≈4–6×; the mirror error applies Lindhard to a keV_nr number and suppresses the rate ~5–7×.
**Why it happens:** most transferable Ge numbers are quoted quenched because real Ge detectors measure charge; the "recoil→apply QF" reflex is backwards on a fieldless phonon calorimeter.
**How to avoid:** tag every locked input's native axis; transfer NR on keV_nr = E_dep (no QF); un-quench any keV_ee import with the Jacobian and a documented QF(E) band. Add a guard mirroring `CONVENTIONS.md §B` FORBIDDEN list.
**Warning signs:** any locked number multiplied by a 0.1–0.3 "quenching" factor; an NR background peaking ~5× low.

### Pitfall 2: Surface-vs-underground / shielded-residual import

**What goes wrong:** importing NUCLEUS ~250 dru, CONUS sub-keV, or RELICS residuals as the *unshielded surface* rate under-counts by orders of magnitude (they are post-shield residuals).
**Why it happens:** most CEvNS/DM literature is written for shielded, deep experiments.
**How to avoid:** tag every flux/rate with (depth, shielding); the surface baseline uses raw Gordon/sea-level with NO shielding factor; treat NUCLEUS/CONUS/RELICS as back-corrected cross-checks only (VALD-08 direction check, Phase 12).
**Warning signs:** a locked flux matching an underground residual to order unity; a "shielding suppression factor" with no shield in the geometry.

### Pitfall 3: Saturation activity quoted for ³H (history-dependence)

**What goes wrong:** using a single saturation activity for all cosmogenic isotopes overstates ³H, which never saturates (12.3 yr) and grows ~linearly with exposure.
**Why it happens:** activation is usually tabulated as production rate or saturation activity for convenience.
**How to avoid:** state explicit t_exp/t_cool; compute each isotope with its own λ; carry ³H as exposure-time-dependent (⁶⁸Ge/⁶⁵Zn saturate).
**Warning signs:** the cosmogenic background is independent of the stated exposure time; one "saturation" number used for ³H.

### Pitfall 4: Generic (α,n) yield across the whole stack; and Ge "self-shielding" reflex

**What goes wrong:** a single (α,n) yield per ppb is wrong by large factors (low-Z content and thin-film α-escape dominate; pure Ge ≈ nothing). Separately, "Ge self-shields its γ" is a thick-crystal reflex — 2 mm is optically thin to MeV γ.
**How to avoid (Phase 7 part):** lock the U/Th assay **per material/component** so Phase 10 can compute (α,n) per material; record which components are low-Z. Keep the γ (CALC-07) and neutron (CALC-08) budgets split.
**Warning signs:** one (α,n) number for the whole detector; the housing budget not broken out by component.

### Pitfall 5 (numerical): under-resolved sub-MeV Ge(n,el) resonances

**What goes wrong:** integrating σ_el(E_n)×φ(E_n) on a coarse fixed mesh misses sharp elastic resonances below ~1 MeV, biasing the interaction rate.
**How to avoid:** build σ_el on the **union of the ENDF native energy grid and the flux grid**; check that halving the internal mesh changes the total rate <0.5%.
**Warning signs:** rate shifts when the mesh is refined; visibly clipped resonance peaks.

</common_pitfalls>

<key_derivations>

## Key Equations and Starting Points

### Cosmogenic activity (as-deployed, isotope-specific)

```
# Source: Bateman; CONVENTIONS.md; PITFALLS.md Pitfall 5
A(t) = R · N_target · (1 - e^{-λ t_exp}) · e^{-λ t_cool}
     = R · (1 - e^{-λ t_exp}) · e^{-λ t_cool}     [per kg, since A = λN and dN/dt = R - λN]
λ = ln2 / t_half
# 3H: λ = 0.0563/yr  -> A(1 yr) = 74 * 0.0548 ≈ 4.1 decays/kg/day (never saturates)
# 68Ge, 65Zn: t_half ~ 271/244 d -> saturate (A -> R) within ~1 yr
```
**Valid when:** constant sea-level production over t_exp; t_cool the shielded/underground interval before running. **Breaks down when:** variable altitude/exposure history (use a piecewise R).

### Neutron elastic recoil kinematics (endpoint check for VALD-05)

```
# Source: two-body kinematics; METHODS.md
T = [2A/(1+A)^2] · (1 - cosθ_cm) · E_n ;  T_max = 4A/(1+A)^2 · E_n
# natural Ge (A=72.6): T_max/E_n = 0.0538 ; per isotope 0.0555 (70Ge) ... 0.0513 (76Ge)
```
**Valid:** elastic two-body. **Note:** the flat-box kernel dσ/dT = σ_el/T_max (isotropic CM) and the a₁ forward-peaking correction are **Phase 9**, not built here.

### Thin-target interaction length (sanity check for VALD-06)

```
# Source: COMPUTATIONAL.md; N_Ge = 4.41e22 cm^-3
Σ = N_Ge · σ_tot ≈ 4.41e22 · 4e-24 ≈ 0.18 cm^-1
λ = 1/Σ ≈ 5.6 cm  (>> 0.2 cm wafer)
P_int(2 mm) = 1 - e^{-Σ t} = 1 - e^{-0.036} ≈ 3.5%   (multiple-scatter <~1%)
```
**Valid:** fast neutrons, thin wafer. **Breaks down:** thermal capture / thick targets.

### ppb ↔ activity conversions (record in every radiopurity header)

```
1 ppb U (nat, secular eq) ≈ 12.4 mBq/kg
1 ppb Th (nat, secular eq) ≈ 4.06 mBq/kg
nat-K specific activity ≈ 31 Bq / g(K)  ->  1 ppm nat-K ≈ 31 mBq/kg of 40K
40K gamma: E = 1460.8 keV, p_gamma = 0.1067 per decay
238U SF neutron yield = 1.353e-11 n/g/s per ppb U  (material-independent; <E_n> ~ 2 MeV Watt)
```

</key_derivations>

<validation_strategies>

## Validation Strategies (what makes Phase 7 "done")

| Locked input | Validation check | Benchmark | Pass criterion |
| --- | --- | --- | --- |
| Ambient φ(E_n) | Integrate the digitized spectrum | Gordon Φ(>10 MeV)=3.5×10⁻³; broad ~1.3×10⁻² cm⁻²s⁻¹ | within cited precision; (depth,shielding) tag present; ">10 MeV" vs "broad" labels reconciled |
| Radiopurity budget | Round-trip ppb↔µBq/kg; bracket spans optimistic↔pessimistic | 1 ppb U=12.4 mBq/kg; Cu <0.3 µBq/kg ↔ mBq–Bq/kg | conversions correct; γ (CALC-07) and (α,n)+SF (CALC-08) budgets split; per-component |
| Exposure/cool-down | A(t) per isotope with its own λ | CDMSlite/EDELWEISS R; ⁶⁸Ge/⁶⁵Zn saturate, ³H linear | ³H shown non-saturating; as-deployed (not saturation) activity band quoted |
| ENDF σ_el | `openmc.data`-parsed σ_el vs NNDC Sigma plot + sandy/ENDFtk spot-check | ENDF/B-VIII.0 pointwise σ_el; fast ~3–7 b | curves match; resonances resolved on union grid |
| ENDF kinematics | endpoint per isotope | T_max/E_n = 4A/(1+A)² = 0.0538 (nat) | reproduced per isotope (VALD-05 pre-check) |
| ENDF mfp | Σ = N_Ge σ_tot | Σ ≈ 0.18 cm⁻¹, λ ≈ 5–6 cm, P_int ≈ 3.5% | matches; thin-target regime confirmed (VALD-06 pre-check) |
| ENDF sensitivity | JEFF-3.3 and/or ENDF/B-VIII.1 σ_el | cross-library agreement below ~1 MeV | discrepancies small / documented |
| Axis discipline | grep the locked tables for any QF/Lindhard/keVee | `CONVENTIONS.md §B` FORBIDDEN list | every input keV_nr-tagged; no quenching anywhere |
| Grid consistency | assert bin edges vs `shared_energy_grid()` | v1.0 grid (~584 log bins, 0.01 keV→197 MeV) | committed tables bin-compatible |

</validation_strategies>

<existing_results_to_leverage>

## Existing Results to Leverage (cite, don't re-derive)

- **Gordon-2004** sea-level flux + integrals (web-verified) — the ambient default.
- **CDMSlite/EDELWEISS-III** measured production rates — the activation band.
- **Mei–Zhang–Hime** ²³⁸U SF constant + (α,n) tables — the radiogenic-neutron budget.
- **MAJORANA electroformed-Cu / GERDA Ge-bulk** assays — the radiopurity bracket.
- **ENDF/B-VIII.0** evaluated n-Ge elastic — the cross-section data.
- **v1.0 repo:** `shared_energy_grid()` (`src/qpd_potential/muon_deposit.py`), the `data/gamma_lines.csv` provenance-header pattern, `src/flux/build_flux_table.py` CSV writer, `CONVENTIONS.md §B/§D/§F`. Reuse verbatim.

</existing_results_to_leverage>

<open_questions>

## Open Questions

1. **Exact Gordon analytic coefficient set (φ(E_n) above ~0.4 MeV).**
   - Know: the fit exists (JEDEC JESD89 lognormal-type), integrals are web-verified (3.5×10⁻³ >10 MeV; ~1.3×10⁻² broad).
   - Unclear: the numeric coefficients are not reproduced from memory here (would be fabrication).
   - Recommendation: at plan time, read the coefficients from the Gordon paper / JESD89A (or digitize the published spectrum) and commit them with the citation in the CSV header.

2. **Actual deployment: bare-outdoor vs inside-reactor-building.** Sets the ambient-neutron default within the factor-of-a-few band.
   - Recommendation: default to outdoor sea-level (upper anchor) with a downward building-shielding band; if the user later fixes the site, narrow the band.

3. **Representative housing composition / assay.** The (α,n) budget depends on the low-Z content per component, unknown until a materials list exists.
   - Recommendation: lock the electroformed-Cu↔commercial bracket now; flag a NeuCBOT/SOURCES-4C cross-check for Phase 10 if tables are insufficient.

4. **Whether ENDF/B-VIII.1 changes the Ge(n,el) evaluations.**
   - Recommendation: baseline on VIII.0; run VIII.1 (and JEFF-3.3) as a documented sensitivity check, not the anchor.

</open_questions>

<not_found>

## What Was NOT Found

- The **exact Gordon-2004 analytic parametrization coefficients** — web results confirmed the integrals and that an analytic fit exists above ~0.4 MeV, but did not surface the coefficient table (behind the IEEE paywall / in JESD89A). Deliberately NOT reconstructed from memory. (Sources checked: ResearchGate PDF, NASA/ADS, Semantic Scholar.)
- **Per-isotope ENDF/B-VIII.0 Ge(n,el) thermal cross-section values** in barns — general web search did not return the pointwise numbers; they must be read from the parsed evaluation / NNDC Sigma at implementation time. The fast-band ~3–7 b range and the Σ≈0.18 cm⁻¹ / λ≈5–6 cm sanity check are the validated anchors.
- A published **surface (unshielded) in-band NR dru** number to validate against directly — only shielded lower bounds exist (NUCLEUS ~250 dru); the surface baseline is expected above it (VALD-08 is a direction check, Phase 12).

</not_found>

<caveats_and_alternatives>

## Caveats and Alternatives (adversarial self-critique)

**Am I over-trusting the "cited default + band" framing to launder input uncertainty?** Partly — the band is genuine but the *shape* of the ambient φ(E_n) inside the building is not just a scalar factor (roof moderation reshapes the spectrum, shifting the evaporation hump). A pure scalar-factor band understates a spectral-shape systematic. Mitigation: default outdoor (unmoderated) and flag the indoor spectral reshaping as a Phase-8/12 sensitivity rather than pretending a single factor captures it.

**Is t_cool = 0 defensible?** For a continuously-operating surface detector it is the correct/worst-case framing (no underground cool-down), but a real device spends time shielded during fabrication/transport. t_cool=0 is conservative (maximizes short-lived ⁶⁸Ge/⁶⁵Zn); it does not bias ³H much (12.3 yr). Acceptable as default; carry t_cool as a tunable.

**Could the housing bracket be so wide (µBq/kg → Bq/kg, ~6 orders) as to be useless?** Yes if left unresolved — a 6-order bracket makes CALC-07/08 non-predictive. The recommended representative middle (commercial OFHC Cu ~tens-µBq–mBq/kg with a PCB sub-budget) narrows it to a factor of ~10–100; the extremes are kept only as documented bounds. The planner should force a single representative default, not just the bracket.

**Am I sure the two Gordon integrals are just range labels, not a real discrepancy?** Web-verified: 3.5–3.6×10⁻³ is 10 MeV–10 GeV; ~1.3×10⁻² is the broad thermal→GeV total. HIGH confidence. The residual risk is a unit/range slip when digitizing — the VALD-07 >10 MeV check catches it.

**ENDF parsing risk:** `openmc.data` occasionally mis-parses non-standard File-4 sections. Mitigation: sandy/ENDFtk fallback and a σ_el spot-check vs NNDC Sigma. LOW risk for Ge (standard evaluation).

**Biggest residual weakness:** the ambient-neutron absolute normalization (factor-of-a-few, site-dependent) is the single largest input uncertainty and is only checkable against the Gordon integral + a shielded peer lower bound — it is **input-limited, not method-limited**. This is inherent to the milestone and is exactly why the cited-default+band treatment (not a single number) is mandated.

**Unresolved tradeoff:** representing φ(E_n) as a committed static CSV (reproducible, reviewable) vs an EXPACS/PARMA live-scaled spectrum (site-accurate). Recommendation: static Gordon CSV as baseline (matches the v1.0 `data/` pattern), EXPACS as an optional documented cross-check — do not add a live dependency.

</caveats_and_alternatives>

<sources>

## Sources

### Primary (HIGH)

- Gordon et al., IEEE TNS 51, 3427 (2004) — sea-level cosmic-ray neutron flux; integrals web-verified (3.5–3.6×10⁻³ >10 MeV, ~1.3×10⁻² broad). https://ui.adsabs.harvard.edu/abs/2004ITNS...51.3427G/abstract
- Amman et al. (CDMSlite), Astropart. Phys. 105, 44 (2019), arXiv:1806.07043 — Ge ³H/⁶⁵Zn/⁶⁸Ge production.
- Armengaud et al. (EDELWEISS-III), Astropart. Phys. 91, 51 (2017), arXiv:1607.04560 — upper-band Ge activation.
- Mei, Zhang & Hime, NIMA 606, 651 (2009), arXiv:0812.4307 — ²³⁸U SF 1.353×10⁻¹¹ n/g/s/ppb + (α,n) tables.
- Brown et al., ENDF/B-VIII.0, Nucl. Data Sheets 148, 1 (2018), OSTI 1427384 — n-Ge elastic evaluation. https://www.osti.gov/pages/biblio/1427384
- Agostini et al. (GERDA), Astropart. Phys. 91, 15 (2017), arXiv:1611.06884 — Ge bulk µBq/kg U/Th.
- MAJORANA contamination-control & assay, OSTI 1481666 — electroformed-Cu <0.3 µBq/kg U/Th.
- `GPD/CONVENTIONS.md §B/§D/§F`; `data/gamma_lines.csv` header; `src/qpd_potential/muon_deposit.py::shared_energy_grid` — internal authoritative references.

### Secondary (MEDIUM)

- `openmc.data` docs — `IncidentNeutron.from_endf`, `AngleDistribution.from_endf`. https://docs.openmc.org/en/stable/pythonapi/generated/openmc.data.IncidentNeutron.html
- NNDC ENDF retrieval / Sigma — https://www.nndc.bnl.gov/endf/ , https://www.nndc.bnl.gov/sigma/ ; IAEA-NDS https://www-nds.iaea.org/ ; OpenMC data https://openmc.org/data/ (Zenodo 8410375).
- NUCLEUS Collab., EPJC 86 (2026), arXiv:2509.03559 — ~250 dru shielded lower bound (Phase 12 cross-check).
- sandy (Fiorito), ENDFtk (njoy), JEFF-3.3, PARMA/EXPACS (Sato) — fallback/cross-check tools.
- v1.1 project literature: `GPD/literature/{SUMMARY,PRIOR-WORK,METHODS,COMPUTATIONAL,PITFALLS}.md` — the completed survey this file consolidates.

### Tertiary (LOW / flags)

- ENDF/B-VIII.1 (2024), arXiv:2511.03564 — Ge(n,el) sensitivity check only.
- Gordon analytic coefficient set / JEDEC JESD89A — cited but not reproduced here (must be read at plan time; see What Was NOT Found).
- ⁴⁰K specific activity ~31 Bq/g(K) — standard textbook value; double-check the exact figure at plan time.

</sources>

<metadata>

## Metadata

**Research scope:**
- Physics subfield: surface low-background detector inputs — ambient/radiogenic neutron normalization, material radioassay, cosmogenic activation history, ENDF acquisition.
- Methods explored: cited-default+band input-lock pattern; `openmc.data` ENDF-6 MF=3/MF=4 parsing; A(t) Bateman; ppb↔activity conversions.
- Known results catalogued: Gordon integrals, CDMSlite/EDELWEISS rates, MZH SF yield, Cu/Ge assays, T_max/E_n=0.0538, Σ≈0.18 cm⁻¹.
- Pitfalls: keV_nr/keV_ee axis, surface-vs-underground, ³H non-saturation, per-material (α,n), sub-MeV resonance resolution.

**Confidence breakdown:**
- Literature coverage: HIGH — complete web-verified v1.1 survey consolidated.
- Methods (ENDF recipe): HIGH — mature `openmc.data` path, cross-file consistent.
- Known results (defaults): HIGH on the cited values; MEDIUM on the absolute normalization choice within each band (input-gated by design).
- Pitfalls/conventions: HIGH — grounded in `CONVENTIONS.md §B/§F` + PITFALLS.md.

**Research date:** 2026-07-21
**Valid until:** 2026-08-20 (30 days — established nuclear data + peer-reviewed anchors; ENDF/B-VIII.1 sensitivity is the only moving piece)

</metadata>

---

_Phase: 07-scenario-nuclear-data-lock_
_Research completed: 2026-07-21_
_Ready for planning: yes_
