# Stage-1 Reader Review — Claim Index and Overclaim Flags

Manuscript: `paper/qpd_reactor_cevns_spectra.tex` (+ 10 `\input` sections).
Title: *Reconstructed-energy background spectra for a Quantum-Parity-Detector germanium wafer: reactor CEvNS, cosmic muons, and environmental gammas.*

Reader-stage scope: claim extraction, narrative diagnosis, early overclaim/consistency detection. Not a final referee verdict. No literature search performed; project STATE/ROADMAP/phase summaries were NOT used as ground truth.

**Main claim (one sentence).** An end-to-end forward model folds published-anchored deposited-energy spectra of reactor CEvNS, cosmic muons, and environmental-gamma Compton scattering — all on a single unquenched phonon scale — through a Monte-Carlo, bandwidth-limited (25 kHz, non-paralyzable) QPD response matrix, and finds that the reactor-CEvNS signal reconstructs linearly to tens of eV while cosmic muons saturate into a tens-of-keV pile-up that is an instrumental artifact rather than a physical line.

---

## Claim index

Type legend: METH = methodological, NUM = numerical-result, PHYS = physical-interpretation, NOV = novelty, BENCH = benchmark/anchor, SCOPE = scope statement.

| ID | Type | One-line statement | Where |
|----|------|--------------------|-------|
| C1 | METH | All channels placed on a single unified phonon energy scale with NO ionization quenching (fieldless calorimeter); Lindhard/quenching would be "physically incorrect for this sensor." | model §, intro |
| C2 | METH | Deposit→signal chain: N_qp = εE_s/Δ_tr, Γ_in = K n_qp, peak rate Γ_in^pk = pΓ_in. | model Eq.(1) |
| C3 | METH | Readout saturates when Γ_in^pk > Γ_max = 1/τ_d = 25 kHz (τ_d = 40 µs); **non-paralyzable** censoring adopted as canonical, paralyzable retained only as sensitivity. | model Eqs.(2)-(3) |
| C4 | METH | Efficiency ε≈0.5 imposed as a *definitional* forward-model baseline (E_rec≈0.5 E_dep in linear regime), carried with ±10–20% band; distinct from the physical estimate η_ce≈0.3. | model § |
| C5 | METH | Localized-plus-diffuse sensor-sharing partition with exposed parameters f_prompt (0.3; 0.1–0.5) and r (2; 1–5), no thin-wafer QPD measurement. | response Eq.(6) |
| C6 | METH | Count-integral estimator E_rec = C·N_obs with a single global constant C per design, calibrated once on a deeply unsaturated deposit to slope 0.5; low-energy recovery is a *calibration-consistency check, not an independent validation*. | response Eq.(8), appendix-response |
| C7 | METH | EMG two-exponential tunneling-burst template fed with the expected event count n_ev (= Kτ_qp N_qp/V_tr), NOT the trapped population N_qp (differ by ~0.03 Al, ~0.008 Hf). | response, appendix-response Eq.(A5) |
| C8 | METH | Monte-Carlo response matrix R(E_rec|E_dep): 5000 realizations over 584 log-spaced deposits (10.14 eV–197 MeV), columns normalized to 1e-12, peak-cell MC error ≲1.8%. | response Eq.(9), appendix-response |
| C9 | NOV | The decisive observable for a bandwidth-limited detector is the *reconstructed* energy, not deposited energy; the bandwidth-limited reconstruction chain is "the methodological core of the work." | intro, response |
| C10 | BENCH | Deposited CEvNS reproduces the Billard et al. (2017) Ge benchmark (0.76/0.51/0.26 → 0.742/0.501/0.257 cts/kg/day above 50/100/200 eV_nr) to within 2.4% after a geometry-power rescale k=0.01112. | cevns § |
| C11 | BENCH | Freedman cross section: σ(72Ge,4 MeV)=1.0026e-40 cm² (0.26% from first-principles anchor); differential matches closed form to 3e-9–6e-8; /4π and (ħc)² conventions load-bearing. | cevns, appendix-cevns |
| C12 | BENCH | Reconstructed ²³⁵U spectrum agrees with Huber tabulation to 0.73% (3 MeV) / 0.13% (5 MeV); emission 1.96e20 ν̄/s/GW reproduces Hayes–Vogel ~2e20. | cevns § |
| C13 | BENCH | Total muon rate through wafer 1.366 Hz, consistent with PDG sea-level flux to ~20% (within VALD-02 30% tolerance); "weakest anchor" of this channel due to 30–35% inter-experiment spread. | backgrounds § |
| C14 | BENCH | Compton edges fixed by kinematics at 1243/1541/2382 keV (⁴⁰K, ²¹⁴Bi, ²⁰⁸Tl), reproduced to <0.5 keV; single-scatter rate 0.267 Hz within 2% of independent Φσ_KN N_e estimate. | backgrounds § |
| C15 | NUM | Deposited CEvNS = 67.8 cts/kg/day above 50 eV_nr at 3 GW_th / 25 m; flux uncertainty 3.4–10%, sub-1.8 MeV placeholder dominant below 95 eV_nr. | cevns § |
| C16 | NUM | Reconstructed CEvNS peaks near 42 eV, ~85% of counts below 100 eV, integrates to 109.6 cts/kg/day, maps linearly down to ~2.5 eV. | results, intro |
| C17 | NUM | Cosmic muons deposit ~1.5–197 MeV and reconstruct into a single pile-up at E_rec ≈ 18.8 keV (Ta→Al) / 15.0 keV (Al→Hf). | results, intro, conclusions |
| C18 | NUM | Environmental-gamma Compton reconstructs to peaks near 16.8 keV (Ta→Al) / 13.3 keV (Al→Hf), integrated 2.1e5 cts/kg/day. | results § |
| C19 | NUM | Crossover deposit energy is a band ~50 eV to ~13 keV (f_prompt-dominated, "not a computed precision"); whole-array plateau 18.6 keV (Ta→Al) / 11.3 keV (Al→Hf). | response, appendix-response |
| C20 | NUM | Non-paralyzable response at the 197 MeV muon endpoint plateaus at E_rec ≈ 34.8 keV (Ta→Al) / 26.8 keV (Al→Hf); paralyzable variant rolls over to ~3.3 / 2.6 keV. | response § |
| C21 | NUM | Pileup occupancy Rτ ≈ 3.3e-5 (total in-wafer rate 1.634 Hz); quiescent reconstruction "not precluded" even at 10× flux. | results, conclusions |
| C22 | PHYS | The tens-of-keV muon pile-up is an *instrumental artifact of the modeled 25 kHz ceiling, not a physical spectral line*; saturated-regime response shape has NO literature anchor at any energy. | intro, response, results, discussion, conclusions |
| C23 | PHYS | Reactor-CEvNS recoils lie entirely in the linear regime and never test the unbenchmarked saturated shape, so the flagship result is quarantined from the dominant model risk. | discussion, results |
| C24 | PHYS | Environmental-gamma Compton continuum overlaps the CEvNS region (~1e3 cts/kg/day/keV) and is the dominant reducible background. | results, discussion |
| C25 | PHYS | Threshold placement is decisive: recovering CEvNS demands an eV-scale reconstruction floor, not merely a low deposited threshold. | discussion, conclusions |
| C26 | PHYS | Three of the four modeling caveats act only on the saturated backgrounds; the flagship (CEvNS → tens of eV) is the most robust feature. | discussion, conclusions |
| C27 | SCOPE | This is a stage-1 forward-model / feasibility study only: no sensitivity, no detectability or discovery-significance claim. | intro, discussion, conclusions |

