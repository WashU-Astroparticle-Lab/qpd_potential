"""Phase-4 Plan 04-01, Task 2 unit tests: Landau-Vavilov MPV deposit and the
muon dR/dE_dep assembly with the VALD-02 integral-rate check.

Guards:
  * xi(vertical, x~=1.065 g/cm^2) ~= 0.072 MeV   (mass-thickness units, Pitfall 4)
  * MPV Delta_p strictly below the mean deposit   (mean-vs-MPV, fp-mean-not-mpv)
  * sampled Landau mode = Delta_p, heavy tail      (Landau, NOT Moyal)
  * integral muon rate ~1.5-2 Hz within ~30%       (VALD-02)
  * tens-of-MeV long-chord tail present            (Phase-5 saturation input)
  * convergence < 5% under 2x samples; energy closure
"""
import numpy as np
import pytest

from qpd_potential import muon_deposit as md
from qpd_potential import wafer_geometry as g


X_VERT = md.RHO * g.CHORD_VERTICAL  # ~1.065 g/cm^2
MEAN_VERT = md.DEDX_MEAN * X_VERT   # ~1.459 MeV


def test_xi_vertical_mass_thickness():
    """xi for the vertical chord matches the PDG value -> mass-thickness units OK."""
    bg = md.beta_gamma(np.array([4.0]))  # ~MIP muon
    _, xi = md.mpv_deposit(np.array([X_VERT]), bg)
    assert xi[0] == pytest.approx(0.072, abs=0.003)
    # Feeding ell[cm] instead of x[g/cm^2] would be off by rho ~ 5.3.
    _, xi_wrong = md.mpv_deposit(np.array([g.CHORD_VERTICAL]), bg)
    assert xi_wrong[0] < 0.02  # the (wrong) cm-based value is ~5x too small


def test_mpv_below_mean_formula():
    """PDG Delta_p is strictly below the mean <dE/dx>*x (highly skewed Landau)."""
    for E in (1.0, 4.0, 100.0):
        bg = md.beta_gamma(np.array([E]))
        dp, _ = md.mpv_deposit(np.array([X_VERT]), bg)
        assert 0.0 < dp[0] < MEAN_VERT
        assert dp[0] == pytest.approx(1.23, abs=0.15)  # computed, not memorized


def test_kappa_in_landau_regime():
    """kappa = xi/T_max << 10 for all wafer chords -> Landau/mild-Vavilov, not
    Gaussian; even the longest chord at the lowest MIP energy stays < 0.1."""
    bg = md.beta_gamma(np.array([1.0, 1.0, 4.0]))
    x = md.RHO * np.array([g.CHORD_VERTICAL, g.CHORD_DIAGONAL, g.CHORD_DIAGONAL])
    kap = md.kappa(x, bg)
    assert np.all(kap < 10.0)
    assert kap[0] < 1e-2          # vertical -> Landau
    assert kap[1] < 0.1           # longest chord, lowest E -> mild Vavilov


def test_landau_sampler_mode_and_tail():
    """Custom Landau sampler: mode at Delta_p, heavy (non-Moyal) high tail."""
    rng = np.random.default_rng(7)
    n = 2_000_000
    x = np.full(n, X_VERT)
    bg = md.beta_gamma(np.full(n, 4.0))
    dep = md.sample_deposit(x, bg, rng)
    dp, xi = md.mpv_deposit(np.array([X_VERT]), md.beta_gamma(np.array([4.0])))
    dp = dp[0]

    hist, be = np.histogram(dep, bins=400, range=(0.3, 2.5))
    bc = 0.5 * (be[1:] + be[:-1])
    mode = bc[np.argmax(np.convolve(hist, np.ones(7) / 7.0, mode="same"))]
    assert mode == pytest.approx(dp, abs=0.08)          # mode = MPV
    # Landau skew: mean > median > mode; heavy tail (a Moyal/Gaussian would not
    # push several percent of events past mode + 5*xi).
    assert np.median(dep) > mode
    assert dep.mean() > np.median(dep)
    assert (dep > dp + 5.0 * xi[0]).mean() > 0.02


def test_standard_landau_sampler():
    """The custom Landau sampler reproduces the standard-Landau shape: median at
    the tabulated value, mode near lambda = -0.22278, and a heavy positive tail.

    (The mode is read from a smoothed histogram: the Landau peak is broad on the
    left, so a raw argmax is bin-noise sensitive.)
    """
    rng = np.random.default_rng(1)
    lam = md.sample_standard_landau(rng.random(3_000_000))
    # Robust shape anchor: the standard-Landau median is ~1.355 (heavy tail
    # pulls the median well above the mode) -- reproduces the table quantile.
    assert np.median(lam) == pytest.approx(1.355, abs=0.05)
    # Smoothed mode near -0.22278.
    hist, be = np.histogram(lam, bins=200, range=(-1.0, 1.0))
    bc = 0.5 * (be[1:] + be[:-1])
    mode = bc[np.argmax(np.convolve(hist, np.ones(9) / 9.0, mode="same"))]
    assert mode == pytest.approx(-0.22278, abs=0.07)
    # Heavy (non-Moyal/Gaussian) tail: several percent of samples beyond lambda=5.
    assert (lam > 5.0).mean() > 0.03


def test_vald02_integral_rate():
    """VALD-02: integral muon rate ~1.5-2 Hz, within ~30% of the PDG anchor."""
    spec = md.run_muon_mc(n_samples=800_000, seed=20260720)
    assert 1.05 < spec.rate_hz < 2.0                     # within 30% of 1.5-2 Hz
    assert spec.rate_hz == pytest.approx(1.6, rel=0.30)


def test_sampled_vertical_mpv_below_mean():
    """Sampled near-vertical MPV matches the formula and lies below the mean."""
    spec = md.run_muon_mc(n_samples=800_000, seed=20260720)
    assert spec.vertical_mpv_mev < spec.vertical_mean_mev
    assert spec.vertical_mpv_mev == pytest.approx(1.23, abs=0.15)
    assert spec.vertical_mean_mev == pytest.approx(1.46, abs=0.02)


def test_high_energy_tail_present():
    """Long near-horizontal chords populate the tens-of-MeV deposit tail."""
    spec = md.run_muon_mc(n_samples=800_000, seed=20260720)
    c, y = spec.centers_kev, spec.dRdE
    assert (y[c > 3.0e4] > 0).sum() > 5      # non-empty bins above 30 MeV
    assert c[y > 0].max() > 5.0e4            # deposits reach > 50 MeV


def test_convergence_and_energy_closure():
    """Rate stable < 5% under 2x samples; spectrum integrates to the total rate."""
    s1 = md.run_muon_mc(n_samples=500_000, seed=11)
    s2 = md.run_muon_mc(n_samples=1_000_000, seed=11)
    rel = abs(s1.rate_hz - s2.rate_hz) / s2.rate_hz
    assert rel < 0.05
    # energy closure: int dR/dE_dep dE = rate * 86400 / mass_kg  (counts/kg/day)
    integral = (s2.dRdE * np.diff(s2.edges_kev)).sum()
    expected = s2.rate_hz * 86400.0 / g.MASS_KG
    assert integral == pytest.approx(expected, rel=1e-3)
