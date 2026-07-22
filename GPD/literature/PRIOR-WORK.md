# Prior Work: Neutron-Induced Nuclear Recoils and Detector-Material Radiogenic Backgrounds for a Surface Ge CEvNS Detector

**Surveyed:** 2026-07-21
**Domain:** Low-background detector physics — cosmogenic and radiogenic neutron backgrounds, cosmogenic activation, and material radioassay for surface-deployed cryogenic/Ge CEvNS experiments
**Confidence:** HIGH overall (each entry carries its own level; DERIVED estimates are labeled)

**Milestone this survey serves (v1.1):** extends the v1.0 QPD-Ge forward model to the *in-band* (CEvNS-band) background budget from neutron-induced nuclear recoils and detector-material radioactivity, on the **unified phonon energy scale (no ionization quenching)**, for a ~110 g single-sided natural-Ge wafer, **SURFACE deployment (no overburden)**, 25 m from a 3 GW_th reactor. Analytic / Monte-Carlo response chain only — no G4CMP.

**The single most important framing fact for v1.1:** On the QPD unified phonon scale there is **no keVnr/keVee distinction**. A fast neutron that elastically scatters off a Ge nucleus deposits its full recoil energy `T` as phonons and lands on the *same axis* as a CEvNS recoil of energy `T`. Neutron elastic scattering in Ge is therefore an **irreducible, kinematically-identical in-band background** to the CEvNS signal — the defining background of this milestone. Electron-recoil backgrounds (betas, gammas, activation X-rays) also land on the same phonon axis but with a different spectral shape (this is the v1.0 Compton channel generalized).

---

## Key Results

