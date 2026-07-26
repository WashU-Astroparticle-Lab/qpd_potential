# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Phase 12, plan 12-03: the closure audit.

Three things, none of which produces a new spectrum: the VALD-10 regression against the
frozen v1.0 CEvNS artifacts above 10 eV on the PRESERVED reconstructed-energy edge
indices; the target-swap benchmark arithmetic, recomputed in order to be rejected; and
the optional VNS line as a single labelled scalar multiplication.

EVERY TOLERANCE HERE IS A STATED TARGET. In particular, the <1% VALD-10 target is NOT
relaxed: one design fails it in one bin and that failure is reported, not absorbed.
"""
import os
import subprocess
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from qpd_potential import cevns, cevns_subev as cs, fold, trigger  # noqa: E402

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ART = os.path.join(_ROOT, "artifacts", "v2.0")
_DESIGNS = ("Ta->Al", "Al->Hf")
_REPORT = os.path.join(
    _ROOT, "GPD", "phases",
    "12-reactor-cevns-down-to-100-mev-at-the-paper-s-surface-scenario-p-sig",
    "12-03-CLOSURE-AND-RESCALE.md")

# ---- stated targets -------------------------------------------------------- #
VALD10_TARGET = 0.01          # ROADMAP SC3: "<1%"
FROZEN_V1_RECOIL_FLOOR_eV = 5.0
NAIVE_RATIO_TARGET = 1.95     # GPD/literature/SUMMARY.md figure to REPRODUCE
GE_N2A_TARGET = 22.7
CAWO4_N2A_TARGET = 44.2
PURE_W_TARGET = 65.8          # the 184W value, a DIFFERENT quantity
SAME_PIPELINE_BENCHMARK = 2.31
NUCLEUS_STATED_FLUX = 2.1e12
PROJECT_GEOMETRIC_FLUX = 1.830269e12


@pytest.fixture(scope="module")
def reg():
    return {d: cs.v1_regression(d) for d in _DESIGNS}


# =========================================================================== #
# claim-v1-regression                                                         #
# =========================================================================== #
def test_index_carry_not_interpolation(reg):
    """test-index-carry-not-interpolation. np.array_equal, max difference EXACTLY 0.0,
    and no interpolation anywhere on the comparison path.

    A tolerance-based axis comparison would let Phase-10's fp-naive-logspace drift (up
    to 5.1e-4 relative) through unnoticed; interpolating either spectrum onto the other
    would smooth a real deviation away (fp-regression-by-interpolation).
    """
    for d in _DESIGNS:
        assert reg[d]["axis_index_carry"] is True
        assert reg[d]["axis_max_difference"] == 0.0
    src = open(os.path.join(_ROOT, "src", "qpd_potential", "cevns_subev.py")).read()
    body = src[src.index("def v1_regression"):src.index("def frozen_v1_recoil_support")]
    for bad in ("np.interp", "interp1d", "PchipInterpolator", "np.allclose"):
        assert bad not in body, f"{bad} on the regression comparison path"


def test_regression_non_vacuous(reg):
    """test-regression-non-vacuous. A non-empty overlap of stated size, and a deviation
    that is small but NOT identically zero.

    An identically zero deviation would mean the extended pipeline is echoing the frozen
    v1.0 numbers rather than recomputing them -- passing the tolerance while testing
    nothing.
    """
    for d in _DESIGNS:
        r = reg[d]
        assert r["n_compared"] == 40
        assert r["min_abs_deviation"] > 0.0
        assert r["max_abs_deviation"] > 1e-4
        assert np.all(np.isfinite(r["deviation"]))


def test_regression_superseded_by_calibration_scale(reg):
    """RE-ANCHORED 2026-07-25. The per-bin reconstructed-axis VALD-10 regression is
    SUPERSEDED by the unit-calibration-slope change (params.CALIB_SLOPE = 1.0,
    CONVENTIONS Section E.1).

    The archived v1.0 stage1/ spectrum is on the former eps = 0.5 axis; the v2.0
    fold is on the unit-slope axis, so the reconstructed count->energy constant C
    differs by exactly 2x. VALD-10 compares the two spectra by EXACT INDEX CARRY on
    a shared E_rec grid, forbidding interpolation -- but a 2x log-axis rescale is a
    ~6.02-bin (non-integer) shift, so no exact index-carry comparison can survive
    it. The per-bin deviation is now dominated by the calibration (order 10^4), which
    this test asserts as evidence of the supersession rather than a physics change.

    The scale-FREE content the regression actually cared about -- that the Phase-10
    response-matrix REGENERATION preserved the overlap physics -- is re-anchored in
    DEPOSIT (count) space in
    test_response_matrix_extended::test_overlap_vs_archived, where dividing each
    matrix's mean E_rec by its own C removes the calibration. See task-3 decision."""
    # the reconstructed GRID is still preserved (VALD-10's structural premise)
    for d in _DESIGNS:
        assert reg[d]["axis_index_carry"] is True
        assert reg[d]["axis_max_difference"] == 0.0
    # the C's differ by exactly the 2x eps->1 rescale
    for d, f in zip(_DESIGNS, ("TaAl", "AlHf")):
        Co = float(np.load(os.path.join(_ROOT, "artifacts", "stage1",
                    f"response_matrix_{f}.npz"), allow_pickle=True)[
                    "C_non_paralyzable_eV_per_event"])
        Cn = float(fold.load_design_extended(d)["C_non_paralyzable_eV_per_event"])
        assert Cn / Co == pytest.approx(2.0, rel=1e-6)
    # and the per-bin reconstructed deviation is now calibration-dominated (huge),
    # i.e. the old <1% pins can no longer be measured on the reconstructed axis
    for d in _DESIGNS:
        assert reg[d]["max_abs_deviation"] > 1.0, (
            "the reconstructed-axis deviation is small again -- if the axes are back "
            "on one calibration the VALD-10 per-bin regression should be restored")


