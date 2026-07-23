# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Plan 16-02: the channel inventory audit and the S/B_particle assembly.

Every tolerance is a module constant declared BEFORE any check runs.
"""
import ast
import csv
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from qpd_potential import params
from qpd_potential import sb_assembly as sb
from qpd_potential import surface_environment as se

import test_env_v1_identity as ev          # the Phase-9 token guard and normalizer

# --- tolerances, declared first ------------------------------------------- #
HEADLINE_REL = 1.0e-4            # a channel's own headline must reproduce to this
RECOMPUTE_REL = 1.0e-9           # emitted numbers are recomputed, not transcribed
CAPTURE_UNDERSTATEMENT = 1.31    # full band / thermal only
CAPTURE_UNDERSTATEMENT_TOL = 0.01

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ART = os.path.join(_ROOT, "artifacts", "v2.0")
_PHASE = os.path.join(
    _ROOT, "GPD", "phases",
    "16-s-b-particle-assembly-lee-overlay-and-the-signal-side-conus-check-p-sb")
INVENTORY = os.path.join(_ART, "channel_inventory.csv")
OMISSIONS = os.path.join(_ART, "channel_omissions.csv")
SB = os.path.join(_ART, "sb_particle.csv")
LOO = os.path.join(_ART, "sb_leave_one_out.csv")
REPORT = os.path.join(_PHASE, "16-02-SB-ASSEMBLY.md")
MODULE = os.path.join(_ROOT, "src", "qpd_potential", "sb_assembly.py")
TESTFILE = os.path.abspath(__file__)

EMITTED_ARTIFACTS = (INVENTORY, OMISSIONS, SB, LOO)
EMITTED_DOCS = (REPORT,)


def _rows(path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(r for r in fh if not r.startswith("#")))


def _header(path):
    return "\n".join(l for l in open(path, encoding="utf-8").read().split("\n")
                     if l.startswith("#"))


# --------------------------------------------------------------------------- #
# claim-inventory-complete-and-disjoint                                         #
# --------------------------------------------------------------------------- #
def test_integrator_reproduces_headlines():
    """test-integrator-reproduces-headlines.  Validated BEFORE use, on every
    channel, against that channel's own published number."""
    val = sb.validate_integrator()
    assert val, "vacuous: no headline was checked"
    for (chan, band, design), r in val.items():
        assert r["residual_rel"] <= HEADLINE_REL, (chan, band, design, r)
        assert r["reproduced"] is True
    assert sb.blocked_channels() == [], sb.blocked_channels()
    # the residual is recorded per channel in the inventory artifact
    inv = _rows(INVENTORY)
    for r in inv:
        assert r["headline_reproduced"] == "True", r["channel"]
        assert r["reproduction_residual_rel"] != ""
        assert float(r["reproduction_residual_rel"]) <= HEADLINE_REL, r["channel"]
    # and the residual table is in the artifact header
    h = _header(INVENTORY)
    for needle in ("5430.287", "72.9214", "34.2484", "7.4656", "118.73"):
        assert needle in h, needle


def test_no_double_count():
    """test-no-double-count.  Both candidates resolved in writing, by reaction
    channel AND by event time; no two rows share both artifact and mechanism."""
    res = sb.DOUBLE_COUNT_RESOLUTIONS
    assert set(res) == {"neutron_elastic_vs_prompt_capture",
                        "prompt_capture_vs_ge71_ec_line"}
    for name, d in res.items():
        assert len(d["by_reaction"]) > 40, name
        assert len(d["by_event_time"]) > 40, name
        assert d["verdict"] == "NOT A DOUBLE COUNT"
    inv = [r for r in _rows(INVENTORY) if r["design"] == "Ta->Al"]
    seen = {}
    for r in inv:
        key = (r["source_artifact"], r["deposit_mechanism"])
        assert key not in seen, (r["channel"], seen.get(key))
        seen[key] = r["channel"]
    for chan in ("neutron_elastic", "prompt_ngamma_capture", "ge71_ec_M_line"):
        row = [r for r in inv if r["channel"] == chan][0]
        assert "BY REACTION" in row["double_count_resolution"], chan
        assert "BY EVENT TIME" in row["double_count_resolution"], chan
    text = open(REPORT, encoding="utf-8").read()
    assert "MT=2" in text and "MT=102" in text
    assert "11.43" in text


