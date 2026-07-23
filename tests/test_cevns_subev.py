# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Phase 12, plan 12-01: CALC-17 truncation bound and the VALD-10 plateau leg.

EVERY TOLERANCE IN THIS FILE IS A STATED PHYSICS TARGET, NOT A FITTED VALUE.
The targets come from ROADMAP Phase 12 success criteria 2 and 4 and from the
recorded planning measurements, and they were written BEFORE the artifacts were
regenerated.  Loosening one to make a test pass is exactly the failure mode
``fp-narrow-the-window`` and ``fp-bound-by-assertion`` exist to block.
"""
import os
import re
import subprocess
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from qpd_potential import cevns, cevns_subev as cs, params  # noqa: E402

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TRUNC_CSV = os.path.join(_ROOT, "artifacts", "v2.0", "cevns_truncation_bound.csv")
_PLATEAU_CSV = os.path.join(_ROOT, "artifacts", "v2.0", "cevns_plateau_profile.csv")
_GATES_MD = os.path.join(
    _ROOT, "GPD", "phases",
    "12-reactor-cevns-down-to-100-mev-at-the-paper-s-surface-scenario-p-sig",
    "12-01-SUBEV-GATES.md")

# ---- stated physics targets ------------------------------------------------ #
FLOOR_eV = 0.0999350                 # Phase-10 extended-grid floor
ROADMAP_BOUND_AT_100meV = 0.0081     # ROADMAP SC4: "<= 0.81% at T = 100 meV"
PLANNING_BOUND_AT_FLOOR = 0.00803    # recorded planning measurement
ROADMAP_EMIN_100meV_keV = 58.16      # ROADMAP SC4, the molar-mass value
PLANNING_PLATEAU = 2372.4            # counts/kg/day/keV
PLATEAU_APPROACH_MAX_DEFICIT = 0.015  # dR/dT(floor) within 1.5% BELOW the plateau
SC2_WINDOW_HI_eV = 10.0


def _load_csv(path):
    rows = []
    header = None
    with open(path) as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if header is None:
                header = s.split(",")
                continue
            rows.append([float(t) for t in s.split(",")])
    return header, np.asarray(rows, float)


@pytest.fixture(scope="module")
def trunc():
    assert os.path.exists(_TRUNC_CSV), (
        "artifacts/v2.0/cevns_truncation_bound.csv missing -- run "
        "`python -m qpd_potential.cevns_subev`")
    return _load_csv(_TRUNC_CSV)


@pytest.fixture(scope="module")
def plateau():
    assert os.path.exists(_PLATEAU_CSV), (
        "artifacts/v2.0/cevns_plateau_profile.csv missing -- run "
        "`python -m qpd_potential.cevns_subev`")
    return _load_csv(_PLATEAU_CSV)


# =========================================================================== #
# claim-truncation-bound                                                      #
# =========================================================================== #
def test_bound_magnitude(trunc):
    """test-bound-magnitude. <= 0.81% at the extended-grid floor, reproducing the
    recorded 0.803% to within 1% relative.

    A value materially ABOVE 0.81% means CALC-17's established figure does NOT
    reproduce and must be reported as a failed reproduction -- never absorbed by
    relaxing the target.
    """
    b = cs.truncation_bound(FLOOR_eV)["bound_fraction"]
    assert b <= ROADMAP_BOUND_AT_100meV, (
        f"bound {b:.6%} exceeds the ROADMAP SC4 target 0.81% -- CALC-17 does not "
        "reproduce; report the failure, do not widen the target")
    assert b == pytest.approx(PLANNING_BOUND_AT_FLOOR, rel=0.01)
    # and it appears in the artifact at that same energy
    header, rows = trunc
    i = int(np.argmin(np.abs(rows[:, 0] - FLOOR_eV)))
    assert rows[i, 0] == pytest.approx(FLOOR_eV, rel=1e-9)
    assert rows[i, header.index("bound_fraction")] == pytest.approx(b, rel=1e-9)


def test_bound_at_100meV_and_150meV():
    """The other two recorded planning values, at exactly 100 and 150 meV."""
    assert cs.truncation_bound(0.1)["bound_fraction"] == pytest.approx(0.00802, rel=0.01)
    assert cs.truncation_bound(0.15)["bound_fraction"] == pytest.approx(0.00383, rel=0.01)


def test_bound_vanishes(trunc):
    """test-bound-vanishes. EXACTLY 0.0 above the isotope-resolved threshold, and a
    non-zero but <1e-4 residual at exactly 0.29 eV, attributable to 70Ge alone.

    Reporting 'exactly zero above 0.29 eV' WITHOUT this reconciliation fails: the
    roadmap figure is the natural-mean-mass statement and the isotope-resolved
    threshold, set by the lightest isotope, sits higher.
    """
    zp = cs.isotope_zero_point_eV()
    assert zp["binding_isotope"] == "70Ge"
    assert zp["threshold_eV"] == pytest.approx(0.3067, rel=1e-3)
    assert zp["threshold_eV"] > zp["roadmap_stated_eV"]

    # exactly zero above the threshold -- 0.0, not "small"
    for T in (zp["threshold_eV"] * 1.0000001, 0.31, 0.5, 1.0):
        b = cs.truncation_bound(T)
        assert b["missing_total"] == 0.0
        assert b["bound_fraction"] == 0.0
        assert all(pi["kinematically_closed"] for pi in b["per_isotope"].values())

    # Non-zero but tiny at exactly the roadmap's 0.29 eV.
    #
    # MEASURED REFINEMENT OF PLANNING FINDING F2. F2 attributes the 0.29 eV
    # residual to 70Ge alone. It is not: FOUR of the five isotopes still have
    # E_min < 100 keV there (70, 72, 73, 74Ge); only 76Ge is closed. 70Ge
    # DOMINATES the residual (~71%) and is the isotope that sets the threshold,
    # but it does not exhaust it. Asserted here so the refinement cannot be lost.
    b29 = cs.truncation_bound(0.29)
    assert b29["missing_total"] > 0.0
    assert 0.0 < b29["bound_fraction"] < 1.0e-4
    for name in ("70Ge", "72Ge", "73Ge", "74Ge"):
        assert b29["per_isotope"][name]["missing"] > 0.0
        assert not b29["per_isotope"][name]["kinematically_closed"]
    assert b29["per_isotope"]["76Ge"]["missing"] == 0.0
    assert b29["per_isotope"]["76Ge"]["kinematically_closed"]
    assert b29["per_isotope"]["70Ge"]["missing"] / b29["missing_total"] > 0.5
    # The roadmap's 0.29 eV is very nearly 74Ge's OWN zero point, 0.290146 eV.
    assert zp["per_isotope_T_eV"]["74Ge"] == pytest.approx(0.29, abs=0.001)

    # the artifact agrees: every row above the threshold is exactly zero
    header, rows = trunc
    col = header.index("bound_fraction")
    above = rows[rows[:, 0] > zp["threshold_eV"], col]
    assert above.size > 0
    assert np.all(above == 0.0)


def test_flat_continuation_is_upper_bound():
    """test-flat-continuation-is-upper-bound. THE PHASE'S PRIMARY NON-IDENTITY
    DISCONFIRMING CHECK.

    The flat continuation bounds the missing rate from ABOVE only if Phi is
    non-increasing as E falls toward the 0.1 MeV table floor.  That is a property
    of the FROZEN TABLE, measured here from its own knots.  If Phi RISES toward the
    floor this test FAILS and CALC-17's upper-bound language must be WITHDRAWN, not
    restated with a wider tolerance.
    """
    s = cs.flux_floor_slope()
    assert s["floor_MeV"] == pytest.approx(0.1, rel=1e-12)
    assert np.all(s["dlogPhi_dlogE"] >= 0.0), (
        "Phi RISES as E falls toward the table floor: the flat continuation "
        "UNDER-estimates the missing flux and the <=0.81% figure is not an upper "
        "bound at all. Withdraw the bound language; do not restate it.")
    assert s["non_increasing_toward_floor"] is True
    # and the physically motivated E^2 continuation gives a STRICTLY smaller bound
    flat = cs.truncation_bound(FLOOR_eV, continuation="flat")["bound_fraction"]
    e2 = cs.truncation_bound(FLOOR_eV, continuation="E2")["bound_fraction"]
    assert 0.0 < e2 < flat


def test_emin_reconciliation():
    """test-emin-reconciliation. All three circulating values, with their masses
    named; the roadmap's 58.16 keV is REPRODUCED from the molar mass, not quoted."""
    r = cs.e_min_reconciliation(0.1)
    assert r["phase7_natural"]["E_min_keV"] == pytest.approx(58.19, abs=0.01)
    assert r["conventions_molar"]["E_min_keV"] == pytest.approx(
        ROADMAP_EMIN_100meV_keV, abs=0.01)
    assert r["ge74_only"]["E_min_keV"] == pytest.approx(58.70, abs=0.01)
    assert r["spread_relative"] < 0.01
    assert r["adopted"] == "phase7_natural"
    for key in ("phase7_natural", "conventions_molar", "ge74_only"):
        assert len(r[key]["source"]) > 30      # the mass is NAMED, not implied
        assert r[key]["M_MeV"] > 0.0
    # the adopted value is what cevns.E_min_MeV gives on the Phase-7 frozen mass
    assert r["phase7_natural"]["E_min_keV"] == pytest.approx(
        cevns.E_min_MeV(1.0e-4, cs.M_N_PHASE7_eV * 1e-6) * 1e3, rel=1e-12)


