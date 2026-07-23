# 16-02 — The `S/B_particle` Assembly (CALC-22)

**Plan:** 16-02 · **Phase:** 16 (terminal, milestone v2.0) · **Axis:** RECONSTRUCTED throughout
**Configuration:** NUCLEUS's-shielding-absent · **Veto credit:** exactly **1.0 BY CONSTRUCTION**
**Artifacts:** `artifacts/v2.0/channel_inventory.csv`, `channel_omissions.csv`, `sb_particle.csv`, `sb_leave_one_out.csv`
**Module:** `src/qpd_potential/sb_assembly.py` · **Tests:** `tests/test_sb_assembly.py`

---

## 1. The headline

`S/B_particle`, trigger applied, veto credit exactly 1.0 by construction, at the
paper's 3 GW_th / 25 m surface scenario:

| design | band | estimates only | estimates + bounds (a **LOWER bound**) |
|---|---|---|---|
| **Ta→Al** | RoI 10–100 eV | **1.33 × 10⁻²** | **7.29 × 10⁻³** |
| **Al→Hf** | RoI 10–100 eV | **1.32 × 10⁻²** | **7.27 × 10⁻³** |
| Ta→Al | sub-eV (E_rec ≤ 1 eV) | 1.05 × 10⁻³ | 4.11 × 10⁻⁴ |
| Al→Hf | sub-eV (E_rec ≤ 1 eV) | 1.05 × 10⁻³ | 4.12 × 10⁻⁴ |

**The assembled accuracy label is `order_of_magnitude`**, inherited from the neutron
and capture channels, which together are 98 % of the RoI denominator. The propagation
rule is written into the artifact header so it can be challenged:

> `assembled_label` = the **loosest** label among the channels actually summed;
> `order_of_magnitude` renders as the multiplicative band **[10^−0.5, 10^+0.5]**, one
> full decade of total span. A percent-level band is forbidden regardless of how the
> arithmetic comes out.

So the reportable statement is: **`S/B_particle` in the 10–100 eV RoI is of order
10⁻², with a band spanning roughly 4 × 10⁻³ to 4 × 10⁻² (estimates only) — and it is
essentially design-independent.** The many digits in the artifacts are reproducibility
figures for the quadrature, not precision claims.

This is a poor ratio. It is reported as computed. **No target value is carried, the
pre-re-scope expectation is WITHDRAWN, and nothing here has been adjusted to improve
the number.** For an unshielded surface wafer with no veto and no overburden, a ratio
of order 10⁻² is the expected physics, not a defect to repair.

---

## 2. The integrator was validated before it was used

On the Phase-14 precedent, every channel's **own published headline** is reproduced by
this plan's band integrator **before** that channel is allowed into the sum. A channel
that does not reproduce is **BLOCKED**, not admitted with a note.

| channel | band | reproduced | published | residual (rel) |
|---|---|---|---|---|
| CEvNS | whole axis TOTAL | 118.728595 / 118.729156 | 118.73 | 1.18e-05 / 7.11e-06 |
| CEvNS | RoI 10–100 eV | 72.921435 / 73.144065 | 72.9214 / 73.1441 | 4.7e-07 / 4.8e-07 |
| neutron elastic | RoI 10–100 eV | 5430.286621 / 5485.151456 | 5430.287 / 5485.152 | 7.0e-08 / 9.9e-08 |
| Compton | RoI 10–100 eV | 34.248436 / 35.861630 | 34.2484 / 35.8616 | 1.1e-06 / 8.3e-07 |
| muon | RoI 10–100 eV | 7.465639 / 7.723080 | 7.4656 / 7.7231 | 5.3e-06 / 2.5e-06 |

Tolerance 1e-4 relative, declared as a module constant before use. **Blocked channels:
none.**

---

## 3. The bands, defined once here

The inputs disagree about the sub-eV band. Phase 13 reports the neutron channel at
`E_rec < 1 eV`; Phase 15 reports muon, Compton and CEvNS on a wider sub-10 eV band.
**Mixing them would integrate the numerator and the denominator over different regions
of the axis.** Every channel is therefore **re-integrated here**, from its own
committed artifact, on bands declared once as module constants above every function
that uses them:

- **RoI** = `E_rec` ∈ [10, 100] eV
- **sub-eV** = `E_rec` ∈ [0, 1] eV

The re-integration was not a formality: **this plan's neutron sub-eV integral is
2851.998 counts kg⁻¹ day⁻¹ against Phase 13's own 2852.040 for its `E_rec < 1 eV`
figure**, a 1.5e-05 difference arising purely at the band-edge bin. Small here, but the
same operation on the differently-defined Phase-15 band would not have been.

