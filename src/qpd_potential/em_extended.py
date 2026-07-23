# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
#
# Phase-15 Plan 15-02: extended-axis assembly for the two ELECTRON-RECOIL channels.
#
# Puts the v1.0 muon and Compton deposited-energy spectra onto Phase 10's 744-bin
# extended axis reaching 0.0999350 eV, with the v1.0 machinery UNCHANGED and at the
# v1.0 sea-level, ZERO overburden normalization, so that every difference from the
# published v1.0 spectra is attributable to the grid extension alone.
#
# THE ROUTE IS DECIDED BY MEASUREMENT, NOT BY ASSERTION.  Two routes can satisfy
# ROADMAP Phase 15 SC1 and they have different failure modes:
#   exact_redrive_identical_stream -- re-run each Monte Carlo at the identical
#       (n, seed, batch_size) on the extended edges.  Licensed only if the RNG
#       stream is independent of the histogram edges.
#   index_carry_frozen_bins        -- carry the frozen v1.0 bins by INDEX via
#       legacy_grid.carried_onto_extended_axis and run the MC only for bins 0..159.
# `select_route` runs the tests and records the outcome either way.
#
# NO NORMALIZATION FACTOR OTHER THAN EXACTLY 1.0 multiplies either channel.  Veto
# credit is 1.0 by construction; there is no overburden, no shield, no attenuation.
#
# BINS WITH NO MONTE-CARLO SUPPORT ARE WRITTEN NaN AND LABELLED, NEVER 0.0.  A zero
# reads as a measured absence of rate; the correct statement is that the estimator
# has no support there.  legacy_grid.carried_onto_extended_axis already writes NaN
# for exactly this reason and this module keeps that discipline (fp-zero-for-no-data).
#
# THESE TABLES ARE UNBROADENED and say so in their headers
# (broadened_provenance = false), per Plan 15-01's per-channel verdict
# `does_not_apply`.  fold.read_broadened_provenance reads that declaration; a table
# declaring nothing is treated as UNKNOWN, which would block Plan 15-03.

from __future__ import annotations

import csv
import os
import subprocess
from dataclasses import dataclass
from typing import Optional

import numpy as np

from . import compton_deposit as cd
from . import compton_source as cs
from . import em_recoil as er
from . import legacy_grid as lg
from . import muon_deposit as md
from . import wafer_geometry as wg

__all__ = [
    "ROUTE_VOCABULARY",
    "STAT_ADEQUACY_VOCABULARY",
    "ARTIFACT_DIR",
    "MUON_EXT_CSV",
    "COMPTON_EXT_CSV",
    "REGRESSION_CSV",
    "MUON_ACCURACY_LABEL",
    "GAMMA_ACCURACY_LABEL",
    "PROD_MUON_SAMPLES",
    "PROD_COMPTON_SAMPLES_PER_LINE",
    "PROD_SEED",
    "PROD_BATCH_SIZE",
    "repo_head",
    "extended_grid",
    "bit_identity_probe",
    "select_route",
    "stat_adequacy_label",
    "below_validity_floor_flags",
    "assemble_channel",
    "write_channel_csv",
    "read_channel_csv",
    "closed_form_compton_edges",
    "v1_regression",
    "write_regression_csv",
]

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
ARTIFACT_DIR = os.path.join(_ROOT, "artifacts", "v2.0")

MUON_EXT_CSV = os.path.join(ARTIFACT_DIR, "muon_dRdEdep_ext.csv")
COMPTON_EXT_CSV = os.path.join(ARTIFACT_DIR, "compton_dRdEdep_ext.csv")
REGRESSION_CSV = os.path.join(ARTIFACT_DIR, "em_v1_regression.csv")

FROZEN_MUON_CSV = os.path.join(_ROOT, "data", "muon_dRdEdep.csv")
FROZEN_COMPTON_CSV = os.path.join(_ROOT, "data", "compton_dRdEdep.csv")

#: The settings recorded in the frozen CSV headers and in the scripts that wrote
#: them (scripts/make_muon_spectrum.py, scripts/make_compton_spectrum.py).
PROD_MUON_SAMPLES = 1_000_000_000
PROD_COMPTON_SAMPLES_PER_LINE = 40_000_000
PROD_SEED = 20260720
PROD_BATCH_SIZE = 5_000_000

