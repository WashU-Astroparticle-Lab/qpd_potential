# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Impulse-approximation quantum broadening of the nuclear-recoil spectrum (CALC-15).

Derivation, in-phase, from the impulse approximation (Sears, Phys. Rev. B 35, 2038
(1987)) rather than from the closed form
--------------------------------------------------------------------------------
A nucleus struck with momentum transfer ``q`` recoils freely; the energy transfer is

    w = q^2/(2 m_N) + q.p / m_N

with ``p`` the nucleus's momentum BEFORE the collision.  For an isotropic momentum
distribution:

    <w>      = q^2/(2 m_N) = E_R                     (the second term has zero mean)
    Var(w)   = <(q.p)^2>/m_N^2 = q^2 sigma_p^2/m_N^2  (sigma_p = 1-D momentum spread)

so with ``q = sqrt(2 m_N E_R)`` and the zero-point spread ``sigma_p^2 = m_N w_p / 2``:

    sigma_E = q sigma_p / m_N = sqrt(2 m_N E_R) sqrt(m_N w_p/2) / m_N = sqrt(E_R w_p)

Units check with hbar restored: ``q`` and ``sigma_p`` in eV/c, ``m_N`` in eV/c^2, so
``q sigma_p/m_N`` is in eV.  No explicit hbar survives once the phonon energy is
carried as an energy rather than an angular frequency.

WHICH ``w_p``?  -- the check the closed form hides
--------------------------------------------------
``sigma_p^2 = m_N w/2`` and ``<u_x^2> = 1/(2 m_N w)`` share ONE ``w`` only for a
single-mode oscillator.  For a real VDOS they are different moments of ``g(w)``:

    w_u = [ int g(w)/w dw ]^-1     HARMONIC mean   -> governs <u_x^2>  -> the LOCKED omega_bar
    w_p =   int g(w) w dw          ARITHMETIC mean -> governs <p_x^2>

(both at T -> 0; derived in ``11-02-IA-WIDTH-DERIVATION.md`` from the same normal-mode
expansion that gives ``<u_x^2>``, with ``<p_x^2> = (m_N/2) int g w coth(w/2kT) dw``).

By Cauchy-Schwarz ``w_p >= w_u`` for any spectrum with spread, with equality only for a
single mode.  So the headline ``sigma_E = sqrt(E_R * omega_bar)`` built on the LOCKED
(harmonic) omega_bar **UNDERSTATES** the true impulse-approximation width by
``sqrt(w_p/w_u)``.  That factor is 9/8 -> sqrt(9/8) = 1.0607 for a Debye VDOS and
**1.1639 for the measured Ge spectrum**.

This module keeps the headline widths on the LOCKED omega_bar -- so that ROADMAP SC3's
stated identity ``sigma_E/E_R = 1/sqrt(2W)`` holds exactly -- and exposes the moment
correction as an explicit, LABELLED, ONE-SIDED systematic.  It does not silently switch
which mean is used.

IDENTITY FLAG (not a cross-check)
---------------------------------
``sigma_E/E_R = sqrt(omega_bar/E_R) = 1/sqrt(2W)`` is TRUE BY CONSTRUCTION once
``2W = E_R/omega_bar`` (CONVENTIONS.md Section J).  It holds for ANY omega_bar
whatsoever and is therefore not evidence for the width.  Reporting it as corroboration
is forbidden proxy ``fp-identity-as-evidence``.  The decisive content of SC3 is the
numerical values and the quadrature with the Phase-10 counting floor.

SCOPE
-----
``sigma_E`` is a NUCLEAR-recoil width, on the unified phonon scale with no ionization
quenching (CONVENTIONS Section B) -- never keVee.  Whether it applies to the muon and
Compton (ELECTRON-recoil) channels is an OPEN question assigned to Phase 15 by the
project contract.  This module neither applies it there nor answers the question.

Validity: the IA criterion is ``q >> sqrt(2 m_N omega_bar)``, i.e. ``E_R >> omega_bar``
(Campbell-Deem et al., Phys. Rev. D 106, 036019 (2022)), equivalently ``2W >> 1``.
``2W = 5.60`` at the 100 meV grid floor and rises linearly, so the criterion is
satisfied but not comfortably so in the bottom bin; the residual ``O(1/2W)`` correction
is quantified by plan 11-03.
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from . import params, phonon_scale

#: Fractional width of one extended-grid bin: 79.988714 bins/decade (plan 10-03),
#: so a bin spans 10^(1/79.988714) in energy.
EXT_GRID_BINS_PER_DECADE = 79.988714
ONE_BIN_FRACTIONAL_WIDTH = 10.0 ** (1.0 / EXT_GRID_BINS_PER_DECADE) - 1.0

