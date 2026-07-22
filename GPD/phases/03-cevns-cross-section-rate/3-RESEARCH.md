# Phase 3: CEvNS Cross Section & Rate - Research

**Researched:** 2026-07-20
**Domain:** Reactor coherent elastic neutrino-nucleus scattering (CEvNS); deterministic flux-folded differential rate on natural germanium in deposited nuclear-recoil energy
**Depth:** standard
**Confidence:** HIGH (cross section, isotope sum, closed-form check, Billard assumptions — primary source read); MEDIUM (Helm near-endpoint magnitude, sub-1.8 MeV band propagation)

<user_constraints>

## User Constraints (from CONTEXT.md)

No `CONTEXT.md` exists for this phase (`gpd:discuss-phase` was not run). There are therefore no locked per-phase user decisions. **However, this phase is heavily constrained by Phase-1 locked conventions and Phase-2 frozen artifacts**, which act as binding inputs (see Active Anchor References). All physics choices below build on those and must not re-open them.

**Agent's discretion (recommendations given, planner may choose):** recoil-energy grid spacing and range; flux-interpolation scheme; quadrature method; whether to expose the defect-storage systematic in Phase 3 or defer to Phase 5.

**Out of scope for Phase 3:** detector response (ε=0.5, bandwidth censoring, reconstructed energy) — that is Phase 5; muon/Compton channels — Phase 4; any ionization-quenching treatment — forbidden by CONVENTIONS Section B.
</user_constraints>

## Active Anchor References

These are mandatory inputs, not background reading. The planner must wire each into tasks.

| Anchor | What it fixes | How Phase 3 uses it |
| --- | --- | --- |
| `GPD/CONVENTIONS.md` Section C (LOCKED) | dσ/dT form, **/4π** prefactor, Q_W = N−(1−4sin²θ_W)Z, sin²θ_W=0.2387, (ħc)²=3.894×10⁻²⁸ GeV²·cm², Helm FF, σ_tot closed form | USE verbatim; do NOT re-choose. Cross-section coefficient and unit tests already fixed here. |
| `GPD/CONVENTIONS.md` Sections A.2, D, G | (ħc)² conversion; Ge atoms/kg = 8.29×10²⁴; per-kg normalization; symbol registry | Unit discipline + target normalization. |
| `src/qpd_potential/cevns.py` (Phase 1) | `weak_charge(Z,N)`, `sigma_tot(E_nu_GeV,Z,N)`, `sigma_tot_MeV(...)` closed-form total | EXTEND this module: add Helm FF, dσ/dT, isotope sum, rate fold. `sigma_tot` is the closed-form normalization check. |
| `src/qpd_potential/params.py` (Phase 1) | G_F, (ħc)², sin²θ_W, 1−4sin²θ_W, CEVNS_PREFACTOR_DENOM=4π, Ge atoms/kg, ρ, molar mass | Pull all constants from here; do not hardcode. Note: only `72Ge` is registered (`BENCHMARK_ISOTOPE`); Phase 3 must add the full 5-isotope table. |
| `data/flux/reactor_flux_v1.0.csv` (Phase 2, FROZEN) | Flagship Φ(E_ν), 3 GW_th / 25 m, ∫Φ dE = 7.50×10¹²; 7-col schema with `rel_uncertainty`, `region_flag` | The flagship fold input (CALC-02 dR/dT and the CONUS+/rescaled comparison). |
| `data/flux/reactor_flux_billard_variant.csv` (Phase 2) | Billard **spectral-shape** assumptions (HM held constant below 2 MeV; fractions 55.6/32.6/7.1/4.7; no n-capture); normalized at 3 GW_th / 25 m, ∫Φ dE = 4.586×10¹² | VALD-01 Table-1 reproduction — but **renormalize to Billard's 8.54 GW / ~400 m config first** (see Existing Results §Billard). |
| `ref-cevns-benchmark` — Billard et al., J. Phys. G 44, 105101 (2017), arXiv:1612.09035 | Table 1 Ge rates 0.76/0.51/0.26 counts/kg/day above 50/100/200 eV_nr; assumptions read this session | VALD-01 primary benchmark (~20%). |
| `ref-huber` (Huber 2011 / Mueller 2011) | Reactor ν̄ spectra above 2 MeV | Already embedded in the frozen flux; no re-derivation. |
| CONUS+ baseline (Nature 643, 1229 (2025)) | Ge-at-reactor rate scale | Secondary VALD-01 sanity (factor ~2), eV_ee scale → needs quenching caveat, cross-check only. |

<research_summary>

## Summary

Phase 3 computes the per-isotope-summed CEvNS differential rate dR/dT on natural Ge in **deposited** nuclear-recoil energy, by folding the Phase-1 Freedman cross section (with Helm form factor) against the Phase-2 frozen flux. Every physics ingredient except the Helm form factor and the rate-folding loop is already locked in `CONVENTIONS.md` Section C and partially implemented in `cevns.py`. The phase is a deterministic 1-D quadrature problem (no Monte Carlo), cheap (<seconds), and its correctness is anchored by two independent checks: (a) the closed-form total cross section σ_tot = G_F²Q_W²E_ν²/(4π)·(ħc)² already coded as `sigma_tot`, and (b) reproduction of Billard (2017) Table 1.

