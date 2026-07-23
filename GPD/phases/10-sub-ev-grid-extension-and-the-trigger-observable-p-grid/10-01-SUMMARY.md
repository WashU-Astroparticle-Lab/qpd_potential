---
phase: 10-sub-ev-grid-extension-and-the-trigger-observable-p-grid
plan: 01
status: complete
one_liner: "Out-of-domain interpolation is now an exception at 7 call sites; the decisive pre-fix witness is that fold._erec_of_edep returned 4.899066 eV for a 0.1 eV deposit -- the clamped 10.14 eV answer, a factor-49 overstatement with no error -- and 13 of 24 new boundary tests fail against the unguarded code."
plan_contract_ref: GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-01-PLAN.md#/contract

contract_results:
  claims:
    claim-raises:
      status: passed
      summary: "All 7 guarded tabulated-input call sites raise InterpolationDomainError just outside both declared bounds and return finite, non-NaN values exactly at both bounds. Zero guarded sites clamp, slope-extrapolate past the declared domain, return NaN, or return 0.0 outside it. Non-vacuity is demonstrated: with the guard helper present but the call sites unguarded, 13 of the 24 new tests fail, including every per-site test."
      linked_ids: [deliv-guard, deliv-tests, deliv-inventory, test-raise-at-floor, test-witness-pre-fix, test-domain-extension-witness, test-no-regression]
      evidence:
        - verifier: gpd-executor
          method: pre-fix witness measurement then post-fix assertion, plus a pristine-HEAD re-run
          confidence: high
          claim_id: claim-raises
          deliverable_id: deliv-tests
          acceptance_test_id: test-witness-pre-fix
          reference_id: ref-phase7-gapd3
          forbidden_proxy_id: fp-vacuous-guard
          evidence_path: GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-01-INTERPOLATOR-INVENTORY.md
    claim-inventory:
      status: passed
      summary: "The enumeration is a recorded grep re-run by the test suite: 33 hits, 33 inventory rows, 7 GUARDED and 26 excluded, every row carrying a non-empty written justification. The 6 extra hits relative to the 27 found pre-guard are prose strings introduced by this plan and are enumerated and excluded individually rather than filtered out by a pattern tweak."
      linked_ids: [deliv-inventory, test-inventory-closure]
  deliverables:
    deliv-guard:
      status: passed
      path: src/qpd_potential/interp_guard.py
      summary: "InterpolationDomainError (a named ValueError subclass) plus a frozen Domain dataclass carrying lo/hi, the abscissa units, the table provenance path, the tabulated span, and witness strings. Domain.__post_init__ RAISES AT CONSTRUCTION if a declared bound falls outside the tabulated span with no witness, so an unwitnessed extension cannot be shipped. check_domain rejects scalars and arrays alike and rejects non-finite abscissae."
      linked_ids: [claim-raises, test-raise-at-floor]
    deliv-tests:
      status: passed
      path: tests/test_interpolator_bounds.py
      summary: "24 tests. Per guarded site: raises at lo*(1-1e-9) and hi*(1+1e-9), finite at lo and hi exactly, and the recorded pre-fix clamped/extrapolated value asserted unreachable. Plus the inventory-closure tests that re-run the grep."
      linked_ids: [claim-raises, claim-inventory]
    deliv-inventory:
      status: passed
      path: GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-01-INTERPOLATOR-INVENTORY.md
      summary: "33-row table with the literal grep command and its raw output, per-row tabulated span read from the frozen file at run time, declared domain, measured pre-fix out-of-domain return, verdict and justification; plus the witness table for the two declared extensions and four residual findings recorded rather than fixed."
      linked_ids: [claim-raises, claim-inventory]
  acceptance_tests:
    test-raise-at-floor:
      status: passed
      summary: "Every guarded site raises at declared_lo*(1-1e-9) and declared_hi*(1+1e-9) and returns a finite non-NaN value at declared_lo and declared_hi exactly. Zero guarded sites return NaN, 0.0, or a clamped edge value outside the domain."
      linked_ids: [claim-raises, deliv-tests, deliv-guard]
    test-witness-pre-fix:
      status: passed
      summary: "PASS with the informative outcome. FIVE call sites previously returned a finite non-error value outside their tabulated span, so the guard is not vacuous. The load-bearing one: fold._erec_of_edep returned 4.899065996392436 eV for 0.1 eV, 0.5 eV and 1 eV alike -- the clamped E_rec of a 10.144970 eV deposit, E_rec/E_dep = 49 instead of ~0.5. A sixth site returned NaN."
      linked_ids: [claim-raises, deliv-inventory, deliv-tests]
    test-domain-extension-witness:
      status: passed
      summary: "Two declared extensions, both witnessed, and the witness requirement is enforced in code by Domain.__post_init__. mu_over_rho [200,3000] keV vs table [600,2000]: witnesses Pb-214 241.997 keV and Tl-208 2614.511 keV, both real gamma lines the v1.0 Compton channel folds. incoherent_S [0,inf) vs table [1e-3, 4.2646e4]: witnesses exact forward scatter x=0 and the x=1e6 evaluation in tests/test_compton_source.py."
      linked_ids: [claim-raises, deliv-inventory]
    test-inventory-closure:
      status: passed
      summary: "test_inventory_closure_grep_hits_equal_inventory_rows re-runs the recorded grep in a subprocess: 33 hits == 33 rows, every hit present as a `path:line` key, every row with verdict in {GUARDED, excluded} and a justification longer than 20 characters."
      linked_ids: [claim-inventory, deliv-inventory]
    test-no-regression:
      status: passed
      summary: "Full suite before the guard: 313 passed. After: 349 passed, 0 failed. The delta is +24 new boundary tests and +12 from tests/test_env_v1_identity.py, which Phase 9 added to the same worktree concurrently and which is not this plan's work. Zero pre-existing tests changed status."
      linked_ids: [claim-raises, deliv-tests]
  references:
    ref-roadmap-p10:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "ROADMAP Phase 10 success criterion 3 and its forbidden-proxy line are quoted verbatim at the head of the inventory and drive the raise-not-clamp requirement at every guarded site."
    ref-conventions:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "CONVENTIONS A.1 fixes that each declared bound is recorded in the units of its own abscissa; section 7 of the inventory tabulates all six unit systems. CONVENTIONS E is untouched: no efficiency, no tabulated value, and no physics constant was modified."
    ref-phase7-gapd3:
      status: completed
      completed_actions: [read, compare]
      missing_actions: []
      summary: "The Phase-7 D3 vacuous-metric failure is the reason Task 1 ran before any guard existed. Compared directly: this guard's tests were re-run against a pristine HEAD checkout with the guard helper present and the call sites unguarded, and 13 of 24 failed."
  forbidden_proxies:
    fp-vacuous-guard:
      status: rejected
      notes: "Rejected by measurement, not by assertion. A detached git worktree at HEAD was created, the guard HELPER copied in but the four call-site modules left unguarded, and the boundary suite re-run: 13 failed / 11 passed, with every per-site test among the failures. The 11 that still passed are the guard-helper unit tests and the in-domain invariance tests, which are supposed to pass either way."
    fp-domain-widening:
      status: rejected
      notes: "No test was silenced by widening a domain: the full pre-existing suite passed unchanged (313 -> 313 of the pre-existing tests) with no domain adjusted after the fact. The two declared extensions were chosen from the gamma-line table and the forward-scatter kinematics BEFORE the suite was re-run, and the witness requirement is enforced at Domain construction so an unwitnessed widening raises immediately."
    fp-nan-instead-of-raise:
      status: rejected
      notes: "cevns.ReactorFlux._log_phi's PchipInterpolator(extrapolate=False) NaN return is replaced by a raise via log_phi_guarded. check_domain additionally treats a non-finite abscissa as out of domain, because NaN compares False against both bounds and would otherwise slip through every comparison."
    fp-grep-by-recall:
      status: rejected
      notes: "The inventory table is generated from the literal grep output, and the test suite re-runs the same command in a subprocess and fails if the hit set changes. The planning-supplied candidate list was used only as a cross-check; it missed nothing but it was not the source."
  uncertainty_markers:
    weakest_anchors:
      - "The GUARDED / excluded boundary is a judgement call. The two constructed-grid exclusions (muon_deposit.py:164 inverse-CDF sampler, response.py:613 Poisson thinning) are defensible because their abscissae are drawn from rng.uniform over the constructed grid itself, but that reasoning is the weakest link in the closure claim."
      - "compton_source.mu_over_rho slope-extrapolates a FOUR-POINT NIST XCOM table by design. The declared [200, 3000] keV domain makes the extrapolation explicit and bounded; it does not make it validated. The 200 keV floor is a physics judgement (photoabsorption in Ge turns up below it), not a measured breakdown point."
      - "The incoherent_S bounds guard is VACUOUS for every finite non-negative x, because exact forward scatter genuinely produces x = 0 and S(x->inf) = Z is the exact asymptote. Recorded plainly in the inventory rather than presented as a fix."
      - "src/nuclear/parse_endf_nGe.py and src/flux/assemble_spectrum.py are excluded as frozen data-preparation scripts. assemble_spectrum.py:122 uses PchipInterpolator(extrapolate=True), so the outermost points of the frozen v1.0 flux table may be extrapolated rather than tabulated. Reported, not patched."
    unvalidated_assumptions:
      - "That the recorded grep pattern catches every interpolation route. A hand-rolled interpolation written as arithmetic rather than as a call to np.interp or a scipy class would not be found."
      - "That declaring mu_over_rho valid down to 200 keV is defensible. No measurement bounds the extrapolation error there; the bound is reasoned from where photoabsorption starts to dominate in Ge."
    competing_explanations:
      - "The wafer_self_veto._tail_integral pre-fix return could be argued as harmless, since a_self_direct short-circuits before reaching it and the value at 1e-4 keV was within 1.5e-7 of the true integral. The counter-reading, adopted here, is that a fabricated number that is almost exactly right is the worst kind: it survives every plausibility check."
    disconfirming_observations:
      - "DID NOT OCCUR: 'no call site ever returned a finite value outside its table span'. Five did, so the guard is not defending against a failure mode this pipeline lacks."
      - "DID NOT OCCUR: 'the existing pytest suite starts failing after the guard is installed'. The pre-existing 313 tests all still pass, so no latent out-of-domain evaluation was exposed in v1.0 physics by this guard."
      - "STILL OPEN and inherited by plan 10-03: the guarded fold._erec_of_edep call site is exactly the one the 0.1 eV extension will drive out of domain. Plan 10-04 must supply a response curve whose deposit floor is 0.1013838 eV, or that guard will fire in production."
