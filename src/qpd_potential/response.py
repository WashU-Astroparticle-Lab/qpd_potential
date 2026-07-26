# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
#
# Phase-5 (Plan 05-01) QPD forward response chain + count-integral E_rec estimator.
#
# SCOPE: turn the Phase-1 forward-chain scaffold (qpd_potential.energy_scale)
# into a working per-design reconstructed-energy response. This module
# implements the ONE genuinely missing piece -- the real E_rec estimator -- as a
# CALIBRATED COUNT-INTEGRAL estimator, driven by a single-deposit forward
# realization that reuses the MUST-USE qpd EMG burst template
# (QuasiparticleBurstModel) for the tunneling-EVENT train and the scaffold
# `observed_rate` closed forms for the 25 kHz / 40 us bandwidth censoring.
#
# It does NOT re-derive or re-transcribe any device constant (all imported from
# `params`) and does NOT re-implement the forward chain (all imported from
# `energy_scale`). It does NOT fold any spectrum (Phase 6) and does NOT build the
# full Monte-Carlo response matrix R(E_rec|E_dep) (Plan 05-02).
#
# KEY PHYSICS (encoded, not re-litigated -- see 5-RESEARCH.md):
#   * The two-exponential pulse (paper Eq. 4) has trapped population
#         N_qp(t) = tau_qp * N_qp * g(t),   g = (e^{-t/tau_qp} - e^{-t/tau_inj})/(tau_qp - tau_inj)
#     with INT g dt = 1 and tau_qp*max(g) = p (the recorded peak factor: 0.25 Al
#     / 0.13 Hf -- verified against params.PEAK_FACTOR_*). Hence
#         Gamma_in(t) = (K/V_tr) N_qp(t) = event_count * g(t)
#     with the TWO invariants that the EMG mapping must preserve:
#         (1) event_count = INT Gamma_in dt = K*tau_qp*N_qp/V_tr    (drives the count)
#         (2) peak Gamma_in = event_count*max(g) = p*K*N_qp/V_tr    (drives censoring)
#   * PITFALL 1 (fp-eventcount): QuasiparticleBurstModel.expected_n_qp is the
#     Poisson mean of the number of TUNNELING EVENTS = event_count = INT Gamma_in dt,
#     NOT the trapped-QP count N_qp. They differ by K*tau_qp/V_tr (0.03 Al /
#     0.008 Hf). Feeding N_qp mis-scales the whole saturation.
#   * PITFALL 2 (fp-calib-as-validation): the count-integral constant C is a
#     SINGLE global per-design constant fixed by the low-E slope dE_rec/dE_dep =
#     params.CALIB_SLOPE = 1.0. The low-E linearity is therefore a
#     CALIBRATION-CONSISTENCY check, not independent validation.
#     (USER DECISION 2026-07-25: the slope is 1.0, not eps = 0.5. E_rec estimates
#     the DEPOSIT; on-detector calibration absorbs the physical deposit->QP
#     conversion fraction eps into C. Saturation is still never unfolded.)
#   * The saturated-regime PLATEAU of the count-integral IS the modeled
#     saturation (fp-no-saturation): non_paralyzable censoring caps the observed
#     count (E_rec plateaus, ~10-20 keV whole-array scale), paralyzable rolls it
#     over (E_rec strictly sub-linear, may turn over). BOTH variants carried
#     (CONVENTIONS F open switch).
#   * Ta gate (fp-ta-band): Delta_abs(Ta) enters the response arithmetic NOWHERE
#     (yield/rate/onset use the Al TRAP gap); it is a BINARY trapping gate
#     Delta_abs/Delta_tr >= ~2, asserted here.
#
# UNITS (CONVENTIONS Section A.1): energy eV; time s; length um; rates Hz.

from __future__ import annotations

import sys
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional, Union

import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.stats import exponnorm

from . import params
from . import energy_scale as es
from .params import TrapDesign

