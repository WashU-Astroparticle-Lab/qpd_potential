# 11-02 — In-phase derivation of the impulse-approximation width σ_E

**Plan:** 11-02 (CALC-15) · **Deliverable:** `deliv-width-derivation` · **Date:** 2026-07-22
**Reproduce:**

```bash
/opt/anaconda3/bin/python3 scripts/make_ia_width_table.py
/opt/anaconda3/bin/python3 -m pytest tests/test_ia_broadening.py -q
```

---

## 1. The derivation, from the impulse approximation — not from the closed form

Impulse approximation (Sears, Phys. Rev. B **35**, 2038 (1987)): at momentum transfer **q** large
enough that the struck nucleus recoils before its neighbours can respond, the nucleus behaves as a
free particle carrying its *initial* momentum **p**. Energy conservation for a free nucleus of mass
m_N struck with momentum transfer **q**:

    (p + q)²/(2m_N) − p²/(2m_N)  =  q²/(2m_N)  +  q·p/m_N   ≡   ω

So the energy transfer is **not** the single value q²/2m_N. It is a distribution, inherited from the
distribution of **p** in the ground state.

**Mean.** For an isotropic momentum distribution ⟨**p**⟩ = 0, so

    ⟨ω⟩ = q²/(2m_N) = E_R

exactly — the broadening does not shift the centroid. (Checked numerically at every tabulated energy
by `test_sigma_derivation`; the mean equals E_R to 1e-15 relative.)

**Variance.** Only the second term fluctuates:

    Var(ω) = ⟨(q·p)²⟩/m_N² = q²⟨p_∥²⟩/m_N² ≡ q² σ_p²/m_N²

where σ_p² = ⟨p_x²⟩ is the **1-D** momentum spread — the momentum-space partner of the 1-D ⟨u_x²⟩
locked in `CONVENTIONS.md` §J, and for cubic Ge the projection is again exact by symmetry.

**Zero-point momentum spread.** For a harmonic oscillator ⟨p_x²⟩ = m_N ω/2 and
⟨u_x²⟩ = 1/(2 m_N ω) (ħ = 1), whose product is the uncertainty minimum ħ²/4. With
σ_p² = m_N ω̄/2 and q = √(2 m_N E_R):

    σ_E = q σ_p / m_N = √(2 m_N E_R) · √(m_N ω̄/2) / m_N = √(E_R ω̄)

**m_N cancels identically.** Verified in code over a 28× mass range (`test_sigma_derivation`).

**Units, ħ restored.** q and σ_p in eV/c, m_N in eV/c²: `q σ_p/m_N` → eV. `σ_p² = m_N ω̄/2` →
(eV/c²)(eV) = eV²/c². No explicit ħ survives once the phonon scale is carried as an *energy* rather
than an angular frequency; ħ was already consumed once, in `⟨u_x²⟩ = (ħc)²/(2 m_N c²) ∫g/ω dω`.

**Validity.** The IA criterion is q ≫ √(2 m_N ω̄), i.e. **E_R ≫ ω̄**, i.e. **2W ≫ 1**
(Campbell-Deem et al., Phys. Rev. D **106**, 036019 (2022)). With ω̄ = 17.86 meV: 2W = 5.60 at the
100 meV grid floor, rising linearly to 5599 at 100 eV. Satisfied — but only by a factor of ~5.6 in
the bottom bin, so the O(1/2W) ≈ 18 % residual there is real. Plan 11-03 owns bounding it; every
bottom-bin width in this plan carries it.

---

## 2. IDENTITY FLAG — σ_E/E_R = 1/√(2W) is not evidence

    σ_E/E_R = √(ω̄/E_R) = 1/√(E_R/ω̄) = 1/√(2W)

This is **TRUE BY CONSTRUCTION**, because `2W ≡ E_R/ω̄` (`CONVENTIONS.md` §J). It holds for *any*
ω̄ whatsoever — including physically absurd ones. `test_identity_flag` demonstrates exactly that by
verifying the relation at ω̄ = 0.1 meV, 0.5 eV and 12 eV, none of which is a phonon energy in
germanium.

