# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
#
# Phase-9 Plan 09-02: committed driver for the sea-level ambient neutron
# differential flux, built on the OFFICIAL, UNMODIFIED PARMA C++ routine at the
# pinned mirror commit 6ff37cacb8cf003e2fc269963f9a08f812407264.
#
# WHY THIS MODULE EXISTS.  Phase-7 verification gap D2 (severity: significant,
# called "the weakest reproducibility link in the phase") reads: "No PARMA
# driver committed; the decisive 3.55e-3 and 1.317e-2 integrals cannot be
# recomputed."  ROADMAP Phase 9 SC2 requires the neutron source be actually
# retrieved and integrity-checked rather than recalled.  This module closes D2:
# with it, both anchor integrals AND data/ambient_neutron_flux_v1.1.csv's own
# phi_default column are recomputable in-repo.
#
# =========================== SHAPE vs ANCHOR ROLES ===========================
#   * SHAPE  source : PARMA v4.10 / Sato T., PLOS ONE 10(12):e0144679 (2015),
#                     DOI 10.1371/journal.pone.0144679 (OPEN ACCESS).  The
#                     fitted coefficients are NOT tabulated in the article --
#                     they live in the EXPACS/PARMA distribution -- which is why
#                     the source is retrieved and compiled rather than typed.
#   * ANCHOR source : Gordon M. S. et al., IEEE Trans. Nucl. Sci. 51, 3427
#                     (2004), used ONLY as the >10 MeV INTEGRAL normalization
#                     benchmark.  Gordon's DIFFERENTIAL coefficients are
#                     PAYWALLED and were unsourceable in this environment, so
#                     Gordon is NOT the spectral shape source and must never be
#                     cited as one (guard fp-gordon-as-shape).
#
# ====================== LETHARGY: DIVIDE BY E EXACTLY ONCE ===================
# Sato Eq. (6) is an ENERGY-WEIGHTED (lethargy-form) normalized spectrum.
# THE ONE AND ONLY DIVISION BY E LIVES INSIDE PARMA ITSELF, at
# data/external/parma/src/subroutines.cpp line 673:
#
#     getNeutSpec = Fl * (basic * geofactor + ther) / e;
#
# so getNeutSpecCpp() already returns the PER-ENERGY differential
# dPhi/dE_n [cm^-2 s^-1 MeV^-1].  Neither parma_neutron_driver.cpp nor this
# module divides again (guard fp-lethargy-double-divide).  The identity
# INT phi dE == INT (E phi) d(ln E) is asserted in
# tests/test_ambient_neutron_flux.py::test_lethargy_divided_exactly_once.
#
# ================================== AXIS TAG =================================
# E_n is INCIDENT NEUTRON KINETIC ENERGY.  It is NOT a recoil axis: a 1 MeV
# neutron does not deposit 1 MeV of recoil.  No recoil kinematics, no keV_nr, no
# quenching factor appears anywhere in this module.  The n-Ge elastic fold is
# Phase 13.
#
# =============================== ACCURACY LABEL ==============================
# ACCURACY_LABEL = order_of_magnitude, attached at the point of definition and
# returned in the metadata of every public call.  The ONLY independent
# cross-check that exists on this spectrum is a SINGLE integral above 10 MeV
# agreeing to ~9% untuned; that constrains nothing about the eV-keV shape which
# is what actually sets the Ge recoil rate in the CEvNS region of interest.  The
# label is a consequence of the evidence, not a formality
# (guard fp-precision-inflation).

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass, field

import numpy as np

#: Accuracy class of every quantity this module emits.  There is no other
#: admissible value for the sea-level neutron channel.
ACCURACY_LABEL = "order_of_magnitude"

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))

PARMA_CACHE = os.path.join(REPO_ROOT, "data", "external", "parma")
PARMA_SRC = os.path.join(PARMA_CACHE, "src")
PARMA_DRIVER_CPP = os.path.join(PARMA_CACHE, "parma_neutron_driver.cpp")
PARMA_SUBROUTINES = os.path.join(PARMA_SRC, "subroutines.cpp")
PARMA_BINARY = os.path.join(PARMA_CACHE, "build_parma_neutron")

PINNED_COMMIT = "6ff37cacb8cf003e2fc269963f9a08f812407264"

