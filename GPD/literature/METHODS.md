# Methods Research — v1.1 Neutron-NR and Radiogenic In-Band Backgrounds

**Domain:** Neutron-induced Ge nuclear-recoil and detector-material radiogenic background spectra
for a thin (2 mm, ~110 g) natural-Ge wafer at surface, folded to reconstructed energy through the
existing v1.0 QPD response chain.
**Researched:** 2026-07-21
**Confidence:** MEDIUM-HIGH (source-grounded parametrizations; surface-flux normalization and
detector radiopurity budget carry the largest residual uncertainty)

> **Scope note.** This file is the v1.1 (subsequent-milestone) methods survey. The v1.0 methods
> (Freedman CEvNS + Helm; Gaisser–Guan muon flux × ray-box chord × Landau–Vavilov; Klein–Nishina
> Compton; the MC response chain producing `R(E_rec | E_dep)`) are archived at
> `GPD/milestones/v1.0/literature/METHODS.md` and are **reused, not re-researched**. Everything below
> is the NEW background physics. Every new channel must land on the **unified phonon `E_dep` scale
> with NO ionization quenching** (CONVENTIONS Section B) and be folded through the existing
> `R(E_rec | E_dep)` matrix on the shared log grid (`0.01 keV → 200 MeV`, ~80 bins/decade;
> `muon_deposit.shared_energy_grid`).

---

## Governing kinematics and the shared folding operator

All five channels reduce to the same two-step analytic pipeline, which is the central methodological
recommendation:

1. **Source → `dR/dE_dep` on the shared grid** (channel-specific; below).
2. **Fold** `dR/dE_rec = ∫ R(E_rec | E_dep) · dR/dE_dep dE_dep` reusing the v1.0 response matrix.

**Neutron elastic recoil kinematics (HIGH confidence, textbook).** For a neutron of energy `E_n`
elastically scattering off a Ge nucleus of mass number `A`, the recoil kinetic energy is
`T_r = [2A/(1+A)²]·(1 − cosθ_cm)·E_n`, with maximum `T_max = 4A/(1+A)² · E_n`. For Ge (`A≈72.6`),
`4A/(1+A)² ≈ 0.0538`, so `T_max ≈ 0.054·E_n` — a 1 MeV neutron produces up to ~54 keV_nr; the
tens-of-eV-to-keV CEvNS ROI is populated by the forward-scatter (small-`θ_cm`) part of neutrons from
tens of keV up to a few MeV. `T_r ≡ E_nr` is deposited **in full as phonons** (no Lindhard/quenching,
CONVENTIONS B); the same few-% Frenkel-defect NR-only correction as CEvNS applies and nothing more.

**Recoil-spectrum fold (HIGH confidence).** `dR/dT_r = N_Ge ∫ φ(E_n) · (dσ_el/dT_r)(E_n) dE_n`,
with `N_Ge` the target-atom number. Under the s-wave (isotropic-CM) approximation valid at low
`E_n`, `dσ_el/dT_r = σ_el(E_n)/T_max(E_n)` is a **flat box in `T_r`** from 0 to `T_max` — the fold is
a single 1-D quadrature over the incident spectrum. This box form is the workhorse for the ROI.

---

## Recommended Methods

### Analytical Methods

