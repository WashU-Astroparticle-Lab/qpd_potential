# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
#
# Phase-15 Plan 15-01: the ELECTRON-RECOIL channel module.
#
# It carries three things, and nothing else:
#   1. the machine-readable per-channel verdict on whether the Phase-11
#      NUCLEAR-recoil impulse-approximation width sigma_E = sqrt(E_R omega_bar)
#      applies to the muon-ionization and Compton channels, plus a guard that
#      RAISES (never warns, never clamps) when a caller contradicts it;
#   2. the low-energy validity floor of the v1.0 Landau-Vavilov muon deposit
#      model, computed on the COMMITTED muon_deposit code path;
#   3. the Compton-channel S(x, Z=32) suppression read from the COMMITTED
#      Hubbell table, kept explicitly separate from the physical floor set by
#      electron-hole pair creation in germanium.
#
# ENERGY SCALE: unified phonon E_dep scale, NO quenching, NO keVee/keVnr mixing
# (CONVENTIONS Section B).  "Electron recoil" here names the INTERACTION -- which
# particle absorbs the momentum transfer -- and never licenses a keVee axis.
#
# WHAT THIS MODULE DELIBERATELY DOES NOT DO.  It never applies a broadening.  It
# never multiplies a rate by exp(-2W) (milestone-wide prohibition, CONVENTIONS
# Section J).  It never cites sigma_E/E_R = 1/sqrt(2W) or 2W = E_R/omega_bar as
# evidence for anything: CONVENTIONS Section J records both as algebraic
# identities true by construction for ANY omega_bar, and treating an identity as
# corroboration is `fp-identity-as-corroboration`.

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np

from . import compton_source as cs
from . import muon_deposit as md
from . import params

__all__ = [
    "IA_VERDICT_VOCABULARY",
    "ELECTRON_RECOIL_CHANNELS",
    "IA_APPLICABILITY",
    "IAVerdict",
    "ElectronRecoilBroadeningError",
    "ia_verdict",
    "assert_nuclear_kernel_use",
    "REFERENCE_E_MU_GEV",
    "GE_LATTICE_CONSTANT_ANGSTROM",
    "I_GE_eV",
    "I_GE_PROVENANCE",
    "reference_beta_gamma",
    "xi_coefficient_MeV_per_cm",
    "xi_eV_of_chord_cm",
    "deposit_eV_of_chord_cm",
    "chord_cm_of_deposit_eV",
    "landau_validity_floor",
    "indicted_v1_bins",
    "compton_x_of_recoil_inv_angstrom",
    "compton_S_suppression",
    "GE_BAND_GAP_T0_eV",
    "GE_BAND_GAP_300K_eV",
    "GE_FREE_EXCITON_BINDING_eV",
    "compton_physical_floor",
    "electron_ia_scale_eV",
    "electron_side_sigma_T_eV",
    "electron_side_summary",
    "validity_floor_rows",
]


# =========================================================================== #
# 1. THE APPLICABILITY VERDICT                                                #
# =========================================================================== #

#: Closed vocabulary.  A verdict outside it is an error, and the ABSENCE of a
#: verdict is not a default to "does_not_apply" -- ROADMAP Phase 15 SC3 names
#: "proceeding without deciding" as the one unacceptable outcome.
IA_VERDICT_VOCABULARY = (
    "applies_as_derived_for_electron_recoil",
    "does_not_apply",
    "undecidable",
)

ELECTRON_RECOIL_CHANNELS = ("muon", "compton")


class ElectronRecoilBroadeningError(ValueError):
    """Raised when an electron-recoil channel is fed the NUCLEAR IA kernel.

    Modelled on ``fold.DoubleBroadeningError``: it RAISES.  A guard that warns,
    clamps, or returns a flag is a guard that a later caller routinely works
    around, and ROADMAP Phase 15 SC3 exists precisely so that transplanting the
    nuclear width onto an electron recoil cannot happen by accident.
    """


@dataclass(frozen=True)
class IAVerdict:
    """One channel's determination, inseparable from its reason."""

    channel: str
    verdict: str
    recoiling_body: str
    initial_state_momentum_distribution: str
    reason: str
    consequence_for_spectra: str
    falsifier: str

    def __post_init__(self) -> None:
        if self.verdict not in IA_VERDICT_VOCABULARY:
            raise ValueError(
                f"{self.channel}: verdict {self.verdict!r} is outside the closed "
                f"vocabulary {IA_VERDICT_VOCABULARY}")
        for field in ("recoiling_body", "initial_state_momentum_distribution",
                      "reason", "consequence_for_spectra", "falsifier"):
            if not str(getattr(self, field)).strip():
                raise ValueError(f"{self.channel}: empty {field}")

    @property
    def nuclear_kernel_applies(self) -> bool:
        return self.verdict == "applies_as_derived_for_electron_recoil"


