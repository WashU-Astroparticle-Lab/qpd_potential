# Computational Approaches: v2.0 VNS Deployment + Extension to 100 meV (QPD-Ge)

**Surveyed:** 2026-07-22
**Domain:** Reactor-site low-background physics — shielded neutron transport data, sub-100-keV reactor antineutrino flux, crystal/phonon response of Ge at sub-eV recoil
**Confidence:** MEDIUM-HIGH. Every URL, package version, file size, and byte-range capability quoted below was probed live this session (HTTP status, `Content-Length`, `Accept-Ranges`) or read out of the fetched file itself. Items I could not verify are marked **[UNVERIFIED]** and must not be planned around as facts.

> **Milestone note:** This is the **v2.0** computational survey. It supersedes the v1.1 `COMPUTATIONAL.md` (neutron-NR + radiogenic backgrounds), which remains in git history. The v1.0/v1.1 stack is **reused, not replaced** — see Reuse Constraint.

---

## Scope and Reuse Constraint

v2.0 relocates the wafer to the NUCLEUS Chooz Very-Near-Site (VNS) behind the NUCLEUS shielding and extends every spectrum down to 100 meV. Nothing in this document proposes replacing the existing stack.

**Reused verbatim:** Python 3.11 / numpy / scipy / matplotlib; `src/qpd_potential/` (`cevns.py`, `response.py`, `response_matrix.py`, `fold.py`, `deposited_spectra.py`, `energy_scale.py`, `params.py`); `src/flux/`; `src/nuclear/`; `shared_energy_grid()`; the frozen-CSV-with-provenance-header convention exemplified by `data/endf_nGe_elastic_v1.1.csv`; and — critically — the `HTTPRangeFile` remote-ZIP reader in `src/nuclear/fetch_ace_lib80x.py`, which is the single most reusable asset for everything in Section 1.

**HARD CONSTRAINTS honoured:** no G4CMP, no Geant4, no MCNP/FLUKA. **openmc and NJOY are treated as unbuildable on osx-arm64** (established in a prior phase). Every recommendation below either (a) is pure Python / has a native arm64 wheel, or (b) consumes data that somebody else already ran NJOY on.

---

## Recommended Stack

**Shield nuclear data (Q1a).** Do not process anything. LANL **Lib80x** (`https://nucleardata.lanl.gov/lib/Lib80x.zip`, 7,053,992,984 B = 7.05 GB, `Accept-Ranges: bytes` **verified**) already contains NJOY-2016-processed, resonance-reconstructed, Doppler-broadened (293.6 K, `.800nc`) pointwise ACE for every ENDF/B-VIII.0 neutron nuclide — Pb, B, Li, C, H, O, Cu, Si included. The existing `HTTPRangeFile` + stdlib `zipfile` reader pulls individual members with ~MB of range requests instead of a 7 GB download. This is exactly the route already used for the five Ge isotopes and it generalises by changing a ZAID table. For hydrogen bound in polyethylene, add **ENDF80SaB2** (`https://nucleardata.lanl.gov/lib/ENDF80SaB2.zip`, 2,565,465,484 B = 2.57 GB, `Accept-Ranges: bytes` **verified**), which carries a `h-poly` thermal-scattering-law table among its 34 materials.

**Above 20 MeV (Q1b).** **TENDL-2023** is the answer and it is a direct single-file download — no archive, no processing. `https://tendl.imperial.ac.uk/tendl_2023/neutron_file/Ge/Ge074/lib/endf/n-Ge074.tendl` returned HTTP 200, 3,355,911 B, and its own header line reads `TENDL-2023 gen. purp. file: neutron + Ge- 74  1.e-5 eV - 200 MeV`. I read MF=3/MT=2 out of the downloaded file: 305 points, terminating at `2.000000+8 5.680830-1` (200 MeV, 0.568 b). Splice it onto the frozen ENDF/B-VIII.0 table at 20 MeV — see the measured continuity step in Validation.

**Sub-100-keV antineutrinos (Q2).** **CONFLUX v1.1.3** (LLNL, MIT, `github.com/CNFLUX/conflux`, released 2026-07-16). Pure-Python summation engine with a Python port of the Beta Spectrum Generator corrections bundled in `conflux/bsg/`; the C++ `miniBSG/` tree is a separate reference implementation, not a required build. The spectral grid `xbins` is a user-supplied array (default `np.arange(0, 20, 0.1)` MeV) — it is not hard-floored at 100 keV, so extending to 58.7 keV is a parameter change, not a code change. This is the only laptop-runnable, publicly distributed summation code in the field: BESTIOLE is not distributed, FISPACT-II is licence-gated and does not emit antineutrino spectra anyway.

**Crystal / low-q response (Q3).** **NCrystal 4.4.6** (`pip install ncrystal`; `ncrystal_core-4.4.6-py3-none-macosx_11_0_arm64.whl`, 2.5 MB — a **native arm64 wheel exists**, no build) with the bundled `Ge_sg227.ncmat`, plus **DarkELF** (pure Python, numpy/scipy/pyyaml/pandas) for the multiphonon structure factor and its shipped `data/Ge/Ge_pDoS.dat`. **But read the Impulse-Regime Finding in Section 3 before planning a phase around either** — the arithmetic says the whole 100 meV–20 eV band sits *above* the regime where crystal binding is a leading effect, which turns these tools from a modelling backbone into a one-off justification calculation.

**Digitization (Q4).** Upgrade to **vector extraction** with PyMuPDF 1.28.0: arXiv PDFs are vector, so the published polyline vertices can be read exactly out of the content stream instead of being recovered from a 300-dpi raster. Keep the existing raster pipeline as the fallback for genuinely bitmap figures, and report digitization error using the scaled median symmetric accuracy ζ from Wojtyniak et al. (2020), measured by a synthetic round-trip.

**Published data (Q5).** One real win: **CRESST-III arXiv:1905.07335v3 ancillary files** are event-level energies down to 29.6 eV, publicly downloadable, no digitization. Everything from NUCLEUS, CONUS/CONUS+, and RICOCHET is on-request only — I checked each arXiv record individually and none carries ancillary files. The **Goupy 2024 thesis full text is public** (73.7 MB PDF, verified) and is the best available proxy for VNS background detail.

---

## 1a. Shield-Material Nuclear Data

### What Lib80x provides and how to get it

| Item | Value | Status |
|---|---|---|
| Archive URL | `https://nucleardata.lanl.gov/lib/Lib80x.zip` | HTTP 200 verified |
| Size | 7,053,992,984 B (7.05 GB) | `Content-Length` verified |
| Byte ranges | `Accept-Ranges: bytes` | verified |
| Basis | ENDF/B-VIII.0 neutron sublibrary, processed by NJOY2016 | LA-UR-18-24034 |
| Temperatures | 293.6 K (`.800nc`), 600/900/1200/2500 K, 0.1 K (`.805nc`), 250 K | LANL `/ace/lib80x/` page |
| Content | Pointwise, resonance-reconstructed, Doppler-broadened σ + angular data | already exploited in v1.1 |

**Nuclides needed for the shield.** ZAID = 1000·Z + A; the existing loader resolves members from the archive central directory (it does not hardcode paths), so extending the ZAID table is the whole change.

| Shield material | Nuclides (ZAID) | Reactions that matter |
|---|---|---|
| Lead | Pb-204/206/207/208 (82204/82206/82207/82208) | MT=2 elastic (Pb is a gamma shield and a neutron reflector, a poor moderator), MT=102 (n,γ), MT=16 (n,2n) |
| Polyethylene (CH2) | H-1 (1001), C-12 (6012), C-13 (6013) | MT=2 on H-1 dominates moderation; H-1 (n,γ) MT=102 makes the 2.223 MeV capture gamma |
| Borated PE / B4C | B-10 (5010), B-11 (5011) | **B-10 (n,α) MT=107** (+ discrete MT=800/801); the absorber, and an IAEA/CSEWG neutron cross-section standard in ENDF/B-VIII.0 |
| Li-loaded (if present) | Li-6 (3006), Li-7 (3007) | **Li-6 (n,t)α is MT=105**, also a standard |
| Copper | Cu-63 (29063), Cu-65 (29065) | MT=2, MT=102; activation relevance |
| Silicon | Si-28/29/30 (14028/14029/14030) | MT=2, MT=102 |

> **Convention trap:** B-10(n,α) is MT=107 and Li-6(n,t) is MT=105 — different MT numbers for what a physicist calls "the same" thermal-absorber reaction. Do not write one loop that assumes MT=107 for both.