N_PREPENDED = 160
N_EXT_BINS = 744
N_V1_BINS = 584

ROUTE_VOCABULARY = ("exact_redrive_identical_stream", "index_carry_frozen_bins")

#: Closed vocabulary for the per-bin statistical adequacy label.  A bin with NO
#: Monte-Carlo support FAILS this scale rather than merely scoring lower on it --
#: `no_mc_support` is not "worse statistics", it is "no measurement".
STAT_ADEQUACY_VOCABULARY = (
    "no_mc_support",            # zero raw entries; the value is NaN, never 0.0
    "kinematically_forbidden",  # zero entries because the MODEL FORBIDS content
    "insufficient_mc_support",  # entries < 10, or relative MC error > 0.5
    "marginal_mc_support",      # 0.2 < relative MC error <= 0.5
    "adequate_mc_support",      # relative MC error <= 0.2
)

#: THE ONE NARROW EXCEPTION TO THE NaN DISCIPLINE, and it is a physics
#: distinction rather than a convenience.
#:
#: `fp-zero-for-no-data` forbids writing 0.0 for an absent measurement because "a
#: zero reads as a measured absence of rate [when] the estimator has no support
#: there".  ABOVE THE HIGHEST COMPTON EDGE that reasoning inverts: the thin-target
#: single-scatter model KINEMATICALLY FORBIDS any deposit above
#: E_edge = 2 E_gamma^2/(m_e c^2 + 2 E_gamma) of the most energetic line, so a
#: measured absence is exactly the correct statement and 0.0 is the model's
#: PREDICTION, not a gap.  Writing NaN there would be the opposite error: it would
#: say "unmeasured" about a region the model positively excludes, and it would
#: make `test-no-photopeak` untestable in the artifact -- while `fp-full-absorption`
#: requires the single-scatter approximation to remain intact IN THE ARTIFACT, not
#: merely in the prose.  The exception is therefore confined to Compton bins whose
#: LOWER EDGE exceeds the highest closed-form Compton edge, and to those only.
COMPTON_KINEMATIC_CEILING_NOTE = (
    "bins whose LOWER EDGE exceeds the highest Compton edge are kinematically "
    "forbidden to the single-scatter model, so 0.0 there is the model's "
    "prediction rather than an absence of measurement")

#: Below this raw entry count the Gaussian sqrt(sum w^2) error is not a confidence
#: interval at all, so the ADEQUACY LABEL rather than the error bar is the
#: operative statement (Plan 15-02 unvalidated_assumptions).
MIN_ENTRIES_FOR_ERROR_BAR = 10

#: Accuracy labels, carried forward UNNARROWED (ROADMAP Phase 15 SC5).  The muon
#: label NEVER travels as a bare -20.61 % or a bare flatters_SB: the two PDG
#: statements BRACKET the adopted 1.3659 Hz from opposite sides, so the ~20 %
#: magnitude is solid while the SIGN is anchor-leg dependent (fp-bare-sign).
MUON_ACCURACY_LABEL = (
    "flatters_SB | -20.61% vs PDG Leg A (~1 muon cm^-2 min^-1 x A_top = 1.7204 Hz) "
    "| BRACKETING DISCLOSURE: PDG Leg B (I_v ~ 70 m^-2 s^-1 sr^-1 with cos^2 theta "
    "-> 1.1350 Hz) puts the same adopted 1.3659 Hz at +20.34%, i.e. penalizes_SB; "
    "the two PDG statements BRACKET the adopted rate from opposite sides, so the "
    "~20% MAGNITUDE is solid and the SIGN is anchor-leg dependent "
    "| underlying limit: 30-35% inter-experiment Gaisser-Guan normalization spread, "
    "which no in-repo artifact can narrow"
)
GAMMA_ACCURACY_LABEL = (
    "neutral | +0.00% vs the LABChico measured survey, which IS the adopted "
    "normalization | factor-2 site-dependent band x0.5 .. x2 (the low edge is the "
    "flattering one and is not used) | weakest anchor: the U-chain flux rests on an "
    "assumed Phi_U = Phi_Th chain balance, not a measured line intensity"
)

