# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
#
# Phase-5 (Plan 05-02) Monte-Carlo response matrix R(E_rec | E_dep).
#
# SCOPE (SIMU-02): assemble the bandwidth-limited transfer function
#   R(E_rec | E_dep) -- the normalized conditional distribution of reconstructed
#   energy given a deposited energy -- PER DESIGN (Ta->Al, Al->Hf) and PER
#   CENSORING VARIANT (non_paralyzable, paralyzable), spanning the CEvNS sub-keV
#   floor through the 197 MeV cosmic-muon tail, i.e. the linear -> saturated
#   range. R (NOT a folded spectrum) is the deliverable; folding the CEvNS /
#   muon / Compton deposit spectra through R is Phase 6 (SIMU-03).
#
# It REUSES the Plan 05-01 forward chain WITHOUT re-implementing it:
#   * qpd_potential.response.expected_event_count  -- the Pitfall-1 event-count
#     mapping ec = INT Gamma_in dt = K*tau_qp*N_qp/V_tr (NOT the trapped N_qp),
#   * qpd_potential.response.censored_count        -- the analytic dead-time
#     closed-form observed count (the deliverable estimator's per-sensor mean),
#   * qpd_potential.response.emg_pulse_params + the MUST-USE ref-qpd-repo
#     QuasiparticleBurstModel EMG template (via response.realize_event_train /
#     censor_event_train) -- the tunneling-EVENT realization,
#   * qpd_potential.response.calibrate_C           -- the single global per-design
#     count->energy constant fixing the low-E slope dE_rec/dE_dep =
#     params.CALIB_SLOPE = 1.0 (USER DECISION 2026-07-25; was eps = 0.5). E_rec
#     ESTIMATES the deposit: on-detector calibration absorbs the physical
#     deposit->QP conversion fraction eps into C, so a 10 eV deposit reconstructs
#     at 10 eV. Saturation above the onset is still never unfolded.
#   * qpd_potential.response.crossover_band / whole_array_plateau_energy -- the
#     per-design saturation onset / plateau scales marked on the figure.
#
# MONTE-CARLO STRATEGY (documented, honest):
#   For each E_dep column (uniform importance sampling in log E_dep on the
#   Phase-4 grid), N_s stochastic forward realizations of the SUMMED censored
#   count over the ~10,300-sensor array give the conditional distribution of
#   E_rec = C * total_N_obs. Per realization the ~pi r^2 on-spot sensors and the
#   ~10,287 identical off-spot sensors are drawn as an AGGREGATE ensemble (one
#   multinomial / Poisson draw per class per realization -- never a 10,300 python
#   loop). The per-sensor observed-count DISTRIBUTION is obtained by:
#     (a) ec <= EC_EMG_MAX  (linear -> mild saturation, feasible):
#           the MUST-USE EMG event train (response.realize/censor) -> empirical
#           per-sensor pmf; the aggregate class sum is multinomial over that pmf.
#     (b) ec >  EC_EMG_MAX  (deep saturation, EMG event train is O(1e8) events
#           and INFEASIBLE to realize):  the observed REGISTERED count is
#           dead-time regularized and bounded (~ pulse_duration / tau_d ~ O(1e2)
#           per sensor); its counting statistics are modeled as Poisson about the
#           analytic censored_count mean.  In this regime the *relative* spread
#           of the summed E_rec is ~1/sqrt(N_sensors * count) ~ 1e-3, so the
#           column is ~a delta and the model choice is immaterial; the branch
#           exists only because the EMG event train cannot be materialized.
#   In BOTH branches the per-class MEAN is pinned to the analytic
#   response.censored_count (the validated Plan 05-01 deliverable estimator), so
#   the response CURVE (median E_rec vs E_dep) is exactly the analytic estimator
#   -- continuous across the branch, no spurious kink -- while the branch sets
#   only the fluctuation SHAPE.  See ASSUMPTIONS.md / SUMMARY for the caveat.
#
# HONESTY (carried on the figure + npz provenance):
#   The saturated-regime response SHAPE has NO literature anchor at any energy
#   (Plan 05-01); the low-E 0.5 slope is CALIBRATION-consistency, not validation;
#   the muon-end ceiling pile-up is an instrument artifact of the modeled
#   saturation, NOT a physical spectral peak (Pitfall 5).  Both censoring
#   variants are carried (OPEN switch, CONVENTIONS F) -- never silently closed
#   (fp-single-censoring) -- and no curve ramps linearly to tens of MeV
#   (fp-no-saturation).  The time-over-saturation estimator is a clearly LABELED
#   SECONDARY variant, never auto-switched into the baseline (fp-tos-autoswitch).
#
# UNITS (CONVENTIONS Section A.1): energy eV internal; time s; rate Hz. R columns
# are dimensionless probabilities that sum to 1 over the E_rec bins.

from __future__ import annotations

import argparse
import json
import os
import zlib
from dataclasses import dataclass, asdict
from typing import Optional

import numpy as np

from . import params
from . import energy_scale as es
from . import response as resp
from . import muon_deposit as md

# --------------------------------------------------------------------------- #
# Defaults (all overridable; recorded in the npz metadata for reproducibility)  #
# --------------------------------------------------------------------------- #

