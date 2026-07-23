# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Plan 11-01, Task 1: freeze the measured Ge vibrational density of states.

Writes, under ``data/external/ge_vdos/``:

* ``Ge_sg227_vdos_raw.csv``     -- the NCrystal ``Ge_sg227.ncmat`` VDOS exactly as the
  library reports it (425 uniformly spaced points, 3.7709-37.7897 meV), in the library's
  own arbitrary density units, NOT renormalized.
* ``ge_vdos_normalized.csv``    -- the headline normalized table: the raw grid PLUS the
  parabolic low-energy segment that NCrystal itself assumes below its first grid point,
  renormalized so that ``int g(omega) d(omega) = 1`` over the full support, g in 1/meV.
* ``Ge_pDoS.dat``               -- the DarkELF cross-check table, byte-for-byte as fetched.
* ``ge_vdos_darkelf_normalized.csv`` -- DarkELF renormalized under the SAME convention.

The parabolic segment is not an invention of this plan. NCrystal's own
``DI_VDOS.analyseVDOS()['integral']`` exceeds the trapezoid integral of the tabulated
points by exactly ``density[0] * egrid[0] / 3``, which is the integral of
``density[0] * (E/egrid[0])**2`` over ``[0, egrid[0]]``. That is recorded in the MANIFEST
as a measured fact, not asserted.

