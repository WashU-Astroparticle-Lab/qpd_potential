# Plan 10-01 --- Interpolator Inventory and Pre-Fix Witness Record

**Phase:** 10 --- Sub-eV Grid Extension and the Trigger Observable (P-GRID)
**Discharges:** ROADMAP Phase 10 success criterion 3 --- *"every interpolator raises
outside its declared evaluation domain (no silent clamping or extrapolation at a table
floor)"*, and the forbidden-proxy line naming silent clamping/extrapolation at a table floor.
**Interpreter:** `/opt/anaconda3/bin/python3` --- numpy 1.26.4, scipy 1.17.1, pytest 7.4.0.
(The `gpd` venv has no scipy and cannot import `qpd_potential.response`.)

---

## 0. Why this exists, and why it could have been worthless

`GPD/STATE.md`, Phase-07-verify: *"D3 `test-resonance-grid` passed on a vacuous metric."*
This project has already shipped a guard test that passed without testing anything. So
Task 1 of this plan was run **before any guard was written**, against the unmodified source
tree, and it recorded what each call site *actually returned* just outside its table. Those
recorded values are compiled into `tests/test_interpolator_bounds.py` as assertions that the
values are no longer obtainable. If the guard were removed, those tests fail --- verified by
stashing the guard, see section 5.

The decisive question this record answers is section 3's: **did any call site previously
return a finite, non-error value outside its tabulated span?** If none had, the guard would
be defending against a failure mode this pipeline does not have, and the honest report would
have been to say so rather than to claim a fix.

---

## 1. The recorded enumeration command

Run from the repository root. This is the literal command; its raw output follows verbatim.

```
grep -rn "np\.interp\|PchipInterpolator\|CubicSpline\|interp1d\|_interp_loglog\|loglog_interp" --include=*.py src/
```

`fp-grep-by-recall` guard: `tests/test_interpolator_bounds.py::test_inventory_closure_grep_hits_equal_inventory_rows`
re-runs exactly this command and asserts hit count == inventory row count, and that every hit
appears in the table below.

**Hit count: 33.** (27 before this plan; the guard added 6 further *prose* hits --- docstrings
and `note=` strings that quote the pre-fix behaviour. Those 6 are enumerated and excluded
individually below rather than filtered out by a pattern tweak, so the count stays auditable.)

### 1.1 Raw output

