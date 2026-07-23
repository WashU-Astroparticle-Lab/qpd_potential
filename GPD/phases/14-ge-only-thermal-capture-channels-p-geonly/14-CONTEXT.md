# Phase 14 Context — Ge-Only Thermal-Capture Channels (P-GEONLY)

**Status:** No `/gpd:discuss-phase` session was run for this phase.
**Recorded:** 2026-07-23, during autonomous roadmap execution.

## Provenance of this file

This file is **not** a transcript of a discussion with the user. It exists to record, honestly
and auditably, what the binding intent for Phase 14 actually is, given that the user issued a
standing session directive to run the roadmap to completion without per-phase discussion unless
a genuine blocker arises.

**No new user decisions were collected while writing this file.** Everything in the *Decisions*
section below is transcribed from artifacts that already existed before this planning pass, or
computed during planning from committed data. Nothing is invented, and no user preference is
attributed that was not already on record.

<domain>
## Phase Boundary

The two backgrounds that are structurally invisible in any CaWO₄/Al₂O₃ budget — **prompt (n,γ)
cascade recoils** and the **⁷¹Ge electron-capture lines** — are carried into the CEvNS RoI as
**bounds with stated provenance** rather than as omissions, so that a channel landing on top of
the signal is a number with an error bar rather than a blank.

Re-scoped 2026-07-22: driven from the **rough surface neutron estimate** and **bounded rather
than quantified**. Accuracy is explicitly not required. The B₄C ¹⁰B(n,α)⁷Li 478 keV inheritance
was removed (there is no liner in an unshielded configuration) and φ_th is re-pointed to the
sea-level thermal component.

Requirements: **CALC-23** *(reduced to bounds by the 2026-07-22 re-scope; the requirement text
still reads "Gated on the in-shield thermal flux φ_th, which NUCLEUS does not publish" and needs
re-wording — **flagged for the orchestrator, not edited by any plan in this phase**)*.

Adjacent-scope deliverable with no CALC ID of its own: ROADMAP SC5, Ge inelastic
(⁷⁴Ge 596 keV, ⁷²Ge 834 keV) at least **bounded and named** rather than silently omitted.

</domain>

<contract_coverage>
## Contract Coverage

- **Prompt (n,γ) cascade recoil bound** — an upper bound on the channel inside the RoI, carrying
  the `order_of_magnitude` label of its driving flux. Success is a **number with a stated
  derivation**, not a spectrum.
- **⁷¹Ge EC line inventory** — M / L / K at 158.7 ± 1.4 / 1298.5 / 10368.3 eV, with the M line
  folded through the response chain onto the extended axis, and with the **activation and decay
  scenario stated explicitly** rather than an implied steady state.
- **φ_th disposition** — explicit, carried into Phase 16. Phase 9 delivered
  **Φ_th = 2.767075×10⁻³ cm⁻² s⁻¹** (0.01–0.5 eV, cadmium cutoff), so ROADMAP SC4 discharges on
  branch (a) — the flux was sourced, not gapped. The never-zero rule remains in force for every
  *derived* quantity in this phase.
- **Cross-section provenance** — sourced and verified from a locally frozen artifact via a
  recorded, reproducible command, never asserted.
- **False progress to reject:** reporting the capture channel as zero when a number was simply
  not computed; presenting the single-γ kinematic limit as the cascade answer; presenting a bound
  as a quantification; quoting either channel to better than the Phase-9 `order_of_magnitude`
  label it is driven from.

</contract_coverage>

<user_guidance>
## User Guidance To Preserve

Standing project directives already on record, restated here because they are load-bearing for
this phase specifically:

- **"Just take the approximation as was done in the paper. I don't need a very accurate result."**
  (user, 2026-07-22, the re-scope decision). This phase **bounds**; it does not quantify.
- **Evidence discipline.** Every quoted number must be traceable to a locally frozen artifact via
  a recorded, reproducible command. **`WebFetch` is not a quote source** — two verified factual
  errors traced to it in Phase 8.
- **Interpreter.** `/opt/anaconda3/bin/python3` (numpy 1.26.4, scipy 1.17.1, pytest 7.4.0,
  NCrystal 4.4.6). **scipy is absent from the gpd venv.**
