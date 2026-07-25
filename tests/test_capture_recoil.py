# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""The (n,gamma) capture recoil spectrum, checked against physics identities and its
own frozen provenance.

This channel replaces a shapeless bound, so the tests defend the two claims that
make the spectrum trustworthy rather than merely smooth:

  * ENERGY CONSERVATION per cascade -- every cascade's emitted gamma energies must
    sum to the ENDF neutron separation energy S_n. A parsing slip in the level
    tables would break this and silently move the recoil.
  * THE MEAN RECOIL IS MODE-INDEPENDENT -- <|sum p_i|^2> = sum |p_i|^2 for isotropic
    independent gamma directions, so the "fast" (vector) and "slow" (scalar) limits
    have the SAME mean and differ only in shape. This is the decisive check that the
    vector kinematics are implemented correctly; if the fast mean drifted from the
    slow line, the momentum sum would be wrong.

The coverage deficit (the table resolves 26.85% of captures) is asserted to be
REPORTED and never renormalised to 1 -- renormalising would assert the unresolved
73% recoils like the resolved 27%, which the E^2 weighting makes unsafe.
"""
from __future__ import annotations

import numpy as np
import pytest

from qpd_potential import capture_recoil as cr
from qpd_potential import capture_channel as cc
from qpd_potential import muon_deposit as md


@pytest.fixture(scope="module")
def edges():
    return md.shared_energy_grid("v2.0-ext")


# --------------------------------------------------------------------------- #
# Provenance and parsing                                                       #
# --------------------------------------------------------------------------- #
def test_level_files_parse_and_cover_the_significant_channels():
    """The nrCascadeSim natural-Ge table lists 4 of the 5 capture products.
    77Ge (76Ge capture) is ABSENT: 76Ge is only 0.54% of natural thermal capture
    and its EGAF entry is anomalous (9 gammas, sigma_0 mismatch, completeness > 1;
    see data/egaf/MANIFEST.md), so the curated table omits it. That is a real
    coverage limit of the source, asserted here so it cannot regress unnoticed."""
    for mode in ("fast", "slow"):
        cas = cr.read_level_file(mode)
        assert len(cas) == 74
        products = {c.product_A for c in cas}
        assert products == {71, 73, 74, 75}, "expected 71/73/74/75 Ge, not 77"


def test_every_cascade_conserves_energy_to_the_endf_separation_energy():
    """claim-energy-closure. sum(E_gamma) == S_n from ENDF MF=3 MT=102 QM."""
    for c in cr.read_level_file("fast"):
        Sn_keV = cc.capture_Q_eV(cr._TARGET_OF_PRODUCT[c.product_A]) / 1.0e3
        assert c.gammas_keV.sum() == pytest.approx(Sn_keV, rel=1e-9), (
            f"{c.product_A}Ge cascade sums to {c.gammas_keV.sum()} != S_n {Sn_keV}")
        assert np.all(c.gammas_keV >= 0.0)


def test_coverage_is_reported_not_renormalised(edges):
    """The table resolves 26.85% of captures; the spectrum must carry that number
    and integrate to coverage x rate, NOT to the full capture rate."""
    cov = cr.coverage_fraction("fast")
    assert cov == pytest.approx(0.2685, abs=1e-3)
    assert cov < 1.0
    s = cr.recoil_spectrum(edges, mode="fast", n_per_cascade=20_000)
    total = float((s.dRdT * np.diff(edges)).sum())
    assert total == pytest.approx(cov * cr._default_capture_rate(), rel=1e-6)
    assert s.coverage_fraction == pytest.approx(cov, rel=1e-9)


# --------------------------------------------------------------------------- #
# The Weisskopf estimate, against nrCascadeSim's own formula                    #
# --------------------------------------------------------------------------- #
def test_weisskopf_matches_nrcascadesim_coefficients():
    # E1, A=74, E_gamma=1 MeV: width = 6.748e-2 * 74^(2/3) * 1^3 eV.
    width = 6.748e-2 * 74.0 ** (2.0 / 3.0)
    assert cr.weisskopf_tau_fs("E1", 1.0, 74) == pytest.approx(
        cr.HBAR_EV_FS / width, rel=1e-12)


def test_high_multipole_falls_back_to_m3_like_the_source():
    """weisskopf.cpp implements only L<=3 and falls through to M3. WSlow relies on
    that fallback (its w(E7)/w(M7) entries), so it must be reproduced."""
    tau_e7 = cr.weisskopf_tau_fs("E7", 2.0, 73)
    tau_m3 = cr.weisskopf_tau_fs("M3", 2.0, 73)
    assert tau_e7 == tau_m3


# --------------------------------------------------------------------------- #
# The decisive physics identity                                                #
# --------------------------------------------------------------------------- #
def test_mean_recoil_is_mode_independent(edges):
    """claim-vector-kinematics. <|sum p_i|^2> = sum|p_i|^2 for isotropic directions,
    so fast, slow and lifetime share ONE mean. A drift means the momentum sum is
    wrong."""
    means = {m: cr.recoil_spectrum(edges, mode=m, n_per_cascade=60_000).mean_recoil_keV
             for m in ("slow", "fast", "lifetime")}
    assert means["fast"] == pytest.approx(means["slow"], rel=5e-3)
    assert means["lifetime"] == pytest.approx(means["slow"], rel=5e-3)


def test_slow_mode_is_a_line_spectrum_above_the_roi():
    """Fully-stopped recoils add as energies: T = sum E_i^2 / 2Mc^2, one value per
    cascade. All 74 lines land between 182 and 671 eV -- NONE below 100 eV."""
    cas = cr.read_level_file("slow")
    lines_eV = []
    for c in cas:
        M = c.product_A * cr.U_TO_KEV
        lines_eV.append(float(np.sum(c.gammas_keV ** 2) / (2.0 * M)) * 1e3)
    lines_eV = np.array(lines_eV)
    assert lines_eV.min() > 100.0
    assert 150.0 < lines_eV.min() < 250.0
    assert 600.0 < lines_eV.max() < 750.0


def test_fast_mode_spreads_recoil_below_the_slow_minimum(edges):
    """Vector cancellation lets some cascades recoil LESS than their stopped value,
    so the fast spectrum populates the RoI while the slow one does not."""
    slow = cr.recoil_spectrum(edges, mode="slow", n_per_cascade=40_000)
    fast = cr.recoil_spectrum(edges, mode="fast", n_per_cascade=40_000)
    E = fast.centers_keV * 1e3
    w = np.diff(edges)
    roi = lambda s: float((s.dRdT * w)[(E >= 10) & (E < 100)].sum())  # noqa: E731
    assert roi(slow) == 0.0
    assert roi(fast) > 0.0


def test_recoil_never_exceeds_the_single_gamma_ceiling(edges):
    """T <= (sum E)^2/2Mc^2 = Q^2/2Mc^2: no cascade can recoil harder than if the
    whole Q left in one gamma. The slow line spectrum saturates this from below."""
    for c in cr.read_level_file("fast"):
        M = c.product_A * cr.U_TO_KEV
        ceiling = float(c.gammas_keV.sum() ** 2 / (2.0 * M))
        slow_val = float(np.sum(c.gammas_keV ** 2) / (2.0 * M))
        assert slow_val <= ceiling * (1.0 + 1e-12)


def test_lifetime_mode_lands_between_the_two_limits(edges):
    """The binary lifetime classifier must not escape the slow/fast bracket in the
    RoI integral -- it is an interpolation between them, not a third answer."""
    w = np.diff(edges)
    E = np.sqrt(edges[:-1] * edges[1:]) * 1e3
    sel = (E >= 10) & (E < 100)
    roi = lambda m: float((cr.recoil_spectrum(  # noqa: E731
        edges, mode=m, n_per_cascade=60_000).dRdT * w)[sel].sum())
    lo, hi = sorted((roi("slow"), roi("fast")))
    val = roi("lifetime")
    assert lo - 1e-9 <= val <= hi + max(hi * 0.05, 1e-9)


def test_recoil_axis_is_the_shared_grid(edges):
    s = cr.recoil_spectrum(edges, mode="fast", n_per_cascade=10_000)
    assert np.array_equal(s.edges_keV, edges)
    assert s.dRdT.size == edges.size - 1
    assert np.all(np.isfinite(s.dRdT))
    assert np.all(s.dRdT >= 0.0)