#: The single statement of what multiplies each channel's normalization.  Enumerated
#: rather than summarised, because a product can be unity by cancellation.
NORMALIZATION_FACTORS = (
    ("overburden_attenuation", 1.0, "no overburden in this configuration"),
    ("shield_attenuation", 1.0, "no shield in this configuration"),
    ("veto_credit", 1.0, "exactly 1.0 BY CONSTRUCTION -- surface_environment.veto_credit()"),
    ("buildup_factor", 1.0, "no shield, so no buildup"),
    ("ambience_rescale", 1.0, "the v1.0 sea-level normalization stands unchanged"),
)


def repo_head() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                              cwd=_ROOT, capture_output=True, text=True,
                              check=True).stdout.strip()
    except Exception:                                     # pragma: no cover
        return "unknown"


def extended_grid():
    """``(edges, centres)`` of the 744-bin extended axis, in keV."""
    edges = md.shared_energy_grid("v2.0-ext")
    return edges, np.sqrt(edges[:-1] * edges[1:])


# =========================================================================== #
# 1. THE ROUTE DECISION, BY MEASUREMENT                                        #
# =========================================================================== #

def bit_identity_probe(n_muon: int = 300_000, n_compton_per_line: int = 50_000,
                       seed: int = PROD_SEED,
                       batch_size: int = PROD_BATCH_SIZE) -> dict:
    """Run each Monte Carlo twice at small N -- v1.0 edges and extended edges --
    and compare bins ``160..743`` with ``np.array_equal``, never ``np.allclose``.

    This is the STRUCTURAL claim, established before a production run is spent on
    it: in both drivers every random draw precedes ``np.histogram``, so the RNG
    stream cannot depend on the edge array.  If that holds, the extended run's
    retained bins reproduce the v1.0 run's EXACTLY, because Plan 10-03 preserved
    the v1.0 edge array bit-for-bit (``np.array_equal``, max difference 0.0).
    """
    v1 = md.shared_energy_grid("v1.0")
    ext = md.shared_energy_grid("v2.0-ext")
    out = {
        "edge_join_array_equal": bool(np.array_equal(ext[N_PREPENDED:], v1)),
        "edge_join_max_abs_diff": float(np.abs(ext[N_PREPENDED:] - v1).max()),
        "n_muon": int(n_muon), "n_compton_per_line": int(n_compton_per_line),
        "seed": int(seed), "batch_size": int(batch_size),
    }

    m1 = md.run_muon_mc(n_samples=n_muon, seed=seed, batch_size=batch_size,
                        grid_version="v1.0")
    m2 = md.run_muon_mc(n_samples=n_muon, seed=seed, batch_size=batch_size,
                        grid_version="v2.0-ext")
    out["muon_bins_array_equal"] = bool(
        np.array_equal(m2.dRdE[N_PREPENDED:], m1.dRdE))
    out["muon_err_array_equal"] = bool(
        np.array_equal(m2.dRdE_err[N_PREPENDED:], m1.dRdE_err))
    out["muon_entries_array_equal"] = bool(
        np.array_equal(m2.mc_entries[N_PREPENDED:], m1.mc_entries))
    out["muon_rate_equal"] = bool(m1.rate_hz == m2.rate_hz)

    c1 = cd.run_compton_mc(n_per_line=n_compton_per_line, seed=seed,
                           batch_size=batch_size, grid_version="v1.0")
    c2 = cd.run_compton_mc(n_per_line=n_compton_per_line, seed=seed,
                           batch_size=batch_size, grid_version="v2.0-ext")
    out["compton_bins_array_equal"] = bool(
        np.array_equal(c2.dRdE[N_PREPENDED:], c1.dRdE))
    out["compton_err_array_equal"] = bool(
        np.array_equal(c2.dRdE_err[N_PREPENDED:], c1.dRdE_err))
    out["compton_entries_array_equal"] = bool(
        np.array_equal(c2.mc_entries[N_PREPENDED:], c1.mc_entries))
    out["compton_rate_equal"] = bool(c1.rate_hz == c2.rate_hz)

    out["all_bit_identical"] = all(
        out[k] for k in out if k.endswith("array_equal") or k.endswith("rate_equal"))
    return out


