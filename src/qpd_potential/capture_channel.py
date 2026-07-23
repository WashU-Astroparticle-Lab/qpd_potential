# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
#
# Phase-14 Plans 14-01 / 14-02: the Ge-only THERMAL-CAPTURE channels.
#
#   14-01  prompt (n,gamma) capture -- cross sections, the band-decomposed
#          reaction rate, the rigorous cascade-independent in-RoI bound, the
#          single-gamma kinematic ceilings, and the discrete-inelastic bound.
#   14-02  the 71Ge ELECTRON-CAPTURE lines -- inventory, activation law, and the
#          M-line fold through the Phase-10 extended response chain.
#
# ============================ THE MEASURED TRAP ==============================
# MF=3 MT=102 in data/endf/raw/n_*.dat is IDENTICALLY 0.0 through the resolved
# resonance region.  In the RRR the capture cross section lives in FILE 2 as
# resonance parameters and File 3 carries only the smooth background, so reading
# MF=3 MT=102 at 0.0253 eV returns 0.0 -- which is exactly the "capture channel
# is zero" outcome ROADMAP Phase 14 forbids, produced out of a file that DOES
# contain the physics.  The operative source is therefore the PRE-RECONSTRUCTED,
# Doppler-broadened LANL Lib80x ACE set at data/endf/ace/32*.800nc, which is the
# same resolution Phase 7 reached for elastic and for the same reason.
# ``mf3_mt102_probe_b`` exists so that the trap is asserted by EXECUTION
# (tests/test_capture_channel.py::test_mf3_mt102_is_zero_in_the_rrr) rather than
# described in prose.  The MF=3 QM field IS used -- it is the capture Q-value and
# it is perfectly well defined there.
#
# ================================== AXIS TAGS ================================
# E_n  : INCIDENT NEUTRON KINETIC ENERGY [eV].  Not a recoil axis.
# T    : NUCLEAR RECOIL energy [eV].
# E_dep: DEPOSITED energy [eV] on the shared extended grid.
# E_rec: RECONSTRUCTED energy [eV], 161 bins.  E_dep and E_rec are NOT equal and
#        are never tabulated on a shared column without a label.
#
# =============================== ACCURACY LABEL ==============================
# order_of_magnitude, inherited from the Phase-9 sea-level flux.  Every rate and
# every bound this module emits carries it.  Many-digit values appear only as
# reproducibility figures for the quadrature and the parsing (fp-precision-
# inflation).
#
# ================================= FLUX LEG ==================================
# phi_default == phi_hi (OUTDOOR).  phi_lo = phi_default/5 is the INDOOR leg
# (09-02 Section 4), not an error bar; it is refused by
# neutron_recoil.neutron_flux_cm2_s_MeV and never appears here.

from __future__ import annotations

import functools
import hashlib
import os
import subprocess

import numpy as np

from . import neutron_recoil as nr
from . import params
from . import parma_neutron_flux as parma

#: Accuracy class of every quantity this module emits.
ACCURACY_LABEL = "order_of_magnitude"

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))

ACE_DIR = os.path.join(REPO_ROOT, "data", "endf", "ace")
RAW_DIR = os.path.join(REPO_ROOT, "data", "endf", "raw")
EGAF_DIR = os.path.join(REPO_ROOT, "data", "egaf")
GE71_DIR = os.path.join(REPO_ROOT, "data", "ge71_ec")
ARTIFACT_DIR = os.path.join(REPO_ROOT, "artifacts", "v2.0")

#: ACE ZAID suffixes.  ``.800nc`` = 293.6 K (the operative set, matching Phase 7
#: for elastic); ``.805nc`` = 0.1 K, used ONLY for the Doppler-sensitivity check.
ACE_SUFFIX_293K = "800nc"
ACE_SUFFIX_0P1K = "805nc"

#: Raw ENDF/B-VIII.0 filenames.  The MAT is READ from the file, never taken from
#: this dict -- the dict only locates the file.
RAW_ENDF_FILE = {
    70: "n_3225_32-Ge-70.dat",
    72: "n_3231_32-Ge-72.dat",
    73: "n_3234_32-Ge-73.dat",
    74: "n_3237_32-Ge-74.dat",
    76: "n_3243_32-Ge-76.dat",
}

MT_CAPTURE = 102
#: MT=51..91 are the DISCRETE inelastic levels (n,n'_1 .. n,n'_40).  MT=91 is the
#: continuum; it is included because ROADMAP SC5 asks for the inelastic channel
#: to be bounded, and excluding the continuum would under-bound it.
MT_INELASTIC_DISCRETE = tuple(range(51, 92))

#: The thermal reference energy, 2200 m/s.
E_THERMAL_REF_eV = 0.0253

#: Phi_th is PHASE 9's product (09-02-NEUTRON-DECLARATION.md Section 5), consumed
#: here unchanged.  It is NOT re-derived in Phase 14.
PHI_TH_PHASE9_cm2_s = 2.767075e-3
PHI_TH_CUTOFF_CONVENTION = "cadmium cutoff, 0.5 eV = 5.0e-7 MeV; lower bound 0.01 eV"
PHI_TH_SOURCE = ("GPD/phases/09-sea-level-surface-environment-lock-p-env/"
                 "09-02-NEUTRON-DECLARATION.md Section 5 (PHASE 9's product)")

#: Biffl et al., PRD 107, 092011 (2023): stated thermal-flux requirement.
BIFFL_PHI_TH_REQUIREMENT_cm2_s = 7.0e-4

#: Incident-neutron energy bands.  The thermal band top is the SAME cadmium
#: cutoff Phi_th uses, so the two are the same band by construction.
FOLD_E_LO_eV = 0.01
FOLD_E_HI_eV = 2.0e7        # the 20 MeV ENDF/B-VIII.0 ceiling
BANDS = (
    ("thermal", 0.01, 0.5),
    ("epithermal", 0.5, 1.0e3),
    ("intermediate", 1.0e3, 1.0e6),
    ("fast", 1.0e6, 2.0e7),
)

#: Wafer thickness for the self-shielding check [cm] (CONVENTIONS Section D).
WAFER_THICKNESS_cm = 0.2

BARN_cm2 = 1.0e-24
SECONDS_PER_DAY = 86400.0
EV_PER_MEV = 1.0e6
U_eV = params._U_MEV * 1.0e6      # atomic mass unit in eV


class CaptureSourceError(ValueError):
    """Raised when a capture cross section is requested from the wrong file."""


# --------------------------------------------------------------------------- #
# Provenance helpers                                                           #
# --------------------------------------------------------------------------- #
def sha256_of(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _git_sha() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                              cwd=REPO_ROOT, capture_output=True,
                              text=True).stdout.strip() or "unknown"
    except Exception:                                        # pragma: no cover
        return "unknown"


def ace_path(A: int, suffix: str = ACE_SUFFIX_293K) -> str:
    return os.path.join(ACE_DIR, f"{32000 + int(A)}.{suffix}")


def raw_endf_path(A: int) -> str:
    return os.path.join(RAW_DIR, RAW_ENDF_FILE[int(A)])


# --------------------------------------------------------------------------- #
# The MF=3 MT=102 TRAP, probed by execution                                    #
# --------------------------------------------------------------------------- #
@functools.lru_cache(maxsize=8)
def _raw_material(A: int):
    import endf
    return endf.Material(raw_endf_path(A))


def mf3_mt102_probe_b(A: int, E_eV) -> np.ndarray:
    """MF=3 MT=102 evaluated straight out of the RAW ENDF file [barn].

    THIS IS THE TRAP, NOT THE PHYSICS.  Through the resolved-resonance region
    this returns IDENTICALLY 0.0, because in the RRR the capture cross section
    lives in File 2 as resonance parameters and File 3 carries only the smooth
    background.  It is exposed so ``test-mf3-zero-recorded`` can assert the zero
    by execution.  Nothing in the fold path calls it.
    """
    sec = _raw_material(int(A)).section_data[3, MT_CAPTURE]
    E = np.atleast_1d(np.asarray(E_eV, dtype=float))
    return np.asarray([float(sec["sigma"](float(e))) for e in E], dtype=float)


def capture_Q_eV(A: int) -> float:
    """Capture Q-value [eV], READ from the MF=3 MT=102 ``QM`` field.

    The QM field is perfectly well defined in File 3 even where the File-3 cross
    section is zero -- QM is the reaction Q-value, not a cross section.  Reading
    it here is therefore the correct use of the raw file, and it is read rather
    than transcribed.
    """
    return float(_raw_material(int(A)).section_data[3, MT_CAPTURE]["QM"])


def endf_MAT(A: int) -> int:
    """The MAT number, read from the file header rather than from the filename."""
    return int(_raw_material(int(A)).MAT)


# --------------------------------------------------------------------------- #
# The OPERATIVE source: the pre-reconstructed Lib80x ACE set                   #
# --------------------------------------------------------------------------- #
@functools.lru_cache(maxsize=16)
def _ace(A: int, suffix: str):
    import endf
    return endf.IncidentNeutron.from_ace(ace_path(A, suffix))


@functools.lru_cache(maxsize=32)
def _ace_xs(A: int, mt: int, suffix: str):
    """(E_eV, sigma_barn, temperature_key) for one MT from one ACE file."""
    inc = _ace(int(A), suffix)
    if int(mt) not in inc.reactions:
        return None
    xs = inc.reactions[int(mt)].xs
    key = list(xs.keys())[0]
    f = xs[key]
    return np.asarray(f.x, dtype=float), np.asarray(f.y, dtype=float), str(key)


def ace_temperature_key(A: int, suffix: str = ACE_SUFFIX_293K) -> str:
    return _ace_xs(A, MT_CAPTURE, suffix)[2]


@functools.lru_cache(maxsize=16)
def _capture_grid(A: int, suffix: str):
    E, s, _ = _ace_xs(int(A), MT_CAPTURE, suffix)
    return E, s


def sigma_capture_b(A: int, E_eV, *, suffix: str = ACE_SUFFIX_293K) -> np.ndarray:
    """sigma_(n,gamma) [barn] for isotope ``A`` at incident energies ``E_eV``.

    Linear interpolation on the ACE native grid, which is NJOY's own lin-lin
    linearisation to err=1e-3 -- the same treatment Phase 7 applied to elastic.
    """
    E, s = _capture_grid(int(A), suffix)
    return np.interp(np.asarray(E_eV, dtype=float), E, s)


@functools.lru_cache(maxsize=16)
def _inelastic_grid(A: int, suffix: str):
    """Summed MT=51..91 on the union of the contributing MTs' own grids."""
    parts = []
    for mt in MT_INELASTIC_DISCRETE:
        got = _ace_xs(int(A), mt, suffix)
        if got is not None:
            parts.append((got[0], got[1]))
    if not parts:
        raise CaptureSourceError(f"no MT=51..91 present for Ge-{A}")
    union = np.unique(np.concatenate([p[0] for p in parts]))
    tot = np.zeros_like(union)
    for x, y in parts:
        # Each partial has threshold behaviour: it is zero below its own grid.
        tot += np.interp(union, x, y, left=0.0, right=y[-1])
    return union, tot


def sigma_inelastic_b(A: int, E_eV, *, suffix: str = ACE_SUFFIX_293K) -> np.ndarray:
    """Summed DISCRETE-plus-continuum inelastic sigma (MT=51..91) [barn]."""
    E, s = _inelastic_grid(int(A), suffix)
    return np.interp(np.asarray(E_eV, dtype=float), E, s, left=0.0, right=s[-1])


def sigma_capture_natural_b(E_eV, *, suffix: str = ACE_SUFFIX_293K) -> np.ndarray:
    """Abundance-weighted natural-Ge sigma_(n,gamma) [barn].

    Abundances come from ``params.GE_ISOTOPES`` ONLY -- never transcribed.
    """
    E = np.asarray(E_eV, dtype=float)
    out = np.zeros_like(E)
    for iso in params.GE_ISOTOPES:
        out = out + iso.abundance * sigma_capture_b(iso.A, E, suffix=suffix)
    return out


def sigma_inelastic_natural_b(E_eV, *, suffix: str = ACE_SUFFIX_293K) -> np.ndarray:
    E = np.asarray(E_eV, dtype=float)
    out = np.zeros_like(E)
    for iso in params.GE_ISOTOPES:
        out = out + iso.abundance * sigma_inelastic_b(iso.A, E, suffix=suffix)
    return out


def thermal_capture_summary(*, suffix: str = ACE_SUFFIX_293K) -> dict:
    """sigma_(n,gamma) at 0.0253 eV per isotope and natural, with the shares.

    The 73Ge row is the one that matters: 7.75% of the atoms carrying roughly
    half the natural thermal capture.  Both numbers are COMPUTED here.
    """
    per = {}
    nat = 0.0
    for iso in params.GE_ISOTOPES:
        s = float(sigma_capture_b(iso.A, E_THERMAL_REF_eV, suffix=suffix))
        per[iso.A] = {"sigma_b": s, "abundance": iso.abundance,
                      "contribution_b": iso.abundance * s}
        nat += iso.abundance * s
    for A in per:
        per[A]["share_of_natural"] = per[A]["contribution_b"] / nat
    return {"E_eV": E_THERMAL_REF_eV, "natural_sigma_b": nat,
            "per_isotope": per, "ace_suffix": suffix,
            "accuracy_label": ACCURACY_LABEL}


