# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""The 110 g monolithic wafer's OWN muon-rejection handles (Phase 8, Plan 08-02).

Success Criteria 3 and 4 of ROADMAP Phase 8. This module answers one question:
*what muon rejection does the wafer earn from its own geometry and its own
deposit distribution* -- and, just as importantly, what it does **not** earn.

NO NUCLEUS REJECTION PERCENTAGE IS APPLIED AS A COMPUTATIONAL VALUE ANYWHERE IN
THIS MODULE.
    Every number produced here traces to exactly one of two places: (a) the
    wafer's own frozen chord (x) Landau-Vavilov deposit distribution
    ``data/muon_dRdEdep.csv``, or (b) a counting identity about a
    single-readout target. Nothing traces to a NUCLEUS efficiency. NUCLEUS
    percentages appear below **only inside docstrings**, each explicitly
    labelled as a number that is quoted and *not applied*. This guards the
    milestone-wide forbidden proxy ``fp-veto-credit-transfer``.

THE TWO ACCEPTANCES ARE SEPARATE QUANTITIES AND ARE NEVER MERGED.
    ``a_self_direct(E_cut)``  -- muons that CROSS the wafer, tagged by their own
                                 deposit in the wafer.  ~1 at every threshold
                                 of interest.
    ``A_SELF_INDUCED``        -- muon-INDUCED secondaries (neutrons and
                                 bremsstrahlung gammas born in the surrounding
                                 Pb) whose parent muon never enters the wafer.
                                 Exactly 0.0.
    There is deliberately no function, constant, column, or table cell in this
    module -- or in ``data/wafer_self_veto.csv`` -- that merges the two into one
    number. Merging them would be ``fp-lumped-acceptance``: the near-unit direct
    acceptance would mask the zero induced acceptance and manufacture something
    that reads like an inherited veto efficiency. The class NUCLEUS's vetoes
    actually suppress is the induced secondaries, which is exactly the class the
    wafer cannot touch.

PHYSICAL READING OF ``a_self_direct`` -- the half that was never the difficulty.
    The frozen artifact's vertical-chord Landau MPV is 1.2323 MeV (mean
    1.4585 MeV). Against thresholds of 10 eV, 1 keV and 100 keV -- four to eight
    orders of magnitude below the MPV -- an acceptance of ~1 is the expected and
    physically meaningful outcome: **the wafer is an excellent self-tagger for
    muons that cross it.** This is the easy half of the problem. It says nothing
    whatsoever about the muon-induced shower born outside the wafer, and the
    whole point of reporting two numbers is to keep that asymmetry visible.

MULTIPLICITY: EXACTLY ZERO, BY COUNTING.
    NUCLEUS's selection requires a hit in one and only one target detector
    (quote in ``mult_rejection``). With N = 1 readout channel that requirement is
    satisfied identically, so the cut removes nothing: ``mult_rejection(1)``
    returns exactly ``0.0`` by an early return, not by a probability model that
    happens to evaluate near zero.

COUNTERPOINT THAT CUTS AGAINST THIS PROJECT'S FRAMING -- recorded, not buried.
    NUCLEUS themselves assess the marginal benefit of the multiplicity cut,
    quoted verbatim from ``08-01-SOURCE-EVIDENCE.md`` §B.7
    (arXiv:2509.03559v1 §5.2.1):

        "Finally, the benefit of applying all vetoes, i.e. (i) using the IV and
        (ii) requesting only one cryogenic detector hit in addition to the MV
        and COV anti-coincidence selection criteria, is very marginal."

    Read plainly: because the handle NUCLEUS gains from that cut is very
    marginal in the first place, **the absolute background cost of the wafer's
    identically-zero multiplicity handle is small.** That is a point in the
    wafer's favour and against this project's own "we lose their multiplicity
    cut" framing, and it is reported here rather than suppressed. The zero is
    not softened either: it is exactly zero, and it is small in consequence.

UNCREDITED FUTURE HANDLE (must not be used to fill the multiplicity gap).
    The wafer carries ~10,300 QPD sensors at 1/mm^2 on one instrumented face
    (``GPD/CONVENTIONS.md`` §D), so in principle it has a *spatial*
    position-reconstruction / track-vs-point observable that NUCLEUS's
    inter-crystal multiplicity cut does not have. That is a genuinely different
    observable, with no established efficiency and no design behind it. It is
    **not credited anywhere in v2.0** and may not be used to fill the
    multiplicity gap (``fp-spatial-handle-credit``, 08-RESEARCH Pitfall 10).

PATHS (08-RESEARCH Pitfall 9).
    The frozen inputs are ``data/muon_dRdEdep.csv`` and
    ``src/qpd_potential/muon_deposit.py``. The paths
    ``data/muon/muon_dep_spectrum.csv`` and ``src/muon/deposited_spectrum.py``
    recorded in ``04-01-SUMMARY.md`` front-matter DO NOT EXIST and are never
    referenced here.

CONVENTIONS.
    Energy: unified phonon E_dep scale, no ionization quenching
    (``GPD/CONVENTIONS.md`` §B). Geometry and wafer mass: §D, imported from
    ``wafer_geometry`` rather than restated. Resolving times: §F (40 us Nyquist,
    20 us sampling; non-paralyzable censoring locked project-wide 2026-07-21).
