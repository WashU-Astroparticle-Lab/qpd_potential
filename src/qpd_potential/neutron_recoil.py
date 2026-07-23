# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
#
# Phase-13 Plan 13-01/13-02: the Ge NEUTRON ELASTIC nuclear-recoil fold.
#
# WHAT THIS MODULE COMPUTES
#   dR/dT(T) = N_Ge * INT_{E_min(T)}^{E_top} phi(E_n) sigma_el(E_n) / (f E_n) dE_n
#   with E_min(T) = T / f and f = T_max/E_n the abundance-weighted kinematic factor
#   READ FROM THE FROZEN ELASTIC TABLE'S OWN HEADER (never transcribed from prose).
#
# ============================ AXIS TAG (READ CAREFULLY) ======================
# E_n is INCIDENT NEUTRON KINETIC ENERGY.  T is NUCLEAR RECOIL energy.  A 1 MeV
# neutron does NOT deposit 1 MeV.  The two are never conflated in a column name,
# a plot label, or a variable name anywhere in this module.
#
# ============================== RECOIL SCALE =================================
# T is on the UNIFIED PHONON SCALE, keV_nr, with NO Lindhard factor and NO
# ionization quenching (CONVENTIONS.md Section B; the frozen elastic table's own
# `recoil_axis` header line says the same).  Nothing here is keVee.
#
# ============================ NODE PLACEMENT IS PHYSICS ======================
# With the roughly 1/E epithermal flux the integrand phi sigma / (f E) behaves as
# 1/E^2 and is peaked EXACTLY at the lower limit E_min(T).  E_min(T) is therefore
# an EXACT quadrature node for every T, and the 23,155-point resonance-resolved
# union grid of the frozen table is carried in as exact nodes too, so the fold
# does not average across the resonances it exists to resolve
# (fp-unanchored-quadrature, fp-smooth-as-result).
#
# ============================== OPERATIVE FLUX ===============================
# phi_default == phi_hi, the OUTDOOR sea-level leg.  phi_lo = phi_default/5 is the
# INDOOR leg and is NOT an error bar for an unshielded surface wafer
# (09-02-NEUTRON-DECLARATION.md Section 4).  Asking for it RAISES
# (fp-indoor-band-as-central).  NOT applied, under any name: shield attenuation,
# post-shield fluence, overburden, buildup factor (all NOT applied), veto credit
# and multiplicity credit -- veto credit is exactly 1.0 by construction
# (fp-shielded-quantity-leak).
#
# ============================== ACCURACY LABEL ===============================
# ACCURACY_LABEL = order_of_magnitude, inherited at the point of definition from
# 09-02-NEUTRON-DECLARATION.md Section 3.4.  The ONLY independent cross-check the
# input flux owns is a SINGLE >10 MeV integral agreeing to -8.77% untuned; nothing
# validates its eV-keV differential shape, which is exactly the band that sets the
# in-RoI Ge recoil rate.  The label is a consequence of that evidence, not a
# formality (fp-precision-inflation).

from __future__ import annotations

import functools
import os
import re
from dataclasses import dataclass

import numpy as np

from . import parma_neutron_flux as parma

#: Accuracy class of every quantity this module emits.
ACCURACY_LABEL = "order_of_magnitude"

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))

ELASTIC_TABLE_PATH = os.path.join(REPO_ROOT, "data", "endf_nGe_elastic_v1.1.csv")
PER_ISOTOPE_PATH = os.path.join(REPO_ROOT, "data", "endf",
                                "nGe_elastic_per_isotope.csv")
FLUX_V11_PATH = os.path.join(REPO_ROOT, "data", "ambient_neutron_flux_v1.1.csv")
FLUX_THERMAL_PATH = os.path.join(REPO_ROOT, "data",
                                 "ambient_neutron_thermal_v2.0.csv")

# --------------------------------------------------------------------------- #
# Named unit conversions.  No unexplained numerical constant appears anywhere    #
# else in this module (test-dimensions).                                        #
# --------------------------------------------------------------------------- #
BARN_TO_CM2 = 1.0e-24          # 1 barn = 1e-24 cm^2
EV_PER_MEV = 1.0e6             # phi is emitted per MeV; the fold works in eV
EV_PER_KEV = 1.0e3             # rate per eV -> rate per keV
SECONDS_PER_DAY = 86400.0      # rate per second -> rate per day

# --------------------------------------------------------------------------- #
# Region of interest (GPD/PROJECT.md: "the 10-100 eV RoI and below")            #
# --------------------------------------------------------------------------- #
ROI_LO_eV = 10.0
ROI_HI_eV = 100.0

# --------------------------------------------------------------------------- #
# Sub-5 eV kernel disposition (ROADMAP Phase 13 SC5, first half)                #
# --------------------------------------------------------------------------- #
#: The seam energy the ROADMAP names.  Below it the ENDF FREE-ATOM sigma_el is
#: not the bound-crystal cross section and is never used as physics.
SUB5EV_SEAM_eV = 5.0

#: The declared route.  "ncrystal_splice" or "truncate"; "free_gas" is FORBIDDEN
#: as physics and exists only as the tripwire the guard protects against.
SUB5EV_ROUTES = ("ncrystal_splice", "truncate", "free_gas")
SUB5EV_ROUTE_DECLARED = "ncrystal_splice"

#: NCrystal material id and temperature for the bound-atom kernel.  293.6 K is
#: chosen to MATCH the frozen ENDF set's own processing temperature so that the
#: measured seam step is a free-vs-bound step and not a temperature step.
NCRYSTAL_CFG = "Ge_sg227.ncmat;temp=293.6K"

#: Instrumentation for test-no-freegas-below-5ev.  Incremented whenever the raw
#: ENDF free-atom table is evaluated below SUB5EV_SEAM_eV, by ANY caller.
_FREE_ATOM_BELOW_SEAM_EVALUATIONS = 0


class FluxColumnError(ValueError):
    """Raised when a caller asks for a flux column that is not operative here."""


class SubEvRouteError(ValueError):
    """Raised when the forbidden free-atom route is requested as physics."""


# --------------------------------------------------------------------------- #
# Frozen-artifact parsing.  Every number below is READ, never transcribed.      #
# --------------------------------------------------------------------------- #
def _header_lines(path: str) -> list[str]:
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("#"):
                break
            out.append(line.rstrip("\n"))
    return out


def _numeric_rows(path: str, ncol: int | None = None) -> np.ndarray:
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            toks = line.strip().split(",")
            if ncol is not None:
                toks = toks[:ncol]
            try:
                rows.append([float(t) for t in toks])
            except ValueError:
                continue  # column-name header row
    return np.asarray(rows, dtype=float)


@dataclass(frozen=True)
class ElasticHeader:
    """Everything this module needs from the frozen elastic table's own header."""
    f_natural: float                    # T_max/E_n, abundance weighted
    f_per_isotope: dict                 # {70: 0.0555, ...}
    abundances: dict                    # IUPAC, {70: 0.2057, ...}
    n_ge_per_cm3: float                 # atoms/cm^3
    rho_g_cm3: float
    molar_mass_g_mol: float
    validity_lo_eV: float
    resonance_peak_b: float
    resonance_peak_E_eV: float
    mesh_convergence_pct: float         # max over isotopes, 0.1 keV - 1 MeV
    doppler_sensitivity_pct: float      # 0.1 keV - 1 MeV
    ace_vs_mf3_pct: float               # max
    ace_temperature_K: float
    git_sha: str


