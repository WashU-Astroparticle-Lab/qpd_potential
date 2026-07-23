# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Plan 15-02: the extended-axis deposit spectra for the two electron-recoil channels.

Executable counterpart of ``src/qpd_potential/em_extended.py`` and the three
artifacts it emits.
"""
import hashlib
import os
import subprocess
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from qpd_potential import compton_deposit as cd
from qpd_potential import em_extended as ee
from qpd_potential import em_recoil as er
from qpd_potential import fold
from qpd_potential import legacy_grid as lg
from qpd_potential import muon_deposit as md

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_REPORT = os.path.join(
    _ROOT, "GPD", "phases",
    "15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em",
    "15-02-EXTENDED-DEPOSIT-SPECTRA.md")

_MU = ee.read_channel_csv(ee.MUON_EXT_CSV)
_CO = ee.read_channel_csv(ee.COMPTON_EXT_CSV)
_TABLES = {"muon": (_MU, ee.MUON_EXT_CSV), "compton": (_CO, ee.COMPTON_EXT_CSV)}


def _header(path):
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("#"):
                break
            out.append(line)
    return "".join(out)


# --------------------------------------------------------------------------- #
# claim-route-decided                                                           #
# --------------------------------------------------------------------------- #
def test_smallN_bit_identity():
    """test-smallN-bit-identity. The RNG stream does not depend on the histogram
    edges, so bins 160..743 reproduce EXACTLY. np.array_equal, not np.allclose."""
    p = ee.bit_identity_probe(n_muon=60_000, n_compton_per_line=8_000)
    assert p["edge_join_array_equal"] is True
    assert p["edge_join_max_abs_diff"] == 0.0
    for k in ("muon_bins_array_equal", "muon_err_array_equal",
              "muon_entries_array_equal", "muon_rate_equal",
              "compton_bins_array_equal", "compton_err_array_equal",
              "compton_entries_array_equal", "compton_rate_equal"):
        assert p[k] is True, f"{k} failed -- the exact-re-drive route is unavailable"
    assert p["all_bit_identical"] is True


def test_frozen_reproduction_recorded():
    """test-frozen-reproduction. The attempt was made and its outcome recorded.

    Here the production extended run's retained bins are compared against the
    frozen CSVs. Both reproduce at the frozen files' own %.6e precision in all
    584 bins, so the frozen v1.0 artifacts ARE regenerable from committed code at
    their recorded settings -- a positive finding, recorded either way.
    """
    for ch, (tab, path) in _TABLES.items():
        frozen = (ee.FROZEN_MUON_CSV if ch == "muon" else ee.FROZEN_COMPTON_CSV)
        rep = ee.frozen_reproduction(tab["dRdEdep"], frozen)
        assert rep["n_bins"] == ee.N_V1_BINS
        assert rep["n_identical_at_6_sig_figs"] == ee.N_V1_BINS, (
            f"{ch}: only {rep['n_identical_at_6_sig_figs']}/584 bins reproduce")
        assert rep["reproduced"] is True
        assert rep["max_rel_diff"] < 1.0e-6
        assert rep["n_frozen_zero_ext_nonzero"] == 0
        assert rep["n_frozen_nonzero_ext_zero"] == 0


def test_route_recorded():
    """test-route-recorded. Both tables name their route AND the evidence."""
    for ch, (tab, path) in _TABLES.items():
        h = _header(path)
        routes = [r for r in ee.ROUTE_VOCABULARY if f"route = {r}" in h]
        assert len(routes) == 1, f"{ch}: route not named exactly once"
        assert routes[0] == "exact_redrive_identical_stream"
        assert "route_selected_by" in h
        assert "np.array_equal" in h and "PASS" in h


# --------------------------------------------------------------------------- #
# claim-extended-deposit-spectra                                                #
# --------------------------------------------------------------------------- #
def test_grid_shape():
    """test-grid-shape. 744 rows, centres to rtol 1e-6, and np.array_equal on the
    edge join -- np.allclose would let the Plan 10-03 5.1e-4 drift through."""
    edges, centres = ee.extended_grid()
    v1 = md.shared_energy_grid("v1.0")
    assert np.array_equal(edges[ee.N_PREPENDED:], v1)
    assert np.abs(edges[ee.N_PREPENDED:] - v1).max() == 0.0
    for ch, (tab, path) in _TABLES.items():
        assert tab["E_dep_keV"].size == ee.N_EXT_BINS, ch
        assert np.allclose(tab["E_dep_keV"], centres, rtol=1e-6), ch


def test_no_frozen_file_written():
    """test-no-frozen-file-written. No data/ file carrying a Phase-9 identity
    assertion was modified, and the Phase-9 identity suite still passes."""
    frozen = ("data/muon_dRdEdep.csv", "data/compton_dRdEdep.csv",
              "data/gamma_lines.csv", "data/ge_incoherent_S.csv",
              "data/ge_xcom_mu.csv")
    for rel in frozen:
        on_disk = hashlib.sha256(open(os.path.join(_ROOT, rel), "rb").read()).hexdigest()
        head = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=_ROOT,
                              capture_output=True, check=True).stdout
        assert on_disk == hashlib.sha256(head).hexdigest(), (
            f"{rel} differs from HEAD -- a frozen artifact has been overwritten")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q",
                        os.path.join(_ROOT, "tests", "test_env_v1_identity.py")],
                       cwd=_ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-3000:]


def test_unbroadened_declared():
    """test-unbroadened-declared. read_broadened_provenance returns exactly False.
    A None return -- a table declaring nothing -- would FAIL: the downstream guard
    treats undeclared as UNKNOWN, not as unbroadened."""
    for ch, (tab, path) in _TABLES.items():
        got = fold.read_broadened_provenance(path)
        assert got is False, f"{ch}: read_broadened_provenance returned {got!r}"


def test_no_exp_minus_2W_and_no_broadening_applied():
    """The Plan 15-01 verdict is enforced, not merely asserted."""
    src = open(os.path.join(_ROOT, "src", "qpd_potential", "em_extended.py")).read()
    # no Debye-Waller factor is COMPUTED anywhere; the only mentions of exp(-2W)
    # are the header text stating that no rate was multiplied by it
    assert "np.exp(-2" not in src and "np.exp(-two" not in src
    assert "ia_broadening" not in src
    for path in (ee.MUON_EXT_CSV, ee.COMPTON_EXT_CSV):
        for line in _header(path).split("\n"):
            if "exp(-2W)" in line:
                assert "no rate" in line or "never" in line or "NOT" in line
    for ch in ("muon", "compton"):
        assert er.ia_verdict(ch).verdict == "does_not_apply"
        with pytest.raises(er.ElectronRecoilBroadeningError):
            er.assert_nuclear_kernel_use(ch, True)


def test_labels_inseparable():
    """test-labels-inseparable. Every row carries all three labels, and the muon
    accuracy label carries the Leg A citation WITH the bracketing disclosure --
    never the bare -20.61% (fp-bare-sign)."""
    for ch, (tab, path) in _TABLES.items():
        n = tab["E_dep_keV"].size
        assert tab["stat_adequacy_label"].size == n
        assert tab["accuracy_label"].size == n
        assert tab["below_validity_floor"].size == n
        assert all(s in ee.STAT_ADEQUACY_VOCABULARY
                   for s in tab["stat_adequacy_label"]), ch
        assert len(set(tab["accuracy_label"])) == 1
        lab = tab["accuracy_label"][0]
        assert len(lab) > 60
        if ch == "muon":
            assert "Leg A" in lab and "Leg B" in lab
            assert "-20.61%" in lab and "+20.34%" in lab
            assert "BRACKET" in lab
            assert "Gaisser-Guan" in lab
        else:
            assert "neutral" in lab and "x0.5 .. x2" in lab
            assert "LABChico" in lab
    # a naive numeric parse of a row stops at the label columns, so a rate cannot
    # be read out of the file without also encountering them
    with open(ee.MUON_EXT_CSV, encoding="utf-8") as fh:
        row = [ln for ln in fh if not ln.startswith("#")][1]
    vals = []
    for tok in row.split(","):
        try:
            vals.append(float(tok))
        except ValueError:
            break
    assert len(vals) == 5, "the trailing labels are not blocking a plain numeric parse"


def test_no_support_not_zero():
    """test-no-support-not-zero. Zero-entry bins are NaN and labelled; a 0.0 in a
    zero-entry bin FAILS -- with ONE narrow, physics-justified exception above the
    Compton kinematic ceiling, where 0.0 is the model's PREDICTION."""
    for ch, (tab, path) in _TABLES.items():
        n = tab["mc_entries"]
        y = tab["dRdEdep"]
        lab = tab["stat_adequacy_label"]
        forb = lab == "kinematically_forbidden"
        if ch == "muon":
            assert not forb.any(), "the exception is Compton-only"
        zero_entry = n == 0
        assert np.all(lab[zero_entry & ~forb] == "no_mc_support")
        assert np.all(~np.isfinite(y[zero_entry & ~forb])), (
            f"{ch}: a zero-entry bin is not NaN")
        assert not np.any((zero_entry & ~forb) & (y == 0.0))
        # and no bin with support is NaN
        assert np.all(np.isfinite(y[n > 0])), f"{ch}: a supported bin is NaN"
        assert np.all(lab[n > 0] != "no_mc_support")
    # the exception is exactly the kinematically forbidden region, nothing else
    top = max(d["E_edge_keV"] for d in ee.closed_form_compton_edges().values())
    edges, _ = ee.extended_grid()
    forb = _CO["stat_adequacy_label"] == "kinematically_forbidden"
    assert np.array_equal(forb, edges[:-1] > top)
    assert np.all(_CO["dRdEdep"][forb] == 0.0)
    assert np.all(_CO["mc_entries"][forb] == 0)


