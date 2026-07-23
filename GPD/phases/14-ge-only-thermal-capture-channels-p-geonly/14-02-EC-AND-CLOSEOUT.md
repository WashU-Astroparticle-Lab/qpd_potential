# 14-02 — ⁷¹Ge electron-capture lines, and the Phase-14 closeout

**Plan:** 14-02 (wave 2) · **Phase:** 14 Ge-Only Thermal-Capture Channels (P-GEONLY)
**Accuracy label:** `order_of_magnitude`, inherited from the Phase-9 flux through the
Plan 14-01 production rate. Every rate below carries it. **This channel is delivered as a
BOUND, not a quantification** (ROADMAP SC2).

**Interpreter:** `/opt/anaconda3/bin/python3` — numpy 1.26.4, scipy 1.17.1, matplotlib 3.8.0.

---

## 1. The line inventory

### 1.1 Energies, and the Ga identification — CHECKED, not asserted

An EC line energy **is** the binding energy of the captured shell **in the daughter**,
gallium (Z = 31). Allowed EC captures s-electrons, so K / L / M are the 1s / 2s (L1) /
3s (M1) edges. That identification is checked against a **separately retrieved** Ga edge
table (`data/ge71_ec/xraylib_edges.dat`, SHA-256 recorded in
`data/ge71_ec/MANIFEST.md`) rather than marked UNVERIFIED:

| line | ROADMAP energy [eV, **DEPOSITED**] | Ga edge | Ga binding [eV] | difference | status |
|---|---:|---|---:|---:|---|
| **M** | **158.7 ± 1.4** | M1 (3s) | 158.1 | **+0.60 eV (+0.3795 %)** — inside the stated ±1.4 | CHECKED |
| L | 1298.5 | L1 (2s) | 1297.7 | +0.80 eV (+0.0616 %) | CHECKED |
| K | 10368.3 | K (1s) | 10367.1 | +1.20 eV (+0.0116 %) | CHECKED |

The two sources are independent: the line energies are the ROADMAP's CONUS+ sub-keV
calibration anchor; the binding energies are a separately retrieved compilation.
**Provenance honesty:** the edge table is xraylib's own compiled data file, retrieved and
integrity-checked *as a file*; the tabulation it compiles is not further traced, so this
establishes consistency with a standard compilation rather than with a primary measurement.

**158.7 eV is a DEPOSIT.** It is never quoted as a position on the reconstructed axis
(`fp-deposit-as-reconstructed`); §2 measures where the image actually lands.

### 1.2 Activation scenario — stated, never implied

A(t) = A_sat (1 − e^{−λt}), λ = ln2 / 11.43 d = 0.060642 d⁻¹.

**A_sat = 1054.1472 counts kg⁻¹ day⁻¹**, the ⁷⁰Ge(n,γ) production rate from Plan 14-01
over the **full** incident-energy band — epithermal ⁷⁰Ge capture makes ⁷¹Ge just as surely
as thermal capture does; only 90.63 % of the ⁷⁰Ge production is thermal.

**The abundance factor is not optional and it was a live bug.** A first implementation
folded the bare ⁷⁰Ge cross section against N_Ge and returned 5124.68 — the rate for an
isotopically **pure** ⁷⁰Ge wafer, 4.86× too large. It was caught by comparing against the
Plan 14-01 per-isotope row, which already carried the 0.2057 abundance weight.

| scenario | A(t) [counts kg⁻¹ day⁻¹] | fraction of saturation |
|---|---:|---:|
| t = 1 d | 62.03 | 5.88 % |
| t = 11.43 d (one half-life) | 527.07 | 50.00 % |
| t = 30 d | 883.23 | 83.79 % |
| saturation (t → ∞) | 1054.15 | 100 % |

**A ⁷¹Ge rate quoted without its t is undefined, not conservative** — saturation is 17× the
one-day value. Every rate row in `artifacts/v2.0/ge71_ec_lines.csv` carries its scenario,
asserted in test.

### 1.3 Branching — P_K SOURCED-DERIVED, P_L and P_M BOUNDED

No decay-scheme file states the capture-shell branching fractions directly, and none was
written from recollection (`fp-assert-branching`). What the frozen IAEA Live Chart
retrieval **does** state is the fate of the vacancies, and that is enough:

> Every K-shell vacancy created by the capture is filled either **radiatively** (a Ga K
> X-ray) or **non-radiatively** (a K Auger electron). Those channels are exhaustive and
> mutually exclusive, so **P_K = I(K X-rays) + I(K Auger)** per decay.

