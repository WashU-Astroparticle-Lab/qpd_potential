# Phase 8 — Source Evidence Block (Plan 08-01)

**Deliverable:** `deliv-evidence-block`
**Produced:** 2026-07-22
**Source cache:** `data/external/nucleus/` — see `data/external/nucleus/MANIFEST.md` for retrieval
commands, byte sizes, SHA-256 checksums, integrity verdicts and conversion-probe outcomes.

## How to read this document

Every quoted sentence below is reproduced from a **locally frozen file** by a **recorded shell
command**. No sentence, number, or citation in this document originates from WebFetch, a page
summarizer, or model recall (`fp-webfetch-quote`). Two verified failures on these exact sources
motivate that rule: a summarizer reported `99.8` as absent from §5.2.1 when it is present (see
B9), and misreported the 2019 journal reference as EPJC 79, 214 when it is **EPJC 79, 1018**.

**Running the commands.** All commands assume the working directory `data/external/nucleus/`:

```bash
cd data/external/nucleus
```

Each command is `grep -o -F "<quote>" <file>`, which prints the quoted string itself on success and
exits 0. `-F` (fixed string) is required because the frozen text contains LaTeX backslashes.

**Text-normalization caveat (affects how quotes read).** The `.txt` artifacts are produced from the
frozen raw HTML by `data/external/nucleus/html_to_text.py`. Math is rendered **once** from LaTeXML's
`alttext` attribute, so mathematical fragments appear in their LaTeX source form: `\sim 5` is the
paper's "∼5", `93\times 93\times 86` is "93 × 93 × 86", `\mathrm{keV_{ee}}` is "keV_ee",
`\ceCaWO4` is "CaWO₄", `\nu` is "ν". This is a rendering of the source's own markup, not a
paraphrase. Where a reader wants the typeset form, the raw HTML is retained alongside every `.txt`.

**Version labelling.** Quotes tagged `arXiv v1` come from `2509.03559v1.txt`. §E records a
successful retrieval of the **published open-access EPJC 86, 29 (2026)** version and a four-statement
cross-version comparison; all four agree. Quotes remain labelled by the file they were taken from.

---

## A. Geometry

### A.1 The COV cap crystal — the single load-bearing geometric statement

**arXiv:2508.02488v1**, §2 "Cryogenic Outer Veto".

> In the scope of the presented commissioning, only one of the six crystals is installed directly above the target detectors. It features a cylindrical geometry with 100 mm diameter and 25 mm height, and a mass of 1 kg.

```bash
grep -o -F "In the scope of the presented commissioning, only one of the six crystals is installed directly above the target detectors. It features a cylindrical geometry with 100 mm diameter and 25 mm height, and a mass of 1 kg." 2508.02488v1.txt
```

Converted once, here: **100 mm = 10.0 cm** outer diameter, **25 mm = 2.5 cm** height.
Mass closure in §C.1.

### A.2 Internal shielding cylinder

**arXiv:2508.02488v1**, §2 "Passive shielding".

> The internal shielding, positioned directly above the cryogenic target detectors, has a cylindrical shape with a diameter of 297 mm and is mechanically secured to the cryostat using a bayonet mount.

```bash
grep -o -F "The internal shielding, positioned directly above the cryogenic target detectors, has a cylindrical shape with a diameter of 297 mm and is mechanically secured to the cryostat using a bayonet mount." 2508.02488v1.txt
```

Converted once, here: **297 mm = 29.7 cm**.

### A.3 External shielding and cryostat bore

**arXiv:2508.02488v1**, §2 "Passive shielding". *Math-bearing: `93\times 93\times 86` is LaTeXML's
`alttext` for "93 × 93 × 86"; `cm3` is "cm³".*

> The external shielding measures 93\times 93\times 86 cm3 and features a cylindrical opening (430 mm in diameter) from the top to accommodate the cryostat.

```bash
grep -o -F "The external shielding measures 93\times 93\times 86 cm3 and features a cylindrical opening (430 mm in diameter) from the top to accommodate the cryostat." 2508.02488v1.txt
```

Converted once, here: **93 × 93 × 86 cm³** external shield; **430 mm = 43.0 cm** cryostat bore.

### A.4 Chooz payload count — 18 targets + 6 COV

**arXiv:2508.02488v1**, Fig. 1 caption.

> The latter is the main difference to the final NUCLEUS setup at Chooz, which will include 18 target detectors arranged in an instrumented silicon holder, 6 high-purity germanium detectors forming the cryogenic outer veto, and an additional boron carbide layer around it.

```bash
grep -o -F "The latter is the main difference to the final NUCLEUS setup at Chooz, which will include 18 target detectors arranged in an instrumented silicon holder, 6 high-purity germanium detectors forming the cryogenic outer veto, and an additional boron carbide layer around it." 2508.02488v1.txt
```

### A.5 Chooz payload count — the 4 inner active veto detectors

**arXiv:2508.02488v1**, §2 "Data Acquisition".

> The current setup employs a preliminary version of the VDAQ with 2 channels only (VDAQ2); the final configuration at Chooz will use an upgraded system with enough channels to accommodate the 18 cryogenic target detectors, the 6 COV detectors and the 4 inner active veto detectors.

```bash
grep -o -F "The current setup employs a preliminary version of the VDAQ with 2 channels only (VDAQ2); the final configuration at Chooz will use an upgraded system with enough channels to accommodate the 18 cryogenic target detectors, the 6 COV detectors and the 4 inner active veto detectors." 2508.02488v1.txt
```

**18 targets + 6 COV + 4 IV**, from two independent statements in the same paper. 18 targets is
consistent with the two 3 × 3 arrays of A.13/A.14 (2 × 9 = 18).

### A.6 Commissioning SINGLE target detectors — *not* the array crystals

**arXiv:2508.02488v1**, §2 "Target Detectors". *Math-bearing: `5\times 5\times 5 mm3` is
"5 × 5 × 5 mm³".*

> Two types of detectors were used in the commissioning run: a CaWO4 single-TES detector, shaped as a 5\times 5\times 5 mm3 cube with a mass of 0.76 g and a TES transition temperature of approximately 15.0 mK, and a Al2O3 double-TES detector, measuring 5\times 5\times 7.5 mm3, with a mass of 0.75 g and transition temperatures of the two TES of 15.1 mK and 15.6 mK respectively.

```bash
grep -o -F "Two types of detectors were used in the commissioning run: a CaWO4 single-TES detector, shaped as a 5\times 5\times 5 mm3 cube with a mass of 0.76 g and a TES transition temperature of approximately 15.0 mK, and a Al2O3 double-TES detector, measuring 5\times 5\times 7.5 mm3, with a mass of 0.75 g and transition temperatures of the two TES of 15.1 mK and 15.6 mK respectively." 2508.02488v1.txt
```

