# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Plan 10-03: the extended deposited-energy axis, caller pins, axis decoupling.

ROADMAP Phase 10 success criteria 1 and 2.

The decisive assertion in this file is ``np.array_equal``, NOT ``np.allclose``.
A tolerance-based check passes for the naive rebuild too, and would let a
5.10e-04 relative edge drift through into every downstream spectrum. The
counterexample test is what makes the superset claim testable at all: both
constructions pass a bin-count check.
"""
import os
import subprocess
import sys
import zlib

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from qpd_potential import muon_deposit as md
from qpd_potential import response_matrix as rm

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_COMBINED_CSV = os.path.join(_ROOT, "data", "combined_dRdEdep.csv")

keV_to_eV = 1.0e3


def _v1():
    return md.shared_energy_grid("v1.0")


def _ext():
    return md.shared_energy_grid("v2.0-ext")


# --------------------------------------------------------------------------- #
# claim-superset                                                               #
# --------------------------------------------------------------------------- #
def test_exact_superset_array_equal_not_allclose():
    """test-exact-superset. EXACT array equality, max |difference| == 0.0."""
    v1, ext = _v1(), _ext()
    assert np.array_equal(ext[160:], v1)
    assert float(np.abs(ext[160:] - v1).max()) == 0.0
    # every v1.0 bin survives with BOTH its edges intact
    assert np.array_equal(ext[160:-1], v1[:-1])
    assert np.array_equal(ext[161:], v1[1:])


def test_bin_count_and_realised_spacing():
    """test-bin-count. 744 bins, 745 edges, spacing inherited from v1.0."""
    v1, ext = _v1(), _ext()
    assert v1.size == 585 and v1.size - 1 == 584
    assert ext.size == 745 and ext.size - 1 == 744
    dex = md.v1_0_dex_per_bin()
    assert dex == np.log10(2.0e5 / 1.0e-2) / 584          # exact expression
    assert dex == pytest.approx(0.0125017637, abs=1e-10)
    assert 1.0 / dex == pytest.approx(79.988714, abs=1e-5)
    # "80 bins/decade" is NOMINAL: the realised value is not 80.
    assert 1.0 / dex != 80.0
    # the extension's own realised spacing equals the v1.0 one
    ext_dex = np.log10(ext[-1] / ext[0]) / 744
    assert ext_dex == pytest.approx(dex, rel=1e-14)


def test_floor_reaches_0p1_eV_and_first_centre():
    """test-floor-reaches-0p1."""
    ext = _ext()
    floor_eV = float(ext[0]) * keV_to_eV
    assert floor_eV <= 0.1, "the axis does not reach 0.1 eV"
    assert floor_eV == pytest.approx(0.0999350, abs=5e-8)
    first_centre_eV = float(np.sqrt(ext[0] * ext[1])) * keV_to_eV
    assert first_centre_eV == pytest.approx(0.1013838, abs=5e-8)   # 7 significant figures   # 7 sig figs
    # and the v1.0 floor / first centre are untouched
    v1 = _v1()
    assert float(v1[0]) * keV_to_eV == pytest.approx(10.0, abs=1e-12)
    assert float(np.sqrt(v1[0] * v1[1])) * keV_to_eV == pytest.approx(
        10.144972680282425, rel=1e-14)


def test_naive_rejected_counterexample():
    """test-naive-rejected. THE disconfirming check.

    The naive rebuild has the RIGHT bin count and a first centre of 0.1014497 eV
    that looks entirely correct, but its overlapping edges drift from v1.0 by up
    to 5.10e-04 relative because it re-solves the round() over a wider range.
    Without this test the exact-superset claim is untested, since both
    constructions pass a bin-count check."""
    v1 = _v1()
    naive = np.logspace(np.log10(1.0e-4), np.log10(2.0e5), 745)

    # it LOOKS right on every superficial check
    assert naive.size - 1 == 744
    assert float(naive[0]) * keV_to_eV == pytest.approx(0.1, rel=1e-12)
    assert float(np.sqrt(naive[0] * naive[1])) * keV_to_eV == pytest.approx(
        0.1014497, rel=1e-6)
    # ... and it would even pass a loose tolerance check
    assert np.allclose(naive[160:], v1, rtol=1e-3)

    # but it is NOT the v1.0 edge set
    assert not np.array_equal(naive[160:], v1)
    drift = np.abs(naive[160:] - v1) / v1
    assert float(drift.max()) == pytest.approx(5.101629e-04, rel=1e-4)
    assert int(drift.argmax()) == 0        # worst at the v1.0 floor itself
    # its spacing differs from v1.0's
    assert np.log10(2.0e9) / 744 != md.v1_0_dex_per_bin()

    # the SHIPPED construction is not that array
    ext = _ext()
    assert not np.array_equal(ext, naive)
    assert float(np.abs(ext - naive).max()) > 0.0


def test_159_bin_variant_rejected():
    """The rejected 159-bin variant: floor 0.1028536 eV, ABOVE 0.1 eV, so the
    axis would not reach 0.1 eV, and it gives 743 bins not 744. 160 is the
    unique prepend count satisfying both success criterion 1 clauses."""
    v1 = _v1()
    dex = md.v1_0_dex_per_bin()
    for n_pre, expect_floor_eV, expect_bins in ((159, 0.1028536, 743),
                                                (160, 0.0999350, 744),
                                                (161, 0.0970993, 745)):
        pre = 1.0e-2 * 10.0 ** (-np.arange(n_pre, 0, -1) * dex)
        cand = np.concatenate([pre, v1])
        assert cand.size - 1 == expect_bins
        assert float(cand[0]) * keV_to_eV == pytest.approx(expect_floor_eV, abs=5e-8)
        # all three preserve the v1.0 edges; only 160 satisfies BOTH criteria
        assert np.array_equal(cand[n_pre:], v1)
    assert 0.1028536 > 0.1            # 159 fails: floor above 0.1 eV
    assert 0.0970993 <= 0.1           # 161 reaches 0.1 eV but gives 745 bins
    assert md._EXT_PREPENDED_BINS == 160


def test_unknown_version_raises():
    with pytest.raises(ValueError, match="unknown grid version"):
        md.shared_energy_grid("v2.0")
    with pytest.raises(ValueError):
        md.shared_energy_grid("extended")


# --------------------------------------------------------------------------- #
# claim-callers-pinned                                                         #
# --------------------------------------------------------------------------- #
_PIN_TABLE = os.path.join(
    _ROOT, "GPD", "phases",
    "10-sub-ev-grid-extension-and-the-trigger-observable-p-grid",
    "10-03-GRID-CONSTRUCTION.md")


def _grid_call_sites():
    out = subprocess.run(
        ["grep", "-rn", "shared_energy_grid(", "--include=*.py", "src/", "tests/"],
        cwd=_ROOT, capture_output=True, text=True).stdout.strip().splitlines()
    return [h for h in out if "def shared_energy_grid(" not in h]


def test_caller_pins_every_site_is_in_the_table():
    """test-caller-pins. Grep hit count equals version-pin table row count, and
    every call site either passes the version explicitly or is listed with a
    written reason for relying on the default."""
    assert os.path.exists(_PIN_TABLE)
    text = open(_PIN_TABLE).read()
    hits = _grid_call_sites()
    rows = [ln for ln in text.splitlines()
            if ln.startswith("| `src/") or ln.startswith("| `tests/")]
    assert len(rows) == len(hits), (
        f"{len(rows)} pin-table rows for {len(hits)} call sites:\n"
        + "\n".join(hits))
    for h in hits:
        path, line, _ = h.split(":", 2)
        assert f"`{path}:{line}`" in text, f"unpinned call site {path}:{line}"


def test_default_is_v1_0_so_no_archived_product_can_be_rebinned():
    """DEVIATION D1 (10-03-GRID-CONSTRUCTION.md). The plan asked for a v2.0-ext
    default; that broke a Phase-9 test executing concurrently in this worktree
    (744 vs 584 broadcast) and is the fp-default-change proxy caught in the act.
    A v1.0 default makes silent re-binning impossible rather than merely
    pinned-against, and fails in the safe direction."""
    assert md.DEFAULT_GRID_VERSION == "v1.0"
    assert np.array_equal(md.shared_energy_grid(), md.shared_energy_grid("v1.0"))
    assert md.shared_energy_grid().size == 585


def test_phase4_producers_still_emit_the_584_bin_axis():
    """test-phase4-unchanged. The Phase-4 deposit producers are pinned to v1.0
    and still match the archived CSV axis to the same round-trip precision as
    before this plan. Any change in bin count is a failure."""
    csv_centres = rm.load_E_dep_grid_eV(_COMBINED_CSV)
    assert csv_centres.size == 584
    v1_centres = rm.E_dep_grid_from_shared_grid_eV("v1.0")
    assert v1_centres.size == 584
    # source-level pin check: the producers name the version explicitly
    for path in ("src/qpd_potential/muon_deposit.py",
                 "src/qpd_potential/compton_deposit.py",
                 "src/qpd_potential/deposited_spectra.py",
                 "src/nuclear/parse_endf_nGe.py"):
        src = open(os.path.join(_ROOT, path)).read()
        assert 'shared_energy_grid("v1.0")' in src, f"{path} is not pinned"


# --------------------------------------------------------------------------- #
# claim-axis-decoupled                                                         #
# --------------------------------------------------------------------------- #
def test_axis_decoupled_from_the_archived_csv():
    """test-axis-decoupled. The grid-sourced v1.0 axis matches the CSV-parsed
    axis to within 5e-7 relative. The archived R matrices were built on the CSV
    values, so the regenerated R CANNOT be bit-identical to them
    (fp-bit-identical-promise)."""
    csv = rm.load_E_dep_grid_eV(_COMBINED_CSV)
    grid = rm.E_dep_grid_from_shared_grid_eV("v1.0")
    assert csv.size == grid.size == 584
    rel = np.abs(grid - csv) / csv
    assert float(rel.max()) < 5.0e-7
    assert float(rel.max()) == pytest.approx(4.917619e-07, rel=1e-4)
    # ... and it is NOT zero: the two routes really are different axes
    assert float(rel.max()) > 0.0
    assert not np.array_equal(csv, grid)
    assert float(csv[0]) == pytest.approx(10.144970, abs=1e-9)
    assert float(grid[0]) == pytest.approx(10.144972680282425, rel=1e-14)
    # the CSV parser itself is unchanged and still readable
    assert csv[0] < csv[-1] and np.all(np.diff(csv) > 0)


def test_extended_centres_are_an_exact_superset_of_the_v1_centres():
    ext = rm.E_dep_grid_from_shared_grid_eV("v2.0-ext")
    v1 = rm.E_dep_grid_from_shared_grid_eV("v1.0")
    assert ext.size == 744
    assert float(ext[0]) == pytest.approx(0.1013838, abs=5e-8)   # 7 significant figures
    assert np.array_equal(ext[160:], v1)
    assert float(np.abs(ext[160:] - v1).max()) == 0.0
    assert np.all(np.diff(ext) > 0)


def _draws(ss, n=4):
    return np.random.default_rng(ss).random(n)


def _ordinal_child(n_edep, j, design="Ta->Al", variant="non_paralyzable"):
    """The PRE-10-03 scheme, reproduced here so its failure is demonstrable."""
    ss = np.random.SeedSequence(
        [rm.DEFAULT_SEED, zlib.crc32(design.encode()), zlib.crc32(variant.encode())])
    return ss.spawn(n_edep)[j]


def test_seed_stability_energy_keyed_and_ordinal_failure():
    """test-seed-stability. Demonstrate the ordinal scheme FAILS first, then
    that the energy-keyed scheme fixes it -- otherwise the fix is vacuous."""
    v1 = rm.E_dep_grid_from_shared_grid_eV("v1.0")
    ext = rm.E_dep_grid_from_shared_grid_eV("v2.0-ext")
    j_v1, j_ext = 300, 460                      # the SAME deposit energy
    assert float(v1[j_v1]) == float(ext[j_ext])

    # (a) the pre-fix ordinal scheme does NOT survive the column shift
    a = _draws(_ordinal_child(584, j_v1))
    b = _draws(_ordinal_child(744, j_ext))
    assert not np.array_equal(a, b), (
        "the ordinal scheme unexpectedly agreed; the demonstration is vacuous")
    assert _ordinal_child(584, j_v1).spawn_key == (300,)
    assert _ordinal_child(744, j_ext).spawn_key == (460,)

    # (b) the energy-keyed scheme does
    c = _draws(rm.column_seed_sequence(rm.DEFAULT_SEED, "Ta->Al",
                                       "non_paralyzable", float(v1[j_v1])))
    d = _draws(rm.column_seed_sequence(rm.DEFAULT_SEED, "Ta->Al",
                                       "non_paralyzable", float(ext[j_ext])))
    assert np.array_equal(c, d)
    # every overlapping column, not just one
    for k in range(0, 584, 37):
        s1 = rm.column_seed_sequence(rm.DEFAULT_SEED, "Ta->Al", "non_paralyzable",
                                     float(v1[k]))
        s2 = rm.column_seed_sequence(rm.DEFAULT_SEED, "Ta->Al", "non_paralyzable",
                                     float(ext[160 + k]))
        assert s1.entropy == s2.entropy


def test_seed_keys_are_distinct_and_process_stable():
    ext = rm.E_dep_grid_from_shared_grid_eV("v2.0-ext")
    keys = {zlib.crc32((rm._SEED_KEY_FORMAT % float(e)).encode()) for e in ext}
    assert len(keys) == ext.size, "two deposit columns share a sub-seed key"
    # process stability: crc32, never the salted builtin hash
    src = open(os.path.join(_ROOT, "src", "qpd_potential", "response_matrix.py")).read()
    fn = src.split("def column_seed_sequence(")[1].split("\ndef ")[0]
    assert "zlib.crc32" in fn
    assert "hash(" not in fn
    # design and variant still separate the streams
    s_a = rm.column_seed_sequence(1, "Ta->Al", "non_paralyzable", 10.0)
    s_b = rm.column_seed_sequence(1, "Al->Hf", "non_paralyzable", 10.0)
    s_c = rm.column_seed_sequence(1, "Ta->Al", "paralyzable", 10.0)
    assert s_a.entropy != s_b.entropy != s_c.entropy != s_a.entropy


def test_erec_grid_bounds_untouched():
    """Dimensional / scope check: only the DEPOSIT axis moved."""
    edges = rm.build_E_rec_edges_eV()
    assert edges[0] == 0.0                        # underflow bin
    assert edges[1] == pytest.approx(rm.DEFAULT_EREC_MIN_eV)
    assert edges[-1] == pytest.approx(rm.DEFAULT_EREC_MAX_eV)
    assert rm.DEFAULT_EREC_MIN_eV == 1.0e-3
    assert rm.DEFAULT_EREC_MAX_eV == 1.0e5


#: PRE-EXISTING, DOCUMENTED CHURN, NOT CAUSED BY PHASE 10. Running the test suite
#: regenerates these two flux tables and rewrites their `generated:` / `git_sha:`
#: HEADER LINES ONLY. Verified line by line below rather than excluded on trust.
_SUITE_CHURN = ("data/flux/reactor_flux_v1.0.csv",
                "data/flux/reactor_flux_billard_variant.csv")

#: DELIBERATELY REBUILT by the 2026-07-25 energy-scale recalibration (USER
#: DECISION; CONVENTIONS Section E.1).  The count->energy constant C is now fixed
#: by params.CALIB_SLOPE = 1.0 instead of eps = 0.5, so E_rec ESTIMATES the
#: deposit rather than carrying the physical deposit->QP conversion fraction on
#: the axis.  Every E_rec-axis artifact below is therefore a NEW-SCALE product and
#: its modification is intended, not the freeze violation this test exists to
#: catch.  They are exempted from the "unexpected" predicate ONLY -- they are NOT
#: added to _SUITE_CHURN, because that tuple additionally asserts a header-only
#: diff, which a rebuilt npz/png/CSV cannot satisfy.
#: artifacts/stage1/ is deliberately NOT in this list: the v1.0 matrices are the
#: frozen comparison baseline and were not rebuilt (fp-overwrite-v1-matrices).
_CALIB_REBUILD_2026_07_25 = (
    "artifacts/v2.0/response_matrix_AlHf_ext.npz",
    "artifacts/v2.0/response_matrix_TaAl_ext.npz",
    "artifacts/v2.0/cevns_dRdErec_ext_AlHf.csv",
    "artifacts/v2.0/cevns_dRdErec_ext_TaAl.csv",
    "artifacts/v2.0/neutron_dRdErec_ext_AlHf.csv",
    "artifacts/v2.0/neutron_dRdErec_ext_TaAl.csv",
    "artifacts/v2.0/ge71_ec_dRdErec_AlHf.csv",
    "artifacts/v2.0/ge71_ec_dRdErec_TaAl.csv",
    "artifacts/v2.0/al_hf_spectrum_AlHf.png",
)


def test_no_frozen_artifact_was_modified_by_this_plan():
    """git-level check: nothing under data/ or artifacts/ changed."""
    out = subprocess.run(["git", "status", "--porcelain", "data/", "artifacts/"],
                         cwd=_ROOT, capture_output=True, text=True).stdout
    # Untracked ('??') and NEWLY ADDED ('A ') paths are not modifications of a
    # frozen artifact: a file that did not exist before cannot have been modified.
    # MODIFY / DELETE / RENAME of an existing artifact remains caught. Narrowed in
    # Plan 14-01, which froze new acquisitions under data/ and new products under
    # artifacts/v2.0/ and tripped the over-broad predicate rather than the behaviour.
    changed = [ln for ln in out.splitlines()
               if not ln.startswith("??") and not ln.startswith("A ")]
    unexpected = [ln for ln in changed
                  if not any(c in ln for c in _SUITE_CHURN)
                  and not any(c in ln for c in _CALIB_REBUILD_2026_07_25)]
    assert unexpected == [], f"frozen artifacts modified: {unexpected}"
    for path in _SUITE_CHURN:
        diff = subprocess.run(["git", "diff", "--unified=0", "--", path],
                              cwd=_ROOT, capture_output=True, text=True).stdout
        for ln in diff.splitlines():
            if ln.startswith(("+++", "---")) or not ln.startswith(("+", "-")):
                continue
            assert "generated:" in ln and "git_sha:" in ln, (
                f"{path}: a NON-header line changed: {ln}")