**Theorem-like statements:** none. The paper contains no theorem/lemma/proposition/corollary constructs; claims are computational/physical, not formal-mathematical. (Proof audits therefore empty, as expected for this stage.)

---

## Overclaim flags

Overall the manuscript is unusually disciplined about its own limits: the "unbenchmarked saturated response" caveat (C22) is repeated verbatim in the abstract, intro, response, results, discussion, and conclusions, and the scope disclaimer (C27) appears three times. There are **no blocker-level overclaims** — no claim of sensitivity, discovery, or detection sneaks in. The flags below are the residual gaps between headline numbers and what the body actually anchors.

### Major

**MAJ-1 — Every quoted reconstructed-energy number inherits the definitional ε=0.5, which conflicts with the paper's own physical estimate η_ce≈0.3 by more than the stated band.**
C4 imposes ε≈0.5 as a "definitional baseline" with a "±10–20% band," but simultaneously cites a physical efficiency estimate η_ce≈0.3 that it "retains only as an independent cross-reference." A value of 0.3 is ~40% below 0.5 — well outside the ±10–20% band the paper carries. Because C is calibrated to the 0.5 slope (C6) and the whole reconstructed axis is E_rec≈ε·E_dep in the linear regime, the flagship numbers "peaking near 42 eV" (C16, abstract/intro/conclusions) and, indirectly, the plateau scales all ride on 0.5. Under the paper's own alternate physical value they would shift toward ~25 eV. The qualitative "tens of eV" claim survives either way, but the *precise* numbers are quoted with more authority than the disclosed efficiency uncertainty supports. The stated ±10–20% band understates the true uncertainty the paper itself documents.
Offending phrasing: abstract "reconstructs to tens of eV"/intro "peaking near 42 eV" resting on model § "we carry a design-dependent ±10–20% band" while the same section names η_ce≈0.3.