# --------------------------------------------------------------------------- #
# Evaluation point -- EXPLICIT NAMED PARAMETERS, not buried constants.          #
# Phase-7 values, matching data/ambient_neutron_flux_v1.1.csv's header and the  #
# Gordon-2004 NYC reference the integral anchor refers to.                      #
# --------------------------------------------------------------------------- #
S_WINDEX_DEFAULT = 100.0     # W-index (mid-solar); PARMA converts to force-field potential
RC_GV_DEFAULT = 2.08         # vertical cut-off rigidity [GV], NYC
D_GCM2_DEFAULT = 1033.0      # atmospheric depth [g/cm^2], sea level, US Std Atm 1976
G_GEOM_DEFAULT = 0.15        # local geometry (ground water weight fraction), Sato default

#: The single scalar Gordon-2004 normalization anchor, applied UNIFORMLY at all
#: energies.  It constrains only the >10 MeV integral; propagating it onto the
#: eV-keV region is an assumption, not a measurement (see ACCURACY_LABEL).
K_GORDON_ANCHOR = 1.09610

#: Anchor values of record (data/ambient_neutron_flux_v1.1.csv header).
PHI_NATIVE_10MEV_10GEV = 3.239e-3   # cm^-2 s^-1, PARMA UNTUNED (k = 1)
PHI_GORDON_10MEV_10GEV = 3.550e-3   # cm^-2 s^-1, Gordon 3.5-3.6e-3 midpoint
PHI_BROAD_0P01EV_10GEV = 1.317e-2   # cm^-2 s^-1, anchored, 0.01 eV -> 10 GeV

#: Thermal cutoff convention adopted by this plan, stated with its number:
#: the standard CADMIUM CUTOFF at 0.5 eV = 5.0e-7 MeV.  Phi_th is defined as
#: the integral from the PARMA low-energy floor up to this bound.
E_THERMAL_CUTOFF_MEV = 5.0e-7
E_PARMA_FLOOR_MEV = 1.0e-8   # 0.01 eV -- the floor the committed header quotes


class ParmaBuildError(RuntimeError):
    """Raised when the pinned PARMA routine cannot be built or invoked."""


@dataclass(frozen=True)
class NeutronFlux:
    """dPhi/dE_n on a caller-supplied grid, with its accuracy label attached.

    A consumer cannot obtain a neutron number from this module without also
    receiving ``accuracy_label``.
    """

    e_n_mev: np.ndarray          # incident neutron kinetic energy [MeV]
    phi_cm2_s_mev: np.ndarray    # dPhi/dE_n [cm^-2 s^-1 MeV^-1]
    k: float                     # applied normalization scalar (dimensionless)
    evaluation_point: dict = field(default_factory=dict)
    accuracy_label: str = ACCURACY_LABEL
    axis_tag: str = "incident_neutron_kinetic_energy_NOT_recoil"
    shape_source: str = "PARMA_v4.10_Sato2015_PLOSONE_e0144679"
    norm_anchor: str = "Gordon2004_IEEE_TNS_51_3427_integral_gt10MeV_only"
    lethargy_division_site: str = (
        "data/external/parma/src/subroutines.cpp:673 "
        "(getNeutSpecCpp: '... / e') -- applied exactly once, nowhere else"
    )


# --------------------------------------------------------------------------- #
# Build / invoke                                                               #
# --------------------------------------------------------------------------- #
def parma_available() -> bool:
    """True if the frozen PARMA source and a C++ compiler are both present."""
    return (os.path.isfile(PARMA_SUBROUTINES)
            and os.path.isfile(PARMA_DRIVER_CPP)
            and shutil.which("c++") is not None)


def build(force: bool = False) -> str:
    """Compile the pinned PARMA routine UNMODIFIED plus the batch driver.

    Returns the binary path.  Raises :class:`ParmaBuildError` carrying the exact
    failing command and its stderr -- never a substituted number.
    """
    if os.path.isfile(PARMA_BINARY) and not force:
        return PARMA_BINARY
    if not os.path.isfile(PARMA_SUBROUTINES):
        raise ParmaBuildError(
            f"pinned PARMA source absent: {PARMA_SUBROUTINES} (commit {PINNED_COMMIT}). "
            "Re-run the retrieval command recorded in data/external/parma/MANIFEST.md."
        )
    cmd = ["c++", "-O2", "-std=c++17", "-o", PARMA_BINARY,
           PARMA_DRIVER_CPP, PARMA_SUBROUTINES]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0 or not os.path.isfile(PARMA_BINARY):
        raise ParmaBuildError(
            "PARMA build FAILED.\ncommand: " + " ".join(cmd)
            + f"\nreturncode: {proc.returncode}\nstderr:\n{proc.stderr}"
        )
    return PARMA_BINARY


