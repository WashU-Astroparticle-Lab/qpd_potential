---
phase: 02-reactor-flux-model
verified: "2026-07-20T00:00:00Z"
status: expert_needed
score: "15/15"
plan_contract_ref: GPD/phases/02-reactor-flux-model/02-02-PLAN.md#/contract
contract_results:
  claims:
    claim-frozen-flux:
      status: passed
      summary: "Plan 02-02 headline. Frozen data/flux/reactor_flux_v1.0.csv normalizes to int Phi dE = 7.503e12 nu-bar/cm2/s at 3 GW_th, 25 m (target 7-8e12), independently reproduced from the CSV by trapz. R_f=9.098e19 fissions/s and 1/(4 pi d^2)=1.273e-8 cm^-2 both reproduced from first principles; <E_f>=205.8 MeV effective-thermal (Ma 2013), NOT total Q; R_f x geometry applied once (no ~6/fission double-count). Split band 2-5% above / 20-25% below verified from the CSV region_flag. Billard variant is a distinct table (4.586e12) with HM held constant below 2 MeV (1 unique value, 0 spread) and correct isotope-labelled fractions 55.6/32.6/7.1/4.7."
      linked_ids: [deliv-frozen-csv, deliv-normalization-code, deliv-overlay-fig, test-normalization, test-csv-schema, test-band-split, test-billard-variant, ref-huber, ref-cevns-benchmark, ref-ma, ref-hayes-vogel]
  deliverables:
    deliv-frozen-csv:
      status: passed
      path: data/flux/reactor_flux_v1.0.csv
      summary: "Seven columns (E_nu_MeV, total, flux_fission_HM, flux_fission_summation, flux_ncapture_238U, rel_uncertainty, region_flag) + version/date/git-sha/normalization/per-source-provenance/integral-check header. Additive: HM+summation+ncapture reproduces total to 1e6 (float round). region_flag in {above_2MeV, seam, below_1p8MeV}."
      linked_ids: [claim-frozen-flux]
    deliv-normalization-code:
      status: passed
      path: src/flux/normalization.py
      summary: "R_f=P_th/<E_f> with effective-thermal <E_f> (Ma 2013), dimensioned asserts pinning <E_f> to 195-220 MeV, geometry 1/(4 pi d^2) at d=2500 cm, single multiplication. GW_th (not GW_e), effective thermal (not total Q), and no ~6 double-count all guarded in code and confirmed numerically."
      linked_ids: [claim-frozen-flux]
    deliv-overlay-fig:
      status: passed
      path: GPD/phases/02-reactor-flux-model/figures/flux_overlay.png
      summary: "flux_overlay.png (107 KB) exists: total flux with split band, computed 235U contribution, and published Huber 235U benchmark points overlaid, seam marked. seam_continuity.png (136 KB) also present from Plan 02-01."
      linked_ids: [claim-frozen-flux]
  acceptance_tests:
    test-normalization:
      status: passed
      summary: "Independently: R_f=3e9/(205.815 x 1.602e-13)=9.098e19 fissions/s (target ~9e19); int Phi dE=7.503e12 nu-bar/cm2/s (target 7-8e12) reproduced by trapz on the frozen CSV; emission=1.964e20 nu-bar/s/GW_th (Hayes-Vogel ~2e20). Uses GW_th and effective-thermal <E_f>, not GW_e or total Q."
      linked_ids: [claim-frozen-flux, ref-ma, ref-hayes-vogel]
    test-csv-schema:
      status: passed
      summary: "All seven columns present; region_flag values in {above_2MeV(23), seam(3), below_1p8MeV(75)}; rel_uncertainty populated every row; header documents version v1.0, git_sha eb7da23, normalization, per-source provenance, and integral checks."
      linked_ids: [deliv-frozen-csv]
    test-band-split:
      status: passed
      summary: "rel_uncertainty from the CSV: 0.025-0.050 for above_2MeV, 0.10 at seam, 0.20-0.25 below_1p8MeV — widens across the seam, NOT uniform. Overlay figure shows the computed 235U contribution tracking published Huber above 2 MeV within band."
      linked_ids: [claim-frozen-flux, deliv-frozen-csv, deliv-overlay-fig, ref-huber]
    test-billard-variant:
      status: passed
      summary: "reactor_flux_billard_variant.csv is distinct (int 4.586e12); HM held exactly constant below 2 MeV (1 unique flux value, 0 spread); fractions 235U/239Pu/238U/241Pu=55.6/32.6/7.1/4.7 isotope-labelled with no 238U<->239Pu swap; n-capture excluded, matching Billard assumptions."
      linked_ids: [deliv-normalization-code, ref-cevns-benchmark]
  references:
    ref-huber:
      status: completed
      completed_actions: [read, use, compare, cite]
      missing_actions: []
      summary: "Huber coefficients (235U/239Pu/241Pu) fetched with provenance and used; the computed 235U flux was compared against the published Huber tabulation (agreement within band above 2 MeV, reconstructed 235U within 0.73%/0.13% at 3/5 MeV); cited in code and CSV header."
    ref-hayes-vogel:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "Compared: total ~6/fission (5.875), above-1.8 ~1.9 (1.881), and emission ~2e20 nu-bar/s/GW_th (1.964e20) all consistent. Cited in normalization docstring and CSV header."
    ref-ma:
      status: completed
      completed_actions: [use, cite]
      missing_actions: []
      summary: "Ma 2013 effective-thermal energies (202.4/205.9/211.1/213.6 MeV) used to set <E_f>=205.8 MeV (deposited, not total Q). Cited in code and header."
    ref-cevns-benchmark:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "Billard (2017) flux assumptions reproduced as a distinct variant table (HM constant below 2 MeV, fractions 55.6/32.6/7.1/4.7) ready for the Phase-3 Table-1 reproduction. Cited in variant CSV header."
  forbidden_proxies:
    fp-loose-1e13:
      status: rejected
      notes: "Authoritative target 7-8e12 used; achieved 7.503e12 (the honest arithmetic value), NOT tuned up to the loose REQUIREMENTS CALC-01 '~1e13'. No spurious ~30% inflation."
    fp-norm-chain-traps:
      status: rejected
      notes: "GW_th (3e9 W, not GW_e), effective-thermal <E_f>=205.8 MeV (not total Q), and single R_f x 1/(4 pi d^2) multiplication all confirmed numerically; per-fission spectrum already integrates to ~6 and is not re-multiplied."
    fp-uniform-band:
      status: rejected
      notes: "Split band verified from the frozen CSV: 2-5% above 2 MeV, 10% seam, 20-25% below 1.8 MeV. The never-measured region is explicitly wider, not masked as data-anchored."
  uncertainty_markers:
    weakest_anchors:
      - "Sub-1.8 MeV summation SHAPE is a documented MODEL PLACEHOLDER (seam-anchored allowed-beta-like continuation), not a sourced EF/CONFLUX/Kopeikin table; it governs ~71% of the total flux integral and the Phase-3 low-recoil CEvNS bins. Covered by a wide 20-25% band."
      - "238U(n,gamma) shape is a first-principles allowed-beta (F=1, no-Coulomb) computation, MEDIUM confidence; only its 0.6/fission integral is sourced."
      - "Point-source 1/(4 pi d^2) neglects finite-core geometry (adequate only at the ~2x rate tolerance)."
    unvalidated_assumptions:
      - "The summation SHAPE is trustworthy in the 2-3 MeV overlap where the seam scale c_i is fit, even if its absolute normalization is not."
      - "Low-energy flattening of the log-slope (single physical assumption in the placeholder), not tuned to any integral target."
    competing_explanations:
      - "The absolute integral flux (7.5e12) and its sub-1.8 shape could shift if a real EF/CONFLUX/Kopeikin table replaces the placeholder; the ~6/fission and ~1.9-above anchors bound the integral but not the differential shape below 1.8 MeV."
    disconfirming_observations:
      - "A visible seam step (checked false: 0.15% dense jump, C1), negative flux (checked false: min 1.06), integral far from 7-8e12 (checked false: 7.503e12), or a Billard 238U<->239Pu fraction swap (checked false)."
