---
phase: 08-veto-envelope-geometry-gate-p-veto
plan: 1
plan_contract_ref: GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-01-PLAN.md#/contract
title: "Phase-8 evidentiary floor: four NUCLEUS primary sources frozen with integrity + conversion probes, 34 grep-reproducible verbatim quotes, four mass closures, and the auditable determination that EPJC 86,29 Fig. 1 is dimensionally silent"
date: 2026-07-22
status: complete
depth: full
completed: 2026-07-22
one_liner: "Froze arXiv:2509.03559v1, 1905.10258, 2508.02488v1 and 2401.09837v1 plus Figure1.png as raw HTML + probe-validated normalized text with SHA-256 provenance, and built a 34-quote / 52-command evidence block in which every recorded grep re-runs and exits 0; the three conversion failure modes were reproduced against a naive converter and fixed, with the diagnosis CORRECTED (the mechanism for the two exact-phrase probes is U+2009 THIN SPACE, not dropped content or newline wrapping); all four mass closures pass -- COV cap crystal 1045.2 g at rho_Ge=5.323 vs a 1-significant-figure published '1 kg' (a naive 5% band is cleared by only 4.8 g and fails at rho_Ge=5.35), CaWO4 array-crystal edge 4.996 mm (-0.09%), Al2O3 ARRAY-crystal edge 5.008 mm (+0.17%, a different object from the 0.75 g 5x5x7.5 mm3 commissioning single detector, the 1.50 mass ratio being exactly the 7.5/5.0 height ratio), wafer 109.89 g / 103.2256 cm2; the three factor-5 statements of Sect. 5.2.1 are separated and labelled by physical object and the >99.8% claim is quoted with 'muon-induced' inside the quotation; direct inspection of the 1875x2613 Figure 1 across all six panels establishes NO scale bar and NO dimension callout anywhere, with the whole-paper length inventory reducing to four shield thicknesses plus the 2.5 cm COV crystal thickness and zero occurrences of envelope/cavity/inner-diameter/clearance -- so Success Criterion 1's named evidence route is silent and must be amended in writing; the overburden 2.92+/-0.01 m w.e., attenuation 1.41+/-0.02 and Table 4 uncertainties 25/30/20/30 are all VERIFIED VERBATIM in Sect. 4.1 / Table 4; and contrary to the plan's expectation the published open-access EPJC 86,29 WAS retrievable, with all four load-bearing L2 statements agreeing with arXiv v1 word-for-word and both versions equally silent on any envelope dimension; the Goupy 2024 thesis remains unobtainable (Anubis challenge, HTTP 200 / text/html / 12607 B / first bytes '<!do') and was recorded as a failure rather than saved, leaving Phase 8 unblocked."
provides:
  - "data/external/nucleus/ -- integrity-checked source cache: raw .html AND probe-validated whitespace-normalized .txt for arXiv:2509.03559v1, 1905.10258 (ar5iv), 2508.02488v1, 2401.09837v1, plus 2509.03559v1_Figure1.png (1875x2613) and the published EPJC 86,29 article HTML/text"
  - "data/external/nucleus/MANIFEST.md -- per-artifact curl command, UTC timestamp, byte size, SHA-256, integrity verdict, and the three conversion-probe outcomes; plus the recorded failed Goupy-thesis acquisition with its live challenge signature and a PDF %PDF magic-byte admission guard"
  - "data/external/nucleus/html_to_text.py -- the load-bearing LaTeXML HTML-to-text converter (math -> alttext once, Unicode space family -> ASCII before collapse, one block element per line), frozen with the cache and checksummed"
  - "GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-01-SOURCE-EVIDENCE.md -- the Phase-8 verbatim evidence block: 34 quotes / 52 reproducing grep commands, the three separated factor-5 statements, four mass closures with rho sensitivity, the Fig. 1 inspection record, the carried-anchor status table, and the four-statement cross-version verdict table"