**A caveat on the sub-eV band, recorded rather than hidden.** The band top is a literal
`E_rec` = 1 eV, chosen so both designs are integrated over the *same* region. It
therefore **spans** the `E_rec` image of the 1 eV **deposit** regime boundary
(0.497240 / 0.495855 eV), and `CONVENTIONS.md` §I says that below that boundary the
reported observable is a **trigger probability, not dR/dE_rec**. The sub-eV rows are a
ratio of band-integrated trigger-weighted rates across a boundary where the observable
changes character. That is why the RoI rows, not the sub-eV rows, are the headline.

---

## 4. The channel inventory, and the two double-count resolutions

Seven channels. Six enter the denominator in one layer or the other; one is excluded
with a measured reason.

| channel | class | RoI (Ta→Al) | RoI (Al→Hf) | sub-eV (Ta→Al) | label | in sum |
|---|---|---|---|---|---|:-:|
| **CEvNS signal** | ESTIMATE | **72.9214** | **73.1441** | 2.9812 | factor_two | numerator |
| neutron elastic | ESTIMATE | 5430.2865 | 5485.1513 | 2851.998 | **order_of_magnitude** | yes |
| prompt (n,γ) capture | **BOUND** | ≤ 4399.777 | ≤ 4399.777 | ≤ 4399.777 | **order_of_magnitude** | yes |
| ⁷¹Ge EC M line | **BOUND** | ≤ 130.8197 | ≤ 130.8196 | 0.0000 | order_of_magnitude | yes |
| Compton γ | ESTIMATE | 34.2484 | 35.8616 | 0.0120 | factor_two | yes |
| muon ionization | ESTIMATE | 7.4656 | 7.7231 | 0.0169 | factor_two | yes |
| Ge discrete inelastic | BOUND | ≤ 2666.833 | ≤ 2666.833 | ≤ 2666.833 | order_of_magnitude | **EXCLUDED** |

**The CEvNS numerator is COMPUTED, not substituted.** 118.73 is the whole-axis
**TOTAL**; the in-RoI signal is 72.9214 / 73.1441, a factor 1.63 smaller. In the
emitted artifacts 118.73 appears only in fields explicitly labelled TOTAL, and a test
asserts that.

**The capture channel enters as the FULL BAND.** 4399.777 = thermal 3365.536 +
non-thermal 1034.241. The non-thermal part is **23.51 %** of the channel and is itself
**~8.7× the entire CEvNS total**. Reading Phase 14's title literally and folding the
thermal component alone would understate this channel by **1.31×**.

**The ⁷¹Ge M line sits at its RECONSTRUCTED image, not at its deposit energy.** 158.7 eV
is a **deposited** energy; the reconstructed image is at **65.0 / 63.0 eV** (mapping
slope 0.4099 / 0.3967). It is **100 % in-RoI and exactly 0 % sub-eV**, which the
leave-one-out sweep independently confirms. It is a **bound with a scenario** and both
scenarios travel together: **130.8197 at saturation** against **7.697512 at t = 1 d**, a
**17.0× spread** that a bare number would hide. Saturation is used in the headline layer
because it is the larger, non-flattering choice; the exposure history is not a physics
input this project owns.

### 4.1 Double-count candidate 1 — neutron elastic vs prompt (n,γ) capture

**Verdict: NOT A DOUBLE COUNT.**

- **By reaction channel.** These are *different reactions* on a shared incident flux.
  Elastic scattering is ENDF **MT=2**; radiative capture is **MT=102**. They are
  separate partial cross sections of the same total, evaluated from the same ACE files.
  Sharing an incident flux is not sharing a deposit.
- **By event time.** Simultaneous but **mutually exclusive per interaction**. Both
  deposits are prompt on the nuclear-reaction timescale, but they are alternative
  outcomes of one collision: the neutron either scatters and survives, or is absorbed
  and does not. No single event contributes to both rates.

### 4.2 Double-count candidate 2 — prompt (n,γ) recoil vs the ⁷¹Ge EC line

**Verdict: NOT A DOUBLE COUNT.**

- **By reaction channel.** The prompt bound counts the **nuclear recoil** accompanying
  the (n,γ) cascade (MT=102). The M line is the **atomic de-excitation** deposit
  following the *electron-capture decay* of the ⁷¹Ge nucleus that capture created. One
  is a nuclear recoil at the instant of capture; the other is a 158.7 eV atomic deposit
  in a later, separate decay.