> **⚠ OBJECT-IDENTITY WARNING — read before comparing any mass in this document.**
> These are the **two single detectors of the TUM commissioning run**. They are **different objects**
> from the **3 × 3 ARRAY crystals** of §C.2 and §C.3.
> - The **Al₂O₃ single detector** is **5 × 5 × 7.5 mm³, 0.75 g, double-TES** — a *taller* crystal.
> - The **Al₂O₃ ARRAY crystal** is a **5 mm cube, 0.50 g** (§C.3).
> The apparent **0.50 g vs 0.75 g** discrepancy is **two different detectors, not a transcription
> error**. The ratio 0.75/0.50 = 1.50 is exactly the height ratio 7.5 mm / 5.0 mm = 1.50, and both
> close against their own published masses to better than 0.5% (§C.5). **Do not "fix" this.**

### A.7 Mounting hardware (overhead scale)

**arXiv:2508.02488v1**, §2 "Target Detectors".

> The detectors were secured with bronze clamps, while sapphire spheres provided thermal and electrical isolation between the detector, holder, and clamps.

```bash
grep -o -F "The detectors were secured with bronze clamps, while sapphire spheres provided thermal and electrical isolation between the detector, holder, and clamps." 2508.02488v1.txt
```

### A.8 External shield stack

**arXiv:2509.03559v1** (arXiv v1), §2 "The NUCLEUS shielding system".

> An external shielding first combines a 5-cm thick plastic scintillator-based muon veto (MV) [37] in the outermost part, together with a 5-cm thick layer of low radioactivity Pb and a 20-cm thick layer of 5% boron-loaded high-density polyethylene (HDPE) in the innermost part.

```bash
grep -o -F "An external shielding first combines a 5-cm thick plastic scintillator-based muon veto (MV) [37] in the outermost part, together with a 5-cm thick layer of low radioactivity Pb and a 20-cm thick layer of 5% boron-loaded high-density polyethylene (HDPE) in the innermost part." 2509.03559v1.txt
```

### A.9 Internal shielding and the nearly-4π B₄C layer

**arXiv:2509.03559v1**, §2. *Math-bearing: `\mathrm{4\pi}` is "4π"; `\ceB4C` is "B₄C".*

> This internal shielding follows the same layer arrangement as the external shielding, with the addition of a nearly \mathrm{4\pi} 4-cm thick boron carbide (\ceB4C) layer to further suppress neutrons reaching the target detectors. It also features a plastic scintillator-based cold muon veto, which was designed to operate at cryogenic temperatures [38].

```bash
grep -o -F "This internal shielding follows the same layer arrangement as the external shielding, with the addition of a nearly \mathrm{4\pi} 4-cm thick boron carbide (\ceB4C) layer to further suppress neutrons reaching the target detectors. It also features a plastic scintillator-based cold muon veto, which was designed to operate at cryogenic temperatures [38]." 2509.03559v1.txt
```

### A.10 The COV composition — two cylindrical + four rectangular, 2.5 cm thick

**arXiv:2509.03559v1**, §2. *Math-bearing: `\mathcal{O} (mK)` is "𝒪(mK)".*

> The COV is an arrangement of two cylindrical and four rectangular 2.5 cm thick HPGe crystals mechanically held within a Cu support structure, operated at \mathcal{O} (mK) temperatures and read-out through the ionization channel.

```bash
grep -o -F "The COV is an arrangement of two cylindrical and four rectangular 2.5 cm thick HPGe crystals mechanically held within a Cu support structure, operated at \mathcal{O} (mK) temperatures and read-out through the ionization channel." 2509.03559v1.txt
```

**This is the only COV dimension the ROADMAP's named Success-Criterion-1 source contains: a
thickness. It states no diameter, no envelope, and no cavity dimension.** See §F.

### A.11 The COV is hermetic

**arXiv:2509.03559v1**, §2.

> It hermetically covers the cryogenic target detectors, with the primary purpose of complementing the relatively modest attenuation of the NUCLEUS passive shielding to external gamma rays.

```bash
grep -o -F "It hermetically covers the cryogenic target detectors, with the primary purpose of complementing the relatively modest attenuation of the NUCLEUS passive shielding to external gamma rays." 2509.03559v1.txt
```

### A.12 The inner veto (IV)

**arXiv:2509.03559v1**, §2. *Two output lines in the frozen text — two commands.*

> The last piece of the NUCLEUS shielding strategy is the target detector TES-instrumented holder, called inner veto (IV).

```bash
grep -o -F "The last piece of the NUCLEUS shielding strategy is the target detector TES-instrumented holder, called inner veto (IV)." 2509.03559v1.txt
```

> The main purpose of the IV is to reject surface events and holder-related events.

```bash
grep -o -F "The main purpose of the IV is to reject surface events and holder-related events." 2509.03559v1.txt
```

### A.13 The 2019 corroboration — outer veto diameter 10 cm

**arXiv:1905.10258** (EPJC **79, 1018** (2019); the journal reference was independently confirmed
via ref. [24] of arXiv:2509.03559), Fig. 8 caption. *Math-bearing: `3 \times 3` is "3 × 3";
`CE \nu NS` is "CEνNS".*

> Figure 8: 3D sketch of the NUCLEUS-10g detector. It consists of three different types of cryogenic calorimeters – two 3 \times 3 arrays of gram-scale cryogenic calorimeters as CE \nu NS target (1), an inner veto (2) and an outer veto (3) with a diameter of 10 cm. The assembly is held mechanically by a non-instrumented support structure (4). The target is operated in anti-coincidence with the inner and the outer veto. See text for details.

```bash
grep -o -F "an inner veto (2) and an outer veto (3) with a diameter of 10 cm" 1905.10258.txt
```

**This independently corroborates the 100 mm of A.1 from a different paper, six years earlier.**

### A.14 The two 3 × 3 target arrays (2019 design-stage masses)

**arXiv:1905.10258**, §3.2.1.

> Figure 8 shows a schematic view of NUCLEUS-10g: a 3 \times 3 array of CaWO4 (6 g) and a 3 \times 3 array of Al2O3 (4 g).

```bash
grep -o -F "Figure 8 shows a schematic view of NUCLEUS-10g: a 3 \times 3 array of CaWO4 (6 g) and a 3 \times 3 array of Al2O3 (4 g)." 1905.10258.txt
```

