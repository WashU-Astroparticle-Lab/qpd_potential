---
phase: 08-veto-envelope-geometry-gate-p-veto
plan: 2
plan_contract_ref: GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-02-PLAN.md#/contract
title: "The wafer's own muon rejection, derived and split: A_self_direct ~ 1 from the frozen chord-times-Landau spectrum, A_self_induced = 0 with its physical argument, eps_mult(N=1) = 0 as a counting identity, and f_dead ~ 3.9e-5 as a labelled lower bound"
date: 2026-07-22
status: complete
depth: full
completed: 2026-07-22
one_liner: "Derived the 110 g wafer's direct muon self-veto acceptance entirely from its own frozen 1e9-sample chord-times-Landau-Vavilov deposit distribution -- A_self_direct = 1.000000000000 at the 10.14 eV table floor, 0.999971887382 at 1 keV and 0.997858048250 at 100 keV, monotone non-increasing and bounded by 1 across a 400-point sweep -- on a denominator that reproduces the frozen header integral_muon_rate_Hz = 1.3659 Hz to -0.0485% (1.365237 Hz, gate V6, well inside the 1% criterion); kept that near-unity number rigorously separate from A_self_induced = 0.0, a named module constant carrying the argument that the wafer's only tagging handle is the parent muon's own deposit and that a neutron or bremsstrahlung gamma born in the surrounding Pb arrives with its parent nowhere near the wafer, with NUCLEUS's >99.8% sentence quoted verbatim from 08-01-SOURCE-EVIDENCE.md B.9 solely to show it is a muon-INDUCED background rejection and not a tagging efficiency and therefore has no transfer route -- and with the honest statement that zero is a defensible floor rather than an impossibility proof, since a secondary escorted into the wafer by its own parent would be tagged; established eps_mult(1) = 0.0 by an early-return counting identity asserted under exact identity comparison rather than a tolerance, cross-checked by showing the binomial-conditional occupancy model returns 0 at N = 1 for every p_hit in (0,1] so the identity does not depend on the model at all, while mult_rejection(18) > 0 is retained as a unit-test contrast only and no N = 18 number is written into the data table because it spans 0.083 to 0.9999 across p_hit = 0.01 to 0.5 and is therefore entirely model-driven; recorded NUCLEUS's own 'very marginal' assessment of the inner-veto-plus-single-hit requirement verbatim in both the module docstring and the CSV header with the plain statement that this makes the absolute cost of the wafer's zero multiplicity handle SMALL and thereby weakens this project's own framing; quantified the live-time cost as R_mu(2.92 m w.e.) = 1.3659/1.41 = 0.968723 Hz giving f_dead = 3.874894e-05 at 40 us and 1.937447e-05 at 20 us, labelled a first-order LOWER BOUND for two stated reasons (1.41 is an integral-flux factor while the angular distribution also hardens with depth, and CONVENTIONS F supplies a single-event resolving time rather than a muon-saturation veto window) with the separate note that A_self_direct is a ratio in which the normalization cancels exactly -- machine-verified by re-running the acceptance on a spectrum rescaled by 1/1.41 and recovering the identical value to 1e-12; carried Plan 08-01's verdict 'verified verbatim, arXiv:2509.03559v1 Sect. 4.1' into the R_mu row's source field and the f_dead docstring so neither the 1.41 attenuation factor nor the 2.92 m w.e. overburden appears without its status, together with the Sect. 4.1 nuance that the measured 2.9 +/- 0.1 m w.e. and the simulated 2.92 +/- 0.01 m w.e. are two different numbers; and verified by 36 passing tests plus recorded greps that neither 99.8 nor 0.998 is evaluated as a NUMBER token anywhere in the module, that no identifier or CSV column merges the two acceptances, and that no stale 04-01-SUMMARY path is used."
provides:
  - "src/qpd_potential/wafer_self_veto.py -- a_self_direct(E_cut) from the frozen artifact, A_SELF_INDUCED = 0.0 with its physical argument and honesty caveat, mult_rejection(n_channels) with the N = 1 early-return identity, r_mu_underground_Hz() and f_dead(tau) with the lower-bound label and the carried-anchor verdict, and emit_table()"
  - "data/wafer_self_veto.csv -- 57-line provenance header plus 8 rows (three A_self_direct thresholds, A_self_induced, eps_mult_N1, R_mu at 2.92 m w.e., f_dead at 40 us and 20 us), every row carrying its own definition, source and caveat; no N = 18 entry and no merged-acceptance row or column"
  - "tests/test_wafer_self_veto.py -- 36 tests covering V6 normalization closure, V7 acceptance limits and monotonicity, V8 multiplicity identity, the split invariant, the induced-zero argument, the no-transferred-percentage token guard, the counterpoint quotes checked verbatim against 08-01-SOURCE-EVIDENCE.md, and the dead-time bound"
