# 11-01 — Determination of the effective phonon energy ω̄ and the Debye–Waller convention

**Plan:** 11-01 (CALC-14) · **Deliverable:** `deliv-determination` · **Date:** 2026-07-22
**Reproduce every number below with:**

```bash
/opt/anaconda3/bin/python3 -c "import sys; sys.path.insert(0,'src'); \
  from qpd_potential import phonon_scale as ps; \
  print(ps.derive('ncrystal')); print(ps.derive('darkelf'))"
/opt/anaconda3/bin/python3 -m pytest tests/test_phonon_scale.py -q
```

---

## 0. The answer

| Quantity | Locked value | Where |
|---|---|---|
| ⟨u_x²⟩ (1-D MSD, T→0) | **1.6096194483 × 10⁻³ Å²** | `params.U_X_SQ_ANGSTROM2` |
| **ω̄ ≡ ħ²/(2 m_N ⟨u_x²⟩)** | **17.8597 meV** | `params.OMEGA_BAR_eV` |
| B = 8π²⟨u_x²⟩ | **0.1270905 Å²** | `params.DEBYE_WALLER_B_ANGSTROM2` |
| 2W = q²⟨u_x²⟩ at E_R = 100 meV | **5.5992** | derived |
| Debye–Waller convention | **2W = q²⟨u_x²⟩** (1-D); `q²⟨u²⟩/3` REJECTED | `CONVENTIONS.md` §J |
| Citation | Nelin & Nilsson, Phys. Rev. B **5**, 3151 (1972), via NCrystal 4.4.6 `Ge_sg227.ncmat` | frozen at `data/external/ge_vdos/` |

**ω̄ = 17.86 meV lands INSIDE the survey's 12–21 meV band.** The band survives contact with the
measured VDOS. That is a result, not a target that was aimed at — the anti-confirmation instruction
was live throughout, and §5 records what would have happened had it landed outside.

---

## 1. What the two candidate values physically ARE

This is the part that must not be overstated. The ambiguity CALC-14 closes is **largely a notation
collision**, and the phase should not be reported as having resolved a physics dispute.

| Candidate | What it actually is | Correct symbol |
|---|---|---|
| **≈37.79 meV** | The **top of the Ge phonon spectrum** — the zone-centre optical-phonon energy. It is the *ceiling* of the VDOS, a perfectly correct number for a completely different question. | ω_max, ω_LO(Γ) |
| **12–21 meV** | An **effective phonon energy defined through the mean-square displacement**, `ω̄ ≡ ħ²/(2 m_N ⟨u_x²⟩)`. | ω̄ |

`GPD/literature/SUMMARY.md` line 37 already says this: *"The only real disagreement is the label
ω̄."* Both numbers are correct measurements of the same spectrum; they answer different questions.
Presenting the choice below as a physics discovery would be false progress.

**Why the ⟨u²⟩-derived definition wins.** Not because 37 meV is wrong, but because only this
definition makes the two expressions the project actually needs *exact*:

* `2W = q²⟨u_x²⟩ = 2 m_N E_R ⟨u_x²⟩ = E_R/ω̄` — exact, by construction, once ω̄ ≡ ħ²/(2m_N⟨u_x²⟩).
* `σ_E = √(E_R ω̄)` — the impulse-approximation width, self-consistent with the same ω̄.

Substituting 37.79 meV into either of those would produce a number that is not the Debye–Waller
exponent of anything. The choice is a *definitional* one, forced by the downstream algebra.

---

## 2. Derivation, and the two normalization statements it depends on

VDOS normalization (stated, because the alternative differs by exactly the factor being guarded):

    ∫ g(ω) dω = 1

Harmonic-lattice mean-square displacement, temperature factor written out, not pre-reduced:

    ⟨u²⟩_3D(T) = (3ħ²/2m_N) ∫ [ g(ω)/ω · coth(ω/2k_BT) ] dω
    ⟨u_x²⟩     = ⟨u²⟩_3D / 3

The leading **3** counts the three Cartesian branches per atom and belongs with `∫g dω = 1`. If `g`
were instead normalized to 3, the leading 3 would have to go — that pair of choices is the single
most likely place for a silent factor-3 error, which is why both halves are written on the same
line here and in the MANIFEST.