# --- MUST-USE ref-qpd-repo EMG burst template (submodule path only; the
#     top-level qpd package pulls qutip). See tool_requirements: qpd-emg-template.
_QPD_SRC = "/Users/lanqingyuan/Documents/GitHub/qpd/src"
if _QPD_SRC not in sys.path:
    sys.path.insert(0, _QPD_SRC)
from qpd.simulator.quasiparticle_bursts import (  # noqa: E402
    QuasiparticleBurstModel,
    poisson_burst_times,  # re-exported for downstream 05-02 use
)

__all__ = [
    "SATURATION_CEILING_HZ",
    "TRAPPING_GATE_MIN",
    "assert_trapping_gate",
    "trapping_gate_ok",
    "pulse_shape",
    "pulse_shape_integral",
    "expected_event_count",
    "gamma_in_of_t",
    "censored_count",
    "ForwardCounts",
    "forward_counts",
    "calibrate_C",
    "E_rec",
    "emg_pulse_params",
    "realize_event_train",
    "censor_event_train",
    "realized_censored_count",
    "analytic_thinning_train",
    "onset_deposit_energy",
    "whole_array_plateau_energy",
    "crossover_band",
    "sweep_E_rec",
]

SATURATION_CEILING_HZ: float = es.SATURATION_CEILING_HZ  # 25 kHz = 1/tau_d

# Trapping gate lower bound: Delta_abs/Delta_tr >= ~2 (LOWER bound, not a ceiling;
# CONVENTIONS Section G / 5-RESEARCH Pitfall 4). Below this the absorber cannot
# trap into the junction and the design premise is invalid (e.g. beta-Ta).
TRAPPING_GATE_MIN: float = 2.0

ArrayLike = Union[float, np.ndarray]
Design = Union[str, TrapDesign]


# --------------------------------------------------------------------------- #
# Ta trapping gate (fp-ta-band): binary gate, NOT a response band              #
# --------------------------------------------------------------------------- #


def trapping_gate_ok(design: Design) -> bool:
    """True iff Delta_abs/Delta_tr >= TRAPPING_GATE_MIN for this design.

    The Ta->Al response is numerically independent of Delta_abs(Ta) WITHIN the
    trapping regime (the arithmetic uses the Al TRAP gap Delta_tr everywhere);
    the only Ta-gap dependence is this binary gate. alpha-Ta (ratio 3.58,
    T_c=4.48 K) passes; beta-Ta would fail and invalidate the design.
    """
    d = es.resolve_design(design)
    return d.trapping_ratio >= TRAPPING_GATE_MIN


def assert_trapping_gate(design: Design) -> None:
    """Assert the binary trapping gate Delta_abs/Delta_tr >= 2; raise otherwise.

    A sub-gate ratio (e.g. beta-Ta) means the absorber cannot confine
    quasiparticles into the trap and the whole response model is void -- fail
    loudly rather than emit a silently-wrong curve.
    """
    d = es.resolve_design(design)
    ratio = d.trapping_ratio
    assert ratio >= TRAPPING_GATE_MIN, (
        f"trapping gate VIOLATED for design {d.name!r}: "
        f"Delta_abs/Delta_tr = {ratio:.3g} < {TRAPPING_GATE_MIN} "
        f"(Delta_abs={d.delta_abs.value*1e6:.1f} ueV, Delta_tr={d.delta_tr.value*1e6:.1f} ueV). "
        "The absorber cannot trap into the junction (e.g. beta-phase Ta) -- design premise invalid."
    )


# --------------------------------------------------------------------------- #
# Two-exponential pulse shape (paper Eq. 4)                                     #
# --------------------------------------------------------------------------- #


def _tau_pair(design: Design) -> tuple[float, float]:
    d = es.resolve_design(design)
    return d.tau_inj.value, d.tau_qp.value


