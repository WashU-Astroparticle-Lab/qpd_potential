# Known Pitfalls Research — v1.1 Neutron-NR + Detector-Radioactivity Extension

**Domain:** Reactor-CEvNS forward model, extended to neutron-induced nuclear recoils
(cosmic-ray, muon-induced, radiogenic (α,n)/fission) and detector-material radioactivity,
on a thin (2 mm, ~110 g) natural-Ge wafer at the surface, read out by ~10,300 QPD sensors.
**Unit/scale regime:** unified phonon energy scale, **NO ionization quenching**, E_rec ≈ 0.5·E_dep
in the linear regime, 25 kHz non-paralyzable saturation (both trapping designs, Ta→Al and Al→Hf).
**Researched:** 2026-07-21
**Confidence:** HIGH on the quenching, double-counting, thin-detector transport, and saturation
pitfalls (grounded in v1.0 `GPD/CONVENTIONS.md` + published Ge quenching/activation/(α,n)/flux
literature); MEDIUM on absolute normalization details (depend on an as-yet-unspecified QPD
materials/radiopurity budget and housing geometry).

> **Scope note.** This file catalogues pitfalls SPECIFIC to the v1.1 neutron + radiogenic
> extension. The generic CEvNS/muon/response pitfalls (/4π prefactor, (ħc)², GW_th vs GW_e,
> sin²θ_W scheme, 40 µs vs 20 µs) are already locked in `GPD/CONVENTIONS.md` and the v1.0
> `PITFALLS.md`; they are not repeated here except where a v1.1 channel re-triggers them.

> **Phase handles.** v1.1 phases are not yet numbered by the roadmapper. Pitfalls below are
> mapped to *suggested* phase handles the roadmapper can rename/renumber:
> - **P-NSRC** — Neutron source terms & flux normalization (cosmic-ray CRN, muon-induced, radiogenic (α,n)/fission).
> - **P-NTRANS** — Neutron transport & recoil deposition in the thin wafer (single/multi-scatter, escape, kinematics).
> - **P-RAD** — Detector-material radioactivity budget (U/Th/K → γ ER + (α,n) NR, self-shielding, solid angle).
> - **P-COSMO** — Cosmogenic activation history model (68Ge/68Ga, 65Zn, 3H, 60Co; exposure/cooldown).
> - **P-FOLD** — Response folding & reconstructed-energy spectra (25 kHz saturation, E_rec≈0.5·E_dep, band-overlap reporting).

---

## Critical Pitfalls

### Pitfall 1: Quenching confusion — importing keV_ee-quoted rates onto the phonon (keV_nr = E_dep) axis, or "helpfully" applying Lindhard

**What goes wrong:**
Neutron-NR and dark-matter literature quotes nuclear-recoil spectra in one of two axes:
**keV_nr** (true recoil kinetic energy) or **keV_ee** (electron-equivalent = ionization signal
after multiplying the recoil by the Lindhard quenching factor QF). In Ge at CEvNS-relevant
energies the measured QF is small — **QF ≈ 0.15–0.25 over 0.3–8.5 keV_nr** (Lindhard k ≈ 0.157–0.18;
Collar 2021, Bonhomme 2022). This project's observable is the **unified phonon scale = full
deposited energy E_dep with NO quenching**, so:

- A **keV_nr** number is *already* E_dep for a nuclear recoil (up to the few-% Frenkel/defect
  storage that is NR-only in `CONVENTIONS.md §B`). It transfers to the E_dep axis **essentially
  1:1, with NO quenching applied.**
- A **keV_ee** number for an NR background has *already* been multiplied by QF. Treating that
  keV_ee axis as the phonon E_dep axis places the recoil at ~0.2× its true deposited energy —
  shifting the whole NR background **down in energy by ~5×** and, because the differential
  rate carries the Jacobian dE_ee = QF·dE_nr (plus a dQF/dE term), **mis-normalizing dR/dE by
  a factor ~1/QF ≈ 4–6** as well.
