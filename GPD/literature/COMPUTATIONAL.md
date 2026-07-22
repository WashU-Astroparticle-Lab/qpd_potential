# Computational Approaches: v1.1 Neutron-NR & Radiogenic In-Band Backgrounds (QPD-Ge)

**Surveyed:** 2026-07-21
**Domain:** Low-background nuclear/particle physics — neutron elastic recoils and detector radioactivity for a ~110 g surface Ge wafer
**Confidence:** MEDIUM-HIGH (tools/versions and Python access paths verified against GitHub/docs/papers; a few exact patch versions and the 238U SF Watt parameters carry documented spread)

> **Milestone note:** This is the **v1.1** computational survey. It supersedes the v1.0 `COMPUTATIONAL.md` (Reactor-CEvNS + cosmic-muon reconstructed spectra), which remains in git history. The v1.0 pipeline is **reused, not re-researched** (see reuse constraint below).

## Scope and Reuse Constraint

v1.1 adds neutron-nuclear-recoil (NR) and detector-radioactivity in-band backgrounds to the existing forward model. The v1.0 stack is reused verbatim: Python (numpy/scipy/matplotlib); `shared_energy_grid()` (~584 log bins, ~0.01 keV to 197 MeV); Monte-Carlo response matrices `R(E_rec|E_dep)` stored per trapping design in `.npz`; non-paralyzable dead-time censoring (~25 kHz, 40 us resolving time); count-conserving fold utilities (`src/flux/assemble_spectrum.py`, `src/qpd_potential/deposited_spectra.py`, `response.py`, `response_matrix.py`); CSV tables with provenance headers (`data/flux/reactor_flux_v1.0.csv`, `data/gamma_lines.csv`, `data/ge_xcom_mu.csv`).

**Every v1.1 deposited-energy spectrum must be produced on the same `shared_energy_grid()` and folded through the same `R` matrices** so it is directly comparable to the v1.0 CEvNS / muon / Compton spectra.

**HARD CONSTRAINT:** no G4CMP. Prefer nuclear-data-driven analytic/MC over heavy transport codes (Geant4, MCNP, FLUKA). The recommendations honor this: physics is extracted from evaluated nuclear data via lightweight Python parsers, and the wafer response is computed by an **analytic thin-target single-scatter fold**, not a transport simulation.

## Recommended Stack

**Neutron-NR channel.** Do NOT run a transport code for the wafer. A 2 mm Ge wafer is optically thin to fast neutrons: with n_Ge = 4.4e22 cm^-3 (rho = 5.323 g/cm^3, A = 72.6) and fast-neutron total cross section sigma_tot ~ 3-5 b, the macroscopic Sigma ~ 0.18 cm^-1 gives a mean free path ~ 5-6 cm >> 0.2 cm, so P(interaction) ~ Sigma*t ~ 3-4% and multiple scattering is negligible (<0.1%). The correct method is a **thin-target single-scatter analytic fold**: extract elastic cross sections sigma(E_n) (ENDF MF=3, MT=2) and CM angular distributions (ENDF MF=4, MT=2) per Ge isotope with **`openmc.data.IncidentNeutron.from_endf`**, convert each angular distribution to a recoil-energy kernel dsigma/dE_R via two-body kinematics, and integrate over the incident neutron flux. Use **`openmc.data`** as the ENDF reader (pure-Python, no NJOY needed for File 3/File 4); keep **NJOY2016 / ENDFtk / sandy** as fallbacks for resonance reconstruction or File-4 edge cases. Ge NR quenching is a physics input handled by the methods/roadmap layer, not by these tools.