For cubic Ge (spacegroup 227) the MSD tensor is isotropic, so **⟨u_x²⟩ = ⟨u²⟩/3 is EXACT by
symmetry**, not an approximation. It has therefore *already been applied* by the time ⟨u_x²⟩ exists.
Applying `/3` a **second** time inside 2W is the factor-3 trap, and it is rejected explicitly in
`CONVENTIONS.md` §J and guarded by `test_factor_three_trap_is_detectable_by_the_oracle`.

At T→0 (`coth → 1`, taken exactly):

    ω̄ = ħ²/(2 m_N ⟨u_x²⟩),   2W(E_R) = q²⟨u_x²⟩ with q = √(2 m_N E_R),   B = 8π²⟨u_x²⟩

### 2.1 Two consequences that change how the results should be read

**(a) ω̄ is the harmonic mean of the VDOS, and m_N cancels.**
With ⟨u_x²⟩ = (ħ²/2m_N)·I and I = ∫g/ω dω, we get ω̄ = 1/I and 2W = E_R·I. The nuclear mass drops
out of both. This is why the 0.10 % ambiguity in how natural-Ge mass is averaged (72.7053 u from
`params.GE_ISOTOPES` with M_i = A_i·931.494 MeV, vs 72.632249 u carried by the `.ncmat` file) moves
⟨u_x²⟩ and B by 0.10 % and moves ω̄ and 2W by **exactly zero**. Verified in
`test_omega_bar_is_mass_free` over a 2000× mass range.

**(b) The single-frequency form hides a moment mismatch — this is load-bearing for plan 11-02.**
⟨u_x²⟩ is governed by the **harmonic** mean ⟨1/ω⟩⁻¹; ⟨p_x²⟩, which sets the IA Gaussian width, is
governed by the **arithmetic** mean ⟨ω⟩. They coincide only for a single mode.

| Spectrum | harmonic mean | arithmetic mean | ⟨ω⟩⟨1/ω⟩ | √(⟨ω⟩⟨1/ω⟩) |
|---|---|---|---|---|
| Debye (analytic oracle) | 21.4859 meV | 24.1717 meV | **1.125000000** (= 9/8, exact) | 1.06066 |
| **Measured Ge (NCrystal)** | **17.8597 meV** | **24.1955 meV** | **1.354758** | **1.16394** |
| Measured Ge (DarkELF) | 18.2100 meV | 24.3373 meV | 1.336480 | 1.15606 |

So `σ_E = √(E_R ω̄)` built on the locked ω̄ **understates** the true IA width by 1.164× for real Ge —
worse than the Debye 1.061×, as expected for a spectrum with more low-frequency weight. Recorded in
`params.OMEGA_BAR_ARITHMETIC_eV`. Plan 11-02 must derive this from the VDOS moments and plan 11-03
must reproduce it independently from the second central moment of S(q,ω); **disagreement between
those two routes blocks 11-04.**

---

## 3. The oracle gate — run first, before any Ge number was quoted

Analytic Debye VDOS `g(ω) = 3ω²/ω_D³` on `[0, ω_D]`, ħω_D = k_Bθ_D, θ_D = 374 K, T→0. One line:

    (3ħ²/2m)∫₀^{ω_D}(3ω²/ω_D³)/ω dω = (3ħ²/2m)(3/2ω_D) = 9ħ²/(4 m ω_D) = 9ħ²/(4 m k_Bθ_D)

| Check | Result | Tolerance | Verdict |
|---|---|---|---|
| Quadrature vs closed form, ⟨u²⟩_3D | rel. error **3.75 × 10⁻¹¹** | < 1e-3 | **PASS** |
| ⟨u_x²⟩ = ⟨u²⟩_3D/3 | difference **exactly 0.0** | machine precision | **PASS** |
| Re-derived ⟨u²⟩_3D | **4.0139 × 10⁻³ Å²** | — | matches the 4.02e-3 baseline |
| Re-derived ⟨u_x²⟩ | **1.3380 × 10⁻³ Å²** | — | matches the 1.34e-3 baseline |
| Debye mean-ratio oracle ⟨ω⟩⟨1/ω⟩ | **1.124999999972** | = 9/8 | **PASS** |

