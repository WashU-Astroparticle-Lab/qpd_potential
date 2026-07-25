# Known Pitfalls Research — v2.0 NUCLEUS-VNS Relocation + Sub-eV Extension

**Domain:** Adopting another collaboration's published, shielded, *measured-and-simulated* residual
background environment (NUCLEUS at the Chooz Very-Near-Site) for a **different target material,
different detector mass, and different geometry** (a single ~110 g, 4″×4″×2 mm Ge wafer on a
unified phonon scale, ~10,300 QPDs on one face), plus **extending every spectrum two decades below
the v1.0/v1.1 validated floor, down to 100 meV**.
**Researched:** 2026-07-22
**Confidence:** **HIGH** on the unit/normalization, veto-transferability, neutron target-scaling,
and LEE-omission pitfalls (all grounded in verbatim numbers from NUCLEUS arXiv:2509.03559 /
EPJC 10.1140/epjc/s10052-025-15168-9 and in this repo's own frozen Phase-7 artifacts).
**MEDIUM** on the sub-eV phonon-regime boundary (the physics literature is solid but no
CEvNS-specific sub-eV Ge calculation was located). **LOW/UNRESOLVED** on one specific internal
inconsistency in NUCLEUS Table 5 (see Pitfall 2), which must be closed by reading the rendered PDF.

> **Scope note.** This file catalogues pitfalls SPECIFIC to v2.0. It does **not** repeat the v1.0
> conventions lock (`GPD/CONVENTIONS.md` §B/§E/§F/§G) or the v1.1 catalogue (keV_ee↔keV_nr,
> Lindhard-on-phonon-scale, muon↔neutron double counting, thin-wafer γ escape, cosmogenic A(t),
> per-material (α,n), deposited-vs-reconstructed axis). Those remain in force; the archived v1.1
> file is at `GPD/milestones/` / git history. Where a v2.0 channel re-triggers one of them it is
> flagged by name only.
>
> **Bias direction is annotated.** Every pitfall carries **[S/B↑]** (a flattering error — the most
> dangerous kind for this milestone, whose headline is an uncomfortable S/B ≈ 0.65–1.2),
> **[S/B↓]**, or **[S/B?]**.

> **Suggested phase handles** (v2.0 phases are not yet numbered; the roadmapper may rename):
> - **P-ENV** — VNS environment adoption: transcription, units, provenance, duty cycle, flux lock.
> - **P-VETO** — Shield/veto transferability: what rejection survives a 110 g wafer; geometry re-derivation.
> - **P-TGT** — Ge target re-fold: neutron NR target scaling, capture channel, γ-ER re-fold.
> - **P-SUBEV** — Sub-eV extension: validity floor, nuclear-data floor, phonon-regime boundary.
> - **P-SB** — S/B assembly, systematics, LEE statement, publication framing.

---

## Verified anchor numbers (transcribe from here, not from memory)

All from NUCLEUS **arXiv:2509.03559** (EPJC 2026), text read directly this run.

| Quantity | Value | Where |
| --- | --- | --- |
| ν̄ flux at VNS, both cores at nominal 4.25 GW_th | **2.1 × 10¹² cm⁻² s⁻¹** | §2 |
| Overburden | **2.9 ± 0.1 m w.e.** (cosmic wheel); **2.92 ± 0.01 m w.e.** (Geant4) | §4 |
| Target payload | CaWO₄ **6.8 g**, Al₂O₃ **4.5 g**, 10 g total (3×3 arrays) | §2 |
| Surface muon flux used | 1.90 × 10⁻² cm⁻² s⁻¹, **25 %** unc. | Table 4 |
| Surface neutron flux used (Gordon) | 1.34 × 10⁻² cm⁻² s⁻¹, **30 %** unc. | Table 4 |
| Ambient γ flux at VNS | 5.03 cm⁻² s⁻¹, **20 %** unc. | Table 4 |
| Material radioactivity | see their Table 3, **30 %** unc. | Table 4 |
| B₄C internal shield | ²³²Th series **240 ± 30 Bq/kg** | Table 3 |
| CaWO₄ intrinsic | ²¹⁰Pb **0.174 ± 0.006 mBq/kg** | Table 3 |
| Total residual, CaWO₄, 10–100 eV | **~250 d⁻¹ kg⁻¹ keV⁻¹** | abstract |
| Total rejection power | **10²–10³** | §5.3 / conclusions |
| MV+COV muon rejection | **> 99.8 %** of the **muon-INDUCED** backgrounds in the CEvNS RoI | §5.2.1 |
| COV extra neutron rejection | **factor 5** **[F5-b]** — the COV anti-coincidence, at a **1 keV_ee** COV threshold | §5.2.1 |
| COV threshold sensitivity | 1 → 10 keV_ee degrades neutron rejection **~20 %** (the sensitivity of **[F5-b]**, not an independent factor) | §5.2.1 |
| Unshielded neutron rate in RoI | **10⁴–10⁵ d⁻¹ kg⁻¹ keV⁻¹** | §5.2.1 |
| Reactor operating cycle | **100 %** and "more realistic **80 %**" both quoted | Table 5 caption |
| S/B band, 1 keV_ee COV threshold, 10–100 eV | **[0.9 – 1.5] at 68 % CL** | §5.3 / Fig. 12 |
| VNS **absolute neutron flux measurement** | **MISSING** — explicitly stated as a limiting unknown | conclusions |
| Geant4 sub-keV physics-list reliability | "another **major question mark**" | conclusions |
| LEE | "**overwhelming**"; "seems **not tied to particle-induced backgrounds** but rather to fundamental aspects in the design of their respective detection setups" | §1, conclusions |

---

> ### ⚠ PHASE-8 CORRECTION 1 — "factor 5" is THREE different statements. Never quote the bare number.
>
> **Issued:** Phase 8 (P-VETO), Plan 08-04, **2026-07-22**.
> **Source:** verbatim quotes from `GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-01-SOURCE-EVIDENCE.md`
> §B.3/§B.4/§B.5, each reproduced from the frozen `data/external/nucleus/2509.03559v1.txt`
> by a recorded `grep -o -F` command. Classified in `GPD/analysis/VETO-TAXONOMY.md`.
>
> **What was wrong here:** this file previously carried a bare "COV factor ~5" entry and repeated
> the bare number in several checklist and table rows. **Section 5.2.1 of arXiv:2509.03559v1
> contains three distinct statements involving a factor 5, describing three different physical
> objects — and one of them is not a rejection factor at all.** Every occurrence of the number in
> this file now carries one of the three labels below.
>
> **[F5-a] — PASSIVE attenuation by the 4 cm B₄C liner.** Tier **L1\***; transferable credit **1.0**.
> > "It turns out to be a very effective complement to the external neutron shield, further
> > suppressing the event rates in the \ceCaWO4 detectors by a factor \sim 5."
> > — §5.2.1, evidence block §B.4
>
> Not an anti-coincidence veto. But its value is quoted for a nearly-4π liner in the direct
> vicinity of a centimetre-scale payload, so it is **payload-geometry-coupled** and does not
> freely transfer. See `GPD/analysis/VETO-TAXONOMY.md` §5 for why it is L1\* and not clean L1.
>
> **[F5-b] — the COV ANTI-COINCIDENCE neutron rejection.** Tier **L2**; transferable credit **1.0**.
> > "While the impact of the MV is marginal, the COV brings a sizable additional reduction of the
> > neutron-induced backgrounds of a factor 5."
> > — §5.2.1, evidence block §B.5
>
> This is the genuine L2 statement, and the one this file's Pitfall 3 is about.
>
> **[F5-c] — a Geant4 MODELLING CONSERVATISM. NOT A REJECTION FACTOR.** No credit; nothing to
> transfer.
> > "For the case of atmospheric neutrons, a crude but conservative approximation scaled down all
> > deposited energies in the COV and the MV volumes by a factor 5 and 2 respectively, to take
> > into account their quenching to neutron-induced nuclear recoils [70, 71, 72]."
> > — §5.2.1, evidence block §B.3
>
> This is a downscaling applied to **simulated deposited energies inside the COV and MV volumes**.
> It **reduces** the credited veto response in their Monte Carlo. It is not a background-rejection
> factor in any sense.
>
> **The concrete failure mode, observed in this project.** During the Phase-8 research pass an LLM
> summarizer asked for "factor 5" in §5.2.1 returned **[F5-c]**, the modelling conservatism. Had
> that been carried forward, a Monte Carlo caveat would have been silently converted into a
> claimed veto factor. **The bare number must never be quoted without its sentence.**

---

**Table 5 (their units: milli-counts per day, mcpd), as extracted:**

| Source | CaWO₄ 10–100 eV | CaWO₄ 0.1–1 keV | Al₂O₃ 10–100 eV | Al₂O₃ 0.1–1 keV |
| --- | --- | --- | --- | --- |
| Atm. muons | < 14 | < 18 | < 11 | < 23 |
| Atm. neutrons | 131 ± 6 | 305 ± 8 | 48 ± 4 | 168 ± 6 |
| Env. gamma rays | 6 ± 3 | 60 ± 11 | < 3 | 66 ± 11 |
| Material radioactivity | 7.1 ± 1.1 | 80 ± 5 | 4.3 ± 1.1 | 86 ± 6 |
| **Total** | **144 ± 6** | **445 ± 14** | **52 ± 4** | **320 ± 14** |
| CEνNS signal | 218.2 | 60.7 | 8.4 | – |

> **Extraction caveat (load-bearing).** The Table 5 caption promises CEνNS rates at **both** 100 %
> and 80 % operating cycle, but text extraction returns only one number per column. The CEνNS row
> is therefore **known to be incompletely extracted** and **must be re-read from the rendered PDF**
> before any of it is used. This is itself a live instance of Pitfall 6.

---

## Critical Pitfalls

### Pitfall 1: mcpd → d⁻¹kg⁻¹keV⁻¹ conversion — three independent ways to be wrong by 9×, 11×, or 1.5× **[S/B?]**

**What goes wrong:**
NUCLEUS's decisive background budget (Table 5) is in **milli-counts per day (mcpd)** for a
**specific array mass** and a **specific RoI width**. Everything else in the paper (abstract,
figures, our own pipeline) is in **d⁻¹ kg⁻¹ keV⁻¹**. The conversion is

```
R[d⁻¹kg⁻¹keV⁻¹] = R[mcpd] × 1e-3 / ( m_array[kg] × ΔE_RoI[keV] )
```

with **m = 6.8 g (CaWO₄) / 4.5 g (Al₂O₃)** and **ΔE = 0.09 keV** (10–100 eV) or **0.9 keV**
(0.1–1 keV). Three failure modes, all plausible and all silent:

1. **Per-detector vs per-array mass.** The CaWO₄ payload is a **3×3 array** — nine crystals of
   ~0.75 g each summing to 6.8 g. Dividing by 0.75 g instead of 6.8 g inflates every rate by
   **9.06×**. This is structurally identical to the project's own `fp-billard-norm` incident
   (a 90× geometry/power normalization overshoot).
2. **RoI width rounded to 0.1 keV.** 10–100 eV is **0.09** keV wide, not 0.1 — an **11 %** error,
   comfortably inside the range that looks like "agreement."
3. **Mass mix-up between materials.** 6.8 g vs 4.5 g is a **1.51×** swing; applying the CaWO₄
   divisor to the Al₂O₃ column (or vice versa) silently rescales the *material contrast*, which is
   exactly the quantity v2.0 needs (see Pitfall 4).

**Correct conversions [COMPUTED this run]:** multiply mcpd by **1634** for CaWO₄ 10–100 eV, by
**2469** for Al₂O₃ 10–100 eV, by **163.4** and **246.9** for the respective 0.1–1 keV bands. Then:

| | CaWO₄ 10–100 eV | Al₂O₃ 10–100 eV | CaWO₄ 0.1–1 keV | Al₂O₃ 0.1–1 keV |
| --- | --- | --- | --- | --- |
| Atm. neutrons | **214.1** | **118.5** | **49.8** | **41.5** |
| Env. gammas | 9.8 | < 7.4 | 9.8 | 16.3 |
| Material radioactivity | 11.6 | 10.6 | 13.1 | 21.2 |
| **Total** | **235.3** | **128.4** | **72.7** | **79.0** |

(all in d⁻¹ kg⁻¹ keV⁻¹)

**Why it happens:**
mcpd is an *experiment-facing* unit (how many counts will we actually see this week) and
d⁻¹kg⁻¹keV⁻¹ is a *physics-facing* unit. Papers mix both because both are useful. The array-vs-
crystal mass ambiguity is invisible unless you have read §2.

**How to avoid:**
- One conversion function, `mcpd_to_dru(rate_mcpd, mass_kg, roi_keV)`, used everywhere; masses and
  RoI widths as **named constants with a source citation**, never inline literals.
- **Self-consistency unit test (this is the whole point):** the converted **Total** must reproduce
  the abstract's **~250 d⁻¹kg⁻¹keV⁻¹** for CaWO₄ 10–100 eV. It does: **235.3** [COMPUTED]. If your
  conversion gives 2100 or 26, you used the crystal mass or the wrong RoI width.
- **Second unit test:** the converted Al₂O₃ CEνNS row must reproduce the paper's prose "about
  20 d⁻¹kg⁻¹keV⁻¹". It does: 8.4 mcpd → **20.7** [COMPUTED]. The Al₂O₃ column is therefore the
  *calibrated* column for the conversion recipe; use it to validate the recipe before touching CaWO₄.

**Warning signs:**
- Any adopted rate that is a clean 9×, 11 %, or 1.5× away from an independent estimate.
- The converted total is not within ~10 % of 250 d⁻¹kg⁻¹keV⁻¹.
- Mass or RoI width appears as a bare number in a formula.

**Phase to address:** **P-ENV**, as the first deliverable, before any Ge folding.

---

### Pitfall 2: The CaWO₄ CEνNS number does not close — a live, unresolved factor 1.27 in the very paper we are adopting **[S/B↑ if resolved the wrong way]**

**What goes wrong:**
Apply the *validated* conversion recipe (Pitfall 1) to the CaWO₄ CEνNS row and it **disagrees with
the paper's own prose** [COMPUTED this run]:

- Table 5: **218.2 mcpd** ÷ (6.8 g × 0.09 keV) = **356.5** d⁻¹kg⁻¹keV⁻¹.
- §2 prose: "an average CEνNS detection rate of about **280** … in the CaWO₄ (6.8 g)".
- Ratio **1.27**.

Meanwhile the Al₂O₃ CEνNS entry closes **exactly** (8.4 mcpd → 20.7 vs prose "about 20"), and the
background Total closes acceptably (235 vs abstract "~250"). So the recipe is right and one CaWO₄
number is off.

Two candidate resolutions, **and I could not decide between them from the extracted text**:

- **(a) Duty cycle applied inconsistently in the prose.** 218.2 × 0.8 = 174.6 mcpd → **285.2**
  d⁻¹kg⁻¹keV⁻¹ ≈ "about 280" [COMPUTED]. This fits to 2 %. But the same sentence says the flux is
  quoted "assuming both reactors are running at nominal power" (i.e. 100 %), so the prose would be
  mixing a 100 % flux with an 80 % rate in one sentence.
- **(b) Table 5's CEνNS row was partially lost in text extraction.** The caption promises both
  100 % and 80 % values; only one number per column survives extraction. 218.2 may be the 100 %
  entry with its 80 % partner (174.6) dropped.

**Why this matters, quantitatively.** The S/B you inherit depends on which you take:
Table-5-as-extracted gives 218.2/144 = **1.52**; prose gives 280/250 = **1.12**; the 80 % reading
gives 174.6/144 = **1.21**, which lands in the middle of the paper's own published S/B band
**[0.9–1.5] at 68 % CL** and is therefore the most likely intended value. **Anchoring our Ge
prediction to the 1.52 reading would flatter our own S/B by ~25 %.**

**Why it happens:**
Convenience numbers in prose drift out of sync with tables during revision; duty-cycle factors get
folded into some numbers and not others. The user's own recorded instance — the 2019 NUCLEUS PROSE
quoting "~3 × 10¹² ν̄/cm²/s" against a Fig. 1 normalized at ~1.8–2.1 × 10¹² [USER-ASSERTED,
not independently verified this run] — is the same failure mode in the same collaboration's
earlier paper. The 2026 paper's **2.1 × 10¹²** is [VERIFIED] verbatim.

**How to avoid:**
- **Read Table 5 from the rendered PDF, not from text extraction.** Record every CEνNS entry with
  its duty-cycle label. Do not proceed on the extracted row.
- Adopt **2.1 × 10¹² cm⁻² s⁻¹** (the 2026 value) as the flux, never 3 × 10¹².
- **Declare the duty cycle once, at the top of the pipeline**, and assert that flux and rate carry
  the same one. A rate normalized to 2.1e12 (nominal, 100 %) must **not** later be multiplied by 0.8
  a second time.
- Cross-check any CaWO₄-anchored normalization against the **Al₂O₃** column, which closes cleanly.

**Warning signs:**
- Our Ge CEνNS rate, divided by the adopted CaWO₄ rate, is ~1.27 away from the ~0.5 the project
  expects ("Ge signal per kg ~2× below CaWO₄").
- A duty-cycle factor appears in more than one place in the call graph.
- S/B lands neatly at the optimistic edge of NUCLEUS's own [0.9–1.5] band.

**Phase to address:** **P-ENV** (blocking; nothing downstream is trustworthy until closed).

---

### Pitfall 3: Inheriting a veto rejection factor that is a property of a 6.8 g payload, not of the shield **[S/B↑, large]**

**What goes wrong:**
The headline "10²–10³ rejection" and "~250 d⁻¹kg⁻¹keV⁻¹ residual" are **not** properties of the
NUCLEUS *shield*. They are properties of the shield **plus** a cm-scale cryogenic payload inside a
cryogenic outer veto (COV) of six 2.5 cm HPGe crystals, an inner veto (IV) TES-instrumented holder,
and a 4 cm B₄C liner — all dimensioned for a **~1 cm** object. Specific non-transferable pieces:

1. **COV factor-5 neutron rejection is anti-coincidence** — this is **[F5-b]**, §5.2.1, *not* the
   passive B₄C attenuation **[F5-a]** and *not* the Geant4 modelling conservatism **[F5-c]**; see the
   Phase-8 correction above. It works because a neutron that scatters
   in a gram-scale target then reaches the surrounding HPGe and deposits ≥ **1 keV_ee** there.
   Its efficiency depends on (i) the veto's solid-angle coverage of the target and (ii) the veto
   threshold — NUCLEUS states raising 1 → 10 keV_ee costs **~20 %** of the neutron rejection, and
   that O(10 keV_ee) is what was actually demonstrated in commissioning. A 4″×4″ wafer has a
   **103.23 cm²** face against a **published 2.25 cm²** 3×3 crystal footprint — a ratio of
   **45.9× on the crystal basis**, or **11.5× on the holder basis** if the ~9 cm² project
   holder-scale estimate is used instead (see **Phase-8 correction 2** below; the ratio must never
   be quoted without its basis) — and cannot be surrounded at the same solid angle by the same COV.
   **Adopting "factor 5" [F5-b] is asserting a veto we have not designed.**

2. **The multiplicity / "single cryogenic detector hit" cut vanishes entirely.** NUCLEUS notes this
   cut is "very marginal" *for them* precisely because their gram-scale detectors are small compared
   to the keV–MeV neutron mean free path. Our wafer is a **single monolithic detector**: there is no
   multiplicity handle at all, and a neutron that scatters twice inside the wafer produces **one
   summed deposit** rather than a rejectable coincidence (v1.1 Pitfall 3 still applies).
3. **The IV rejects "surface events and holder-related events"** for a crystal held on three 1 mm
   sapphire spheres. Our wafer is held differently and carries ~10,300 sensor films on one face.
   The IV's rejection is a statement about *their* holder.
4. **The MV+COV > 99.8 % muon rejection** is a geometric coincidence efficiency. It is the most
   likely of the four to transfer approximately (a through-going muon at 2.92 m w.e. is a large,
   well-tagged signal), but it still needs the wafer's own acceptance re-derived — and the v1.0
   muon channel already shows the wafer's chord-length distribution is not a cube's.

**Why it happens:**
"Residual background at the VNS" reads like a site property. It is a *setup* property. The paper's
own conclusions say the rejection "was found to significantly depend on the COV energy threshold" —
i.e. even NUCLEUS treats these as configuration-dependent, not environmental.

> ### ⚠ PHASE-8 CORRECTION 2 — the array footprint. "~9 cm²" is NOT a NUCLEUS number.
>
> **Issued:** Phase 8 (P-VETO), Plan 08-04, **2026-07-22**.
> **Source:** `GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-01-SOURCE-EVIDENCE.md`
> §C.2/§C.3 (mass closures) and §C.6 (wafer closure).
>
> **What was wrong here:** this file carried a **~9 cm²** array footprint marked `[COMPUTED]` and
> propagated an **~11×** wafer/array area ratio from it, with no basis label. The ROADMAP repeats
> the ~9 cm² without even the `[COMPUTED]` marker.
>
> - **Published (crystal basis): 2.25 cm².** The NUCLEUS target array is a 3×3 array of (5 mm)³
>   crystals, so 9 × (0.5 cm)² = **2.25 cm²**. Confirmed **two independent ways** by mass closure
>   in Plan 08-01: from the published 6.8 g CaWO₄ array total the per-crystal edge closes at
>   **4.996 mm** (−0.09%), and from the published 4.5 g Al₂O₃ array total at **5.008 mm** (+0.17%),
>   both against the directly published (5 mm)³ cube.
> - **~9 cm² is a PROJECT holder-scale estimate**, assuming a ~3 cm holder envelope. **It is not a
>   NUCLEUS number and must not be attributed to NUCLEUS.**
> - **Any area ratio must carry a basis label.** Wafer face 103.2256 cm² gives **≈45.9× (crystal
>   basis)** or **≈11.5× (holder basis)** — a factor-four spread that must not be reported as a
>   single number.

**How to avoid:**
- Split the adoption into two **separately citable** layers and never conflate them:
  **(L1) environmental**, which does transfer — the VNS ambient fields *outside* the setup: 2.92
  m w.e. overburden, Table 4 fluxes (muon 1.90e-2, neutron 1.34e-2 surface-normalized, γ 5.03 at
  VNS), radon, primordial activities; and the *passive* attenuation of the external shield (5 cm
  plastic MV, 5 cm Pb, 20 cm 5 %-borated HDPE), which is a bulk-material property.
  **(L2) payload-coupled**, which does **not** transfer — COV factor 5 **[F5-b]**, IV, multiplicity
  cut; and the 4 cm B₄C liner **[F5-a]**, which Phase 8 classifies as its own tier **L1\*** (passive
  but payload-geometry-coupled) rather than as L2. See `GPD/analysis/VETO-TAXONOMY.md`.
- **Default to L2 = 1.0** (no rejection) and treat any credit as an explicit, argued, separately
  reported assumption with its own line in the systematic budget.
- Report the S/B **twice**: with L2 = 1 (honest lower bound) and with an argued L2, and make the
  gap visible. If the headline needs L2, say so.

**Warning signs:**
- A "factor 5" **[F5-a or F5-b]** or "> 99.8 %" appears in our code with no wafer geometry behind
  it. (Enforced from Phase 8 onward by `tests/test_veto_credit.py`.)
- The predicted background is insensitive to the wafer's size or to the veto threshold.
- Our S/B improves when we change *nothing* about the wafer.

**Phase to address:** **P-VETO** (owns the L1/L2 split and the L2-off baseline); **P-SB** enforces
dual reporting.

---

### Pitfall 4: Neutron NR target scaling — the naive flat-box estimate gets the material contrast wrong, and the error direction is not obvious **[S/B↑ or ↓]**

**What goes wrong:**
For elastic scattering with near-isotropic CM angular distribution, `dσ/dT` is flat on
`0 ≤ T ≤ T_max = 4A/(A+1)² · E_n`. A **heavier** nucleus therefore compresses the *same* number of
recoils into a *narrower* window, **raising** the differential rate inside a fixed low-energy RoI.
NUCLEUS states this explicitly: their neutron rate is larger in CaWO₄ than Al₂O₃ because (i) larger
neutron cross section and (ii) "elastic scattering … kinematically produces much smaller recoils in
CaWO₄ than in Al₂O₃". This is why our project's "Ge signal 2× below CaWO₄ but neutron background
only 1.2–1.8× below" is physically sensible — but it also means the S/B is set by a *ratio of
ratios* that a crude model gets badly wrong.

Endpoints [COMPUTED, `4A/(A+1)²`]: **O-16 0.2215**, **Al-27 0.1378**, **Ca-40 0.0952**,
**Ge natural 0.0536** (project Phase-7 frozen value), **W-184 0.0215**.

**The concrete failure.** A flat-in-T, single-scatter estimate with 1 MeV elastic cross sections
weighted by `Σᵢ nᵢ σᵢ / (T_max/E_n)ᵢ` per kg gives CaWO₄/Al₂O₃ ≈ **1.1** in the RoI [COMPUTED, crude
σ values]. NUCLEUS's full Geant4 result is **214.1 / 118.5 = 1.81** [COMPUTED from Table 5]. The
naive model is **~60 % low on a ratio in which most normalization cancels.** Reasons the naive model
fails, all of which apply equally to Ge:

- **The RoI is fed by moderated, not primary, neutrons.** NUCLEUS: the residual RoI rate comes from
  "elastic scattering of **0.001–1 MeV** neutrons off tungsten nuclei", and B₄C works by capturing
  the "≲ 10 keV component". The in-shield neutron spectrum below 1 MeV is a property of *their*
  HDPE + Pb + B₄C arrangement, not of the Gordon surface spectrum.
- **Cross sections in the keV region are resonance-structured**, not the smooth fast-region values.
  Our own frozen artifact has a **natural-Ge elastic peak of 669.1 b at 102.6 eV** (the ⁷³Ge
  resonance, 8533 b at isotope level) against a fast-region median of ~5.08 b — a factor **130**.
- **The contrast is band-dependent.** CaWO₄/Al₂O₃ is **1.81** in 10–100 eV but only
  **49.8/41.5 = 1.20** in 0.1–1 keV [COMPUTED]. Any target-scaling model that produces a
  band-independent ratio has lost the kinematic compression physics.

**Why it happens:**
"Scale the neutron background by A" or "by the cross section" feels dimensionally reasonable.
Both are wrong: the correct scaling is `n σ(E_n) / T_max(A)` folded over the *in-shield* spectrum,
and the T_max factor pulls the opposite way from the mass-density factor.

**How to avoid — an acceptance test the roadmapper should make mandatory:**
1. Build the target-scaling model **material-agnostically** (per-isotope n, σ(E_n) from evaluated
   data, `T_max/E_n` per isotope, flat-box fold over an assumed in-shield φ(E_n)).
2. **Calibrate it on NUCLEUS before pointing it at Ge:** it must reproduce, from the same φ(E_n),
   **both** CaWO₄/Al₂O₃ = **1.81** in 10–100 eV **and** **1.20** in 0.1–1 keV, each to within the
   30 % neutron-flux systematic. Two bands, two materials, four numbers, one free normalization.
3. Only then evaluate Ge. Quote the Ge/CaWO₄ neutron ratio **with** the residual mismatch from
   step 2 folded in as a systematic.
4. Do **not** transfer φ(E_n) from the Gordon surface spectrum; the RoI needs the **moderated**
   spectrum at the target position, which is not published pointwise. If it cannot be obtained,
   say so and treat the Ge neutron background as a *ratio-anchored* estimate with an explicitly
   stated shape assumption — not a first-principles number.

**Also do not forget the channels the flat box omits:**
- **Inelastic scattering** on Ge (⁷²Ge first 2⁺ at 834 keV, ⁷⁴Ge at 596 keV) opens above ~0.6 MeV
  and both removes flux from the elastic channel and produces a γ that deposits in the wafer.
- **Neutron capture-induced recoils.** ⁷³Ge has a very large thermal/resonance capture cross
  section; the de-excitation γ cascade recoils the nucleus by `Σ E_γ²/(2Mc²)`-type kinematics,
  landing at **O(100 eV–1 keV)** — squarely on the CEνNS axis. This is a documented reactor-CEvNS
  background (Zhang et al., arXiv:2212.14148, which finds the spectrum "strongly overlaps the CEνNS
  signal for recoils ≲ 100 eV" in Si or Ge). NUCLEUS's model has no reason to carry it at Ge
  strength, so it does **not** come with the adopted budget.
- **The B₄C ¹⁰B(n,α)⁷Li 478 keV γ line.** NUCLEUS calls it "harmless… efficiently shielded and
  vetoed by the 2.5 cm thick COV HPGe crystals." That is an **L2** statement (Pitfall 3). A 4 cm
  B₄C liner emitting 478 keV γ next to an *unvetoed* 110 g wafer contributes an unrejected Compton
  continuum. This is a background we would **inherit from their shield and then fail to reject**.

**Warning signs:**
- The Ge/CaWO₄ neutron ratio is the same in the 10–100 eV and 0.1–1 keV bands.
- The sub-10 eV neutron NR spectrum is smooth (the ⁷³Ge 102.6 eV resonance maps to recoils up to
  102.6 × 0.0536 = **5.5 eV** [COMPUTED] and must imprint structure there).
- Only elastic scattering appears in the channel list.
- The 478 keV line does not appear anywhere in the wafer's ER budget.

**Phase to address:** **P-TGT** (owns the calibrated scaling model, capture channel, 478 keV line);
φ(E_n) shape assumption owned by **P-ENV**.

---

### Pitfall 5: Extending to 100 meV — free-nucleus recoil kinematics is not valid there, and the nuclear data floor is a free-gas fiction **[S/B↑, and it fabricates the most eye-catching part of the plot]**

**What goes wrong:**
Four independent things break between ~10 eV and 100 meV, and each one, if ignored, *creates*
apparent signal at the bottom of the plot.

**(a) The impulse (free-nucleus) approximation fails.** Ge's Debye temperature is 374 K →
`k_B T_D ≈ 32 meV`; the zone-centre optical phonon is ~**37 meV** [COMPUTED / standard values].
A "100 meV nuclear recoil" is therefore only **~3 phonon quanta**. The free-recoil picture requires
`E_R ≫ ħω_phonon` (conventionally ≳ 10×, i.e. ≳ **0.4 eV** for Ge). Between ~0.4 eV and the phonon
band the correct description is **multiphonon excitation with a Debye–Waller/Lamb–Mössbauer
suppression**, and below the band a large fraction of scatters are **zero-phonon (elastic)** — the
lattice recoils as a whole and **deposits nothing at all**. Treating `E_dep = T` at 100 meV
therefore invents deposits that physically do not occur. Reference framework:
Campbell-Deem, Knapen, Lin & Villarama, *Dark matter direct detection from the single phonon to the
nuclear recoil regime*, **PRD 106, 036019 (2022)** (arXiv:2205.02250), which explicitly bridges the
single-phonon and free-nuclear-recoil regimes; and Campbell-Deem et al., **PRD 101, 036006 (2020)**
for the multiphonon structure factor. **[MEDIUM confidence: these are DM-scattering calculations;
no CEvNS-specific sub-eV Ge calculation was located this run.]**

**(b) The frozen n-Ge cross section is a free-gas, 293.6 K table with no crystal binding.** This
repo's Phase-7 artifact is LANL Lib80x ACE (NJOY 2016.68, **293.6 K**), and its own validation log
records the tell-tale **"low-E free-gas 1/v upturn: 20.6 b @ 1e-4 eV → 8.97 b @ 0.0253 eV"**
[PROJECT-INTERNAL, `GPD/phases/07-scenario-nuclear-data-lock/07-02-SUMMARY.md`]. That upturn is the
free-gas Doppler model of a **room-temperature ideal gas of unbound Ge atoms**, not a mK crystal.
A real Ge crystal has **coherent elastic (Bragg) scattering with a cutoff** at
`λ = 2 d_111 = 2a/√3 = 6.53 Å → E ≈ 1.9 meV` [COMPUTED, a = 5.658 Å], below which coherent elastic
scattering **switches off entirely**. I **could not verify** that any evaluated `S(α,β)` thermal
scattering law exists for germanium in ENDF/B-VIII.0/VIII.1 or the IAEA INDL/TSL library
**[UNVERIFIED — must be checked against the library index in P-SUBEV]**. If none exists, the sub-eV
neutron channel has **no valid evaluated data** and must be reported as such rather than
extrapolated.
- The 0.1 K `.805nc` ACE set is already on disk and should be used wherever line shapes matter, but
  it is still a **free-gas** treatment; a colder free gas is not a crystal.

**(c) Kinematic thresholds silently fall through table floors.** Two distinct cases with opposite
symptoms:
- **CEνNS.** `E_ν,min ≈ √(M T/2)`. For Ge (M = 67.66 GeV): T = 10 eV → **582 keV**; T = 0.1 eV →
  **58 keV** [COMPUTED]. Both are far below the Huber–Mueller tabulation floor and below the
  1.8 MeV IBD threshold. Depending on the interpolator, `Φ(58 keV)` returns 0 (rate collapses),
  raises (good), or **power-law extrapolates** a steeply rising reactor spectrum (rate explodes).
  **The physically correct answer is neither**: because `dσ/dT` is flat in T, the T → 0 limit is a
  **constant plateau**, `dR/dT|_{T→0} = N_targets · (G_F²/4π) Q_w² M · ∫Φ dE`, fed by the whole MeV
  flux. The sub-MeV extension contributes negligibly to the *rate* even though it dominates the
  *integration limit*.
- **Neutrons.** T = 0.1 eV on Ge needs `E_n ≥ 0.1/0.0536 = 1.87 eV` [COMPUTED] — epithermal, inside
  the resonance region, and inside the regime where (b) applies.

**(d) Grid-floor and binding artifacts.** The project already carries a memory rule: **never
display QPD spectra below 10 eV** — grid-floor / binding-artifact territory. **[RETRACTED 2026-07-22 by user decision; recorded here as history, not as a live rule — spectra now run to 100 meV, and below 1 eV deposit the reported observable is a trigger-probability curve. See CONVENTIONS §I and GPD/phases/10-.../10-05-COUNTING-FLOOR.md.]** v2.0 explicitly asks
for 100 meV, i.e. **two decades inside the region that rule was written to exclude.** The rule must
be consciously superseded with an argument, not silently overridden.

**Why it happens:**
"Extend the axis" reads as a plotting change. It is a physics-regime change. Every numerical layer
(flux table, cross-section table, kinematics, response matrix) has a floor, and floors fail
*quietly* — by returning an edge value or a monotone extrapolation — rather than by raising.

**How to avoid — three implementable tests:**
1. **Plateau test (CEνNS).** Assert `dR/dT` is flat to within a few % from 100 meV up to ~10 eV,
   **and** that its value equals the analytic `T→0` plateau computed independently from the frozen
   `∫Φ`. A rise toward low T is an extrapolation artifact; a fall to zero is a table floor.
2. **Floor-guard test (all tables).** Every interpolator must **raise** outside its evaluated range,
   never clamp and never extrapolate. Then run the full 100 meV fold and confirm which tables raise.
   Whatever raises is a real physics gap, to be documented, not silenced.
3. **Validity-floor annotation.** Compute and publish, per channel, the energy below which the model
   is not defended: CEνNS ~ the multiphonon boundary (**~0.4 eV** for Ge, argued from `ħω_max`);
   neutron NR ~ the sub-eV nuclear-data gap. Shade those regions on every figure. Extending the
   *computation* to 100 meV is fine; extending the *claim* is not.

**Warning signs:**
- `dR/dT` rises as T → 0 (nothing physical does this for flat-box CEνNS).
- Any spectrum is exactly zero below a round number (a table floor, not physics).
- The neutron NR spectrum extends below ~1 eV with no `S(α,β)` in the provenance chain.
- The 100 meV bin is the most visually striking feature of the deliverable figure.

**Phase to address:** **P-SUBEV** (owns all four), with the display-floor decision escalated to the
user because it supersedes a standing project memory rule.

---

### Pitfall 6: Digitized-figure and transcribed-table inputs **[S/B?]**

**What goes wrong:**
v2.0 is unusually digitization-heavy: NUCLEUS's Figures 8, 11, 12 carry information (spectral shape
of the residual background, the S/B-vs-COV-threshold band, the moderated neutron shape) that is
**nowhere in the tables**. Documented failure modes, ranked by how likely each is to hit here:

1. **Table extraction silently dropping columns.** Already happened this run: Table 5's CEνNS row
   promises 100 % *and* 80 % duty-cycle values and text extraction returned one number per column
   (Pitfall 2). **[VERIFIED — this is not hypothetical.]**
2. **`E·dΦ/dE` (per-lethargy) vs `dΦ/dE`.** Neutron spectra are conventionally plotted per unit
   lethargy — `Φ(u) = E Φ(E)`, `du = -dE/E` — because a `1/E` moderated spectrum then appears flat.
   The Gordon sea-level spectrum that NUCLEUS normalizes to is standardly presented this way.
   Reading a lethargy plot as `dΦ/dE` misweights by a factor `E`: **six decades of neutron energy →
   a factor 10⁶ tilt** across the spectrum, which at fixed integral looks like a plausible but
   completely wrong shape. Symptom: the moderated region looks flat in your `dΦ/dE`.
3. **Log-axis calibration error.** WebPlotDigitizer-class tools require two calibration points per
   axis; on a log axis, misplacing one by a few pixels rescales *multiplicatively* and the result
   still looks smooth. A 2 % pixel error over 6 decades is a **~1.3×** error.
4. **Reading a curve that is plotted after cuts you did not notice.** NUCLEUS's Fig. 8 panels show
   *successive* shielding/veto stages on the same axes. Digitizing the wrong trace silently imports
   an **L2** rejection (Pitfall 3). The unshielded trace is 10⁴–10⁵ and the final one ~10² — a
   **10²–10³** error available from a single mis-click. **See Phase-8 correction 3 below: the
   Fig. 8 caption itself tells you which panel is which, and Phase 9 must read it before
   digitizing anything.**
5. **Figure-vs-prose disagreement.** The user's recorded NUCLEUS-2019 case (prose ~3e12 vs figure
   ~1.8–2.1e12, a factor 1.6 that overshoots their own figure by ~50 % when folded)
   [USER-ASSERTED] and the Pitfall-2 CaWO₄ discrepancy [VERIFIED] are the same failure.