comparison_verdicts:
  - subject_id: test-normalization
    subject_kind: acceptance_test
    subject_role: decisive
    reference_id: ref-hayes-vogel
    comparison_kind: benchmark
    metric: emission_rate_and_integral_flux
    threshold: "int Phi dE in 7-8e12; emission 1.7e20-2.3e20 nu-bar s^-1 GW_th^-1"
    verdict: pass
    notes: "int Phi dE = 7.503e12 nu-bar/cm2/s inside the authoritative 7-8e12 target; emission 1.964e20 nu-bar/s/GW_th vs Hayes-Vogel ~2e20 (within ~2%); yields total 5.875/fission (~6) and above-1.8 1.881/fission (~1.9) consistent with reactor accounting."
  - subject_id: claim-frozen-flux
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-huber
    comparison_kind: benchmark
    metric: relative_error
    threshold: "<= band (~2-5% above 2 MeV)"
    verdict: pass
    notes: "Reconstructed 235U vs published Huber: +0.73% at 3 MeV, -0.13% at 5 MeV (pass window ~5%); computed 235U flux tracks published Huber within band above 2 MeV."
  - subject_id: claim-frozen-flux
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-cevns-benchmark
    comparison_kind: prior_work
    metric: variant_distinctness
    threshold: "constant below 2 MeV + Billard fractions labelled; distinct from flagship"
    verdict: pass
    notes: "Billard-assumption variant reproduces HM-constant-below-2-MeV with correct isotope-labelled fractions; distinct 4.586e12 table ready for Phase-3."