def test_omission_list_nonempty():
    """test-omission-list-nonempty.  Named, non-empty, bias direction on every
    row.  'Nothing missing' for a surface detector is vacuous, not reassuring."""
    rows = _rows(OMISSIONS)
    assert rows, "the omission list is EMPTY"
    names = " ".join(r["omission"] for r in rows)
    for needle in ("muon_induced_neutrons", "muon_induced_secondary_gammas",
                   "cosmogenic_activation", "K_line_X_ray_escape",
                   "above_the_20_MeV_ENDF_ceiling"):
        assert needle in names, needle
    for r in rows:
        assert r["bias_direction"] in se.BIAS_DIRECTIONS, r
        assert len(r["reason"]) > 40, r["omission"]
    # the >20 MeV row carries in-RoI and total-rate bounds SEPARATELY, un-netted
    hi = [r for r in rows if "20_MeV" in r["omission"]][0]
    assert float(hi["in_roi_fraction_hi"]) < 1e-4
    assert float(hi["total_rate_fraction_lo"]) > 1e-2
    assert float(hi["total_rate_fraction_lo"]) / float(hi["in_roi_fraction_hi"]) > 1e3
    # both directions present, i.e. the list is not netted to one sign
    assert {"flatters_SB", "penalizes_SB"} <= {r["bias_direction"] for r in rows}


def test_axis_tag_on_every_operand():
    """test-axis-tag-on-every-operand.  axis == RECONSTRUCTED everywhere, and the
    158.7 eV DEPOSIT energy never used as a reconstructed-axis position."""
    for path in (INVENTORY, SB, LOO):
        for r in _rows(path):
            assert r["axis"] == "RECONSTRUCTED", (path, r)
    inv = _rows(INVENTORY)
    for r in inv:
        for k, v in r.items():
            if v in ("", None):
                continue
            if "158.7" in str(v) and k not in ("deposit_energy_eV_DEPOSITED", "note",
                                               "double_count_resolution",
                                               "reaction_or_source"):
                raise AssertionError(f"158.7 in unlabelled field {k}: {v[:80]}")
    ge = [r for r in inv if r["channel"] == "ge71_ec_M_line"]
    for r in ge:
        assert float(r["deposit_energy_eV_DEPOSITED"]) == 158.7
        assert float(r["erec_image_eV"]) in (65.0, 63.0)
        # the line's RoI rate is the whole of it: 100% in-RoI
        assert float(r["roi_untriggered"]) == pytest.approx(
            float(r["whole_axis_TOTAL_untriggered"]), rel=1e-12)


def test_full_capture_band():
    """test-full-capture-band.  The FULL band enters the sum, not the thermal
    component alone."""
    row = [r for r in _rows(INVENTORY) if r["channel"] == "prompt_ngamma_capture"][0]
    full = float(row["roi_untriggered"])
    therm = float(row["capture_thermal_counts_kg_day"])
    nonth = float(row["capture_nonthermal_counts_kg_day"])
    assert full == pytest.approx(sb.CAPTURE_BOUND_counts_kg_day, rel=1e-12)
    assert full != pytest.approx(therm, rel=1e-3), "the thermal-only value entered the sum"
    assert full == pytest.approx(therm + nonth, rel=2e-4), (full, therm, nonth)
    assert float(row["capture_nonthermal_fraction"]) == pytest.approx(0.2351, abs=5e-4)
    assert float(row["capture_full_over_thermal_only"]) == pytest.approx(
        CAPTURE_UNDERSTATEMENT, abs=CAPTURE_UNDERSTATEMENT_TOL)
    # and the value actually summed IS the full band
    a = sb.assemble("Ta->Al", "RoI_10_100eV")
    b_est = a["B_particle_estimates_only"]
    assert a["B_particle_estimates_plus_bounds"] - b_est == pytest.approx(
        sb.CAPTURE_BOUND_counts_kg_day + sb.GE71_M_SATURATION_counts_kg_day, rel=1e-3)
    text = open(REPORT, encoding="utf-8").read()
    assert "1.31" in text and "23.51" in text and "1034" in text


