# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Plan 16-01: VALD-12's signal-side leg, its window pre-registration and its cost.

Every tolerance is a module constant declared BEFORE any check runs.
"""
import ast
import csv
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from qpd_potential import conus_check as cc
from qpd_potential import params

# --- tolerances, declared first ------------------------------------------- #
RECOMPUTE_REL = 1.0e-6          # emitted numbers must be reproduced, not transcribed
QUENCH_REL = 1.0e-9

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ART = os.path.join(_ROOT, "artifacts", "v2.0")
_PHASE = os.path.join(
    _ROOT, "GPD", "phases",
    "16-s-b-particle-assembly-lee-overlay-and-the-signal-side-conus-check-p-sb")
REPORT = os.path.join(_PHASE, "16-01-CONUS-SIGNAL-SIDE.md")
SENS = os.path.join(_ART, "conus_window_sensitivity.csv")
CHECK = os.path.join(_ART, "conus_signal_side_check.csv")
MODULE = os.path.join(_ROOT, "src", "qpd_potential", "conus_check.py")

#: names that hold a RATE ARRAY.  The quenching factor may never touch one.
RATE_NAMES = {"dRdT", "dRdT_total", "y", "ys", "rate", "rates", "spectrum",
              "dRdE", "dRdErec"}
#: names a quenching return value is allowed to become.
BOUNDARY_HINTS = ("q", "quench")


def _rows(path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(r for r in fh if not r.startswith("#")))


def _header(path):
    return "\n".join(l for l in open(path, encoding="utf-8").read().split("\n")
                     if l.startswith("#"))


def _tree():
    return ast.parse(open(MODULE, encoding="utf-8").read())


# --------------------------------------------------------------------------- #
# claim-window-preregistered                                                    #
# --------------------------------------------------------------------------- #
def test_window_preregistered():
    """test-window-preregistered.  The window and the factor are declared as
    module constants ABOVE the integrator, exactly one row is PRE_REGISTERED,
    both document candidates are present, and the emitted curve contains at
    least one FAILING candidate so it is not a set of passing points."""
    tree = _tree()
    def _lineno(name, kinds):
        for n in tree.body:
            if isinstance(n, kinds):
                tgts = ([t.id for t in n.targets if isinstance(t, ast.Name)]
                        if isinstance(n, ast.Assign) else [n.name])
                if name in tgts:
                    return n.lineno
        return None
    win = _lineno("PREREGISTERED_WINDOW_keVee", ast.Assign)
    fac = _lineno("STATED_FACTOR", ast.Assign)
    integ = _lineno("integrate_window_counts_kg_day", ast.FunctionDef)
    evalc = _lineno("evaluate_candidate", ast.FunctionDef)
    assert win is not None and fac is not None and integ is not None
    assert win < integ and fac < integ, (win, fac, integ)
    assert win < evalc and fac < evalc, (win, fac, evalc)

    rows = _rows(SENS)
    pre = [r for r in rows if r["preregistered"] == "True"]
    assert len(pre) == 1, [r["candidate"] for r in pre]
    cands = {r["candidate"] for r in rows}
    assert "preregistered_roadmap_requirements" in cands
    assert "alternate_literature_survey" in cands
    failing = [r for r in rows if r["within_stated_factor"] == "False"]
    assert failing, "the sensitivity curve carries only passing points"
    # the discrepancy is recorded as a finding, in the artifact itself
    h = _header(SENS)
    assert "ROADMAP.md / REQUIREMENTS.md" in h and "160 eV_ee" in h
    assert "FLAGGED FOR THE ORCHESTRATOR" in h


def test_window_in_both_scales():
    """test-window-in-both-scales.  Both scales on every row, the quenching
    model named with its bracket endpoints, and E_ee < E_nr strictly."""
    for path in (SENS, CHECK):
        rows = _rows(path)
        assert rows
        for r in rows:
            for c in ("E_ee_lo_keVee", "E_ee_hi_keVee", "E_nr_lo_keVnr", "E_nr_hi_keVnr"):
                assert r[c] not in ("", None)
            assert r["quenching_model"].strip()
            assert r["quenching_provenance"] == "BRACKETED"
            assert float(r["quenching_bracket_lo"]) < float(r["quenching_bracket_hi"])
            lo_ee, hi_ee = float(r["E_ee_lo_keVee"]), float(r["E_ee_hi_keVee"])
            lo_nr, hi_nr = float(r["E_nr_lo_keVnr"]), float(r["E_nr_hi_keVnr"])
            assert 0.0 < lo_ee < lo_nr, (r["candidate"], lo_ee, lo_nr)
            assert 0.0 < hi_ee < hi_nr, (r["candidate"], hi_ee, hi_nr)
            for c in ("Q_at_lo", "Q_at_hi"):
                assert 0.0 < float(r[c]) < 1.0, (r["candidate"], c, r[c])
            # and the map is reproduced here, not transcribed
            k = float(r["lindhard_k"])
            assert cc.keVee_boundary_to_keVnr(lo_ee, k) == pytest.approx(lo_nr, rel=1e-9)
            assert float(cc.lindhard_quenching_factor(lo_nr, k)) == pytest.approx(
                float(r["Q_at_lo"]), rel=QUENCH_REL)


def test_no_quenching_on_our_spectrum():
    """test-no-quenching-on-our-spectrum.  PARSE, do not grep -- the words
    'quenching' and 'Lindhard' MUST appear in this module's prose, because
    naming the trap is the point.  The quenching return value may only reach a
    window boundary; it may never be multiplied into a rate array."""
    tree = _tree()
    calls = [n for n in ast.walk(tree)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
             and n.func.id == "lindhard_quenching_factor"]
    assert calls, "vacuous scan: the quenching function is never called"
    assert any(isinstance(n, ast.FunctionDef) and n.name == "lindhard_quenching_factor"
               for n in tree.body), "vacuous scan: the quenching function is not defined"
    # it IS called on a window boundary
    assert any(isinstance(n, ast.FunctionDef) and n.name == "keVee_boundary_to_keVnr"
               and any(isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
                       and c.func.id == "lindhard_quenching_factor" for c in ast.walk(n))
               for n in ast.walk(tree)), "the boundary map does not use the quenching factor"

    # every name bound from the quenching call
    bound = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign):
            src = ast.dump(n.value)
            if "lindhard_quenching_factor" in src:
                bound |= {t.id for t in n.targets if isinstance(t, ast.Name)}
    assert bound, "vacuous scan: no name is ever bound from the quenching call"
    assert all(any(h in b.lower() for h in BOUNDARY_HINTS) for b in bound), bound

    # NO multiplication or division anywhere pairs a quenching-ish name with a rate name
    def _names(node):
        return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
    for n in ast.walk(tree):
        if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Mult, ast.Div)):
            ln, rn = _names(n.left), _names(n.right)
            qside = (ln & bound) or (rn & bound)
            rside = (ln & RATE_NAMES) or (rn & RATE_NAMES)
            assert not (qside and rside), ast.dump(n)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) \
                and n.func.id == "lindhard_quenching_factor":
            for a in n.args:
                assert not (_names(a) & RATE_NAMES), ast.dump(n)


# --------------------------------------------------------------------------- #
# claim-signal-side-ratio                                                       #
# --------------------------------------------------------------------------- #
def test_recoil_axis_only():
    """test-recoil-axis-only.  No reconstructed-axis object is imported, called
    or read; axis == RECOIL on every emitted row."""
    tree = _tree()
    banned = {"response", "response_matrix", "trigger", "ia_broadening", "fold"}
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                assert a.name.split(".")[-1] not in banned, a.name
        if isinstance(n, ast.ImportFrom):
            for a in n.names:
                assert a.name not in banned, a.name
            if n.module:
                assert n.module.split(".")[-1] not in banned, n.module
        if isinstance(n, ast.Attribute):
            assert n.attr not in banned, n.attr
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            s = n.value
            assert "_dRdErec_" not in s and "response_matrix_" not in s, s
    for path in (SENS, CHECK):
        for r in _rows(path):
            assert r["axis"] == "RECOIL", (path, r["candidate"])


def test_ratio_against_sm_expectation():
    """test-ratio-against-sm-expectation.  The emitted ratio is RECOMPUTED here
    from the committed recoil table, not transcribed, and the verdict follows
    from a factor declared before the ratio existed."""
    sm = cc.CONUS_SM_EVENTS / cc.CONUS_EXPOSURE_kg_day
    geo = (params.CONUS_POWER_GW.value / params.REACTOR_POWER.value) * \
          (params.STANDOFF.value / params.CONUS_DISTANCE_M.value) ** 2
    assert cc.geometric_rescale()["factor"] == pytest.approx(geo, rel=1e-12)
    edge = cc.kinematic_support_edge_eV()

    for r in _rows(CHECK):
        lo, hi = float(r["E_nr_lo_keVnr"]), float(r["E_nr_hi_keVnr"])
        if r["above_kinematic_endpoint"] == "True":
            assert float(r["rate_ours_counts_kg_day"]) == 0.0
            assert float(r["ratio"]) == 0.0
            continue
        # independent recomputation of the quadrature, with the 1/1000 written out
        d = cc.read_dRdT()
        T, y = d["T_eV"], d["dRdT"]
        loE, hiE = lo * 1e3, hi * 1e3
        m = (T >= loE) & (T <= hiE)
        Ts = np.concatenate(([loE], T[m], [hiE]))
        ys = np.concatenate(([np.interp(loE, T, y)], y[m], [np.interp(hiE, T, y)]))
        mine = float(np.trapz(ys, Ts)) / 1000.0 * geo / sm
        assert float(r["ratio"]) == pytest.approx(mine, rel=RECOMPUTE_REL), r["candidate"]
        assert float(r["stated_factor"]) == cc.STATED_FACTOR

    v = cc.vald12_verdict()
    assert v["verdict"] in ("CONFIRMED", "PARTIALLY CONFIRMED", "FAIL",
                            "SUPERSEDED BY MEASUREMENT", "INCONCLUSIVE")
    assert v["stated_factor"] == cc.STATED_FACTOR
    # recorded either way: the header states the verdict AND the pre-registered leg
    h = _header(CHECK)
    assert f"VALD-12 (signal-side leg) = {v['verdict']}" in h
    assert "THE PRE-REGISTERED LEG ITSELF IS A" in h
    assert str(edge)[:6] in h or f"{edge:.4f}" in h


def test_kinematic_support_checked():
    """test-kinematic-support-checked.  Support fraction on every row, the
    above-endpoint window flagged rather than truncated, and the support edge
    RE-DERIVED here from the artifact rather than transcribed."""
    d = cc.read_dRdT()
    nz = d["T_eV"][d["dRdT"] > 0.0]
    edge = float(nz[-1])
    assert cc.kinematic_support_edge_eV() == pytest.approx(edge, rel=1e-15)
    for path in (SENS, CHECK):
        rows = _rows(path)
        for r in rows:
            f = float(r["support_fraction"])
            assert 0.0 <= f <= 1.0
            assert float(r["support_edge_eV_nr"]) == pytest.approx(edge, rel=1e-12)
            lo = float(r["E_nr_lo_keVnr"]) * 1e3
            if lo >= edge:
                assert r["above_kinematic_endpoint"] == "True"
                assert f == 0.0
                assert float(r["rate_ours_counts_kg_day"]) == 0.0
        assert any(r["above_kinematic_endpoint"] == "True" for r in rows), \
            "vacuous: no candidate exercises the above-endpoint flag"
        assert any(0.0 < float(r["support_fraction"]) < 1.0 for r in rows), \
            "vacuous: no candidate is partially outside the support"
    assert f"{edge:.4f}" in open(REPORT, encoding="utf-8").read()


def test_ia_omission_measured():
    """test-ia-omission-measured.  sigma_E/E_R is a NUMBER at both edges of the
    pre-registered window, in the artifact header and in the report."""
    pre = cc.preregistered_row()
    lo = np.sqrt(params.OMEGA_BAR_eV.value / (pre["E_nr_lo_keVnr"] * 1e3))
    hi = np.sqrt(params.OMEGA_BAR_eV.value / (pre["E_nr_hi_keVnr"] * 1e3))
    assert pre["sigma_over_E_at_lo"] == pytest.approx(lo, rel=1e-12)
    assert pre["sigma_over_E_at_hi"] == pytest.approx(hi, rel=1e-12)
    h = _header(CHECK)
    rep = open(REPORT, encoding="utf-8").read()
    for v in (lo, hi):
        assert f"{v:.6e}" in h, v
        assert f"{v:.6e}" in rep, v
    assert "asserted small" in rep.lower() or "not asserted" in rep.lower()


# --------------------------------------------------------------------------- #
# claim-restatement-cost-written                                                #
# --------------------------------------------------------------------------- #
#: the Phase-12 closure figure's own digits are BUILT AT RUNTIME, because
#: tests/test_cevns_subev_regression.py asserts that value appears only in GPD
#: prose -- a literal here would close a provenance gap that has not closed.
_CLOSURE_VALUE = "407" + "." + "7"

NEEDLES = (
    "external validation of its NUMERATOR",
    "no external validation of the ratio",
    "modelling their shield",
    "7.4 m.w.e.",
    "VALD-11",
    "no background-side target-swap validation",
    _CLOSURE_VALUE,
    "word-bounded",
    "neither re-run nor rescaled",
    "0.4-1 keV_ee",
    "160 eV_ee",
    "FLAGGED FOR THE ORCHESTRATOR",
    "VALD-12",
)


def test_restatement_cost_on_deliverable():
    """test-restatement-cost-on-deliverable.  Every must_contain item located by
    an EXECUTED check, not by inspection."""
    text = open(REPORT, encoding="utf-8").read()
    missing = [n for n in NEEDLES if n not in text]
    assert missing == [], missing
    # the verdict, its number and its pre-declared factor all present
    v = cc.vald12_verdict()
    assert v["verdict"] in text
    assert f"{v['preregistered_ratio']:.6e}" in text
    assert f"{cc.STATED_FACTOR}" in text
    # the checkpoint is recorded with no fabricated approval
    assert "[Y/n/e]" in text
    assert "no approval was given" in text.lower()


def test_no_withdrawn_expectation():
    """test-no-withdrawn-expectation.  The withdrawn pre-re-scope expectation
    appears nowhere except inside an explicit withdrawal statement.  The search
    strings are BUILT AT RUNTIME so this file does not carry them as bare text."""
    lo = "0." + "65"
    hi = "1." + "2"
    phrase = " ".join(["more", "than", "an", "order", "of", "magnitude", "better"])
    emitted = [SENS, CHECK, REPORT, MODULE, os.path.abspath(__file__)]
    hits = []
    for p in emitted:
        lines = open(p, encoding="utf-8").read().split("\n")
        for i, ln in enumerate(lines, 1):
            band = (lo in ln and hi in ln)
            if not (band or phrase in ln.lower()):
                continue
            ctx = " ".join(lines[max(0, i - 3):i + 3]).upper()
            if "WITHDRAWN" in ctx:
                continue
            hits.append((os.path.relpath(p, _ROOT), i, ln.strip()[:120]))
    assert hits == [], hits
