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


# --------------------------------------------------------------------------- #
# test-band: flux-uncertainty band widths + sub-1.8-MeV toggle                 #
# --------------------------------------------------------------------------- #
#
# HONEST FINDING (surfaced to the orchestrator): the plan's claim-band guessed a
# "wide 20-25%" propagated band below ~95 eV_nr. The rigorous flux-weighted 1-sigma
# propagation does NOT reach 20-25% -- it is ~3.4% above 200 eV, rising to ~6% at
# 50 eV and ~10% at 20 eV -- because the well-anchored (2-5%) >1.8 MeV flux
# dominates the RATE integrand at every recoil energy; the sub-1.8-MeV placeholder
# is only 18% (50 eV) to 34% (20 eV) of the rate. The QUALITATIVE claim holds
# (band widens below ~95 eV, narrow above ~200 eV; the sub-1.8 sensitivity is
# localized below ~95 eV), so these tests assert the TRUE behavior, not the guessed
# magnitude. (No fp-hide-band: both the band AND the sub-1.8 fraction are reported.)


def test_band_narrow_above_200eV():
    """Propagated 1-sigma band is narrow (2-5%) for T >~ 200 eV_nr."""
    f = cevns.ReactorFlux()
    for T_eV in (200.0, 300.0, 500.0, 1000.0):
        b = cevns.fractional_band(T_eV * 1e-3, f)
        assert 0.02 <= b <= 0.06, f"T={T_eV:.0f} eV band {b:.3f} not in narrow 2-5%"


def test_band_widens_below_95eV():
    """Band widens monotonically as T drops below the ~95 eV_nr boundary."""
    f = cevns.ReactorFlux()
    b20 = cevns.fractional_band(0.020, f)
    b50 = cevns.fractional_band(0.050, f)
    b200 = cevns.fractional_band(0.200, f)
    assert b50 > b200, f"band not wider at 50 eV ({b50:.3f}) than 200 eV ({b200:.3f})"
    assert b20 > b50, f"band not wider at 20 eV ({b20:.3f}) than 50 eV ({b50:.3f})"
    # The widening is real but modest (does NOT reach 20-25%; documented finding).
    assert b50 < 0.15


def test_sub18_toggle_localized_below_95eV():
    """Zeroing flux below 1.8 MeV changes T<95 eV bins substantially and leaves
    T>200 eV bins essentially unchanged (E_min(95 eV) approx 1.78 MeV)."""
    f = cevns.ReactorFlux()
    # Below 95 eV: substantial sub-1.8-MeV weight in the rate.
    assert cevns.sub18_sensitivity_fraction(0.020, f) > 0.25
    assert cevns.sub18_sensitivity_fraction(0.050, f) > 0.10
    # At/above the boundary: negligible (well-anchored >1.8 MeV flux only).
    assert cevns.sub18_sensitivity_fraction(0.095, f) < 1e-2
    for T_eV in (200.0, 500.0):
        assert cevns.sub18_sensitivity_fraction(T_eV * 1e-3, f) < 1e-3, T_eV


def test_toggle_leaves_high_T_rate_unchanged():
    """The explicit e_min_cut=1.8 MeV fold reproduces the full dR/dT for T>200 eV."""
    f = cevns.ReactorFlux()
    f_cut = cevns.ReactorFlux(f.csv_path, e_min_cut_MeV=1.8)
    for T_eV in (200.0, 500.0):
        full = cevns.differential_rate(T_eV * 1e-3, f)
        cut = cevns.differential_rate(T_eV * 1e-3, f_cut)
        assert abs(full - cut) / full < 1e-3, f"T={T_eV:.0f} eV changed by toggle"


def test_csv_band_column_consistent():
    """deliv-drdt-band-csv: the 03-01 CSV band column matches the live fold."""
    import os

    csv = os.path.join(
        os.path.dirname(__file__), "..", "artifacts", "stage1", "cevns_dRdT.csv"
    )
    rows = []
    with open(csv) as fh:
        for line in fh:
            if line.startswith("#") or line.startswith("T_eV"):
                continue
            rows.append([float(x) for x in line.split(",")])
    arr = np.array(rows)
    T_eV = arr[:, 0]
    total_csv = arr[:, 6]  # dRdT_total
    band_csv = arr[:, 7]   # dRdT_band_1sigma
    f = cevns.ReactorFlux()
    # Spot-check three rows spanning the band-widening boundary.
    for T in (40.0, 100.0, 400.0):
        j = int(np.argmin(np.abs(T_eV - T)))
        tot = cevns.differential_rate(T_eV[j] * 1e-3, f)
        band = cevns.differential_rate_band(T_eV[j] * 1e-3, f)
        assert abs(tot - total_csv[j]) / total_csv[j] < 1e-3
        assert abs(band - band_csv[j]) / band_csv[j] < 1e-3
