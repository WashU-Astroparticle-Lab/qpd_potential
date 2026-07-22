"""Acceptance tests for Phase-2 Plan 02-01: per-fission reactor antineutrino spectrum.

Encodes the four contract acceptance tests:
  test-coeffs-sourced   : every HM coefficient row carries provenance; no NaN/placeholder.
  test-hm-unit          : reconstructed 235U within ~5% of published Huber tabulation at 3, 5 MeV.
  test-integral-yields  : total ~6, above-1.8 ~1.9, n-capture ~0.6 nu-bar/fission (within bands).
  test-seam-continuity  : no visible step (<2%) at the seam, C1 blend, non-negative everywhere.
"""
import csv
import os
import sys

import numpy as np
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from flux.huber_mueller import load_coefficients, hm_spectrum, ISOTOPES, N_COEFF  # noqa: E402
from flux.assemble_spectrum import assemble, build_energy_grid, SEAM_LO, SEAM_HI  # noqa: E402

DATA = os.path.join(ROOT, "data", "flux")


# ---------------------------------------------------------------- test-coeffs-sourced
def test_coeffs_sourced():
    """Every isotope coefficient row is finite and carries a populated source column."""
    path = os.path.join(DATA, "hm_coefficients.csv")
    rows = list(csv.DictReader(r for r in open(path) if not r.startswith("#")))
    seen = set()
    for row in rows:
        iso = row["isotope"].strip()
        seen.add(iso)
        assert row["source"].strip(), f"{iso} missing source provenance"
        assert row["arxiv_id"].strip(), f"{iso} missing arxiv_id provenance"
        for p in range(1, N_COEFF + 1):
            v = float(row[f"alpha{p}"])
            assert np.isfinite(v), f"{iso} alpha{p} not finite"
    assert set(ISOTOPES) <= seen


def test_ncapture_sourced_provenance():
    """The n-capture data file states its sourced normalization and computed shape."""
    txt = open(os.path.join(DATA, "ncapture_238U.csv")).read()
    assert "Kopeikin" in txt and "0.6" in txt and "AME2020" in txt


# --------------------------------------------------------------------- test-hm-unit
def test_hm_unit_235U():
    """Reconstructed 235U matches the published Huber tabulation within ~5% at 3 and 5 MeV."""
    coeffs = load_coefficients()
    bench = {}
    for row in open(os.path.join(DATA, "huber_U235_benchmark.csv")):
        if row.startswith("#") or row.startswith("E_nu"):
            continue
        e, s = row.split(",")
        bench[float(e)] = float(s)
    for E in (3.0, 5.0):
        recon = float(hm_spectrum(E, coeffs["235U"]))
        rel = abs(recon - bench[E]) / bench[E]
        assert rel < 0.05, f"235U at {E} MeV: {rel*100:.1f}% > 5%"


def test_hm_uses_exponential_not_direct_polynomial():
    """Guard the classic bug: the polynomial must be applied inside exp(), not directly."""
    coeffs = load_coefficients()
    a = coeffs["235U"]
    E = 3.0
    poly = sum(a[p] * E ** p for p in range(N_COEFF))
    recon = float(hm_spectrum(E, a))
    assert np.isclose(recon, np.exp(poly)), "hm_spectrum must exponentiate the polynomial"
    assert not np.isclose(recon, poly), "hm_spectrum must NOT return the bare polynomial"


# ------------------------------------------------------------- test-integral-yields
def test_integral_yields():
    y = assemble().integral_yields()
    assert abs(y["total_fission_per_fission"] - 6.0) / 6.0 < 0.15, y
    assert abs(y["above_1p8_per_fission"] - 1.9) / 1.9 < 0.20, y
    assert abs(y["ncapture_per_fission"] - 0.6) / 0.6 < 0.30, y


def test_sub_ibd_not_truncated():
    """Forbidden proxy fp-truncate-ibd: the sub-1.8 MeV fission flux must be populated."""
    spec = assemble()
    below = spec.E < SEAM_LO
    fw = spec.fission_weighted()
    assert np.all(fw[below] > 0), "sub-1.8 MeV flux must not be zero/truncated"
    # and it must carry a substantial fraction of the total antineutrinos
    assert spec.integral_yields()["below_1p8_per_fission"] > 2.0


# ------------------------------------------------------------- test-seam-continuity
def test_seam_continuity_and_nonnegativity():
    # fine uniform grid through the seam for a clean C1 check
    fine = np.linspace(1.2, 2.6, 1401)
    spec = assemble(grid=fine)
    E = spec.E
    for iso in ISOTOPES:
        S = spec.per_isotope[iso]
        assert np.all(S > 0), f"{iso} negative/zero flux"
        # no visible step: max adjacent relative jump < 2%
        reljump = np.max(np.abs(np.diff(S)) / S[:-1])
        assert reljump < 0.02, f"{iso} seam step {reljump*100:.2f}% >= 2%"
        # C1: first derivative of log-flux has no discontinuity (bounded 2nd difference)
        d1 = np.gradient(np.log(S), E)
        assert np.max(np.abs(np.diff(d1))) < 0.05, f"{iso} log-slope discontinuity at seam"


def test_global_nonnegativity_and_pchip_no_ringing():
    """Forbidden proxy fp-negative-spline: full-grid flux stays non-negative (no ringing)."""
    spec = assemble()
    assert np.all(spec.total() >= 0)
    assert np.all(spec.ncapture >= 0)
    for iso in ISOTOPES:
        assert np.all(spec.per_isotope[iso] > 0)


def test_ncapture_endpoint_below_1p3():
    """n-capture antineutrino flux confined to E_nu <~ 1.3 MeV (Kopeikin)."""
    E = build_energy_grid()
    from flux.summation_ncapture import ncapture_spectrum
    cap = ncapture_spectrum(E)
    emax = float(E[cap > 1e-3 * cap.max()].max())
    assert emax < 1.35, f"n-capture endpoint {emax} MeV too high"
