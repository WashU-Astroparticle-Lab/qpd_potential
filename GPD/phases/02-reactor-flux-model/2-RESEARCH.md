# Phase 2: Reactor Flux Model - Research

**Researched:** 2026-07-20
**Domain:** Reactor antineutrino flux modeling (conversion + summation methods), CEvNS input flux
**Depth:** standard
**Confidence:** HIGH above 2 MeV (data-anchored Huber–Mueller); MEDIUM below 1.8 MeV (model-only summation + n-capture); HIGH on normalization arithmetic

---

## User Constraints (from CONTEXT.md)

**No `CONTEXT.md` exists for this phase** (`gpd:discuss-phase` was not run). All modeling choices below are at the researcher/planner's discretion, constrained only by the roadmap goal, `GPD/REQUIREMENTS.md` (CALC-01), and the Phase-1 conventions lock (`GPD/CONVENTIONS.md`).

Binding upstream constraints inherited (not user "discretion"):

- **Contract (CALC-01 → claim-cevns, anchor ref-huber):** 4-isotope Huber–Mueller spectrum with an *explicit* sub-1.8 MeV treatment (summation + neutron-capture), normalized to 3 GW_th at 25 m.
- **Forbidden proxy (must be guarded in the plan):** Huber–Mueller truncated or naively power-law-extrapolated at the 1.8 MeV IBD threshold. The sub-IBD flux populates the flagship low-recoil CEvNS bins and must be modeled, not dropped.
- **Deliverable form:** a *frozen, versioned* CSV/table with a documented energy grid and an uncertainty band explicitly split at ~1.8–2 MeV.

---

## Active Anchor References

Contract-critical anchors for this phase (mandatory inputs, not background reading):

| Anchor | What it is | How Phase 2 must use it |
| --- | --- | --- |
| **ref-huber** — Huber, PRC 84, 024617 (2011), arXiv:1106.0687 | Conversion-method per-fission ν̄ spectra for ²³⁵U, ²³⁹Pu, ²⁴¹Pu | Primary >2 MeV spectrum for the three fissile isotopes. **The exact polynomial coefficients must be fetched from this paper (or a verified tabulation) — do not invent them.** |
| Mueller et al., PRC 83, 054615 (2011), arXiv:1101.2663 | Summation/ab-initio ²³⁸U per-fission spectrum (the "Mueller" half of Huber–Mueller) | ²³⁸U component >2 MeV. Coefficients likewise fetched, not invented. (Optional refinement: Haag et al. 2014 measured ²³⁸U.) |
| **ref-cevns-benchmark (downstream)** — Billard et al., J. Phys. G 44, 105101 (2017), arXiv:1612.09035 | Ge phonon-scale CEvNS rates; *its* flux assumptions | Phase 3 folds this flux to reproduce Billard Table 1. To reproduce it faithfully, Phase 2 must be able to emit a variant matching Billard's assumptions (HM + **spectrum frozen constant below 2 MeV**, fission fractions 235/239/238/241 = 55.6/32.6/7.1/4.7%). This is a *validation variant*, not the flagship model. |
| Phase-1 `GPD/CONVENTIONS.md` (Sections A, D, G) | Locked units, 3 GW_th, 25 m, flux ~7–8×10¹² ν̄ cm⁻² s⁻¹, Φ(E_ν) definition | Normalization convention is fixed here; Phase 2 must be numerically consistent with it. |

Anchors named but **model-only / lower confidence** (still required components):

| Source | Role |
| --- | --- |
| CONFLUX, Zhang et al., arXiv:2503.18966 (2025) | Recommended generator for the sub-2 MeV summation spectra (open framework). |
| Estienne, Fallot et al., PRL 123, 022502 (2019) | Modern summation spectrum agreeing with Daya Bay; cross-check / alternative sub-2 MeV source. |
| Kopeikin, Mikaelyan, Sinev, Phys. At. Nucl. 67, 1892 (2004), hep-ph/0308186; Huber & Jaffke, PRL 116, 122503 (2016) | ²³⁸U(n,γ)²³⁹U → ²³⁹Np neutron-capture ν̄ chain (the non-fission sub-1.8 MeV component). |
| Liao, Liu, Marfatia, PRD 108, 033002 (2023), arXiv:2302.10460 | Framework defining what low-threshold CEvNS is sensitive to below 1.8 MeV; the honest-band reference. |

---

## Summary

Phase 2 produces one frozen, versioned Φ(E_ν) table that stitches two regimes of established reactor-antineutrino physics. **Above ~2 MeV** the flux is data-anchored: the Huber–Mueller model gives each isotope's per-fission spectrum as `S_i(E_ν) = exp(Σ_{p=1}^{6} α_{ip} E_ν^{p-1})` (a fifth-order polynomial in the exponent, six coefficients per isotope), combined by fission fractions, with a ~2–5% uncertainty band. **Below 1.8 MeV** the conversion method is undefined and the flux has never been measured; it must be built from a summation calculation (recommended: CONFLUX, with Estienne–Fallot 2019 as cross-check) plus an explicit ²³⁸U(n,γ)²³⁹U→²³⁹Np neutron-capture component, and carried with a much wider ~10–20% band. The two regimes are joined across the 1.8–2 MeV seam by normalizing the summation spectrum to Huber–Mueller in an overlap window so no discontinuity appears.

Normalization is a 4-step chain — thermal power → fissions/s → ν̄/s → 1/(4πd²) flux — that I verified numerically: 3 GW_th at 25 m gives **~7–8×10¹² ν̄ cm⁻² s⁻¹** (my arithmetic below yields 7.1–7.6×10¹²). The "~1×10¹³" figure in `REQUIREMENTS.md` CALC-01 is a loose order-of-magnitude rounding, **not** the correct normalization target; the roadmap's ~7–8×10¹² is right and is what the frozen table must integrate to.

