# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Bounded impulse-limit justification: harmonic incoherent S(q,w) for Ge (SC5).

BOUNDED ARTIFACT.  ROADMAP SC5 requires this be a one-off justification, not a
modelling backbone: at most 5 q values, one FFT each, no coherent-crystal S(q,w)
and no phonon-order multiphonon expansion (``fp-coherent-backbone``,
``fp-scope-creep``).

Formalism (T -> 0 cumulant / self-correlation route)
---------------------------------------------------
Intermediate scattering function for a harmonic lattice, incoherent (self) part::

    F(q,t) = exp(-2W + gamma(t))
    gamma(t) = (hbar^2 q^2 / 2 m_N) int g(w)/w * e^{-i w t} dw          (T -> 0, n_B = 0)
    2W = gamma(0) = q^2 <u_x^2>                                          (ties back to Section J)
    S(q,w) = (1/2pi) int e^{+i w t} F(q,t) dt

Sign convention fixed by requiring the ONE-PHONON term to sit at POSITIVE energy
transfer: expanding ``exp(gamma) ~ 1 + gamma`` gives
``S_1(w) = e^{-2W} (hbar^2 q^2/2 m_N) g(w)/w`` for ``w > 0``, and the zero-phonon term
gives ``e^{-2W} delta(w)``.  With ``e^{-i w t}`` in the ``S`` transform the one-phonon
line would land at negative w, which is wrong.

A simplification that removes every free constant
-------------------------------------------------
``q^2 = 2 m_N E_R`` gives ``hbar^2 q^2 / (2 m_N) = E_R`` EXACTLY, so::

    gamma(t) = E_R * int g(w)/w * e^{-i w t} dw       and   2W = E_R / omega_bar_u

The whole harmonic S is fixed by E_R and the VDOS alone; no mass, no hbar survives.

EXACT CUMULANTS -- the analytic backbone, and the fallback the plan asked for
----------------------------------------------------------------------------
``ln F = -2W + gamma(t)``, and with ``F(t) = <e^{-i w t}>`` the cumulants of S are
``kappa_n = i^n gamma^{(n)}(0)``.  Since
``gamma^{(n)}(0) = E_R int (g/w)(-i w)^n dw = E_R (-i)^n <w^{n-1}>``::

    kappa_n = E_R * <w^{n-1}>_g          for all n >= 1

so, EXACTLY and for the FULL S including the elastic line:

    kappa_1 = E_R                        <- the f-sum rule, exact for any interaction
    kappa_2 = E_R * <w>   = E_R * omega_bar_p     <- the ARITHMETIC VDOS mean
    kappa_3 = E_R * <w^2>
    skewness = kappa_3 / kappa_2^{3/2} = <w^2> / (sqrt(E_R) * <w>^{3/2})  ~ 1/sqrt(2W)

``kappa_2 = E_R * omega_bar_p`` is an INDEPENDENT confirmation of plan 11-02's
arithmetic-vs-harmonic systematic, reached from the harmonic correlation function
rather than from the momentum distribution.  If it had come out ``E_R * omega_bar_u``,
plan 11-02 would be wrong and 11-04 would be blocked.

The numerical FFT is therefore a CHECK on these closed forms, not the only route.  If
the FFT is unusable at some q, the analytic cumulants stand and the fallback is
recorded rather than the scope expanded.

Strength partition and the e^(-2W) prohibition
----------------------------------------------
``lim_{t->inf} F(q,t) = e^{-2W}`` (Riemann-Lebesgue on gamma), so ``e^{-2W}`` is the
weight of the ZERO-PHONON (elastic) line at w = 0 and NOTHING ELSE.  The remaining
``1 - e^{-2W}`` sits in the multiphonon continuum, and since the elastic line at w = 0
contributes exactly zero to the first moment, **the inelastic continuum alone carries
the entire f-sum rule**.  Multiplying the RATE by ``e^{-2W}`` would therefore discard
that continuum -- ~99.6 % of the strength at 100 meV and effectively all of it at 1 eV.
Milestone-wide locked prohibition ``fp-dw-rate-suppression``; nothing in this module
multiplies any rate by anything.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Optional