> **[UNVERIFIED]** The per-element directory naming *inside* the archive was confirmed only for Ge (`Lib80x/Lib80x/Ge/<ZAID>.<ext>`). Do not hardcode `Lib80x/Lib80x/Pb/...`; enumerate the central directory (the existing loader already does) and assert the member exists before reading. This is a 30-second check, not a risk.

### Thermal scattering (bound hydrogen in polyethylene)

Free-gas H-1 elastic is wrong below ~1 eV in a hydrogenous moderator; the C–H molecular modes must be used.

| Item | Value | Status |
|---|---|---|
| Archive | `https://nucleardata.lanl.gov/lib/ENDF80SaB2.zip` | HTTP 200, `Accept-Ranges: bytes` verified |
| Size | 2,565,465,484 B (2.57 GB) | verified |
| Released | 2018-07-26; **SaB2 is the corrected library** — SaB (v1) contained faulty/mis-processed files | LANL page |
| Materials | 34 total. Relevant: `h-poly` (hydrogen in polyethylene), `h-luci` (Lucite), `grph`/`grph10`/`grph30`, `sio2`, `si-sic`, `c-sic`, `al-27`, `fe-56` | full list read off LANL page |
| ZAID extension | `.40t` for the room-temperature table | LANL page |

**Hard negatives read directly off that 34-material list — plan around these, they are not oversights:**
- **No germanium TSL exists in ENDF/B-VIII.0.** This is precisely why Section 3 needs NCrystal.
- **No elemental crystalline silicon** (only `sio2` and `si-sic`).
- **No lead, no copper, no boron, no B4C.** For these, bound-atom effects are small compared with H, and free-atom ACE is adequate — say so explicitly rather than silently omitting.

### Should we move to ENDF/B-VIII.1?

`Lib81` exists: `https://nucleardata.lanl.gov/lib/Lib81.zip`, 9,468,760,553 B (9.47 GB), `Accept-Ranges: bytes` verified, released 2025-09-11, based on the NNDC ENDF/B-VIII.1 release of 2024-08-30.

**Recommendation: stay on VIII.0/Lib80x for the frozen tables.** The frozen n-Ge elastic table is VIII.0; mixing library versions across materials in one chain is a provenance hazard for no physics gain at our precision. Use Lib81 only as an explicit *sensitivity variant*, and if so re-fetch **all** materials from Lib81, not a subset.

### What is NOT needed

**NJOY is not needed and should not be attempted.** Lib80x/ENDF80SaB2 are the NJOY *output*. The v1.1 phase already established this substitution works and cross-checked ACE against the raw MF=3 background to float32 storage precision. The same argument covers every shield nuclide.

---

## 1b. Above 20 MeV

### The ceiling is real

ENDF/B-VIII.0 (and VIII.1) general-purpose evaluations for Ge terminate at 20 MeV. `shared_energy_grid()` runs to 197 MeV and muon-induced neutrons at the VNS extend well past 20 MeV, so the gap is physically live, not cosmetic.

### TENDL-2023 — verified, recommended

| Item | Value | How verified |
|---|---|---|
| Per-nuclide URL | `https://tendl.imperial.ac.uk/tendl_2023/neutron_file/Ge/Ge074/lib/endf/n-Ge074.tendl` | HTTP 200, downloaded |
| Size | 3,355,911 B | `Content-Length` + `ls` |
| Byte ranges | `Accept-Ranges: bytes` | verified |
| Energy range | `1.e-5 eV - 200 MeV` | read from the file's own line-1 header |
| MAT | 3237 (same MAT as ENDF/B-VIII.0 ⁷⁴Ge) | read from columns 67–70 |
| Evaluators | A. J. Koning and D. Rochman, IAEA, `EVAL-DEC23` | read from MF=1/MT=451 |
| MF=3 MT=2 | present, 305 points, ends `2.000000+8  5.680830-1` | parsed from file |
| MF=2 | present (MAT 3237, 2151), resolved region `1.000000-5` to `6.120000+4` eV | parsed from file |
| Other MF=3 MTs | 1,2,3,4,5,11,16,17,22,24,25,28,29,32,33,34,37,41,42,44,45,51–69,91,102–108,111,112,115,116,117 | parsed from file |
| Release choice | the **August 2024** neutron release is the one TENDL marks "recommended"; a December 2023 release is marked "not recommended" | TENDL tar page |
| Tarballs | 2847 ENDF files, 2.9 GB (s30); 600 MeV test files also offered | TENDL tar page |

**Access route: fetch the five per-isotope files individually (~17 MB total, seconds).** Do not download the 2.9 GB tarball. URL pattern verified for Ge074; **[UNVERIFIED]** for Ge070/072/073/076 — issue a HEAD on each before committing a phase to it.

**Critical caveat — do not replace the frozen table with TENDL.** Below 20 MeV, TENDL is a TALYS calculation with its own resonance parameterisation (MF=2 to 61.2 keV for ⁷⁴Ge), *not* the same evaluation as ENDF/B-VIII.0. Substituting would silently discard the resonance-resolved 23,155-point structure the v1.1 phase worked to obtain. **Splice, do not substitute.**

### The other candidates, ranked and dismissed

| Library | Ge coverage above 20 MeV | Verdict |
|---|---|---|
| **TENDL-2023** | Yes — verified to 200 MeV, MF=3 MT=2 and MF=4 present | **Use this** |
| ENDF/B-VIII.0 high-energy sublibrary | **[UNVERIFIED]** whether Ge appears. LANL hosts `/ace/la150n` (LA150, 150 MeV) whose nuclide list I did not read; LA150 is historically a short list (light elements, structural metals, W/Pb) and Ge is unlikely | Check `/ace/la150n` before assuming; do not plan on it |
| JENDL/HE-2007 | 107 nuclides H–Am to 3 GeV. **Germanium inclusion NOT VERIFIED**; the list is dominated by structural/shielding materials | Do not plan on it without checking the JAEA nuclide table |
| JENDL-5 high-energy sublibrary | Extends selected nuclides to 200 MeV or 3 GeV. **[UNVERIFIED]** for Ge | Same |
| IAEA IRDFF-II | A *dosimetry* library: a curated set of reaction-specific activation cross sections for flux monitors. It does **not** provide elastic scattering plus angular distributions, which is what a recoil kernel needs | **Wrong tool.** Do not plan a phase around IRDFF-II for n-Ge elastic. (Confidence MEDIUM — labelled background knowledge, not re-verified this session) |

---

## 2. Reactor Antineutrinos Below 100 keV

### The kinematic target

For Ge, `M c² = 72.63 × 931.494 MeV = 67,644 MeV`. CEvNS maximum recoil `T_max = 2E_ν²/M`:

```
E_nu = 58.7 keV  ->  T_max = 2 (0.0587 MeV)^2 / 67644 MeV = 1.019e-7 MeV = 102 meV   OK
```

Dimensionally consistent and consistent with the stated 100 meV floor. At that `E_ν`, `q ≈ 2E_ν ≈ 117 keV/c` and `qR ≈ 0.003` for `R ≈ 5 fm`, so the Helm form factor is 1 to five digits — **the nuclear-physics side of CEvNS is trivially safe here; all the difficulty is in the flux.**

### CONFLUX — the recommendation

| Item | Value | Status |
|---|---|---|
| Repo | `https://github.com/CNFLUX/conflux` (default branch `master`) | verified via GitHub API |
| Version | **1.1.3**, published 2026-07-16 ("fixed a bug that returns NaN covariance matrix elements") | verified |
| Prior releases | v1.0.1 (2025-04-09, first stable), v1.1 (2025-08-30), v1.1.1, v1.1.2 | verified |
| Licence | MIT, `LLNL-CODE-2003431` | verified |
| Repo size | ~127 MB | verified |
| Install | `git clone`; `pip3 install ./conflux`; `export CONFLUX_DB=<repo>/data` | README |
| Paper | Zhang, Irani, Mendenhall, Rybicki, Hayen, Bowden, Huber, Littlejohn, Bogetic — arXiv:2503.18966, LLNL-JRNL-872396; Comput. Phys. Commun. (ScienceDirect S0010465525003339) | verified |

