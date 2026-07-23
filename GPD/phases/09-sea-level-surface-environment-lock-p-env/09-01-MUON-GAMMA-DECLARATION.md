# Muon and Environmental-Gamma Surface-Environment Declaration (v2.0)

**Phase:** 09 — Sea-Level Surface Environment Lock (P-ENV)
**Plan:** 09-01, Tasks 1–2 (`deliv-mu-gamma-declaration`)
**Requirement:** ROADMAP Phase 9 **SC1** — the v1.0 muon and gamma inputs are re-declared
**numerically identical** to their committed values, *verified by direct comparison against the
frozen v1.0 artifacts rather than by assertion*.
**Scenario:** unshielded surface wafer, sea level, **zero overburden**, 3 GW_th at 25 m
(`GPD/CONVENTIONS.md` §D, unchanged). Veto credit is exactly **1.0 by construction** — there is
no veto in this configuration.
**Energy scale:** single unified phonon scale, **no ionization quenching**, no keVee/keVnr
mixing (`CONVENTIONS.md` §B). Both channels are **electron** recoils.

**Executed:** 2026-07-22. Repo HEAD at execution: `72011f2`.
Environment: Darwin 25.3.0 (arm64) · Python 3.11.7 · numpy 1.26.4 · pandas 1.5.3 · scipy 1.17.1.
Every number below was **parsed from a committed file or recomputed by committed code** using the
command printed next to it. **WebFetch and any LLM page summarizer were not used as a quote
source anywhere in this declaration** (Phase-8 lesson: a summarizer produced two verified factual
errors on sources that were correct and accessible).

---

## 0. Binding path correction (`fp-wrong-muon-path`)

`GPD/phases/04-muon-compton-deposited-energy-spectra/04-01-SUMMARY.md` front-matter names
`src/muon/deposited_spectrum.py` and `data/muon/muon_dep_spectrum.csv`. **Neither exists.**
Confirmed on disk:

```console
$ ls -d src/muon 2>&1; ls -d data/muon 2>&1
ls: src/muon: No such file or directory
ls: data/muon: No such file or directory

$ ls src/muon/deposited_spectrum.py 2>&1; ls data/muon/muon_dep_spectrum.csv 2>&1
ls: src/muon/deposited_spectrum.py: No such file or directory
ls: data/muon/muon_dep_spectrum.csv: No such file or directory
```

Those paths are **not cited** anywhere in this declaration. The real artifacts of record are
`data/muon_dRdEdep.csv`, `src/qpd_potential/muon_deposit.py` and `src/qpd_potential/muon_flux.py`.
Consequence recorded for downstream consumers: **the Phase-4 summary layer is not a trustworthy
provenance source without a filesystem check.**

---

## 1. Artifact identity

Recorded by:

```console
$ shasum -a 256 data/muon_dRdEdep.csv data/compton_dRdEdep.csv data/gamma_lines.csv \
                data/ge_incoherent_S.csv data/ge_xcom_mu.csv \
                src/qpd_potential/muon_deposit.py src/qpd_potential/muon_flux.py \
                src/qpd_potential/compton_source.py src/qpd_potential/compton_deposit.py
$ wc -c <same file list>
$ git status --porcelain -- <same file list>
```

