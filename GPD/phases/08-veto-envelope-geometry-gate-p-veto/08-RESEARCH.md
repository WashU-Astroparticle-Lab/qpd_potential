# Phase 8: Veto-Envelope Geometry Gate (P-VETO) — Research

**Researched:** 2026-07-22
**Domain:** Low-background cryogenic detector instrumentation / experimental geometry; cosmic-ray muon transport through a thin plate
**Depth:** standard (balanced mode)
**Confidence:** HIGH on the L1/L2 taxonomy and on the multiplicity argument; HIGH on the *direction* of the fit verdict (does not fit); MEDIUM on the numerical clearance

---

## User Constraints (from CONTEXT.md)

No `CONTEXT.md` exists for this phase. No user constraints from `gpd:discuss-phase` — all sub-decisions are at agent's discretion, subject to the binding ROADMAP Phase 8 Success Criteria, `REQUIREMENTS.md` VALD-09, and the milestone-wide forbidden proxies (`fp-veto-credit-transfer` in particular).

Two standing user decisions dated 2026-07-22 are carried in from the contract and are treated as locked:

- **Inherited veto credit defaults to ZERO unless earned by wafer geometry.**
- **If the wafer does not fit: STOP and re-scope with the user.** No reduced veto credit, no invented resized veto.

---

## Active Anchor References

Contract-critical anchors for this phase, with what each actually supplies (verified this pass unless marked otherwise).

| Anchor | What it supplies for Phase 8 | Status this pass |
| --- | --- | --- |
| **NUCLEUS EPJC 86, 29 (2026)**, arXiv:2509.03559 (v1 HTML retrieved) | §2 shield stack + COV/IV description; Fig. 1 panels (a)–(f); §5.1 veto thresholds and the "one and only one target detector" cut; §5.2.1 COV factor 5, MV+COV >99.8%, 1→10 keV threshold cost; §5.2.2 Pb ~50× and COV gamma role | **Retrieved and grep-verified.** Contains **no** internal envelope dimension. |
| **NUCLEUS EPJC 79, 1018 (2019)**, arXiv:1905.10258 (ar5iv retrieved) | Fig. 8 caption "outer veto (3) **with a diameter of 10 cm**"; two 3×3 arrays; Si-wafer IV; (5 mm)³ prototype; 1 m³ passive shield; VNS 24 m² room | **Retrieved and grep-verified.** Journal ref confirmed as **79, 1018** via ref [24] of the 2026 paper. |
| **Goupy 2024 thesis** (NNT 2024UNIP7170, HAL `tel-05298505`) | Expected to hold the rectangular COV crystal dimensions, Cu support and IV beaker geometry | **NOT RETRIEVABLE in this environment.** See "What Was NOT Found". |
| **NUCLEUS commissioning**, arXiv:2508.02488 (Phys. Rev. D) — *not in the roadmap anchor list; added by this research* | **The single most load-bearing geometric source found.** COV crystal 100 mm ⌀ × 25 mm, 1 kg; internal shielding cylinder ⌀ 297 mm; external shield 93×93×86 cm³ with a 430 mm cryostat bore; final Chooz payload = 18 targets + 6 COV + 4 IV detectors; target crystals 5×5×5 mm³ | **Retrieved and grep-verified.** Promote to a Phase 8 anchor. |
| **COV prototype**, Goupy et al., NIM A 1064, 169383 (2024), arXiv:2401.09837 — *added by this research* | Prototype geometry (70 mm ⌀ × 20 mm HPGe, 3 mm Cu housing, PTFE holders) — shows the mounting-overhead scale | Retrieved. Prototype, **not** the final COV. |
| **Wafer geometry** (CONVENTIONS §D, `src/qpd_potential/wafer_geometry.py`) | 10.16 × 10.16 × 0.20 cm, 20.65 cm³, 109.9 g, S = 214.6 cm², diagonal 14.37 cm | In-repo, HIGH |
| **v1.0 Phase 4 muon machinery** (`data/muon_dRdEdep.csv`, frozen) | Gaisser–Guan ⊗ chord ⊗ Landau; integral rate **1.3659 ± 0.0003 Hz**; vertical MPV 1.2323 MeV (mean 1.4585); 10⁹ samples | In-repo, HIGH |

---

## Summary

Phase 8 asks one factual question and one taxonomic question. Both are answerable now, but **not from the source the roadmap names**.

**The factual question (does the wafer fit).** NUCLEUS EPJC 86, 29 (2026) — the paper whose Fig. 1e/f Success Criterion 1 points at — contains **no dimension at all** for the COV/IV internal envelope. I downloaded the paper, converted it to text, and grep'd every numeric `mm`/`cm` token: the only setup dimensions are the 5 cm MV, 5 cm Pb, 20 cm borated HDPE, ~4 cm B₄C, and the **2.5 cm COV crystal thickness**. I then downloaded Fig. 1 itself (1875×2613 px) and inspected it: it is an unannotated artist's schematic titled "Simplified schematic view", with **no scale bar and no dimension callouts on any of panels (a)–(f)**. Success Criterion 1 as literally written is therefore **not satisfiable from that figure**, and any clearance quoted "from Fig. 1e/f" alone would be fabricated precision.

The numbers do exist — in two other NUCLEUS papers. The 2019 paper's Fig. 8 caption states the outer veto has **a diameter of 10 cm**. The 2025 commissioning paper (arXiv:2508.02488) states the COV cylindrical HPGe crystal is **100 mm diameter × 25 mm height, 1 kg** (a self-consistency check: ρ_Ge π (5 cm)² (2.5 cm) = 1043 g ≈ 1 kg ✓), that the internal shielding is a **297 mm** diameter cylinder, and that the final Chooz payload is 18 targets + 6 COV + 4 IV detectors. Combined with the 2026 paper's "two cylindrical and four rectangular 2.5 cm thick HPGe crystals", the COV is a box of four 2.5-cm-thick slabs capped top and bottom by two 10 cm cylinders, so the enclosed cavity is bounded by **≈10.0 − 2×2.5 = 5.0 cm**. Fig. 1(e) pixel-scaled against the 100 mm cylinder gives an inner-detector-module envelope of **≈4 cm**. The wafer needs a cavity with **two orthogonal dimensions ≥ 10.16 cm** — no rotation reduces that, since a 10.16 × 10.16 × 0.20 cm plate has two bounding-box sides ≥ 10.16 cm under every orientation. **The leading determination is a clear no-fit, by roughly a factor of two on the in-plane axis and a factor of ~3 on the diagonal, before any holder, clamp, or Cu-support allowance.** The wafer is in fact wider (101.6 mm) than the *entire outer diameter* of a COV crystal (100 mm).

**The taxonomic question (what transfers).** All the L2 statements are now quotable verbatim with section numbers, and one of them is materially mis-stated in the project's carried-forward literature. §5.2.1 contains **three distinct "factor 5"s**: the B₄C passive layer suppressing rates by ~5, the COV anti-coincidence reducing neutron background by a factor 5, and a Geant4 modelling conservatism that scales down deposited energies in the COV/MV by 5 and 2 for nuclear-recoil quenching. The project must quote the sentence, not the number. Equally important, the "MV+COV reject more than 99.8% of the **muon-induced** backgrounds" claim is about muon-*induced secondaries*, not about tagging through-going muons — which is exactly why a wafer self-veto cannot inherit it: a self-veto tags ~100% of muons that cross the wafer and ~0% of the muon-induced neutrons and bremsstrahlung gammas produced in the surrounding Pb that reach the wafer without the parent muon. That distinction is the whole of Success Criterion 3, and it is the difference between an honest L2-off baseline and `fp-veto-credit-transfer`.

