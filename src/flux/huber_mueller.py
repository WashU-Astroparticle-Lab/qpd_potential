# ASSERT_CONVENTION: natural_units=io_MeV, energy_input=MeV, spectrum_units=nubar_per_fission_per_MeV
"""
Huber-Mueller per-fission reactor antineutrino spectrum (>~2 MeV, data-anchored).

Model (Huber PRC 84,024617; Mueller et al. PRC 83,054615):

    S_i(E_nu) = exp( sum_{p=1}^{6} alpha_{ip} * E_nu^{p-1} )   [nu-bar / fission / MeV]

with E_nu in MeV. The six coefficients per isotope are LOADED from
``data/flux/hm_coefficients.csv`` (fetched from the primary arXiv e-prints with a
provenance column) -- they are NOT inlined literals, per the phase's fetch-not-invent
contract (forbidden proxy fp-invented-coeffs).

Guarded classic bug: the polynomial lives INSIDE the exponential. Applying the
polynomial directly (forgetting exp) is the canonical Huber-Mueller error and is
explicitly asserted against in the unit tests.

Validity: the conversion/summation fit is anchored on 2-8 MeV. Evaluating below
~1.8 MeV is undefined for this model; callers must use the summation + n-capture
extension (see summation_ncapture.py / assemble_spectrum.py). This module will
evaluate the polynomial at any E for machinery/seam purposes but records the
validity window in HM_VALID_MIN / HM_VALID_MAX.
"""
from __future__ import annotations

import csv
import os
from typing import Dict, Sequence

import numpy as np

HM_VALID_MIN = 2.0   # MeV -- lower edge of the data-anchored fit range
HM_VALID_MAX = 8.0   # MeV -- upper edge of the tabulated fit range
N_COEFF = 6

_DATA = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "flux", "hm_coefficients.csv")
)

ISOTOPES = ("235U", "238U", "239Pu", "241Pu")


def load_coefficients(path: str = _DATA) -> Dict[str, np.ndarray]:
    """Load the six-coefficient row per isotope from the provenance-tagged CSV.

    Returns ``{isotope: np.array([alpha1..alpha6])}``. Raises if any coefficient is
    missing / non-finite (guards the fp-invented-coeffs / placeholder failure mode).
    """
    coeffs: Dict[str, np.ndarray] = {}
    with open(path, newline="") as fh:
        reader = csv.DictReader(row for row in fh if not row.startswith("#"))
        for row in reader:
            iso = row["isotope"].strip()
            a = np.array([float(row[f"alpha{p}"]) for p in range(1, N_COEFF + 1)], dtype=float)
            if not np.all(np.isfinite(a)):
                raise ValueError(f"Non-finite Huber-Mueller coefficient for {iso}: {a}")
            if not row.get("source", "").strip():
                raise ValueError(f"Missing source/provenance for {iso} (fetch-not-invent violated)")
            coeffs[iso] = a
    missing = set(ISOTOPES) - set(coeffs)
    if missing:
        raise ValueError(f"Missing isotopes in coefficient table: {sorted(missing)}")
    return coeffs


def hm_spectrum(E_nu, alpha: Sequence[float]):
    """S_i(E_nu) = exp( sum_p alpha_p E_nu^{p-1} ), E_nu in MeV, out in nu-bar/fission/MeV.

    The polynomial is evaluated in the EXPONENT (guarded against the direct-apply bug).
    """
    E = np.asarray(E_nu, dtype=float)
    a = np.asarray(alpha, dtype=float)
    # log_S = a1 + a2 E + a3 E^2 + ... + a6 E^5  (powers p-1 for p=1..6)
    log_S = np.zeros_like(E)
    for p, ap in enumerate(a):
        log_S = log_S + ap * np.power(E, p)
    return np.exp(log_S)


def hm_log_slope(E_nu, alpha: Sequence[float]):
    """d/dE_nu [ ln S_i ] = sum_{p=1}^{5} p * alpha_{p+1} * E_nu^{p-1}  (1/MeV).

    Used for C1 seam matching against the summation extension.
    """
    E = np.asarray(E_nu, dtype=float)
    a = np.asarray(alpha, dtype=float)
    dlog = np.zeros_like(E)
    for p in range(1, a.size):
        dlog = dlog + p * a[p] * np.power(E, p - 1)
    return dlog


def spectrum_by_isotope(E_nu, coeffs: Dict[str, np.ndarray] | None = None) -> Dict[str, np.ndarray]:
    """Return {isotope: S_i(E_nu)} evaluated on the given energy array."""
    if coeffs is None:
        coeffs = load_coefficients()
    return {iso: hm_spectrum(E_nu, coeffs[iso]) for iso in coeffs}


if __name__ == "__main__":
    c = load_coefficients()
    for iso in ISOTOPES:
        for E in (2.0, 3.0, 5.0):
            print(f"{iso:6s} S({E} MeV) = {float(hm_spectrum(E, c[iso])):.4g} nu-bar/fission/MeV")
