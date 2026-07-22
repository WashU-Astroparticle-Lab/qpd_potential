# Stage 3 — Mathematical Soundness Review

**Manuscript:** `paper/qpd_reactor_cevns_spectra.tex` (+ `paper/sections/*.tex`)
**Manuscript sha256:** `bcc30a3d108c9703a41163f36ae4c2d71773186ebef527d3c374cc184e977a4e`
**Reviewer role:** mathematical-soundness (forward-model, no theorems)
**Overall:** Mathematically sound. 0 blockers, 0 majors, 5 minors.

## Theorem/proof audit
No formal theorems, lemmas, or proofs exist (revtex4-2, no `\newtheorem`, no proof
environments). The paper is a forward-model computation; the reviewer confirms the
"no theorems" premise directly. No proof-redteam is applicable. **checks out.**

## Equation-by-equation verification (independently recomputed)

- **Eq. 4 (flux) — checks out.** `R_f = P_th/⟨E_f⟩ = 3e9 J·s⁻¹ / (205.8 MeV) = 9.098e19`
  fissions/s, matches quoted 9.10e19. Use of the effective thermal energy per fission
  (205.8 MeV, not the total Q) is the physically correct choice (avoids double-counting
  escaping-ν energy). Integrated flux 7.5e12 cm⁻²s⁻¹ and 1.96e20 ν̄/s/GW are mutually
  self-consistent and reproduce Hayes–Vogel ~2e20. `/4π d²` point-source geometry correct.
- **Eq. 5 / A1 (Freedman dσ/dT) — checks out.** `/4π` prefactor (not `/8π`) plus explicit
  `(ħc)²=3.894e-28 GeV²cm²` are both present and load-bearing; the combination is validated
  numerically below. Dimensional bookkeeping in App. A ([G_F²ME²]=GeV⁻¹, ħc² carries GeV²cm²)
  is correct → dσ/dT in cm²/GeV. Q_W = N−(1−4sin²θ_W)Z with sin²θ_W=0.2387 gives
  1−4sin²θ_W=0.0452; Q_W(72Ge)=38.55, N²-scaling to ~0.5% confirmed.
- **A2 (closed-form total) — checks out and the error bound is exactly right.** The residual
  between the differential integral and `σ_tot=G_F²Q_W²E_ν²/4π·(ħc)²` is the dropped
  O((2E_ν/M)²) term; recomputed relative error is 3.6e-9 (2 MeV), 1.4e-8 (4 MeV), 5.7e-8
  (8 MeV) — matches the paper's stated "3e-9–6e-8" band precisely. `σ(72Ge,4MeV)` recomputed
  = 1.0026e-40 cm², i.e. 0.26% from the 1.0e-40 anchor — matches. This joint reproduction is
  the strongest internal cross-check: it simultaneously confirms the `/4π` prefactor, the
  `(ħc)²` conversion, and the Q_W convention.
- **Eq. 6 (CEvNS fold) — checks out.** `E_ν^min=√(M_iT/2)` is the correct inversion of the
  kinematic endpoint `T_max=2E_ν²/(M+2E_ν)` (App. A gives the exact `½(T+√(T²+2M_iT))` form).
  Per-isotope (not lumped-A) treatment is correct; isotope table masses `M_i=A_i·931.494 MeV`
  and endpoints (2824–3066 eV at 10 MeV) are internally consistent.
- **Eq. 7 (Billard k-factor) — checks out.** `k=(P_B/P_th)(d/d_B)²=(8.54/3)(25/400)²=0.01112`,
  `1/k=89.93` (paper 89.9). Both powers thermal → only 1/d² survives, correctly stated.
  Recomputed Billard deviations 2.37/1.76/1.15% → worst bin 2.4%, matches abstract/body.
- **Eq. 8 (Gaisser–Guan) — checks out.** Matches the Guan et al. modified-Gaisser form
  including the cosθ* effective-zenith parametrization and the two-term high-energy correction.
- **Eq. 9 (muon fold) — checks out (dimensionally).** `(1/m)∫dΩ(n̂·Ω̂)_+A∫dE_μ (dI/dE_μdΩ) f_L`
  reduces to kg⁻¹s⁻¹MeV⁻¹. Cauchy mean chord `⟨ℓ⟩=4V/S`: recomputed V=20.65 cm³, S=214.6 cm²
  → 0.3848 cm (paper 0.385); space diagonal 14.370 cm — both match. See Minor 1 (Landau vs
  Vavilov) and Minor 5 (197 MeV cap).