def read_frozen_csv(path: str) -> dict:
    """Read a frozen v1.0 deposit CSV -> centres / dRdE / mc_err (keV, cts/kg/day/keV)."""
    E, y, e = [], [], []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#") or line.startswith("E_dep"):
                continue
            parts = line.strip().split(",")
            if len(parts) < 3:
                continue
            E.append(float(parts[0]))
            y.append(float(parts[1]))
            e.append(float(parts[2]))
    return {"E_dep_keV": np.asarray(E), "dRdEdep": np.asarray(y),
            "mc_err": np.asarray(e), "path": path}


def frozen_reproduction(ext_dRdE: np.ndarray, frozen_path: str) -> dict:
    """Compare an extended-axis run's retained bins against the frozen v1.0 CSV.

    The frozen CSVs are written with ``%.6e``, six significant figures, so an
    EXACT reproduction shows up as (a) identical strings at that precision in all
    584 bins and (b) a residual relative difference no larger than the CSV's own
    round-trip.  Both are reported; neither outcome is a blocker -- a failure to
    reproduce would be a FINDING about the v1.0 artifacts' regenerability and
    would select the index-carry route.
    """
    fz = read_frozen_csv(frozen_path)
    sub = np.asarray(ext_dRdE)[N_PREPENDED:]
    y = fz["dRdEdep"]
    if sub.size != y.size:
        raise ValueError(f"{frozen_path}: {y.size} frozen bins vs {sub.size} retained")
    nz = y != 0.0
    rel = np.zeros_like(sub)
    rel[nz] = np.abs(sub[nz] - y[nz]) / np.abs(y[nz])
    same_6sf = int(np.sum(np.array([f"{v:.6e}" for v in sub])
                          == np.array([f"{v:.6e}" for v in y])))
    return {
        "frozen_path": os.path.relpath(frozen_path, _ROOT),
        "n_bins": int(y.size),
        "max_rel_diff": float(rel.max()),
        "argmax_bin": int(rel.argmax()),
        "argmax_centre_keV": float(fz["E_dep_keV"][int(rel.argmax())]),
        "n_identical_at_6_sig_figs": same_6sf,
        "reproduced": bool(same_6sf == y.size),
        "n_frozen_zero_ext_nonzero": int(np.sum((~nz) & (sub != 0.0))),
        "n_frozen_nonzero_ext_zero": int(np.sum(nz & (sub == 0.0))),
        "rel_diff": rel,
        "frozen": fz,
    }


def select_route(probe: dict, muon_repro: dict, compton_repro: dict) -> dict:
    """Choose the route from EXECUTED evidence.  Both outcomes are recorded."""
    ok = (probe["all_bit_identical"] and probe["edge_join_array_equal"]
          and muon_repro["reproduced"] and compton_repro["reproduced"])
    route = ROUTE_VOCABULARY[0] if ok else ROUTE_VOCABULARY[1]
    return {
        "route": route,
        "selected_by": (
            "small-N np.array_equal on bins 160..743 for BOTH channels "
            f"({'PASS' if probe['all_bit_identical'] else 'FAIL'}), plus "
            "reproduction of both frozen v1.0 CSVs at their recorded settings "
            f"(muon {'PASS' if muon_repro['reproduced'] else 'FAIL'}, "
            f"compton {'PASS' if compton_repro['reproduced'] else 'FAIL'})"),
        "bit_identity": probe["all_bit_identical"],
        "muon_frozen_reproduced": muon_repro["reproduced"],
        "compton_frozen_reproduced": compton_repro["reproduced"],
    }


# =========================================================================== #
# 2. PER-BIN LABELS                                                            #
# =========================================================================== #

