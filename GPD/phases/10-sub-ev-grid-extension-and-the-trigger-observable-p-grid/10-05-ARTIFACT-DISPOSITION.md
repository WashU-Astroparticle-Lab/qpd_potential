# Plan 10-05 --- Archived-Artifact Disposition

**Phase:** 10 --- Sub-eV Grid Extension and the Trigger Observable (P-GRID)
**Discharges:** `claim-disposition`; ROADMAP Phase 10 success criterion 2 ---
*"Every archived v1.x spectrum is either re-gridded onto the extended axis or explicitly
tagged valid only above 10.14 eV; no legacy artifact is silently reinterpolated onto the
new grid."*

**Regime boundary.** `trigger.SUBEV_REGIME_BOUNDARY_eV` = **1 eV** (CONVENTIONS §I,
plan 10-02). Below it the reported observable is the **trigger probability**
P_trig(E_dep), **not** dR/dE_rec. This document imports that constant rather than
restating a literal.

---

## 1. The reading of "archived v1.x spectrum" this register adopts

Criterion 2 does not define whether **input tables on foreign axes** are in scope.
Two readings are available:

- **Narrow** --- only products binned on the shared deposited-energy grid: the three
  `*_dRdEdep.csv` files and the two response matrices. Five artifacts.
- **Wide** --- every tracked `.csv`/`.npz` artifact, including the CEvNS dR/dT table on
  its own recoil axis, the ENDF n-Ge table from thermal energies, and the reactor flux
  tables on an E_nu axis.

**This register adopts the WIDE reading.** The narrow one would leave untagged exactly
the artifacts a sub-eV plot is most likely to be silently extended through: the CEvNS
dR/dT table stops at 5 eV, and a spectrum drawn from it down to 0.1 eV would be pure
interpolation into a region that table never covered. Criterion 2's *purpose* is to
stop that; its *letter* does not name it. The wide reading is the one that serves the
purpose.

**Consequence, stated so it is not a surprise:** the register also contains rows for
artifacts that are not spectra at all (parameter tables, line lists, scalar registries).
Those carry the disposition `not_a_spectrum` with a reason, rather than being omitted,
because an omission is indistinguishable from an oversight.

## 2. The register is a SIDECAR, not an edit (`fp-header-rewrite`)

The frozen artifacts' own provenance headers carry recorded git SHAs and integrity
statements. Editing them to add validity tags would invalidate precisely the provenance
this register exists to protect. So the tags live in
`artifacts/v2.0/legacy_grid_disposition.csv` and `src/qpd_potential/legacy_grid.py`
reads them. `tests/test_legacy_grid_disposition.py::test_frozen_headers_were_not_rewritten`
enforces this with `git status --porcelain data/ artifacts/stage1/`.

## 3. The recorded enumeration command

```bash
git ls-files | grep -E '\.(csv|npz)$'
```

**29 tracked artifacts, 29 register rows.** Re-run by
`test_register_closure`, which fails if a newly added tracked `.csv`/`.npz` has no
disposition row --- that is the closure guard working, not a spurious failure.

Every bounded row's floor is **read from the frozen file at run time**, and
`test_register_floors_are_read_from_the_files_not_asserted` re-reads them and compares.

## 4. The disposition vocabulary (closed)

| Disposition | Meaning |
|---|---|
| `carried_onto_extended_axis_without_reinterpolation` | Binned on the shared v1.0 deposit grid. Values map bin-for-bin **by index** into bins 160–743 of the 744-bin extended axis, because plan 10-03 preserved the v1.0 edge array exactly. |
| `bounded_native_axis` | Lives on its own axis; valid only at or above its recorded floor. |
| `bounded_superseded` | Bounded, and replaced on the extended axis by a v2.0 product. |
| `native_to_extended_axis` | Produced **on** the extended axis; not a legacy artifact. |
| `not_a_spectrum` | A registry, line list, or coefficient table with no bins to re-grid. |

A row outside this vocabulary is a register **error**, not a default
(`legacy_grid.load_register` raises).

---

## 5. The carry, and why it is not a tautology

