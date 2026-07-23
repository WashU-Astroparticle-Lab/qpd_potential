# Methods Research — v2.0 NUCLEUS-VNS Background Transfer and the 100 meV Extension

**Domain:** Rare-event cryogenic-detector background modelling — transferring a published, measured,
shielded background environment (NUCLEUS at the Chooz Very-Near-Site) to a different target material
(natural Ge), and extending an analytic recoil/response pipeline two decades below its present
10.14 eV grid floor to 100 meV.
**Researched:** 2026-07-22
**Confidence:** MEDIUM-HIGH overall. HIGH for the flux/response separation, the flat-box inversion,
the digitization/lethargy conventions, and the lattice-scale kinematics. MEDIUM for the semi-analytic
shield-propagation accuracy figures and for what NUCLEUS actually publishes per layer (verified only
from the arXiv/EPJC full text via WebFetch, not from a locally-read PDF). LOW for the LEE amplitude
itself — that is irreducibly a scenario input, not a computable quantity.

> **Scope note.** v1.0 methods (Freedman CEvNS + Helm; Huber–Mueller flux; Gaisser–Guan × ray-box
> chord × Landau–Vavilov MPV; Klein–Nishina Compton; MC `R(E_rec|E_dep)` with non-paralyzable 25 kHz
> censoring) and the v1.1 isotropic-CM flat-box neutron fold over ENDF/B-VIII.0 elastic data are
> **reused, not re-researched**. The previous v1.1 content of this file is superseded here and should
> be archived by the orchestrator to `GPD/milestones/v1.1/literature/METHODS.md` (it is recoverable
> from git in any case). Everything below is the NEW v2.0 methodology for four tasks:
> (1) background transfer across target materials, (2) figure digitization as forward-model input,
> (3) the 100 meV extension, (4) LEE parameterization.

> **Convention conflict to resolve before any plotting.** The user auto-memory records "never display
> QPD spectra/energy axes below 10 eV (grid-floor/binding-artifact territory)". **[RETRACTED 2026-07-22; quoted as history, not as a live rule.]** The v2.0 milestone
> explicitly retracts that floor (`STATE.md`, 2026-07-22). Methods below are written for the retracted
> floor, but Section 3 identifies *physics* reasons the 10 eV guidance was partly right. This must be
> reconciled in CONVENTIONS, not silently.

---

## 0. The one structural decision everything else depends on

**Separate the target-independent incident fluence from the target-dependent response, and never
transfer anything that mixes the two.**

For a thin, low-mass target the background rate factorizes exactly:

```
dR/dT  =  Σ_i N_i ∫ dE  φ(E)  (dσ_i/dT)(E, T)          [counts / keV / kg / day]
          ^^^^^^^^^^^^^  ^^^^  ^^^^^^^^^^^^^^^^
          target-dependent   |  target-dependent kernel
                     target-INdependent fluence at the detector position
```

`φ(E)` (fluence spectrum at the detector position, after all shielding) is target-independent to the
extent that the target does not perturb the field. **Everything NUCLEUS publishes as a deposit
spectrum (their Figs. 8–11) or as a residual rate (their Table 5) is on the wrong side of this line
and must NOT be rescaled to Ge.** Only `φ(E)` transfers.

Quantitative justification of the non-perturbation assumption (HIGH confidence, and it is *stronger*
for NUCLEUS than for us): NUCLEUS targets are 6.8 g CaWO₄ / 4.5 g Al₂O₃; our wafer is ~110 g of Ge,
2 mm thick. Elastic mean free path in Ge is `λ = 1/(Nσ_el) ≈ 5–6 cm` for fast neutrons
(`N ≈ 4.4×10²² cm⁻³`, `σ_el ≈ 3–4 b`), so the 2 mm wafer has interaction probability `t/λ ≈ 3–4%` and
multiple-scatter `~0.1%` — the wafer is optically thin and does not deplete or reshape the field it
sits in. **This is the assumption that makes the whole milestone possible; it must be re-verified for
the 16× larger mass and, separately, for thermal neutrons where Ge's capture cross-section is large
(Section 1.5).**

**Failure condition for this whole approach:** if the Ge wafer's 16× mass / 4″×4″ footprint forces a
change in the inner shield or the veto envelope (already flagged as a gating open question in
PROJECT.md), then `φ(E)` at the detector position is *no longer the NUCLEUS `φ(E)`* and nothing
transfers. **Resolve the geometry-fit question before building on this.**

---

## 1. Task 1 — Transferring a published shielded background to a different target

### 1.1 Recommended primary method: invert NUCLEUS's own deposit spectra for `φ_post-shield(E_n)`

**Do not propagate their Fig. 4 incident spectrum through the shield yourself as the primary route.**
Their Figs. 8–11 are component-resolved *post-shield* deposit spectra on two targets — that is
already an in-situ measurement of `φ_post(E_n)` convolved with a kernel you can write down exactly.
Invert it.

**What it computes.** `φ_post(E_n)` at the detector position inside the full NUCLEUS shield, from the
published neutron-component deposit spectrum on CaWO₄ and/or Al₂O₃.

**Method (analytic, exact under s-wave).** For a single-element target with
`f ≡ T_max/E_n = 4A/(1+A)²` and the isotropic-CM flat box `dσ/dT = σ_el(E_n)/(f E_n)`:

```
G(T) ≡ dR/dT = N ∫_{T/f}^{∞} φ(E) σ_el(E) / (f E) dE
⇒  φ(E) σ_el(E) = −(f² E / N) · G'(f E)          [exact inversion, one derivative]
```

For a multi-element target (`CaWO₄`: f_W = 0.0215, f_Ca = 0.0950, f_O = 0.2215; `Al₂O₃`: f_Al = 0.1378,
f_O = 0.2215) the same differentiation gives a Volterra-type system that is solved by **marching
downward in `T` from the highest `T`**, because at a given `T` the heaviest element samples the
highest `E_n` and is unwound first. Having *two* published targets over-determines the system and
gives the consistency test that makes the Ge transfer credible.

**Cost.** Seconds. One numerical derivative of a digitized curve plus a downward march. Trivially
laptop-scale.

**Accuracy / regime of validity.**
- Exact where the isotropic-CM (s-wave) approximation holds, i.e. `E_n ≲ 0.5–1 MeV` for these
  nuclei. Above that the File-4 Legendre `a₁` forward-peaking breaks the flat box and the inversion
  degrades — apply the same `a₁` correction already scoped in v1.1, or restrict the inversion to
  `E_n < 1 MeV` and take the high-`E_n` tail from the Fig. 4 + attenuation route (Section 1.2).
- Requires their published curve to be the *pure single-scatter elastic nuclear-recoil component*.
  Their spectra are component-resolved, which is what makes this possible, but any inelastic
  `(n,n'γ)`, capture, or multiple-scatter admixture contaminates the inversion. Check by verifying
  the recovered `φ` is non-negative everywhere — negativity is the diagnostic that the kernel is
  wrong.
- **Numerically ill-conditioned in the worst way: it differentiates digitized data.** Do not use
  finite differences. Use a smoothing/penalized spline or Tikhonov/total-variation regularized
  differentiation (Chartrand, *ISRN Appl. Math.* 2011, doi:10.5402/2011/164564), with the
  regularization strength set by the digitization error budget from Section 2.
- Expected fidelity: integral quantities and decade-scale spectral shape to tens of percent; fine
  structure (resonance dips, the Bragg/thermal edge) unrecoverable. That is adequate, because the
  Ge fold is itself an integral over a smooth kernel.

**What would make it inapplicable.** If NUCLEUS's Figs. 8–11 are plotted after their veto cuts
(COV/IV coincidence rejection), the recovered `φ` is not a fluence but a veto-survival-weighted
fluence and is only transferable to Ge if the same veto acceptance applies — which is exactly the
open geometry question. **Check the figure captions for whether they are pre- or post-veto.**