"""
from __future__ import annotations

import csv
import re
from functools import lru_cache
from pathlib import Path

import numpy as np

from . import wafer_geometry as wg
from . import interp_guard as ig

#: numpy >= 2.0 renamed ``trapz`` to ``trapezoid``; support both.
_trapz = getattr(np, "trapezoid", None) or np.trapz

# --------------------------------------------------------------------------- #
# Frozen inputs and locked constants                                           #
# --------------------------------------------------------------------------- #
_REPO_ROOT = Path(__file__).resolve().parents[2]

#: The frozen v1.0 Phase-4 muon deposit spectrum. 1e9 MC samples, validated.
#: NOT re-run here: regenerating it costs hours and risks silent drift against a
#: validated artifact for zero physics gain (contract: forbidden estimator
#: family "re-run Monte Carlo replacing the frozen artifact").
MUON_CSV = _REPO_ROOT / "data" / "muon_dRdEdep.csv"

#: Output table for this plan.
SELF_VETO_CSV = _REPO_ROOT / "data" / "wafer_self_veto.csv"

#: Wafer mass [kg]. CONVENTIONS §D via wafer_geometry (109.9 g); not restated.
M_WAFER_KG = wg.MASS_KG  # 0.1099 kg

SECONDS_PER_DAY = 86_400.0

#: Resolving times, CONVENTIONS §F (locked 2026-07-21, non-paralyzable).
#: 1/25 kHz Nyquist resolving time and 1/50 kHz sampling interval. BOTH stated.
TAU_DEAD_RESOLVE_S = 40e-6
TAU_DEAD_SAMPLE_S = 20e-6

#: Omnidirectional muon attenuation factor at the NUCLEUS Chooz Very-Near-Site.
#: VERIFICATION VERDICT (Plan 08-01, ``08-01-SOURCE-EVIDENCE.md`` §E.1.2):
#: **verified verbatim, arXiv:2509.03559v1 Sect. 4.1**.
MU_ATTENUATION_VNS = 1.41  # +/- 0.02

#: Omnidirectional overburden [m w.e.]. VERIFICATION VERDICT (Plan 08-01,
#: ``08-01-SOURCE-EVIDENCE.md`` §E.1.1): **verified verbatim,
#: arXiv:2509.03559v1 Sect. 4.1**. Nuance carried forward from §E.1.2: the
#: paper's §4.1 contains TWO overburden numbers -- the *simulated*
#: overburden-map average 2.92 +/- 0.01 m w.e. (this constant) and the
#: *measured* cosmic-wheel value 2.9 +/- 0.1 m w.e., which is the one the
#: 1.41 +/- 0.02 attenuation factor is stated to correspond to. They are
#: consistent but they are not the same measurement.
OVERBURDEN_MWE = 2.92  # +/- 0.01

#: Verbatim carried-anchor verdict string, reproduced into the data table so a
#: reader never sees either anchor without its verification status attached.
ANCHOR_VERDICT = (
    "verified verbatim, arXiv:2509.03559v1 Sect. 4.1 "
    "(08-01-SOURCE-EVIDENCE.md E.1.1 overburden 2.92 +/- 0.01 m w.e.; "
    "E.1.2 attenuation 1.41 +/- 0.02)"
)

#: NUCLEUS Chooz target-detector count. This is a **geometry fact** (a count of
#: crystals), not a rejection efficiency: ``08-01-SOURCE-EVIDENCE.md`` §A.4/§A.5,
#: arXiv:2508.02488v1 -- "18 cryogenic target detectors".
N_CHANNELS_NUCLEUS_CHOOZ = 18

#: Illustrative per-channel occupancy for the N > 1 multiplicity model. ARBITRARY.
#: It is NOT derived, NOT measured, and NOT a NUCLEUS number. It exists only so
#: that ``mult_rejection(18) > 0`` can be asserted as a *contrast* against the
#: N = 1 identity. See ``mult_rejection`` for why no value computed from it is
#: allowed into ``data/wafer_self_veto.csv``.
P_HIT_ILLUSTRATIVE = 0.05


# --------------------------------------------------------------------------- #
# A_self_induced -- the number the wafer cannot earn                           #
# --------------------------------------------------------------------------- #
A_SELF_INDUCED = 0.0
"""Wafer self-veto acceptance for muon-INDUCED secondaries. Exactly 0.0.

THE PHYSICAL ARGUMENT (this is the content; the value alone is not).
    The wafer's only muon-tagging handle is *the parent muon's own energy
    deposit in the wafer*. A neutron or a bremsstrahlung gamma produced when a
    muon interacts in the surrounding lead reaches the wafer while its parent
    muon passes nowhere near it. There is therefore no coincident signal to tag
    the secondary with, and a single self-vetoing wafer rejects none of this
    class. Hence exactly zero -- not "small", not "reduced".