The two subtleties that most affect correctness are (1) **the per-isotope sum**: natural Ge is five isotopes (⁷⁰/⁷²/⁷³/⁷⁴/⁷⁶Ge) with different N (38–44), hence different Q_W, nuclear mass M_i, kinematic endpoint T_max^(i), and minimum neutrino energy E_min^(i)(T) — the rate MUST sum per isotope weighted by number-abundance, never use a lumped A=72.63; and (2) **the Billard normalization**: the frozen `billard_variant.csv` carries Billard's *spectral shape* but our 3 GW_th/25 m *normalization* — Billard's Table 1 is at Chooz's **8.54 GW combined thermal power at ~400 m** (two cores at 355.39 and 468.76 m), so the variant flux must be renormalized by a factor ≈ 0.0111 before it reproduces 0.76/0.51/0.26. This is not stated in the CSV and is the single most likely way to "fail" VALD-01 for a spurious reason.

The Helm form factor is a genuine but small correction: F² > 0.996 across the flagship Billard thresholds (50–200 eV), but my quick calculation shows it falls to ~0.95 near the ~2 keV recoil endpoint — so implement Helm properly (it is nearly free) rather than setting F=1, but expect it to shift the integrated Billard rates by <1%.

**Primary recommendation:** Extend `src/qpd_potential/cevns.py` with a Helm form factor, a per-isotope `dsigma_dT`, and a flux-folding `differential_rate(T)` that sums over the five Ge isotopes reading the frozen CSVs; validate against `sigma_tot` (closed form, <0.1%) and Billard Table 1 (renormalized, ~20%); carry the split flux band into the dR/dT uncertainty, wide (20–25%) below T≈95 eV.
</research_summary>

<literature_landscape>

## Literature Landscape

### Foundational Papers

| Paper | Authors | Year | Key Result | Relevance |
| --- | --- | --- | --- | --- |
| Coherent effects of a weak neutral current | Freedman | 1974 | SM CEvNS cross section dσ/dT (the "/4π" form) | The cross section implemented here (CONVENTIONS Sec C). |
| Review of mathematics, numerical factors... for dark matter (Helm FF) | Lewin & Smith | 1996 | Helm form factor parameters (c, a, s) for nuclear recoils | The exact Helm parameterization to implement. |
| Coherent Neutrino Scattering with Low Temperature Bolometers at Chooz Reactor Complex | Billard, Carr, Dawson, et al. | 2017 | Table 1 Ge rates 0.76/0.51/0.26 counts/kg/day above 50/100/200 eV; 8.54 GW, 400 m, HM constant below 2 MeV | VALD-01 primary benchmark. Table 1 + assumptions read this session (arXiv:1612.09035). |

### Recent Advances

| Paper | Authors | Year | Key Result | Relevance |
| --- | --- | --- | --- | --- |
| Impact of form-factor uncertainties on CEvNS interpretations | Aristizabal Sierra, De Romeri, Rojas | 2019 | Form-factor / neutron-radius uncertainties irrelevant for reactor CEvNS (matter only for q ≳ 20–50 MeV) | Justifies Helm-as-completeness, not a systematic driver, in the flagship low-recoil bins. |
| Reactor CEvNS on Ge: CONUS+ and TEXONO... | De Romeri et al. | 2025 | Ge-at-reactor SM rate framework; form-factor insensitivity at reactor q | Secondary rate-scale cross-check (arXiv:2501.18550), eV_ee scale. |
| CONUS+ observation | CONUS+ Collab. | 2025 | Measured Ge CEvNS at reactor (Nature 643, 1229) | Factor-~2 external anchor for the flagship rate (needs quenching caveat). |

### Review Articles and Textbook Treatments

| Source | Authors | Coverage | Best For |
| --- | --- | --- | --- |
| `GPD/literature/METHODS.md` (project) | this project | Freedman σ, Helm, flux fold recipe, quadrature | The prescriptive method already vetted for this project. |
| `GPD/literature/PITFALLS.md` (project) | this project | 12 CEvNS/detector pitfalls with warning signs | The failure-mode catalogue Phase 3 must guard. |

### Notation Conventions Across Papers

| Quantity | Billard (2017) | Project (CONVENTIONS) | Our convention | Notes |
| --- | --- | --- | --- | --- |
| Recoil energy | E_R | T ≡ E_nr | **T** (keV_nr / eV_nr, deposited) | Same quantity; no quenching. |
| Nuclear mass | M_A | M | **M_i** per isotope | Billard uses one M_A per material; we sum isotopes. |
| Weak charge | Q_W = N − Z(1−4sin²θ_W) | Q_W = N − (1−4sin²θ_W)Z | identical | ✓ Billard's Eq. 1 matches CONVENTIONS Sec C exactly, including /4π. |
| Cross section | dσ/dE_R = (G_F²/4π)M_A Q_W²(1−M_A E_R/2E_ν²)F² | dσ/dT = (G_F²M/4π)Q_W²(1−MT/2E_ν²)F² | identical | ✓ Same prefactor, same kinematic truncation. |