# --------------------------------------------------------------------------- #
# Single-gamma kinematic ceiling                                               #
# --------------------------------------------------------------------------- #
def product_mass_eV(A: int) -> float:
    """Mass of the CAPTURE PRODUCT (A+1) nucleus [eV].

    The recoiling body after (n,gamma) on A is the A+1 nucleus, so the ceiling
    T = Q^2 / (2 M_(A+1) c^2) uses A+1, not A.  Using A would overstate every
    ceiling by ~1.4%.
    """
    return (int(A) + 1) * U_eV


def single_gamma_ceiling_eV(A: int) -> float:
    """T_max = Q_cap^2 / (2 M_(A+1) c^2) [eV] -- the ONE-gamma kinematic maximum.

    THIS IS A CEILING, NOT THE CASCADE ANSWER (fp-single-gamma-as-cascade).  A
    real capture de-excites through a multi-gamma cascade, and because
    Sum(E_gamma^2) != (Sum E_gamma)^2 the cascade mean is BELOW this value by
    roughly the multiplicity.
    """
    Q = capture_Q_eV(A)
    return Q * Q / (2.0 * product_mass_eV(A))


def single_gamma_ceilings() -> dict:
    """All five ceilings, plus which isotope sets the maximum."""
    out = {}
    for iso in params.GE_ISOTOPES:
        out[iso.A] = {
            "Q_cap_eV": capture_Q_eV(iso.A),
            "M_product_eV": product_mass_eV(iso.A),
            "T_max_eV": single_gamma_ceiling_eV(iso.A),
            "product": f"{iso.A + 1}Ge",
        }
    amax = max(out, key=lambda a: out[a]["T_max_eV"])
    return {"per_isotope": out, "max_isotope": amax,
            "max_T_eV": out[amax]["T_max_eV"], "accuracy_label": ACCURACY_LABEL}


def gamma_emission_recoil_eV(E_gamma_eV: float, A_recoil: int) -> float:
    """T = E_gamma^2 / (2 M c^2) [eV] for a single gamma emitted by mass A."""
    return float(E_gamma_eV) ** 2 / (2.0 * int(A_recoil) * U_eV)


def sum_of_squares_demo(partition_eV) -> dict:
    """Numerical demonstration that Sum(E^2) != (Sum E)^2 for one partition.

    Returns the two sums and their ratio.  The point is arithmetic, not
    physical: it is what makes the single-gamma ceiling an OVERSTATEMENT of a
    real cascade, and it is shown with numbers rather than asserted.
    """
    e = np.asarray(partition_eV, dtype=float)
    ss = float(np.sum(e ** 2))
    sq = float(np.sum(e) ** 2)
    return {"partition_eV": e.tolist(), "sum_of_squares": ss,
            "square_of_sum": sq, "ratio_ss_over_sq": ss / sq,
            "multiplicity": int(e.size)}


# --------------------------------------------------------------------------- #
# The quadrature and the fold                                                  #
# --------------------------------------------------------------------------- #
def capture_quadrature_nodes(e_lo_eV: float, e_hi_eV: float, *,
                             per_decade: int = 200,
                             suffix: str = ACE_SUFFIX_293K,
                             anchors=()) -> np.ndarray:
    """Node set for the capture fold: ACE native grid UNION a stated log grid.

    Including every ACE native node inside the band means the fold never
    averages across the resonance structure it exists to resolve.  The band
    edges are explicit anchors, so band integrals sum to the total EXACTLY
    rather than to a quadrature tolerance.
    """
    grids = [_capture_grid(iso.A, suffix)[0] for iso in params.GE_ISOTOPES]
    native = np.unique(np.concatenate(grids))
    n_sup = int(round(np.log10(e_hi_eV / e_lo_eV) * per_decade)) + 1
    nodes = np.concatenate([
        native[(native >= e_lo_eV) & (native <= e_hi_eV)],
        np.logspace(np.log10(e_lo_eV), np.log10(e_hi_eV), n_sup),
        np.asarray(anchors, dtype=float).ravel(),
        [e_lo_eV, e_hi_eV],
    ])
    nodes = np.unique(nodes)
    return nodes[(nodes >= e_lo_eV) & (nodes <= e_hi_eV)]


def flux_at_nodes_cm2_s_eV(E_eV: np.ndarray) -> np.ndarray:
    """dPhi/dE_n [cm^-2 s^-1 eV^-1] on the OUTDOOR leg.

    Delegates to ``neutron_recoil.neutron_flux_cm2_s_MeV``, which evaluates the
    PINNED PARMA DRIVER DIRECTLY at every node -- it does not interpolate either
    committed table.  That is precisely what covers the 1 eV - 10.14 eV gap that
    ``data/ambient_neutron_thermal_v2.0.csv`` (0.01-1 eV) and
    ``data/ambient_neutron_flux_v1.1.csv`` (10.14 eV - 197 MeV) leave open, with
    no interpolation across either table's edge.
    """
    return nr.neutron_flux_cm2_s_MeV(E_eV) / EV_PER_MEV


def reaction_rate_counts_kg_day(sigma_fn, e_lo_eV: float, e_hi_eV: float, *,
                                per_decade: int = 200,
                                suffix: str = ACE_SUFFIX_293K,
                                nodes: np.ndarray | None = None,
                                flux: np.ndarray | None = None) -> dict:
    """R = N_Ge INT phi(E_n) sigma(E_n) dE_n  [counts kg^-1 day^-1].

    Dimensions: [cm^-2 s^-1 eV^-1] x [cm^2] x [eV] x [kg^-1] x [s/day]
              = counts kg^-1 day^-1.

    Quadrature: exact-for-a-power-law log-log segment integration
    (``neutron_recoil.loglog_segment_integrals``), the same estimator Phase 13
    used for the elastic fold.
    """
    if nodes is None:
        nodes = capture_quadrature_nodes(e_lo_eV, e_hi_eV,
                                         per_decade=per_decade, suffix=suffix)
    if flux is None:
        flux = flux_at_nodes_cm2_s_eV(nodes)
    sig_cm2 = np.asarray(sigma_fn(nodes), dtype=float) * BARN_cm2
    integrand = flux * sig_cm2
    seg = nr.loglog_segment_integrals(nodes, integrand)
    phi_sigma = float(np.sum(seg))                 # [cm^-2 s^-1] x [cm^2]
    n_ge = nr.n_ge_per_kg()
    return {
        "rate_counts_kg_day": phi_sigma * n_ge * SECONDS_PER_DAY,
        "phi_sigma_cm2_per_cm2_s": phi_sigma,
        "n_ge_per_kg": n_ge,
        "n_nodes": int(nodes.size),
        "e_lo_eV": float(e_lo_eV),
        "e_hi_eV": float(e_hi_eV),
        "accuracy_label": ACCURACY_LABEL,
    }


@functools.lru_cache(maxsize=8)
def _nodes_and_flux(per_decade: int, suffix: str):
    """Nodes over the WHOLE fold band, with the band edges as exact anchors.

    One PARMA subprocess call for the whole node set; band integrals are then
    slices of the same node/flux arrays, so the bands sum to the total exactly.
    """
    edges = [b[1] for b in BANDS] + [BANDS[-1][2]]
    nodes = capture_quadrature_nodes(FOLD_E_LO_eV, FOLD_E_HI_eV,
                                     per_decade=per_decade, suffix=suffix,
                                     anchors=edges)
    return nodes, flux_at_nodes_cm2_s_eV(nodes)


def band_decomposed_rate(sigma_fn, *, per_decade: int = 200,
                         suffix: str = ACE_SUFFIX_293K) -> dict:
    """The reaction rate over the full band and over each of the four bands."""
    nodes, flux = _nodes_and_flux(per_decade, suffix)
    total = reaction_rate_counts_kg_day(sigma_fn, FOLD_E_LO_eV, FOLD_E_HI_eV,
                                        nodes=nodes, flux=flux)
    bands = {}
    for name, lo, hi in BANDS:
        m = (nodes >= lo) & (nodes <= hi)
        bands[name] = reaction_rate_counts_kg_day(
            sigma_fn, lo, hi, nodes=nodes[m], flux=flux[m])
        bands[name]["fraction"] = (bands[name]["rate_counts_kg_day"]
                                   / total["rate_counts_kg_day"])
    band_sum = sum(b["rate_counts_kg_day"] for b in bands.values())
    return {
        "total": total,
        "bands": bands,
        "band_sum_counts_kg_day": band_sum,
        "band_sum_residual": abs(band_sum - total["rate_counts_kg_day"])
                             / total["rate_counts_kg_day"],
        "per_decade": int(per_decade),
        "ace_suffix": suffix,
        "accuracy_label": ACCURACY_LABEL,
    }


def gap_coverage_report(*, per_decade: int = 200,
                        suffix: str = ACE_SUFFIX_293K) -> dict:
    """Evidence that the 1 - 10.14 eV table gap is DRIVER-evaluated.

    Two facts, both measured:
      * how many quadrature nodes fall inside the gap;
      * that the flux at a gap node is BIT-IDENTICAL to a direct
        ``parma.differential_flux`` call, i.e. no table interpolation entered.
    """
    thermal_top_eV = parma.THERMAL_TABLE_E_HI_MEV * EV_PER_MEV      # 1 eV
    v11_floor_eV = float(nr.read_flux_v11()["E_lo_eV"][0])          # 10.14... eV
    nodes, flux = _nodes_and_flux(per_decade, suffix)
    inside = (nodes > thermal_top_eV) & (nodes < v11_floor_eV)
    probe = nodes[inside]
    direct = parma.differential_flux(probe / EV_PER_MEV).phi_cm2_s_mev / EV_PER_MEV
    return {
        "gap_lo_eV": thermal_top_eV,
        "gap_hi_eV": v11_floor_eV,
        "n_nodes_in_gap": int(inside.sum()),
        "max_abs_diff_vs_direct_driver": float(np.max(np.abs(flux[inside] - direct)))
                                         if inside.any() else float("nan"),
        "bit_identical": bool(np.array_equal(flux[inside], direct)),
        "note": ("neutron_recoil.neutron_flux_cm2_s_MeV evaluates the pinned PARMA "
                 "driver at EVERY node; neither committed table is interpolated "
                 "anywhere, so the gap is covered by construction and this report "
                 "measures that rather than assuming it."),
    }


def naive_thermal_product() -> dict:
    """Phi_th x sigma_(n,gamma)(0.0253 eV) x N_Ge x 86400.

    NOT THE ANSWER (fp-westcott-product).  sigma_(n,gamma) is a 1/v absorber, so
    a band-integrated flux times a POINT cross section is not the reaction rate.
    It is emitted as a separately labelled comparison whose measured ratio
    against the folded thermal band must DIFFER; agreement would indicate the
    fold collapsed to this product rather than that the physics is right.
    """
    sig_b = float(sigma_capture_natural_b(E_THERMAL_REF_eV))
    n_ge = nr.n_ge_per_kg()
    rate = (PHI_TH_PHASE9_cm2_s * sig_b * BARN_cm2 * n_ge * SECONDS_PER_DAY)
    return {
        "label": "NAIVE_PRODUCT_NOT_THE_ANSWER",
        "phi_th_cm2_s": PHI_TH_PHASE9_cm2_s,
        "phi_th_source": PHI_TH_SOURCE,
        "phi_th_cutoff_convention": PHI_TH_CUTOFF_CONVENTION,
        "sigma_2200_natural_b": sig_b,
        "rate_counts_kg_day": rate,
        "accuracy_label": ACCURACY_LABEL,
    }


def westcott_comparison(*, per_decade: int = 200) -> dict:
    """The measured ratio naive_product / folded_thermal_band.

    The Westcott factor sqrt(pi)/2 = 0.8862 is reported for CONTEXT ONLY and is
    NOT substituted for the measured ratio.
    """
    bd = band_decomposed_rate(sigma_capture_natural_b, per_decade=per_decade)
    folded = bd["bands"]["thermal"]["rate_counts_kg_day"]
    naive = naive_thermal_product()
    r = naive["rate_counts_kg_day"] / folded
    return {
        "folded_thermal_band_counts_kg_day": folded,
        "naive_product_counts_kg_day": naive["rate_counts_kg_day"],
        "ratio_naive_over_folded": r,
        "relative_difference": r - 1.0,
        "differs_by_more_than_5pct": bool(abs(r - 1.0) > 0.05),
        "westcott_sqrt_pi_over_2": float(np.sqrt(np.pi) / 2.0),
        "westcott_is_NOT_the_measured_ratio": True,
        "total_counts_kg_day": bd["total"]["rate_counts_kg_day"],
        "ratio_naive_over_total": naive["rate_counts_kg_day"]
                                  / bd["total"]["rate_counts_kg_day"],
        "accuracy_label": ACCURACY_LABEL,
    }


