# Phase 9 Context — Sea-Level Surface Environment Lock (P-ENV)

**Status:** No `/gpd:discuss-phase` session was run for this phase.
**Recorded:** 2026-07-22, during autonomous roadmap execution.

## Provenance of this file

This file is **not** a transcript of a discussion with the user. It exists to record,
honestly and auditably, what the binding intent for Phase 9 actually is, given that the
user issued a standing session directive to run the roadmap to completion without
per-phase discussion unless a genuine blocker arises.

**No new user decisions were collected while writing this file.** Everything below is
transcribed from artifacts that already existed before this session's planning began:
`GPD/ROADMAP.md` (the re-scope banner and the Phase 9 section), `GPD/STATE.md`
(Accumulated Context), `GPD/state.json` field `project_contract`, `GPD/CONVENTIONS.md`,
`GPD/REQUIREMENTS.md`, and `paper/sections/backgrounds.tex`. Nothing here is invented.

<domain>
## Phase Boundary

Declare the unshielded sea-level environment the wafer sits in **once**, and freeze it as a
single provenance-headed input set covering all three particle channels — muons,
environmental gammas, and neutrons. The v1.0 muon and gamma inputs are **re-declared
numerically unchanged**; the one genuinely new input is a **rough sea-level neutron flux**,
retrieved from published literature and labelled **order-of-magnitude at the point of
definition** rather than downstream.

This phase produces **inputs**, not folds. It does not compute a Ge recoil spectrum
(Phase 13), does not compute a capture channel (Phase 14), and does not touch the energy
grid (Phase 10, which runs in parallel).

Requirements: CALC-11 *(re-pointed by the 2026-07-22 re-scope; its literal object list — the
NUCLEUS VNS digitization set — is void. What survives is its methodology: freeze a
provenance-headed environment input set with lethargy-convention and integral-conservation
acceptance tests, now applied to the sea-level set. `REQUIREMENTS.md` itself flags the
requirement text as needing re-wording; no plan in this phase edits it.)*

</domain>

<contract_coverage>
## Contract Coverage

Binding source: `GPD/ROADMAP.md` § "Phase 9: Sea-Level Surface Environment Lock (P-ENV)",
success criteria 1–5, verbatim. Reproduced here in condensed form; the ROADMAP text governs
on any discrepancy.

- **SC1 — muon and gamma re-declared numerically identical.** One frozen artifact declares
  all three channels with per-input provenance; the v1.0 muon and gamma inputs are
  re-declared **numerically identical** to their committed values — no renormalization, no
  relocation factor, no site correction — verified by **direct comparison against the frozen
  v1.0 artifacts rather than by assertion**.
- **SC2 — the neutron source is retrieved, not recalled.** Citation, energy range,
  normalization basis, and the accuracy the source itself claims are all recorded. If it is
  published in lethargy units the division by E happens **exactly once**; integral-conserving
  rebinning preserves the integral to <1%. If no source can be retrieved, the phase reports a
  **blocking gap** rather than substituting a remembered number.
- **SC3 — order-of-magnitude label at the point of definition.** The label propagates into
  Phases 13, 14 and 16, and **no acceptance test anywhere downstream demands better than
  order-of-magnitude agreement on this channel**.
- **SC4 — thermal component named, never zeroed.** The sub-eV component is identified as a
  separately named quantity for Phase 14's capture channel, **or** its absence from the
  sourced spectrum is recorded as a named gap. It is never silently set to zero.
- **SC5 — no shielded quantity enters.** A provenance / call-graph check confirms that no
  NUCLEUS attenuation factor, post-shield fluence, overburden depth, buildup factor, or
  rejection percentage appears anywhere in the environment set. The Phase-8 credit sentinels
  remain exactly 1.0 and the veto credit is 1.0 **by construction** — there is no veto in
  this configuration — rather than by policy default.

**Acceptance signals:** header-level numeric identity against the committed v1.0 CSVs;
recomputation of the neutron anchor integrals from committed code; a named Φ_th scalar or a
named gap row; a zero-hit forbidden-token scan over the environment set.