**Primary recommendation:** Build a component-wise flux table Φ(E_ν) = [Huber–Mueller fission spectrum, E_ν > 2 MeV] ⊕ [summation fission spectrum, E_ν < 2 MeV, seam-matched] ⊕ [²³⁸U(n,γ) capture ν̄], on a fine linear/PCHIP-interpolable grid from ~0 to 10 MeV, normalized via the effective-thermal-energy-per-fission chain to 3 GW_th / 25 m, with a per-bin relative-uncertainty column whose band widens from ~2–5% above 2 MeV to ~10–20% below 1.8 MeV. Fetch every coefficient/table from its primary source; invent nothing.

---

## Literature Landscape

### Foundational Papers

| Paper | Authors | Year | Key Result | Relevance |
| --- | --- | --- | --- | --- |
| On the determination of anti-neutrino spectra from nuclear reactors, PRC 84, 024617 (arXiv:1106.0687) | Huber | 2011 | Conversion-method per-fission ν̄ spectra for ²³⁵U, ²³⁹Pu, ²⁴¹Pu; the `exp(Σ α_p E^{p-1})` parameterization | **The** >2 MeV model for the three fissiles (anchor ref-huber) |
| Improved predictions of reactor ν̄ spectra, PRC 83, 054615 (arXiv:1101.2663) | Mueller et al. | 2011 | Summation/ab-initio ²³⁸U spectrum; "Huber–Mueller" combination | ²³⁸U component >2 MeV |
| Coherent effects of a weak neutral current, PRD 9, 1389 | Freedman | 1974 | CEvNS cross section (downstream consumer of this flux) | Fixes what E_ν range and shape matter (E_ν,min(T)=√(MT/2)) |
| Components of antineutrino emission in nuclear reactor, Phys. At. Nucl. 67, 1892 (hep-ph/0308186) | Kopeikin, Mikaelyan, Sinev | 2004 | Six emission components incl. ²³⁸U(n,γ)²³⁹U→²³⁹Np capture ν̄ (~0.6/fission, E_ν≲1.3 MeV) | The non-fission sub-1.8 MeV component |

### Recent Advances

| Paper | Authors | Year | Key Result | Relevance |
| --- | --- | --- | --- | --- |
| CONFLUX: standardized reactor ν̄ flux framework, arXiv:2503.18966 | Zhang et al. | 2025 | Open, maintained code computing conversion+summation spectra over the full energy range | Recommended generator for the sub-2 MeV summation region |
| Updated summation model (agrees with Daya Bay), PRL 123, 022502 | Estienne, Fallot et al. | 2019 | Summation spectrum matching measured IBD flux without anomaly | Cross-check / alternative sub-2 MeV source |
| Comprehensive revision of the summation method, arXiv:2304.14992 | (summation collab.) | 2023 | Updated per-isotope summation fluxes and spectra | Alternative/uncertainty input for summation region |
| How to measure the reactor ν flux below IBD threshold with CEvNS, PRD 108, 033002 (arXiv:2302.10460) | Liao, Liu, Marfatia | 2023 | Framework for sub-1.8 MeV flux via low-threshold CEvNS; n-capture unobservability | Defines the honest error band on our lowest bins |
| Re-measured ²³⁵U/²³⁹Pu β ratio ("KI" model), PRD 104, L071301 (arXiv:2103.01684) | Kopeikin, Skorokhvatov, Titov | 2021 | ~5% lower ²³⁵U flux, largely resolving the anomaly | Optional normalization switch (±5% systematic) |
| Reactor antineutrino flux and anomaly (review), Prog. Part. Nucl. Phys. (arXiv:2310.13070) | Hayen, Kostensalo (eds.) | 2024 | Anomaly status, HM vs summation, 5 MeV bump | Systematics context |

### Review Articles and Textbook Treatments

| Source | Authors | Coverage | Best For |
| --- | --- | --- | --- |
| Reactor ν̄ flux and anomaly, arXiv:2310.13070 | Hayen & Kostensalo (eds.) | HM vs summation, anomaly, 5 MeV bump | Systematic-band justification |
| Reactor ν̄ yield/accounting, ARNPS 66, 219 (arXiv:1605.02047) | Hayes & Vogel | ~6 ν̄/fission, ~2×10²⁰ ν̄ s⁻¹ GW_th⁻¹ | Normalization sanity anchors |

### Notation Conventions Across Papers

| Quantity | Huber/Mueller | Summation papers | Our convention (Phase-1 lock) | Notes |
| --- | --- | --- | --- | --- |
| Per-fission spectrum | S_i(E_ν) [ν̄/fission/MeV] | dN_i/dE [ν̄/fission/MeV] | S_i(E_ν) [ν̄/fission/MeV] | Same units; **already integrates to ~6/fission — never re-multiply by 6** |
| Detector flux | — | — | Φ(E_ν) [ν̄ cm⁻² s⁻¹ MeV⁻¹] | = Σ_i f_i S_i(E) × R_f × 1/(4πd²) |
| Fission fractions | f_i | f_i | f_i, Σf_i = 1 | Default 235:238:239:241 = 0.58:0.07:0.30:0.05 (see below) |
| Energy/fission | — | — | ⟨E_f⟩ = Σ f_i E_i (effective thermal) | Use effective thermal (~200–214 MeV), **not** total Q incl. neutrinos |