contract_results:
  claims:
    claim-acceptance-split:
      status: passed
      summary: "The two acceptances are separate quantities everywhere and are never merged. In the module they are a function a_self_direct(E_cut) and a distinct module-level constant A_SELF_INDUCED, each with its own definition and its own docstring argument; in data/wafer_self_veto.csv they occupy four separate rows (three A_self_direct thresholds plus A_self_induced) with no summed, averaged or otherwise combined row, and no column that could be read as one. The structural test is deliberately run against identifiers and CSV quantity/column names rather than prose, because the module's own prose necessarily contains the sentence describing the prohibition; a raw text grep would flag the honesty statement itself. Every module attribute name and every CSV column and quantity name was checked against eight merged-acceptance patterns (combined/total/overall/lumped acceptance, a_self without a _direct or _induced suffix, a_self_total, a_self_combined, muon_veto_acceptance) with zero matches. The A_self_induced row's caveat opens 'NEVER SUM OR AVERAGE THIS WITH A_self_direct'."
      linked_ids: [deliv-self-veto-module, deliv-self-veto-table, test-split-reported, test-no-transferred-percentage, ref-evidence-block, ref-research-08]
    claim-direct-acceptance-derived:
      status: passed
      summary: "A_self_direct is derived exclusively from the wafer's own frozen chord-times-Landau-Vavilov deposit distribution data/muon_dRdEdep.csv (1e9 MC samples), as the ratio of the tail integral above E_cut to the full-range integral, both taken by trapezoid on the native log grid with no re-binning and with a single interpolated point inserted at E_cut so the partial first bin is exact rather than snapped to a grid node. Values: 1.000000000000 at the 1.014497e-02 keV (10.14 eV) table floor, 0.999971887382 at 1 keV, 0.997858048250 at 100 keV. Monotone non-increasing and bounded by 1 across a 400-point geomspace sweep from the floor to 100 keV (maximum step increase <= 1e-15, i.e. zero to floating point). The denominator was established first and gates everything else: the full-range trapezoid times m_wafer = 0.1099 kg (imported from wafer_geometry, CONVENTIONS D, not restated) divided by 86400 s/day gives 1.365237 Hz against the frozen header 1.3659 Hz, a deviation of -0.0485%. The near-unity result is the physically expected outcome and is stated as such: the vertical-chord Landau MPV is 1.2323 MeV, four to eight orders of magnitude above these thresholds, so the wafer is an excellent self-tagger for muons that cross it -- the half of the problem that was never the difficulty. The small departures from unity are statistically resolved rather than MC noise: the complement at 1 keV is 2.784e-05 against a propagated MC error of 1.20e-06 on the same integral (about 4%), and at 100 keV 2.115e-03 against 1.08e-05 (about 0.5%). They come from the genuine short-chord population (muons clipping a corner or an edge of the 0.20 cm slab), not from a numerical artifact."
      linked_ids: [deliv-self-veto-module, deliv-self-veto-table, deliv-self-veto-tests, test-normalization-closure, test-acceptance-monotone, ref-frozen-muon, ref-wafer-geometry]
    claim-induced-zero:
      status: passed
      summary: "A_SELF_INDUCED is a named module-level float equal to exactly 0.0 whose docstring carries the argument rather than only the value: the wafer's sole muon-tagging handle is the parent muon's own energy deposit in the wafer, and a neutron or bremsstrahlung gamma produced when a muon interacts in the surrounding lead reaches the wafer while its parent passes nowhere near it, so there is no coincident signal to tag it with. NUCLEUS's sentence is quoted verbatim from 08-01-SOURCE-EVIDENCE.md B.9 (arXiv:2509.03559v1 Sect. 5.2.1), with the phrase 'muon-induced' inside the quotation, and is immediately labelled as a rejection of muon-INDUCED secondary backgrounds rather than a muon tagging efficiency -- a different observable, earned by a 5 cm plastic-scintillator muon veto plus a six-crystal HPGe cryogenic outer veto surrounding gram-scale targets, neither of which a 110 g monolithic wafer has. It is explicitly stated to be quoted for identification and NOT applied. The honesty caveat is carried in the same docstring and into the CSV row: zero is the defensible FLOOR, not an impossibility proof, because a secondary accompanied into the wafer by its own parent muon would be tagged and that configuration is argued negligible here rather than measured; a referee could reasonably argue the wafer's 103.23 cm^2 face makes such accidental coincidences non-negligible."
      linked_ids: [deliv-self-veto-module, test-induced-zero-named, test-no-transferred-percentage, ref-evidence-block]
    claim-multiplicity-zero:
      status: passed
      summary: "mult_rejection(1) returns exactly 0.0 through an early return of the literal, and is asserted in the tests under identity comparison (== 0.0), not a tolerance. The counting argument is stated in the docstring alongside the verbatim NUCLEUS Sect. 5.1 selection sentence from 08-01-SOURCE-EVIDENCE.md B.2: with one and only one channel available to hit, conjunct (ii) 'a hit in one and only one of the target detectors' is satisfied identically by every event that triggers at all, so P(exactly one) == 1 and the cut removes nothing. A second, stronger check was added beyond the plan: the binomial-conditional occupancy model used for N > 1 itself returns 0 at N = 1 for every p_hit tested in (0, 1] -- N p (1-p)^0 / (1 - (1-p)) = p/p = 1 -- so the identity is model-independent and the early return agrees with, rather than substitutes for, the model. The N = 18 contrast is positive (0.375718 at the illustrative p_hit = 0.05) and is retained as a unit test only; the occupancy model is named explicitly in the docstring as 'independent per-channel firing with common probability p_hit, conditioned on at least one channel firing'."
      linked_ids: [deliv-self-veto-module, deliv-self-veto-tests, test-multiplicity-identity, ref-evidence-block, ref-research-08]
    claim-multiplicity-counterpoint:
      status: passed
      summary: "NUCLEUS's own assessment is recorded verbatim from 08-01-SOURCE-EVIDENCE.md B.7 (arXiv:2509.03559v1 Sect. 5.2.1) in three places -- the module docstring, the mult_rejection docstring, and the data-table header -- and a regression test compares the quoted string character-for-character against the evidence block itself so it cannot drift into paraphrase. The accompanying sentence states plainly that because the handle NUCLEUS gains from that cut is itself very marginal, the ABSOLUTE background cost of the wafer's identically-zero multiplicity handle is SMALL, and that this weakens this project's own 'we lose their multiplicity cut' framing rather than supporting it. Neither statement is softened: the rejection is exactly zero AND the consequence is small, reported together."
      linked_ids: [deliv-self-veto-module, deliv-self-veto-table, test-counterpoint-recorded, ref-evidence-block]
    claim-deadtime-cost:
      status: passed
      summary: "R_mu(2.92 m w.e.) = 1.3659 Hz / 1.41 = 0.968723 Hz, with the surface rate parsed from the frozen CSV header rather than typed, giving f_dead = 3.874894e-05 at tau_dead = 40 us and 1.937447e-05 at 20 us. Dimensions check: [Hz] x [s] is dimensionless, and both values are of order 1e-5 as expected. Both are labelled a first-order LOWER BOUND with both reasons stated in the docstring and in each CSV caveat: (1) 1.41 is an INTEGRAL-FLUX factor while the angular distribution also hardens with depth, changing the chord distribution and hence the deposit-spectrum shape, with Phase 15 owning the re-fold; (2) CONVENTIONS F supplies a single-event RESOLVING TIME rather than a muon-saturation veto window, and an MeV-scale deposit saturates the readout so the true post-muon window is plausibly considerably longer -- no muon-specific saturation study exists to fix it. The ratio-insensitivity of A_self_direct is stated separately and was machine-verified, not merely asserted: re-running the acceptance on a spectrum rescaled by 1/1.41 reproduces the identical value to 1e-12, so A_self_direct does not inherit this caveat while f_dead does. At R_mu*tau ~ 1e-5 the paralyzable and non-paralyzable forms are numerically indistinguishable, so the locked censoring choice is not load-bearing here and this is said explicitly."
      linked_ids: [deliv-self-veto-module, deliv-self-veto-table, test-deadtime-bounded, ref-conventions-f, ref-frozen-muon]
  deliverables:
    deliv-self-veto-module:
      status: passed
      path: src/qpd_potential/wafer_self_veto.py
      summary: "Contains a_self_direct(e_cut_keV) reading data/muon_dRdEdep.csv (the stale 04-01-SUMMARY paths appear only inside the explicit DO-NOT-EXIST warning, verified by a test that requires the warning within a 12-line window of any such mention); A_SELF_INDUCED = 0.0 with a docstring giving the parent-muon argument, the B.9 quote labelled not-applied, and the zero-is-a-floor caveat; mult_rejection(n_channels, p_hit) with the N = 1 early-return identity and the named occupancy model for N > 1; r_mu_underground_Hz() and f_dead(tau_dead_s) at 40 us and 20 us with the lower-bound label; integral_rate_Hz() performing the counts/kg/day -> Hz conversion exactly once with m_wafer imported from wafer_geometry; and emit_table(). The module docstring opens with the assertion that no NUCLEUS rejection percentage is applied as a computational value anywhere in it, and separately names the ~10,300-sensor QPD spatial handle as an explicitly uncredited future observable. Carries the project ASSERT_CONVENTION line."
      linked_ids: [claim-acceptance-split, claim-direct-acceptance-derived, claim-induced-zero, claim-multiplicity-zero, claim-multiplicity-counterpoint, claim-deadtime-cost, test-split-reported, test-induced-zero-named, test-no-transferred-percentage, test-multiplicity-identity, test-counterpoint-recorded, test-deadtime-bounded]
    deliv-self-veto-table:
      status: passed
      path: data/wafer_self_veto.csv
      summary: "A 57-line '#' provenance header following the data/muon_dRdEdep.csv pattern, followed by the columns quantity,value,units,definition,source,caveat and exactly 8 rows: A_self_direct_10eV, A_self_direct_1keV, A_self_direct_100keV, A_self_induced, eps_mult_N1, R_mu_2.92mwe, f_dead_tau40us, f_dead_tau20us. Every row carries a non-trivial definition, source and caveat. The 10 eV row's caveat states the table-floor situation explicitly. The R_mu row's source field reproduces Plan 08-01's verdict verbatim -- 'verified verbatim, arXiv:2509.03559v1 Sect. 4.1 (08-01-SOURCE-EVIDENCE.md E.1.1 overburden 2.92 +/- 0.01 m w.e.; E.1.2 attenuation 1.41 +/- 0.02)' -- and so do both f_dead rows, so no row uses either carried anchor without its status. The header records the normalization closure (1.365237 Hz vs 1.3659 Hz, -0.0485%, PASS), the NUCLEUS very-marginal counterpoint verbatim with the plain statement that it weakens this project's framing, the decision to omit any N = 18 value with the reason, and the uncredited ~10,300-sensor spatial handle. The file is regenerable and a test asserts the committed bytes match a fresh emit_table()."
      linked_ids: [claim-acceptance-split, claim-direct-acceptance-derived, claim-multiplicity-counterpoint, claim-deadtime-cost, test-split-reported, test-acceptance-monotone, test-counterpoint-recorded, test-deadtime-bounded]
    deliv-self-veto-tests:
      status: passed
      path: tests/test_wafer_self_veto.py
      summary: "36 tests, all passing, and the full repository suite still passes at 278/278 with no regressions. Covers V6 (normalization closure plus the locked-constant and correct-path checks), V7 (exactly 1 at the table floor, monotone non-increasing and bounded across a 400-point sweep, the three reported values pinned to 1e-9, out-of-range behaviour, and a scale-invariance check proving the acceptance is ratio-insensitive to the attenuation normalization), V8 (identity comparison at N = 1, model-independence of that identity across five p_hit values, positivity at N = 18 across four p_hit values, input validation, and the absence of any N = 18 row in the CSV), plus the split invariant, the induced-zero argument, the token-level no-transferred-percentage guard, verbatim-quote regression against 08-01-SOURCE-EVIDENCE.md, the dead-time bound and label checks, the carried-anchor verdict check, and the uncredited-spatial-handle check."
      linked_ids: [claim-direct-acceptance-derived, claim-multiplicity-zero, test-normalization-closure, test-acceptance-monotone, test-multiplicity-identity, test-no-transferred-percentage]
  acceptance_tests:
    test-normalization-closure:
      status: passed
      summary: "PASS. Trapezoidal integration of the dRdEdep_cts_per_kg_day_keV column over the full tabulated E_dep range on the native log grid gives 1073307.591365 counts/kg/day; times m_wafer = 0.1099 kg divided by 86400 s/day gives 1.365237 Hz against the frozen header integral_muon_rate_Hz = 1.3659 Hz, a deviation of -0.0485%, well inside the 1% criterion. The residual is consistent with the trapezoid rule's discretization on an 80-bins-per-decade log grid; it was NOT rescaled away, and the acceptance denominator is the computed integral rather than the header value. The test also pins the header value itself, so if the benchmark artifact ever changes the gate fails rather than silently re-basing. m_wafer is asserted to be the same object as wafer_geometry.MASS_KG, and SECONDS_PER_DAY == 86400.0."
      linked_ids: [claim-direct-acceptance-derived, deliv-self-veto-tests, ref-frozen-muon]
    test-acceptance-monotone:
      status: passed
      summary: "PASS. a_self_direct(table_floor) == 1.0 under exact equality, and a_self_direct(0.010 keV) == 1.0 as well because 10 eV sits marginally below the 1.014497e-02 keV floor -- reported as edge-of-support rather than extrapolated, since the frozen distribution carries no probability mass below the floor to lose. Across a 400-point geomspace sweep from the floor to 100 keV every value is <= 1 and >= 0, and the maximum forward difference is <= 1e-15, i.e. monotone non-increasing to floating point. The three reported values are 1.000000000000, 0.999971887382 and 0.997858048250, quoted to twelve digits precisely so any departure from unity is visible rather than rounded to '1'. The ordering a(10 eV) >= a(1 keV) >= a(100 keV) is asserted, and a separate assertion requires a(1 keV) > 0.999 as the named disconfirming check for a units error."
      linked_ids: [claim-direct-acceptance-derived, deliv-self-veto-tests, deliv-self-veto-table]
    test-split-reported:
      status: passed
      summary: "PASS. Every module attribute name, every CSV column name and every CSV quantity name was matched against eight merged-acceptance regexes; zero matches. The CSV has exactly three A_self_direct rows and one A_self_induced row, with no duplicate quantity names, and the column set is exactly quantity,value,units,definition,source,caveat. Every row's definition, source and caveat exceed 20 characters and every value parses as a float. A methodological note is recorded: the check is structural rather than a raw text grep, because the module and the CSV header both contain the sentence describing the prohibition ('fp-lumped-acceptance', 'never merged'), so a naive prose grep would flag the honesty statement itself. A separate test asserts each CSV value equals the corresponding live module computation, so the table cannot drift from the code."
      linked_ids: [claim-acceptance-split, deliv-self-veto-module, deliv-self-veto-table]
    test-induced-zero-named:
      status: passed
      summary: "PASS (automated portion; the hybrid human-review portion is discharged by the recorded docstring text). A_SELF_INDUCED exists as a module-level float and equals exactly 0.0. Its docstring block was extracted from the source and asserted to contain: the phrase 'muon-induced', an explicit reference to evidence-block entry B.9, the phrase 'tagging efficiency' distinguishing the two observables, the phrase 'not applied', the physical mechanism ('parent muon' and the surrounding lead), and the honesty caveat ('floor', 'impossibility proof'). The corresponding CSV row was checked for the same distinction and the same floor caveat, plus the B.9 citation and the NOT-applied label in its source field."
      linked_ids: [claim-induced-zero, deliv-self-veto-module, ref-evidence-block]
    test-no-transferred-percentage:
      status: passed
      summary: "PASS. The module was tokenized with the Python tokenize module and every NUMBER token collected; neither 99.8 nor 0.998 appears among them, i.e. neither is ever evaluated as a computational value. Tokenizing is used in preference to a raw grep because it draws exactly the line the contract asks for: a number inside a docstring or comment is a STRING or COMMENT token and is correctly excluded, while any number the interpreter would evaluate is caught. The single textual occurrence of '99.8' in the file is inside the A_SELF_INDUCED docstring, within the verbatim B.9 quotation, and a second test requires an explicit 'not applied' statement within 25 lines of any such occurrence -- satisfied. data/wafer_self_veto.csv contains neither literal at all (grep -c returns 0). A further check confirms no module-level numeric constant has a name matching rejection/efficiency/factor apart from MU_ATTENUATION_VNS, that the literal 18 appears at most once as a NUMBER token (the channel COUNT, a geometry fact from 08-01 A.4/A.5), and no bare factor-5 rejection constant exists."
      linked_ids: [claim-acceptance-split, claim-induced-zero, deliv-self-veto-module, deliv-self-veto-tests]
    test-multiplicity-identity:
      status: passed
      summary: "PASS. mult_rejection(1) == 0.0 under exact identity comparison and returns a float; mult_rejection(18) = 0.375718 > 0 under the illustrative occupancy, and remains positive at p_hit = 0.01, 0.05, 0.2 and 0.5. The docstring states the counting argument, names the occupancy model as 'independent per-channel firing with common probability p_hit, conditioned on at least one channel firing', and keeps that model clearly separate from the N = 1 identity, which was additionally shown not to depend on it (zero at N = 1 for p_hit = 0.001, 0.05, 0.3, 0.9 and 1.0). No N = 18 value appears in data/wafer_self_veto.csv: the row was OMITTED by decision, which the contract permits, with the reason recorded in the CSV header. The justification is quantitative -- the N = 18 value ranges from 0.083 at p_hit = 0.01 to 0.9999 at p_hit = 0.5, more than an order of magnitude, so the number is entirely a function of an occupancy model this phase does not derive and would read as a NUCLEUS efficiency if published beside the wafer's own quantities. A forward guard is in place: if a future edit adds any row mentioning 18, the test requires the labels 'illustrative', 'model-dependent' and 'not a NUCLEUS' in its caveat."
      linked_ids: [claim-multiplicity-zero, deliv-self-veto-module, deliv-self-veto-tests]
    test-counterpoint-recorded:
      status: passed
      summary: "PASS (automated portion; the human-review portion is discharged by the recorded text below). The B.7 'very marginal' sentence is present in the module docstring, in the mult_rejection docstring and in the CSV header, each with the Sect. 5.2.1 attribution and the B.7 evidence-block reference. A regression test flattens whitespace and asserts the quotation appears character-for-character in both the module docstring and the CSV, and independently asserts the same string is present in 08-01-SOURCE-EVIDENCE.md, so any future paraphrase drift fails the suite. The framing sentence is present in both places: the CSV header states that the absolute background cost of the wafer's identically-zero multiplicity handle is SMALL and that this 'weakens this project's' argument; the module docstring says the same and adds that it is reported for that reason rather than despite it. The Sect. 5.1 selection quote is likewise verified verbatim against the evidence block (modulo the module rendering LaTeXML's 'CE \\nu NS' as 'CEnuNS' for readability, which the test accounts for explicitly)."
      linked_ids: [claim-multiplicity-counterpoint, deliv-self-veto-module, deliv-self-veto-table, ref-evidence-block]
    test-deadtime-bounded:
      status: passed
      summary: "PASS. R_mu = 0.968723 Hz, matching the required approximately 0.969 to within 5e-4, and equal to frozen_header_rate_Hz()/1.41 to 1e-12. f_dead = R_mu x tau exactly, dimensionless as [Hz] x [s], and of order 1e-5 at both resolving times: 3.874894e-05 at 40 us and 1.937447e-05 at 20 us, both asserted inside (1e-6, 1e-4). TAU_DEAD_RESOLVE_S == 40e-6 and TAU_DEAD_SAMPLE_S == 20e-6 are pinned against CONVENTIONS F. The f_dead docstring is asserted to contain 'LOWER BOUND', 'integral-flux factor' (reason 1), 'saturates the readout' (reason 2), 'Phase 15' and the explicit statement that a_self_direct 'does NOT inherit this caveat'; the a_self_direct docstring is asserted to carry the RATIO-INSENSITIVITY section, so the two caveats are stated separately rather than conflated. Both f_dead CSV rows carry the LOWER BOUND label, the RESOLVING TIME distinction and the integral-flux reason. Plan 08-01's carried-anchor verdict was read and is reproduced: every CSV row whose source mentions 1.41 or 2.92 is required to contain all three fragments 'verified verbatim', '2509.03559v1' and 'Sect. 4.1', and the R_mu row additionally cites E.1.1 and E.1.2; the same fragments are asserted present in the f_dead docstring. The anchor is therefore VERIFIED rather than NOT-FOUND, and it is visible as such in the data table rather than silently adopted."
      linked_ids: [claim-deadtime-cost, deliv-self-veto-module, deliv-self-veto-table]
  references:
    ref-frozen-muon:
      status: completed
      completed_actions: [read, use, compare]
      missing_actions: []
      summary: "Read as the sole source of both the acceptance numerator and denominator; used without re-running the Monte Carlo; and compared against its own header value, which is the V6 gate. The header rate 1.3659 Hz, the vertical-chord MPV 1.2323 MeV and the mean 1.4585 MeV all appear in the module and the emitted table. The header rate is PARSED from the file rather than hard-coded, so a change to the frozen artifact surfaces as a test failure instead of a silent inconsistency."
    ref-wafer-geometry:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "Read and used as the source of truth for the wafer mass: M_WAFER_KG is bound directly to wafer_geometry.MASS_KG (0.1099 kg, CONVENTIONS D) and a test asserts the identity, so the geometry constants are not restated by hand anywhere in this plan. The chord distribution itself was not re-sampled -- it is already baked into the frozen deposit spectrum -- consistent with the contract's exclusion of a Monte Carlo re-run."
    ref-conventions-f:
      status: completed
      completed_actions: [read, cite]
      missing_actions: []
      summary: "Read and cited as the source of tau_dead. Both locked values are carried and reported: 40 us (25 kHz Nyquist resolving time) and 20 us (50 kHz sampling interval), with the non-paralyzable censoring lock of 2026-07-21 named. The section's own framing is what licenses the lower-bound label: it supplies a single-event resolving time, not a muon-saturation veto window. It is also noted that at R_mu*tau ~ 1e-5 the paralyzable and non-paralyzable forms are numerically indistinguishable, so the censoring lock is not load-bearing for this quantity."
    ref-evidence-block:
      status: completed
      completed_actions: [read, cite]
      missing_actions: []
      summary: "Read in full and cited as the only source for every NUCLEUS sentence used: B.2 (the Sect. 5.1 selection criterion including the single-hit conjunct), B.7 (the very-marginal assessment), B.9 (the >99.8% muon-induced rejection sentence with 'muon-induced' inside the quotation), and A.4/A.5 (the 18-target Chooz count). No sentence was taken from memory or a summarizer. Two regression tests compare the quoted strings character-for-character against the evidence-block file itself. Also read and carried: the E.1.1/E.1.2 carried-anchor verdicts and the two-overburden nuance."
    ref-research-08:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "Read (read-only; 08-RESEARCH.md is owned by Plan 08-03 in this wave and was not edited). Used: F4's acceptance decomposition is the definition implemented for a_self_direct and A_SELF_INDUCED; F3's multiplicity identity is implemented as the N = 1 early return; Pitfall 2 (>99.8% is not a tagging efficiency) is the argument recorded in the A_SELF_INDUCED docstring; Pitfall 9's stale-path correction is applied and unit-tested; Pitfall 10's instruction that the ~10,300-sensor spatial handle stay uncredited is honoured in both the module docstring and the CSV header. The Sect. F1 round-2 retraction of the orientation-invariant fit lemma was noted and respected -- no geometric fit reasoning appears in this plan, which is Plan 08-03's scope."
  forbidden_proxies:
    fp-veto-credit-transfer:
      status: rejected
      notes: "Rejected structurally, not merely by intention. No NUCLEUS rejection percentage is evaluated as a value anywhere in the module: a tokenize-based test collects every NUMBER literal and asserts neither 99.8 nor 0.998 is among them, and no bare factor-5 rejection constant exists. The single textual occurrence of the >99.8% figure sits inside the A_SELF_INDUCED docstring, inside the verbatim B.9 quotation, explicitly labelled as a NUCLEUS number that is NOT applied -- and its purpose there is precisely to establish that it is a muon-INDUCED background rejection rather than a tagging efficiency, i.e. not even the same observable. The only NUCLEUS numeral used computationally is the channel count 18, which is a geometry fact, and it is used only inside a unit-test contrast whose value is never published."
    fp-lumped-acceptance:
      status: rejected
      notes: "Rejected. No function, constant, CSV column or CSV row merges A_self_direct with A_self_induced by summing, averaging or any other operation; the structural test scans identifiers and table names against eight merged-acceptance patterns and finds none. The A_self_induced row's caveat opens with 'NEVER SUM OR AVERAGE THIS WITH A_self_direct'. The reason is recorded in the module docstring: the near-unity direct acceptance would mask the zero induced acceptance, and the class NUCLEUS's vetoes actually suppress is exactly the class the wafer cannot touch."
    fp-multiplicity-softening:
      status: rejected
      notes: "Rejected. The multiplicity rejection is stated as exactly zero, returned as a literal 0.0 by an early return and asserted under identity comparison rather than a tolerance. The words 'small', 'marginal' and 'reduced' are never applied to the rejection itself. They ARE applied, correctly and separately, to its CONSEQUENCE: NUCLEUS's own very-marginal assessment means the absolute background cost of the zero handle is small. The two statements are kept distinct in the text so the zero is not softened by proximity to the counterpoint."
    fp-spatial-handle-credit:
      status: rejected
      notes: "Rejected. The ~10,300 QPD sensors at 1/mm^2 are named in both the module docstring and the CSV header as a genuinely different observable with no established efficiency and no design behind it, explicitly NOT CREDITED ANYWHERE IN v2.0, with a stated prohibition on using it to fill the multiplicity gap. No numeric credit of any kind is attached to it anywhere in the module, the tests or the table."
  uncertainty_markers:
    weakest_anchors:
      - "tau_dead is the locked single-event resolving time (40 us / 20 us, CONVENTIONS F), not a muon-saturation veto window; an MeV-scale deposit saturates the readout so the real post-muon window is plausibly considerably longer, making both f_dead values lower bounds by an unquantified factor"
      - "The 1.41 +/- 0.02 omnidirectional attenuation factor is an integral-flux factor while the angular distribution also hardens with depth; A_self_direct is machine-verified ratio-insensitive to it, but f_dead is not and inherits the full first-order caveat"
      - "arXiv:2509.03559v1 Sect. 4.1 states TWO overburden values -- the simulated map average 2.92 +/- 0.01 m w.e. and the measured cosmic-wheel 2.9 +/- 0.1 m w.e. that the 1.41 factor is said to correspond to; both are verified verbatim but they are not the same measurement, and this plan pairs 1.41 with the 2.92 label as the project contract does"
      - "The 10 eV acceptance is evaluated at the edge of the frozen artifact's support (table floor 1.014497e-02 keV = 10.14 eV), so the exact 1.0 there is a statement about the artifact's range and not an independent physical measurement below 10 eV"
    unvalidated_assumptions:
      - "That every muon crossing the wafer produces a deposit drawn from the frozen chord-times-Landau distribution, with no separate population of grazing or delta-ray-dominated events treated differently"
      - "That A_self_induced is exactly zero rather than merely negligible -- a muon-induced secondary accompanied into the wafer by its own parent would be tagged, and this configuration is argued negligible rather than measured or simulated"
      - "That the illustrative binomial-conditional occupancy model is an adequate stand-in for NUCLEUS's real 18-crystal hit multiplicity; it is not derived here, which is exactly why no value from it enters the data table"
      - "That the trapezoid rule on the native 80-bins-per-decade log grid is adequate for the tail integrals; supported by the -0.0485% closure of the full-range integral against the frozen header, but not independently convergence-tested at a second resolution because the artifact is frozen and may not be re-gridded"
    competing_explanations:
      - "A referee could argue the wafer's large 103.23 cm^2 face makes accidental parent-plus-secondary coincidences non-negligible, raising A_self_induced slightly above zero; the honest response is that zero is the defensible floor, not that the effect is impossible"
      - "The 2.1e-03 complement of A_self_direct at 100 keV could in principle be a low-energy artifact of the frozen MC rather than a genuine short-chord population; the propagated MC error on that complement is 1.08e-05, about 0.5% of it, so the departure from unity is statistically resolved and this explanation is disfavoured"
      - "One could argue the multiplicity handle should be credited to the wafer via QPD spatial reconstruction rather than being zero; this is explicitly refused here as fp-spatial-handle-credit, and recorded as a future direction with no efficiency attached"
    disconfirming_observations:
      - "If the frozen CSV integral had failed to reproduce 1.3659 Hz within 1% the acceptance denominator would have been invalid and every acceptance number blocked; it reproduced to -0.0485%, so this check did not fire"
      - "If a_self_direct had come out materially below 1 at 1 keV it would have contradicted the 1.23 MeV vertical MPV and indicated a units error; it returned 0.999971887382, so this check did not fire"
      - "If mult_rejection(1) had returned a nonzero value it would have indicated the counting argument was implemented as a probability model rather than an identity; it returns exactly 0.0 by early return, and the model was separately shown to agree, so this check did not fire"
      - "A future re-freeze of data/muon_dRdEdep.csv with a different header rate will fail test_v6_normalization_closure_reproduces_frozen_rate by design, rather than silently re-basing the acceptance denominator"
