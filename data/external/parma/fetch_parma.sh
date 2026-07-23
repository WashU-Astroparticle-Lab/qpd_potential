#!/bin/sh
# Reproduce the frozen PARMA source cache at its PINNED commit.
#
# Plan 09-02, Task 1.  Follows the data/external/nucleus/ + data/endf precedent:
# the fetcher and the hashes are committed; the bulky retrieved tree is not.
#
# WebFetch and any LLM page summarizer are FORBIDDEN as a source here.  Only this
# recorded curl command is.
#
# Run from data/external/parma/ :   sh fetch_parma.sh
set -eu

COMMIT=6ff37cacb8cf003e2fc269963f9a08f812407264
TARBALL=PARMA-6ff37cac.tar.gz
TARBALL_SHA256=ee95687f3c61488ee05e246788215e5321e00962896986fd0a587d94e831ef08

curl -sS -L -w 'http=%{http_code} type=%{content_type} size=%{size_download}\n' \
     -o "$TARBALL" \
     "https://codeload.github.com/WeiMXi/PARMA/tar.gz/${COMMIT}"

# Integrity gate: a retrieval that returns HTTP 200 with an HTML body is a
# FAILED retrieval, not source.  Check the magic bytes AND the hash.
file "$TARBALL" | grep -q 'gzip compressed data' || {
    echo "FAILED: $TARBALL is not gzip (likely an HTML error/challenge page)" >&2
    exit 1
}
GOT=$(shasum -a 256 "$TARBALL" | cut -d' ' -f1)
[ "$GOT" = "$TARBALL_SHA256" ] || {
    echo "FAILED: SHA-256 mismatch: got $GOT expected $TARBALL_SHA256" >&2
    exit 1
}

rm -rf src "PARMA-${COMMIT}"
tar xzf "$TARBALL"
mv "PARMA-${COMMIT}" src

# The committed coefficient copies must be byte-identical to the retrieved ones.
for f in neutro_coefficients/*; do
    cmp "$f" "src/input/neutro/$(basename "$f")" || {
        echo "FAILED: committed coefficient $f differs from the pinned source" >&2
        exit 1
    }
done

echo "OK: PARMA source frozen at $COMMIT; coefficients verified byte-identical."