**Reporting it as a cross-check of the width is forbidden proxy `fp-identity-as-evidence`**, the same
failure mode as the momentum-transfer route in plan 11-01. The decisive content of ROADMAP SC3 is
the **numerical values** and the **quadrature with the counting floor**, not this relation.

---

## 3. The check the closed form hides — and it does not come out favourably

`σ_p² = m_N ω̄/2` and `⟨u_x²⟩ = 1/(2 m_N ω̄)` share **one** ω̄ only for a **single-mode** oscillator.
For a real spectrum they are different moments of g(ω). From the same normal-mode expansion that
gave ⟨u_x²⟩ in plan 11-01 (with ∫g dω = 1):

    ⟨u_x²⟩ = (ħ²/2m_N) ∫ g(ω)/ω · coth(ω/2k_BT) dω   →  (1/2m_N)·⟨1/ω⟩  =  1/(2 m_N ω̄_u)
    ⟨p_x²⟩ = (m_N/2)   ∫ g(ω)·ω · coth(ω/2k_BT) dω   →  (m_N/2)·⟨ω⟩     =  m_N ω̄_p/2

so

    ω̄_u ≡ [∫ g/ω dω]⁻¹   HARMONIC mean   — governs ⟨u_x²⟩ — **this is the LOCKED ω̄**
    ω̄_p ≡  ∫ g·ω dω      ARITHMETIC mean — governs ⟨p_x²⟩ — **this is what σ_E actually needs**

By Cauchy–Schwarz, ⟨ω⟩⟨1/ω⟩ ≥ 1 with equality only for a single mode, so **ω̄_p ≥ ω̄_u always**.
Building σ_E on the locked (harmonic) ω̄ therefore **understates** the width — a one-sided bias, and
in the direction that makes the broadening look smaller than it is.

### 3.1 Oracle first: the analytic Debye ratio must be exactly 9/8

For g(ω) = 3ω²/ω_D³ on [0, ω_D]:

    ω̄_p = ∫₀^{ω_D} ω·(3ω²/ω_D³) dω = 3ω_D/4
    ⟨1/ω⟩ = ∫₀^{ω_D} (3ω²/ω_D³)/ω dω = 3/(2ω_D)  ⟹  ω̄_u = 2ω_D/3
    ω̄_p/ω̄_u = (3/4)/(2/3) = **9/8 exactly**

| Quantity | Closed form | Diagnostic returns | Verdict |
|---|---|---|---|
| ω̄_p | 3ω_D/4 = 24.1716 meV | 24.17162 meV | PASS |
| ω̄_u | 2ω_D/3 = 21.4859 meV | 21.48588 meV | PASS |
| ratio | 9/8 = 1.125 | **1.1249999999719** | PASS (2.5e-11) |
| √ratio | 1.060660 | 1.060660 | PASS |

The diagnostic is correct before it touches germanium.

### 3.2 Ge: the disconfirming check FIRED

| Spectrum | ω̄_u (harmonic) | ω̄_p (arithmetic) | ⟨ω⟩⟨1/ω⟩ | **√ratio = σ_E correction** |
|---|---|---|---|---|
| Debye (oracle) | 21.4859 meV | 24.1716 meV | 1.125000 | 1.06066 |
| **Measured Ge** | **17.85968 meV** | **24.19553 meV** | **1.354758** | **1.163941** |

`ω̄_u` reproduces the locked ω̄ to 1e-9 — as it must, since they are the same quantity computed by
two code paths; a mismatch would have meant one quadrature was wrong.

**Real Ge is 20 % worse than Debye at this.** The plan's `unresolved_questions` asked whether the
mismatch "is large enough on the real Ge VDOS to matter", expecting the Debye 9/8 → 6 % in σ_E. The
answer is **no, it is bigger: +16.4 % on every width**, because real Ge has flat, heavily-populated
transverse-acoustic branches near 8 meV *and* a separated optical group near 35 meV, which pushes
the arithmetic and harmonic means further apart than a smooth ω² density can.

