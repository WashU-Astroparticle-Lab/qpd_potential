# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Acceptance tests for the wafer's own muon-rejection handles (Plan 08-02).

Maps to the plan's acceptance-test ids:

    V6  test-normalization-closure   -- the acceptance DENOMINATOR reproduces the
                                        frozen header 1.3659 Hz to within 1%.
    V7  test-acceptance-monotone     -- A_self_direct == 1 at the table floor,
                                        monotone non-increasing, bounded by 1.
    V8  test-multiplicity-identity   -- mult_rejection(1) == 0.0 by IDENTITY
                                        comparison; mult_rejection(18) > 0.
        test-split-reported          -- no API name, CSV column, or CSV row merges
                                        the two acceptances.
        test-induced-zero-named      -- A_SELF_INDUCED is a named 0.0 carrying its
                                        physical argument.
        test-no-transferred-percentage -- no NUCLEUS rejection percentage appears
                                        as a computational value in the module.
        test-counterpoint-recorded   -- the NUCLEUS "very marginal" assessment is
                                        present in both the module and the table.
        test-deadtime-bounded        -- R_mu ~ 0.969 Hz, f_dead ~ 1e-5, labelled a
                                        lower bound, anchor verdict carried.

V6 is the gate: a wrong denominator silently produces a plausible-looking
acceptance, so it is asserted before any acceptance number is trusted.
"""
from __future__ import annotations

import csv
import io
import re
import tokenize
from pathlib import Path

import numpy as np
import pytest

from qpd_potential import wafer_self_veto as wsv

MODULE_PATH = Path(wsv.__file__)
CSV_PATH = wsv.SELF_VETO_CSV

#: Any of these, matched case-insensitively against an identifier or a CSV
#: quantity/column name, would be a merged acceptance (fp-lumped-acceptance).
_MERGED_PATTERNS = (
    r"combined[_\s-]*(muon[_\s-]*veto[_\s-]*)?acceptance",
    r"total[_\s-]*(muon[_\s-]*veto[_\s-]*)?acceptance",
    r"overall[_\s-]*(muon[_\s-]*veto[_\s-]*)?acceptance",
    r"lumped[_\s-]*(muon[_\s-]*veto[_\s-]*)?acceptance",
    r"a_self\b(?!_direct|_induced)",
    r"a_self_total",
    r"a_self_combined",
    r"muon_veto_acceptance",
)


# --------------------------------------------------------------------------- #
# Helpers                                                                      #
# --------------------------------------------------------------------------- #
def _module_source() -> str:
    return MODULE_PATH.read_text()


def _module_number_literals() -> list[float]:
    """Every NUMBER token in the module, i.e. every literal used as a VALUE.

    Tokenizing is stricter and less brittle than a raw grep: a number inside a
    docstring or a comment is a STRING / COMMENT token and is correctly excluded,
    while any number the interpreter would actually evaluate is a NUMBER token
    and is caught. This is precisely the "used as a computational value"
    distinction the plan's proxy test asks for.
    """
    out: list[float] = []
    with open(MODULE_PATH, "rb") as fh:
        for tok in tokenize.tokenize(fh.readline):
            if tok.type == tokenize.NUMBER:
                try:
                    out.append(float(tok.string.replace("_", "")))
                except ValueError:  # complex literal etc. -- none expected
                    pass
    return out


def _read_table() -> tuple[list[str], list[str], list[dict[str, str]]]:
    """Return (header comment lines, column names, rows) of the emitted CSV."""
    header, body = [], []
    with open(CSV_PATH) as fh:
        for line in fh:
            (header if line.startswith("#") else body).append(line)
    reader = csv.DictReader(io.StringIO("".join(body)))
    return header, list(reader.fieldnames or []), list(reader)


@pytest.fixture(scope="module")
def table():
    if not CSV_PATH.exists():
        wsv.emit_table()
    return _read_table()


# --------------------------------------------------------------------------- #
# V6 -- test-normalization-closure (the gate)                                  #
# --------------------------------------------------------------------------- #
def test_v6_normalization_closure_reproduces_frozen_rate():
    """The acceptance DENOMINATOR must reproduce the frozen header 1.3659 Hz.

    int dR/dE_dep dE [cts/kg/day] x 0.1099 kg / 86400 s = Hz. A failure here is a
    normalization error in the denominator and BLOCKS every acceptance number in
    this plan; it is never rescaled away.
    """
    closure = wsv.integral_rate_Hz()
    header_rate = wsv.frozen_header_rate_Hz()
    assert header_rate == pytest.approx(1.3659, abs=1e-4), (
        "frozen header rate changed -- the benchmark itself moved"
    )
    rel = abs(closure / header_rate - 1.0)
    assert rel < 0.01, (
        f"denominator closure {closure:.6f} Hz vs header {header_rate:.4f} Hz "
        f"= {100 * rel:.3f}% -- NORMALIZATION ERROR in the acceptance denominator"
    )


def test_v6_conversion_constants_are_the_locked_ones():
    """m_wafer comes from wafer_geometry (CONVENTIONS D), not restated by hand."""
    from qpd_potential import wafer_geometry as wg

    assert wsv.M_WAFER_KG is wg.MASS_KG or wsv.M_WAFER_KG == wg.MASS_KG
    assert wsv.M_WAFER_KG == pytest.approx(0.1099, abs=5e-5)
    assert wsv.SECONDS_PER_DAY == 86_400.0


def test_v6_uses_the_correct_frozen_paths_not_the_stale_ones():
    """08-RESEARCH Pitfall 9: the 04-01-SUMMARY paths do not exist."""
    src = _module_source()
    assert wsv.MUON_CSV.name == "muon_dRdEdep.csv"
    assert wsv.MUON_CSV.exists()
    assert "data/muon/" not in src.replace("data/muon/muon_dep_spectrum.csv", "")
    assert not (wsv.MUON_CSV.parent / "muon").exists(), (
        "a data/muon/ directory now exists -- re-check which artifact is frozen"
    )
    # Only the explicit does-not-exist warnings may mention the stale paths.
    for stale in ("data/muon/muon_dep_spectrum.csv", "src/muon/deposited_spectrum.py"):
        for line_no, line in enumerate(src.splitlines(), start=1):
            if stale in line:
                window = "\n".join(src.splitlines()[max(0, line_no - 6):line_no + 6])
                assert "DO NOT EXIST" in window, (
                    f"{stale} mentioned at line {line_no} without the "
                    "does-not-exist warning"
                )


# --------------------------------------------------------------------------- #
# V7 -- test-acceptance-monotone                                               #
# --------------------------------------------------------------------------- #
def test_v7_acceptance_is_exactly_one_at_the_table_floor():
    floor = wsv.table_floor_keV()
    assert floor == pytest.approx(1.014497e-02, rel=1e-9)
    assert wsv.a_self_direct(floor) == 1.0
    # 10 eV sits marginally BELOW the floor -> still exactly 1, by construction,
    # and explicitly not an extrapolation below the artifact's support.
    assert wsv.a_self_direct(0.010) == 1.0


def test_v7_acceptance_is_monotone_non_increasing_and_bounded():
    floor = wsv.table_floor_keV()
    sweep = np.geomspace(floor, 100.0, 400)
    vals = np.array([wsv.a_self_direct(e) for e in sweep])
    assert np.all(vals <= 1.0), f"acceptance exceeds 1: max {vals.max()!r}"
    assert np.all(vals >= 0.0)
    diffs = np.diff(vals)
    assert np.all(diffs <= 1e-15), (
        f"acceptance not monotone non-increasing: max increase {diffs.max():.3e}"
    )


def test_v7_reported_thresholds_are_each_approximately_one():
    """1.2323 MeV vertical MPV against 10 eV - 100 keV thresholds.

    Materially below 1 at 1 keV would indicate a units error (disconfirming
    observation named in the plan's uncertainty markers).
    """
    a10ev = wsv.a_self_direct(0.010)
    a1kev = wsv.a_self_direct(1.0)
    a100kev = wsv.a_self_direct(100.0)
    assert a10ev == 1.0
    assert a1kev == pytest.approx(0.999971887382, rel=1e-9)
    assert a100kev == pytest.approx(0.997858048250, rel=1e-9)
    assert a1kev > 0.999, "materially below 1 at 1 keV -- suspect a units error"
    assert a100kev > 0.99
    assert a10ev >= a1kev >= a100kev


def test_v7_acceptance_is_dimensionless_ratio_insensitive_to_normalization():
    """Scaling the spectrum by any constant leaves the acceptance unchanged.

    This is the machine-checkable form of the claim that A_self_direct does NOT
    inherit the 1.41-attenuation caveat that f_dead carries.
    """
    e_grid, rate = wsv.frozen_spectrum()
    e_cut = 100.0
    idx = int(np.searchsorted(e_grid, e_cut, side="right"))
    r_cut = float(np.interp(e_cut, e_grid, rate))

    def acc(scale: float) -> float:
        scaled = rate * scale
        num = np.trapz(
            np.concatenate(([r_cut * scale], scaled[idx:])),
            np.concatenate(([e_cut], e_grid[idx:])),
        )
        return float(num / np.trapz(scaled, e_grid))

    assert acc(1.0) == pytest.approx(acc(1.0 / 1.41), rel=1e-12)
    assert acc(1.0) == pytest.approx(wsv.a_self_direct(e_cut), rel=1e-12)


def test_v7_out_of_range_thresholds_behave():
    assert wsv.a_self_direct(wsv.table_ceiling_keV()) == 0.0
    assert wsv.a_self_direct(1e9) == 0.0
    with pytest.raises(ValueError):
        wsv.a_self_direct(-1.0)


# --------------------------------------------------------------------------- #
# V8 -- test-multiplicity-identity                                             #
# --------------------------------------------------------------------------- #
def test_v8_multiplicity_rejection_is_exactly_zero_for_one_channel():
    """Identity comparison, not a tolerance. N = 1 -> the cut removes nothing."""
    assert wsv.mult_rejection(1) == 0.0
    assert isinstance(wsv.mult_rejection(1), float)


def test_v8_multiplicity_identity_does_not_depend_on_the_occupancy_model():
    """The N = 1 zero is a counting identity, not a model output.

    The binomial-conditional model itself returns 0 at N = 1 for ANY p_hit, so
    the identity survives every choice of the illustrative occupancy.
    """
    for p in (0.001, 0.05, 0.3, 0.9, 1.0):
        assert wsv.mult_rejection(1, p_hit=p) == 0.0


def test_v8_multiplicity_rejection_is_positive_for_eighteen_channels():
    """Contrast only. The VALUE is model-dependent and is not published."""
    assert wsv.N_CHANNELS_NUCLEUS_CHOOZ == 18
    val = wsv.mult_rejection(18)
    assert val > 0.0
    assert 0.0 < val < 1.0
    for p in (0.01, 0.05, 0.2, 0.5):
        assert wsv.mult_rejection(18, p_hit=p) > 0.0


def test_v8_multiplicity_rejection_rejects_bad_input():
    with pytest.raises(ValueError):
        wsv.mult_rejection(0)
    with pytest.raises(ValueError):
        wsv.mult_rejection(18, p_hit=0.0)
    with pytest.raises(ValueError):
        wsv.mult_rejection(18, p_hit=1.5)


def test_v8_no_bare_n18_value_in_the_data_table(table):
    """A number here would read as a NUCLEUS-derived efficiency. It is not one."""
    _, _, rows = table
    for row in rows:
        assert "18" not in row["quantity"], (
            f"row {row['quantity']!r} looks like an N = 18 multiplicity entry"
        )
        assert not re.search(r"eps_mult.*(?<!_)N?18", row["quantity"])
    quantities = {r["quantity"] for r in rows}
    assert "eps_mult_N1" in quantities
    # If a future edit adds an N = 18 row it must carry the illustrative label.
    for row in rows:
        if "18" in row["quantity"] or "18" in row["definition"]:
            caveat = row["caveat"].lower()
            assert "illustrative" in caveat and "model-dependent" in caveat
            assert "not a nucleus" in caveat


def test_v8_multiplicity_docstring_carries_the_quotes_and_the_model():
    doc = wsv.mult_rejection.__doc__ or ""
    flat = " ".join(doc.split())
    assert "one and only one of the target detectors" in flat, "08-01 B.2 quote"
    assert "very marginal" in flat, "08-01 B.7 counterpoint"
    assert "B.2" in doc and "B.7" in doc, "evidence-block entry references"
    assert "OCCUPANCY MODEL" in doc
    assert "independent per-channel firing" in doc


# --------------------------------------------------------------------------- #
# test-induced-zero-named                                                      #
# --------------------------------------------------------------------------- #
def test_induced_acceptance_is_a_named_exact_zero():
    assert hasattr(wsv, "A_SELF_INDUCED")
    assert wsv.A_SELF_INDUCED == 0.0
    assert isinstance(wsv.A_SELF_INDUCED, float)


def test_induced_acceptance_docstring_carries_the_physical_argument():
    """The value alone is not the deliverable; the argument is."""
    src = _module_source()
    block = src.split("A_SELF_INDUCED = 0.0", 1)[1].split('"""')[1]
    lower = block.lower()
    # muon-induced vs through-going distinction, sourced to the evidence block
    assert "muon-induced" in lower
    assert "B.9" in block, "the >99.8% sentence must be cited by its 08-01 entry"
    assert "tagging efficiency" in lower
    assert "not applied" in lower
    # the physical mechanism, not just an assertion
    assert "parent muon" in lower
    assert "lead" in lower or "pb" in lower
    # the honesty caveat: zero is a floor, not an impossibility proof
    assert "floor" in lower
    assert "impossibility proof" in lower


def test_induced_acceptance_row_states_the_argument(table):
    _, _, rows = table
    row = next(r for r in rows if r["quantity"] == "A_self_induced")
    assert float(row["value"]) == 0.0
    assert "muon-INDUCED" in row["source"]
    assert "NOT applied" in row["source"]
    assert "B.9" in row["source"]
    assert "floor" in row["caveat"].lower()


# --------------------------------------------------------------------------- #
# test-no-transferred-percentage                                               #
# --------------------------------------------------------------------------- #
def test_no_nucleus_rejection_percentage_is_used_as_a_value():
    """Neither 99.8 nor 0.998 may be evaluated as a number by this module."""
    numbers = _module_number_literals()
    for forbidden in (99.8, 0.998):
        assert not any(abs(n - forbidden) < 1e-12 for n in numbers), (
            f"{forbidden} appears as a NUMBER literal, i.e. as a computational "
            "value -- fp-veto-credit-transfer"
        )


def test_any_textual_percentage_is_inside_a_docstring_marked_not_applied():
    src = _module_source()
    for token in ("99.8", "0.998"):
        for line_no, line in enumerate(src.splitlines(), start=1):
            if token not in line:
                continue
            window = "\n".join(src.splitlines()[max(0, line_no - 25):line_no + 25])
            assert "NOT applied" in window or "not applied" in window, (
                f"{token} at line {line_no} is not accompanied by an explicit "
                "'not applied' statement"
            )


def test_no_bare_factor_five_rejection_constant():
    """No module-level constant is a transferred rejection factor."""
    for name, value in vars(wsv).items():
        if name.startswith("_") or not isinstance(value, (int, float)):
            continue
        assert not re.search(r"rejection|efficiency|factor", name, re.I) or (
            name == "MU_ATTENUATION_VNS"
        ), f"{name} = {value} looks like a transferred rejection constant"
    numbers = _module_number_literals()
    # the only integer 18 permitted is the channel COUNT (a geometry fact)
    assert numbers.count(18.0) <= 1
    assert wsv.N_CHANNELS_NUCLEUS_CHOOZ == 18


def test_no_nucleus_percentage_in_the_data_table():
    text = CSV_PATH.read_text()
    assert "99.8" not in text
    assert "0.998" not in text


# --------------------------------------------------------------------------- #
# test-split-reported                                                          #
# --------------------------------------------------------------------------- #
def test_module_api_has_no_merged_acceptance_name():
    """Structural check on identifiers, not on prose.

    The module's own prose *describes* the prohibition, so a raw text grep would
    flag the honesty statement itself. What matters is that no callable, no
    constant, and no table column named as a merged acceptance exists.
    """
    names = [n for n in vars(wsv) if not n.startswith("__")]
    for name in names:
        for pat in _MERGED_PATTERNS:
            assert not re.search(pat, name, re.I), (
                f"module attribute {name!r} reads as a merged acceptance"
            )
    assert "a_self_direct" in names
    assert "A_SELF_INDUCED" in names


def test_data_table_keeps_the_two_acceptances_on_separate_rows(table):
    _, columns, rows = table
    quantities = [r["quantity"] for r in rows]
    direct = [q for q in quantities if q.startswith("A_self_direct")]
    assert len(direct) == 3, f"expected 3 A_self_direct rows, got {direct}"
    assert "A_self_induced" in quantities
    assert len(set(quantities)) == len(quantities), "duplicate quantity names"
    for name in columns + quantities:
        for pat in _MERGED_PATTERNS:
            assert not re.search(pat, name, re.I), (
                f"{name!r} reads as a merged/total acceptance"
            )


def test_every_data_row_carries_a_source_and_a_caveat(table):
    _, columns, rows = table
    assert columns == ["quantity", "value", "units", "definition", "source", "caveat"]
    for row in rows:
        assert row["quantity"]
        assert row["value"]
        assert row["units"] in ("dimensionless", "Hz")
        assert len(row["definition"]) > 20, row["quantity"]
        assert len(row["source"]) > 20, row["quantity"]
        assert len(row["caveat"]) > 20, row["quantity"]
        float(row["value"])  # parses as a number


def test_data_table_values_match_the_module(table):
    _, _, rows = table
    by_q = {r["quantity"]: float(r["value"]) for r in rows}
    assert by_q["A_self_direct_10eV"] == pytest.approx(wsv.a_self_direct(0.010))
    assert by_q["A_self_direct_1keV"] == pytest.approx(wsv.a_self_direct(1.0))
    assert by_q["A_self_direct_100keV"] == pytest.approx(wsv.a_self_direct(100.0))
    assert by_q["A_self_induced"] == wsv.A_SELF_INDUCED
    assert by_q["eps_mult_N1"] == wsv.mult_rejection(1)
    assert by_q["R_mu_2.92mwe"] == pytest.approx(wsv.r_mu_underground_Hz(), rel=1e-6)
    assert by_q["f_dead_tau40us"] == pytest.approx(
        wsv.f_dead(wsv.TAU_DEAD_RESOLVE_S), rel=1e-6
    )
    assert by_q["f_dead_tau20us"] == pytest.approx(
        wsv.f_dead(wsv.TAU_DEAD_SAMPLE_S), rel=1e-6
    )


def test_emit_table_is_reproducible(tmp_path):
    out = wsv.emit_table(tmp_path / "wafer_self_veto.csv")
    assert out.read_text() == CSV_PATH.read_text(), (
        "committed data/wafer_self_veto.csv is stale -- re-run "
        "python -m qpd_potential.wafer_self_veto"
    )


# --------------------------------------------------------------------------- #
# test-deadtime-bounded                                                        #
# --------------------------------------------------------------------------- #
def test_deadtime_rate_and_fraction_are_dimensionally_sane():
    r_mu = wsv.r_mu_underground_Hz()
    assert r_mu == pytest.approx(0.969, abs=5e-4), f"R_mu = {r_mu}"
    assert r_mu == pytest.approx(wsv.frozen_header_rate_Hz() / 1.41, rel=1e-12)
    for tau in (wsv.TAU_DEAD_RESOLVE_S, wsv.TAU_DEAD_SAMPLE_S):
        f = wsv.f_dead(tau)
        assert f == pytest.approx(r_mu * tau, rel=1e-12)  # Hz x s -> dimensionless
        assert 1e-6 < f < 1e-4, f"f_dead({tau}) = {f} is not of order 1e-5"
    assert wsv.f_dead(wsv.TAU_DEAD_RESOLVE_S) == pytest.approx(3.874894e-05, rel=1e-6)
    assert wsv.f_dead(wsv.TAU_DEAD_SAMPLE_S) == pytest.approx(1.937447e-05, rel=1e-6)
    assert wsv.TAU_DEAD_RESOLVE_S == 40e-6  # CONVENTIONS F, 25 kHz Nyquist
    assert wsv.TAU_DEAD_SAMPLE_S == 20e-6   # CONVENTIONS F, 50 kHz sampling


def test_deadtime_is_labelled_a_lower_bound_with_both_reasons():
    doc = wsv.f_dead.__doc__ or ""
    assert "LOWER BOUND" in doc
    assert "integral-flux factor" in doc          # reason 1
    assert "saturates the readout" in doc         # reason 2
    assert "Phase 15" in doc
    # and the ratio-insensitivity of a_self_direct is stated SEPARATELY
    assert "does NOT inherit this caveat" in doc
    assert "RATIO-INSENSITIVITY" in (wsv.a_self_direct.__doc__ or "")


def test_carried_anchor_verdict_is_reproduced_with_the_number(table):
    """No row may use the 1.41 / 2.92 anchors without Plan 08-01's verdict."""
    _, _, rows = table
    verdict_bits = ("verified verbatim", "2509.03559v1", "Sect. 4.1")
    anchored = [r for r in rows if "1.41" in r["source"] or "2.92" in r["source"]]
    assert anchored, "no row carries the attenuation/overburden anchor"
    for row in anchored:
        for bit in verdict_bits:
            assert bit in row["source"], (
                f"row {row['quantity']!r} uses a carried anchor without "
                f"Plan 08-01's verdict fragment {bit!r}"
            )
    r_mu_row = next(r for r in rows if r["quantity"] == "R_mu_2.92mwe")
    assert "E.1.1" in r_mu_row["source"] and "E.1.2" in r_mu_row["source"]
    # the same verdict appears in the f_dead docstring
    doc = wsv.f_dead.__doc__ or ""
    for bit in verdict_bits:
        assert bit in doc


def test_deadtime_rows_are_labelled_lower_bounds(table):
    _, _, rows = table
    for row in rows:
        if row["quantity"].startswith("f_dead"):
            assert "LOWER BOUND" in row["caveat"].upper()
            assert "RESOLVING TIME" in row["caveat"].upper()
            assert "integral-flux factor" in row["caveat"]


# --------------------------------------------------------------------------- #
# test-counterpoint-recorded                                                   #
# --------------------------------------------------------------------------- #
_MARGINAL_QUOTE = (
    "the benefit of applying all vetoes, i.e. (i) using the IV and\n"
    "        (ii) requesting only one cryogenic detector hit in addition to the MV\n"
    "        and COV anti-coincidence selection criteria, is very marginal."
)


def test_counterpoint_is_present_in_the_module_docstring():
    doc = wsv.__doc__ or ""
    assert "very marginal" in doc
    assert "B.7" in doc, "quote must be referenced to its 08-01 evidence entry"
    assert "5.2.1" in doc
    lower = doc.lower()
    assert "cost of the wafer's" in lower or "costs little" in lower
    assert "against this project's framing" in lower or "cuts *against*" in lower


def test_counterpoint_is_present_in_the_data_table_header(table):
    header, _, _ = table
    text = "".join(header)
    assert "very" in text and "marginal" in text
    assert "B.7" in text
    assert "5.2.1" in text
    assert "SMALL" in text, "the reduced absolute cost must be stated plainly"
    assert "weakens this project's" in text


def test_counterpoint_quote_matches_the_evidence_block_verbatim():
    """Guard against paraphrase drift away from 08-01-SOURCE-EVIDENCE.md B.7."""
    evidence = (
        Path(__file__).resolve().parents[1]
        / "GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-01-SOURCE-EVIDENCE.md"
    )
    if not evidence.exists():
        pytest.skip("evidence block not present in this checkout")
    ref = (
        "Finally, the benefit of applying all vetoes, i.e. (i) using the IV and "
        "(ii) requesting only one cryogenic detector hit in addition to the MV "
        "and COV anti-coincidence selection criteria, is very marginal."
    )
    assert ref in " ".join(evidence.read_text().split())
    for text in (wsv.__doc__ or "", CSV_PATH.read_text()):
        flat = " ".join(text.replace("#", " ").split())
        assert ref in flat, "quote drifted from the 08-01 evidence block"


def test_selection_quote_matches_the_evidence_block_verbatim():
    evidence = (
        Path(__file__).resolve().parents[1]
        / "GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-01-SOURCE-EVIDENCE.md"
    )
    if not evidence.exists():
        pytest.skip("evidence block not present in this checkout")
    ref = (
        "the identification of a CE \\nu NS-like event must meet the combination "
        "of all possible anti-coincidence selection criteria, i.e. having (i) no "
        "hits in any of the veto detectors and (ii) a hit in one and only one of "
        "the target detectors."
    )
    assert ref in " ".join(evidence.read_text().split())
    # The module renders \nu as "nu" for readability; compare the rest verbatim.
    flat = " ".join((wsv.mult_rejection.__doc__ or "").split())
    assert ref.replace("CE \\nu NS", "CEnuNS") in flat


# --------------------------------------------------------------------------- #
# Uncredited spatial handle (08-RESEARCH Pitfall 10)                           #
# --------------------------------------------------------------------------- #
def test_qpd_spatial_handle_is_named_and_left_uncredited():
    doc = wsv.__doc__ or ""
    assert "10,300" in doc
    lower = doc.lower()
    assert "not credited anywhere in v2.0" in lower
    assert "fp-spatial-handle-credit" in doc
    header = "".join(_read_table()[0]).lower()
    assert "10,300" in header
    assert "not credited anywhere in v2.0" in header


def test_module_docstring_asserts_no_applied_nucleus_percentage():
    doc = wsv.__doc__ or ""
    assert "NO NUCLEUS REJECTION PERCENTAGE IS APPLIED AS A COMPUTATIONAL VALUE" in doc