- **Eq. 10 (Landau MPV) — checks out.** `ξ=(K/2)(Z/A)(x/β²)`, `Δ_p=ξ[ln(2m_ec²β²γ²/I)+ln(ξ/I)
  +j−β²−δ]` is the PDG most-probable-value form with j=0.200. Recomputed ξ(MIP,x=1.065 g/cm²)
  =0.0720 MeV — matches PDG value quoted. Ordering Δ_p=1.23 < ⟨Δ⟩=1.46 MeV is the correct
  Landau-skew signature; Z/A=0.4406, K=0.307, I≈350 eV all correct for Ge.
- **Eq. 11/12 (Klein–Nishina + incoherent) — checks out.** Standard KN differential ×S(x,Z);
  momentum-transfer x=E[keV]sin(θ/2)/12.39842 Å⁻¹ uses hc=12.398 keV·Å correctly; S(x→0)→0
  (binding suppression) and S(x→∞)→Z limits correctly stated.
- **Eq. 13 (Compton edge) — checks out.** Recomputed edges 1243.5/1540.8/2381.2 keV for
  40K(1461)/214Bi(1764)/208Tl(2614) → matches 1243/1541/2382 to <0.5 keV as claimed.
- **Eq. 14 (sensor sharing) — checks out; energy-conserving.** Total energy over all sensors
  = f_prompt·E_dep (prompt over spot) + (1−f_prompt)·E_dep (diffuse over N_sens) = E_dep. The
  on-spot sensors correctly receive prompt+diffuse. Units of energy on both sides.
- **Eq. 15 (count-integral estimator) — checks out.** E_rec=C·N_obs, N_obs,i=∫m(Γ_in(t))dt is
  dimensionally consistent (m a rate, ∫dt a count, C in eV/event). Single global C fixed on an
  unsaturated deposit is an honest calibration, correctly labelled a consistency check (not an
  independent validation); the predictive content is the saturated regime — correctly framed.
- **Eq. 16 (crossover) / B3 (onset band) — checks out.** Inversion of Eq. 14 recomputed:
  default crossover 53.0/32.2 eV (paper 52.9/32.1; residual is N_sens 10300 vs 10287),
  equal-split E_onset·N_sens = 13.1/7.9 keV, plateau E_onset·N_sens/(1−f_prompt) = 18.7/11.3
  keV — all match. Scan extremes recomputed: 8.0 eV (f=0.5,r=1) to 933 eV (f=0.1,r=5) — matches
  "~8 eV to ~0.93 keV". See Minor 4 (wording conflation in response.tex).
- **Eq. 17 (response matrix) — checks out.** Normalized conditional dP/dE_rec, ∫R dE_rec=1.
- **Eq. 18 (fold) — checks out.** Because Σ_j R_ji=1, Σ_j(dR/dE_rec|_j ΔE_rec,j)=Σ_i N_dep,i,
  so counts are conserved by construction; the numerical ~1e-16 residual is machine precision
  and therefore fully coherent with the stated equation.
- **B1 (event count n_ev) — checks out.** n_ev=∫Γ_in dt=Kτ_qp N_qp/V_tr follows from unit-area
  g(t); prefactor Kτ_qp/V_tr is dimensionless (Hz·μm³·s/μm³) and ~0.03(Al)/~0.008(Hf) implies
  τ_qp~1 ms / 0.4 ms — physically plausible. Distinction from N_qp correctly enforced.
- **B2 (MC convergence) — checks out.** ε=1/√(N_s R_jk); ε≲1.8% at N_s=5000 ⇒ peak cell holds
  ~62% of column probability, consistent with a near-delta saturated column.

## Approximation-validity assessment

- **Log-log power-law rebinning (counts to 9.6e-5).** Plausible: power-law interpolation of a
  smooth, monotone spectrum leaves only curvature residual; the coarser "0.12% above 50 eV" is
  the well-populated-region figure. Not independently reproducible from the manuscript alone but
  internally consistent. **acceptable, minor caveat.**