_MUON_VERDICT = IAVerdict(
    channel="muon",
    verdict="does_not_apply",
    recoiling_body=(
        "An ATOMIC ELECTRON of the germanium target, in each individual "
        "ionizing collision along the muon's chord. No germanium nucleus recoils "
        "in the process that produces the deposit; the nucleus participates only "
        "as the static binding potential that fixes the oscillator strengths "
        "entering the mean excitation energy I."),
    initial_state_momentum_distribution=(
        "The bound-electron momentum distribution of the struck shell. In the "
        "muon channel it is not an independent input at all: it is already "
        "folded into the Bethe stopping-power cross section through I = 350 eV "
        "and the Sternheimer density-effect coefficients, and the resulting "
        "collision-by-collision fluctuation of the total loss IS the "
        "Landau-Vavilov straggling density the chain already samples "
        "(muon_deposit.sample_deposit)."),
    reason=(
        "omega_bar = 17.8597 meV is set by the germanium NUCLEUS's zero-point "
        "momentum: sigma_p^2 = m_N omega_bar / 2 for the nuclear oscillator "
        "(Phase 11, 11-02). Nothing in this channel recoils with that momentum "
        "distribution, so the width has no physical source here. Two independent "
        "objections, either of which is sufficient. (a) SCALE. The electron-side "
        "IA scale is omega_bar_e = 2 sigma_pz^2 / m_e, and even its rigorous "
        "lower bound from the uncertainty principle over the Ge covalent bond "
        "(a*sqrt(3)/4 = 2.44999 angstrom) is 0.6347 eV -- 35.5x the nuclear "
        "omega_bar, i.e. the nuclear kernel would understate the electron-side "
        "width by at least 5.96x even where the electron-side formalism is "
        "valid. (b) DOUBLE COUNTING. The Landau-Vavilov density is ALREADY the "
        "fluctuation of this deposit. Convolving an additional IA Gaussian onto "
        "it would broaden a distribution whose spread the chain has already "
        "computed, on top of a straggling width xi that at the vertical chord is "
        "0.072069 MeV -- six orders of magnitude above any candidate IA width."),
    consequence_for_spectra=(
        "Plan 15-02 emits the muon deposit table UNBROADENED and declares "
        "broadened_provenance = false. Plan 15-03 folds it with broaden=False. "
        "No leakage budget arises for this channel, so "
        "residual_retained_plus_leaked and residual_retained_only COINCIDE and "
        "must be reported as one statement, not as two independent "
        "confirmations. No 100 meV kernel-leakage fraction applies here."),
    falsifier=(
        "A measured or first-principles sub-keV muon energy-loss distribution in "
        "germanium whose width exceeds the Landau-Vavilov prediction by a margin "
        "that scales as sqrt(E_dep) with a coefficient consistent with "
        "sqrt(omega_bar) = 0.1336 eV^(1/2), i.e. an unexplained residual "
        "broadening of 42.3% at 100 meV and 4.20% at 10.14 eV. Equivalently: a "
        "demonstration that the Ge nucleus takes up a resolvable share of the "
        "momentum transfer in muon ionization, which would make the nuclear "
        "zero-point distribution an input to the deposit after all."),
)

_COMPTON_VERDICT = IAVerdict(
    channel="compton",
    verdict="does_not_apply",
    recoiling_body=(
        "A BOUND ATOMIC ELECTRON of germanium, struck by the environmental "
        "gamma. The deposit is the electron kinetic energy T_e = E_gamma - E' "
        "(compton_deposit.sample_electron_recoil); the germanium nucleus takes "
        "up no part of the momentum transfer in the incoherent channel -- that "
        "is precisely what distinguishes incoherent from coherent/Rayleigh "
        "scattering, and the coherent channel is out of scope."),
    initial_state_momentum_distribution=(
        "The COMPTON PROFILE J(p_z) of the germanium electrons -- the projection "
        "of the bound-electron momentum density onto the scattering vector. This "
        "is the exact electron-side analogue of the nuclear zero-point "
        "distribution, and it is a real, nonzero, physically present "
        "distribution. It is NOT dismissed here; it is evaluated below and in "
        "15-01-BROADENING-APPLICABILITY.md."),
    reason=(
        "The same impulse-approximation decomposition that Phase 11 applied to "
        "the nucleus applies verbatim to the electron: T = q^2/(2m) + p.q/m, so "
        "the width is sigma_T = q sigma_pz / m = sqrt(T * omega_bar_e) with "
        "omega_bar_e = 2 sigma_pz^2 / m_e. Identical FORM, different BODY, and "
        "therefore a different scale. omega_bar_e for germanium electrons lies "
        "between 0.6347 eV (rigorous uncertainty-principle lower bound over the "
        "Ge covalent bond) and 16.8 eV (valence virial estimate), with a "
        "core-inclusive whole-atom envelope near 2.35 keV. The nuclear "
        "omega_bar = 17.8597 meV is smaller than the LOWEST of these by 35.5x, "
        "so transplanting it would understate the electron-side width by at "
        "least 5.96x and by up to 363x -- it is not merely the wrong "
        "justification for the right number, it is the wrong number. Separately "
        "and decisively, the electron-side IA is itself INVALID in the sub-eV "
        "region: the Campbell-Deem criterion used in Phase 11 is 2W >> 1, and "
        "its electron analogue 2W_e = T / omega_bar_e is 0.157 at the 0.0999350 "
        "eV extended floor under the most favourable bound and 4.2e-5 under the "
        "core-inclusive envelope. Below its own validity threshold the transfer "
        "cannot be described as a free recoil at all."),
    consequence_for_spectra=(
        "Plan 15-02 emits the Compton deposit table UNBROADENED and declares "
        "broadened_provenance = false. Plan 15-03 folds it with broaden=False, "
        "and the two counts residuals coincide as for the muon channel. BUT this "
        "is NOT the statement that the deposit axis carries no broadening: the "
        "Compton-profile Doppler width is real and is NEGLECTED by the v1.0 "
        "chain, which samples T_e from FREE kinematics at the sampled angle and "
        "uses S(x,Z) only as a cross-section normalization. That width is 252% "
        "of the deposit at 100 meV under the lower bound -- 86 extended-grid "
        "bins -- so it is emphatically not unresolvable. It is not applied here "
        "because it is outside its own validity domain exactly where it would "
        "matter, and because modelling it would be a NEW mechanism, which SC1 "
        "excludes. It is handed to Phase 16 as a NAMED GAP and it reinforces the "
        "Compton physical floor rather than competing with it."),
    falsifier=(
        "A germanium Compton-profile measurement or calculation giving a "
        "projected-momentum spread sigma_pz small enough that omega_bar_e falls "
        "to or below the nuclear omega_bar = 17.8597 meV -- i.e. sigma_pz <= "
        "0.0181 atomic units, an electron delocalized over more than 27.6 "
        "angstrom, five Ge lattice constants. Alternatively: a demonstration "
        "that the germanium nucleus recoils coherently with the struck electron "
        "in the incoherent channel, which would reinstate m_N as the relevant "
        "mass. Either would overturn this verdict."),
)