---

<!-- ASSERT_CONVENTION: metric_signature=not_applicable, fourier_convention=not_applicable, natural_units=internal-only (hbar=c=1) for CEvNS cross section; k_B EXPLICIT (not =1); I/O in eV/keV/MeV, counts/kg/day/keV, s, cm/um; (hbar c)^2 = 3.894e-28 GeV^2 cm^2 -->

# Phase 2 Verification — Reactor Flux Model

**Verdict:** PASSED-WITH-CAVEATS (top-level status `expert_needed`) · **Confidence:** HIGH · **Mode:** initial (no prior VERIFICATION.md)
**Plan reference (machine ledger):** `02-02-PLAN.md#/contract` (headline `claim-frozen-flux`, the CALC-01 deliverable). Plan `02-01` (the per-fission shape half, `claim-perfission-spectrum`) is a full contract in its own right; the frontmatter binds one plan per phase report, so both plans' claims/deliverables/acceptance_tests are carried in the ledger above and covered below with the same rigor.

## 1. Goal Achievement

Phase goal: *"A frozen, versioned Phi(E_nu) table is produced — Huber–Mueller above 2 MeV plus a summation + 238U(n,gamma) neutron-capture extension below 1.8 MeV — with explicit above/below-2-MeV uncertainty bands, normalized to 3 GW_th at 25 m (~7–8e12 nu-bar/cm2/s)."*

| Goal element | Where | Independent check | Status |
|---|---|---|---|
| Frozen versioned table | data/flux/reactor_flux_v1.0.csv | 7 columns + version/git-sha/provenance/integral-check header; 31 tests pass | VERIFIED |
| HM above 2 MeV, sourced | hm_coefficients.csv, huber_mueller.py | Coeffs = canonical Huber/Mueller; 235U reconstruction +0.73%/-0.13% at 3/5 MeV | VERIFIED |
| Summation + n-capture below 1.8 MeV | assemble_spectrum.py, summation_ncapture.py | Sub-1.8 populated, non-negative, C1 seam; n-capture 0.60/fission | VERIFIED (shape = placeholder, see §6) |
| Explicit split band | build_flux_table.py, CSV region_flag | 2-5% above / 10% seam / 20-25% below, from the CSV | VERIFIED |
| Normalized to ~7-8e12 at 3 GW_th, 25 m | normalization.py | int Phi dE = 7.503e12; R_f=9.10e19; single geometry factor | VERIFIED |

All five goal elements are established. The sub-1.8 MeV region is MODELED (not truncated), satisfying the goal literally, but its shape rests on a placeholder rather than a sourced dataset — the documented, pre-anticipated caveat (§6).

