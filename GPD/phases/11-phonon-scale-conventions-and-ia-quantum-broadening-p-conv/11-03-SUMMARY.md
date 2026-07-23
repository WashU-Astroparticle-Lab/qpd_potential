---
phase: 11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv
plan: 03
status: complete
one_liner: "The harmonic incoherent S(q,w) was computed from the frozen Ge VDOS at five recoil energies and all three exact checks pass at every q (zeroth moment to 2e-7, f-sum rule to 2e-8, gamma(0) = q^2<u_x^2> to 7e-12); the closed-form cumulant kappa_n = E_R <w^(n-1)> makes the second central moment EXACTLY E_R times the ARITHMETIC VDOS mean, independently confirming plan 11-02's 1.1639 systematic from a completely different direction, so 11-04 is NOT blocked; the bottom bin is NOT a delta -- fractional width 49.19%, skewness 0.590 (= 1.3972/sqrt(2W) exactly), excess kurtosis 0.381 -- so 'the IA is reached by 100 meV' is supported only at the ORDER-OF-MAGNITUDE level; e^(-2W) = 3.70e-3 at 100 meV is the ZERO-PHONON weight alone and the inelastic continuum carries 100% of the f-sum rule, so multiplying the rate by it would discard 99.63% of the strength at 100 meV and 1 - 5e-25 of it at 1 eV; and the matched Gaussian puts 0.90% of its weight at unphysical w < 0 and 48.6-49.9% below the extended-grid floor, which is the leakage plan 11-04 must report rather than renormalize away."
plan_contract_ref: GPD/phases/11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv/11-03-PLAN.md#/contract

