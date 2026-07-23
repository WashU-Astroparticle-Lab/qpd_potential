# Computational Approaches: Reactor-CEvNS + Cosmic-Muon Reconstructed-Energy Spectra in a QPD-Instrumented Ge Crystal

**Surveyed:** 2026-07-20
**Domain:** Low-energy neutrino/cosmic-ray rate calculation + Monte-Carlo readout-chain simulation (superconducting quasiparticle detectors)
**Confidence:** HIGH for local-repo inventory (code read directly); MEDIUM-HIGH for external package status (verified via GitHub/paper pages); MEDIUM for background-knowledge numbers flagged inline

## Recommended Stack

Pure Python (numpy/scipy/matplotlib) on the local macOS workstation. Nothing in this project needs HPC, Geant4, or G4CMP: the physics rates are 1-2D integrals, the muon generator is an analytic-formula sampler, and the readout chain is a vectorizable point-process Monte Carlo. The single heaviest computation (a detector response matrix built by MC) is minutes on a laptop.

**Reuse strategy (opinionated):**

1. **Readout chain — reuse the local qpd repo nearly verbatim.** `qpd/src/qpd/simulator/quasiparticle_bursts.py` (`QuasiparticleBurstModel`, `BurstTruth`, `poisson_burst_times`) is exactly the EMG-burst point-process generator this project needs: per burst, `N ~ Poisson(expected_n_qp)`, offsets `= Normal(mu, sigma) + Exponential(tau)`, sorted absolute event times plus ground truth. `parity.py` (`parity_from_flip_times`, `generate_parity_trajectory`) provides the searchsorted-based flip-time-to-grid machinery and the burst/background merge logic. Add fresh, thin layers on top: per-event Bernoulli thinning (50% efficiency), a bandwidth/pile-up censoring model (25 kHz max resolvable rate), and the energy-to-`expected_n_qp` map for the Ta→Al and Al→Hf designs.
2. **CEvNS rate — write fresh (~150 lines), validate against wimprates and bradkav/CEvNS.** The local wimprates repo (v0.5.0) has the right *pattern* (`rate_elastic` = flux-weighted `scipy.integrate.quad` over a kinematic threshold, `helm_form_factor_squared` from Lewin & Smith, `Ge` already in `ATOMIC_WEIGHT`), but it is hardwired to dark-matter halo velocity integrals and the global-state `numericalunits` package. Do not import it as a dependency; copy the Helm form-factor formula into plain-keV units and cross-check numerically against `wimprates.helm_form_factor_squared` (should agree to float precision).
3. **Reactor spectrum — tabulate Huber-Mueller >2 MeV; extend below with a summation-model table.** Hard-code the Huber (arXiv:1106.0687) exponential-polynomial fits for 235U/239Pu/241Pu and Mueller et al. (arXiv:1101.2663) for 238U. The sub-IBD-threshold region (Eν < 1.8-2 MeV) matters for low-threshold Ge CEvNS and is NOT covered by Huber tables — take a digitized/tabulated summation-model spectrum (see Data Gaps below; CONFLUX can generate one if a published table is not adopted).
4. **Muon flux — reimplement the Guan et al. modified-Gaisser formula (arXiv:1509.06176) as a ~50-line numpy rejection sampler.** EcoMug (the standard lightweight Geant4 alternative) is header-only C++; wrapping it costs more than reimplementing the analytic flux formula it parametrizes.

## Numerical Algorithms