**osx-arm64 feasibility: GOOD.** The beta-shape physics lives in `conflux/bsg/` as **pure Python** (`CoulombFunctions.py`, `FiniteSize.py`, `Screening.py`, `SpectralFunctions.py`, `Functions.py`, `Constants.py`). The `miniBSG/` tree (C++ with `CMakeLists.txt`) is a separate reference/validation implementation — it is not imported by `conflux.BetaEngine` and does not need to be built. **This is not another openmc/NJOY situation.**

**Bundled databases (no download step):** `data/betaDB/ENSDFbetaDB_250804.xml` (1.36 MB), `ENSDFbetaDB_EC_250804.xml` (1.66 MB), `ENDF_betaDB.xml` (1.27 MB), `betaDB.xml` (1.13 MB); `data/fissionDB/ENDF/nfy-*.xml` and `data/fissionDB/JEFF/nfpy_*.xml` covering U-235/238, Pu-239/241 and many more. Parsers are shipped for re-parsing a newer ENDF/JEFF/ENSDF drop. FYCoM covariance matrices are a separate `CovMatDownloader.py` fetch (CSV, kept out of the repo for size).

**Physics corrections implemented** (read from the paper text): corrected Fermi function `F0 L0`, atomic screening `S`, radiative corrections `R`, shape factor `C_shape`; weak magnetism with `b_Ac = 0.0047`; **all forbidden transitions treated as first-order unique forbidden by default.** That last default is a modelling choice, not a measurement — flag it in any uncertainty budget.

**Extending below 100 keV is a parameter change.** `BetaIstp.__init__` and `BetaEngine.__init__` both accept `xbins` (default `np.arange(0, 20, 0.1)` MeV), and the branch endpoint filter `branchErange` defaults to `[0, 20.]` MeV. Supplying a custom array reaching `1e-5` MeV requires no source edit.

### Is the tens-of-keV region within claimed validity?

**Nobody claims it, because nobody has measured it.** Be blunt with the roadmapper:

1. **No measurement of any kind exists below the IBD threshold (1.8 MeV).** Every reactor-antineutrino dataset in existence is IBD-based. Below 1.8 MeV the spectrum is 100% model; below 100 keV it is model with no adjacent anchor at all.

2. **The kinematic suppression is severe but structurally favourable.** For an allowed branch, `dN/dE_ν ∝ E_ν² p_e E_e F(Z,E_e)` with `E_e = E_0 − E_ν`. As `E_ν → 0` this vanishes as `E_ν²`. At 58.7 keV *every* branch with `E_0 > 58.7 keV` contributes, and each contributes at `E_e ≈ E_0` — i.e. at its own endpoint, where the shape is best constrained by the tabulated `E_0` and branching ratio. **The low-energy tail is therefore closer to a sum rule over the entire beta inventory than to a shape extrapolation.** This argues the sub-100-keV prediction is *more* robust to pandemonium-type ENSDF incompleteness than the 2–8 MeV region is, not less. **This is my derivation from the standard allowed spectrum, not a quoted literature result — a phase must verify it numerically against CONFLUX before relying on it.**

3. **Genuine low-energy-specific effects that may not be well handled at 58.7 keV:** atomic screening dominates when the emitted electron is non-relativistic, which is the case for the lowest-Q branches; and electron-capture branches (handled by a separate `BetaPlusEngine`/EC database) produce *line-like* neutrino emission, not a continuum — for low-Q-value nuclides an EC neutrino line can land in the tens of keV. Do not assume the continuum treatment covers those.

4. **Literature anchors to read before the phase** (both found via search, **abstract-level only, MEDIUM confidence**): "Calculation of low-energy electron antineutrino spectra emitted from nuclear reactors with consideration of fuel burn-up", *J. Nucl. Sci. Technol.*, DOI 10.1080/00223131.2017.1291370 — explicitly identifies nuclides with `Q_β` below 100 keV; and "How to measure the reactor neutrino flux below the inverse beta decay [threshold]", Phys. Rev. D **108**, 033002 (2023). A ~20% spread between the two conventional low-energy calculations ("KOP" and "MHVE") is quoted in secondary sources — **verify against the primary before adopting any number.**

### Everything else in Q2, dismissed with reasons

| Candidate | Verdict |
|---|---|
| **BESTIOLE** (Mueller/Fallot summation engine) | **Not publicly distributed.** No repository, no PyPI, no release. A phase cannot be planned around it. |
| **FISPACT-II** | **Licence-gated** — UKAEA direct licence, or NEA-1890, or RSICC CCC-836. macOS gfortran binaries are shipped, but this is an *inventory/activation* code: nuclide inventories, decay heat, gamma spectra. **It does not emit antineutrino spectra.** Wrong tool plus a licence delay. |
| **ENDF decay sublibrary + ENSDF/DDEP directly** | Technically viable, and *exactly what CONFLUX already implements*, including the beta-shape corrections that are the hard part. Reimplementing is duplicated risk. Use it only as an independent cross-check on a handful of dominant branches. |
| **Huber–Mueller conversion (current v1.0 method)** | Structurally cannot reach below its fit range; the virtual-branch construction is anchored to measured aggregate beta spectra above ~2 MeV. Not extendable to 58.7 keV. |

**Recommendation: CONFLUX summation mode, hybrid with the frozen HM table above 1.8 MeV**, matched at the seam exactly as `data/flux/reactor_flux_v1.0.csv` already does with its `flux_fission_HM` / `flux_fission_summation` split. This preserves the validated high-energy flux and replaces only the low-energy component, which the current header honestly labels `MODEL PLACEHOLDER`.

---

## 3. Low-q / Crystal Response — and the Impulse-Regime Finding

### Read this before planning any phase here

Four numbers decide the whole question.

**(a) Ge's phonon spectrum ends at ~37.8 meV.** Read directly from NCrystal's `Ge_sg227.ncmat`: `vdos_egrid .0037709431308882 .037789664141454` (eV). The VDOS was digitised by T. Kittelmann from Fig. 3 of **G. Nelin and G. Nilsson, "Phonon Density of States in Germanium at 80 K Measured by Neutron Spectrometry", Phys. Rev. B 5, 3151 (1972), DOI 10.1103/PhysRevB.5.3151** — an experimental measurement, which is a strength (no DFT dependence) and a provenance caveat (it is itself a digitised figure; see the irony in Section 4).

**(b) 100 meV is 2.6× that ceiling.** A 100 meV recoil cannot be a single-phonon excitation. The impulse-approximation criterion `E_R >> ħω_max` is already satisfied at the *bottom* of the v2.0 band and increasingly so above it.

**(c) The momentum transfer is tens of Brillouin zones out.** At `T = 100 meV`, `q = sqrt(2MT) = sqrt(2 × 67644 MeV × 1e-10 MeV) = 116.3 keV/c`. With `ħc = 197,327 keV·fm` and `1 fm⁻¹ = 1e5 Å⁻¹`:

```
q     = 116.3 / 197327 fm^-1 = 5.894e-4 fm^-1 = 58.9 A^-1
q_BZ  = 2 pi / a = 2 pi / 5.657 A = 1.11 A^-1
q / q_BZ = 53
```

**(d) The Debye-Waller factor kills coherent/elastic channels across the whole band.** With `θ_D(Ge) ≈ 374 K` and the T→0 Debye result `<u²>_3D = 9ħ²/(4 m k_B θ_D) ≈ 4.0e-3 Å²`, the 1-D projection is `<u²>_1D ≈ 1.3e-3 Å²`. Using `2W = q² <u²>_1D`:

| Recoil `T` | `q` (Å⁻¹) | `2W` | `exp(−2W)` |
|---|---|---|---|
| 21.5 meV | 27.3 | 1.0 | 0.37 |
| **100 meV (v2.0 floor)** | 58.9 | 4.7 | ~1e-2 |
| 1 eV | 186 | 47 | ~1e-20 |
| 20 eV | 833 | 930 | ~0 |

**Consequence, stated bluntly: the crystal-coherent regime (`2W ≲ 1`) lives below ~21 meV recoil, which is BELOW the v2.0 floor of 100 meV. Across the entire 100 meV – 20 eV band the recoiling Ge nucleus behaves as a quasi-free particle in the impulse approximation. Do not plan a phase whose backbone is a coherent-crystal `S(q,ω)` calculation — it would model a regime the milestone never enters.**

