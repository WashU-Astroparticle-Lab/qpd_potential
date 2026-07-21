---
phase: 03-cevns-cross-section-rate
verified: "2026-07-20T00:00:00Z"
status: expert_needed
score: "21/21"
plan_contract_ref: GPD/phases/03-cevns-cross-section-rate/03-02-PLAN.md#/contract
contract_results:
  claims:
    claim-billard:
      status: passed
      summary: "Plan 03-02, VALD-01 decisive benchmark. INDEPENDENTLY REPRODUCED by folding the Billard-variant CSV with my own dsigma/dT and my own k. k_single=(8.54/3)(25/400)^2=0.011120 and two-core k=0.011092 agree to 0.25% (<1%); k-rescaled integral flux 5.10e10. WITH k the per-isotope Ge sum gives 0.7415/0.5009/0.2567 counts/kg/day above 50/100/200 eV_nr vs Billard Table 1 0.76/0.51/0.26 (-2.4/-1.8/-1.3%, all <2.5% << 20% tolerance). WITHOUT k the fold overshoots by a uniform 89.9x = 1/k (66.68/45.05/23.09) -- fp-billard-norm regression. Both powers thermal (GW_th), distance squared (fp-gwe-gwth rejected). ROADMAP >20% backtrack trigger NOT met (100/200 eV bins <2%)."
      linked_ids: [deliv-billard-report, deliv-billard-tests, test-billard, test-k-derivation, ref-billard, ref-billard-flux]
    claim-band:
      status: passed
      summary: "Plan 03-02. VERIFIED IN MECHANISM WITH A DOCUMENTED MAGNITUDE CORRECTION. CONUS+ cross-check: flagship and Billard-Table-1 both rescaled to CONUS+ config give ratio 0.99 (within factor 2; eV_ee quenching caveat -> coarse scale check). Flux-band propagation independently reproduced: fractional 1sigma band = 3.5% (200 eV), 6.2% (50 eV), 9.8% (20 eV); sub-1.8-MeV rate fraction = ~0 (>=95 eV), 17.8% (50 eV), 33.8% (20 eV). The band WIDENS below ~95 eV and is narrow above 200 eV, and the sub-1.8 toggle is localized below ~95 eV (T>200 eV unchanged <1e-3) -- the QUALITATIVE claim holds exactly. The plan's guessed '20-25% below 95 eV' MAGNITUDE is NOT reproduced (true band 6-10%): the well-anchored (2-5%) >1.8 MeV flux dominates the rate integrand at every recoil. This is an honest downward refinement from actual computation, reported as BOTH the band and the sub-1.8 fraction (no fp-hide-band), not a failure. Recommend orchestrator reword claim-band."
      linked_ids: [deliv-dep-figure, deliv-drdt-band-csv, deliv-billard-tests, test-conus, test-band, ref-conus, ref-flagship-flux-v2]
  deliverables:
    deliv-billard-report:
      status: passed
      path: artifacts/stage1/BILLARD_REPRODUCTION.md
      summary: "k breakdown (single 0.0111198 vs two-core 0.0110917, 0.25%), reproduced 0.7415/0.5009/0.2567 vs 0.76/0.51/0.26 with %-agreement, the without-k 89.9x=1/k table, CONUS+ ratio 0.99, and the matched Billard assumptions (HM constant <2 MeV, fractions 55.6/32.6/7.1/4.7, no n-capture, per-isotope sum). All numbers reproduced independently."
      linked_ids: [claim-billard]
    deliv-dep-figure:
      status: passed
      path: artifacts/stage1/cevns_dRdT_deposited.pdf
      summary: "PDF present (39 KB): dR/dT vs deposited T_nr with the propagated band and the ~95 eV band-widening boundary; regenerable via scripts/gen_cevns_figure.py. Content not pixel-inspected but the underlying arrays (CSV total+band) are independently verified."
      linked_ids: [claim-band]
    deliv-drdt-band-csv:
      status: passed
      path: artifacts/stage1/cevns_dRdT.csv
      summary: "The 03-01 CSV band column (dRdT_band_1sigma) is the propagated flux rel_uncertainty fold; independently reproduced at 20/50/200 eV (see comparison ledger). Same artifact as deliv-drdt-csv, confirmed carrying the band used by the figure and test-band."
      linked_ids: [claim-band]
    deliv-billard-tests:
      status: passed
      path: tests/test_cevns_billard.py
      summary: "11 tests: k-derivation two-way, Billard within 20% WITH k, 100/200 backtrack guard, without-k ~90x regression, CONUS+ factor-2, band narrow>200eV, band widens<95eV, sub-1.8 toggle localized, high-T toggle-invariance, CSV band consistency. All pass. Tests assert the TRUE band behavior (widening + localization), not the plan-guessed 20-25% magnitude."
      linked_ids: [claim-billard, claim-band]
  acceptance_tests:
    test-k-derivation:
      status: passed
      summary: "k=(P_B/P_v)(G_B/G_v): single-source (8.54 GW/400 m) 0.011120 vs two-core (4.27 GW at 355.39 & 468.76 m) 0.011092 agree 0.25% (<1%); k-rescaled Billard integral flux 5.10e10 nu cm^-2 s^-1 (target ~5.1e10). Guard brackets k in [0.006,0.05]: a 1/d error -> ~0.18, a GW_e error -> ~0.004 (fp-gwe-gwth rejected). Independently reproduced."
      linked_ids: [claim-billard, deliv-billard-report, deliv-billard-tests]
    test-billard:
      status: passed
      summary: "WITH k: 0.7415/0.5009/0.2567 vs 0.76/0.51/0.26, all within 2.5% (<< 20%). WITHOUT k: 66.68/45.05/23.09, uniform 89.9x=1/k overshoot (regression). Independently reproduced by my own fold of the variant CSV. 100/200 eV bins <2% -> no ROADMAP backtrack."
      linked_ids: [claim-billard, deliv-billard-report, deliv-billard-tests, ref-billard]
    test-conus:
      status: passed
      summary: "Flagship (67.75 >50 eV) and Billard-Table-1 both rescaled to CONUS+ config (3.6 GW_th/20.7 m) by (P/P')(d'/d)^2 give 118.6 vs 119.6, ratio 0.99 (within factor 2). Two independently-normalized flux models agree at a common config. CAVEAT: CONUS+ reports eV_ee (ionization), needs a quenching model -> coarse rate-scale check, not a direct spectrum match (MEDIUM)."
      linked_ids: [claim-band, deliv-billard-report, ref-conus]
    test-band:
      status: passed
      summary: "PASSED AS IMPLEMENTED (asserts true behavior), WITH A DOCUMENTED PLAN-MAGNITUDE CORRECTION. Band narrow 3.5-4.8% for T>=200 eV (matches '2-5%'); widens below 95 eV (6.2% at 50 eV, 9.8% at 20 eV, all <15%); sub-1.8-MeV zeroing changes T<95 eV substantially (>25% at 20 eV, >10% at 50 eV) and leaves T>200 eV unchanged (<1e-3). All independently reproduced. The plan pass_condition literal '20-25% below 95 eV' is NOT met (true 6-10%); the implemented test correctly asserts the widening+localization structure instead. See comparison verdict cmp-band-magnitude."
      linked_ids: [claim-band, deliv-dep-figure, deliv-drdt-band-csv, ref-flagship-flux-v2]
  references:
    ref-billard:
      status: completed
      completed_actions: [compare, cite]
      missing_actions: []
      summary: "Billard 2017 (arXiv:1612.09035) Table 1 (0.76/0.51/0.26) COMPARED: reproduced 0.7415/0.5009/0.2567 within 2.5%. Cited in report + module."
    ref-billard-flux:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "reactor_flux_billard_variant.csv (int Phi=4.586e12, HM constant <2 MeV) read and renormalized by k=0.0111 before the Table-1 fold; folding as-stored (without k) kept only as the 89.9x regression."
    ref-conus:
      status: completed
      completed_actions: [compare, cite]
      missing_actions: []
      summary: "CONUS+ (Nature 643, 1229 (2025), arXiv:2501.05206, 3.6 GW_th/20.7 m) COMPARED as a coarse factor-2 rate-scale anchor (ratio 0.99); eV_ee quenching caveat recorded. Cited in report + params."
    ref-flagship-flux-v2:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "The v1.0 split rel_uncertainty column (2-5% >2 MeV, 20-25% <1.8 MeV) read and propagated into the dR/dT band; the RATE-weighted propagation yields 6-10% below 95 eV because the well-anchored high-E flux dominates the integrand."
  forbidden_proxies:
    fp-billard-norm:
      status: rejected
      notes: "k=0.0111 rescale applied before the Table-1 comparison; folding at the stored 3 GW_th/25 m norm is kept ONLY as test_without_k_overshoots_90x (89.9x=1/k regression)."
    fp-gwe-gwth:
      status: rejected
      notes: "Both P_B=8.54 and P_v=3 are GW_th; distance enters as (d_v/d_B)^2. Guard test brackets k in [0.006,0.05]; a 1/d error -> 0.18, a GW_e error -> 0.004. Reproduced."
    fp-hide-band:
      status: rejected
      notes: "The figure and CSV report BOTH the 1sigma flux band AND the sub-1.8-MeV rate fraction; the low-recoil systematic is explicit. The honest 6-10% band replaces the plan's 20-25% guess -- disclosed, not hidden."
    fp-lumped-A-billard:
      status: rejected
      notes: "Billard reproduction uses the 5-isotope Ge sum on per-isotope kinematic domains, not a lumped A=72.63; BILLARD_REPRODUCTION.md Sec 2 states the abundances used."
  uncertainty_markers:
    weakest_anchors:
      - "The sub-1.8-MeV flux SHAPE is the Phase-2 Kopeikin-2012-consistent MODEL PLACEHOLDER (not a sourced EF/CONFLUX table); it drives 18% (50 eV) to 34% (20 eV) of the low-recoil rate. Inherited from Phase 2 (which is expert_needed for the same reason), covered by the propagated band, not independently anchored here."
      - "CONUS+ is on an eV_ee (ionization) scale and needs a quenching model; the factor-2 ratio 0.99 is a coarse rate-scale cross-check, not a direct eV_nr spectrum match (MEDIUM)."
      - "Billard's residual exact sub-2-MeV shape vs our HM-flat variant is unverified; it only touches the 50 eV bin, where the deviation is -2.4%."
      - "Helm F^2 near the ~2 keV endpoint dips to 0.964; reproduced in code, but the deep-endpoint tail carries negligible rate weight."
    unvalidated_assumptions:
      - "The 73Ge spin-dependent/axial term is ~1/N^2 suppressed and not modeled (stated)."
      - "Single 8.54 GW at 400 m reproduces the two-core Chooz geometry (confirmed to 0.25%)."
      - "Ge nuclear masses M_i = A_i x 931.494 MeV (binding/electron-mass corrections <1e-3, negligible at the T/E_nu ~ 1e-3 kinematic level)."
    competing_explanations:
      - "If a real EF/CONFLUX/Kopeikin sub-1.8-MeV table replaces the placeholder, the low-recoil (T<~95 eV) band and the sub-1.8 rate fraction (18-34%) could shift; the Billard and CONUS+ anchors constrain the >1.8 MeV normalization but not the differential shape below 1.8 MeV."
    disconfirming_observations:
      - "Differential failing to integrate to sigma_tot at >0.1% (checked false: rel 1e-8). A single sharp endpoint instead of five T_max steps (checked false: 2.82-3.07 keV spread). PCHIP negative/jagged flux (checked false). Billard 100/200 eV bins off >20% (checked false: <2%). Sub-1.8 toggle changing T>200 eV bins (checked false: <1e-3)."
