# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Prompt (n,gamma) capture NUCLEAR RECOIL spectrum for natural Ge.

Replaces the shapeless hatched band on the combined figure -- the capture channel is
44% of the 10-100 eV RoI background and Phase 14 could only deliver an INTEGRATED
BOUND (<= 4399.78 counts/kg/day), because a spectrum needs the gamma cascade and the
in-repo EGAF line lists carry only 60-71% of the capture Q-value.

PROVENANCE OF THE CASCADES -- NOT DERIVED HERE
----------------------------------------------
The cascade tables are `nrCascadeSim`'s curated natural-Ge level files, frozen at
`data/external/nrcascadesim/`:

    A. N. Villano, K. Harris, S. Brown, "nrCascadeSim -- A simulation tool for
    nuclear recoil cascades resulting from neutron capture", J. Open Source
    Software 7, 3993 (2022); arXiv:2104.02742; DOI 10.5281/zenodo.5579857.
    Repository commit 0f7793e4077b292891ac2fd33db12deb1e140eee.

They are the same tables used by Biffl, Gevorgian, Harris & Villano, PRD 107,
092011 (2023) (arXiv:2212.14148, frozen at `data/external/biffl/`), which is the
published treatment of exactly this background for reactor CEvNS.

WHAT IS REIMPLEMENTED HERE, AND WHAT IS NOT
-------------------------------------------
`nrCascadeSim` requires ROOT, which is not available here and which this project
has a standing line against adding (cf. the OpenMC/Geant4 exclusion). What is used
from it is its DATA -- the curated cascade level/lifetime tables, which are the
nuclear-structure input and the hard part -- plus its Weisskopf coefficients, read
from `src/weisskopf.cpp` rather than recalled (`weisskopf.cpp.reference`).

The recoil kinematics are elementary and are implemented here directly:

    gamma i carries momentum p_i = E_i/c; the nucleus takes -p_i.
    T = |sum of the momenta accumulated since the ion last stopped|^2 / (2 M c^2)

The ONE thing not reproduced is their continuous constant-stopping-power slowing
(`cascadeProd.cpp::geStop`, a Lindhard-based model), which governs how much
momentum survives between emissions. That is bracketed instead of approximated:

  * `mode="slow"`  -- the ion STOPS between every emission, so recoils add as
                      ENERGIES:      T = sum_i E_i^2 / (2 M c^2).   Deterministic
                      per cascade, so this limit is a LINE spectrum.
  * `mode="fast"`  -- the ion never slows, so recoils add as MOMENTUM VECTORS:
                      T = |sum_i p_i|^2 / (2 M c^2).   Continuous, since the
                      relative gamma directions are random.
  * `mode="lifetime"` -- each level is classified by comparing a sampled decay
                      time t ~ Exp(tau) against `tau_stop_fs`; the ion is taken to
                      have stopped if t > tau_stop_fs. A binary stand-in for the
                      continuous model, and it must land BETWEEN the two limits.

The true spectrum lies between "slow" and "fast" BY CONSTRUCTION, because partial
slowing interpolates between "all momentum survives" and "none does". So the
bracket is a bound on the model gap, not an estimate of it.

THE COVERAGE DEFICIT IS REPORTED, NEVER RENORMALISED AWAY
----------------------------------------------------------
The natural-Ge table's cascade fractions sum to 0.2685, not 1: it resolves 26.85%
of captures and the remainder is the unresolved quasi-continuum (the pandemonium
problem that also limits the EGAF route). `coverage_fraction` returns that number
and every emitted spectrum carries it. The spectrum is therefore a spectrum OF THE
RESOLVED CASCADES, and the Phase-14 bound remains the statement covering all
captures. Renormalising to unity would silently assert that the unresolved 73.15%
has the same recoil distribution as the resolved part -- exactly the assumption the
E^2 weighting makes unsafe, since a single hard unobserved gamma contributes far
more recoil than many soft ones.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass

import numpy as np

from . import capture_channel as cc

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
LEVELFILE_DIR = os.path.join(REPO_ROOT, "data", "external", "nrcascadesim")

LEVELFILES = {"fast": "v1_natGe_WFast.txt", "slow": "v1_natGe_WSlow.txt"}

#: u -> keV. Used for the product-nucleus mass; the excitation energy is added on
#: top exactly as cascadeProd.cpp does.
U_TO_KEV = 931494.10242

#: hbar in eV*fs, the value weisskopf.cpp uses (its comment: "converted with google").
HBAR_EV_FS = 0.6582119