| # | Channel | Artifact | Bytes | SHA-256 | `git status --porcelain` |
|---|---------|----------|-------|---------|--------------------------|
| 1 | muon | `data/muon_dRdEdep.csv` | 23972 | `677080a6db980e538b71d2895ef41e9bdab3f0d6ea860e854f8830b03baa347a` | *(empty — unmodified)* |
| 2 | muon | `src/qpd_potential/muon_deposit.py` | 17154 | `f035dbdb39b7d1bc64a6171281de5fd271784b756bb9dce8fc128f3d1d50dce9` | *(empty — unmodified)* |
| 3 | muon | `src/qpd_potential/muon_flux.py` | 3542 | `d7c71b08a60e9a982c16c37b158b4d55dc4e060a1b0ba97af916a42e29d7e56d` | *(empty — unmodified)* |
| 4 | gamma | `data/compton_dRdEdep.csv` | 24821 | `54e8144b7997bf8b8dc3acb8b30cc11812a1ff7094fb233ba93178ad6a3b58eb` | *(empty — unmodified)* |
| 5 | gamma | `data/gamma_lines.csv` | 4237 | `9e6f79913cbf3032f7d7a94b574e98d2b70b71d8f2b338ba48e237aba25ca50b` | *(empty — unmodified)* |
| 6 | gamma | `data/ge_incoherent_S.csv` | 5668 | `edd1d9592f97f155d507eb8539857e5c03b664b325e77b785799ca655cb53f4c` | *(empty — unmodified)* |
| 7 | gamma | `data/ge_xcom_mu.csv` | 1002 | `3e811088a2b86d6d0f7f37e5fa753e64e156468b9352d04f0d461f8443f10bcc` | *(empty — unmodified)* |
| 8 | gamma | `src/qpd_potential/compton_source.py` | 11418 | `fbf8fb1ec98159071fdcfa6f0a02ef22bb9e95ddda10d310d5c197490a3c157b` | *(empty — unmodified)* |
| 9 | gamma | `src/qpd_potential/compton_deposit.py` | 13947 | `9afc55d85a6edf79a97d76b498732bd48d68e632d5af3ff5566ea78d7a5a2b3e` | *(empty — unmodified)* |

Every SHA-256 above is the hash of the file **as committed at git HEAD `72011f2`**
(`git show HEAD:<path> | shasum -a 256`), which is the definition of the frozen v1.0 artifact.
`git status --porcelain` returned **empty output** for all nine paths at the time the table was
built. **Neither Monte Carlo was re-run and no `data/` file was written by Plan 09-01**
(`fp-mc-rerun-drift`); `git status --porcelain -- data/` stayed clean for the whole plan.

**Concurrency note (recorded, not smoothed over).** Phase 10 (`10-sub-ev-grid-extension...`,
Plan 10-01) executes in parallel **in this same working tree** and, at 21:16–21:18 local on
2026-07-22, added `src/qpd_potential/interp_guard.py` and an uncommitted interpolation-domain
guard to `src/qpd_potential/compton_source.py` (working-tree SHA-256 `c784ec9d…`, HEAD blob
`fbf8fb1e…`). Consequences, checked rather than assumed:
(i) the artifact of record for SC1 is the **HEAD blob**, and its hash is what this table quotes;
(ii) the gamma channel's declared numbers are **unchanged** under that edit — re-evaluated on the
modified working-tree module, ℓ̄ = 0.38484848 cm, μℓ̄(1 MeV) = 0.1173818, double-scatter
= 0.01377849, E_edge(²⁰⁸Tl) = 2381.7571 keV, all bit-identical to the values recorded below;
(iii) Plan 09-01 committed **none** of Phase 10's files. `tests/test_env_v1_identity.py` therefore
verifies the declared hashes against `git show HEAD:<path>` rather than against the shared
checkout, so it remains a genuine identity check on the frozen input without locking a working
tree that another phase legitimately owns part of.

---

## 2. Muon channel

### 2.1 Committed scalars — parsed, not typed

| Quantity | Value | Units | Extraction command |
|---|---|---|---|
| `integral_muon_rate_Hz` | **1.3659 ± 0.0003** | Hz (through-wafer, absolute) | `grep '^# integral_muon_rate_Hz' data/muon_dRdEdep.csv` → `# integral_muon_rate_Hz = 1.3659 +/- 0.0003` |
| first tabulated `E_dep_keV` | **1.014497e-02** | keV | `sed -n '10p' data/muon_dRdEdep.csv` → `1.014497e-02,1.601101e+01,7.605844e+00` |
| `vertical_chord_MPV_MeV` | **1.2323** (mean 1.4585) | MeV | `grep '^# vertical_chord_MPV_MeV' data/muon_dRdEdep.csv` |
| MC samples | 1e9, fixed seed | — | header line `# n_mc_samples = 1000000000; seed fixed for reproducibility` |

