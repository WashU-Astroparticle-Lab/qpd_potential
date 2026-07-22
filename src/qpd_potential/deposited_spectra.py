# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
#
# Phase-4 deposited-energy spectra ASSEMBLY (Plan 04-03, depends on 04-01 muon
# and 04-02 Compton). Co-adds the two channel dR/dE_dep spectra on the IDENTICAL
# shared log E_dep grid, verifies per-channel energy closure, computes the
# 50 kHz pileup / stop-condition occupancy, and emits the combined figure.
#
# ENERGY SCALE: unified phonon E_dep scale, NO ionization quenching, NO
# keVee/keVnr split (CONVENTIONS Section B). This module delivers DEPOSITED
# energy dR/dE_dep only; the QPD response R(E_rec|E_dep) and reconstructed-energy
# folding are Phase 5. Guards fp-reconstructed-not-deposited.
#
# KEY PHYSICS / GUARDS:
#  * SHARED GRID: the two channel CSVs are asserted to be on the identical log
#    E_dep grid before any co-addition. Guards fp-grid-mismatch.
#  * ENERGY CLOSURE: per channel, the count-rate closure integral
#    int dR/dE_dep dE  ==  rate_Hz * 86400 / mass_kg  (counts/kg/day) ties the
#    differential histogram back to the INDEPENDENTLY computed scalar event rate
#    (the muon MC/analytic rate 04-01, the Compton flux*sigma_KN*N_e rate 04-02).
#    The first moment  int E*dR/dE_dep dE  (deposited power) is reported as a
#    physical diagnostic (mean deposit per event), derived from the same
#    histogram -- NOT an independent number.
#  * PILEUP STOP-CONDITION: event-level occupancy = total event rate x pulse
#    duration vs the 50 kHz bandwidth (ROADMAP Phase 4/5). Reported explicitly,
#    never asserted. Guards fp-pileup-unchecked.
#
# The channel rates are PARSED from the CSV headers (not hard-coded), so the
# closure check consumes the value each upstream plan actually produced.
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from . import wafer_geometry as wg
from .muon_deposit import shared_energy_grid

# --- Bandwidth-censoring convention (CONVENTIONS Section F, locked) ----------
BANDWIDTH_HZ = 50_000.0        # 50 kHz sampling bandwidth
SAMPLE_TIME_S = 20e-6          # 20 us  (50 kHz sample slot)
RESOLVE_TIME_S = 40e-6         # 40 us  (25 kHz Nyquist resolving time)
SECONDS_PER_DAY = 86_400.0

# Compton Klein-Nishina electron-recoil edges (04-02, keV) for the figure.
COMPTON_EDGES_KEV = {"40K": 1243.4, "214Bi": 1541.3, "208Tl": 2381.8}

_REPO_ROOT = Path(__file__).resolve().parents[2]
MUON_CSV = _REPO_ROOT / "data" / "muon_dRdEdep.csv"
COMPTON_CSV = _REPO_ROOT / "data" / "compton_dRdEdep.csv"


@dataclass
class Channel:
    """One deposited-energy channel loaded from its dR/dE_dep CSV."""
    name: str
    E_dep_keV: np.ndarray          # bin centers [keV]
    dRdEdep: np.ndarray            # counts/kg/day/keV
    mc_err: np.ndarray             # counts/kg/day/keV
    rate_Hz: float                 # independently-computed total wafer event rate


def _parse_rate_Hz(header_lines: list[str]) -> float:
    """Extract the total event rate (Hz) an upstream plan wrote into the header.

    Matches e.g. 'integral_muon_rate_Hz = 1.3657 +/- 0.0049' or
    'total_single_scatter_rate_Hz = 2.6846e-01 (...)'.
    """
    for ln in header_lines:
        m = re.search(r"rate_Hz\s*=\s*([0-9.eE+\-]+)", ln)
        if m:
            return float(m.group(1))
    raise ValueError("no '*_rate_Hz = <value>' line found in CSV header")


def load_channel(csv_path: str | Path, name: str) -> Channel:
    """Load a channel dR/dE_dep CSV (comment header + E_dep,dRdEdep,mc_err)."""
    csv_path = Path(csv_path)
    header, rows = [], []
    with open(csv_path) as fh:
        for ln in fh:
            if ln.startswith("#"):
                header.append(ln)
                continue
            if ln.startswith("E_dep"):        # column-name line
                continue
            parts = ln.strip().split(",")
            if len(parts) < 3:
                continue
            rows.append([float(parts[0]), float(parts[1]), float(parts[2])])
    arr = np.asarray(rows, dtype=float)
    return Channel(
        name=name,
        E_dep_keV=arr[:, 0],
        dRdEdep=arr[:, 1],
        mc_err=arr[:, 2],
        rate_Hz=_parse_rate_Hz(header),
    )