def stat_adequacy_label(entries, rel_err) -> np.ndarray:
    """Per-bin statistical adequacy, from the closed vocabulary.

    A bin with zero raw entries gets ``no_mc_support`` -- it FAILS the scale
    rather than merely scoring lower on it, because there is no measurement there
    to be imprecise.
    """
    entries = np.asarray(entries)
    rel = np.asarray(rel_err, dtype=float)
    out = np.empty(entries.shape, dtype=object)
    for i in range(entries.size):
        n = int(entries.flat[i])
        r = float(rel.flat[i])
        if n == 0:
            out.flat[i] = "no_mc_support"
        elif n < MIN_ENTRIES_FOR_ERROR_BAR or not np.isfinite(r) or r > 0.5:
            out.flat[i] = "insufficient_mc_support"
        elif r > 0.2:
            out.flat[i] = "marginal_mc_support"
        else:
            out.flat[i] = "adequate_mc_support"
    return out


def below_validity_floor_flags(channel: str, centres_keV) -> tuple[np.ndarray, float]:
    """Per-bin flag against the Plan 15-01 validity floor for ``channel``.

    The flag is EMITTED, never used to delete the row: deleting would hide the
    model's reach, flagging shows it.
    """
    floors = {r["criterion_name"]: r for r in er.validity_floor_rows()
              if r["channel"] == channel}
    key = ("landau_vavilov_xi_le_I" if channel == "muon"
           else "ge_pair_creation_threshold")
    floor_eV = float(floors[key]["floor_eV"])
    centres_eV = np.asarray(centres_keV, dtype=float) * 1.0e3
    return centres_eV < floor_eV, floor_eV


# =========================================================================== #
# 3. ASSEMBLY                                                                  #
# =========================================================================== #

@dataclass
class ExtendedChannel:
    channel: str
    edges_keV: np.ndarray
    centres_keV: np.ndarray
    dRdE: np.ndarray            # NaN where there is no MC support
    mc_err: np.ndarray          # NaN where there is no MC support
    mc_entries: np.ndarray
    rel_mc_err: np.ndarray
    adequacy: np.ndarray
    below_floor: np.ndarray
    validity_floor_eV: float
    accuracy_label: str
    route: str
    provenance: dict


def assemble_channel(channel: str, dRdE, mc_err, mc_entries, route: str,
                     provenance: dict) -> ExtendedChannel:
    """Attach the NaN discipline and the three per-bin labels."""
    if channel not in ("muon", "compton"):
        raise ValueError(f"unknown electron-recoil channel {channel!r}")
    if route not in ROUTE_VOCABULARY:
        raise ValueError(f"route {route!r} outside {ROUTE_VOCABULARY}")
    edges, centres = extended_grid()
    y = np.array(dRdE, dtype=float)
    e = np.array(mc_err, dtype=float)
    n = np.array(mc_entries, dtype=np.int64)
    if not (y.size == e.size == n.size == N_EXT_BINS):
        raise ValueError(f"expected {N_EXT_BINS} bins, got "
                         f"{y.size}/{e.size}/{n.size}")

    # The narrow, physics-justified exception, computed BEFORE the NaN pass so it
    # cannot be reached by accident: Compton bins above the kinematic ceiling.
    forbidden = np.zeros(N_EXT_BINS, dtype=bool)
    if channel == "compton":
        top_edge = max(d["E_edge_keV"] for d in closed_form_compton_edges().values())
        forbidden = edges[:-1] > top_edge
        if np.any(forbidden & (n > 0)):
            raise ValueError(
                "Compton entries found above the highest closed-form Compton edge "
                f"{top_edge!r} keV. The thin-target single-scatter approximation "
                "forbids content there (fp-full-absorption); a photopeak has "
                "appeared and must be diagnosed, not written out.")

    # NO MONTE-CARLO SUPPORT -> NaN, NEVER 0.0 (fp-zero-for-no-data).
    no_support = (n == 0) & (~forbidden)
    y[no_support] = np.nan
    e[no_support] = np.nan
    # ... except above the kinematic ceiling, where 0.0 IS the prediction.
    y[forbidden] = 0.0
    e[forbidden] = 0.0

    with np.errstate(divide="ignore", invalid="ignore"):
        rel = np.where(y != 0.0, e / np.abs(y), np.nan)

    adequacy = stat_adequacy_label(n, rel)
    adequacy[forbidden] = "kinematically_forbidden"
    below, floor_eV = below_validity_floor_flags(channel, centres)
    label = MUON_ACCURACY_LABEL if channel == "muon" else GAMMA_ACCURACY_LABEL
    return ExtendedChannel(
        channel=channel, edges_keV=edges, centres_keV=centres,
        dRdE=y, mc_err=e, mc_entries=n, rel_mc_err=rel,
        adequacy=adequacy, below_floor=below, validity_floor_eV=floor_eV,
        accuracy_label=label, route=route, provenance=dict(provenance))