> ### ⚠ PHASE-8 CORRECTION 3 (CROSS-PHASE HANDOFF TO **P-ENV** / Phase 9) — Fig. 8 carries a passive-only family AND an all-vetoes trace on the same axes.
>
> **Issued:** Phase 8 (P-VETO), Plan 08-04, **2026-07-22**.
> **Source:** the Fig. 8 caption of arXiv:2509.03559v1, quoted verbatim below from the frozen
> `data/external/nucleus/2509.03559v1.txt`. Newly quoted by Plan 08-04 (it is not in the Plan
> 08-01 evidence block); its `grep` command is recorded in `GPD/analysis/VETO-TAXONOMY.md` §7 as
> `Q-fig8` and was re-run in that pass.
>
> **Caption evidence — the panels are labelled, so trace selection is a decision, not a guess:**
>
> > "The left panels show the impact of sequentially adding passive shielding layers. The right
> > panels show how using the different veto detectors complements the passive shields. The
> > “all vetoes” selection criteria apply all possible anti-coincidence criteria for the rejection
> > of background events."
>
> The same caption states the top panels are the atmospheric-neutron component and the bottom
> panels the atmospheric-muon component, and that each histogram is the rate of events with
> deposited energy between 0 and 1 keV **in the CaWO₄ array of target detectors**.
>
> **Instruction for Phase 9 (P-ENV, CALC-11/CALC-12).** If Phase 9 wants a **fluence** — an
> incident field to fold through the wafer's own response — it must digitize a trace from the
> **left (passive-only) family**. Reading a post-veto curve as pre-veto would import an **L2**
> credit through the digitization: the same forbidden proxy `fp-veto-credit-transfer` arriving by
> a different route, and one that no code review of the veto module would catch because no veto
> factor would ever appear in the code. Record the **panel and trace label** on the digitized CSV's
> provenance header, as this file's Pitfall 6 already requires, and state explicitly which cut
> stage the trace corresponds to.
>
> **Consequence if a post-veto trace is used anyway:** the inverted object is not φ_post but a
> **veto-survival-weighted** φ_post, and it transfers only under the condition that the wafer has
> the same veto acceptance — which Phase 8 has determined it does not (every L1\* and L2 credit is
> 1.0; `GPD/analysis/VETO-TAXONOMY.md`). ROADMAP Phase 9 Success Criterion 3 already requires this
> pre-vs-post determination to be made and recorded; this correction supplies the caption evidence
> that makes it decidable.


