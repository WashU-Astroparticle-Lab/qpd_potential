# Plan 10-03 --- Grid Construction, Caller Pins, and the Decoupled Deposit Axis

**Phase:** 10 --- Sub-eV Grid Extension and the Trigger Observable (P-GRID)
**Discharges:** ROADMAP Phase 10 success criteria 1 and 2; requirement CALC-13.
**Interpreter:** `/opt/anaconda3/bin/python3` --- numpy 1.26.4, scipy 1.17.1, pytest 7.4.0.

---

## 1. The construction

```python
dex = log10(2e5 / 1e-2) / 584                       # = 0.0125017637 dex/bin
prepended = 1e-2 * 10**(-arange(160, 0, -1) * dex)  # 160 new edges, keV
extended  = concatenate([prepended, v1_0_edges])    # 745 edges, 744 bins
```

The extension **prepends 160 bins at the v1.0 spacing**. It does **not** re-run
`logspace` over the wider range. That distinction is the whole plan.

### Measured properties (all reproduced by `tests/test_energy_grid_extension.py`)

| Quantity | v1.0 | v2.0-ext |
|---|---|---|
| bins / edges | 584 / 585 | **744 / 745** |
| first edge | 10 eV exactly | **0.0999350 eV** |
| first bin centre | **10.144972680282425 eV** | **0.1013838 eV** |
| last edge | 2e5 keV = 197 MeV… (2.0e8 eV) | identical |
| realised spacing | 0.0125017637 dex/bin | identical, by construction |
| realised bins/decade | **79.988714**, not 80 | identical |
| `np.array_equal(ext[160:], v1_0)` | --- | **True** |
| max absolute edge difference on the overlap | --- | **exactly 0.0** |

"80 bins/decade" is **nominal**. `round(log10(2e7) * 80) = 584` and
`log10(2e7)/584 = 0.0125017637`, i.e. 79.988714 bins/decade. Preserving *that*
number, rather than re-solving the rounding, is what makes success criterion 2
achievable.

---

## 2. Rejected alternative A --- the naive rebuild (`fp-naive-logspace`)

```python
naive = np.logspace(log10(1e-4), log10(2e5), 745)
```

**It looks right on every superficial check:**

| Check | naive | verdict |
|---|---|---|
| bin count | 744 | passes |
| first edge | 0.1000000 eV exactly | passes, and looks *better* than 0.0999350 |
| first bin centre | 0.1014497 eV | plausible |
| `np.allclose(naive[160:], v1_0, rtol=1e-3)` | True | **passes** |

**And it is not the v1.0 edge set.** Its spacing is `log10(2e9)/744 = 0.0125013844`
dex/bin against the v1.0 `0.0125017637`, so its overlapping edges drift:

```
max relative edge drift vs v1.0 = 5.101629e-04,  worst at index 0 (the v1.0 floor itself)
np.array_equal(naive[160:], v1_0_edges) = False
```

Every archived v1.x spectrum placed on that axis would be **silently
reinterpolated** --- the exact failure success criterion 2 names.

**Both constructions pass a bin-count check, and the naive one passes a
1e-3 tolerance check.** Only `np.array_equal` distinguishes them. That is why the
shipped assertion is `np.array_equal` and never `np.allclose`, and why
`test_naive_rejected_counterexample` exists: without it the exact-superset claim
would be untested.

## 3. Rejected alternative B --- 159 prepended bins

| n prepended | bins | floor | verdict |
|---|---|---|---|
| 159 | 743 | **0.1028536 eV** | **fails**: floor is ABOVE 0.1 eV, so the axis does not reach 0.1 eV; and 743 bins, not 744 |
| **160** | **744** | **0.0999350 eV** | **the unique choice satisfying both clauses of criterion 1** |
| 161 | 745 | 0.0970993 eV | reaches 0.1 eV but gives 745 bins, breaking "~744 bins" |

All three preserve the v1.0 edges exactly (that is a property of prepending at the
v1.0 spacing, not of the count). 160 is singled out by the *floor* and the *bin
count* together.

### Owning the loose reading of criterion 1

