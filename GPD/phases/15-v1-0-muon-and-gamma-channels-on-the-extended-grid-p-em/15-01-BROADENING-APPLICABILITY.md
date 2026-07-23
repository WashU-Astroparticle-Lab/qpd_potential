# 15-01 — Does the Phase-11 IA broadening apply to the electron-recoil channels?

**Plan:** 15-01 · **Phase:** 15 · **Date:** 2026-07-23
**Interpreter:** `/opt/anaconda3/bin/python3` (numpy 1.26.4, scipy 1.17.1)
**Repo HEAD at execution:** `e6efbcf`

Every number below carries the command that produced it. All commands are run from
the repository root with `sys.path.insert(0, "src")`.

---

## 0. The verdicts, in one table

| Channel | Verdict | Recoiling body | Initial-state momentum distribution |
|---|---|---|---|
| **muon** | `does_not_apply` | An atomic **electron** of the Ge target, in each ionizing collision | The struck shell's momentum distribution — **already inside the model** through the Bethe cross section (`I = 350 eV`), and its collision-by-collision fluctuation **is** the Landau–Vavilov density the chain samples |
| **compton** | `does_not_apply` | A **bound atomic electron** of Ge | The **Compton profile `J(p_z)`** — a real, nonzero, physically present distribution, evaluated in §3, not dismissed |

Neither verdict is `undecidable`, so the ROADMAP Phase-15 backtracking trigger does
not fire.

Machine-readable at `src/qpd_potential/em_recoil.py::IA_APPLICABILITY`, reachable
through `em_recoil.ia_verdict(channel)`. There is no accessor returning a bare
boolean: a consumer cannot get the decision without also getting the reason and the
consequence.

```
/opt/anaconda3/bin/python3 -c "import sys;sys.path.insert(0,'src')
from qpd_potential import em_recoil as e
for c in e.ELECTRON_RECOIL_CHANNELS: print(c, e.ia_verdict(c).verdict)"
```

**Guard.** `em_recoil.assert_nuclear_kernel_use(channel, apply_nuclear_kernel)`
raises `ElectronRecoilBroadeningError` — a named, catchable exception carrying the
verdict, the recoiling body, the reason and the consequence — when a caller
contradicts the verdict, and returns the verdict when consistent. It raises; it does
not warn, clamp, or return a flag. The codebase precedent is
`fold.DoubleBroadeningError`.

---

## 1. What Phase 11 actually derived, and for what body

`11-02-SUMMARY.md` (`claim-sigma-derivation`) derives the width from the impulse
decomposition of the energy transfer, **not** from a closed form:

> `w = q²/(2 m_N) + q·p/m_N`; `⟨w⟩ = q²/(2 m_N) = E_R` exactly; `Var(w) = q² σ_p²/m_N²`;
> `σ_p² = m_N ω̄ /2` **from the zero-point oscillator**; hence `σ_E = q σ_p/m_N = √(E_R ω̄)`.

Two things follow, and they are the whole determination.

1. The **body** whose initial-state momentum enters is the **germanium nucleus**.
   `σ_p² = m_N ω̄/2` is the nuclear zero-point momentum spread; `ω̄ = 17.8597 meV` is
   the harmonic mean of the measured Ge **phonon** VDOS (`CONVENTIONS.md` §J,
   Nelin & Nilsson 1972 via NCrystal). Nothing in either Phase-15 channel gives the
   Ge nucleus that role.
2. The **form** is generic. `T = q²/(2m) + p·q/m` holds for **any** struck particle.
   That is what makes the electron-side analogue a real question rather than a
   rhetorical one, and it is why §3 exists.

`fold.run_neutron_fold_extended`'s APPLICABILITY paragraph states verbatim that the
neutron channel's applicability follows from its *nuclear-recoil character* and that
"Phase 15's ELECTRON-recoil channels are a separate question and are not settled by
this." This document discharges that handoff.

**No algebraic identity is cited as evidence anywhere below.** `CONVENTIONS.md` §J
records `σ_E/E_R = 1/√(2W)` and `2W = E_R/ω̄` as identities true by construction for
*any* `ω̄`; treating either as corroboration is `fp-identity-as-corroboration`, and
Phase 11's own `test-identity-flag` demonstrated the point by verifying the relation
at three physically absurd `ω̄` values. The arguments here are about *which particle
recoils* and *what its momentum distribution is*.

