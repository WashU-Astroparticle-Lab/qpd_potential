# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
#
# Phase-6 (Plan 06-01) FOLD PIPELINE (SIMU-03).
#
# Turns the frozen DEPOSITED-energy spectra (CEvNS dR/dT, muon dR/dE_dep,
# Compton dR/dE_dep) into RECONSTRUCTED-energy spectra dR/dE_rec by folding them
# through the Phase-5 non-paralyzable response matrix R(E_rec | E_dep), per design
# (Ta->Al, Al->Hf).  R (161 E_rec x 584 E_dep, each column sums to 1) and the
# shared E_dep / E_rec grids are REUSED from artifacts/stage1/response_matrix_*.npz
# -- the response chain is NOT re-implemented here.
#
# METHOD (deterministic, counts-conserving):
#   * CEvNS rebin: cevns_dRdT.csv lives on a 320-pt recoil grid (5-3200 eV_nr),
#     NOT the shared 584-bin E_dep grid.  It is rebinned onto the shared grid by
#     integrating dR/dT over each shared E_dep bin using a piecewise LOG-LOG
#     power-law interpolant (exact for a steeply-falling spectrum; NOT linear-
#     space interpolation).  This conserves counts: total rebinned counts equal
#     the trapezoidal integral of dR/dT over 5-3200 eV to <1%, and the above-50-eV
#     integral matches the frozen 67.752 counts/kg/day header to <2%.
#   * CEvNS LOW EDGE (5 - 10.14 eV, below the shared grid floor): NOT dropped
#     (fp-drop-lowE-cevns).  These deposits sit far below the crossover onset
#     (~52.9 eV Ta->Al / ~32.1 eV Al->Hf), so the response is EXACTLY LINEAR there:
#     they are reconstructed via E_rec = 0.5 * E_dep and carried into the matching
#     E_rec bins.  (The Phase-5 MC response median at the lowest bins is ~0.483,
#     not exactly 0.5 -- a ~3% calibration nuance; 0.5 is used for this sub-floor
#     band, noted in the landing report.)
#   * Fold: N_dep[i] = dRdEdep[i] * dE_dep[i] (dE_dep from npz E_dep_edges_eV),
#     N_rec[j] = sum_i R[j,i] * N_dep[i], dR/dE_rec[j] = N_rec[j] / dE_rec[j].
#     Because each R column sums to 1, sum_j N_rec = sum_i N_dep EXACTLY (counts
#     conserved per channel per design).
#   * Bands: the CEvNS 1-sigma flux band (dRdT_band_1sigma) is folded the same
#     way; the Compton factor-2 site-flux band is 0.5x / 2x the Compton spectrum
#     folded the same way; the muon ~30% normalization is carried as a +/-30%
#     band on the folded muon spectrum (normalization, not a shape change).
#
# CANONICAL VARIANT: only R_non_paralyzable is folded (CONVENTIONS Section F,
# RESOLVED 2026-07-21 non-paralyzable project-wide).  R_paralyzable is a retained
# sensitivity, NEVER the deliverable (fp-paralyzable-swap).
#
# The output axis is RECONSTRUCTED energy E_rec, never deposited energy
# (fp-deposited-only): the muon deposits (MeV - 197 MeV) reconstruct to a bounded
# plateau of TENS OF keV (saturation), not to ~0.5*E_dep.
#
# UNITS (CONVENTIONS Section A): energy eV internal, keV on the I/O axes; rate
# counts/kg/day/keV.

from __future__ import annotations

import os
from typing import Optional

import numpy as np

from . import ia_broadening
from . import interp_guard as ig
from . import response_matrix as rm

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
_ARTIFACT_DIR = os.path.join(_PROJECT_ROOT, "artifacts", "stage1")
_DATA_DIR = os.path.join(_PROJECT_ROOT, "data")

CEVNS_CSV = os.path.join(_ARTIFACT_DIR, "cevns_dRdT.csv")
MUON_CSV = os.path.join(_DATA_DIR, "muon_dRdEdep.csv")
COMPTON_CSV = os.path.join(_DATA_DIR, "compton_dRdEdep.csv")

RECON_FILE = {
    "Ta->Al": "reconstructed_spectra_TaAl.csv",
    "Al->Hf": "reconstructed_spectra_AlHf.csv",
}

# Low-E linear-regime reconstruction slope dE_rec/dE_dep (CONVENTIONS B/E).
LOW_E_SLOPE = 0.5
# Muon absolute-normalization band (Phase-4 VALD-02: ~15% vs PDG, carried ~30%).
MUON_NORM_BAND = 0.30
# Compton site-flux band (Phase-4 VALD-03: documented factor-2 site dependence).
COMPTON_SITE_FACTOR = 2.0


# --------------------------------------------------------------------------- #
# CSV readers                                                                  #
# --------------------------------------------------------------------------- #


def _read_numeric_rows(path: str) -> list[list[float]]:
    rows = []
    with open(path) as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            toks = s.split(",")
            try:
                rows.append([float(t) for t in toks])
            except ValueError:
                continue  # column-name header row
    return rows


def read_cevns(path: str = CEVNS_CSV) -> dict:
    """CEvNS dR/dT on the 320-pt recoil grid.

    Returns T_eV (ascending), dRdT_total, dRdT_band_1sigma (counts/kg/day/keV).
    Uses the pre-summed `dRdT_total` column (col 6) -- isotopes NOT re-lumped.
    """
    rows = np.asarray(_read_numeric_rows(path), dtype=float)
    T = rows[:, 0]
    order = np.argsort(T)
    return {
        "T_eV": T[order],
        "dRdT_total": rows[order, 6],
        "dRdT_band_1sigma": rows[order, 7],
    }


def read_channel_dRdEdep(path: str) -> dict:
    """A shared-grid deposited-energy channel (muon / Compton).

    Returns E_dep_eV (centers, ascending) and dRdEdep (counts/kg/day/keV).
    """
    rows = np.asarray(_read_numeric_rows(path), dtype=float)
    E_keV = rows[:, 0]
    order = np.argsort(E_keV)
    return {"E_dep_eV": E_keV[order] * 1.0e3, "dRdEdep": rows[order, 1]}


# --------------------------------------------------------------------------- #
# Counts-conserving log-log rebin                                             #
# --------------------------------------------------------------------------- #


def _loglog_segment_integral(
    T1: float, T2: float, y1: float, y2: float, a: float, b: float
) -> float:
    """Integral of the interpolant of (T1,y1)-(T2,y2) over [a,b] subset [T1,T2].

    Interpolation is a power law in log-log space (y = A T^p) when both endpoints
    are positive; otherwise it falls back to a linear interpolant.  Returns the
    integral in the native T units (eV here) times y units (per keV) -- the caller
    converts the eV integral to keV counts.
    """
    if b <= a:
        return 0.0
    if y1 <= 0.0 or y2 <= 0.0:
        slope = (y2 - y1) / (T2 - T1)
        ya = y1 + slope * (a - T1)
        yb = y1 + slope * (b - T1)
        return 0.5 * (ya + yb) * (b - a)
    p = np.log(y2 / y1) / np.log(T2 / T1)
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        A = y1 / (T1 ** p)
        if abs(p + 1.0) < 1e-9:
            return A * np.log(b / a)
        val = A * (b ** (p + 1.0) - a ** (p + 1.0)) / (p + 1.0)
    if not np.isfinite(val):
        # NUMERICAL FALLBACK, added by plan 11-04. A power law cannot represent a
        # GAUSSIAN tail: past a spectrum's kinematic endpoint the IA-broadened rate
        # falls super-exponentially, giving |p| ~ 400 and T1**p under/overflowing, so
        # A becomes inf and inf*0 becomes nan. Fall back to the same linear rule this
        # function already uses for non-positive endpoints. Unreachable for every
        # segment of the unbroadened v1.0 table -- switch-off bit-identity is tested.
        slope = (y2 - y1) / (T2 - T1)
        ya = y1 + slope * (a - T1)
        yb = y1 + slope * (b - T1)
        return 0.5 * (ya + yb) * (b - a)
    return val


def rebin_counts(T: np.ndarray, y: np.ndarray, edges: np.ndarray) -> np.ndarray:
    """Counts/kg/day per target bin defined by `edges` (eV), from dR/dT `y`
    (per keV) sampled at `T` (eV), via the piecewise log-log integral.

    Support is [T[0], T[-1]]; target bins outside that range get zero.  Counts are
    conserved: sum over any set of contiguous target bins equals the log-log
    integral of dR/dT over the covered T range.
    """
    T = np.asarray(T, float)
    y = np.asarray(y, float)
    edges = np.asarray(edges, float)
    counts = np.zeros(edges.size - 1, dtype=float)
    Tmin, Tmax = T[0], T[-1]
    for k in range(edges.size - 1):
        lo = max(edges[k], Tmin)
        hi = min(edges[k + 1], Tmax)
        if hi <= lo:
            continue
        i0 = int(np.searchsorted(T, lo, side="right") - 1)
        i1 = int(np.searchsorted(T, hi, side="left"))
        acc = 0.0
        for i in range(max(i0, 0), min(i1, T.size - 1)):
            a = max(lo, T[i])
            b = min(hi, T[i + 1])
            if b > a:
                acc += _loglog_segment_integral(T[i], T[i + 1], y[i], y[i + 1], a, b)
        counts[k] = acc / 1.0e3  # eV integral of a per-keV rate -> counts
    return counts