def doppler_sensitivity(*, per_decade: int = 200) -> dict:
    """Epithermal band rate at 293.6 K (.800nc) vs 0.1 K (.805nc).

    This ANSWERS the mK caveat Phase 9 Section 5 handed to Phase 14 with a
    number rather than restating it.  The RATE is set by the neutron field's
    temperature (ambient), but the resonance-region Doppler width is set by the
    TARGET temperature, and the sign of that error is not obvious a priori.
    """
    out = {}
    for suffix, label in ((ACE_SUFFIX_293K, "293.6K"), (ACE_SUFFIX_0P1K, "0.1K")):
        def _s(E, _sfx=suffix):
            return sigma_capture_natural_b(E, suffix=_sfx)
        bd = band_decomposed_rate(_s, per_decade=per_decade, suffix=suffix)
        out[label] = {
            "epithermal": bd["bands"]["epithermal"]["rate_counts_kg_day"],
            "thermal": bd["bands"]["thermal"]["rate_counts_kg_day"],
            "total": bd["total"]["rate_counts_kg_day"],
        }
    d = out["0.1K"]["epithermal"] - out["293.6K"]["epithermal"]
    out["epithermal_signed_relative_difference"] = d / out["293.6K"]["epithermal"]
    dt = out["0.1K"]["total"] - out["293.6K"]["total"]
    out["total_signed_relative_difference"] = dt / out["293.6K"]["total"]
    out["accuracy_label"] = ACCURACY_LABEL
    return out


def self_shielding_check(*, per_decade: int = 200,
                         suffix: str = ACE_SUFFIX_293K) -> dict:
    """P_capture(2 mm) = Sigma_102 x 0.2 cm, COMPUTED from the same sigma.

    The thin-target formula R = Phi sigma N presumes this is << 1.  It is
    checked at the thermal reference, at the bottom of the fold band (where 1/v
    makes sigma largest outside resonances), and -- the honest one -- at the
    single largest sigma anywhere on the fold node set, which is a resonance
    peak and is NOT small in the same way.
    """
    h = nr.elastic_header()
    n_cm3 = h.n_ge_per_cm3
    nodes, _ = _nodes_and_flux(per_decade, suffix)
    sig = sigma_capture_natural_b(nodes, suffix=suffix)
    imax = int(np.argmax(sig))

    def _p(sig_b):
        return float(n_cm3 * sig_b * BARN_cm2 * WAFER_THICKNESS_cm)

    s_th = float(sigma_capture_natural_b(E_THERMAL_REF_eV, suffix=suffix))
    s_lo = float(sigma_capture_natural_b(FOLD_E_LO_eV, suffix=suffix))

    # A BOUND on the thin-target overstatement, not a transport calculation.
    # Thin target uses Sigma*t; a normally incident slab uses 1 - exp(-Sigma*t).
    # The ratio of the two folds bounds how much the thin-target formula
    # overstates each band.  No angular distribution and no scattering are
    # modelled, so this is an indicative bound with its direction stated.
    flux = flux_at_nodes_cm2_s_eV(nodes)
    tau = n_cm3 * sig * BARN_cm2 * WAFER_THICKNESS_cm
    slab = {}
    for name, lo, hi in BANDS:
        m = (nodes >= lo) & (nodes <= hi)
        thin = float(np.sum(nr.loglog_segment_integrals(nodes[m], flux[m] * tau[m])))
        att = float(np.sum(nr.loglog_segment_integrals(
            nodes[m], flux[m] * (1.0 - np.exp(-tau[m])))))
        slab[name] = {"thin_target": thin, "slab_attenuated": att,
                      "ratio_att_over_thin": (att / thin) if thin > 0 else float("nan")}
    return {
        "n_ge_per_cm3": n_cm3,
        "thickness_cm": WAFER_THICKNESS_cm,
        "sigma_at_2200ms_b": s_th,
        "P_capture_2mm_at_2200ms": _p(s_th),
        "sigma_at_fold_floor_b": s_lo,
        "P_capture_2mm_at_fold_floor": _p(s_lo),
        "sigma_max_on_nodes_b": float(sig[imax]),
        "E_at_sigma_max_eV": float(nodes[imax]),
        "P_capture_2mm_at_sigma_max": _p(float(sig[imax])),
        "slab_vs_thin_by_band": slab,
        "slab_bound_note": (
            "1 - exp(-Sigma t) vs Sigma t, normal incidence, no scattering and "
            "no angular distribution. It BOUNDS the thin-target overstatement "
            "rather than correcting it; the thin-target rate is the one reported "
            "everywhere else, so the overstatement direction is penalizes_SB."),
        "accuracy_label": ACCURACY_LABEL,
    }


def biffl_comparison() -> dict:
    """The adopted Phi_th against Biffl et al.'s stated requirement.

    Direction matters and is stated: the adopted flux is ABOVE the requirement,
    so this configuration does NOT meet it.
    """
    r = PHI_TH_PHASE9_cm2_s / BIFFL_PHI_TH_REQUIREMENT_cm2_s
    return {
        "phi_th_adopted_cm2_s": PHI_TH_PHASE9_cm2_s,
        "phi_th_source": PHI_TH_SOURCE,
        "biffl_requirement_cm2_s": BIFFL_PHI_TH_REQUIREMENT_cm2_s,
        "ratio_adopted_over_requirement": r,
        "direction": ("ABOVE the requirement -- the unshielded sea-level "
                      "configuration EXCEEDS Biffl's stated thermal-flux "
                      "requirement by this factor"),
        "meets_requirement": bool(r <= 1.0),
        "reference": "Biffl et al., Phys. Rev. D 107, 092011 (2023)",
        "accuracy_label": ACCURACY_LABEL,
    }


def rigorous_in_roi_bound(*, per_decade: int = 200) -> dict:
    """The cascade-INDEPENDENT upper bound on the in-RoI capture-recoil rate.

    DERIVATION, one line: every capture event produces exactly ONE recoiling
    nucleus, therefore at most one event per capture can land in the RoI,
    therefore R_RoI <= R_capture.  This holds on the recoil axis, on the deposit
    axis and on the reconstructed axis alike, because the response matrix's
    columns each sum to 1 and so the fold moves counts without creating them.

    It depends on NO cascade parameter: not the multiplicity, not the gamma
    energy partition, not the angular correlation.  ``cascade_params`` is
    accepted and ignored, and ``test-bound-is-cascade-free`` uses that to assert
    the invariance by execution.
    """
    bd = band_decomposed_rate(sigma_capture_natural_b, per_decade=per_decade)
    return {
        "bound_counts_kg_day": bd["total"]["rate_counts_kg_day"],
        "label": "RIGOROUS_BOUND",
        "derivation": ("every (n,gamma) capture yields exactly one recoiling "
                       "nucleus, so at most one event per capture lands in the "
                       "RoI: R_RoI <= R_capture, on any axis (R's columns sum "
                       "to 1)"),
        "depends_on_cascade": False,
        "accuracy_label": ACCURACY_LABEL,
    }


def in_roi_bound_with_cascade_params(multiplicity=None, partition_eV=None,
                                     angular_correlation=None, *,
                                     per_decade: int = 200) -> float:
    """The same bound, with cascade parameters supplied and DELIBERATELY IGNORED.

    The arguments exist so a test can vary them and assert the returned number
    does not move.  A bound that moved would not be the rigorous bound.
    """
    del multiplicity, partition_eV, angular_correlation
    return rigorous_in_roi_bound(per_decade=per_decade)["bound_counts_kg_day"]


# --------------------------------------------------------------------------- #
# EGAF prompt capture-gamma line lists                                          #
# --------------------------------------------------------------------------- #
#: EGAF product nuclei, one per Ge capture channel: A + n -> (A+1).
EGAF_FILE = {70: "71GE_EGAF.ens", 72: "73GE_EGAF.ens", 73: "74GE_EGAF.ens",
             74: "75GE_EGAF.ens", 76: "77GE_EGAF.ens"}

EGAF_RETRIEVAL_URL = "https://www-nds.iaea.org/pgaa/egaf.zip"


def egaf_available() -> bool:
    return all(os.path.isfile(os.path.join(EGAF_DIR, f))
               for f in EGAF_FILE.values())


def read_egaf_gammas(A: int) -> dict:
    """Parse the ENSDF-format EGAF gamma records for the A+n capture product.

    EACH FILE CARRIES THREE DATASETS: the evaluated ``{~EGAF}`` set and the raw
    ``^BUDAPEST`` and ``^L^A^N^L`` measurement sets, each with its OWN
    normalisation record.  Summing across all three -- which a naive whole-file
    parse does -- inflates the per-capture intensity by roughly a factor of
    three and was caught here by the completeness check below.  Only the
    ``{~EGAF}`` dataset is used, and the selection is recorded.

    ENSDF gamma record, fixed columns (1-indexed):
        1-5 NUCID | 6 continuation | 7 comment | 8 record type ('G')
        | 10-19 E_gamma [keV] | 22-29 RI

    The file's own comment records define the normalisation:
        ``RI$Elemental |s(|g)``, ``NR$Isotopic |s(|g) = NR*RI``,
        ``Divide by |s{-0} for intensity per neutron capture``.
    So intensity per capture = NR * RI / sigma_0, with NR read from the N record
    and sigma_0 from the ``BR$|s{-0}=`` comment.  Both are READ, not supplied.
    """
    path = os.path.join(EGAF_DIR, EGAF_FILE[int(A)])
    lines = open(path, encoding="latin-1").read().splitlines()
    e_keV, ri_b = [], []
    nr_norm, sigma0_b, dsid, in_egaf = None, None, None, False
    for line in lines:
        if len(line) < 9:
            continue
        is_id = (line[5] == " " and line[6] == " " and line[7] == " "
                 and line[9:].strip())
        if is_id:
            dsid = line[9:].strip()
            in_egaf = "EGAF" in dsid.upper()
            continue
        if not in_egaf:
            continue
        if line[6] == "c" and "|s{-0}=" in line and sigma0_b is None:
            try:
                sigma0_b = float(line.split("|s{-0}=", 1)[1].strip().split()[0])
            except (ValueError, IndexError):
                sigma0_b = None
            continue
        if line[5] == " " and line[6] == " " and line[7] == "N" and nr_norm is None:
            try:
                nr_norm = float(line[9:19])
            except ValueError:
                nr_norm = None
            continue
        if line[5] != " " or line[6] != " " or line[7] != "G" or len(line) < 29:
            continue
        try:
            e = float(line[9:19])
            ri = float(line[21:29])
        except ValueError:
            continue                       # unmeasured intensity -- skipped
        e_keV.append(e)
        ri_b.append(ri)
    return {"A_target": int(A), "product": EGAF_FILE[int(A)].split("_")[0],
            "path": path, "sha256": sha256_of(path),
            "E_gamma_keV": np.asarray(e_keV, dtype=float),
            "partial_sigma_b": np.asarray(ri_b, dtype=float),
            "nr_norm": nr_norm, "sigma0_b": sigma0_b,
            "dataset_used": "{~EGAF}",
            "n_gammas": len(e_keV)}


def egaf_cascade_completeness(A: int) -> dict:
    """Does the OBSERVED EGAF cascade carry the full capture Q-value?

    Per capture, energy conservation requires Sum_i I_i E_i = Q_cap (up to the
    recoil, which is eV-scale against a MeV-scale Q).  If the observed sum falls
    short, the line list is REAL but INCOMPLETE, and the missing strength is
    the unobserved quasi-continuum -- which is exactly the part a cascade recoil
    spectrum would need.  This is the check that decides whether the frozen EGAF
    artifact can sharpen the in-RoI FRACTION or only document the attempt.
    """
    g = read_egaf_gammas(A)
    Q = capture_Q_eV(A)
    s0, nrm = g["sigma0_b"], g["nr_norm"]
    if not s0 or not nrm:
        return {**g, "Q_cap_eV": Q, "intensity_per_capture": None,
                "sum_I_E_eV": None, "completeness": None}
    I = nrm * g["partial_sigma_b"] / s0               # per capture
    E_eV = g["E_gamma_keV"] * 1.0e3
    sum_IE = float(np.sum(I * E_eV))
    sum_IE2 = float(np.sum(I * E_eV ** 2))
    return {
        "A_target": int(A), "product": g["product"], "n_gammas": g["n_gammas"],
        "sigma0_b": s0, "nr_norm": nrm, "dataset_used": g["dataset_used"],
        "sha256": g["sha256"], "Q_cap_eV": Q,
        "sum_I_eV_per_capture": float(np.sum(I)),
        "sum_I_E_eV": sum_IE,
        "completeness": sum_IE / Q,
        "sum_I_E2_eV2": sum_IE2,
        "mean_T_from_observed_eV": sum_IE2 / (2.0 * product_mass_eV(A)),
        # The unobserved strength carries E_miss = Q - Sum(I E) per capture.
        # Maximising Sum(I E^2) subject to that budget and to E_i <= Q puts all
        # of it at E = Q, so the missing contribution is at most E_miss * Q.
        # That makes [observed, observed + E_miss*Q/(2Mc^2)] a RIGOROUS bracket
        # on the isotropic-cascade MEAN, given the observed list and energy
        # conservation -- and it is tighter than the single-gamma ceiling.
        "E_missing_eV": max(Q - sum_IE, 0.0),
        "mean_T_upper_bracket_eV": (sum_IE2 + max(Q - sum_IE, 0.0) * Q)
                                   / (2.0 * product_mass_eV(A)),
        "T_max_single_gamma_eV": single_gamma_ceiling_eV(A),
        "label": "CONDITIONAL_ESTIMATE",
    }