contract_results:
  claims:
    claim-sources-frozen:
      status: passed
      summary: "Four primary NUCLEUS sources plus Figure 1 were retrieved by recorded curl commands and frozen as raw HTML AND normalized text, each with byte size, SHA-256 and an explicit integrity verdict of 'real source text'. Every one of the 34 quoted sentences in 08-01-SOURCE-EVIDENCE.md is reproduced by a recorded grep against a named local file; a single re-verification pass over all 52 extracted commands returned 0 failures. No quote, number or citation anywhere in the deliverable originates from WebFetch, a page summarizer or model recall. The HTML-to-text conversion was treated as load-bearing and validated rather than assumed: all three declared failure modes were reproduced against a naive BeautifulSoup get_text() baseline and fixed, and the naive-vs-fixed comparison is recorded in MANIFEST.md Sect. 3.2. One correction to 08-RESEARCH.md is reported: the mechanism behind the two exact-phrase probes is the U+2009 THIN SPACE separating every number from its unit in the source HTML, not content being dropped or newline-wrapped -- the sentences are present and unwrapped in the naive text, but an ASCII exact-phrase grep returns nothing, which is observationally indistinguishable."
      linked_ids: [deliv-source-cache, deliv-evidence-block, test-download-integrity, test-quote-grep, test-conversion-fidelity, ref-nucleus-2026, ref-nucleus-2019, ref-nucleus-commissioning, ref-cov-prototype, ref-goupy-thesis]
    claim-geometry-closure:
      status: passed
      summary: "All four mass closures pass and none was rounded away. COV cap crystal: rho_Ge*pi*(5.0 cm)^2*(2.5 cm) = 1045.17 g with rho_Ge = 5.323 g/cm3, consistent with the published 1-significant-figure 'a mass of 1 kg' (+4.52% against a nominal 1000 g). The computed value and the assumed density are both reported because the margin against a naive +/-5% band is only 4.8 g (0.48 pp) and the band is FAILED at rho_Ge = 5.35 -- so the closure is stated as 'consistent with 1 s.f.', not as 'within 5%'. CaWO4 3x3 ARRAY crystal: 6.8 g / 9 = 0.7556 g at rho = 6.06 -> edge 4.996 mm, -0.09% vs the published 5 mm cube (5.001 mm, +0.01%, using the paper's own Table 3 total of 6.82 g). Al2O3 3x3 ARRAY crystal: 4.5 g / 9 = 0.5000 g at rho = 3.98 -> edge 5.008 mm, +0.17%; the derived 0.500 g matches the directly published '0.5 g prototype detector made from a (5 mm)3 Al2O3 cubic crystal' exactly. Wafer: 10.16*10.16*0.20*5.323 = 109.89 g, face 103.2256 cm2, diagonal 14.3684 cm, reproducing CONVENTIONS Sect. D. Object identity is stated explicitly: the Al2O3 ARRAY crystal (0.50 g, 5 mm cube) is a DIFFERENT object from the commissioning Al2O3 single detector (5x5x7.5 mm3, 0.75 g, double-TES); the 0.75/0.50 = 1.50 ratio is exactly the 7.5/5.0 height ratio and both close against their own published masses to better than 0.5%. Number-provenance correction: the 6.8 g / 4.5 g array totals come from arXiv:2509.03559v1 Sect. 2, not from the 2019 paper, which gives design-stage 6 g / 4 g that close only to -4.2% / -3.7%; 08-RESEARCH V2/V3 quoted 6.8 and 4.5 without naming their source."
      linked_ids: [deliv-evidence-block, test-mass-closure, ref-nucleus-commissioning]
    claim-fig1-silent:
      status: passed
      summary: "Established by direct inspection of the frozen 1875x2613 px RGB PNG across ALL SIX panels -- whole figure at 2x downscale plus full-resolution crops of panels (d), (e) and (f) with recorded crop boxes -- that EPJC 86,29 (arXiv:2509.03559v1) Figure 1 carries no scale bar, no ruler, no dimension leader and no numeric dimension callout on any panel. The complete set of numerals appearing anywhere on the figure is the six panel letters, the B1/B2 reactor labels, and the '3 x 3' array multiplicity on panel (f), which is a count carrying no unit. Panel (e) has 8 callouts and panel (f) has 6, all transcribed in full; every one is a material or component name. The caption self-describes the figure as a 'Simplified schematic view'. Separately, the Sect. 2 length inventory was enumerated exhaustively by regex over the section text and contains exactly five entries -- 5-cm MV, 5-cm Pb, 20-cm HDPE, 4-cm B4C and the 2.5 cm COV crystal thickness -- with no diameter, height, envelope or cavity; whole-document counts for 'envelope', 'cavity', 'inner diameter', 'clearance' and '100 mm' are all zero. Confirmed identically against the published EPJC HTML. Success Criterion 1's literal evidence route is therefore silent and must be amended in writing rather than discharged; a trap is flagged for later readers, namely that 10.16 cm and 1.27 cm DO appear in the paper, as Bonner-sphere Pb shell dimensions in Sect. 4.2.1, and that 297/430 appear only inside bibliography URLs."
      linked_ids: [deliv-evidence-block, deliv-source-cache, test-fig1-silence, ref-nucleus-2026]
    claim-factor5-disambiguated:
      status: passed
      summary: "The three distinct factor-5 statements of Sect. 5.2.1 are quoted as three separate sentences, each with its own reproducing grep command and each labelled with the physical object it describes: (B.3) a Geant4 modelling conservatism scaling simulated deposited energies in the COV and MV down by 5 and 2 respectively for nuclear-recoil quenching -- explicitly labelled NOT a rejection factor; (B.4) the passive nearly-4pi 4 cm B4C liner further suppressing CaWO4 event rates by a factor ~5, flagged as the L1* payload-geometry-coupled case; (B.5) the COV anti-coincidence bringing a sizable additional reduction of neutron-induced backgrounds of a factor 5, the genuine L2 statement. They appear in the source in exactly that order. An audit of the deliverable confirms every occurrence of 'factor 5' / 'factor ~5' sits inside a labelled heading, a quoted sentence, or a grep command; there is no bare unattributed 'factor 5' anywhere. The separately-labelled Sect. 5.2.2 Pb factor ~50 and additional ~10 are kept distinct from these three."
      linked_ids: [deliv-evidence-block, test-factor5-separation, ref-nucleus-2026]
    claim-carried-anchors-status:
      status: passed
      summary: "Every carried-forward L1 anchor carries an explicit verdict with its section and reproducing command; none is left implicitly assumed. Overburden 2.92 +/- 0.01 m w.e.: VERIFIED VERBATIM in Sect. 4.1. Muon attenuation factor 1.41 +/- 0.02: VERIFIED VERBATIM in Sect. 4.1. Table 4 normalization uncertainties: VERIFIED VERBATIM -- atmospheric muons 25%, atmospheric neutrons 30%, environmental gammas 20%, material radioactivity 30%, with the measured VNS gamma ambience 5.03 cm-2 s-1 in the same table. Reported as a finding rather than a failure: the literal ASCII string 'm.w.e' is NOT FOUND in v1 (grep -c returns 0), because the paper typesets the unit as 'm w.e.'; any future anchor grep must search the value, not the compressed unit. A nuance is carried forward: Sect. 4.1 contains TWO overburden numbers -- the measured cosmic-wheel 2.9 +/- 0.1 m w.e. to which the 1.41 factor corresponds, and the simulated overburden-map average 2.92 +/- 0.01 m w.e. Contrary to the plan's expectation the published open-access EPJC 86,29 version WAS retrievable, and all four load-bearing statements (COV factor-5 neutron rejection, >99.8% muon-induced rejection, ~20% cost of raising the COV threshold 1 -> 10 keV_ee, 2.5 cm COV crystal thickness) agree with arXiv v1 word-for-word, differing only in typography and math markup. The 2.92, 1.41 and B4C ~5 statements are also confirmed in the journal version. Residual: the Table 4 numeric body is served behind a Springer 'Full size table' link and is therefore verified against arXiv v1 only."
      linked_ids: [deliv-evidence-block, test-carried-anchor-status, test-cross-version-spotcheck, ref-nucleus-2026]
  deliverables:
    deliv-source-cache:
      status: passed
      path: data/external/nucleus/
      summary: "13 manifest rows. Raw .html AND probe-validated normalized .txt retained for all four primary sources; 2509.03559v1_Figure1.png (1875x2613 RGB PNG) verified openable with PIL; the frozen converter html_to_text.py checksummed alongside. Every artifact carries its exact curl or conversion command, UTC retrieval timestamp, byte size, SHA-256 and an integrity verdict of 'real source text'. All four text artifacts exceed 20 kB and contain their declared discriminating strings ('boron carbide', '297', 'outer veto', '70 mm'). No artifact is exactly 12587 bytes. No .pdf exists in the cache, and a %PDF magic-byte admission guard is written into the manifest procedure. Three conversion probes are recorded per text artifact together with the naive-converter baseline that shows each failure mode really occurs. The failed Goupy-thesis acquisition is a manifest row with its live signature, and a researcher_setup pointer names the manual browser route and the target path data/external/goupy_thesis_2024.pdf. Two artifacts beyond the plan's list -- the published EPJC 86,29 article HTML and its converted text -- were added for the cross-version spot-check."
      linked_ids: [claim-sources-frozen, claim-fig1-silent, test-download-integrity, test-conversion-fidelity, test-quote-grep]
    deliv-evidence-block:
      status: passed
      path: GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-01-SOURCE-EVIDENCE.md
      summary: "34 verbatim quotes in three labelled sections -- (A) geometry, 17 entries; (B) rejection, 13 entries; (C) mass closure -- each with arXiv id, version, section or caption, and an exact grep command; plus (D) the arXiv:2508.02488 anchor-promotion record, (E) the carried-anchor status table and the cross-version verdict table, (F) the Fig. 1 inspection record and the two negative-result determinations, (G) the re-verification recipe, and (H) uncertainty markers. All 52 recorded grep commands re-run and exit 0. Math-bearing quotes are labelled with their LaTeXML alttext rendering, and the raw HTML is retained so any quote can be checked against the untransformed source. Prototype quotes from arXiv:2401.09837 carry an explicit PROTOTYPE -- NOT THE FINAL COV warning."
      linked_ids: [claim-sources-frozen, claim-geometry-closure, claim-fig1-silent, claim-factor5-disambiguated, claim-carried-anchors-status, test-quote-grep, test-mass-closure, test-fig1-silence, test-factor5-separation, test-carried-anchor-status, test-cross-version-spotcheck]
  acceptance_tests:
    test-download-integrity:
      status: passed
      summary: "PASS. Every artifact in MANIFEST.md carries a command, a byte size, a SHA-256 and an integrity verdict of 'real source text'. Size/discriminator check: 2509.03559v1.txt 109960 B with 'boron carbide' x1; 2508.02488v1.txt 101805 B with '297' x1; 1905.10258.txt 70397 B with 'outer veto' x5; 2401.09837v1.txt 47677 B with '70 mm' x1 -- all > 20 kB. 'find . -type f -size 12587c' returns nothing. No artifact with a challenge-page signature is used as evidence anywhere: the single Anubis response was never written to the cache. One refinement is recorded against 08-RESEARCH.md: the live challenge body was 12607 bytes, not 12587, with a different SHA-256, so byte-size equality is NOT a reliable detector; the stable discriminators are content-type text/html on a .pdf request, first four bytes '<!do' (3c21646f) rather than '%PDF' (25504446), and the literal title 'Making sure you're not a bot!'."
      linked_ids: [claim-sources-frozen, deliv-source-cache]
    test-quote-grep:
      status: passed
      summary: "PASS, 52/52. Every grep command was extracted mechanically from 08-01-SOURCE-EVIDENCE.md by matching lines beginning 'grep ' and re-run in a single pass against the frozen files: 0 failures. Zero quotes in the deliverable lack a reproducing command. Three quotes initially spanned an output-line boundary in the frozen text (the IV description, the Pb ~50 sentence, and the Table 4 body) and returned exit 1 under a single fixed-string grep; rather than loosening the quote they were split into per-line commands that each reproduce their own sentence exactly. No quote needed to be taken from the raw HTML in the end, because the conversion fixes made every load-bearing sentence greppable from the .txt; math-bearing quotes are instead labelled with their alttext rendering and the raw HTML is retained for checking."
      linked_ids: [claim-sources-frozen, deliv-evidence-block, deliv-source-cache]
    test-conversion-fidelity:
      status: passed
      summary: "PASS on all three probes against 2508.02488v1.txt, and the probes were made meaningful by first reproducing each failure against a naive BeautifulSoup get_text() baseline. P1 dropped-content: 'grep -c -F \"100 mm diameter and 25 mm height\"' returns 1 (naive: absent). P2 line-wrap: 'grep -c -F \"diameter of 297 mm\"' returns 1 (naive: absent). P3 math-mangling: the external-shielding sentence renders as '93\\times 93\\times 86 cm3', the expression appearing ONCE with its cm3 unit intact, where the naive conversion produced '93x93x8693\\times 93\\times 8693 x 93 x 86 cm3' -- the LaTeXML triple rendering. The token '93' occurs twice on that line, which is correct because the dimension IS 93 x 93 x 86; the failure mode excluded is the triple rendering of the whole expression, not the literal token count. No probe failure was worked around by loosening a quote. Correction to the declared diagnosis, reported rather than silently fixed: the mechanism behind P1 and P2 is U+2009 THIN SPACE between every number and its unit, not dropped content and not newline wrapping -- the raw HTML literally contains '100 U+2009 mm diameter and 25 U+2009 mm height, and a mass of 1 U+2009 kg', so the sentences are present and unwrapped, and only an ASCII exact-phrase grep fails. The newline-collapse fix is retained anyway because it is required in general. The same fix restores 'with a diameter of 10 cm' in 1905.10258 and '70 mm' in 2401.09837, both of which are also absent under a naive conversion."
      linked_ids: [claim-sources-frozen, deliv-source-cache]
    test-mass-closure:
      status: passed
      summary: "PASS, all four. COV cap crystal: V = pi*(5.0)^2*(2.5) = 196.3495 cm3, m = 1045.17 g at rho_Ge = 5.323 g/cm3, consistent with a 1-significant-figure 'a mass of 1 kg' whose band is [500, 1500] g; against a nominal 1000 g the offset is +4.52%. Both the computed value and the assumed rho_Ge are reported rather than only a percentage, with a sensitivity table (rho = 5.320 -> 1044.6 g, +4.46%; 5.323 -> 1045.2 g, +4.52%; 5.350 -> 1050.5 g, +5.05%, which FAILS a naive +/-5% band) -- the margin against that band is 4.8 g, i.e. about half a percentage point. CaWO4 ARRAY crystal edge 4.996 mm (-0.09%) from the 6.8 g total, or 5.001 mm (+0.01%) from Table 3's 6.82 g. Al2O3 ARRAY crystal edge 5.008 mm (+0.17%) from the 4.5 g total, with the derived 0.500 g matching the directly published 0.5 g (5 mm)3 crystal. Wafer 109.89 g, face 103.2256 cm2, diagonal 14.3684 cm, reproducing CONVENTIONS Sect. D exactly. A sensitivity using the 2019 design-stage array totals (6 g / 4 g) gives 4.792 mm and 4.816 mm, -4.17% and -3.69%, failing the 1% criterion -- which is itself evidence that 6.8 g / 4.5 g are the current per-array masses. Densities rho_CaWO4 = 6.06 and rho_Al2O3 = 3.98 g/cm3 are flagged as ASSUMED standard values, not quoted from any NUCLEUS source."
      linked_ids: [claim-geometry-closure, deliv-evidence-block, ref-nucleus-commissioning]
    test-fig1-silence:
      status: passed
      summary: "PASS. The image opens with PIL at 1875 x 2613 px, RGB, PNG, 149.987 DPI. All six panels were inspected: the whole figure at 2x downscale with every callout legible, plus full-resolution crops of panel (d) at (900,830)-(1875,1690), panel (e) at (0,1680)-(960,2613) and panel (f) at (930,1740)-(1875,2500). Panel (e)'s complete 8-callout list and panel (f)'s complete 6-callout list are transcribed in the deliverable, together with the panel titles and the callouts of (a)-(d). The deliverable contains an explicit finding sentence stating that no scale bar and no numeric dimension callout appears on any panel, and records the inspection method so the negative result is auditable rather than asserted. The Sect. 2 dimension inventory lists exactly the four shield-stack thicknesses (5-cm MV, 5-cm Pb, 20-cm HDPE, 4-cm B4C) and the 2.5 cm COV crystal thickness, with an explicit statement that no envelope dimension appears; whole-document counts for 'envelope', 'cavity', 'inner diameter', 'clearance' and '100 mm' are all zero, and the same enumeration against the published EPJC HTML returns the same token set and the same zeros."
      linked_ids: [claim-fig1-silent, deliv-evidence-block, deliv-source-cache, ref-nucleus-2026]
    test-factor5-separation:
      status: passed
      summary: "PASS. Three distinct sentences are quoted separately, each with its own grep command and each labelled with its physical object: (a) the 4-cm B4C passive layer 'further suppressing the event rates in the CaWO4 detectors by a factor ~5'; (b) the COV anti-coincidence bringing 'a sizable additional reduction of the neutron-induced backgrounds of a factor 5'; (c) the Geant4 conservatism that 'scaled down all deposited energies in the COV and the MV volumes by a factor 5 and 2 respectively, to take into account their quenching to neutron-induced nuclear recoils'. All three sit inside Sect. 5.2.1, appearing in the source in the order (c), (a), (b). A mechanical audit of the deliverable confirms every 'factor 5' / 'factor ~5' occurrence lies inside a labelled heading, a quoted sentence, or a grep command; the document contains no bare 'factor 5' unattached to one of these three sentences. The Sect. 5.2.2 Pb 'factor ~50' and 'additional factor ~10' are quoted under their own separate heading so they cannot be confused with these."
      linked_ids: [claim-factor5-disambiguated, deliv-evidence-block, ref-nucleus-2026]
    test-carried-anchor-status:
      status: passed
      summary: "PASS. Each of the three carried anchors carries an explicit verdict with its section and grep command, and none is left implicitly assumed. '2.92': present, Sect. 4.1 -- 'An omnidirectional overburden of 2.92 +/- 0.01 m w.e. was computed by averaging the overburden map over all directions.' '1.41': present, Sect. 4.1 -- 'gave an omnidirectional muon attenuation factor of 1.41 +/- 0.02, corresponding to a mean overburden of 2.9 +/- 0.1 m w.e. [24]'. Table 4 normalization uncertainties: present, four separate row-level greps returning 'Atm. muons ... 25', 'Atm. neutrons ... 30', 'Env. gamma rays 5.03 (VNS) 20' and 'Material radioactivity see table 3 30'. The literal string 'm.w.e' is NOT FOUND (grep -c returns 0) and is reported as a finding: the paper typesets the unit as 'm w.e.'. The two-overburden nuance (measured 2.9 +/- 0.1 vs simulated 2.92 +/- 0.01, both in Sect. 4.1) is recorded so a later reader does not treat them as one measurement."
      linked_ids: [claim-carried-anchors-status, deliv-evidence-block, ref-nucleus-2026]
    test-cross-version-spotcheck:
      status: passed
      summary: "PASS, and better than the plan anticipated. The published open-access EPJC 86, 29 (2026) version WAS retrieved by curl from link.springer.com (HTTP 200, text/html, 725650 B, SHA-256 989842e6...), validated as full open-access text containing Sect. 5.2.1 and Sect. 5.2.2 rather than a paywall stub, and converted with the same frozen converter. All four load-bearing statements are marked AGREES WITH V1 and are word-for-word identical: (1) 'the COV brings a sizable additional reduction of the neutron-induced backgrounds of a factor 5'; (2) 'reject more than 99.8% of the muon-induced backgrounds'; (3) 'degrades the neutron-induced background rejection by approximately 20%'; (4) 'two cylindrical and four rectangular 2.5 cm thick HPGe crystals'. The only differences anywhere in the compared passages are typographic or markup: '10-100' -> '10-100' with an en dash, 'figure 8' -> 'Fig. 8', 'section 5.3' -> 'Sect. 5.3', and LaTeXML vs MathJax math delimiters. No numeric or physical difference was found. Additionally confirmed unchanged in the journal version: the 2.92 +/- 0.01 m w.e. overburden, the 1.41 +/- 0.02 attenuation factor, and the B4C 'factor ~5' sentence; and the journal version is equally silent on any COV/IV envelope dimension. Residual unresolved item recorded explicitly: the Table 4 numeric body is served behind a Springer 'Full size table' link and is not present in the retrieved article HTML, so 25/30/20/30 remain verified against arXiv v1 only. Downstream quotes stay labelled by the file they were taken from."
      linked_ids: [claim-carried-anchors-status, deliv-evidence-block, ref-nucleus-2026]
  references:
    ref-nucleus-2026:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "Frozen as raw HTML and normalized text with SHA-256. READ: Sect. 2, 4.1, 5.1, 5.2.1, 5.2.2, Table 4, Fig. 1 caption, and Figure1.png inspected directly at full resolution. COMPARED: against the published EPJC version (four statements, all agreeing) and against 08-RESEARCH.md's carried quotes. CITED: 20 of the 34 evidence-block quotes come from this source, each with a reproducing grep. Both what it says (the 2.5 cm COV crystal thickness, the shield stack, the L2 rejection catalogue, the carried L1 anchors) and what it does NOT say (no envelope dimension anywhere; no scale bar in Fig. 1) are established with recorded evidence."
    ref-nucleus-commissioning:
      status: completed
      completed_actions: [read, use, cite]
      missing_actions: []
      summary: "Frozen and grep-verified. READ and USED as the single load-bearing geometric source: COV crystal 100 mm diameter x 25 mm height with a 1 kg mass, internal shielding cylinder 297 mm, external shield 93x93x86 cm3 with a 430 mm cryostat bore, Chooz payload 18 targets + 6 COV + 4 IV from two independent statements, and the two commissioning single detectors. CITED with the explicit written record that it is NOT in the ROADMAP anchor list and is being promoted to a Phase-8 anchor by this phase, together with its three-way corroboration argument and its honest TUM-not-Chooz caveat."
    ref-nucleus-2019:
      status: completed
      completed_actions: [read, compare, cite]
      missing_actions: []
      summary: "Retrieved via ar5iv (arXiv native HTML does not exist for 2019 papers), frozen and grep-verified. READ: Fig. 8 caption, Sect. 3.2.1. COMPARED: the Fig. 8 caption's 'an outer veto (3) with a diameter of 10 cm' independently corroborates the commissioning paper's 100 mm from a different paper six years earlier, and its design-stage array totals (6 g / 4 g) were compared against the 2026 totals (6.8 g / 4.5 g) as a mass-closure sensitivity. CITED as EPJC 79, 1018 -- the journal reference an LLM summarizer misreported as 79, 214 during research."
    ref-cov-prototype:
      status: completed
      completed_actions: [read, avoid]
      missing_actions: []
      summary: "Frozen and grep-verified. READ: the prototype geometry (two cylindrical ~400 g HPGe crystals of 70 mm diameter x 20 mm height, 3-mm thick copper boxes, PTFE holders). AVOIDED as required: both quotes carry an explicit 'PROTOTYPE -- NOT THE FINAL COV' warning block stating that they may be used only as an indication of mounting-overhead scale and must never be substituted for the final COV geometry (100 mm x 25 mm, 2.5 cm thick). No prototype number enters any mass closure, dimension inventory, or fit input."
    ref-goupy-thesis:
      status: completed
      completed_actions: [avoid, cite]
      missing_actions: []
      summary: "AVOIDED: one acquisition attempt was made for the record and failed with an Anubis JavaScript proof-of-work challenge (HTTP 200, content-type text/html, 12607 B, first four bytes 3c21646f = '<!do' rather than '%PDF', title 'Making sure you're not a bot!'). The response was deliberately NOT saved and in particular not written as goupy_thesis_2024.pdf. No number, dimension or statement anywhere in this phase derives from it. CITED: recorded in MANIFEST.md Sect. 4 as a failed acquisition with its full observed signature, as an acquisition obligation, and with a named manual browser route plus a %PDF verification step. Phase 8 is NOT blocked by it; the consequence is that open questions Q1 (rectangular COV crystal and Cu support dimensions) and Q2 (IV beaker / module stack height) stay bounded rather than read, and that the only genuinely independent third route to the COV cavity remains unavailable."
    ref-research-08:
      status: completed
      completed_actions: [read, compare]
      missing_actions: []
      summary: "READ in full, including the dated round-2 RETRACTION of Sect. F1 and Pitfall 7 -- the retracted orientation-invariance lemma was respected and no struck text was re-imported; this plan does no fit arithmetic, which is Plan 08-03's scope. COMPARED: its quoted sentences were treated as the target of independent re-verification rather than as a substitute for it, and all of them reproduce from the frozen files. Four corrections are reported rather than absorbed: (i) the stated conversion failure mechanism (dropped content / newline wrapping) is actually U+2009 THIN SPACE; (ii) the Anubis challenge body is not byte-stable at 12587 B, so byte-size equality is not a valid detector; (iii) V2/V3's 6.8 g and 4.5 g array totals come from arXiv:2509.03559v1 Sect. 2, not from the 2019 paper, which gives 6 g / 4 g; (iv) V2 compares the CaWO4 ARRAY crystal against the commissioning single-TES detector's '5 x 5 x 5 mm3, 0.76 g', which is a different object. None of these changes a physics conclusion, and every NUCLEUS sentence 08-RESEARCH carries reproduces verbatim from the frozen files."
  forbidden_proxies:
    fp-webfetch-quote:
      status: rejected
      notes: "WebFetch and every LLM page summarizer were used for nothing. All four sources and the journal version were retrieved by recorded curl commands and frozen locally; all 34 quotes come from those files via 52 recorded greps that re-run and exit 0. The two research-pass failures were specifically re-tested and both are refuted from the frozen text: '99.8' IS present in Sect. 5.2.1 at character offset 70413 (a summarizer had reported it absent), and the 2019 journal reference IS EPJC 79, 1018 (a summarizer had reported 79, 214). Section attributions were determined by locating each quote relative to the numbered section headings in the frozen text, not from recall."
    fp-silent-challenge-page:
      status: rejected
      notes: "The Goupy attempt returned HTTP 200 with content-type text/html and a 12607-byte Anubis challenge body. It was written to a temporary file, inspected (first four bytes 3c21646f, not 25504446; title 'Making sure you're not a bot!'; markers 'anubis' and 'challenge' present), reported, and deleted. It was never saved into data/external/nucleus/ and never named .pdf. No .pdf exists anywhere in the cache. A binding admission guard is written into MANIFEST.md Sect. 2: any future .pdf must have '%PDF' as its first four bytes, and byte-size equality with 12587 is explicitly documented as NOT a sufficient discriminator because the live body was 12607 bytes."
    fp-fig1-fabricated-precision:
      status: rejected
      notes: "No COV or IV envelope dimension is recorded anywhere in this plan's output as having been read from Fig. 1e/f, and no pixel-scaling measurement was performed. The figure was inspected only to establish what it does NOT carry. The finding is stated as a negative determination with a recorded inspection method (image SHA-256, 1875x2613 px, all six panels, named crop boxes, full callout transcriptions) so it is auditable, and it is explicitly framed as licensing a written amendment of Success Criterion 1's evidence route -- which Plan 08-03 owns -- rather than as discharging it. The dimensions Phase 8 will actually use are routed through arXiv:2508.02488 and arXiv:1905.10258, each with a mass closure or an independent cross-paper corroboration."
  uncertainty_markers:
    weakest_anchors:
      - "The 100 mm COV cylinder diameter comes from arXiv:2508.02488, a TUM commissioning paper describing a setup in which only ONE of the six COV crystals was installed, not from a Chooz drawing; it is not in the ROADMAP anchor list and is promoted by this phase"
      - "The Goupy 2024 thesis, the only genuinely independent third route to the COV cavity, is unobtainable by any scripted route, so the rectangular-COV-crystal and Cu-support dimensions stay bounded rather than read"
      - "Densities rho_CaWO4 = 6.06 and rho_Al2O3 = 3.98 g/cm3 are assumed standard material values, not quoted from any NUCLEUS source, and the C.2/C.3 array-crystal closures depend on them"
      - "The COV mass closure clears a naive +/-5% band by only 4.8 g and fails it at rho_Ge = 5.35, so it is defensible only as consistency with a 1-significant-figure '1 kg'"
      - "Table 4's numeric normalization uncertainties (25/30/20/30) are verified against arXiv v1 only; the Springer article HTML serves the table body behind a 'Full size table' link"
    unvalidated_assumptions:
      - "That the TUM commissioning COV crystal and the Chooz COV cap crystals are the same part, supported only by the shared 2.5 cm / 25 mm thickness and the 10 cm / 100 mm diameter agreement across three papers"
      - "That the 2026 array totals 6.8 g and 4.5 g divide over exactly 9 crystals per array; the count 9 comes from the 2019 paper's '3 x 3 array' and is corroborated by the 18-target Chooz payload, but the 2026 paper never says '3 x 3' itself"
      - "That the LaTeXML alttext rendering faithfully represents the typeset math in every quoted math-bearing sentence; the raw HTML is retained so this is checkable but was spot-checked, not exhaustively verified"
    competing_explanations:
      - "The 100 mm crystal could be a commissioning-only part with larger cylinders at Chooz, which would weaken the fit determination's tight route; weakened but not excluded by the 2019 paper's independent 10 cm and by the shared 2.5 cm thickness"
      - "The four rectangular COV crystals could be larger than the cylindrical caps, which would make the cavity exceed the tight 5.0 cm estimate; this plan reads no rectangular-crystal dimension and takes no position on it"
    disconfirming_observations:
      - "Neither arXiv:2509.03559v1 nor the published EPJC 86,29 contains any COV/IV envelope dimension, so the disconfirming observation that would have restored Success Criterion 1's literal evidence route did NOT occur -- searched for exhaustively and absent in both versions"
      - "The COV mass closure did NOT fail: 1045.2 g against a published 1 kg, so the disconfirming observation that would have indicated a mis-read of 100 mm x 25 mm did not occur"
      - "The open-access EPJC version does NOT state a different COV crystal thickness or a different rejection factor than arXiv v1; all four spot-checked statements are word-for-word identical, so the version-drift disconfirmation did not occur"
      - "A live disconfirmation that DID occur, against 08-RESEARCH.md rather than against the physics: the Anubis challenge body is not byte-stable at 12587 bytes (observed 12607 with a different SHA-256), so the recorded byte-size signature is not a valid detector and was replaced with magic-byte and content-type checks"