contract_results:
  claims:
    claim-sum-rules:
      status: passed
      summary: "Harmonic incoherent S(q,w) built by the T->0 cumulant route, gamma(t) = E_R int g(w)/w e^{-iwt} dw (every constant cancels: hbar^2 q^2/2m_N = E_R exactly once q^2 = 2 m_N E_R, so the harmonic S is fixed by E_R and the VDOS alone). All three exact checks pass at all five q: zeroth moment |m0-1| from 2.1e-7 (100 meV) to 3.4e-13 (100 eV), tolerance 1e-6; f-sum rule |m1/E_R - 1| from 1.9e-8 to 3.0e-13, tolerance 1e-4; gamma(0) reproduces 2W = q^2<u_x^2> from CONVENTIONS.md Section J to 7.3e-12 at every q, tying the S(q,w) quadrature back to the lock. Convergence onto delta(w - E_R) is demonstrated: the exact fractional width sqrt(<w>/E_R) falls as 1/sqrt(E_R) exactly (consecutive-decade ratios equal sqrt(10) to 1e-12), 49.19% -> 22.00% -> 15.55% -> 4.92% -> 1.56%."
      linked_ids: [deliv-impulse-module, deliv-moments-table, test-zeroth-moment, test-f-sum-rule, test-2W-reduction, test-delta-convergence, ref-sears, ref-computational-impulse]
      evidence:
        - verifier: gpd-executor
          method: "closed-form cumulants kappa_n = E_R <w^(n-1)> cross-checked against a numerical FFT with a convergence ladder, plus three exact sum rules"
          confidence: high
          claim_id: claim-sum-rules
          deliverable_id: deliv-impulse-module
          acceptance_test_id: test-f-sum-rule
          reference_id: ref-sears
          forbidden_proxy_id: fp-ia-overclaim
          evidence_path: GPD/phases/11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv/11-03-IMPULSE-LIMIT-JUSTIFICATION.md
    claim-residual-correction:
      status: passed
      summary: "The exact cumulants are kappa_n = E_R <w^(n-1)> for every n >= 1, so kappa_2 = E_R <w> = E_R * omega_bar_p -- the ARITHMETIC VDOS mean -- confirmed numerically to 5.1e-7 relative at 100 meV and 4.8e-10 at 100 eV, and demonstrably NOT E_R * omega_bar_u, which is 35.5% smaller. Skewness = 1.39718/sqrt(2W) EXACTLY, with the constant verified to 4 decimals at all five energies: 0.590461 / 0.264062 / 0.186720 / 0.059046 / 0.018672. Bottom-bin residual: skewness 0.590, excess kurtosis 0.381, 1/2W = 0.179. The matched symmetric Gaussian puts 0.898% of its weight at w < 0 where the true T->0 S vanishes identically (2.103% if matched to the true wider width), and 49.94% below the extended-grid floor when centred at 100 meV, 48.64% when centred at the first bin centre 0.1013838 eV."
      linked_ids: [deliv-moments-table, deliv-justification, test-second-moment, test-skewness, test-negative-energy-weight, ref-sears]
      evidence:
        - verifier: gpd-executor
          method: "exact cumulant expansion of the harmonic correlation function, cross-checked numerically, and compared against plan 11-02's independent momentum-distribution route"
          confidence: high
          claim_id: claim-residual-correction
          deliverable_id: deliv-moments-table
          acceptance_test_id: test-second-moment
          reference_id: ref-sears
          forbidden_proxy_id: fp-ia-overclaim
          evidence_path: tests/test_impulse_limit.py
    claim-no-dw-suppression:
      status: passed
      summary: "lim_{t->inf} F(q,t) = e^(-2W) by Riemann-Lebesgue, so e^(-2W) is the ZERO-PHONON weight and nothing else. Strength partition at 100 meV, computed not asserted: zero-phonon 0.370%, one-phonon 2W e^(-2W) = 2.072%, multiphonon 97.558%, elastic + inelastic = 1.000000 to 2e-6. The elastic delta sits at w = 0 and contributes EXACTLY ZERO to the first moment, so the inelastic continuum alone carries the entire f-sum rule -- verified to 1e-8 or better at every q. Multiplying the rate by e^(-2W) would therefore discard 99.63% of the strength at 100 meV and a factor 4.82e-25 of it at 1 eV: erasing a real signal, not correcting one. A machine test asserts that no module in this phase applies e^(-2W) as a multiplicative rate factor."
      linked_ids: [deliv-justification, deliv-moments-table, test-elastic-weight, test-strength-partition, ref-pitfalls-dw, ref-computational-impulse]
  deliverables:
    deliv-impulse-module:
      status: passed
      path: src/qpd_potential/impulse_limit.py
      summary: "vdos_raw_moments, exact cumulants and analytic_moments (mean, variance, skewness, excess kurtosis in closed form), two_W and elastic_weight, structure_factor (ONE FFT per q with the zero-phonon and one-phonon terms subtracted analytically and the one-phonon term added back on the w grid), numeric_moments, converged_numeric_moments with a 60/240/960/3840 points-per-sigma ladder gated on the zeroth moment, and gaussian_offgrid_weights. Reads the frozen VDOS and the params.py lock; hard-codes nothing."
      linked_ids: [claim-sum-rules, claim-residual-correction]
    deliv-moments-table:
      status: passed
      path: GPD/phases/11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv/11-03-IMPULSE-LIMIT-JUSTIFICATION.md#moments
      summary: "Five rows as a markdown section inside the justification artifact, exactly as the plan required -- NO tracked CSV was added under artifacts/v2.0/, so the Phase-10 disposition register is untouched by this plan. Columns: q in both units, 2W, e^(-2W), m0-1, m1/E_R-1, kappa_2/(E_R<w>)-1, numerical and exact skewness, 1/sqrt(2W), skew*sqrt(2W), excess kurtosis, exact fractional width, and the points-per-sigma actually needed. Plus a three-row matched-Gaussian off-grid weight table."
      linked_ids: [claim-sum-rules, claim-residual-correction, claim-no-dw-suppression]
    deliv-justification:
      status: passed
      path: GPD/phases/11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv/11-03-IMPULSE-LIMIT-JUSTIFICATION.md
      summary: "Headed explicitly as BOUNDED and NOT A MILESTONE PILLAR. Seven sections: the method and the exact cumulants; the moments table; the sum rules with the honest order-of-magnitude convergence verdict; the O(1/2W) residual with the numbers that must travel to Phases 12-16; the e^(-2W) prohibition argued with the computed strength partition, including a subsection recording a real 5-order-of-magnitude disagreement with the survey magnitude at 1 eV and explaining it; a five-item 'what this artifact does NOT establish'; and the cross-check verdict for plans 11-02 and 11-04."
      linked_ids: [claim-sum-rules, claim-residual-correction, claim-no-dw-suppression]
  acceptance_tests:
    test-zeroth-moment:
      status: passed
      summary: "|m0 - 1| = 2.1e-7 at 100 meV (needing the 3840 points/sigma rung) and 1.7e-12 or better at the four upper energies (first rung). Tolerance 1e-6, met at all five q."
      linked_ids: [claim-sum-rules, deliv-impulse-module, deliv-moments-table]
    test-f-sum-rule:
      status: passed
      summary: "|m1/E_R - 1| from 1.9e-8 (100 meV) to 3.0e-13 (100 eV), tolerance 1e-4. The test also verifies that q^2/(2 m_N) really equals E_R in the units used, to 1e-14, so the sum rule is not being checked against a circular definition."
      linked_ids: [claim-sum-rules, deliv-impulse-module, deliv-moments-table]
    test-2W-reduction:
      status: passed
      summary: "gamma(0) = E_R <1/w> agrees with q^2<u_x^2> from CONVENTIONS.md Section J to 7.3e-12 at every q, and with E_R/omega_bar to the same precision. Two independent quadratures over the same frozen VDOS."
      linked_ids: [claim-sum-rules, deliv-impulse-module]
    test-delta-convergence:
      status: passed
      summary: "Width falls monotonically and the consecutive-decade ratio equals sqrt(10) to 1e-12, i.e. exact 1/sqrt(E_R) scaling. The test ASSERTS the bottom-bin width exceeds 40%, so it fails if a future change makes the bottom bin look narrow enough to justify calling the limit reached. Verdict recorded as ORDER-OF-MAGNITUDE, not ~20%."
      linked_ids: [claim-sum-rules, deliv-moments-table]
    test-second-moment:
      status: passed
      summary: "THE DECISIVE CROSS-CHECK. Numerical second central moment matches E_R * omega_bar_p to 5.1e-7 (100 meV) through 4.8e-10 (100 eV); the closed form matches to 1e-12. The test additionally asserts it is NOT within 5% of E_R * omega_bar_u, so agreeing with the wrong mean would fail. Plan 11-02's systematic is CONFIRMED and plan 11-04 is NOT blocked."
      linked_ids: [claim-residual-correction, deliv-impulse-module, deliv-moments-table]
    test-skewness:
      status: passed
      summary: "skew * sqrt(2W) = 1.39718 to 1e-4 at all five energies -- exact 1/sqrt(2W) scaling with a VDOS-fixed constant, better than the 'within a factor of a few' the plan asked for. Numerical skewness matches the closed form to 2e-3 relative at every q, including the bottom bin (0.590457 vs 0.590461)."
      linked_ids: [claim-residual-correction, deliv-moments-table]
    test-negative-energy-weight:
      status: passed
      summary: "Matched Gaussian at 100 meV: 0.8984% of the weight at w < 0 (unphysical -- the T->0 S vanishes there, no phonons to absorb) and 49.9386% below the 0.0999350 eV grid floor; at the first bin centre 0.1013838 eV, 0.8596% and 48.6420%. With the TRUE arithmetic-mean width the negative-energy tail more than doubles to 2.1027%. The test asserts the sub-floor weight EXCEEDS 40%, with the reason stated: a clean sub-1e-3 conservation residual in plan 11-04 would be evidence of hidden renormalization."
      linked_ids: [claim-residual-correction, deliv-impulse-module, deliv-justification]
    test-elastic-weight:
      status: partial
      summary: "PARTIAL, and deliberately so. e^(-2W) computed from the frozen VDOS: 3.7008e-3 at 100 meV, 6.94e-13 at 0.5 eV, 4.819e-25 at 1 eV, 6.75e-244 at 10 eV, underflow (~1e-2432) at 100 eV. The 100 meV value agrees with the survey magnitude ~1e-2 within a factor 2.7 -- PASS. The 1 eV value does NOT agree with the survey ~1e-20; it is 5 orders of magnitude smaller -- FAIL on the literal criterion. The cause is identified and TESTED: e^(-2W) is exponentially sensitive to omega_bar, the survey used the Debye value ~21.5 meV (2W = 46.5, exp(-46.5) = 6.4e-21 ~ 1e-20, reproduced by an assertion), and the locked measured 17.86 meV gives 2W = 55.99. 'Within an order of magnitude' was never well posed for an exponentially sensitive quantity at 2W = 56. No conclusion changes: the coherent channel is extinct either way. Recorded as a miss rather than absorbed by widening the tolerance."
      linked_ids: [claim-no-dw-suppression, deliv-moments-table]
    test-strength-partition:
      status: passed
      summary: "Elastic + inelastic = 1 to 2e-6 at 0.1, 0.5 and 1 eV; the first moment equals E_R to 1e-4 with the elastic line contributing exactly nothing, so the inelastic continuum alone carries the whole f-sum rule. The discarded fraction 1 - e^(-2W) exceeds 99% at every energy tested. A separate machine test greps the three phase modules for patterns that would apply exp(-2W) as a rate factor and asserts none appear."
      linked_ids: [claim-no-dw-suppression, deliv-justification, deliv-moments-table]
  references:
    ref-sears:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "The IA / final-state framework is what sets the expectation that the leading correction is O(1/2W) and that the true lineshape is asymmetric at low 2W. Both were confirmed quantitatively: the skewness is exactly proportional to 1/sqrt(2W) and is 0.590 in the bottom bin. Cited in the module docstring and section 1 of the artifact."
    ref-computational-impulse:
      status: completed
      completed_actions: [read, compare]
      missing_actions: []
      summary: "Supplied the e^(-2W) magnitudes to reproduce and the ~21 meV coherent-regime boundary. Compared explicitly: agreement within a factor 2.7 at 100 meV, a REPORTED 5-decade disagreement at 1 eV traced to the survey's Debye omega_bar. The ~21 meV coherent boundary is consistent with the locked numbers: 2W = 1 at E_R = omega_bar = 17.86 meV, below the 100 meV grid floor."
    ref-pitfalls-dw:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "The failure mode it names is closed numerically in section 4 of the artifact: e^(-2W) is the zero-phonon weight, the strength moves into the multiphonon continuum, and that continuum carries 100% of the f-sum rule. The milestone-wide prohibition is enforced by a machine test over three modules."
    ref-supercdms:
      status: completed
      completed_actions: [cite]
      missing_actions: []
      summary: "Cited via CONVENTIONS.md Section J's new Cross-Convention Consistency Check row (added by plan 11-01), which records that the 19.7 eV displacement threshold with no defect production below ~6 eV means no defect-storage channel opens in the 0.1-6 eV band, so E_ph = E_dep holds across the region where the IA broadening matters."
  forbidden_proxies:
    fp-dw-rate-suppression:
      status: rejected
      notes: "Nothing in this plan multiplies any rate by anything. A machine test greps impulse_limit.py, ia_broadening.py and phonon_scale.py for six patterns that would apply exp(-2W) as a multiplicative rate factor and asserts none appear. The artifact argues the prohibition with the computed strength partition rather than by assertion."
    fp-coherent-backbone:
      status: rejected
      notes: "Incoherent (self) response only, by the cumulant route. A test asserts the module contains no 'Bragg', 'coherent_structure' or 'phonon_order' identifiers. No phonon-order expansion was used; the one-phonon term appears only as an analytic SUBTRACTION to control FFT truncation ringing, not as a series being summed."
    fp-scope-creep:
      status: rejected
      notes: "Exactly five recoil energies, asserted by a test, and exactly one np.fft call, asserted by a test that ignores comments. The n_fft_max cap RAISES with an explicit instruction to take the analytic-moment fallback rather than raising the cap. The analytic cumulants exist as closed forms, so the fallback was available throughout and no temptation to expand arose."
    fp-ia-overclaim:
      status: rejected
      notes: "The verdict is recorded as ORDER-OF-MAGNITUDE, not ~20%. The artifact lists what the bottom bin actually looks like -- 49.19% width, skewness 0.590, excess kurtosis 0.381, 1/2W = 0.179 -- and states that a distribution half as wide as its own mean with an O(1) skewness is not a delta function. A test asserts the bottom-bin width exceeds 40%, so the guard fails if the claim is ever quietly strengthened."
  uncertainty_markers:
    weakest_anchors:
      - "The incoherent-only treatment is SELF-justified: it is licensed by e^(-2W) being tiny, but that smallness is computed here from the same harmonic model. Internally consistent, not externally validated."
      - "The harmonic approximation is inherited unchanged from the CONVENTIONS.md Section J lock and is not tested anywhere in this phase."
      - "There is no published Ge S(q,w) at q = 59-1865 inverse angstrom to benchmark against. The only external checks are the sum rules, which are exact but weak: they constrain moments, not shape."
      - "The frozen VDOS's own low-energy parabolic segment feeds <1/w> and therefore 2W directly; a 1.2% shift there moves e^(-2W) at 1 eV by ~2 orders of magnitude, which is why the survey comparison at 1 eV is not a meaningful test of anything."
    unvalidated_assumptions:
      - "RESOLVED, not carried: the plan flagged that the T->0 cumulant route might be numerically unstable at large 2W. It is not -- the 100 eV case (2W = 5599) is the CLEANEST of the five, because the elastic and one-phonon terms underflow to zero exactly and the remainder is a well-localized Gaussian-like kernel. The genuinely hard case was the BOTTOM bin, where gamma decays only as a power law; that was fixed by subtracting the one-phonon term analytically, not by expanding scope."
      - "That the numerical FFT and the closed-form cumulants are genuinely independent. They share the same VDOS quadrature and the same normalization, so a VDOS-level error would move both together. What they independently check is the transform and the moment algebra, not the input spectrum."
    competing_explanations:
      - "Sum-rule satisfaction is necessary but far from sufficient: a wrong lineshape with the correct first four moments would pass every quantitative check here. The skewness and negative-energy-weight diagnostics exist because the sum rules cannot detect that, and the artifact says so explicitly in its 'what this does not establish' section."
      - "The exact agreement between this plan's second moment and plan 11-02's could be read as two independent confirmations. It is weaker than that: both compute the same VDOS arithmetic mean from the same frozen table. What is genuinely independent is the ROUTE -- momentum distribution versus correlation-function cumulants -- not the input."
    disconfirming_observations:
      - "RAN, DID NOT FIRE: the second central moment matching E_R * omega_bar_u instead of E_R * omega_bar_p, which would have invalidated plan 11-02 and blocked plan 11-04. It matched omega_bar_p to 5e-7, and is 35.5% away from omega_bar_u."
      - "RAN, DID NOT FIRE: the f-sum rule failing at any q (1.9e-8 worst case)."
      - "RAN, DID NOT FIRE: gamma(0) disagreeing with q^2<u_x^2> (7.3e-12 at every q)."
      - "FIRED, AND WAS FIXED RATHER THAN ACCEPTED: the first FFT implementation put the peak at n*dw - E_R because np.fft.fft carries the minus sign, and the moments looked internally self-consistent while being wrong. The mean was 480 eV for a 0.5 eV recoil. Caught by the f-sum rule, which is exactly what it is for."
      - "FIRED: the bottom-bin skewness did not converge under the original scheme, oscillating between -2.8 and +0.7 with grid parameters, because truncation ringing dominated the third moment. Fixed by subtracting the one-phonon term analytically (still one FFT); it now converges to 0.590457 against the exact 0.590461."
      - "PARTIALLY FIRED, REPORTED NOT SMOOTHED: e^(-2W) at 1 eV is 4.82e-25 against the survey's ~1e-20, a 5-decade miss on the literal acceptance criterion. Traced to the survey's use of the Debye omega_bar; no conclusion changes."
      - "NOT FIRED but WORTH THE WEIGHT IT CARRIES: the bottom-bin skewness 0.590 and the 48.6-49.9% sub-floor Gaussian weight both say the 100 meV point is the least reliable in the milestone. Both are handed to plan 11-04 as binding constraints."