def rebin_cevns_to_edep_grid(
    E_dep_edges_eV: np.ndarray, path: str = CEVNS_CSV, *,
    broaden: bool | None = None, omega_bar_eV: float | None = None
) -> dict:
    """Rebin CEvNS dR/dT onto the shared E_dep grid, conserving counts, and split
    off the sub-floor 5 - E_dep_edges_eV[0] low edge (reconstructed via
    E_rec = 0.5 * E_dep, NOT dropped).

    Returns a dict with:
      counts        : counts/kg/day per shared E_dep bin (>= floor)
      counts_band   : same for the 1-sigma flux band
      dRdEdep       : counts / dE_dep(keV)  (dR/dE_dep on the shared grid)
      dRdEdep_band  : same for the band
      low_counts    : counts/kg/day per sub-floor sub-bin (5 -> floor)
      low_band      : same for the band
      low_Erec_eV   : E_rec = 0.5 * E_dep of each sub-floor sub-bin
      floor_eV, T_min_eV, T_max_eV
    """
    c = read_cevns(path)
    T, y, band = c["T_eV"], c["dRdT_total"], c["dRdT_band_1sigma"]
    floor = float(E_dep_edges_eV[0])

    # ------------------------------------------------------------------ #
    # Plan 11-04 (CALC-15): impulse-approximation quantum broadening.     #
    # Applied HERE, on the RECOIL axis, strictly upstream of every        #
    # rebin_counts call below and therefore upstream of the deposit grid  #
    # and of R(E_rec|E_dep).  The IA width is a property of the nuclear   #
    # recoil, not of the sensor; applying it downstream would double-count#
    # the response and mislabel a nuclear effect as a detector effect     #
    # (fp-broadening-after-response).                                     #
    #                                                                     #
    # DEFAULT OFF (ia_broadening.BROADENING_DEFAULT), following the       #
    # Phase-10 precedent that left shared_energy_grid defaulting to v1.0. #
    # With broaden=False this function is bit-identical to v1.0.          #
    # Nothing here multiplies the rate by exp(-2W) (fp-dw-suppression).   #
    # ------------------------------------------------------------------ #
    if broaden is None:
        broaden = ia_broadening.BROADENING_DEFAULT
    broadening_leakage = None
    if broaden:
        T, y, band, broadening_leakage = ia_broadening.broaden_native_spectrum(
            T, y, band, omega_bar_eV=omega_bar_eV)

    counts = rebin_counts(T, y, E_dep_edges_eV)
    counts_band = rebin_counts(T, band, E_dep_edges_eV)
    dE_dep_keV = np.diff(E_dep_edges_eV) / 1.0e3
    dRdEdep = counts / dE_dep_keV
    dRdEdep_band = counts_band / dE_dep_keV

    # Sub-floor low edge [T[0], floor]: sub-bin on the native knots so the log-log
    # integral is exact, then map each sub-bin to E_rec = 0.5 * E_dep.
    inner = T[(T > T[0]) & (T < floor)]
    sub_edges = np.concatenate([[T[0]], inner, [floor]])
    low_counts = rebin_counts(T, y, sub_edges)
    low_band = rebin_counts(T, band, sub_edges)
    low_centers = np.sqrt(sub_edges[:-1] * sub_edges[1:])
    low_Erec = LOW_E_SLOPE * low_centers

    return {
        "counts": counts,
        "counts_band": counts_band,
        "dRdEdep": dRdEdep,
        "dRdEdep_band": dRdEdep_band,
        "low_counts": low_counts,
        "low_band": low_band,
        "low_Erec_eV": low_Erec,
        "broadening_applied": bool(broaden),
        "broadening_leakage": broadening_leakage,
        "floor_eV": floor,
        "T_min_eV": float(T[0]),
        "T_max_eV": float(T[-1]),
    }


# --------------------------------------------------------------------------- #
# Fold                                                                         #
# --------------------------------------------------------------------------- #


def dep_counts_from_dRdEdep(dRdEdep: np.ndarray, E_dep_edges_eV: np.ndarray) -> np.ndarray:
    """N_dep[i] = dRdEdep[i] * dE_dep[i], dE_dep from the npz edges (eV -> keV)."""
    dE_dep_keV = np.diff(E_dep_edges_eV) / 1.0e3
    return np.asarray(dRdEdep, float) * dE_dep_keV


def fold_counts(N_dep: np.ndarray, R: np.ndarray) -> np.ndarray:
    """N_rec[j] = sum_i R[j,i] N_dep[i].  R columns sum to 1 -> counts conserved."""
    return R @ np.asarray(N_dep, float)


def _add_low_edge(N_rec: np.ndarray, low_counts: np.ndarray,
                  low_Erec_eV: np.ndarray, E_rec_edges_eV: np.ndarray) -> np.ndarray:
    """Deposit the linear-regime low-edge counts into the matching E_rec bins."""
    out = N_rec.copy()
    idx = np.searchsorted(E_rec_edges_eV, low_Erec_eV, side="right") - 1
    idx = np.clip(idx, 0, E_rec_edges_eV.size - 2)
    np.add.at(out, idx, low_counts)
    return out


def load_design(design: str) -> dict:
    fn = os.path.join(_ARTIFACT_DIR, rm.DESIGN_FILE[design])
    if not os.path.exists(fn):
        raise FileNotFoundError(f"response matrix not built: {fn}")
    return dict(np.load(fn, allow_pickle=True))


def run_fold(design: str, write: bool = True, out_dir: str = _ARTIFACT_DIR) -> dict:
    """Fold all three channels through R_non_paralyzable for one design.

    Returns per-channel reconstructed spectra (dR/dE_rec, counts/kg/day/keV) plus
    bands and counts-conservation diagnostics, and (optionally) writes the CSV.
    """
    d = load_design(design)
    R = d["R_non_paralyzable"]
    E_dep_edges = d["E_dep_edges_eV"]
    E_dep_centers = d["E_dep_centers_eV"]
    E_rec_edges = d["E_rec_edges_eV"]
    E_rec_centers = d["E_rec_centers_eV"]
    dE_rec_keV = np.diff(E_rec_edges) / 1.0e3

    # --- CEvNS ---------------------------------------------------------------
    reb = rebin_cevns_to_edep_grid(E_dep_edges, CEVNS_CSV)
    N_dep_cevns = reb["counts"]
    N_dep_cevns_band = reb["counts_band"]
    N_rec_cevns = _add_low_edge(
        fold_counts(N_dep_cevns, R), reb["low_counts"], reb["low_Erec_eV"], E_rec_edges
    )
    N_rec_cevns_band = _add_low_edge(
        fold_counts(N_dep_cevns_band, R), reb["low_band"], reb["low_Erec_eV"], E_rec_edges
    )
    cevns_total_dep = float(N_dep_cevns.sum() + reb["low_counts"].sum())

    # --- muon / Compton (already on the shared grid) -------------------------
    muon = read_channel_dRdEdep(MUON_CSV)
    compton = read_channel_dRdEdep(COMPTON_CSV)
    for name, ch in (("muon", muon), ("compton", compton)):
        rel = np.max(np.abs(ch["E_dep_eV"] - E_dep_centers) / E_dep_centers)
        if rel > 1e-6:
            raise ValueError(
                f"{name} E_dep grid does not match npz E_dep centers (max rel {rel:.2e})"
            )
    N_dep_muon = dep_counts_from_dRdEdep(muon["dRdEdep"], E_dep_edges)
    N_dep_compton = dep_counts_from_dRdEdep(compton["dRdEdep"], E_dep_edges)
    N_rec_muon = fold_counts(N_dep_muon, R)
    N_rec_compton = fold_counts(N_dep_compton, R)

    # --- differential reconstructed spectra ----------------------------------
    def diff(nrec):
        return nrec / dE_rec_keV

    cevns = diff(N_rec_cevns)
    cevns_band = diff(N_rec_cevns_band)
    muon_d = diff(N_rec_muon)
    compton_d = diff(N_rec_compton)

    # Bands: CEvNS flux band folded; Compton factor-2 site band; muon +/-30% norm.
    cevns_lo = np.maximum(cevns - cevns_band, 0.0)
    cevns_hi = cevns + cevns_band
    muon_lo = (1.0 - MUON_NORM_BAND) * muon_d
    muon_hi = (1.0 + MUON_NORM_BAND) * muon_d
    compton_lo = compton_d / COMPTON_SITE_FACTOR
    compton_hi = compton_d * COMPTON_SITE_FACTOR
    total = cevns + muon_d + compton_d

    result = {
        "design": design,
        "E_rec_centers_eV": E_rec_centers,
        "E_rec_edges_eV": E_rec_edges,
        "cevns_dRdErec": cevns,
        "cevns_band_lo": cevns_lo,
        "cevns_band_hi": cevns_hi,
        "muon_dRdErec": muon_d,
        "muon_band_lo": muon_lo,
        "muon_band_hi": muon_hi,
        "compton_dRdErec": compton_d,
        "compton_band_lo": compton_lo,
        "compton_band_hi": compton_hi,
        "total_dRdErec": total,
        # diagnostics (counts/kg/day)
        "N_rec_cevns": N_rec_cevns,
        "N_rec_muon": N_rec_muon,
        "N_rec_compton": N_rec_compton,
        "N_dep_cevns_total": cevns_total_dep,
        "N_dep_muon_total": float(N_dep_muon.sum()),
        "N_dep_compton_total": float(N_dep_compton.sum()),
        "rebin": reb,
    }
    if write:
        result["_path"] = write_reconstructed_csv(result, out_dir)
    return result


# --------------------------------------------------------------------------- #
# CSV export (drops the [0, 1e-3 eV) underflow catch-bin from the differential  #
# spectrum; its counts are ~0 and its "center" is not a physical E_rec)         #
# --------------------------------------------------------------------------- #

_CSV_COLUMNS = [
    "E_rec_keV",
    "cevns_dRdErec", "cevns_band_lo", "cevns_band_hi",
    "muon_dRdErec", "muon_band_lo", "muon_band_hi",
    "compton_dRdErec", "compton_band_lo", "compton_band_hi",
    "total_dRdErec",
]