comparison_verdicts:
  - subject_id: claim-carried-anchors-status
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-nucleus-2026
    comparison_kind: cross_method
    metric: verbatim_sentence_agreement
    threshold: "4/4 statements agree"
    verdict: pass
    recommended_action: "Keep quotes labelled by source file; re-check Table 4's numeric body against the journal version if a Springer full-size-table route becomes available."
    notes: "arXiv v1 vs published open-access EPJC 86, 29 (2026): COV factor-5 neutron rejection, >99.8% muon-induced rejection, ~20% cost of raising the COV threshold 1 -> 10 keV_ee, and the 2.5 cm COV crystal thickness are all word-for-word identical. Differences are typographic/markup only. 2.92 m w.e., 1.41 and the B4C ~5 also confirmed. Table 4's numeric body is not in the Springer article HTML and stays v1-verified."
  - subject_id: claim-geometry-closure
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-nucleus-commissioning
    comparison_kind: benchmark
    metric: computed_vs_published_mass
    threshold: "COV consistent with 1 s.f. '1 kg'; array-crystal edges within 1% of 5 mm"
    verdict: pass
    recommended_action: "Carry the computed 1045.2 g and the assumed rho_Ge = 5.323 g/cm3 explicitly into Plan 08-03; do not restate the closure as 'within 5%'."
    notes: "COV cap crystal 1045.17 g vs published 'a mass of 1 kg' (+4.52% vs nominal 1000 g, inside the 1 s.f. band, clearing a naive 5% band by only 4.8 g and failing it at rho_Ge = 5.35). CaWO4 ARRAY crystal edge 4.996 mm (-0.09%). Al2O3 ARRAY crystal edge 5.008 mm (+0.17%), with the derived 0.500 g matching a directly published 0.5 g (5 mm)3 crystal. Wafer reproduces CONVENTIONS Sect. D exactly."
  - subject_id: ref-nucleus-2019
    subject_kind: reference
    subject_role: decisive
    reference_id: ref-nucleus-commissioning
    comparison_kind: cross_method
    metric: independent_diameter_agreement
    threshold: "10 cm vs 100 mm"
    verdict: pass
    recommended_action: "Cite both papers together whenever the 10.0 cm COV cap diameter is used; do not present them as three independent routes, since any Fig. 1 pixel-scaling route shares the same anchor."
    notes: "arXiv:1905.10258 Fig. 8 caption states the outer veto has 'a diameter of 10 cm', independently corroborating arXiv:2508.02488's 100 mm from a different paper six years earlier. Supporting rather than decisive because the fit determination itself is Plan 08-03's scope."
  - subject_id: claim-sources-frozen
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-research-08
    comparison_kind: prior_work
    metric: verbatim_quote_reproduction
    threshold: "100% of carried NUCLEUS quotes reproduce from a frozen file"
    verdict: pass
    recommended_action: "Carry the four recorded corrections into Plan 08-03 and any Phase-8 verification pass; do not re-import 08-RESEARCH's byte-size challenge signature, its conversion-failure mechanism, its unattributed 6.8 g / 4.5 g provenance, or its V2 object identification."
    notes: "PASS on the compared quantity: every NUCLEUS sentence 08-RESEARCH.md carries reproduces verbatim from the frozen primary sources via a recorded grep, which is exactly what claim-sources-frozen asserts. The verdict is pass rather than tension because the four discrepancies found are in 08-RESEARCH's methodology and provenance notes, not in any quote failing to reproduce: (i) the stated conversion-failure mechanism is U+2009 THIN SPACE, not dropped content or newline wrapping; (ii) the Anubis challenge body is 12607 B with a different SHA-256 this session, so its recorded 12587-byte signature is not a valid detector; (iii) the 6.8 g / 4.5 g array totals come from arXiv:2509.03559v1 Sect. 2, not the 2019 paper, which gives design-stage 6 g / 4 g; (iv) V2 compares the CaWO4 ARRAY crystal against the commissioning single-TES detector's published '5 x 5 x 5 mm3, 0.76 g', which is a different object -- the closure still passes, and the array/single distinction is now stated explicitly in the evidence block. All four are recorded in contract_results.references.ref-research-08 and in the Deviations section rather than absorbed."
