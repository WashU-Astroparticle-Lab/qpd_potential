---
phase: 11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv
plan: 02
status: complete
one_liner: "sigma_E = sqrt(E_R omega_bar) re-derived in-phase from the IA momentum distribution (mean E_R exact, m_N cancelling identically), giving 42.261% / 18.900% / 13.364% / 4.226% / 1.336% at 0.1 / 0.5 / 1 / 10 / 100 eV -- all four ROADMAP SC3 bands hit, but that is agreement by shared ancestry since the bands were built from the same 12-21 meV range the locked omega_bar sits inside; the informative result is the moment mismatch, where the disconfirming check FIRED: the real Ge VDOS gives <w><1/w> = 1.3548 against the Debye 9/8, so the physically correct arithmetic mean raises every width by 16.4% and pushes ALL FOUR moment-corrected values ABOVE their SC3 bands; quadrature with the Phase-10 best-case counting floor at 0.5 eV gives 24.769% (Ta->Al) and 23.682% (Al->Hf), inside 22-26%, with the IA width now the LARGER contribution; and 'negligible above ~100 eV' resolves to a sub-bin crossing at 20.940 eV, five times more conservative than stated."
plan_contract_ref: GPD/phases/11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv/11-02-PLAN.md#/contract

contract_results:
  claims:
    claim-sigma-derivation:
      status: passed
      summary: "Derived from w = q^2/(2 m_N) + q.p/m_N, not from the closed form. <w> = q^2/(2 m_N) = E_R exactly (verified to 1e-15 at every tabulated energy, so the broadening does not shift the centroid); Var(w) = q^2 sigma_p^2/m_N^2 with sigma_p the 1-D momentum spread; sigma_p^2 = m_N omega_bar/2 from the zero-point oscillator; hence sigma_E = q sigma_p/m_N = sqrt(E_R omega_bar). Implemented as a SEPARATE code path (sigma_E_from_momentum_distribution) so the closed form is checked against the argument it came from rather than merely asserted, and m_N is shown to cancel over a 28x mass range. Units close with hbar restored: q and sigma_p in eV/c, m_N in eV/c^2."
      linked_ids: [deliv-ia-module, deliv-width-derivation, test-sigma-derivation, test-sigma-dimensions, test-identity-flag, ref-sears, ref-campbell-deem]
      evidence:
        - verifier: gpd-executor
          method: "two independent code paths for the same width, plus a scaling test under deliberate factor-2 perturbations of E_R and omega_bar"
          confidence: high
          claim_id: claim-sigma-derivation
          deliverable_id: deliv-ia-module
          acceptance_test_id: test-sigma-derivation
          reference_id: ref-sears
          forbidden_proxy_id: fp-identity-as-evidence
          evidence_path: GPD/phases/11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv/11-02-IA-WIDTH-DERIVATION.md
    claim-width-table:
      status: passed
      summary: "Fractional widths re-derived from the locked omega_bar: 42.261% at 100 meV (band 35-46%, IN), 18.900% at 0.5 eV (15.5-20.5%, IN), 13.364% at 1 eV (11-15%, IN), 4.226% at 10 eV (no band), 1.336% at 100 eV (1.1-1.5%, IN). Every value computed by ia_broadening.fractional_width; none transcribed. The artifact states plainly that the four IN BAND verdicts carry little weight, because the bands were generated from the survey's omega_bar = 12-21 meV and the locked 17.860 meV sits inside it -- agreement by shared ancestry. Sub-bin crossing: one extended-grid bin is 2.92047% (79.988714 bins/decade), and sigma_E/E_R falls below it at E_R = 20.940 eV, so 'negligible above ~100 eV' is conservative by a factor ~5."
      linked_ids: [deliv-width-table, deliv-width-derivation, test-width-bands, test-sub-bin-crossing, ref-prior-work-widths]
    claim-quadrature:
      status: passed
      summary: "At 0.5 eV: IA width 18.900% combined in quadrature with the Phase-10 PIPELINE-DERIVED counting floors 16.009% (Ta->Al) and 14.271% (Al->Hf) gives 24.769% and 23.682%, both inside the ROADMAP 22-26% band. Using the ROADMAP comparison floors 15.9/14.2 instead gives 24.698% / 23.640%, so the verdict does not hinge on the choice. Never summed linearly (that would give 34.9% / 33.2%). The independence that licenses quadrature -- sensor quasiparticle counting statistics versus nuclear zero-point motion -- is stated as an ASSERTION, not proven. The best-case-no-noise-sources caveat travels with every use of the floor, in the module constant, the CSV header, and the derivation artifact, enforced by a test. NEW FINDING: the IA width is now the LARGER of the two contributions at 0.5 eV, overtaking the Ta->Al floor at 0.70 eV and the Al->Hf floor at 0.88 eV, both below the 1 eV regime boundary."
      linked_ids: [deliv-width-table, deliv-width-figure, test-quadrature, ref-counting-floor]
    claim-mean-systematic:
      status: passed
      summary: "THE DISCONFIRMING CHECK FIRED. The analytic Debye oracle passed first (w_p = 3w_D/4 = 24.1716 meV, w_u = 2w_D/3 = 21.4859 meV, ratio 1.1249999999719 against the exact 9/8, i.e. 2.5e-11), validating the diagnostic before it touched Ge. On the measured Ge VDOS the ratio is 1.354758, materially WORSE than Debye, giving a one-sided width correction sqrt(w_p/w_u) = 1.163941, i.e. +16.4% on every width rather than the +6.1% a Debye spectrum would give. Cause: real Ge has flat heavily-populated transverse-acoustic branches near 8 meV AND a separated optical group near 35 meV, which spreads the arithmetic and harmonic means further apart than a smooth w^2 density can. w_u reproduces the locked omega_bar to 1e-9, as it must. Consequence: all four moment-corrected widths land ABOVE the upper edge of their SC3 bands, and the 0.5 eV quadrature rises to 27.19% / 26.20%, above the 22-26% band."
      linked_ids: [deliv-ia-module, deliv-width-derivation, test-mean-ratio, test-debye-mean-ratio-oracle, ref-sears]
      evidence:
        - verifier: gpd-executor
          method: "analytic Debye closed-form oracle on the moment diagnostic, then evaluation on the frozen measured VDOS, with Cauchy-Schwarz one-sidedness asserted in code"
          confidence: high
          claim_id: claim-mean-systematic
          deliverable_id: deliv-ia-module
          acceptance_test_id: test-debye-mean-ratio-oracle
          reference_id: ref-sears
          forbidden_proxy_id: fp-single-mode-assumption
          evidence_path: tests/test_ia_broadening.py
  deliverables:
    deliv-ia-module:
      status: passed
      path: src/qpd_potential/ia_broadening.py
      summary: "sigma_E_eV, sigma_E_from_momentum_distribution (the long route, kept separate on purpose), mean_energy_transfer_eV, fractional_width, sub_bin_crossing_energy_eV, vdos_means / debye_vdos_means / sigma_E_upper_moment_eV for the moment systematic, and quadrature_with_counting_floor. Imports omega_bar from params.py; hard-codes no phonon numbers. The best-case caveat is a module constant interpolated into the quadrature function's own docstring so it cannot be used without it."
      linked_ids: [claim-sigma-derivation, claim-mean-systematic]
    deliv-width-table:
      status: passed
      path: artifacts/v2.0/ia_broadening_widths.csv
      summary: "749 rows -- the five ROADMAP energies plus all 744 extended-grid centres -- with E_R, sigma_E, frac_width, two_W, frac_width_upper_moment, both counting floors, both quadrature sums, and an is_roadmap_energy flag. The header records the locked omega_bar, the identity warning, the one-sided moment correction, the best-case caveat, the never-linear rule, and the sub-bin crossing energy. The floors are held CONSTANT across the table because Phase 10 evaluated them only at 0.49382 eV; they are explicitly NOT extrapolated."
      linked_ids: [claim-width-table, claim-quadrature]
    deliv-width-figure:
      status: passed
      path: artifacts/v2.0/ia_width_vs_counting_floor.png
      summary: "Log-log over 0.1-1000 eV: the IA width, the shaded one-sided moment band up to the arithmetic-mean curve, both counting-floor points labelled BEST CASE in the legend, the 2.92% one-bin line with the 20.9 eV crossing starred, the 0.5 eV trigger 50% point, the 1.0 eV sub-eV regime boundary imported from trigger.SUBEV_REGIME_BOUNDARY_eV, and the two energies at which the IA width overtakes each floor."
      linked_ids: [claim-quadrature]
    deliv-width-derivation:
      status: passed
      path: GPD/phases/11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv/11-02-IA-WIDTH-DERIVATION.md
      summary: "Nine sections: the full momentum-distribution derivation with the mean and variance computed separately; the identity flag with the demonstration that the relation holds for absurd omega_bar values too; the moment mismatch derived from the same normal-mode expansion as <u_x^2>, with the Debye oracle table first and the Ge result second; the width table with both headline and moment-corrected verdicts; the quadrature section with the best-case caveat repeated and an explicit 'what this comparison is not' paragraph; the sub-bin crossing; the Phase-15 scope boundary; and four ways the numbers could be overturned."
      linked_ids: [claim-sigma-derivation, claim-width-table, claim-mean-systematic]
  acceptance_tests:
    test-sigma-derivation:
      status: passed
      summary: "sigma_E built from q and sigma_p equals sqrt(E_R omega_bar) to 1e-15 at all five ROADMAP energies; the mean energy transfer equals E_R to 1e-15; m_N cancels to 1e-14 across a 28x mass range. The derivation artifact writes the momentum-distribution argument out in full rather than quoting the closed form."
      linked_ids: [claim-sigma-derivation, deliv-ia-module, deliv-width-derivation]
    test-sigma-dimensions:
      status: passed
      summary: "sigma_E(4 E_R) = 2 sigma_E(E_R) and sigma_E(4 omega_bar) = 2 sigma_E(omega_bar) to 1e-14; sigma_E(1 eV) equals sqrt(omega_bar) and lands at the 0.1 eV scale; fractional width dimensionless; the sigma_p^2 = m_N omega_bar/2 route reproduces the closed form to 1e-14."
      linked_ids: [claim-sigma-derivation, deliv-ia-module]
    test-identity-flag:
      status: passed
      summary: "sigma_E/E_R * sqrt(2W) = 1 to 1e-14 at every ROADMAP energy -- AND at omega_bar = 0.1 meV, 0.5 eV and 12 eV, none of which is a phonon energy in germanium. That is the point: the relation is true by construction for ANY omega_bar and is therefore not evidence about Ge. The test also asserts the artifact contains 'identity', 'true by construction' and 'fp-identity-as-evidence'."
      linked_ids: [claim-sigma-derivation, deliv-width-derivation]
    test-width-bands:
      status: passed
      summary: "All four SC3 energies IN BAND: 42.261/[35,46], 18.900/[15.5,20.5], 13.364/[11,15], 1.336/[1.1,1.5]. Values asserted numerically at the level they were derived, not at the band level, so a drift in omega_bar would fail this test even while staying in band. The docstring records that agreement here is expected and weak."
      linked_ids: [claim-width-table, deliv-width-table]
    test-sub-bin-crossing:
      status: passed
      summary: "One bin = 2.920471%; crossing at E_R = 20.9396 eV, inside the required 10-100 eV window; the round trip fractional_width(crossing) == one bin holds to 1e-12."
      linked_ids: [claim-width-table, deliv-width-table]
    test-quadrature:
      status: passed
      summary: "24.7686% (Ta->Al) and 23.6824% (Al->Hf), both inside 22-26%; each verified strictly less than the linear sum; the same verdict reproduced with the ROADMAP comparison floors so it does not depend on which floor set is used. A separate test asserts the best-case caveat appears in the module constant, in the quadrature function's docstring, in the CSV header and at least four times in the derivation artifact, alongside fp-poisson-as-resolution."
      linked_ids: [claim-quadrature, deliv-width-table, deliv-width-figure]
    test-debye-mean-ratio-oracle:
      status: passed
      summary: "w_p = 3 w_D/4 and w_u = 2 w_D/3 to 1e-6 relative; ratio = 9/8 to 2.5e-11 (the test demands 1e-3 and then re-asserts 1e-9 so the margin is visible); sigma_correction = sqrt(9/8) = 1.060660."
      linked_ids: [claim-mean-systematic, deliv-ia-module]
    test-mean-ratio:
      status: passed
      summary: "w_u equals the locked omega_bar to 1e-9 (same quantity, two code paths); w_p >= w_u as Cauchy-Schwarz requires; ratio 1.354758; correction 1.163941; and the corrected width strictly exceeds the headline at every ROADMAP energy, so the systematic is verifiably one-sided. A dedicated test asserts the ratio EXCEEDS the Debye 9/8 -- i.e. the disconfirming outcome is asserted, not merely tolerated."
      linked_ids: [claim-mean-systematic, deliv-ia-module, deliv-width-derivation]
  references:
    ref-sears:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "The impulse-approximation framework (free-nucleus recoil Doppler-broadened by the initial momentum distribution) is what the derivation is built on, and it is cited at the head of section 1 of the derivation artifact and in the module docstring. Used, not merely name-dropped: the w = q^2/2m_N + q.p/m_N decomposition and the separation into mean and variance is the Sears structure."
    ref-campbell-deem:
      status: completed
      completed_actions: [use, cite]
      missing_actions: []
      summary: "Supplies the IA validity criterion q >> sqrt(2 m_N omega_bar) <=> E_R >> omega_bar <=> 2W >> 1. Applied quantitatively: 2W = 5.60 at the 100 meV floor, so the criterion is satisfied by a factor 5.6 there and the O(1/2W) ~ 18% residual is real and is handed to plan 11-03."
    ref-counting-floor:
      status: completed
      completed_actions: [read, use, compare]
      missing_actions: []
      summary: "The PIPELINE-DERIVED floors 16.009% / 14.271% at 0.49382 eV were used, not the ROADMAP comparison targets 15.9 / 14.2, because 10-05 established the pipeline values as the measured ones. Both sets are reported and both give the same in-band verdict. The best-case, no-noise-sources framing was carried through verbatim."
    ref-prior-work-widths:
      status: completed
      completed_actions: [read, compare, avoid]
      missing_actions: []
      summary: "The SC3 bands appear only in a comparison column with explicit verdicts. No width was transcribed. The artifact goes further than avoidance and states why agreement with those bands is weak evidence: they were generated from the same 12-21 meV range that the locked omega_bar sits inside."
  forbidden_proxies:
    fp-transcribe-widths:
      status: rejected
      notes: "Every width comes from ia_broadening.fractional_width applied to params.OMEGA_BAR_eV. The tests assert the derived values numerically (42.261%, 18.900%, 13.364%, 4.226%, 1.336%), so a value copied from the literature would have to match the derivation to five digits to pass -- and the bands themselves are only ever compared against, never read in."
    fp-identity-as-evidence:
      status: rejected
      notes: "sigma_E/E_R = 1/sqrt(2W) is labelled TRUE BY CONSTRUCTION in the module docstring, in section 2 of the derivation artifact, and in the CSV header. The test demonstrates it rather than asserting it, by verifying the relation at three physically absurd omega_bar values."
    fp-poisson-as-resolution:
      status: rejected
      notes: "The caveat is a module constant interpolated into quadrature_with_counting_floor's own docstring, is written into the CSV header, appears in the figure legend on both floor points, and appears repeatedly in the derivation artifact including a dedicated 'what this comparison is not' paragraph stating that quoting the 24.8%/23.7% quadrature as the resolution at 0.5 eV would be this proxy. Machine-enforced by test_counting_floor_is_labelled_best_case_everywhere_it_is_used."
    fp-electron-recoil-leak:
      status: rejected
      notes: "Section 7 of the derivation artifact records the boundary and explicitly declines to answer in EITHER direction. A test asserts that ia_broadening.py does not import or mention muon_deposit, compton_deposit or compton_source, and that it names Phase 15 and the OPEN status."
    fp-single-mode-assumption:
      status: rejected
      notes: "Tested rather than assumed, and the test came out against the comfortable answer: the real Ge ratio 1.3548 exceeds the Debye 9/8, so the single-frequency form understates sigma_E by 16.4% rather than 6.1%. Carried as a labelled one-sided column in the table and a shaded band on the figure. The headline was NOT silently switched to the arithmetic mean."
  uncertainty_markers:
    weakest_anchors:
      - "sigma_E inherits plan 11-01's omega_bar uncertainty LINEARLY under a square root: a factor-2 error in omega_bar is a factor-1.41 error in every width here, and the omega_bar lock rests on a single 1972 measurement."
      - "The Gaussian is only the leading IA result. At 2W = 5.60 in the bottom bin the O(1/2W) ~ 18% correction is comparable to the width's own precision, so the 100 meV width should not be quoted to better than one significant figure until plan 11-03 bounds it."
      - "The ROADMAP SC3 bands are DERIVED in-survey from a Debye-model omega_bar band, so the four IN BAND verdicts are weak evidence. They were essentially guaranteed once plan 11-01's omega_bar landed inside 12-21 meV."
      - "The Phase-10 counting floors are themselves a best case with five named noise sources omitted, so the quadrature sum is a LOWER bound on the combined smearing, not an estimate of it."
    unvalidated_assumptions:
      - "PROMOTED TO TESTED AND FAILED-AGAINST: the single-effective-frequency assumption. It does not hold for Ge; the residual is +16.4% one-sided and is now carried explicitly."
      - "Statistical independence of the counting floor and the IA width, which is what licenses quadrature. They arise from unrelated physics (sensor counting statistics vs nuclear zero-point motion) but independence is ASSERTED, not proven."
      - "That the Phase-10 floors, measured only at 0.49382 eV, are the right comparison at exactly 0.5 eV. The 0.6% energy difference is far below the floor's own precision, but the floors are held constant in the table rather than extrapolated, and that is stated."
    competing_explanations:
      - "All four headline widths landing inside the ROADMAP SC3 bands looks like confirmation and is not. The bands were built from omega_bar = 12-21 meV and the locked omega_bar = 17.860 meV sits inside that range, so sigma_E = sqrt(E_R omega_bar) could hardly have landed anywhere else. This is agreement by shared ancestry."
      - "The 22-26% quadrature agreement inherits the same weakness, since the ROADMAP band was formed from the same SC3 widths."
    disconfirming_observations:
      - "FIRED: omega_bar_p/omega_bar_u on the real Ge VDOS is 1.3548, well above the Debye 9/8. The plan anticipated this as a possible disconfirming outcome and it happened. Consequence: the single-frequency IA width is understated by 16.4%, and ALL FOUR moment-corrected widths land ABOVE their SC3 bands (49.19% vs 46%, 22.00% vs 20.5%, 15.56% vs 15%, 1.555% vs 1.5%). The 0.5 eV quadrature rises to 27.19%/26.20%, above the 22-26% band."
      - "RAN, DID NOT FIRE: the Debye mean-ratio oracle (1.1249999999719 against 9/8)."
      - "RAN, DID NOT FIRE: the headline width at 0.5 eV moving outside 15.5-20.5% because plan 11-01 superseded the survey band. It did not; 11-01's omega_bar landed inside the band, so the SC3 widths are unchanged in character."
      - "RAN, DID NOT FIRE: the quadrature landing outside 22-26%. The headline quadrature is in band for both designs and for both floor sets. It leaves the band only under the moment correction."
      - "NEW: the sub-bin crossing at 20.94 eV shows 'negligible above ~100 eV' is conservative by a factor ~5. At 100 eV the IA width is 1.34%, under half an extended-grid bin."