comparison_verdicts:
  - subject_id: test-billard
    subject_kind: acceptance_test
    subject_role: decisive
    reference_id: ref-billard
    comparison_kind: benchmark
    metric: relative_error
    threshold: "<= 0.025"
    verdict: pass
    notes: "Reproduced 0.7415/0.5009/0.2567 vs Billard Table 1 0.76/0.51/0.26 counts/kg/day (-2.4/-1.8/-1.3%, all <2.5% << 20%); independently reproduced by an own fold with an independently derived k. Folding at the stored norm (k=1) overshoots by a uniform 89.9x = 1/k, proving the mismatch is pure geometry+power normalization."
  - subject_id: test-conus
    subject_kind: acceptance_test
    subject_role: decisive
    reference_id: ref-conus
    comparison_kind: benchmark
    metric: rate_scale_ratio
    threshold: "within factor 2"
    verdict: pass
    notes: "Flagship and Billard rates rescaled to CONUS+ config agree to ratio 0.99 (within factor 2). CAVEAT: coarse eV_ee-scale check needing a quenching model, not a direct eV_nr spectrum match -> MEDIUM confidence."
  - subject_id: claim-band
    subject_kind: claim
    subject_role: supporting
    comparison_kind: cross_method
    metric: band_magnitude
    threshold: "plan-guessed 20-25% below 95 eV"
    verdict: tension
    notes: "Computed rate-weighted 1sigma flux band is 6-10% below 95 eV (9.8% at 20 eV) and 3.5% above 200 eV, NOT the plan-guessed 20-25%. The QUALITATIVE structure (widening below 95 eV, narrow above 200 eV, sub-1.8 toggle localized, T>200 eV unchanged <1e-3) is confirmed; only the guessed magnitude is superseded because the well-anchored (2-5%) >1.8 MeV flux dominates the rate integrand. Honest downward refinement (both band and 18-34% sub-1.8 rate fraction reported), not a failure; needs an orchestrator reword of claim-band, not a backtrack."