---

# Plan 08-01 Summary — Phase-8 evidentiary floor

**Objective (from the plan).** Freeze the primary NUCLEUS sources locally, prove every sentence
Phase 8 will quote is actually in them, and determine what the named Success-Criterion-1 source
does and does not carry.

**Verdict: complete.** All three tasks executed. All eight acceptance tests pass. Zero deviations
requiring escalation; three corrections to `08-RESEARCH.md` reported rather than absorbed.

---

## What was produced

| Artifact | Path |
|---|---|
| Source cache + provenance manifest | `data/external/nucleus/` (13 manifest rows) |
| The frozen HTML→text converter | `data/external/nucleus/html_to_text.py` |
| Verbatim evidence block | `GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-01-SOURCE-EVIDENCE.md` |

---

## Acceptance tests — actual results

| Test | Result | Evidence |
|---|---|---|
| `test-download-integrity` | **PASS** | 13 manifest rows, each with command + size + SHA-256 + verdict. All four `.txt` > 20 kB with their discriminating strings. `find . -type f -size 12587c` → nothing. No `.pdf` in cache. |
| `test-quote-grep` | **PASS 52/52** | All commands extracted mechanically from the deliverable and re-run in one pass; **0 failures**. |
| `test-conversion-fidelity` | **PASS 3/3** | P1 `100 mm diameter and 25 mm height` → 1; P2 `diameter of 297 mm` → 1; P3 expression rendered once as `93\times 93\times 86 cm3`. Each failure first reproduced against a naive baseline. |
| `test-mass-closure` | **PASS 4/4** | 1045.17 g / 4.996 mm / 5.008 mm / 109.89 g. See below. |
| `test-fig1-silence` | **PASS** | 1875 × 2613 px, all six panels inspected, full callout lists transcribed, explicit finding sentence recorded. |
| `test-factor5-separation` | **PASS** | Three sentences quoted separately and labelled; mechanical audit finds no bare unattributed "factor 5". |
| `test-carried-anchor-status` | **PASS** | 2.92 ± 0.01 m w.e. and 1.41 ± 0.02 verified in §4.1; Table 4 25/30/20/30 verified. `m.w.e` literal NOT FOUND — reported as a finding. |
| `test-cross-version-spotcheck` | **PASS 4/4 agree** | Published EPJC 86, 29 retrieved (725 650 B) and all four statements word-for-word identical to v1. |