**Radiogenic channel.** Build a decay line/continuum source from evaluated decay data with **`radioactivedecay`** (ICRP-107 default; ENSDF dataset optional) plus curated ENSDF/DDEP line energies and per-decay intensities (the v1.0 `data/gamma_lines.csv` convention already does this for the environmental Compton channel and should be extended, not replaced). Photon self-shielding/attenuation in the thin wafer uses **`xraylib`** (Python bindings) or the frozen NIST XCOM points already in `data/ge_xcom_mu.csv`. Beta and internal-conversion/Auger/X-ray spectra (3H endpoint 18.6 keV, 68Ga beta+, 65Zn/68Ge EC with K/L X-rays) are the physically important in-band deposits and are built from tabulated endpoints/branching, then binned onto the shared grid. Cosmogenic activation yields (surface exposure) come from published tabulations (Saldanha 2020, CDMSlite, EDELWEISS-III) with **ACTIVIA/COSMO** only as a cross-check — do not stand up a Geant4/CRY chain.

Both channels terminate identically: produce `dR/dE_dep` on `shared_energy_grid()` as a provenance-headed CSV, then fold through the existing `R(E_rec|E_dep)` and censoring utilities.

## Numerical Algorithms

| Algorithm | Problem | Convergence | Cost per Step | Memory | Key Reference |
| --------- | ------- | ----------- | ------------- | ------ | ------------- |
| Two-body elastic recoil kinematics + angular-dist transform | Convert sigma(E_n), dsigma/dOmega_cm to dsigma/dE_R per isotope | Exact (analytic Jacobian); accuracy set by ENDF interpolation | O(N_En x N_ang) | O(N_En x N_ER) | Two-body kinematics; ENDF-6 Formats Manual (MF=4) |
| Thin-target single-scatter flux fold | dR/dE_R = N_atoms * INT dPhi/dE_n * sum_i a_i dsigma_i/dE_R dE_n | Trapz/Simpson on log grid; O(h^2) | O(N_En x N_ER x N_iso) | O(N_ER) | Standard NR-rate formalism (e.g. Lewin-Smith 1996) |
| Watt spectrum eval/sample (SF) | 238U SF neutron source N(E)=C e^{-E/a} sinh(sqrt(bE)) | Analytic pdf; normalize numerically | O(N_E) | O(N_E) | Verbeke et al. UCRL-AR-228518; SOURCES-4C |
| (alpha,n) yield fold | Thick-target yield x normalized spectrum per (isotope, matrix) | Table interpolation | O(N_lines) | O(N_E) | SOURCES-4C (CCC-0661); published thick-target yields |
| Bateman decay-chain solver | Activity of U/Th chains + cosmogenic isotopes vs exposure/cooldown | Analytic (eigendecomp) or SymPy high-precision | O(N_nuc^3) once | O(N_nuc^2) | `radioactivedecay` (Fleming 2022, arXiv:2203.09761) |
| Photon self-shielding (thin slab) | Escape/absorption of decay gammas in 2 mm wafer | Analytic (1 - e^{-mu rho t})/(mu rho t) LOS avg | O(N_lines x N_mu) | O(1) | Beer-Lambert; NIST XCOM / xraylib |
| Count-conserving rebin to shared grid | Map any dR/dE onto `shared_energy_grid()` | Exact under integral preservation | O(N_bins) | O(N_bins) | Reuse v1.0 fold utilities |

### Convergence Properties

- **Recoil-kernel + flux fold:** Criterion — halving the internal E_n integration mesh changes total NR rate by < 0.5% and each shared-grid bin by < 1%. Rate: algebraic O(h^2) (trapezoid on log mesh). Failure mode: sharp Ge(n,el) resonances below ~1 MeV are under-resolved on a fixed coarse mesh — integrate on the **union** of the ENDF native energy grid and the flux grid.
- **Watt / (alpha,n) source:** Normalize the analytic pdf to unit integral; check the mean energy reproduces literature (238U SF mean ~ 2.0 MeV). Failure mode: parameter-set ambiguity shifts the mean ~10% (see caveats).
- **Bateman solver:** `radioactivedecay` is analytic; only failure mode is catastrophic cancellation when two half-lives are within floating-point ratio — use its SymPy high-precision mode for U/Th chains with widely separated half-lives.
- **Shared-grid rebin:** Criterion is exact count conservation — assert `sum(counts_out) == sum(counts_in)` to machine tolerance (reuse the v1.0 pattern in `tests/test_deposited_spectra_closure.py`).

## Software Ecosystem

