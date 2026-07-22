# Prior Work: Sub-eV Nuclear Recoil, the Low-Energy Excess, the Sub-100-keV Reactor Flux, and Ge vs CaWO₄ at a Shallow Reactor Site

**Surveyed:** 2026-07-22
**Domain:** Reactor CEvNS at ultra-low recoil energy; condensed-matter response of crystals to sub-eV nuclear recoils; cryogenic-detector low-energy excess; reactor antineutrino flux below the IBD threshold; target-material comparison for shallow-overburden reactor CEvNS
**Confidence:** MEDIUM overall — HIGH on fronts 1 and 4, MEDIUM on front 2, LOW-on-literature-but-HIGH-on-conclusion for front 3. Each entry carries its own level; DERIVED estimates are labeled.

**Milestone this survey serves (v2.0):** a QPD-instrumented ~110 g (4″×4″×2 mm) single-sided natural-Ge wafer deployed at the **NUCLEUS Chooz Very-Near-Site**, behind the NUCLEUS shielding, with **all spectra extended down to 100 meV** — two decades below the v1.0 10.14 eV grid floor and below both per-sensor saturation onsets (~1.27 eV Ta→Al, ~0.77 eV Al→Hf). Unified phonon energy scale throughout; analytic / Monte-Carlo response chain only, no G4CMP.

**The single most important framing fact for v2.0:** at 100 meV recoil in germanium the momentum transfer is `q ≈ 116 keV`, i.e. `q·a ≈ 144` — roughly 140 Brillouin zones outside the first zone. **There is no crystal-wide coherent enhancement anywhere in the v2.0 window, and single-phonon CEvNS events cannot deposit more than ~37 meV, so they lie entirely below the 100 meV floor.** What the 100 meV floor *does* enter is the **multiphonon regime at the edge of impulse-approximation validity** (`2W ≈ 5–8`), where the deposited-energy distribution for a given momentum transfer is not a delta function at `E_R` but a distribution of fractional width `1/√(2W) ≈ 35–46%`. That intrinsic quantum broadening — independent of and much larger than any detector resolution at 100 meV — is the principal new physics of this milestone and is absent from the v1.0 model.

---

## 0. Scope and Reading Guide

This file surveys **only what is new for v2.0**. The v1.0 validated physics — CEvNS cross section, Helm form factor, Huber–Mueller flux, Billard (2017) Table 1 reproduction, CONUS+ rate cross-check, Klein–Nishina Compton, Gaisser–Guan muon flux, the 25 kHz non-paralyzable saturation matrix, and the frozen ENDF/B-VIII.0 + NJOY n-Ge elastic set with abundance-weighted `T_max/E_n = 0.0536` — is **not** re-surveyed and is assumed carried forward unchanged. The v1.1 neutron/radiogenic background survey is superseded only where noted (§4.4).

Every finding is tagged:

| Tag | Meaning |
| --- | --- |
| **[INPUT]** | Directly usable as a forward-model input (number, formula, or parameterization) |
| **[CONTEXT]** | Qualitative; constrains interpretation but is not a model input |
| **[GAP]** | The literature does **not** answer the question. The project must generate the number itself or accept an unbounded systematic. |
| **[DERIVED]** | Computed *in this survey* from standard theory + retrieved literature parameters. **Not** a literature quote. Must be re-derived and unit-checked in an execution phase before use. |

Measurement / simulation / model-assumption is stated for every quoted number.

---

## 1. Front 1 — Sub-eV nuclear recoil in Ge: does the free-nucleus CEvNS picture survive to 100 meV?

**Front confidence: HIGH** on the framework; **MEDIUM** on the Ge numerics (the crossover scales below are derived here, not quoted).

### 1.1 The controlling published statement

> "the free nuclear recoil description of dark matter scattering breaks down for masses ≲ 100 MeV, **or when the recoil energy is comparable to a few times the typical phonon energy**."
> — B. Campbell-Deem, S. Knapen, T. Lin, E. Villarama, *Dark matter direct detection from the single phonon to the nuclear recoil regime*, **Phys. Rev. D 106, 036019 (2022)**, arXiv:2205.02250, DOI 10.1103/PhysRevD.106.036019. *(Theory + numerics, harmonic-crystal approximation.)*

Their impulse-approximation (IA) validity criterion, verbatim from the text preceding their Eq. (37):

> "q ≫ √(2 m_d ω̄_d)"

with `m_d` the mass of atom species *d* and `ω̄_d` its characteristic phonon energy. Squaring and dividing by `2 m_d`, this is exactly `E_R ≫ ω̄`. **This is the published criterion the project should quote.** [INPUT — as a criterion; the Ge number attached to it is DERIVED below]

Framework origin: B. Campbell-Deem, P. Cox, S. Knapen, T. Lin, T. Melia, *Multiphonon excitations from dark matter scattering in crystals*, **Phys. Rev. D 101, 036006 (2020)**, arXiv:1911.03482 — analytic two-acoustic-phonon rates for cubic crystals including Ge and Si.

**Public code:** `DarkELF`, https://github.com/tongylin/DarkELF — implements the single-phonon → multiphonon → nuclear-recoil bridge for Ge, Si, GaAs, Al₂O₃. Its `S(q,ω)` is a *material response*, independent of the dark-matter model, and is therefore reusable with a CEvNS matrix element. **This is the single most actionable software finding of this front.** [INPUT]

### 1.2 Regime map for germanium

The following is **[DERIVED]** — computed in this survey from standard harmonic-crystal / IA theory with literature Ge parameters (`A = 72.63`, `m_N c² = 67.65 GeV`, Debye temperature `Θ_D = 374 K`, nearest-neighbour spacing `a = 2.45 Å`). It is *not* quoted from any paper and **must be independently re-derived in an execution phase.**

Definitions (standard Squires/Sears conventions):
- Free-recoil momentum transfer `q = √(2 m_N E_R)`
- Debye–Waller exponent `2W(q) = q²⟨u_x²⟩`, `⟨u_x²⟩` = **1-D** mean-square displacement
- Debye-model `T→0`: `⟨u_x²⟩ = 3ħ²/(4 m_N k_B Θ_D) = 1.34×10⁻³ Å²` (crystallographic `B = 8π²⟨u_x²⟩ = 0.106 Å²`). Experimental low-T Ge `B ≈ 0.19–0.24 Å²` (i.e. `⟨u_x²⟩ ≈ 2.4–3.0×10⁻³ Å²`) because the DW effective Debye temperature is below `Θ_D`; the table brackets both.
- Effective phonon energy `ω̄ ≡ ħ/(2 m_N ⟨u_x²⟩)` → **`ω̄(Ge) = 12–21 meV`**. Note this is *below* the 37 meV zone-centre optical phonon because `⟨u²⟩` is dominated by low-frequency acoustic modes. With this definition the identity `2W = E_R/ω̄` is exact.

| `E_R` (Ge) | `q` [eV] | `q·a` | `2W = E_R/ω̄` | Regime | IA fractional broadening `1/√(2W)` |
| --- | --- | --- | --- | --- | --- |
| 0.03 meV | 2.0×10³ | ≈2.5 | ~0.002 | **single-phonon / first BZ** | IA invalid |
| 1 meV | 1.2×10⁴ | 14 | 0.05–0.08 | few-phonon | IA invalid |
| 37 meV | 7.1×10⁴ | 88 | 1.7–3.1 | multiphonon | 57–76% |
| **100 meV** | **1.16×10⁵** | **144** | **4.7–8.3** | **multiphonon → IA edge** | **35–46%** |
| 300 meV | 2.02×10⁵ | 250 | 14–25 | IA | 20–26% |
| 1 eV | 3.68×10⁵ | 457 | 47–83 | IA / quasi-free | 11–15% |
| 10 eV | 1.16×10⁶ | 1444 | 465–834 | free nucleus | 3.5–4.6% |
| 20 eV | 1.65×10⁶ | 2042 | 931–1670 | free nucleus | 2.5–3.3% |
| 1 keV | 1.16×10⁷ | 14443 | 4.7–8.3×10⁴ | free nucleus | 0.35–0.46% |

### 1.3 Four decisive conclusions

**(1a) There is NO crystal-wide coherent enhancement anywhere in the 100 meV – 10 eV window.** [DERIVED, HIGH]
Coherence over the lattice requires `q ≲ 2π/a`, i.e. `E_R = q²/2m_N ≲ 30 μeV` in Ge — more than three decades below the v2.0 floor. At 100 meV, `q·a ≈ 144`: the neutrino resolves individual nuclei. The `N²` coherence in CEvNS is *intranuclear* (over the ~fm nucleus, `qR_A ≪ 1`, governed by the Helm form factor) and is unaffected; there is **no additional `N_atoms²` enhancement**. Any claim of "the neutrino couples coherently to the whole crystal" at these recoils is wrong and should be explicitly rebutted in the milestone writeup.

