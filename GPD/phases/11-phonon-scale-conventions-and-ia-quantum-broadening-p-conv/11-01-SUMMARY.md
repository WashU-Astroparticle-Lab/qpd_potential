---
phase: 11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv
plan: 01
status: complete
one_liner: "The measured Ge VDOS (Nelin & Nilsson 1972 via NCrystal Ge_sg227.ncmat) gives <u_x^2> = 1.6096e-3 A^2 at T->0 and locks omega_bar = 17.8597 meV, which lands INSIDE the survey's 12-21 meV band, so that band survives; the analytic Debye oracle passes to 3.75e-11 and returns the 9/8 mean-ratio exactly, the DarkELF digitization agrees to -1.92% (reported, never averaged), and an unplanned cross-implementation check against NCrystal's own MSD agrees to 1.97e-5, simultaneously validating the normalization, the factor of 3, and the parabolic low-energy segment; 2W(100 meV) = 5.5992 lands inside 4.7-8.3 without tuning, and the VDOS turns out to have <w><1/w> = 1.3548, so a single-frequency sigma_E built on the locked omega_bar understates the IA width by 1.164x."
plan_contract_ref: GPD/phases/11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv/11-01-PLAN.md#/contract

contract_results:
  claims:
    claim-quadrature-correct:
      status: passed
      summary: "The analytic Debye oracle was written and run BEFORE any Ge number was quoted. Feeding g(w) = 3w^2/w_D^3 on [0, w_D] at theta_D = 374 K, T->0, the quadrature returns <u^2>_3D = 4.0139e-3 A^2 against the closed form 9 hbar^2/(4 m_N k_B theta_D) with relative error 3.75e-11 (tolerance 1e-3), and <u_x^2> = <u^2>_3D/3 with difference EXACTLY 0.0. A second analytic oracle was added: the Debye VDOS must satisfy <w><1/w> = 9/8 exactly, and it returns 1.124999999972. Both are independent of every Ge data file and of every project-internal prior estimate. A dedicated test asserts that building 2W from <u^2>/3 would change it by exactly 3x, so a future reintroduction of the factor-3 trap fails loudly."
      linked_ids: [deliv-phonon-module, deliv-tests, test-debye-oracle, test-dimensions, ref-computational]
      evidence:
        - verifier: gpd-executor
          method: "analytic closed-form oracle on an analytic VDOS input, plus an hbar*c scaling test proving the conversion is applied exactly once per path"
          confidence: high
          claim_id: claim-quadrature-correct
          deliverable_id: deliv-phonon-module
          acceptance_test_id: test-debye-oracle
          reference_id: ref-computational
          forbidden_proxy_id: fp-factor-three
          evidence_path: tests/test_phonon_scale.py
    claim-vdos-fidelity:
      status: passed
      summary: "BOTH sources were obtained. NCrystal Ge_sg227.ncmat: support ceiling 37.78966 meV against the 37.79 meV measured value, grid spacing 0.08023 meV. DarkELF Ge_pDoS.dat: ceiling 37.70769 meV, 0.082 meV below NCrystal and inside its own 0.12611 meV grid spacing. VDOS-integral <u_x^2> = 1.609619e-3 A^2 against the Debye baseline 1.337961e-3 A^2, ratio 1.2030, inside the SC2 factor-1.5 window. Cross-source: DarkELF gives 1.578654e-3, i.e. -1.92% -- inside the 10% requirement, reported and NOT averaged, with the sign and size EXPLAINED (DarkELF's digitization carries no support below 2.396 meV and <u_x^2> weights by 1/w, so a truncated acoustic tail biases it low). An unplanned third check was added: this module's quadrature reproduces NCrystal's own analyseVDOS()['msd'] = 6.931414999e-3 A^2 at 293.6 K to 1.97e-5 relative, which independently validates the int g dw = 1 normalization, the factor of 3 (NCrystal's msd IS the 1-D MSD), and the parabolic low-energy segment (dropping it moves the number by 8.5%)."
      linked_ids: [deliv-vdos-frozen, deliv-determination, test-vdos-ceiling, test-vdos-vs-debye, test-source-cross-check, ref-ncmat, ref-darkelf]
      evidence:
        - verifier: gpd-executor
          method: "two independent digitizations of the same 1972 measurement, compared under one quadrature and one normalization; plus a cross-implementation comparison against the source library's internal MSD"
          confidence: medium
          claim_id: claim-vdos-fidelity
          deliverable_id: deliv-vdos-frozen
          acceptance_test_id: test-source-cross-check
          reference_id: ref-ncmat
          forbidden_proxy_id: fp-debye-substitute
          evidence_path: data/external/ge_vdos/MANIFEST.md
    claim-omega-bar-locked:
      status: passed
      summary: "CONVENTIONS.md Section J locks ONE scalar omega_bar = 17.8597 meV, ONE <u_x^2> = 1.6096e-3 A^2, ONE B = 0.12709 A^2, the convention string 2W = q^2<u_x^2>, the rejected form q^2<u^2>/3 labelled REJECTED with its reason, and ONE citation (Nelin & Nilsson, Phys. Rev. B 5, 3151 (1972)). No range, no 'or', no 'between X and Y' appears on any LOCKED line, and a test parses Section J to enforce that. Mirrored into params.py as U_X_SQ_ANGSTROM2 / OMEGA_BAR_eV / OMEGA_BAR_ARITHMETIC_eV / DEBYE_WALLER_B_ANGSTROM2 / GE_THETA_D_K, and into the state.json convention lock under phonon_energy_scale and debye_waller_convention via gpd convention set (not hand-edited). Three Numerical Factor Registry rows and two Cross-Convention Consistency Check rows added. The milestone-wide prohibition -- the rate is NEVER multiplied by exp(-2W) -- is restated inside Section J."
      linked_ids: [deliv-conventions-j, deliv-determination, test-single-value-lock, test-2w-identity, ref-prior-work, ref-ncmat]
      evidence:
        - verifier: gpd-executor
          method: "machine parse of CONVENTIONS.md Section J for single-valuedness and the rejected form, plus params/derivation agreement at 1e-9"
          confidence: high
          claim_id: claim-omega-bar-locked
          deliverable_id: deliv-conventions-j
          acceptance_test_id: test-single-value-lock
          reference_id: ref-prior-work
          forbidden_proxy_id: fp-omega-range
          evidence_path: GPD/CONVENTIONS.md
  deliverables:
    deliv-vdos-frozen:
      status: passed
      path: data/external/ge_vdos/
      summary: "Five files: Ge_pDoS.dat (DarkELF, byte-for-byte as fetched), Ge_sg227_vdos_raw.csv (NCrystal density in its own arbitrary units, deliberately NOT renormalized so the renormalization factor stays auditable), ge_vdos_normalized.csv (headline, int g dw = 1, 1225 points), ge_vdos_darkelf_normalized.csv (same convention), MANIFEST.md. SHA-256 for every file, the exact retrieval command, package version 4.4.6, the underlying citation, the normalization convention, what the raw table integrated to before renormalization (4.1220017e-3) and the factor applied (1/4.1300746e-3). The generator scripts/freeze_ge_vdos.py is committed with the data."
      linked_ids: [claim-vdos-fidelity]
    deliv-phonon-module:
      status: passed
      path: src/qpd_potential/phonon_scale.py
      summary: "VDOS loader, coth-explicit T-dependent <u_x^2> quadrature with an EXACT T->0 branch (thermal_factor returns 1.0, not a coth at a small T), omega_bar, 2W(E_R) by both routes, B, q(E_R) in keV/c and inverse angstrom, the analytic Debye VDOS and its closed form, and vdos_moment_means for the harmonic/arithmetic mismatch. No Ge number is hard-coded: everything reads the frozen tables. Module docstring records the two algebraic consequences -- the q-route identity and the fact that m_N cancels out of omega_bar entirely."
      linked_ids: [claim-quadrature-correct, claim-vdos-fidelity, claim-omega-bar-locked]
    deliv-tests:
      status: passed
      path: tests/test_phonon_scale.py
      summary: "16 tests, all passing: the Debye oracle, the 9/8 mean-ratio oracle, an explicit factor-3-trap detector, dimensional checks including an hbar*c scaling test (scaling hbar*c by f must scale <u_x^2> by f^2 and q by 1/f, leaving 2W invariant), normalization, ceiling, Debye comparison, cross-source not-averaged, the NCrystal cross-implementation check, the T->0 justification, the 2W identity at 1e-14 with the identity stated in the docstring, mass-freedom over a 2000x mass range, the moment mismatch, params/derivation agreement, and two CONVENTIONS.md Section J parsers."
      linked_ids: [claim-quadrature-correct, claim-vdos-fidelity, claim-omega-bar-locked]
    deliv-conventions-j:
      status: passed
      path: GPD/CONVENTIONS.md
      summary: "Section J added in the table style of Sections E/F/I, plus one Change Log row, three Numerical Factor Registry rows (Debye-Waller exponent, VDOS normalization, effective phonon energy) and two Cross-Convention Consistency Check rows (Section B unified phonon scale via the SuperCDMS 19.7 eV displacement threshold with no defect below ~6 eV; Section C recoil kinematics via the shared m_N). Mirrored to state.json through gpd convention set."
      linked_ids: [claim-omega-bar-locked]
    deliv-determination:
      status: passed
      path: GPD/phases/11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv/11-01-VDOS-DETERMINATION.md
      summary: "Nine sections: the answer; what the two candidates physically ARE and why the <u^2>-derived definition wins (because it is the one that makes 2W = E_R/omega_bar exact, NOT because 37 meV is wrong); the derivation with both halves of the normalization pair on one line; the oracle gate; both sources side by side with the argued adoption and the EXPLANATION of the -1.9%; SC1 and SC2 clause by clause; the survey-band verdict with the pre-commitment recorded; the temperature table; the 2W/q table; and residual uncertainty. States plainly that the phase resolved a NOTATION COLLISION and made a definitional choice forced by downstream algebra, and did not discover new physics about germanium."
      linked_ids: [claim-vdos-fidelity, claim-omega-bar-locked]
  acceptance_tests:
    test-debye-oracle:
      status: passed
      summary: "Relative error 3.75e-11 on <u^2>_3D against 9 hbar^2/(4 m_N k_B theta_D), tolerance 1e-3; the test additionally asserts < 1e-8 so the margin is visible rather than merely sufficient. <u_x^2> = <u^2>_3D/3 to difference EXACTLY 0.0. Re-derived values 4.0139e-3 and 1.3380e-3 A^2, computed from the closed form in code, not pasted."
      linked_ids: [claim-quadrature-correct, deliv-phonon-module, deliv-tests]
    test-vdos-ceiling:
      status: passed
      summary: "NCrystal 37.78966 meV, within 0.08023 meV (one grid spacing) of 37.79. DarkELF 37.70769 meV, within its own 0.12611 meV spacing. The two agree with each other to 0.082 meV. Note the definition matters: 'ceiling' is the support endpoint, not the last grid point with non-zero density -- NCrystal's spectrum terminates by carrying g = 0 exactly at its final row, so a last-non-zero reading would have understated the ceiling by 0.080 meV."
      linked_ids: [claim-vdos-fidelity, deliv-vdos-frozen]
    test-vdos-vs-debye:
      status: passed
      summary: "Ratio 1.2030, inside the ROADMAP SC2 factor-1.5 window in either direction. The measured VDOS gives a LARGER <u_x^2> than Debye because real Ge carries more weight in the flat low-lying transverse acoustic branches and <u_x^2> weights by 1/w."
      linked_ids: [claim-vdos-fidelity, deliv-phonon-module]
    test-source-cross-check:
      status: passed
      summary: "PERFORMED, not skipped: both sources were obtained. -1.92% on <u_x^2> (1.609619e-3 vs 1.578654e-3), +1.96% on omega_bar (17.8597 vs 18.2100 meV), against a 10% requirement. NOT averaged -- the test asserts the locked value equals the NCrystal value and is NOT the mean of the two. NCrystal carries the headline for three reasons argued from the data: finer digitization, physical low-energy behaviour, and the direct measurement citation."
      linked_ids: [claim-vdos-fidelity, deliv-vdos-frozen, deliv-determination]
    test-2w-identity:
      status: passed
      summary: "2W = q^2<u_x^2> and 2W = E_R/omega_bar agree to < 1e-14 when both are taken from the same <u_x^2>, and to < 1e-10 against the params.py literals (limited by their 11-significant-figure printed precision, not by physics). The test docstring states in words that this is an ALGEBRAIC IDENTITY, not independent corroboration. Units check: q(100 meV) = 116.383 keV/c = 58.980 inverse angstrom against the expected 116 keV/c = 58.9. 2W(100 meV) = 5.5992, reported against the ROADMAP band 4.7-8.3 and landing inside it without tuning."
      linked_ids: [claim-omega-bar-locked, deliv-phonon-module, deliv-determination]
    test-single-value-lock:
      status: passed
      summary: "Section J parsed: the locked lines carry no ' or ', no 'between', and no en-dash range; 2W = q^2 <u_x^2> present; REJECTED present; B = 8 pi^2 present; the exp(-2W) prohibition present; exactly one citation string. params.py scalars equal the derivation to 1e-9 and are internally consistent (B = 8 pi^2 <u_x^2>, omega_bar = hbar^2/(2 m_N <u_x^2>)). tests/test_conventions_consistency.py stays green."
      linked_ids: [claim-omega-bar-locked, deliv-conventions-j, deliv-tests]
    test-dimensions:
      status: passed
      summary: "<u_x^2> in angstrom^2, omega_bar in eV at the meV scale, 2W dimensionless, B = 8 pi^2 <u_x^2> to 1e-15. hbar*c applied exactly once per path, proven by perturbing HBAR_C_eV_ANGSTROM by a factor f and checking <u_x^2> scales as f^2 while q[1/angstrom] scales as 1/f -- so 2W is invariant, which is the correct behaviour and would break if hbar*c were applied twice or zero times on either path."
      linked_ids: [claim-quadrature-correct, deliv-phonon-module, deliv-tests]
    test-disposition-row:
      status: passed
      summary: "Three rows added to artifacts/v2.0/legacy_grid_disposition.csv with disposition not_a_spectrum and reasons naming the files as VDOS input on a phonon-energy abscissa rather than spectra on the shared deposit axis. tests/test_legacy_grid_disposition.py passes 30/30. Note the register enumerates git-TRACKED files, so the rows only close once the data is committed."
      linked_ids: [deliv-vdos-frozen]
  references:
    ref-ncmat:
      status: completed
      completed_actions: [read, use, compare, cite]
      missing_actions: []
      summary: "Read via NCrystal 4.4.6, used as the headline VDOS, compared against DarkELF and against the Debye baseline, and cited in CONVENTIONS.md Section J as the single citation. The underlying measurement (Nelin & Nilsson, Phys. Rev. B 5, 3151 (1972), DOI 10.1103/PhysRevB.5.3151) is what is cited; NCrystal is named as the delivery vehicle."
    ref-darkelf:
      status: completed
      completed_actions: [use, compare]
      missing_actions: []
      summary: "Fetched from github.com/tongylin/DarkELF branch main at data/Ge/Ge_pDoS.dat (note: no darkelf/ path component; the obvious URL 404s, and there is no darkelf package on PyPI). Used under the identical quadrature and normalization; agrees to -1.92% on <u_x^2>. Reported, argued against as the headline, never averaged."
    ref-prior-work:
      status: completed
      completed_actions: [read, compare, avoid]
      missing_actions: []
      summary: "Read as the COMPARISON TARGET only. The 12-21 meV band, the 4.7-8.3 2W band and the 1.34e-3 A^2 Debye value appear in this phase's artifacts exclusively in comparison columns with explicit verdicts, never as inputs and never as citations. Its central warning was honoured: SUMMARY.md line 37's 'the only real disagreement is the label omega_bar' is quoted and acted on in the determination artifact, which explicitly declines to present the resolution as a physics discovery."
    ref-computational:
      status: completed
      completed_actions: [read, use, compare]
      missing_actions: []
      summary: "Supplied the analytic Debye closed form used as the oracle and the SC2 factor-1.5 tolerance. The 4.02e-3 / 1.34e-3 A^2 baselines were RE-DERIVED from the closed form in code (4.0139e-3 / 1.3380e-3) rather than pasted, and the 37.79 meV ceiling was re-read from the frozen file."
  forbidden_proxies:
    fp-factor-three:
      status: rejected
      notes: "2W = q^2<u_x^2> with the 1-D MSD throughout. q^2<u^2>/3 appears exactly once in CONVENTIONS.md Section J, labelled REJECTED with its reason. Three independent guards: the analytic Debye oracle (a 3x error would show as a 3x oracle failure), an explicit test asserting that the trapped form differs by exactly 3x, and the cross-implementation match against NCrystal's own 1-D msd to 1.97e-5."
    fp-debye-substitute:
      status: rejected
      notes: "The Debye model appears only as (a) an input to the analytic oracle and (b) a comparison baseline with an explicit ratio. omega_bar and <u_x^2> come from the measured spectrum. Both external sources were successfully obtained, so no fallback situation arose. Recorded for the record: NCrystal's own VDOS-fitted Debye temperature for this spectrum is 295.35 K, NOT the 374 K oracle input -- they are different estimators and the disagreement is expected."
    fp-quote-survey-numbers:
      status: rejected
      notes: "Every Ge number in CONVENTIONS.md Section J, params.py and the determination artifact was computed in-phase from the frozen VDOS by a recorded command. The survey's 12-21 meV, 4.7-8.3 and 1.34e-3 A^2 appear only in comparison columns labelled as targets."
    fp-omega-range:
      status: rejected
      notes: "ONE scalar omega_bar = 17.8597 meV. A machine test parses Section J and fails on ' or ', 'between', or an en-dash range appearing on any LOCKED line."
    fp-q-route-as-independent:
      status: rejected
      notes: "The q-route is run and reported explicitly as a UNITS CHECK. The determination artifact states that with q^2 = 2 m_N E_R and omega_bar = hbar^2/(2 m_N <u_x^2>) the two expressions are the same expression, that SC2's 2W clause is likewise not independent of SC1's omega_bar, and that SC2 therefore has exactly TWO genuinely independent legs (the measured ceiling and the VDOS-vs-Debye comparison). Section 4.1 adds an unplanned third."
  uncertainty_markers:
    weakest_anchors:
      - "Everything rests on a SINGLE 1972 inelastic-neutron measurement (Nelin & Nilsson). The two available digitizations agree to 1.9%, which bounds digitization error but says nothing about measurement error. No independent modern Ge VDOS was obtained."
      - "The parabolic low-energy segment below 3.771 meV contributes +1.21% to <u_x^2> at T->0. Its PRESENCE is verified from NCrystal's own reported integral (agreeing with density[0]*egrid[0]/3 to 1.5e-8), but the w^2 form itself is a model, not data."
      - "The survey band 12-21 meV remains DERIVED in-survey at MED confidence. It was used only as a comparison target; the fact that omega_bar landed inside it is a coincidence of two independent estimates agreeing, not a validation of either."
      - "The 0.10% ambiguity in natural-Ge mass averaging (72.7053 u from params.GE_ISOTOPES integer-A weighting vs 72.632249 u carried by the ncmat file) moves <u_x^2> and B by 0.10%. It does NOT move omega_bar or 2W at all, because m_N cancels."
    unvalidated_assumptions:
      - "Harmonic lattice. At mK the displacement is zero-point dominated, which is the most favourable case, but anharmonic corrections to <u_x^2> are not quantified anywhere in this phase."
      - "That a symmetric Gaussian is adequate at 2W = 5.6. Not this plan's job; SC5 / plan 11-04 must bound it."
      - "PROMOTED TO VALIDATED: the T->0 reduction. Previously asserted, now measured -- at 10 mK the full coth form differs from the exact limit by 5e-9 relative."
    competing_explanations:
      - "The 37 meV optical-phonon value is NOT wrong. It is the zone-centre LO energy, a different quantity wearing the same symbol. This plan resolved a NOTATION COLLISION and made a definitional choice forced by the downstream algebra (only omega_bar = hbar^2/(2 m_N <u_x^2>) makes 2W = E_R/omega_bar exact). It did not discover new physics about germanium and the determination artifact says so explicitly."
      - "omega_bar landing inside 12-21 meV could be read as the survey being confirmed. The honest reading is weaker: the survey's upper end 21 meV is essentially the Debye-model value 21.486 meV for the same mass and theta_D, so 'inside the band' partly means 'not far from Debye', which the factor-1.203 ratio already said."
    disconfirming_observations:
      - "RAN, DID NOT FIRE: the analytic Debye oracle (3.75e-11, needed < 1e-3)."
      - "RAN, DID NOT FIRE: the VDOS ceiling check (37.78966 vs 37.79 meV)."
      - "RAN, DID NOT FIRE: NCrystal vs DarkELF disagreement (-1.92%, threshold 10%)."
      - "RAN, DID NOT FIRE: omega_bar outside 12-21 meV. It landed at 17.860 meV, inside. The pre-commitment stood: no quadrature, normalization, temperature or mass adjustment was made toward the band, and SC2's own tolerance maps to the WIDER window [14.3, 32.2] meV, so landing outside was live."
      - "RAN, DID NOT FIRE: the 9/8 Debye mean-ratio oracle (1.124999999972)."
      - "NEW, UNPLANNED, RAN AND PASSED: cross-implementation against NCrystal's internal msd at 293.6 K, 1.97e-5. This one would have fired at 8.5% had the parabolic low-energy segment been dropped, and at ~200% had the factor of 3 been wrong."