The criterion says the axis "runs from 0.1 eV". **The first edge is 0.0999350 eV,
not exactly 0.1 eV.** Read as "the axis covers 0.1 eV", it is satisfied. Read as
"the first edge is exactly 0.1 eV", it is not --- and only the naive rebuild
satisfies that stricter reading, at the cost of criterion 2. The two readings are
not simultaneously satisfiable, and this plan chose criterion 2. That trade is
stated here rather than left for a reader to discover.

---

## 4. DEVIATION D1 --- the default stayed at `v1.0`

**The plan instructed:** *"Make the extended selection the default so that
'shared_energy_grid() runs from 0.1 eV' is literally true."*

**What was shipped:** `DEFAULT_GRID_VERSION = "v1.0"`. The extension is reached by
`shared_energy_grid("v2.0-ext")`.

**Why.** The instruction assumes Phase 10 owns every call site. It does not:
**Phase 9 was executing concurrently in this same worktree**, adding its own
callers. Flipping the default produced, in a full-suite run:

```
FAILED tests/test_env_v1_identity.py::test_no_photopeak_above_edge
E   ValueError: operands could not be broadcast together with shapes (744,) (584,)
```

against a Phase-9 file this phase is not permitted to edit.

That failure is not an inconvenience. **It is `fp-default-change` caught in the
act:** a caller that does not state its version silently receives a different
axis. The plan's mitigation for that proxy was to pin every caller --- which works
only if you can reach every caller.

A `v1.0` default:

- makes silent re-binning **impossible** rather than merely pinned-against;
- **fails in the safe direction** --- a caller that forgets to ask for the
  extension gets the v1.0 axis, and then trips the plan 10-01 `_erec_of_edep`
  guard the moment it tries to evaluate sub-eV, instead of quietly re-binning an
  archived artifact;
- discharges criterion 2 **more strongly** than the plan's own construction would
  have, at the cost of discharging criterion 1 through
  `shared_energy_grid("v2.0-ext")` rather than through a bare call.

**Follow-up recorded rather than acted on:** Phase 9 has since pinned its own
callers explicitly (`shared_energy_grid(version="v1.0")` at
`tests/test_env_v1_identity.py:335,409` and `tests/test_surface_environment.py:147`,
and a both-versions parametrisation at `tests/test_ambient_neutron_flux.py:300`).
A future default flip would therefore now be safe. It was **not** performed here,
because Phase 9 is still in flight and because the argument above stands on its
own merits regardless of who is pinned.

---

## 5. The caller version-pin table

Recorded command, re-run by
`tests/test_energy_grid_extension.py::test_caller_pins_every_site_is_in_the_table`:

```
grep -rn "shared_energy_grid(" --include=*.py src/ tests/
```

**29 hits, 29 rows.** (28 at the end of plan 10-03; plan 10-04 added one prose hit at `response_matrix.py:608`, enumerated below.) (The `def shared_energy_grid(` line itself is excluded.)

### 5.1 Raw output