- **Suite stays green** (784 passed, 0 failed). Running the suite rewrites `data/flux/*.csv`
  provenance headers — pre-existing churn, revert before committing.
- **Confirmation pressure is a live failure mode in this project and checking keeps paying.**
  Phase 11's moment check fired; Phase 12 refuted a roadmap success criterion by measurement;
  Phase 13 superseded another and found the resonance imprint washes out on the reported axis;
  Phase 15 found the "too small to resolve" argument would have been false and that the
  Landau–Vavilov validity floor indicts 209 of 584 published v1.0 bins. **At least one
  disconfirming check in this phase must not be an algebraic identity of what it corroborates.**

</user_guidance>

<decisions>
## Methodological Decisions (LOCKED — carried from prior artifacts, not newly elicited)

### The five ROADMAP Phase 14 success criteria are binding verbatim

See `GPD/ROADMAP.md`, section "### Phase 14: Ge-Only Thermal-Capture Channels (P-GEONLY)".
They are the definition of done. SC2 in particular fixes the shape of the answer: *"bounded,
not quantified … the single-γ limit is never presented as the cascade answer."*

### Driving flux — inherited, not re-sourced

- **Φ_th = 2.767075×10⁻³ cm⁻² s⁻¹** (0.01–0.5 eV, cadmium cutoff) is **Phase 9's product**, from
  `09-02-NEUTRON-DECLARATION.md` §5, and Phase 13's closeout explicitly hands it here labelled as
  Phase 9's, not Phase 13's. It is **not** re-derived in this phase.
- The differential flux comes from the same three-part path Phase 13 used: the sub-eV table
  `data/ambient_neutron_thermal_v2.0.csv` (0.01–1 eV), the committed
  `data/ambient_neutron_flux_v1.1.csv` (10.14 eV – 197 MeV), and the pinned PARMA driver
  `src/qpd_potential/parma_neutron_flux.py` evaluated directly across the 1 – 10.14 eV gap that
  neither table covers. Phase 13 closed that gap by evaluating the driver at every quadrature
  node; this phase does the same and does **not** interpolate across it.
- **`phi_default == phi_hi` (OUTDOOR).** `phi_lo = phi_default/5` is an **indoor/building
  attenuation stand-in, not an error bar** (Phase 9 §4). Using it would cut the background by a
  factor 5 and improve S/B by the same factor. It is not used, not emitted, not averaged.
- The channel inherits `accuracy_label = order_of_magnitude` and Phase 13's measured finding that
  the eV–keV differential **flux shape is UNBOUNDED**: two perturbations invisible to the only
  independent cross-check moved the in-RoI elastic rate by +41.33 % and −16.31 %.

### Cross-section source — already local, already frozen

Measured during planning, not assumed: the ENDF/B-VIII.0 evaluated files for all five Ge isotopes
are **already committed** at `data/endf/raw/n_*.dat`, and the Lib80x ACE files at
`data/endf/ace/32*.800nc`. Both carry MT=102. ROADMAP SC1's "new acquisition" is therefore mostly
already discharged by Phase 7's acquisition, and the phase reuses `src/nuclear/parse_endf_nGe.py`
and the `endf 0.1.12` reader rather than building a second path.

**The trap, measured and recorded before planning proceeded:** `MF=3 MT=102` in the raw ENDF
files is **identically zero** through the resolved-resonance region — in the RRR the capture
cross section lives in File 2 as resonance parameters, and MF=3 carries only the background.
Reading MF=3 MT=102 and reporting σ_th = 0 would produce exactly the forbidden "capture channel
is zero" outcome from a file that does contain the physics. The **pre-reconstructed,
Doppler-broadened Lib80x ACE files at 293.6 K are the operative source**, which is the same
resolution Phase 7 reached for elastic and for the same reason.

### Isotopic abundances — frozen

`params.GE_ISOTOPES` (Phase-7 nuclear-data lock, IUPAC): ⁷⁰Ge 0.2057, ⁷²Ge 0.2745, ⁷³Ge 0.0775,
⁷⁴Ge 0.3650, ⁷⁶Ge 0.0773. `N_Ge = 8.29×10²⁴ atoms/kg` (CONVENTIONS §D). Never transcribed from
prose.