| Result | Expression / Value | Conditions | Source | Year | Confidence |
| --- | --- | --- | --- | --- | --- |
| Sea-level cosmic-ray fast-neutron flux (>10 MeV) | Φ_n(>10 MeV) = 3.50×10⁻³ cm⁻² s⁻¹ | Sea level, NYC, mid solar modulation, outdoor, no overburden; two-lognormal spectral parameterization φ(E) valid thermal→GeV | Gordon et al., IEEE TNS 51, 3427 (2004) | 2004 | HIGH |
| Sea-level total neutron flux (broad, all E) | Φ_n,tot ≈ 1.3×10⁻² cm⁻² s⁻¹ (≈ order 10⁻²) | Sea level; integral of Gordon/Ziegler spectrum over thermal→GeV; strong site/altitude/geomagnetic/solar and **local-shielding** dependence | Gordon 2004; Ziegler, IBM J. Res. Dev. 42, 117 (1998) | 2004 | MEDIUM (absolute normalization site-dependent) |
| **Fast-neutron NR rate in Ge (in-band, no quenching)** | full recoil-energy spectrum spans the entire CEvNS band; elastic n-Ge scattering deposits T_recoil on the phonon axis with **no quenching** | surface, unshielded thin Ge; the dominant irreducible in-band NR background for v1.1 | DERIVED from Gordon flux + n-Ge elastic kinematics; template in Billard et al. 2017 background budget | 2026 | MEDIUM (must be computed in-project) |
| Cosmic-ray-induced neutrons dominate even at a *shielded shallow* CEvNS site | ≈ 250 counts keV⁻¹ kg⁻¹ d⁻¹ (dru) in the 10–100 eV ROI, after >2 orders-of-magnitude rejection; residual "strongly dominated by cosmic-ray-induced neutrons" | NUCLEUS at Chooz (shallow overburden + active/passive shield + muon veto); CaWO₄/Al₂O₃ gram-scale | NUCLEUS Collab., EPJC 86 (2026); arXiv:2509.03559 | 2026 | HIGH |
| Muon-induced neutrons vs muon veto (shallow) | μ-induced neutrons ≈ 80% of total μ-induced contribution below 10 keV; muon veto (97.0±0.5)% efficient → suppresses μ-induced background by >1 order of magnitude | CONUS, 24 m.w.e. overburden, 25 cm Pb + 10 cm borated PE shield + plastic-scintillator muon veto | CONUS Collab., "Full background decomposition," arXiv:2112.09585 | 2021 | HIGH |
| Sub-keV total background achieved (shielded, shallow) | 5–15 counts kg⁻¹ d⁻¹ in [0.4,1] keV (ionization scale); detector-dependent 6–13 kg⁻¹ d⁻¹ sub-keV | CONUS, heavily shielded + vetoed, 24 m.w.e. | CONUS, arXiv:2112.09585 & EPJC 79 (2019) 699 (arXiv:1903.09269) | 2019–21 | HIGH |
| Spontaneous-fission neutron yield (²³⁸U) | 1.353×10⁻¹¹ n g⁻¹ s⁻¹ per ppb U, **material-independent**; ⟨E_n⟩ ≈ 2 MeV (Watt spectrum) | secular equilibrium; ²³⁸U SF branch only | Mei, Zhang & Hime, NIMA 606, 651 (2009); arXiv:0812.4307 | 2009 | HIGH |
| Radiogenic (α,n) neutron yield, material-dependent | expressed as n g⁻¹ s⁻¹ per ppb U/Th; ⟨E_n⟩ ≈ 0.8 MeV in Cu; Si yield only 7.4×10⁻⁸ per α; ≲30% yield uncertainty (up to O(100%) for some nuclides, esp. F) | U/Th chain α on light/mid-Z nuclei; SOURCES4 / NeuCBOT / Mei-Zhang-Hime | Mei-Zhang-Hime 2009; review IOP J.Phys.G 52 (2025) 10.1088/1361-6471/adeffa | 2009–25 | MEDIUM-HIGH |
| Example integrated radiogenic yields | ≈ 0.12±0.04 (Th chain α,n), 0.27±0.09 (U chain α,n), 0.8±0.3 (²³⁸U SF) n kg⁻¹ yr⁻¹ | for a stated ppb-level U/Th contamination in a detector material | (α,n) literature compilation (see Sources) | — | MEDIUM |
| **Ge cosmogenic activation — EDELWEISS-III** | production (nuclei kg⁻¹ d⁻¹, sea level): ³H 82±21; ⁶⁵Zn 106±13; ⁵⁵Fe 4.6±0.7; ⁴⁹V 2.8±0.6; ⁶⁸Ge >71 (90% CL LL) | sea-level cosmic-ray exposure; rates saturate over years above ground | Armengaud et al. (EDELWEISS-III), Astropart. Phys. 91, 51 (2017); arXiv:1607.04560 | 2017 | HIGH |
| **Ge cosmogenic activation — CDMSlite/SuperCDMS** | production (atoms kg⁻¹ d⁻¹, sea level): ³H 74±9; ⁶⁵Zn 17±5; ⁵⁵Fe 1.5±0.7; ⁶⁸Ge 30±18 | sea level | Amman et al. (SuperCDMS/CDMSlite), Astropart. Phys. 105, 44 (2019); arXiv:1806.07043 | 2018 | HIGH |
| Ge cosmogenic activation — CONUS in-situ | ⁶⁸Ge 40–70; ⁶⁵Zn 60±10 atoms kg⁻¹ d⁻¹; ⁷¹Ge in-situ (thermal-n capture) | measured from CONUS HPGe spectra | CONUS, arXiv:2112.09585 | 2021 | HIGH |
| Tritium (³H) in-band signature | continuous β⁻, Q = 18.6 keV, t₁/₂ = 12.3 yr; on the phonon scale a **smooth electron-recoil continuum from 0 to 18.6 keV** | activity ∝ surface cosmic-ray exposure history; ~74–82 atoms kg⁻¹ d⁻¹ production saturating over decades | EDELWEISS/CDMSlite above; standard nuclear data | 2017–18 | HIGH |
| Activation X-ray lines (EC daughters) | ⁶⁸Ge/⁶⁸Ga & ⁷¹Ge → 10.37 keV (Ga K); ⁵⁵Fe → 5.9 keV (Mn K); ⁶⁵Zn → 8.98 keV (Cu K); plus L-shell lines ≈ 1.1–1.3 keV | discrete phonon-scale peaks; **L-shell captures (~1.1–1.3 keV) sit just above the CEvNS band** | Ge cosmogenics literature (EDELWEISS, CDMSlite, MAJORANA) | 2017–18 | HIGH |
| Thermal/epithermal neutron capture → NR ≲100 eV | radiative-capture γ-cascade recoils the Ge nucleus; spectrum "strongly overlaps CEvNS for recoils ≲100 eV"; requires effective thermal flux ≲ 7×10⁻⁴ n cm⁻² s⁻¹ (≈60% of sea-level) for 5σ in 100 kg·yr | Ge (Si needs ~10× lower); thermal flux is the key parameter | Biffl, Gevorgian, Harris & Villano, PRD 107, 092011 (2023); arXiv:2212.14148 | 2023 | HIGH |
| Reactor-correlated thermalized neutron field | (745±30) cm⁻² d⁻¹ thermal fluence at the shield; core neutrons reduced ~10²⁰ en route; ROI contribution ≪ signal with realistic quenching | CONUS at Brokdorf, 17.1 m from 3.9 GW_th | Hakenmüller et al. (CONUS), EPJC 79 (2019) 699; arXiv:1903.09269 | 2019 | HIGH |
| Ge intrinsic bulk U/Th radiopurity | ultra-low: bulk ²²⁶Ra, ²²⁸Th, ²²⁷Ac 90% CL limits ≈ µBq kg⁻¹ (≈10⁻¹²–10⁻¹³ g/g U/Th) | zone-refined HPGe crystal bulk | Agostini et al. (GERDA), "Limits on U/Th bulk content in GERDA Phase I," arXiv:1611.06884 | 2017 | HIGH |
| Electroformed-Cu radiopurity (housing benchmark) | < 0.3 µBq kg⁻¹ U and Th (electroformed Cu); common Cu / stainless ~mBq–Bq kg⁻¹; ⁴⁰K ~mBq–Bq kg⁻¹ in many structural materials | underground-electroformed Cu vs commercial materials | MAJORANA contamination-control & assay, OSTI 1481666; standard radioassay databases (ILIAS/SNOLAB) | 2016 | HIGH |

