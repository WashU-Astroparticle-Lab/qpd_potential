# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Plan 16-03: the LEE overlay band, SC4's adjudication and the Phase-16 closeout.

Every tolerance is a module constant declared BEFORE any check runs.
"""
import ast
import csv
import os
import re
import subprocess
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from qpd_potential import lee_overlay as lo
from qpd_potential import sb_assembly as sba

import test_env_v1_identity as ev

# --- tolerances, declared first ------------------------------------------- #
CROSSOVER_REL = 1.0e-6           # independent in-test recomputation tolerance
ALPHA_REL = 1.0e-12

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ART = os.path.join(_ROOT, "artifacts", "v2.0")
_PHASE = os.path.join(
    _ROOT, "GPD", "phases",
    "16-s-b-particle-assembly-lee-overlay-and-the-signal-side-conus-check-p-sb")
BAND_CSV = os.path.join(_ART, "lee_overlay_band.csv")
CROSS_CSV = os.path.join(_ART, "lee_crossover_amplitudes.csv")
FIGURE = os.path.join(_ART, "sb_particle_with_lee.pdf")
SB_CSV = os.path.join(_ART, "sb_particle.csv")
REPORT = os.path.join(_PHASE, "16-03-LEE-AND-CLOSEOUT.md")
MODULE = os.path.join(_ROOT, "src", "qpd_potential", "lee_overlay.py")
TESTFILE = os.path.abspath(__file__)

EMITTED = (BAND_CSV, CROSS_CSV, REPORT)


def _rows(path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(r for r in fh if not r.startswith("#")))


def _header(path):
    return "\n".join(l for l in open(path, encoding="utf-8").read().split("\n")
                     if l.startswith("#"))


def _pdf_text(path=FIGURE):
    """Read the PDF's own text stream, rejoining matplotlib's TJ kerning arrays.

    The figure is written with pdf.compression = 0 so that this is a REAL read
    of the file rather than 'the figure exists and the report mentions it'.
    """
    with open(path, "rb") as fh:
        blob = fh.read()
    return "".join(m.decode("latin-1", "replace")
                   for m in re.findall(rb"\(([^()]*)\)", blob))


def _tree():
    return ast.parse(open(MODULE, encoding="utf-8").read())


# --------------------------------------------------------------------------- #
# claim-lee-band-carried                                                        #
# --------------------------------------------------------------------------- #
def test_lee_not_folded():
    """test-lee-not-folded.  AST parse, not grep -- 'response' and 'fold' MUST
    appear in this module's prose, because naming the trap is the point."""
    tree = _tree()
    banned = {"response", "response_matrix", "fold", "trigger"}
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                assert a.name.split(".")[-1] not in banned, a.name
        if isinstance(n, ast.ImportFrom):
            for a in n.names:
                assert a.name not in banned, a.name
            if n.module:
                assert n.module.split(".")[-1] not in banned, n.module
        if isinstance(n, ast.Call):
            f = n.func
            name = f.id if isinstance(f, ast.Name) else (
                f.attr if isinstance(f, ast.Attribute) else "")
            assert name not in banned, name
        if isinstance(n, ast.Attribute):
            assert n.attr not in banned, n.attr
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            assert "response_matrix_" not in n.value, n.value
    # non-vacuity: the evaluation function exists and IS called
    assert any(isinstance(n, ast.FunctionDef) and n.name == "lee_dRdE"
               for n in ast.walk(tree))
    assert any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
               and n.func.id == "lee_dRdE" for n in ast.walk(tree)), \
        "vacuous scan: the LEE evaluation is never called"
    for r in _rows(BAND_CSV) + _rows(CROSS_CSV):
        assert r["not_folded_through_response"] == "True"
        assert r["axis"] == "RECONSTRUCTED"


def test_both_scalings_present():
    """test-both-scalings-present.  Neither edge is ever emitted without the
    other, in any artifact or on the figure."""
    names = {"romani_al_film_area", "chang_bulk_volume"}
    seen = {r["band_edge"] for r in _rows(BAND_CSV)}
    assert seen == names, seen
    # both present for EVERY alpha tag, so no single-scaling emission exists
    for atag in {r["alpha_tag"] for r in _rows(BAND_CSV)}:
        s = {r["band_edge"] for r in _rows(BAND_CSV) if r["alpha_tag"] == atag}
        assert s == names, (atag, s)
    # the extrapolation factors are present as NUMBERS
    for r in _rows(BAND_CSV):
        f = r["extrapolation_factor_written_out"]
        assert any(ch.isdigit() for ch in f), f
    h = _header(BAND_CSV)
    assert "1950" in h and "955" in h and "10300" in h
    assert "118.28" in h or "118.2796" in h
    # on the figure, read out of its own text stream
    txt = _pdf_text()
    for n in names:
        assert n in txt, f"{n} missing from the figure text stream"
    # crossover table places BOTH against every crossover
    for r in _rows(CROSS_CSV):
        if r["is_sc4_as_written"] == "True":
            continue
        for n in names:
            assert r[f"ratio_{n}_over_crossover"] not in ("", None)
            float(r[f"ratio_{n}_over_crossover"])