#: Weisskopf single-particle WIDTHS in eV for E_gamma in MeV, mass number A.
#: Coefficients read from nrCascadeSim src/weisskopf.cpp (its cited source:
#: Eq. 5, Nucl. Data A 2, 347 (1966)). NOT recalled.
_WEISSKOPF = {
    "E1": (6.748e-2, 2.0 / 3.0, 3),
    "M1": (2.072e-2, 0.0, 3),
    "E2": (4.792e-8, 4.0 / 3.0, 5),
    "M2": (1.472e-8, 2.0 / 3.0, 5),
    "E3": (2.233e-14, 2.0, 7),
    "M3": (6.856e-15, 4.0 / 3.0, 7),
}
#: weisskopf.cpp implements only L <= 3 and falls through with
#: "unrecognized multipole, giving you my slowest multipole, M3".
#: That fallback is not incidental -- it is HOW the WSlow file works: its w(E7),
#: w(M7), w(M4), w(E6) entries all resolve to M3. Reproducing the fallback is
#: therefore required for fidelity, not a convenience.
_WEISSKOPF_FALLBACK = "M3"

#: Target A -> product A for the five natural-Ge capture channels.
_PRODUCT_OF_TARGET = {70: 71, 72: 73, 73: 74, 74: 75, 76: 77}
_TARGET_OF_PRODUCT = {v: k for k, v in _PRODUCT_OF_TARGET.items()}


@dataclass
class Cascade:
    fraction: float          # absolute fraction of ALL captures in natural Ge
    product_A: int           # e.g. 74 for 74Ge
    levels_keV: np.ndarray   # excitation energies below S_n, descending, ending 0.0
    tau_fs: np.ndarray       # lifetime of each level [fs]
    gammas_keV: np.ndarray   # emitted gamma energies, len == len(levels)


@dataclass
class CaptureRecoilSpectrum:
    edges_keV: np.ndarray
    centers_keV: np.ndarray
    dRdT: np.ndarray             # counts / kg / day / keV
    mode: str
    coverage_fraction: float     # fraction of captures the cascade table resolves
    capture_rate_per_kg_day: float
    resolved_rate_per_kg_day: float
    mean_recoil_keV: float
    n_cascades: int
    n_samples: int


def weisskopf_tau_fs(multipole: str, e_gamma_MeV: float, A: int) -> float:
    """Weisskopf single-particle lifetime [fs], nrCascadeSim's own formula."""
    key = multipole if multipole in _WEISSKOPF else _WEISSKOPF_FALLBACK
    coeff, a_pow, e_pow = _WEISSKOPF[key]
    width_eV = coeff * (A ** a_pow) * (e_gamma_MeV ** e_pow)
    return HBAR_EV_FS / width_eV


def _parse_tau(tok: str, e_gamma_MeV: float, A: int) -> float:
    """A lifetime token: either a number in ATTOseconds, or w(XL) to be estimated."""
    m = re.fullmatch(r"w\(([EM]\d+)\)", tok.strip())
    if m:
        return weisskopf_tau_fs(m.group(1), e_gamma_MeV, A)
    return float(tok) * 1.0e-3          # attoseconds -> femtoseconds


def read_level_file(mode: str) -> list[Cascade]:
    """Parse a frozen natural-Ge cascade table.

    Line format (data/external/nrcascadesim/README.md):
        fraction  symbol  A  [levels keV ...]  [lifetimes attoseconds ...]
    The first gamma runs from the neutron separation energy S_n down to levels[0];
    subsequent gammas run between consecutive levels; the last level is the ground
    state (0.0) and terminates the cascade.
    """
    if mode not in LEVELFILES:
        raise KeyError(f"mode {mode!r} not in {sorted(LEVELFILES)}")
    path = os.path.join(LEVELFILE_DIR, LEVELFILES[mode])
    out: list[Cascade] = []
    for raw in open(path):
        if not raw.strip():
            continue
        groups = re.findall(r"\[([^\]]*)\]", raw)
        if len(groups) != 2:
            raise ValueError(f"malformed cascade line in {path}: {raw!r}")
        head = raw.split("[", 1)[0].split()
        fraction, product_A = float(head[0]), int(head[2])
        levels = np.array([float(x) for x in groups[0].split()], dtype=float)
        tau_tokens = groups[1].split()
        if levels.size != len(tau_tokens):
            raise ValueError(
                f"{path}: {levels.size} levels but {len(tau_tokens)} lifetimes in {raw!r}")

        target_A = _TARGET_OF_PRODUCT[product_A]
        Sn_keV = cc.capture_Q_eV(target_A) / 1.0e3      # ENDF MF=3 MT=102 QM
        upper = np.concatenate([[Sn_keV], levels[:-1]])
        gammas = upper - levels
        if np.any(gammas < 0):
            raise ValueError(f"{path}: negative gamma energy in {raw!r}")

        tau = np.array([_parse_tau(t, g / 1.0e3, product_A)
                        for t, g in zip(tau_tokens, gammas)], dtype=float)
        out.append(Cascade(fraction, product_A, levels, tau, gammas))
    return out