WHY NUCLEUS'S HEADLINE NUMBER HAS NO TRANSFER ROUTE.
    Quoted verbatim from ``08-01-SOURCE-EVIDENCE.md`` §B.9
    (arXiv:2509.03559v1 §5.2.1; the phrase "muon-induced" is *inside* the
    source sentence). **This is a NUCLEUS number quoted for identification and
    it is NOT applied anywhere in this module:**

        "Unsurprisingly, the MV was also found to be very efficient. When
        combined with the COV, they are predicted to reject more than 99.8% of
        the muon-induced backgrounds in the CEnuNS RoI, making them a
        negligible contributor to the total background budget (see section
        5.3)."

    That sentence is a **rejection of muon-INDUCED secondary backgrounds**, not
    a **muon tagging efficiency**. The two are different observables. Reading it
    as a tagging efficiency (08-RESEARCH Pitfall 2) makes it look inheritable;
    it is not. It was earned by a 5-cm plastic-scintillator muon veto plus a
    six-crystal HPGe cryogenic outer veto surrounding gram-scale targets. A
    110 g monolithic wafer has neither. Even the near-unit ``a_self_direct``
    below cannot substitute for it, because ``a_self_direct`` describes the
    opposite population: muons that cross the wafer, not secondaries whose
    parent does not.

HONESTY CAVEAT -- zero is a defensible FLOOR, not an impossibility proof.
    A muon-induced secondary that happens to be accompanied into the wafer by
    its own parent muon *would* be tagged. That configuration is argued to be
    negligible here; it has not been measured or simulated in this phase. A
    referee could reasonably argue that the wafer's large 103.23 cm^2 face makes
    such accidental parent-plus-secondary coincidences non-negligible, which
    would push this quantity slightly above zero. The honest response is that
    zero is the defensible floor, not that the effect is impossible.
