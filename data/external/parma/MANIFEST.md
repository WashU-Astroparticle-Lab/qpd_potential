# PARMA primary-source cache — provenance manifest

**Deliverable:** `deliv-parma-cache` (Plan 09-02, Task 1)
**Phase:** 09 — Sea-Level Surface Environment Lock (P-ENV)
**Retrieved:** 2026-07-22 (UTC-05 local 21:20–21:22)
**Retrieval host:** Darwin 25.3.0 (osx-arm64) · curl 8.16.0 (OpenSSL/3.0.18) ·
Apple clang 21.0.0 (clang-2100.0.123.102) · Python 3.11.7 · numpy 1.26.4

**Why this cache exists.** Phase-7 verification gap **D2** (severity *significant*, called by
the Phase-7 verifier *"the weakest reproducibility link in the phase"*) reads: *"No PARMA driver
committed; the decisive 3.55e-3 and 1.317e-2 integrals cannot be recomputed."* ROADMAP Phase 9
**SC2** requires the neutron source be **actually retrieved and integrity-checked, not recalled**.
This cache plus `src/qpd_potential/parma_neutron_flux.py` closes D2.

**`WebFetch` and any LLM page summarizer were NOT used as a source for anything in this cache.**
Every byte here came from the single recorded `curl` command below. (Phase-8 lesson: a page
summarizer produced two verified factual errors on sources that were correct and accessible.)

---

## 1. Shape vs anchor roles — recorded here so they cannot drift

| Role | Source | Status |
|---|---|---|
| Differential **SHAPE** | **PARMA v4.10 / Sato T., PLOS ONE 10(12):e0144679 (2015)**, DOI 10.1371/journal.pone.0144679, **open access**. Neutron spectrum = Eq. (6) energy-weighted normalized form × Eq. (4) normalization flux. | The article states the **fitted coefficients live in the EXPACS/PARMA distribution, not in the paper** — which is exactly why the source is retrieved and compiled here rather than typed. |
| **>10 MeV INTEGRAL anchor only** | **Gordon M. S. et al., IEEE Trans. Nucl. Sci. 51, 3427 (2004)**: sea-level NYC Φ(>10 MeV) = 3.5–3.6×10⁻³ cm⁻² s⁻¹. | Gordon's **differential coefficients are PAYWALLED and were unsourceable in this environment.** Gordon is **NOT the spectral shape source** and must never be cited as one (`fp-gordon-as-shape`). |

That the only independent cross-check available is a **single integral above 10 MeV** is precisely
why the neutron channel carries an **order-of-magnitude** accuracy label rather than a percentage
band.

---

## 2. Retrieval command (verbatim)

Working directory for every command in this manifest: `data/external/parma/`.

```console
$ curl -sS -L -w 'http=%{http_code} type=%{content_type} size=%{size_download}\n' \
       -o PARMA-6ff37cac.tar.gz \
       "https://codeload.github.com/WeiMXi/PARMA/tar.gz/6ff37cacb8cf003e2fc269963f9a08f812407264"
http=200 type=application/x-gzip size=1390611
```

