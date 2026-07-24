The format of the files in this director are:

Each line represents an individual cascade realization for a capture. Each number in the line is defined as follows:

(total fraction): the absolute fraction that this cascade represents in this capture sample

(symbol for post-capture nucleus): like 71Ge represents the final nucleus after the capture

(A value for post-capture nucleus): This is redundant for now

(vector of the energy levels): these are the energy levels AFTER the neutron separation energy.

(vector of level lifetimes): these are the lifetimes in attoseconds of each intermediate level

Here is an example:


0.000671	29Si	29	[4840.4	0.0]	[3500	100000000000000]

Here, this cascade is meant to be simulated with an overall fraction of 0.07%. The capture happens
on 28-Si and proceeds with two emitted gammas. First a gamma is emitted by the difference
between the neutron separation energy and the 4840.4 keV. The next gamma is emitted between the
4840.4 level and the ground state. 

## A Note on Estimation in Levelfiles

If the lifetime of the state was not available, then the Weisskopf estimate for an electric dipole was used.
This generally gives shorter lifetimes than found experimentally.
The dipole is chosen because it is the lowest allowed multipolarity for the transitions calculated
because this leads to underestimation instead of overestimation of the half-lives.
Calculating a lifetime that is too large would eliminate aspects of the spectrum if it prevents decay-in-flight,
while calculating one that is too small will increase the probability of decay-in-flight,
changing the probabilities of some energy readings occurring,
but will not affect what energies can be read in the first place.

[Weisskopf, V. F. Radiative Transition Probabilities in Nuclei. September 1951. Physical Review. Vol83 I5 P1073--1073.](https://link.aps.org/doi/10.1103/PhysRev.83.1073)