DEFAULT_SEED = 20260721                 # Plan 05-02 fixed RNG seed
DEFAULT_N_S = 5000                      # forward realizations per E_dep column
DEFAULT_M_POOL = 2000                   # EMG per-sensor pool size (feasible regime)
DEFAULT_EC_EMG_MAX = 2000.0             # ec above which the EMG event train is infeasible
DEFAULT_EREC_BINS_PER_DECADE = 20       # global log E_rec binning
DEFAULT_EREC_MIN_eV = 1.0e-3            # E_rec grid floor (underflow bin below this)
DEFAULT_EREC_MAX_eV = 1.0e5             # E_rec grid ceiling (> non_par plateau ~3.5e4)

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
_COMBINED_CSV = os.path.join(_PROJECT_ROOT, "data", "combined_dRdEdep.csv")
_ARTIFACT_DIR = os.path.join(_PROJECT_ROOT, "artifacts", "stage1")

DESIGN_FILE = {"Ta->Al": "response_matrix_TaAl.npz", "Al->Hf": "response_matrix_AlHf.npz"}


# --------------------------------------------------------------------------- #
# Grids                                                                        #
# --------------------------------------------------------------------------- #


def load_E_dep_grid_eV(csv_path: str = _COMBINED_CSV) -> np.ndarray:
    """Phase-4 deposited-energy grid CENTERS [eV] from data/combined_dRdEdep.csv.

    The E_dep columns of R are placed on the IDENTICAL log grid used by the
    Phase-4 muon+Compton deposit spectra (~80 bins/decade, ~10 eV -> 2e5 keV) so
    R composes cleanly with them in Phase 6.  The CSV column is keV; returned in
    eV.  The CEvNS grid (5 - 3200 eV_nr) lies inside this range except the sub-
    threshold 5-10 eV sliver.
    """
    # Skip '#'-comment lines AND the (non-commented) column-name header row.
    vals = []
    with open(csv_path) as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            tok = s.split(",", 1)[0]
            try:
                vals.append(float(tok))
            except ValueError:
                continue  # column-name header row
    E_keV = np.asarray(vals, dtype=float)
    return np.sort(E_keV) * 1.0e3  # keV -> eV


def E_dep_grid_from_shared_grid_eV(version: str = "v1.0") -> np.ndarray:
    """Deposit-axis CENTRES [eV] computed from the grid function. Plan 10-03.

    Centres are the GEOMETRIC MEANS of adjacent ``shared_energy_grid(version)``
    edges (the v1.0 Phase-4 convention), converted keV -> eV.

    WHY THIS EXISTS. ``load_E_dep_grid_eV`` parses
    ``data/combined_dRdEdep.csv``, which makes the response matrix's deposit
    axis a function of an ARCHIVED PHASE-4 PRODUCT. That axis cannot be extended
    without re-running the Phase-4 muon and Compton Monte Carlo, which is Phase
    15's job. This route decouples the axis from the archive so plan 10-04 can
    regenerate R on the 744-bin extended axis. The CSV parser is kept unchanged
    so the archived provenance stays readable.

    MEASURED DISCREPANCY BETWEEN THE TWO ROUTES. The CSV centres are
    round-tripped through a decimal text representation and deviate from the
    exact geometric means by up to **4.918e-07 relative** (CSV first centre
    10.144970 eV vs exact 10.144972680282425 eV). The archived
    ``artifacts/stage1/response_matrix_*.npz`` were built on the CSV values.
    **Bit-identical reproduction of the archived matrices is therefore NOT
    achievable and must not be promised** (``fp-bit-identical-promise``).
    """
    edges_keV = md.shared_energy_grid(version)
    centres_keV = np.sqrt(edges_keV[:-1] * edges_keV[1:])
    return centres_keV * 1.0e3


def _git_sha() -> str:
    """Short git SHA of the working tree, for the npz provenance header."""
    import subprocess
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                             cwd=_PROJECT_ROOT, capture_output=True,
                             text=True, timeout=10).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain"],
                               cwd=_PROJECT_ROOT, capture_output=True,
                               text=True, timeout=10).stdout.strip()
        return sha + ("-dirty" if dirty else "") if sha else "unknown"
    except Exception:                                    # pragma: no cover
        return "unknown"


def _log_edges_from_centers(centers: np.ndarray) -> np.ndarray:
    """Geometric-midpoint bin edges for a log-spaced set of centers."""
    c = np.asarray(centers, dtype=float)
    mid = np.sqrt(c[:-1] * c[1:])
    first = c[0] * c[0] / mid[0]
    last = c[-1] * c[-1] / mid[-1]
    return np.concatenate([[first], mid, [last]])


def build_E_rec_edges_eV(
    bins_per_decade: int = DEFAULT_EREC_BINS_PER_DECADE,
    e_min: float = DEFAULT_EREC_MIN_eV,
    e_max: float = DEFAULT_EREC_MAX_eV,
) -> np.ndarray:
    """Global log-spaced E_rec bin edges [eV], with an explicit [0, e_min)
    underflow bin prepended (zero-count / sub-threshold realizations land here).
    """
    n_dec = np.log10(e_max / e_min)
    n = int(round(bins_per_decade * n_dec))
    log_edges = np.logspace(np.log10(e_min), np.log10(e_max), n + 1)
    return np.concatenate([[0.0], log_edges])  # underflow bin [0, e_min)


# --------------------------------------------------------------------------- #
# Fast dead-time censoring (semantics IDENTICAL to response.censor_event_train, #
# but O(n_registered) not O(n_events) -- via searchsorted jumps -- so saturated  #
# trains with O(1e5) events censor in O(1e2) steps). Cross-checked in tests.     #
# --------------------------------------------------------------------------- #