---

## Foundational Work

### Gordon et al. (2004) — Sea-level cosmic-ray neutron spectrum — **surface-flux anchor**

**Key contribution:** The reference measurement + parameterization of the ground-level cosmic-ray-induced neutron energy spectrum, from thermal to GeV, measured at five US sites and scaled to sea-level NYC at mid solar modulation. Two-lognormal fit φ(E) reproduces the data to ~2%; integral flux >10 MeV = 3.50×10⁻³ cm⁻² s⁻¹, total broad flux ~1.3×10⁻² cm⁻² s⁻¹.
**Method:** Bonner-sphere / large-area neutron spectrometry, unfolded to a differential spectrum.
**Limitations:** Absolute normalization varies strongly with **altitude, geomagnetic rigidity, solar cycle, and — critically for us — local shielding** (building roof/walls can both attenuate and, via (n,xn) and moderation, reshape the spectrum). "Surface, no overburden" must specify indoor vs. outdoor.
**Relevance:** This IS the surface number. A thin unshielded Ge wafer at the surface sees essentially this full flux; the elastic-scatter NR spectrum from it is the dominant irreducible in-band background for v1.1. **Directly transferable** (it is already a sea-level surface number), modulo the local-shielding caveat.

### Mei, Zhang & Hime (2009) — Radiogenic (α,n) + SF neutron yields — **radiogenic anchor**

**Key contribution:** Tabulated neutron yields and energy spectra from U/Th-chain (α,n) reactions and ²³⁸U spontaneous fission for materials common in low-background detectors, in n g⁻¹ s⁻¹ per ppb U/Th. SF of ²³⁸U is material-independent at 1.353×10⁻¹¹ n g⁻¹ s⁻¹ per ppb; (α,n) is strongly material-dependent (high in light elements, low in Si/Ge/high-Z).
**Method:** SOURCES4-type convolution of α stopping powers with (α,n) cross sections; validated against measured yields.
**Limitations:** (α,n) cross-section libraries carry ~30% uncertainty typically, up to O(100%) for poorly-measured nuclides (esp. ¹⁹F in PTFE). Requires the U/Th assay of each material as input.
**Relevance:** Sets the radiogenic-neutron in-band NR budget from the wafer, mount, and cryostat. **For an unshielded surface wafer this channel is subdominant to the ambient cosmogenic flux** (radiogenic yields are ~1 n kg⁻¹ yr⁻¹-scale for realistic contamination, vs. the ambient sea-level neutron field), but it is the source that *dominates underground* — so peer numbers quoting radiogenic dominance are underground numbers and must not be transferred naively to the surface.

