# Plan 10-05 --- The Emergent Counting-Statistics Floor

**Phase:** 10 --- Sub-eV Grid Extension and the Trigger Observable (P-GRID)
**Discharges:** `claim-floor`; ROADMAP Phase 10 success criterion 5.
**Interpreter:** `/opt/anaconda3/bin/python3` --- numpy 1.26.4, scipy 1.17.1.

---

## 0. READ THIS BEFORE QUOTING ANY NUMBER BELOW

> **This project has no resolution parameter anywhere.** Every percentage in this document
> is a BEST-CASE lower bound on the achievable
> fractional width, with NO noise sources of any kind in the model. It is NOT the
> detector's energy resolution. This project has NO resolution parameter anywhere,
> and never quoted the QPD paper for one.**

The width of R(E_rec|E_dep) is **emergent counting statistics only** --- multinomial
over the per-sensor EMG pmf in the unsaturated regime, Poisson about the analytic
censored mean in the saturated one. Nothing else contributes.

**Noise sources explicitly NOT in the model**, enumerated so the omission is auditable:

| Omitted | Status |
|---|---|
| **baseline** noise | not modelled |
| **amplifier** noise | not modelled |
| **phonon-collection** fluctuation | not modelled |
| **position dependence** on the wafer | not modelled |
| **readout** noise | not modelled |

Quoting any figure below as σ_E/E, or as "the resolution", without the best-case
qualifier **in the same sentence or the one before it**, is the milestone-wide
forbidden proxy **`fp-poisson-as-resolution`**.

**Regime boundary.** `trigger.SUBEV_REGIME_BOUNDARY_eV` = **1 eV** (CONVENTIONS §I).
Below it the reported observable is the **trigger probability** P_trig(E_dep), **not**
dR/dE_rec. The floors quoted at 0.1 eV and 0.5 eV therefore describe the width of a
response kernel in a regime where **the differential rate is not what this project
reports**.

---

## 1. Derived, not copied (`fp-floor-quoted-not-derived`)

The roadmap's percentages come from an **orchestrator note recorded in `GPD/STATE.md`**,
not from a verified phase deliverable. Echoing them back would make this document
circular evidence for them. So N_obs was extracted from the plan 10-04 extended
matrices (`artifacts/v2.0/response_matrix_*_ext.npz`, `non_paralyzable`, the canonical
variant per CONVENTIONS §F) and the floor computed as 100/√N_obs.

### 1.1 Ta→Al

| E_dep | **measured N_obs** | **derived floor = 100/√N_obs** | roadmap figure | difference |
|---|---|---|---|---|
| 0.10138 eV | **7.980** | **35.399 %** | 35.6 % | −0.56 % |
| 0.49382 eV | **39.019** | **16.009 %** | 15.9 % | +0.69 % |
| 10.145 eV | **773.399** | **3.596 %** | 3.6 % | −0.12 % |
| 98.603 eV | **6557.064** | **1.235 %** | 1.2 % | +2.91 % |

### 1.2 Al→Hf

| E_dep | **measured N_obs** | **derived floor = 100/√N_obs** | roadmap figure | difference |
|---|---|---|---|---|
| 0.10138 eV | **10.158** | **31.375 %** | 31.6 % | −0.71 % |
| 0.49382 eV | **49.100** | **14.271 %** | 14.2 % | +0.50 % |
| 10.145 eV | **965.113** | **3.219 %** | 3.2 % | +0.59 % |
| 98.603 eV | **8021.322** | **1.117 %** | 1.1 % | +1.50 % |

**Every derived floor agrees with the roadmap figure to within 3 %**, and the measured
N_obs at 0.5 eV is **39.019 / 49.100** against the note's 39.4 / 49.9 (−0.97 % / −1.60 %).
The roadmap figures are corroborated by the pipeline rather than assumed.

*(All eight of the above are BEST-CASE floors with no noise sources — see §0.)*

---