def censor_fast(event_times: np.ndarray, variant: str, tau_d: Optional[float] = None) -> int:
    """Observed (registered) count after dead-time censoring of an event train."""
    if tau_d is None:
        tau_d = params.TAU_D.value
    ev = np.sort(np.asarray(event_times, dtype=float))
    n = ev.size
    if n == 0:
        return 0
    if variant == "paralyzable":
        # EVERY event restarts the dead window; an event registers iff the
        # preceding event is > tau_d earlier. First event always registers.
        return int(1 + np.count_nonzero(np.diff(ev) > tau_d))
    if variant == "non_paralyzable":
        # Dead window restarts only from REGISTERED events; jump event->event.
        count = 1
        i = 0
        while True:
            j = int(np.searchsorted(ev, ev[i] + tau_d, side="right"))
            if j >= n:
                break
            count += 1
            i = j
        return count
    raise ValueError(
        f"unknown censoring variant {variant!r}; expected one of {params.CENSORING_VARIANTS}"
    )


# --------------------------------------------------------------------------- #
# Per-sensor EMG pool (MUST-USE ref-qpd-repo template) -> empirical count pmf    #
# --------------------------------------------------------------------------- #


def emg_count_pool(
    N_qp: float, design: es.Design, variant: str, M: int, rng: np.random.Generator
) -> np.ndarray:
    """Pool of M realized per-sensor observed counts via the MUST-USE EMG template.

    Reuses response.emg_pulse_params + the ref-qpd-repo QuasiparticleBurstModel:
    one model with M identical bursts, expected_n_qp = ec (the Pitfall-1 event
    count), then dead-time censoring of each burst's event train.  This is the
    feasible-regime realization; each burst carries ec ~<= EC_EMG_MAX events.
    """
    d = es.resolve_design(design)
    tau, mu0, sigma = resp.emg_pulse_params(d.name)
    ec = float(resp.expected_event_count(N_qp, d))
    if ec <= 0.0:
        return np.zeros(M, dtype=float)
    model = resp.QuasiparticleBurstModel(
        times=[0.0] * M, tau=tau, mu=mu0, sigma=sigma, expected_n_qp=ec
    )
    _events, truth = model.sample(rng)
    return np.array(
        [censor_fast(t.event_times, variant) for t in truth], dtype=float
    )


# --------------------------------------------------------------------------- #
# Aggregate class sum (on-spot ~pi r^2 sensors OR off-spot ~10,287 sensors)      #
# --------------------------------------------------------------------------- #


@dataclass
class ClassDiag:
    branch: str          # "emg" | "poisson_saturated" | "zero"
    ec: float            # per-sensor event count (Pitfall-1 mapping)
    mu_analytic: float   # per-sensor analytic censored mean (response.censored_count)
    mu_pool: float       # per-sensor EMG-pool mean (nan if poisson branch)
    n_sensors: float     # sensors in this class (fractional pi r^2 allowed)


def class_sum_samples(
    N_qp: float,
    n_sensors: float,
    design: es.Design,
    variant: str,
    N_s: int,
    rng: np.random.Generator,
    *,
    M_pool: int = DEFAULT_M_POOL,
    ec_emg_max: float = DEFAULT_EC_EMG_MAX,
) -> tuple[np.ndarray, ClassDiag]:
    """N_s realizations of the SUMMED observed count over `n_sensors` identical
    sensors, with the per-class mean pinned to n_sensors * response.censored_count.

    Fractional n_sensors (= pi r^2, or n_sensors - pi r^2) is handled as
    floor(n) aggregate + a fractional single-sensor contribution, so the mean is
    exact.
    """
    d = es.resolve_design(design)
    ec = float(resp.expected_event_count(N_qp, d))
    mu_a = float(resp.censored_count(N_qp, d, variant=variant))

    if ec <= 0.0 or n_sensors <= 0.0:
        return np.zeros(N_s, dtype=float), ClassDiag("zero", ec, mu_a, float("nan"), n_sensors)

    n_full = int(np.floor(n_sensors))
    frac = float(n_sensors - n_full)

    if ec <= ec_emg_max:
        # (a) MUST-USE EMG realization -> empirical per-sensor pmf.
        pool = emg_count_pool(N_qp, d, variant, M_pool, rng)
        mu_pool = float(pool.mean())
        kmax = int(pool.max())
        pmf = np.bincount(pool.astype(int), minlength=kmax + 1).astype(float)
        pmf /= pmf.sum()
        kvals = np.arange(pmf.size, dtype=float)
        # aggregate floor(n) sensors as one multinomial draw per realization
        if n_full > 0:
            mm = rng.multinomial(n_full, pmf, size=N_s)  # (N_s, K)
            sums = mm @ kvals
        else:
            sums = np.zeros(N_s, dtype=float)
        if frac > 0.0:
            extra = rng.choice(kvals, size=N_s, p=pmf)
            sums = sums + frac * extra
        # pin the class MEAN to the analytic estimator (rescale ~1 in this regime)
        if mu_pool > 0.0:
            sums = sums * (mu_a / mu_pool)
        return sums, ClassDiag("emg", ec, mu_a, mu_pool, n_sensors)

    # (b) deep saturation: EMG event train infeasible; registered-count Poisson
    #     about the analytic mean (spread negligible vs the column mean here).
    sums = rng.poisson(n_sensors * mu_a, size=N_s).astype(float)
    return sums, ClassDiag("poisson_saturated", ec, mu_a, float("nan"), n_sensors)