---

# Plan 11-02 — IA quantum broadening width (CALC-15)

## Widths at the five ROADMAP energies

| E_R | σ_E | **σ_E/E_R** | SC3 band | verdict | moment-corrected (×1.1639) | vs band |
|---|---|---|---|---|---|---|
| 100 meV | 42.261 meV | **42.261 %** | 35–46 % | IN | 49.189 % | **ABOVE** |
| 0.5 eV | 94.498 meV | **18.900 %** | 15.5–20.5 % | IN | 21.998 % | **ABOVE** |
| 1 eV | 133.640 meV | **13.364 %** | 11–15 % | IN | 15.555 % | **ABOVE** |
| 10 eV | 422.607 meV | **4.226 %** | — | — | 4.919 % | — |
| 100 eV | 1.33640 eV | **1.336 %** | 1.1–1.5 % | IN | 1.555 % | **ABOVE** |

Locked ω̄ = 17.859677 meV. σ_E = √(E_R ω̄), derived in-phase; nothing transcribed.

## Quadrature at the 0.5 eV trigger threshold

| Design | Phase-10 counting floor (**best case, no noise sources**) | IA width | **quadrature** | 22–26 % |
|---|---|---|---|---|
| Ta→Al | 16.009 % | 18.900 % | **24.769 %** | IN |
| Al→Hf | 14.271 % | 18.900 % | **23.682 %** | IN |