Caveats I am obliged to attach:
- The Debye-Waller convention (3-D total `<u²>` vs its 1-D projection) carries a factor of 3 and is a classic error. The table uses the 1-D projection; a phase must recompute using the convention fixed in `GPD/CONVENTIONS.md`.
- The `θ_D`-based `<u²>` is an order-of-magnitude estimate. NCrystal computes `<u²>` from the actual VDOS; use that for any number that reaches the paper.
- `exp(−2W)` is the suppression of the *elastic/coherent* channel, not a claim that nothing happens. The strength moves into the multiphonon / quasi-free continuum — which is exactly the free-nucleus recoil the existing pipeline already models.

**What the crystal codes are therefore actually for:** a bounded, cheap validation phase that (i) computes `2W(q)` and the multiphonon `S(q,ω)` from the real Ge VDOS, (ii) demonstrates the free-nucleus limit is reached by ~100 meV, (iii) quantifies the residual few-percent correction at the very bottom of the band. That *justifies* the 100 meV floor rather than asserting it. One or two plans, not a milestone pillar.

### Tool-by-tool verdict

| Tool | Installable on osx-arm64 with numpy/scipy? | What it gives for Ge | Verdict |
|---|---|---|---|
| **NCrystal 4.4.6** | **YES — native wheel.** `ncrystal_core-4.4.6-py3-none-macosx_11_0_arm64.whl` (2.5 MB) on PyPI; `pip install ncrystal` pulls `ncrystal-core==4.4.6` + `ncrystal-python==4.4.6`. Apache-2.0, `requires_python >=3.8`. Extras: `[plot]`→matplotlib, `[cif]`→ase/gemmi/spglib, `[endf]`→endf-parserpy, `[composer]`→spglib | `Ge_sg227.ncmat` (in the 134-file bundled data library): cubic `a = 5.65735 Å`, spacegroup 227, 8 atom positions, VDOS 3.77–37.79 meV (Nelin & Nilsson 1972). Gives coherent elastic (Bragg), incoherent elastic with Debye-Waller, inelastic via phonon expansion; the `[endf]` extra enables export of `S(α,β)` to ENDF-6 TSL. Also ships `Si_sg227`, `Pb_sg225`, `Cu_sg225`, `Al_sg225`, `C_sg227_Diamond`, `SiO2-alpha`, `PbS`, `PbO` | **PRIMARY.** The only practical route to a Ge `S(q,ω)`, because ENDF/B-VIII.0 has no Ge TSL (verified). Zero build risk. |
| **DarkELF** | **YES — pure Python.** `github.com/tongylin/DarkELF`, `pip install -e .`, `requires-python >=3.9`, deps numpy/scipy/pandas/pyyaml/matplotlib/seaborn/ipykernel | `data/Ge/Ge_pDoS.dat` (15 KB phonon DoS), `Ge_epsphonon_data2K.dat`, `Ge_epsphonon_theory6K.dat`, `Ge_gpaw_withLFE.dat`/`_noLFE.dat` (47 MB each, GPAW DFT energy-loss function), `Ge_mermin.dat` (2.5 MB), `Ge_Fn.dat`, `Ge_Migdal_FAC.dat`, `Ge.yaml` (lattice 5.66 Å, `ombar = 0.02 eV`, `LO = 0.036 eV`, `c_LA = 5.3 km/s`, full isotopic table). Modules `multiphonon_spin_independent.py` (isotropic, arXiv:2205.02250), `multiphonon_anisotropic.py` (arXiv:2411.03433), `phonon.py`. Paper arXiv:2104.12786, Phys. Rev. D 105, 015014 | **SECONDARY.** The closest existing laptop-runnable "phonon DoS → multiphonon structure factor with Debye-Waller" implementation for Ge. **Integration warning:** the public API is parameterised in DM kinematics (`m_DM`, `v ~ 1e-3 c`). Lift the structure-factor internals and re-drive with neutrino/neutron kinematics — calling its rate functions directly yields a dark-matter rate, not ours. Budget for *reading* `multiphonon_spin_independent.py`, not for calling it. Repo ~100 MB. |
| **phonopy** | Installs (pure Python + C extension, arm64 wheels), *but* computes phonons **from DFT forces you must supply** (VASP/QE/ABINIT) | Nothing on its own | **NOT NEEDED.** Both NCrystal and DarkELF already ship a Ge phonon DoS. Reaching for phonopy drags in a DFT code — out of scope. |
| **PhonoDark** | Requires phonopy output + a completed DFT calculation | — | **HEAVY DFT PIPELINE. Do not attempt.** |
| **EXCEED-DM** | Fortran + HDF5 (+MPI), consumes Quantum ESPRESSO output | — | **HEAVY. Do not attempt.** Same build-risk class as openmc/NJOY. |
| **QEdark** | A patch against Quantum ESPRESSO — requires building QE | — | **HEAVY. Do not attempt.** |
| **Materials Project** (`mp-api`) | pip-installable, needs a free API key. Ge is `mp-32`. MP hosts DFPT (ABINIT) phonon band structures for ~1,500 semiconductors/insulators | An independent DFT phonon DoS for Ge | **OPTIONAL CROSS-CHECK ONLY.** Useful to show the Nelin–Nilsson experimental VDOS and a DFT VDOS agree. **[UNVERIFIED]** that `mp-32` specifically carries a phonon DoS entry. |

### Honest gap

**I found no code that computes CEvNS-induced single-phonon production in germanium.** DarkELF's single-phonon machinery is built for a dark-photon mediator with DM kinematics; NCrystal's is built for thermal neutrons. The neutrino–phonon coupling would be original work. Given the impulse-regime arithmetic that is probably the right answer anyway — but "use an existing CEvNS-phonon code" is a fiction and must not appear in the roadmap.

---

## 4. Figure Digitization and Validation Tooling

### Tier 1 (recommended upgrade): vector extraction

arXiv and journal PDFs store plotted curves as **vector paths**, not pixels. The published polyline vertices sit in the content stream at the renderer's coordinate precision. Recovering them removes raster resampling, anti-aliasing, and colour-mask thresholding from the error budget entirely — the residual error becomes purely axis calibration.

| Tool | Version (PyPI, verified) | Licence | Notes |
|---|---|---|---|
| **PyMuPDF** | **1.28.0** | Dual (AGPL / commercial) | `page.get_drawings()` returns path items with coordinates. Native macOS arm64 wheels. **Recommended.** |
| **pdfminer.six** | **20260107** | MIT | Pure Python, lower level; use if the AGPL licence is a concern. |

Methods precedent worth citing: **B. Sun and C. Xiao, "Automated High-Precision Extraction and Forensic Verification of Data-Bearing Vector Figures", arXiv:2606.31345 (submitted 2026-06-30)** — verified to exist; **[UNVERIFIED]** beyond title/authors/date, I did not read it. Its framing (vector figures *encode* rather than approximate the data; axis calibration, not rendering, is the accuracy bottleneck) is exactly the argument for this tier.

### Tier 2 (keep): raster fallback, benchmarked

`scripts/digitize_nucleus_fig1.py` (300 dpi `pdftoppm`, auto-calibrated log axes, colour-masked extraction, 5% reproduction of a published Ge CEvNS curve) stays for genuinely bitmap figures. Benchmark it against:

| Tool | Access | Citation |
|---|---|---|
| **WebPlotDigitizer v5.2** | `https://apps.automeris.io/wpd4/` (browser), Automeris; Ankit Rohatgi, developed since 2011 | Marin & Rohatgi, arXiv:1708.02025 — the standard citable usage paper |
| **`plotdigitizer` 0.3.0** | PyPI, LGPL-3.0-or-later; deps `opencv-python>=4.10`, `numpy>=2.0`, `matplotlib>=3.9.1` | scriptable second opinion; note opencv is a heavier install than the rest of our stack |
| **Engauge Digitizer** | the tool NCrystal's maintainer used for the Ge VDOS | noted for provenance symmetry, not recommended for us |

### Quantified digitization uncertainty — the citable convention

**Wojtyniak et al., "Data Digitizing: Accurate and Precise Data Extraction for Quantitative Systems Pharmacology and Physiologically-Based Pharmacokinetic Modeling", CPT: Pharmacometrics Syst. Pharmacol. 9 (2020), DOI 10.1002/psp4.12511.** It defines the **scaled median symmetric accuracy ζ** as the digitization accuracy metric and reports mean `ζ ≈ 0.99%` under controlled conditions versus `ζ > 5%` for 85% of a real literature sample — i.e. the *tool* is far more accurate than the *practice*. That is a warning about workflow, not software.