def write_reconstructed_csv(result: dict, out_dir: str = _ARTIFACT_DIR) -> str:
    design = result["design"]
    E_rec_keV = result["E_rec_centers_eV"] / 1.0e3
    # bin 0 is the [0, 1e-3 eV) underflow catch-bin -> not a physical differential
    # bin; drop it from the spectrum (its counts are negligible, see landing report).
    sl = slice(1, None)
    cols = {
        "E_rec_keV": E_rec_keV[sl],
        "cevns_dRdErec": result["cevns_dRdErec"][sl],
        "cevns_band_lo": result["cevns_band_lo"][sl],
        "cevns_band_hi": result["cevns_band_hi"][sl],
        "muon_dRdErec": result["muon_dRdErec"][sl],
        "muon_band_lo": result["muon_band_lo"][sl],
        "muon_band_hi": result["muon_band_hi"][sl],
        "compton_dRdErec": result["compton_dRdErec"][sl],
        "compton_band_lo": result["compton_band_lo"][sl],
        "compton_band_hi": result["compton_band_hi"][sl],
        "total_dRdErec": result["total_dRdErec"][sl],
    }
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, RECON_FILE[design])
    header = (
        f"# QPD Phase-6 Plan 06-01 -- reconstructed-energy spectra dR/dE_rec, design {design}.\n"
        f"# Source R: artifacts/stage1/{rm.DESIGN_FILE[design]}, key R_non_paralyzable\n"
        f"#   (CONVENTIONS Section F RESOLVED non-paralyzable; paralyzable is a sensitivity only).\n"
        f"# Axis: RECONSTRUCTED energy E_rec (from npz E_rec grid), NOT deposited energy.\n"
        f"# Grid: shared 584-bin E_dep (10.14 eV -> 197 MeV) folded to 161 E_rec bins;\n"
        f"#   the [0, 1e-3 eV) underflow catch-bin is omitted below.\n"
        f"# CEvNS rebinned onto the shared E_dep grid conserving counts; the 5-10.14 eV\n"
        f"#   sub-floor low edge is reconstructed via E_rec = 0.5*E_dep (retained, not dropped).\n"
        f"# Bands: cevns = folded 1-sigma flux band; muon = +/-{int(MUON_NORM_BAND*100)}% normalization;\n"
        f"#   compton = factor-{int(COMPTON_SITE_FACTOR)} site-flux (0.5x / 2x).\n"
        f"# Units: counts/kg/day/keV (per-kg normalization; CONVENTIONS A).\n"
    )
    with open(path, "w") as fh:
        fh.write(header)
        fh.write(",".join(_CSV_COLUMNS) + "\n")
        n = cols["E_rec_keV"].size
        for i in range(n):
            fh.write(",".join(f"{cols[c][i]:.6e}" for c in _CSV_COLUMNS) + "\n")
    return path


# --------------------------------------------------------------------------- #
# Counts-conservation diagnostics                                             #
# --------------------------------------------------------------------------- #


def counts_conservation(result: dict) -> dict:
    """Per-channel |sum N_rec - sum N_dep| / sum N_dep for a run_fold result."""
    out = {}
    for ch in ("cevns", "muon", "compton"):
        n_rec = result[f"N_rec_{ch}"].sum()
        n_dep = result[f"N_dep_{ch}_total"]
        out[ch] = {
            "N_rec": float(n_rec),
            "N_dep": float(n_dep),
            "rel": float(abs(n_rec - n_dep) / n_dep) if n_dep > 0 else float("nan"),
        }
    return out


# --------------------------------------------------------------------------- #
# Landing report (Task 3): where each reconstructed spectrum sits vs threshold  #
# --------------------------------------------------------------------------- #

_REF_THRESHOLDS_eV = (10.0, 50.0, 100.0)


def _peak_Erec_keV(N_rec: np.ndarray, E_rec_centers_eV: np.ndarray) -> float:
    j = int(np.argmax(N_rec[1:]) + 1)  # skip underflow bin
    return float(E_rec_centers_eV[j] / 1.0e3)


def landing_report(designs: Optional[tuple] = None) -> dict:
    """Assemble the reconstructed-energy landing + report-don't-force verdict.

    For each channel x design: integrated reconstructed rate (counts/kg/day),
    peak E_rec, and the fraction of counts below the 10/50/100 eV E_rec reference
    thresholds.  Applies the ROADMAP stop condition: a channel entirely below the
    reference threshold for BOTH designs is surfaced (not forced).
    """
    if designs is None:
        designs = tuple(rm.DESIGN_FILE.keys())
    report = {"designs": {}, "stop_condition": {}}
    below = {ch: {thr: [] for thr in _REF_THRESHOLDS_eV} for ch in ("cevns", "muon", "compton")}
    for design in designs:
        res = run_fold(design, write=False)
        centers = res["E_rec_centers_eV"]
        edges = res["E_rec_edges_eV"]
        entry = {}
        for ch in ("cevns", "muon", "compton"):
            n_rec = res[f"N_rec_{ch}"]
            tot = float(n_rec.sum())
            peak = _peak_Erec_keV(n_rec, centers)
            frac = {}
            for thr in _REF_THRESHOLDS_eV:
                mask = edges[1:] <= thr  # bin fully below thr (upper edge <= thr)
                frac[thr] = float(n_rec[mask].sum() / tot) if tot > 0 else float("nan")
                below[ch][thr].append(frac[thr])
            entry[ch] = {
                "integrated_rate_cts_per_kg_day": tot,
                "peak_Erec_keV": peak,
                "frac_below_eV": frac,
            }
        report["designs"][design] = entry
    # stop condition: entirely below a threshold for BOTH designs
    for ch in ("cevns", "muon", "compton"):
        verdict = {}
        for thr in _REF_THRESHOLDS_eV:
            both = below[ch][thr]
            verdict[thr] = bool(len(both) == len(designs) and all(f > 0.999 for f in both))
        report["stop_condition"][ch] = verdict
    return report


# --------------------------------------------------------------------------- #
# Deliverable figure (Plan 06-02, deliv-fig-spectra)                           #
#                                                                              #
# Renders the RECONSTRUCTED-energy spectra dR/dE_rec vs E_rec for all three    #
# channels (CEvNS, muon, Compton) and BOTH designs (Ta->Al, Al->Hf) in         #
# counts/kg/day/keV, from the Plan 06-01 reconstructed_spectra_*.csv, and      #
# reuses the Phase-5 npz mapping curve (E_rec_median_non_paralyzable_eV vs     #
# E_dep_centers_eV) for the true->reconstructed panel.  The saturation region  #
# is delimited on the E_rec axis (fp-no-saturation-mark) and the x-axis is     #
# RECONSTRUCTED energy, never deposited (fp-deposited-only).  Only the         #
# non-paralyzable deliverable is drawn (fp-paralyzable-swap).                   #
# --------------------------------------------------------------------------- #

SPECTRA_FIG_FILE = "reconstructed_energy_spectra.pdf"

# Reconstructed-energy landing peaks (Plan 06-01 landing_report), keV.
_MUON_PEAK_keV = {"Ta->Al": 18.8, "Al->Hf": 15.0}

_CH_STYLE = {
    "cevns": {"color": "#1f77b4", "label": "CEvNS (reactor)"},
    "muon": {"color": "#d62728", "label": "cosmic muon"},
    "compton": {"color": "#2ca02c", "label": "environmental $\\gamma$ (Compton)"},
}
_DESIGN_LS = {"Ta->Al": "-", "Al->Hf": "--"}


def _read_recon_csv(design: str, art_dir: str = _ARTIFACT_DIR) -> dict:
    """Load a Plan 06-01 reconstructed_spectra_*.csv into named arrays."""
    path = os.path.join(art_dir, RECON_FILE[design])
    rows = np.asarray(_read_numeric_rows(path), dtype=float)
    keys = [
        "E_rec_keV",
        "cevns_dRdErec", "cevns_band_lo", "cevns_band_hi",
        "muon_dRdErec", "muon_band_lo", "muon_band_hi",
        "compton_dRdErec", "compton_band_lo", "compton_band_hi",
        "total_dRdErec",
    ]
    return {k: rows[:, i] for i, k in enumerate(keys)}


def _erec_of_edep(E_dep_eV, E_dep_centers, E_rec_median,
                  table: str = "response matrix npz :: E_dep_centers_eV"):
    """Interpolate E_rec (eV) at a deposited energy via the Phase-5 median
    non-paralyzable mapping curve, in log-log space.

    PLAN 10-01 -- THE LOAD-BEARING GUARD OF THE PHASE. The abscissa floor is the
    response matrix's first deposit centre, 10.144970 eV for the archived v1.0
    matrices. Before this guard, ``np.interp`` CLAMPED below that floor, so
    asking for the reconstructed energy of a 0.1 eV deposit returned
    **4.899066 eV** -- the E_rec of a 10.14 eV deposit -- a finite, plausible,
    completely wrong answer overstating E_rec by a factor of ~49, with no error
    and no NaN to notice. The same 4.899066 eV came back for 0.5 eV, 1 eV, and
    every other sub-floor deposit: a flat, invented plateau exactly where plan
    10-03 extends the axis. It now raises.

    The declared evaluation domain is exactly the span of ``E_dep_centers``:
    there is no witness for any extension, because no v1.0 anchor evaluates this
    curve below 10.14 eV -- the retracted "nothing below 10 eV" display rule is
    precisely why.
    """
    centers = np.asarray(E_dep_centers, float)
    dom = ig.Domain(
        quantity="E_rec(E_dep) Phase-5 median mapping curve",
        lo=float(centers.min()), hi=float(centers.max()), units="eV",
        table=table,
        table_lo=float(centers.min()), table_hi=float(centers.max()),
        note="np.interp previously clamped to E_rec(first centre) below the floor.",
    )
    ig.check_domain(E_dep_eV, dom)
    lx = np.log(np.asarray(E_dep_eV, float))
    return np.exp(np.interp(lx, np.log(centers), np.log(E_rec_median)))


