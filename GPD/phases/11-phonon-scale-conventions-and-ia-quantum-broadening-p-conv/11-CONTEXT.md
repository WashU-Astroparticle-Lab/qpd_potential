# Phase 11 Context — Phonon-Scale Conventions and IA Quantum Broadening (P-CONV)

**Status:** No `/gpd:discuss-phase` session was run for this phase.
**Recorded:** 2026-07-22, during autonomous roadmap execution.

## Provenance of this file

This file is **not** a transcript of a discussion with the user. It exists to record,
honestly and auditably, what the binding intent for Phase 11 actually is, given that the
user issued a standing session directive to run the roadmap to completion without
per-phase discussion unless a genuine blocker arises.

**No new user decisions were collected while writing this file.** Everything below is
transcribed from artifacts that already existed before this planning pass began:
`GPD/ROADMAP.md` (Phase 11 section), `GPD/REQUIREMENTS.md` (CALC-14, CALC-15),
`GPD/state.json` → `project_contract`, `GPD/literature/` (SUMMARY, PRIOR-WORK,
COMPUTATIONAL, PITFALLS), and the Phase-10 summaries. Nothing here is an invented user
preference.

<domain>
## Phase Boundary

Pin the effective phonon energy ω̄ and the Debye–Waller convention from the **real Ge
vibrational density of states** — closing a 2–3× ambiguity that propagates *linearly* into
everything sub-eV — and then stop treating the recoil spectrum as a delta function:
apply impulse-approximation (IA) quantum broadening to dR/dE_R **before** the response
chain.

Requirements: **CALC-14**, **CALC-15**.

**Site-independence note.** Phase 11 carries **no NUCLEUS anchor** and was deliberately left
byte-for-byte unchanged by the 2026-07-22 re-scope (`ROADMAP.md`, phase-disposition table,
row "10, 11"). Nothing about surfaces, shielding, overburden, or veto envelopes belongs in
this phase. Do not fold re-scope content in.

</domain>

## Decisions (LOCKED — carried from prior artifacts, not newly elicited)

1. **The five ROADMAP Phase 11 success criteria are binding verbatim.** See
   `GPD/ROADMAP.md`, section "### Phase 11: Phonon-Scale Conventions and IA Quantum
   Broadening (P-CONV)". They are the definition of done.

2. **Binding ordering constraint (ROADMAP, verbatim):** *"CALC-14 must be its **own early
   plan** (11-01) and must complete before CALC-15 (11-02) begins. Both 2W and σ_E scale
   **linearly** with ω̄, and the ⟨u²⟩-derived 12–21 meV and the 37 meV optical-phonon value
   differ by 2–3×. This is a CONVENTIONS.md decision, not an implementation detail, and it
   must not be buried inside the broadening implementation."* Encoded here as a wave
   boundary: 11-01 is wave 1 and alone in it; every other plan depends on it.

3. **Forbidden proxies are binding** (ROADMAP Phase 11 "Forbidden proxies", plus the
   milestone-wide prohibition):
   - Multiplying the rate by `e^(−2W)` — it suppresses only the zero-phonon channel and
     would erase a real signal. Milestone-wide prohibition, not a Phase-11-local one.
   - The 3-D/1-D factor-3 trap: `q²⟨u²⟩/3` instead of `q²⟨u_x²⟩`.
   - Quoting the survey's *derived* Ge numbers instead of re-deriving them in-phase.
     `GPD/literature/PRIOR-WORK.md` marks ω̄ = 12–21 meV and the σ_E table as **DERIVED**
     (in-survey), not INPUT. `REQUIREMENTS.md` line 97 restates this.
   - Building a coherent-crystal `S(q,ω)` backbone — rejected in synthesis: the coherent
     channel is extinct, `e^(−2W) ≈ 10⁻²` at 100 meV and `~10⁻²⁰` at 1 eV.

4. **Accuracy expectation is lowered milestone-wide** (user, 2026-07-22): bounded estimates
   and closed-form folds. SC5's impulse-limit justification is explicitly *"bounded ... without
   becoming a milestone pillar."* This licenses a one-off justification artifact, not a
   multiphonon-expansion programme.

<contract_coverage>
## Contract Coverage

- **CALC-14 / SC1 (deliverable):** a CONVENTIONS.md entry fixing `ω̄ ≡ ħ/(2 m_N ⟨u_x²⟩)` and
  `2W = q²⟨u_x²⟩` (1-D MSD), with `q²⟨u²⟩/3` explicitly rejected and `B = 8π²⟨u_x²⟩` quoted
  alongside. **One number, one convention, one citation** — the 12–21 vs 37 meV ambiguity
  closed by an *argued choice*, not carried as a range.
