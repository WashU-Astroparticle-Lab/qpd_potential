---
phase: 07-scenario-nuclear-data-lock
plan: 01
status: blocked
one_liner: "Locked v1.1 radiopurity budget (representative default + electroformed<->commercial band, gamma/(alpha,n)+SF split) and Ge activation scenario (t_exp=1yr/t_cool=0; as-deployed A=4.05/18.2/11.0 dec/kg/day for 3H/68Ge/65Zn, 68Ge/65Zn NOT saturated at 1yr); Input 1 ambient neutron flux BLOCKED — Gordon-2004 coefficients unsourceable in-environment, not fabricated."
plan_contract_ref: GPD/phases/07-scenario-nuclear-data-lock/07-01-PLAN.md
tasks_completed: 2
tasks_total: 3
contract_results:
  claims:
    - id: claim-ambient-flux
      status: blocked
      confidence: n/a
      evidence: "Gordon-2004/JESD89A analytic coefficients paywalled/registration-gated; prior 07-RESEARCH survey (ResearchGate/ADS/Semantic Scholar) + in-environment scripted retrieval both failed; figure not viewable to digitize. Two integrals (3.5e-3 >10 MeV, 1.3e-2 broad) cited but do not fix the differential shape. Deliberately NOT reconstructed from memory (fabrication). data/ambient_neutron_flux_v1.1.csv NOT written."
    - id: claim-radiopurity
      status: produced
      confidence: MEDIUM
      evidence: "data/radiopurity_budget_v1.1.csv: per-component U/Th/40K, single representative default + electroformed-Cu(<0.3 uBq/kg, MAJORANA) <-> commercial(mBq-Bq/kg) bracket; gamma(CALC-07)/(alpha,n)+238U-SF(CALC-08) split, low-Z flagged; conversions re-derived <1% (12.44/4.06 mBq/kg, 31.03 Bq/g); SF 1.353e-11, p_gamma 0.1067 in header. Representative middle is a documented discretionary pick (input-limited until materials list exists)."
    - id: claim-activation-scenario
      status: produced
      confidence: HIGH
      evidence: "data/activation_scenario_v1.1.csv: A=R(1-e^{-lam t_exp})e^{-lam t_cool} verified independently; 3H 4.05, 68Ge 18.2, 65Zn 11.0 dec/kg/day (CDMSlite, 1yr); 68Ge/65Zn at 61%/65% of R (NOT saturated), full saturation t_exp>~3yr; 3H never saturates. Band 0.25-3yr, CDMSlite central/EDELWEISS upper. Anchored arXiv:1806.07043 / arXiv:1607.04560."
    - id: claim-axis-discipline
      status: produced
      confidence: HIGH
      evidence: "Both committed CSVs carry a keV_nr / unified-phonon axis tag; grep of CSVs for keVee/Lindhard/QF/NUCLEUS/CONUS/RELICS = zero; note carries the FORBIDDEN + surface-vs-underground guards as required. CSVs have no energy axis so shared_energy_grid() bin-identity is N/A for them (the grid check attaches to Input 1's blocked flux table)."
  deliverables:
    - id: deliv-ambient-flux
      status: failed
      path: data/ambient_neutron_flux_v1.1.csv
      note: "Not written — blocked on defensible sourcing of the Gordon-2004 spectral shape (see claim-ambient-flux). No fabricated spectrum committed."
    - id: deliv-radiopurity
      status: produced
      path: data/radiopurity_budget_v1.1.csv
    - id: deliv-activation
      status: produced
      path: data/activation_scenario_v1.1.csv
    - id: deliv-scenario-note
      status: produced
      path: docs/v1.1-scenario-assumptions.md
      note: "Covers all three inputs; Input 1 section documents the block + resolution request."
  acceptance_tests:
    - id: test-ambient-integrals
      outcome: blocked
      note: "Cannot run — no committed φ(E_n) to integrate (Input 1 blocked)."
    - id: test-radiopurity-conversions
      outcome: pass
      note: "Round-trip ppb<->activity reproduced to <1% (12.44/4.06 mBq/kg, 31.03 Bq/g); exactly one representative default per component with lo/hi band; gamma and (alpha,n)+SF channel columns present; SF 1.353e-11 recorded."
    - id: test-activation-band
      outcome: pass_with_finding
      note: "A(t) verified. FINDING: at 1yr 68Ge/65Zn are 61%/65% of R (18.2/11.0), NOT the ~30/~17 saturation the plan verify text quoted; as-deployed values committed. 3H 4.05 @1yr non-saturating confirmed. Limiting cases t_exp->0 (A->0) and t_exp->inf (68Ge/65Zn->R, 3H grows) hold."
    - id: test-axis-grep
      outcome: pass
      note: "Zero QF/Lindhard/keVee/underground-import tokens in the two committed CSVs; note carries the guard text by requirement."
  must_surface_refs:
    - id: ref-gordon
      status: missing_required_action
      note: "read/use/compare/cite NOT completed — coefficient set unsourceable in-environment. Root cause of the block."
    - id: ref-majorana
      status: complete
      note: "electroformed-Cu <0.3 uBq/kg lo anchor used + cited in radiopurity budget."
    - id: ref-mzh
      status: complete
      note: "238U SF 1.353e-11 n/g/s/ppb used + cited in radiopurity header."
    - id: ref-cdmslite
      status: complete
      note: "central production rates compared + cited in activation scenario."
    - id: ref-edelweiss
      status: complete
      note: "upper-band rates compared + cited in activation scenario."
    - id: ref-conventions-B
      status: complete
      note: "keV_nr axis discipline + FORBIDDEN guard applied to all artifacts."
  forbidden_proxies:
    - id: fp-quenching
      status: rejected
      note: "No Lindhard/QF applied; all deposits keV_nr on the phonon scale."
    - id: fp-underground-import
      status: rejected
      note: "No NUCLEUS/CONUS/RELICS residual imported; surface baseline set as upper case (documented in note). Also the reason Input 1 was blocked rather than back-filled from a shielded number."
    - id: fp-open-bracket
      status: rejected
      note: "Radiopurity forced to a single representative default per component; >2-order bracket kept only as the band."
    - id: fp-saturation-3H
      status: rejected
      note: "As-deployed A(t) per isotope with its own lambda; 3H flagged non-saturating; 68Ge/65Zn shown below saturation at 1yr."