```
src/nuclear/parse_endf_nGe.py:17:      (ENDF native  U  shared_energy_grid()) with log-log interpolation.
src/nuclear/parse_endf_nGe.py:278:    shared_energy_grid() (keV -> eV), clipped to the ENDF support."""
src/nuclear/parse_endf_nGe.py:283:    shared_eV = shared_energy_grid("v1.0") * 1.0e3  # keV -> eV
src/qpd_potential/compton_deposit.py:183:    edges = shared_energy_grid("v1.0")
src/qpd_potential/response_matrix.py:137:    Centres are the GEOMETRIC MEANS of adjacent ``shared_energy_grid(version)``
src/qpd_potential/response_matrix.py:156:    edges_keV = md.shared_energy_grid(version)
src/qpd_potential/parma_neutron_flux.py:296:#: Sub-eV table grid, DELIBERATELY NOT shared_energy_grid().  Phase 10 owns the
src/qpd_potential/parma_neutron_flux.py:333:        "# ======================== THIS GRID IS NOT shared_energy_grid() ====================",
src/qpd_potential/parma_neutron_flux.py:338:        "# It is DELIBERATELY NOT the project shared_energy_grid(), whose floor is 0.01 keV.",
src/qpd_potential/muon_deposit.py:223:#: `shared_energy_grid()` "runs from 0.1 eV" literally. That instruction assumed
src/qpd_potential/muon_deposit.py:240:#: `shared_energy_grid("v2.0-ext")`, and criterion 2 is discharged more strongly
src/qpd_potential/muon_deposit.py:264:def shared_energy_grid(version: str = DEFAULT_GRID_VERSION) -> np.ndarray:
src/qpd_potential/muon_deposit.py:420:    edges = shared_energy_grid("v1.0")
src/qpd_potential/deposited_spectra.py:129:    edges = shared_energy_grid("v1.0")
tests/test_env_v1_identity.py:335:    edges = md.shared_energy_grid(version="v1.0")
tests/test_env_v1_identity.py:409:    edges = md.shared_energy_grid(version="v1.0")
tests/test_ambient_neutron_flux.py:279:    assert "NOT the project shared_energy_grid()" in text
tests/test_ambient_neutron_flux.py:290:    # The grid really is not shared_energy_grid(), for EITHER version.  Checked by
tests/test_ambient_neutron_flux.py:300:        shared = md.shared_energy_grid(version=version)
tests/test_energy_grid_extension.py:32:    return md.shared_energy_grid("v1.0")
tests/test_energy_grid_extension.py:36:    return md.shared_energy_grid("v2.0-ext")
tests/test_energy_grid_extension.py:138:        md.shared_energy_grid("v2.0")
tests/test_energy_grid_extension.py:140:        md.shared_energy_grid("extended")
tests/test_energy_grid_extension.py:154:        ["grep", "-rn", "shared_energy_grid(", "--include=*.py", "src/", "tests/"],
tests/test_energy_grid_extension.py:156:    return [h for h in out if "def shared_energy_grid(" not in h]
tests/test_energy_grid_extension.py:183:    assert np.array_equal(md.shared_energy_grid(), md.shared_energy_grid("v1.0"))
tests/test_energy_grid_extension.py:184:    assert md.shared_energy_grid().size == 585
tests/test_energy_grid_extension.py:201:        assert 'shared_energy_grid("v1.0")' in src, f"{path} is not pinned"
tests/test_surface_environment.py:147:    edges = md.shared_energy_grid(version="v1.0")   # frozen v1.0 artifacts live here
tests/test_compton_channel.py:153:    assert np.array_equal(_SPEC.edges_kev, shared_energy_grid("v1.0"))
```

### 5.2 The table

