# 15-04 — Re-scope audit, accuracy carry-forward, dominance re-check, and Phase-15 closure

**Plan:** 15-04 · **Phase:** 15 · **Date:** 2026-07-23
**Interpreter:** `/opt/anaconda3/bin/python3` (numpy 1.26.4, scipy 1.17.1)
**Repo HEAD at execution:** `b8addf2`

---

## 1. ROADMAP SC4 — the re-scope audit

### 1.1 The scan

The token list is **imported**, never re-typed, via
`surface_environment.shielded_token_guard()` → `tests/test_env_v1_identity.py`,
the single definition site. Two divergent copies of a guard list is how a guard
silently stops guarding — and the digit-boundary matching that lives there is what
keeps the germanium lattice constant **5.658 Å** from false-positiving on the
**5.65 Bq/kg** ²³⁸U activity. An ad-hoc substring scan written during this phase
*did* produce that false positive; the imported guard did not.

**Scope: 31 files.**

| what | count |
|---|---|
| full **import closure** of every module this phase touches, computed by walking module attributes as Plan 09-01 did | **18** |
| artifact files this phase emits | **7** |
| documents this phase **emits** | **6** |

Closure files: `compton_deposit`, `compton_source`, `em_extended`, `em_recoil`,
`energy_scale`, `fold`, `ia_broadening`, `interp_guard`, `legacy_grid`,
`muon_deposit`, `muon_flux`, `params`, `phonon_scale`, `response`,
`response_matrix`, `surface_environment`, `trigger`, `wafer_geometry`.

**Not scanned, and the exclusion is stated rather than silent:** the `*-PLAN.md`
files and `15-CONTEXT.md`. They are **inputs authored upstream** and they
necessarily quote every retired quantity by name and value **because they command
this audit**; scanning them would flag the instruction as the violation.

### 1.2 Result

```
35 token hits
  34  explicit NOT-APPLIED / enumeration declarations  (the enumeration SC4 requires)
   1  allowlist entry, justified below
   0  APPLIED quantities outside the allowlist
```

**Allowlist — one entry, with a justification a future reader can audit rather than
trust:**

`src/qpd_potential/compton_source.py:187` —
`"""Linear attenuation coefficient mu = (mu/rho) * rho [cm^-1]."""`
This is the NIST XCOM photon **mass-attenuation coefficient of the germanium target
wafer** (`data/ge_xcom_mu.csv`), used for `μ·ℓ̄` and the double-scatter fraction. It
is a property of the *target*, not a shield, an overburden, a buildup factor or any
post-shield quantity, and **it multiplies no normalization**. This is the same
single entry Plan 09-01 exempted, by name. A new attenuation-like term would not
match this substring and would fail.

A local extension to the Phase-9 `NOT_APPLIED_MARKERS` was needed and is recorded
rather than hidden: SC4 *requires* each retired quantity to be enumerated by name as
removed, so the audit's own prose and the emitted reports' "no relocation quantity"
statements necessarily contain the tokens. The added phrases are
`retired`, `removed by the`, `zero-overburden`, `ZERO overburden`,
`no relocation quantity`, `must not`, `cannot be relaxed`, `absence of the`,
`there is no`, `enumerat`, `prohibition`, `sentinel`, `by construction`.
**None of them can let an applied quantity through:** an applied factor appears in
an assignment or a multiplication, not in a sentence containing "retired" or
"removed by the".

### 1.3 Each retired quantity, enumerated by name and value as REMOVED

`artifacts/v2.0/em_rescope_audit.csv` — **17 rows**. An audit reporting "no hits"
without enumerating what it searched for cannot distinguish deliberate removal from
accidental omission, which is the whole reason SC4 exists.