@functools.lru_cache(maxsize=4)
def elastic_header(path: str = ELASTIC_TABLE_PATH) -> ElasticHeader:
    """Parse the frozen elastic table's provenance header (fp-quote-from-prose)."""
    h = "\n".join(_header_lines(path))

    m = re.search(r"T_max/E_n natural \(abundance-weighted, AS COMPUTED\) = "
                  r"([0-9.eE+-]+)", h)
    if m is None:
        raise ValueError(f"{path}: no natural T_max/E_n line in the header")
    f_nat = float(m.group(1))

    m = re.search(r"T_max/E_n per isotope[^:]*:\s*(.+)", h)
    f_iso = {int(a): float(v) for a, v in re.findall(r"(\d+)Ge=([0-9.eE+-]+)",
                                                     m.group(1))}
    m = re.search(r"abundances_IUPAC\s*=\s*(.+)", h)
    ab = {int(a): float(v) for a, v in re.findall(r"(\d+)Ge=([0-9.eE+-]+)",
                                                  m.group(1))}
    m = re.search(r"N_Ge\s*=\s*([0-9.eE+-]+) atoms/cm\^3 \(rho=([0-9.eE+-]+) "
                  r"g/cm\^3, M=([0-9.eE+-]+) g/mol\)", h)
    n_cm3, rho, molar = float(m.group(1)), float(m.group(2)), float(m.group(3))

    m = re.search(r"sigma_el natural VALID from ([0-9.eE+-]+) eV upward", h)
    lo = float(m.group(1))
    m = re.search(r"resonance-band peak \(0\.1keV-1MeV\) = ([0-9.eE+-]+) b at "
                  r"E=([0-9.eE+-]+) eV", h)
    peak_b, peak_e = float(m.group(1)), float(m.group(2))

    m = re.search(r"->\s*max ([0-9.eE+-]+)% \(PASS if", h)
    mesh = float(m.group(1))
    m = re.search(r"Doppler sensitivity[^:]*:\s*0\.1keV-1MeV=([0-9.eE+-]+)%", h)
    dopp = float(m.group(1))
    ace = max(float(v) for v in re.findall(r"max=([0-9.eE+-]+)%", h))
    m = re.search(r"ace_temperature\s*=\s*([0-9.eE+-]+) K", h)
    temp = float(m.group(1))
    m = re.search(r"git_sha\s*=\s*(\S+)", h)
    sha = m.group(1)

    return ElasticHeader(f_nat, f_iso, ab, n_cm3, rho, molar, lo, peak_b, peak_e,
                         mesh, dopp, ace, temp, sha)


@functools.lru_cache(maxsize=4)
def elastic_table(path: str = ELASTIC_TABLE_PATH) -> tuple:
    """(E_eV, sigma_el_natural_b, a1_natural) on the frozen 23,155-point union grid."""
    a = _numeric_rows(path)
    if not np.all(np.diff(a[:, 0]) > 0):
        raise ValueError(f"{path}: energy column is not strictly increasing")
    return a[:, 0].copy(), a[:, 1].copy(), a[:, 2].copy()


@functools.lru_cache(maxsize=4)
def per_isotope_table(path: str = PER_ISOTOPE_PATH) -> tuple:
    """(E_eV, {A: sigma_b}, {A: a1}) from the per-isotope frozen table."""
    a = _numeric_rows(path)
    hdr = "\n".join(_header_lines(path))
    order = [int(x) for x in re.findall(r"(\d+)Ge=MAT", hdr)]
    E = a[:, 0]
    sig = {A: a[:, 1 + i].copy() for i, A in enumerate(order)}
    a1 = {A: a[:, 1 + len(order) + i].copy() for i, A in enumerate(order)}
    return E.copy(), sig, a1


def kinematic_factor(mass_number: float) -> float:
    """f = T_max/E_n = 4A/(1+A)^2 for s-wave elastic scattering off mass number A."""
    A = float(mass_number)
    return 4.0 * A / (1.0 + A) ** 2


def f_natural() -> float:
    """The abundance-weighted natural-Ge kinematic factor, from the frozen header."""
    return elastic_header().f_natural


def n_ge_per_kg() -> float:
    """Ge atoms per kg, DERIVED from the frozen table's own N_Ge and rho.

    N_Ge [atoms/cm^3] / rho [g/cm^3] * 1000 [g/kg].  CONVENTIONS.md Section D
    quotes 8.29e24 atoms/kg from 1000 g / 72.63 g/mol * N_A; the two agree to
    better than 0.05%, and the frozen-artifact value is the one used.
    """
    h = elastic_header()
    return h.n_ge_per_cm3 / h.rho_g_cm3 * 1.0e3


def endf_ceiling_eV() -> float:
    """The top of the frozen elastic table -- the 20 MeV ENDF/B-VIII.0 ceiling."""
    return float(elastic_table()[0][-1])


def free_atom_tripwire_b() -> float:
    """Peak of the ENDF free-atom 1/v upturn below the seam.

    This is the value the sub-5 eV guard protects against: the free-atom elastic
    cross section climbs as the target-motion (free-gas) treatment takes over, and
    using it as physics below 5 eV would manufacture sub-eV recoil rate out of a
    data-format artefact (fp-free-gas-below-5ev).
    """
    E, s, _ = elastic_table()
    return float(s[E < SUB5EV_SEAM_eV].max())


# --------------------------------------------------------------------------- #
# Flux -- the operative OUTDOOR column, evaluated by the pinned PARMA driver     #
# --------------------------------------------------------------------------- #
OPERATIVE_FLUX_COLUMN = "phi_default"

_REFUSED_FLUX_COLUMNS = {          # every name here is REFUSED, never used
    "phi_lo", "phi_lo_cm2_s_mev",  # _REFUSED: the INDOOR leg
    "indoor", "midpoint", "band_midpoint",
    "phi_mid", "phi_band_midpoint", "geometric_mean",
}


def neutron_flux_cm2_s_MeV(E_n_eV, *, column: str = OPERATIVE_FLUX_COLUMN,
                           k: float = parma.K_GORDON_ANCHOR) -> np.ndarray:
    """dPhi/dE_n [cm^-2 s^-1 MeV^-1] at INCIDENT NEUTRON energies ``E_n_eV`` [eV].

    Evaluated by the pinned PARMA driver DIRECTLY -- not by interpolating either
    committed table.  That is what closes the 1 eV - 10.14 eV gap the two committed
    tables leave open, and it is why no interpolation or extrapolation of either
    table ever spans that gap (claim-flux-continuity).

    ``column`` is selected BY NAME.  ``phi_lo`` and any band midpoint RAISE: they
    are the INDOOR configuration leg, not an error bar for an unshielded surface
    wafer, and adopting one would cut this background by a factor 5
    (fp-indoor-band-as-central).
    """
    c = str(column).strip().lower()
    if c in _REFUSED_FLUX_COLUMNS:
        raise FluxColumnError(
            f"{column!r} is NOT selectable in this channel. phi_lo = phi_default/5 "
            "is the INDOOR leg (09-02-NEUTRON-DECLARATION.md Section 4), a "
            "configuration question and not an uncertainty. This wafer is an "
            "UNSHIELDED OUTDOOR surface detector; the operative column is "
            f"{OPERATIVE_FLUX_COLUMN!r} == phi_hi. phi_lo is REFUSED; using it, "
            "or the band midpoint, would cut this background fivefold "
            "(fp-indoor-band-as-central).")
    if c not in ("phi_default", "phi_hi", "outdoor"):
        raise FluxColumnError(
            f"unknown flux column {column!r}; the operative column is "
            f"{OPERATIVE_FLUX_COLUMN!r} (== phi_hi, outdoor).")
    E = np.atleast_1d(np.asarray(E_n_eV, dtype=float))
    return parma.differential_flux(E / EV_PER_MEV, k=k).phi_cm2_s_mev


# --------------------------------------------------------------------------- #
# Cross section, with the sub-5 eV disposition applied                          #
# --------------------------------------------------------------------------- #
def _sigma_endf_natural_b(E_eV: np.ndarray) -> np.ndarray:
    """Raw ENDF/B-VIII.0 + Lib80x natural sigma_el [barn], INSTRUMENTED.

    Linear interpolation on the frozen union grid, matching NJOY's own lin-lin
    linearisation to err=1e-3.  Every evaluation below the seam is COUNTED so that
    test-no-freegas-below-5ev can assert zero of them by execution rather than by
    inspection.
    """
    global _FREE_ATOM_BELOW_SEAM_EVALUATIONS
    E = np.asarray(E_eV, dtype=float)
    n_below = int(np.count_nonzero(E < SUB5EV_SEAM_eV))
    if n_below:
        _FREE_ATOM_BELOW_SEAM_EVALUATIONS += n_below
    Et, st, _ = elastic_table()
    return np.interp(E, Et, st)


def free_atom_below_seam_evaluations() -> int:
    """How many times the raw ENDF free-atom table has been evaluated below 5 eV."""
    return _FREE_ATOM_BELOW_SEAM_EVALUATIONS


def reset_free_atom_counter() -> None:
    global _FREE_ATOM_BELOW_SEAM_EVALUATIONS
    _FREE_ATOM_BELOW_SEAM_EVALUATIONS = 0


@functools.lru_cache(maxsize=2)
def _ncrystal_material(cfg: str = NCRYSTAL_CFG):
    import NCrystal
    return NCrystal.load(cfg)