---

# Plan 11-03 — Bounded impulse-limit justification (ROADMAP SC5)

## Moments across the window

| E_R | 2W | e^(−2W) | zeroth moment | f-sum rule | κ₂/(E_R⟨ω⟩) | skewness | 1/√(2W) | excess kurtosis | exact σ/E_R |
|---|---|---|---|---|---|---|---|---|---|
| **0.1 eV** | **5.599205** | **3.7008×10⁻³** | 1 + 2.1e−7 | 1 + 1.9e−8 | 1 + 5.1e−7 | **0.590461** | 0.422607 | **0.381132** | **49.189 %** |
| 0.5 eV | 27.996027 | 6.9419×10⁻¹³ | 1 − 1.7e−12 | 1 − 8.7e−13 | 1 − 4.9e−11 | 0.264062 | 0.188996 | 0.076226 | 21.998 % |
| 1 eV | 55.992054 | 4.8190×10⁻²⁵ | 1 − 9.9e−15 | 1 + 2.0e−15 | 1 + 1.3e−12 | 0.186720 | 0.133640 | 0.038113 | 15.555 % |
| 10 eV | 559.920539 | 6.75×10⁻²⁴⁴ | 1 − 4.7e−14 | 1 − 2.4e−15 | 1 + 4.3e−11 | 0.059046 | 0.042261 | 0.003811 | 4.919 % |
| 100 eV | 5599.205393 | 0 (≈10⁻²⁴³²) | 1 − 3.4e−13 | 1 − 3.0e−13 | 1 − 4.8e−10 | 0.018672 | 0.013364 | 0.000381 | 1.556 % |