## 2. The 100 eV saturation signature --- the check whose failure would be the finding

Linear scaling of N_obs from the measured 0.5 eV value would give, at 98.603 eV:

| Design | measured N_obs | **linear extrapolation** | ratio | derived floor (measured) | floor if linear | roadmap |
|---|---|---|---|---|---|---|
| Ta→Al | **6557.1** | 7791.1 | **0.8416** | **1.235 %** | 1.133 % | 1.2 % |
| Al→Hf | **8021.3** | 9804.1 | **0.8182** | **1.117 %** | 1.010 % | 1.1 % |

*(Best-case floors, no noise sources.)*

**OUTCOME: the measured N_obs is BELOW the linear extrapolation for both designs**
(ratios 0.842 and 0.818), i.e. **sub-linear**, consistent with the Phase-5 saturation
onsets at ~52.9 eV (Ta→Al) and ~32.1 eV (Al→Hf), both of which sit below 98.6 eV.

The plan stated plainly that **reproducing exactly the linear values would be a FINDING,
not a pass** --- it would mean saturation was not entering the response above the onset.
**It did not happen.** The measured floors 1.235 % / 1.117 % land on the roadmap's
sub-linear 1.2 % / 1.1 % and *not* on the naive linear 1.133 % / 1.010 %; the measured
value is closer to the roadmap figure than the linear one is, for both designs.
Saturation is entering the response.

---

## 3. Is 1/√N even the right description at 0.1 eV? Compared, not assumed

The plan requires 1/√N_obs to be checked against the **actual column spread** measured
in plan 10-04, with a verdict.

| Design | E_dep | **actual std/mean** | **1/√N_obs label** | label / actual |
|---|---|---|---|---|
| Ta→Al | 0.10138 eV | **36.625 %** | 35.399 % | 0.967 |
| Ta→Al | 0.49382 eV | 16.220 % | 16.009 % | 0.987 |
| Ta→Al | 10.145 eV | 3.461 % | 3.596 % | 1.039 |
| Ta→Al | 98.603 eV | 1.164 % | 1.235 % | 1.061 |
| **Al→Hf** | **0.10138 eV** | **27.458 %** | **31.375 %** | **1.143** |
| Al→Hf | 0.49382 eV | 16.150 % | 14.271 % | 0.884 |
| Al→Hf | 10.145 eV | 3.106 % | 3.219 % | 1.036 |
| Al→Hf | 98.603 eV | 1.049 % | 1.117 % | 1.065 |

*(Best-case widths, no noise sources.)*

### VERDICT: they agree above ~10 eV and disagree by ~13 % at and below 0.5 eV.

- **Ta→Al at 0.1 eV**: the label understates the actual spread by 3.4 % --- acceptable.
- **Al→Hf at 0.1 eV**: the label **overstates** the actual spread by **12.5 %**
  (31.375 % against a measured 27.458 %).
- **Al→Hf at 0.5 eV**: the label **understates** it by 11.6 %.

So the discrepancy is not even one-signed: 1/√N is too wide at 0.1 eV and too narrow at
0.5 eV for the same design. **A single Gaussian fractional width is a marginal
description of these columns**, and the sub-eV floors should be quoted with that
attached rather than as though 1/√N described the distribution.

### Why, mechanically (plan 10-04, §5.1)

At 0.1 eV the column holds N_obs ≈ 8–10, and plan 10-04 measured that **the registered
count is not an integer**: 228 (Ta→Al) / 359 (Al→Hf) distinct non-integer values out of
5000 realizations. Both sensor classes carry **fractional populations**
(πr² = 12.566371 on-spot; 10287.433629 off-spot), so a `frac × extra` term is added, and
each class sum is then rescaled by `mu_analytic/mu_pool` (1.0515 and 1.0879 at 0.1 eV
for Ta→Al) to pin the class mean.

The distribution is therefore **neither a Poisson staircase nor a Gaussian** --- it is a
two-class lattice of independently-rescaled sums. 1/√N_obs is a label attached to it,
not a description derived from it.

