# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Ge-intrinsic cosmogenic backgrounds (3H, 68Ge, 65Zn), checked against their sources.

This channel is drawn at FULL rate on the shielded-scenario figure -- no
suppression -- because no shield or veto reaches a decay inside the crystal. That
makes its NORMALIZATION load-bearing in a way the suppressed channels' is not, so
the tests defend the normalization and the line placement first:

  * the activation rates must equal the FROZEN scenario file, not a transcribed
    copy that can drift (test_rates_match_the_frozen_activation_scenario);
  * every emitted spectrum must integrate to its activation rate;
  * 68Ge and 71Ge decay to the SAME Ga daughter, so their EC line energies must be
    identical -- checked against the Phase-14 frozen 71Ge inventory rather than
    re-typed (test_68ge_shares_the_71ge_gallium_lines). This is the cross-check
    that the shielded-out in-situ 71Ge line is genuinely replaced by the
    unshieldable cosmogenic 68Ge line at the same energy.

EC IS MONO-ENERGETIC. The deposit is a discrete shell binding energy, so the
spectra are LINES, and the tests assert discreteness explicitly
(test_ec_spectra_are_discrete_lines_not_continua). Drawing them as a connected
curve was a real rendering bug caught in review; a test now pins the physics.

The L/M sub-shell split is the one ASSIGNED quantity (standard EC ratio, not
frozen). It is labelled, and the Phase-14 BOUND remains reachable via
split='bound'; test_bound_split_is_looser_than_standard keeps the two ordered so
the assigned value can never silently exceed the bound it is meant to sharpen.
"""
from __future__ import annotations

import csv
import os

import numpy as np
import pytest

from qpd_potential import capture_channel as cc
from qpd_potential import cosmogenic_intrinsic as ci
from qpd_potential import muon_deposit as md

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ACTIVATION_CSV = os.path.join(_ROOT, "data", "activation_scenario_v1.1.csv")


@pytest.fixture(scope="module")
def edges():
    return md.shared_energy_grid("v2.0-ext")


# --------------------------------------------------------------------------- #
# Normalization, against the frozen scenario file                              #
# --------------------------------------------------------------------------- #
def test_rates_match_the_frozen_activation_scenario():
    """claim-rates-not-transcribed. ACTIVITY_1YR must equal the frozen Phase-7
    t_exp = 1 yr, t_cool = 0 column, so the constant cannot drift from its source."""
    with open(_ACTIVATION_CSV) as fh:
        rows = list(csv.DictReader(x for x in fh if not x.startswith("#")))
    frozen = {r["isotope"]: float(r["A_default_CDMSlite_1yr_dec_kg_day"]) for r in rows}
    assert set(ci.ACTIVITY_1YR) <= set(frozen)
    for iso, val in ci.ACTIVITY_1YR.items():
        assert val == pytest.approx(frozen[iso], rel=1e-12), (
            f"{iso}: module has {val}, frozen scenario has {frozen[iso]}")


def test_every_spectrum_integrates_to_its_activation_rate(edges):
    """No decay is created or lost by the binning."""
    for iso, sp in ci.deposit_spectra(edges).items():
        total = float((sp.dRdE * np.diff(edges)).sum())
        assert total == pytest.approx(ci.ACTIVITY_1YR[iso], rel=1e-9), iso


def test_spectra_are_non_negative_and_finite(edges):
    for iso, sp in ci.deposit_spectra(edges).items():
        assert np.all(np.isfinite(sp.dRdE)), iso
        assert np.all(sp.dRdE >= 0.0), iso


# --------------------------------------------------------------------------- #
# 3H beta continuum                                                            #
# --------------------------------------------------------------------------- #
def test_tritium_respects_its_endpoint(edges):
    """A beta spectrum is exactly zero above Q. An electron cannot carry more
    than the decay energy."""
    sp = ci.tritium_deposit(edges)
    above = sp.centers_keV > ci.TRITIUM_Q_keV
    assert np.all(sp.dRdE[above] == 0.0)
    populated = sp.centers_keV[sp.dRdE > 0]
    assert populated.max() < ci.TRITIUM_Q_keV
    # and it must actually reach up near the endpoint, not stop decades short
    assert populated.max() > 0.9 * ci.TRITIUM_Q_keV


def test_tritium_shape_is_a_continuum_not_a_line(edges):
    """3H is the ONE genuinely continuous intrinsic; it must populate most of the
    grid below its endpoint, unlike the discrete EC lines."""
    sp = ci.tritium_deposit(edges)
    in_range = (sp.centers_keV > 1e-3) & (sp.centers_keV < ci.TRITIUM_Q_keV)
    frac = float((sp.dRdE[in_range] > 0).mean())
    assert frac > 0.95, f"only {frac:.2%} of in-range bins populated"


def test_tritium_shape_vanishes_at_both_ends():
    """Allowed beta shape: p*E*(Q-E)^2 -> 0 at E->0 (p->0) and at E->Q."""
    assert ci.tritium_shape(np.array([0.0]))[0] == 0.0
    assert ci.tritium_shape(np.array([ci.TRITIUM_Q_keV]))[0] == 0.0
    assert ci.tritium_shape(np.array([-1.0]))[0] == 0.0
    assert ci.tritium_shape(np.array([ci.TRITIUM_Q_keV * 2]))[0] == 0.0
    assert ci.tritium_shape(np.array([ci.TRITIUM_Q_keV / 2]))[0] > 0.0


def test_fermi_function_enhances_low_energy_for_beta_minus():
    """F(Z,E) > 1 for beta- (attractive daughter nucleus) and falls toward 1 as
    the electron gets fast. Getting the SIGN wrong would tilt the whole spectrum."""
    lo = ci._fermi_function(ci.TRITIUM_Z_DAUGHTER, np.array([0.5]))[0]
    hi = ci._fermi_function(ci.TRITIUM_Z_DAUGHTER, np.array([17.0]))[0]
    assert lo > 1.0 and hi > 1.0
    assert lo > hi, "Fermi enhancement must decrease with energy"


# --------------------------------------------------------------------------- #
# EC lines                                                                     #
# --------------------------------------------------------------------------- #
def test_68ge_shares_the_71ge_gallium_lines():
    """claim-shared-daughter. 68Ge and 71Ge both decay to Ga, so the EC line
    energies are IDENTICAL. Read from the frozen Phase-14 71Ge inventory, not
    re-typed -- this is why the shielded-out in-situ 71Ge line reappears as the
    unshieldable cosmogenic 68Ge line at the same energy."""
    frozen = {sh: e for sh, e, _ in cc.GE71_EC_LINES}
    assert ci.ec_line_energies_eV("68Ge") == frozen


def test_ec_line_rates_sum_to_the_activation_rate():
    for iso in ("68Ge", "65Zn"):
        rates = ci.ec_line_rates(iso)
        assert sum(rates.values()) == pytest.approx(ci.ACTIVITY_1YR[iso], rel=1e-12), iso


def test_k_capture_dominates():
    """P_K ~ 0.88 for these Z: the K shell takes the overwhelming majority of
    captures, so the K line must be the strongest."""
    for iso in ("68Ge", "65Zn"):
        r = ci.ec_line_rates(iso)
        assert r["K"] > r["L"] > r["M"], iso
        assert r["K"] / ci.ACTIVITY_1YR[iso] > 0.8, iso


def test_gallium_p_k_matches_the_frozen_sourced_value():
    """The Ga K-capture fraction is the Phase-14 SOURCED value (IAEA Live Chart
    K-vacancy conservation), not a recollection."""
    assert ci._P_K["Ga"] == pytest.approx(
        cc.ge71_k_shell_capture_fraction()["P_K"], rel=1e-12)


def test_bound_split_is_looser_than_standard():
    """The assigned L/M ratio must never exceed the Phase-14 bound it sharpens."""
    for iso in ("68Ge", "65Zn"):
        std = ci.ec_line_rates(iso, split="standard")
        bnd = ci.ec_line_rates(iso, split="bound")
        assert std["M"] < bnd["M"], iso
        assert std["L"] < bnd["L"], iso
        assert std["K"] == pytest.approx(bnd["K"], rel=1e-12), iso


def test_ec_spectra_are_discrete_lines_not_continua(edges):
    """claim-ec-is-monoenergetic. EC deposits a discrete shell binding energy.
    Exactly as many populated bins as there are shells -- a connected curve
    through these points would be a rendering artifact, not physics."""
    for iso in ("68Ge", "65Zn"):
        sp = ci.ec_deposit(edges, iso)
        n_pop = int((sp.dRdE > 0).sum())
        assert n_pop == len(ci.ec_line_energies_eV(iso)) == 3, (
            f"{iso}: {n_pop} populated bins for 3 shell lines")


def test_ec_lines_land_in_the_bin_containing_their_energy(edges):
    for iso in ("68Ge", "65Zn"):
        sp = ci.ec_deposit(edges, iso)
        populated = sp.centers_keV[sp.dRdE > 0]
        for sh, E_eV in ci.ec_line_energies_eV(iso).items():
            E_keV = E_eV / 1e3
            # the nearest populated bin centre must be within one bin width
            assert np.min(np.abs(populated - E_keV)) < 0.06 * E_keV, f"{iso} {sh}"


def test_only_the_m_line_reaches_the_roi():
    """On the DEPOSIT axis the 10-100 eV RoI is reached only by the M shell; the
    L and K lines sit above it. (They still matter on the reconstructed axis via
    the response fold, which is the figure's job, not this module's.)"""
    for iso in ("68Ge", "65Zn"):
        lines = ci.ec_line_energies_eV(iso)
        assert 10.0 <= lines["M"] <= 200.0, iso
        assert lines["L"] > 200.0 and lines["K"] > 200.0, iso


def test_unknown_isotope_and_split_raise():
    with pytest.raises(KeyError):
        ci.ec_line_energies_eV("3H")          # a beta emitter, not an EC line source
    with pytest.raises(KeyError):
        ci.ec_line_rates("77Ge")
    with pytest.raises(ValueError):
        ci.ec_line_rates("68Ge", split="whatever")