### Primary Tools

| Tool | Version | Purpose | License | Maturity |
| ---- | ------- | ------- | ------- | -------- |
| `openmc` (openmc.data) | 0.15.x (conda-forge; osx-64 + osx-arm64) | Pure-Python ENDF MF=3/MF=4 reader: `IncidentNeutron.from_endf`, `AngleDistribution.from_endf`, `Reaction.xs` | MIT | Stable |
| numpy / scipy / matplotlib | numpy >= 1.26, scipy >= 1.11 | Fold, interpolation, integration, plotting (already in v1.0) | BSD | Stable |
| `radioactivedecay` | 0.6.x (PyPI) | Decay-chain activities, half-lives, branching; ICRP-107 default, ENSDF option | MIT | Stable |
| `xraylib` | 4.1.x (conda-forge, Python bindings) | Photon mass attenuation mu/rho for Ge/compounds (XCOM-equivalent) | BSD-style | Stable |
| ENDF/B-VIII.0 evaluated files | VIII.0 (2018) | Ge (70,72,73,74,76) neutron elastic xs + angular dist | Public (NNDC) | Established, widely benchmarked |

### Supporting Tools

| Tool | Version | Purpose | When Needed |
| ---- | ------- | ------- | ----------- |
| `sandy` | latest PyPI (`pip install sandy`) | ENDF-6 -> pandas dataframes (xs, decay, fission yields); covariance sampling | If `openmc.data` mis-parses a File-4 section or uncertainty bands are wanted |
| ENDFtk | njoy/ENDFtk (conda-forge `endftk`; C++/Python) | Robust low-level ENDF-6 read/write mirroring the Formats Manual | Deep ENDF surgery, non-standard MT sections |
| NJOY2016 | 2016.x | Resonance reconstruction, Doppler broadening, group averaging | Only if pointwise reconstruction below broadened resonances is required (heavier; compile) |
| SOURCES-4C | RSICC CCC-0661 (Fortran) | (alpha,n) + SF + delayed neutron source spectra | Cross-check the analytic Watt/(alpha,n) source; NOT required if published yields are used |
| ACTIVIA / COSMO | ACTIVIA (Back & Ramachers 2008, C++) | Cosmogenic production cross sections/yields for surface exposure | Cross-check Saldanha-2020/CDMSlite tabulated rates only |
| ENDF/B-VIII.1 | VIII.1 (2024; arXiv:2511.03564) | Newest evaluation | Sensitivity check vs VIII.0; not the default anchor |
| EXPACS / PARMA | PARMA-4.0 (Sato) | Cosmic-ray ground-level neutron flux, location-scaled | If Gordon-2004 form needs geomagnetic/altitude scaling for the site |

**macOS-local flags (no cluster).** Primary tools install via conda-forge with native Apple-Silicon (osx-arm64) or x86 (osx-64) builds — `openmc`, `xraylib`, `radioactivedecay`, `endftk`, `sandy`. **NJOY2016** needs a Fortran/C++ compile (gfortran) — avoidable in the recommended path. **SOURCES-4C** is legacy Fortran via RSICC (registration required, not pip-installable) — optional cross-check; use published tabulations as primary. **ACTIVIA** needs a C++ build + data files — optional cross-check only. **Geant4/G4CMP/MCNP/FLUKA are excluded** by the milestone constraint and are unnecessary given the thin-wafer single-scatter physics.

## Data Flow