#: The recorded per-channel determination.  Public, so a reader can enumerate
#: the verdicts without calling anything.
IA_APPLICABILITY = {"muon": _MUON_VERDICT, "compton": _COMPTON_VERDICT}


def ia_verdict(channel: str) -> IAVerdict:
    """The recorded per-channel applicability verdict.

    There is no accessor returning a bare boolean: a consumer cannot obtain the
    decision without also receiving the reason and the consequence.
    """
    if channel not in IA_APPLICABILITY:
        raise KeyError(
            f"{channel!r} is not an electron-recoil channel; expected one of "
            f"{ELECTRON_RECOIL_CHANNELS}")
    return IA_APPLICABILITY[channel]


def assert_nuclear_kernel_use(channel: str, apply_nuclear_kernel: bool) -> IAVerdict:
    """Guard.  RAISES if the request contradicts the recorded verdict.

    ``apply_nuclear_kernel=True`` means "convolve sigma_E = sqrt(E_R omega_bar),
    the Phase-11 NUCLEAR-recoil width, onto this channel".  Returns the verdict
    when the request is consistent with it, so a caller that passes the guard has
    necessarily also read the reason.
    """
    v = ia_verdict(channel)
    if v.verdict == "undecidable":
        raise ElectronRecoilBroadeningError(
            f"channel {channel!r} carries verdict 'undecidable'. The ROADMAP "
            "Phase-15 backtracking trigger requires blocking and requesting "
            "scope repair, not defaulting in either direction.")
    if bool(apply_nuclear_kernel) != v.nuclear_kernel_applies:
        raise ElectronRecoilBroadeningError(
            f"channel {channel!r}: apply_nuclear_kernel="
            f"{bool(apply_nuclear_kernel)} contradicts the Plan 15-01 verdict "
            f"{v.verdict!r}.\n  RECOILING BODY: {v.recoiling_body}\n"
            f"  REASON: {v.reason}\n"
            f"  CONSEQUENCE FOR SPECTRA: {v.consequence_for_spectra}\n"
            "omega_bar = 17.8597 meV is set by the germanium NUCLEUS's zero-point "
            "momentum (CONVENTIONS Section J); applying it where no nucleus "
            "recoils fabricates a smearing with no physical source "
            "(fp-transplant-nuclear-width).")
    return v


# =========================================================================== #
# 2. THE MUON CHANNEL'S LANDAU-VAVILOV VALIDITY FLOOR                          #
# =========================================================================== #

#: The reference muon total energy at which Plan 09-01 Section 2.3 quoted the
#: vertical-chord scalars (xi = 0.072069 MeV, Delta_p = 1.230614 MeV,
#: kappa = 6.727e-05).  Named here so the floor is computed at the SAME point the
#: verified v1.0 scalars were verified at.
REFERENCE_E_MU_GEV: float = 4.0

#: Germanium lattice constant [angstrom].  Diamond structure, so the covalent
#: bond length is a*sqrt(3)/4.
GE_LATTICE_CONSTANT_ANGSTROM: float = 5.658

#: Germanium mean excitation energy [eV].  NOT re-typed: read from the committed
#: muon_deposit chain, where it is the I that already sets every Delta_p the v1.0
#: manuscript published.  Converting here rather than restating keeps one value.
I_GE_eV: float = md.I_GE * 1.0e6

I_GE_PROVENANCE: str = (
    "src/qpd_potential/muon_deposit.py::I_GE = 350.0e-6 MeV, the germanium mean "
    "excitation energy already in use by the committed Landau-Vavilov chain "
    "(PDG 'Atomic and Nuclear Properties of Materials' table for Ge, I = 350.0 "
    "eV). Read from the code, not re-typed. The external PDG value is "
    "[UNVERIFIED - not re-fetched in this phase]; what IS verified is that this "
    "is the same I that produced every v1.0 Delta_p."
)