def assert_shared_grid(a: np.ndarray, b: np.ndarray, rtol: float = 1e-9) -> float:
    """Verify two E_dep grids are identical. Returns the max relative deviation.

    Guards fp-grid-mismatch: silently co-adding mismatched/re-binned grids would
    corrupt both the closure test and the Phase-5 fold.
    """
    if a.shape != b.shape:
        raise ValueError(f"grid length mismatch: {a.shape} vs {b.shape}")
    max_rel = float(np.max(np.abs(a - b) / np.abs(b)))
    if max_rel > rtol:
        raise ValueError(
            f"grids differ by max rel {max_rel:.3e} > rtol {rtol:.1e} "
            "(fp-grid-mismatch guard)"
        )
    return max_rel


def bin_edges_and_widths() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Shared log-grid edges, geometric-mean centers, and linear widths dE [keV].

    The channel CSVs store bin CENTERS = geometric means of the log edges; the
    histogram normalization used the LINEAR bin widths dE = edge_{i+1}-edge_i,
    so the closure integral must use those same widths.
    """
    edges = shared_energy_grid()
    centers = np.sqrt(edges[:-1] * edges[1:])
    dE = np.diff(edges)
    return edges, centers, dE


@dataclass
class ClosureResult:
    name: str
    count_integral: float          # int dR/dE_dep dE  [counts/kg/day]
    count_integral_err: float      # MC error on the integral
    expected: float                # rate_Hz * 86400 / mass_kg
    ratio: float                   # count_integral / expected
    power_integral: float          # int E*dR/dE_dep dE [keV/kg/day] (first moment)
    mean_deposit_keV: float        # power_integral / count_integral


def energy_closure(channel: Channel, dE: np.ndarray,
                   mass_kg: float = wg.MASS_KG) -> ClosureResult:
    """Per-channel count-rate closure + deposited-power first moment.

    Count closure (the INDEPENDENT conservation cross-check):
        int dR/dE_dep dE  ==  rate_Hz * 86400 / mass_kg     [counts/kg/day]
    Power (first moment, physical diagnostic, NOT independent):
        int E * dR/dE_dep dE                                [keV/kg/day]
    """
    C = float(np.sum(channel.dRdEdep * dE))
    C_err = float(np.sqrt(np.sum((channel.mc_err * dE) ** 2)))
    expected = channel.rate_Hz * SECONDS_PER_DAY / mass_kg
    P = float(np.sum(channel.dRdEdep * channel.E_dep_keV * dE))
    return ClosureResult(
        name=channel.name,
        count_integral=C,
        count_integral_err=C_err,
        expected=expected,
        ratio=C / expected,
        power_integral=P,
        mean_deposit_keV=P / C,
    )


@dataclass
class PileupResult:
    total_rate_Hz: float
    mean_interval_s: float                 # 1 / total_rate
    occupancy_sample: float                # rate * 20us  (50 kHz slot)
    occupancy_resolve: float               # rate * 40us  (25 kHz resolving)
    deadtime_frac_nonparalyzable: float    # R*tau / (1 + R*tau), tau = resolve
    livetime_frac_paralyzable: float       # exp(-R*tau), tau = resolve
    rate_over_bandwidth: float             # total_rate / 50 kHz
    stop_condition_triggered: bool
    per_channel_Hz: dict = field(default_factory=dict)


def pileup_occupancy(rates_Hz: dict[str, float],
                     resolve_time_s: float = RESOLVE_TIME_S,
                     sample_time_s: float = SAMPLE_TIME_S,
                     bandwidth_Hz: float = BANDWIDTH_HZ,
                     stop_threshold: float = 1e-2) -> PileupResult:
    """Event-level pileup / stop-condition occupancy vs the 50 kHz bandwidth.

    ROADMAP Phase 4/5 stop-condition: if muon+gamma pileup makes quiescent
    reconstruction impossible at 50 kHz, REPORT the pileup regime rather than
    forcing a spectrum. With a few-Hz total event rate this is a formality, but
    the occupancy is COMPUTED, not asserted (guards fp-pileup-unchecked).

    stop_threshold: occupancy above which quiescent operation is flagged as
    non-trivial (1% dead-time). Occupancy << this => no event-level pileup.
    """
    R = float(sum(rates_Hz.values()))
    occ_res = R * resolve_time_s
    return PileupResult(
        total_rate_Hz=R,
        mean_interval_s=1.0 / R,
        occupancy_sample=R * sample_time_s,
        occupancy_resolve=occ_res,
        deadtime_frac_nonparalyzable=occ_res / (1.0 + occ_res),
        livetime_frac_paralyzable=float(np.exp(-occ_res)),
        rate_over_bandwidth=R / bandwidth_Hz,
        stop_condition_triggered=bool(occ_res >= stop_threshold),
        per_channel_Hz=dict(rates_Hz),
    )


def assemble(muon_csv: str | Path = MUON_CSV,
             compton_csv: str | Path = COMPTON_CSV):
    """Load, verify shared grid, co-add, run closure + pileup. Returns a dict."""
    muon = load_channel(muon_csv, "muon")
    compton = load_channel(compton_csv, "compton")

    max_rel = assert_shared_grid(muon.E_dep_keV, compton.E_dep_keV)
    edges, centers, dE = bin_edges_and_widths()
    # The CSV centers must also match the canonical shared grid (guards a silent
    # re-bin upstream); tolerance covers 6-significant-figure CSV rounding.
    assert_shared_grid(muon.E_dep_keV, centers, rtol=1e-5)

    total = muon.dRdEdep + compton.dRdEdep
    total_err = np.sqrt(muon.mc_err ** 2 + compton.mc_err ** 2)

    closures = {
        "muon": energy_closure(muon, dE),
        "compton": energy_closure(compton, dE),
    }
    pileup = pileup_occupancy({"muon": muon.rate_Hz, "compton": compton.rate_Hz})

    return {
        "muon": muon,
        "compton": compton,
        "E_dep_keV": muon.E_dep_keV,
        "total": total,
        "total_err": total_err,
        "grid_max_rel": max_rel,
        "dE": dE,
        "closures": closures,
        "pileup": pileup,
    }


def write_combined_table(result: dict, out_csv: str | Path) -> Path:
    """Emit the combined muon+Compton+total dR/dE_dep table on the shared grid."""
    out_csv = Path(out_csv)
    E = result["E_dep_keV"]
    muon = result["muon"].dRdEdep
    compton = result["compton"].dRdEdep
    total = result["total"]
    total_err = result["total_err"]
    pu = result["pileup"]
    hdr = [
        "# Combined Phase-4 deposited-energy background spectra (Plan 04-03).",
        "# Co-added muon (04-01) + Compton (04-02) dR/dE_dep on the IDENTICAL",
        "# shared log E_dep grid. UNIFIED PHONON SCALE, NO quenching (CONVENTIONS B).",
        "# DEPOSITED energy only -- the QPD response / E_rec fold is Phase 5.",
        f"# muon_rate_Hz = {result['muon'].rate_Hz:.5g}; "
        f"compton_rate_Hz = {result['compton'].rate_Hz:.5g}; "
        f"total_rate_Hz = {pu.total_rate_Hz:.5g}",
        f"# pileup_occupancy(50kHz,20us) = {pu.occupancy_sample:.3e}; "
        f"deadtime_frac(40us) = {pu.deadtime_frac_nonparalyzable:.3e}; "
        f"stop_condition_triggered = {pu.stop_condition_triggered}",
        "# grid: shared log E_dep, 0.01 keV -> 2e5 keV (200 MeV), ~80 bins/decade",
        "# units: E_dep_keV [keV]; all dR/dE_dep [counts/kg/day/keV]",
        "E_dep_keV,muon_dRdEdep,compton_dRdEdep,total_dRdEdep,total_mc_err",
    ]
    lines = list(hdr)
    for i in range(len(E)):
        lines.append(
            f"{E[i]:.6e},{muon[i]:.6e},{compton[i]:.6e},"
            f"{total[i]:.6e},{total_err[i]:.6e}"
        )
    out_csv.write_text("\n".join(lines) + "\n")
    return out_csv


def make_figure(result: dict, out_png: str | Path) -> Path:
    """Log-log combined deposited-energy spectra: muon, Compton, total."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    E = result["E_dep_keV"]
    muon = result["muon"].dRdEdep
    compton = result["compton"].dRdEdep
    total = result["total"]
    pu = result["pileup"]

    def _mask(y):
        return np.where(y > 0, y, np.nan)

    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    ax.loglog(E, _mask(total), color="black", lw=2.0, label="total (muon + Compton)")
    ax.loglog(E, _mask(muon), color="C0", lw=1.4, label="muon (04-01)")
    ax.loglog(E, _mask(compton), color="C3", lw=1.4, label="Compton (04-02)")

    ymax = np.nanmax(total)
    ymin = max(np.nanmin(_mask(total)), ymax * 1e-9)
    ax.set_ylim(ymin, ymax * 3)

    # Compton Klein-Nishina electron-recoil edges.
    for lbl, ekev in COMPTON_EDGES_KEV.items():
        ax.axvline(ekev, color="C3", ls=":", lw=0.8, alpha=0.7)
        ax.text(ekev, ymax * 1.4, lbl, rotation=90, va="bottom", ha="right",
                fontsize=7, color="C3")
    # Muon high-E tail marker (~197 MeV Phase-5 saturation input).
    tail = float(E[result["muon"].dRdEdep > 0].max())
    ax.axvline(tail, color="C0", ls="--", lw=0.8, alpha=0.6)
    ax.text(tail, ymin * 3, f"muon tail\n~{tail/1e3:.0f} MeV", rotation=90,
            va="bottom", ha="right", fontsize=7, color="C0")

    ax.set_xlabel("deposited (phonon) energy  $E_{\\mathrm{dep}}$  [keV]")
    ax.set_ylabel("$dR/dE_{\\mathrm{dep}}$  [counts kg$^{-1}$ day$^{-1}$ keV$^{-1}$]")
    ax.set_title("Phase-4 deposited-energy backgrounds (deposited, NOT reconstructed)")
    cl = result["closures"]
    txt = (
        f"muon closure {cl['muon'].ratio:.3f}, Compton {cl['compton'].ratio:.4f}\n"
        f"$R_\\mathrm{{tot}}$ = {pu.total_rate_Hz:.2f} Hz; "
        f"occupancy @50 kHz = {pu.occupancy_sample:.1e} $\\ll$ 1\n"
        "shared log grid, no E_rec fold (Phase 5)"
    )
    ax.text(0.02, 0.03, txt, transform=ax.transAxes, fontsize=7.5,
            va="bottom", ha="left",
            bbox=dict(boxstyle="round", fc="white", ec="0.7", alpha=0.9))
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, which="both", ls=":", alpha=0.3)
    fig.tight_layout()
    out_png = Path(out_png)
    fig.savefig(out_png, dpi=140)
    plt.close(fig)
    return out_png