- **SC2 (acceptance signals):** VDOS reproduces the measured ceiling **37.79 meV**; the
  VDOS-integral ⟨u²⟩ agrees with the Debye value **1.34×10⁻³ Å²** within ~1.5×; 2W at
  100 meV lands at **≈4.7–8.3**, consistent with `q(100 meV) = 116 keV/c = 58.9 Å⁻¹`.
- **CALC-15 / SC3 (deliverable):** `σ_E = √(E_R ω̄)` **re-derived in-phase**, reproducing
  `σ_E/E_R = 1/√(2W)`: 35–46% at 100 meV, **15.5–20.5% at the 0.5 eV threshold**, 11–15% at
  1 eV, 1.1–1.5% at 100 eV, negligible above; plus the quadrature sum with the Phase-10
  counting floor (~22–26% at 0.5 eV), since both act on the trigger sigmoid at the same energy.
- **SC4 (acceptance signal):** the Gaussian convolution applied to dR/dE_R **before** the
  response chain, conserving counts to **≤1e-3**, and vanishing correctly — the broadened
  spectrum reproduces the frozen v1.0 result above ~10 eV to **<1%**.
- **SC5 (bounded deliverable):** a justification artifact demonstrating via the f-sum rule
  that `S(q,ω) → δ(ω − q²/2M)` is reached by ~100 meV, quantifying the residual `O(1/2W)`
  correction in the bottom bin, and recording why the rate is never multiplied by `e^(−2W)`.
- **False progress to reject:** any of the four forbidden proxies in Decision 3; a σ_E table
  transcribed from `PRIOR-WORK.md` rather than recomputed; a "count conservation ≤1e-3"
  claim obtained by renormalizing away the sub-floor tail of the convolution.

</contract_coverage>

<user_guidance>
## User Guidance To Preserve

The only standing user guidance that reaches this phase is procedural and milestone-wide;
**no phase-specific user decision exists.**

- **Standing directive (session-level):** run the roadmap to completion without per-phase
  discussion unless a genuine blocker arises.
- **Accuracy expectation, verbatim (2026-07-22):** *"Just take the approximation as was done
  in the paper. I don't need a very accurate result."* Reaches Phase 11 only through the
  milestone-wide instruction to prefer bounded estimates and closed-form folds.
- **Evidence discipline (project-standing):** every quoted number traceable to a locally
  frozen artifact via a recorded, reproducible command. `WebFetch` produced two verified
  factual errors in Phase 8 and **is not a quote source**. Newly frozen external sources
  follow the `data/external/` pattern: raw + normalized + MANIFEST with SHA-256.
- **Interpreter:** `/opt/anaconda3/bin/python3` for anything importing `qpd_potential`
  (numpy 1.26.4, scipy 1.17.1, pytest 7.4.0). **scipy is absent from the gpd venv.**
- **Suite state:** 518 passed / 0 failed. Keep it green. Running the suite rewrites
  `data/flux/*.csv` provenance headers — pre-existing churn; revert before committing.

</user_guidance>

<decisions>
## Methodological Decisions

### VDOS source and freezing

- **Primary:** NCrystal `Ge_sg227.ncmat` (Nelin & Nilsson, PRB 5, 3151 (1972)) —
  `GPD/literature/COMPUTATIONAL.md` records NCrystal 4.4.6 with a **native osx-arm64 wheel**
  (`ncrystal_core-4.4.6-py3-none-macosx_11_0_arm64.whl`, Apache-2.0, no build) and a bundled
  VDOS spanning **3.77–37.79 meV**.
- **Cross-check:** DarkELF `data/Ge/Ge_pDoS.dat` (pure Python, no build).
- Neither package is currently importable under `/opt/anaconda3/bin/python3` (checked
  2026-07-22: `NCrystal`, `ncrystal`, `darkelf` all absent). Acquisition is a genuine
  execution prerequisite, carried in `tool_requirements` + `researcher_setup` on 11-01.
- The VDOS is **frozen to `data/external/ge_vdos/`** (raw + normalized + MANIFEST with
  SHA-256) so the derived numbers stay reproducible without the package installed.

### Temperature limit for ⟨u_x²⟩