> **Number-provenance note.** The 2019 paper gives the array totals as **6 g** and **4 g**
> (design stage). The 2026 paper gives them as **6.8 g** and **4.5 g** (D.1 below). The mass
> closures in §C.2/§C.3 use the **2026** totals, which are the current values; §C.4 reports the
> 2019 variant as a sensitivity. `08-RESEARCH.md` V2/V3 quote 6.8 g and 4.5 g without naming their
> source paper — the source is **arXiv:2509.03559v1 §2**, not the 2019 paper.

### A.15 The published (5 mm)³ crystal edge

**arXiv:1905.10258**, §3.2.1. This is the CRESST-heritage prototype crystal from which the
gram-scale array crystals derive.

> With a 0.5 g prototype detector made from a (5 mm)3 Al2O3 cubic crystal, an unprecedented ultra-low threshold of Eth = (19.7 \pm 0.9) eV has been reached [13], one order of magnitude lower than previous devices.

```bash
grep -o -F "With a 0.5 g prototype detector made from a (5 mm)3 Al2O3 cubic crystal, an unprecedented ultra-low threshold of Eth = (19.7 \pm 0.9) eV has been reached [13], one order of magnitude lower than previous devices." 1905.10258.txt
```

Note the direct agreement: **0.5 g at a (5 mm)³ Al₂O₃ cube**, matching the array per-crystal mass
derived independently in §C.3.

### A.16 COV **PROTOTYPE** geometry — ⚠ NOT THE FINAL COV

**arXiv:2401.09837v1** (Goupy et al., NIM A **1064**, 169383 (2024)).

> It consists of two cylindrical \mathrm{\sim} 400 g HPGe crystals of 70 mm diameter \times 20 mm height, each placed above and below a 25 mm diameter \times 25 mm height 51.7 g cylindrical \mathrm{Li_{2}WO_{4}} crystal BASKET ; LWO_Growth .

```bash
grep -o -F "It consists of two cylindrical \mathrm{\sim} 400 g HPGe crystals of 70 mm diameter \times 20 mm height" 2401.09837v1.txt
```

### A.17 Prototype mounting overhead — ⚠ PROTOTYPE

**arXiv:2401.09837v1**, §2.

> The two HPGe crystals were housed within 3-mm thick copper boxes and secured using PTFE (Teflon) holders.

```bash
grep -o -F "The two HPGe crystals were housed within 3-mm thick copper boxes and secured using PTFE (Teflon) holders." 2401.09837v1.txt
```

> **⚠ PROTOTYPE — NOT THE FINAL COV.** A.16/A.17 describe a **70 mm × 20 mm prototype** tested in a
> dry dilution refrigerator, **not** the six-crystal Chooz COV. The final COV crystals are
> **100 mm × 25 mm** (A.1) and **2.5 cm thick** (A.10). A.16/A.17 may be used **only** as an
> indication of the *scale of mounting overhead* (3 mm Cu walls + PTFE holders). They must never be
> substituted for the final COV geometry.

---

## B. Rejection statements (the L2 catalogue)

All from **arXiv:2509.03559v1**. Section attributions were determined by locating each quote
relative to the numbered section headings in the frozen text.

### B.1 §5.1 — veto thresholds

> The energy thresholds defining a MV hit, a COV hit, an IV hit and a cryogenic target detector hit were set to 5 MeV, 1 keV, 30 eV and 10 eV, respectively.

```bash
grep -o -F "The energy thresholds defining a MV hit, a COV hit, an IV hit and a cryogenic target detector hit were set to 5 MeV, 1 keV, 30 eV and 10 eV, respectively." 2509.03559v1.txt
```

### B.2 §5.1 — the full selection, including the multiplicity conjunct

> Finally, the identification of a CE \nu NS-like event must meet the combination of all possible anti-coincidence selection criteria, i.e. having (i) no hits in any of the veto detectors and (ii) a hit in one and only one of the target detectors.

```bash
grep -o -F "Finally, the identification of a CE \nu NS-like event must meet the combination of all possible anti-coincidence selection criteria, i.e. having (i) no hits in any of the veto detectors and (ii) a hit in one and only one of the target detectors." 2509.03559v1.txt
```

### The three distinct "factor 5" statements of §5.2.1

**Section 5.2.1 of arXiv:2509.03559v1 contains three separate statements involving a factor 5.
They describe three different physical objects. They are quoted separately below and each is
labelled by the object it describes. This document contains no bare, unattributed "factor 5".**
They appear in the source in the order B.3 → B.4 → B.5.

#### B.3 — factor 5 **#1: a Geant4 modelling conservatism.** NOT a rejection factor.

**Physical object:** a downscaling applied to *simulated deposited energies* in the COV and MV
volumes, to account for nuclear-recoil quenching. It reduces the *credited* veto response; it is
not a background-rejection factor at all.

> For the case of atmospheric neutrons, a crude but conservative approximation scaled down all deposited energies in the COV and the MV volumes by a factor 5 and 2 respectively, to take into account their quenching to neutron-induced nuclear recoils [70, 71, 72]. For muon-induced background, since in the COV, most of the events seen in coincidence with the cryodetectors come from secondary neutrons, a factor 5 down scaling of the energies deposited in the COV is cautiously applied as well.

```bash
grep -o -F "For the case of atmospheric neutrons, a crude but conservative approximation scaled down all deposited energies in the COV and the MV volumes by a factor 5 and 2 respectively, to take into account their quenching to neutron-induced nuclear recoils [70, 71, 72]." 2509.03559v1.txt
```

#### B.4 — factor ~5 **#2: PASSIVE attenuation by the 4 cm B₄C liner.**

**Physical object:** the nearly-4π 4-cm-thick boron-carbide layer inside the cryostat (A.9). This is
material attenuation, not an anti-coincidence veto — but its value is coupled to the payload's
size, which is why 08-RESEARCH classifies it **L1\*** (passive but payload-geometry-coupled) rather
than clean L1.

> It turns out to be a very effective complement to the external neutron shield, further suppressing the event rates in the \ceCaWO4 detectors by a factor \sim 5.

```bash
grep -o -F "It turns out to be a very effective complement to the external neutron shield, further suppressing the event rates in the \ceCaWO4 detectors by a factor \sim 5." 2509.03559v1.txt
```

#### B.5 — factor 5 **#3: the COV ANTI-COINCIDENCE neutron rejection.** The genuine L2 statement.

**Physical object:** the active cryogenic outer veto operating in anti-coincidence at a 1 keV_ee
threshold, reducing neutron-induced backgrounds.

> While the impact of the MV is marginal, the COV brings a sizable additional reduction of the neutron-induced backgrounds of a factor 5.

