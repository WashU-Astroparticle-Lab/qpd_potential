# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""The deterministic Compton path must AGREE WITH THE MONTE CARLO, not replace it.

`compton_deposit.run_compton_analytic` evaluates dsigma/dT_e in closed form so the
emitted spectrum carries no sampling scatter.  A noise-free curve is worthless if it
is noise-free about the WRONG mean, and the closed-form change of variable
(cos theta -> T_e) is exactly the step the Monte-Carlo path was written to avoid.
So the analytic curve is checked against the frozen MC artifact as data:

  * bin-by-bin PULL, (analytic - MC)/mc_err, must look like a unit Gaussian.  A
    pull spread far below 1 would mean the "agreement" is trivial (e.g. both
    paths collapsed to the same wrong constant); far above 1 means a real
    discrepancy.  Both directions fail.
  * the integral, the per-line rates and the Compton edges must match the frozen
    header values, which were produced by the MC path.

The smoothness assertion is deliberately SEPARATE from the agreement assertion.
Smoothness alone is not evidence of correctness -- that is the whole trap here.
"""
from __future__ import annotations

import csv
import os

import numpy as np
import pytest

from qpd_potential import compton_deposit as cd
from qpd_potential import compton_source as cs

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MC_CSV = os.path.join(_ROOT, "artifacts", "v2.0", "compton_dRdEdep_ext.csv")

#: Bins with very few MC entries have an unreliable sqrt(N) error, so the pull is
#: not meaningful there. 25 entries is where the Poisson error is within ~20% of
#: Gaussian. This threshold selects WHICH bins the pull test can speak about; it
#: is not a tolerance on the physics.
_MIN_MC_ENTRIES = 25


@pytest.fixture(scope="module")
def analytic():
    return cd.run_compton_analytic("v2.0-ext")


@pytest.fixture(scope="module")
def mc_table():
    with open(_MC_CSV) as fh:
        rows = list(csv.DictReader(x for x in fh if not x.startswith("#")))
    g = lambda k: np.array([float(r[k]) for r in rows])  # noqa: E731
    return {"E_keV": g("E_dep_keV[keV]"),
            "y": g("dRdEdep[counts/kg/day/keV]"),
            "err": g("mc_err[counts/kg/day/keV]"),
            "n": g("mc_entries[raw count]")}


def test_analytic_lands_on_the_same_grid(analytic, mc_table):
    assert analytic.centers_kev.size == mc_table["E_keV"].size == 744
    assert np.abs(mc_table["E_keV"] / analytic.centers_kev - 1).max() < 1e-8


def test_pull_against_mc_is_a_unit_gaussian(analytic, mc_table):
    """claim-analytic-equals-mc. The decisive check."""
    k = ((mc_table["y"] > 0) & (mc_table["err"] > 0) & (analytic.dRdE > 0)
         & (mc_table["n"] >= _MIN_MC_ENTRIES))
    assert k.sum() > 300, f"only {k.sum()} bins usable for the pull test"
    pull = (analytic.dRdE[k] - mc_table["y"][k]) / mc_table["err"][k]

    # Centred: no systematic offset between the two evaluations.
    assert abs(pull.mean()) < 0.20, f"pull mean {pull.mean():+.3f}"
    # Spread consistent with unity IN BOTH DIRECTIONS. The lower bound is the
    # one that catches a vacuous pass.
    assert 0.6 < pull.std() < 1.6, f"pull std {pull.std():.3f}"
    # Heavy tails are expected at the 16 Compton edges (the MC's rejection
    # sampler resolves a step across a bin), but they must stay rare.
    assert (np.abs(pull) > 3).sum() <= 0.05 * k.sum()


def test_integral_and_rates_match_the_frozen_mc_header(analytic):
    # Values carried in artifacts/v2.0/compton_dRdEdep_ext.csv, produced by the MC.
    assert analytic.rate_hz == pytest.approx(2.6747e-01, rel=1e-3)
    assert analytic.counts_per_kg_day == pytest.approx(2.1028e05, rel=1e-3)
    # Energy closure: integral dR/dE_dep dE == rate * 86400 / mass.
    closure = analytic.counts_per_kg_day / (analytic.rate_hz * 86400.0 / cs.MASS_KG)
    assert closure == pytest.approx(1.0, abs=2e-3)


def test_compton_edges_are_reproduced_not_asserted(analytic):
    """VALD-03 carried over. The edge still falls out of the kinematics: the
    highest bin carrying non-zero probability must sit just ABOVE the analytic
    edge (same bin), never below it and never a bin away."""
    for e_gamma, e_edge, e_top in zip(analytic.line_energies,
                                      analytic.line_edges,
                                      analytic.line_edges_sampled):
        assert e_top >= e_edge, f"line {e_gamma}: support ends below its edge"
        assert e_top / e_edge < 1.03, f"line {e_gamma}: support overruns its edge"


def test_no_signal_above_the_highest_edge(analytic):
    """fp-full-absorption / fp-electron-not-photon. There is no photopeak: the
    spectrum must be identically zero above the largest Compton edge."""
    top = float(np.max(analytic.line_edges))
    above = analytic.centers_kev > top * 1.03
    assert np.all(analytic.dRdE[above] == 0.0)


def test_analytic_curve_is_smooth_where_the_mc_was_not(analytic, mc_table):
    """The DELIVERABLE property, asserted separately from correctness.

    Raggedness = median |second difference of log y| over populated bins. Below
    1 keV the MC is dominated by sampling scatter; the analytic curve must be
    orders of magnitude smoother there. Compton has REAL curvature (the S(x,Z)
    binding roll-off), so this is not asserted to be zero.
    """
    E_eV = analytic.centers_kev * 1e3

    def raggedness(y, lo, hi):
        m = y > 0
        d2 = np.abs(np.diff(np.log(y[m]), 2))
        band = E_eV[m][1:-1]
        sel = (band >= lo) & (band < hi)
        return float(np.median(d2[sel])) if sel.sum() else np.nan

    for lo, hi in ((0.1, 1.0), (1.0, 10.0), (10.0, 100.0)):
        a = raggedness(analytic.dRdE, lo, hi)
        m = raggedness(mc_table["y"], lo, hi)
        assert a < 1e-3, f"analytic ragged in {lo}-{hi} eV: {a}"
        assert a < m / 50.0, f"analytic only {m / a:.1f}x smoother in {lo}-{hi} eV"


def test_dsigma_dT_is_zero_outside_the_kinematic_support(analytic):
    e_gamma = 1460.822
    edge = float(cs.compton_edge_kev(e_gamma))
    probe = np.array([-1.0, 0.0, edge * 1.001, e_gamma, e_gamma * 2.0])
    assert np.all(cd.dsigma_dT_incoh(e_gamma, probe) == 0.0)
    inside = cd.dsigma_dT_incoh(e_gamma, np.array([edge * 0.5]))
    assert inside[0] > 0.0


def test_dsigma_dT_integrates_to_the_same_total_cross_section():
    """The change of variable must CONSERVE the normalization: integrating
    dsigma/dT over the support has to return sigma_incoh_atom, which the angular
    integral computes independently."""
    for e_gamma in (242.0, 1460.822, 2614.511):
        edge = float(cs.compton_edge_kev(e_gamma))
        t = np.linspace(1e-9, edge, 400_001)
        got = float(np.trapz(cd.dsigma_dT_incoh(e_gamma, t), t))
        want = cd.sigma_incoh_atom(e_gamma)
        assert got == pytest.approx(want, rel=2e-3), f"line {e_gamma}"
