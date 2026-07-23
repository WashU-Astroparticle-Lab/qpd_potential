# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Plan 14-01: the Ge (n,gamma) capture channel and the discrete-inelastic bound.

Every acceptance test of the plan contract has a test here.  ALL TOLERANCES ARE
DECLARED AS MODULE CONSTANTS BELOW, BEFORE ANY CHECK RUNS (the Phase-13 pattern),
so no tolerance can be chosen after seeing a number.
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from qpd_potential import capture_channel as cc
from qpd_potential import neutron_recoil as nr
from qpd_potential import params

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------- #
# TOLERANCES AND EXPECTATIONS -- declared BEFORE any check runs.               #
# The two anchor values are stated INDEPENDENTLY in GPD/ROADMAP.md Phase 14    #
# ("natural Ge sigma_th ~ 2.2 b, 73Ge ~ 15 b"); nothing here is fitted to them.#
# --------------------------------------------------------------------------- #
ROADMAP_SIGMA_TH_NATURAL_b = 2.2
ROADMAP_SIGMA_TH_73GE_b = 15.0
XS_ANCHOR_REL_TOL = 0.20              # ROADMAP-stated agreement window

BAND_SUM_REL_TOL = 5.0e-3             # bands must sum to the total
NODE_DOUBLING_REL_TOL = 5.0e-3        # quadrature convergence
WESTCOTT_MIN_RELATIVE_DIFFERENCE = 0.05   # the naive product must DIFFER
THERMAL_DOMINANCE_THRESHOLD = 0.60    # mirrors cc.THERMAL_DOMINANCE_THRESHOLD
MF3_RRR_PROBE_eV = (0.0253, 1.0, 100.0, 1000.0)
CASCADE_INVARIANCE_REL_TOL = 0.0      # EXACT: the bound must not move at all

ARTIFACTS = {
    "xs": os.path.join(_ROOT, "artifacts", "v2.0", "ge_capture_xs.csv"),
    "rates": os.path.join(_ROOT, "artifacts", "v2.0", "capture_rate_bands.csv"),
    "bounds": os.path.join(_ROOT, "artifacts", "v2.0", "capture_recoil_bounds.csv"),
}
REPORT = os.path.join(_ROOT, "GPD", "phases",
                      "14-ge-only-thermal-capture-channels-p-geonly",
                      "14-01-CAPTURE-BOUNDS.md")