# --------------------------------------------------------------------------- #
# Single-column forward realization of E_rec                                    #
# --------------------------------------------------------------------------- #


def E_rec_samples(
    E_dep_eV: float,
    design: es.Design,
    variant: str,
    C: float,
    rng: np.random.Generator,
    *,
    f_prompt: Optional[float] = None,
    r: Optional[float] = None,
    n_sensors: Optional[float] = None,
    N_s: int = DEFAULT_N_S,
    M_pool: int = DEFAULT_M_POOL,
    ec_emg_max: float = DEFAULT_EC_EMG_MAX,
) -> tuple[np.ndarray, dict]:
    """N_s realizations of E_rec = C * (on-spot sum + off-spot sum) for one deposit."""
    d = es.resolve_design(design)
    if f_prompt is None:
        f_prompt = params.F_PROMPT.value
    if r is None:
        r = params.R_SPOT.value
    if n_sensors is None:
        n_sensors = params.N_SENSORS.value

    n_spot = float(np.pi * r * r)
    n_off = float(n_sensors - n_spot)
    E_on = float(es.sensor_energy_split(E_dep_eV, f_prompt, r, n_sensors, on_spot=True))
    E_off = float(es.sensor_energy_split(E_dep_eV, f_prompt, r, n_sensors, on_spot=False))
    N_on = float(es.n_qp_yield(E_on, d))
    N_off = float(es.n_qp_yield(E_off, d))

    on_sum, diag_on = class_sum_samples(
        N_on, n_spot, d, variant, N_s, rng, M_pool=M_pool, ec_emg_max=ec_emg_max
    )
    off_sum, diag_off = class_sum_samples(
        N_off, n_off, d, variant, N_s, rng, M_pool=M_pool, ec_emg_max=ec_emg_max
    )
    E_rec = C * (on_sum + off_sum)
    diag = {
        "E_dep_eV": float(E_dep_eV),
        "on": asdict(diag_on),
        "off": asdict(diag_off),
        "peak_gamma_on": float(es.peak_tunneling_rate(N_on, d)),
    }
    return E_rec, diag


# --------------------------------------------------------------------------- #
# Time-over-saturation SECONDARY estimator (LABELED; never auto-switched)        #
# --------------------------------------------------------------------------- #


def time_over_saturation_curve(
    E_dep_grid_eV: np.ndarray,
    design: es.Design,
    *,
    f_prompt: Optional[float] = None,
    r: Optional[float] = None,
    n_sensors: Optional[float] = None,
    ceiling_hz: float = resp.SATURATION_CEILING_HZ,
) -> dict:
    """SECONDARY, UNVALIDATED time-over-saturation estimator (fp-tos-autoswitch
    guard: kept separate, NEVER blended into the count-integral baseline).

    t_over(E_dep) = duration the on-spot pulse rate Gamma_in(t) exceeds the 25 kHz
    ceiling; logarithmic in E_dep (~ tau_qp * ln(peak_Gamma/ceiling)).  Offered
    only to show recoverable high-E ORDERING once the count-integral has
    saturated; tau_qp is held fixed (Rothwarf-Taylor tau_qp ~ 1/n_qp is NOT
    modeled -> MEDIUM/LOW, no anchor).
    """
    d = es.resolve_design(design)
    if f_prompt is None:
        f_prompt = params.F_PROMPT.value
    if r is None:
        r = params.R_SPOT.value
    if n_sensors is None:
        n_sensors = params.N_SENSORS.value

    t_grid = resp._default_time_grid(d, span=60.0, n=40000)
    g = resp.pulse_shape(t_grid, d, normalized=True)  # unit-area shape [1/s]
    t_over = np.zeros_like(E_dep_grid_eV, dtype=float)
    for i, E in enumerate(E_dep_grid_eV):
        E_on = es.sensor_energy_split(float(E), f_prompt, r, n_sensors, on_spot=True)
        N_on = es.n_qp_yield(E_on, d)
        ec = resp.expected_event_count(N_on, d)
        gamma = ec * g  # Gamma_in(t) [Hz]
        above = gamma > ceiling_hz
        if np.any(above):
            t_over[i] = float(np.trapz(above.astype(float), t_grid))
    return {"design": d.name, "E_dep_eV": np.asarray(E_dep_grid_eV, float), "t_over_s": t_over}


# --------------------------------------------------------------------------- #
# Full response matrix R(E_rec | E_dep) for one design + variant                #
# --------------------------------------------------------------------------- #


#: Fixed-precision canonical form of a deposit centre, used as the sub-seed key.
#: 12 significant digits: the grid spacing is 1.25e-2 dex ~ 2.9% between adjacent
#: centres, so no two columns can collide, while the 4.918e-07 CSV-vs-exact
#: centre discrepancy IS resolved -- i.e. the CSV-sourced and grid-sourced axes
#: deliberately produce DIFFERENT seeds, which is why plan 10-04 compares against
#: the archived matrices statistically rather than bitwise.
_SEED_KEY_FORMAT = "%.12e"


