# Ge vibrational density of states — provenance manifest

**Deliverable:** `deliv-vdos-frozen` (Plan 11-01, Task 1)
**Phase:** 11 — Phonon-Scale Conventions and IA Quantum Broadening (P-CONV)
**Frozen:** 2026-07-22 (UTC)
**Host:** macOS 26.3 (Darwin, osx-arm64) · Python 3.11.7 (`/opt/anaconda3/bin/python3`) ·
NumPy 1.26.4 · NCrystal 4.4.6 · curl 8.16.0 (OpenSSL/3.0.18)

**Why this cache exists.** CALC-14 pins the project's single effective phonon energy `ω̄` from the
**measured** Ge VDOS, not from the Debye model. Freezing raw + normalized tables with hashes means
every derived number (`⟨u_x²⟩`, `ω̄`, `B`, `2W`) stays reproducible after the phase ends, with no
NCrystal install required. `WebFetch` is not a quote source in this project; every number below
comes from a file that was downloaded or written locally and hashed, or from a command recorded here.

---

## 1. Artifact table

Working directory for every command: repository root.

| # | Artifact | Retrieval / generation command | Bytes | SHA-256 |
|---|---|---|---|---|
| 1 | `Ge_pDoS.dat` | `curl -sS -o data/external/ge_vdos/Ge_pDoS.dat https://raw.githubusercontent.com/tongylin/DarkELF/main/data/Ge/Ge_pDoS.dat` (HTTP 200) | 15017 | `39df1cb32f6b7bfee41b0210b20e8477b0810277fd64ec17ecb2d05586bbe5fb` |
| 2 | `Ge_sg227_vdos_raw.csv` | `/opt/anaconda3/bin/python3 scripts/freeze_ge_vdos.py` | 19292 | `c8e6d23981fd97a1af123e08e6fb52e75264d25e82c64016e69cc3c92d80040d` |
| 3 | `ge_vdos_normalized.csv` | `/opt/anaconda3/bin/python3 scripts/freeze_ge_vdos.py` | 54570 | `4ed0b3d458ba619d3c23db73f1da9b0da2e319215e6ffae225d594a2244828fc` |
| 4 | `ge_vdos_darkelf_normalized.csv` | `/opt/anaconda3/bin/python3 scripts/freeze_ge_vdos.py` | 13732 | `2b813de6ecb908d0e9cfb7aeb5f3da8b8c77df9082346829dbf25dc5c52b8d0a` |

Re-verify with:

```bash
shasum -a 256 data/external/ge_vdos/*
```

`scripts/freeze_ge_vdos.py` is the generator and is committed alongside the data.

---

## 2. Sources and citations

**Primary — NCrystal `Ge_sg227.ncmat`.** NCrystal 4.4.6 (Apache-2.0), installed into
`/opt/anaconda3` from the native osx-arm64 wheel; no build step. Extraction:

```python
import NCrystal as NC
info = NC.createInfo("Ge_sg227.ncmat;temp=293.6K")
di   = info.dyninfos[0]           # DI_VDOS, fraction 1.0, Ge, mass 72.632248855 amu
egrid   = di.vdos_egrid_expanded  # 425 uniform points, 3.7709431308882e-3 .. 3.778966414145409e-2 eV
density = di.vdos_density         # 425 values, NCrystal-internal arbitrary units
```

Underlying measurement: **G. Nelin and G. Nilsson, Phys. Rev. B 5, 3151 (1972)**,
DOI `10.1103/PhysRevB.5.3151` — inelastic-neutron-scattering Ge phonon dispersion, from which the
`.ncmat` VDOS is built. This is the citation carried into `CONVENTIONS.md` Section J.

**Cross-check — DarkELF `data/Ge/Ge_pDoS.dat`.** `github.com/tongylin/DarkELF`, branch `main`
(arXiv:2104.12786; Phys. Rev. D 105, 015014). Header line is `# eV, DoS`; 300 rows, uniform spacing
1.261126798250630e-4 eV, first column energy in eV, second column DOS already normalized
(raw trapezoid integral = 1.0020085985896547).

Note the retrieval path: the file lives at `data/Ge/Ge_pDoS.dat` in the repository root, **not**
under a `darkelf/` package directory, and the branch is `main`. The obvious
`.../DarkELF/master/darkelf/data/Ge/Ge_pDoS.dat` URL returns HTTP 404. There is no `darkelf`
package on PyPI; only the single data file is needed and no import is performed.

---

## 3. Normalization convention — stated, and what changed

The normalization used everywhere downstream is

    ∫ g(ω) dω = 1        over the full support,  ω in meV,  g in 1/meV

so that the mean-square-displacement quadrature reads
`⟨u²⟩_3D = (3ħ²/2m_N) ∫ (g(ω)/ω) coth(ω/2k_BT) dω` with a **3**, and
`⟨u_x²⟩ = ⟨u²⟩_3D/3`. If instead `g` were normalized to 3 (one unit per Cartesian branch), the
leading 3 would have to be dropped. The two conventions differ by exactly the factor this phase is
guarding against, which is why the normalization is stated here rather than left implicit.

### 3.1 What the raw NCrystal density integrated to before renormalization