| quantity | retired value | token | applied hits | disposition |
|---|---|---|---|---|
| NUCLEUS overburden depth | **2.92 m.w.e.** | `overburden` | 0 | removed by the 2026-07-22 re-scope |
| omnidirectional attenuation factor | **1.41** | `1.41` | 0 | removed by the 2026-07-22 re-scope |
| NUCLEUS Table 2 total gamma ambience | **5.03 cm⁻² s⁻¹** | `ambience` | 0 | removed by the 2026-07-22 re-scope |
| NUCLEUS Table 2 ⁴⁰K activity | **59.6 Bq/kg** | `ambience` | 0 | removed by the 2026-07-22 re-scope |
| NUCLEUS Table 2 ²³²Th activity | **3.28 Bq/kg** | `ambience` | 0 | removed by the 2026-07-22 re-scope |
| NUCLEUS Table 2 ²³⁸U activity | **5.65 Bq/kg** | `ambience` | 0 | removed by the 2026-07-22 re-scope |
| passive-shielding reduction factor | **~50** | `buildup` | 0 | removed by the 2026-07-22 re-scope |
| shield buildup factor | n/a | `buildup` | 0 | removed by the 2026-07-22 re-scope |
| MV + COV veto rejection | **99.8 %** | `veto_credit` | 0 | removed by the 2026-07-22 re-scope |
| COV rejection factor at 1 keV_ee | **~5** | `veto_credit` | 0 | removed by the 2026-07-22 re-scope |
| NUCLEUS Table 5 muon residual | **< 14 mcpd** | `mcpd` | 0 | removed by the 2026-07-22 re-scope |
| **veto credit sentinel** | **1.0** | `veto_credit` | 0 | **exactly 1.0 BY CONSTRUCTION, not by policy default** |
| 5 × normalization factor | **1.0 each** | (numeric) | 0 | exactly 1.0, asserted INDIVIDUALLY |

Each row carries the reason it no longer applies. Examples: an attenuation factor
presupposes an attenuator and there is none; buildup describes scattered-photon
accumulation *inside* a shield and there is no shield; the Table 5 residual is a
**post-veto** number for a shielded, vetoed apparatus, and its removal is recorded
with its consequence rather than hidden — **the muon channel now has no external
benchmark on the reconstructed axis at all**, beyond the v1.0 PDG sanity check.

### 1.4 The veto credit sentinel

`surface_environment.veto_credit()` returns **exactly 1.0**, and the audit records
it as **by construction** rather than as a default. The distinction is the point: a
1.0 arrived at as a policy default is something a later phase could quietly relax; a
1.0 that follows from the **absence of the apparatus** cannot be relaxed without
first changing the configuration. No artifact or document in this phase applies a
rejection factor of any other value.

### 1.5 The numeric complement — every factor individually unity

A token scan cannot see a retired quantity re-entering under a **new** name with a
**new** value. The complement is an enumeration of every multiplicative factor
applied to each channel's normalization between the frozen v1.0 rate and the emitted
reconstructed spectrum, each asserted to be **exactly 1.0 on its own**:

```
overburden_attenuation = 1.0    (no overburden in this configuration)
shield_attenuation     = 1.0    (no shield in this configuration)
veto_credit            = 1.0    (exactly 1.0 BY CONSTRUCTION)
buildup_factor         = 1.0    (no shield, so no buildup)
ambience_rescale       = 1.0    (the v1.0 sea-level normalization stands unchanged)
```

**Asserting only that the product is 1.0 would not do**, because a product can be
unity by cancellation between two wrong factors (`fp-product-instead-of-factors`).
The test checks each one separately, and all five are written into both Plan 15-02
deposit-table headers and both Plan 15-03 reconstructed-table headers.

The end-to-end numeric evidence is independent of the enumeration: the through-wafer
muon rate is **1.365914 Hz** against the frozen **1.3659 Hz**, and the Compton
bound-incoherent rate is **2.6747e-01 Hz** against the frozen **2.6747e-01 Hz** —
identical to the frozen precision, which no surviving normalization factor other
than 1.0 could produce.

### 1.6 The word that must not appear

Text scan for **"conservative"** attached to this configuration over all 31 scanned
files: **zero occurrences.** One occurrence existed in an earlier draft of
`15-01-BROADENING-APPLICABILITY.md` describing a *physical choice* (the band-gap
reading) rather than the configuration; it was reworded to "more restrictive"
because a text check that has to reason about attachment is a weak check. An L2-off,
shielding-absent configuration is a **different and worse** configuration than
NUCLEUS's, not a subset of it, and the word would misrepresent a worse configuration
as a safer estimate. Phase-8 lock, milestone-wide.