**False progress to reject:**

- Re-running a Monte Carlo and accepting a slightly different rate as "identical".
- Quoting any sea-level neutron number from memory, from a secondary citation, or from a
  WebFetch/LLM page summary rather than from a locally frozen file via a recorded command.
- Presenting the neutron input to better than order-of-magnitude precision.
- Any NUCLEUS shielding attenuation, φ_post, overburden, buildup factor, veto credit or
  multiplicity credit re-entering under a new name.
- Building a second pipeline, flux table, or spectral shape for the NUCLEUS VNS.

</contract_coverage>

<user_guidance>
## User Guidance To Preserve

Two user decisions are load-bearing for this phase. Both predate this file; neither was
elicited for it.

- **Re-scope decision, verbatim (2026-07-22):** *"Just take the approximation as was done in
  the paper. I don't need a very accurate result."* "The paper" is this project's own v1.0
  manuscript, `paper/sections/backgrounds.tex`, which treats the wafer as an **unshielded
  surface detector**. Recorded in `GPD/ROADMAP.md` re-scope banner and `GPD/STATE.md`.
  - Operative consequence: **accuracy is explicitly not required**. Prefer closed-form folds
    and bounded estimates. Regularized/Tikhonov inversion, curve-digitization campaigns, and
    multi-target over-determination tests are **out of scope by user decision**.
- **Veto-credit decision (2026-07-22, carried from Phase 8):** no reduced veto credit may be
  assumed and no resized veto may be invented. In this configuration the credit is exactly
  **1.0** — i.e. none — **by construction**, because there is no veto.

- **User-stated observables:** none newly stated for this phase. The phase's observables are
  the ROADMAP's three declared channel inputs.
- **User-stated deliverables:** one frozen, provenance-headed 3-channel surface-environment
  input set (ROADMAP Phase 9 Deliverables line).
- **Must-have references / prior outputs:** `paper/sections/backgrounds.tex` as *the binding
  statement of what the background environment is* — this is the answer, not a starting
  point; the committed v1.0 muon and gamma artifacts; the Phase-7 frozen n-Ge elastic set.
- **Stop / rethink conditions:** if the neutron source cannot be retrieved and
  integrity-checked, report a **blocking gap**, not a remembered number (ROADMAP SC2). If the
  thermal component cannot be obtained, report a **named gap**, never zero (ROADMAP SC4).

</user_guidance>

<decisions>
## Methodological Decisions (LOCKED — carried from prior artifacts, not newly elicited)

### Scenario and normalization

- The primary configuration is an **unshielded surface wafer at 3 GW_th / 25 m**, which is
  simultaneously the paper's own scenario, the frozen `data/flux/reactor_flux_v1.0.csv`
  table, and the standing `GPD/CONVENTIONS.md` §D lock (Standoff distance 25 m; Reactor
  thermal power 3 GW_th). **§D needs no edit for this milestone.**
- The NUCLEUS VNS survives only as an optional **labelled scalar rescale** (≈0.28) of the
  finished result. Building a second pipeline, flux table, or spectral shape for it is
  forbidden (`fp-second-vns-run`, project contract).

### Muon channel

- The v1.0 sea-level **Gaisser–Guan ⊗ ray-box chord ⊗ Landau–Vavilov MPV** chain stands
  unchanged. Re-declare it; do not recompute it.
- Frozen artifact of record: `data/muon_dRdEdep.csv`
  (header `integral_muon_rate_Hz = 1.3659 +/- 0.0003`; first grid edge `1.014497e-02` keV).
  Modules: `src/qpd_potential/muon_deposit.py`, `src/qpd_potential/muon_flux.py`.
- **Path correction (binding).** `04-01-SUMMARY.md` front-matter names
  `src/muon/deposited_spectrum.py` and `data/muon/muon_dep_spectrum.csv`. **Those paths do
  not exist.** Do not cite them.
- Stated accuracy carried forward as-is: within ~20% of the PDG sea-level expectation, inside
  the VALD-02 30% tolerance, with the 30–35% inter-experiment Gaisser–Guan normalization
  spread named as the weakest anchor of the channel.