#: Phase-10 counting floors at 0.49382 eV, PIPELINE-DERIVED from
#: artifacts/v2.0/response_matrix_*_ext.npz (10-05-COUNTING-FLOOR.md section 1),
#: not the ROADMAP comparison targets 15.9 % / 14.2 %.
#: BEST CASE WITH NO NOISE SOURCES -- see COUNTING_FLOOR_CAVEAT.
COUNTING_FLOOR_05eV = {"Ta->Al": 16.009e-2, "Al->Hf": 14.271e-2}
COUNTING_FLOOR_05eV_ROADMAP = {"Ta->Al": 15.9e-2, "Al->Hf": 14.2e-2}
COUNTING_FLOOR_ENERGY_eV = 0.49382

COUNTING_FLOOR_CAVEAT = (
    "BEST CASE WITH NO NOISE SOURCES: the Phase-10 counting floor is 1/sqrt(N_obs) "
    "quasiparticle counting statistics with no baseline, amplifier, phonon-collection, "
    "position or readout noise, and this project has no resolution parameter at all. "
    "It is NOT the detector resolution (fp-poisson-as-resolution)."
)


# --------------------------------------------------------------------------- #
# The width                                                                    #
# --------------------------------------------------------------------------- #
def sigma_E_eV(E_R_eV, omega_bar_eV_value: Optional[float] = None):
    """Impulse-approximation Gaussian width ``sigma_E = sqrt(E_R * omega_bar)`` in eV.

    Defaults to the LOCKED omega_bar (CONVENTIONS.md Section J, `params.OMEGA_BAR_eV`).
    """
    if omega_bar_eV_value is None:
        omega_bar_eV_value = params.OMEGA_BAR_eV.value
    return np.sqrt(np.asarray(E_R_eV, float) * omega_bar_eV_value)


def sigma_E_from_momentum_distribution(E_R_eV, omega_bar_eV_value: Optional[float] = None,
                                       m_N_eV: Optional[float] = None):
    """The SAME width, built the long way: ``sigma_E = q sigma_p / m_N``.

    Kept as a separate code path so the closed form is checked against the argument it
    came from rather than merely asserted.  ``m_N`` must cancel identically.
    """
    if omega_bar_eV_value is None:
        omega_bar_eV_value = params.OMEGA_BAR_eV.value
    if m_N_eV is None:
        m_N_eV = phonon_scale.ge_nuclear_mass_eV()
    q_eV = np.sqrt(2.0 * m_N_eV * np.asarray(E_R_eV, float))     # eV/c
    sigma_p_eV = np.sqrt(m_N_eV * omega_bar_eV_value / 2.0)      # eV/c
    return q_eV * sigma_p_eV / m_N_eV                            # eV


def mean_energy_transfer_eV(E_R_eV, m_N_eV: Optional[float] = None):
    """``<w> = q^2/(2 m_N)``, which must be exactly ``E_R``."""
    if m_N_eV is None:
        m_N_eV = phonon_scale.ge_nuclear_mass_eV()
    q_eV = np.sqrt(2.0 * m_N_eV * np.asarray(E_R_eV, float))
    return q_eV ** 2 / (2.0 * m_N_eV)


def fractional_width(E_R_eV, omega_bar_eV_value: Optional[float] = None):
    """``sigma_E/E_R = sqrt(omega_bar/E_R)``.

    Equals ``1/sqrt(2W)`` BY CONSTRUCTION -- an identity, not a check.
    """
    if omega_bar_eV_value is None:
        omega_bar_eV_value = params.OMEGA_BAR_eV.value
    return np.sqrt(omega_bar_eV_value / np.asarray(E_R_eV, float))


def sub_bin_crossing_energy_eV(omega_bar_eV_value: Optional[float] = None,
                               fractional_bin: float = ONE_BIN_FRACTIONAL_WIDTH) -> float:
    """E_R at which ``sigma_E/E_R`` equals one extended-grid bin width.

    Above this energy the broadening is SUB-BIN on the Phase-10 axis and cannot move
    counts between bins -- which is what "negligible above ~100 eV" actually means.
    """
    if omega_bar_eV_value is None:
        omega_bar_eV_value = params.OMEGA_BAR_eV.value
    return omega_bar_eV_value / fractional_bin ** 2


# --------------------------------------------------------------------------- #
# The moment systematic                                                        #
# --------------------------------------------------------------------------- #
def vdos_means(source: str = "ncrystal") -> dict:
    """``w_u`` (harmonic, governs <u_x^2>) and ``w_p`` (arithmetic, governs <p_x^2>).

    Returns energies in eV plus the one-sided width correction ``sqrt(w_p/w_u)``.
    """
    m = phonon_scale.vdos_moment_means(*phonon_scale.load_vdos(source))
    w_u = m["harmonic_mean_meV"] * 1e-3
    w_p = m["arithmetic_mean_meV"] * 1e-3
    return {
        "omega_bar_u_eV": w_u,
        "omega_bar_p_eV": w_p,
        "ratio": w_p / w_u,
        "sigma_correction": np.sqrt(w_p / w_u),
    }


