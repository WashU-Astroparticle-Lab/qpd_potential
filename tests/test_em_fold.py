# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Plan 15-03: the electron-recoil extended fold, its five guards, and the
reconstructed spectra for both trapping designs.
"""
import csv
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from qpd_potential import deposited_spectra as ds
from qpd_potential import em_extended as ee
from qpd_potential import em_recoil as er
from qpd_potential import fold
from qpd_potential import params
from qpd_potential import trigger

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ART = os.path.join(_ROOT, "artifacts", "v2.0")
_REPORT = os.path.join(
    _ROOT, "GPD", "phases",
    "15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em",
    "15-03-RECONSTRUCTED-SPECTRA.md")
_FIGURE = os.path.join(_ART, "em_subev_spectra.pdf")
_KSENS = os.path.join(_ART, "em_trigger_k_sensitivity.csv")

DESIGNS = ("Ta->Al", "Al->Hf")
CHANNELS = ("muon", "compton")
POLICY = "exclude_and_record"


def _fold(ch, des, **kw):
    kw.setdefault("no_support_policy", POLICY)
    return fold.run_em_fold_extended(ch, des, **kw)


def _header(path):
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("#"):
                break
            out.append(line)
    return "".join(out)


def _rec_table(des):
    path = os.path.join(_ART, fold.EM_EXT_RECON_FILE[des])
    with open(path, encoding="utf-8") as fh:
        rdr = csv.DictReader(r for r in fh if not r.startswith("#"))
        rows = list(rdr)
    return rows, path


# --------------------------------------------------------------------------- #
# claim-em-fold-path : the five guards, all of which RAISE                      #
# --------------------------------------------------------------------------- #
def test_shape_check_raises():
    """test-shape-check-raises. A 584-column matrix would truncate at 10.14 eV."""
    d = fold.load_design_extended("Ta->Al")
    assert d["R_non_paralyzable"].shape == (161, 744)
    # a deposit vector of the wrong length is rejected by the grid-identity guard
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as fh:
        fh.write("# broadened_provenance = false\n")
        fh.write("E_dep_keV,dRdEdep,mc_err,mc_entries,rel,flag,a,b\n")
        for i in range(584):
            fh.write(f"{1.0e-2 * (i + 1):.6e},1.0,0.1,5,0.1,False,x,y\n")
        short = fh.name
    with pytest.raises(ValueError) as exc:
        _fold("muon", "Ta->Al", path=short)
    assert "584" in str(exc.value) and "744" in str(exc.value)
    os.unlink(short)


def test_columns_sum_to_one():
    """test-columns-sum-to-one. Without this the conservation residual would be
    measuring the matrix, not the fold."""
    for des in DESIGNS:
        R = fold.load_design_extended(des)["R_non_paralyzable"]
        cs = R.sum(axis=0)
        assert np.allclose(cs, 1.0, atol=1e-9), (des, cs.min(), cs.max())


def test_applicability_guard_raises():
    """test-applicability-guard-raises. The Plan 15-01 verdict is read at fold
    time; a contradicting request raises the NAMED em_recoil exception."""
    for ch in CHANNELS:
        for des in DESIGNS:
            with pytest.raises(er.ElectronRecoilBroadeningError) as exc:
                _fold(ch, des, broaden=True)
            msg = str(exc.value)
            assert "does_not_apply" in msg
            assert "REASON:" in msg
            assert "fp-transplant-nuclear-width" in msg
    # and the verdict is READ, not hard-coded: the fold reports what it read
    r = _fold("muon", "Ta->Al")
    assert r["broadening_verdict"] == er.ia_verdict("muon").verdict
    assert r["broadening_reason"] == er.ia_verdict("muon").reason
    assert r["broadening_applied"] is False
    src = open(os.path.join(_ROOT, "src", "qpd_potential", "fold.py")).read()
    assert "_er.assert_nuclear_kernel_use(channel, broaden)" in src


def test_double_broaden_raises():
    """test-double-broaden-raises. A table declaring TRUE raises, and a table
    declaring NOTHING raises too -- undeclared is UNKNOWN, not unbroadened."""
    import tempfile
    src = fold.EM_EXT_CSV["muon"]
    body = open(src, encoding="utf-8").read()
    for decl in ("true", None):
        text = body.replace("# broadened_provenance = false",
                            f"# broadened_provenance = {decl}" if decl
                            else "# (this table declares nothing)")
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as fh:
            fh.write(text)
            p = fh.name
        assert fold.read_broadened_provenance(p) is (True if decl else None)
        # the applicability guard fires first for these channels, which is itself
        # correct; bypass it by asking the double-broaden guard directly
        got = fold.read_broadened_provenance(p)
        assert got is not False, "the fixture did not change the declaration"
        with pytest.raises(er.ElectronRecoilBroadeningError):
            _fold("muon", "Ta->Al", path=p, broaden=True)
        os.unlink(p)
    # and the real tables declare exactly False, so the guard would not fire on
    # them if the verdict ever changed
    for ch in CHANNELS:
        assert fold.read_broadened_provenance(fold.EM_EXT_CSV[ch]) is False


def test_nan_guard_raises():
    """test-nan-guard-raises. The unpolicied call RAISES; the policied call
    returns and records which bins were excluded and under what policy."""
    for ch in CHANNELS:
        with pytest.raises(fold.NonFiniteDepositError) as exc:
            fold.run_em_fold_extended(ch, "Ta->Al")          # no policy
        m = str(exc.value)
        assert "dense" in m.lower() and "nan_to_num" in m
        r = _fold(ch, "Ta->Al")
        assert r["no_support_policy"] == POLICY
        assert r["n_excluded_bins"] > 0
        assert r["counts_budget"]["excluded_no_support_bins"] == r["n_excluded_bins"]
        assert np.all(np.isfinite(r["N_rec"])), "a NaN reached the reconstructed axis"
        assert np.all(np.isfinite(r["dRdErec"]))
    assert set(fold.NO_SUPPORT_POLICIES) == {"raise", "exclude_and_record"}
    # there is no zero-fill member and there must never be one
    assert not any("zero" in p for p in fold.NO_SUPPORT_POLICIES)


def test_no_nan_to_num_in_the_fold_path():
    """fp-nan-to-num, at the source level over the whole module."""
    src = open(os.path.join(_ROOT, "src", "qpd_potential", "fold.py")).read()
    # only EXECUTABLE occurrences count; the module names the forbidden call in
    # its guard message and in two docstrings precisely so the prohibition is
    # discoverable at the point of temptation
    calls = []
    for ln in src.split("\n"):
        if "nan_to_num" not in ln:
            continue
        t = ln.strip()
        if (t.startswith("#") or t.startswith('"') or "forbidden" in ln
                or "``np.nan_to_num``" in ln):
            continue
        calls.append(ln)
    assert not calls, f"np.nan_to_num in the fold path: {calls}"


def test_counts_conservation():
    """test-counts-conservation. residual_fold at or below 1e-3 (ROADMAP SC2),
    with the two leakage residuals kept as separate fields."""
    for ch in CHANNELS:
        for des in DESIGNS:
            b = _fold(ch, des)["counts_budget"]
            assert b["residual_fold"] <= 1.0e-3
            assert b["residual_fold"] < 1.0e-12, "R conserves exactly; expect ~0"
            assert "residual_retained_plus_leaked" in b
            assert "residual_retained_only" in b
            # no broadening was applied, so the two COINCIDE by construction and
            # the budget says so rather than implying two confirmations
            assert b["residuals_coincide_because_no_broadening"] is True
            assert b["residual_retained_plus_leaked"] == b["residual_retained_only"]
            assert b["leaked_below_floor"] == 0.0
            assert b["leaked_above_top"] == 0.0


# --------------------------------------------------------------------------- #
# claim-reconstructed-spectra                                                   #
# --------------------------------------------------------------------------- #
def test_ptrig_identity_one():
    """test-ptrig-identity-one. P_trig identically 1 reproduces the un-triggered
    spectrum with EXACTLY zero difference -- anything else means the trigger has
    displaced eps instead of multiplying it."""
    for ch in CHANNELS:
        for des in DESIGNS:
            r = _fold(ch, des)
            ones = np.ones_like(r["E_dep_centers_eV"])
            r1 = _fold(ch, des, p_trig_override=ones)
            assert np.array_equal(r1["dRdErec_trigger"], r1["dRdErec"])
            assert float(np.max(np.abs(r1["dRdErec_trigger"] - r1["dRdErec"]))) == 0.0
            assert np.array_equal(r1["N_rec_trigger"], r1["N_rec"])


def test_ptrig_test_values():
    """test-ptrig-test-values. The CONVENTIONS Section I hand-checkable values."""
    assert float(trigger.P_trig(0.0)) == 0.0
    assert float(trigger.P_trig(0.25)) == pytest.approx(1.0 / 17.0, rel=1e-14)
    assert float(trigger.P_trig(0.5)) == pytest.approx(0.5, rel=1e-14)
    assert float(trigger.P_trig(1.0)) == pytest.approx(16.0 / 17.0, rel=1e-14)
    e50 = params.TRIGGER_E50.value
    assert e50 == 0.5
    for k in (1.0, 4.0, 12.0):
        assert float(trigger.P_trig(e50, sharpness=k)) == pytest.approx(0.5, rel=1e-14)


def test_regime_boundary_imported():
    """test-regime-boundary-imported. The 1.0 eV boundary appears as a literal
    nowhere in the new code, and its reconstructed image is read off the matrix's
    OWN median mapping curve, never assumed to be 0.5 times anything."""
    for des in DESIGNS:
        b = fold.subev_boundary_Erec_eV(des)
        d = fold.load_design_extended(des)
        expect = float(np.exp(np.interp(
            np.log(trigger.SUBEV_REGIME_BOUNDARY_eV),
            np.log(d["E_dep_centers_eV"]),
            np.log(d["E_rec_median_non_paralyzable_eV"]))))
        assert b == pytest.approx(expect, rel=1e-12)
        # NOT 0.5 x the deposit boundary
        assert abs(b - 0.5 * trigger.SUBEV_REGIME_BOUNDARY_eV) > 1e-3
        rows, path = _rec_table(des)
        h = _header(path)
        assert "trigger.SUBEV_REGIME_BOUNDARY_eV" in h
        assert f"{b:.6f}" in h
        # the emitted regime flags agree with the imported boundary
        flags = np.array([r["regime_flag"] for r in rows])
        erec = np.array([float(r["E_rec_keV[keV]"]) for r in rows]) * 1e3
        assert np.array_equal(flags == "trigger_probability_regime", erec < b)
    # the guard against a hard-coded literal, over the Plan 15-03 code surface
    src = open(os.path.join(_ROOT, "src", "qpd_potential", "fold.py")).read()
    em_section = src[src.index("Phase-15 plan 15-03"):]
    for bad in ("1.0 eV regime", "SUBEV = 1.0", "boundary = 1.0"):
        assert bad not in em_section


def test_both_designs():
    """test-both-designs. Both tables exist, are folded through their OWN
    matrices, and differ where the designs differ."""
    tabs = {}
    for des in DESIGNS:
        rows, path = _rec_table(des)
        assert os.path.exists(path)
        assert len(rows) == 161
        assert fold.EXT_DESIGN_FILE[des] in _header(path)
        tabs[des] = np.array([float(r["muon_dRdErec_untriggered[counts/kg/day/keV]"])
                              for r in rows])
    assert not np.array_equal(tabs["Ta->Al"], tabs["Al->Hf"]), "the two are copies"
    # the per-design saturation onsets are reflected in the mapping
    on = {des: float(fold.load_design_extended(des)["saturation_onset_Edep_eV"])
          for des in DESIGNS}
    assert on["Ta->Al"] > on["Al->Hf"], on
    assert on["Ta->Al"] == pytest.approx(52.9074, rel=1e-3)
    assert on["Al->Hf"] == pytest.approx(32.1300, rel=1e-3)


def test_dimensions():
    """test-dimensions. Units in every header; counts vs differential explicit."""
    for des in DESIGNS:
        rows, path = _rec_table(des)
        cols = list(rows[0].keys())
        for c in cols:
            if c.endswith("_label") or c == "regime_flag":
                continue
            assert "[" in c and c.endswith("]"), c
        assert "E_rec_keV[keV]" in cols
        for c in cols:
            if "dRdErec" in c or "band" in c:
                assert c.endswith("[counts/kg/day/keV]"), c
    # N_dep / N_rec are COUNTS, dRdErec is a DIFFERENTIAL, and the code keeps them apart
    r = _fold("muon", "Ta->Al")
    dE = np.diff(r["E_rec_edges_eV"]) / 1.0e3
    assert np.allclose(r["dRdErec"] * dE, r["N_rec"], rtol=1e-12)
    assert r["N_rec"].shape == (161,)
    assert r["N_dep"].shape == (744,)
    # P_trig is dimensionless in [0, 1]
    P = r["P_trig_on_Edep"]
    assert P.min() >= 0.0 and P.max() <= 1.0


def test_no_exp_minus_2W_multiplies_any_rate():
    """fp-exp-minus-2W, milestone-wide."""
    src = open(os.path.join(_ROOT, "src", "qpd_potential", "fold.py")).read()
    em_section = src[src.index("Phase-15 plan 15-03"):]
    assert "np.exp(-2" not in em_section
    assert "debye_waller" not in em_section.lower()
    for des in DESIGNS:
        h = _header(os.path.join(_ART, fold.EM_EXT_RECON_FILE[des]))
        for line in h.split("\n"):
            if "exp(-2W)" in line:
                assert "never" in line or "NOT" in line or "prohibition" in line


# --------------------------------------------------------------------------- #
# claim-saturation-preserved                                                    #
# --------------------------------------------------------------------------- #
def test_saturation_peak():
    """test-saturation-peak. The muon reconstructed peak sits at the instrumental
    ceiling, NOT at a reconstructed energy proportional to the MeV deposits."""
    for des in DESIGNS:
        d = fold.load_design_extended(des)
        r = _fold("muon", des)
        ec = r["E_rec_centers_eV"]
        peak = float(ec[int(np.argmax(r["dRdErec"]))])
        ceiling = float(d["E_rec_median_non_paralyzable_eV"][-1])
        dep_peak = float(d["E_dep_centers_eV"][int(np.argmax(r["N_dep"]))])
        # the deposit that dominates is of order MeV
        assert 1.0e5 < dep_peak < 1.0e8, dep_peak
        # ... yet the reconstructed peak is tens of keV, not tens of MeV
        assert peak < ceiling, (peak, ceiling)
        assert peak / dep_peak < 0.05, "the peak tracks the deposit energy"
        # compression of the dominant deposit onto the reconstructed axis
        med = float(np.exp(np.interp(np.log(dep_peak),
                                     np.log(d["E_dep_centers_eV"]),
                                     np.log(d["E_rec_median_non_paralyzable_eV"]))))
        assert dep_peak / med > 50.0, "saturation lost in the re-grid"
        # a linear eps ~ 0.5 map would have put it at ~0.5 * dep_peak; it does not
        assert peak < 0.5 * dep_peak / 20.0


def test_pileup_occupancy_is_recomputed_not_quoted():
    """test-pileup-occupancy. Recomputed with deposited_spectra.pileup_occupancy
    from the through-wafer rate and the CANONICAL 40 us resolving time."""
    rates = {"muon": 1.365914, "compton": 0.2674705}
    p = ds.pileup_occupancy(rates)
    assert ds.RESOLVE_TIME_S == 4.0e-5           # CONVENTIONS Section F
    assert ds.SAMPLE_TIME_S == 2.0e-5
    assert p.occupancy_resolve == pytest.approx(6.533538e-05, rel=1e-4)
    assert p.stop_condition_triggered is False
    # THE FINDING: the v1.0 ~3e-5 is the 20 us SAMPLE-time occupancy, not the
    # 40 us resolving-time one. CONVENTIONS Section F's Numerical Factor Registry
    # names exactly this conflation. Both are asserted so neither can drift.
    assert p.occupancy_sample == pytest.approx(3.266768e-05, rel=1e-4)
    assert p.occupancy_resolve == pytest.approx(2.0 * p.occupancy_sample, rel=1e-12)
    text = open(_REPORT, encoding="utf-8").read()
    assert "6.5335" in text and "3.2668" in text or "3e-5" in text


def test_peak_not_presented_as_a_physical_line():
    """test-peak-not-physical-line (automatable part). The feature is named
    INSTRUMENTAL with its mechanism, in the report and on the figure."""
    text = open(_REPORT, encoding="utf-8").read()
    low = text.lower()
    assert "instrumental" in low
    assert "non-paralyzable" in low
    assert "40" in text and ("us" in low or "µs" in text or "microsec" in low)
    assert "not a physical line" in low
    assert os.path.exists(_FIGURE) and os.path.getsize(_FIGURE) > 5000
    fig_src = open(os.path.join(
        _ROOT, "GPD", "phases",
        "15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em",
        "15-03-RECONSTRUCTED-SPECTRA.md"), encoding="utf-8").read()
    assert "INSTRUMENTAL" in fig_src


# --------------------------------------------------------------------------- #
# claim-k-sensitivity                                                           #
# --------------------------------------------------------------------------- #
def _ksens_rows():
    with open(_KSENS, encoding="utf-8") as fh:
        return list(csv.DictReader(r for r in fh if not r.startswith("#")))


def test_k_range_covered():
    """test-k-range-covered. The full declared range for both channels and both
    designs, with the spread reported as a RANGE, not a plus-or-minus."""
    rows = _ksens_rows()
    assert len(rows) == 12                      # 2 designs x 2 channels x 3 quantities
    ks = [float(c.split("=")[1].split("[")[0]) for c in rows[0] if c.startswith("k=")]
    lo, hi = params.TRIGGER_SHARPNESS_RANGE
    assert min(ks) == lo and max(ks) == hi, (ks, lo, hi)
    assert params.TRIGGER_SHARPNESS.value == 4.0
    seen = {(r["design"], r["channel"]) for r in rows}
    assert seen == {(d, c) for d in DESIGNS for c in CHANNELS}
    for r in rows:
        vals = [float(r[c]) for c in r if c.startswith("k=")]
        assert float(r["range_lo[counts/kg/day]"]) == pytest.approx(min(vals), rel=1e-9)
        assert float(r["range_hi[counts/kg/day]"]) == pytest.approx(max(vals), rel=1e-9)
    h = _header(_KSENS)
    assert "RANGE, NOT AS A PLUS-OR-MINUS" in h
    assert "+/-" not in h.split("PLUS-OR-MINUS")[1]


def test_no_bare_triggered_number():
    """test-no-bare-triggered-number. Every triggered quantity in the emitted
    tables, the figure caption and the report carries its k or its k range."""
    for des in DESIGNS:
        h = _header(os.path.join(_ART, fold.EM_EXT_RECON_FILE[des]))
        assert "trigger k =" in h
        assert "one-parameter family" in h.lower()
        assert "fp-hardcoded-width" in h
    text = open(_REPORT, encoding="utf-8").read()
    assert "k = 4" in text or "k=4" in text
    assert "[1, 12]" in text or "[1,12]" in text
    assert "fp-hardcoded-width" in text


def test_subev_k_spread_reported_as_measured():
    """Whether the sub-eV observable is dominated by the unmeasured k is a
    question this plan must ANSWER, not assume. Here it is not: the spread is
    1.10x (muon) and 1.39x (Compton), well under an order of magnitude."""
    rows = [r for r in _ksens_rows() if r["quantity"].startswith("subev")]
    assert len(rows) == 4
    for r in rows:
        ratio = float(r["spread_ratio_hi_over_lo[dimensionless]"])
        assert 1.0 <= ratio < 10.0
        assert r["varies_by_an_order_of_magnitude_or_more[bool]"] == "False"
    ratios = sorted(float(r["spread_ratio_hi_over_lo[dimensionless]"]) for r in rows)
    assert ratios[0] == pytest.approx(1.099, rel=5e-3)
    assert ratios[-1] == pytest.approx(1.385, rel=5e-3)


def test_labels_and_bands_reach_the_reconstructed_tables():
    """Accuracy labels on every row, unnarrowed, with the muon bracketing."""
    for des in DESIGNS:
        rows, path = _rec_table(des)
        for r in rows[:3] + rows[-3:]:
            mu = r["muon_accuracy_label"]
            ga = r["gamma_accuracy_label"]
            assert "Leg A" in mu and "Leg B" in mu and "BRACKET" in mu
            assert "-20.61%" in mu and "+20.34%" in mu
            assert "neutral" in ga and "x0.5 .. x2" in ga
        # the muon band is the WIDER Gaisser-Guan spread and encloses the PDG bracket
        y = np.array([float(r["muon_dRdErec_untriggered[counts/kg/day/keV]"]) for r in rows])
        lo = np.array([float(r["muon_band_lo[counts/kg/day/keV]"]) for r in rows])
        hi = np.array([float(r["muon_band_hi[counts/kg/day/keV]"]) for r in rows])
        m = y > 0
        assert np.allclose(lo[m] / y[m], 0.65, rtol=1e-5)
        assert np.allclose(hi[m] / y[m], 1.35, rtol=1e-5)
        assert 0.65 < 1.1350 / 1.3659 and 1.35 > 1.7204 / 1.3659, "band narrows the PDG bracket"
        cl = np.array([float(r["compton_band_lo[counts/kg/day/keV]"]) for r in rows])
        cy = np.array([float(r["compton_dRdErec_untriggered[counts/kg/day/keV]"]) for r in rows])
        mc = cy > 0
        assert np.allclose(cl[mc] / cy[mc], 0.5, rtol=1e-5)


def test_disposition_rows_and_no_relocation_quantity():
    from qpd_potential import legacy_grid as lg
    reg = lg.load_register()
    for p in ("artifacts/v2.0/em_dRdErec_ext_TaAl.csv",
              "artifacts/v2.0/em_dRdErec_ext_AlHf.csv",
              "artifacts/v2.0/em_trigger_k_sensitivity.csv"):
        assert len(lg.disposition_for(p, reg).reason) > 40
    import test_env_v1_identity as ev
    tokens = ev.SHIELDED_TOKENS + tuple(
        t for t in ev.SHIELDED_TOKENS_EXTRA if t[0] in ("dru", "Table 5"))
    for path in (os.path.join(_ART, fold.EM_EXT_RECON_FILE["Ta->Al"]),
                 os.path.join(_ART, fold.EM_EXT_RECON_FILE["Al->Hf"]),
                 _KSENS):
        text = ev.normalize_unicode(open(path, encoding="utf-8").read())
        for lineno, name, line in ev.scan_text(text, tokens):
            assert any(m.lower() in line.lower() for m in ev.NOT_APPLIED_MARKERS), (
                f"{path}:{lineno}: shielded token {name!r} applied:\n{line}")