### Environmental-gamma channel

- The v1.0 **Klein–Nishina ⊗ Hubbell bound-incoherent** treatment with the LABChico-anchored
  absolute normalization and its **factor-2 site-dependent band** stands unchanged.
  Re-declare it; do not replace it.
- Frozen artifacts of record: `data/gamma_lines.csv`, `data/ge_incoherent_S.csv`,
  `data/ge_xcom_mu.csv`, `data/compton_dRdEdep.csv`
  (header `total_single_scatter_rate_Hz = 2.6747e-01`). Modules:
  `src/qpd_potential/compton_source.py`, `src/qpd_potential/compton_deposit.py`.
- Confidence split preserved verbatim from the paper: edge positions HIGH (exact Compton
  kinematics, 1243 / 1541 / 2382 keV), absolute normalization MEDIUM (factor ~2).

### Neutron channel — the one genuinely new input

- The paper omitted neutrons entirely. They were ~91% of NUCLEUS's shielded RoI budget, so a
  silent omission would flatter the result (`fp-silent-neutron-omission`).
- **Planning finding, recorded because it changes what this phase must do.** The ROADMAP
  Phase 9 anchor line states *"The sea-level neutron flux has no anchor yet and none is
  asserted here"*, naming Gordon et al. (IEEE TNS **51**, 3427 (2004)) and ICRU/JEDEC-class
  spectra as **candidates to source and verify**. That is true of the *milestone's* anchor
  registry, but a sea-level surface neutron flux **already exists in this repository**:
  `data/ambient_neutron_flux_v1.1.csv`, produced by Phase 7 Plan 07-01 (v1.1, carried
  forward), with
  - **shape** from PARMA v4.10 / Sato, PLOS ONE **10**(12):e0144679 (2015), open access,
    coefficients taken from the official PARMA C++ source at pinned mirror commit
    `6ff37cacb8cf003e2fc269963f9a08f812407264` — *not* typed from the article;
  - **normalization** anchored by a single scalar k = 1.09610 to the cited Gordon-2004
    sea-level NYC integral Φ(>10 MeV) = 3.55×10⁻³ cm⁻²s⁻¹, with PARMA's untuned native
    integral 3.239×10⁻³ agreeing to ~9% as an independent cross-check;
  - a recorded **USER DECISION 2026-07-22** switching the differential shape from the
    paywalled Gordon/JEDEC coefficients to open-access PARMA, retaining Gordon as the
    integral benchmark only.
  Phase 9 therefore **adopts and verifies** this artifact rather than re-sourcing from
  scratch. This is a scope *reduction* consistent with the lowered accuracy expectation, and
  it is recorded here rather than assumed silently.
- **What is genuinely open and must be closed in-phase:**
  1. Phase-7 verification gap **D2** (severity *significant*): *"No PARMA driver committed;
     the decisive 3.55e−3 and 1.317e−2 integrals cannot be recomputed."* The Phase-7
     verifier called this *"the weakest reproducibility link in the phase."* ROADMAP SC2
     demands the source be *actually retrieved and integrity-checked*, so D2 must be closed
     here or recorded as a persisting limitation on the environment set itself.
  2. The committed table's energy floor is **10.14 eV**. Its header quotes
     Φ(0.01 eV → 10 GeV) = 1.317×10⁻² cm⁻²s⁻¹ evaluated natively in PARMA, but **no sub-10 eV
     bins are on the table**. ROADMAP SC4's thermal component is therefore not currently a
     named quantity — closing D2 with a committed driver is also what makes Φ_th obtainable.
- **Band semantics for an unshielded surface wafer (binding).** The committed table's
  `phi_hi = phi_default` is the **outdoor sea-level** value and is the operative one here;
  `phi_lo = phi_default/5` is a scalar stand-in for **indoor/building attenuation** and does
  **not** describe an unshielded surface wafer. Its header already flags the scalar as an
  unvalidated treatment that understates the spectral-shape systematic (building moderation
  shifts fast → thermal). Using `phi_lo` as a central value or a symmetric error bar would
  lower the neutron background and improve S/B — a flattering direction.
