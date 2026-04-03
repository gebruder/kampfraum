#!/usr/bin/env bash
set -euo pipefail

# fetch_rfuav.sh - Clone/download RFUAV dataset
# Source: https://github.com/kitoweeknd/RFUAV
# Size: ~1.3TB, 37 UAV types, variable SNR, USRP-collected

DEST="$(dirname "$0")/../datasets/rf/rfuav"
MARKER="${DEST}/.fetched"

if [ -f "$MARKER" ]; then
    echo "RFUAV already fetched. Remove ${MARKER} to re-download."
    exit 0
fi

echo "Cloning RFUAV repository..."
if [ -d "$DEST" ]; then
    echo "  Directory exists, pulling latest..."
    git -C "$DEST" pull
else
    git clone https://github.com/kitoweeknd/RFUAV "$DEST"
fi

# Check for external data pointers (README instructions, download links)
if [ -f "${DEST}/README.md" ]; then
    echo ""
    echo "=== RFUAV README - check for additional download instructions ==="
    # Extract any URLs pointing to external data
    grep -iE '(download|data|drive\.google|mega\.nz|zenodo|kaggle|dropbox|onedrive)' "${DEST}/README.md" || true
    echo "=== end ==="
    echo ""
    echo "NOTE: RFUAV is 1.3TB. The git repo may contain only metadata/pointers."
    echo "Review the README above for external download links and follow manually."
fi

date -u > "$MARKER"
echo "RFUAV cloned to ${DEST}"
echo "Done."