import numpy as np

from . import params, phonon_scale

#: ROADMAP SC5 bound: five recoil energies, one FFT each. Not a tunable.
BOUNDED_RECOIL_ENERGIES_eV = (0.1, 0.5, 1.0, 10.0, 100.0)

#: Extended-grid floor and first bin centre (plan 10-03), for the leakage diagnostic.
EXT_GRID_FLOOR_eV = 0.0999350
EXT_GRID_FIRST_CENTRE_eV = 0.1013838


# --------------------------------------------------------------------------- #
# VDOS moments                                                                 #
# --------------------------------------------------------------------------- #
def vdos_raw_moments(source: str = "ncrystal", n_max: int = 4) -> dict:
    """``<w^k>`` for k = -1..n_max from the frozen VDOS, in eV^k."""
    omega_meV, g_meV = phonon_scale.load_vdos(source)
    w = omega_meV * 1e-3
    g = phonon_scale.normalize_vdos(w, g_meV * 1e3)     # 1/eV, int g dw = 1
    out = {-1: float(np.trapz(g / w, w))}
    for k in range(0, n_max + 1):
        out[k] = float(np.trapz(g * w ** k, w))
    return out


def cumulants(E_R_eV: float, source: str = "ncrystal", n_max: int = 4) -> dict:
    """Exact cumulants of the harmonic incoherent S: ``kappa_n = E_R <w^{n-1}>``."""
    mom = vdos_raw_moments(source, n_max=n_max)
    return {n: E_R_eV * mom[n - 1] for n in range(1, n_max + 2)}


def analytic_moments(E_R_eV: float, source: str = "ncrystal") -> dict:
    """Closed-form mean, variance, skewness and excess kurtosis of the harmonic S."""
    k = cumulants(E_R_eV, source, n_max=4)
    var = k[2]
    return {
        "E_R_eV": E_R_eV,
        "mean_eV": k[1],
        "variance_eV2": var,
        "sigma_eV": float(np.sqrt(var)),
        "skewness": k[3] / var ** 1.5,
        "excess_kurtosis": k[4] / var ** 2,
    }


# --------------------------------------------------------------------------- #
# 2W and the elastic weight                                                    #
# --------------------------------------------------------------------------- #
def two_W(E_R_eV: float, source: str = "ncrystal") -> float:
    """``2W = gamma(0) = E_R * <1/w>`` -- must equal ``q^2 <u_x^2>`` from Section J."""
    return E_R_eV * vdos_raw_moments(source, n_max=0)[-1]


def elastic_weight(E_R_eV: float, source: str = "ncrystal") -> float:
    """``e^(-2W)``: the ZERO-PHONON weight, and nothing else.

    Never a rate suppression (``fp-dw-rate-suppression``).
    """
    return float(np.exp(-two_W(E_R_eV, source)))