def test_no_nan_to_num_anywhere_in_the_15_02_path():
    """fp-zero-for-no-data at the source level."""
    src = open(os.path.join(_ROOT, "src", "qpd_potential", "em_extended.py")).read()
    calls = [ln for ln in src.split("\n")
             if "nan_to_num" in ln and not ln.lstrip().startswith(("#", "``"))
             and "``nan_to_num``" not in ln]
    assert not calls, f"np.nan_to_num is forbidden in this path: {calls}"


def test_adequacy_label_fails_rather_than_scores_lower():
    """A bin with no support must FAIL the scale, not merely rank low on it."""
    lab = ee.stat_adequacy_label(np.array([0, 1, 9, 50, 5000, 5000]),
                                 np.array([np.nan, 0.9, 0.3, 0.4, 0.3, 0.01]))
    assert list(lab) == ["no_mc_support", "insufficient_mc_support",
                         "insufficient_mc_support", "marginal_mc_support",
                         "marginal_mc_support", "adequate_mc_support"]
    assert ee.MIN_ENTRIES_FOR_ERROR_BAR == 10


def test_validity_floor_flags_come_from_plan_15_01():
    """The flag is read from the Plan 15-01 table, not re-chosen here, and it is
    EMITTED rather than used to delete rows."""
    for ch, (tab, path) in _TABLES.items():
        flags, floor = ee.below_validity_floor_flags(ch, tab["E_dep_keV"])
        assert np.array_equal(flags, tab["below_validity_floor"])
        assert tab["E_dep_keV"].size == ee.N_EXT_BINS          # nothing deleted
    _, mu_floor = ee.below_validity_floor_flags("muon", _MU["E_dep_keV"])
    _, co_floor = ee.below_validity_floor_flags("compton", _CO["E_dep_keV"])
    assert mu_floor == pytest.approx(4111.8165, rel=1e-6)
    assert co_floor == pytest.approx(0.73955, rel=1e-9)
    assert int(_MU["below_validity_floor"].sum()) == 369
    assert int(_CO["below_validity_floor"].sum()) == 70


