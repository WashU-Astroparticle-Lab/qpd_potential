# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""VALD-02 acceptance suite: NUCLEUS (2019) Fig. 1 germanium reproduction.

Angloher et al. (NUCLEUS Collab.), Eur. Phys. J. C 79, 1018 (2019). Their Fig. 1
Ge curve is the closest published reactor Ge dR/dE_R on a pure nuclear-recoil
axis, so it anchors our fold with NO ionization-yield model in between (unlike
the CONUS+ check, which lives on the ionization scale).

Covers: their emission normalization reproduced from their own stated numbers
(~8e20 nubar/s per core); the prose-vs-geometry site-flux gap (fp-nucleus-3e12);
the scale and -- decisively -- the SHAPE agreement of our fold with their
digitized curve; and the sub-1.8-MeV toggle, which shows their flux model must
carry sub-IBD-threshold flux.

DECLARED GAP: the Tengblad(1989)/Guetlein(2013) flux shape they fold was not
machine-sourceable in-environment, so the Phase-2 flagship SHAPE is substituted.
Every absolute normalization factor (power, baselines, nubar/fission, MeV/fission)
is theirs. The residual ~9% scale offset is attributed to that substitution plus
~5% figure-digitization error; the flatness test is what carries the physics.
"""

from __future__ import annotations

import numpy as np

import pytest

from qpd_potential import cevns, params

# The fold is the expensive step; run each variant ONCE for the whole module.
_FULL = cevns.reproduce_nucleus_fig1(sub18=True)
_ABOVE18 = cevns.reproduce_nucleus_fig1(sub18=False)


@pytest.fixture(scope="module")
def full():
    return _FULL


@pytest.fixture(scope="module")
def above18():
    return _ABOVE18


# --------------------------------------------------------------------------- #
# test-nucleus-emission: their site flux from their own numbers                 #
# --------------------------------------------------------------------------- #


def test_nucleus_emission_normalization():
    """6 nubar/fission at 200 MeV and 4.25 GW_th reproduces their ~8e20 nubar/s."""
    n = cevns.nucleus_flux_normalization()
    # Paper Sect. 2: "about 8 x 10^20 nubar/s are produced by a 4.25 GW_th reactor".
    assert 7.8e20 < n["emission_per_core"] < 8.2e20, n["emission_per_core"]
    # Two cores at 72 m and 102 m -> point-source sum.
    assert 1.75e12 < n["site_flux"] < 1.90e12, n["site_flux"]
    # Powers are THERMAL; a GW_e slip would drop the flux ~3x (fp-gwe-gwth).
    assert params.NUCLEUS_CORE_POWER_GW.units == "GW_th"


def test_prose_site_flux_is_not_the_figure_normalization():
    """fp-nucleus-3e12: their prose 3e12 is 1.6x their own geometric site flux.

    Folding at the prose value overshoots Fig. 1 by ~50%. This is the regression
    that keeps the quoted number out of the fold.
    """
    n = cevns.nucleus_flux_normalization()
    assert 1.55 < n["prose_over_geometric"] < 1.75, n["prose_over_geometric"]
    # dR/dT is linear in the flux normalization, so the overshoot is exact.
    overshoot = _FULL["mean_ratio"] * n["prose_over_geometric"]
    assert overshoot > 1.35, overshoot


# --------------------------------------------------------------------------- #
# test-nucleus-scale / test-nucleus-shape                                      #
# --------------------------------------------------------------------------- #


def test_fig1_absolute_scale(full):
    """Under their assumptions we land within 15% of their published Ge curve."""
    assert 0.85 < full["mean_ratio"] < 1.15, full["mean_ratio"]


def test_fig1_shape_is_flat(full):
    """DECISIVE: the ours/theirs ratio is FLAT in T over 10-500 eV_nr.

    A flat ratio means the spectral SHAPE agrees and only overall normalization
    conventions can differ -- i.e. any residual is a normalization choice, not a
    cross-section, kinematics, or form-factor disagreement. Bounds are set well
    inside the >0.30/decade slope that the >=1.8-MeV-only variant produces.
    """
    assert full["max_dev_from_mean"] < 0.08, full["rows"]
    assert abs(full["ratio_slope_per_decade"]) < 0.10, full["ratio_slope_per_decade"]


def test_every_point_agrees_within_20_percent(full):
    for row in full["rows"]:
        assert 0.80 < row["ratio"] < 1.20, row


# --------------------------------------------------------------------------- #
# test-nucleus-sub18: their flux must extend below the IBD threshold            #
# --------------------------------------------------------------------------- #


def test_fig1_requires_sub_1p8_MeV_flux(full, above18):
    """Truncating at 1.8 MeV destroys the shape agreement -> their flux goes lower.

    The >=1.8 MeV part is IDENTICAL between the two variants, so the divergence
    below ~95 eV_nr isolates the sub-IBD-threshold flux. This is an independent
    confirmation of the paper's own claim (Sect. 6) that NUCLEUS "will probe the
    reactor anti-neutrino spectrum below 1.8 MeV".
    """
    # The truncated fold develops a strong ratio ramp; the full fold does not.
    assert above18["ratio_slope_per_decade"] > 0.25, above18["ratio_slope_per_decade"]
    assert above18["ratio_slope_per_decade"] > 5.0 * abs(
        full["ratio_slope_per_decade"]
    )
    # At the lowest recoil the truncated fold misses roughly half the rate.
    lo_full, lo_cut = full["rows"][0], above18["rows"][0]
    assert lo_full["T_eV"] == lo_cut["T_eV"] == 10.0
    assert lo_cut["ratio"] < 0.60, lo_cut
    assert 0.40 < 1.0 - lo_cut["ours"] / lo_full["ours"] < 0.60


def test_sub18_toggle_is_inert_above_the_kinematic_turn_on(full, above18):
    """Above ~95 eV_nr no neutrino below 1.8 MeV is kinematically allowed."""
    for rf, rc in zip(full["rows"], above18["rows"]):
        if rf["T_eV"] >= 100.0:
            assert rf["ours"] == pytest.approx(rc["ours"], rel=1e-12), (rf, rc)


# --------------------------------------------------------------------------- #
# test-nucleus-s2w: the Weinberg-angle systematic of this anchor                #
# --------------------------------------------------------------------------- #


def test_sin2thetaw_systematic_is_bounded_and_documented(full):
    """The paper states no sin^2 theta_W; the choice moves the rate ~5%.

    Q_W^2 factorizes, so the shift is exact and does NOT touch the locked
    project convention (0.2387). Direction matters: PDG on-shell 0.2312 would
    LOWER the rate, so it cannot close the residual -- it widens it.
    """
    f = full["s2w_0p2312_factor"]
    assert 0.93 < f < 0.97, f
    assert f < 1.0
    assert params.SIN2_THETA_W.value == 0.2387


def test_locked_convention_untouched_by_the_systematic():
    """sin2thetaw_rate_factor at the locked value must be exactly 1."""
    flux = cevns.nucleus_variant_flux()
    per_iso = cevns.differential_rate_per_isotope(0.1, flux, use_form_factor=True)
    assert cevns.sin2thetaw_rate_factor(
        params.SIN2_THETA_W.value, per_iso
    ) == pytest.approx(1.0, rel=1e-9)


# --------------------------------------------------------------------------- #
# digitized-reference integrity                                                #
# --------------------------------------------------------------------------- #


def test_digitized_fig1_is_sane():
    """The frozen Fig. 1 Ge curve is monotone-falling and spans the plotted range."""
    E, R = cevns.load_nucleus_fig1()
    assert len(E) > 250
    assert E.min() < 1.1 and E.max() > 1000.0
    assert np.all(np.diff(E) > 0)
    # Falling: allow pixel-level noise, but no sustained rise.
    assert np.mean(np.diff(R) <= 0) > 0.95
    # Endpoints bracket the decades actually drawn in the figure.
    assert 400.0 < R[0] < 600.0, R[0]
    assert R[-1] < 1.0, R[-1]