**Recommended protocol (self-validating, needs no external tool):**
1. Generate a synthetic figure from a known analytic curve with matplotlib, in the same style/axes/log-scaling as the target publication figure.
2. Render it to PDF (vector) and to 300 dpi PNG (raster).
3. Run both through the full digitizer pipeline.
4. Report ζ separately for the vector and raster paths.
5. Quote that ζ in the provenance header of any digitized CSV.

This cleanly separates *pipeline* error from *disagreement with the published curve* — which the current 5% NUCLEUS Fig-1 agreement conflates.

---

## 5. Published Data Releases: What Exists and What Does Not

### AVAILABLE — real data, no digitization

**CRESST-III event-level data (arXiv:1905.07335v3 ancillary files).** Verified by download; base `https://arxiv.org/src/1905.07335v3/anc/`.

| File | Size | Content (verified by reading it) |
|---|---|---|
| `C3P1_DetA_full.dat` | 9.03 KB | 1,256 event energies in keV, all events surviving data selection. Header: `#Energies (keV) for all events surviving data selection in CRESST-III`. Lowest entries `0.0296`, `0.0299`, `0.0314` keV — **a real event list from 29.6 eV** |
| `C3P1_DetA_AR.dat` | 3.18 KB | 441 acceptance-region event energies |
| `C3P1_DetA_cuteff.dat` | 410 B | 22-point cut-survival efficiency vs energy (`0.0089 keV → 0`, rising through `0.0311 keV → 0.300`) |
| `C3P1_DetA_eff_AR_{O,Ca,W}.dat` | ~124 KB each | per-nucleus acceptance-region efficiency |
| `C3P1_DetA_DataRelease_{SI,SD}.xy` | 446 B / 400 B | published exclusion curves |

Paper: CRESST Collaboration (A. H. Abdelhameed et al.), "Description of CRESST-III Data", arXiv:1905.07335 — written specifically to document this release. **This is the low-energy-excess spectrum as data.** Material caveat: CaWO₄, not Ge, with a 30.1 eV nuclear-recoil threshold — so it constrains the *shape and existence* of a cryogenic LEE, not a Ge-specific normalisation.

**Dark Matter Data Center (ORIGINS Cluster, Munich):** `https://www.origins-cluster.de/odsl/dark-matter-data-center/available-datasets` — hosts CRESST-II/III, XENON, ANAIS, COSINE-100 with download and in-browser visualisation. **It does not host NUCLEUS, CONUS, or RICOCHET** (the collaboration list is exactly those four). The dataset inventory loads dynamically and could not be enumerated server-side; open it in a browser.

**COHERENT Zenodo data releases** (Zenodo API, title-exact query returned exactly two records):
- `10.5281/zenodo.1228631`, 2018-04-25 — first observation of CEvNS (CsI)
- `10.5281/zenodo.3903810`, 2020-06-22 — first detection of CEvNS on argon

Accelerator, not reactor, and not Ge — but these are the field's standard CEvNS validation datasets, each shipping a technical note plus data-treatment scripts. **A COHERENT *germanium* data release was NOT found** (their Ge result is PRL 134, 231801). Absence of a Zenodo record under that exact title is not proof it does not exist — mark as "not found", and check the paper's supplemental material.

**Goupy PhD thesis — FULL TEXT PUBLIC.**
- PDF: `https://theses.hal.science/tel-05298505/document` — **verified HTTP 200, `content-type: application/pdf`, 73,700,930 B (73.7 MB)**
- Title: "Background mitigation strategy for the detection of coherent elastic scattering of reactor antineutrinos on nuclei with the NUCLEUS experiment"
- Chloé Goupy, Université Paris Cité, defended 2024-10-08, NNT `2024UNIP7170`, supervisor Thierry Lasserre, laboratory APC Paris
- DOI: `10.70675/574d6e17z1b68z4676zbde9z255450e1c649`

This is ref. 48 of the NUCLEUS background paper and the single best public source for VNS background detail. It is still figures and tables rather than machine-readable data — but a thesis typically tabulates what a letter only plots, so **read it before digitizing anything from arXiv:2509.03559.**

### NOT AVAILABLE — verified individually, do not plan a phase around these

I fetched each arXiv abstract page and checked for an "Ancillary files" block. **All returned none:**

| Paper | arXiv | Ancillary files |
|---|---|---|
| NUCLEUS, "Particle background characterization and prediction for the NUCLEUS reactor CEνNS experiment" | 2509.03559 | **NONE** |
| NUCLEUS, "Prospect of the NUCLEUS Experiment at Chooz for CEνNS and New Physics Searches" | 2603.24450 | **NONE** |
| NUCLEUS, "Commissioning of the NUCLEUS Experiment at TUM" | 2508.02488 | **NONE** |
| CONUS+, "Direct observation of coherent elastic antineutrino–nucleus scattering" (Nature 643, 1229 (2025)) | 2501.05206 | **NONE** |
| CONUS, "Full background decomposition of the CONUS experiment" | 2112.09585 | **NONE** |
| CONUS+, "Background characterization of the CONUS+ experimental location" | 2412.13707 | **NONE** |
| CONUS+, "Sub-keV energy calibration of CONUS+ via ⁷¹Ge M-shell neutron activation" | 2604.25748 | **NONE** |

The CONUS+ Nature Data Availability Statement states the ROOT-based analysis code is available from `conus.eb@mpi-hd.mpg.de` upon reasonable request — **code on request, not data deposited.** This matches the NUCLEUS situation the orchestrator described.

**RICOCHET:** no public data release found. The collaboration is in its initial science phase (installation completed 2024, science running from July 2025); commissioning results are published as papers (mini-CryoCube characterization, Phys. Rev. D, 2025) with no dataset. **Treat "obtain RICOCHET data" as not currently possible.**

**HEPData: I could not query it.** `hepdata.net` returned HTTP 403 to WebFetch and a Cloudflare interstitial to `curl` for both HTML and `?format=json`. **[UNVERIFIED]** whether any CONUS/NUCLEUS/RICOCHET/COHERENT record exists there. This is a genuine hole: check `hepdata.net` manually in a browser before concluding a spectrum must be digitized.

### Practical consequence for the roadmap

Any v2.0 phase needing the NUCLEUS VNS background *spectrum* must be planned as **digitization of published figures plus the Goupy thesis**, with the Section 4 ζ protocol applied and the uncertainty carried explicitly — **not** as "download the dataset". Planning otherwise builds a phase on a fiction.

---

## Numerical Algorithms

| Algorithm | Problem | Convergence | Cost per Step | Memory | Key Reference |
|---|---|---|---|---|---|
| HTTP-range ZIP central-directory read + inflate | Pull individual ACE members from a 7–9.5 GB remote archive | Exact (stdlib `zipfile`) | O(members in CD) + O(member size) | O(chunk) = 1 MB | existing `src/nuclear/fetch_ace_lib80x.py` |
| ENDF-6 TAB1/TAB2 interpolation-law evaluation | σ(E), dσ/dΩ_cm from TENDL/ENDF files | Exact under the file's own INT laws | O(N_pts) | O(N_pts) | ENDF-6 Formats Manual |
| Two-body elastic recoil kinematics + angular Jacobian | dσ/dE_R per isotope from σ(E_n) and CM angular distribution | Exact analytic Jacobian | O(N_En × N_ang) | O(N_En × N_ER) | reused from v1.1 |
| Cross-library splice with continuity reporting | Join ENDF/B-VIII.0 (≤20 MeV) to TENDL-2023 (>20 MeV) | The discontinuity must be measured, not assumed zero | O(N) | O(N) | this document, Validation |
| Beta/neutrino spectrum per branch (`conflux.bsg`) | `dN/dE_ν ∝ E_ν² p_e E_e F0 L0 S R C_shape` | Analytic; accuracy set by the correction terms | O(N_bins) per branch | O(N_bins) | Zhang et al. arXiv:2503.18966 |
| Fission-product summation | Σ over ~10³ isotopes × ~10⁴ branches, FPY-weighted | Linear sum; "convergence" is branch-inventory completeness, **not** a numerical criterion | O(N_branch × N_bins) | O(N_bins) | CONFLUX `SumEngine` |
| Debye-Waller from VDOS | `2W(q) = q² <u²>`, `<u²>` from ∫ g(ω)/ω coth(ħω/2kT) dω | Exact quadrature over the VDOS grid | O(N_ω) | O(N_ω) | NCrystal; Nelin & Nilsson (1972) |
| Multiphonon expansion of S(q,ω) | n-phonon convolution of the VDOS with the DW prefactor | Terminate when order n+1 contributes <1% of ∫S dω | O(n_max × N_ω log N_ω) via FFT convolution | O(N_ω) | DarkELF `multiphonon_spin_independent.py`, arXiv:2205.02250 |
| PDF vector-path extraction + log-axis affine calibration | Recover published curve coordinates exactly | Exact for vector; calibration-limited | O(N_paths) | O(N_vertices) | PyMuPDF; arXiv:2606.31345 |
| Count-conserving rebin to shared grid | Map any dR/dE onto the extended `shared_energy_grid()` | Exact under integral preservation | O(N_bins) | O(N_bins) | existing v1.0 fold utilities |

