# NUCLEUS primary-source cache — provenance manifest

**Deliverable:** `deliv-source-cache` (Plan 08-01, Task 1)
**Phase:** 08 — Veto-Envelope Geometry Gate (P-VETO)
**Retrieved:** 2026-07-22, 22:53:03Z → 22:53:04Z (UTC)
**Retrieval host:** Darwin 25.3.0 (osx-arm64) · curl 8.16.0 (OpenSSL/3.0.18) · Python 3.11.7 · bs4 4.12.2 · lxml 5.3.0 · Pillow 10.2.0

**Why this cache exists.** Every NUCLEUS sentence Phase 8 quotes must be reproducible by a
recorded shell command against a local file. `WebFetch` and any LLM page summarizer are
**forbidden as a quote source** for this phase (`fp-webfetch-quote`): during Phase-8 research a
summarizer reported `99.8` as absent from arXiv:2509.03559v1 §5.2.1 when it is present, and
misreported EPJC **79, 1018** as 79, 214. Both errors were on sources that were in fact correct
and accessible.

---

## 1. Artifact table

Working directory for every command below: `data/external/nucleus/`.

| # | Artifact | Retrieval command | Bytes | SHA-256 | Integrity verdict |
|---|---|---|---|---|---|
| 1 | `2509.03559v1.html` | `curl -sS -L -o 2509.03559v1.html "https://arxiv.org/html/2509.03559v1"` | 398143 | `d82dd32381b7ad8ec090f1d5c517011a9954209293f368bf07a513ae3262543c` | **real source text** |
| 2 | `2509.03559v1.txt` | `python3 html_to_text.py 2509.03559v1.html 2509.03559v1.txt` | 109960 | `74f043f413edc5d1e61eda513a75449ed3651e315af8c44b9f789ae50c33b839` | **real source text** |
| 3 | `2509.03559v1_Figure1.png` | `curl -sS -L -o 2509.03559v1_Figure1.png "https://arxiv.org/html/2509.03559v1/Figures/Figure1.png"` | 1660744 | `bddf5c998b9f54b10a9ff1fbbe6e372c7ea2d579effabcaad6f861c4535c34da` | **real source image** (PNG, RGB, 1875×2613) |
| 4 | `1905.10258.html` | `curl -sS -L -o 1905.10258.html "https://ar5iv.labs.arxiv.org/html/1905.10258"` | 395723 | `f8ca119bc9c486e355ed959f6e42f22262dbc597761191acf57129d4dd0a3ba7` | **real source text** |
| 5 | `1905.10258.txt` | `python3 html_to_text.py 1905.10258.html 1905.10258.txt` | 70397 | `d956e553931356f389209ea2f5974997ff09c37ef45e07111e68470906e85a7c` | **real source text** |
| 6 | `2508.02488v1.html` | `curl -sS -L -o 2508.02488v1.html "https://arxiv.org/html/2508.02488v1"` | 287033 | `0a35aeffdb93adb830623616e8dc6a98ab08a4b2553c3b4fa3dc1770e1589f2f` | **real source text** |
| 7 | `2508.02488v1.txt` | `python3 html_to_text.py 2508.02488v1.html 2508.02488v1.txt` | 101805 | `7905a2605b18eb943e24f33c8fc51a48ce9a63fe72b3ff626ba310bc817a6193` | **real source text** |
| 8 | `2401.09837v1.html` | `curl -sS -L -o 2401.09837v1.html "https://arxiv.org/html/2401.09837v1"` | 267552 | `44d06fc063264fa6a44fc47ecbcd0cb00af35afc8f777f9119f7a46080362ddc` | **real source text** |
| 9 | `2401.09837v1.txt` | `python3 html_to_text.py 2401.09837v1.html 2401.09837v1.txt` | 47677 | `cfb347a8c5b9b65ae9f94abf93cf22c5106ce58fd5d2c787e58f64e993d06df7` | **real source text** |
| 10 | `html_to_text.py` | (written in-plan; the converter itself, frozen with the cache) | 4828 | `bad70df607c6dd494b19c7f7bcac38e43303120c4b4121efeb97645be14fd8c3` | n/a — tool |
| 11 | `epjc_86_29.html` | `curl -sS -L -A "<browser UA>" -o epjc_86_29.html "https://link.springer.com/article/10.1140/epjc/s10052-025-15168-9"` | 725650 | `989842e65bfae44adf22c1e759defeb8ed0beba9e486033ac64813e89724ff19` | **real source text** (published open-access EPJC 86, 29 (2026); version of record) |
| 12 | `epjc_86_29.txt` | `python3 html_to_text.py epjc_86_29.html epjc_86_29.txt` | 116076 | `b60641eba11a15885edd1c23a99b5f71991c24ce672bf0cdf3179f0c40592793` | **real source text** |
| 13 | *(Goupy 2024 thesis)* | see §4 | — | — | **FAILED — anti-bot challenge; NOT saved** |