---

## The four mass closures

| # | Object | Computed | Published | Verdict |
|---|---|---|---|---|
| V1 | COV cap crystal (Ge cylinder) | **1045.17 g** @ ρ_Ge = 5.323 g/cm³ | "a mass of 1 kg" (1 s.f.) | **PASS** — consistent with 1 s.f.; +4.52% vs nominal 1000 g |
| V2 | CaWO₄ **3×3 ARRAY** crystal | edge **4.996 mm** | 5 mm cube | **PASS** (−0.09%) |
| V3 | Al₂O₃ **3×3 ARRAY** crystal | edge **5.008 mm** | 5 mm cube | **PASS** (+0.17%) |
| V4 | QPD wafer | 109.89 g, 103.2256 cm², diag 14.3684 cm | CONVENTIONS §D | **PASS** (exact) |

**The V1 precision caveat matters and must travel with the number.** The margin against a naive
±5% band is **4.8 g** — about half a percentage point — and the band is *failed* at ρ_Ge = 5.35.
The defensible statement is "1045.2 g, consistent with a 1-significant-figure published 1 kg,
assuming ρ_Ge = 5.323 g/cm³", not "passes within 5%".

**Object identity (do not "fix" this later).** The Al₂O₃ **array** crystal (0.50 g, 5 mm cube) and
the Al₂O₃ **commissioning single detector** (5 × 5 × 7.5 mm³, 0.75 g, double-TES) are **two
different detectors**. 0.75/0.50 = 1.50 = 7.5/5.0, and both close against their own published
masses to better than 0.5%.

