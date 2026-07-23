# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
#
# Phase-10 (Plan 10-02) SUB-eV REPORTED OBSERVABLE: the trigger-probability curve.
#
# ROADMAP Phase 10 success criterion 4; requirement CALC-16.
#
# WHY THE REPORTED OBJECT CHANGES BELOW ~1 eV.  USER DECISION 2026-07-22
# (GPD/STATE.md, Accumulated Context): below roughly 1 eV of deposited energy,
# dR/dE_rec presupposes the lumped eps ~= 0.5 deposited-to-signal collection
# efficiency of CONVENTIONS Section E, and that lumping is not defensible for a
# deposit of ~3 optical-phonon quanta in Ge.  The user chose to REPLACE THE
# REPORTED OBJECT rather than patch the efficiency: below the regime boundary the
# reported quantity is a trigger PROBABILITY, not a differential rate.
#
# THIS CURVE IS PHENOMENOLOGICAL.  No trigger threshold has ever been measured
# for this device.  Exactly ONE property of it carries a project decision: the
# 50% point sits at 0.5 eV.  The functional form is chosen (see below) and the
# sharpness is fixed by NO project artifact -- it is an exposed, scannable
# parameter registered in params.py alongside F_PROMPT and R_SPOT, never a
# buried literal.  A hard-coded width would fabricate a device property that
# downstream results would inherit without being able to test sensitivity to it
# (fp-hardcoded-width).
#
# WHY A HILL / LOG-ENERGY LOGISTIC AND NOT A LINEAR-ENERGY LOGISTIC.  For
#     P(E) = 1 / (1 + (E50/E)^k)          [adopted]
# the 50% point sits at E = E50 IDENTICALLY IN k, P(0+) = 0, and P -> 1.  For
#     P(E) = 1 / (1 + exp(-(E - E50)/w))  [rejected, fp-linear-sigmoid]
# the 50% point is also at E50, but P(0) = 1/(1 + exp(E50/w)) > 0: a nonzero
# probability of triggering on NOTHING, and a nonzero probability at negative
# energy.  On an axis spanning four decades from 0.1 eV that is not a rounding
# detail.  At w = 0.1 eV the rejected form gives P(0) = 6.693e-03 -- a 0.67%
# floor at zero deposit that would sit under every sub-eV number in the project.
# See 10-02-TRIGGER-CURVE-DERIVATION.md.
#
# COMPOSITION -- THIS MULTIPLIES eps, IT DOES NOT REPLACE IT.  eps enters the
# physics chain in TWO places: inside energy_scale.n_qp_yield as
# N_qp = eps * E_sensor / Delta_tr, and again as the calibration slope through
# response.calibrate_C.  There is therefore no single pre-existing
# efficiency-composition point in the codebase, so this module CREATES one:
# compose_efficiency(E, untriggered) returns P_trig(E) * untriggered, where the
# un-triggered quantity already carries eps through the response chain.  Setting
# P_trig == 1 reproduces the pre-existing chain bit-for-bit.  CONVENTIONS
# Sections E and F are untouched by this module (fp-sigmoid-replaces-eps).
#
# UNITS (CONVENTIONS Section A.1): deposited energy E_dep in eV; P_trig is
# dimensionless in [0, 1]; the sharpness k is dimensionless.

from __future__ import annotations

import numpy as np

from . import params

__all__ = [
    "P_trig",
    "compose_efficiency",
    "SUBEV_REGIME_BOUNDARY_eV",
    "REGIME_STATEMENT",
    "linear_energy_logistic_rejected",
]

# --------------------------------------------------------------------------- #
# The declared sub-eV regime boundary -- ONE importable definition             #
# --------------------------------------------------------------------------- #

#: Deposited energy [eV] below which the reported observable is the TRIGGER
#: PROBABILITY, not dR/dE_rec.  ROADMAP Phase 10 success criterion 4 phrases the
#: boundary as "~1 eV"; this is the single importable definition of it, so that
#: plan 10-05 and Phases 12-15 label the boundary from one source instead of
#: restating a literal (test-regime-constant).
SUBEV_REGIME_BOUNDARY_eV: float = 1.0

#: The one-sentence statement every sub-eV deliverable must carry, imported
#: rather than paraphrased.
REGIME_STATEMENT: str = (
    f"Below {SUBEV_REGIME_BOUNDARY_eV:g} eV deposited energy the reported observable is the "
    "trigger probability P_trig(E_dep), not the differential rate dR/dE_rec: at that scale "
    "dR/dE_rec presupposes the lumped eps ~= 0.5 collection efficiency (CONVENTIONS Section E), "
    "which is not defensible for a deposit of a few optical-phonon quanta in Ge "
    "(USER DECISION 2026-07-22)."
)


# --------------------------------------------------------------------------- #
# The curve                                                                    #
# --------------------------------------------------------------------------- #