---

## 2. Muon channel — the recoiling body, and the double-counting question

**Which particle recoils.** In muon ionization the momentum transfer is absorbed by
an **atomic electron**. The germanium nucleus participates only as the static
binding potential fixing the oscillator strengths that enter the mean excitation
energy `I`. The nuclear zero-point momentum distribution is not an input to the
deposit at any point in `muon_deposit.sample_deposit`.

**What the muon-channel counterpart of the IA smearing actually is.** The plan
required this to be decided and recorded rather than left implicit: *would an
additional IA convolution double-count a fluctuation the chain already carries?*

**It would.** The Landau–Vavilov straggling density **is** the fluctuation of this
deposit. `sample_deposit` draws `Δ = Δ_p + ξ(λ − λ_mode)` with `λ` a standard Landau
variate — i.e. the chain already samples the full collision-by-collision
distribution of the energy loss, including the contribution of the bound-electron
momentum distribution, which enters the underlying Bethe cross section through
`I = 350 eV` and the Sternheimer density-effect coefficients. Convolving a further
Gaussian on top would broaden a distribution whose spread the model has already
computed.

The scale comparison makes the point quantitative rather than rhetorical. At the
vertical chord the straggling width is

```
ξ(0.20 cm) = 0.072069 MeV = 7.2069e4 eV
```

(reproduced from the committed path in
`tests/test_em_recoil.py::test_reference_point_reproduces_the_09_01_scalars`),
against a candidate nuclear IA width of `√(E_R ω̄) = 0.0422 eV` at 100 meV. The
Landau width exceeds any candidate IA width by six orders of magnitude at the
chord that dominates the channel.

**Verdict: `does_not_apply`.** Two independent objections, either sufficient: the
scale is wrong (§3 shows the electron-side scale is ≥ 35.5× the nuclear one), and
the fluctuation is already carried.

**Consequence for the spectra (Plan 15-03 may act on this directly).** The muon
deposit table is emitted **unbroadened** with `broadened_provenance = false`; the
fold is called with `broaden=False`; **no leakage budget arises**, so
`residual_retained_plus_leaked` and `residual_retained_only` **coincide** and must be
reported as one statement rather than as two independent confirmations. The 100 meV
kernel-leakage caveats of `CONVENTIONS.md` §J (48.98 % below the floor, 0.87 % to
`T < 0`) do **not** apply to this channel.

**Falsifier.** A measured or first-principles sub-keV muon energy-loss distribution
in Ge whose width exceeds the Landau–Vavilov prediction by a residual scaling as
`√E_dep` with coefficient `√ω̄ = 0.1336 eV^½` — i.e. an unexplained extra 42.3 % at
100 meV and 4.20 % at 10.14 eV. Equivalently, a demonstration that the Ge nucleus
takes up a resolvable share of the momentum transfer in muon ionization.

---

## 3. Compton channel — the electron-side analogue, EVALUATED

This is the section `test-electron-analogue-evaluated` requires and `fp-unexamined-no`
exists to force. The correct-sounding answer — "electron recoils, so the nuclear
kernel does not apply, therefore nothing" — is **not** accepted here without testing
the mechanism that could make it wrong.

### 3.1 The analogue exists and has the identical form

Energy–momentum conservation for a struck particle of mass `m` with initial momentum
`p` receiving transfer `q` (non-relativistic, binding suppressed for the moment):

```
T = (|p + q|² − p²)/(2m) = q²/(2m) + p·q/m
```

— the same decomposition Phase 11 applied to the nucleus. Mean `= q²/(2m)`, the free
recoil; variance `= q² σ_pz²/m²`. Hence

```
σ_T = q σ_pz / m = √(2 m T) σ_pz / m = √(T · ω̄_X),      ω̄_X ≡ 2 σ_pz² / m
```

For the **nucleus**, `σ_p² = m_N ω̄/2` returns `ω̄_X = ω̄` — Phase 11's result, recovered.
For the **electron**, `σ_pz` is the width of the **Compton profile `J(p_z)`** and
`ω̄_e ≡ 2 σ_pz²/m_e` (`omega_bar_e` in the code) is an **electronic** energy. *Same form, different body,
different scale.* This is derived, not asserted, and it is not an identity
restatement of anything in `CONVENTIONS.md` §J.

