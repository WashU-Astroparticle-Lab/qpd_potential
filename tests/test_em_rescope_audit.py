# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Plan 15-04: the re-scope audit (SC4), the accuracy carry-forward (SC5) and the
in-band dominance re-check.
"""
import csv
import os
import sys

import numpy as np
import pytest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "src"))
sys.path.insert(0, os.path.join(_ROOT, "tests"))

from qpd_potential import (compton_deposit, compton_source, em_extended as ee,
                           em_recoil as er, fold, legacy_grid, muon_deposit,
                           muon_flux, params, surface_environment as se, trigger,
                           wafer_geometry)
import test_env_v1_identity as ev

_ART = os.path.join(_ROOT, "artifacts", "v2.0")
_PHASE = os.path.join(_ROOT, "GPD", "phases",
                      "15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em")

AUDIT_CSV = os.path.join(_ART, "em_rescope_audit.csv")
LABELS_CSV = os.path.join(_ART, "em_accuracy_labels.csv")
DOMINANCE_CSV = os.path.join(_ART, "em_inband_dominance.csv")

#: Documents this phase EMITS. The *-PLAN.md files and 15-CONTEXT.md are INPUTS
#: authored upstream; they quote every retired quantity BECAUSE THEY COMMAND THIS
#: AUDIT, so scanning them would flag the instruction as the violation. The
#: exclusion is recorded in the audit header rather than left silent.
EMITTED_DOCS = ("15-01-BROADENING-APPLICABILITY.md", "15-01-SUMMARY.md",
                "15-02-EXTENDED-DEPOSIT-SPECTRA.md", "15-02-SUMMARY.md",
                "15-03-RECONSTRUCTED-SPECTRA.md", "15-03-SUMMARY.md",
                "15-04-RESCOPE-AUDIT.md", "15-04-SUMMARY.md")

EMITTED_ARTIFACTS = ("em_validity_floors.csv", "muon_dRdEdep_ext.csv",
                     "compton_dRdEdep_ext.csv", "em_v1_regression.csv",
                     "em_dRdErec_ext_TaAl.csv", "em_dRdErec_ext_AlHf.csv",
                     "em_trigger_k_sensitivity.csv", "em_rescope_audit.csv",
                     "em_accuracy_labels.csv", "em_inband_dominance.csv")

#: Local extension to the Phase-9 NOT_APPLIED_MARKERS, justified rather than
#: convenient: ROADMAP SC4 REQUIRES each retired quantity to be enumerated by name
#: as removed, so the audit's own prose necessarily contains the tokens. None of
#: these can let an APPLIED quantity through -- an applied factor appears in an
#: assignment or a multiplication, not in a sentence containing "retired".
LOCAL_MARKERS = ("retired", "removed by the", "zero-overburden", "ZERO overburden",
                 "no relocation quantity", "must not", "cannot be relaxed",
                 "absence of the", "there is no", "enumerat", "prohibition",
                 "sentinel", "by construction")

CLOSURE_ROOTS = (er, ee, fold, muon_deposit, muon_flux, compton_source,
                 compton_deposit, trigger, legacy_grid, wafer_geometry, params, se)


def _scope():
    files = ev.import_closure_files(*CLOSURE_ROOTS)
    arts = [os.path.join(_ART, f) for f in EMITTED_ARTIFACTS]
    docs = [os.path.join(_PHASE, f) for f in EMITTED_DOCS
            if os.path.exists(os.path.join(_PHASE, f))]
    return files, arts, docs


def _rows(path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(r for r in fh if not r.startswith("#")))


def _header(path):
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("#"):
                break
            out.append(line)
    return "".join(out)


# --------------------------------------------------------------------------- #
# claim-rescope-audit                                                           #
# --------------------------------------------------------------------------- #
def test_token_list_is_imported_not_retyped():
    """The single definition site. Two divergent copies of a guard list is how a
    guard silently stops guarding."""
    ST, EX = se.shielded_token_guard()
    assert ST is ev.SHIELDED_TOKENS
    assert EX is ev.SHIELDED_TOKENS_EXTRA
    # the digit-boundary matching that keeps 5.658 A from hitting 5.65 Bq/kg
    import re
    pat = dict(ST)["1.41"]
    assert re.search(pat, "1.41 factor")
    assert not re.search(pat, "1.4150")
    assert not re.search(pat, "1.4585")


def test_token_scan_clean():
    """test-token-scan-clean. Zero shielded-configuration hits outside the named
    allowlist, over the full import closure plus every emitted artifact and
    document."""
    ST, _ = se.shielded_token_guard()
    files, arts, docs = _scope()
    assert len(files) >= 15, files
    for m in ("em_recoil.py", "em_extended.py", "fold.py", "muon_deposit.py",
              "compton_deposit.py", "compton_source.py", "trigger.py",
              "legacy_grid.py", "wafer_geometry.py", "params.py",
              "surface_environment.py", "muon_flux.py"):
        assert any(f.endswith(m) for f in files), f"{m} missing from the closure"
    applied, allow, notapplied = [], [], []
    for p in files + arts + docs:
        text = ev.normalize_unicode(open(p, encoding="utf-8").read())
        lines = text.split("\n")
        # PROSE is scanned in a +/-3-line WINDOW; CODE is scanned line by line.
        # Justified, not loosened: a not-applied declaration in a wrapped Markdown
        # paragraph or a wrapped CSV header block routinely lands on an adjacent
        # line, whereas an APPLIED factor in a .py file is a single assignment or
        # multiplication on one line and cannot hide behind a neighbour.
        prose = not p.endswith(".py")
        for lineno, name, line in ev.scan_text(
                text, ST, skip_fenced=p.endswith(".md")):
            rel = os.path.relpath(p, _ROOT)
            ctx = (" ".join(lines[max(0, lineno - 4):lineno + 3]) if prose else line)
            aw = any(rel.endswith(a[0]) and a[1] in line
                     for a in ev.SHIELDED_ALLOWLIST)
            na = any(m.lower() in ctx.lower()
                     for m in ev.NOT_APPLIED_MARKERS + LOCAL_MARKERS)
            (allow if aw else notapplied if na else applied).append(
                (rel, lineno, name, line))
    assert applied == [], "\n".join(f"{a[0]}:{a[1]} {a[2]}: {a[3]}" for a in applied)
    assert len(allow) == 1, allow
    assert allow[0][0].endswith("compton_source.py")
    assert notapplied, "the enumeration SC4 requires is missing entirely"
    # every allowlist entry carries a written justification a reader can audit
    for _, _, why in [(a[0], a[1], a[2]) for a in ev.SHIELDED_ALLOWLIST]:
        assert len(why) > 80


def test_retired_quantities_named():
    """test-retired-quantities-named. Every retired quantity from the deliverable's
    must_contain block appears as its own row with a disposition and a reason. An
    audit reporting 'no hits' without enumerating what it searched for FAILS."""
    rows = _rows(AUDIT_CSV)
    blob = " | ".join(f"{r['quantity_name']} {r['retired_value']} {r['retired_units']}"
                      for r in rows)
    for token in ("2.92", "m.w.e", "1.41", "5.03", "59.6", "3.28", "5.65",
                  "~50", "buildup", "99.8", "~5", "14", "mcpd"):
        assert token in blob, f"retired quantity {token!r} not enumerated"
    for r in rows:
        assert r["disposition"].strip()
        assert len(r["reason_it_no_longer_applies"]) > 40, r["quantity_name"]
    retired = [r for r in rows
               if r["disposition"] == "removed by the 2026-07-22 re-scope"]
    assert len(retired) == 11, [r["quantity_name"] for r in retired]
    for r in retired:
        assert int(r["applied_hits[count]"]) == 0
        assert int(r["files_scanned[count]"]) >= 30


def test_factors_are_unity():
    """test-factors-are-unity. EACH factor individually 1.0. Asserting only that
    the PRODUCT is 1.0 FAILS: a product can be unity by cancellation."""
    assert len(ee.NORMALIZATION_FACTORS) == 5
    for name, val, why in ee.NORMALIZATION_FACTORS:
        assert val == 1.0, f"{name} = {val!r}"
        assert len(why) > 10
    rows = {r["quantity_name"]: r for r in _rows(AUDIT_CSV)}
    for name, val, why in ee.NORMALIZATION_FACTORS:
        key = f"normalization_factor::{name}"
        assert key in rows, key
        assert float(rows[key]["retired_value"]) == 1.0
        assert "INDIVIDUALLY" in rows[key]["disposition"]
    # end-to-end numeric evidence, independent of the enumeration
    h = _header(os.path.join(_ART, "muon_dRdEdep_ext.csv"))
    rate = float([l for l in h.split("\n") if "integral_muon_rate_Hz" in l][0]
                 .split("=")[1].split("+/-")[0])
    assert abs(rate - 1.3659) <= 3e-4, "a factor other than 1.0 moved the muon rate"
    hc = _header(os.path.join(_ART, "compton_dRdEdep_ext.csv"))
    assert "2.6747e-01" in hc


def test_veto_credit_sentinel():
    """test-veto-credit-sentinel. Exactly 1.0, recorded as BY CONSTRUCTION."""
    assert se.veto_credit() == 1.0
    assert isinstance(se.veto_credit(), float)
    assert "BY CONSTRUCTION" in se.veto_credit.__doc__
    rows = {r["quantity_name"]: r for r in _rows(AUDIT_CSV)}
    r = rows["veto_credit_sentinel"]
    assert float(r["retired_value"]) == 1.0
    assert "BY CONSTRUCTION" in r["disposition"]
    assert "policy default" in r["disposition"] or "policy default" in r["reason_it_no_longer_applies"]
    # no artifact applies a rejection factor of any other value: every audit row
    # whose token is veto_credit either IS the sentinel (value 1.0) or is a RETIRED
    # rejection percentage with an applied-hit count of zero
    for row in _rows(AUDIT_CSV):
        if row["token_searched"] != "veto_credit":
            continue
        if row["quantity_name"] == "veto_credit_sentinel":
            assert float(row["retired_value"]) == 1.0
        else:
            assert row["disposition"] == "removed by the 2026-07-22 re-scope"
            assert int(row["applied_hits[count]"]) == 0
    # and no emitted artifact carries a veto credit other than exactly 1.0
    for f in EMITTED_ARTIFACTS:
        for line in open(os.path.join(_ART, f), encoding="utf-8").read().split("\n"):
            low = line.lower()
            if "veto credit" in low or "veto_credit =" in low:
                assert "1.0" in line, line


def test_no_conservative_word():
    """test-no-conservative-word. Phase-8 lock, milestone-wide. An L2-off,
    shielding-absent configuration is a DIFFERENT AND WORSE configuration, not a
    subset of NUCLEUS's."""
    files, arts, docs = _scope()
    #: The word may appear ONLY in a statement about the prohibition itself. These
    #: markers identify exactly that; none of them could excuse the word being
    #: ATTACHED to the configuration, which would read as "this configuration is a
    #: conservative one" with no scan, no zero-count and no proxy id nearby.
    ABOUT_THE_CHECK = ("text scan", "zero occurrence", "no occurrence",
                       "fp-conservative-label", "must not", "reworded",
                       "phase-8 lock", "different and worse")
    hits = []
    for p in files + arts + docs:
        lines = open(p, encoding="utf-8").read().split("\n")
        for i, ln in enumerate(lines, 1):
            if "conservative" not in ln.lower():
                continue
            ctx = " ".join(lines[max(0, i - 4):i + 3]).lower()
            if any(m in ctx for m in ABOUT_THE_CHECK):
                continue
            hits.append((os.path.relpath(p, _ROOT), i, ln.strip()[:120]))
    assert hits == [], hits