- **T → 0 zero-point only.** Justified physically: the QPD operates at mK against
  θ_D(Ge) ≈ 374 K, so `coth(ħω/2k_BT) → 1` to far better than the phase's tolerance. The
  general form `⟨u_x²⟩ = (ħ/2m_N) ∫ g(ω)/ω · coth(ħω/2k_BT) dω` must still be written down
  and the T→0 reduction stated, not silently assumed.

### 1-D projection

- Ge is cubic (spacegroup 227), so the mean-square-displacement tensor is **isotropic** and
  `⟨u_x²⟩ = ⟨u²⟩/3` is *exact by symmetry*, not an approximation. The forbidden `/3` trap is
  applying that factor a **second time**, inside `2W`. State both facts in the same paragraph
  of the CONVENTIONS entry so the distinction cannot be lost.

### Nuclear mass

- Natural abundance-weighted Ge, consistent with the Phase-7 nuclear-data lock
  (abundance-weighted `T_max/E_n = 0.0536`). The isotope choice must be stated explicitly
  in the CONVENTIONS entry, because ω̄ ∝ 1/m_N.

### Broadening lineshape

- Symmetric **Gaussian** of width `σ_E = √(E_R ω̄)`, per `PRIOR-WORK.md` §"Recommended
  implementation" and the Sears PRB 35, 2038 (1987) IA framework. The true `S(q,ω)` is
  asymmetric at low 2W; the resulting error is the `O(1/2W)` residual SC5 must quantify.

### Wiring point

- Broadening acts on `dR/dT` on the **recoil** axis, upstream of
  `fold.rebin_cevns_to_edep_grid` and therefore upstream of `R(E_rec|E_dep)`. It is exposed
  as an explicit switch so that switching it off reproduces the frozen v1.0 chain
  **bit-identically** — the same fail-safe discipline Phase 10 adopted when it left
  `shared_energy_grid` defaulting to `v1.0`.

### Agent's Discretion

- Module decomposition, test layout, quadrature scheme for the VDOS integral, and the
  numerical convolution method (direct kernel vs FFT), provided the analytic Debye oracle
  below passes.
- Which of NCrystal / DarkELF carries the headline number, provided the choice is argued
  from the data and the other is reported as the cross-check.
- Whether the broadening switch defaults on or off, provided the v1.0 bit-identity test
  exists either way and the default is recorded for Phase 12.

</decisions>

<assumptions>
## Physical Assumptions

- **Impulse approximation valid across the whole window.** Justification: `2W = E_R/ω̄ ≈ 4.7–8.3`
  at the 100 meV floor and grows linearly with E_R; `COMPUTATIONAL.md` §3 concludes the
  crystal-coherent regime (`2W ≲ 1`) lives below ~21 meV, under the floor. | If wrong at the
  bottom bin, the Gaussian width and the whole sub-eV signal shape are wrong there; SC5 is
  the check that bounds it.
- **Harmonic lattice.** Justification: standard for the Debye–Waller/MSD formalism and for
  the VDOS itself. | Anharmonicity would shift ⟨u_x²⟩; at mK the zero-point-dominated regime
  is the most favourable case for harmonicity.
- **Gaussian (symmetric) IA lineshape.** Justification: leading IA result, Sears 1987. | The
  true lineshape is asymmetric at 2W of a few; the error is the `O(1/2W)` ≈ 12–21% residual
  in the bottom bin.
- **`σ_E = √(E_R ω̄)` is a NUCLEAR-recoil width.** The muon and Compton channels are
  ELECTRON recoils. `state.json.project_contract.scope.unresolved_questions` records this as
  **open and assigned to Phase 15**, not Phase 11. Phase 11 must not silently apply the
  broadening to electron-recoil channels, and must not resolve the question either.

</assumptions>

<limiting_cases>
## Expected Limiting Behaviors

- **ω̄ → 0 (or σ_E → 0):** the convolution reduces to the identity and the broadened spectrum
  must equal the input **bit-identically**.
- **E_R ≫ ω̄ (above ~10 eV):** `σ_E/E_R = √(ω̄/E_R) → 0`; the broadened spectrum must reproduce
  the frozen v1.0 result to **<1%** (SC4). At 10 eV with ω̄ ≈ 21.5 meV this width is ≈4.6%,
  so <1% on the spectrum is a real, non-vacuous test.