Neither Debye number was pasted; both are computed from the closed form in
`phonon_scale.debye_msd_3d_closed_form` and cross-checked by the quadrature. This gate is
independent of every Ge data file and of every project-internal prior estimate.

---

## 4. What the two sources gave

Both were obtained. Neither was averaged.

| | **NCrystal `Ge_sg227.ncmat`** (adopted) | **DarkELF `Ge_pDoS.dat`** (cross-check) |
|---|---|---|
| Grid | 425 uniform points, spacing 0.08023 meV | 299 uniform points (E>0), spacing 0.12611 meV |
| Support ceiling | **37.78966 meV** | **37.70769 meV** |
| Low-energy handling | measured table starts at 3.77094 meV; NCrystal's own parabolic `g ∝ ω²` segment below it, carried explicitly | table reaches E = 0; **no support at all below 2.39614 meV** |
| ⟨u_x²⟩ (T→0) | **1.609619 × 10⁻³ Å²** | 1.578654 × 10⁻³ Å² |
| ω̄ | **17.8597 meV** | 18.2100 meV |
| B | **0.127090 Å²** | 0.124646 Å² |

**Cross-source agreement: −1.92 % on ⟨u_x²⟩, +1.96 % on ω̄.** Requirement was 10 %. **PASS.**
The two ceilings differ by 0.082 meV, i.e. **inside one DarkELF grid spacing** (0.126 meV).

**Which carries the headline, and why.** NCrystal. Three reasons, all from the data:

1. It is the finer digitization (0.080 vs 0.126 meV) of the same 1972 measurement.
2. Its low-energy behaviour is physical: the acoustic branches continue to ω = 0 as ω², and
   NCrystal supplies that segment. DarkELF's digitization simply stops at 2.396 meV. Since ⟨u_x²⟩
   weights by 1/ω, a truncated low-energy tail biases it **low** — which is exactly the sign and
   roughly the size of the observed −1.9 % discrepancy. The disagreement is therefore *explained*,
   not merely tolerated.
3. NCrystal exposes the underlying measurement citation directly; DarkELF's table is a
   redigitization at one remove.

**The −1.9 % is reported, not averaged.** Averaging would manufacture a value neither source
supports and would hide the explanation in (2).

### 4.1 An unplanned but decisive check: cross-implementation against NCrystal's own MSD

NCrystal computes this same integral internally. At its reference temperature 293.6 K,
`DI_VDOS.analyseVDOS()['msd'] = 6.931414998755903 × 10⁻³ Å²`. This module, run at NCrystal's own
atomic mass, gives **6.931278618 × 10⁻³ Å² — a relative difference of 1.97 × 10⁻⁵.**

This was not in the plan and it is the strongest check in the phase after the analytic oracle,
because it simultaneously validates three things that no other check separates:

* the `∫g dω = 1` normalization,
* **the factor of 3** — NCrystal's `msd` is the *1-D* MSD, so the agreement confirms that
  `⟨u_x²⟩ = ⟨u²⟩_3D/3` is what NCrystal means too, which is precisely the quantity that enters 2W,
* the parabolic low-energy segment. Dropping it moves this number by **8.5 %** (6.34293e-3 instead
  of 6.93128e-3), far outside the agreement — so the segment is not a cosmetic choice.

Independently, NCrystal's reported spectral integral exceeds the trapezoid integral of its
tabulated points by 8.0718 × 10⁻⁶, matching `density[0]·egrid[0]/3 = 8.071842 × 10⁻⁶` to 1.5 × 10⁻⁸
— i.e. the parabolic convention is *measured* from the library, not assumed. Recorded in
`data/external/ge_vdos/MANIFEST.md` §3.1.

---

## 5. Where the number sits, clause by clause

### ROADMAP Phase 11 SC1 — one number, one convention, one citation