```bash
grep -o -F "While the impact of the MV is marginal, the COV brings a sizable additional reduction of the neutron-induced backgrounds of a factor 5." 2509.03559v1.txt
```

### B.6 §5.2.1 — the threshold cost of the COV rejection

*Math-bearing: `\mathrm{keV_{ee}}` is "keV_ee".*

> For instance, raising the COV threshold from 1 \mathrm{keV_{ee}} to 10 \mathrm{keV_{ee}} degrades the neutron-induced background rejection by approximately 20%.

```bash
grep -o -F "For instance, raising the COV threshold from 1 \mathrm{keV_{ee}} to 10 \mathrm{keV_{ee}} degrades the neutron-induced background rejection by approximately 20%." 2509.03559v1.txt
```

Note the source unit is **keV_ee** (electron-equivalent), not bare keV.

### B.7 §5.2.1 — the IV plus one-hit requirement is "very marginal"

> Finally, the benefit of applying all vetoes, i.e. (i) using the IV and (ii) requesting only one cryogenic detector hit in addition to the MV and COV anti-coincidence selection criteria, is very marginal.

```bash
grep -o -F "Finally, the benefit of applying all vetoes, i.e. (i) using the IV and (ii) requesting only one cryogenic detector hit in addition to the MV and COV anti-coincidence selection criteria, is very marginal." 2509.03559v1.txt
```

This is the sentence that makes the monolithic wafer's identically-zero multiplicity rejection cost
little in *absolute* background — an honest point in the wafer's favour, which Phase 8 must report
alongside the no-fit direction.

### B.8 §5.2.1 — the 478 keV ¹⁰B(n,α) line

*Math-bearing: `\mathrm{{}^{10}B}` is "¹⁰B".*

> The emission of a 478 keV gamma-ray line following neutron capture on \mathrm{{}^{10}B} is harmless to the cryogenic target detectors, as it is efficiently shielded and vetoed by the 2.5 cm thick COV HPGe crystals.

```bash
grep -o -F "The emission of a 478 keV gamma-ray line following neutron capture on \mathrm{{}^{10}B} is harmless to the cryogenic target detectors, as it is efficiently shielded and vetoed by the 2.5 cm thick COV HPGe crystals." 2509.03559v1.txt
```

The "harmless" verdict is **conditional on the COV**: the line is inherited with the B₄C liner; the
rejection that makes it harmless is not.

### B.9 §5.2.1 — the >99.8% claim, quoted in full

**The phrase "muon-induced" is inside the quotation itself.** The claim is about muon-*induced
secondaries*, not about tagging through-going muons.

> Unsurprisingly, the MV was also found to be very efficient. When combined with the COV, they are predicted to reject more than 99.8% of the muon-induced backgrounds in the CE \nu NS RoI, making them a negligible contributor to the total background budget (see section 5.3).

```bash
grep -o -F "Unsurprisingly, the MV was also found to be very efficient. When combined with the COV, they are predicted to reject more than 99.8% of the muon-induced backgrounds in the CE \nu NS RoI, making them a negligible contributor to the total background budget (see section 5.3)." 2509.03559v1.txt
```

This is the sentence a summarizer reported as **absent** during research. It is present, at
character offset 70413 of `2509.03559v1.txt`, in §5.2.1.

### B.10 §5.2.2 — the Pb factor ~50 and the additional ~10

*Two output lines in the frozen text — two commands.*

> A thickness of 5 cm of Pb followed from extensive Geant4 simulation studies.

```bash
grep -o -F "A thickness of 5 cm of Pb followed from extensive Geant4 simulation studies." 2509.03559v1.txt
```

> It gives a factor \sim 50 reduction of the event rate in the \ceCaWO4 target detectors, while the rest of the NUCLEUS setup passive materials (see figure 1 (d) and figure 1 (e)) makes an additional factor \sim 10 reduction.

```bash
grep -o -F "It gives a factor \sim 50 reduction of the event rate in the \ceCaWO4 target detectors, while the rest of the NUCLEUS setup passive materials (see figure 1 (d) and figure 1 (e)) makes an additional factor \sim 10 reduction." 2509.03559v1.txt
```

### B.11 §5.2.2 — the COV's "essential role" in gamma rejection

> It particularly points out the essential role of the COV in reducing the environmental gamma ray contribution down to sufficiently low levels.

```bash
grep -o -F "It particularly points out the essential role of the COV in reducing the environmental gamma ray contribution down to sufficiently low levels." 2509.03559v1.txt
```

### B.12 §5.2.2 — the IV is insensitive to environmental gammas

> The IV is a very thin detector (see figure 1 (f)), which makes it insensitive to the interactions of environmental gamma rays. As expected, it does not improve the rejection of this background component.

```bash
grep -o -F "The IV is a very thin detector (see figure 1 (f)), which makes it insensitive to the interactions of environmental gamma rays. As expected, it does not improve the rejection of this background component." 2509.03559v1.txt
```

### B.13 §2 — the target masses used by the 2026 paper

> In the region of interest (RoI) between 10 and 100 eV, this flux gives an average CE \nu NS detection rate of about 280 and 20 \text{\,}{\mathrm{d}}^{-1}\text{\,}{\mathrm{kg}}^{-1}\text{\,}{\mathrm{keV}}^{-1} in the \ceCaWO4 (6.8 g) and \ceAl2O3 (4.5 g) target detectors, respectively.

```bash
grep -o -F "in the \ceCaWO4 (6.8 g) and \ceAl2O3 (4.5 g) target detectors, respectively." 2509.03559v1.txt
```

**This is the source of the 6.8 g and 4.5 g totals used in §C.** Note the 280 d⁻¹kg⁻¹keV⁻¹ here is
the §2 prose value at 100% duty; the project's contract already flags that the Table 5 value, not
this prose number, is the anchor.

---

## C. Mass closure — dimensions checked against independently published masses

**Principle.** A length read from a paper is trusted only when it reproduces an independently
published mass. Densities are standard material values, **assumed** rather than quoted from these
papers; ρ_Ge is fixed by `GPD/CONVENTIONS.md` §D.

| Symbol | Value | Provenance |
|---|---|---|
| ρ_Ge | 5.323 g/cm³ | `GPD/CONVENTIONS.md` §D (project convention lock) |
| ρ_CaWO₄ | 6.06 g/cm³ | standard material density — **assumed**, not quoted from any NUCLEUS paper |
| ρ_Al₂O₃ | 3.98 g/cm³ | standard material density — **assumed**, not quoted from any NUCLEUS paper |

### C.1 COV cap crystal (Ge) — licenses the 100 mm × 25 mm read