**Net posture for the planner.** Plan Phase 8 as a *source-verified geometry determination plus a written taxonomy*, with the fit arithmetic re-derived in-phase from downloaded source files (never from an LLM summary — see Pitfall 8, where WebFetch got both "99.8 NOT FOUND" and the 2019 journal reference wrong in this very session). Expect the gate to **fail**, and plan the no-fit emission path as a first-class deliverable, not an afterthought.

---

## Mathematical Framework

The phase is geometric and combinatorial, not field-theoretic. Four small formal objects carry the whole argument.

### F1. Orientation-invariant fit lemma (the core of Success Criterion 1)

For a rectangular plate of edges $a \times a \times t$ with $t \ll a$, let $B(R)$ be the axis-aligned bounding box of the plate under rotation $R \in SO(3)$, with sorted side lengths $b_1(R) \ge b_2(R) \ge b_3(R)$.

$$\min_{R \in SO(3)} b_2(R) \;=\; a$$

i.e. **no orientation reduces the requirement that the cavity have two orthogonal free dimensions of at least $a$.** The 2 mm thickness buys clearance in one axis only. Equivalently, the minimum enclosing cylinder of the wafer has diameter

$$D_{\min} = \sqrt{2a^2 + t^2} = \sqrt{2(10.16)^2 + (0.20)^2} = 14.370\ \text{cm}$$

which is the relevant number against a cylindrical COV. This lemma is what forecloses "could we just stand it on edge / tilt it?" — it must be stated explicitly, because "reorientation" is the first thing a referee will ask.

### F2. Clearance / shortfall definition

For cavity dimension $D_i$ and required wafer dimension $W_i$:

$$C_i \equiv D_i - W_i \qquad (C_i < 0 \Rightarrow \text{shortfall of } |C_i|)$$

Report $C$ in cm for: (i) the in-plane axis against the COV cavity, (ii) the diagonal against the COV cylinder diameter, (iii) the in-plane axis against the COV *outer* cylinder diameter (the "even the whole crystal is smaller than the wafer" statement). Quote each with the source of $D_i$.

### F3. Multiplicity rejection with $N$ target channels

NUCLEUS's cut is a conjunction (2026 paper §5.1): *"(i) no hits in any of the veto detectors and (ii) a hit in one and only one of the target detectors."* Part (ii) has rejection power

$$\varepsilon_{\text{mult}} = 1 - P(\text{exactly one of } N \text{ channels above threshold})$$

For NUCLEUS, $N = 18$ (commissioning paper: "18 cryogenic target detectors"). For a **monolithic single-readout wafer, $N = 1$**, hence $P \equiv 1$ and

$$\boxed{\varepsilon_{\text{mult}} = 0 \ \text{identically}}$$

This is not "small" or "marginal" — it is zero by counting, and Success Criterion 4 requires it stated that way rather than absorbed into a lumped factor.

### F4. Wafer self-veto acceptance (Success Criterion 3)

Define, from the wafer's own chord-length⊗Landau deposit distribution:

$$A_{\text{self}}^{\text{direct}}(E_{\text{cut}}) \;=\; \frac{\int_{E_{\text{cut}}}^{\infty} (dR/dE_{\text{dep}})\, dE_{\text{dep}}}{\int_{0}^{\infty} (dR/dE_{\text{dep}})\, dE_{\text{dep}}}$$

= the fraction of muons **that cross the wafer** which the wafer can identify by its own deposit. Its complement $1 - A_{\text{self}}^{\text{direct}}$ is the un-self-taggable crossing fraction.

**This is only half the acceptance, and it is the half that was never the problem.** The class NUCLEUS's MV+COV actually suppresses is muon-*induced* secondaries — neutrons and bremsstrahlung gammas born in the Pb, reaching the target with the parent muon nowhere near it. For those,

$$A_{\text{self}}^{\text{induced}} = 0 \quad \text{(no handle: the parent muon never enters the wafer)}$$

**Both numbers must be reported separately.** Lumping them into one "muon-veto acceptance" is precisely `fp-veto-credit-transfer` wearing a derivation as a disguise.

A third derived quantity is the practical cost of self-veto: the live-time lost to muon-coincident vetoing,

$$f_{\text{dead}} = R_\mu \times \tau_{\text{dead}}, \qquad R_\mu(2.92\ \text{m.w.e.}) = \frac{1.3659\ \text{Hz}}{1.41} = 0.969\ \text{Hz}$$

using the project's carried-forward omnidirectional attenuation factor 1.41 ± 0.02. Caveat to state: the attenuation factor is an *integral-flux* factor; the angular distribution also hardens at depth, which slightly changes the chord distribution. Phase 15 owns the proper re-fold; Phase 8 should use the ratio (attenuation cancels to first order in $A_{\text{self}}$) and flag $f_{\text{dead}}$ as first-order only.

---

## Standard Approaches

This is instrumentation-geometry provenance work, not a calculation with an approximation scheme. The standard method in the low-background community, and the one to follow:

1. **Never scale a figure without an in-figure length anchor of published size.** The accepted practice is to identify an object in the schematic whose dimension is stated in text, measure it in pixels, and propagate the ratio. Here the anchor is the **100 mm COV cylinder** (arXiv:2508.02488). Record the pixel coordinates in the artifact so the measurement is reproducible.
2. **Cross-check every read geometry against an independent physical quantity.** For crystals, mass is the check: $m = \rho V$. Two such checks are available and both pass (see Validation Strategies) — if a read dimension fails its mass check, the read is wrong.
3. **Bound rather than assume when the drawing is schematic.** State an upper bound on the cavity from the enclosing structure (the 297 mm internal shield) and a tighter bound from the enclosing detector (the 100 mm COV cap), and be explicit that the verdict rests on the tighter one.
4. **Separate environmental from configuration-dependent rejection by asking "would this number change if I swapped the payload and nothing else?"** If yes → L2. NUCLEUS themselves treat these as configuration-dependent: §5.2.1 quantifies how the neutron rejection moves with the COV threshold.
5. **For the self-veto acceptance, reuse the frozen spectrum rather than re-running the Monte Carlo.** The v1.0 result is a 10⁹-sample frozen artifact; re-running it introduces avoidable divergence risk for zero physics gain.

### Package / Framework Reuse Decision

**Decision: reuse in-repo modules directly; add one thin bespoke analysis module. No new external package.**