def differential_flux(
    e_n_mev,
    *,
    k: float = K_GORDON_ANCHOR,
    s_windex: float = S_WINDEX_DEFAULT,
    rc_gv: float = RC_GV_DEFAULT,
    d_gcm2: float = D_GCM2_DEFAULT,
    g_geom: float = G_GEOM_DEFAULT,
) -> NeutronFlux:
    """dPhi/dE_n [cm^-2 s^-1 MeV^-1] at incident neutron energies ``e_n_mev`` [MeV].

    ``k`` is the uniform Gordon normalization scalar; pass ``k=1.0`` for PARMA's
    UNTUNED native spectrum (the honest, un-fitted cross-check).

    No division by E happens here -- PARMA already did it exactly once.
    """
    e = np.atleast_1d(np.asarray(e_n_mev, dtype=float))
    if np.any(e <= 0):
        raise ValueError("neutron kinetic energy must be strictly positive")

    binary = build()
    payload = "\n".join(repr(float(x)) for x in e.ravel()) + "\n"
    # subroutines.cpp opens "input/neutro/*.inp" RELATIVELY -> cwd must be the
    # PARMA source root.
    proc = subprocess.run([binary, repr(float(s_windex)), repr(float(rc_gv)),
                           repr(float(d_gcm2)), repr(float(g_geom))],
                          input=payload, capture_output=True, text=True,
                          cwd=PARMA_SRC)
    if proc.returncode != 0:
        raise ParmaBuildError(
            f"PARMA driver FAILED (rc={proc.returncode})\nstderr:\n{proc.stderr}")
    rows = [ln.split() for ln in proc.stdout.strip().splitlines() if ln.strip()]
    if len(rows) != e.size:
        raise ParmaBuildError(
            f"PARMA driver returned {len(rows)} rows for {e.size} energies")
    phi = np.array([float(r[1]) for r in rows], dtype=float) * float(k)

    return NeutronFlux(
        e_n_mev=e.reshape(np.shape(e_n_mev)) if np.ndim(e_n_mev) else e,
        phi_cm2_s_mev=phi.reshape(np.shape(e_n_mev)) if np.ndim(e_n_mev) else phi,
        k=float(k),
        evaluation_point={"s_windex": s_windex, "rc_gv": rc_gv,
                          "d_gcm2": d_gcm2, "g_geom": g_geom},
    )


# --------------------------------------------------------------------------- #
# Quadrature                                                                   #
# --------------------------------------------------------------------------- #
def log_grid(e_lo_mev: float, e_hi_mev: float, per_decade: int = 200) -> np.ndarray:
    """Log-spaced node vector with a STATED node density [nodes/decade]."""
    n = int(round(np.log10(e_hi_mev / e_lo_mev) * per_decade)) + 1
    return np.logspace(np.log10(e_lo_mev), np.log10(e_hi_mev), n)


def integral_flux(
    e_lo_mev: float,
    e_hi_mev: float,
    *,
    k: float = K_GORDON_ANCHOR,
    per_decade: int = 200,
    **eval_point,
) -> float:
    """Phi = INT dPhi/dE_n dE_n over [e_lo, e_hi] [cm^-2 s^-1].

    Deterministic trapezoidal quadrature in ln E on a log grid of stated node
    density.  Integrating phi dE as (E phi) d(ln E) is the SAME integral -- that
    identity is exactly what proves the lethargy division was applied once.
    """
    e = log_grid(e_lo_mev, e_hi_mev, per_decade)
    phi = differential_flux(e, k=k, **eval_point).phi_cm2_s_mev
    return float(np.trapz(e * phi, np.log(e)))


def solve_anchor_scalar(
    target_cm2_s: float = PHI_GORDON_10MEV_10GEV,
    e_lo_mev: float = 10.0,
    e_hi_mev: float = 1.0e4,
    per_decade: int = 200,
    **eval_point,
) -> float:
    """Solve for the uniform k that lands the [e_lo, e_hi] integral on ``target``.

    Because k multiplies the spectrum uniformly, the solution is exact:
    k = target / Phi_native.  Solving it independently and comparing against the
    committed 1.09610 is a real check, not a tautology, because Phi_native comes
    from the recompiled pinned source rather than from the committed header.
    """
    native = integral_flux(e_lo_mev, e_hi_mev, k=1.0,
                           per_decade=per_decade, **eval_point)
    return float(target_cm2_s / native)


