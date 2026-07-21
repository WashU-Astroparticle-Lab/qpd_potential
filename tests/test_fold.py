# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
#
# Plan 06-01 acceptance tests for the fold pipeline (qpd_potential.fold).
# Contract acceptance tests:
#   test-counts-conservation -> test_counts_conservation_*  (sum N_rec == sum N_dep)
#   test-erec-axis           -> test_erec_axis_*            (E_rec axis; muon saturates)
#   test-cevns-rebin         -> test_cevns_rebin_*          (total <1%, >50 eV <2%)
#   test-lowedge-retained    -> test_lowedge_retained       (5-10.14 eV carried)
# plus the forbidden-proxy guards:
#   fp-deposited-only  -> test_fp_deposited_only  (peak moved off the deposit axis)
#   fp-drop-lowE-cevns -> test_lowedge_retained
#   fp-paralyzable-swap-> test_fp_paralyzable_swap (only non-paralyzable folded)

import os

import numpy as np
import pytest

from qpd_potential import fold
from qpd_potential import response_matrix as rm

DESIGNS = ("Ta->Al", "Al->Hf")
CEVNS_ABOVE_50_HEADER = 67.752  # counts/kg/day (cevns_dRdT.csv header)


def _have_npz(design):
    return os.path.exists(os.path.join(fold._ARTIFACT_DIR, rm.DESIGN_FILE[design]))


def _require(design):
    if not _have_npz(design):
        pytest.skip(f"response matrix npz not built for {design}")


def _trapz_ref():
    c = fold.read_cevns()
    T, y = c["T_eV"], c["dRdT_total"]
    return np.trapz(y, T / 1.0e3), np.trapz(y[T >= 50.0], T[T >= 50.0] / 1.0e3)


# --------------------------------------------------------------------------- #
# test-counts-conservation                                                    #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("design", DESIGNS)
def test_counts_conservation(design):
    _require(design)
    res = fold.run_fold(design, write=False)
    cc = fold.counts_conservation(res)
    # muon / Compton: R columns sum to 1 -> exact to fp round-off.
    assert cc["muon"]["rel"] <= 1e-9
    assert cc["compton"]["rel"] <= 1e-9
    # CEvNS: fold + low-edge conserves the rebinned deposited counts (rebin
    # tolerance vs the raw spectrum is checked separately in test_cevns_rebin).
    assert cc["cevns"]["rel"] <= 1e-2


# --------------------------------------------------------------------------- #
# test-cevns-rebin                                                            #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("design", DESIGNS)
def test_cevns_rebin(design):
    _require(design)
    d = fold.load_design(design)
    reb = fold.rebin_cevns_to_edep_grid(d["E_dep_edges_eV"])
    ref_total, _ = _trapz_ref()
    rebinned_total = reb["counts"].sum() + reb["low_counts"].sum()
    # (1) total rebinned counts within 1% of the trapezoidal integral 5-3200 eV
    assert abs(rebinned_total - ref_total) / ref_total <= 1e-2
    # (2) above-50-eV integral within 2% of the frozen 67.752 counts/kg/day
    ctr = d["E_dep_centers_eV"]
    above50 = reb["counts"][ctr >= 50.0].sum()
    assert abs(above50 - CEVNS_ABOVE_50_HEADER) / CEVNS_ABOVE_50_HEADER <= 2e-2
    # (3) support: nothing above 3200 eV and the grid tops out at the CEvNS range
    assert reb["counts"][ctr > 3200.0].sum() == 0.0


# --------------------------------------------------------------------------- #
# test-lowedge-retained  (fp-drop-lowE-cevns guard)                           #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("design", DESIGNS)
def test_lowedge_retained(design):
    _require(design)
    d = fold.load_design(design)
    reb = fold.rebin_cevns_to_edep_grid(d["E_dep_edges_eV"])
    # The 5 - floor(~10.14 eV) band carries nonzero counts, reconstructed at
    # E_rec = 0.5*E_dep (i.e. ~2.5 - 5 eV) rather than being dropped.
    assert reb["low_counts"].sum() > 0.0
    assert np.all(reb["low_Erec_eV"] < reb["floor_eV"] * fold.LOW_E_SLOPE + 1e-9)
    assert reb["low_Erec_eV"].min() >= fold.LOW_E_SLOPE * reb["T_min_eV"] - 1e-9
    # Those counts appear in the reconstructed CEvNS spectrum in the E_rec bins
    # covering ~2.5-5 eV (below where the folded main-grid CEvNS would reach).
    res = fold.run_fold(design, write=False)
    edges = res["E_rec_edges_eV"]
    lo, hi = 0.5 * reb["T_min_eV"], reb["floor_eV"] * fold.LOW_E_SLOPE
    band_bins = (edges[:-1] >= lo * 0.99) & (edges[1:] <= hi * 1.01)
    assert res["N_rec_cevns"][band_bins].sum() > 0.0