For the three shared-grid deposit spectra the carry is an **index operation**:

```python
out = np.full(744, np.nan)
out[160:] = v1_0_values          # NO interpolation of any kind
```

It is legitimate **only** because plan 10-03 made `np.array_equal(ext_edges[160:],
v1_0_edges)` true with maximum absolute difference exactly 0.0, so v1.0 bin *i* **is**
extended bin 160+*i*.

Asserting `out[160:] == v1_0_values` alone would be a tautology about array assignment.
So `test_carry_without_reinterpolation_is_bit_identical` checks **both halves**:

1. **the carry is exact** --- `np.array_equal`, max difference **0.0**; and
2. **the artifact really sits on those bins** --- 584 rows whose energy column matches
   the extended axis's centres 160–743 to within the recorded **4.918e-07** CSV
   round-trip precision.

Without (2), (1) would prove nothing.

**The lower 160 bins are filled with NaN, not zero.** This artifact carries **no data**
there; a zero would read as a measured absence rather than an absence of measurement.
**That absence is the tag, not a gap to fill** (`fp-silent-carry`).

## 6. A finding: the archived response matrices are **not** tagged "carried"

`artifacts/stage1/response_matrix_*.npz` are tagged `bounded_superseded`, not
`carried_onto_extended_axis_without_reinterpolation`, and the distinction is real.

Their deposit centres are the **CSV round-tripped** values parsed from
`data/combined_dRdEdep.csv`, which differ from the extended axis's exact geometric
means by up to **4.918e-07 relative** (plan 10-03). Placing those matrices on the
extended axis would therefore be a genuine --- if tiny --- re-mapping, **not** an index
copy. Calling it "carried" would be exactly the silent reinterpolation criterion 2
forbids, at the 5e-7 level.

They remain the frozen v1.0 comparison baseline, are loaded directly by
`notebooks/paper_calculations.ipynb`, and are superseded on the extended axis by
`artifacts/v2.0/response_matrix_*_ext.npz` (plan 10-04).

`test_response_matrices_are_NOT_tagged_carried` pins this, including a direct
`np.array_equal(csv_axis, exact_axis) == False` check.

## 7. The guard raises; it does not clamp

Same discipline as plan 10-01. `legacy_grid.check_evaluation_point` raises
`LegacyArtifactError` --- reporting the offending value, the floor, the artifact's
native axis and units, and its disposition --- rather than returning a clamped,
extrapolated, or zero value. Arrays are rejected wholesale, never masked or filtered.
Non-finite input is itself out of domain.

```
artifacts/stage1/cevns_dRdT.csv: evaluation at [0.1] [eV] is BELOW the recorded
validity floor 5.0 [eV]. Native axis: own CEvNS nuclear-recoil grid (320 points).
Disposition: bounded_native_axis. Below its own floor this artifact HAS NO DATA --
a value here would be whatever an interpolation invented ...
```

---

## 8. The register