---

<!-- ASSERT_CONVENTION: metric_signature=not_applicable, fourier_convention=not_applicable, natural_units=internal-only (hbar=c=1) for CEvNS cross section; k_B EXPLICIT (not =1); I/O in eV/keV/MeV, counts/kg/day/keV, s, cm/um; (hbar c)^2 = 3.894e-28 GeV^2 cm^2 -->

# Phase 3 Verification — CEvNS Cross Section & Rate

**Verdict:** PASSED-WITH-CAVEATS (top-level status `expert_needed`) · **Confidence:** HIGH · **Mode:** initial (no prior VERIFICATION.md)
**Plan reference (machine ledger):** `03-02-PLAN.md#/contract` (headline `claim-billard`/`claim-band`, VALD-01). Plan `03-01` (`claim-dsigma`/`claim-drdt`, CALC-02, the computational core) is a full contract in its own right; the frontmatter binds one plan per phase report, so both plans' claims/deliverables/acceptance_tests/references/forbidden_proxies are carried in the ledger above and covered below with equal, independent rigor. Full suite: **82/82 pytest pass**.

## 1. Goal Achievement

Phase goal: *"Compute the per-isotope-summed CEvNS differential rate dR/dT on natural Ge in DEPOSITED nuclear-recoil energy (Freedman cross section + Helm form factor, folded with the frozen Phase-2 flux), validated against (a) the closed-form total cross section and (b) Billard et al. (2017) Table 1."*