### Convergence Properties

- **Cross-library splice at 20 MeV.** Criterion: the fractional step `|σ_TENDL − σ_ENDF|/σ_ENDF` at 20 MeV must be *reported*, not smoothed away. Measured for ⁷⁴Ge: **+1.35%** (see Validation). Failure mode: blending over a window hides an evaluation disagreement inside a "smooth" curve. Prefer a hard seam with a documented step, matching the existing flux-seam convention.
- **CONFLUX summation.** There is **no numerical convergence criterion that certifies physical correctness** — the sum is a finite sum over a database. Meaningful checks: (i) total ν̄ per fission reproduces the accepted ~6/fission (the frozen table gives `grand total = 6.477`); (ii) the 1.8–8 MeV integral reproduces the frozen HM result within its band; (iii) bin-count independence — halving the sub-100-keV bin width changes the 58–100 keV integral by <1%. Failure mode: a uniformly fine grid over 0–20 MeV multiplies runtime linearly in `N_bins` for no gain above 1 MeV. **Use a two-region `xbins`: fine below 1 MeV, coarse above.**
- **Multiphonon expansion.** Criterion: adding the next phonon order changes `∫S(q,ω)dω` by <1%, **and** the result converges onto the free-nucleus (impulse) limit `S → δ(ω − q²/2M)` as q grows. That limit is the physics check that matters; if it is not reproduced, the implementation is wrong. Failure mode: at `2W >> 1` the expansion needs many orders and is the wrong representation — switch to the impulse approximation explicitly rather than pushing the expansion.
- **Debye-Waller `<u²>`.** Criterion: the VDOS integral and the Debye-model estimate (`~4.0e-3 Å²` 3-D at T→0) agree within a factor ~1.5. Larger disagreement usually means a 3-D-vs-1-D factor-of-3 convention error, not physics.
- **Shared-grid rebin.** Exact count conservation: `sum(counts_out) == sum(counts_in)` to machine tolerance. Reuse the existing closure-test pattern.

---

## Software Ecosystem

### Primary Tools

| Tool | Version | Purpose | Licence | osx-arm64 | Maturity |
|---|---|---|---|---|---|
| numpy / scipy / matplotlib | existing | fold, interpolation, quadrature, plotting | BSD | already installed | stable |
| `endf` (Python ENDF-6/ACE reader) | 0.1.12 (already in use) | read ACE members and TENDL ENDF-6 files | MIT | pure Python — **already proven in v1.1** | stable |
| **LANL Lib80x** | ENDF/B-VIII.0 basis, 2018-06-29 | pre-processed ACE for all shield nuclides | public | n/a (data) | established |
| **LANL ENDF80SaB2** | ENDF/B-VIII.0 TSL, 2018-07-26 | `h-poly` bound-hydrogen TSL | public | n/a (data) | established (**use SaB2, not SaB**) |
| **TENDL-2023** | Aug-2024 neutron release | n-Ge elastic + angular, 20–200 MeV | public | n/a (data) | mature system; **calculational** below 20 MeV |
| **CONFLUX** | **1.1.3** (2026-07-16) | summation reactor ν̄ spectrum below 1.8 MeV | MIT | **pure Python — YES** | stable since v1.0.1 (Apr-2025); small user base (8 GitHub stars) |
| **NCrystal** | **4.4.6** | Ge crystal structure, VDOS, Debye-Waller, S(q,ω)/S(α,β) | Apache-2.0 | **native arm64 wheel — YES** | mature, widely used in neutron instrumentation |
| **DarkELF** | git HEAD (no tagged release) | Ge phonon DoS, multiphonon structure factor | see repo | **pure Python — YES** | research code; API shaped by DM kinematics |
| **PyMuPDF** | 1.28.0 | vector figure extraction | AGPL / commercial | wheels — YES | stable |

### Supporting Tools

| Tool | Version | Purpose | When Needed |
|---|---|---|---|
| `endf-parserpy` | ≥0.14.3 (`pip install ncrystal[endf]`) | export NCrystal S(α,β) to ENDF-6 TSL | only if a TSL file is a deliverable |
| `pdfminer.six` | 20260107 | MIT-licensed vector extraction | if the PyMuPDF AGPL licence is a problem |
| `plotdigitizer` | 0.3.0 | scriptable raster second opinion | benchmarking the home-grown digitizer |
| WebPlotDigitizer | v5.2 (browser) | manual raster digitization reference | ζ benchmarking; citable via arXiv:1708.02025 |
| `mp-api` | current | Materials Project DFPT Ge phonons | optional VDOS cross-check only |
| LANL Lib81 | ENDF/B-VIII.1, 2025-09-11 | library-version sensitivity variant | only for an explicit uncertainty study |

### Explicitly rejected

`openmc` (unbuildable here, and unnecessary — `endf` reads ACE), `NJOY` (unbuildable, and Lib80x/SaB2 are its output), `FISPACT-II` (licence-gated + wrong physics output), `phonopy` / `PhonoDark` / `EXCEED-DM` / `QEdark` (all require a DFT calculation we are not doing), `Geant4` / `G4CMP` / `MCNP` / `FLUKA` (out of scope by decision).

---

## Data Flow

```
Lib80x.zip (remote, 7.05 GB)             TENDL-2023 per-nuclide URLs
ENDF80SaB2.zip (remote, 2.57 GB)         (5 x ~3.4 MB, direct download)
        |  HTTPRangeFile + zipfile                |
        v                                         v
   ACE members (Pb,B,Li,C,H,Cu,Si,Ge)      n-Ge0NN.tendl (1e-5 eV - 200 MeV)
        |  endf 0.1.12                            |  endf 0.1.12
        v                                         v
   sigma(E), angular dist per nuclide  ---> SPLICE at 20 MeV (step measured, not hidden)
        |
        +--> shield attenuation / source-term model --> n flux at wafer
        |
        v
   two-body recoil kernel dsigma/dE_R --> dR/dE_R (neutron NR channel)

CONFLUX 1.1.3 (local, pure Python)
   ENSDF/ENDF beta DB + FPY DB
        |  BetaEngine(xbins = two-region grid down to 1e-5 MeV)
        v
   per-branch nu spectra --> SumEngine --> Phi(E_nu) down to ~10 keV
        |  seam-match at 1.8 MeV to frozen reactor_flux_v1.0.csv
        v
   reactor_flux_v2.0.csv --> existing cevns.py fold --> dR/dT down to 100 meV

NCrystal 4.4.6 (Ge_sg227.ncmat)  +  DarkELF (Ge_pDoS.dat)
        |
        v
   <u^2>, 2W(q), multiphonon S(q,omega)
        |
        v
   JUSTIFICATION artifact: free-nucleus/impulse limit reached by ~100 meV
   (a correction factor near the band floor, NOT a replacement kernel)

published PDFs (NUCLEUS papers, Goupy thesis)
        |  PyMuPDF vector paths   (fallback: existing 300 dpi raster pipeline)
        v
   digitized CSV + zeta uncertainty from a synthetic round-trip

ALL channels -> extended shared_energy_grid() -> existing R(E_rec|E_dep) fold -> reconstructed spectra
```

---

## Computation Order and Dependencies

