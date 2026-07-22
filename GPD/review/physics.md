# Stage: Physical-Soundness Review — QPD reactor-CEvNS reconstructed-energy spectra

- stage: physics
- reviewer_role: physical-soundness
- manuscript: paper/qpd_reactor_cevns_spectra.tex (+ sections/*.tex, appendices)
- supporting: GPD/phases/*/*SUMMARY.md, GPD/literature/{PITFALLS,PRIOR-WORK,SUMMARY,METHODS}.md, GPD/{PROJECT,REQUIREMENTS,ROADMAP}.md
- recommendation_ceiling: **major_revision**
- proof_audits: none (not requested this stage)
- overall: Physically careful and honestly caveated *within* its declared electron-recoil-background scope. The response/saturation methodology, the muon-artifact interpretation, the CEvNS cross-section/flux physics, and the environmental-gamma normalization honesty are sound. It is **not sound as presented** because it advertises an incomplete background model as complete ("three dominant channels", "two irreducible ambient radiation fields dominate the deposited-energy budget"), and the omitted class (nuclear-recoil backgrounds) is maximally consequential precisely because this detector has *no NR/ER discrimination* and the omission lands directly on the flagship CEvNS axis.

---

## BLOCKER-1 — Background model presented as complete while the physically dominant signal-axis background is silently omitted

**Where:** abstract ("the three dominant channels"), intro §1 ("its two dominant surface backgrounds"), backgrounds §1 ("Two irreducible ambient radiation fields dominate the deposited-energy budget of an unshielded surface wafer"), conclusions ("the three dominant surface channels"), discussion (gamma named "the dominant reducible background... its mitigation... is therefore the primary lever").

**Claim under test:** that reactor CEvNS, cosmic muons, and environmental-gamma Compton are the dominant background budget for this detector, and that the muon pile-up (keV) and gamma continuum are the relevant things on/near the signal axis.

**Why it fails physically:**
1. An **unshielded, surface, near-reactor (3 GW / 25 m)** germanium detector faces nuclear-recoil (NR) backgrounds that are entirely unmodeled and unmentioned: cosmic-ray/atmospheric fast neutrons, muon-induced (in-situ and rock/shield) fast neutrons, reactor-correlated fast neutrons, cosmogenic activation of Ge (e.g. ³H, ⁶⁸Ge/⁶⁸Ga, ⁶⁵Zn), and intrinsic/material radioactivity (²¹⁰Pb/²¹⁰Po surface, U/Th in components).
2. This detector's defining feature is a **unified phonon scale with no NR/ER discrimination**. Neutron-induced nuclear recoils therefore reconstruct through the *same* linear 0.5·E_dep mapping and land in the **tens-of-eV to keV region — directly on top of the flagship CEvNS band** — not displaced like muons and not merely overlapping like the gamma continuum. They mimic CEvNS event-for-event.
3. The project's own literature notes state this repeatedly and unambiguously: neutron-induced NR "mimic CEvNS exactly and are the dominant real reactor background" (SUMMARY.md), "the dominant surface background for reactor CEvNS; if out of scope, say so prominently" (PITFALLS.md), and the named comparator RELICS/Billard model five background categories (Compton γ, cosmogenic fast neutrons, ²¹⁰Pb/³H/²⁰⁶Pb internal, ν̄–e) precisely because these dominate the budget.
4. The manuscript contains **no scope-exclusion statement** for these channels. Its only "scope" statements concern being "stage-one / not a sensitivity." REQUIREMENTS.md and PROJECT.md do declare neutron NR "out of scope" — a legitimate project decision — but that makes a *prominent in-paper exclusion statement mandatory*, not optional, and the paper instead makes the *opposite* (affirmative completeness) claim.

**Consequence for interpretation:** The central interpretive conclusions about the signal axis are built on a background set that omits the one class that sits on the signal. The conclusion "cosmic muons do not preclude quiescent operation... spectrally displaced from the signal" and "environmental-gamma Compton... is the dominant reducible background... its mitigation... is the primary lever" are unsupported as *complete* physical conclusions: on a no-discrimination surface detector, NR-background suppression (veto/moderator/depth) is at least as primary, and is the reason such searches go underground. A physical conclusion about the primary background-mitigation lever outruns the modeled evidence.

**Required to clear:** (a) Add a prominent, explicit scope-exclusion paragraph (abstract-adjacent and in §Backgrounds) naming the unmodeled NR backgrounds and stating that, absent NR/ER discrimination, they reconstruct onto the CEvNS band and are expected to dominate the signal-axis budget of an unshielded surface deployment. (b) Downgrade every "dominant channels / irreducible fields dominate the budget" claim to "the two ambient electron-recoil backgrounds modeled here." (c) Re-scope the mitigation conclusion so the gamma "primary lever" statement is conditioned on the excluded NR backgrounds. This is fixable by reframing + caveat, not necessarily new simulation — hence major_revision rather than reject.

---

## MAJOR-1 — Nuclear-recoil phonon-yield / defect-loss band dropped on the flagship channel ("E_ph ≈ E_dep")

**Where:** model §"Unified phonon energy scale": "E_ph = E_dep − E_stored, where the defect (Frenkel-pair) storage E_stored is a few-percent nuclear-recoil-only correction... we take E_ph ≈ E_dep throughout."

**Assessment:** The headline assumption — *no ionization quenching, unified phonon scale* — is **physically correct** for a fieldless calorimeter with no charge collection and no Luke–Neganov gain, and is applied consistently across all three channels. Importing a Lindhard factor would indeed be wrong. That part is sound.

**But** the paper then treats the NR-specific phonon-yield defect (E_stored) as negligible ("few-percent... take E_ph ≈ E_dep"), whereas the project's own PITFALLS.md prescribes carrying it as a **systematic band (0–15% loss for 20 eV–2 keV recoils), not a point estimate.** The flagship CEvNS peak (E_rec ≈ 42 eV → E_dep ≈ 84 eV) and its "85% below 100 eV" claim sit exactly in this 20 eV–2 keV NR regime. A 0–15% NR-only shift moves the reconstructed peak position and is a *signal-side, channel-asymmetric* systematic (it does not affect the electron-recoil muon/gamma channels). The paper claims systematics are "quantified channel by channel," carries flux bands, yet drops this required NR-yield band on the one channel it most affects. The qualitative "tens of eV" survives, but the specific peak number is softer than presented.

**Required to clear:** Carry E_stored as a stated 0–15% NR-only band on the CEvNS reconstructed peak (or justify a tighter bound with a citation), and reflect it in Fig. spectra / the "42 eV" and "85% < 100 eV" figures.

---

## MINOR-1 — Efficiency ε = 0.5 vs the paper's own physical estimate η_ce ≈ 0.3 is under-propagated into the flagship number

**Where:** model §"Efficiency". E_rec ≈ 0.5·E_dep fixes the "peaks near 42 eV" headline; the paper flags ε=0.5 as a *definitional* baseline carried with ±10–20%, distinct from the physical η_ce ≈ 0.3.

**Issue:** 0.5 vs 0.3 is a ~40% difference, exceeding the stated ±10–20% band; under η_ce the CEvNS peak moves to ~25 eV and the whole reconstructed axis compresses. Both remain "tens of eV," so the qualitative flagship claim is robust and the labeling is honest, but the specific 42 eV / 16.8 keV / 18.8 keV numbers ride on a definitional choice larger than the quoted band. Recommend either widening the ε band to bracket the 0.3 estimate or stating explicitly that quoted peak energies scale linearly with ε and are not pinned.

## MINOR-2 — Non-paralyzable plateau reported as a single headline number despite an order-of-magnitude model ambiguity

**Where:** model/response §; abstract and results quote the muon pile-up at ≈18.8/15.0 keV. The equally-defensible paralyzable variant rolls the 197-MeV endpoint over to ~3.3/2.6 keV — ~order of magnitude lower — and is carried only as a "sensitivity," with the choice "closed by decision."

**Assessment:** Acceptable and well-caveated: the *qualitative* physical inference (muons pile up **above** the tens-of-eV CEvNS band, spectrally displaced from signal) holds under **both** censoring models, so the load-bearing conclusion is robust. Noting only that the headline single plateau energy is model-selected, not physical; the paper already labels it an instrumental artifact. No blocker.

## MINOR-3 — Environmental-gamma channel omits reactor-correlated and muon-secondary electromagnetic contributions; factor-of-2 site band is honest but possibly optimistic

**Where:** backgrounds §"Environmental gammas". Only radiogenic ⁴⁰K/U/Th lines are modeled. No reactor-correlated gammas (plausibly attenuated by the biological shield at 25 m, likely subdominant) and no muon soft/EM secondary continuum (PITFALLS.md recommends a soft-component/secondary term). The factor-of-2 site band is clearly and honestly flagged (edge positions HIGH confidence, normalization MEDIUM, ²³⁸U-chain balance assumed), and because the modeled gamma rate (2.1×10⁵ counts kg⁻¹ day⁻¹) swamps CEvNS (~110) the *ranking* is robust to a factor of 2. Muon-induced neutrons fold into BLOCKER-1. Minor.

---

## What is sound (explicitly credited)
- **No-quenching unified phonon scale**: correct physics for a fieldless calorimeter; applied consistently; correctly avoids mixing keV_ee/keV_nr. Matches phonon-detector convention (Billard).
- **CEvNS cross section**: /4π prefactor, (ħc)² restoration, low-energy sin²θ_W=0.2387, N² scaling, Helm form factor (negligible at reactor q) — all correct and verified against the closed form and the σ(⁷²Ge,4 MeV) anchor.
- **Reactor flux**: Huber–Mueller + honestly-banded sub-1.8 MeV placeholder + ²³⁸U(n,γ); effective 205.8 MeV/fission (not Q-value). Billard reproduction to 2.4% is a genuine external anchor.
- **Muon channel**: Gaisser–Guan flux, Landau–Vavilov MPV (not mean/Moyal), Cauchy 4V/S chord mean, importance-sampled long-chord tail — textbook-grade; 1.366 Hz within ~20–30% of PDG.
- **Saturation/response methodology**: the "instrumental artifact, not a physical line" caveat is honored prominently and repeatedly (intro, response, results, discussion, conclusions, figure caption); no linear rate→energy extrapolation (censoring-off returns exactly 0.5·E_dep); the unbenchmarked-shape risk is stated plainly. Exemplary caveat discipline.

## Counts
- blocker: 1
- major: 1
- minor: 3
- most_consequential_gap: BLOCKER-1 — unmodeled, unstated nuclear-recoil backgrounds (cosmic/muon-induced/reactor neutrons, cosmogenic activation, intrinsic radioactivity) that, on a no-discrimination phonon detector, reconstruct directly onto the flagship CEvNS axis, while the paper asserts its three channels are "dominant" and gives no scope-exclusion.