**How to avoid:**
- **Every digitized curve gets a closure test against a number printed in text or table.**
  Integrate the digitized Fig. 11 residual spectrum over 10–100 eV and require **235 ± 25**
  d⁻¹kg⁻¹keV⁻¹ (Pitfall 1). If it does not close, the digitization is wrong — full stop.
- Record, per digitized curve: source figure, **panel and trace label**, which cuts are applied,
  axis type (lin/log), the two calibration points per axis, and the closure-test residual. Store as
  a machine-readable provenance header on the CSV, exactly as Phase 7 did for the ACE tables.
- **Unit-tag every ordinate** as `dΦ/dE` or `E·dΦ/dE` at the point of digitization. Convert once,
  in one place. Assert that a `1/E`-like moderated region is *not* flat in `dΦ/dE`.
- Read tables from the **rendered PDF**; treat `pdftotext` output as a hint, never as data.

**Warning signs:**
- A digitized integral disagrees with the printed total by a round factor (E, 10, 100).
- A `dΦ/dE` curve is flat over decades in the epithermal region.
- Any digitized curve without a recorded panel/trace label.

**Phase to address:** **P-ENV** (all environment digitization + closure tests).

---

### Pitfall 7: Quoting S/B without the LEE — the single largest omission, and it is not in the number we are adopting **[S/B↑, order of magnitude]**