def column_seed_sequence(seed: int, design_name: str, variant: str,
                         E_dep_eV: float) -> np.random.SeedSequence:
    """Per-column MC sub-seed, a stable function of the column's DEPOSIT ENERGY.

    Plan 10-03. The pre-existing scheme was::

        ss = SeedSequence([seed, crc32(design), crc32(variant)])
        child_seeds = ss.spawn(n_edep)
        rng = default_rng(child_seeds[j])          # j is the ORDINAL INDEX

    so a column's sub-seed was a function of *how many columns sat below it*.
    Prepending the 160 sub-eV columns of the extended axis shifts every index and
    therefore RE-SEEDS every column above 10.14 eV. Any comparison of the
    regenerated matrix against v1.0 would then be pure Monte Carlo noise, and a
    real regression of order that noise would be invisible (``fp-ordinal-seed``).

    Keying on the deposit energy instead makes the sub-seed independent of the
    column count and of the column order. Stability across processes is
    preserved by using ``zlib.crc32``, never Python's per-process-salted builtin
    ``hash`` -- the same reason the original scheme used crc32 on the design and
    variant names.
    """
    key = zlib.crc32((_SEED_KEY_FORMAT % float(E_dep_eV)).encode())
    return np.random.SeedSequence(
        [int(seed), zlib.crc32(design_name.encode()), zlib.crc32(variant.encode()), key]
    )


def build_matrix(
    design: es.Design,
    variant: str,
    E_dep_centers_eV: np.ndarray,
    E_rec_edges_eV: np.ndarray,
    *,
    seed: int = DEFAULT_SEED,
    N_s: int = DEFAULT_N_S,
    M_pool: int = DEFAULT_M_POOL,
    ec_emg_max: float = DEFAULT_EC_EMG_MAX,
    f_prompt: Optional[float] = None,
    r: Optional[float] = None,
    n_sensors: Optional[float] = None,
) -> dict:
    """Assemble R (n_Erec, n_Edep), per-cell counts + relative MC error, and the
    per-column median / 16-84 percentile E_rec band.
    """
    d = es.resolve_design(design)
    resp.assert_trapping_gate(d)  # Ta binary trapping gate (fp-ta-band)
    C = resp.calibrate_C(d, variant, f_prompt=f_prompt, r=r, n_sensors=n_sensors)

    n_erec = E_rec_edges_eV.size - 1
    n_edep = E_dep_centers_eV.size
    counts = np.zeros((n_erec, n_edep), dtype=float)
    R = np.zeros((n_erec, n_edep), dtype=float)
    err = np.full((n_erec, n_edep), np.nan, dtype=float)
    med = np.zeros(n_edep, dtype=float)
    lo = np.zeros(n_edep, dtype=float)
    hi = np.zeros(n_edep, dtype=float)
    mean_curve = np.zeros(n_edep, dtype=float)
    n_obs_mean = np.zeros(n_edep, dtype=float)
    p_zero = np.zeros(n_edep, dtype=float)
    n_distinct = np.zeros(n_edep, dtype=int)
    spread = np.zeros(n_edep, dtype=float)
    n_off_hi = np.zeros(n_edep, dtype=int)
    n_off_lo = np.zeros(n_edep, dtype=int)

    # column-deterministic sub-seeding, keyed to the column's DEPOSIT ENERGY.
    # See column_seed_sequence: the pre-10-03 ordinal scheme would have re-seeded
    # every column above 10.14 eV when 160 columns were prepended.
    for j, E in enumerate(E_dep_centers_eV):
        rng = np.random.default_rng(
            column_seed_sequence(seed, d.name, variant, float(E)))
        samples, _diag = E_rec_samples(
            float(E), d, variant, C, rng,
            f_prompt=f_prompt, r=r, n_sensors=n_sensors,
            N_s=N_s, M_pool=M_pool, ec_emg_max=ec_emg_max,
        )
        # PLAN 10-04, fp-renormalised-conservation. Count samples that fall OFF
        # the E_rec grid BEFORE histogramming. np.histogram silently discards
        # anything above the top edge, and `col = h / h.sum()` then renormalises
        # whatever is left, so the column always sums to 1 no matter how much
        # probability was thrown away. The conservation test is meaningless
        # without this counter.
        n_off_hi[j] = int(np.count_nonzero(samples > E_rec_edges_eV[-1]))
        n_off_lo[j] = int(np.count_nonzero(samples < E_rec_edges_eV[0]))
        h, _ = np.histogram(samples, bins=E_rec_edges_eV)
        counts[:, j] = h
        col = h / h.sum() if h.sum() > 0 else h
        R[:, j] = col
        nz = h > 0
        err[nz, j] = 1.0 / np.sqrt(h[nz])  # Poisson relative MC error per cell
        med[j] = float(np.median(samples))
        lo[j] = float(np.percentile(samples, 16))
        hi[j] = float(np.percentile(samples, 84))
        mean_curve[j] = float(samples.mean())
        # Sub-eV diagnostics (plan 10-04 claim-subev-diagnosed). E_rec = C * N_obs,
        # so the registered count and its discreteness are recoverable exactly.
        n_obs = samples / C if C > 0 else samples
        n_obs_mean[j] = float(n_obs.mean())
        p_zero[j] = float(np.count_nonzero(samples <= 0.0) / samples.size)
        n_distinct[j] = int(np.unique(samples).size)
        spread[j] = float(samples.std(ddof=1) / samples.mean()) if samples.mean() > 0 else np.nan

    return {
        "design": d.name,
        "variant": variant,
        "C_eV_per_event": float(C),
        "R": R,
        "counts": counts,
        "err": err,
        "E_rec_median_eV": med,
        "E_rec_p16_eV": lo,
        "E_rec_p84_eV": hi,
        "E_rec_mean_eV": mean_curve,
        "N_obs_mean": n_obs_mean,
        "P_zero_count": p_zero,
        "n_distinct_Erec": n_distinct,
        "rel_spread": spread,
        "n_offgrid_high": n_off_hi,
        "n_offgrid_low": n_off_lo,
    }


