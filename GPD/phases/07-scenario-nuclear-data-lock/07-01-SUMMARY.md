---
phase: 07-scenario-nuclear-data-lock
plan: 01
status: completed
one_liner: "Locked all three v1.1 gating inputs (3/3): surface ambient fast-neutron phi(E_n) from open-access PARMA/Sato-2015 (v4.10 code), anchored to Gordon-2004 >10MeV=3.55e-3 (native PARMA 3.24e-3 agrees ~9% un-tuned), broad thermal->GeV=1.32e-2, on shared_energy_grid, +downward building band; radiopurity budget (representative default + electroformed<->commercial band, gamma/(alpha,n)+SF split); Ge activation (t_exp=1yr/t_cool=0; A=4.05/18.2/11.0 dec/kg/day for 3H/68Ge/65Zn, 68Ge/65Zn NOT saturated at 1yr). Input-1 Gordon-shape block resolved via documented reference-model change (Gordon coefficients unsourceable -> PARMA shape + Gordon integral anchor)."
plan_contract_ref: GPD/phases/07-scenario-nuclear-data-lock/07-01-PLAN.md
tasks_completed: 3
tasks_total: 3
contract_results:
  claims:
    - id: claim-ambient-flux
      status: produced
      confidence: MEDIUM
      evidence: "data/ambient_neutron_flux_v1.1.csv: surface ground-level phi(E_n) built from open-access PARMA/Sato-2015 (official PARMA v4.10 C++ getNeutSpecCpp + input/neutro/*.inp, WeiMXi/PARMA mirror commit 6ff37ca, retrieved 2026-07-22, compiled unmodified), evaluated at W=100/r_c=2.08GV(NYC)/d=1033 g/cm2(sea level)/g=0.15(ground) on shared_energy_grid() (584 bins, edges byte-identical via np.array_equal). Four canonical features present (thermal/1-over-E/evaporation/cascade). Absolute scale anchored by k=1.096 to Gordon-2004 Phi(10MeV-10GeV)=3.55e-3; PARMA native 3.24e-3 agrees ~9% UN-tuned (independent cross-check). Reconciled integrals: full-range Phi(10MeV-10GeV)=3.55e-3, Phi(thermal->10GeV)=1.32e-2 (~Gordon 1.3e-2); on-grid Phi(10-197MeV)=2.82e-3 (grid ceiling omits ~21% >10MeV cascade tail above 197 MeV, documented). Factor-of-5 downward building-shielding band. Reference-model change (Gordon differential shape unsourceable -> PARMA shape + Gordon integral anchor) documented per USER DECISION 2026-07-22. Shape+coefficients SOURCED, not memory. MEDIUM: absolute norm is factor-of-a-few site-dependent (input-limited)."
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
      evidence: "All three committed CSVs axis-tagged; grep for keVee/Lindhard/QF/NUCLEUS/CONUS/RELICS = zero across all three; note carries the FORBIDDEN + surface-vs-underground guards. Input-1 flux table is on an INCIDENT-NEUTRON-ENERGY (E_n) axis explicitly distinguished from the recoil keV_nr axis (elastic n-Ge fold deferred to Phase 9, no quenching); its E_n bin edges are byte-identical to shared_energy_grid() (np.array_equal on the reconstructed 585-edge vector = True, 584 rows). Radiopurity/activation CSVs have no energy axis (grid bin-identity N/A for those two)."
  deliverables:
    - id: deliv-ambient-flux
      status: produced
      path: data/ambient_neutron_flux_v1.1.csv
      note: "584-row provenance-headed phi(E_n) on shared_energy_grid(); PARMA/Sato-2015 shape (sourced from open PARMA v4.10), Gordon-2004 >10MeV integral anchor, factor-of-5 downward band, (depth,shielding)+E_n axis tags, reconciled >10MeV/broad integrals. Reference-model change documented in header + note."
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
      outcome: pass
      note: "Committed phi(E_n) integrated: full-range Phi(10MeV-10GeV)=3.55e-3 (== Gordon 3.5-3.6e-3 anchor) and Phi(thermal->10GeV)=1.32e-2 (~Gordon broad 1.3e-2); labels reconciled in header (two ranges of one spectrum). On-grid Phi(10-197MeV)=2.82e-3 with the ~21% >197MeV cascade-tail omission explicitly documented (anchor defined on full range, not on-grid). (depth,shielding)+E_n axis tags present; shape coefficient source cited (PARMA v4.10 / Sato 2015 / WeiMXi mirror commit 6ff37ca), not memorized. E_n grid edges byte-identical to shared_energy_grid()."
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
      status: complete
      note: "Role revised by documented reference-model change (USER DECISION 2026-07-22): Gordon differential COEFFICIENTS remain unsourceable in-environment, so Gordon is used as the NORMALIZATION BENCHMARK (compare/cite done) rather than the shape source. Committed phi(E_n) anchored to Gordon Phi(10MeV-10GeV)=3.55e-3 (integral re-confirmed via open DarkSide-20k arXiv:2301.12970); native PARMA agrees ~9% un-tuned. Differential SHAPE now sourced from open-access Sato 2015 PLOS ONE e0144679 + PARMA v4.10 code (WeiMXi mirror commit 6ff37ca) — added as the shape reference; see CSV header and scenario note."
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
    - "Absolute ambient-neutron normalization: factor-of-a-few, site-dependent (input-limited, not method-limited). Anchored to Gordon >10 MeV; the ~21% of the >10 MeV flux above the 197 MeV grid ceiling is off-grid (accounted in the anchor, not in the on-grid table)."
    - "Building-shielding band is a pure scalar; roof/wall moderation reshapes the spectrum (fast->thermal) — scalar band understates that spectral-shape systematic (Phase-8/12 sensitivity)."
    - "Per-component housing assay: input-limited until a QPD materials list exists; representative middle is a documented discretionary pick (accepted)."
  unvalidated_assumptions:
    - "Scalar building-shielding band understates the indoor spectral-shape systematic (Input 1)."
    - "PARMA evaluated at NYC-representative r_c=2.08 GV / sea-level / mid-solar W=100; a different deployment site needs re-evaluation at its (d, r_c). Shape is fairly site-insensitive above 10 MeV; absolute scale is anchored to Gordon regardless."
    - "t_cool=0 worst-case surface framing; a real device spends time shielded during fabrication/transport."
    - "Representative radiopurity middle (commercial OFHC Cu ~tens uBq/kg + PCB/connector ~mBq/kg) — accepted by user."
  disconfirming_observations:
    - "Committed φ(E_n) anchor Φ(10 MeV-10 GeV)=3.55e-3 (on target); native PARMA 3.24e-3 within ~9% (checked: consistent)."
    - "Any locked number carrying a 0.1-0.3 quenching factor (checked: none; grep clean across all three CSVs)."
    - "Radiopurity band spanning >2 orders with no representative middle (checked: middle forced)."