| Need | Decision | Justification |
| --- | --- | --- |
| Chord-length distribution, wafer geometry constants | **Use `src/qpd_potential/wafer_geometry.py` directly** | Already validated (Cauchy 4V/S, chord bounds, projected-area measure); constants match CONVENTIONS §D |
| Muon flux, Landau deposit, dR/dE_dep | **Use the frozen `data/muon_dRdEdep.csv`**; `src/qpd_potential/muon_deposit.py` only for the reproduction check | 10⁹-sample frozen artifact; re-running costs hours and risks silent drift |
| Figure pixel scaling of Fig. 1(e) | **Thin bespoke script using PIL + numpy** (both verified available in this environment) | A GUI digitizer (WebPlotDigitizer etc.) is not scriptable, leaves no provenance trail, and is overkill for measuring two edge-to-edge distances. A 30-line numpy script that records pixel coordinates in the artifact header is strictly better for reproducibility. |
| Geometry fit arithmetic + L1/L2 taxonomy artifact | **New `src/qpd_potential/veto_envelope.py`** (or equivalent), ~150 lines: named constants with source strings, clearance function, `L2_CREDIT = 1.0` sentinel | No package provides "compare a plate to a published cavity". The value is in the *provenance discipline* (every constant carrying its citation), which is a project-specific requirement no library satisfies. |
| CAD / mesh / solid-modelling library | **Reject** | The comparison is three scalars against three scalars. A mesh library adds a dependency and hides the arithmetic. |
| Geant4 / OpenMC / G4CMP | **Reject — forbidden milestone-wide** | ROADMAP Overview: no phase carries an OpenMC/MCNP/Geant4/G4CMP dependency; OpenMC is unbuildable on osx-arm64. Any transport fallback is SIMU-05, follow-up scope. |

**Binding implementation constraint:** the `L2` credit must exist in code as a named constant set to `1.0` with a docstring citing this phase, so that any future reintroduction of a veto factor is a visible, reviewable diff. A factor that lives only in a markdown table will eventually be typed into a formula by someone.

---

## Existing Results to Leverage

### Verbatim source statements — geometry

**arXiv:2509.03559 (EPJC 86, 29 (2026)), §2:**

> "An external shielding first combines a 5-cm thick plastic scintillator-based muon veto (MV) [37] in the outermost part, together with a 5-cm thick layer of low radioactivity Pb and a 20-cm thick layer of 5% boron-loaded high-density polyethylene (HDPE) in the innermost part."

> "It is extended within the cryostat by a so-called internal shielding (see figure 1 (e)), which is housed below the still stage. This internal shielding follows the same layer arrangement as the external shielding, with the addition of a nearly 4π 4-cm thick boron carbide (B₄C) layer to further suppress neutrons reaching the target detectors. It also features a plastic scintillator-based cold muon veto, which was designed to operate at cryogenic temperatures [38]."

> "The COV is an arrangement of two cylindrical and four rectangular 2.5 cm thick HPGe crystals mechanically held within a Cu support structure, operated at O(mK) temperatures and read-out through the ionization channel. It hermetically covers the cryogenic target detectors…"

> "The last piece of the NUCLEUS shielding strategy is the target detector TES-instrumented holder, called inner veto (IV). The main purpose of the IV is to reject surface events and holder-related events."

> "The concept of such an HPGe cryogenic veto system was recently validated, especially showing that a O(10 keV) threshold is within reach when operated in a dry dilution refrigerator [39]."

**arXiv:2509.03559, Fig. 1 caption (complete):**

> "Simplified schematic view of NUCLEUS at the VNS, breaking down the main components of the experiment."

Panel titles read off the figure image directly: **a)** Chooz nuclear power plant; **b)** Very Near Site (VNS); **c)** VNS room; **d)** NUCLEUS experimental setup; **e)** Cryostat volume; **f)** Inner detector modules.
Panel **(e)** callouts: Copper support & thermalization structure · Cold muon veto · Internal gamma shield (lead) · Internal neutron shield (polyethylene) · Vessels (Al or Cu) · Cryogenic outer veto (germanium) · Cryogenic neutron shield (boron carbide) · Inner detector modules.
Panel **(f)** callouts: Upper module (CaWO₄) · Lower module (Al₂O₃) · Support structure (silicon) · Inner veto beaker (silicon) · Inner veto wafer (silicon) · 3 × 3 target detector array.
**No scale bar. No dimension annotation. On any panel.**

**arXiv:1905.10258 (EPJC 79, 1018 (2019)), Fig. 8 caption (verbatim):**

> "3D sketch of the NUCLEUS-10g detector. It consists of three different types of cryogenic calorimeters – two 3×3 arrays of gram-scale cryogenic calorimeters as CEνNS target (1), an inner veto (2) and an outer veto (3) **with a diameter of 10 cm**. The assembly is held mechanically by a non-instrumented support structure (4). The target is operated in anti-coincidence with the inner and the outer veto. See text for details."

**arXiv:2508.02488 (NUCLEUS commissioning at TUM):**

> "…the final NUCLEUS setup at Chooz, which will include **18 target detectors** arranged in an instrumented silicon holder, **6 high-purity germanium detectors** forming the cryogenic outer veto, and an additional boron carbide layer around it." (Fig. 1 caption)

> "The external shielding measures **93 × 93 × 86 cm³** and features a cylindrical opening (**430 mm in diameter**) from the top to accommodate the cryostat."

> "The internal shielding, positioned directly above the cryogenic target detectors, has a cylindrical shape with a **diameter of 297 mm** and is mechanically secured to the cryostat using a bayonet mount."

> "In the scope of the presented commissioning, only one of the six crystals is installed directly above the target detectors. It features a **cylindrical geometry with 100 mm diameter and 25 mm height, and a mass of 1 kg.**"

> "a CaWO₄ single-TES detector, shaped as a **5 × 5 × 5 mm³** cube with a mass of **0.76 g** … and a Al₂O₃ double-TES detector, measuring 5 × 5 × 7.5 mm³, with a mass of 0.75 g"

> "The detectors were secured with **bronze clamps**, while **sapphire spheres** provided thermal and electrical isolation between the detector, holder, and clamps." (mounting overhead)

> "the final configuration at Chooz will use an upgraded system with enough channels to accommodate the 18 cryogenic target detectors, the 6 COV detectors and the **4 inner active veto detectors**."

**arXiv:2401.09837 (COV prototype, NIM A 1064, 169383):** "two cylindrical ~400 g HPGe crystals of 70 mm diameter × 20 mm height"; "housed within **3-mm thick copper boxes** and secured using PTFE (Teflon) holders". *Prototype only — do not substitute for the final COV.*

### Verbatim source statements — rejection (the L2 catalogue)

**arXiv:2509.03559 §5.1 (the selection):**

> "The energy thresholds defining a MV hit, a COV hit, an IV hit and a cryogenic target detector hit were set to **5 MeV, 1 keV, 30 eV and 10 eV**, respectively."

> "…the identification of a CEνNS-like event must meet the combination of all possible anti-coincidence selection criteria, i.e. having (i) **no hits in any of the veto detectors** and (ii) **a hit in one and only one of the target detectors**."

**arXiv:2509.03559 §5.2.1 (all three "factor 5"s, in source order):**

> [modelling conservatism] "For the case of atmospheric neutrons, a crude but conservative approximation **scaled down all deposited energies in the COV and the MV volumes by a factor 5 and 2 respectively, to take into account their quenching to neutron-induced nuclear recoils** [70,71,72]. For muon-induced background, since in the COV, most of the events seen in coincidence with the cryodetectors come from secondary neutrons, a factor 5 down scaling of the energies deposited in the COV is cautiously applied as well."