**(1b) Single-phonon CEvNS events deposit at most ~37 meV in Ge and therefore lie ENTIRELY BELOW the 100 meV floor.** [DERIVED, HIGH]
In a single-phonon event the deposited energy is `ω_phonon(q) ≤ ω_max ≈ 37 meV` (Ge zone-centre optical phonon; standard solid-state value). The single-phonon channel cannot populate any bin at or above 100 meV. **The 100 meV floor is safely above the single-phonon regime — but only just, and the choice of floor should be documented as resting on this fact.**

**(1c) At 100 meV the recoil sits in the multiphonon regime at the edge of IA validity, with a large, physically real quantum broadening.** [INPUT, high priority. Framework is textbook; the Ge numbers are DERIVED.]
In the impulse approximation the dynamic structure factor is not a delta at `E_R` but a distribution centred on `E_R` whose width is set by the nuclear momentum distribution — the Doppler / final-state broadening familiar from deep-inelastic neutron scattering (V. F. Sears, *Scaling and deep-inelastic neutron scattering from quantum liquids and solids*, **Phys. Rev. B 35, 2038 (1987)**, DOI 10.1103/PhysRevB.35.2038). With zero-point `σ_p² = m_N ω̄/2` and `q = √(2 m_N E_R)`:

```
σ_E  =  q σ_p / m_N  =  √( E_R · ω̄ )          [ħ = 1]
σ_E / E_R  =  1/√(2W)
```

| `E_R` | `σ_E` (Ge, `ω̄` = 12–21 meV) | `σ_E / E_R` |
| --- | --- | --- |
| 100 meV | 35–46 meV | **35–46%** |
| 300 meV | 60–80 meV | 20–26% |
| 1 eV | 110–147 meV | 11–15% |
| 10 eV | 346–464 meV | 3.5–4.6% |
| 100 eV | 1.1–1.5 eV | 1.1–1.5% |
| 1 keV | 3.5–4.6 eV | 0.35–0.46% |

**This is an intrinsic, irreducible smearing of the deposited phonon energy that exists before any detector response, and it is absent from the v1.0 forward model.** Recommended implementation: convolve the free-recoil `dR/dE_R` with a Gaussian of `σ_E = √(E_R ω̄)` **before** the QPD response chain (saturation matrix, collection efficiency). Caveats to carry: (i) the IA has `O(1/2W)` corrections, so at `2W ≈ 5–8` the correction is itself 15–20% and the Gaussian is only approximate; (ii) the true `S(q,ω)` is asymmetric at low `2W`; use DarkELF if better than ~30% accuracy is required in the bottom bin.

**(1d) Below ~6 eV recoil in Ge no lattice defect can be created, so 100% of the recoil goes to phonons.** [INPUT — measurement + simulation]
> "the first experimentally determined average displacement threshold energy for germanium is **(19.7 ⁺⁰·⁶ ₋₀·₅) eV**"; "an energy loss of **(6.08 ± 0.18)%** … attributed to defect formation"; "below about **6 eV** in germanium, the recoil is not strong enough to create a defect"; TRIM-2013 scanned `E_d` over 15–23 eV.
> — R. Agnese *et al.* (SuperCDMS), *Energy loss due to defect formation from ²⁰⁶Pb recoils in SuperCDMS germanium detectors*, **Appl. Phys. Lett. 113, 092101 (2018)**, arXiv:1805.09942, DOI 10.1063/1.5041457.
> *Conditions:* SuperCDMS Ge, high-energy (~100 keV) ²⁰⁶Pb recoils. The 19.7 eV is a **measurement**; the 6 eV no-defect statement and the 15–23 eV scan are **TRIM simulation**.

**Consequence:** the project's "no quenching — all energy is phonons" convention is *strengthened*, not weakened, in the 100 meV – 6 eV window, because the defect-formation loss channel is closed entirely there. Suggested model input: `f_phonon(E_R) = 1` below 6 eV, ramping to `1 − 0.061` above ~100 eV. Anti-correlated pitfall: energy stored in Frenkel pairs can later be *released* as phonons — see the TESSERACT neutron-damage work (arXiv:2603.17964, title/abstract only, not read in this survey).

### 1.4 Structural note specific to Ge/Si (diamond lattice)

Ge has two **identical** atoms per primitive cell. For an operator coupling identically to both basis atoms — the CEvNS case, since both are the same isotope mixture with the same weak charge — the optical-phonon matrix element is suppressed by destructive interference between the sublattices, leaving acoustic phonons as the leading single-phonon channel. This is the standard motivation for the DM-phonon community's focus on **polar** targets (GaAs, Al₂O₃, SiC): S. Knapen, T. Lin, M. Pyle, K. Zurek, *Detection of light dark matter with optical phonons in polar materials*, **Phys. Lett. B 785, 386 (2018)**, arXiv:1712.06598; S. Griffin, S. Knapen, T. Lin, K. Zurek, *Directional detection of light dark matter with polar materials*, **Phys. Rev. D 98, 115034 (2018)**, DOI 10.1103/PhysRevD.98.115034.

**Confidence: MEDIUM.** The polar-material preference is firmly established in those papers; the *specific* sublattice-cancellation statement for equal couplings in Ge was **not verified verbatim from retrieved text in this survey**. It only affects the <37 meV region, which is below the v2.0 floor, so it is off the critical path — but flag it for verification before it appears in any writeup. [CONTEXT]

### 1.5 What does NOT exist in the literature

**[GAP — decisive for scoping]** I found **no published calculation of the reactor-CEvNS single-phonon or multiphonon rate in germanium.** The DM-phonon literature computes the material response model-independently but attaches DM kinematics. The one neutrino-specific paper found — Y.-F. Li & S.-y. Xia, *Migdal effect of phonon-mediated neutrino nucleus scattering in semiconductor detectors*, **arXiv:2310.05704** (Nucl. Phys. B) — treats the *electronic* Migdal channel mediated by phonons, **not** the phonon-energy-deposition channel we need. Adjacent: K. Berghaus et al., *The phonon background from gamma rays in sub-GeV dark matter detectors*, **arXiv:2112.09702** (single/multiphonon γ backgrounds in Si, Ge, GaAs, SiC, compared to solar-neutrino CEvNS rates).

**Recommendation (opinionated):** the project must do this itself, and it should be its own v2.0 phase. Take DarkELF's Ge `S(q,ω)` and contract it with the CEvNS matrix element `∝ G_F² Q_W² F_Helm²(q)`. This is bounded work with a clear deliverable. **Fallback if too heavy:** free-recoil spectrum ⊗ Gaussian(`√(E_R ω̄)`), with the `O(1/2W)` ≈ 20% uncertainty quoted explicitly at the bottom bin. Do **not** simply extend the v1.0 free-nucleus spectrum to 100 meV with no broadening — that is the one option the literature clearly forbids.

---

## 2. Front 2 — The Low-Energy Excess (LEE)

**Front confidence: MEDIUM.** The phenomenology is well documented and a usable **time**-dependence parameterization now exists; the **energy**-dependence parameterization is experiment-specific, and **there is no LEE measurement anywhere near 100 meV**.

### 2.1 Anchor documents

| Document | Citation | What it gives |
| --- | --- | --- |
| EXCESS Workshop compilation | P. Adari *et al.* (10 collaborations, ~310 authors), *EXCESS workshop: Descriptions of rising low-energy spectra*, **SciPost Phys. Proc. 9, 001 (2022)**, arXiv:2202.05097, DOI 10.21468/SciPostPhysProc.9.001 | Per-experiment spectra, thresholds, rates; **public data repository** |
| CRESST-III LEE study | G. Angloher *et al.* (CRESST), *Latest observations on the low energy excess in CRESST-III*, **SciPost Phys. Proc. 12, 013 (2023)**, arXiv:2207.09375 | Holder-design comparison, warm-up and decay behaviour |
| **NUCLEUS LEE study (2026)** | NUCLEUS Collaboration, *Characterization of the Low Energy Excess using a NUCLEUS Al₂O₃ detector*, **arXiv:2603.07687** (8 Mar 2026; no journal ref) | **Best available time-dependence parameterization**; cooldown-rate dependence; muon-independence |
| Stress origin (measurement) | R. Anthony-Petersen, A. Biekert, R. Bunker *et al.*, *A stress-induced source of phonon bursts and quasiparticle poisoning*, **Nat. Commun. 15, 6444 (2024)**, arXiv:2208.02790, DOI 10.1038/s41467-024-50173-8 | Glued vs suspended Si: **>2 orders of magnitude** rate difference |
| Stress origin (model) | R. K. Romani, *Aluminum relaxation as the source of excess low energy events in low threshold calorimeters*, **J. Appl. Phys. 136, 124502 (2024)**, arXiv:2406.15425, DOI 10.1063/5.0222654 | Mechanistic model: `1/t` decay, aluminium-**area** scaling |
| **Sub-eV bursts** | C. L. Chang *et al.*, *Spontaneous generation of athermal phonon bursts within bulk silicon causing excess noise, low energy background events and quasiparticle poisoning in superconducting sensors*, **Appl. Phys. Lett. 127, 263502 (2025)**, arXiv:2505.16092, DOI 10.1063/5.0281876 | **The only sub-eV/meV-scale burst measurement found**; volume scaling |