comparison_verdicts:
  - subject: "PARMA/Sato-2015 native vs Gordon-2004 >10 MeV integral"
    verdict: match
    detail: "PARMA native Phi(10MeV-10GeV)=3.24e-3 vs Gordon 3.5-3.6e-3 — agree to ~9% with NO tuning; broad thermal->GeV 1.20e-2 vs Gordon ~1.3e-2 (~8%). Independent cross-check of shape+scale; anchor factor k=1.096 is a small adjustment."
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

**Status: COMPLETE (3 of 3 tasks; all three gating inputs locked). Human-verify checkpoint resolved by
USER DECISION 2026-07-22 (three discretionary defaults accepted; Input-1 Gordon-shape block resolved via
documented reference-model change).**

## What was done

- **Task 1 — ambient fast-neutron flux** → `data/ambient_neutron_flux_v1.1.csv` (this run).
  584-row provenance-headed φ(E_n) on `shared_energy_grid()`. Differential **shape** from the open-access
  **PARMA/Sato-2015** model (official PARMA v4.10 C++ `getNeutSpecCpp` + `input/neutro/*.inp`, mirror
  `github.com/WeiMXi/PARMA` commit `6ff37ca`, retrieved 2026-07-22, compiled unmodified) evaluated at
  W=100 / r_c=2.08 GV (NYC) / d=1033 g/cm² (sea level) / g=0.15 (ground). Absolute scale **anchored** by
  k=1.096 to Gordon-2004 Φ(10 MeV–10 GeV)=3.55×10⁻³; PARMA native 3.24×10⁻³ agrees ~9% un-tuned. Factor-of-5
  downward building-shielding band; (depth,shielding) + incident-neutron-energy (E_n) axis tags.
- **Task 2A — radiopurity budget** → `data/radiopurity_budget_v1.1.csv` (committed `d120b70`, prior run).
  Per-component (Cu housing / PCB-readout / connectors / SS-mount; Ge-bulk context-only) U/Th/⁴⁰K budget
  with a single representative default + electroformed-Cu(lo)↔commercial(hi) bracket band; γ (CALC-07) vs
  (α,n)+²³⁸U-SF (CALC-08) channel split with low-Z flags; ppb↔activity conversions + SF yield, <1%.
- **Task 2B — activation scenario** → `data/activation_scenario_v1.1.csv` (committed `d120b70`, prior run).
  t_exp=1 yr, t_cool=0; per-isotope R, t_half, λ, saturation fraction, and **as-deployed** A verified
  independently; CDMSlite central / EDELWEISS upper band over t_exp ∈ [0.25, 3] yr.
- **Task 3 deliverable — scenario note** → `docs/v1.1-scenario-assumptions.md` (updated this run).
  All three inputs (default + band + citation + provenance tag + axis tag), §B FORBIDDEN guard,
  surface-vs-underground guard, scope-repair trigger. Input-1 section updated BLOCKED→LOCKED.