| Algorithm | Problem | Convergence | Cost per Step | Memory | Key Reference |
| --- | --- | --- | --- | --- | --- |
| Flux-folded rate integral (quad or log-grid trapezoid) | dR/dT = N_T ∫_{Eν,min(T)} dEν Φ(Eν) dσ/dT | quad: `epsrel=1e-6`; trapezoid: 2nd order in grid spacing | O(n_Eν) per recoil-energy point | O(n_Eν) | wimprates `rate_elastic` pattern; Freedman CEvNS xsec (standard) |
| Rejection sampling of (E, cosθ) muon flux | Draw muons from modified Gaisser | Exact (acceptance-rejection); efficiency set by envelope tightness | O(1)/trial, vectorized | O(N) | Guan et al. arXiv:1509.06176; EcoMug NIM A 1014, 165732 (2021) |
| Chord-length sampling on a box | Muon path length in crystal | Exact (analytic ray-box intersection) | O(1), vectorized | O(N) | standard geometry |
| Landau-like straggling via `scipy.stats.moyal` | Energy-deposit fluctuations around ⟨dE/dx⟩·L | Exact sampling of Moyal approx to Landau (approximation error is physical, not numerical) | O(1) | O(N) | PDG passage-of-particles review; scipy ≥1.1 |
| Lewis-Shedler thinning | Inhomogeneous Poisson event streams (if a time-varying burst rate is needed) | Exact given majorant λ* ≥ λ(t) for all t | O(1)/candidate; efficiency λ̄/λ* | O(N) | Lewis & Shedler, Nav. Res. Logist. Q. 26, 403 (1979) |
| EMG burst sampling (Normal + Exponential) | Tunneling-event times within a burst | Exact | O(N_qp) per burst | O(N_qp) | qpd repo `quasiparticle_bursts.py` (already implemented) |
| Bernoulli thinning | 50% sensor efficiency | Exact | O(1)/event | O(N) | elementary |
| Sort-and-merge pile-up censoring | 25 kHz max resolvable tunneling rate (50 kHz bandwidth): events closer than the resolving time are merged/lost | Exact given the chosen censoring rule | O(N log N) per trace (sort) | O(N) | fresh code; convention must be fixed in CONVENTIONS.md |
| MC response matrix R(E_rec \| E_true) | Fold analytic dR/dT through the readout chain | Per-cell relative error ≈ 1/√n_ij; target ≤3% per populated cell | O(N_samples × ⟨N_qp⟩) | O(n_true × n_rec) matrix, trivially small | standard detector-response folding |

### Convergence Properties

- **Rate integral.** Criterion: quad `epsrel=1e-6` (wimprates default pattern), or for the vectorized trapezoid, halve the log-Eν grid spacing until the total rate changes by <0.1%. Failure mode: the integrand support is a narrow window just above Eν,min(T) = (T + √(T² + 2 M_Ge T))/2 ≈ √(M_Ge T/2), multiplied by a steeply falling reactor flux; a linear Eν grid that does not resolve the region near Eν,min underestimates the rate at the highest recoil energies. Use a log grid anchored exactly at Eν,min per T value.
- **Muon MC.** Statistical error scales as 1/√N per histogram bin. Criterion: N large enough that every reported reconstructed-energy bin has ≥1000 accepted events (≤3% relative error). Rejection efficiency: with a power-law envelope in E and uniform cosθ, expect ≳10% acceptance; a flat envelope over a wide E range can drop below 1% — tighten the envelope rather than brute-forcing.
- **Response matrix.** Sample uniformly (or log-uniformly) in E_true per column — this is importance sampling that decouples MC cost from the steeply falling physical spectrum. Criterion: ≥10⁴ burst realizations per E_true column; verify the folded spectrum changes by <1% when doubling samples. Failure mode: direct event-by-event MC of the physical CEvNS spectrum instead of response folding — reactor CEvNS in 1 kg Ge is O(1-100) counts/kg/day depending on site, so simulating "one live-time" gives statistically useless spectra; always fold.
- **Pile-up model.** Not a convergence issue but a convention issue: the mapping from "events within one resolving time" to "counted events" (merge to one count vs. dead-time loss) changes the saturation curve. Fix the rule once, document it, and verify the counting statistics against the analytic Type-I (non-paralyzable) dead-time formula m = n/(1 + n·τ_d) in the constant-rate limit.

## Software Ecosystem

### Primary Tools

