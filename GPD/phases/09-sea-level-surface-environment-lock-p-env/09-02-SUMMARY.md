---
phase: 09-sea-level-surface-environment-lock-p-env
plan: 02
plan_contract_ref: GPD/phases/09-sea-level-surface-environment-lock-p-env/09-02-PLAN.md#/contract
title: "Phase-7 gap D2 closed: PARMA frozen at its pinned commit, both anchor integrals and the committed table recomputed in-repo, and Phi_th delivered as a named quantity"
date: 2026-07-22
status: complete
depth: full
completed: 2026-07-22
tasks_completed: 3
tasks_total: 3
one_liner: "Retrieved and integrity-checked the sea-level neutron source rather than recalling it, and closed the Phase-7 verification gap D2 that the Phase-7 verifier called the weakest reproducibility link in that phase: the official PARMA C++ source was pulled at the PINNED mirror commit 6ff37cacb8cf003e2fc269963f9a08f812407264 by a recorded curl (archive SHA-256 ee95687f..., 1390611 B), validated as real source by three independent gates (file type, archive hash, discriminating strings getNeutSpecCpp x2 / the A(1)..A(12) header / EXPACS x6), compiled UNMODIFIED, and driven by a committed module -- giving, in the plan's required order, UNTUNED FIRST Phi(10 MeV-10 GeV) = 3.238744e-3 cm^-2 s^-1 (-0.008% vs the committed native 3.239e-3, 0.0000% change on node doubling 200->400/decade) which sits -8.77% from the Gordon midpoint with NO fitting, then ANCHORED Phi = 3.549986e-3 (-0.0004%), an independently solved k = 1.096104 (+0.0004% vs the committed 1.09610), and Phi(0.01 eV-10 GeV) = 1.317379e-2 (+0.029%); the JOINT identity D2 said had never been performed -- driver vs data/ambient_neutron_flux_v1.1.csv on its own 584 bin centres -- returns median AND max relative deviation 3.88e-6 with zero bins above 1%, a uniform offset that is exactly the rounding of k (exact 1.0961043 vs recorded 1.09610), so the ADVERSE reading that the table was produced by a path its header does not describe is excluded by evidence rather than assumed away; the lethargy division by E is shown to happen EXACTLY ONCE, inside PARMA's own subroutines.cpp:673, proved by INT phi dE == INT (E phi) dlnE to <0.0001% across five well-separated decades; all four canonical ground-level features are present with the thermal peak of phi(E) at 0.0250 eV = PARMA's E_th = kT at 293.6 K and the lethargy peak at 0.0507 eV = the analytic 2 E_th; and Phi_th = 2.767075e-3 cm^-2 s^-1 over 0.01 eV -> 0.5 eV (cadmium cutoff, stated with its number) is emitted as a named, strictly positive scalar on a sub-eV table deliberately kept OFF shared_energy_grid() so Phase 10 is not serialized -- with every emitted quantity carrying accuracy_label = order_of_magnitude at its point of definition and phi_lo = phi_default/5 held out as INDOOR attenuation that is explicitly NOT an error bar for an unshielded surface wafer."
provides:
  - "data/external/parma/MANIFEST.md -- frozen PARMA cache on the data/external/nucleus pattern: pinned commit, verbatim curl command with its observed HTTP status and content type, 13 artifact rows with byte counts, SHA-256 and per-artifact integrity verdicts, the three gates used to separate real source from an HTML challenge page, the checked (not assumed) U+2009 caveat, the Sato-as-shape / Gordon-as-integral-anchor role split, and the exact location of the single lethargy division"
  - "data/external/parma/fetch_parma.sh -- re-runnable retrieval that FAILS LOUDLY on a magic-byte or SHA-256 mismatch and cmp-verifies the committed coefficients against the freshly retrieved tree"
  - "data/external/parma/neutro_coefficients/ -- the ten input/neutro coefficient files, COMMITTED, being the part the Sato-2015 article does not tabulate"
  - "data/external/parma/parma_neutron_driver.cpp -- batch shim linking the unmodified pinned subroutines.cpp; frozen and hashed with the cache"
  - "src/qpd_potential/parma_neutron_flux.py -- the committed driver that closes D2, with the evaluation point (s, r_c, d, g) and the anchor scalar k as explicit named parameters and every return carrying its accuracy label"
  - "data/ambient_neutron_thermal_v2.0.csv -- 201-node sub-eV differential flux with Phi_th, its stated bounds, its cutoff convention and order_of_magnitude on every single row"
  - "GPD/phases/09-.../09-02-NEUTRON-DECLARATION.md -- the neutron channel declaration: roles, range, normalization basis, the source's own accuracy vs this project's, band semantics, thermal disposition, the two quantified Phase-13 omissions, and the directional-bias row"
  - "tests/test_ambient_neutron_flux.py -- 19 executable checks covering cache integrity, both anchor integrals in the required order, the joint identity, the lethargy identity on five decades, the four-feature morphology, band semantics, and the order-of-magnitude labelling"