- **By event time.** Separated by the **11.43 d** half-life. Same parent nucleus, two
  distinct events at two distinct times, each depositing its own energy. Counting both
  counts two deposits, not one deposit twice.

A structural check backs both arguments: no two inventory rows share **both** a source
artifact path **and** a deposit mechanism.

---

## 5. What is NOT in the inventory

Completeness is claimed against this list, never against silence. An audit returning
"nothing missing" for an unshielded surface detector would be vacuous.

| omission | bias | status |
|---|---|---|
| muon-induced neutrons at the surface | `flatters_SB` | unquantified in this milestone |
| muon-induced secondary gammas at the surface | `flatters_SB` | unquantified in this milestone |
| cosmogenic activation of ⁷¹Ge/⁶⁸Ge/⁶⁵Zn by the fast component | `flatters_SB` | out of scope, Phase 14 |
| ⁷¹Ge EC **K-line X-ray escape** near the wafer surface | `penalizes_SB` | unquantified in this milestone |
| neutron elastic recoils above the 20 MeV ENDF ceiling | `flatters_SB` | **bounded**, Phase 13 |
| the low-energy excess | `flatters_SB` | **by construction**, see plan 16-03 |

**The rows are not netted against each other.** Four flatter `S/B_particle` by leaving
background out; one would penalize it. Netting two separately unquantified effects
would replace them with an invented number.

**The >20 MeV bounds are carried SEPARATELY and are never combined:** in-RoI omission
fraction **1.348166e-05 … 2.554578e-05** against **total-rate** omission fraction
**8.905297e-02 … 1.687424e-01** — four decades apart. Reporting one in place of the
other would misstate the channel entirely.

The K-line escape row is the one that would *raise* the denominator, and it is worth
naming twice: the K line carries **87.59 %** of the EC branching, seven times the
M-line branching, and escape of its 9.9 keV X-ray near the wafer face moves counts
**downward toward the RoI**. Nothing in this milestone computes the escape fraction for
a 110 g wafer.

---

## 6. Two denominator layers, never collapsed

Two of the six background channels arrive as **upper bounds**, not rate estimates.

| layer | channels | RoI B (Ta→Al) | direction |
|---|---|---|---|
| `estimates_only` | neutron + Compton + muon | 5472.001 | an **estimate** |
| `estimates_plus_bounds` | + capture bound + M-line bound | 10002.597 | `S/B_particle` is a **LOWER bound** |

**Summing upper bounds into the denominator makes `S/B_particle` a LOWER bound.** That
direction is part of the result, not a caveat on it. The two layers are never collapsed
into one column and every quoted ratio names its layer.

The two layers differ by a factor 1.83 in the RoI, so **the bounded channels are not
small** — the capture bound alone is 44 % of the full denominator, and it is loose by an
**unknown factor ≤ 1**, because converting it into an in-RoI fraction needs the cascade,
which Phase 14 established is not determined.

---

## 7. The disconfirming checks

### 7.1 Leave-one-out — 40 rows, monotone

Every in-layer removal of a **contributing** channel strictly increases
`S/B_particle`. Ranking in the RoI (`estimates_plus_bounds`, Ta→Al), by the factor the
removal produces:

| rank | channel removed | `S/B_particle` × |
|---|---|---|
| 1 | **neutron elastic** | ×2.188 |
| 2 | **prompt (n,γ) capture** | ×1.785 |
| 3 | ⁷¹Ge EC M line | ×1.013 |
| 4 | Compton γ | ×1.0034 |
| 5 | muon ionization | ×1.0007 |

In `estimates_only` the neutron removal gives ×131.2 — the channel is 99.2 % of that
layer.

**One measured exception, separated rather than swept up.** The ⁷¹Ge M line contributes
**exactly zero** in the sub-eV band: it is a monochromatic line whose reconstructed
image is at 65.0 / 63.0 eV, 100 % inside the RoI and 0 % below 1 eV. Removing a zero
cannot raise a ratio, so demanding a strict increase there would be demanding the wrong
thing. Those two rows carry `monotonicity_check = EXACT_NO_OP_REQUIRED` and are checked
for an **exact** no-op instead — which is a real check on where that line was placed,
not a waiver.

### 7.2 The inelastic exclusion, justified by measurement

