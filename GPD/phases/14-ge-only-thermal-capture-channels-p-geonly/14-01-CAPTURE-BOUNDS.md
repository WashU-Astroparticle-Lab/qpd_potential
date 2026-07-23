# 14-01 — Ge prompt (n,γ) capture: acquisition, fold, and the recoil bounds

**Plan:** 14-01 (wave 1) · **Phase:** 14 Ge-Only Thermal-Capture Channels (P-GEONLY)
**Accuracy label:** `order_of_magnitude`, inherited from the Phase-9 sea-level flux and
attached to every rate and every bound below. **This is a BOUND, not a quantification**
(ROADMAP SC2). Many-digit values appear only as reproducibility figures for the quadrature
and the parsing.

**Interpreter:** `/opt/anaconda3/bin/python3` — numpy 1.26.4, scipy 1.17.1, `endf` 0.1.12.
**Flux leg:** `phi_default == phi_hi` (OUTDOOR). `phi_lo` is the indoor leg, refused in code.

---

## 1. Acquisition, and the trap that sits one line of code away

### 1.1 `MF=3 MT=102` is identically zero — MEASURED, not described

The raw ENDF/B-VIII.0 files for all five Ge isotopes are already committed at
`data/endf/raw/n_*.dat` from Phase 7 and they carry MT=102. Reading `MF=3 MT=102` from them
is the obvious move and it is **wrong**:

| E_n | ⁷⁰Ge | ⁷²Ge | ⁷³Ge | ⁷⁴Ge | ⁷⁶Ge |
|---|---|---|---|---|---|
| 0.0253 eV | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 1 eV | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 100 eV | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 1 keV | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

In the resolved-resonance region the capture cross section lives in **File 2** as resonance
parameters, and File 3 carries only the smooth background. Reading `MF=3 MT=102` there and
reporting σ = 0 would have produced **exactly** the "capture channel is zero" outcome ROADMAP
Phase 14 names as a forbidden proxy (`fp-capture-as-zero`) — **manufactured out of a file that
does contain the physics**.

The zero is asserted by execution in
`tests/test_capture_channel.py::test_mf3_mt102_is_zero_in_the_rrr`, so the trap is proved
real rather than hypothesised, and the artifact header at
`artifacts/v2.0/ge_capture_xs.csv` states it in words.

**The operative source is the pre-reconstructed, Doppler-broadened LANL Lib80x ACE set** at
`data/endf/ace/32*.800nc` (293.6 K) — the same resolution Phase 7 reached for elastic and for
the same reason. The switch is recorded, not made silently. The MF=3 **`QM` field IS used**:
`QM` is the reaction Q-value and is well defined in File 3 even where the File-3 cross
section is zero.

**NCrystal is not used here**, and the reduction is stated with its reason: NCrystal supplies
a thermal *scattering* law S(q,ω); σ_(n,γ) is smooth and 1/v and needs none.

### 1.2 The anchor reproduces with nothing fitted

σ_(n,γ) at 0.0253 eV, abundance-weighted from `params.GE_ISOTOPES` (IUPAC, Phase-7 lock):

| isotope | σ_th [b] | abundance | share of natural thermal capture |
|---|---:|---:|---:|
| ⁷⁰Ge | 3.0517 | 0.2057 | 28.38 % |
| ⁷²Ge | 0.8857 | 0.2745 | 10.99 % |
| **⁷³Ge** | **14.7009** | **0.0775** | **51.52 %** |
| ⁷⁴Ge | 0.5189 | 0.3650 | 8.56 % |
| ⁷⁶Ge | 0.1546 | 0.0773 | 0.54 % |
| **natural** | **2.211522** | 1.0 | 100 % |

ROADMAP states ~2.2 b natural and ~15 b for ⁷³Ge **independently**. Both fall out of the
frozen ACE set unassisted — nothing here is fitted or scaled to reach them. **⁷³Ge is
7.75 % of the atoms carrying 51.52 % of the natural thermal capture.**

### 1.3 EGAF: acquired — and the sharpening gap survives anyway