comparison_verdicts:
  - subject_id: claim-direct-acceptance-derived
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-frozen-muon
    comparison_kind: benchmark
    metric: relative_error
    threshold: "<= 0.01"
    verdict: pass
    recommended_action: "Carry A_self_direct forward to Phase 16's L2-off baseline as the wafer's only DERIVED muon rejection; do not pair it with any inherited veto credit."
    notes: "Acceptance denominator computed from the frozen artifact = 1.365237 Hz against the artifact's own header integral_muon_rate_Hz = 1.3659 Hz; relative deviation 4.85e-4, i.e. -0.0485%, inside the 1% pass condition. The residual is trapezoid discretization on the 80-bins-per-decade log grid and was not rescaled away."
  - subject_id: claim-deadtime-cost
    subject_kind: claim
    subject_role: supporting
    reference_id: ref-conventions-f
    comparison_kind: baseline
    metric: order_of_magnitude
    threshold: "1e-6 < f_dead < 1e-4"
    verdict: pass
    recommended_action: "Treat f_dead as a lower bound in any live-time budget; a muon-saturation study is needed before it can be quoted as the definitive loss."
    notes: "f_dead = 3.874894e-05 at 40 us and 1.937447e-05 at 20 us against the plan's expected order 1e-5, with R_mu = 0.968723 Hz against the expected approximately 0.969 Hz."