| Clause | Verdict |
|---|---|
| ω̄ and ⟨u_x²⟩ pinned from the **real Ge VDOS**, not the Debye model | **PASS** — `fp-debye-substitute` avoided; the Debye value appears only as an oracle input and a comparison baseline |
| `2W = q²⟨u_x²⟩` locked | **PASS** — `CONVENTIONS.md` §J |
| `q²⟨u²⟩/3` explicitly rejected | **PASS** — appears once, labelled REJECTED, with the reason; guarded by a test |
| `B = 8π²⟨u_x²⟩` quoted alongside | **PASS** — 0.12709 Å² |
| One number / one convention / one citation, no range | **PASS** — `test_single_value_lock` parses §J and rejects a range on any LOCKED line |

### ROADMAP Phase 11 SC2 — acceptance signals

| Clause | Target | Measured | Verdict |
|---|---|---|---|
| VDOS reproduces the measured ceiling | 37.79 meV | **37.78966 meV** (NCrystal); 37.70769 meV (DarkELF, within its own grid spacing) | **PASS** |
| VDOS-integral ⟨u_x²⟩ vs Debye value, within ~1.5× | 1.3380e-3 Å² | **1.6096e-3 Å², ratio 1.2030** | **PASS** |
| 2W at 100 meV lands in 4.7–8.3 | [4.7, 8.3] | **5.5992** | **PASS** |
| consistent with q(100 meV) = 116 keV/c = 58.9 Å⁻¹ | — | **116.383 keV/c = 58.980 Å⁻¹** | **PASS as a UNITS CHECK — see below** |

**The fourth clause is not independent evidence and is not reported as such.** With `q² = 2m_N E_R`
and `ω̄ ≡ ħ²/(2m_N⟨u_x²⟩)`, `2W = q²⟨u_x²⟩` and `2W = E_R/ω̄` are the *same expression*; the code
confirms they agree to 1 part in 10¹⁴, which is a statement about arithmetic, not about germanium.
Locked as forbidden proxy `fp-q-route-as-independent`. Equally, `2W ∈ [4.76, 8.33]` ⟺
`ω̄ ∈ [12.0, 21.0] meV` **exactly**, so SC2's third clause is not independent of SC1's ω̄ either.

**The genuinely independent legs of SC2 are two:** the measured ceiling (37.79 meV) and the
VDOS-vs-Debye ⟨u_x²⟩ comparison. Both pass. §4.1 adds a third that the plan did not anticipate.

### The survey band

| | |
|---|---|
| Survey band (`PRIOR-WORK.md`, marked DERIVED in-survey, MED confidence) | 12–21 meV |
| SC2's ~1.5× ⟨u_x²⟩ tolerance mapped to ω̄ | [14.3, 32.2] meV — **wider** than the survey band |
| **Measured-VDOS result** | **17.860 meV** |
| Verdict | **INSIDE both.** The survey band **SURVIVES** and is not superseded. |

The Debye-model ω̄ for the same mass and θ_D = 374 K is **21.486 meV**, i.e. essentially the top of
the survey band — which identifies where the survey's upper end came from. The measured spectrum
gives a *lower* ω̄ than Debye because real Ge carries more weight in the flat low-lying transverse
acoustic branches than a Debye ω² density does, and ⟨u_x²⟩ weights by 1/ω.

**What was pre-committed:** had ω̄ landed outside 12–21 meV, the measured value would have been
reported and the survey band marked superseded. No tuning of the quadrature, normalization,
temperature or mass toward the band was performed or would have been. Landing inside was a live
outcome, not a foregone one — SC2's own tolerance is the wider window.

---

## 6. Temperature: the T→0 reduction, measured rather than asserted

| T | ⟨u_x²⟩ (Å²) | ratio to T→0 | B (Å²) |
|---|---|---|---|
| **T → 0 (locked)** | **1.60961946e-3** | 1 (exact) | **0.12709** |
| 10 mK (operating point) | 1.60961946e-3 | **1.000000005** | 0.12709 |
| 293.6 K | 6.92431513e-3 | 4.3018 | 0.54672 |
| 300 K | 7.06736266e-3 | 4.3907 | 0.55802 |

At 10 mK the full `coth` form and the exact limit differ by **5 × 10⁻⁹** relative — nine orders of
magnitude below any tolerance in this phase. The T→0 lock is therefore justified by evaluation, not
by assertion. `thermal_factor(ω, None)` returns exactly 1.0, so the lock does not depend on a chosen
"small enough" temperature either.

