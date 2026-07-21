# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
#
# Stage-1 constant registry for the QPD reconstructed-energy pipeline.
#
# SOURCE OF TRUTH: GPD/CONVENTIONS.md (locked) + GPD/state.json convention_lock.
# Every convention-bearing numeric factor below is machine-checked against the
# CONVENTIONS.md "Numerical Factor Registry" by tests/test_conventions_consistency.py.
#
# Device parameters are transcribed VERBATIM from Table II of
#   K. Ramanathan et al., APS Open Science 1, 000013 (2026),
#   DOI 10.1103/kqd2-spb1, arXiv:2405.17192 (Table II, p. 14),
# as recorded in GPD/phases/01-.../01-RESEARCH.md. They are NOT paraphrased
# from memory.
#
# UNITS (I/O practical): energy in eV; time in s; length in um; K in Hz*um^3;
# tunneling rates in Hz; densities in um^-3; temperature in K. Cross-section
# internals live in cevns.py (GeV natural units, converted to cm^2 there).
#
# FORBIDDEN (CONVENTIONS Section B): a fieldless phonon calorimeter has a single
# unified phonon energy scale. There is deliberately NO electron-equivalent vs
# nuclear-recoil scale split and NO ionization-suppression factor anywhere in
# this module (see CONVENTIONS Section B forbidden proxies).

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

# --------------------------------------------------------------------------- #
# Provenance record shape                                                      #
# --------------------------------------------------------------------------- #

_CONFIDENCE = {"HIGH", "MEDIUM", "LOW", "DERIVED"}


@dataclass(frozen=True)
class Param:
    """A single provenance-tagged constant.

    value      : numeric value in the stated units
    units      : unit string ("" for dimensionless)
    source     : where the value comes from (paper table, convention section, ...)
    confidence : one of HIGH / MEDIUM / LOW / DERIVED
    note       : optional flag text (assumptions, caveats, film-phase warnings)
    """

    value: float
    units: str
    source: str
    confidence: str
    note: Optional[str] = None

    def __post_init__(self) -> None:
        if self.confidence not in _CONFIDENCE:
            raise ValueError(
                f"confidence {self.confidence!r} not in {_CONFIDENCE}"
            )


# --------------------------------------------------------------------------- #
# CEvNS cross-section constants (CONVENTIONS Sections A.2 / C)                  #
# --------------------------------------------------------------------------- #

G_F = Param(
    1.1663787e-5,
    "GeV^-2",
    "PDG 2024 Fermi constant; CONVENTIONS Section C",
    "HIGH",
)
SIN2_THETA_W = Param(
    0.2387,
    "",
    "Low-energy MS-bar weak mixing angle; CONVENTIONS Section C (NOT 0.2312 at M_Z)",
    "HIGH",
)
ONE_MINUS_4SIN2THETAW = Param(
    0.0452,
    "",
    "Proton weak coupling 1-4 sin^2 theta_W; CONVENTIONS Section C (= 1 - 4*0.2387)",
    "HIGH",
)
HBARC2 = Param(
    3.894e-28,
    "GeV^2*cm^2",
    "(hbar c)^2 unit conversion; CONVENTIONS Section A.2 (dropping this is the #1 CEvNS bug)",
    "HIGH",
)
# CEvNS closed-form prefactor is /(4*pi), NOT /(8*pi). The /8pi form is a
# factor-of-2 error (CONVENTIONS Section C, forbidden proxy fp-prefactor).
CEVNS_PREFACTOR_DENOM = Param(
    4.0 * math.pi,
    "",
    "Closed-form CEvNS prefactor denominator 4*pi; CONVENTIONS Section C (NOT 8*pi)",
    "HIGH",
)

# Representative CEvNS benchmark isotope: 72Ge.
BENCHMARK_ISOTOPE = {
    "name": "72Ge",
    "Z": Param(32, "", "72Ge proton number; CONVENTIONS Section C benchmark", "HIGH"),
    "N": Param(40, "", "72Ge neutron number; CONVENTIONS Section C benchmark", "HIGH"),
}