**Object:** one of the two *cylindrical* HPGe crystals of the six-crystal Chooz COV (A.1, A.10).

```
V = π r² h = π (5.0 cm)² (2.5 cm) = 196.3495 cm³
m = ρ_Ge V = 5.323 g/cm³ × 196.3495 cm³ = 1045.17 g
```

**Computed: 1045.2 g, with ρ_Ge = 5.323 g/cm³. Published (A.1): "a mass of 1 kg".**

"1 kg" is a **1-significant-figure specification**. Its 1-s.f. band is [500, 1500] g; 1045.2 g sits
comfortably inside. Against a *nominal* 1000 g the offset is **+4.52%**.

> **Precision caveat — do not report this as "passes within 5%" without the numbers.** The margin
> against a naive ±5% band ([950, 1050] g) is only **4.8 g**, i.e. **0.48 percentage points**, and
> it depends on the ρ_Ge rounding:
>
> | ρ_Ge assumed | computed mass | offset vs 1000 g | inside naive ±5%? |
> |---|---|---|---|
> | 5.320 | 1044.6 g | +4.46% | yes |
> | **5.323** (CONVENTIONS §D) | **1045.2 g** | **+4.52%** | yes (by 4.8 g) |
> | 5.350 | 1050.5 g | +5.05% | **no** |
>
> The closure is therefore reported as **consistent with a 1-significant-figure "1 kg"**, which is
> the honest statement, rather than as "within 5%", which is true only for the adopted ρ_Ge.

**What this licenses:** treating **100 mm diameter × 25 mm height** as a correct read of a
germanium crystal. It does *not* license anything about the four rectangular COV crystals.

### C.2 CaWO₄ **3 × 3 ARRAY** crystal — licenses the array footprint

**Object:** one crystal of the **3 × 3 CaWO₄ target array** (A.13, A.14). **NOT** the commissioning
single-TES detector of A.6.

```
m_crystal = 6.8 g / 9 = 0.7556 g            [total from B.13, count 9 from A.13/A.14]
V         = 0.7556 g / 6.06 g/cm³ = 0.12468 cm³
edge      = V^(1/3) = 0.4996 cm = 4.996 mm   vs published 5 mm cube (A.15)
deviation = -0.09%                            PASS (< 1%)
```

Cross-check with the paper's own Table 3 total of **6.82 g**: edge = **5.001 mm**, deviation
**+0.01%**.

### C.3 Al₂O₃ **3 × 3 ARRAY** crystal — licenses the array footprint, independently

**Object:** one crystal of the **3 × 3 Al₂O₃ target array**. **⚠ THIS IS THE ARRAY CRYSTAL, NOT the
commissioning Al₂O₃ single detector of A.6** (which is 5 × 5 × 7.5 mm³, 0.75 g, double-TES).

```
m_crystal = 4.5 g / 9 = 0.5000 g            [total from B.13, count 9 from A.13/A.14]
V         = 0.5000 g / 3.98 g/cm³ = 0.12563 cm³
edge      = V^(1/3) = 0.5008 cm = 5.008 mm   vs published 5 mm cube (A.15)
deviation = +0.17%                            PASS (< 1%)
```

The derived per-crystal mass **0.500 g** matches the directly published **"0.5 g prototype detector
made from a (5 mm)³ Al₂O₃ cubic crystal"** (A.15) exactly.

**What C.2 and C.3 license:** the published 3 × 3 target-array crystal footprint is
**9 × (5 mm)² = 2.25 cm²**. These closures are entirely unaffected by the single-detector geometry
of A.6.

### C.4 Sensitivity to the 2019 design-stage totals

Using the 2019 array totals (A.14: 6 g CaWO₄, 4 g Al₂O₃) instead of the 2026 totals:

| Array | 2019 total | per-crystal | edge | deviation vs 5 mm |
|---|---|---|---|---|
| CaWO₄ | 6 g | 0.6667 g | 4.792 mm | −4.17% |
| Al₂O₃ | 4 g | 0.4444 g | 4.816 mm | −3.69% |

Both still round to a 5 mm cube but **fail the 1% criterion**. The 2026 totals (6.8 / 4.5 g) close
at the 0.1% level and the 2019 totals do not, which is itself evidence that **6.8 g / 4.5 g are the
current per-array masses and 6 g / 4 g were early design figures.** The closures in C.2/C.3 use the
2026 values.

### C.5 Cross-check on the two-object distinction (A.6)

Both commissioning **single** detectors close against their own published masses, confirming they
are correctly read *and* that they are different objects from the array crystals:

| Object | Published geometry | Published mass | ρ × V | Deviation |
|---|---|---|---|---|
| CaWO₄ single-TES | 5 × 5 × 5 mm³ | 0.76 g | 0.757 g | −0.33% |
| Al₂O₃ double-TES | 5 × 5 × **7.5** mm³ | 0.75 g | 0.746 g | −0.50% |

0.75 g / 0.50 g = **1.50** = 7.5 mm / 5.0 mm = **1.50**. The Al₂O₃ mass difference is fully
explained by the crystal being 1.5× taller. **It is not a transcription error.**

### C.6 Wafer closure against CONVENTIONS §D

**Object:** the QPD project's 4″ × 4″ × 2 mm single-sided germanium wafer.

```
V     = 10.16 cm × 10.16 cm × 0.20 cm = 20.6451 cm³
m     = 5.323 g/cm³ × 20.6451 cm³      = 109.89 g          -> 109.9 g   ✓ CONVENTIONS §D
face  = 10.16 cm × 10.16 cm            = 103.2256 cm²      -> 103.23 cm² ✓
diag  = √2 × 10.16 cm                  = 14.3684 cm        -> 14.37 cm   ✓
```

Face-area ratio to the published 3 × 3 crystal footprint: 103.2256 / 2.25 = **45.9×**.
(The "~9 cm²" figure repeated in the ROADMAP is a *holder-scale* estimate, not a NUCLEUS number;
its ratio would be 11.5×. Plan 08-05 owns flagging that. **Both bases must always be labelled.**)

### C.7 Closure verdict

| # | Closure | Computed | Published | Criterion | Verdict |
|---|---|---|---|---|---|
| V1 | COV cap crystal (Ge) | 1045.2 g @ ρ=5.323 | "a mass of 1 kg" (1 s.f.) | consistent with 1 s.f. | **PASS** |
| V2 | CaWO₄ 3×3 ARRAY crystal | 4.996 mm edge | 5 mm cube | < 1% | **PASS** (−0.09%) |
| V3 | Al₂O₃ 3×3 ARRAY crystal | 5.008 mm edge | 5 mm cube | < 1% | **PASS** (+0.17%) |
| V4 | Wafer | 109.89 g, 103.2256 cm² | 109.9 g, 103.23 cm² | exact | **PASS** |