### 3.2 How big is `ω̄_e`? — three estimators, bracketing

```
/opt/anaconda3/bin/python3 -c "import sys;sys.path.insert(0,'src')
from qpd_potential import em_recoil as e; print(e.electron_ia_scale_eV())"
```

| Estimator | `σ_pz` [a.u.] | `ω̄_e` [eV] | Status |
|---|---|---|---|
| **Lower bound** — uncertainty principle over the Ge covalent bond, `a√3/4 = 2.449986 Å` (from the committed lattice constant `a = 5.658 Å`) | ≥ **0.107996** | ≥ **0.634740** | **Rigorous.** No bound Ge electron is more delocalized than its bond. Requires no external number. |
| **Valence virial** — `⟨p²⟩ = 2m|E_B|`, `σ_pz² = ⟨p²⟩/3`, so `ω̄_e = 4|E_B|/3` at the Ge valence-band width `|E_B| = 12.6 eV` | 0.5556 | **16.80** | [UNVERIFIED — training data] |
| **Whole-atom envelope** — the same virial over all 32 electrons at the non-relativistic HF total energy 2075.36 hartree | 6.576 | **2353.06** | An **envelope**, not an estimate: it is dominated by 1s electrons inaccessible below ~11 keV of transfer. [UNVERIFIED — training data] |

**Against the nuclear scale `ω̄ = 17.8597 meV`:**

```
ω̄_e(lower bound) / ω̄ = 35.540
width ratio σ_T(electron)/σ_E(nuclear) = √(ω̄_e/ω̄) = 5.9616×  (up to 362.98×)
```

The width ratio is **energy-independent** — both widths go as `√T` — so this is a
single number, not a curve. **Transplanting the nuclear kernel onto the Compton
channel would understate the electron-side width by at least a factor 6 and by up
to a factor 363.** The transplant is not merely the wrong justification for
approximately the right number; it is the wrong number by 0.8–2.6 decades.

**The verdict does not depend on the two `[UNVERIFIED]` estimators.** The rigorous
lower bound alone — derived from nothing but the committed lattice constant and the
uncertainty principle — already puts `ω̄_e` a factor 35.5 above `ω̄`.

### 3.3 Is the analogue width negligible against the response chain? — **No.**

```
/opt/anaconda3/bin/python3 -c "import sys;sys.path.insert(0,'src')
from qpd_potential import em_recoil as e
print(e.electron_side_summary(e.EXT_FLOOR_eV)); print(e.electron_side_summary(e.V1_FLOOR_eV))"
```

One extended-grid bin is **2.920471 %**.

| `T` [eV] | `σ_T/T` (lower bd) | in bins | `σ_T/T` (valence) | `σ_T/T` (atom env.) | nuclear transplant `σ_E/E` |
|---|---|---|---|---|---|
| 0.0999350 (ext floor) | **252.02 %** | **86.3** | 1297 % | 1.53e4 % | 42.27 % |
| 10.144973 (v1.0 floor) | 25.01 % | 8.6 | 128.7 % | 1523 % | 4.196 % |
| 100 | 7.967 % | 2.7 | 40.99 % | 485.1 % | 1.336 % |

**Stated plainly, because it cuts against the comfortable answer:** one of this
plan's declared disconfirming observations has **fired**. The electron-side
Compton-profile analogue produces a width that is *emphatically not* unresolvable
against the response chain — 86 extended-grid bins at the extended floor under the
most favourable bound. "No broadening because it would be too small to see" would
have been a **false** argument. It is not the argument made here.

### 3.4 Why the analogue is nevertheless not applied

The electron-side IA is **outside its own validity domain** exactly where it would
matter. Phase 11 used the Campbell–Deem criterion `2W ≫ 1` (equivalently
`E_R ≫ ω̄`) and applied it quantitatively: `2W = 5.60` at the 100 meV floor, so the
nuclear IA is satisfied there by a factor 5.6. The electron analogue of that same
criterion is `2W_e = T/ω̄_e`:

| `T` [eV] | `2W_e` (lower bd) | `2W_e` (valence) | `2W_e` (atom env.) |
|---|---|---|---|
| 0.0999350 | **0.1574** | 0.005949 | 4.247e-05 |
| 0.73955 (adopted physical floor) | 1.165 | 0.04402 | 3.14e-04 |
| 10.144973 | 15.98 | 0.6039 | 0.004311 |

**Under every estimator, `2W_e < 1` at the extended grid floor.** Below its own
validity threshold the transfer cannot be described as a free recoil at all: it goes
into discrete atomic/band excitations, and there is no recoil continuum to broaden.
That is the same physics that drives `S(x, Z) → 0` in the forward direction, and it
is why §4's two independent Compton criteria land in the same eV-scale region.

**Conclusion of the analogue evaluation.** The electron-side IA broadening
(i) **exists**, (ii) has width `σ_T = √(T ω̄_e)` with `ω̄_e ∈ [0.635, 2353] eV`,
(iii) is **not negligible** — ≥ 252 % of the deposit at 100 meV — and (iv) is
**not applicable** in the sub-eV region because `2W_e < 1` there. The v1.0 chain
neglects it: `compton_deposit.sample_electron_recoil` samples `T_e` from **free**
kinematics at the sampled angle and uses `S(x, Z)` only as a cross-section
normalization. Modelling it would be a **new mechanism**, which ROADMAP SC1
excludes. It is therefore carried forward as a **NAMED GAP for Phase 16**, and it
*reinforces* the Compton physical floor of §4 rather than competing with it.

**Verdict: `does_not_apply`** — for the *nuclear* kernel, on the grounds of the
recoiling body and the scale, with the electron-side analogue evaluated and
separately excluded on its own validity criterion.

**Consequence for the spectra.** Identical to the muon channel: unbroadened table,
`broadened_provenance = false`, `broaden=False` at the fold, the two counts
residuals coincide.

**Falsifier.** A germanium Compton-profile measurement or calculation giving
`σ_pz ≤ 0.0181 a.u.` — an electron delocalized over more than 27.6 Å, five Ge lattice
constants — which would bring `ω̄_e` down to the nuclear `ω̄`. Or a demonstration that
the Ge nucleus recoils coherently with the struck electron in the *incoherent*
channel, which would reinstate `m_N`.

---

## 4. The Compton channel's low-energy floors

### 4.1 The S(x, Z=32) table domain **does** cover the extended floor

```
/opt/anaconda3/bin/python3 -c "import sys;sys.path.insert(0,'src')
from qpd_potential import em_recoil as e
print(e.compton_S_suppression(e.EXT_FLOOR_eV)); print(e.compton_S_suppression(e.V1_FLOOR_eV))"
```

| `T_e` [eV] | `x` [Å⁻¹] | `S(x, 32)` | `S/Z` | suppression vs free KN |
|---|---|---|---|---|
| 0.0999350 (ext floor) | 1.288806e-02 | 0.0699475 | **2.185858e-03** | **457.49×** |
| 10.144973 (v1.0 floor) | 1.298536e-01 | 3.953804 | **0.1235564** | **8.093×** |

The committed table spans `x ∈ [1.0e-3, 4.2646e4] Å⁻¹`. `x` at the extended floor is
**inside** it with a margin of **12.888× above the table floor**, so **no
interpolator raises on the extended axis** — this is not a blocking finding for Plan
15-02. Verified over all 744 extended-grid centres in
`tests/test_em_recoil.py::test_S_domain_covers_floor`.

Two structural checks that make the mapping trustworthy rather than merely computed:

* `x` is **independent of the line energy** at small transfer, as a momentum
  transfer must be. All sixteen `data/gamma_lines.csv` lines give
  `x = 1.288806e-02 Å⁻¹` at `T_e = 0.0999350 eV` to seven digits.
* `x` **is** the momentum transfer: `4π x a₀ = √(2 m_e T)` in atomic units, agreeing
  to 1.3e-8 at every energy tested (`test_momentum_transfer_variable_is_the_momentum_transfer`).

### 4.2 The physical floor, which is a different object from the suppression

`S(x, Z)` is an interpolated **cross-section modifier**. It is not a validity
statement, and a table that returns a number outside the regime its physics
describes returns a number, not a rate (`fp-suppressed-means-valid`).

**Adopted physical floor:** the germanium **indirect band gap in the `T → 0` limit**,
`E_g = 0.7437 eV`, less the free-exciton binding `4.15 meV`, giving