### 2.2 Measured amplitudes and spectral shapes (all measurements)

From arXiv:2202.05097 — conditions attached:

| Experiment | Target / mass | Threshold | Excess description | Notes |
| --- | --- | --- | --- | --- |
| **EDELWEISS RED20** | **Ge, 33.4 g** | above ground | **10⁵ counts/(keV·kg·d) at 200 eV; 10⁴ counts/(keV·kg·d) at 1 keV** | Implies effective power-law index `n ≈ 1.4` over 0.2–1 keV **[DERIVED from those two points]**. "shape of the spectra does not vary significantly in time, while the absolute rate decreases slowly over time" |
| **EDELWEISS RED30** | Ge, 33.4 g | underground | **factor ~3 lower** than RED20, similar shape | "Sudden increases were observed at times after warming-up the detectors above 10 K" |
| **RICOCHET CryoCube** | Ge, 42 g | — | "consistent with EDELWEISS RED20 above-ground"; improved holding scheme gave **no** improvement | Directly relevant Ge datum |
| SuperCDMS CPD | Si, 10.6 g | 4.2σ trigger | "rises exponentially above the flat background" below 100 eV; **steeper exponential below 30 eV**; flat background **2×10⁵ counts/(keV·kg·d)** above 100 eV | Two-slope shape; candidate causes listed include "stress microfractures from the clamping" |
| CRESST-III Det-A | CaWO₄, 23.6 g | 30.1 eV (NR) | sharp rise below 200 eV | |
| NUCLEUS 1 g prototype | **Al₂O₃, 0.49 g** | **19.7 eV** | sharp rise below ~200 eV; persists below ~100 eV even with inner cryogenic veto | The NUCLEUS-relevant datum |
| DAMIC | Si CCD, 6 g | 50 eV_ee | 17.1 ± 7.6 excess events in 50–200 eV_ee (p = 2.2×10⁻⁴); **"decaying exponentially with a decay constant of (67 ± 37) eV"** | The cleanest single *energy*-scale fit in the compilation |
| SENSEI | Si skipper-CCD | 1–4 e⁻h⁺ | ~3370 counts/(keV·kg·d), 500 eV–10 keV | 225 m.w.e., 135 K |

**Honest observation:** there is **no agreed functional form**. The EXCESS paper itself "does not specify uniform mathematical descriptions … across all experiments." Published shapes span `~E^{-1.4}` (Ge, EDELWEISS), a two-slope exponential (Si, SuperCDMS CPD), and a single exponential with a 67 eV scale (Si CCD, DAMIC). [CONTEXT for the shape; becomes [INPUT] only once the project explicitly adopts one and carries the spread as its systematic.]

### 2.3 Time dependence after cooldown — the best available parameterization

**[INPUT — highest-value LEE result for the forward model]**

NUCLEUS Al₂O₃, arXiv:2603.07687 (measurement; 0.75 g sapphire, 5×5×7.5 mm³, two W-TES at `T_c` = 15.1 / 15.6 mK, baseline `σ₀` = 5.5–11.9 eV):

```
R_LEE(t) = A · (t − t₀)^(−k)
R_LEE ≡ Rate([100,300] eV) − Rate([1,3] keV)     [dru = counts/(keV·kg·d)]
t₀ ≡ the moment the detector reaches 4 K (start of He condensation); t in days
```
- **`k̄(Al₂O₃) = 0.59 ± 0.06`** (weighted average over all runs)
- **`k(CaWO₄) = 0.73 ± 0.08`** (compatible with Al₂O₃ within 1.5σ)
- Normalization `A` shows a "strong decreasing trend with increasing duration of the cooldown from room temperature to the condensation start"; **slower cooldowns reduce the initial LEE rate by up to an order of magnitude**
- **No** dependence found on: particle background level, time since remounting, number of thermal cycles, cumulative cryogenic time
- Muon coincidence probability **`p_LEE = 0.025 ± 0.004`** → **">98% of the measured LEE has a different origin"** than muons. *(Important for v2.0: this decouples the LEE from the muon channel the project already models.)*

CRESST-III, arXiv:2207.09375 (measurement) fits an **exponential in time** instead, `R(t) = A e^{−t/τ} + C`, with `τ = (149 ± 40) d` in the BCK period and `τ = (18 ± 7) d` after a warm-up; analysis window 60–120 eV. Rates vary "up to one order of magnitude in the 60–120 eV range" across detectors and "up to two orders of magnitude" when mass-normalized. Modules compared: Si2 (Si, 0.35 g, Cu holder), Sapp1/2 (Al₂O₃, 16 g each, Cu), Li1 (LiAlO₂, 11 g, Cu), TUM93A (CaWO₄, 24 g, mixed Cu/CaWO₄), Comm2 (CaWO₄, 24 g, bronze clamps). Holder modifications (Cu sticks, bronze clamps with broader contact, removal of scintillating foils) had **"no significant impact."** Warm-up to 60 K re-excites the LEE; warm-ups to 600 mK and 200 mK produce **no** measurable effect.

**Conflict to resolve, with a recommendation:** CRESST uses an exponential in time, NUCLEUS a power law. **Adopt the NUCLEUS power law with `k = 0.6`** — it is the more recent measurement, it spans both Al₂O₃ and CaWO₄, and it agrees with both the Romani `1/t` depinning prediction (§2.4) and the independently measured `κ = 0.635 ± 0.009` in bulk Si (§2.5). Carry the CRESST exponential as the alternative inside the systematic band.

**Contradiction to note:** CRESST and RICOCHET both report holder redesigns making **no** difference, while Anthony-Petersen et al. report a **>100×** effect from going glued → suspended. These are not necessarily inconsistent — the CRESST/RICOCHET changes were incremental (stick material, clamp area) whereas Anthony-Petersen changed the mounting *topology* — but the milestone should not claim that "mounting fixes the LEE."

### 2.4 Origin hypotheses — stress and relaxation

**Measurement (strongest single result on this front):** Anthony-Petersen et al., Nat. Commun. 15, 6444 (2024):
> "a silicon crystal glued to its holder exhibits a rate of low-energy phonon events that is **more than two orders of magnitude larger** than in a functionally identical crystal suspended from its holder in a low-stress state,"
attributed to relaxation of thermally induced glue–crystal stress.

**Model:** Romani, J. Appl. Phys. 136, 124502 (2024). Thermal stress in **aluminium films** creates dislocations pinned at defects; pinned dislocations tunnel free, accelerate toward the film–substrate interface and emit phonon bursts on impact.
- Time dependence `R(t) ≈ N/(Γ t)` — **"1/t rather than exponential"** (consistent with NUCLEUS `k ≈ 0.6`)
- Scaling `N = A_Al × ρ_D` — **rate scales with aluminium film area** and dislocation density
- Simulated spectrum "peaks in the tens-to-hundreds eV range"; "emerges from the convolution of stress distributions and dislocation geometries, rather than following a simple power law"
- Predicted rates "0.37, 0.54, and 0.28 Hz" one week post-cooldown for realistic dislocation densities — these "bracket measured excesses in CRESST-III and SuperCDMS"
- "predicts primarily **meV-to-eV scale phonons**, with substantial coupling to the substrate phonon system"

**This is directly and unfavourably relevant to the QPD design.** A QPD wafer carries **Ta/Al or Al/Hf superconducting films on its surface** — precisely the aluminium-film geometry Romani identifies as the source, and the Chang et al. burst energy scale (§2.5) sits at the Al gap. The v2.0 model therefore **cannot** treat the LEE as an external, geometry-independent background: it scales with `A_Al` and with mounting stress, both of which are design choices for the 4″×4″ wafer. **Flag as a first-class v2.0 modeling decision, and note it as a *design lever* the milestone can advocate (minimize Al coverage; low-stress suspension; slow cooldown).**

### 2.5 The sub-eV regime — the only relevant measurement

**[INPUT + GAP]** Chang et al., APL 127, 263502 (2025), arXiv:2505.16092 (measurement, Si):
- 1 cm² Si substrates: **1 mm thick, 0.233 g** (70 kΩ·cm) and **4 mm thick, 0.932 g** (20 kΩ·cm)
- World-leading resolution **258.5 ± 0.4 meV** (1 mm device); sensitivity below 1 eV, spectra usable to ~30 eV before cosmic-ray saturation
- Sub-threshold burst characteristic energy from shot-noise analysis: **`ε = 0.68 ± 0.38 meV`** — "approximates the low-energy cutoff of the underlying phonon distribution," compared with the Al gap ~360 μeV
- Correlated phonon noise and bias power decay as a power law in time, **`κ = 0.635 ± 0.009`**, over 12 days
- **"the correlated noise in the 4 mm detector is 4 times as large as the 1 mm detector"** → the burst source scales with **substrate volume**, not surface area, at low energy; "shared" LEE events show linear **mass** scaling at higher energies
- Conclusion: "the dominant source of both above and below threshold [bursts] originates in the **bulk silicon substrate itself**," and these bursts "are likely a significant source of **quasiparticle poisoning in superconducting qubits**"