files_created:
  - src/qpd_potential/interp_guard.py
  - tests/test_interpolator_bounds.py
  - GPD/phases/10-sub-ev-grid-extension-and-the-trigger-observable-p-grid/10-01-INTERPOLATOR-INVENTORY.md
files_modified:
  - src/qpd_potential/cevns.py
  - src/qpd_potential/compton_source.py
  - src/qpd_potential/fold.py
  - src/qpd_potential/wafer_self_veto.py
---

# Plan 10-01 Summary --- Interpolator Bounds Guard

## What was actually established

Seven tabulated-input interpolation call sites now raise `InterpolationDomainError` outside a
**declared** evaluation domain instead of clamping, slope-extrapolating without limit,
returning NaN, or returning zero. ROADMAP Phase 10 success criterion 3.

## The decisive number

`fold._erec_of_edep` maps deposited energy to the Phase-5 median reconstructed energy. Its
abscissa floor is the response matrix's first deposit centre, **10.144970 eV**. Before this
plan, `np.interp` clamped below that floor:

| E_dep asked for | E_rec returned (pre-fix) | E_rec / E_dep | physically expected |
|---|---|---|---|
| 10.144970 eV | 4.899065996392436 eV | 0.483 | 0.483 (in domain, correct) |
| 1.0 eV | 4.899065996392436 eV | 4.9 | ~0.5 |
| 0.5 eV | 4.899065996392436 eV | 9.8 | ~0.5 |
| 0.1 eV | 4.899065996392436 eV | **49** | ~0.5 |