| quantity | value per 100 decays |
|---|---:|
| I(K X-rays) = Kα1 + Kα2 + Kβ | 45.284 ± 0.252 |
| I(K Auger) | 42.306 ± 0.350 |
| **P_K** | **0.8759 ± 0.0043 — SOURCED (derived)** |

Two reading rules, both verified in code rather than assumed: the rows are filtered to the
**ground-state EC decay** (the files also carry the 198.371 keV isomer's IT rows, which
would inflate every intensity), and only **leaves** are summed (Kβ′1 + Kβ′2 = Kβ, and
KLL + KLX + KXY = K-Auger are both checked to close before use).

**P_L and P_M are not obtainable this way** — L vacancies are produced both by direct L
capture and by the K-vacancy cascade, so the L intensities do not isolate P_L. Both are
therefore **BOUNDED by 1 − P_K = 0.1241**, and the L/M split is left undetermined.

That bound is **8.06× tighter** than the trivial branching ≤ 1. It is still a bound, and a
bound of 1 − P_K on *every* remaining line is a statement that carries limited information —
said plainly rather than dressed as a result.

### 1.4 The coincident neutrino recoil

Q_EC = **232.47 ± 1.15 keV** (IAEA Live Chart, frozen).
**T_ν = Q_EC²/(2Mc²) = 0.408569 eV** — genuinely sub-eV, in the region this milestone
exists to reach.

- as a fraction of the M line: **0.2574 %**
- as a fraction of one reconstructed bin (12.202 %): **0.0211 bins**

It is **coincident** with the shell relaxation, so it **shifts** the deposit rather than
creating a separate sub-eV event, and the shift is 2 % of one bin. A standalone sub-eV event
requires the shell relaxation to **escape**, which is the declared and unmodelled K-line
escape omission (§4).

### 1.5 No IA broadening — and the criterion comes out the OTHER way here

