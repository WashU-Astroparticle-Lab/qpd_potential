// Minimal batch driver for the OFFICIAL, UNMODIFIED PARMA neutron routine.
//
// Frozen with the PARMA source cache (Plan 09-02, Task 1), following the
// data/external/nucleus/ pattern in which the in-plan converter is itself
// hashed into the MANIFEST.
//
// It links against the pinned-commit subroutines.cpp WITHOUT editing a single
// line of it and simply exposes getNeutSpecCpp() over a batch of energies, so
// that the decisive integrals of data/ambient_neutron_flux_v1.1.csv become
// recomputable in-repo (Phase-7 verification gap D2).
//
// LETHARGY DISCIPLINE (ROADMAP Phase 9 SC2, guard fp-lethargy-double-divide).
// Sato Eq. (6) is an ENERGY-WEIGHTED (lethargy-form) normalized spectrum.  The
// division by E happens EXACTLY ONCE, and it happens INSIDE PARMA's own
// getNeutSpecCpp at subroutines.cpp:673
//
//     getNeutSpec = Fl * (basic * geofactor + ther) / e;
//                                                    ^^^ the one and only /E
//
// so getNeutSpecCpp already returns the PER-ENERGY differential in
// cm^-2 s^-1 MeV^-1.  This driver does NOT divide again, and neither does
// src/qpd_potential/parma_neutron_flux.py.
//
// AXIS TAG: e is INCIDENT NEUTRON KINETIC ENERGY in MeV.  It is not a recoil
// axis; no recoil kinematics and no quenching appear anywhere here.
//
// usage:  cd <parma source root> && ./parma_neutron_driver s r d g < energies_MeV.txt
// stdin :  one energy in MeV per line
// stdout:  "<E_MeV> <dPhi/dE_n in cm^-2 s^-1 MeV^-1>" per line, 17 sig figs
//
// The relative input paths inside subroutines.cpp ("input/neutro/*.inp") mean
// the working directory MUST be the PARMA source root.
#include <cstdio>
#include <cstdlib>
#include <iostream>

double getNeutSpecCpp(double s, double r1, double d1, double g, double e);

int main(int argc, char **argv)
{
    if (argc != 5)
    {
        std::fprintf(stderr,
                     "usage: %s s_Windex r_c_GV d_gcm2 g_geom < energies_MeV\n",
                     argv[0]);
        return 2;
    }
    const double s = std::atof(argv[1]); // W-index (solar activity)
    const double r = std::atof(argv[2]); // vertical cut-off rigidity [GV]
    const double d = std::atof(argv[3]); // atmospheric depth [g/cm^2]
    const double g = std::atof(argv[4]); // local geometry (water weight fraction)

    double e;
    while (std::cin >> e)
    {
        // getNeutSpecCpp returns dPhi/dE_n [cm^-2 s^-1 MeV^-1] -- already
        // per-energy.  NO further division by e here.
        std::printf("%.17g %.17g\n", e, getNeutSpecCpp(s, r, d, g, e));
    }
    return 0;
}