| Call site | What it is | Version pin | Reason |
|---|---|---|---|
| `src/nuclear/parse_endf_nGe.py:17` | module docstring | n/a — prose | Not a call site: documentation or a string literal mentioning the function by name. Enumerated individually rather than filtered out by a pattern tweak, so the grep count stays auditable. |
| `src/nuclear/parse_endf_nGe.py:278` | function docstring | n/a — prose | Not a call site: documentation or a string literal mentioning the function by name. Enumerated individually rather than filtered out by a pattern tweak, so the grep count stays auditable. |
| `src/nuclear/parse_endf_nGe.py:283` | union-grid construction — writes `data/endf_nGe_elastic_v1.1.csv` | **v1.0**, explicit | Frozen data-preparation script. The extension is irrelevant here anyway (the union grid is clipped to the ENDF support), but the pin is stated so the artifact's provenance does not depend on an implicit default. |
| `src/qpd_potential/compton_deposit.py:205` | `spectrum()` — writes `data/compton_dRdEdep.csv` | **v1.0**, explicit | Phase-4 producer. Same reason: silent re-binning of an archived v1.x product is exactly what success criterion 2 forbids. LINE MOVED BY PLAN 15-02 (183 -> 205), which added a `grid_version` parameter DEFAULTING to `"v1.0"` and KEPT THIS LITERAL PIN as the default branch, so a caller that does not name a version still receives the 584-bin axis. |
| `src/qpd_potential/response_matrix.py:137` | docstring of `E_dep_grid_from_shared_grid_eV` | n/a — prose | Not a call site: documentation or a string literal mentioning the function by name. Enumerated individually rather than filtered out by a pattern tweak, so the grep count stays auditable. |
| `src/qpd_potential/response_matrix.py:156` | `E_dep_grid_from_shared_grid_eV(version)` | **caller-supplied**, required argument | The decoupling point added by this plan. It has no default of its own: the caller must name the version, which is how plan 10-04 selects the 744-column axis while the v1.0 comparison rebuild selects 584. |
| `src/qpd_potential/response_matrix.py:608` | `axis_source` provenance string in `run_design` | n/a — prose | Not a call site: an f-string recording which axis route the npz provenance header should name. ADDED BY PLAN 10-04; enumerated here rather than filtered out by a pattern tweak, so the grep count stays auditable. |
| `src/qpd_potential/parma_neutron_flux.py:296` | PHASE 9 FILE — comment stating its grid is deliberately NOT this one | n/a — prose | Not a call site: documentation or a string literal mentioning the function by name. Enumerated individually rather than filtered out by a pattern tweak, so the grep count stays auditable. |
| `src/qpd_potential/parma_neutron_flux.py:333` | PHASE 9 FILE — CSV header string | n/a — prose | Not a call site: documentation or a string literal mentioning the function by name. Enumerated individually rather than filtered out by a pattern tweak, so the grep count stays auditable. |
| `src/qpd_potential/parma_neutron_flux.py:338` | PHASE 9 FILE — CSV header string | n/a — prose | Not a call site: documentation or a string literal mentioning the function by name. Enumerated individually rather than filtered out by a pattern tweak, so the grep count stays auditable. |
| `src/qpd_potential/muon_deposit.py:223` | DEVIATION D1 comment on `DEFAULT_GRID_VERSION` | n/a — prose | Not a call site: documentation or a string literal mentioning the function by name. Enumerated individually rather than filtered out by a pattern tweak, so the grep count stays auditable. |
| `src/qpd_potential/muon_deposit.py:240` | DEVIATION D1 comment on `DEFAULT_GRID_VERSION` | n/a — prose | Not a call site: documentation or a string literal mentioning the function by name. Enumerated individually rather than filtered out by a pattern tweak, so the grep count stays auditable. |
| `src/qpd_potential/muon_deposit.py:452` | `spectrum()` — writes `data/muon_dRdEdep.csv` | **v1.0**, explicit | Phase-4 producer of a validated 1e9-sample artifact. Inheriting a changed default would silently re-bin it. Re-running the Phase-4 deposit Monte Carlo onto the extended axis is Phase 15's job. LINE MOVED BY PLAN 15-02 (420 -> 452), which did exactly that: it added a `grid_version` parameter DEFAULTING to `"v1.0"` and KEPT THIS LITERAL PIN as the default branch. |
| `src/qpd_potential/deposited_spectra.py:129` | combined spectrum — writes `data/combined_dRdEdep.csv` | **v1.0**, explicit | Phase-4 producer, and the file `response_matrix.load_E_dep_grid_eV` still parses for archived provenance. Moving it would invalidate the 4.918e-07 round-trip comparison this plan measures. |
| `tests/test_env_v1_identity.py:335` | Phase-9 identity test | **v1.0**, explicit | PHASE 9 FILE, not edited by this plan. Phase 9 pinned itself to v1.0 after the version selector appeared. Correct: it compares against frozen v1.0 artifacts. |
| `tests/test_env_v1_identity.py:409` | Phase-9 identity test | **v1.0**, explicit | PHASE 9 FILE, not edited by this plan. Same reasoning. |
| `tests/test_ambient_neutron_flux.py:279` | PHASE 9 FILE — asserts the header string | n/a — prose | Not a call site: documentation or a string literal mentioning the function by name. Enumerated individually rather than filtered out by a pattern tweak, so the grep count stays auditable. |
| `tests/test_ambient_neutron_flux.py:290` | PHASE 9 FILE — comment | n/a — prose | Not a call site: documentation or a string literal mentioning the function by name. Enumerated individually rather than filtered out by a pattern tweak, so the grep count stays auditable. |
| `tests/test_ambient_neutron_flux.py:300` | Phase-9 neutron-table test | **parametrised over BOTH versions** | PHASE 9 FILE, not edited by this plan. Phase 9 asserts its own sub-eV neutron grid is not shared_energy_grid() for either version. |
| `tests/test_energy_grid_extension.py:32` | `_v1()` helper | **v1.0**, explicit | This plan's own test helper. |
| `tests/test_energy_grid_extension.py:36` | `_ext()` helper | **v2.0-ext**, explicit | This plan's own test helper. |
| `tests/test_energy_grid_extension.py:138` | unknown-version rejection | n/a | Asserts an unrecognised version string raises rather than falling back to a default. |
| `tests/test_energy_grid_extension.py:140` | unknown-version rejection | n/a | Same. |
| `tests/test_energy_grid_extension.py:154` | the recorded grep command itself | n/a | The literal enumeration command, inside the closure test. |
| `tests/test_energy_grid_extension.py:183` | default-is-v1.0 assertion | **default**, deliberately | Pins DEVIATION D1: the bare call must return the v1.0 axis, so no archived product can be re-binned by omission. |
| `tests/test_energy_grid_extension.py:184` | default-is-v1.0 assertion | **default**, deliberately | Same; asserts 585 edges from the bare call. |
| `tests/test_energy_grid_extension.py:201` | source-level pin check | n/a | Greps the four Phase-4 producers for the literal `shared_energy_grid("v1.0")`. |
| `tests/test_surface_environment.py:147` | Phase-9 surface-environment test | **v1.0**, explicit | PHASE 9 FILE, not edited by this plan. Comment in that file states 'frozen v1.0 artifacts live here'. |
| `tests/test_compton_channel.py:153` | asserts the frozen Compton spectrum's axis | **v1.0**, explicit | The frozen Compton spectrum is a v1.0 product and must keep matching the v1.0 axis. UPDATED BY THIS PLAN from a bare call. |
| `tests/test_ia_broadening.py:292` | switch-off bit-identity check | **v1.0**, explicit | ADDED BY PLAN 11-04. Compares the broadening-OFF fold against the pre-existing v1.0 chain, so it MUST use the v1.0 axis; a v2.0-ext axis would make the comparison meaningless rather than merely different. |
| `tests/test_ia_broadening.py:372` | order-of-operations check | **v1.0**, explicit | ADDED BY PLAN 11-04. Shows broaden-then-rebin differs from rebin-then-broaden. Pinned to v1.0 because the frozen comparison object is a v1.0 product; the ordering result is axis-independent. |
| `tests/test_ia_broadening.py:393` | no-exp(-2W)-factor check | **v1.0**, explicit | ADDED BY PLAN 11-04. Verifies the integrated rate above 10 eV is unchanged by broadening. Pinned to v1.0 because the >10 eV region is exactly the v1.0 support. |
| `tests/test_ia_broadening.py:447` | v1.0 regression (ROADMAP SC4) | **v1.0**, explicit | ADDED BY PLAN 11-04. THE regression target itself. Pinned to v1.0 by definition -- it compares against the frozen v1.0 spectrum on the preserved overlapping edge set. |
| `tests/test_neutron_fold.py:53` | Phase-13 assertion that the DEFAULT is still the 585-edge v1.0 axis | **default (v1.0)**, deliberately unpinned | ADDED BY PLAN 13-03. This call site exists PRECISELY to exercise the default, so pinning it would make the check vacuous. It asserts `shared_energy_grid()` still returns 585 edges, i.e. that `DEFAULT_GRID_VERSION` is `v1.0` and that the `muon_deposit.shared_energy_grid` docstring calling `v2.0-ext` the default is wrong. |
| `tests/test_neutron_fold.py:54` | Phase-13 assertion that the extended axis is 745 edges / 744 bins | **v2.0-ext**, explicit | ADDED BY PLAN 13-03. The neutron-only extended fold loads its deposit axis from the `_ext.npz` matrices, not from this function; this row is the independent check that the opt-in extended axis has the 744 bins the fold's own shape guard demands. |
| `src/qpd_potential/muon_deposit.py:446` | comment naming the pin | n/a — prose | Not a call site: a comment in the Plan 15-02 branch explaining why the literal v1.0 pin is kept alongside the new `grid_version` parameter. Enumerated individually so the grep count stays auditable. |
| `src/qpd_potential/muon_deposit.py:454` | muon deposit MC — opt-in extended axis | **caller-supplied**, reached only by naming a non-v1.0 version | ADDED BY PLAN 15-02. The other branch of the same pin. It is unreachable unless the caller passes `grid_version="v2.0-ext"` explicitly, which is what Plan 15-02's extended run does at its own call site. |
| `src/qpd_potential/compton_deposit.py:198` | comment naming the pin | n/a — prose | Not a call site: a comment in the Plan 15-02 branch explaining why the literal v1.0 pin is kept alongside the new `grid_version` parameter. Enumerated individually so the grep count stays auditable. |
| `src/qpd_potential/compton_deposit.py:207` | Compton deposit MC — opt-in extended axis | **caller-supplied**, reached only by naming a non-v1.0 version | ADDED BY PLAN 15-02. Unreachable without an explicit `grid_version="v2.0-ext"`. |
| `src/qpd_potential/compton_deposit.py:367` | `run_compton_analytic()` — deterministic (noise-free) Compton assembly | **caller-supplied**, defaults to `"v2.0-ext"` | ADDED 2026-07-23 (curve-smoothing work). This path has NO v1.0 leg on purpose: it exists only to replace the extended-axis MC deliverable, whose sampling scatter dominated the sub-keV roll-off the reconstructed figure plots. It writes NO archived v1.x product, so the success-criterion-2 re-binning hazard that forces the literal `"v1.0"` pin on the Phase-4 producers does not apply. It is validated AGAINST the MC (`tests/test_compton_analytic.py`), never substituted for it silently. |
| `src/qpd_potential/muon_analytic.py:208` | `run_muon_analytic()` — deterministic (noise-free) muon assembly | **caller-supplied**, defaults to `"v2.0-ext"` | ADDED 2026-07-23 (curve-smoothing work). Same disposition as the Compton analytic path: no v1.0 leg, because it writes no archived v1.x product and exists only to replace the extended-axis MC deliverable, whose sampling scatter dominated every bin below ~1 keV. Validated against the MC in `tests/test_muon_analytic.py`, never substituted for it silently. |
| `tests/test_cosmogenic_intrinsic.py:46` | Ge-intrinsic cosmogenic test fixture — supplies the extended deposit axis | **v2.0-ext**, explicit | ADDED 2026-07-25 (Ge-intrinsic 3H/68Ge/65Zn floor). Test-only call, same disposition as the capture-recoil fixture below: `cosmogenic_intrinsic.py` never calls `shared_energy_grid` — it takes the edge array as an argument — so this fixture is the single site, pinned explicitly to the extended axis the RoI lives on. |
| `tests/test_capture_recoil.py:33` | capture-recoil test fixture — supplies the extended recoil axis | **v2.0-ext**, explicit | ADDED 2026-07-23 (capture recoil spectrum). Test-only call: the `edges` fixture builds the 744-bin extended axis that `capture_recoil.recoil_spectrum` histograms onto. `capture_recoil.py` itself never calls `shared_energy_grid` — it takes the edge array as an argument — so this fixture is the single site, pinned explicitly to the extended axis the RoI lives on. |
| `src/qpd_potential/em_extended.py:178` | `em_extended.extended_grid()` | **v2.0-ext**, explicit | ADDED BY PLAN 15-02. The single place this module obtains the 744-bin axis; every emitted table's centres are the geometric means of these edges. |
| `src/qpd_potential/em_extended.py:198` | `bit_identity_probe` — v1.0 leg of the route test | **v1.0**, explicit | ADDED BY PLAN 15-02. The comparison leg. Pinned to v1.0 by definition: the probe asks whether the extended run's bins 160..743 reproduce the v1.0 run EXACTLY. |
| `src/qpd_potential/em_extended.py:199` | `bit_identity_probe` — extended leg of the route test | **v2.0-ext**, explicit | ADDED BY PLAN 15-02. The other leg. `np.array_equal(ext[160:], v1)` is asserted here, never `np.allclose`. |
| `src/qpd_potential/em_extended.py:442` | provenance header string | n/a — prose | Not a call site: the emitted tables' header text recording that the edge join is exact. Enumerated individually so the grep count stays auditable. |
| `src/qpd_potential/em_recoil.py:454` | `indicted_v1_bins` — the 584 frozen v1.0 bin centres | **v1.0**, explicit | ADDED BY PLAN 15-01. Counts how many PUBLISHED v1.0 bins lie below the Landau-Vavilov validity floor. Pinned to v1.0 by definition: the indictment is about the v1.0 bins. |
| `src/qpd_potential/em_recoil.py:456` | `indicted_v1_bins` — the 744 extended bin centres | **v2.0-ext**, explicit | ADDED BY PLAN 15-01. The same count over the extended axis, reported alongside so the two are not conflated. |
| `src/qpd_potential/em_recoil.py:751` | `validity_floor_rows` — extended bins below the Compton physical floor | **v2.0-ext**, explicit | ADDED BY PLAN 15-01. Counts the extended bins below the Ge pair-creation threshold for the frozen floor table. |
| `src/qpd_potential/em_recoil.py:752` | continuation of the same expression | **v2.0-ext**, explicit | ADDED BY PLAN 15-01. Second half of the geometric-mean expression on the preceding line; enumerated separately because the grep is line-based. |
| `tests/test_em_extended.py:101` | Plan 15-02 edge-join assertion | **v1.0**, explicit | ADDED BY PLAN 15-02. Asserts `np.array_equal(ext_edges[160:], v1_edges)` with max absolute difference exactly 0.0, which is what excludes the `fp-silent-reinterpolation` drift `np.allclose` would let through. |
| `tests/test_em_recoil.py:301` | Plan 15-01 S(x,Z) domain sweep | **v2.0-ext**, explicit | ADDED BY PLAN 15-01. Evaluates the incoherent scattering function at all 744 extended centres to show no interpolator raises anywhere on the extended axis. |