| Method | Purpose | Why Recommended |
| ------ | ------- | --------------- |
| Isotropic-CM (s-wave) flat-box recoil kernel `dσ/dT_r = σ_el/T_max` | Fold any incident neutron spectrum → `dR/dT_r` in the ROI | Exact for `E_n ≲ 0.5–1 MeV` where n-Ge elastic scattering is s-wave dominated; reduces every neutron channel (cosmogenic, muon-induced, radiogenic) to one 1-D integral. This is the ROI-dominant regime. |
| Thin-target single-scatter approximation | Justify skipping full neutron transport in the 2 mm wafer | Fast-neutron elastic mean free path in Ge is `λ = 1/(N σ_el) ≈ 5–6 cm` (`N≈4.4×10²²/cm³`, `σ_el≈3–4 b`) ≫ 0.2 cm wafer → interaction probability `t/λ ≈ 3–4%`, multiple-scatter `~0.1%`. Single-scatter fold is accurate to ≪1%. |
| Legendre-coefficient angular fold `dσ/dT_r ∝ Σ aℓ(E_n) Pℓ(cosθ)` | Forward-peaking correction for `E_n ≳ 1 MeV` | Above ~1 MeV the CM angular distribution becomes forward-peaked; the `a₁` (and higher) Legendre coefficients from ENDF/B-VIII.0 File-4 skew the recoil box toward low `T_r`. Needed only for the high-`E_n` tail of the ambient/muon-induced spectra. |
| Watt fission-neutron spectrum `N(E)=C·exp(−E/a)·sinh√(bE)` | ²³⁸U spontaneous-fission source term | Standard closed form; Los Alamos parameters for ²³⁸U SF `a=0.7124 MeV, b=5.6405 MeV⁻¹` (mean ≈2 MeV). Feeds directly into the flat-box fold. |
| Solid-angle × exponential-attenuation transport `exp(−μx)` | Housing/stack gamma & neutron sources reaching the wafer | For sources OUTSIDE the Ge (QPD stack, wirebonds, housing), the wafer subtends a small solid angle; gamma attenuation uses `μ(E)` from NIST XCOM, neutron non-interaction over the standoff is ~1. Analytic, no MC transport needed. |
| Klein–Nishina Compton continuum (REUSE v1.0 `compton_deposit.py`) | U/Th/⁴⁰K + intrinsic gamma → electron-recoil deposit | The v1.0 external-ambient-gamma machinery already produces the ER Compton continuum on the phonon scale; extend its input line list, do not rewrite. |
| Full-absorption β/EC deposit for intrinsic isotopes | ³H, ⁶⁸Ge/⁶⁸Ga, ⁶⁵Zn born INSIDE the Ge | A β/Auger/X-ray emitted in the bulk deposits its FULL energy (range ≪ mm). ³H β-continuum (endpoint **18.6 keV**) and the ⁶⁸Ga/⁷¹Ge K-shell EC lines (~10.4 keV) land directly in the ROI on the phonon scale — model as a bulk full-energy deposit, not a Compton continuum. |

### Numerical (Monte-Carlo) Methods

| Method | Purpose | When to Use |
| ------ | ------- | ----------- |
| 1-D importance-sampled quadrature (scipy) | Evaluate the `∫ φ(E_n) dσ/dT_r dE_n` folds | Default for all neutron recoil spectra — deterministic, fast (<1 s), reproducible; no MC noise. |
| Thin-wafer single-scatter MC (bespoke numpy, mirrors `muon_deposit._mc_batch`) | Cross-check the analytic fold; propagate angular (Legendre) distributions and the entry-point/chord geometry | Use when the `a₁` forward-peaking correction or the wafer-edge geometry matters, or to verify the single-scatter fraction. Same batched-accumulator pattern already in the repo. |
| Decay-chain line sampler | Build the U/Th/⁴⁰K gamma line+continuum source before Compton folding | Sample emission lines with ENSDF branching ratios, then push through the reused Klein–Nishina machinery. |

### Computational Tools

| Tool/Library | Version | Purpose | Notes |
| ------------ | ------- | ------- | ----- |
| numpy / scipy | existing repo pins | All folds, quadrature, MC accumulators | Reuse the v1.0 stack; no new heavy dependency. |
| ENDF/B-VIII.0 (n,elastic) for ⁷⁰,⁷²,⁷³,⁷⁴,⁷⁶Ge | 2018 release | `σ_el(E_n)` and File-4 Legendre coefficients | Get pointwise data from IAEA/NNDC. Parse with `endf-parserpy`/`openmc.data` OR export a pre-tabulated `σ_el(E_n)`, `a₁(E_n)` CSV (recommended — avoids adding OpenMC as a runtime dep). JEFF-3.3 is an equivalent cross-check library. |
| NIST XCOM | web/DB | Gamma mass-attenuation `μ(E)` in Ge and housing | For self-shielding/attenuation and the photoelectric/Compton/pair partition in the 2 mm wafer. |
| ENSDF / `radioactivedecay` (py) | current | U/Th/⁴⁰K/⁶⁸Ge/⁶⁵Zn/³H line energies, intensities, half-lives | Table-driven decay lines; lighter than a Geant4 RDM run and sufficient for a rough estimate. |
| Gordon et al. (2004) analytic sea-level spectrum | fixed parametrization | Ambient cosmogenic fast-neutron flux `φ(E_n)` | Static reference spectrum (= JEDEC JESD89 basis). Use EXPACS/PARMA (Sato) or CRY only if altitude/geomagnetic/solar-cycle scaling to a specific site is required. |
| SOURCES-4C **or** NeuCBOT **or** published (α,n) yield tables | 4C (legacy) / current | `(α,n)` neutron yield & spectrum per U/Th ppb per material | Prefer published per-material yield tables + the emitted-neutron spectrum as analytic inputs; run SOURCES-4C/NeuCBOT only if a specific stack material is missing from tables. |