### Conventions

- **CONVENTIONS §D** — 110 g wafer geometry, per-kg rate normalization (counts·kg⁻¹·day⁻¹).
- **CONVENTIONS §I** — the trigger curve is an **analysis efficiency multiplied on top of**
  ε ≈ 0.5, Hill form, E50 = 0.5 eV exactly, k default 4.0 with the [1, 12] sensitivity obligation.
  It never replaces ε.
- **CONVENTIONS §J** — ω̄ = 17.8597 meV locked; **the rate is never multiplied by exp(−2W)**.
- **CONVENTIONS §B** — unified phonon scale, **no quenching**, no keV_ee ↔ keV_nr mixing.

### IA broadening applies to one channel here and not the other

- **Prompt (n,γ) cascade recoils are NUCLEAR recoils.** The Phase-11 impulse-approximation width
  σ_E = √(E_R ω̄) is legitimate for them on the same footing Phase 13 used for elastic recoils.
- **The ⁷¹Ge EC lines are ELECTRONIC.** Phase 15 established with a number — not by assertion —
  that the nuclear kernel does not transfer: the electron analogue's own validity criterion
  2W_e = T/ω̄_e = 0.1574 < 1 fails, and ω̄_e ≥ 0.634740 eV = 35.540 × ω̄ from the uncertainty
  principle over the Ge covalent bond, so transplanting the nuclear kernel would understate the
  width by 5.96×. **The same reasoning applies here and must be stated, not inherited silently.**
- `BROADENING_DEFAULT = False`; **double-broadening raises no error by itself** — the
  `DoubleBroadeningError` guard Phase 13 installed in `fold.run_neutron_fold_extended` reads a
  `broadened_provenance` marker, and any new table this phase emits must carry one.

### Grid and response chain

`shared_energy_grid(version="v2.0-ext")` = 744 bins, floor 0.0999350 eV. **`v1.0` remains the
default**; the extended axis is opt-in. Response matrices
`artifacts/v2.0/response_matrix_{TaAl,AlHf}_ext.npz`, 161 E_rec × 744 E_dep, columns summing to 1.
Interpolators **raise** outside their domains. Every new tracked `.csv`/`.npz` needs a disposition
row in `artifacts/v2.0/legacy_grid_disposition.csv`.

### Agent's Discretion

- Module decomposition, artifact layout, test design, quadrature node counts.
- Whether the capture-rate fold is written into `neutron_recoil.py` or a new module, subject to
  not shifting line numbers that `tests/test_interpolator_bounds.py` keys by `file:line`
  (Phase 13 was bitten by this three times).
- The exact form of the cascade-multiplicity scaling statement, provided the single-γ limit is
  never presented as the cascade answer.
- Which cadmium-cutoff convention is quoted alongside Φ_th, provided it is stated with its number.

</decisions>

<assumptions>
## Physical Assumptions

- **The 293.6 K ACE processing temperature and PARMA's 293.6 K free-gas ambient Maxwellian are
  adequate for a mK cryogenic target's capture channel.** | Phase 9 §5 explicitly flags this as an
  unvalidated assumption it could not settle and **hands it to Phase 14 with the number**. |
  What breaks if wrong: σ_capture is 1/v, so the thermal reaction rate is set by the *neutron*
  temperature — which is the ambient moderator's, not the target's — so the assumption is probably
  benign for the *rate*; but the Doppler width of the resonance-region capture integral is set by
  the *target* temperature, and a 293.6 K processing against a mK crystal is not the same
  calculation. **The direction of that error is not obvious and must be stated rather than
  assumed benign.**
- **Every capture produces exactly one recoiling nucleus.** | Elementary. | This is what makes the
  total capture reaction rate a *rigorous, cascade-independent* upper bound on the in-RoI rate,
  and it is the backbone of the whole phase.
