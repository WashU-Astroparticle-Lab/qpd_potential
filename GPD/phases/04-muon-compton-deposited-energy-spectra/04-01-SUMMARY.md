# Plan 04-01 Summary — Muon Deposited-Energy Spectrum dR/dE_dep

**One-liner:** The sea-level cosmic-ray muon deposited-energy spectrum for the 110 g Ge wafer is produced on the unified phonon scale (no quenching) by folding the Gaisser–Guan angular/energy flux with the analytic ray–box chord-length distribution and the Landau–Vavilov **most-probable** deposit (Δ_p, not the mean, not Moyal); integral rate **1.366 ± 0.005 Hz** (PDG ~1.5–2 Hz, VALD-02 within ~15%), vertical-chord MPV **1.232 MeV** sitting strictly below the mean **1.459 MeV**, with the long near-horizontal chord tail resolved to **~197 MeV** (the Phase-5 saturation input).

**Status:** Tasks 1–2 complete and verified (98/98 tests pass). Task 3 (`checkpoint:human-verify`) executed and **self-assessed satisfied, pending orchestrator review** per the autonomous-run directive — not blocked.

**Profile/mode:** numerical / balanced autonomy / code-heavy. Phase class: numerical.

---

## Conventions in effect (from `state.json` convention_lock + CONVENTIONS §B/§D/§G)

| Quantity | Convention | Notes |
| --- | --- | --- |
| Energy scale | Single unified **phonon E_dep** scale, **NO quenching**, no keVee/keVnr | Muon = electron recoil, zero Frenkel-defect correction (§B) |
| Wafer geometry | 10.16 × 10.16 × 0.20 cm, V = 20.65 cm³, ρ = 5.323 g/cm³, m = 109.9 g | Reused from `params.py`; per-kg normalization kept (§D) |
| Chord / mass thickness | ℓ [cm]; **x = ρℓ [g/cm²]** carried explicitly into Landau formulas | Guards Pitfall 4 |
| Output units | counts·kg⁻¹·day⁻¹·keV⁻¹; rate in Hz | Shared log E_dep grid 0.01 keV → 200 MeV, ~80 bins/decade |
| Metric / gauge / Fourier | not_applicable | No relativistic field theory in this channel |

---

## Key results (with confidence)

- **Integral muon rate = 1.366 ± 0.005 Hz** (N = 4×10⁶, seed 20260720). Deterministic quadrature cross-check 1.415 Hz (E>0.1 GeV). PDG anchor ~1.5–2 Hz. **[CONFIDENCE: HIGH]** — independent checks: MC vs analytic quadrature (agree), J_horiz surface-measure test (0.01%), Gaisser–Guan I_v(>1 GeV) = 60 m⁻²s⁻¹sr⁻¹ (inside the 30–35% inter-experiment band).
- **Vertical-chord MPV Δ_p = 1.232 MeV**, strictly below the mean ⟨Δ⟩ = 1.459 MeV (= 1.370 MeV·cm²/g × 1.065 g/cm²). Computed in code from the PDG formula (not memorized). **[CONFIDENCE: HIGH]** — sampled mode matches the analytic Δ_p, and ξ(vertical) = 0.0721 MeV matches the PDG 0.072 MeV.
- **ξ(vertical, x = 1.065 g/cm²) = 0.0721 MeV** — confirms mass-thickness units (feeding ℓ[cm] would give ~5× too small). **[CONFIDENCE: HIGH]**
- **High-E tail resolved to ~197 MeV**; 66 non-empty bins above 30 MeV. Driven by long near-horizontal chords (up to the 14.37 cm space diagonal). **[CONFIDENCE: HIGH]** — geometry Cauchy invariant ⟨ℓ⟩ = 0.385 cm reproduced to 0.03%.
- **κ = ξ/T_max < 0.07 for all wafer chords** (even the longest chord at the lowest MIP energy) → firmly in the Landau/mild-Vavilov regime; the Gaussian branch is never triggered. **[CONFIDENCE: HIGH]**
- **Convergence:** rate stable to ~1% under 2× samples; vertical MPV stable to <2 keV bins. **Energy closure:** ∫ dR/dE_dep dE = rate × 86400 / mass_kg to 1e-3. **[CONFIDENCE: HIGH]**

---

## Acceptance-test outcomes (self-assessed)

