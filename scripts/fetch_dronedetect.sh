#!/usr/bin/env bash
set -euo pipefail

# fetch_dronedetect.sh - Download DroneDetect dataset from IEEE DataPort
# Source: https://ieee-dataport.org/open-access/dronedetect-dataset-radio-frequency-dataset-unmanned-aerial-system-uas-signals-machine
# Size: ~3.5GB, 7 DJI/Parrot models, BladeRF SDR
# Includes Bluetooth/WiFi interference variants
#
# MANUAL STEP: IEEE DataPort requires a free account.
# 1. Create an account at https://ieee-dataport.org/
# 2. Navigate to the dataset page above
# 3. Open browser dev tools (F12) -> Network tab
# 4. Click a download link
# 5. Copy the session cookie value
# 6. Export it: export IEEE_TOKEN="your_session_cookie"
# 7. Re-run this script

DEST="$(dirname "$0")/../datasets/rf/dronedetect"
MARKER="${DEST}/.fetched"
DATASET_URL="https://ieee-dataport.org/open-access/dronedetect-dataset-radio-frequency-dataset-unmanned-aerial-system-uas-signals-machine"

if [ -f "$MARKER" ]; then
    echo "DroneDetect already fetched. Remove ${MARKER} to re-download."
    exit 0
fi

mkdir -p "$DEST"

if [ -z "${IEEE_TOKEN:-}" ]; then
    echo "============================================================"
    echo "  IEEE_TOKEN not set - manual authentication required"
    echo "============================================================"
    echo ""
    echo "DroneDetect is hosted on IEEE DataPort and requires a free account."
    echo ""
    echo "Steps:"
    echo "  1. Create a free account at https://ieee-dataport.org/"
    echo "  2. Go to: ${DATASET_URL}"
    echo "  3. Open browser dev tools -> Network tab"
    echo "  4. Click a download link on the dataset page"
    echo "  5. Copy the Cookie header value from the request"
    echo "  6. Run: export IEEE_TOKEN=\"<cookie_value>\""
    echo "  7. Re-run this script"
    echo ""
    exit 1
fi

echo "Fetching DroneDetect dataset page..."
PAGE=$(curl -sS -b "$IEEE_TOKEN" "$DATASET_URL")

# Extract download links from the page
LINKS=$(echo "$PAGE" | grep -oP 'href="[^"]*"' | grep -i 'download\|\.zip\|\.mat\|\.tar' | sed 's/href="//;s/"$//' | sort -u)

if [ -z "$LINKS" ]; then
    echo "WARNING: Could not extract download links. The session token may be invalid." >&2
    echo "Try refreshing your IEEE_TOKEN." >&2
    exit 1
fi

echo "Found download links:"
echo "$LINKS"
echo ""

for url in $LINKS; do
    # Make relative URLs absolute
    case "$url" in
        http*) ;;
        *) url="https://ieee-dataport.org${url}" ;;
    esac

    FILENAME=$(basename "$url" | sed 's/?.*//')
    if [ -f "${DEST}/${FILENAME}" ]; then
        echo "  SKIP ${FILENAME} (exists)"
        continue
    fi
    echo "  Downloading ${FILENAME}..."
    curl -L -b "$IEEE_TOKEN" -o "${DEST}/${FILENAME}" "$url"
done

FILE_COUNT=$(find "$DEST" -maxdepth 1 -type f ! -name '.fetched' | wc -l)
if [ "$FILE_COUNT" -eq 0 ]; then
    echo "ERROR: No files downloaded." >&2
    exit 1
fi

echo "DroneDetect: ${FILE_COUNT} files downloaded to ${DEST}"
date -u > "$MARKER"
echo "Done."