Adding the ≤ 2666.833 counts kg⁻¹ day⁻¹ inelastic bound to the RoI
`estimates_plus_bounds` denominator moves `S/B_particle` by **-21.049 %** (ratio
0.789506); in the sub-eV band by -26.887 %. Meanwhile the nuclear recoils that bound
describes sit at **2.271606e+05 eV = 227 keV**, **3.356 decades above** the 100 eV RoI
top.

**Read those two numbers together and do not confuse them.** The ~3 decades is how far
the bound sits from the physics it stands for *in the band*; it is **not** the size of
the move in `S/B_particle`, and it could not have been. The denominator is already
~1 × 10⁴ counts kg⁻¹ day⁻¹, so a 2.67 × 10³ addition can only ever move the ratio by a
factor of order one. **A 3-decade move was never arithmetically available, and its
absence is not evidence against the exclusion.**

The honest consequence, stated rather than hidden: at the assembled
`order_of_magnitude` label a 21 % move is **inside the band**, so **the exclusion is not
load-bearing for the headline at the precision it is quoted to**. It is made because
summing a bound that is ~3 decades loose in the band would let a nearly information-free
quantity into the denominator, not because it would change the answer. The part of that
channel that *does* land near the band is the separate gamma-emission recoil, **2.576622
eV** (⁷⁴Ge 596 keV) and **5.185 eV** (⁷²Ge 834 keV).

### 7.3 Trigger sharpness, and the gap in it

`P_trig` **multiplies** ε; it does not replace it (`CONVENTIONS.md` §I). The sharpness
`k` is fixed by no project artifact and carries a standing `[1, 12]` sensitivity
obligation, and the range is **read from `params.TRIGGER_SHARPNESS_RANGE`**, not
re-typed. On the sub-eV rows:

| quantity | Ta→Al |
|---|---|
| sub-eV `S/B_particle` at the default k = 4 | 4.111043e-04 |
| sub-eV `S/B_particle` at `P_trig ≡ 1` | 4.160981e-04 |
| trigger cost ratio | 0.987999 |
| measured k ∈ [1,12] spread, muon | 1.099112 |
| measured k ∈ [1,12] spread, Compton | 1.379186 |

**The gap is named rather than papered over.** The trigger acts on the **deposit** axis
upstream of `R`, so producing a k-scan of a *reconstructed*-axis rate requires
re-folding, which this plan places out of scope. **No committed reconstructed-axis
k-scan exists for the CEvNS or the neutron channels — and the neutron channel dominates
the sub-eV denominator.** The spreads above therefore cover muon and Compton only and
are a **LOWER BOUND** on the true k-sensitivity of the sub-eV `S/B_particle`, not a
measurement of it. That field travels in the artifact as `k_scan_gap`.

---

## 8. The caveat table that travels with the headline

These attach to the number above and travel into plan 16-03 and into the milestone
record.

**1. The neutron resonance imprint WASHES OUT on the reconstructed axis.** Phase 13's
resolving statistic falls to **3.383 / 3.598** against its **own** pre-declared
threshold of **5.0** — a 9.5× / 8.9× washout, caused by the 12.202 %-per-bin
reconstructed binning acting on a 1.87 %-wide feature. The imprint survives broadening
(32.160 → 6.531) and the deposit rebin (6.113), and dies at the fold.
**Anyone quoting germanium's resonance structure as a discriminating handle in
reconstructed energy would be over-reading it.** The amplitude contrast (33–35 % against
the smoothed control) survives; the resolving statistic does not.

**2. The Landau–Vavilov validity floor is 4111.82 eV, and it indicts the published v1.0
manuscript.** It lies far above the 10.14 eV v1.0 grid floor and **indicts 209 of the
584 bins the v1.0 manuscript published — 35.79 %**, reaching up to 4042.2 eV. Varying
the mean excitation energy `I` over 300–400 eV gives 204–213: **no plausible value makes
it zero.** This is a fact about the **v1.0 paper**, not only about this milestone, and
it bears directly on the usable range of the muon channel in the table above.

**3. The 100 meV bin is the least reliable number in the milestone.** `CONVENTIONS.md`
§J says so. Carry the kernel leakage **with its axis attached**: **48.98 %** below the
floor on the Phase-11 480-bin axis and **49.728 %** on the Phase-13 744-bin axis — the
difference is binning, not physics — together with **0.892 %** landing at unphysical
`T < 0` and a lineshape **skewness of 0.590** against a symmetric Gaussian. Nothing was
renormalized to hide it.