def debye_vdos_means(theta_D_K: Optional[float] = None) -> dict:
    """The same diagnostic on the ANALYTIC Debye VDOS -- the oracle.

    Closed forms: ``w_p = 3 w_D/4``, ``w_u = 2 w_D/3``, ratio exactly ``9/8``.
    """
    if theta_D_K is None:
        theta_D_K = phonon_scale.GE_THETA_D_K
    w = phonon_scale.debye_grid(theta_D_K)
    m = phonon_scale.vdos_moment_means(w, phonon_scale.debye_vdos(w, theta_D_K))
    w_u = m["harmonic_mean_meV"] * 1e-3
    w_p = m["arithmetic_mean_meV"] * 1e-3
    return {
        "omega_bar_u_eV": w_u,
        "omega_bar_p_eV": w_p,
        "omega_D_eV": phonon_scale.K_B_eV_PER_K * theta_D_K,
        "ratio": w_p / w_u,
        "sigma_correction": np.sqrt(w_p / w_u),
    }


def sigma_E_upper_moment_eV(E_R_eV, source: str = "ncrystal"):
    """``sigma_E`` built on the ARITHMETIC mean -- the physically correct <p_x^2> route.

    Reported as a ONE-SIDED upper correction alongside the headline value, never
    substituted for it silently.
    """
    return sigma_E_eV(E_R_eV, vdos_means(source)["omega_bar_p_eV"])


# --------------------------------------------------------------------------- #
# Quadrature with the Phase-10 counting floor                                  #
# --------------------------------------------------------------------------- #
def quadrature_with_counting_floor(frac_width: float, design: str,
                                   floors: Optional[dict] = None) -> float:
    """``sqrt(sigma_frac^2 + floor_frac^2)`` for one design.

    Added in QUADRATURE, never linearly.  This assumes the two mechanisms are
    statistically INDEPENDENT: quasiparticle counting statistics in the sensor versus
    nuclear zero-point motion in the target lattice.  They arise from unrelated
    physics, but the independence is ASSERTED here, not proven.

    The floor is a %s
    """
    if floors is None:
        floors = COUNTING_FLOOR_05eV
    return float(np.hypot(frac_width, floors[design]))


quadrature_with_counting_floor.__doc__ = (
    quadrature_with_counting_floor.__doc__ % COUNTING_FLOOR_CAVEAT)


# --------------------------------------------------------------------------- #
# Plan 11-04: applying the convolution to dR/dE_R BEFORE the response chain    #
# --------------------------------------------------------------------------- #
#: Recorded default of the broadening switch, for Phase 12 to consume.
#: OFF, following the Phase-10 precedent that left ``shared_energy_grid`` defaulting
#: to ``v1.0``: a fail-safe default makes a silent change of physics impossible, and
#: turning the broadening on becomes a deliberate Phase-12 act rather than something
#: every existing call site inherits.  Flipping it is a Phase-12 decision, not a
#: refactor.
BROADENING_DEFAULT = False


def _normal_cdf(z):
    from scipy.special import ndtr
    return ndtr(z)