| Goal element | Where | Independent check | Status |
|---|---|---|---|
| Per-isotope Freedman dsigma/dT + Helm F | cevns.py | int dsigma/dT dT = sigma_tot to 1e-8; F(0)=1; F^2(200 eV)=0.996 | VERIFIED |
| Closed-form validation (a) | cevns.py, test_cevns_differential.py | sigma(72Ge,4 MeV)=1.0026e-40 (+0.26%); closure rel 3e-3 | VERIFIED |
| Per-isotope-summed dR/dT, deposited eV_nr | cevns.py, cevns_dRdT.csv | 67.752 counts/kg/day >50 eV; five T_max steps; no quenching | VERIFIED |
| Billard Table-1 validation (b) | BILLARD_REPRODUCTION.md, test_cevns_billard.py | 0.742/0.501/0.257 vs 0.76/0.51/0.26 (<2.5%); without-k 89.9x | VERIFIED |
| Flux-band + CONUS+ carry-through | cevns.py, cevns_dRdT_deposited.pdf | CONUS+ ratio 0.99; band 6-10% <95 eV (plan guessed 20-25%) | VERIFIED (magnitude reworded, §6) |

All goal elements are established. The output is DEPOSITED nuclear-recoil energy (reconstruction/response is Phase 5, correctly out of scope). The single caveat driving `expert_needed` is the inherited Phase-2 sub-1.8-MeV placeholder (§6); the claim-band magnitude is an honest downward refinement, not a failure.