**What goes wrong:**
NUCLEUS's "~250 d⁻¹kg⁻¹keV⁻¹" and "S/B ≳ 1" are explicitly a **particle** background budget. The
**low energy excess (LEE)** is *not in it*, and NUCLEUS says so plainly: the LEE "seems **not tied
to particle-induced backgrounds** but rather to fundamental aspects in the design of their
respective detection setups", and their conclusions state "the **overwhelming** LEE background
component still prevents such a study in the O(100 eV) region." The NUCLEUS LEE characterization
paper (arXiv:2603.07687) defines the LEE operationally as
`Rate([100,300] eV) − Rate([1,3] keV)` — i.e. it is *subtracted off* before the particle background
is compared, and its commissioning magnitude in [100,300] eV is reported at the **10⁶
d⁻¹kg⁻¹keV⁻¹** scale, decaying as a power law `R(t) = A (t−t₀)^{−k}` with `k = 0.59 ± 0.06` in days
since 4 K, with **slower cooldowns giving up to an order of magnitude lower initial rates**
[from the paper's own text; retrieved this run].

Three consequences that must be stated, not buried:

1. **Our S/B ≈ 0.65–1.2 is an S/(particle B) upper bound**, on exactly the same footing as
   NUCLEUS's 0.9–1.5. It is not a projected sensitivity.
2. **The LEE is design-specific and therefore cannot be adopted from NUCLEUS in either direction.**
   Their number would not be ours. Our detector is *further* from theirs than theirs is from
   CRESST's: a 110 g wafer with ~10,300 sensor films on one face has far more instrumented
   interface per unit mass than a 6.8 g crystal on three sapphire spheres. Surface-to-mass
   [COMPUTED]: wafer ≈ 215 cm²/0.110 kg ≈ **1950 cm²/kg**; a 6.8 g CaWO₄ cube (ρ ≈ 6.06 g/cm³,
   side ≈ 1.04 cm) ≈ 6.5 cm²/0.0068 kg ≈ **955 cm²/kg** — roughly **2× worse before counting the
   sensor films at all**. If the LEE has any surface/interface component (the leading hypotheses —
   holder stress relaxation, relative interfacial thermal contraction, arXiv:2605.30194 — all do),
   this scaling is adverse for us.
3. **The LEE lives exactly where v2.0 is extending the axis.** It rises steeply below a few hundred
   eV. Pushing the deliverable to 100 meV puts the entire new decade of plot inside the region where
   every cryogenic experiment that has looked has found something it cannot explain.

**How to avoid:**
- **Rename the observable.** Report `S/B_particle`, never bare "S/B". Put the LEE in the
  observable's definition, not in a caveat sentence.
- Add a **standing, non-removable figure annotation** on every reconstructed-energy deliverable:
  "particle backgrounds only; LEE not modelled."
- Report the *LEE rate that would erase the signal* as a derived number: for a Ge signal of
  `S` d⁻¹kg⁻¹keV⁻¹ in-band, quote the LEE level `R_LEE = S` at which S/B_total = 0.5. Then compare
  that number to the 10⁶-scale commissioning LEE. This converts an omission into a falsifiable
  requirement on the QPD design and is far more useful than a caveat.
- Do **not** claim the QPD architecture is LEE-free. There is no evidence either way; the honest
  statement is that the LEE is unmeasured for this detector.

**Warning signs:**
- A figure or abstract carries "S/B" without a qualifier.
- Any sentence implying the QPD unified phonon scale avoids the LEE.
- The 100 meV region is presented as physics rather than as extrapolation.

**Phase to address:** **P-SB** (owns the observable definition and the LEE-requirement number);
**P-SUBEV** must not produce a sub-eV figure without the annotation.

---

### Pitfall 8: Systematics and duty cycle — reusing NUCLEUS's central values while dropping their uncertainties **[S/B↑]**

**What goes wrong:**
The adopted environment carries large, **stated** systematics that are easy to leave behind when
only the central numbers are transcribed: **30 %** on the neutron flux, **25 %** on muons, **20 %**
on ambient γ, **30 %** on material radioactivity (their Table 4). NUCLEUS propagates these with a
deliberately conservative **min/max** method (all components scaled up together, then all down),
which is why their S/B band is as wide as **[0.9–1.5]**. Adopting the central 250 and quoting a
tight S/B is not conservative — it is *less* conservative than the source.

Additional, specific traps:

- **The VNS absolute neutron flux has never been measured.** NUCLEUS's conclusions name this as one
  of the two most important missing inputs. Since neutrons **dominate** the RoI (214 of 235
  d⁻¹kg⁻¹keV⁻¹, i.e. **91 %** [COMPUTED]), the *entire* background budget inherits an unmeasured
  normalization. Our Ge number cannot be more certain than that.
- **Geant4 sub-keV reliability is flagged by the authors themselves** as "another major question
  mark". Anything we inherit below ~1 keV inherits that caveat, and v2.0 goes to 100 meV.
- **Duty cycle is not a multiplicative afterthought.** Two cores (B1, B2) at 4.25 GW_th; NUCLEUS
  uses 80 % as "more realistic". But the two cores are at **different baselines**, so "80 %" is a
  time-average over four states (both on, B1 only, B2 only, both off) with different fluxes, and
  the flux is not proportional to the number of running cores. Worse for sensitivity:
  **ON/OFF subtraction is not clean at a two-core site** — a genuine both-off period is rare, so the
  "OFF" sample usually still contains signal from the other core. A projection that assumes a clean
  background measurement from reactor-off data overstates the achievable systematic control.
  (The published two-core reactor experience is that reactor-off residual neutrino rates carry
  large assigned uncertainties — Double Chooz assigns ~30 % to residual ν rates in reactor-off
  periods, arXiv:1305.2734.)
- **Background is not stationary.** Cosmic-ray neutron flux varies with atmospheric pressure and
  solar modulation (NUCLEUS folds this into the 25 %/30 % bands); radon varies seasonally (their
  §4 records 22.1 ± 1.5 vs 11.8 ± 2.1 Bq/m³ in different periods). An ON/OFF difference over months
  is not a pure signal.

**How to avoid:**
- Propagate NUCLEUS's Table 4 uncertainties with the **same min/max method**, so our band is
  directly comparable to their [0.9–1.5]. **Never** quote a Ge S/B tighter than the CaWO₄ S/B band
  it is anchored to.
- **Reproduce their band first.** Our machinery, applied to CaWO₄, must return ≈[0.9–1.5]. If it
  returns [1.3–1.4], the systematics are not wired in.
- State the duty-cycle model explicitly (fraction of live time in each of the four core states, with
  the per-state flux), and declare it once at the top of the pipeline (see Pitfall 2).
- If a sensitivity is quoted at all, state whether it assumes ON/OFF subtraction, and if so what
  fraction of live time is genuinely both-cores-off.

**Warning signs:**
- Our S/B uncertainty is narrower than NUCLEUS's.
- The background systematic is smaller than 30 %.
- A sensitivity curve exists with no stated duty-cycle model.
- "Reactor off" appears as a clean background measurement.

**Phase to address:** **P-SB** (systematics propagation, duty cycle, any sensitivity statement);
flux/uncertainty transcription owned by **P-ENV**.

---

## Approximation Shortcuts

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
| --- | --- | --- | --- |
| Adopt "~250 d⁻¹kg⁻¹keV⁻¹" wholesale as our background | One number, done | Bakes in a CaWO₄ target, a 6.8 g mass, a COV, an IV, and a multiplicity cut we do not have (Pitfalls 1, 3, 4) | Never as a result; acceptable only as an order-of-magnitude sanity band |
| Inherit the COV factor-5 **[F5-b]** neutron rejection | Preserves a good-looking S/B | Asserts a veto we have not designed for a payload **45.9× larger in face area on the crystal basis** (11.5× on the holder basis — see Phase-8 correction 2) | Never without a wafer-specific veto geometry; if used, report L2-off in parallel |
| Scale the neutron background by A or by σ alone | One-line target transfer | Ignores the `1/T_max` compression that pulls the opposite way; wrong by ~60 % on a *ratio* (Pitfall 4) | Never; the calibrated CaWO₄/Al₂O₃ two-band test is cheap |
| Use fast-region σ_el for the sub-keV neutron fold | Smooth, fast | Misses the 669 b @ 102.6 eV ⁷³Ge resonance that feeds recoils up to 5.5 eV | Never below ~10 keV neutron energy |
| Free-gas 293.6 K ACE below 1 eV | Data already frozen | Not a crystal: no Bragg cutoff (~1.9 meV), no bound-atom S(α,β), spurious 1/v rise to 20.6 b | Never for a sub-eV claim; acceptable above ~10 eV neutron energy |
| `E_dep = T` at 100 meV | Keeps one kinematics function | Free-nucleus recoil is invalid at ~3 phonon quanta; zero-phonon scatters deposit nothing (Pitfall 5) | Never below ~0.4 eV as a *claim*; fine as a labelled extrapolation on a shaded axis |
| Power-law extrapolate the reactor ν̄ flux below its table floor | Avoids a raise at T→0 | Reactor spectra rise steeply toward low E; extrapolation fabricates rate | Never; use the flat-box T→0 plateau instead |
| Quote central NUCLEUS values without their 20–30 % systematics | Tight, quotable band | Less conservative than the source paper; S/B looks decided when it is not | Never in a headline |
| Report S/B without "particle-only" | Simpler abstract | Omits the LEE, which is ~10³–10⁴× the particle background in commissioning data | Never |

## Convention Traps

| Convention Issue | Common Mistake | Correct Approach |
| --- | --- | --- |
| mcpd vs d⁻¹kg⁻¹keV⁻¹ | Dividing by the single-crystal mass (0.75 g) instead of the array mass (6.8 g) → 9.06× | `R_dru = R_mcpd × 1e-3 / (m_array × ΔE_RoI)`; validate on the Al₂O₃ column, which closes exactly |
| RoI width | Treating 10–100 eV as 0.1 keV | It is **0.09** keV (11 % error) |
| Duty cycle | Applying 0.8 twice, or mixing a 100 % flux with an 80 % rate in one comparison | Declare once at pipeline top; assert flux and rate carry the same label |
| ν̄ flux at the VNS | Using the 2019 prose "~3×10¹²" | **2.1 × 10¹² cm⁻² s⁻¹** (2026 paper, verified verbatim) |
| Neutron spectrum ordinate | Reading `E·dΦ/dE` (per lethargy) as `dΦ/dE` | Tag at digitization; a moderated `1/E` region must **not** be flat in `dΦ/dE` |
| Veto threshold | Quoting the COV "1 keV" threshold without the `_ee` | It is **1 keV_ee**; the demonstrated value is O(10 keV_ee), which costs ~20 % of the neutron rejection |
| "Background at the VNS" | Treating it as a site property | Split L1 (environmental, transfers) from L2 (payload-coupled, does not) |
| Target-scaling of neutron NR | Scaling by A or by σ | Scale by `n σ(E_n)/T_max(A)` folded over the **in-shield** φ(E_n); check band-dependence |
| "S/B" | Bare ratio | `S/B_particle`; LEE explicitly excluded |

## Numerical Traps

| Trap | Symptoms | Prevention | When It Breaks |
| --- | --- | --- | --- |
| Table interpolator clamps instead of raising at its floor | Spectrum exactly zero, or exactly constant, below a round energy | Every interpolator raises outside its evaluated range; no clamping, no extrapolation | Any T below ~10 eV (CEνNS `E_ν,min` = 582 eV… 58 keV) |
| Power-law extrapolation of a steeply rising flux | `dR/dT` **rises** as T → 0 | Assert the analytic flat-box plateau `dR/dT|_{T→0} = N (G_F²/4π) Q_w² M ∫Φ dE` | T ≲ 10 eV |
| Free-gas 1/v cross section below thermal | σ_el rises to 20.6 b at 1e-4 eV | Recognize as a free-gas artifact; a crystal has a Bragg cutoff at ~1.9 meV | E_n ≲ 1 eV |
| Resonance grid averaged away | Sub-10 eV neutron NR spectrum is smooth | Preserve the 23,155-point union grid; 669 b @ 102.6 eV must imprint below 5.5 eV recoil | Recoils 0.1–10 eV |
| Chord/interaction-probability mismatch between geometries | Neutron rate transfers unchanged between a cube and a wafer | Use `⟨chord⟩ = 4V/S` (wafer **3.85 mm**, i.e. 1.93× the 2 mm thickness; 1.04 cm cube **6.9 mm**, i.e. 0.67× its side) [COMPUTED]; pair crossing rate and path length consistently or work per volume | Any cross-geometry transfer; the two conventions differ by ~3× between cube and wafer |
| Log-axis digitization miscalibration | Smooth curve, wrong by a constant factor | Two calibration points per axis, recorded; closure test against a printed integral | 6-decade log axes |
| Displaying below the 10 eV project floor | Striking rise at the bottom of the plot | Shade the undefended region; escalate the floor decision (it supersedes a standing memory rule) | 100 meV – 10 eV |

## Interpretation Mistakes

| Mistake | Risk | Prevention |
| --- | --- | --- |
| Reading "~250 d⁻¹kg⁻¹keV⁻¹" as a site background | Imports a CaWO₄ target, a 6.8 g mass, and three vetoes we do not have; S/B flattered by an unknown factor | L1/L2 split; L2-off baseline reported alongside |
| Concluding S/B ≈ 1.5 from Table 5's CEνNS row | 25 % flattering error from a duty-cycle/extraction ambiguity | Re-read Table 5 rendered; anchor on the Al₂O₃ column |
| Treating the Ge/CaWO₄ neutron ratio as A-driven | Wrong sign of the kinematic term; ratio wrong by ~60 % | Calibrate on CaWO₄/Al₂O₃ = 1.81 (10–100 eV) **and** 1.20 (0.1–1 keV) before touching Ge |
| Presenting a 100 meV spectrum as physics | Free-nucleus recoil invalid at ~3 phonon quanta; zero-phonon scatters deposit nothing | Shade below ~0.4 eV; label as extrapolation |
| "The unified phonon scale avoids the LEE" | Unsupported; the LEE is design-specific and our surface/mass ratio is ~2× worse | State that the LEE is unmeasured for this detector; quote the LEE level that would erase the signal |
| Assuming reactor-off gives a clean background measurement | Two-core site; genuine both-off periods are rare | State the four-state duty-cycle model; assign a residual-signal uncertainty |
| Inheriting NUCLEUS's central values as if measured | The VNS absolute neutron flux is **unmeasured**, and neutrons are 91 % of the RoI budget | Carry the 30 % band; never quote tighter than the source |

## Publication Pitfalls

| Pitfall | Impact | Better Approach |
| --- | --- | --- |
| "We adopt the NUCLEUS background" | Referee (plausibly a NUCLEUS author) will ask which vetoes we assumed | State L1/L2 explicitly; show the L2-off baseline |
| Quoting S/B without "particle-only" | Overclaim; NUCLEUS itself calls the LEE "overwhelming" | `S/B_particle`, plus the LEE level that would erase the signal |
| A tighter uncertainty band than the source paper | Immediately falsifiable | Reproduce [0.9–1.5] on CaWO₄ with our machinery first |
| Plotting to 100 meV without a validity shading | Reads as a claim about a regime where free-nucleus recoil fails | Shade and annotate; cite the multiphonon/nuclear-recoil bridge literature |
| Citing "3×10¹² ν̄/cm²/s" | Contradicts the collaboration's own 2026 value | Cite **2.1 × 10¹²** with the 2026 reference |
| Not stating that the VNS neutron flux is unmeasured | Hides the dominant systematic | Say it, and carry the 30 % band through |
| Presenting the uncomfortable S/B ≈ 0.65–1.2 as a fixed number | Precision beyond validation | Present as a band with the L2 assumption and the LEE omission named |

## "Looks Correct But Is Not" Checklist

- [ ] **Adopted background level:** often missing the mass/RoI provenance — verify the converted CaWO₄ total is **235 ± 25** d⁻¹kg⁻¹keV⁻¹ against the abstract's ~250, and that the Al₂O₃ CEνNS row closes at 20.7 vs prose "about 20".
- [ ] **CEνNS anchor:** often taken from the extracted Table 5 — verify against the **rendered** table with duty-cycle labels; the 1.27 discrepancy must be closed, not averaged over.
- [ ] **Veto credit:** often inherited implicitly — verify the code contains no factor 5 (**[F5-a]** or **[F5-b]**; **[F5-c]** is not a rejection factor and must never be used as one), no > 99.8 %, and no multiplicity cut that is not derived from the wafer's own geometry. Machine-checked by `tests/test_veto_credit.py` from Phase 8 onward.
- [ ] **Neutron target scaling:** often A-scaled — verify the model reproduces **1.81** (10–100 eV) and **1.20** (0.1–1 keV) for CaWO₄/Al₂O₃ from one normalization.
- [ ] **Neutron channel list:** often elastic-only — verify inelastic (⁷⁴Ge 596 keV, ⁷²Ge 834 keV), (n,γ) capture recoils on ⁷³Ge, and the B₄C 478 keV line are each present or explicitly bounded.
- [ ] **Sub-eV cross sections:** often silently free-gas — verify the provenance chain names an `S(α,β)` evaluation for Ge, or records that none exists.
- [ ] **T → 0 CEνNS limit:** often rising or zero — verify `dR/dT` is flat from 100 meV to 10 eV and equals the analytic plateau from the frozen `∫Φ`.
- [ ] **Every digitized curve:** often unlabelled — verify the recorded panel/trace, the cut stage, the axis type, and a closure test against a printed number.
- [ ] **Systematics:** often dropped — verify the Ge S/B band is at least as wide as NUCLEUS's [0.9–1.5], propagated min/max.
- [ ] **Duty cycle:** often applied twice or not at all — verify exactly one application, with a stated four-state core model.
- [ ] **Final figures:** often unqualified — verify "particle backgrounds only; LEE not modelled" appears, and that the sub-0.4 eV region is shaded.

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
| --- | --- | --- |
| mcpd conversion error | LOW | Fix the one conversion function; re-run closure tests against 250 and 20.7 |
| Wrong CEνNS anchor (Pitfall 2) | LOW–MEDIUM | Re-read rendered Table 5; re-normalize; re-quote S/B and its band |
| Inherited L2 veto credit | MEDIUM | Set L2 = 1, re-run, report both; if the headline needed L2, the headline changes |
| Uncalibrated neutron target scaling | MEDIUM | Insert the CaWO₄/Al₂O₃ two-band calibration upstream; refold Ge; propagate the residual as systematic |
| Missing capture / inelastic / 478 keV channels | MEDIUM | Add as separate labelled channels; re-fold to E_rec; re-evaluate in-band overlap |
| Free-gas sub-eV extrapolation | MEDIUM–HIGH | Truncate the neutron channel at the last defended energy and document the omission (the Phase-7 gap-D1 precedent); do not extrapolate σ_el |
| Sub-0.4 eV presented as physics | LOW | Shade and re-caption; keep the computation, retract the claim |
| S/B quoted without LEE | LOW | Rename observable, add annotation, add the LEE-erasure requirement number |
| Systematics dropped | LOW | Re-propagate Table 4 min/max; widen the band; re-verify against [0.9–1.5] |

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase (suggested handle) | Verification |
| --- | --- | --- |
| 1. mcpd → dru conversion (9× / 11 % / 1.5×) | **P-ENV** | Converted CaWO₄ total = 235 vs abstract ~250; Al₂O₃ CEνNS = 20.7 vs prose "about 20" |
| 2. CaWO₄ CEνNS 1.27 discrepancy / duty cycle | **P-ENV** (blocking) | Rendered Table 5 read; every CEνNS entry duty-cycle-labelled; exactly one duty-cycle application in the call graph |
| 3. Payload-coupled veto credit (COV/IV/multiplicity) | **P-VETO** | No factor 5 (**[F5-a]**/**[F5-b]**), > 99.8 %, or multiplicity cut without wafer geometry; L2-off baseline exists and is reported |
| 4. Neutron NR target scaling + missing channels | **P-TGT** | CaWO₄/Al₂O₃ = 1.81 and 1.20 reproduced from one normalization; capture, inelastic, 478 keV present or bounded |
| 5. Sub-eV extension (impulse approx., free-gas data, table floors) | **P-SUBEV** | Plateau test passes; all interpolators raise at their floors; validity floor computed and shaded per channel |
| 6. Digitized-figure inputs | **P-ENV** | Every curve has panel/trace/cut/axis provenance and a passing closure test |
| 7. LEE omission | **P-SB** (+ **P-SUBEV** annotation) | Observable is `S/B_particle`; LEE-erasure level reported; annotation on every deliverable figure |
| 8. Systematics + duty cycle + ON/OFF | **P-SB** | Our machinery reproduces NUCLEUS's [0.9–1.5] on CaWO₄; Ge band not tighter; duty-cycle model stated |

## Sources

**Primary (read directly this run, verbatim numbers):**
- NUCLEUS Collaboration, *Particle background characterization and prediction for the NUCLEUS reactor CEνNS experiment*, **Eur. Phys. J. C** (2026), DOI **10.1140/epjc/s10052-025-15168-9**, **arXiv:2509.03559** — 2.1×10¹² cm⁻²s⁻¹, 2.92 m w.e., Tables 3/4/5, MV+COV > 99.8 % of the muon-**induced** backgrounds, COV factor 5 **[F5-b]** at 1 keV_ee, ~250 d⁻¹kg⁻¹keV⁻¹, S/B [0.9–1.5], unmeasured VNS neutron flux, Geant4 sub-keV caveat, LEE exclusion.
- NUCLEUS Collaboration, *Exploring CEνNS with NUCLEUS at the Chooz Nuclear Power Plant*, **EPJ C 79, 1018 (2019)**, arXiv:**1905.10258** — two 4.25 GW_th cores; NUCLEUS-10g = 3×3 CaWO₄ + 3×3 Al₂O₃. *(Abstract only retrieved this run; the prose-vs-figure flux discrepancy noted in the milestone brief is **[USER-ASSERTED, not independently verified here]**.)*
- NUCLEUS Collaboration, *Characterization of the Low Energy Excess using a NUCLEUS Al₂O₃ detector*, arXiv:**2603.07687** — LEE defined as Rate([100,300] eV) − Rate([1,3] keV); power law `k = 0.59 ± 0.06`; slower cooldown → up to 10× lower initial rate; commissioning [100,300] eV rate at the 10⁶ d⁻¹kg⁻¹keV⁻¹ scale.

**Supporting:**
- *The relative interfacial thermal contraction as a possible origin of the low-energy excess in cryogenic calorimeters*, arXiv:**2605.30194** — surface/interface origin hypothesis (basis for the adverse surface-to-mass scaling argument).
- Biffl, Gevorgian, Harris & Villano, *Neutron capture-induced nuclear recoils as background for CEνNS measurements at reactors*, **PRD 107, 092011 (2023)**, arXiv:**2212.14148** — capture recoils "strongly overlap the CEνNS signal for recoils ≲ 100 eV" in Si/Ge. (Authorship corrected from "Zhang et al." 2026-07-23 against the frozen PDF `data/external/biffl/`; it computes the recoil spectrum with nrCascadeSim.)
- Campbell-Deem, Knapen, Lin & Villarama, *Dark matter direct detection from the single phonon to the nuclear recoil regime*, **PRD 106, 036019 (2022)**, arXiv:**2205.02250**; Campbell-Deem, Cox, Knapen, Lin & Melia, **PRD 101, 036006 (2020)** — multiphonon → free-nuclear-recoil bridge; basis for the ~0.4 eV impulse-approximation boundary.
- Double Chooz, *Rate-Only analysis with reactor-off data*, arXiv:**1305.2734** — reactor-off residual-rate uncertainties at a multi-core site.
- Gordon et al., **IEEE Trans. Nucl. Sci. 51, 3427 (2004)** — sea-level cosmic-ray neutron spectrum (NUCLEUS's neutron normalization; conventionally presented per unit lethargy).
- ENDF/B-VIII.0 (Brown et al., **NDS 148, 1 (2018)**) and the ENDF thermal-scattering (TSL) sublibrary — **germanium `S(α,β)` availability could not be confirmed this run and is an open verification item.**

**Project-internal (read this run):**
- `GPD/phases/07-scenario-nuclear-data-lock/07-02-SUMMARY.md` — frozen natural-Ge σ_el, LANL Lib80x ACE / NJOY 2016.68 / **293.6 K free-gas**, 1.03e-5 eV → 20 MeV, 23,155-point union grid, natural resonance peak **669.1 b at 102.6 eV**, Σ = 0.1646 cm⁻¹, λ = 6.076 cm, P_int(2 mm) = 3.24 %, natural `T_max/E_n` = **0.0536**, the documented low-E free-gas 1/v upturn to 20.6 b, and the 0.1 K `.805nc` set on disk.
- `GPD/state.json` `project_contract.forbidden_proxies` — `fp-deposited-only`, `fp-no-saturation`, `fp-full-absorption`; `decisions` — the `fp-billard-norm` 89.9× normalization incident.
- `GPD/CONVENTIONS.md` §B/§E/§F — unified phonon scale, no quenching, ε ≈ 0.5, 25 kHz non-paralyzable.
- `GPD/MILESTONES.md` (v1.1 superseded entry) — the 10⁴–10⁵ vs ~200 d⁻¹kg⁻¹keV⁻¹ shielding delta; gap-D1 (20 MeV truncation) precedent for honest truncation over extrapolation.

**Arithmetic performed in this survey [COMPUTED]:** all mcpd → d⁻¹kg⁻¹keV⁻¹ conversions; the
CaWO₄/Al₂O₃ neutron ratios 1.81 and 1.20; `4A/(A+1)²` endpoints for O/Al/Ca/W; `E_ν,min = √(MT/2)`
= 582 keV at 10 eV and 58 keV at 100 meV for Ge; Ge Bragg cutoff `2a/√3 = 6.53 Å → 1.9 meV`;
`k_B T_D = 32 meV`; mean chord `4V/S` = 3.85 mm (wafer) and 6.9 mm (1.04 cm cube); surface-to-mass
1950 vs 955 cm²/kg; the 102.6 eV resonance → 5.5 eV maximum Ge recoil.

---

_Known pitfalls research for: v2.0 relocation of the QPD-Ge forward model to the NUCLEUS Chooz
Very-Near-Site behind the NUCLEUS shielding, with sub-eV (100 meV) spectral extension_
_Researched: 2026-07-22_
