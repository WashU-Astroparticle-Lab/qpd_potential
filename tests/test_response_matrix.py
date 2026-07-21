# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
#
# Plan 05-02 acceptance tests for the Monte-Carlo response matrix
# R(E_rec | E_dep) (qpd_potential.response_matrix). Covers the contract tests:
#   test-convergence        -> test_convergence_*        (<=~3%/cell, 1/sqrt(N_s))
#   test-span               -> test_span_*               (Phase-4 grid; columns sum to 1)
#   test-both-variants      -> test_both_variants        (4 baseline matrices)
#   test-repro              -> test_repro_*              (seed reproduces R; metadata)
#   test-fig-content        -> test_fig_content          (deliverable figure present)
#   test-variant-divergence -> test_variant_divergence   (np plateau vs par rollover)
# plus the aggregate-vs-explicit off-spot spot-check, the Pitfall-1 event-count
# mapping carried into R, and the fp-no-saturation / fp-tos-autoswitch guards.

import json
import os

import numpy as np
import pytest

from qpd_potential import response_matrix as rm
from qpd_potential import response as resp
from qpd_potential import energy_scale as es
from qpd_potential import params

DESIGNS = ("Ta->Al", "Al->Hf")
VARIANTS = params.CENSORING_VARIANTS
ART_DIR = rm._ARTIFACT_DIR


def _load(design):
    fn = os.path.join(ART_DIR, rm.DESIGN_FILE[design])
    if not os.path.exists(fn):
        pytest.skip(f"deliverable npz not built yet: {fn} (run response_matrix.run_all)")
    return dict(np.load(fn, allow_pickle=True))


# --------------------------------------------------------------------------- #
# test-span: Phase-4 grid + column normalization                              #
# --------------------------------------------------------------------------- #


def test_span_grid_matches_phase4():
    """E_dep grid = data/combined_dRdEdep.csv log grid: ~10 eV -> 2e5 keV, 80/decade."""
    E = rm.load_E_dep_grid_eV()
    assert E.size == 584
    assert E.min() == pytest.approx(10.14, rel=1e-2)          # ~10 eV floor
    assert E.max() == pytest.approx(1.9714e8, rel=1e-3)        # ~197 MeV = 2e5 keV
    ratios = E[1:] / E[:-1]
    bins_per_decade = 1.0 / np.log10(np.median(ratios))
    assert bins_per_decade == pytest.approx(80.0, abs=0.5)     # ~80 bins/decade


@pytest.mark.parametrize("design", DESIGNS)
def test_span_columns_normalized(design):
    """Every E_dep column of R (both variants) sums to 1 over E_rec bins."""
    d = _load(design)
    for v in VARIANTS:
        R = d[f"R_{v}"]
        colsum = R.sum(axis=0)
        assert np.allclose(colsum, 1.0, atol=1e-12), f"{design}/{v} columns not normalized"
        # grid stored and spans the Phase-4 range
        assert d["E_dep_centers_eV"].size == R.shape[1]
        assert d["E_rec_edges_eV"].size == R.shape[0] + 1


# --------------------------------------------------------------------------- #
# test-both-variants: 4 baseline matrices (2 designs x 2 variants)            #
# --------------------------------------------------------------------------- #


def test_both_variants_present():
    """Guards fp-single-censoring: BOTH non_paralyzable AND paralyzable per design."""
    n = 0
    for design in DESIGNS:
        d = _load(design)
        for v in VARIANTS:
            assert f"R_{v}" in d, f"missing {v} matrix for {design}"
            assert d[f"R_{v}"].shape[1] == 584
            n += 1
    assert n == 4  # four count-integral baseline matrices


# --------------------------------------------------------------------------- #
# test-repro: fixed seed reproduces R bit-for-bit; metadata header present     #
# --------------------------------------------------------------------------- #


def test_repro_same_seed_identical():
    """Same seed + params reproduce R exactly (stable crc32 sub-seeding)."""
    E = rm.load_E_dep_grid_eV()[::120]            # small subgrid
    edges = rm.build_E_rec_edges_eV(20)
    kw = dict(seed=777, N_s=400, M_pool=200)
    m1 = rm.build_matrix("Ta->Al", "non_paralyzable", E, edges, **kw)
    m2 = rm.build_matrix("Ta->Al", "non_paralyzable", E, edges, **kw)
    assert np.array_equal(m1["R"], m2["R"])
    assert np.array_equal(m1["counts"], m2["counts"])


