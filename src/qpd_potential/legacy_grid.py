# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
#
# Phase-10 (Plan 10-05) archived-artifact disposition register and its guard.
#
# ROADMAP Phase 10 success criterion 2: "Every archived v1.x spectrum is either
# re-gridded onto the extended axis or explicitly tagged valid only above
# 10.14 eV; no legacy artifact is silently reinterpolated onto the new grid."
#
# THE REGISTER IS A SIDECAR, NOT AN EDIT.  The frozen artifacts' own provenance
# headers carry recorded git SHAs and integrity statements; rewriting them to add
# validity tags would invalidate exactly the provenance this register exists to
# protect (`fp-header-rewrite`).  So the tags live in
# artifacts/v2.0/legacy_grid_disposition.csv and this module reads them.
#
# THE GUARD RAISES, IT DOES NOT CLAMP.  Same discipline as plan 10-01: asking for
# a bounded artifact below its recorded validity floor is an error at the point
# of the request, not a clamped, extrapolated, or zero value.  Below its own
# floor a legacy artifact HAS NO DATA; continuity there would come from whatever
# interpolation filled the gap, which is precisely the silent reinterpolation
# success criterion 2 forbids (`fp-silent-carry`).
#
# WHICH READING OF "ARCHIVED v1.x SPECTRUM" THIS ADOPTS.  Criterion 2 does not
# define whether input tables on foreign axes are in scope.  This register adopts
# the WIDER reading -- every tracked .csv/.npz artifact gets a row -- because the
# narrow reading would leave the CEvNS dR/dT table, the ENDF n-Ge table and the
# reactor flux tables untagged, and those are exactly the artifacts a sub-eV plot
# is most likely to be silently extended through.  Justified in
# 10-05-ARTIFACT-DISPOSITION.md.

from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from typing import Optional

__all__ = [
    "LegacyArtifactError",
    "Disposition",
    "REGISTER_PATH",
    "load_register",
    "disposition_for",
    "check_evaluation_point",
    "carried_onto_extended_axis",
    "DISPOSITION_VALUES",
]

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))

REGISTER_PATH = os.path.join(_PROJECT_ROOT, "artifacts", "v2.0",
                             "legacy_grid_disposition.csv")

#: Closed vocabulary. A row outside it is a register error, not a default.
DISPOSITION_VALUES = (
    "carried_onto_extended_axis_without_reinterpolation",
    "bounded_native_axis",
    "bounded_superseded",
    "native_to_extended_axis",
    "not_a_spectrum",
)

#: Dispositions that carry a numeric validity floor and are therefore guardable.
_BOUNDED = ("bounded_native_axis", "bounded_superseded",
            "carried_onto_extended_axis_without_reinterpolation",
            "native_to_extended_axis")


class LegacyArtifactError(ValueError):
    """Raised when a bounded archived artifact is asked for below its floor."""


@dataclass(frozen=True)
class Disposition:
    path: str
    native_axis: str
    axis_units: str
    validity_floor: Optional[float]
    disposition: str
    reason: str

    @property
    def is_bounded(self) -> bool:
        return self.disposition in _BOUNDED and self.validity_floor is not None


def load_register(path: str = REGISTER_PATH) -> dict[str, Disposition]:
    """Read the disposition register into ``{path: Disposition}``."""
    out: dict[str, Disposition] = {}
    with open(path, newline="") as fh:
        rows = csv.DictReader(r for r in fh if not r.startswith("#"))
        for r in rows:
            floor = r["validity_floor"].strip()
            if r["disposition"] not in DISPOSITION_VALUES:
                raise ValueError(
                    f"{r['path']}: disposition {r['disposition']!r} is outside the "
                    f"closed vocabulary {DISPOSITION_VALUES}")
            if not r["reason"].strip():
                raise ValueError(f"{r['path']}: empty disposition reason")
            out[r["path"]] = Disposition(
                path=r["path"], native_axis=r["native_axis"],
                axis_units=r["axis_units"],
                validity_floor=float(floor) if floor else None,
                disposition=r["disposition"], reason=r["reason"])
    return out


def disposition_for(artifact_path: str, register=None) -> Disposition:
    reg = register if register is not None else load_register()
    if artifact_path not in reg:
        raise KeyError(
            f"{artifact_path!r} has no disposition row. Every tracked .csv/.npz "
            "artifact must carry one; add it to artifacts/v2.0/"
            "legacy_grid_disposition.csv rather than assuming a default "
            "(ROADMAP Phase 10 success criterion 2).")
    return reg[artifact_path]


def check_evaluation_point(artifact_path: str, value, register=None):
    """Raise ``LegacyArtifactError`` if ``value`` is below the artifact's floor.

    ``value`` is in the units of the artifact's OWN native axis, recorded in the
    register's ``axis_units`` column -- keV for the shared-grid deposit spectra,
    eV for the CEvNS recoil table and the response matrices, MeV for the reactor
    flux tables, dimensionless x for the incoherent scattering function.
    """
    d = disposition_for(artifact_path, register)
    if not d.is_bounded:
        return value
    lo = float(d.validity_floor)
    import numpy as np
    arr = np.asarray(value, dtype=float)
    if np.any(~np.isfinite(arr)):
        raise LegacyArtifactError(
            f"{artifact_path}: non-finite evaluation point {value!r}")
    if np.any(arr < lo):
        bad = np.atleast_1d(arr[arr < lo] if arr.ndim else arr)
        raise LegacyArtifactError(
            f"{artifact_path}: evaluation at {np.array2string(bad[:5], precision=9)} "
            f"[{d.axis_units}] is BELOW the recorded validity floor {lo!r} "
            f"[{d.axis_units}]. Native axis: {d.native_axis}. "
            f"Disposition: {d.disposition}. "
            "Below its own floor this artifact HAS NO DATA -- a value here would be "
            "whatever an interpolation invented, which is the silent reinterpolation "
            "ROADMAP Phase 10 success criterion 2 forbids. This is an error, not a "
            "clamp.")
    return arr


def carried_onto_extended_axis(values, n_prepended: int = 160, n_total: int = 744):
    """Place a v1.0 shared-grid quantity onto the 744-bin extended axis.

    **By INDEX, with no interpolation of any kind.** Plan 10-03 preserved the
    v1.0 edge array exactly (``np.array_equal``, max difference 0.0), so v1.0
    bin *i* IS extended bin ``n_prepended + i``. The lower ``n_prepended`` bins
    are filled with NaN, not zero: this artifact carries **no data** there, and a
    zero would read as a measured absence rather than as an absence of
    measurement.
    """
    import numpy as np
    v = np.asarray(values, dtype=float)
    if v.shape[0] != n_total - n_prepended:
        raise ValueError(
            f"expected {n_total - n_prepended} v1.0 bins, got {v.shape[0]}; this "
            "quantity is not on the v1.0 shared deposit grid and cannot be carried "
            "by index")
    out = np.full((n_total,) + v.shape[1:], np.nan, dtype=float)
    out[n_prepended:] = v
    return out