| quantity | value |
|---|---:|
| ω̄_e (lower bound, Ge covalent bond, Phase 15) | 0.634740 eV |
| ω̄ (nuclear, CONVENTIONS §J) | 0.0178597 eV |
| ratio | 35.540× |
| **2W_e = T/ω̄_e at 158.7 eV** | **250.02** |
| 2W_e at the 0.1 eV grid floor (Phase 15's evaluation) | 0.1574 |

**At this line the electron-side IA validity condition 2W_e ≫ 1 is SATISFIED.** Phase 15
evaluated the same criterion at the 0.1 eV grid floor, where it gives 0.1574 < 1 and fails.
**Inheriting Phase 15's sentence would therefore have been wrong at this energy**, and that
is reported rather than absorbed. The criterion does not justify the exclusion here.

The exclusion rests on two other things, both stated:

1. **The frozen kernel is the wrong one.** `ia_broadening` carries the **nuclear** ω̄.
   Transplanting it to an electronic deposit understates the width by **5.9616×** (the
   Phase-15 number, reproduced here).
2. **The deposit is not a recoil.** The ⁷¹Ge EC deposit is the atomic relaxation energy of a
   Ga shell vacancy — a fixed atomic-physics quantity, not a recoil against a
   momentum-distributed target — so there is no Doppler kernel to apply at all. What
   broadens its measured image is the detector response R, which *is* applied.

**The stake is measured, not dismissed.** Phase 15 established that the "too small to
resolve" shortcut would have been **false**, so it is not used. If the *electron-side*
kernel were applied it would give σ = **10.0366 eV = 6.3243 % of the line ≈ 0.518 of one
reconstructed bin** — comparable to the binning, not negligible. `broaden=True` **raises**
on this path rather than defaulting to off, and the rate is never multiplied by exp(−2W).

---

## 2. Where the M line actually lands — MEASURED

Monochromatic 158.7 eV deposit → `shared_energy_grid("v2.0-ext")` bin 256 (centre
160.849678 eV) → `response_matrix_{TaAl,AlHf}_ext.npz` (161 × 744, columns summing to 1) →
trigger on the **deposit** axis multiplying ε (CONVENTIONS §I).

| quantity | Ta→Al | Al→Hf |
|---|---:|---:|
| matrix's own unbinned E_rec **mean** | **65.049 eV** | **62.964 eV** |
| median | 65.045 eV | 62.971 eV |
| p16 / p84 | 64.451 / 65.651 eV | 62.425 / 63.491 eV |
| response `rel_spread` | 0.9281 % | 0.8470 % |
| **mapping slope E_rec / 158.7 eV** | **0.4099** | **0.3967** |
| binned peak bin centre | 66.834 eV | 59.566 eV (59.3 % of counts) |
| populated reconstructed bins | 1 | 2 |
| one reconstructed bin here | 11.519 % | 11.519 % |
| **in-RoI fraction, E_rec 10–100 eV** | **1.000000** | **1.000000** |
| sub-eV (E_rec < 1 eV) fraction | 0.000000 | 0.000000 |

**The image is narrower than one bin.** rel_spread 0.93 % against an 11.5 % bin, so the
apparent width of the reconstructed line is the **binning**, not the physics. This matters
for §1.5: the electron-side IA width that was *not* applied (0.518 bins) is larger than the
response's own spread at this energy, so the exclusion decision is not cosmetic.

**The mapping slope is not a constant 0.5.** The same chain maps a 1 eV deposit to
0.5056 eV (Ta→Al) / 0.5032 eV (Al→Hf) — consistent with Phase 13's median-based sub-eV
regime boundaries 0.497240 / 0.495855 eV, which are a slightly different statistic on the
same curve — but at 158.7 eV the slope has fallen to 0.4099 / 0.3967. Assuming a constant
0.5 would have placed the line at 79.4 eV; the measured values are 65.0 and 63.0 eV. Both
readings land inside the RoI, so the conclusion is unchanged — but it is unchanged **by
measurement**, not by the assumption.

### 2.1 ROADMAP SC3 adjudication

> **"…with the M-shell line landing inside the RoI"** — **CONFIRMED**, by measurement, and
> for a reason the ROADMAP does not state.

- On the **DEPOSIT** axis the clause is **false**: 158.7 eV > the 100 eV RoI top.
- On the **RECONSTRUCTED** axis — the reported observable, and what the clause is actually
  about — **100.0000 % of the line's reconstructed counts fall inside E_rec 10–100 eV**, for
  both designs. The reason is the measured mapping slope ≈ 0.40, which carries the deposit
  down to 65.0 / 63.0 eV.
- **The ROADMAP asserts the conclusion without deriving it.** Had the slope been ≳ 0.63 the
  clause would have been REFUTED, and nothing in the criterion's own text would have
  revealed that. Phase 13 caught itself making exactly this cross-axis error once; this is
  the same error avoided by measurement.

### 2.2 Counts budget

Identical for both designs, because R's columns each sum to 1:

| quantity | value |
|---|---:|
| input counts | 130.819666 |
| deposit counts | 130.819666 |
| reconstructed counts | 130.819666 |
| leaked below floor / above top | 0 / 0 |
| `residual_retained_plus_leaked` | 0.000e+00 |
| `residual_retained_only` | +0.000e+00 |
| `residual_fold` | 0.000e+00 |

The two residuals **coincide by construction** here: no broadening is applied and the
monochromatic input lies strictly inside the deposit axis, so there is no kernel leakage to
separate them. That is **stated** rather than presented as two independent confirmations —
the Phase-13 pattern keeps them separate precisely because there the leakage is real.
Nothing is rescaled.

### 2.3 Trigger composition

- `P_trig ≡ 1` reproduces the untriggered spectrum **bit-identically** (`np.array_equal`,
  not `allclose`) on both `N_rec_trigger` and `dRdErec_trigger`, for both designs.
- P(0.5 eV) = 1/2 to 1e-12, evaluated on the **deposit** centres before R acts.
- P_trig at the line's deposit bin = **0.999999999907** — essentially 1, as expected
  2.5 decades above E50. No finding about the curve.
- **k-sensitivity over [1, 12]** on the in-RoI rate: **0.31 %** (k=1 costs 0.31 %,
  k=4 and k=12 are indistinguishable). The trigger is not a lever on this channel.

### 2.4 Shared-axis comparison

Every operand below is read from a **committed reconstructed-axis artifact** and the axis
tag travels with it; a test asserts both operands of every comparison are `RECONSTRUCTED`.
The band integrator reproduces the committed headline numbers (CEvNS total 118.7286 /
118.7292 against the quoted 118.73; neutron in-RoI 5430.2866 / 5485.1515 against
5430.287 / 5485.152), so it is validated rather than trusted.

| comparison, E_rec 10–100 eV, **saturation scenario** | Ta→Al | Al→Hf |
|---|---:|---:|
| ⁷¹Ge EC M-line **bound** | **130.82** | **130.82** counts kg⁻¹ day⁻¹ |
| Phase-12 CEvNS in-RoI | 72.92 | 73.14 |
| **ratio, M-line bound / CEvNS in-RoI** | **1.794×** | **1.789×** |
| ratio, M-line bound / CEvNS **total** (118.73) | 1.102× | 1.102× |
| Phase-13 neutron elastic in-RoI | 5430.29 | 5485.15 |
| ratio, M-line bound / neutron in-RoI | 0.0241 | 0.0239 |

**At saturation the M-line bound exceeds the CEvNS signal inside the RoI by ~1.8×**, and it
lands there entirely. At t = 1 d the bound is 7.70 counts kg⁻¹ day⁻¹, ~11 % of the CEvNS
in-RoI rate. **The scenario is the difference between "dominant" and "sub-dominant", which
is exactly why `fp-saturation-unstated` is a real proxy.**

Figure: `artifacts/v2.0/capture_channel_bounds.pdf`, both designs, RoI shaded, sub-eV
boundary drawn, the deposit-vs-reconstructed distinction annotated on each panel, and
`accuracy_label` in a box on the figure.

---

## 3. ROADMAP Phase-14 success criteria — five verdicts

| # | criterion (abridged) | verdict | evidence |
|---|---|---|---|
| **SC1** | ENDF MT=102 for five Ge isotopes **and** EGAF capture-γ line lists acquired and frozen as provenance-headed artifacts, Phase-7 pattern | **CONFIRMED** | `artifacts/v2.0/ge_capture_xs.csv`; `data/egaf/MANIFEST.md` (curl command, byte counts, SHA-256, all five product nuclei); `14-01-CAPTURE-BOUNDS.md` §1 |
| **SC2** | Cascade recoil **bounded, not quantified**; single-γ limit never the cascade answer | **PARTIALLY CONFIRMED** | `artifacts/v2.0/capture_recoil_bounds.csv`; `14-01-CAPTURE-BOUNDS.md` §3 |
| **SC3** | ⁷¹Ge EC inventory at 158.7 ± 1.4 / 1298.5 / 10368.3 eV, **M line landing inside the RoI**, folded through the response chain | **CONFIRMED** | `artifacts/v2.0/ge71_ec_lines.csv`, `ge71_ec_dRdErec_{TaAl,AlHf}.csv`, `capture_channel_bounds.pdf`; §2.1 above |
| **SC4** | φ_th disposition explicit; never zero | **CONFIRMED**, discharged on **branch (a)** | §5 below; `14-01-CAPTURE-BOUNDS.md` §2.3 and §2.6 |
| **SC5** | Ge inelastic (⁷⁴Ge 596 keV, ⁷²Ge 834 keV) at least bounded and named | **CONFIRMED** | `artifacts/v2.0/capture_recoil_bounds.csv`; `14-01-CAPTURE-BOUNDS.md` §3.5 |

**No window was narrowed, no threshold lowered and the RoI was not moved to make any
criterion true.** One is PARTIAL, and the reason is a measurement, not a shortfall:

### Why SC2 is PARTIAL

The **shape** of the answer is delivered exactly as required — the in-RoI contribution is a
rigorous, cascade-independent upper bound; the single-γ ceilings sit beside it labelled
`RIGOROUS_BOUND`; the multiplicity-N mean is symbolic; nothing is presented as a
quantification. But **both of the criterion's own illustrative numbers are superseded by
measurement on Ge**:

- *"single-γ kinematic limit 473 eV at 8 MeV"* — the Ge ceilings from the actual ENDF QM
  values are 415.77 / 338.30 / **754.11** / 302.87 / 257.07 eV. The maximum belongs to ⁷³Ge,
  which is also the isotope dominating the capture rate, and it is **59 % higher** than the
  illustrative figure.
- *"tens of eV for a realistic multi-γ cascade"* — the EGAF-sourced isotropic-cascade means
  over the observed lines are **149.5 – 186.5 eV**, with rigorous upper brackets of
  250.9 – 408.9 eV, on observed multiplicities of only **1.66 – 4.25**. "Tens of eV" would
  need a multiplicity roughly an order of magnitude larger than EGAF observes.

Neither correction changes the rigorous bound, which does not use either number.

---

## 4. Un-netted directional-bias table (Phase-9 §7 schema), whole phase

Each row stands alone. **Nothing is netted against anything else.**

| # | omission / configuration choice | direction | magnitude, measured |
|---|---|---|---|
| 1 | Outdoor flux leg `phi_default = phi_hi`; `phi_lo` refused | `penalizes_SB` | factor 5 on the background if the indoor leg were adopted. A configuration choice, not an error bar |
| 2 | 20 MeV ENDF ceiling — capture | `flatters_SB` | top-decade fraction 0.09 % → negligible |
| 3 | 20 MeV ENDF ceiling — inelastic | `flatters_SB` | top-decade fraction **73.55 %**; Phase 13's 11.85× elastic margin **not** reused; carried unquantified |
| 4 | ~197 MeV flux-grid ceiling | `flatters_SB` | inherited from Phase 13 unchanged |
| 5 | Thin-target formula, no capture self-shielding | `penalizes_SB` | epithermal band overstated by ≤ 11.00 % (P_capture(2 mm) = 73.6 % at the 102.59 eV resonance) |
| 6 | Cascade in-RoI fraction (≤ 1) unknown | `penalizes_SB` | unbounded above by 1; the observed EGAF cascade covers only 60–71 % of Q_cap |
| 7 | **Saturation** as the ⁷¹Ge scenario | `penalizes_SB` | a genuine upper bound for any history, and **17×** the one-day value |
| 8 | **⁷¹Ge M/L branching bounded by 1 − P_K** rather than sourced | `penalizes_SB` | the M line is quoted at ≤ 0.1241 of the EC rate; the true P_M is smaller by an unknown factor |
| 9 | **K-line X-ray escape near the wafer surface** — declared, NOT modelled | `flatters_SB` | escape moves 10.37 keV deposits down toward the RoI; omitting it understates the low-energy background by an unquantified amount |
| 10 | **No IA broadening on the EC line** | `penalizes_SB` (likely) | the electron-side kernel would spread the line by 0.518 reconstructed bins; since the line sits entirely inside the RoI, spreading could only move counts out. Not applied because the frozen kernel is the wrong one |
| 11 | 293.6 K ACE processing against a mK target | `neutral` on band integrals | +0.010 % epithermal; unresolved for resonance line shapes |
| 12 | eV–keV differential flux shape | **UNBOUNDED**, direction undetermined | Phase 13's perturbations moved the in-RoI elastic rate by +41.33 % and −16.31 % |

---

## 5. φ_th disposition (ROADMAP SC4)

> **Φ_th = 2.767075×10⁻³ cm⁻² s⁻¹** over **0.01 – 0.5 eV**, the standard **cadmium cutoff**
> convention, is **PHASE 9's product**, delivered by
> `09-02-NEUTRON-DECLARATION.md` §5. It was **SOURCED, not gapped**, so **ROADMAP SC4
> discharges on branch (a)**. It is consumed unchanged by Phase 14 and is **not** re-derived
> here. Attributing it to Phase 13 would be wrong — Phase 13's closeout explicitly hands it
> forward labelled as Phase 9's.

**Biffl comparison, with its direction.** Biffl et al., PRD **107**, 092011 (2023) state a
requirement Φ_th < 7×10⁻⁴ n/cm²·s. The adopted flux is **3.95× ABOVE** it: this unshielded
sea-level configuration **does not meet** the requirement. Biffl also state that capture
recoils "strongly overlap the CEvNS signal for recoils ≲ 100 eV" — the regime both of this
phase's channels land in.

**Nothing derived in Phase 14 is reported as zero.** Every capture band rate, the total, the
⁷¹Ge production rate and every EC line bound are strictly positive, asserted by execution.
The one exact zero anywhere is the thermal and epithermal **inelastic** rate, which is zero
because MT=51–91 is a **thresholded** reaction and no discrete level is open below ~600 keV —
a measured zero from physics, not a manufactured one, and it is not the capture channel.

---

## 6. Hand-off to Phase 16

Phase 16 receives, as **labelled bounds** with `accuracy_label = order_of_magnitude`:

| channel | quantity | scenario / caveat |
|---|---:|---|
| prompt (n,γ) cascade recoils | **≤ 4399.78 counts kg⁻¹ day⁻¹** in the RoI | rigorous, cascade-independent; loose by an unknown factor ≤ 1 |
| — of which non-thermal | 1034.24 counts kg⁻¹ day⁻¹ (23.51 %) | **do not fold the thermal band alone** |
| ⁷¹Ge EC **M line** | **≤ 130.82** counts kg⁻¹ day⁻¹, **100 % in-RoI**, at E_rec ≈ 65.0 / 63.0 eV | **saturation**; at t = 1 d, ≤ 7.70 |
| ⁷¹Ge EC **K line** | 923.33 counts kg⁻¹ day⁻¹ at saturation, deposit 10.37 keV | SOURCED P_K = 0.8759; **outside** the RoI on both axes; K-shell X-ray escape not modelled |
| ⁷¹Ge EC **L line** | ≤ 130.82 counts kg⁻¹ day⁻¹, deposit 1298.5 eV | saturation; outside the RoI |
| Ge discrete inelastic | ≤ 2666.83 counts kg⁻¹ day⁻¹ | very loose in the RoI: nuclear recoils ~227 keV; only the 2.577 / 5.185 eV γ-emission recoils land near the band |

Attached: the twelve-row un-netted directional-bias table (§4), the declared omissions
(K-line X-ray escape; cascade in-RoI fraction; cosmogenic ⁷¹Ge/⁶⁸Ge/⁶⁵Zn production by the
fast component, which is a real surface-detector effect deliberately outside this phase),
and the note that **Φ_th is Phase 9's product, sourced on branch (a)**.

**Flagged for the orchestrator — not edited by any plan in this phase:**

1. **CALC-23's requirement text** still reads *"Gated on the in-shield thermal flux φ_th,
   which NUCLEUS does not publish"*. That framing was removed by the 2026-07-22 re-scope and
   needs re-wording.
2. **CALC-23's title, "Ge-only thermal-capture channel", is measurably too narrow in a
   second way.** 23.51 % of the capture channel is not thermal. The thermal-dominance test
   passed its 60 % threshold, so the framing survives — but it is not a description of the
   whole channel.
3. **The ROADMAP Phase-14 plan checkboxes** are the orchestrator's to tick.

---

## 7. Audits

| audit | result |
|---|---|
| `accuracy_label` present | all six data artifacts, both reports, and in the figure's text stream |
| Phase-9 shielded-token scan (`SHIELDED_TOKENS` + `_EXTRA`, `is_not_applied`) | **zero APPLIED hits** over the module, both reports and all artifacts |
| `phi_lo` line scan over the module | **zero uses** — comments and string literals only |
| veto credit | exactly 1.0 by construction; not imported into this channel |
| disposition register | 71 rows, closure test passes with no unregistered `.csv`/`.npz` |
| `np.nan_to_num` | absent from this module |
| double broadening | `broaden=True` **raises** on the EC path |

---

## 8. CHECKPOINT — Phase 14 closeout (Task 3, `checkpoint:human-verify`)

> ## CHECKPOINT REACHED — Phase 14 closeout
>
> What a reviewer should look at, in order:
> 1. `artifacts/v2.0/capture_channel_bounds.pdf` — the M line's reconstructed image against
>    the CEvNS and neutron spectra on the shared axis.
> 2. **The SC3 adjudication.** 158.7 eV is a *deposit*; whether its reconstructed image lands
>    in the 10–100 eV RoI is the measured question, and the roadmap asserts the answer
>    without deriving it.
> 3. **The bound's usefulness.** If every line is bounded only by the total EC rate, the
>    bound is true and may carry little information. That judgement is a physicist's, not a
>    test's.
>
> Accept the closeout and hand Phase 14 to Phase 16? **[Y/n/e]** (Enter = Y)

**Recorded, and closed on the default, under the standing session directive.**

On point 3, the evidence moved during execution and the reviewer should know it: the lines
are **not** bounded only by the total EC rate. P_K was derived from the frozen retrieval by
K-vacancy conservation, so the M and L bounds are 1 − P_K = 0.1241 rather than 1 — **8.06×
tighter**. The M-line bound is still 1.79× the CEvNS in-RoI rate at saturation, so it stays
a live background rather than a vacuous statement. What remains genuinely uninformative is
the **L/M split**: both lines carry the same bound, and only the M line is inside the RoI,
so the M-line number is the one carrying the looseness.

---

## 9. Reproduction

```bash
PYTHONPATH=src /opt/anaconda3/bin/python3 -c \
  "from qpd_potential import capture_channel as c; \
   c.write_ge71_ec_lines_csv(); \
   c.write_ge71_ec_erec_csv('Ta->Al'); c.write_ge71_ec_erec_csv('Al->Hf'); \
   c.make_capture_bounds_figure()"
/opt/anaconda3/bin/python3 -m pytest tests/test_ge71_ec.py tests/test_capture_channel.py -q
```

Every number above is traceable to a locally frozen artifact through a recorded command.
`WebFetch` was not used as a quote source anywhere in this phase.