def test_normalization_factors_are_each_exactly_one():
    """No numeric factor other than exactly 1.0 multiplies either normalization,
    asserted factor by factor rather than on the product."""
    from qpd_potential import surface_environment as se
    for name, val, why in ee.NORMALIZATION_FACTORS:
        assert val == 1.0, f"{name} = {val!r}"
        assert isinstance(val, float) and val.is_integer()
    assert se.veto_credit() == 1.0
    for ch, (tab, path) in _TABLES.items():
        h = _header(path)
        for name, val, why in ee.NORMALIZATION_FACTORS:
            assert f"{name} = 1.0" in h, f"{ch}: {name} not enumerated in the header"


# --------------------------------------------------------------------------- #
# claim-sc1-invariants                                                          #
# --------------------------------------------------------------------------- #
def test_compton_edges():
    """test-compton-edges. Closed-form edges from data/gamma_lines.csv, computed
    independently of the sampler."""
    e = ee.closed_form_compton_edges()
    assert e["K40"]["E_edge_keV"] == pytest.approx(1243.3573, abs=0.5)
    assert e["Bi214"]["E_edge_keV"] == pytest.approx(1541.3115, abs=0.5)
    assert e["Tl208"]["E_edge_keV"] == pytest.approx(2381.7571, abs=0.5)
    # tighter than the contract requires, so a drift would show
    assert e["K40"]["E_edge_keV"] == pytest.approx(1243.3573, abs=1e-3)
    assert e["Bi214"]["E_edge_keV"] == pytest.approx(1541.3115, abs=1e-3)
    assert e["Tl208"]["E_edge_keV"] == pytest.approx(2381.7571, abs=1e-3)