#: The published criterion.  A continuous energy-loss density presupposes many
#: collisions; the Landau-Vavilov straggling function ceases to be the correct
#: distribution when the width parameter xi falls to the scale of the mean
#: excitation energy I, because the loss is then dominated by a small number of
#: discrete single collisions (PDG, "Passage of Particles Through Matter",
#: energy loss in thin absorbers; Bichsel, Rev. Mod. Phys. 60, 663 (1988)).
#: The committed chain already guards the OTHER end via kappa = xi/T_max.
LANDAU_CRITERION: str = "xi <= I (Landau-Vavilov continuous straggling requires xi >> I)"
LANDAU_CRITERION_RATIO: float = 1.0


def reference_beta_gamma(e_mu_gev: float = REFERENCE_E_MU_GEV) -> float:
    """beta*gamma of the reference muon, from the committed kinematics."""
    return float(md.beta_gamma(e_mu_gev))


def xi_coefficient_MeV_per_cm(e_mu_gev: float = REFERENCE_E_MU_GEV) -> float:
    """xi / ell [MeV/cm] on the committed ``muon_deposit.xi_width`` path."""
    bg = reference_beta_gamma(e_mu_gev)
    beta2 = bg * bg / (bg * bg + 1.0)
    return float(md.xi_width(md.RHO * 1.0, beta2))


def xi_eV_of_chord_cm(ell_cm, e_mu_gev: float = REFERENCE_E_MU_GEV):
    """Landau width xi [eV] for a chord ``ell_cm`` [cm]."""
    bg = reference_beta_gamma(e_mu_gev)
    beta2 = bg * bg / (bg * bg + 1.0)
    return np.asarray(md.xi_width(md.RHO * np.asarray(ell_cm, float), beta2)) * 1.0e6


def deposit_eV_of_chord_cm(ell_cm, e_mu_gev: float = REFERENCE_E_MU_GEV):
    """Most-probable deposit Delta_p [eV] for a chord ``ell_cm`` [cm].

    Straight through ``muon_deposit.mpv_deposit`` -- the committed code path, not
    a textbook restatement of it.
    """
    bg = reference_beta_gamma(e_mu_gev)
    dp, _ = md.mpv_deposit(md.RHO * np.asarray(ell_cm, float), bg)
    return np.asarray(dp) * 1.0e6


def chord_cm_of_deposit_eV(target_eV: float,
                           e_mu_gev: float = REFERENCE_E_MU_GEV) -> float:
    """Invert Delta_p(ell) on the committed path: the chord giving ``target_eV``.

    Bisection on log ell.  Delta_p(ell) is strictly increasing over the bracket,
    so the root is unique.
    """
    from scipy.optimize import brentq
    f = lambda lg: float(deposit_eV_of_chord_cm(10.0 ** lg, e_mu_gev)) - target_eV
    lo, hi = -12.0, -1.0
    if f(lo) > 0.0 or f(hi) < 0.0:
        raise ValueError(
            f"deposit {target_eV!r} eV is outside the bracketed chord range "
            f"[1e{lo:g}, 1e{hi:g}] cm on the committed mpv_deposit path")
    return float(10.0 ** brentq(f, lo, hi, xtol=1e-14, rtol=1e-15))


def chord_in_lattice_constants(ell_cm: float) -> float:
    """A chord expressed in germanium lattice constants (a = 5.658 angstrom)."""
    return float(ell_cm * 1.0e8 / GE_LATTICE_CONSTANT_ANGSTROM)


def landau_validity_floor(e_mu_gev: float = REFERENCE_E_MU_GEV,
                          ratio: float = LANDAU_CRITERION_RATIO,
                          I_eV: Optional[float] = None) -> dict:
    """The deposit energy at which xi crosses ``ratio * I``.

    Returns the crossing chord, the crossing xi, the floor in eV, and the
    diagnostics the frozen table carries.
    """
    I_use = I_GE_eV if I_eV is None else float(I_eV)
    coeff_eV_per_cm = xi_coefficient_MeV_per_cm(e_mu_gev) * 1.0e6
    ell_star = ratio * I_use / coeff_eV_per_cm
    return {
        "criterion": LANDAU_CRITERION,
        "criterion_ratio_xi_over_I": float(ratio),
        "I_eV": I_use,
        "I_provenance": I_GE_PROVENANCE,
        "reference_E_mu_GeV": float(e_mu_gev),
        "reference_beta_gamma": reference_beta_gamma(e_mu_gev),
        "xi_coefficient_MeV_per_cm": xi_coefficient_MeV_per_cm(e_mu_gev),
        "chord_cm": float(ell_star),
        "chord_um": float(ell_star * 1.0e4),
        "chord_lattice_constants": chord_in_lattice_constants(ell_star),
        "xi_at_crossing_eV": float(xi_eV_of_chord_cm(ell_star, e_mu_gev)),
        "floor_eV": float(deposit_eV_of_chord_cm(ell_star, e_mu_gev)),
    }