**4. The muon channel's signed bias label is anchor-leg dependent.** The deviation is
**-20.61 %** against **PDG Leg A** (~1 muon cm⁻² min⁻¹ × A_top = 1.7204 Hz);
**BRACKETING DISCLOSURE: PDG Leg B** (I_v ~ 70 m⁻² s⁻¹ sr⁻¹ with cos²θ → 1.1350 Hz)
gives **+20.34 %** on the same adopted 1.3659 Hz. The two legs **bracket** the adopted
rate from opposite sides: **the ~20 % magnitude is solid, the SIGN is not.** It must
never travel without its Leg A citation and the Leg B bracketing. Underneath sits a
30–35 % inter-experiment Gaisser–Guan normalization spread that no in-repo artifact can
narrow, and this channel has **no external benchmark on the reconstructed axis at all**.

**5. Phase 13's Ge-vs-CaWO₄ reversal is conditional.** The finding that Ge is the better
target per kg (Ge/CaWO₄ = 0.673–0.692) rests on a **common-constant-sigma** (`constant-sigma`) substitution;
this repository owns a resonance-resolved `σ_el` for **germanium only**. The direction
is conditional on that assumption and is not a target-comparison result.

**6. There is no external validation of the ratio.** Carried from plan 16-01:
`S/B_particle` has external validation of its **numerator only**, and that check
(VALD-12's signal-side leg) came back **PARTIALLY CONFIRMED and window-conditional** —
it **fails** on the window this project pre-registered and passes only on a declared
alternate its own documents dispute. Since **VALD-11's** deletion there is **no
background-side target-swap validation at all**, and the one signal-side closure
(407.7 dru CaWO₄) has no reproducible artifact.

---

## 9. Re-scope integrity

- **Veto credit = exactly 1.0 BY CONSTRUCTION**, read from
  `surface_environment.veto_credit()` and never re-typed. There is no veto and no shield
  in this configuration, so there is nothing for a rejection credit to be taken against.
  **Exactly one baseline** is emitted: no reduced credit, no for-reference credit, no
  second veto-credited number.
- **`configuration = NUCLEUS's-shielding-absent`** on every row. It is a **different and
  worse** configuration than NUCLEUS's, not a subset of it — the Phase-8 lock, enforced
  here by the attachment-aware text scan, which finds zero occurrences of the forbidden
  adjective attached to this configuration.
- The Phase-9 shielded-token guard is imported **by identity**
  (`se.shielded_token_guard()[0] is ev.SHIELDED_TOKENS`), not re-typed.
- **The observable is named `S/B_particle` everywhere**, never the bare unqualified
  form. The forbidden string is built at runtime in the test so the test file does not
  carry it.
- NUCLEUS's CaWO₄ ≈ 1.2 and Al₂O₃ ≈ 0.13, and CONUS+'s ≈ 0.03, are context for
  **shielded** experiments and are **not** targets this unshielded surface wafer should
  approach.

---

## 10. Checkpoint (Task 3), recorded in full

Standing session directive: run the roadmap without per-phase discussion unless a
genuine blocker arises. The checkpoint's content is recorded here **in full** and the
default was taken. **No approval was given and none is fabricated** — the precedent of
12-03 §6, 13-03 and 14-02 §8.

> **`S/B_particle` = 1.33 × 10⁻² (estimates-only) / 7.29 × 10⁻³
> (estimates-plus-bounds), Ta→Al, RoI 10–100 eV, at `order_of_magnitude`**
> (Al→Hf: 1.32 × 10⁻² / 7.27 × 10⁻³). Denominator ranked by leave-one-out: neutron
> elastic (×2.19) > prompt (n,γ) capture (×1.79) > ⁷¹Ge M line (×1.013) > Compton
> (×1.0034) > muon (×1.0007). The estimates-plus-bounds layer is a **lower bound** on
> `S/B_particle`. Six caveats attached. The three things most worth a physicist's own
> judgement, in order: **(1)** the two-layer bound structure — is summing upper bounds
> into the denominator the right presentation, or should the bounded channels be
> reported only as a separate envelope? **(2)** the omission list — is anything missing
> from it that a surface detector would actually see, and in particular is the K-line
> X-ray escape row the one that should have been computed? **(3)** the resonance
> washout and the Landau–Vavilov indictment, both of which bear on the **published v1.0
> manuscript** and not only on this milestone.
> Accept the assembly and proceed to the LEE overlay (16-03)? **[Y/n/e]** (Enter = Y)

**The 16-01 gate travels with this number.** VALD-12's signal-side leg failed on its
pre-registered window, so the ROADMAP Phase-16 backtracking trigger remains live and the
unresolved gate is on this deliverable as caveat 6 rather than left behind in 16-01.
