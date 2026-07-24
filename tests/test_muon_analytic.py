# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""The deterministic muon path must AGREE WITH THE MONTE CARLO where the MC can speak.

`muon_analytic.run_muon_analytic` replaces three sampling steps (entry face, chord,
Landau straggling) with the closed-form objects they sample from.  A smooth curve
proves nothing on its own -- a constant is perfectly smooth -- so correctness is
pinned independently of smoothness, and the two are asserted separately:

  * the CHORD LAW is checked against `wafer_geometry.sample_entry_and_chord`
    itself, not against a re-derivation of it;
  * the LANDAU CDF is the very table `sample_deposit` inverts, so an error in it
    is common to both paths and cannot hide in the comparison;
  * band integrals are compared to the frozen 1e9-sample MC artifact WITH the
    MC's own weight-variance errors.

DISCLOSED, NOT ASSERTED AWAY: below ~10 eV of deposit the two paths differ by up
to ~4x.  That is not treated as agreement.  The MC is unconverged there -- four
independent 1e8-sample seeds give the 0.1-1 eV band as 0.0057 / 0.0380 / 0.0172 /
0.0122 counts/kg/day, a 6.7x spread from 4-10 entries each -- and a positive
heavy-tailed weight estimator sits BELOW its own mean in most realizations, which
is the pattern observed.  `test_low_band_disagreement_is_disclosed` pins that
disagreement so it cannot silently disappear or silently grow.  The region is
also below the Landau-Vavilov validity floor and is 0.015% of the RoI budget.
"""
from __future__ import annotations

import csv
import os

import numpy as np
import pytest

from qpd_potential import muon_analytic as ma
from qpd_potential import muon_deposit as md
from qpd_potential import wafer_geometry as wg

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MC_CSV = os.path.join(_ROOT, "artifacts", "v2.0", "muon_dRdEdep_ext.csv")

#: Bands (eV of deposit) where the frozen 1e9 MC has enough weight to be a
#: reference at all. Below 10 eV it does not -- see the module docstring.
_TRUSTED_BANDS = [(10.0, 1e2), (1e2, 1e3), (1e3, 1e4), (1e4, 1e6), (1e6, 1e9)]


@pytest.fixture(scope="module")
def spec():
    return ma.run_muon_analytic("v2.0-ext")


@pytest.fixture(scope="module")
def mc():
    with open(_MC_CSV) as fh:
        rows = list(csv.DictReader(x for x in fh if not x.startswith("#")))
    g = lambda k: np.array([float(r[k]) for r in rows])  # noqa: E731
    E_keV = g("E_dep_keV[keV]")
    lE = np.log(E_keV)
    ed = np.empty(E_keV.size + 1)
    ed[1:-1] = np.exp(0.5 * (lE[:-1] + lE[1:]))
    ed[0] = E_keV[0] ** 2 / ed[1]
    ed[-1] = E_keV[-1] ** 2 / ed[-2]
    return {"E_eV": E_keV * 1e3,
            "y": np.nan_to_num(g("dRdEdep[counts/kg/day/keV]")),
            "err": np.nan_to_num(g("mc_err[counts/kg/day/keV]")),
            "w": np.diff(ed)}


def _band(y, w, E, lo, hi):
    k = (E >= lo) & (E < hi)
    return float((y[k] * w[k]).sum())


def _band_err(err, w, E, lo, hi):
    k = (E >= lo) & (E < hi)
    return float(np.sqrt(((err[k] * w[k]) ** 2).sum()))


# --------------------------------------------------------------------------- #
# The chord law, against the actual sampler                                    #
# --------------------------------------------------------------------------- #
def test_chord_law_reproduces_the_sampler():
    """claim-chord-exact. P(ell > t) from the closed form must match the
    empirical survival of `sample_entry_and_chord` across every decade that
    matters, including the grazing-corner tail that feeds the low-deposit bins."""
    rng = np.random.default_rng(20260723)
    n = 400_000
    theta = np.arccos(rng.random(n))
    phi = rng.uniform(0.0, 2.0 * np.pi, n)
    dirs = wg.direction_from_angles(theta, phi)
    ell = wg.sample_entry_and_chord(dirs, rng)

    absD = np.abs(dirs)
    with np.errstate(divide="ignore"):
        M = wg.EDGES[None, :] / absD
    fw = absD * wg.FACE_AREA[None, :]
    fp = fw / fw.sum(axis=1, keepdims=True)

    def survival(t):
        tot = np.zeros(n)
        for a in range(3):
            o = [j for j in range(3) if j != a]
            fb = np.clip(1.0 - t / M[:, o[0]], 0.0, None)
            fc = np.clip(1.0 - t / M[:, o[1]], 0.0, None)
            tot += fp[:, a] * np.where(t < M[:, a], fb * fc, 0.0)
        return float(tot.mean())

    for t in (1e-5, 1e-3, 1e-2, 0.1, 0.2, 1.0, 3.0):
        emp = float((ell > t).mean())
        assert survival(t) == pytest.approx(emp, abs=3e-3), f"chord survival at t={t}"


def test_chord_law_is_normalized(spec):
    """A sign or clip error here would rescale the whole spectrum WITHOUT
    showing up as noise, so the normalization is carried out of the run and
    asserted rather than trusted."""
    assert spec.chord_norm_max_dev < 5e-3


def test_atom_at_the_straight_through_chord_is_not_dropped():
    """The atom IS the MPV peak. For a near-vertical muon entering the 2 mm face
    it carries almost the entire probability; dropping it would delete the peak
    while leaving a perfectly smooth curve behind."""
    d = wg.direction_from_angles(np.array([0.02]), np.array([0.3]))
    absD = np.abs(d)[0]
    M = wg.EDGES / absD
    _, atom = ma.chord_law(np.array([M[2]]), np.array([M[0]]), np.array([M[1]]),
                           np.array([1e-6]))
    assert atom[0] > 0.99


# --------------------------------------------------------------------------- #
# Regime and normalization                                                     #
# --------------------------------------------------------------------------- #
def test_gaussian_branch_is_unreachable(spec):
    """muon_analytic implements only the Landau branch of `sample_deposit`.
    That is legitimate only while kappa stays below the Gaussian switch at 10."""
    assert spec.kappa_max < 10.0
    ma.assert_landau_regime(spec.kappa_max)          # must not raise
    with pytest.raises(RuntimeError):
        ma.assert_landau_regime(10.0)                 # and must bite when it should


def test_rate_matches_the_monte_carlo_and_pdg(spec):
    # Two independent estimators of the same 4-D integral.
    assert spec.rate_hz == pytest.approx(1.3659, rel=5e-3)
    # VALD-02: PDG sea-level 1.5-2 Hz, 30-35% Gaisser-Guan normalization spread.
    assert 0.9 < spec.rate_hz < 2.2


def test_energy_closure(spec):
    closure = spec.counts_per_kg_day / (spec.rate_hz * 86400.0 / wg.MASS_KG)
    assert closure == pytest.approx(1.0, abs=5e-3)


def test_vertical_mpv_is_the_pdg_anchored_value(spec):
    # Landau-Vavilov MPV on the 2 mm vertical chord, computed not memorized.
    assert spec.vertical_mpv_mev == pytest.approx(1.232, rel=5e-3)
    # Strictly below the mean loss -- fp-mean-not-mpv.
    assert spec.vertical_mpv_mev < spec.vertical_mean_mev


# --------------------------------------------------------------------------- #
# Agreement with the MC, where the MC can speak                                #
# --------------------------------------------------------------------------- #
def test_band_integrals_agree_where_the_mc_is_converged(spec, mc):
    """claim-analytic-equals-mc."""
    for lo, hi in _TRUSTED_BANDS:
        a = _band(spec.dRdE, mc["w"], mc["E_eV"], lo, hi)
        m = _band(mc["y"], mc["w"], mc["E_eV"], lo, hi)
        s = _band_err(mc["err"], mc["w"], mc["E_eV"], lo, hi)
        assert abs(a - m) < 4.0 * s, (
            f"band {lo}-{hi} eV: analytic {a:.6g} vs MC {m:.6g} +- {s:.3g}")


def test_total_integral_agrees_with_the_monte_carlo(spec, mc):
    a = float((spec.dRdE * mc["w"]).sum())
    m = float((mc["y"] * mc["w"]).sum())
    assert a == pytest.approx(m, rel=3e-3)


def test_low_band_disagreement_is_disclosed(spec, mc):
    """The 0.1-1 eV band DISAGREES with the frozen MC by roughly 4x.

    This is pinned, not hidden. It must not silently vanish (which would mean
    someone quietly reconciled the two paths) and must not silently grow past
    an order of magnitude (which would mean a real regression). See the module
    docstring for why the MC is not the reference in this band.
    """
    a = _band(spec.dRdE, mc["w"], mc["E_eV"], 0.1, 1.0)
    m = _band(mc["y"], mc["w"], mc["E_eV"], 0.1, 1.0)
    assert 2.0 < a / m < 10.0, f"disclosed low-band ratio moved: {a / m:.2f}"


# --------------------------------------------------------------------------- #
# The deliverable property, asserted separately from correctness               #
# --------------------------------------------------------------------------- #
def test_curve_is_smooth_where_the_mc_was_ragged(spec, mc):
    E = spec.centers_kev * 1e3

    def ragged(y, lo, hi):
        m = y > 0
        d2 = np.abs(np.diff(np.log(y[m]), 2))
        b = E[m][1:-1]
        s = (b >= lo) & (b < hi)
        return float(np.median(d2[s])) if s.sum() else np.nan

    for lo, hi in ((0.1, 1.0), (1.0, 10.0), (10.0, 100.0), (100.0, 1e3)):
        a = ragged(spec.dRdE, lo, hi)
        m = ragged(mc["y"], lo, hi)
        assert a < 1e-2, f"analytic ragged in {lo}-{hi} eV: {a}"
        assert a < m / 100.0, f"only {m / a:.0f}x smoother in {lo}-{hi} eV"


def test_every_bin_is_populated(spec):
    """The MC leaves 35 bins empty and writes NaN there. Deterministic
    evaluation has no empty bins to leave, which is why the plotted curve no
    longer has gaps."""
    assert np.all(np.isfinite(spec.dRdE))
    assert (spec.dRdE > 0).sum() == spec.dRdE.size


def test_quadrature_is_converged():
    """Every order is a knob; doubling them must not move the answer."""
    base = ma.run_muon_analytic("v2.0-ext")
    fine = ma.run_muon_analytic("v2.0-ext", n_e=192, n_theta=128, n_phi=48,
                                n_ell=512)
    assert fine.rate_hz == pytest.approx(base.rate_hz, rel=1e-4)
    E = base.centers_kev * 1e3
    w = np.diff(base.edges_kev)
    for lo, hi in [(0.1, 1.0)] + _TRUSTED_BANDS:
        b = _band(base.dRdE, w, E, lo, hi)
        f = _band(fine.dRdE, w, E, lo, hi)
        assert f == pytest.approx(b, rel=5e-3), f"band {lo}-{hi} eV not converged"