def _mpv_deposit_with_I(x_gcm2, bg, I_MeV: float):
    """``muon_deposit.mpv_deposit`` with I exposed as a parameter.

    The committed ``mpv_deposit`` hard-wires ``I_GE``, so the floor's sensitivity
    to the adopted mean excitation energy cannot be measured on it directly.
    This is a faithful re-expression of the SAME PDG formula with I lifted out --
    and ``tests/test_em_recoil.py::test_mpv_with_I_reproduces_committed_path``
    asserts it reproduces ``muon_deposit.mpv_deposit`` to 1e-14 at ``I = I_GE``,
    so it cannot drift from the committed path without failing.
    """
    bg = np.asarray(bg, dtype=float)
    g2 = bg * bg + 1.0
    beta2 = (bg * bg) / g2
    xi = md.xi_width(x_gcm2, beta2)
    delta = md.density_effect(bg)
    dp = xi * (np.log(2.0 * md.M_E * bg * bg / I_MeV)
               + np.log(xi / I_MeV) + md.J_LANDAU - beta2 - delta)
    return dp, xi


def landau_floor_sensitivity_to_I(I_values_eV=(300.0, 322.0, 350.0, 400.0),
                                  e_mu_gev: float = REFERENCE_E_MU_GEV,
                                  ratio: float = LANDAU_CRITERION_RATIO) -> list[dict]:
    """Floor and indicted-bin count as I is varied CONSISTENTLY.

    I enters the criterion (xi = I) AND the Delta_p bracket, so both are varied
    together; changing only one would misstate the sensitivity.  This is a
    sensitivity report, not a licence to re-choose I: ``fp-floor-softened``
    forbids adopting whichever value makes the indicted count zero, and none of
    these does -- the count runs 203 to 214 over a +/-14% swing in I.
    """
    bg = reference_beta_gamma(e_mu_gev)
    coeff_eV_per_cm = xi_coefficient_MeV_per_cm(e_mu_gev) * 1.0e6
    out = []
    for I_eV in I_values_eV:
        ell = ratio * I_eV / coeff_eV_per_cm
        dp, xi = _mpv_deposit_with_I(md.RHO * ell, bg, I_eV * 1.0e-6)
        floor = float(dp) * 1.0e6
        out.append({
            "I_eV": float(I_eV),
            "chord_um": float(ell * 1.0e4),
            "xi_eV": float(xi) * 1.0e6,
            "floor_eV": floor,
            "n_v1_bins_below_floor": indicted_v1_bins(floor)["n_v1_bins_below_floor"],
            "is_committed_value": bool(abs(I_eV - I_GE_eV) < 1.0e-9),
        })
    return out


def indicted_v1_bins(floor_eV: float) -> dict:
    """How many of the 584 frozen v1.0 bins lie below ``floor_eV``.

    The disconfirming check of Plan 15-01.  The count is reported whatever it is;
    the criterion is never moved to make it zero (``fp-floor-softened``).
    """
    v1 = md.shared_energy_grid("v1.0")
    c1 = np.sqrt(v1[:-1] * v1[1:]) * 1.0e3          # eV
    ext = md.shared_energy_grid("v2.0-ext")
    ce = np.sqrt(ext[:-1] * ext[1:]) * 1.0e3        # eV
    n1 = int(np.sum(c1 < floor_eV))
    return {
        "floor_eV": float(floor_eV),
        "n_v1_bins_total": int(c1.size),
        "n_v1_bins_below_floor": n1,
        "frac_v1_bins_below_floor": float(n1) / float(c1.size),
        "highest_indicted_v1_centre_eV": float(c1[n1 - 1]) if n1 else float("nan"),
        "lowest_surviving_v1_centre_eV": float(c1[n1]) if n1 < c1.size else float("nan"),
        "n_ext_bins_total": int(ce.size),
        "n_ext_bins_below_floor": int(np.sum(ce < floor_eV)),
    }


# =========================================================================== #
# 3. THE COMPTON CHANNEL: S(x,Z) SUPPRESSION vs THE PHYSICAL FLOOR             #
# =========================================================================== #

def compton_x_of_recoil_inv_angstrom(T_e_eV, e_gamma_keV: Optional[float] = None):
    """Momentum-transfer variable x [1/angstrom] for an electron recoil T_e [eV].

    Exact Compton kinematics inverted at fixed line energy: with
    alpha = E_gamma/m_e c^2 and u = 1 - cos(theta),
    ``T_e = E_gamma alpha u / (1 + alpha u)`` gives
    ``u = T_e / (alpha (E_gamma - T_e))``, and
    ``x = E_gamma sin(theta/2) / 12.39842`` with ``sin(theta/2) = sqrt(u/2)``
    (``compton_source.momentum_transfer_x``).

    ``e_gamma_keV=None`` uses the small-transfer limit
    ``x -> sqrt(T_e m_e c^2) / (sqrt(2) hc)``, which is INDEPENDENT of the line
    energy -- as it must be, since x is a momentum transfer and at fixed recoil
    the transfer is fixed.  Cross-checked in the tests against 4 pi x a_0 =
    sqrt(2 m_e T_e) in atomic units, agreeing to 1.3e-8.
    """
    T = np.asarray(T_e_eV, float) * 1.0e-3          # keV
    if e_gamma_keV is None:
        return np.sqrt(T * cs.M_E_KEV) / (np.sqrt(2.0) * cs.HC_KEV_ANG)
    Eg = float(e_gamma_keV)
    a = Eg / cs.M_E_KEV
    u = T / (a * (Eg - T))
    return Eg * np.sqrt(u / 2.0) / cs.HC_KEV_ANG


