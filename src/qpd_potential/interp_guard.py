# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
#
# Phase-10 (Plan 10-01) shared bounds guard for tabulated-input interpolators.
#
# ROADMAP Phase 10 success criterion 3: "every interpolator raises outside its
# declared evaluation domain (no silent clamping or extrapolation at a table
# floor)".  Extending the shared deposited-energy axis two decades below
# 10.14 eV (plan 10-03) is exactly the operation that drives evaluations below
# table floors, so this guard has to land BEFORE the extension.
#
# WHY A RAISE AND NOT A NaN (fp-nan-instead-of-raise).  `PchipInterpolator(...,
# extrapolate=False)` returns NaN outside its knots.  A NaN propagates silently
# into a spectrum where it can be filtered, zeroed, or masked downstream; the
# requirement is an error AT THE POINT OF EVALUATION.
#
# WHY A DECLARED DOMAIN AND NOT JUST THE TABLE SPAN.  Two v1.0 call sites
# deliberately evaluate outside their tabulated span -- the NIST XCOM mu/rho
# slope extrapolation and the Hubbell S(x) low-x continuation.  Making those
# raise unconditionally would break v1.0 anchors.  So a call site may declare a
# domain WIDER than its table, but only with a named WITNESS: a concrete
# evaluation point an existing v1.0 anchor already uses that falls inside the
# extension.  A declared extension with no witness is indistinguishable from
# silencing the guard and is forbidden (see
# GPD/phases/10-.../10-01-INTERPOLATOR-INVENTORY.md).
#
# UNITS (CONVENTIONS Section A.1).  Every Domain records the units of its OWN
# abscissa -- MeV for Phi(E_nu), keV for mu/rho, eV for E_dep, dimensionless x
# for the incoherent scattering function.  No bound is converted implicitly.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np

__all__ = [
    "InterpolationDomainError",
    "Domain",
    "check_domain",
    "register_domain",
    "registered_domains",
]


class InterpolationDomainError(ValueError):
    """Raised when a tabulated-input interpolator is evaluated out of domain.

    Subclasses ``ValueError`` so that callers written against the pre-existing
    ``ValueError`` contract still behave, but it is a NAMED type so it is
    distinguishable from the plain ``ValueError``s raised elsewhere (e.g. the
    unknown-censoring-variant error in ``response_matrix.censor_fast`` or the
    non-positive-flux error in ``cevns.ReactorFlux``).
    """


@dataclass(frozen=True)
class Domain:
    """A declared evaluation domain for one tabulated-input interpolator.

    Parameters
    ----------
    quantity   : what is being interpolated (for the error message).
    lo, hi     : the DECLARED domain, inclusive, in ``units``.
    units      : units of the ABSCISSA, recorded explicitly (CONVENTIONS A.1).
    table      : provenance path of the frozen table supplying the abscissa.
    table_lo, table_hi : the TABULATED span, read from the table at run time.
    witness_lo, witness_hi :
        For a declared bound that lies OUTSIDE the tabulated span, the concrete
        v1.0 evaluation point that requires the extension.  ``None`` when the
        declared bound coincides with the table (no extension, no witness
        needed).  A bound outside the span with no witness is rejected at
        construction -- that is the ``fp-domain-widening`` guard.
    """

    quantity: str
    lo: float
    hi: float
    units: str
    table: str
    table_lo: float
    table_hi: float
    witness_lo: Optional[str] = None
    witness_hi: Optional[str] = None
    note: str = ""

    def __post_init__(self) -> None:
        if not (self.lo <= self.hi):
            raise ValueError(f"Domain {self.quantity!r}: lo={self.lo} > hi={self.hi}")
        # An extension below the tabulated floor needs a named witness.
        if self.lo < self.table_lo and not self.witness_lo:
            raise ValueError(
                f"Domain {self.quantity!r} declares lo={self.lo} {self.units} below its "
                f"tabulated floor {self.table_lo} {self.units} with no witness point. "
                "A declared extension with no witness is forbidden (fp-domain-widening)."
            )
        if self.hi > self.table_hi and not self.witness_hi:
            raise ValueError(
                f"Domain {self.quantity!r} declares hi={self.hi} {self.units} above its "
                f"tabulated ceiling {self.table_hi} {self.units} with no witness point. "
                "A declared extension with no witness is forbidden (fp-domain-widening)."
            )

    @property
    def extends_below(self) -> bool:
        return self.lo < self.table_lo

    @property
    def extends_above(self) -> bool:
        return self.hi > self.table_hi


_REGISTRY: dict[str, Domain] = {}


def register_domain(domain: Domain) -> Domain:
    """Register a module-level Domain so tests can enumerate it mechanically."""
    _REGISTRY[domain.quantity] = domain
    return domain


def registered_domains() -> dict[str, Domain]:
    """All module-level declared domains, keyed by quantity name."""
    return dict(_REGISTRY)


def check_domain(x, domain: Domain):
    """Assert every entry of ``x`` lies inside ``domain``; return ``x`` as array.

    Raises ``InterpolationDomainError`` -- never clamps, never masks, never
    drops offending entries, never returns NaN.  Non-finite input (NaN, +-inf)
    is itself an out-of-domain condition: a NaN abscissa compares False against
    both bounds and would otherwise slip through every comparison.

    Scalars and arrays are both accepted.  The bounds are compared strictly, so
    evaluation exactly AT ``lo`` or ``hi`` is legal and evaluation at
    ``lo * (1 - 1e-9)`` is not.
    """
    arr = np.asarray(x, dtype=float)
    bad_nan = ~np.isfinite(arr)
    if np.any(bad_nan):
        offending = arr[bad_nan] if arr.ndim else arr
        raise InterpolationDomainError(
            f"{domain.quantity}: non-finite abscissa {np.atleast_1d(offending)[:5]} "
            f"[{domain.units}]; declared domain is "
            f"[{domain.lo!r}, {domain.hi!r}] {domain.units} from table {domain.table}"
        )
    below = arr < domain.lo
    above = arr > domain.hi
    if np.any(below) or np.any(above):
        bad = arr[below | above] if arr.ndim else arr
        bad = np.atleast_1d(bad)
        raise InterpolationDomainError(
            f"{domain.quantity}: abscissa out of declared evaluation domain. "
            f"offending value(s) (first 5 of {bad.size}) = "
            f"{np.array2string(bad[:5], precision=9)} [{domain.units}]; "
            f"declared domain = [{domain.lo!r}, {domain.hi!r}] {domain.units}; "
            f"tabulated span = [{domain.table_lo!r}, {domain.table_hi!r}] {domain.units}; "
            f"source table = {domain.table}. "
            "This is an error, not a clamp: the value would previously have been "
            "silently clamped, slope-extrapolated, or returned as NaN/0 "
            "(ROADMAP Phase 10 success criterion 3)."
        )
    return arr