## Software Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
| ---------- | ------- | ------- | --------------- |
| Python + numpy/scipy | existing | Analytic folds, 1-D quadrature, bespoke single-scatter MC, response folding | The entire v1.0 forward model/response pipeline is numpy/scipy; every new channel plugs into the same shared grid and `R(E_rec|E_dep)` matrix. |
| Static nuclear-data CSVs (ENDF-derived `σ_el`, `a₁`; decay-line tables; Gordon spectrum; Watt/(α,n) spectra) | committed to `data/` | Reproducible inputs without heavy runtime libraries | Keeps the calculation self-contained and reviewable; matches the existing `data/` + `src/flux` table pattern. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
| ------- | ------- | ------- | ----------- |
| `endf-parserpy` or `openmc.data` | current | One-off ENDF → CSV extraction of `σ_el(E_n)`, `a₁(E_n)` | Build-time only; do not make it a runtime dependency. |
| `radioactivedecay` | current | Decay-chain line/branching tables for the gamma+beta source | Build the U/Th/⁴⁰K line list and intrinsic-isotope spectra. |
| `pandas` | existing | Tabulated flux/yield/line I/O | Same role as in `src/flux/build_flux_table.py`. |

### Symbolic Computation

| Tool | Version | Purpose | Notes |
| ---- | ------- | ------- | ----- |
| (none required) | — | Kinematics closed-form; no symbolic algebra needed | The recoil kinematics and Watt/Klein–Nishina forms are elementary; keep everything numeric as in v1.0. |

## Installation

