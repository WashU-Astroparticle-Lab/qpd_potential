# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Deterministic (noise-free) muon deposited-energy spectrum dR/dE_dep.

Same physics as ``muon_deposit.run_muon_mc`` -- Gaisser-Guan flux, ray-box chord,
Landau-Vavilov straggling -- with every sampling step replaced by the closed-form
object it was sampling from.  The Monte-Carlo path remains in place and this
module is validated AGAINST it; nothing here supersedes it silently.

WHY THE MONTE CARLO IS NOISY EVEN THOUGH EVERY INGREDIENT IS ANALYTIC
--------------------------------------------------------------------
``run_muon_mc`` evaluates a 4-D integral (E_mu, theta, phi, chord) plus a Landau
convolution by drawing 1e9 uniform points.  MC allocates samples by PROBABILITY;
a log-binned spectrum displays DECADES with equal weight.  A 0.1 eV deposit needs
a chord of ~1e-7 cm, a corner-grazing track of probability ~1e-7, so 1e9 samples
put ~88 events into that entire decade -- ~2 per bin, relative error ~1.  Nothing
there is physically uncertain; uniform sampling simply does not know to look in a
region carrying 1e-7 of the measure.  The noise is a property of the estimator,
not of the integrand.

THE THREE SAMPLING STEPS AND WHAT REPLACES EACH
-----------------------------------------------
1. ENTRY FACE.  ``sample_entry_and_chord`` picks entry axis ``a`` with probability
   ``A_a |Omega_a| / sum_j A_j |Omega_j|``.  Here all three are summed over with
   those weights.  No sampling.

2. CHORD.  Given entry axis ``a``, the entry point is uniform on the opposite two
   coordinates, so the exit distances are:

     * along ``a``:  T_a = L_a / |Omega_a|                      (a CONSTANT)
     * along ``j``:  uniform on (0, M_j),  M_j = L_j / |Omega_j|

   because the entry coordinate is uniform on (0, L_j) whichever sign Omega_j has.
   Therefore

       ell = min(T_a, U_b, U_c),      U_j ~ Uniform(0, M_j) independent

   and the chord law is EXACT and elementary:

       S(t) = P(ell > t) = 1{t < T_a} (1 - t/M_b)_+ (1 - t/M_c)_+
       p(t) = -S'(t) = [(1 - t/M_c)/M_b + (1 - t/M_b)/M_c]   on (0, t_max)
       plus an ATOM of mass S(T_a) at t = T_a when T_a < min(M_b, M_c)

   The atom is not a technicality: it is the straight-through chord that produces
   the MPV peak.  For a near-vertical muon entering the 2 mm face, T_z = 0.2/cos
   while M_x, M_y are ~10 cm, so the atom carries almost the whole probability.
   Dropping it would delete the peak.  Normalization is checked in-code.

3. LANDAU STRAGGLING.  ``sample_deposit`` draws lambda from the standard Landau
   and forms ``dep = Delta_p + xi (lambda - lambda_mode)``.  Here the Landau CDF
   is evaluated at the bin EDGES instead, so each (chord, energy) contributes its
   exact probability to every bin (Rao-Blackwellization: same expectation, zero
   variance from this step).

   The Gaussian (kappa >= 10) branch of ``sample_deposit`` is NOT reimplemented.
   It is unreachable: kappa <= 1.7e-3 over the whole (chord, energy) domain of
   this wafer.  ``assert_landau_regime`` proves that rather than assuming it, and
   raises if a future geometry ever leaves the Landau/mild-Vavilov regime.

WHAT THIS DOES NOT FIX (carried forward, unchanged)
---------------------------------------------------
Smoothness is not validity.  Below the Landau-Vavilov floor of 4111.8 eV the
straggling model itself does not apply (it requires xi >> I; xi = I exactly at
that point), and at the 0.0999 eV grid floor the implied muon path is under two
germanium lattice constants.  This module makes that region SMOOTH, not TRUE.  It
is emitted so the figure can mark the floor and style the sub-floor range as the
geometric extrapolation it is.  The channel is 0.015% of the 10-100 eV RoI
background, so none of this moves the budget.

Nor does anything here add secondary transport: no delta-ray escape geometry, no
EM showers, no muon-induced neutrons or gammas in surrounding material.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import muon_deposit as md
from . import muon_flux
from . import wafer_geometry as wg