# --------------------------------------------------------------------------- #
# claim-accuracy-carried                                                        #
# --------------------------------------------------------------------------- #
def test_bands_not_narrowed():
    """test-bands-not-narrowed. Identical or wider, never narrower."""
    rows = {r["channel"]: r for r in _rows(LABELS_CSV)}
    assert set(rows) == {"muon", "gamma"}
    g = rows["gamma"]
    assert float(g["band_lo[dimensionless]"]) == 0.5      # the v1.0 factor-2 band
    assert float(g["band_hi[dimensionless]"]) == 2.0
    m = rows["muon"]
    lo, hi = float(m["band_lo[dimensionless]"]), float(m["band_hi[dimensionless]"])
    # the muon band must ENCLOSE the PDG Leg A / Leg B bracket, not narrow it
    pdg_lo, pdg_hi = 1.1350 / 1.3659, 1.7204 / 1.3659
    assert lo <= pdg_lo and hi >= pdg_hi, (lo, hi, pdg_lo, pdg_hi)
    # ... and be at least the 30% Gaisser-Guan spread
    assert lo <= 0.70 and hi >= 1.30, (lo, hi)
    assert "30-35%" in m["underlying_limit"]
    assert "Gaisser-Guan" in m["underlying_limit"]
    # the emitted spectra use the same band, not a tighter one
    for des in ("TaAl", "AlHf"):
        rr = _rows(os.path.join(_ART, f"em_dRdErec_ext_{des}.csv"))
        y = np.array([float(r["muon_dRdErec_untriggered[counts/kg/day/keV]"]) for r in rr])
        bl = np.array([float(r["muon_band_lo[counts/kg/day/keV]"]) for r in rr])
        bh = np.array([float(r["muon_band_hi[counts/kg/day/keV]"]) for r in rr])
        k = y > 0
        assert np.all(bl[k] / y[k] <= lo * (1 + 1e-5))
        assert np.all(bh[k] / y[k] >= hi * (1 - 1e-5))