**Key notational hazards:** (1) fission-fraction *ordering* differs between papers — Billard 2017 lists 235/239/238/241 = 55.6/32.6/7.1/4.7%, while Daya Bay/METHODS lists 235/238/239/241; always label the isotope explicitly. (2) "per fission" vs "per second per GW" vs "per fission per MeV" normalizations are silently mixed in the literature (Pitfall 2). (3) `E_ν` in the Huber polynomial is in **MeV** and the polynomial is in the *exponent* — a common bug is applying the polynomial directly instead of exponentiating.

---

## Methods and Approaches

### Standard Analytical Methods

| Method | When to Use | Limitations | Key Reference |
| --- | --- | --- | --- |
| Huber–Mueller conversion spectra `S_i=exp(Σ_{p=1}^{6} α_{ip}E^{p-1})` | E_ν ≳ 1.8–2 MeV, all four isotopes | Undefined <1.8 MeV; ~5% anomaly normalization; ~10% "bump" at 5–7 MeV | Huber 2011; Mueller 2011 |
| Summation (ab-initio) method | Full range, esp. E_ν < 2 MeV | ≳10–20% shape uncertainty from β-decay database gaps; imperfect power correlation | CONFLUX (2025); Estienne–Fallot (2019) |
| ²³⁸U(n,γ)²³⁹U→²³⁹Np capture ν̄ | E_ν ≲ 1.3 MeV non-fission component | ~0.6/fission, equilibrates on ²³⁹Np lifetime (2.3 d) → imperfect power correlation | Kopeikin 2004; Huber–Jaffke 2016 |
| Vogel–Engel analytic form `dN/dE ∝ exp(a₀+a₁E+a₂E²)` | Crude per-isotope fallback | Coarse; superseded by summation | Vogel–Engel, PRD 39, 3378 |
| Normalization chain R_f = P_th/⟨E_f⟩ → 1/(4πd²) | Always (fixes absolute scale) | Convention-trap dense (see Pitfalls) | Hayes–Vogel (arXiv:1605.02047) |

**The Huber parameterization (functional form — HIGH confidence on form, coefficients TO BE FETCHED):**

```
S_i(E_ν) = exp( Σ_{p=1}^{6} α_{ip} · E_ν^{p-1} )     [ν̄ per fission per MeV], E_ν in MeV
```

Order-5 polynomial ⇒ 6 coefficients α_{i,1..6} per isotope; i ∈ {²³⁵U, ²³⁹Pu, ²⁴¹Pu} from Huber (conversion), ²³⁸U from Mueller (summation). Nominal validity ~1.8/2 to 8 MeV. **The α_{ip} values are NOT reproduced here** — they must be read from Huber PRC 84, 024617 (Table in the paper) and Mueller PRC 83, 054615, or from a verified digitized tabulation (e.g., the coefficient tables shipped with `bradkav/CEvNS`, cross-checked against the papers). Do not transcribe from memory.

### Combining isotopes

```
Φ_fission(E_ν) = Σ_i f_i · S_i(E_ν),     Σ_i f_i = 1
```

**Default fission fractions (tunable input, state explicitly):** cycle-averaged PWR
235U : 238U : 239Pu : 241Pu = **0.58 : 0.07 : 0.30 : 0.05** (Daya Bay convention, PRL 130, 211801; also METHODS.md Domain-1). Carry a begin-of-cycle vs end-of-cycle band as a shape systematic (²³⁹Pu spectrum is softer than ²³⁵U, so the effect on the folded CEvNS recoil shape is only a few %). Provide a switch to the **Billard set (55.6/32.6/7.1/4.7% = 235/239/238/241)** for benchmark reproduction.

### Sub-1.8 MeV extension and seam-matching (the phase's central method decision)

1. Generate per-isotope summation spectra `S_i^{sum}(E_ν)` over the full range (recommended: **CONFLUX**; cross-check against **Estienne–Fallot 2019** tabulation).
2. **Seam-match to avoid discontinuity:** in an overlap window (e.g., 2.0–3.0 MeV) compute a per-isotope scale factor `c_i = ∫ S_i^{HM} / ∫ S_i^{sum}` (or a smooth multiplicative correction), so the summation curve is normalized onto the data-anchored Huber–Mueller curve where both are valid. Then define
   `S_i(E_ν) = S_i^{HM}(E_ν)` for E_ν ≥ 2 MeV, `= c_i · S_i^{sum}(E_ν)` for E_ν < 1.8 MeV, with a smooth blend (e.g., linear-in-E weight, or C¹ monotone interpolation) across 1.8–2.0 MeV.
3. **Add the ²³⁸U(n,γ) capture component** as a separate additive term normalized to ~0.6 ν̄/fission (Kopeikin 2004 / Huber–Jaffke 2016), with E_ν ≲ 1.3 MeV shape from the ²³⁹U (Q=1.26 MeV) and ²³⁹Np (Q=0.72 MeV) β spectra. Keep it a distinct column so it can be toggled (Pitfall 1 warning-sign test).

**Do NOT** power-law-extrapolate the >2 MeV Huber fit below 1.8 MeV, and **do NOT** truncate at 1.8 MeV — both are the forbidden proxy.

### Computational Tools

| Tool/Package | Version | Purpose | Why Standard |
| --- | --- | --- | --- |
| Python + NumPy/SciPy | ≥3.11 / current | polynomial eval, integration, PCHIP interpolation, CSV I/O | Project baseline (COMPUTATIONAL.md); flux build is a one-off table generation |
| `scipy.interpolate.PchipInterpolator` | current | monotone interpolation of tabulated summation spectra | Avoids negative flux / ringing at the 5 MeV bump (Numerical Traps, PITFALLS.md) |
| CONFLUX | arXiv:2503.18966 release | generate sub-2 MeV summation spectra per isotope | Open, maintained, standardized; covers the never-measured region |
| `bradkav/CEvNS` (arXiv:1805.01798) | current | source of digitized Huber–Mueller coefficients + a flux-build reference to cross-check against | Independent validation oracle for the >2 MeV spectrum |