| Artifact | Native axis | Units | Validity floor | Disposition | Reason |
|---|---|---|---|---|---|
| `artifacts/stage1/cevns_dRdT.csv` | own CEvNS nuclear-recoil grid (320 points) | eV | 5 | `bounded_native_axis` | Not on the shared deposit grid. Its recoil axis starts at its own floor and it carries NO DATA below it. Extending a spectrum plot down to 0.1 eV from this table would be pure interpolation into a region the table never covered (fp-silent-carry). |
| `artifacts/stage1/reconstructed_spectra_AlHf.csv` | Al->Hf RECONSTRUCTED-energy axis (Phase-6 fold output) | keV | 1.05925e-06 | `bounded_native_axis` | A reconstructed-energy spectrum, not a deposited-energy one, so the shared-grid extension does not apply to it at all. It is bounded below by its own first E_rec point and is superseded for sub-eV work by whatever Phases 12-15 fold through the artifacts/v2.0 matrices. |
| `artifacts/stage1/reconstructed_spectra_TaAl.csv` | Ta->Al RECONSTRUCTED-energy axis (Phase-6 fold output) | keV | 1.05925e-06 | `bounded_native_axis` | A reconstructed-energy spectrum, not a deposited-energy one, so the shared-grid extension does not apply to it at all. It is bounded below by its own first E_rec point and is superseded for sub-eV work by whatever Phases 12-15 fold through the artifacts/v2.0 matrices. |
| `artifacts/stage1/response_matrix_AlHf.npz` | Al->Hf deposit axis parsed from data/combined_dRdEdep.csv (584 centres) | eV | 10.145 | `bounded_superseded` | NOT tagged 'carried'. Its deposit centres are the CSV ROUND-TRIPPED values, which differ from the extended axis's exact geometric means by up to 4.918e-07 relative (plan 10-03). Placing this matrix on the extended axis would therefore be a genuine though tiny re-mapping, not an index copy. Valid only at or above its own first centre; SUPERSEDED on the extended axis by artifacts/v2.0/response_matrix_*_ext.npz (plan 10-04). Remains the frozen v1.0 comparison baseline and is loaded directly by notebooks/paper_calculations.ipynb, so it must never be overwritten. |
| `artifacts/stage1/response_matrix_TaAl.npz` | Ta->Al deposit axis parsed from data/combined_dRdEdep.csv (584 centres) | eV | 10.145 | `bounded_superseded` | NOT tagged 'carried'. Its deposit centres are the CSV ROUND-TRIPPED values, which differ from the extended axis's exact geometric means by up to 4.918e-07 relative (plan 10-03). Placing this matrix on the extended axis would therefore be a genuine though tiny re-mapping, not an index copy. Valid only at or above its own first centre; SUPERSEDED on the extended axis by artifacts/v2.0/response_matrix_*_ext.npz (plan 10-04). Remains the frozen v1.0 comparison baseline and is loaded directly by notebooks/paper_calculations.ipynb, so it must never be overwritten. |
| `artifacts/v2.0/response_matrix_AlHf_ext.npz` | Al->Hf deposit axis = shared_energy_grid('v2.0-ext') geometric means (744 centres) | eV | 0.101384 | `native_to_extended_axis` | Produced by plan 10-04 ON the extended axis. Not a legacy artifact. Carries its own provenance header including the linear-quasiparticle-yield caveat: below ~1 eV this matrix is a mean-field extrapolation two decades below where the chain was validated. |
| `artifacts/v2.0/response_matrix_TaAl_ext.npz` | Ta->Al deposit axis = shared_energy_grid('v2.0-ext') geometric means (744 centres) | eV | 0.101384 | `native_to_extended_axis` | Produced by plan 10-04 ON the extended axis. Not a legacy artifact. Carries its own provenance header including the linear-quasiparticle-yield caveat: below ~1 eV this matrix is a mean-field extrapolation two decades below where the chain was validated. |
| `data/activation_scenario_v1.1.csv` | named budget/scenario quantities (registry table) | mixed, per row | — | `not_a_spectrum` | A budget/scenario registry of named scalar quantities, not a binned spectrum on any energy axis. No re-gridding operation applies and no energy validity floor exists. |
| `data/ambient_neutron_flux_v1.1.csv` | neutron energy | MeV | 0.01 | `bounded_native_axis` | PHASE 9 ARTIFACT, enumerated here for register closure but owned by Phase 9. A neutron flux on its own energy axis, deliberately NOT shared_energy_grid(); Phase 10 does not touch it. Bounded by its own tabulated span. |
| `data/ambient_neutron_thermal_v2.0.csv` | neutron energy | eV | 1e-05 | `bounded_native_axis` | PHASE 9 ARTIFACT, enumerated here for register closure but owned by Phase 9. A neutron flux on its own energy axis, deliberately NOT shared_energy_grid(); Phase 10 does not touch it. Bounded by its own tabulated span. |
| `data/combined_dRdEdep.csv` | shared deposited-energy grid v1.0 (584 bin centres) | keV | 0.010145 | `carried_onto_extended_axis_without_reinterpolation` | Binned on shared_energy_grid('v1.0'). Plan 10-03 preserved the v1.0 edge array EXACTLY (np.array_equal, max difference 0.0), so v1.0 bin i IS extended bin 160+i: the values map bin for bin by INDEX, with no interpolation of any kind. The lower 160 bins of the extended axis carry NO DATA for this artifact -- that absence is the tag, not a gap to fill. Re-running the Phase-4 deposit Monte Carlo onto the extended axis is Phase 15's job. |
| `data/compton_dRdEdep.csv` | shared deposited-energy grid v1.0 (584 bin centres) | keV | 0.010145 | `carried_onto_extended_axis_without_reinterpolation` | Binned on shared_energy_grid('v1.0'). Plan 10-03 preserved the v1.0 edge array EXACTLY (np.array_equal, max difference 0.0), so v1.0 bin i IS extended bin 160+i: the values map bin for bin by INDEX, with no interpolation of any kind. The lower 160 bins of the extended axis carry NO DATA for this artifact -- that absence is the tag, not a gap to fill. Re-running the Phase-4 deposit Monte Carlo onto the extended axis is Phase 15's job. |
| `data/endf/nGe_elastic_per_isotope.csv` | ENDF per-isotope neutron-energy grid | eV | 1.03125e-05 | `bounded_native_axis` | Intermediate per-isotope table feeding data/endf_nGe_elastic_v1.1.csv. Same axis, same bound, same reasoning. |
| `data/endf_nGe_elastic_v1.1.csv` | ENDF/B-VIII.0 neutron-energy union grid | eV | 1.03125e-05 | `bounded_native_axis` | Neutron incident energy, not deposited energy. Its floor is thermal and it is unaffected by the deposit-axis extension. Guarded separately: parse_endf_nGe.loglog_interp returns NaN rather than clamping outside the span (plan 10-01 inventory, residual finding 2). |
| `data/external/nucleus2019_fig1_ge.csv` | digitized NUCLEUS Fig. 1 recoil axis | eV | 1.02049 | `bounded_native_axis` | A DIGITIZED FIGURE. There is nothing outside its span to extrapolate from, so no declared extension could ever be witnessed. cevns._interp_loglog now raises outside it (plan 10-01). |
| `data/flux/hm_coefficients.csv` | Huber-Mueller polynomial coefficient index | dimensionless | — | `not_a_spectrum` | A coefficient table, not a spectrum: its first column indexes isotope/order, not energy. It has no energy axis to be re-gridded onto and no validity floor in energy. |
| `data/flux/huber_U235_benchmark.csv` | antineutrino energy E_nu | MeV | 2 | `bounded_native_axis` | A reactor antineutrino FLUX table on an E_nu axis. Nothing in Phase 10 touches the neutrino energy axis, and the deposited-energy extension cannot reach it. Bounded by its own tabulated span; cevns.ReactorFlux now RAISES outside that span (plan 10-01) rather than returning NaN or a clamped band. |
| `data/flux/ncapture_238U.csv` | antineutrino energy E_nu | MeV | 0.1 | `bounded_native_axis` | A reactor antineutrino FLUX table on an E_nu axis. Nothing in Phase 10 touches the neutrino energy axis, and the deposited-energy extension cannot reach it. Bounded by its own tabulated span; cevns.ReactorFlux now RAISES outside that span (plan 10-01) rather than returning NaN or a clamped band. |
| `data/flux/perfission_spectrum.csv` | antineutrino energy E_nu | MeV | 0.1 | `bounded_native_axis` | A reactor antineutrino FLUX table on an E_nu axis. Nothing in Phase 10 touches the neutrino energy axis, and the deposited-energy extension cannot reach it. Bounded by its own tabulated span; cevns.ReactorFlux now RAISES outside that span (plan 10-01) rather than returning NaN or a clamped band. |
| `data/flux/reactor_flux_billard_variant.csv` | antineutrino energy E_nu | MeV | 0.1 | `bounded_native_axis` | A reactor antineutrino FLUX table on an E_nu axis. Nothing in Phase 10 touches the neutrino energy axis, and the deposited-energy extension cannot reach it. Bounded by its own tabulated span; cevns.ReactorFlux now RAISES outside that span (plan 10-01) rather than returning NaN or a clamped band. |
| `data/flux/reactor_flux_v1.0.csv` | antineutrino energy E_nu | MeV | 0.1 | `bounded_native_axis` | A reactor antineutrino FLUX table on an E_nu axis. Nothing in Phase 10 touches the neutrino energy axis, and the deposited-energy extension cannot reach it. Bounded by its own tabulated span; cevns.ReactorFlux now RAISES outside that span (plan 10-01) rather than returning NaN or a clamped band. |
| `data/flux/summation_spectra.csv` | antineutrino energy E_nu | MeV | 0.1 | `bounded_native_axis` | A reactor antineutrino FLUX table on an E_nu axis. Nothing in Phase 10 touches the neutrino energy axis, and the deposited-energy extension cannot reach it. Bounded by its own tabulated span; cevns.ReactorFlux now RAISES outside that span (plan 10-01) rather than returning NaN or a clamped band. |
| `data/gamma_lines.csv` | discrete gamma-line energies (16 lines) | keV | — | `not_a_spectrum` | A DISCRETE LINE LIST, not a binned spectrum. It has no bins to re-grid. Its energies are the witnesses for the plan 10-01 mu/rho declared-domain extension (241.997-2614.511 keV). |
| `data/ge_incoherent_S.csv` | momentum-transfer variable x (145 points) | 1/Angstrom | 0.001 | `bounded_native_axis` | A frozen PHYSICS PARAMETER TABLE on its own abscissa, not a spectrum on the deposit grid. Its evaluation bounds are already declared and enforced by src/qpd_potential/interp_guard.py (plan 10-01); this register records the same floor so both routes agree. |
| `data/ge_xcom_mu.csv` | NIST XCOM photon energy (4 points) | MeV | 0.6 | `bounded_native_axis` | A frozen PHYSICS PARAMETER TABLE on its own abscissa, not a spectrum on the deposit grid. Its evaluation bounds are already declared and enforced by src/qpd_potential/interp_guard.py (plan 10-01); this register records the same floor so both routes agree. |
| `data/muon_dRdEdep.csv` | shared deposited-energy grid v1.0 (584 bin centres) | keV | 0.010145 | `carried_onto_extended_axis_without_reinterpolation` | Binned on shared_energy_grid('v1.0'). Plan 10-03 preserved the v1.0 edge array EXACTLY (np.array_equal, max difference 0.0), so v1.0 bin i IS extended bin 160+i: the values map bin for bin by INDEX, with no interpolation of any kind. The lower 160 bins of the extended axis carry NO DATA for this artifact -- that absence is the tag, not a gap to fill. Re-running the Phase-4 deposit Monte Carlo onto the extended axis is Phase 15's job. |
| `data/radiopurity_budget_v1.1.csv` | named budget/scenario quantities (registry table) | mixed, per row | — | `not_a_spectrum` | A budget/scenario registry of named scalar quantities, not a binned spectrum on any energy axis. No re-gridding operation applies and no energy validity floor exists. |
| `data/surface_environment_v2.0.csv` | named environment quantities (registry table) | mixed, per row | — | `not_a_spectrum` | PHASE 9 ARTIFACT, enumerated for closure. A registry of named scalar environment quantities, not a binned spectrum: it has no single energy axis and no re-gridding operation applies. |
| `data/wafer_self_veto.csv` | named acceptance quantities (registry table) | mixed, per row | — | `not_a_spectrum` | A registry of named scalar quantities (acceptances, rates, catalogued verdict strings), not a binned spectrum. The muon deposit spectrum it derives from IS registered separately as data/muon_dRdEdep.csv. |