All three exact checks pass at every q. `skew·√(2W) = 1.39718` at every energy — the skewness scales
as `1/√(2W)` exactly, with a VDOS-fixed constant.

## The decisive cross-check on plan 11-02: PASSED

The exact cumulants of the harmonic S are **κ_n = E_R·⟨ω^(n−1)⟩**, so

    κ₂ = E_R·⟨ω⟩ = E_R·ω̄_p        ← the ARITHMETIC VDOS mean

reproduced numerically to 5.1×10⁻⁷ at 100 meV, and **35.5 % away from `E_R·ω̄_u`**. Plan 11-02 got
the same answer from the impulse-approximation momentum distribution; this plan got it from the
correlation function. Both give width 49.189 meV at 100 meV and correction ×1.163941.
**Plan 11-04 is NOT blocked.**

## Is the IA reached by 100 meV? — order-of-magnitude only

Convergence onto `δ(ω − q²/2M)` is demonstrated (width ∝ 1/√E_R exactly). But at the bottom bin the
harmonic S has width **49.2 % of its own mean**, skewness **0.590**, excess kurtosis **0.381**, and
`1/2W = 0.179`. That is not a delta function. **Verdict: the IA claim at 100 meV is supported at the
order-of-magnitude level, not at the ~20 % level.** The bottom bin remains the least reliable point
in the milestone, and `skewness = 0.590` is the O(1/2W) caveat that must travel with every 100 meV
number in Phases 12–16.