#: Quadrature orders. Every one is a CONVERGENCE KNOB, not a physics choice:
#: `convergence_table` re-runs at doubled orders and reports the change.
N_E = 96          # Gauss-Legendre nodes in log E_mu
N_THETA = 64      # Gauss-Legendre nodes in theta on (0, pi/2)
N_PHI = 24        # Gauss-Legendre nodes in phi on (0, pi/2); see _PHI_PERIOD
N_ELL = 256       # log-spaced midpoint nodes per (direction, entry axis)

#: Bins of the intermediate chord histogram. ~100/decade over 10 decades, i.e.
#: finer than the 80/decade energy grid it feeds, so the chord discretization is
#: subdominant to the axis the answer is reported on.
_N_ELL_BINS = 1024

#: A_proj and the chord law depend on phi only through |cos phi| and |sin phi|,
#: which have period pi/2. Integrating one quarter-period and multiplying by 4 is
#: exact, not an approximation, and buys 4x the phi resolution for free.
_PHI_PERIOD = np.pi / 2.0

#: Smallest chord carried. dep(1e-9 cm) ~ 1e-3 eV, two decades below the 0.0999 eV
#: grid floor, so nothing that could land in a bin is truncated.
ELL_MIN_CM = 1.0e-9

E_MIN_GEV = 0.2
E_MAX_GEV = 1.0e5


@dataclass
class MuonAnalyticSpectrum:
    edges_kev: np.ndarray
    centers_kev: np.ndarray
    dRdE: np.ndarray             # counts / kg / day / keV
    rate_hz: float               # integral muon rate through the wafer [Hz]
    counts_per_kg_day: float     # integral of dR/dE_dep dE (energy closure)
    vertical_mpv_mev: float
    vertical_mean_mev: float
    kappa_max: float
    chord_norm_max_dev: float    # worst |chord law normalization - 1|
    grid_version: str


# --------------------------------------------------------------------------- #
# Landau CDF (the sampler's own table, read forwards instead of inverted)      #
# --------------------------------------------------------------------------- #
def landau_cdf(lam: np.ndarray) -> np.ndarray:
    """F(lambda) for the standard Landau, from muon_deposit's cached table.

    Deliberately reuses ``muon_deposit._build_landau_table`` rather than
    rebuilding the density: the MC samples by inverting exactly this table, so
    any error in it is COMMON to both paths and cannot hide in the comparison.
    Beyond the tabulated range the analytic tail F = 1 - c/lambda is used, the
    same continuation the sampler applies.
    """
    grid, cdf, lam_hi, c_tail = md._build_landau_table()
    lam = np.asarray(lam, dtype=float)
    out = np.interp(lam, grid, cdf, left=0.0, right=cdf[-1])
    hi = lam > lam_hi
    if np.any(hi):
        out = np.where(hi, 1.0 - c_tail / np.clip(lam, 1e-12, None), out)
    return np.clip(out, 0.0, 1.0)


def assert_landau_regime(kappa_max: float) -> None:
    """The Gaussian branch of ``sample_deposit`` must be unreachable.

    ``sample_deposit`` switches to a Gaussian at kappa >= 10. This module
    implements only the Landau branch, so that switch must never fire. Proven,
    not assumed.
    """
    if kappa_max >= 10.0:
        raise RuntimeError(
            f"kappa_max = {kappa_max:.4g} >= 10: the Vavilov/Gaussian branch is "
            "reachable for this geometry, but muon_analytic implements only the "
            "Landau branch. Extend it before trusting this spectrum.")


# --------------------------------------------------------------------------- #
# Exact chord law for a box under parallel illumination                        #
# --------------------------------------------------------------------------- #
def chord_law(T_a: np.ndarray, M_b: np.ndarray, M_c: np.ndarray, ell: np.ndarray):
    """Continuous density p(ell) and the atom mass at T_a, vectorized.

    Shapes: T_a, M_b, M_c are (N,); ell is (K,); returns p of shape (N, K) and
    atom of shape (N,). Infinite M (a direction exactly parallel to a face) is
    handled by 1/M -> 0, which is the correct limit: that axis never bounds the
    chord.
    """
    T_a = T_a[:, None]
    inv_b = np.where(np.isfinite(M_b), 1.0 / M_b, 0.0)[:, None]
    inv_c = np.where(np.isfinite(M_c), 1.0 / M_c, 0.0)[:, None]
    t = ell[None, :]

    fb = np.clip(1.0 - t * inv_b, 0.0, None)
    fc = np.clip(1.0 - t * inv_c, 0.0, None)
    inside = t < T_a
    p = np.where(inside, fb * inv_c + fc * inv_b, 0.0)

    fb_a = np.clip(1.0 - T_a[:, 0] * inv_b[:, 0], 0.0, None)
    fc_a = np.clip(1.0 - T_a[:, 0] * inv_c[:, 0], 0.0, None)
    atom = fb_a * fc_a
    return p, atom