# --------------------------------------------------------------------------- #
# Driver: assemble both designs x both variants + secondary, write npz          #
# --------------------------------------------------------------------------- #


def run_design(
    design_name: str,
    *,
    seed: int = DEFAULT_SEED,
    N_s: int = DEFAULT_N_S,
    M_pool: int = DEFAULT_M_POOL,
    ec_emg_max: float = DEFAULT_EC_EMG_MAX,
    bins_per_decade: int = DEFAULT_EREC_BINS_PER_DECADE,
    csv_path: str = _COMBINED_CSV,
    write: bool = True,
    out_dir: str = _ARTIFACT_DIR,
    grid_version: Optional[str] = None,
    file_name: Optional[str] = None,
    variants: Optional[tuple] = None,
    provenance_note: str = "",
) -> dict:
    """Build + (optionally) save response_matrix_<design>.npz for both variants.

    ``grid_version``  None (default) keeps the v1.0 behaviour: the deposit axis
                      is PARSED from ``data/combined_dRdEdep.csv``. Passing
                      "v1.0" or "v2.0-ext" instead sources the axis from
                      ``E_dep_grid_from_shared_grid_eV`` (plan 10-03), which is
                      how plan 10-04 builds on the 744-column extended axis.
                      The two v1.0 routes differ by up to 4.918e-07 relative --
                      see ``E_dep_grid_from_shared_grid_eV`` -- so they are NOT
                      interchangeable and produce different sub-seeds.
    ``file_name``     output file name override; the v1.0
                      ``artifacts/stage1/response_matrix_*.npz`` must never be
                      overwritten (``fp-overwrite-v1-matrices``).
    ``variants``      censoring variants to build; defaults to
                      ``params.CENSORING_VARIANTS`` (both).
    """
    d = es.resolve_design(design_name)
    if grid_version is None:
        E_dep = load_E_dep_grid_eV(csv_path)
        axis_source = os.path.relpath(csv_path, _PROJECT_ROOT)
    else:
        E_dep = E_dep_grid_from_shared_grid_eV(grid_version)
        axis_source = f"muon_deposit.shared_energy_grid({grid_version!r}) geometric means"
    E_rec_edges = build_E_rec_edges_eV(bins_per_decade)
    E_rec_centers = np.sqrt(E_rec_edges[1:-1] * np.maximum(E_rec_edges[2:], E_rec_edges[1:-1]))
    # centers for the underflow bin + log bins (underflow center = its geometric-ish mid)
    centers = np.empty(E_rec_edges.size - 1, dtype=float)
    centers[0] = 0.5 * E_rec_edges[1]  # underflow bin representative
    centers[1:] = np.sqrt(E_rec_edges[1:-1] * E_rec_edges[2:])

    xover = resp.crossover_band(d)
    onset_Edep = float(xover["default_point_eV"])
    plateau_Edep = float(xover["whole_array_plateau_default_eV"])

    out = {
        "design": d.name,
        "E_dep_centers_eV": E_dep,
        "E_dep_edges_eV": _log_edges_from_centers(E_dep),
        "E_rec_edges_eV": E_rec_edges,
        "E_rec_centers_eV": centers,
        "saturation_onset_Edep_eV": onset_Edep,
        "whole_array_plateau_Edep_eV": plateau_Edep,
    }
    for variant in (variants or params.CENSORING_VARIANTS):
        m = build_matrix(
            d, variant, E_dep, E_rec_edges,
            seed=seed, N_s=N_s, M_pool=M_pool, ec_emg_max=ec_emg_max,
        )
        out[f"R_{variant}"] = m["R"]
        out[f"counts_{variant}"] = m["counts"]
        out[f"err_{variant}"] = m["err"]
        out[f"E_rec_median_{variant}_eV"] = m["E_rec_median_eV"]
        out[f"E_rec_p16_{variant}_eV"] = m["E_rec_p16_eV"]
        out[f"E_rec_p84_{variant}_eV"] = m["E_rec_p84_eV"]
        out[f"E_rec_mean_{variant}_eV"] = m["E_rec_mean_eV"]
        out[f"C_{variant}_eV_per_event"] = m["C_eV_per_event"]
        # Plan 10-04 diagnostics, stored per variant.
        out[f"N_obs_mean_{variant}"] = m["N_obs_mean"]
        out[f"P_zero_count_{variant}"] = m["P_zero_count"]
        out[f"n_distinct_Erec_{variant}"] = m["n_distinct_Erec"]
        out[f"rel_spread_{variant}"] = m["rel_spread"]
        out[f"n_offgrid_high_{variant}"] = m["n_offgrid_high"]
        out[f"n_offgrid_low_{variant}"] = m["n_offgrid_low"]

    # LABELED SECONDARY (never auto-switched): time-over-saturation estimator.
    tos = time_over_saturation_curve(E_dep, d)
    out["tos_t_over_s"] = tos["t_over_s"]

    meta = {
        "plan": "05-02" if grid_version is None else "10-04",
        "design": d.name,
        "seed": int(seed),
        "N_s": int(N_s),
        "M_pool": int(M_pool),
        "ec_emg_max": float(ec_emg_max),
        "erec_bins_per_decade": int(bins_per_decade),
        "f_prompt": float(params.F_PROMPT.value),
        "r_spot_sensors": float(params.R_SPOT.value),
        "n_sensors": float(params.N_SENSORS.value),
        "tau_d_s": float(params.TAU_D.value),
        "saturation_ceiling_hz": float(resp.SATURATION_CEILING_HZ),
        "censoring_variants": list(variants or params.CENSORING_VARIANTS),
        "E_dep_range_eV": [float(E_dep.min()), float(E_dep.max())],
        "E_dep_n_columns": int(E_dep.size),
        "E_dep_source_grid": axis_source,
        "grid_version": grid_version,
        "seed_scheme": (
            "response_matrix.column_seed_sequence: SeedSequence([seed, crc32(design), "
            "crc32(variant), crc32('%.12e' % E_dep_eV)]). Plan 10-03: the sub-seed is a "
            "stable function of the column's DEPOSIT ENERGY, not of its ordinal index, so "
            "prepending the 160 sub-eV columns does not re-seed the 584 columns above "
            "10.14 eV (fp-ordinal-seed)."),
        "git_sha": _git_sha(),
        "linear_yield_extrapolation_caveat": (
            "BELOW ~1 eV THIS MATRIX IS A MEAN-FIELD EXTRAPOLATION, NOT A DEVICE "
            "PREDICTION. energy_scale.n_qp_yield is exactly linear, N_qp = eps*E_sensor/"
            "Delta_tr, with no pair-breaking threshold and no discreteness. At a 0.1 eV "
            "deposit the off-spot per-sensor share is ~6.8 ueV against an Al trap gap "
            "Delta_tr ~ 190 ueV, so the model assigns ~0.018 quasiparticles to a sensor "
            "that could not energetically host one. The bottom two decades are therefore "
            "a linear extrapolation two decades below where the chain was ever validated. "
            "Phase 10 can only label this; it cannot fix it. A matrix that looks smooth at "
            "0.1 eV is NOT evidence that the extrapolation is valid."),
        "subev_regime_note": (
            "Below trigger.SUBEV_REGIME_BOUNDARY_eV = 1.0 eV the project's REPORTED "
            "observable is the trigger probability P_trig(E_dep) (CONVENTIONS Section I, "
            "plan 10-02), not dR/dE_rec. The trigger curve is NOT folded into this matrix: "
            "it is an analysis efficiency on a rate, not part of the response kernel "
            "(fp-trigger-applied-here)."),
        "phase10_provenance_note": provenance_note,
        "v1_comparison_note": (
            "The archived artifacts/stage1/response_matrix_*.npz were built on deposit "
            "centres round-tripped through data/combined_dRdEdep.csv, which differ from "
            "the exact geometric means by up to 4.918e-07 relative. BIT-IDENTICAL "
            "reproduction of the archived matrices is NOT achievable and is not claimed "
            "(fp-bit-identical-promise)."),
        "R_column_norm": "each E_dep column sums to 1 over E_rec bins (incl. underflow)",
        "estimator": "count-integral E_rec = C * sum_i N_obs,i (Plan 05-01 deliverable)",
        "mc_fluctuation_model": {
            "ec_le_ec_emg_max": "MUST-USE EMG event train (ref-qpd-repo) -> per-sensor pmf; class sum multinomial; mean pinned to analytic censored_count",
            "ec_gt_ec_emg_max": "deep saturation, EMG event train infeasible (O(1e8) events); registered-count Poisson about analytic censored_count; relative spread negligible",
        },
        "secondary_tos": "time-over-saturation curve is a LABELED SECONDARY (unvalidated, tau_qp fixed); NEVER auto-switched into the baseline (fp-tos-autoswitch)",
        "no_anchor_caveat": "the saturated-regime E_rec SHAPE has NO literature anchor at any energy; the low-E UNIT slope (params.CALIB_SLOPE = 1.0, user decision 2026-07-25) is calibration-consistency, not validation",
        "units": "energy eV internal; R dimensionless probability per E_rec bin",
        "provenance": "qpd_potential.response_matrix.run_design; reuses Plan 05-01 qpd_potential.response + ref-qpd-repo QuasiparticleBurstModel EMG template",
    }
    out["meta_json"] = json.dumps(meta, indent=2)

    if write:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, file_name or DESIGN_FILE[d.name])
        np.savez_compressed(path, **out)
        out["_path"] = path
    return out