**Grid-floor clarification (recorded correction, not a change of value).** The plan calls
`1.014497e-02` keV the "first grid edge". It is in fact the **first log-bin *centre*** of the
project grid: `shared_energy_grid()` returns *edges* starting at exactly `1.000000e-02` keV
(585 edges, 584 bins, 0.01 keV → 2e5 keV, 80 bins/decade), and
`sqrt(edges[0]*edges[1]) = 1.014497e-02` keV. The committed table's `E_dep_keV` column is the
bin-centre column and matches `sqrt(edges[:-1]*edges[1:])` to `rtol = 1e-6` over all 584 rows
(verified in `tests/test_env_v1_identity.py::test_muon_grid_floor_matches_shared_grid`). The
frozen table is therefore **on-grid**; only the wording "edge" was imprecise.

### 2.2 Physics chain (matches `paper/sections/backgrounds.tex` §"Cosmic muons")

Sea-level muon intensity is sampled from the **modified-Gaisser ("Gaisser–Guan")**
parametrization with the effective zenith angle cos θ\*
(P1–P5 = 0.102573, −0.068287, 0.958633, 0.0407253, 0.817285), which supplies the
low-energy/large-angle correction plain Gaisser lacks. Each muon traverses a chord ℓ fixed by the
**ray–box intersection** with the 10.16 × 10.16 × 0.20 cm slab (0.20 cm vertical thickness to the
14.37 cm space diagonal), sampled with the **inward surface projection** measure
I(θ)·A_proj·sin θ — not a bare cos²θ. The per-chord deposit is drawn from the
**Landau–Vavilov** density whose **mode is the most-probable value Δ_p**, computed in code from
the PDG formula with mass thickness x = ρℓ [g cm⁻²]. **The mean deposit ⟨Δ⟩ = ⟨dE/dx⟩·x is NOT
used, and the Moyal approximation is NOT used** — either would misplace the peak and suppress the
high-deposit tail. Rare near-horizontal chords reach ~197 MeV; that tail, not the ~MeV bulk, is
the Phase-5 saturation driver.

### 2.3 Independent re-derivation of the deterministic scalars

These are closed-form quantities; recomputing them exercises the committed **code**, not just the
CSV. Command:

```console
$ PYTHONPATH=src python -c "
import numpy as np
from qpd_potential import muon_deposit as md, wafer_geometry as g
ell=g.cauchy_mean_chord(); x=md.RHO*g.CHORD_VERTICAL; bg=md.beta_gamma(np.array([4.0]))
dp,xi=md.mpv_deposit(np.array([x]),bg); print(ell, xi[0], dp[0], md.DEDX_MEAN*x, md.kappa(np.array([x]),bg)[0])"
```

| Scalar | Recomputed from committed module | Committed / paper value | Signed deviation | Tolerance | Verdict |
|---|---|---|---|---|---|
| ⟨ℓ⟩ = 4V/S (Cauchy mean chord) | **0.384848 cm** | 0.385 cm | **−0.039 %** | 0.1 % | **PASS** |
| x_vert = ρ·L_z (mass thickness) | **1.064600 g cm⁻²** | 1.065 g cm⁻² | −0.038 % | — | PASS |
| ξ (vertical chord, βγ at E_μ = 4 GeV) | **0.072069 MeV** | 0.0721 MeV | **−0.043 %** | 0.5 % | **PASS** |
| Δ_p (vertical chord) | **1.230614 MeV** | 1.2323 MeV | **−0.137 %** | 0.5 % | **PASS** |
| ⟨Δ⟩ = ⟨dE/dx⟩·x | **1.458502 MeV** | 1.4585 MeV | **+0.000 %** | — | PASS |
| Ordering Δ_p < ⟨Δ⟩ | 1.230614 < 1.458502 | required strictly | — | strict | **PASS** |
| κ = ξ/T_max (Vavilov regime) | **6.727e-05** | < 0.07 required | — | — | **PASS** (deep Landau) |