Added in quadrature, never linearly (linear would give 34.9 % / 33.2 %). **The IA width is now the
larger of the two contributions**, overtaking the Ta→Al floor at 0.70 eV and the Al→Hf floor at
0.88 eV — both below the 1 eV regime boundary. Neither number, nor the sum, is a detector
resolution.

## Sub-bin crossing — what "negligible above ~100 eV" actually means

One extended-grid bin = **2.92047 %**. σ_E/E_R falls below it at **E_R = 20.940 eV**. Above ~21 eV
the broadening cannot move counts between bins on the Phase-10 axis. The ROADMAP's "~100 eV" is
conservative by a factor of ~5.

## Moment mismatch — the disconfirming check fired

| Spectrum | ω̄_u (harmonic, ⟨u_x²⟩) | ω̄_p (arithmetic, ⟨p_x²⟩) | ⟨ω⟩⟨1/ω⟩ | σ_E correction |
|---|---|---|---|---|
| Debye (oracle) | 21.4859 meV | 24.1716 meV | 1.125000 (exact 9/8) | 1.06066 |
| **Measured Ge** | **17.85968 meV** | **24.19553 meV** | **1.354758** | **1.163941** |

σ_E is governed by ⟨p_x²⟩ and therefore by the **arithmetic** mean, while the locked ω̄ is the
**harmonic** mean. Real Ge is 20 % worse at this than a Debye spectrum, so the single-frequency form
**understates σ_E by 16.4 %**, not 6.1 %. Headline widths stay on the locked ω̄; the correction is
carried as a labelled one-sided column and a shaded band on the figure. **It is never averaged in
and the headline is never silently switched.**

**This is what 11-03 must reproduce independently** from the exact second central moment of S(q,ω).
A disagreement between the two routes **blocks 11-04**.

## Deviations

None requiring a rule. Two recorded choices:

* **Counting-floor values.** The plan named 15.9 % / 14.2 %; those are ROADMAP *comparison targets*.
  Phase 10's own pipeline-derived values are 16.009 % / 14.271 %. Evidence discipline says use the
  derived ones, so those are primary. Both are reported and both give the same verdict.
* **Floors held constant across the table** rather than extrapolated: Phase 10 evaluated them only
  at 0.49382 eV. Stated in the CSV header so no one reads the column as an energy-dependent curve.

## Suite

**546 passed, 0 failed** (534 after plan 11-01 + 12 new in `tests/test_ia_broadening.py`).
`data/flux/*.csv` churn reverted.