A finite, plausible, non-NaN, **factor-49-wrong** answer, identical for every sub-floor
deposit --- a flat invented plateau sitting exactly where plan 10-03 extends the axis. This is
the single strongest justification for ordering 10-01 before 10-03.

## Non-vacuity check (`fp-vacuous-guard`, Phase-7 D3)

Method, so it can be re-run:

```bash
git worktree add --detach /tmp/prefix_tree HEAD
cp tests/test_interpolator_bounds.py                 /tmp/prefix_tree/tests/
cp GPD/phases/10-.../10-01-INTERPOLATOR-INVENTORY.md /tmp/prefix_tree/GPD/phases/10-.../
cp src/qpd_potential/interp_guard.py                 /tmp/prefix_tree/src/qpd_potential/
cd /tmp/prefix_tree && python -m pytest tests/test_interpolator_bounds.py -q
```

The guard *helper* is copied in (so the module imports) but the four call-site modules are
left unguarded. Result: **13 failed, 11 passed.** Every per-site guard test is among the 13:

```
FAILED test_reactor_flux_pchip_raises_instead_of_returning_nan
FAILED test_rel_uncertainty_raises_and_prefix_clamp_unreachable
FAILED test_nucleus_fig1_loglog_raises_outside_the_digitized_span
FAILED test_xcom_raises_outside_the_declared_domain
FAILED test_xcom_declared_extension_has_a_witness_inside_it
FAILED test_xcom_low_energy_extrapolation_is_no_longer_unbounded
FAILED test_incoherent_S_declared_domain_is_unbounded_and_witnessed
FAILED test_incoherent_S_rejects_negative_momentum_transfer
FAILED test_erec_of_edep_raises_below_the_response_floor
FAILED test_erec_of_edep_prefix_clamped_plateau_is_unreachable
FAILED test_tail_integral_raises_outside_the_frozen_grid
FAILED test_tail_integral_prefix_values_unreachable
FAILED test_inventory_closure_grep_hits_equal_inventory_rows
```

