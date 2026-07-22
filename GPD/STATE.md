# Research State

## Project Reference

See: GPD/PROJECT.md

**Machine-readable scoping contract:** `GPD/state.json` field `project_contract`

**Core research question:** Reactor-CEvNS, cosmic-muon, and environmental-gamma Compton spectra in reconstructed energy for a 4"×4"×2mm single-sided Ge wafer read out by QPDs (Ta→Al and Al→Hf designs).
**Current focus:** Phase 1 complete ✓ — next: Phase 2 (Reactor Flux Model) and Phase 4 (Muon & Compton) can start

## Current Position

**Current Phase:** 7
**Current Phase Name:** Scenario & Nuclear-Data Lock
**Total Phases:** 12
**Current Plan:** none
**Total Plans in Phase:** none
**Status:** Phase complete — ready for verification
**Last Activity:** 2026-07-22

**Progress:** [██████████] 100%

## Active Calculations

None yet.

## Intermediate Results

None yet.

## Open Questions

- What crystal area is instrumented (one face vs all faces), fixing N_sens from the 1/mm^2 sensor density?
- [RESOLVED Phase 5] Saturated-regime reconstruction: non-paralyzable dead-time model (count-integral estimator; plateau = saturation). User decision 2026-07-21.
- [RESOLVED Phase 5] Ta->Al tunneling params: Table II Al-trap column; Ta absorber gap is a binary trapping gate (α-Ta ratio 3.58≥2), response numerically independent of it above the gate.
- What absolute environmental gamma flux and line composition best represent a surface-level reactor-site deployment? [Phase 4: sourced from Heusser 1995 with a factor-2 site-dependent band; edges exact, total rate MEDIUM.]

## Performance Metrics

| Label | Duration | Tasks | Files |
| ----- | -------- | ----- | ----- |
| Phase 01 P01-01 | 900s | 3 tasks | 8 files |
| Phase 01 P01-02 | 330s | 3 tasks | 4 files |
| Phase 02 P02-01 | 5400s | 3 tasks | 13 files |
| Phase 02 P02-02 | 3600s | 3 tasks | 9 files |
| Phase 03 P03-01 | 3600s | 3 tasks | 6 files |
| Phase 03 P03-02 | 2400s | 3 tasks | 7 files |
| Phase 04 P04-01 | 2700s | 3 tasks | 9 files |
| Phase 04 P04-02 | 2100s | 3 tasks | 10 files |
| Phase 04 P04-03 | 240s | 2 tasks | 5 files |
| Phase 05 P05-01 | 2700s | 3 tasks | 4 files |
| Phase 05 P05-02 | 2400s | 3 tasks | 6 files |
| Phase 06 P06-01 | 1500s | 3 tasks | 5 files |
| Phase 06 P06-02 | 360s | 3 tasks | 5 files |

## Accumulated Context

### Decisions