# =========================================================================== #
# PLAN 14-02: the 71Ge ELECTRON-CAPTURE lines                                  #
# =========================================================================== #
#: Half-life of 71Ge [days].  Sourced with the retrieval recorded in
#: data/ge71_ec/MANIFEST.md (IAEA Live Chart ground_states, 11.43 d).
GE71_HALF_LIFE_d = 11.43

#: The line inventory.  ENERGIES are DEPOSITED energies, from the ROADMAP
#: Phase-14 SC3 anchor (CONUS+ sub-keV calibration).  158.7 eV is a DEPOSIT and
#: is NEVER quoted as a reconstructed position (fp-deposit-as-reconstructed).
GE71_EC_LINES = (
    ("M", 158.7, 1.4),
    ("L", 1298.5, None),
    ("K", 10368.3, None),
)
GE71_LINE_ENERGY_SOURCE = ("GPD/ROADMAP.md Phase-14 anchor list "
                           "(CONUS+ sub-keV calibration); DEPOSITED energies")

GE71_M_LINE_eV = 158.7

LIVECHART_URL_TEMPLATE = ("https://nds.iaea.org/relnsd/v1/data?"
                          "fields={fields}&nuclides=71ge{extra}")
GE71_GS_CSV = os.path.join(GE71_DIR, "livechart_71ge_ground_states.csv")
GE71_XRAY_CSV = os.path.join(GE71_DIR, "livechart_71ge_decay_rads_x.csv")
GE71_AUGER_CSV = os.path.join(GE71_DIR, "livechart_71ge_decay_rads_e.csv")


def ge71_decay_scheme_available() -> bool:
    return all(os.path.isfile(p) for p in
               (GE71_GS_CSV, GE71_XRAY_CSV, GE71_AUGER_CSV))


def _read_csv_rows(path: str) -> list[dict]:
    import csv
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def ge71_ground_state() -> dict:
    """Q_EC and the half-life, READ from the frozen Live Chart retrieval."""
    row = _read_csv_rows(GE71_GS_CSV)[0]
    return {
        "q_ec_keV": float(row["qec"]),
        "q_ec_unc_keV": float(row["unc_qec"]),
        "half_life_d": float(row["half_life"]),
        "half_life_unit": row["unit_hl"],
        "half_life_s": float(row["half_life_sec"]),
        "decay_mode": row["decay_1"],
        "decay_pct": float(row["decay_1_%"]),
        "daughter": "71Ga (Z=31)",
        "source": "IAEA Live Chart of Nuclides, fields=ground_states",
        "sha256": sha256_of(GE71_GS_CSV),
    }


def _ec_rows(path: str) -> list[dict]:
    """Rows belonging to the 71Ge GROUND-STATE EC decay only.

    The retrieved files also carry the 198.371 keV isomer's IT rows.  Mixing the
    two would inflate every intensity; the filter is on ``decay == 'EC'`` and
    ``p_energy`` at the ground state.
    """
    out = []
    for r in _read_csv_rows(path):
        if r.get("decay") != "EC":
            continue
        pe = (r.get("p_energy") or "").strip()
        if pe not in ("", "0", "0.0"):
            continue
        out.append(r)
    return out


def ge71_k_shell_capture_fraction() -> dict:
    """P_K, DERIVED from K-vacancy conservation on the frozen retrieval.

    Every K-shell vacancy created by the electron capture is filled either
    RADIATIVELY (a Ga K X-ray) or NON-RADIATIVELY (a K Auger electron).  The two
    channels are exhaustive and mutually exclusive, so

        P_K = I(K X-rays) + I(K Auger)     per decay.

    Both intensities are read from the frozen IAEA Live Chart retrieval, so this
    is a DERIVED-FROM-SOURCED number, not a recollected branching fraction
    (fp-assert-branching).

    The retrieved X-ray table lists Kalpha1, Kalpha2 and Kbeta as the leaves and
    K'beta1 / K'beta2 as COMPONENTS of Kbeta; likewise the Auger table lists a
    total 'K' row whose components are KLL, KLX and KXY.  Summing leaves only is
    checked here by requiring the Auger components to reproduce the Auger total.
    """
    xr = _ec_rows(GE71_XRAY_CSV)
    au = _ec_rows(GE71_AUGER_CSV)

    def _get(rows, shell):
        for r in rows:
            if r.get("shell") == shell:
                return float(r["intensity"]), float(r["unc_i"] or 0.0)
        raise KeyError(shell)

    ka1, dka1 = _get(xr, "KA1")
    ka2, dka2 = _get(xr, "KA2")
    kb, dkb = _get(xr, "KB")
    kpb1, _ = _get(xr, "KpB1")
    kpb2, _ = _get(xr, "KpB2")
    k_au, dk_au = _get(au, "K")
    kll, _ = _get(au, "KLL")
    klx, _ = _get(au, "KLX")
    kxy, _ = _get(au, "KXY")

    kx = ka1 + ka2 + kb
    dkx = float(np.sqrt(dka1 ** 2 + dka2 ** 2 + dkb ** 2))
    p_k = (kx + k_au) / 100.0
    dp_k = float(np.sqrt(dkx ** 2 + dk_au ** 2)) / 100.0
    return {
        "I_K_xray_per_100": kx,
        "I_K_xray_unc_per_100": dkx,
        "I_K_auger_per_100": k_au,
        "I_K_auger_unc_per_100": dk_au,
        "P_K": p_k,
        "P_K_unc": dp_k,
        "P_notK_upper_bound": 1.0 - p_k,
        "P_notK_upper_bound_unc": dp_k,
        "kbeta_components_close": abs(kpb1 + kpb2 - kb) <= 1e-6 * max(kb, 1.0),
        "kauger_components_close": abs(kll + klx + kxy - k_au) <= 1e-3 * k_au,
        "status": "SOURCED",
        "derivation": ("K-vacancy conservation: every K hole is filled by a K "
                       "X-ray or a K Auger electron, so P_K = I(Kx) + I(K Auger). "
                       "Intensities from the frozen IAEA Live Chart retrieval."),
        "source": "IAEA Live Chart of Nuclides, fields=decay_rads, rad_types=x and e",
        "sha256_x": sha256_of(GE71_XRAY_CSV),
        "sha256_e": sha256_of(GE71_AUGER_CSV),
    }


def ge71_branching_disposition() -> dict:
    """Per-line branching status: SOURCED for K, BOUNDED for L and M.

    P_K is derived from the frozen retrieval (above).  Splitting the remaining
    1 - P_K between L and M is NOT determined by anything in the retrieved data,
    so P_L and P_M are BOUNDED by 1 - P_K each rather than assigned a value.
    That bound is ~8x tighter than the trivial branching <= 1, and every digit
    of it traces to a recorded command.
    """
    k = ge71_k_shell_capture_fraction()
    rest = k["P_notK_upper_bound"]
    return {
        "K": {"status": "SOURCED", "value": k["P_K"], "unc": k["P_K_unc"],
              "basis": k["derivation"]},
        "L": {"status": "BOUNDED", "upper_bound": rest,
              "basis": "P_L <= 1 - P_K; the L/M split is not determined by the "
                       "retrieved data and is NOT assigned from recollection"},
        "M": {"status": "BOUNDED", "upper_bound": rest,
              "basis": "P_M <= 1 - P_K; same reason. The trivial bound would be "
                       "1.0, so this is tighter by 1/(1-P_K)"},
        "trivial_bound": 1.0,
        "improvement_factor": 1.0 / rest,
        "accuracy_label": ACCURACY_LABEL,
    }


def ge71_lambda_per_day() -> float:
    return float(np.log(2.0) / GE71_HALF_LIFE_d)


def ge71_activity(t_days, a_sat_counts_kg_day: float):
    """A(t) = A_sat (1 - exp(-lambda t)).

    Exact for constant irradiation from t = 0.  A(0) = 0 and A(inf) = A_sat, so
    saturation is a genuine upper bound for ANY exposure history -- but a rate
    quoted without its t is UNDEFINED, not conservative (fp-saturation-unstated):
    at t = 1 d the activity is only a few percent of saturation.
    """
    t = np.asarray(t_days, dtype=float)
    return float(a_sat_counts_kg_day) * (1.0 - np.exp(-ge71_lambda_per_day() * t))


GE71_SCENARIOS = (("t=1d", 1.0), ("t=1_half_life_11.43d", GE71_HALF_LIFE_d),
                  ("t=30d", 30.0), ("saturation", np.inf))


def ge71_production_rate(*, per_decade: int = 200) -> dict:
    """A_sat: the 70Ge-ONLY capture rate over ALL incident energies.

    71Ge is made by 70Ge(n,gamma), and EPITHERMAL 70Ge capture makes it just as
    surely as thermal capture does, so the production rate is the FULL-band
    70Ge capture rate, not the thermal-band one.
    """
    def _s70(E):
        return sigma_capture_b(70, E)
    bd = band_decomposed_rate(_s70, per_decade=per_decade)
    return {
        "a_sat_counts_kg_day": bd["total"]["rate_counts_kg_day"],
        "bands": {k: v["rate_counts_kg_day"] for k, v in bd["bands"].items()},
        "thermal_fraction": bd["bands"]["thermal"]["fraction"],
        "isotope": "70Ge -> 71Ge",
        "accuracy_label": ACCURACY_LABEL,
    }


def ge71_neutrino_recoil_eV() -> dict:
    """T = Q_EC^2 / (2 M c^2) for the coincident neutrino recoil.

    COINCIDENT with the shell relaxation, so it SHIFTS the line rather than
    creating separate events.  Expressed as a fraction of the M line and of one
    reconstructed bin so the "negligible" claim is measured, not asserted.
    """
    gs = ge71_ground_state()
    q_eV = gs["q_ec_keV"] * 1.0e3
    m_eV = 71 * U_eV
    T = q_eV ** 2 / (2.0 * m_eV)
    return {
        "q_ec_eV": q_eV,
        "q_ec_unc_eV": gs["q_ec_unc_keV"] * 1.0e3,
        "T_nu_recoil_eV": T,
        "M_71Ge_eV": m_eV,
        "fraction_of_M_line": T / GE71_M_LINE_eV,
        "reconstructed_bin_width_fraction": None,   # filled by the caller
        "note": ("coincident with the atomic relaxation, so it shifts the "
                 "deposit rather than creating a separate sub-eV event; a "
                 "standalone sub-eV event requires the shell relaxation to "
                 "ESCAPE, which is the declared K-line escape omission"),
        "accuracy_label": ACCURACY_LABEL,
    }


