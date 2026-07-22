# Referee report — internal review iteration (Round 1)

**Manuscript:** `paper/qpd_reactor_cevns_spectra.tex` — "Reconstructed-energy background spectra for a Quantum-Parity-Detector germanium wafer: reactor CEvNS, cosmic muons, and environmental gammas"
**Date:** 2026-07-22
**Mode:** Internal review iteration, orchestrator-synthesized from a five-specialist panel (reader/claims, math, physics, literature, significance). This is **not** the strict `/gpd:peer-review` publication adjudication — that harness is gate-blocked (see "Harness status" below). Recommendation here is advisory.

## Recommendation: MAJOR REVISION
**Confidence:** high. **Blockers:** 1. **Major:** 4. **Minor:** ~10.

The manuscript is technically sound and unusually honest about its limits — the math reviewer independently reproduced every load-bearing number to the stated precision (0 blockers, 0 major), and no sensitivity/discovery claim leaks in anywhere. It does **not** clear acceptance because (a) it makes an explicit *completeness* claim about the background budget that is false as stated, and (b) its quantitative deliverables rest on a definitional efficiency and an unbenchmarked response in ways the prose caveats but the specific numbers partially undercut. All are fixable without new physics; one requires only a scope sentence.

## Panel verdicts (ceilings)
| Stage | Assessment | Blk | Maj | Ceiling |
|---|---|---|---|---|
| Reader / claims | disciplined; 2 internal-consistency majors | 0 | 2 | major |
| Math | sound; all numbers reproduce | 0 | 0 | minor |
| Physics | careful but advertises an incomplete model as complete | 1 | 1 | major |
| Literature | novelty genuine but narrow, honestly framed | 0 | 2 | major |
| Significance | competent; payload thin, partly definitional | 0 | — | major (reject if PRL) |

---

## BLOCKER

**B1 — Completeness overclaim: nuclear-recoil backgrounds omitted while the paper claims the budget is complete.**
The abstract/intro/§Backgrounds/conclusions call reactor CEvNS + muons + environmental γ "the three dominant channels" and "two irreducible ambient radiation fields [that] dominate the deposited-energy budget," with **no scope statement**. But an unshielded, surface, near-reactor Ge detector also faces cosmic-ray & muon-induced fast neutrons, reactor-correlated neutrons, cosmogenic Ge activation (³H, ⁶⁸Ge, ⁶⁵Zn), and intrinsic radioactivity — none modeled. This is maximally consequential *because the phonon scale has no NR/ER discrimination*: neutron-induced recoils reconstruct through the same linear 0.5·E_dep mapping and land **directly on the flagship tens-of-eV CEvNS band**, mimicking signal event-for-event (unlike muons, which pile up harmlessly at keV). The comparator RELICS (PRD 110, 072011, same 3 GW/25 m config) models five categories for exactly this reason. The overclaim then propagates into the unsupported conclusion that environmental-γ mitigation is "the primary lever."
*Fix (cheap, do now):* add an explicit scope caveat — the model covers the dominant **signal + electron-recoil** channels; nuclear-recoil backgrounds are out of scope for this stage-1 model, would be undiscriminable on the phonon scale, and are deferred (already logged as a next-milestone todo). Soften "dominant"/"irreducible…dominate the budget" language and condition the "primary lever" conclusion. *Actually modeling* those channels stays a next-milestone item, not a Round-1 blocker.

## MAJOR

**M1 — Headline numbers ride on a definitional ε=0.5 that conflicts with the paper's own physical estimate η_ce≈0.3.** (reader MAJ-1 + physics MINOR-1, two independent flags.) The ±10–20% band on 0.5 does not cover 0.3 (~40% lower). Since E_rec scales linearly with ε, the 42 eV signal peak and all plateau numbers would shift ~40% under the paper's own alternative. *Fix:* either widen the band to span η_ce, or add an explicit ε-sensitivity statement ("all E_rec values scale linearly with ε; adopting η_ce≈0.3 shifts them down ~40%").

**M2 — The muon "single plateau" is oversold as a delta.** Results quotes pile-up at 18.8/15.0 keV, but §Response's own 197 MeV-endpoint value is 34.8/26.8 keV — the reconstructed muon spectrum spans a factor ~2 (bulk near the whole-array plateau, tail to the endpoint), not a line. Compounded by a clarity hazard: the E_dep whole-array plateau (18.6 keV) and the E_rec pile-up (18.8 keV) nearly coincide on *different axes*. *Fix:* describe the muon channel as a broad pile-up spanning ~19→35 keV, de-emphasize 3-significant-figure plateau values, and disambiguate the two 18.x keV numbers.

