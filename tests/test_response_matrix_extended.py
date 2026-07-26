# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Plan 10-04: the regenerated R(E_rec|E_dep) on the 744-column extended axis.

ROADMAP Phase 10 success criterion 1 (second half) and the line-435 stop-condition.

Two things make the conservation test mean anything:
  * the OFF-GRID MASS counter -- a column divided by its own sum always sums to
    1, so `max |colsum - 1|` alone measures the division, not the physics
    (``fp-renormalised-conservation``);
  * the BITWISE overlap check against a same-code v1.0-range rebuild, which is
    what proves plan 10-03's energy-keyed sub-seed actually took.

Bit-identity against the ARCHIVED matrices is NOT asserted anywhere: they were
built on CSV-round-tripped deposit centres differing by 4.918e-07
(``fp-bit-identical-promise``). That comparison is statistical.
"""
import json
import os
import subprocess
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from qpd_potential import energy_scale as es
from qpd_potential import params
from qpd_potential import response as resp
from qpd_potential import response_matrix as rm
from qpd_potential import trigger

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_V20 = os.path.join(_ROOT, "artifacts", "v2.0")
_V10 = os.path.join(_ROOT, "artifacts", "stage1")

EXT_FILE = {"Ta->Al": "response_matrix_TaAl_ext.npz",
            "Al->Hf": "response_matrix_AlHf_ext.npz"}
ARC_FILE = {"Ta->Al": "response_matrix_TaAl.npz",
            "Al->Hf": "response_matrix_AlHf.npz"}
DESIGNS = tuple(EXT_FILE)
CANONICAL = "non_paralyzable"          # CONVENTIONS Section F, user decision 2026-07-21

_CACHE = {}


def _ext(design):
    if design not in _CACHE:
        p = os.path.join(_V20, EXT_FILE[design])
        assert os.path.exists(p), f"missing regenerated matrix {p}"
        _CACHE[design] = dict(np.load(p, allow_pickle=True))
    return _CACHE[design]


def _arc(design):
    key = "arc:" + design
    if key not in _CACHE:
        _CACHE[key] = dict(np.load(os.path.join(_V10, ARC_FILE[design]), allow_pickle=True))
    return _CACHE[key]


# --------------------------------------------------------------------------- #
# claim-regenerated                                                            #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("design", DESIGNS)
@pytest.mark.parametrize("variant", params.CENSORING_VARIANTS)
def test_conservation(design, variant):
    """test-conservation. Column sums INCLUDE the underflow bin. For a correctly
    constructed column this should sit at machine precision; a value merely
    under 1e-3 would be a warning sign, not a pass."""
    z = _ext(design)
    R = z[f"R_{variant}"]
    sums = R.sum(axis=0)
    worst = float(np.abs(sums - 1.0).max())
    assert worst <= 1e-3, f"{design}/{variant}: max |colsum-1| = {worst}"
    assert worst < 1e-12, (
        f"{design}/{variant}: max |colsum-1| = {worst} is far above machine "
        "precision; a correctly normalised column construction should not do this")
    # the underflow bin is genuinely part of the sum
    assert z["E_rec_edges_eV"][0] == 0.0


@pytest.mark.parametrize("design", DESIGNS)
def test_column_normalisation_shapes_and_positivity(design):
    """test-column-normalisation."""
    z = _ext(design)
    Ec = z["E_dep_centers_eV"]
    assert Ec.size == 744
    assert np.all(np.diff(Ec) > 0)
    assert float(Ec[0]) == pytest.approx(0.1013838, abs=5e-8)
    for variant in params.CENSORING_VARIANTS:
        R = z[f"R_{variant}"]
        assert R.shape == (z["E_rec_edges_eV"].size - 1, 744)
        assert R.shape[0] == 161
        assert int(np.isnan(R).sum()) == 0
        assert int((R < 0).sum()) == 0
        # per-cell relative MC error stored wherever the cell is populated
        err = z[f"err_{variant}"]
        pop = z[f"counts_{variant}"] > 0
        assert np.all(np.isfinite(err[pop]))
        assert np.all(np.isnan(err[~pop]))


@pytest.mark.parametrize("design", DESIGNS)
@pytest.mark.parametrize("variant", params.CENSORING_VARIANTS)
def test_no_mass_off_grid(design, variant):
    """test-no-mass-off-grid, fp-renormalised-conservation.

    Counted BEFORE histogramming. Without this the conservation test above
    measures the `col = h / h.sum()` division, not the physics."""
    z = _ext(design)
    assert int(z[f"n_offgrid_high_{variant}"].sum()) == 0, (
        "probability mass fell off the TOP of the E_rec grid and was silently "
        "discarded by np.histogram, then renormalised away by col = h / h.sum()")
    assert int(z[f"n_offgrid_low_{variant}"].sum()) == 0


@pytest.mark.parametrize("design", DESIGNS)
def test_both_censoring_variants_present_and_non_paralyzable_is_canonical(design):
    """CONVENTIONS Section F: non-paralyzable is canonical; paralyzable is a
    retained sensitivity, never silently dropped (fp-single-censoring)."""
    z = _ext(design)
    for variant in ("non_paralyzable", "paralyzable"):
        assert f"R_{variant}" in z
    assert params.DEFAULT_CENSORING == CANONICAL


@pytest.mark.parametrize("design", DESIGNS)
def test_provenance_header_carries_the_required_caveats(design):
    z = _ext(design)
    meta = json.loads(str(z["meta_json"]))
    assert meta["plan"] == "10-04"
    assert meta["grid_version"] == "v2.0-ext"
    assert meta["E_dep_n_columns"] == 744
    assert meta["N_s"] == 5000 == rm.DEFAULT_N_S
    assert meta["M_pool"] == 2000 == rm.DEFAULT_M_POOL
    assert meta["ec_emg_max"] == 2000.0 == rm.DEFAULT_EC_EMG_MAX
    assert meta["git_sha"] and meta["git_sha"] != "unknown"
    assert "column_seed_sequence" in meta["seed_scheme"]
    assert "DEPOSIT ENERGY" in meta["seed_scheme"]
    cav = meta["linear_yield_extrapolation_caveat"]
    assert "6.8 ueV" in cav and "190 ueV" in cav and "0.018 quasiparticles" in cav
    assert "MEAN-FIELD EXTRAPOLATION" in cav
    assert "1.0 eV" in meta["subev_regime_note"]
    assert "4.918e-07" in meta["v1_comparison_note"]
    assert "not claimed" in meta["v1_comparison_note"]


def test_v1_artifacts_are_untouched():
    """fp-overwrite-v1-matrices. The anchor notebook loads these directly, so
    overwriting them would make the anchor re-run circular."""
    out = subprocess.run(
        ["git", "status", "--porcelain", "artifacts/stage1/"],
        cwd=_ROOT, capture_output=True, text=True).stdout
    changed = [ln for ln in out.splitlines() if not ln.startswith("??")]
    assert changed == [], f"v1.0 artifacts modified: {changed}"
    for f in ARC_FILE.values():
        assert os.path.exists(os.path.join(_V10, f))


# --------------------------------------------------------------------------- #
# claim-overlap-intact                                                         #
# --------------------------------------------------------------------------- #
def test_overlap_bitwise_against_a_same_code_v1_range_rebuild():
    """test-overlap-bitwise. THE proof that plan 10-03's energy-keyed sub-seed
    took. A subset of the v1.0-range columns is rebuilt by the same code on the
    584-column axis and compared to the corresponding columns of the 744-column
    build. Bit-for-bit, max |difference| exactly 0.0.

    A subset (every 60th column) is used so the test runs in seconds; the full
    584-column comparison was run once during plan 10-04 and reported in the
    SUMMARY as array_equal=True with max |difference| 0.0 for both designs."""
    design = "Ta->Al"
    z = _ext(design)
    v1_centres = rm.E_dep_grid_from_shared_grid_eV("v1.0")
    idx = np.arange(0, 584, 60)
    sub = v1_centres[idx]
    d = es.resolve_design(design)
    m = rm.build_matrix(d, CANONICAL, sub, z["E_rec_edges_eV"],
                        seed=rm.DEFAULT_SEED, N_s=rm.DEFAULT_N_S,
                        M_pool=rm.DEFAULT_M_POOL, ec_emg_max=rm.DEFAULT_EC_EMG_MAX)
    R_ext = z[f"R_{CANONICAL}"][:, 160 + idx]
    assert np.array_equal(m["R"], R_ext)
    assert float(np.abs(m["R"] - R_ext).max()) == 0.0
    assert np.array_equal(m["E_rec_median_eV"],
                          z[f"E_rec_median_{CANONICAL}_eV"][160 + idx])
    # ... and the deposit energies really are identical, not merely close
    assert np.array_equal(sub, z["E_dep_centers_eV"][160 + idx])


@pytest.mark.parametrize("design", DESIGNS)
def test_overlap_vs_archived_is_consistent_with_monte_carlo_noise(design):
    """test-overlap-vs-archived. STATISTICAL, never bitwise.

    Differences are normalised by the ABSOLUTE per-cell MC error stored in the
    archived npz (R_arch * err_arch). Restricted to WELL-POPULATED cells, where
    a Gaussian 3-sigma criterion actually applies. The raw all-cells fraction is
    much larger and is reported as a finding in the SUMMARY -- it is low-count
    Poisson discreteness, not a regression."""
    z, a = _ext(design), _arc(design)
    R_ext = z[f"R_{CANONICAL}"][:, 160:]
    Ra, ea, ca = a[f"R_{CANONICAL}"], a[f"err_{CANONICAL}"], a[f"counts_{CANONICAL}"]
    assert R_ext.shape == Ra.shape == (161, 584)

    well = (ca >= 1000) & np.isfinite(ea)
    assert well.sum() > 500
    dn = np.abs(R_ext[well] - Ra[well]) / (Ra[well] * ea[well])
    # a difference of two INDEPENDENT estimates has sigma_diff ~ sqrt(2)*sigma,
    # so the Gaussian expectation for |d|/sigma > 3 is ~2*(1-Phi(3/sqrt2)) ~ 3.4e-3
    assert float(np.mean(dn > 3.0)) < 0.01, (
        f"{design}: {np.mean(dn > 3.0):.4f} of well-populated cells beyond 3 sigma")
    assert float(np.mean(dn > 3.0 * np.sqrt(2.0))) < 0.005
    # the disagreement carries very little probability mass
    tv = np.abs(R_ext - Ra).sum(axis=0)
    assert float(np.median(tv)) < 1e-9      # most columns agree exactly
    assert float(tv.max()) < 0.10


# --------------------------------------------------------------------------- #
# claim-subev-diagnosed                                                        #
# --------------------------------------------------------------------------- #
def _col(z, target_eV):
    Ec = z["E_dep_centers_eV"]
    return int(np.argmin(np.abs(np.log(Ec) - np.log(target_eV))))


@pytest.mark.parametrize("design", DESIGNS)
def test_subev_diagnostics_measured(design):
    """test-subev-diagnostics. All four quantities measured at 0.1, 0.5 and 1 eV."""
    z = _ext(design)
    for target in (0.1, 0.5, 1.0):
        j = _col(z, target)
        n_obs = float(z[f"N_obs_mean_{CANONICAL}"][j])
        p0 = float(z[f"P_zero_count_{CANONICAL}"][j])
        nd = int(z[f"n_distinct_Erec_{CANONICAL}"][j])
        err = z[f"err_{CANONICAL}"][:, j]
        assert np.isfinite(n_obs) and n_obs > 0
        assert 0.0 <= p0 <= 1.0
        assert nd > 0
        assert np.isfinite(np.nanmin(err))
    # the roadmap's N_obs figure at 0.5 eV is a COMPARISON TARGET, measured here
    j = _col(z, 0.5)
    n_obs_half = float(z[f"N_obs_mean_{CANONICAL}"][j])
    roadmap = {"Ta->Al": 39.4, "Al->Hf": 49.9}[design]
    assert n_obs_half == pytest.approx(roadmap, rel=0.05), (
        f"{design}: measured N_obs(0.5 eV) = {n_obs_half} vs roadmap {roadmap}")


@pytest.mark.parametrize("design", DESIGNS)
def test_registered_count_is_NOT_an_integer_lattice(design):
    """FINDING, recorded as a test so it cannot be forgotten.

    The plan expected 'the response is C times an integer count, so it is
    discrete' and predicted a small number of distinct reconstructed values at
    0.1 eV. It is NOT: 228 (Ta->Al) / 359 (Al->Hf) distinct values out of 5000
    samples, and the values are not integers times C.

    Mechanism, measured: the sensor classes carry FRACTIONAL populations
    (pi*r^2 = 12.566371 on-spot, 10287.433629 off-spot), so class_sum_samples
    adds a `frac * extra` term; and each class sum is then rescaled by
    mu_analytic/mu_pool (1.0515 and 1.0879 at 0.1 eV for Ta->Al) to pin the class
    mean to the analytic estimator. The registered count is therefore a
    continuously-rescaled, fractionally-weighted sum, not a Poisson integer."""
    z = _ext(design)
    j = _col(z, 0.1)
    nd = int(z[f"n_distinct_Erec_{CANONICAL}"][j])
    assert nd > 100, (
        "the 0.1 eV column turned out to be genuinely low-cardinality; the "
        "recorded finding needs revisiting")
    n_spot = float(np.pi * params.R_SPOT.value ** 2)
    n_off = float(params.N_SENSORS.value - n_spot)
    assert n_spot % 1.0 != 0.0 and n_off % 1.0 != 0.0, (
        "both sensor classes were expected to carry fractional populations")


@pytest.mark.parametrize("design", DESIGNS)
def test_double_count_verdict_zero_count_mass_vs_one_minus_ptrig(design):
    """test-double-count-check. The comparison Phases 12 and 15 need BEFORE they
    multiply R by the trigger curve.

    Measured: P(no counts registered) is <= 2e-4 at 0.1 eV and exactly 0 at
    0.5 and 1 eV, while 1 - P_trig is 0.998, 0.512 and 0.056 there. They differ
    by three to four orders of magnitude (and are incommensurable where P_zero
    is exactly zero), so they are NOT describing the same non-detection and may
    be multiplied. See 10-04-ANCHOR-AUDIT.md for the verdict and its caveat."""
    z = _ext(design)
    for target in (0.1, 0.5, 1.0):
        j = _col(z, target)
        E = float(z["E_dep_centers_eV"][j])
        p_zero = float(z[f"P_zero_count_{CANONICAL}"][j])
        one_minus = 1.0 - float(trigger.P_trig(E))
        assert p_zero <= 2.0e-4, f"{design} at {E} eV: P_zero = {p_zero}"
        assert one_minus > 0.05
        # the decisive inequality: the two are not comparable in size
        assert p_zero < 0.01 * one_minus, (
            f"{design} at {E} eV: P_zero = {p_zero} is comparable to "
            f"1-P_trig = {one_minus}; multiplying them would double-count "
            "non-detection and the verdict must be revisited")


def test_trigger_curve_is_not_folded_into_the_matrix():
    """fp-trigger-applied-here. The trigger is an analysis efficiency on a rate,
    not part of the response kernel. If it had been folded in, the sub-eV columns
    would no longer be normalised."""
    for design in DESIGNS:
        z = _ext(design)
        j = _col(z, 0.5)
        assert float(z[f"R_{CANONICAL}"][:, j].sum()) == pytest.approx(1.0, abs=1e-12)
        meta = json.loads(str(z["meta_json"]))
        assert "NOT folded into this matrix" in meta["subev_regime_note"]


# --------------------------------------------------------------------------- #
# claim-anchors: the 197 MeV endpoint recomputed from the NEW matrices          #
# --------------------------------------------------------------------------- #
# EXPECTED VALUES REVISED 2026-07-25 for the unit calibration slope
# (params.CALIB_SLOPE = 1.0, CONVENTIONS Section E.1). The reconstructed axis is
# now full-scale (E_rec estimates the deposit), so the 197 MeV endpoint plateau
# doubled from the paper's old-axis 34.8 / 26.8 keV to 69.53 / 53.69 keV. The
# paper (paper/sections/results.tex) still quotes the old values and its update is
# pending (follow-up todo); these are the CORRECT current-axis numbers.
@pytest.mark.parametrize("design,paper_keV", [("Ta->Al", 69.53), ("Al->Hf", 53.69)])
def test_197MeV_endpoint_anchor_from_the_v2_matrices(design, paper_keV):
    """The anchor notebook loads the FROZEN v1.0 matrices, so its run proves the
    grid work did not break v1.0. This recomputes the same anchor from the NEW
    artifacts/v2.0/ matrices -- the one that actually tests the regeneration.
    Tolerance tol_pct = 3. The expected value is the corrected unit-slope endpoint
    (69.53 / 53.69 keV), which SUPERSEDES the paper's old-axis 34.8 / 26.8 keV."""
    z = _ext(design)
    erec_end_keV = float(z[f"E_rec_median_{CANONICAL}_eV"][-1]) / 1.0e3
    diff_pct = 100.0 * (erec_end_keV - paper_keV) / paper_keV
    assert abs(diff_pct) <= 3.0, (
        f"{design}: v2.0 endpoint {erec_end_keV:.4f} keV vs paper {paper_keV} "
        f"({diff_pct:+.2f}%)")
    # and the deposit endpoint really is the 197 MeV column
    assert float(z["E_dep_centers_eV"][-1]) == pytest.approx(1.97e8, rel=0.01)


def test_anchor_audit_records_a_counted_number_not_the_unsourced_24():
    """fp-anchor-count-restated. The audit must state the number actually
    emitted, and must not launder the unsourced figure 24 through a phase gate."""
    p = os.path.join(_ROOT, "GPD", "phases",
                     "10-sub-ev-grid-extension-and-the-trigger-observable-p-grid",
                     "10-04-ANCHOR-AUDIT.md")
    assert os.path.exists(p)
    text = open(p).read()
    assert "32" in text
    assert "24" in text                     # the claimed figure is confronted
    assert "unsourced" in text.lower()
    assert "jupyter nbconvert" in text      # the literal execution command
    assert "computed=" in text              # the raw anchor lines