def pulse_shape(t: ArrayLike, design: Design, *, normalized: bool = True) -> ArrayLike:
    """Two-exponential trapped-population shape g(t) [s^-1], zero for t<0.

    g(t) = (e^{-t/tau_qp} - e^{-t/tau_inj}) / (tau_qp - tau_inj),  t >= 0

    Unit area (INT g dt = 1) and tau_qp*max(g) = p (the recorded peak factor).
    With ``normalized=False`` the peak-height-normalized shape h(t)=g/max(g)
    (peak 1) is returned instead -- convenient for Gamma_in(t)=peak*h(t).
    """
    tau_inj, tau_qp = _tau_pair(design)
    t = np.asarray(t, dtype=float)
    g = np.where(
        t >= 0.0,
        (np.exp(-t / tau_qp) - np.exp(-t / tau_inj)) / (tau_qp - tau_inj),
        0.0,
    )
    if normalized:
        return g if g.ndim else float(g)
    gmax = pulse_peak_value(design)
    h = g / gmax
    return h if h.ndim else float(h)


def _peak_time(design: Design) -> float:
    tau_inj, tau_qp = _tau_pair(design)
    # d/dt g = 0  =>  t* = (tau_inj*tau_qp/(tau_inj-tau_qp)) * ln(tau_inj/tau_qp)
    return (tau_inj * tau_qp / (tau_inj - tau_qp)) * np.log(tau_inj / tau_qp)


def pulse_peak_value(design: Design) -> float:
    """max_t g(t) [s^-1]; equals p/tau_qp (p = recorded two-exponential peak factor)."""
    return float(pulse_shape(_peak_time(design), design, normalized=True))


def pulse_shape_integral(design: Design, t_grid: Optional[np.ndarray] = None) -> float:
    """Numerical INT_0^inf g(t) dt on the standard grid; should be ~1 (unit area)."""
    if t_grid is None:
        t_grid = _default_time_grid(design)
    return float(np.trapz(pulse_shape(t_grid, design), t_grid))


def _default_time_grid(design: Design, span: float = 30.0, n: int = 8000) -> np.ndarray:
    tau_inj, tau_qp = _tau_pair(design)
    t_max = span * max(tau_inj, tau_qp)
    return np.linspace(0.0, t_max, n)


# --------------------------------------------------------------------------- #
# Event-count mapping (PITFALL 1) and instantaneous rate                        #
# --------------------------------------------------------------------------- #


def expected_event_count(N_qp: ArrayLike, design: Design) -> ArrayLike:
    """Expected number of TUNNELING EVENTS in the pulse = INT Gamma_in dt.

        event_count = INT (K/V_tr) N_qp(t) dt = (K/V_tr) * tau_qp * N_qp
                    = tau_qp * tunneling_rate(qp_density(N_qp))

    This is the Poisson mean fed to QuasiparticleBurstModel.expected_n_qp --
    NOT the trapped count N_qp (fp-eventcount / Pitfall 1). The two differ by
    the factor K*tau_qp/V_tr (0.03 Al / 0.008 Hf).
    """
    d = es.resolve_design(design)
    return d.K.value * d.tau_qp.value * N_qp / d.v_tr.value


def gamma_in_of_t(t: ArrayLike, N_qp: ArrayLike, design: Design) -> ArrayLike:
    """Instantaneous tunneling rate Gamma_in(t) = event_count * g(t) [Hz].

    Peak equals event_count*max(g) = p*K*N_qp/V_tr = peak_tunneling_rate(N_qp)
    (scaffold), and INT Gamma_in dt = event_count (both invariants preserved).
    """
    ec = expected_event_count(N_qp, design)
    g = pulse_shape(t, design, normalized=True)
    return ec * g


# --------------------------------------------------------------------------- #
# Analytic censored count per sensor: N_obs = INT observed_rate(Gamma_in(t)) dt #
# --------------------------------------------------------------------------- #


