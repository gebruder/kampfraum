#!/usr/bin/env bash
set -euo pipefail

# fetch_acoustic.sh — Download acoustic multiclass drone detection dataset
# Paper: https://arxiv.org/abs/2509.04715
# 32 drone categories, spectrograms, MFCCs
#
# DATA RELEASE NOT LOCATED
# The arXiv paper (2509.04715) describes a 32-category acoustic drone dataset
# with spectrograms and MFCCs, but no public data repository link (Zenodo,
# GitHub, or otherwise) has been identified in the paper or its references.
#
# If you locate the data release, update this script and catalog.json.

DEST="$(dirname "$0")/../datasets/acoustic"
MARKER="${DEST}/.fetched_acoustic_multiclass"

ARXIV_URL="https://arxiv.org/abs/2509.04715"

if [ -f "$MARKER" ]; then
    echo "Acoustic multiclass marker present. Remove ${MARKER} to retry."
    exit 0
fi

mkdir -p "$DEST"

echo "============================================================"
echo "  Acoustic Multiclass Drone Detection Dataset"
echo "============================================================"
echo ""
echo "Paper: ${ARXIV_URL}"
echo ""
echo "STATUS: Data release URL not located."
echo ""
echo "The paper describes a 32-category acoustic drone detection dataset"
echo "with spectrograms and MFCCs, but no public download link has been"
echo "found in the paper abstract, body, or references."
echo ""
echo "To contribute:"
echo "  1. Check the paper for supplementary materials"
echo "  2. Contact the authors for the data release"
echo "  3. Update this script with the download URL"
echo "  4. Update catalog.json with size and license info"
echo ""

# Attempt to find data link from arXiv abstract page
echo "Checking arXiv page for data links..."
ABSTRACT_PAGE=$(curl -sS "$ARXIV_URL" 2>/dev/null || true)
if [ -n "$ABSTRACT_PAGE" ]; then
    DATA_LINKS=$(echo "$ABSTRACT_PAGE" | grep -oiE 'https?://[^"<>]*\b(zenodo|github|kaggle|figshare|dataverse|drive\.google)[^"<>]*' || true)
    if [ -n "$DATA_LINKS" ]; then
        echo "Potential data links found:"
        echo "$DATA_LINKS"
        echo ""
        echo "Review these links and update this script."
    else
        echo "No data repository links found on arXiv page."
    fi
else
    echo "Could not reach arXiv (network issue?)."
fi

echo ""
echo "Marking as attempted (no data downloaded)."
date -u > "$MARKER"
echo "Done."
