# Milestones

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