def _mask_pos(x, y):
    """Return (x, y) keeping only strictly-positive y (log-axis safe)."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    m = y > 0.0
    return x[m], y[m]


def make_spectra_figure(
    out_path: Optional[str] = None,
    art_dir: str = _ARTIFACT_DIR,
    designs: tuple = ("Ta->Al", "Al->Hf"),
) -> str:
    """Render deliv-fig-spectra: reconstructed-energy spectra (all 3 channels,
    both designs) + saturation delimitation + true->reconstructed mapping panel.

    Reads the committed reconstructed_spectra_*.csv (Plan 06-01) and the Phase-5
    response_matrix_*.npz mapping arrays; does NOT re-run the fold.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    if out_path is None:
        out_path = os.path.join(art_dir, SPECTRA_FIG_FILE)

    spectra = {d: _read_recon_csv(d, art_dir) for d in designs}
    npz = {d: dict(np.load(os.path.join(art_dir, rm.DESIGN_FILE[d]))) for d in designs}

    # Deposited (true, pre-reconstruction) spectra dR/dE_dep vs E_dep [keV].
    # These are design-independent (the deposit precedes the QPD response), and are
    # overlaid (dashed) on top of the reconstructed spectra to expose the response:
    # the MeV-scale muon deposits are compressed onto the tens-of-keV reconstructed
    # pile-up, while the tens-of-eV CEvNS deposits map ~linearly.
    _cev = read_cevns()
    _mu = read_channel_dRdEdep(MUON_CSV)
    _cp = read_channel_dRdEdep(COMPTON_CSV)
    deposited = {
        "cevns": (_cev["T_eV"] / 1e3, _cev["dRdT_total"]),
        "muon": (_mu["E_dep_eV"] / 1e3, _mu["dRdEdep"]),
        "compton": (_cp["E_dep_eV"] / 1e3, _cp["dRdEdep"]),
    }

    # E_rec image of the two saturation E_dep scales, per design.
    sat = {}
    for d in designs:
        z = npz[d]
        cen = z["E_dep_centers_eV"]
        med = z["E_rec_median_non_paralyzable_eV"]
        onset_ed = float(z["saturation_onset_Edep_eV"])
        plateau_ed = float(z["whole_array_plateau_Edep_eV"])
        sat[d] = {
            "onset_Erec_keV": float(_erec_of_edep(onset_ed, cen, med)) / 1e3,
            "plateau_Erec_keV": float(_erec_of_edep(plateau_ed, cen, med)) / 1e3,
            "onset_Edep_eV": onset_ed,
            "plateau_Edep_eV": plateau_ed,
            "cen": cen,
            "med": med,
        }

    fig, axes = plt.subplots(1, len(designs), figsize=(11.0, 4.7))
    if len(designs) == 1:
        axes = [axes]

    # ---- Panels A/B: spectra per design ------------------------------------ #
    ymin, ymax = 1e-3, 1e9
    # RETRACTED 2026-07-22 (user decision; ROADMAP Phase 10, plan 10-05). The former
    # project rule -- "never display below 10 eV" -- is HISTORY, not physics, and must
    # not be restated as a live rule. Spectra now run down to 100 meV.
    #
    # The 1e-2 keV low limit BELOW IS NOT THAT RULE. It is the support floor of the
    # V1.0 ARTIFACTS this v1.0 figure draws: artifacts/stage1/reconstructed_spectra_*.csv
    # and the frozen response matrices have no data below 10.14 eV, and plotting below a
    # table's own floor is silent extrapolation (plan 10-05 disposition register,
    # fp-silent-carry). Phases 12-15 own the v2.0 figures on the extended axis; below
    # trigger.SUBEV_REGIME_BOUNDARY_eV = 1 eV the reported observable there is the
    # trigger probability, not dR/dE_rec.
    #
    # The high end is extended to ~300 MeV so the deposited (true) muon spectrum, which
    # reaches the ~197 MeV endpoint, is visible alongside the reconstructed spectra.
    xmin, xmax = 1e-2, 3e5  # keV
    for col, d in enumerate(designs):
        ax = axes[col]
        s = spectra[d]
        E = s["E_rec_keV"]
        # saturation shading, capped at the top of the RECONSTRUCTED range (no
        # reconstructed events land beyond ~35 keV; the far-right axis is the
        # deposited-only region, which must not read as reconstructed-saturated).
        sat_xmax = 5e1  # keV
        o = sat[d]["onset_Erec_keV"]
        p = sat[d]["plateau_Erec_keV"]
        ax.axvspan(o, sat_xmax, color="0.86", zorder=0)
        ax.axvspan(p, sat_xmax, color="0.72", zorder=0)
        mu_peak = _MUON_PEAK_keV[d]
        ax.axvline(mu_peak, color="#d62728", ls=":", lw=1.3, zorder=1)
        # bands
        xb, lo = _mask_pos(E, s["cevns_band_lo"])
        _, hi = _mask_pos(E, s["cevns_band_hi"])
        if xb.size:
            ax.fill_between(xb, lo, hi, color=_CH_STYLE["cevns"]["color"],
                            alpha=0.22, lw=0, zorder=2)
        xb, lo = _mask_pos(E, s["compton_band_lo"])
        _, hi = _mask_pos(E, s["compton_band_hi"])
        if xb.size:
            ax.fill_between(xb, lo, hi, color=_CH_STYLE["compton"]["color"],
                            alpha=0.18, lw=0, zorder=2)
        xb, lo = _mask_pos(E, s["muon_band_lo"])
        _, hi = _mask_pos(E, s["muon_band_hi"])
        if xb.size:
            ax.fill_between(xb, lo, hi, color=_CH_STYLE["muon"]["color"],
                            alpha=0.18, lw=0, zorder=2)
        # deposited (true) spectra: dashed, same channel colors, design-independent
        for ch in ("cevns", "muon", "compton"):
            dx, dy = _mask_pos(deposited[ch][0], deposited[ch][1])
            ax.plot(dx, dy, color=_CH_STYLE[ch]["color"], lw=1.2, ls="--",
                    alpha=0.85, zorder=3)
        # reconstructed central curves (solid)
        for ch in ("cevns", "muon", "compton"):
            xx, yy = _mask_pos(E, s[f"{ch}_dRdErec"])
            ax.plot(xx, yy, color=_CH_STYLE[ch]["color"], lw=1.8,
                    label=_CH_STYLE[ch]["label"], zorder=5)
        xx, yy = _mask_pos(E, s["total_dRdErec"])
        ax.plot(xx, yy, color="0.15", lw=1.1, ls="-", label="total (reconstructed)", zorder=4)

        ax.annotate("muon pile-up\n(saturated)", xy=(mu_peak, 3e5),
                    xytext=(mu_peak * 0.14, 3e7),
                    fontsize=8.5, color="#d62728", ha="center",
                    arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.0))
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax)
        ax.set_xlabel(r"energy  [keV]   (solid: reconstructed $E_{\rm rec}$;  "
                      r"dashed: deposited $E_{\rm dep}$)")
        if col == 0:
            ax.set_ylabel(r"$dR/dE$  [counts kg$^{-1}$ day$^{-1}$ keV$^{-1}$]")
        ax.set_title(f"({'ab'[col]}) {d}   (non-paralyzable)", fontsize=11)
        ax.grid(True, which="major", alpha=0.25)
        if col == 0:
            ax.legend(loc="lower left", fontsize=8.0, framealpha=0.9, ncol=1)
        if col == len(designs) - 1:
            style_handles = [
                Line2D([0], [0], color="0.3", lw=1.8, ls="-",
                       label=r"reconstructed ($E_{\rm rec}$)"),
                Line2D([0], [0], color="0.3", lw=1.2, ls="--",
                       label=r"deposited / true ($E_{\rm dep}$)"),
            ]
            ax.legend(handles=style_handles, loc="lower left", fontsize=8.0,
                      framealpha=0.9)

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    return out_path


MAPPING_FIG_FILE = "true_reconstructed_mapping.pdf"