# --------------------------------------------------------------------------- #
# claim-sb-particle-assembled                                                   #
# --------------------------------------------------------------------------- #
def test_single_baseline_credit_one():
    """test-single-baseline-credit-one.  Exactly 1.0 BY CONSTRUCTION, one baseline."""
    c = se.veto_credit()
    assert isinstance(c, float) and c == 1.0
    assert "BY CONSTRUCTION" in se.veto_credit.__doc__
    creds = {r["veto_credit"] for r in _rows(SB)}
    assert creds == {"1.0"}, creds
    disp = {r["veto_credit_disposition"] for r in _rows(SB)}
    assert disp == {"BY CONSTRUCTION"}, disp
    # exactly ONE baseline: one row per (design, band, layer), no second credit
    keys = [(r["design"], r["band"], r["denominator_layer"]) for r in _rows(SB)]
    assert len(keys) == len(set(keys)) == 2 * 2 * 2, keys
    cfg = {r["configuration"] for r in _rows(SB)}
    assert cfg == {"NUCLEUS's-shielding-absent"}, cfg


def test_numerator_computed_not_substituted():
    """test-numerator-computed-not-substituted.  118.73 is a TOTAL and appears
    only under a TOTAL label."""
    for design, expect in (("Ta->Al", 72.9214), ("Al->Hf", 73.1441)):
        a = sb.assemble(design, "RoI_10_100eV")
        assert a["S_counts_kg_day"] == pytest.approx(expect, rel=HEADLINE_REL)
        assert abs(a["S_counts_kg_day"] - 118.73) > 1.0
    inv = _rows(INVENTORY)
    for r in inv:
        for k, v in r.items():
            if "118.7" in str(v) and "TOTAL" not in k and k not in ("note",):
                raise AssertionError(f"118.73 in a non-TOTAL field {k}: {str(v)[:80]}")
    for r in _rows(SB):
        assert abs(float(r["S_counts_kg_day"]) - 118.73) > 1.0


def test_one_band_definition():
    """test-one-band-definition.  Each band declared ONCE as a module constant
    above every use, and every channel re-integrated on it."""
    tree = ast.parse(open(MODULE, encoding="utf-8").read())
    lineno = {}
    for n in tree.body:
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    lineno[t.id] = n.lineno
        if isinstance(n, ast.FunctionDef):
            lineno[n.name] = n.lineno
    for c in ("ROI_EREC_LO_eV", "ROI_EREC_HI_eV", "SUBEV_EREC_LO_eV",
              "SUBEV_EREC_HI_eV", "BANDS"):
        assert c in lineno, c
        assert lineno[c] < lineno["band_integral"], c
        assert lineno[c] < lineno["assemble"], c
    # exactly one assignment of each band constant
    src = open(MODULE, encoding="utf-8").read()
    for c in ("ROI_EREC_LO_eV", "SUBEV_EREC_HI_eV"):
        assert src.count(f"\n{c} = ") == 1, c
    # every spectral channel is re-integrated here from its own artifact
    assert set(sb.SPECTRAL_SOURCES) >= {"cevns", "neutron", "muon", "compton",
                                        "ge71_ec_M"}
    text = open(REPORT, encoding="utf-8").read()
    assert "E_rec < 1 eV" in text            # the Phase-13 band definition
    assert "Phase 15" in text                # the other one