- **Truncations carried forward, not closed here:** the 20 MeV ENDF/B-VIII.0 σ_el ceiling
  (Phase-7 gap D1, resolved by user decision 2026-07-22 as *truncate and document*), and the
  ~197 MeV shared-grid ceiling above which 21% of the >10 MeV flux lies. Both are Phase-13
  fold concerns; Phase 9 records them as declared omissions on the input.

### Evidence discipline (carried from Phase 8, binding)

- Every quoted number must come from a **locally frozen file via a recorded, reproducible
  command**. **WebFetch and any LLM page summarizer are forbidden as a quote source** — during
  Phase 8 a summarizer produced two verified factual errors on sources that were correct and
  accessible.
- Reuse the frozen-source pattern already established in `data/external/nucleus/`: raw
  artifact + normalized text + `MANIFEST.md` carrying retrieval command, byte count, SHA-256,
  and an integrity verdict distinguishing real source text from an anti-bot challenge page.
- **U+2009 thin-space gotcha:** normalize Unicode spaces before grepping. Un-normalized thin
  spaces silently break ASCII exact-phrase greps and make present text look absent.

### Agent's Discretion

- Module decomposition, artifact layout, and test design.
- The exact integration bound used to define the thermal component (e.g. a cadmium-cutoff
  convention), provided the bound is stated explicitly with the value.
- The tolerance thresholds on the anchor-integral reproduction, provided each is stated
  before the check is run and is not loosened after a failure.
- Whether the extended sub-eV neutron table is emitted on PARMA's native grid or a
  documented log grid — but it must **not** be placed on the project shared grid, because
  Phase 10 owns the grid extension and runs in parallel with this phase.

</decisions>

<assumptions>
## Physical Assumptions

- **The wafer is outdoors at sea level with zero overburden.** Justification: the re-scope
  adopts the v1.0 manuscript's own treatment, which assumes no overburden and no shield |
  If the intended deployment is in fact inside a building, the neutron flux drops by roughly
  a factor of a few and its spectrum hardens/moderates non-uniformly, and the muon flux is
  essentially unchanged. This is a **configuration** question, not an uncertainty band, and
  it is why `phi_lo` must not be used as an error bar.
- **PARMA evaluated at the NYC reference point (r_c = 2.08 GV, d = 1033 g/cm², s = 100,
  g = 0.15) represents the deployment site.** Justification: it matches the Gordon-2004 NYC
  reference the integral anchor comes from | If the real site differs in altitude or
  geomagnetic cutoff the normalization moves upward, not downward — the omission is in the
  penalizing direction, which is the safe one.
- **The v1.0 muon and gamma channels remain valid at the surface without modification.**
  Justification: they were computed for exactly this configuration | Nothing breaks; this is
  the one assumption in the phase that is close to definitional.
- **The gamma absolute flux is site-representative to a factor ~2.** Justification: LABChico
  measured anchor with U-chain set by an assumed chain balance | A different site rescales
  the overall rate but not the edge structure.

</assumptions>

<limiting_cases>
## Expected Limiting Behaviors

- **Muon rate:** the re-declared through-wafer rate must equal the committed
  `1.3659 Hz` exactly, and the analytic scalars must reproduce from the committed module —
  ⟨ℓ⟩ = 4V/S = 0.385 cm (Cauchy), ξ = 0.0721 MeV, Δ_p = 1.2323 MeV, with
  Δ_p < ⟨Δ⟩ = 1.4585 MeV (Landau right-skew ordering).
- **Compton edges:** recomputing E_edge = 2E_γ²/(m_ec² + 2E_γ) from the committed
  `data/gamma_lines.csv` line energies must return 1243.4 / 1541.3 / 2381.8 keV for
  ⁴⁰K / ²¹⁴Bi / ²⁰⁸Tl, agreeing with the committed values to better than 0.5 keV.