---

# Plan 11-01 — Phonon scale pinned from the measured Ge VDOS (CALC-14)

## Locked scalars

| Quantity | Value | Where |
|---|---|---|
| ⟨u_x²⟩ (1-D MSD, T→0) | **1.6096194483 × 10⁻³ Å²** | `params.U_X_SQ_ANGSTROM2` |
| **ω̄ ≡ ħ²/(2 m_N ⟨u_x²⟩)** | **17.8597 meV** (1.7859677040 × 10⁻² eV) | `params.OMEGA_BAR_eV` |
| B = 8π²⟨u_x²⟩ | **0.1270904575 Å²** | `params.DEBYE_WALLER_B_ANGSTROM2` |
| 2W(100 meV) | **5.5992** | derived |
| VDOS arithmetic mean ⟨ω⟩ | **24.1955 meV** | `params.OMEGA_BAR_ARITHMETIC_eV` |
| Convention | **2W = q²⟨u_x²⟩** (1-D); `q²⟨u²⟩/3` REJECTED | `CONVENTIONS.md` §J |
| Citation | Nelin & Nilsson, Phys. Rev. B **5**, 3151 (1972) | via NCrystal 4.4.6 `Ge_sg227.ncmat` |

## Did the survey band survive?

**Yes.** ω̄ = 17.860 meV is inside 12–21 meV, and inside the wider window [14.3, 32.2] meV that
SC2's own factor-1.5 ⟨u_x²⟩ tolerance maps to. The band is **not** superseded.