def test_two_layer_denominator():
    """test-two-layer-denominator.  Both layers present and never collapsed; the
    bounds layer strictly larger; the LOWER BOUND direction stated."""
    rows = _rows(SB)
    layers = {r["denominator_layer"] for r in rows}
    assert layers == {"estimates_only", "estimates_plus_bounds"}, layers
    for design in sb.DESIGNS:
        for band in sb.BANDS:
            sel = {r["denominator_layer"]: r for r in rows
                   if r["design"] == design and r["band"] == band}
            b_est = float(sel["estimates_only"]["B_particle_counts_kg_day"])
            b_all = float(sel["estimates_plus_bounds"]["B_particle_counts_kg_day"])
            assert b_all > b_est, (design, band, b_est, b_all)
            assert float(sel["estimates_plus_bounds"]["S_over_B_particle"]) < \
                float(sel["estimates_only"]["S_over_B_particle"])
            assert "LOWER BOUND" in sel["estimates_plus_bounds"]["layer_direction"]
    text = open(REPORT, encoding="utf-8").read()
    assert "LOWER bound" in text or "LOWER BOUND" in text


def test_leave_one_out_monotone():
    """test-leave-one-out-monotone.  Every in-layer removal of a CONTRIBUTING
    channel strictly increases S/B_particle; a channel contributing exactly zero
    in a band must leave it EXACTLY unchanged."""
    rows = _rows(LOO)
    assert rows
    strict = [r for r in rows if r["operation"] == "REMOVE"
              and r["monotonicity_check"] == "STRICT_INCREASE_REQUIRED"]
    assert strict, "vacuous: no strict-increase row"
    for r in strict:
        assert float(r["ratio_after_over_baseline"]) > 1.0, r
        assert r["strictly_increases"] == "True", r
    noop = [r for r in rows if r["monotonicity_check"] == "EXACT_NO_OP_REQUIRED"]
    for r in noop:
        assert float(r["contribution_in_band_counts_kg_day"]) == 0.0, r
        assert float(r["ratio_after_over_baseline"]) == 1.0, r
    assert all(r["monotonicity_passed"] == "True" for r in rows), \
        [r for r in rows if r["monotonicity_passed"] != "True"]
    # the ranking is emitted, and the neutron channel ranks first everywhere
    for design in sb.DESIGNS:
        for band in sb.BANDS:
            for layer in ("estimates_only", "estimates_plus_bounds"):
                sel = [r for r in rows if r["operation"] == "REMOVE"
                       and r["design"] == design and r["band"] == band
                       and r["denominator_layer"] == layer]
                top = min(sel, key=lambda x: int(x["rank_by_effect"]))
                # rank 1 must be the LARGEST contributor in that layer and band --
                # which is the neutron channel in the RoI and the capture bound in
                # the sub-eV band, so asserting a fixed name would be wrong.
                biggest = max(sel, key=lambda x: float(
                    x["contribution_in_band_counts_kg_day"]))
                assert top["channel"] == biggest["channel"], (design, band, layer, top)
    # and the sweep covers every summed channel
    covered = {r["channel"] for r in rows if r["operation"] == "REMOVE"}
    assert covered == set(sum(sb.summed_channels().values(), ())), covered


def test_inelastic_exclusion_measured():
    """test-inelastic-exclusion-measured.  The exclusion is justified by a
    MEASURED move plus the physical recoil scale, not by assertion."""
    ine = sb.inelastic_sensitivity()
    assert ine["move_ratio"] < 1.0
    assert ine["decades_above_roi"] == pytest.approx(3.356, abs=0.01)
    add = [r for r in _rows(LOO) if r["operation"] == "ADD_EXCLUDED_BOUND"]
    assert add, "the inelastic-addition row is missing"
    for r in add:
        assert float(r["ratio_after_over_baseline"]) < 1.0
    row = [r for r in _rows(INVENTORY) if r["channel"] == "ge_discrete_inelastic"][0]
    assert row["in_sum"] == "False"
    assert row["excluded_reason"] == "EXCLUDED_FROM_SUM"
    assert float(row["inelastic_nuclear_recoil_scale_eV"]) == pytest.approx(2.271606e5)
    h = _header(LOO)
    assert "2.576622" in h and "5.185" in h
    text = open(REPORT, encoding="utf-8").read()
    assert f"{ine['move_percent']:+.3f}" in text or f"{ine['move_percent']:.2f}" in text
    assert "227" in text or "2.271606e+05" in text