> [passive B₄C] "A second 4-cm thick [B₄C] layer, which is located within the cryostat in the direct vicinity of the cryogenic detection setup (see figure 1 (e)), captures the low-energy (< 10 keV) component of the surviving neutron flux. It turns out to be a very effective complement to the external neutron shield, **further suppressing the event rates in the CaWO₄ detectors by a factor ~5**."

> [COV anti-coincidence] "While the impact of the MV is marginal, **the COV brings a sizable additional reduction of the neutron-induced backgrounds of a factor 5.**"

> "The COV rejection performances particularly depends on its ability to detect low energy nuclear recoils induced by 10-100 keV neutrons reaching the target detectors… For instance, **raising the COV threshold from 1 [keV] to 10 [keV] degrades the neutron-induced background rejection by approximately 20%.**"

> "Finally, the benefit of applying all vetoes, i.e. (i) using the IV and (ii) **requesting only one cryogenic detector hit** in addition to the MV and COV anti-coincidence selection criteria, is **very marginal**. This result makes sense as the IV and the gram-scale cryogenic target detectors are small compared to the mean free path of keV to MeV neutrons either in Si, CaWO₄ or Al₂O₃ materials."

> "The emission of a 478 keV gamma-ray line following neutron capture on [¹⁰B] is harmless to the cryogenic target detectors, as it is efficiently **shielded and vetoed by the 2.5 cm thick COV HPGe crystals**."

> "Unsurprisingly, the MV was also found to be very efficient. When combined with the COV, they are predicted to **reject more than 99.8% of the muon-induced backgrounds in the CEνNS RoI**, making them a negligible contributor to the total background budget (see section 5.3)."

**arXiv:2509.03559 §5.2.2 (gammas):**

> "A thickness of 5 cm of Pb followed from extensive Geant4 simulation studies. It gives a **factor ~50 reduction** of the event rate in the CaWO₄ target detectors, while the rest of the NUCLEUS setup passive materials … makes an **additional factor ~10 reduction**."

> "The right panel of figure 9 illustrates the effect of the NUCLEUS IV and COV detectors. It particularly points out the **essential role of the COV** in reducing the environmental gamma ray contribution down to sufficiently low levels."

> "**The IV is a very thin detector** (see figure 1 (f)), which makes it insensitive to the interactions of environmental gamma rays. As expected, it does not improve the rejection of this background component."

**Bonus finding, hand-off to Phase 9** (this pass answers a listed open question, at least for Fig. 8): the Fig. 8 caption explicitly separates pre- and post-veto traces —

> "The left panels show the impact of sequentially adding passive shielding layers. The right panels show how using the different veto detectors complements the passive shields. **The 'all vetoes' selection criteria apply all possible anti-coincidence criteria for the rejection of background events.**"

So Fig. 8 carries *both* a passive-only family and an all-veto trace on the same axes — which is exactly the trace-selection trap PITFALLS.md warns about. Phase 9 must digitize the **passive-only** trace if it wants a fluence. Record this in the Phase 8 output as a cross-phase finding; do not let Phase 9 rediscover it.

### In-repo results to reuse verbatim

| Artifact | Content | Use |
| --- | --- | --- |
| `data/muon_dRdEdep.csv` | dR/dE_dep, 0.01 keV → 200 MeV, 80 bins/decade; header: `integral_muon_rate_Hz = 1.3659 +/- 0.0003`, `vertical_chord_MPV_MeV = 1.2323 (mean = 1.4585)`, `n_mc_samples = 1000000000` | Numerator/denominator of $A_{\text{self}}^{\text{direct}}$ |
| `src/qpd_potential/wafer_geometry.py` | `LX=LY=10.16`, `LZ=0.20`, `S_SURFACE=214.6 cm²`, `CHORD_VERTICAL=0.20`, `CHORD_DIAGONAL=14.37`, `cauchy_mean_chord()=4V/S=0.385 cm`, `chord_lengths()`, `projected_area()`, `sample_entry_and_chord()` | Geometry constants and, if a per-chord cut study is wanted, the sampler |
| `src/qpd_potential/muon_deposit.py` | `run_muon_mc()`, `mpv_deposit()`, `shared_energy_grid()` | Reproduction check only |
| `tests/test_muon_geometry.py` | Cauchy invariant, chord bounds, `J_horiz = πI_v/2` surface measure | Regression guard if geometry code is touched |
| `GPD/CONVENTIONS.md` §D | Wafer 20.65 cm³, 109.9 g, ρ_Ge = 5.323 g/cm³ | Source of truth for wafer numbers |

**⚠ Path correction the planner must apply.** `GPD/phases/04-.../04-01-SUMMARY.md` front-matter records deliverable paths `src/muon/deposited_spectrum.py` and `data/muon/muon_dep_spectrum.csv`. **Neither exists in the repository.** The real paths are `src/qpd_potential/muon_deposit.py` (+ `muon_flux.py`, `wafer_geometry.py`) and `data/muon_dRdEdep.csv`. Any plan task that cites the summary's paths will fail at execution.

---

## Don't Re-Derive

| Do not re-derive | Cite instead | Why |
| --- | --- | --- |
| Muon dR/dE_dep and the 1.3659 ± 0.0003 Hz integral rate | `data/muon_dRdEdep.csv` header | Frozen 10⁹-sample v1.0 artifact; VALD-02 passed against PDG within ~15% |
| Vertical-chord MPV 1.2323 MeV / mean 1.4585 MeV | Same | Already validated (MPV < mean) |
| Cauchy mean chord 4V/S = 0.385 cm, diagonal 14.37 cm, S = 214.6 cm² | `wafer_geometry.py` + `tests/test_muon_geometry.py` | Unit-tested |
| Wafer mass/volume 20.65 cm³ / 109.9 g | CONVENTIONS §D | Locked convention |
| Gaisser–Guan parameters P1–P5 | `muon_flux.py` (verified vs arXiv:1509.06176) | Transcribed and validated in Phase 4 |
| The NUCLEUS shield stack description | Quotes above | Verbatim from source |
| Any neutron fluence, deposit spectrum, or φ_post | — | **Phase 9 scope.** Phase 8 must not touch the inversion. |
| Whether Ge is a better or worse target than CaWO₄ | Ge/CaWO₄ same-pipeline ratio 2.31 (v1.0) | Phase 12/13 scope |

---

## Computational Tools

| Tool | Version / location | Role in Phase 8 |
| --- | --- | --- |
| numpy, scipy | in-repo env | Clearance arithmetic, spectrum integration |
| PIL (Pillow) | verified available | Fig. 1(e) pixel measurement |
| pytest | in-repo | Acceptance tests |
| `curl` | verified working from Bash | Source acquisition (see below) |
| WebFetch | **use with distrust** | See Pitfall 8 |

**Source acquisition that is verified to work in this environment** (record the exact commands in the plan so execution is reproducible):

- `https://arxiv.org/html/2509.03559v1` — 398 kB HTML, full text, **works** (note: `…v2` returns 404 even though v2 exists on the abs page; the published EPJC version may differ from v1 and any quote should be labelled `v1`).
- `https://arxiv.org/html/2509.03559v1/Figures/Figure1.png` — 1.66 MB, 1875×2613, **works**.
- `https://ar5iv.labs.arxiv.org/html/1905.10258` — **works** (arXiv native HTML does not exist for 2019 papers).
- `https://arxiv.org/html/2508.02488v1` — **works**.
- `https://arxiv.org/html/2401.09837v1` — **works**.
- `https://api.archives-ouvertes.fr/search/?q=halId_s:tel-05298505&fl=…&wt=json` — **works** (metadata only).
- **HAL full text — does NOT work.** Four routes tried (`theses.hal.science/tel-05298505{,/document,/file/va_Goupy_Chloe.pdf}`, `hal.science/…`, `www.theses.fr/2024UNIP7170.pdf`), all return an identical 12,587-byte Anubis anti-bot proof-of-work challenge page with `content-type: text/html`, including with a browser User-Agent. See "What Was NOT Found".