# --------------------------------------------------------------------------- #
# Numerical S(q,w) -- one FFT per q, elastic line handled analytically          #
# --------------------------------------------------------------------------- #
def structure_factor(E_R_eV: float, source: str = "ncrystal",
                     n_fft_max: int = 1 << 21, sigma_span: float = 24.0,
                     points_per_sigma: float = 60.0):
    """Inelastic part of the harmonic incoherent S(q,w), by one FFT.

    Returns ``(w_eV, S_inel_per_eV, elastic_weight)`` with

        S(q,w) = elastic_weight * delta(w) + S_inel(w)

    TWO terms are split off ANALYTICALLY before the transform, both for the same
    reason: whatever ``F`` fails to decay to is turned into ringing across the ENTIRE
    w grid by a finite transform, and the third moment -- which weights by
    ``(w - E_R)^3`` out to several eV -- is dominated by that ringing rather than by
    physics.

    * **Zero-phonon.** ``F(t) -> e^{-2W}`` as ``t -> inf``.  Subtracting it leaves
      ``e^{-2W}(e^{gamma}-1)``, and the elastic weight is carried as a delta.
    * **One-phonon.** The remainder still behaves as ``e^{-2W} gamma(t)`` at large t,
      and ``gamma`` only decays as a power law (the VDOS has hard edges).  But that
      piece transforms EXACTLY to ``S_1(w) = e^{-2W} E_R g(w)/w``, which has compact
      support on the VDOS band.  Subtracting it leaves ``e^{-2W}(e^{gamma}-1-gamma) ~
      e^{-2W} gamma^2/2``, four orders of magnitude smaller at the truncation point,
      and the analytic ``S_1`` is added back on the w grid.

    Still ONE FFT per q (``fp-scope-creep``); the extra pieces are closed forms.

    ``S_inel`` integrates to ``1 - e^{-2W}`` and carries the ENTIRE first moment,
    because a delta at w = 0 contributes nothing to it.
    """
    omega_meV, g_meV = phonon_scale.load_vdos(source)
    w_v = omega_meV * 1e-3
    g_v = phonon_scale.normalize_vdos(w_v, g_meV * 1e3)

    an = analytic_moments(E_R_eV, source)
    sigma = an["sigma_eV"]
    dw = sigma / points_per_sigma
    span = E_R_eV + sigma_span * sigma
    # The FFT's positive-frequency half is k < n/2, so the grid must span 2*span in
    # total or the peak aliases onto the negative-frequency half.  Getting this wrong
    # is silent: the moments look self-consistent but the mean lands at n*dw - E_R.
    n = 1 << 12
    while n * dw < 2.0 * span and n < n_fft_max:
        n <<= 1
    if n * dw < 2.0 * span:
        raise RuntimeError(
            f"E_R = {E_R_eV} eV needs n*dw >= {2*span:.3f} eV but the cap n_fft_max = "
            f"{n_fft_max} gives {n*dw:.3f} eV. Take the ANALYTIC-MOMENT FALLBACK and "
            "record it -- do not raise the cap (fp-scope-creep).")
    dt = 2.0 * np.pi / (n * dw)
    t = np.arange(n) * dt

    # gamma(t) = E_R * int g(w)/w e^{-i w t} dw, by direct quadrature over the VDOS.
    # Chunked so the (n x n_vdos) outer product never materialises in full.
    kern = g_v / w_v
    gamma = np.empty(n, dtype=complex)
    chunk = max(1, int(4e7 // len(w_v)))
    for a in range(0, n, chunk):
        b = min(a + chunk, n)
        phase = np.exp(-1j * np.outer(t[a:b], w_v))
        gamma[a:b] = E_R_eV * np.trapz(kern * phase, w_v, axis=1)

    tw = float(gamma[0].real)
    e2w = float(np.exp(-tw))
    # e^{-2W}(e^{gamma}-1) written as exp(gamma - 2W) - exp(-2W): at E_R = 100 eV,
    # 2W = 5599 and e^{+gamma} overflows while e^{-2W} underflows to exactly 0.  This
    # form is finite everywhere and reduces to 1 at t = 0 and to 0 as t -> infinity.
    # multiphonon-only remainder: e^{-2W}(e^{gamma} - 1 - gamma), written so that it
    # stays finite at 2W = 5599 where e^{+gamma} overflows and e^{-2W} underflows to 0.
    F_inel = np.exp(gamma - tw) - e2w * (1.0 + gamma)

    # S(w) = (1/2pi) int e^{+i w t} F(t) dt = (1/pi) Re int_0^inf e^{+i w t} F(t) dt
    # Trapezoid on [0, t_max) -> half weight at t = 0.
    F_inel[0] *= 0.5
    # w_k t_j = 2 pi j k / n, and we need e^{+i w t}, i.e. sum_j F_j e^{+2 pi i j k/n}
    # = n * ifft(F).  np.fft.fft carries the MINUS sign and would put the peak at
    # w = -E_R, which aliases to n*dw - E_R and looks superficially plausible.
    spec = np.fft.ifft(F_inel) * n
    S = (dt / np.pi) * np.real(spec)
    half = n // 2                             # keep the positive-frequency half only
    w_grid = np.arange(half) * dw
    S = S[:half]
    # add back the analytic one-phonon term S_1(w) = e^{-2W} E_R g(w)/w on the w grid
    S = S + e2w * E_R_eV * np.interp(w_grid, w_v, g_v / w_v, left=0.0, right=0.0)
    return w_grid, S, e2w


@lru_cache(maxsize=32)
def converged_numeric_moments(E_R_eV: float, source: str = "ncrystal",
                              tol: float = 1e-6, ladder=(60, 240, 960, 3840)) -> dict:
    """``numeric_moments`` refined until the zeroth moment is within ``tol`` of 1.

    The zeroth moment is the right convergence handle because its exact value is
    known independently (it is 1 by construction) and because it responds to the
    same truncation ringing that limits the third moment.  At the four upper
    energies the first rung already gives 1e-12; only the bottom bin (2W = 5.60,
    where gamma decays as a slow power law) needs the ladder.
    """
    last = None
    for pps in ladder:
        last = numeric_moments(E_R_eV, source=source, points_per_sigma=pps)
        last["points_per_sigma"] = pps
        last["converged"] = abs(last["zeroth_moment"] - 1.0) < tol
        if last["converged"]:
            break
    return last


def numeric_moments(E_R_eV: float, **kw) -> dict:
    """Zeroth / first / second-central / skewness of the NUMERICAL S, plus the
    elastic weight.  Moments are of the FULL S (elastic line included), so they are
    directly comparable with ``analytic_moments``."""
    w, S, e2w = structure_factor(E_R_eV, **kw)
    m0 = float(np.trapz(S, w)) + e2w                     # + elastic delta at w = 0
    m1 = float(np.trapz(w * S, w))                       # elastic contributes 0
    mean = m1 / m0
    m2c = float(np.trapz((w - mean) ** 2 * S, w)) + e2w * mean ** 2
    m3c = float(np.trapz((w - mean) ** 3 * S, w)) - e2w * mean ** 3
    return {
        "zeroth_moment": m0,
        "first_moment_eV": m1,
        "mean_eV": mean,
        "second_central_eV2": m2c / m0,
        "skewness": (m3c / m0) / (m2c / m0) ** 1.5,
        "elastic_weight": e2w,
        "inelastic_weight": float(np.trapz(S, w)),
    }


# --------------------------------------------------------------------------- #
# What the matched symmetric Gaussian gets wrong                               #
# --------------------------------------------------------------------------- #
def _phi(z):
    """Standard normal CDF, via erf (no scipy dependency needed for one call)."""
    from math import erf, sqrt
    return 0.5 * (1.0 + erf(z / sqrt(2.0)))


def gaussian_offgrid_weights(centre_eV: float,
                             sigma_eV: Optional[float] = None,
                             floor_eV: float = EXT_GRID_FLOOR_eV) -> dict:
    """Weight the matched symmetric Gaussian puts where the true S cannot go.

    ``w < 0`` is unphysical by construction: the T -> 0 harmonic S vanishes for
    negative energy transfer (no phonons available to absorb).  ``w < floor`` is the
    off-grid leakage plan 11-04 must account for on the extended axis.
    """
    if sigma_eV is None:
        sigma_eV = float(np.sqrt(centre_eV * params.OMEGA_BAR_eV.value))
    return {
        "centre_eV": centre_eV,
        "sigma_eV": sigma_eV,
        "weight_below_zero": _phi((0.0 - centre_eV) / sigma_eV),
        "weight_below_floor": _phi((floor_eV - centre_eV) / sigma_eV),
        "n_sigma_to_zero": centre_eV / sigma_eV,
    }