- **Neutron anchor:** k → 1 must return PARMA's untuned native integral 3.239×10⁻³ cm⁻²s⁻¹,
  and k = 1.09610 must return the Gordon anchor 3.550×10⁻³ cm⁻²s⁻¹ by construction.
- **Neutron shape:** the driver-recomputed φ(E_n) on the committed table's own bin centres
  must reproduce `phi_default` to ≲1%. Any larger deviation means the committed table is not
  what the recorded provenance says it is.
- **Spectral morphology:** a correct sea-level neutron spectrum shows four canonical
  ground-level features — thermal Maxwellian peak near 0.03 eV, a 1/E epithermal plateau, a
  1–3 MeV evaporation hump, and a ~100 MeV cascade peak with tail. A monotone or
  feature-free spectrum is a bug.
- **Veto credit:** `src/qpd_potential/veto_credit.py` sentinels must return exactly 1.0.

</limiting_cases>

<anchor_registry>
## Active Anchor Registry

- `paper/sections/backgrounds.tex` — the v1.0 manuscript's own background treatment
  - Why it matters: this is the **binding statement of what the environment is** under the
    re-scope. It is the answer, not a starting point.
  - Carry forward: planning, execution, verification, writing
  - Required action: read, use, cite
- `data/muon_dRdEdep.csv` + `src/qpd_potential/muon_deposit.py`, `muon_flux.py`
  - Why it matters: the frozen v1.0 muon input that SC1 requires be re-declared identical
  - Carry forward: planning, execution, verification
  - Required action: read, use, compare
- `data/compton_dRdEdep.csv`, `data/gamma_lines.csv`, `data/ge_incoherent_S.csv`,
  `data/ge_xcom_mu.csv` + `src/qpd_potential/compton_source.py`, `compton_deposit.py`
  - Why it matters: the frozen v1.0 gamma input that SC1 requires be re-declared identical
  - Carry forward: planning, execution, verification
  - Required action: read, use, compare
- `data/ambient_neutron_flux_v1.1.csv` (Phase 7 Plan 07-01)
  - Why it matters: the existing sea-level neutron flux this phase adopts and verifies
  - Carry forward: planning, execution, verification
  - Required action: read, use, compare
- Sato T., PLOS ONE **10**(12):e0144679 (2015), DOI 10.1371/journal.pone.0144679 — PARMA
  - Why it matters: the differential **shape** source; open access
  - Carry forward: execution, verification, writing
  - Required action: read, use, cite
- PARMA v4.10 official C++ source, mirror commit `6ff37cacb8cf003e2fc269963f9a08f812407264`
  - Why it matters: the coefficients live in the distribution, not the article; this is the
    only route to a reproducible anchor and to the sub-eV thermal component
  - Carry forward: execution, verification
  - Required action: read, use, cite
- Gordon et al., IEEE Trans. Nucl. Sci. **51**, 3427 (2004)
  - Why it matters: the **integral** normalization benchmark, Φ(>10 MeV) = 3.5–3.6×10⁻³
    cm⁻²s⁻¹. Its **differential coefficients are paywalled and were unsourceable** — it is not
    the shape source and must not be cited as one.
  - Carry forward: execution, verification, writing
  - Required action: compare, cite
- `GPD/phases/07-scenario-nuclear-data-lock/07-VERIFICATION.md` (gap D2)
  - Why it matters: names the unreproducible anchor this phase must close or carry
  - Carry forward: planning, execution
  - Required action: read, compare
- `GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-05-GATE-VERDICT.md`
  - Why it matters: the NO-FIT verdict that voided the shielded premise and forced this scope
  - Carry forward: planning
  - Required action: read
- `data/external/nucleus/MANIFEST.md`
  - Why it matters: the frozen-source provenance pattern to reuse (SHA-256, recorded command,
    integrity verdict, Unicode-space normalization)
  - Carry forward: execution
  - Required action: read, use
- `GPD/CONVENTIONS.md` §D
  - Why it matters: the 3 GW_th / 25 m scenario lock, unchanged and now primary
  - Carry forward: planning, execution
  - Required action: read, use

</anchor_registry>

