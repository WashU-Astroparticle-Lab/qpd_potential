# Stage 2 — Literature & Novelty Review

Manuscript: `paper/qpd_reactor_cevns_spectra.tex` (+ `paper/sections/*.tex`)
sha256 (master): `bcc30a3d108c9703a41163f36ae4c2d71773186ebef527d3c374cc184e977a4e`
Bibliography: `paper/references.bib` (21 entries)
Reviewer stage: literature-context (Stage 2). Not the final referee.
Note: no Stage-1 `CLAIMS.json` / `STAGE-reader.json` was present in `GPD/review/` at review time; claim IDs below are this stage's own labels, not Stage-1 `CLM-` IDs.

## Verdict summary

- **Novelty: genuine but narrow, and currently under-positioned.** The genuinely new element — an end-to-end *reconstructed-energy* forward model that folds reactor-CEvNS, cosmic-muon, and environmental-gamma deposited spectra through a QPD bandwidth-saturation (dead-time censoring) response matrix, yielding the result that muon MeV-scale deposits collapse onto a tens-of-keV instrumental pile-up while CEvNS recoils reconstruct linearly at tens of eV — is not something I can find in prior work. The framing is honest and conspicuously non-overclaimed (repeatedly labels the pile-up an "instrumental artifact," disclaims sensitivity/discovery, flags the unanchored saturated-regime shape). The problem is not inflation; it is that the nearest neighbors in the literature are not cited or compared.
- **Standard components correctly credited:** Freedman CEvNS cross section, Drukier–Stodolsky detection proposal, Huber–Mueller reactor flux, Billard Ge benchmark, Gaisser–Guan muon flux, Klein–Nishina + Hubbell incoherent-scattering Compton, Helm/Lewin–Smith form factor, PDG muon flux. Attribution of these is accurate.
- **No hallucinated or mis-keyed references.** All 21 bib entries are cited; every `\cite` resolves; bib has a dated verification header.

Recommendation ceiling from this stage: **major_revision** (literature positioning needs substantial repair; the core contribution survives, so not reject).

---

## Findings

### REF-L1 — [MAJOR] RELICS reactor-CEvNS design study uncited and un-positioned
- **Claim touched:** implicit novelty — "first reconstructed-observable forward model for reactor CEvNS at 3 GW_th / 25 m in a specific detector technology."
- **Issue:** Cai et al., "Reactor neutrino liquid xenon coherent elastic scattering experiment (RELICS)," PRD **110**, 072011 (2024), arXiv:2405.05554, is a directly comparable reactor-CEvNS *detector-response feasibility/design study* — Monte-Carlo optimized, ionization-only analysis channel, mapping the CEvNS signal into the detector's actual observable, at the **same reactor configuration this paper adopts: 3 GW_th thermal power at a 25 m baseline.** The matching config is almost certainly not coincidental. RELICS appears nowhere in the manuscript or `references.bib`.
- **Why it matters:** This is the closest existing "forward-model the observable, not the true recoil energy, for reactor CEvNS at 3 GW/25 m" paper. An honest novelty statement must situate the present work against it and articulate the distinction (Ge fieldless phonon calorimeter with QPD *reconstructed-energy + bandwidth-saturation* response and a unified no-quenching phonon scale, vs. LXe TPC ionization-only channel with S2 response). The overlap is in *class and scenario*, not in *method or result*, so it does **not** collapse the novelty — but leaving it out is a substantive positioning gap, not a trivial citation add.
- **Required action:** Cite RELICS; add one to two sentences (intro and/or discussion) contrasting the QPD reconstructed-energy/saturation approach with the RELICS ionization-only LXe approach at the shared reactor config.

### REF-L2 — [MAJOR] Empirical cosmic-ray → parity/quasiparticle-burst literature omitted
- **Claim touched:** the muon channel's physical basis and the "saturated-regime response has no published anchor" framing.
- **Issue:** The paper's central background mechanism — through-going muons dumping MeV-scale energy that drives quasiparticle/charge-parity bursts and saturates a parity readout — has a direct empirical literature that is not cited: Wilen et al., *Nature* **594**, 369 (2021) (radiation-induced correlated charge-parity/QP bursts in qubit arrays); McEwen et al., *Nat. Phys.* **18**, 107 (2022) (catastrophic cosmic-ray error bursts in large qubit arrays); and Li et al., *Nat. Commun.* **16**, 4677 (2025), arXiv:2402.04245 (muon-vs-gamma-resolved QP bursts with in-fridge muon detectors). The manuscript's own `GPD/literature/PRIOR-WORK.md` explicitly flags Wilen et al. as "direct experimental proof that ionizing radiation drives exactly the parity-flip channel QPDs read out," yet it is dropped from the paper.
- **Why it matters:** (i) It is the empirical grounding that the muon "background" is real in exactly these devices; omitting it makes the muon channel look purely modeled when it is empirically motivated. (ii) It bears on the repeated claim that the saturated-regime response "has no published anchor at any energy." That claim is defensible *for the energy-reconstruction curve specifically*, but it must be stated against the existing QP-burst-from-muons literature, not in a vacuum — those works establish the saturating mechanism even though they do not provide a reconstruction curve. As written, the novelty caveat is slightly stronger than the literature warrants.
- **Required action:** Cite at least Wilen 2021 and one of McEwen 2022 / Li 2025 where the muon channel and the saturation caveat are introduced; narrow "no published anchor" to "no published anchor for the reconstructed-energy saturation *shape*, though muon-induced parity/QP bursts are experimentally established [refs]."