```
Neutron-NR channel:
  Site neutron flux dPhi/dE_n              Ge(n,el) evaluated data (ENDF/B-VIII.0)
   [Gordon-2004 cosmic]                     [openmc.data.IncidentNeutron.from_endf]
   [(alpha,n) + SF radiogenic]                        |
            |                               sigma_i(E_n) (MF=3, MT=2)
            |                               dsigma_i/dOmega_cm (MF=4, MT=2)
            |                                          |
            |                              two-body kinematics + Jacobian
            |                                          |
            |                              dsigma_i/dE_R per isotope i
            +----------------> thin-target single-scatter fold <-----+
                               dR/dE_R = N_atoms INT dPhi/dE_n sum_i a_i dsigma_i/dE_R dE_n
                                          |
                               apply Ge NR quenching (physics input) -> dR/dE_dep
                                          |
                               rebin to shared_energy_grid()  (count-conserving)
                                          |
                               fold through R(E_rec|E_dep) + non-paralyzable censoring
                                          |
                               dR/dE_rec  (directly comparable to v1.0 spectra)

Radiogenic channel:
  Surface exposure + cooldown             Decay data (ENSDF/DDEP + radioactivedecay)
   [Saldanha-2020 / CDMSlite yields]        [gamma lines, betas, EC/IC, X-rays]
            |                                          |
   Bateman activities A_iso(t)  --------->  per-decay in-band deposit spectra
   (U/Th chains, 40K, 3H, 68Ge/68Ga,                  |
    65Zn, 60Co, 57Co)                       photon self-shielding (xraylib / XCOM)
            |                                          |
            +-------------------> dR/dE_dep (lines + betas + continua) ------+
                                          |
                               rebin to shared_energy_grid()  (count-conserving)
                                          |
                               fold through R(E_rec|E_dep) + non-paralyzable censoring
                                          |
                               dR/dE_rec
```

## Computation Order and Dependencies

| Step | Depends On | Produces | Can Parallelize? |
| ---- | ---------- | -------- | ---------------- |
| 1. Acquire Ge ENDF files (5 isotopes) | NNDC / OpenMC data release | local ENDF-6 files | Yes (independent downloads) |
| 2. Parse xs + angular dist with openmc.data | Step 1 | sigma_i(E_n), dsigma_i/dOmega_cm | Yes (per isotope) |
| 3. Build recoil kernels dsigma_i/dE_R | Step 2 + kinematics | per-isotope recoil kernels | Yes (per isotope) |
| 4. Assemble neutron flux (cosmic + radiogenic) | Gordon-2004 + Watt/(alpha,n) tables | dPhi/dE_n CSV (provenance header) | No (single assembly) |
| 5. Thin-target fold -> dR/dE_R -> dR/dE_dep | Steps 3, 4 + quenching | neutron dR/dE_dep on shared grid | No |
| 6. Radiogenic activities + line/beta/continuum builder | decay data + Saldanha yields | radiogenic dR/dE_dep on shared grid | Partially (per isotope) |
| 7. Fold both through R + censoring | Steps 5, 6 + v1.0 R matrices | dR/dE_rec spectra | Yes (per design/variant) |
| 8. Closure + validation tests | Steps 5-7 | passing count-conservation + benchmark checks | Yes |

## Resource Estimates

| Computation | Time (estimate) | Memory | Storage | Hardware |
| ----------- | --------------- | ------ | ------- | -------- |
| ENDF download (5 Ge isotopes) | seconds-minutes (network) | negligible | ~50-200 MB raw ENDF | local |
| openmc.data parse + kernel build (per isotope) | < 10 s each | < 200 MB | few MB per kernel | local CPU |
| Thin-target single-scatter fold (full flux) | seconds (vectorized numpy) | < 500 MB | few MB CSV | local CPU |
| Radiogenic activity + line/beta/continuum build | seconds | < 200 MB | few MB CSV | local CPU |
| Fold through R + censoring (per design/variant) | reuses v1.0 timing (seconds-minutes) | as v1.0 | as v1.0 npz | local CPU |
| OpenMC HDF5 data library (only if transport ever used) | one-time download | — | ~5-10 GB | local disk |

**Bottom line:** the entire v1.1 background computation is **seconds-to-minutes on a single macOS workstation** because it is an analytic thin-target fold, not a transport MC. The multi-GB OpenMC HDF5 library is **avoidable** — `openmc.data` reads raw ENDF-6 text directly and needs only the handful of Ge evaluations, not the full processed library. There is **no MC-sampling convergence budget** for the wafer response; the response-matrix fold reuses v1.0's already-validated MC.

## Integration with Existing Code