def censored_count(
    N_qp: ArrayLike,
    design: Design,
    variant: str = params.DEFAULT_CENSORING,
    t_grid: Optional[np.ndarray] = None,
) -> ArrayLike:
    """Observed (censored) tunneling-event count on one sensor.

        N_obs = INT_0^inf m(Gamma_in(t)) dt

    with m the dead-time closed form (`energy_scale.observed_rate`, selectable
    variant). Valid because the pulse (~ms) varies slowly vs tau_d=40 us, so the
    local registered rate is m(Gamma_in(t)); this matches the event-train
    dead-window realization in expectation (verified in tests).

    Linear regime: m ~= Gamma_in  =>  N_obs ~= event_count (linear in E_sensor).
    Saturated (non_paralyzable): m -> 1/tau_d  =>  N_obs caps (plateau).
    Saturated (paralyzable):     m -> 0        =>  N_obs rolls over.

    Vectorized over an array of N_qp (broadcast against the time grid).
    """
    d = es.resolve_design(design)
    if t_grid is None:
        t_grid = _default_time_grid(d)
    g = pulse_shape(t_grid, d, normalized=True)  # (nt,)
    ec = np.atleast_1d(np.asarray(expected_event_count(N_qp, d), dtype=float))  # (ns,)
    # Gamma_in(t) for each sensor: outer product (ns, nt)
    gamma = ec[:, None] * g[None, :]
    m = es.observed_rate(gamma, variant=variant)
    n_obs = np.trapz(m, t_grid, axis=1)  # (ns,)
    if np.isscalar(N_qp) or np.asarray(N_qp).ndim == 0:
        return float(n_obs[0])
    return n_obs


# --------------------------------------------------------------------------- #
# Single-deposit forward realization (array-summed censored count)             #
# --------------------------------------------------------------------------- #


@dataclass
class ForwardCounts:
    """Per-deposit forward-chain summary (one design, one censoring variant)."""

    E_dep_eV: float
    design: str
    variant: str
    E_sensor_on: float
    E_sensor_off: float
    N_qp_on: float
    N_qp_off: float
    n_spot: float
    n_off: float
    peak_gamma_on: float
    peak_gamma_off: float
    N_obs_on: float
    N_obs_off: float
    total_N_obs: float
    on_spot_saturated: bool
    off_spot_saturated: bool


def _n_spot(r: float) -> float:
    return np.pi * r * r


def forward_counts(
    E_dep_eV: float,
    design: Design,
    variant: str = params.DEFAULT_CENSORING,
    *,
    f_prompt: Optional[float] = None,
    r: Optional[float] = None,
    n_sensors: Optional[float] = None,
    t_grid: Optional[np.ndarray] = None,
    check_gate: bool = True,
) -> ForwardCounts:
    """Forward realization of a single deposit -> summed censored tunneling count.

    The ~pi r^2 on-spot sensors carry f_prompt of the energy plus the diffuse
    share; the ~10,300-pi r^2 off-spot sensors share one identical diffuse
    energy and are aggregated analytically (NOT looped). Ta trapping gate
    asserted (uses Delta_tr only; Delta_abs never enters).
    """
    d = es.resolve_design(design)
    if check_gate:
        assert_trapping_gate(d)
    if f_prompt is None:
        f_prompt = params.F_PROMPT.value
    if r is None:
        r = params.R_SPOT.value
    if n_sensors is None:
        n_sensors = params.N_SENSORS.value

    E_on = float(es.sensor_energy_split(E_dep_eV, f_prompt, r, n_sensors, on_spot=True))
    E_off = float(es.sensor_energy_split(E_dep_eV, f_prompt, r, n_sensors, on_spot=False))
    N_on = float(es.n_qp_yield(E_on, d))
    N_off = float(es.n_qp_yield(E_off, d))
    n_spot = _n_spot(r)
    n_off = n_sensors - n_spot

    peak_on = float(es.peak_tunneling_rate(N_on, d))
    peak_off = float(es.peak_tunneling_rate(N_off, d))

    N_obs_on = censored_count(N_on, d, variant=variant, t_grid=t_grid)
    N_obs_off = censored_count(N_off, d, variant=variant, t_grid=t_grid)
    total = n_spot * N_obs_on + n_off * N_obs_off

    return ForwardCounts(
        E_dep_eV=float(E_dep_eV),
        design=d.name,
        variant=variant,
        E_sensor_on=E_on,
        E_sensor_off=E_off,
        N_qp_on=N_on,
        N_qp_off=N_off,
        n_spot=n_spot,
        n_off=n_off,
        peak_gamma_on=peak_on,
        peak_gamma_off=peak_off,
        N_obs_on=N_obs_on,
        N_obs_off=N_obs_off,
        total_N_obs=float(total),
        on_spot_saturated=bool(peak_on > SATURATION_CEILING_HZ),
        off_spot_saturated=bool(peak_off > SATURATION_CEILING_HZ),
    )