## 2. Contract Coverage

### Frontmatter scope, Plan 03-01 verification, and expert review (relocated from frontmatter)
<!-- frontmatter contract_results is bound to the single Plan 03-02 contract; Plan 03-01 ledger + the expert-review items below were relocated here from frontmatter to satisfy the one-plan-per-verification schema -->


The machine-readable `contract_results` ledger in this file's frontmatter is bound to the single Plan 03-02 contract (`03-02-PLAN.md#/contract`), as the validator resolves one plan contract per verification. **Plan 03-01 (CEvNS cross section & differential rate) is fully verified and its machine-readable ledger lives in `03-01-SUMMARY.md`.** For the record, the Plan 03-01 headline verified here independently:

- `claim-dsigma` (PASS): per-isotope Freedman dsigma_i/dT with Helm F and /(4pi)+(hbar c)^2 discipline integrates to the closed-form sigma_tot to rel 1.3e-8..1.5e-8 across all five isotopes; sigma(72Ge,4 MeV) full Q_W = 1.0026e-40 cm^2 (+0.26% vs the CONVENTIONS Sec C anchor); Helm F(0)=1, F^2(200 eV,72Ge)=0.99634. Deliverables `deliv-cevns-code`, `deliv-drdt-csv`, `deliv-tests`; tests `test-closedform`, `test-sigma-anchor`, `test-helm`; refs `ref-conventions`, `ref-cevns-code`, `ref-lewin-smith`; forbidden proxies `fp-hbarc2` (/(4pi)+(hbar c)^2 mandatory), `fp-4pi-8pi`, `fp-lumped-A`, `fp-quenching` all rejected.
- `claim-drdt` (PASS): per-isotope-summed dR/dT on natural Ge, flagship rate above 50 eV = 67.752 counts/kg/day; rate closure 119.06 vs 119.42 (rel 3.0e-3); five distinct T_max endpoints (2.82-3.07 keV) vs a lumped-A endpoint. Tests `test-rate-closure`, `test-per-isotope`, `test-convergence`; ref `ref-flagship-flux`.
- Decisive 03-01 comparisons (in `03-01-SUMMARY.md` ledger): sigma anchor +0.26% (benchmark, pass); closed-form identity rel ~1e-8 (cross_method, pass); per-isotope vs lumped-A stepped structure (cross_method, pass).

**Expert review requested (drives `status: expert_needed`):**
1. Adequacy of the inherited sub-1.8-MeV model-placeholder flux shape for the Phase-3 low-recoil CEvNS bins (T <~ 95 eV_nr), domain reactor antineutrino spectroscopy / low-energy CEvNS. Automated checks confirm the placeholder contributes only 18-34% of the low-recoil rate and is covered by the propagated band, but whether that band adequately spans the true EF-vs-CONFLUX sub-1.8-MeV shape spread -- or whether a digitized table must replace it before precision use -- is a domain-expert judgment (inherited from Phase 2, status expert_needed). Expected: accept placeholder + band as adequate for a stage-1 estimate, or source a real Estienne-Fallot/CONFLUX/Kopeikin-2012 per-isotope sub-1.8-MeV table.
2. Orchestrator bookkeeping (non-expert): reword `claim-band`/`test-band` magnitude from "band 20-25% below 95 eV" to "band widens to ~6-10% below ~95 eV; sub-1.8 rate fraction reaches 18-34%". The implemented test asserts the correct physical behavior (widening + localization) and passes; the computed value is 6-10%, an honest refinement, not a failure. Needs a contract-wording update decision, not a physics/backtrack action. (Recorded as the `claim-band` `tension` comparison verdict.)

**Plan 03-02 (machine ledger, headline):** claims 2/2, deliverables 4/4, acceptance_tests 4/4, references 4/4 completed, forbidden_proxies 4/4 rejected.
**Plan 03-01 (machine ledger, carried):** claims 2/2, deliverables 3/3, acceptance_tests 6/6, references 4/4 completed, forbidden_proxies 4/4 rejected.
**Combined primary contract targets (claims + deliverables + acceptance_tests): 21/21 VERIFIED.** `claim-band`/`test-band` pass in mechanism with a documented plan-magnitude correction (cmp-band-magnitude: tension). Key links (link-dsigma, link-drdt, link-billard, link-band): **4/4** verified.