```
adopted pair-creation floor = 0.73955 eV
```

**The choice is named, not assumed.** The detector sits at the `T → 0` evaluation
point of `CONVENTIONS.md` §J (10 mK), so the low-temperature gap is the operative
one; the 300 K gap `0.661 eV` is the named alternative, and the exciton correction is
applied because a bound electron–hole *pair* can be created marginally below the gap.
The conclusion does not turn on the choice: the two candidates differ by a factor
1.13 and both sit **7.4× and 6.6× above the extended grid floor** respectively.
Provenance: **[UNVERIFIED — training data]**; no repository artifact carries a
germanium band gap, and this is recorded as one of the plan's weakest anchors.

**The distinction, written out rather than left to the reader.** At
`T_e = 0.0999350 eV`:

* the S table **returns** `S/Z = 2.186e-03` — a finite, small, positive number, and
  the machinery will happily produce a rate from it;
* the deposit is **7.40× below** the energy at which germanium can create an
  electron–hole pair at all, so **no electron recoil of that energy is a physical
  outcome of incoherent scattering**;
* independently, the electron-side IA validity parameter `2W_e = 0.157 < 1` there
  (§3.4), so the impulse approximation that `S(x, Z)` itself encodes has already
  broken down.

Two criteria of different origin — a thermodynamic pair-creation threshold and a
kinematic IA validity condition — land within a factor ~1.2 of each other
(`0.73955 eV` vs `ω̄_e(lower bound) = 0.6347 eV`). That agreement is not a
construction: nothing forced them to coincide. **A number the S table returns
here is not the same object as a rate the physics supports: a suppressed rate
is not a rate.** `70` of the 744 extended bins lie below the adopted physical floor.

---

## 5. The muon channel's Landau–Vavilov validity floor — the disconfirming check

### 5.1 The criterion

The committed chain guards the **thin** end: `κ = ξ/T_max = 6.727e-05`, deep Landau.
It does **not** guard the other end. A *continuous* energy-loss density presupposes
many collisions, i.e. `ξ` comfortably above the mean excitation energy `I`. The
Landau–Vavilov straggling function ceases to be the correct distribution when `ξ`
falls to the scale of `I`, where the loss is dominated by a small number of discrete
single collisions (PDG, *Passage of Particles Through Matter*, energy loss in thin
absorbers; Bichsel, Rev. Mod. Phys. **60**, 663 (1988)).

**Criterion adopted: `ξ ≤ I`.** This is a published boundary applied to computed
numbers, not a chosen threshold.

**`I` provenance.** `src/qpd_potential/muon_deposit.py::I_GE = 350.0e-6 MeV` — the Ge
mean excitation energy **already in use by the committed chain**, i.e. the same `I`
that produced every `Δ_p` the v1.0 manuscript published (PDG *Atomic and Nuclear
Properties of Materials*, Ge, `I = 350.0 eV`). Read from the code, never re-typed.
The external PDG value is **[UNVERIFIED — not re-fetched in this phase]**; what *is*
verified is that it is the value the v1.0 results were built on.

**Reference point.** `E_μ = 4.0 GeV` (`βγ = 37.844651`) — the point at which Plan
09-01 §2.3 quoted the verified vertical-chord scalars. Computing the floor there
rather than at an invented reference is what makes it comparable to those scalars.
The committed path reproduces them: `ξ(0.20 cm) = 0.072069 MeV`,
`Δ_p = 1.230614 MeV`, `κ = 6.7267e-05`, `Δ_p < ⟨Δ⟩ = 1.458502 MeV`.

### 5.2 The floor

```
/opt/anaconda3/bin/python3 -c "import sys;sys.path.insert(0,'src')
from qpd_potential import em_recoil as e
lv=e.landau_validity_floor(); print(lv); print(e.indicted_v1_bins(lv['floor_eV']))"
```

```
ξ/ℓ           = 0.36034504 MeV/cm            (committed muon_deposit.xi_width)
ξ = I = 350 eV at ℓ* = 9.712913e-04 cm = 9.712913 µm
FLOOR  Δ_p(ℓ*) = 4111.8165 eV = 4.1118 keV   (committed muon_deposit.mpv_deposit)
```