def run_all(**kwargs) -> dict:
    """Build + save both design npz files (Ta->Al, Al->Hf), both variants each."""
    return {name: run_design(name, **kwargs) for name in DESIGN_FILE}


# --------------------------------------------------------------------------- #
# Convergence diagnostic helpers (used by tests + the CLI report)               #
# --------------------------------------------------------------------------- #


def populated_cell_report(counts_col: np.ndarray, floor_count: float = 1111.0) -> dict:
    """Per-column convergence summary. floor_count = 1111 is the Poisson 3%
    threshold (1/sqrt(1111) ~= 0.03).  Returns the peak-cell relative error, the
    fraction of probability mass in cells at/above the 3% Poisson floor, and the
    number of populated cells.
    """
    total = counts_col.sum()
    if total <= 0:
        return {"peak_rel_err": float("nan"), "mass_frac_le_3pct": 0.0, "n_populated": 0}
    peak = counts_col.max()
    well = counts_col >= floor_count
    return {
        "peak_rel_err": float(1.0 / np.sqrt(peak)),
        "mass_frac_le_3pct": float(counts_col[well].sum() / total),
        "n_populated": int(np.count_nonzero(counts_col > 0)),
    }


# --------------------------------------------------------------------------- #
# deliv-fig-response: E_rec vs E_dep, both designs, both variants, saturation    #
# onset marked + saturated region delimited + caveats                           #
# --------------------------------------------------------------------------- #