### Frontmatter scope, sub-1.8 MeV verdict, and expert review (relocated from frontmatter)

The machine-readable `contract_results` ledger in this file's frontmatter is bound to the single Plan 02-02 contract (`02-02-PLAN.md#/contract`), as the validator resolves one plan contract per verification. The Plan 02-01 headline (component-wise per-fission spectrum: `claim-perfission-spectrum`, `deliv-assembly-code`, `deliv-component-data`, `test-coeffs-sourced`, `test-hm-unit`, `test-integral-yields`, `test-seam-continuity`, `ref-mueller`, `ref-summation`, `ref-ncapture`, `fp-truncate-ibd`, `fp-invented-coeffs`, `fp-negative-spline`) is verified in the goal-achievement table above and §6 below, and its machine-readable ledger lives in `02-01-SUMMARY.md`.

- **Sub-1.8 MeV shape comparison — INCONCLUSIVE (not a pass).** The sub-1.8 MeV SHAPE (which governs ~71% of the flux integral and the flagship low-recoil CEvNS input) is a model placeholder, not benchmarked against a sourced Estienne-Fallot/CONFLUX/Kopeikin-2012 table. `ref-summation` was cited but the digitized per-isotope table could not be machine-sourced in-environment (Huber/Mueller tabulations stop at 2.0 MeV; the full CONFLUX ENDF summation is out of plan scope). Band-covered (20-25%) and within the phase goal's "modeled extension" scope, but not literature-anchored; needs a sourced replacement before precision use.
- **Expert review requested (drives `status: expert_needed`).** Adequacy of the sub-1.8 MeV model-placeholder shape for the Phase-3 CEvNS low-recoil spectrum (domain: reactor antineutrino spectroscopy / low-energy CEvNS). The placeholder governs ~71% of the flux integral and directly shapes the flagship T<~96 eV recoil bins; whether the 20-25% band adequately covers the true EF-vs-CONFLUX shape spread, or whether a digitized summation table must be sourced before precision use, is a domain-expert judgment automated checks cannot settle. Expected resolution: either accept the placeholder+band as adequate for a stage-1 estimate (the goal explicitly asks for a MODELED extension with a wide band), or source a real Estienne-Fallot/CONFLUX/Kopeikin-2012 per-isotope sub-1.8 MeV table to replace it.

## 2. Contract Coverage

**Plan 02-02 (machine ledger):** claim 1/1, deliverables 3/3, acceptance_tests 4/4, references 4/4 completed, forbidden_proxies 3/3 rejected.
**Plan 02-01 (machine ledger):** claim 1/1, deliverables 2/2, acceptance_tests 4/4, references 4/5 completed (ref-summation PARTIAL), forbidden_proxies 3/3 rejected.
**Combined primary contract targets (claims + deliverables + acceptance_tests): 15/15 VERIFIED.** One reference action (`ref-summation` use of a real EF/CONFLUX table) is PARTIAL and drives the `expert_needed` status.

## 3. Required Artifacts (levels 1–4)

| Artifact | Exists | Substantive | Content-valid | Integrated | Status |
|---|---|---|---|---|---|
| src/flux/huber_mueller.py | ✓ | ✓ exp(poly), CSV-loaded | ✓ 235U +0.73%/-0.13% | ✓ feeds assemble | VERIFIED |
| src/flux/summation_ncapture.py | ✓ | ✓ allowed-beta, sourced Q | ✓ n-cap 0.60/fission | ✓ feeds assemble | VERIFIED (placeholder flagged) |
| src/flux/assemble_spectrum.py | ✓ | ✓ PCHIP-log, C1 blend | ✓ C1, non-neg, yields | ✓ feeds normalization | VERIFIED |
| src/flux/normalization.py | ✓ | ✓ dimensioned chain | ✓ R_f, geom, flux | ✓ feeds build_flux_table | VERIFIED |
| src/flux/build_flux_table.py | ✓ | ✓ band, header, Billard | ✓ CSV + figure | ✓ freezes CALC-01 | VERIFIED |
| data/flux/hm_coefficients.csv | ✓ | ✓ provenance per row | ✓ canonical values | ✓ loaded by code | VERIFIED |
| data/flux/reactor_flux_v1.0.csv | ✓ | ✓ 7 cols + header | ✓ int 7.503e12, additive | ✓ Phase-3 input | VERIFIED |
| data/flux/reactor_flux_billard_variant.csv | ✓ | ✓ constant-below-2 | ✓ 4.586e12, correct fractions | ✓ Phase-3 closure | VERIFIED |
| figures/{flux_overlay,seam_continuity}.png | ✓ | ✓ 107/136 KB | ✓ overlay + seam | ✓ | VERIFIED |
| tests/ (3 flux files) | ✓ | ✓ | ✓ 31 passed | ✓ | VERIFIED |