### Supporting Tools

| Tool/Package | Version | Purpose | When to Use |
| --- | --- | --- | --- |
| pandas or csv | current | frozen versioned CSV with header/provenance | Deliverable packaging |
| matplotlib | current | overlay Φ(E_ν) vs published Huber curve; show band split | Validation figure |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
| --- | --- | --- |
| CONFLUX for sub-2 MeV | Estienne–Fallot 2019 tabulated summation | Estienne–Fallot is a fixed published table (reproducible, no install) but less flexible; use as cross-check or primary if CONFLUX install is undesirable |
| Huber–Mueller >2 MeV | Full summation everywhere (Estienne–Fallot / arXiv:2304.14992) | Summation has no conversion-anomaly baggage but larger per-branch uncertainty; offer as a switch if low-recoil systematics dominate conclusions |
| Default HM normalization | HM×KI rescaling (Kopeikin 2021) | KI lowers ²³⁵U ~5%; carry as a ±5% normalization switch, not the baseline |
| ²³⁸U from Mueller 2011 | Haag et al. 2014 measured ²³⁸U | Minor; only matters at high precision >4 MeV |

**Installation / Setup:**

```bash
uv add numpy scipy pandas matplotlib
# CONFLUX: install per arXiv:2503.18966 repo instructions (or use Estienne–Fallot tabulation as a CSV input)
# Huber–Mueller coefficients: fetch from Huber PRC 84,024617 / Mueller PRC 83,054615
#   (optionally cross-check against bradkav/CEvNS coefficient tables)
```

### Package / Framework Reuse Decision

**Wrap/extend existing tabulations; write bespoke only for stitching and normalization.**

- **Reuse (do not re-derive):** the Huber/Mueller polynomial *coefficients* (from the papers or `bradkav/CEvNS`), and the sub-2 MeV summation spectra (CONFLUX output or Estienne–Fallot table). Re-deriving conversion spectra from ILL β data or running a full summation from ENDF is out of scope and error-prone.
- **Bespoke (write fresh, ~100–200 lines):** the seam-matching/blend across 1.8–2 MeV, the ²³⁸U(n,γ) additive component assembly, the power→fission→flux normalization function, and the frozen-CSV writer with provenance/version header and the above/below-2-MeV uncertainty columns. These are integration glue with project-specific conventions (3 GW_th, 25 m, per-kg bookkeeping) that no package provides directly.
- **Justification for bespoke glue:** the missing capability is exactly the *stitched, uncertainty-banded, versioned deliverable* — packages emit either a >2 MeV spectrum or a raw summation spectrum, not the joined, normalized, provenance-tagged table this contract requires. Reuse the physics; own the assembly and the unit-tested normalization.

---

## Known Results and Benchmarks

### Established Results

| Result | Value/Expression | Conditions | Source | Confidence |
| --- | --- | --- | --- | --- |
| ν̄ per fission (all energies) | ≈ 6 ν̄/fission | integral of per-fission spectrum | Hayes–Vogel (arXiv:1605.02047) | HIGH |
| ν̄ per fission above IBD threshold | ≈ 1.9 ν̄/fission | E_ν > 1.8 MeV | reactor ν̄ accounting | HIGH |
| ν̄ emission rate | ≈ 2×10²⁰ ν̄ s⁻¹ per GW_th (⇒ ~6×10²⁰/s at 3 GW_th) | standard fission accounting | Hayes–Vogel | HIGH |
| Effective thermal energy/fission | ≈ 202.4 / 205.9 / 211.1 / 213.6 MeV (²³⁵U/²³⁸U/²³⁹Pu/²⁴¹Pu) | excludes ν̄ energy, includes capture-γ | Ma et al., PRC 88, 014605 | HIGH |
| ²³⁸U(n,γ) capture ν̄ yield | ≈ 0.6 capture ν̄ per fission, E_ν ≲ 1.3 MeV | equilibrium power reactor | Kopeikin 2004; Huber–Jaffke 2016 | HIGH (existence), MEDIUM (shape) |
| Flux at detector | **~7–8×10¹² ν̄ cm⁻² s⁻¹** | 3 GW_th, 25 m, point source | DERIVED (verified below); Phase-1 lock | HIGH (arithmetic) |

### Normalization arithmetic (verified this session — the answer to research-focus item 3)

```
Fission rate:   R_f = P_th / ⟨E_f⟩
  P_th = 3 GW  = 3.0×10⁹ J/s
  ⟨E_f⟩ ≈ 205 MeV = 205×10⁶ × 1.602×10⁻¹⁹ J = 3.28×10⁻¹¹ J
  R_f = 3.0×10⁹ / 3.28×10⁻¹¹ ≈ 9.1×10¹⁹ fissions/s

ν̄ rate:        N_ν = ⟨n_ν/fission⟩ × R_f ≈ 6 × 9.1×10¹⁹ ≈ 5.5×10²⁰ ν̄/s
  (consistent with 2×10²⁰ ν̄/s/GW_th × 3 GW_th = 6×10²⁰ ν̄/s)

Flux at d=25 m: Φ = N_ν / (4π d²),  d = 2500 cm
  4π d² = 4π (2500)² = 7.85×10⁷ cm²
  Φ = (5.5–6.0)×10²⁰ / 7.85×10⁷ ≈ 7.0–7.6×10¹² ν̄ cm⁻² s⁻¹
```