uncertainty_markers:
  weakest_anchors:
    - "Gordon-2004 analytic coefficients — unsourceable in-environment (BLOCKS Input 1)."
    - "Absolute ambient-neutron normalization: factor-of-a-few, site-dependent (input-limited) — moot until Input 1 unblocked."
    - "Per-component housing assay: input-limited until a QPD materials list exists; representative middle is a documented discretionary pick pending confirmation."
  unvalidated_assumptions:
    - "Scalar building-shielding band understates the indoor spectral-shape systematic (Input 1)."
    - "t_cool=0 worst-case surface framing; a real device spends time shielded during fabrication/transport."
    - "Representative radiopurity middle (commercial OFHC Cu ~tens uBq/kg + PCB/connector ~mBq/kg) pending researcher confirmation."
  disconfirming_observations:
    - "Committed φ(E_n) missing Φ(>10 MeV)=3.5e-3 beyond cited precision (cannot occur yet — no φ committed)."
    - "Any locked number carrying a 0.1-0.3 quenching factor (checked: none)."
    - "Radiopurity band spanning >2 orders with no representative middle (checked: middle forced)."
comparison_verdicts:
  - subject: "ppb<->activity conversions"
    verdict: match
    detail: "12.44 vs 12.4 mBq/kg (U), 4.057 vs 4.06 (Th), 31.03 vs 31 Bq/g (nat-K) — all <1%."
  - subject: "3H as-deployed A @1yr"
    verdict: match
    detail: "4.05 vs plan 4.1 dec/kg/day."
  - subject: "68Ge/65Zn as-deployed A @1yr"
    verdict: finding
    detail: "18.2/11.0 dec/kg/day = 61%/65% of R; plan verify quoted saturation ~30/~17 (reached only at t_exp>~3yr). As-deployed governs per deliverable spec."
---

# Plan 07-01 — Scenario Input-Lock — SUMMARY

**Status: BLOCKED (2 of 3 tasks complete; Task 1 blocked on sourcing; Task 3 human-verify pending).**

## What was done

- **Task 2A — radiopurity budget** → `data/radiopurity_budget_v1.1.csv` (committed `d120b70`).
  Per-component (Cu housing / PCB-readout / connectors / SS-mount; Ge-bulk context-only) U/Th/⁴⁰K budget
  with a single representative default + electroformed-Cu(lo)↔commercial(hi) bracket band; γ (CALC-07) vs
  (α,n)+²³⁸U-SF (CALC-08) channel split with low-Z flags; ppb↔activity conversions and SF yield in the
  header, all re-derived to <1%.