## 4. Computational Verification (oracles)

### Oracle A — independent Huber recon, normalization chain, integral flux, band, yields, emission (executed)

```python
import numpy as np, csv
a=[4.367,-4.577,2.100,-5.294e-1,6.186e-2,-2.777e-3]           # 235U, from hm_coefficients.csv
S=lambda E: np.exp(sum(a[p]*E**p for p in range(6)))
# reconstruction vs published Huber (0.651 @3, 0.110 @5)
# normalization from first principles
Rf=3.0e9/(205.815*1.602176634e-13); geom=1/(4*np.pi*2500.0**2)
# integral flux + additive + non-neg from the FROZEN csv
rows=[r for r in open("data/flux/reactor_flux_v1.0.csv") if not r.startswith("#")]
d=list(csv.DictReader(rows)); E=np.array([float(r["E_nu_MeV"]) for r in d])
tot=np.array([float(r["flux_nu_per_cm2_per_s_per_MeV"]) for r in d])
hm=np.array([float(r["flux_fission_HM"]) for r in d]); su=np.array([float(r["flux_fission_summation"]) for r in d])
nc=np.array([float(r["flux_ncapture_238U"]) for r in d])
print("235U recon 3/5 MeV:", round(float(S(3)),4), round(float(S(5)),4))
print("Rf=%.3e  geom=%.3e"%(Rf,geom))
print("int Phi dE=%.3e"%np.trapz(tot,E), " additive_err=%.1e"%np.max(np.abs(hm+su+nc-tot)), " min=%.2e"%tot.min())
print("below-1.8 fraction=%.1f%%"%(100*np.trapz(tot[E<1.8],E[E<1.8])/np.trapz(tot,E)))
```

**Output:**

```output
235U recon 3/5 MeV: 0.6558 0.1099
Rf=9.098e+19  geom=1.273e-08
int Phi dE=7.503e+12  additive_err=1.0e+06  min=2.98e+06
below-1.8 fraction=70.8%
```