def test_trigger_k_sensitivity():
    """test-trigger-k-sensitivity.  The declared range is READ from params, and
    the sensitivity is a numeric column on every sub-eV row."""
    lo, hi = params.TRIGGER_SHARPNESS_RANGE
    subev = [r for r in _rows(SB) if r["band"] == "subeV_le_1eV"]
    assert subev
    for r in subev:
        assert float(r["trigger_k_range_lo"]) == lo
        assert float(r["trigger_k_range_hi"]) == hi
        for c in ("sb_particle_ptrig_identically_one", "trigger_cost_ratio",
                  "measured_k_spread_muon", "measured_k_spread_compton"):
            assert r[c] not in ("", None), c
            float(r[c])
        assert "LOWER BOUND" in r["k_scan_gap"], "the k-scan gap is not named"
    # P_trig == 1 is a real limit, not a copy of the triggered number
    for r in subev:
        assert float(r["sb_particle_ptrig_identically_one"]) != \
            float(r["S_over_B_particle"])


# --------------------------------------------------------------------------- #
# claim-labels-survive-into-the-band                                            #
# --------------------------------------------------------------------------- #
def test_band_not_tighter_than_loosest():
    """test-band-not-tighter-than-loosest.  The assembled label is the loosest
    input label; a percent-level band would FAIL this test."""
    lab = sb.assembled_label()
    assert lab["assembled_label"] == "order_of_magnitude", lab
    assert "order_of_magnitude" in lab["input_labels"]
    blo, bhi = lab["band_multiplier"]
    # the emitted band must be at least this wide, i.e. at least a full decade
    assert bhi / blo >= 10.0 - 1e-9, (blo, bhi)
    for r in _rows(SB):
        assert r["assembled_accuracy_label"] == "order_of_magnitude"
        v = float(r["S_over_B_particle"])
        lo_, hi_ = float(r["S_over_B_particle_band_lo"]), float(r["S_over_B_particle_band_hi"])
        assert lo_ <= v <= hi_
        assert hi_ / lo_ >= 10.0 - 1e-9, r
        # the explicit anti-precision assertion: a percent band would fail here
        assert hi_ / lo_ > 1.25, "a percent-level band was emitted"
    assert sb.LABEL_PROPAGATION_RULE in _header(SB)


CAVEAT_NEEDLES = (
    "3.383", "3.598", "5.0",              # resonance washout vs its own threshold
    "WASH", "over-read",
    "4111.8", "209", "584", "35.79",      # Landau-Vavilov floor
    "100 meV", "0.590", "48.98",          # the least reliable bin
    "-20.61", "+20.34", "Leg A", "Leg B",
    "CaW" + "O", "constant-sigma",        # Phase 13 reversal conditionality
    "no external validation of the ratio",
)


def test_caveats_travel():
    """test-caveats-travel.  Every caveat located by an EXECUTED check, and no
    bare -20.61% anywhere in the emitted files."""
    text = open(REPORT, encoding="utf-8").read()
    missing = [n for n in CAVEAT_NEEDLES if n not in text]
    assert missing == [], missing
    # reuse the Phase-15 four-line window check rather than writing a weaker one
    for p in EMITTED_ARTIFACTS + EMITTED_DOCS:
        body = ev.normalize_unicode(open(p, encoding="utf-8").read())
        lines = body.split("\n")
        for i, ln in enumerate(lines, 1):
            if "-20.61" not in ln:
                continue
            near = " ".join(lines[max(0, i - 4):i + 4])
            assert "Leg A" in near and "Leg B" in near, (
                f"{os.path.relpath(p, _ROOT)}:{i}: bare -20.61% without its "
                f"anchor leg and bracketing")