### 1.7 Which of the two readings this establishes

**Stated plainly, because the two are not the same claim.** A clean token scan
establishes that **no relocation quantity survived under a recognised name or
value**. It does **not** establish that none survived under a *new* name with a
*new* value — a token scan cannot see that, and an attribute-walk import closure
cannot see a dynamically imported module either (none is used in this closure, but
the walk cannot prove that).

The numeric-factor enumeration is the complement, and together they are a **strong
check, not a proof**. The audit CSV says so in its own header.

---

## 2. ROADMAP SC5 — accuracy carried forward unnarrowed

`artifacts/v2.0/em_accuracy_labels.csv`, reusing the Plan 09-01 §5 directional-bias
schema. This is the machine-readable object Phase 16 propagates, complete enough
that Phase 16 need not re-derive any of it.

| field | muon | gamma |
|---|---|---|
| accuracy label | `pdg_within_20pct_vald02_tol_30pct` | `site_band_factor_2` |
| bias direction | `flatters_SB` | `neutral` |
| **signed deviation** | **−20.61 %** | **+0.00 %** |
| **anchor leg** | **PDG Leg A**: ≈1 muon cm⁻² min⁻¹ × A_top = 1.7204 Hz | LABChico measured survey — the adopted normalization **is** the anchor |
| **bracketing disclosure** | **PDG Leg B** (I_v ≈ 70 m⁻²s⁻¹sr⁻¹, cos²θ → 1.1350 Hz) gives **+20.34 %**, i.e. `penalizes_SB`. The two legs **bracket** the adopted 1.3659 Hz from opposite sides: the **~20 % magnitude is solid, the SIGN is not.** | n/a — the adopted value sits **at** the anchor, not on either edge. The **low** edge (×0.5) is the flattering one and is **not** used. |
| band | **×0.65 … ×1.35** | **×0.5 … ×2.0** |
| underlying limit | the **30–35 % inter-experiment Gaisser–Guan spread**, which no in-repo artifact can narrow | the **assumed Φ_U = Φ_Th chain balance** for the U-238 lines (`flux_unc_frac = 1.0`), not a measured line intensity |

**Nothing narrowed.** The muon band ×0.65 … ×1.35 is the Gaisser–Guan spread and it
**encloses** the PDG leg bracket ×0.8309 … ×1.2595, so choosing it cannot be a
narrowing; the test asserts the enclosure explicitly. The gamma band is exactly the
v1.0 ×0.5 … ×2. `test_bands_not_narrowed` compares every band multiplier in every
Phase-15 artifact against the v1.0 values and fails if any is narrower.

**The muon sign never travels alone.** Every occurrence of −20.61 % in every
Phase-15 artifact carries the Leg A citation and the Leg B bracketing disclosure —
asserted by `test_sign_carries_anchor_leg` over all seven emitted artifacts. A bare
−20.61 % or a bare `flatters_SB` would let a downstream phase inherit a direction
the evidence does not establish.

**Extending the energy axis does not improve a normalization.** The axis and the
normalization are independent, and no deliverable of this phase implies otherwise.

---

## 3. The in-band dominance re-check — recomputed, not inherited

`artifacts/v2.0/em_inband_dominance.csv`, 322 rows (161 reconstructed bins × 2
designs), every row carrying **both** contributing channels' accuracy labels.

Computed from the Plan 15-03 artifacts. **The CEvNS column is present for
orientation only**, so the overlap question can be asked at all; no quantity in this
phase is a signal-to-background ratio and none is named as one. Assembling that
ratio is Phase 16's terminal deliverable.

### 3.1 Integrated rates