Read it carefully, though: the Debye-model ω̄ for the same mass and θ_D = 374 K is **21.486 meV**,
essentially the top of the survey band — so "inside the band" partly restates "within 1.203× of
Debye", which the ⟨u_x²⟩ ratio already said. The two legs are less independent than the two numbers
look.

## SC1 / SC2 clause-by-clause

| Criterion | Clause | Verdict |
|---|---|---|
| SC1 | pinned from the real Ge VDOS, not the Debye model | **PASS** |
| SC1 | `2W = q²⟨u_x²⟩` locked | **PASS** |
| SC1 | `q²⟨u²⟩/3` explicitly rejected | **PASS** |
| SC1 | `B = 8π²⟨u_x²⟩` quoted alongside | **PASS** (0.12709 Å²) |
| SC1 | one number / one convention / one citation, no range | **PASS** (machine-parsed) |
| SC2 | ceiling 37.79 meV | **PASS** (37.78966 meV) |
| SC2 | VDOS ⟨u_x²⟩ within ~1.5× of Debye | **PASS** (ratio 1.2030) |
| SC2 | 2W(100 meV) in 4.7–8.3 | **PASS** (5.5992, untuned) |
| SC2 | consistent with q = 116 keV/c = 58.9 Å⁻¹ | **PASS as a UNITS IDENTITY**, not corroboration (116.383 keV/c = 58.980 Å⁻¹) |

