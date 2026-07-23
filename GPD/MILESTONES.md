# Milestones

## v1.1 Neutron & Radiogenic Backgrounds (SUPERSEDED: 2026-07-22)

**Status:** SUPERSEDED, not completed. Phases 7–12 were planned; **only Phase 7 executed** (2 plans, verified 19/22 with gaps). Phases 8–12 were never started and are withdrawn.

**Why superseded:** v1.1's premise was to project the in-band background ourselves from *surface, unshielded* ambient fluxes (PARMA/Gordon fast neutrons, own housing radiopurity budget) for a generic 3 GW_th / 25 m reactor site. On 2026-07-22 the user redirected the project to assume deployment at the NUCLEUS Chooz Very-Near-Site behind the NUCLEUS shielding. That makes Phases 8–9 answer the wrong question — NUCLEUS's own Fig. 8 puts the unshielded rate at 10⁴–10⁵ d⁻¹kg⁻¹keV⁻¹ against ~200 after shielding, a 2–3 order-of-magnitude difference — and inverts contract item VALD-08, which had NUCLEUS as an end-of-milestone cross-check rather than a front-of-milestone input.

**Carried forward into v2.0 (NOT discarded):**
- Phase 7 nuclear data: frozen ENDF/B-VIII.0 + NJOY/Lib80x n-Ge elastic table (thermal→20 MeV, 23155-point resonance-resolved grid), σ_tot(1–2 MeV) = 3.729 b, Σ = 0.1646 cm⁻¹, λ = 6.076 cm, P_int(2 mm) = 3.24%.
- Abundance-weighted natural T_max/E_n = 0.0536 and the per-isotope kinematics.
- The gap-D1 decision (truncate the neutron fold at 20 MeV, document the omission, never extrapolate σ_el) — *less* severe at the VNS, since building plus shield cut the >10 MeV flux by ~5–7×, but still to be quantified.
- Radiopurity/activation machinery, now driven by NUCLEUS's screened material inventory rather than our own assumed budget.

**Withdrawn:** Phases 8 (P-NSRC surface neutron source terms), 9 (P-NTRANS bare single-scatter fold), 10 (P-RAD own housing budget), 11 (P-COSMO as scoped), 12 (P-FOLD as scoped). Their physics content is re-scoped inside v2.0 against the shielded VNS environment.

**Archived evidence:** `GPD/phases/07-scenario-nuclear-data-lock/`, prior `GPD/ROADMAP.md` (v1.1) in git history at `40804a5`.

---

## v1.0 Reconstructed-Energy Spectra (Shipped: 2026-07-22)

**Phases completed:** 6 phases, 13 plans

**Delivered:** an end-to-end forward model of the reconstructed-energy background spectra (reactor CEvNS, cosmic muons, environmental-gamma Compton) for a ~110 g QPD germanium wafer, both trapping designs, plus the PRD manuscript, pipeline code, and a reproducing notebook.

**Key accomplishments:**
- Fixed the unified phonon energy scale (no ionization quenching) and the CEvNS cross-section convention/units (Phase 1).
- Frozen reactor antineutrino flux (Huber–Mueller + seam-matched sub-1.8 MeV band); ∫Φ = 7.5×10¹² ν̄/cm²/s (Phase 2).
- CEvNS dR/dT reproduces Billard within 2.4%; σ(⁷²Ge,4 MeV)=1.0026×10⁻⁴⁰ cm² (0.26%) (Phase 3).
- Muon (Gaisser–Guan⊗chord⊗Landau, 1.366 Hz) and Compton (Klein–Nishina continuum, edges 1243/1541/2382 keV, 0.267 Hz) deposited spectra (Phase 4).
- MC response matrix R(E_rec|E_dep) with 25 kHz non-paralyzable saturation; crossover band per design (Phase 5).
- Reconstructed-energy spectra: CEvNS→tens of eV (flagship band); MeV muon deposits compress onto a tens-of-keV instrumental pile-up (Phase 6).

**Validation status:**
- Billard Table 1 reproduced within 2.4% — PASSED
- PDG sea-level muon flux within ~20% — PASSED
- Klein–Nishina Compton edges within 0.5 keV — PASSED
- Response limits (E_rec≈0.5·E_dep low-E; saturation >25 kHz) — PASSED
- Cross-phase consistency (24 checks) — CONSISTENT
- All 24 anchors reproduced end-to-end by notebooks/paper_calculations.ipynb — PASSED

**What's next:** v1.1 — nuclear-recoil/RELICS-class backgrounds + round-1 manuscript revision + a quantitative sensitivity/payoff.

**Archived evidence:**
- `GPD/milestones/v1.0-ROADMAP.md`
- `GPD/milestones/v1.0-REQUIREMENTS.md`
- `GPD/milestones/v1.0/RESEARCH-DIGEST.md`
- `GPD/milestones/v1.0-MILESTONE-AUDIT.md`

---