---

## Validation Strategies

Each check below is a pass/fail the plan can turn into an acceptance test.

| # | Check | Expected | Guards |
| --- | --- | --- | --- |
| V1 | **COV crystal mass closure.** ρ_Ge π (5.0 cm)² (2.5 cm) = 5.323 × 196.35 = **1045 g** vs the published "a mass of 1 kg" | agree within ~5% | That the 100 mm × 25 mm read is correct and refers to Ge |
| V2 | **CaWO₄ array crystal closure.** 6.8 g / 9 = 0.756 g; at ρ = 6.06 g/cm³ → 0.1247 cm³ → edge **4.99 mm** vs published "5 × 5 × 5 mm³, 0.76 g" | agree within ~1% | That the 3×3 array really is (5 mm)³ cubes, hence a **2.25 cm² crystal footprint** |
| V3 | **Al₂O₃ array crystal closure.** 4.5 g / 9 = 0.50 g; at ρ = 3.98 g/cm³ → 0.1256 cm³ → edge **5.01 mm** | agree within ~1% | Same, independently |
| V4 | **Wafer closure.** 10.16 × 10.16 × 0.20 × 5.323 = **109.9 g**, face 103.23 cm², diagonal 14.370 cm | exact | CONVENTIONS §D consistency |
| V5 | **Figure-scaling anchor.** Measure the COV cylinder width and the pink "inner detector modules" box width in Fig. 1(e) in pixels; the cylinder must map to 100 mm | ratio recorded with pixel coords | Fabricated precision (Pitfall 3) |
| V6 | **Frozen muon reproduction.** Integrating `data/muon_dRdEdep.csv` over all E and converting counts/kg/day → Hz with m = 0.1099 kg must return **1.3659 Hz** | ≤1% | That the acceptance denominator is the right normalization |
| V7 | **Acceptance monotonicity and limit.** $A_{\text{self}}^{\text{direct}}(E_{\text{cut}} \to 0) = 1$ exactly; monotone non-increasing in $E_{\text{cut}}$; $\le 1$ everywhere | exact / monotone | Arithmetic slips in the integration |
| V8 | **Multiplicity identity.** A unit test asserting `mult_rejection(N_target_channels=1) == 0.0` and `> 0` for `N=18` | exact | Success Criterion 4 being softened into "small" |
| V9 | **L2 sentinel.** A test asserting the L2 credit constant equals exactly 1.0 and that no `5`, `0.998`, or `0.2` veto factor appears in any code path without a wafer-geometry argument | pass | `fp-veto-credit-transfer` |
| V10 | **Independent-route honesty check.** The 100 mm-cylinder route and the Fig.-1(e) pixel route **share the same anchor** and are therefore *not* independent. The artifact must say so. A genuinely independent third route requires the Goupy thesis. | statement present | Over-claiming corroboration |

**Note on V1–V3:** these are the strongest evidence available that the geometry has been read correctly, because they close a *dimension* against an independently published *mass*. Both pass. That is what licenses treating the 100 mm × 25 mm number as reliable.

---

## Common Pitfalls

### Pitfall 1: The three "factor 5"s of §5.2.1 **[severity: high — misattributed physics]**
The same section states (a) the passive B₄C layer suppresses CaWO₄ rates by ~5, (b) the COV anti-coincidence reduces neutron backgrounds by a factor 5, and (c) a Monte-Carlo conservatism scales COV/MV deposited *energies* down by 5 (and MV by 2) for nuclear-recoil quenching. These are three different physical objects. (a) is passive attenuation (borderline L1, see Pitfall 6), (b) is L2, (c) is not a rejection factor at all.
**Avoid:** quote the sentence with its section number, never the bare number. In this research pass an LLM summarizer returned (c) when asked for "factor 5", which would have silently converted a modelling conservatism into a claimed veto factor.

### Pitfall 2: Reading ">99.8%" as a muon-tagging efficiency **[severity: high — this is the whole of SC3]**
The source says MV+COV "reject more than 99.8% of the **muon-induced** backgrounds in the CEνNS RoI". Muon-induced ≠ through-going. A wafer self-veto tags essentially every muon that crosses it (Δ_p = 1.23 MeV against an eV-scale threshold) and *nothing* of the muon-induced neutron/gamma shower born in the surrounding Pb. Reading 99.8% as a tagging efficiency makes it look ~inheritable. It is not.
**Avoid:** report $A_{\text{self}}^{\text{direct}}$ and $A_{\text{self}}^{\text{induced}}$ as two separate numbers with two separate physical definitions.

### Pitfall 3: Quoting a clearance "from Fig. 1e/f" **[severity: high — fabricated precision]**
Fig. 1 is an artist's schematic titled "Simplified schematic view", with no scale bar and no dimension callout on any panel (verified by direct image inspection at 1875×2613). Success Criterion 1's literal instruction cannot be discharged from that figure alone.
**Avoid:** route the dimensions through arXiv:2508.02488 (100 mm / 297 mm / 430 mm) and arXiv:1905.10258 (10 cm), use Fig. 1(e) only for *relative* scaling against the 100 mm anchor, and state in the deliverable that SC1's named source is silent. Amending the criterion's evidence route is legitimate; quoting a number the figure does not carry is not.

### Pitfall 4: Treating "~9 cm²" as a published NUCLEUS number **[severity: medium — false provenance]**
The published crystal footprint of a 3×3 array of (5 mm)³ cubes is **2.25 cm²** (V2/V3). "~9 cm²" is a holder-scale estimate assuming a ~3 cm envelope; it appears in the project's own literature files marked `[COMPUTED]`, and the ROADMAP repeats it without that marker. The area ratio to the wafer's 103.23 cm² is therefore **11.5×** (holder basis) or **45.9×** (crystal basis) — a factor-4 spread that must not be reported as a single number without saying which basis.
**Avoid:** report both, label the basis, and never attribute 9 cm² to NUCLEUS.

### Pitfall 5: Treating L2-off as "a conservative NUCLEUS" **[severity: medium — mis-framing that will draw a referee]**
§5.2.2 says 5 cm of Pb was chosen as a *trade-off* precisely because the COV compensates for the thin gamma shield. Keeping their L1 shield while dropping their L2 vetoes is not a conservative subset of NUCLEUS — it is a **different and worse configuration** than either NUCLEUS or an independently optimized shield, because nobody would design a 5 cm Pb shield for an unvetoed detector.
**Avoid:** label the baseline "NUCLEUS's shielding without NUCLEUS's vetoes", and say explicitly that it is not the optimum for our payload.