---

# Plan 08-02 Summary — The wafer's own muon rejection, derived and split

## The one-sentence result

The wafer self-tags essentially every muon that crosses it (`A_self_direct` = 1.000000000000 / 0.999971887382 / 0.997858048250 at 10 eV / 1 keV / 100 keV) and tags **none** of the muon-induced secondaries born in the surrounding lead (`A_self_induced` = 0.0) — and those are two different numbers about two different populations, which is exactly why NUCLEUS's ">99.8%" cannot be inherited.

## Key results

| Quantity | Value | Basis |
|---|---|---|
| Denominator closure (gate V6) | 1.365237 Hz vs frozen header 1.3659 Hz, **−0.0485%** | trapezoid on native log grid × 0.1099 kg / 86400 s |
| `A_self_direct` @ 10 eV | 1.000000000000 | at the 10.14 eV table floor — edge of support, stated not extrapolated |
| `A_self_direct` @ 1 keV | 0.999971887382 | complement 2.784e−05 ± 1.20e−06 (MC) |
| `A_self_direct` @ 100 keV | 0.997858048250 | complement 2.115e−03 ± 1.08e−05 (MC) |
| `A_self_induced` | **0.0** exactly | no parent-muon handle; floor, not impossibility proof |
| `eps_mult(N=1)` | **0.0** exactly | counting identity, early return, identity-compared |
| `eps_mult(N=18)` | 0.375718 — **illustrative, model-dependent, unit test only** | binomial-conditional occupancy, p_hit = 0.05 (arbitrary) |
| `R_mu(2.92 m w.e.)` | 0.968723 Hz | 1.3659 Hz / 1.41, anchor **verified verbatim, Sect. 4.1** |
| `f_dead(40 µs)` | 3.874894e−05 | **first-order LOWER BOUND** |
| `f_dead(20 µs)` | 1.937447e−05 | **first-order LOWER BOUND** |