**Verdict: PASS.** Reconstruction matches published Huber (+0.73%/-0.13%); R_f, geometry, and integral flux (7.503e12, in 7-8e12) reproduced from scratch; components additive to float round-off; flux non-negative; the placeholder-governed sub-1.8 region carries ~71% of the integral (confirms it dominates the CEvNS input and thus the caveat's weight).

### Oracle B — dense C1 seam continuity, integral yields, Billard-constant (executed)

```python
import numpy as np
from src.flux.assemble_spectrum import assemble, build_energy_grid
grid=np.unique(np.concatenate([build_energy_grid(), np.linspace(1.5,2.3,801)]))
sp=assemble(grid=grid); S=sp.per_isotope["235U"]; m=(grid>=1.5)&(grid<=2.3)
Es,Ss=grid[m],S[m]; dln=np.gradient(np.log(Ss),Es)
print("max adj rel jump=%.4f%%  minS=%.3f"%(100*np.max(np.abs(np.diff(Ss))/Ss[:-1]), Ss.min()))
y=sp.integral_yields(); print("total=%.3f above1.8=%.3f ncap=%.3f"%(y["total_fission_per_fission"],y["above_1p8_per_fission"],y["ncapture_per_fission"]))
```

**Output:**

```output
max adj rel jump=0.1469%  minS=1.062
total=5.875 above1.8=1.881 ncap=0.600
```

**Verdict: PASS.** Seam is C0/C1 continuous (0.15% dense jump, smooth log-slope), non-negative; yields (5.875 / 1.881 / 0.600) match the Hayes-Vogel and Kopeikin anchors. Billard-variant below-2-MeV flux independently confirmed constant (1 unique value, 0 spread; not shown above but run separately).

## 5. Physics Consistency

- **Dimensional:** [W]/[J/fission]=fissions/s; x[cm^-2]x[nu/fission/MeV]=nu/cm2/s/MeV; int over MeV -> nu/cm2/s. Consistent.
- **Convention lock:** flux pipeline has metric/fourier `not_applicable`; I/O in MeV, GW_th, cm — matches state.json. All flux artifacts carry `ASSERT_CONVENTION` headers (io_MeV / GW_thermal / standoff_cm=2500). No mismatch.
- **Normalization traps:** GW_th not GW_e; effective-thermal <E_f> not total Q; single geometry factor. All guarded and confirmed.
- **Physical plausibility:** reactor spectrum peaks below 1 MeV with ~6 nu/fission total, ~1.9 above IBD threshold — reproduced. Emission ~2e20/s/GW_th reproduced.

## 6. Primary Caveat — sub-1.8 MeV model placeholder

The sub-1.8 MeV summation SHAPE is a transparent MODEL PLACEHOLDER (seam-anchored allowed-beta-like continuation), NOT a digitized Estienne-Fallot/CONFLUX/Kopeikin-2012 per-isotope table — that dataset could not be machine-sourced in-environment, and per the fetch-not-invent rule none was fabricated. This is honestly recorded in the CSV header, both SUMMARYs, ASSUMPTIONS.md, and state.json decisions, and is covered by a wide 20-25% below-1.8 band. It is **pre-anticipated in the ROADMAP risk register** (Phase 2 top risk: "Sub-1.8 MeV flux model choice carries ≳10–20% shape uncertainty", mitigation = versioned CSV with a separate below-2-MeV band — exactly what was delivered).

Why it is not a silent pass and not a fail:
- It is **within the phase goal**, which asks for a *modeled* extension with an explicit band, not a measured one.
- The forbidden proxy `fp-truncate-ibd` is cleanly **rejected**: the region is populated, non-negative, C1, and not an HM power-law extrapolation.
- But it **governs ~71% of the flux integral** and the flagship low-recoil CEvNS bins, so its adequacy for precision Phase-3 use is a domain-expert judgment → top-level `expert_needed`.

## 7. Discrepancies / Anti-Patterns

- **Robustness (INFO, not a defect in the deliverable):** `ncapture_spectrum` divides by `trapz` of the branch shapes; on a grid that excludes E < Q (~1.3 MeV) both branches are all-zero → NaN → the `assert cap>=0` fires. The production pipeline always uses the full 0.1-10 MeV grid, so the frozen table is unaffected, but the function is fragile if reused on a restricted grid. Recommend guarding the zero-area normalization.
- No physics anti-patterns (no invented coefficients, no direct-apply polynomial, no negative/ringing spline, no double-count, no uniform band, no GW_e/total-Q trap).

## 8. Requirements Coverage

REQUIREMENTS CALC-01 ("~1e13 nu/cm2/s") — the loose wording was correctly NOT used as a target; the authoritative 7-8e12 was used (achieved 7.503e12). The '~1e13' discrepancy is surfaced for the orchestrator, as the plan required.

## 9. Confidence

**HIGH.** Every decisive computational check was independently re-executed from source/CSV and matched (Huber recon, R_f, geometry, integral flux, yields, emission, seam C1, band split, Billard-constant). The one open item is not a verification-confidence deficit but a known, bounded, honestly-flagged modeling limitation requiring expert judgment.

## 10. Summary

15/15 primary contract targets VERIFIED; 31/31 tests pass; 6 forbidden proxies rejected; 6/7 reference actions completed (ref-summation `use` PARTIAL). Overall: **PASSED-WITH-CAVEATS**, top-level `expert_needed` on the adequacy of the sub-1.8 MeV placeholder for downstream CEvNS precision.