**Key notational hazard:** Billard's Table-1 caption says "reactor power of 8.54 GW, detector distance of 400 m," while the text gives two cores at 355.39 m and 468.76 m with 4.27 GW each. These are numerically equivalent geometry factors (see Existing Results); do not double-count power or distance.
</literature_landscape>

<methods_and_approaches>

## Methods and Approaches

### Standard Analytical Methods

| Method | When to Use | Limitations | Key Reference |
| --- | --- | --- | --- |
| Freedman SM dσ/dT with truncated kinematic factor (1−MT/2E_ν²) | The whole cross section | Drops O(T/E_ν)~10⁻³ subleading terms −T/E_ν+T²/2E_ν² (standard at reactor E) | CONVENTIONS Sec C; Billard Eq. 1 |
| Helm form factor F(q)=3j₁(qR₀)/(qR₀)·exp(−q²s²/2) | Nuclear FF for all T | ≈1 at flagship recoils; ~few-% near endpoint | Lewin & Smith 1996 |
| Per-isotope deterministic flux fold (1-D quadrature) | dR/dT on natural Ge | Requires per-isotope kinematic domains | METHODS.md Domain 1 |
| Closed-form σ_tot = G_F²Q_W²E_ν²/(4π)·(ħc)² | Normalization cross-check | Valid in M≫E_ν, F=1 limit | `cevns.py::sigma_tot` |

### Package / Framework Reuse Decision

**Decision: extend existing project code (thin, bespoke additions to `src/qpd_potential/cevns.py`); reuse SciPy/NumPy for quadrature and interpolation. No new framework.**

- `cevns.py` already provides `weak_charge`, `sigma_tot`, `sigma_tot_MeV` with the locked constants pulled from `params.py`. Phase 3 adds, in the same module and unit discipline: `helm_form_factor(q_or_T, ...)`, `dsigma_dT(E_nu, T, Z, N, M)`, a Ge isotope table, and `differential_rate(T, flux_csv)` that folds and sums.
- **Why not a external CEvNS package** (e.g. a public reactor-CEvNS code): the project has already *locked* its own conventions and unit tests (the /4π, (ħc)², sin²θ_W=0.2387 choices); importing an external package would re-introduce exactly the convention-mismatch risk PITFALLS.md §3/§5 warn about, and would not read the project's frozen flux CSVs or per-isotope schema. The missing capability (per-isotope sum over *this* Ge abundance table, folded with *this* frozen flux, in *this* deposited-energy convention) is small and project-specific — a thin extension is lower-risk than adapting a general package.
- **Reuse SciPy** for `scipy.integrate.quad`/fixed Gauss-Legendre (the E_ν integral) and `scipy.interpolate.PchipInterpolator` (monotone, non-ringing flux interpolation in log-flux — PITFALLS.md numerical trap). `scipy.special.spherical_jn` for j₁ in the Helm FF.

### Computational Tools

| Tool/Package | Version | Purpose | Why Standard |
| --- | --- | --- | --- |
| Python + NumPy | ≥3.11 | arrays, grids | project baseline |
| SciPy | current | `integrate.quad`, `interpolate.PchipInterpolator`, `special.spherical_jn` | smooth 1-D fold; monotone flux interp; Bessel j₁ |
| matplotlib | current | dR/dT figures, isotope-endpoint plot, band overlay | deliv-fig |
| pytest | current | closed-form + Billard + endpoint acceptance tests | project test harness (57/57 passing) |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
| --- | --- | --- |
| Helm form factor | Klein–Nystrand (COHERENT convention) | Equivalent at reactor q (<0.5% difference below 200 eV); not worth choosing — Helm matches CONVENTIONS/Lewin–Smith. Do NOT import a COHERENT-tuned FF with fm⁻¹/MeV unit mismatch (PITFALLS §5). |
| Truncated kinematic factor (1−MT/2E_ν²) | Full (1−T/E_ν−MT/2E_ν²) | ~10⁻³ at reactor E; truncated form is the CONVENTIONS/Billard choice — keep it, document truncation. |
| `scipy.quad` per T | Fixed Gauss–Legendre on log-E_ν grid | Both fine (smooth integrand); quad is safer near the steep flux×threshold at E_min(T). |
| Lumped A=72.63 | — | FORBIDDEN (PITFALLS §4): smooths endpoints, biases near-threshold and near-endpoint bins. |

**Installation / Setup:**

```bash
# Already in the project environment; no new dependencies.
uv sync   # scipy/numpy/matplotlib/pytest already present
```
</methods_and_approaches>

<known_results>

## Known Results and Benchmarks

### Established Results (USE, do not re-derive)