| Test | Procedure | Result | Verdict |
| --- | --- | --- | --- |
| **test-cauchy** | Isotropic flux → mean chord vs 4V/S | ⟨ℓ⟩ = 0.3849 cm vs 0.3848; vertical 0.20 cm, max 14.24→diag 14.37 cm | **PASS** |
| **test-jhoriz** | cos²θ flux → surface rate vs πI_v/2 | 1.0996e-2 vs 1.0996e-2 (0.01%) | **PASS** |
| **test-mpv** | ξ, Δ_p (vertical) vs PDG; MPV < mean | ξ = 0.0721 MeV; sampled MPV 1.232 < mean 1.459 MeV | **PASS** |
| **test-hetail** | High-E tail present + stable under 2× | deposits to ~197 MeV, 66 bins > 30 MeV; rate stable ~1% | **PASS** |
| **test-muon-rate** (VALD-02) | Integral rate vs PDG × acceptance | 1.366 Hz, within ~15% of 1.5–2 Hz (≤30%) | **PASS** |

Forbidden proxies rejected: **fp-mean-not-mpv** (Landau MPV sampled, not mean, not Moyal), **fp-angular-bias** (surface measure I·A_proj·sinθ, verified by J_horiz), **fp-quenching-muon** (single phonon scale, no quenching).

---

## Method notes / decisions (balanced-autonomy, in-scope)

- **Custom Landau sampler:** numerical inverse-CDF of the standard Landau density φ(λ)=(1/π)∫₀^∞ e^{−t ln t − λt} sin(πt) dt (mode λ=−0.22278, textbook/PDG). Built once and cached. pylandau is absent (as the plan anticipated); `scipy.stats.landau` (v1.17) is available but uses a *different* location/scale parametrization (mode −0.429), so it is kept only as an optional second opinion, not the engine.
- **Deposit = Δ_p + ξ(λ − λ_mode)**, so the sampled mode sits exactly at the PDG Δ_p; deposits capped at the muon kinetic energy (energy conservation). Gaussian branch implemented for κ≥10 but never used here (κ_max ≈ 0.07).
- **Density effect** via Sternheimer Ge coefficients (At. Data Nucl. Data Tables 30, 261) — a modest correction to the MPV log-bracket; coefficients tagged MEDIUM confidence.
- **Importance sampling:** zenith drawn uniform in [0, π/2] (oversamples the horizon vs the physical sinθ·cos²θ measure) with proper reweighting, so the rare long-chord tens-of-MeV tail is statistically resolved; energy drawn from an E^−2.7 proposal.

## Deviations / issues

- **DEVIATION (Rule 1, test-expectation fixes, not code):** two initial geometry-test assertions were physically wrong — (a) grazing corner-clipping rays legitimately give near-zero chords (no positive lower chord bound), and (b) a deterministic long-chord ray was launched from the wrong entry face. Both corrected; the sampler code was unchanged and correct.
- **Noisy sub-keV bins:** a few non-empty bins at 0.01–1 keV come from rare grazing-corner chords depositing ~nothing; they carry negligible rate (large relative MC error) and do not affect the physics. Honest feature, not a bug.
- **Scope omissions (named, per RESEARCH Pitfall 6):** through-going primaries only — stopped-muon Michel electrons, soft EM component, δ-ray escape, and muon-induced neutrons are out of scope for this baseline and must be named in any downstream sensitivity statement.

## Reproducibility

- Seed 20260720; NumPy 1.26.4, SciPy 1.17.1, Python 3.11.7. Regenerate: `python scripts/make_muon_spectrum.py`.

## Deliverables

- `src/qpd_potential/wafer_geometry.py`, `src/qpd_potential/muon_flux.py`, `src/qpd_potential/muon_deposit.py`
- `tests/test_muon_geometry.py` (7), `tests/test_muon_channel.py` (9)
- `scripts/make_muon_spectrum.py`, `data/muon_dRdEdep.csv`, `figs/muon_dep_check.png`

## Self-Check: PASSED

All deliverable files exist; three atomic commits recorded (162214f, 4813d2f, c408a6f); 98/98 tests pass; CSV/figure regenerated reproducibly; every contract claim, acceptance test, and forbidden proxy has an explicit outcome below.