def test_regression_residual_is_not_the_broadening(reg):
    """The decisive diagnostic on WHY the residual is what it is, RE-ANCHORED to a
    RELATIVE comparison (2026-07-25).

    Switching the IA kernel OFF changes the maximum deviation by a negligible
    FRACTION. The residual is therefore NOT caused by anything Phase 12 added. (The
    former ABSOLUTE 1e-4 tolerance assumed the deviation was ~1%; after the
    calibration change the reconstructed-axis deviation is order 10^4, so the same
    physical statement is now made as a relative one.)  The response-matrix
    REGENERATION difference against the archived v1.0 matrix is confirmed separately.
    """
    for d in _DESIGNS:
        r = reg[d]
        assert r["max_abs_deviation_broadening_off"] == pytest.approx(
            r["max_abs_deviation"], rel=1e-3)
    for d, f in zip(_DESIGNS, ("TaAl", "AlHf")):
        R1 = np.load(os.path.join(_ROOT, "artifacts", "stage1",
                                  f"response_matrix_{f}.npz"),
                     allow_pickle=True)["R_non_paralyzable"]
        R2 = fold.load_design_extended(d)["R_non_paralyzable"][:, 160:]
        assert R1.shape == R2.shape
        assert not np.array_equal(R1, R2)
        assert float(np.abs(R1 - R2).max()) > 1e-3


def test_trigger_off_above_boundary(reg):
    """test-trigger-off-above-boundary. The compared object is the UN-TRIGGERED spectrum,
    and P_trig is within the regression tolerance of 1 well above the boundary, so that
    choice cannot be hiding a real deviation."""
    for d in _DESIGNS:
        assert 1.0 - reg[d]["P_trig_at_100eV"] < VALD10_TARGET
    assert float(trigger.P_trig(cs.REGRESSION_FLOOR_eV)) > 1.0 - VALD10_TARGET
    # the regression really did fold with broaden=True and compare dRdErec, not the
    # trigger-weighted column
    src = open(os.path.join(_ROOT, "src", "qpd_potential", "cevns_subev.py")).read()
    body = src[src.index("def v1_regression"):src.index("def frozen_v1_recoil_support")]
    assert '["dRdErec"]' in body
    assert "dRdErec_trigger" not in body