| | Ta→Al | Al→Hf |
|---|---|---|
| **muon**, E_rec 10–100 eV | 7.4656 | 7.7231 |
| **Compton**, E_rec 10–100 eV | **34.2484** | **35.8616** |
| CEvNS (orientation), E_rec 10–100 eV | 72.9214 | 73.1441 |
| muon, below 10 eV | 0.6681 | 0.6787 |
| Compton, below 10 eV | 0.9448 | 0.9851 |
| CEvNS (orientation), below 10 eV | 29.2236 | 29.7991 |
| **Compton / muon in the RoI** | **4.587** | **4.643** |

(counts kg⁻¹ day⁻¹)

Cross-check: the CEvNS total over the whole reconstructed axis reproduces as
**118.7286 / 118.7292** against Phase 12's **118.730** — the orientation curve is
the right one and was not mis-read.

### 3.2 Does the v1.0 conclusion still hold?

The v1.0 conclusion was that **MeV muon deposits land above the CEvNS band**, while
the **environmental-gamma Compton continuum overlaps it** and is therefore the
dominant reducible background of the two.

**On the extended reconstructed axis, with two refinements:**

1. **CONFIRMED — the Compton continuum overlaps the CEvNS region and is the larger
   of the two electron-recoil channels there**, by **4.59×** (Ta→Al) and **4.64×**
   (Al→Hf) in the 10–100 eV RoI. The ordering is unchanged from v1.0.

2. **REFINED, and this is a departure worth stating.** The v1.0 phrasing that muons
   land *above* the CEvNS band is too strong on the extended reconstructed axis.
   The muon channel now carries **7.47 / 7.72 counts kg⁻¹ day⁻¹ in the RoI** — about
   **10 %** of the CEvNS rate there — and **0.67 / 0.68 below 10 eV**. It is not
   absent from the band; it is subdominant within it. What survives of the v1.0
   statement is that the muon channel's *bulk* is far above the band (the
   reconstructed peak is at 18.8 / 15.0 keV) and that it is the smaller of the two
   electron-recoil backgrounds in-band. What does not survive is the implication
   that it can be neglected there.

3. **Ordering crossovers.** The muon-to-Compton ratio crosses unity at
   **0.5309, 0.7499, 1.059, 1.189, 2.661 eV** and again at **1.884e+04 eV**
   (Ta→Al; **1.334e+04 eV** for Al→Hf). The sub-eV crossings sit in the region both
   Plan 15-01 floors exclude and where Plan 15-02 recorded no adequate Monte-Carlo
   support for the muon channel, so **they must not be read as physics**. The
   high-energy crossing is the muon saturation feature and is real.

### 3.3 What this table does **not** bound

**Nothing here bounds the total background.** Only two of the milestone's channels
appear. For orientation, the Phase-13 neutron channel alone integrates to
**5430.29** (Ta→Al) and **5485.15** (Al→Hf) counts kg⁻¹ day⁻¹ over the same
10–100 eV band — **159× and 153× the Compton channel** — and carries an
`order_of_magnitude` accuracy label. The neutron-capture channel is not in scope
here either.

So the in-band ordering of what has been computed so far is

```
neutron (5430 / 5485, order_of_magnitude)
   >>  CEvNS signal (72.9 / 73.1)
   >   Compton (34.2 / 35.9, factor-2 site band)
   >   muon (7.47 / 7.72, ~20% vs PDG with the sign anchor-leg dependent)
```

and the statement that follows for Phase 16 is that **the dominant background in the
region of interest is the neutron channel, not either electron-recoil channel** —
which is a comparison Phase 16 must make with all channels and their labels in hand,
not one this phase concludes.

---

## 4. Phase-15 closure

### 4.1 Success criteria