| Tool | Version | Purpose | License | Maturity |
| --- | --- | --- | --- | --- |
| numpy | ≥1.23 | All array math, `default_rng` sampling | BSD | stable |
| scipy | ≥1.9 | `integrate.quad`, `stats.moyal`, `special.erf` | BSD | stable |
| matplotlib | ≥3.3 | Spectra figures | PSF-like | stable |
| pyyaml | ≥5.4 | Read `materials.yaml`-style config | MIT | stable |
| local qpd repo (`/Users/lanqingyuan/Documents/GitHub/qpd`) | 0.1.0 | EMG burst model, parity/flip-time machinery, materials DB | see repo LICENSE | working research code, tested via `checks/` |
| local wimprates (`/Users/lanqingyuan/Documents/GitHub/wimprates`) | 0.5.0 | Helm form-factor validation reference; rate-integral pattern | per repo | stable (Zenodo DOI 10.5281/zenodo.2604222) |

### Supporting Tools (reference/validation only — do not add as dependencies)

| Tool | Version | Purpose | When Needed |
| --- | --- | --- | --- |
| bradkav/CEvNS (github.com/bradkav/CEvNS) | v1.0 (2018), MIT, Python | Independent SM CEvNS rate benchmark; ships a CHOOZ reactor flux table | Validation of the fresh CEvNS code (clone locally, run once) |
| Ikaroshu/pyCEvNS (github.com/Ikaroshu/pyCEvNS) | github | Alternative CEvNS/NSI package | Only if bradkav/CEvNS is insufficient; not needed for SM rates |
| CONFLUX (github.com/CNFLUX/conflux) | 0.7 docs, MIT, LLNL; arXiv:2503.18966 | Summation-method reactor spectrum incl. Eν < 1.8 MeV, from ENDF/JEFF/ENSDF | If no published low-energy spectrum table is adopted; heavy (downloads nuclear DBs) — run once offline to produce a frozen CSV |
| EcoMug (NIM A 1014, 165732, 2021) | header-only C++11 | Reference implementation of surface muon generation (>10⁵ μ/s) | Cross-check of the numpy Guan-formula sampler only; do not integrate |
| qutip, iminuit, resonator_tools (qpd repo deps) | — | Dispersive-readout theory in qpd repo | NOT needed here: this project works at the tunneling-event-count level, not I/Q waveforms |

### Local Repo Inventory (inspected directly)

**qpd repo — reuse directly:**

- `src/qpd/simulator/quasiparticle_bursts.py` — `QuasiparticleBurstModel(times, tau, mu, sigma, expected_n_qp)` with `.sample(rng) -> (event_times, list[BurstTruth])`; `poisson_burst_times(rate_hz, duration, rng)` for homogeneous-Poisson burst arrivals. `expected_n_qp` accepts a per-burst array — this is precisely the hook for mapping deposited energy → expected tunneling count per burst. `BurstTruth` records `t_arrival, n_qp, t_start, t_end, event_times` (perfect-tunneling-ID ground truth is already the design of this class).
- `src/qpd/simulator/parity.py` — `parity_from_flip_times` (vectorized searchsorted, `side="right"` convention) and `generate_parity_trajectory` (two-state CTMC with burst flips as external forcing, exact resampling via memorylessness). Needed only if the analysis descends to parity-trajectory level; for count-level spectra, `quasiparticle_bursts` alone suffices.
- `src/qpd/theory/materials.yaml` — DOS, T_c, Δ for Al (Δ=1.89e-4 eV), AlMn, Hf (Δ=2.25e-5 eV, T_c=0.128 K), Nb, TiN, plus constants (BCS ratio 1.764). **Gap: no tantalum entry.** The Ta→Al design requires adding Ta (T_c≈4.48 K, Δ≈0.7 meV — verify against literature before adding; do not trust these from memory).
- `src/qpd/mlebench/generate.py` — chunked dataset-generation pattern (frozen physics config + per-chunk structural randomization + seed bookkeeping); a good template for organizing MC campaigns, not a direct dependency.
- `src/qpd/simulator/vna_simulator.py`, `resonator.py`, `noise.py`, `checks/check_readout_window.py` — full I/Q waveform chain (Probst notch S21, dispersive χ, lock-in window). Out of scope for this project (no G4CMP, count-level analysis), but available if a waveform-level sanity check of the 50 kHz bandwidth limit is ever wanted.

**wimprates repo — pattern donor + validation oracle:**