def sigma_ncrystal_bound_b(E_eV) -> np.ndarray:
    """NCrystal ``Ge_sg227`` BOUND-ATOM scattering cross section [barn/atom].

    Used only below the 5 eV seam.  No Ge thermal scattering law exists in
    ENDF/B-VIII.0, so below the seam the free-atom evaluation is not the
    bound-crystal cross section (ROADMAP Phase 13 SC5).

    CONVENTIONS.md Section J bounds what this may claim: the crystal-coherent
    regime lies below ~21 meV, entirely under the 0.0999350 eV grid floor, so on
    this axis the bound kernel is used only in its high-energy (free-atom-limit)
    tail.  The rate is NEVER multiplied by exp(-2W).
    """
    E = np.atleast_1d(np.asarray(E_eV, dtype=float))
    return np.asarray(_ncrystal_material().scatter.xsect(ekin=E), dtype=float)


def sigma_for_fold_b(E_eV, *, route: str = SUB5EV_ROUTE_DECLARED) -> np.ndarray:
    """sigma_el [barn] under the declared sub-5 eV disposition route.

    ``ncrystal_splice`` : ENDF above 5 eV, NCrystal Ge_sg227 below.
    ``truncate``        : ENDF above 5 eV, EXACTLY ZERO below (the contribution is
                          dropped and the omission bounded, Phase-7 gap-D1 pattern).
    ``free_gas``        : FORBIDDEN as physics; available only as an explicitly
                          named diagnostic so the stake of the guard can be
                          measured (fp-free-gas-below-5ev).
    """
    if route not in SUB5EV_ROUTES:
        raise SubEvRouteError(f"unknown sub-5 eV route {route!r}; "
                              f"choose one of {SUB5EV_ROUTES}")
    E = np.atleast_1d(np.asarray(E_eV, dtype=float))
    out = np.zeros_like(E)
    hi = E >= SUB5EV_SEAM_eV
    if hi.any():
        out[hi] = _sigma_endf_natural_b(E[hi])
    lo = ~hi
    if lo.any():
        if route == "ncrystal_splice":
            out[lo] = sigma_ncrystal_bound_b(E[lo])
        elif route == "truncate":
            out[lo] = 0.0
        else:  # free_gas -- diagnostic only
            out[lo] = _sigma_endf_natural_b(E[lo])
    return out


def seam_discontinuity() -> dict:
    """The measured sigma step at the 5 eV seam (Route A's reported number)."""
    endf = float(_sigma_endf_natural_b(np.array([SUB5EV_SEAM_eV]))[0])
    nc = float(sigma_ncrystal_bound_b([SUB5EV_SEAM_eV])[0])
    return {"seam_eV": SUB5EV_SEAM_eV, "sigma_endf_free_atom_b": endf,
            "sigma_ncrystal_bound_b": nc,
            "relative_step": (nc - endf) / endf}