- **Input formats:** raw ENDF-6 text (Ge isotopes) for the neutron channel; tabulated CSV yields/parameters (Watt, (alpha,n), Saldanha production rates) with provenance headers matching the v1.0 convention (`data/flux/reactor_flux_v1.0.csv`, `data/gamma_lines.csv`).
- **Output formats:** `dR/dE_dep` CSV on the exact `shared_energy_grid()` bin edges, with a provenance header block (source library + version, ENDF MAT/MT, parameter sets, uncertainty band) mirroring `data/gamma_lines.csv` and `data/ge_xcom_mu.csv`. This is what the downstream fold expects.
- **Interface points:**
  - `src/qpd_potential/response.py` / `response_matrix.py` and the `.npz` `R(E_rec|E_dep)` matrices — v1.1 spectra fold through these unchanged.
  - `shared_energy_grid()` — v1.1 MUST bin onto the identical ~584-bin log grid (assert bin edges match before folding).
  - Fold/censoring utilities (`src/flux/assemble_spectrum.py`, `deposited_spectra.py`) — reuse the count-conserving rebin and non-paralyzable ~25 kHz / 40 us censoring; do not re-implement.
  - Test pattern `tests/test_deposited_spectra_closure.py`, `test_fold.py`, `test_response_chain.py` — extend with neutron- and radiogenic-spectrum closure tests.
- **Display floor:** honor the project rule — never plot Ge spectra/energy axes below 10 eV (grid-floor/binding-artifact territory).

## Validation Strategy

| Result | Validation Method | Benchmark | Source |
| ------ | ----------------- | --------- | ------ |
| Ge(n,el) cross section extracted | Compare openmc.data-parsed sigma(E_n) to NNDC/Sigma plots + ENDFtk/sandy spot check | ENDF/B-VIII.0 pointwise xs | NNDC; njoy/ENDFtk (OSTI 2448319) |
| Recoil kinematics | Max recoil E_R,max = E_n * 4A/(A+1)^2; check endpoint per isotope | Analytic two-body limit | Standard kinematics |
| Thin-target assumption | Confirm Sigma*t << 1 and multiple-scatter fraction < 0.1% | Sigma ~ 0.18 cm^-1, t = 0.2 cm | this file (n_Ge, sigma_tot) |
| 238U SF neutron spectrum | Mean energy and shape vs Watt fit | mean ~ 2.0 MeV; a,b sets (documented spread) | Verbeke UCRL-AR-228518; SOURCES-4C |
| Cosmic neutron flux normalization | Integral flux > 10 MeV | Gordon-2004 ~3.5e-3 cm^-2 s^-1; EXPACS ~3.3e-3 | Gordon 2004; Sato PARMA/EXPACS |
| Cosmogenic Ge production rates | Compare adopted yields to measured | 3H 82+-21, 65Zn 106+-13, 68Ge >=71 nuclei/kg/day (sea level) | CDMSlite (arXiv:1806.07043); EDELWEISS-III (arXiv:1607.04560); Saldanha 2020 |
| Photon attenuation mu/rho(Ge) | xraylib vs frozen XCOM points | `data/ge_xcom_mu.csv` (NIST XCOM) | NIST XCOM; xraylib |
| Decay-chain activities | radioactivedecay vs hand Bateman for a 3-member chain | analytic secular equilibrium | radioactivedecay (arXiv:2203.09761) |
| Shared-grid fold | Count conservation to machine precision | v1.0 closure test | `tests/test_deposited_spectra_closure.py` |

## Open Data / Version Caveats

