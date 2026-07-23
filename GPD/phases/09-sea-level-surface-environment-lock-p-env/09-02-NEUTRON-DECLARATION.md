# Sea-Level Ambient Neutron Channel Declaration (v2.0)

**Phase:** 09 — Sea-Level Surface Environment Lock (P-ENV)
**Plan:** 09-02, Task 3 (`deliv-neutron-declaration`)
**Requirements:** ROADMAP Phase 9 **SC2** (source actually retrieved and integrity-checked, not
recalled; lethargy division exactly once), **SC3** (order-of-magnitude label at the point of
definition), **SC4** (thermal component named, never zeroed), **SC5** (no shielded quantity).
**Scenario:** unshielded surface, sea level, **zero overburden**, outdoor.
**Executed:** 2026-07-22. Environment: Darwin 25.3.0 (arm64) · Apple clang 21.0.0 · curl 8.16.0 ·
Python 3.11.7 · numpy 1.26.4.

> **ACCURACY LABEL FOR THIS ENTIRE CHANNEL: `order_of_magnitude`.**
> It is attached to every quantity below at its point of definition, and it propagates into
> Phases 13, 14 and 16. **No downstream acceptance test may demand better than order-of-magnitude
> agreement on this channel.** §3 explains why the label is a *consequence of the evidence*, not a
> formality.

---

## 1. Citation and roles — shape vs anchor

| Role | Source | `accuracy_label` |
|---|---|---|
| Differential **SHAPE** | **Sato T., "Analytical Model for Estimating Terrestrial Cosmic Ray Fluxes Nearly Anytime and Anywhere in the World: Extension of PARMA/EXPACS", PLOS ONE 10(12):e0144679 (2015)**, DOI 10.1371/journal.pone.0144679, **open access**. Neutron spectrum = Eq. (6) energy-weighted normalized form × Eq. (4) normalization flux. | `order_of_magnitude` |
| **>10 MeV INTEGRAL anchor, and nothing else** | **Gordon M. S. et al., IEEE Trans. Nucl. Sci. 51, 3427 (2004)**: sea-level NYC Φ(>10 MeV) = 3.5–3.6×10⁻³ cm⁻² s⁻¹ (midpoint 3.550×10⁻³ adopted). | `order_of_magnitude` |

The fitted coefficients **are not tabulated in the Sato article** — the paper states they live in
the EXPACS/PARMA distribution. They were therefore **taken from the official PARMA C++ source at
the pinned mirror commit `6ff37cacb8cf003e2fc269963f9a08f812407264`, compiled unmodified, and not
typed from any article, secondary source, or memory.** Provenance, retrieval command, byte counts,
SHA-256 values and per-artifact integrity verdicts: `data/external/parma/MANIFEST.md`.

**Gordon's DIFFERENTIAL coefficients are PAYWALLED and were unsourceable in this environment.**
Gordon supplies the **integral** benchmark only and is **never** the spectral shape source
(`fp-gordon-as-shape`). Presenting it as one would claim a differential validation that does not
exist.

`WebFetch` and any LLM page summarizer were **not used** as a quote or data source anywhere in
this channel (`fp-neutron-from-memory`).

---

## 2. Energy range, normalization basis, and the lethargy division

| Item | Value | `accuracy_label` |
|---|---|---|
| Committed v1.1 table span | 10.14 eV → 197 MeV (`data/ambient_neutron_flux_v1.1.csv`, 584 bins) | `order_of_magnitude` |
| Sub-eV extension emitted here | 0.01 eV → 1 eV (`data/ambient_neutron_thermal_v2.0.csv`, 201 nodes, 100/decade) | `order_of_magnitude` |
| Normalization basis | per cm² per s; anchored on the **10 MeV – 10 GeV** integral | `order_of_magnitude` |
| Anchor scalar | **k = 1.09610**, dimensionless, applied **uniformly at all energies** | `order_of_magnitude` |
| Evaluation point | s(W-index) = 100, r_c = 2.08 GV (NYC), d = 1033 g cm⁻² (sea level), g = 0.15 (ground) | — |