def compton_S_suppression(T_e_eV, e_gamma_keV: Optional[float] = None) -> dict:
    """S(x, Z=32)/Z at an electron recoil energy, from the COMMITTED table.

    Reports the momentum transfer, the raw S, the suppression against free
    Klein-Nishina, and the margin against the tabulated x domain.  It reports a
    NUMBER; whether that number is a rate is ``compton_physical_floor``'s
    question, and the two are never merged (``fp-suppressed-means-valid``).
    """
    x = float(compton_x_of_recoil_inv_angstrom(T_e_eV, e_gamma_keV))
    S = float(cs.incoherent_S(x))
    return {
        "T_e_eV": float(T_e_eV),
        "x_inv_angstrom": x,
        "S_incoherent": S,
        "S_over_Z": S / cs.Z_GE,
        "suppression_vs_free_KN": cs.Z_GE / S,
        "table_x_lo": float(cs._SF_X[0]),
        "table_x_hi": float(cs._SF_X[-1]),
        "inside_table_domain": bool(cs._SF_X[0] <= x <= cs._SF_X[-1]),
        "margin_above_table_floor": x / float(cs._SF_X[0]),
    }


#: Germanium indirect band gap.  The detector sits at the T -> 0 evaluation point
#: of CONVENTIONS Section J, so the low-temperature value is the operative one.
#: [UNVERIFIED - training data]: not present in any repository artifact.
GE_BAND_GAP_T0_eV: float = 0.7437
GE_BAND_GAP_300K_eV: float = 0.661
#: Free-exciton binding energy in Ge; an electron-hole PAIR can be created
#: (as a bound exciton) marginally below the gap.  [UNVERIFIED - training data].
GE_FREE_EXCITON_BINDING_eV: float = 4.15e-3


def compton_physical_floor() -> dict:
    """The energy transfer below which no electron-hole pair can be created.

    ADOPTED: the germanium indirect band gap in the T -> 0 limit, 0.7437 eV,
    reduced by the free-exciton binding energy to 0.7396 eV for the lowest
    pair-creating transfer.  The 300 K gap 0.661 eV is recorded as the
    alternative; the choice is NAMED rather than assumed, and the conclusion of
    this plan does not turn on which of the two is taken because both sit within
    a factor 1.13 of each other and 7.4 times above the extended grid floor.
    """
    return {
        "adopted_floor_eV": GE_BAND_GAP_T0_eV - GE_FREE_EXCITON_BINDING_eV,
        "band_gap_T0_eV": GE_BAND_GAP_T0_eV,
        "band_gap_300K_eV": GE_BAND_GAP_300K_eV,
        "free_exciton_binding_eV": GE_FREE_EXCITON_BINDING_eV,
        "choice": "indirect band gap at T -> 0, less the free-exciton binding",
        "alternatives_named": "300 K indirect gap 0.661 eV; bare T->0 gap 0.7437 eV",
        "provenance": "[UNVERIFIED - training data]; no repository artifact "
                      "carries a germanium band gap.",
    }


# =========================================================================== #
# 4. THE ELECTRON-SIDE IMPULSE-APPROXIMATION ANALOGUE                          #
# =========================================================================== #
#
# THE POINT OF THIS SECTION.  `fp-unexamined-no` forbids concluding "these are
# electron recoils, so the nuclear kernel does not apply" without testing the one
# mechanism that could make that conclusion wrong.  That mechanism is the
# Compton profile: the SAME impulse-approximation formalism with the bound
# ELECTRON's momentum distribution in place of the nucleus's.  It is evaluated
# here with numbers, not dismissed.
#
# THE DERIVATION, in one line and not re-using any Section-J identity.  Energy
# and momentum conservation for a struck particle of mass m carrying initial
# momentum p, receiving momentum transfer q:
#       T = (|p + q|^2 - p^2) / (2m) = q^2/(2m) + p.q/m .
# The mean is q^2/(2m) -- the free recoil -- and the variance is
# q^2 sigma_pz^2 / m^2, so
#       sigma_T = q sigma_pz / m = sqrt(2 m T) sigma_pz / m = sqrt(T * omega_bar_X)
# with  omega_bar_X == 2 sigma_pz^2 / m .
# For the NUCLEUS, sigma_p^2 = m_N omega_bar / 2 (zero-point oscillator) returns
# omega_bar_X = omega_bar, which is Phase 11's result.  For the ELECTRON, sigma_pz
# is the width of the Compton profile and omega_bar_e is an ELECTRONIC energy.
# Same form, different body, different scale.

#: Rydberg-atomic-unit conversions used only in this section.
HARTREE_eV: float = 27.211386245988
BOHR_ANGSTROM: float = 0.529177210903