Planning recorded EGAF as "NOT present locally" and treated a retrieval failure as an
acceptable named gap. **The retrieval succeeded.** All five Ge capture-product line lists are
frozen at `data/egaf/{71,73,74,75,77}GE_EGAF.ens`, with the `curl` command, byte counts and
SHA-256 recorded in `data/egaf/MANIFEST.md` on the Phase-9 PARMA pattern. `WebFetch` and LLM
page summarizers were not used. **This discharges the acquisition half of ROADMAP SC1.**

Two reading traps, both measured rather than assumed:

1. **Each `.ens` file carries three datasets** — the evaluated `{~EGAF}` set plus the raw
   `^BUDAPEST` and `^L^A^N^L` measurement sets, each with its own normalisation record. A
   naive whole-file parse sums all three and inflates the per-capture intensity by roughly
   3×. Only `{~EGAF}` is used.
2. **Intensity per capture = NR × RI / σ₀**, with `NR` read from the N record and σ₀ from the
   `BR$|s{-0}=` comment — the file's own normalisation, not a supplied one.

**What caught trap 1 was a cascade-completeness check, and that check is also the result:**
per capture, energy conservation requires Σᵢ Iᵢ Eᵢ = Q_cap.

| target | product | observed γ | observed multiplicity Σ I | completeness Σ I E / Q |
|---|---|---:|---:|---:|
| ⁷⁰Ge | ⁷¹Ge | 82 | 2.233 | **0.6084** |
| ⁷²Ge | ⁷³Ge | 45 | 1.662 | **0.6022** |
| ⁷³Ge | ⁷⁴Ge | 603 | 4.245 | **0.7050** |
| ⁷⁴Ge | ⁷⁵Ge | 36 | 2.027 | **0.6654** |
| ⁷⁶Ge | ⁷⁷Ge | 9 | 8.493 | 5.018 — **EXCLUDED** |

**The observed cascade carries only 60–71 % of the capture Q-value.** The remaining 29–40 %
is unobserved quasi-continuum strength — and that is precisely the part a cascade recoil
*spectrum* would need. So the acquisition succeeded and **the sharpening gap survived**; what
changed is that the gap is now a number rather than an absence. ⁷⁶Ge is excluded: EGAF
normalises to σ₀ = 0.06 b against the ENDF/ACE 0.1546 b and lists only 9 γ, so its
completeness exceeds 1. It carries 0.54 % of the natural thermal capture, so excluding it
changes nothing — but the inconsistency is reported rather than smoothed.

---

## 2. The fold

R = N_Ge ∫ φ(E_n) σ_(n,γ)(E_n) dE_n, with N_Ge = 8.291565×10²⁴ atoms/kg (CONVENTIONS §D),
log–log segment quadrature exact for a power law, on the ACE native union grid unioned with
200 nodes/decade and the band edges as exact anchors — 24 298 nodes over 0.01 eV – 20 MeV.

**Flux path.** `neutron_recoil.neutron_flux_cm2_s_MeV` evaluates the **pinned PARMA driver
directly at every node**; neither committed table is interpolated anywhere. The
1 – 10.14 eV gap that `ambient_neutron_thermal_v2.0.csv` (0.01–1 eV) and
`ambient_neutron_flux_v1.1.csv` (10.14 eV – 197 MeV) leave open contains **232 quadrature
nodes**, and the flux there is **bit-identical** to a direct `parma.differential_flux` call —
measured, not assumed.

### 2.1 Band decomposition

| band (incident E_n) | rate [counts kg⁻¹ day⁻¹] | fraction |
|---|---:|---:|
| thermal, ≤ 0.5 eV (cadmium cutoff) | **3365.54** | 76.49 % |
| epithermal, 0.5 eV – 1 keV | 857.08 | 19.48 % |
| intermediate, 1 keV – 1 MeV | 167.75 | 3.81 % |
| fast, 1 – 20 MeV | 9.41 | 0.21 % |
| **total, 0.01 eV – 20 MeV** | **4399.78** | 100 % |

Bands sum to the total with residual **2.07×10⁻¹⁶**. Node doubling (200 → 400 per decade)
moves the total by **1.19×10⁻⁵** — both far inside the 0.5 % acceptance.

Per isotope (abundance-weighted contribution to the natural total): ⁷³Ge 2553.07,
⁷⁰Ge 1054.15, ⁷²Ge 420.61, ⁷⁴Ge 335.25, ⁷⁶Ge 36.70. **⁷³Ge carries 58.0 % of the capture rate
and it is also the isotope with the highest single-γ recoil ceiling.** The ⁷⁰Ge row, 1054.15,
is the ⁷¹Ge production rate Plan 14-02 consumes.