def make_mapping_figure(
    out_path: Optional[str] = None,
    art_dir: str = _ARTIFACT_DIR,
    designs: tuple = ("Ta->Al", "Al->Hf"),
) -> str:
    """Render the standalone true->reconstructed energy-mapping figure.

    This was formerly panel (c) of the spectra figure; it is now a separate
    figure. Shows the Phase-5 median non-paralyzable mapping E_rec(E_dep) for
    both designs, the on-spot saturation onset and whole-array plateau E_dep
    scales, and the linear-calibration reference E_rec = 0.5 E_dep. Reuses the
    committed response_matrix_*.npz mapping arrays; does NOT re-run the fold.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if out_path is None:
        out_path = os.path.join(art_dir, MAPPING_FIG_FILE)

    npz = {d: dict(np.load(os.path.join(art_dir, rm.DESIGN_FILE[d]))) for d in designs}

    fig, axm = plt.subplots(figsize=(5.4, 4.3))
    for d in designs:
        z = npz[d]
        cen = z["E_dep_centers_eV"]
        med = z["E_rec_median_non_paralyzable_eV"]
        axm.plot(cen, med, ls=_DESIGN_LS[d], color="0.15", lw=1.8,
                 label=f"{d}: median $E_{{\\rm rec}}(E_{{\\rm dep}})$")
        oe = float(z["saturation_onset_Edep_eV"])
        pe = float(z["whole_array_plateau_Edep_eV"])
        axm.axvline(oe, color="#ff7f0e", ls=_DESIGN_LS[d], lw=1.0, alpha=0.8)
        axm.axvline(pe, color="#8c564b", ls=_DESIGN_LS[d], lw=1.0, alpha=0.8)
    ed = np.array([5.0, 5e5])
    axm.plot(ed, 0.5 * ed, color="#1f77b4", ls=":", lw=1.4,
             label=r"linear calib. $E_{\rm rec}=0.5\,E_{\rm dep}$")
    axm.set_xscale("log"); axm.set_yscale("log")
    axm.set_xlim(10.0, 2.5e8); axm.set_ylim(1.0, 1e5)  # 10 eV floor (user directive)
    axm.set_xlabel(r"deposited energy $E_{\rm dep}$  [eV]")
    axm.set_ylabel(r"reconstructed $E_{\rm rec}$  [eV]")
    axm.grid(True, which="major", alpha=0.25)
    axm.legend(loc="upper left", fontsize=8.0, framealpha=0.9)
    axm.text(0.985, 0.05,
             "orange = on-spot saturation onset ($\\sim$53/32 eV)\n"
             "brown = whole-array plateau ($\\sim$18.6/11.3 keV)",
             transform=axm.transAxes, ha="right", va="bottom", fontsize=7.6,
             bbox=dict(boxstyle="round", fc="white", ec="0.7", alpha=0.9))
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    return out_path


def run_all(write: bool = True) -> dict:
    return {name: run_fold(name, write=write) for name in rm.DESIGN_FILE}


# =========================================================================== #
# Phase-12 (Plan 12-02, CALC-25): CEvNS-ONLY fold on the extended axis         #
# =========================================================================== #
#
# WHY A SEPARATE ENTRY POINT.  ``run_fold`` above folds CEvNS **and** muon **and**
# Compton, and it RAISES if the muon/Compton deposit grids do not match the
# response matrix's E_dep centres.  Those two channels are still on the 584-bin
# v1.0 axis; carrying them onto the 744-bin extended axis is **Phase 15's** job
# and Phase 12 must not pre-empt it in either direction (``fp-electron-recoil-leak``).
# So Phase 12 gets its own CEvNS-only path rather than a flag on ``run_fold``.
#
# WHAT IS SWITCHED ON HERE, DELIBERATELY.
#   * ``broaden=True`` is passed AT THIS CALL SITE.  ``ia_broadening.BROADENING_DEFAULT``
#     stays ``False`` -- a Phase-11 test asserts it, and that fail-safe is the reason
#     turning the kernel on is an explicit act rather than something every existing
#     call site inherits.
#   * ``response_matrix_{TaAl,AlHf}_ext.npz`` (744 deposit columns) is loaded, NOT the
#     v1.0 584-column matrices, which would truncate the spectrum at 10.14 eV.
#   * ``shared_energy_grid``'s default stays ``v1.0``; the extended axis arrives here
#     through the npz, not through a changed default.
#
# ORDER OF OPERATIONS (not negotiable).  IA broadening acts on the RECOIL axis inside
# ``rebin_cevns_to_edep_grid``, strictly upstream of the deposit grid and of
# R(E_rec|E_dep).  The trigger curve acts as an ANALYSIS efficiency on top of a
# quantity that already carries eps through the response chain.
#
# WHERE THE TRIGGER IS EVALUATED, AND WHY.  CONVENTIONS Section I defines
# ``P_trig(E_dep)`` and puts the regime boundary at 1.0 eV of **deposited** energy.
# It is therefore evaluated on the DEPOSIT axis, and the trigger-weighted
# reconstructed spectrum is ``R @ (P_trig(E_dep) * N_dep)`` -- i.e. exactly the
# "multiply the response matrix by the trigger curve" operation whose licence Phase 10
# established, and which is MODEL-SPECIFIC: P(no counts registered) = 2.0e-4 at 0.1 eV
# and exactly 0 at 0.5/1 eV against 1 - P_trig of 0.998/0.512/0.056, so the two do not
# double-count -- but that follows from a LINEAR yield assigning 0.018 quasiparticles
# to a sensor holding 6.89 ueV against a ~190 ueV gap, and a THRESHOLD yield model
# would invert the verdict.  Evaluating P_trig on the RECONSTRUCTED axis instead would
# silently move the 0.5 eV 50% point by the ~0.47 response slope, i.e. change
# CONVENTIONS Section I without amending it.  It is not done.

EXT_ARTIFACT_DIR = os.path.join(_PROJECT_ROOT, "artifacts", "v2.0")

EXT_DESIGN_FILE = {
    "Ta->Al": "response_matrix_TaAl_ext.npz",
    "Al->Hf": "response_matrix_AlHf_ext.npz",
}

#: The Phase-12 extended-axis UNBROADENED CEvNS recoil table (plan 12-02 Task 1).
#: It must be fed UNBROADENED: ``artifacts/v2.0/cevns_dRdT_broadened.csv`` already has
#: the kernel applied, and passing it here with ``broaden=True`` would apply the kernel
#: TWICE, widening the bottom bin by sqrt(2), with no error raised anywhere
#: (``fp-double-broadening``).
CEVNS_EXT_CSV = os.path.join(EXT_ARTIFACT_DIR, "cevns_dRdT_ext.csv")

EXT_RECON_FILE = {
    "Ta->Al": "cevns_dRdErec_ext_TaAl.csv",
    "Al->Hf": "cevns_dRdErec_ext_AlHf.csv",
}


def load_design_extended(design: str) -> dict:
    """Load the Phase-10 744-column extended response matrix for one design."""
    fn = os.path.join(EXT_ARTIFACT_DIR, EXT_DESIGN_FILE[design])
    if not os.path.exists(fn):
        raise FileNotFoundError(f"extended response matrix not built: {fn}")
    return dict(np.load(fn, allow_pickle=True))


def run_cevns_fold_extended(
    design: str, *, path: str = CEVNS_EXT_CSV, broaden: bool = True,
    omega_bar_eV: Optional[float] = None, sharpness: Optional[float] = None,
    p_trig_override: Optional[np.ndarray] = None,
) -> dict:
    """Fold the CEvNS channel ALONE through the extended response matrix.

    Parameters
    ----------
    design : "Ta->Al" or "Al->Hf".
    path : the extended-axis **UNBROADENED** dR/dT table.
    broaden : passed straight through to ``rebin_cevns_to_edep_grid``.  Phase 12 calls
        with ``True``; the global ``BROADENING_DEFAULT`` is left ``False``.
    omega_bar_eV : ``None`` -> the LOCKED harmonic VDOS mean (CONVENTIONS Section J).
        Pass ``params.OMEGA_BAR_ARITHMETIC_eV.value`` for the one-sided UPPER band.
    sharpness : trigger sharpness k; ``None`` -> ``params.TRIGGER_SHARPNESS``.
    p_trig_override : an explicit P_trig array on the deposit grid.  Its only use is
        the ``P_trig == 1`` bit-identity leg of the composition proof.

    Returns a dict carrying the deposit and reconstructed axes, the untriggered and
    trigger-weighted reconstructed spectra, the folded flux band, the broadening
    leakage record, and the full counts budget.
    """
    from . import params as _params, trigger as _trigger

    d = load_design_extended(design)
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

    # --- recoil axis -> deposit grid, with the IA kernel applied ONCE, upstream --- #
    reb = rebin_cevns_to_edep_grid(E_dep_edges, path,
                                   broaden=broaden, omega_bar_eV=omega_bar_eV)

    # FLOOR-COVERAGE CHECK, made explicit here rather than inherited.
    # ``broaden_native_spectrum(require_floor_coverage=True)`` compares the table's
    # first KNOT against the floor and would raise even for a table whose bottom bin
    # EDGE is exactly the floor -- which is the case for the Phase-11 480-bin
    # construction this plan reuses.  The physically correct statement is about the
    # bottom EDGE, so it is asserted directly.
    src = read_cevns(path)
    native_lo = float(ia_broadening.native_edges(src["T_eV"])[0])
    floor = float(E_dep_edges[0])
    if native_lo > floor * (1.0 + 1.0e-9):
        raise ValueError(
            f"the recoil table {os.path.basename(path)} has its bottom bin edge at "
            f"{native_lo!r} eV but the extended deposit grid floors at {floor!r} eV. "
            "Its support does not reach the floor; folding it would report a "
            "sub-eV spectrum the table never covered.")

    N_dep = reb["counts"]
    N_dep_band = reb["counts_band"]

    # --- the trigger, on the DEPOSIT axis (CONVENTIONS Section I) ---------------- #
    if p_trig_override is None:
        P = np.asarray(_trigger.P_trig(E_dep_centers, sharpness=sharpness), float)
    else:
        P = np.asarray(p_trig_override, float)
        if P.shape != E_dep_centers.shape:
            raise ValueError("p_trig_override must live on the deposit centres")

    # --- fold ------------------------------------------------------------------- #
    N_rec = _add_low_edge(fold_counts(N_dep, R), reb["low_counts"],
                          reb["low_Erec_eV"], E_rec_edges)
    N_rec_band = _add_low_edge(fold_counts(N_dep_band, R), reb["low_band"],
                               reb["low_Erec_eV"], E_rec_edges)
    # Trigger-weighted: the analysis efficiency is a per-event property of the
    # DEPOSIT, so it multiplies N_dep column-wise before R acts.  The low-edge band
    # is weighted at its own deposit energies for the same reason.
    low_P = np.asarray(_trigger.P_trig(reb["low_Erec_eV"] / LOW_E_SLOPE,
                                       sharpness=sharpness), float) \
        if p_trig_override is None else np.ones_like(reb["low_counts"])
    N_rec_trig = _add_low_edge(fold_counts(N_dep * P, R),
                               reb["low_counts"] * low_P,
                               reb["low_Erec_eV"], E_rec_edges)

    dRdErec = N_rec / dE_rec_keV
    dRdErec_band = N_rec_band / dE_rec_keV
    dRdErec_trig = N_rec_trig / dE_rec_keV

    # --- counts budget ---------------------------------------------------------- #
    T_src, y_src = src["T_eV"], src["dRdT_total"]
    dE_src_keV = np.diff(ia_broadening.native_edges(T_src)) / 1.0e3
    input_counts = float(np.sum(y_src * dE_src_keV))
    leak = reb["broadening_leakage"]
    leaked_below = float(leak["below_floor"]) if leak else 0.0
    leaked_below_zero = float(leak["below_zero"]) if leak else 0.0
    leaked_above = float(leak["above_top"]) if leak else 0.0
    deposit_counts = float(N_dep.sum() + reb["low_counts"].sum())
    rec_counts = float(N_rec.sum())

    budget = {
        "input_counts": input_counts,
        "leaked_below_floor": leaked_below,
        "leaked_below_zero": leaked_below_zero,   # a SUBSET of leaked_below_floor
        "leaked_above_top": leaked_above,
        "deposit_counts": deposit_counts,
        "reconstructed_counts": rec_counts,
        # The budget that must CLOSE:
        "residual_retained_plus_leaked": abs(
            deposit_counts + leaked_below + leaked_above - input_counts) / input_counts,
        # The one that must MISS -- ~49% of the bottom bin genuinely leaves the axis,
        # so a clean retained-only closure would be evidence of a hidden rescale.
        "residual_retained_only": (deposit_counts - input_counts) / input_counts,
        # R's columns sum to 1, so this is exact up to floating point.
        "residual_fold": abs(rec_counts - deposit_counts) / deposit_counts,
    }

    return {
        "design": design,
        "broadening_applied": bool(broaden),
        "broadening_default": ia_broadening.BROADENING_DEFAULT,
        "omega_bar_eV": (_params.OMEGA_BAR_eV.value if omega_bar_eV is None
                         else float(omega_bar_eV)),
        "cevns_table": path,
        "E_dep_centers_eV": E_dep_centers,
        "E_dep_edges_eV": E_dep_edges,
        "E_rec_centers_eV": E_rec_centers,
        "E_rec_edges_eV": E_rec_edges,
        "E_rec_median_of_Edep_eV": d["E_rec_median_non_paralyzable_eV"],
        "P_trig_on_Edep": P,
        "N_dep": N_dep,
        "N_rec": N_rec,
        "N_rec_trigger": N_rec_trig,
        "dRdEdep": reb["dRdEdep"],
        "dRdErec": dRdErec,
        "dRdErec_band": dRdErec_band,
        "dRdErec_trigger": dRdErec_trig,
        "rebin": reb,
        "leakage": leak,
        "counts_budget": budget,
    }


def subev_boundary_Erec_eV(design: str) -> float:
    """The E_rec image of the 1.0 eV DEPOSITED regime boundary, for labelling.

    The boundary itself is a DEPOSIT energy, imported from
    ``trigger.SUBEV_REGIME_BOUNDARY_eV`` and never restated as a literal.  Its image on
    the reconstructed axis is read off the response matrix's OWN median mapping curve
    rather than assumed to be ``0.5 x`` anything.
    """
    from . import trigger as _trigger
    d = load_design_extended(design)
    return float(_erec_of_edep(_trigger.SUBEV_REGIME_BOUNDARY_eV,
                               d["E_dep_centers_eV"],
                               d["E_rec_median_non_paralyzable_eV"],
                               table=EXT_DESIGN_FILE[design] + " :: E_dep_centers_eV"))


if __name__ == "__main__":  # pragma: no cover
    import json as _json
    res = run_all(write=True)
    for name, r in res.items():
        print(f"{name}: wrote {r.get('_path', '<memory>')}")
        cc = counts_conservation(r)
        for ch, v in cc.items():
            print(f"  {ch:8s} N_dep={v['N_dep']:.4f} N_rec={v['N_rec']:.4f} rel={v['rel']:.2e}")
    print(_json.dumps(landing_report(), indent=2, default=float))


# =========================================================================== #
# Phase-13 plan 13-03: a NEUTRON-ONLY extended fold path.                      #
#                                                                             #
# Appended, not inserted.  ``fold.py`` line numbers are keyed by the Phase-10   #
# interpolator inventory (fold.py:554/588/592) and the Phase-12 summary records  #
# that shifting them is itself a defect, so nothing above this line moved.       #
#                                                                             #
# WHY A CHANNEL-SPECIFIC PATH.  ``run_fold`` folds all three channels and raises #
# on the still-584-bin muon and Compton grids, exactly as it did for Phase 12.   #
# =========================================================================== #

NEUTRON_EXT_CSV = os.path.join(EXT_ARTIFACT_DIR, "neutron_dRdT_ge_ext.csv")

NEUTRON_EXT_RECON_FILE = {
    "Ta->Al": "neutron_dRdErec_ext_TaAl.csv",
    "Al->Hf": "neutron_dRdErec_ext_AlHf.csv",
}

#: Header key every recoil table produced by Phase 13 carries.  It is what makes
#: the double-broaden trap CATCHABLE rather than a discipline problem: Phase 12
#: recorded that feeding an already-broadened table with ``broaden=True`` applies
#: the IA kernel TWICE with no error raised anywhere in the codebase.
BROADENED_PROVENANCE_KEY = "broadened_provenance"


class DoubleBroadeningError(ValueError):
    """Raised when an already-broadened recoil table is fed with broaden=True."""


def read_broadened_provenance(path: str):
    """Read ``broadened_provenance = true|false`` from a recoil table's header.

    Returns ``True``, ``False``, or ``None`` when the table declares nothing --
    and ``None`` is NOT treated as "unbroadened".  A table that does not say is a
    table whose broadening state is unknown, and the guard says so.
    """
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("#"):
                break
            import re as _re
            if not _re.search(r"(?<![A-Za-z_])" + BROADENED_PROVENANCE_KEY
                              + r"\s*=", line):
                continue
            val = line.split("=", 1)[1].strip().lower()
            if val.startswith("true"):
                return True
            if val.startswith("false"):
                return False
    return None


def read_neutron_recoil_table(path: str = NEUTRON_EXT_CSV,
                              rate_column: int = 1) -> dict:
    """The Phase-13 neutron recoil table: ``T_eV_nr`` in column 0.

    ``rate_column`` selects which rate column to fold.  Column 1 is the physical
    spectrum; column 2 is the smoothed-sigma CONTROL, which exists so that the
    SC3 imprint question can be re-asked on the RECONSTRUCTED axis with the
    control pushed through the IDENTICAL chain -- a difference between them then
    cannot be a chain artefact.
    """
    # Parse only the LEADING numeric tokens: the Phase-13 tables carry a trailing
    # per-row ``accuracy_label`` string, which is deliberate -- a consumer cannot
    # read a rate out of this channel without also reading its label.
    parsed = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            vals = []
            for tok in line.strip().split(","):
                try:
                    vals.append(float(tok))
                except ValueError:
                    break
            if len(vals) > rate_column:
                parsed.append(vals)
    rows = np.asarray(parsed, dtype=float)
    if rows.ndim != 2:
        raise ValueError(f"{path}: no numeric rows with a column {rate_column}")
    T = rows[:, 0]
    order = np.argsort(T)
    return {"T_eV": T[order], "dRdT": rows[order, rate_column],
            "rate_column": int(rate_column),
            "broadened_provenance": read_broadened_provenance(path)}


def rebin_recoil_arrays_to_edep_grid(
    E_dep_edges_eV: np.ndarray, T_eV: np.ndarray, dRdT: np.ndarray, *,
    broaden: bool | None = None, omega_bar_eV: float | None = None,
) -> dict:
    """Array-input twin of :func:`rebin_cevns_to_edep_grid`.

    Identical arithmetic, identical helper calls, identical low-edge treatment --
    it differs only in taking the recoil arrays directly rather than reading a
    fixed 8-column CSV layout.  ``tests/test_neutron_fold.py`` asserts it
    reproduces ``rebin_cevns_to_edep_grid`` BIT-IDENTICALLY on the Phase-12 CEvNS
    table, so the two cannot drift apart silently.
    """
    T = np.asarray(T_eV, float)
    y = np.asarray(dRdT, float)
    floor = float(E_dep_edges_eV[0])

    if broaden is None:
        broaden = ia_broadening.BROADENING_DEFAULT
    broadening_leakage = None
    if broaden:
        T, y, _, broadening_leakage = ia_broadening.broaden_native_spectrum(
            T, y, None, omega_bar_eV=omega_bar_eV)

    counts = rebin_counts(T, y, E_dep_edges_eV)
    dE_dep_keV = np.diff(E_dep_edges_eV) / 1.0e3
    dRdEdep = counts / dE_dep_keV

    inner = T[(T > T[0]) & (T < floor)]
    sub_edges = np.concatenate([[T[0]], inner, [floor]])
    low_counts = rebin_counts(T, y, sub_edges)
    low_centers = np.sqrt(sub_edges[:-1] * sub_edges[1:])
    low_Erec = LOW_E_SLOPE * low_centers

    return {
        "counts": counts,
        "dRdEdep": dRdEdep,
        "low_counts": low_counts,
        "low_Erec_eV": low_Erec,
        "broadening_applied": bool(broaden),
        "broadening_leakage": broadening_leakage,
        "floor_eV": floor,
        "T_min_eV": float(T[0]),
        "T_max_eV": float(T[-1]),
    }


def run_neutron_fold_extended(
    design: str, *, path: str = NEUTRON_EXT_CSV, broaden: bool = True,
    omega_bar_eV: Optional[float] = None, sharpness: Optional[float] = None,
    p_trig_override: Optional[np.ndarray] = None, rate_column: int = 1,
) -> dict:
    """Fold the Ge NEUTRON elastic channel ALONE through the extended matrices.

    Modelled on :func:`run_cevns_fold_extended` and carrying its three structural
    guards -- the 744-column shape check, the floor-coverage assertion on the
    bottom bin EDGE rather than the first knot, and a ``counts_budget`` that keeps
    ``residual_retained_plus_leaked`` and ``residual_retained_only`` SEPARATE --
    plus one guard Phase 12 identified but the codebase still lacked: an
    already-broadened input fed with ``broaden=True`` now RAISES
    (``fp-double-broaden``) instead of applying the kernel twice in silence.

    APPLICABILITY, STATED RATHER THAN ASSUMED.  IA broadening is a NUCLEAR-recoil
    width.  Neutron elastic recoils are nuclear recoils, so the kernel applies here
    on the same footing as CEvNS.  That is asserted from the shared nuclear-recoil
    character; the Phase-11 derivation was performed for the CEvNS channel and is
    not re-derived here.  Phase 15's ELECTRON-recoil channels are a separate
    question and are not settled by this.

    Pipeline order (Phase-12 lock, not negotiable): IA broadening on the recoil
    axis, upstream of the deposit rebin; then ``R(E_rec|E_dep)``; then the trigger
    curve as an analysis efficiency on the DEPOSIT axis, MULTIPLYING eps.  The rate
    is NEVER multiplied by ``exp(-2W)``.
    """
    from . import params as _params, trigger as _trigger

    src = read_neutron_recoil_table(path, rate_column=rate_column)
    if broaden and src["broadened_provenance"] is not False:
        raise DoubleBroadeningError(
            f"{os.path.basename(path)} declares "
            f"{BROADENED_PROVENANCE_KEY} = {src['broadened_provenance']!r} and "
            "broaden=True was requested. Applying the IA kernel to an already-"
            "broadened (or unlabelled) recoil table would widen every sub-eV "
            "feature by sqrt(2) and change the leakage budget while looking "
            "entirely normal (fp-double-broaden). Feed the UNBROADENED table, or "
            "pass broaden=False.")

    d = load_design_extended(design)
    R = d["R_non_paralyzable"]
    E_dep_edges = d["E_dep_edges_eV"]
    E_dep_centers = d["E_dep_centers_eV"]
    E_rec_edges = d["E_rec_edges_eV"]
    E_rec_centers = d["E_rec_centers_eV"]
    dE_rec_keV = np.diff(E_rec_edges) / 1.0e3

    if R.shape[1] != E_dep_centers.size or E_dep_centers.size != 744:
        raise ValueError(
            f"{design}: expected the 744-column EXTENDED response matrix, got "
            f"{R.shape}. The v1.0 584-column matrix would truncate at 10.14 eV "
            "and silently discard the entire sub-eV region this milestone exists "
            "to reach.")

    # FLOOR COVERAGE, asserted on the bottom bin EDGE rather than the first knot.
    native_lo = float(ia_broadening.native_edges(src["T_eV"])[0])
    floor = float(E_dep_edges[0])
    if native_lo > floor * (1.0 + 1.0e-9):
        raise ValueError(
            f"the recoil table {os.path.basename(path)} has its bottom bin edge at "
            f"{native_lo!r} eV but the extended deposit grid floors at {floor!r} eV. "
            "Its support does not reach the floor; folding it would report a "
            "sub-eV spectrum the table never covered.")

    reb = rebin_recoil_arrays_to_edep_grid(
        E_dep_edges, src["T_eV"], src["dRdT"],
        broaden=broaden, omega_bar_eV=omega_bar_eV)
    N_dep = reb["counts"]

    if p_trig_override is None:
        P = np.asarray(_trigger.P_trig(E_dep_centers, sharpness=sharpness), float)
    else:
        P = np.asarray(p_trig_override, float)
        if P.shape != E_dep_centers.shape:
            raise ValueError("p_trig_override must live on the deposit centres")

    N_rec = _add_low_edge(fold_counts(N_dep, R), reb["low_counts"],
                          reb["low_Erec_eV"], E_rec_edges)
    low_P = np.asarray(_trigger.P_trig(reb["low_Erec_eV"] / LOW_E_SLOPE,
                                       sharpness=sharpness), float) \
        if p_trig_override is None else np.ones_like(reb["low_counts"])
    N_rec_trig = _add_low_edge(fold_counts(N_dep * P, R),
                               reb["low_counts"] * low_P,
                               reb["low_Erec_eV"], E_rec_edges)

    dRdErec = N_rec / dE_rec_keV
    dRdErec_trig = N_rec_trig / dE_rec_keV

    T_src, y_src = src["T_eV"], src["dRdT"]
    dE_src_keV = np.diff(ia_broadening.native_edges(T_src)) / 1.0e3
    input_counts = float(np.sum(y_src * dE_src_keV))
    leak = reb["broadening_leakage"]
    leaked_below = float(leak["below_floor"]) if leak else 0.0
    leaked_below_zero = float(leak["below_zero"]) if leak else 0.0
    leaked_above = float(leak["above_top"]) if leak else 0.0
    deposit_counts = float(N_dep.sum() + reb["low_counts"].sum())
    rec_counts = float(N_rec.sum())

    budget = {
        "input_counts": input_counts,
        "leaked_below_floor": leaked_below,
        "leaked_below_zero": leaked_below_zero,   # a SUBSET of leaked_below_floor
        "leaked_above_top": leaked_above,
        "deposit_counts": deposit_counts,
        "reconstructed_counts": rec_counts,
        # The budget that must CLOSE:
        "residual_retained_plus_leaked": abs(
            deposit_counts + leaked_below + leaked_above - input_counts) / input_counts,
        # The one that must MISS.  A retained-only residual that also closes is
        # evidence of a hidden rescale (fp-renormalize-leakage).
        "residual_retained_only": (deposit_counts - input_counts) / input_counts,
        # R's columns sum to 1, so this is exact up to floating point.
        "residual_fold": abs(rec_counts - deposit_counts) / deposit_counts,
    }

    return {
        "design": design,
        "channel": "neutron_elastic_NR",
        "rate_column": int(rate_column),
        "broadening_applied": bool(broaden),
        "broadening_default": ia_broadening.BROADENING_DEFAULT,
        "omega_bar_eV": (_params.OMEGA_BAR_eV.value if omega_bar_eV is None
                         else float(omega_bar_eV)),
        "recoil_table": path,
        "E_dep_centers_eV": E_dep_centers,
        "E_dep_edges_eV": E_dep_edges,
        "E_rec_centers_eV": E_rec_centers,
        "E_rec_edges_eV": E_rec_edges,
        "E_rec_median_of_Edep_eV": d["E_rec_median_non_paralyzable_eV"],
        "P_trig_on_Edep": P,
        "N_dep": N_dep,
        "N_rec": N_rec,
        "N_rec_trigger": N_rec_trig,
        "dRdEdep": reb["dRdEdep"],
        "dRdErec": dRdErec,
        "dRdErec_trigger": dRdErec_trig,
        "rebin": reb,
        "leakage": leak,
        "counts_budget": budget,
    }


# =========================================================================== #
# Phase-15 plan 15-03: an ELECTRON-RECOIL extended fold path.                   #
#                                                                             #
# Appended, not inserted, for the same reason plan 13-03 appended: ``fold.py``  #
# line numbers are keyed by the Phase-10 interpolator inventory and shifting     #
# them is itself a defect.                                                     #
#                                                                             #
# WHY A CHANNEL-SPECIFIC PATH.  ``run_fold`` asserts the channel E_dep centres   #
# match the loaded matrix to 1e-6 relative and the muon/Compton tables were      #
# 584-bin, so it RAISES on them, exactly as it did for Phases 12 and 13.         #
#                                                                             #
# THE ONE STRUCTURAL DIFFERENCE FROM run_neutron_fold_extended.  These channels  #
# are ALREADY on the deposit axis.  There is no recoil-to-deposit rebin, so the  #
# recoil-table floor-coverage assertion is replaced by a DIRECT GRID-IDENTITY    #
# assertion of the input's 744 bin centres against the matrix's own              #
# ``E_dep_centers_eV``.                                                        #
# =========================================================================== #

EM_EXT_CSV = {
    "muon": os.path.join(EXT_ARTIFACT_DIR, "muon_dRdEdep_ext.csv"),
    "compton": os.path.join(EXT_ARTIFACT_DIR, "compton_dRdEdep_ext.csv"),
}

EM_EXT_RECON_FILE = {
    "Ta->Al": "em_dRdErec_ext_TaAl.csv",
    "Al->Hf": "em_dRdErec_ext_AlHf.csv",
}

#: Closed vocabulary for what a caller may do about non-finite deposit bins.
#: There is no "fill with zero" member and there never will be: R is dense, so a
#: zero-fill would convert an absence of measurement into a measured absence
#: spread across every reconstructed bin (``fp-nan-to-num``).
NO_SUPPORT_POLICIES = (
    "raise",                      # the default; a non-finite input is an error
    "exclude_and_record",         # drop the bin from the fold, record which and how many
)


class NonFiniteDepositError(ValueError):
    """Raised when a deposit vector carries non-finite bins and no policy was given.

    ``R`` is DENSE.  A single NaN deposit bin propagates to every reconstructed
    bin with a non-zero column entry, and the result renders as plausible-looking
    gaps rather than as an error.  There is no regime in which carrying a NaN
    through ``R @ N_dep`` is safe, so the fold refuses unless the caller states a
    policy and accepts having it written into the output header.
    """


def read_em_deposit_table(path: str) -> dict:
    """Read a Plan 15-02 extended-axis deposit table, labels included.

    Only the LEADING numeric tokens of each row are parsed, because the Phase-13
    pattern places the adequacy flag and the accuracy label last precisely so that
    a consumer cannot read a rate out of the file without meeting them.
    """
    rows, labels = [], []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#") or line.startswith("E_dep_keV"):
                continue
            vals, rest = [], []
            for tok in line.strip().split(","):
                try:
                    vals.append(float(tok))
                except ValueError:
                    rest.append(tok)
            if len(vals) >= 2:
                rows.append(vals[:5])
                labels.append(rest)
    arr = np.asarray(rows, dtype=float)
    return {
        "E_dep_keV": arr[:, 0],
        "dRdEdep": arr[:, 1],
        "mc_err": arr[:, 2],
        "mc_entries": arr[:, 3].astype(np.int64),
        "rel_mc_err": arr[:, 4],
        "labels": labels,
        "broadened_provenance": read_broadened_provenance(path),
        "path": path,
    }


def run_em_fold_extended(
    channel: str, design: str, *, path: Optional[str] = None,
    broaden: bool = False, sharpness: Optional[float] = None,
    p_trig_override: Optional[np.ndarray] = None,
    no_support_policy: str = "raise",
) -> dict:
    """Fold ONE electron-recoil channel through the extended response matrices.

    Modelled structurally on :func:`run_neutron_fold_extended` so the two extended
    paths cannot drift apart silently.  Five guards, ALL of which RAISE -- none
    warns, clamps, or falls back:

    1. **744-column shape check.**  The v1.0 584-column matrix would truncate at
       10.14 eV and silently discard the entire sub-eV region this milestone
       exists to reach.
    2. **Applicability guard.**  The Plan 15-01 verdict is read from
       :mod:`em_recoil` AT FOLD TIME rather than hard-coded, so a later change to
       the verdict cannot leave a stale branch here.  A broadening request that
       contradicts it raises ``em_recoil.ElectronRecoilBroadeningError`` carrying
       the verdict and its reason.
    3. **Double-broadening guard.**  ``read_broadened_provenance`` +
       ``DoubleBroadeningError``.  A table that declares NOTHING raises too:
       undeclared is *unknown*, not unbroadened.
    4. **Non-finite-input guard.**  ``NonFiniteDepositError`` unless the caller
       passes an explicit ``no_support_policy``; the policy and the number of bins
       it excluded are returned for the output header.  ``np.nan_to_num`` appears
       nowhere in this path.
    5. **Grid identity.**  The input's 744 centres must match the matrix's own
       ``E_dep_centers_eV`` to 1e-6 relative.  This REPLACES the recoil-table
       floor-coverage assertion of the neutron path, because these channels are
       already on the deposit axis and there is no rebin step to cover.

    Pipeline order (Phase-12 lock): any broadening on the native axis upstream of
    the deposit rebin -- not applicable here, see guard 2 -- then
    ``R(E_rec|E_dep)``, then the trigger curve as an analysis efficiency on the
    DEPOSIT axis, MULTIPLYING eps rather than replacing it.
    The rate is NEVER multiplied by ``exp(-2W)`` (milestone-wide prohibition).
    """
    from . import em_recoil as _er, trigger as _trigger

    if channel not in _er.ELECTRON_RECOIL_CHANNELS:
        raise KeyError(f"{channel!r} is not an electron-recoil channel; expected "
                       f"one of {_er.ELECTRON_RECOIL_CHANNELS}")
    if no_support_policy not in NO_SUPPORT_POLICIES:
        raise ValueError(f"no_support_policy {no_support_policy!r} outside "
                         f"{NO_SUPPORT_POLICIES}")
    path = EM_EXT_CSV[channel] if path is None else path

    # --- GUARD 2: the Plan 15-01 applicability verdict, read at fold time ----- #
    verdict = _er.assert_nuclear_kernel_use(channel, broaden)

    src = read_em_deposit_table(path)

    # --- GUARD 3: double broadening; undeclared is UNKNOWN, not unbroadened --- #
    if broaden and src["broadened_provenance"] is not False:
        raise DoubleBroadeningError(
            f"{os.path.basename(path)} declares {BROADENED_PROVENANCE_KEY} = "
            f"{src['broadened_provenance']!r} and broaden=True was requested. "
            "Applying a kernel to an already-broadened (or unlabelled) table "
            "would widen every sub-eV feature and change the leakage budget while "
            "looking entirely normal (fp-double-broaden).")

    d = load_design_extended(design)
    R = d["R_non_paralyzable"]
    E_dep_edges = d["E_dep_edges_eV"]
    E_dep_centers = d["E_dep_centers_eV"]
    E_rec_edges = d["E_rec_edges_eV"]
    E_rec_centers = d["E_rec_centers_eV"]
    dE_rec_keV = np.diff(E_rec_edges) / 1.0e3

    # --- GUARD 1: 744 columns ------------------------------------------------ #
    if R.shape[1] != E_dep_centers.size or E_dep_centers.size != 744:
        raise ValueError(
            f"{design}: expected the 744-column EXTENDED response matrix, got "
            f"{R.shape}. The v1.0 584-column matrix would truncate at 10.14 eV "
            "and silently discard the entire sub-eV region this milestone exists "
            "to reach.")
    # R's columns sum to 1, so the conservation residual is a real check on the
    # fold rather than a measurement of the matrix.  Asserted BEFORE folding.
    colsum = R.sum(axis=0)
    if not np.allclose(colsum, 1.0, atol=1e-9):
        raise ValueError(
            f"{design}: response-matrix columns do not sum to 1 "
            f"(min {colsum.min()!r}, max {colsum.max()!r}); the counts-conservation "
            "residual would then be measuring the matrix, not the fold.")

    # --- GUARD 5: grid identity (replaces the neutron floor-coverage check) --- #
    dep_eV = src["E_dep_keV"] * 1.0e3
    if dep_eV.size != E_dep_centers.size:
        raise ValueError(
            f"{os.path.basename(path)} has {dep_eV.size} bins but the extended "
            f"matrix has {E_dep_centers.size}. These channels are ALREADY on the "
            "deposit axis; there is no rebin step that could reconcile them.")
    rel = np.abs(dep_eV - E_dep_centers) / E_dep_centers
    if rel.max() > 1.0e-6:
        raise ValueError(
            f"{os.path.basename(path)} deposit centres differ from the matrix's "
            f"own E_dep_centers_eV by up to {rel.max():.3e} relative. These "
            "channels are already on the deposit axis, so a mismatch is a "
            "re-grid error, not something a rebin should paper over.")

    # --- GUARD 4: non-finite input ------------------------------------------- #
    dRdEdep = np.asarray(src["dRdEdep"], float)
    bad = ~np.isfinite(dRdEdep)
    n_bad = int(bad.sum())
    if n_bad and no_support_policy == "raise":
        idx = np.flatnonzero(bad)
        raise NonFiniteDepositError(
            f"{os.path.basename(path)} carries {n_bad} non-finite deposit bins "
            f"(first at index {int(idx[0])}, centre {dep_eV[idx[0]]:.6g} eV). R is "
            "DENSE: one NaN propagates to every reconstructed bin with a non-zero "
            "column entry and renders as plausible-looking gaps. Pass an explicit "
            f"no_support_policy from {NO_SUPPORT_POLICIES} and accept having it "
            "written into the output header. np.nan_to_num is forbidden here: it "
            "would convert an absence of measurement into a measured absence, "
            "undoing exactly what Plan 15-02 wrote NaN to prevent.")
    excluded = np.flatnonzero(bad)
    N_dep = dep_counts_from_dRdEdep(np.where(bad, 0.0, dRdEdep), E_dep_edges)

    # --- the trigger, on the DEPOSIT axis (CONVENTIONS Section I) ------------- #
    if p_trig_override is None:
        P = np.asarray(_trigger.P_trig(E_dep_centers, sharpness=sharpness), float)
    else:
        P = np.asarray(p_trig_override, float)
        if P.shape != E_dep_centers.shape:
            raise ValueError("p_trig_override must live on the deposit centres")

    # --- fold ---------------------------------------------------------------- #
    N_rec = fold_counts(N_dep, R)
    N_rec_trig = fold_counts(N_dep * P, R)
    dRdErec = N_rec / dE_rec_keV
    dRdErec_trig = N_rec_trig / dE_rec_keV

    deposit_counts = float(N_dep.sum())
    rec_counts = float(N_rec.sum())
    budget = {
        "input_counts": deposit_counts,
        "excluded_no_support_bins": n_bad,
        "no_support_policy": no_support_policy,
        "leaked_below_floor": 0.0,
        "leaked_below_zero": 0.0,
        "leaked_above_top": 0.0,
        "deposit_counts": deposit_counts,
        "reconstructed_counts": rec_counts,
        # NO BROADENING IS APPLIED to an electron-recoil channel (Plan 15-01
        # verdict does_not_apply), so there is no kernel leakage and these two
        # residuals COINCIDE BY CONSTRUCTION.  They are reported separately for
        # structural parity with the neutron path, and the coincidence is stated
        # rather than presented as two independent confirmations.
        "residual_retained_plus_leaked": 0.0,
        "residual_retained_only": 0.0,
        "residuals_coincide_because_no_broadening": True,
        # R's columns sum to 1, so this is exact up to floating point.
        "residual_fold": abs(rec_counts - deposit_counts) / deposit_counts,
    }

    return {
        "channel": channel,
        "design": design,
        "deposit_table": path,
        "broadening_applied": bool(broaden),
        "broadening_verdict": verdict.verdict,
        "broadening_reason": verdict.reason,
        "no_support_policy": no_support_policy,
        "excluded_bins": excluded,
        "n_excluded_bins": n_bad,
        "E_dep_centers_eV": E_dep_centers,
        "E_dep_edges_eV": E_dep_edges,
        "E_rec_centers_eV": E_rec_centers,
        "E_rec_edges_eV": E_rec_edges,
        "E_rec_median_of_Edep_eV": d["E_rec_median_non_paralyzable_eV"],
        "P_trig_on_Edep": P,
        "sharpness": (None if sharpness is None else float(sharpness)),
        "N_dep": N_dep,
        "N_rec": N_rec,
        "N_rec_trigger": N_rec_trig,
        "dRdEdep": dRdEdep,
        "dRdErec": dRdErec,
        "dRdErec_trigger": dRdErec_trig,
        "mc_entries": src["mc_entries"],
        "counts_budget": budget,
    }