**Conclusion:** ~7–8×10¹² ν̄ cm⁻² s⁻¹ is correct (roadmap + Phase-1 lock). The "~1×10¹³" in `REQUIREMENTS.md` CALC-01 is a loose order-of-magnitude rounding (they agree at the "order 10¹³" level, differ by ~30%); **use 7–8×10¹² as the normalization target**, and recommend the planner flag the CALC-01 wording so it is not mistaken for a ~30%-tighter target. (Cross-check: CONUS+ ~1.4×10¹³ at 20.7 m from 3.6 GW_th scales to (3/3.6)(20.7/25)² × 1.4×10¹³ ≈ 8×10¹² — consistent.)

### Limiting Cases

| Limit | Expected Behavior | Expression | Source |
| --- | --- | --- | --- |
| Integrate S_i over all E | ~6 ν̄/fission per isotope | ∫ S_i dE ≈ 6 | Hayes–Vogel |
| Integrate above 1.8 MeV | ~1.9 ν̄/fission | ∫_{1.8}^{∞} Φ_fission dE | reactor accounting |
| Toggle sub-1.8 MeV component off | Flux → 0 below ~1.8 MeV (the forbidden truncation) — used only as a labeled "conservative floor" variant | — | Pitfall 1 |
| d → any distance | Φ ∝ 1/d² | 1/(4πd²) | geometry |

### Numerical Benchmarks

| Quantity | Published Value | Method | Parameters | Source |
| --- | --- | --- | --- | --- |
| Ge CEvNS rate (downstream target this flux must reproduce) | 0.76 / 0.51 / 0.26 counts kg⁻¹ day⁻¹ >50/100/200 eV_nr | HM flux + spectrum constant <2 MeV | 8.54 GW_th, 400 m, f=55.6/32.6/7.1/4.7% | Billard 2017, Table 1 |
| Rescaled to this project (context only) | ~68/46/23 counts kg⁻¹ day⁻¹ (×~90 flux) | 1/r²+power scaling | 3 GW_th, 25 m | DERIVED (PRIOR-WORK.md) — recompute in Phase 3 |
| IBD yield per fission (optional cross-check) | ~6×10⁻⁴³ cm²/fission scale | σ_IBD-weighted ∫ | — | reactor ν̄ literature |

**Key insight:** Phase 2's absolute normalization and >2 MeV shape are tightly benchmarked (flux anchor + Billard reproduction). The sub-1.8 MeV region has *no* data anchor — its only checks are (a) the ²³⁸U(n,γ) yield magnitude ~0.6/fission and (b) internal consistency of the total ~6 ν̄/fission. This is why the wide below-2-MeV band is mandatory, not optional.

---

## Don't Re-derive

| Problem | Don't Derive From Scratch | Use Instead | Why |
| --- | --- | --- | --- |
| >2 MeV per-fission spectra | Converting ILL β spectra to ν̄ | Huber 2011 / Mueller 2011 coefficients (fetched) | Conversion involves virtual β-branch fitting; decades of subtlety, not reproducible in-phase |
| Sub-2 MeV fission spectrum | Full ENDF summation from scratch | CONFLUX or Estienne–Fallot table | Requires the entire fission-yield + β-decay database; a research program, not a task |
| ²³⁸U(n,γ) capture ν̄ shape | Building the ²³⁹U/²³⁹Np β→ν̄ spectra by hand | Kopeikin 2004 / Huber–Jaffke 2016 tabulated component | Known result; ~0.6/fission normalization is the number to import |
| Effective energy per fission | Summing decay heat + capture γ | Ma et al. 2014 values | Standard evaluated constants |
| Absolute normalization | — (this one you DO compute) | The R_f = P_th/⟨E_f⟩ → 1/(4πd²) chain, unit-tested | It is short and project-specific, but every step is a convention trap (Pitfall 2) — write it fresh with dimensioned asserts |

**Key insight:** the physics inputs are all published tabulations; the only thing Phase 2 legitimately *computes* is the assembly (stitch + capture add + normalization + uncertainty banding + freezing). Custom derivation of spectra is where errors and non-reproducibility enter.

---

## Common Pitfalls

### Pitfall 1: Truncating or power-law-extrapolating Huber–Mueller at 1.8 MeV (the forbidden proxy)

**What goes wrong:** Huber–Mueller is undefined below ~1.8–2 MeV; dropping the flux there (or extrapolating the >2 MeV fit downward) wipes out the sub-IBD flux that populates all recoils T ≲ 96 eV — exactly the QPD flagship bins.
**Why it happens:** HM is the "default" reactor flux; IBD experiments never needed the sub-threshold part.
**How to avoid:** Summation + ²³⁸U(n,γ) below 2 MeV, seam-matched; keep the sub-IBD flux as a togglable component and verify the T<96 eV bins respond when toggled (Phase 3 will do this fold).
**Warning signs:** discontinuity/hard cutoff at 1.8–2 MeV; quoted flux uncertainty <5% at low E_ν; low-recoil rate insensitive to the n-capture component.

### Pitfall 2: Normalization-chain errors (power → fission rate → flux)

**What goes wrong:** ×3 (GW_e vs GW_th), wrong energy/fission (total Q incl. neutrinos vs effective thermal), double-counting ~6 ν̄/fission on top of an already-per-fission spectrum, MeV↔J slips, 1/(4πd²) with diameter or wrong length unit.
**Why it happens:** it's a 4–5 step chain, each with a convention.
**How to avoid:** single unit-tested normalization function; use effective thermal ⟨E_f⟩ (Ma et al.), never total Q; the per-fission spectrum already integrates to ~6 — multiply only by R_f and 1/(4πd²); assert the result ≈ 7–8×10¹² ν̄ cm⁻² s⁻¹.
**Warning signs:** flux off from ~7×10¹² by >2×; folded rate off from Billard-scaled by >2×.