- `wimprates/elastic_nr.py` — `helm_form_factor_squared(erec, anucl)` (Lewin & Smith parameters c=1.23·A^{1/3}−0.60 fm, a=0.52 fm, s=0.9 fm), `ATOMIC_WEIGHT['Ge']=72.64`, `reduced_mass`, and the `rate_elastic` structure (kinematic v_min threshold + `quad` over flux weight). The CEvNS analog replaces the halo-velocity integral with the neutrino-energy integral; the code shape carries over one-to-one.
- Uses `numericalunits` (global mutable unit state) — the reason to copy formulas rather than import.

## Data Flow

```
Reactor inputs (P_th, distance, fission fractions)
  -> Huber-Mueller polynomials + low-E summation table  -> Φ(Eν) [ν / MeV / fission], fissions/s = P_th / Σ f_i e_i
  -> CEvNS kernel: dσ/dT (Freedman SM, Helm FF)         -> analytic dR/dT_true  [counts / kg / day / keV]

Muon inputs (Guan modified-Gaisser flux, crystal box geometry)
  -> rejection-sample (E_mu, cosθ, φ, entry point)      -> chord length L
  -> <dE/dx>(E_mu) * L + Moyal straggling               -> MC sample of E_dep -> dR/dE_dep

Readout-chain inputs (design: Ta→Al or Al→Hf; 1 sensor/mm², ε≈0.5; 50 kHz BW)
  -> E_dep -> expected_n_qp(E_dep) map (from theory dimension)
  -> QuasiparticleBurstModel.sample (EMG: tau, mu, sigma)
  -> Bernoulli thinning (ε) -> pile-up/bandwidth censoring (25 kHz)
  -> counted events N_det -> E_rec estimator
  -> response matrix R(E_rec | E_true) on (n_true x n_rec) grid

Fold: dR/dE_rec = R @ dR/dE_true   (separately for CEvNS and muons, per design)
  -> final reconstructed-energy spectra + figures
```

## Computation Order and Dependencies

| Step | Depends On | Produces | Can Parallelize? |
| --- | --- | --- | --- |
| 1. Reactor Φ(Eν) table (incl. low-E extension) | Huber/Mueller coefficients; summation table or one-off CONFLUX run | frozen CSV Φ(Eν) | n/a (one-off) |
| 2. Analytic CEvNS dR/dT | Step 1; Helm FF; Ge mass/isotopes | dR/dT_true on log grid | yes (per T point) |
| 3. Muon E_dep MC | Guan sampler; box geometry; dE/dx table | dR/dE_dep histogram + event list | yes (embarrassingly) |
| 4. E→n_qp map + EMG parameters per design | theory dimension (not this file) | `expected_n_qp(E)`, (tau, mu, sigma) | n/a |
| 5. Response matrix per design | Steps 4; qpd burst model; thinning + censoring code | R(E_rec\|E_true), 2 designs | yes (per E_true column) |
| 6. Folding + spectra | Steps 2, 3, 5 | dR/dE_rec figures | trivial |

## Resource Estimates

| Computation | Time (estimate) | Memory | Storage | Hardware |
| --- | --- | --- | --- | --- |
| CEvNS dR/dT, 200 T points, quad epsrel 1e-6 | seconds-1 min; vectorized trapezoid <1 s | <100 MB | KB (CSV) | laptop |
| Muon MC, 10⁶ accepted muons (vectorized numpy) | ~1-10 s | <1 GB | ~50 MB if event list saved | laptop |
| Response matrix: 200 E_true columns × 10⁴ bursts | ~10-100 s per design (dominated by per-burst EMG draws; ⟨N_qp⟩ can reach 10⁴-10⁶ for MeV muon deposits — see pitfall below) | <2 GB if chunked per column | MB | laptop |
| Full pipeline, both designs | minutes | <2 GB | <100 MB | laptop |

Scale sanity numbers (background knowledge, order-of-magnitude; verify in the theory dimension): 1 kg Ge (ρ=5.32 g/cm³) is a ~5.7 cm cube, top-face area ~33 cm²; sea-level muon rate through it ~0.5/s (rule-of-thumb 1 μ/cm²/min); mean chord ~3.8 cm at ⟨dE/dx⟩~7 MeV/cm gives ~25-30 MeV typical muon deposits — 4-7 orders of magnitude above CEvNS recoils (T_max ≈ 2Eν²/M_Ge ≈ 1.9 keV at Eν=8 MeV). The two populations stress completely different parts of the readout chain.