## 3. Required Artifacts (levels 1–4)

| Artifact | Exists | Substantive | Content-valid | Integrated | Status |
|---|---|---|---|---|---|
| src/qpd_potential/cevns.py | ✓ | ✓ Helm/dsigma/fold/Billard | ✓ 1e-8 closure, 1.0026e-40 | ✓ params-driven, Phase-5 input | VERIFIED |
| src/qpd_potential/params.py | ✓ | ✓ provenance-tagged, 5-iso table | ✓ constants match CONVENTIONS | ✓ single source of truth | VERIFIED |
| artifacts/stage1/cevns_dRdT.csv | ✓ | ✓ 8 cols + header checks | ✓ rows reproduce live fold <1e-3 | ✓ figure + band test input | VERIFIED |
| artifacts/stage1/BILLARD_REPRODUCTION.md | ✓ | ✓ k, rates, 90x, CONUS+ | ✓ all numbers reproduced | ✓ VALD-01 record | VERIFIED |
| artifacts/stage1/cevns_dRdT_deposited.pdf | ✓ | ✓ 39 KB | ~ arrays verified (not pixel-read) | ✓ | VERIFIED |
| tests/test_cevns_differential.py | ✓ | ✓ | ✓ green | ✓ | VERIFIED |
| tests/test_cevns_billard.py | ✓ | ✓ 11 tests | ✓ green | ✓ | VERIFIED |

## 4. Computational Verification (oracle — executed, independent of `cevns`)

The following was run from scratch with my own constants and quadrature (no import of the project module), then compared to the artifacts:

```python
import numpy as np, math
from scipy.integrate import quad
from scipy.special import spherical_jn
from scipy.interpolate import PchipInterpolator
GF=1.1663787e-5; s2w=0.2387; om4=1-4*s2w; hbarc2=3.894e-28; u=931.494; hc=197.327; NA=8.29e24
QW=lambda Z,N:N-om4*Z
sigtot=lambda Eg,Z,N:GF**2*QW(Z,N)**2*Eg**2/(4*math.pi)*hbarc2
# Helm + per-isotope dsigma/dT + PCHIP-log flux fold rebuilt independently (see report body)
# checks: sigma anchor, closed-form identity, k, flagship rate, Billard, band, sub-1.8
```

**Output:**

```output
1) sigma(72Ge,4MeV) full Q_W = 1.0026e-40 cm^2   (anchor ~1.0e-40; +0.26%)
2) Helm F(0)=1.000000000000 ; F^2(200eV,72Ge)=0.99634 ; F^2(2keV)=0.96390
3) closed-form identity int dsig/dT dT (F=1) vs sigma_tot @4MeV:
   70Ge rel=1.50e-08  72Ge 1.42e-08  73Ge 1.38e-08  74Ge 1.35e-08  76Ge 1.28e-08
4) k_single=0.011120  k_two=0.011092  reldiff=0.2531%
5) flagship dR>50eV = 67.752 counts/kg/day
6) Billard WITH k:  >50 0.7415(-2.4%)  >100 0.5009(-1.8%)  >200 0.2567(-1.3%)
   WITHOUT k: 66.68/45.05/23.09  overshoot 89.9x=1/k
7) band frac: 20eV=0.098 50eV=0.062 200eV=0.035 500eV=0.042
   sub-1.8 frac: 20eV=0.338 50eV=0.178 95eV=0.0003 200eV=0.00000
fp checks: /8pi=5.013e-41(0.50x, fails 20% window); hbarc2-omit=2.575e-13 GeV^-2(2.6e27x)
Tmax: 70Ge 3.066 keV / 76Ge 2.824 keV / lumped-A72.63 2.955 keV
```

**Verdict: PASS.** Every artifact headline number is reproduced to matching precision by an independent implementation. The two convention forbidden proxies are decisive discriminators: /8π halves σ (fails the anchor), and omitting (ħc)² inflates σ by ~2.6e27.

