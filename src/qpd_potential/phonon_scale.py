# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Phonon energy scale and Debye-Waller convention for Ge (CALC-14, plan 11-01).

CONVENTIONS.md Section J is the human-readable projection of what this module computes.

Definitions used here, and nowhere departed from
-----------------------------------------------
VDOS normalization (stated because the alternative differs by exactly the factor
this module exists to guard against)::

    int g(w) dw = 1        over the full support, w an ENERGY (meV), g in 1/meV

With that normalization the harmonic-lattice mean-square displacement is

    <u^2>_3D(T) = (3 hbar^2 / (2 m_N)) * int [ g(w)/w * coth( w / (2 k_B T) ) ] dw
    <u_x^2>     = <u^2>_3D / 3

The leading 3 counts the three Cartesian branches per atom; it belongs with
``int g dw = 1``.  Had ``g`` been normalized to 3 instead, the 3 would have to go.

For cubic Ge (spacegroup 227) the MSD tensor is isotropic, so ``<u_x^2> = <u^2>/3``
is EXACT by symmetry, not an approximation.  That is why applying ``/3`` a *second*
time inside the Debye-Waller exponent is a bug and not a convention choice::

    2W(E_R) = q^2 <u_x^2>,   q = sqrt(2 m_N E_R)      # CORRECT (1-D MSD)
    2W(E_R) = q^2 <u^2> / 3                            # REJECTED: double-counted projection

    omega_bar == hbar^2 / (2 m_N <u_x^2>)              # effective phonon energy
    B         = 8 pi^2 <u_x^2>                         # crystallographic B factor

Two exact algebraic consequences, both used as identity checks and NEITHER of which
is independent corroboration of anything
----------------------------------------------------------------------------------
1. ``2W = q^2 <u_x^2> = 2 m_N E_R <u_x^2> = E_R / omega_bar``.  Substituting
   ``q^2 = 2 m_N E_R`` turns one expression into the other.  Reporting the
   momentum-transfer route as an INDEPENDENT confirmation of ``2W`` is forbidden
   proxy ``fp-q-route-as-independent``.  It is a units-and-arithmetic check.
2. ``m_N cancels out of omega_bar entirely``:

       <u_x^2> = (hbar^2 / 2 m_N) * I,  I = int g(w)/w dw   (at T -> 0)
       omega_bar = hbar^2 / (2 m_N <u_x^2>) = 1 / I

   so ``omega_bar`` is the **harmonic mean** of the VDOS and ``2W = E_R * I = E_R/omega_bar``
   is mass-free.  Only ``<u_x^2>`` and ``B`` depend on ``m_N``.  This is not a
   coincidence to be admired -- it is the reason a mass error would show up in
   ``<u_x^2>`` but not in ``2W``, and the reason the ``omega_bar`` lock is robust
   against the 0.10% ambiguity in how natural-Ge mass is averaged.

The harmonic-mean identity also matters downstream: ``<u_x^2>`` is governed by the
HARMONIC mean of the VDOS, whereas ``<p_x^2>`` -- which sets the impulse-approximation
Gaussian width ``sigma_E`` -- is governed by the ARITHMETIC mean.  They coincide only
for a single mode.  See ``vdos_moment_means`` and plan 11-02.

Nuclear mass
------------
Natural abundance-weighted Ge from ``params.GE_ISOTOPES`` (M_i = A_i * 931.494 MeV,
CIAAW representative atom fractions), i.e. the Phase-7 nuclear-data lock.  NCrystal's
``Ge_sg227.ncmat`` carries 72.632248855 amu (real isotope masses); the two differ by
0.10%, which is 100x below every tolerance in this phase.  ``omega_bar`` and ``2W`` are
mass-free (above), so the ambiguity touches only ``<u_x^2>`` and ``B``.

