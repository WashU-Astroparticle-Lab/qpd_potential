# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
#
# Phase-9 Plan 09-03: the ONE loader for the frozen unshielded sea-level surface
# environment.  Phases 13, 14 and 15 draw every environment quantity from here,
# always together with its per-channel accuracy label, so that no channel can be
# silently renormalized downstream.
#
# SCENARIO (CONVENTIONS.md Section D, unchanged): unshielded surface wafer, sea
# level, ZERO OVERBURDEN, 3 GW_th at 25 m.  Veto credit is exactly 1.0 BY
# CONSTRUCTION -- there is no veto in this configuration -- not by a policy
# default a later phase could relax.
#
# ENERGY SCALE (CONVENTIONS.md Section B): single unified phonon scale, NO
# ionization quenching.  The muon and Compton deposits are ELECTRON recoils.  The
# neutron entry is an INCIDENT FLUX on an incident-neutron-kinetic-energy axis --
# never a recoil, never quenched; the n-Ge fold is Phase 13.
#
# WHY THERE IS NO COMBINED UNCERTAINTY BAND (fp-combined-band).  The three
# channels rest on qualitatively different evidence: a validated fold with a
# ~20% anchor comparison, a site-dependent factor-2 normalization, and an
# order-of-magnitude estimate whose only cross-check is a single >10 MeV
# integral.  Averaging them into one phase-level band would launder the neutron
# order_of_magnitude label into a percentage and let a downstream acceptance test
# demand better than order-of-magnitude agreement on a channel that cannot
# support it.  This module therefore exposes NO combined-band accessor at all.

from __future__ import annotations

import csv
import hashlib
import os
import sys
from dataclasses import dataclass

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
REGISTRY_PATH = os.path.join(REPO_ROOT, "data", "surface_environment_v2.0.csv")

CHANNELS = ("muon", "gamma", "neutron")

REQUIRED_COLUMNS = (
    "channel", "quantity", "value", "units", "artifact_path", "artifact_sha256",
    "source_citation", "accuracy_label", "bias_direction", "signed_deviation",
    "notes",
)

BIAS_DIRECTIONS = ("flatters_SB", "penalizes_SB", "neutral")

#: One accuracy label per channel, kept SEPARATE by construction.
CHANNEL_ACCURACY = {
    "muon": "pdg_within_20pct_vald02_tol_30pct",
    "gamma": "site_band_factor_2",
    "neutron": "order_of_magnitude",
}


# --------------------------------------------------------------------------- #
# Shielded-token guard -- single source of truth, not re-typed                  #
# --------------------------------------------------------------------------- #
def shielded_token_guard():
    """Return ``(SHIELDED_TOKENS, SHIELDED_TOKENS_EXTRA)`` from Plan 09-01.

    Deliberately IMPORTED rather than re-typed: the token list is the SC5 guard,
    and two divergent copies of a guard list is how a guard silently stops
    guarding.  ``tests/test_env_v1_identity.py`` is the single definition site.
    """
    tests_dir = os.path.join(REPO_ROOT, "tests")
    if tests_dir not in sys.path:
        sys.path.insert(0, tests_dir)
    from test_env_v1_identity import SHIELDED_TOKENS, SHIELDED_TOKENS_EXTRA
    return SHIELDED_TOKENS, SHIELDED_TOKENS_EXTRA


def veto_credit() -> float:  # exactly 1.0 BY CONSTRUCTION; NOT applied as a rejection
    """The veto rejection credit for this configuration: exactly 1.0.

    BY CONSTRUCTION, not by default.  This is an UNSHIELDED SURFACE wafer: there
    is no veto, no shield and no overburden, so there is nothing for a rejection
    credit to be taken against.  1.0 here means "the background is unchanged".

    The distinction matters and is why this docstring exists: a 1.0 arrived at as
    a policy default is something a later phase could quietly relax; a 1.0 that
    follows from the absence of the apparatus cannot be relaxed without first
    changing the configuration.  The Phase-8 geometry gate
    (08-05-GATE-VERDICT.md) returned NO FIT and voided the shielded premise.
    """
    return 1.0


# --------------------------------------------------------------------------- #
# Registry access                                                              #
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class EnvironmentQuantity:
    """One declared environment input, inseparable from its accuracy label."""

    channel: str
    quantity: str
    value: float
    units: str
    artifact_path: str
    artifact_sha256: str
    source_citation: str
    accuracy_label: str
    bias_direction: str
    signed_deviation: str
    notes: str

    def verify_artifact(self, repo_root: str = REPO_ROOT) -> bool:
        """True if the referenced artifact is on disk with the declared hash."""
        p = os.path.join(repo_root, self.artifact_path)
        if not os.path.isfile(p):
            return False
        return sha256_of(p) == self.artifact_sha256


def sha256_of(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def header_lines(path: str = REGISTRY_PATH) -> list[str]:
    """The '#' provenance header block above the CSV data."""
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("#"):
                break
            out.append(line.rstrip("\n"))
    return out


def load(path: str = REGISTRY_PATH) -> list[EnvironmentQuantity]:
    """Load every declared environment input, each with its accuracy label."""
    rows: list[EnvironmentQuantity] = []
    with open(path, encoding="utf-8") as fh:
        body = (ln for ln in fh if not ln.startswith("#"))
        for r in csv.DictReader(body):
            rows.append(EnvironmentQuantity(
                channel=r["channel"], quantity=r["quantity"],
                value=float(r["value"]), units=r["units"],
                artifact_path=r["artifact_path"],
                artifact_sha256=r["artifact_sha256"],
                source_citation=r["source_citation"],
                accuracy_label=r["accuracy_label"],
                bias_direction=r["bias_direction"],
                signed_deviation=r["signed_deviation"],
                notes=r["notes"],
            ))
    return rows


def get(channel: str, quantity: str,
        path: str = REGISTRY_PATH) -> EnvironmentQuantity:
    """Return one quantity, INSEPARABLE from its accuracy label.

    There is no accessor that returns a bare float: a consumer cannot obtain a
    neutron number without also receiving its ``order_of_magnitude`` tag.
    """
    for row in load(path):
        if row.channel == channel and row.quantity == quantity:
            return row
    raise KeyError(
        f"({channel!r}, {quantity!r}) is not a declared surface-environment "
        "input. Declared: "
        + ", ".join(f"({r.channel},{r.quantity})" for r in load(path))
    )


def accuracy_label(channel: str) -> str:
    """The accuracy label of ONE channel.  There is no combined-band accessor."""
    if channel not in CHANNELS:
        raise ValueError(f"{channel!r} not in {CHANNELS}")
    return CHANNEL_ACCURACY[channel]


def bias_audit(path: str = REGISTRY_PATH) -> dict[str, tuple[str, str]]:
    """Per-channel ``(bias_direction, signed_deviation)`` for the headline rows."""
    out: dict[str, tuple[str, str]] = {}
    for row in load(path):
        if row.bias_direction and row.bias_direction != "-":
            out.setdefault(row.channel, (row.bias_direction, row.signed_deviation))
    return out