**Artifacts 11–12 were not anticipated by the plan.** 08-RESEARCH.md and Plan 08-01 both allowed for
the journal version being unretrievable. It was retrieved (2026-07-22 UTC, HTTP 200, `text/html`).
Validation: contains §5.2.1 and §5.2.2 in full (open access), not a paywall stub; discriminating
strings `sizable additional reduction` (1 hit), `99.8` (1 hit), `2.5 cm thick HPGe` (1 hit),
`raising the COV threshold` (1 hit). Used for the four-statement cross-version spot-check in
`08-01-SOURCE-EVIDENCE.md` §E.2 — all four agree with arXiv v1 word-for-word. Note the converter
reports `0` math nodes for this file: Springer serves math as MathJax `\( \)` inline text rather
than LaTeXML `<math alttext=...>`, so the alttext path is inapplicable and the text passes through
directly. The Unicode-space and whitespace-collapse fixes still apply and are what make its
sentences greppable.

HTTP status and content-type observed at retrieval (from `curl -w`):

```
2509.03559v1.html         http=200  type=text/html; charset=utf-8   size=398143
2509.03559v1_Figure1.png  http=200  type=image/png                  size=1660744
1905.10258.html           http=200  type=text/html; charset=utf-8   size=395723
2508.02488v1.html         http=200  type=text/html; charset=utf-8   size=287033
2401.09837v1.html         http=200  type=text/html; charset=utf-8   size=267552
```

Checksums reproduce with:

```bash
shasum -a 256 2509.03559v1.html 2509.03559v1.txt 2509.03559v1_Figure1.png \
              1905.10258.html 1905.10258.txt 2508.02488v1.html 2508.02488v1.txt \
              2401.09837v1.html 2401.09837v1.txt html_to_text.py
```

**Version labelling.** arXiv HTML `…v2` for 2509.03559 returns 404 even though v2 exists on the
abs page. Every quote drawn from these files is therefore labelled **arXiv v1**, not the journal
version of record. See `08-01-SOURCE-EVIDENCE.md` §E for the cross-version spot-check.

---

## 2. Discriminating-string and size validation (`test-download-integrity`)

Each text artifact must be > 20 kB and contain its declared discriminating string.

| Artifact | Size | > 20 kB | Discriminating string | Hits | Verdict |
|---|---|---|---|---|---|
| `2509.03559v1.txt` | 109 960 B | yes | `boron carbide` | 1 | PASS |
| `2508.02488v1.txt` | 101 805 B | yes | `297` | 1 | PASS |
| `1905.10258.txt` | 70 397 B | yes | `outer veto` | 5 | PASS |
| `2401.09837v1.txt` | 47 677 B | yes | `70 mm` | 1 | PASS |

```bash
grep -c -F "boron carbide" 2509.03559v1.txt   # 1
grep -c -F "297"           2508.02488v1.txt   # 1
grep -c -F "outer veto"    1905.10258.txt     # 5
grep -c -F "70 mm"         2401.09837v1.txt   # 1
```

**Anti-bot signature check.** No artifact in this cache is exactly 12 587 bytes:

```bash
find . -type f -size 12587c    # returns nothing
```

**PDF admission guard (procedure, binding on any future addition to this cache).** Any `.pdf`
admitted here must satisfy **both**: (i) its first four bytes are `%PDF` (`head -c 4 <f> | xxd -p`
→ `25504446`), and (ii) it is not an HTML body. Byte-size equality with 12 587 is **not** a
sufficient discriminator — see §4, where the live challenge page came back at 12 607 bytes, not
12 587. The reliable discriminators are the magic bytes, the `content-type`, and the challenge
markup. There is currently **no `.pdf` in this cache**.