- **Task 2B — activation scenario** → `data/activation_scenario_v1.1.csv` (committed `d120b70`).
  t_exp=1 yr, t_cool=0; per-isotope R, t_half, λ, saturation fraction, and **as-deployed** A verified
  independently; CDMSlite central / EDELWEISS upper band over t_exp ∈ [0.25, 3] yr.
- **Task 3 deliverable — scenario note** → `docs/v1.1-scenario-assumptions.md` (committed `fda5a12`).
  All three inputs (default + band + citation + provenance tag + keV_nr tag), the §B FORBIDDEN guard, the
  surface-vs-underground guard, and the explicit scope-repair trigger. Cross-checked against the CSVs.

## What is blocked — Input 1 (ambient fast-neutron flux)

`data/ambient_neutron_flux_v1.1.csv` was **not written**. Building φ(E_n) requires the Gordon-2004 /
JESD89A analytic coefficient set, which the plan mandates be **sourced or digitized, never reconstructed
from memory**. In this environment the coefficients are paywalled/registration-gated, the prior phase-7
survey already failed to surface them, and the figure cannot be fetched/viewed to digitize. The two
integrals are cited but do not fix the differential shape. Per the plan `stop_and_rethink` condition this
input is **BLOCKED pending scope repair** — no fabricated spectrum was committed.

**Resolution requested (any one):** (a) Gordon-2004/JESD89A coefficient table; (b) a digitized (E_n, φ)
table with source; or (c) explicit authorization to represent φ(E_n) as a labeled physically-motivated
multi-component parametrization normalized to the two cited integrals (a genuine scope change).

## Key results (with confidence)

| Quantity | Value | Confidence |
| --- | --- | --- |
| 1 ppb U / Th ↔ activity | 12.44 / 4.057 mBq/kg (<1% of 12.4 / 4.06) | HIGH |
| nat-K specific activity | 31.03 Bq/g(K) (<1% of 31) | HIGH |
| ³H as-deployed A (CDMSlite, 1 yr) | 4.05 dec/kg/day (never saturates) | HIGH |
| ⁶⁸Ge / ⁶⁵Zn as-deployed A (CDMSlite, 1 yr) | 18.2 / 11.0 dec/kg/day (61% / 65% of R — NOT saturated) | HIGH |
| Radiopurity representative default | Cu ~tens µBq/kg + PCB/connector ~mBq/kg (bracket electroformed↔commercial) | MEDIUM (discretionary) |
| Ambient φ(E_n) | — | BLOCKED |

## Deviations / findings

- **[Finding — Rule 4/5 boundary] ⁶⁸Ge/⁶⁵Zn not saturated at t_exp=1 yr.** The plan verify text quoted
  saturation values (~30/~17) at 1 yr; the correct as-deployed A = R(1−e^{−λt_exp}) gives 18.2/11.0
  (61%/65% of R). Full saturation needs t_exp ≳ 3 yr. Committed the as-deployed values (matches the
  deliverable spec "as-deployed A ... NOT saturation"). Finding, not a bug.
- **[Rule 6 — scope block] Input 1 unsourceable.** Escalated to the orchestrator/researcher per the plan
  `stop_and_rethink` trigger. Not improvised.

## Conventions in effect

keV_nr / unified phonon energy scale (CONVENTIONS §B), NO ionization quenching; per-kg normalization;
provenance-headed frozen CSV pattern (data/gamma_lines.csv). No QFT convention categories apply.

## Checkpoints

| Commit | Content |
| --- | --- |
| `d120b70` | Task 2 — radiopurity + activation CSVs |
| `fda5a12` | Task 3 deliverable — scenario/assumptions note (Input 1 flagged blocked) |

## Human-verify checkpoint (Task 3) — awaiting researcher

Three discretionary defaults presented for confirmation (see the return envelope): (1) ambient-flux
anchor choice — moot until Input 1 is unblocked; (2) radiopurity representative middle; (3) t_exp=1 yr,
t_cool=0. Not self-approved.

## Self-Check: PASSED (for committed artifacts)

Files exist and committed; activation A(t) reproduces from the committed table; conversions <1%; CSV axis
grep clean; note ↔ CSV numbers consistent. Input 1 correctly absent (blocked, not fabricated).
