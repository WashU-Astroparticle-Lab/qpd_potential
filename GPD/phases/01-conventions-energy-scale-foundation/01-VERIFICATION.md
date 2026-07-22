---
phase: 01-conventions-energy-scale-foundation
verified: "2026-07-20T22:35:00Z"
status: passed
score: "15/15"
plan_contract_ref: GPD/phases/01-conventions-energy-scale-foundation/01-02-PLAN.md#/contract
contract_results:
  claims:
    claim-response-def:
      status: passed
      summary: "energy_scale.py implements the unified no-quenching chain N_qp=eps*E_sensor/Delta_tr -> n_qp=N_qp/V_tr -> Gamma_in=K*n_qp with the localized+diffuse split and two-exponential peak factor; both censoring variants are a switch at tau_d=40us; E_rec is a Phase-5 stub. Independently confirmed: 25 kHz ceiling (non-paralyzable monotone -> 25 kHz, paralyzable peaks at 25 kHz then rolls over to 25kHz/e=9197 Hz), Hf/Al plateau Gamma_in ratio 3.1667 (not 5-10x), onsets 1.267 eV (Al)/0.769 eV (Hf) with Hf first, and the equal-split discriminator (2 keV localized saturates ~1e6 Hz, equal-split ~4-6 kHz stays below 25 kHz, 1.5 MeV muon still saturates under equal-split ~3-5 MHz)."
      linked_ids: [deliv-energy-scale, test-lowrate, test-saturation, test-ordering, test-equalsplit, ref-qpd-paper, ref-qpd-repo]
    claim-assumptions:
      status: passed
      summary: "artifacts/stage1/ASSUMPTIONS.md is seeded with the unified no-quenching chain + forbidden keVee/keVnr and Lindhard proxies, localized+diffuse sharing (f_prompt=0.3 range 0.1-0.5, r=2 range 1-5, both flagged LOW/EXPOSED), eps~=0.5, both censoring variants (default non_paralyzable) with the OPEN paralyzable/non-paralyzable switch flagged as blocking Phase 5, defect=0, detector geometry (110 g wafer, ~10300 sensors, per-kg normalization), the verbatim Table II per-design table, the flagged Ta gap (0.68 meV bulk alpha-Ta MEDIUM), and BOTH the ~4.75x N_qp raw-yield ratio and the ~3.2x Gamma_in saturation-ordering ratio."
      linked_ids: [deliv-note, test-assumptions-content]
  deliverables:
    deliv-energy-scale:
      status: passed
      path: src/qpd_potential/energy_scale.py
      summary: "Pure-function yield/density/rate/peak-factor/sharing/censoring module importing all constants from params; both dead-time laws as a switch; E_rec NotImplementedError stub with linear_placeholder=True -> 0.5*E_dep. Imports cleanly; 15 energy-scale tests pass."
      linked_ids: [claim-response-def]
    deliv-note:
      status: passed
      path: artifacts/stage1/ASSUMPTIONS.md
      summary: "Stage-1 assumptions note covering all six assumption areas plus the Table II table, flagged Ta gap, both trapping ratios, and the OPEN censoring switch. Numbers cross-checked against params.py and CONVENTIONS.md."
      linked_ids: [claim-assumptions]
  acceptance_tests:
    test-lowrate:
      status: passed
      summary: "Both variants give m~=Gamma within 1% only for Gamma<=250 Hz; at 1 kHz deviation ~3.85-3.92% (~Gamma*tau_d=0.04), correctly NOT asserted at 1%. E_rec linear placeholder = 0.5*E_dep; default estimator raises NotImplementedError. Independently reproduced."
      linked_ids: [claim-response-def, deliv-energy-scale]
    test-saturation:
      status: passed
      summary: "Non-paralyzable m monotone, bounded by and -> 1/tau_d = 25 kHz; paralyzable argmax at Gamma~=25009 Hz with max=9197 Hz (=25kHz/e) then rolls over. Ceiling is 25 kHz, NOT 50 kHz. Independently reproduced."
      linked_ids: [claim-response-def, deliv-energy-scale]
    test-ordering:
      status: passed
      summary: "Plateau Gamma_in per eV ratio Hf/Al = 3.1667 (in [2.5,4.0], <5); N_qp per-eV ratio = 4.75 (raw yield). Onset(Al)=1.267 eV > Onset(Hf)=0.769 eV so Hf saturates first. Independently reproduced from Table II K, V_tr, Delta_tr."
      linked_ids: [claim-response-def, deliv-energy-scale]
    test-equalsplit:
      status: passed
      summary: "keV-scale (2 keV) deposit saturates when localized (f_prompt=0.3: ~9.4e5/1.6e6 Hz) but not under equal-split (f_prompt->0: 3836/6316 Hz < 25 kHz); a 1.5 MeV muon still saturates under equal-split (2.9e6/4.7e6 Hz), so localization sets degree not existence. Independently reproduced for both designs."
      linked_ids: [claim-response-def, deliv-energy-scale]
    test-assumptions-content:
      status: passed
      summary: "ASSUMPTIONS.md exists and contains every required section: unified no-quenching chain, forbidden proxies, sharing with f_prompt/r flagged LOW, eps, both censoring variants (default non_paralyzable) with OPEN switch, defect=0, Table II per-design table, flagged Ta gap, detector geometry with per-kg normalization."
      linked_ids: [claim-assumptions, deliv-note]
  references:
    ref-qpd-paper:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Table II device parameters transcribed verbatim (via 01-RESEARCH PDF p.14) into params.py and consumed by energy_scale.py; two-exponential peak factor and Gamma_in ordering derive from it; cited in code comments and ASSUMPTIONS.md."
    ref-qpd-repo:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "quasiparticle_bursts.py exists and was read; its EMG burst parametrization (N~Poisson, offsets Normal(mu,sigma)+Exp(tau)) fixes the peak-instantaneous-rate definition that peak_tunneling_rate approximates. Verbatim generator reuse deferred to Phase 5 as declared."
  forbidden_proxies:
    fp-nosat:
      status: rejected
      notes: "Default sharing is localized (f_prompt=0.3), under which keV deposits saturate; equal-split is exposed only as the f_prompt->0 sanity knob, never the default. test_equalsplit_is_not_the_default_sharing_model guards this."
    fp-derived-sharing:
      status: rejected
      notes: "f_prompt and r are tagged LOW and documented as EXPOSED/scannable parameters (not derived) in params.py, energy_scale.py docstrings, and ASSUMPTIONS.md."
    fp-20us:
      status: rejected
      notes: "tau_d = 40e-6 s (25 kHz ceiling) used everywhere; SAMPLING=20e-6 s kept distinct; test_saturation_ceiling_is_25kHz_not_50kHz asserts ceiling != 50 kHz."
    fp-nqp-ordering:
      status: rejected
      notes: "Ordering stated as the Gamma_in-based ~3.17x ratio, not the N_qp-only 4.75x or the mistaken 5-10x; both ratios recorded side-by-side in ASSUMPTIONS.md with Gamma_in flagged as the saturation driver."
  uncertainty_markers:
    weakest_anchors:
      - "f_prompt (0.3) and r (2 sensors) have no thin-wafer QPD measurement (LOW); muon spectrum shape depends strongly on them"
      - "Muon deposit point-collapse overstates per-sensor saturation vs a real ~cm track"
      - "Table II K and V_tr assumed to transfer to this wafer geometry"
      - "Ta absorber gap ~0.68 meV is a bulk alpha-Ta BCS assumption, film phase unverified (MEDIUM)"
    unvalidated_assumptions:
      - "Uniform diffuse spread of the (1-f_prompt) fraction across all ~10300 sensors"
      - "Trap-gap quantum (N_qp proportional to 1/Delta_tr) rather than an effective quantum nearer Delta_abs"
    competing_explanations:
      - "The DEGREE of the muon compression feature could be a point-collapse+localization artifact; the equal-split limit distinguishes degree from existence"
    disconfirming_observations:
      - "A keV-scale deposit that saturates under equal-split (checked false: 2 keV -> ~4-6 kHz/sensor < 25 kHz)"
      - "Non-paralyzable ceiling landing at 50 kHz instead of 25 kHz (checked false: 25 kHz)"
      - "Gamma_in^Hf/Gamma_in^Al far from ~3, e.g. 5-10x (checked false: 3.1667)"