**Pinned commit: `6ff37cacb8cf003e2fc269963f9a08f812407264`** (2023-08-04), open mirror
`github.com/WeiMXi/PARMA`. This is the *same* commit `data/ambient_neutron_flux_v1.1.csv`'s header
records. **Any other commit is a different artifact**; no substitute commit and no release tarball
was accepted. The mirror's own `README.md` states it is *"copied from [EXPACS Homepage in
English](https://phits.jaea.go.jp/expacs/index.html)"* — the official JAEA distribution.

The whole retrieval, integrity gate and extraction is re-runnable as
`sh data/external/parma/fetch_parma.sh`, which **fails loudly** rather than proceeding if the
magic bytes or the SHA-256 do not match.

---

## 3. Artifact table

```console
$ shasum -a 256 <artifact>   ;   wc -c <artifact>   ;   file <artifact>
```

| # | Artifact | Bytes | SHA-256 | Integrity verdict |
|---|----------|-------|---------|-------------------|
| 1 | `PARMA-6ff37cac.tar.gz` | 1390611 | `ee95687f3c61488ee05e246788215e5321e00962896986fd0a587d94e831ef08` | **real source archive** — `file` reports *gzip compressed data, from Unix*; **not** an HTML body |
| 2 | `src/subroutines.cpp` | 72995 | `75923ebd84d8b113efc680905542af18d1faf65c5b4cea4e07ad9126eac16652` | **real source text** — `file` reports *C++ source text*; contains `getNeutSpecCpp` (2 hits) |
| 3 | `neutro_coefficients/fitting-lowspec.inp` | 316 | `c5b3d92a6f4aebfd13513a9bdde1ec8803f94ff2147599b352f8ea86e92499a4` | **real coefficient table** — ASCII, header row `A(1) … A(12)`, 12 fitted values |
| 4 | `neutro_coefficients/solar-dep.inp` | 186 | `d9efcc4f0d0af9b4b6310a230952ecab151ac66ebaa6edc20fc83f07b4a78d8c` | **real coefficient table** (ASCII) |
| 5 | `neutro_coefficients/Rigid-Dep.inp` | 1233 | `c57c2fef52e45d861e409304ef20c26f0afc01601ab764b74cd107e744e80f90` | **real coefficient table** (ASCII) |
| 6 | `neutro_coefficients/bestR.inp` | 2349 | `217aa103c47b10bf59fede119aca77cbcfd302dd97a16778f2c4fdc864d067f9` | **real coefficient table** (ASCII) |
| 7 | `neutro_coefficients/correction-depth-rigid.inp` | 31960 | `9fecb317f3d994e52777d8ae10a9bc6615e3cee27b0fa8c0bd998f800969386e` | **real coefficient table** (ASCII) |
| 8 | `neutro_coefficients/Geo-Dep.inp` | 306 | `f2efcb36e8a1215805f4d6cdf25d64b621da2d7bec7f31e625b91dca12e1ebc1` | **real coefficient table** (ASCII) |
| 9 | `neutro_coefficients/Water-Dep.inp` | 327 | `94cc091f6a9196c25fd7f845f8c38a6eed3b1fc9a136fb8ec20e309fb10a1001` | **real coefficient table** (ASCII) |
| 10 | `neutro_coefficients/Aircraft-Dep.inp` | 307 | `0c321011de1fd7e923b94ce7c504b2f75ccda23e2b356db24149ae893dfabbbb` | **real coefficient table** (ASCII) |
| 11 | `neutro_coefficients/Depth-Dep-mid.out` | 1141 | `13991905fe6c0fdc8ae4d41929a7eecbfcefd64ae0e3cdbe4d023dc83a0d57dc` | **real coefficient table** (ASCII) |
| 12 | `neutro_coefficients/Depth-Dep-hig.out` | 1141 | `8140b17bddbccbae6c0166dd70a45fc386b50bb754250474bf5ed59b5c33ed79` | **real coefficient table** (ASCII) |
| 13 | `parma_neutron_driver.cpp` | 2575 | `d94286aee8e0fbf50c54bd4d39e2522cb504b36207c184e95b4e90757e985af4` | n/a — **tool, written in-plan**, frozen with the cache (the `html_to_text.py` precedent in `data/external/nucleus/MANIFEST.md`) |

`neutro_coefficients/` is the **committed** copy of `src/input/neutro/`. `fetch_parma.sh` `cmp`s
every one of the ten files against the freshly-retrieved tree and aborts on any difference; that
comparison ran clean at freeze time (10/10 byte-identical).

**How real source was distinguished from an error page.** Three independent gates, all recorded:
(i) `file` reports `gzip compressed data` for the archive and `C++ source text` / `ASCII text` for
the extracted members — an anti-bot or rate-limit response would be `HTML document text`;
(ii) SHA-256 of the archive matches the value pinned in `fetch_parma.sh`;
(iii) **discriminating strings** are present — `getNeutSpecCpp` (2 hits) in `subroutines.cpp`, the
`A(1) … A(12)` coefficient header in `fitting-lowspec.inp`, and `EXPACS` (6 hits) in the mirror
`README.md`. An HTML challenge page satisfies none of the three.

**Unicode caveat (U+2009 thin space).** Normalize Unicode spaces before any exact-phrase grep:
un-normalized thin spaces silently break ASCII greps and make present text look absent (Phase-8
lesson). For this cache the point is moot but it was **checked, not assumed** — a byte scan of
`subroutines.cpp`, `fitting-lowspec.inp` and `README.md` found **zero** bytes above 0x7F in all
three, so every phrase quoted from them is plain ASCII.

**What is gitignored and why.** `PARMA-*.tar.gz`, the extracted `src/` tree, and the build product
`build_parma_neutron` are third-party bulk, excluded per the `data/endf` precedent (fetcher +
hashes committed, binaries not). **The neutron coefficient files are committed** — they are the
part the Sato-2015 article does not tabulate and the part reproducibility actually depends on.

---

## 4. Build

```console
$ c++ -O2 -std=c++17 -o build_parma_neutron parma_neutron_driver.cpp src/subroutines.cpp
$ ls -la build_parma_neutron
-rwxr-xr-x  1  116208  build_parma_neutron
```

Exit status 0, **no warnings, no diagnostics, and not one line of `subroutines.cpp` edited.**
`subroutines.cpp` opens its coefficient files by **relative** path (`input/neutro/*.inp`), so the
binary must be invoked with the PARMA source root as its working directory —
`src/qpd_potential/parma_neutron_flux.py` does exactly that (`cwd=PARMA_SRC`).

Smoke run at the Phase-7 evaluation point (s = 100, r_c = 2.08 GV, d = 1033 g/cm², g = 0.15):

```console
$ cd src && printf "1.0144972680282425e-5\n" | ../build_parma_neutron 100 2.08 1033 0.15
1.0144972680282425e-05 20.182015...
```

× k = 1.09610 → **22.12152**, against the committed
`data/ambient_neutron_flux_v1.1.csv` first-row `phi_default = 2.21216032e+01`. See §5.

---

## 5. The lethargy division happens **exactly once**, and here is where

Sato Eq. (6) is an **energy-weighted (lethargy-form)** normalized spectrum. The single division by
E lives **inside PARMA's own routine**, at `src/subroutines.cpp` line 673:

```cpp
     getNeutSpec = Fl * (basic * geofactor + ther) / e;
//                                                  ^^^ the one and only /E
```

so `getNeutSpecCpp()` already returns the **per-energy** differential dΦ/dE_n in
cm⁻² s⁻¹ MeV⁻¹. Neither `parma_neutron_driver.cpp` nor
`src/qpd_potential/parma_neutron_flux.py` divides again (`fp-lethargy-double-divide`). The claim
is proved by an integral identity rather than by inspection —
`tests/test_ambient_neutron_flux.py::test_lethargy_divided_exactly_once` checks
∫φ dE = ∫(Eφ) d(ln E) across five well-separated decades.

`s` is the **W-index**, not the force-field potential: `subroutines.cpp` converts it internally via
`getFFPfromWCpp(s) = 370 + 0.3·s^1.45` MV (line 20), giving 608.3 MV at s = 100. The routine's own
inline comment `// s:Force Field Potential (MV)` is **stale**; the calling convention in
`main-simple.cpp` (`double s = getHPcpp(iyear,imonth,iday); // W-index`) is authoritative. Recorded
because typing 608 instead of 100 would silently change every number in this channel.

---

## 6. Checksums reproduce with

```bash
cd data/external/parma
shasum -a 256 PARMA-6ff37cac.tar.gz parma_neutron_driver.cpp src/subroutines.cpp \
              neutro_coefficients/*
```