# --------------------------------------------------------------------------- #
# Calibration (single global per-design constant C) + estimator                #
# --------------------------------------------------------------------------- #


def calibrate_C(
    design: Design,
    variant: str = params.DEFAULT_CENSORING,
    *,
    f_prompt: Optional[float] = None,
    r: Optional[float] = None,
    n_sensors: Optional[float] = None,
    E_dep_cal_eV: float = 0.01,
    slope: float = None,
    t_grid: Optional[np.ndarray] = None,
) -> float:
    """Solve the SINGLE global count->energy constant C [eV/event] per design.

    C is fixed once, on a low-E deposit where NO sensor saturates, by requiring
    the linear slope dE_rec/dE_dep = params.CALIB_SLOPE = 1.0. Because the
    linear-regime summed count is exactly proportional to E_dep, one point fixes
    C:  C = slope * E_dep_cal / total_N_obs(E_dep_cal). No per-bin tuning
    (Pitfall 2 / fp-calib-as-validation).

    THE SLOPE IS 1.0, NOT params.EPSILON (USER DECISION 2026-07-25).  E_rec is an
    ESTIMATOR of the deposited energy, not the collected signal.  A real detector
    is calibrated on a known line, and that calibration absorbs the physical
    deposit->quasiparticle conversion fraction EPSILON into C; a 10 eV deposit
    reconstructs at 10 eV.  EPSILON keeps its physical role everywhere else in the
    forward chain (energy_scale.n_qp_yield, the saturation onset, the trigger) --
    it is simply not the energy scale.  What calibration does NOT undo, and what
    this slope must never be used to undo, is the sub-linear SATURATION above the
    onset: that is genuine information loss (fp-unfold-saturation).
    """
    if slope is None:
        slope = params.CALIB_SLOPE.value
    fc = forward_counts(
        E_dep_cal_eV, design, variant,
        f_prompt=f_prompt, r=r, n_sensors=n_sensors, t_grid=t_grid,
    )
    # Guard: calibration deposit must be unsaturated (linear regime).
    assert not fc.on_spot_saturated, (
        f"calibration deposit E_dep={E_dep_cal_eV} eV already saturates the on-spot "
        f"sensor for {fc.design} (peak Gamma={fc.peak_gamma_on:.3g} Hz > {SATURATION_CEILING_HZ:.0f}); "
        "pick a lower E_dep_cal_eV."
    )
    return slope * E_dep_cal_eV / fc.total_N_obs


