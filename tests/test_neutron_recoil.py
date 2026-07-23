# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Phase-13 Plan 13-01 acceptance tests for the Ge neutron elastic recoil fold.

EVERY tolerance is a module constant declared HERE, before any check runs, in the
Phase-9 pattern.  None of them is loosened afterwards.
"""
from __future__ import annotations

import os

import numpy as np
import pytest

from qpd_potential import neutron_recoil as nr

# --------------------------------------------------------------------------- #
# TOLERANCES -- declared before the checks run, not after                       #
# --------------------------------------------------------------------------- #
ORACLE_REL_TOL = 1.0e-3          # test-oracle, plan pass condition
ORACLE_F_SPREAD_TOL = 1.0e-5     # f-cancellation must be exact, not approximate
CONVERGENCE_TOL = 5.0e-3         # 0.5%, the Phase-9 tolerance for this quadrature
ANCHOR_LOSS_MIN_MAGNITUDE = 1.0e-4   # a run reporting ZERO everywhere FAILS
FLUX_MEDIAN_TOL = 0.01           # 09-02 Section 3.3, unchanged
FLUX_MAX_TOL = 0.05              # 09-02 Section 3.3, unchanged
CONTROL_RESONANCE_INTEGRAL_TOL = 0.05   # smoothing must preserve INT sigma dE
SUB5EV_ESCALATION_FACTOR = 3.0   # "a factor ~3" = the order-of-magnitude label
DIMENSIONAL_SCALING_TOL = 1.0e-12

#: A small, fixed recoil axis reused by the fast tests.
T_PROBE_eV = np.array([0.1, 1.0, 10.0, 100.0, 1000.0])


# --------------------------------------------------------------------------- #
# Frozen-artifact provenance                                                    #
# --------------------------------------------------------------------------- #
def test_header_numbers_are_parsed_not_transcribed():
    """fp-quote-from-prose: f, N_Ge and the resonance peak come from the file."""
    h = nr.elastic_header()
    raw = open(nr.ELASTIC_TABLE_PATH, encoding="utf-8").read(20000)
    assert f"= {h.f_natural}" in raw
    assert f"{h.resonance_peak_b:.2f} b" in raw
    # N_Ge/kg is DERIVED from the header, and agrees with CONVENTIONS D 8.29e24.
    assert abs(nr.n_ge_per_kg() / 8.29e24 - 1.0) < 5.0e-3
    # The natural peak reconstructed from the per-isotope table x IUPAC abundances
    # must reproduce the natural table's own header value.
    c = nr.resonance_carrier()
    assert abs(c["natural_peak_b"] / c["natural_peak_b_header"] - 1.0) < 1.0e-3


def test_kinematic_factor_matches_header_per_isotope():
    h = nr.elastic_header()
    for A, f_hdr in h.f_per_isotope.items():
        assert abs(nr.kinematic_factor(A) - f_hdr) < 5.0e-5


# --------------------------------------------------------------------------- #
# test-oracle                                                                   #
# --------------------------------------------------------------------------- #
def test_oracle_closed_form_and_exact_f_cancellation():
    """dR/dT = N sigma C / T for phi = C/E, constant sigma -- and f cancels.

    The f-independence is part of the pass condition, not a bonus: it is the
    analytic backbone of the Plan 13-02 SC4 adjudication.
    """
    T = np.array([0.1, 10.0, 1000.0])
    C, sigma_b = 2.24e-4, 8.9
    exact = nr.epithermal_oracle_dRdT(T, C_cm2_s=C, sigma_b=sigma_b)
    vals = []
    for f in (0.0215, 0.0536, 0.2215):
        v = nr.fold_synthetic_epithermal(T, f=f, C_cm2_s=C, sigma_b=sigma_b)
        assert np.max(np.abs(v / exact - 1.0)) <= ORACLE_REL_TOL, f
        vals.append(v)
    vals = np.asarray(vals)
    spread = np.max(np.abs(vals / vals[0] - 1.0))
    assert spread <= ORACLE_F_SPREAD_TOL, f"f-cancellation broke: spread {spread:.3e}"


def test_oracle_derivation_is_scale_linear():
    """N, sigma and C each enter linearly; T enters as 1/T. Checked, not assumed."""
    T = np.array([1.0, 100.0])
    base = nr.epithermal_oracle_dRdT(T, C_cm2_s=1e-4, sigma_b=10.0, n_per_kg=1e24)
    assert np.allclose(
        nr.epithermal_oracle_dRdT(T, C_cm2_s=2e-4, sigma_b=10.0, n_per_kg=1e24),
        2.0 * base, rtol=DIMENSIONAL_SCALING_TOL)
    assert np.allclose(
        nr.epithermal_oracle_dRdT(T, C_cm2_s=1e-4, sigma_b=20.0, n_per_kg=1e24),
        2.0 * base, rtol=DIMENSIONAL_SCALING_TOL)
    assert np.allclose(base * T, base[0] * T[0], rtol=DIMENSIONAL_SCALING_TOL)


# --------------------------------------------------------------------------- #
# test-convergence                                                              #
# --------------------------------------------------------------------------- #
def test_convergence_under_node_doubling():
    T = np.logspace(np.log10(nr.EXT_GRID_FLOOR_eV), 4.0, 60)
    y1 = nr.fold_dRdT(T, per_decade=200)
    y2 = nr.fold_dRdT(T, per_decade=400)
    rel = np.max(np.abs(y2 / y1 - 1.0))
    assert rel <= CONVERGENCE_TOL, f"node doubling moved dR/dT by {rel:.3e}"


# --------------------------------------------------------------------------- #
# test-anchor-loss                                                              #
# --------------------------------------------------------------------------- #
def test_anchor_loss_is_quantified_and_nonzero():
    """fp-unanchored-quadrature costs a NUMBER, not a warning.

    A run reporting zero difference at every T fails: it would mean neither route
    resolved the endpoint spike, so the 1/E^2 behaviour was never present.
    """
    T = np.logspace(np.log10(nr.EXT_GRID_FLOOR_eV), 4.0, 60)
    a = nr.anchor_loss(T, per_decade=200)
    rel = a["relative"]
    assert np.nanmax(np.abs(rel)) > ANCHOR_LOSS_MIN_MAGNITUDE
    # The endpoint segment carries positive integrand, so dropping it must lose
    # rate on balance: the median deficit is NEGATIVE.
    assert np.nanmedian(rel) < 0.0
    # And the plain log-substituted grid (no union nodes at all) is worse still.
    b = nr.anchor_loss(T, per_decade=50, include_union_nodes=False)
    assert abs(np.nanmedian(b["relative"])) > abs(np.nanmedian(rel))


# --------------------------------------------------------------------------- #
# test-dimensions (executable part of the hybrid check)                         #
# --------------------------------------------------------------------------- #
def test_dimensional_scaling_of_the_fold():
    """N_Ge and sigma enter linearly; the conversion chain is a fixed factor."""
    T = np.array([1.0, 50.0])
    y = nr.fold_dRdT(T, n_per_kg=1.0e24)
    y2 = nr.fold_dRdT(T, n_per_kg=2.0e24)
    assert np.allclose(y2, 2.0 * y, rtol=DIMENSIONAL_SCALING_TOL)
    s = nr.sigma_for_fold_b
    y3 = nr.fold_dRdT(T, n_per_kg=1.0e24,
                      sigma_b_fn=lambda e: 3.0 * s(e))
    assert np.allclose(y3, 3.0 * y, rtol=DIMENSIONAL_SCALING_TOL)


def test_conversion_constants_are_named():
    """No unexplained numerical constant: the chain is exactly these four."""
    assert nr.BARN_TO_CM2 == 1.0e-24
    assert nr.EV_PER_MEV == 1.0e6
    assert nr.EV_PER_KEV == 1.0e3
    assert nr.SECONDS_PER_DAY == 86400.0


# --------------------------------------------------------------------------- #
# Operative flux column                                                         #
# --------------------------------------------------------------------------- #
def test_phi_lo_and_band_midpoint_raise():
    """fp-indoor-band-as-central: the fivefold flattering move is unavailable."""
    for bad in ("phi_lo", "PHI_LO", "midpoint", "band_midpoint", "indoor"):
        with pytest.raises(nr.FluxColumnError):
            nr.neutron_flux_cm2_s_MeV([100.0], column=bad)
    # and the operative column still works
    assert nr.neutron_flux_cm2_s_MeV([100.0])[0] > 0.0


# --------------------------------------------------------------------------- #
# test-flux-overlap / test-gap-closed                                           #
# --------------------------------------------------------------------------- #
def test_flux_overlap_against_both_committed_tables():
    ov = nr.flux_overlap_check()
    assert set(ov) == {"v1.1", "thermal_v2.0"}
    for name, v in ov.items():
        assert abs(v["median_rel"]) <= FLUX_MEDIAN_TOL, name
        assert v["max_abs_rel"] <= FLUX_MAX_TOL, name
        assert v["n_gt_1pct"] == 0 and v["n_gt_5pct"] == 0, name
    # The v1.1 deviation pattern IS the known uniform k-rounding offset; it is
    # reported rather than smoothed over.
    assert ov["v1.1"]["consistent_with_k_rounding"]


def test_gap_is_real_and_closed_by_the_driver():
    g = nr.flux_gap()
    assert g["gap_lo_eV"] < g["gap_hi_bin_edge_eV"] <= g["gap_hi_bin_centre_eV"]
    # Recoils below this T are fed from inside the gap.
    assert 0.4 < g["T_below_which_gap_contributes_eV"] < 0.7
    # The driver returns finite positive flux across the whole gap.
    E = np.logspace(np.log10(g["gap_lo_eV"]),
                    np.log10(g["gap_hi_bin_centre_eV"]), 41)
    phi = nr.neutron_flux_cm2_s_MeV(E)
    assert np.all(np.isfinite(phi)) and np.all(phi > 0)
    # Neither committed table has ANY node strictly inside the gap: an
    # interpolation across it would be an extrapolation of both.
    v11 = nr.read_flux_v11()["E_n_eV"]
    th = nr.read_flux_thermal()["E_n_eV"]
    inner = 0.5 * (g["gap_lo_eV"] + g["gap_hi_bin_edge_eV"])
    assert not np.any((v11 > g["gap_lo_eV"]) & (v11 < g["gap_hi_bin_edge_eV"]))
    assert not np.any((th > g["gap_lo_eV"]) & (th < g["gap_hi_bin_edge_eV"]))
    assert th.max() <= g["gap_lo_eV"] and v11.min() >= g["gap_hi_bin_edge_eV"]
    assert g["gap_lo_eV"] < inner < g["gap_hi_bin_edge_eV"]


def test_subeV_recoils_are_fed_by_gap_nodes():
    """A dR/dT below 0.54 eV produced without gap coverage would be wrong."""
    g = nr.flux_gap()
    T = np.array([nr.EXT_GRID_FLOOR_eV, 0.3])
    d = nr.fold_dRdT(T, return_detail=True)
    nodes = d["nodes_eV"]
    inside = (nodes > g["gap_lo_eV"]) & (nodes < g["gap_hi_bin_centre_eV"])
    assert inside.sum() > 10
    # E_min(T) itself lands inside the gap for both probe energies.
    emin = nr.E_min_eV(T)
    assert np.all(emin > g["gap_lo_eV"]) and np.all(emin < g["gap_hi_bin_centre_eV"])


# --------------------------------------------------------------------------- #
# test-imprint-present / test-imprint-rejects-smooth / test-edge-smearing        #
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def imprint_pair():
    _, T = nr.native_recoil_axis()
    y = nr.fold_dRdT(T)
    y_c = nr.fold_dRdT(T, sigma_b_fn=nr.smoothed_sigma_fn())
    return T, y, y_c


def test_imprint_present(imprint_pair):
    T, y, _ = imprint_pair
    s = nr.imprint_statistic(T, y)
    assert s["passes"], s
    c = nr.resonance_carrier()
    assert c["edge_window_lo_eV"] <= s["T_at_max_eV"] <= c["edge_window_hi_eV"]


def test_imprint_rejects_smoothed_control(imprint_pair):
    """The decisive check: a statistic BOTH spectra pass would be worthless."""
    T, y, y_c = imprint_pair
    real = nr.imprint_statistic(T, y)
    ctrl = nr.imprint_statistic(T, y_c)
    assert real["passes"] and not ctrl["passes"], (real, ctrl)
    assert real["excursion"] > 10.0 * ctrl["excursion"]
    # The control must be a fair one: it preserves the resonance integral.
    chk = nr.control_resonance_integral_check()
    assert abs(chk["relative_change"]) <= CONTROL_RESONANCE_INTEGRAL_TOL


def test_imprint_statistic_is_resolution_stable(imprint_pair):
    """Excludes 'the structure is a quadrature/binning artefact'."""
    for bpd in (200, 800):
        _, T = nr.native_recoil_axis(bins_per_decade=bpd)
        y = nr.fold_dRdT(T)
        y_c = nr.fold_dRdT(T, sigma_b_fn=nr.smoothed_sigma_fn())
        assert nr.imprint_statistic(T, y)["passes"]
        assert not nr.imprint_statistic(T, y_c)["passes"]


def test_edge_is_a_measured_band_with_a_named_carrier():
    c = nr.resonance_carrier()
    assert c["carrier_A"] == 73
    assert c["carrier_fraction_of_natural_peak"] > 0.9
    # The single natural f misplaces the edge relative to the carrier's own f.
    off = c["edge_natural_f_eV"] / c["edge_carrier_eV"] - 1.0
    assert 0.0 < off < 0.02
    assert c["edge_window_lo_eV"] < c["edge_carrier_eV"] < c["edge_window_hi_eV"]


def test_per_isotope_fold_places_the_edge_at_the_carrier_energy():
    """Five per-isotope boxes, each with its OWN f -- the edge moves as predicted."""
    _, T = nr.native_recoil_axis(bins_per_decade=800)
    m = (T > 4.5) & (T < 6.5)
    y_iso = nr.per_isotope_edge_fold(T[m])
    y_nat = nr.fold_dRdT(T[m])
    c = nr.resonance_carrier()
    s_iso = np.abs(np.gradient(np.log(y_iso), np.log(T[m])))
    s_nat = np.abs(np.gradient(np.log(y_nat), np.log(T[m])))
    t_iso = float(T[m][int(np.argmax(s_iso))])
    t_nat = float(T[m][int(np.argmax(s_nat))])
    assert abs(t_iso / c["edge_carrier_eV"] - 1.0) < 0.01, t_iso
    assert abs(t_nat / c["edge_natural_f_eV"] - 1.0) < 0.01, t_nat
    assert t_iso < t_nat  # the carrier's f is smaller than the natural f


# --------------------------------------------------------------------------- #
# test-no-freegas-below-5ev / test-sub5ev-route-declared / band bound            #
# --------------------------------------------------------------------------- #
def test_no_free_atom_evaluation_below_the_seam_reaches_the_spectrum():
    """EXECUTED guard, not an inspection claim (fp-free-gas-below-5ev)."""
    tripwire = nr.free_atom_tripwire_b()
    assert tripwire > 20.0    # the 1/v upturn this guard protects against
    _, T = nr.native_recoil_axis(bins_per_decade=100)
    for route in ("ncrystal_splice", "truncate"):
        nr.reset_free_atom_counter()
        nr.fold_dRdT(T, route=route, per_decade=100)
        assert nr.free_atom_below_seam_evaluations() == 0, route
    # ...and the counter is not vacuous: the forbidden route does trip it.
    nr.reset_free_atom_counter()
    nr.fold_dRdT(T[:50], route="free_gas", per_decade=100)
    assert nr.free_atom_below_seam_evaluations() > 0
    nr.reset_free_atom_counter()


def test_exactly_one_sub5ev_route_is_declared_with_a_measured_seam():
    assert nr.SUB5EV_ROUTE_DECLARED in ("ncrystal_splice", "truncate")
    assert nr.SUB5EV_ROUTE_DECLARED != "free_gas"
    if nr.SUB5EV_ROUTE_DECLARED == "ncrystal_splice":
        s = nr.seam_discontinuity()
        assert s["seam_eV"] == nr.SUB5EV_SEAM_eV
        assert abs(s["relative_step"]) < 0.2      # a reported number, not a hope
        assert s["sigma_ncrystal_bound_b"] > 0.0


def test_sub5ev_band_bound_and_escalation_rule():
    stake = nr.sub5ev_stake()
    # Kinematics, not approximation: sub-5 eV neutrons cannot reach the RoI.
    assert stake["T_edge_eV"] < nr.ROI_LO_eV
    roi = stake["bands"]["RoI"]
    assert abs(roi["truncate_omission_fraction"]) == 0.0
    # The escalation rule is EVALUATED, not skipped.
    for name, b in stake["bands"].items():
        assert abs(b["truncate_omission_fraction"]) < SUB5EV_ESCALATION_FACTOR, name
    # The declared route's residual model uncertainty (bound vs free-atom) is the
    # number that actually stands, and it is small.
    assert abs(stake["bottom_bin"]["free_gas_vs_ncrystal_fraction"]) < 0.1


# --------------------------------------------------------------------------- #
# Emitted artifacts                                                             #
# --------------------------------------------------------------------------- #
def test_emitted_tables_exist_and_carry_the_label():
    for p in (nr.DRDT_CSV, nr.FLUX_CONTINUITY_CSV):
        assert os.path.exists(p), p
        head = "".join(open(p, encoding="utf-8").readlines()[:80])
        assert "accuracy_label = order_of_magnitude" in head
        assert "phi_lo NOT USED" in head
        assert "T_max/E_n = 0.0536" in head or "f = T_max/E_n = 0.0536" in head
    head = "".join(open(nr.DRDT_CSV, encoding="utf-8").readlines()[:120])
    assert f"sub5eV_disposition = {nr.SUB5EV_ROUTE_DECLARED}" in head
    assert "git_sha" in head


def test_emitted_dRdT_reproduces_the_module():
    t = nr.read_dRdT_table()
    _, T = nr.native_recoil_axis()
    assert np.allclose(t["T_eV"], T, rtol=1e-9)
    y = nr.fold_dRdT(T)
    assert np.max(np.abs(t["dRdT"] / y - 1.0)) < 1.0e-6
    assert t["T_eV"][0] > 0.0999 and t["T_eV"][0] < 0.101


def test_spectrum_is_positive_monotone_and_reaches_the_floor():
    t = nr.read_dRdT_table()
    assert np.all(t["dRdT"] > 0)
    # dR/dT is a suffix integral of a positive integrand, so it is non-increasing.
    assert np.all(np.diff(t["dRdT"]) <= 0)
    edges, _ = nr.native_recoil_axis()
    assert abs(edges[0] - nr.EXT_GRID_FLOOR_eV) < 1e-12


def test_no_shielded_or_indoor_token_in_the_module_or_artifacts():
    """fp-shielded-quantity-leak, reusing the Phase-9 shielded-token machinery."""
    import sys
    sys.path.insert(0, os.path.join(nr.REPO_ROOT, "tests"))
    from test_env_v1_identity import is_not_applied, scan_paths  # noqa: E402

    paths = [nr.__file__, nr.DRDT_CSV, nr.FLUX_CONTINUITY_CSV]
    hits = [h for h in scan_paths(paths) if not is_not_applied(h[3])]
    assert hits == [], f"shielded token APPLIED in the neutron channel: {hits}"


def test_no_phi_lo_use_in_the_module_or_artifacts():
    """fp-indoor-band-as-central: phi_lo appears only as a REFUSAL."""
    import re as _re
    paths = [nr.__file__, nr.DRDT_CSV, nr.FLUX_CONTINUITY_CSV]
    #: Markers that make a phi_lo mention a DEFINITION or a REFUSAL rather than
    #: a use.  A new line that actually consumed phi_lo would match none of them.
    allow = ("not used", "raise", "indoor", "refus", "not selectable",
             "fp-indoor", "phi_default/5", "not returned", "not an error bar",
             "would cut this background")
    for p in paths:
        for i, line in enumerate(open(p, encoding="utf-8"), 1):
            low = line.lower()
            if "phi_lo" in low and not any(a in low for a in allow):
                raise AssertionError(f"{p}:{i} uses phi_lo: {line.rstrip()}")
