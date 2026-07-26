# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Plan 14-02: the 71Ge electron-capture lines and the Phase-14 closeout.

ALL TOLERANCES ARE DECLARED AS MODULE CONSTANTS BELOW, BEFORE ANY CHECK RUNS.
The Phase-9 shielded-token machinery is IMPORTED from tests/test_env_v1_identity.py
rather than re-typed as a private list.
"""
import csv
import io
import os
import subprocess
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from qpd_potential import capture_channel as cc
from qpd_potential import legacy_grid as lg
from qpd_potential import params
from qpd_potential import trigger

from test_env_v1_identity import (SHIELDED_TOKENS, SHIELDED_TOKENS_EXTRA,
                                  is_not_applied)

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------- #
# TOLERANCES AND CONSTANTS -- declared BEFORE any check runs                    #
# --------------------------------------------------------------------------- #
HALF_LIFE_LIMIT_TOL = 1.0e-9        # A(t1/2) = 0.5 A_sat
TRIGGER_E50_TOL = 1.0e-12           # P(E50) = 1/2 exactly, whatever E50 is
COUNTS_CLOSURE_TOL = 1.0e-3         # retained+leaked residual
FOLD_RESIDUAL_TOL = 1.0e-12         # R's columns sum to 1
GA_EDGE_REL_TOL = 0.01              # line energy vs Ga binding energy
NU_RECOIL_MAX_BIN_FRACTION = 1.0    # the shift must be under one E_rec bin
EREC_BIN_WIDTH_FRACTION = 0.12202   # Phase-13 measured 12.202%/bin
SHARPNESS_RANGE = params.TRIGGER_SHARPNESS_RANGE   # [1, 12]
ROI = (cc.ROI_EREC_LO_eV, cc.ROI_EREC_HI_eV)
DESIGNS = ("Ta->Al", "Al->Hf")

ARTIFACTS = {
    "lines": os.path.join(_ROOT, "artifacts", "v2.0", "ge71_ec_lines.csv"),
    "erec_TaAl": os.path.join(_ROOT, "artifacts", "v2.0", "ge71_ec_dRdErec_TaAl.csv"),
    "erec_AlHf": os.path.join(_ROOT, "artifacts", "v2.0", "ge71_ec_dRdErec_AlHf.csv"),
}
FIGURE = os.path.join(_ROOT, "artifacts", "v2.0", "capture_channel_bounds.pdf")
PHASE_DIR = os.path.join(_ROOT, "GPD", "phases",
                         "14-ge-only-thermal-capture-channels-p-geonly")
REPORT = os.path.join(PHASE_DIR, "14-02-EC-AND-CLOSEOUT.md")
REPORT_01 = os.path.join(PHASE_DIR, "14-01-CAPTURE-BOUNDS.md")
MODULE = os.path.join(_ROOT, "src", "qpd_potential", "capture_channel.py")

SC_VERDICTS = ("CONFIRMED", "PARTIALLY CONFIRMED",
               "SUPERSEDED BY MEASUREMENT", "REFUTED")


def _text(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _rows(path):
    body = "\n".join(ln for ln in _text(path).splitlines() if not ln.startswith("#"))
    r = list(csv.reader(io.StringIO(body)))
    return r[0], [x for x in r[1:] if x]


# --------------------------------------------------------------------------- #
# claim-ec-inventory                                                           #
# --------------------------------------------------------------------------- #
def test_ec_energies():
    """test-ec-energies. The three line energies are recorded with the ROADMAP
    anchor as their source, and the physical identification -- an EC line energy
    IS the binding energy of the captured shell in the DAUGHTER -- is CHECKED
    against a separately retrieved Ga edge table rather than marked UNVERIFIED."""
    chk = cc.ge71_line_energy_check()
    shells = {r["shell"]: r for r in chk["rows"]}
    assert set(shells) == {"K", "L", "M"}
    assert shells["M"]["line_energy_eV_DEPOSITED"] == 158.7
    assert shells["M"]["line_energy_unc_eV"] == 1.4
    assert shells["L"]["line_energy_eV_DEPOSITED"] == 1298.5
    assert shells["K"]["line_energy_eV_DEPOSITED"] == 10368.3

    # allowed EC captures s-electrons: K(1s), L1(2s), M1(3s)
    assert cc.GE71_SHELL_IDENTIFICATION == {"K": "K", "L": "L1", "M": "M1"}
    for r in chk["rows"]:
        assert r["status"] == "CHECKED", f"{r['shell']} could not be checked"
        assert abs(r["relative_difference"]) < GA_EDGE_REL_TOL, r
    # the M line's stated +/-1.4 eV must actually cover the difference
    assert shells["M"]["within_stated_unc"] is True

    txt = _text(ARTIFACTS["lines"])
    assert "CHECKED" in txt and "Ga" in txt
    assert chk["sha256"][:16] in txt, "the Ga table's SHA-256 is not recorded"


def test_activation_law():
    """test-activation-law. A(0) = 0, A(inf) = A_sat exactly, A(t_half) = A_sat/2
    to 1e-9, and EVERY quoted rate carries its scenario label."""
    a_sat = cc.ge71_production_rate()["a_sat_counts_kg_day"]
    assert cc.ge71_activity(0.0, a_sat) == 0.0
    assert cc.ge71_activity(np.inf, a_sat) == a_sat
    assert cc.ge71_activity(cc.GE71_HALF_LIFE_d, a_sat) == pytest.approx(
        0.5 * a_sat, abs=HALF_LIFE_LIMIT_TOL * a_sat)
    assert cc.ge71_activity(1.0, 1.0) < 0.07, "the 1-day fraction should be a few %"

    header, body = _rows(ARTIFACTS["lines"])
    si, ki, ri = (header.index(c) for c in ("scenario", "row_kind", "rate_counts_kg_day"))
    rated = [r for r in body if r[ri] != ""]
    assert rated
    for r in rated:
        assert r[si] not in ("", "n/a"), (
            f"a rate is quoted with no scenario label: {r} (fp-saturation-unstated)")
    # all four scenarios present
    assert {r[si] for r in rated} == {n for n, _ in cc.GE71_SCENARIOS}


def test_branching_sourced_or_bounded():
    """test-branching-sourced-or-bounded. Every branching row carries SOURCED
    with a retrieval record, or BOUNDED. None is written from recollection."""
    br = cc.ge71_branching_disposition()
    assert br["K"]["status"] == "SOURCED"
    assert br["L"]["status"] == "BOUNDED" and br["M"]["status"] == "BOUNDED"

    k = cc.ge71_k_shell_capture_fraction()
    # the derivation must be K-vacancy conservation, checked against the file's
    # own component/total consistency rather than trusted
    assert k["kbeta_components_close"] and k["kauger_components_close"]
    assert 0.0 < k["P_K"] < 1.0
    assert k["P_K"] == pytest.approx(
        (k["I_K_xray_per_100"] + k["I_K_auger_per_100"]) / 100.0)
    assert br["M"]["upper_bound"] == pytest.approx(1.0 - k["P_K"])
    # the bound must be an improvement on the trivial one, or it carries nothing new
    assert br["improvement_factor"] > 2.0

    header, body = _rows(ARTIFACTS["lines"])
    bi, vi = header.index("branching_status"), header.index("branching_value_or_bound")
    for r in body:
        if r[vi] != "" and r[0] == "LINE_RATE":
            assert r[bi] in ("SOURCED", "BOUNDED"), r

    # the retrievals must be integrity-recorded
    man = _text(os.path.join(cc.GE71_DIR, "MANIFEST.md"))
    for p in (cc.GE71_GS_CSV, cc.GE71_XRAY_CSV, cc.GE71_AUGER_CSV, cc.GA_EDGES_DAT):
        assert cc.sha256_of(p) in man, f"{os.path.basename(p)} SHA-256 not in MANIFEST"
    assert "curl" in man.lower()


def test_nu_recoil_named():
    """test-nu-recoil-named. The coincident neutrino recoil is named, computed in
    eV from a SOURCED Q_EC, and its shift expressed as a fraction of one
    reconstructed bin rather than asserted negligible."""
    nu = cc.ge71_neutrino_recoil_eV()
    gs = cc.ge71_ground_state()
    assert nu["q_ec_eV"] == gs["q_ec_keV"] * 1.0e3
    # dimensional identity: [eV]^2 / [eV] = [eV]
    assert nu["T_nu_recoil_eV"] == pytest.approx(
        nu["q_ec_eV"] ** 2 / (2.0 * 71 * params._U_MEV * 1e6), rel=1e-12)
    assert 0.0 < nu["T_nu_recoil_eV"] < 1.0, "expected a genuinely sub-eV recoil"

    in_bins = nu["fraction_of_M_line"] / EREC_BIN_WIDTH_FRACTION
    assert in_bins < NU_RECOIL_MAX_BIN_FRACTION, (
        f"the neutrino recoil shifts the line by {in_bins:.4f} reconstructed bins")
    for path in (ARTIFACTS["lines"], REPORT):
        txt = _text(path)
        assert "NU_RECOIL" in txt or "neutrino" in txt.lower()
        assert f"{nu['T_nu_recoil_eV']:.6f}" in txt or f"{nu['T_nu_recoil_eV']:.4f}" in txt


# --------------------------------------------------------------------------- #
# claim-ec-fold                                                                #
# --------------------------------------------------------------------------- #
def test_no_ia_on_electron_recoil():
    """test-no-ia-on-electron-recoil. The Phase-15 criterion is EVALUATED WITH A
    NUMBER for this line, and the finding is that it comes out the OTHER WAY here
    -- so the exclusion cannot rest on it, and the report says so."""
    ia = cc.ec_ia_criterion(cc.GE71_M_LINE_eV)
    assert ia["omega_bar_e_lower_bound_eV"] == pytest.approx(0.634740, rel=1e-5)
    assert ia["ratio_omega_e_over_omega_nuclear"] == pytest.approx(35.540, rel=1e-4)
    # Phase 15's own number at the grid floor is reproduced, so the comparison is real
    assert ia["phase15_two_W_e_at_grid_floor"] == pytest.approx(0.1574, rel=1e-3)
    # ... and at THIS energy the criterion is satisfied, which is the finding
    assert ia["two_W_e"] > 1.0 and ia["criterion_satisfied_at_this_energy"]
    assert ia["transplant_understatement_factor"] == pytest.approx(5.96, rel=1e-3)
    assert not ia["broadening_applied"]

    # the fold REFUSES broadening rather than merely defaulting to off
    for d in DESIGNS:
        with pytest.raises(ValueError, match="ELECTRONIC"):
            cc.fold_monochromatic_line(d, cc.GE71_M_LINE_eV, 1.0, broaden=True)
        r = cc.fold_monochromatic_line(d, cc.GE71_M_LINE_eV, 1.0)
        assert r["broadening_applied"] is False

    # executed scan: no IA kernel, no exp(-2W) and no nan_to_num in this path
    # Executed scan on the PARSED module, so a mention inside a docstring or a
    # comment cannot be mistaken for a use and a use cannot hide in prose.
    import ast
    src = _text(MODULE)
    assert "nan_to_num" not in src
    tree = ast.parse(src)
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    attrs = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    imported = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.ImportFrom):
            imported |= {(a.asname or a.name) for a in n.names}
        elif isinstance(n, ast.Import):
            imported |= {(a.asname or a.name.split(".")[0]) for a in n.names}
    for banned in ("ia_broadening", "gaussian_broaden", "native_edges"):
        assert banned not in imported, f"{banned} is IMPORTED into this path"
        assert banned not in names and banned not in attrs, \
            f"{banned} is CALLED in this path"
    # ... and it is genuinely absent from the module's runtime namespace
    import qpd_potential.capture_channel as _m
    assert not hasattr(_m, "ia_broadening")

    for path in (ARTIFACTS["erec_TaAl"], ARTIFACTS["erec_AlHf"], REPORT):
        txt = _text(path)
        assert f"{ia['two_W_e']:.2f}" in txt, f"2W_e not reported in {path}"
        assert "SATISFIED" in txt


def test_line_placement_measured():
    """test-line-placement-measured. The reconstructed peak, the mapping slope and
    the in-RoI fraction are MEASURED for both designs, and ROADMAP SC3's clause is
    adjudicated with one of the four verdicts."""
    a_sat = cc.ge71_production_rate()["a_sat_counts_kg_day"]
    bound = a_sat * cc.ge71_branching_disposition()["M"]["upper_bound"]
    for d in DESIGNS:
        r = cc.fold_monochromatic_line(d, cc.GE71_M_LINE_eV, bound)
        # CORRECTED AXIS (params.CALIB_SLOPE = 1.0, CONVENTIONS Section E.1): E_rec
        # ESTIMATES the deposit, so the 158.7 eV line images NEAR its own energy,
        # only mildly compressed by saturation -- NOT halved to ~79 eV as the former
        # eps = 0.5 axis did. The reconstructed image is a bit below the deposit...
        assert 0.7 < r["matrix_mapping_slope_vs_line"] < 0.9
        assert 0.6 * cc.GE71_M_LINE_eV < r["matrix_Erec_mean_eV"] < cc.GE71_M_LINE_eV
        # ...and it lands ABOVE the 100 eV RoI top, so the line does NOT contaminate
        # the signal RoI. The former "inside the RoI" reading was the eps=0.5 artifact.
        assert r["matrix_Erec_mean_eV"] > ROI[1]
        assert r["in_roi_fraction"] == pytest.approx(0.0, abs=1e-9)
        # the deposit energy is also outside the RoI, as it always was
        assert cc.GE71_M_LINE_eV > ROI[1]

    txt = _text(REPORT)
    assert "SC3" in txt
    assert any(v in txt for v in SC_VERDICTS), "SC3 carries no verdict"
    r = cc.fold_monochromatic_line("Ta->Al", cc.GE71_M_LINE_eV, bound)
    assert f"{r['matrix_Erec_mean_eV']:.3f}" in txt or \
        f"{r['matrix_Erec_mean_eV']:.2f}" in txt, \
        "the measured reconstructed position is not in the report"
    assert f"{r['matrix_mapping_slope_vs_line']:.4f}" in txt or \
        f"{r['matrix_mapping_slope_vs_line']:.3f}" in txt


def test_counts_budget_ec():
    """test-counts-budget-ec. retained+leaked closes, residual_fold is zero to
    1e-12 because R's columns sum to 1, and the coincidence of the two residuals
    is STATED rather than presented as two independent confirmations."""
    for d in DESIGNS:
        r = cc.fold_monochromatic_line(d, cc.GE71_M_LINE_eV, 1234.5)
        b = r["counts_budget"]
        assert b["residual_retained_plus_leaked"] < COUNTS_CLOSURE_TOL
        assert b["residual_fold"] < FOLD_RESIDUAL_TOL
        assert b["residuals_coincide_because_no_broadening"] is True
        assert b["reconstructed_counts"] == pytest.approx(b["input_counts"], rel=1e-12)
    for k in ("erec_TaAl", "erec_AlHf"):
        txt = _text(ARTIFACTS[k])
        assert "residual_retained_plus_leaked" in txt
        assert "residual_retained_only" in txt
        assert "COINCIDE BY CONSTRUCTION" in txt


def test_trigger_composition_ec():
    """test-trigger-composition-ec. P_trig == 1 reproduces the untriggered
    spectrum BIT-IDENTICALLY, P(E50) = 1/2 on the DEPOSIT axis, and the
    k-sensitivity over [1, 12] is reported.

    Asserted against params.TRIGGER_E50 rather than a literal, so the identity
    is tested as an identity. E50 moved 0.5 -> 1.0 eV on 2026-07-23 and a
    hardcoded 0.5 would have silently become a test of the wrong energy."""
    e50 = params.TRIGGER_E50.value
    assert float(np.asarray(trigger.P_trig(np.array([e50])))[0]) == pytest.approx(
        0.5, abs=TRIGGER_E50_TOL)
    for d in DESIGNS:
        r = cc.fold_monochromatic_line(d, cc.GE71_M_LINE_eV, 1000.0)
        ones = np.ones_like(r["E_dep_centers_eV"])
        r1 = cc.fold_monochromatic_line(d, cc.GE71_M_LINE_eV, 1000.0,
                                        p_trig_override=ones)
        assert np.array_equal(r1["N_rec_trigger"], r1["N_rec"])
        assert np.array_equal(r1["dRdErec_trigger"], r1["dRdErec"])
        # the trigger is evaluated on the DEPOSIT centres
        assert r["P_trig_on_Edep"].shape == r["E_dep_centers_eV"].shape
        # 2.5 decades above E50, it should be essentially 1
        assert r["P_trig_at_line"] > 0.99

    # k-sensitivity of the TRIGGERED line rate. On the corrected axis (unit
    # calibration slope) the 158.7 eV line images near 130 eV, ABOVE the 10-100 eV
    # RoI, so its in-RoI content is identically ZERO for every k -- a RoI-restricted
    # spread would be 0/0. The line sits 2.5 decades above E50 = 1 eV where P_trig ~ 1
    # for every k, so the meaningful, non-degenerate statement is that the WHOLE
    # triggered line rate is k-insensitive. Measured over the full reconstructed axis.
    for k in (SHARPNESS_RANGE[0], params.TRIGGER_SHARPNESS.value, SHARPNESS_RANGE[1]):
        rk = cc.fold_monochromatic_line("Ta->Al", cc.GE71_M_LINE_eV, 1000.0,
                                        sharpness=k)
        E = rk["E_rec_centers_eV"]
        # the line has left the RoI: no triggered counts inside 10-100 eV, any k
        assert float(rk["N_rec_trigger"][(E >= ROI[0]) & (E <= ROI[1])].sum()) == \
            pytest.approx(0.0, abs=1e-9)
    rates = {}
    for k in (SHARPNESS_RANGE[0], params.TRIGGER_SHARPNESS.value, SHARPNESS_RANGE[1]):
        rk = cc.fold_monochromatic_line("Ta->Al", cc.GE71_M_LINE_eV, 1000.0,
                                        sharpness=k)
        rates[k] = float(np.asarray(rk["N_rec_trigger"]).sum())
    spread = (max(rates.values()) - min(rates.values())) / max(rates.values())
    assert spread < 0.05, f"k-sensitivity on the total triggered line rate is {spread}"
    assert f"{spread*100:.2f}" in _text(REPORT) or "k-sensitivity" in _text(REPORT)


def test_shared_axis_comparison():
    """test-shared-axis-comparison. Every comparison is computed from a COMMITTED
    reconstructed-axis artifact, and both operands are asserted to be on the same
    axis. No deposit-axis quantity is compared against a reconstructed-axis one."""
    for d in DESIGNS:
        cmp = cc.shared_axis_comparison(d)
        assert cmp["axis"] == "RECONSTRUCTED"
        for name in ("cevns", "neutron"):
            assert cmp[name]["axis"] == cmp["axis"], (
                "cross-axis comparison attempted -- Phase 13 caught itself doing "
                "exactly this once")
            assert os.path.isfile(cmp[name]["path"])
        # the band integrator must reproduce the committed headline numbers
        assert cmp["cevns"]["total_counts_kg_day"] == pytest.approx(118.73, rel=1e-3)
        assert cmp["neutron"]["in_roi_counts_kg_day"] == pytest.approx(
            cc.PHASE13_ELASTIC_INROI[d], rel=1e-5)
    assert "RECONSTRUCTED" in _text(REPORT)


# --------------------------------------------------------------------------- #
# claim-phase-closeout                                                         #
# --------------------------------------------------------------------------- #
def test_sc_verdicts_14():
    """test-sc-verdicts-14. All five ROADMAP Phase-14 criteria carry a verdict in
    the Phase-12/13 vocabulary with its evidence located."""
    txt = _text(REPORT)
    for n in range(1, 6):
        assert f"SC{n}" in txt, f"SC{n} has no entry in the closeout"
    found = [v for v in SC_VERDICTS if v in txt]
    assert found, "no verdict vocabulary present"
    # every criterion line must name an evidence path
    for tok in ("artifacts/v2.0/", "data/egaf/", "14-01-CAPTURE-BOUNDS.md"):
        assert tok in txt, f"evidence location {tok} not named"
    # SC2's shape must be honoured
    assert "bounded, not quantified" in txt or "BOUND, not a quantification" in txt


def test_phi_th_disposition():
    """test-phi-th-disposition. Phi_th is named as PHASE 9's product with its
    cutoff convention, SC4 is recorded as discharged on branch (a), the Biffl
    ratio is reported with its direction, and nothing derived is zero."""
    b = cc.biffl_comparison()
    txt = _text(REPORT)
    assert "2.767075" in txt
    assert "Phase 9" in txt or "PHASE 9" in txt
    assert "cadmium" in txt.lower()
    assert "branch (a)" in txt
    assert f"{b['ratio_adopted_over_requirement']:.2f}" in txt
    assert "ABOVE" in txt
    # attributing it to Phase 13 fails
    assert "Phase 13's product" not in txt
    # nothing derived is zero: every capture band and the EC bound are positive
    bd = cc.band_decomposed_rate(cc.sigma_capture_natural_b, per_decade=200)
    assert all(v["rate_counts_kg_day"] > 0 for v in bd["bands"].values())
    a_sat = cc.ge71_production_rate()["a_sat_counts_kg_day"]
    assert a_sat > 0
    assert a_sat * cc.ge71_branching_disposition()["M"]["upper_bound"] > 0


def test_label_and_shielded_audit():
    """test-label-and-shielded-audit. accuracy_label everywhere including ON the
    figure; zero APPLIED shielded-token hits; zero phi_lo uses; veto credit
    exactly 1.0 by construction and not imported."""
    for p in list(ARTIFACTS.values()) + [REPORT, REPORT_01,
                                         os.path.join(_ROOT, "artifacts", "v2.0",
                                                      "ge_capture_xs.csv"),
                                         os.path.join(_ROOT, "artifacts", "v2.0",
                                                      "capture_rate_bands.csv"),
                                         os.path.join(_ROOT, "artifacts", "v2.0",
                                                      "capture_recoil_bounds.csv")]:
        assert "order_of_magnitude" in _text(p), f"no accuracy_label in {p}"
    # ON the figure: the label is drawn into the PDF text stream. The figure is
    # written with pdf.compression = 0 so this is a real read of the file rather
    # than "the figure exists and the report mentions it". matplotlib splits
    # strings across TJ kerning arrays, so the literals are rejoined first --
    # otherwise "order_of_magnitude" is invisible as "or" + "der_of_magnitude".
    import re
    with open(FIGURE, "rb") as fh:
        blob = fh.read()
    text = "".join(m.decode("latin-1", "replace")
                   for m in re.findall(rb"\(([^()]*)\)", blob))
    assert "order_of_magnitude" in text, \
        "accuracy_label is not present in the figure's text stream"
    assert "RECONSTRUCTED" in text, \
        "the figure does not state the axis it is drawn on"

    # Phase-9 shielded-token scan over this phase's module and artifacts.
    # SHIELDED_TOKENS is the list the plan names. SHIELDED_TOKENS_EXTRA is Plan
    # 09-03's environment-assembly addendum, and one of its members collides
    # semantically: "residual" there means a residual dose rate AFTER shielding,
    # while here it is a counts-CONSERVATION residual on the Phase-13 pattern.
    # The extra tokens are still scanned, with that one narrow, named exemption --
    # "dru" and "Table 5" carry no such collision and remain live.
    import re
    _RESIDUAL_EXEMPT = re.compile(
        r"residual_retained|residual_fold|band_sum_residual|residuals_coincide"
        r"|with residual|to residual", re.IGNORECASE)
    targets = [MODULE, REPORT, REPORT_01] + list(ARTIFACTS.values())
    applied = []
    for path in targets:
        for i, line in enumerate(_text(path).splitlines(), 1):
            for name, pattern in SHIELDED_TOKENS + SHIELDED_TOKENS_EXTRA:
                if not re.search(pattern, line, flags=re.IGNORECASE):
                    continue
                if is_not_applied(line):
                    continue
                if name == "residual" and _RESIDUAL_EXEMPT.search(line):
                    continue
                applied.append((path, i, name, line.strip()[:110]))
    assert applied == [], f"APPLIED shielded-token hits: {applied}"

    # phi_lo line scan: definitions and refusals only
    for line in _text(MODULE).splitlines():
        if "phi_lo" in line:
            s = line.lstrip()
            assert s.startswith("#") or s.startswith('"') or s.startswith("'"), line

    # veto credit is exactly 1.0 BY CONSTRUCTION here, not imported
    assert "veto" not in _text(MODULE).lower().replace("veto credit is exactly", "")


def test_disposition_rows_02():
    """test-disposition-rows-02. The register test passes with no unregistered
    artifact across BOTH plans of this phase."""
    reg = lg.load_register()
    for p in ("artifacts/v2.0/ge_capture_xs.csv",
              "artifacts/v2.0/capture_rate_bands.csv",
              "artifacts/v2.0/capture_recoil_bounds.csv",
              "artifacts/v2.0/ge71_ec_lines.csv",
              "artifacts/v2.0/ge71_ec_dRdErec_TaAl.csv",
              "artifacts/v2.0/ge71_ec_dRdErec_AlHf.csv",
              "data/ge71_ec/livechart_71ge_ground_states.csv",
              "data/ge71_ec/livechart_71ge_decay_rads_x.csv",
              "data/ge71_ec/livechart_71ge_decay_rads_e.csv"):
        assert p in reg, f"{p} has no disposition row"
        assert reg[p].disposition in lg.DISPOSITION_VALUES
        assert len(reg[p].reason) > 40

    files = subprocess.run(["bash", "-c", "git ls-files | grep -E '\\.(csv|npz)$'"],
                           cwd=_ROOT, capture_output=True, text=True).stdout.split()
    missing = sorted(set(files) - set(reg))
    assert missing == [], f"tracked artifacts with no disposition row: {missing}"


@pytest.mark.parametrize("key", sorted(ARTIFACTS))
def test_accuracy_label_column(key):
    header, body = _rows(ARTIFACTS[key])
    assert "accuracy_label" in header
    ai = header.index("accuracy_label")
    assert body
    for row in body:
        assert row[ai] == "order_of_magnitude", row