### EDELWEISS-III (Armengaud et al. 2017) & CDMSlite (Amman et al. 2018) — Ge cosmogenic activation — **activation anchors**

**Key contribution:** Direct measurements of cosmogenic isotope production rates in Ge from decay-rate-vs-exposure analysis. The two independent measurements agree on ³H (82±21 vs 74±9 kg⁻¹ d⁻¹) and bracket ⁶⁵Zn (106±13 vs 17±5) and ⁶⁸Ge (>71 vs 30±18) — the spread reflects differing exposure/altitude histories and analysis methods.
**Method:** Fit decay-corrected line and continuum activities against known above-ground exposure and cooldown times.
**Limitations:** Activation is entirely **history-dependent** — production happens at the surface/altitude, saturating over the isotope lifetime; underground the clock stops and activity decays. Absolute activity for a specific detector requires its true exposure/transport/storage timeline.
**Relevance:** ³H is the headline in-band background: a smooth 0–18.6 keV electron-recoil β continuum on the phonon scale, directly under and through the CEvNS band, with no line to subtract against. For a **freshly-fabricated, surface-deployed** wafer with recent cosmic exposure, ³H (and the EC activation X-ray lines at ~1.1–1.3 keV L-shell and ~10 keV K-shell) are near saturation — the *worst-case* activation scenario. This is a genuinely different regime from the deep, well-aged detectors these papers describe.

### Biffl, Gevorgian, Harris & Villano (2023) — Neutron-capture NR overlap with CEvNS

**Key contribution:** Showed that **thermal/epithermal radiative neutron capture** on Ge (and Si) recoils the capturing nucleus via the de-excitation γ cascade, producing a nuclear-recoil spectrum that "strongly overlaps the CEvNS signal for recoils ≲100 eV." Quantified the thermal-flux ceiling: effective thermal flux must stay ≲ 7×10⁻⁴ n cm⁻² s⁻¹ (~60% of sea-level) to reach 5σ in 100 kg·yr at 10 m from a 1 MW reactor; Si needs ~10× lower.
**Method:** Capture-γ cascade kinematics + neutron-transport flux modeling.
**Relevance:** Identifies a *second* neutron channel distinct from elastic scattering, populating exactly the lowest CEvNS bins (≲100 eV) where v1.0 places its flagship signal. Thermal-neutron capture also produces ⁷¹Ge (in-situ activation → 10.37 keV EC line). For a surface wafer the ambient thermal-neutron flux is a real, on-band NR source and cannot be reactor-on/off subtracted (it is cosmogenic, not reactor-correlated).

### NUCLEUS particle-background study (2026) — surface-like CEvNS background benchmark

**Key contribution:** End-to-end Geant4 + site-measurement prediction for a reactor CEvNS experiment at a **shallow** site. After passive shield + active veto giving >2 orders-of-magnitude rejection, the residual 10–100 eV background is ≈ 250 counts keV⁻¹ kg⁻¹ d⁻¹ and is **strongly dominated by cosmic-ray-induced neutrons**.
**Method:** Environmental γ/neutron measurements at Chooz + full-geometry Geant4 with cosmic-ray, environmental-γ, and material-radioactivity generators.
**Limitations:** NUCLEUS has *some* overburden and full shielding; our v1.1 scenario has **none**, so the ambient neutron term is *larger* and less moderated for us.
**Relevance:** The closest published demonstration that, for a low-threshold reactor CEvNS detector near the surface, **cosmogenic neutrons — not radiogenic neutrons, not muon-induced neutrons, not gammas — set the in-band floor.** This validates prioritizing the ambient fast-neutron elastic-scatter channel as the leading v1.1 deliverable.

---

## Recent Developments