---

<!-- ASSERT_CONVENTION: metric_signature=not_applicable — no relativistic field theory in this detector/rate pipeline, fourier_convention=not_applicable, natural_units=internal-only (hbar=c=1) for CEvNS cross section; k_B EXPLICIT (not =1); I/O in eV/keV/MeV, counts/kg/day/keV, s, cm/um; (hbar c)^2 = 3.894e-28 GeV^2 cm^2 -->

# Phase 1 Verification — Conventions & Energy-Scale Foundation

**Verdict:** passed · **Confidence:** HIGH · **Mode:** initial (no prior VERIFICATION.md)
**Plan reference (machine ledger):** `01-02-PLAN.md#/contract` (headline claim-response-def + deliv-note = 3 of the 4 goal elements). Plan `01-01` (params + CEvNS benchmark hook) is a full contract in its own right; the frontmatter schema binds one plan per phase report, so `01-01` is covered in the body below with the same computational rigor and is fully PASS.

## 1. Goal Achievement

Phase goal: *"The stage-1 bookkeeping is fixed and dimensionally consistent — a single unified phonon energy scale with no ionization quenching, the CEvNS cross-section convention and units, the E_dep→n_qp mapping, and the 50 kHz/25 kHz bandwidth-censoring rule — recorded in CONVENTIONS.md and seeded into the assumptions note."*