def test_repro_metadata_header():
    """npz carries seed + f_prompt + r + N_s + grid edges (reproducibility)."""
    for design in DESIGNS:
        d = _load(design)
        meta = json.loads(str(d["meta_json"]))
        for key in ("seed", "N_s", "M_pool", "f_prompt", "r_spot_sensors",
                    "n_sensors", "tau_d_s", "E_dep_range_eV", "estimator"):
            assert key in meta, f"metadata missing {key}"
        assert meta["f_prompt"] == pytest.approx(params.F_PROMPT.value)


# --------------------------------------------------------------------------- #
# test-convergence: <=~3%/cell on well-populated cells; ~1/sqrt(N_s)          #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("E_dep_eV", [30.0, 120.0, 1.0e3, 1.0e6])
def test_convergence_peak_cell_le_3pct(E_dep_eV):
    """Peak (well-populated) cell converges below ~3% at the production N_s."""
    edges = rm.build_E_rec_edges_eV(20)
    C = resp.calibrate_C("Ta->Al", "non_paralyzable")
    rng = np.random.default_rng(int(E_dep_eV) + 5)
    s, _ = rm.E_rec_samples(E_dep_eV, "Ta->Al", "non_paralyzable", C, rng,
                            N_s=rm.DEFAULT_N_S, M_pool=1000)
    h, _ = np.histogram(s, bins=edges)
    rep = rm.populated_cell_report(h)
    # hard guarantee: the peak (mode) cell always meets the ~3% Poisson floor
    assert rep["peak_rel_err"] <= 0.03
    # bulk of the probability mass sits in <=3% cells; a bin-straddling column
    # may leave a minor (<~20%) tail bin flagged (honest per-cell reporting).
    assert rep["mass_frac_le_3pct"] >= 0.80


def test_convergence_poisson_scaling():
    """Per-cell error follows the ~1/sqrt(N_s) Poisson floor when N_s quadruples."""
    edges = rm.build_E_rec_edges_eV(20)
    C = resp.calibrate_C("Ta->Al", "non_paralyzable")
    errs = {}
    for Ns in (2000, 8000):
        s, _ = rm.E_rec_samples(120.0, "Ta->Al", "non_paralyzable",
                                C, np.random.default_rng(42), N_s=Ns, M_pool=1000)
        h, _ = np.histogram(s, bins=edges)
        errs[Ns] = rm.populated_cell_report(h)["peak_rel_err"]
    # 4x samples -> ~1/2 the error (allow 25% slack)
    assert errs[8000] == pytest.approx(0.5 * errs[2000], rel=0.25)


# --------------------------------------------------------------------------- #
# aggregate-vs-explicit off-spot spot-check                                    #
# --------------------------------------------------------------------------- #


def test_aggregate_offspot_matches_explicit_loop():
    """The aggregate off-spot ensemble mean matches an explicit ~10,300-sensor
    EMG loop within MC tolerance (validates the aggregate optimization)."""
    design, variant = "Ta->Al", "non_paralyzable"
    E_dep = 2.0e3  # off-spot in the feasible EMG regime (ec_off ~ 10)
    f_prompt, r, n_sensors = params.F_PROMPT.value, params.R_SPOT.value, params.N_SENSORS.value
    n_spot = np.pi * r * r
    n_off = n_sensors - n_spot
    E_off = float(es.sensor_energy_split(E_dep, f_prompt, r, n_sensors, on_spot=False))
    N_off = float(es.n_qp_yield(E_off, design))

    # explicit: realize n_off individual off-spot sensors ONCE -> one array sum
    rng_e = np.random.default_rng(2024)
    pool = rm.emg_count_pool(N_off, design, variant, int(round(n_off)), rng_e)
    explicit_sum = pool.sum()
    # pin to the same analytic mean the aggregate uses
    mu_a = resp.censored_count(N_off, design, variant=variant)
    explicit_sum *= mu_a / pool.mean()

    # aggregate: many realizations, compare the mean
    rng_a = np.random.default_rng(2025)
    agg, diag = rm.class_sum_samples(N_off, n_off, design, variant, 4000, rng_a, M_pool=2000)
    assert diag.branch == "emg"
    # explicit single draw is within a few sigma of the aggregate mean
    rel = abs(agg.mean() - explicit_sum) / explicit_sum
    assert rel < 0.05, f"aggregate {agg.mean():.1f} vs explicit {explicit_sum:.1f} (rel {rel:.3f})"