def test_table_not_extended():
    """test-table-not-extended (fp-extend-flux-table).

    Two halves: (a) the frozen table's DATA ROWS are byte-identical to the
    committed state and still floor at 0.1 MeV with 101 knots -- the provenance
    HEADER stamp is excluded because the suite's own flux regeneration rewrites it
    (pre-existing, documented churn, see tests/test_legacy_grid_disposition.py);
    (b) no code path in cevns_subev.py writes to, appends to, or synthesises a knot
    for any flux table, and the one place a sub-floor flux value appears is the
    single labelled continuation constant.
    """
    rel = "data/flux/reactor_flux_v1.0.csv"
    committed = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=_ROOT,
                               capture_output=True, text=True).stdout.splitlines()
    current = open(os.path.join(_ROOT, rel)).read().splitlines()
    strip = lambda ls: [l for l in ls if not l.startswith("#")]  # noqa: E731
    assert strip(committed) == strip(current), (
        "the frozen flux table's DATA changed -- fp-extend-flux-table")

    f = cevns.ReactorFlux()
    assert f.E.size == 101
    assert f.E.min() == pytest.approx(0.1, rel=1e-12)
    assert not np.any(f.E < 0.1)

    src = open(os.path.join(_ROOT, "src", "qpd_potential", "cevns_subev.py")).read()
    code = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith("#"))
    # (b1) the module opens exactly two things for writing, and both are its own
    #      artifacts/v2.0 outputs -- never a flux table.
    for m in re.finditer(r'open\(([^)]*)\)', code):
        args = m.group(1)
        if '"w"' in args or "'w'" in args or '"a"' in args or "'a'" in args:
            assert "flux" not in args.lower() and "data" not in args.lower(), (
                f"cevns_subev.py opens a data/flux path for writing: {args}")
    # (b2) no synthetic-knot / clamping / extrapolation idiom on the flux path
    for bad in ("np.append", "flux.E =", "flux.phi =", "np.clip",
                "extrapolate=True", "fill_value"):
        assert bad not in code, f"{bad} on the flux path"
    # (b3) Phi below the table floor exists ONLY inside the single labelled
    #      continuation helper: exactly one definition and one call site.
    assert code.count("def _continuation_phi") == 1
    assert code.count("_continuation_phi(") == 2   # the def line + one call
    # (b4) every ReactorFlux.flux() call in the module is at or above the floor:
    #      the only literal energies passed to it are the table floor itself and
    #      knots read back from the table.
    assert "flux.flux(FLUX_FLOOR_MeV)" in code
    assert "flux.flux(E)" in code                  # inside the tabulated integrand


