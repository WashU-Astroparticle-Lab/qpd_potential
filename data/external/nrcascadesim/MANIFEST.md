# nrCascadeSim -- natural-Ge capture cascade tables

**Retrieved:** 2026-07-23 from the public repository. **`WebFetch` and LLM summarizers were NOT
used as a data source.** Only the curated cascade DATA and the Weisskopf coefficient reference are
taken; the code itself (which requires ROOT) is not built or vendored.

## Retrieval command (reproducible)

```bash
git clone --depth 1 https://github.com/villano-lab/nrCascadeSim.git
# commit 0f7793e4077b292891ac2fd33db12deb1e140eee (2023-03-31)
cp nrCascadeSim/levelfiles/v1_natGe_WFast.txt \
   nrCascadeSim/levelfiles/v1_natGe_WSlow.txt \
   nrCascadeSim/levelfiles/README.md .
cp nrCascadeSim/src/weisskopf.cpp weisskopf.cpp.reference
shasum -a 256 *
```

## Integrity

| file | sha256 |
|---|---|
| `v1_natGe_WFast.txt` | `f1c718354993626312b456bdc859c8f2c7faabae4cb7ad51dc6a7b4c3003437d` |
| `v1_natGe_WSlow.txt` | `28d30ed9b50e972531c4bfa2fc6b4fc7f3092d4e8dde2914cda19a66294f4b7e` |
| `README.md` | `a700ee73ba1539bd7e15544ee1ec2fea7ba018bebec597304007e04d983809c6` |
| `weisskopf.cpp.reference` | `6feb2cfe86e55b7e39cb43901817d18cda4a9f419d59c96e5871b7c76bb66dff` |

## Source

A. N. Villano, K. Harris, S. Brown, *nrCascadeSim -- A simulation tool for nuclear recoil cascades
resulting from neutron capture*, **J. Open Source Software 7, 3993 (2022)**, arXiv:2104.02742,
DOI 10.5281/zenodo.5579857. Repository https://github.com/villano-lab/nrCascadeSim, commit
`0f7793e4077b292891ac2fd33db12deb1e140eee`.

## What is used, and what is not

`src/qpd_potential/capture_recoil.py` consumes the DATA only:

- **`v1_natGe_WFast.txt` / `v1_natGe_WSlow.txt`** -- curated cascade realizations (fraction, product
  nucleus, level energies below S_n, level lifetimes). `WFast`/`WSlow` differ only in the Weisskopf
  multipolarity assumed for unknown lifetimes (short vs long), which brackets decay-in-flight.
- **`weisskopf.cpp.reference`** -- the Weisskopf single-particle width coefficients (Nucl. Data A 2,
  347 (1966)) read to reproduce the code's lifetime estimates, including its L>3 -> M3 fallback.

NOT used: the ROOT-dependent executables, the continuous Lindhard stopping model (bracketed in
`capture_recoil.py` by the slow/fast limits instead), and the ionization model.

## Two limits of the source, both carried explicitly

- **Coverage.** The natural-Ge table's cascade fractions sum to **0.2685**: it resolves 26.85% of
  captures; the rest is the unresolved quasi-continuum (pandemonium). Never renormalised to 1.
- **77Ge absent.** The table lists 4 of 5 capture products (71/73/74/75 Ge). 76Ge(n,gamma)77Ge is
  omitted -- 76Ge is 0.54% of natural thermal capture and its EGAF entry is anomalous.