def electron_ia_scale_eV() -> dict:
    """The electron-side IA scale omega_bar_e = 2 sigma_pz^2 / m_e, bracketed.

    Three estimators, deliberately spanning the plausible range rather than
    picking one, because the verdict must not depend on the choice:

    LOWER BOUND (rigorous, and derived from a COMMITTED number).  A valence
    electron confined to the germanium covalent bond, length a*sqrt(3)/4 with
    a = 5.658 angstrom, has sigma_pz >= hbar/(2 d) by the uncertainty principle.
    This is a bound, not an estimate: no germanium electron can be more
    delocalized than its bond and still be bound.

    VALENCE VIRIAL.  For an electron bound by |E_B|, the virial theorem gives
    <p^2> = 2 m |E_B| and sigma_pz^2 = <p^2>/3, hence omega_bar_e = 4|E_B|/3.
    Evaluated at the germanium valence-band width, |E_B| = 12.6 eV.
    [UNVERIFIED - training data.]

    WHOLE-ATOM ENVELOPE.  The same virial argument over ALL 32 electrons, using
    the nonrelativistic Hartree-Fock total energy of neutral Ge.  It is an
    ENVELOPE, not an estimate for this problem: the 1s electrons it is dominated
    by are inaccessible below ~11 keV of transfer and cannot contribute to a
    sub-eV deposit at all.  [UNVERIFIED - training data.]
    """
    d_bond_ang = GE_LATTICE_CONSTANT_ANGSTROM * np.sqrt(3.0) / 4.0
    d_bond_au = d_bond_ang / BOHR_ANGSTROM
    sigma_lo_au = 0.5 / d_bond_au
    w_lo = 2.0 * sigma_lo_au ** 2 * HARTREE_eV

    E_B_valence_eV = 12.6
    w_val = 4.0 * E_B_valence_eV / 3.0

    E_HF_hartree = 2075.36     # |E_total| of neutral Ge, nonrelativistic HF
    w_atom = 4.0 / 3.0 * (E_HF_hartree / 32.0) * HARTREE_eV

    return {
        "bond_length_angstrom": float(d_bond_ang),
        "sigma_pz_lower_bound_au": float(sigma_lo_au),
        "omega_bar_e_lower_bound_eV": float(w_lo),
        "omega_bar_e_valence_virial_eV": float(w_val),
        "omega_bar_e_whole_atom_envelope_eV": float(w_atom),
        "omega_bar_nuclear_eV": float(params.OMEGA_BAR_eV.value),
        "ratio_lower_bound_to_nuclear": float(w_lo / params.OMEGA_BAR_eV.value),
        "width_ratio_lower_bound": float(np.sqrt(w_lo / params.OMEGA_BAR_eV.value)),
        "width_ratio_whole_atom": float(np.sqrt(w_atom / params.OMEGA_BAR_eV.value)),
        "provenance": (
            "lower bound: DERIVED from GE_LATTICE_CONSTANT_ANGSTROM = 5.658 and "
            "the uncertainty principle, no external number needed. valence and "
            "whole-atom estimators: [UNVERIFIED - training data]. The verdict "
            "rests on the LOWER BOUND alone; the other two only show how much "
            "further the true value can lie from the nuclear scale."),
    }


def electron_side_sigma_T_eV(T_eV, omega_bar_e_eV: float):
    """sigma_T = sqrt(T * omega_bar_e), the electron-side IA width [eV]."""
    return np.sqrt(np.asarray(T_eV, float) * float(omega_bar_e_eV))


def electron_side_summary(T_eV: float) -> dict:
    """The full electron-analogue evaluation at one deposit energy.

    Reports the electron-side width under each estimator, its size in extended
    grid bins, the electron-side IA validity parameter 2W_e = T/omega_bar_e, and
    -- for comparison only -- what the NUCLEAR kernel would have produced.  The
    nuclear number is present so the transplant's error is quantified; it is not
    an endorsement of applying it.
    """
    sc = electron_ia_scale_eV()
    one_bin = 10.0 ** (np.log10(2.0e5 / 1.0e-2) / 584) - 1.0
    out = {"T_eV": float(T_eV), "one_extended_bin_fractional": float(one_bin)}
    for key, w in (("lower_bound", sc["omega_bar_e_lower_bound_eV"]),
                   ("valence_virial", sc["omega_bar_e_valence_virial_eV"]),
                   ("whole_atom_envelope", sc["omega_bar_e_whole_atom_envelope_eV"])):
        s = float(electron_side_sigma_T_eV(T_eV, w))
        out[f"omega_bar_e_{key}_eV"] = float(w)
        out[f"sigma_T_{key}_eV"] = s
        out[f"sigma_T_over_T_{key}"] = s / float(T_eV)
        out[f"sigma_T_in_bins_{key}"] = (s / float(T_eV)) / one_bin
        out[f"two_W_e_{key}"] = float(T_eV) / float(w)
    wn = float(params.OMEGA_BAR_eV.value)
    sn = float(electron_side_sigma_T_eV(T_eV, wn))
    out["nuclear_transplant_sigma_E_eV"] = sn
    out["nuclear_transplant_sigma_E_over_E"] = sn / float(T_eV)
    return out


# =========================================================================== #
# 5. THE FROZEN FLOOR TABLE                                                    #
# =========================================================================== #

V1_FLOOR_eV: float = 10.144972680282425
EXT_FLOOR_eV: float = 0.09993497

MUON_ACCURACY_LABEL: str = (
    "flatters_SB(-20.61% vs PDG Leg A; Leg B +20.34%; legs BRACKET the adopted "
    "1.3659 Hz, magnitude ~20% solid, SIGN anchor-leg dependent)"
)
GAMMA_ACCURACY_LABEL: str = "neutral(factor-2 site band x0.5..x2, LABChico anchor)"