## Why the rate is never multiplied by e^(−2W)

At 100 meV the strength partitions as **0.370 % zero-phonon / 2.072 % one-phonon / 97.558 %
multiphonon**, summing to 1.000000 (2×10⁻⁶). The elastic delta sits at ω = 0 and contributes exactly
nothing to the first moment, so **the inelastic continuum alone carries the entire f-sum rule**.
Multiplying the rate by `e^(−2W)` would discard **99.63 % of the strength at 100 meV** and a factor
**4.82×10⁻²⁵** of it at 1 eV.

**Reported miss:** `e^(−2W)` at 1 eV is 4.82×10⁻²⁵ against the survey's ~10⁻²⁰ — 5 decades low. The
cause is exponential sensitivity to ω̄: the survey used the Debye 21.5 meV (`exp(−1/0.0215) =
6.4×10⁻²¹`, reproduced by a test), the lock uses the measured 17.86 meV. Recorded rather than
absorbed by widening the tolerance. No conclusion changes.

## Handed to plan 11-04 as binding constraints

| Quantity | Value |
|---|---|
| Gaussian weight at ω < 0, centred 100 meV (locked ω̄) | **0.898 %** — unphysical by construction |
| Same, with the true arithmetic-mean width | **2.103 %** |
| Gaussian weight below the 0.0999350 eV floor, centred 0.1 eV | **49.939 %** |
| Same, centred at the first bin centre 0.1013838 eV | **48.642 %** |