```yaml
gpd_return:
  status: checkpoint
  phase: "04"
  plan: "01"
  tasks_completed: 3
  tasks_total: 3
  duration_seconds: 2700
  files_written:
    - src/qpd_potential/wafer_geometry.py
    - src/qpd_potential/muon_flux.py
    - src/qpd_potential/muon_deposit.py
    - tests/test_muon_geometry.py
    - tests/test_muon_channel.py
    - scripts/make_muon_spectrum.py
    - data/muon_dRdEdep.csv
    - figs/muon_dep_check.png
    - GPD/phases/04-muon-compton-deposited-energy-spectra/04-01-SUMMARY.md
  issues:
    - "Task 3 is checkpoint:human-verify; per the autonomous directive it is recorded satisfied-pending-orchestrator-review, not blocked. Orchestrator to confirm VALD-02 (rate 1.366 Hz vs PDG 1.5-2 Hz, within ~15%) and that the muon spectrum is physically sound (MPV<mean, tens-of-MeV tail, deposited/phonon axis, no quenching) before the Phase-5 handoff."
    - "Sternheimer Ge density-effect coefficients tagged MEDIUM confidence (standard tabulated values); the density effect is a modest correction to the MPV log-bracket and does not affect the mean-vs-MPV or tail conclusions."
    - "A few non-empty sub-keV bins (0.01-1 keV) are rare grazing-corner chords with negligible rate and large MC error; physical, not spurious."
    - "Scope omissions named (through-going primaries only): stopped-muon Michel electrons, soft EM component, delta-ray escape, muon-induced neutrons (the last mimic CEvNS nuclear recoils and are the dominant real reactor-CEvNS background) - out of scope, must be named downstream."
  next_actions:
    - "Orchestrator: review the Task-3 checkpoint figure figs/muon_dep_check.png and CSV data/muon_dRdEdep.csv, then sign off VALD-02 / CALC-03."
    - "Phase 5: co-add this muon dR/dE_dep with the Compton channel (04-03) on the identical shared log grid, then fold through R(E_rec|E_dep); the tens-of-MeV long-chord tail is the saturated-regime input."
    - "Plan 04-02 (Compton channel): reuse shared_energy_grid() from muon_deposit.py for a co-addable spectrum."
  decisions:
    - summary: "Muon dR/dE_dep folded from Gaisser-Guan flux (P1-P5 verbatim, arXiv:1509.06176) x analytic ray-box chord (Cauchy <ell>=0.385 cm reproduced to 0.03%) x Landau-Vavilov MPV. Integral rate 1.366 +/- 0.005 Hz (deterministic quadrature 1.415 Hz), within ~15% of PDG 1.5-2 Hz (VALD-02). Surface-flux measure I*A_proj*sin(theta) validated by J_horiz=pi*I_v/2 to 0.01%."
      phase: "04-muon-compton-deposited-energy-spectra"
    - summary: "Landau-Vavilov MPV computed in code (not memorized): vertical-chord xi=0.0721 MeV (PDG 0.072), Delta_p=1.232 MeV strictly below mean 1.459 MeV. Custom Landau inverse-CDF sampler (mode -0.22278); deposit=Delta_p+xi*(lambda-lambda_mode) so sampled mode=Delta_p; NOT mean, NOT Moyal. kappa=xi/T_max<0.07 for all chords -> Landau/mild-Vavilov. Guards fp-mean-not-mpv."
      phase: "04-muon-compton-deposited-energy-spectra"
    - summary: "Long near-horizontal chords importance-sampled (zenith uniform in [0,pi/2] with reweighting) so the deposit tail is resolved to ~197 MeV (66 bins >30 MeV) - the Phase-5 saturation input. Deposits on the unified phonon E_dep scale, NO quenching, no keVee/keVnr (electron recoil, zero Frenkel correction). Guards fp-angular-bias, fp-quenching-muon."
      phase: "04-muon-compton-deposited-energy-spectra"
  contract_updates:
    claims_passed: [claim-muon-spectrum, claim-muon-rate]
    acceptance_tests_passed: [test-cauchy, test-jhoriz, test-mpv, test-hetail, test-muon-rate]
    forbidden_proxies_rejected: [fp-mean-not-mpv, fp-angular-bias, fp-quenching-muon]
  state_updates:
    advance_plan: false
    update_progress: false
    record_metric:
      phase: "04"
      plan: "04-01"
      duration: 2700
      tasks: 3
      files: 9
```