def broaden_counts(edges_eV, counts, *, omega_bar_eV=None, floor_eV=None):
    """Energy-dependent Gaussian convolution of a COUNTS histogram on ``edges_eV``.

    Works in counts (rate x bin width), not in the differential rate, so that
    conservation is a sum rather than a quadrature artefact.

    Each source bin i, centred at the geometric mean ``E_i`` of its edges, is spread
    over a Gaussian of width ``sigma_E(E_i) = sqrt(E_i * omega_bar)`` (plan 11-02).
    The mass delivered to target bin j is the exact CDF difference
    ``Phi((e_{j+1}-E_i)/sigma_i) - Phi((e_j-E_i)/sigma_i)``, so the redistribution
    of each source bin telescopes to exactly 1 across
    ``(-inf, e_0) u [e_0, e_N] u (e_N, +inf)``.

    Returns ``(out_counts, leakage)``.  ``leakage`` carries ``below_floor``,
    ``below_zero`` (a SUBSET of below_floor), ``above_top``, and the per-source-bin
    breakdowns.  **Nothing is rescaled after the convolution.**  The mass that lands
    below the axis floor and below zero is REPORTED, because at 100 meV the fractional
    width is 42 % and roughly half a bottom-bin kernel genuinely falls off the axis
    (plan 11-03 predicts 48.6-49.9 % analytically).  Rescaling to make the retained
    grid sum to the input would manufacture counts the physics does not produce and
    would hide the one place the symmetric Gaussian is known to fail
    (``fp-rescale-to-conserve``).

    Strict linearity in the input amplitude is a consequence and is unit-tested: the
    redistribution matrix does not depend on the counts.
    """
    if omega_bar_eV is None:
        omega_bar_eV = params.OMEGA_BAR_eV.value
    edges = np.asarray(edges_eV, float)
    counts = np.asarray(counts, float)
    if edges.size != counts.size + 1:
        raise ValueError(f"{edges.size} edges for {counts.size} bins")
    if floor_eV is None:
        floor_eV = float(edges[0])

    zero = {"below_floor": 0.0, "below_zero": 0.0, "above_top": 0.0,
            "below_floor_per_bin": np.zeros_like(counts),
            "below_zero_per_bin": np.zeros_like(counts),
            "above_top_per_bin": np.zeros_like(counts),
            "sigma_eV": np.zeros_like(counts)}
    if omega_bar_eV == 0.0:
        # EXACT identity at zero width -- returned bit-for-bit, not as a limit.
        return counts.copy(), zero

    centres = np.sqrt(edges[:-1] * edges[1:])
    sigma = np.sqrt(centres * omega_bar_eV)
    z = (edges[None, :] - centres[:, None]) / sigma[:, None]
    cdf = _normal_cdf(z)                                   # (n_src, n_edges)

    frac = cdf[:, 1:] - cdf[:, :-1]                        # (n_src, n_tgt)
    out = counts @ frac

    below = counts * cdf[:, 0]
    above = counts * (1.0 - cdf[:, -1])
    below_zero = counts * _normal_cdf((0.0 - centres) / sigma)

    leak = {
        "below_floor": float(below.sum()),
        "below_zero": float(below_zero.sum()),
        "above_top": float(above.sum()),
        "below_floor_per_bin": below,
        "below_zero_per_bin": below_zero,
        "above_top_per_bin": above,
        "sigma_eV": sigma,
    }
    return out, leak


def native_edges(T_eV):
    """Bin edges around a set of tabulated recoil knots, geometric midpoints."""
    T = np.asarray(T_eV, float)
    inner = np.sqrt(T[:-1] * T[1:])
    return np.concatenate([[T[0] ** 2 / inner[0]], inner, [T[-1] ** 2 / inner[-1]]])


def broaden_native_spectrum(T_eV, dRdT, band=None, *, omega_bar_eV=None,
                            floor_eV=None, require_floor_coverage=False):
    """Broaden a dR/dT spectrum on its OWN tabulated recoil knots.

    This is the shipped entry point, and it acts on the RECOIL axis strictly upstream
    of ``fold.rebin_cevns_to_edep_grid`` and therefore upstream of ``R(E_rec|E_dep)``
    (``fp-broadening-after-response``).  The IA width is a property of the nuclear
    recoil, not of the sensor.

    ``require_floor_coverage=True`` asserts that the table's own support reaches down
    to ``floor_eV``.  It RAISES when it does not -- deliberately, and in the same
    spirit as ``interp_guard``: the frozen v1.0 CEvNS table starts at 5 eV and carries
    no data below it, so producing a broadened spectrum down to the 0.0999350 eV
    extended-grid floor from that table would be pure extrapolation into a region the
    table never covered.  There is no try/except and no clamp anywhere on this path;
    the sub-eV spectrum is RECOMPUTED from ``cevns.differential_rate`` instead.

    Returns ``(T_eV, dRdT_broadened, band_broadened_or_None, leakage)``.
    """
    T = np.asarray(T_eV, float)
    if require_floor_coverage:
        if floor_eV is None:
            raise ValueError("require_floor_coverage=True needs an explicit floor_eV")
        if T[0] > floor_eV:
            raise ValueError(
                f"recoil table support starts at {T[0]!r} eV but the kernel was asked "
                f"to reach {floor_eV!r} eV. This table carries NO DATA below its floor; "
                "broadening into that region would be extrapolation, not convolution. "
                "Recompute dR/dT there instead of clamping or zero-filling.")
    edges = native_edges(T)
    dE_keV = np.diff(edges) / 1.0e3
    out, leak = broaden_counts(edges, np.asarray(dRdT, float) * dE_keV,
                               omega_bar_eV=omega_bar_eV, floor_eV=floor_eV)
    y = out / dE_keV
    b = None
    if band is not None:
        ob, _ = broaden_counts(edges, np.asarray(band, float) * dE_keV,
                               omega_bar_eV=omega_bar_eV, floor_eV=floor_eV)
        b = ob / dE_keV
    return T, y, b, leak
