#!/usr/bin/env python
# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Generate figs/nucleus_fig1_reproduction.png (VALD-02).

Overlays our CEvNS fold, run under the NUCLEUS (2019) assumptions, on their
digitized Fig. 1 germanium curve:
  * upper panel : dR/dE_R vs nuclear-recoil energy -- their curve, our full
    fold, and our fold with the flux truncated at the 1.8 MeV IBD threshold,
  * lower panel : the ours/theirs ratio, which is the decisive test (FLAT means
    the shape agrees and only normalization conventions can differ).

Deposited nuclear-recoil energy only -- NO quenching, NO detector response.
The x-axis floors at 10 eV: below that the project reports nothing (grid-floor
and binding-artifact territory), even though the published figure extends to 1 eV.
"""

from __future__ import annotations

import os
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
)

from qpd_potential import cevns  # noqa: E402

_OUT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "figs", "nucleus_fig1_reproduction.png",
)

_T_FLOOR_EV = 10.0     # project display floor; never plot below this
_T_CEIL_EV = 1000.0


def main() -> int:
    E_fig, R_fig = cevns.load_nucleus_fig1()
    keep = (E_fig >= _T_FLOOR_EV) & (E_fig <= _T_CEIL_EV)
    E_fig, R_fig = E_fig[keep], R_fig[keep]

    T = np.logspace(np.log10(_T_FLOOR_EV), np.log10(_T_CEIL_EV), 70)
    flux_full = cevns.nucleus_variant_flux(sub18=True)
    flux_cut = cevns.nucleus_variant_flux(sub18=False)
    ours = np.array([cevns.differential_rate(t * 1e-3, flux_full) for t in T])
    ours_cut = np.array([cevns.differential_rate(t * 1e-3, flux_cut) for t in T])

    ref = 10.0 ** np.interp(np.log10(T), np.log10(E_fig), np.log10(R_fig))

    fig, (ax, axr) = plt.subplots(
        2, 1, figsize=(6.4, 6.4), sharex=True,
        gridspec_kw={"height_ratios": [2.6, 1.0], "hspace": 0.08},
    )

    ax.loglog(E_fig, R_fig, color="crimson", lw=2.4, alpha=0.85,
              label="NUCLEUS 2019 Fig. 1, Ge (digitized)")
    ax.loglog(T, ours, color="k", lw=1.6, ls="--",
              label="this work, NUCLEUS assumptions")
    ax.loglog(T, ours_cut, color="tab:blue", lw=1.3, ls=":",
              label=r"same, flux truncated at $E_\nu \geq 1.8$ MeV")
    ax.set_ylabel(r"$dR/dE_R$  [counts / (keV kg day)]")
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")
    ax.grid(alpha=0.25, which="both")
    ax.set_title(
        "Ge CEvNS at the Chooz VNS: "
        r"$2\times4.25\,\mathrm{GW_{th}}$ at 72 m and 102 m",
        fontsize=10,
    )

    axr.semilogx(T, ours / ref, color="k", lw=1.6, ls="--")
    axr.semilogx(T, ours_cut / ref, color="tab:blue", lw=1.3, ls=":")
    axr.axhline(1.0, color="crimson", lw=1.2, alpha=0.7)
    axr.axvline(95.0, color="gray", lw=0.9, ls="-.", alpha=0.8)
    axr.text(99.0, 0.42, r"$E_\nu(T)=1.8$ MeV", fontsize=7.5, color="gray")
    axr.set_ylim(0.35, 1.35)
    axr.set_xlabel(r"nuclear-recoil energy $E_R$  [eV]")
    axr.set_ylabel("ratio to\nNUCLEUS", fontsize=9)
    axr.grid(alpha=0.25, which="both")

    fig.savefig(_OUT, dpi=200, bbox_inches="tight")
    print(f"wrote {_OUT}")

    res = cevns.reproduce_nucleus_fig1()
    print(f"mean ratio {res['mean_ratio']:.3f}, "
          f"max deviation {res['max_dev_from_mean']:.3f}, "
          f"slope {res['ratio_slope_per_decade']:+.3f}/decade")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
