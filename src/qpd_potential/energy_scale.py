# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
#
# Stage-1 energy-scale / response-DEFINITION module for the QPD reconstructed-
# energy pipeline (Plan 01-02).
#
# SCOPE: this module fixes the unified no-quenching chain
#
#     E_dep  --(sharing)-->  E_sensor  --(yield)-->  N_qp  -->  n_qp  -->  Gamma_in
#          --(peak factor)-->  peak Gamma_in  --(vs 25 kHz)-->  saturation
#          --(dead-time censoring switch)-->  observed rate m
#
# and the SATURATION DEFINITION (peak Gamma_in vs 25 kHz), so Phase 5 has an
# unambiguous, physically-reachable response model. It does NOT compute any
# spectrum, and the E_rec ESTIMATOR is a deliberate Phase-5 stub (see
# E_rec_estimator).
#
# SOURCE OF TRUTH: GPD/CONVENTIONS.md (locked) + qpd_potential.params (Table II
# device parameters, censoring/efficiency/sharing constants). Every physical
# constant is IMPORTED from params -- nothing is re-encoded here.
#
# UNITS (I/O practical, CONVENTIONS Section A.1): energy in eV; time in s;
# length in um; K in Hz*um^3; tunneling rates Gamma_in and observed rate m in
# Hz; densities in um^-3.
#
# FORBIDDEN (CONVENTIONS Section B): a fieldless phonon calorimeter has a single
# unified phonon energy scale. There is NO electron-equivalent vs nuclear-recoil
# scale split and NO ionization/Lindhard suppression anywhere in this module.

from __future__ import annotations

import math
from typing import Union

import numpy as np

from . import params
from .params import TrapDesign

__all__ = [
    "resolve_design",
    "n_qp_yield",
    "qp_density",
    "tunneling_rate",
    "peak_factor",
    "peak_tunneling_rate",
    "sensor_energy_split",
    "peak_gamma_in_from_sensor_energy",
    "peak_gamma_in_from_deposit",
    "saturation_onset_energy",
    "observed_rate",
    "is_saturated",
    "E_rec_estimator",
    "SATURATION_CEILING_HZ",
]

# Locked bandwidth-saturation ceiling: 1/tau_d = 1/40 us = 25 kHz
# (CONVENTIONS Section F; NOT 50 kHz = 1/20 us sampling interval).
SATURATION_CEILING_HZ: float = 1.0 / params.TAU_D.value  # 25_000.0 Hz

ArrayLike = Union[float, np.ndarray]
Design = Union[str, TrapDesign]


# --------------------------------------------------------------------------- #
# Design resolution                                                            #
# --------------------------------------------------------------------------- #


def resolve_design(design: Design) -> TrapDesign:
    """Return the TrapDesign for a name ("Ta->Al"/"Al->Hf") or a TrapDesign."""
    if isinstance(design, TrapDesign):
        return design
    try:
        return params.DESIGNS[design]
    except KeyError as exc:  # pragma: no cover - defensive
        raise KeyError(
            f"unknown design {design!r}; known: {sorted(params.DESIGNS)}"
        ) from exc


# --------------------------------------------------------------------------- #
# Yield / density / tunneling-rate chain (CONVENTIONS Section E; Ramanathan)   #
# --------------------------------------------------------------------------- #


def n_qp_yield(E_sensor_eV: ArrayLike, design: Design) -> ArrayLike:
    """Quasiparticle COUNT per sensor: N_qp = eps * E_sensor / Delta_tr.

    eps ~= 0.5 (params.EPSILON, imposed deposited-to-signal efficiency lumping
    phonon collection + pair-breaking + trapping + the Delta_abs/Delta_tr
    multiplication); the quantum is the TRAP gap Delta_tr (Al 190 ueV, Hf 40
    ueV). E_sensor in eV, Delta_tr in eV -> dimensionless count.
    """
    d = resolve_design(design)
    return params.EPSILON.value * E_sensor_eV / d.delta_tr.value


def qp_density(N_qp: ArrayLike, design: Design) -> ArrayLike:
    """Per-sensor QP density n_qp = N_qp / V_tr [um^-3]."""
    d = resolve_design(design)
    return N_qp / d.v_tr.value


def tunneling_rate(n_qp: ArrayLike, design: Design) -> ArrayLike:
    """Plateau tunneling rate Gamma_in = K * n_qp [Hz].

    K [Hz*um^3] * n_qp [um^-3] -> Hz. This is the *plateau* (steady) rate; the
    peak instantaneous rate that defines saturation carries an extra two-
    exponential pulse peak factor p (see peak_tunneling_rate).
    """
    d = resolve_design(design)
    return d.K.value * n_qp


