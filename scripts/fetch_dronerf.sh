#!/usr/bin/env bash
set -euo pipefail

# fetch_dronerf.sh - Download DroneRF dataset from Mendeley Data
# Source: https://dx.doi.org/10.17632/f4c2b4n755.1
# Size: ~40GB, CSV, 3 drone types
# Parrot Bebop, Parrot AR, DJI Phantom
# Flight modes: off / on+connected / hovering / flying / recording

DEST="$(dirname "$0")/../datasets/rf/dronerf"
MARKER="${DEST}/.fetched"

if [ -f "$MARKER" ]; then
    echo "DroneRF already fetched. Remove ${MARKER} to re-download."
    exit 0
fi

mkdir -p "$DEST"

echo "Querying Mendeley Data API for file list..."
FILE_LIST=$(curl -sS "https://data.mendeley.com/api/datasets/f4c2b4n755/files")

if [ -z "$FILE_LIST" ] || [ "$FILE_LIST" = "[]" ]; then
    echo "ERROR: Empty response from Mendeley API." >&2
    exit 1
fi

URLS=$(echo "$FILE_LIST" | jq -r '.[].download_url')
NAMES=$(echo "$FILE_LIST" | jq -r '.[].filename')

echo "Found $(echo "$URLS" | wc -l) files."

paste <(echo "$URLS") <(echo "$NAMES") | while IFS=$'\t' read -r url name; do
    if [ -f "${DEST}/${name}" ]; then
        echo "  SKIP ${name} (exists)"
        continue
    fi
    echo "  Downloading ${name}..."
    curl -L -o "${DEST}/${name}" "$url"
done

# Verify we got files
FILE_COUNT=$(find "$DEST" -maxdepth 1 -type f ! -name '.fetched' | wc -l)
if [ "$FILE_COUNT" -eq 0 ]; then
    echo "ERROR: No files downloaded." >&2
    exit 1
fi

echo "DroneRF: ${FILE_COUNT} files downloaded to ${DEST}"
date -u > "$MARKER"
echo "Done."