def _report(result: dict) -> str:
    cl = result["closures"]
    pu = result["pileup"]
    lines = ["Phase-4 deposited-energy assembly (Plan 04-03)",
             f"  shared grid max rel deviation: {result['grid_max_rel']:.2e} (identical)"]
    for name in ("muon", "compton"):
        c = cl[name]
        lines.append(
            f"  {name:8s} closure int={c.count_integral:.4e} "
            f"expected={c.expected:.4e} ratio={c.ratio:.5f} "
            f"(+/-{c.count_integral_err/c.expected:.1e}) | "
            f"mean deposit={c.mean_deposit_keV:.4g} keV"
        )
    lines.append(
        f"  pileup: R_tot={pu.total_rate_Hz:.4f} Hz, 1/R={pu.mean_interval_s:.3f} s; "
        f"occ(20us)={pu.occupancy_sample:.3e}, occ(40us)={pu.occupancy_resolve:.3e}, "
        f"R/50kHz={pu.rate_over_bandwidth:.3e}"
    )
    lines.append(
        f"  stop-condition triggered: {pu.stop_condition_triggered} "
        "(within-event muon saturation ~200 MeV tail flagged for Phase 5)"
    )
    return "\n".join(lines)


def main() -> dict:
    result = assemble()
    out_csv = _REPO_ROOT / "data" / "combined_dRdEdep.csv"
    out_png = _REPO_ROOT / "figs" / "phase4_deposited_spectra.png"
    write_combined_table(result, out_csv)
    make_figure(result, out_png)
    print(_report(result))
    print(f"  wrote {out_csv}")
    print(f"  wrote {out_png}")
    return result


if __name__ == "__main__":
    main()