def test_alpha_derived_not_quoted():
    """alpha is DERIVED from the two RED20 above-ground points inside the test,
    not transcribed from the artifact."""
    (e1, a1), (e2, a2) = lo.RED20_ANCHORS_dru
    mine = float(np.log(a1 / a2) / np.log(e2 / e1))
    assert lo.alpha_from_anchors() == pytest.approx(mine, rel=ALPHA_REL)
    lo_a, hi_a = lo.alpha_range()
    assert lo_a < lo.alpha_from_anchors() < hi_a, (lo_a, hi_a)
    emitted = sorted({float(r["alpha"]) for r in _rows(BAND_CSV)})
    assert emitted == pytest.approx(sorted([lo_a, mine, hi_a]))
    # the ABOVE-GROUND anchors are the ones used, not the /3 underground values
    assert a1 == 1.0e5 and a2 == 1.0e4
    assert "ABOVE-GROUND" in _header(BAND_CSV).upper()


def test_no_lee_prediction_claimed():
    """test-no-lee-prediction-claimed.  Every amplitude row marked unmeasured;
    no LEE-free claim anywhere.  Forbidden phrasings built at runtime."""
    for r in _rows(BAND_CSV):
        assert r["status"] == "UNMEASURED_FOR_THIS_DETECTOR"
    for r in _rows(CROSS_CSV):
        if r["is_sc4_as_written"] == "True":
            continue
        assert r["status"] == "UNMEASURED_FOR_THIS_DETECTOR"
    text = open(REPORT, encoding="utf-8").read()
    assert "no amplitude here is a prediction" in text.lower()
    free = "LEE" + "-free"
    avoids = " ".join(["phonon", "scale", "avoids", "the", "LEE"])
    for p in EMITTED:
        body = open(p, encoding="utf-8").read()
        for i, ln in enumerate(body.split("\n"), 1):
            if free in ln:
                # allowed ONLY inside an explicit refusal of the claim
                ctx = " ".join(body.split("\n")[max(0, i - 3):i + 3]).lower()
                assert ("not claim" in ctx or "does not" in ctx or "no evidence"
                        in ctx or "forbid" in ctx), (p, i, ln[:120])
            assert avoids not in ln.lower(), (p, i, ln[:120])


def test_lee_not_summed_into_headline():
    """test-lee-not-summed-into-headline.  sb_particle.csv is byte-identical to
    its committed state, so S/B_particle was overlaid upon, not modified."""
    out = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "--", "artifacts/v2.0/sb_particle.csv"],
        cwd=_ROOT, capture_output=True, text=True).stdout.strip()
    assert out == "", f"sb_particle.csv was modified by this plan: {out}"
    # no quantity named S/B_particle carries a LEE term
    for r in _rows(SB_CSV):
        assert "lee" not in r["channels_summed"].lower()
    # every LEE-inclusive ratio carries a DIFFERENT name
    src = open(MODULE, encoding="utf-8").read()
    assert "sb_total_with_lee" in src
    assert "def sb_particle" not in src, "this module must not define S/B_particle"


# --------------------------------------------------------------------------- #
# claim-sc4-adjudicated                                                         #
# --------------------------------------------------------------------------- #
def test_sc4_evaluated_as_written():
    """test-sc4-evaluated-as-written.  BOTH determinations recorded with their
    numbers, the criterion quoted verbatim, an explicit verdict EITHER WAY."""
    d = lo.evaluate_sc4_as_written()
    assert d["criterion_verbatim"] == lo.SC4_WORDING
    assert d["verdict"] in ("CONFIRMED", "PARTIALLY CONFIRMED",
                            "SUPERSEDED BY MEASUREMENT", "RESTATEMENT",
                            "INCONCLUSIVE")
    assert isinstance(d["determination_1_answer"], bool)
    assert isinstance(d["determination_2_answer"], bool)
    for k in ("determination_1_numbers", "determination_2_numbers"):
        assert any(ch.isdigit() for ch in d[k]), k
    # determination 1 is a CONTRAST, not a repetition: S/B_total must MOVE
    a = lo.alpha_from_anchors()
    t_small = lo.sb_total_with_lee("Ta->Al", "RoI_10_100eV", 1.0e-6, a)
    t_large = lo.sb_total_with_lee("Ta->Al", "RoI_10_100eV", 1.0e6, a)
    assert t_small > t_large * 10.0, (t_small, t_large)
    # while S/B_particle is identically independent of A
    base = sba.assemble("Ta->Al", "RoI_10_100eV")
    assert t_small == pytest.approx(base["sb_particle_estimates_only"], rel=1e-3)
    # determination 2: the required LEE contribution is NEGATIVE
    need = base["S_counts_kg_day"] - base["B_particle_estimates_only"]
    assert need < 0.0, need
    # recorded in the artifact, verbatim, with the verdict
    h = _header(CROSS_CSV)
    assert lo.SC4_WORDING in h
    assert d["verdict"] in h
    assert "DETERMINATION 1" in h and "DETERMINATION 2" in h
    text = open(REPORT, encoding="utf-8").read()
    assert lo.SC4_WORDING in text
    assert d["verdict"] in text
    assert "FLAGGED FOR THE ORCHESTRATOR" in text.upper()