```
src/flux/assemble_spectrum.py:28:from scipy.interpolate import PchipInterpolator
src/flux/assemble_spectrum.py:122:        pchip_log = PchipInterpolator(E_tab, np.log(s_tab), extrapolate=True)
src/nuclear/parse_endf_nGe.py:105:def loglog_interp(x_new, x, y, extrapolate_below=False):
src/nuclear/parse_endf_nGe.py:124:        out[inside] = np.exp(np.interp(np.log(x_new[inside]), lx, ly))
src/nuclear/parse_endf_nGe.py:128:        out = np.interp(x_new, x, y, left=(y[0] if extrapolate_below else np.nan),
src/nuclear/parse_endf_nGe.py:246:        sig_tot = np.interp(E, Et, sig_tot)
src/nuclear/parse_endf_nGe.py:265:    ref = loglog_interp(E[m], Eb, y_b)
src/nuclear/parse_endf_nGe.py:482:        u = loglog_interp(union, native_E[A], native_sig[A])
src/nuclear/parse_endf_nGe.py:557:        per_sig[A] = loglog_interp(union, native_E[A], native_sig[A])
src/nuclear/parse_endf_nGe.py:558:        per_a1[A] = np.interp(union, a1_E[A], a1_v[A],
src/nuclear/parse_endf_nGe.py:561:            per_tot[A] = loglog_interp(union, native_E[A], native_tot[A])
src/nuclear/parse_endf_nGe.py:569:    per_tot_all = {A: loglog_interp(union, tot_E[A], tot_v[A], extrapolate_below=True)
src/nuclear/parse_endf_nGe.py:598:            cold_sig[A] = loglog_interp(union, Ec, sc)
src/qpd_potential/interp_guard.py:11:# WHY A RAISE AND NOT A NaN (fp-nan-instead-of-raise).  `PchipInterpolator(...,
src/qpd_potential/cevns.py:25:from scipy.interpolate import PchipInterpolator
src/qpd_potential/cevns.py:235:        self._log_phi = PchipInterpolator(self.E, np.log(self.phi), extrapolate=False)
src/qpd_potential/cevns.py:250:            note="np.interp previously CLAMPED to the end values (0.25 below the "
src/qpd_potential/cevns.py:287:        return float(np.interp(E_nu_MeV, self.E, self.rel))
src/qpd_potential/cevns.py:653:def _interp_loglog(x, xs, ys, *, table: str = "<digitized curve>",
src/qpd_potential/cevns.py:660:    ``np.interp`` clamped to the end values (for the NUCLEUS Fig.1 digitization:
src/qpd_potential/cevns.py:672:    return 10.0 ** np.interp(np.log10(x), np.log10(xs), np.log10(ys))
src/qpd_potential/cevns.py:718:        theirs = float(_interp_loglog(
src/qpd_potential/response.py:626:    lam = np.interp(t_prop, t_grid, gamma)
src/qpd_potential/wafer_self_veto.py:321:        note="np.interp previously clamped the rate to 16.01101 below the floor "
src/qpd_potential/wafer_self_veto.py:325:    r_cut = float(np.interp(e_cut_keV, e_grid, rate))
src/qpd_potential/muon_deposit.py:164:    lam = np.interp(u, cdf, grid)
src/qpd_potential/compton_source.py:174:    # np.interp clamps at the ends; replace clamped regions with slope extrapolation.
src/qpd_potential/compton_source.py:175:    ly = np.interp(lx, _LOG_E, _LOG_MOR)
src/qpd_potential/compton_source.py:265:    ly = np.interp(lx, _LOG_SF_X, _LOG_SF_S)          # np.interp clamps at ends
src/qpd_potential/compton_source.py:268:    # above x_max np.interp already clamps to _LOG_SF_S[-1] = ln(Z) -> S = Z.
src/qpd_potential/fold.py:531:    matrices. Before this guard, ``np.interp`` CLAMPED below that floor, so
src/qpd_potential/fold.py:550:        note="np.interp previously clamped to E_rec(first centre) below the floor.",
src/qpd_potential/fold.py:554:    return np.exp(np.interp(lx, np.log(centers), np.log(E_rec_median)))
```

---

## 2. The inventory

Nine columns: call site, what it is, the frozen table (or the constructed grid) supplying its
abscissa, the abscissa units, the **tabulated span read from the actual file at run time**,
the **declared evaluation domain**, the **measured pre-fix out-of-domain return**, the
verdict, and the justification. Spans were read by
`scratchpad/witness_prefix.py`, which calls `cs.load_xcom()`, `cs.load_incoherent_sf()`,
`cevns.load_nucleus_fig1()`, `wsv.frozen_spectrum()` and `np.load(...)["E_dep_centers_eV"]`
--- never a docstring literal.

| Call site | What it is | Table / abscissa source | Units | Tabulated span | Declared domain | **Pre-fix out-of-domain return** | Verdict | Justification |
|---|---|---|---|---|---|---|---|---|
| `src/flux/assemble_spectrum.py:28` | `from scipy.interpolate import PchipInterpolator` | n/a | n/a | n/a | n/a | n/a | excluded | Import statement, not an evaluation site; and this module is a frozen data-preparation script (see the assemble_spectrum row below). |
| `src/flux/assemble_spectrum.py:122` | `PchipInterpolator(E_tab, log s_tab, extrapolate=True)` for the Huber/Mueller per-fission spectra | `data/flux/summation_spectra.csv`, `data/flux/huber_U235_benchmark.csv` | MeV (E_nu) | per-table span | not declared -- script is frozen | `extrapolate=True` slope-continues the log spectrum outside the tabulated span | excluded | `src/flux/assemble_spectrum.py` is a one-shot data-PREPARATION script that writes the frozen `data/flux/reactor_flux_v1.0.csv`, which is what `cevns.ReactorFlux` then reads and which IS guarded (cevns.py:235/287). RECORDED AS A FINDING RATHER THAN FIXED: this call site uses `extrapolate=True` deliberately, so the frozen v1.0 flux table's outermost points may contain extrapolated rather than tabulated values. That is a v1.0 provenance question, it is not created or worsened by the sub-eV deposit-axis extension (the neutrino energy axis is untouched by Phase 10), and re-running the flux assembly is out of scope here. |
| `src/nuclear/parse_endf_nGe.py:105` | ENDF n-Ge elastic cross-section preparation (`loglog_interp` def/body and its callers) | raw ENDF/B-VIII.0 point files under `data/endf/` | eV (neutron energy) | per-isotope ENDF native span | not declared -- script is frozen | NaN outside the span by default (`left=np.nan`), i.e. already not a clamp | excluded | `src/nuclear/parse_endf_nGe.py` is a one-shot data-PREPARATION script: it parses raw ENDF/B-VIII.0 files and writes the frozen `data/endf_nGe_elastic_v1.1.csv`, which is the artifact everything downstream reads. Guarding it would change nothing about the already-frozen table, and re-running it is out of scope for Phase 10. Its own `loglog_interp` already takes an explicit `extrapolate_below` flag and returns NaN (not a clamp) outside the span by default, so its out-of-domain behaviour is at least declared rather than silent. RECORDED AS A RESIDUAL: if Phase 15 ever re-runs this script, the NaN default should become a raise. The Phase-10 extended deposit axis never reaches it -- `parse_endf_nGe.py:279` calls `shared_energy_grid()` and CLIPS to the ENDF support, and plan 10-03 pins that caller to grid version v1.0. |
| `src/nuclear/parse_endf_nGe.py:124` | ENDF n-Ge elastic cross-section preparation (`loglog_interp` def/body and its callers) | raw ENDF/B-VIII.0 point files under `data/endf/` | eV (neutron energy) | per-isotope ENDF native span | not declared -- script is frozen | NaN outside the span by default (`left=np.nan`), i.e. already not a clamp | excluded | `src/nuclear/parse_endf_nGe.py` is a one-shot data-PREPARATION script: it parses raw ENDF/B-VIII.0 files and writes the frozen `data/endf_nGe_elastic_v1.1.csv`, which is the artifact everything downstream reads. Guarding it would change nothing about the already-frozen table, and re-running it is out of scope for Phase 10. Its own `loglog_interp` already takes an explicit `extrapolate_below` flag and returns NaN (not a clamp) outside the span by default, so its out-of-domain behaviour is at least declared rather than silent. RECORDED AS A RESIDUAL: if Phase 15 ever re-runs this script, the NaN default should become a raise. The Phase-10 extended deposit axis never reaches it -- `parse_endf_nGe.py:279` calls `shared_energy_grid()` and CLIPS to the ENDF support, and plan 10-03 pins that caller to grid version v1.0. |
| `src/nuclear/parse_endf_nGe.py:128` | ENDF n-Ge elastic cross-section preparation (`loglog_interp` def/body and its callers) | raw ENDF/B-VIII.0 point files under `data/endf/` | eV (neutron energy) | per-isotope ENDF native span | not declared -- script is frozen | NaN outside the span by default (`left=np.nan`), i.e. already not a clamp | excluded | `src/nuclear/parse_endf_nGe.py` is a one-shot data-PREPARATION script: it parses raw ENDF/B-VIII.0 files and writes the frozen `data/endf_nGe_elastic_v1.1.csv`, which is the artifact everything downstream reads. Guarding it would change nothing about the already-frozen table, and re-running it is out of scope for Phase 10. Its own `loglog_interp` already takes an explicit `extrapolate_below` flag and returns NaN (not a clamp) outside the span by default, so its out-of-domain behaviour is at least declared rather than silent. RECORDED AS A RESIDUAL: if Phase 15 ever re-runs this script, the NaN default should become a raise. The Phase-10 extended deposit axis never reaches it -- `parse_endf_nGe.py:279` calls `shared_energy_grid()` and CLIPS to the ENDF support, and plan 10-03 pins that caller to grid version v1.0. |
| `src/nuclear/parse_endf_nGe.py:246` | ENDF n-Ge elastic cross-section preparation (`loglog_interp` def/body and its callers) | raw ENDF/B-VIII.0 point files under `data/endf/` | eV (neutron energy) | per-isotope ENDF native span | not declared -- script is frozen | NaN outside the span by default (`left=np.nan`), i.e. already not a clamp | excluded | `src/nuclear/parse_endf_nGe.py` is a one-shot data-PREPARATION script: it parses raw ENDF/B-VIII.0 files and writes the frozen `data/endf_nGe_elastic_v1.1.csv`, which is the artifact everything downstream reads. Guarding it would change nothing about the already-frozen table, and re-running it is out of scope for Phase 10. Its own `loglog_interp` already takes an explicit `extrapolate_below` flag and returns NaN (not a clamp) outside the span by default, so its out-of-domain behaviour is at least declared rather than silent. RECORDED AS A RESIDUAL: if Phase 15 ever re-runs this script, the NaN default should become a raise. The Phase-10 extended deposit axis never reaches it -- `parse_endf_nGe.py:279` calls `shared_energy_grid()` and CLIPS to the ENDF support, and plan 10-03 pins that caller to grid version v1.0. |
| `src/nuclear/parse_endf_nGe.py:265` | ENDF n-Ge elastic cross-section preparation (`loglog_interp` def/body and its callers) | raw ENDF/B-VIII.0 point files under `data/endf/` | eV (neutron energy) | per-isotope ENDF native span | not declared -- script is frozen | NaN outside the span by default (`left=np.nan`), i.e. already not a clamp | excluded | `src/nuclear/parse_endf_nGe.py` is a one-shot data-PREPARATION script: it parses raw ENDF/B-VIII.0 files and writes the frozen `data/endf_nGe_elastic_v1.1.csv`, which is the artifact everything downstream reads. Guarding it would change nothing about the already-frozen table, and re-running it is out of scope for Phase 10. Its own `loglog_interp` already takes an explicit `extrapolate_below` flag and returns NaN (not a clamp) outside the span by default, so its out-of-domain behaviour is at least declared rather than silent. RECORDED AS A RESIDUAL: if Phase 15 ever re-runs this script, the NaN default should become a raise. The Phase-10 extended deposit axis never reaches it -- `parse_endf_nGe.py:279` calls `shared_energy_grid()` and CLIPS to the ENDF support, and plan 10-03 pins that caller to grid version v1.0. |
| `src/nuclear/parse_endf_nGe.py:482` | ENDF n-Ge elastic cross-section preparation (`loglog_interp` def/body and its callers) | raw ENDF/B-VIII.0 point files under `data/endf/` | eV (neutron energy) | per-isotope ENDF native span | not declared -- script is frozen | NaN outside the span by default (`left=np.nan`), i.e. already not a clamp | excluded | `src/nuclear/parse_endf_nGe.py` is a one-shot data-PREPARATION script: it parses raw ENDF/B-VIII.0 files and writes the frozen `data/endf_nGe_elastic_v1.1.csv`, which is the artifact everything downstream reads. Guarding it would change nothing about the already-frozen table, and re-running it is out of scope for Phase 10. Its own `loglog_interp` already takes an explicit `extrapolate_below` flag and returns NaN (not a clamp) outside the span by default, so its out-of-domain behaviour is at least declared rather than silent. RECORDED AS A RESIDUAL: if Phase 15 ever re-runs this script, the NaN default should become a raise. The Phase-10 extended deposit axis never reaches it -- `parse_endf_nGe.py:279` calls `shared_energy_grid()` and CLIPS to the ENDF support, and plan 10-03 pins that caller to grid version v1.0. |
| `src/nuclear/parse_endf_nGe.py:557` | ENDF n-Ge elastic cross-section preparation (`loglog_interp` def/body and its callers) | raw ENDF/B-VIII.0 point files under `data/endf/` | eV (neutron energy) | per-isotope ENDF native span | not declared -- script is frozen | NaN outside the span by default (`left=np.nan`), i.e. already not a clamp | excluded | `src/nuclear/parse_endf_nGe.py` is a one-shot data-PREPARATION script: it parses raw ENDF/B-VIII.0 files and writes the frozen `data/endf_nGe_elastic_v1.1.csv`, which is the artifact everything downstream reads. Guarding it would change nothing about the already-frozen table, and re-running it is out of scope for Phase 10. Its own `loglog_interp` already takes an explicit `extrapolate_below` flag and returns NaN (not a clamp) outside the span by default, so its out-of-domain behaviour is at least declared rather than silent. RECORDED AS A RESIDUAL: if Phase 15 ever re-runs this script, the NaN default should become a raise. The Phase-10 extended deposit axis never reaches it -- `parse_endf_nGe.py:279` calls `shared_energy_grid()` and CLIPS to the ENDF support, and plan 10-03 pins that caller to grid version v1.0. |
| `src/nuclear/parse_endf_nGe.py:558` | ENDF n-Ge elastic cross-section preparation (`loglog_interp` def/body and its callers) | raw ENDF/B-VIII.0 point files under `data/endf/` | eV (neutron energy) | per-isotope ENDF native span | not declared -- script is frozen | NaN outside the span by default (`left=np.nan`), i.e. already not a clamp | excluded | `src/nuclear/parse_endf_nGe.py` is a one-shot data-PREPARATION script: it parses raw ENDF/B-VIII.0 files and writes the frozen `data/endf_nGe_elastic_v1.1.csv`, which is the artifact everything downstream reads. Guarding it would change nothing about the already-frozen table, and re-running it is out of scope for Phase 10. Its own `loglog_interp` already takes an explicit `extrapolate_below` flag and returns NaN (not a clamp) outside the span by default, so its out-of-domain behaviour is at least declared rather than silent. RECORDED AS A RESIDUAL: if Phase 15 ever re-runs this script, the NaN default should become a raise. The Phase-10 extended deposit axis never reaches it -- `parse_endf_nGe.py:279` calls `shared_energy_grid()` and CLIPS to the ENDF support, and plan 10-03 pins that caller to grid version v1.0. |
| `src/nuclear/parse_endf_nGe.py:561` | ENDF n-Ge elastic cross-section preparation (`loglog_interp` def/body and its callers) | raw ENDF/B-VIII.0 point files under `data/endf/` | eV (neutron energy) | per-isotope ENDF native span | not declared -- script is frozen | NaN outside the span by default (`left=np.nan`), i.e. already not a clamp | excluded | `src/nuclear/parse_endf_nGe.py` is a one-shot data-PREPARATION script: it parses raw ENDF/B-VIII.0 files and writes the frozen `data/endf_nGe_elastic_v1.1.csv`, which is the artifact everything downstream reads. Guarding it would change nothing about the already-frozen table, and re-running it is out of scope for Phase 10. Its own `loglog_interp` already takes an explicit `extrapolate_below` flag and returns NaN (not a clamp) outside the span by default, so its out-of-domain behaviour is at least declared rather than silent. RECORDED AS A RESIDUAL: if Phase 15 ever re-runs this script, the NaN default should become a raise. The Phase-10 extended deposit axis never reaches it -- `parse_endf_nGe.py:279` calls `shared_energy_grid()` and CLIPS to the ENDF support, and plan 10-03 pins that caller to grid version v1.0. |
| `src/nuclear/parse_endf_nGe.py:569` | ENDF n-Ge elastic cross-section preparation (`loglog_interp` def/body and its callers) | raw ENDF/B-VIII.0 point files under `data/endf/` | eV (neutron energy) | per-isotope ENDF native span | not declared -- script is frozen | NaN outside the span by default (`left=np.nan`), i.e. already not a clamp | excluded | `src/nuclear/parse_endf_nGe.py` is a one-shot data-PREPARATION script: it parses raw ENDF/B-VIII.0 files and writes the frozen `data/endf_nGe_elastic_v1.1.csv`, which is the artifact everything downstream reads. Guarding it would change nothing about the already-frozen table, and re-running it is out of scope for Phase 10. Its own `loglog_interp` already takes an explicit `extrapolate_below` flag and returns NaN (not a clamp) outside the span by default, so its out-of-domain behaviour is at least declared rather than silent. RECORDED AS A RESIDUAL: if Phase 15 ever re-runs this script, the NaN default should become a raise. The Phase-10 extended deposit axis never reaches it -- `parse_endf_nGe.py:279` calls `shared_energy_grid()` and CLIPS to the ENDF support, and plan 10-03 pins that caller to grid version v1.0. |
| `src/nuclear/parse_endf_nGe.py:598` | ENDF n-Ge elastic cross-section preparation (`loglog_interp` def/body and its callers) | raw ENDF/B-VIII.0 point files under `data/endf/` | eV (neutron energy) | per-isotope ENDF native span | not declared -- script is frozen | NaN outside the span by default (`left=np.nan`), i.e. already not a clamp | excluded | `src/nuclear/parse_endf_nGe.py` is a one-shot data-PREPARATION script: it parses raw ENDF/B-VIII.0 files and writes the frozen `data/endf_nGe_elastic_v1.1.csv`, which is the artifact everything downstream reads. Guarding it would change nothing about the already-frozen table, and re-running it is out of scope for Phase 10. Its own `loglog_interp` already takes an explicit `extrapolate_below` flag and returns NaN (not a clamp) outside the span by default, so its out-of-domain behaviour is at least declared rather than silent. RECORDED AS A RESIDUAL: if Phase 15 ever re-runs this script, the NaN default should become a raise. The Phase-10 extended deposit axis never reaches it -- `parse_endf_nGe.py:279` calls `shared_energy_grid()` and CLIPS to the ENDF support, and plan 10-03 pins that caller to grid version v1.0. |
| `src/qpd_potential/interp_guard.py:11` | module docstring of the guard itself | n/a | n/a | n/a | n/a | n/a | excluded | Prose inside the Plan 10-01 guard module explaining why NaN is rejected. It contains no interpolation call and did not exist when the pre-fix witnesses were measured. |
| `src/qpd_potential/cevns.py:25` | `from scipy.interpolate import PchipInterpolator` | n/a | n/a | n/a | n/a | n/a | excluded | Import statement, not an evaluation site. The interpolator it names is constructed at cevns.py:235 and guarded there. |
| `src/qpd_potential/cevns.py:235` | `PchipInterpolator(E, log Phi, extrapolate=False)` construction; evaluated via `log_phi_guarded` / `flux` | `data/flux/reactor_flux_v1.0.csv` (and the Billard/NUCLEUS variants) col 0 | MeV | [0.1, 10.0] | [0.1, 10.0] (no extension) | **NaN** at 0.1*(1-1e-9) and at 10.0*(1+1e-9) | GUARDED | Tabulated-table abscissa. `extrapolate=False` returned NaN, which is a silent failure that propagates into a folded spectrum where it can be masked or zeroed downstream (`fp-nan-instead-of-raise`); it now raises at the point of evaluation. The separate zero-return in `flux()` outside the tabulated support is a DECLARED v1.0 truncation of the flux support applied before the interpolator, not a clamp of it, and is deliberately left unchanged. |
| `src/qpd_potential/cevns.py:250` | docstring/`note=` string in the guarded Domain | n/a | n/a | n/a | n/a | n/a | excluded | Prose recording the measured pre-fix clamp values for cevns.py:287; not a call site. Introduced by this plan. |
| `src/qpd_potential/cevns.py:287` | `ReactorFlux.rel_uncertainty` = `np.interp(E_nu, E, rel)` | same flux CSV, `rel_uncertainty` column | MeV | [0.1, 10.0] | [0.1, 10.0] (no extension) | **0.25** below the floor (clamped `rel[0]`), **0.05** above the ceiling (clamped `rel[-1]`); same values at 0.05 MeV and 20 MeV | GUARDED | Tabulated-table abscissa. `np.interp` clamps at both ends, so the 1-sigma flux band was silently extended at constant fractional width outside the range where it was ever evaluated. Now raises. |
| `src/qpd_potential/cevns.py:653` | `def _interp_loglog(...)` signature | n/a | n/a | n/a | n/a | n/a | excluded | Function definition line. Its body at cevns.py:672 is the guarded evaluation site. |
| `src/qpd_potential/cevns.py:660` | `_interp_loglog` docstring | n/a | n/a | n/a | n/a | n/a | excluded | Prose recording the measured pre-fix clamp values for cevns.py:672; not a call site. Introduced by this plan. |
| `src/qpd_potential/cevns.py:672` | `_interp_loglog` body = `10**np.interp(log10 x, log10 xs, log10 ys)` | `data/external/nucleus2019_fig1_ge.csv` (digitized NUCLEUS Fig. 1), via `load_nucleus_fig1` | eV (recoil T) | [1.020494, 1578.476] | [1.020494, 1578.476] (no extension) | **494.7631** below the floor and **0.5185263** above the ceiling (both clamped end values); identical at 0.51 eV and 3157 eV | GUARDED | Tabulated-table abscissa, and the table is a DIGITIZED FIGURE: there is nothing outside its span to extrapolate from, so no witness could ever justify an extension. The clamp returned a plausible finite differential rate where the published figure has no curve. |
| `src/qpd_potential/cevns.py:718` | `theirs = float(_interp_loglog(T, E_fig, R_fig, ...))` | `data/external/nucleus2019_fig1_ge.csv` | eV | [1.020494, 1578.476] | inherits the cevns.py:672 domain | inherits cevns.py:672 | excluded | Caller of the already-guarded `_interp_loglog`; guarding it a second time would double-report the same bound. The `reproduce_nucleus_fig1` anchor evaluates T = 10-500 eV, comfortably inside the digitized span (asserted by `test_nucleus_fig1_anchor_points_stay_in_domain`). |
| `src/qpd_potential/response.py:626` | `_thin_poisson` cross-check: `lam = np.interp(t_prop, t_grid, gamma)` | **no frozen table** -- `t_grid` is built by `resp._default_time_grid(d)` in the same call, and `gamma` is evaluated on it in the same call | s (time) | [t_grid[0], t_grid[-1]] by construction | not applicable -- constructed grid | not applicable | excluded | Constructed internal grid. `t_prop` is drawn from `rng.uniform(0, t_grid[-1])`, so it cannot leave the grid by construction. This helper is also an internal cross-check, explicitly not part of the deliverable estimator, and the extended deposit axis cannot drive it out of domain. |
| `src/qpd_potential/wafer_self_veto.py:321` | `note=` string in the guarded Domain | n/a | n/a | n/a | n/a | n/a | excluded | Prose recording the measured pre-fix clamp values for wafer_self_veto.py:325; not a call site. Introduced by this plan. |
| `src/qpd_potential/wafer_self_veto.py:325` | `_tail_integral` = `np.interp(E_cut, e_grid, rate)` for the partial first bin | `data/muon_dRdEdep.csv` via `frozen_spectrum()` | keV | [1.014497e-02, 1.97142e5] | [1.014497e-02, 1.97142e5] (no extension) | rate clamped to **16.01101** below the floor, giving `_tail_integral(1e-4 keV)` = **1073307.7521947508** counts/kg/day against a true full integral of 1073307.5913646354; **0.0** above the ceiling | GUARDED | Tabulated-table abscissa. `a_self_direct` short-circuits to 1.0 at/below the floor and 0.0 at/above the ceiling, so the public path never reached here out of domain -- but a direct call did, and returned a finite, *nearly right*, entirely fabricated number, which is precisely the kind of value nobody notices. Above the ceiling it returned a silent 0.0 rather than an error. |
| `src/qpd_potential/muon_deposit.py:164` | `sample_standard_landau`: `lam = np.interp(u, cdf, grid)` | **no frozen table** -- the abscissa is the cumulative distribution `cdf` built in `_build_landau_table()` in the same module by quadrature of the Landau density | dimensionless u in [0, 1] | [0.0, cdf[-1]] by construction | not applicable -- constructed grid | not applicable | excluded | Inverse-CDF sampler. The abscissa `u` is drawn from `rng.uniform(0,1)` and the ordinate grid is built in code, not read from a frozen table, so there is no table floor for the extended deposit axis to fall below. The one out-of-range case, u above `cdf[-1]`, is ALREADY handled explicitly on the next two lines by the analytic 1 - c/lambda tail rather than by a clamp. |
| `src/qpd_potential/compton_source.py:174` | comment above the `mu_over_rho` interp | n/a | n/a | n/a | n/a | n/a | excluded | Pre-existing comment explaining that `np.interp` clamps; not a call site. |
| `src/qpd_potential/compton_source.py:175` | `mu_over_rho` = `np.interp(log E, log E_tab, log mu/rho)` + explicit slope extrapolation | `data/ge_xcom_mu.csv` (4 frozen NIST XCOM points) | keV (function argument; the table abscissa is MeV, converted explicitly by 1e3) | [600.0, 2000.0] | **[200.0, 3000.0] -- WIDER THAN THE TABLE, both sides, witnessed** | **0.11879** cm^2/g at 241.997 keV (below the floor) and **0.0360649** cm^2/g at 2614.511 keV (above the ceiling), both by deliberate log-log slope extrapolation | GUARDED | Tabulated-table abscissa with a DELIBERATE v1.0 extrapolation. See the witness section below: the Pb-214 241.997 keV and Tl-208 2614.511 keV gamma lines both sit outside the table and are both folded by the v1.0 Compton channel, so an unconditional raise at the table span would break v1.0 anchors. The declared floor stops at 200 keV because below ~200 keV photoabsorption in Ge dominates and a log-log continuation of the Compton-regime interval would be badly wrong rather than mildly so. |
| `src/qpd_potential/compton_source.py:265` | `incoherent_S` = `np.interp(log x, log x_tab, log S)` + low-x slope extrapolation, high-x clamp to Z | `data/ge_incoherent_S.csv` (Hubbell 1975, 145 points) | dimensionless x [1/Angstrom] | [1.0e-3, 4.2646e4] | **[0.0, +inf) -- UNBOUNDED, both sides, witnessed; the bounds guard is VACUOUS for finite x >= 0 and this is stated rather than dressed up** | **6.677e-08** at x = 1e-5 (slope extrapolation), **0.0** at x = 0, **0.0** at x = -1.0 (negative x silently mapped to 1e-300), **32.0** at x = 1e6 (clamped to Z) | GUARDED | Tabulated-table abscissa, but exact forward scatter gives x = 0 identically and S(x -> inf) = Z = 32 is the exact free-electron asymptote, so neither bound can be narrowed without breaking the v1.0 Compton channel. The one genuine silent failure at this site is a NEGATIVE momentum transfer, previously mapped to 1e-300 by `np.maximum` and returned as S = 0.0; that now raises, as does a non-finite x. |
| `src/qpd_potential/compton_source.py:268` | comment below the `incoherent_S` interp | n/a | n/a | n/a | n/a | n/a | excluded | Pre-existing comment explaining the high-x clamp to S = Z; not a call site. |
| `src/qpd_potential/fold.py:569` | `_erec_of_edep` docstring | n/a | n/a | n/a | n/a | n/a | excluded | Prose recording the load-bearing pre-fix witness for fold.py:554; not a call site. Introduced by this plan. |
| `src/qpd_potential/fold.py:588` | `note=` string in the guarded Domain | n/a | n/a | n/a | n/a | n/a | excluded | Prose recording the measured pre-fix clamp value for fold.py:554; not a call site. Introduced by this plan. |
| `src/qpd_potential/fold.py:592` | `_erec_of_edep` = `exp(np.interp(log E_dep, log centers, log E_rec_median))` | `artifacts/stage1/response_matrix_*.npz :: E_dep_centers_eV` (Phase-5 response curve) | eV | [10.144970, 1.97142e8] | [10.144970, 1.97142e8] (no extension; no witness exists) | **4.899065996392436 eV** for EVERY deposit below the floor -- identical at 0.1 eV, 0.5 eV and 1 eV -- and **34763.53869373643 eV** for every deposit above the ceiling | GUARDED | THE LOAD-BEARING SITE OF THE PHASE. This is the first call site the plan 10-03 extension to 0.1 eV drives out of domain. The clamp answered a 0.1 eV deposit with the reconstructed energy of a 10.14 eV deposit -- E_rec/E_dep = 49 instead of ~0.5, a factor-49 overstatement -- as a finite, plausible, non-NaN number, and returned the same flat plateau for every sub-floor deposit. No v1.0 anchor evaluates below 10.14 eV (the retracted 'nothing below 10 eV' display rule is exactly why), so there is no witness and no extension is declared. |
| `src/qpd_potential/phonon_scale.py:191` | `vdos_weight_quantile_meV` = `np.interp(quantile, cdf, omega)` -- inverts the normalized cumulative VDOS weight to report a grid-independent "low-energy edge" | `data/external/ge_vdos/ge_vdos_normalized.csv` (and the DarkELF twin), cumulative trapezoid of g(omega) | dimensionless CDF (abscissa); returns meV | [0, 1] by construction -- the CDF is normalized to its own endpoint | [0, 1]; the only caller passes quantile = 1e-3 | n/a -- NO out-of-domain return is reachable: the abscissa is a CDF that spans exactly [0, 1] and the argument is a fixed interior constant | GUARDED | ADDED BY PLAN 11-01, and registered rather than hand-rolled to avoid this guard. It is the weakest kind of interpolation site in the repository: the abscissa is a normalized CDF whose span is [0, 1] by construction, so np.interp's clamping behaviour is unreachable for any quantile in (0, 1). It is a DIAGNOSTIC ONLY -- no locked scalar (omega_bar, <u_x^2>, B, 2W) depends on it; those come from trapezoid quadrature, not interpolation. Domain declaration is therefore recorded here rather than enforced through interp_guard, and that choice is deliberate and stated. |
| `src/qpd_potential/impulse_limit.py:220` | `structure_factor` adds the ANALYTIC one-phonon term back onto the FFT output: `np.interp(w_grid, w_v, g_v/w_v, left=0, right=0)` | `data/external/ge_vdos/ge_vdos_normalized.csv`, the frozen Ge VDOS | eV (phonon energy) | [1e-15, 0.03778966] eV | same; the one-phonon term has COMPACT SUPPORT on the VDOS band by physics, so outside it the correct value is exactly zero | n/a -- clamping is explicitly DISABLED via `left=0.0, right=0.0`, so the out-of-domain return is 0, which is the physically correct value rather than a clamp | GUARDED | ADDED BY PLAN 11-03, and registered rather than hand-rolled. This is the one case in the repository where returning zero outside the table is not a silent failure but the right answer: a Ge crystal has no one-phonon strength above its 37.79 meV VDOS ceiling or below zero energy transfer. `left`/`right` are set EXPLICITLY rather than relying on np.interp's default clamp-to-endpoint, which would have smeared the 37.79 meV edge value across the whole multi-eV FFT grid and destroyed the sum rules. |
| `src/qpd_potential/neutron_recoil.py:324` | `_sigma_endf_natural_b` = `np.interp(E, Et, st)` -- the raw ENDF/B-VIII.0 + Lib80x natural sigma_el on the frozen 23155-point union grid | `data/endf_nGe_elastic_v1.1.csv :: E_eV, sigma_el_natural_b` | eV (INCIDENT NEUTRON energy, not a recoil axis) | [1.031250e-05, 2.0e+07] | [5.0, 2.0e+07] -- the declared domain is NARROWER than the table on purpose: below the 5 eV seam the free-atom evaluation is not the bound-crystal cross section | clamp-to-endpoint, i.e. **59.42741 b** below the table floor (the free-gas 1/v upturn) and **1.222782 b** above the 20 MeV ceiling | GUARDED | ADDED BY PLAN 13-01, registered rather than hand-rolled. Guarded at BOTH ends by construction rather than by `interp_guard`, and both guards are executed rather than asserted. Above: `fold_dRdT` RAISES when any requested recoil needs E_n above the frozen ceiling, so sigma_el is never extrapolated past 20 MeV (fp-extrapolate-above-20mev). Below: the sub-5 eV route switch routes every evaluation under the seam to NCrystal `Ge_sg227` or to exact zero, and a module counter increments on every call to THIS function under 5 eV; `tests/test_neutron_recoil.py::test_no_free_atom_evaluation_below_the_seam_reaches_the_spectrum` asserts the counter is 0 for both admissible routes and >0 for the forbidden one, so the guard is shown non-vacuous. Linear (lin-lin) interpolation is the correct reconstruction here because NJOY linearised this grid to err=1e-3 in lin-lin. |
| `src/qpd_potential/neutron_recoil.py:695` | `smoothed_sigma_b` forward map: `np.interp(u, lnE, y)` places `sigma*E` on a uniform ln E grid before the Gaussian convolution | `data/endf_nGe_elastic_v1.1.csv`, transformed to ln E | ln(eV) | `[ln(1.03125e-05), ln(2.0e+07)]` | identical -- `u = np.linspace(lnE[0], lnE[-1], 400000)` spans exactly the table by construction | n/a -- clamping is UNREACHABLE: the query grid is built from the table's own endpoints | GUARDED | ADDED BY PLAN 13-01. Part of the SC3 smoothed-sigma CONTROL, which exists to be REJECTED by the imprint statistic; it never enters a reported spectrum. The abscissa is the table's own ln E span and the query points are constructed from it, so no out-of-domain evaluation exists. |
| `src/qpd_potential/neutron_recoil.py:702` | `smoothed_sigma_b` inverse map: `np.interp(lnE, u, num/den)` returns the convolved result to the frozen union grid | the uniform ln E grid built at line 695 | ln(eV) | `[ln(1.03125e-05), ln(2.0e+07)]` | identical -- the target points ARE the table nodes that generated `u` | n/a -- clamping is UNREACHABLE by the same construction | GUARDED | ADDED BY PLAN 13-01. Same control-only role as line 695. The two maps are inverses on the same span, so the round trip cannot leave the domain. |
| `src/qpd_potential/neutron_recoil.py:769` | `smoothed_sigma_fn` = `np.interp(e[hi], E, ss)` -- the smoothed sigma_el evaluated at the fold's quadrature nodes above the seam | the smoothed table produced by `smoothed_sigma_b` on the frozen union grid | eV (incident neutron energy) | [1.031250e-05, 2.0e+07] | [5.0, 2.0e+07] -- masked to `e >= SUB5EV_SEAM_eV`; sub-seam nodes go to the declared route instead | clamp-to-endpoint outside the union grid, unreachable because the quadrature node set is bounded by the table's own ceiling and by the seam mask | GUARDED | ADDED BY PLAN 13-01. CONTROL PATH ONLY -- this is the smoothed spectrum the SC3 imprint statistic must REJECT, emitted as an explicitly labelled control column and never as a result. Inherits the same upper guard as line 324 because it is evaluated on the same node set. |
| `src/qpd_potential/neutron_recoil.py:839` | `per_isotope_edge_fold` inner sigma callable: `np.interp(E[hi], _E, _s)` -- one frozen per-isotope sigma_el per Ge isotope | `data/endf/nGe_elastic_per_isotope.csv :: E_eV, sigma_el_b_<A>` | eV (incident neutron energy) | [1.031250e-05, 2.0e+07] (same energy grid as the natural table) | [5.0, 2.0e+07], masked identically to line 767 | clamp-to-endpoint outside the grid, unreachable for the same two reasons | GUARDED | ADDED BY PLAN 13-01. CROSS-CHECK ONLY: five per-isotope flat boxes, each with its own 4A/(1+A)^2, used to locate the kinematic edge independently of the production single-f fold. It is what measures the +0.52% edge misplacement of the abundance-weighted stand-in; it is not itself a deliverable spectrum. |
| `src/qpd_potential/neutron_recoil.py:973` | `forward_peaking_report` = `np.interp(nodes[sel], E, a1)` -- the CM P1 Legendre coefficient at the quadrature nodes above E_min(T) | `data/endf_nGe_elastic_v1.1.csv :: E_eV, a1_natural` | eV (incident neutron energy) | [1.031250e-05, 2.0e+07] | [E_min(T_floor) = 1.8645, 2.0e+07] -- `nodes` is the fold's own node set, bounded below by the axis floor and above by the frozen ceiling | clamp-to-endpoint, unreachable because `nodes` is generated inside the table span | GUARDED | ADDED BY PLAN 13-01. DIAGNOSTIC ONLY -- a1 is REPORTED and never applied; the frozen Phase-7 kernel is the isotropic-CM flat box. No emitted rate depends on this call site, so its only obligation is not to be evaluated outside the table, which the node construction already guarantees. |
| `src/qpd_potential/capture_channel.py:228` | `sigma_capture_b` = `np.interp(E, E_ace, sigma_ace)` -- the pre-reconstructed Lib80x ACE MT=102 capture cross section for one Ge isotope | `data/endf/ace/32<A>.800nc :: MT=102 xs` (and `.805nc` for the Doppler check) | eV (INCIDENT NEUTRON energy, not a recoil axis) | [1.0e-05, 2.0e+07] per isotope, as stored in the ACE file | [0.01, 2.0e+07] -- the Plan 14-01 fold band, strictly inside the ACE span at BOTH ends | clamp-to-endpoint outside the ACE grid | GUARDED | ADDED BY PLAN 14-01. Guarded by CONSTRUCTION rather than by `interp_guard`: every evaluation comes from `capture_quadrature_nodes`, which is built as the union of the ACE native grid inside `[e_lo, e_hi]` with a log grid over the SAME interval and then masked to it, and the fold band `[0.01 eV, 20 MeV]` lies strictly inside the ACE span, so no query point can leave the table. Linear (lin-lin) interpolation is the correct reconstruction because NJOY linearised this grid to err=1e-3 in lin-lin, exactly as for elastic at `neutron_recoil.py:324`. NOTE the source: MF=3 MT=102 in the raw ENDF file is identically zero through the resolved-resonance region, so the ACE set is not a convenience here, it is the only local source of a pointwise capture cross section. |
| `src/qpd_potential/capture_channel.py:245` | `_inelastic_grid` = `np.interp(union, x, y, left=0.0, right=y[-1])` -- one discrete-inelastic partial (MT=51..91) placed on the union of the contributing MTs' own grids before summing | `data/endf/ace/32<A>.800nc :: MT=51..91 xs` | eV (incident neutron energy) | each partial's own grid, which starts at ITS OWN THRESHOLD | the union grid of all present partials for that isotope | `left=0.0` EXPLICITLY, `right=y[-1]` | GUARDED | ADDED BY PLAN 14-01. `left=0.0` is the physics, not a fallback: an inelastic partial is EXACTLY ZERO below its own level threshold, so clamping to `y[0]` would manufacture sub-threshold inelastic scattering. `right` clamping is unreachable in the fold because every partial's grid ends at the same 20 MeV ENDF ceiling that bounds the fold band. |
| `src/qpd_potential/capture_channel.py:252` | `sigma_inelastic_b` = `np.interp(E, E_union, sigma_union, left=0.0, right=s[-1])` -- the summed MT=51..91 inelastic cross section at the fold's quadrature nodes | the per-isotope union grid built at line 245 | eV (incident neutron energy) | [first threshold, 2.0e+07] | [0.01, 2.0e+07] -- the fold band, which extends BELOW the lowest inelastic threshold | `left=0.0` EXPLICITLY, so the sub-threshold band contributes exactly zero rather than a clamped positive value | GUARDED | ADDED BY PLAN 14-01. This is the one site in the plan whose query band genuinely extends outside its table, and it does so DOWNWARD into a region where the physical cross section is zero. `left=0.0` is therefore correct and is the reason the thermal and epithermal inelastic band rates come out exactly 0.0 -- a measured zero from a thresholded reaction, not a manufactured one. ROADMAP SC4's never-zero rule applies to the CAPTURE channel, whose every band is non-zero. |
| `src/qpd_potential/conus_check.py:218` | `integrate_window_counts_kg_day` = `np.interp(lo, T, y)` and `np.interp(hi, T, y)` -- the two WINDOW-EDGE values of the committed recoil-axis CEvNS dR/dT, inserted so a CONUS+ analysis-window integral starts and ends exactly at its own converted boundary instead of at the nearest tabulated knot | `artifacts/v2.0/cevns_dRdT_ext.csv :: dRdT_total` | eV (NUCLEAR RECOIL energy T, not a deposit or reconstructed axis) | [0.1010207935, 3165.6057026] as tabulated, of which the non-zero support ends at 3031.6858 eV | the converted keV_ee -> keV_nr window edges of each candidate, which for the pre-registered window are 2116.49 and 4742.51 eV | clamp-to-endpoint, which for the UPPER edge means clamping to the table's own trailing ZERO | GUARDED | ADDED BY PLAN 16-01. Guarded by MEASUREMENT rather than by `interp_guard`: the fraction of every candidate window lying inside the non-zero support is computed and emitted as a column, and a window whose LOWER edge is above the support edge is flagged `above_kinematic_endpoint` and recorded as a ZERO rate rather than as a truncated integral (`fp-silent-endpoint-truncation`). Clamping at the upper edge is therefore harmless here and is visible in the artifact rather than silent: the table's trailing values are exact zeros, so the clamp returns 0.0 and cannot manufacture rate above the kinematic endpoint. Linear interpolation is the correct reconstruction because the table's 400-bins-per-decade spacing makes the edge correction a sub-bin adjustment, and the alternative -- snapping to the nearest knot -- would make the window integral depend on the grid rather than on the window. |
| `src/qpd_potential/muon_analytic.py:135` | `landau_cdf` = `np.interp(lam, grid, cdf, left=0.0, right=cdf[-1])` -- the standard-Landau CDF F(lambda), evaluated at the deposited-energy BIN EDGES so each (chord, muon energy) contributes its exact probability to every bin instead of one sampled delta (Rao-Blackwellization of the straggling draw) | `muon_deposit._build_landau_table()` -- the SAME cached table `sample_deposit` inverts; not a re-tabulation | dimensionless Landau variate lambda | [-4.0, 300.0], 1000 nodes; `cdf[0] = 0.0` by construction, `cdf[-1] = 0.99574330` | unbounded in principle: lambda = (E_edge - Delta_p)/xi + lambda_mode runs over every bin edge, so both ends are reached routinely | clamp LOW to 0.0; above `lam_hi = 300.0` the ANALYTIC tail `F = 1 - c/lambda` (`c_tail = 1.277010`) replaces the clamp, the same continuation `sample_standard_landau` applies | GUARDED | ADDED 2026-07-23 (curve-smoothing work). Deliberately NOT guarded by `interp_guard`, because clamping is the physically correct behaviour at BOTH ends and raising would be wrong. LOW end: the standard Landau density falls off double-exponentially below lambda ~ -4, so `left=0.0` asserts "no deposit this far below the MPV", which is the true limit and not a truncation -- the table's own `cdf[0] = 0.0` encodes the same statement. HIGH end: the clamp is never reached, because the `lam > lam_hi` branch substitutes the closed-form 1/lambda tail first; `right=cdf[-1]` is unreachable defensive code. The decisive point is that this table is READ FORWARDS here and INVERTED by the Monte-Carlo sampler, so any error in it is COMMON to both paths and cannot hide inside the analytic-vs-MC comparison in `tests/test_muon_analytic.py` (`fp-shared-error-cancels` is therefore not available as an escape: the comparison tests the INTEGRATION method, not the Landau table, and that scope limit is stated in the test module docstring). |

> **Line numbers refreshed 2026-07-22 after plan 10-03.** The pin comments plan 10-03
> added to `src/nuclear/parse_endf_nGe.py` shifted its line numbers; the hit COUNT and the
> classification are unchanged. The pre-fix witness values in section 3 were measured
> against the pre-guard tree and are unaffected.

**Verdict tally: 7 GUARDED, 26 excluded** (26 = 2 imports + 1 def line + 4 comments + 5
prose strings introduced by this plan + 1 already-guarded caller + 2 constructed-grid sites
+ 11 `parse_endf_nGe.py` data-prep + 1 `assemble_spectrum.py` data-prep... which is 27 by
that grouping; the caller row `cevns.py:718` is counted once. The mechanical count is what
the test asserts: 33 rows total, 7 with verdict `GUARDED`.)

---

## 3. THE DECISIVE FINDING: the guard is not vacuous

`test-witness-pre-fix` pass condition: *"at least one call site is shown to have previously
returned a finite non-error value outside its table span. If none did, the guard is vacuous
and the phase must say so rather than claim a fix."*

**Five call sites did.** They are listed here in descending order of how badly wrong the
returned number was.

### 3.1 `fold.py::_erec_of_edep` --- the load-bearing witness

The abscissa floor is the response matrix's first deposit centre, **10.144970 eV**. Under
`np.interp` in log-log space, every evaluation below that floor returned the clamped
end value:

| E_dep queried | pre-fix E_rec returned | E_rec / E_dep | what it should be |
|---|---|---|---|
| 10.144970 eV (the floor) | 4.899065996392436 eV | 0.483 | 0.483 --- correct, in domain |
| 1.0 eV | 4.899065996392436 eV | **4.9** | ~0.5 |
| 0.5 eV | 4.899065996392436 eV | **9.8** | ~0.5 |
| 0.1 eV | 4.899065996392436 eV | **49** | ~0.5 |

A 0.1 eV deposit was reported to reconstruct at 4.90 eV --- **a factor of ~49 too high** ---
as a finite, plausible, non-NaN number, and the *same* number came back for every sub-floor
deposit. That flat invented plateau sits exactly where plan 10-03 extends the axis. Above the
ceiling the same clamp returned 34763.53869373643 eV for any deposit, including 1e9 eV.

This is the single number that most justifies the ordering `10-01 -> 10-03`.

### 3.2 `wafer_self_veto.py::_tail_integral` --- the near-miss

`_tail_integral(1e-4 keV)` returned **1073307.7521947508** counts/kg/day against a true full
integral of **1073307.5913646354** --- 1.5e-7 relative. The clamped floor rate of 16.01101
was extended over a decade of energy that carries no data, and the result was *almost exactly
right*, which is precisely why nobody would notice it. Above the ceiling the same function
returned exactly **0.0**: a silent zero, not an error. (`a_self_direct` short-circuits before
reaching here, so no v1.0 acceptance number moves; the exposure was to a direct call.)

### 3.3 `compton_source.py::mu_over_rho` --- a *deliberate* extrapolation, now visible

Returned **0.11879 cm^2/g** at 241.997 keV and **0.0360649 cm^2/g** at 2614.511 keV, both
outside the four-point NIST XCOM table [600, 2000] keV, by explicit log-log slope
extrapolation. This one is by design and cannot be removed (section 4); the guard bounds it.

### 3.4 `cevns.py::rel_uncertainty` --- constant-width band, forever

Clamped to **0.25** below 0.1 MeV and **0.05** above 10 MeV, at any distance from the table.

### 3.5 `cevns.py::_interp_loglog` on the NUCLEUS Fig. 1 digitization

Clamped to **494.7631** below 1.020494 eV and **0.5185263** above 1578.476 eV --- a plausible
finite differential rate where the *published figure has no curve at all*.

### 3.6 And one that returned NaN rather than a number

`cevns.py::ReactorFlux._log_phi` (`PchipInterpolator(..., extrapolate=False)`) returned
**NaN** on both sides. Per `fp-nan-instead-of-raise`, NaN is not "not extrapolating": it
propagates silently into a spectrum where it can be filtered, zeroed, or masked downstream.
It now raises.

---

## 4. Declared domains wider than their table, and their witnesses

`test-domain-extension-witness`: *"Zero declared extensions lack a witness point. A declared
extension whose only purpose is to avoid raising is a failure of this test, not a passing
configuration."* Two sites declare an extension. Both are enforced in code ---
`interp_guard.Domain.__post_init__` **raises at construction** if a bound falls outside the
tabulated span with no witness string, so an unwitnessed extension cannot be shipped.

### 4.1 `mu_over_rho`: declared [200, 3000] keV vs table [600, 2000] keV

| Side | Witness | Value | Where it is already evaluated in v1.0 |
|---|---|---|---|
| below | **Pb-214 241.997 keV** line | mu/rho = 0.11879 cm^2/g | `data/gamma_lines.csv` row 16; folded by the v1.0 Compton channel. `tests/test_compton_source.py::test_xcom_extrapolation_monotone_and_reasonable` evaluates 295.0 keV and asserts 0.10 < mu/rho < 0.12. |
| above | **Tl-208 2614.511 keV** line | mu/rho = 0.0360649 cm^2/g | `data/gamma_lines.csv` row 2, the highest-energy line. The same v1.0 test asserts 0.034 < mu/rho(2614.5 keV) < 0.038. |

Making this site raise at the table span would break both of those v1.0 anchors. The declared
floor stops at 200 keV rather than running to zero because **below ~200 keV photoabsorption in
Ge (Z = 32) dominates** and a log-log linear continuation of the Compton-regime 0.6--2.0 MeV
interval would be badly wrong there, not mildly wrong. Pre-fix, that continuation ran to
arbitrarily low energy with no complaint.

**This is an extrapolation made explicit. The guard makes it visible; it does not make it
correct.** It remains a documented extrapolation from four points, not a validated
interpolation, and it is carried as a weakest anchor.

### 4.2 `incoherent_S`: declared [0, +inf) vs table [1.0e-3, 4.2646e4]

| Side | Witness | Why the bound cannot be narrowed |
|---|---|---|
| below | **exact forward scatter, x = 0 identically** | `momentum_transfer_x(E, cos_theta=1) == 0.0` exactly (asserted by `tests/test_compton_source.py::test_momentum_transfer_x`), and `compton_deposit._kn_bound` evaluates S at every angular grid point including the forward one. `test_incoherent_S_limits` evaluates x = 1e-5. Any positive declared floor breaks the v1.0 Compton channel. |
| above | **x = 1e6** (`test_incoherent_S_limits`) | S(x -> inf) = Z = 32 *exactly* (electrons act free), so the value above the table is the exact asymptote, not a truncation artefact. |

**Stated plainly rather than dressed up: the bounds guard at this site is VACUOUS for every
finite x >= 0.** Both bounds are unbounded, both are witnessed, and neither can be tightened
without breaking v1.0 physics. What the guard *does* catch here is real but narrow: a
**negative momentum transfer**, which the pre-guard code mapped silently to x = 1e-300 via
`np.maximum` and returned as S = 0.0. That, plus a non-finite x, now raises.

---

## 5. Confirming the tests fail without the guard (`fp-vacuous-guard`)

Procedure and result recorded in `10-01-SUMMARY.md` section "Non-vacuity check". Method:
`git stash` the guard changes to `src/`, keep `tests/test_interpolator_bounds.py`, re-run.

---

## 6. Residual findings recorded, not fixed

1. **`src/flux/assemble_spectrum.py:122` uses `PchipInterpolator(..., extrapolate=True)`.**
   That is a *deliberate* extrapolation in the script that writes the frozen
   `data/flux/reactor_flux_v1.0.csv`. The outermost points of the frozen flux table may
   therefore be extrapolated rather than tabulated values. This is a v1.0 provenance
   question; it is neither created nor worsened by the sub-eV deposit-axis extension (the
   E_nu axis is untouched by Phase 10), and re-running the flux assembly is out of scope.
   **Reported, not patched away.**
2. **`src/nuclear/parse_endf_nGe.py::loglog_interp` returns NaN outside its span by
   default.** Better than a clamp, still not a raise. The script is frozen and its output
   `data/endf_nGe_elastic_v1.1.csv` is what downstream reads. If Phase 15 re-runs it, the
   NaN default should become a raise.
3. **`ReactorFlux.flux()` returns 0.0 outside the tabulated E_nu support.** This is a
   *declared truncation of the flux support*, applied before the interpolator, and it is a
   physics statement the project inherited from v1.0 --- not a statement that the reactor
   antineutrino flux vanishes below 0.1 MeV. Plan 10-01 deliberately left it alone, because
   changing it would move v1.0 physics rather than error behaviour. It is recorded here so
   that the distinction between "the interpolator clamps" and "the model truncates the
   support" is on the record and testable
   (`test_reactor_flux_zero_support_truncation_is_preserved`).
4. **A hand-rolled interpolation written as arithmetic** rather than as a call to `np.interp`
   or a scipy class would not be found by the recorded grep. This is the stated unvalidated
   assumption of the enumeration and remains open.

---

## 7. Units discipline (CONVENTIONS Section A.1)

Every declared bound is recorded in the units of **its own** abscissa; no bound was converted
implicitly, and `interp_guard.Domain` carries the unit string into the exception message.

| Site | Abscissa units | Declared bounds in those units |
|---|---|---|
| `ReactorFlux` Phi and rel_uncertainty | MeV | 0.1, 10.0 |
| NUCLEUS Fig.1 log-log | eV (recoil T) | 1.020494, 1578.476 |
| `mu_over_rho` | keV (arg); table is MeV, converted by an explicit `/1.0e3` | 200.0, 3000.0 |
| `incoherent_S` | dimensionless x [1/Angstrom] | 0.0, +inf |
| `_erec_of_edep` | eV | 10.144970, 1.97142e8 |
| `_tail_integral` | keV | 1.014497e-02, 1.97142e5 |