| Result | Value/Expression | Conditions | Source | Confidence |
| --- | --- | --- | --- | --- |
| dσ/dT form + /4π prefactor | (G_F²M/4π)Q_W²(1−MT/2E_ν²)F² | tree-level SM | CONVENTIONS Sec C | HIGH |
| σ(⁷²Ge, 4 MeV) full Q_W | ≈ 1.0×10⁻⁴⁰ cm² | Q_W=N−(1−4sin²θ_W)Z | CONVENTIONS Sec C | HIGH |
| σ coefficient | ≈ 4.22×10⁻⁴⁵ N²(E_ν/MeV)² cm² | N-dominant | CONVENTIONS Sec C | HIGH |
| (ħc)² conversion | 3.894×10⁻²⁸ GeV²·cm² | mandatory | CONVENTIONS Sec A.2 | HIGH |
| Ge atoms/kg (total) | 8.29×10²⁴ | natural abundance | CONVENTIONS Sec D / `params.py` | HIGH |
| Frozen flagship flux integral | ∫Φ dE = 7.50×10¹² ν cm⁻²s⁻¹ | 3 GW_th, 25 m | Phase-2 SUMMARY / CSV header | HIGH |
| Billard Table 1 (Ge) | 0.76 / 0.51 / 0.26 counts/kg/day above 50 / 100 / 200 eV | 8.54 GW, ~400 m, HM flat <2 MeV, ±5% | Billard 2017 Table 1 (read) | HIGH |

### Germanium isotope table (per-isotope sum — CALC-02 core)

Number (mole) abundances and neutron numbers (Z=32 for all). Abundances are standard IUPAC/NIST representative isotopic composition; the task-prompt values (20.6/27.4/7.8/36.5/7.8) round these.

| Isotope | Z | N | Abundance x_i (number frac) | Atomic mass (u) | Nuclear mass M_i ≈ A·931.494 MeV |
| --- | --- | --- | --- | --- | --- |
| ⁷⁰Ge | 32 | 38 | 0.2057 | 69.9243 | ≈ 65.13 GeV |
| ⁷²Ge | 32 | 40 | 0.2745 | 71.9221 | ≈ 66.99 GeV |
| ⁷³Ge | 32 | 41 | 0.0775 | 72.9235 | ≈ 67.93 GeV |
| ⁷⁴Ge | 32 | 42 | 0.3650 | 73.9212 | ≈ 68.86 GeV |
| ⁷⁶Ge | 32 | 44 | 0.0773 | 75.9214 | ≈ 70.72 GeV |

- Per-isotope target number: **N_target,i = x_i · 8.29×10²⁴ /kg** (mole fraction × total atoms/kg; Σ_i = 8.29×10²⁴). [HIGH]
- Use M_i = A_i · 931.494 MeV (or the atomic mass in u × 931.494; nuclear vs atomic mass differs <0.1% and is negligible here). [HIGH]
- Q_W,i = weak_charge(32, N_i) from `cevns.py`. Q_W ranges from ~36.6 (⁷⁰Ge) to ~42.6 (⁷⁶Ge); the rate weight Q_W,i² spans ~±16%. [HIGH]
- ⁷³Ge nuclear spin gives a spin-dependent/axial term that is ~1/N² suppressed and negligible for the rate — state it, do not model it. [HIGH — PITFALLS §4]

### Limiting Cases

| Limit | Expected Behavior | Expression | Source |
| --- | --- | --- | --- |
| ∫₀^{Tmax} dσ/dT dT (F=1) | equals closed-form total | = G_F²Q_W²E_ν²/(4π)·(ħc)² = `sigma_tot` | derived §Key Derivations; verify <0.1% |
| T → 0 | dσ/dT → (G_F²M/4π)Q_W²·(ħc)² (flat, F²→1) | finite | CONVENTIONS Sec C |
| T → T_max(E_ν) | kinematic factor → 0 | (1−MT/2E_ν²)→0 | Freedman |
| q → 0 | F(0)=1 | Helm | Lewin–Smith |
| E_ν < E_min(T)=√(MT/2) | no contribution | integration lower limit | METHODS.md |

### Numerical Benchmarks / kinematic anchors

| Quantity | Value | Source |
| --- | --- | --- |
| T_max(E_ν) per isotope | 2E_ν²/(M_i+2E_ν) | e.g. at E_ν=8 MeV: ~1.96 keV (⁷⁰Ge) vs ~1.81 keV (⁷⁶Ge) — five distinct steps | PITFALLS §4 |
| E_min(T) (Ge, M≈67.7 GeV) | √(MT/2): 10 eV→0.58 MeV; 50 eV→1.29 MeV; 95 eV→1.78 MeV; 100 eV→1.83 MeV; 200 eV→2.59 MeV | this session (verified vs PITFALLS anchor) |
| Reactor ν̄ mean/endpoint | ⟨E_ν⟩≈3.6 MeV, endpoint ≈10 MeV | Billard 2017 §1 |
| F²(Ge) at 200 eV / ~2 keV | ≈0.996 / ≈0.95 (quick calc, MEDIUM) | this session (verify in code) |