Run with /opt/anaconda3/bin/python3 (NCrystal 4.4.6 lives there; scipy is absent from the
gpd venv and is not needed here).
"""
import hashlib
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "external", "ge_vdos")

N_PARABOLIC = 800          # log-spaced points in the sub-egrid[0] parabolic segment
E_PARABOLIC_MIN_eV = 1e-12  # lower cut of that segment; the omitted [0, 1e-12] eV slab
                            # contributes < 1e-12 relative to any integral used here


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    import NCrystal as NC

    os.makedirs(OUT, exist_ok=True)
    info = NC.createInfo("Ge_sg227.ncmat;temp=293.6K")
    di = info.dyninfos[0]
    egrid = np.asarray(di.vdos_egrid_expanded, dtype=float)   # eV
    density = np.asarray(di.vdos_density, dtype=float)        # arbitrary units
    analysis = di.analyseVDOS()
    mass_amu = di.atomData.averageMassAMU()

    # --- raw dump -----------------------------------------------------------
    raw = os.path.join(OUT, "Ge_sg227_vdos_raw.csv")
    with open(raw, "w") as fh:
        fh.write("# Ge VDOS as reported by NCrystal %s from the bundled Ge_sg227.ncmat.\n"
                 % NC.__version__)
        fh.write("# Underlying measurement: G. Nelin and G. Nilsson, Phys. Rev. B 5, 3151 (1972).\n")
        fh.write("# Extraction: NCrystal.createInfo('Ge_sg227.ncmat;temp=293.6K')"
                 ".dyninfos[0].vdos_egrid_expanded / .vdos_density\n")
        fh.write("# Density units are NCrystal-internal and ARBITRARY; trapezoid integral over\n")
        fh.write("# the tabulated support = %.15e (not 1).\n" % np.trapz(density, egrid))
        fh.write("# The tabulated support starts at %.15e eV; NCrystal treats the VDOS as\n" % egrid[0])
        fh.write("# parabolic (g propto E^2) below that point -- see MANIFEST.md section 3.\n")
        fh.write("energy_eV,density_ncrystal_arb\n")
        for e, d in zip(egrid, density):
            fh.write("%.15e,%.15e\n" % (e, d))

    # --- normalized headline table -----------------------------------------
    lo = np.geomspace(E_PARABOLIC_MIN_eV, egrid[0], N_PARABOLIC, endpoint=False)
    e_full = np.concatenate([lo, egrid])
    d_full = np.concatenate([density[0] * (lo / egrid[0]) ** 2, density])
    norm = np.trapz(d_full, e_full)          # eV * (arb)
    g_full_per_eV = d_full / norm            # 1/eV
    g_full_per_meV = g_full_per_eV * 1e-3    # 1/meV  (g dE invariant => g_meV = g_eV*1e-3)

    normcsv = os.path.join(OUT, "ge_vdos_normalized.csv")
    with open(normcsv, "w") as fh:
        fh.write("# Ge vibrational density of states, NORMALIZED so that int g dw = 1 over\n")
        fh.write("# the full tabulated support, with w in meV and g in 1/meV.\n")
        fh.write("# Source: NCrystal %s bundled Ge_sg227.ncmat; measurement Nelin & Nilsson,\n"
                 % NC.__version__)
        fh.write("# Phys. Rev. B 5, 3151 (1972).\n")
        fh.write("# Support = [%.6e, %.9f] meV.  Rows %d..%d are the LOG-SPACED PARABOLIC\n"
                 % (E_PARABOLIC_MIN_eV * 1e3, egrid[-1] * 1e3, 1, N_PARABOLIC))
        fh.write("# segment g = g(w1)*(w/w1)^2 below the first NCrystal grid point w1 = %.9f meV;\n"
                 % (egrid[0] * 1e3))
        fh.write("# rows %d..%d are the NCrystal grid verbatim.\n"
                 % (N_PARABOLIC + 1, N_PARABOLIC + len(egrid)))
        fh.write("# Renormalization factor applied to the raw NCrystal density: 1/%.15e per eV,\n" % norm)
        fh.write("# i.e. the raw table integrated to %.15e eV*(arb) before renormalization.\n" % norm)
        fh.write("omega_meV,g_per_meV\n")
        for e, g in zip(e_full * 1e3, g_full_per_meV):
            fh.write("%.15e,%.15e\n" % (e, g))

    # --- DarkELF, same normalization convention -----------------------------
    dat = os.path.join(OUT, "Ge_pDoS.dat")
    de = np.loadtxt(dat)
    de_E, de_g = de[:, 0], de[:, 1]
    keep = de_E > 0                       # drop the E=0 row; g is identically 0 up to 2.4 meV
    de_E, de_g = de_E[keep], de_g[keep]
    de_norm = np.trapz(de_g, de_E)
    de_gn = de_g / de_norm * 1e-3
    decsv = os.path.join(OUT, "ge_vdos_darkelf_normalized.csv")
    with open(decsv, "w") as fh:
        fh.write("# Ge phonon DOS from DarkELF data/Ge/Ge_pDoS.dat, renormalized under the\n")
        fh.write("# SAME convention as ge_vdos_normalized.csv: int g dw = 1, w in meV, g in 1/meV.\n")
        fh.write("# Source file header: '# eV, DoS'. Raw trapezoid integral = %.15e (already ~1).\n"
                 % de_norm)
        fh.write("# Renormalization factor applied: 1/%.15e.\n" % de_norm)
        fh.write("# The E = 0 row of the source file is dropped (g is identically zero there and\n")
        fh.write("# g/E would be 0/0); the digitization carries NO support below %.6f meV, which\n"
                 % (de_E[np.nonzero(de_g)[0][0]] * 1e3))
        fh.write("# is why no parabolic segment is prepended here -- see MANIFEST.md section 3.\n")
        fh.write("omega_meV,g_per_meV\n")
        for e, g in zip(de_E * 1e3, de_gn):
            fh.write("%.15e,%.15e\n" % (e, g))

    facts = {
        "ncrystal_version": NC.__version__,
        "mass_amu": mass_amu,
        "egrid_min_eV": egrid[0],
        "egrid_max_eV": egrid[-1],
        "n_points": len(egrid),
        "spacing_eV": float(np.diff(egrid).mean()),
        "raw_trapz": float(np.trapz(density, egrid)),
        "analyse_integral": analysis["integral"],
        "parabolic_tail_analytic": float(density[0] * egrid[0] / 3.0),
        "analyse_msd": analysis["msd"],
        "analyse_debye_temp": analysis["debye_temp"],
        "darkelf_raw_integral": float(de_norm),
        "darkelf_max_eV": float(de_E[np.nonzero(de_g)[0][-1]]),
        "darkelf_spacing_eV": float(np.diff(de_E).mean()),
        "norm_factor": float(norm),
    }
    for k, v in facts.items():
        print("%-28s %r" % (k, v))
    print()
    for f in sorted(os.listdir(OUT)):
        p = os.path.join(OUT, f)
        if os.path.isfile(p):
            print("%s  %d bytes  %s" % (sha256(p), os.path.getsize(p), f))


if __name__ == "__main__":
    main()