---

## 9. Weakest points of this register

1. **The wide/narrow reading is a judgement call.** Section 1 states which was adopted
   and why. A reader who takes criterion 2 to mean only shared-grid products would find
   24 of these 29 rows unnecessary. They are not harmful, but they are not compelled by
   the criterion's letter.
2. **`not_a_spectrum` is the weakest tag.** It records that no re-gridding operation
   applies, which is true, but it provides no guard: nothing stops a downstream reader
   from misusing a scalar registry. The tag is a statement, not an enforcement.
3. **Closure is coupled to a concurrently-executing phase.** Phase 9 added
   `data/ambient_neutron_thermal_v2.0.csv` and `data/surface_environment_v2.0.csv` to
   the tracked set while this plan ran; both are enumerated and tagged here. If Phase 9
   adds another tracked `.csv` after this commit, `test_register_closure` will fail
   until a row is added. That is the guard behaving correctly, but it does couple the
   two phases' test suites.
4. **The floors are first-tabulated-abscissa values, not validated support limits.**
   `artifacts/stage1/reconstructed_spectra_*.csv` have a floor of 1.059254e-06 keV
   simply because that is where their E_rec axis starts; that is a grid property, not a
   statement that the spectrum is trustworthy there.

## 10. UNRESOLVED --- one live occurrence this plan is forbidden to fix