### REF-L3 — [MINOR] Reactor-CEvNS experimental landscape is thin; closest technology cousin (Ricochet) missing
- **Issue:** The paper cites COHERENT (akimov2017), CONUS+ (conus2025), Dresden-II (dresden2022), and NUCLEUS (nucleus). It omits: the original/final CONUS limits (Bonet et al., PRL 126, 041804 (2021); PRL 133, 251802 (2024)), TEXONO/Kuo-Sheng (arXiv:2411.18812), nu-GeN, and — most notably — **Ricochet** (EPJ C 84 (2024); arXiv:2507.22751), which is *cryogenic Ge at a reactor* and thus the closest existing detector-technology cousin to a phonon-scale Ge QPD.
- **Why it matters:** For a paper whose discussion positions QPDs "within the reactor-CEvNS program," Ricochet is the natural comparison for a fieldless/cryogenic Ge phonon-scale detector and its absence is conspicuous; the others are completeness gaps. None of these collapse novelty — a representative subset is acceptable for a forward-model paper — so this is minor, but Ricochet in particular should be added.
- **Required action:** Add Ricochet; optionally add original CONUS / TEXONO / nu-GeN for a fuller landscape sentence.

### REF-L4 — [MINOR] Freedman 1974 mis-cited in `model.tex` for a quenching statement
- **Location:** `paper/sections/model.tex` — "Applying a Lindhard or ionization-yield factor here would suppress the CEvNS rate by ~5–7x and would be physically incorrect for this sensor~\cite{freedman1974}."
- **Issue:** Freedman 1974 (the CEvNS prediction) says nothing about Lindhard/ionization quenching or fieldless phonon calorimeters, so it does not support this specific statement. Elsewhere freedman1974 is used correctly (for the cross section). This one instance is a mis-attachment.
- **Required action:** Drop the citation here, or replace with an appropriate quenching/Lindhard reference (e.g., Lindhard 1963, or Lewin–Smith which is already in the bib).

### REF-L5 — [SUGGESTION] Standard dead-time model uncited
- **Issue:** The non-paralyzable / paralyzable censoring forms in `model.tex` Eq. (censor) are textbook nuclear-instrumentation results but carry no reference. A single citation (e.g., Knoll, *Radiation Detection and Measurement*) would anchor the standard part of the "methodological core."
- **Required action:** Add a standard dead-time reference at Eq. (censor). Optional/polish.

---

## Integrity spot-check (as requested)

| Reference | Attached claim | Verdict |
| --- | --- | --- |
| freedman1974 (PRD 9, 1389) | CEvNS prediction + coherent cross section | Correct in `cevns.tex`; **mis-attached** in `model.tex` (see REF-L4) |
| drukier1984 | CEvNS as a neutrino-detection channel | Correct |
| huber2011 (PRC 84, 024617) | ²³⁵U/²³⁹Pu/²⁴¹Pu conversion ν̄ spectra above 2 MeV | Correct; paper even quotes agreement with Huber tabulation (0.73%@3 MeV) |
| mueller2011 (PRC 83, 054615) | ²³⁸U flux above 2 MeV | Correct |
| billard2017 (J. Phys. G 44, 105101) | Ge benchmark 0.76/0.51/0.26 kg⁻¹d⁻¹ @ 50/100/200 eV_nr | Correct; Table-1 values match; reproduced to 2.4% |
| ramanathan2026 (arXiv:2405.17192) | QPD concept, Table II device params, EMG burst template, saturation chain | Consistent with the paper's use; the 25 kHz/40 μs ceiling and the saturated-regime shape are the authors' own modeling (explicitly disclaimed as unanchored), so no over-attribution to Ramanathan |
| guan2015 (arXiv:1509.06176) | Modified-Gaisser muon flux | Correct; preprint-only by design (acknowledged) |
| pdg | Sea-level muon flux, ξ value | Correct |
| kleinnishina1929 / hubbell1975 | Compton continuum shape / incoherent binding suppression | Correct |

No reference appears hallucinated or fabricated; all keys resolve.

## Comparison-credit check (as requested)
- **Billard benchmark:** correctly credited and quantitatively reproduced (2.4%). Good.
- **PDG muon flux:** correctly credited; ~20% agreement quoted within the stated ~30% inter-experiment spread. Good.
- **Klein–Nishina Compton edges:** correctly credited; edges fixed by kinematics, binding via Hubbell S(x,Z). Good.
- **RELICS:** not credited (REF-L1) — the one comparison a reader would expect at this reactor config and is missing.

## Net
Honest, well-scoped, non-overclaimed novelty on a narrow but real methodological contribution. Two MAJOR positioning gaps (RELICS; muon/qubit QP-burst literature) plus minor completeness/attribution issues. Fixable by citation additions and a few positioning sentences — no evidence the central claim collapses against prior work. Ceiling: **major_revision**.