---

## 3. HTML → text conversion probes (`test-conversion-fidelity`)

The conversion is load-bearing. `html_to_text.py` (frozen as artifact 10) implements three fixes:
math nodes replaced by their `alttext` exactly once with the MathML subtree discarded; Unicode
space family (U+00A0, U+2000–U+200A incl. **U+2009 THIN SPACE**, U+2028/9, U+202F, U+205F, U+3000)
mapped to ASCII space *before* collapsing; whitespace runs collapsed and one block element per
output line so sentence-level greps match.

### 3.1 The three declared probes, run on `2508.02488v1.txt`

| Probe | Command | Result | Verdict |
|---|---|---|---|
| **P1 dropped-content** | `grep -c -F "100 mm diameter and 25 mm height" 2508.02488v1.txt` | `1` | **PASS** |
| **P2 line-wrap** | `grep -c -F "diameter of 297 mm" 2508.02488v1.txt` | `1` | **PASS** |
| **P3 math-mangling** | `grep -F "The external shielding measures" 2508.02488v1.txt` | expression rendered once as `93\times 93\times 86 cm3` | **PASS** |

P1 full return:

```
cylindrical geometry with 100 mm diameter and 25 mm height, and a mass of 1 kg
```

P3 full return (fixed converter):

```
The external shielding measures 93\times 93\times 86 cm3 and features a cylindrical
opening (430 mm in diameter) from the top to accommodate the cryostat.
```

`93` occurs exactly twice on that line, which is correct: the dimension *is* 93 × 93 × 86. The
failure mode being excluded is the LaTeXML **triple rendering of the whole expression**, not the
literal count of the token `93`. The `cm3` unit is intact and adjacent (the `<sup>3</sup>` did not
detach).

### 3.2 Naive-conversion baseline — the failure modes actually reproduced

Run with a plain `BeautifulSoup(html, "lxml").get_text()` and no post-processing:

| Probe | Naive converter | Fixed converter |
|---|---|---|
| `"100 mm diameter and 25 mm height"` in `2508.02488` | **absent** | present |
| `"diameter of 297 mm"` in `2508.02488` | **absent** | present |
| external-shielding math | `93×93×8693\times 93\times 8693 × 93 × 86 cm3` (**expression rendered 3×**) | `93\times 93\times 86 cm3` |
| `"diameter of 10 cm"` in `1905.10258` | **absent** | present |
| `"70 mm"` in `2401.09837` | **absent** | present |
| `"99.8"` in `2509.03559v1` | present | present |

### 3.3 Correction to the failure-mode diagnosis carried in 08-RESEARCH.md

`08-RESEARCH.md` and the plan attribute probes P1/P2 to *content being dropped* and to *newline
wrapping*. The mechanism verified in this execution is **neither**: it is the U+2009 THIN SPACE.
The raw HTML contains, literally,

```
cylindrical geometry with 100 mm diameter and 25 mm height, and a mass of 1 kg
... has a cylindrical shape with a diameter of 297 mm and is mechanically secured ...
```

so the sentences are present and unwrapped in the naive text, but the ASCII exact-phrase grep
returns nothing because the separator is not U+0020. The **observable** is identical to a dropped
or wrapped sentence — an exact-phrase grep returning nothing — which is why the two were
indistinguishable during research. The recorded fix (Unicode-space normalization) covers all
three, and the newline-collapse fix is retained because it is required in general even though
line wrapping was not the operative mechanism in *this* retrieval. This is recorded as a finding,
not silently corrected.

### 3.4 Per-artifact probe outcomes

| Artifact | Dropped-content probe | Line-wrap probe | Math-mangling probe |
|---|---|---|---|
| `2509.03559v1.txt` | PASS — `99.8` present (`grep -c -F "99.8"` → 1) | PASS — `reject more than 99.8% of the muon-induced backgrounds` matches as one string | PASS — 265 `<math>` nodes replaced by `alttext`, none triple-rendered |
| `2508.02488v1.txt` | PASS — P1 above | PASS — P2 above | PASS — P3 above; 204 `<math>` nodes replaced |
| `1905.10258.txt` | PASS — `with a diameter of 10 cm` present (absent under naive conversion) | PASS — Fig. 8 caption matches as one string | PASS — 287 `<math>` nodes replaced |
| `2401.09837v1.txt` | PASS — `70 mm` present (absent under naive conversion) | PASS — prototype sentence matches as one string | PASS — 139 `<math>` nodes replaced |