- **Full containment of the ⁷¹Ge EC atomic relaxation energy in a 2 mm Ge wafer.** | At 158.7 eV
  (M) the relaxation products are Auger electrons with ranges far below 1 µm. | Breaks for the
  K line at 10.37 keV near a surface, where the X-ray can escape; that escape fraction is **not**
  modelled here and must be declared as an omission rather than assumed zero.
- **The thin-target reaction-rate formula R = Φ σ N.** | P_int(2 mm) = 3.24 % for elastic;
  capture is far smaller. | Self-attenuation and flux depression are negligible at this accuracy.
- **`phi_default` (outdoor) is the operative configuration.** | Phase 9 §4, structurally verified.
  | Indoors is a different configuration, not an uncertainty band.

</assumptions>

<limiting_cases>
## Expected Limiting Behaviours

- **Cascade multiplicity → 1:** the recoil concentrates at T = Q²/(2Mc²), the single-γ kinematic
  ceiling. This is the **maximum**, never the answer.
- **Cascade multiplicity → N with comparable γ energies:** ⟨T⟩ → T_max/N, because
  Σ E_γ² ≠ (Σ E_γ)². The roadmap's "tens of eV for a realistic multi-γ cascade" is this statement.
- **Isotropic cascade:** ⟨T⟩ = Σ E_γ²/(2Mc²) exactly, since the cross terms in |Σ p_i|² average
  to zero. Any bound that ignores the cross terms must state which side it errs on.
- **σ_capture → 1/v at low energy:** the folded reaction rate over a Maxwellian must **not** equal
  Φ_th × σ(0.0253 eV). The ratio is a Westcott-type convention factor and is a measurable,
  non-trivial number — **it must be measured, not assumed to be √π/2 = 0.8862.**
- **Trigger curve k → ∞:** P_trig → a step at 0.5 eV; **P_trig ≡ 1** must reproduce the
  untriggered result bit-identically.
- **⁷¹Ge exposure time t → ∞:** activity saturates at the production rate. **t → 0:** activity → 0.
  Any quoted ⁷¹Ge number without a stated t is undefined.

</limiting_cases>

<anchor_registry>
## Active Anchor Registry

- **Phase 9 `09-02-NEUTRON-DECLARATION.md`** — Φ_th = 2.767075×10⁻³ cm⁻² s⁻¹, the
  `order_of_magnitude` label and *why* it is a consequence of the evidence (§3.4), the
  `phi_lo`-is-indoor semantics (§4), the mK caveat handed here (§5), the directional-bias schema (§7).
  - Carry forward: planning, execution, verification, writing. Required action: read, use, cite.
- **Phase 13 `13-03-SUMMARY.md` / `13-03-NEUTRON-SPECTRUM.md`** — the elastic channel this sits
  beside: 5430.29 / 5485.15 counts kg⁻¹ day⁻¹ in E_rec 10–100 eV; the demonstrated-UNBOUNDED flux
  term; the `DoubleBroadeningError` guard and its `broadened_provenance` marker; the counts-budget
  pattern with retained-only vs retained+leaked kept separate.
  - Carry forward: planning, execution. Required action: read, use, compare.
- **Phase 12 CEvNS total 118.73 counts kg⁻¹ day⁻¹** — the signal this channel must be compared
  against, on the **shared reconstructed axis** (Phase 13 corrected its own cross-axis overclaim).
  - Carry forward: execution, writing. Required action: compare.
- **Phase 15 `15-01`** — the IA-applicability determination for electron-recoil channels, and the
  derivation route (Compton profile / bound-electron momentum distribution) that makes the "no"
  a result rather than a shrug.
  - Carry forward: execution. Required action: read, use, cite.
- **Frozen ENDF/B-VIII.0 + Lib80x ACE** at `data/endf/raw/`, `data/endf/ace/`, with
  `data/endf_nGe_elastic_v1.1.csv` as the acquisition-and-provenance pattern.
  - Carry forward: execution, verification. Required action: read, use, cite.
- **Biffl et al., PRD 107, 092011** — capture recoils "strongly overlap the CEvNS signal for
  recoils ≲ 100 eV"; Φ_th < 7×10⁻⁴ n/cm²·s stated as a requirement. Roadmap-named anchor.
  - Carry forward: execution, writing. Required action: compare, cite.
  - **Note the direction:** the adopted Φ_th = 2.767×10⁻³ is **3.95× above** Biffl's stated
    requirement. That is a comparison this phase must make explicitly, not skip.