- **Debye VDOS `g(ω) = 3ω²/ω_D³` fed to the ⟨u_x²⟩ quadrature:** must return the closed form
  `⟨u²⟩_3D = 9ħ²/(4 m_N k_B θ_D)`, i.e. **4.02×10⁻³ Å²** at θ_D = 374 K, and
  `⟨u_x²⟩ = 1.34×10⁻³ Å²`. This is an **analytic oracle** independent of any Ge data file and
  is the single strongest guard against the factor-3 trap and a VDOS normalization error.
- **q → 0:** `2W → 0`, `e^(−2W) → 1` (coherent limit). Outside the window; quoted only to show
  where the window is *not*.

</limiting_cases>

<anchor_registry>
## Active Anchor Registry

- **NCrystal `Ge_sg227.ncmat`** (Nelin & Nilsson, PRB 5, 3151 (1972))
  - Why it matters: the measured Ge VDOS; the arbiter that closes the 12–21 vs 37 meV ambiguity
  - Carry forward: planning, execution, verification, writing
  - Required action: read, use, compare, cite
- **DarkELF `data/Ge/Ge_pDoS.dat`** (github.com/tongylin/DarkELF; arXiv:2104.12786)
  - Why it matters: independent digitization of the Ge phonon DOS; the ⟨u_x²⟩ cross-check
  - Carry forward: planning, execution, verification
  - Required action: use, compare
- **Sears, Phys. Rev. B 35, 2038 (1987)**, DOI 10.1103/PhysRevB.35.2038
  - Why it matters: the IA / final-state framework behind `σ_E = √(E_R ω̄)`
  - Carry forward: execution, writing
  - Required action: read, use, cite
- **Campbell-Deem et al., PRD 106, 036019 (2022)**
  - Why it matters: the published IA criterion `q ≫ √(2 m_d ω̄_d)` ⇔ `E_R ≫ ω̄`
  - Carry forward: execution, verification, writing
  - Required action: use, cite
- **SuperCDMS, APL 113, 092101** — Ge displacement threshold 19.7 ⁺⁰·⁶₋₀·₅ eV, no defect below ~6 eV
  - Why it matters: strengthens the unified phonon scale in-window (no defect-storage channel
    opens anywhere in the 0.1 eV–6 eV band)
  - Carry forward: execution, writing
  - Required action: cite
- **Frozen v1.0 spectra above 10 eV** (`artifacts/stage1/`, `data/flux/reactor_flux_v1.0.csv`)
  - Why it matters: the vanishing-limit regression target for SC4 (<1%)
  - Carry forward: execution, verification
  - Required action: use, compare
- **Phase-10 counting floor** — `GPD/phases/10-.../10-05-COUNTING-FLOOR.md` (15.9% / 14.2% at
  0.5 eV; 35.6% / 31.6% at 0.1 eV; best case, no noise sources)
  - Why it matters: the quadrature partner in SC3; both act on the trigger sigmoid at 0.5 eV
  - Carry forward: execution, writing
  - Required action: use, compare
- **`GPD/literature/PRIOR-WORK.md`, SUMMARY.md, COMPUTATIONAL.md**
  - Why it matters: the *targets* to be reproduced — and explicitly **DERIVED**, so they are
    comparison values, never quotable sources
  - Carry forward: planning, verification
  - Required action: compare, avoid (as a citation)

</anchor_registry>

<skeptical_review>
## Skeptical Review

**Planning finding, load-bearing for SC2 — the "independent momentum-transfer route" is not
independent.** SC2 asks that `2W ≈ 4.7–8.3` at 100 meV be *"consistent with the independent
momentum-transfer route q(100 meV) = 116 keV/c = 58.9 Å⁻¹."* With `q² = 2 m_N E_R` and
`ω̄ ≡ ħ/(2 m_N ⟨u_x²⟩)`, the two expressions are algebraically **identical**:
`2W = q²⟨u_x²⟩ = 2 m_N E_R ⟨u_x²⟩ = E_R/ω̄`. The q-route is therefore a **units-and-arithmetic
cross-check, not independent physics**, and reporting it as corroboration would be exactly the
confirmation-pressure failure mode this project has already recorded twice. Plans must label it
as an identity check. The *genuinely* independent legs of SC2 are the measured VDOS ceiling
(37.79 meV) and the VDOS-vs-Debye ⟨u²⟩ comparison. Likewise, `2W ∈ [4.76, 8.33]` ⟺
`ω̄ ∈ [12.0, 21.0] meV` exactly, so SC2's third clause is not independent of SC1's ω̄ either.