**MAJ-2 — The "single tens-of-keV muon pile-up" framing (C17) is in numerical tension with the response section's own endpoint value (C20), and no reconciliation is given.**
Results/intro/conclusions state the muon channel "collapse[s] onto a single tens-of-keV pile-up" at E_rec ≈ 18.8 / 15.0 keV. But the response section (C20) reports the non-paralyzable response at the 197 MeV endpoint as E_rec ≈ 34.8 / 26.8 keV — roughly 2× higher. Since muon deposits span 1.5–197 MeV, the reconstructed muon distribution must actually span ~18.8→34.8 keV (a factor ~1.85), i.e. a slowly rising log-plateau, not a delta at 18.8 keV. The "18.8 keV" figure is best read as the *mode* (where the ~MeV MPV bulk lands), but the text presents it as the location of the entire channel and never states how it relates to the 34.8 keV endpoint value in the very same paper. A reader cannot reconcile 18.8 keV (results) with 34.8 keV (response) without externally reconstructing the argument. This should be made explicit; as written it reads as an internal contradiction and slightly oversells the compression.
Offending phrasing: results "every one of them ... piles up at E_rec≈18.8 keV" vs response "the non-paralyzable response plateaus at ∼34.8 keV (Ta→Al)."

### Minor

**MIN-1 — For the signal channel, "reconstructs to tens of eV" is close to a definitional relabeling, not an emergent finding.** The deposited CEvNS spectrum already lives at tens–hundreds of eV; the linear response merely halves it (E_rec≈0.5 E_dep). Calling this a "finding" / "flagship result" (C16, C23, C26) is defensible but inflates what is essentially "small deposits stay small under a linear map." The genuinely non-trivial content is the *background* saturation, not the signal placement. The paper is honest that CEvNS sits in the linear regime, so this is presentation emphasis rather than a false claim.

**MIN-2 — The reported Compton reconstructed peak (C18, 16.8 / 13.3 keV) sits inside the unbenchmarked saturated regime but is quoted at that spot without re-flagging.** The discussion quarantine correctly includes "the high-recoil gamma tail," but the results section states the 16.8/13.3 keV peak as a definite number in the same breath as the (linear, robust) low-energy overlap, without noting that this peak is as model-dependent as the muon plateau. Easy to fix with one clause.

**MIN-3 — "Compton edges fall at the Klein–Nishina energies" (abstract) is loose terminology.** The Compton *edge* is fixed by two-body kinematics (Eq. for E_edge), independent of the Klein–Nishina cross section; KN sets the continuum *shape*, not the edge location. The body states this correctly; the abstract phrasing conflates the two. Cosmetic.