### 5.3 **The floor lies above the v1.0 grid floor and indicts 209 published bins**

```
floor / v1.0 grid floor      = 405.31×
v1.0 bins with centre below the floor:  209 of 584   (35.79 %)
   highest indicted v1.0 centre =  4042.199 eV
   lowest surviving v1.0 centre =  4160.251 eV
extended-axis bins below the floor:     369 of 744   (49.60 %)
```

**Stated plainly, as the plan requires and without softening.** The criterion indicts
**209 of the 584 bins the v1.0 manuscript already published** — more than a third of
the v1.0 muon deposit spectrum. This is not restricted to the 160 new sub-eV bins;
it reaches up to 4.04 keV.

**Nothing was tuned to move it.** `fp-floor-softened` forbids choosing `I`, the
criterion, or the threshold to make the count zero. The sensitivity, with `I` varied
**consistently** in both the criterion and the `Δ_p` bracket
(`em_recoil.landau_floor_sensitivity_to_I`, verified against the committed path at
`I = I_GE` to `rel diff = 0.0`):

| `I` [eV] | `ℓ*` [µm] | floor [eV] | v1.0 bins indicted |
|---|---|---|---|
| 300 | 8.3254 | 3570.66 | 204 |
| 322 | 8.9359 | 3809.72 | 206 |
| **350 (committed)** | **9.7129** | **4111.82** | **209** |
| 400 | 11.1005 | 4645.81 | 213 |

Over a ±14 % swing in `I` the count runs 204–213. **No plausible `I` makes it zero.**
A stricter reading of the criterion (`ξ/I ≥ 10`, the "comfortably above" reading)
would put the floor at 49.18 keV and indict far more; the count above is the
**loosest** defensible one.

**What this does and does not say.** It does not say the v1.0 muon spectrum is wrong
below 4.11 keV. It says that below 4.11 keV the *distribution* used to generate it —
a continuous straggling density — is outside the regime the Landau–Vavilov theory
describes, so the content of those bins is an extrapolation of the model rather than
a prediction of it. The channel's integral rate (`1.3659 Hz`) and its bulk
(4 keV → 200 MeV, where the pile-up and the physics live) are untouched: the
sub-4 keV deposited tail carries only ~1e-4 of the flux, per the `04-01` refinement
note quoted in `scripts/make_muon_spectrum.py`.

**Handed to Phase 16 as a named gap**, and to the paper as a standing finding about
the v1.0 record.

### 5.4 Chord map, and what the extended floor physically means

```
/opt/anaconda3/bin/python3 -c "import sys;sys.path.insert(0,'src')
from qpd_potential import em_recoil as e
for t in (e.V1_FLOOR_eV, e.EXT_FLOOR_eV):
    l=e.chord_cm_of_deposit_eV(t); print(t, l, e.chord_in_lattice_constants(l))"
```

| Target `Δ_p` | chord `ℓ` | in Ge lattice constants (`a = 5.658 Å`) | `ξ` there | `ξ/I` |
|---|---|---|---|---|
| 10.144973 eV (v1.0 floor) | 4.428417e-06 cm = **44.28 nm** | **78.27** | 1.5958 eV | 4.56e-03 |
| 0.0999350 eV (ext floor) | 1.057434e-07 cm = **1.0574 nm** | **1.869** | 0.03810 eV | 1.09e-04 |

**In words, because that is the physical content of the number.** A muon depositing
the extended-grid floor energy of 100 meV as its *most probable* loss would have to
traverse **1.06 nanometres of germanium — under two lattice constants, a path of
roughly two atomic layers**. There is no such chord through a 2 mm wafer except by
corner-clipping at grazing incidence, and at that path length the notion of a
continuous energy-loss density over many collisions has no content: `ξ` there is
0.038 eV, four orders of magnitude below `I`.

### 5.5 The two competing explanations for the lowest v1.0 muon bins

The plan required these to be distinguished rather than picked between:

* **(A) genuine short-chord corner-clipping geometry**, with the Landau density a
  fair description of it;
* **(B) an artefact of the tabulated Landau inverse-CDF's left tail combined with the
  clip at zero deposit** in `sample_deposit` (`dep = np.clip(dep, 0.0, e_kin)`).

