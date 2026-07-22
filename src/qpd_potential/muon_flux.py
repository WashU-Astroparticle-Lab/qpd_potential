# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
#
# Sea-level cosmic-ray muon flux: modified-Gaisser ("Gaisser-Guan") angular /
# energy differential intensity and the surface-flux sampling measure for the
# Phase-4 muon deposited-energy channel (Plan 04-01).
#
# PARAMETERS TAKEN VERBATIM from GPD/literature/METHODS.md Domain 2 (verified
# against Guan, Chu, Wang, Yu, arXiv:1509.06176). NOT transcribed from memory.
#
#   dI/dE_mu = 0.14 * [ (E/GeV) (1 + 3.64 GeV/(E cos*^1.29)) ]^{-2.7}
#              * [ 1/(1 + 1.1 E cos*/115 GeV) + 0.054/(1 + 1.1 E cos*/850 GeV) ]
#   cos* = sqrt[ (cos^2 t + P1^2 + P2 cos^P3 t + P4 cos^P5 t)/(1 + P1^2 + P2 + P4) ]
#   P1=0.102573 P2=-0.068287 P3=0.958633 P4=0.0407253 P5=0.817285
#   units: cm^-2 s^-1 sr^-1 GeV^-1
#
# Surface-flux measure (guards RESEARCH Pitfall 3 / fp-angular-bias): the rate of
# muons crossing the wafer within dOmega dE is dI/dE * A_proj(Omega) dOmega dE,
# where A_proj is the convex-body projected area (wafer_geometry.projected_area).
# The extra projection cos(theta_n) is folded into A_proj = sum_a A_a|Omega_a|,
# and the solid-angle Jacobian sin(theta) enters the theta integral -- so the
# effective zenith weight is I(theta) * A_proj * sin(theta), NOT bare cos^2 theta.

from __future__ import annotations

import numpy as np
from scipy import integrate

# Gaisser-Guan effective-angle parameters (METHODS.md Domain 2, verbatim).
P1 = 0.102573
P2 = -0.068287
P3 = 0.958633
P4 = 0.0407253
P5 = 0.817285

_COS_STAR_DEN = 1.0 + P1**2 + P2 + P4


def cos_theta_star(cos_theta: np.ndarray) -> np.ndarray:
    """Earth-curvature effective angle cos(theta*) (Guan et al., arXiv:1509.06176)."""
    c = np.asarray(cos_theta, dtype=float)
    c = np.clip(c, 1e-6, 1.0)
    num = c**2 + P1**2 + P2 * c**P3 + P4 * c**P5
    return np.sqrt(np.clip(num / _COS_STAR_DEN, 0.0, None))


def dI_dE(E_gev: np.ndarray, cos_theta: np.ndarray) -> np.ndarray:
    """Gaisser-Guan differential intensity dI/dE_mu [cm^-2 s^-1 sr^-1 GeV^-1]."""
    E = np.asarray(E_gev, dtype=float)
    cs = cos_theta_star(cos_theta)
    base = 0.14 * (E * (1.0 + 3.64 / (E * cs**1.29))) ** (-2.7)
    bracket = 1.0 / (1.0 + 1.1 * E * cs / 115.0) + 0.054 / (1.0 + 1.1 * E * cs / 850.0)
    return base * bracket


def vertical_intensity(e_min: float = 1.0, e_max: float = 1.0e5) -> float:
    """Vertical (theta=0) integral intensity I_v = int dI/dE dE [cm^-2 s^-1 sr^-1].

    PDG anchor: I_v ~= 70 m^-2 s^-1 sr^-1 for E_mu > 1 GeV (VALD-02 flux anchor).
    """
    val, _ = integrate.quad(lambda E: dI_dE(E, 1.0), e_min, e_max, limit=200)
    return float(val)


# --------------------------------------------------------------------------- #
# Energy proposal for importance sampling: p(E) ~ E^{-alpha} on [Emin, Emax]   #
# (matches the steep vertical spectrum so flux/proposal weights are O(1)).     #
# --------------------------------------------------------------------------- #
def sample_energy(n: int, rng: np.random.Generator, e_min: float, e_max: float,
                  alpha: float = 2.7):
    """Draw E from p(E) = C E^{-alpha}; return (E, pdf) for importance weighting."""
    one_ma = 1.0 - alpha
    lo = e_min**one_ma
    hi = e_max**one_ma
    u = rng.random(n)
    E = (u * (hi - lo) + lo) ** (1.0 / one_ma)
    norm = one_ma / (hi - lo)  # so that int p dE = 1
    pdf = norm * E**(-alpha)
    return E, pdf