| Quantity | Value |
|---|---|
| Trapezoid integral of the 425 tabulated points, `∫ density dE` | `4.1220017201149374e-3` eV·(arb) |
| NCrystal's own `DI_VDOS.analyseVDOS()['integral']` | `4.130073562154515e-3` eV·(arb) |
| Difference | `8.0718e-6` eV·(arb) |
| `density[0] * egrid[0] / 3` (analytic integral of `density[0]·(E/egrid[0])²` over `[0, egrid[0]]`) | `8.071842039580992e-6` eV·(arb) |

The last two agree to `1.5e-8` relative. **This is a measured fact, not an assumption:** NCrystal
treats the VDOS as parabolic, `g ∝ E²`, below its first grid point, and its reported integral
includes that segment. The normalized table therefore carries the parabolic segment explicitly
rather than silently dropping it.

Renormalization factor actually applied to the raw NCrystal density:
divide by **`4.1300745840333825e-3`** eV·(arb) (the trapezoid integral of raw grid + discretized
parabolic segment), then multiply by `1e-3` to convert `1/eV` → `1/meV`. The residual `2.5e-7`
relative gap between this factor and NCrystal's `analyseVDOS` integral is trapezoid discretization
of the parabola on a log grid; it is far below every tolerance in this phase.

### 3.2 Grid of `ge_vdos_normalized.csv`

* Rows 1–800: log-spaced (`numpy.geomspace`) from `1e-12` eV to `egrid[0]`, endpoint excluded,
  carrying `g = g(ω₁)·(ω/ω₁)²`. The omitted `[0, 1e-12]` eV slab contributes `< 1e-12` relative to
  any integral used in this phase.
* Rows 801–1225: the NCrystal grid verbatim (425 uniform points, spacing `8.023283257e-5` eV).

Why a log grid: at `T = 10` mK the thermal factor `coth(ω/2k_BT)` only departs from 1 for
`ω ≲ k_BT ≈ 8.6e-7` eV, three decades below the first NCrystal grid point. A linear sub-grid would
not resolve that region, and the resulting `T → 0` claim would be untested rather than tested.
Convergence was checked at (800 points, `1e-12` eV) against (1600, `1e-12`) and (400, `1e-9`):
`⟨u_x²⟩(T→0)` moves by `< 2e-7` relative.

### 3.3 Grid of `ge_vdos_darkelf_normalized.csv`

The DarkELF table already starts at `E = 0`, so **no parabolic segment is prepended**. The `E = 0`
row is dropped (`g` is identically zero there and `g/E` would be `0/0`). The digitization carries
no support at all below **2.396140916676198 meV** (first non-zero row), which is one of the two
reasons its `⟨u_x²⟩` sits ≈1.9 % below the NCrystal value; the other is the coarser 0.1261 meV grid.

---

## 4. Integrity checks performed at freeze time

| Check | Expected | Measured | Verdict |
|---|---|---|---|
| NCrystal VDOS ceiling | 37.79 meV (Nelin & Nilsson spectrum) | **37.78966414145409 meV** | PASS |
| DarkELF ceiling (last non-zero row) | same spectrum, coarser digitization | **37.707691267693855 meV** | PASS — 0.082 meV below NCrystal, i.e. **within one DarkELF grid spacing** (0.1261 meV) |
| NCrystal low-energy edge | ~3.77 meV | **3.7709431308882 meV** | PASS — sets `k_BT/ħω_min = 2.3e-4` at 10 mK, which is why `coth → 1` |
| Normalized table integrates to 1 | 1 | `1.0000000000` (trapezoid, both files) | PASS |
| Ge atomic mass carried by the ncmat | natural abundance-weighted | **72.632248855 amu** (vs `params.GE_MOLAR_MASS = 72.63 g/mol`) | PASS |
| NCrystal `analyseVDOS()['debye_temp']` | — | **295.3477089328913 K** | recorded; see note |

**Note on `debye_temp = 295 K`.** NCrystal's VDOS-derived Debye temperature is *not* the
`θ_D = 374 K` used as the analytic-oracle baseline. They are different estimators (NCrystal fits a
Debye model to the VDOS second moment; 374 K is the low-temperature specific-heat value). The 374 K
number is used **only** as an input to the analytic closed-form oracle
`⟨u²⟩_3D = 9ħ²/(4 m_N k_Bθ_D)`, which is a test of the quadrature, never a source of the locked
`ω̄`. Substituting the Debye model for the measured VDOS is forbidden proxy `fp-debye-substitute`.

---

## 5. Disposition register

`ge_vdos_normalized.csv` and `ge_vdos_darkelf_normalized.csv` are tracked `.csv` files and therefore
appear in the Phase-10 closure enumeration `git ls-files | grep -E '\.(csv|npz)$'`. Both carry a row
in `artifacts/v2.0/legacy_grid_disposition.csv` with disposition `not_a_spectrum`: a VDOS is an input
on a phonon-energy abscissa, not a spectrum on the shared deposited-energy axis, so no re-gridding
operation applies to it. `Ge_sg227_vdos_raw.csv` likewise. `Ge_pDoS.dat` is not a `.csv`/`.npz` and
is not enumerated.