**MIN-4 — Crossover band lower bound quoted as "~50 eV" in the narrative, but the appendix f/r scan reaches ~8 eV (Ta→Al) / ~4.8 eV (Al→Hf).** The "~50 eV to ~13 keV" band (C19) in intro/discussion/conclusions uses the *default-point* lower edge, while appendix-response's own scan goes lower. Minor internal looseness; does not affect any conclusion because CEvNS falls below even 8 eV_dep-cross.

**MIN-5 — Near-coincidence of two different-axis numbers invites confusion: whole-array deposit plateau 18.6 keV (E_dep, C19) vs muon reconstructed pile-up 18.8 keV (E_rec, C17) for Ta→Al.** These live on different axes but are numerically almost identical, which (combined with MAJ-2) makes the plateau discussion hard to follow. The Al→Hf pair (11.3 keV E_dep vs 15.0 keV E_rec) shows they are genuinely distinct, so this is a clarity hazard, not an error.

---

## Contradictions / dropped-caveat check

- **No dropped saturated-response caveat.** C22 is honored consistently across all sections including the abstract. This is the paper's strongest integrity feature and it holds.
- **No dropped scope caveat.** C27 ("no sensitivity, no discovery claim") is restated in intro, discussion, and conclusions; nowhere does a detectability or significance claim leak in.
- **Internal tension (see MAJ-2):** muon pile-up location 18.8/15.0 keV (results/conclusions) vs response endpoint 34.8/26.8 keV (response). Not a stated contradiction but unreconciled.
- **Internal tension (see MAJ-1):** ε=0.5 baseline with ±10–20% band vs cited physical η_ce≈0.3. The two efficiencies are named in the same paragraph but the band does not span them.
- **Consistent handling of quenching:** the "no ionization quenching" stance (C1) is maintained; the CONUS+ eV_ee cross-check (C10 tail) is explicitly demoted to a "rate-scale cross-check only" precisely because it needs a quenching model, so no contradiction with C1.
- **Muon anchor honesty:** abstract says "within ~30%," body says ~20% within a 30% tolerance — the abstract is if anything *more* conservative than the body, so no overclaim here.
- **Promised deliverables present:** all four referenced figures exist (`cevns_dRdT_deposited.pdf`, `energy_response.pdf`, `reconstructed_energy_spectra.pdf`, `true_reconstructed_mapping.pdf`); all 21 cited bib keys are present in `references.bib`. No missing-deliverable blocker.

---

## Unbenchmarked / model-only content (for downstream specialist reviewers)

The following rest on model-only content and must be treated as "the model says," not "the detector measures." The paper labels all of these, but a technical reviewer should verify the internal math rather than the framing:

1. **Saturated-regime response shape** (C8, C20, C22) — no external anchor at any energy; only two limiting cases (linear slope 0.5; plateau above 25 kHz) are validated. Drives C17, C18-peak, C20.
2. **Sensor-sharing parameters f_prompt, r** (C5) — no measurement; scanned. Drive the 3-order-of-magnitude crossover band (C19).
3. **Efficiency ε=0.5** (C4) — definitional, conflicts with η_ce≈0.3 (MAJ-1). Sets the entire reconstructed-energy scale.
4. **Sub-1.8 MeV reactor flux** (C15) — cited-but-not-digitized placeholder (Kopeikin), ~6–10% signal-side band below 95 eV_nr.
5. **Environmental-gamma absolute normalization** (C14, C24) — site-dependent, factor-of-~2 (MEDIUM confidence); edges HIGH confidence.

Consistency verdict on the "honor the unanchored framing" test: the paper *does* consistently honor it in prose. The two places the framing slips numerically are MAJ-1 (efficiency band too narrow) and MAJ-2 (single-plateau vs 2× endpoint span). Neither overturns the qualitative separation, which is close to guaranteed by construction (tiny deposits stay linear; MeV deposits hit a bounded ceiling).