**Files edited by this plan to add a pin:** `muon_deposit.py`,
`compton_deposit.py`, `deposited_spectra.py`, `parse_endf_nGe.py`,
`tests/test_compton_channel.py`. **Phase-9 files were not touched**; Phase 9
pinned its own.

---

## 6. The decoupled deposit axis, and the precision floor it inherits

`response_matrix.load_E_dep_grid_eV()` parses `data/combined_dRdEdep.csv`, which
makes the response matrix's deposit axis **a function of an archived Phase-4
product**. That axis cannot be extended without re-running the Phase-4 Monte
Carlo, which is Phase 15's job. `E_dep_grid_from_shared_grid_eV(version)` adds a
grid-sourced route: centres are the geometric means of
`shared_energy_grid(version)` edges, keV -> eV. **The CSV parser is unchanged**,
so the archived provenance stays readable.

### Measured discrepancy between the two routes

```
max |grid - csv| / csv  =  4.917619e-07     (at index 320)
csv[0]   = 10.144970          (decimal round-trip through the CSV text)
exact[0] = 10.144972680282425 (geometric mean of the v1.0 edges)
```

This corroborates the independently-recorded Phase-4 figure in `GPD/STATE.md`
("centers = geometric means of shared_energy_grid() edges to 5e-7").