- **Weakest anchor:** the `ω̄ = 12–21 meV` band itself. `PRIOR-WORK.md` marks it **DERIVED**
  (in-survey, confidence MED) from a Debye-model ⟨u_x²⟩ with an experimental-`B` upper end —
  i.e. *not* from the real VDOS this phase is supposed to use. The whole point of CALC-14 is
  that this band may not survive contact with the measured VDOS.
- **Unvalidated assumptions:** that the measured VDOS integral lands inside SC2's ~1.5× window
  of the Debye ⟨u_x²⟩; that a symmetric Gaussian is adequate at 2W ≈ 5; that the T→0 reduction
  is exact enough at mK (almost certainly yes, but it is currently asserted, not shown).
- **Competing explanation:** the 37 meV optical-phonon value is not *wrong* — it is a different
  quantity (zone-centre LO energy) wearing the same symbol. If the argued choice is made badly,
  the phase will look like it resolved a physics ambiguity when it only resolved a notation
  collision. `SUMMARY.md` line 37 already says as much: *"The only real disagreement is the
  label ω̄."* The CONVENTIONS entry must say this explicitly rather than claiming a physics win.
- **Disconfirming checks (must be run, failure is informative):**
  1. **Analytic Debye oracle.** Feed the quadrature `g(ω) = 3ω²/ω_D³` at θ_D = 374 K; it must
     return `⟨u²⟩_3D = 9ħ²/(4 m_N k_B θ_D)` to <0.1%. Failure ⇒ factor-3 or normalization bug,
     independent of any Ge data.
  2. **NCrystal vs DarkELF ⟨u_x²⟩.** Two independent digitizations of the same measurement.
     A >10% disagreement means one is misnormalized; it cannot be averaged away.
  3. **ω̄ outside 12–21 meV.** If the measured VDOS gives an ω̄ outside the survey band, the
     phase **reports the VDOS value and marks the survey band superseded**. It does not tune
     toward the band, and it does not re-derive until the band is hit. SC2's ~1.5× tolerance on
     ⟨u_x²⟩ maps to `ω̄ ∈ [14.3, 32.2] meV`, which is *wider* than 12–21 meV — so landing
     outside is a live possibility, not a hypothetical.
  4. **Sub-floor mass leakage at 100 meV.** With `σ_E/E_R ≈ 35–46%`, a Gaussian centred on the
     bottom bin puts a non-negligible fraction of its mass **below the 0.0999350 eV grid floor
     and below zero** (E = 0 sits ≈2.2σ below the centre at ω̄ ≈ 21.5 meV, i.e. ~1.5% of the
     mass at E < 0). Count conservation to ≤1e-3 across the retained grid is therefore **not**
     automatic. If it comes out clean without a leakage line item, something has been
     renormalized away. Report the leaked fraction; never rescale to hide it.
- **False progress to reject:** a σ_E table that matches `PRIOR-WORK.md` because it was copied
  from it; a "consistent with the independent q-route" claim that is an identity; a conservation
  pass obtained by renormalization; treating `e^(−2W) ≈ 10⁻²` as a rate suppression rather than
  as evidence that the coherent channel is extinct and the strength has moved into the
  multiphonon continuum.

</skeptical_review>

<deferred>
## Deferred Ideas

- **Does the IA broadening apply to the muon and Compton (electron-recoil) channels?**
  Explicitly assigned to **Phase 15** by `state.json.project_contract` unresolved questions.
  Phase 11 neither applies it there nor answers the question.
- **A full multiphonon `S(q,ω)` for Ge contracted with the CEvNS matrix element**
  (`PRIOR-WORK.md` "Front 1"). Out of scope by the project contract: *"Coherent-crystal
  S(q,omega) modelling backbone"* is listed under `out_of_scope`, and SC5 bounds the IA
  justification to a one-off artifact.
- **Turning the broadening on in production and reporting the signal spectrum.** That is
  **Phase 12** (CALC-25, VALD-10). Phase 11 delivers the machinery, the convention, and the
  regression proof.
- **Fixing `energy_scale.n_qp_yield`'s missing pair-breaking threshold** (Phase-10 finding:
  ≈0.018 quasiparticles at 0.1 eV, 6.89 µeV against a ~190 µeV Al trap gap; the bottom two
  decades are a mean-field extrapolation). Flagged by Phase 10 as *"aware of but not required
  to fix"*. Phase 11 does not touch it; the broadening sits upstream of the response chain, so
  the two are separable.

</deferred>

---

_Phase: 11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv_
_Context recorded: 2026-07-22 (no user decisions elicited; transcribed from prior artifacts)_