| SC | Statement | Verdict |
|---|---|---|
| **SC1** | Both spectra recomputed with the v1.0 machinery unchanged at the v1.0 normalizations, validated invariants reproduced, agreement with the frozen CSVs above 10.14 eV better than 1 % | **MET.** Max relative difference **4.6e-07**, four decades inside the bar; all three Compton edges to < 1e-3 keV; muon rate inside its frozen uncertainty; no photopeak. |
| **SC2** | Both channels on the extended grid from 100 meV, folded through the regenerated `R(E_rec\|E_dep)` for both designs with count conservation ≤ 1e-3, and the v1.0 saturation behaviour preserved | **MET.** `residual_fold ≤ 2.169e-16`; saturation survives as a **77.1× / 101.3×** instrumental compression, named instrumental with its 40 µs non-paralyzable mechanism. |
| **SC3** | Whether the Phase-11 broadening applies is decided and stated with a physical reason, with the consequence for the spectra written down | **MET.** Per-channel verdict `does_not_apply`, argued from which particle recoils and its initial-state momentum distribution, with the electron-side Compton-profile analogue **evaluated** rather than dismissed, and enforced by a guard that raises. |
| **SC4** | Explicit audit asserting the absence of every retired relocation quantity, each **recorded as removed** | **MET.** 0 applied hits over a 31-file scope; 17 enumerated rows; veto credit 1.0 by construction; every normalization factor individually 1.0; zero occurrences of the forbidden configuration adjective. |
| **SC5** | Both channels' accuracy carried forward unchanged from v1.0 | **MET.** Bands identical or wider; the muon sign always with its anchor leg and bracketing; a test fails if either band narrows. |

**No success criterion was superseded by measurement in this phase.** All five are
met as written. That is worth stating explicitly given the Phase-11/12/13 precedent,
where SC clauses turned out false: here they did not, and the disconfirming findings
that *did* fire (below) are about the **inherited record**, not about this phase's
own criteria.

### 4.2 Findings that cut against expectations

Four fired across the phase and none was softened:

1. **The Landau–Vavilov validity floor lies at 4111.82 eV — above the 10.14 eV v1.0
   grid floor — and indicts 209 of the 584 bins the v1.0 manuscript published**
   (35.79 %, reaching up to 4042.2 eV). Varying the mean excitation energy over
   300–400 eV gives 204–213; no plausible value makes it zero, and the stricter
   reading `ξ/I ≥ 10` would indict far more. Reported as measured.

2. **The electron-side Compton-profile analogue is NOT negligible** — 252 % of the
   deposit at 100 meV, ~86 extended grid bins — so "no broadening because it would
   be unresolvable" would have been a *false* argument. The verdict rests on the
   analogue's own IA validity criterion (`2W_e = 0.157 < 1`) instead.

3. **The recomputed pile-up occupancy is 6.533538e-05, a factor of exactly 2 above
   the v1.0 quoted ~3e-5**, because the v1.0 figure is the 20 µs *sampling*
   occupancy (3.266768e-05) rather than the 40 µs *resolving-time* occupancy — the
   conflation `CONVENTIONS` §F's Numerical Factor Registry names by row. Both
   numbers and their exact 2:1 relation are now asserted in code.

4. **The muon sub-eV region is a bounded absence, not a spectrum.** Not one of its
   160 new bins reaches `adequate_mc_support`; the median relative MC error is 0.868;
   35 have no support at all; and all 160 lie below the validity floor.

And two expected failures that did **not** occur, recorded because the plans required
the answer either way: the **frozen v1.0 CSVs are regenerable** (584/584 bins, both
channels), and the **sub-eV observable is not dominated by the unmeasured trigger
sharpness** (1.10× / 1.39× over k ∈ [1, 12]).

### 4.3 What Phase 16 receives

* `artifacts/v2.0/muon_dRdEdep_ext.csv`, `compton_dRdEdep_ext.csv` — deposit spectra,
  744 bins from 100 meV, per-bin MC errors, adequacy labels, validity-floor flags.
* `artifacts/v2.0/em_dRdErec_ext_TaAl.csv`, `em_dRdErec_ext_AlHf.csv` —
  reconstructed spectra, both channels, both designs, un-triggered and
  trigger-weighted, with bands and regime flags.
* `artifacts/v2.0/em_trigger_k_sensitivity.csv` — so no triggered number can be read
  as though k were measured.