# --------------------------------------------------------------------------- #
# IA broadening exclusion for the EC lines -- ARGUED, not defaulted            #
# --------------------------------------------------------------------------- #
def ec_ia_criterion(T_eV: float = GE71_M_LINE_eV) -> dict:
    """The Phase-15 ELECTRON-recoil IA criterion, evaluated WITH A NUMBER here.

    Phase 15 derived omega_bar_e >= 0.634740 eV from the uncertainty principle
    over the Ge covalent bond -- 35.540 x the nuclear omega_bar -- and evaluated
    2W_e = T/omega_bar_e at the 0.1 eV grid floor, where it gives 0.1574 < 1 and
    the impulse approximation FAILS.

    EVALUATED HERE AT 158.7 eV THE CRITERION COMES OUT THE OTHER WAY, and that
    is reported rather than absorbed: 2W_e = 158.7/0.634740 = 250.0 >> 1, so the
    electron-side IA validity condition is SATISFIED at this line's energy.
    Inheriting Phase 15's sentence would therefore have been wrong.

    The exclusion rests on two other things instead, both stated:
      (1) THE FROZEN KERNEL IS THE WRONG ONE.  ia_broadening uses the NUCLEAR
          omega_bar = 17.8597 meV.  Transplanting it to an electronic deposit
          understates the width by sqrt(35.540) = 5.96x (the Phase-15 number).
      (2) THE DEPOSIT IS NOT A RECOIL.  The 71Ge EC deposit is the atomic
          relaxation energy of a Ga shell vacancy -- a fixed atomic-physics
          quantity, not a recoil against a momentum-distributed target -- so
          there is no Doppler kernel to apply at all.  What broadens its
          measured image is the detector response R, which is applied.

    The width the ELECTRON-side kernel WOULD produce is reported so the stake is
    measured rather than dismissed as "too small" -- Phase 15 established that
    the smallness argument would have been FALSE at the grid floor.
    """
    from . import em_recoil as _er
    sc = _er.electron_ia_scale_eV()
    w_e = sc["omega_bar_e_lower_bound_eV"]
    w_n = params.OMEGA_BAR_eV.value
    two_W_e = float(T_eV) / w_e
    sigma_e = float(np.sqrt(float(T_eV) * w_e))
    sigma_n = float(np.sqrt(float(T_eV) * w_n))
    return {
        "T_eV": float(T_eV),
        "omega_bar_e_lower_bound_eV": w_e,
        "omega_bar_nuclear_eV": w_n,
        "ratio_omega_e_over_omega_nuclear": w_e / w_n,
        "two_W_e": two_W_e,
        "ia_validity_condition": "2W_e >> 1",
        "criterion_satisfied_at_this_energy": bool(two_W_e > 1.0),
        "phase15_two_W_e_at_grid_floor": _er.EXT_FLOOR_eV / w_e,
        "electron_side_sigma_eV": sigma_e,
        "electron_side_sigma_over_T": sigma_e / float(T_eV),
        "nuclear_transplant_sigma_eV": sigma_n,
        "transplant_understatement_factor": sigma_e / sigma_n,
        "broadening_applied": False,
        "exclusion_basis": (
            "NOT the 2W_e criterion, which is SATISFIED at 158.7 eV; and NOT "
            "smallness, which Phase 15 showed would be a false argument. The "
            "exclusion rests on (1) the frozen kernel carrying the NUCLEAR "
            "omega_bar, whose transplant understates the electron-side width by "
            "the factor reported here, and (2) the EC deposit being an atomic "
            "relaxation energy rather than a recoil against a momentum "
            "distribution, so no impulse-approximation Doppler kernel applies."),
        "accuracy_label": ACCURACY_LABEL,
    }


# --------------------------------------------------------------------------- #
# The M-line fold through the Phase-10 extended response chain                 #
# --------------------------------------------------------------------------- #
def fold_monochromatic_line(design: str, E_line_eV: float, rate_counts_kg_day: float,
                            *, broaden: bool = False,
                            sharpness: float | None = None,
                            p_trig_override: np.ndarray | None = None) -> dict:
    """Fold a MONOCHROMATIC deposit through R(E_rec|E_dep) for one design.

    Structurally the Phase-13 / Phase-15 extended path, with the input reduced
    to a single populated deposit bin.  Guards, all raising:
      * 744-column shape check (the v1.0 584-column matrix would truncate at
        10.14 eV and is the wrong object);
      * column-sum check (R's columns must each sum to 1, else the conservation
        residual would be measuring the matrix rather than the fold);
      * broadening refusal -- this path is for ELECTRON-recoil atomic deposits
        and ``broaden=True`` raises rather than silently applying a nuclear
        kernel (see :func:`ec_ia_criterion`);
      * line-inside-the-axis check.

    The trigger is composed on the DEPOSIT axis, MULTIPLYING eps
    (CONVENTIONS Section I).  The rate is NEVER multiplied by exp(-2W).
    """
    from . import fold as _fold, trigger as _trigger

    if broaden:
        raise ValueError(
            "broaden=True is refused on the 71Ge EC line path. The deposit is an "
            "ELECTRONIC atomic relaxation energy, not a nuclear recoil; the "
            "frozen IA kernel carries the NUCLEAR omega_bar and transplanting it "
            "would understate the electron-side width by ~5.96x "
            "(fp-ia-on-electron-recoil). See capture_channel.ec_ia_criterion().")

    d = _fold.load_design_extended(design)
    R = d["R_non_paralyzable"]
    E_dep_edges = d["E_dep_edges_eV"]
    E_dep_centers = d["E_dep_centers_eV"]
    E_rec_edges = d["E_rec_edges_eV"]
    E_rec_centers = d["E_rec_centers_eV"]
    dE_rec_keV = np.diff(E_rec_edges) / 1.0e3

    if R.shape[1] != E_dep_centers.size or E_dep_centers.size != 744:
        raise ValueError(
            f"{design}: expected the 744-column EXTENDED response matrix, got "
            f"{R.shape}. The v1.0 584-column matrix would truncate at 10.14 eV.")
    colsum = R.sum(axis=0)
    if not np.allclose(colsum, 1.0, atol=1e-9):
        raise ValueError(f"{design}: response-matrix columns do not sum to 1")
    if not (E_dep_edges[0] <= E_line_eV <= E_dep_edges[-1]):
        raise ValueError(
            f"line at {E_line_eV} eV lies outside the extended deposit axis "
            f"[{E_dep_edges[0]}, {E_dep_edges[-1]}] eV")

    idx = int(np.searchsorted(E_dep_edges, E_line_eV, side="right") - 1)
    idx = min(max(idx, 0), E_dep_centers.size - 1)
    N_dep = np.zeros(E_dep_centers.size, dtype=float)
    N_dep[idx] = float(rate_counts_kg_day)

    if p_trig_override is None:
        P = np.asarray(_trigger.P_trig(E_dep_centers, sharpness=sharpness), float)
    else:
        P = np.asarray(p_trig_override, float)
        if P.shape != E_dep_centers.shape:
            raise ValueError("p_trig_override must live on the deposit centres")

    N_rec = _fold.fold_counts(N_dep, R)
    N_rec_trig = _fold.fold_counts(N_dep * P, R)
    dRdErec = N_rec / dE_rec_keV
    dRdErec_trig = N_rec_trig / dE_rec_keV

    deposit_counts = float(N_dep.sum())
    rec_counts = float(N_rec.sum())
    budget = {
        "input_counts": float(rate_counts_kg_day),
        "leaked_below_floor": 0.0,
        "leaked_below_zero": 0.0,
        "leaked_above_top": 0.0,
        "deposit_counts": deposit_counts,
        "reconstructed_counts": rec_counts,
        "residual_retained_plus_leaked": abs(deposit_counts - float(rate_counts_kg_day))
                                         / float(rate_counts_kg_day),
        "residual_retained_only": (deposit_counts - float(rate_counts_kg_day))
                                  / float(rate_counts_kg_day),
        "residuals_coincide_because_no_broadening": True,
        "residual_fold": abs(rec_counts - deposit_counts) / deposit_counts,
    }

    peak = int(np.argmax(N_rec))
    in_roi = (E_rec_centers >= 10.0) & (E_rec_centers <= 100.0)
    sub_ev = E_rec_centers < 1.0
    return {
        "design": design,
        "channel": "ge71_ec_M_line",
        "E_line_eV_DEPOSITED": float(E_line_eV),
        "deposit_bin_index": idx,
        "deposit_bin_center_eV": float(E_dep_centers[idx]),
        "broadening_applied": False,
        "E_dep_centers_eV": E_dep_centers,
        "E_dep_edges_eV": E_dep_edges,
        "E_rec_centers_eV": E_rec_centers,
        "E_rec_edges_eV": E_rec_edges,
        "P_trig_on_Edep": P,
        "P_trig_at_line": float(P[idx]),
        "N_dep": N_dep,
        "N_rec": N_rec,
        "N_rec_trigger": N_rec_trig,
        "dRdErec": dRdErec,
        "dRdErec_trigger": dRdErec_trig,
        "peak_index": peak,
        "peak_Erec_eV": float(E_rec_centers[peak]),
        "mean_Erec_eV": float(np.sum(N_rec * E_rec_centers) / rec_counts),
        "mapping_slope_peak": float(E_rec_centers[peak]) / float(E_line_eV),
        "mapping_slope_mean": float(np.sum(N_rec * E_rec_centers) / rec_counts)
                              / float(E_line_eV),
        "in_roi_counts": float(N_rec[in_roi].sum()),
        "in_roi_fraction": float(N_rec[in_roi].sum() / rec_counts),
        "sub_ev_counts": float(N_rec[sub_ev].sum()),
        "sub_ev_fraction": float(N_rec[sub_ev].sum() / rec_counts),
        "counts_budget": budget,
        "accuracy_label": ACCURACY_LABEL,
    }


# =========================================================================== #
# ARTIFACT WRITERS -- Plan 14-01                                               #
# =========================================================================== #
XS_CSV = os.path.join(ARTIFACT_DIR, "ge_capture_xs.csv")
RATE_BANDS_CSV = os.path.join(ARTIFACT_DIR, "capture_rate_bands.csv")
RECOIL_BOUNDS_CSV = os.path.join(ARTIFACT_DIR, "capture_recoil_bounds.csv")

#: Node density of the EMITTED artifact grid.  The FOLD does NOT use this grid;
#: it uses the ACE native union grid, and the header reports the difference so
#: the artifact's own coarseness cannot be mistaken for the fold's.
XS_ARTIFACT_PER_DECADE = 100


def _artifact_grid() -> np.ndarray:
    n = int(round(np.log10(FOLD_E_HI_eV / FOLD_E_LO_eV) * XS_ARTIFACT_PER_DECADE)) + 1
    return np.logspace(np.log10(FOLD_E_LO_eV), np.log10(FOLD_E_HI_eV), n)


def _sigma_integral(sigma_fn, nodes, lo, hi) -> float:
    m = (nodes >= lo) & (nodes <= hi)
    x = nodes[m]
    return float(np.sum(nr.loglog_segment_integrals(x, np.asarray(sigma_fn(x), float))))


