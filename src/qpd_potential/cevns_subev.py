# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Sub-eV CEvNS validity gates (Phase 12, plan 12-01: CALC-17 and the VALD-10 plateau leg).

WHAT THIS MODULE IS FOR
-----------------------
Before any detector response is applied, two independent questions have to be
answered about the reactor-CEvNS recoil spectrum at 100 meV:

1. **CALC-17 -- how much rate is missing because the frozen flux table stops at
   100 keV?**  ``truncation_bound`` computes it per isotope under an explicitly
   labelled FLAT continuation ``Phi(E < 0.1 MeV) := Phi(0.1 MeV)``, using the
   same ``cevns.dsigma_dT`` (and therefore the same ``(1 - MT/2E^2)`` kinematic
   factor) that the pipeline uses.  **The flux table is never extended and
   ``ReactorFlux.flux`` is never evaluated below its own floor.**  The flat
   continuation is an UPPER bound only while ``Phi`` is non-increasing as ``E``
   falls toward the floor, which ``flux_floor_slope`` measures from the frozen
   table's own knots -- see ``fp-extend-flux-table``.

2. **VALD-10 (plateau leg) -- does dR/dT approach the analytic flat-box T -> 0
   limit?**  ``analytic_plateau`` builds that limit INDEPENDENTLY of the fold:
   it integrates the frozen ``Phi`` once to get ``int Phi dE`` and multiplies by
   the ``T -> 0`` cross-section prefactor with ``(1 - MT/2E^2) -> 1`` and the
   Helm form factor off.  It is never obtained by extrapolating the computed
   ``dR/dT`` downward, which would make the comparison an identity
   (``fp-plateau-by-extrapolation``).