**Key insight:** Because E_min(T=95 eV)≈1.78 MeV, only recoils **below ~95 eV** draw on the sub-1.8-MeV flux — exactly the Kopeikin-2012 placeholder region with the wide 20–25% band. Above ~200 eV the rate is set entirely by the well-anchored (2–5% band) >2 MeV flux. This cleanly localizes the flux systematic in the flagship low-recoil bins.
</known_results>

<dont_rederive>

## Don't Re-derive

| Problem | Don't Derive From Scratch | Use Instead | Why |
| --- | --- | --- | --- |
| Cross-section normalization / prefactor | Re-deriving /4π vs /8π, Q_W, sin²θ_W | CONVENTIONS Sec C + `cevns.py` | LOCKED and unit-tested; re-deriving invites the /8π and (ħc)² traps (PITFALLS §3). |
| Total cross section | Re-implementing σ_tot | `cevns.py::sigma_tot` | Already coded; it is the closed-form check for the differential. |
| Reactor flux Φ(E_ν) | Re-building Huber–Mueller + summation + n-capture | `reactor_flux_v1.0.csv` (frozen) / `billard_variant.csv` | Phase-2 deliverable, provenance-tagged, band-split, benchmarked to Huber <4.4%. |
| Flux normalization chain | Re-deriving R_f = P_th/⟨E_f⟩·1/(4πd²) | Read it from the CSV (flagship); for Billard, apply the geometry rescale (§Billard) | Phase-2 applied it exactly once; re-doing risks the ×6 / GW_e / total-Q traps (PITFALLS §2). |
| Weak mixing angle scheme | Choosing sin²θ_W | 0.2387 (low-E MS-bar) from `params.py` | LOCKED; 0.2312 (M_Z) is wrong here (PITFALLS §3). |

**Key insight:** Nearly every convention-bearing number is already locked and machine-checked (`tests/test_conventions_consistency.py`). Phase-3's job is the *fold and the isotope sum*, plus the Helm FF — not the constants.
</dont_rederive>

<common_pitfalls>

## Common Pitfalls

(Full catalogue in `GPD/literature/PITFALLS.md` §§2–5; the Phase-3-critical ones, plus one new finding.)

### Pitfall 1: Billard normalization mismatch (NEW — highest-risk for VALD-01)

**What goes wrong:** Folding `reactor_flux_billard_variant.csv` at its stored 3 GW_th / 25 m normalization (∫Φ=4.586×10¹²) and comparing to Table 1 gives Ge rates ~90× too high (~40 vs 0.76 counts/kg/day). The variant encodes Billard's *spectral shape*, not Billard's *flux magnitude*.
**Why it happens:** The CSV header says "3 GW_th, 25 m" and does not state Billard's actual Chooz config (8.54 GW combined at 355.39 m + 468.76 m ≈ single 8.54 GW at 400 m). CONVENTIONS Sec C's Billard reference-map note ("rescale flux (3 GW_th, 25 m) only") is about rescaling *Billard→our config* for the flagship comparison, NOT about reproducing Table 1.
**How to avoid:** Before the Table-1 fold, multiply the variant flux by the geometry+power factor
`k = (P_B/P_v)·(G_B/G_v) = (8.54/3)·[(1/(4π·355.39²·½)+1/(4π·468.76²·½)) / (1/(4π·25²))]` in consistent length units. With distances in cm this evaluates to **k ≈ 0.0111** (single-source 8.54 GW at 400 m and the two-core sum agree to <1%). Expected Billard integral flux ≈ 5.1×10¹⁰ ν cm⁻²s⁻¹.
**Warning signs:** Table-1 reproduction off by a clean ~90× or ~1/90×; "rate" of tens of counts/kg/day above 50 eV.

### Pitfall 2: Lumped A instead of per-isotope sum

**What goes wrong:** Using one A=72.63, M, Q_W, T_max smooths the five-step endpoint structure and biases near-threshold/near-endpoint bins (PITFALLS §4).
**How to avoid:** Loop over the five isotopes with their own N_i, M_i, Q_W,i, T_max^(i), E_min^(i), integrate each on its own kinematic domain, weight by x_i·8.29×10²⁴, sum.
**Warning signs:** Single sharp endpoint instead of a stepped superposition; per-kg rate quoted as ∝N² without threshold discussion.

### Pitfall 3: (ħc)² omission / /4π vs /8π

**What goes wrong:** σ left in GeV⁻² (≈10²⁸× too large) or a factor-2 from /8π (PITFALLS §3).
**How to avoid:** Reuse `params.HBARC2` and `params.CEVNS_PREFACTOR_DENOM`; assert dσ/dT integrates to `sigma_tot`; assert σ(⁷²Ge,4 MeV)≈1.0×10⁻⁴⁰ cm².
**Warning signs:** Rate off by ~4× (prefactor) or ~10²⁸× (units).

### Pitfall 4: Coarse E_ν grid near E_min(T) / spline ringing in flux