# --------------------------------------------------------------------------- #
# Natural germanium isotope table (Phase 3, Plan 03-01)                        #
# --------------------------------------------------------------------------- #
# The per-isotope CEvNS sum is the decisive physics (forbidden proxy fp-lumped-A:
# a single lumped A=72.63 smooths the five-step T_max endpoint structure). Z=32
# for all; N=38/40/41/42/44 -> A=70/72/73/74/76.
#
# Number (atom) abundances are the IUPAC/CIAAW representative isotopic
# composition of natural Ge (Meija et al., Pure Appl. Chem. 88, 293 (2016),
# CIAAW 2013 "representative" column): 70Ge 20.57%, 72Ge 27.45%, 73Ge 7.75%,
# 74Ge 36.50%, 76Ge 7.73% (atom %). They sum to 1.0000. [MEDIUM confidence:
# representative values, small isotope-abundance spread across sources.]
#
# Nuclear mass M_i is taken as A_i * u with u = 931.494 MeV (the CONVENTIONS/plan
# spec; binding-energy / electron-mass corrections are <~1e-3 and irrelevant at
# the CEvNS kinematic-factor level of ~T/E_nu ~ 1e-3).
#
# N_target,i = x_i * GE_ATOMS_PER_KG (sum = 8.29e24 /kg), consistent with the
# Section D per-kg normalization (1000 g / 72.63 g/mol * N_A).

_U_MEV = 931.494  # atomic mass unit in MeV (CODATA; matches CONVENTIONS)


@dataclass(frozen=True)
class GeIsotope:
    """A single natural-Ge isotope for the CEvNS per-isotope sum.

    A          : mass number (used for the Helm nuclear radius c ~ A^{1/3})
    Z, N       : proton / neutron numbers (Z=32 for all Ge)
    abundance  : number (atom) fraction, dimensionless (sum over isotopes = 1)
    M_MeV      : nuclear mass = A * 931.494 MeV
    name       : label ("70Ge", ...)
    """

    A: int
    Z: int
    N: int
    abundance: float
    M_MeV: float
    name: str


GE_ISOTOPES = (
    GeIsotope(70, 32, 38, 0.2057, 70 * _U_MEV, "70Ge"),
    GeIsotope(72, 32, 40, 0.2745, 72 * _U_MEV, "72Ge"),
    GeIsotope(73, 32, 41, 0.0775, 73 * _U_MEV, "73Ge"),
    GeIsotope(74, 32, 42, 0.3650, 74 * _U_MEV, "74Ge"),
    GeIsotope(76, 32, 44, 0.0773, 76 * _U_MEV, "76Ge"),
)

# Helm form-factor parameters (Lewin & Smith, Astropart. Phys. 6, 87 (1996),
# Appendix): a = 0.52 fm (surface diffuseness), s = 0.90 fm (skin thickness),
# c(A) = 1.23 A^{1/3} - 0.60 fm; R_0^2 = c^2 + (7/3) pi^2 a^2 - 5 s^2.
HELM_A_FM = 0.52
HELM_S_FM = 0.90
HBAR_C_MEV_FM = 197.327  # hbar c in MeV*fm (q[fm^-1] = q[MeV] / 197.327)

# --------------------------------------------------------------------------- #
# Detector / normalization constants (CONVENTIONS Section D)                   #
# --------------------------------------------------------------------------- #

GE_ATOMS_PER_KG = Param(
    8.29e24,
    "atoms/kg",
    "1000 g / 72.63 g/mol * N_A; CONVENTIONS Section D",
    "HIGH",
)
GE_DENSITY = Param(
    5.323,
    "g/cm^3",
    "Germanium density; CONVENTIONS Section D",
    "HIGH",
)
GE_MOLAR_MASS = Param(
    72.63,
    "g/mol",
    "Ge natural-abundance molar mass; CONVENTIONS Section D",
    "HIGH",
)
WAFER_VOLUME = Param(
    20.65,
    "cm^3",
    "4in x 4in x 2mm wafer; CONVENTIONS Section D",
    "HIGH",
)
WAFER_MASS = Param(
    109.9,
    "g",
    "20.65 cm^3 * 5.323 g/cm^3 ~= 110 g; CONVENTIONS Section D",
    "HIGH",
)
N_SENSORS = Param(
    10300,
    "",
    "~10300 sensors at 1/mm^2 on ONE instrumented face; CONVENTIONS Section D",
    "HIGH",
)
SENSOR_PITCH = Param(
    1.0,
    "mm",
    "1 mm sensor pitch (1/mm^2 density); CONVENTIONS Section D",
    "HIGH",
)
REACTOR_POWER = Param(
    3.0,
    "GW_th",
    "Reactor thermal power 3 GW_th (thermal, NOT electric); CONVENTIONS Section D",
    "HIGH",
)
STANDOFF = Param(
    25.0,
    "m",
    "Detector standoff distance; CONVENTIONS Section D",
    "HIGH",
)
REACTOR_FLUX = Param(
    7.5e12,
    "nubar/cm^2/s",
    "~7-8e12 nubar/cm^2/s at 25 m for 3 GW_th; CONVENTIONS Section D (DERIVED, CONUS+ scaling)",
    "DERIVED",
    note="Range 7-8e12; midpoint recorded. Derived, not measured.",
)