### Pitfall 6: Classifying the 4 cm B₄C liner as clean L1 **[severity: medium — the taxonomy's soft edge]**
Its ~5× is a *passive material* attenuation (L1-flavoured) but is quoted for a nearly-4π liner "in the direct vicinity" of a ~cm object. Its value is geometry-coupled to the very payload size under dispute. The binary L1/L2 split in Success Criterion 2 does not have a slot for this.
**Avoid:** introduce an explicit **L1\*** category — "passive but payload-geometry-coupled" — for the B₄C liner and the internal shielding, defaulting its transferable credit to 1.0 alongside L2 while documenting *why* it is not L2. Do not silently promote it to L1 to make the budget look better.

### Pitfall 7: "Could we reorient it?" **[severity: low — but it will be asked]**
Handled by lemma F1: every orientation of the plate requires two orthogonal cavity dimensions ≥ 10.16 cm.
**Avoid:** state the lemma; do not hand-wave "it's too big in every direction".

### Pitfall 8: Trusting an LLM page-summarizer for a quote or a citation **[severity: high — demonstrated failure this session]**
Two concrete failures occurred during this research pass, both on sources that were in fact correct and accessible:
- WebFetch reported **"99.8: NOT FOUND"** for arXiv:2509.03559v1. The string is present in §5.2.1. Recovered only by `curl` + local grep.
- WebFetch reported the 2019 paper as **"EPJC Volume 79, Article 214"**. It is **EPJC 79, 1018**, as confirmed by ref [24] of the 2026 paper.
**Avoid:** every quoted sentence and every citation in the Phase 8 deliverable must come from a locally downloaded source file, retrieved by a recorded command, and grep-verified. Record the retrieval command in the artifact header.

### Pitfall 9: Stale in-repo deliverable paths **[severity: low — but breaks execution]**
`04-01-SUMMARY.md` cites `src/muon/deposited_spectrum.py` and `data/muon/muon_dep_spectrum.csv`; neither exists. Use `src/qpd_potential/muon_deposit.py` and `data/muon_dRdEdep.csv`.

### Pitfall 10: Letting the ~10,300 QPD sensors become a back-door multiplicity credit **[severity: medium]**
The wafer carries ~10,300 sensors at 1/mm², so in principle it has a *spatial* handle (position reconstruction, track-vs-point topology) that NUCLEUS's inter-crystal multiplicity cut does not have. This is a genuinely different observable and a legitimate future direction — but it is **not** NUCLEUS's cut, it has no established efficiency, and Phase 8's job is to set L2 = 1.0.
**Avoid:** record it as a named, unquantified future handle in the open-questions section, with an explicit statement that it may not be credited anywhere in v2.0.

---

## Key Equations and Starting Points

Where each phase action begins.

**SC1 — fit determination.** Start from these five numbers and F1–F2:

| Quantity | Value | Source |
| --- | --- | --- |
| Wafer in-plane edge | 10.16 cm | CONVENTIONS §D |
| Wafer min-enclosing-cylinder diameter | $\sqrt{2(10.16)^2 + 0.20^2}$ = **14.370 cm** | F1 |
| COV cylindrical crystal outer diameter | **10.0 cm** | arXiv:2508.02488 (100 mm), corroborated by arXiv:1905.10258 Fig. 8 ("diameter of 10 cm") |
| COV crystal thickness (all six) | **2.5 cm** | arXiv:2509.03559 §2 |
| Internal shielding cylinder diameter | **29.7 cm** | arXiv:2508.02488 |

Cavity bound (tight route, the load-bearing one):
$$D_{\text{cav}} \;\lesssim\; D_{\text{cyl}} - 2 t_{\text{rect}} \;=\; 10.0 - 2(2.5) \;=\; \mathbf{5.0\ cm}$$
Cavity bound (loose route, for honesty about what is *strictly* excluded):
$$D_{\text{cav}} \;\le\; D_{\text{int.shield}} - 2 t_{\text{B}_4\text{C}} - 2 t_{\text{rect}} \;=\; 29.7 - 8.0 - 5.0 \;=\; 16.7\ \text{cm}$$
**Report both.** The loose route alone does **not** exclude a 14.37 cm diagonal; the verdict rests entirely on the tight route. Saying so is the difference between a defensible gate and an overclaim.

Resulting clearances to quote:
- against the COV cavity, in-plane: $C = 5.0 - 10.16 = \mathbf{-5.2\ cm}$ (shortfall)
- against the COV cavity, diagonal: $C = 5.0 - 14.37 = \mathbf{-9.4\ cm}$
- against the COV crystal *outer* diameter: $C = 10.0 - 10.16 = \mathbf{-0.16\ cm}$ — **the wafer is wider than an entire COV crystal**, the single most compact way to state the result.

**SC2 — the taxonomy.** Start from the quote table in "Existing Results". Emit three columns: *statement (verbatim)*, *section*, *classification (L1 / L1\* / L2)*, *transferable credit for the wafer*. Proposed classification:

| Statement | § | Class | Credit |
| --- | --- | --- | --- |
| Overburden 2.92 ± 0.01 m.w.e.; muon attenuation 1.41 ± 0.02 | §4 (carried, see gaps) | **L1** | transfers |
| Table 4 surface fluxes + normalization uncertainties (μ 25%, n 30%, γ 20%, mat. 30%) | Table 4 | **L1** | transfers |
| Measured VNS gamma ambience 5.03 cm⁻²s⁻¹ | §4.3 / Table 5.1 | **L1** | transfers |
| 5 cm plastic MV / 5 cm Pb / 20 cm 5%-borated HDPE bulk attenuation | §2 | **L1** | transfers as *material* attenuation only |
| 5 cm Pb → factor ~50 γ reduction; other passives → ~10 | §5.2.2 | **L1** | transfers, but see Pitfall 5 |
| ~4 cm nearly-4π B₄C liner → factor ~5 | §5.2.1 | **L1\*** | **1.0** — geometry-coupled to a ~cm payload |
| COV neutron anti-coincidence, factor 5 at 1 keV_ee | §5.2.1 | **L2** | **1.0** |
| COV threshold 1→10 keV costs ~20% of that | §5.2.1 | **L2** | context for the above |
| MV+COV > 99.8% of muon-*induced* background | §5.2.1 | **L2** | **1.0** |
| COV "essential role" in γ rejection | §5.2.2 | **L2** | **1.0** |
| IV rejection of surface / holder events | §2 | **L2** | **1.0** |
| "one and only one target detector" cut | §5.1 | **L2** | **0 rejection**, identically (F3) |
| 478 keV ¹⁰B(n,α) line "harmless … vetoed by the 2.5 cm COV" | §5.2.1 | **L2** | **1.0** — line is inherited, rejection is not |

**SC3 — self-veto acceptance.** Start from `data/muon_dRdEdep.csv` and F4. Recommended reported set: $A_{\text{self}}^{\text{direct}}(E_{\text{cut}})$ at $E_{\text{cut}} \in \{10\ \text{eV}, 1\ \text{keV}, 100\ \text{keV}\}$ (expect ≈1 at all three, which is itself the point), $A_{\text{self}}^{\text{induced}} = 0$ with its argument, and $f_{\text{dead}}$ at 0.969 Hz with a stated $\tau_{\text{dead}}$ from the Phase 5 saturation work.

**SC4 — multiplicity.** F3, one line, one unit test (V8).

**SC5 — stop condition.** See below.

### The stop condition, spelled out