**Handling.** The headline widths stay on the locked ω̄ — so ROADMAP SC3's stated identity holds
exactly and the phase does not silently redefine its own convention mid-milestone. The correction is
carried as an explicit, labelled, **one-sided** multiplicative systematic ×1.1639 in a dedicated
column of the width table (`frac_width_upper_moment`) and as the shaded band on the figure.

---

## 4. Width table against ROADMAP SC3

Locked ω̄ = 17.859677 meV. σ_E = √(E_R ω̄).

| E_R | σ_E | **σ_E/E_R** | 2W | SC3 band | **verdict** | moment-corrected (×1.1639) | vs band |
|---|---|---|---|---|---|---|---|
| 100 meV | 42.261 meV | **42.261 %** | 5.599 | 35–46 % | **IN BAND** | 49.189 % | **ABOVE** |
| 0.5 eV | 94.498 meV | **18.900 %** | 27.996 | 15.5–20.5 % | **IN BAND** | 21.998 % | **ABOVE** |
| 1 eV | 133.640 meV | **13.364 %** | 55.992 | 11–15 % | **IN BAND** | 15.555 % | **ABOVE** |
| 10 eV | 422.607 meV | **4.226 %** | 559.92 | (none) | — | 4.919 % | — |
| 100 eV | 1.33640 eV | **1.336 %** | 5599.2 | 1.1–1.5 % | **IN BAND** | 1.555 % | **ABOVE** |

Every headline value was computed from the locked ω̄ by `ia_broadening.fractional_width`. **None was
transcribed** from `GPD/literature/`; the SC3 bands appear only as a comparison column.

**How much weight should the four IN BAND verdicts carry? Very little.** The bands were generated
from the survey's ω̄ = 12–21 meV, and plan 11-01's locked ω̄ = 17.86 meV sits inside that band. So
σ_E/E_R = √(ω̄/E_R) was *guaranteed* to land inside bands built from the same range. This is
**agreement by shared ancestry, not independent confirmation** — exactly the competing explanation
the plan's `uncertainty_markers` flagged. What is genuinely informative is the last column: with the
physically correct arithmetic mean, **every** width exceeds the upper edge of its band.

---

## 5. Quadrature with the Phase-10 counting floor at the 0.5 eV threshold

Both mechanisms act on the trigger sigmoid at the same energy, and only one of them was in the v1.0
model.

The Phase-10 counting floor is a **BEST CASE WITH NO NOISE SOURCES** — 1/√N_obs quasiparticle
counting statistics with no baseline, amplifier, phonon-collection, position or readout noise, and
this project has no resolution parameter at all. Calling it the detector resolution is the locked
forbidden proxy `fp-poisson-as-resolution`.

| Design | counting floor at 0.494 eV (**best case**) | IA width at 0.5 eV | **quadrature** | ROADMAP 22–26 % |
|---|---|---|---|---|
| Ta→Al | 16.009 % | 18.900 % | **24.769 %** | **IN BAND** |
| Al→Hf | 14.271 % | 18.900 % | **23.682 %** | **IN BAND** |

Floors are the Phase-10 **pipeline-derived** values, not the ROADMAP comparison targets 15.9 % /
14.2 %. Using the targets instead gives 24.698 % / 23.640 %, so the verdict does not hinge on the
choice.

**Added in quadrature, never linearly.** Linear sums would give 34.9 % / 33.2 %. Quadrature assumes
the two are statistically **independent**: quasiparticle counting statistics in the sensor versus
nuclear zero-point motion in the target lattice. They arise from unrelated physics, but the
independence is **asserted here, not proven**.

