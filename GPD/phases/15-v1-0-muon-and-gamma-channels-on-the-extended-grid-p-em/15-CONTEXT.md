# Phase 15 Context — v1.0 Muon and Gamma Channels on the Extended Grid (P-EM)

**Status:** No `/gpd:discuss-phase` session was run for this phase.
**Recorded:** 2026-07-22, during autonomous roadmap execution.

## Provenance of this file

This file is **not** a transcript of a discussion with the user. It exists to record,
honestly and auditably, what the binding intent for Phase 15 actually is, given that the
user issued a standing session directive to run the roadmap to completion without
per-phase discussion unless a genuine blocker arises.

**No new user decisions were collected while writing this file.** Everything below is
transcribed from artifacts that already existed before this planning session began:
`GPD/ROADMAP.md` (the Phase 15 section, the 2026-07-22 re-scope banner, the risk register
rows for Phase 15, and the Phase-15 backtracking trigger), `GPD/REQUIREMENTS.md` (CALC-19,
CALC-20 and their traceability rows), `GPD/CONVENTIONS.md` §A/§B/§D/§E/§I/§J,
`GPD/state.json` `project_contract`, and the Phase 9/10/11/12/13 outputs. Where this file
states a decision, the source artifact is named. Nothing is invented.

Numbers appearing below under "Open items" that are labelled *planning finding* were
computed during this planning session with `/opt/anaconda3/bin/python3` against committed
code and committed data. They are recorded so the executor can reproduce them, and they are
**not** conclusions — each is explicitly handed to a plan as a question to settle.

## Decisions (LOCKED — carried from prior artifacts, not newly elicited)

1. **The five ROADMAP Phase 15 success criteria are binding verbatim.** See
   `GPD/ROADMAP.md`, section "### Phase 15: v1.0 Muon and Gamma Channels on the Extended
   Grid (P-EM)". They are the definition of done. Where a success criterion is found FALSE
   by measurement, the Phase-11/12/13 precedent applies: report it **SUPERSEDED BY
   MEASUREMENT** with the measurement attached; do not narrow a window or soften a claim
   until it becomes true.

2. **The relocation is cancelled and the v1.0 surface treatment STANDS as the answer.**
   Re-scope banner, `GPD/ROADMAP.md` 2026-07-22, driven by the user's verbatim decision
   *"Just take the approximation as was done in the paper. I don't need a very accurate
   result."* The premise of this phase **inverts**: it was "re-drive the two v1.0-solved
   channels from the VNS environment rather than the surface"; the answer under the
   re-scope is that there is nothing to re-drive them *from*. What survives is the grid
   extension and the sub-eV response physics, and nothing else.

3. **CALC-19's "replacing the v1.0 Heusser-1995 factor-2 band" clause and CALC-20's
   "replacing the v1.0 sea-level/no-overburden assumption" clause are VOID.**
   `GPD/REQUIREMENTS.md` traceability rows 140–141 carry both as re-pointed with the
   replacement clause void. The requirement *texts* still read the old way and need
   re-wording — **flagged for the orchestrator; no plan in this phase edits
   `GPD/REQUIREMENTS.md`.**

4. **No VNS ambience, no overburden, no shielding attenuation, no veto credit.**
   Veto credit is exactly **1.0 by construction** — there is no veto in an unshielded
   surface configuration (`surface_environment.veto_credit()`, Phase 9). Every retired
   relocation quantity is forbidden: the 2.92 m.w.e. overburden, the 1.41 omnidirectional
   attenuation, the NUCLEUS Table 2 ambience (5.03 cm⁻²s⁻¹; ⁴⁰K 59.6, ²³²Th 3.28, ²³⁸U
   5.65 Bq/kg), the "factor ~50" passive reduction, buildup factors, MV+COV > 99.8%, the
   COV factor ~5 at 1 keV_ee, and the Table 5 muon residual < 14 mcpd.
   `fp-shielded-quantity-leak`, binding milestone-wide.

5. **The inputs are Phase 9's re-declaration, verified rather than asserted.**
   `09-01-MUON-GAMMA-DECLARATION.md` re-declared both channels numerically identical to
   v1.0 by direct comparison against the frozen artifacts: `integral_muon_rate_Hz` =
   1.3659 exactly; ⟨ℓ⟩ = 0.384848 cm (−0.039 %); ξ = 0.072069 MeV (−0.043 %);
   Δ_p = 1.230614 MeV (−0.137 %), strictly < ⟨Δ⟩ = 1.458502 MeV; Compton edges
   1243.3573 / 1541.3115 / 2381.7571 keV (≤ 0.05 keV off).

