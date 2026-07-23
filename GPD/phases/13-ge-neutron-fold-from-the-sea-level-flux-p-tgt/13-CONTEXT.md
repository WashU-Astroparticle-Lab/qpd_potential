# Phase 13 Context — Ge Neutron Fold from the Sea-Level Flux (P-TGT)

**Status:** No `/gpd:discuss-phase` session was run for this phase.
**Recorded:** 2026-07-22, during autonomous roadmap execution.

## Provenance of this file

This file is **not** a transcript of a discussion with the user. It exists to record,
honestly and auditably, what the binding intent for Phase 13 actually is, given that the
user issued a standing session directive to run the roadmap to completion without
per-phase discussion unless a genuine blocker arises.

**No new user decisions were collected while writing this file.** Everything below is
transcribed from artifacts that already existed before this planning session began:
`GPD/ROADMAP.md` (Phase 13 section and the 2026-07-22 re-scope banner),
`GPD/REQUIREMENTS.md` (CALC-18 and its traceability rows), `GPD/CONVENTIONS.md` §A/§B/§D/§I/§J,
`GPD/state.json` `project_contract`, and the Phase 7/9/10/11/12 outputs. Where this file
states a decision, the source artifact is named. Nothing is invented.

## Decisions (LOCKED — carried from prior artifacts, not newly elicited)

1. **The five ROADMAP Phase 13 success criteria are binding verbatim.** See
   `GPD/ROADMAP.md`, section "### Phase 13: Ge Neutron Fold from the Sea-Level Flux (P-TGT)".
   They are the definition of done. Where a success criterion is found FALSE by
   measurement, the Phase-11/12 precedent applies: report it SUPERSEDED BY MEASUREMENT
   with the measurement attached; do not narrow the window until the claim becomes true.

2. **The input is the rough sea-level neutron flux, not a post-shield fluence.**
   Re-scope banner, `GPD/ROADMAP.md` 2026-07-22, driven by the user's verbatim decision
   *"Just take the approximation as was done in the paper. I don't need a very accurate
   result."* **CALC-12 (φ_post recovery by regularized inversion) and the VALD-11 two-band
   CaWO₄/Al₂O₃ ratio gate are orphaned by design and MUST NOT be planned or executed.**
   `GPD/REQUIREMENTS.md` traceability rows carry both as *Unmet by design (2026-07-22
   re-scope)*.

3. **The whole channel carries `accuracy_label = order_of_magnitude`,** inherited at the
   point of definition from `09-02-NEUTRON-DECLARATION.md` §3.4. No acceptance test on
   this channel may demand better than order-of-magnitude agreement. Forbidden proxy
   `fp-precision-inflation` is binding milestone-wide.

4. **The operative flux column is `phi_default` = `phi_hi` (OUTDOOR sea level).**
   `09-02-NEUTRON-DECLARATION.md` §4: `phi_lo = phi_default/5` is the **INDOOR** leg and is
   **not an error bar** for an unshielded surface wafer. Using it, or the band midpoint,
   as a central value would cut this background by a factor 5 — the single largest
   flattering move available in this phase. `fp-indoor-band-as-central`.

5. **The kinematic-compression physics is retained; the site physics is not.**
   Re-scope banner: the resonance imprint and T_max/E_n = 0.0536 are properties of
   germanium, not of the site. ROADMAP SC3 and SC4 survive the re-scope untouched.
   `fp-mass-scaled-target` is retained as a standing prohibition though now vacuous — no
   NUCLEUS residual enters the pipeline anywhere.