# --------------------------------------------------------------------------- #
# Efficiency + censoring constants (CONVENTIONS Sections E / F)                #
# --------------------------------------------------------------------------- #

EPSILON = Param(
    0.5,
    "",
    "Deposited-to-signal efficiency baseline; CONVENTIONS Section E (imposed forward-model definition)",
    "MEDIUM",
    note="+/-10-20% design-dependent band; SAME baseline both designs. "
    "Paper physical estimate eta_ce ~= 0.3 is an independent cross-reference, NOT baseline.",
)
TAU_D = Param(
    40e-6,
    "s",
    "Resolving (dead) time = 1/25 kHz Nyquist; CONVENTIONS Section F (LOCKED)",
    "HIGH",
    note="40 us resolving time, NOT the 20 us sampling interval.",
)
SAMPLING = Param(
    20e-6,
    "s",
    "Sampling interval = 1/50 kHz; CONVENTIONS Section F",
    "HIGH",
)
DEFAULT_CENSORING = "non_paralyzable"  # CONTEXT decision (D); paralyzable + merge/drop remain as code switches.
CENSORING_VARIANTS = ("non_paralyzable", "paralyzable")

# Two-exponential peak (shape) factors, for Plan 02 / Phase 5 saturation onset.
PEAK_FACTOR_AL = Param(
    0.25,
    "",
    "Two-exponential pulse peak factor, Al (tau_inj=2ms, tau_qp=1ms); 01-RESEARCH Eq.(4)",
    "MEDIUM",
    note="Recorded for Plan 02 / Phase 5; not used in Phase 1 arithmetic.",
)
PEAK_FACTOR_HF = Param(
    0.13,
    "",
    "Two-exponential pulse peak factor, Hf (tau_inj=2ms, tau_qp~=0.4ms); 01-RESEARCH Eq.(4)",
    "MEDIUM",
    note="Recorded for Plan 02 / Phase 5; not used in Phase 1 arithmetic.",
)

# --------------------------------------------------------------------------- #
# Absorber superconducting gaps (CONVENTIONS Section G; 01-RESEARCH)           #
# --------------------------------------------------------------------------- #
# Al plays TRAP (design 1) and ABSORBER (design 2) with the same 190 ueV gap.

DELTA_ABS_AL = Param(
    190e-6,
    "eV",
    "Aluminum gap 190 ueV; Table II (Ramanathan 2026)",
    "HIGH",
    note="Al is the trap in Ta->Al and the absorber in Al->Hf; same 190 ueV gap in both roles.",
)
DELTA_ABS_TA = Param(
    0.68e-3,
    "eV",
    "Tantalum absorber gap ~= 0.68 meV from bulk alpha-Ta BCS: 1.764 k_B T_c, T_c=4.48 K",
    "MEDIUM",
    note="ASSUMPTION: bulk alpha-Ta; film phase UNVERIFIED (alpha vs beta shifts T_c 5-9x). "
    "materials.yaml has NO Ta entry. Firm up in Phase 5. Cite bulk Ta T_c ~= 4.48 K.",
)

# --------------------------------------------------------------------------- #
# Per-design trap parameters (Table II, indexed by TRAP material)             #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class TrapDesign:
    """Per-design junction/trap parameters + absorber gap, all provenance-tagged.

    name        : project design label ("Ta->Al" or "Al->Hf")
    absorber    : absorber material symbol
    trap        : trap/junction material symbol (the Table II column)
    delta_tr    : trap superconducting gap [eV]
    v_tr        : effective trap volume [um^3]
    K           : tunneling proportionality [Hz*um^3] (Gamma_in = K * n_qp)
    tau_qp      : QP recombination lifetime [s]
    tau_inj     : QP injection time [s]
    gamma_out   : back-tunneling rate [Hz]
    n_0         : quiescent QP density [um^-3]
    fano        : Fano factor [dimensionless]
    T_opr       : operating temperature [K]
    delta_abs   : absorber gap [eV]
    """

    name: str
    absorber: str
    trap: str
    delta_tr: Param
    v_tr: Param
    K: Param
    tau_qp: Param
    tau_inj: Param
    gamma_out: Param
    n_0: Param
    fano: Param
    T_opr: Param
    delta_abs: Param

    @property
    def trapping_ratio(self) -> float:
        """Delta_abs / Delta_tr. Trapping requires this >= ~2 (LOWER bound, not a ceiling)."""
        return self.delta_abs.value / self.delta_tr.value


