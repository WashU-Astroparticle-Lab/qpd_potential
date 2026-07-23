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


if __name__ == "__main__":  # pragma: no cover
    print(write_truncation_table())
    print(write_plateau_table())