## Input 1 resolution — reference-model change (documented)

The plan originally specified the **Gordon-2004 / JESD89A differential coefficients** for the neutron
spectral shape. Those are paywalled/registration-gated and were **unsourceable in-environment**; the first
run correctly BLOCKED rather than reconstruct them from memory. Per **USER DECISION 2026-07-22**, the shape
source was changed to the **fully open-access PARMA/Sato-2015** model (Sato, PLOS ONE 10(12):e0144679; the
PLOS paper gives functional forms Eqs (4)–(6) and states the fitted coefficients ship in EXPACS/PARMA — so
coefficients were taken from the open PARMA v4.10 source, not typed from memory), while **Gordon-2004 is
retained as the absolute-normalization benchmark** via the >10 MeV integral anchor. Both shape and scale are
sourced; the ~9% native PARMA↔Gordon agreement makes the anchor a small, physical adjustment. No fabrication.

## Key results (with confidence)

| Quantity | Value | Confidence |
| --- | --- | --- |
| φ(E_n) anchor Φ(10 MeV–10 GeV) | 3.55×10⁻³ cm⁻²s⁻¹ (Gordon; PARMA native 3.24×10⁻³, ~9% un-tuned) | MEDIUM (site-dependent norm) |
| φ(E_n) broad Φ(thermal→10 GeV) | 1.32×10⁻² cm⁻²s⁻¹ (~Gordon 1.3×10⁻²) | MEDIUM |
| 1 ppb U / Th ↔ activity | 12.44 / 4.057 mBq/kg (<1% of 12.4 / 4.06) | HIGH |
| nat-K specific activity | 31.03 Bq/g(K) (<1% of 31) | HIGH |
| ³H as-deployed A (CDMSlite, 1 yr) | 4.05 dec/kg/day (never saturates) | HIGH |
| ⁶⁸Ge / ⁶⁵Zn as-deployed A (CDMSlite, 1 yr) | 18.2 / 11.0 dec/kg/day (61% / 65% of R — NOT saturated) | HIGH |
| Radiopurity representative default | Cu ~tens µBq/kg + PCB/connector ~mBq/kg (bracket electroformed↔commercial) | MEDIUM (discretionary) |

## Deviations / findings

- **[Rule 6 → resolved] Input 1 reference-model change.** Gordon differential coefficients unsourceable
  in-environment; the first run BLOCKED (not improvised). Resolved by user decision: PARMA/Sato-2015 shape +
  Gordon integral anchor. Documented in the CSV header, the scenario note (§1), and here.
- **[Finding — Rule 4/5 boundary] ⁶⁸Ge/⁶⁵Zn not saturated at t_exp=1 yr.** The plan verify text quoted
  saturation values (~30/~17) at 1 yr; the correct as-deployed A = R(1−e^{−λt_exp}) gives 18.2/11.0
  (61%/65% of R). Full saturation needs t_exp ≳ 3 yr. Committed the as-deployed values. Finding, not a bug.
- **[Note] Grid ceiling.** `shared_energy_grid()` tops at ~197 MeV; ~21% of the >10 MeV flux lies in the
  197 MeV–10 GeV cascade tail. The >10 MeV **anchor** is the full-range PARMA integral; the on-grid subset
  (Φ(10–197 MeV)=2.82×10⁻³) is recorded separately and the omission is documented.

## Conventions in effect

keV_nr / unified phonon energy scale (CONVENTIONS §B), NO ionization quenching; per-kg normalization;
provenance-headed frozen CSV pattern (data/gamma_lines.csv). Input-1 table is on an **incident-neutron-energy
(E_n)** axis, explicitly distinct from the recoil keV_nr axis (elastic n-Ge fold = Phase 9, no quenching).
No QFT convention categories apply.

## Checkpoints

| Commit | Content |
| --- | --- |
| `d120b70` | Task 2 — radiopurity + activation CSVs (prior run) |
| `fda5a12` | Task 3 deliverable — scenario/assumptions note (prior run) |
| `78f7728` | SUMMARY — inputs 2-3 locked, input 1 blocked (prior run) |
| (this run) | Task 1 — ambient neutron flux CSV (PARMA/Sato, Gordon-anchored) + note/SUMMARY update to 3/3 |

## Self-Check: PASSED

All three CSVs exist and committed; φ(E_n) integrals reproduce from the committed table (anchor 3.55×10⁻³,
broad 1.32×10⁻²); E_n grid edges byte-identical to `shared_energy_grid()` (np.array_equal=True, 584 rows);
band relations phi_lo=phi/5, phi_hi=phi hold; activation A(t) reproduces; conversions <1%; forbidden-token
grep (keVee/Lindhard/QF/NUCLEUS/CONUS/RELICS) clean across all three CSVs; note ↔ CSV numbers consistent.