def _text(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _rows(path):
    """(header, rows) from a '#'-headed CSV, parsed with the csv module.

    A naive ``split(',')`` breaks on the quoted basis/note fields, which contain
    commas -- and it breaks SILENTLY, reading the wrong column.
    """
    import csv
    import io
    body = "\n".join(ln for ln in _text(path).splitlines() if not ln.startswith("#"))
    r = list(csv.reader(io.StringIO(body)))
    return r[0], [x for x in r[1:] if x]


# --------------------------------------------------------------------------- #
# claim-xs-frozen                                                              #
# --------------------------------------------------------------------------- #
def test_xs_anchor():
    """test-xs-anchor. Natural sigma_th and the 73Ge value reproduce the
    ROADMAP's independently stated ~2.2 b / ~15 b with nothing fitted, and the
    73Ge share of the natural thermal capture is reported against its 7.75%
    abundance share."""
    ts = cc.thermal_capture_summary()
    nat = ts["natural_sigma_b"]
    assert abs(nat - ROADMAP_SIGMA_TH_NATURAL_b) / ROADMAP_SIGMA_TH_NATURAL_b \
        < XS_ANCHOR_REL_TOL, f"natural sigma_th = {nat} b"
    s73 = ts["per_isotope"][73]["sigma_b"]
    assert abs(s73 - ROADMAP_SIGMA_TH_73GE_b) / ROADMAP_SIGMA_TH_73GE_b \
        < XS_ANCHOR_REL_TOL, f"73Ge sigma_th = {s73} b"

    # The disproportion is the point: 7.75% of the atoms, ~half the capture.
    share = ts["per_isotope"][73]["share_of_natural"]
    ab = ts["per_isotope"][73]["abundance"]
    assert ab == pytest.approx(0.0775)
    assert share > 5.0 * ab, (
        f"73Ge carries {share:.4f} of natural thermal capture from {ab} of the atoms")
    # and it is REPORTED, not merely computed
    assert f"{share*100:.2f}%" in _text(ARTIFACTS["xs"])


def test_mf3_mt102_is_zero_in_the_rrr():
    """test-mf3-zero-recorded. The trap is ASSERTED, not described: MF=3 MT=102
    read straight out of the raw ENDF file evaluates to EXACTLY 0.0 through the
    resolved-resonance region, for every isotope. The fold's source is the ACE
    set, and the artifact header states the trap in words."""
    for iso in params.GE_ISOTOPES:
        v = cc.mf3_mt102_probe_b(iso.A, MF3_RRR_PROBE_eV)
        assert np.array_equal(v, np.zeros_like(v)), (
            f"MF=3 MT=102 for Ge-{iso.A} is no longer identically zero in the RRR: {v}. "
            "If the frozen file changed, the trap statement must be re-measured.")

    # ... while the OPERATIVE source is emphatically non-zero.
    assert cc.sigma_capture_b(70, cc.E_THERMAL_REF_eV) > 1.0
    assert cc.sigma_capture_natural_b(cc.E_THERMAL_REF_eV) > 1.0

    # The fold's source path is the ACE set, not the raw file.
    assert cc.ace_path(70).endswith(".800nc")
    assert "ace" in cc.ace_path(70)

    head = _text(ARTIFACTS["xs"])
    for phrase in ("MF=3 MT=102", "IDENTICALLY 0.0", "FILE 2",
                   "pre-reconstructed", "FORBIDDEN PROXY"):
        assert phrase.lower() in head.lower(), f"header does not state {phrase!r}"


def test_q_values_are_read_not_transcribed():
    """Q_cap must come from the file. Asserted by re-reading the QM field
    directly here and requiring the module's value to match it exactly."""
    import endf
    for iso in params.GE_ISOTOPES:
        m = endf.Material(cc.raw_endf_path(iso.A))
        assert cc.capture_Q_eV(iso.A) == float(m.section_data[3, 102]["QM"])
        assert cc.endf_MAT(iso.A) == int(m.MAT)


def test_egaf_disposition():
    """test-egaf-disposition. Either a frozen, integrity-checked line list with
    its retrieval command recorded, or a NAMED GAP. Silence fails; invention
    fails."""
    manifest = os.path.join(cc.EGAF_DIR, "MANIFEST.md")
    report = _text(REPORT)
    if cc.egaf_available():
        assert os.path.isfile(manifest), "frozen EGAF files but no MANIFEST"
        man = _text(manifest)
        assert "sha256" in man.lower() and "curl" in man.lower()
        for A, fn in cc.EGAF_FILE.items():
            p = os.path.join(cc.EGAF_DIR, fn)
            assert cc.sha256_of(p) in man, f"{fn} SHA-256 not recorded in the manifest"
        # Acquisition is not the same as sharpening: the completeness deficit
        # must be reported, not glossed.
        assert "completeness" in report.lower()
    else:
        assert "NAMED GAP" in report, "no EGAF artifact and no named gap written"


@pytest.mark.skipif(not cc.egaf_available(), reason="EGAF not frozen locally")
def test_egaf_uses_only_the_evaluated_dataset():
    """Each .ens file carries three datasets with separate normalisations.
    Summing all three inflates the per-capture intensity ~3x. Only {~EGAF} is
    used, and the completeness check is what makes that visible."""
    for A in (70, 72, 73, 74):
        d = cc.egaf_cascade_completeness(A)
        assert d["dataset_used"] == "{~EGAF}"
        assert d["nr_norm"] is not None and d["sigma0_b"] is not None
        assert 0.0 < d["completeness"] < 1.0, (
            f"Ge-{A} EGAF completeness {d['completeness']} outside (0,1); a value "
            "above 1 means more energy is emitted than the capture Q-value")
        # The bracket must actually be a bracket, and tighter than the ceiling.
        assert d["mean_T_from_observed_eV"] < d["mean_T_upper_bracket_eV"]
        assert d["mean_T_upper_bracket_eV"] < d["T_max_single_gamma_eV"]


# --------------------------------------------------------------------------- #
# claim-capture-rate                                                           #
# --------------------------------------------------------------------------- #
def test_rate_fold_bands():
    """test-rate-fold-bands. Bands sum to the total, node doubling moves the
    total by less than the declared tolerance, and the 1 - 10.14 eV table gap is
    covered by DIRECT driver evaluation rather than by interpolating across
    either table's edge."""
    bd = cc.band_decomposed_rate(cc.sigma_capture_natural_b, per_decade=200)
    assert bd["band_sum_residual"] < BAND_SUM_REL_TOL

    bd2 = cc.band_decomposed_rate(cc.sigma_capture_natural_b, per_decade=400)
    delta = abs(bd2["total"]["rate_counts_kg_day"] - bd["total"]["rate_counts_kg_day"]) \
        / bd["total"]["rate_counts_kg_day"]
    assert delta < NODE_DOUBLING_REL_TOL, f"node doubling moved the total by {delta}"

    gap = cc.gap_coverage_report(per_decade=200)
    assert gap["n_nodes_in_gap"] > 0, "no quadrature node inside the table gap"
    assert gap["bit_identical"], (
        "the flux inside the 1 - 10.14 eV gap is NOT bit-identical to a direct "
        "PARMA driver call, so something interpolated a table across the gap")

    # Nothing derived is zero (ROADMAP SC4's never-zero rule).
    assert bd["total"]["rate_counts_kg_day"] > 0.0
    for b in bd["bands"].values():
        assert b["rate_counts_kg_day"] > 0.0


def test_flux_leg_is_outdoor_and_phi_lo_is_refused():
    """The indoor leg would cut this background fivefold. It must raise."""
    with pytest.raises(nr.FluxColumnError):
        nr.neutron_flux_cm2_s_MeV(np.array([1.0]), column="phi_lo")
    with pytest.raises(nr.FluxColumnError):
        nr.neutron_flux_cm2_s_MeV(np.array([1.0]), column="band_midpoint")
    # Line scan: every phi_lo occurrence in this plan's module must be a comment
    # or a prose/header string literal -- a definition or a refusal, never a use.
    src = _text(os.path.join(_ROOT, "src", "qpd_potential", "capture_channel.py"))
    for line in src.splitlines():
        if "phi_lo" in line:
            s = line.lstrip()
            assert s.startswith("#") or s.startswith('"') or s.startswith("'"), (
                f"phi_lo appears outside a comment or a string literal: {line!r}")


def test_westcott_not_identity():
    """test-westcott-not-identity. AGREEMENT IS THE FAILURE CONDITION. The naive
    Phi_th x sigma(0.0253 eV) product and the spectrally folded thermal band are
    the same integral evaluated two ways; agreement would indicate the fold
    collapsed to the product rather than that the physics is right."""
    wc = cc.westcott_comparison(per_decade=200)
    rel = abs(wc["ratio_naive_over_folded"] - 1.0)
    assert rel > WESTCOTT_MIN_RELATIVE_DIFFERENCE, (
        f"the folded thermal band and the naive product agree to {rel*100:.2f}%, "
        "which FAILS by design: it indicates the fold collapsed to the product.")

    # sqrt(pi)/2 must NOT have been substituted for the measured ratio.
    assert abs(wc["ratio_naive_over_folded"] - wc["westcott_sqrt_pi_over_2"]) > 0.05

    # The ratio and its sign must be REPORTED, not merely computed.
    txt = _text(ARTIFACTS["rates"])
    assert "NAIVE_PRODUCT_NOT_THE_ANSWER" in txt
    assert f"{wc['ratio_naive_over_folded']:.4f}" in txt


def test_thermal_dominance():
    """test-thermal-dominance. THE PLAN'S PRIMARY NON-IDENTITY DISCONFIRMING
    CHECK. The number is computed and a verdict is written either way; the
    threshold is declared above, before the number is seen."""
    v = cc.thermal_dominance_verdict(per_decade=200)
    assert cc.THERMAL_DOMINANCE_THRESHOLD == THERMAL_DOMINANCE_THRESHOLD
    f = v["thermal_fraction"]
    assert 0.0 < f < 1.0
    assert v["thermal_dominates"] == (f >= THERMAL_DOMINANCE_THRESHOLD)

    for path in (ARTIFACTS["rates"], REPORT):
        txt = _text(path)
        assert f"{f*100:.2f}%" in txt, f"the thermal fraction is not reported in {path}"
        assert v["verdict"] in txt, f"no verdict written in {path}"

    # The non-thermal remainder must be named, whichever way the verdict falls.
    assert f"{(1-f)*100:.2f}%" in _text(REPORT)


def test_doppler_sensitivity():
    """test-doppler-sensitivity. The Phase-9 mK caveat is ANSWERED WITH A NUMBER
    computed from the committed 0.1 K ACE set, not restated."""
    dop = cc.doppler_sensitivity(per_decade=200)
    assert cc.ace_temperature_key(70, cc.ACE_SUFFIX_293K) != \
        cc.ace_temperature_key(70, cc.ACE_SUFFIX_0P1K), \
        "the two ACE sets report the same temperature; the check would be vacuous"
    d = dop["epithermal_signed_relative_difference"]
    assert np.isfinite(d)
    # A signed number must appear in the artifact.
    assert f"{d*100:+.5f}%" in _text(ARTIFACTS["rates"])


def test_self_shielding_is_computed_not_assumed():
    """The thin-target formula is CHECKED from the same sigma the fold uses, and
    the resonance-peak value -- which is NOT << 1 -- is reported rather than
    replaced by the thermal one."""
    ss = cc.self_shielding_check(per_decade=200)
    assert ss["P_capture_2mm_at_2200ms"] < 0.05
    assert ss["P_capture_2mm_at_sigma_max"] > ss["P_capture_2mm_at_2200ms"]
    txt = _text(ARTIFACTS["rates"])
    assert f"{ss['P_capture_2mm_at_sigma_max']*100:.1f}%" in txt
    # the slab bound must be per band and must show the epithermal cost
    assert ss["slab_vs_thin_by_band"]["epithermal"]["ratio_att_over_thin"] < 1.0


def test_biffl_comparison_is_made_and_directional():
    """The adopted Phi_th is ABOVE Biffl's stated requirement, and the direction
    is stated rather than skipped."""
    b = cc.biffl_comparison()
    assert b["phi_th_adopted_cm2_s"] == cc.PHI_TH_PHASE9_cm2_s
    assert not b["meets_requirement"]
    assert b["ratio_adopted_over_requirement"] > 1.0
    assert "09-02-NEUTRON-DECLARATION" in b["phi_th_source"]
    assert "PHASE 9" in b["phi_th_source"].upper()
    for path in (ARTIFACTS["rates"], REPORT):
        assert f"{b['ratio_adopted_over_requirement']:.2f}" in _text(path)


# --------------------------------------------------------------------------- #
# claim-cascade-bound                                                          #
# --------------------------------------------------------------------------- #
def test_cascade_ceiling():
    """test-cascade-ceiling. Five ceilings from PARSED Q values, dimensionally
    consistent in eV, with the maximum isotope identified -- and it is checked
    against whether that isotope also dominates the rate."""
    c = cc.single_gamma_ceilings()
    assert set(c["per_isotope"]) == {70, 72, 73, 74, 76}
    for A, v in c["per_isotope"].items():
        # dimensional identity: [eV]^2 / [eV] = [eV]
        assert v["T_max_eV"] == pytest.approx(
            v["Q_cap_eV"] ** 2 / (2.0 * (A + 1) * params._U_MEV * 1e6), rel=1e-12)
        assert 100.0 < v["T_max_eV"] < 1000.0
        # the recoiling body is A+1, not A
        assert v["product"] == f"{A + 1}Ge"
    # the largest ceiling belongs to the largest Q
    amaxQ = max(c["per_isotope"], key=lambda a: c["per_isotope"][a]["Q_cap_eV"])
    assert c["max_isotope"] == amaxQ == 73

    # ... and 73Ge is also the isotope dominating the capture rate.
    per = cc.per_isotope_band_rates("capture", per_decade=200)
    dominant = max(per, key=lambda a: per[a]["total"]["rate_counts_kg_day"])
    assert dominant == 73

    # The ROADMAP's generic "473 eV at 8 MeV" is an illustration, not the Ge
    # answer, and the real maximum is HIGHER. Say so rather than reconcile.
    assert c["max_T_eV"] > 473.0


def test_bound_is_cascade_free():
    """test-bound-is-cascade-free. The reported in-RoI bound must be numerically
    INVARIANT under every cascade parameter varied. A bound that moves is not
    the rigorous bound."""
    base = cc.rigorous_in_roi_bound(per_decade=200)["bound_counts_kg_day"]
    variants = [
        dict(multiplicity=1), dict(multiplicity=3), dict(multiplicity=17),
        dict(partition_eV=[7.4159e6]),
        dict(partition_eV=[2.0e6, 3.0e6, 2.4159e6]),
        dict(partition_eV=[1.0e6] * 7 + [0.4159e6]),
        dict(angular_correlation="isotropic"),
        dict(angular_correlation="fully_aligned"),
        dict(multiplicity=5, partition_eV=[1.48318e6] * 5,
             angular_correlation="anti_aligned"),
    ]
    for kw in variants:
        got = cc.in_roi_bound_with_cascade_params(per_decade=200, **kw)
        assert got == base, f"the bound moved under {kw}: {got} != {base}"

    # It equals the total capture rate, and it is derived rather than integrated.
    total = cc.band_decomposed_rate(cc.sigma_capture_natural_b,
                                    per_decade=200)["total"]["rate_counts_kg_day"]
    assert base == total
    assert "exactly one recoiling nucleus" in \
        cc.rigorous_in_roi_bound(per_decade=200)["derivation"]


def test_multiplicity_statement():
    """test-multiplicity-statement. Sum(E^2) != (Sum E)^2 is shown WITH NUMBERS,
    the multiplicity-N mean is written as T_max/N with N SYMBOLIC, and the label
    column distinguishes RIGOROUS_BOUND from CONDITIONAL_ESTIMATE on every row."""
    d = cc.sum_of_squares_demo([2.0e6, 3.0e6, 2.4159e6])
    assert d["sum_of_squares"] != d["square_of_sum"]
    assert d["ratio_ss_over_sq"] < 1.0

    header, body = _rows(ARTIFACTS["bounds"])
    assert "evidence_class" in header
    ci, qi, vi, ei = (header.index(c) for c in
                      ("evidence_class", "quantity", "value", "expression"))
    assert body
    for row in body:
        assert row[ci] in ("RIGOROUS_BOUND", "CONDITIONAL_ESTIMATE"), row

    # N stays symbolic: no numeric value on the multiplicity-N mean row.
    nrow = [r for r in body if r[qi] == "multiplicity_N_mean"]
    assert len(nrow) == 1
    assert "N SYMBOLIC" in nrow[0][ei]
    assert nrow[0][vi] == "", "the multiplicity-N mean was assigned a value"
    assert nrow[0][ci] == "CONDITIONAL_ESTIMATE"


# --------------------------------------------------------------------------- #
# claim-inelastic-named                                                        #
# --------------------------------------------------------------------------- #
def test_inelastic_named():
    """test-inelastic-named. A natural inelastic rate exists, both ROADMAP-named
    levels appear, and the RECOIL-PLACEMENT statement is present. A bare rate
    with no placement statement fails."""
    bd = cc.band_decomposed_rate(cc.sigma_inelastic_natural_b, per_decade=200)
    assert bd["total"]["rate_counts_kg_day"] > 0.0

    place = cc.inelastic_placement()
    # the nuclear recoil lands FAR above the 100 eV RoI top
    assert place["nuclear_recoil_ceiling_at_mean_En_eV"] > 1.0e3 * place["roi_top_eV"]
    # while the gamma-emission recoil is a few eV
    g74 = place["named_levels"]["74Ge_596keV"]["gamma_recoil_eV"]
    g72 = place["named_levels"]["72Ge_834keV"]["gamma_recoil_eV"]
    assert 0.1 < g74 < 100.0 and 0.1 < g72 < 100.0

    for path in (ARTIFACTS["bounds"], REPORT):
        txt = _text(path)
        assert "596" in txt and "834" in txt, f"named levels missing from {path}"
        assert "ABOVE" in txt

    # the >20 MeV omission direction must be re-labelled for inelastic rather
    # than inheriting Phase 13's elastic margin
    top = cc.top_decade_fraction(cc.sigma_inelastic_natural_b, per_decade=200)
    if top > 0.10:
        assert "flatters_SB" in _text(ARTIFACTS["bounds"])


# --------------------------------------------------------------------------- #
# artifact hygiene                                                             #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("key", sorted(ARTIFACTS))
def test_accuracy_label_on_every_artifact(key):
    """fp-precision-inflation. Every artifact of this plan carries the label."""
    assert "order_of_magnitude" in _text(ARTIFACTS[key])
    header, body = _rows(ARTIFACTS[key])
    assert "accuracy_label" in header
    ai = header.index("accuracy_label")
    assert body
    for row in body:
        assert row[ai] == "order_of_magnitude", row


def test_report_exists_and_carries_the_verdicts():
    txt = _text(REPORT)
    for phrase in ("order_of_magnitude", "RIGOROUS", "CONDITIONAL",
                   "flatters_SB", "penalizes_SB", "Biffl", "MF=3 MT=102"):
        assert phrase in txt, f"{phrase!r} missing from the bounds report"