6. **Binding path correction (`fp-wrong-muon-path`).** The real artifacts of record are
   `src/qpd_potential/muon_deposit.py`, `src/qpd_potential/muon_flux.py`,
   `src/qpd_potential/compton_source.py`, `src/qpd_potential/compton_deposit.py`,
   `data/muon_dRdEdep.csv`, `data/compton_dRdEdep.csv`. `04-01-SUMMARY.md` front-matter
   names `src/muon/deposited_spectrum.py` and `data/muon/muon_dep_spectrum.csv` —
   **neither exists**, confirmed on disk by Plan 09-01. Those paths are never cited.

7. **The four frozen v1.0 inputs are read-only in this phase.** `data/muon_dRdEdep.csv`
   and `data/compton_dRdEdep.csv` carry Phase-9 SHA-256 identity assertions verified
   against `git show HEAD:<path>` in `tests/test_env_v1_identity.py`. This phase writes
   its extended-axis outputs to `artifacts/v2.0/` and **never overwrites a `data/` file**
   (`fp-mc-rerun-drift`, `fp-header-rewrite`).

8. **Conventions are inherited, never re-chosen here.**
   - Unified phonon scale, **no quenching, no keVee/keVnr mixing** — `CONVENTIONS.md` §B.
     Both channels are **electron** recoils; that is a statement about the interaction,
     not about the energy scale, which stays unified.
   - Rate units counts·kg⁻¹·day⁻¹·keV⁻¹, per-kg normalization with the 110 g wafer
     geometry — `CONVENTIONS.md` §A.1 and §D (3 GW_th at 25 m, unchanged).
   - Trigger `P(E) = 1/(1 + (E50/E)^k)`, `E50 = 0.5 eV` exactly, k default 4.0 with a
     declared scan range [1, 12]; it **multiplies** ε ≈ 0.5 and never replaces it, and
     `P_trig ≡ 1` must reproduce the un-triggered chain bit-for-bit —
     `CONVENTIONS.md` §I. Below the 1.0 eV deposit regime boundary
     (`trigger.SUBEV_REGIME_BOUNDARY_eV`) the reported observable is a trigger
     probability, not dR/dE_rec.
   - IA broadening constants, **if and only if Plan 15-01 determines they apply**:
     ω̄ = 17.8597 meV, `2W = q²⟨u_x²⟩`, and **the rate is NEVER multiplied by e^(−2W)** —
     `CONVENTIONS.md` §J.
   - Pipeline order (Phase-12 lock): any broadening on the native axis **upstream** of the
     deposit rebin, then `R(E_rec|E_dep)`, then the trigger as an analysis efficiency on
     the deposit axis.

9. **The interpreter is `/opt/anaconda3/bin/python3`** (numpy 1.26.4, scipy 1.17.1,
   pytest 7.4.0, NCrystal 4.4.6). scipy is ABSENT from the gpd venv. The suite is
   **707 passed, 0 failed** and must stay green.

## The one genuinely open physics question this phase must settle

**Does Phase 11's IA broadening apply to these channels at all?**

σ_E = √(E_R ω̄) is a **NUCLEAR-recoil** width — it comes from the target nucleus's
zero-point momentum in the impulse approximation. Muon ionization deposits and Compton
scattering are **ELECTRON** recoils. Nothing in Phase 11 answered this, and Phase 13's
argument does not settle it either: `fold.run_neutron_fold_extended`'s own docstring says
the kernel applies to neutron elastic recoils *because they are nuclear recoils on the same
footing as CEvNS*, and adds verbatim that "Phase 15's ELECTRON-recoil channels are a
separate question and are not settled by this." Both phases explicitly handed it here.

**This is planned as an in-phase determination with a written verdict, not an assumption in
either direction.** Applying a nuclear-recoil width to electron recoils without
justification would be a real physics error; silently omitting it without argument would be
equally unjustified. Plan 15-01 owns it. Either outcome is acceptable; proceeding without
deciding is not. If it cannot be decided either way, the ROADMAP backtracking trigger
applies: **block and request scope repair**, do not apply it by default.

## Agent's Discretion