"""


# --------------------------------------------------------------------------- #
# Frozen-spectrum loading and the normalization closure                        #
# --------------------------------------------------------------------------- #
@lru_cache(maxsize=1)
def _load_frozen() -> tuple[tuple[float, ...], tuple[float, ...], float]:
    """Load ``data/muon_dRdEdep.csv``; return (E_dep keV, dR/dE_dep, header Hz).

    Returned as tuples so the ``lru_cache`` payload is immutable.
    """
    header: list[str] = []
    rows: list[list[float]] = []
    with open(MUON_CSV) as fh:
        for line in fh:
            if line.startswith("#"):
                header.append(line)
                continue
            if line.startswith("E_dep"):
                continue
            parts = line.strip().split(",")
            if len(parts) < 3:
                continue
            rows.append([float(parts[0]), float(parts[1])])
    if not rows:
        raise ValueError(f"no data rows parsed from {MUON_CSV}")
    match = None
    for line in header:
        match = re.search(r"integral_muon_rate_Hz\s*=\s*([0-9.eE+\-]+)", line)
        if match:
            break
    if match is None:
        raise ValueError(f"no 'integral_muon_rate_Hz = ...' in {MUON_CSV} header")
    arr = np.asarray(rows, dtype=float)
    return tuple(arr[:, 0]), tuple(arr[:, 1]), float(match.group(1))


def frozen_spectrum() -> tuple[np.ndarray, np.ndarray]:
    """(E_dep [keV], dR/dE_dep [counts/kg/day/keV]) on the native log grid."""
    e_grid, rate, _ = _load_frozen()
    return np.asarray(e_grid), np.asarray(rate)


def frozen_header_rate_Hz() -> float:
    """The integral muon rate the Phase-4 plan wrote into the frozen header [Hz]."""
    return _load_frozen()[2]


def table_floor_keV() -> float:
    """Lowest tabulated E_dep [keV]. 1.014497e-02 keV = 10.14 eV.

    An ``E_cut`` of 10 eV therefore sits **at (marginally below) the table
    floor**, i.e. at the edge of the artifact's support. This module reports
    that fact rather than extrapolating below it: for any ``E_cut`` at or below
    the floor the acceptance is exactly 1.0 by construction, because the frozen
    distribution carries no probability mass there to lose.
    """
    return _load_frozen()[0][0]


def table_ceiling_keV() -> float:
    """Highest tabulated E_dep [keV] (~1.97e5 keV = 197 MeV)."""
    return _load_frozen()[0][-1]


def integral_rate_Hz() -> float:
    """Full-range integral of the frozen spectrum, converted to Hz.

    THE ACCEPTANCE DENOMINATOR. Computed once, in one place:

        int dR/dE_dep dE   [counts/kg/day]     (trapezoid, native log grid)
          x  M_WAFER_KG    [kg]                 -> counts/day
          /  86400 s/day                        -> counts/s = Hz

    Dimensional check: [counts kg^-1 day^-1 keV^-1] x [keV] x [kg] / [s day^-1]
    = [counts s^-1] = [Hz].

    This must reproduce the frozen header value 1.3659 Hz. A failure here is a
    normalization error in the acceptance denominator and BLOCKS the acceptance
    numbers; it is never rescaled away (acceptance test V6 /
    ``test-normalization-closure``).
    """
    e_grid, rate = frozen_spectrum()
    counts_per_kg_day = float(_trapz(rate, e_grid))
    return counts_per_kg_day * M_WAFER_KG / SECONDS_PER_DAY


def _tail_integral(e_cut_keV: float) -> float:
    """int_{E_cut}^{E_max} dR/dE_dep dE on the native grid [counts/kg/day].

    The native log grid is used as-is -- no re-binning. A single interpolated
    point is inserted at ``E_cut`` so that the partial first bin is handled
    exactly rather than snapped to the nearest grid node; without it the
    acceptance would be a step function of ``E_cut`` and the monotonicity check
    would be testing the grid, not the physics.

    Plan 10-01: guarded. The declared evaluation domain is exactly the frozen
    grid span [1.014497e-02, 1.97142e5] keV -- no witness exists for any
    extension, because ``a_self_direct`` short-circuits to 1.0 at or below the
    floor and 0.0 at or above the ceiling and therefore never reaches here out
    of domain. What the guard stops is a DIRECT call: before it,
    ``_tail_integral`` at 1e-4 keV returned 1073307.752 counts/kg/day against a
    true full integral of 1073307.591 -- a finite, nearly-right, entirely
    fabricated number built from the clamped floor rate of 16.01101 extended
    over a decade of energy that carries no data. Above the ceiling it returned
    exactly 0.0, which is a silent zero, not an error.
    """
    e_grid, rate = frozen_spectrum()
    ig.check_domain(e_cut_keV, ig.Domain(
        quantity="muon dR/dE_dep tail integral cut energy",
        lo=float(e_grid[0]), hi=float(e_grid[-1]), units="keV",
        table=str(MUON_CSV),
        table_lo=float(e_grid[0]), table_hi=float(e_grid[-1]),
        note="np.interp previously clamped the rate to 16.01101 below the floor "
             "and 0.003293117 above the ceiling.",
    ))
    idx = int(np.searchsorted(e_grid, e_cut_keV, side="right"))
    r_cut = float(np.interp(e_cut_keV, e_grid, rate))
    e_tail = np.concatenate(([e_cut_keV], e_grid[idx:]))
    r_tail = np.concatenate(([r_cut], rate[idx:]))
    return float(_trapz(r_tail, e_tail))


def a_self_direct(e_cut_keV: float) -> float:
    """Direct muon self-veto acceptance of the wafer at threshold ``E_cut`` [keV].

    DEFINITION (08-RESEARCH §F4):

        A_self_direct(E_cut) = int_{E_cut}^{inf} (dR/dE_dep) dE
                             / int_{0}^{inf}     (dR/dE_dep) dE

    = the fraction of muons **that cross the wafer** whose own deposit in the
    wafer lands above ``E_cut``, i.e. the fraction the wafer can self-tag. Its
    complement ``1 - A_self_direct`` is the un-self-taggable crossing fraction.

    Dimensionless: a ratio of two integrals with identical units. The
    counts/kg/day -> Hz conversion is deliberately absent here -- it would cancel.

    RATIO-INSENSITIVITY TO THE ATTENUATION FACTOR. Because this is a ratio of
    two integrals of the *same* spectrum, an overall normalization factor
    (including the 1.41 omnidirectional attenuation at 2.92 m w.e.) cancels
    exactly. ``a_self_direct`` therefore does NOT inherit the first-order caveat
    that ``f_dead`` carries. What does not cancel is the *shape* change from the
    angular distribution hardening with depth, which alters the chord
    distribution; Phase 15 owns that re-fold.

    TABLE FLOOR. The frozen grid starts at 1.014497e-02 keV (10.14 eV), so an
    ``E_cut`` of 10 eV sits at the edge of support. For ``E_cut`` at or below the
    floor this returns exactly 1.0 -- the artifact carries no mass below the
    floor to lose -- and that is stated rather than extrapolated. Above the
    tabulated ceiling it returns 0.0.

    NOT DERIVED FROM ANY NUCLEUS NUMBER. The numerator and denominator are both
    integrals of the wafer's own frozen chord (x) Landau-Vavilov distribution.
    """
    e_cut = float(e_cut_keV)
    if e_cut < 0.0:
        raise ValueError(f"E_cut must be non-negative, got {e_cut}")
    e_grid, _ = frozen_spectrum()
    if e_cut <= e_grid[0]:
        return 1.0
    if e_cut >= e_grid[-1]:
        return 0.0
    denom = float(_trapz(frozen_spectrum()[1], e_grid))
    return _tail_integral(e_cut) / denom


# --------------------------------------------------------------------------- #
# Multiplicity: the counting identity                                          #
# --------------------------------------------------------------------------- #
def mult_rejection(n_channels: int, p_hit: float = P_HIT_ILLUSTRATIVE) -> float:
    """Rejection power of NUCLEUS's single-target-hit requirement with N channels.

    DEFINITION (08-RESEARCH §F3):

        eps_mult(N) = 1 - P(exactly one of N target channels above threshold)

    NUCLEUS's selection is a conjunction. Quoted verbatim from
    ``08-01-SOURCE-EVIDENCE.md`` §B.2 (arXiv:2509.03559v1 §5.1):

        "Finally, the identification of a CEnuNS-like event must meet the
        combination of all possible anti-coincidence selection criteria, i.e.
        having (i) no hits in any of the veto detectors and (ii) a hit in one
        and only one of the target detectors."

    THE N = 1 IDENTITY -- exactly zero, by counting, not by estimate.
        A monolithic single-readout wafer has N = 1. With one and only one
        channel available to hit, conjunct (ii) -- "a hit in one and only one of
        the target detectors" -- is satisfied *identically* by every event that
        triggers at all. P(exactly one) == 1, so eps_mult == 0 exactly. The cut
        removes nothing. This is returned by an early return of literal ``0.0``,
        so the value is an identity and not the output of a probability model
        that happens to land near zero. Softening this to "small" or "marginal",
        or absorbing it into a lumped rejection factor, is
        ``fp-multiplicity-softening``.

    THE N > 1 BRANCH IS ILLUSTRATIVE AND MODEL-DEPENDENT.
        OCCUPANCY MODEL, named explicitly: *independent per-channel firing with
        common probability ``p_hit``, conditioned on at least one channel
        firing* (binomial, conditional on a trigger). Then

            P(exactly one | >= 1) = N p (1-p)^(N-1) / (1 - (1-p)^N)
            eps_mult(N)           = 1 - that

        ``p_hit`` is an ARBITRARY illustrative occupancy. It is not derived, not
        measured, and not a NUCLEUS number. Consequently **no numeric value from
        this branch is written into** ``data/wafer_self_veto.csv``: a bare number
        sitting next to the wafer's own quantities would read as a
        NUCLEUS-derived rejection efficiency, which it emphatically is not. The
        unit-tested *contrast* -- ``mult_rejection(1) == 0.0`` exactly versus
        ``mult_rejection(18) > 0`` -- is the point; the specific N = 18 value is
        not, and it may not be used as an efficiency anywhere.

        Consistency cross-check: the model formula itself returns 0 at N = 1 for
        *any* ``p_hit`` in (0, 1], since N p (1-p)^0 / (1 - (1-p)) = p/p = 1.
        The identity therefore does not depend on the occupancy model at all --
        the early return is a statement about counting, and the model agrees
        with it rather than establishing it.

    NUCLEUS'S OWN ASSESSMENT -- the counterpoint, quoted verbatim from
    ``08-01-SOURCE-EVIDENCE.md`` §B.7 (arXiv:2509.03559v1 §5.2.1):

        "Finally, the benefit of applying all vetoes, i.e. (i) using the IV and
        (ii) requesting only one cryogenic detector hit in addition to the MV
        and COV anti-coincidence selection criteria, is very marginal."

        Stated plainly: **the wafer's zero multiplicity handle costs little in
        absolute background terms**, because the handle NUCLEUS gains from that
        cut is itself very marginal. This cuts *against* this project's framing
        -- it weakens the "we lose their multiplicity cut" argument -- and it is
        recorded here for that reason, not despite it. Both statements stand
        together without softening either: the rejection is exactly zero, and
        the consequence is small.

    Args:
        n_channels: number of independently read-out target channels, N >= 1.
        p_hit: illustrative per-channel occupancy for the N > 1 branch only.

    Returns:
        eps_mult, dimensionless in [0, 1). Exactly 0.0 when ``n_channels == 1``.
    """
    n = int(n_channels)
    if n < 1:
        raise ValueError(f"n_channels must be >= 1, got {n_channels}")
    if n == 1:
        # Counting identity: one and only one channel to hit -> requirement is
        # satisfied identically -> the cut rejects nothing. Not an estimate.
        return 0.0
    p = float(p_hit)
    if not 0.0 < p <= 1.0:
        raise ValueError(f"p_hit must lie in (0, 1], got {p_hit}")
    q = 1.0 - p
    p_exactly_one = n * p * q ** (n - 1) / (1.0 - q**n)
    return 1.0 - p_exactly_one


# --------------------------------------------------------------------------- #
# Live-time cost of muon-coincident self-vetoing                               #
# --------------------------------------------------------------------------- #
def r_mu_underground_Hz() -> float:
    """Muon rate through the wafer at the NUCLEUS Chooz VNS [Hz].

        R_mu(2.92 m w.e.) = R_mu(surface) / 1.41 = 1.3659 Hz / 1.41 ~= 0.969 Hz

    The surface rate is the frozen artifact's own header value (parsed, not
    typed). The divisor is the omnidirectional muon attenuation factor.

    CARRIED-ANCHOR VERIFICATION VERDICT (Plan 08-01):
        **verified verbatim, arXiv:2509.03559v1 Sect. 4.1**
        -- ``08-01-SOURCE-EVIDENCE.md`` §E.1.1 (overburden 2.92 +/- 0.01 m w.e.)
           and §E.1.2 (attenuation factor 1.41 +/- 0.02).
        Neither anchor is used anywhere without this status attached.

        Nuance carried forward from §E.1.2: §4.1 states TWO overburden values --
        the *simulated* map average 2.92 +/- 0.01 m w.e. and the *measured*
        cosmic-wheel value 2.9 +/- 0.1 m w.e., the latter being the one the
        1.41 +/- 0.02 factor is stated to correspond to. Consistent, but not the
        same measurement.

        A further provenance limitation recorded by Plan 08-01 §E.2: the
        Table 4 normalization uncertainties are verified against arXiv v1 only,
        because Springer serves the published table body behind a "Full size
        table" link. Those values are NOT used in this module.
    """
    return frozen_header_rate_Hz() / MU_ATTENUATION_VNS


def f_dead(tau_dead_s: float) -> float:
    """Live-time fraction lost to muon-coincident self-vetoing. Dimensionless.

        f_dead = R_mu(2.92 m w.e.) x tau_dead      [Hz] x [s] = dimensionless

    Evaluated at the two locked resolving times of ``GPD/CONVENTIONS.md`` §F:
    ``TAU_DEAD_RESOLVE_S`` = 40 us (25 kHz Nyquist resolving time) and
    ``TAU_DEAD_SAMPLE_S`` = 20 us (50 kHz sampling interval). Both are reported;
    neither is presented alone. Censoring is non-paralyzable (locked
    2026-07-21), and at R_mu tau_dead ~ 1e-5 the paralyzable and non-paralyzable
    forms are numerically indistinguishable, so the choice is not load-bearing
    here.

    THIS IS A FIRST-ORDER **LOWER BOUND**, not a definitive live-time loss.
    Two independent reasons, both stated:

      1. *The attenuation factor is an integral-flux factor.* 1.41 rescales the
         total flux at 2.92 m w.e., but the angular distribution also hardens
         with depth, which changes the chord distribution and therefore the
         deposit spectrum shape. Phase 15 owns the proper angular re-fold. Note
         that ``a_self_direct`` is a RATIO in which this normalization cancels
         to first order, so it does NOT inherit this caveat -- ``f_dead`` does,
         because it is not a ratio.

      2. *The resolving time is not a veto window.* CONVENTIONS §F supplies a
         single-event resolving time. An MeV-scale muon deposit (MPV 1.2323 MeV,
         four to eight orders of magnitude above the trigger threshold)
         saturates the readout, so the true post-muon veto window is plausibly
         considerably longer than 40 us. No muon-specific saturation study
         exists to fix it, so the locked resolving time is used as a lower bound
         rather than a guess being dressed up as a measurement.

    CARRIED-ANCHOR VERIFICATION VERDICT (Plan 08-01), reproduced here and in the
    ``R_mu`` row of ``data/wafer_self_veto.csv``:
        **verified verbatim, arXiv:2509.03559v1 Sect. 4.1**
        (``08-01-SOURCE-EVIDENCE.md`` §E.1.1 overburden 2.92 +/- 0.01 m w.e.;
         §E.1.2 attenuation 1.41 +/- 0.02).
    """
    tau = float(tau_dead_s)
    if tau < 0.0:
        raise ValueError(f"tau_dead must be non-negative, got {tau_dead_s}")
    return r_mu_underground_Hz() * tau


# --------------------------------------------------------------------------- #
# Data table emission                                                          #
# --------------------------------------------------------------------------- #
#: Thresholds reported in the data table [keV]: 10 eV, 1 keV, 100 keV.
E_CUTS_KEV = (0.010, 1.0, 100.0)

_SRC_FROZEN = (
    "derived: data/muon_dRdEdep.csv (frozen v1.0 Phase-4 artifact, "
    "Gaisser-Guan flux x ray-box chord x Landau-Vavilov deposit, 1e9 MC samples)"
)


def _header_lines() -> list[str]:
    closure = integral_rate_Hz()
    header_rate = frozen_header_rate_Hz()
    floor = table_floor_keV()
    return [
        "# The 110 g monolithic Ge wafer's OWN muon-rejection handles.",
        "# Phase 8 Plan 08-02 (ROADMAP Success Criteria 3 and 4). Generated by",
        "# src/qpd_potential/wafer_self_veto.py :: emit_table().",
        "#",
        "# NO NUCLEUS REJECTION PERCENTAGE IS APPLIED AS A VALUE IN THIS TABLE.",
        "# Every number below traces to either (a) the wafer's own frozen chord x",
        "# Landau-Vavilov deposit distribution data/muon_dRdEdep.csv, or (b) a",
        "# counting identity about a single-readout target. Nothing traces to a",
        "# NUCLEUS efficiency (guards fp-veto-credit-transfer).",
        "#",
        "# THE TWO ACCEPTANCES ARE SEPARATE ROWS AND ARE NEVER MERGED. There is no",
        "# row and no column here that merges A_self_direct (~1, muons that cross",
        "# the wafer) with A_self_induced (0, secondaries born in the surrounding",
        "# Pb whose parent muon never enters the wafer). Merging them would mask",
        "# the zero behind the near-unity number (fp-lumped-acceptance).",
        "#",
        "# COUNTERPOINT AGAINST THIS PROJECT'S OWN FRAMING -- recorded, not buried.",
        "# NUCLEUS themselves, arXiv:2509.03559v1 Sect. 5.2.1, verbatim via",
        "# 08-01-SOURCE-EVIDENCE.md B.7:",
        '#   "Finally, the benefit of applying all vetoes, i.e. (i) using the IV',
        "#    and (ii) requesting only one cryogenic detector hit in addition to",
        "#    the MV and COV anti-coincidence selection criteria, is very",
        '#    marginal."',
        "# Because the handle NUCLEUS gains from that cut is itself very marginal,",
        "# the ABSOLUTE background cost of the wafer's identically-zero",
        "# multiplicity handle is SMALL. That weakens this project's 'we lose",
        "# their multiplicity cut' argument and is reported for that reason. The",
        "# zero is not softened either: it is exactly zero, and small in effect.",
        "#",
        "# NO N = 18 MULTIPLICITY VALUE APPEARS IN THIS TABLE, BY DECISION. Its",
        "# value depends entirely on an occupancy model this phase does not",
        "# derive, and a bare number here would read as a NUCLEUS-derived",
        "# efficiency. The mult_rejection(1) == 0.0 vs mult_rejection(18) > 0",
        "# contrast lives in tests/test_wafer_self_veto.py only.",
        "#",
        "# UNCREDITED FUTURE HANDLE: the wafer's ~10,300 QPD sensors at 1/mm^2",
        "# (CONVENTIONS D) give a spatial position-reconstruction observable that",
        "# NUCLEUS's inter-crystal multiplicity cut does not have. Different",
        "# observable, no established efficiency, NOT CREDITED ANYWHERE IN v2.0,",
        "# and it may not be used to fill the multiplicity gap.",
        "#",
        "# ENERGY SCALE: unified phonon E_dep, no ionization quenching",
        "# (CONVENTIONS B). GEOMETRY / MASS: CONVENTIONS D via wafer_geometry.py",
        f"# (m_wafer = {M_WAFER_KG:.4f} kg). RESOLVING TIMES: CONVENTIONS F,",
        "# 40 us (25 kHz Nyquist) and 20 us (50 kHz sampling), non-paralyzable.",
        "#",
        "# NORMALIZATION CLOSURE (acceptance denominator, test V6):",
        f"#   trapezoid over the native log grid x {M_WAFER_KG:.4f} kg / 86400 s"
        f" = {closure:.6f} Hz",
        f"#   frozen header integral_muon_rate_Hz = {header_rate:.4f} Hz"
        f"   -> deviation {100.0 * (closure / header_rate - 1.0):+.4f}% (PASS, <1%)",
        f"# TABLE FLOOR: {floor:.6e} keV = {1000.0 * floor:.2f} eV. The 10 eV",
        "# threshold sits AT the floor; the acceptance there is 1 by construction",
        "# and is not extrapolated below the artifact's support.",
        "#",
        "# PATHS: inputs are data/muon_dRdEdep.csv and",
        "# src/qpd_potential/muon_deposit.py. The 04-01-SUMMARY.md front-matter",
        "# paths data/muon/muon_dep_spectrum.csv and src/muon/deposited_spectrum.py",
        "# DO NOT EXIST and are not used.",
    ]


def build_rows() -> list[dict[str, str]]:
    """Assemble the data-table rows. Each carries its own source and caveat."""
    floor = table_floor_keV()
    rows: list[dict[str, str]] = []

    for e_cut in E_CUTS_KEV:
        acc = a_self_direct(e_cut)
        label = f"{1000.0 * e_cut:.0f}eV" if e_cut < 1.0 else f"{e_cut:.0f}keV"
        if e_cut <= floor:
            caveat = (
                f"AT THE TABLE FLOOR: the frozen grid starts at {floor:.6e} keV "
                f"({1000.0 * floor:.2f} eV), so this threshold sits at the edge of "
                "support and the value is 1 by construction, NOT an extrapolation "
                "below the artifact. Ratio-insensitive to the 1.41 attenuation "
                "factor (normalization cancels); the depth-hardening SHAPE change "
                "is a Phase-15 re-fold, not covered here."
            )
        else:
            caveat = (
                "Muons that CROSS the wafer only. Says nothing about muon-induced "
                "secondaries -- see the A_self_induced row, which is never merged "
                "with this one. Expected ~1: vertical-chord Landau MPV is "
                "1.2323 MeV, four to eight orders of magnitude above this "
                "threshold. Ratio-insensitive to the 1.41 attenuation factor "
                "(normalization cancels); the depth-hardening SHAPE change is a "
                "Phase-15 re-fold, not covered here."
            )
        rows.append(
            {
                "quantity": f"A_self_direct_{label}",
                "value": f"{acc:.12f}",
                "units": "dimensionless",
                "definition": (
                    f"fraction of wafer-crossing muons whose own deposit exceeds "
                    f"E_cut = {e_cut:g} keV, = int_Ecut^inf (dR/dE_dep) dE / "
                    "int_0^inf (dR/dE_dep) dE"
                ),
                "source": _SRC_FROZEN,
                "caveat": caveat,
            }
        )

    rows.append(
        {
            "quantity": "A_self_induced",
            "value": f"{A_SELF_INDUCED:.1f}",
            "units": "dimensionless",
            "definition": (
                "fraction of muon-INDUCED secondaries (neutrons, bremsstrahlung "
                "gammas born in the surrounding Pb, parent muon nowhere near the "
                "wafer) that a single self-vetoing wafer can tag"
            ),
            "source": (
                "derived: counting/physical argument -- the wafer's only tagging "
                "handle is the parent muon's own deposit, which is absent for this "
                "class. NUCLEUS's MV+COV muon-INDUCED background rejection quoted "
                "in 08-01-SOURCE-EVIDENCE.md B.9 (arXiv:2509.03559v1 Sect. 5.2.1) "
                "is a rejection of induced secondaries, NOT a muon tagging "
                "efficiency, and is NOT applied here or anywhere in this project"
            ),
            "caveat": (
                "NEVER SUM OR AVERAGE THIS WITH A_self_direct. Zero is the "
                "defensible FLOOR, not an impossibility proof: a secondary "
                "accompanied into the wafer by its own parent muon would be "
                "tagged, and that configuration is argued negligible here rather "
                "than measured. A referee could argue the wafer's 103.23 cm^2 face "
                "makes such accidental coincidences non-negligible."
            ),
        }
    )

    rows.append(
        {
            "quantity": "eps_mult_N1",
            "value": f"{mult_rejection(1):.1f}",
            "units": "dimensionless",
            "definition": (
                "rejection power of NUCLEUS's single-target-hit requirement "
                "applied to a monolithic target with N = 1 readout channel, "
                "= 1 - P(exactly one of N channels above threshold)"
            ),
            "source": (
                "derived: counting identity. NUCLEUS Sect. 5.1 requires 'a hit in "
                "one and only one of the target detectors' (08-01-SOURCE-EVIDENCE"
                ".md B.2); with N = 1 that is satisfied identically, so P = 1 and "
                "the cut removes nothing"
            ),
            "caveat": (
                "EXACTLY ZERO, by counting -- not 'small', not 'marginal', not to "
                "be absorbed into a lumped rejection factor. Asserted by identity "
                "comparison in tests/test_wafer_self_veto.py. Counterpoint in the "
                "header: NUCLEUS call this cut's benefit 'very marginal', so the "
                "absolute cost of the missing handle is small. No N = 18 value "
                "appears in this table -- see header."
            ),
        }
    )

    rows.append(
        {
            "quantity": "R_mu_2.92mwe",
            "value": f"{r_mu_underground_Hz():.6f}",
            "units": "Hz",
            "definition": (
                "muon rate through the wafer at the NUCLEUS Chooz Very-Near-Site, "
                f"= {frozen_header_rate_Hz():.4f} Hz (frozen surface rate) / "
                f"{MU_ATTENUATION_VNS} (omnidirectional attenuation)"
            ),
            "source": (
                "derived: surface rate parsed from the data/muon_dRdEdep.csv "
                "header (frozen v1.0 Phase-4 artifact), divided by the "
                f"omnidirectional attenuation factor {MU_ATTENUATION_VNS} +/- 0.02 "
                f"at overburden {OVERBURDEN_MWE} +/- 0.01 m w.e. -- "
                f"Plan 08-01 verdict: {ANCHOR_VERDICT}"
            ),
            "caveat": (
                "First-order only: 1.41 is an INTEGRAL-FLUX factor while the "
                "angular distribution also hardens with depth, changing the chord "
                "distribution and hence the deposit-spectrum shape (Phase 15 owns "
                "the re-fold). Sect. 4.1 also states a second, MEASURED overburden "
                "2.9 +/- 0.1 m w.e. -- the one 1.41 is said to correspond to; "
                "consistent with 2.92 +/- 0.01 but not the same measurement. "
                "A_self_direct is a ratio and does NOT inherit this caveat."
            ),
        }
    )

    for tau, tag in ((TAU_DEAD_RESOLVE_S, "40us"), (TAU_DEAD_SAMPLE_S, "20us")):
        rows.append(
            {
                "quantity": f"f_dead_tau{tag}",
                "value": f"{f_dead(tau):.6e}",
                "units": "dimensionless",
                "definition": (
                    f"live-time fraction lost to muon-coincident self-vetoing, "
                    f"= R_mu(2.92 m w.e.) x tau_dead with tau_dead = {tau:.0e} s"
                ),
                "source": (
                    f"derived: R_mu row above x CONVENTIONS.md Sect. F resolving "
                    f"time {tag} "
                    f"({'25 kHz Nyquist' if tag == '40us' else '50 kHz sampling'}, "
                    f"non-paralyzable censoring locked 2026-07-21). Attenuation "
                    f"anchor status: {ANCHOR_VERDICT}"
                ),
                "caveat": (
                    "FIRST-ORDER LOWER BOUND, not a definitive live-time loss. "
                    "(1) 1.41 is an integral-flux factor while the angular "
                    "distribution hardens with depth (Phase 15 re-fold). (2) "
                    "CONVENTIONS F supplies a single-event RESOLVING TIME, not a "
                    "muon veto window; an MeV-scale deposit (MPV 1.2323 MeV) "
                    "saturates the readout so the true window is plausibly longer. "
                    "No muon-specific saturation study exists to fix it."
                ),
            }
        )

    return rows


_COLUMNS = ("quantity", "value", "units", "definition", "source", "caveat")


def emit_table(path: str | Path = SELF_VETO_CSV) -> Path:
    """Write the provenance-headed ``data/wafer_self_veto.csv``."""
    path = Path(path)
    with open(path, "w", newline="") as fh:
        for line in _header_lines():
            fh.write(line + "\n")
        writer = csv.DictWriter(fh, fieldnames=list(_COLUMNS))
        writer.writeheader()
        for row in build_rows():
            writer.writerow(row)
    return path


def main() -> None:
    closure = integral_rate_Hz()
    header_rate = frozen_header_rate_Hz()
    print(f"denominator closure : {closure:.6f} Hz vs header {header_rate:.4f} Hz "
          f"({100.0 * (closure / header_rate - 1.0):+.4f}%)")
    print(f"table floor         : {table_floor_keV():.6e} keV")
    for e_cut in E_CUTS_KEV:
        print(f"a_self_direct({e_cut:g} keV) = {a_self_direct(e_cut):.12f}")
    print(f"A_SELF_INDUCED      : {A_SELF_INDUCED}")
    print(f"mult_rejection(1)   : {mult_rejection(1)!r}")
    print(f"R_mu(2.92 m w.e.)   : {r_mu_underground_Hz():.6f} Hz")
    for tau in (TAU_DEAD_RESOLVE_S, TAU_DEAD_SAMPLE_S):
        print(f"f_dead({tau:.0e} s)    : {f_dead(tau):.6e}")
    out = emit_table()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