All four pass. No closure was rounded away, and no failure was absorbed.

---

## D. Anchor promotion: arXiv:2508.02488 is NOT in the ROADMAP Phase-8 anchor list

**Declaration.** `arXiv:2508.02488` (NUCLEUS commissioning at TUM) does **not** appear in the
`GPD/ROADMAP.md` Phase 8 anchor list. It is **promoted to a Phase-8 anchor by this phase**, and this
document is the written record of that promotion. It is the **single load-bearing geometric source**
for Phase 8: A.1 (100 mm × 25 mm, 1 kg), A.2 (297 mm), A.3 (93 × 93 × 86 cm³, 430 mm bore),
A.4/A.5 (18 + 6 + 4).

**Corroboration argument — three consistent statements plus a physical closure:**

1. **Thickness agreement across papers.** arXiv:2509.03559v1 §2 independently states the COV
   crystals are **2.5 cm thick** (A.10), matching the commissioning crystal's **25 mm height**
   (A.1). Two papers, one number.
2. **Diameter agreement across papers, six years apart.** arXiv:1905.10258 Fig. 8 states the outer
   veto has **a diameter of 10 cm** (A.13), matching the commissioning crystal's **100 mm** (A.1).
3. **Mass closure (C.1).** ρ_Ge π (5.0 cm)² (2.5 cm) = **1045 g**, consistent with the
   independently published **1 kg**. A dimension read that reproduces an independently published
   mass is not a mis-read.

**Honest caveat — this is a TUM commissioning paper, not Chooz.** arXiv:2508.02488 describes the
commissioning setup at the Technical University of Munich, in which *one* of the six COV crystals
was installed (A.1). It is **not** the Chooz drawing. The inference that the commissioning COV
crystal and the Chooz COV cap crystals are the same part is supported by (1) and (2) above but is
**not read from a Chooz engineering source**. This remains a `weakest_anchors` item and a live
`competing_explanations` item (the 100 mm crystal could be a commissioning-only part).

**Not-independent warning (V10).** The 100 mm-cylinder route and any Fig.-1(e) pixel-scaling route
**share the same scale anchor** and therefore do **not** corroborate each other independently. A
genuinely independent third route requires the Goupy 2024 thesis, which is unobtainable by any
scripted route (`MANIFEST.md` §4).

---

## E. Carried-forward L1 anchor verification, and the cross-version spot-check

### E.1 Carried-anchor status table

Every anchor carries an explicit verdict. No anchor is left silently assumed.

| Anchor | Verdict | Section | Reproducing command |
|---|---|---|---|
| Overburden **2.92 ± 0.01 m w.e.** | **VERIFIED VERBATIM** | §4.1 | see E.1.1 |
| Muon attenuation **1.41 ± 0.02** | **VERIFIED VERBATIM** | §4.1 | see E.1.2 |
| Table 4 normalization uncertainties **25% / 30% / 20% / 30%** | **VERIFIED VERBATIM** | Table 4 (in §5.1) | see E.1.3 |
| The literal ASCII string `m.w.e` | **NOT FOUND in v1** | — | see E.1.4 — *reportable finding, not a failure* |

#### E.1.1 Overburden — §4.1 "Attenuation of cosmic ray-induced muons"

*Math-bearing: `2.92\pm 0.01\text{\,}\mathrm{m}\text{\,}\mathrm{w.e.}` is "2.92 ± 0.01 m w.e.".*

> An omnidirectional overburden of 2.92\pm 0.01\text{\,}\mathrm{m}\text{\,}\mathrm{w.e.} was computed by averaging the overburden map over all directions.

```bash
grep -o -F "An omnidirectional overburden of 2.92\pm 0.01\text{\,}\mathrm{m}\text{\,}\mathrm{w.e.} was computed by averaging the overburden map over all directions." 2509.03559v1.txt
```

#### E.1.2 Muon attenuation factor — §4.1

> Measurements of the muon count rates above ground and in the VNS at various zenith and azimuth orientations gave an omnidirectional muon attenuation factor of 1.41\pm 0.02\text{\,} , corresponding to a mean overburden of 2.9\pm 0.1\text{\,}\mathrm{m}\text{\,}\mathrm{w.e.} [24].

```bash
grep -o -F "gave an omnidirectional muon attenuation factor of 1.41\pm 0.02\text{\,} , corresponding to a mean overburden of 2.9\pm 0.1\text{\,}\mathrm{m}\text{\,}\mathrm{w.e.} [24]." 2509.03559v1.txt
```

> **Nuance worth carrying forward.** These are **two different overburden numbers in the same
> section**: the *measured* cosmic-wheel value is **2.9 ± 0.1 m w.e.** and is what the 1.41 ± 0.02
> attenuation factor corresponds to; the **2.92 ± 0.01 m w.e.** of E.1.1 is the *simulated*
> overburden-map average. The project's contract carries 2.92 ± 0.01 and 1.41 ± 0.02 together; they
> are consistent but are not the same measurement.

#### E.1.3 Table 4 normalization uncertainties

Table 4 caption:

```bash
grep -o -F "Table 4: Flux and uncertainty assumptions used in the normalization of the different background components." 2509.03559v1.txt
```

Table body (each row is a separate output line in the frozen text):

```bash
grep -o -F "Background component Flux [ {\mathrm{cm}}^{-2}\text{\,}{\mathrm{s}}^{-1} ] Uncertainty (VNS) [%]" 2509.03559v1.txt
grep -o -F "Atm. muons 1.90 \times\,10^{-2} (surface) 25" 2509.03559v1.txt
grep -o -F "Atm. neutrons 1.34 \times\,10^{-2} (surface) 30" 2509.03559v1.txt
grep -o -F "Env. gamma rays 5.03 (VNS) 20" 2509.03559v1.txt
grep -o -F "Material radioactivity see table 3 30" 2509.03559v1.txt
```

Verified: atmospheric muons **25%**, atmospheric neutrons **30%**, environmental gammas **20%**,
material radioactivity **30%**. The measured VNS gamma ambience **5.03 cm⁻² s⁻¹** is verified in the
same table.

#### E.1.4 `m.w.e` as a literal string — NOT FOUND

```bash
grep -c -F "m.w.e" 2509.03559v1.txt    # exit 1, no match
```