All four goal elements are established and independently confirmed:

| Goal element | Where fixed | Independent check | Status |
|---|---|---|---|
| Unified phonon scale, no quenching (NR+ER) | CONVENTIONS §B, params.py, energy_scale.py, ASSUMPTIONS.md §1 | No keVee/keVnr/Lindhard/quench token in live code; no ionization factor in the yield chain | VERIFIED |
| CEvNS cross-section convention + units | CONVENTIONS §C, cevns.py | σ(72Ge,4 MeV) full Q_W = 1.0026e-40 cm² via /4π + (ħc)² (see Oracle A) | VERIFIED |
| E_dep→n_qp mapping | CONVENTIONS §E, energy_scale.py, ASSUMPTIONS.md §2 | N_qp=ε·E/Δ_tr, n_qp=N_qp/V_tr, Γ_in=K·n_qp reproduced; dimensions Hz (see Oracle B) | VERIFIED |
| 50 kHz/25 kHz censoring rule | CONVENTIONS §F, energy_scale.py, ASSUMPTIONS.md §4 | Both variants at τ_d=40 µs; 25 kHz ceiling; OPEN switch flagged blocking Phase 5 | VERIFIED |

`CONVENTIONS.md` exists and is complete against Phase-1 success criteria 1–5 (Sections A–H + Numerical Factor Registry + cross-consistency table). `artifacts/stage1/ASSUMPTIONS.md` (deliv-note) is seeded with all required content.

## 2. Contract Coverage

**Plan 01-02 (machine ledger):** claims 2/2, deliverables 2/2, acceptance_tests 5/5, references 2/2 completed, forbidden_proxies 4/4 rejected → **15/15**.

**Plan 01-01 (body coverage, all PASS):**
- claim-params — params.py records Table II per-design (Al & Hf columns), absorber gaps (Al 190 µeV HIGH; Ta 0.68 meV MEDIUM flagged), Ge/reactor/CEvNS constants, sharing defaults, each with source+confidence. `test_conventions_consistency.py` (6 tests) passes: every registry constant matches; Δ_abs/Δ_tr = 3.58 (Ta→Al) and 4.75 (Al→Hf), both ≥ 2; Ta gap/f_prompt/r all tagged non-HIGH; no quenching token in params.py source. VERIFIED.
- claim-cevns-hook — cevns.py `weak_charge`/`sigma_tot` reproduce the benchmark (Oracle A). `test_cevns_benchmark.py` (5 tests) passes. VERIFIED.
- deliv-params (src/qpd_potential/params.py), deliv-cevns (src/qpd_potential/cevns.py) — exist, substantive, imported by downstream module. VERIFIED.
- test-conv-consistency (consistency) PASS; test-cevns-benchmark (benchmark) PASS — full Q_W within 0.26% of 1.0e-40 (target ±5%), N-only 1.079e-40 within tolerance of 1.08e-40 (±20%).
- ref-qpd-paper completed (read/use/cite). fp-prefactor / fp-quenching / fp-ta-invented all rejected (live code uses /4π and applies (ħc)²; no quenching; Ta gap carries citation + MEDIUM + film-phase flag).