def E_rec(
    E_dep_eV: ArrayLike,
    design: Design,
    variant: str = params.DEFAULT_CENSORING,
    *,
    C: Optional[float] = None,
    f_prompt: Optional[float] = None,
    r: Optional[float] = None,
    n_sensors: Optional[float] = None,
    t_grid: Optional[np.ndarray] = None,
) -> ArrayLike:
    """Reconstructed energy E_rec = C * sum_i N_obs,i [eV] (count-integral estimator).

    Replaces the Phase-1 `energy_scale.E_rec_estimator` STUB with the real
    calibrated estimator. Low-E: E_rec ~= E_dep (by calibration). High-E:
    PLATEAU (non_paralyzable) or ROLLOVER (paralyzable) -- the modeled
    saturation (fp-no-saturation), never a linear extrapolation into the MeV
    range. C is calibrated once if not supplied.
    """
    d = es.resolve_design(design)
    if t_grid is None:
        t_grid = _default_time_grid(d)
    if C is None:
        C = calibrate_C(
            d, variant, f_prompt=f_prompt, r=r, n_sensors=n_sensors, t_grid=t_grid
        )
    E_arr = np.atleast_1d(np.asarray(E_dep_eV, dtype=float))
    out = np.array([
        C * forward_counts(
            float(E), d, variant,
            f_prompt=f_prompt, r=r, n_sensors=n_sensors, t_grid=t_grid,
            check_gate=False,
        ).total_N_obs
        for E in E_arr
    ])
    if np.isscalar(E_dep_eV) or np.asarray(E_dep_eV).ndim == 0:
        return float(out[0])
    return out


def sweep_E_rec(
    E_dep_grid_eV: np.ndarray,
    design: Design,
    variant: str = params.DEFAULT_CENSORING,
    *,
    f_prompt: Optional[float] = None,
    r: Optional[float] = None,
    n_sensors: Optional[float] = None,
) -> dict:
    """Sweep E_dep -> (E_rec, total_N_obs, peak_gamma_on) for a design+variant.

    Convenience for the VALD-04 limiting-case and stop-condition checks and for
    the Plan 05-01 review curve. Returns a dict of arrays.
    """
    d = es.resolve_design(design)
    t_grid = _default_time_grid(d)
    C = calibrate_C(d, variant, f_prompt=f_prompt, r=r, n_sensors=n_sensors, t_grid=t_grid)
    E_dep_grid_eV = np.asarray(E_dep_grid_eV, dtype=float)
    fcs = [
        forward_counts(float(E), d, variant, f_prompt=f_prompt, r=r,
                       n_sensors=n_sensors, t_grid=t_grid, check_gate=False)
        for E in E_dep_grid_eV
    ]
    return {
        "design": d.name,
        "variant": variant,
        "C": C,
        "E_dep": E_dep_grid_eV,
        "E_rec": np.array([C * fc.total_N_obs for fc in fcs]),
        "total_N_obs": np.array([fc.total_N_obs for fc in fcs]),
        "peak_gamma_on": np.array([fc.peak_gamma_on for fc in fcs]),
        "peak_gamma_off": np.array([fc.peak_gamma_off for fc in fcs]),
        "on_spot_saturated": np.array([fc.on_spot_saturated for fc in fcs]),
        "off_spot_saturated": np.array([fc.off_spot_saturated for fc in fcs]),
    }


# --------------------------------------------------------------------------- #
# MUST-USE EMG realization (QuasiparticleBurstModel) + event-train censoring    #
# --------------------------------------------------------------------------- #


@lru_cache(maxsize=None)
def emg_pulse_params(design_name: str) -> tuple[float, float, float]:
    """(tau, mu, sigma) [s] for the EMG that reproduces the two-exponential pulse.

    tau = tau_qp (decay tail); mu = 0 (onset reference); sigma solved once per
    design so the EMG pdf PEAK equals max(g) = p/tau_qp. Then, with
    QuasiparticleBurstModel.expected_n_qp = event_count, the realized point
    process has:
        (1) mean count       = event_count            (INT Gamma_in dt)
        (2) peak inst. rate  = event_count*max(pdf)    = p*K*N_qp/V_tr = peak Gamma_in
    i.e. BOTH pulse invariants (Pitfall 1 mapping). sigma encodes the tau_inj
    onset spread; solved because p<1 requires broadening below the pure-Exp peak
    1/tau_qp.
    """
    d = es.resolve_design(design_name)
    tau = d.tau_qp.value
    target = pulse_peak_value(d)  # p / tau_qp

    def max_pdf(sigma: float) -> float:
        dist = exponnorm(tau / sigma, loc=0.0, scale=sigma)
        res = minimize_scalar(
            lambda t: -dist.pdf(t),
            bounds=(-5.0 * sigma, tau + 15.0 * sigma),
            method="bounded",
        )
        return float(dist.pdf(res.x))

    # max_pdf decreases monotonically with sigma: sigma->0 gives ~1/tau > target,
    # large sigma gives ~0 < target. Bracket and solve.
    sigma = brentq(lambda s: max_pdf(s) - target, 1e-4 * tau, 100.0 * tau, xtol=1e-12)
    return tau, 0.0, sigma