**Two conclusions.** (i) There *is* a measured phonon-burst population at the ~0.7 meV scale — below the entire v2.0 window. This is the physical floor a meV-threshold QPD will sit on, and since a QPD's signal *is* quasiparticle poisoning, this population is not merely a background but a direct competitor to the signal mechanism. (ii) The volume scaling is bad news for a 110 g wafer: Chang et al.'s devices are 0.23–0.93 g. Naive linear extrapolation to 110 g is a factor **~120–470**, simultaneously extrapolating >2 decades in mass and >2 decades in energy. **That is not defensible as a prediction** — state it as an order-of-magnitude scaling argument with explicitly unbounded uncertainty.

### 2.6 The gap, stated plainly

**[GAP]** **No experiment has ever measured a low-energy-excess spectrum below ~10 eV in germanium, and none has measured one at 100 meV in any material.** Every LEE parameterization in the literature is anchored at 20–300 eV. Extending any of them to 100 meV is a **two-to-three-decade extrapolation in energy** of a phenomenon whose microscopic origin is not established (and whose two leading models — bulk-substrate bursts and Al-film dislocation relaxation — predict *different* scalings, with volume and with `A_Al` respectively). The forward model must present the LEE below 10 eV as a **band with an explicit extrapolation assumption**, never as a prediction. **This is the single largest irreducible uncertainty in v2.0.**

**On the NUCLEUS VNS paper's exclusion of the LEE:** Abele et al., **Eur. Phys. J. C 86, 29 (2026)**, arXiv:2509.03559, deliberately excludes the LEE from its background budget while naming it a definite limit on sensitivity. Given the above, that exclusion is **scientifically honest rather than evasive** — there is no defensible number to put in. Recommend v2.0 adopt the same posture: report the CEvNS / muon / gamma / neutron budget quantitatively, with the LEE as a **separately flagged overlay band**, never folded into a single headline S/B number.

---

## 3. Front 3 — The reactor antineutrino spectrum below ~100 keV

**Front confidence: LOW on the literature (there is almost none), HIGH on the scoping conclusion.**

### 3.1 Established facts

**(3a) There is no measurement of the reactor antineutrino spectrum below 1.8 MeV. None, anywhere.** [GAP, HIGH]
The IBD threshold is 1.8 MeV; every reactor spectral measurement (ILL, Daya Bay, RENO, Double Chooz, PROSPECT, STEREO) is an IBD measurement and is blind below it. Quoting the paper whose entire purpose is to fix this:
> "no experimental spectral information is available for `E_ν < 1.8 MeV`. Instead, only ab initio, or database driven spectral calculations can provide information."
> — *Impact of reactor neutrino uncertainties on coherent scattering's discovery potential*, **arXiv:2406.16081**, J. Phys. G (2024), DOI 10.1088/1361-6471/ad8ee2.

And the companion result: J. Liao, H. Liu, D. Marfatia, *How to measure the reactor neutrino flux below the inverse beta decay threshold with CEνNS*, **Phys. Rev. D 108, 033002 (2023)**, arXiv:2302.10460, DOI 10.1103/PhysRevD.108.033002 — an ultra-low-threshold CEvNS experiment can set **upper bounds** on the sub-1.8 MeV flux via regularized unfolding, but "the neutron capture component cannot be definitively identified." *(Note: this is a positive framing opportunity for the milestone — a 100 meV-threshold Ge detector is exactly the instrument this paper calls for.)*

**(3b) The frozen Huber–Mueller table is already an extrapolation below 2 MeV.** [CONTEXT — important pre-existing caveat, HIGH]
P. Huber, **Phys. Rev. C 84, 024617 (2011)** (²³⁵U, ²³⁹Pu, ²⁴¹Pu) and T. A. Mueller *et al.*, **Phys. Rev. C 83, 054615 (2011)** (²³⁸U) provide polynomial-fit spectra **valid over 2–8 MeV**. Everything the project already uses between 100 keV and 2 MeV is outside the fitted range. **The v2.0 extension from 100 keV to 58.7 keV therefore does not cross a new qualitative boundary — the boundary was crossed at 2 MeV, in v1.0.** The honest framing: *the sub-2-MeV flux is a model, the sub-100-keV flux is the same model further extrapolated, and neither is measured.* This reframing is itself a deliverable — it converts a v2.0-specific worry into a correctly-scoped, pre-existing systematic.

**(3c) Only one line of work appears to compute reactor antineutrino spectra explicitly into the keV region.** [CONTEXT, MEDIUM — **partially unverified**]
*Calculation of low-energy electron antineutrino spectra emitted from nuclear reactors with consideration of fuel burn-up*, **J. Nucl. Sci. Technol.**, published online 22 Feb 2017, DOI 10.1080/00223131.2017.1291370. Motivation quoted from the abstract: "neutrinos in the keV region, since they may have information on fuel burn-up and may be detected in the future with advanced measurement technology." Key finding quoted: "**the electron antineutrino flux in the low-energy region increases with burn-up of nuclear fuel by accumulated nuclides with low Q values in beta-decay**." Uses JENDL FP Fission Yields Data File 2011 for ²³⁸U fast-fission yields.
> **VERIFICATION FAILURE:** Taylor & Francis returned HTTP 403 and Ingenta Connect returned HTTP 403. I have **not** verified the author list, volume/page, the lowest energy on their grid, the absolute normalization, or which nuclides dominate below 100 keV. **Treat as a lead, not a source. Do not cite until retrieved.**

Related, higher-energy: V. Kopeikin, L. Mikaelyan, V. Sinev, *Components of antineutrino emission in nuclear reactor*, **Phys. At. Nucl. 67, 1892 (2004)**, DOI 10.1134/1.1825513 — identifies six emission components (β decays of fission fragments of ²³⁵U, ²³⁹Pu, ²³⁸U, ²⁴¹Pu, plus β emitters from neutron capture on ²³⁸U and on accumulated fission fragments). **Paywalled; component magnitudes not verified here.**

### 3.2 The decisive physics argument — [DERIVED, must be re-verified in a phase]

**(3d) Every allowed β decay contributes an antineutrino spectrum that vanishes as `E_ν²` at zero energy.** [INPUT, HIGH]
For an allowed transition, `dΓ/dE_ν ∝ E_ν² p_e E_e F(Z, E_e)` with `E_e = E_0 − E_ν`. As `E_ν → 0` every branch contributes `∝ E_ν² ×` (a finite constant). Summing over the ~800 fission-product β branches does not change this: **the total reactor `dN/dE_ν` is quadratically suppressed as `E_ν → 0`.** This is textbook β-decay kinematics, not a model choice, and it is the strongest bound the project has on this front. It also means that the "flux is unmeasured down there" worry is far less severe than it sounds: the flux is not merely unknown, it is *known to be small* on kinematic grounds.