6. **Conventions are inherited, never re-chosen here.**
   - Unified phonon scale, **no quenching / no Lindhard** — `CONVENTIONS.md` §B; the frozen
     elastic table's own header records `recoil_axis = keV_nr (unified phonon scale, NO
     Lindhard/quenching)`.
   - Rate units counts·kg⁻¹·day⁻¹·keV⁻¹, per-kg normalization with the 110 g wafer geometry
     — `CONVENTIONS.md` §A.1 and §D.
   - IA broadening `ω̄ = 17.8597 meV`, `2W = q²⟨u_x²⟩`, **the rate is NEVER multiplied by
     e^(−2W)** — `CONVENTIONS.md` §J.
   - Trigger `P(E) = 1/(1 + (E50/E)^k)`, `E50 = 0.5 eV` exactly, **multiplies** ε ≈ 0.5 and
     never replaces it — `CONVENTIONS.md` §I.
   - Pipeline order: IA broadening on the recoil axis **upstream** of the deposit rebin,
     then `R(E_rec|E_dep)`, then the trigger as an analysis efficiency. Phase 12 lock.

7. **Deferral policy for CALC-24 (>20 MeV TENDL splice) is decided by measurement, not
   inherited.** `09-02-NEUTRON-DECLARATION.md` §6.2 records that the Phase-7 deferral
   rationale (shield attenuation of the >10 MeV tail) is **VOID at the surface**. ROADMAP
   SC5 states a bound is sufficient and the splice remains follow-up scope. This phase
   therefore **bounds and does not close** — but the deferral is made conditional on the
   measured bound, not asserted: if the bound exceeds the channel's own
   order-of-magnitude label, the phase escalates rather than defers.

## Agent's Discretion

- Module decomposition, artifact layout, and test design.
- The native recoil axis (node density, span), subject to the anchored-quadrature and
  convergence requirements in the plans.
- **The sub-5 eV kernel disposition** — ROADMAP SC5 explicitly offers two routes
  (NCrystal `Ge_sg227` splice at 5 eV with the discontinuity measured, **or** truncation at
  the last defended energy with the omission documented, on the Phase-7 gap-D1 precedent).
  Either is acceptable; the choice must be argued from what is actually measured in-phase,
  and the ENDF free-atom σ_el is never used as physics below 5 eV under either route.
- The statistic used to demonstrate resonance imprint, provided it is falsifiable — a
  smooth spectrum must fail the test, not merely score lower.
- Which comparison basis carries the SC4 kinematic-compression statement, provided the
  direction is measured rather than asserted.

## Deferred / Out of Scope

- **CALC-12** (φ_post inversion) and **VALD-11** (two-band ratio gate). Orphaned by design.
  No regularized differentiation, no figure digitization, no multi-target
  over-determination test.
- **CALC-24** (TENDL-2023 splice above the 20 MeV ENDF ceiling). Bounded here, not closed.
- **Phase 14** work: thermal capture, (n,γ) cascade recoils, ⁷¹Ge EC lines, Ge inelastic.
  Φ_th = 2.767075×10⁻³ cm⁻² s⁻¹ exists as a named Phase-9 quantity and is **Phase 14's**
  input, not this phase's.
- Any Geant4/OpenMC/MCNP transport. `project_contract.scope.out_of_scope`.
- Any NUCLEUS shielding attenuation, post-shield fluence, overburden, buildup factor,
  veto or multiplicity credit. Veto credit is exactly **1.0 by construction**.
  `fp-shielded-quantity-leak`.

## Open items carried into execution

- **The eV–keV spectral shape of the neutron flux has NO independent validation and none
  is obtainable in this environment.** The only independent cross-check the channel owns is
  a single >10 MeV integral agreeing to −8.77 % untuned; Gordon's differential coefficients
  are paywalled. Two spectra can share that integral and differ badly at eV–keV — which are
  exactly the energies that set the Ge recoil rate in the RoI. The `order_of_magnitude`
  label is load-bearing, not decorative.
- **ROADMAP SC4's compression direction is an assertion this phase must test, not adopt.**
  Phases 11 and 12 between them found four roadmap clauses that were algebraic identities of
  what they purported to corroborate, and Phase 12 measured one success criterion to be
  false as written. SC4 states that T_max/E_n = 0.0536 (Ge) against 0.0215 (W) makes Ge the
  *worse* target. In the pure epithermal limit (φ ∝ 1/E, σ constant) the kinematic factor
  cancels **exactly** out of dR/dT — verified analytically during planning:
  ∫_{T/f}^∞ (C/E)·σ/(fE) dE = Cσ/T, independent of f. Since the sea-level spectrum is flat
  in lethargy to a factor 1.390 over 1 eV – 10 keV (`09-02-NEUTRON-DECLARATION.md` §5), that
  limit is close to the regime that actually feeds the RoI. Plan 13-02 owns the adjudication.
- **Two mechanical traps inherited from Phase 12** are carried as tests here:
  `fold.run_fold` raises on still-584-bin inputs (a neutron-only extended path is needed,
  analogous to `run_cevns_fold_extended`); and feeding an already-broadened artifact with
  `broaden=True` double-broadens with **no error raised anywhere**.
- **`shared_energy_grid` still DEFAULTS to `v1.0`.** The extended 744-bin axis is opt-in via
  `version="v2.0-ext"`. The `muon_deposit.shared_energy_grid` docstring wrongly calls
  v2.0-ext the default; `DEFAULT_GRID_VERSION` is authoritative and reads `"v1.0"`.
- **100 meV bin caveats** (`CONVENTIONS.md` §J, Phase 11): 48.98 % kernel leakage below the
  floor, skewness 0.590. Leakage is reported, never renormalized.
- Running the suite rewrites `data/flux/*.csv` provenance headers — pre-existing churn;
  revert before committing.
- `REQUIREMENTS.md` CALC-18 text still reads "from the recovered φ_post(E_n)" and needs
  re-wording. **Flagged for the orchestrator; no plan in this phase edits that file.**