| Paper | Authors | Year | Advance | Impact on Our Work |
| --- | --- | --- | --- | --- |
| arXiv:2509.03559 (EPJC 2026) | NUCLEUS Collab. | 2026 | ~250 dru cosmic-neutron-dominated 10–100 eV background at a shallow shielded reactor site | Primary peer benchmark for the surface neutron floor; our unshielded case is an upper bound relative to it |
| arXiv:2503.08859 | LEE community (Ge/CEvNS/DM) | 2025 | Review of "Low-Energy Excess" and sub-keV backgrounds in phonon/charge detectors | Cautions that near threshold an unexplained excess (LEE) often dominates over all modeled backgrounds — relevant if v1.1 quotes a floor near eV scale |
| arXiv:2212.14148 (PRD 107, 092011) | Biffl, Villano et al. | 2023 | Neutron-capture NR overlaps CEvNS ≲100 eV; thermal-flux ceiling 7×10⁻⁴ n/cm²/s | Adds capture channel to elastic; sets thermal-neutron requirement for the surface scenario |
| arXiv:2112.09585 | CONUS Collab. | 2021 | Full background decomposition: μ-induced neutrons ~80% of μ term <10 keV; 97% veto | Quantifies muon-correlated neutron fraction and veto leverage (we have no overburden, so μ-induced share differs) |
| J.Phys.G 52 (2025) 10.1088/1361-6471/adeffa | (α,n) review | 2025 | Modern (α,n) yield methods; 30%–O(100%) yield uncertainties | Sets the honest error bar on the radiogenic-neutron budget |
| arXiv:1706.05324 | Wei, Mei et al. | 2017 | Cosmogenic Ge activation for tonne-scale searches (Geant4, natural + enriched Ge) | Cross-check for ³H/⁶⁸Ge/⁶⁵Zn production and exposure-history modeling |
| arXiv:2605.16534 | (shallow-depth cosmogenics) | 2026 | Cosmogenic activation at shallow depths | Directly addresses the shallow/surface regime our wafer occupies |

---

## Known Limiting Cases

| Limit | Known Result | Source | Notes |
| --- | --- | --- | --- |
| Deep underground (μ shielded out) | in-situ **muon-induced** + **radiogenic** neutrons dominate the NR background; ambient atmospheric neutrons negligible | Mei & Hime, PRD 73, 053004 (2006), astro-ph/0512125; EDELWEISS at Modane (4800 m.w.e., Φ_n(2–10 MeV) ≈ 4×10⁻⁶ cm⁻² s⁻¹) | **Do NOT transfer underground radiogenic-dominance to the surface** |
| Surface, no overburden (our case) | **ambient cosmogenic fast-neutron elastic scattering dominates**; muon-induced and radiogenic neutrons subdominant; activation (³H) near saturation | Gordon 2004 flux; NUCLEUS shallow-site finding | The defining regime for v1.1 |
| Thermal-flux → 0 | capture-induced NR ≲100 eV vanishes; only elastic fast-n and CEvNS remain in that band | Biffl/Villano 2023 | Motivates a moderator/absorber in any real design |
| U/Th → 0 in materials | radiogenic (α,n)+SF neutron term → 0; only cosmogenic + reactor-correlated neutrons remain | Mei-Zhang-Hime scaling (linear in ppb) | Ge bulk is already ~µBq/kg, so intrinsic radiogenic term is tiny |
| No cosmic exposure history | cosmogenic activation (³H, ⁶⁸Ge, ⁶⁵Zn, ⁵⁵Fe) → 0 | EDELWEISS/CDMSlite exposure scaling | Unphysical for a surface detector, but bounds the activation term from below |

---

## Open Questions