**Lethargy: the division by E happens EXACTLY ONCE, and here is the one place.**
Sato Eq. (6) is an **energy-weighted (lethargy-form)** normalized spectrum. The single division
lives inside PARMA's own routine, `data/external/parma/src/subroutines.cpp` **line 673**:

```cpp
     getNeutSpec = Fl * (basic * geofactor + ther) / e;
//                                                  ^^^ the one and only /E
```

so `getNeutSpecCpp()` already returns the **per-energy** differential dΦ/dE_n in
cm⁻² s⁻¹ MeV⁻¹. Neither `data/external/parma/parma_neutron_driver.cpp` nor
`src/qpd_potential/parma_neutron_flux.py` divides again (`fp-lethargy-double-divide`). This is
proved by an **integral identity, not by inspection**: ∫φ dE = ∫(Eφ) d(ln E) agrees to
**< 0.0001 %** on five well-separated decades (0.01–0.1 eV, 1–10 eV, 1–10 keV, 1–10 MeV,
100–1000 MeV) — `tests/test_ambient_neutron_flux.py::test_lethargy_divided_exactly_once`.

**Axis tag.** E_n is **incident neutron kinetic energy**, never a recoil axis. A 1 MeV neutron does
not deposit 1 MeV of recoil. No recoil kinematics, no keV_nr, no quenching factor appears anywhere
in this channel; the n-Ge elastic fold is **Phase 13**.

**Also recorded because it would silently change every number:** PARMA's `s` argument is the
**W-index**, not the force-field potential. `subroutines.cpp:20` converts internally,
`getFFPfromWCpp(s) = 370 + 0.3·s^1.45` MV → 608.3 MV at s = 100. The routine's own inline comment
`// s:Force Field Potential (MV)` is **stale**; `main-simple.cpp`'s calling convention is
authoritative.

---

## 3. Anchor reproduction — Phase-7 gap D2 **CLOSED**