`[CONFIDENCE: HIGH]` for `A_self_direct` — three independent checks: the denominator reproduces an independently computed benchmark (the frozen header rate), the value is bounded and monotone across a 400-point sweep, and it is consistent with the independent physical expectation from the 1.2323 MeV MPV against eV-to-100-keV thresholds. A fourth, weaker check is the MC-error resolution of the complements.

`[CONFIDENCE: HIGH]` for `eps_mult(1) = 0` — it is a counting identity, verified two independent ways (early return, and the occupancy model reducing to zero at N = 1 for every p_hit).

`[CONFIDENCE: MEDIUM]` for `A_self_induced = 0` — the argument is sound but the "exactly zero rather than negligible" step is argued, not measured. Accidental parent-plus-secondary coincidences are the unchecked failure mode. Zero is the defensible floor.

`[CONFIDENCE: LOW]` for `f_dead` as an absolute live-time loss — it is a lower bound with two unquantified upward corrections (depth-hardening shape change; readout saturation lengthening the true veto window). `[CONFIDENCE: HIGH]` only for the statement that it is *at least* ~4e−5.

## Conventions in effect

| Convention | Value | Source |
|---|---|---|
| Energy scale | unified phonon `E_dep`, **no** ionization quenching | CONVENTIONS §B |
| Wafer mass | 0.1099 kg, imported from `wafer_geometry.MASS_KG` | CONVENTIONS §D |
| Geometry | 10.16 × 10.16 × 0.20 cm; chord distribution frozen, not re-sampled | CONVENTIONS §D |
| Resolving times | 40 µs (25 kHz Nyquist) and 20 µs (50 kHz sampling), non-paralyzable | CONVENTIONS §F |
| Units | `E_dep` in keV; counts/kg/day → Hz conversion performed **exactly once** | plan frontmatter |