**What constitutes "does not fit":** the wafer's required cavity (two orthogonal dimensions ≥ 10.16 cm) exceeds the best-supported bound on the COV internal cavity, with the bound traced to a published dimension that passes an independent mass-closure check (V1). The current evidence meets that standard.

**What the phase must emit on a no-fit verdict:**
1. The determination with full provenance: every dimension, its source paper, section/caption, and retrieval command.
2. The explicit premise-void statement: a wafer this size forces a redesign of the COV, the Cu support, the B₄C liner, and plausibly the internal shielding and cryostat bore — therefore **φ_post at the detector position is no longer NUCLEUS's φ_post, and essentially nothing beyond room-level environment transfers.**
3. **No reduced veto credit. No resized veto.** Not even as a "for reference" number — a number in the artifact will be reused.
4. The L1/L2/L1\* taxonomy **anyway**: it is independently correct, Phase 16 needs it, and it is the deliverable that survives the verdict.
5. A phase-by-phase disposition of the rest of the milestone. Note for the user, because it is not obvious from the ROADMAP's dependency arrows: **Phases 10 (grid extension + trigger observable) and 11 (ω̄, Debye–Waller, IA broadening) are physically site-independent** — they depend on the Ge VDOS and the QPD response chain, not on the NUCLEUS environment. They survive a no-fit verdict intact. Phases 9, 12, 13, 14, 15, 16 are premised on the NUCLEUS environment transfer and do not.
6. `gpd_return.status: blocked` (or `checkpoint`) returning control to the user for re-scope. Candidate re-scope directions may be *listed* for the user but must not be adopted by the phase: (a) adopt only room-level L1 (overburden, Table 4 fluxes, measured γ ambience) and design an independent shield; (b) revisit the wafer format, which `REQUIREMENTS.md` explicitly places out of scope ("VALD-09 may show this geometry is incompatible … which is a stop-condition, not an optimization trigger"); (c) retarget to a different host experiment.

**What would overturn the no-fit verdict** (state these so the gate is falsifiable):
- The Goupy thesis showing rectangular COV crystals substantially larger than the 100 mm cylinders, with a cavity ≥ 10.16 cm in two axes.
- A published NUCLEUS-1kg or upgrade geometry with a materially larger cavity.
- Evidence that the 100 mm crystal is a commissioning-only part and the Chooz cylinders are larger. *(Weak: the 2026 paper independently gives 2.5 cm thickness, matching the 25 mm commissioning crystal, so the two descriptions are consistent.)*

---

## Open Questions

| # | Question | Impact | Resolution route |
| --- | --- | --- | --- |
| Q1 | Dimensions of the four **rectangular** COV crystals and of the Cu support structure | Would convert the cavity bound from "argued" to "read". Could in principle overturn the verdict. | **Goupy thesis** — see "What Was NOT Found". Named acquisition obligation. |
| Q2 | IV beaker / IV wafer dimensions and the module stack height | Refines the cavity in the vertical axis (currently unconstrained by this research) | Goupy thesis; possibly Fig. 1(f) scaling |
| Q3 | Is the 2.92 ± 0.01 m.w.e. overburden and the 1.41 ± 0.02 attenuation verbatim in §4? | L1 anchor integrity | **Not re-verified in this pass** — carried from the project's own v2.0 literature survey. Cheap grep on the already-downloaded `2509.03559v1` text. Do it in-phase. |
| Q4 | Does the published EPJC v2 differ from arXiv v1 in §5.2.1 numbers? | All L2 quotes are labelled v1 | v2 HTML returns 404; EPJC is open access (doi:10.1140/epjc/s10052-025-15168-9). Spot-check the four L2 numbers against the journal version. |
| Q5 | Could the ~10,300 QPD sensors provide a *spatial* coincidence handle? | Not a Phase 8 credit; possible future work | **Record only.** May not be credited in v2.0 (Pitfall 10). |
| Q6 | What τ_dead should be used for $f_{\text{dead}}$? | Turns the 0.969 Hz muon rate into a live-time number | Phase 5/6 saturation and censoring conventions (CONVENTIONS §F, 25 kHz non-paralyzable) |

---

## What Was NOT Found

**The Goupy 2024 thesis full text could not be retrieved in this environment.** This is the roadmap's designated fallback source "where the paper is silent", and it is silent on exactly the dimensions Q1/Q2 need.

- Metadata **is** retrievable via the HAL API (`https://api.archives-ouvertes.fr/search/?q=halId_s:tel-05298505`): author Chloé Goupy, defence 2024-10-08, DOI 10.70675/574d6e17z1b68z4676zbde9z255450e1c649, file `https://theses.hal.science/tel-05298505/file/va_Goupy_Chloe.pdf`.
- **All four full-text routes are blocked** by an Anubis proof-of-work anti-bot challenge, returning an identical 12,587-byte HTML challenge page with `HTTP 200` and `content-type: text/html` (so a naive downloader will silently save an HTML file named `.pdf`): `theses.hal.science/tel-05298505{,/document,/file/va_Goupy_Chloe.pdf}`, `hal.science/tel-05298505v1/document`, `www.theses.fr/2024UNIP7170.pdf`. A browser User-Agent does not help; the challenge requires client-side JavaScript.
- **Named acquisition route:** manual download in a real browser by the user (the challenge resolves in a few seconds interactively), placing the PDF in-repo (e.g. `data/external/goupy_thesis_2024.pdf`) so the phase can grep it. Alternative: institutional interlibrary/ABES copy.
- **Planning consequence:** Phase 8 must be plannable **without** the thesis. It is — the commissioning paper supplies the load-bearing 100 mm number and it passes an independent mass-closure check. The thesis upgrades Q1/Q2 from "bounded" to "read", and is the only genuinely independent third route (V10). Plan it as an *optional enrichment task with a user-action dependency*, never as a blocking task.