**Both `<id>.html` (raw) and `<id>.txt` (normalized) are retained for every source.** The `.txt`
is the default grep target. Where a sentence is math-bearing or fails to survive conversion,
quoting from the frozen **raw HTML** with a recorded command is permitted and is labelled as such
in `08-01-SOURCE-EVIDENCE.md`.

---

## 4. Goupy 2024 thesis — recorded acquisition FAILURE

**Target:** C. Goupy, *Background mitigation strategy for the detection of coherent elastic
scattering of reactor antineutrinos on nuclei with the NUCLEUS experiment*, PhD thesis,
Université Paris Cité (2024), NNT 2024UNIP7170, HAL `tel-05298505`,
DOI `10.70675/574d6e17z1b68z4676zbde9z255450e1c649`.

**Attempt (one, for the record), 2026-07-22 UTC:**

```bash
curl -sS -L -o "$TMP" \
  -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36" \
  -w "http=%{http_code} content_type=%{content_type} size=%{size_download}\n" \
  "https://theses.hal.science/tel-05298505/document"
```

**Observed:**

```
http=200  content_type=text/html; charset=utf-8  size=12607
first 4 bytes = 3c21646f   ("<!do")   — NOT %PDF (25504446)
sha256 = 5a5bf3a1b05825cd5115f9ba99dcde83407e97cc0d86ea47c5a65205fe0e081e
<!doctype html><html lang="en"><head><title>Making sure you're not a bot!</title>
  <link rel="stylesheet" href="/.within.website/x/xess/xess.css?...">
markers found: "anubis", "challenge"
```

**Verdict: `failed` — Anubis JavaScript proof-of-work anti-bot challenge.** The response was
**deliberately not saved** to the cache and in particular was not written as
`goupy_thesis_2024.pdf` (`fp-silent-challenge-page`). HTTP 200 here means "the challenge page was
served successfully", not "the thesis was obtained".

**Signature refinement.** 08-RESEARCH.md records the challenge body as exactly **12 587** bytes.
The live body this session was **12 607** bytes with a different SHA-256, so the body is not
byte-stable (it carries a per-request nonce / cachebuster). **Do not use byte-size equality alone
as the challenge detector.** The stable discriminators are: `content-type: text/html` on a `.pdf`
request, first four bytes `<!do` rather than `%PDF`, and the literal title
`Making sure you're not a bot!`.

**Impact: NONE on Phase 8's completion.** The thesis is optional, non-blocking enrichment. It is
the only genuinely independent third route to the COV cavity (V10) and would upgrade open
questions Q1 (rectangular COV crystal dimensions, Cu support) and Q2 (IV beaker / module stack
height) from *bounded* to *read*. It is cited as an acquisition obligation and is **not** evidence
for any number in this phase.

### `researcher_setup` — named manual acquisition route

The Anubis challenge clears in a few seconds in a real browser but cannot be passed by any
scripted route (four routes verified blocked in 08-RESEARCH.md: `theses.hal.science/tel-05298505`,
`…/document`, `…/file/va_Goupy_Chloe.pdf`, `hal.science/tel-05298505v1/document`, plus
`www.theses.fr/2024UNIP7170.pdf`).

1. Open <https://theses.hal.science/tel-05298505> in a real browser; wait for the challenge to clear.
2. Download the PDF (`va_Goupy_Chloe.pdf`).
3. Place it at **`data/external/goupy_thesis_2024.pdf`** (note: outside this `nucleus/` directory,
   per the plan's `researcher_setup`).
4. Verify before use: `head -c 4 data/external/goupy_thesis_2024.pdf | xxd -p` must print
   `25504446`.

Phase 8 does **not** block on this and completed without it.

---

## 5. Integrity closure statement

Every artifact in this cache carries a retrieval command, a byte size, a SHA-256, and an explicit
integrity verdict. Every text artifact additionally carries its three conversion-probe outcomes.
The single artifact with an `anti-bot challenge` signature (the Goupy attempt) was **not saved**
and is used as evidence for nothing. No quote anywhere in Phase 8 originates from WebFetch, a page
summarizer, or model recall.