# --------------------------------------------------------------------------- #
# test-erec-axis  (fp-deposited-only guard)                                    #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("design", DESIGNS)
def test_erec_axis_muon_saturates(design):
    _require(design)
    d = fold.load_design(design)
    res = fold.run_fold(design, write=False)
    # Output axis is derived from the npz E_rec grid.
    assert np.allclose(res["E_rec_centers_eV"], d["E_rec_centers_eV"])
    centers = res["E_rec_centers_eV"]
    edges = res["E_rec_edges_eV"]
    n_muon = res["N_rec_muon"]
    # muon reconstructed peak sits at TENS OF keV (bounded plateau), not at the
    # ~0.5*E_dep the deposit axis would give.
    jpk = int(np.argmax(n_muon[1:]) + 1)
    peak_keV = centers[jpk] / 1.0e3
    assert 5.0 < peak_keV < 100.0
    # Contrast with the deposited axis: muon counts-weighted median deposit is
    # MeV-scale, so a linear (no-saturation) reconstruction would land near ~1 MeV
    # -- above the 100 keV E_rec grid cap.  Saturation compressed it to tens of keV.
    muon = fold.read_channel_dRdEdep(fold.MUON_CSV)
    N_dep = fold.dep_counts_from_dRdEdep(muon["dRdEdep"], d["E_dep_edges_eV"])
    cE = d["E_dep_centers_eV"]
    cdf = np.cumsum(N_dep) / N_dep.sum()
    median_dep_keV = cE[np.searchsorted(cdf, 0.5)] / 1.0e3
    assert median_dep_keV > 1.0e3  # > 1 MeV deposit
    assert peak_keV < median_dep_keV / 10.0  # reconstruction strongly compressed
    # no muon support above the 100 keV E_rec ceiling
    assert n_muon[edges[:-1] >= 1.0e5].sum() == 0.0


@pytest.mark.parametrize("design", DESIGNS)
def test_fp_deposited_only(design):
    """The reconstructed spectrum is NOT the deposited spectrum (an identity/no-op
    response) -- the peak moved off the deposit axis for the saturating channel."""
    _require(design)
    d = fold.load_design(design)
    res = fold.run_fold(design, write=False)
    cE = d["E_dep_centers_eV"]
    muon = fold.read_channel_dRdEdep(fold.MUON_CSV)
    N_dep = fold.dep_counts_from_dRdEdep(muon["dRdEdep"], d["E_dep_edges_eV"])
    peak_dep_keV = cE[int(np.argmax(N_dep))] / 1.0e3
    centers = res["E_rec_centers_eV"]
    peak_rec_keV = centers[int(np.argmax(res["N_rec_muon"][1:]) + 1)] / 1.0e3
    # deposited muon peak is MeV-scale; reconstructed peak is tens of keV.
    assert peak_dep_keV > 1.0e3
    assert peak_rec_keV < 100.0


# --------------------------------------------------------------------------- #
# fp-paralyzable-swap guard: only the non-paralyzable R is folded               #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("design", DESIGNS)
def test_fp_paralyzable_swap(design):
    _require(design)
    d = fold.load_design(design)
    # run_fold must fold R_non_paralyzable, reproducible by an explicit fold.
    res = fold.run_fold(design, write=False)
    R_np = d["R_non_paralyzable"]
    muon = fold.read_channel_dRdEdep(fold.MUON_CSV)
    N_dep = fold.dep_counts_from_dRdEdep(muon["dRdEdep"], d["E_dep_edges_eV"])
    N_rec_np = R_np @ N_dep
    assert np.allclose(res["N_rec_muon"], N_rec_np)
    # and it is genuinely the non-paralyzable one (paralyzable gives a different
    # muon reconstruction -- retained only as a sensitivity).
    R_par = d["R_paralyzable"]
    N_rec_par = R_par @ N_dep
    assert not np.allclose(res["N_rec_muon"], N_rec_par, rtol=0.05)


# --------------------------------------------------------------------------- #
# CSV deliverables: written with all channels + bands                          #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("design", DESIGNS)
def test_reconstructed_csv_schema(design, tmp_path):
    _require(design)
    res = fold.run_fold(design, write=True, out_dir=str(tmp_path))
    path = res["_path"]
    assert os.path.exists(path)
    header_cols = None
    rows = 0
    with open(path) as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if header_cols is None:
                header_cols = s.split(",")
                continue
            rows += 1
    assert header_cols == fold._CSV_COLUMNS
    assert rows == d_erec_bins(design)


def d_erec_bins(design):
    d = fold.load_design(design)
    return d["E_rec_centers_eV"].size - 1  # underflow bin dropped in the CSV


def test_cevns_reconstructs_low():
    """Honest landing: the CEvNS channel reconstructs to tens of eV (E_rec ~
    0.5*E_dep), i.e. very low -- surfaced, not forced."""
    _require("Ta->Al")
    rep = fold.landing_report(("Ta->Al", "Al->Hf"))
    for design in ("Ta->Al", "Al->Hf"):
        cev = rep["designs"][design]["cevns"]
        assert cev["peak_Erec_keV"] < 1.0  # sub-keV reconstruction
        assert cev["integrated_rate_cts_per_kg_day"] > 0.0