def write_capture_xs_csv(path: str = XS_CSV) -> str:
    """Freeze the Ge capture + discrete-inelastic cross sections (deliv-capture-xs).

    Reproduce with:
        PYTHONPATH=src /opt/anaconda3/bin/python3 -c \
          "from qpd_potential import capture_channel as c; c.write_capture_xs_csv()"
    """
    grid = _artifact_grid()
    ts = thermal_capture_summary()
    ceil = single_gamma_ceilings()
    native = capture_quadrature_nodes(FOLD_E_LO_eV, FOLD_E_HI_eV, per_decade=200)

    mat = {iso.A: endf_MAT(iso.A) for iso in params.GE_ISOTOPES}
    sha = {iso.A: sha256_of(ace_path(iso.A))[:16] for iso in params.GE_ISOTOPES}
    sha_raw = {iso.A: sha256_of(raw_endf_path(iso.A))[:16] for iso in params.GE_ISOTOPES}
    probe_E = (E_THERMAL_REF_eV, 1.0, 100.0, 1000.0)
    mf3 = {iso.A: mf3_mt102_probe_b(iso.A, probe_E) for iso in params.GE_ISOTOPES}

    band = (1.0e2, 1.0e6)
    i_art = _sigma_integral(sigma_capture_natural_b, grid, *band)
    i_nat = _sigma_integral(sigma_capture_natural_b, native, *band)

    h = [
        "# QPD Phase-14 Plan 14-01 -- Ge (n,gamma) CAPTURE and DISCRETE-INELASTIC cross sections",
        f"# ACCURACY_LABEL = {ACCURACY_LABEL}   <-- attached at the point of definition and to every row.",
        "#",
        "# =================== THE MF=3 MT=102 TRAP, RECORDED IN WORDS ===================",
        "# MF=3 MT=102 in data/endf/raw/n_*.dat is IDENTICALLY 0.0 through the RESOLVED",
        "# RESONANCE REGION.  In the RRR the capture cross section lives in FILE 2 as",
        "# resonance parameters and File 3 carries only the smooth background.  Reading MF=3",
        "# MT=102 at 0.0253 eV therefore returns 0.0 -- which is exactly the 'capture channel",
        "# is zero' outcome ROADMAP Phase 14 names as a FORBIDDEN PROXY, manufactured out of a",
        "# file that DOES contain the physics.  MEASURED THIS RUN at E = "
        + ", ".join(f"{e:g} eV" for e in probe_E) + ":",
    ]
    for A in sorted(mf3):
        h.append(f"#   MF3 MT=102 Ge-{A}: " + ", ".join(f"{v:.6g}" for v in mf3[A]) + "  b")
    h += [
        "# THE OPERATIVE SOURCE IS THE PRE-RECONSTRUCTED, DOPPLER-BROADENED LANL Lib80x ACE",
        "# SET at data/endf/ace/32*.800nc -- the same resolution Phase 7 reached for elastic",
        "# and for the same reason.  The switch is recorded here rather than made silently.",
        "# The MF=3 QM field IS used: QM is the reaction Q-value and is well defined in File 3",
        "# even where the File-3 cross section is zero.",
        "#",
        "# ================================== AXIS TAG ==================================",
        "# E_eV is INCIDENT NEUTRON KINETIC ENERGY.  It is NOT a recoil axis and NOT a",
        "# deposited-energy axis.  No recoil kinematics and no quenching appear in this file.",
        "#",
        "# ================================= PROVENANCE =================================",
        "# source           = ENDF/B-VIII.0 neutron sublibrary (Brown et al., NDS 148, 2018)",
        "# reaction         = MF=3 MT=102 (QM only) ; ACE MT=102 (sigma_capture) ; ACE MT=51..91 (inelastic)",
        "# per_isotope_MAT  = " + ", ".join(f"{A}Ge=MAT{mat[A]}" for A in sorted(mat))
        + "   (read from the file header, not hardcoded)",
        "# raw_sha256_head  = " + ", ".join(f"{A}Ge={sha_raw[A]}" for A in sorted(sha_raw)),
        "# ace_library      = LANL Lib80x (ENDF/B-VIII.0-based ACE), LA-UR-18-24034 (2018)",
        "# ace_zaids        = " + ", ".join(f"{A}Ge={32000+A}.{ACE_SUFFIX_293K}"
                                            for A in sorted(sha)),
        "# ace_sha256_head  = " + ", ".join(f"{A}Ge={sha[A]}" for A in sorted(sha)),
        f"# ace_temperature  = {ace_temperature_key(70)} (ZAID ext .{ACE_SUFFIX_293K} = 293.6 K); "
        f"the 0.1 K set .{ACE_SUFFIX_0P1K} ({ace_temperature_key(70, ACE_SUFFIX_0P1K)}) is used ONLY "
        "for the Doppler-sensitivity check in capture_rate_bands.csv",
        "# ace_reader       = endf.IncidentNeutron.from_ace() (endf 0.1.12)",
        "# abundances       = params.GE_ISOTOPES (IUPAC, Phase-7 nuclear-data lock): "
        + ", ".join(f"{i.A}Ge={i.abundance}" for i in params.GE_ISOTOPES),
        f"# N_Ge             = {nr.n_ge_per_kg():.6e} atoms/kg (derived from the frozen "
        "elastic table's own N_Ge and rho; CONVENTIONS Section D quotes 8.29e24)",
        f"# git_sha          = {_git_sha()}",
        "# reproduce        = PYTHONPATH=src /opt/anaconda3/bin/python3 -c "
        "\"from qpd_potential import capture_channel as c; c.write_capture_xs_csv()\"",
        "#",
        "# ==================== VALIDATION (computed this run, not memorized) ====================",
        f"# natural sigma_(n,gamma)(0.0253 eV) = {ts['natural_sigma_b']:.6f} b   "
        "[ROADMAP states ~2.2 b INDEPENDENTLY; nothing here is fitted or scaled to it]",
    ]
    for A in sorted(ts["per_isotope"]):
        v = ts["per_isotope"][A]
        h.append(f"#   {A}Ge: sigma_th = {v['sigma_b']:.4f} b, abundance = {v['abundance']:.4f}, "
                 f"share of natural thermal capture = {v['share_of_natural']*100:.2f}%")
    h += [
        "#   NOTE 73Ge: 7.75% of the atoms carrying "
        f"{ts['per_isotope'][73]['share_of_natural']*100:.2f}% of the natural thermal capture.",
        "# per-isotope capture Q-value, READ from the MF=3 MT=102 QM field, and the SINGLE-GAMMA",
        "# kinematic ceiling T_max = Q^2/(2 M_(A+1) c^2).  THE CEILING IS NOT THE CASCADE ANSWER:",
        "# a real capture de-excites through a multi-gamma cascade and Sum(E^2) != (Sum E)^2.",
    ]
    for A in sorted(ceil["per_isotope"]):
        v = ceil["per_isotope"][A]
        h.append(f"#   {A}Ge -> {v['product']}: Q_cap = {v['Q_cap_eV']:.1f} eV, "
                 f"T_max = {v['T_max_eV']:.2f} eV")
    h += [
        f"#   maximum ceiling: {ceil['max_isotope']}Ge at {ceil['max_T_eV']:.2f} eV -- and that is "
        "ALSO the isotope dominating the capture rate.",
        "#   ROADMAP's generic '473 eV at 8 MeV' is an ILLUSTRATION, not the Ge answer; the Ge",
        "#   ceilings follow from the actual QM values above and are not reconciled to it.",
        "# MESH: this artifact is emitted on a STATED log grid of "
        f"{XS_ARTIFACT_PER_DECADE} nodes/decade.  THE FOLD DOES NOT USE THIS GRID -- it uses the",
        "#   ACE NATIVE union grid (NJOY lin-lin, err=1e-3) unioned with 200 nodes/decade.",
        f"#   INT sigma_nat dE over 0.1 keV - 1 MeV: artifact grid {i_art:.6e} b.eV vs native "
        f"{i_nat:.6e} b.eV, relative difference {(i_art - i_nat)/i_nat*100:+.4f}% -- reported so",
        "#   the artifact's coarseness cannot be mistaken for the fold's.",
        "# NCrystal is NOT used here and the reduction is stated with its reason: NCrystal supplies",
        "#   a thermal SCATTERING law S(q,omega); sigma_(n,gamma) is smooth and 1/v and needs none.",
        "# columns: E_eV, sigma_capture_{70,72,73,74,76}Ge_b, sigma_capture_natural_b,",
        "#          sigma_inelastic_MT51_91_natural_b, accuracy_label",
    ]

    per = {iso.A: sigma_capture_b(iso.A, grid) for iso in params.GE_ISOTOPES}
    nat = sigma_capture_natural_b(grid)
    inel = sigma_inelastic_natural_b(grid)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(h) + "\n")
        fh.write("E_eV,sigma_capture_70Ge_b,sigma_capture_72Ge_b,sigma_capture_73Ge_b,"
                 "sigma_capture_74Ge_b,sigma_capture_76Ge_b,sigma_capture_natural_b,"
                 "sigma_inelastic_MT51_91_natural_b,accuracy_label\n")
        for i, e in enumerate(grid):
            fh.write(f"{e:.9e}," + ",".join(f"{per[A][i]:.6e}" for A in (70, 72, 73, 74, 76))
                     + f",{nat[i]:.6e},{inel[i]:.6e},{ACCURACY_LABEL}\n")
    return path


def per_isotope_band_rates(sigma_kind: str = "capture", *,
                           per_decade: int = 200,
                           suffix: str = ACE_SUFFIX_293K) -> dict:
    """Abundance-weighted per-isotope contributions to the natural rate."""
    out = {}
    for iso in params.GE_ISOTOPES:
        if sigma_kind == "capture":
            def _s(E, A=iso.A, ab=iso.abundance, sfx=suffix):
                return ab * sigma_capture_b(A, E, suffix=sfx)
        else:
            def _s(E, A=iso.A, ab=iso.abundance, sfx=suffix):
                return ab * sigma_inelastic_b(A, E, suffix=sfx)
        out[iso.A] = band_decomposed_rate(_s, per_decade=per_decade, suffix=suffix)
    return out


def top_decade_fraction(sigma_fn, *, per_decade: int = 200,
                        suffix: str = ACE_SUFFIX_293K) -> float:
    """Fraction of a reaction rate coming from the top decade, 2 - 20 MeV."""
    nodes, flux = _nodes_and_flux(per_decade, suffix)
    tot = reaction_rate_counts_kg_day(sigma_fn, FOLD_E_LO_eV, FOLD_E_HI_eV,
                                      nodes=nodes, flux=flux)["rate_counts_kg_day"]
    m = (nodes >= 2.0e6) & (nodes <= FOLD_E_HI_eV)
    top = reaction_rate_counts_kg_day(sigma_fn, 2.0e6, FOLD_E_HI_eV,
                                      nodes=nodes[m], flux=flux[m])["rate_counts_kg_day"]
    return top / tot


THERMAL_DOMINANCE_THRESHOLD = 0.60


def thermal_dominance_verdict(*, per_decade: int = 200) -> dict:
    """THE PLAN'S PRIMARY NON-IDENTITY DISCONFIRMING CHECK.

    Nothing in CALC-23, in the phase title or in the ROADMAP establishes that the
    thermal band dominates the capture rate.  1/v weighting favours thermal; the
    sea-level spectrum's flat-in-lethargy 1 eV - 10 keV plateau pushes the other
    way.  The verdict is written either way and the threshold is declared here,
    before the number is computed, rather than chosen after seeing it.
    """
    bd = band_decomposed_rate(sigma_capture_natural_b, per_decade=per_decade)
    f = bd["bands"]["thermal"]["fraction"]
    dominant = f >= THERMAL_DOMINANCE_THRESHOLD
    return {
        "thermal_fraction": f,
        "non_thermal_fraction": 1.0 - f,
        "threshold": THERMAL_DOMINANCE_THRESHOLD,
        "thermal_dominates": bool(dominant),
        "verdict": ("THERMAL FRAMING SURVIVES" if dominant
                    else "THERMAL FRAMING MEASURABLY TOO NARROW"),
        "statement": (
            f"The thermal band (<= 0.5 eV, the same cadmium cutoff Phi_th uses) carries "
            f"{f*100:.2f}% of the total Ge capture rate, against the pre-declared "
            f"{THERMAL_DOMINANCE_THRESHOLD*100:.0f}% threshold. "
            + ("The phase's 'thermal-capture' framing therefore SURVIVES the test -- but "
               f"{(1-f)*100:.2f}% of the channel is NOT thermal, which the phase title does "
               "not admit, and that non-thermal remainder is carried forward to Phase 16 "
               "as part of the channel rather than absorbed into the thermal label."
               if dominant else
               "The phase's 'thermal-capture' framing is therefore MEASURABLY TOO NARROW and "
               "CALC-23's wording is wrong in a second way beyond the already-flagged "
               "phi_th clause.")),
        "bands": {k: v["rate_counts_kg_day"] for k, v in bd["bands"].items()},
        "band_fractions": {k: v["fraction"] for k, v in bd["bands"].items()},
        "total_counts_kg_day": bd["total"]["rate_counts_kg_day"],
        "accuracy_label": ACCURACY_LABEL,
    }