- **Delta-like deep-saturation column.** Justified: saturated columns pile at the plateau with
  relative spread ~1e-3, so the Poisson-about-analytic-mean branch (used when n_ev>2000 makes
  the O(1e8)-event train infeasible) is immaterial to R, and the mean is pinned to the validated
  estimator in both branches → no kink at the split. **sound and honestly disclosed.**
- **Sub-1.8 MeV flux placeholder (C¹ seam-match).** Continuous-through-derivative matching is a
  reasonable interpolation; it is explicitly carried as a wide uncertainty band (6–10% below 95
  eV_nr). **sound; see Minor 3 on the integrated ν/fission consequence.**

## Cross-check coherence
All four quoted cross-checks are internally coherent with the stated equations and reproduce on
independent recomputation: Billard 2.4% (worst bin 2.37%), closed-form ≤6e-8 (5.7e-8 at 8 MeV),
σ(72Ge,4MeV) 0.26%, counts-conservation 1e-16 (machine precision of a column-normalized fold).
Implementation (`src/qpd_potential/cevns.py`, `muon_deposit.py`) matches manuscript conventions
(explicit `/4π`, `(ħc)²=3.894e-28`, sin²θ_W=0.2387, K=0.307075, Z/A=0.4406).

## Findings (severity-tagged)

- **[minor] Eq. 9 / backgrounds.tex — Landau vs Vavilov regime.** The density is called
  "Landau–Vavilov," but for the long near-horizontal chords (thick absorber, large κ=ξ/T_max)
  the true distribution is Vavilov/Gaussian, not pure Landau; pure Landau would overestimate the
  extreme high-deposit tail. **Failure mode is immaterial to the conclusions** because every muon
  deposit saturates the readout and piles at the plateau regardless of tail shape. Worth a
  one-line clarification of which form is used per chord.
- **[minor] backgrounds.tex vs abstract — muon-rate tolerance wording.** Abstract says the muon
  rate matches PDG "within ~30%"; backgrounds.tex says "~20% ... within the VALD-02 tolerance of
  30%." Not a math error (20% ⊂ 30%), but the two numbers should be reconciled.
- **[minor] Eq. 4 / cevns.tex — integrated ν̄/fission ≈ 6.5.** The self-consistent chain
  (7.5e12 cm⁻²s⁻¹ ⇒ 5.9e20 ν/s ⇒ 6.47 ν/fission) is slightly above the canonical ~6.0–6.14; the
  excess is the direct consequence of the sub-1.8 MeV placeholder + n-capture addition. It is
  honestly flagged as a placeholder and does not affect the anchored >1.8 MeV rate, but the
  ν/fission value could be stated so the reader can see it is a modeling consequence, not data.
- **[minor] response.tex — crossover-band sentence conflates two definitions.** "ranges up to
  ~13 keV and ~7.9 keV in the equal-split limit, with a whole-array plateau at ~18.6 keV" mixes
  the r-scan maximum (~0.93 keV) with the f_prompt→0 equal-split (~13 keV, outside the [0.1,0.5]
  scan). Numbers are individually correct (appendix B3 is clear); the body sentence reads as if
  one continuous scan. Presentation clarity only.
- **[minor] backgrounds.tex — 197 MeV muon endpoint = grid maximum.** The "~197 MeV" maximum
  deposit coincides with the response-grid ceiling; the Landau tail formally extends higher, so
  197 MeV is a chosen cap rather than a kinematic endpoint. Immaterial (all such deposits
  saturate) but should be stated as a cap.

## Weakest step
The weakest *mathematical* link is the saturated-regime response shape between the two validated
limits (Eqs. 15–17): it has no literature anchor and rides on the low-confidence sharing
parameters f_prompt and r, which the crossover (Eq. 16) spreads over ~3 orders of magnitude. The
authors are commendably explicit that this is "the model says," not "the detector measures," and
the limiting cases (E_rec=0.5E_dep unsaturated; plateau above 25 kHz, with censoring-off returning
exactly 0.5E_dep) are correctly demonstrated — so this is a scoping/interpretation caveat, not an
algebraic defect. Mathematically the manuscript is exceptionally clean.

**Recommendation ceiling (math axis only):** minor_revision.