```bash
# Reuse the existing environment
uv sync   # or the repo's existing pip/uv workflow

# Build-time only, for ENDF -> CSV extraction and decay tables (not runtime deps):
pip install endf-parserpy radioactivedecay   # openmc optional, heavier

# External static data (download once, commit to data/):
#   - ENDF/B-VIII.0 (n,elastic) File-3/File-4 for Ge isotopes  (IAEA/NNDC)
#   - Gordon 2004 sea-level neutron spectrum parametrization
#   - NIST XCOM Ge attenuation table
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
| ----------- | ----------- | ----------------------- |
| Analytic single-scatter flat-box fold | Full Geant4/FLUKA/MCNP neutron transport | Only as a **light, single-material cross-check** of the single-scatter fraction and the high-`E_n` inelastic tail. Out of scope as the primary method (too heavy for a rough estimate; explicit HARD CONSTRAINT). Flag the ~3–4% interaction-probability and multiple-scatter numbers as the things a light MCNP/Geant4 run would confirm. |
| Gordon 2004 static sea-level spectrum | EXPACS/PARMA (Sato) or CRY generator | When a specific altitude, geomagnetic cutoff, or solar-cycle epoch must be matched, or when a full time-correlated shower (muon+neutron together) is wanted. |
| Published (α,n) yield tables | SOURCES-4C / NeuCBOT direct run | When the stack material (specific ceramic, epoxy, Ta/Al/Hf films) is absent from published tables and its light-element (α,n) yield must be computed from stopping power + cross sections. |
| `radioactivedecay`/ENSDF line list + reused Klein–Nishina | Geant4 Radioactive Decay Module full-chain sim | When coincidence-summing or true-vs-observed cascade correlations in the small crystal become load-bearing — not expected at rough-estimate stage. |

## What NOT to Use

| Avoid | Why | Use Instead |
| ----- | --- | ----------- |
| Lindhard / ionization quenching on neutron recoils | Neutron NR is on the SAME unified phonon scale as CEvNS; applying quenching would suppress it ~5–7× and is physically wrong for a fieldless phonon calorimeter (CONVENTIONS B, forbidden proxy) | Deposit full `T_r` as phonons; only the few-% Frenkel-defect NR correction applies. |
| keVee↔keVnr conversion for any neutron/gamma channel | Mixing scales is forbidden here; ER and NR deposits share one axis | Keep everything on `E_dep`, fold through the single `R(E_rec|E_dep)`. |
| G4CMP phonon-transport simulation | Explicitly OUT OF SCOPE | The response is already captured by the v1.0 `R(E_rec|E_dep)` matrix. |
| Full Geant4/FLUKA shower simulation as the primary engine | Too heavy for a rough-estimate milestone | Parametrized flux/yield + analytic single-scatter fold; light MC only as cross-check. |
| Adding muon-induced atmospheric neutrons on top of the Gordon ambient flux | **Double-counting**: the Gordon sea-level spectrum ALREADY contains neutrons produced by atmospheric muon/hadron cascades | Restrict the muon-induced channel to neutrons produced IN the wafer + immediate housing by the same through-going muons v1.0 already models (see below). |

## Double-Counting Hazard — muon-induced neutrons vs the v1.0 muon channel and the ambient flux

This is the central methodological trap for v1.1 and must be resolved at the method level:

1. **vs the v1.0 direct-ionization muon channel.** `muon_deposit.py` already deposits each muon's
   direct ionization (Landau–Vavilov MPV per chord). Muon-induced neutrons are **secondaries**: the
   neutron elastically scatters off Ge and produces a distinct nuclear recoil. Adding this recoil is
   **not** double-counting deposited energy. The requirement is normalization discipline — the
   neutron-production rate MUST be driven by the SAME Gaisser–Guan muon flux/intensity already
   integrated in `run_muon_mc` (do not introduce a second, independent muon population).
2. **vs the ambient cosmogenic flux (channel 3).** The Gordon sea-level spectrum is dominated by
   atmospheric muon/hadron-cascade neutrons. Therefore the muon-induced channel must be **restricted
   to LOCAL production** — neutrons spalled in the 110 g wafer and its immediate housing by the
   through-going muons — otherwise the atmospheric component is counted twice.
3. **Magnitude sanity.** In-wafer production is tiny: Wang (2001) yield
   `N_n ≈ 4.14×10⁻⁶ E_μ^0.74 n/(μ·g·cm⁻²)`; a vertical muon traverses only `ρℓ ≈ 0.11 g/cm²`, so
   in-wafer muon-induced neutrons are ~10⁻⁶ per muon — negligible vs the ambient elastic-recoil rate.
   The muon-induced term is dominated by production in surrounding material and is **subdominant at
   surface**; treat it as a bounded correction, not a flagship channel, and state the assumed housing
   mass/composition.

## Method Selection by Problem Type

**Ambient cosmogenic fast-neutron NR (highest-priority NR background):**
- Use the Gordon-2004 sea-level `φ(E_n)` × isotropic-CM flat-box fold (+ `a₁` correction above 1 MeV).
- Because it lands directly in the CEvNS ROI, is undiscriminable on the phonon scale, and the surface
  flux is orders of magnitude above any shielded reference — this is the dominant new NR term.

**Muon-induced local neutrons:**
- Use Wang-2001 / Mei–Hime-2006 yield+spectrum parametrizations, normalized to the v1.0 muon flux,
  restricted to wafer+housing production, folded through the same flat-box kernel.
- Because it must not double-count the atmospheric component and is a bounded subdominant correction.

**Radiogenic (α,n) + SF neutrons from U/Th in the stack/housing:**
- Use published (α,n) yield tables + Watt SF spectrum per assumed U/Th ppb, × solid-angle, × flat-box.
- Because a full SOURCES-4C run is only needed for materials absent from tables; the estimate is
  gated by the (unknown) radiopurity budget, not by the transport.

**Radiogenic gamma/β ER (dominant ER background by analogy to RELICS):**
- Reuse the v1.0 Klein–Nishina Compton continuum for U/Th/⁴⁰K + housing gammas (with XCOM
  attenuation/self-shielding); add bulk full-energy deposits for intrinsic ³H, ⁶⁸Ge/⁶⁸Ga, ⁶⁵Zn.
- Because the thin 2 mm wafer lets most MeV gammas escape (Compton-continuum-dominated, few full-energy
  peaks — favorable for the existing single-Compton machinery), while the in-bulk ³H β-continuum
  (endpoint 18.6 keV) is the crucial in-ROI ER term.

**Cosmogenic activation inventory (source term for the intrinsic-isotope deposits):**
- Use measured sea-level production rates (CDMSlite/EDELWEISS-III) × assumed surface-exposure and
  cooldown times to set the ³H/⁶⁸Ge/⁶⁵Zn activities, then feed the bulk-deposit model.
- Because unshielded surface operation makes this worse than for underground experiments and it is
  fixed by an exposure scenario, not a transport calculation.

## Validation Strategy by Method

| Method | Validation Approach | Key Benchmarks |
| ------ | ------------------- | -------------- |
| Flat-box recoil kernel | Check `T_max = 4A/(1+A)²·E_n ≈ 0.054 E_n` for Ge; verify the box integrates to `σ_el·N_Ge`; recover a flat `dR/dT_r` for a mono-energetic sub-MeV neutron | Textbook n-A elastic kinematics; ENDF `σ_el(E_n)` ≈ few barn thermal→MeV |
| Single-scatter approximation | Compute `t/λ` and compare a bespoke single-scatter MC to the analytic fold; verify multiple-scatter ≪ single | `λ≈5–6 cm` in Ge → `~3–4%` interaction probability in 2 mm |
| Ambient CRN fold | Integral flux check against Gordon: `>1 MeV` sea-level flux `≈1.3×10⁻² n·cm⁻²·s⁻¹` (NYC reference); compare ROI recoil rate to RELICS post-shield residual scaled to unshielded surface | Gordon 2004 (IEEE TNS 51, 3427); RELICS Sec. V (PRD 110, 072011) |
| Muon-induced yield | Reproduce Wang-2001 `N_n` normalization; flag that the ~4 GeV mean SURFACE muon energy is at the soft edge of the parametrization's validity | Wang hep-ex/0101049; Mei–Hime PRD 73, 053004 |
| (α,n) + SF | Mean SF neutron energy ≈2 MeV (Watt `a,b` above); benchmark (α,n) yield against published Ge/material tables (~20–50% spread) | SOURCES4 arXiv:2211.02080; Westerdale–Meyers arXiv:1702.02465 |
| Gamma/β ER | Reproduce dominant line energies (1460 keV ⁴⁰K; 2615 keV ²⁰⁸Tl; 609/1120/1764 keV ²¹⁴Bi); ³H endpoint 18.6 keV; ⁶⁸Ga EC K-line ~10.4 keV; production rates ³H ≈74–82, ⁶⁵Zn ≈17, ⁶⁸Ge ≈30 atoms/kg/day sea level | ENSDF; CDMSlite tritium/cosmogenic (Astropart. Phys. 2018), EDELWEISS-III (arXiv:1607.04560) |

## Version Compatibility

| Component | Compatible With | Notes |
| --------- | --------------- | ----- |
| New neutron/radiogenic channels | v1.0 `muon_deposit.shared_energy_grid` (0.01 keV→200 MeV, 80/decade) | All channels MUST use this grid so they co-add on `E_dep`. |
| New channels | v1.0 `response_matrix.R(E_rec\|E_dep)`, non-paralyzable censoring (CONVENTIONS F) | Fold every channel through the SAME response matrix per QPD design. |
| ENDF/B-VIII.0 | JEFF-3.3 | Use JEFF as an independent `σ_el` cross-check; discrepancies below ~1 MeV are small. |

## Sources

- Neutron elastic kinematics & thin-target single-scatter: standard reactor/detector physics; "Features
  of Fast Neutrons in Dark Matter Searches" (arXiv:1009.3791); ZEPLIN-III (arXiv:2007.01683).
- ENDF/B-VIII.0: Brown et al., *Nucl. Data Sheets* 148, 1 (2018), doi:10.1016/j.nds.2018.02.001
  (OSTI 1427384). Ge cross sections & File-4 angular data via IAEA/NNDC.
- Ambient cosmogenic neutron flux: Gordon et al., *IEEE Trans. Nucl. Sci.* 51, 3427 (2004),
  2004ITNS...51.3427G (+ Correction); basis of JEDEC JESD89. Site scaling: Sato PARMA/EXPACS.
- Muon-induced neutrons: Wang et al., "Predicting Neutron Production from Cosmic-ray Muons,"
  arXiv:hep-ex/0101049 (`N_n≈4.14×10⁻⁶E_μ^0.74`); Mei & Hime, *Phys. Rev. D* 73, 053004 (2006),
  doi:10.1103/PhysRevD.73.053004.
- Radiogenic (α,n) + SF: SOURCES4 (arXiv:2211.02080; Wilson et al. code); Westerdale & Meyers
  (NeuCBOT), arXiv:1702.02465, *NIM A* 875, 57 (2017); Mei, Yin, Elliott (α,n) evaluation. ²³⁸U SF
  Watt parameters `a=0.7124 MeV, b=5.6405 MeV⁻¹` (Los Alamos model).
- Gamma/β decay-chain modeling & self-absorption: ENSDF; `radioactivedecay` py package; NIST XCOM
  (Ge attenuation); Geant4 RDM validation refs (as heavier alternative).
- Ge cosmogenic activation rates: CDMSlite tritium/cosmogenic production (*Astropart. Phys.* 2018);
  EDELWEISS-III, arXiv:1607.04560; review arXiv:1708.07449.
- Background anchor / channel inventory: RELICS reactor-CEvNS study, Cai et al., *Phys. Rev. D* 110,
  072011 (2024) (same 3 GW, 25 m configuration).

---

_Methods research for: v1.1 neutron-NR and radiogenic in-band backgrounds, thin-Ge QPD forward model_
_Researched: 2026-07-21_