## 3. Required Artifacts (levels 1–4)

| Artifact | Exists | Substantive | Content-valid | Integrated | Status |
|---|---|---|---|---|---|
| src/qpd_potential/params.py | ✓ | ✓ provenance dataclasses, no stubs | ✓ registry match | ✓ imported by cevns.py + energy_scale.py | VERIFIED |
| src/qpd_potential/cevns.py | ✓ | ✓ closed form | ✓ 1.0026e-40 cm² | ✓ Phase-3 hook | VERIFIED |
| src/qpd_potential/energy_scale.py | ✓ | ✓ pure functions, E_rec stub | ✓ all limits reproduced | ✓ Phase-5 module | VERIFIED |
| tests/ (3 files, 26 tests) | ✓ | ✓ | ✓ 26 passed | ✓ | VERIFIED |
| GPD/CONVENTIONS.md | ✓ | ✓ Sections A–H + registry | ✓ numerically consistent | ✓ authoritative projection | VERIFIED |
| artifacts/stage1/ASSUMPTIONS.md | ✓ | ✓ all 6 areas + Table II | ✓ matches params/CONVENTIONS | ✓ deliv-note | VERIFIED |

## 4. Computational Verification (oracles)

### Oracle A — CEvNS benchmark, dimensional trace, and unit-trap guards (independent, from scratch)

```python
import math
G_F = 1.1663787e-5      # GeV^-2
sin2 = 0.2387
hbarc2 = 3.894e-28      # GeV^2 cm^2
Z, N = 32, 40
E_nu = 4.0e-3           # GeV
Q_W = N - (1 - 4*sin2)*Z
sigma      = G_F**2 * Q_W**2 * E_nu**2 / (4*math.pi) * hbarc2   # correct /4pi + (hbar c)^2
sigma_N    = G_F**2 * N**2   * E_nu**2 / (4*math.pi) * hbarc2   # N-only
sigma_8pi  = G_F**2 * Q_W**2 * E_nu**2 / (8*math.pi) * hbarc2   # WRONG prefactor
sigma_GeV  = G_F**2 * Q_W**2 * E_nu**2 / (4*math.pi)           # WRONG: (hbar c)^2 dropped
print(Q_W, sigma, sigma_N, sigma_8pi, sigma_GeV)
# cross-check against repo module
import sys; sys.path.insert(0,'src'); from qpd_potential import cevns
print(cevns.sigma_tot_MeV(4.0,32,40), math.isclose(cevns.sigma_tot_MeV(4.0,32,40), sigma, rel_tol=1e-9))
```

**Output:**
```text
Q_W (full) = 38.5536
sigma full Q_W /4pi = 1.0026e-40 cm^2   (target ~1.0e-40)
sigma N-only /4pi   = 1.0792e-40 cm^2   (target ~1.08e-40)
sigma /8pi  (WRONG) = 5.0129e-41
without (hbar c)^2  = 2.5747e-13 GeV^-2
coefficient sigma/[N^2 (E/MeV)^2] = 4.2157e-45 cm^2   (target 4.22e-45)
repo sigma_tot_MeV(4,32,40) = 1.0026e-40 ; match with independent = True
```

**Verdict: PASS.** The convention asserts and reproduces the correct ~1.0e-40 cm² (NOT the wrong ~1e-42 in PITFALLS.md, which would be 100× low). Dimensional trace confirmed: [G_F²][E_ν²] = GeV⁻² → ×(ħc)² [GeV²·cm²] → cm². The /8π form gives ~5.0e-41 (factor-of-2 low) and is explicitly rejected by the ±5% full-Q_W test; dropping (ħc)² gives ~2.6e-13 GeV⁻² and is rejected by the cm²-range test. Coefficient 4.216e-45 matches the recorded 4.22e-45.

### Oracle B — Energy-scale chain, censoring, ordering, equal-split (independent, from Table II)

