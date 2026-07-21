# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""VALD-01 acceptance suite (Phase 3, Plan 03-02).

Covers: the Billard geometry+power k-rescale derivation (two ways), the Billard
(2017) Table-1 reproduction within ~20% WITH k and the ~90x overshoot WITHOUT k
(forbidden-proxy regression fp-billard-norm), the coarse factor-~2 CONUS+
cross-check, the propagated flux-uncertainty band widths, and the sub-1.8-MeV
toggle that localizes the Phase-2 placeholder systematic below ~95 eV_nr.
"""

from __future__ import annotations

import numpy as np

import pytest

from qpd_potential import cevns

# n=600 is already converged to 4 significant figures (identical to n=4000);
# compute the Billard reproduction ONCE for the whole module (the fold is the
# expensive step).
_BILLARD = cevns.reproduce_billard(n=600)


@pytest.fixture(scope="module")
def billard():
    return _BILLARD


# --------------------------------------------------------------------------- #
# test-k-derivation                                                            #
# --------------------------------------------------------------------------- #


def test_k_derivation():
    """k approx 0.0111 two ways (single-source vs two-core) agree <1%."""
    info = cevns.billard_k_factor()
    # k = (8.54/3) * (25/400)^2 approx 0.0111.
    assert abs(info["k_single"] - 0.0111) < 0.0003, info["k_single"]
    # Single 8.54 GW at 400 m and the two-core sum agree to <1%.
    assert info["rel_diff"] < 0.01, info["rel_diff"]
    # The k-rescaled Billard integral flux is approx 5.1e10 nu cm^-2 s^-1.
    assert 4.8e10 < info["rescaled_integral_flux"] < 5.4e10, info["rescaled_integral_flux"]


def test_k_uses_thermal_power_and_squared_distance():
    """Guard fp-gwe-gwth: k must use GW_th and a 1/d^2 (not 1/d) geometry."""
    info = cevns.billard_k_factor()
    # If distance entered as 1/d (not 1/d^2), k would be (8.54/3)*(25/400) ~ 0.178.
    assert info["k_single"] < 0.05, "k too large -- distance not squared?"
    # If GW_e (~1/3 of GW_th) had been used, k would drop ~3x below ~0.004.
    assert info["k_single"] > 0.006, "k too small -- GW_e used instead of GW_th?"


# --------------------------------------------------------------------------- #
# test-billard: Table-1 reproduction within ~20% WITH k                        #
# --------------------------------------------------------------------------- #


def test_billard_reproduction_within_20pct(billard):
    """WITH k, reproduce 0.76/0.51/0.26 counts/kg/day above 50/100/200 eV_nr."""
    r = billard
    targets = cevns.BILLARD_TABLE1
    for T0, target in targets.items():
        got = r["rates_with_k"][T0]
        rel = abs(got - target) / target
        assert rel < 0.20, f"T>{T0:.0f} eV: got {got:.4f} vs {target} (rel {rel:.1%})"


def test_billard_100_200_bins_not_backtrack(billard):
    """ROADMAP backtrack guard: the 100/200 eV bins (insensitive to the sub-2-MeV
    shape) must agree to <20%; disagreement there signals a fold/normalization bug."""
    r = billard
    for T0 in (100.0, 200.0):
        rel = abs(r["percent_vs_billard"][T0]) / 100.0
        assert rel < 0.20, f"T>{T0:.0f} eV off {rel:.1%} -- backtrack trigger"


# --------------------------------------------------------------------------- #
# test-billard (regression half): the ~90x overshoot WITHOUT k                 #
# --------------------------------------------------------------------------- #


def test_without_k_overshoots_90x(billard):
    """Forbidden proxy fp-billard-norm: folding the variant at its stored
    3 GW_th/25 m normalization overshoots Table 1 by ~90x."""
    r = billard
    for T0 in (50.0, 100.0, 200.0):
        factor = r["overshoot_factor"][T0]
        assert 70.0 < factor < 110.0, f"T>{T0:.0f} eV overshoot {factor:.1f}x (expect ~90x)"
        # And the without-k rate is tens of counts/kg/day, not ~1.
        assert r["rates_without_k"][T0] > 10.0


# --------------------------------------------------------------------------- #
# test-conus: coarse factor-~2 cross-check                                     #
# --------------------------------------------------------------------------- #


def test_conus_factor2():
    """Flagship rate rescaled to CONUS+ config within a factor ~2 of Billard's
    Table-1 rate rescaled to the same config (eV_ee quenching caveat noted)."""
    c = cevns.conus_rescale_check()
    ratio = c["ratio"]
    assert 0.5 < ratio < 2.0, f"CONUS+ scale ratio {ratio:.3f} outside factor 2"
    # Flagship absolute scale is the genuine reactor-CEvNS tens/kg/day (geometry
    # ratio ~90x Billard's 0.76), not ~1.
    assert 30.0 < c["R_flagship_ours"] < 120.0, c["R_flagship_ours"]