The Δ_p and ξ residuals are **rounding-level** (the committed header carries 4–5 significant
figures of a value evaluated at a representative βγ), not a code/artifact disagreement: the
benign reading and the adverse reading of §"competing explanations" are distinguished by the fact
that the *code path itself* was executed here and reproduces every scalar inside its stated
tolerance. **Δ_p < ⟨Δ⟩ holds strictly**, so the MPV has not been silently replaced by the mean or
by a Moyal approximation.

### 2.4 Scenario statement — zero overburden

Sea level, **overburden = 0 m.w.e. exactly**, no shield, no building. The NUCLEUS Very-Near-Site
overburden of 2.92 m.w.e. and its omnidirectional attenuation factor of 1.41 are **NOT applied and are not applicable to this configuration** (Phase-8 geometry gate: NO FIT, shielded premise voided).
No numeric factor other than exactly **1.0** multiplies this channel's normalization.
See §4 for the executed scan that proves it.

### 2.5 Accuracy, **with direction** (`claim-accuracy-direction`)

The v1.0 treatment claims agreement with the PDG sea-level expectation to **within ~20 %**, inside
the VALD-02 tolerance of 30 %, with the **30–35 % inter-experiment Gaisser–Guan normalization
spread** named in the paper itself as the weakest anchor of an otherwise textbook-grade channel.

Anchor arithmetic, computed here rather than quoted (A_top = 10.16² = 103.2256 cm²):

