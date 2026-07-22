# ASSERT_CONVENTION: natural_units=io_MeV, energy_input=MeV, spectrum_units=nubar_per_fission_per_MeV
"""
Sub-1.8 MeV extension of the per-fission reactor antineutrino spectrum:
  (a) per-isotope fission "summation" shape below ~2 MeV, and
  (b) the 238U(n,gamma)239U->239Np neutron-capture antineutrino component.

SOURCING STATUS (fetch-not-invent contract, honest accounting):

  * 238U(n,gamma) NORMALIZATION (~0.6 nu-bar/fission, E_nu <~ 1.3 MeV):
        SOURCED -- Kopeikin, Mikaelyan, Sinev, Phys. At. Nucl. 67, 1892 (2004),
        hep-ph/0308186; Huber & Jaffke, PRL 116, 122503 (2016).
  * 238U(n,gamma) SHAPE:
        COMPUTED from SOURCED beta endpoints (AME2020 Q-values) via the allowed-beta
        antineutrino spectral function (F=1, no-Coulomb approximation). Q-values:
        239U ->239Np  Q_beta = 1.263 MeV;   239Np->239Pu  Q_beta = 0.722 MeV
        (AME2020, Wang et al., Chin. Phys. C 45, 030003 (2021)). Two nu-bar per capture.
        Shape confidence: MEDIUM (allowed approximation; Coulomb/forbidden corrections
        neglected). This is a short first-principles computation, NOT invented coefficients.

  * SUB-2 MeV FISSION SUMMATION per-isotope shape:
        SOURCING GAP. A primary digitized Estienne-Fallot 2019 / CONFLUX per-isotope
        sub-1.8 MeV antineutrino table could NOT be obtained in this environment
        (Huber PRC84 and Mueller PRC83 tabulations both stop at 2.0 MeV; running the
        full CONFLUX ENDF summation is out of plan scope). Per the fetch-not-invent
        rule we do NOT invent a summation table. Instead we provide a TRANSPARENT,
        seam-anchored allowed-beta-like continuation as an explicit MODEL PLACEHOLDER
        so the pipeline is functional end-to-end; it is flagged as such in the data
        provenance and in the SUMMARY, and must be replaced by a real EF/CONFLUX table
        in Plan 02-02. It is NOT the forbidden proxy fp-truncate-ibd: the sub-IBD flux
        is populated (not dropped) with a physical, non-negative, rising shape, and the
        continuation is exponential (bounded), not a blind power-law of the HM fit.
"""
from __future__ import annotations

import os
import numpy as np

# --- Sourced physical constants ---------------------------------------------------
M_E = 0.510998950  # MeV, electron mass (CODATA)

# AME2020 beta-minus Q-values for the 238U(n,gamma) chain [MeV]
Q_239U = 1.263    # 239U  -> 239Np
Q_239NP = 0.722   # 239Np -> 239Pu
NCAPTURE_YIELD_PER_FISSION = 0.6   # nu-bar/fission, Kopeikin 2004 / Huber-Jaffke 2016

_DATADIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "flux"))


# --- Allowed-beta antineutrino spectral shape -------------------------------------
def allowed_beta_nu_shape(E_nu, Q):
    """Unnormalized allowed-beta antineutrino spectrum for endpoint Q (MeV), F=1.

    Kinematics (neglecting nuclear recoil): E_nu = W0 - W with W0 = Q + m_e the
    electron endpoint total energy and W the electron total energy. The allowed
    electron spectrum ~ p_e * W * (W0 - W)^2 becomes, in E_nu = W0 - W:

        dN/dE_nu ~ E_nu^2 * (W0 - E_nu) * sqrt((W0 - E_nu)^2 - m_e^2),   0 < E_nu < Q
    """
    E = np.asarray(E_nu, dtype=float)
    W0 = Q + M_E
    W = W0 - E                       # electron total energy
    p2 = W * W - M_E * M_E           # electron momentum^2
    shape = np.where((E > 0) & (E < Q) & (p2 > 0), E * E * W * np.sqrt(np.clip(p2, 0, None)), 0.0)
    return shape


def ncapture_spectrum(E_grid):
    """238U(n,gamma) capture antineutrino spectrum on E_grid [MeV].

    Sum of the two allowed-beta branches (239U, 239Np), normalized so the TOTAL
    integral over the grid equals NCAPTURE_YIELD_PER_FISSION (0.6 nu-bar/fission).
    Returns nu-bar/fission/MeV.
    """
    E = np.asarray(E_grid, dtype=float)
    s1 = allowed_beta_nu_shape(E, Q_239U)
    s2 = allowed_beta_nu_shape(E, Q_239NP)
    # normalize each branch to 1 antineutrino, then scale total to the sourced yield
    def _norm(s):
        area = np.trapz(s, E)
        return s / area if area > 0 else s
    total = _norm(s1) + _norm(s2)                  # 2 nu-bar per capture (area = 2)
    total *= NCAPTURE_YIELD_PER_FISSION / np.trapz(total, E)
    return total


# --- Sub-2 MeV fission summation shape (MODEL PLACEHOLDER) -------------------------
def summation_shape_placeholder(E_grid, low_log_slope, E_ref=2.0):
    """Seam-anchored allowed-beta-like fission summation PLACEHOLDER shape.

    Rises toward low energy but FLATTENS (does not blow up) at low E, matching the
    qualitative behaviour of ensemble fission-product antineutrino spectra. We model
    the log-flux with an energy-dependent log-slope that scales linearly toward zero:

        d(ln S)/dE = low_log_slope * (E / E_ref)   ->   ln S(E) = low_log_slope * (E^2 - E_ref^2) / (2 E_ref)

    so that (i) S(E_ref)=1, and (ii) the log-slope AT the seam equals ``low_log_slope``
    (the isotope's Huber-Mueller log-derivative at 2 MeV) -- preserving the C1 seam anchor
    -- while the slope relaxes toward 0 at E->0 instead of diverging (a single physical
    "low-energy flattening" assumption, not tuned to any integral target). Arbitrary
    overall normalization -- the assembler rescales onto the sourced HM curve via c_i.

    THIS IS A DOCUMENTED PLACEHOLDER for the un-fetchable EF/CONFLUX summation table.
    """
    E = np.asarray(E_grid, dtype=float)
    return np.exp(low_log_slope * (E * E - E_ref * E_ref) / (2.0 * E_ref))