**What the numbers support.** Both mechanisms are present, and the floor locates the
crossover — but they do not contribute equally, and the tail mechanism dominates at
the bottom of the axis:

* For **(A)** to produce a 100 meV *most probable* deposit requires a 1.06 nm chord
  (§5.4). The ray-box sampler can produce arbitrarily short corner chords, so the
  geometry is not forbidden — but the solid angle for a chord under two lattice
  constants through a 10.16 × 10.16 × 0.20 cm box is vanishing.
* For **(B)**, the far more accessible route to a sub-eV entry is a *typical* chord
  with a strongly negative Landau variate: `dep = Δ_p + ξ(λ − λ_mode)`, and for a
  0.20 cm chord `ξ = 7.2e4 eV`, so a sub-eV deposit needs
  `λ − λ_mode ≈ −Δ_p/ξ = −17.1`. The tabulated standard Landau density is built on
  `λ ∈ [−4, 300]` (`muon_deposit._build_landau_table`), so `np.interp` **clamps** at
  `λ = −4`, giving a hard minimum `dep = Δ_p − 3.777 ξ`, which for the vertical chord
  is `+0.958 MeV` — positive, so the clamp does not manufacture sub-eV entries at
  full chord length. Sub-eV entries therefore require *both* a short chord and a
  left-tail draw.

**Conclusion the numbers support:** the sub-eV content is the **joint tail** of a
short-chord geometry and a left-tail Landau draw, and in *both* limbs the deposit
sits far below `ξ ≈ I` — i.e. **outside the model's domain either way**. The
validity floor is what makes that visible; neither explanation licenses reporting a
sub-eV muon rate as a physical prediction. Plan 15-02's per-bin statistical adequacy
label and this floor together are what a consumer must read before quoting one.

---

## 6. Frozen table and what Plans 15-02 / 15-03 must do with it

`artifacts/v2.0/em_validity_floors.csv` — 6 rows, unit-bearing headers, disposition
row `not_a_spectrum` added to `artifacts/v2.0/legacy_grid_disposition.csv`
(53 register rows, closure guard green).

| channel | criterion | floor [eV] | v1.0 bins below | ext bins below |
|---|---|---|---|---|
| muon | `landau_vavilov_xi_le_I` | **4111.8165** | **209** | **369** |
| muon | `chord_map_v1_grid_floor` | 10.144973 | — | — |
| muon | `chord_map_ext_grid_floor` | 0.0999350 | — | — |
| compton | `ge_pair_creation_threshold` | **0.73955** | 0 | **70** |
| compton | `S_suppression_at_ext_grid_floor` | 0.0999350 | — | — |
| compton | `S_suppression_at_v1_grid_floor` | 10.144973 | — | — |

**Instructions carried forward, so nothing is re-derived downstream:**

1. **Plan 15-02** flags every emitted bin against the per-channel floor
   (`below_validity_floor`). The flag is **emitted, not used to delete the row** —
   deleting would hide the model's reach; flagging shows it. Both tables declare
   `broadened_provenance = false`.
2. **Plan 15-03** calls the fold with `broaden=False` for both channels, reading the
   verdict from `em_recoil` at fold time rather than hard-coding it, and states that
   the two counts residuals coincide because no broadening was applied.
3. **Phase 16** inherits two named gaps: (a) the neglected Compton-profile Doppler
   broadening, real and ≥ 252 % of the deposit at 100 meV but outside its own IA
   validity domain there; (b) the 209 indicted v1.0 muon bins.

---

## 7. What would falsify this determination

Per channel, in §2 and §3.4. Collected:

1. **Muon.** An unexplained residual broadening of the Ge muon energy-loss
   distribution scaling as `√E_dep` with coefficient `√ω̄ = 0.1336 eV^½`; or a
   demonstration that the Ge nucleus takes up a resolvable share of the momentum
   transfer in ionization.
2. **Compton.** A Ge Compton profile with `σ_pz ≤ 0.0181 a.u.`; or coherent nuclear
   recoil in the incoherent channel.
3. **Both.** A derivation showing that the phonon bath — not the nucleus in
   isolation — sets an initial-state momentum distribution for the *struck electron*
   with a spread near `√(m_e ω̄/2)`. This is the one route by which `ω̄` could enter
   an electron-recoil channel legitimately, and it is **not** what Phase 11 derived;
   it would be new physics, and it is recorded here as the residual uncertainty in
   the verdict rather than dismissed.