The 300 K row matters for a different reason: it is **4.4× the locked value**, and it is the regime
in which room-temperature diffraction B factors — the anchor behind the survey band's other end —
are measured. A room-temperature B factor and the locked zero-point B are **not the same quantity**,
which is a large part of why the survey band was a factor of ~2 wide.

---

## 7. Derived 2W and q across the window

| E_R | q (keV/c) | q (Å⁻¹) | 2W = q²⟨u_x²⟩ | 2W = E_R/ω̄ | agreement |
|---|---|---|---|---|---|
| 100 meV | 116.383 | 58.980 | 5.599205 | 5.599205 | 3e-16 |
| 0.5 eV | 260.239 | 131.882 | 27.99603 | 27.99603 | 0 |
| 1 eV | 368.034 | 186.510 | 55.99205 | 55.99205 | 0 |
| 10 eV | 1163.83 | 589.796 | 559.9205 | 559.9205 | 2e-16 |
| 100 eV | 3680.34 | 1865.10 | 5599.205 | 5599.205 | 2e-16 |

2W ≫ 1 everywhere in the window, which is the impulse-approximation condition. Correspondingly
`exp(−2W)` ≈ 3.7 × 10⁻³ at 100 meV and ≈ 5 × 10⁻²⁵ at 1 eV: **the coherent channel is extinct.**
That is evidence that the strength has moved into the multiphonon continuum, **not** a rate
suppression. The rate is never multiplied by `exp(−2W)`.

---

## 8. Residual uncertainty and what would change the answer

**Weakest anchors.**
1. Everything rests on a **single 1972 inelastic-neutron measurement** (Nelin & Nilsson). The two
   available digitizations of it agree to 1.9 %, which bounds digitization error but not
   measurement error. No independent modern Ge VDOS was obtained.
2. The **harmonic-lattice assumption**. At mK the displacement is zero-point dominated, which is
   the most favourable case, but anharmonic corrections are not quantified here.
3. The low-energy segment. The NCrystal parabolic extension contributes **+1.21 %** to ⟨u_x²⟩ at
   T→0 (1.59198e-3 without it vs 1.61124e-3 with, at NCrystal's mass). Its presence is verified
   from NCrystal's own integral, but the ω² form below 3.77 meV is a model, not data.

**Unvalidated assumptions.** That a symmetric Gaussian is adequate at 2W ≈ 5.6 — that is SC5's job
(plan 11-04), not this plan's. That the T→0 reduction is exact enough at mK — this one is now
*validated*, at 5e-9 (§6), rather than assumed.

**Competing explanation, kept on the record.** The 37 meV optical-phonon value is not wrong; it is
a different quantity wearing the same symbol. This plan resolved a **notation collision** and made a
**definitional choice forced by downstream algebra**. It did not discover new physics about
germanium, and it should not be written up as though it had.

**What would overturn the lock.** A modern measured Ge VDOS disagreeing with Nelin & Nilsson by more
than ~10 % in its 1/ω moment; or a demonstration that anharmonicity at mK shifts ⟨u_x²⟩ by more than
the 1.5× SC2 window. Neither is in scope for this milestone.

---

## 9. Files

| File | Role |
|---|---|
| `data/external/ge_vdos/MANIFEST.md` | SHA-256, retrieval commands, normalization convention, integrity checks |
| `data/external/ge_vdos/Ge_sg227_vdos_raw.csv` | NCrystal VDOS, unnormalized, as reported |
| `data/external/ge_vdos/ge_vdos_normalized.csv` | headline normalized table, ∫g dω = 1 |
| `data/external/ge_vdos/Ge_pDoS.dat` | DarkELF table, byte-for-byte as fetched |
| `data/external/ge_vdos/ge_vdos_darkelf_normalized.csv` | DarkELF under the same convention |
| `scripts/freeze_ge_vdos.py` | the generator, committed with the data |
| `src/qpd_potential/phonon_scale.py` | quadrature, oracles, derived scales |
| `src/qpd_potential/params.py` | the locked scalars |
| `tests/test_phonon_scale.py` | 23 checks incl. both analytic oracles and the §J parser |
| `GPD/CONVENTIONS.md` §J | the lock |