def test_bound_uses_the_pipeline_cross_section():
    """The bound's denominator IS the pipeline's own rate, not a re-derivation.

    tabulated_total must equal cevns.differential_rate at the same T, otherwise the
    fraction is being formed against a different spectrum than the one the phase
    ships.
    """
    for T in (FLOOR_eV, 0.15, 1.0, 100.0):
        b = cs.truncation_bound(T)
        assert b["tabulated_total"] == pytest.approx(
            cevns.differential_rate(T * 1e-3), rel=1e-9)


# =========================================================================== #
# claim-plateau                                                               #
# =========================================================================== #
def test_plateau_value(plateau):
    """test-plateau-value. The analytic plateau is built from int Phi dE and the
    cross-section prefactor -- NOT by extrapolating dR/dT downward
    (fp-plateau-by-extrapolation) -- and dR/dT(floor) sits just BELOW it."""
    ap = cs.analytic_plateau()
    assert ap["plateau_cts_per_kg_day_keV"] == pytest.approx(PLANNING_PLATEAU, rel=2e-4)
    assert ap["integral_flux"] == pytest.approx(7.4958e12, rel=1e-3)

    r = cevns.differential_rate(FLOOR_eV * 1e-3)
    deficit = 1.0 - r / ap["plateau_cts_per_kg_day_keV"]
    assert 0.0 < deficit < PLATEAU_APPROACH_MAX_DEFICIT

    header, rows = plateau
    assert rows[0, header.index("T_eV")] == pytest.approx(FLOOR_eV, rel=1e-9)
    assert rows[0, header.index("deficit")] == pytest.approx(deficit, rel=1e-9)