### Pitfall 3: Presenting the sub-1.8 MeV model as validated (band too small)

**What goes wrong:** carrying a single uniform ~5% band hides the ≳10–20% model uncertainty of the never-measured region and the imperfect power correlation of the ²³⁹Np-lifetime capture component.
**Why it happens:** one band is easier than two.
**How to avoid:** per-bin relative-uncertainty column with the band *split at ~1.8–2 MeV*: ~2–5% above, ~10–20% below. Document that below-2-MeV is model, not data.
**Warning signs:** uncertainty column constant across the seam; no separate treatment of the capture component's power-correlation caveat.

### Pitfall 4: Interpolation artifacts in the tabulated summation spectrum

**What goes wrong:** cubic-spline interpolation of sparse summation tables produces negative flux between points and rings at the 5 MeV bump.
**Why it happens:** naive spline on a kinked, sparse spectrum.
**How to avoid:** monotone PCHIP interpolation in log-flux; assert flux ≥ 0 everywhere; test at the bump and near the seam.
**Warning signs:** negative or oscillating flux; a spurious wiggle at 5–7 MeV.

### Pitfall 5: Discontinuity at the 1.8–2 MeV seam

**What goes wrong:** naively concatenating summation (<2 MeV) and Huber (>2 MeV) leaves a step where they disagree, biasing the folded low-recoil spectrum.
**Why it happens:** the two models have different absolute normalizations in the overlap.
**How to avoid:** per-isotope scale-match in a 2.0–3.0 MeV overlap window, then C¹ blend across 1.8–2.0 MeV; plot the joined curve and inspect the seam.
**Warning signs:** visible step at 2 MeV in Φ(E_ν); folded dR/dT kink near the corresponding recoil energy.

---

## Key Derivations and Formulas

### Per-fission spectrum (Huber–Mueller, >2 MeV)

```
# Source: Huber PRC 84, 024617 (2011) [235U,239Pu,241Pu]; Mueller PRC 83,054615 (2011) [238U]
S_i(E_ν) = exp( Σ_{p=1}^{6} α_{ip} E_ν^{p-1} )      [ν̄/fission/MeV], E_ν in MeV
```
**Valid when:** ~1.8/2 ≤ E_ν ≤ 8 MeV.
**Breaks down when:** E_ν < 1.8 MeV (undefined — use summation); coefficients α_{ip} MUST be fetched from source.

### Detector flux

```
Φ(E_ν) = [ Σ_i f_i S_i(E_ν) + S_capture(E_ν) ] × R_f × 1/(4π d²)
R_f = P_th / ⟨E_f⟩,   ⟨E_f⟩ = Σ_i f_i E_i (effective thermal)
```
**Valid when:** point-source approximation (d ≫ core size; 25 m vs few-m core is adequate at the target ~2× tolerance).
**Breaks down when:** finite-core / near-field geometry matters at the >10% level (not required here; note as a systematic).

### Seam-matching scale factor

```
c_i = [ ∫_{2.0}^{3.0} S_i^{HM}(E) dE ] / [ ∫_{2.0}^{3.0} S_i^{sum}(E) dE ]
S_i(E) = S_i^{HM}(E)          for E ≥ 2.0 MeV
       = c_i S_i^{sum}(E)     for E ≤ 1.8 MeV
       = smooth blend         for 1.8 < E < 2.0 MeV
```
**Valid when:** HM and summation overlap and are both ~valid in 2–3 MeV.
**Breaks down when:** the 5 MeV bump region is used for matching (avoid; match in 2–3 MeV, below the bump).

---

## Deliverable format (research-focus item 4)

**Recommended energy grid:** E_ν from **0 (or 0.1) to 10 MeV**, fine enough to resolve the folding integrand near E_ν,min(T)=√(MT/2) for the lowest recoil bins. Recommend a **linear grid at ~10–25 keV spacing** (≈400–1000 points) or a **log grid** with dense sampling below 2 MeV; either is fine provided the downstream Phase-3 fold uses PCHIP interpolation. Store the raw table plus a documented interpolation rule. (A log grid is natural for the CEvNS fold since the flux spans orders of magnitude; a linear grid is simpler to seam-blend. Recommend **log spacing with ≥ 20 points/decade**, floored at 0.1 MeV, with the n-capture component tabulated on the same grid.)

**Frozen CSV schema (versioned):**

```
# QPD reactor flux model — Phase 2 — version: v1.0 — generated: <date> — git: <sha>
# Normalization: 3 GW_th, d=25 m, <E_f>=<value> MeV/fission, fission fractions 235:238:239:241=0.58:0.07:0.30:0.05
# Sources: Huber PRC84,024617 (>2 MeV 235/239/241); Mueller PRC83,054615 (238U); <summation source> (<2 MeV); Kopeikin2004/Huber-Jaffke2016 (238U(n,g))
# Integral checks: total nu/fission=<>, above-1.8MeV nu/fission=<>, flux=<> nu/cm2/s
columns:
  E_nu_MeV,
  flux_nu_per_cm2_per_s_per_MeV,        # total Φ(E_ν)
  flux_fission_HM,                       # >2 MeV Huber–Mueller fission component
  flux_fission_summation,                # <2 MeV summation fission component (seam-matched)
  flux_ncapture_238U,                    # 238U(n,γ) capture component
  rel_uncertainty,                       # per-bin fractional 1σ
  region_flag                            # "above_2MeV" | "below_1p8MeV" | "seam"
```