**Also not found:** any dimension of the COV/IV internal envelope in arXiv:2509.03559 itself (exhaustively grep'd); any scale bar or dimension annotation in its Fig. 1 (inspected directly).

---

## Caveats and Alternatives

Adversarial self-critique of this research.

**1. The no-fit verdict rests on a single load-bearing number from a paper that is not in the roadmap's anchor list.** The 100 mm COV cylinder comes from arXiv:2508.02488, a commissioning paper describing the TUM setup, not Chooz. My defence: (i) the 2026 Chooz paper independently states 2.5 cm crystal thickness, matching the commissioning crystal's 25 mm height; (ii) the 2019 paper independently states the outer veto has "a diameter of 10 cm"; (iii) the mass closure V1 (1045 g computed vs "1 kg" stated) confirms the read. Three consistent statements across three papers plus a physical closure is strong. But it is *not* the same as reading it off the Chooz drawing, and the plan must not present it as such.

**2. The tight cavity bound (5.0 cm) assumes the rectangular slabs sit inside the cylinder rim.** If the four rectangular crystals are larger than the cylindrical caps — a plausible geometry for "hermetic" coverage of a stacked two-module payload — the cavity could exceed 5 cm. The loose bound from the 297 mm internal shield (16.7 cm) does **not** exclude a 14.37 cm diagonal. So the *strict* exclusion is: the wafer's 10.16 cm edge exceeds the 10.0 cm outer diameter of a COV cap crystal, which forecloses the cylindrical caps regardless of the side slabs. That statement is airtight; the −5.2 cm shortfall figure is not. **Report the airtight statement as the verdict and the −5.2 cm as an estimate.**

**3. My Fig. 1(e) pixel scaling is not a rigorous measurement.** I located the pink "inner detector modules" annotation box programmatically (51 px wide) and estimated the COV cylinder at ≈130 px by inspection, giving ≈4 cm. That is an agent eyeballing a schematic. It is *consistent* with the 5 cm bound, which is why I report it, but it must be redone in-plan with recorded pixel coordinates and an uncertainty, and it shares its scale anchor with the primary route (V10) so it corroborates nothing independently.

**4. I am asserting a conclusion the project wants to hear.** The project has already written PITFALLS.md around "the veto does not transfer" and the roadmap pre-labels `fp-veto-credit-transfer`. That creates confirmation pressure, and I should flag where I pushed back rather than agreed: (a) the project's "COV factor ~5" is quotable but sits next to two other factor-5s and the project's own text does not distinguish them; (b) the project's "~9 cm²" array footprint is 4× larger than the published crystal footprint and is not a NUCLEUS number; (c) NUCLEUS themselves call the multiplicity cut "very marginal", which means the wafer's zero-multiplicity handicap costs *little in absolute background* — an honest point in the wafer's favour that the project's framing suppresses and that Phase 8 must report; (d) the L2-off baseline is **not** conservative, it is a different and worse configuration, which cuts against the project's framing of L2-off as a safe lower bound.

**5. Alternative reading of Success Criterion 1 that I rejected.** One could satisfy SC1 literally by scaling Fig. 1(e) against the 297 mm internal shield (which *is* in the figure and *is* published). I rejected this as the primary route because the internal shield is drawn in a different panel region with a different apparent perspective from the COV, and because it yields only the loose bound. It is worth doing as a *secondary* consistency check, and if it and the 100 mm route disagree by more than ~30%, the figure is too schematic to scale at all — which is itself a reportable finding.

**6. Unresolved tradeoff: how hard to push for the thesis.** Blocking Phase 8 on a user-action PDF download is bad workflow. Proceeding without it means Q1/Q2 stay bounded rather than read. My recommendation is to proceed and mark the thesis as an enrichment task, but a reviewer could reasonably argue that a *stop-condition gate for an entire milestone* deserves the extra source before the user is told to re-scope. The plan should make this an explicit, visible choice rather than a default.

**7. Weakest anchor overall.** The claim "the COV internal cavity is ~5 cm" — everything else (the taxonomy, the multiplicity identity, the self-veto decomposition) stands independently of it, and would stand even if the wafer did fit.

---

## Sources

### Primary (HIGH — downloaded, converted to text, grep-verified this session)

1. **NUCLEUS Collaboration (H. Abele et al.)**, *Particle background characterization and prediction for the NUCLEUS reactor CEνNS experiment*, Eur. Phys. J. C **86**, 29 (2026); doi:10.1140/epjc/s10052-025-15168-9; arXiv:2509.03559. Retrieved: `curl https://arxiv.org/html/2509.03559v1` (398 kB) and `.../Figures/Figure1.png` (1875×2613). Used: §2, §5.1, §5.2.1, §5.2.2, Fig. 1, Fig. 8 caption. **All quotes are from v1**; the published EPJC version may differ.
2. **NUCLEUS Collaboration (G. Angloher et al.)**, *Exploring CEνNS with NUCLEUS at the Chooz nuclear power plant*, Eur. Phys. J. C **79**, 1018 (2019); doi:10.1140/epjc/s10052-019-7454-4; arXiv:1905.10258. Retrieved: `curl https://ar5iv.labs.arxiv.org/html/1905.10258`. Used: Fig. 7 and Fig. 8 captions, §2.1, §3.2.1, §3.2.3. Journal reference **79, 1018** confirmed via ref [24] of source 1.
3. **NUCLEUS Collaboration (H. Abele et al.)**, *Commissioning of the NUCLEUS experiment at the Technical University of Munich*, arXiv:2508.02488 (2025); Phys. Rev. D. Retrieved: `curl https://arxiv.org/html/2508.02488v1`. Used: Fig. 1 caption, "Passive shielding", "Cryogenic Outer Veto", "Target Detectors", "Data Acquisition". **The load-bearing geometric source; recommend promoting to a Phase 8 anchor.**
4. **In-repo:** `src/qpd_potential/{wafer_geometry,muon_flux,muon_deposit}.py`; `data/muon_dRdEdep.csv`; `tests/test_muon_geometry.py`; `GPD/CONVENTIONS.md` §D.

### Secondary (MEDIUM)

5. **C. Goupy, S. Marnieros, B. Mauri, C. Nones, M. Vivier**, *Prototyping a High Purity Germanium cryogenic veto system for a bolometric detection experiment*, Nucl. Instrum. Meth. A **1064**, 169383 (2024); arXiv:2401.09837. Retrieved and grep'd. **Prototype geometry (70 mm ⌀ × 20 mm, 3 mm Cu boxes, PTFE holders) — indicative of mounting overhead only; not the final COV.**
6. **GPD/literature/{SUMMARY,PITFALLS,METHODS,COMPUTATIONAL}.md** (v2.0 survey). Used as entry context. **Two corrections issued by this pass:** the "COV factor 5" needs the disambiguation of Pitfall 1, and the "~9 cm²" footprint needs the basis label of Pitfall 4.
7. **GPD/phases/04-.../04-01-SUMMARY.md** — physics results HIGH, **deliverable paths stale** (Pitfall 9).

### Tertiary (LOW — named but not obtained)

8. **C. Goupy**, *Background mitigation strategy for the detection of coherent elastic scattering of reactor antineutrinos on nuclei with the NUCLEUS experiment*, Ph.D. thesis, Université Paris Cité (2024), NNT 2024UNIP7170, HAL `tel-05298505`, DOI 10.70675/574d6e17z1b68z4676zbde9z255450e1c649. **Full text not obtainable in this environment** (Anubis PoW; four routes verified blocked). Metadata via HAL API only. Cited as an acquisition obligation, **not** as evidence for any number in this document.
9. **Carried-forward, not re-verified this pass:** overburden 2.92 ± 0.01 m.w.e.; muon attenuation 1.41 ± 0.02; Table 4 normalization uncertainties; VNS γ ambience 5.03 cm⁻²s⁻¹. These come from the project's own v2.0 literature survey against source 1 and are cheap to re-verify in-phase (Q3).

---

## Metadata

- **Research mode:** balanced
- **Phase:** 08 — Veto-Envelope Geometry Gate (P-VETO)
- **Requirement:** VALD-09 (GATING — milestone stop-condition)
- **Consumer:** `gpd-planner`
- **Forbidden proxies in scope:** `fp-veto-credit-transfer`; inventing a resized veto; continuing with a reduced veto credit past a failed gate
- **New anchors proposed:** arXiv:2508.02488 (promote to Phase 8 anchor); arXiv:2401.09837 (secondary)
- **Cross-phase findings handed off:** Fig. 8 of arXiv:2509.03559 carries both passive-only and "all vetoes" traces on the same axes → Phase 9 trace-selection (partially answers the pre-/post-veto open question for Fig. 8); Phases 10 and 11 are site-independent and survive a no-fit verdict