`grep -rn -i "below 10 eV"` finds the retracted display rule still stated as a **live
instruction** in one place this plan may not touch:

```
paper/HANDOFF.md:33: - **Display rule: nothing below 10 eV** on any figure
                       (memory `plot-energy-floor-10ev`; enforced in
                       src/qpd_potential/fold.py xlim). Keep this for any
                       new/regenerated figure.
```

Plan 10-05's scope explicitly forbids editing anything under `paper/`, and its own
verification step requires that `git diff` touch no file there. So this occurrence is
**recorded, not fixed**, and `claim-labelling` is reported as **partial** rather than
passed.

It also contains a second staleness: it says the rule is "enforced in
`src/qpd_potential/fold.py` xlim". Plan 10-05 rewrote that comment. The 1e-2 keV low
limit in `fold.make_spectra_figure` survives, but it is now documented as **the support
floor of the v1.0 artifacts that figure draws** --- `reconstructed_spectra_*.csv` and
the frozen response matrices have no data below 10.14 eV, and plotting below a table's
own floor is silent extrapolation --- **not** as the retracted display rule. The v1.0
figure's axis was deliberately not changed: changing it would alter a v1.0 deliverable,
and Phases 12–15 own the v2.0 figures on the extended axis.

**Follow-up owed:** `paper/HANDOFF.md` line 33 must be updated by whoever next has the
paper in scope.

