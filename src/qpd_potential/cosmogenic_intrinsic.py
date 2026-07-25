# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Ge-intrinsic cosmogenic-activation backgrounds: 3H, 68Ge, 65Zn.

These are decays of isotopes produced by cosmic-ray activation of the germanium
DURING its above-ground history. They live INSIDE the crystal, so no shield or
veto removes them (unlike the thermal-neutron-driven capture recoil and in-situ
71Ge EC, which a B4C thermal shield eliminates). They are therefore drawn at FULL
rate -- NO suppression factor -- in the "NUCLEUS-equivalent suppression" figure,
which is the whole point: they are the residual floor a shield cannot touch, and
they are Ge-SPECIFIC (CaWO4/Al2O3 do not make them).

They are studied by the Ge CEvNS / dark-matter community and validated externally:
CONUS+ (arXiv:2501.05206v3, l.228) carries exactly 3H, 68Ge, 65Zn (and 68Ga) in
its background model and uses the 68Ge/71Ge EC K/L/M lines for calibration.

NORMALIZATION (frozen scenario)
-------------------------------
Rates from data/activation_scenario_v1.1.csv, the Phase-7 default t_exp = 1 yr,
t_cool = 0 (continuous surface exposure -- correct for a surface experiment,
where activation keeps building during the run rather than decaying):

    3H   : 4.05  dec/kg/day   beta-, Q = 18.6 keV endpoint (in-band continuum)
    68Ge : 18.22 dec/kg/day   EC -> 68Ga daughter (Ga X-rays/Auger, SAME lines as 71Ge)
    65Zn : 10.98 dec/kg/day   EC -> 65Cu daughter (Cu X-rays/Auger)

Production rates: CDMSlite/SuperCDMS (Amman et al., APh 105, 44 (2019),
arXiv:1806.07043), cross-checked EDELWEISS-III (arXiv:1607.04560). The end-of-year
activity is representative-to-slightly-conservative: over the run the activity
grows from the crystal's starting point, and pre-run surface handling adds to it.

WHAT IS DEPOSITED
-----------------
* 3H beta: the electron kinetic energy, fully contained (<~um range in Ge for
  <18.6 keV). Allowed-shape spectrum with the Fermi function (Z_daughter = 2).
* EC: the binding energy of the captured shell in the DAUGHTER atom, released as
  X-rays + Auger electrons. For Ga (Z=31) and Cu (Z=29) at these energies the
  cascade is contained in a 2 mm wafer, so deposit = shell binding energy. These
  are discrete lines.

DELIBERATELY OUT OF SCOPE (flagged, not modelled): the daughter FOLLOW-ON decays
-- 68Ga (beta+, 68 min, endpoint 1.9 MeV + 511 keV annihilation) and the 65Zn
1115.5 keV gamma (~50% branch). Both are >~MeV, land far above the RoI, and
largely ESCAPE the optically-thin 2 mm wafer. They add a small high-energy
continuum that this low-energy deliverable does not resolve.

SUB-SHELL SPLIT -- honest labelling
-----------------------------------
The K-capture fraction P_K is SOURCED (Ga: the frozen 71Ge value 0.8759, IAEA
Live Chart K-vacancy conservation; Cu: standard EC tables). The L/M split of the
remaining (1 - P_K) is NOT determined by the frozen retrieval (Phase 14 bounded
it). Here it is ASSIGNED a standard EC sub-shell ratio (P_L/P_M ~ 7, Bambynek et
al., Rev. Mod. Phys. 49, 77 (1977) class) so the figure shows a spectrum rather
than a bound -- LABELLED order_of_magnitude, with the Phase-14 bound (M <= 1-P_K)
recoverable via ec_line_rates(..., split='bound'). The M line is the only EC line
that reaches the 10-100 eV RoI; the L and K lines sit above it.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

import numpy as np

from . import capture_channel as cc

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))

M_E_keV = 510.998950            # electron rest energy
ALPHA = 7.2973525693e-3

#: Frozen 1-yr surface activities [dec/kg/day] (activation_scenario_v1.1.csv).
ACTIVITY_1YR = {"3H": 4.05, "68Ge": 18.22, "65Zn": 10.98}

#: 3H allowed beta decay endpoint [keV] and daughter Z (3He).
TRITIUM_Q_keV = 18.592
TRITIUM_Z_DAUGHTER = 2

#: EC daughter shell binding energies [eV] = the deposited line energies.
#: Ga (Z=31) is the daughter of BOTH 68Ge and 71Ge -> identical lines; values are
#: the frozen 71Ge line inventory (capture_channel.GE71_EC_LINES).
_GA_LINES_eV = {sh: e for sh, e, _ in cc.GE71_EC_LINES}          # M 158.7, L 1298.5, K 10368.3
#: Cu (Z=29) is the daughter of 65Zn. K from the activation CSV (8.98 keV);
#: L1, M1 from standard X-ray binding-energy tables [order_of_magnitude].
_CU_LINES_eV = {"K": 8979.0, "L": 1096.0, "M": 120.0}

#: K-capture fraction P_K. Ga: frozen 71Ge value (SOURCED). Cu: standard EC value.
_P_K = {"Ga": 0.8759, "Cu": 0.882}
#: Standard EC L/M sub-shell capture ratio P_L/P_M for this Z range (Bambynek 1977
#: class). Used to SPLIT (1 - P_K); the alternative 'bound' puts all of it in each.
_PL_OVER_PM = 7.0

_DAUGHTER = {"68Ge": "Ga", "65Zn": "Cu"}
_LINES = {"68Ge": _GA_LINES_eV, "65Zn": _CU_LINES_eV}