### Consequence for plan 10-04, stated plainly (`fp-bit-identical-promise`)

**The archived `artifacts/stage1/response_matrix_*.npz` were built on the CSV
round-tripped centres.** The regenerated matrices sit on the exact geometric
means. **Bit-identical reproduction of the archived matrices is therefore NOT
achievable, and plan 10-04 must not promise it.** Promising bit-identity would
either be false, or would force the new code to reproduce a precision-loss
artefact of a decimal text format.

Plan 10-04's comparison against the archived matrices is therefore **statistical**
(normalised by the archived per-cell Monte Carlo error), and its **bitwise** check
is against a *same-code* v1.0-range rebuild, which is a different and answerable
question.

---

## 7. The sub-seed: from ordinal index to deposit energy (`fp-ordinal-seed`)

**Before.** `build_matrix` did:

```python
ss = SeedSequence([seed, crc32(design), crc32(variant)])
child_seeds = ss.spawn(n_edep)
rng = default_rng(child_seeds[j])          # j is the ORDINAL INDEX
```

A column's sub-seed was a function of **how many columns sat below it**.
Prepending 160 sub-eV columns shifts every index and re-seeds every column above
10.14 eV.

**Demonstrated, not asserted.** The same deposit energy 57118.92025870707 eV sits
at index 300 on the 584-column axis and index 460 on the 744-column axis:

```
ORDINAL  584-axis col 300 first draws: [0.49813092 0.71201118 0.18689986]   spawn_key (300,)
ORDINAL  744-axis col 460 first draws: [0.74471769 0.32187198 0.87944215]   spawn_key (460,)
                                        -> DIFFERENT streams for the same physics
```

Every v1.0 comparison would then be pure Monte Carlo noise, and a real regression
of order that noise would be invisible.

**After.** `column_seed_sequence(seed, design, variant, E_dep_eV)` keys on the
deposit energy:

```python
key = zlib.crc32(("%.12e" % E_dep_eV).encode())
SeedSequence([seed, crc32(design), crc32(variant), key])
```

```
ENERGY-KEYED 584-axis: [0.20015866 0.67617383 0.17417598]
ENERGY-KEYED 744-axis: [0.20015866 0.67617383 0.17417598]   -> IDENTICAL
```

Verified for every 37th overlapping column, not just one. All **744 energy keys
are distinct** (adjacent centres differ by 2.9%, twelve significant digits
resolves them with enormous margin). Process stability is preserved by using
`zlib.crc32` and never Python's salted builtin `hash` --- the same reason the
original scheme used crc32 on the design and variant names.

**A deliberate consequence.** Twelve significant digits also resolves the
4.918e-07 CSV-vs-exact centre discrepancy, so the CSV-sourced and grid-sourced
axes produce **different** sub-seeds for the "same" column. That is correct and
intentional: they are different axes, and pretending otherwise is what
`fp-bit-identical-promise` forbids.

