#!/usr/bin/env python3
"""LaTeXML/ar5iv HTML -> greppable plain text, for the Phase-8 NUCLEUS source cache.

Plan: GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-01-PLAN.md, Task 1.

This conversion is LOAD-BEARING, not a formality. Three failure modes were
declared in the plan and all three were reproduced against these exact sources:

  (1) MATH MANGLING.  LaTeXML emits
          <math alttext="93\\times 93\\times 86">
            <semantics><mrow><mn>93</mn><mo>x</mo>...</mrow>
              <annotation encoding="application/x-tex">93\\times 93\\times 86</annotation>
              <annotation encoding="application/x-llamapun">93 x 93 x 86</annotation>
            </semantics></math>
      A naive get_text() concatenates the presentation MathML *and* both
      annotations, rendering the expression THREE times, and splits the
      following "cm<sup>3</sup>" across the seam.
      FIX: replace every <math> node by its `alttext` attribute exactly once
      and discard the entire MathML subtree (presentation + both annotations).

  (2) LINE WRAPPING.  A naive conversion emits "diameter of 297\\nmm", so the
      exact-phrase grep "diameter of 297 mm" returns nothing although the
      sentence is present.
      FIX: whitespace-normalize -- every run of whitespace (including newlines)
      inside a block collapses to a single ASCII space, and each block element
      is emitted on exactly one output line, so sentence-level greps match.

  (3) DROPPED CONTENT.  The single most load-bearing sentence of Phase 8,
      "cylindrical geometry with 100 mm diameter and 25 mm height, and a mass
      of 1 kg", does not survive a naive conversion as a greppable string.
      DIAGNOSED CAUSE (this execution): the source separates every number from
      its unit with U+2009 THIN SPACE, not U+0020 -- the raw HTML literally
      contains "100\\u2009mm diameter and 25\\u2009mm height, and a mass of
      1\\u2009kg".  A converter that preserves U+2009 therefore yields a file in
      which the ASCII phrase is absent, which is indistinguishable from the
      sentence having been dropped.
      FIX: map the Unicode space family (U+00A0, U+2000-U+200A, U+2028,
      U+2029, U+202F, U+205F, U+3000) to ASCII space BEFORE collapsing runs.

Everything else in the document is preserved verbatim: no de-hyphenation, no
quote folding, no dash folding, no case folding.  Non-space Unicode
(x, ~, mu, en-dashes, Greek) is left exactly as the source wrote it.

Usage:  python3 html_to_text.py <in.html> <out.txt>
"""

import re
import sys

from bs4 import BeautifulSoup

# Unicode whitespace that must become ASCII space so exact-phrase greps match.
UNICODE_SPACE_CODEPOINTS = (
    [0x00A0, 0x1680]                # NO-BREAK SPACE, OGHAM SPACE MARK
    + list(range(0x2000, 0x200B))   # EN QUAD .. ZERO WIDTH SPACE (incl. U+2009 THIN SPACE)
    + [0x2028, 0x2029]              # LINE / PARAGRAPH SEPARATOR
    + [0x202F, 0x205F, 0x3000]      # NARROW NBSP, MEDIUM MATH SPACE, IDEOGRAPHIC SPACE
)
SPACE_MAP = {cp: " " for cp in UNICODE_SPACE_CODEPOINTS}

# Elements that start a new output line (block-level in the LaTeXML output).
BLOCK_TAGS = {
    "p", "div", "section", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6",
    "figcaption", "blockquote", "table", "caption", "dt", "dd", "article",
}

DROP_TAGS = {"script", "style", "noscript"}


def convert(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    for tag in soup.find_all(list(DROP_TAGS)):
        tag.decompose()

    # (1) math: emit alttext once, drop the MathML subtree entirely.
    n_math = 0
    for m in soup.find_all("math"):
        alt = m.get("alttext")
        m.replace_with(" " + (alt if alt else "") + " ")
        n_math += 1

    # Emit one line per block element.
    for tag in soup.find_all(list(BLOCK_TAGS)):
        tag.insert_before("\n")
        tag.insert_after("\n")

    text = soup.get_text()

    # (3) Unicode spaces -> ASCII space, BEFORE collapsing.
    text = text.translate(SPACE_MAP)

    # (2) collapse intra-line whitespace runs; one block per line.
    lines = []
    for raw in text.split("\n"):
        line = re.sub(r"[ \t\r\f\v]+", " ", raw).strip()
        if line:
            lines.append(line)
    out = "\n".join(lines) + "\n"
    sys.stderr.write(f"  math nodes replaced by alttext: {n_math}\n")
    return out


def main() -> int:
    if len(sys.argv) != 3:
        sys.stderr.write(__doc__ or "")
        return 2
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as fh:
        html = fh.read()
    out = convert(html)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(out)
    sys.stderr.write(f"  {src} -> {dst}  ({len(out)} bytes, {out.count(chr(10))} lines)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