Keep components as separate columns so any can be toggled/re-banded without regenerating; freeze with a version header and provenance; commit the generator script alongside.

---

## Validation Strategies (research-focus item 5)

| Check | Target | Source |
| --- | --- | --- |
| Total ν̄/fission | ∫ Σ_i f_i S_i dE ≈ 6 | Hayes–Vogel |
| Above-IBD ν̄/fission | ∫_{1.8}^{∞} ≈ 1.9 | reactor accounting |
| ²³⁸U(n,γ) yield | S_capture integrates to ≈ 0.6 ν̄/fission | Kopeikin 2004 |
| Integral detector flux | **∫ Φ dE ≈ 7–8×10¹² ν̄ cm⁻² s⁻¹** | Phase-1 lock; verified above |
| >2 MeV shape | overlay Φ(E_ν) on a published Huber ²³⁵U curve; agree within stated band | Huber 2011 figures / bradkav/CEvNS |
| Sub-1.8 MeV magnitude | sub-IBD flux is a large fraction (~60–70% by number of the total ν̄); n-capture bump present ≲1.3 MeV | Pitfall 1 quantification; Kopeikin |
| Seam continuity | no step at 1.8–2 MeV; C¹ across blend | internal |
| Non-negativity | Φ ≥ 0 on the whole grid | PCHIP guard |
| Normalization unit test | dimensioned assert: R_f in fissions/s, Φ in ν̄ cm⁻² s⁻¹ MeV⁻¹ | Pitfall 2 |
| Billard-variant closure (for Phase 3) | HM + constant-below-2-MeV + f=55.6/32.6/7.1/4.7% variant reproduces Billard flux assumptions | Billard 2017 |

---

## Open Questions

1. **Which summation dataset for sub-1.8 MeV?**
   - What we know: CONFLUX (arXiv:2503.18966) and Estienne–Fallot 2019 both cover the region; arXiv:2304.14992 is a further revision. Liao–Liu–Marfatia (arXiv:2302.10460) frames the sensitivity.
   - What's unclear: exact digitized values and whether CONFLUX output is preferred over a fixed published table for reproducibility.
   - Recommendation: **use CONFLUX as generator, Estienne–Fallot 2019 as cross-check** (or Estienne–Fallot as primary if CONFLUX install is undesirable); carry the spread between the two as part of the below-2-MeV band. Decide at planning time based on install effort; either is defensible.

2. **Exact Huber/Mueller coefficients.**
   - What we know: functional form `exp(Σ_{p=1}^{6} α_{ip} E^{p-1})`, 6 coefficients/isotope, confirmed this session.
   - What's unclear: the numeric α_{ip} — NOT reproduced here to avoid fabrication.
   - Recommendation: fetch from Huber PRC 84,024617 and Mueller PRC 83,054615; cross-check against bradkav/CEvNS coefficient tables; unit-test the reconstructed ²³⁵U spectrum against a published figure before use.

3. **Fission-fraction set and its band.**
   - What we know: default 0.58:0.07:0.30:0.05 (235:238:239:241); Billard used 55.6/32.6/7.1/4.7 (235/239/238/241).
   - What's unclear: the specific reactor's fuel state (not specified in the contract).
   - Recommendation: default cycle-averaged set as baseline (tunable), BOC/EOC as a shape-systematic band; Billard set available as a switch for benchmark reproduction.

4. **Finite-core geometry.**
   - What we know: point-source 1/(4πd²) at 25 m is adequate for ~2× tolerance.
   - What's unclear: percent-level correction from core extent.
   - Recommendation: point source baseline; note finite-core as a small systematic, out of scope for Stage-1.

---

## What Was NOT Found

- **Exact Huber/Mueller α_{ip} coefficient values** were deliberately not transcribed (must be fetched from the primary papers; fabricating them is forbidden). Web search confirmed only the functional form and coefficient count.
- **A single authoritative digitized sub-1.8 MeV per-isotope table** with quoted uncertainties was not pinned to specific numbers this session; CONFLUX / Estienne–Fallot are the named sources to extract it from at planning time.
- **The precise ²³⁸U(n,γ) ν̄ spectral shape** (vs its ~0.6/fission integral) was not tabulated here; import from Kopeikin 2004 / Huber–Jaffke 2016.
- No source contradicts the ~7–8×10¹² ν̄ cm⁻² s⁻¹ normalization; the only tension is the loosely-rounded "~1×10¹³" in REQUIREMENTS.md CALC-01 (order-of-magnitude, not a discrepancy).

---

## Caveats and Alternatives (adversarial self-critique)