def test_sign_carries_anchor_leg():
    """test-sign-carries-anchor-leg. EVERY occurrence of -20.61% carries the Leg A
    citation and the Leg A / Leg B bracketing disclosure. A bare -20.61% or a bare
    flatters_SB FAILS."""
    m = {r["channel"]: r for r in _rows(LABELS_CSV)}["muon"]
    assert m["signed_deviation[percent]"].startswith("-")
    assert "Leg A" in m["anchor_leg"]
    assert "Leg B" in m["bracketing_disclosure"]
    assert "+20.34" in m["bracketing_disclosure"]
    assert "BRACKET" in m["bracketing_disclosure"].upper()
    assert m["bias_direction"] == "flatters_SB"
    # over every emitted artifact and document
    files, arts, docs = _scope()
    for p in arts + docs:
        text = ev.normalize_unicode(open(p, encoding="utf-8").read())
        for i, ln in enumerate(text.split("\n"), 1):
            if "-20.61" not in ln:
                continue
            near = " ".join(text.split("\n")[max(0, i - 4):i + 4])
            assert "Leg A" in near and "Leg B" in near, (
                f"{os.path.relpath(p, _ROOT)}:{i}: bare -20.61% without its "
                f"anchor leg and bracketing:\n{ln.strip()[:160]}")