**What goes wrong:** Jagged/biased dR/dT at low T where the steep flux meets the E_min(T) threshold; cubic-spline flux interpolation produces negative flux / ringing near the 5 MeV bump (PITFALLS numerical traps).
**How to avoid:** Log-spaced E_ν grid or adaptive `quad`; interpolate the tabulated flux with **PCHIP in log-flux** (monotone, non-negative). Integrate each isotope on its own T-grid domain.
**Warning signs:** Negative flux values; jagged low-T spectrum; per-isotope steps at wrong T.

### Pitfall 5: Applying quenching / wrong energy scale

**What goes wrong:** Multiplying T by a Lindhard yield, or mixing eV_ee/eV_nr — suppresses CEvNS ~5–7× (PITFALLS §6, CONVENTIONS Sec B forbidden).
**How to avoid:** Phase-3 output axis is **deposited nuclear-recoil energy T = E_nr**, no quenching, no ε (ε and reconstruction are Phase 5). Defect-storage is a few-% NR-only *systematic band*, optional here.
**Warning signs:** Any "eV_ee" in the CEvNS pipeline; CEvNS rate ~5× below a phonon-scale benchmark.
</common_pitfalls>

<key_derivations>

## Key Derivations and Formulas

### 1. Differential cross section (per isotope) — CONVENTIONS Sec C

```
# Source: CONVENTIONS.md Sec C; Freedman 1974; Billard 2017 Eq. 1
dσ_i/dT (E_ν, T) = (G_F² M_i / 4π) · Q_W,i² · (1 − M_i T / (2 E_ν²)) · F²(q)  · (ħc)²
Q_W,i = N_i − (1 − 4 sin²θ_W) Z,   sin²θ_W = 0.2387,   (ħc)² = 3.894e-28 GeV²·cm²
q = √(2 M_i T)
```
Internal units: G_F [GeV⁻²], M_i [GeV], T,E_ν [GeV] ⇒ dσ/dT [cm²/GeV]. Convert to cm²/keV by ×10⁻⁶.
**Valid when:** E_ν ≪ M (coherent, non-relativistic recoil), E_ν ≤ ~10 MeV.
**Breaks down when:** q large enough that F²≠1 matters at the %-level (near the ~2 keV endpoint) — handled by the FF; and the dropped O(T/E_ν) terms (~10⁻³).

### 2. Kinematic limits (per isotope)

```
# Source: METHODS.md Domain 1; PITFALLS §4
T_max^(i)(E_ν) = 2 E_ν² / (M_i + 2 E_ν)
E_min^(i)(T)   = (T + √(T² + 2 M_i T)) / 2  ≈  √(M_i T / 2)      (E_ν ≪ M)
```
**Valid when:** always (exact kinematics); use the exact form, the √(MT/2) approximation is for anchors only.

### 3. Helm form factor — Lewin & Smith 1996

```
# Source: Lewin & Smith, Astropart. Phys. 6, 87 (1996); METHODS.md
F(q) = 3 j₁(q R₀) / (q R₀) · exp(−q² s² / 2)
R₀² = c² + (7/3) π² a² − 5 s²,   c = 1.23 A^{1/3} − 0.60 fm,   a = 0.52 fm,   s = 0.90 fm
```
**Unit discipline:** q from √(2M_iT) is in MeV/c; convert to fm⁻¹ via q[fm⁻¹] = q[MeV]/(ħc=197.327 MeV·fm) so that qR₀ and qs are dimensionless. j₁(x)=sin x/x² − cos x/x (use `scipy.special.spherical_jn(1, x)`).
**Checks:** F(0)=1 (limit 3j₁(x)/x→1); for Ge, F²≈0.996 at T=200 eV and ≈0.95 near T≈2 keV (my quick calc, MEDIUM — verify in code). **Valid when:** qR₀ ≲ 1 (all reactor recoils). **Breaks down when:** never in this regime, but do NOT feed q in wrong units (PITFALLS §5 — a wrong-unit q produces a large spurious suppression).

### 4. Per-isotope-summed differential rate (CALC-02)

```
# Source: METHODS.md Domain 1 rate fold; CONVENTIONS Sec D normalization
dR/dT = Σ_i  (x_i · 8.29e24 /kg) · ∫_{E_min^(i)(T)}^{E_max}  Φ(E_ν) · (dσ_i/dT)(E_ν,T)  dE_ν
```
Φ(E_ν) [ν cm⁻²s⁻¹MeV⁻¹] from the frozen CSV (already contains all normalization). E_max = flux grid top (10 MeV; flux negligible beyond ~8 MeV).
**Unit chain:** [atoms/kg]·[cm²/keV]·[ν cm⁻²s⁻¹MeV⁻¹]·d E_ν[MeV] → counts kg⁻¹ s⁻¹ keV⁻¹ ; ×86400 → **counts kg⁻¹ day⁻¹ keV⁻¹**.
**Valid when:** deposited nuclear-recoil energy axis, no quenching/ε (Phase 3 scope).

### 5. Closed-form normalization identity (the check)