**A clean ≤10⁻³ count-conservation residual on the retained grid would be evidence of hidden
renormalization, not of a correct convolution.** Roughly half a bottom-bin kernel falls off the
retained axis. Leakage must be non-zero, reported per bin, and never rescaled away.

## Deviations

* **[Rule 1 — code fix]** The first FFT implementation used `np.fft.fft`, which carries the minus
  sign, placing the peak at `n·dω − E_R` rather than at `E_R`. The zeroth moment and the second
  *central* moment both looked correct; only the f-sum rule caught it (mean = 480 eV for a 0.5 eV
  recoil). Fixed by `np.fft.ifft` and by keeping only the positive-frequency half.
* **[Rule 2 — numerical]** The bottom-bin skewness did not converge (oscillating −2.8 to +0.7 with
  grid parameters) because the third moment was dominated by truncation ringing: `F(t)` decays only
  as a power law once the zero-phonon part is removed. Fixed by additionally subtracting the
  one-phonon term analytically — it transforms exactly to `e^(−2W)E_R g(ω)/ω`, which has compact
  support — and adding it back on the ω grid. Still one FFT per q. This was a real fix, not a
  tolerance relaxation.
* **[Rule 4 — missing component]** Registered the resulting `np.interp` add-back in the Phase-10
  interpolator inventory and bumped the closure count 34 → 35. Its `left=0.0, right=0.0` is set
  explicitly rather than relying on `np.interp`'s clamp, which would have smeared the 37.79 meV edge
  value across the whole multi-eV FFT grid and destroyed the sum rules.
* No tracked `.csv`/`.npz` was added under `artifacts/v2.0/`, per the plan.

## Suite

**581 passed, 0 failed** (546 after plan 11-02 + 35 new in `tests/test_impulse_limit.py`).
`data/flux/*.csv` churn reverted.