* `artifacts/v2.0/em_accuracy_labels.csv` — the machine-readable labels to propagate.
* `artifacts/v2.0/em_validity_floors.csv` — which bins may be quoted at all.
* `artifacts/v2.0/em_inband_dominance.csv` — the re-checked ordering.
* `src/qpd_potential/em_recoil.py` — a guard that **raises** if an electron-recoil
  channel is ever fed the nuclear IA kernel.

### 4.4 Named gaps handed forward

1. **209 indicted v1.0 muon bins** below the Landau–Vavilov validity floor of
   4111.82 eV. Below that floor the v1.0 muon deposit spectrum is an extrapolation
   of the model rather than a prediction of it. The integral rate and the bulk of
   the channel are untouched (the sub-4 keV deposited tail carries ~1e-4 of the flux).
2. **The neglected Compton-profile Doppler broadening** — real, ≥ 252 % of the
   deposit at 100 meV, and outside its own IA validity domain exactly where it would
   matter. Modelling it would be a new mechanism, which SC1 excluded.
3. **The muon sub-eV region is a bounded absence**, and the Compton region below
   the 0.73955 eV pair-creation floor is not a physical rate whatever the estimator
   returned (70 of 744 extended bins).
4. **The muon channel has no external benchmark on the reconstructed axis at all.**
   The NUCLEUS Table 5 residual comparison was removed by the re-scope, leaving only
   the v1.0 PDG sanity check — whose two legs bracket the adopted rate, so it fixes
   the magnitude and not the sign.
5. **A token scan plus a numeric enumeration is a strong check, not a proof.** A
   quantity re-entering under a new name with a new value would be invisible to both.
6. **Flagged for the orchestrator, not edited here:** `GPD/REQUIREMENTS.md` CALC-19
   and CALC-20 still carry their "replacing the v1.0 …" clauses in their requirement
   *texts*, which the 2026-07-22 re-scope voided. `15-CONTEXT.md` Decision 3 records
   this; no plan in this phase edits `REQUIREMENTS.md`.

---

## 5. Verification ledger

| Acceptance test | Outcome | Evidence |
|---|---|---|
| `test-token-scan-clean` | **PASS** | 0 applied hits over 31 files; 1 justified allowlist entry |
| `test-retired-quantities-named` | **PASS** | all 11 named quantities + the sentinel + 5 factors, each with disposition and reason |
| `test-factors-are-unity` | **PASS** | each of the five checked **individually**, not as a product |
| `test-veto-credit-sentinel` | **PASS** | exactly 1.0, recorded as "by construction" |
| `test-no-conservative-word` | **PASS** | zero occurrences over the scanned scope |
| `test-bands-not-narrowed` | **PASS** | ×0.65…×1.35 encloses the PDG bracket; ×0.5…×2 unchanged |
| `test-sign-carries-anchor-leg` | **PASS** | every occurrence in every emitted artifact |
| `test-labels-reach-artifacts` | **PASS** | per-row labels in all four Plan 15-02/15-03 tables match `em_accuracy_labels.csv` |
| `test-dominance-recomputed` | **PASS** | computed from the 15-03 artifacts; CEvNS total reproduces 118.729 vs 118.730 |
| `test-not-named-sb` | **PASS** | zero occurrences of the forbidden ratio name in any emitted artifact or document |
| `test-labels-on-every-ratio` | **PASS** | all 322 rows carry both labels |
| `test-dimensions` | **PASS** | veto credit dimensionless and exactly 1.0; no signed deviation without its anchor leg |

**Forbidden proxies.** `fp-shielded-quantity-leak` rejected (0 applied hits).
`fp-absence-without-enumeration` rejected (17 enumerated rows with values and
reasons). `fp-product-instead-of-factors` rejected (each factor individually).
`fp-reduced-credit` rejected (exactly 1.0 by construction; no modified geometry
proposed, sized or costed). `fp-conservative-label` rejected (zero occurrences).
`fp-narrowed-band` rejected (bands identical or wider, enclosure asserted).
`fp-bare-sign` rejected (Leg A + bracketing on every occurrence).
`fp-sb-by-another-name` rejected (the ratio here is a channel-magnitude comparison,
explicitly labelled as orientation, with the neutron channel named as the reason it
bounds nothing).