<skeptical_review>
## Skeptical Review

- **Weakest anchor:** the neutron channel's *shape* has no independent validation. Gordon's
  differential coefficients are paywalled, so the only cross-check that exists is a **single
  integral** agreeing to ~9%. Two spectra can share a >10 MeV integral and differ badly at
  the eV–keV energies that actually matter for a Ge recoil in the CEvNS RoI. The channel's
  order-of-magnitude label is therefore honest, not decorative.
- **Unvalidated assumptions:** that the recorded PARMA provenance of
  `data/ambient_neutron_flux_v1.1.csv` is what actually produced the committed numbers — this
  has **never been checked jointly**, which is precisely Phase-7 gap D2; that the committed
  table's `phi_lo = phi_default/5` scalar is an adequate stand-in for building attenuation
  (its own header says it is not, and it is not used here anyway); that a NYC-referenced
  PARMA evaluation represents the deployment site.
- **Competing explanation:** if the driver-recomputed φ fails to match the committed table,
  the benign reading is a grid/interpolation difference and the adverse reading is that the
  committed table was produced by a path the header does not describe. The check must be run
  before either story is told, and the adverse reading must not be assumed away.
- **Disconfirming check (deliberate, and required):** a **directional-bias audit** across all
  three channels. For each channel, state which direction its adopted central value errs
  relative to its own published anchor, and whether that direction raises or lowers S/B.
  Known in advance: the muon rate is ~20% *below* the PDG expectation (**lowers background →
  flatters S/B**); the gamma normalization carries a factor-2 band whose low edge would also
  flatter; the neutron `phi_lo`, if misused, would flatter by a factor 5. A phase in which
  every channel happens to sit on the flattering edge of its own band is reporting a
  preference, not a measurement. This audit exists because **three of the four errors found in
  Phase 8 pointed in the direction that favoured the expected conclusion**, and the fourth was
  found only when a verifier was explicitly told to hunt for one.
- **False progress to reject:** a beautifully provenance-headed artifact whose neutron numbers
  were never recomputed from committed code; a "verification" of numeric identity that
  re-runs a Monte Carlo and accepts drift; an order-of-magnitude label that appears in the
  header but not on the individual quantities downstream consumers actually read.

</skeptical_review>

<deferred>
## Deferred Ideas

- **Deleted by the 2026-07-22 re-scope — must not appear in any Phase 9 plan:** the
  `mcpd_to_dru()` unit chain and duty-cycle-on-Table-5 anchoring; digitization of NUCLEUS
  Figs. 4 and 8–11; the pre-vs-post-veto determination for Figs. 8–11; **CALC-12** φ_post
  recovery by regularized (Tikhonov/TV) differentiation with the CaWO₄/Al₂O₃
  over-determination test; the **VALD-11** two-band gate. CALC-12 and VALD-11 are **orphaned
  by design**.
- The Ge neutron recoil fold, the resonance imprint, and the kinematic-compression statement
  — **Phase 13**, where they belong as target physics.
- The (n,γ) capture channel and the ⁷¹Ge EC lines — **Phase 14**, which consumes this phase's
  Φ_th (or its named gap).
- The 0.1 eV grid extension and regenerated response matrices — **Phase 10**, running in
  parallel. Phase 9 must not depend on it.
- Closing the 20 MeV ENDF ceiling by a TENDL-2023 splice (**CALC-24**) — follow-up scope.
  Note that its Phase-7 deferral rationale (shield attenuation of the >10 MeV tail) is void
  at the surface, and the ROADMAP already flags this for the orchestrator.
- Re-wording CALC-11's requirement text, and the `REQUIREMENTS.md` citation of a
  `CONVENTIONS §D` VNS lock that never happened — both flagged in `REQUIREMENTS.md` for the
  orchestrator. **No plan in this phase edits `REQUIREMENTS.md` or `CONVENTIONS.md`.**

</deferred>

---

_Phase: 09-sea-level-surface-environment-lock-p-env_
_Context recorded: 2026-07-22 (transcribed from existing artifacts; no discussion session held)_