The project-wide `ASSERT_CONVENTION` line is carried on both new source files; all QFT categories are `not_applicable`, matching the existing modules in `src/qpd_potential/`.

## Two things that cut against the project's own framing

Both are required outputs, not concessions:

1. **NUCLEUS call the multiplicity cut "very marginal."** Quoted verbatim from `08-01-SOURCE-EVIDENCE.md` §B.7 in the module docstring and the CSV header. The wafer's multiplicity rejection is exactly zero — but because the handle NUCLEUS gains from that cut is itself very marginal, the **absolute background cost of losing it is small**. That weakens the "we lose their multiplicity cut" argument.
2. **`A_self_direct` ≈ 1 is the easy half.** The wafer being an excellent self-tagger for through-going muons is the physically expected outcome of a 1.2323 MeV MPV against eV-scale thresholds. It is not an achievement and it does not offset `A_self_induced` = 0. Reporting it alone would be `fp-lumped-acceptance` in effect if not in form.

## Methodological decisions made and documented (no checkpoints raised)

- **N = 18 row omitted from the CSV.** The contract permits either omission or an `illustrative — model-dependent` label. Omission was chosen because the value spans 0.083 → 0.9999 as `p_hit` runs 0.01 → 0.5 — more than an order of magnitude — so it carries essentially no information beyond "positive". A forward guard in the test suite requires the full illustrative labelling if any future edit adds such a row.
- **Partial-bin interpolation at `E_cut`.** A single interpolated point is inserted at the cut rather than snapping to the nearest grid node, so the acceptance is a smooth function of `E_cut` and the monotonicity test probes the physics rather than the grid. No re-binning of the frozen artifact occurs.
- **Structural rather than textual split test.** The module and the CSV header both *describe* the prohibition on merging the acceptances, so a raw prose grep for "combined/total acceptance" would flag the honesty statement itself. The test therefore scans identifiers, CSV columns and CSV quantity names.
- **Tokenize rather than grep for the percentage guard.** `tokenize` distinguishes a NUMBER token (a computational value) from a STRING token (a docstring quotation) exactly as the contract's pass condition requires.