- The mirror error: taking a keV_nr spectrum and "applying Lindhard to be safe" **suppresses the
  CEvNS/NR rate by ~5–7×** — exactly the mistake `CONVENTIONS.md §B` forbids ("Applying
  Lindhard/ionization quenching would suppress CEvNS ~5–7× and is physically wrong here").

The RELICS reference numbers in the v1.1 seed todo mix both axes: the CRN and muon-induced NR
rates are in **keV_nr** (`[0.63, 1.36] keV_nr`) → transfer to E_dep directly; the ER background
`[0, 20] keV_ee` is in electron-equivalent. For an *electron* recoil, keV_ee ≈ deposited energy
already (ER quenching ≡ 1 on the ionization scale, and the phonon scale is also full energy), so
ER keV_ee ≈ E_dep — but this is a *coincidence of the ER case*, not a licence to treat keV_ee and
E_dep as interchangeable for the NR channels.

**Why it happens:**
Nearly every transferable Ge background number in the literature is quoted in a quenched or
electron-equivalent axis because real Ge ionization detectors measure charge. Physicists on
autopilot reach for "recoil → apply QF → keV_ee" as a reflex. On a fieldless phonon calorimeter
that reflex is exactly backwards.

**How to avoid:**
- Tag **every** imported NR/ER number with its **native axis (keV_nr vs keV_ee)** at the point
  of transfer, in a provenance table. Never let an untagged number enter the pipeline.
- Transfer NR backgrounds on the **keV_nr axis** and set **E_dep = E_nr** (minus the few-% NR-only
  Frenkel storage). Apply **no** QF.
- If a source gives an NR background only in **keV_ee**, you must **un-quench**: E_nr = E_ee/QF(E_nr)
  solved self-consistently, and rescale the differential rate by the Jacobian dE_nr/dE_ee = 1/QF +
  (E_ee/QF²)(dQF/dE_nr). Document the QF(E) model used (Lindhard k≈0.157–0.18) and its uncertainty.
- Add a guard/assertion in the transfer code mirroring `CONVENTIONS.md §B` FORBIDDEN list: no
  keV_ee/keV_nr mixing, no Lindhard factor on the phonon scale.

**Warning signs:**
- A neutron-NR background peaks ~5× lower in energy than the naive recoil kinematics predict.
- The neutron-NR differential rate is a factor ~4–6 off a same-flux cross-check.
- The CEvNS rate drops by ~5–7× when a "background comparison" branch is enabled (Lindhard leaked in).
- Any code path multiplies a recoil energy by a number in the 0.1–0.3 range labelled "quenching."

**Phase to address:** **P-NSRC** (tag axes at import) and **P-NTRANS** (set E_dep = E_nr, no QF);
guard enforced project-wide, mirrored from `CONVENTIONS.md §B`.

---

### Pitfall 2: Muon–neutron double counting — re-counting the same muons already in the v1.0 direct-ionization channel

**What goes wrong:**
v1.0 already models the through-going cosmic muon as a **direct ionization deposit**
(⟨dE/dx⟩ ≈ 1.370 MeV·cm²·g⁻¹ ≈ 7.3 MeV/cm × chord length, with straggling; `CONVENTIONS.md §G`).
Muon-induced fast neutrons are produced by the **same muon population**. Two distinct
double-counting errors are possible:

1. **Energy double-count within an event.** Attributing part of the muon's energy loss to
   "neutron production" *and* still counting the full ionization deposit. The spallation-neutron
   energy is a tiny, separate sink; the neutron carries its energy *away* from the muon track. The
   muon direct deposit and the neutron-induced recoil are **two independent deposits**, never one
   summed deposit.
2. **Rate/acceptance double-count.** Normalizing the muon-induced-neutron rate as "a fraction of
   the direct-muon events already in the model." This is wrong because the two channels have
   **different geometric acceptance**: a muon that spalls a neutron in the surrounding
   rock/floor/housing and **never crosses the 2 mm wafer** contributes a neutron-NR but **zero**
   direct deposit. Conversely most wafer-crossing muons produce no wafer-reaching neutron. The
   channels overlap only partially.

**Why it happens:**
The neutron channel is genuinely a *secondary* of an already-modeled primary, so it feels like it
should be bookkept "inside" the muon channel. Muon-induced neutron yields are also usually quoted
per muon per g/cm² of *converter material* (e.g., (3–6)×10⁻³ n/muon/(g/cm²) in lead; Kluck 2015),
inviting a naive "multiply the modeled muon rate by a yield" that ignores where the converter is
and where the neutron goes.

**How to avoid:**
- Treat the muon-induced-neutron channel as a **fully independent source term** feeding the same
  neutron-transport stage as cosmic-ray and radiogenic neutrons (P-NTRANS), **not** as a modifier
  of the v1.0 muon deposit.
- Normalize it as: (surface muon flux) × (neutron yield per muon per g/cm², **for the actual
  converter** — wafer Ge is a negligible converter at 2 mm; the floor/housing/rock dominate) ×
  (neutron transport probability to the wafer) × (recoil deposition). The parent-muon's own
  direct deposit is counted **only** when that muon also crosses the wafer, exactly as in v1.0 —
  no change to the v1.0 muon channel.
- Keep the two channels as **separate labelled contributions** to dR/dE_dep so their sum is
  auditable and neither is silently folded into the other.

**Warning signs:**
- The muon-induced-neutron NR rate scales rigidly as a fixed fraction of the v1.0 muon deposit rate.
- Turning on the neutron channel changes the *direct* muon spectrum (it must not).
- The muon-induced-neutron rate ignores the surrounding-material converter mass and depends only
  on wafer-crossing muons (it should be dominated by neutrons made *outside* the wafer).

**Phase to address:** **P-NSRC** (independent source-term normalization) with an explicit
"does not modify the v1.0 muon channel" invariant checked in **P-FOLD**.

---

### Pitfall 3: Single-scatter / full-absorption assumptions in a 2 mm wafer — neutrons mostly escape after one recoil

**What goes wrong:**
Fast-neutron transport intuition is calibrated on **thick** detectors (kg–tonne, cm–dm), where
neutrons multiple-scatter and can thermalize. In a **2 mm** Ge wafer the opposite regime holds.
With Ge number density n = 4.41×10²² cm⁻³ and a fast-neutron elastic cross section σ ≈ 3–7 b, the
**mean free path is λ ≈ 3–8 cm ≫ 2 mm**. Consequences:

- **Interaction probability per crossing is only ~3–6%** — most neutrons pass straight through
  depositing nothing.
- **Conditional on interacting, the neutron overwhelmingly single-scatters and then escapes**
  (P(second scatter) ~ 0.1–0.4%). There is **no thermalization and no full-energy absorption** in
  2 mm.
- Each elastic scatter deposits only a **kinematic fraction** of the neutron energy: the maximum
  Ge elastic recoil is **4A/(A+1)² ≈ 5.4% of E_n**, sampled from the angular distribution — **not**
  the full neutron energy.

Two opposite errors follow: (a) **depositing the full neutron energy** (thick-target /
full-absorption assumption) grossly over-counts the per-neutron deposit; (b) blindly reusing a
**single-scatter recoil spectrum with multiples vetoed** (standard in thick-detector NR analyses)
mis-states the deposited-energy spectrum for the rare multi-site events — on the phonon scale
there is **no position resolution and no multi-site veto**, so the ~0.1–0.4% of events that do
double-scatter have their two recoils **summed into one calorimetric bucket** (a small high-energy
tail), rather than being discarded.

**Why it happens:**
Neutron-background templates are almost all developed for large low-background detectors where
multiple scattering, thermalization, and multi-site vetoes are central. Porting those templates to
a wafer without redoing the transport regime is the trap.

**How to avoid:**
- Work in the **thin-target single-scatter regime**: per interacting neutron, sample **one**
  elastic recoil from the Ge angular distribution (occasionally two, summed); do **not** deposit
  the full neutron energy and do **not** assume thermalization.
- Use the interaction probability P ≈ 1 − exp(−n σ(E_n) t), t = 0.2 cm, with energy-dependent
  σ(E_n) from ENDF/JEFF (not a single constant), for the absolute normalization of deposited
  events. Most of the incident neutron flux escapes.
- On the phonon scale, **sum** multi-site recoils within one resolving-time window into a single
  E_dep (do not veto them); verify the multiple-scatter fraction is the expected ≲1% so the tail
  is a controlled, not dominant, feature.

**Warning signs:**
- Per-neutron deposited energy approaches the incident neutron energy (should cap near ~5% of E_n).
- The neutron-NR spectrum extends to MeV-scale recoils from MeV neutrons (kinematically forbidden).
- The interaction/efficiency per neutron is order-unity rather than a few percent.
- A "multiple-scatter veto" appears anywhere in the wafer analysis (there is no position handle).

**Phase to address:** **P-NTRANS** (thin-target single-scatter transport + kinematics), with the
multiple-scatter fraction reported as a checked ≲1% number.

---

### Pitfall 4: Self-shielding & solid angle — a thin wafer is optically thin to γ, and absolute normalization needs attenuation × geometry

**What goes wrong:**
Two coupled normalization errors, one internal and one external:

**(a) Ge-bulk γ self-absorption runs *backwards* for a thin wafer.** The instinct "a Ge crystal
self-shields its own gammas" is a *thick*-crystal statement. At 1 MeV the Ge attenuation length is
~3 cm ≫ 2 mm, so the wafer is **optically thin to its own MeV gammas** (interaction probability
~6% over 2 mm) — internal γ lines from decays (e.g., 65Zn 1115 keV, 68Ga annihilation/γ) mostly
**escape**, depositing only a partial Compton edge, **not** a full-energy peak. Assuming
full-energy deposition of internal γ lines **over-counts** those peaks. But the mirror subtlety is
dangerous: **low-energy internal emissions deposit fully.** At ~100 keV the Ge attenuation length
is ~1.6 mm (photoelectric dominates), so K/L-capture X-rays, Auger cascades, and β continua are
**absorbed in the wafer** — e.g., 68Ge/71Ge electron-capture X-rays (~10.4 keV K, ~1.3 keV L) and
the 3H β continuum (18.6 keV endpoint) land **right in the CEvNS band** and deposit their full
energy. So the correct picture is: **internal γ peaks mostly escape (do not count them full-energy),
internal X-rays/Augers/low-E β deposit fully (these are the in-band killers).**

**(b) External/housing sources need attenuation × solid angle, and thin-target interaction.** A γ
from a housing component reaches the wafer with flux ∝ (activity) × (Ω/4π geometric solid angle)
× (self-absorption in the source component) × (attenuation through intervening material), and then
deposits with the **thin-target** probability ~μ(E)·t (~6% at 1 MeV), **not** a thick-detector
full-absorption efficiency. Getting the solid angle wrong (e.g., assuming 4π/isotropic capture),
ignoring self-absorption inside the source part, or using a full-absorption efficiency mis-normalizes
the **absolute rate by large factors**.

**Why it happens:**
"Germanium self-shields" and "full-energy peak efficiency" are ingrained from HPGe γ-spectroscopy
with cm-scale crystals. A 2 mm wafer inverts both. External-source normalization is also
notoriously error-prone because solid angle and attenuation multiply into order-of-magnitude swings.

**How to avoid:**
- For internal decays, deposit **γ lines with the thin-target escape-corrected fraction** (most
  MeV γ energy escapes) but deposit **X-rays/Augers/low-E β in full**; treat the low-energy,
  fully-absorbed emissions as the in-band signal-mimicking component.
- For external/housing sources, build the normalization explicitly as
  activity × (Ω/4π) × source-self-absorption × path attenuation × wafer thin-target interaction
  (μ(E)·t), with each factor auditable. Do **not** use a full-absorption detector efficiency.
- Sanity-check absolute rates against RELICS's detector-radioactivity ER magnitude
  (~3.1×10⁻¹ kg⁻¹day⁻¹keV⁻¹ dominant ER) **only after** correcting for their shielding/geometry
  vs our unshielded thin wafer — not as a direct transfer (see Pitfall 7).

**Warning signs:**
- Internal γ lines appear as sharp full-energy peaks in E_dep (should be suppressed Compton continua).
- The predicted rate is insensitive to source-to-wafer distance or housing thickness (solid
  angle/attenuation not wired in).
- A "full-energy peak efficiency" or "self-shielding factor >1" appears for the 2 mm wafer.

**Phase to address:** **P-RAD** (internal + external radioactivity normalization, self-absorption,
solid angle), feeding E_dep templates to **P-FOLD**.

---

### Pitfall 5: Cosmogenic activation history-dependence — quoting saturation activity instead of the as-deployed, isotope-specific activity

**What goes wrong:**
Cosmogenic isotope activities are **not** a single material constant — they depend on the
**exposure time above ground** and the **cooldown time** before operation:
A(t) = R·N_target·[1 − exp(−λ t_exp)]·exp(−λ t_cool), where R is the production rate and λ the
decay constant. Quoting the **saturation activity** R·N (the t_exp → ∞ limit) when the crystal has
only been exposed for months **over-states** short-lived isotopes; forgetting cooldown decay
**over-states** them if the design assumes shielded/underground storage before running. Because
each isotope has its own half-life, **a single "as-deployed" snapshot cannot be used for all of
them**:

- Sea-level Ge production rates (CDMSlite, Amman 2018): **3H ≈ 74 atoms/kg/day, 65Zn ≈ 17,
  68Ge ≈ 30** (with large spreads); ~90% of production is neutron-induced.
- Half-lives: **68Ge 271 d** (→ 68Ga, then in secular equilibrium), **65Zn 244 d**, **3H 12.3 yr**,
  **60Co 5.27 yr** (Cu/steel housing), **55Fe 2.74 yr**.
- For a **permanently-surface** detector run continuously above ground (this project), 68Ge and
  65Zn reach **secular equilibrium (saturate)** on ~1-yr timescales, but **3H (12.3 yr) never
  saturates** on realistic exposures — its activity **grows ~linearly** with exposure time. So the
  3H in-band β background depends directly on how long the wafer has sat at the surface.

**Why it happens:**
Activation numbers are most often tabulated as production rates or saturation activities for
convenience, and underground experiments (which cool down for years) have different bookkeeping
than a continuously-surface detector. Grabbing a saturation number is the path of least resistance.

**How to avoid:**
- State an explicit **exposure/cooldown scenario** (t_exp above ground, t_cool if any) and compute
  each isotope's activity with its own λ — never a blanket saturation value.
- For this surface, continuously-operating detector: treat 68Ge/65Zn as saturated, but carry **3H
  as exposure-time-dependent** (a stated t_exp, with sensitivity to it). Flag 3H (β endpoint
  18.6 keV) and the 68Ge/71Ge EC X-rays (~1.3/10.4 keV) as the **in-band** cosmogenic components.
- Because production is neutron-dominated and the surface neutron flux is ~10⁶× underground, do
  **not** import underground/shielded activation rates (see Pitfall 7).

**Warning signs:**
- A single "saturation activity" is used for 3H alongside 68Ge/65Zn.
- The cosmogenic background is independent of the stated surface-exposure time.
- Activation rates are quoted from an underground/deep-storage reference for a surface detector.

**Phase to address:** **P-COSMO** (isotope-specific A(t) with explicit exposure/cooldown scenario).

---

### Pitfall 6: (α,n) yield material dependence — a generic yield is a trap; the QPD stack's low-Z content sets everything

**What goes wrong:**
Radiogenic (α,n) neutron production depends **very strongly on the light-element content** of the
material the α stops in, because the α range is short (~tens of µm) so only low-Z nuclei within
that range contribute. Using a **single generic yield per ppb U/Th** across the whole QPD stack is
wrong by large factors: αs stopping in **pure Ge** produce almost no neutrons (few accessible
light isotopes, high thresholds), whereas αs in **oxides/fluorides/light-element films** (SiO₂ or
Al₂O₃ substrate, Al/Ta/Hf sensor films, wirebonds, adhesives) produce far more. The (α,n) yield is
also sensitive to the **spatial distribution of contaminants** and, for **thin films**, to whether
the α **stops in the film or escapes** it before producing a neutron (Westerdale 2017; NeuCBOT /
SOURCES-4C both flag this microphysical sensitivity).

**Why it happens:**
It is tempting to fold all U/Th contamination into one bulk (α,n) number. The short α range makes
that physically meaningless — the yield is a per-material, per-microstructure quantity.

**How to avoid:**
- Compute (α,n) **per material** with the actual U/Th siting in each component of the QPD stack
  (Ge crystal, substrate, sensor films, wirebonds, housing), using **NeuCBOT** and/or **SOURCES-4C**
  with the real elemental composition — never a generic bulk yield.
- Account for **thin-film α escape**: a µm-scale sensor film may not stop the α, so the neutron
  yield is set by the substrate the α actually stops in.
- Pair each (α,n) source with a **spontaneous-fission** neutron term (238U SF) from the same U
  contamination; report both.
- State the assumed U/Th assay per material as an explicit input with its uncertainty (this is a
  materials/radiopurity budget assumption, flagged MEDIUM confidence until an assay exists).

**Warning signs:**
- One (α,n) yield-per-ppb is applied to the whole detector regardless of composition.
- The (α,n) rate is dominated by α stopping in pure Ge (should be small there).
- Thin sensor films are treated as full α absorbers.

**Phase to address:** **P-RAD** (per-material (α,n)+SF neutron source terms into P-NTRANS).

---

### Pitfall 7: Surface vs underground flux confusion — importing shielded/deep numbers into an unshielded surface deployment

**What goes wrong:**
This detector is **unshielded at the surface**. Underground/shielded neutron and muon fluxes are
**orders of magnitude lower**: deep-site neutron fluxes are ~10⁶× below the surface, muon fluxes
~10⁵–10⁶× below. The RELICS reference numbers in the v1.1 seed are **post-shielding residuals**
(after a 5 m water roof + 4π active veto) — e.g., the CRN residual (6.0±0.6)×10⁻² kg⁻¹day⁻¹ in
[0.63, 1.36] keV_nr. **Importing such a residual as the unshielded surface rate under-counts by
orders of magnitude.** The correct surface inputs are the **raw sea-level fluxes**:

- **Cosmic-ray neutrons:** Gordon (2004) sea-level spectrum, integral ~3.6×10⁻³ cm⁻²s⁻¹ above
  10 MeV (NYC, mid solar modulation); use the full meV–GeV Gordon parametrization, and note CRY
  under-predicts the >10 MeV tail and must be normalized to Gordon.
- **Muons:** I_v ≈ 70 m⁻²s⁻¹sr⁻¹ vertical (`CONVENTIONS.md §G`), already the surface value in v1.0.
- **Cosmogenic activation:** a **surface-rate** process (neutron-dominated) — surface activation
  ≫ underground.

The reverse error (using surface fluxes where a shielded number is meant) also corrupts
cross-checks against RELICS.

**Why it happens:**
Most CEvNS/DM background literature is written for shielded, deep experiments; their headline
numbers are residuals after heavy mitigation. Surface, unshielded operation is unusual and its
raw fluxes are much larger. Numbers get transferred without their **depth + shielding provenance**.

**How to avoid:**
- Tag **every** imported neutron/γ/muon flux and background rate with its **(depth, shielding)
  provenance**; never mix a shielded residual with an unshielded surface flux.
- Use raw **surface** fluxes (Gordon neutrons, sea-level muons) with **no shielding factor** for
  the baseline; treat any RELICS number as a **shielded cross-check**, back-corrected for their
  water roof + veto, not a direct transfer.
- Where the seed asks whether the flagship "CEvNS reconstructs to tens of eV" framing survives,
  the surface (not underground) NR background level is the correct comparator — expect it far above
  the RELICS residual.

**Warning signs:**
- A background rate matches a RELICS/underground residual to order unity (should be much larger
  unshielded).
- A "shielding suppression factor" appears with no shield in the geometry.
- Neutron flux inputs carry no depth/shielding label.

**Phase to address:** **P-NSRC** (surface flux normalization with provenance tags), enforced in
**P-FOLD** band-overlap comparisons.

---

### Pitfall 8: Reporting deposited-energy-only spectra — MeV neutron/γ deposits saturate the 25 kHz readout and reconstruct at E_rec ≈ 0.5·E_dep, exactly like muons

**What goes wrong:**
MeV-scale neutron-recoil and γ deposits produce large phonon signals that drive the per-sensor
tunneling rate **above 25 kHz**, entering the **non-paralyzable saturation** plateau
(m = Γ/(1+Γτ_d), 1/τ_d = 25 kHz; `CONVENTIONS.md §F`) — **the same saturation the v1.0 muons
already exhibit**. In the linear regime E_rec ≈ 0.5·E_dep, and the full response matrix
R(E_rec|E_dep) compresses high deposits toward the saturation ceiling. Reporting a
**deposited-energy-only** dR/dE_dep for the new neutron/γ channels and comparing it to the CEvNS
**reconstructed** spectrum is an apples-to-oranges error: it (a) ignores the ~0.5× reconstruction
scale, (b) ignores saturation compression of high-energy deposits, and (c) misplaces the
band-overlap with the CEvNS ROI.

Because the phonon scale has **no NR/ER discrimination and no fiducial/position handle**, the
signal-mimicking overlap **must be evaluated in E_rec after folding**: a neutron recoil depositing
~1 keV lands at ~0.5 keV E_rec, **indistinguishable** from a 1 keV CEvNS recoil; and saturating
MeV deposits get pulled down toward the ceiling and can **leak into the ROI from above**.

**Why it happens:**
Neutron/γ background templates are naturally produced in deposited (true) energy, and it is easy to
stop there. The v1.0 pipeline's whole point — folding every channel through the same
saturation+reconstruction response — must be re-applied to each new channel, not skipped.

**How to avoid:**
- Fold **every** new channel (cosmic/muon-induced/radiogenic neutron-NR, intrinsic γ ER, (α,n) NR,
  cosmogenic β/X-ray) through the **same** R(E_rec|E_dep) response matrix used in v1.0, for **both**
  designs (Ta→Al, Al→Hf), under the **non-paralyzable** 25 kHz convention.
- Report **reconstructed-energy** spectra as the deliverable; deposited-energy spectra are
  intermediate only (the v1.0 paper's convention of overlaying deposited/true is fine as an
  auxiliary, but the comparison axis is E_rec).
- Evaluate each channel's **CEvNS-band overlap in E_rec**, explicitly, since there is no NR/ER
  discrimination — including high-E deposits that saturate and leak downward.
- Respect the project memory floor: **do not display spectra below 10 eV** (grid-floor/binding
  artifact territory).

**Warning signs:**
- A neutron/γ background is plotted on a deposited-energy axis next to the reconstructed CEvNS
  spectrum.
- MeV deposits appear at MeV E_rec (should be compressed by saturation, not linear).
- Band-overlap fractions are computed on E_dep rather than E_rec.
- The two designs give identical folded spectra (the response differs per design).

**Phase to address:** **P-FOLD** (response folding + reconstructed-energy deliverables + E_rec
band-overlap), reusing the v1.0 `response.py` / `response_matrix.py` pipeline.

---

## Approximation Shortcuts

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
| -------- | ----------------- | -------------- | --------------- |
| Apply Lindhard QF to put NR backgrounds on a "detector" axis | Matches most literature axes | Wrong scale/normalization by ~5×; violates `CONVENTIONS.md §B` | **Never** on the phonon scale |
| Deposit full neutron energy per interacting neutron | Trivial energy bookkeeping | Over-counts deposit ~20× (max recoil 5.4% of E_n); wrong spectrum | **Never** for the thin wafer |
| Single constant neutron cross section for σ(E_n) | Fast normalization | Mis-normalizes interaction probability across the fast-neutron band | Order-of-magnitude scoping only |
| Treat muon-induced neutrons as a fixed fraction of modeled muon deposits | One-line coupling | Double-counts / wrong acceptance (Pitfall 2) | **Never**; keep source terms independent |
| Full-energy γ absorption / HPGe peak efficiency for the 2 mm wafer | Reuses spectroscopy intuition | Over-counts internal γ peaks; wrong external normalization (Pitfall 4) | **Never**; wafer is optically thin to MeV γ |
| Generic (α,n) yield per ppb U/Th across the whole stack | Avoids per-material assay | Wrong by large factors from low-Z dependence (Pitfall 6) | Rough upper bound only, flagged as such |
| Saturation activity for all cosmogenic isotopes | Single number per isotope | Over-states 3H (never saturates); ignores exposure history (Pitfall 5) | 68Ge/65Zn on a continuously-surface detector only |
| Import RELICS/underground residual as the surface rate | Ready-made number | Under-counts by orders of magnitude (Pitfall 7) | Shielded cross-check only, back-corrected |
| Report deposited-energy-only spectra | Skips folding | Ignores 0.5× scale + 25 kHz saturation; wrong band overlap (Pitfall 8) | Intermediate/auxiliary plots only |

## Convention Traps

| Convention Issue | Common Mistake | Correct Approach |
| ---------------- | -------------- | ---------------- |
| keV_nr vs keV_ee axis of a transferred NR number | Treating keV_ee as the phonon E_dep axis (recoil placed ~5× too low, dR/dE off ~1/QF) | Transfer NR on keV_nr = E_nr = E_dep (no QF); un-quench any keV_ee-quoted NR with the Jacobian |
| "Quenching factor" on a phonon calorimeter | Multiplying recoils by QF≈0.15–0.25 "to be safe" | No QF on the phonon scale; QF only used to *un-quench* keV_ee imports |
| NR recoil energy scale | Depositing full neutron energy | Cap at kinematic recoil ≤ 5.4% of E_n; sample the angular distribution |
| Muon-induced neutron normalization | Per-muon yield tied to wafer-crossing muons only | Normalize to surrounding-converter mass and transport; independent of the v1.0 muon deposit acceptance |
| Ge "self-shielding" | Assuming the crystal absorbs its own γ (thick-crystal reflex) | 2 mm is optically thin to MeV γ (λ~3 cm): peaks escape, only low-E X-ray/β deposit fully |
| Cosmogenic activity | Saturation activity for all isotopes | Isotope-specific A(t) with exposure/cooldown; 3H exposure-time-dependent |
| Flux provenance | Mixing shielded/underground residuals with surface fluxes | Tag every flux with (depth, shielding); surface baseline uses raw Gordon/sea-level fluxes |
| Reconstruction axis | Comparing E_dep backgrounds to E_rec CEvNS | Fold every channel to E_rec through R(E_rec|E_dep); compare in E_rec |

## Numerical Traps

| Trap | Symptoms | Prevention | When It Breaks |
| ---- | -------- | ---------- | -------------- |
| Thick-target neutron transport in a thin wafer | Per-neutron deposit ~ E_n; interaction prob ~ order unity | Thin-target single-scatter model; P≈nσt~3–6% | 2 mm wafer, fast neutrons (λ~3–8 cm) |
| Multiple-scatter veto reused on the phonon scale | Multi-site events discarded | Sum multi-site recoils into one E_dep (~0.1–0.4% tail) | No position/NR-ER handle in QPD wafer |
| Constant σ(E_n) | Wrong energy-dependence of interaction probability | Use ENDF/JEFF σ(E_n) across the fast band + resonances | Broad neutron spectra (meV–GeV) |
| Full-energy γ peak deposition | Sharp internal peaks in E_dep | Escape-correct MeV γ; deposit only low-E X-ray/Auger/β fully | 2 mm wafer, MeV γ |
| Saturation ignored for MeV deposits | E_rec grows linearly to MeV | Apply non-paralyzable 25 kHz + R matrix to every channel | Peak Γ > 25 kHz (MeV-scale deposits) |
| Displaying spectra below 10 eV | Rising counts at few-eV E_rec | Enforce 10 eV display floor (project memory) | Grid-floor/binding-artifact region |

## Interpretation Mistakes

| Mistake | Risk | Prevention |
| ------- | ---- | ---------- |
| Reading a keV_ee-quoted NR background as if on the phonon E_dep axis | NR background shifted ~5× low and mis-normalized; wrong ROI overlap conclusion | Axis-provenance tags; un-quench keV_ee imports |
| Concluding neutron-NR is negligible from an underground/shielded residual | Under-states the dominant surface NR background; false "CEvNS clean" claim | Use surface fluxes; RELICS only as back-corrected cross-check |
| Treating deposited-energy band overlap as the physical overlap | Wrong signal/background separation on an axis the detector never measures | Evaluate overlap in E_rec after folding both designs |
| Assuming NR/ER discrimination suppresses these backgrounds | Over-optimistic ROI; the phonon scale has NO discrimination | State explicitly: every channel lands undiscriminated on the E_rec axis |
| Quoting one cosmogenic snapshot for all isotopes | 3H (in-band β) mis-stated; exposure dependence hidden | Isotope-specific A(t); carry 3H exposure sensitivity |

## Publication Pitfalls

| Pitfall | Impact | Better Approach |
| ------- | ------ | --------------- |
| Comparing our surface, unshielded rates to RELICS residuals without noting their 5 m water roof + veto | Reviewer flags an apples-to-oranges background comparison | State shielding/depth provenance in every comparison; back-correct or label clearly |
| Reporting neutron/γ backgrounds in deposited energy only | Inconsistent with the E_rec CEvNS deliverable; not reproducible on the observable axis | Report E_rec spectra for both designs; deposited energy auxiliary only |
| Not stating the exposure/cooldown scenario behind cosmogenic activities | Cosmogenic numbers non-reproducible; 3H ambiguous | State t_exp, t_cool, half-lives, production rates explicitly |
| Presenting an (α,n) rate without the per-material assay assumptions | Yield unreproducible; hides the low-Z sensitivity | Tabulate U/Th per material + tool (NeuCBOT/SOURCES) used |
| Implying the phonon scale discriminates NR from ER | Overstates background rejection | Explicitly state no discrimination; overlaps quoted in E_rec |

## "Looks Correct But Is Not" Checklist

- [ ] **Transferred NR background:** often missing the axis tag — verify it is keV_nr (→ E_dep, no QF), and that no keV_ee number was placed on the phonon axis.
- [ ] **Neutron deposit per interaction:** often set to full E_n — verify it caps at ≤5.4% of E_n and comes from the angular distribution.
- [ ] **Neutron interaction rate:** often order unity — verify P ≈ nσ(E_n)t ~ 3–6% per crossing (λ~3–8 cm ≫ 2 mm).
- [ ] **Muon-induced neutron channel:** often coupled to the v1.0 muon deposit — verify it is an independent source term and does not modify the direct muon spectrum.
- [ ] **Internal γ lines:** often deposited full-energy — verify MeV γ peaks are escape-suppressed while low-E X-ray/Auger/β are deposited fully.
- [ ] **External source normalization:** often missing solid angle or attenuation — verify activity × (Ω/4π) × self-absorption × path atten × thin-target μt.
- [ ] **Cosmogenic 3H:** often quoted at saturation — verify exposure-time-dependent A(t) with the stated surface scenario.
- [ ] **(α,n) yield:** often generic — verify per-material composition + thin-film α-escape handling.
- [ ] **Flux inputs:** often unlabelled — verify each carries (depth, shielding) provenance; surface baseline uses Gordon/sea-level with no shield.
- [ ] **Final spectra:** often on E_dep — verify every channel is folded to E_rec through R for both designs under non-paralyzable 25 kHz, and nothing is displayed below 10 eV.

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
| ------- | ------------- | -------------- |
| keV_ee imported as phonon E_dep | MEDIUM | Re-tag the source axis; un-quench with QF(E) + Jacobian; re-fold; re-evaluate ROI overlap |
| Muon–neutron double count | LOW | Decouple the neutron source term from the muon channel; renormalize to converter mass; confirm muon spectrum unchanged |
| Full-absorption / thick-target neutron transport | MEDIUM | Switch to thin-target single-scatter; recompute interaction prob and recoil kinematics; re-fold |
| Full-energy internal γ peaks | LOW | Apply thin-wafer escape correction; keep only low-E fully-absorbed emissions in-band; re-fold |
| Generic (α,n) yield | MEDIUM | Recompute per-material with NeuCBOT/SOURCES + stated assay; add SF term |
| Saturation activity for 3H | LOW | Replace with exposure-dependent A(t); re-quote with scenario |
| Underground residual used as surface rate | MEDIUM | Replace with raw surface flux (Gordon/sea-level); demote RELICS to cross-check |
| Deposited-energy-only deliverable | LOW | Fold every channel through R to E_rec for both designs; re-plot with 10 eV floor |

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase (suggested handle) | Verification |
| ------- | ----------------------------------- | ------------ |
| 1. Quenching confusion (keV_nr vs keV_ee) | P-NSRC (tag axes) + P-NTRANS (E_dep=E_nr, no QF) | Provenance table lists native axis of every imported number; guard rejects keV_ee/keV_nr mixing and any Lindhard factor on the phonon scale |
| 2. Muon–neutron double counting | P-NSRC (independent source term) | v1.0 muon spectrum byte-identical with neutron channel on/off; neutron rate normalized to surrounding-converter mass, not wafer-crossing muons |
| 3. Thin-wafer multiple scattering / escape | P-NTRANS (single-scatter transport) | Per-neutron deposit ≤ 5.4% E_n; interaction prob ~3–6%; multi-scatter fraction ≲1% reported |
| 4. Self-shielding & solid angle | P-RAD (internal + external normalization) | Internal MeV γ escape-suppressed; external rate = activity×(Ω/4π)×atten×μt; distance/thickness sensitivity present |
| 5. Cosmogenic history-dependence | P-COSMO (isotope-specific A(t)) | Explicit t_exp/t_cool scenario; 3H exposure-dependent; per-isotope half-lives applied |
| 6. (α,n) material dependence | P-RAD (per-material (α,n)+SF) | Yields computed per material with NeuCBOT/SOURCES; thin-film α-escape handled; assay stated |
| 7. Surface vs underground flux | P-NSRC (surface flux + provenance) | Every flux tagged (depth, shielding); surface baseline uses Gordon/sea-level with no shield; RELICS only back-corrected |
| 8. Deposited-only spectra / saturation | P-FOLD (response folding to E_rec) | Every channel folded through R for both designs under non-paralyzable 25 kHz; overlaps in E_rec; no display below 10 eV |

## Sources

- v1.0 project convention lock: `GPD/CONVENTIONS.md` (§B unified phonon scale/no quenching, §E ε≈0.5, §F 25 kHz non-paralyzable, §G symbol registry) — authoritative internal reference.
- v1.1 seed: `GPD/todos/pending/2026-07-22-add-relics-class-backgrounds-to-forward-model-next-milestone.md`; RELICS design study Chang Cai et al., **PRD 110, 072011 (2024)** (same 3 GW, 25 m reactor configuration; background channel taxonomy and post-shield residuals).
- **Ge quenching / Lindhard:** Collar et al., *Germanium response to sub-keV nuclear recoils*, **Phys. Rev. D 103, 122003 (2021)**; Bonhomme et al., *Direct measurement of the ionization quenching factor of nuclear recoils in germanium*, **EPJC 82, 815 (2022)** [arXiv:2202.03754] (QF≈0.15–0.25 over 0.3–8.5 keV_nr, k≈0.157–0.18); 88Y/Be photoneutron measurement (k=0.179±0.001), OSTI 1423260.
- **Muon-induced neutrons:** H. Kluck, *Production Yield of Muon-Induced Neutrons in Lead* (Springer Theses, 2015); muon-induced neutrons in lead/copper at shallow depth, NIM/Astropart. Phys.; Mei & Hime, *Muon-induced background study for underground laboratories*, **Phys. Rev. D 73, 053004 (2006)** [astro-ph/0512125] (depth dependence, yield scaling).
- **Neutron cross sections / transport:** ENDF/JEFF Ge elastic cross sections (~3–7 b fast); fast-neutron scattering from Ge (OSTI 4765768); CDMS Ge neutron-interaction benchmark (hep.umn.edu/cdms). Mean-free-path and kinematics computed in this survey (λ≈3–8 cm, max recoil 4A/(A+1)²≈5.4%).
- **Cosmogenic activation of Ge:** Amman et al. / CDMSlite, *Production rate measurement of tritium and other cosmogenic isotopes in Germanium*, **Astropart. Phys. 104, 1 (2019)** [arXiv:1806.07043] (3H≈74, 65Zn≈17, 68Ge≈30 atoms/kg/day; ~90% neutron-induced); cosmogenic-activation review [arXiv:1708.07449]; shallow-depth activation [arXiv:2301.12970].
- **(α,n) yields:** Westerdale & Meyers, *Radiogenic neutron yield calculations for low-background experiments* (NeuCBOT), **NIM A 875, 57 (2017)** [arXiv:1702.02465]; SOURCES-4C; (α,n) yield review, **J. Phys. G (2024)** — strong low-Z / microstructure dependence.
- **Surface neutron flux:** Gordon et al., *Measurement of the flux and energy spectrum of cosmic-ray induced neutrons on the ground*, **IEEE Trans. Nucl. Sci. 51, 3427 (2004)** (sea-level spectrum, ~3.6×10⁻³ cm⁻²s⁻¹ >10 MeV, NYC); CRY generator (normalize to Gordon).
- **γ attenuation in Ge:** NIST XCOM mass attenuation coefficients (μ/ρ≈0.061 cm²/g at 1 MeV → λ≈3 cm; ~1.6 mm at 100 keV) — computed in this survey for the thin-wafer optical-thinness argument.

---

_Known pitfalls research for: v1.1 neutron-NR + detector-radioactivity extension of the QPD-Ge CEvNS forward model (thin surface wafer, unified phonon scale, no quenching)_
_Researched: 2026-07-21_