@dataclass
class IntrinsicSpectrum:
    isotope: str
    edges_keV: np.ndarray
    centers_keV: np.ndarray
    dRdE: np.ndarray            # counts / kg / day / keV, deposit axis
    rate_per_kg_day: float      # integral (== the activation rate carried in-band)
    kind: str                   # "continuum" (3H) or "lines" (EC)


# --------------------------------------------------------------------------- #
# 3H allowed beta spectrum                                                     #
# --------------------------------------------------------------------------- #
def _fermi_function(Z: int, E_keV: np.ndarray) -> np.ndarray:
    """Non-relativistic Fermi function F(Z,E) for beta- (attractive, enhances
    low energy). eta = alpha Z / beta, F = 2 pi eta / (1 - exp(-2 pi eta))."""
    E = np.asarray(E_keV, dtype=float)
    Etot = E + M_E_keV
    p = np.sqrt(np.clip(E * (E + 2.0 * M_E_keV), 0.0, None))     # momentum*c [keV]
    beta = np.where(Etot > 0, p / Etot, 1.0)
    eta = ALPHA * Z / np.clip(beta, 1e-12, None)                 # >0 for beta-
    x = 2.0 * np.pi * eta
    return np.where(x > 1e-9, x / (1.0 - np.exp(-x)), 1.0)


def tritium_shape(E_keV: np.ndarray) -> np.ndarray:
    """Unnormalized allowed beta spectrum dN/dE (0 outside (0, Q))."""
    E = np.asarray(E_keV, dtype=float)
    out = np.zeros_like(E)
    ok = (E > 0.0) & (E < TRITIUM_Q_keV)
    Ek = E[ok]
    p = np.sqrt(Ek * (Ek + 2.0 * M_E_keV))                       # momentum*c
    Etot = Ek + M_E_keV
    out[ok] = (_fermi_function(TRITIUM_Z_DAUGHTER, Ek)
               * p * Etot * (TRITIUM_Q_keV - Ek) ** 2)
    return out


def tritium_deposit(edges_keV: np.ndarray,
                    rate_per_kg_day: float = ACTIVITY_1YR["3H"]) -> IntrinsicSpectrum:
    centers = np.sqrt(edges_keV[:-1] * edges_keV[1:])
    shape = tritium_shape(centers)
    widths = np.diff(edges_keV)
    norm = float((shape * widths).sum())
    dRdE = shape / norm * rate_per_kg_day if norm > 0 else np.zeros_like(shape)
    return IntrinsicSpectrum("3H", edges_keV, centers, dRdE, rate_per_kg_day, "continuum")


# --------------------------------------------------------------------------- #
# EC line spectra (68Ge, 65Zn)                                                 #
# --------------------------------------------------------------------------- #
def ec_line_energies_eV(isotope: str) -> dict:
    """Deposited shell-line energies [eV] for an EC intrinsic (K, L, M)."""
    if isotope not in _LINES:
        raise KeyError(f"{isotope!r} not an EC intrinsic ({sorted(_LINES)})")
    return dict(_LINES[isotope])


def ec_line_rates(isotope: str, rate_per_kg_day: float | None = None,
                  split: str = "standard") -> dict:
    """Per-shell line rates [dec/kg/day].

    split='standard': K sourced (P_K), (1-P_K) split L/M by P_L/P_M ~ 7.
    split='bound'   : Phase-14 discipline -- K sourced, M and L each <= (1-P_K).
    """
    if isotope not in _DAUGHTER:
        raise KeyError(f"{isotope!r} not an EC intrinsic ({sorted(_DAUGHTER)})")
    A = ACTIVITY_1YR[isotope] if rate_per_kg_day is None else rate_per_kg_day
    p_k = _P_K[_DAUGHTER[isotope]]
    rest = 1.0 - p_k
    if split == "bound":
        frac = {"K": p_k, "L": rest, "M": rest}          # each <= rest (a bound)
    elif split == "standard":
        p_m = rest / (1.0 + _PL_OVER_PM)
        frac = {"K": p_k, "L": rest - p_m, "M": p_m}
    else:
        raise ValueError(f"split {split!r} not in ('standard','bound')")
    return {sh: A * frac[sh] for sh in ("K", "L", "M")}


def ec_deposit(edges_keV: np.ndarray, isotope: str, split: str = "standard",
               rate_per_kg_day: float | None = None) -> IntrinsicSpectrum:
    """Discrete EC lines binned onto the deposit grid (dR/dE_dep = rate/binwidth)."""
    centers = np.sqrt(edges_keV[:-1] * edges_keV[1:])
    dRdE = np.zeros_like(centers)
    lines = _LINES[isotope]
    rates = ec_line_rates(isotope, rate_per_kg_day, split)
    for sh, E_eV in lines.items():
        E_keV = E_eV / 1e3
        j = int(np.searchsorted(edges_keV, E_keV) - 1)
        if 0 <= j < centers.size:
            dRdE[j] += rates[sh] / (edges_keV[j + 1] - edges_keV[j])
    A = ACTIVITY_1YR[isotope] if rate_per_kg_day is None else rate_per_kg_day
    return IntrinsicSpectrum(isotope, edges_keV, centers, dRdE, A, "lines")


def deposit_spectra(edges_keV: np.ndarray, split: str = "standard") -> dict:
    """All three Ge-intrinsic deposit spectra on the shared grid."""
    return {"3H": tritium_deposit(edges_keV),
            "68Ge": ec_deposit(edges_keV, "68Ge", split),
            "65Zn": ec_deposit(edges_keV, "65Zn", split)}