## Deviations

None of Rules 1–6 was triggered. Two Rule-4-flavoured additions were made inline as correctness items and are noted here rather than as deviations: the partial-bin interpolation above, and a `_trapz` alias so the module works under both `numpy.trapz` (1.26, the installed version) and `numpy.trapezoid` (≥ 2.0).

## Verification evidence

- `pytest tests/test_wafer_self_veto.py` → **36 passed**.
- `pytest tests/` → **278 passed**, no regressions.
- `grep -n "data/muon/\|src/muon/"` on the module and CSV → only the explicit DO-NOT-EXIST warning lines.
- `grep -n "99\.8\|0\.998"` on the module → one hit, line 183, inside the B.9 quotation in the `A_SELF_INDUCED` docstring; on the CSV → 0 hits.
- Regeneration check: `python -m qpd_potential.wafer_self_veto` reproduces `data/wafer_self_veto.csv` byte-for-byte (asserted in the suite).

## Reproducibility

- Python 3.11.7, numpy 1.26.4, scipy 1.17.1, pytest (repo default), macOS/Darwin 25.3.0.
- No random numbers are drawn by this plan. The frozen artifact's own MC seed and 1e9 sample count are recorded in its header and were not re-run.
- Regenerate the table with `PYTHONPATH=src python3 -m qpd_potential.wafer_self_veto`.

## Notes for downstream phases

- Phase 15 owns the angular re-fold of the muon spectrum at 2.92 m w.e.; `f_dead` should be recomputed there, and `A_self_direct` re-checked for the *shape* change (the normalization cancellation already verified here does not cover it).
- Phase 16's L2-off baseline may carry `A_self_direct` as the wafer's only derived muon-rejection number. It may **not** carry `A_self_induced` as anything other than 0, and it may not merge the two.
- One item for the phase owner, reported rather than edited (08-RESEARCH.md is Plan 08-03's file this wave): §F4 writes the `A_self_direct` denominator as `∫₀^∞`, whereas the frozen artifact's support starts at 10.14 eV. The implementation integrates over the tabulated range and states the floor explicitly; §F4's notation is idealised, not wrong, but a reader could take it as licence to extrapolate below the floor.