def chord_normalization(T_a, M_b, M_c, ell, dell):
    """integral p dell + atom, which must be 1 for every direction/entry axis.

    Returned so the caller can assert it rather than trust the algebra. This is
    the one place a sign or a clip error would silently rescale the whole
    spectrum, and it would NOT show up as noise.
    """
    p, atom = chord_law(T_a, M_b, M_c, ell)
    return (p * dell[None, :]).sum(axis=1) + atom


# --------------------------------------------------------------------------- #
# Assembly                                                                     #
# --------------------------------------------------------------------------- #
def _gauss_legendre(a, b, n):
    x, w = np.polynomial.legendre.leggauss(n)
    return 0.5 * (b - a) * x + 0.5 * (a + b), 0.5 * (b - a) * w


def run_muon_analytic(grid_version: str = "v2.0-ext",
                      n_e: int = N_E, n_theta: int = N_THETA,
                      n_phi: int = N_PHI, n_ell: int = N_ELL,
                      e_min_gev: float = E_MIN_GEV,
                      e_max_gev: float = E_MAX_GEV) -> MuonAnalyticSpectrum:
    """Deterministic dR/dE_dep [counts/kg/day/keV] on the shared log grid."""
    edges = md.shared_energy_grid(grid_version)          # keV
    centers = np.sqrt(edges[:-1] * edges[1:])
    edges_mev = edges * 1.0e-3
    nb = centers.size

    # ---- outer quadrature: log E_mu x theta x phi -------------------------- #
    lnE, wlnE = _gauss_legendre(np.log(e_min_gev), np.log(e_max_gev), n_e)
    E = np.exp(lnE)
    wE = wlnE * E                                        # dE = E d(lnE)
    th, wth = _gauss_legendre(0.0, np.pi / 2.0, n_theta)
    ph, wph = _gauss_legendre(0.0, _PHI_PERIOD, n_phi)
    wph = wph * 4.0                                      # exact quarter-period fold

    bg_of_E = md.beta_gamma(E)
    beta2_of_E = (bg_of_E ** 2) / (bg_of_E ** 2 + 1.0)

    # direction grid (theta x phi)
    TH, PH = np.meshgrid(th, ph, indexing="ij")
    dirs = wg.direction_from_angles(TH.ravel(), PH.ravel())      # (ND,3)
    a_proj = wg.projected_area(dirs)                             # (ND,)
    sin_th = np.sin(TH).ravel()
    cos_th = np.cos(TH).ravel()
    w_dir = (np.outer(wth, wph)).ravel() * sin_th * a_proj       # dOmega weight x area
    ND = dirs.shape[0]

    absD = np.abs(dirs)
    face_w = absD * wg.FACE_AREA[None, :]                        # (ND,3)
    face_p = face_w / face_w.sum(axis=1, keepdims=True)          # entry-face probs

    # per (direction, entry axis): T_a and the two bounding M_j
    with np.errstate(divide="ignore"):
        M_all = wg.EDGES[None, :] / absD                         # (ND,3), inf if D=0

    # ---- pass 1: collapse the geometry into a chord x theta distribution --- #
    # The muon energy enters ONLY through dI/dE(E, cos theta) and through
    # (Delta_p, xi). Neither the chord law nor A_proj depends on E, so the whole
    # (phi, entry-axis, chord) structure can be integrated ONCE into
    # H[chord bin, theta node] and reused for every energy node. That is what
    # makes this affordable; it also lets each direction get chord nodes matched
    # to ITS OWN cap, which a single shared node set cannot do -- p(ell) is
    # largest just below the cap, so a shared grid mis-resolves exactly the
    # directions whose cap is far below the global maximum.
    ell_hi_global = float(np.nanmax(np.where(np.isfinite(M_all), M_all, 0.0)))
    ell_edges = np.logspace(np.log10(ELL_MIN_CM), np.log10(ell_hi_global * 1.001),
                            _N_ELL_BINS + 1)
    ell_ctr = np.sqrt(ell_edges[:-1] * ell_edges[1:])
    H = np.zeros((_N_ELL_BINS, n_theta))
    chord_dev = 0.0

    # fixed log-spaced FRACTIONS of each direction's own cap
    frac_edges = np.logspace(np.log10(1.0e-9), 0.0, n_ell + 1)
    for idx in range(ND):
        i_th = idx // n_phi
        base = w_dir[idx]
        if base <= 0.0:
            continue
        for a in range(3):
            pa = face_p[idx, a]
            if pa <= 0.0:
                continue
            others = [j for j in range(3) if j != a]
            T_a = M_all[idx, a]
            M_b, M_c = M_all[idx, others[0]], M_all[idx, others[1]]
            cap = min(T_a, M_b, M_c)
            if not np.isfinite(cap) or cap <= 0.0:
                continue
            ee = frac_edges * cap
            ell_n = np.sqrt(ee[:-1] * ee[1:])
            dell_n = np.diff(ee)
            p_n, atom = chord_law(np.array([T_a]), np.array([M_b]),
                                  np.array([M_c]), ell_n)
            w_n = p_n[0] * dell_n
            chord_dev = max(chord_dev, abs(float(w_n.sum() + atom[0]) - 1.0))
            contrib = base * pa
            H[:, i_th] += np.histogram(ell_n, bins=ell_edges,
                                       weights=w_n * contrib)[0]
            if atom[0] > 0.0:
                H[:, i_th] += np.histogram(np.array([T_a]), bins=ell_edges,
                                           weights=np.array([atom[0] * contrib]))[0]

    # ---- pass 2: fold in the muon energy and the Landau straggling --------- #
    sumw = np.zeros(nb)
    rate_hz = 0.0
    kappa_max = 0.0
    live_ell = H.sum(axis=1) > 0.0
    ell_live = ell_ctr[live_ell]
    x_gcm2 = md.RHO * ell_live
    cos_nodes = np.cos(th)

    for ie in range(n_e):
        bg = bg_of_E[ie]
        inten = muon_flux.dI_dE(np.full(n_theta, E[ie]), cos_nodes)   # (n_theta,)
        w_ell = H[live_ell] @ (inten * wE[ie])                        # (NL,)
        if not np.any(w_ell > 0.0):
            continue
        bgv = np.full_like(x_gcm2, bg)
        dp, xi = md.mpv_deposit(x_gcm2, bgv)
        kappa_max = max(kappa_max, float(md.kappa(x_gcm2, bgv).max()))

        # Rao-Blackwellized Landau: exact probability into every bin.
        lam = (edges_mev[None, :] - dp[:, None]) / xi[:, None] + md._LAM_MODE
        F = landau_cdf(lam)
        sumw += (w_ell[:, None] * np.diff(F, axis=1)).sum(axis=0)
        # The rate counts every track with a POSITIVE deposit, matching the MC's
        # `valid = dep > 0` mask (mass at dep <= 0 is dropped, not clipped to 0).
        F0 = landau_cdf((0.0 - dp) / xi + md._LAM_MODE)
        rate_hz += float((w_ell * (1.0 - F0)).sum())

    assert_landau_regime(kappa_max)

    per_day = 86400.0 / wg.MASS_KG
    dRdE = sumw * per_day / np.diff(edges)
    counts = float((dRdE * np.diff(edges)).sum())

    dp_v, xi_v = md.mpv_deposit(np.array([md.RHO * wg.LZ]),
                                np.array([md.beta_gamma(np.array([4.0]))[0]]))
    return MuonAnalyticSpectrum(
        edges_kev=edges,
        centers_kev=centers,
        dRdE=dRdE,
        rate_hz=rate_hz,
        counts_per_kg_day=counts,
        vertical_mpv_mev=float(dp_v[0]),
        vertical_mean_mev=float(md.DEDX_MEAN * md.RHO * wg.LZ),
        kappa_max=kappa_max,
        chord_norm_max_dev=chord_dev,
        grid_version=grid_version,
    )