### 1.2 Recommended cross-check method: semi-analytic propagation of their Fig. 4 through the shield

**What it computes.** An independent estimate of `φ_post(E_n)` from the published incident VNS
spectrum (their Fig. 4, obtained by Geant4-transporting the Gordon sea-level spectrum through the VNS
building — *verified from the paper text*).

**Method A — removal cross-section / Albert–Welton kernel (fast-flux integral only).**
`Φ_fast(x) = Φ_fast(0) · exp(−Σ_R x)` with `Σ_R` the macroscopic removal cross-section, using the
empirical rule `Σ_R ≈ (2/3) Σ_T` for fission-energy neutrons and tabulated `Σ_R` for Pb / HDPE / B₄C.
Validity: the Albert–Welton construction *assumes a hydrogenous slab follows the removal material*,
so a first collision with H is equivalent to removal from the fast group. The NUCLEUS stack
(Pb outside 20 cm borated HDPE) satisfies this for the outer layers.

- **Cost:** microseconds. Pure closed form.
- **Accuracy:** conventional shielding-handbook figure is ~10–20% on the *integral fast flux above a
  few MeV* through hydrogenous shields (MEDIUM confidence — this is the standard folklore figure from
  the removal-cross-section literature; treat it as an order-of-magnitude-plus statement, not a
  quoted uncertainty). Cross-checks well against NUCLEUS's own statement that "the first 20-cm thick
  borated HDPE layer reduces by more than one order of magnitude the residual event rate" and B₄C
  gives a further "factor ~5" (verified from the paper text).
- **Hard limitation, and it is the decisive one for this milestone:** the removal method produces
  **no spectrum**. It attenuates the fast group and says nothing about the moderated epithermal and
  thermal populations that the borated HDPE *creates*. Section 3.4 shows that the sub-eV recoil floor
  is dominated by neutrons within a factor of a few of `E_n = T/0.0536`, i.e. by eV-scale neutrons.
  **Removal cross-sections cannot produce the part of the spectrum that dominates the new physics of
  this milestone.** Use them as a sanity bound on the fast integral, never as the sub-keV source.

**Method B — 1-D multigroup transport (this is what actually gives a spectrum).** Model the shield as
a 1-D spherical shell stack (B₄C / PE / Pb / borated HDPE / Pb / scintillator) with an isotropic
external source drawn from the digitized Fig. 4, and run either (i) OpenMC in a 1-D-equivalent
spherical geometry with a cell flux tally and MAGIC or FW-CADIS weight windows, or (ii) a hand-rolled
discrete-ordinates (S_N) solver on a coupled n-γ multigroup library.

- **Cost:** OpenMC with weight windows on a 1-D spherical shell, `10⁷–10⁸` histories, tallying *flux
  in a shell* (not energy deposits in a gram-scale crystal): **minutes to a few hours multithreaded
  on a laptop.** This is a completely different problem from the NUCLEUS Geant4 chain, which
  simulates the full building geometry with a 4π tangent-plane source and scores deposits in gram-scale
  crystals down to sub-keV — that is what is expensive, not shield attenuation per se.
- **This is the honest answer to "does it secretly need Monte Carlo?"** — a *spectral* propagation
  through 30+ cm of moderating shield genuinely requires transport. It does **not** require the
  NUCLEUS-scale simulation. A reduced 1-D shield model is laptop-feasible and is the correct fallback
  if the Section 1.1 inversion fails.
- **Accuracy / limitations:** 1-D geometry loses shield penetrations, the cryostat neck, and streaming
  paths, which in real setups are the dominant term for the last order of magnitude. Expect the 1-D
  result to be an *underestimate* of the residual. Treat it as a lower bound and say so.

### 1.3 Gammas: point-kernel with buildup factors (no MC needed)

The measured VNS gamma ambience (5.03 cm⁻² s⁻¹; ⁴⁰K 59.6, ²³²Th 3.28, ²³⁸U 5.65 Bq/kg) is already the
target-independent input. Propagate through the Pb/PE stack with the standard point-kernel
`Φ = Φ₀ B(μx, E) e^{−μx}` using NIST XCOM `μ(E)` and ANS-6.4.3 / Berger-form buildup factors, then
fold with the existing Klein–Nishina machinery on Ge. Accuracy: 10–30% for slab geometries at a few
mean free paths — well documented and standard. Cross-check against NUCLEUS's stated "factor ~50
reduction" for gammas from the passive materials. **Do not use bare `e^{−μx}` without a buildup
factor**; it under-predicts by factors of several at 3–5 mfp of Pb.

### 1.4 Muons: adopt directly, re-fold the chord/`dE/dx`

Adopt the published overburden (2.92 m.w.e.) and muon attenuation factor (1.41) as scalars applied to
the existing Gaisser–Guan flux. The target dependence is entirely in `ρ dE/dx × chord` and is already
implemented. **No new method is needed here** — this is the one channel that transfers cleanly,
because the incident flux is a scalar-attenuated version of what v1.0 already uses.

### 1.5 The channel that does NOT transfer: Ge-specific thermal-neutron capture (HIGH priority)

**This is the single most important target-dependence finding of this survey.** Behind 20 cm of
borated HDPE + 4 cm B₄C the fast flux is suppressed but the surviving field is *thermalized*. Ge has
a large thermal capture cross-section (natural `σ_th ≈ 2.2 b`, with ⁷⁰Ge ≈ 3.0 b and ⁷³Ge ≈ 15 b) and
produces in-band signatures that CaWO₄ and Al₂O₃ simply do not have:

| Channel | In-band signature | Why it cannot be transferred |
| ------- | ----------------- | ---------------------------- |
| Prompt `(n,γ)` recoil | Nuclear recoil from the ~8 MeV de-excitation cascade; single-γ limit `E_γ²/2Mc² = 473 eV` at 8 MeV, tens of eV for a typical multi-γ cascade | Directly in the 10–100 eV RoI, on the phonon scale, indistinguishable from CEvNS |
| ⁷⁰Ge(n,γ)⁷¹Ge → EC (T½ = 11.4 d) | **M-shell line at 158.7 ± 1.4 eV**, L-shell 1298.5 eV, K-shell 10368.3 eV (measured by CONUS+, arXiv:2604.25748) | Delayed, accumulates with exposure, Ge-only |
| ⁷⁴Ge(n,γ)⁷⁵Ge → β⁻ (T½ = 82.8 min) | β continuum, in-bulk full-energy deposit | Ge-only |

**Method:** thermal-capture rate `R = N_Ge ∫ φ_th(E) σ_(n,γ)(E) dE` using ENDF/B-VIII.0 MF=3/MT=102
for the five Ge isotopes; prompt-cascade recoil from the EGAF/PGAA capture-γ line list with recoil
`Σ_j E_j²/2Mc²` (isotropic-cascade limit) as a bounding estimate; delayed lines from the activation
inventory `A(t) = R(1 − e^{−λt})`. Cost: trivial. **The blocking input is `φ_th` inside the shield**,
which the Section 1.1 inversion does *not* give you (CaWO₄/Al₂O₃ have small thermal cross-sections
and their deposit spectra are blind to the thermal population). This is a genuine gap that requires
either a NUCLEUS-published thermal flux number or the Section 1.2 Method B transport run.
Confidence that this channel matters: HIGH. Confidence in its magnitude: LOW until `φ_th` is fixed.

### 1.6 Material radioactivity: recompute geometry, do not scale

NUCLEUS Table 3 screening results are target-independent *activities* and transfer. Their *rates* do
not: our 110 g / 4″×4″×2 mm wafer has a completely different solid angle to the holder, a different
surface-to-mass ratio, and different self-shielding than a 6.8 g crystal. Recompute with the v1.1
solid-angle × `e^{−μx}` machinery. Ge-bulk cosmogenic activation (³H, ⁶⁸Ge, ⁶⁵Zn) is Ge-only and
carries over from the v1.1 method, re-scaled to the new exposure scenario.