**(3e) The truncation error from flooring the flux at 100 keV is bounded and small.** [DERIVED]
The CEvNS differential rate is
```
dR/dT  ∝  ∫_{E_min}^{∞} dE_ν  φ(E_ν) · [ 1 − E_min² / E_ν² ] ,     E_min = √( M_Ge T / 2 )
```
At `T = 100 meV`, this survey obtains `E_min = 58.16 keV` (using `A = 72.63`; the project's frozen 58.7 keV presumably uses a different isotope-abundance weighting of `M_Ge` — **reconcile, §7 item 8**). The missing contribution is the integral over `[58.2, 100] keV` alone, where **both** factors are small: `φ ∝ E_ν²` is suppressed, and the kinematic bracket vanishes at the lower limit.

A deliberately **conservative** upper bound (continue `φ` flat at its 100 keV value, i.e. *ignore* the `E_ν²` suppression):
```
∫_{58.2}^{100} φ(100 keV) [1 − (58.2/E)²] dE  =  φ(100 keV) × 17.0 keV
```
Relative to the full integral (normalization ≈ 6 ν̄/fission), this is a truncation error of order `17 keV × φ(100 keV) / 6`. With a plausible `φ(100 keV) ~ 3 ν̄/(fission·MeV)` this is **≲ 1%**, and the true value is substantially smaller once the `E_ν²` suppression is applied.
> **[DERIVED]** The arithmetic is mine; `φ(100 keV) ~ 3/(fission·MeV)` is a **placeholder**, not a retrieved value. An execution phase must evaluate this with the project's own frozen flux-table value at 100 keV and report the actual number.

### 3.3 What the forward model should legitimately claim (opinionated)

1. **Do not attempt to predict or "measure" the sub-100-keV flux.** No measurement exists and none is imminent.
2. **Do extend the flux grid to ~50 keV with a summation calculation, labelled as a model with unbounded shape uncertainty.** The tool is **CONFLUX** — X. Zhang, A. Irani, M. P. Mendenhall *et al.*, *CONFLUX: A standardized framework to calculate reactor antineutrino flux*, **arXiv:2503.18966** (2025): a Python/C++ package implementing the summation method from **ENDF/B-VIII** and **JEFF-3.3** fission yields plus **ENSDF** β-decay data, with a **user-configurable energy grid** (documented examples run 0–15 MeV at 0.1 MeV resolution). It does **not** explicitly validate below 1.8 MeV and quotes no low-energy uncertainty, so any output must be labelled accordingly. [INPUT — the concrete route to fill the 58.7–100 keV band]
3. **Lead with the truncation bound of §3.2, not with a spectrum.** "The unmeasured sub-100-keV flux changes the 100 meV recoil rate by ≲X%, where X is computed from the frozen table" converts an open-ended model risk into a bounded, defensible statement, and is far more valuable than a fabricated sub-100-keV spectrum.
4. **Non-equilibrium and activation sources** — ²³⁸U(n,γ) → ²³⁹U → ²³⁹Np, activation of structural steel, long-lived fission products accumulating with burn-up — are real and are known to *raise* the very-low-energy flux with burn-up (§3.1c). They are **not quantified below 100 keV in any source I retrieved.** Treat as a **one-sided** systematic that can only increase the rate. [GAP]

---

## 4. Front 4 — Ge vs CaWO₄/Al₂O₃ as a reactor CEvNS target at a shallow site

**Front confidence: HIGH on the published numbers. The direct answer to the project's question is: NO — nobody has published a Ge-at-a-shallow-reactor-site S/B anywhere near 0.65–1.2.**

### 4.1 Target-scaling physics (established, qualitative)

- CEvNS cross section `∝ N²`, so heavier targets give more signal per unit mass; **but** `T_max = 2E_ν²/M` falls as `1/M`, pushing signal below threshold. Standard trade-off, stated in every review.
- **The signal/background scaling asymmetry is the core argument:** the coherent cross section scales as `A²` per nucleus while neutron elastic cross sections are roughly `A`-independent — favouring high-`A` targets.
- **CaWO₄ vs Al₂O₃ in NUCLEUS:** "Al₂O₃ produces a CEvNS signal **more than an order of magnitude below** that in CaWO₄, and can be conservatively regarded as measuring background under identical experimental conditions to the CaWO₄ array." The Al₂O₃ array is a **background monitor**, not a second signal channel. [CONTEXT]
- **Ge sits between** (`A = 72.6`, vs W = 183.8 in CaWO₄ and Al/O = 27/16 in sapphire), and uniquely combines a mature low-background detector technology with the best-characterized nuclear data — which this project has already frozen.

### 4.2 Published Ge-at-a-reactor numbers (measurements)

| Experiment | Site / power / distance | Overburden | Target | Threshold | Background near threshold | Signal | S/B |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **CONUS+** | Leibstadt, **3.6 GW_th**, 20.7 m | **7.4 m.w.e.** | HPGe ×3, **2.83 ± 0.02 kg** | **160–180 eV_ee** | **≈ 40 counts/(kg·d)** in 0.4–1 keV_ee | **395 ± 106** observed (SM 347 ± 59) in **327 kg·d** on / 60 kg·d off → **1.21 counts/(kg·d)** | **≈ 0.03** in that band **[DERIVED from the two quoted rates]**; the signal rises above background only **below 250 eV_ee**. Significance **3.7σ**; data/SM = **1.14 ± 0.36** |
| **CONUS** (final) | Brokdorf, 17.1 m, 3.9 GW_th | ~24 m.w.e., 11 t shield | HPGe, **3.73 ± 0.02 kg** | **210 eV_ee** | noise-peak contribution "< 1 count/(kg·d·keV)" in ROI; reactor-correlated ¹⁶N γ adds **1–2 counts/(kg·d)** | **91 ⁺¹¹ ₋₉** predicted for 426 kg·d | limit only: < 0.34 signal events/(kg·d) at 90% CL — **a factor 2 above the SM prediction** |
| **RICOCHET** | ILL, **58 MW_th**, 8.8 m | **15 m.w.e.** | Ge CryoCube, ~42 g | 50 eV (design) | "will be dominated by cosmogenic neutrons" despite the overburden | **≈ 12.8 events/(kg·d)** at 50 eV threshold (**prediction**) | not quoted |

**Citations:**
- CONUS+ Collaboration, *Direct observation of coherent elastic antineutrino–nucleus scattering*, **Nature 643 (8074), 1229–1233 (2025)**, DOI 10.1038/s41586-025-09322-2, arXiv:2501.05206. Background decomposition: cosmogenic neutrons ≈ 21.6 counts/(kg·d) (~50%), cosmic muons ≈ 17.4 counts/(kg·d) (~33%), radon ≈ 2–3 counts/(kg·d) (~5%), leakage-test component <10%, metastable Ge states and radiogenic isotopes subdominant.
- CONUS Collaboration (N. Ackermann *et al.*), *Final CONUS results on coherent elastic neutrino-nucleus scattering at the Brokdorf reactor*, **Phys. Rev. Lett. 133, 251802 (2024)**, DOI 10.1103/PhysRevLett.133.251802, arXiv:2401.07684.
- RICOCHET: collaboration public description (ILL H7); arXiv:2306.00166 (first demonstration of 30 eV_ee ionization resolution); arXiv:2208.01760 (fast-neutron background characterization at ILL); arXiv:2507.22751 (mini-CryoCube: 40 eV_ee ionization, 50–80 eV phonon resolution).

### 4.3 The direct answer to the project's question

**[GAP + CONTEXT — decisive]** I found **no published Ge signal-to-background ratio at a shallow-overburden reactor site in the range 0.65–1.2.** The only *measured* Ge S/B at a reactor is CONUS+'s, of order **0.03** in the 0.4–1 keV_ee band at 7.4 m.w.e., and CONUS+ needed 327 kg·d to reach 3.7σ. **The published state of the art for Ge at a reactor is more than an order of magnitude worse than the number this project intends to claim.**

That does not make the project's number wrong. The QPD wafer differs from CONUS+ in three ways that all push S/B up:
1. a **~10³× lower threshold** (100 meV vs 160 eV_ee) captures the steeply-rising part of the CEvNS recoil spectrum that CONUS+ integrates over only a sliver of;
2. the **Chooz VNS has substantially more overburden** than CONUS+'s 7.4 m.w.e. and sits behind the NUCLEUS shield (per arXiv:2509.03559);
3. there is **no ionization quenching** in the phonon-only readout, so no `eV_ee → eV_nr` conversion penalty and no Lindhard-model systematic.

**But the burden of proof is on us.** The milestone must present S/B explicitly as a function of threshold and overburden, such that the CONUS+ point is *reproduced* as a limiting case at 160 eV_ee and 7.4 m.w.e. **Recommend this as a hard validation checkpoint in the roadmap: if the machinery cannot reproduce CONUS+'s ~0.03 at CONUS+'s threshold and site, the 0.65–1.2 claim is not defensible.**

### 4.4 The Ge-specific background that must not be forgotten: neutron capture

**[INPUT — high priority; Ge-specific; lands inside the v2.0 window]**
> "Neutron capture-induced nuclear recoils … strongly overlap the CEvNS signal for recoils **≲ 100 eV**" in Si and Ge. For a **1 MW reactor at 10 m with 100 kg·yr**, the thermal neutron flux must be "**below ~7×10⁻⁴ n/cm²·s**" for 5σ in **germanium** — "approximately **60% of sea-level neutron flux**." Silicon requires "an order of magnitude lower." Mitigation: "active veto systems tagging deexcitation gamma rays following neutron capture."
> — A. J. Biffl, A. Gevorgian, K. Harris, A. N. Villano, *Neutron capture-induced nuclear recoils as background for CEvNS measurements at reactors*, **Phys. Rev. D 107, 092011 (2023)**, arXiv:2212.14148, DOI 10.1103/PhysRevD.107.092011. *(Simulation study.)*

Physics: `Ge(n,γ)` de-excitation γ emission recoils the nucleus with `T = E_γ²/(2 M c²)`; for MeV-scale γ in Ge this lands at tens-to-hundreds of eV — **inside the upper part of the v2.0 window, produced by exactly the thermal-neutron field a reactor site has.** This citation already appears in the v1.1 survey; what is **new for v2.0** is that the v2.0 window now extends *below* this background's peak, so the model must resolve its spectral shape rather than treat it as a single integrated rate. The project has ENDF/B-VIII.0 n-Ge **elastic** data frozen; the `(n,γ)` recoil channel is a **separate** contribution. It does **not** contaminate the 100 meV bottom bin, but it dominates precisely the 10–500 eV region where the integrated CEvNS rate is largest.

### 4.5 NUCLEUS reference numbers for comparison

- ROI 20–100 eV, expected total counting rate **30 events/(kg·d)** above background; Al₂O₃ background design goal **< 100 counts/(kg·d·keV)**; achieved threshold **(19.7 ± 0.8) eV** on the 0.49 g Al₂O₃ prototype. (NUCLEUS programme documents; arXiv:2211.04189 and collaboration proceedings.)
- Commissioning at the 15 m.w.e. TUM shallow lab: *Commissioning of the NUCLEUS experiment at the Technical University of Munich*, **Phys. Rev. D**, DOI 10.1103/c95p-8kh2.
- VNS background prediction: Abele *et al.* (NUCLEUS), **Eur. Phys. J. C 86, 29 (2026)**, arXiv:2509.03559 — already summarized by the orchestrator; not re-extracted here.
- The v1.1 survey's number ≈ **250 dru in the 10–100 eV ROI** at the VNS, "strongly dominated by cosmic-ray-induced neutrons," is the residual-background anchor and is carried forward unchanged.

> **VERIFICATION FAILURE:** I could **not** retrieve a source stating the NUCLEUS S/B ≈ 1.2 verbatim (SciPost Phys. Proc. 12, 053 returned access-denied). The orchestrator's summary of arXiv:2509.03559 is the authority for that number; cite it from there, not from this file.

---

## 5. Key Results Table (consolidated)

| Result | Expression / Value | Conditions | Source | Year | Tag | Conf. |
| --- | --- | --- | --- | --- | --- | --- |
| IA validity criterion | `q ≫ √(2 m_N ω̄)` ⇔ `E_R ≫ ω̄` | harmonic crystal | Campbell-Deem et al., PRD 106, 036019 | 2022 | INPUT | HIGH |
| Free-recoil breakdown | "recoil energy comparable to a few times the typical phonon energy" | any crystal | ibid. | 2022 | INPUT | HIGH |
| Ge `ω̄` (from `⟨u_x²⟩`) | **12–21 meV** | `T→0`; Debye `Θ_D=374 K` → expt. `B` | this survey | 2026 | DERIVED | MED |
| Ge `2W` at 100 meV | **4.7–8.3** | `T→0` | this survey | 2026 | DERIVED | MED |
| Ge `q·a` at 100 meV | ≈ 144 | `a = 2.45 Å` | this survey | 2026 | DERIVED | HIGH |
| Crystal-coherence ceiling | `E_R ≲ 30 μeV` | Ge, `q ≲ 2π/a` | this survey | 2026 | DERIVED | HIGH |
| Single-phonon deposit ceiling | `ω ≤ ~37 meV` | Ge zone-centre optical phonon | standard solid state | — | CONTEXT | HIGH |
| **IA quantum broadening** | **`σ_E = √(E_R ω̄)`; `σ_E/E_R = 1/√(2W)`**; 35–46% at 100 meV | `2W ≫ 1` (marginal at 100 meV) | Sears, PRB 35, 2038 (framework); this survey (Ge numbers) | 1987 / 2026 | INPUT | MED-HIGH |
| Ge displacement threshold | **19.7 ⁺⁰·⁶ ₋₀·₅ eV** (measurement) | SuperCDMS Ge, ²⁰⁶Pb recoils | Agnese et al., APL 113, 092101 | 2018 | INPUT | HIGH |
| Ge no-defect energy | **~6 eV** (TRIM simulation) | Ge | ibid. | 2018 | INPUT | MED |
| Ge defect energy loss | **6.08 ± 0.18 %** | ~100 keV ²⁰⁶Pb recoils | ibid. | 2018 | INPUT | HIGH |
| **LEE time law (Al₂O₃)** | `R(t)=A(t−t₀)^(−k)`, **`k = 0.59 ± 0.06`**, `t₀` = 4 K crossing | 0.75 g Al₂O₃, 100–300 eV band | NUCLEUS, arXiv:2603.07687 | 2026 | INPUT | MED-HIGH |
| LEE time law (CaWO₄) | `k = 0.73 ± 0.08` | CaWO₄ | ibid. | 2026 | INPUT | MED |
| LEE cooldown-rate effect | slower cooldown ⇒ initial rate lower **by up to 10×** | Al₂O₃ | ibid. | 2026 | INPUT | MED |
| LEE muon-independence | `p_LEE = 0.025 ± 0.004`; ">98% non-muon" | Al₂O₃ | ibid. | 2026 | INPUT | MED-HIGH |
| LEE time law (alternative) | `R(t)=Ae^{−t/τ}+C`, `τ = 149±40 d`; `18±7 d` post-warm-up | CRESST-III, 60–120 eV | arXiv:2207.09375 | 2023 | CONTEXT | MED |
| **Ge LEE amplitude** | **10⁵ / 10⁴ counts/(keV·kg·d) at 200 eV / 1 keV** | EDELWEISS RED20, Ge 33.4 g, **above ground** | arXiv:2202.05097 | 2022 | INPUT | MED |
| Ge LEE underground | factor **~3 lower** | EDELWEISS RED30 | ibid. | 2022 | INPUT | MED |
| Ge LEE effective index | `n ≈ 1.4` over 0.2–1 keV | from the two RED20 points | this survey | 2026 | DERIVED | MED |
| Si LEE flat background | 2×10⁵ counts/(keV·kg·d) above 100 eV; exponential rise below; steeper below 30 eV | SuperCDMS CPD, Si 10.6 g | arXiv:2202.05097 | 2022 | CONTEXT | MED |
| Si CCD LEE energy scale | exponential, decay constant **67 ± 37 eV** | DAMIC, 50–200 eV_ee | ibid. | 2022 | CONTEXT | MED |
| **Stress dependence** | **>100×** rate reduction, glued → suspended | Si, low-stress mount | Anthony-Petersen et al., Nat. Commun. 15, 6444 | 2024 | INPUT | HIGH |
| Al-relaxation model | `R(t) ≈ N/(Γt)`; `N = A_Al ρ_D`; spectrum peaks 10s–100s eV; predicts **meV–eV phonons**; 0.28–0.54 Hz one week post-cooldown | model, not measurement | Romani, JAP 136, 124502 | 2024 | INPUT | MED |
| **Sub-eV burst energy scale** | **`ε = 0.68 ± 0.38 meV`** | bulk Si, shot-noise analysis | Chang et al., APL 127, 263502 | 2025 | INPUT | MED |
| Burst volume scaling | 4 mm noise = **4×** 1 mm noise (0.932 g vs 0.233 g) | Si | ibid. | 2025 | INPUT | MED |
| Burst time decay | `κ = 0.635 ± 0.009` over 12 d | Si | ibid. | 2025 | INPUT | MED |
| Sub-1.8 MeV flux status | **no measurement exists** | all reactor experiments | arXiv:2406.16081; PRD 108, 033002 | 2023–24 | GAP | HIGH |
| Huber–Mueller validity | polynomial fits over **2–8 MeV only** | ²³⁵U/²³⁹Pu/²⁴¹Pu (Huber), ²³⁸U (Mueller) | PRC 84, 024617; PRC 83, 054615 | 2011 | CONTEXT | HIGH |
| `dN/dE_ν → 0` as `E_ν²` | allowed β kinematics; holds branch by branch | every fission-product β decay | textbook | — | INPUT | HIGH |
| `E_min` at `T` = 100 meV | **58.16 keV** (`A = 72.63`) | Ge | this survey | 2026 | DERIVED | HIGH |
| Flux truncation bound | `≲ 17.0 keV × φ(100 keV) / N_tot`; ≲1% with a placeholder `φ` | Ge, `T` = 100 meV, flat-continuation upper bound | this survey | 2026 | DERIVED | MED |
| **CONUS+ Ge background** | **≈ 40 counts/(kg·d)** in 0.4–1 keV_ee, at **7.4 m.w.e.** | HPGe 2.83 kg, 160–180 eV_ee | Nature 643, 1229 | 2025 | INPUT | HIGH |
| **CONUS+ Ge signal** | **395 ± 106** in 327 kg·d = 1.21 counts/(kg·d); 3.7σ; data/SM = 1.14 ± 0.36 | ibid. | ibid. | 2025 | INPUT | HIGH |
| **CONUS+ Ge S/B** | **≈ 0.03** in 0.4–1 keV_ee | ibid. | this survey, from the two rates above | 2026 | DERIVED | MED-HIGH |
| CONUS (Brokdorf) limit | < 0.34 signal events/(kg·d) at 90% CL = factor 2 above SM | 3.73 kg, 210 eV_ee, ~24 m.w.e. | PRL 133, 251802 | 2024 | CONTEXT | HIGH |
| RICOCHET Ge rate | **12.8 events/(kg·d)** at 50 eV threshold (prediction) | ILL 58 MW, 8.8 m, 15 m.w.e. | collaboration | 2025 | CONTEXT | MED |
| Ge (n,γ) recoil overlap | overlaps CEvNS for **recoils ≲ 100 eV**; needs `Φ_th < 7×10⁻⁴ n/cm²·s` for 5σ (1 MW, 10 m, 100 kg·yr) | Ge; simulation | Biffl et al., PRD 107, 092011 | 2023 | INPUT | HIGH |
| NUCLEUS ROI rate | 30 events/(kg·d) in 20–100 eV; Al₂O₃ signal >10× below CaWO₄ | CaWO₄ + Al₂O₃, 19.7 eV threshold | NUCLEUS programme docs | 2022–26 | CONTEXT | MED |

---

## 6. Known Limiting Cases (validation targets)

| Limit | Expected result | Source | How to verify in v2.0 |
| --- | --- | --- | --- |
| `E_R ≫ ω̄` (`E_R ≳ 10 eV` in Ge) | Structure factor → free-nucleus delta; **the v1.0 result must be recovered exactly** | Campbell-Deem et al. 2022 | The new multiphonon/IA machinery must reproduce the frozen v1.0 spectrum above ~10 eV to <1% |
| `E_R → 30 μeV` | Single-phonon / first-BZ regime; free-nucleus picture invalid | this survey [DERIVED] | Confirm the model is never run there; document the floor rationale |
| `E_R` deposit `> 37 meV` | No single-phonon contribution possible | this survey [DERIVED] | Confirms the 100 meV floor is above the single-phonon regime |
| `E_R < 6 eV` | Zero defect-formation loss; `f_phonon = 1` | Agnese et al. 2018 | Adopt as convention; check consistency with the 6.08% high-energy loss |
| Threshold → 160 eV_ee, 7.4 m.w.e., 2.83 kg Ge | S/B ≈ 0.03; 395 ± 106 events in 327 kg·d; 3.7σ | CONUS+, Nature 2025 | **Hard validation checkpoint** for the front-4 S/B machinery |
| Threshold → 50 eV, Ge, ILL geometry | 12.8 events/(kg·d) | RICOCHET | Secondary cross-check of the CEvNS rate integral at a different site/power |
| `T → 0.290 eV` | Must match the frozen v1.0 result exactly (lowest recoil the 100 keV flux floor supports) | v1.0 frozen | Regression test on the flux-grid extension |
| Flux grid 100 → 50 keV | Rate change at `T` = 100 meV must be ≲ the §3.2 bound | this survey [DERIVED] | Compute explicitly; report the number as a headline result |
| Cooldown time-series | LEE ∝ `(t−t₀)^{−0.6}` with `t₀` = 4 K crossing | NUCLEUS arXiv:2603.07687 | Only relevant if v2.0 models an exposure schedule |

---

## 7. Open Questions

1. **[Front 1 — must resolve]** What is the actual reactor-CEvNS `S(q,ω)` for Ge at `E_R` = 0.1–1 eV? No published calculation exists. Route: DarkELF Ge structure factor × CEvNS matrix element. Fallback: free recoil ⊗ Gaussian(`√(E_R ω̄)`) with a stated ~20% uncertainty at the bottom bin.
2. **[Front 1]** Which `ω̄` does the project adopt? The `⟨u²⟩`-derived `ω̄` (12–21 meV) differs from the 37 meV optical-phonon energy by 2–3×, and both `2W` and `σ_E` depend on it directly. Fix in CONVENTIONS.md, with the Ge phonon DOS as arbiter.
3. **[Front 1]** Does the project's `E_rec ≈ 0.5 · E_dep` collection convention hold at 100 meV, where the created phonons are themselves near zone-boundary/optical energies and the down-conversion cascade is truncated? **Not addressed by any source found.** This is an unresolved *detector-physics* assumption, not a literature gap — flag separately.
4. **[Front 2 — cannot resolve from literature]** What is the LEE at 100 meV in Ge? Unmeasured in any material, by two to three decades. The model must present a band with an explicit extrapolation assumption.
5. **[Front 2]** Does the QPD's own Ta/Al/Hf film stack generate a Romani-type aluminium-relaxation background, and how does it scale with the 4″×4″ wafer's film area? This is a **design-dependent** background the model cannot treat as external.
6. **[Front 2]** Chang et al.'s bulk-substrate burst source scales with **volume**; naive extrapolation from 0.93 g to 110 g is ×120. Is that scaling real at 110 g? No data. State as unbounded.
7. **[Front 2]** Reconcile the contradiction that CRESST/RICOCHET holder redesigns produced *no* improvement while Anthony-Petersen's suspension produced >100×. Do not claim mounting "fixes" the LEE.
8. **[Front 3]** Reconcile `E_min(T = 100 meV) = 58.16 keV` (this survey, `A = 72.63`) with the project's frozen **58.7 keV** — a ~1% discrepancy presumably from isotope-abundance weighting of `M_Ge`. Trivial but must be closed, since the whole flux-extension argument is stated in terms of this number.
9. **[Front 3 — cannot resolve from literature]** What is `φ(E_ν)` between 58.7 and 100 keV? Never measured; the one calculation that appears to reach there (JNST 2017) could not be retrieved. Generate with CONFLUX, label as model, lead with the truncation bound.
10. **[Front 4 — must resolve]** Can the S/B machinery reproduce CONUS+'s measured ~0.03 at 160 eV_ee / 7.4 m.w.e.? Until it does, the 0.65–1.2 VNS claim is unvalidated.
11. **[Front 4]** The `Ge(n,γ)` de-excitation recoil spectrum (Biffl et al.) is in the v1.1 survey but not, as far as this survey can tell, in the frozen v1.0 background set. It lands at 10–500 eV, inside the v2.0 window. Add it or explicitly document the omission.

---

## 8. Notation Conventions in the Literature

| Quantity | Standard symbol(s) | Variations | Recommended for this project | Reason |
| --- | --- | --- | --- | --- |
| Nuclear recoil energy | `E_R` | `T`, `E_nr`, `E_rec`, `ω_R` | `T` for CEvNS kinematics (v1.0 convention); `E_R` when quoting the phonon literature | Preserve v1.0; state the mapping once |
| Deposited (phonon) energy | `ω`, `E_dep` | `E_det`, `E_ph` | `E_dep` | Already the project's convention. **In the multiphonon regime `E_dep ≠ T` event-by-event** — this distinction did not matter in v1.0 and now does |
| Momentum transfer | `q` | `Q` (neutron scattering) | `q` | Matches the DM-phonon literature |
| Debye–Waller exponent | `2W(q)` | `e^{−2W}`; `exp(−q²⟨u²⟩/3)` (3-D `⟨u²⟩` convention) | **`2W = q²⟨u_x²⟩`** with `⟨u_x²⟩` **1-D** | **Convention trap:** the `/3` appears only if `⟨u²⟩` is the 3-D sum. State explicitly in CONVENTIONS.md |
| Mean-square displacement | `⟨u²⟩` | `B = 8π²⟨u_x²⟩` (crystallography) | `⟨u_x²⟩` (1-D); quote `B` alongside | Crystallography tables report `B`; the `8π²` is a common error |
| Typical phonon energy | `ω̄`, `ω₀` | `ω_D`, `k_BΘ_D`, `ω_min` | **`ω̄ ≡ ħ/(2 m_N ⟨u_x²⟩)`** | Only this definition makes `2W = E_R/ω̄` exact and `σ_E = √(E_R ω̄)` consistent |
| LEE rate | dru | counts/(keV·kg·d), c/keV/kg/d | **dru**, defined once | NUCLEUS/CRESST standard: "1 dru = 1 count/(keV·kg·d)" |
| LEE time origin | `t₀` | time since cooldown / since 4 K / since base temperature | **`t₀` = 4 K crossing** (NUCLEUS definition) | The `k ≈ 0.6` power law is fitted with this `t₀`; a different origin invalidates it |
| Energy scale | `eV_ee` / `eV_nr` | keVee / keVnr | **Neither** — the project uses a unified phonon scale | But CONUS/CONUS+/EDELWEISS/DAMIC numbers are in `eV_ee`. Conversions must be explicit and flagged at every import |
| Displacement threshold | `E_d` | `T_d`, `E_disp` | `E_d` | Radiation-damage convention |

---

## 9. Sources

**Front 1 — sub-eV recoil physics**
- B. Campbell-Deem, S. Knapen, T. Lin, E. Villarama, **PRD 106, 036019 (2022)**, arXiv:2205.02250 — *primary*: IA validity criterion, single→multi→NR bridge, DarkELF
- B. Campbell-Deem, P. Cox, S. Knapen, T. Lin, T. Melia, **PRD 101, 036006 (2020)**, arXiv:1911.03482 — two-acoustic-phonon rates in Ge/Si/GaAs/diamond
- DarkELF, https://github.com/tongylin/DarkELF — Ge/Si/Al₂O₃ structure factors, directly reusable
- V. F. Sears, **PRB 35, 2038 (1987)**, DOI 10.1103/PhysRevB.35.2038 — IA scaling / final-state effects; the framework behind `σ_E = √(E_R ω̄)`
- S. Knapen, T. Lin, M. Pyle, K. Zurek, **Phys. Lett. B 785, 386 (2018)**, arXiv:1712.06598 — polar vs non-polar optical-phonon coupling
- S. Griffin, S. Knapen, T. Lin, K. Zurek, **PRD 98, 115034 (2018)** — anisotropic/directional phonon response
- Y.-F. Li, S.-y. Xia, **arXiv:2310.05704** (Nucl. Phys. B) — phonon-mediated *Migdal* channel for ν-nucleus scattering (adjacent, not our channel)
- K. Berghaus et al., **arXiv:2112.09702** — γ-induced single/multiphonon background vs solar CEvNS in Si/Ge/GaAs/SiC
- R. Agnese et al. (SuperCDMS), **APL 113, 092101 (2018)**, arXiv:1805.09942 — Ge displacement threshold, no-defect energy, defect energy loss
- S. Sassi et al., **arXiv:2206.06772** — MD simulations of energy loss to lattice defects in low-energy recoils (title/abstract only; not read in this survey)
- TESSERACT Collaboration, **arXiv:2603.17964** (2026) — phonon bursts from fast-neutron lattice damage (title/abstract only; not read)

**Front 2 — LEE**
- P. Adari et al., **SciPost Phys. Proc. 9, 001 (2022)**, arXiv:2202.05097, DOI 10.21468/SciPostPhysProc.9.001 — cross-experiment compilation; **use its public data repository**
- G. Angloher et al. (CRESST), **SciPost Phys. Proc. 12, 013 (2023)**, arXiv:2207.09375 — holder-design and warm-up systematics
- NUCLEUS Collaboration, **arXiv:2603.07687** (2026) — **best available time-dependence parameterization**; cooldown-rate dependence; muon-independence
- R. Anthony-Petersen et al., **Nat. Commun. 15, 6444 (2024)**, arXiv:2208.02790, DOI 10.1038/s41467-024-50173-8 — glued vs suspended, >100× stress dependence
- R. K. Romani, **J. Appl. Phys. 136, 124502 (2024)**, arXiv:2406.15425, DOI 10.1063/5.0222654 — Al-film dislocation model, `1/t`, `A_Al` scaling
- C. L. Chang et al., **APL 127, 263502 (2025)**, arXiv:2505.16092, DOI 10.1063/5.0281876 — **sub-meV burst scale and volume scaling; the closest thing to data inside our window**

**Front 3 — sub-100 keV reactor flux**
- *Impact of reactor neutrino uncertainties on coherent scattering's discovery potential*, **arXiv:2406.16081**, J. Phys. G (2024), DOI 10.1088/1361-6471/ad8ee2 — "no experimental spectral information … for `E_ν < 1.8 MeV`"
- J. Liao, H. Liu, D. Marfatia, **PRD 108, 033002 (2023)**, arXiv:2302.10460 — unfolding upper bounds on the sub-IBD flux with CEvNS
- P. Huber, **PRC 84, 024617 (2011)**; T. A. Mueller et al., **PRC 83, 054615 (2011)** — the frozen flux model; **fitted over 2–8 MeV only**
- X. Zhang, A. Irani, M. P. Mendenhall et al., **arXiv:2503.18966** (2025) — **CONFLUX**; the recommended tool for the 50–100 keV band (ENDF/B-VIII + JEFF-3.3 + ENSDF, configurable grid)
- *Calculation of low-energy electron antineutrino spectra emitted from nuclear reactors with consideration of fuel burn-up*, **J. Nucl. Sci. Technol.**, DOI 10.1080/00223131.2017.1291370 (2017) — **UNVERIFIED (HTTP 403 twice); lead only, do NOT cite until retrieved**
- V. Kopeikin, L. Mikaelyan, V. Sinev, **Phys. At. Nucl. 67, 1892 (2004)**, DOI 10.1134/1.1825513 — six emission components; **paywalled, magnitudes unverified**

**Front 4 — Ge vs CaWO₄/Al₂O₃ at shallow reactor sites**
- CONUS+ Collaboration, **Nature 643, 1229–1233 (2025)**, DOI 10.1038/s41586-025-09322-2, arXiv:2501.05206 — **the benchmark Ge-at-a-reactor measurement**
- CONUS Collaboration, **PRL 133, 251802 (2024)**, arXiv:2401.07684 — Brokdorf final result and background decomposition
- A. J. Biffl, A. Gevorgian, K. Harris, A. N. Villano, **PRD 107, 092011 (2023)**, arXiv:2212.14148 — **Ge (n,γ) recoil background**
- RICOCHET: **arXiv:2306.00166** (30 eV_ee ionization resolution), **arXiv:2208.01760** (ILL fast-neutron background), **arXiv:2507.22751** (mini-CryoCube characterization)
- NUCLEUS: **arXiv:2211.04189** (reactor CEvNS programme); *Commissioning of the NUCLEUS experiment at TUM*, **PRD**, DOI 10.1103/c95p-8kh2; and (orchestrator-supplied) Abele et al., **EPJC 86, 29 (2026)**, arXiv:2509.03559; Angloher et al., **EPJC 79, 1018 (2019)**, arXiv:1905.10258

**Sources attempted and NOT retrieved — do not cite from this file:**
- Taylor & Francis, DOI 10.1080/00223131.2017.1291370 — HTTP 403; Ingenta mirror also 403
- Springer, DOI 10.1134/1.1825513 (Kopeikin components) — authentication redirect
- Springer EPJC, DOI 10.1140/epjc/s10052-024-13551-6 (CONUS+ detector paper) — authentication redirect
- SciPost Phys. Proc. 12, 053 (NUCLEUS proceedings; would have carried the S/B ≈ 1.2 statement) — access denied (Anubis)
- Direct arXiv PDFs for 2205.02250 and 2406.15425 — binary parse failure; **ar5iv HTML used successfully instead**

---

## 10. Forward-Model Input vs Qualitative Context — Summary for the Roadmapper

**Directly usable as forward-model inputs — implement these:**
1. IA quantum broadening `σ_E = √(E_R ω̄)` convolved into the recoil spectrum. **Largest new physics effect in the window: 35–46% at 100 meV, 11–15% at 1 eV, negligible above ~100 eV.** [§1.3(1c)]
2. `f_phonon(E_R) = 1` below 6 eV, ramping to `1 − 0.061` above ~100 eV. [§1.3(1d)]
3. DarkELF Ge `S(q,ω)` × CEvNS matrix element — the rigorous replacement for (1). [§1.5]
4. LEE time law `R(t) = A(t−t₀)^{−0.59±0.06}`, `t₀` = 4 K crossing. [§2.3]
5. LEE amplitude anchors: EDELWEISS Ge 10⁵ / 10⁴ dru at 200 eV / 1 keV above ground; ÷3 underground. [§2.2]
6. Sub-eV burst scale `ε = 0.68 ± 0.38 meV`, volume-scaled. [§2.5]
7. Flux truncation-bound formula for the 58.7–100 keV band. [§3.2]
8. CONFLUX to generate the 50–100 keV flux band as a labelled model. [§3.3]
9. `Ge(n,γ)` de-excitation recoil background; `Φ_th < 7×10⁻⁴ n/cm²·s` requirement. [§4.4]
10. CONUS+ validation point: 160–180 eV_ee, 7.4 m.w.e., 2.83 kg, ≈40 counts/(kg·d) background, 1.21 counts/(kg·d) signal, S/B ≈ 0.03. [§4.2–4.3]

**Qualitative context — shapes the narrative, not the numbers:**
- No crystal-wide coherence anywhere in the window; rebut the misconception explicitly. [§1.3(1a)]
- Single-phonon events sit below the 100 meV floor, which justifies the floor choice. [§1.3(1b)]
- Non-polar Ge suppresses optical-phonon coupling (verify before use). [§1.4]
- LEE stress/mounting origin and the Al-film implication for QPD design — a *design lever*, not just a background. [§2.4]
- CaWO₄ vs Al₂O₃ as a signal / background-monitor pair in NUCLEUS. [§4.1]
- Liao–Liu–Marfatia's call for an ultra-low-threshold CEvNS measurement of the sub-IBD flux is a positive physics case the milestone can claim. [§3.1a]

**Explicit "this is unmeasured" statements the milestone MUST make:**
- No LEE measurement exists below ~10 eV in Ge, or at 100 meV in any material. [§2.6]
- No measurement of the reactor antineutrino spectrum below 1.8 MeV exists anywhere. [§3.1a]
- Huber–Mueller is fitted only over 2–8 MeV; everything below is extrapolation — **including in v1.0**. [§3.1b]
- No published reactor-CEvNS phonon-regime calculation exists for Ge. [§1.5]
- No published Ge S/B at a shallow reactor site is anywhere near 0.65–1.2; the only measured value is ≈0.03 (CONUS+). [§4.3]
</content>