**Finding, not a failure.** The paper writes the unit as `\mathrm{m}\text{\,}\mathrm{w.e.}`, i.e.
typeset "m w.e." with a thin space, never the compressed "m.w.e" used in the project's own
documents. The *values* 2.92 ± 0.01 and 1.41 ± 0.02 are verified verbatim (E.1.1, E.1.2). Any
future grep for this anchor must search `2.92\pm 0.01`, not `2.92 m.w.e.`.

### E.2 Cross-version spot-check against the published EPJC 86, 29 (2026)

**The journal version WAS retrievable.** The plan and 08-RESEARCH anticipated it might not be.

```bash
curl -sS -L -A "<browser UA>" -o epjc_86_29.html \
  "https://link.springer.com/article/10.1140/epjc/s10052-025-15168-9"
python3 html_to_text.py epjc_86_29.html epjc_86_29.txt
```

Retrieved 2026-07-22 UTC · HTTP 200 · `text/html` · 725 650 B ·
SHA-256 `989842e65bfae44adf22c1e759defeb8ed0beba9e486033ac64813e89724ff19`. Converted text
116 076 B, SHA-256 `b60641eba11a15885edd1c23a99b5f71991c24ce672bf0cdf3179f0c40592793`. Verified as
full open-access text (contains §5.2.1 and §5.2.2 in full), not a paywall stub.

| # | Statement | Verdict |
|---|---|---|
| 1 | COV factor-5 neutron rejection | **agrees with v1** |
| 2 | >99.8% muon-induced rejection | **agrees with v1** |
| 3 | ~20% cost of raising the COV threshold 1 → 10 keV_ee | **agrees with v1** |
| 4 | 2.5 cm COV crystal thickness | **agrees with v1** |

Reproducing commands (run against `epjc_86_29.txt`):

```bash
grep -o -F "While the impact of the MV is marginal, the COV brings a sizable additional reduction of the neutron-induced backgrounds of a factor 5." epjc_86_29.txt
grep -o -F "they are predicted to reject more than 99.8% of the muon-induced backgrounds" epjc_86_29.txt
grep -o -F "degrades the neutron-induced background rejection by approximately 20%." epjc_86_29.txt
grep -o -F "The COV is an arrangement of two cylindrical and four rectangular 2.5 cm thick HPGe crystals mechanically held within a Cu support structure" epjc_86_29.txt
```

All four sentences are **word-for-word identical** between arXiv v1 and the published EPJC version.
The only differences observed anywhere in the compared passages are typographic/markup:
`10-100` → `10–100` (en dash), `figure 8` → `Fig. 8`, `section 5.3` → `Sect. 5.3`, and LaTeXML
`\nu` vs MathJax `\(\nu \)`. **No numeric or physical difference was found.**

Additionally verified present and unchanged in the journal version: the 2.92 ± 0.01 m w.e.
overburden, the 1.41 ± 0.02 attenuation factor, and the B₄C "factor ∼5" sentence.

**Effect on labelling.** Because the four load-bearing L2 statements are confirmed against the
version of record, the confidence in the arXiv-v1 quotes is **upgraded**. Quotes in this document
remain labelled by the file they were taken from (`arXiv v1`), which is a provenance label, not a
statement that the journal version differs.

**Residual caveat.** The Table 4 numeric body (25/30/20/30) is served by Springer behind a "Full
size table" link and is **not present** in the retrieved article HTML, so those four values are
verified against **arXiv v1 only** (E.1.3).

---

## F. Figure 1 inspection — the Success-Criterion-1 evidence route

### F.1 Inspection method (so the negative result is auditable)

| Item | Value |
|---|---|
| File | `data/external/nucleus/2509.03559v1_Figure1.png` |
| SHA-256 | `bddf5c998b9f54b10a9ff1fbbe6e372c7ea2d579effabcaad6f861c4535c34da` |
| Pixel dimensions | **1875 × 2613** |
| Mode / format / DPI | RGB / PNG / 149.987 |
| Panels examined | **all six, (a)–(f)** |
| Full-figure inspection | whole image at 2× downscale (938 × 1307) — every callout legible |
| Full-resolution inspection | panel (d) crop `(900, 830)–(1875, 1690)`; panel (e) crop `(0, 1680)–(960, 2613)`; panel (f) crop `(930, 1740)–(1875, 2500)` |
| Tool | PIL (Pillow) 10.2.0 |

```bash
python3 -c "from PIL import Image; im=Image.open('2509.03559v1_Figure1.png'); print(im.size, im.mode, im.format)"
# -> (1875, 2613) RGB PNG
```

### F.2 Figure 1 caption (complete)

> Figure 1: Simplified schematic view of NUCLEUS at the VNS, breaking down the main components of the experiment.

```bash
grep -o -F "Figure 1: Simplified schematic view of NUCLEUS at the VNS, breaking down the main components of the experiment." 2509.03559v1.txt
```

**The caption contains no dimension and no scale statement.** It self-describes the figure as
"Simplified schematic".

### F.3 Complete transcription of the panel titles

Read directly off the image:

| Panel | Title |
|---|---|
| a) | Chooz nuclear power plant |
| b) | Very Near Site (VNS) |
| c) | VNS room |
| d) | NUCLEUS experimental setup |
| e) | Cryostat volume |
| f) | Inner detector modules |

### F.4 Complete callout list — panel (e) "Cryostat volume"

Every text label on the panel, transcribed from the full-resolution crop:

1. Copper support & thermalization structure
2. Cold muon veto
3. Internal gamma shield (lead)
4. Internal neutron shield (poly-ethylene)
5. Vessels (Al or Cu)
6. Cryogenic outer veto (germanium)
7. Inner detector modules *(pink; the callout linking to panel f)*
8. Cryogenic neutron shield (boron carbide)

**Eight callouts. All are material/component names. None carries a number, a length, or a unit.**

### F.5 Complete callout list — panel (f) "Inner detector modules"

1. Upper module (CaWO₄)
2. Support structure (silicon)
3. Inner veto beaker (silicon)
4. Inner veto wafer (silicon)
5. 3 × 3 target detector array
6. Lower module (Al₂O₃)

**Six callouts.** The only numeral anywhere on panel (f) is the **"3 × 3"** of callout 5, which is an
**array multiplicity (a count), not a dimension** — it carries no unit and no length.

For completeness, the other panels' callouts: (a) B2 Reactor · B1 Reactor · Very Near Site;
(b) VNS room · Basement; (c) Spring decoupling rack · Cryostat support rack · NUCLEUS experimental
setup · Rail system & mechanical structure; (d) Cryostat · External gamma shield (lead) · External
neutron shield (poly-ethylene) · Muon veto · Cryostat volume. None carries a number.