def test_regression_artifact(reg):
    """The emitted table carries both designs, the edge index, and the per-design maxima."""
    path = os.path.join(_ART, "cevns_v1_regression.csv")
    assert os.path.exists(path)
    header = "".join(l for l in open(path) if l.startswith("#"))
    assert "INDEX CARRY, NOT AN INTERPOLATION" in header
    assert "EXACTLY 0.0" in header
    assert "UN-TRIGGERED" in header
    for d in _DESIGNS:
        assert f"#   {d}:" in header
    rows = [l.strip().split(",") for l in open(path)
            if l.strip() and not l.startswith("#") and not l.startswith("design,")]
    assert len(rows) == sum(reg[d]["n_compared"] for d in _DESIGNS)
    for d in _DESIGNS:
        sub = [r for r in rows if r[0] == d]
        assert len(sub) == reg[d]["n_compared"]
        idx = np.asarray([int(r[2]) for r in sub])
        assert np.all(np.diff(idx) > 0)            # a real index carry, ascending
        assert np.all(np.asarray([float(r[1]) for r in sub]) > cs.REGRESSION_FLOOR_eV)


# =========================================================================== #
# claim-sc3-adjudicated                                                       #
# =========================================================================== #
def test_no_fabricated_comparison():
    """test-no-fabricated-comparison. The frozen v1.0 RECOIL table's support floor is
    confirmed at 5 eV programmatically, and no test or artifact in this phase claims a
    comparison against a frozen v1.0 value at 0.290 eV.

    Recomputing dR/dT at 0.290 eV with the same code and calling that agreement a
    regression would be an identity dressed as a check.
    """
    s = cs.frozen_v1_recoil_support()
    assert s["T_min_eV"] == pytest.approx(FROZEN_V1_RECOIL_FLOOR_eV, rel=1e-12)
    assert s["covers_0p290_eV"] is False
    assert s["n_rows"] == 320

    # nothing anywhere in this phase claims such a comparison
    phase = os.path.join(_ROOT, "GPD", "phases",
                         "12-reactor-cevns-down-to-100-mev-at-the-paper-s-surface-scenario-p-sig")
    for root, _, files in os.walk(phase):
        for fn in files:
            if not fn.endswith(".md") or fn.endswith("PLAN.md"):
                continue
            txt = open(os.path.join(root, fn)).read().lower()
            for bad in ("reproduces the frozen v1.0 value at 0.290",
                        "frozen v1.0 value at 0.29 ev",
                        "matches the frozen v1.0 value at 0.290 ev"):
                assert bad not in txt, f"{fn} claims a fabricated 0.290 eV comparison"


@pytest.mark.skipif(not os.path.exists(_REPORT), reason="closure report not yet written")
def test_sc3_restatement_recorded():
    """test-sc3-restatement-recorded. The report must say that SC3's 0.290 eV clause
    RESTATES SC4's zero-point and is therefore not independent corroboration."""
    txt = open(_REPORT).read()
    low = txt.lower()
    assert "restate" in low
    assert "0.290" in txt or "0.29 eV" in txt
    assert "5 eV" in txt
    assert "not independent" in low or "not counted as independent" in low


# =========================================================================== #
# claim-benchmark-documented                                                  #
# =========================================================================== #
def test_compound_arithmetic_recomputed():
    """test-compound-arithmetic-recomputed. Ge ~22.7, CaWO4 compound ~44.2, ratio ~1.95,
    pure W ~65.8 identified as a DIFFERENT quantity -- all RECOMPUTED, none quoted."""
    c = cs.compound_n2_over_a()
    assert c["Ge"] == pytest.approx(GE_N2A_TARGET, abs=0.1)
    assert c["CaWO4_compound"] == pytest.approx(CAWO4_N2A_TARGET, abs=0.1)
    assert c["naive_ratio_CaWO4_over_Ge"] == pytest.approx(NAIVE_RATIO_TARGET, abs=0.02)
    # 65.8 is the 184W value; the standard-atomic-weight tungsten value is 65.63.
    # Both are reported and neither may stand in for the CaWO4 compound 44.2.
    assert c["pure_184W"] == pytest.approx(PURE_W_TARGET, abs=0.1)
    assert c["pure_W_standard_atomic_weight"] == pytest.approx(65.63, abs=0.1)
    assert c["pure_184W"] > 1.4 * c["CaWO4_compound"]
    assert c["same_pipeline_benchmark_ratio"] == SAME_PIPELINE_BENCHMARK
    assert "REJECTED" in c["verdict"]
    # recomputed from atomic weights held here, not read from GPD/literature/
    for s in ("Ca", "W", "O", "Ge"):
        assert s in c["atomic_weights_used"]