def test_no_conservative_word():
    """test-no-conservative-word.  Phase-8 lock.  The Phase-9 token guard is
    imported BY IDENTITY, not re-typed."""
    tok, extra = se.shielded_token_guard()
    assert tok is ev.SHIELDED_TOKENS            # BY IDENTITY, not by equality
    assert extra is ev.SHIELDED_TOKENS_EXTRA
    # the forbidden adjective is BUILT AT RUNTIME so this file does not carry it
    WORD = "conserv" + "ative"
    ABOUT_THE_CHECK = ("text scan", "zero occurrence", "no occurrence",
                       "fp-" + WORD + "-label", "must not", "reworded",
                       "phase-8 lock", "different and worse", "forbids")
    hits = []
    for p in EMITTED_ARTIFACTS + EMITTED_DOCS + (MODULE, TESTFILE):
        lines = open(p, encoding="utf-8").read().split("\n")
        for i, ln in enumerate(lines, 1):
            if WORD not in ln.lower():
                continue
            ctx = " ".join(lines[max(0, i - 4):i + 3]).lower()
            if any(m in ctx for m in ABOUT_THE_CHECK):
                continue
            hits.append((os.path.relpath(p, _ROOT), i, ln.strip()[:120]))
    assert hits == [], hits
    for r in _rows(SB):
        assert r["configuration"] == "NUCLEUS's-shielding-absent"
    # zero APPLIED shielded-quantity hits in the module itself
    src = open(MODULE, encoding="utf-8").read()
    applied = [t for t in tok if t[0].lower() in src.lower()
               and "attenuation" in t[0].lower()]
    assert applied == [], applied


def test_named_sb_particle():
    """test-named-sb-particle.  Never the bare unqualified ratio name.  The
    forbidden string is BUILT AT RUNTIME so this file does not carry it."""
    bare = "S" + "/" + "B"
    qualified = bare + "_particle"
    hits = []
    for p in EMITTED_ARTIFACTS + EMITTED_DOCS:
        text = open(p, encoding="utf-8").read()
        for i, ln in enumerate(text.split("\n"), 1):
            j = 0
            while True:
                j = ln.find(bare, j)
                if j < 0:
                    break
                if not ln[j:].startswith(qualified):
                    # a bare occurrence is allowed ONLY when it names someone
                    # else's published ratio, which must be said on the line
                    if not any(w in ln for w in ("CONUS+", "NUCLEUS", "their ",
                                                 "shielded")):
                        hits.append((os.path.relpath(p, _ROOT), i, ln.strip()[:120]))
                j += 1
    assert hits == [], hits
    for r in _rows(SB):
        assert r["observable_S_over_B_particle"] == qualified
    assert sb.OBSERVABLE == qualified


def test_no_target_value():
    """fp-rescued-headline: no withdrawn expectation, no target value.  Search
    strings built at runtime."""
    lo, hi = "0." + "65", "1." + "2"
    hits = []
    for p in EMITTED_ARTIFACTS + EMITTED_DOCS + (MODULE,):
        lines = open(p, encoding="utf-8").read().split("\n")
        for i, ln in enumerate(lines, 1):
            if not (lo in ln and hi in ln):
                continue
            ctx = " ".join(lines[max(0, i - 3):i + 3]).upper()
            if "WITHDRAWN" in ctx:
                continue
            hits.append((os.path.relpath(p, _ROOT), i, ln.strip()[:120]))
    assert hits == [], hits


def test_emitted_numbers_are_recomputed():
    """Nothing in sb_particle.csv is transcribed: every ratio is recomputed here
    from the committed channel artifacts."""
    for r in _rows(SB):
        a = sb.assemble(r["design"], r["band"])
        v = a[f"sb_particle_{r['denominator_layer']}"]
        assert float(r["S_over_B_particle"]) == pytest.approx(v, rel=RECOMPUTE_REL)
        assert float(r["S_counts_kg_day"]) == pytest.approx(
            a["S_counts_kg_day"], rel=RECOMPUTE_REL)