### 1.7 The validation that licenses the whole transfer

**Target-swap closure test.** Feed the recovered `φ_post(E_n)` back through *our own* pipeline with
CaWO₄ and Al₂O₃ kernels and reproduce NUCLEUS's published Figs. 8–11 and their Table 5 in-band value
(~250 dru in 10–100 eV on CaWO₄, verified from the abstract). Only after that closure test passes is
swapping in the Ge kernel defensible. **State the achieved closure percentage in the paper.** This is
the standard forward-model validation pattern and it is what distinguishes a defensible transfer from
a rescaling. Target: agreement within a factor ~1.5 on the in-band integral; if worse than a factor
2, the transfer premise is broken and must be reported as such.

---

## 2. Task 2 — Digitizing published spectra as forward-model inputs

### 2.1 Lethargy vs per-energy: the convention that silently costs a decade

NUCLEUS Fig. 4 is plotted as `E × dΦ/dE` on a log-E axis (**verified from the paper text**). The
identity is:

```
E · dΦ/dE  =  dΦ/d(ln E)  =  dΦ/du    (u = lethargy = ln(E_ref/E), du = −dE/E)
```

so `E dΦ/dE` **is** the per-unit-lethargy fluence up to the sign convention on `u`. The ISO/Bonner
convention is that spectral bins are flat in fluence per unit lethargy, which is why every neutron
spectrometry paper plots this quantity: on a log-E axis, **equal areas under the curve are equal
neutron numbers**. That is the property that makes the plot readable and the property you must
preserve.

**Mandatory conversion and its trap.** To use it as `φ(E)` in the fold:
`dΦ/dE = (E dΦ/dE) / E`. Two failure modes, both silent:
1. **Forgetting the `1/E`.** Produces a spectrum too hard by exactly one power of `E` — the fold
   result is then wrong by orders of magnitude at the low-`E` end that dominates the sub-eV recoil
   floor. Detection: a `1/E`-flat epithermal region must appear *flat* in `E dΦ/dE` and as a `1/E`
   power law in `dΦ/dE`. Check this explicitly; a well-moderated field always shows it.
2. **Ambiguity between `E dΦ/dE` and `dΦ/dlethargy` with a nonstandard `E_ref` or a per-decade
   (`log₁₀`) rather than per-`ln` normalization.** A `log₁₀` convention differs by `ln 10 = 2.303`.
   Detection: integrate the digitized curve and compare against any integral flux quoted in the text.
   **This is a required acceptance test, not optional** — it is the only way to catch a 2.3× error.

### 2.2 Log-axis digitization and error propagation

Use WebPlotDigitizer (automeris.io, v4/v5) with axis calibration explicitly set to *log* on both axes
and calibration points placed as far apart as possible. Reported digitization error under good
practice is <1% of axis span (MEDIUM confidence — from applied-literature usage, not a metrology
study), but on a **log** axis a fixed pixel error is a fixed *fractional* error in the value:

```
Δ(log₁₀ y) = (pixel error / pixels per decade)
⇒ σ_y / y = ln(10) · Δ(log₁₀ y)
```

For a figure with ~150 px/decade and ~2 px placement error, `σ_y/y ≈ 3%`. **Propagate this as a
correlated, not independent, error** — a mis-set calibration point biases the whole curve coherently.
The practical recipe: digitize each curve twice (independently), take the spread as the placement
error, and separately propagate a global multiplicative calibration uncertainty. Project precedent:
NUCLEUS 2019 Fig. 1 Ge curve was reproduced to 5% — take **5% correlated + ~3% point-to-point** as
the working budget for the Fig. 4 digitization and record it in CONVENTIONS.

**Cross-decade caution:** Fig. 4 spans ~10 decades of energy. Placement error in `x` on a log axis is
also fractional, so a 2 px `x` error at 150 px/decade is a 3% energy error — which matters near a
threshold (`E_min(T)`) where the integrand is steep.

### 2.3 Re-binning onto the shared grid while conserving the integral

**Never interpolate a differential spectrum directly.** Interpolate its **cumulative** and
differentiate — that is the only scheme that conserves the integral by construction.

**Recommended algorithm (integral-conserving / "flux-conserving" resampling):**
1. Build `C(E) = ∫_{E₀}^{E} φ(E') dE'` on the digitized nodes using trapezoid-in-`log E` (equivalently
   `∫ (E φ) d ln E`), which is the natural quadrature for a log-spaced digitization.
2. Monotone-interpolate `C` (PCHIP — monotonicity-preserving; **not** a natural cubic spline, which
   overshoots and can produce negative `φ`).
3. `φ_new(bin) = [C(E_hi) − C(E_lo)] / (E_hi − E_lo)` per target bin.

**Cost:** milliseconds. **Reference implementations:** `SpectRes` (Carnall, arXiv:1705.05165) and
`specutils.FluxConservingResampler` implement exactly this for astronomical spectra; the algorithm is
identical here. Either use them or implement the three steps above (≈20 lines) so the log-E
quadrature is under your control.

**Acceptance tests (make these unit tests):**
- `∫ φ_new dE == ∫ φ_orig dE` to `<0.1%` over the overlap region.
- Re-binning a pure `1/E` spectrum onto the shared 80-bin/decade grid returns `1/E` to machine
  precision.
- Round-trip: rebin to a coarse grid and back; integral preserved, shape degraded only by resolution.
- `φ_new ≥ 0` everywhere (catches spline overshoot).

**Extrapolation policy (must be explicit).** The digitized Fig. 4 has a lowest plotted energy `E_low`.
Below it, `φ` is **unknown, not zero**. Because the flat-box fold at recoil `T` samples `φ` from
`E = T/0.0536` upward, any `T < 0.0536 · E_low` is *not computed* — it is truncated. Carry a
`valid_below` flag on the flux table and refuse (or explicitly band) the fold below that recoil energy.
The v1.1 pattern of an explicit placeholder band (already used for the sub-1.8 MeV reactor flux) is the
right precedent.

---

## 3. Task 3 — Extending the pipeline to 100 meV

### 3.1 What the numerics actually cost (short answer: nothing)

Extending `shared_energy_grid()` from 10.14 eV to 0.1 eV at 80 bins/decade adds ~160 bins to ~585 —
a 27% increase. All 1-D quadratures scale linearly. **Numerics are not the obstacle.** The obstacles
are three physics-validity gates (3.2, 3.3, 3.5) and one quadrature pathology (3.4).

### 3.2 Gate 1 — the free-nuclear-recoil (impulse) approximation breaks near 100 meV

This is the decisive finding for the 100 meV target. Using the harmonic-crystal framework of
**Campbell-Deem, Knapen, Lin & Villarama, PRD 106, 036019 (2022), arXiv:2205.02250** (which explicitly
provides numerical results for Ge):

- **Impulse-approximation criterion:** `q ≫ √(2 m_d ω̄_d)`, equivalently `E_r ≫ ω̄`, where `ω̄` is the
  typical phonon energy. For Ge, `ω̄ ≈ 20–37 meV` (Debye `k_Bθ_D ≈ 32 meV` at `θ_D = 374 K`; zone-centre
  optical phonon ≈ 37 meV).
- **At `T = 100 meV`:** `q = √(2M_Ge T) = 116 keV` versus `q_crit = √(2M_Ge ω̄) = 52–71 keV`.
  Ratio 1.6–2.2, i.e. `E_r/ω̄ ≈ 2.7–5`. The paper's own phrasing is that the free nuclear recoil
  description breaks down "when the recoil energy is comparable to a few times the typical phonon
  energy." **We are sitting exactly on that boundary at the 100 meV floor.**
- **At `T = 1 eV`:** `E_r/ω̄ ≈ 27–50` — impulse approximation solid.
- **At `T = 10 eV`:** solid, and this is where the current floor sits.