| PDG anchor leg | Anchor rate for this wafer | Adopted 1.3659 Hz sits | **Signed deviation** | S/B direction |
|---|---|---|---|---|
| **Leg A (primary, the paper's own):** integral flux ≈ 1 muon cm⁻² min⁻¹ through a horizontal detector → R = A_top/60 | **1.7204 Hz** | **below** | **−20.61 %** | **`flatters_SB`** |
| Leg B (secondary): I_v ≈ 70 m⁻² s⁻¹ sr⁻¹ with I(θ) ∝ cos²θ → J = πI_v/2 → R = A_top·J | 1.1350 Hz | above | **+20.34 %** | `penalizes_SB` |

**Channel label: `flatters_SB`, signed deviation −20.6 % against Leg A.**
One-line justification: the adopted muon rate is *lower* than the primary PDG anchor, so it
under-counts the muon background; less background raises the eventual signal-to-background ratio.

**Disclosure, recorded because it makes the audit stronger and not weaker.** The two PDG
statements quoted by `ref-pdg-muon` are not mutually consistent at the ±20 % level: they bracket
the adopted value from opposite sides (Leg A −20.6 %, Leg B +20.3 %). The channel is therefore
labelled `flatters_SB` **on the anchor leg the v1.0 paper itself invokes**, while the honest
magnitude of the muon channel's directional bias is **≲20 % in either direction**, dominated by
the 30–35 % Gaisser–Guan spread that no in-repo artifact can narrow. Adding the wafer's side-entry
faces (A_x = A_y = 2.032 cm²) raises either anchor by only **+1.97 %** under a cos²θ-weighted
projected-area integral, so side entry does not resolve the discrepancy. **The band is not
narrowed here and the sign is not dropped.**

---

## 3. Environmental-gamma channel

### 3.1 Committed scalar and the four-way numeric distinction (`fp-rate-conflation`)

```console
$ grep '^# total_single_scatter_rate_Hz' data/compton_dRdEdep.csv
# total_single_scatter_rate_Hz = 2.6747e-01 (BOUND incoherent; free-KN pre-binding = 2.6846e-01, binding f_bind = 0.9963)
$ grep '^# VALD-03 anchor' data/compton_dRdEdep.csv
# VALD-03 anchor flux x sigma_KN x N_e (free) = 2.7305e-01; bound/anchor ratio 0.980 (within factor 2)
```

**These are four different numbers. They are not interchangeable.**

| Value [Hz] | What it is | Status |
|---|---|---|
| **2.6747e-01** | **Bound-incoherent single-scatter rate: Klein–Nishina × Hubbell S(x, Z=32)** | **THE RATE OF RECORD** |
| 2.6846e-01 | Free-Klein–Nishina rate *before* binding suppression | pre-binding intermediate |
| 2.7305e-01 | VALD-03 independent anchor Φ·σ_KN·N_e (free electrons), bound/anchor ratio 0.980 | external cross-check |
| 0.267 | The paper's rounded presentation of the rate of record | rounding only |

Binding factor f_bind = 0.9963. Conflating these destroys the ability to check downstream whether
the Hubbell binding suppression is actually applied.

### 3.2 Physics chain (matches `backgrounds.tex` §"Environmental gammas")

**Bound-electron incoherent scattering**: the Klein–Nishina differential cross section
dσ/dΩ = (r_e²/2)(E′/E_γ)²(E′/E_γ + E_γ/E′ − sin²θ) is multiplied by the **Hubbell (1975)
incoherent scattering function S(x, Z = 32)** (`data/ge_incoherent_S.csv`) evaluated at the
momentum-transfer variable x = E_γ[keV]·sin(θ/2)/12.39842 Å⁻¹. Scattering is sampled on the
**pinned Cauchy mean chord ℓ̄ = 4V/S = 0.384848 cm** in the optically thin wafer:
μℓ̄ = **0.117382** at 1 MeV and the double-scatter fraction is **1.3778 %** (recomputed from
`compton_source.optical_depth_mean_chord(1000.0)` and `double_scatter_fraction(1000.0)`), so each
photon scatters **at most once** and the scattered photon escapes. The deposit is therefore the
**recoil-electron kinetic energy T_e = E_γ − E′, a continuum, NOT a full-energy photopeak**.
S(x→0) → 0 rolls the continuum off near 30–50 eV (removing the unphysical free-KN low-energy
plateau); S(x→∞) → Z leaves the Compton **edges** and the bulk continuum unchanged. S(x, Z)
changes the **cross section**, not the energy scale — no quenching, electron recoil throughout.

### 3.3 Independent Compton-edge reproduction

Line energies read from `data/gamma_lines.csv` via `compton_source.load_gamma_lines()`;
E_edge = 2E_γ²/(m_ec² + 2E_γ) evaluated in closed form with m_ec² = 510.99895 keV,
**independently of the sampler**.

| Isotope | E_γ [keV] (from file) | **Recomputed E_edge [keV]** | Committed / paper | **Difference** | Tolerance | Verdict |
|---|---|---|---|---|---|---|
| ⁴⁰K | 1460.822 | **1243.3573** | 1243.4 | **−0.0427 keV** | 0.5 keV | **PASS** |
| ²¹⁴Bi | 1764.494 | **1541.3115** | 1541.3 | **+0.0115 keV** | 0.5 keV | **PASS** |
| ²⁰⁸Tl | 2614.511 | **2381.7571** | 2381.8 | **−0.0429 keV** | 0.5 keV | **PASS** |

**No photopeak.** Over the full 16-line list the highest Compton edge is **2381.7571 keV**
(²⁰⁸Tl). In `data/compton_dRdEdep.csv` the number of bins whose **lower edge** lies above
2381.7571 keV and which carry non-zero content is **0**. Exactly one non-zero bin has a *centre*
above the edge — bin 430, edges [2375.5183, 2444.8947] keV, centre 2409.9569 keV — and the edge
2381.7571 keV falls **inside** that bin; its content 0.7166 counts/kg/day/keV is 10.8 % of the
preceding bin's 6.6071, consistent with a sharp kinematic edge cutting 9 % into a log bin. This is
a **binning effect, not a photopeak**. The bin containing the full line energy 2614.511 keV
(centre 2627.33 keV) carries **exactly 0.0**. The thin-target single-scatter approximation is
therefore intact in the artifact, not merely in the prose.

### 3.4 Normalization band — carried forward **unnarrowed**

Absolute per-line fluxes are anchored to the **LABChico measured environmental-gamma survey**
(Eur. Phys. J. Plus, 2022): ⁴⁰K 1460.8 keV = 0.036 cm⁻² s⁻¹, ²⁰⁸Tl 2614.5 keV = 0.0016
cm⁻² s⁻¹. Th-chain sibling lines are scaled from the measured ²⁰⁸Tl anchor by **DDEP/LNHB
intra-chain emission-probability ratios**; the U-chain is set by the documented **Φ_U = Φ_Th
assumption** (an assumed chain balance, `flux_unc_frac = 1.0` in the file, not a measured line
intensity). Line list context: Heusser, Annu. Rev. Nucl. Part. Sci. **45**, 543 (1995).

**Confidence split, verbatim from the paper and NOT narrowed here:**
**edge positions HIGH** (exact Compton kinematics); **absolute normalization MEDIUM, factor ~2,
site-dependent**.

**Direction (`fp-flattering-gamma-edge`).** The committed normalization sits at the **measured
LABChico anchor itself**, i.e. at the *centre* of the factor-2 band — **not** on either edge.
Channel label: **`neutral`**, signed deviation **0.00 %** relative to its own anchor by
construction (the anchor *is* the adopted value). The **low edge** of the band (×0.5 → 0.1337 Hz)
is the flattering edge and **is not used**; the high edge (×2 → 0.5349 Hz) would penalize. The
band is reported as ×0.5 … ×2 and is not narrowed.

---

## 4. No renormalization, no relocation, no site correction, no overburden — executed scan

Token list (module-level constant `SHIELDED_TOKENS` in `tests/test_env_v1_identity.py`, exported
for reuse by Plan 09-03) — audit machinery, these are the strings that must NOT be applied:
`m.w.e`, `overburden`, `post_shield`, `phi_post`, `buildup`, — audit machinery, must NOT be applied
`attenuation`, `2.92`, `1.41`, `veto_credit`, `mcpd`. — audit machinery, must NOT be applied.
Numeric tokens are matched with digit boundaries by the scan so that `1.4150` and `1.4585` are
*not* false positives on `1.41` (audit machinery; none of these is applied).

Scan target: the four channel modules **plus their full import closure** inside the
`qpd_potential` package, computed by walking module attributes —
`muon_deposit`, `muon_flux`, `compton_source`, `compton_deposit`, `wafer_geometry`, `params`.

```console
$ grep -nEi "m\.w\.e|overburden|post_shield|phi_post|buildup|attenuation|2\.92|1\.41|veto_credit|mcpd" \
    src/qpd_potential/muon_deposit.py src/qpd_potential/muon_flux.py \
    src/qpd_potential/compton_source.py src/qpd_potential/compton_deposit.py \
    src/qpd_potential/wafer_geometry.py src/qpd_potential/params.py
src/qpd_potential/compton_source.py:147:    """Linear attenuation coefficient mu = (mu/rho) * rho [cm^-1]."""
```

**Total hits: 1. Shielded-configuration hits: 0.**

The single hit is **allow-listed with a named justification**, recorded here so a future reader
can audit the exemption rather than trust it:

| File | Line | Text | Why it is not a shielded quantity |
|---|---|---|---|
| `src/qpd_potential/compton_source.py` | 147 | `"""Linear attenuation coefficient mu = (mu/rho) * rho [cm^-1]."""` | This is the **photon mass-attenuation coefficient of germanium** (NIST XCOM, `data/ge_xcom_mu.csv`) — a property of the **target wafer itself**, used to compute μℓ̄ and the double-scatter fraction. It is not a shield, an overburden, a buildup factor, or any post-shield quantity. It multiplies **no** normalization: the total rate is set by the sourced line fluxes and the bound-incoherent cross section. |

The allowlist is a single explicit `(file, exact-line-substring, justification)` entry in
`tests/test_env_v1_identity.py`; any *new* attenuation-like term (NOT applied here) would fail
the test (audit machinery — nothing here is applied). **No numeric factor other than exactly 1.0 multiplies either channel's normalization.**

Veto credit: **exactly 1.0, by construction** — there is no veto in an unshielded surface
configuration. Sentinels are asserted in Plan 09-03.

---

## 5. Directional-bias rows (schema reused by Plan 09-02 and 09-03)

| channel | central value | anchor | **signed deviation** | **direction** | why |
|---|---|---|---|---|---|
| **muon** | 1.3659 Hz | PDG sea-level, Leg A: ≈1 muon cm⁻² min⁻¹ × A_top = **1.7204 Hz** | **−20.61 %** | **`flatters_SB`** | The adopted rate is *below* the primary anchor, so the muon background is under-counted; less background raises S/B. (Anchor Leg B, I_v = 70 m⁻²s⁻¹sr⁻¹ with cos²θ → 1.1350 Hz, gives **+20.34 %**, i.e. `penalizes_SB`; the anchor's own two legs bracket the adopted value.) |
| **gamma** | 2.6747e-01 Hz | LABChico measured survey normalization (the adopted value *is* the anchor), factor-2 site band | **+0.00 %** | **`neutral`** | The committed normalization sits at the measured anchor, not on either edge of its factor-2 band. The **low** edge (×0.5 → 0.1337 Hz) is the flattering one and is **not** used; the high edge (×2) would penalize. |

Both rows carry a **signed** deviation and a direction label from
{`flatters_SB`, `penalizes_SB`, `neutral`}. A row that dropped the sign, or omitted the direction,
fails `tests/test_env_v1_identity.py::test_declaration_records_bias_direction`.

---

## 6. Dimensional check

| Quantity | Dimension | Unit used here |
|---|---|---|
| `integral_muon_rate_Hz`, `total_single_scatter_rate_Hz` | [time]⁻¹ | Hz (absolute, through-wafer — **not** per kg) |
| `dRdEdep` | [mass]⁻¹[time]⁻¹[energy]⁻¹ | counts kg⁻¹ day⁻¹ keV⁻¹ |
| E_dep, E_γ, E_edge | [energy] | keV |
| ξ, Δ_p, ⟨Δ⟩ | [energy] | MeV |
| ⟨ℓ⟩, ℓ̄ | [length] | cm |
| x = ρℓ | [mass][length]⁻² | g cm⁻² |
| per-line gamma flux | [length]⁻²[time]⁻¹ | cm⁻² s⁻¹ |
| μℓ̄, double-scatter fraction, κ, f_bind, veto credit | dimensionless | — |

---

## 7. What this declaration does **not** do

- It does **not** re-run either Monte Carlo (`fp-mc-rerun-drift`).
- It writes **no** file under `data/`.
- It does **not** touch the shared energy grid or any response matrix (**Phase 10** owns the grid
  extension and runs in parallel).
- It does **not** cover the neutron channel (Plan 09-02) or assemble the combined set (Plan 09-03).
- It applies **no** overburden, attenuation, relocation, site-correction or veto credit —
  guards `fp-overburden-leak`, `fp-inherited-shielding` — all NOT applied.

---

_Plan 09-01 · deliverable `deliv-mu-gamma-declaration` · executable counterpart
`tests/test_env_v1_identity.py` (`deliv-identity-tests`)._