def write_capture_rate_bands_csv(path: str = RATE_BANDS_CSV, *,
                                 per_decade: int = 200) -> str:
    """Freeze the band-decomposed capture reaction rate (deliv-capture-rate).

    Reproduce with:
        PYTHONPATH=src /opt/anaconda3/bin/python3 -c \
          "from qpd_potential import capture_channel as c; c.write_capture_rate_bands_csv()"
    """
    bd = band_decomposed_rate(sigma_capture_natural_b, per_decade=per_decade)
    bd2 = band_decomposed_rate(sigma_capture_natural_b, per_decade=2 * per_decade)
    per_iso = per_isotope_band_rates("capture", per_decade=per_decade)
    wc = westcott_comparison(per_decade=per_decade)
    naive = naive_thermal_product()
    dop = doppler_sensitivity(per_decade=per_decade)
    ss = self_shielding_check(per_decade=per_decade)
    gap = gap_coverage_report(per_decade=per_decade)
    biffl = biffl_comparison()
    tdv = thermal_dominance_verdict(per_decade=per_decade)
    node_delta = abs(bd2["total"]["rate_counts_kg_day"]
                     - bd["total"]["rate_counts_kg_day"]) / bd["total"]["rate_counts_kg_day"]

    h = [
        "# QPD Phase-14 Plan 14-01 -- Ge (n,gamma) CAPTURE REACTION RATE, band-decomposed",
        f"# ACCURACY_LABEL = {ACCURACY_LABEL} on EVERY row.  A bound, not a quantification.",
        "#",
        "# R = N_Ge INT phi(E_n) sigma_(n,gamma)(E_n) dE_n   [counts kg^-1 day^-1]",
        "#   dimensions: [cm^-2 s^-1 eV^-1] x [cm^2] x [eV] x [kg^-1] x [s/day]",
        f"#   N_Ge = {nr.n_ge_per_kg():.6e} atoms/kg (CONVENTIONS Section D)",
        "#",
        "# ================================= FLUX LEG ==================================",
        "# phi_default == phi_hi (OUTDOOR).  phi_lo = phi_default/5 is the INDOOR leg",
        "# (09-02 Section 4), NOT an error bar; it is refused in code and never appears here.",
        "# The flux is evaluated by the PINNED PARMA DRIVER DIRECTLY at every quadrature node.",
        f"#   1 - 10.14 eV table gap: {gap['n_nodes_in_gap']} quadrature nodes fall inside "
        f"[{gap['gap_lo_eV']:g}, {gap['gap_hi_eV']:.5g}] eV; the flux there is BIT-IDENTICAL "
        f"({gap['bit_identical']}) to a direct parma.differential_flux call, so neither committed",
        "#   table is interpolated across the gap.  Measured, not assumed.",
        "#",
        "# ============================ QUADRATURE CONVERGENCE =========================",
        f"# nodes = {bd['total']['n_nodes']} (ACE native union grid + {per_decade}/decade + band edges)",
        f"# node doubling ({per_decade} -> {2*per_decade}/decade) moves the total by "
        f"{node_delta*100:.4f}%  [pass < 0.5%]",
        f"# band rates sum to the total with residual {bd['band_sum_residual']:.3e}  [pass < 0.5%]",
        "#",
        "# ======================= THERMAL-DOMINANCE VERDICT (non-identity check) =======",
        f"# {tdv['verdict']}: thermal fraction {tdv['thermal_fraction']*100:.2f}% vs the "
        f"pre-declared {tdv['threshold']*100:.0f}% threshold.",
        "# " + tdv["statement"],
        "#",
        "# ========== THE NAIVE PRODUCT IS NOT THE ANSWER (fp-westcott-product) =========",
        f"# Phi_th x sigma(0.0253 eV) x N_Ge x 86400 = {naive['rate_counts_kg_day']:.2f} counts/kg/day",
        f"#   vs the SPECTRALLY FOLDED thermal band {wc['folded_thermal_band_counts_kg_day']:.2f}",
        f"#   measured ratio naive/folded = {wc['ratio_naive_over_folded']:.4f} "
        f"({wc['relative_difference']*100:+.2f}%) -- they DIFFER, which is the pass condition.",
        "#   WHY: sigma_(n,gamma) is a 1/v absorber, so a band-integrated flux times a POINT",
        "#   cross section is not the reaction rate.  The 2200 m/s point sits above the",
        "#   flux-weighted mean of sigma over the sub-cadmium band, so the product OVERSTATES it.",
        f"#   The Westcott factor sqrt(pi)/2 = {wc['westcott_sqrt_pi_over_2']:.4f} is quoted for",
        "#   CONTEXT ONLY and is NOT the measured ratio; it is not substituted for it.",
        f"#   TRAP: naive/TOTAL = {wc['ratio_naive_over_total']:.4f}, which LOOKS like agreement.",
        "#   It is not corroboration: the product overstates the thermal band while knowing",
        "#   nothing about the epithermal and fast capture in the total.  Two errors nearly",
        "#   cancelling.  Agreement here would indicate a collapsed fold, not correct physics.",
        "#",
        "# ================== DOPPLER SENSITIVITY (the Phase-9 mK caveat) ===============",
        "# Phase 9 Section 5 handed Phase 14 the 293.6 K processing temperature against a mK",
        "# crystal as an UNVALIDATED assumption it could not settle.  ANSWERED WITH A NUMBER:",
        f"#   epithermal band, 0.1 K (.805nc) vs 293.6 K (.800nc): "
        f"{dop['epithermal_signed_relative_difference']*100:+.5f}%",
        f"#   total: {dop['total_signed_relative_difference']*100:+.5f}%",
        "#   MECHANISM: Doppler broadening is a convolution with a NORMALISED kernel, so it",
        "#   conserves the resonance integral while reshaping peaks.  A ~0 band-integrated shift",
        "#   is the EXPECTED result, not a null cross-check.  CAVEAT RETAINED: anything that",
        "#   resolves individual resonance LINE SHAPES must re-derive from the 0.1 K set.",
        "#",
        "# ======================== SELF-SHIELDING / THIN-TARGET CHECK ==================",
        f"# P_capture(2 mm) = Sigma_102 x 0.2 cm, computed from the SAME sigma used in the fold:",
        f"#   at 2200 m/s (sigma = {ss['sigma_at_2200ms_b']:.4f} b): {ss['P_capture_2mm_at_2200ms']*100:.3f}%  << 1",
        f"#   at the fold floor 0.01 eV (sigma = {ss['sigma_at_fold_floor_b']:.4f} b): "
        f"{ss['P_capture_2mm_at_fold_floor']*100:.3f}%  << 1",
        f"#   AT THE LARGEST sigma ON THE NODE SET ({ss['sigma_max_on_nodes_b']:.2f} b at "
        f"{ss['E_at_sigma_max_eV']:.4g} eV): {ss['P_capture_2mm_at_sigma_max']*100:.1f}% -- NOT << 1.",
        "#   The wafer is nearly BLACK to capture at that resonance peak, so the thin-target",
        "#   formula OVERSTATES the epithermal band.  Bounded, not corrected: comparing",
        "#   INT phi (1-exp(-Sigma t)) dE against INT phi Sigma t dE gives, per band --",
    ]
    for name in ("thermal", "epithermal", "intermediate", "fast"):
        r = ss["slab_vs_thin_by_band"][name]["ratio_att_over_thin"]
        h.append(f"#     {name}: attenuated/thin = {r:.4f}  ({(r-1)*100:+.2f}%)")
    h += [
        "#   The THIN-TARGET rate is the one reported in every row below, so this omission's",
        "#   direction is penalizes_SB (the background is overstated).  Normal incidence, no",
        "#   scattering, no angular distribution: it BOUNDS the effect, it does not correct it.",
        "#",
        "# ================================ BIFFL COMPARISON ===========================",
        f"# Phi_th adopted = {biffl['phi_th_adopted_cm2_s']:.6e} cm^-2 s^-1 "
        f"({PHI_TH_CUTOFF_CONVENTION})",
        f"#   SOURCE: {biffl['phi_th_source']} -- Phase 9's product, NOT Phase 13's, NOT re-derived here.",
        f"#   Biffl et al., PRD 107, 092011 (2023) state a requirement Phi_th < "
        f"{biffl['biffl_requirement_cm2_s']:.1e} n/cm^2/s.",
        f"#   RATIO = {biffl['ratio_adopted_over_requirement']:.4f} -- the adopted flux is "
        f"{biffl['ratio_adopted_over_requirement']:.2f}x ABOVE the requirement.  This unshielded",
        "#   sea-level configuration DOES NOT MEET IT, and that direction is stated rather than skipped.",
        "#",
        f"# top-decade (2 - 20 MeV) fraction of the capture rate = "
        f"{top_decade_fraction(sigma_capture_natural_b, per_decade=per_decade)*100:.4f}% "
        "-- the 20 MeV ENDF ceiling omission is negligible for capture (Phase 13 sustained the",
        "#   CALC-24 deferral on a measured 11.85x margin; the same disposition applies).",
        f"# git_sha = {_git_sha()}",
        "# reproduce = PYTHONPATH=src /opt/anaconda3/bin/python3 -c "
        "\"from qpd_potential import capture_channel as c; c.write_capture_rate_bands_csv()\"",
        "# columns: row_kind, isotope, band, E_lo_eV, E_hi_eV, rate_counts_kg_day, "
        "band_fraction, accuracy_label, note",
    ]

    rows = []

    def _row(kind, iso, band, lo, hi, rate, frac, note):
        rows.append(f"{kind},{iso},{band},{lo:.6g},{hi:.6g},{rate:.6e},"
                    f"{'' if frac is None else format(frac, '.6e')},{ACCURACY_LABEL},\"{note}\"")

    for name, lo, hi in BANDS:
        b = bd["bands"][name]
        _row("FOLDED_BAND", "natural", name, lo, hi, b["rate_counts_kg_day"],
             b["fraction"], "spectral fold, outdoor leg, ACE 293.6 K")
    _row("FOLDED_TOTAL", "natural", "0.01eV-20MeV", FOLD_E_LO_eV, FOLD_E_HI_eV,
         bd["total"]["rate_counts_kg_day"], 1.0,
         "sum of the four bands to residual %.2e" % bd["band_sum_residual"])
    for A in sorted(per_iso):
        pb = per_iso[A]
        for name, lo, hi in BANDS:
            b = pb["bands"][name]
            _row("FOLDED_BAND", f"{A}Ge", name, lo, hi, b["rate_counts_kg_day"],
                 b["rate_counts_kg_day"] / bd["total"]["rate_counts_kg_day"],
                 "abundance-weighted contribution to the natural rate")
        _row("FOLDED_TOTAL", f"{A}Ge", "0.01eV-20MeV", FOLD_E_LO_eV, FOLD_E_HI_eV,
             pb["total"]["rate_counts_kg_day"],
             pb["total"]["rate_counts_kg_day"] / bd["total"]["rate_counts_kg_day"],
             "abundance-weighted; 70Ge is the 71Ge production rate used by plan 14-02")
    _row("NAIVE_PRODUCT_NOT_THE_ANSWER", "natural", "thermal", FOLD_E_LO_eV, 0.5,
         naive["rate_counts_kg_day"], None,
         "Phi_th x sigma(0.0253 eV) x N_Ge x 86400. NOT the reaction rate. "
         "ratio naive/folded_thermal = %.4f (%+.2f%%); NOT sqrt(pi)/2."
         % (wc["ratio_naive_over_folded"], wc["relative_difference"] * 100))
    for lab in ("293.6K", "0.1K"):
        _row("DOPPLER_CHECK", "natural", "epithermal", 0.5, 1.0e3,
             dop[lab]["epithermal"], None,
             f"ACE set {lab}; answers the Phase-9 mK caveat with a number")
    _row("DOPPLER_SIGNED_DIFF", "natural", "epithermal", 0.5, 1.0e3,
         dop["epithermal_signed_relative_difference"], None,
         "relative, 0.1K minus 293.6K over 293.6K; dimensionless in the rate column")
    _row("SELF_SHIELDING_CHECK", "natural", "at_2200ms", E_THERMAL_REF_eV,
         E_THERMAL_REF_eV, ss["P_capture_2mm_at_2200ms"], None,
         "P_capture(2 mm) = Sigma_102 x 0.2 cm; dimensionless in the rate column")
    _row("SELF_SHIELDING_CHECK", "natural", "at_sigma_max", ss["E_at_sigma_max_eV"],
         ss["E_at_sigma_max_eV"], ss["P_capture_2mm_at_sigma_max"], None,
         "NOT << 1 at the resonance peak; the thin-target formula overstates "
         "the epithermal band (penalizes_SB)")
    _row("BIFFL_COMPARISON", "n/a", "thermal", FOLD_E_LO_eV, 0.5,
         biffl["ratio_adopted_over_requirement"], None,
         "Phi_th adopted / Biffl requirement; ABOVE, so the requirement is NOT met")
    _row("NODE_DOUBLING", "natural", "0.01eV-20MeV", FOLD_E_LO_eV, FOLD_E_HI_eV,
         node_delta, None, f"{per_decade} -> {2*per_decade} nodes/decade; relative change")

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(h) + "\n")
        fh.write("row_kind,isotope,band,E_lo_eV,E_hi_eV,rate_counts_kg_day,"
                 "band_fraction,accuracy_label,note\n")
        fh.write("\n".join(rows) + "\n")
    return path


def inelastic_placement() -> dict:
    """Where the discrete-inelastic recoils land relative to the 10-100 eV RoI.

    TWO DIFFERENT RECOILS, and conflating them is the error this guards against:

    (1) THE NUCLEAR RECOIL from the scattering itself.  The reaction is populated
        by FAST neutrons, and the elastic-kinematics ceiling f x E_n with
        f = 4A/(1+A)^2 puts it at tens to hundreds of keV -- FAR ABOVE the RoI.
        The inelastic reaction-rate bound is therefore very loose in the RoI.

    (2) THE GAMMA-EMISSION RECOIL when the excited level de-excites,
        T = E_gamma^2/(2Mc^2).  For the 74Ge 596 keV and 72Ge 834 keV levels this
        is a few eV -- that is the part landing NEAR the band.
    """
    nodes, flux = _nodes_and_flux(200, ACE_SUFFIX_293K)
    sig = sigma_inelastic_natural_b(nodes) * BARN_cm2
    w = flux * sig
    seg = nr.loglog_segment_integrals(nodes, w)
    segE = nr.loglog_segment_integrals(nodes, w * nodes)
    mean_En = float(np.sum(segE) / np.sum(seg))
    f = nr.f_natural()
    return {
        "mean_incident_En_eV": mean_En,
        "f_natural": f,
        "nuclear_recoil_ceiling_at_mean_En_eV": f * mean_En,
        "roi_top_eV": 100.0,
        "named_levels": {
            "74Ge_596keV": {"E_gamma_eV": 596.0e3,
                            "gamma_recoil_eV": gamma_emission_recoil_eV(596.0e3, 74)},
            "72Ge_834keV": {"E_gamma_eV": 834.0e3,
                            "gamma_recoil_eV": gamma_emission_recoil_eV(834.0e3, 72)},
        },
        "statement": (
            "The nuclear recoil accompanying discrete inelastic scattering is set by the "
            "FAST incident neutron and lands at tens to hundreds of keV -- three to four "
            "decades ABOVE the 10-100 eV RoI -- so the inelastic reaction-rate bound is very "
            "loose there. The part landing near the band is the separate GAMMA-EMISSION "
            "recoil E_gamma^2/(2Mc^2), a few eV for the named levels."),
        "accuracy_label": ACCURACY_LABEL,
    }


#: Comparison anchors, on the shared RECONSTRUCTED axis, from the committed
#: prior-phase artifacts and closeouts.  Named so no comparison is anonymous.
PHASE13_ELASTIC_INROI = {"Ta->Al": 5430.287, "Al->Hf": 5485.152}
PHASE12_CEVNS_TOTAL = 118.73