### 2.2 THERMAL-DOMINANCE VERDICT — the non-identity disconfirming check

Nothing in CALC-23, in the phase title, or in the ROADMAP establishes that the thermal band
dominates. 1/v weighting favours thermal; the sea-level spectrum's flat-in-lethargy
1 eV – 10 keV plateau (Phase 9: flat to a factor 1.390) pushes the other way. The 60 %
threshold was declared in code and in the test module *before* the number was computed.

> **VERDICT: THERMAL FRAMING SURVIVES.** The thermal band carries **76.49%** of the total Ge
> capture rate, against the pre-declared 60 % threshold.
>
> **But 23.51% of the channel is not thermal**, which the phase title does not admit. That
> non-thermal remainder — 1034.24 counts kg⁻¹ day⁻¹, itself ~8.7× the entire Phase-12 CEvNS
> total — is carried forward to Phase 16 as part of the channel rather than absorbed into the
> thermal label. A budget that took the phase title literally and folded only the thermal
> component would understate this channel by a factor 1.31.

### 2.3 The naive product — agreement would have been the failure

Φ_th × σ(0.0253 eV) × N_Ge × 86400 = **4383.92** counts kg⁻¹ day⁻¹, using **Phase 9's**
Φ_th = 2.767075×10⁻³ cm⁻² s⁻¹ (0.01–0.5 eV, cadmium cutoff), consumed unchanged.

| comparison | value |
|---|---:|
| naive product | 4383.92 |
| **spectrally folded thermal band** | **3365.54** |
| **measured ratio naive / folded** | **1.3026 (+30.26 %)** |
| Westcott √π/2, for context only | 0.8862 |
| naive / **total** | 0.9964 |

The two **differ by 30.26 %**, which is the pass condition — agreement would have indicated
the fold collapsed to the product rather than that the physics is right. σ_(n,γ) is a 1/v
absorber, so the 2200 m/s point sits above the flux-weighted mean of σ over the sub-cadmium
band and the product overstates it. **√π/2 = 0.8862 is not the measured ratio and is not
substituted for it.**

**The trap is the last row.** naive/total = 0.9964 *looks* like corroboration. It is not: the
product overstates the thermal band by 30 % while knowing nothing about the ~1034 counts of
epithermal, intermediate and fast capture in the total. Two errors nearly cancelling.

### 2.4 The Phase-9 mK caveat, answered with a number

Phase 9 §5 handed Phase 14 the 293.6 K ACE processing temperature against a mK crystal as an
unvalidated assumption it could not settle. Recomputing with the **committed 0.1 K set**
(`.805nc`, temperature key `0K` vs `294K`):

| band | 293.6 K | 0.1 K | signed relative difference |
|---|---:|---:|---:|
| epithermal 0.5 eV – 1 keV | 857.076 | 857.163 | **+0.01016 %** |
| total | 4399.777 | 4399.782 | +0.00013 % |

**Mechanism, so this is not read as a null cross-check:** Doppler broadening is a convolution
with a normalised kernel, so it conserves the resonance integral while reshaping peaks. A
~0 band-integrated shift is the *expected* result. **Caveat retained:** anything that
resolves individual resonance *line shapes* must re-derive from the 0.1 K set. The rate
question is settled; the line-shape question is not, and the distinction is the answer.

### 2.5 Thin-target validity — checked, and it does not hold everywhere

P_capture(2 mm) = Σ₁₀₂ × 0.2 cm, computed from the same σ the fold uses:

| point | σ [b] | P_capture(2 mm) |
|---|---:|---:|
| 2200 m/s (0.0253 eV) | 2.2115 | 1.95 % ≪ 1 |
| fold floor 0.01 eV | 3.5180 | 3.11 % ≪ 1 |
| **largest σ on the node set, 102.59 eV** | **83.43** | **73.6 % — NOT ≪ 1** |

At that ⁷³Ge resonance the wafer is nearly **black** to capture, so the thin-target formula
overstates the epithermal band. Bounded rather than corrected — comparing
∫φ(1−e^{−Σt})dE against ∫φΣt dE:

| band | attenuated / thin |
|---|---:|
| thermal | 0.9915 (−0.85 %) |
| **epithermal** | **0.8900 (−11.00 %)** |
| intermediate | 0.9868 (−1.32 %) |
| fast | 1.0000 (−0.00 %) |

Normal incidence, no scattering, no angular distribution: it **bounds** the effect, it does
not correct it. The thin-target rate is the one reported everywhere, so this omission is
`penalizes_SB` — the background is overstated by ≲ 11 % in one band.

### 2.6 Biffl comparison — made, with its direction

Φ_th adopted = **2.767075×10⁻³ cm⁻² s⁻¹**, sourced from
`09-02-NEUTRON-DECLARATION.md` §5 — **Phase 9's product**, not Phase 13's, and not re-derived
here. Biffl et al., PRD **107**, 092011 (2023) state a requirement Φ_th < 7×10⁻⁴ n/cm²·s.

> **Ratio = 3.95×, ABOVE the requirement.** This unshielded sea-level configuration **does
> not meet** Biffl's stated thermal-flux requirement. Biffl also state that capture recoils
> "strongly overlap the CEvNS signal for recoils ≲ 100 eV" — the regime this phase's bound
> lands in.

---

## 3. The recoil bounds

### 3.1 RIGOROUS, cascade-independent

> **Every (n,γ) capture yields exactly ONE recoiling nucleus**, so at most one event per
> capture can land in the RoI:  **R_RoI ≤ R_capture = 4399.78 counts kg⁻¹ day⁻¹.**

It holds on the recoil axis, the deposit axis and the reconstructed axis alike, because the
response matrix's columns each sum to 1 — the fold moves counts, it does not create them. It
is derived in one line and **not** obtained by integrating a spectrum, and it depends on **no
cascade parameter**. `test_bound_is_cascade_free` varies multiplicity (1, 3, 5, 17), γ-energy
partition (four explicit partitions) and angular correlation (isotropic, fully aligned,
anti-aligned) and asserts the number is **exactly** unchanged.

| comparison, all totals | value | ratio |
|---|---:|---:|
| this bound | 4399.78 | — |
| Phase-13 elastic, E_rec 10–100 eV | 5430.29 (Ta→Al) / 5485.15 (Al→Hf) | 0.81 / 0.80 |
| **Phase-12 CEvNS total** | **118.73** | **37.1× larger** |

**This channel is not a rounding correction.** It sits at the same order as the elastic
channel and 37× the signal. It is also **loose by an unknown factor ≤ 1**: converting the
rate bound into an in-RoI *fraction* needs the cascade, which §1.3 shows is only 60–71 %
observed.

### 3.2 RIGOROUS, per isotope — the single-γ ceiling, which is NOT the cascade answer

T_max = Q_cap² / (2 M_(A+1) c²), with Q_cap **read** from the ENDF `MF=3 MT=102 QM` field and
the recoiling body the A+1 product (using A would overstate every ceiling by ~1.4 %):

| target | product | Q_cap [eV] | **T_max [eV]** |
|---|---|---:|---:|
| ⁷⁰Ge | ⁷¹Ge | 7 415 890 | 415.77 |
| ⁷²Ge | ⁷³Ge | 6 782 890 | 338.30 |
| **⁷³Ge** | **⁷⁴Ge** | **10 196 200** | **754.11** |
| ⁷⁴Ge | ⁷⁵Ge | 6 505 220 | 302.87 |
| ⁷⁶Ge | ⁷⁷Ge | 6 072 570 | 257.07 |

**⁷³Ge sets the maximum at 754.11 eV, and ⁷³Ge is also the isotope dominating the capture
rate (58.0 %).** The ROADMAP's generic *"473 eV at 8 MeV"* is an **illustration, not the Ge
answer**: the real Ge maximum is **higher**, and it follows from the actual QM values above
rather than being reconciled to the illustrative figure.

**These are ceilings.** A real capture de-excites through a multi-γ cascade and
Σ E_γ² ≠ (Σ E_γ)². Demonstrated with numbers for an explicit 3-γ partition summing to the
⁷⁰Ge Q-value, {2.0, 3.0, 2.4159} MeV: Σ(E²) = 1.8837×10¹³ eV² vs (ΣE)² = 5.4996×10¹³ eV²,
ratio **0.3425**.