| Step | Depends On | Produces | Can Parallelize? |
|---|---|---|---|
| 1. Extend `shared_energy_grid()` to 0.1 eV | conventions decision (see Integration) | ~744-bin grid | n/a — do first, everything binds to it |
| 2. Fetch shield ACE from Lib80x + ENDF80SaB2 | existing `HTTPRangeFile` | frozen per-nuclide σ tables | yes |
| 3. Fetch TENDL-2023 Ge, splice at 20 MeV | frozen `endf_nGe_elastic_v1.1.csv` | `endf_nGe_elastic_v2.0.csv` to 200 MeV | yes |
| 4. CONFLUX sub-100-keV flux, seam-match at 1.8 MeV | frozen `reactor_flux_v1.0.csv`; step 1 | `reactor_flux_v2.0.csv` | yes |
| 5. Ge VDOS → `<u²>`, `2W(q)`, multiphonon S | NCrystal + DarkELF install | impulse-limit justification + floor correction | yes |
| 6. Digitize NUCLEUS / Goupy background spectra | PyMuPDF; Goupy PDF | digitized CSVs + ζ | yes |
| 7. Shield transport / attenuation model | steps 1, 2; **shield geometry input (see Gaps)** | n flux at wafer | no — needs 2 |
| 8. CEvNS fold to 100 meV | steps 1, 4; existing `cevns.py` | dR/dT to 100 meV | no — needs 4 |
| 9. Fold everything through `R(E_rec\|E_dep)` | steps 1, 7, 8; existing response matrices | v2.0 reconstructed spectra | no — terminal |

Steps 2–6 are five genuinely independent fetch/compute tracks. Step 1 gates all of them and should be a single small plan done first.

---

## Resource Estimates

| Computation | Time | Memory | Storage | Hardware |
|---|---|---|---|---|
| Lib80x range-fetch, ~15 shield nuclides | minutes (central directory + ~1 MB/member) | <100 MB | ~20 MB of cached ACE | laptop + network |
| ENDF80SaB2 range-fetch, `h-poly` | ~1 min | <100 MB | few MB | laptop + network |
| TENDL-2023 Ge, 5 isotopes | seconds; 5 × 3.36 MB ≈ 17 MB | trivial | 17 MB | laptop + network |
| CONFLUX install + DB | minutes; repo ~127 MB | — | ~130 MB | laptop |
| CONFLUX summation run | **UNMEASURED — must be measured in-phase.** Cost is O(N_branch × N_bins); the default grid is 200 bins over 0–20 MeV, while a uniform 1-keV grid to 20 MeV would be 20,000 bins = 100× the default. **This is why the two-region grid is not optional.** | likely <2 GB | outputs <10 MB | laptop |
| NCrystal install | seconds (2.5 MB wheel) | trivial | ~10 MB | laptop |
| DarkELF install | ~1 min | — | ~100 MB (two 47 MB ELF tables) | laptop |
| Multiphonon S(q,ω) on a (q,ω) mesh | **UNMEASURED**; FFT-convolution based, expected seconds–minutes per q | <1 GB | small | laptop |
| Extended response matrix | 744² float64 ≈ 4.4 MB per design — negligible growth from 584² | <100 MB | tens of MB `.npz` | laptop |

Nothing here needs a cluster. **The two unmeasured runtimes (CONFLUX on a fine grid; multiphonon S) are the only schedule risks, and each should get a timing spike early in its phase rather than a guess in the roadmap.**

---

## Integration with Existing Code

**Input formats.** Frozen CSVs with the provenance-header convention already established by `data/endf_nGe_elastic_v1.1.csv` and `data/flux/reactor_flux_v1.0.csv`. Every new table must carry: `source`, `retrieval` URL + date, MAT/ZAID or database version, reaction MT, reader + version, upstream-processing statement, SHA-256 of the fetched member, `git_sha`, `generated_utc`, and a **validation block computed at generation time, not memorized** — the v1.1 header is the model and should be copied structurally.

**Output formats.** `dR/dE_dep` on the extended `shared_energy_grid()`, folded through the existing `R(E_rec|E_dep)` and dead-time censoring utilities. Unchanged.

**Interface points and new modules.**
- `src/nuclear/fetch_ace_lib80x.py` → generalise to `fetch_ace.py` with a nuclide→ZAID table and an archive selector (`Lib80x` | `ENDF80SaB2` | `Lib81`). `HTTPRangeFile` needs no change — I verified `Accept-Ranges: bytes` on all three archives.
- `src/nuclear/fetch_tendl.py` — new, trivial (direct GET, no archive).
- `src/nuclear/splice.py` — new; owns the 20 MeV seam and *records* the discontinuity.
- `src/flux/summation_conflux.py` — new; wraps CONFLUX, mirrors the structure of the existing `summation_ncapture.py`, writes `reactor_flux_v2.0.csv` in the same split-uncertainty header style.
- `src/crystal/` — new package; thin wrappers over NCrystal and DarkELF. Keep them thin: their job is to emit a frozen `ge_vdos_v2.0.csv` and `debye_waller_v2.0.csv`, not to become a phonon framework.
- `scripts/digitize_*.py` — add a vector path alongside the raster path; share the axis-calibration code.

**Two integration conflicts the roadmapper must resolve, not inherit silently:**

1. **Grid floor vs. plotting floor.** `shared_energy_grid()` currently starts at 10.14 eV; v2.0 requires 0.1 eV. At 80 bins/decade, 0.1 eV → 197 MeV spans `log10(1.97e9) = 9.29` decades → **~744 bins** (up from 584). But the project carries a standing instruction never to *display* QPD spectra below 10 eV (grid-floor / binding-artifact territory). **These are not automatically compatible** — v2.0 deliberately enters the region that rule was written to hide. The roadmap must state explicitly whether the display floor is (a) lifted for v2.0 because the Section 3 physics justification now exists, or (b) retained, with sub-10-eV results computed but shown only in a dedicated, caveated figure. Do not let a plan silently violate either.

2. **Library-version homogeneity.** The frozen Ge table is ENDF/B-VIII.0. If shield materials come from Lib80x (VIII.0) the chain is homogeneous. If anyone reaches for Lib81, the whole chain must move together, or the provenance header must say loudly that it is mixed.

---

## Validation Strategy

| Result | Validation Method | Benchmark | Source |
|---|---|---|---|
| TENDL/ENDF splice at 20 MeV | Evaluate both at exactly 2.0e7 eV; report the step | **Measured this session for ⁷⁴Ge: ENDF/B-VIII.0 = 1.247550 b (from `data/endf/nGe_elastic_per_isotope.csv`), TENDL-2023 = 1.264380 b (from `n-Ge074.tendl`) → +1.35%.** Repeat for the other four isotopes | frozen table + downloaded TENDL file |
| Shield ACE fetch integrity | SHA-256 of each fetched member recorded in the header | reproducible across re-fetch, exactly as the v1.1 `ace_sha256_head` fields do | existing convention |
| B-10 absorber cross section | 10B(n,α) MT=107 at 0.0253 eV | ≈3840 b (standard thermal value) — **verify against the file, do not hardcode**; B-10 is an evaluated standard so agreement should be sub-1% | Lib80x |
| Bound-H moderation | Compare `h-poly` TSL to free-gas H-1 below 1 eV | the two must differ substantially; if they agree, the TSL is not being applied | ENDF80SaB2 |
| CONFLUX total ν̄ yield | ∫ over all E of the summation spectrum | ~6 ν̄/fission; the frozen table gives `grand total = 6.477` | `reactor_flux_v1.0.csv` header |
| CONFLUX vs frozen HM | ∫ 1.8–8 MeV, CONFLUX conversion mode vs frozen HM | agree within the frozen table's 2–5% band above 2 MeV | `reactor_flux_v1.0.csv` |
| Low-E flux shape | Check that `Φ(E_ν) ∝ E_ν²` emerges as `E_ν → 0` | the `E_ν²` kinematic factor is model-independent; if CONFLUX does not show it, the grid or branch filter is wrong | this document, §2 |
| CEvNS endpoint | `T_max = 2E_ν²/M` at `E_ν = 58.7 keV` | 102 meV | computed above |
| Ge VDOS | NCrystal VDOS maximum energy | 37.79 meV (`vdos_egrid` upper bound); cross-check the DarkELF `Ge_pDoS.dat` cutoff | `Ge_sg227.ncmat` |
| Ge `<u²>` | NCrystal VDOS integral vs Debye model at T→0 | Debye estimate `<u²>_3D ≈ 4.0e-3 Å²` for `θ_D = 374 K`; agree within ~1.5× | this document, §3 |
| Multiphonon S(q,ω) | Free-nucleus limit at large q | `S → δ(ω − q²/2M)`; the first moment must equal `q²/2M` exactly (f-sum rule) | standard |
| Digitizer | Synthetic round-trip: known curve → PDF/PNG → digitize → ζ | vector path ζ should be well below raster path ζ; report both | Wojtyniak et al., DOI 10.1002/psp4.12511 |
| CRESST-III data ingest | Reproduce the published event count and threshold | 1,256 events in `C3P1_DetA_full.dat`, 441 in `C3P1_DetA_AR.dat`, minimum energy 0.0296 keV | verified by reading the files |
| Existing anchors | All 24 v1.0/v1.1 anchors must still reproduce after the grid extension | unchanged | `notebooks/paper_calculations.ipynb` |

