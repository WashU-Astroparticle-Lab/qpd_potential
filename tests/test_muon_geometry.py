"""Phase-4 Plan 04-01, Task 1 unit tests: wafer geometry, ray-box chord sampler,
and the Gaisser-Guan surface-flux measure.

Guards:
  * Cauchy invariant <ell> = 4V/S           (chord sampler correctness)
  * chord range [0.20, 14.37] cm            (vertical / space-diagonal)
  * J_horiz = pi*I_v/2 for a cos^2 flux     (surface-flux measure, fp-angular-bias)
"""
import numpy as np
import pytest

from qpd_potential import muon_flux as mf
from qpd_potential import wafer_geometry as g


def test_geometry_constants():
    # Geometric volume from edges matches the locked params V within 0.1%.
    assert g.V_GEOM == pytest.approx(g.V_PARAMS, rel=2e-3)
    assert g.S_SURFACE == pytest.approx(214.6, rel=1e-3)
    assert g.CHORD_VERTICAL == pytest.approx(0.20, abs=1e-9)
    assert g.CHORD_DIAGONAL == pytest.approx(14.37, abs=0.02)
    assert g.cauchy_mean_chord() == pytest.approx(0.385, rel=2e-2)


def test_vertical_and_diagonal_chords():
    rng = np.random.default_rng(0)
    # Vertical muon -> chord = wafer thickness.
    D = g.direction_from_angles(np.array([0.0]), np.array([0.0]))
    ell = g.sample_entry_and_chord(D, rng)
    assert ell[0] == pytest.approx(0.20, abs=1e-6)
    # A near-horizontal ray entering the top face traverses nearly the full
    # in-plane extent -> a long chord in the tens-of-MeV-deposit tail.
    theta = np.array([np.deg2rad(89.2)])
    phi = np.array([0.0])
    Dd = g.direction_from_angles(theta, phi)  # mostly +x, slight -z
    O = np.array([[1e-6, 5.0, g.LZ - 1e-6]])
    ell_d = g.chord_lengths(O, Dd)
    assert ell_d[0] > 5.0  # clearly in the long-chord tail
    assert ell_d[0] <= g.CHORD_DIAGONAL + 1e-6


def test_cauchy_invariant():
    """Isotropic flux -> flux-weighted mean chord = 4V/S (Cauchy)."""
    rng = np.random.default_rng(20260720)
    ell, w = g.sample_isotropic_chords(2_000_000, rng)
    mean_chord = np.average(ell, weights=w)
    assert mean_chord == pytest.approx(g.cauchy_mean_chord(), rel=2e-2)
    # Upper chord bound = space diagonal. (There is no positive lower bound:
    # grazing rays that clip a corner give arbitrarily short chords.)
    assert ell.max() <= g.CHORD_DIAGONAL + 1e-6


def test_projected_area_vertical_is_top_face():
    D = g.direction_from_angles(np.array([0.0]), np.array([0.0]))
    assert g.projected_area(D)[0] == pytest.approx(g.LX * g.LY, rel=1e-9)


def test_jhoriz_surface_measure():
    """cos^2(theta) test flux -> top-face flux = pi*I_v/2 (guards fp-angular-bias).

    Sampling zenith from bare cos^2 (without the extra projection cos and the
    sin Jacobian) would fail this by ~30%.
    """
    Iv = 0.007  # cm^-2 s^-1 sr^-1  (I_v = 70 m^-2 s^-1 sr^-1)
    rng = np.random.default_rng(3)
    N = 3_000_000
    theta = rng.uniform(0.0, np.pi / 2.0, N)
    phi = rng.uniform(0.0, 2.0 * np.pi, N)
    cth = np.cos(theta)
    sth = np.sin(theta)
    D = g.direction_from_angles(theta, phi)
    intensity = Iv * cth**2
    # top-face-only projected area = A_z * |Omega_z|
    aproj_top = g.FACE_AREA[2] * np.abs(D[:, 2])
    q = (2.0 / np.pi) * (1.0 / (2.0 * np.pi))
    R_top = (intensity * aproj_top * sth / q).sum() / N
    J_mc = R_top / (g.LX * g.LY)
    assert J_mc == pytest.approx(np.pi * Iv / 2.0, rel=5e-2)


def test_gaisser_guan_vertical_intensity_anchor():
    """Gaisser-Guan I_v(>1 GeV) is O(70) m^-2 s^-1 sr^-1 (PDG anchor)."""
    Iv = mf.vertical_intensity(1.0)  # cm^-2 s^-1 sr^-1
    Iv_m2 = Iv * 1.0e4
    # PDG ~70; Gaisser-Guan gives ~60, well inside the 30-35% inter-experiment band.
    assert 45.0 < Iv_m2 < 90.0


def test_cos_theta_star_monotone():
    # cos(theta*) = 1 at vertical, decreases toward the horizon but stays > 0.
    assert mf.cos_theta_star(1.0) == pytest.approx(1.0, rel=1e-6)
    assert 0.0 < mf.cos_theta_star(1e-3) < mf.cos_theta_star(0.5) < 1.0