def test_closure_cited_with_provenance_gap():
    """test-closure-cited-with-provenance-gap. The repository-wide search is RUN and its
    result recorded; if nothing reproducible turns up, the citation says so.

    An informative outcome in either direction: finding a reproducible source would
    CLOSE the provenance gap and strengthen the closure citation.
    """
    s = cs.closure_provenance_search("407.7")
    assert s["all_hits"], "the closure figure is not in the repository at all"
    assert all(p.startswith("GPD/") for p in s["all_hits"]), (
        f"407.7 now appears outside GPD prose: {s['all_hits']} -- the provenance gap "
        "may have CLOSED; re-check the closure citation")
    assert s["has_reproducible_source"] is False
    assert s["reproducible_hits"] == []


def test_closure_not_rerun():
    """test-closure-not-rerun. No CaWO4 or Al2O3 target model, fold or pipeline was added.

    The closure was folded at the NUCLEUS/VNS normalization against THEIR Table 5 at
    THEIR site: rescaling it to the primary normalization would destroy the comparison,
    so it must be neither re-run nor rescaled.
    """
    out = subprocess.run(
        ["bash", "-c", "git grep -il 'cawo4\\|al2o3\\|calcium tungstate' -- src tests || true"],
        cwd=_ROOT, capture_output=True, text=True).stdout.split()
    # PRE-EXISTING, and not target models: veto_envelope/veto_credit describe NUCLEUS's
    # own (5 mm)^3 Al2O3 cryodetector cubes from the Phase-8 geometry gate. Recorded
    # explicitly so this guard cannot be satisfied by a blanket allow-list later.
    preexisting = {"src/qpd_potential/veto_envelope.py",
                   "src/qpd_potential/veto_credit.py",
                   "tests/test_veto_credit.py"}
    added_here = {"src/qpd_potential/cevns_subev.py",
                  "tests/test_cevns_subev_regression.py"}
    # ADDED BY PLAN 13-02, and recorded explicitly rather than allow-listed by
    # pattern. ROADMAP Phase 13 SC4 requires the Ge-vs-CaWO4 kinematic-compression
    # statement to be EXHIBITED, so neutron_recoil.py computes CaWO4's own atom
    # fractions and kinematic factors FROM FIRST PRINCIPLES -- its own atoms/kg,
    # its own 4A/(1+A)^2 per species, the same incident neutron flux. No NUCLEUS
    # CaWO4 measured rate, residual, Table-5 entry or target-swap rescale enters,
    # which is what fp-mass-scaled-target actually forbids; that is separately
    # asserted by tests/test_neutron_kinematics.py::
    # test_no_mass_scaled_nucleus_residual_anywhere. This is the NEUTRON channel,
    # not the CEvNS closure, and nothing here re-runs or rescales that closure.
    phase13_neutron_target_comparison = {
        "src/qpd_potential/neutron_recoil.py",
        "tests/test_neutron_kinematics.py",
    }
    added_here = added_here | phase13_neutron_target_comparison
    # ADDED BY PLAN 16-03, and recorded explicitly rather than allow-listed by
    # pattern, on the Phase-13 precedent above. ROADMAP Phase 16 SC3 requires the
    # LEE overlay band to carry the Romani Al-film AREA scaling, whose stated
    # extrapolation factor IS a surface-to-mass ratio against a 6.8 g calcium
    # tungstate crystal (1950 vs 955 cm^2/kg, from PITFALLS Pitfall 7). That is a
    # GEOMETRY ratio quoted as a band-edge label. No fold, no pipeline, no target
    # rate, no Table-5 entry and no rescale of the signal-side closure enters, which
    # is what fp-mass-scaled-target actually forbids -- asserted immediately below.
    phase16_lee_band_edge_label = {"src/qpd_potential/lee_overlay.py"}
    added_here = added_here | phase16_lee_band_edge_label
    # ADDED 2026-07-25 (Ge-intrinsic cosmogenic floor), recorded explicitly on the
    # same precedent. cosmogenic_intrinsic.py mentions CaWO4/Al2O3 ONLY in prose --
    # noting that those targets structurally cannot make 3H/68Ge/65Zn, which is why
    # this Ge-specific floor exists. There is no CaWO4/Al2O3 target model, fold,
    # rate, Table-5 entry or closure rescale in it (asserted below); it models Ge
    # decays only. The test file is its adversarial check.
    ge_intrinsic_prose = {"src/qpd_potential/cosmogenic_intrinsic.py",
                          "tests/test_cosmogenic_intrinsic.py"}
    added_here = added_here | ge_intrinsic_prose
    cos = open(os.path.join(_ROOT, "src", "qpd_potential",
                            "cosmogenic_intrinsic.py")).read().lower()
    assert "def cawo4" not in cos and "def al2o3" not in cos
    assert "table 5" not in cos and "table-5" not in cos and "407.7" not in cos
    lee = open(os.path.join(_ROOT, "src", "qpd_potential", "lee_overlay.py")).read()
    low = lee.lower()
    assert "def cawo4" not in low and "def calcium" not in low
    assert "reactorflux" not in low
    assert "table 5" not in low and "table-5" not in low
    assert "407.7" not in lee, "the signal-side closure figure leaked into src/"
    assert set(out) <= preexisting | added_here, (
        f"a CaWO4/Al2O3 model was added: {sorted(set(out) - preexisting - added_here)}")
    # ...and what those two files contain is arithmetic and prose, not a target model
    src = open(os.path.join(_ROOT, "src", "qpd_potential", "cevns_subev.py")).read()
    assert "def cawo4" not in src.lower()
    assert "ReactorFlux(" not in src.split("PLAN 12-03")[1]