### F.6 FINDING — Fig. 1 is dimensionally silent

> **Determination.** EPJC 86, 29 (2026) (arXiv:2509.03559v1) Figure 1 carries **no scale bar, no
> ruler, no dimension leader, and no numeric dimension callout on any of panels (a)–(f)**. It is an
> unannotated rendered schematic, self-described in its own caption as a "Simplified schematic
> view". The complete set of numerals appearing anywhere on the figure is the six panel letters
> (a)–(f), the reactor labels B1 and B2, and the array multiplicity "3 × 3" on panel (f) — no
> length, no unit, no scale reference. This was established by direct inspection of the frozen
> 1875 × 2613 px image at full resolution across all six panels.

**Consequence.** ROADMAP Phase 8 Success Criterion 1 names Fig. 1(e)/(f) as the evidence route for
the veto-envelope dimensions. **That route is silent.** Any clearance quoted "as read from Fig. 1e/f"
would be fabricated precision (`fp-fig1-fabricated-precision`). The criterion's evidence route must
be **amended in writing** — which Plan 08-03 does — and the dimensions routed instead through
arXiv:2508.02488 (A.1–A.3) and arXiv:1905.10258 (A.13). **This finding is a deliverable, not a
failure:** it is what licenses the amendment.

### F.7 Section-2 dimension inventory — what the paper actually gives

Every numeric length token in §2 and the Fig. 1 caption of `2509.03559v1.txt`, exhaustively
enumerated by regex over the section text (character range 12997–17074 of the frozen file):

| Token | Object |
|---|---|
| `5-cm` | plastic-scintillator muon veto (MV) thickness |
| `5-cm` | low-radioactivity Pb layer thickness |
| `20-cm` | 5% boron-loaded HDPE layer thickness |
| `4-cm` | nearly-4π boron carbide (B₄C) layer thickness |
| `2.5 cm` | COV HPGe crystal thickness |

**That is the complete list. Five entries: four shield-stack thicknesses and one crystal
thickness.** No diameter. No height. No envelope. No cavity. No clearance.

Whole-document confirmation (`2509.03559v1.txt`, entire file):

```bash
grep -c -i -F "envelope"        2509.03559v1.txt   # 0
grep -c -i -F "cavity"          2509.03559v1.txt   # 0
grep -c -i -F "inner diameter"  2509.03559v1.txt   # 0
grep -c -i -F "clearance"       2509.03559v1.txt   # 0
grep -c -F "100 mm"             2509.03559v1.txt   # 0
```

The complete set of `N cm` / `N mm` tokens in the whole paper body is
`{0.5 mm, 1.27 cm, 2 mm, 2.5 cm, 5 cm, 10 mm, 10.16 cm, 20-cm, 20.32-cm, 22.86-cm, 4-cm, 5-cm, 80 cm}`.

> **⚠ Trap flagged for later readers.** `10.16 cm` and `1.27 cm` **do** appear in this paper — in
> §4.2.1, as the **Bonner-sphere Pb shell converter** ("an outer diameter of 10.16 cm and a thickness
> of 1.27 cm"), alongside the 20.32-cm and 22.86-cm sphere diameters. The numerical coincidence with
> the QPD wafer's 10.16 cm edge is **accidental and unrelated**. Likewise `297` and `430` do occur in
> the file, but only inside DOI/URL strings in the bibliography — **not** as NUCLEUS dimensions in
> this paper. Neither may be used as a setup dimension from this source.

### F.8 FINDING — the paper states no COV/IV envelope dimension anywhere

> **Determination.** arXiv:2509.03559v1 (EPJC 86, 29 (2026)) states **no internal envelope, cavity,
> or clearance dimension for the cryogenic outer veto or the inner veto, anywhere in the document**.
> The only COV dimension it gives is a **2.5 cm crystal thickness** (A.10, B.8). The words
> "envelope", "cavity", "inner diameter" and "clearance" do not occur in the text at all. This was
> established by exhaustive enumeration of every `cm`/`mm` numeric token in the frozen file, not by
> a targeted search.

**Confirmed in the version of record.** The same enumeration run against the published EPJC HTML
(`epjc_86_29.txt`) returns the same token set and the same zero counts for
`envelope` / `cavity` / `inner diameter` / `297` / `430` / `100 mm`. **Both versions are silent.**

---

## G. Re-verification pass

All `grep` commands in this document were extracted mechanically and re-run in a single pass
against the frozen files. See `08-01-SUMMARY.md` §"Acceptance tests" for the recorded result.

```bash
# reproduce:
cd data/external/nucleus
grep -h '^grep ' ../../../GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-01-SOURCE-EVIDENCE.md \
  | while IFS= read -r cmd; do eval "$cmd" >/dev/null 2>&1 || echo "FAIL: $cmd"; done
```

---

## H. Uncertainty markers carried forward

**Weakest anchors.**
- The 100 mm COV cylinder diameter comes from arXiv:2508.02488, a **TUM commissioning** paper, not
  from a Chooz drawing, and it is **not in the ROADMAP anchor list** (promoted here, §D).
- The Goupy 2024 thesis — the only genuinely independent third route to the COV cavity — is
  **unobtainable** by any scripted route (`MANIFEST.md` §4), so the rectangular-COV-crystal and
  Cu-support dimensions remain **bounded rather than read**.
- Densities ρ_CaWO₄ = 6.06 and ρ_Al₂O₃ = 3.98 g/cm³ are **assumed standard values**, not quoted from
  any NUCLEUS source. The closures in C.2/C.3 depend on them.

**Unvalidated assumptions.**
- That the TUM commissioning COV crystal and the Chooz COV cap crystals are **the same part**.
  Supported by the shared 2.5 cm / 25 mm thickness and the 10 cm / 100 mm diameter agreement (§D),
  but not read from a Chooz source.
- That the 2026 array totals 6.8 g / 4.5 g divide over exactly **9** crystals per array. The count 9
  comes from the 2019 paper's "3 × 3 array" (A.13/A.14) and is corroborated by the 18-target Chooz
  payload (A.4/A.5, 2 × 9 = 18), but the 2026 paper never says "3 × 3" itself.

**Competing explanations.**
- The 100 mm crystal could be a **commissioning-only part**, with larger cylinders at Chooz. Weakened
  but not excluded by the 2019 paper's independent 10 cm and by the shared 2.5 cm thickness.

**Resolved this pass (previously open).**
- ~~The published EPJC version may differ from arXiv v1.~~ **Retrieved and compared; all four
  load-bearing statements agree word-for-word** (§E.2). Table 4's numeric body remains v1-only.