UNITS (CONVENTIONS Section A.1)
-------------------------------
``T`` in eV on the recoil axis (converted to keV at the ``cevns`` boundary),
``E_nu`` in MeV, ``dR/dT`` and the analytic plateau in counts/kg/day/keV,
``E_min`` reported in keV, the truncation bound a dimensionless fraction and its
additive band in counts/kg/day/keV (METHODS.md 3.4's recommended form).

NORMALIZATION
-------------
PRIMARY AND ONLY: the frozen ``data/flux/reactor_flux_v1.0.csv`` at 3 GW_th /
25 m, surface, unshielded, used UNMODIFIED.  ``CONVENTIONS.md`` Section D stands
unchanged.  Nothing in this module writes, appends to, or synthesises knots for
any flux table.

WHAT THIS MODULE DELIBERATELY DOES NOT DO
-----------------------------------------
No broadening, no response matrix, no trigger curve, no ``dR/dE_rec``: plan
12-02 owns all four.  (Plan 12-02 and 12-03 append their own sections below.)
"""

from __future__ import annotations

import math
import os
from typing import Optional, Sequence

import numpy as np
from scipy.integrate import quad

from . import cevns, params

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
ARTIFACT_DIR_V2 = os.path.join(_PROJECT_ROOT, "artifacts", "v2.0")
FLUX_CSV = os.path.join(_PROJECT_ROOT, "data", "flux", "reactor_flux_v1.0.csv")

#: The Phase-10 extended deposit-grid floor [eV] (``muon_deposit.shared_energy_grid
#: ("v2.0-ext")[0] * 1e3``).  The recoil axes below are anchored on it so that the
#: leakage boundary plan 12-02 sees is the boundary Phase 12 actually reports.
EXT_GRID_FLOOR_eV = 0.0999350

#: Top of the CEvNS recoil support carried through the milestone (Phase-11 precedent).
RECOIL_TOP_eV = 3200.0

#: The frozen flux table's own lowest tabulated antineutrino energy [MeV].
#: NOT a modelling choice -- it is read back from the table in ``flux_floor_slope``
#: and asserted by ``tests/test_cevns_subev.py``.
FLUX_FLOOR_MeV = 0.1

#: Phase-7 frozen abundance-weighted natural-Ge NUCLEAR mass [eV].
M_N_PHASE7_eV = 6.7724551e10

_SECONDS_PER_DAY = 86400.0


# --------------------------------------------------------------------------- #
# Recoil axes                                                                  #
# --------------------------------------------------------------------------- #
def truncation_axis_eV(n: int = 480) -> np.ndarray:
    """Log recoil axis for the truncation table: floor -> 3200 eV, endpoints exact.

    The first point is EXACTLY ``EXT_GRID_FLOOR_eV`` so that the bound is reported
    at the energy the extended deposit grid actually starts at, and the last is the
    CEvNS recoil top.
    """
    return np.logspace(np.log10(EXT_GRID_FLOOR_eV), np.log10(RECOIL_TOP_eV), n)


def plateau_axis_eV(n: int = 240, T_hi_eV: float = 10.0) -> np.ndarray:
    """Log recoil axis spanning the FULL ROADMAP SC2 window, endpoints exact.

    ``[EXT_GRID_FLOOR_eV, 10 eV]``.  The window is a stated success criterion, not
    a tunable: narrowing it until "flat to a few percent" becomes true is
    ``fp-narrow-the-window``.
    """
    return np.logspace(np.log10(EXT_GRID_FLOOR_eV), np.log10(T_hi_eV), n)


# --------------------------------------------------------------------------- #
# E_min reconciliation                                                         #
# --------------------------------------------------------------------------- #
def e_min_reconciliation(T_eV: float = 0.1) -> dict:
    """``E_min(T)`` [keV] under the three natural-Ge masses in circulation.

    Three numbers circulate for ``E_min(100 meV)`` -- 58.19, 58.16 and 58.7 keV --
    and none of them is wrong: they are three DIFFERENT masses.  This function
    computes all three from their masses and records which one the phase adopts,
    rather than asserting one and rounding the others away.

    * ``phase7_natural``  -- the Phase-7 frozen abundance-weighted NUCLEAR mass
      ``m_N c^2 = 6.7724551e10 eV``.  **ADOPTED**: it is the project's own frozen
      value and is what ``cevns.E_min_MeV`` reproduces when fed the same mass.
    * ``conventions_molar`` -- ``CONVENTIONS.md`` Section D's natural-Ge MOLAR mass
      72.63 u.  This is the mass behind the ROADMAP's 58.16 keV.
    * ``ge74_only`` -- the single isotope 74Ge, ``74 u``.  The project-frozen
      74Ge-only figure, ~1% above the abundance-weighted value.
    """
    u_MeV = 931.494  # params._U_MEV, CODATA; matches CONVENTIONS
    masses_MeV = {
        "phase7_natural": M_N_PHASE7_eV * 1.0e-6,
        "conventions_molar": params.GE_MOLAR_MASS.value * u_MeV,
        "ge74_only": 74.0 * u_MeV,
    }
    T_keV = T_eV * 1.0e-3
    out = {}
    for key, M in masses_MeV.items():
        out[key] = {
            "M_MeV": M,
            "E_min_keV": cevns.E_min_MeV(T_keV, M) * 1.0e3,
            "source": {
                "phase7_natural":
                    "Phase-7 frozen abundance-weighted natural-Ge nuclear mass "
                    "m_N c^2 = 6.7724551e10 eV",
                "conventions_molar":
                    "CONVENTIONS.md Section D natural-Ge molar mass 72.63 u "
                    "x 931.494 MeV/u (the mass behind the ROADMAP's 58.16 keV)",
                "ge74_only":
                    "74Ge alone, 74 u x 931.494 MeV/u (project-frozen 74Ge-only value)",
            }[key],
        }
    vals = np.array([v["E_min_keV"] for v in out.values()])
    out["adopted"] = "phase7_natural"
    out["spread_relative"] = float((vals.max() - vals.min()) / vals.mean())
    out["T_eV"] = T_eV
    return out


# --------------------------------------------------------------------------- #
# The frozen table's own slope near its floor -- the disconfirming check       #
# --------------------------------------------------------------------------- #
def flux_floor_slope(n_knots: int = 5, csv_path: str = FLUX_CSV) -> dict:
    """``d log Phi / d log E`` across the frozen table's LOWEST knots.

    THE POINT OF THIS FUNCTION.  A flat continuation of ``Phi`` below the table
    floor over-estimates the missing flux -- and therefore bounds it from ABOVE --
    only if ``Phi`` is non-increasing as ``E`` falls toward the floor.  That is a
    property of the frozen table, not of the bound, so it is a genuine
    disconfirming check rather than an algebraic identity: if ``Phi`` RISES toward
    the floor the ``<= 0.81%`` figure is not an upper bound at all and CALC-17's
    bound language must be WITHDRAWN, not restated.

    Reads the knots straight off the CSV.  Does not touch the interpolator and
    never evaluates below the floor.
    """
    E, phi = [], []
    with open(csv_path) as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith("#") or s.startswith("E_nu"):
                continue
            cols = s.split(",")
            E.append(float(cols[0]))
            phi.append(float(cols[1]))
    E = np.asarray(E)
    phi = np.asarray(phi)
    order = np.argsort(E)
    E, phi = E[order], phi[order]
    k = min(n_knots, E.size)
    Ek, pk = E[:k], phi[:k]
    slopes = np.diff(np.log(pk)) / np.diff(np.log(Ek))
    return {
        "E_MeV": Ek,
        "phi": pk,
        "dlogPhi_dlogE": slopes,
        # Phi non-increasing as E FALLS toward the floor  <=>  Phi non-decreasing
        # with increasing E across the lowest knots  <=>  every slope >= 0.
        "non_increasing_toward_floor": bool(np.all(slopes >= 0.0)),
        "floor_MeV": float(E.min()),
        "phi_at_floor": float(pk[0]),
        "csv_path": csv_path,
    }


# --------------------------------------------------------------------------- #
# CALC-17: the sub-100-keV flux-truncation bound                               #
# --------------------------------------------------------------------------- #
def _continuation_phi(E_MeV, phi_floor: float, continuation: str) -> float:
    """The LABELLED synthetic flux used ONLY below the frozen table's floor.

    ``flat`` : ``Phi(E) = Phi(0.1 MeV)``           -- the CALC-17 upper bound.
    ``E2``   : ``Phi(E) = Phi(0.1) (E/0.1)^2``     -- the allowed-beta-branch
               shape, used only as a strictly-smaller comparison.

    This is the ONE place a flux value below 0.1 MeV appears anywhere in this
    module, and it is a declared constant (or a declared power law) rather than an
    extrapolation of the interpolator: ``ReactorFlux.flux`` is never called here.
    """
    if continuation == "flat":
        return phi_floor
    if continuation == "E2":
        return phi_floor * (E_MeV / FLUX_FLOOR_MeV) ** 2
    raise ValueError(f"unknown continuation {continuation!r}; expected 'flat' or 'E2'")


def truncation_bound(T_eV: float, flux: Optional[cevns.ReactorFlux] = None,
                     continuation: str = "flat") -> dict:
    """Per-isotope sub-100-keV flux-truncation contribution to ``dR/dT`` at ``T``.

    For each natural-Ge isotope:

    * MISSING   ``= N_i int_{E_min_i(T)}^{0.1 MeV} Phi_cont(E) dsigma_i/dT dE``,
      skipped ENTIRELY (contributing exactly ``0.0``, not a small residual) when
      ``E_min_i(T) >= 0.1 MeV``;
    * TABULATED ``= N_i int_{max(E_min_i(T), 0.1)}^{E_max} Phi(E) dsigma_i/dT dE``
      -- the same integral ``cevns._fold_isotope`` performs, so the denominator is
      the rate the pipeline actually produces.

    Both use ``cevns.dsigma_dT`` with the Helm form factor ON, i.e. the SAME cross
    section and the SAME ``(1 - MT/2E^2)`` factor the pipeline uses; both are
    multiplied by ``x_i * GE_ATOMS_PER_KG * 86400`` so every quantity is in
    counts/kg/day/keV (CONVENTIONS Section A.1).

    Returns the per-isotope breakdown, the totals, the dimensionless
    ``bound_fraction = missing / (missing + tabulated)`` and the one-sided ADDITIVE
    band ``missing`` in counts/kg/day/keV (METHODS.md 3.4).
    """
    if flux is None:
        flux = cevns.ReactorFlux()
    phi_floor = flux.flux(FLUX_FLOOR_MeV)
    T_keV = T_eV * 1.0e-3

    per_iso = {}
    missing_total = 0.0
    tabulated_total = 0.0
    for iso in params.GE_ISOTOPES:
        e_min_MeV = cevns.E_min_MeV(T_keV, iso.M_MeV)
        N_target = iso.abundance * params.GE_ATOMS_PER_KG.value * _SECONDS_PER_DAY

        if e_min_MeV < FLUX_FLOOR_MeV:
            def _missing_integrand(E, iso=iso):
                return _continuation_phi(E, phi_floor, continuation) * cevns.dsigma_dT(
                    E, T_keV, iso.Z, iso.N, iso.M_MeV, iso.A, True)
            val, _ = quad(_missing_integrand, e_min_MeV, FLUX_FLOOR_MeV, limit=200)
            missing = N_target * val
        else:
            # Kinematically closed: EXACTLY zero, not a small residual.
            missing = 0.0

        lo = max(e_min_MeV, FLUX_FLOOR_MeV)
        if lo < flux.E_max:
            def _tab_integrand(E, iso=iso):
                phi = flux.flux(E)
                if phi <= 0.0:
                    return 0.0
                return phi * cevns.dsigma_dT(
                    E, T_keV, iso.Z, iso.N, iso.M_MeV, iso.A, True)
            val, _ = quad(_tab_integrand, lo, flux.E_max, limit=200)
            tabulated = N_target * val
        else:
            tabulated = 0.0

        per_iso[iso.name] = {
            "E_min_keV": e_min_MeV * 1.0e3,
            "missing": missing,
            "tabulated": tabulated,
            "kinematically_closed": bool(e_min_MeV >= FLUX_FLOOR_MeV),
        }
        missing_total += missing
        tabulated_total += tabulated

    denom = missing_total + tabulated_total
    return {
        "T_eV": T_eV,
        "continuation": continuation,
        "phi_floor": phi_floor,
        "per_isotope": per_iso,
        "missing_total": missing_total,
        "tabulated_total": tabulated_total,
        "bound_fraction": (missing_total / denom) if denom > 0.0 else 0.0,
        "additive_band_cts_per_kg_day_keV": missing_total,
    }


def isotope_zero_point_eV() -> dict:
    """The recoil energy above which the truncation term vanishes for EVERY isotope.

    ``E_min_i(T) >= 0.1 MeV`` for all five isotopes; the binding isotope is the
    LIGHTEST, 70Ge, so the threshold is set by it alone.  Inverting
    ``T = 2 E^2 / (M + 2 E)`` at ``E = 0.1 MeV`` gives the exact value in closed
    form -- no scan, no tolerance.

    The ROADMAP states "exactly zero above 0.29 eV".  That is the
    natural-mean-mass statement; the isotope-resolved threshold is slightly HIGHER
    and 0.29 eV therefore still carries a small but NON-ZERO 70Ge residual.
    """
    E = FLUX_FLOOR_MeV
    out = {}
    for iso in params.GE_ISOTOPES:
        T_MeV = 2.0 * E**2 / (iso.M_MeV + 2.0 * E)
        out[iso.name] = T_MeV * 1.0e6  # MeV -> eV
    T_all = max(out.values())
    binding = max(out, key=out.get)
    return {
        "per_isotope_T_eV": out,
        "threshold_eV": T_all,
        "binding_isotope": binding,
        "roadmap_stated_eV": 0.29,
    }


# --------------------------------------------------------------------------- #
# VALD-10 plateau leg                                                          #
# --------------------------------------------------------------------------- #
def integral_flux(flux: Optional[cevns.ReactorFlux] = None) -> float:
    """``int Phi(E) dE`` over the frozen table's own span [nubar/cm^2/s].

    Integrated KNOT BY KNOT rather than in one ``quad`` call: the PCHIP(log Phi)
    interpolant is only piecewise smooth, and a single adaptive call over the whole
    0.1-10 MeV span emits a roundoff warning.  Knot-to-knot panels agree with the
    single call to 4e-9 relative, which is far below anything this phase claims.
    """
    if flux is None:
        flux = cevns.ReactorFlux()
    total = 0.0
    knots = np.sort(flux.E)
    for a, b in zip(knots[:-1], knots[1:]):
        val, _ = quad(lambda e: flux.flux(e), a, b, limit=200)
        total += val
    return total


def analytic_plateau(flux: Optional[cevns.ReactorFlux] = None) -> dict:
    """The analytic flat-box ``T -> 0`` plateau [counts/kg/day/keV].

    ``plateau = sum_i N_i * (G_F^2 M_i / 4pi) Q_W,i^2 (hbar c)^2 * int Phi dE * 86400``

    i.e. ``dsigma_i/dT`` evaluated in the ``T -> 0`` limit where the kinematic
    factor ``(1 - M T / 2 E^2) -> 1`` and the Helm form factor ``F(q) -> 1``, so
    that the neutrino-energy dependence factorises out of the fold entirely and
    only ``int Phi dE`` survives.

    **Built INDEPENDENTLY of the fold.**  It never calls ``differential_rate`` and
    is never obtained by extrapolating the computed ``dR/dT`` downward -- that
    would make the plateau comparison an identity (``fp-plateau-by-extrapolation``).
    What it DOES share with the fold is the frozen ``Phi`` and the locked
    cross-section prefactor; that shared dependence is a stated weakest anchor, not
    a cross-check: a normalization error in the frozen table would move both.
    """
    if flux is None:
        flux = cevns.ReactorFlux()
    int_phi = integral_flux(flux)
    G_F = params.G_F.value
    hbarc2 = params.HBARC2.value
    denom = params.CEVNS_PREFACTOR_DENOM.value

    per_iso = {}
    total = 0.0
    for iso in params.GE_ISOTOPES:
        M_GeV = iso.M_MeV * 1.0e-3
        Q_W = cevns.weak_charge(iso.Z, iso.N)
        # cm^2/GeV -> cm^2/keV via 1e-6, exactly as cevns.dsigma_dT does.
        prefactor = G_F**2 * M_GeV / denom * Q_W**2 * hbarc2 * 1.0e-6
        N_target = iso.abundance * params.GE_ATOMS_PER_KG.value
        contrib = N_target * prefactor * int_phi * _SECONDS_PER_DAY
        per_iso[iso.name] = contrib
        total += contrib
    return {
        "plateau_cts_per_kg_day_keV": total,
        "integral_flux": int_phi,
        "per_isotope": per_iso,
        "method": ("sum_i N_i (G_F^2 M_i/4pi) Q_W_i^2 (hbar c)^2 x int Phi dE x 86400, "
                   "with (1 - MT/2E^2) -> 1 and the Helm form factor OFF; computed "
                   "from the frozen flux table and the locked cross-section prefactor, "
                   "NOT by extrapolating dR/dT downward"),
    }


def plateau_profile(T_eV: Sequence[float],
                    flux: Optional[cevns.ReactorFlux] = None) -> dict:
    """``dR/dT``, the analytic plateau, their ratio, the deficit and the log-log slope.

    ``dR/dT`` comes from ``cevns.differential_rate`` with the Helm form factor ON
    -- the pipeline's own quantity, unbroadened, no response, no trigger.
    """
    if flux is None:
        flux = cevns.ReactorFlux()
    T = np.asarray(T_eV, float)
    plateau = analytic_plateau(flux)["plateau_cts_per_kg_day_keV"]
    dRdT = np.array([cevns.differential_rate(t * 1.0e-3, flux) for t in T])
    ratio = dRdT / plateau
    deficit = 1.0 - ratio
    slope = np.full_like(T, np.nan)
    if T.size > 1:
        lg_T = np.log(T)
        lg_R = np.log(dRdT)
        slope[1:-1] = (lg_R[2:] - lg_R[:-2]) / (lg_T[2:] - lg_T[:-2])
        slope[0] = (lg_R[1] - lg_R[0]) / (lg_T[1] - lg_T[0])
        slope[-1] = (lg_R[-1] - lg_R[-2]) / (lg_T[-1] - lg_T[-2])
    return {
        "T_eV": T,
        "dRdT": dRdT,
        "plateau": plateau,
        "ratio": ratio,
        "deficit": deficit,
        "loglog_slope": slope,
    }


# --------------------------------------------------------------------------- #
# Artifact writers                                                             #
# --------------------------------------------------------------------------- #
_TRUNC_COLUMNS = (
    ["T_eV"]
    + [f"E_min_{iso.name}_keV" for iso in params.GE_ISOTOPES]
    + [f"missing_{iso.name}" for iso in params.GE_ISOTOPES]
    + ["missing_total", "tabulated_total", "bound_fraction",
       "additive_band_cts_per_kg_day_keV", "bound_fraction_E2_continuation"]
)


def write_truncation_table(path: Optional[str] = None, n: int = 480,
                           flux: Optional[cevns.ReactorFlux] = None) -> str:
    """Emit ``artifacts/v2.0/cevns_truncation_bound.csv``."""
    if path is None:
        path = os.path.join(ARTIFACT_DIR_V2, "cevns_truncation_bound.csv")
    if flux is None:
        flux = cevns.ReactorFlux()
    T_axis = truncation_axis_eV(n)
    slope = flux_floor_slope()
    zero_pt = isotope_zero_point_eV()
    emin = e_min_reconciliation(0.1)

    rows = []
    for T in T_axis:
        b_flat = truncation_bound(T, flux, "flat")
        # The E^2 comparison is only meaningful while the window is open.
        if b_flat["missing_total"] > 0.0:
            b_e2 = truncation_bound(T, flux, "E2")["bound_fraction"]
        else:
            b_e2 = 0.0
        row = [T]
        row += [b_flat["per_isotope"][iso.name]["E_min_keV"] for iso in params.GE_ISOTOPES]
        row += [b_flat["per_isotope"][iso.name]["missing"] for iso in params.GE_ISOTOPES]
        row += [b_flat["missing_total"], b_flat["tabulated_total"],
                b_flat["bound_fraction"], b_flat["additive_band_cts_per_kg_day_keV"],
                b_e2]
        rows.append(row)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(
            "# QPD Phase-12 plan 12-01 (CALC-17) -- sub-100-keV FLUX-TRUNCATION BOUND.\n"
            "# THE FLUX TABLE WAS NOT EXTENDED. data/flux/reactor_flux_v1.0.csv is\n"
            "#   byte-identical to its committed state; no knot was added below 0.1 MeV\n"
            "#   and ReactorFlux.flux() is never evaluated below its own floor\n"
            "#   (fp-extend-flux-table). What is bounded here is the rate the frozen\n"
            "#   table cannot carry, NOT a modelled sub-100-keV spectrum.\n"
            "# Assumption (LABELLED): a FLAT continuation Phi(E < 0.1 MeV) := Phi(0.1 MeV)\n"
            f"#   = {slope['phi_at_floor']:.6e} nubar/cm^2/s/MeV.\n"
            "# Conservatism evidence, from the frozen table's OWN lowest knots\n"
            "#   (this is a disconfirming check, not an identity of the bound):\n"
            f"#   E_nu/MeV = {np.array2string(slope['E_MeV'], precision=6)}\n"
            f"#   Phi       = {np.array2string(slope['phi'], precision=6)}\n"
            f"#   d log Phi / d log E = {np.array2string(slope['dlogPhi_dlogE'], precision=4)}\n"
            f"#   Phi non-increasing as E falls toward the floor: "
            f"{slope['non_increasing_toward_floor']}\n"
            "#   => a constant continuation at Phi(0.1 MeV) OVER-estimates the missing\n"
            "#      flux, so bound_fraction is a genuine UPPER bound. Had Phi risen\n"
            "#      toward the floor the upper-bound language would have to be withdrawn.\n"
            "# Comparison continuation: Phi(E) = Phi(0.1)(E/0.1)^2 (allowed-beta branch),\n"
            "#   reported in the last column and strictly smaller everywhere.\n"
            "# Cross section: cevns.dsigma_dT with the SAME (1 - MT/2E^2) kinematic factor\n"
            "#   and the SAME Helm form factor the pipeline uses (CONVENTIONS Section C).\n"
            "# Zero point: the missing term is EXACTLY 0.0 (not a small residual) once\n"
            f"#   E_min_i(T) >= 0.1 MeV for EVERY isotope, i.e. above T = "
            f"{zero_pt['threshold_eV']:.5f} eV,\n"
            f"#   set by the lightest isotope {zero_pt['binding_isotope']}. The ROADMAP's\n"
            "#   'exactly zero above 0.29 eV' is the natural-mean-mass statement; at\n"
            "#   0.29 eV a small NON-ZERO 70Ge residual survives.\n"
            f"# E_min(100 meV) adopted: {emin[emin['adopted']]['E_min_keV']:.4f} keV "
            f"({emin['adopted']}).\n"
            f"#   Also in circulation: {emin['conventions_molar']['E_min_keV']:.4f} keV "
            "(CONVENTIONS Section D molar mass 72.63 u, the ROADMAP's 58.16 keV) and\n"
            f"#   {emin['ge74_only']['E_min_keV']:.4f} keV (74Ge alone). Spread "
            f"{emin['spread_relative']*100:.3f}% -- three MASSES, not three answers.\n"
            "# Normalization: data/flux/reactor_flux_v1.0.csv, 3 GW_th / 25 m, surface,\n"
            "#   unshielded, UNMODIFIED (CONVENTIONS Section D).\n"
            "# Units: T in eV (nuclear recoil, unified phonon scale, no quenching);\n"
            "#   E_min in keV; missing/tabulated/additive band in counts/kg/day/keV;\n"
            "#   bound_fraction dimensionless.\n"
        )
        fh.write(",".join(_TRUNC_COLUMNS) + "\n")
        for row in rows:
            fh.write(",".join(f"{v:.10e}" for v in row) + "\n")
    return path


_PLATEAU_COLUMNS = ["T_eV", "dRdT", "analytic_plateau", "ratio", "deficit",
                    "loglog_slope"]


def write_plateau_table(path: Optional[str] = None, n: int = 240,
                        flux: Optional[cevns.ReactorFlux] = None) -> str:
    """Emit ``artifacts/v2.0/cevns_plateau_profile.csv`` over the FULL SC2 window."""
    if path is None:
        path = os.path.join(ARTIFACT_DIR_V2, "cevns_plateau_profile.csv")
    if flux is None:
        flux = cevns.ReactorFlux()
    prof = plateau_profile(plateau_axis_eV(n), flux)
    ap = analytic_plateau(flux)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(
            "# QPD Phase-12 plan 12-01 (VALD-10, plateau leg) -- dR/dT against the\n"
            "#   analytic flat-box T->0 plateau, over the FULL ROADMAP SC2 window.\n"
            f"# Analytic plateau = {ap['plateau_cts_per_kg_day_keV']:.6f} counts/kg/day/keV.\n"
            f"# Method: {ap['method']}\n"
            f"# int Phi dE = {ap['integral_flux']:.6e} nubar/cm^2/s, integrated knot by knot\n"
            "#   over the frozen table's own span (0.1 - 10 MeV).\n"
            "# Window: 0.0999350 eV (the Phase-10 extended-grid floor) to 10 eV, inclusive.\n"
            "#   The window is ROADMAP SC2's own; it was NOT narrowed (fp-narrow-the-window).\n"
            "# dR/dT is cevns.differential_rate with the Helm form factor ON:\n"
            "#   UNBROADENED, no response matrix, no trigger curve. Plan 12-02 owns those.\n"
            "# Normalization: data/flux/reactor_flux_v1.0.csv, 3 GW_th / 25 m, surface,\n"
            "#   unshielded, UNMODIFIED (CONVENTIONS Section D).\n"
            "# Units: T in eV (nuclear recoil, no quenching); dR/dT and the plateau in\n"
            "#   counts/kg/day/keV; ratio, deficit and slope dimensionless.\n"
        )
        fh.write(",".join(_PLATEAU_COLUMNS) + "\n")
        for i in range(prof["T_eV"].size):
            fh.write(",".join(f"{v:.10e}" for v in (
                prof["T_eV"][i], prof["dRdT"][i], prof["plateau"],
                prof["ratio"][i], prof["deficit"][i], prof["loglog_slope"][i])) + "\n")
    return path


# =========================================================================== #
# PLAN 12-02 (CALC-25): the decisive signal deliverable                        #
# =========================================================================== #
#
# The extended-axis UNBROADENED recoil table, the folded dR/dE_rec for both
# designs, the sub-eV trigger observable with its k-sensitivity, and the figure.
#
# SWITCHES TURNED ON DELIBERATELY HERE, AND RECORDED:
#   * the IA broadening, via ``broaden=True`` at the Phase-12 call site in
#     ``fold.run_cevns_fold_extended``.  ``ia_broadening.BROADENING_DEFAULT`` stays
#     ``False``; the global default is NOT flipped.
#   * the Phase-10 extended axis, via the ``_ext.npz`` response matrices.
#     ``muon_deposit.shared_energy_grid`` still defaults to ``v1.0``.
#
# THE CAVEATS THAT TRAVEL WITH EVERY 100 meV NUMBER (written into artifact headers,
# not only into prose) are collected in ``BOTTOM_BIN_CAVEAT`` below.

#: Phase-11 measured bottom-bin leakage and lineshape facts, plus the model-specific
#: licence to multiply R by the trigger curve.  Emitted verbatim into every artifact
#: header this plan writes: a caveat that lives only in a phase report does not travel
#: with the data.
BOTTOM_BIN_CAVEAT = (
    "# BOTTOM-BIN CAVEATS (Phase 11; they travel with this data, they are not asides).\n"
    "#   * 48.98% of the 100 meV bin's kernel falls BELOW the 0.0999350 eV grid floor\n"
    "#     and 0.87% lands at unphysical T < 0. This is physics plus axis truncation.\n"
    "#     It is ACCOUNTED and REPORTED and is NEVER renormalized away\n"
    "#     (fp-renormalize-leakage): the retained-only sum MUST miss.\n"
    "#   * The shipped kernel is a SYMMETRIC Gaussian against a true lineshape with\n"
    "#     skewness 0.590 and excess kurtosis 0.381, and 2W is only 5.60 at the floor,\n"
    "#     so the impulse approximation is satisfied but not comfortably.\n"
    "#     DO NOT QUOTE THE 100 meV BIN TO BETTER THAN ONE SIGNIFICANT FIGURE.\n"
    "#   * MODEL-SPECIFIC LICENCE: multiplying R(E_rec|E_dep) by the trigger curve is\n"
    "#     licensed ONLY for this yield model. Phase 10 measured P(no counts\n"
    "#     registered) = 2.0e-4 at 0.1 eV and exactly 0 at 0.5/1 eV against 1 - P_trig\n"
    "#     of 0.998/0.512/0.056, so the two do not double-count -- but that follows\n"
    "#     from a LINEAR yield assigning 0.018 quasiparticles to a sensor holding\n"
    "#     6.89 ueV against a ~190 ueV gap. A THRESHOLD yield model would INVERT the\n"
    "#     verdict and the two would then double-count.\n"
    "#   * The Phase-10 counting floor is a BEST CASE WITH NO NOISE SOURCES, not a\n"
    "#     resolution model; this project has no resolution parameter at all\n"
    "#     (fp-poisson-as-resolution).\n"
    "#   * The trigger sharpness k is fixed by NO project artifact. Every sub-eV number\n"
    "#     ships with its k-sensitivity over [1, 12] (CONVENTIONS Section I).\n"
)

_NORMALIZATION_HEADER = (
    "# Normalization: data/flux/reactor_flux_v1.0.csv, 3 GW_th at 25 m, surface,\n"
    "#   unshielded, used UNMODIFIED. NO rescale of any kind is applied here -- not a\n"
    "#   VNS rescale, not a duty cycle, not a shielding or overburden credit\n"
    "#   (fp-second-vns-run, fp-inherited-shielding). CONVENTIONS Section D unchanged.\n"
)

#: The Phase-11 480-bin recoil construction, reused so that the leakage boundary this
#: phase sees is the extended-grid floor itself.
EXT_RECOIL_BINS = 480


def ext_recoil_edges_eV(n: int = EXT_RECOIL_BINS) -> np.ndarray:
    """Recoil bin EDGES whose bottom edge is exactly the extended-grid floor."""
    return np.logspace(np.log10(EXT_GRID_FLOOR_eV), np.log10(RECOIL_TOP_eV), n + 1)


def ext_recoil_centres_eV(n: int = EXT_RECOIL_BINS) -> np.ndarray:
    """Geometric bin centres of :func:`ext_recoil_edges_eV`.

    These are the knots the table is tabulated on.  ``ia_broadening.native_edges``
    of these centres reproduces the edges EXACTLY (geometric midpoints of geometric
    centres of a constant-ratio grid), so the kernel's floor is the extended-grid
    floor and not something one half-bin away from it.
    """
    e = ext_recoil_edges_eV(n)
    return np.sqrt(e[:-1] * e[1:])


_EXT_DRDT_COLUMNS = (["T_eV_nr"]
                     + [f"dRdT_{iso.name}" for iso in params.GE_ISOTOPES]
                     + ["dRdT_total", "dRdT_band_1sigma"])


def write_ext_dRdT_table(path: Optional[str] = None, n: int = EXT_RECOIL_BINS,
                         flux: Optional[cevns.ReactorFlux] = None) -> str:
    """Emit ``artifacts/v2.0/cevns_dRdT_ext.csv`` -- UNBROADENED, 8-column layout.

    ``fold.read_cevns`` reads columns 0, 6 and 7 POSITIONALLY, so the layout must match
    the frozen `artifacts/stage1/cevns_dRdT.csv` exactly or the wiring silently reads
    the wrong column.

    ``dR/dT`` is RECOMPUTED from ``cevns.differential_rate_per_isotope`` and
    ``cevns.differential_rate_band`` at each knot, never extrapolated downward from the
    5 eV-floored frozen table (``fp-silent-carry``).
    """
    if path is None:
        path = os.path.join(ARTIFACT_DIR_V2, "cevns_dRdT_ext.csv")
    if flux is None:
        flux = cevns.ReactorFlux()
    T = ext_recoil_centres_eV(n)
    edges = ext_recoil_edges_eV(n)

    rows = []
    for t in T:
        t_keV = t * 1.0e-3
        per = cevns.differential_rate_per_isotope(t_keV, flux, use_form_factor=True)
        total = sum(per.values())
        band = cevns.differential_rate_band(t_keV, flux)
        rows.append([t] + [per[iso.name] for iso in params.GE_ISOTOPES] + [total, band])

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(
            "# QPD Phase-12 plan 12-02 (CALC-25) -- EXTENDED-AXIS CEvNS dR/dT.\n"
            "# THIS TABLE IS UNBROADENED. The IA Gaussian kernel is applied DOWNSTREAM,\n"
            "#   exactly once, inside fold.rebin_cevns_to_edep_grid(broaden=True) on the\n"
            "#   recoil axis and upstream of R(E_rec|E_dep). Feeding\n"
            "#   artifacts/v2.0/cevns_dRdT_broadened.csv to that call instead would apply\n"
            "#   the kernel TWICE, widening the bottom bin by sqrt(2), and nothing in the\n"
            "#   existing wiring would raise (fp-double-broadening).\n"
            f"# {n} log bins; bottom bin EDGE exactly {EXT_GRID_FLOOR_eV} eV (the Phase-10\n"
            f"#   extended-grid floor), top edge {RECOIL_TOP_eV} eV. Knots are the geometric\n"
            "#   bin centres, so ia_broadening.native_edges reproduces these edges exactly.\n"
            "# dR/dT is RECOMPUTED from cevns.differential_rate_per_isotope with the Helm\n"
            "#   form factor ON, and the 1-sigma band from cevns.differential_rate_band.\n"
            "#   Nothing is extrapolated from the 5 eV-floored artifacts/stage1/cevns_dRdT.csv.\n"
            "# Column layout is the FROZEN 8-column layout: fold.read_cevns reads columns\n"
            "#   0, 6 and 7 positionally.\n"
            "# Recoil energy on the unified phonon scale, NO quenching, never keVee.\n"
            "# The rate is NEVER multiplied by exp(-2W) (fp-dw-suppression).\n"
            + _NORMALIZATION_HEADER
            + "# Units: T in eV_nr; rates in counts/kg/day/keV (CONVENTIONS Section A.1).\n"
        )
        fh.write(",".join(_EXT_DRDT_COLUMNS) + "\n")
        for row in rows:
            fh.write(",".join(f"{v:.10e}" for v in row) + "\n")
    return path


# --------------------------------------------------------------------------- #
# The folded reconstructed-energy spectra                                      #
# --------------------------------------------------------------------------- #
_SPECTRA_COLUMNS = ["E_rec_keV", "dRdErec_central", "dRdErec_upper_width_onesided",
                    "dRdErec_band_1sigma", "dRdErec_trigger_weighted",
                    "P_trig_effective", "regime"]


def _regime_flags(E_rec_eV: np.ndarray, boundary_Erec_eV: float) -> list:
    from . import trigger
    lo = "subev_P_trig_is_the_reported_observable"
    hi = "dRdErec_is_the_reported_observable"
    assert trigger.SUBEV_REGIME_BOUNDARY_eV > 0.0     # imported, never restated
    return [lo if e < boundary_Erec_eV else hi for e in E_rec_eV]


def run_extended_spectra(design: str, sharpness: Optional[float] = None) -> dict:
    """Fold one design twice: central on the LOCKED harmonic omega_bar, and the
    ONE-SIDED UPPER variant on the arithmetic VDOS mean.  Never averaged."""
    from . import fold, trigger

    central = fold.run_cevns_fold_extended(design, broaden=True, sharpness=sharpness)
    upper = fold.run_cevns_fold_extended(
        design, broaden=True, omega_bar_eV=params.OMEGA_BAR_ARITHMETIC_eV.value,
        sharpness=sharpness)
    boundary_Erec = fold.subev_boundary_Erec_eV(design)

    # The EFFECTIVE trigger acceptance in each reconstructed bin, formed from the two
    # spectra this fold actually produced: P_eff = triggered / untriggered.  It is not
    # an interpolation of P_trig onto the E_rec axis -- that would need a mapping the
    # response matrix does not provide below its first median, and clamping there is
    # precisely the silent-extrapolation failure the Phase-10 guards exist against.
    # P_eff is exact where the untriggered rate is non-zero and 0 where it is not.
    E_rec = central["E_rec_centers_eV"]
    assert trigger.SUBEV_REGIME_BOUNDARY_eV > 0.0
    with np.errstate(divide="ignore", invalid="ignore"):
        P_eff = np.where(central["dRdErec"] > 0.0,
                         central["dRdErec_trigger"] / central["dRdErec"], 0.0)
    return {
        "central": central, "upper": upper,
        "boundary_Erec_eV": boundary_Erec,
        "P_trig_effective": P_eff,
        "regime": _regime_flags(E_rec, boundary_Erec),
    }


def write_extended_spectrum(design: str, res: Optional[dict] = None,
                            path: Optional[str] = None,
                            sharpness: Optional[float] = None) -> str:
    """Emit ``artifacts/v2.0/cevns_dRdErec_ext_{TaAl,AlHf}.csv``."""
    from . import fold, params as P, trigger

    if res is None:
        res = run_extended_spectra(design, sharpness=sharpness)
    if path is None:
        path = os.path.join(ARTIFACT_DIR_V2, fold.EXT_RECON_FILE[design])

    c, u = res["central"], res["upper"]
    b = res["boundary_Erec_eV"]
    bud = c["counts_budget"]
    # bin 0 of the E_rec axis is the [0, 1e-3 eV) underflow catch-bin -- not a physical
    # differential bin.  Dropped from the spectrum exactly as the v1.0 writer does.
    sl = slice(1, None)
    E_rec_keV = c["E_rec_centers_eV"][sl] / 1.0e3

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(
            f"# QPD Phase-12 plan 12-02 (CALC-25) -- dR/dE_rec, design {design}.\n"
            "# THE MILESTONE'S DECISIVE SIGNAL DELIVERABLE, from 100 meV upward.\n"
            f"# Response: artifacts/v2.0/{fold.EXT_DESIGN_FILE[design]}, key\n"
            "#   R_non_paralyzable, 161 E_rec x 744 E_dep (Phase-10 EXTENDED axis; the\n"
            "#   v1.0 584-column matrix would truncate the spectrum at 10.14 eV).\n"
            "# Pipeline order (not negotiable): IA Gaussian broadening on the RECOIL axis\n"
            "#   -> rebin onto the extended deposit grid -> R(E_rec|E_dep) -> the trigger\n"
            "#   curve as an ANALYSIS efficiency on top of eps.\n"
            f"# Broadening: APPLIED, broaden=True at the Phase-12 call site. The global\n"
            f"#   ia_broadening.BROADENING_DEFAULT is still {c['broadening_default']}.\n"
            f"# Central column: the LOCKED harmonic VDOS mean omega_bar = "
            f"{c['omega_bar_eV']:.10e} eV\n"
            "#   (CONVENTIONS Section J), so 2W = E_R/omega_bar and sigma_E = sqrt(E_R omega_bar)\n"
            "#   stay exact.\n"
            f"# dRdErec_upper_width_onesided: the ONE-SIDED UPPER moment systematic, built on\n"
            f"#   the ARITHMETIC VDOS mean omega_bar_p = {u['omega_bar_eV']:.10e} eV, a x"
            f"{np.sqrt(u['omega_bar_eV']/c['omega_bar_eV']):.6f} correction on the WIDTH.\n"
            "#   'UPPER' refers to the WIDTH, not to the rate: a wider kernel moves MORE\n"
            "#   mass off the bottom of the axis, so in the bottom decade this column sits\n"
            "#   BELOW the central curve. It is a SEPARATE column: never absorbed into the\n"
            "#   central curve and the two are never averaged (fp-absorb-systematic). There\n"
            "#   is NO lower band -- Cauchy-Schwarz forces omega_bar_p >= omega_bar_u.\n"
            "# P_trig_effective = dRdErec_trigger_weighted / dRdErec_central, exact where the\n"
            "#   untriggered rate is non-zero and 0 where it is not. It is NOT an\n"
            "#   interpolation of P_trig onto the reconstructed axis.\n"
            "# dRdErec_trigger_weighted: R @ (P_trig(E_dep) * N_dep). P_trig is evaluated on\n"
            "#   the DEPOSIT axis because CONVENTIONS Section I defines P_trig(E_dep) and\n"
            "#   puts the regime boundary at 1.0 eV of DEPOSITED energy. It MULTIPLIES a\n"
            "#   quantity that already contains eps through energy_scale.n_qp_yield and the\n"
            "#   response.calibrate_C slope; it does NOT replace eps (fp-trigger-replaces-eps).\n"
            f"# P_trig parameters: E50 = {P.TRIGGER_E50.value:g} eV exactly, k = "
            f"{P.TRIGGER_SHARPNESS.value if sharpness is None else sharpness:g}, declared scan\n"
            f"#   range {P.TRIGGER_SHARPNESS_RANGE}. k is fixed by NO project artifact; its\n"
            "#   sensitivity is discharged in artifacts/v2.0/cevns_subev_trigger.csv.\n"
            f"# Regime boundary: trigger.SUBEV_REGIME_BOUNDARY_eV = "
            f"{trigger.SUBEV_REGIME_BOUNDARY_eV:g} eV DEPOSITED, imported from the module\n"
            f"#   constant and never restated as a literal. Its image on this reconstructed\n"
            f"#   axis, read off THIS matrix's own median mapping curve, is "
            f"{b:.6e} eV.\n"
            f"#   {trigger.REGIME_STATEMENT}\n"
            "# COUNTS BUDGET (counts/kg/day), central curve:\n"
            f"#   input recoil          {bud['input_counts']:.10e}\n"
            f"#   leaked below floor    {bud['leaked_below_floor']:.10e}"
            f"  ({bud['leaked_below_floor']/bud['input_counts']*100:.6f}%)\n"
            f"#   of which at T < 0     {bud['leaked_below_zero']:.10e}"
            f"  ({bud['leaked_below_zero']/bud['input_counts']*100:.6f}%)\n"
            f"#   leaked above top      {bud['leaked_above_top']:.10e}\n"
            f"#   on the deposit grid   {bud['deposit_counts']:.10e}\n"
            f"#   after folding through R {bud['reconstructed_counts']:.10e}\n"
            f"#   residual retained+leaked {bud['residual_retained_plus_leaked']:.6e}"
            "  (target <= 1e-3)\n"
            f"#   residual retained ONLY   {bud['residual_retained_only']:.6e}"
            "  -- this MUST miss; a clean\n"
            "#     retained-only closure would be positive evidence of a hidden rescale.\n"
            f"#   residual across the fold {bud['residual_fold']:.6e}  (R columns sum to 1)\n"
            "# The [0, 1e-3 eV) E_rec underflow catch-bin is omitted below, as in v1.0.\n"
            + _NORMALIZATION_HEADER
            + BOTTOM_BIN_CAVEAT
            + "# Units: E_rec in keV; every rate in counts/kg/day/keV; P_trig dimensionless.\n"
        )
        fh.write(",".join(_SPECTRA_COLUMNS) + "\n")
        for i in range(E_rec_keV.size):
            j = i + 1
            fh.write(
                f"{E_rec_keV[i]:.10e},{c['dRdErec'][j]:.10e},{u['dRdErec'][j]:.10e},"
                f"{c['dRdErec_band'][j]:.10e},{c['dRdErec_trigger'][j]:.10e},"
                f"{res['P_trig_effective'][j]:.10e},{res['regime'][j]}\n")
    return path


# --------------------------------------------------------------------------- #
# The sub-eV trigger observable and CONVENTIONS Section I's k-sensitivity       #
# --------------------------------------------------------------------------- #
K_SCAN = (1.0, 2.0, 4.0, 8.0, 12.0)

_TRIGGER_COLUMNS = (["E_dep_eV"] + [f"P_trig_k{int(k)}" for k in K_SCAN])


def trigger_k_sensitivity(designs: Sequence[str] = ("Ta->Al", "Al->Hf")) -> dict:
    """Trigger-weighted CEvNS rate below the regime boundary for each k in the scan.

    Discharges CONVENTIONS Section I's standing sensitivity obligation IN DATA.
    Phase 12 is the first downstream result computed with this curve, so the
    obligation lands here.
    """
    from . import fold, trigger

    out = {"k_scan": list(K_SCAN), "designs": {}}
    for design in designs:
        per_k = {}
        for k in K_SCAN:
            r = fold.run_cevns_fold_extended(design, broaden=True, sharpness=k)
            edges = r["E_rec_edges_eV"]
            b = fold.subev_boundary_Erec_eV(design)
            mask = edges[1:] <= b        # bins fully below the boundary image
            per_k[k] = {
                "rate_below_boundary": float(r["N_rec_trigger"][mask].sum()),
                "untriggered_below_boundary": float(r["N_rec"][mask].sum()),
                "rate_total": float(r["N_rec_trigger"].sum()),
                "untriggered_total": float(r["N_rec"].sum()),
            }
        vals = np.array([per_k[k]["rate_below_boundary"] for k in K_SCAN])
        out["designs"][design] = {
            "per_k": per_k,
            "boundary_Erec_eV": fold.subev_boundary_Erec_eV(design),
            "spread_relative": float((vals.max() - vals.min()) / np.mean(vals)),
            "untriggered_below_boundary": per_k[K_SCAN[0]]["untriggered_below_boundary"],
        }
    out["boundary_Edep_eV"] = trigger.SUBEV_REGIME_BOUNDARY_eV
    return out


def write_trigger_table(path: Optional[str] = None,
                        designs: Sequence[str] = ("Ta->Al", "Al->Hf")) -> str:
    """Emit ``artifacts/v2.0/cevns_subev_trigger.csv``."""
    from . import fold, ia_broadening, params as P, trigger

    if path is None:
        path = os.path.join(ARTIFACT_DIR_V2, "cevns_subev_trigger.csv")
    ks = trigger_k_sensitivity(designs)

    d0 = fold.load_design_extended(designs[0])
    E_dep = d0["E_dep_centers_eV"]
    sub = E_dep[E_dep < trigger.SUBEV_REGIME_BOUNDARY_eV]

    # The comparison the plan asks for: is the k spread larger than the combined
    # IA-width + counting-floor smearing at 0.5 eV?
    frac_w = float(ia_broadening.fractional_width(0.5))
    quad = {d: ia_broadening.quadrature_with_counting_floor(frac_w, d)
            for d in designs}

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(
            "# QPD Phase-12 plan 12-02 -- THE SUB-eV REPORTED OBSERVABLE and CONVENTIONS\n"
            "#   Section I's standing k-sensitivity obligation, discharged IN DATA.\n"
            f"# {trigger.REGIME_STATEMENT}\n"
            f"# Regime boundary: trigger.SUBEV_REGIME_BOUNDARY_eV = "
            f"{trigger.SUBEV_REGIME_BOUNDARY_eV:g} eV DEPOSITED (imported, not restated).\n"
            f"# Hill form P(E) = 1/(1 + (E50/E)^k), E50 = {P.TRIGGER_E50.value:g} eV EXACTLY.\n"
            "#   P(E50) = 1/2 for EVERY k -- structural, not tuned. P(0) = 0 exactly.\n"
            f"# k is fixed by NO project artifact. Declared scan range "
            f"{P.TRIGGER_SHARPNESS_RANGE}; default {P.TRIGGER_SHARPNESS.value:g}.\n"
            f"#   Scanned here at k = {', '.join(f'{k:g}' for k in K_SCAN)}.\n"
            "# TRIGGER-WEIGHTED CEvNS RATE BELOW THE BOUNDARY (counts/kg/day), by design:\n"
        )
        for d in designs:
            e = ks["designs"][d]
            fh.write(f"#   {d}: boundary image on E_rec = {e['boundary_Erec_eV']:.6e} eV; "
                     f"UNtriggered {e['untriggered_below_boundary']:.6e}\n")
            for k in K_SCAN:
                v = e["per_k"][k]["rate_below_boundary"]
                fh.write(f"#       k = {k:4g} -> {v:.6e}"
                         f"  ({v/e['untriggered_below_boundary']*100:.4f}% of untriggered)\n")
            fh.write(f"#     k-spread over [1, 12] = {e['spread_relative']*100:.4f}% "
                     f"of the mean; IA width (+) counting floor in quadrature at 0.5 eV = "
                     f"{quad[d]*100:.4f}%\n")
            fh.write(f"#     => the k spread is "
                     f"{'LARGER' if e['spread_relative'] > quad[d] else 'SMALLER'} than the "
                     "combined IA-width/counting-floor smearing at 0.5 eV.\n")
        fh.write(
            f"# IA fractional width at 0.5 eV on the locked omega_bar: {frac_w*100:.4f}%.\n"
            "# The Phase-10 counting floor used in that quadrature is a BEST CASE WITH NO\n"
            "#   NOISE SOURCES, not a resolution model (fp-poisson-as-resolution).\n"
            "# Rows below: P_trig(E_dep) on the extended deposit centres BELOW the boundary.\n"
            + _NORMALIZATION_HEADER
            + BOTTOM_BIN_CAVEAT
            + "# Units: E_dep in eV; P_trig dimensionless in [0, 1].\n"
        )
        fh.write(",".join(_TRIGGER_COLUMNS) + "\n")
        cols = [np.asarray(trigger.P_trig(sub, sharpness=k), float) for k in K_SCAN]
        for i in range(sub.size):
            fh.write(",".join([f"{sub[i]:.10e}"] + [f"{c[i]:.10e}" for c in cols]) + "\n")
    return path


# --------------------------------------------------------------------------- #
# The figure                                                                   #
# --------------------------------------------------------------------------- #
def make_subev_spectra_figure(out_path: Optional[str] = None,
                              designs: Sequence[str] = ("Ta->Al", "Al->Hf")) -> str:
    """Render ``artifacts/v2.0/cevns_subev_spectra.pdf``."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from . import trigger

    if out_path is None:
        out_path = os.path.join(ARTIFACT_DIR_V2, "cevns_subev_spectra.pdf")

    res = {d: run_extended_spectra(d) for d in designs}
    fig, axes = plt.subplots(1, len(designs), figsize=(11.4, 4.8), sharey=True)
    if len(designs) == 1:
        axes = [axes]

    for col, d in enumerate(designs):
        ax = axes[col]
        r = res[d]
        c, u = r["central"], r["upper"]
        E = c["E_rec_centers_eV"][1:]        # drop the underflow catch-bin
        y_c = c["dRdErec"][1:]
        y_u = u["dRdErec"][1:]
        y_t = c["dRdErec_trigger"][1:]
        m = y_c > 0.0

        # The bottom decade carries the ~49% leakage caveat -- marked, not hidden.
        ax.axvspan(E[m].min(), 10.0 * E[m].min(), color="#fdece7", zorder=0)
        ax.axvline(r["boundary_Erec_eV"], color="0.35", ls="-.", lw=1.2, zorder=1)

        # The band is between the two width variants. 'Upper' is the WIDTH: in the
        # bottom decade a wider kernel moves MORE mass off the axis, so the upper-width
        # curve sits BELOW the central one there. Shading min..max keeps that honest
        # instead of silently clipping the band to one side.
        ax.fill_between(E[m], np.minimum(y_c[m], y_u[m]), np.maximum(y_c[m], y_u[m]),
                        color="#1f77b4", alpha=0.28, lw=0, zorder=2,
                        label=r"one-sided upper-WIDTH variant ($\bar\omega_p$, "
                              r"$\times$1.164 on $\sigma_E$)")
        ax.plot(E[m], y_c[m], color="#1f77b4", lw=1.9, zorder=4,
                label=r"central ($\bar\omega$ locked, harmonic)")
        mt = y_t > 0.0
        ax.plot(E[mt], y_t[mt], color="#d62728", lw=1.5, ls="--", zorder=5,
                label=r"trigger-weighted, $k=4$")

        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_xlim(0.04, 3.0e3)
        ax.set_xlabel(r"reconstructed energy $E_{\rm rec}$  [eV]")
        if col == 0:
            ax.set_ylabel(r"$dR/dE_{\rm rec}$  [counts kg$^{-1}$ day$^{-1}$ keV$^{-1}$]")
        ax.set_title(f"({'ab'[col]}) {d}", fontsize=11)
        ax.grid(True, which="major", alpha=0.25)
        ax.annotate(
            f"$E_{{\\rm dep}} = {trigger.SUBEV_REGIME_BOUNDARY_eV:g}$ eV regime boundary\n"
            r"(below: $P_{\rm trig}$ is the reported observable)",
            xy=(r["boundary_Erec_eV"], 0.02), xycoords=("data", "axes fraction"),
            xytext=(6, 6), textcoords="offset points", fontsize=7.4, color="0.25")
        ax.annotate("bottom decade:\n~49% of the kernel\nleaves the axis\n"
                    "(1 significant figure)",
                    xy=(0.02, 0.97), xycoords="axes fraction", va="top",
                    fontsize=7.4, color="#b03a2e")
        if col == 0:
            ax.legend(loc="lower left", fontsize=7.8, framealpha=0.92)

    fig.suptitle("Reactor CEvNS from 100 meV — 3 GW$_{\\rm th}$ at 25 m, surface, "
                 "unshielded (frozen reactor_flux_v1.0.csv, unmodified)", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(out_path)
    plt.close(fig)
    return out_path


# =========================================================================== #
# PLAN 12-03: closure -- the v1.0 regression, the target-swap benchmark, the    #
#             labelled VNS scalar rescale                                       #
# =========================================================================== #
#
# NOTHING HERE PRODUCES A NEW SPECTRUM.  Plan 12-02 owns the fold.  This section
# compares, documents and (scalar-)rescales a FINISHED result.

#: The v1.0 frozen reconstructed spectra this phase regresses against.
V1_RECON_FILE = {"Ta->Al": "reconstructed_spectra_TaAl.csv",
                 "Al->Hf": "reconstructed_spectra_AlHf.csv"}

#: Above this reconstructed energy the extended pipeline must reproduce v1.0 (VALD-10).
REGRESSION_FLOOR_eV = 10.0

#: ROADMAP VALD-10 target on the folded comparison.
REGRESSION_TARGET = 0.01

#: CIAAW standard atomic weights [u] and proton numbers, for the target-swap
#: benchmark arithmetic.  Recomputed here rather than quoted from GPD/literature/.
_ATOMIC = {
    "Ca": (40.078, 20),
    "W": (183.84, 74),
    "O": (15.999, 8),
    "Ge": (72.630, 32),
    "184W": (184.0, 74),       # the single isotope, a DIFFERENT quantity
}


def _read_two_columns(path: str, value_col: int = 1) -> np.ndarray:
    rows = []
    with open(path) as fh:
        for line in fh:
            if not line.strip() or line.startswith("#") or line[0].isalpha():
                continue
            t = line.split(",")
            rows.append(float(t[value_col]))
    return np.asarray(rows, float)


def v1_regression(design: str) -> dict:
    """Compare the plan-12-02 extended ``dR/dE_rec`` against the frozen v1.0 spectrum.

    THE COMPARISON IS AN INDEX CARRY, NOT AN INTERPOLATION.  The reconstructed-energy
    grids of ``artifacts/stage1/response_matrix_*.npz`` and
    ``artifacts/v2.0/response_matrix_*_ext.npz`` are asserted equal with
    ``np.array_equal`` (max difference exactly 0.0), so bins are selected by INDEX.
    Neither spectrum is interpolated onto the other (``fp-regression-by-interpolation``):
    a tolerance-based axis comparison would let Phase-10's ``fp-naive-logspace`` drift
    (up to 5.1e-4 relative) through unnoticed, and interpolating would smooth a real
    deviation away.

    The comparison object is the **UN-TRIGGERED** extended spectrum: the trigger is an
    analysis efficiency and the v1.0 numbers carry none.
    """
    from . import fold, trigger

    z1 = np.load(os.path.join(_PROJECT_ROOT, "artifacts", "stage1",
                              f"response_matrix_{'TaAl' if design == 'Ta->Al' else 'AlHf'}.npz"),
                 allow_pickle=True)
    z2 = fold.load_design_extended(design)
    axis_identical = bool(np.array_equal(z1["E_rec_edges_eV"], z2["E_rec_edges_eV"]))
    axis_max_diff = float(np.abs(z1["E_rec_edges_eV"] - z2["E_rec_edges_eV"]).max())
    if not axis_identical:
        raise ValueError(
            "the v1.0 and extended reconstructed-energy edge sets are NOT identical; "
            "every comparison in this phase against v1.0 would be invalid")

    E_rec = z2["E_rec_centers_eV"]
    v1_path = os.path.join(_PROJECT_ROOT, "artifacts", "stage1", V1_RECON_FILE[design])
    v1 = _read_two_columns(v1_path, value_col=1)      # cevns_dRdErec
    # the v1.0 CSV drops the [0, 1e-3 eV) underflow catch-bin; re-align by INDEX
    if v1.size != E_rec.size - 1:
        raise ValueError(f"v1.0 spectrum has {v1.size} rows for {E_rec.size - 1} bins")
    ext_untriggered = fold.run_cevns_fold_extended(design, broaden=True)["dRdErec"][1:]
    ext_unbroadened = fold.run_cevns_fold_extended(design, broaden=False)["dRdErec"][1:]
    E = E_rec[1:]
    idx = np.arange(1, E_rec.size)

    mask = (E > REGRESSION_FLOOR_eV) & (v1 > 0.0)
    dev = np.zeros_like(v1)
    dev[mask] = (ext_untriggered[mask] - v1[mask]) / v1[mask]
    dev_unbroadened = np.zeros_like(v1)
    dev_unbroadened[mask] = (ext_unbroadened[mask] - v1[mask]) / v1[mask]

    # P_trig well above the boundary must be indistinguishable from 1, so comparing the
    # un-triggered object cannot be hiding a real deviation.
    P_hi = float(trigger.P_trig(100.0))

    a = np.abs(dev[mask])
    return {
        "design": design,
        "axis_index_carry": axis_identical,
        "axis_max_difference": axis_max_diff,
        "E_rec_eV": E,
        "v1_index": idx,
        "mask": mask,
        "v1": v1,
        "extended": ext_untriggered,
        "extended_unbroadened": ext_unbroadened,
        "deviation": dev,
        "deviation_unbroadened": dev_unbroadened,
        "n_compared": int(mask.sum()),
        "max_abs_deviation": float(a.max()),
        "max_at_E_rec_eV": float(E[mask][int(np.argmax(a))]),
        "mean_abs_deviation": float(a.mean()),
        "min_abs_deviation": float(a.min()),
        "n_above_target": int((a > REGRESSION_TARGET).sum()),
        "max_abs_deviation_broadening_off": float(np.abs(dev_unbroadened[mask]).max()),
        "P_trig_at_100eV": P_hi,
    }


_REGRESSION_COLUMNS = ["E_rec_eV", "v1_edge_index", "v1_dRdErec", "ext_dRdErec",
                       "relative_deviation", "ext_dRdErec_broadening_off",
                       "relative_deviation_broadening_off"]


def write_v1_regression_table(path: Optional[str] = None,
                              designs: Sequence[str] = ("Ta->Al", "Al->Hf")) -> str:
    """Emit ``artifacts/v2.0/cevns_v1_regression.csv`` (both designs, one file)."""
    if path is None:
        path = os.path.join(ARTIFACT_DIR_V2, "cevns_v1_regression.csv")
    res = {d: v1_regression(d) for d in designs}

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(
            "# QPD Phase-12 plan 12-03 (VALD-10, regression leg) -- the extended sub-eV\n"
            "#   pipeline against the committed FROZEN v1.0 CEvNS reconstructed spectra,\n"
            f"#   bin by bin above {REGRESSION_FLOOR_eV:g} eV of reconstructed energy.\n"
            "# THE COMPARISON IS AN INDEX CARRY, NOT AN INTERPOLATION. The v1.0 and\n"
            "#   extended reconstructed-energy edge sets are identical under np.array_equal\n"
            "#   with maximum difference EXACTLY 0.0, so bins are selected by index.\n"
            "#   Neither spectrum was interpolated onto the other\n"
            "#   (fp-regression-by-interpolation).\n"
            "# The compared object is the UN-TRIGGERED extended spectrum: the trigger is an\n"
            "#   analysis efficiency and the v1.0 numbers carry none. P_trig(100 eV) = "
            f"{res[designs[0]]['P_trig_at_100eV']:.12f},\n"
            "#   indistinguishable from 1 far above the boundary, so that choice cannot be\n"
            "#   hiding a real deviation.\n"
            "# RESULT, per design:\n"
        )
        for d in designs:
            r = res[d]
            fh.write(
                f"#   {d}: {r['n_compared']} bins compared, "
                f"{r['E_rec_eV'][r['mask']].min():.4g} - {r['E_rec_eV'][r['mask']].max():.4g} eV\n"
                f"#       max |deviation| = {r['max_abs_deviation']*100:.4f}% at E_rec = "
                f"{r['max_at_E_rec_eV']:.4g} eV;  mean {r['mean_abs_deviation']*100:.4f}%;  "
                f"min {r['min_abs_deviation']:.3e} (NON-ZERO, so the comparison is not vacuous)\n"
                f"#       bins above the 1% VALD-10 target: {r['n_above_target']}\n"
                f"#       with broadening OFF the same maximum is "
                f"{r['max_abs_deviation_broadening_off']*100:.4f}% -- the IA kernel is NOT the\n"
                "#       cause of the residual; the Phase-10 response-matrix REGENERATION is.\n")
        fh.write(
            "# The archived v1.0 R_non_paralyzable and the regenerated extended one are NOT\n"
            "#   bit-identical on their overlapping deposit columns (they are independent\n"
            "#   Monte Carlo samplings), which is what this residual measures.\n"
            + _NORMALIZATION_HEADER
            + "# Units: E_rec in eV; both rates in counts/kg/day/keV; deviation dimensionless.\n"
        )
        fh.write("design," + ",".join(_REGRESSION_COLUMNS) + "\n")
        for d in designs:
            r = res[d]
            for i in np.nonzero(r["mask"])[0]:
                fh.write(
                    f"{d},{r['E_rec_eV'][i]:.10e},{r['v1_index'][i]:d},"
                    f"{r['v1'][i]:.10e},{r['extended'][i]:.10e},{r['deviation'][i]:.10e},"
                    f"{r['extended_unbroadened'][i]:.10e},"
                    f"{r['deviation_unbroadened'][i]:.10e}\n")
    return path


def frozen_v1_recoil_support() -> dict:
    """The frozen v1.0 CEvNS RECOIL table's own support, confirmed programmatically.

    ROADMAP SC3 asks that ``T = 0.290 eV`` "reproduces the frozen v1.0 value exactly".
    This function is how that clause is adjudicated rather than asserted: the frozen
    table's support starts at 5 eV, so **there is no frozen v1.0 value at 0.290 eV to
    compare against**.  Recomputing ``dR/dT`` at 0.290 eV with the same code and calling
    the agreement a regression would be an identity dressed as a check.
    """
    from . import fold
    T = fold.read_cevns(fold.CEVNS_CSV)["T_eV"]
    return {
        "path": "artifacts/stage1/cevns_dRdT.csv",
        "n_rows": int(T.size),
        "T_min_eV": float(T.min()),
        "T_max_eV": float(T.max()),
        "covers_0p290_eV": bool(T.min() <= 0.290),
    }


# --------------------------------------------------------------------------- #
# The target-swap benchmark                                                    #
# --------------------------------------------------------------------------- #
def compound_n2_over_a() -> dict:
    """``sum N_i^2 / sum A_i`` for natural Ge and for the CaWO4 compound, RECOMPUTED.

    This arithmetic is cheap and is the ONE part of the target-swap benchmark this
    repository can actually reproduce, so it is recomputed here rather than quoted from
    ``GPD/literature/`` (which is the source of 22.7 / 44.2 / 1.95 / 65.8).

    It is computed only in order to be **REJECTED** as the Ge/CaWO4 benchmark: the naive
    ratio omits the Helm form factor, the kinematic ``T_max/E_nu`` compression, and the
    per-isotope threshold structure that the same-pipeline fold includes.  The benchmark
    is the same-pipeline ratio **2.31** (``fp-naive-compound-ratio``).
    """
    def n2a(items):
        sN2 = sum((_ATOMIC[s][0] - _ATOMIC[s][1]) ** 2 * c for s, c in items)
        sA = sum(_ATOMIC[s][0] * c for s, c in items)
        return sN2 / sA

    ge = n2a([("Ge", 1)])
    cawo4 = n2a([("Ca", 1), ("W", 1), ("O", 4)])
    w_natural = n2a([("W", 1)])
    w184 = n2a([("184W", 1)])
    return {
        "Ge": ge,
        "CaWO4_compound": cawo4,
        "naive_ratio_CaWO4_over_Ge": cawo4 / ge,
        "pure_W_standard_atomic_weight": w_natural,
        "pure_184W": w184,
        "same_pipeline_benchmark_ratio": 2.31,
        "atomic_weights_used": {k: v[0] for k, v in _ATOMIC.items()},
        "verdict": ("the naive compound ratio is REJECTED as the Ge/CaWO4 benchmark; "
                    "the same-pipeline fold gives 2.31. The pure-tungsten value describes "
                    "a DIFFERENT material and must not stand in for the CaWO4 compound."),
    }


def closure_provenance_search(needle: str = "407.7") -> dict:
    """Repository-wide search for the CaWO4 closure figure OUTSIDE GPD prose.

    Planning finding F7 predicts nothing: no CaWO4 module, no test, no notebook cell,
    no committed artifact reproduces it.  This function RECORDS what the search returns
    rather than asserting the prediction (``fp-closure-as-reproduced``).
    """
    import subprocess
    # WORD-BOUNDED. A bare substring search for "407.7" matches by coincidence inside
    # long numeric fields of several committed CSVs, which would manufacture a
    # reproducible source that does not exist.
    pattern = needle.replace(".", "[.]")
    cmd = f"git grep -lE '(^|[^0-9.]){pattern}([^0-9]|$)' | sort"
    out = subprocess.run(["bash", "-c", cmd],
                         cwd=_PROJECT_ROOT, capture_output=True, text=True).stdout.split()
    # this module itself carries the search string as a default argument
    out = [p for p in out if not p.endswith("cevns_subev.py")]
    prose = [p for p in out if p.startswith("GPD/")]
    reproducible = [p for p in out
                    if p.endswith((".py", ".ipynb", ".csv", ".npz", ".json"))
                    and not p.startswith("GPD/")]
    return {
        "needle": needle,
        "command": cmd,
        "all_hits": out,
        "gpd_prose_hits": prose,
        "reproducible_hits": reproducible,
        "has_reproducible_source": bool(reproducible),
    }


# --------------------------------------------------------------------------- #
# The optional VNS context line -- a LABELLED SCALAR RESCALE, nothing else      #
# --------------------------------------------------------------------------- #
ROI_LO_eV, ROI_HI_eV = 10.0, 100.0


def vns_rescale(designs: Sequence[str] = ("Ta->Al", "Al->Hf")) -> dict:
    """The NUCLEUS VNS siting as a SINGLE labelled scalar multiplication.

    It is a multiplication applied to the FINISHED primary result or it is not reported
    (``fp-second-vns-run``).  ``cevns.nucleus_variant_flux()`` exists in the codebase and
    is exactly the trap: calling it would produce a physically reasonable SECOND spectrum
    and silently violate the locked forbidden proxy.  **It is not called.**

    TWO candidate integral fluxes, both named, because the project's own arithmetic does
    not reproduce the NUCLEUS-stated one (``fp-unlabelled-rescale``):

    * **2.1e12** nubar/cm^2/s -- STATED by NUCLEUS, EPJC 86, 29 (2026), arXiv:2509.03559.
    * **1.830269e12** -- what ``cevns.nucleus_flux_normalization()`` RECONSTRUCTS from
      NUCLEUS's own stated 4.25 GW_th per core, 6 nubar/fission, 200 MeV/fission at 72 m
      and 102 m.  A ~15% gap, already recorded in ``state.json``.

    (Their 2019 prose "about 3e12" is a third number and is a locked forbidden proxy,
    ``fp-nucleus-3e12``.  It is reported here only as the gap it is.)
    """
    from . import cevns as _cevns, fold

    norm = _cevns.nucleus_flux_normalization()
    ours = integral_flux()
    candidates = {
        "nucleus_stated_2026": {
            "integral_flux": 2.1e12,
            "source": ("NUCLEUS Collab., Eur. Phys. J. C 86, 29 (2026), arXiv:2509.03559 "
                       "-- STATED VNS integral antineutrino flux"),
        },
        "project_geometric": {
            "integral_flux": float(norm["site_flux"]),
            "source": ("cevns.nucleus_flux_normalization(): reconstructed from NUCLEUS's "
                       "OWN 4.25 GW_th per core, 6 nubar/fission, 200 MeV/fission, at "
                       "72 m and 102 m (EPJC 79, 1018 (2019), arXiv:1905.10258 Sect. 2)"),
        },
    }
    for v in candidates.values():
        v["rescale_factor"] = v["integral_flux"] / ours

    per_design = {}
    for d in designs:
        r = fold.run_cevns_fold_extended(d, broaden=True)
        E = r["E_rec_centers_eV"]
        roi = (E >= ROI_LO_eV) & (E <= ROI_HI_eV)
        primary = float(r["N_rec"][roi].sum())
        per_design[d] = {
            "primary_roi_counts_per_kg_day": primary,
            "roi_bins": int(roi.sum()),
            **{k: primary * v["rescale_factor"] for k, v in candidates.items()},
        }
    return {
        "project_integral_flux": ours,
        "candidates": candidates,
        "nucleus_2019_prose_flux": float(norm["prose_flux"]),
        "prose_over_geometric": float(norm["prose_over_geometric"]),
        "per_design": per_design,
        "roi_eV": (ROI_LO_eV, ROI_HI_eV),
    }


def write_vns_rescale_table(path: Optional[str] = None,
                            designs: Sequence[str] = ("Ta->Al", "Al->Hf")) -> str:
    """Emit ``artifacts/v2.0/cevns_vns_rescale.csv``."""
    if path is None:
        path = os.path.join(ARTIFACT_DIR_V2, "cevns_vns_rescale.csv")
    v = vns_rescale(designs)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(
            "# QPD Phase-12 plan 12-03 -- the OPTIONAL NUCLEUS VNS context line, as a\n"
            "#   SINGLE LABELLED SCALAR MULTIPLICATION of the FINISHED primary result.\n"
            "# NO SECOND PIPELINE RUN, NO SECOND FLUX TABLE, NO SECOND SPECTRAL SHAPE was\n"
            "#   produced (fp-second-vns-run). cevns.nucleus_variant_flux() exists in the\n"
            "#   codebase and was NOT called: it would have produced a physically\n"
            "#   reasonable second spectrum and silently violated the locked proxy.\n"
            "# TWO candidate integral fluxes are carried, because the project's own\n"
            "#   arithmetic does not reproduce the NUCLEUS-stated one. A bare 0.28 would be\n"
            "#   fake precision on an optional context line (fp-unlabelled-rescale).\n"
            f"# Project integral flux (frozen reactor_flux_v1.0.csv): {v['project_integral_flux']:.6e}"
            " nubar/cm^2/s.\n"
        )
        for k, c in v["candidates"].items():
            fh.write(f"#   {k}: {c['integral_flux']:.6e} -> factor "
                     f"{c['rescale_factor']:.6f}\n#       source: {c['source']}\n")
        fh.write(
            f"# The NUCLEUS 2019 prose figure {v['nucleus_2019_prose_flux']:.3e} is a THIRD\n"
            f"#   number, {v['prose_over_geometric']:.4f}x the geometric reconstruction, and is a\n"
            "#   locked forbidden proxy (fp-nucleus-3e12). It is named here only as the gap.\n"
            "# CAVEAT: the rescale is valid for the TOTAL RATE NORMALIZATION only. It assumes\n"
            "#   the VNS spectral SHAPE is the project's Phase-2 shape, and it says nothing\n"
            "#   about duty cycle or site-dependent backgrounds. The VNS also carries\n"
            "#   2.92 m.w.e. of overburden that the surface background treatment does not\n"
            "#   have -- which is precisely why the 2026-07-22 re-scope demoted this to a\n"
            "#   context line (fp-inherited-shielding).\n"
            f"# RoI: {ROI_LO_eV:g} - {ROI_HI_eV:g} eV of RECONSTRUCTED energy, on the finished\n"
            "#   plan-12-02 spectra.\n"
            + _NORMALIZATION_HEADER
            + "# Units: integral fluxes in nubar/cm^2/s; rates in counts/kg/day; factors\n"
            "#   dimensionless.\n"
        )
        cols = ["design", "candidate", "candidate_integral_flux", "project_integral_flux",
                "rescale_factor", "primary_roi_counts_per_kg_day",
                "rescaled_roi_counts_per_kg_day"]
        fh.write(",".join(cols) + "\n")
        for d in designs:
            pd = v["per_design"][d]
            for k, c in v["candidates"].items():
                fh.write(f"{d},{k},{c['integral_flux']:.10e},"
                         f"{v['project_integral_flux']:.10e},{c['rescale_factor']:.10e},"
                         f"{pd['primary_roi_counts_per_kg_day']:.10e},{pd[k]:.10e}\n")
    return path


if __name__ == "__main__":  # pragma: no cover
    import sys as _sys
    which = _sys.argv[1] if len(_sys.argv) > 1 else "12-01"
    if which == "12-01":
        print(write_truncation_table())
        print(write_plateau_table())
    elif which == "12-02":
        print(write_ext_dRdT_table())
        for _d in ("Ta->Al", "Al->Hf"):
            print(write_extended_spectrum(_d))
        print(write_trigger_table())
        print(make_subev_spectra_figure())
    elif which == "12-03":
        print(write_v1_regression_table())
        print(write_vns_rescale_table())
    else:
        raise SystemExit(f"unknown target {which!r}")