```python
import math, numpy as np
eps=0.5; tau_d=40e-6; ceiling=1/tau_d; Nsens=10300
D={"Ta->Al":dict(Delta=190e-6,V=100.,K=3e3,p=0.25),
   "Al->Hf":dict(Delta=40e-6, V=1000.,K=2e4,p=0.13)}
for n,d in D.items():
    peak_per_eV=d['p']*d['K']*eps/(d['Delta']*d['V']); onset=ceiling/peak_per_eV
    print(n, eps/d['Delta'], d['K']*eps/(d['Delta']*d['V']), onset)
G=np.logspace(2,7,4000); npm=G/(1+G*tau_d); parm=G*np.exp(-G*tau_d)
print(np.all(np.diff(npm)>0), npm.max()<=ceiling+1e-6, G[np.argmax(parm)], parm.max(), ceiling/math.e)
def peak(E,n,f,r=2.):
    d=D[n]; Es=f*E/(math.pi*r*r)+(1-f)*E/Nsens; return d['p']*d['K']*(eps*Es/d['Delta'])/d['V']
for n in D: print(n, peak(2000,n,0.3), peak(2000,n,1e-6), peak(1.5e6,n,1e-6))
```

**Output:**
```text
Ta->Al: N_qp/eV=2632, plateauGamma/eV=7.895e4 Hz, onset=1.267 eV
Al->Hf: N_qp/eV=1.25e4, plateauGamma/eV=2.500e5 Hz, onset=0.769 eV
N_qp ratio Hf/Al = 4.75 ; plateau Gamma ratio Hf/Al = 3.1667 ; Hf onset < Al onset = True
non-paralyzable monotone=True, <=ceiling=True ; paralyzable argmax G=25009, max=9197.0, 25kHz/e=9197.0
Ta->Al: 2keV loc=9.45e5 (sat), 2keV equal-split=3836 (<25k), 1.5MeV equal-split=2.877e6 (sat)
Al->Hf: 2keV loc=1.556e6 (sat), 2keV equal-split=6316 (<25k), 1.5MeV equal-split=4.737e6 (sat)
```

**Verdict: PASS.** 25 kHz ceiling exact (non-paralyzable monotone→25 kHz, never exceeds; paralyzable peaks at ~25 kHz then rolls over to 25kHz/e). Saturation ordering is the Γ_in-based 3.1667× (Hf/Al), explicitly NOT the 4.75× raw N_qp ratio and NOT the mistaken 5–10×; Hf onset 0.769 eV < Al 1.267 eV so Hf saturates first. Equal-split discriminator confirmed: a 2 keV deposit saturates when localized but not when spread (3836/6316 Hz < 25 kHz), while a 1.5 MeV muon still saturates under equal-split — localization sets degree, not existence.

### Oracle C — Full repo test suite

```bash
$ /opt/anaconda3/envs/mtf/bin/python -m pytest tests/ -q
```
**Output:** `26 passed in 0.10s`

**Verdict: PASS.** All convention-consistency (6), CEvNS-benchmark (5), and energy-scale limiting-case (15) tests pass.

## 5. Physics Consistency

- **Dimensional analysis:** σ chain GeV⁻²→cm² via (ħc)² (Oracle A); Γ_in = K[Hz·µm³]·n_qp[µm⁻³] = Hz, N_qp dimensionless, m in Hz (Oracle B). Consistent.
- **No-quenching / unified scale:** live code contains no keVee/keVnr/Lindhard/quench construct (guard comments only); NR and ER share the same E_dep→E_rec map. `test_no_quenching_symbols_in_params_source` enforces this.
- **Limiting cases:** low-rate linearity (correctly bounded to Γ≤250 Hz for 1%), 25 kHz saturation ceiling (both variants), Γ_in ordering, keV on/off + muon-still-saturates equal-split — all independently re-derived and matching.
- **Flagged assumptions honored:** Ta gap (0.68 meV bulk α-Ta, MEDIUM, film phase flagged) and f_prompt/r (LOW, EXPOSED) are tagged non-HIGH and carry explanatory notes; not treated as precise. The τ_qp(Hf)=400 µs vs 1 ms table-cell discrepancy is flagged MEDIUM.
- **OPEN censoring switch:** paralyzable-vs-non-paralyzable (and merge-vs-drop) preserved as an explicit code switch and flagged in CONVENTIONS §F and ASSUMPTIONS §4 as an OPEN question blocking Phase 5 — not silently chosen.