with, for the load-bearing one:

```
        for probe in (0.1, 0.5, 1.0):
>           with pytest.raises(InterpolationDomainError) as ei:
E           Failed: DID NOT RAISE
```

The 11 that pass either way are the guard-helper unit tests and the in-domain invariance
tests; they are supposed to pass either way, and they do not carry the claim.

## The seven guarded sites

| Site | Declared domain | Units | Pre-fix out-of-domain return |
|---|---|---|---|
| `cevns.py:235` `ReactorFlux._log_phi` | [0.1, 10.0] | MeV | **NaN** |
| `cevns.py:287` `rel_uncertainty` | [0.1, 10.0] | MeV | clamped 0.25 / 0.05 |
| `cevns.py:672` `_interp_loglog` (NUCLEUS Fig.1) | [1.020494, 1578.476] | eV | clamped 494.7631 / 0.5185263 |
| `compton_source.py:175` `mu_over_rho` | **[200, 3000]** (witnessed) | keV | 0.11879 / 0.0360649 by slope extrapolation |
| `compton_source.py:265` `incoherent_S` | **[0, +inf)** (witnessed) | dimensionless x | 6.677e-08 at 1e-5; **0.0 at x = -1.0** |
| `fold.py:554` `_erec_of_edep` | [10.144970, 1.97142e8] | eV | **4.899065996392436 eV** |
| `wafer_self_veto.py:325` `_tail_integral` | [1.014497e-02, 1.97142e5] | keV | 1073307.752 at 1e-4 keV; **0.0** above ceiling |

## Two declared extensions, both witnessed and both enforced in code

`Domain.__post_init__` raises at construction if a bound lies outside the tabulated span with
no witness string, so an unwitnessed widening cannot be committed. That is the structural
answer to `fp-domain-widening`.

- **`mu_over_rho`, [200, 3000] keV vs table [600, 2000] keV.** Witnesses: the Pb-214
  **241.997 keV** and Tl-208 **2614.511 keV** gamma lines in `data/gamma_lines.csv`, both
  folded by the v1.0 Compton channel and both already asserted by
  `tests/test_compton_source.py::test_xcom_extrapolation_monotone_and_reasonable`. Raising at
  the table span would break those v1.0 anchors. The declared floor stops at 200 keV because
  photoabsorption in Ge dominates below it and a log-log continuation of the Compton-regime
  interval would be badly wrong there. **The guard makes this extrapolation visible; it does
  not make it correct.**
- **`incoherent_S`, [0, +inf) vs table [1e-3, 4.2646e4].** Stated plainly: **the bounds guard
  here is vacuous for every finite non-negative x.** Exact forward scatter gives x = 0
  identically, and S(x -> inf) = Z = 32 is the exact free-electron asymptote, so neither bound
  can be narrowed without breaking the v1.0 Compton channel. What the guard does catch is real
  but narrow: a **negative momentum transfer**, previously mapped to 1e-300 by `np.maximum`
  and returned as S = 0.0.

## What was deliberately NOT changed

`ReactorFlux.flux()` still returns **0.0** outside the tabulated E_nu support. That is a
declared v1.0 truncation of the flux support, applied *before* the interpolator is reached ---
not a clamp of it. Changing it would move v1.0 physics rather than error behaviour, which this
plan is not permitted to do. It is recorded as residual finding 3 in the inventory and pinned
by `test_reactor_flux_zero_support_truncation_is_preserved`, so the distinction between "the
interpolator clamps" and "the model truncates the support" is on the record and testable.

No tabulated value, no `params` constant, no censoring convention, and no file under `data/`
or `artifacts/` was modified.

## Regression triage

| Run | Result |
|---|---|
| `pytest tests/` before | **313 passed** |
| `pytest tests/` after | **349 passed**, 0 failed |

The +36 decomposes as **+24** new boundary tests from this plan and **+12** from
`tests/test_env_v1_identity.py`, which **Phase 9 added to the same worktree concurrently** and
which is not this plan's work. Zero pre-existing tests changed status, so nothing had to be
triaged as either a latent v1.0 out-of-domain evaluation or an over-tight guard.

That is itself worth stating against expectation: the plan's disconfirming-observation list
anticipated that installing the guard might expose a latent out-of-domain evaluation in v1.0
physics. **It did not.** Every v1.0 evaluation point sits inside its declared domain.

## Handoff to plan 10-03

The `fold._erec_of_edep` guard is now live and its floor is 10.144970 eV. The plan 10-03
extension takes the deposit axis to 0.1013838 eV. Plan 10-04 must therefore supply a response
curve on the extended axis, or this guard fires in production --- which is exactly the
behaviour the criterion asks for, and exactly why it had to land first.