**Nothing here needs more than a laptop.** The only computation that could blow up is naively sampling every individual quasiparticle tunneling event for MeV-scale muon deposits if `expected_n_qp` reaches ≫10⁶ per burst; if so, switch that regime to a Gaussian/analytic approximation of the counting statistics (valid at large N) instead of explicit event lists — the saturated-readout limit does not need per-event times anyway.

## Integration with Existing Code

- **Input formats:** qpd `QuasiparticleBurstModel` takes plain numpy arrays (seconds, dimensionless counts) and a `np.random.Generator` seeded upstream — adopt the same convention (explicit `rng` threading, absolute times in seconds) throughout the new code.
- **Interface points:** (a) `expected_n_qp` array argument of `QuasiparticleBurstModel` = energy-deposit hook; (b) `BurstTruth.event_times` = input to the fresh thinning + censoring layer; (c) `materials.yaml` schema = template for the project's own material/design config (add Ta; keep units and the eV conventions documented in that file).
- **Import vs. copy:** the qpd repo is a proper installable package (`pip install -e /Users/lanqingyuan/Documents/GitHub/qpd`); importing `qpd.simulator.quasiparticle_bursts` directly is safe (module depends only on numpy). Note the heavier `qpd` package `__init__` pulls transmon theory (qutip) — import the submodule path, not the top-level package, to avoid the qutip dependency at runtime; verify this at implementation time.
- **wimprates:** validation only; call `wimprates.helm_form_factor_squared` in a test, never in the pipeline.

## Validation Strategy

| Result | Validation Method | Benchmark | Source |
| --- | --- | --- | --- |
| Helm FF² (Ge) | Compare fresh keV-unit implementation vs `wimprates.helm_form_factor_squared(erec, 72.64)` over 0.01-10 keV | agreement to ≲1e-10 relative | local wimprates v0.5.0 |
| SM CEvNS rate | Run bradkav/CEvNS with its CHOOZ flux for Ge; match with same flux input | agreement to a few % (flux-table differences) | github.com/bradkav/CEvNS (arXiv:1805.01798) |
| Reactor-Ge rate scale | Compare predicted counts/kg/day at a CONUS+-like configuration against published CONUS+ prediction/observation | order-of-magnitude + shape | CONUS+ CEvNS detection (2025); exact citation to be pinned in PRIOR-WORK |
| Muon sampler | Integrated vertical intensity and angular distribution vs PDG values; total rate vs 1 μ/cm²/min rule | I_v ≈ 70 m⁻²s⁻¹sr⁻¹ (PDG, background knowledge — verify) | Guan arXiv:1509.06176; PDG cosmic-ray review |
| EMG sampler | Sample moments: mean = mu + tau, var = sigma² + tau² | analytic | closed form; qpd model already unit-consistent |
| Thinning + censoring | Constant-rate limit vs non-paralyzable dead-time formula m = n/(1+nτ_d); ε-thinning recovers binomial statistics | analytic | standard |
| Response folding | Fold a delta-function spectrum; recover the single-column response | exact | internal consistency |

## Known Numerical Pitfalls (checklist for implementation)