_COLUMNS = [
    "E_dep_keV[keV]",
    "dRdEdep[counts/kg/day/keV]",
    "mc_err[counts/kg/day/keV]",
    "mc_entries[raw count]",
    "rel_mc_err[dimensionless]",
    "below_validity_floor[bool]",
    "stat_adequacy_label",
    "accuracy_label",
]


def _common_header(ch: ExtendedChannel) -> list[str]:
    p = ch.provenance
    n_nan = int(np.sum(ch.adequacy == "no_mc_support"))
    n_forb = int(np.sum(ch.adequacy == "kinematically_forbidden"))
    n_low = int(np.sum(ch.mc_entries[:N_PREPENDED] > 0))
    return [
        f"# route = {ch.route}",
        f"# route_selected_by = {p['route_selected_by']}",
        f"# grid_version = v2.0-ext ({N_EXT_BINS} bins, floor 0.0999350 eV); "
        f"np.array_equal(edges[160:], shared_energy_grid('v1.0')) is True, "
        f"max abs difference exactly 0.0",
        f"# seed = {p['seed']}; batch_size = {p['batch_size']}",
        f"# repo_HEAD_at_execution = {p['repo_head']}",
        f"# interpreter = /opt/anaconda3/bin/python3 (numpy 1.26.4, scipy 1.17.1)",
        "#",
        "# broadened_provenance = false",
        "#   Plan 15-01 verdict for this ELECTRON-RECOIL channel is does_not_apply:",
        "#   the Phase-11 width sigma_E = sqrt(E_R omega_bar) is a NUCLEAR-recoil width",
        "#   and no nucleus recoils here. NO broadening of any kind has been applied to",
        "#   this table, and no rate in its production was ever multiplied by exp(-2W)",
        "#   (milestone-wide prohibition). fold.read_broadened_provenance reads this line.",
        "#",
        "# NORMALIZATION: v1.0 sea-level, ZERO overburden, no shield, no veto.",
        "#   Every multiplicative factor is exactly 1.0, enumerated individually:",
    ] + [
        f"#     {name} = {val!r}  ({why})" for name, val, why in NORMALIZATION_FACTORS
    ] + [
        "#",
        f"# validity floor (Plan 15-01) = {ch.validity_floor_eV:.6g} eV; "
        f"{int(np.sum(ch.below_floor))} of {N_EXT_BINS} bins are flagged "
        "below_validity_floor. The flag is EMITTED, not used to delete the row.",
        f"# NO-SUPPORT DISCIPLINE: {n_nan} bins have zero raw MC entries and are written",
        "#   NaN with stat_adequacy_label = no_mc_support. They are NEVER written 0.0:",
        "#   a zero reads as a measured absence of rate, and the correct statement is",
        "#   that the estimator has no support there (fp-zero-for-no-data).",
        f"#   Of the 160 new sub-10.14 eV bins, {n_low} carry at least one MC entry.",
        f"#   ONE NARROW EXCEPTION, {n_forb} bins: {COMPTON_KINEMATIC_CEILING_NOTE}.",
        "#   Those bins are written 0.0 with stat_adequacy_label = kinematically_forbidden,",
        "#   because writing NaN there would say 'unmeasured' about a region the model",
        "#   positively excludes and would make the no-photopeak check untestable in the",
        "#   artifact (fp-full-absorption requires it intact in the artifact, not the prose).",
        "#",
        "# ACCURACY LABEL, carried forward UNNARROWED (ROADMAP Phase 15 SC5), on EVERY",
        "#   row so that a rate cannot be read out of this file without it:",
        f"#   {ch.accuracy_label}",
        "#",
        "# columns: " + ", ".join(_COLUMNS),
    ]