Temperature
-----------
The locked evaluation point is ``T -> 0`` (``coth -> 1`` EXACTLY, not numerically).
Justification is measured, not asserted: at T = 10 mK the full ``coth`` form differs
from the T -> 0 limit by ``< 1e-8`` relative, because the VDOS low-energy edge sits at
3.771 meV against ``k_B T = 0.862 ueV``.  ``mean_square_displacement_1d`` accepts a
temperature so the 300 K value -- where the experimental B-factor anchor of the survey
band was measured -- can be reported alongside rather than hand-waved.

Interpreter: ``/opt/anaconda3/bin/python3`` (numpy 1.26.4; scipy is not required here
and is absent from the gpd venv).
"""

from __future__ import annotations

import os
from typing import Optional, Tuple

import numpy as np

from . import params

# --------------------------------------------------------------------------- #
# Physical constants                                                           #
# --------------------------------------------------------------------------- #
#: hbar*c in eV*angstrom (CODATA 2018: 197.3269804 MeV*fm).  Applied EXACTLY ONCE
#: on each path: once in the <u_x^2> prefactor (hbar c)^2 / (2 m_N c^2), and once in
#: the q conversion eV/c -> 1/angstrom.
HBAR_C_eV_ANGSTROM = 1973.269804

#: Boltzmann constant in eV/K (CODATA 2018, exact by SI definition).  k_B is kept
#: EXPLICIT project-wide (CONVENTIONS Section A.3); it is never set to 1.
K_B_eV_PER_K = 8.617333262e-5

#: Debye temperature of Ge used ONLY as the input to the analytic oracle.  It is a
#: comparison baseline, never a source of the locked omega_bar (fp-debye-substitute).
GE_THETA_D_K = 374.0

_HERE = os.path.dirname(os.path.abspath(__file__))
_VDOS_DIR = os.path.join(os.path.dirname(os.path.dirname(_HERE)), "data", "external", "ge_vdos")

VDOS_SOURCES = {
    "ncrystal": "ge_vdos_normalized.csv",
    "darkelf": "ge_vdos_darkelf_normalized.csv",
}


# --------------------------------------------------------------------------- #
# Nuclear mass                                                                 #
# --------------------------------------------------------------------------- #
def ge_nuclear_mass_eV() -> float:
    """Natural abundance-weighted Ge nuclear mass in eV (i.e. m_N c^2).

    Weighted with the CIAAW representative atom fractions already locked in
    ``params.GE_ISOTOPES``; M_i = A_i * 931.494 MeV, the Phase-7 convention.
    """
    return 1.0e6 * sum(iso.abundance * iso.M_MeV for iso in params.GE_ISOTOPES)


# --------------------------------------------------------------------------- #
# VDOS handling                                                                #
# --------------------------------------------------------------------------- #
def load_vdos(source: str = "ncrystal") -> Tuple[np.ndarray, np.ndarray]:
    """Load a frozen, normalized Ge VDOS.

    Returns ``(omega_meV, g_per_meV)`` with ``int g dw = 1``.  No Ge number is
    hard-coded anywhere in this module: everything reads these tables.
    """
    try:
        fname = VDOS_SOURCES[source]
    except KeyError:
        raise ValueError(
            f"unknown VDOS source {source!r}; expected one of {sorted(VDOS_SOURCES)}"
        ) from None
    path = os.path.join(_VDOS_DIR, fname)
    rows = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("omega_meV"):
                continue
            a, b = line.split(",")
            rows.append((float(a), float(b)))
    data = np.asarray(rows, dtype=float)
    omega, g = data[:, 0], data[:, 1]
    if np.any(omega <= 0.0):
        raise ValueError(f"{fname}: VDOS grid must be strictly positive (g/w is integrated)")
    if not np.all(np.diff(omega) > 0):
        raise ValueError(f"{fname}: VDOS grid must be strictly increasing")
    return omega, g


def normalize_vdos(omega: np.ndarray, g: np.ndarray) -> np.ndarray:
    """Renormalize so that ``int g dw = 1`` over the tabulated support."""
    return np.asarray(g, float) / np.trapz(np.asarray(g, float), np.asarray(omega, float))


def vdos_ceiling_meV(source: str = "ncrystal") -> float:
    """Top of the frozen VDOS support, in meV -- the highest tabulated grid point.

    Deliberately the grid endpoint, NOT the last grid point with non-zero density.
    The NCrystal spectrum terminates by having ``g = 0`` exactly at its final row
    (37.78966 meV); reading "last non-zero" would report the point one spacing below
    and understate the measured ceiling by 0.080 meV.
    """
    omega, _ = load_vdos(source)
    return float(omega[-1])


def vdos_last_nonzero_meV(source: str = "ncrystal") -> float:
    """Highest grid point at which the density is strictly positive, in meV."""
    omega, g = load_vdos(source)
    nz = np.nonzero(g)[0]
    return float(omega[nz[-1]]) if len(nz) else float(omega[-1])


def vdos_weight_quantile_meV(source: str = "ncrystal", quantile: float = 1e-3) -> float:
    """Energy below which the given fraction of the spectral weight lies, in meV.

    A grid-independent stand-in for "the low-energy edge".  The raw first grid point
    is not usable for that purpose here: the NCrystal table carries an explicit
    parabolic segment reaching 1e-9 meV (MANIFEST section 3.2), so its literal
    minimum is a quadrature detail, not a physical edge.  What actually justifies the
    T -> 0 reduction is measured directly instead -- see the T = 10 mK row in
    ``11-01-VDOS-DETERMINATION.md``.
    """
    omega, g = load_vdos(source)
    cdf = np.concatenate([[0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) * np.diff(omega))])
    cdf /= cdf[-1]
    return float(np.interp(quantile, cdf, omega))


# --------------------------------------------------------------------------- #
# Mean-square displacement                                                     #
# --------------------------------------------------------------------------- #
def thermal_factor(omega_meV: np.ndarray, temperature_K: Optional[float]) -> np.ndarray:
    """``coth( w / (2 k_B T) )``, or EXACTLY 1.0 when ``temperature_K is None``.

    ``temperature_K=None`` is the locked T -> 0 evaluation point and returns the
    exact limit rather than a coth evaluated at a small-but-finite T, so the
    ``omega_bar`` lock does not depend on a chosen "small enough" temperature.
    """
    omega_meV = np.asarray(omega_meV, float)
    if temperature_K is None:
        return np.ones_like(omega_meV)
    if temperature_K <= 0.0:
        raise ValueError("temperature_K must be > 0, or None for the exact T -> 0 limit")
    x = (omega_meV * 1e-3) / (2.0 * K_B_eV_PER_K * temperature_K)
    return 1.0 / np.tanh(x)


def mean_square_displacement_1d(
    omega_meV: np.ndarray,
    g_per_meV: np.ndarray,
    temperature_K: Optional[float] = None,
    m_N_eV: Optional[float] = None,
) -> float:
    """1-D mean-square displacement ``<u_x^2>`` in angstrom^2.

        <u_x^2> = (hbar c)^2 / (2 m_N c^2) * int [ g(w)/w * coth(w / 2 k_B T) ] dw

    ``g`` must satisfy ``int g dw = 1``; it is renormalized defensively here so a
    caller-supplied analytic VDOS cannot silently carry a different normalization.
    """
    omega_meV = np.asarray(omega_meV, float)
    g = normalize_vdos(omega_meV, g_per_meV)
    if m_N_eV is None:
        m_N_eV = ge_nuclear_mass_eV()
    omega_eV = omega_meV * 1e-3
    g_per_eV = g * 1e3                      # g dw is invariant: g_eV = g_meV * 1e3
    integrand = g_per_eV / omega_eV * thermal_factor(omega_meV, temperature_K)
    integral = np.trapz(integrand, omega_eV)          # units 1/eV
    return HBAR_C_eV_ANGSTROM ** 2 / (2.0 * m_N_eV) * integral


def mean_square_displacement_3d(
    omega_meV: np.ndarray,
    g_per_meV: np.ndarray,
    temperature_K: Optional[float] = None,
    m_N_eV: Optional[float] = None,
) -> float:
    """``<u^2>_3D = 3 <u_x^2>``, angstrom^2.  Exact for cubic Ge by symmetry."""
    return 3.0 * mean_square_displacement_1d(omega_meV, g_per_meV, temperature_K, m_N_eV)


# --------------------------------------------------------------------------- #
# Derived scales                                                               #
# --------------------------------------------------------------------------- #
def omega_bar_eV(u_x_sq_A2: float, m_N_eV: Optional[float] = None) -> float:
    """``omega_bar = (hbar c)^2 / (2 m_N c^2 <u_x^2>)`` in eV."""
    if m_N_eV is None:
        m_N_eV = ge_nuclear_mass_eV()
    return HBAR_C_eV_ANGSTROM ** 2 / (2.0 * m_N_eV * u_x_sq_A2)


def momentum_transfer(E_R_eV, m_N_eV: Optional[float] = None):
    """``q = sqrt(2 m_N E_R)`` returned as ``(q_keV_per_c, q_inv_angstrom)``.

    UNITS CHECK ONLY.  ``q`` is not an independent handle on 2W: see the module
    docstring and forbidden proxy ``fp-q-route-as-independent``.
    """
    if m_N_eV is None:
        m_N_eV = ge_nuclear_mass_eV()
    q_eV = np.sqrt(2.0 * m_N_eV * np.asarray(E_R_eV, float))
    return q_eV * 1e-3, q_eV / HBAR_C_eV_ANGSTROM


def two_W(E_R_eV, u_x_sq_A2: float, m_N_eV: Optional[float] = None):
    """Debye-Waller exponent ``2W = q^2 <u_x^2>`` with the **1-D** MSD, dimensionless.

    NEVER ``q^2 <u^2> / 3``: the ``/3`` is the isotropic projection, which for cubic
    Ge is exact and has ALREADY been applied in ``<u_x^2>``.  Applying it again is
    forbidden proxy ``fp-factor-three`` and changes 2W (and hence every sub-eV width)
    by a factor 3.

    This quantity is used to SIZE the impulse-approximation broadening.  The rate is
    never multiplied by ``exp(-2W)``: that factor suppresses only the zero-phonon
    (coherent) channel, whose strength has moved into the multiphonon continuum, and
    using it as a rate suppression would erase a real signal (milestone-wide
    prohibition; CONVENTIONS Section J).
    """
    _, q_invA = momentum_transfer(E_R_eV, m_N_eV)
    return q_invA ** 2 * u_x_sq_A2


def two_W_from_omega_bar(E_R_eV, omega_bar_eV_value: float):
    """``2W = E_R / omega_bar`` -- ALGEBRAICALLY THE SAME EXPRESSION as ``two_W``."""
    return np.asarray(E_R_eV, float) / omega_bar_eV_value


def debye_waller_B(u_x_sq_A2: float) -> float:
    """Crystallographic B factor ``B = 8 pi^2 <u_x^2>`` in angstrom^2."""
    return 8.0 * np.pi ** 2 * u_x_sq_A2


# --------------------------------------------------------------------------- #
# VDOS moments -- the harmonic/arithmetic mean mismatch (feeds plan 11-02)      #
# --------------------------------------------------------------------------- #
def vdos_moment_means(omega_meV: np.ndarray, g_per_meV: np.ndarray) -> dict:
    """Harmonic and arithmetic means of the VDOS, and their ratio.

    ``<u_x^2> ~ <1/w>`` (harmonic mean) while ``<p_x^2> ~ <w>`` (arithmetic mean).
    The two coincide only for a single mode.  For a Debye VDOS the ratio
    ``<w> * <1/w>`` is exactly 9/8; for a real spectrum it is larger.  Any
    single-frequency ``sigma_E = sqrt(E_R omega_bar)`` built on the harmonic mean
    therefore UNDERSTATES the width by ``sqrt(<w><1/w>)``.
    """
    omega_meV = np.asarray(omega_meV, float)
    g = normalize_vdos(omega_meV, g_per_meV)
    inv = np.trapz(g / omega_meV, omega_meV)      # <1/w>, 1/meV
    ari = np.trapz(g * omega_meV, omega_meV)      # <w>, meV
    return {
        "harmonic_mean_meV": 1.0 / inv,
        "arithmetic_mean_meV": ari,
        "mean_ratio": ari * inv,                  # <w><1/w>, dimensionless, >= 1
    }


# --------------------------------------------------------------------------- #
# Analytic Debye oracle -- independent of every Ge data file                    #
# --------------------------------------------------------------------------- #
def debye_vdos(omega_meV: np.ndarray, theta_D_K: float = GE_THETA_D_K) -> np.ndarray:
    """Analytic Debye VDOS ``g(w) = 3 w^2 / w_D^3`` on ``[0, w_D]``, w_D = k_B theta_D.

    Already satisfies ``int g dw = 1``; zero above w_D.
    """
    omega_meV = np.asarray(omega_meV, float)
    w_D = K_B_eV_PER_K * theta_D_K * 1e3          # meV
    return np.where(omega_meV <= w_D, 3.0 * omega_meV ** 2 / w_D ** 3, 0.0)


def debye_msd_3d_closed_form(
    theta_D_K: float = GE_THETA_D_K, m_N_eV: Optional[float] = None
) -> float:
    """``<u^2>_3D = 9 hbar^2 / (4 m_N k_B theta_D)`` in angstrom^2, T -> 0.

    Derivation (not pasted -- it is one line):
    ``(3 hbar^2/2m) int_0^{w_D} (3 w^2/w_D^3)/w dw = (3 hbar^2/2m)(3/2 w_D) = 9 hbar^2/(4 m w_D)``
    with ``w_D = k_B theta_D``.
    """
    if m_N_eV is None:
        m_N_eV = ge_nuclear_mass_eV()
    return 9.0 * HBAR_C_eV_ANGSTROM ** 2 / (4.0 * m_N_eV * K_B_eV_PER_K * theta_D_K)


def debye_grid(theta_D_K: float = GE_THETA_D_K, n: int = 200_001) -> np.ndarray:
    """Quadrature grid for the Debye oracle, in meV, excluding w = 0."""
    w_D = K_B_eV_PER_K * theta_D_K * 1e3
    return np.linspace(0.0, w_D, n)[1:]


# --------------------------------------------------------------------------- #
# One-call summary                                                             #
# --------------------------------------------------------------------------- #
def derive(source: str = "ncrystal",
           temperature_K: Optional[float] = None,
           m_N_eV: Optional[float] = None) -> dict:
    """Every phonon-scale scalar for one VDOS source, at one temperature."""
    omega, g = load_vdos(source)
    if m_N_eV is None:
        m_N_eV = ge_nuclear_mass_eV()
    ux2 = mean_square_displacement_1d(omega, g, temperature_K, m_N_eV)
    wbar = omega_bar_eV(ux2, m_N_eV)
    out = {
        "source": source,
        "temperature_K": temperature_K,
        "m_N_eV": m_N_eV,
        "u_x_sq_A2": ux2,
        "u_sq_3d_A2": 3.0 * ux2,
        "omega_bar_eV": wbar,
        "omega_bar_meV": wbar * 1e3,
        "B_A2": debye_waller_B(ux2),
        "ceiling_meV": vdos_ceiling_meV(source),
        "last_nonzero_meV": vdos_last_nonzero_meV(source),
        "weight_q001_meV": vdos_weight_quantile_meV(source, 1e-3),
    }
    out.update(vdos_moment_means(omega, g))
    return out