## 6. Forbidden-Proxy Audit

Plan 01-02: fp-nosat, fp-derived-sharing, fp-20us, fp-nqp-ordering — all REJECTED (see ledger notes; each has a guarding test). Plan 01-01: fp-prefactor (/8π or GeV⁻² left unconverted), fp-quenching (keVee/keVnr or Lindhard), fp-ta-invented (unflagged/wrong-phase Ta gap) — all REJECTED. No forbidden proxy is used as success evidence anywhere.

## 7. Comparison Verdict Ledger

No decisive benchmark/cross-method acceptance test and no compare-reference exist in the referenced plan (01-02), so no machine `comparison_verdicts` entry is required. For completeness, the phase's forward-hook benchmark (Plan 01-01, a Phase-3 hook, not a Phase-1 advanced claim per ROADMAP) is recorded in-body: σ(72Ge, 4 MeV) full Q_W = 1.0026e-40 cm² vs target 1.0e-40 cm², relative error 0.26% (≤5%) → **PASS** (Oracle A).

## 8. Anti-Patterns / Discrepancies Found

- **MINOR (tooling hygiene, non-physics):** The three phase code files (params.py, cevns.py, energy_scale.py) fail `gpd pre-commit-check` (`passed: False`, warnings) because their ASSERT_CONVENTION short-token values (e.g. `natural_units=internal_cevns_only`, `metric_signature=not_applicable`, `coupling_convention=cevns_4pi_QW`, `renormalization_scheme=tree_level_SM_...`) do not equal the verbose `convention_lock` strings, and the lock provides no value-alias mapping for these keys. The convention *content* is correct and numerically consistent (verified against the Numerical Factor Registry); this is a header-format vs lock-string mismatch at the tooling layer only. **Recommended follow-up (not blocking Phase 1's physics goal):** either add value aliases to the lock for these keys, or switch the code headers to comma-free exact lock values / the not_applicable fields. This VERIFICATION.md itself uses lock-matching values and passes the ASSERT_CONVENTION check cleanly.
- No TODO/FIXME/PLACEHOLDER, no unexplained magic numbers (all constants provenance-tagged), no division-by-zero risk, no float-equality hazard, no skipped-derivation/circular reasoning found. No blocker anti-patterns.

## 9. Requirements Coverage

CONV-01 (Phase 1 requirement per ROADMAP): SATISFIED — CONVENTIONS.md records the unified no-quenching chain, the /4π+Q_W+(ħc)² CEvNS convention, the E_dep→n_qp mapping with ε≈0.5 and detector normalization, and the 40/25 kHz censoring switch; all dimensionally checked and seeded into ASSUMPTIONS.md.

## 10. Cross-Phase Consistency

Phase 1 is the entry point (no prior phase); no cross-phase check applies. It sets the convention lock consumed downstream; convention_lock in state.json is authoritative and matches CONVENTIONS.md content.

## 11. Expert Verification Required

None blocking. Two items are appropriately flagged for later (Phase 5) firm-up, not Phase-1 blockers: (a) the Ta film-phase superconducting gap (α vs β Ta shifts T_c 5–9×), and (b) f_prompt/r localization parameters (no thin-wafer QPD measurement). Both are honestly tagged and exposed; verifying their true values requires device measurement/simulation beyond this bookkeeping phase.

## 12. Confidence Assessment

**HIGH.** The two decisive numbers (CEvNS σ = 1.0026e-40 cm²; Γ_in ordering 3.1667× with 25 kHz ceiling and eV-scale onsets) were re-derived independently from first principles and from Table II, matching the repo to machine precision. All 26 tests pass. The unified-no-quenching scale, both censoring variants, the OPEN switch flag, and every LOW/MEDIUM assumption flag are present and correct. The single finding is a non-physics tooling-hygiene warning.

## 13. Gaps Summary

No physics or evidence gaps. Phase goal achieved. One minor tooling follow-up (ASSERT_CONVENTION header vs lock-string matching for the three code files) is recorded for hygiene; it does not affect correctness, dimensional consistency, or any downstream physics and is not a decisive contract check.
