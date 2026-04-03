#!/usr/bin/env bash
set -euo pipefail

# fetch_zenodo.sh - Download RF/Video dataset from Zenodo
# Source: https://zenodo.org/record/4264467
# No auth required. Uses Zenodo REST API.

RECORD_ID="4264467"
DEST="$(dirname "$0")/../datasets/multimodal/zenodo"
MARKER="${DEST}/.fetched"

if [ -f "$MARKER" ]; then
    echo "Zenodo RF/Video already fetched. Remove ${MARKER} to re-download."
    exit 0
fi

mkdir -p "$DEST"

echo "Querying Zenodo API for record ${RECORD_ID}..."
RECORD=$(curl -sS "https://zenodo.org/api/records/${RECORD_ID}")

if [ -z "$RECORD" ]; then
    echo "ERROR: Empty response from Zenodo API." >&2
    exit 1
fi

# Extract file download links and names
FILES=$(echo "$RECORD" | jq -r '.files[] | "\(.links.self)\t\(.key)\t\(.checksum)"')

if [ -z "$FILES" ]; then
    echo "ERROR: No files found in Zenodo record." >&2
    exit 1
fi

echo "Found $(echo "$FILES" | wc -l) files."

echo "$FILES" | while IFS=$'\t' read -r url name checksum; do
    if [ -f "${DEST}/${name}" ]; then
        echo "  SKIP ${name} (exists)"
        continue
    fi
    echo "  Downloading ${name}..."
    curl -L -o "${DEST}/${name}" "$url"

    # Verify checksum if available (Zenodo uses md5:hash format)
    if [ -n "$checksum" ] && echo "$checksum" | grep -q '^md5:'; then
        EXPECTED=$(echo "$checksum" | sed 's/^md5://')
        ACTUAL=$(md5sum "${DEST}/${name}" | awk '{print $1}')
        if [ "$EXPECTED" = "$ACTUAL" ]; then
            echo "    checksum OK"
        else
            echo "    WARNING: checksum mismatch for ${name}" >&2
            echo "      expected: ${EXPECTED}" >&2
            echo "      actual:   ${ACTUAL}" >&2
        fi
    fi
done

FILE_COUNT=$(find "$DEST" -maxdepth 1 -type f ! -name '.fetched' | wc -l)
echo "Zenodo RF/Video: ${FILE_COUNT} files downloaded to ${DEST}"
date -u > "$MARKER"
echo "Done."