## 5. Physics Consistency

- **Dimensional:** [G_F^2 M/4pi]=GeV^-3, x[Q_W^2 dimensionless]x[(hbar c)^2 GeV^2 cm^2]=GeV^-1 cm^2 = cm^2/GeV, x1e-6 -> cm^2/keV; fold x[atoms/kg][nu cm^-2 s^-1 MeV^-1]dE[MeV]x86400 -> counts/kg/day/keV. Consistent.
- **Limiting cases:** F(0)=1 exact; kinematic factor (1-MT/2E^2)->1 at low T; T_max->2E^2/M at E<<M; closed-form recovered as F->1 integral.
- **Conservation/kinematics:** exact E_min^(i)(T) inversion of T=2E^2/(M+2E); dsigma/dT clamped to [0,T_max]; five distinct endpoints preserved.
- **Convergence:** rate>50 eV stable <1% (n=120 vs 240); PCHIP log-flux non-negative (no ringing); Billard fold converged by n=600 (4 sig figs).

## 6. Discrepancy / Honest Finding — the low-recoil band magnitude

The plan's `claim-band`/`test-band` guessed a **20-25%** propagated 1σ flux band below ~95 eV_nr. The rigorous rate-weighted propagation gives **3.5% (200 eV) → 6.2% (50 eV) → 9.8% (20 eV)** — independently reproduced. Mechanism (verified): the rate integrand at every recoil is dominated by the well-anchored (2-5%) >1.8 MeV flux, because those neutrinos carry larger cross sections; the wide-band sub-1.8-MeV placeholder is only 18% (50 eV) to 34% (20 eV) of the rate, so a fully-correlated 25% swing of that block moves the low-T rate by at most ~0.25×0.34 ≈ 8%. The **qualitative** claim holds exactly (band widens below 95 eV, narrow above 200 eV, sub-1.8 toggle localized, T>200 eV unchanged <1e-3), and both the band and the sub-1.8 rate fraction are reported (no `fp-hide-band`). This is a legitimate downward refinement from actual computation, **not** a physics failure and **not** a backtrack trigger. It requires an orchestrator reword of the claim-band wording (see expert_review item 2).

## 7. Requirements Coverage

CALC-02 (per-isotope-summed dR/dT on natural Ge, deposited eV_nr) — DELIVERED. VALD-01 (Billard Table-1 within ~20%; CONUS+ within factor 2) — SATISFIED (2.5% / ratio 0.99). Advances claim-cevns and the deposited-energy precursor of obs-cevns-spectrum. Anchors ref-cevns-benchmark (Billard), CONUS+, ref-huber all exercised. ROADMAP >20% backtrack trigger NOT met (σ +0.26%; Billard 100/200 eV <2%).

## 8. Anti-Patterns Scanned

No hardcoded convention constants (all pulled from params.py); no /8π; no (ħc)² omission; no lumped-A; no ionization quenching / eV_ee mixing on the output axis; no hidden band; no GW_e/GW_th confusion; no 1/d (vs 1/d²) geometry error. All eight contract forbidden proxies rejected with decisive evidence.

## 9. Expert / Human Review Required

1. **Expert (reactor ν spectroscopy):** adequacy of the inherited sub-1.8-MeV placeholder shape for the T<~95 eV bins — inherited from Phase 2 (`expert_needed`); band-covered but not literature-anchored.
2. **Orchestrator (non-expert bookkeeping):** reword claim-band/test-band from "20-25% below 95 eV" to the computed "~6-10% below ~95 eV; sub-1.8 rate fraction 18-34%". Honest refinement, no code/convention change.

## 10. Confidence Assessment

**HIGH.** Every decisive check — σ anchor, closed-form identity, k derivation, Billard Table-1, without-k overshoot, flagship rate, band widths, sub-1.8 localization, forbidden-proxy discriminators — was **independently recomputed** from scratch and matches the artifacts to the reported precision (most to ≥4 significant figures, the closed-form identity to 1e-8). The only open items are an inherited expert-judgment caveat and a contract-wording reword, neither of which is a physics gap. Top-level status `expert_needed` mirrors the Phase-2 precedent for the same sub-1.8-MeV placeholder.