## What this hands to 11-02 and 11-03

**The moment mismatch is real and larger than Debye.** ⟨u_x²⟩ is set by the VDOS **harmonic** mean;
⟨p_x²⟩ — which sets σ_E — is set by the **arithmetic** mean.

| Spectrum | harmonic | arithmetic | ⟨ω⟩⟨1/ω⟩ | √(⟨ω⟩⟨1/ω⟩) |
|---|---|---|---|---|
| Debye (oracle) | 21.4859 meV | 24.1717 meV | 1.125 exactly | 1.06066 |
| **Measured Ge** | **17.8597 meV** | **24.1955 meV** | **1.354758** | **1.16394** |

So `σ_E = √(E_R ω̄)` built on the locked ω̄ **understates** the IA width by **1.164×** for real Ge.
Plan 11-02 must derive this from the VDOS moments and plan 11-03 must reproduce it independently
from the exact second central moment of S(q,ω); a disagreement between those two routes **blocks
11-04**.

## Deviations

* **[Rule 4 — missing component]** The Phase-10 interpolator-inventory closure guard
  (`tests/test_interpolator_bounds.py`) failed at 34 grep hits against a hard-coded 33, because
  `phonon_scale.vdos_weight_quantile_meV` introduced a new `np.interp` call site. Registered it in
  `10-01-INTERPOLATOR-INVENTORY.md` with a full domain declaration and bumped the count to 34 with
  a comment stating that bumping is the only sanctioned response and must come with a row. The
  alternative — hand-rolling the interpolation to dodge the grep — was rejected as exactly the
  evasion the guard exists to catch.
