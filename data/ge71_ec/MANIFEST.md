# 71Ge decay scheme and Ga shell binding energies -- retrieval manifest

**Retrieved:** 2026-07-23, Phase 14 Plan 14-02 (`test-branching-sourced-or-bounded`,
`test-ec-energies`).
**Pattern:** the Phase-9 PARMA acquisition pattern -- recorded command, byte count, SHA-256.
**`WebFetch` and LLM page summarizers were NOT used and are not a data source.**

## Retrieval commands (reproducible)

```bash
# IAEA Live Chart of Nuclides
curl -sS -A "Mozilla/5.0" -o data/ge71_ec/livechart_71ge_ground_states.csv \
  "https://nds.iaea.org/relnsd/v1/data?fields=ground_states&nuclides=71ge"
curl -sS -A "Mozilla/5.0" -o data/ge71_ec/livechart_71ge_decay_rads_x.csv \
  "https://nds.iaea.org/relnsd/v1/data?fields=decay_rads&nuclides=71ge&rad_types=x"
curl -sS -A "Mozilla/5.0" -o data/ge71_ec/livechart_71ge_decay_rads_e.csv \
  "https://nds.iaea.org/relnsd/v1/data?fields=decay_rads&nuclides=71ge&rad_types=e"
# xraylib electron binding energies (edge energies), Z = 1..100
curl -sSL -o data/ge71_ec/xraylib_edges.dat \
  "https://raw.githubusercontent.com/tschoonj/xraylib/master/data/edges.dat"
shasum -a 256 data/ge71_ec/*.csv data/ge71_ec/*.dat
```

## Integrity

| file | bytes | sha256 |
|---|---:|---|
| `data/ge71_ec/livechart_71ge_ground_states.csv` | 749 | `180352f7663df26ecf82ac3daf59f77e3f9f88263537f2c0a3509726631e3be3` |
| `data/ge71_ec/livechart_71ge_decay_rads_x.csv` | 2316 | `e330e3a203fb23da111b8da71cb755697d80ea87467e3d3c33731ae606efba21` |
| `data/ge71_ec/livechart_71ge_decay_rads_e.csv` | 3287 | `f9a4a4f59ed3c9b6140fcfe10d35e69190de453aa330cd29f5c5e91fd48d44fa` |
| `data/ge71_ec/xraylib_edges.dat` | 27760 | `f0eaecfaf3cac3fadb0d0ba39eb5630e80b42ad78812ee900290307b4dc389f0` |

## What each file supplies, and what it does NOT

### `livechart_71ge_ground_states.csv`

Q_EC = 232.47 +/- 1.15 keV and the 11.43 d half-life, both SOURCED. Consumed by
`capture_channel.ge71_ground_state()`.

### `livechart_71ge_decay_rads_x.csv` and `..._e.csv`

Discrete X-ray and Auger/conversion-electron line lists. **These do NOT contain the
capture-shell branching fractions directly.** What they contain is the fate of the
vacancies, which is enough to DERIVE P_K rigorously:

> Every K-shell vacancy created by the electron capture is filled either radiatively
> (a Ga K X-ray) or non-radiatively (a K Auger electron). Those two channels are
> exhaustive and mutually exclusive, so **P_K = I(K X-rays) + I(K Auger)** per decay.

Two reading rules, both verified in code rather than assumed:

1. **Filter to the ground-state EC decay.** Both files also carry the 198.371 keV
   isomer's IT rows; mixing them would inflate every intensity. The filter is
   `decay == "EC"` AND `p_energy` at the ground state.
2. **Sum LEAVES, not leaves-plus-totals.** The X-ray table lists `KA1`, `KA2`, `KB` as
   the leaves with `KpB1`/`KpB2` as components of `KB`; the Auger table lists a total
   `K` row whose components are `KLL`, `KLX`, `KXY`. `ge71_k_shell_capture_fraction()`
   checks both decompositions close before using them.

**P_L and P_M are NOT obtainable this way** -- L vacancies are produced both by direct
L capture and by the K-vacancy cascade, so the L intensities do not isolate P_L. They
are therefore BOUNDED by 1 - P_K, and the L/M split is left undetermined rather than
assigned from recollection (`fp-assert-branching`).

### `xraylib_edges.dat`

Electron binding (absorption-edge) energies for Z = 1..100. Only the Ga (Z = 31) rows
are used, to CHECK the physical identification of the EC line energies. **Provenance
honesty:** this is xraylib's own compiled data file, retrieved and integrity-checked
as a file; the underlying tabulation it compiles is not further traced here, so the
check establishes consistency with a standard compilation rather than with a primary
measurement.