- **ENDF/B-VIII.0 (2018)** is the well-benchmarked default anchor; **ENDF/B-VIII.1 (2024, arXiv:2511.03564)** exists and should be run as a sensitivity check, not the baseline, until its Ge evaluations are confirmed changed. JEFF-3.3 is a viable alternative library for the same isotopes (cross-check).
- **238U SF Watt parameters carry real spread across sources** (e.g. a=0.7124 MeV, b=5.6405 MeV^-1 Los Alamos model vs a=0.6483 MeV, b=6.811 MeV^-1 SOURCES-4A file). Pin ONE set with a cited source in the CSV header and carry the alternate as an uncertainty variant. LOW confidence on a single "correct" pair.
- **Exact patch versions** (openmc 0.15.x, radioactivedecay 0.6.x, xraylib 4.1.x) are MEDIUM confidence — verify with `pip show` / `conda list` at implementation time; the APIs cited (`IncidentNeutron.from_endf`, `AngleDistribution.from_endf`) are stable across recent releases.
- **radioactivedecay default is ICRP-107**, which is decay-constant/branching-oriented; for precise gamma/beta line energies and intensities prefer curated **ENSDF/DDEP** values (as v1.0 already does in `data/gamma_lines.csv`) and use radioactivedecay for chain activities/timing.

## Sources

- ENDFtk (njoy) — robust C++/Python ENDF-6 reader: [OSTI 2448319](https://www.osti.gov/biblio/2448319), [github.com/njoy/ENDFtk](https://github.com/njoy/ENDFtk)
- sandy (Fiorito) — ENDF-6 to pandas, covariance sampling: [PyPI](https://pypi.org/project/sandy/), [docs](https://luca-fiorito-11.github.io/sandy-docs/introduction.html)
- openmc.data — Python ENDF File 3/4 parser: [IncidentNeutron API](https://docs.openmc.org/en/stable/pythonapi/generated/openmc.data.IncidentNeutron.html), [angle_distribution module](https://docs.openmc.org/en/latest/_modules/openmc/data/angle_distribution.html), [data config](https://docs.openmc.org/en/stable/usersguide/data.html), [OpenMC cross-section data](https://openmc.org/data/)
- ENDF/B-VIII.0 — Brown et al., Nucl. Data Sheets 148 (2018): [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0090375218300206); ENDF/B-VIII.1: [arXiv:2511.03564](https://arxiv.org/pdf/2511.03564)
- SOURCES-4C — (alpha,n)/SF/delayed neutron source code: [OECD-NEA CCC-0661](https://www.oecd-nea.org/tools/abstract/detail/ccc-0661), [OSTI 976142](https://www.osti.gov/biblio/976142)
- 238U SF Watt spectrum — Verbeke et al. UCRL-AR-228518: [LLNL tech report](https://mcnp.lanl.gov/pdf_files/TechReport_2007_LLNL_UCRL-AR-228518_VerbekeHagmannEtAl.pdf); parameter table: [ResearchGate](https://www.researchgate.net/figure/The-Watt-spectrum-parameters-for-238-U-and-232-Th-12_tbl2_282181830)
- Gordon 2004 — ground-level cosmic-ray neutron spectrum/analytic fit (IEEE TNS 51, 3427): [ResearchGate](https://www.researchgate.net/publication/3139171_Measurement_of_the_flux_and_energy_spectrum_of_cosmic-ray_induced_neutrons_on_the_ground); PARMA/EXPACS extension (Sato): [PMC4973932](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4973932/)
- Cosmogenic Ge activation — CDMSlite tritium/isotope rates: [arXiv:1806.07043](https://arxiv.org/pdf/1806.07043); EDELWEISS-III: [arXiv:1607.04560](https://arxiv.org/pdf/1607.04560); ACTIVIA: [ResearchGate](https://www.researchgate.net/publication/1766248_ACTIVIA_Calculation_of_Isotope_Production_Cross-sections_and_Yields)
- radioactivedecay — decay-chain Python package: [arXiv:2203.09761](https://arxiv.org/pdf/2203.09761), [docs](https://radioactivedecay.github.io/), [github](https://github.com/radioactivedecay/radioactivedecay)
- NIST XCOM / xraylib — photon attenuation: [XCOM database](https://www.nist.gov/pml/xcom-photon-cross-sections-database), [NIST XrayMassCoef Ge (Z=32)](https://physics.nist.gov/PhysRefData/XrayMassCoef/ElemTab/z32.html)
- OpenMC install (macOS/conda) + ENDF/B-VIII.0 HDF5: [OpenMC data](https://openmc.org/data/), [Zenodo 8410375](https://zenodo.org/records/8410375)
</content>