1. **Low-energy flux cutoff:** Huber tables cover roughly 2-8 MeV (background knowledge — verify exact range against arXiv:1106.0687 when transcribing); naively extrapolating the exponential-polynomial below its fit range produces unphysical spectra. Use a summation-model table below ~2 MeV; the sub-IBD region contributes substantially to low-threshold Ge CEvNS (arXiv:2302.10460).
2. **Rate-integral stability:** anchor the Eν grid at Eν,min(T) exactly; log-spacing; watch the T→T_max edge where the integration window shrinks to zero (integrand → 0, but a coarse grid gives negative or noisy rates).
3. **Units bookkeeping:** Φ in ν/MeV/fission × fissions/s (P_th / ⟨e_fission⟩ with ⟨e⟩≈200 MeV weighted by fission fractions) × 1/(4πL²); cross section in cm²; a factor-of-4π or per-fission/per-second slip is the classic error here. State conventions in CONVENTIONS.md before coding.
4. **Steep spectra + histogram binning:** use log-spaced reconstructed-energy bins (spectra span eV-scale CEvNS recoils to tens-of-MeV muon deposits); never subtract histograms with unmatched bin edges.
5. **Saturation regime:** during a muon burst the instantaneous tunneling rate (N_qp × EMG pdf peak) exceeds 25 kHz by orders of magnitude; reconstructed energy compresses nonlinearly. This is the physics headline, not a bug — but it means the E_rec estimator must be defined and characterized in the saturated regime, and the ⟨N_qp⟩≫10⁶ event lists should be replaced by analytic counting statistics (see Resource Estimates).
6. **EMG pre-onset events:** Gaussian lower tail lets events precede burst onset (documented in `quasiparticle_bursts.py`); the censoring window must key off actual event times (`BurstTruth.t_start`), not `t_arrival`.
7. **RNG discipline:** one `np.random.default_rng(seed)` per run, threaded explicitly (qpd convention); never mix with legacy `np.random.*` global state.
8. **Materials data provenance:** `materials.yaml` values are sourced from Serniak et al. PRA 2019 / arXiv:2405.17192 per its header; the missing Ta entry must be added with a citation, not from memory.

## Data Gaps / Open Items for Phase Research

- **Sub-2 MeV reactor spectrum table:** pick a specific published summation dataset (e.g., from the arXiv:2302.10460 supplementary material or a one-off CONFLUX run) — decision deferred to phase research; freeze it as a versioned CSV either way.
- **Tantalum superconductor parameters** for the Ta→Al design (Δ, DOS, T_c with citation).
- **E_dep → expected_n_qp conversion** (phonon-to-QP efficiency per design) is a theory-dimension input; the computational hook (`expected_n_qp` array) is ready.
- **Exact censoring convention** for the 25 kHz limit (merge vs. drop; paralyzable vs. non-paralyzable) — must be fixed in CONVENTIONS.md before the response matrix is built.

## Sources

- Local qpd repo (read 2026-07-20): `/Users/lanqingyuan/Documents/GitHub/qpd/src/qpd/simulator/{quasiparticle_bursts.py,parity.py,vna_simulator.py,noise.py,resonator.py}`, `/Users/lanqingyuan/Documents/GitHub/qpd/src/qpd/theory/materials.yaml`, `pyproject.toml`, `checks/check_readout_window.py`, `src/qpd/mlebench/generate.py`
- Local wimprates v0.5.0 (read 2026-07-20): `/Users/lanqingyuan/Documents/GitHub/wimprates/wimprates/{elastic_nr.py,halo.py,utils.py}`, `README.md` — Helm FF, rate-integral pattern, Ge atomic weight
- bradkav/CEvNS — https://github.com/bradkav/CEvNS (MIT, v1.0 2018, arXiv:1805.01798) — SM CEvNS xsec + CHOOZ reactor flux, validation benchmark
- Ikaroshu/pyCEvNS — https://github.com/Ikaroshu/pyCEvNS — alternative CEvNS package (not selected)
- CONFLUX — https://github.com/CNFLUX/conflux , https://conflux.readthedocs.io , arXiv:2503.18966 (Comput. Phys. Commun., MIT license) — summation/conversion reactor flux framework
- P. Huber, Phys. Rev. C 84, 024617 (2011), arXiv:1106.0687 — converted 235U/239Pu/241Pu spectra
- T. Mueller et al., arXiv:1101.2663 — improved reactor spectra incl. 238U (summation)
- Reactor flux below IBD threshold with CEvNS — arXiv:2302.10460 (Phys. Rev. D 108, 033002)
- M. Guan et al., arXiv:1509.06176 — modified Gaisser sea-level muon flux (valid to low E, all zenith angles)
- EcoMug — Pagano et al., NIM A 1014, 165732 (2021) (sciencedirect S0168900221007178) — efficient cosmic muon generator, reference implementation
- Lewis & Shedler, Nav. Res. Logist. Q. 26, 403 (1979) — inhomogeneous Poisson thinning (background knowledge; standard reference)