def test_replacements_named_separately():
    """test-replacements-named-separately.  SC4's phrasing appears on exactly
    the as-written row and nowhere else."""
    rows = _rows(CROSS_CSV)
    asw = [r for r in rows if r["is_sc4_as_written"] == "True"]
    assert len(asw) == 1, len(asw)
    assert asw[0]["quantity_name"] == lo.SC4_WORDING
    others = [r for r in rows if r["is_sc4_as_written"] != "True"]
    assert others
    for r in others:
        assert r["quantity_name"] in ("lee_equals_B_particle", "lee_equals_S")
        assert r["quantity_name"] != lo.SC4_WORDING
    assert {r["quantity_name"] for r in others} == {"lee_equals_B_particle",
                                                    "lee_equals_S"}
    text = open(REPORT, encoding="utf-8").read()
    assert "lee_equals_B_particle" in text and "lee_equals_S" in text
    assert "Pitfall 7" in text


def test_crossovers_computed():
    """test-crossovers-computed.  Every crossover reproduced by an independent
    in-test recomputation to 1e-6 relative."""
    for r in _rows(CROSS_CSV):
        if r["is_sc4_as_written"] == "True":
            continue
        alpha = float(r["alpha"])
        lo_k, hi_k = float(r["band_lo_keV"]), float(r["band_hi_keV"])
        target = float(r["target_counts_kg_day"])
        # independent closed-form integral, written out here
        if abs(alpha - 1.0) < 1e-12:
            unit = lo.E0_keV * np.log(hi_k / lo_k)
        else:
            unit = (lo.E0_keV ** alpha
                    * (hi_k ** (1 - alpha) - lo_k ** (1 - alpha)) / (1 - alpha))
        mine = target / unit
        assert float(r["A_crossover_dru_at_E0"]) == pytest.approx(
            mine, rel=CROSSOVER_REL), r["quantity_name"]
        # the anchor placements are ratios and are present
        for c in ("ratio_romani_al_film_area_over_crossover",
                  "ratio_chang_bulk_volume_over_crossover",
                  "ratio_red20_above_ground_anchor_over_crossover"):
            assert float(r[c]) > 0.0
        if r["band"] == "subeV_le_1eV":
            assert "trigger probability" in r["subev_regime_caveat"].lower()
    # both bands, both designs, both layers covered for the dominance crossover
    dom = [r for r in _rows(CROSS_CSV) if r["quantity_name"] == "lee_equals_B_particle"]
    assert {r["design"] for r in dom} == set(sba.DESIGNS)
    assert {r["band"] for r in dom} == set(sba.BANDS)
    assert {r["denominator_layer"] for r in dom} == {"estimates_only",
                                                     "estimates_plus_bounds"}


def test_scaling_bracket_recorded_either_way():
    """The two scalings' relationship to the RED20 anchor is RECORDED, whichever
    way it comes out -- never quietly widened."""
    br = lo.scalings_bracket_the_anchor()
    assert "strictly_brackets" in br
    h = _header(BAND_CSV)
    assert "BRACKET THE RED20 ANCHOR" in h.upper()
    assert str(br["strictly_brackets"]) in h
    text = open(REPORT, encoding="utf-8").read()
    assert "strictly bracket" in text.lower(), \
        "the bracket question is not addressed on the terminal deliverable"


# --------------------------------------------------------------------------- #
# claim-phase-closeout-16                                                       #
# --------------------------------------------------------------------------- #
VOCAB = ("CONFIRMED", "PARTIALLY CONFIRMED", "SUPERSEDED BY MEASUREMENT",
         "RESTATEMENT", "INCONCLUSIVE")