1. **Absolute ambient neutron normalization at the actual deployment.** Gordon gives the outdoor sea-level spectrum to ~2%, but the *local* flux depends on building overburden, roof material, and moderation — factor-of-a-few uncertainty. v1.1 must state whether "surface, no overburden" means bare outdoor or inside a reactor building, since that sets the leading in-band background normalization. **Biggest single normalization uncertainty.**
2. **Fast-neutron elastic-scatter recoil spectrum in a thin (2 mm) Ge wafer.** The thinness matters: many fast neutrons deposit only a partial recoil or multiple-scatter; the single-vs-multiple-scatter fraction and the escape probability in 2 mm change the in-band spectral shape. Requires an MC transport step (elastic n-Ge cross sections, ENDF/B), not just flux × cross-section.
3. **Cosmogenic activation for THIS wafer's history.** ³H and the EC X-ray lines depend entirely on the fabrication/transport/storage/deployment timeline. Near-saturation (worst case) vs. a freshly-zone-refined-and-quickly-deployed crystal differ by an order of magnitude. Needs an assumed exposure model stated as a v1.1 input.
4. **Muon-correlated vs. uncorrelated neutron separation at the surface.** With no overburden, is the QPD muon-tag (v1.0 channel) able to veto the in-situ muon-induced neutron component, and what fraction of the total neutron NR rate is muon-correlated vs. ambient-atmospheric? CONUS's 80% figure is at 24 m.w.e. and does not transfer.
5. **Reactor-correlated thermal neutrons at 25 m / 3 GW.** CONUS measured (745±30) cm⁻² d⁻¹ at 17.1 m / 3.9 GW behind shielding. Unshielded at 25 m the reactor-correlated thermal fluence and its capture-NR contribution need a dedicated estimate; unlike cosmogenic neutrons this one *is* reactor-on/off separable.
6. **Low-Energy Excess (LEE).** Every low-threshold phonon detector to date shows an unmodeled rising excess near threshold (arXiv:2503.08859) that dwarfs modeled backgrounds below ~100 eV. v1.1 should flag that its modeled in-band floor is a *lower* bound; the LEE is not yet predictable from first principles.

---

## Notation & Convention Reconciliation (backgrounds)

| Quantity | Standard Symbol(s) | Variations in literature | Our (v1.1) choice | Reason |
| --- | --- | --- | --- | --- |
| Neutron elastic recoil energy | T, E_R, E_nr | keVnr in quenched detectors | phonon-scale T (eV/keV), **no quenching** | QPD reads full recoil as phonons — same axis as CEvNS |
| Background rate unit | dru = counts keV⁻¹ kg⁻¹ d⁻¹ | c/keV/kg/day; counts kg⁻¹ d⁻¹ (integrated) | dru (differential) + integrated kg⁻¹ d⁻¹ | Match NUCLEUS/CONUS |
| Cosmogenic production rate | R (nuclei kg⁻¹ d⁻¹) | atoms/(kg·day) | nuclei kg⁻¹ d⁻¹, sea-level, saturation-corrected | Match EDELWEISS/CDMSlite |
| Radiogenic yield | Y (n g⁻¹ s⁻¹ per ppb) | n/yr; n per 10⁶ α; n/(g·ppb) | n g⁻¹ s⁻¹ per ppb U/Th (Mei-Zhang-Hime) | Standard radiogenic convention |
| U/Th contamination | ppb (mass) or Bq/kg | mBq/kg, µBq/kg, g/g | µBq/kg (assay) → ppb via 1 ppb U ≈ 12.4 mBq/kg, 1 ppb Th ≈ 4.06 mBq/kg | Assay databases quote Bq/kg; yield code wants ppb |
| Neutron flux | Φ_n (cm⁻² s⁻¹) | cm⁻² d⁻¹ (fluence rate); m⁻² s⁻¹ | cm⁻² s⁻¹, energy-differential where needed | Gordon native units |

---

## Transferability Verdict (for the roadmapper)

**Directly transferable to a thin ~110 g unshielded surface Ge wafer (no rescale):**
- Gordon (2004) sea-level neutron flux — it *is* the surface number (state indoor/outdoor).
- Ge cosmogenic production rates (EDELWEISS/CDMSlite) — sea-level production; apply the wafer's own exposure-history/saturation model.
- Mei-Zhang-Hime radiogenic yields per ppb — apply the wafer/mount/cryostat U/Th assay.
- Ge bulk radiopurity (GERDA µBq/kg) and Cu/structural assay budgets — material-intrinsic, deployment-independent.

**Needs rescaling / re-derivation before use:**
- NUCLEUS ~250 dru and CONUS sub-keV rates — these include overburden + heavy shield + veto; the unshielded surface wafer sees a **higher** ambient-neutron rate (treat NUCLEUS as a *shielded lower bound*).
- CONUS "μ-induced = 80% of μ term" and 97% veto leverage — 24 m.w.e. numbers, not valid at zero overburden.
- Any underground radiogenic/muon-induced-neutron-dominance statement (EDELWEISS-Modane etc.) — inverted regime; ambient cosmogenic dominates at the surface.

