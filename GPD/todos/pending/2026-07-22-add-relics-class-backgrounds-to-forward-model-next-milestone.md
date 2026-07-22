---
created: 2026-07-22T00:40:49.494574+00:00
title: Add RELICS-class backgrounds to forward model (next milestone)
area: numerical
files:
  - src/qpd_potential/fold.py
  - src/qpd_potential/muon_deposit.py
  - src/qpd_potential/compton_deposit.py
  - paper/sections/backgrounds.tex
---

## Problem

The stage-1 forward model carries only three deposited-energy channels (reactor
CEvNS, direct cosmic-muon ionization, external ambient-gamma Compton). Comparison
with the RELICS liquid-xenon reactor-CEvNS design study (Chang Cai et al., PRD 110,
072011 (2024) — same 3 GW, 25 m reactor configuration as ours) shows five
background channels we omit. Because our detector model is on a *unified phonon
energy scale with no NR/ER discrimination and no S2/S1 or fiducial handle*, every
one of these — especially the nuclear-recoil ones — lands directly on the same axis
as the flagship CEvNS signal in the tens-of-eV-to-keV band, so they cannot be
separated the way a shielded LXe TPC separates them. Our wafer is also *unshielded*
and at the surface, whereas RELICS suppresses most of these with a 7x7x7 m water
shield + 4pi active LXe veto. These omissions are the natural first referee question
and should be closed (or explicitly bounded) in the next milestone.

Missing channels (RELICS Sec. V), in rough priority for us:

1. **Cosmic-ray neutron-induced Ge nuclear recoils.** We have no neutron channel at
   all. High-energy CRNs (> ~10^3 MeV) penetrate shielding and produce Ge recoils in
   the CEvNS ROI. RELICS residual after a 5 m water roof: (6.0 +/- 0.6)e-2 kg^-1
   day^-1 in [0.63, 1.36] keV_nr — unshielded at surface this is far larger. Highest
   priority: it is NR, lands in the flagship band, and is undiscriminable on our
   phonon scale.
2. **Muon-induced fast neutrons + related gammas.** Secondaries of the muon channel
   we already model as direct deposits only. A through-going muon spalls fast
   neutrons from the wafer + surroundings that produce genuine NR in the signal
   region. RELICS: muon-induced NR (0.06 +/- 0.01)e-2 kg^-1 day^-1 keV^-1 in
   [0.63, 1.36] keV_nr; ER (28.0 +/- 2)e-3 kg^-1 day^-1 keV^-1 in [0, 20] keV_ee.
3. **Detector-material intrinsic radioactivity.** U/Th/K contamination in the
   ~10,300 QPD sensors, the substrate, the readout/wirebonds, and the housing
   (analog of RELICS's PMTs/vessel), producing gamma ER + (alpha,n) NR. This is
   RELICS's *dominant* ER background at (310 +/- 10)e-3 kg^-1 day^-1 keV^-1. Our
   current gamma channel is *external ambient* only and ignores the detector's own
   contamination. Needs a materials/radiopurity budget for the QPD stack.
4. **Cosmogenic activation of the Ge target and materials.** The Ge analog of
   RELICS's cosmogenic 127Xe/37Ar: 3H (tritium), 68Ge/68Ga, 65Zn in the crystal,
   plus 60Co in any Cu/steel. Continuous activation during unshielded surface
   operation makes this worse for us than for a shielded/underground experiment.
5. **Reactor-correlated gamma/neutron flux.** Prompt + n-capture reactor gammas
   (up to ~10 MeV) and reactor neutrons, which we omit entirely and RELICS bundles
   into the shielded-away external field. Unshielded at 25 m this deserves at least
   a bound.

Note which RELICS backgrounds are NOT gaps for us (LXe-technology-specific, do not
port): intrinsic 222Rn/214Pb and 85Kr in liquid xenon, and the delayed-electron /
S2-pileup background. Our pileup occupancy (R*tau) is already handled.

## Solution

Scope for the next milestone (TBD in detail during planning):

- Add a neutron transport / deposited-recoil channel (cosmic-ray + muon-induced +
  radiogenic (alpha,n)) producing dR/dE_dep on the shared phonon grid, folded
  through the existing response matrix R(E_rec | E_dep) exactly like the current
  three channels. Anchor CRN flux to CRY/Gordon-style spectra and cross-check
  against the CONUS reactor+environment neutron measurement RELICS cites.
- Add a detector-material radioactivity budget (U/Th/K + resulting gamma ER and
  (alpha,n) NR) for the QPD sensor stack; requires a materials assay assumption.
- Add a cosmogenic-activation estimate for Ge (3H, 68Ge, 65Zn) and Cu/steel (60Co)
  under a stated surface exposure / cooldown scenario.
- Bound reactor-correlated gamma/neutron flux at 25 m unshielded.
- Cross-cutting: because the phonon scale has no NR/ER discrimination, report each
  new channel's overlap with the CEvNS band explicitly and revisit whether the
  stage-1 "flagship CEvNS reconstructs to tens of eV" framing survives once NR
  backgrounds are included, or whether minimal shielding/veto must be assumed.
- Consider a short Discussion paragraph in the current paper (or the next revision)
  positioning against RELICS and flagging these as out-of-scope-for-stage-1.