def thermal_flux(
    *,
    e_lo_mev: float = E_PARMA_FLOOR_MEV,
    e_cut_mev: float = E_THERMAL_CUTOFF_MEV,
    k: float = K_GORDON_ANCHOR,
    per_decade: int = 200,
    **eval_point,
) -> tuple[float, dict]:
    """Phi_th: the separately named thermal component Phase 14 consumes.

    Returns ``(Phi_th [cm^-2 s^-1], metadata)``.  The integration bounds are
    STATED, not implied: from the PARMA low-energy floor 1.0e-8 MeV (0.01 eV, the
    floor the committed v1.1 header itself quotes) up to the standard CADMIUM
    CUTOFF 5.0e-7 MeV (0.5 eV).

    It is never zero and never silently omitted (ROADMAP Phase 9 SC4).
    """
    phi_th = integral_flux(e_lo_mev, e_cut_mev, k=k,
                           per_decade=per_decade, **eval_point)
    meta = {
        "quantity": "Phi_th",
        "value_cm2_s": phi_th,
        "e_lo_mev": e_lo_mev,
        "e_cut_mev": e_cut_mev,
        "cutoff_convention": "cadmium cutoff, 0.5 eV = 5.0e-7 MeV",
        "k": k,
        "accuracy_label": ACCURACY_LABEL,
        "axis_tag": "incident_neutron_kinetic_energy_NOT_recoil",
        "on_shared_energy_grid": False,
    }
    return phi_th, meta


# --------------------------------------------------------------------------- #
# Sub-eV table emission                                                        #
# --------------------------------------------------------------------------- #
#: Sub-eV table grid, DELIBERATELY NOT shared_energy_grid().  Phase 10 owns the
#: project grid extension below 10.14 eV and runs in PARALLEL with Phase 9;
#: taking a dependency on it here would serialize two independent phases.
THERMAL_TABLE_E_LO_MEV = 1.0e-8    # 0.01 eV
THERMAL_TABLE_E_HI_MEV = 1.0e-6    # 1 eV
THERMAL_TABLE_PER_DECADE = 100

THERMAL_TABLE_PATH = os.path.join(
    REPO_ROOT, "data", "ambient_neutron_thermal_v2.0.csv")