def test_muon_rate():
    """test-muon-rate. ABSOLUTE through-wafer rate in Hz, never per kg."""
    h = _header(ee.MUON_EXT_CSV)
    line = [ln for ln in h.split("\n") if "integral_muon_rate_Hz" in ln][0]
    val = float(line.split("=")[1].split("+/-")[0])
    err = float(line.split("+/-")[1].split()[0])
    assert abs(val - 1.3659) <= 0.0003, f"{val} outside the frozen uncertainty"
    assert err == pytest.approx(0.0003, abs=5e-5)
    assert "ABSOLUTE through-wafer rate in Hz, NOT a per-kg quantity" in h


def test_v1_regression_1pct():
    """test-v1-regression-1pct. Max relative difference below 1% for both
    channels -- and under the exact-re-drive route it should be identically 0 in
    the computation, so a nonzero maximum is itself information."""
    import csv as _csv
    rows = {}
    with open(ee.REGRESSION_CSV, encoding="utf-8") as fh:
        rdr = _csv.DictReader(r for r in fh if not r.startswith("#"))
        for r in rdr:
            rows.setdefault(r["channel"], []).append(float(r["rel_diff[dimensionless]"]))
    assert set(rows) == {"muon", "compton"}
    for ch, rel in rows.items():
        assert len(rel) == ee.N_V1_BINS, ch
        m = max(rel)
        assert m < 1.0e-2, f"{ch}: max rel diff {m} exceeds 1% -- a RE-GRID BUG"
        # the residual is the frozen CSV's own %.6e round-trip, nothing more
        assert m < 1.0e-6, f"{ch}: {m} is larger than a 6-significant-figure round trip"