# Design 1: Ta absorber + Aluminum trap column of Table II.
DESIGN_TA_AL = TrapDesign(
    name="Ta->Al",
    absorber="Ta",
    trap="Al",
    delta_tr=Param(190e-6, "eV", "Table II Al gap (Ramanathan 2026)", "HIGH"),
    v_tr=Param(100.0, "um^3", "Table II effective V_tr, Al (100 = 50x2 OCS)", "HIGH"),
    K=Param(3e3, "Hz*um^3", "Table II K = 3 kHz*um^3, Al", "HIGH"),
    tau_qp=Param(1e-3, "s", "Table II tau_qp = 1 ms, Al", "HIGH"),
    tau_inj=Param(2e-3, "s", "Table II tau_inj = 2 ms (global)", "HIGH"),
    gamma_out=Param(2e3, "Hz", "Table II Gamma_out = 2 kHz, Al-CPB", "HIGH"),
    n_0=Param(0.3, "um^-3", "Table II n_0 = 0.3 um^-3, Al", "HIGH"),
    fano=Param(0.2, "", "Table II Fano F = 0.2 (global)", "HIGH"),
    T_opr=Param(0.1, "K", "Table II T_opr = 0.1 K, Al", "HIGH"),
    delta_abs=DELTA_ABS_TA,  # flagged MEDIUM-confidence bulk alpha-Ta assumption
)

# Design 2: Al absorber + Hafnium trap column of Table II.
DESIGN_AL_HF = TrapDesign(
    name="Al->Hf",
    absorber="Al",
    trap="Hf",
    delta_tr=Param(40e-6, "eV", "Table II Hf gap (Ramanathan 2026)", "HIGH"),
    v_tr=Param(1000.0, "um^3", "Table II effective V_tr, Hf (1000 = 500x2 OCS)", "HIGH"),
    K=Param(2e4, "Hz*um^3", "Table II K = 20 kHz*um^3, Hf", "HIGH"),
    tau_qp=Param(
        400e-6,
        "s",
        "Table II caption/lit [92] ~400 us for Hf",
        "MEDIUM",
        note="Table cell reads 1 ms (Al-side footnote b); caption gives ~400 us for Hf. "
        "Paper's own flagged uncertainty.",
    ),
    tau_inj=Param(2e-3, "s", "Table II tau_inj = 2 ms (global)", "HIGH"),
    gamma_out=Param(1e4, "Hz", "Table II Gamma_out = 10 kHz, Hf-CPB", "HIGH"),
    n_0=Param(0.03, "um^-3", "Table II n_0 = 0.03 um^-3, Hf", "HIGH"),
    fano=Param(0.2, "", "Table II Fano F = 0.2 (global)", "HIGH"),
    T_opr=Param(0.025, "K", "Table II T_opr = 0.025 K, Hf", "HIGH"),
    delta_abs=DELTA_ABS_AL,  # Al = 190 ueV absorber gap
)

DESIGNS = {DESIGN_TA_AL.name: DESIGN_TA_AL, DESIGN_AL_HF.name: DESIGN_AL_HF}

# --------------------------------------------------------------------------- #
# Phonon-sharing defaults (CONTEXT decision A; 01-RESEARCH) — LOW confidence   #
# EXPOSED as scannable parameters, NOT derived values.                         #
# --------------------------------------------------------------------------- #

F_PROMPT = Param(
    0.3,
    "",
    "Localized+diffuse prompt fraction; 01-RESEARCH geometric-argument default",
    "LOW",
    note="EXPOSED PARAMETER, not a derived value. Range 0.1-0.5. "
    "Least-constrained number in the pipeline; muon spectrum shape depends strongly on it.",
)
F_PROMPT_RANGE = (0.1, 0.5)
R_SPOT = Param(
    2.0,
    "sensors",
    "Localization spot radius; 01-RESEARCH geometric-argument default",
    "LOW",
    note="EXPOSED PARAMETER, not a derived value. Range 1-5 sensors "
    "(~wafer thickness 2 mm ~= 2 sensor pitches).",
)
R_SPOT_RANGE = (1.0, 5.0)


# --------------------------------------------------------------------------- #
# Convenience accessors                                                        #
# --------------------------------------------------------------------------- #


def trapping_ratio(design_name: str) -> float:
    """Delta_abs/Delta_tr for a named design (Ta->Al = 3.58, Al->Hf = 4.75)."""
    return DESIGNS[design_name].trapping_ratio