---

## Known Gaps and Required Inputs

1. **The NUCLEUS shield geometry and material composition are not in this document.** I identified where the *data* lives (Lib80x, ENDF80SaB2) but not what thicknesses of what materials to transport through. That must be read out of arXiv:2509.03559 and the Goupy thesis and is a prerequisite for step 7. **Do not let a plan assume a shield stack.**
2. **HEPData was unreachable** (Cloudflare 403 to WebFetch and curl). A manual browser check is required before concluding any spectrum must be digitized.
3. **Ge above 20 MeV in the ENDF/B-VIII.0 high-energy sublibrary, JENDL/HE-2007, and JENDL-5 is unverified.** TENDL-2023 is verified and sufficient; the others are listed only so nobody plans a phase on an unchecked assumption.
4. **TENDL per-nuclide URL pattern verified only for Ge-074.** HEAD the other four before relying on it.
5. **No CEvNS-to-phonon code exists** that I could find. If the roadmap wants single-phonon CEvNS in Ge, that is original implementation work, not tool integration — and the §3 impulse-regime arithmetic argues it is not needed at a 100 meV floor.
6. **CONFLUX runtime on a fine sub-MeV grid is unmeasured.** Timing spike required.
7. **`Ge_sg227.ncmat`'s VDOS is itself a digitised figure** (Nelin & Nilsson 1972, Fig. 3, via Engauge). Experimental origin is preferable to DFT, but it carries an unquantified digitization uncertainty — the same class §4 asks us to quantify for our own work. Cross-check against DarkELF's `Ge_pDoS.dat` (independent origin) before quoting any VDOS-derived number.

---

## Sources

**Nuclear data**
- LANL ACE library index — `https://nucleardata.lanl.gov/ace/` (live; enumerates lib80x, lib81, endf80sab2, endf81sab, la150n)
- Lib80x — `https://nucleardata.lanl.gov/ace/lib80x/`; archive `https://nucleardata.lanl.gov/lib/Lib80x.zip` (7.05 GB, byte ranges) — Conlin, Haeck, Neudecker, Parsons, White, LA-UR-18-24034 (2018)
- ENDF80SaB2 — `https://nucleardata.lanl.gov/ace/endf80sab2`; archive `https://nucleardata.lanl.gov/lib/ENDF80SaB2.zip` (2.57 GB); 34 TSL materials; released 2018-07-26; corrected version of ENDF80SaB
- Lib81 — `https://nucleardata.lanl.gov/ace/lib81`; archive `https://nucleardata.lanl.gov/lib/Lib81.zip` (9.47 GB); released 2025-09-11; ENDF/B-VIII.1 basis (NNDC release 2024-08-30)
- ENDF/B-VIII.0 — Brown et al., Nucl. Data Sheets 148 (2018); IAEA mirror `https://www-nds.iaea.org/public/download-endf/ENDF-B-VIII.0/n/`
- ENDF/B-VIII.1 overview — arXiv:2511.03564
- TENDL-2023 — `https://tendl.imperial.ac.uk/tendl_2023/tendl2023.html`; tar index `.../tar.html`; per-nuclide `https://tendl.imperial.ac.uk/tendl_2023/neutron_file/Ge/Ge074/lib/endf/n-Ge074.tendl` (verified: 3.36 MB, 1e-5 eV – 200 MeV, MAT 3237, Koning & Rochman, EVAL-DEC23)
- JENDL/HE-2007 — 107 nuclides H–Am to 3 GeV; Ge coverage **unverified**

**Reactor antineutrino flux**
- CONFLUX — `https://github.com/CNFLUX/conflux`, v1.1.3 (2026-07-16), MIT, LLNL-CODE-2003431
- Zhang, Irani, Mendenhall, Rybicki, Hayen, Bowden, Huber, Littlejohn, Bogetic, "CONFLUX: A Standardized Framework to Calculate Reactor Antineutrino Flux", arXiv:2503.18966; Comput. Phys. Commun. (ScienceDirect S0010465525003339); LLNL-JRNL-872396
- "A comprehensive revision of the summation method for the prediction of reactor antineutrino fluxes and spectra", arXiv:2304.14992
- "Calculation of low-energy electron antineutrino spectra emitted from nuclear reactors with consideration of fuel burn-up", J. Nucl. Sci. Technol., DOI 10.1080/00223131.2017.1291370 (**abstract-level only**)
- "How to measure the reactor neutrino flux below the inverse beta decay [threshold]", Phys. Rev. D 108, 033002 (2023) (**abstract-level only**)
- FISPACT-II — `https://fispact.ukaea.uk/`; NEA-1890; RSICC CCC-836; UKAEA-R(18)001

**Crystal / phonon**
- NCrystal — `https://github.com/mctools/ncrystal`; PyPI `ncrystal` 4.4.6 / `ncrystal-core` 4.4.6 (macosx_11_0_arm64 wheel); Apache-2.0; data file `Ge_sg227.ncmat`
- G. Nelin and G. Nilsson, "Phonon Density of States in Germanium at 80 K Measured by Neutron Spectrometry", Phys. Rev. B 5, 3151 (1972), DOI 10.1103/PhysRevB.5.3151 — the source of the Ge VDOS
- NJOY+NCrystal (S(α,β) generation) — Nucl. Instrum. Methods A, ScienceDirect S0168900221010755
- DarkELF — `https://github.com/tongylin/DarkELF`; Knapen, Kozaczuk, Lin et al., arXiv:2104.12786, Phys. Rev. D 105, 015014
- Multiphonon formalism — arXiv:2205.02250 (isotropic), arXiv:2411.03433 (anisotropic / daily modulation), arXiv:2506.11191 (spin-dependent)
- Togo & Tanaka, phonopy — J. Phys. Soc. Jpn. 92, 012001 (2023); PhononDB `http://phonondb.mtl.kyoto-u.ac.jp/`

**Digitization**
- Rohatgi, WebPlotDigitizer v5.2 — `https://apps.automeris.io/wpd4/`; Marin & Rohatgi, arXiv:1708.02025
- Wojtyniak et al., CPT: Pharmacometrics Syst. Pharmacol. 9 (2020), DOI 10.1002/psp4.12511 — scaled median symmetric accuracy ζ
- Sun & Xiao, arXiv:2606.31345 (2026-06-30) — vector-figure extraction and verification (**title/authors/date verified only**)
- PyMuPDF 1.28.0; pdfminer.six 20260107; plotdigitizer 0.3.0 (all PyPI-verified)

**Experimental data**
- CRESST Collaboration, "Description of CRESST-III Data", arXiv:1905.07335 — ancillary files at `https://arxiv.org/src/1905.07335v3/anc/` (verified; event-level; 29.6 eV minimum)
- Dark Matter Data Center, ORIGINS Cluster — `https://www.origins-cluster.de/odsl/dark-matter-data-center/available-datasets` (CRESST, XENON, ANAIS, COSINE-100 only)
- COHERENT data releases — Zenodo DOI 10.5281/zenodo.1228631 (CsI, 2018) and 10.5281/zenodo.3903810 (LAr, 2020)
- C. Goupy, PhD thesis, Université Paris Cité, 2024, NNT 2024UNIP7170, DOI 10.70675/574d6e17z1b68z4676zbde9z255450e1c649 — full text `https://theses.hal.science/tel-05298505/document` (73.7 MB, verified)
- NUCLEUS — arXiv:2509.03559 (VNS background), arXiv:2603.24450 (Chooz prospects), arXiv:2508.02488 (TUM commissioning), arXiv:1905.10258 (Chooz CEvNS) — **no ancillary files on any**
- CONUS / CONUS+ — arXiv:2501.05206 (Nature 643, 1229 (2025)), arXiv:2112.09585, arXiv:2412.13707, arXiv:2604.25748 — **no ancillary files on any**; Nature DAS: analysis code on request from `conus.eb@mpi-hd.mpg.de`
- RICOCHET — `https://ricochet-experiment.github.io/`; mini-CryoCube characterization, Phys. Rev. D (2025) — **no public data release found**