def coverage_fraction(mode: str = "fast") -> float:
    """Sum of the table's cascade fractions: the fraction of captures RESOLVED."""
    return float(sum(c.fraction for c in read_level_file(mode)))


def _product_mass_keV(product_A: int, excitation_keV: float = 0.0) -> float:
    return product_A * U_TO_KEV + excitation_keV


def sample_cascade_recoils(cascade: Cascade, n: int, mode: str,
                           rng: np.random.Generator,
                           tau_stop_fs: float = 1.0e3) -> np.ndarray:
    """n recoil energies [keV] for one cascade.

    "slow" is deterministic (one value repeated); the sampling is over the random
    gamma directions, which only matter when momenta are allowed to accumulate.
    """
    M = _product_mass_keV(cascade.product_A)
    g = cascade.gammas_keV
    if mode == "slow":
        return np.full(n, float(np.sum(g ** 2) / (2.0 * M)))

    # Random isotropic direction per gamma per realization: (n, n_gamma, 3)
    ng = g.size
    v = rng.normal(size=(n, ng, 3))
    v /= np.linalg.norm(v, axis=2, keepdims=True)
    p = v * g[None, :, None]                       # momentum in keV/c

    if mode == "fast":
        total_p = np.sum(p, axis=1)                 # (n, 3), vector momentum sum
        return np.sum(total_p ** 2, axis=1) / (2.0 * M)

    if mode != "lifetime":
        raise KeyError(f"mode {mode!r} not in ('fast', 'slow', 'lifetime')")

    # Binary stand-in for continuous slowing: the ion has stopped before the next
    # emission if its sampled decay time exceeds tau_stop_fs.
    t = rng.exponential(np.broadcast_to(cascade.tau_fs, (n, ng)))
    stopped = t > tau_stop_fs
    T = np.zeros(n)
    acc = np.zeros((n, 3))
    for i in range(ng):
        acc += p[:, i, :]
        flush = stopped[:, i] | (i == ng - 1)
        if np.any(flush):
            T[flush] += (acc[flush] ** 2).sum(axis=1) / (2.0 * M)
            acc[flush] = 0.0
    return T


def recoil_spectrum(edges_keV: np.ndarray, mode: str = "fast",
                    n_per_cascade: int = 200_000, seed: int = 20260723,
                    tau_stop_fs: float = 1.0e3,
                    capture_rate_per_kg_day: float | None = None
                    ) -> CaptureRecoilSpectrum:
    """dR/dT [counts/kg/day/keV] for the RESOLVED capture cascades in natural Ge."""
    cascades = read_level_file(mode if mode != "lifetime" else "fast")
    cov = float(sum(c.fraction for c in cascades))
    if capture_rate_per_kg_day is None:
        capture_rate_per_kg_day = _default_capture_rate()

    rng = np.random.default_rng(seed)
    hist = np.zeros(edges_keV.size - 1)
    mean_num = 0.0
    for c in cascades:
        T = sample_cascade_recoils(c, n_per_cascade, mode, rng,
                                   tau_stop_fs=tau_stop_fs)
        w = c.fraction * capture_rate_per_kg_day / n_per_cascade
        hist += np.histogram(T, bins=edges_keV, weights=np.full(T.size, w))[0]
        mean_num += c.fraction * float(T.mean())

    return CaptureRecoilSpectrum(
        edges_keV=edges_keV,
        centers_keV=np.sqrt(edges_keV[:-1] * edges_keV[1:]),
        dRdT=hist / np.diff(edges_keV),
        mode=mode,
        coverage_fraction=cov,
        capture_rate_per_kg_day=capture_rate_per_kg_day,
        resolved_rate_per_kg_day=cov * capture_rate_per_kg_day,
        mean_recoil_keV=mean_num / cov,
        n_cascades=len(cascades),
        n_samples=n_per_cascade * len(cascades),
    )


def _default_capture_rate() -> float:
    """The Phase-14 in-RoI capture BOUND, reused as the total capture rate.

    Phase 14 established R_RoI <= R_capture = 4399.78 counts/kg/day by the
    one-recoil-per-capture argument, so that number IS the total capture rate.
    Reusing it keeps this spectrum on the same normalisation the bound used, which
    is what makes the two directly comparable on the figure.
    """
    return 4399.78