def write_capture_recoil_bounds_csv(path: str = RECOIL_BOUNDS_CSV, *,
                                    per_decade: int = 200) -> str:
    """Freeze the cascade and inelastic recoil bounds (deliv-recoil-bounds)."""
    bound = rigorous_in_roi_bound(per_decade=per_decade)
    ceil = single_gamma_ceilings()
    inel = band_decomposed_rate(sigma_inelastic_natural_b, per_decade=per_decade)
    inel_iso = per_isotope_band_rates("inelastic", per_decade=per_decade)
    place = inelastic_placement()
    demo = sum_of_squares_demo([2.0e6, 3.0e6, 2.4159e6])
    egaf = {A: egaf_cascade_completeness(A) for A in EGAF_FILE} if egaf_available() else {}

    h = [
        "# QPD Phase-14 Plan 14-01 -- Ge capture CASCADE RECOIL BOUNDS and the INELASTIC bound",
        f"# ACCURACY_LABEL = {ACCURACY_LABEL} on every row.  BOUNDS, not quantifications "
        "(ROADMAP SC2).",
        "#",
        "# ===================== THE RIGOROUS, CASCADE-FREE BOUND ======================",
        "# EVERY (n,gamma) capture yields EXACTLY ONE recoiling nucleus, so at most one event",
        "# per capture can land in the RoI:   R_RoI <= R_capture.",
        "# It holds on the RECOIL axis, the DEPOSIT axis and the RECONSTRUCTED axis alike,",
        "# because the response matrix's columns each sum to 1 -- the fold moves counts, it does",
        "# not create them.  It is derived in one line and NOT obtained by integrating a spectrum,",
        "# and it depends on NO cascade parameter: not the multiplicity, not the gamma-energy",
        "# partition, not the angular correlation (test-bound-is-cascade-free asserts that by",
        "# varying all three and checking the number does not move).",
        f"#   BOUND = {bound['bound_counts_kg_day']:.2f} counts kg^-1 day^-1",
        f"#   vs Phase-13 ELASTIC in E_rec 10-100 eV: {PHASE13_ELASTIC_INROI['Ta->Al']:.2f} "
        f"(Ta->Al) / {PHASE13_ELASTIC_INROI['Al->Hf']:.2f} (Al->Hf) -- the SAME ORDER.",
        f"#   vs Phase-12 CEvNS TOTAL {PHASE12_CEVNS_TOTAL}: "
        f"{bound['bound_counts_kg_day']/PHASE12_CEVNS_TOTAL:.1f}x LARGER.",
        "#   THE BOUND IS LOOSE BY AN UNKNOWN FACTOR <= 1: converting it into an in-RoI",
        "#   FRACTION needs the cascade, which is exactly what is not fully determined below.",
        "#",
        "# =============== THE SINGLE-GAMMA CEILING IS NOT THE CASCADE ANSWER ==========",
        "# fp-single-gamma-as-cascade.  Sum(E_gamma^2) != (Sum E_gamma)^2, demonstrated with a",
        f"#   3-gamma partition {demo['partition_eV']} eV summing to the 70Ge Q-value:",
        f"#   Sum(E^2) = {demo['sum_of_squares']:.6e} eV^2 vs (Sum E)^2 = "
        f"{demo['square_of_sum']:.6e} eV^2, ratio {demo['ratio_ss_over_sq']:.6f}.",
        "#   For an equal-energy multiplicity-N cascade the isotropic mean is T_max/N with N",
        "#   LEFT SYMBOLIC -- no multiplicity is assigned from recollection "
        "(fp-assumed-multiplicity).",
        "#",
        "# ===================== EGAF DISPOSITION: ACQUIRED, AND ITS LIMIT =============",
    ]
    if egaf:
        h += [
            "# The EGAF prompt capture-gamma line lists WERE retrieved and are frozen at",
            "# data/egaf/*.ens with the retrieval command, byte counts and SHA-256 recorded in",
            "# data/egaf/MANIFEST.md.  This DISCHARGES the acquisition half of ROADMAP SC1.",
            "# BUT THE SHARPENING GAP SURVIVES, AND IS NOW NAMED WITH A NUMBER: the OBSERVED",
            "# cascade does not carry the full capture Q-value, so the line list cannot close a",
            "# cascade recoil SPECTRUM.  Completeness = Sum(I_i E_i) / Q_cap per capture:",
        ]
        for A in sorted(egaf):
            d = egaf[A]
            if d.get("completeness") is None:
                continue
            h.append(f"#   {A}Ge -> {d['product']}: {d['n_gammas']} gammas, NR={d['nr_norm']}, "
                     f"sigma_0={d['sigma0_b']} b, completeness = {d['completeness']:.4f}, "
                     f"observed multiplicity = {d['sum_I_eV_per_capture']:.3f}")
        h += [
            "#   NOTE the 76Ge outlier: EGAF normalises to sigma_0 = 0.06 b against the ENDF/ACE",
            "#   0.1546 b, and only 9 gammas are listed, so its completeness exceeds 1 and is",
            "#   NOT used. 76Ge carries 0.54% of the natural thermal capture, so excluding it",
            "#   changes nothing -- but the inconsistency is reported rather than smoothed.",
            "#   EACH FILE CARRIES THREE DATASETS ({~EGAF}, ^BUDAPEST, ^L^A^N^L) with separate",
            "#   normalisations; only {~EGAF} is used. Summing all three -- what a naive",
            "#   whole-file parse does -- inflates the per-capture intensity ~3x, and the",
            "#   completeness check above is what caught it.",
        ]
    else:
        h += ["# NAMED GAP: no EGAF line list is present or retrievable in this environment."]
    h += [
        "#",
        "# ======================= INELASTIC (ROADMAP SC5), NAMED ======================",
        f"# summed MT=51..91, natural: {inel['total']['rate_counts_kg_day']:.2f} counts kg^-1 day^-1",
        f"#   {inel['bands']['fast']['fraction']*100:.2f}% of it from the 1-20 MeV band; "
        f"top-decade (2-20 MeV) fraction = "
        f"{top_decade_fraction(sigma_inelastic_natural_b, per_decade=per_decade)*100:.2f}%.",
        "#   THE TOP-DECADE FRACTION EXCEEDS 10%, so Phase 13's 11.85x >20 MeV margin is NOT",
        "#   reused for this channel: the >20 MeV omission for INELASTIC is labelled",
        "#   flatters_SB and carried as such.",
        f"# PLACEMENT: {place['statement']}",
        f"#   flux-and-cross-section-weighted mean incident energy = "
        f"{place['mean_incident_En_eV']/1e6:.4f} MeV; elastic-kinematics recoil ceiling "
        f"f x <E_n> = {place['nuclear_recoil_ceiling_at_mean_En_eV']/1e3:.2f} keV, "
        "which is ~3 decades ABOVE the 100 eV RoI top.",
        f"#   74Ge 596 keV level: gamma-emission recoil = "
        f"{place['named_levels']['74Ge_596keV']['gamma_recoil_eV']:.4f} eV",
        f"#   72Ge 834 keV level: gamma-emission recoil = "
        f"{place['named_levels']['72Ge_834keV']['gamma_recoil_eV']:.4f} eV",
        "#",
        f"# git_sha = {_git_sha()}",
        "# reproduce = PYTHONPATH=src /opt/anaconda3/bin/python3 -c "
        "\"from qpd_potential import capture_channel as c; c.write_capture_recoil_bounds_csv()\"",
        "# columns: quantity, isotope, value, units, expression, evidence_class, "
        "accuracy_label, basis",
    ]

    rows = []

    def _row(q, iso, val, units, expr, cls, basis):
        v = "" if val is None else f"{val:.6e}"
        rows.append(f"{q},{iso},{v},{units},\"{expr}\",{cls},{ACCURACY_LABEL},\"{basis}\"")

    _row("in_RoI_upper_bound", "natural", bound["bound_counts_kg_day"],
         "counts/kg/day", "R_RoI <= R_capture", "RIGOROUS_BOUND",
         "every capture yields exactly one recoiling nucleus; holds on any axis "
         "because R's columns sum to 1; independent of every cascade parameter")
    _row("ratio_to_Phase12_CEvNS_total", "natural",
         bound["bound_counts_kg_day"] / PHASE12_CEVNS_TOTAL, "dimensionless",
         "bound / 118.73", "RIGOROUS_BOUND",
         "Phase-12 CEvNS total on the reconstructed axis; the bound is a TOTAL "
         "reaction rate, so this compares totals, not a spectrum to a spectrum")
    for A in sorted(ceil["per_isotope"]):
        v = ceil["per_isotope"][A]
        _row("single_gamma_ceiling", f"{A}Ge", v["T_max_eV"], "eV",
             "T_max = Q_cap^2/(2 M_(A+1) c^2)", "RIGOROUS_BOUND",
             f"Q_cap = {v['Q_cap_eV']:.1f} eV READ from the ENDF MF=3 MT=102 QM field; "
             f"recoiling body is {v['product']}. A CEILING, never the cascade answer")
    _row("multiplicity_N_mean", "any", None, "eV", "<T> = T_max / N (N SYMBOLIC)",
         "CONDITIONAL_ESTIMATE",
         "equal-energy isotropic cascade of multiplicity N. N is NOT assigned a "
         "value here; assigning one from recollection is fp-assumed-multiplicity")
    _row("sum_of_squares_vs_square_of_sum", "70Ge", demo["ratio_ss_over_sq"],
         "dimensionless", "Sum(E^2) / (Sum E)^2", "CONDITIONAL_ESTIMATE",
         f"explicit 3-gamma partition {demo['partition_eV']} eV summing to Q_cap; "
         "shows with numbers why the single-gamma ceiling overstates a real cascade")
    for A in sorted(egaf):
        d = egaf[A]
        if d.get("completeness") is None or d["completeness"] > 1.0:
            _row("egaf_cascade_completeness", f"{A}Ge",
                 d.get("completeness"), "dimensionless", "Sum(I E) / Q_cap",
                 "CONDITIONAL_ESTIMATE",
                 "EXCLUDED: EGAF sigma_0 disagrees with the ENDF/ACE thermal cross "
                 "section for this isotope and the completeness exceeds 1")
            continue
        _row("egaf_cascade_completeness", f"{A}Ge", d["completeness"],
             "dimensionless", "Sum(I E) / Q_cap", "CONDITIONAL_ESTIMATE",
             f"{d['n_gammas']} observed gammas, EGAF dataset only; the deficit is "
             "unobserved quasi-continuum strength")
        _row("egaf_mean_recoil_observed", f"{A}Ge", d["mean_T_from_observed_eV"],
             "eV", "<T> = Sum(I E^2)/(2 M c^2)", "CONDITIONAL_ESTIMATE",
             "isotropic-cascade MEAN over the OBSERVED lines only. A MEAN, not a "
             "spectrum, and the in-RoI fraction is not determined by it")
        _row("egaf_mean_recoil_upper_bracket", f"{A}Ge",
             d["mean_T_upper_bracket_eV"], "eV",
             "<T> <= [Sum(I E^2) + E_miss * Q] / (2 M c^2)", "RIGOROUS_BOUND",
             "given the observed list and energy conservation: maximising the "
             "missing Sum(I E^2) subject to Sum(I E) = E_miss and E_i <= Q puts it "
             "all at E = Q. Tighter than the single-gamma ceiling")
    _row("inelastic_reaction_rate", "natural",
         inel["total"]["rate_counts_kg_day"], "counts/kg/day",
         "R = N_Ge INT phi sigma_MT51_91 dE", "RIGOROUS_BOUND",
         "summed MT=51..91 folded over the same flux; a RATE bound, and a very "
         "loose one in the RoI because its nuclear recoils land far above it")
    for A in sorted(inel_iso):
        _row("inelastic_reaction_rate", f"{A}Ge",
             inel_iso[A]["total"]["rate_counts_kg_day"], "counts/kg/day",
             "abundance-weighted", "RIGOROUS_BOUND",
             "contribution to the natural inelastic rate")
    _row("inelastic_nuclear_recoil_scale", "natural",
         place["nuclear_recoil_ceiling_at_mean_En_eV"], "eV",
         "f_nat x <E_n>", "CONDITIONAL_ESTIMATE",
         "elastic-kinematics ceiling at the rate-weighted mean incident energy; "
         "~3 decades ABOVE the 100 eV RoI top, which is why the rate bound is loose")
    _row("gamma_emission_recoil", "74Ge",
         place["named_levels"]["74Ge_596keV"]["gamma_recoil_eV"], "eV",
         "T = E_gamma^2/(2 M c^2), E_gamma = 596 keV", "RIGOROUS_BOUND",
         "the 74Ge 596 keV level named by ROADMAP SC5; this is the part of the "
         "inelastic channel landing NEAR the band")
    _row("gamma_emission_recoil", "72Ge",
         place["named_levels"]["72Ge_834keV"]["gamma_recoil_eV"], "eV",
         "T = E_gamma^2/(2 M c^2), E_gamma = 834 keV", "RIGOROUS_BOUND",
         "the 72Ge 834 keV level named by ROADMAP SC5")

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(h) + "\n")
        fh.write("quantity,isotope,value,units,expression,evidence_class,"
                 "accuracy_label,basis\n")
        fh.write("\n".join(rows) + "\n")
    return path