def validity_floor_rows() -> list[dict]:
    """The rows frozen into ``artifacts/v2.0/em_validity_floors.csv``."""
    lv = landau_validity_floor()
    ind = indicted_v1_bins(lv["floor_eV"])
    s_ext = compton_S_suppression(EXT_FLOOR_eV)
    s_v1 = compton_S_suppression(V1_FLOOR_eV)
    pf = compton_physical_floor()
    ell_v1 = chord_cm_of_deposit_eV(V1_FLOOR_eV)
    ell_ext = chord_cm_of_deposit_eV(EXT_FLOOR_eV)

    def _row(channel, criterion, floor_eV, label, note, **extra):
        r = {
            "channel": channel,
            "criterion_name": criterion,
            "floor_eV": floor_eV,
            "v1_grid_floor_eV": V1_FLOOR_eV,
            "ext_grid_floor_eV": EXT_FLOOR_eV,
            "floor_above_v1_grid_floor": bool(floor_eV > V1_FLOOR_eV),
            "floor_over_v1_grid_floor_ratio": floor_eV / V1_FLOOR_eV,
            "n_v1_bins_below_floor": 0,
            "n_ext_bins_below_floor": 0,
            "accuracy_label": label,
            "note": note,
        }
        r.update(extra)
        return r

    rows = [
        _row("muon", "landau_vavilov_xi_le_I", lv["floor_eV"], MUON_ACCURACY_LABEL,
             ("Landau-Vavilov continuous straggling requires many collisions, i.e. "
              "xi >> I. Crossing computed on the committed muon_deposit path at "
              f"E_mu = {REFERENCE_E_MU_GEV} GeV, the reference point of the "
              "09-01 vertical-chord scalars. The committed chain already guards "
              "the THIN end via kappa = 6.727e-05; this guards the other end. "
              "THIS FLOOR LIES ABOVE THE v1.0 GRID FLOOR AND THEREFORE INDICTS "
              "BINS THE v1.0 MANUSCRIPT PUBLISHED."),
             n_v1_bins_below_floor=ind["n_v1_bins_below_floor"],
             n_ext_bins_below_floor=ind["n_ext_bins_below_floor"],
             chord_at_floor_cm=lv["chord_cm"],
             chord_at_floor_lattice_constants=lv["chord_lattice_constants"],
             xi_at_floor_eV=lv["xi_at_crossing_eV"],
             I_eV=lv["I_eV"]),
        _row("muon", "chord_map_v1_grid_floor", V1_FLOOR_eV, MUON_ACCURACY_LABEL,
             ("Chord required for a Delta_p of exactly the v1.0 grid floor, "
              "inverted on the committed mpv_deposit path. Reported for scale, "
              "not as a validity criterion."),
             chord_at_floor_cm=ell_v1,
             chord_at_floor_lattice_constants=chord_in_lattice_constants(ell_v1),
             xi_at_floor_eV=float(xi_eV_of_chord_cm(ell_v1)),
             I_eV=I_GE_eV),
        _row("muon", "chord_map_ext_grid_floor", EXT_FLOOR_eV, MUON_ACCURACY_LABEL,
             ("Chord required for a Delta_p of exactly the extended grid floor. "
              "UNDER TWO GERMANIUM LATTICE CONSTANTS: the deposit at the extended "
              "floor corresponds to a muon path of a few atomic layers."),
             chord_at_floor_cm=ell_ext,
             chord_at_floor_lattice_constants=chord_in_lattice_constants(ell_ext),
             xi_at_floor_eV=float(xi_eV_of_chord_cm(ell_ext)),
             I_eV=I_GE_eV),
        _row("compton", "ge_pair_creation_threshold", pf["adopted_floor_eV"],
             GAMMA_ACCURACY_LABEL,
             ("Adopted physical floor: germanium indirect band gap at T -> 0 "
              "(0.7437 eV) less the free-exciton binding (4.15 meV). Below this "
              "no electron-hole pair can be created, so an 'electron recoil "
              "deposit' is not the physical process the S(x,Z) machinery "
              "describes. [UNVERIFIED - training data]; the 300 K gap 0.661 eV "
              "is the named alternative."),
             n_ext_bins_below_floor=int(np.sum(
                 np.sqrt(md.shared_energy_grid("v2.0-ext")[:-1]
                         * md.shared_energy_grid("v2.0-ext")[1:]) * 1e3
                 < pf["adopted_floor_eV"])),
             S_incoherent=float("nan"), S_over_Z=float("nan"),
             x_inv_angstrom=float("nan")),
        _row("compton", "S_suppression_at_ext_grid_floor", EXT_FLOOR_eV,
             GAMMA_ACCURACY_LABEL,
             ("S(x, Z=32) read from the committed data/ge_incoherent_S.csv. The "
              "table domain COVERS this x, so no interpolator raises on the "
              "extended axis. A number the table returns is NOT a rate the "
              "physics supports: this recoil sits a factor 7.40 BELOW the "
              "adopted pair-creation floor."),
             S_incoherent=s_ext["S_incoherent"], S_over_Z=s_ext["S_over_Z"],
             x_inv_angstrom=s_ext["x_inv_angstrom"]),
        _row("compton", "S_suppression_at_v1_grid_floor", V1_FLOOR_eV,
             GAMMA_ACCURACY_LABEL,
             ("S(x, Z=32) at the v1.0 grid floor, same committed table. This "
              "recoil is above the pair-creation floor by a factor 13.7."),
             S_incoherent=s_v1["S_incoherent"], S_over_Z=s_v1["S_over_Z"],
             x_inv_angstrom=s_v1["x_inv_angstrom"]),
    ]
    return rows