def write_thermal_table(path: str = THERMAL_TABLE_PATH,
                        *, k: float = K_GORDON_ANCHOR) -> str:
    """Emit data/ambient_neutron_thermal_v2.0.csv (Plan 09-02 deliv-thermal-table).

    Reproduce with:
        PYTHONPATH=src python -c \
          "from qpd_potential import parma_neutron_flux as p; p.write_thermal_table()"
    """
    e_mev = log_grid(THERMAL_TABLE_E_LO_MEV, THERMAL_TABLE_E_HI_MEV,
                     THERMAL_TABLE_PER_DECADE)
    phi = differential_flux(e_mev, k=k).phi_cm2_s_mev
    phi_native = differential_flux(e_mev, k=1.0).phi_cm2_s_mev
    phi_th, meta = thermal_flux(k=k, per_decade=800)
    phi_broad = integral_flux(E_PARMA_FLOOR_MEV, 1.0e4, k=k, per_decade=400)

    h = [
        "# QPD Phase-9 Plan 09-02 -- SUB-eV ambient neutron differential flux, version v2.0",
        "# ACCURACY_LABEL = order_of_magnitude   <-- attached HERE, at the point of definition,",
        "#   and to EVERY quantity below.  No downstream acceptance test may demand better than",
        "#   order-of-magnitude agreement on this channel (ROADMAP Phase 9 SC3).",
        "#",
        "# ============================ AXIS TAG (READ CAREFULLY) ============================",
        "# E_n is INCIDENT NEUTRON KINETIC ENERGY.  It is NOT a recoil axis: a 1 MeV neutron does",
        "# not deposit 1 MeV of recoil.  No recoil kinematics, no keV_nr, no ionization quenching",
        "# appears in this file.  The n-Ge elastic fold is Phase 13, not here.",
        "#",
        "# ======================== THIS GRID IS NOT shared_energy_grid() ====================",
        "# The nodes below are a STATED log grid, "
        f"{THERMAL_TABLE_PER_DECADE} nodes/decade over "
        f"[{THERMAL_TABLE_E_LO_MEV:.3e}, {THERMAL_TABLE_E_HI_MEV:.3e}] MeV "
        "= [0.01 eV, 1 eV].",
        "# It is DELIBERATELY NOT the project shared_energy_grid(), whose floor is 0.01 keV.",
        "# WHY: Phase 10 (sub-eV grid extension) owns the shared-grid extension and runs in",
        "# PARALLEL with Phase 9.  Placing this table on the shared grid would take a dependency",
        "# on Phase 10 and serialize two independent phases.  Phase 13/14 must resample.",
        "#",
        "# ================================ NAMED SCALAR ====================================",
        f"# Phi_th = {phi_th:.6e} cm^-2 s^-1   [ACCURACY_LABEL = order_of_magnitude]",
        f"#   integration bounds : {meta['e_lo_mev']:.6e} MeV -> {meta['e_cut_mev']:.6e} MeV",
        "#                        (0.01 eV -> 0.5 eV)",
        f"#   cutoff convention  : {meta['cutoff_convention']}",
        f"#   fraction of Phi(0.01 eV-10 GeV) = {phi_broad:.6e} : {phi_th / phi_broad:.4f}",
        "#   This is the separately named quantity Phase 14's (n,gamma) capture channel",
        "#   consumes.  It is NEVER set to zero and never silently omitted (ROADMAP SC4).",
        "#",
        "# ============================== SHAPE vs ANCHOR ====================================",
        "# SHAPE  : PARMA v4.10 / Sato T., PLOS ONE 10(12):e0144679 (2015), open access.",
        "#          Coefficients taken from the OFFICIAL PARMA C++ source at pinned commit",
        f"#          {PINNED_COMMIT} -- compiled UNMODIFIED, not typed.",
        "# ANCHOR : Gordon M. S. et al., IEEE Trans. Nucl. Sci. 51, 3427 (2004), used ONLY as",
        "#          the >10 MeV INTEGRAL benchmark.  Its DIFFERENTIAL coefficients are PAYWALLED",
        "#          and were unsourceable, so Gordon is NOT the spectral shape source.",
        f"# k = {k:.5f} applied uniformly at all energies (dimensionless).",
        "#   The only independent cross-check that exists is a SINGLE >10 MeV integral agreeing",
        "#   to ~8.8% UNTUNED.  It constrains nothing about the eV-keV shape.  That is WHY the",
        "#   accuracy label is order_of_magnitude -- a consequence, not a formality.",
        "#",
        "# =========================== EVALUATION POINT / SCENARIO ==========================",
        f"# s(W-index) = {S_WINDEX_DEFAULT}; r_c = {RC_GV_DEFAULT} GV (NYC); "
        f"d = {D_GCM2_DEFAULT} g/cm^2 (sea level); g = {G_GEOM_DEFAULT} (ground).",
        "# UNSHIELDED SURFACE, ZERO OVERBURDEN, outdoor.  phi_default = phi_hi (outdoor) is the",
        "# operative normalization.  The v1.1 table's phi_lo = phi_default/5 represents",
        "# INDOOR/building attenuation (NOT applied) and is NOT an error bar for this configuration;",
        "# it is not emitted here.  No NUCLEUS shielding quantity, no post-shield fluence, no buildup",
        "# factor and no veto credit enters -- all NOT applied; veto credit is exactly 1.0 by construction.",
        "#",
        "# =============================== LETHARGY DISCIPLINE ===============================",
        "# Sato Eq. (6) is an energy-weighted (lethargy-form) spectrum.  The division by E happens",
        "# EXACTLY ONCE, inside PARMA's own getNeutSpecCpp at",
        "# data/external/parma/src/subroutines.cpp:673 ('... / e').  Neither the C++ batch driver",
        "# nor src/qpd_potential/parma_neutron_flux.py divides again.",
        "#",
        "# reproduce: PYTHONPATH=src python -c \"from qpd_potential import "
        "parma_neutron_flux as p; p.write_thermal_table()\"",
        "# units: E_n_keV [keV]; phi [cm^-2 s^-1 MeV^-1]; accuracy_label per row.",
    ]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(h) + "\n")
        fh.write("E_n_keV,phi_default_cm2_s_MeV,phi_native_untuned_cm2_s_MeV,accuracy_label\n")
        for ee, pd_, pnat in zip(e_mev, phi, phi_native):
            fh.write(f"{ee * 1.0e3:.17g},{pd_:.9e},{pnat:.9e},{ACCURACY_LABEL}\n")
    return path