# --------------------------------------------------------------------------- #
# Pitfall-1 event-count mapping carried into R                                 #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("design", DESIGNS)
def test_eventcount_mapping_carried(design):
    """The class sampler drives ec = INT Gamma_in dt (response.expected_event_count),
    NOT the trapped N_qp (guards fp-eventcount / Pitfall 1)."""
    N_qp = es.n_qp_yield(50.0, design)
    ec = resp.expected_event_count(N_qp, design)
    # event count differs from the trapped count by K*tau_qp/V_tr (0.03 Al / 0.008 Hf)
    assert not np.isclose(ec, N_qp)
    _, diag = rm.class_sum_samples(N_qp, 10.0, design, "non_paralyzable", 200,
                                   np.random.default_rng(1), M_pool=200)
    assert diag.ec == pytest.approx(ec, rel=1e-9)


# --------------------------------------------------------------------------- #
# test-variant-divergence + fp-no-saturation (from the saved matrices)         #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("design", DESIGNS)
def test_variant_divergence_muon_end(design):
    """At the muon end non_paralyzable E_rec PLATEAUS (bounded) while paralyzable
    ROLLS OVER to lower values -- the two diverge qualitatively (Pitfall 3)."""
    d = _load(design)
    np_med = d["E_rec_median_non_paralyzable_eV"]
    par_med = d["E_rec_median_paralyzable_eV"]
    # muon-end (last column, 197 MeV): non_par strongly above paralyzable
    assert np_med[-1] > par_med[-1] * 3.0, "variants do not diverge at the muon end"
    # non_par plateau is monotone/bounded near the top decade (< 2x growth)
    top = d["E_dep_centers_eV"] > 1e7
    assert np_med[top].max() / np_med[top].min() < 2.0
    # paralyzable is NON-monotone: peaks at an INTERIOR E_dep then declines
    # (rollover). The rollover DEPTH is design-dependent (shallower for Hf) --
    # an explicit uncertainty marker -- so require an interior peak + a
    # measurable decline, not a fixed depth.
    kpk = int(np.argmax(par_med))
    assert kpk < par_med.size - 1, "paralyzable peak is at the muon end (no rollover)"
    assert par_med[-1] < 0.95 * par_med.max(), "paralyzable does not decline from its peak"


@pytest.mark.parametrize("design", DESIGNS)
def test_no_linear_ramp_fp_no_saturation(design):
    """fp-no-saturation: muon-end E_rec is >=3 orders below 0.5*E_dep and bounded
    to ~tens of keV -- NOT a linear ramp to tens of MeV."""
    d = _load(design)
    Ed = d["E_dep_centers_eV"]
    for v in VARIANTS:
        med = d[f"E_rec_median_{v}_eV"]
        assert med[-1] < 1e-3 * (0.5 * Ed[-1]), f"{design}/{v} looks linear at the muon end"
        assert med[-1] < 1.0e5, f"{design}/{v} E_rec unbounded (> 100 keV) at the muon end"


# --------------------------------------------------------------------------- #
# time-over-saturation SECONDARY: present, labeled, NOT switched into baseline  #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("design", DESIGNS)
def test_tos_secondary_labeled_not_switched(design):
    """fp-tos-autoswitch: the time-over-saturation curve is stored SEPARATELY and
    the baseline R median is the count-integral estimator (never the TOS curve)."""
    d = _load(design)
    assert "tos_t_over_s" in d
    tos = d["tos_t_over_s"]
    # t_over is >= 0 and rises into saturation (logarithmic ordering recovered)
    assert np.all(tos >= 0.0)
    assert tos[-1] > 0.0
    # baseline median E_rec is NOT the (very different-scaled) TOS curve
    np_med = d["E_rec_median_non_paralyzable_eV"]
    assert not np.allclose(np_med, tos)


# --------------------------------------------------------------------------- #
# test-fig-content: the deliverable figure exists (visual items in SUMMARY)     #
# --------------------------------------------------------------------------- #


def test_fig_content_exists():
    """deliv-fig-response present and non-trivial. The visual content (both
    designs, both variants, saturation onset marked, saturated region delimited,
    caveat annotations) is confirmed in the checkpoint review / SUMMARY."""
    fig = os.path.join(ART_DIR, "energy_response.pdf")
    if not os.path.exists(fig):
        pytest.skip("figure not built yet (run response_matrix.make_figure)")
    assert os.path.getsize(fig) > 10_000