---

## The load-bearing negative findings

Both are **deliverables**, not omissions.

1. **EPJC 86, 29 Fig. 1 is dimensionally silent.** No scale bar, no ruler, no dimension leader, no
   numeric callout on any of panels (a)–(f), verified by direct inspection of the frozen
   1875 × 2613 image at full resolution. The only numerals anywhere on the figure are the panel
   letters, the B1/B2 reactor labels, and the "3 × 3" array multiplicity. **Success Criterion 1's
   named evidence route is silent** and must be amended in writing — which is Plan 08-03's job.

2. **The paper states no COV/IV envelope dimension anywhere.** The §2 length inventory is exactly
   five entries (5 cm MV, 5 cm Pb, 20 cm HDPE, 4 cm B₄C, 2.5 cm COV crystal thickness).
   `envelope`, `cavity`, `inner diameter` and `clearance` occur **zero** times in the whole
   document. Confirmed identically in the published EPJC version.

**Trap flagged for later readers:** `10.16 cm` and `1.27 cm` *do* appear in arXiv:2509.03559v1 —
as the **Bonner-sphere Pb shell converter** dimensions in §4.2.1. The coincidence with the wafer's
10.16 cm edge is accidental. `297` and `430` appear only inside bibliography URLs.

---

## Deviations and corrections