* **[Rule 1 — code fix]** `vdos_ceiling_meV` initially returned the last grid point with non-zero
  density, which for the NCrystal table is 37.70943 meV rather than the support endpoint 37.78966
  meV (its final row carries g = 0 exactly). Changed to the support endpoint and split the other
  reading into `vdos_last_nonzero_meV`. Both readings pass the one-grid-spacing tolerance; the
  first would have understated the measured ceiling by 0.080 meV.
* **[Rule 1 — code fix]** `vdos_floor_meV` was meaningless for the NCrystal table, whose parabolic
  segment reaches 1e-9 meV by construction. Replaced with `vdos_weight_quantile_meV`, and the
  T→0 justification is now carried by a direct 10 mK evaluation rather than by a floor ratio.
* Precision note, not a deviation: `params.py` literals carry 11 significant figures, so
  identity checks against them hold to 1e-10 rather than 1e-14. The identity itself is asserted at
  1e-14 using values from a single source.

## Suite

**534 passed, 0 failed** (518 baseline + 16 new in `tests/test_phonon_scale.py`).
`data/flux/*.csv` provenance-header churn reverted before commit.

## Artifacts

`data/external/ge_vdos/{MANIFEST.md, Ge_pDoS.dat, Ge_sg227_vdos_raw.csv, ge_vdos_normalized.csv,
ge_vdos_darkelf_normalized.csv}` · `scripts/freeze_ge_vdos.py` ·
`src/qpd_potential/phonon_scale.py` · `src/qpd_potential/params.py` ·
`tests/test_phonon_scale.py` · `GPD/CONVENTIONS.md` §J ·
`GPD/phases/11-.../11-01-VDOS-DETERMINATION.md` · `artifacts/v2.0/legacy_grid_disposition.csv`