def test_plateau_is_not_an_extrapolation_of_the_fold():
    """The plateau must NOT be dR/dT at the lowest bin dressed up.

    Independent construction: rebuilding the plateau by hand from int Phi and the
    prefactor reproduces analytic_plateau exactly, and it differs from dR/dT(floor)
    by the measured ~0.9% -- so agreement between them is evidence, not an identity.
    """
    ap = cs.analytic_plateau()
    hand = 0.0
    for iso in params.GE_ISOTOPES:
        M_GeV = iso.M_MeV * 1e-3
        Q_W = cevns.weak_charge(iso.Z, iso.N)
        pref = (params.G_F.value**2 * M_GeV / params.CEVNS_PREFACTOR_DENOM.value
                * Q_W**2 * params.HBARC2.value * 1e-6)
        hand += iso.abundance * params.GE_ATOMS_PER_KG.value * pref \
            * ap["integral_flux"] * 86400.0
    assert hand == pytest.approx(ap["plateau_cts_per_kg_day_keV"], rel=1e-12)
    assert ap["plateau_cts_per_kg_day_keV"] != cevns.differential_rate(FLOOR_eV * 1e-3)


def test_does_not_rise(plateau):
    """test-does-not-rise. Monotone non-increasing in T across the WHOLE window, and
    bounded above by the analytic plateau everywhere.

    A spectrum that RISES toward low T is the signature of power-law flux
    extrapolation below the table floor -- a failure, never a feature.
    """
    header, rows = plateau
    T = rows[:, header.index("T_eV")]
    y = rows[:, header.index("dRdT")]
    p = rows[0, header.index("analytic_plateau")]
    assert np.all(np.diff(y) <= 0.0), "dR/dT rises somewhere in the SC2 window"
    assert np.all(y < p), "dR/dT exceeds the analytic T->0 plateau"
    assert np.all(rows[:, header.index("loglog_slope")] <= 0.0)
    assert T[0] == pytest.approx(FLOOR_eV, rel=1e-9)


def test_does_not_fall_to_zero(plateau):
    """test-does-not-fall-to-zero. No zero bins, no order-of-magnitude neighbour
    discontinuity, and dR/dT(floor)/plateau > 0.9.

    A collapse at the bottom is a silently reached table floor -- the exact failure
    the Phase-10 raising interpolators were installed against.
    """
    header, rows = plateau
    y = rows[:, header.index("dRdT")]
    p = rows[0, header.index("analytic_plateau")]
    assert np.all(y > 0.0)
    assert y[0] / p > 0.9
    assert float(np.max(y[:-1] / y[1:])) < 10.0


def test_approaches_from_below(plateau):
    """test-approaches-from-below. The fractional deficit must SHRINK monotonically
    as T falls.

    A deficit that is FLAT in T would be a normalization offset masquerading as a
    kinematic approach; that is the competing explanation this test separates.
    """
    header, rows = plateau
    d = rows[:, header.index("deficit")]
    assert np.all(d > 0.0)
    assert np.all(np.diff(d) > 0.0), "the deficit does not shrink toward low T"
    assert d[0] == pytest.approx(0.0093, abs=0.002)
    # and it is NOT flat: the 10 eV end is an order of magnitude larger
    assert d[-1] / d[0] > 10.0


# =========================================================================== #
# claim-sc2-verdict                                                           #
# =========================================================================== #
def test_window_not_narrowed(plateau):
    """test-window-not-narrowed (fp-narrow-the-window). The emitted profile spans
    the FULL 0.0999350 -> 10 eV window SC2 states."""
    header, rows = plateau
    T = rows[:, header.index("T_eV")]
    assert T.min() == pytest.approx(FLOOR_eV, rel=1e-9)
    assert T.max() == pytest.approx(SC2_WINDOW_HI_eV, rel=1e-9)
    assert T.size >= 100


def test_sc2_deficits_are_the_measured_ones(plateau):
    """The five SC2 checkpoints, recomputed. These are the numbers the verdict
    rests on, so they are asserted rather than merely written into prose."""
    expected = {0.0999: 0.0093, 0.15: 0.0172, 0.29: 0.0394,
                1.0: 0.1282, 10.0: 0.4430}
    ap = cs.analytic_plateau()["plateau_cts_per_kg_day_keV"]
    for T, want in expected.items():
        got = 1.0 - cevns.differential_rate(T * 1e-3) / ap
        assert got == pytest.approx(want, rel=0.01), f"T={T} eV"


@pytest.mark.skipif(not os.path.exists(_GATES_MD), reason="gates report not yet written")
def test_sc2_adjudicated():
    """test-sc2-adjudicated. A verdict WORD with the measured 10 eV deficit beside
    it, plus every item deliv-gates-report.must_contain requires."""
    txt = open(_GATES_MD).read()
    assert "SUPERSEDED" in txt or "PASS" in txt
    assert "44.30" in txt or "44.3" in txt          # the measured 10 eV deficit
    for needle in ("58.19", "58.16", "58.7", "0.3067", "0.29",
                   "was NOT extended", "2372.3"):
        assert needle in txt, f"gates report is missing {needle!r}"