**Consequence.** At the 0.5 eV threshold the IA width is now the *larger* of the two contributions
(18.9 % against a best case floor of 16.0 %/14.3 %), so the best case counting floor alone
understates the combined smearing by 55 % / 66 % in quadrature terms. The IA width overtakes the
Ta→Al best case floor at **0.70 eV** and the Al→Hf best case floor at **0.88 eV** — both inside the
sub-eV regime, both below the 1.0 eV regime boundary. Since the floor is a best case, any real noise
source moves those crossings to *higher* energy, so they are lower bounds on where the IA width
dominates, not estimates.

With the moment correction the quadrature becomes 27.19 % (Ta→Al) and 26.20 % (Al→Hf), i.e. **both
above the ROADMAP band**. That is reported, not smoothed.

**What this comparison is not.** Neither number here, nor their quadrature sum, is a detector
resolution. The IA width is a real physical broadening of the recoil spectrum; the counting floor is
a best case statistical limit with no noise sources, computed from N_obs alone. Quoting the 24.8 % /
23.7 % quadrature as "the resolution at 0.5 eV" would be `fp-poisson-as-resolution`.

---

## 6. Giving "negligible above ~100 eV" a number

One extended-grid bin at 79.988714 bins/decade spans a fractional width

    10^(1/79.988714) − 1 = **2.92047 %**

Solving σ_E/E_R = 2.92047 % gives

    **E_R = ω̄ / (0.0292047)² = 20.940 eV**

Above ~21 eV the IA broadening is **sub-bin on the Phase-10 axis and cannot move counts between
bins**. That is the operational content of "negligible above ~100 eV" — and it is in fact
conservative by a factor of ~5: the true crossing is at 21 eV, not 100 eV. At 100 eV the width is
1.34 %, less than half a bin.

(With the moment correction, the crossing moves to 20.940 × 1.1639² = **28.37 eV** — still well
inside 10–100 eV.)

---

## 7. Scope boundary that this plan does not cross

σ_E = √(E_R ω̄) is a **NUCLEAR-recoil** width, on the unified phonon scale with no ionization
quenching (`CONVENTIONS.md` §B) — never keVee. The muon and Compton channels are **electron**
recoils. Whether this broadening applies to them is recorded as **OPEN and assigned to Phase 15** by
the project contract. This plan neither applies it there nor states that it does or does not apply
(`fp-electron-recoil-leak`, which is violated in *either* direction). `test_no_electron_recoil_leak`
enforces that `ia_broadening.py` does not import or touch the muon/Compton modules.

---

## 8. What would overturn these numbers

1. **σ_E inherits plan 11-01's ω̄ uncertainty linearly under a square root.** A factor-2 error in ω̄
   is a factor-1.41 error in every width here. The ω̄ lock rests on a single 1972 measurement.
2. **The Gaussian is only the leading IA result.** At 2W = 5.6 the O(1/2W) ≈ 18 % correction in the
   bottom bin is comparable to the width's own precision. Plan 11-03 must bound it; if it exceeds
   ~20 %, the 100 meV width should not be quoted to better than one significant figure.
3. **The independence assumption behind the quadrature is asserted, not proven.**
4. **The moment systematic is one-sided and already 16 %.** If plan 11-03's exact second moment of
   S(q,ω) disagrees with √(ω̄_p/ω̄_u) = 1.1639, that disagreement **blocks 11-04** — the two routes
   are supposed to be computing the same quantity by different means.

---

## 9. Files

| File | Role |
|---|---|
| `src/qpd_potential/ia_broadening.py` | σ_E, fractional width, moment diagnostics, quadrature |
| `tests/test_ia_broadening.py` | 12 checks incl. the Debye 9/8 oracle and the identity demonstration |
| `artifacts/v2.0/ia_broadening_widths.csv` | 749 rows: 5 ROADMAP energies + 744 extended-grid centres |
| `artifacts/v2.0/ia_width_vs_counting_floor.png` | widths, floors, one-bin line, crossing energies |
| `scripts/make_ia_width_table.py` | the generator |