def make_figure(
    out_path: str = os.path.join(_ARTIFACT_DIR, "energy_response.pdf"),
    npz_dir: str = _ARTIFACT_DIR,
) -> str:
    """Build the response figure from the saved npz (both designs, both variants)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    keV = 1.0e-3
    data = {name: dict(np.load(os.path.join(npz_dir, fn), allow_pickle=True))
            for name, fn in DESIGN_FILE.items()}

    fig, ax = plt.subplots(figsize=(9.2, 6.6))
    colors = {"Ta->Al": "#1f77b4", "Al->Hf": "#d62728"}
    styles = {"non_paralyzable": "-", "paralyzable": "--"}

    for design, d in data.items():
        E_dep = d["E_dep_centers_eV"] * keV  # keV
        for variant in params.CENSORING_VARIANTS:
            med = d[f"E_rec_median_{variant}_eV"] * keV
            p16 = d[f"E_rec_p16_{variant}_eV"] * keV
            p84 = d[f"E_rec_p84_{variant}_eV"] * keV
            ax.plot(E_dep, med, styles[variant], color=colors[design], lw=1.8,
                    label=f"{design} — {variant}")
            ax.fill_between(E_dep, np.maximum(p16, 1e-12), np.maximum(p84, 1e-12),
                            color=colors[design], alpha=0.12, lw=0)
        # per-design saturation onset (on-spot bend) + whole-array plateau band
        onset = float(d["saturation_onset_Edep_eV"]) * keV
        plateau = float(d["whole_array_plateau_Edep_eV"]) * keV
        ax.axvspan(onset, plateau, color=colors[design], alpha=0.05, lw=0)
        ax.axvline(onset, color=colors[design], ls=":", lw=1.0, alpha=0.7)

    # calibration-consistency 0.5 slope reference (NOT independent validation)
    E_ref = data["Ta->Al"]["E_dep_centers_eV"] * keV
    ax.plot(E_ref, 0.5 * E_ref, color="0.4", ls="-.", lw=1.0,
            label=r"$0.5\,E_{\rm dep}$ (low-E calibration line, not validation)")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"Deposited energy $E_{\rm dep}$ [keV]")
    ax.set_ylabel(r"Reconstructed energy $E_{\rm rec}$ [keV]  (median, 16–84% band)")
    ax.set_title("QPD bandwidth-limited response $R(E_{\\rm rec}\\,|\\,E_{\\rm dep})$: linear → saturated\n"
                 "(both designs, both censoring variants)", fontsize=11)
    ax.set_xlim(E_ref.min(), E_ref.max())
    ax.grid(True, which="major", alpha=0.25)

    # annotations / caveats
    ax.text(0.015, 0.60,
            "Saturated region (shaded): on-spot bend → whole-array plateau.\n"
            "non-paralyzable (solid) PLATEAUS; paralyzable (dashed) ROLLS OVER.\n"
            "Ceiling pile-up is an INSTRUMENT ARTIFACT of the modeled saturation,\n"
            "NOT a physical spectral peak (Pitfall 5).\n"
            "Saturated-regime SHAPE has NO literature anchor at any energy;\n"
            "low-E 0.5 slope is calibration-consistency, not validation.",
            transform=ax.transAxes, fontsize=8.0, va="top", ha="left",
            bbox=dict(boxstyle="round", fc="#fffbe6", ec="0.6", alpha=0.95))

    handles, labels = ax.get_legend_handles_labels()
    handles.append(Line2D([0], [0], color="0.5", alpha=0.3, lw=8))
    labels.append("saturated region (per design)")
    ax.legend(handles, labels, fontsize=7.6, loc="lower right", framealpha=0.95)

    fig.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path)
    plt.close(fig)
    return out_path


if __name__ == "__main__":  # pragma: no cover
    ap = argparse.ArgumentParser(description="Build R(E_rec|E_dep) for both designs x both variants.")
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--nsamples", type=int, default=DEFAULT_N_S)
    ap.add_argument("--mpool", type=int, default=DEFAULT_M_POOL)
    ap.add_argument("--ec-emg-max", type=float, default=DEFAULT_EC_EMG_MAX)
    ap.add_argument("--bins-per-decade", type=int, default=DEFAULT_EREC_BINS_PER_DECADE)
    ap.add_argument("--no-write", action="store_true")
    args = ap.parse_args()
    res = run_all(
        seed=args.seed, N_s=args.nsamples, M_pool=args.mpool,
        ec_emg_max=args.ec_emg_max, bins_per_decade=args.bins_per_decade,
        write=not args.no_write,
    )
    for name, out in res.items():
        print(f"{name}: wrote {out.get('_path', '<memory>')}")