def test_no_photopeak():
    """test-no-photopeak. Zero non-zero bins with a LOWER EDGE above the highest
    Compton edge, and exactly 0.0 in the bin containing 2614.511 keV."""
    edges, centres = ee.extended_grid()
    top = 2381.7571
    above = edges[:-1] > top
    assert int(above.sum()) > 0
    vals = _CO["dRdEdep"][above]
    assert np.all(np.isfinite(vals)), "a bin above the edge is NaN, not 0.0"
    assert np.all(vals == 0.0), "content above the highest Compton edge"
    i = int(np.searchsorted(edges, 2614.511) - 1)
    assert edges[i] <= 2614.511 < edges[i + 1]
    assert _CO["dRdEdep"][i] == 0.0
    assert _CO["mc_entries"][i] == 0
    # the muon channel has no such ceiling and must not have acquired one
    assert not np.any(_MU["stat_adequacy_label"] == "kinematically_forbidden")


def test_dimensions():
    """test-dimensions. Column headers carry units; mc_err carries the same
    dimension as the quantity it bounds; the Compton energy closure reproduces."""
    for ch, (tab, path) in _TABLES.items():
        hdr = tab["header"]
        assert hdr[0] == "E_dep_keV[keV]"
        assert hdr[1] == "dRdEdep[counts/kg/day/keV]"
        assert hdr[2] == "mc_err[counts/kg/day/keV]"     # same dimension
        assert hdr[3] == "mc_entries[raw count]"
        assert hdr[4] == "rel_mc_err[dimensionless]"
        assert hdr[5] == "below_validity_floor[bool]"
    h = _header(ee.COMPTON_EXT_CSV)
    closure = float([ln for ln in h.split("\n")
                     if "integral dR/dE_dep" in ln][0].split("=")[1].split()[0])
    assert closure == pytest.approx(2.1028e5, rel=1e-3)
    rate = float([ln for ln in h.split("\n")
                  if "total_single_scatter_rate_Hz" in ln][0].split("=")[1].split()[0])
    assert closure == pytest.approx(rate * 86400.0 / 0.1099, rel=2e-3)
    # the four Compton rates are four different numbers, not interchangeable
    for token in ("2.6747e-01", "2.6846e-01", "2.7305e-01", "0.9963"):
        assert token in h, f"missing {token} from the four-way rate distinction"
    # a Hz quantity must not be written per-kg
    assert "ABSOLUTE" in _header(ee.MUON_EXT_CSV)


def test_disposition_rows_exist():
    reg = lg.load_register()
    for p in ("artifacts/v2.0/muon_dRdEdep_ext.csv",
              "artifacts/v2.0/compton_dRdEdep_ext.csv",
              "artifacts/v2.0/em_v1_regression.csv"):
        d = lg.disposition_for(p, reg)
        assert d.disposition in lg.DISPOSITION_VALUES
        assert len(d.reason) > 40


def test_no_relocation_quantity_in_the_emitted_tables():
    """fp-shielded-quantity-leak. Phase-9 token list IMPORTED, not re-typed."""
    import test_env_v1_identity as ev
    tokens = ev.SHIELDED_TOKENS + tuple(
        t for t in ev.SHIELDED_TOKENS_EXTRA if t[0] in ("dru", "Table 5"))
    for path in (ee.MUON_EXT_CSV, ee.COMPTON_EXT_CSV, ee.REGRESSION_CSV,
                 os.path.join(_ROOT, "src", "qpd_potential", "em_extended.py")):
        text = ev.normalize_unicode(open(path, encoding="utf-8").read())
        for lineno, name, line in ev.scan_text(text, tokens):
            assert any(m.lower() in line.lower() for m in ev.NOT_APPLIED_MARKERS), (
                f"{path}:{lineno}: shielded token {name!r} applied:\n{line}")


def test_report_states_the_subev_support_honestly():
    text = open(_REPORT, encoding="utf-8").read()
    low = text.lower()
    for token in ("exact_redrive_identical_stream", "584/584", "no_mc_support",
                  "bounded absence", "kinematically_forbidden",
                  "fp-zero-for-no-data"):
        assert token.lower() in low, f"report missing {token!r}"