Phase-7 verification gap **D2** (severity *significant*, *"the weakest reproducibility link in the
phase"*) read: *"No PARMA driver committed; the decisive 3.55e-3 and 1.317e-2 integrals cannot be
recomputed."* A driver is now committed and every decisive number is recomputable in-repo.

Tolerances were **stated before the checks ran** (`tests/test_ambient_neutron_flux.py`, module
constants) and were **not loosened afterwards**.

### 3.1 Untuned first — reported **before** the anchor rescale

An agreement that only appears after tuning is not a cross-check, and reporting it in the other
order would make it look like one.

| nodes/decade | Φ_native(10 MeV – 10 GeV), k = 1 | vs committed 3.239×10⁻³ |
|---|---|---|
| 100 | 3.238751×10⁻³ | **−0.008 %** |
| 200 | 3.238744×10⁻³ | **−0.008 %** |
| 400 | 3.238743×10⁻³ | **−0.008 %** |
| 800 | 3.238742×10⁻³ | **−0.008 %** |

Quadrature convergence on node doubling (200 → 400): **0.0000 %** change (tolerance 0.5 %).
Tolerance on the anchor: 2 %. **PASS.**

**The untuned cross-check itself:** Φ_native = 3.2387×10⁻³ against the Gordon midpoint
3.550×10⁻³ → **−8.77 %, with no fitting whatsoever.** This ~9 % agreement between an
independently-parametrized transport model and a measured integral is the *only* independent
validation this channel possesses.

### 3.2 Anchored

| Quantity | Recomputed | Committed | Deviation | Tol | Verdict |
|---|---|---|---|---|---|
| Φ(10 MeV – 10 GeV), k = 1.09610 | **3.549986×10⁻³** cm⁻²s⁻¹ | 3.550×10⁻³ | **−0.0004 %** | 1 % | **PASS** |
| Independently solved k for the Gordon midpoint | **1.096104** | 1.09610 | **+0.0004 %** | 1 % | **PASS** |
| Φ(0.01 eV – 10 GeV), k = 1.09610 | **1.317379×10⁻²** cm⁻²s⁻¹ | 1.317×10⁻² | **+0.029 %** | 5 % | **PASS** |

### 3.3 Joint identity — the check D2 said had never been performed

The committed table and its recorded provenance had only ever been validated **separately**. The
recompiled pinned source was evaluated at the table's **own 584 bin centres** and compared
pointwise against `phi_default_cm2_s_MeV`:

| Statistic | Value | Tolerance | Verdict |
|---|---|---|---|
| **median** relative deviation | **3.88×10⁻⁶ (0.000388 %)** | ≤ 1 % | **PASS** |
| **max** relative deviation | **3.88×10⁻⁶ (0.000388 %)**, at E_n = 0.0170327 keV | ≤ 5 % | **PASS** |
| bins deviating > 1 % | **0 / 584** | — | **PASS** |
| bins deviating > 5 % | **0 / 584** | — | **PASS** |

The deviation is **uniform across all 584 bins** — which is itself informative, and is reported
rather than waved through. A uniform relative offset of 3.88×10⁻⁶ is exactly the rounding of the
anchor scalar: the exact solved k is 1.0961043 and the header records k = 1.09610, giving
(1.0961043 − 1.09610)/1.09610 = 3.9×10⁻⁶. The committed table was generated with the *unrounded*
k. **The benign reading is confirmed and the adverse reading — that the table was produced by a
path its header does not describe — is excluded by evidence, not assumed away.**

### 3.4 Why the label is still `order_of_magnitude`

Every check above passed at the 10⁻⁵–10⁻³ level. **That is a reproducibility result, not an
accuracy result.** It proves the committed numbers are what the recorded code produces. It says
nothing about whether the spectrum is right.

The accuracy the *source* claims: Sato validates PARMA against measured ground-level spectra to
roughly a few tens of percent in the fast region. The accuracy **this project** claims is weaker
and deliberately so:

- The **only independent cross-check that exists is a single integral above 10 MeV** agreeing to
  ~8.8 % untuned.
- The Gordon anchor is applied as a **single energy-independent scalar k**, so a normalization
  constrained *only above 10 MeV* is propagated onto the **entire** spectrum, including the eV–keV
  region where it is untested.
- **Two spectra can share the >10 MeV integral and differ badly at eV–keV energies** — and those
  are exactly the energies that set the Ge recoil rate in the CEvNS region of interest.
- Gordon's differential coefficients are paywalled, so no differential validation is available at
  all.

**Therefore: `accuracy_label = order_of_magnitude`, and it is a consequence of that evidence, not
a formality** (`fp-precision-inflation`).

---

## 4. Band semantics for an **unshielded surface wafer** — stated unambiguously

| Column in `data/ambient_neutron_flux_v1.1.csv` | What it is | Status here |
|---|---|---|
| `phi_default` = `phi_hi` | **OUTDOOR sea level** — the upper leg of the band | **OPERATIVE.** This is the value this configuration uses. |
| `phi_lo` = `phi_default`/5 | A scalar stand-in for **INDOOR / building attenuation** | **NOT an error bar for this configuration.** Not used, not emitted, not averaged. |

Verified structurally, not just asserted: over all 584 bins `phi_hi == phi_default` to
rtol 10⁻¹², and `phi_lo == phi_default/5` to rtol 10⁻⁶
(`tests/test_ambient_neutron_flux.py::test_band_semantics_phi_lo_is_indoor_not_an_error_bar`).
`data/ambient_neutron_thermal_v2.0.csv` emits **no `phi_lo` column at all**.

**The consequence, stated explicitly.** Using `phi_lo` — or the band midpoint — as the central
value would **cut the neutron background by a factor 5 and improve S/B by the same factor.** That
is the single largest available flattering move in this phase, and it is exactly the direction the
Phase-8 errors ran. `fp-indoor-band-as-central`.

The committed v1.1 header itself already flags the scalar as **unvalidated**: building roof/wall
moderation reshapes the spectrum (moderating fast → thermal), and a pure scalar **understates**
that spectral-shape systematic. Whether the wafer is indoors or outdoors is a **configuration
question, not an uncertainty band** — no scalar can represent it, and this phase cannot settle it.

---

## 5. Thermal disposition — Φ_th is a **named quantity**, never zero

**Φ_th is produced, not gapped.** ROADMAP SC4 is satisfied on branch (a).

| Quantity | Value | Bounds | Convention | `accuracy_label` |
|---|---|---|---|---|
| **Φ_th** | **2.767075×10⁻³ cm⁻² s⁻¹** | 1.0×10⁻⁸ MeV → 5.0×10⁻⁷ MeV, i.e. **0.01 eV → 0.5 eV** | **cadmium cutoff, 0.5 eV** (stated with its number, as the plan's agent-discretion clause requires) | `order_of_magnitude` |

- Table: `data/ambient_neutron_thermal_v2.0.csv`, 201 nodes, 100/decade, 0.01 eV → 1 eV.
- Φ_th is **21.00 %** of the broad Φ(0.01 eV – 10 GeV) = 1.317379×10⁻² cm⁻² s⁻¹.
- Cutoff sensitivity, reported because the convention is a choice: 0.4 eV → 2.728×10⁻³;
  **0.5 eV → 2.767×10⁻³ (adopted)**; 1.0 eV → 2.898×10⁻³. The choice moves Φ_th by ≲5 %, far
  inside the channel's own accuracy label.
- The sub-eV table is **deliberately NOT on `shared_energy_grid()`**, and sits entirely below its
  0.01 keV floor. **Phase 10 owns the shared-grid extension and runs in parallel with Phase 9**;
  taking a dependency on it here would serialize two independent phases. Phase 13/14 must resample.
- **Caveat carried, not buried:** PARMA's thermal term is a 293.6 K free-gas ambient Maxwellian.
  Whether that is adequate for a **mK cryogenic** target's capture channel is an unvalidated
  assumption this phase cannot settle; it is handed to Phase 14 with the number.

**Morphology confirmed** (all four canonical ground-level features present; a feature-free spectrum
would be a bug, not a result):

| Feature | Located at | Expected |
|---|---|---|
| thermal Maxwellian peak of φ(E) | **0.0250 eV** | ~0.03 eV — and equal to PARMA's E_th = 2.5×10⁻⁸ MeV = kT at 293.6 K (0.0253 eV) |
| same peak in the **lethargy** representation E·φ | **0.0507 eV** | analytic 2·E_th = 0.0500 eV (E·φ ∝ (E/E_th)²e^{−E/E_th}) |
| 1/E epithermal plateau, 1 eV – 10 keV | E·φ flat to a factor **1.390** | flat within a factor ~2 |
| evaporation hump | **1.957 MeV** | 1–3 MeV |
| cascade peak | **118.9 MeV** | ~100 MeV |

---

## 6. Declared omissions carried to Phase 13 — each quantified

1. **The 20 MeV ENDF/B-VIII.0 σ_el ceiling** (Phase-7 gap **D1**). Resolved by **user decision
   2026-07-22 as *truncate and document***: σ_el is **not to be extrapolated above 20 MeV**. This
   is a truncation of the *cross section*, not of this flux; it is recorded here because the fold
   consumes both.
2. **The ~197 MeV shared-grid ceiling.** The committed v1.1 table stops at 197 MeV. From its own
   header: the on-grid Φ(10 – 197 MeV) = 2.820×10⁻³ against the full-range anchor
   Φ(10 MeV – 10 GeV) = 3.550×10⁻³, so **21 % of the >10 MeV flux lies above the grid ceiling**, in
   the 197 MeV – 10 GeV cascade tail.
   **The Phase-7 deferral rationale for CALC-24 — that shield attenuation (NOT applied here) made the >10 MeV tail
   unimportant — is VOID at the surface.** There is no shield. The omission is therefore a larger
   fraction of a larger flux than it was under the (now void) shielded premise. Flagged for the
   orchestrator; **not closed here**, because closing it (a TENDL-2023 splice) is follow-up scope.

Both omissions are **declared**, quantified, and directionally identified in §7.

---

## 7. Directional-bias row for this channel

Same schema as Plan 09-01 §5.

| channel | central value | anchor | **signed deviation** | **direction** | why |
|---|---|---|---|---|---|
| **neutron** | Φ(10 MeV–10 GeV) = 3.550×10⁻³ cm⁻²s⁻¹ on `phi_default` = `phi_hi` (outdoor) | Gordon 2004 NYC sea level, 3.5–3.6×10⁻³, midpoint 3.550×10⁻³ | **+0.00 %** (anchored to the midpoint by construction; the **untuned** PARMA prediction sits at **−8.77 %**) | **`penalizes_SB`** | The channel adopts the **outdoor / upper** leg of its own band and the **midpoint** of the Gordon range, not the low edge; and the NYC evaluation point is *low* for any higher-altitude or higher-cutoff site, so the normalization would move **up**, raising the background and lowering S/B. Choosing the operative value this way costs S/B rather than buying it. |

Two directional facts that belong in the same row and are **not** hidden in prose:

- **The available flattering move, quantified and refused:** using `phi_lo = phi_default/5` would
  be a **factor-5 `flatters_SB`** move. It is not used anywhere in this channel.
- **The declared omissions are also directional:** dropping the 21 % of >10 MeV flux above the
  ~197 MeV grid ceiling, and truncating σ_el at 20 MeV, both *remove* background from the eventual
  fold — i.e. both are **`flatters_SB`** omissions. They are carried openly to Phase 13 rather than
  netted against the channel's `penalizes_SB` central value.

---

## 8. No shielded quantity — SC5 statement for this channel

No NUCLEUS shielding attenuation, no post-shield fluence φ_post, no overburden depth, no buildup
factor, no veto credit and no multiplicity credit appears anywhere in this channel, under any name
— all **NOT applied**. Veto credit is exactly **1.0 by construction**: there is no veto in an
unshielded surface configuration, so this is not a policy default a later phase could relax. The
Phase-8 geometry gate returned NO FIT and voided the shielded premise
(`fp-shielded-quantity-leak`, project proxy `fp-inherited-shielding`).

Executed check (audit machinery; every token below is one that must **NOT be applied**):
`tests/test_ambient_neutron_flux.py::test_no_shielded_quantity_in_neutron_channel` scans
`src/qpd_potential/parma_neutron_flux.py` and `data/ambient_neutron_thermal_v2.0.csv` with the
token constant exported by `tests/test_env_v1_identity.py` and requires **zero** hits. It returned
zero.

No regularized/Tikhonov differentiation, no figure digitization, no multi-target
over-determination test was introduced (`fp-inversion-scope-creep`); CALC-12 and VALD-11 remain
orphaned by design.

---

## 9. Dimensional check

| Quantity | Dimension | Unit |
|---|---|---|
| φ = dΦ/dE_n | [length]⁻²[time]⁻¹[energy]⁻¹ | cm⁻² s⁻¹ MeV⁻¹ |
| Φ, Φ_th | [length]⁻²[time]⁻¹ | cm⁻² s⁻¹ |
| E_n | [energy] | **keV** in project-facing tables; MeV internally to PARMA |
| k | dimensionless | — |
| veto credit | dimensionless | exactly 1.0 |

---

_Plan 09-02 · deliverables `deliv-parma-cache` (`data/external/parma/MANIFEST.md`),
`deliv-parma-driver` (`src/qpd_potential/parma_neutron_flux.py`), `deliv-thermal-table`
(`data/ambient_neutron_thermal_v2.0.csv`), `deliv-neutron-tests`
(`tests/test_ambient_neutron_flux.py`)._