**M3 — Literature positioning: two missing citation clusters.** (a) **RELICS** (Cai et al., PRD 110, 072011 (2024), arXiv:2405.05554) — nearest "forward-model the reactor-CEvNS observable" neighbor, same config, uncited; add a contrast paragraph (LXe ionization-only vs Ge QPD phonon reconstructed-energy). (b) The empirical **cosmic-ray→charge-parity/quasiparticle-burst** literature (Wilen 2021 *Nature* 594; McEwen 2022 *Nat. Phys.*; Li 2025 *Nat. Commun.*) — this is the empirical anchor for the muon channel and would let the "no published anchor" caveat be *narrowed* to the reconstruction **shape** rather than the effect. Minor: add Ricochet + original CONUS/TEXONO/νGeN; fix a Freedman-1974 mis-attachment in `model.tex`.

**M4 — Thin quantitative payload; no payoff metric.** (significance.) The two headline results are close to definitional consequences of the setup (linear-at-low-E is a calibration-consistency check by the paper's own admission; a monotone ceiling compressing a broad MeV spectrum inevitably piles up). Declining any S/B or exposure estimate leaves a methods exercise. *Highest-leverage fix:* add a background-subtracted signal-region S/B in the tens-of-eV band and/or an approximate exposure-to-detection (even with wide bands) — this most cleanly lifts it from technical note to PRD-worthy feasibility study.

## Decision-blocking bookkeeping
**V — Venue mismatch.** `paper/PAPER-CONFIG.json` says `journal: prl`; the documentclass and intent are PRD. This is decisive: against a PRL bar this work is a reject; against PRD's detector-feasibility scope it is a defensible major-revision. Resolve the config to PRD (assuming PRD is the target).

## MINOR (from math + reader + physics)
- NR-only defect-loss band (0–15% for 20 eV–2 keV recoils) dropped as E_ph≈E_dep on precisely the flagship channel whose 42 eV peak it shifts — state it or bound it.
- "Landau–Vavilov" but a pure Landau density is used (overstates the long-chord tail; immaterial since all muons saturate).
- Abstract "~30%" vs body "~20%" muon-rate agreement wording — reconcile.
- Integrated ν/fission ≈6.5 slightly high — disclosed consequence of the sub-1.8 MeV placeholder; note it.
- 197 MeV muon endpoint is a grid cap, not a kinematic endpoint — label it.
- Compton peak quoted inside the unanchored saturated regime without re-flagging; "Klein–Nishina energies" abstract wording is loose; crossover lower-bound narrative (50 eV) vs appendix scan (8 eV) mismatch.
- A consolidated systematics table would help.

## What's solid (keep)
- CEvNS normalization verified three ways at once (/4π prefactor, (ħc)² conversion, Q_W) via the σ(⁷²Ge,4 MeV)=1.0026e-40 reproduction (0.26%); Billard benchmark 2.37%; closed-form total to O(1e-8); counts conservation to machine precision; Compton edges, R_f, ⟨ℓ⟩, ξ(MIP) all reproduce. Implementation matches the manuscript conventions verbatim.
- The "instrumental artifact, not a physical line" caveat is honored consistently; no sensitivity/discovery leak; no hallucinated citations; all 4 figures and 21 bib keys present.

## Prioritized action list
1. **[B1]** Add the NR/neutron scope caveat + soften completeness language + condition the "primary lever" claim. *(fast; unblocks)*
2. **[V]** Fix `PAPER-CONFIG.json` journal → prd. *(fast)*
3. **[M1]** Add ε-sensitivity statement (or widen band to η_ce). *(fast)*
4. **[M2]** Reframe muon pile-up as a ~19–35 keV band; disambiguate the two 18.x keV numbers. *(fast)*
5. **[M3]** Cite + contrast RELICS; cite the cosmic-ray-burst empirical anchor and narrow the "no anchor" caveat to the response *shape*; add Ricochet/CONUS/TEXONO/νGeN; fix Freedman mis-attachment. *(moderate)*
6. **[M4]** Add a quantitative payoff (S/B in the signal band and/or exposure-to-detection) + a systematics table. *(largest lift; strengthens significance most)*
7. Sweep the minors.

Items 1–4 are internal-consistency/scope fixes achievable now; 5–6 are the substantive strengthening pass.

## Harness status
The strict `/gpd:peer-review` adjudication could not run: project-backed strict mode requires `paper/BIBLIOGRAPHY-AUDIT.json` and `paper/reproducibility-manifest.json` as inputs, neither of which exists; the only generator (`gpd paper-build`) is forbidden here (would revert the hand-refactored master). `paper/ARTIFACT-MANIFEST.json` was reconciled to the current on-disk files during this review (real fix). To run the strict harness later, those two artifacts must be produced without paper-build (bibliography audit is feasible via the bibliographer agent; the reproducibility manifest needs a generator or a faithful hand-authored version).

Stage artifacts: `GPD/review/reader-claims.md`, `math.md`, `physics.md`, `literature.md`, `STAGE-interestingness.json`.