- Module decomposition, artifact layout, and test design.
- Which route satisfies ROADMAP SC1's "<1 % above 10.14 eV" — an exact re-drive of the
  Monte Carlo on the extended edges with the identical sample stream, or an index-carry of
  the frozen v1.0 bins via `legacy_grid.carried_onto_extended_axis` with only the 160 new
  bins computed. **The choice must be decided by measurement in Plan 15-02, not asserted**;
  both routes are legitimate and each has a recorded failure mode.
- The statistic used to label the statistical adequacy of a sub-eV bin, provided a bin with
  no Monte Carlo support fails it rather than merely scoring lower.
- The form of the validity-floor criterion for each channel, provided it is a published
  criterion applied to computed numbers rather than a chosen threshold.

## Deferred / Out of Scope

- **Any relocation quantity.** See Decision 4. This is the phase's principal risk
  (ROADMAP risk register, Phase 15, row 1) and SC4 is the audit that closes it.
- **Improving either v1.0 normalization.** ROADMAP SC5: the muon channel keeps its
  ~20 %-vs-PDG standing as its weakest anchor and the gamma channel keeps its factor-2
  site band. Extending the energy axis does not improve a normalization and no deliverable
  may imply that it did.
- **Any new deposit mechanism.** Delta rays entering from surrounding material, muon
  electromagnetic near-field deposits, coherent/Rayleigh scattering, phonon-mediated
  photon absorption. SC1 requires the v1.0 machinery **unchanged**; a new mechanism would
  be new physics, not a re-grid. If a validity floor implies such a mechanism dominates
  below it, that is recorded as a **named gap for Phase 16**, not modelled here.
- **Editing `GPD/REQUIREMENTS.md`** to re-word CALC-19/CALC-20. Flagged for the
  orchestrator (Decision 3).
- **Comparison against NUCLEUS Table 5's muon residual (< 14 mcpd).** Removed by the
  re-scope with its consequence stated rather than hidden: the muon channel now has **no
  external benchmark at all** beyond the v1.0 PDG sanity check.
- Any Geant4 / OpenMC / MCNP transport. `project_contract.scope.out_of_scope`.

## Open items carried into execution

- **The muon channel's directional-bias label is anchor-leg dependent and the SIGN is not
  robust.** `09-01-MUON-GAMMA-DECLARATION.md` §2.5 and §5: the channel sits **−20.61 %**
  below PDG **Leg A** (≈1 muon cm⁻² min⁻¹ × A_top = 1.7204 Hz), labelled `flatters_SB`;
  but **Leg B** (I_v ≈ 70 m⁻²s⁻¹sr⁻¹, cos²θ → 1.1350 Hz) puts it **+20.34 %** above,
  i.e. `penalizes_SB`. The two PDG statements **bracket** the adopted 1.3659 Hz. Magnitude
  ~20 % is solid; the sign is not. **Any downstream claim leaning on the sign must cite
  Leg A explicitly** and carry the bracketing disclosure with it. The gamma channel is
  `neutral` (the adopted normalization *is* the LABChico anchor) with the factor-2
  site-dependent band retained.
- **Both channels are still on the 584-bin v1.0 grid and `fold.run_fold` raises on them**
  (it asserts the channel `E_dep` centres match the loaded response matrix to 1e-6
  relative). Phases 12 and 13 each added their own extended single-channel path
  (`run_cevns_fold_extended`, `run_neutron_fold_extended`); Phase 15 must add the
  electron-recoil equivalent rather than reach for `run_fold`.
- **`shared_energy_grid` still DEFAULTS to `v1.0`.** The 744-bin extended axis (floor
  0.0999350 eV) is opt-in via `version="v2.0-ext"`. The `muon_deposit.shared_energy_grid`
  **docstring wrongly calls v2.0-ext the default**; `DEFAULT_GRID_VERSION` is authoritative
  and reads `"v1.0"`. Both MC drivers currently pin `shared_energy_grid("v1.0")` at the
  call site, and `compton_deposit.run_compton_mc` carries a comment saying in as many words
  that re-running onto the extended axis is Phase 15's job.
- **The disposition register already assigns this work to Phase 15.** Rows 30 and 47 of
  `artifacts/v2.0/legacy_grid_disposition.csv` tag both frozen CSVs
  `carried_onto_extended_axis_without_reinterpolation` and state that "the lower 160 bins
  of the extended axis carry NO DATA for this artifact — that absence is the tag, not a gap
  to fill." `legacy_grid.carried_onto_extended_axis` fills those 160 bins with **NaN, not
  zero**, precisely so an absence of measurement cannot read as a measured absence. Every
  new tracked `.csv`/`.npz` this phase produces needs its own disposition row;
  `tests/test_legacy_grid_disposition.py` enumerates via `git ls-files`.