No deviation rule 5 or 6 was triggered. Four corrections to `08-RESEARCH.md` are reported rather
than absorbed, none of which changes a physics conclusion:

1. **[Rule 1 — diagnosis correction] Conversion failure mechanism.** 08-RESEARCH attributes the two
   exact-phrase probe failures to *dropped content* and *newline wrapping*. The verified mechanism
   is **U+2009 THIN SPACE** between every number and its unit. The sentences are present and
   unwrapped in a naive conversion; only the ASCII exact-phrase grep fails. The observable is
   identical, which is why the two were indistinguishable during research. The newline-collapse fix
   is retained anyway because it is required in general.

2. **[Rule 1 — guard correction] The Anubis challenge signature is not byte-stable.** 08-RESEARCH
   records the challenge body as exactly 12 587 bytes. The live body this session was **12 607
   bytes** with a different SHA-256. **Byte-size equality is not a valid detector.** The manifest
   guard was rewritten around the `%PDF` magic bytes, the `content-type`, and the challenge title.

3. **[Rule 4 — missing provenance] The 6.8 g / 4.5 g array totals.** 08-RESEARCH V2/V3 use these
   without naming a source. They come from **arXiv:2509.03559v1 §2**, not from the 2019 paper,
   which gives design-stage **6 g / 4 g** — those close only to −4.2% / −3.7% and would *fail* the
   1% criterion. The closures use the 2026 values and the 2019 variant is reported as a sensitivity.

