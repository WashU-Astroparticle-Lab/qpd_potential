"""Phase-4 Plan 04-02, Task 1 unit tests: sourced gamma line/flux table, frozen
NIST XCOM Ge mu/rho, and the thin-target single-scatter bookkeeping.

Guards:
  * every intensity/flux row is SOURCED (provenance + uncertainty band)  -> fp-invented-flux
  * line ENERGIES match nuclear data                                     -> VALD-03 anchor
  * single-scatter on the ONE pinned mean chord ell_bar = 4V/S = 0.385 cm:
      mu*ell_bar ~= 0.117 @1 MeV, ~= 0.084 @2 MeV; double-scatter ~= 1.4%
  * the 0.2 cm normal-incidence mu*t ~= 0.06 is a labelled demo, NOT the rate path
  * Klein-Nishina sigma_KN -> Thomson limit; edge closed form (VALD-03 targets)
"""
import numpy as np
import pytest

from qpd_potential import compton_source as cs
from qpd_potential import wafer_geometry as g


# --------------------------------------------------------------------------- #
# Provenance completeness (fp-invented-flux)                                   #
# --------------------------------------------------------------------------- #
def test_flux_provenance_complete():
    """No un-sourced intensity or flux: every row carries provenance + a band."""
    lines = cs.load_gamma_lines()
    assert len(lines) >= 10
    for ln in lines:
        assert ln.p_gamma_source.strip()          # emission prob provenance
        assert ln.flux_source.strip()             # flux provenance
        assert ln.flux_cm2_s > 0.0
        assert 0.0 < ln.p_gamma <= 1.0
        assert ln.flux_unc_frac > 0.0             # explicit uncertainty band


def test_flux_anchors_are_cited_measurements():
    """The two absolute anchors trace to the cited LABChico measured spectrum."""
    lines = {(_round(ln.energy_keV)): ln for ln in cs.load_gamma_lines()}
    k40 = lines[1460.8]
    tl = lines[2614.5]
    assert "measured" in k40.flux_source.lower()
    assert k40.flux_cm2_s == pytest.approx(0.036, rel=1e-3)   # LABChico 40K anchor
    assert tl.flux_cm2_s == pytest.approx(0.0016, rel=1e-3)   # LABChico 208Tl anchor


def _round(x):
    return round(x, 1)


# --------------------------------------------------------------------------- #
# Line energies are fixed nuclear data (VALD-03 anchor)                        #
# --------------------------------------------------------------------------- #
def test_line_energies_nuclear_data():
    energies = {round(ln.energy_keV, 1) for ln in cs.load_gamma_lines()}
    for e in (1460.8, 2614.5, 583.2, 1764.5, 609.3, 1120.3, 351.9, 911.2):
        assert e in energies


def test_compton_edges_closed_form():
    """VALD-03 edge targets from E_edge = 2E^2/(m_e c^2 + 2E)."""
    assert float(cs.compton_edge_kev(1460.822)) == pytest.approx(1243.4, abs=1.0)
    assert float(cs.compton_edge_kev(2614.511)) == pytest.approx(2381.7, abs=1.0)
    assert float(cs.compton_edge_kev(1764.494)) == pytest.approx(1541.3, abs=1.0)


# --------------------------------------------------------------------------- #
# ONE pinned path length: Cauchy mean chord ell_bar = 4V/S                      #
# --------------------------------------------------------------------------- #
def test_ell_bar_is_pinned_mean_chord():
    assert cs.ELL_BAR_CM == pytest.approx(g.cauchy_mean_chord(), rel=1e-12)
    assert cs.ELL_BAR_CM == pytest.approx(0.385, abs=2e-3)   # 4V/S


def test_single_scatter_mean_chord():
    """mu*ell_bar ~8-12%/crossing on the mean chord; single-scatter dominance."""
    assert float(cs.optical_depth_mean_chord(1000.0)) == pytest.approx(0.117, abs=0.005)
    assert float(cs.optical_depth_mean_chord(2000.0)) == pytest.approx(0.084, abs=0.005)
    # interaction probability 8-15%/crossing across the line band.
    P1 = float(cs.interaction_prob(1000.0))
    P2 = float(cs.interaction_prob(2000.0))
    assert 0.08 < P1 < 0.15
    assert 0.06 < P2 < 0.12
    # double-scatter ~ (mu*ell_bar)^2 ~= 1.4% at 1 MeV -- << 1, single-scatter holds.
    assert float(cs.double_scatter_fraction(1000.0)) == pytest.approx(0.014, abs=0.003)
    assert float(cs.double_scatter_fraction(1000.0)) < 0.05


def test_normal_incidence_is_labelled_demo_not_rate_path():
    """mu*t (t=0.2 cm, normal incidence) ~= 0.06 -- optically-thin demo only.

    It must be SMALLER than mu*ell_bar (t < ell_bar), confirming the rate path
    length is the mean chord, not the normal-incidence thickness.
    """
    assert float(cs.optical_depth_normal_incidence(1000.0)) == pytest.approx(0.061, abs=0.005)
    assert cs.THICKNESS_CM < cs.ELL_BAR_CM
    assert float(cs.optical_depth_normal_incidence(1000.0)) < float(cs.optical_depth_mean_chord(1000.0))


# --------------------------------------------------------------------------- #
# Frozen NIST XCOM Ge mu/rho                                                    #
# --------------------------------------------------------------------------- #
def test_xcom_frozen_points_reproduced():
    """Log-log interpolation reproduces the four frozen NIST XCOM points exactly."""
    for e_mev, ref in [(0.6, 0.0745), (1.0, 0.0573), (1.25, 0.0510), (2.0, 0.0409)]:
        assert float(cs.mu_over_rho(e_mev * 1e3)) == pytest.approx(ref, rel=1e-6)


def test_xcom_extrapolation_monotone_and_reasonable():
    """Mild log-log extrapolation stays smooth and physical across the line band."""
    e = np.array([295.0, 351.9, 600.0, 1460.8, 2614.5])   # keV
    mor = np.asarray(cs.mu_over_rho(e))
    assert np.all(mor > 0)
    assert np.all(np.diff(mor) < 0)                        # mu/rho falls with E here
    assert 0.10 < mor[0] < 0.12                            # ~0.107 at 295 keV
    assert 0.034 < mor[-1] < 0.038                         # ~0.036 at 2614.5 keV


# --------------------------------------------------------------------------- #
# Klein-Nishina cross section                                                  #
# --------------------------------------------------------------------------- #
def test_sigma_kn_thomson_limit():
    """IDENTITY check: sigma_KN(E -> 0) -> Thomson 8 pi r_e^2 / 3."""
    assert float(cs.sigma_kn(1.0)) == pytest.approx(cs.SIGMA_THOMSON, rel=0.01)
    assert cs.SIGMA_THOMSON == pytest.approx(6.6524e-25, rel=1e-3)


def test_sigma_kn_1mev_literature():
    """sigma_KN(1 MeV) ~= 0.211 barn per electron (standard KN value)."""
    assert float(cs.sigma_kn(1000.0)) == pytest.approx(2.11e-25, rel=0.02)