### 3.3 CONDITIONAL — multiplicity

For an equal-energy isotropic cascade of multiplicity N the mean is **⟨T⟩ = T_max / N**, with
**N left symbolic**. No multiplicity is assigned from recollection (`fp-assumed-multiplicity`),
and the artifact row carries no numeric value.

### 3.4 The EGAF bracket — a real, sourced tightening of the recoil scale

From the frozen `{~EGAF}` line lists, ⟨T⟩ = Σ Iᵢ Eᵢ² / (2Mc²) over the **observed** lines is a
lower estimate. The unobserved strength carries E_miss = Q − ΣIE per capture; maximising the
missing Σ I E² subject to that budget and Eᵢ ≤ Q puts it all at E = Q, so
⟨T⟩ ≤ [Σ I E² + E_miss·Q] / (2Mc²) is a **rigorous upper bracket given the observed list and
energy conservation**:

| target | ⟨T⟩ observed [eV] (CONDITIONAL) | ⟨T⟩ upper bracket [eV] (RIGOROUS) | single-γ ceiling [eV] |
|---|---:|---:|---:|
| ⁷⁰Ge | 161.6 | 324.4 | 415.8 |
| ⁷²Ge | 155.3 | 289.8 | 338.3 |
| **⁷³Ge** | **186.5** | **408.9** | **754.1** |
| ⁷⁴Ge | 149.5 | 250.9 | 302.9 |

For the dominant isotope this tightens the ceiling by a factor **1.84**. It is a **mean, not
a spectrum**, so it does not give the in-RoI fraction — which is exactly why the rigorous rate
bound in §3.1 is stated independently of it and is not adjusted by it.

### 3.5 Inelastic (ROADMAP SC5) — bounded, named, and PLACED

Summed MT=51–91 folded over the same flux: **2666.83 counts kg⁻¹ day⁻¹** natural
(⁷⁴Ge 1014.66, ⁷²Ge 708.63, ⁷⁰Ge 446.47, ⁷³Ge 278.86, ⁷⁶Ge 218.16). 94.42 % from the
1–20 MeV band.

**Placement — two different recoils, and conflating them is the error this guards against:**

1. **The nuclear recoil from the scattering itself.** The reaction is populated by *fast*
   neutrons: the rate-weighted mean incident energy is **4.238 MeV**, and the
   elastic-kinematics ceiling f_nat × ⟨E_n⟩ = **227.2 keV** — **~3 decades ABOVE the 100 eV
   RoI top.** The inelastic reaction-rate bound is therefore **very loose** in the RoI.
2. **The γ-emission recoil** when the excited level de-excites, T = E_γ²/(2Mc²). This is the
   part landing **near** the band:
   - **⁷⁴Ge 596 keV** → **2.577 eV**
   - **⁷²Ge 834 keV** → **5.185 eV**

**The >20 MeV ceiling is NOT covered by Phase 13's margin for this channel.** The top-decade
(2–20 MeV) fraction of the inelastic rate is **73.55 %** — far above the 10 % trigger — so
Phase 13's measured 11.85× >20 MeV margin, established for *elastic*, is **not reused**. The
inelastic >20 MeV omission is labelled `flatters_SB` and carried as such. For **capture** the
top-decade fraction is 0.09 %, so the same ceiling is genuinely negligible there.

---

## 4. Un-netted directional-bias table (Phase-9 §7 schema)

Each row stands alone. **Nothing is netted against anything else.**