---

## 8. Scope discipline

- Nothing was written to `data/` or `artifacts/`.
  `test_no_frozen_artifact_was_modified_by_this_plan` enforces this with
  `git status --porcelain data/ artifacts/`.
- No matrix was regenerated. That is plan 10-04.
- The `E_rec` grid bounds (1e-3 to 1e5 eV, 20 bins/decade, underflow bin) are
  untouched --- only the **deposit** axis moved.
- `shared_energy_grid` returns **keV**, unchanged. Every eV figure in this note is
  a labelled conversion by 1e3.

---

## 9. Weakest points

1. **The floor is 0.0999350 eV, not 0.1 eV.** Section 3 owns that reading.
2. **The 4.918e-07 CSV round-trip discrepancy** means the archived v1.0 response
   matrices sit on a very slightly different axis from the exact one. Nothing
   downstream has ever depended on that difference, but plan 10-04's comparison
   against v1.0 inherits it as an irreducible floor beneath the Monte Carlo noise.
3. **Pinning the Phase-4 producers to v1.0 is a decision made here** on the
   grounds that Phase 15 owns the re-run. If Phase 15's scope changes, this pin
   has to be revisited.
4. **Preserving the v1.0 edge set is sufficient only for artifacts binned on
   `shared_energy_grid`.** Artifacts on their own native axes
   (`artifacts/stage1/cevns_dRdT.csv` from 5 eV,
   `data/endf_nGe_elastic_v1.1.csv` from thermal energies, the reactor flux tables
   on an E_nu axis) are unaffected by this construction and are handled by the
   plan 10-05 disposition register.