### Occurrences reviewed and left as history by location

`GPD/milestones/v1.0/**` and `GPD/milestones/v1.1/**` are **closed milestone archives**.
They record what the project believed when those milestones closed and are not live
statements; they are deliberately not rewritten. `GPD/ROADMAP.md`,
`GPD/REQUIREMENTS.md` and `GPD/literature/SUMMARY.md` already carried the retraction
before this plan ran.

### Occurrences this plan converted from live to dated history

| File | Was | Now |
|---|---|---|
| `notebooks/paper_calculations.ipynb` (final cell) | printed *"Nothing below 10 eV is displayed on any spectrum (project display rule)."* | prints a dated **RETRACTED 2026-07-22** line, the 100 meV floor, the 744-bin grid parameters, and the 1 eV regime boundary imported from `trigger.SUBEV_REGIME_BOUNDARY_eV` |
| `src/qpd_potential/fold.py` (`make_spectra_figure`) | *"Do NOT display anything below 10 eV … (user directive)"* | dated retraction, plus the real reason the v1.0 figure's axis stops where it does |
| `GPD/literature/PITFALLS.md` | live pitfall entry | marked `[RETRACTED 2026-07-22 … history, not a live rule]` |
| `GPD/literature/COMPUTATIONAL.md` | *"the project carries a standing instruction"* | *"the project **carried** (until its retraction on 2026-07-22 — this sentence is history, not a live rule)"* |
| `GPD/literature/METHODS.md` | quoted as a standing rule | marked `[RETRACTED 2026-07-22; quoted as history]` |

---

## 11. The regime label these deliverables carry

Every sub-eV deliverable of this phase imports the boundary from
`trigger.SUBEV_REGIME_BOUNDARY_eV` = **1 eV** rather than restating a literal, and
states: **below it the reported observable is the trigger probability P_trig(E_dep),
not dR/dE_rec.**