def peak_factor(design: Design) -> float:
    """Two-exponential pulse peak factor p (paper Eq. 4), indexed by trap.

    p ~= 0.25 (Al: tau_inj=2 ms, tau_qp=1 ms); p ~= 0.13 (Hf: tau_qp~=0.4 ms).
    peak Gamma_in ~= p * (plateau Gamma_in).
    """
    d = resolve_design(design)
    if d.trap == "Al":
        return params.PEAK_FACTOR_AL.value
    if d.trap == "Hf":
        return params.PEAK_FACTOR_HF.value
    raise KeyError(f"no peak factor recorded for trap material {d.trap!r}")


def peak_tunneling_rate(N_qp: ArrayLike, design: Design) -> ArrayLike:
    """Peak instantaneous tunneling rate ~= p * K * N_qp / V_tr [Hz].

    The saturation-defining quantity: peak Gamma_in > 25 kHz <=> saturated.
    Equivalent to peak_factor(design) * tunneling_rate(qp_density(N_qp, ...)).
    """
    d = resolve_design(design)
    return peak_factor(d) * d.K.value * N_qp / d.v_tr.value


# --------------------------------------------------------------------------- #
# Localized + diffuse per-sensor energy sharing (CONTEXT decision A)           #
# LOW confidence -- f_prompt / r are EXPOSED, SCANNED parameters, NOT derived. #
# --------------------------------------------------------------------------- #


def sensor_energy_split(
    E_dep_eV: ArrayLike,
    f_prompt: float | None = None,
    r: float | None = None,
    n_sensors: float | None = None,
    on_spot: bool = True,
) -> ArrayLike:
    """Per-sensor energy share under the localized-near-hit + diffuse-tail model.

    A fraction ``f_prompt`` of the deposit is absorbed near the impact point,
    spread over a spot of ~pi*r^2 sensors; the remaining (1 - f_prompt) spreads
    diffusely (~uniform) across all ``n_sensors``::

        E_sensor(on spot)  = f_prompt*E_dep/(pi*r^2) + (1-f_prompt)*E_dep/n_sensors
        E_sensor(off spot) =                            (1-f_prompt)*E_dep/n_sensors

    WEAKEST-ANCHOR WARNING: ``f_prompt`` (default 0.3, range 0.1-0.5) and ``r``
    (default 2 sensors, range 1-5) have NO direct thin-wafer QPD measurement.
    They are LOW-confidence, EXPOSED/scannable parameters -- never derived
    values (CONVENTIONS-consistent, 01-RESEARCH Pitfall 4). The equal-split
    limit f_prompt -> 0 is the required sanity knob.

    Parameters default to params.F_PROMPT / params.R_SPOT / params.N_SENSORS.
    """
    if f_prompt is None:
        f_prompt = params.F_PROMPT.value
    if r is None:
        r = params.R_SPOT.value
    if n_sensors is None:
        n_sensors = params.N_SENSORS.value

    n_spot = math.pi * r * r  # sensors under the localized spot
    localized = f_prompt * E_dep_eV / n_spot
    diffuse = (1.0 - f_prompt) * E_dep_eV / n_sensors
    if on_spot:
        return localized + diffuse
    return diffuse


def peak_gamma_in_from_sensor_energy(E_sensor_eV: ArrayLike, design: Design) -> ArrayLike:
    """Convenience chain: E_sensor -> N_qp -> peak Gamma_in [Hz]."""
    d = resolve_design(design)
    return peak_tunneling_rate(n_qp_yield(E_sensor_eV, d), d)


def peak_gamma_in_from_deposit(
    E_dep_eV: ArrayLike,
    design: Design,
    f_prompt: float | None = None,
    r: float | None = None,
    n_sensors: float | None = None,
    on_spot: bool = True,
) -> ArrayLike:
    """Full chain E_dep -> sharing -> N_qp -> peak Gamma_in [Hz] for the on-spot sensor."""
    E_sensor = sensor_energy_split(
        E_dep_eV, f_prompt=f_prompt, r=r, n_sensors=n_sensors, on_spot=on_spot
    )
    return peak_gamma_in_from_sensor_energy(E_sensor, design)