def P_trig(E_dep_eV, e50_eV: float | None = None, sharpness: float | None = None):
    """Trigger probability at deposited energy ``E_dep_eV`` [eV].

    Hill form, equivalently a logistic in log energy::

        P(E) = 1 / (1 + (E50 / E)^k)       for E > 0
        P(0) = 0                            by continuity

    Parameters
    ----------
    E_dep_eV : scalar or array, deposited energy [eV], >= 0.
    e50_eV   : the 50% point [eV].  Defaults to ``params.TRIGGER_E50.value``,
               fixed at 0.5 eV by USER DECISION 2026-07-22.  Never a literal here.
    sharpness : dimensionless k > 0.  Defaults to
               ``params.TRIGGER_SHARPNESS.value``; scan range
               ``params.TRIGGER_SHARPNESS_RANGE``.  Fixed by no measurement.

    Structural properties, exact for EVERY k > 0 (see the derivation note):
      * ``P(E50) = 1/(1 + 1^k) = 1/2`` exactly, independent of k;
      * ``P(E) -> 0`` as ``E -> 0+``, and ``P(0) = 0``;
      * ``P(E) -> 1`` as ``E -> inf``, and ``P`` is strictly increasing on E > 0.

    The 50% point is therefore a property of the FUNCTIONAL FORM, not of any
    particular width (``fp-e50-by-tuning``).
    """
    if e50_eV is None:
        e50_eV = params.TRIGGER_E50.value
    if sharpness is None:
        sharpness = params.TRIGGER_SHARPNESS.value
    if e50_eV <= 0.0:
        raise ValueError(f"the trigger 50% point must be positive, got {e50_eV}")
    if sharpness <= 0.0:
        raise ValueError(f"the trigger sharpness k must be positive, got {sharpness}")

    E = np.asarray(E_dep_eV, dtype=float)
    if np.any(E < 0.0):
        raise ValueError("deposited energy must be non-negative")

    out = np.zeros_like(E, dtype=float)     # P(0) = 0 exactly, by continuity
    pos = E > 0.0
    if np.any(pos):
        # Evaluated in log space so that (E50/E)^k does not overflow for E far
        # below E50: (E50/E)^k = exp(k * (ln E50 - ln E)) and
        # 1/(1 + exp(z)) is computed as expit(-z).
        z = sharpness * (np.log(e50_eV) - np.log(E[pos]))
        # numerically stable logistic
        out[pos] = np.where(z >= 0.0,
                            np.exp(-z) / (1.0 + np.exp(-z)),
                            1.0 / (1.0 + np.exp(z)))
    return out if out.ndim else float(out)


def linear_energy_logistic_rejected(E_dep_eV, e50_eV: float | None = None,
                                    width_eV: float = 0.1):
    """THE REJECTED ALTERNATIVE, kept only so its defect is testable.

    ``P(E) = 1 / (1 + exp(-(E - E50)/w))``.  Its 50% point is also at E50, but
    ``P(0) = 1/(1 + exp(E50/w)) > 0``: a nonzero probability of triggering on
    nothing.  Never use this as the project's trigger curve
    (``fp-linear-sigmoid``); it exists so ``tests/test_trigger_efficiency.py``
    can demonstrate which assertion it breaks.
    """
    if e50_eV is None:
        e50_eV = params.TRIGGER_E50.value
    E = np.asarray(E_dep_eV, dtype=float)
    return 1.0 / (1.0 + np.exp(-(E - e50_eV) / width_eV))


# --------------------------------------------------------------------------- #
# The composition point (created here; none existed)                          #
# --------------------------------------------------------------------------- #


def compose_efficiency(E_dep_eV, untriggered, e50_eV: float | None = None,
                       sharpness: float | None = None):
    """Compose the trigger efficiency ON TOP OF an already-computed quantity.

    ``composed(E) = P_trig(E) * untriggered``

    ``untriggered`` is a quantity that has ALREADY been through the response
    chain and therefore ALREADY CONTAINS eps ~= 0.5 -- both through
    ``energy_scale.n_qp_yield`` (N_qp = eps * E_sensor / Delta_tr) and through
    the ``response.calibrate_C`` calibration slope.  **eps lives inside
    ``untriggered`` and is NOT replaced here.**  This function multiplies a
    dimensionless analysis efficiency onto it and does nothing else: no
    renormalisation, no absorption of eps into the sigmoid, no clipping.

    Two consequences that are unit-tested and are the acceptance evidence for
    CALC-16:
      * exact factorisation -- ``composed == P_trig * untriggered`` on every
        grid point;
      * ``P_trig == 1`` reproduces ``untriggered`` bit-for-bit, proving the
        curve is a factor added on top rather than a modification of the chain.

    Perturbing ``params.EPSILON`` must change ``composed`` by exactly the ratio
    it changes ``untriggered``, with ``P_trig`` bit-identical.  If ``composed``
    is insensitive to eps, the sigmoid has REPLACED eps and the requirement has
    been violated (``fp-sigmoid-replaces-eps``).
    """
    p = P_trig(E_dep_eV, e50_eV=e50_eV, sharpness=sharpness)
    return p * np.asarray(untriggered, dtype=float)