- **EGAF / IAEA prompt capture-γ line lists** — **NOT present locally.** Required to *sharpen*
  the cascade bound; **not** required to *state* it. Recorded as a candidate acquisition whose
  failure is an acceptable, named gap.
- **CONVENTIONS §B / §D / §I / §J.** Carry forward: execution. Required action: use.

</anchor_registry>

<skeptical_review>
## Skeptical Review

- **Weakest anchor:** the eV–keV differential shape of the sea-level neutron flux. Phase 13
  demonstrated *concretely* that perturbations invisible to the channel's only independent
  cross-check move the in-RoI rate by tens of percent. Everything in this phase inherits that,
  and the epithermal part of the capture rate inherits it most directly.
- **Second weakest, and specific to this phase:** the cascade multiplicity distribution. Without
  EGAF there is no way to convert the rigorous rate bound into a recoil *spectrum*. The phase must
  not paper over that with an assumed multiplicity presented as a result.
- **Unvalidated assumptions:** the 293.6 K neutron and processing temperature against a mK target
  (handed here by Phase 9, unresolved); full containment of the EC relaxation energy; the
  irradiation history implied by any ⁷¹Ge activity quoted.
- **Competing explanation:** a capture rate that lands close to the elastic channel's RoI rate
  could reflect real physics *or* an arithmetic conflation — e.g. multiplying a band-integrated
  Φ_th by a point cross section, or double-counting the epithermal region between the two flux
  tables. Separated by band-decomposing the fold and by keeping the naive product as a
  *separately reported comparison* rather than as the answer.
- **Disconfirming check that is NOT an algebraic identity:** band-decompose the capture reaction
  rate by **incident** neutron energy and test whether the thermal band (≤ 0.5 eV) actually
  dominates. Nothing in the phase's own title, in CALC-23, or in the roadmap establishes that it
  does — 1/v weighting favours thermal, but the sea-level spectrum is flat in lethargy over
  1 eV – 10 keV to a factor 1.390 (Phase 9), which pushes the other way, and the resonance
  integral is not the thermal cross section. **If the epithermal and fast bands together carry a
  large fraction, the phase's "thermal-capture" framing is measurably too narrow and that must be
  reported, not absorbed.**
- **False progress to reject:** a capture number that agrees with the naive Φ_th × σ_2200 product
  is *not* corroboration — the two are the same integral evaluated two ways, and agreement would
  more likely indicate that the fold silently collapsed to the naive product. The check is that
  they **differ**, in a measured and explicable direction.

</skeptical_review>

<deferred>
## Deferred Ideas

- **Sharpening the cascade recoil bound into a spectrum** — requires the EGAF capture-γ cascade
  line lists and a cascade Monte Carlo. Follow-up scope; explicitly outside the lowered accuracy
  expectation.
- **CALC-24 (TENDL-2023 splice above the 20 MeV ENDF ceiling)** — Phase 13 sustained the deferral
  on a *measured* bound with 11.85× margin. Not reopened here. The capture cross section shares the
  same 20 MeV ceiling and the same disposition.
- **Cosmogenic activation of ⁷¹Ge / ⁶⁸Ge / ⁶⁵Zn by the fast/spallation component** — a real
  surface-detector effect, distinct from thermal-capture production, and **not** in this phase's
  scope. Named here so its absence is deliberate rather than accidental.
- **X-ray escape modelling for the K-shell EC line near the wafer surface** — declared as an
  omission, not modelled.
- **Fixing the CALC-23 requirement text** (it still reads "in-shield thermal flux φ_th, which
  NUCLEUS does not publish"). Flagged for the orchestrator; no plan in this phase edits
  `GPD/REQUIREMENTS.md` or the ROADMAP.

</deferred>

---

_Phase: 14-ge-only-thermal-capture-channels-p-geonly_
_Context recorded: 2026-07-23 (no discussion session; standing directive)_