- **Am I overconfident on normalization?** The 7–8×10¹² figure depends on ~6 ν̄/fission and ~205 MeV/fission, both good to a few %, and the point-source approximation. At the contract's ~2× tolerance this is safe, but the *shape* of the sub-IBD flux (not its normalization) is the real risk — and I have flagged it MEDIUM with a 10–20% band. If Stage-1 conclusions ever hinge on <10% low-recoil accuracy, this phase is the bottleneck, and no amount of care removes the fact that the region is unmeasured.
- **Is the seam-match physically justified?** Scaling summation onto Huber in 2–3 MeV assumes the summation *shape* is trustworthy where its *normalization* may not be. If summation shape is itself biased at low E, the seam-match propagates that. Mitigation: carry the CONFLUX-vs-Estienne–Fallot spread in the band; do not present the joined curve as better-known than either input.
- **Could truncation ever be defensible?** Only as an explicitly-labeled "conservative floor" variant for a sensitivity cross-check — never as the flagship. The contract forbids it as the deliverable; I keep it only as a toggle for testing Pitfall-1 sensitivity.
- **CALC-01 wording risk.** The "~1×10¹³" requirement text could be read as a tighter target than 7–8×10¹². I recommend the planner add a note (or a requirement clarification) that 7–8×10¹² is authoritative, to avoid a spurious "off by 30%" verification flag downstream.
- **Fission-fraction ambiguity.** Different papers order isotopes differently; a silent mislabel would swap ²³⁸U and ²³⁹Pu fractions (0.07 vs 0.30) and distort the spectrum. I have flagged the ordering explicitly; the plan must unit-test that f_i are attached to the correct isotope.
- **Alternative worth stating:** a full-summation-everywhere model (no HM) sidesteps the anomaly and the seam entirely, at the cost of larger >2 MeV uncertainty and losing the data anchor. Offered as a switch, not the baseline, because the contract names ref-huber and Phase 3 must reproduce Billard (which used HM).

---

## Sources

### Primary (HIGH)

- Huber, PRC 84, 024617 (2011), arXiv:1106.0687 — >2 MeV ²³⁵U/²³⁹Pu/²⁴¹Pu conversion spectra; `exp(Σα_p E^{p-1})` form (anchor ref-huber). *Form confirmed via web search this session; coefficients to be fetched.*
- Mueller et al., PRC 83, 054615 (2011), arXiv:1101.2663 — ²³⁸U summation spectrum; Huber–Mueller combination.
- Billard et al., J. Phys. G 44, 105101 (2017), arXiv:1612.09035 — downstream benchmark; its flux assumptions (HM, constant <2 MeV, fission fractions).
- Ma et al., PRC 88, 014605 — effective thermal energy per fission per isotope.
- Hayes & Vogel, ARNPS 66, 219 (2016), arXiv:1605.02047 — ~6 ν̄/fission, ~2×10²⁰ ν̄ s⁻¹ GW_th⁻¹ normalization anchors.
- Phase-1 `GPD/CONVENTIONS.md` (Sections A, C, D, G) — locked units, 3 GW_th, 25 m, Φ definition, ~7–8×10¹² target.

### Secondary (MEDIUM)

- CONFLUX, Zhang et al., arXiv:2503.18966 (2025) — summation framework for sub-2 MeV. *Existence/scope confirmed via web search.*
- Estienne, Fallot et al., PRL 123, 022502 (2019) — updated summation spectrum (Daya Bay agreement); sub-2 MeV cross-check.
- Comprehensive summation revision, arXiv:2304.14992 (2023) — alternative summation fluxes/uncertainties.
- Kopeikin, Mikaelyan, Sinev, Phys. At. Nucl. 67, 1892 (2004), hep-ph/0308186; Huber & Jaffke, PRL 116, 122503 (2016) — ²³⁸U(n,γ) capture ν̄ component (~0.6/fission).
- Liao, Liu, Marfatia, PRD 108, 033002 (2023), arXiv:2302.10460 — sub-1.8 MeV CEvNS sensitivity framing.
- Kopeikin, Skorokhvatov, Titov, PRD 104, L071301 (2021), arXiv:2103.01684 — KI ~5% ²³⁵U rescaling (optional switch).
- Hayen & Kostensalo (eds.), arXiv:2310.13070 (2024) — anomaly / 5 MeV bump systematics.
- Project literature: `GPD/literature/METHODS.md` (Domain 1 flux recipe), `PITFALLS.md` (Pitfalls 1,2), `PRIOR-WORK.md` (Kopeikin/Estienne–Fallot entries), `SUMMARY.md` (Phase-2 rationale).
- `bradkav/CEvNS`, arXiv:1805.01798 — digitized HM coefficients + flux-build cross-check oracle.

### Tertiary (LOW — needs validation at execution time)

- Vogel–Engel analytic per-isotope form, PRD 39, 3378 — crude fallback only.
- Haag et al. 2014 measured ²³⁸U — optional >4 MeV refinement.
- CONUS+ ~1.4×10¹³ at 20.7 m (Nature 643, 1229 (2025)) — used only as an independent normalization scaling cross-check.

---

## Metadata

**Research scope:**
- Physics subfield: reactor antineutrino flux modeling (conversion + summation), CEvNS input flux
- Methods explored: Huber–Mueller conversion parameterization, summation method (CONFLUX / Estienne–Fallot), ²³⁸U(n,γ) capture component, seam-matching, power→flux normalization chain
- Known results catalogued: ~6 ν̄/fission, ~1.9 above IBD, ~0.6 n-capture, 7–8×10¹² flux (verified), effective energy/fission
- Pitfalls: truncation at IBD threshold, normalization chain, band-too-small, interpolation artifacts, seam discontinuity

**Confidence breakdown:**
- Literature coverage: HIGH — sources named in project files and cross-checked; two web verifications this session
- Methods: HIGH above 2 MeV (data-anchored); MEDIUM below 1.8 MeV (model-only, wide band by design)
- Known results: HIGH for normalization/yields (verified arithmetic); MEDIUM for sub-IBD shape
- Pitfalls: HIGH — mapped directly from PITFALLS.md Pitfalls 1–2 plus interpolation/seam traps

**Research date:** 2026-07-20
**Valid until:** 2026-08-19 (30 days; established reactor-flux physics, though CONUS+ follow-ups and summation revisions warrant a re-check if the sub-IBD band becomes conclusion-critical)

---

_Phase: 02-reactor-flux-model_
_Research completed: 2026-07-20_
_Ready for planning: yes_