- **Double-broadening raises no error on this path.** `fold.DoubleBroadeningError` and
  `read_broadened_provenance` exist but are wired only into `run_neutron_fold_extended`.
  If any broadening is applied to these channels it must carry the same guard, and a table
  that declares nothing is treated as **unknown**, not as unbroadened.
- **100 meV bin caveats** (`CONVENTIONS.md` §J, Phase 11): if broadening is applied,
  48.98 % of the kernel leaks below the grid floor plus 0.87 % to unphysical T < 0, and
  skewness is 0.590. **Leakage is reported, never renormalized** (`fp-renormalize-leakage`).
  The counts budget must keep `residual_retained_plus_leaked` (must close) and
  `residual_retained_only` (must miss) separate.
- **Both channels are already Monte-Carlo-statistics-limited at the v1.0 floor**
  *(planning finding, computed from the committed CSVs)*: the muon channel's per-bin
  relative MC error in its first ten bins runs 0.44–0.68 (47.5 % in the very first bin,
  16.011 ± 7.606 counts/kg/day/keV at 10.14 eV) at n = 1e9 samples; the Compton channel's
  runs 0.12–0.27 at 4e7 samples per line. Two more decades of axis at the same sample count
  will be worse, not better. Plan 15-02 must emit per-bin MC errors and a statistical
  adequacy label, and a bin with no MC support must be reported as *no support*, never as
  a rate of zero.
- **The validity floors of the two v1.0 deposit models are the phase's real disconfirming
  check, and the planning-time estimates suggest they may indict bins v1.0 already
  published.** These are estimates handed to Plan 15-01 as questions, not findings:
  - *Muon.* With ⟨dE/dx⟩ρ = 7.2925 MeV/cm, the Landau width ξ = 0.36035·ℓ MeV (ℓ in cm),
    so a Δ_p of 10.14 eV needs ℓ ≈ 4e-6 cm ≈ 40 nm and a Δ_p of 0.0999 eV needs
    ℓ ≈ 1.05e-7 cm ≈ 1 nm — **under two Ge lattice constants** (a = 5.658 Å), i.e. a few
    atomic layers. Separately, ξ falls below the Ge mean excitation energy I ≈ 350 eV for
    chords under ~10 µm, which on the same map is a deposit of order a few keV. The
    Landau–Vavilov continuous-straggling density is not the correct energy-loss
    distribution where ξ ≲ I. **If the criterion lands above 10.14 eV it indicts v1.0
    bins, and that must be reported as a finding, not suppressed.**
  - *Compton.* The Hubbell S(x, Z=32) table spans x = 0.001 … 42646 Å⁻¹, so no
    interpolator raises: a 0.1 eV recoil sits at x = 1.289e-2 Å⁻¹ where S = 0.0727, i.e.
    **0.227 % of Z** — a suppression of ~440× against free Klein–Nishina, and ~8× at
    10 eV. The machinery therefore *returns* a number down to 100 meV. Whether that number
    is physics is a different question: a 0.1 eV transfer is below the Ge band gap
    (~0.67 eV) and far below any binding energy, which is exactly where the incoherent
    impulse approximation that S(x, Z) encodes ceases to describe the scattering.
- **The Compton continuum's in-band dominance must be re-checked, not inherited.** The v1.0
  manuscript's conclusion was that muons do not preclude quiescent operation (pile-up
  occupancy Rτ ≈ 3e-5, `deposited_spectra.pileup_occupancy`) because MeV muon deposits land
  above the CEvNS band, while the environmental-gamma Compton continuum **overlaps** it and
  is the dominant reducible background. Whether that still holds two decades lower, after
  the response chain and the trigger curve, is a question this phase answers with numbers.
- **Confirmation pressure is a live failure mode in this project.** Every phase that
  planted a genuine disconfirming check found something real: Phase 11's moment check
  fired, Phase 12 refuted a roadmap success criterion by measurement, Phase 13 superseded
  another and found the resonance imprint washes out on the reported axis. Plans here must
  carry at least one disconfirming check that is **not** an algebraic identity of what it
  purports to corroborate.
- Running the suite rewrites `data/flux/*.csv` provenance headers — pre-existing churn;
  revert before committing.