def saturation_onset_energy(design: Design, ceiling_hz: float = SATURATION_CEILING_HZ) -> float:
    """Per-sensor E_sensor [eV] at which peak Gamma_in reaches the 25 kHz ceiling.

    Solve peak Gamma_in = p*K*eps*E/(Delta_tr*V_tr) = ceiling for E:

        E_onset = ceiling * Delta_tr * V_tr / (p * K * eps)

    ~1.27 eV (Al) / ~0.77 eV (Hf) -- Hf saturates first (lower onset).
    """
    d = resolve_design(design)
    return (
        ceiling_hz
        * d.delta_tr.value
        * d.v_tr.value
        / (peak_factor(d) * d.K.value * params.EPSILON.value)
    )


# --------------------------------------------------------------------------- #
# Bandwidth / dead-time censoring switch (CONVENTIONS Section F -- OPEN switch) #
# --------------------------------------------------------------------------- #


def observed_rate(
    Gamma: ArrayLike,
    variant: str = params.DEFAULT_CENSORING,
    tau_d: float | None = None,
) -> ArrayLike:
    """Observed (censored) rate m [Hz] from the true tunneling rate Gamma [Hz].

    Dead-time counting statistics (Knoll Ch. 4; Usman & Patil 2018), resolving
    time tau_d = 40 us = 1/25 kHz (CONVENTIONS Section F; NOT the 20 us sampling
    interval). Two variants, kept as an EXPLICIT SWITCH -- neither is silently
    chosen (the paralyzable-vs-non-paralyzable choice is an OPEN question that
    BLOCKS Phase 5's final numbers):

      * "non_paralyzable" (DEFAULT):  m = Gamma / (1 + Gamma*tau_d)
            monotone, saturating at 1/tau_d = 25 kHz as Gamma -> inf.
      * "paralyzable":                m = Gamma * exp(-Gamma*tau_d)
            non-monotone, PEAKS at Gamma = 1/tau_d = 25 kHz then rolls over.

    Event-handling sub-switch (merge vs drop) is DROP by default (arrivals in
    the dead window are lost, not merged into one timestamped count); the merge
    variant is a Phase-5 refinement and does not change these closed forms.
    """
    if tau_d is None:
        tau_d = params.TAU_D.value
    Gamma = np.asarray(Gamma, dtype=float)
    if variant == "non_paralyzable":
        m = Gamma / (1.0 + Gamma * tau_d)
    elif variant == "paralyzable":
        m = Gamma * np.exp(-Gamma * tau_d)
    else:
        raise ValueError(
            f"unknown censoring variant {variant!r}; "
            f"expected one of {params.CENSORING_VARIANTS}"
        )
    # Return a Python float for scalar input to keep the API friendly.
    return float(m) if m.ndim == 0 else m


def is_saturated(peak_Gamma_in: ArrayLike, ceiling_hz: float = SATURATION_CEILING_HZ) -> ArrayLike:
    """Saturation test: True where peak Gamma_in exceeds the 25 kHz ceiling."""
    peak = np.asarray(peak_Gamma_in, dtype=float)
    sat = peak > ceiling_hz
    return bool(sat) if sat.ndim == 0 else sat


# --------------------------------------------------------------------------- #
# E_rec ESTIMATOR -- Phase-5 STUB (do NOT implement the real estimator here)   #
# --------------------------------------------------------------------------- #


def E_rec_estimator(E_dep_eV: ArrayLike, *, linear_placeholder: bool = False) -> ArrayLike:
    """Reconstructed-energy estimator -- DELIBERATE PHASE-5 STUB.

    The real E_rec estimator (count-integral vs time-over-saturation vs hybrid
    auto-switch) is a Phase-5 RESEARCH DECISION and is intentionally NOT
    implemented here (CONTEXT decision D; contract out_of_scope).

    Default behaviour raises NotImplementedError. Passing
    ``linear_placeholder=True`` returns the clearly-marked LOW-ENERGY LINEAR
    placeholder E_rec ~= eps*E_dep = 0.5*E_dep (CONVENTIONS Sections B/E test
    value). This placeholder is valid ONLY in the unsaturated linear regime and
    is NOT the final estimator -- do not use it where peak Gamma_in > 25 kHz.
    """
    if not linear_placeholder:
        raise NotImplementedError(
            "E_rec estimator is deferred to Phase 5 (count-integral vs "
            "time-over-saturation vs hybrid). Pass linear_placeholder=True for "
            "the low-energy linear placeholder E_rec ~= 0.5*E_dep, valid only "
            "in the unsaturated regime."
        )
    return params.EPSILON.value * E_dep_eV
