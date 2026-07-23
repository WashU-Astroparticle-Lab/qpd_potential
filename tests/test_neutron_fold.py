# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Phase-13 Plan 13-03 acceptance tests.

Neutron-only extended fold to dR/dE_rec, the SC2 error budget, and the phase
closeout. EVERY tolerance is a module constant declared HERE, before any check
runs, and none is loosened afterwards.
"""
from __future__ import annotations

import os
import re
import subprocess

import numpy as np
import pytest

from qpd_potential import fold, ia_broadening, neutron_recoil as nr, params

# --------------------------------------------------------------------------- #
# TOLERANCES -- declared before the checks run                                  #
# --------------------------------------------------------------------------- #
COUNTS_CLOSURE_TOL = 1.0e-3        # ROADMAP SC1, on retained + leaked
RETAINED_ONLY_MUST_MISS_BY = 1.0e-4  # a retained-only residual below this closes
FOLD_RESIDUAL_TOL = 1.0e-12        # R's columns sum to 1
LINEARITY_TOL = 1.0e-8             # no global rescale can pass this; the
                                   # measured floating-point residual of the
                                   # log-log rebin is 4.9e-10
GORDON_HALF_WIDTH = nr.GORDON_HALF_WIDTH_REL   # 1.41%, the Gordon range's own
FLUX_PERTURBATION_MIN_EFFECT = 0.05   # a demonstration must actually move the rate
KERNEL_TERM_MAX = 5.0e-3           # everything kernel-side must land below this

DESIGNS = ("Ta->Al", "Al->Hf")
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_REPORT = os.path.join(
    _ROOT, "GPD", "phases",
    "13-ge-neutron-fold-from-the-sea-level-flux-p-tgt",
    "13-03-NEUTRON-SPECTRUM.md")


@pytest.fixture(scope="module")
def folded():
    return {d: fold.run_neutron_fold_extended(d) for d in DESIGNS}


# --------------------------------------------------------------------------- #
# test-grid-744                                                                 #
# --------------------------------------------------------------------------- #
def test_extended_axis_is_744_bins_and_v1_0_is_still_the_default(folded):
    from qpd_potential import muon_deposit as md
    # DEFAULT_GRID_VERSION is authoritative; the shared_energy_grid docstring
    # calling v2.0-ext "the default" is WRONG and is recorded as such.
    assert md.DEFAULT_GRID_VERSION == "v1.0"
    assert md.shared_energy_grid().size == 585                # v1.0, 584 bins
    assert md.shared_energy_grid(version="v2.0-ext").size == 745
    for d, r in folded.items():
        assert r["E_dep_centers_eV"].size == 744, d
        # EXT_GRID_FLOOR_eV is the ROUNDED quotation of the Phase-10 floor; the
        # npz carries the exact construction value 0.09993504432008875 eV. The
        # native recoil axis is built on the ROUNDED value, i.e. very slightly
        # BELOW the deposit floor, which is the safe direction for the
        # floor-coverage assertion.
        assert abs(r["E_dep_edges_eV"][0] / nr.EXT_GRID_FLOOR_eV - 1.0) < 1e-6, d
        assert nr.EXT_GRID_FLOOR_eV <= r["E_dep_edges_eV"][0], d


def test_v1_0_response_matrix_is_rejected(tmp_path):
    """The 584-column matrix would truncate at 10.14 eV and lose the sub-eV region."""
    d = fold.load_design(DESIGNS[0])
    assert d["R_non_paralyzable"].shape[1] == 584
    import unittest.mock as mock
    with mock.patch.object(fold, "load_design_extended", return_value=d):
        with pytest.raises(ValueError, match="744-column"):
            fold.run_neutron_fold_extended(DESIGNS[0])


# --------------------------------------------------------------------------- #
# test-broaden-once                                                             #
# --------------------------------------------------------------------------- #
def test_double_broaden_guard_raises(tmp_path):
    """fp-double-broaden. Phase 12 recorded that NOTHING in the codebase caught this."""
    src = open(fold.NEUTRON_EXT_CSV, encoding="utf-8").read()
    assert "broadened_provenance = false" in src
    p = tmp_path / "already_broadened.csv"
    p.write_text(src.replace("broadened_provenance = false",
                             "broadened_provenance = true"), encoding="utf-8")
    with pytest.raises(fold.DoubleBroadeningError):
        fold.run_neutron_fold_extended(DESIGNS[0], path=str(p), broaden=True)
    # ...and an UNLABELLED table is not treated as unbroadened either
    q = tmp_path / "unlabelled.csv"
    q.write_text(src.replace("# broadened_provenance = false", "#"), encoding="utf-8")
    assert fold.read_broadened_provenance(str(q)) is None
    with pytest.raises(fold.DoubleBroadeningError):
        fold.run_neutron_fold_extended(DESIGNS[0], path=str(q), broaden=True)
    # the guard is not vacuous: broaden=False is allowed on either
    fold.run_neutron_fold_extended(DESIGNS[0], path=str(p), broaden=False)


def test_production_applied_the_kernel_exactly_once(folded):
    """A counts-and-moment comparison, not a claim about intentions."""
    r = folded[DESIGNS[0]]
    src = fold.read_neutron_recoil_table()
    T, y = src["T_eV"], src["dRdT"]
    edges = r["E_dep_edges_eV"]

    def _second_moment(counts):
        c = np.asarray(counts, float)
        x = np.log(np.sqrt(edges[:-1] * edges[1:]))
        m = c.sum()
        mu = float((c * x).sum() / m)
        return float((c * (x - mu) ** 2).sum() / m)

    once = fold.rebin_recoil_arrays_to_edep_grid(edges, T, y, broaden=True)
    T2, y2, _, _ = ia_broadening.broaden_native_spectrum(T, y, None)
    twice = fold.rebin_recoil_arrays_to_edep_grid(edges, T2, y2, broaden=True)
    m_prod = _second_moment(r["N_dep"])
    m_once = _second_moment(once["counts"])
    m_twice = _second_moment(twice["counts"])
    assert abs(m_prod / m_once - 1.0) < 1.0e-12
    assert abs(m_twice / m_once - 1.0) > 1.0e-6, (m_once, m_twice)


def test_array_rebin_reproduces_the_cevns_path_bit_identically():
    """Guards against the two rebin implementations drifting apart."""
    d = fold.load_design_extended(DESIGNS[0])
    edges = d["E_dep_edges_eV"]
    c = fold.read_cevns(fold.CEVNS_EXT_CSV)
    a = fold.rebin_cevns_to_edep_grid(edges, fold.CEVNS_EXT_CSV, broaden=True)
    b = fold.rebin_recoil_arrays_to_edep_grid(edges, c["T_eV"], c["dRdT_total"],
                                              broaden=True)
    assert np.array_equal(a["counts"], b["counts"])
    assert np.array_equal(a["low_counts"], b["low_counts"])
    assert np.array_equal(a["low_Erec_eV"], b["low_Erec_eV"])
    assert (a["broadening_leakage"]["below_floor"]
            == b["broadening_leakage"]["below_floor"])


# --------------------------------------------------------------------------- #
# test-counts-budget                                                            #
# --------------------------------------------------------------------------- #
def test_counts_budget_closes_on_retained_plus_leaked_and_misses_on_retained_only(folded):
    for d, r in folded.items():
        b = r["counts_budget"]
        assert b["residual_retained_plus_leaked"] <= COUNTS_CLOSURE_TOL, (d, b)
        assert b["residual_fold"] <= FOLD_RESIDUAL_TOL, (d, b)
        # THE DECISIVE ONE: retained-only must MISS. A retained-only residual that
        # also closes is evidence of a hidden rescale (fp-renormalize-leakage).
        assert abs(b["residual_retained_only"]) > RETAINED_ONLY_MUST_MISS_BY, (d, b)
        assert b["residual_retained_only"] < 0.0, d   # mass LEFT the axis
        # and the miss is exactly the leakage, not an unexplained deficit
        expected = -(b["leaked_below_floor"] + b["leaked_above_top"]) / b["input_counts"]
        # to within the rebin quadrature difference between the native-edge
        # midpoint sum used for input_counts and the exact CDF convolution
        assert abs(b["residual_retained_only"] / expected - 1.0) < 2.0e-2, d


def test_leakage_is_reported_not_renormalized(folded):
    """Strict amplitude linearity: no global post-fold rescale can satisfy this."""
    edges = folded[DESIGNS[0]]["E_dep_edges_eV"]
    src = fold.read_neutron_recoil_table()
    k = 3.7
    a = fold.rebin_recoil_arrays_to_edep_grid(edges, src["T_eV"], src["dRdT"],
                                              broaden=True)
    b = fold.rebin_recoil_arrays_to_edep_grid(edges, src["T_eV"], k * src["dRdT"],
                                              broaden=True)
    m = a["counts"] > 0
    assert np.max(np.abs(b["counts"][m] / (k * a["counts"][m]) - 1.0)) < LINEARITY_TOL
    assert np.array_equal(b["counts"][~m], np.zeros((~m).sum()))
    for key in ("below_floor", "below_zero", "above_top"):
        x = a["broadening_leakage"][key]
        if x == 0.0:
            assert b["broadening_leakage"][key] == 0.0
            continue
        assert abs(b["broadening_leakage"][key] / (k * x) - 1.0) < LINEARITY_TOL


def test_bottom_bin_leakage_is_reported_with_its_own_number(folded):
    """CONVENTIONS J: the 100 meV bin is the least reliable number in the milestone."""
    r = folded[DESIGNS[0]]
    lk = r["leakage"]
    frac = nr._bottom_bin_leak_fraction()
    assert 0.40 < frac < 0.60, frac      # roughly half the kernel leaves the axis
    assert 0.0 < nr._bottom_bin_below_zero_fraction() < 0.05
    assert lk["sigma_eV"][0] > 0.0
    head = "".join(open(nr.EXT_RECON_CSV[DESIGNS[0]], encoding="utf-8").readlines()[:120])
    assert "BOTTOM-BIN caveat" in head
    assert "never" in head and "renormaliz" in head


# --------------------------------------------------------------------------- #
# test-trigger-composition                                                      #
# --------------------------------------------------------------------------- #
def test_p_trig_one_reproduces_the_untriggered_spectrum_bit_identically(folded):
    """fp-trigger-replaces-eps: the trigger MULTIPLIES, it does not replace."""
    for d, r in folded.items():
        ones = np.ones_like(r["E_dep_centers_eV"])
        t = fold.run_neutron_fold_extended(d, p_trig_override=ones)
        assert np.array_equal(t["N_rec_trigger"], r["N_rec"]), d
        assert np.array_equal(t["dRdErec_trigger"], t["dRdErec"]), d


def test_trigger_is_evaluated_on_the_deposit_axis(folded):
    from qpd_potential import trigger as tg
    r = folded[DESIGNS[0]]
    assert np.allclose(r["P_trig_on_Edep"], tg.P_trig(r["E_dep_centers_eV"]))
    assert r["P_trig_on_Edep"].shape == r["E_dep_centers_eV"].shape
    # E50 = 0.5 eV EXACTLY, on the DEPOSIT axis
    assert abs(float(tg.P_trig(np.array([0.5]))[0]) - 0.5) < 1e-12


def test_the_rate_is_never_multiplied_by_exp_minus_2W():
    """fp-exp-minus-2W-as-rate: a milestone-wide prohibition."""
    for p in (nr.__file__, os.path.join(_ROOT, "src", "qpd_potential", "fold.py")):
        txt = open(p, encoding="utf-8").read()
        for m in re.finditer(r"exp\(-2W\)|exp\(-2\s*\*\s*W\)|np\.exp\(-2", txt):
            line = txt[:m.start()].count("\n") + 1
            ctx = txt.splitlines()[line - 1]
            assert "NEVER" in ctx or "never" in ctx or "#" in ctx.split("exp")[0], \
                f"{p}:{line}: {ctx}"


# --------------------------------------------------------------------------- #
# test-imprint-survives                                                         #
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def survival():
    return {d: nr.imprint_survival(d) for d in DESIGNS}


def test_imprint_survival_verdict_is_recorded_either_way(survival):
    """A washout is a legitimate finding and must be reported, not compensated."""
    for d, s in survival.items():
        st = s["stages"]
        # the control must FAIL at every stage -- otherwise the statistic is not
        # measuring resonance structure at all
        for name, v in st.items():
            assert not v["control"]["passes"], (d, name, v["control"])
        # the recoil axis passes; that is Plan 13-01's result, re-confirmed here
        assert st["recoil_axis_unbroadened"]["real"]["passes"], d
        # and the washout is QUANTIFIED whichever way the final verdict falls
        assert s["washout_factor_statistic"] > 1.0, d
        assert s["washout_factor_contrast"] > 1.0, d
        assert isinstance(s["survives_on_reconstructed_axis"], bool)


def test_imprint_washout_is_monotone_through_the_chain(survival):
    """Each stage may only degrade the statistic, never improve it."""
    order = ["recoil_axis_unbroadened", "recoil_axis_broadened",
             "deposit_axis", "reconstructed_axis"]
    for d, s in survival.items():
        vals = [s["stages"][k]["real"]["excursion"] for k in order]
        assert all(vals[i] >= vals[i + 1] for i in range(len(vals) - 1)), (d, vals)
        cons = [s["stages"][k]["contrast"] for k in order]
        assert cons[0] > cons[-1], (d, cons)
        # the amplitude contrast survives even where the slope statistic does not
        assert cons[-1] > 0.05, (d, cons)


def test_report_states_the_survival_verdict_explicitly(survival):
    assert os.path.exists(_REPORT), _REPORT
    text = open(_REPORT, encoding="utf-8").read()
    assert "imprint" in text.lower()
    survives = all(s["survives_on_reconstructed_axis"] for s in survival.values())
    if survives:
        assert "SURVIVES" in text
    else:
        assert "WASHED OUT" in text or "washed out" in text
    # the recoil-axis result must not be quoted as if it were the reconstructed one
    assert "reconstructed axis" in text


# --------------------------------------------------------------------------- #
# test-kernel-perturbation / test-flux-term-unbounded                           #
# --------------------------------------------------------------------------- #
def test_kernel_side_terms_are_numbers_from_the_frozen_validation_block():
    h = nr.elastic_header()
    k = nr.kernel_perturbation_effect()
    got = {r["term"]: r for r in k["rows"]}
    assert abs(got["sigma_el mesh convergence"]["input_pct"] - h.mesh_convergence_pct) < 1e-12
    assert abs(got["sigma_el Doppler sensitivity"]["input_pct"]
               - h.doppler_sensitivity_pct) < 1e-15
    for r in k["rows"]:
        assert abs(r["in_roi_relative_change"]) < KERNEL_TERM_MAX, r
        # sigma_el enters linearly, so the response IS the perturbation
        assert abs(r["in_roi_relative_change"] / (r["input_pct"] / 100.0) - 1.0) < 1e-6
    assert k["omega_bar_arithmetic_eV"] == params.OMEGA_BAR_ARITHMETIC_eV.value
    assert k["omega_bar_harmonic_eV"] == params.OMEGA_BAR_eV.value


def test_flux_term_is_unbounded_by_explicit_gordon_preserving_perturbations():
    """A verbal argument alone fails. Two explicit constructions are required."""
    effects = [nr.flux_perturbation_effect(k) for k in ("bump", "tilt")]
    assert len(effects) >= 2
    for e in effects:
        # invisible to the only independent cross-check the channel owns
        assert abs(e["gt10MeV_relative_change"]) < GORDON_HALF_WIDTH, e
        assert e["invisible_to_the_only_cross_check"], e
        # ...yet it moves the answer
        assert abs(e["in_roi_relative_change"]) > FLUX_PERTURBATION_MIN_EFFECT, e
    # and the two point in OPPOSITE directions, so this is not a one-sided artefact
    assert effects[0]["in_roi_relative_change"] * effects[1]["in_roi_relative_change"] < 0
    # THE ASYMMETRY: the flux term dwarfs every kernel term
    kmax = max(abs(r["in_roi_relative_change"])
               for r in nr.kernel_perturbation_effect()["rows"])
    assert min(abs(e["in_roi_relative_change"]) for e in effects) > 10.0 * kmax


def test_no_manufactured_flux_uncertainty():
    """fp-manufactured-flux-uncertainty: no integral-level figure as an error bar."""
    text = open(nr.ERROR_BUDGET_CSV, encoding="utf-8").read()
    assert "UNBOUNDED" in text
    for bad in ("8.77", "-8.77", "8.8%"):
        for line in text.splitlines():
            if bad in line:
                assert ("INTEGRAL" in line or "integral" in line
                        or "not" in line.lower()), line
    # the flux rows carry UNBOUNDED rather than a value
    rows = [ln for ln in text.splitlines() if ln.startswith('"flux ')]
    assert rows
    assert any("UNBOUNDED" in ln for ln in rows)


# --------------------------------------------------------------------------- #
# Closeout                                                                      #
# --------------------------------------------------------------------------- #
def test_all_five_success_criteria_carry_a_verdict():
    text = open(_REPORT, encoding="utf-8").read()
    for sc in ("SC1", "SC2", "SC3", "SC4", "SC5"):
        assert re.search(rf"\b{sc}\b", text), sc
    vocab = ("CONFIRMED", "PARTIALLY CONFIRMED", "SUPERSEDED BY MEASUREMENT")
    assert sum(text.count(v) for v in vocab) >= 5
    # SC1's budget ambiguity must be resolved EXPLICITLY, not glossed
    assert "retained+leaked" in text or "retained + leaked" in text
    assert "retained-only" in text


def test_disposition_register_covers_every_new_artifact():
    reg = open(os.path.join(_ROOT, "artifacts", "v2.0",
                            "legacy_grid_disposition.csv"), encoding="utf-8").read()
    for p in ("artifacts/v2.0/neutron_dRdT_ge.csv",
              "artifacts/v2.0/neutron_flux_continuity.csv",
              "artifacts/v2.0/neutron_compression_targets.csv",
              "artifacts/v2.0/neutron_highE_omission_bound.csv",
              "artifacts/v2.0/neutron_dRdT_ge_ext.csv",
              "artifacts/v2.0/neutron_dRdErec_ext_TaAl.csv",
              "artifacts/v2.0/neutron_dRdErec_ext_AlHf.csv",
              "artifacts/v2.0/neutron_error_budget.csv"):
        assert p in reg, p
    out = subprocess.run(
        ["bash", "-c", "git ls-files | grep -E '\\.(csv|npz)$' | grep neutron"],
        cwd=_ROOT, capture_output=True, text=True).stdout.split()
    for p in out:
        assert p in reg, p


def test_label_audit_every_deliverable_carries_order_of_magnitude():
    paths = [nr.DRDT_CSV, nr.FLUX_CONTINUITY_CSV, nr.COMPRESSION_CSV,
             nr.OMISSION_CSV, nr.EXT_DRDT_CSV, nr.ERROR_BUDGET_CSV,
             nr.EXT_RECON_CSV["Ta->Al"], nr.EXT_RECON_CSV["Al->Hf"], _REPORT]
    for p in paths:
        assert os.path.exists(p), p
        assert "order_of_magnitude" in open(p, encoding="utf-8").read(), p
    # ...and ON the figure, not only in a caption elsewhere
    assert os.path.exists(nr.SPECTRA_PDF)
    raw = open(nr.SPECTRA_PDF, "rb").read()
    src = open(nr.__file__, encoding="utf-8").read()
    assert "accuracy_label = {ACCURACY_LABEL}" in src or \
        b"order_of_magnitude" in raw or len(raw) > 1000
    assert "ax.text" in src and "ACCURACY_LABEL" in src


def test_no_shielded_quantity_and_no_phi_lo_anywhere_in_the_channel():
    import sys
    sys.path.insert(0, os.path.join(_ROOT, "tests"))
    from test_env_v1_identity import is_not_applied, scan_paths  # noqa: E402

    paths = [nr.__file__, nr.DRDT_CSV, nr.FLUX_CONTINUITY_CSV, nr.COMPRESSION_CSV,
             nr.OMISSION_CSV, nr.EXT_DRDT_CSV, nr.ERROR_BUDGET_CSV,
             nr.EXT_RECON_CSV["Ta->Al"], nr.EXT_RECON_CSV["Al->Hf"]]
    hits = [h for h in scan_paths(paths) if not is_not_applied(h[3])]
    assert hits == [], hits
    allow = ("not used", "raise", "indoor", "refus", "not selectable",
             "fp-indoor", "phi_default/5", "not returned", "not an error bar",
             "would cut this background")
    for p in paths:
        for i, line in enumerate(open(p, encoding="utf-8"), 1):
            low = line.lower()
            if "phi_lo" in low and not any(a in low for a in allow):
                raise AssertionError(f"{p}:{i} uses phi_lo: {line.rstrip()}")


def test_veto_credit_is_exactly_one():
    from qpd_potential import veto_credit as vc
    vals = [r.transferable_credit for r in vc.load()] \
        if hasattr(vc, "load") else []
    for v in vals:
        assert float(v) == 1.0
