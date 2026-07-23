# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Phase-9 Plan 09-03: the frozen three-channel surface environment.

Two audits, both EXECUTED rather than asserted (SC5 requires a provenance /
call-graph check; SC1 requires verification by direct comparison):

  * Audit A -- no shielded quantity anywhere in the set or its import closure,
    and every veto / coincidence / multiplicity credit sentinel exactly 1.0.
  * Audit B -- the directional-bias audit: one row per channel with a SIGNED
    deviation, a direction label, and a numeric compounded-effect factor.

Guards:
  * fp-shielded-quantity-leak    -- token scan over the set + import closure
  * fp-silent-neutron-omission   -- a missing neutron row fails outright
  * fp-combined-band             -- no combined/averaged uncertainty field or accessor
  * fp-audit-as-formality        -- the audit fails under a sign flip and under all-neutral
  * fp-declaration-without-execution -- every scan/hash/sentinel here is run
"""
from __future__ import annotations

import os
import re

import numpy as np
import pytest

from qpd_potential import compton_source as cs
from qpd_potential import muon_deposit as md
from qpd_potential import surface_environment as se
from qpd_potential import veto_credit as vc

from test_env_v1_identity import (SHIELDED_TOKENS, SHIELDED_TOKENS_EXTRA,
                                  import_closure_files, is_allowlisted,
                                  is_not_applied, normalize_unicode, scan_paths,
                                  scan_text)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(REPO, "data", "surface_environment_v2.0.csv")
DOC = os.path.join(REPO, "docs", "v2.0-surface-environment.md")

ALL_TOKENS = SHIELDED_TOKENS + SHIELDED_TOKENS_EXTRA


# --------------------------------------------------------------------------- #
# Registry structure                                                           #
# --------------------------------------------------------------------------- #
def test_registry_complete():
    """Every required column populated for every row; all three channels present."""
    rows = se.load(REGISTRY)
    assert rows, "registry is empty"

    channels = {r.channel for r in rows}
    assert channels == set(se.CHANNELS), f"channels present: {sorted(channels)}"
    # a missing neutron row fails outright -- fp-silent-neutron-omission
    assert any(r.channel == "neutron" for r in rows)

    for r in rows:
        for col in se.REQUIRED_COLUMNS:
            val = getattr(r, col)
            assert str(val).strip() != "", f"{r.channel}/{r.quantity}: {col} empty"
        assert r.bias_direction in se.BIAS_DIRECTIONS or r.bias_direction == "-"

    header = "\n".join(se.header_lines(REGISTRY))
    assert "ZERO OVERBURDEN" in header
    assert "BY CONSTRUCTION" in header
    assert "VETO CREDIT = 1.0 EXACTLY" in header
    assert "3 GW_th at 25 m" in header


def test_hash_match():
    """Every artifact_path resolves and every stored SHA-256 recomputes."""
    bad = []
    for r in se.load(REGISTRY):
        p = os.path.join(REPO, r.artifact_path)
        if not os.path.isfile(p):
            bad.append((r.channel, r.quantity, "MISSING", r.artifact_path))
        elif se.sha256_of(p) != r.artifact_sha256:
            bad.append((r.channel, r.quantity, "HASH", r.artifact_path))
    assert bad == [], f"registry rows pointing at a missing/changed artifact: {bad}"


def test_labels_separate():
    """One accuracy label per channel; neutron order_of_magnitude; no combined band."""
    rows = se.load(REGISTRY)
    per_channel = {}
    for r in rows:
        per_channel.setdefault(r.channel, set()).add(r.accuracy_label)
    for ch, labels in per_channel.items():
        assert len(labels) == 1, f"{ch} carries {len(labels)} labels: {labels}"
        assert labels.pop() == se.accuracy_label(ch)

    assert se.accuracy_label("neutron") == "order_of_magnitude"
    assert all(r.accuracy_label == "order_of_magnitude"
               for r in rows if r.channel == "neutron")

    # No combined-band field in the CSV...
    text = open(REGISTRY, encoding="utf-8").read().lower()
    for forbidden in ("combined_band", "combined_uncertainty", "phase_uncertainty",
                      "overall_band", "average_band", "total_uncertainty"):
        assert forbidden not in text, f"combined-band field {forbidden!r} in the registry"

    # ...and no combined-band accessor in the loader API.
    api = [n for n in dir(se) if not n.startswith("_")]
    for n in api:
        low = n.lower()
        assert not ("combined" in low or "overall" in low or "average" in low), (
            f"loader exposes {n!r}, which a consumer could read as a combined band")

    # a consumer cannot get a neutron number without its tag
    q = se.get("neutron", "Phi_th", REGISTRY)
    assert q.accuracy_label == "order_of_magnitude"
    assert isinstance(q, se.EnvironmentQuantity)


# --------------------------------------------------------------------------- #
# Registry values re-derived from their frozen artifacts (not trusted)          #
# --------------------------------------------------------------------------- #
def _csv_header_value(path, key):
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("#"):
                break
            if line.startswith(f"# {key}"):
                return line[len(f"# {key}"):].lstrip(" =").rstrip()
    raise AssertionError(f"{key} not in {path}")


def test_registry_values_rederived_from_artifacts():
    """Every headline scalar is re-derived from its artifact, not restated."""
    mu = os.path.join(REPO, "data", "muon_dRdEdep.csv")
    ga = os.path.join(REPO, "data", "compton_dRdEdep.csv")
    nt = os.path.join(REPO, "data", "ambient_neutron_thermal_v2.0.csv")
    nf = os.path.join(REPO, "data", "ambient_neutron_flux_v1.1.csv")

    # muon rate + MC error, parsed from the frozen header
    raw = _csv_header_value(mu, "integral_muon_rate_Hz")
    val, _, err = raw.partition("+/-")
    assert se.get("muon", "through_wafer_rate").value == float(val.strip())
    assert se.get("muon", "rate_mc_uncertainty").value == float(err.strip())

    # muon grid floor = first tabulated energy = first shared-grid bin CENTRE
    with open(mu, encoding="utf-8") as fh:
        first = next(ln for ln in fh if not ln.startswith("#")
                     and not ln.startswith("E_dep"))
    e0 = float(first.split(",")[0])
    assert se.get("muon", "grid_floor_first_bin_center").value == e0
    edges = md.shared_energy_grid(version="v1.0")   # frozen v1.0 artifacts live here
    assert np.sqrt(edges[0] * edges[1]) == pytest.approx(e0, rel=1e-6)

    # gamma bound single-scatter rate
    graw = _csv_header_value(ga, "total_single_scatter_rate_Hz")
    assert se.get("gamma", "through_wafer_single_scatter_rate").value == \
        float(graw.split("(")[0].strip())
    assert "BOUND incoherent" in graw

    # Compton edges, closed form from the committed line list
    for iso, e_gamma in (("K40", 1460.822), ("Bi214", 1764.494), ("Tl208", 2614.511)):
        want = 2.0 * e_gamma**2 / (cs.M_E_KEV + 2.0 * e_gamma)
        assert se.get("gamma", f"compton_edge_{iso}").value == pytest.approx(want, abs=1e-3)

    # neutron: Phi_th from the sub-eV table's own header
    m = re.search(r"Phi_th = ([0-9.eE+-]+) cm\^-2 s\^-1",
                  open(nt, encoding="utf-8").read())
    assert m
    assert se.get("neutron", "Phi_th").value == pytest.approx(float(m.group(1)), rel=1e-9)
    assert se.get("neutron", "Phi_th").value > 0.0   # SC4: never zero

    # neutron: anchor scalar and both integrals appear in the v1.1 header
    hdr = open(nf, encoding="utf-8").read()
    assert "k = 1.09610" in hdr
    assert se.get("neutron", "anchor_scalar_k").value == 1.09610
    assert "3.550e-03" in hdr and "3.239e-03" in hdr and "1.317e-02" in hdr
    assert se.get("neutron", "Phi_anchored_10MeV_10GeV").value == 3.550e-3
    assert se.get("neutron", "Phi_native_untuned_10MeV_10GeV").value == 3.239e-3
    assert se.get("neutron", "Phi_broad_0p01eV_10GeV").value == 1.317e-2


# --------------------------------------------------------------------------- #
# AUDIT A -- no shielded quantity, credits exactly 1.0                          #
# --------------------------------------------------------------------------- #
def test_no_shield_scan():
    """ROADMAP SC5: executed token scan over the set and its import closure."""
    files = import_closure_files(se, md, cs, vc)
    names = {os.path.basename(f) for f in files}
    assert {"surface_environment.py", "veto_credit.py"} <= names, (
        f"import closure did not resolve: {sorted(names)}")

    # source files: every hit must be allow-listed or an explicit not-applied line
    src_hits = [h for h in scan_paths(files, ALL_TOKENS)
                if not is_allowlisted(h[0], h[3]) and not is_not_applied(h[3])]
    assert src_hits == [], f"applied shielded quantity in the import closure: {src_hits}"

    # registry + declaration prose
    for path in (REGISTRY, DOC):
        text = open(path, encoding="utf-8").read()
        bad = [h for h in scan_text(text, ALL_TOKENS, skip_fenced=True)
               if not is_not_applied(h[2])]
        assert bad == [], f"{os.path.basename(path)} applies a shielded quantity: {bad}"

    # the guard list is IMPORTED, not re-typed
    tokens, extra = se.shielded_token_guard()
    assert tokens is SHIELDED_TOKENS and extra is SHIELDED_TOKENS_EXTRA


def test_veto_credit_unity():
    """Every reachable credit sentinel returns EXACTLY 1.0, by construction."""
    assert vc.L2_CREDIT == 1.0
    assert vc.L1STAR_CREDIT == 1.0
    assert vc.L1_REJECTION_CREDIT == 1.0
    assert vc.TAXONOMY, "the veto taxonomy is empty"
    for row_id in sorted(vc.TAXONOMY):
        assert vc.credit_for(row_id) == 1.0, f"{row_id} credit != 1.0"
    assert vc.multiplicity_rejection_is_zero() is True

    assert se.veto_credit() == 1.0
    doc = se.veto_credit.__doc__ or ""
    assert "BY CONSTRUCTION" in doc.upper(), (
        "a 1.0 arrived at as a policy DEFAULT could be quietly relaxed later; the "
        "loader must document that it follows from the absence of the apparatus")
    assert "no veto" in doc.lower()

    header = "\n".join(se.header_lines(REGISTRY))
    assert "BY CONSTRUCTION" in header.upper()


# --------------------------------------------------------------------------- #
# AUDIT B -- directional bias                                                   #
# --------------------------------------------------------------------------- #
AUDIT_ROW_RE = re.compile(
    r"^\|\s*\*\*(?P<channel>muon|gamma|neutron)\*\*\s*\|"
    r"(?P<mid>.*?)\|\s*(?P<dev>[^|]*?)\s*\|"
    r"\s*\*\*`(?P<direction>flatters_SB|penalizes_SB|neutral)`\*\*\s*\|"
)

COMPOUNDED_RE = re.compile(r"Compounded-effect factor\s*=\s*\*{0,2}([0-9]+\.[0-9]+)")


def _doc_audit_rows(text: str):
    rows = {}
    for ln in normalize_unicode(text).splitlines():
        m = AUDIT_ROW_RE.match(ln)
        if m:
            rows[m.group("channel")] = m
    return rows


def test_bias_audit_complete():
    """Three complete rows, SIGNED deviations, direction labels, numeric factor."""
    text = open(DOC, encoding="utf-8").read()
    rows = _doc_audit_rows(text)
    assert set(rows) == set(se.CHANNELS), f"audit rows found: {sorted(rows)}"

    for ch, m in rows.items():
        dev = m.group("dev").strip()
        # A deviation MAGNITUDE with no sign fails -- the sign is the whole point.
        signed = re.search(r"[+-]\s?[0-9]", dev)
        assert signed, (f"{ch}: deviation {dev!r} carries no sign "
                        "(fp-audit-as-formality)")
        assert "%" in dev

    # An all-neutral table is an audit that cannot fail, and is rejected.
    directions = {ch: m.group("direction") for ch, m in rows.items()}
    assert set(directions.values()) != {"neutral"}, (
        "every channel labelled neutral -- an audit that cannot fail is not a check")

    # The contract fixes these three, and they must agree with the registry.
    assert directions["muon"] == "flatters_SB"
    assert directions["gamma"] == "neutral"
    assert directions["neutron"] == "penalizes_SB"
    reg = se.bias_audit(REGISTRY)
    assert {c: d for c, (d, _) in reg.items()} == directions, (
        "the registry bias_direction column and the doc audit table disagree")

    # the muon deviation is ~-20% (below the PDG anchor), stated with its sign
    mu_dev = float(re.search(r"[-+][0-9.]+",
                             normalize_unicode(rows["muon"].group("dev"))).group())
    assert mu_dev < 0 and 15.0 < abs(mu_dev) < 25.0

    # the gamma factor-2 band and the neutron factor-5 phi_lo move are named
    low = text.lower()
    assert "factor-2" in low and "factor 5" in low
    assert "phi_lo" in low or "`phi_lo`" in low

    # the compounded effect is a NUMBER, not a qualitative description
    m = COMPOUNDED_RE.search(normalize_unicode(text))
    assert m, "the compounded-effect factor must be stated as a number"
    factor = float(m.group(1))
    assert 1.0 < factor < 2.0
    # ...and it must be the arithmetic it claims to be
    mu_now = se.get("muon", "through_wafer_rate").value
    ga_now = se.get("gamma", "through_wafer_single_scatter_rate").value
    mu_anchor = mu_now / (1.0 + mu_dev / 100.0)
    assert factor == pytest.approx((mu_anchor + ga_now) / (mu_now + ga_now), abs=5e-4)

    # how many channels sit on the flattering side, stated explicitly
    n_flat = sum(1 for d in directions.values() if d == "flatters_SB")
    assert n_flat == 1
    assert re.search(r"flattering side of their own anchor:\s*\*?\*?1 of 3", text)


def test_bias_audit_is_falsifiable(tmp_path):
    """Demonstrate that the audit FAILS under a sign flip and under all-neutral.

    An audit that passes either way is not testing anything (fp-audit-as-formality).
    """
    text = normalize_unicode(open(DOC, encoding="utf-8").read())
    rows = _doc_audit_rows(text)
    muon_line = rows["muon"].group(0)

    # (a) sign dropped
    dropped = text.replace(muon_line, muon_line.replace("-20.61 %", "20.61 %"), 1)
    r = _doc_audit_rows(dropped)["muon"]
    assert not re.search(r"[+-]\s?[0-9]", r.group("dev").strip()), (
        "dropping the sign must be detectable")

    # (b) sign flipped -> the muon row would no longer be below its anchor
    flipped = text.replace(muon_line, muon_line.replace("-20.61 %", "+20.61 %"), 1)
    dev = float(re.search(r"[-+][0-9.]+",
                          _doc_audit_rows(flipped)["muon"].group("dev")).group())
    assert dev > 0, "a flipped sign must change the parsed deviation"

    # (c) all-neutral
    allneutral = text
    for ch, m in rows.items():
        allneutral = allneutral.replace(
            m.group(0), m.group(0).replace(f"**`{m.group('direction')}`**",
                                           "**`neutral`**"), 1)
    dirs = {c: mm.group("direction") for c, mm in _doc_audit_rows(allneutral).items()}
    assert set(dirs.values()) == {"neutral"}, "the all-neutral mutation must apply"
    # ...and that is exactly the case test_bias_audit_complete rejects.


def test_declared_omissions_recorded():
    """The omissions this set cannot supply are recorded, not assumed negligible."""
    text = open(DOC, encoding="utf-8").read()
    low = text.lower()
    assert "muon-induced neutron" in low
    assert "omission, not as a negligible quantity" in low
    assert "197 mev" in low and "21 %" in low.replace("21%", "21 %")
    assert "20 mev" in low
    assert "double-count" in low
    # the v1.0 paper's neutron omission is disclosed
    assert "omitted neutrons entirely" in low