```
# Derived this session; matches cevns.py::sigma_tot
∫_0^{T_max} (1 − M T/2E_ν²) dT = E_ν²/M   (using T_max = 2E_ν²/M)
⇒ ∫_0^{T_max} dσ/dT dT = (G_F² M/4π) Q_W² (E_ν²/M) (ħc)² = G_F² Q_W² E_ν²/(4π)·(ħc)² = σ_tot(E_ν, Z, N)
```
**Valid when:** F=1 and T_max≈2E_ν²/M. Use as a per-isotope, per-E_ν unit test (<0.1% with F=1; a few ×10⁻⁴ residual from exact T_max is expected). **Breaks down when:** F²<1 near endpoint reduces the integral by <1% — test with F=1 for the exact identity.
</key_derivations>

<validation_strategies>

## Validation Strategies

Concrete, planner-turn-into-tasks checks (map to VALD-01, test-cevns-benchmark, and internal closure):

1. **Cross-section unit test (reuse Phase-1 target):** σ(⁷²Ge, 4 MeV) ≈ 1.0×10⁻⁴⁰ cm² (full Q_W), 1.08×10⁻⁴⁰ (N-only, ~20% tol). Already the anchor in CONVENTIONS Sec C. [HIGH]
2. **Closed-form normalization (independent of flux):** for each isotope and several E_ν, assert ∫ dσ_i/dT dT (F=1) = `sigma_tot(E_ν, 32, N_i)` to <0.1%. Confirms the differential is normalized. [HIGH]
3. **Helm sanity:** F(0)=1 exactly; F²(q built as √(2M_iT)) > 0.99 at T=200 eV; turning F off changes the integrated Billard rates by <1% (form-factor-independent flagship regime). [HIGH for F(0); MEDIUM for the near-endpoint magnitude]
4. **Billard Table 1 (VALD-01 primary):** fold the `billard_variant.csv` **renormalized to 8.54 GW / 400 m** (k≈0.0111), integrate dR/dT above 50/100/200 eV, compare to 0.76/0.51/0.26 counts/kg/day within ~20%. Match Billard's assumptions: HM constant below 2 MeV, fractions 55.6/32.6/7.1/4.7, no n-capture, per-isotope Ge sum, ±5% flux. [HIGH — assumptions read from primary source]
5. **Rescaled / CONUS+ agreement (VALD-01 secondary):** flagship dR/dT (flux v1.0, 3 GW_th/25 m) integrated rate agrees with CONUS+/rescaled Ge predictions within ~factor 2 — note CONUS+ is eV_ee (needs a quenching model), so this is a coarse cross-check only. [MEDIUM]
6. **Isotope-endpoint structure:** the spectrum shows five distinct T_max steps (e.g. at E_ν=8 MeV, 1.81–1.96 keV); a lumped-A run must visibly differ near the endpoint. [HIGH]
7. **Sub-1.8-MeV toggle:** zeroing the flux below 1.8 MeV must change T<95 eV bins substantially and leave T>200 eV bins essentially unchanged (localizes the placeholder systematic). [HIGH]
8. **Rate closure:** ∫(dR/dT)dT (differential path) equals the direct integrated rate (Σ_i N_i ∫Φ σ_tot,i dE_ν) per isotope, to numerical tolerance. [HIGH]
9. **Flux-band propagation:** fold Φ·(1±u(E_ν)) using the CSV `rel_uncertainty` column to produce a dR/dT band; verify it is wide (20–25%) for T≲95 eV and narrow (2–5%) for T≳200 eV. [HIGH for method; the band values are Phase-2 provided]
</validation_strategies>

<open_questions>

## Open Questions

1. **Exact Billard geometry treatment (single 8.54 GW @ 400 m vs two cores).**
   - Known: caption says 8.54 GW / 400 m; text says two 4.27 GW cores at 355.39 & 468.76 m. Both give the same effective 1/(4πd²) to <1%.
   - Unclear: which one Billard actually used to produce 0.76/0.51/0.26 to the quoted precision.
   - Recommendation: use the single 8.54 GW at 400 m (matches the caption and the two-core sum); a ~20% tolerance absorbs the difference. Document both.

2. **Whether Billard's spectrum below 2 MeV matches our variant to <10%.**
   - Known: our variant holds HM flat below 2 MeV per Billard's stated assumption; Phase-2 flagged that Billard's own low-E treatment was not independently verified.
   - Unclear: residual shape difference in the 50–100 eV bins (the only ones sensitive to <1.8 MeV).
   - Recommendation: expect the 50 eV bin to have the largest disagreement; if the 100/200 eV bins match within ~20% but 50 eV does not, attribute to the sub-2-MeV shape, not a code bug.

3. **Helm F² magnitude near the ~2 keV endpoint.**
   - Known: my hand calc gives F²≈0.95 at ~2 keV, ≈0.996 at 200 eV.
   - Unclear: exact value with the precise R₀ and scipy j₁.
   - Recommendation: compute F² across the grid in code and record the endpoint value; it shifts integrated Billard rates <1% but should be reported, not assumed 1.