# --------------------------------------------------------------------------- #
# Quadrature -- exact for a piecewise power law, anchored at E_min(T)           #
# --------------------------------------------------------------------------- #
def loglog_segment_integrals(x, y) -> np.ndarray:
    """INT y dx over each segment, with y a power law in x between the nodes.

    On a segment with positive endpoints, y = A x^p and
        INT_{x1}^{x2} A x^p dx = (y2 x2 - y1 x1) / (p + 1),
    with the p -> -1 limit y1 x1 ln(x2/x1).  Written in that form rather than as
    A (x2^{p+1} - x1^{p+1})/(p+1) because it never forms A = y1 x1^{-p}, which
    under/overflows for the large |p| a resonance edge produces.

    EXACT for the 1/E^2 epithermal integrand, which is why the closed-form oracle
    is reproduced to roundoff rather than to a quadrature tolerance.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    x1, x2, y1, y2 = x[:-1], x[1:], y[:-1], y[1:]
    out = np.zeros(x1.size, dtype=float)
    good = (y1 > 0.0) & (y2 > 0.0) & (x2 > x1)
    p = np.zeros_like(out)
    with np.errstate(divide="ignore", invalid="ignore"):
        p[good] = np.log(y2[good] / y1[good]) / np.log(x2[good] / x1[good])
    near = good & (np.abs(p + 1.0) < 1.0e-9)
    pw = good & ~near
    out[pw] = (y2[pw] * x2[pw] - y1[pw] * x1[pw]) / (p[pw] + 1.0)
    out[near] = y1[near] * x1[near] * np.log(x2[near] / x1[near])
    # Non-positive endpoints (the truncate route zeroes sigma below the seam):
    # a power law cannot represent them; the trapezoid is the honest fallback.
    lin = (~good) & (x2 > x1)
    out[lin] = 0.5 * (y1[lin] + y2[lin]) * (x2[lin] - x1[lin])
    return out


def _suffix_integral(x, y) -> np.ndarray:
    """S[i] = INT_{x[i]}^{x[-1]} y dx, so an anchored fold is one array lookup."""
    seg = loglog_segment_integrals(x, y)
    return np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])


def quadrature_nodes(e_lo_eV: float, e_top_eV: float, *, per_decade: int = 200,
                     anchors=()) -> np.ndarray:
    """The E_n quadrature node set.

    Union of
      * every frozen-table union-grid point inside [e_lo, e_top] -- so the fold
        never averages across the resonance structure it exists to resolve;
      * a supplemental log grid at ``per_decade`` nodes/decade;
      * the explicit ``anchors``, which carry every E_min(T) = T/f and the 5 eV
        seam.  E_min(T) is therefore an EXACT node for every T
        (fp-unanchored-quadrature).
    """
    Et, _, _ = elastic_table()
    n_sup = int(round(np.log10(e_top_eV / e_lo_eV) * per_decade)) + 1
    nodes = np.concatenate([
        Et[(Et >= e_lo_eV) & (Et <= e_top_eV)],
        np.asarray(anchors, dtype=float).ravel(),
        np.logspace(np.log10(e_lo_eV), np.log10(e_top_eV), n_sup),
        [e_lo_eV, e_top_eV],
    ])
    nodes = np.unique(nodes)
    return nodes[(nodes >= e_lo_eV) & (nodes <= e_top_eV)]


# --------------------------------------------------------------------------- #
# The fold                                                                      #
# --------------------------------------------------------------------------- #
def E_min_eV(T_eV, f: float | None = None) -> np.ndarray:
    """The lowest incident neutron energy that can produce recoil T: E_min = T/f."""
    if f is None:
        f = f_natural()
    return np.asarray(T_eV, dtype=float) / float(f)


def fold_dRdT(
    T_eV,
    *,
    f: float | None = None,
    route: str = SUB5EV_ROUTE_DECLARED,
    per_decade: int = 200,
    e_top_eV: float | None = None,
    sigma_b_fn=None,
    flux_fn=None,
    n_per_kg: float | None = None,
    flux_column: str = OPERATIVE_FLUX_COLUMN,
    anchored: bool = True,
    include_union_nodes: bool = True,
    return_detail: bool = False,
):
    """dR/dT [counts/kg/day/keV] on the native recoil axis ``T_eV`` [eV].

    dR/dT(T) = N_Ge INT_{E_min(T)}^{E_top} phi(E_n) sigma_el(E_n) / (f E_n) dE_n

    DIMENSIONS (test-dimensions):
        N_Ge      [kg^-1]
        phi       [cm^-2 s^-1 MeV^-1]  -> /EV_PER_MEV -> [cm^-2 s^-1 eV^-1]
        sigma_el  [barn] -> x BARN_TO_CM2 -> [cm^2]
        1/(f E_n) [eV^-1]
        dE_n      [eV]
      product      [kg^-1 s^-1 eV^-1]
        x SECONDS_PER_DAY  -> [kg^-1 day^-1 eV^-1]
        x EV_PER_KEV       -> [counts kg^-1 day^-1 keV^-1]

    ``anchored=False`` reproduces the forbidden proxy fp-unanchored-quadrature:
    the lower limit is snapped UP to the first grid node above E_min(T), so the
    endpoint segment carrying the 1/E^2 spike is silently dropped.  It exists to
    put a NUMBER on what that proxy costs, and is never used for a deliverable.

    ``include_union_nodes=False`` additionally drops the resonance-resolved union
    grid, giving the full "plain log-substituted grid" version of the same proxy.
    """
    if f is None:
        f = f_natural()
    f = float(f)
    if n_per_kg is None:
        n_per_kg = n_ge_per_kg()
    if e_top_eV is None:
        e_top_eV = endf_ceiling_eV()

    T = np.atleast_1d(np.asarray(T_eV, dtype=float))
    if np.any(T <= 0):
        raise ValueError("recoil energies must be strictly positive")
    Emin = T / f
    if np.any(Emin > e_top_eV):
        raise ValueError(
            f"recoil T up to {T.max():.6g} eV needs incident neutrons up to "
            f"{Emin.max():.6g} eV, above the frozen table's {e_top_eV:.6g} eV "
            "ceiling. sigma_el is NOT extrapolated above it "
            "(fp-extrapolate-above-20mev).")

    e_lo = float(Emin.min())
    if route == "truncate":
        # sigma is EXACTLY ZERO below the seam, so the lower limit is lifted to the
        # seam.  The NODE SET is deliberately left unchanged, so the truncate and
        # splice routes are bit-identical wherever E_min(T) >= the seam and the
        # measured omission is physics rather than a quadrature-grid difference.
        Emin = np.maximum(Emin, SUB5EV_SEAM_eV)

    anchors = np.concatenate([Emin, [SUB5EV_SEAM_eV]])
    if include_union_nodes:
        nodes = quadrature_nodes(e_lo, e_top_eV, per_decade=per_decade,
                                 anchors=anchors if anchored else ())
    else:
        n_sup = int(round(np.log10(e_top_eV / e_lo) * per_decade)) + 1
        nodes = np.logspace(np.log10(e_lo), np.log10(e_top_eV), n_sup)
        if anchored:
            nodes = np.unique(np.concatenate([nodes, anchors]))
            nodes = nodes[(nodes >= e_lo) & (nodes <= e_top_eV)]

    if flux_fn is None:
        phi_per_MeV = neutron_flux_cm2_s_MeV(nodes, column=flux_column)
    else:
        phi_per_MeV = np.asarray(flux_fn(nodes), dtype=float)
    if sigma_b_fn is None:
        sigma_b = sigma_for_fold_b(nodes, route=route)
    else:
        sigma_b = np.asarray(sigma_b_fn(nodes), dtype=float)

    integrand = (phi_per_MeV / EV_PER_MEV) * (sigma_b * BARN_TO_CM2) / (f * nodes)
    suffix = _suffix_integral(nodes, integrand)

    # ``side="left"``: with anchoring E_min IS a node and this returns its own
    # index; without anchoring it returns the first node ABOVE E_min, so the
    # endpoint segment carrying the 1/E^2 spike is dropped -- which is precisely
    # the cost fp-unanchored-quadrature names.
    idx = np.searchsorted(nodes, Emin, side="left")
    idx = np.clip(idx, 0, nodes.size)
    dRdT = n_per_kg * suffix[idx] * SECONDS_PER_DAY * EV_PER_KEV

    if not return_detail:
        return dRdT
    return {
        "T_eV": T, "dRdT": dRdT, "f": f, "route": route,
        "e_lo_eV": e_lo, "e_top_eV": e_top_eV, "per_decade": per_decade,
        "nodes_eV": nodes, "integrand": integrand, "n_per_kg": n_per_kg,
        "anchored": bool(anchored), "flux_column": flux_column,
        "accuracy_label": ACCURACY_LABEL,
    }


# --------------------------------------------------------------------------- #
# The closed-form epithermal oracle                                             #
# --------------------------------------------------------------------------- #
def epithermal_oracle_dRdT(T_eV, *, C_cm2_s: float, sigma_b: float,
                           n_per_kg: float | None = None) -> np.ndarray:
    """Closed form for phi(E) = C/E and constant sigma:  dR/dT = N sigma C / T.

    DERIVATION (re-derived here, not quoted):
        INT_{T/f}^{inf} (C/E) * sigma/(f E) dE
            = (C sigma / f) INT_{T/f}^{inf} E^{-2} dE
            = (C sigma / f) * (f / T)
            = C sigma / T
    The kinematic factor f cancels EXACTLY.  That cancellation is the analytic
    backbone of the Plan 13-02 SC4 adjudication: in the pure epithermal limit the
    kinematic factor has NO effect on dR/dT at all.
    """
    if n_per_kg is None:
        n_per_kg = n_ge_per_kg()
    T = np.atleast_1d(np.asarray(T_eV, dtype=float))
    per_eV_per_s = n_per_kg * sigma_b * BARN_TO_CM2 * C_cm2_s / T
    return per_eV_per_s * SECONDS_PER_DAY * EV_PER_KEV


def fold_synthetic_epithermal(T_eV, *, f: float, C_cm2_s: float, sigma_b: float,
                              e_top_eV: float = 1.0e12, per_decade: int = 200,
                              n_per_kg: float | None = None) -> np.ndarray:
    """Drive the SAME quadrature with phi = C/E and constant sigma.

    ``e_top_eV`` defaults to 1e12 eV so the finite-top truncation term
    T/(f E_top) -- which is the only f-dependence the oracle can have -- sits below
    1e-7 for every T on the tested axis.
    """
    if n_per_kg is None:
        n_per_kg = n_ge_per_kg()
    T = np.atleast_1d(np.asarray(T_eV, dtype=float))
    Emin = T / float(f)
    e_lo = float(Emin.min())
    n_sup = int(round(np.log10(e_top_eV / e_lo) * per_decade)) + 1
    nodes = np.unique(np.concatenate([
        Emin, np.logspace(np.log10(e_lo), np.log10(e_top_eV), n_sup),
        [e_lo, e_top_eV]]))
    nodes = nodes[(nodes >= e_lo) & (nodes <= e_top_eV)]
    phi_per_eV = C_cm2_s / nodes
    integrand = phi_per_eV * (sigma_b * BARN_TO_CM2) / (float(f) * nodes)
    suffix = _suffix_integral(nodes, integrand)
    idx = np.searchsorted(nodes, Emin, side="left")
    return n_per_kg * suffix[idx] * SECONDS_PER_DAY * EV_PER_KEV


# --------------------------------------------------------------------------- #
# The native recoil axis                                                        #
# --------------------------------------------------------------------------- #
#: Phase-10 extended-grid floor.  The native recoil axis's bottom bin EDGE sits
#: exactly here, so ``ia_broadening.native_edges`` reproduces it and the Phase-12
#: floor-coverage assertion passes on the EDGE rather than on the first knot.
EXT_GRID_FLOOR_eV = 0.0999350

#: Bins per decade of the native recoil axis.  The 102.59 eV resonance is ~1.4%
#: wide in E_n, hence ~1.4% wide in T; 400 bins/decade is 0.577% per bin, so the
#: kinematic edge is resolved by ~2.5 bins rather than falling inside one.
NATIVE_BINS_PER_DECADE = 400


def native_recoil_axis(*, floor_eV: float = EXT_GRID_FLOOR_eV,
                       bins_per_decade: int = NATIVE_BINS_PER_DECADE,
                       f: float | None = None,
                       e_top_eV: float | None = None) -> tuple:
    """(edges_eV, centres_eV) of the native recoil axis.

    Log bins from ``floor_eV`` to the kinematic top T_max = f * E_top, knots at the
    geometric bin centres -- the Phase-12 construction, so the bottom bin EDGE is
    exactly the extended-grid floor.
    """
    if f is None:
        f = f_natural()
    if e_top_eV is None:
        e_top_eV = endf_ceiling_eV()
    top = float(f) * float(e_top_eV)
    nb = int(round(np.log10(top / floor_eV) * bins_per_decade))
    edges = np.logspace(np.log10(floor_eV), np.log10(top), nb + 1)
    return edges, np.sqrt(edges[:-1] * edges[1:])


# --------------------------------------------------------------------------- #
# Resonance imprint (ROADMAP SC3)                                               #
# --------------------------------------------------------------------------- #
#: Lethargy width of the Gaussian used to build the smoothed-sigma CONTROL.  It is
#: wide enough to erase the resolved resonance structure while a normalised
#: convolution of sigma*E in ln E conserves INT sigma dE.
CONTROL_SMOOTHING_SIGMA_LNE = 0.35

#: The imprint band: below the kinematic edge of the 102.59 eV resonance.
IMPRINT_BAND_LO_eV = 1.0
IMPRINT_BAND_HI_eV = 5.6

#: Imprint threshold, declared BEFORE the statistic is evaluated.  The statistic is
#: the excess of the steepest local log-log slope over the band's own median slope.
#: In the pure epithermal limit dR/dT ~ 1/T and the slope is exactly -1 everywhere,
#: so the excursion is 0; a smoothly varying flux or cross section moves the slope
#: smoothly and keeps the excursion of order unity.  An excursion above 5 decades
#: per decade means the spectrum loses a finite fraction of its integrand within a
#: fraction of a decade -- which only a RESOLVED narrow feature can do.
IMPRINT_EXCURSION_THRESHOLD = 5.0


def smoothed_sigma_b(*, sigma_lnE: float = CONTROL_SMOOTHING_SIGMA_LNE,
                     n_uniform: int = 400_000) -> np.ndarray:
    """A resonance-integral-preserving SMOOTHED sigma_el on the frozen union grid.

    The convolution is applied to sigma*E in ln E with a normalised Gaussian, so
    INT sigma dE = INT (sigma E) d(ln E) is preserved by construction up to edge
    effects; the residual is measured by ``control_resonance_integral_check``.
    """
    E, s, _ = elastic_table()
    lnE = np.log(E)
    y = s * E
    u = np.linspace(lnE[0], lnE[-1], int(n_uniform))
    du = u[1] - u[0]
    yu = np.interp(u, lnE, y)
    half = int(round(4.0 * sigma_lnE / du))
    x = np.arange(-half, half + 1) * du
    ker = np.exp(-0.5 * (x / sigma_lnE) ** 2)
    ker /= ker.sum()
    num = np.convolve(yu, ker, mode="same")
    den = np.convolve(np.ones_like(yu), ker, mode="same")
    return np.interp(lnE, u, num / den) / E


def control_resonance_integral_check(lo_eV: float = 100.0,
                                     hi_eV: float = 1.0e6, **kw) -> dict:
    """Relative change of INT sigma dE over the resonance band under smoothing."""
    E, s, _ = elastic_table()
    ss = smoothed_sigma_b(**kw)
    m = (E >= lo_eV) & (E <= hi_eV)
    ir = float(np.trapz(s[m], E[m]))
    isv = float(np.trapz(ss[m], E[m]))
    return {"band_lo_eV": lo_eV, "band_hi_eV": hi_eV,
            "resonance_integral_real_b_eV": ir,
            "resonance_integral_smoothed_b_eV": isv,
            "relative_change": (isv - ir) / ir}


def imprint_statistic(T_eV, dRdT, *, lo_eV: float = IMPRINT_BAND_LO_eV,
                      hi_eV: float = IMPRINT_BAND_HI_eV) -> dict:
    """Log-log slope EXCURSION of dR/dT in the imprint band.

    excursion = max |d ln(dR/dT) / d ln T| - median |d ln(dR/dT) / d ln T|

    Falsifiable by construction: a spectrum with no resolved structure has a
    slowly varying slope, so its max and median nearly coincide and the excursion
    collapses.  The smoothed-sigma control is what demonstrates that
    (test-imprint-rejects-smooth); a statistic both spectra pass would be replaced,
    not reinterpreted (fp-imprint-unfalsifiable).
    """
    T = np.asarray(T_eV, dtype=float)
    y = np.asarray(dRdT, dtype=float)
    if np.any(y <= 0):
        raise ValueError("imprint statistic needs a strictly positive spectrum")
    slope = np.gradient(np.log(y), np.log(T))
    a = np.abs(slope)
    m = (T >= lo_eV) & (T <= hi_eV)
    if m.sum() < 5:
        raise ValueError("imprint band contains too few points")
    i = int(np.argmax(a[m]))
    return {
        "excursion": float(a[m][i] - np.median(a[m])),
        "max_abs_slope": float(a[m][i]),
        "median_abs_slope": float(np.median(a[m])),
        "T_at_max_eV": float(T[m][i]),
        "band_lo_eV": lo_eV, "band_hi_eV": hi_eV,
        "threshold": IMPRINT_EXCURSION_THRESHOLD,
        "passes": bool(a[m][i] - np.median(a[m]) > IMPRINT_EXCURSION_THRESHOLD),
    }


def smoothed_sigma_fn(*, route: str = SUB5EV_ROUTE_DECLARED,
                      sigma_lnE: float = CONTROL_SMOOTHING_SIGMA_LNE):
    """A sigma callable for the CONTROL fold: smoothed above the seam, route below.

    The sub-5 eV disposition is held FIXED between the real spectrum and the
    control, so any difference between them can only come from the resolved
    resonance structure and not from the seam treatment.
    """
    E, _, _ = elastic_table()
    ss = smoothed_sigma_b(sigma_lnE=sigma_lnE)

    def _sigma(e):
        e = np.atleast_1d(np.asarray(e, dtype=float))
        out = np.zeros_like(e)
        hi = e >= SUB5EV_SEAM_eV
        out[hi] = np.interp(e[hi], E, ss)
        lo = ~hi
        if lo.any():
            if route == "ncrystal_splice":
                out[lo] = sigma_ncrystal_bound_b(e[lo])
            elif route == "truncate":
                out[lo] = 0.0
            else:
                out[lo] = _sigma_endf_natural_b(e[lo])
        return out

    return _sigma


def resonance_carrier() -> dict:
    """Which Ge isotope actually carries the 102.59 eV natural-Ge resonance.

    The natural peak is an ABUNDANCE-WEIGHTED sum; if one isotope carries it, the
    physically correct kinematic edge uses THAT isotope's own 4A/(1+A)^2, not the
    abundance-weighted natural f.  Measured, not assumed (test-edge-smearing).
    """
    h = elastic_header()
    E_iso, sig_iso, _ = per_isotope_table()
    j = int(np.argmin(np.abs(E_iso - h.resonance_peak_E_eV)))
    peaks = {A: float(s[j]) for A, s in sig_iso.items()}
    contrib = {A: peaks[A] * h.abundances[A] for A in peaks}
    carrier = max(contrib, key=contrib.get)
    tot = sum(contrib.values())
    f_iso = {A: kinematic_factor(A) for A in peaks}
    edges = {A: f_iso[A] * h.resonance_peak_E_eV for A in peaks}
    return {
        "E_res_eV": float(E_iso[j]),
        "natural_peak_b": float(tot),
        "natural_peak_b_header": h.resonance_peak_b,
        "per_isotope_sigma_b": peaks,
        "per_isotope_abundance_weighted_b": contrib,
        "carrier_A": carrier,
        "carrier_fraction_of_natural_peak": contrib[carrier] / tot,
        "f_per_isotope": f_iso,
        "f_per_isotope_header": h.f_per_isotope,
        "edge_per_isotope_eV": edges,
        "edge_carrier_eV": edges[carrier],
        "edge_natural_f_eV": h.f_natural * h.resonance_peak_E_eV,
        "edge_window_lo_eV": min(edges.values()),
        "edge_window_hi_eV": max(edges.values()),
    }


def per_isotope_edge_fold(T_eV, *, per_decade: int = 200,
                          route: str = SUB5EV_ROUTE_DECLARED) -> np.ndarray:
    """dR/dT from FIVE per-isotope flat boxes, each with its own f and sigma.

    The production fold uses ONE abundance-weighted f, which places every kinematic
    edge at f_nat * E_res rather than at the carrying isotope's own f * E_res.  This
    function is the cross-check that measures how far the single-f stand-in moves
    the edge, instead of asserting a +/-4% smearing band.
    """
    h = elastic_header()
    E_iso, sig_iso, _ = per_isotope_table()
    T = np.atleast_1d(np.asarray(T_eV, dtype=float))
    total = np.zeros_like(T)
    n_per_kg = n_ge_per_kg()
    for A, s_iso in sig_iso.items():
        f_A = kinematic_factor(A)
        w = h.abundances[A]

        def _sig(E, _s=s_iso, _E=E_iso):
            E = np.asarray(E, float)
            out = np.zeros_like(E)
            hi = E >= SUB5EV_SEAM_eV
            out[hi] = np.interp(E[hi], _E, _s)
            if route == "ncrystal_splice" and (~hi).any():
                out[~hi] = sigma_ncrystal_bound_b(E[~hi])
            return out

        total = total + w * fold_dRdT(T, f=f_A, route=route,
                                      per_decade=per_decade,
                                      sigma_b_fn=_sig, n_per_kg=n_per_kg)
    return total


# --------------------------------------------------------------------------- #
# Flux above the frozen table's ceiling -- the numerator Plan 13-02 needs        #
# --------------------------------------------------------------------------- #
#: The pinned PARMA driver's own upper reach.  The committed v1.1 flux table stops
#: at ~197 MeV; the driver does not.
DRIVER_TOP_eV = 1.0e10   # 10 GeV


def flux_above_ceiling(e_lo_eV: float | None = None,
                       e_hi_eV: float = DRIVER_TOP_eV,
                       *, per_decade: int = 200) -> dict:
    """Integral neutron flux above the frozen sigma_el ceiling, from the driver."""
    if e_lo_eV is None:
        e_lo_eV = endf_ceiling_eV()
    phi = parma.integral_flux(e_lo_eV / EV_PER_MEV, e_hi_eV / EV_PER_MEV,
                              per_decade=per_decade)
    return {"e_lo_eV": e_lo_eV, "e_hi_eV": e_hi_eV,
            "integral_flux_cm2_s": float(phi),
            "accuracy_label": ACCURACY_LABEL}


# --------------------------------------------------------------------------- #
# Diagnostics: anchor loss, sub-5 eV stake, forward peaking                      #
# --------------------------------------------------------------------------- #
def anchor_loss(T_eV, *, per_decade: int = 200, include_union_nodes: bool = True,
                **kw) -> dict:
    """Signed relative cost of NOT anchoring the quadrature at E_min(T).

    Returns ``(unanchored - anchored)/anchored`` as a function of T.  A run that
    reports ZERO everywhere FAILS the check: it would mean neither route resolved
    the endpoint spike, so the 1/E^2 behaviour was never present in the integrand
    and the fold is wrong upstream of the node placement.
    """
    T = np.atleast_1d(np.asarray(T_eV, dtype=float))
    a = fold_dRdT(T, per_decade=per_decade,
                  include_union_nodes=include_union_nodes, anchored=True, **kw)
    u = fold_dRdT(T, per_decade=per_decade,
                  include_union_nodes=include_union_nodes, anchored=False, **kw)
    with np.errstate(divide="ignore", invalid="ignore"):
        rel = np.where(a > 0, (u - a) / a, np.nan)
    return {"T_eV": T, "anchored": a, "unanchored": u, "relative": rel,
            "per_decade": per_decade,
            "include_union_nodes": bool(include_union_nodes)}


def band_integrated_rate(T_eV, dRdT, lo_eV: float, hi_eV: float) -> float:
    """INT dR/dT dT over [lo, hi] in counts/kg/day, via the same log-log rule."""
    T = np.asarray(T_eV, dtype=float)
    y = np.asarray(dRdT, dtype=float)
    m = (T >= lo_eV) & (T <= hi_eV)
    if m.sum() < 2:
        return 0.0
    # dR/dT is per keV while T is in eV, hence the eV -> keV conversion.
    return float(loglog_segment_integrals(T[m], y[m]).sum() / EV_PER_KEV)


def sub5ev_stake(T_eV=None, *, per_decade: int = 200) -> dict:
    """What the sub-5 eV disposition is worth, measured under all three routes.

    Incident neutrons below 5 eV produce recoils only below T = f * 5 eV, so their
    contribution to the 10-100 eV RoI is ZERO by kinematics, not by approximation.
    The number that actually matters for this milestone is the sub-eV band, which
    is reported alongside it.
    """
    if T_eV is None:
        _, T_eV = native_recoil_axis()
    T = np.asarray(T_eV, dtype=float)
    f = f_natural()
    t_edge = f * SUB5EV_SEAM_eV
    out = {"T_edge_eV": t_edge, "seam_eV": SUB5EV_SEAM_eV, "f": f,
           "free_atom_tripwire_b": free_atom_tripwire_b(),
           "seam_discontinuity": seam_discontinuity()}
    y = {r: fold_dRdT(T, route=r, per_decade=per_decade)
         for r in ("ncrystal_splice", "truncate", "free_gas")}
    bands = {"sub_edge": (float(T.min()), t_edge),
             "sub_eV": (float(T.min()), 1.0),
             "RoI": (ROI_LO_eV, ROI_HI_eV),
             "total": (float(T.min()), float(T.max()))}
    out["bands"] = {}
    for name, (lo, hi) in bands.items():
        i = {r: band_integrated_rate(T, y[r], lo, hi) for r in y}
        ref = i["ncrystal_splice"]
        out["bands"][name] = {
            "lo_eV": lo, "hi_eV": hi,
            "rate_ncrystal_splice": i["ncrystal_splice"],
            "rate_truncate": i["truncate"],
            "rate_free_gas": i["free_gas"],
            "truncate_omission_fraction": ((ref - i["truncate"]) / ref) if ref else 0.0,
            "free_gas_vs_ncrystal_fraction": ((i["free_gas"] - ref) / ref) if ref else 0.0,
        }
    out["bottom_bin"] = {
        "T_eV": float(T[0]),
        "dRdT_ncrystal_splice": float(y["ncrystal_splice"][0]),
        "dRdT_truncate": float(y["truncate"][0]),
        "dRdT_free_gas": float(y["free_gas"][0]),
        "truncate_omission_fraction": float(
            (y["ncrystal_splice"][0] - y["truncate"][0]) / y["ncrystal_splice"][0]),
        "free_gas_vs_ncrystal_fraction": float(
            (y["free_gas"][0] - y["ncrystal_splice"][0]) / y["ncrystal_splice"][0]),
    }
    return out


def forward_peaking_report(T_eV=(0.1, 10.0, 100.0, 1000.0, 1.0e5),
                           *, per_decade: int = 200) -> dict:
    """Contribution-weighted <a1> above E_min(T): how good the flat box is.

    a1 is the CM P1 Legendre coefficient carried in the frozen table's third
    column.  It is REPORTED, never applied (the flat box is the Phase-7 frozen
    kernel).  Forward peaking makes the true dsigma/dT fall toward the high-T end
    of each box, so where a1 is non-negligible the flat box OVERSTATES the high-T
    end -- a flatters/penalizes direction that depends on where T sits in the box.
    """
    f = f_natural()
    E, _, a1 = elastic_table()
    e_top = endf_ceiling_eV()
    out = {"note": "a1 is reported, not applied (frozen isotropic-CM flat box)",
           "rows": []}
    for T in np.atleast_1d(np.asarray(T_eV, dtype=float)):
        d = fold_dRdT([T], per_decade=per_decade, return_detail=True)
        nodes, integ = d["nodes_eV"], d["integrand"]
        sel = nodes >= T / f
        seg = loglog_segment_integrals(nodes[sel], integ[sel])
        a1n = np.interp(nodes[sel], E, a1)
        wa1 = float((seg * 0.5 * (a1n[:-1] + a1n[1:])).sum() / seg.sum())
        out["rows"].append({"T_eV": float(T), "E_min_eV": float(T / f),
                            "weighted_a1": wa1,
                            "max_a1_above_Emin": float(a1n.max())})
    out["global_max_a1"] = float(a1.max())
    out["global_max_a1_at_E_eV"] = float(E[int(np.argmax(a1))])
    return out


# --------------------------------------------------------------------------- #
# Flux continuity: the 1 eV - 10.14 eV gap the two committed tables leave open  #
# --------------------------------------------------------------------------- #
def read_flux_v11(path: str = FLUX_V11_PATH) -> dict:
    """The committed 584-bin v1.1 flux table (10.14 eV - 197 MeV).

    ``phi_lo`` is deliberately NOT returned: it is the INDOOR leg and this channel
    has no use for it (fp-indoor-band-as-central).
    """
    a = _numeric_rows(path, ncol=6)
    return {"E_lo_eV": a[:, 0] * EV_PER_KEV, "E_n_eV": a[:, 1] * EV_PER_KEV,
            "E_hi_eV": a[:, 2] * EV_PER_KEV, "phi_default": a[:, 3]}


def read_flux_thermal(path: str = FLUX_THERMAL_PATH) -> dict:
    """The committed 201-node sub-eV thermal flux table (0.01 eV - 1 eV)."""
    a = _numeric_rows(path, ncol=3)
    return {"E_n_eV": a[:, 0] * EV_PER_KEV, "phi_default": a[:, 1],
            "phi_native_untuned": a[:, 2]}


#: The uniform relative offset the joint-identity check of
#: 09-02-NEUTRON-DECLARATION.md Section 3.3 already identified and explained: the
#: committed v1.1 table was generated with the UNROUNDED anchor scalar 1.0961043
#: while the module carries the rounded 1.09610.  Any deviation pattern that is
#: NOT this offset is reported rather than smoothed over.
KNOWN_K_ROUNDING_OFFSET = 3.88e-06
FLUX_OVERLAP_MEDIAN_TOL = 0.01   # 09-02 Section 3.3 tolerances, reused unchanged
FLUX_OVERLAP_MAX_TOL = 0.05


def flux_overlap_check() -> dict:
    """Pinned driver vs BOTH committed tables, pointwise on their own nodes."""
    out = {}
    for name, rd in (("v1.1", read_flux_v11), ("thermal_v2.0", read_flux_thermal)):
        t = rd()
        drv = neutron_flux_cm2_s_MeV(t["E_n_eV"])
        rel = (drv - t["phi_default"]) / t["phi_default"]
        out[name] = {
            "n_points": int(rel.size),
            "E_lo_eV": float(t["E_n_eV"].min()), "E_hi_eV": float(t["E_n_eV"].max()),
            "median_rel": float(np.median(rel)),
            "max_abs_rel": float(np.abs(rel).max()),
            "n_gt_1pct": int(np.count_nonzero(np.abs(rel) > FLUX_OVERLAP_MEDIAN_TOL)),
            "n_gt_5pct": int(np.count_nonzero(np.abs(rel) > FLUX_OVERLAP_MAX_TOL)),
            "consistent_with_k_rounding": bool(
                np.abs(np.abs(np.median(rel)) - KNOWN_K_ROUNDING_OFFSET)
                < 0.2 * KNOWN_K_ROUNDING_OFFSET),
        }
    return out


def flux_gap() -> dict:
    """The uncovered band between the two committed tables, measured not assumed."""
    th = read_flux_thermal()
    v11 = read_flux_v11()
    f = f_natural()
    gap_lo = float(th["E_n_eV"].max())          # 1 eV, top thermal node
    gap_hi_edge = float(v11["E_lo_eV"].min())   # 10 eV, lowest v1.1 bin EDGE
    gap_hi_centre = float(v11["E_n_eV"].min())  # 10.145 eV, lowest v1.1 bin CENTRE
    return {
        "gap_lo_eV": gap_lo, "gap_hi_bin_edge_eV": gap_hi_edge,
        "gap_hi_bin_centre_eV": gap_hi_centre,
        "T_below_which_gap_contributes_eV": f * gap_hi_centre,
        "T_below_which_nothing_is_covered_eV": f * gap_lo,
        "f": f,
        "closed_by": ("pinned PARMA driver evaluated directly at every quadrature "
                      "node; neither committed table is interpolated or "
                      "extrapolated across the gap"),
    }


# --------------------------------------------------------------------------- #
# Artifact emission                                                             #
# --------------------------------------------------------------------------- #
ARTIFACT_DIR = os.path.join(REPO_ROOT, "artifacts", "v2.0")
DRDT_CSV = os.path.join(ARTIFACT_DIR, "neutron_dRdT_ge.csv")
FLUX_CONTINUITY_CSV = os.path.join(ARTIFACT_DIR, "neutron_flux_continuity.csv")


def _git_sha() -> str:
    import subprocess
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                              cwd=REPO_ROOT, capture_output=True, text=True,
                              check=True).stdout.strip()
    except Exception:
        return "unknown"


def _provenance_header(extra: list[str]) -> list[str]:
    h = elastic_header()
    return [
        "# QPD Phase-13 -- Ge NEUTRON ELASTIC nuclear-recoil channel.",
        f"# accuracy_label = {ACCURACY_LABEL}   <-- inherited at the point of "
        "definition from",
        "#   09-02-NEUTRON-DECLARATION.md Section 3.4. The ONLY independent",
        "#   cross-check the input flux owns is a SINGLE >10 MeV integral agreeing to",
        "#   -8.77% UNTUNED; nothing validates its eV-keV differential shape, which is",
        "#   exactly the band that sets this rate. No quantity here may be quoted to",
        "#   better than this label (fp-precision-inflation).",
        "#",
        "# AXIS TAG: E_n is INCIDENT NEUTRON KINETIC ENERGY; T is NUCLEAR RECOIL",
        "#   energy. A 1 MeV neutron does not deposit 1 MeV. Recoil axis is keV_nr on",
        "#   the unified phonon scale, NO Lindhard and NO quenching (CONVENTIONS B).",
        "#",
        "# flux_column = phi_default (outdoor, == phi_hi); phi_lo NOT USED.",
        "#   phi_lo = phi_default/5 is the INDOOR leg, a configuration question and not",
        "#   an error bar for an unshielded surface wafer (09-02 Section 4). Requesting",
        "#   it RAISES in neutron_recoil.neutron_flux_cm2_s_MeV.",
        "# NOT applied, under any name: shield attenuation, post-shield fluence,",
        "#   overburden, buildup factor -- all NOT applied. Veto credit and",
        "#   multiplicity credit are NOT applied; veto credit is exactly 1.0 by",
        "#   construction.",
        "#",
        f"# f = T_max/E_n = {h.f_natural} (natural Ge, abundance weighted)",
        "#   PROVENANCE: parsed from data/endf_nGe_elastic_v1.1.csv header line",
        "#   'T_max/E_n natural (abundance-weighted, AS COMPUTED) = "
        f"{h.f_natural}'. Not transcribed from prose (fp-quote-from-prose).",
        f"#   per isotope 4A/(1+A)^2: " + ", ".join(
            f"{A}Ge={v}" for A, v in sorted(h.f_per_isotope.items())),
        f"# N_Ge = {n_ge_per_kg():.6e} atoms/kg, DERIVED as "
        f"{h.n_ge_per_cm3:.6g} atoms/cm^3 / {h.rho_g_cm3:.6g} g/cm^3 x 1000 g/kg",
        "#   from the frozen table's own header (CONVENTIONS D quotes 8.29e24; agree",
        "#   to better than 0.05%).",
        f"# sigma_el source = ENDF/B-VIII.0 + LANL Lib80x, 23155-point union grid, "
        f"{h.ace_temperature_K} K,",
        f"#   validity {h.validity_lo_eV:.4g} eV -> {endf_ceiling_eV():.6g} eV; "
        f"resonance peak {h.resonance_peak_b} b at {h.resonance_peak_E_eV} eV.",
        f"#   frozen-table git_sha = {h.git_sha}",
        f"# truncation_energy_upper_eV = {endf_ceiling_eV():.6g}  (the ENDF ceiling; "
        "sigma_el is NEVER extrapolated above it)",
        f"# truncation_energy_lower_eV = {SUB5EV_SEAM_eV:.6g}  (the sub-5 eV seam)",
        "# flux source = pinned PARMA v4.10 / Sato 2015 driver, commit "
        f"{parma.PINNED_COMMIT},",
        f"#   anchor scalar k = {parma.K_GORDON_ANCHOR} applied uniformly "
        "(Gordon 2004 >10 MeV integral only).",
        "#   The driver is evaluated DIRECTLY at every quadrature node, which is how",
        "#   the 1 eV - 10.14 eV gap between the two committed flux tables is closed;",
        "#   neither committed table is interpolated or extrapolated across it.",
        f"# git_sha = {_git_sha()}",
    ] + extra


def write_flux_continuity_table(path: str = FLUX_CONTINUITY_CSV, *,
                                gap_nodes: int = 121) -> str:
    """Emit artifacts/v2.0/neutron_flux_continuity.csv.

    Three row kinds, tagged in the ``region`` column:
      overlap_thermal_v2.0 / overlap_v1.1 -- driver vs the committed table at that
        table's OWN nodes;
      gap -- the driver's own values across 1 eV - 10.14 eV, where neither
        committed table has any data at all.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    g = flux_gap()
    ov = flux_overlap_check()
    rows = []
    for name, rd in (("overlap_thermal_v2.0", read_flux_thermal),
                     ("overlap_v1.1", read_flux_v11)):
        t = rd()
        drv = neutron_flux_cm2_s_MeV(t["E_n_eV"])
        for e, d, c in zip(t["E_n_eV"], drv, t["phi_default"]):
            rows.append((name, e, d, c, (d - c) / c))
    gap_E = np.logspace(np.log10(g["gap_lo_eV"]),
                        np.log10(g["gap_hi_bin_centre_eV"]), gap_nodes)
    for e, d in zip(gap_E, neutron_flux_cm2_s_MeV(gap_E)):
        rows.append(("gap", e, d, float("nan"), float("nan")))

    hdr = _provenance_header([
        "#",
        "# ================= WHAT THIS TABLE IS ==============================",
        "# The two committed flux tables DO NOT JOIN. data/ambient_neutron_thermal_"
        f"v2.0.csv stops at {g['gap_lo_eV']:.6g} eV;",
        f"# data/ambient_neutron_flux_v1.1.csv starts at a {g['gap_hi_bin_edge_eV']:.6g}"
        f" eV bin EDGE (first bin centre {g['gap_hi_bin_centre_eV']:.9g} eV).",
        f"# Ge recoils below T = f x {g['gap_hi_bin_centre_eV']:.6g} eV = "
        f"{g['T_below_which_gap_contributes_eV']:.6g} eV are fed ENTIRELY from that",
        "# uncovered band -- exactly the sub-eV region this milestone exists to reach.",
        "# It is closed by evaluating the PINNED PARMA DRIVER DIRECTLY, with the same",
        "# anchor scalar k the committed tables carry. NO interpolation or",
        "# extrapolation of either committed table spans the gap.",
        "#",
        "# ================= DRIVER vs COMMITTED TABLES ======================",
        "# tolerances reused unchanged from 09-02-NEUTRON-DECLARATION.md Section 3.3:",
        f"#   median <= {FLUX_OVERLAP_MEDIAN_TOL:.0%}, max <= {FLUX_OVERLAP_MAX_TOL:.0%}",
    ] + [
        f"#   {k}: n={v['n_points']}, median={v['median_rel']:+.4e}, "
        f"max|.|={v['max_abs_rel']:.4e}, >1%={v['n_gt_1pct']}, >5%={v['n_gt_5pct']}, "
        f"k-rounding pattern={v['consistent_with_k_rounding']}"
        for k, v in ov.items()
    ] + [
        f"# The v1.1 offset is the KNOWN uniform {KNOWN_K_ROUNDING_OFFSET:.2e} anchor-"
        "scalar rounding",
        "#   (committed table built with the unrounded k=1.0961043; module carries",
        "#   k=1.09610). It is reported, not smoothed over. The thermal table was",
        "#   itself written by this driver, so its residual is CSV formatting only.",
        "#",
        "# units: E_n_eV [eV]; phi [cm^-2 s^-1 MeV^-1]; rel_dev dimensionless.",
        "# reproduce: PYTHONPATH=src /opt/anaconda3/bin/python3 -c \"from "
        "qpd_potential import neutron_recoil as n; n.write_flux_continuity_table()\"",
    ])
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(hdr) + "\n")
        fh.write("region,E_n_eV,phi_driver_cm2_s_MeV,phi_committed_table_cm2_s_MeV,"
                 "rel_dev_driver_minus_table,accuracy_label\n")
        for name, e, d, c, r in rows:
            cs = "" if np.isnan(c) else f"{c:.9e}"
            rs = "" if np.isnan(r) else f"{r:.6e}"
            fh.write(f"{name},{e:.10e},{d:.9e},{cs},{rs},{ACCURACY_LABEL}\n")
    return path