contract_results:
  claims:
    claim-neutron-provenance-real:
      status: passed
      summary: "The recorded provenance of data/ambient_neutron_flux_v1.1.csv resolves to actually-retrievable primary artifacts. The PARMA source at the pinned commit 6ff37cacb8cf003e2fc269963f9a08f812407264 was retrieved by one recorded curl (HTTP 200, application/x-gzip, 1390611 B), frozen with SHA-256 ee95687f3c61488ee05e246788215e5321e00962896986fd0a587d94e831ef08, and its ten input/neutro coefficient files are present and committed. Real source was separated from an HTML error or challenge page by THREE independent gates, all recorded: file type (gzip / C++ source text / ASCII), archive SHA-256, and discriminating strings (getNeutSpecCpp 2 hits in subroutines.cpp, the A(1)..A(12) coefficient header in fitting-lowspec.inp, EXPACS 6 hits in the mirror README, which itself states the mirror is copied from the official JAEA EXPACS homepage). Sato 2015 PLOS ONE e0144679 is recorded as the open-access SHAPE source and Gordon 2004 strictly as the >10 MeV INTEGRAL anchor, with the paywall statement present in the MANIFEST, the declaration AND the driver docstring. No WebFetch and no LLM page summary was used for anything in this cache. The U+2009 thin-space hazard was CHECKED rather than assumed: a byte scan of subroutines.cpp, fitting-lowspec.inp and README.md found zero bytes above 0x7F in all three."
      linked_ids: [deliv-parma-cache, deliv-neutron-declaration, test-cache-integrity, test-shape-vs-anchor-roles, ref-parma-source, ref-parma-paper, ref-gordon, ref-neutron-artifact]
    claim-anchor-reproducible:
      status: passed
      summary: "Both decisive integrals are now recomputable in-repo from committed code, and so is the committed table's own phi_default column -- Phase-7 gap D2 is CLOSED, not carried. Reported in the plan's required order because the order is the point. UNTUNED (k = 1): Phi(10 MeV-10 GeV) = 3.238744e-3 cm^-2 s^-1 at 200 nodes/decade against the committed native 3.239e-3, a deviation of -0.008% (tolerance 2%), with the value stable to 3.238751 / 3.238744 / 3.238743 / 3.238742 e-3 at 100 / 200 / 400 / 800 nodes per decade so the node-doubling change is 0.0000% (tolerance 0.5%). That untuned spectrum sits at -8.77% from the Gordon midpoint WITH NO FITTING -- the only independent validation this channel possesses, and it is reported before any rescale. ANCHORED (k = 1.09610): Phi = 3.549986e-3 (-0.0004%, tol 1%); the independently solved k = 1.096104 (+0.0004%, tol 1%); Phi(0.01 eV-10 GeV) = 1.317379e-2 (+0.029%, tol 5%). JOINT IDENTITY: evaluating the driver at the committed table's own 584 E_n_center_keV values gives median AND max relative deviation 3.88e-6, with 0 bins above 1% and 0 above 5%. The deviation being UNIFORM is reported rather than waved through and is explained quantitatively: (1.0961043 - 1.09610)/1.09610 = 3.9e-6, i.e. the committed table was generated with the unrounded k. LETHARGY: the single division by E lives at data/external/parma/src/subroutines.cpp:673 inside PARMA's own getNeutSpecCpp, and neither the C++ shim nor the Python driver repeats it; proved by INT phi dE == INT (E phi) d(lnE) agreeing to <0.0001% on 0.01-0.1 eV, 1-10 eV, 1-10 keV, 1-10 MeV and 100-1000 MeV. One recorded trap: PARMA's s argument is the W-INDEX, not the force-field potential -- subroutines.cpp:20 converts internally via 370 + 0.3 s^1.45 MV -- and the routine's own inline comment saying otherwise is stale."
      linked_ids: [deliv-parma-driver, deliv-neutron-tests, deliv-neutron-declaration, test-native-integral, test-anchored-integral, test-table-joint-identity, test-lethargy-once, ref-neutron-artifact, ref-gordon, ref-phase7-verification]
    claim-thermal-named:
      status: passed
      summary: "Phi_th is delivered on branch (a): a named, strictly positive scalar, not a gap and never zero. Phi_th = 2.767075e-3 cm^-2 s^-1 integrated from the PARMA low-energy floor 1.0e-8 MeV (0.01 eV, the floor the committed v1.1 header itself quotes) to 5.0e-7 MeV, adopting the standard CADMIUM CUTOFF of 0.5 eV and stating that number explicitly as the plan's agent-discretion clause requires. It is 21.00% of the broad Phi(0.01 eV-10 GeV) = 1.317379e-2. Cutoff sensitivity is reported because the convention is a choice: 0.4 eV -> 2.7283e-3, 0.5 eV -> 2.7671e-3 (adopted), 1.0 eV -> 2.8983e-3, i.e. <~5%, far inside the channel's own accuracy label. The accompanying table data/ambient_neutron_thermal_v2.0.csv spans 0.01 eV - 1 eV at 100 nodes/decade on a grid that is DELIBERATELY not shared_energy_grid(); that independence is now tested by SPACING (ratio 10^(1/100) vs the shared grid's ~79.99 bins/decade) rather than by span, because Phase 10 landed the two-decade downward extension mid-plan and 'below the shared floor' stopped being a valid test of independence. Spectral morphology confirms all four canonical ground-level features and none is assumed: the thermal peak of phi(E) sits at 0.0250 eV, which is exactly PARMA's E_th = 2.5e-8 MeV = kT at 293.6 K (0.0253 eV), while the same feature in the LETHARGY representation E*phi peaks at 0.0507 eV = the analytic 2 E_th -- both were computed and the apparent discrepancy with the conventional '~0.03 eV' was resolved by derivation rather than by loosening a threshold. The 1/E epithermal plateau is flat to a factor 1.390 over 1 eV-10 keV, the evaporation hump is at 1.957 MeV and the cascade peak at 118.9 MeV. A caveat is handed forward with the number rather than buried: PARMA's thermal term is a 293.6 K free-gas ambient Maxwellian and its adequacy against a mK cryogenic target is unvalidated."
      linked_ids: [deliv-thermal-table, deliv-neutron-declaration, test-thermal-named, test-spectral-morphology, ref-parma-paper, ref-neutron-artifact]
    claim-band-and-label:
      status: passed
      summary: "phi_default = phi_hi (outdoor sea level) is stated as the operative normalization for an unshielded surface wafer, and phi_lo = phi_default/5 is stated to represent INDOOR/building attenuation and to be explicitly NOT an error bar for this configuration. This was verified structurally rather than by assertion: over all 584 bins of the committed table phi_hi == phi_default to rtol 1e-12 and phi_lo == phi_default/5 to rtol 1e-6. No code path in this plan uses phi_lo or a band midpoint as a central value, and data/ambient_neutron_thermal_v2.0.csv emits no phi_lo column at all -- asserted by a column-count check. The consequence is stated in the declaration in the plain terms the plan demands: using phi_lo would cut the neutron background by a factor 5 and improve S/B by the same factor, the single largest available flattering move in this phase. Every emitted neutron quantity carries accuracy_label = order_of_magnitude at its point of definition -- the module constant, the NeutronFlux dataclass default, the thermal_flux() metadata, the sub-eV table's header AND every one of its 201 data rows, and each row of the declaration's quantity tables -- and the declaration states that no downstream acceptance test may demand better. Both carried truncation omissions are recorded and quantified for Phase 13: the 20 MeV ENDF/B-VIII.0 sigma_el ceiling (Phase-7 gap D1, truncate-and-document by user decision 2026-07-22, not to be extrapolated), and the ~197 MeV shared-grid ceiling above which 21% of the >10 MeV flux lies -- with the note that CALC-24's Phase-7 deferral rationale (shield attenuation making the tail unimportant) is VOID at the surface, so the omission is a larger fraction here than under the now-void premise."
      linked_ids: [deliv-neutron-declaration, deliv-neutron-tests, test-band-semantics, test-oom-label, ref-neutron-artifact]
  deliverables:
    deliv-parma-cache:
      status: passed
      path: data/external/parma/MANIFEST.md
      summary: "13 artifact rows with byte count, SHA-256 and an integrity verdict each; the verbatim curl command with its observed http/type/size; the three-gate method for distinguishing real source from an HTML challenge page; the recorded environment; the checked U+2009 caveat; the Sato-shape / Gordon-integral-anchor role split with the paywall statement; the build command with its exit status and the note that not one line of subroutines.cpp was edited; and the exact file:line of the single lethargy division. Bulk (tarball, extracted tree, binary) is gitignored and reproducible via the committed fetch_parma.sh, which fails loudly on any hash or magic-byte mismatch; the ten coefficient files are committed."
      linked_ids: [claim-neutron-provenance-real, test-cache-integrity, ref-parma-source]
    deliv-parma-driver:
      status: passed
      path: src/qpd_potential/parma_neutron_flux.py
      summary: "Builds and invokes the pinned PARMA neutron routine unmodified, returning dPhi/dE_n on a caller-supplied grid. The evaluation point (s_windex, rc_gv, d_gcm2, g_geom) and the anchor scalar k are explicit named parameters with the Phase-7 values as defaults, not buried constants. Returns a frozen NeutronFlux dataclass carrying accuracy_label, axis_tag, shape_source, norm_anchor and the lethargy_division_site string, so a caller cannot obtain a neutron number without its provenance and its order-of-magnitude tag. Raises ParmaBuildError carrying the exact failing command and stderr rather than substituting a number. Also emits the sub-eV table, so that artifact is regenerable by one recorded command."
      linked_ids: [claim-anchor-reproducible, test-native-integral, test-anchored-integral, test-table-joint-identity, test-lethargy-once]
    deliv-thermal-table:
      status: passed
      path: data/ambient_neutron_thermal_v2.0.csv
      summary: "201 nodes, 0.01 eV - 1 eV at 100/decade. Header names Phi_th = 2.767075e-3 cm^-2 s^-1 with its exact integration bounds, the cadmium-cutoff convention, the axis tag, the shape-vs-anchor split, the evaluation point, the lethargy-division site, the explicit statement that this grid is NOT shared_energy_grid() and why, and ACCURACY_LABEL = order_of_magnitude; every one of the 201 data rows carries order_of_magnitude in its own accuracy_label column. Both the anchored and the untuned columns are emitted; no phi_lo column exists."
      linked_ids: [claim-thermal-named, test-thermal-named, test-spectral-morphology]
    deliv-neutron-declaration:
      status: passed
      path: GPD/phases/09-sea-level-surface-environment-lock-p-env/09-02-NEUTRON-DECLARATION.md
      summary: "Citation and roles with the paywall statement; energy range and normalization basis; the source's own claimed accuracy separated from this project's, with an explicit section explaining that the 1e-5..1e-3-level agreement of every check is a REPRODUCIBILITY result and not an accuracy result; unambiguous band semantics with the factor-5 S/B consequence; the order-of-magnitude label attached per quantity; the thermal disposition; both Phase-13 omissions quantified with the voided CALC-24 rationale noted; a completed directional-bias row; and the no-shielded-quantity statement with its executed check."
      linked_ids: [claim-neutron-provenance-real, claim-anchor-reproducible, claim-thermal-named, claim-band-and-label, test-shape-vs-anchor-roles, test-band-semantics, test-oom-label]
    deliv-neutron-tests:
      status: passed
      path: tests/test_ambient_neutron_flux.py
      summary: "19 tests, all green. Tolerances are module constants stated BEFORE the checks ran and were not loosened afterwards. Covers cache integrity including on-disk-vs-MANIFEST hashes for all ten coefficient files, the shape-vs-anchor role split across three files, the untuned integral with node-doubling convergence, the anchored integral and the solved k, the broad integral, the pointwise joint identity, the lethargy identity parametrized over five decades, the four-feature morphology, Phi_th's naming/positivity/bounds, the table-vs-driver agreement to 1e-6, band semantics checked structurally over all 584 bins, the order-of-magnitude labelling, and the shielded-token scan. A loud skip guard names the exact fetch command if the frozen source is absent and states plainly that a skip is NOT a pass."
      linked_ids: [claim-anchor-reproducible, claim-thermal-named, claim-band-and-label]
  acceptance_tests:
    test-cache-integrity:
      status: passed
      summary: "Pinned commit resolved; HTTP 200 with content-type application/x-gzip and 1390611 bytes; archive SHA-256 recorded and re-verifiable. Every frozen artifact has a retrieval command, byte count, SHA-256 and an integrity verdict of real source. The ten input/neutro coefficient files named in the committed CSV header are present AND committed, and the test recomputes each of their on-disk SHA-256 values and requires it to appear in the MANIFEST. An HTML body under HTTP 200 would have been flagged FAILED by the file-type gate in fetch_parma.sh; it did not occur."
      linked_ids: [claim-neutron-provenance-real, deliv-parma-cache, ref-parma-source]
    test-shape-vs-anchor-roles:
      status: passed
      summary: "MANIFEST, declaration and driver docstring all name Sato/PARMA as the differential SHAPE source and Gordon strictly as the >10 MeV INTEGRAL anchor, and all three carry the explicit paywall sentence. The driver's own dataclass defaults encode it too: shape_source contains 'Sato', norm_anchor contains 'Gordon' and the substring 'gt10MeV_only', so the role split cannot be read the other way round from the code."
      linked_ids: [claim-neutron-provenance-real, deliv-neutron-declaration, ref-gordon, ref-parma-paper]
    test-native-integral:
      status: passed
      summary: "k = 1: Phi(10 MeV-10 GeV) = 3.238744e-3 cm^-2 s^-1 vs 3.239e-3, -0.008% (tolerance 2%). Node density 100/200/400/800 per decade gives 3.238751 / 3.238744 / 3.238743 / 3.238742 e-3, so the doubling change is 0.0000% (tolerance 0.5%). Reported BEFORE the rescale, and the test additionally asserts the untuned-vs-Gordon offset lies in (-15%, 0%) so a tuned value could not masquerade as the untuned cross-check."
      linked_ids: [claim-anchor-reproducible, deliv-parma-driver, deliv-neutron-tests, ref-neutron-artifact, ref-gordon]
    test-anchored-integral:
      status: passed
      summary: "k = 1.09610: Phi = 3.549986e-3 vs the Gordon midpoint 3.550e-3, -0.0004% (tol 1%). Independently solved k = 1.096104, +0.0004% vs the committed 1.09610 (tol 1%) -- a real check rather than a tautology because the native integral it divides comes from the recompiled pinned source, not from the committed header. Phi(0.01 eV-10 GeV) = 1.317379e-2 vs 1.317e-2, +0.029% (tol 5%)."
      linked_ids: [claim-anchor-reproducible, deliv-parma-driver, deliv-neutron-tests, ref-neutron-artifact, ref-gordon]
    test-table-joint-identity:
      status: passed
      summary: "THE D2 closure. Driver evaluated at all 584 E_n_center_keV values of data/ambient_neutron_flux_v1.1.csv and compared pointwise to phi_default_cm2_s_MeV: median relative deviation 3.88e-6 (tol 1%), max relative deviation 3.88e-6 at E_n = 0.0170327 keV (tol 5%), 0 bins above 1%, 0 above 5%. The uniformity of the deviation is reported and explained as the rounding of k rather than smoothed over, which is what actually excludes the adverse reading."
      linked_ids: [claim-anchor-reproducible, deliv-parma-driver, deliv-neutron-tests, ref-neutron-artifact, ref-phase7-verification]
    test-lethargy-once:
      status: passed
      summary: "INT phi dE vs INT (E phi) d(lnE) on five well-separated decades -- 0.01-0.1 eV (thermal), 1-10 eV (epithermal), 1-10 keV, 1-10 MeV (evaporation), 100-1000 MeV (cascade) -- agree to <0.0001% in every case (tolerance 1%). A systematic factor of E or 1/E, which is what a zero or double division would produce, is absent. The single division site is named in the MANIFEST, the declaration, the driver header and the C++ shim."
      linked_ids: [claim-anchor-reproducible, deliv-parma-driver, deliv-neutron-tests]
    test-thermal-named:
      status: passed
      summary: "Branch (a) satisfied. data/ambient_neutron_thermal_v2.0.csv exists; its header names Phi_th with a parseable value 2.767075e-3, its exact bounds 1.0e-8 -> 5.0e-7 MeV, its cadmium-cutoff convention and units; the value is strictly positive and retrievable programmatically via thermal_flux(); the table is explicitly declared not to be on shared_energy_grid() and the independence is verified by grid spacing. No named-gap branch was needed."
      linked_ids: [claim-thermal-named, deliv-thermal-table, deliv-neutron-declaration]
    test-spectral-morphology:
      status: passed
      summary: "All four canonical features located on driver output spanning 0.01 eV - 10 GeV: thermal peak of phi(E) at 0.0250 eV (= PARMA E_th = kT at 293.6 K; the same feature in E*phi peaks at 0.0507 eV = analytic 2 E_th, and the relation was derived rather than a tolerance widened), 1/E epithermal plateau flat to a factor 1.390 over 1 eV-10 keV (requirement: within ~2), evaporation hump at 1.957 MeV (1-3 MeV), cascade peak at 118.9 MeV (~100 MeV). The test additionally requires at least three interior extrema in E*phi, so a monotone or feature-free spectrum fails."
      linked_ids: [claim-thermal-named, deliv-parma-driver, deliv-neutron-tests]
    test-band-semantics:
      status: passed
      summary: "Structural, not textual: over all 584 committed bins phi_hi == phi_default (rtol 1e-12) and phi_lo == phi_default/5 (rtol 1e-6). The declaration states phi_default = phi_hi operative, phi_lo indoor-only and explicitly not an error bar, and names the factor-5 S/B consequence. No code path uses phi_lo; the sub-eV table has no phi_lo column, checked by column count."
      linked_ids: [claim-band-and-label, deliv-neutron-declaration, deliv-neutron-tests, ref-neutron-artifact]
    test-oom-label:
      status: passed
      summary: "accuracy_label = order_of_magnitude verified at every point of definition: the module constant, the NeutronFlux dataclass default, the thermal_flux() metadata dict, the sub-eV table header AND all 201 data rows, and >=5 occurrences across the declaration's quantity tables. The declaration states that no downstream acceptance test may demand better. Both carried omissions are present and quantified (20 MeV ENDF ceiling; 21% of the >10 MeV flux above ~197 MeV)."
      linked_ids: [claim-band-and-label, deliv-neutron-declaration, deliv-thermal-table, deliv-neutron-tests]
  references:
    ref-neutron-artifact:
      status: completed
      completed_actions: [read, use, compare]
      missing_actions: []
      summary: "The full comment header of data/ambient_neutron_flux_v1.1.csv was read first, as the provenance record under test. Every quantity it records -- k, the native and anchored >10 MeV integrals, the broad integral, the band construction, the 21% grid-ceiling omission -- was compared against a recomputation, and its 584-row phi_default column was compared pointwise against the driver."
    ref-parma-paper:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Sato 2015 PLOS ONE 10(12):e0144679 recorded as the open-access SHAPE source in the MANIFEST, the declaration, the driver and the emitted table. Its Eq. (6) lethargy form is the reason the division-by-E discipline exists, and its statement that the fitted coefficients live in the distribution rather than the article is why the source was compiled rather than typed. The claim about Eq. (6) is used as recorded in the committed v1.1 header and is CORROBORATED by the retrieved code, which does divide by e exactly once; the article PDF itself was not re-retrieved in this plan."
    ref-parma-source:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Retrieved at the pinned commit only, hashed, integrity-verdicted, compiled unmodified, and read directly: subroutines.cpp:673 (the single /e), :20 (getFFPfromWCpp, which establishes that s is the W-index and that the routine's own comment is stale), :596-675 (the evaporation + gaussian + continuum + thermal decomposition). No substitute commit or release tarball was accepted."
    ref-gordon:
      status: completed
      completed_actions: [compare, cite]
      missing_actions: []
      summary: "Used strictly as the >10 MeV integral benchmark. The untuned PARMA integral was compared against the 3.550e-3 midpoint BEFORE any rescale, giving -8.77% with no fitting. The paywalled-differential-coefficients statement is carried in the MANIFEST, the declaration and the driver docstring so the role cannot drift. Gordon's differential shape was NOT retrieved and is NOT claimed."
    ref-phase7-verification:
      status: completed
      completed_actions: [read, compare]
      missing_actions: []
      summary: "Gap D2 read verbatim and used as the definition of done for this plan. It is now CLOSED rather than carried: a driver is committed, both decisive integrals recompute, and the joint table-vs-provenance check D2 identified as never having been performed has been run and passes at the 3.88e-6 level."
  forbidden_proxies:
    fp-neutron-from-memory:
      status: rejected
      notes: "Every neutron number in this plan is either recomputed by the committed driver or grepped from a locally frozen file, with the command recorded. No WebFetch, no page summary, no secondary citation, no model recall."
    fp-gordon-as-shape:
      status: rejected
      notes: "Gordon appears only as the integral anchor; the paywall statement is asserted present in three separate files by test-shape-vs-anchor-roles, and the driver's norm_anchor default encodes 'gt10MeV_only'."
    fp-lethargy-double-divide:
      status: rejected
      notes: "The single /e is located at subroutines.cpp:673 and neither the C++ shim nor the Python driver repeats it; proved by an integral identity to <0.0001% on five decades rather than by inspection."
    fp-indoor-band-as-central:
      status: rejected
      notes: "phi_lo is never used as a central value, an error bar, or a band midpoint. It is not emitted in the sub-eV table at all, and the declaration names the factor-5 S/B consequence of misusing it."
    fp-precision-inflation:
      status: rejected
      notes: "Every emitted quantity carries order_of_magnitude at its point of definition, and the declaration includes an explicit section explaining that the 1e-5-level agreement of the anchor checks is a REPRODUCIBILITY result, not an accuracy result -- precisely so the tight numbers cannot be read as a tight band."
    fp-thermal-zero:
      status: rejected
      notes: "Phi_th = 2.767075e-3 cm^-2 s^-1 is strictly positive with stated bounds; the test asserts value > 0 and would fail on zero, absence, or silent deferral."
    fp-shielded-quantity-leak:
      status: rejected
      notes: "Token scan over the driver and the emitted table returns zero APPLIED hits; every raw hit sits inside an explicit NOT-applied statement. Veto credit is exactly 1.0 by construction; there is no shield to inherit from."
    fp-inversion-scope-creep:
      status: rejected
      notes: "No regularized/Tikhonov differentiation, no figure digitization, no multi-target over-determination. The method is deterministic log-grid quadrature on the recompiled analytic model. CALC-12 and VALD-11 remain orphaned by design."
  uncertainty_markers:
    weakest_anchors:
      - "The spectral SHAPE has no independent validation: Gordon's differential coefficients are paywalled, so the only cross-check is a single >10 MeV integral agreeing to ~8.8% untuned. Two spectra can share that integral and differ badly at the eV-keV energies that actually set the Ge recoil rate."
      - "The Gordon anchor is applied as a single energy-independent scalar k, propagating a normalization constrained only above 10 MeV onto the entire untested low-energy region"
      - "PARMA was evaluated at the NYC reference point because that is what the Gordon anchor refers to; the actual deployment site is unspecified"
      - "The joint identity now passing at 3.88e-6 is a REPRODUCIBILITY result. It proves the committed numbers are what the recorded code produces; it says nothing about whether the spectrum is right."
    unvalidated_assumptions:
      - "That the wafer is genuinely outdoors -- a configuration statement, not an uncertainty band; indoors the flux is both lower AND differently shaped and no scalar can represent that"
      - "That the WeiMXi mirror at the pinned commit is a faithful copy of the official JAEA distribution; the mirror's README says so and the discriminating strings are consistent, but the JAEA original was not independently retrieved"
      - "That a 293.6 K free-gas ambient Maxwellian is adequate for defining a thermal component Phase 14 will use against a mK cryogenic target"
      - "That the Sato Eq. (6) lethargy statement, taken from the committed v1.1 header rather than from a re-retrieved PDF, is correctly attributed -- corroborated by the code dividing by e exactly once, but not verified against the article text in this plan"
    competing_explanations:
      - "A driver-vs-table mismatch would have had a benign reading (grid/interpolation) and an adverse reading (the table was produced by a path its header does not describe). The check was run before either story was told; the observed uniform 3.88e-6 offset matches the k-rounding prediction quantitatively, which is what excludes the adverse reading rather than merely making it inconvenient."
      - "The thermal peak appearing at 0.0507 eV rather than the conventionally quoted ~0.03 eV could have been a bug or a representation difference. Resolved by derivation: phi ~ E exp(-E/E_th) peaks at E_th = 0.0250 eV while E*phi peaks at 2 E_th = 0.0500 eV; both were computed and both match to grid resolution."
    disconfirming_observations:
      - "Driver phi deviating from the committed phi_default by >5% at any energy, or >1% in median -- did not occur (3.88e-6 both)"
      - "The untuned native integral not landing near 3.239e-3, which would mean the ~9% untuned Gordon agreement was never real -- did not occur (-0.008%)"
      - "The solved k differing from 1.09610 by more than 1% -- did not occur (+0.0004%)"
      - "A systematic factor of E or 1/E between the per-energy and lethargy integrals -- absent on all five decades"
      - "A feature-free or monotone spectrum -- all four features present with >=3 interior extrema"
      - "STILL OPEN: no differential validation of the eV-keV shape exists or can be obtained from any source retrievable in this environment. That is the disconfirming check this plan cannot run, and it is why the channel is order_of_magnitude."
comparison_verdicts:
  - subject_id: test-anchored-integral
    subject_kind: acceptance_test
    subject_role: decisive
    reference_id: ref-gordon
    comparison_kind: benchmark
    metric: integral_flux_10MeV_10GeV_vs_gordon_2004_nyc_sea_level
    threshold: "untuned within 2% of the committed native 3.239e-3; anchored within 1% of 3.550e-3; solved k within 1% of 1.09610; broad within 5% of 1.317e-2"
    verdict: pass
    recommended_action: "Always report the UNTUNED comparison before the k rescale; it is the only independent validation this channel has and reporting it second would make a tuned agreement look like a cross-check."
    notes: "UNTUNED FIRST (k=1): 3.238744e-3 cm^-2 s^-1, -0.008% vs the committed native value, stable to 0.0000% under node doubling 200->400/decade, and sitting -8.77% from the Gordon midpoint WITH NO FITTING. ANCHORED (k=1.09610): 3.549986e-3, -0.0004%. Independently solved k = 1.096104, +0.0004%. Broad Phi(0.01 eV-10 GeV) = 1.317379e-2, +0.029%. Gordon is used strictly as the >10 MeV integral benchmark; its differential coefficients are paywalled and were unsourceable, so it is not and cannot be the shape source."
  - subject_id: test-table-joint-identity
    subject_kind: acceptance_test
    subject_role: decisive
    reference_id: ref-neutron-artifact
    comparison_kind: cross_method
    metric: pointwise_relative_deviation_driver_vs_committed_phi_default
    threshold: "median <= 1%, max <= 5%, any >1% excursion explained"
    verdict: pass
    recommended_action: "Phase-7 gap D2 can be closed in the Phase-7 verification record; the joint check it named as never performed has now been run and passes."
    notes: "The recompiled pinned PARMA source was evaluated at the committed table's own 584 E_n_center_keV values and compared to phi_default_cm2_s_MeV: median AND max relative deviation 3.88e-6, at E_n = 0.0170327 keV, with 0 bins above 1% and 0 above 5%. The deviation is UNIFORM across all bins, which is reported rather than smoothed over and is explained quantitatively as the rounding of the anchor scalar -- exact solved k 1.0961043 vs recorded 1.09610 gives 3.9e-6 -- so the committed table was generated with the unrounded k. The adverse reading (the table was produced by a path its header does not describe) is excluded by that quantitative match, not assumed away."
  - subject_id: claim-anchor-reproducible
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-phase7-verification
    comparison_kind: cross_method
    metric: gap_d2_closure_status
    threshold: "both decisive integrals AND the committed table recomputable from committed code, or D2 recorded as persisting with the exact failing command"
    verdict: pass
    recommended_action: "Record D2 as CLOSED rather than persisting. Note that the closure is a reproducibility result and does not upgrade the channel's accuracy label."
    notes: "D2 read: 'No PARMA driver committed; the decisive 3.55e-3 and 1.317e-2 integrals cannot be recomputed.' A driver is now committed at src/qpd_potential/parma_neutron_flux.py; both integrals recompute to -0.0004% and +0.029%; and the joint table check D2 identified as never having been performed passes at 3.88e-6. The fallback named-gap branch was not needed. The lethargy division is proved to occur exactly once by INT phi dE == INT (E phi) dlnE to <0.0001% on five decades."
---

# Plan 09-02 Summary

**One-liner:** see frontmatter.

## Anchor reproduction, in the required order

### 1. Untuned first (k = 1) — the honest cross-check

| nodes/decade | Φ_native(10 MeV – 10 GeV) | vs committed 3.239×10⁻³ |
|---|---|---|
| 100 | 3.238751×10⁻³ | −0.008 % |
| 200 | 3.238744×10⁻³ | −0.008 % |
| 400 | 3.238743×10⁻³ | −0.008 % |
| 800 | 3.238742×10⁻³ | −0.008 % |

Node-doubling change 200→400: **0.0000 %** (tolerance 0.5 %).
**Untuned vs Gordon midpoint: −8.77 %, with no fitting whatsoever.**

### 2. Anchored

| Quantity | Recomputed | Committed | Deviation | Tol |
|---|---|---|---|---|
| Φ(10 MeV–10 GeV), k = 1.09610 | 3.549986×10⁻³ | 3.550×10⁻³ | −0.0004 % | 1 % |
| solved k | 1.096104 | 1.09610 | +0.0004 % | 1 % |
| Φ(0.01 eV–10 GeV) | 1.317379×10⁻² | 1.317×10⁻² | +0.029 % | 5 % |

### 3. Joint identity — the D2 closure

| Statistic | Value | Tol |
|---|---|---|
| median relative deviation | 3.88×10⁻⁶ | ≤ 1 % |
| max relative deviation | 3.88×10⁻⁶ (at 0.0170327 keV) | ≤ 5 % |
| bins > 1 % | 0 / 584 | — |

**[CONFIDENCE: HIGH]** that the committed table is exactly what its recorded provenance says.
Three independent check families: the untuned integral against a value the header records, the
pointwise 584-bin comparison, and the quantitative explanation of the uniform residual as
k-rounding.

**[CONFIDENCE: LOW]** — deliberately — on the *accuracy* of the spectrum below ~10 MeV. Nothing in
this plan validates the eV–keV shape, and nothing available in this environment can.

### 4. Lethargy identity

∫φ dE vs ∫(Eφ) d(ln E) agree to **< 0.0001 %** on 0.01–0.1 eV, 1–10 eV, 1–10 keV, 1–10 MeV and
100–1000 MeV. Single division site: `data/external/parma/src/subroutines.cpp:673`.

### 5. Morphology

φ(E) thermal peak **0.0250 eV** (= PARMA E_th = kT at 293.6 K); E·φ peak **0.0507 eV**
(= analytic 2E_th); 1/E plateau flat to **1.390×** over 1 eV–10 keV; evaporation hump
**1.957 MeV**; cascade peak **118.9 MeV**.

### 6. Thermal component

**Φ_th = 2.767075×10⁻³ cm⁻² s⁻¹**, bounds 0.01 eV → 0.5 eV (cadmium cutoff), 21.00 % of the broad
integral. Sensitivity to the cutoff choice: 0.4 eV → 2.7283×10⁻³, 1.0 eV → 2.8983×10⁻³.

## Deviations

- **[Rule 4 — missing component] C++ batch shim.** The plan named a Python driver; PARMA is a C++
  library with no batch entry point. `data/external/parma/parma_neutron_driver.cpp` was written
  and frozen with the cache on the `html_to_text.py` precedent, linking the pinned
  `subroutines.cpp` **unmodified**.
- **[Rule 4] Committed coefficient copy.** `neutro_coefficients/` holds the ten `input/neutro`
  files so reproducibility does not depend on the network; `fetch_parma.sh` `cmp`s them against a
  fresh retrieval and aborts on any difference. Bulk is gitignored per the `data/endf` precedent.
- **[Rule 4] Grid-independence test re-specified mid-plan.** Phase 10 landed the two-decade
  downward shared-grid extension while this plan was executing, so "the sub-eV table sits below
  the shared floor" stopped being a valid test of independence. Replaced by a **spacing** test
  (10^(1/100) vs ~79.99 bins/decade), checked against **both** grid versions. The artifact did not
  change; the check got stronger.
- **Recorded trap, not a deviation:** PARMA's `s` is the **W-index**, not the force-field
  potential; the routine's own inline comment says otherwise and is stale. Passing 608 instead of
  100 would have silently changed every number in this channel.

## Self-Check: PASSED

- `data/external/parma/MANIFEST.md`, `fetch_parma.sh`, `parma_neutron_driver.cpp`,
  `neutro_coefficients/` (10 files) — FOUND
- `src/qpd_potential/parma_neutron_flux.py` — FOUND
- `data/ambient_neutron_thermal_v2.0.csv` — FOUND, 201 rows + header, Φ_th parseable and > 0
- `GPD/phases/09-.../09-02-NEUTRON-DECLARATION.md` — FOUND
- `tests/test_ambient_neutron_flux.py` — FOUND, 19 tests, all pass
- Commit `7248132` — FOUND