4. **[Rule 4 — object identification] V2's comparison target.** 08-RESEARCH's V2 closes the CaWO₄
   **3×3 array** crystal against the commissioning paper's *single-TES* detector
   ("5 × 5 × 5 mm³, 0.76 g"). Those are **different objects**. The closure still passes — the array
   crystal is 0.7556 g and the single-TES detector is 0.76 g, so they happen to be nearly identical
   in the CaWO₄ case — but the same conflation applied to Al₂O₃ would be badly wrong, since the
   Al₂O₃ single detector is 5 × 5 × **7.5** mm³ at 0.75 g against an array crystal of 0.50 g. The
   evidence block now states the array/single distinction explicitly in three places so no later
   reader "fixes" the 0.50-vs-0.75 g difference.

**Beyond the plan (documented, in-scope):** the published open-access EPJC 86, 29 was retrieved and
frozen, which the plan and 08-RESEARCH both allowed might be impossible. Two extra artifacts were
added to the cache for this. The result upgrades confidence in every arXiv-v1 quote.

**Retraction respected.** `08-RESEARCH.md` §F1 and Pitfall 7 carry a dated round-2 retraction of the
orientation-invariance lemma. No struck text was re-imported. This plan performs **no fit
arithmetic** — that is Plan 08-03's scope — so the retracted lemma had no load-bearing role here.

---

## Handoff

**To Plan 08-03 (the fit determination).** Quote §F.6 and §F.8 of the evidence block directly when
amending Success Criterion 1's evidence route. Use A.1 (100 mm × 25 mm, 1 kg), A.10 (2.5 cm), A.2
(297 mm) and A.13 (10 cm) as the dimension inputs, each with its recorded grep. Carry the V1
precision caveat and the ρ_Ge assumption. Note V10: the 100 mm-cylinder route and any Fig. 1(e)
pixel route **share the same scale anchor** and are not independent.

**To Plan 08-04 (the L1/L1\*/L2 taxonomy).** Section B of the evidence block is the source table:
13 rejection statements with sections and grep commands, the three factor-5s separated by physical
object, and the >99.8% claim quoted with "muon-induced" visible.

**To Plan 08-05.** §C.6 records both footprint bases (103.2256 cm² vs the published 2.25 cm²
crystal footprint → 45.9×; vs the ROADMAP's unlabelled "~9 cm²" holder-scale figure → 11.5×). The
"~9 cm²" figure is **not** a NUCLEUS number.

**Cross-phase (Phase 9).** Not re-verified this pass, carried from 08-RESEARCH: Fig. 8 of
arXiv:2509.03559 carries **both** a passive-only family and an "all vetoes" trace on the same axes.
Phase 9 must select the trace deliberately.

**Still open.** The Goupy 2024 thesis (`researcher_setup`: manual browser download to
`data/external/goupy_thesis_2024.pdf`, verify `%PDF`). It is the only genuinely independent third
route to the COV cavity and the only source that could plausibly overturn the expected verdict.
Phase 8 is **not** blocked by it.

---

## Self-Check: PASSED

Run after the deliverables were written, from a clean shell.

| Check | Result |
|---|---|
| All 15 declared artifact files exist on disk | **15/15 FOUND** |
| MANIFEST.md SHA-256 entries still match the files on disk | **12/12 verified, 0 mismatches** |
| Every `grep` command in 08-01-SOURCE-EVIDENCE.md re-runs | **52/52, 0 failures** |
| `validate summary-contract` on 08-01-SUMMARY.md | **valid: True, errors: []** |
| No `.pdf` in the source cache; no artifact exactly 12587 B | **PASS** |
| Contract coverage: 5 claims, 2 deliverables, 8 acceptance tests, 6 references, 3 forbidden proxies | **all present in the ledger** |
