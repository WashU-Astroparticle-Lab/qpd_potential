# EGAF prompt capture-gamma line lists -- retrieval manifest

**Retrieved:** 2026-07-23, Phase 14 Plan 14-01 (`test-egaf-disposition`).
**Pattern:** the Phase-9 PARMA acquisition pattern -- recorded command, byte count, SHA-256.
**`WebFetch` and LLM page summarizers were NOT used and are not a data source.**

## Retrieval command (reproducible)

```bash
curl -sS -m 60 -o egaf.zip https://www-nds.iaea.org/pgaa/egaf.zip
shasum -a 256 egaf.zip
for f in 71GE 73GE 74GE 75GE 77GE; do unzip -o -q -j egaf.zip "${f}_EGAF.ens" -d data/egaf/; done
```

## Integrity

| file | bytes | sha256 |
|---|---:|---|
| `egaf.zip` (archive, 245 files, not committed) | 1115103 | `288b32b020434165a98dd3314010c79f6d45daee054daf6cb1ec19738e2783e2` |
| `data/egaf/71GE_EGAF.ens` | 36255 | `2bacfb6f507127c6ee608713a8064d8bdbc282207be2d7e0b9f07df646e41cbb` |
| `data/egaf/73GE_EGAF.ens` | 25348 | `bb0f77d613fcb5961de3e529be9577fd691c9fbc16bf29f06dec8d3fd36975a6` |
| `data/egaf/74GE_EGAF.ens` | 166632 | `c7dfafac80d67dc3fd8afe4aab3a9a807470ee4541195e300fa0fb844e63c39c` |
| `data/egaf/75GE_EGAF.ens` | 24118 | `44b2a45532aca14dcf9a47cc9397057dedcd65f41df8da886a080d4ff0245045` |
| `data/egaf/77GE_EGAF.ens` | 9112 | `2e2f7487bfa4c61ad47fff48f1f0d6931938b36200000b0b81dc95c7f7b40edc` |

## Source

Evaluated Gamma-ray Activation File (EGAF), IAEA Nuclear Data Section,
https://www-nds.iaea.org/pgaa/ ; evaluated by R. B. Firestone (LBNL), December 2003.
ENSDF-format `.ens` datasets, one file per capture PRODUCT nucleus.

## Mapping to the Ge capture channels

| target | reaction | EGAF product file |
|---|---|---|
| 70Ge | 70Ge(n,g) | `71GE_EGAF.ens` |
| 72Ge | 72Ge(n,g) | `73GE_EGAF.ens` |
| 73Ge | 73Ge(n,g) | `74GE_EGAF.ens` |
| 74Ge | 74Ge(n,g) | `75GE_EGAF.ens` |
| 76Ge | 76Ge(n,g) | `77GE_EGAF.ens` |

## Reading discipline (two traps, both measured)

1. **Each file carries THREE datasets** -- the evaluated `{~EGAF}` set plus the raw
   `^BUDAPEST` and `^L^A^N^L` measurement sets -- each with its OWN normalisation
   record. A naive whole-file parse sums all three and inflates the per-capture
   intensity by roughly a factor of three. `capture_channel.read_egaf_gammas` uses
   `{~EGAF}` only, and the cascade-completeness check is what caught the inflation.
2. **Intensity per capture = NR x RI / sigma_0**, with `NR` read from the N record and
   `sigma_0` from the `BR$|s{-0}=` comment. `RI` is the ELEMENTAL partial gamma
   cross section in barns, per the file's own `cG`/`cN` comment records.

## What this artifact does and does NOT close

It DISCHARGES the acquisition half of ROADMAP Phase 14 SC1. It does NOT close the
cascade: the observed cascade carries only ~60-71% of the capture Q-value for the four
significant isotopes (see `artifacts/v2.0/capture_recoil_bounds.csv`), so a cascade
recoil SPECTRUM still cannot be constructed from it. That deficit is the named gap,
and it is now a number rather than an absence.