- [Phase 01-conventions-energy-scale-foundation]: Design->parameter mapping locked in code: Ta->Al uses Table II Aluminum column, Al->Hf uses Hafnium column; absorber supplies only Delta_abs.
- [Phase 01-conventions-energy-scale-foundation]: Hf tau_qp = 400 us adopted (caption/lit) over the 1 ms table cell, flagged MEDIUM.
- [Phase 01-conventions-energy-scale-foundation]: Ta absorber gap encoded as bulk alpha-Ta BCS assumption 0.68 meV (MEDIUM), film phase flagged for Phase 5.
- [Phase 01-conventions-energy-scale-foundation]: Saturation ordering fixed as the plateau Gamma_in Hf/Al ratio (3.17x); the 4.75x N_qp-per-eV ratio is the raw yield, not the saturation driver.
- [Phase 01-conventions-energy-scale-foundation]: Per-design saturation onset energies (~1.27 eV Al / ~0.77 eV Hf) carry the two-exponential peak factor p (0.25 Al / 0.13 Hf); Hf saturates first.
- [Phase 01-conventions-energy-scale-foundation]: E_rec estimator implemented as an explicit Phase-5 stub (NotImplementedError by default; linear_placeholder=True returns 0.5*E_dep, valid only in the unsaturated regime).
- [Phase 01-conventions-energy-scale-foundation]: Both censoring variants exposed as a switch at tau_d=40us; the paralyzable-vs-non-paralyzable choice is preserved OPEN as a Phase-5 blocker, not silently chosen.
- [Phase 02-reactor-flux-model]: Huber(235/239/241)+Mueller(238U) coefficients fetched from primary arXiv e-prints with provenance; reconstructed 235U within 0.73%/0.13% of published Huber at 3/5 MeV.
- [Phase 02-reactor-flux-model]: 238U(n,gamma) shape from sourced AME2020 Q-values, normalized to 0.6/fission (Kopeikin 2004).
- [Phase 02-reactor-flux-model]: Sub-1.8 MeV fission summation is a flagged seam-anchored non-negative placeholder pending Kopeikin-2012 grounding in 02-02; NOT invented, NOT truncated. Covered by the below-2-MeV uncertainty band (pre-anticipated ROADMAP risk).
- [Phase 02-reactor-flux-model]: Normalization chain R_f=P_th/<E_f>=9.10e19 fissions/s (3 GW_th, effective-thermal <E_f>=205.8 MeV Ma-2013 NOT total Q) x 1/(4 pi d^2) at d=2500 cm applied ONCE; int Phi dE=7.50e12 nu-bar/cm2/s, emission 1.96e20/s/GW_th (Hayes-Vogel ~2e20).
- [Phase 02-reactor-flux-model]: Frozen data/flux/reactor_flux_v1.0.csv with 7-col additive schema, SPLIT band (2-5% >2 MeV -> 20-25% <1.8 MeV, non-uniform), region flags, and version/git-sha/normalization/provenance/integral-check header.
- [Phase 02-reactor-flux-model]: Billard-2017 closure variant (HM constant below 2 MeV, fractions 55.6/32.6/7.1/4.7 isotope-labelled, no 238U<->239Pu swap) emitted as a distinct table (4.59e12) for the Phase-3 Billard Table-1 reproduction.
- [Phase 02-reactor-flux-model]: Sub-1.8 MeV shape kept as a Kopeikin-2012-cited placeholder (no machine-readable Kopeikin table sourceable; none fabricated), covered by the wide low-E band; limitation documented in CSV header, SUMMARY, and ASSUMPTIONS.md.
- [Phase 03-cevns-cross-section-rate]: Per-isotope exact kinematics: E_min^(i)(T)=(T+sqrt(T^2+2 M_i T))/2, T_max^(i)=2E_nu^2/(M_i+2E_nu); PCHIP log-flux interp + adaptive quad fold. sigma(72Ge,4MeV)=1.0026e-40 (0.26% from anchor); closed-form identity to <=6e-8.
- [Phase 03-cevns-cross-section-rate]: dR/dT = 67.8 counts/kg/day above 50 eV_nr at OUR 3 GW_th/25 m config — genuine physics (~90x Billard's 0.76 at 8.54 GW/400 m, matching the geometry/power ratio). >20% backtrack trigger NOT met; absolute Billard/CONUS+ comparison deferred to 03-02 via the k~=0.0111 rescale.
- [Phase 03-cevns-cross-section-rate]: Helm F^2 (Lewin-Smith): 0.9963 at 200 eV, 0.9639 at 2 keV endpoint; turning F off shifts integrated rate 0.38%. CONVENTIONS 'F^2>0.998' = dominant sub-200 eV regime; 0.964 = rare E_nu~8-10 MeV tail. Reconciled to avoid downstream misflag.
- [Phase 03-cevns-cross-section-rate]: Ge isotope abundances = IUPAC/CIAAW representative number fractions (MEDIUM); M_i=A*931.494 MeV; 73Ge axial term ~1/N^2 not modeled (stated assumption).
- [Phase 03-cevns-cross-section-rate]: Derived Billard renormalization k=(P_B/P_v)(d_v/d_B)^2: single-source (8.54 GW/400 m) 0.011120 vs two-core (4.27 GW at 355.39 & 468.76 m) 0.011092, agree 0.25%; k-rescaled Billard integral flux 5.10e10 nu cm^-2 s^-1. Both powers thermal (GW_th), distance squared (fp-gwe-gwth rejected).
- [Phase 03-cevns-cross-section-rate]: Billard 2017 Table 1 reproduced WITH k: 0.7415/0.5009/0.2567 counts/kg/day above 50/100/200 eV_nr vs 0.76/0.51/0.26 (-2.4/-1.8/-1.3%, all <2.5%, well inside ~20%). WITHOUT k the fold overshoots by exactly 1/k=89.9x (66.7/45.0/23.1). 100/200 eV bins <2% so no ROADMAP backtrack. Per-isotope Ge sum (fp-lumped-A-billard rejected).
- [Phase 03-cevns-cross-section-rate]: CONUS+ coarse factor-2 cross-check: flagship (67.75/kg/day >50 eV) and Billard Table 1 both rescaled to CONUS+ config (3.6 GW_th/20.7 m) give 118.6 vs 119.6, ratio 0.99. Two independently-normalized flux models agree at a common config. eV_ee quenching caveat -> coarse scale check only, MEDIUM confidence.
- [Phase 03-cevns-cross-section-rate]: Flux band propagation: rigorous 1-sigma band 3.4% (>=95 eV, matches well-anchored 2-5% high-E flux) rising to 6.2%/9.8% at 50/20 eV_nr; sub-1.8 MeV toggle localizes the placeholder systematic below ~95 eV (E_min(95 eV)~1.78 MeV): sub-1.8 rate fraction 17.8% at 50 eV, 33.8% at 20 eV, ~0 above 95 eV, T>200 eV unchanged <1e-3. The plan's 20-25% guess is corrected (finding, not a bug).
- [Phase 04-muon-compton-deposited-energy-spectra]: Muon dR/dE_dep folded from Gaisser-Guan flux (P1-P5 verbatim, arXiv:1509.06176) x analytic ray-box chord (Cauchy <ell>=0.385 cm reproduced to 0.03%) x Landau-Vavilov MPV. Integral rate 1.366 +/- 0.005 Hz (deterministic quadrature 1.415 Hz), within ~15% of PDG 1.5-2 Hz (VALD-02). Surface-flux measure I*A_proj*sin(theta) validated by J_horiz=pi*I_v/2 to 0.01%.
- [Phase 04-muon-compton-deposited-energy-spectra]: Landau-Vavilov MPV computed in code (not memorized): vertical-chord xi=0.0721 MeV (PDG 0.072), Delta_p=1.232 MeV strictly below mean 1.459 MeV. Custom Landau inverse-CDF sampler (mode -0.22278); deposit=Delta_p+xi*(lambda-lambda_mode) so sampled mode=Delta_p; NOT mean, NOT Moyal. kappa=xi/T_max<0.07 for all chords -> Landau/mild-Vavilov. Guards fp-mean-not-mpv.
- [Phase 04-muon-compton-deposited-energy-spectra]: Long near-horizontal chords importance-sampled (zenith uniform in [0,pi/2] with reweighting) so the deposit tail is resolved to ~197 MeV (66 bins >30 MeV) - the Phase-5 saturation input. Deposits on the unified phonon E_dep scale, NO quenching, no keVee/keVnr (electron recoil, zero Frenkel correction). Guards fp-angular-bias, fp-quenching-muon.
- [Phase 04-muon-compton-deposited-energy-spectra]: Compton dR/dE_dep built as a Klein-Nishina angle-sampled ELECTRON-recoil continuum (deposit T_e=E_gamma-E_prime, scattered photon escapes the optically-thin 2mm wafer; NO photopeaks) up to each self-validating edge E_edge=2E^2/(m_ec^2+2E). VALD-03 edges reproduced: 40K->1243.4, 208Tl->2381.8, 214Bi->1541.3 keV (max sampled T_e = E_edge per line, exact). No signal above the max edge or at E_gamma=2614.5. Guards fp-full-absorption, fp-electron-not-photon.
- [Phase 04-muon-compton-deposited-energy-spectra]: Total single-scatter Compton rate 0.268 Hz vs independent flux x sigma_KN x N_e anchor 0.273 Hz (ratio 0.983, within VALD-03 factor 2). Thin-target on the ONE pinned Cauchy mean chord ell_bar=4V/S=0.385 cm: mu*ell_bar=0.117@1MeV / 0.084@2MeV, double-scatter 1.4%; normal-incidence mu*t=0.061 quoted as optically-thin demo only. Same ell_bar in P, double-scatter, and rate. Energy closure to ~1e-5.
- [Phase 04-muon-compton-deposited-energy-spectra]: Gamma flux table is a DOCUMENTED TUNABLE input, not invented: line energies + DDEP emission probabilities = nuclear data; absolute flux anchored to cited LABChico EPJP2022 measured spectrum (40K 0.036, 208Tl 2614.5 0.0016 cm^-2 s^-1); Th siblings scaled by DDEP intra-chain ratios; U chain via documented Phi_U=Phi_Th assumption (factor-2 band). NIST XCOM Ge mu/rho frozen (4 cited points, log-log interp). Unified phonon scale, no quenching. Guards fp-invented-flux, fp-quenching-compton.
- [Phase 04-muon-compton-deposited-energy-spectra]: Muon and Compton deposited-energy spectra assembled on the byte-identical shared log E_dep grid (584 bins, 0.01 keV -> 197 MeV; np.array_equal True, max rel dev 0.0; centers = geometric means of shared_energy_grid() edges to 5e-7). Combined table data/combined_dRdEdep.csv (muon+Compton+total) and figs/phase4_deposited_spectra.png emitted; deposited (phonon) energy only, NO E_rec fold. Guards fp-grid-mismatch, fp-reconstructed-not-deposited.
- [Phase 04-muon-compton-deposited-energy-spectra]: Energy closure per channel: int dR/dE_dep dE = rate_Hz*86400/mass_kg (mass 0.1099 kg). Muon 1.0729e6 vs 1.0737e6 -> ratio 0.99928 (+/-3.6e-3 MC, 0.07% sub-grid-floor shortfall); Compton 2.1105e5 vs 2.1105e5 -> 0.99997; total-spectrum closure 0.9994. Rates parsed from CSV headers (1.3657 / 0.26846 Hz), not hard-coded. First-moment deposited power reported as a physical diagnostic (mean deposit muon 2.33 MeV > 1.46 MeV vertical, Compton 589 keV), explicitly not an independent number.
- [Phase 04-muon-compton-deposited-energy-spectra]: Pileup stop-condition: R_tot=1.634 Hz (muon 1.366 + Compton 0.268), occupancy R*tau=3.27e-5 (20us/50kHz sample) / 6.54e-5 (40us/25kHz resolving), R/50kHz=3.27e-5; non-paralyzable dead-time 6.5e-5, paralyzable live fraction 0.999935; mean interval 0.612 s ~ 1.5e4 resolving times. Occupancy << 1 -> stop-condition NOT triggered, quiescent reconstruction not precluded. Within-event muon ~197 MeV saturation flagged for Phase 5. Guards fp-pileup-unchecked.
- [Phase 05]: Count-integral estimator adopted (D-estimator): E_rec=C*sum N_obs with a single global per-design C fixed to slope 0.5; plateau IS the modeled saturation.
- [Phase 05]: Event-count mapping locked (Pitfall 1): expected_n_qp = INT Gamma_in dt = K*tau_qp*N_qp/V_tr (0.03x N_qp Al / 0.008x Hf), NOT the trapped count.
- [Phase 05]: Crossover reported as a band: default ~52.9 eV (Ta->Al) / ~32.1 eV (Al->Hf), equal-split anchor ~13.1/7.9 keV, whole-array plateau ~18.6/11.3 keV; Hf first.
- [Phase 05]: Muon-tail E_rec: non_paralyzable plateau ~35 keV (Ta->Al)/~27 keV (Al->Hf); paralyzable rollover ~3.3/~2.6 keV; both >3 orders below the linear line.
- [Phase 05]: Ta gap handled as a binary trapping gate (ratio 3.58>=2, T_c gate 2.5 K); response invariant to Delta_abs in alpha-phase; beta-Ta design-invalidating; no film value fabricated.
- [Phase 05]: Task 3 checkpoint:human-verify self-assessed satisfied pending orchestrator/researcher review (autonomous run); stop-condition does NOT trigger.
- [Phase 05]: R(E_rec|E_dep) built per design x both censoring variants by uniform log-E_dep importance sampling on the Phase-4 grid (584 cols, 10.14 eV->197 MeV, 80/decade); reuses Plan 05-01 response.py (no re-implementation).
- [Phase 05]: Aggregate off-spot ensemble (~10,287 sensors as one multinomial/Poisson draw per realization); on-spot ~pi r^2 sensors individual; per-class mean pinned to analytic censored_count so the response curve = the validated Plan 05-01 estimator.
- [Phase 05]: Feasibility split EC_EMG_MAX=2000: MUST-USE ref-qpd-repo EMG event train where feasible (CEvNS/low-E), deep-saturation registered-count Poisson (EMG train O(1e8) events infeasible; relative spread ~1e-3 there).
- [Phase 05]: Convergence: peak well-populated cell <=~1.8% at N_s=5000, clean 1/sqrt(N_s) scaling; columns normalize to 1; per-cell MC error stored; straddle-bins flagged. Stable crc32 sub-seeding => reproducible across processes.
- [Phase 05]: Muon-end E_rec: non_paralyzable plateau ~34.8 keV (Ta->Al)/~26.9 keV (Al->Hf); paralyzable rollover ~3.3/~2.6 keV; both ~3-4 orders below 0.5*E_dep (fp-no-saturation). Onset ~52.9/32.1 eV, plateau ~18.6/11.3 keV; Hf first.
- [Phase 05]: Time-over-saturation kept as a LABELED SECONDARY (tos_t_over_s), never auto-switched into the baseline (fp-tos-autoswitch); ceiling pile-up labeled an instrument artifact on the figure (fp-ceiling-peak).
- [Phase 05]: Task 3 checkpoint:human-verify self-assessed satisfied pending orchestrator/researcher review (autonomous run); Phase-5 stop-condition does NOT trigger.
- [Phase 05 / USER DECISION 2026-07-21]: **Censoring switch RESOLVED to non-paralyzable project-wide** (CONVENTIONS F closed). User accepted Phase 5 and chose non_paralyzable for the rest of the project after both variants were computed. params.DEFAULT_CENSORING already = "non_paralyzable"; Phase 6 + downstream use it as the single canonical variant. Paralyzable R matrices retained in response_matrix_*.npz as a sensitivity, not a live switch. Operative high-E response = the plateau (~34.8/26.8 keV muon tail).
- [Phase 06]: Fold conserves counts per channel per design: muon/Compton rel <=2.2e-16 (unit-sum R columns), CEvNS rel <=1.3e-16; CEvNS rebin total 9.6e-5 vs trapz, above-50-eV 67.67 vs 67.752 (0.12%).
- [Phase 06]: Reconstructed peaks (non-paralyzable): CEvNS ~42 eV (0.5*E_dep, sub-keV), muon 18.8/15.0 keV, Compton 16.8/13.3 keV (Ta->Al/Al->Hf); muon MeV deposits saturate to tens of keV (fp-deposited-only guarded).
- [Phase 06]: CEvNS 5-10.14 eV low edge retained (7.27 cts/kg/day) via exact E_rec=0.5*E_dep, not dropped (fp-drop-lowE-cevns); only R_non_paralyzable folded (fp-paralyzable-swap).
- [Phase 06]: deliv-fig-spectra rendered: dR/dE_rec vs E_rec (log-log, counts/kg/day/keV), CEvNS/muon/Compton + total, both designs, from the committed 06-01 CSVs; reconstructed axis not deposited (fp-deposited-only); non-paralyzable only, no paralyzable overlay (fp-paralyzable-swap).
- [Phase 06]: Saturation delimited on E_rec axis (fp-no-saturation-mark): onset (E_dep ~52.9/32.1 eV -> E_rec ~23/14 eV) + whole-array plateau (~18.6/11.3 keV E_dep -> ~4.1/2.5 keV E_rec) shaded; muon pile-up marked at 18.8/15.0 keV E_rec, inside the plateau band -> muon shown reconstructed entirely in saturation.
- [Phase 06]: Mapping panel reuses Phase-5 E_rec_median_non_paralyzable vs E_dep_centers (both designs) with the 0.5*E_dep calibration line + onset/plateau markers; not recomputed.
- [Phase 06]: ASSUMPTIONS.md finalized: censoring OPEN switch retired to RESOLVED non-paralyzable (CONVENTIONS F closed, USER 2026-07-21); Phase-4 gamma-background note + Phase-6 fold addendum added; four caveats + compact stage-1 results (Billard 2.4%, CEvNS ~68/kg/day >50 eV_nr dep, muon 1.37 Hz, pileup 3.3e-5); no live OPEN switch (fp-note-stale).
- [Phase 06]: Stage-1 milestone CLOSED by Plan 06-02.
- [Phase 0]: Started milestone v1.1: Neutron & Radiogenic Backgrounds — New milestone cycle — neutron NR (muon-induced/cosmogenic/radiogenic) + Ge-bulk & housing radioactivity in reconstructed energy
- [Phase 0]: v1.1 roadmap finalized: 6 phases (7-12), 11/11 objectives mapped — Critical path 7->8->9->10->12, Phase 11 parallel; three gating inputs handled via representative cited defaults + explicit band (fixed in Phase 7)
- [Phase 07-01]: Ambient fast-neutron flux LOCKED: PARMA/Sato-2015 shape (coefficients from official PARMA v4.10 source, compiled unmodified) + Gordon-2004 integral anchor k=1.096 -> Phi(10MeV-10GeV)=3.55e-3 cm^-2 s^-1, broad 1.32e-2; band [default/5, default] downward for building shielding — Gordon-2004 differential coefficients paywalled/unsourceable; USER DECISION 2026-07-22. PARMA native integral 3.24e-3 agrees with Gordon ~9% untuned (independent cross-check)
- [Phase 07-01]: Radiopurity budget + activation scenario LOCKED (t_exp=1yr, t_cool=0). FINDING: 68Ge/65Zn NOT saturated at 1yr (A=18.2/11.0 dec/kg/day, 61%/65% of R; full sat ~3yr); 3H non-saturating 4.05 dec/kg/day — Plan verify text had quoted ~30/~17 saturation values; as-deployed activity is the correct deliverable
- [Phase 07-02]: n-Ge elastic FROZEN thermal->fast, 23155-pt resonance-resolved union grid, zero NaN. Sub-MeV sigma_el filled from NJOY-2016.68 Lib80x ACE (HTTP-range extraction of 5 members, 11.8MB of a 7.05GB zip); ACE binaries gitignored, reproducible via committed fetcher+sha256 — MF3 MT2 is exactly zero across resolved+URR (sub-MeV sigma_el lives in File-2); openmc/NJOY unbuildable on osx-arm64. USER DECISION 2026-07-22: pre-reconstructed ACE
- [Phase 07-02]: LOCKED for CALC-06/08: sigma_tot(1-2MeV)=3.729 b, Sigma=0.1646 cm^-1, lambda=6.076 cm, P_int(2mm)=3.24%, endpoint natural 0.0536 (as-computed, NOT force-fit to 0.0538); 0.1-1 MeV band now 100% of nodes in 3-7 b (median 5.08 b) — sigma_tot drifted +2.4% (3.643->3.729 b) moving from MF3 MT1 background to ACE MT=1 pointwise; recorded, not silently absorbed
- [Phase 07-02]: RESIDUAL UNCERTAINTY: ACE baseline is 293.6 K vs a mK cryogenic target. Band integrals insensitive (2.5e-4%) but resonance LINE SHAPES differ materially (Ge-73 peak 9253.7 b at 0.1 K vs 8533.0 b at 293.6 K). Any downstream use resolving line shapes must switch to the .805nc (0.1 K) files — Doppler broadening is convolution with a normalized kernel so the integral is conserved; only line shape changes

### Active Approximations

None yet.

**Convention Lock:**

- Metric signature: not_applicable — no relativistic field theory in this detector/rate pipeline
- Fourier convention: not_applicable
- Natural units: internal-only (hbar=c=1) for CEvNS cross section; k_B EXPLICIT (not =1); I/O in eV/keV/MeV, counts/kg/day/keV, s, cm/um; (hbar c)^2 = 3.894e-28 GeV^2 cm^2
- Gauge choice: not_applicable
- Regularization scheme: not_applicable
- Renormalization scheme: tree-level SM (no loops); only scheme-dependent input is sin2thetaW = 0.2387 (low-energy MS-bar)
- Coordinate system: Cartesian wafer frame: x,y in-plane 4in x 4in face, z through 2mm thickness; sensors on one z-face
- Spin basis: not_applicable
- State normalization: not_applicable
- Coupling convention: CEvNS dsigma/dT = (G_F^2 M/4pi) Q_W^2 (1 - M T/2 E_nu^2) F^2(q^2); prefactor /4pi NOT /8pi; Q_W = N-(1-4 sin2thetaW)Z; sin2thetaW=0.2387 (low-E MSbar); 1-4sin2thetaW=0.0452; Helm F, F(0)=1
- Index positioning: not_applicable
- Time ordering: not_applicable
- Commutation convention: not_applicable
- Levi-Civita sign: not_applicable
- Generator normalization: not_applicable
- Covariant derivative sign: not_applicable
- Gamma matrix convention: not_applicable
- Creation/annihilation order: not_applicable

*Custom conventions:*
- Energy Scale Chain: single unified phonon scale, NO ionization quenching, for BOTH NR (CEvNS) and ER (muon/Compton): T=E_nr -> E_ph -> E_dep -> E_rec; E_ph=E_dep-E_stored(defects) (few-% NR-only, 0 for muons/Compton); E_rec(low-E)~=0.5*E_dep; FORBIDDEN: keVee/keVnr mixing, Lindhard/ionization quenching
- Detector Normalization: Ge 8.29e24 atoms/kg, rho=5.323 g/cm^3, M=72.63 g/mol; wafer 4inx4inx2mm=20.65 cm^3~=110 g, ~10300 sensors 1/mm^2 one face; reactor 3 GW_th (thermal) at 25 m => ~7-8e12 nubar/cm^2/s; adopt 110 g geometry but KEEP per-kg (counts/kg/day) normalization; '1 kg' framing in SUMMARY.md is STALE
- Efficiency Mapping: eps~=0.5 deposited-to-signal, imposed forward-model definition, SAME baseline both designs with +/-10-20% design-dependent band; Ta->Al and Al->Hf may split to per-design numbers in Phase 5; paper physical estimate eta_ce~=0.3 is an independent cross-reference, NOT baseline
- Bandwidth Censoring: LOCKED resolving time: 25 kHz max resolvable tunneling rate => 40 us (Nyquist from 50 kHz bw); 20 us at 50 kHz sampling itself (state both); paralyzable-vs-non-paralyzable AND merge-vs-drop kept as EXPLICIT CODE SWITCH (not fixed); OPEN QUESTION BLOCKS Phase 5; both variants must be implementable
- Cevns Benchmark Target: Phase-3 unit test: FULL Q_W => sigma(Ge,4 MeV)~=1.0e-40 cm^2 (canonical); N-only quick-check ~1.1e-40 cm^2 (1.08e-40, ~20% tol); coefficient sigma~=4.22e-45 N^2 (E_nu/MeV)^2 cm^2; closed form sigma_tot=G_F^2 Q_W^2 E_nu^2/4pi; PITFALLS.md ~1e-42 value is WRONG (100x)

### Propagated Uncertainties

None yet.

### Pending Todos

None yet.

### Blockers/Concerns

None

## Session Continuity

**Last session:** none
**Stopped at:** none
**Resume file:** none
**Last result ID:** none
**Hostname:** none
**Platform:** none