def test_four_sc_verdicts():
    """test-four-sc-verdicts.  All four ROADMAP Phase 16 criteria verdicted with
    an evidence path each, and nothing narrowed to make one true."""
    text = open(REPORT, encoding="utf-8").read()
    for i in (1, 2, 3, 4):
        assert f"SC{i}" in text, i
    # each SC line carries a verdict from the vocabulary and an evidence path
    sc_lines = [l for l in text.split("\n") if l.strip().startswith("| **SC")]
    assert len(sc_lines) == 4, sc_lines
    for l in sc_lines:
        assert any(v in l for v in VOCAB), l
        assert ("artifacts/v2.0/" in l or "16-0" in l), l
    assert "no window was narrowed" in text.lower()
    assert "no threshold" in text.lower() and "no band" in text.lower()


def test_figure_annotation():
    """test-figure-annotation.  Read OUT of the PDF's own text stream."""
    txt = _pdf_text()
    assert lo.FIGURE_ANNOTATION in txt, "the required annotation is not in the file"
    assert "order_of_magnitude" in txt
    assert "romani_al_film_area" in txt and "chang_bulk_volume" in txt
    assert "RECONSTRUCTED" in txt
    assert "UNMEASURED_FOR_THIS_DETECTOR" in txt
    # the sub-eV boundary is drawn as an IMAGE of a 1 eV deposit, not a literal
    assert "IMAGE" in txt and "0.497240" in txt
    assert "decades" in txt
    # the LEE is a BAND, not a single curve
    assert "BAND" in txt


def test_caveats_reach_terminal_deliverable():
    """test-caveats-reach-terminal-deliverable.  The six-row caveat table from
    16-02 and the numerator-only statement from 16-01, on the TERMINAL report."""
    text = open(REPORT, encoding="utf-8").read()
    for n in ("3.383", "3.598", "4111.8", "209", "584", "35.79",
              "100 meV", "0.590", "48.98", "-20.61", "+20.34",
              "Leg A", "Leg B", "constant-sigma",
              "no external validation of the ratio",
              "NUMERATOR"):
        assert n in text, n
    # no bare signed deviation anywhere in the emitted set
    for p in EMITTED:
        body = ev.normalize_unicode(open(p, encoding="utf-8").read())
        lines = body.split("\n")
        for i, ln in enumerate(lines, 1):
            if "-20.61" not in ln:
                continue
            near = " ".join(lines[max(0, i - 4):i + 4])
            assert "Leg A" in near and "Leg B" in near, (p, i)
    # NUCLEUS and CONUS+ ratios appear only as SHIELDED context, never as targets
    assert "not as targets" in text.lower() or "not targets" in text.lower()
    assert "shielded" in text.lower()
    # the forbidden configuration adjective attaches nowhere
    WORD = "conserv" + "ative"
    ABOUT = ("text scan", "no occurrence", "must not", "phase-8 lock",
             "different and worse", "forbids", "fp-" + WORD + "-label")
    hits = []
    for p in EMITTED + (MODULE, TESTFILE):
        lines = open(p, encoding="utf-8").read().split("\n")
        for i, ln in enumerate(lines, 1):
            if WORD not in ln.lower():
                continue
            ctx = " ".join(lines[max(0, i - 4):i + 3]).lower()
            if any(m in ctx for m in ABOUT):
                continue
            hits.append((os.path.relpath(p, _ROOT), i, ln.strip()[:120]))
    assert hits == [], hits


def test_disposition_rows_16_03():
    """test-disposition-rows-16-03.  The register's own closure test, re-run."""
    from qpd_potential import legacy_grid as lg
    reg = lg.load_register()
    for p in ("artifacts/v2.0/lee_overlay_band.csv",
              "artifacts/v2.0/lee_crossover_amplitudes.csv"):
        assert p in reg, p
        assert reg[p].disposition in lg.DISPOSITION_VALUES
        assert len(reg[p].reason) > 40
    files = subprocess.run(
        ["bash", "-c", "git ls-files | grep -E '\\.(csv|npz)$'"],
        cwd=_ROOT, capture_output=True, text=True).stdout.strip().splitlines()
    assert set(files) == set(reg), (sorted(set(files) - set(reg)),
                                    sorted(set(reg) - set(files)))


def test_no_target_value_lee():
    """No withdrawn expectation and no NUCLEUS/CONUS+ ratio presented as a
    target.  Search strings built at runtime."""
    band_lo, band_hi = "0." + "65", "1." + "2"
    hits = []
    for p in EMITTED + (MODULE,):
        lines = open(p, encoding="utf-8").read().split("\n")
        for i, ln in enumerate(lines, 1):
            if not (band_lo in ln and band_hi in ln):
                continue
            ctx = " ".join(lines[max(0, i - 3):i + 3]).upper()
            if "WITHDRAWN" in ctx:
                continue
            hits.append((os.path.relpath(p, _ROOT), i, ln.strip()[:120]))
    assert hits == [], hits