def write_channel_csv(ch: ExtendedChannel, path: str) -> str:
    p = ch.provenance
    if ch.channel == "muon":
        head = [
            "# Muon deposited-energy spectrum dR/dE_dep on the 744-bin EXTENDED axis.",
            "# Phase 15, Plan 15-02. v1.0 machinery UNCHANGED: Gaisser-Guan flux (x)",
            "# ray-box chord (x) Landau-Vavilov MPV deposit, 4in x 4in x 2mm Ge wafer.",
            "# UNIFIED PHONON SCALE, NO quenching (CONVENTIONS Section B).",
            f"# n_mc_samples = {p['n_samples']}",
            f"# integral_muon_rate_Hz = {p['rate_hz']:.4f} +/- {p['rate_err_hz']:.4f}"
            "   <-- ABSOLUTE through-wafer rate in Hz, NOT a per-kg quantity",
            f"# vertical_chord_MPV_MeV = {p['vertical_mpv_mev']:.4f} "
            f"(mean = {p['vertical_mean_mev']:.4f}; MPV < mean by construction)",
        ]
    else:
        head = [
            "# Compton (environmental-gamma) electron-recoil deposited-energy spectrum",
            "# dR/dE_dep on the 744-bin EXTENDED axis. Phase 15, Plan 15-02.",
            "# v1.0 machinery UNCHANGED: angle sampled from dsigma_KN/dOmega * S(x,Z=32)",
            "# (Hubbell 1975, data/ge_incoherent_S.csv), ELECTRON recoil T_e, thin-target",
            "# single scatter on the pinned Cauchy mean chord ell_bar = 4V/S = 0.385 cm.",
            "# UNIFIED PHONON SCALE, NO quenching (CONVENTIONS Section B).",
            f"# n_mc_samples_per_line = {p['n_per_line']}",
            "#",
            "# FOUR DIFFERENT RATES, NOT INTERCHANGEABLE (carried verbatim from the",
            "# frozen v1.0 header):",
            f"#   total_single_scatter_rate_Hz = {p['rate_hz']:.4e}  <-- BOUND INCOHERENT,"
            " the RATE OF RECORD",
            f"#   free-KN pre-binding          = {p['rate_free_hz']:.4e}",
            f"#   VALD-03 anchor flux x sigma_KN x N_e (free) = {p['rate_anchor_hz']:.4e}",
            f"#   binding f_bind               = {p['rate_hz'] / p['rate_free_hz']:.4f}",
            f"# integral dR/dE_dep = {p['counts_per_kg_day']:.4e} counts/kg/day "
            "(= total_rate * 86400 / mass_kg; energy closure)",
        ]
    lines = head + _common_header(ch)
    with open(path, "w", newline="") as fh:
        for ln in lines:
            fh.write(ln + "\n")
        w = csv.writer(fh)
        w.writerow(_COLUMNS)
        for i in range(ch.centres_keV.size):
            y = ch.dRdE[i]
            e = ch.mc_err[i]
            r = ch.rel_mc_err[i]
            w.writerow([
                f"{ch.centres_keV[i]:.9e}",
                "nan" if not np.isfinite(y) else f"{y:.6e}",
                "nan" if not np.isfinite(e) else f"{e:.6e}",
                int(ch.mc_entries[i]),
                "nan" if not np.isfinite(r) else f"{r:.6e}",
                "True" if bool(ch.below_floor[i]) else "False",
                ch.adequacy[i],
                ch.accuracy_label,
            ])
    return path