| # | omission / configuration choice | direction | magnitude, measured |
|---|---|---|---|
| 1 | Outdoor flux leg `phi_default = phi_hi`; `phi_lo` (indoor) refused | `penalizes_SB` | factor 5 on the background if the indoor leg were adopted. A configuration choice, **not** an error bar (09-02 §4) |
| 2 | 20 MeV ENDF ceiling — **capture** | `flatters_SB` | top-decade (2–20 MeV) fraction 0.09 % → negligible; Phase 13's CALC-24 deferral disposition applies |
| 3 | 20 MeV ENDF ceiling — **inelastic** | `flatters_SB` | top-decade fraction **73.55 %**; Phase 13's 11.85× elastic margin is **not** reused, and the omission is carried unquantified |
| 4 | ~197 MeV flux-grid ceiling | `flatters_SB` | inherited from Phase 13 unchanged |
| 5 | Thin-target formula, no capture self-shielding | `penalizes_SB` | epithermal band overstated by ≤ 11.00 %; thermal by 0.85 % |
| 6 | In-RoI bound = **total** capture rate; the in-RoI fraction (≤ 1) is unknown | `penalizes_SB` | unbounded above by 1; the cascade is only 60–71 % observed, so the factor cannot be closed |
| 7 | 293.6 K ACE processing against a mK target | `neutral` on band integrals | +0.010 % epithermal, +0.0001 % total; **unresolved for resonance line shapes** |
| 8 | eV–keV differential flux shape | **UNBOUNDED**, direction undetermined | Phase 13 constructed perturbations invisible to the only cross-check that moved the in-RoI elastic rate by +41.33 % and −16.31 % |
| 9 | EGAF cascade incompleteness (29–40 % of Q unobserved) | affects the recoil-energy scale only | ⟨T⟩ observed is a lower estimate; bracketed in §3.4 |

---

## 5. ROADMAP evidence located by this plan

| criterion | status from 14-01 | evidence |
|---|---|---|
| **SC1** — ENDF MT=102 for five isotopes **and** EGAF line lists acquired and frozen, Phase-7 pattern | **evidence complete**; verdict written in 14-02 closeout | `artifacts/v2.0/ge_capture_xs.csv`, `data/egaf/MANIFEST.md` |
| **SC2** — cascade recoil **bounded, not quantified**; single-γ limit never the cascade answer | **evidence complete** | §3.1–3.4, `artifacts/v2.0/capture_recoil_bounds.csv` |
| **SC5** — Ge inelastic bounded and named | **evidence complete** | §3.5 |
| **SC4** — φ_th disposition | discharged on **branch (a)**: sourced by Phase 9, not gapped | §2.3, §2.6 |
| **SC3** — ⁷¹Ge EC lines | Plan 14-02 | — |

---

## 6. CHECKPOINT — EGAF sharpening (Task 3, `checkpoint:decision`)

> ## CHECKPOINT REACHED — EGAF sharpening
>
> The rigorous bound is stated and does not depend on the cascade. The in-RoI *fraction* does.
>
> 1. **Stop at the bound** *(default)* — carry the rate bound plus the named EGAF gap into Phase 16.
> 2. **Sharpen with a sourced cascade** — only if Task 1's EGAF retrieval succeeded and the
>    line list is frozen and integrity-checked. Never with a remembered multiplicity.
> 3. **Bound the fraction geometrically** — a bounded side investigation deriving an in-RoI
>    fraction limit from the Q-value and the RoI edges alone, with no cascade data.
>
> Proceed with option 1? **[Y/n/e]** (Enter = Y)

**Recorded, and continued on the default (option 1), under the standing session directive.**

Two things changed the evidence available at this checkpoint and are recorded rather than
silently acted on:

- **Option 2's precondition became TRUE.** The EGAF retrieval succeeded and the line lists are
  frozen and integrity-checked. Option 2 is therefore live in a way planning did not expect.
- **It still does not deliver what option 2 was for.** A cascade recoil *spectrum* needs a
  Monte Carlo over the cascade, which this plan's contract lists under
  `forbidden_estimator_families`; and the observed cascade carries only 60–71 % of Q, so even
  a permitted estimator could not close the in-RoI fraction from it.

What was taken from EGAF instead is strictly inside the "bounds only" shape: the
**rigorous ⟨T⟩ upper bracket of §3.4**, derived from the observed list plus energy
conservation, which tightens the ⁷³Ge single-γ ceiling by 1.84× without assuming any
multiplicity. The symbolic T_max/N row is untouched and the rigorous rate bound of §3.1 is
unchanged. **Option 3 was not pursued** — it remains an available follow-up.

---

## 7. Reproduction

```bash
PYTHONPATH=src /opt/anaconda3/bin/python3 -c \
  "from qpd_potential import capture_channel as c; \
   c.write_capture_xs_csv(); c.write_capture_rate_bands_csv(); \
   c.write_capture_recoil_bounds_csv()"
/opt/anaconda3/bin/python3 -m pytest tests/test_capture_channel.py -q
```

Every number above is traceable to a locally frozen artifact through a recorded command.
`WebFetch` was not used as a quote source anywhere in this plan.