def test_labels_reach_artifacts():
    """test-labels-reach-artifacts. Every Plan 15-02 / 15-03 artifact's per-row
    accuracy label is present and matches em_accuracy_labels.csv."""
    lab = {r["channel"]: r for r in _rows(LABELS_CSV)}
    for f in ("muon_dRdEdep_ext.csv", "compton_dRdEdep_ext.csv"):
        rr = _rows(os.path.join(_ART, f))
        assert len(rr) == 744
        col = [c for c in rr[0] if c == "accuracy_label"][0]
        vals = {r[col] for r in rr}
        assert len(vals) == 1
        v = vals.pop()
        if f.startswith("muon"):
            assert lab["muon"]["bias_direction"] in v
            assert "Leg A" in v and "Leg B" in v
        else:
            assert lab["gamma"]["bias_direction"] in v
    for des in ("TaAl", "AlHf"):
        rr = _rows(os.path.join(_ART, f"em_dRdErec_ext_{des}.csv"))
        assert len(rr) == 161
        for r in (rr[0], rr[-1]):
            assert lab["muon"]["bias_direction"] in r["muon_accuracy_label"]
            assert lab["gamma"]["bias_direction"] in r["gamma_accuracy_label"]
    # no rate can be read out of a Phase-15 artifact without its label
    for f in ("muon_dRdEdep_ext.csv", "em_dRdErec_ext_TaAl.csv",
              "em_inband_dominance.csv"):
        hdr = list(_rows(os.path.join(_ART, f))[0].keys())
        assert any("accuracy_label" in c for c in hdr), f


# --------------------------------------------------------------------------- #
# claim-inband-dominance                                                        #
# --------------------------------------------------------------------------- #
def test_dominance_recomputed():
    """test-dominance-recomputed. Computed from the Plan 15-03 artifacts, not
    quoted from the v1.0 manuscript, and the departure is stated plainly."""
    rows = _rows(DOMINANCE_CSV)
    assert len(rows) == 322                    # 161 bins x 2 designs
    for des in ("Ta->Al", "Al->Hf"):
        sub = [r for r in rows if r["design"] == des]
        assert len(sub) == 161
        E = np.array([float(r["E_rec_keV[keV]"]) for r in sub]) * 1e3
        mu = np.array([float(r["muon_dRdErec[counts/kg/day/keV]"]) for r in sub])
        co = np.array([float(r["compton_dRdErec[counts/kg/day/keV]"]) for r in sub])
        ce = np.array([float(r["cevns_dRdErec_orientation_only[counts/kg/day/keV]"])
                       for r in sub])
        # recomputed, not quoted: the fold reproduces the table
        rm_ = fold.run_em_fold_extended("muon", des,
                                        no_support_policy="exclude_and_record")
        assert np.allclose(mu, rm_["dRdErec"], rtol=1e-5)
        dE = np.diff(rm_["E_rec_edges_eV"]) / 1e3
        roi = (E >= 10.0) & (E <= 100.0)
        assert int(roi.sum()) == 20
        mu_roi, co_roi, ce_roi = (float(np.sum(x[roi] * dE[roi])) for x in (mu, co, ce))
        # THE ORDERING: Compton exceeds muon in the RoI, as v1.0 concluded.
        # The MULTIPLE dropped from the old-axis 4-5.5x to ~3.4x under the unit
        # calibration slope (params.CALIB_SLOPE = 1.0, CONVENTIONS Section E.1):
        # the 10-100 eV_rec RoI now images a 10-100 eV DEPOSIT band instead of the
        # former 20-200 eV, and muon and Compton have different slopes there. The
        # qualitative conclusion (Compton is the larger of the two) is unchanged.
        assert co_roi > mu_roi
        assert 3.0 < co_roi / mu_roi < 4.0, co_roi / mu_roi
        # the CEvNS orientation curve is the Phase-12 one, cross-checked on its total
        assert float(np.sum(ce * dE)) == pytest.approx(118.730, rel=1e-4)
        # and the REFINEMENT: the muon channel is NOT absent from the band
        assert mu_roi > 1.0, "the muon channel has non-negligible in-band content"
        assert 0.05 < mu_roi / ce_roi < 0.20
    text = open(os.path.join(_PHASE, "15-04-RESCOPE-AUDIT.md"), encoding="utf-8").read()
    assert "REFINED" in text or "refinement" in text.lower()
    assert "5430" in text and "5485" in text, "the neutron orientation is missing"
    assert "order_of_magnitude" in text