def realize_event_train(
    N_qp: float,
    design: Design,
    rng: np.random.Generator,
    *,
    t0: float = 0.0,
) -> np.ndarray:
    """Draw one sensor's tunneling-event train via QuasiparticleBurstModel.

    expected_n_qp is fed the EVENT COUNT INT Gamma_in dt (Pitfall 1), NOT N_qp.
    Returns sorted absolute event times [s].
    """
    d = es.resolve_design(design)
    tau, mu, sigma = emg_pulse_params(d.name)
    ec = float(expected_event_count(N_qp, d))
    model = QuasiparticleBurstModel(
        times=[t0], tau=tau, mu=mu, sigma=sigma, expected_n_qp=ec
    )
    events, _truth = model.sample(rng)
    return events


def censor_event_train(
    event_times: np.ndarray,
    variant: str = params.DEFAULT_CENSORING,
    tau_d: Optional[float] = None,
) -> int:
    """Dead-window censoring of an event train -> observed count.

    non_paralyzable: after a REGISTERED event, all events within tau_d are lost;
                     the dead window restarts only from registered events.
    paralyzable:     EVERY event (registered or not) restarts the dead window,
                     so an event registers only if the preceding event was
                     > tau_d earlier -- deep saturation collapses the count.
    Matches the `observed_rate` closed forms in expectation.
    """
    if tau_d is None:
        tau_d = params.TAU_D.value
    ev = np.sort(np.asarray(event_times, dtype=float))
    if ev.size == 0:
        return 0
    if variant == "non_paralyzable":
        count = 1
        last_reg = ev[0]
        for t in ev[1:]:
            if t - last_reg > tau_d:
                count += 1
                last_reg = t
        return count
    if variant == "paralyzable":
        count = 1  # first event always registers
        prev = ev[0]
        for t in ev[1:]:
            if t - prev > tau_d:
                count += 1
            prev = t
        return count
    raise ValueError(
        f"unknown censoring variant {variant!r}; expected one of {params.CENSORING_VARIANTS}"
    )


def realized_censored_count(
    N_qp: float,
    design: Design,
    rng: np.random.Generator,
    variant: str = params.DEFAULT_CENSORING,
) -> int:
    """MC realized observed count for one sensor (EMG realize + dead-window drop)."""
    ev = realize_event_train(N_qp, design, rng)
    return censor_event_train(ev, variant=variant)


def analytic_thinning_train(
    N_qp: float,
    design: Design,
    rng: np.random.Generator,
    *,
    t_grid: Optional[np.ndarray] = None,
) -> np.ndarray:
    """Internal cross-check: inhomogeneous-Poisson thinning of Gamma_in(t)=K n_qp(t).

    Independent of the EMG mapping -- used ONLY to verify (in tests) that the
    QuasiparticleBurstModel realization reproduces the same total count and peak
    instantaneous rate. Not part of the deliverable estimator (which uses the
    MUST-USE EMG template).
    """
    d = es.resolve_design(design)
    if t_grid is None:
        t_grid = _default_time_grid(d)
    gamma = gamma_in_of_t(t_grid, N_qp, d)
    gmax = float(gamma.max())
    if gmax <= 0.0:
        return np.empty(0, dtype=float)
    t_max = t_grid[-1]
    # Homogeneous Poisson at rate gmax, then thin by gamma(t)/gmax.
    n_prop = rng.poisson(gmax * t_max)
    t_prop = rng.uniform(0.0, t_max, n_prop)
    lam = np.interp(t_prop, t_grid, gamma)
    keep = rng.uniform(0.0, gmax, n_prop) < lam
    return np.sort(t_prop[keep])