4. **The muon floor.** A published criterion for Landau–Vavilov validity materially
   looser than `ξ ≳ I` — but note that a *looser* criterion is what has already been
   adopted (`ξ/I = 1` rather than `ξ/I ≫ 1`), so the 209-bin count is a lower bound
   on the indictment, not an upper one.

---

## 8. Uncertainty markers

**Weakest anchors.**
* `I = 350 eV` is not a named constant in `params.py` and the floor scales with it;
  its provenance is the committed `muon_deposit.I_GE` and the external PDG value was
  not re-fetched. Sensitivity reported in §5.3: the finding survives ±14 %.
* No measurement of a sub-eV energy-loss distribution exists for either channel in
  this repository or its anchor registry. The determination is published physics
  applied to committed numbers, not a fit.
* The Ge band gap as the Compton physical floor is the more restrictive reading; the
  exciton correction is applied and named, and a band-structure threshold would be a
  different choice. `[UNVERIFIED — training data]`.
* `ω̄_e`'s valence and whole-atom estimators are `[UNVERIFIED — training data]`. The
  verdict rests on the rigorous lower bound alone.

**Unvalidated assumptions.**
* That the two channels can share a verdict. They were determined **separately**, on
  different grounds — the muon on double-counting plus scale, the Compton on scale
  plus its own IA validity — and they happen to agree.
* Not assumed and explicitly **refuted**: that a small electron-side IA width would be
  unresolvable against the response chain. It is 86 extended-grid bins wide at the
  extended floor (§3.3).

**Disconfirming observations, and which fired.**
* ✅ **FIRED** — the Landau–Vavilov floor lands **above** 10.14 eV and indicts 209
  published v1.0 bins.
* ✅ **FIRED** — the electron-side Compton-profile analogue produces a width that is
  **not** negligible against the response chain.
* ❌ did not fire — `x` at the extended floor is **inside** the committed `S(x, Z)`
  domain (margin 12.888×), so Plan 15-02 is not blocked.

---

## 9. Verification ledger

| Acceptance test | Outcome | Evidence |
|---|---|---|
| `test-verdict-declared` | **PASS** | `test_verdict_declared`, `test_verdict_vocabulary_is_closed` |
| `test-verdict-argued` | **PASS** | §1–§3; `test_report_names_the_recoiling_body_and_a_falsifier` |
| `test-electron-analogue-evaluated` | **PASS** | §3 with numbers and a rigorous bound; `test_electron_analogue_is_evaluated_with_numbers` |
| `test-guard-raises` | **PASS** | `test_guard_raises`, `test_guard_is_not_a_warning_or_a_flag` |
| `test-muon-floor-computed` | **PASS** | §5.2; `test_muon_floor_computed`, `test_mpv_with_I_reproduces_committed_path` |
| `test-chord-map-lattice` | **PASS** | §5.4; `test_chord_map_lattice` |
| `test-floor-reported-against-v1-bins` | **PASS (finding: 209 bins indicted)** | §5.3; `test_floor_reported_against_v1_bins`, `test_floor_sensitivity_to_I_never_reaches_zero` |
| `test-S-domain-covers-floor` | **PASS** | §4.1; `test_S_domain_covers_floor` |
| `test-S-suppression-computed` | **PASS** | §4.1; `test_S_suppression_computed` |
| `test-compton-physical-floor-stated` | **PASS** | §4.2; `test_compton_physical_floor_is_named_not_assumed` |
| `test-dimensions` | **PASS** | `test_dimensions` |

**Forbidden proxies.** `fp-transplant-nuclear-width` rejected (the kernel is not
applied and the guard raises). `fp-unexamined-no` rejected (§3 evaluates the analogue
with a bound and a number, and reports that it is *not* negligible). `fp-identity-as-corroboration`
rejected (no §J identity is cited as evidence; asserted by `test_no_section_J_identity_is_cited_as_evidence`).
`fp-floor-softened` rejected (§5.3 sensitivity table; nothing tuned).
`fp-suppressed-means-valid` rejected (§4.2 separates the number from the rate).
`fp-shielded-quantity-leak` rejected (`test_no_relocation_quantity_in_this_plans_code_or_report`).