def test_not_named_signal_over_background():
    """test-not-named-sb. No quantity computed in this phase is named with the
    forbidden ratio name anywhere in an emitted artifact or document."""
    forbidden = "S" + "/" + "B"
    files, arts, docs = _scope()
    hits = []
    for p in arts + docs:
        for i, ln in enumerate(open(p, encoding="utf-8").read().split("\n"), 1):
            if forbidden in ln:
                hits.append((os.path.relpath(p, _ROOT), i, ln.strip()[:120]))
    assert hits == [], hits
    # the dominance table says in its own header what it is NOT
    h = _header(DOMINANCE_CSV)
    assert "ORIENTATION ONLY" in h.upper()
    assert "Phase 16" in h
    assert "NOTHING IN THIS FILE BOUNDS" in h.upper()


def test_labels_on_every_ratio():
    """test-labels-on-every-ratio. Every row carries BOTH contributing channels'
    accuracy labels (fp-precision-inflation)."""
    rows = _rows(DOMINANCE_CSV)
    for r in rows:
        assert "flatters_SB" in r["muon_accuracy_label"]
        assert "Leg A" in r["muon_accuracy_label"]
        assert "Leg B" in r["muon_accuracy_label"]
        assert "neutral" in r["gamma_accuracy_label"]
        assert "x0.5 .. x2" in r["gamma_accuracy_label"]


def test_dimensions():
    """test-dimensions. Units in every header; the veto credit dimensionless and
    exactly 1.0; no signed deviation without its anchor leg."""
    for p in (AUDIT_CSV, LABELS_CSV, DOMINANCE_CSV):
        hdr = list(_rows(p)[0].keys())
        for c in hdr:
            if c in ("channel", "design", "quantity_name", "retired_value",
                     "retired_units", "token_searched", "disposition",
                     "reason_it_no_longer_applies", "accuracy_label",
                     "bias_direction", "anchor_leg", "bracketing_disclosure",
                     "underlying_limit", "artifact_paths", "v1_0_source",
                     "muon_accuracy_label", "gamma_accuracy_label"):
                continue
            assert "[" in c and c.endswith("]"), (p, c)
    lab = _rows(LABELS_CSV)
    for r in lab:
        assert r["signed_deviation[percent]"][0] in "+-", r
        assert r["anchor_leg"].strip(), "a signed deviation with no anchor leg"
    dom = _rows(DOMINANCE_CSV)[0]
    assert "cevns_dRdErec_orientation_only[counts/kg/day/keV]" in dom


def test_disposition_rows_exist():
    reg = legacy_grid.load_register()
    for p in ("artifacts/v2.0/em_rescope_audit.csv",
              "artifacts/v2.0/em_accuracy_labels.csv",
              "artifacts/v2.0/em_inband_dominance.csv"):
        assert len(legacy_grid.disposition_for(p, reg).reason) > 40


def test_audit_states_what_a_token_scan_can_and_cannot_establish():
    """The audit must say which of the two competing readings it has established."""
    h = _header(AUDIT_CSV)
    assert "UNDER A RECOGNISED NAME" in h.upper()
    assert "not a proof" in h.lower() or "NOT establish" in h
    assert "dynamically" in h.lower()
    text = open(os.path.join(_PHASE, "15-04-RESCOPE-AUDIT.md"), encoding="utf-8").read()
    assert "strong\ncheck, not a proof" in text or "strong check, not a proof" in text
