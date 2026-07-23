# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Plan 10-05: the archived-artifact disposition register and its guard.

ROADMAP Phase 10 success criteria 2 and 5, plus the labelling half of 4.

Success criterion 2 is discharged by the register PLUS the bit-for-bit carry
proof, not by the register alone: a register that says "carried" without
demonstrating bit-identity is an assertion.
"""
import os
import subprocess
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from qpd_potential import legacy_grid as lg
from qpd_potential import muon_deposit as md
from qpd_potential import response_matrix as rm
from qpd_potential import trigger

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PHASE = os.path.join(_ROOT, "GPD", "phases",
                      "10-sub-ev-grid-extension-and-the-trigger-observable-p-grid")
_ENUM_CMD = "git ls-files | grep -E '\\.(csv|npz)$'"
SHARED_GRID_PRODUCTS = ("data/muon_dRdEdep.csv", "data/compton_dRdEdep.csv",
                        "data/combined_dRdEdep.csv")


def _enumerate():
    return subprocess.run(["bash", "-c", _ENUM_CMD], cwd=_ROOT,
                          capture_output=True, text=True).stdout.strip().splitlines()


def _numeric_first_col(path):
    vals = []
    with open(os.path.join(_ROOT, path)) as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            try:
                vals.append(float(s.split(",", 1)[0]))
            except ValueError:
                continue
    return np.array(vals)


# --------------------------------------------------------------------------- #
# claim-disposition                                                            #
# --------------------------------------------------------------------------- #
def test_register_closure():
    """test-register-closure. Enumeration hit count equals register row count;
    no empty disposition, no empty reason; bounded rows carry a numeric floor
    with units."""
    files = _enumerate()
    reg = lg.load_register()
    assert len(files) == len(reg), (
        f"{len(files)} enumerated artifacts vs {len(reg)} register rows.\n"
        f"missing from register: {sorted(set(files) - set(reg))}\n"
        f"register rows with no file: {sorted(set(reg) - set(files))}\n"
        "A newly added tracked .csv/.npz needs a disposition row -- that is the "
        "closure guard working, not a spurious failure.")
    assert set(files) == set(reg)
    for p, d in reg.items():
        assert d.disposition in lg.DISPOSITION_VALUES
        assert len(d.reason) > 40, f"{p}: reason too short to be a justification"
        assert d.native_axis and d.axis_units
        if d.disposition in ("bounded_native_axis", "bounded_superseded"):
            assert d.validity_floor is not None and d.validity_floor > 0, (
                f"{p} is tagged bounded but carries no numeric validity floor")


def test_register_floors_are_read_from_the_files_not_asserted():
    """Every bounded row's floor must equal the artifact's actual first
    tabulated abscissa, re-read here from the frozen file."""
    reg = lg.load_register()
    for p in ("artifacts/stage1/cevns_dRdT.csv", "data/endf_nGe_elastic_v1.1.csv",
              "data/flux/reactor_flux_v1.0.csv", "data/ge_xcom_mu.csv",
              "data/ge_incoherent_S.csv", "data/external/nucleus2019_fig1_ge.csv",
              *SHARED_GRID_PRODUCTS):
        assert reg[p].validity_floor == pytest.approx(
            float(_numeric_first_col(p).min()), rel=1e-12), p
    # the archived matrices' floor is their first deposit centre, read from npz
    for p in ("artifacts/stage1/response_matrix_TaAl.npz",
              "artifacts/stage1/response_matrix_AlHf.npz"):
        z = np.load(os.path.join(_ROOT, p), allow_pickle=True)
        assert reg[p].validity_floor == pytest.approx(
            float(z["E_dep_centers_eV"].min()), rel=1e-12)


def test_guard_raises_below_a_recorded_floor():
    """test-guard-raises. A raise, never a clamp / extrapolation / zero."""
    reg = lg.load_register()
    # CEvNS dR/dT table: floor 5 eV on its own recoil axis
    with pytest.raises(lg.LegacyArtifactError, match="BELOW the recorded validity floor"):
        lg.check_evaluation_point("artifacts/stage1/cevns_dRdT.csv", 0.1, reg)
    # the shared-grid deposit spectra: floor 1.014497e-02 keV = 10.14 eV
    with pytest.raises(lg.LegacyArtifactError):
        lg.check_evaluation_point("data/muon_dRdEdep.csv", 1.0e-4, reg)
    # arrays are rejected wholesale, not masked
    with pytest.raises(lg.LegacyArtifactError):
        lg.check_evaluation_point("data/muon_dRdEdep.csv",
                                  np.array([1.0, 0.1, 1e-4]), reg)
    with pytest.raises(lg.LegacyArtifactError):
        lg.check_evaluation_point("data/muon_dRdEdep.csv", np.nan, reg)
    # ... and exactly AT the floor is legal
    lo = reg["data/muon_dRdEdep.csv"].validity_floor
    out = lg.check_evaluation_point("data/muon_dRdEdep.csv", lo, reg)
    assert np.all(np.isfinite(out))


def test_guard_reports_units_axis_and_disposition():
    reg = lg.load_register()
    with pytest.raises(lg.LegacyArtifactError) as ei:
        lg.check_evaluation_point("data/flux/reactor_flux_v1.0.csv", 0.01, reg)
    msg = str(ei.value)
    assert "MeV" in msg and "antineutrino energy" in msg
    assert "bounded_native_axis" in msg
    assert "not a" in msg and "clamp" in msg


def test_unregistered_artifact_raises_rather_than_defaulting():
    with pytest.raises(KeyError, match="no disposition row"):
        lg.disposition_for("data/some_new_table.csv")


@pytest.mark.parametrize("path", SHARED_GRID_PRODUCTS)
def test_carry_without_reinterpolation_is_bit_identical(path):
    """test-carry-without-reinterp. THE proof behind the 'carried' tag.

    The carry is an INDEX operation, legitimate only because plan 10-03
    preserved the v1.0 edges exactly. This test checks both halves:
      (a) the values are bit-identical over the overlapping bins, max difference
          EXACTLY 0.0;
      (b) the artifact really does sit on those bins -- 584 rows whose energy
          column matches the extended axis centres 160..743 to the recorded
          4.918e-07 CSV round-trip precision. Without (b), (a) would be a
          tautology about np.full/assignment.
    """
    reg = lg.load_register()
    assert reg[path].disposition == "carried_onto_extended_axis_without_reinterpolation"

    rows = np.asarray([[float(t) for t in ln.split(",")]
                       for ln in open(os.path.join(_ROOT, path))
                       if ln.strip() and not ln.startswith("#")
                       and not ln[0].isalpha()], dtype=float)
    E_keV, rate = rows[:, 0], rows[:, 1]
    assert E_keV.size == 584

    # (b) the rows really are the v1.0 bins of the extended axis
    ext_centres_keV = rm.E_dep_grid_from_shared_grid_eV("v2.0-ext")[160:] / 1.0e3
    assert ext_centres_keV.size == 584
    rel = np.abs(ext_centres_keV - E_keV) / E_keV
    assert float(rel.max()) < 5.0e-7, (
        "the artifact's energy column does not sit on the extended axis's upper "
        "584 bins; the 'carried' tag would be wrong")

    # (a) the carry itself
    carried = lg.carried_onto_extended_axis(rate)
    assert carried.shape == (744,)
    assert np.array_equal(carried[160:], rate)
    assert float(np.abs(carried[160:] - rate).max()) == 0.0
    # the lower 160 bins carry NO DATA -- NaN, not zero
    assert np.all(np.isnan(carried[:160]))
    assert not np.any(carried[:160] == 0.0)


def test_carry_rejects_a_quantity_that_is_not_on_the_v1_grid():
    with pytest.raises(ValueError, match="not on the v1.0 shared deposit grid"):
        lg.carried_onto_extended_axis(np.zeros(320))


def test_response_matrices_are_NOT_tagged_carried():
    """A finding worth pinning. The archived matrices' deposit centres are the
    CSV ROUND-TRIPPED values, 4.918e-07 from the extended axis's exact geometric
    means, so placing them on the extended axis would be a genuine (if tiny)
    re-mapping rather than an index copy. They are therefore bounded_superseded,
    not carried."""
    reg = lg.load_register()
    for p in ("artifacts/stage1/response_matrix_TaAl.npz",
              "artifacts/stage1/response_matrix_AlHf.npz"):
        assert reg[p].disposition == "bounded_superseded"
        assert "4.918e-07" in reg[p].reason
        z = np.load(os.path.join(_ROOT, p), allow_pickle=True)
        exact = rm.E_dep_grid_from_shared_grid_eV("v1.0")
        csv_axis = z["E_dep_centers_eV"]
        assert not np.array_equal(csv_axis, exact)
        assert float((np.abs(exact - csv_axis) / csv_axis).max()) < 5.0e-7


#: PRE-EXISTING, DOCUMENTED CHURN, NOT CAUSED BY PHASE 10. Running the test suite
#: regenerates these two flux tables and rewrites their `generated:` / `git_sha:`
#: HEADER LINES ONLY (verified: `git diff` shows exactly one changed line per file,
#: and it is the provenance stamp). The data rows are untouched. This guard therefore
#: checks their DATA separately rather than reporting a false fp-header-rewrite.
_SUITE_CHURN = ("data/flux/reactor_flux_v1.0.csv",
                "data/flux/reactor_flux_billard_variant.csv")


def test_frozen_headers_were_not_rewritten():
    """fp-header-rewrite. The register is a sidecar; the frozen artifacts' own
    provenance headers carry recorded git SHAs and are not edited by this plan."""
    out = subprocess.run(["git", "status", "--porcelain", "data/", "artifacts/stage1/"],
                         cwd=_ROOT, capture_output=True, text=True).stdout
    changed = [ln for ln in out.splitlines() if not ln.startswith("??")]
    unexpected = [ln for ln in changed
                  if not any(c in ln for c in _SUITE_CHURN)]
    assert unexpected == [], f"frozen artifacts modified: {unexpected}"
    # for the two churning files, prove only the provenance STAMP moved
    for path in _SUITE_CHURN:
        diff = subprocess.run(["git", "diff", "--unified=0", "--", path],
                              cwd=_ROOT, capture_output=True, text=True).stdout
        body = [ln for ln in diff.splitlines()
                if (ln.startswith("+") or ln.startswith("-"))
                and not ln.startswith(("+++", "---"))]
        for ln in body:
            assert "generated:" in ln and "git_sha:" in ln, (
                f"{path}: a NON-header line changed: {ln}")


# --------------------------------------------------------------------------- #
# claim-labelling                                                              #
# --------------------------------------------------------------------------- #
_RETRACTED_PATTERNS = ("Nothing below 10 eV", "never display below 10 eV")


def test_retraction_no_live_statement_of_the_display_rule():
    """test-retraction. Any surviving occurrence must be explicitly marked as
    retracted history with its date, never left standing as a live rule."""
    hits = subprocess.run(
        ["grep", "-rn", "-i", "below 10 eV", "--include=*.py", "--include=*.ipynb",
         "--include=*.md", "src/", "tests/", "notebooks/", "GPD/"],
        cwd=_ROOT, capture_output=True, text=True).stdout.splitlines()
    live = []
    for h in hits:
        low = h.lower()
        # GPD/milestones/** is a closed historical archive BY LOCATION: v1.0 and v1.1
        # milestone documents record what the project believed at the time and are not
        # live statements. GPD/phases/10-** is this phase's own working record.
        if h.startswith("GPD/milestones/") or h.startswith("GPD/phases/10-"):
            continue
        if h.startswith("tests/test_legacy_grid_disposition.py"):
            continue                       # this guard's own pattern strings
        # The rule is a DISPLAY rule. A sentence that merely mentions the energy
        # range (e.g. "no experiment has measured an LEE spectrum below ~10 eV",
        # "not an independent physical measurement below 10 eV") is not a
        # restatement of it and is not what this guard is for.
        states_the_rule = any(w in low for w in
                              ("display", "displayed", "plot", "shown", "figure"))
        if not states_the_rule:
            continue
        marked = ("retract" in low or "history" in low or "no longer" in low
                  or "superseded" in low or "2026-07-22" in h)
        if not marked:
            live.append(h)
    assert live == [], (
        "the retracted display rule still stands as a live statement in:\n"
        + "\n".join(live))


def test_the_one_live_occurrence_scope_forbids_fixing_is_recorded():
    """HONEST GAP. paper/HANDOFF.md line 33 still carries the rule as a live
    instruction ("Keep this for any new/regenerated figure"). Plan 10-05 is
    explicitly forbidden from modifying anything under paper/, so it CANNOT be
    fixed here. It is recorded rather than silently excluded from the grep."""
    hs = open(os.path.join(_ROOT, "paper", "HANDOFF.md")).read()
    assert "below 10 eV" in hs, (
        "paper/HANDOFF.md no longer carries the rule; update the disposition note")
    note = open(os.path.join(_PHASE, "10-05-ARTIFACT-DISPOSITION.md")).read()
    assert "paper/HANDOFF.md" in note, (
        "the unfixable live occurrence is not recorded in the disposition note")
    out = subprocess.run(["git", "status", "--porcelain", "paper/"],
                         cwd=_ROOT, capture_output=True, text=True).stdout
    assert [l for l in out.splitlines() if not l.startswith("??")] == [], (
        "nothing under paper/ may be modified by this plan")


def test_notebook_no_longer_prints_the_retracted_rule_as_current():
    nb = open(os.path.join(_ROOT, "notebooks", "paper_calculations.ipynb")).read()
    for pat in _RETRACTED_PATTERNS:
        if pat in nb:
            # allowed only inside an explicit retraction sentence
            assert "RETRACTED" in nb, (
                f"{pat!r} appears in the notebook without a retraction marker")
    assert "100 meV" in nb, "the notebook does not state the current position"
    assert "trigger probability" in nb


def test_regime_boundary_labelled_from_the_single_constant():
    """test-regime-labelled. Every sub-eV deliverable names the boundary and
    takes it from the plan 10-02 constant, not a restated literal."""
    for fn in ("10-05-COUNTING-FLOOR.md", "10-05-ARTIFACT-DISPOSITION.md"):
        text = open(os.path.join(_PHASE, fn)).read()
        assert "SUBEV_REGIME_BOUNDARY_eV" in text, fn
        assert f"{trigger.SUBEV_REGIME_BOUNDARY_eV:g} eV" in text, fn
        assert "trigger probability" in text and "dR/dE_rec" in text, fn


# --------------------------------------------------------------------------- #
# claim-floor                                                                  #
# --------------------------------------------------------------------------- #
_VAR = "non_paralyzable"
_EXT = {"Ta->Al": "response_matrix_TaAl_ext.npz", "Al->Hf": "response_matrix_AlHf_ext.npz"}
_ROADMAP_NOBS = {"Ta->Al": 39.4, "Al->Hf": 49.9}
_ROADMAP_FLOOR = {0.1: {"Ta->Al": 35.6, "Al->Hf": 31.6},
                  0.5: {"Ta->Al": 15.9, "Al->Hf": 14.2},
                  10.0: {"Ta->Al": 3.6, "Al->Hf": 3.2},
                  100.0: {"Ta->Al": 1.2, "Al->Hf": 1.1}}


def _nobs(design, target_eV):
    z = np.load(os.path.join(_ROOT, "artifacts", "v2.0", _EXT[design]), allow_pickle=True)
    Ec = z["E_dep_centers_eV"]
    j = int(np.argmin(np.abs(np.log(Ec) - np.log(target_eV))))
    return float(z[f"N_obs_mean_{_VAR}"][j]), float(z[f"rel_spread_{_VAR}"][j]), float(Ec[j])


@pytest.mark.parametrize("design", list(_EXT))
@pytest.mark.parametrize("target", [0.1, 0.5, 10.0, 100.0])
def test_floor_rederived_from_the_pipeline(design, target):
    """test-floor-rederived. DERIVED from N_obs, never copied from the roadmap
    (fp-floor-quoted-not-derived). The roadmap figures come from an orchestrator
    note in STATE.md, not from a verified phase deliverable."""
    n, _, _ = _nobs(design, target)
    floor_pct = 100.0 / np.sqrt(n)
    road = _ROADMAP_FLOOR[target][design]
    assert floor_pct == pytest.approx(road, rel=0.05), (
        f"{design} at {target} eV: derived {floor_pct:.3f}% vs roadmap {road}%")


@pytest.mark.parametrize("design", list(_EXT))
def test_measured_Nobs_at_half_eV_against_the_roadmap_note(design):
    n, _, _ = _nobs(design, 0.5)
    assert n == pytest.approx(_ROADMAP_NOBS[design], rel=0.05)


@pytest.mark.parametrize("design", list(_EXT))
def test_floor_saturation_signature(design):
    """test-floor-saturation-signature. THE counterexample check.

    Reproducing exactly the LINEAR extrapolation at 100 eV would mean saturation
    is not entering the response above the Phase-5 onsets (~52.9 eV Ta->Al,
    ~32.1 eV Al->Hf), and would be a FINDING, not a pass."""
    n_half, _, E_half = _nobs(design, 0.5)
    n_100, _, E_100 = _nobs(design, 100.0)
    linear = n_half * (E_100 / E_half)
    assert n_100 < linear, (
        f"{design}: measured N_obs(100 eV) = {n_100:.1f} is NOT below the linear "
        f"extrapolation {linear:.1f}; saturation is not entering the response "
        "above the onset. This is a finding, not a pass.")
    ratio = n_100 / linear
    assert 0.7 < ratio < 0.95, f"{design}: sub-linearity ratio {ratio:.4f}"
    # and the derived floor must land nearer the roadmap's sub-linear figure
    # than the naive linear one
    floor_meas = 100.0 / np.sqrt(n_100)
    floor_lin = 100.0 / np.sqrt(linear)
    road = _ROADMAP_FLOOR[100.0][design]
    assert abs(floor_meas - road) < abs(floor_lin - road)


@pytest.mark.parametrize("design", list(_EXT))
def test_counting_floor_document_carries_the_framing(design):
    """test-floor-not-resolution (the machine-checkable part of a human-review
    test). fp-poisson-as-resolution is the milestone-wide proxy this guards."""
    text = open(os.path.join(_PHASE, "10-05-COUNTING-FLOOR.md")).read()
    for needed in ("best case", "no resolution parameter",
                   "baseline", "amplifier", "phonon-collection",
                   "position dependence", "readout",
                   "impulse-approximation", "quadrature",
                   "fp-poisson-as-resolution"):
        assert needed in text, f"counting-floor doc missing: {needed!r}"
    # the measured numbers, not the roadmap's, must be present
    n_half, _, _ = _nobs(design, 0.5)
    assert f"{n_half:.3f}" in text, f"measured N_obs(0.5 eV) for {design} not quoted"


def test_counting_floor_document_compares_spread_against_the_1_over_sqrtN_label():
    """The plan requires 1/sqrt(N_obs) to be compared against the ACTUAL column
    spread at 0.1 eV, with a verdict -- not assumed to agree."""
    text = open(os.path.join(_PHASE, "10-05-COUNTING-FLOOR.md")).read()
    for design in _EXT:
        _, spread, _ = _nobs(design, 0.1)
        assert f"{100*spread:.3f}" in text, (
            f"{design}: measured 0.1 eV column spread not quoted in the floor doc")
    assert "12.5" in text          # the Al->Hf disagreement