4. **Defect-storage (Frenkel) NR energy loss in Phase 3.**
   - Known: few-% to ~10–15% for tens-of-eV to ~1 keV recoils, model-spread large (PITFALLS §7).
   - Unclear: whether to apply as a deposited-energy shift now or defer to the Phase-5 energy-scale systematic.
   - Recommendation: Phase 3 = pure recoil→deposited (no defect loss); carry defect storage as a documented systematic band, applied downstream. Flag it, don't bake it in.
</open_questions>

<not_found>

## What Was NOT Found

- **A machine-readable, digitized Kopeikin-2012 sub-1.8-MeV per-isotope table** — not sourceable in-environment (Springer-only; confirmed by Phase 2). The sub-1.8-MeV flux shape remains a placeholder covered by the wide 20–25% band; Phase 3 inherits this and must propagate it, not resolve it.
- **Billard's exact per-bin flux table / their internal fold code** — only Table 1 endpoints and the stated assumptions are recoverable from arXiv:1612.09035; the reproduction must reconstruct the fold from those assumptions.
- **An external CEvNS package matching this project's frozen-CSV + per-isotope + deposited-energy conventions** — none identified as lower-risk than extending `cevns.py`; general packages re-open the locked convention choices.
</not_found>

<sources>

## Sources

### Primary (HIGH)

- `GPD/CONVENTIONS.md` Sections A.2, C, D, G (LOCKED, machine-checked) — cross-section form, /4π, Q_W, sin²θ_W=0.2387, (ħc)², Ge atoms/kg, symbol registry. Read in full.
- `src/qpd_potential/cevns.py`, `src/qpd_potential/params.py` (Phase 1) — `weak_charge`, `sigma_tot`, all constants with provenance. Read in full.
- Billard et al., "Coherent Neutrino Scattering with Low Temperature Bolometers at Chooz Reactor Complex," J. Phys. G 44, 105101 (2017), arXiv:1612.09035 — **Table 1 (Ge 0.76/0.51/0.26 above 50/100/200 eV), Eq. 1 (dσ/dER, /4π, Q_W), assumptions (8.54 GW combined, 355.39 & 468.76 m, fractions 55.6/32.6/7.1/4.7, HM constant below 2 MeV, ±5%). PDF pages 1–6 read this session.**
- `data/flux/reactor_flux_v1.0.csv`, `data/flux/reactor_flux_billard_variant.csv` (Phase 2, frozen) — headers + grids read; normalization, band split, region flags.
- `GPD/phases/02-reactor-flux-model/02-02-SUMMARY.md` — flux normalization chain, integrals, Billard-variant provenance.

### Secondary (MEDIUM)

- `GPD/literature/METHODS.md` — Freedman σ, Helm parameters (Lewin & Smith), fold recipe, quadrature/interpolation guidance.
- `GPD/literature/PITFALLS.md` §§2–7 + numerical/convention traps + "Looks Correct But Is Not" checklist.
- Aristizabal Sierra, De Romeri, Rojas, JHEP 06 (2019) 141, arXiv:1902.07398 — form-factor irrelevance at reactor q (cited via project literature).
- De Romeri et al., arXiv:2501.18550; CONUS+ (Nature 643, 1229, 2025) — Ge-at-reactor rate scale for the factor-2 secondary check.

### Tertiary (LOW — verify in code during execution)

- My hand calculation of F²(Ge) ≈ 0.996 at 200 eV, ≈0.95 near 2 keV, and E_min(T) anchors — arithmetic done this session, to be reproduced by the executor.
- Ge isotope abundances/masses quoted as standard IUPAC/NIST representative values; verify against the project's chosen atomic-data source when coding the isotope table.
</sources>

<metadata>

## Metadata

**Research scope:**
- Physics subfield: reactor CEvNS differential rate on natural Ge, deterministic flux fold, deposited nuclear-recoil energy.
- Methods explored: Freedman cross section (locked), Helm form factor (Lewin–Smith), per-isotope sum, 1-D quadrature fold, closed-form normalization identity, Billard Table-1 reproduction.
- Known results catalogued: σ targets, Ge isotope table, kinematic limits, Billard Table 1 + assumptions (primary), flux integrals.
- Pitfalls: Billard normalization (new), lumped-A, (ħc)²//4π, grid/interpolation, quenching/scale.

**Confidence breakdown:**
- Mathematical framework: HIGH — cross section locked and unit-tested; fold is standard quadrature.
- Standard approaches: HIGH — deterministic fold, per-isotope sum, closed-form check all vetted.
- Existing results / Billard: HIGH — Table 1 and assumptions read from arXiv:1612.09035 this session; the normalization rescale is derived and cross-checked two ways.
- Computational tools: HIGH — extend `cevns.py` + SciPy; no new dependencies.
- Validation strategies: HIGH — multiple independent anchors (closed form, Billard, endpoints, closure).
- Helm near-endpoint magnitude / sub-1.8-MeV shape: MEDIUM — verify in code; band inherited from Phase 2.

**Research date:** 2026-07-20
**Valid until:** 2026-08-19 (30 days — established physics; frozen upstream artifacts).

---

_Phase: 03-cevns-cross-section-rate_
_Research completed: 2026-07-20_
_Ready for planning: yes_
</metadata>