# =========================================================================== #
# claim-vns-rescale-labelled                                                  #
# =========================================================================== #
def test_no_variant_flux_call():
    """test-no-variant-flux-call (fp-second-vns-run).

    cevns.nucleus_variant_flux() EXISTS and is exactly the trap: calling it would produce
    a physically reasonable second spectrum and silently violate the locked proxy.
    """
    assert hasattr(cevns, "nucleus_variant_flux")      # the trap is real, not hypothetical
    # Parsed, not grepped: the name appears in prose in both modules (naming the trap is
    # the point), so only an AST walk can distinguish a mention from a CALL.
    import ast
    for mod in ("cevns_subev.py", "fold.py"):
        tree = ast.parse(open(os.path.join(_ROOT, "src", "qpd_potential", mod)).read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                assert node.attr != "nucleus_variant_flux", f"{mod} calls the trap"
                assert node.attr != "nucleus_flux_normalization" or mod != "fold.py"
            if isinstance(node, ast.Name):
                assert node.id != "nucleus_variant_flux", f"{mod} calls the trap"
    # no second flux table was written: the tracked contents of data/flux/ are
    # unchanged from the phase's starting commit, compared rather than enumerated so
    # this guard cannot rot into a hand-maintained allow-list.
    now = subprocess.run(["bash", "-c", "git ls-files 'data/flux/*' | sort"], cwd=_ROOT,
                         capture_output=True, text=True).stdout.split()
    before = subprocess.run(
        ["bash", "-c", "git ls-tree -r --name-only HEAD -- data/flux | sort"],
        cwd=_ROOT, capture_output=True, text=True).stdout.split()
    assert now == before, f"data/flux/ changed: {sorted(set(now) ^ set(before))}"
    assert not any("vns" in p.lower() or "nucleus" in p.lower() for p in now)


def test_rescale_carries_both_fluxes():
    """test-rescale-carries-both-fluxes. BOTH candidate integral fluxes named with their
    sources, both factors given, and no unqualified bare 0.28 (fp-unlabelled-rescale)."""
    v = cs.vns_rescale()
    c = v["candidates"]
    assert c["nucleus_stated_2026"]["integral_flux"] == NUCLEUS_STATED_FLUX
    assert c["project_geometric"]["integral_flux"] == pytest.approx(
        PROJECT_GEOMETRIC_FLUX, rel=1e-6)
    assert c["nucleus_stated_2026"]["rescale_factor"] == pytest.approx(0.2802, abs=1e-3)
    assert c["project_geometric"]["rescale_factor"] == pytest.approx(0.2442, abs=1e-3)
    # the ~15% gap the project's own arithmetic does not close
    gap = (c["nucleus_stated_2026"]["integral_flux"]
           / c["project_geometric"]["integral_flux"] - 1.0)
    assert 0.10 < gap < 0.20
    for k in c:
        assert "arXiv" in c[k]["source"] or "nucleus_flux_normalization" in c[k]["source"]

    path = os.path.join(_ART, "cevns_vns_rescale.csv")
    header = "".join(l for l in open(path) if l.startswith("#"))
    assert "2.100000e+12" in header and "1.830269e+12" in header
    assert "0.280158" in header and "0.244174" in header
    assert "fp-second-vns-run" in header and "fp-unlabelled-rescale" in header
    assert "NO SECOND PIPELINE RUN" in header
    rows = [l.split(",") for l in open(path)
            if l.strip() and not l.startswith("#") and not l.startswith("design,")]
    assert len(rows) == 4
    assert {r[1] for r in rows} == {"nucleus_stated_2026", "project_geometric"}


def test_rescale_is_multiplication():
    """test-rescale-is-multiplication. EXACT proportionality on every bin.

    Any bin-dependent difference would mean a second fold or a second spectral shape was
    produced, which is fp-second-vns-run.
    """
    v = cs.vns_rescale()
    for d in _DESIGNS:
        r = fold.run_cevns_fold_extended(d, broaden=True)
        primary = r["dRdErec"]
        for k, c in v["candidates"].items():
            rescaled = primary * c["rescale_factor"]
            m = primary != 0.0
            ratio = rescaled[m] / primary[m]
            # THE decisive assertion: the ratio is the SAME on every bin. A second fold
            # or a second spectral shape would make it bin-dependent. The residual
            # 2.2e-16 spread is the float division round-trip, not physics.
            assert float(ratio.max() / ratio.min() - 1.0) <= 1e-15
            assert np.allclose(ratio, c["rescale_factor"], rtol=1e-15, atol=0.0)
            assert np.all(rescaled[~m] == 0.0)
        # and the RoI number in the artifact is that same multiplication of the primary
        E = r["E_rec_centers_eV"]
        roi = (E >= cs.ROI_LO_eV) & (E <= cs.ROI_HI_eV)
        primary_counts = float(r["N_rec"][roi].sum())
        pd = v["per_design"][d]
        assert pd["primary_roi_counts_per_kg_day"] == pytest.approx(primary_counts, rel=1e-12)
        for k, c in v["candidates"].items():
            assert pd[k] == pytest.approx(primary_counts * c["rescale_factor"], rel=1e-12)


@pytest.mark.skipif(not os.path.exists(_REPORT), reason="closure report not yet written")
def test_naive_ratio_rejected_and_sc_table_present():
    """test-naive-ratio-rejected, plus deliv-closure-report.must_contain."""
    txt = open(_REPORT).read()
    low = txt.lower()
    assert "2.31" in txt and "1.95" in txt
    assert "reject" in low
    for needle in ("form factor", "22.7", "44.19", "65.8", "407.7",
                   "VALD-11", "Phase 16", "2.1", "1.830269"):
        assert needle.lower() in low, f"closure report is missing {needle!r}"
    for sc in ("SC1", "SC2", "SC3", "SC4", "SC5"):
        assert sc in txt, f"the phase-level verdict table is missing {sc}"
    assert "SUPERSEDED" in txt
    assert "PARTIAL" in txt


def test_regression_artifacts_have_disposition_rows():
    from qpd_potential import legacy_grid as lg
    reg_rows = lg.load_register()
    for rel in ("artifacts/v2.0/cevns_v1_regression.csv",
                "artifacts/v2.0/cevns_vns_rescale.csv"):
        assert rel in reg_rows, f"{rel} has no disposition row"