---

## 4. What is missing and is COMPARABLE in size: the Phase-11 broadening

The impulse-approximation quantum broadening σ_E = √(E_R ω̄) is **not in the model**.
ROADMAP Phase 11 success criterion 3 puts it at **15.5–20.5 %** at the 0.5 eV
threshold --- **comparable to the counting floor itself** (16.0 % / 14.3 % measured
here).

Added **in quadrature** with the measured counting floors at 0.5 eV:

| Design | counting floor (best case) | Phase-11 broadening | quadrature sum |
|---|---|---|---|
| Ta→Al | 16.009 % | 15.5 – 20.5 % | **22.3 – 26.0 %** |
| Al→Hf | 14.271 % | 15.5 – 20.5 % | **21.1 – 25.0 %** |

matching the roadmap's ~22–26 %.

**Consequence:** at the 0.5 eV threshold the counting floor is **at most about
two-thirds** of the width that the two known contributions would already produce, and
neither of them is a noise source. Quoting the counting floor alone as the achievable
width would understate it by ~40 %, before any of the five omitted noise sources in §0
is added.

---

## 5. The floor inherits every weakness of the sub-eV response

**A tighter-looking floor at low energy is not a better detector. It is a longer
extrapolation.**

1. **The quasiparticle yield is exactly linear**, `N_qp = ε·E_sensor/Δ_tr`, with no
   pair-breaking threshold. Measured at 0.1 eV for Ta→Al: **6.89 µeV** of energy per
   off-spot sensor against a **190 µeV** Al trap gap, and the model assigns **0.018132
   quasiparticles** to that sensor. N_obs ≈ 8 at 0.1 eV is the aggregate of ~10,287
   such fractional assignments. **The 35.4 % / 31.4 % floors rest entirely on that.**
2. **`f_prompt` (0.3, range 0.1–0.5) and `r` (2.0 sensors, range 1–5)** are LOW-confidence
   exposed parameters with no thin-wafer QPD measurement behind them, and they set how
   much energy reaches the on-spot sensors at 0.1 eV.
3. **At 0.1 eV the floor rests on a registered count of order 10** (7.980 / 10.158),
   where a single Gaussian fractional width is a marginal description --- quantified in
   §3.
4. **The Phase-5 convergence benchmark does not transfer.** ≤ 1.8 % peak-cell Monte
   Carlo error at N_s = 5000 was measured *above* 10.14 eV; at 0.1 eV the best per-cell
   relative MC error is **3.84 % / 3.43 %**, roughly twice.

---

## 6. Provenance of every number in this document

| Quantity | Source |
|---|---|
| N_obs, column spread, distinct-value counts | `artifacts/v2.0/response_matrix_*_ext.npz`, keys `N_obs_mean_non_paralyzable`, `rel_spread_non_paralyzable`, `n_distinct_Erec_non_paralyzable` (plan 10-04) |
| derived floors | 100/√N_obs, computed here |
| roadmap comparison figures (35.6/31.6, 15.9/14.2, 3.6/3.2, 1.2/1.1 %; N_obs 39.4/49.9) | `GPD/ROADMAP.md` Phase 10 success criterion 5, originating in a `GPD/STATE.md` orchestrator note --- **comparison targets, not inputs** |
| saturation onsets ~52.9 / ~32.1 eV | Phase 5, reproduced by the anchor notebook (`crossover default point`) |
| Phase-11 broadening 15.5–20.5 % | `GPD/ROADMAP.md` Phase 11 success criterion 3 --- **not implemented anywhere** |
| 6.89 µeV / 190 µeV / 0.018132 qp | measured directly in plan 10-04, §7 |
| regime boundary 1 eV | `trigger.SUBEV_REGIME_BOUNDARY_eV`, imported |

**If the pipeline and the roadmap ever disagree, the pipeline wins and the roadmap
figure is flagged.** They agree here to within 3 %.