**Biggest normalization uncertainties (rank-ordered):**
1. Local ambient-neutron flux (building shielding / indoor-vs-outdoor) — factor of a few, dominant.
2. Cosmogenic activation (³H especially) — exposure-history-dependent, ~order of magnitude.
3. (α,n) yields — 30% to O(100%) per nuclide.
4. Thin-wafer single/multiple-scatter and escape fraction — spectral-shape systematic.
5. LEE — unmodeled, potentially dominant below ~100 eV.

---

## Sources

- Gordon et al., "Measurement of the Flux and Energy Spectrum of Cosmic-Ray Induced Neutrons on the Ground," IEEE Trans. Nucl. Sci. 51, 3427 (2004) — surface fast-neutron flux anchor. Ziegler, IBM J. Res. Dev. 42, 117 (1998) — earlier sea-level parameterization.
- Mei, Zhang & Hime, "Evaluation of (α,n) induced neutrons as a background for dark matter experiments," NIMA 606, 651 (2009), arXiv:0812.4307 — radiogenic (α,n)+SF yields (²³⁸U SF = 1.353×10⁻¹¹ n/g/s/ppb). (α,n) review, J. Phys. G 52 (2025), doi:10.1088/1361-6471/adeffa; SOURCES4/NeuCBOT (arXiv:2211.02080, 2408.10910). Radiogenic-yield calc: arXiv:1702.02465.
- Mei & Hime, "Muon-induced background study for underground laboratories," PRD 73, 053004 (2006), astro-ph/0512125 — muon-induced neutron yield vs depth (why in-situ μ-neutrons dominate underground, not at the surface).
- Armengaud et al. (EDELWEISS-III), "Measurement of the cosmogenic activation of germanium detectors in EDELWEISS-III," Astropart. Phys. 91, 51 (2017), arXiv:1607.04560 — Ge activation rates (³H 82±21, ⁶⁵Zn 106±13, ⁶⁸Ge >71 kg⁻¹ d⁻¹).
- Amman et al. (SuperCDMS/CDMSlite), "Production Rate Measurement of Tritium and Other Cosmogenic Isotopes in Germanium," Astropart. Phys. 105, 44 (2019), arXiv:1806.07043 — ³H 74±9, ⁶⁵Zn 17±5, ⁶⁸Ge 30±18 atoms/kg/day. Wei/Mei et al., arXiv:1706.05324 — tonne-scale Ge cosmogenics. Shallow-depth cosmogenics, arXiv:2605.16534. Cebrián review, arXiv:1708.07449.
- Biffl, Gevorgian, Harris & Villano, "Neutron capture-induced nuclear recoils as background for CEvNS measurements at reactors," PRD 107, 092011 (2023), arXiv:2212.14148 — thermal-capture NR overlap ≲100 eV; thermal-flux ceiling 7×10⁻⁴ n/cm²/s.
- NUCLEUS Collab., "Particle background characterization and prediction for the NUCLEUS reactor CEvNS experiment," EPJC 86 (2026), arXiv:2509.03559 — ~250 dru cosmic-neutron-dominated 10–100 eV background at a shallow shielded site. Commissioning: arXiv:2508.02488.
- CONUS Collab.: Hakenmüller et al., "Neutron-induced background in the CONUS experiment," EPJC 79, 699 (2019), arXiv:1903.09269 (reactor-correlated thermal fluence 745±30 cm⁻² d⁻¹); "Full background decomposition of the CONUS experiment," arXiv:2112.09585 (μ-induced fraction, 97% veto, sub-keV rates, in-situ Ge activation).
- Agostini et al. (GERDA), "Limits on uranium and thorium bulk content in GERDA Phase I detectors," Astropart. Phys. 91, 15 (2017), arXiv:1611.06884 — Ge bulk U/Th ~µBq/kg limits. MAJORANA contamination control & assay, OSTI 1481666 — electroformed-Cu <0.3 µBq/kg U/Th and structural-material radioassay budgets.
- "Low-Energy Backgrounds in Solid-State Phonon and Charge Detectors," arXiv:2503.08859 — LEE / sub-keV background review (flags the unmodeled near-threshold excess).
- EDELWEISS at Modane (Φ_n(2–10 MeV) ≈ 4×10⁻⁶ cm⁻² s⁻¹, μ flux ~4 m⁻² d⁻¹) and CEvNS review arXiv:2203.07361 — underground limiting-case anchors.