def write_dRdT_table(path: str = DRDT_CSV, *,
                     route: str = SUB5EV_ROUTE_DECLARED,
                     per_decade: int = 200,
                     bins_per_decade: int = NATIVE_BINS_PER_DECADE) -> str:
    """Emit artifacts/v2.0/neutron_dRdT_ge.csv -- the native-axis Ge neutron dR/dT."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    edges, T = native_recoil_axis(bins_per_decade=bins_per_decade)
    y = fold_dRdT(T, route=route, per_decade=per_decade)
    y_ctrl = fold_dRdT(T, route=route, per_decade=per_decade,
                       sigma_b_fn=smoothed_sigma_fn(route=route))
    y_trunc = fold_dRdT(T, route="truncate", per_decade=per_decade)
    seam = seam_discontinuity()
    imp = imprint_statistic(T, y)
    imp_c = imprint_statistic(T, y_ctrl)
    carrier = resonance_carrier()
    g = flux_gap()

    hdr = _provenance_header([
        "#",
        "# ==================== SUB-5 eV KERNEL DISPOSITION ==================",
        f"# sub5eV_disposition = {route}",
        "#   ROUTE A of the two ROADMAP SC5 routes: the NCrystal 4.4.6 Ge_sg227",
        f"#   BOUND-ATOM kernel below the {SUB5EV_SEAM_eV:.6g} eV seam, "
        f"{NCRYSTAL_CFG}.",
        f"#   MEASURED seam discontinuity at {seam['seam_eV']:.6g} eV: ENDF free-atom "
        f"{seam['sigma_endf_free_atom_b']:.6f} b vs",
        f"#   NCrystal bound {seam['sigma_ncrystal_bound_b']:.6f} b, step "
        f"{seam['relative_step']:+.4%}.",
        "#   The ENDF FREE-ATOM sigma_el is NEVER used as physics below the seam; its",
        f"#   1/v upturn reaches {free_atom_tripwire_b():.4f} b at the bottom of the",
        "#   table and using it there would manufacture sub-eV recoil rate out of a",
        "#   data-format artefact (fp-free-gas-below-5ev).",
        "#   WHY ROUTE A AND NOT TRUNCATION: truncation at the seam drops "
        f"{(1.0 - y_trunc[0] / y[0]):.1%} of the",
        f"#   bottom bin ({T[0]:.6g} eV) -- measured in-phase, not assumed.",
        "#",
        "# ==================== RESONANCE IMPRINT (SC3) ======================",
        f"# imprint statistic = max|dln(dR/dT)/dlnT| - median|...| over T in "
        f"[{imp['band_lo_eV']:.6g}, {imp['band_hi_eV']:.6g}] eV",
        f"#   threshold (declared before the run) = {imp['threshold']:.6g}",
        f"#   REAL spectrum   : {imp['excursion']:.4f} at T = {imp['T_at_max_eV']:.6g}"
        f" eV  -> {'PASS' if imp['passes'] else 'FAIL'}",
        "#   CONTROL (resonance-integral-preserving smoothed sigma_el): "
        f"{imp_c['excursion']:.4f} -> "
        f"{'PASS' if imp_c['passes'] else 'FAIL (as it must)'}",
        f"#   carrying isotope = {carrier['carrier_A']}Ge "
        f"({carrier['carrier_fraction_of_natural_peak']:.2%} of the natural peak at "
        f"{carrier['E_res_eV']:.6g} eV)",
        f"#   kinematic edge: carrier's own f gives {carrier['edge_carrier_eV']:.6g} eV;"
        f" the single natural f places it at {carrier['edge_natural_f_eV']:.6g} eV;",
        f"#   naive all-isotope window [{carrier['edge_window_lo_eV']:.6g}, "
        f"{carrier['edge_window_hi_eV']:.6g}] eV.",
        "#",
        "# ==================== FLUX CONTINUITY ==============================",
        f"# the 1 eV - {g['gap_hi_bin_centre_eV']:.6g} eV gap between the two committed",
        "#   flux tables is closed by the pinned PARMA driver evaluated directly at",
        "#   every quadrature node; see artifacts/v2.0/neutron_flux_continuity.csv.",
        f"#   Recoils below T = {g['T_below_which_gap_contributes_eV']:.6g} eV are fed",
        "#   partly from inside that gap.",
        "#",
        "# ==================== QUADRATURE ===================================",
        f"# E_min(T) = T/f is an EXACT quadrature node for every T; the "
        f"{len(elastic_table()[0])}-point",
        "#   resonance-resolved union grid is carried in as exact nodes too, plus a",
        f"#   supplemental log grid at {per_decade} nodes/decade "
        "(fp-unanchored-quadrature, fp-smooth-as-result).",
        f"# native recoil axis: {len(T)} log bins at {bins_per_decade}/decade, bottom",
        f"#   bin EDGE exactly {edges[0]:.7g} eV (the Phase-10 extended-grid floor),",
        f"#   top edge {edges[-1]:.9g} eV = f x {endf_ceiling_eV():.6g} eV. Knots are the",
        "#   geometric bin centres, so ia_broadening.native_edges reproduces the edges.",
        "# THIS TABLE IS UNBROADENED. The IA kernel is applied downstream, exactly",
        "#   once, on the recoil axis (Plan 13-03). The rate is NEVER multiplied by",
        "#   exp(-2W) (CONVENTIONS J).",
        "#",
        "# columns:",
        "#   T_eV_nr                  recoil energy [eV], unified phonon scale",
        "#   dRdT                     counts/kg/day/keV, declared route",
        "#   dRdT_smoothed_control    the same fold against a resonance-integral-",
        "#                            preserving SMOOTHED sigma_el -- the SC3 control",
        "#                            that must FAIL the imprint test. NOT a result.",
        "#   dRdT_sub5eV_truncated    the Route-B leg, kept for the omission bound",
        "# reproduce: PYTHONPATH=src /opt/anaconda3/bin/python3 -c \"from "
        "qpd_potential import neutron_recoil as n; n.write_dRdT_table()\"",
    ])
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(hdr) + "\n")
        fh.write("T_eV_nr,dRdT,dRdT_smoothed_control,dRdT_sub5eV_truncated,"
                 "accuracy_label\n")
        for t, a, b, c in zip(T, y, y_ctrl, y_trunc):
            fh.write(f"{t:.10e},{a:.10e},{b:.10e},{c:.10e},{ACCURACY_LABEL}\n")
    return path


def read_dRdT_table(path: str = DRDT_CSV) -> dict:
    """Read back the emitted native-axis dR/dT table."""
    a = _numeric_rows(path, ncol=4)
    return {"T_eV": a[:, 0], "dRdT": a[:, 1], "dRdT_smoothed_control": a[:, 2],
            "dRdT_sub5eV_truncated": a[:, 3]}
