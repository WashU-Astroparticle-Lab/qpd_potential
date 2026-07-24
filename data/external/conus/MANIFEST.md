# CONUS+ (2025) -- first observation of reactor CEvNS on germanium

**Retrieved:** 2026-07-23. **`WebFetch` and LLM summarizers were NOT used as a data source.**

The extracted text `2501.05206v3.txt` is the frozen source of record and IS committed (the raw PDF
was extracted via the gpd-arxiv resource, then sentence-split; no binary is kept).

## Integrity

| file | sha256 | committed |
|---|---|---|
| `2501.05206v3.txt` | `b296286ee1c0771a1a9a4272b9bc5553ed96ca15280a6379d390800afddcb76b` | yes |

## Source

CONUS Collaboration (N. Ackermann et al.), *Direct observation of coherent elastic
antineutrino-nucleus scattering*, **Nature 643, 1229 (2025)**, arXiv:2501.05206v3. Leibstadt
nuclear power plant (KKL), Switzerland; high-purity germanium detectors, 20.7 m from the core.

## What it settles for this project (VALD-12)

- **The CONUS+ signal-extraction window is 160-800 eV_ee** (l.113: "fitted simultaneously in an
  energy window between 160 eV and 800 eV"). This appears in NEITHER authoritative project
  document: ROADMAP/REQUIREMENTS said 0.4-1 keV_ee; SUMMARY.md said 160 eV_ee (open-ended).
- The 0.4-1 keV_ee range is where CONUS+ quotes background COMPONENT rates, not where it fits the
  signal. 160 eV is the lowest detector threshold, not a window. 158.7 eV is the separate 71Ge EC
  M line (arXiv:2604.25748), whose near-coincidence with 160 eV caused the confusion.
- Signal 395/327 = 1.208 cts/kg/d; SM prediction 347/327 = 1.061 cts/kg/d.
- The often-quoted S/B ~ 0.03 combines a 160-800 eV_ee signal with a 400-1000 eV_ee background --
  DIFFERENT windows -- so it is not a well-defined single-window ratio and must not gate VALD-12.

See `docs/v2.0-conus-window-and-reactor-neutrons.md` for the full VALD-12 resolution.