# --------------------------------------------------------------------------- #
# Crossover deposit energy (SIMU-01) -- report as a BAND, not a number          #
# --------------------------------------------------------------------------- #


def _onset_coeff(f_prompt: float, r: float, n_sensors: float) -> float:
    """On-spot per-sensor share coefficient: E_sensor,on-spot = coeff * E_dep."""
    return float(es.sensor_energy_split(1.0, f_prompt, r, n_sensors, on_spot=True))


def onset_deposit_energy(
    design: Design,
    f_prompt: float,
    r: float,
    n_sensors: Optional[float] = None,
    ceiling_hz: float = SATURATION_CEILING_HZ,
) -> float:
    """Crossover deposit energy E_dep,cross [eV] where on-spot peak Gamma_in = ceiling.

        E_dep,cross = E_onset(E_sensor) / [ f_prompt/(pi r^2) + (1-f_prompt)/n_sensors ]
    """
    if n_sensors is None:
        n_sensors = params.N_SENSORS.value
    E_onset = es.saturation_onset_energy(design, ceiling_hz=ceiling_hz)
    return E_onset / _onset_coeff(f_prompt, r, n_sensors)


def whole_array_plateau_energy(
    design: Design,
    f_prompt: float,
    n_sensors: Optional[float] = None,
    ceiling_hz: float = SATURATION_CEILING_HZ,
) -> float:
    """Whole-array plateau deposit energy [eV]: even the diffuse share reaches onset.

        E_dep = E_onset * n_sensors / (1 - f_prompt)
    """
    if n_sensors is None:
        n_sensors = params.N_SENSORS.value
    E_onset = es.saturation_onset_energy(design, ceiling_hz=ceiling_hz)
    return E_onset * n_sensors / (1.0 - f_prompt)


def crossover_band(
    design: Design,
    f_prompt_range: tuple[float, float] = params.F_PROMPT_RANGE,
    r_range: tuple[float, float] = params.R_SPOT_RANGE,
    n_sensors: Optional[float] = None,
    n_grid: int = 9,
) -> dict:
    """Per-design crossover E_dep BAND over f_prompt x r, plus the anchors.

    Returns the default point (f_prompt=0.3, r=2), the [f_prompt_range]x[r_range]
    scan min/max, and the equal-split (f_prompt->0) upper anchor E_onset*n_sensors.
    The ~3-orders-of-magnitude spread is f_prompt-dominated (fp-crossover-point):
    only the band, with the equal-split anchor, is honest.
    """
    if n_sensors is None:
        n_sensors = params.N_SENSORS.value
    d = es.resolve_design(design)
    fps = np.linspace(f_prompt_range[0], f_prompt_range[1], n_grid)
    rs = np.linspace(r_range[0], r_range[1], n_grid)
    grid = np.array([
        [onset_deposit_energy(d, fp, r, n_sensors) for r in rs] for fp in fps
    ])
    E_onset = es.saturation_onset_energy(d)
    return {
        "design": d.name,
        "E_sensor_onset_eV": E_onset,
        "default_point_eV": onset_deposit_energy(
            d, params.F_PROMPT.value, params.R_SPOT.value, n_sensors
        ),
        "band_min_eV": float(grid.min()),
        "band_max_eV": float(grid.max()),
        "equal_split_anchor_eV": E_onset * n_sensors,  # f_prompt -> 0
        "whole_array_plateau_default_eV": whole_array_plateau_energy(
            d, params.F_PROMPT.value, n_sensors
        ),
        "f_prompt_range": tuple(f_prompt_range),
        "r_range": tuple(r_range),
    }