**Verdict:** the CEvNS/neutron recoil rate computed with free-nucleus kinematics is reliable above
~1 eV, carries O(1) corrections between ~100 meV and ~1 eV, and is not defensible below ~30 meV.
**Report 100 meV–1 eV as a band with an explicit "free-nucleus kinematics, O(1) multiphonon
correction not applied" caveat, or compute the correction (3.3).**

### 3.3 What is NOT a problem: Bragg coherence and the nuclear form factor

Two things that intuitively sound like they should matter at 100 meV, and do not:

- **Bragg / lattice coherence.** The incoherent–coherent transition is at `q ≈ q_BZ = 2π/a`; for Ge
  (`a = 5.658 Å`) that is `q_BZ ≈ 2.19 keV`, corresponding to a recoil energy of **35 μeV** — 3.5
  decades below the 100 meV floor. At 100 meV, `q/q_BZ ≈ 53`. **The incoherent approximation is
  valid throughout the entire extended range; no Bragg/Debye–Scherrer treatment is needed for the
  recoil kernel.** (Campbell-Deem et al. state the incoherent approximation is *most* justified at
  large `q`.)
- **Debye–Waller.** `2W(q) = q²⟨u²⟩`; with `⟨u²⟩ ≈ 0.0025 Å²` for Ge at mK (from `B ≈ 0.2 Å²`),
  `2W ≈ 8.7` at `T = 100 meV` and `≈ 87` at 1 eV. `e^{−2W} ≈ 2×10⁻⁴` at 100 meV: the *zero-phonon
  (coherent elastic)* channel is essentially extinct, which is precisely the statement that all the
  strength has moved into the multiphonon continuum — i.e. Debye–Waller **suppresses the wrong
  channel to worry about**, and its role is bookkeeping inside the multiphonon expansion, not a
  correction factor to apply to the free-recoil rate. Do not multiply the CEvNS rate by `e^{−2W}`;
  that is a classic and severe error.
- **Nuclear form factor.** Helm `F(q) → 1` to better than `10⁻⁶` for `q ≲ 1 MeV`. Set `F = 1` below
  ~1 keV recoil and skip the Bessel evaluation entirely (avoids the `j₁(x)/x` `0/0` cancellation at
  small `x`, which is a real floating-point trap — use the series `j₁(x)/x → 1/3 − x²/30` for
  `x < 10⁻³`).

**Recommended tool if the multiphonon correction is to be computed:** `DarkELF`
(Knapen, Kozaczuk & Lin, PRD 105, 015014 (2022), arXiv:2104.12786; github.com/tongylin/DarkELF), which
ships precomputed Ge phonon DOS and implements the single-phonon→multiphonon→nuclear-recoil
interpolation from arXiv:2205.02250. **Caveat with teeth:** DarkELF computes *dark matter* rates. The
lattice/dynamic-structure-factor part is what you want; the coupling structure (`f_d` per atom) must
be replaced by the CEvNS weak charge `Q_W`. Since Ge is monatomic, the substitution is a clean
rescaling of a single per-atom coupling — this is the one target where the transfer is unambiguous.
Stated accuracy of the underlying method: single-phonon analytic vs DFT agree "within an O(1)
factor"; the incoherent two-phonon result is "within a factor of ~5" of the long-wavelength result
and can underestimate by up to an order of magnitude when anharmonicity matters. **So the correction
itself is only order-of-magnitude.** That is an honest reason to *band* rather than *correct*.

### 3.4 The quadrature pathology: `E_min(T)` marching into the flux floor

Both folds have a `T`-dependent lower limit:

| Channel | `E_min(T)` | At `T = 100 meV` | At `T = 10 eV` |
| ------- | ---------- | ---------------- | -------------- |
| CEvNS | `√(M T/2)` | **58.2 keV** | 582 keV |
| Neutron elastic (Ge) | `T / 0.0536` | **1.87 eV** | 187 eV |

**Neutron channel — this is the dangerous one.** For an epithermal `1/E` flux and slowly varying
`σ_el`, the integrand of the flat-box fold goes as `φ σ /(f E) ∝ 1/E²`, so
`dR/dT ∝ ∫_{T/f}^∞ dE/E² = f/T`. **The sub-eV neutron recoil spectrum rises as `1/T` and is dominated
entirely by neutrons within a factor of a few of `E_min(T)`.** Consequences:
- The 100 meV bin is controlled by `φ(E_n ≈ 2–10 eV)` — the epithermal region that the shield
  *creates* by moderation, that the removal-cross-section method cannot predict, and that the
  Section 1.1 inversion recovers only if NUCLEUS's deposit spectra extend low enough.
- **Adaptive quadrature (`scipy.integrate.quad`) will silently under-resolve this.** The integrand is
  a near-singular endpoint spike. Fix: substitute `u = ln E` (making the `1/E²` integrand a decaying
  exponential in `u`), use fixed-order Gauss–Legendre on log-spaced panels with the first panel
  anchored exactly at `E_min(T)`, and pass `points=[E_min]` if `quad` is used at all. Validate with a
  monoenergetic `δ`-function flux — the fold must return an exact flat box of height `σ/(f E₀)` and
  width `f E₀`, integrating to `N σ`.
- **Truncation must be explicit.** If the digitized `φ` floors at `E_low`, then `dR/dT` is truncated
  for `T < 0.0536 E_low`. With `E_low` anywhere above ~2 eV the entire sub-100 meV region is a
  fabrication. Enforce a hard `valid_below` guard.

**CEvNS channel — benign, and quantifiably so.** `dσ/dT ∝ (G_F² Q_W² M/4π)(1 − MT/2E²) → const` as
`T → 0`, so `dR/dT` **plateaus** at low `T` rather than diverging. Lowering `T` from 10 eV to 100 meV
only widens the integration range from `E ≥ 582 keV` to `E ≥ 58 keV`. The frozen flux table floors at
100 keV, so the *missing* contribution is bounded by the antineutrino number flux in 58–100 keV as a
fraction of the total: **bound it by an integral-number-flux argument rather than modelling an
unmeasured spectrum.** Recommended: carry the 58–100 keV band as an explicit additive uncertainty on
`dR/dT(T < 0.29 eV)`, computed as `ΔΦ(58–100 keV) × (G_F²Q_W²M/4π) × N_Ge`, with `ΔΦ` bounded above by
a beta-summation estimate and below by zero. This is a *bounded, quotable* uncertainty, not a
placeholder — a genuine improvement over extending the placeholder band downward.

### 3.5 Gate 3 — the response chain below the per-sensor saturation onsets

The v1.0 `E_rec ≈ 0.5 · E_dep` mapping rests on a lumped ~50% deposited-to-signal efficiency derived
for a fully developed phonon cascade. At `E_dep = 100 meV` the deposit is only ~3 Ge optical-phonon
quanta (`ħω_LO ≈ 37 meV`). The pair-breaking budget is fine (`100 meV ≫ 2Δ_Al ≈ 0.34 meV`), but the
statistical basis of a lumped collection efficiency across ~10,300 sensors is not — a few-quantum
deposit reaches one or a few sensors, not the array. **Recommendation: below ~1 eV deposit, do not
report `dR/dE_rec`; report a detection/trigger probability curve instead**, and state that the
energy-reconstruction interpretation of the response matrix does not extend there. This is the
partly-correct core of the original 10 eV display floor guidance, and it should be preserved as a
*labelled regime boundary* rather than as a hard plotting ban.

### 3.6 The sub-eV neutron kernel: free-atom elastic fails below ~5 eV

The ENDF free-atom elastic representation is conventionally valid above the ~5 eV thermal cutoff;
below it, chemical binding and lattice dynamics require the thermal scattering law `S(α,β)`. Since
`E_min(100 meV) = 1.87 eV`, **the very bottom of the extended range uses the neutron kernel in a
regime where the ENDF free-atom `σ_el` is not the right object.** Options:

- **Germanium appears not to be present in the ENDF/B-VIII.0 / VIII.1 TSL sublibrary** (published
  material lists cover water, Be, BeO, CaH₂, plastics, graphite, HF, oils, ZrH/YH/LiH/LiD, FLiBe, SiC,
  SiO₂, ZrC, and fuels — no Ge). **MEDIUM confidence: verify directly against the IAEA TSL database
  before relying on this.**
- **Recommended: NCrystal** (Cai & Kittelmann, *Comput. Phys. Commun.* 246, 106851 (2020),
  arXiv:1901.08890; github.com/mctools/ncrystal), which ships a validated `Ge_sg227.ncmat` crystal
  definition and computes coherent-elastic (Bragg), incoherent-elastic and inelastic (phonon)
  cross-sections from unit-cell parameters. C++/C/Python bindings, pip/conda installable, runs in
  seconds on a laptop. Use it to generate `σ(E_n)` for Ge from 10⁻⁵ eV to ~5 eV and splice onto the
  ENDF free-atom curve above 5 eV, with the splice discontinuity reported.
- **Fallback:** carry the 100 meV–1 eV recoil band with an explicit "free-atom kernel, binding
  correction not applied" flag. Given that the sub-eV floor is anyway gated by `φ_th` (Section 1.5),
  a band is defensible for a first estimate.

---

## 4. Task 4 — Carrying the low-energy excess as a parameterized input

### 4.1 The framing that published work actually uses

NUCLEUS explicitly discusses the LEE in the introduction of arXiv:2509.03559 and explicitly **excludes
it from the particle-background budget**, on the stated grounds that it "seems not tied to
particle-induced backgrounds but rather to fundamental aspects in the design of their respective
detection setups" (verified from the paper text). That is the published precedent and it is a
*scoping* decision, not a physics result. The defensible options, in order of increasing claim
strength:

| Method | What it delivers | When to use | Cost |
| ------ | ---------------- | ----------- | ---- |
| **Explicit exclusion + named gap** (NUCLEUS's own choice) | A particle-background budget with a stated, quantified regime of validity ("valid above X eV, LEE-free assumption") | When the goal is a particle-background prediction and the LEE is device-specific | zero |
| **Parameterized nuisance component with a scan band** | S/B as a *function* of an assumed LEE amplitude and index, rather than a single number | **Recommended here** — this is a sensitivity study, and the LEE is the dominant sub-100 eV term | trivial |
| **Yellin optimum-interval / maximum-gap** | A conservative exclusion limit valid with *no* background model at all | When converting to a DM/new-physics limit in a later milestone | trivial |
| **Profile-likelihood with the LEE as a free-shape nuisance** | Statistically correct signal extraction | Only when real data exist | n/a |

### 4.2 Recommended: two-parameter power-law nuisance component with an explicit scan

**Parameterization.** `dR/dE_LEE = A · (E / E₀)^{−α}` with `E₀ = 100 eV` a fixed pivot. Published
descriptions consistently use a power law; a reported spectral index for silicon and germanium
excess rates is `α = 3.43` (MEDIUM confidence — from the semiconductor excess-rate literature; the
CRESST/NUCLEUS cryogenic LEE is a different device class and its index differs). CRESST-III also
reports the LEE *amplitude* decaying with time after cooldown, itself described by a power law — so
`A` is not even a constant, and any single number must be tagged with an assumed time-since-cooldown.

**How to carry it defensibly:**
1. **Do not fit it, do not predict it, do not omit it.** Declare `(A, α)` as *scenario inputs* with
   the same provenance-tagging discipline the project already applies to `φ(E_n)` normalizations.
2. **Anchor `A` to a published measurement on a comparable device**, tagged with target material,
   sensor type, absorber mass, and time since cooldown. Ge-absorber phonon detectors, sapphire, and
   CaWO₄ all show LEE with different amplitudes — the anchor must be named and its
   non-transferability stated.
3. **Report S/B as a 2-D contour over `(A, α)`**, not a single number, plus the two limiting cases
   `A = 0` ("LEE-free, comparable to the NUCLEUS budget") and `A = A_published` ("LEE at the observed
   level"). This is the honest structure: it makes the reader's own assumption the input.
4. **Compute and report the break-even LEE amplitude** — the `A` at which S/B = 1 in the 10–100 eV
   RoI. This is a genuine, falsifiable, computable result that does not require knowing `A`, and it
   is the most useful single number the milestone can produce about the LEE.
5. **Never fold the LEE through `R(E_rec|E_dep)`.** The LEE is measured *in reconstructed energy* on
   the devices that report it; treating it as a deposit spectrum and folding it double-counts the
   response. Add it directly on the `E_rec` axis, and say so.

**What would make this inapplicable.** If the LEE mechanism is sensor-substrate-interface-specific
(several candidate mechanisms — stress relaxation, interfacial thermal contraction, aluminum
relaxation, spontaneous phonon bursts in bulk Si — point that way), then a QPD-on-Ge device has no
published analogue at all and even the anchored `A` is a placeholder. **Say that explicitly rather
than borrowing a CRESST number and implying it applies.** The break-even calculation (item 4) is the
result that survives this objection.

### 4.3 Community reference for the phenomenology

The EXCESS workshop series is the standing community forum for LEE descriptions across experiments
and is the correct citation for "no first-principles model exists." The current review-level entry
point verified in this survey is **"Low-Energy Backgrounds in Solid-State Phonon and Charge
Detectors," arXiv:2503.08859**, plus **NUCLEUS's own Al₂O₃ LEE characterization, arXiv:2603.07687**
(target-matched to NUCLEUS's own detectors — the closest thing to a site-matched anchor).
**Verification note:** both were surfaced by WebSearch with titles and arXiv IDs but their full texts
were not read in this survey. **Read them before quoting any number from them.**

---

## Recommended Methods

### Analytical Methods

| Method | Purpose | Why Recommended | Cost / Scaling |
| ------ | ------- | --------------- | -------------- |
| Flux/response factorization `dR/dT = Σ_i N_i ∫ φ dσ_i/dT` | Separates what transfers (`φ`) from what does not (kernel) | The only formulation in which a published background can be legitimately moved to a new target; everything else is rescaling | O(N_bins) |
| Analytic inversion of the flat-box fold, `φσ = −(f²E/N) G'(fE)` | Recover `φ_post-shield(E_n)` from NUCLEUS's published deposit spectra | Closed form, exact under s-wave; over-determined by their two published targets → built-in consistency test | seconds |
| Albert–Welton removal cross-section, `Φ = Φ₀ e^{−Σ_R x}`, `Σ_R ≈ ⅔Σ_T` | Fast-group integral attenuation through the Pb/borated-HDPE stack | Closed form; validates against NUCLEUS's own ">1 order of magnitude" and "factor ~5" statements | microseconds |
| Point-kernel + buildup, `Φ = Φ₀ B(μx,E)e^{−μx}` | Gamma attenuation through the shield | Standard, 10–30% accurate at a few mfp; no MC needed | microseconds |
| Isotropic-CM flat-box recoil kernel (REUSE v1.1) | Ge recoil spectrum from any `φ(E_n)` | Exact for `E_n ≲ 0.5–1 MeV`; already implemented and validated | O(N_bins) per `T` |
| Impulse-approximation validity criterion `q ≫ √(2Mω̄)` / `E_r ≫ ω̄` | Decide where free-nucleus kinematics may be used | Quantitative, target-specific gate; places the boundary at `E_r ≈ 30 meV` for Ge | closed form |
| Integral-conserving (cumulative-then-differentiate) re-binning | Move digitized `φ` onto the shared grid | Only scheme that conserves `∫φ dE` by construction | O(N log N) |
| Thermal-capture activation `A(t) = N∫φ_th σ_(n,γ)(1−e^{−λt})` | Ge-only ⁷¹Ge/⁷⁵Ge in-band lines | Ge-specific channel absent from CaWO₄/Al₂O₃ — cannot be transferred, must be computed | trivial |
| Break-even LEE amplitude (solve S/B = 1 for `A`) | The LEE result that survives not knowing `A` | Converts an unknown into a falsifiable statement | trivial |

### Numerical Methods

| Method | Purpose | When to Use | Cost |
| ------ | ------- | ----------- | ---- |
| Tikhonov / total-variation regularized differentiation | Differentiate a digitized deposit spectrum without amplifying digitization noise | Required by the Section 1.1 inversion; naive finite differences will fail | seconds |
| Log-substituted fixed-order Gauss–Legendre on panels anchored at `E_min(T)` | Evaluate `∫_{E_min(T)}^∞ φ dσ/dT dE` near the endpoint spike | Mandatory below ~10 eV recoil where the neutron integrand is `∝1/E²` | ms per `T` |
| PCHIP monotone interpolation of the cumulative | Re-binning without overshoot / negative flux | Every digitized-input rebin | ms |
| 1-D spherical OpenMC with MAGIC or FW-CADIS weight windows | Spectral neutron propagation through the shield stack | **Only if the Section 1.1 inversion fails or `φ_th` is needed.** 10⁷–10⁸ histories, flux tally in a shell | minutes–hours, laptop-feasible |
| Extended `shared_energy_grid()` (0.1 eV → 200 MeV, 80/decade, ~745 bins) | Common axis for all v2.0 channels | Everywhere; response matrix must be regenerated on it | linear in bins |
| Bespoke thin-wafer single-scatter MC (REUSE v1.1 `_mc_batch` pattern) | Cross-check the analytic fold, `a₁` forward-peaking, edge geometry | Verification only | minutes |

### Computational Tools

| Tool / Library | Version | Purpose | Notes |
| -------------- | ------- | ------- | ----- |
| WebPlotDigitizer | v4/v5 (automeris.io) | Digitize NUCLEUS Figs. 4, 8–11 | Set **both** axes to log explicitly; place calibration points far apart; digitize twice for a placement-error estimate |
| numpy / scipy | existing repo pins | All folds, quadrature, PCHIP, regularized differentiation | `scipy.interpolate.PchipInterpolator`, `scipy.integrate.fixed_quad` |
| NCrystal (`ncrystal`) | current (≥3.x) | Ge sub-5 eV neutron cross-sections incl. Bragg/incoherent/inelastic | `Ge_sg227.ncmat` is in the shipped data library; pip/conda; seconds to evaluate |
| DarkELF | current | Ge phonon DOS + multiphonon `S(q,ω)`, single-phonon→nuclear-recoil interpolation | github.com/tongylin/DarkELF; **DM couplings must be replaced by `Q_W`** |
| OpenMC | ≥0.14 | 1-D shield transport fallback + weight-window generation | Conda; needs an HDF5 cross-section library (ENDF/B-VIII.0 pre-generated set) |
| ENDF/B-VIII.0 MF=3 MT=2/102, MF=4 | 2018 | Ge elastic + capture cross-sections, Legendre `a₁` | Already acquired in Phase 7 for elastic; **capture (MT=102) is new for v2.0** |
| EGAF / PGAA capture-γ line lists | current | Prompt `(n,γ)` cascade energies for the recoil estimate | IAEA database |
| NIST XCOM | web/DB | `μ(E)` for Pb/PE/Ge, point-kernel gamma attenuation | Already used in v1.1 |
| `SpectRes` / `specutils` | current | Reference integral-conserving resampler | Optional — the 20-line implementation is preferable for log-E control |

## Software Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
| ---------- | ------- | ------- | --------------- |
| Python + numpy/scipy | existing | Every fold, inversion, rebin, and response convolution | The entire v1.0/v1.1 pipeline is numpy/scipy; all v2.0 channels plug into `shared_energy_grid()` and `R(E_rec\|E_dep)` |
| Committed static data tables (`data/`) — digitized Fig. 4, recovered `φ_post`, Ge `σ_el`/`σ_(n,γ)`, NCrystal-generated sub-5 eV kernel | in-repo CSV | Reproducibility without heavy runtime deps | Matches the existing `data/` + `src/flux/build_flux_table.py` pattern; digitized inputs **must** be committed with their provenance and error budget |
| NCrystal | ≥3.x | Sub-5 eV Ge neutron kernel | Only laptop-scale route to bound-atom Ge cross-sections; Ge is in the shipped data library |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
| ------- | ------- | ------- | ----------- |
| `openmc` | ≥0.14 | 1-D shield transport fallback | **Only** if Section 1.1 fails; keep out of the runtime critical path |
| `darkelf` | current | Multiphonon `S(q,ω)` for Ge | Only if the 100 meV–1 eV band is to be corrected rather than banded |
| `pandas` | existing | Table I/O for digitized/derived spectra | Same role as v1.0/v1.1 |
| `radioactivedecay` | current | ⁷¹Ge/⁷⁵Ge decay data, EC line intensities | Ge activation inventory |

### Symbolic Computation

| Tool | Version | Purpose | Notes |
| ---- | ------- | ------- | ----- |
| (none required) | — | The flat-box inversion and the DW/impulse criteria are elementary closed forms | Keep everything numeric, as in v1.0/v1.1 |

## Installation

```bash
# Reuse the existing environment
uv sync

# New v2.0 runtime dependency (sub-5 eV Ge neutron kernel)
pip install ncrystal

# Optional / conditional (NOT runtime critical path)
pip install darkelf              # only if the multiphonon correction is computed
conda install -c conda-forge openmc   # only if the 1-D shield transport fallback is needed

# Static data to acquire and commit to data/ (one-off):
#   - digitized NUCLEUS Fig. 4 (E dPhi/dE, log-E) + error budget
#   - digitized NUCLEUS Figs. 8-11 neutron-component deposit spectra (CaWO4, Al2O3)
#   - ENDF/B-VIII.0 MT=102 (n,gamma) for 70,72,73,74,76-Ge
#   - EGAF prompt capture-gamma line lists for Ge
#   - NCrystal-generated sigma(E_n) for Ge, 1e-5 eV to 5 eV
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
| ----------- | ----------- | ----------------------- |
| Invert NUCLEUS's deposit spectra for `φ_post` (1.1) | Propagate Fig. 4 through the shield yourself (1.2) | If their figures are post-veto, cover too narrow a `T` range, or the recovered `φ` goes negative (kernel mismatch). Then the 1-D OpenMC route is required, not optional. |
| Removal cross-sections as a *fast-flux sanity bound* | Removal cross-sections as the primary shield model | Never. They produce no spectrum and are blind to the moderated epithermal population that dominates the sub-eV floor. |
| 1-D spherical OpenMC | Full 3-D Geant4/MCNP with the real geometry | Only if shield penetrations/streaming become load-bearing. Explicitly out of scope: this is the NUCLEUS-scale calculation the milestone is designed to avoid. |
| Band the 100 meV–1 eV recoil region | Compute the multiphonon correction with DarkELF | If a reviewer demands a number rather than a band. Note the underlying method is itself only O(1)/factor-few accurate, so the correction does not remove the band — it recentres it. |
| NCrystal for sub-5 eV Ge | ENDF TSL `S(α,β)` via NJOY/THERMR | If a Ge TSL evaluation turns out to exist (verify against the IAEA TSL database). NCrystal is preferable regardless for laptop-scale use. |
| Power-law LEE nuisance with a 2-D scan | Single "best-guess" LEE amplitude | Never for this milestone — there is no QPD-on-Ge LEE measurement to anchor a single number to. |
| Break-even LEE amplitude | Omitting the LEE (NUCLEUS's choice) | Omission is acceptable *only* if the resulting budget is explicitly labelled "particle backgrounds, LEE-free" and the RoI conclusion is stated as conditional. |

## What NOT to Use

| Avoid | Why | Use Instead |
| ----- | --- | ----------- |
| Rescaling NUCLEUS's Table 5 residual rates or Figs. 8–11 deposit spectra to Ge by `N²/A`, mass, or `T_max` ratio | These are `φ ⊗ kernel` products; rescaling them applies the CaWO₄/Al₂O₃ kernel to Ge and silently transfers `T_max/E_n = 0.0215` (W) as if it were 0.0536 (Ge) — a ~2.5× shape error in exactly the RoI | Extract `φ_post`, re-fold with the Ge kernel |
| Bare `e^{−μx}` for gammas through 5 cm Pb | Under-predicts by factors of several at 3–5 mfp | Point-kernel with ANS-6.4.3 buildup factors |
| Using `E dΦ/dE` directly as `φ(E)` in the fold | Off by one power of `E`; catastrophic at the low-`E` end that dominates the sub-eV floor | Divide by `E`; verify a `1/E` region appears flat in the lethargy plot |
| Linear or cubic-spline interpolation of a differential spectrum onto a new grid | Does not conserve `∫φ dE`; splines overshoot and can produce negative flux | PCHIP on the cumulative, then differentiate |
| `scipy.integrate.quad` on the neutron fold below ~10 eV recoil without `points=[E_min]` or a log substitution | Integrand is a near-singular endpoint spike (`∝1/E²`); adaptive refinement misses it and returns a silently wrong, too-small answer | Log-substituted fixed-order Gauss–Legendre with the first panel anchored at `E_min(T)` |
| Multiplying the CEvNS rate by the Debye–Waller factor `e^{−2W}` | `e^{−2W} ≈ 2×10⁻⁴` at 100 meV; this suppresses the *zero-phonon* channel, not the total rate. Applying it would wipe out a real signal by 4 orders of magnitude | Use the free-nucleus rate above ~1 eV; band or multiphonon-correct below |
| Bragg / Debye–Scherrer treatment of the CEvNS recoil kernel | `q/q_BZ ≈ 53` at 100 meV — the incoherent approximation is valid throughout | Incoherent (single-atom) kernel everywhere in the extended range |
| ENDF free-atom `σ_el` for Ge below ~5 eV | Chemical binding / lattice dynamics dominate; the free-atom form is not the right object there | NCrystal `Ge_sg227.ncmat`, spliced at 5 eV |
| Folding the LEE through `R(E_rec\|E_dep)` | LEE is measured *in reconstructed energy*; folding it double-counts the response | Add on the `E_rec` axis directly |
| Reporting `dR/dE_rec` below ~1 eV deposit | The lumped 50% collection efficiency is not defensible for a ~3-phonon-quantum deposit reaching one sensor rather than the array | Report a trigger/detection probability curve and label the regime boundary |
| Full Geant4/MCNP 3-D shield simulation | The explicit scoping constraint of this project; NUCLEUS's own chain is the thing being avoided | 1.1 inversion; 1-D OpenMC only if forced |

## Method Selection by Problem Type

**If the goal is the residual neutron NR spectrum on Ge behind the NUCLEUS shield:**
- Use the Section 1.1 analytic inversion of their CaWO₄/Al₂O₃ deposit spectra to get `φ_post(E_n)`,
  cross-checked against removal-cross-section attenuation of their Fig. 4 for the fast integral, then
  re-fold with the Ge flat-box kernel.
- Because this is the only route that separates the target-independent fluence from the kernel, and it
  comes with a built-in two-target consistency test.

**If the goal is the thermal-capture / activation contribution on Ge:**
- Use ENDF MT=102 + EGAF cascade lines + `A(t)` inventory, gated on `φ_th` inside the shield.
- Because Ge's thermal channels (⁷¹Ge M-shell 158.7 eV, prompt-cascade recoil up to ~473 eV) are
  absent from CaWO₄/Al₂O₃ and therefore *cannot* be inferred from anything NUCLEUS publishes. If
  `φ_th` cannot be obtained, this channel is **blocked** and must be reported as an unquantified gap,
  not as zero.

**If the goal is spectra between 1 eV and 10 eV:**
- Use the existing free-nucleus kernels with the log-substituted quadrature fix and the extended grid.
- Because both the impulse approximation (`E_r/ω̄ ≈ 27–270`) and the free-atom neutron kernel
  (`E_n ≥ 19 eV`) are solidly valid there. **This band is a clean, defensible win.**

**If the goal is spectra between 100 meV and 1 eV:**
- Use the same kernels but report a band with two named caveats (multiphonon O(1); bound-atom neutron
  kernel), and either splice NCrystal below 5 eV or flag the omission.
- Because this is a genuine transition regime, not a numerical difficulty.

**If the goal is S/B in the 10–100 eV RoI including the LEE:**
- Report a 2-D `(A, α)` contour plus the break-even amplitude, with `A = 0` shown as the
  "LEE-free / NUCLEUS-comparable" limit.
- Because no QPD-on-Ge LEE measurement exists and a single number would be an overclaim.

## Validation Strategy by Method

| Method | Validation Approach | Key Benchmarks |
| ------ | ------------------- | -------------- |
| Flux/response separation + inversion | **Target-swap closure:** feed recovered `φ_post` back through CaWO₄ and Al₂O₃ kernels and reproduce NUCLEUS Figs. 8–11 and Table 5 | ~250 dru in 10–100 eV on CaWO₄ (their stated in-band value); agreement target factor ≲1.5, break condition factor >2 |
| Analytic flat-box inversion | Recovered `φ` non-negative everywhere; the two targets must yield a consistent `φ` | Non-negativity is the kernel-mismatch diagnostic |
| Removal cross-section attenuation | Compare against NUCLEUS's stated ">1 order of magnitude" (20 cm borated HDPE) and "factor ~5" (B₄C) | Their own published layer factors |
| Gamma point-kernel + buildup | Compare against NUCLEUS's stated "factor ~50" passive gamma reduction | Their own published factor |
| Fig. 4 digitization | Integrate the digitized `E dΦ/dE` in lethargy and compare to any integral flux quoted in their text; verify a flat epithermal plateau (= `1/E` in `dΦ/dE`) | Catches the missing-`1/E` and `ln10` convention errors — **the only tests that catch a 2.3× error** |
| Integral-conserving rebin | `∫φ dE` preserved to <0.1%; `1/E` input returns `1/E` to machine precision; round-trip test; `φ ≥ 0` | Unit tests |
| Neutron fold quadrature | Monoenergetic `δ`-flux must return an exact flat box, height `σ/(fE₀)`, width `fE₀`, integral `Nσ`; `dR/dT ∝ 1/T` for a `1/E` flux | Analytic limiting cases |
| Extended grid + response | `T_max/E_n = 0.0536` (natural Ge) preserved; `E_min(100 meV) = 58.2 keV` (CEvNS) and `1.87 eV` (neutron); count conservation across the regenerated `R(E_rec\|E_dep)` | Recomputed above; project quotes 58.7 keV — reconcile the ~1% difference (isotopic-mass convention) |
| Impulse-approximation gate | Recompute `q(T)` vs `√(2Mω̄)` and `2W = q²⟨u²⟩` on the actual grid; verify `q/q_BZ ≫ 1` throughout | `q_BZ ↔ T = 35 μeV`; `E_r = ω̄ ↔ T ≈ 30 meV`; `2W(100 meV) ≈ 8.7` |
| Ge activation lines | Reproduce ⁷¹Ge M/L/K at 158.7 / 1298.5 / 10368.3 eV | CONUS+ measurement, arXiv:2604.25748 |
| LEE parameterization | Verify that `A = 0` reproduces the LEE-free budget exactly, and that the break-even `A` is independent of the assumed `α` to within the stated band | Internal consistency |

## Version Compatibility

| Component | Compatible With | Notes |
| --------- | --------------- | ----- |
| Extended `shared_energy_grid()` (0.1 eV → 200 MeV) | All v1.0/v1.1 channels | **`R(E_rec\|E_dep)` must be regenerated** on the extended grid; every archived v1.x spectrum must be re-gridded or explicitly tagged as valid only above 10.14 eV |
| NCrystal Ge kernel | ENDF/B-VIII.0 free-atom `σ_el` | Splice at 5 eV; report the discontinuity magnitude as a systematic |
| DarkELF Ge | CEvNS coupling | DM coupling `f_d` → `Q_W`; valid because Ge is monatomic. **Do not use DarkELF for CaWO₄/Al₂O₃ closure tests** — multi-atom coupling assignment is ambiguous there |
| OpenMC 1-D shield model | Digitized Fig. 4 as source | Source must be converted to `dΦ/dE` first (Section 2.1) |
| VNS scenario (2×4.25 GW_th, 72/102 m, 2.1×10¹² ν̄/cm²/s, 80% duty) | v1.0 3 GW_th / 25 m results | Mutually exclusive scenarios — never co-plot without labelling; signal ratio ≈ 1/3.6 |

## Sources

**Verified in this survey (fetched or search-confirmed with title + identifier):**

- NUCLEUS Collab. (H. Abele et al.), "Particle background characterization and prediction for the
  NUCLEUS reactor CEνNS experiment," *Eur. Phys. J. C* 86, 29 (2026),
  doi:10.1140/epjc/s10052-025-15168-9, arXiv:2509.03559. **Full text fetched.** Confirms: Fig. 4 is
  `E×dΦ_n/dE` on log-E, obtained by Geant4-transporting the Gordon sea-level spectrum through the VNS
  building; shield layers (20 cm 5%-borated HDPE, 5 cm low-activity Pb, 5 cm plastic-scintillator muon
  veto; internal 4 cm B₄C + cold muon veto); per-layer factors (">one order of magnitude" for the
  borated HDPE, "factor ~5" for B₄C, "factor ~50" gamma reduction from passive materials, "factor 5"
  from the COV); Geant4 10.7.3; tangent-plane source sampling; residual "strongly dominated by cosmic
  ray-induced neutrons"; ~250 d⁻¹kg⁻¹keV⁻¹ in 10–100 eV on CaWO₄ with S/B ≥ 1; LEE explicitly
  discussed and explicitly excluded from the particle-background budget.
  **Not verified:** the "tens to hundreds of millions of CPU-hours" figure supplied in the milestone
  context does not appear in the text fetched; no CPU cost is stated there. Treat that number as
  project lore until located in the paper.
- R. Campbell-Deem, S. Knapen, T. Lin, E. Villarama, "Dark matter direct detection from the single
  phonon to the nuclear recoil regime," *Phys. Rev. D* 106, 036019 (2022), arXiv:2205.02250.
  **Full text fetched (ar5iv).** Impulse criterion `q ≫ √(2m_d ω̄_d)`; Debye–Waller
  `W_d(q) = q²/(4m_d)∫dω D_d(ω)/ω`; incoherent/coherent transition at `q_BZ ≈ 2π/a ≈ 2 keV`; Ge, Si,
  diamond in Appendix D; stated accuracies (single-phonon analytic vs DFT within O(1); two-phonon
  incoherent within ~factor 5, up to an order of magnitude low with anharmonicity).
- S. Knapen, J. Kozaczuk, T. Lin, "DarkELF: A python package for dark matter scattering in dielectric
  targets," *Phys. Rev. D* 105, 015014 (2022), arXiv:2104.12786. Ge among the shipped materials;
  github.com/tongylin/DarkELF.
- X.-X. Cai, T. Kittelmann, "NCrystal: A library for thermal neutron transport," *Comput. Phys.
  Commun.* 246, 106851 (2020), arXiv:1901.08890; github.com/mctools/ncrystal. Coherent-elastic
  (Bragg) + incoherent + inelastic from unit-cell parameters; C++/C/Python; `Ge_sg227.ncmat` in the
  shipped data library.
- CONUS+ Collab., "Sub-keV energy calibration of CONUS+ via ⁷¹Ge M-shell neutron activation,"
  arXiv:2604.25748. ⁷¹Ge M/L/K X-ray lines resolved at 158.7 ± 1.4 / 1298.5 / 10368.3 eVee.
- S. Yellin, "Finding an upper limit in the presence of an unknown background," *Phys. Rev. D* 66,
  032005 (2002), arXiv:physics/0203002. Maximum-gap / optimum-interval; parameter-independent,
  conservative classical limits with no background model.
- M. Reginatto, P. Goldhagen, "MAXED, a computer code for maximum entropy deconvolution of multisphere
  neutron spectrometer data" / UMG 3.3 package (MAXED + GRAVEL), PTB / NEA Data Bank NEA-1665.
  Standard regularized few-channel and multichannel neutron unfolding.
- A. C. Carnall, "SpectRes: A fast spectral resampling tool in Python," arXiv:1705.05165.
  Integral-conserving resampling; `specutils.FluxConservingResampler` is the equivalent.
- R. Chartrand, "Numerical differentiation of noisy, nonsmooth data," *ISRN Applied Mathematics* 2011,
  164564, doi:10.5402/2011/164564. Total-variation regularized differentiation.
- Ricochet Collab., "Fast neutron background characterization of the future Ricochet experiment at the
  ILL research nuclear reactor," arXiv:2208.01760, *Eur. Phys. J. C* (2023). Peer example of the same
  problem (³He counters + Geant4; 44 ± 3 → 9 ± 2 events/day/kg NR in 50 eV–1 keV depending on muon
  veto). Useful as an independent order-of-magnitude anchor for a shielded reactor-site Ge/Zn NR rate.
- EURADOS, "Results of the international comparison exercise on neutron spectra unfolding in Bonner
  spheres spectrometry," arXiv:2201.01241. ISO convention that spectral bins are flat in fluence per
  unit lethargy.
- OpenMC documentation, "Variance Reduction" (docs.openmc.org): MAGIC and FW-CADIS weight-window
  generation. Relevant OpenMC shielding-benchmark and weight-window-mesh literature exists
  (e.g. FNS/SINBAD interpretations; weight-window mesh development in *Fusion Eng. Des.*).
- Albert–Welton kernel / removal cross-section method: standard shielding literature
  (J. K. Shultis & R. E. Faw, *Radiation Shielding*, ANS 2000; *Radiation Shielding and Radiological
  Protection*). `Σ_R ≈ (2/3)Σ_T` at 6–8 MeV; validity requires a following hydrogenous slab.

**Surfaced but NOT read — verify before quoting any number:**

- "Low-Energy Backgrounds in Solid-State Phonon and Charge Detectors," arXiv:2503.08859 (review-level
  LEE entry point).
- "Characterization of the Low Energy Excess using a NUCLEUS Al₂O₃ detector," arXiv:2603.07687
  (closest target- and site-matched LEE anchor).
- CRESST-III, "Latest observations on the low energy excess in CRESST-III," arXiv:2207.09375
  (power-law time decay of the LEE amplitude).
- "Revisiting the dark matter interpretation of excess rates in semiconductors," *Phys. Rev. D* 105,
  123002 (2022) — reported spectral index `α = 3.43` for Si and Ge excess rates. **Confirm the index
  and its applicability to a phonon-only cryogenic device before adopting it.**
- IAEA Nuclear Data Library / Thermal Scattering Law database — **must be checked directly to confirm
  that no Ge TSL evaluation exists** in ENDF/B-VIII.0 or VIII.1.

**Reused from v1.0/v1.1 (not re-researched):** Freedman/Helm CEvNS, Huber–Mueller flux, Gaisser–Guan
muon flux, Klein–Nishina Compton, Landau–Vavilov, ENDF/B-VIII.0 n-Ge elastic (Phase 7),
`R(E_rec|E_dep)` MC response chain, Gordon 2004 sea-level neutron spectrum.

---

_Methods research for: v2.0 NUCLEUS-VNS background transfer, figure digitization as forward-model
input, the 100 meV extension, and LEE parameterization_
_Researched: 2026-07-22_
