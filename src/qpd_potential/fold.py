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
    A = y1 / (T1 ** p)
    if abs(p + 1.0) < 1e-9:
        return A * np.log(b / a)
    return A * (b ** (p + 1.0) - a ** (p + 1.0)) / (p + 1.0)


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
    E_dep_edges_eV: np.ndarray, path: str = CEVNS_CSV
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


def run_all(write: bool = True) -> dict:
    return {name: run_fold(name, write=write) for name in rm.DESIGN_FILE}


if __name__ == "__main__":  # pragma: no cover
    import json as _json
    res = run_all(write=True)
    for name, r in res.items():
        print(f"{name}: wrote {r.get('_path', '<memory>')}")
        cc = counts_conservation(r)
        for ch, v in cc.items():
            print(f"  {ch:8s} N_dep={v['N_dep']:.4f} N_rec={v['N_rec']:.4f} rel={v['rel']:.2e}")
    print(_json.dumps(landing_report(), indent=2, default=float))