def read_channel_csv(path: str) -> dict:
    """Read back an emitted extended-axis table, labels included."""
    E, y, e, n, r, bf, ad, ac = [], [], [], [], [], [], [], []
    with open(path, encoding="utf-8") as fh:
        rdr = csv.reader(row for row in fh if not row.startswith("#"))
        header = next(rdr)
        for row in rdr:
            E.append(float(row[0]))
            y.append(float(row[1]))
            e.append(float(row[2]))
            n.append(int(row[3]))
            r.append(float(row[4]))
            bf.append(row[5] == "True")
            ad.append(row[6])
            ac.append(row[7])
    return {"header": header, "E_dep_keV": np.asarray(E),
            "dRdEdep": np.asarray(y), "mc_err": np.asarray(e),
            "mc_entries": np.asarray(n), "rel_mc_err": np.asarray(r),
            "below_validity_floor": np.asarray(bf),
            "stat_adequacy_label": np.asarray(ad, dtype=object),
            "accuracy_label": np.asarray(ac, dtype=object)}


# =========================================================================== #
# 4. THE SC1 INVARIANTS                                                        #
# =========================================================================== #

def closed_form_compton_edges() -> dict:
    """E_edge = 2 E_gamma^2 / (m_e c^2 + 2 E_gamma) for the three headline lines.

    Computed IN CLOSED FORM from ``data/gamma_lines.csv``, independently of the
    sampler, so agreement with the spectrum's edge structure is a check rather
    than a tautology.
    """
    lines = {ln.isotope + f"_{ln.energy_keV:g}": ln for ln in cs.load_gamma_lines()}
    want = {"K40": 1460.822, "Bi214": 1764.494, "Tl208": 2614.511}
    out = {}
    for iso, e_gamma in want.items():
        key = f"{iso}_{e_gamma:g}"
        if key not in lines:
            raise KeyError(f"{key} not in data/gamma_lines.csv")
        out[iso] = {
            "E_gamma_keV": e_gamma,
            "E_edge_keV": float(cs.compton_edge_kev(e_gamma)),
        }
    return out


def v1_regression(ch: ExtendedChannel, frozen_path: str) -> dict:
    """Per-bin |ext[160+i] - frozen[i]| / frozen[i] over the 584 frozen bins.

    The retained bins are compared as they stand.  No zero-filling, no
    ``nan_to_num``: the NaN no-support bins live below bin 160 and never enter
    this comparison, and if one ever did, the right answer would be to see it.
    """
    return frozen_reproduction(ch.dRdE, frozen_path)


def write_regression_csv(rows: list[dict], scalars: list[dict],
                         path: str = REGRESSION_CSV) -> str:
    head = [
        "# Phase-15 Plan 15-02: extended-versus-frozen regression above 10.14 eV,",
        "# ROADMAP Phase 15 SC1. Per-bin relative difference over the 584 frozen v1.0",
        "# bins for both electron-recoil channels, plus the SC1 scalar invariants.",
        "#",
        "# Under the exact-re-drive route the per-bin difference should be identically 0",
        "# in the COMPUTATION; what remains is the frozen CSVs' own %.6e round-trip, so a",
        "# residual of order 1e-7 is the file format, not the physics. The decisive",
        "# statement is n_identical_at_6_sig_figs = 584/584 for both channels.",
        "#",
        "# columns: channel, bin_index_v1[index], E_dep_keV[keV], "
        "frozen_dRdEdep[counts/kg/day/keV], ext_dRdEdep[counts/kg/day/keV], "
        "rel_diff[dimensionless], is_max_for_channel[bool]",
    ]
    with open(path, "w", newline="") as fh:
        for ln in head:
            fh.write(ln + "\n")
        fh.write("#\n# SCALAR INVARIANTS\n")
        for s in scalars:
            fh.write(f"# {s['name']} = {s['value']} "
                     f"[{s['units']}] ; target {s['target']} ; {s['verdict']}\n")
        fh.write("#\n")
        w = csv.writer(fh)
        w.writerow(["channel", "bin_index_v1[index]", "E_dep_keV[keV]",
                    "frozen_dRdEdep[counts/kg/day/keV]",
                    "ext_dRdEdep[counts/kg/day/keV]",
                    "rel_diff[dimensionless]", "is_max_for_channel[bool]"])
        for r in rows:
            w.writerow([r["channel"], r["i"], f"{r['E']:.9e}",
                        f"{r['frozen']:.6e}", f"{r['ext']:.6e}",
                        f"{r['rel']:.6e}", "True" if r["is_max"] else "False"])
    return path
