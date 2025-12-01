#!/usr/bin/env bash

# Non-interactive downloader for HSC Shirasaki_mocks
# Requires:
#   export HSC_USER="yourname"
#   export HSC_PASS="your_password"
#   bash download_all_from_hsc-release.sh

set -euo pipefail

BASE_URL="https://hsc-release.mtk.nao.ac.jp/archive/filetree/s16a-shape-catalog/pdr1_hscwl"
SHA_FILE="sha256sum.txt"

main() {
    # --- Credentials ---
    if [[ -z "${HSC_USER:-}" || -z "${HSC_PASS:-}" ]]; then
        echo "ERROR: HSC_USER and HSC_PASS must be exported before running." >&2
        exit 1
    fi

    echo "Using HSC_USER=${HSC_USER}"
    echo "Fetching file list from ${BASE_URL} ..."

    # --- Download the full sha256 list ---
    wget \
        --user="${HSC_USER}" \
        --password="${HSC_PASS}" \
        "${BASE_URL}/sha256sum.txt" \
        -O "${SHA_FILE}"

    # --- Filter to just Shirasaki_mocks FITS files ---
    grep 'Shirasaki_mocks/.*\.fits' "${SHA_FILE}" > "${SHA_FILE}.tmp"
    mv "${SHA_FILE}.tmp" "${SHA_FILE}"

    echo "Filtered sha256 list written to ${SHA_FILE}"

    # --- Compute cut-dirs for wget so paths start at Shirasaki_mocks/ ---
    # Count slashes in BASE_URL and subtract 2 (scheme://host)
    local slashes cutdirs
    slashes="${BASE_URL//[^\/]/}"
    cutdirs=$(( ${#slashes} - 2 ))

    # --- Build a URL list for wget ---
    # sha256 line format is typically:
    #   HASH  *./Shirasaki_mocks/.../file.fits
    # We want:
    #   https://.../Shirasaki_mocks/.../file.fits
    echo "Building URL list ..."
    awk '{print $2}' "${SHA_FILE}" \
        | sed 's/^\*\.\///' \
        | sed "s|^|${BASE_URL}/|" \
        > urls.txt

    echo "URL list written to urls.txt"

    # --- Download all FITS files ---
    echo "Starting bulk download ..."
    wget \
        --user="${HSC_USER}" \
        --password="${HSC_PASS}" \
        --force-directories \
        --no-host-directories \
        --cut-dirs="${cutdirs}" \
        --input-file=urls.txt

    echo "Download finished. Verifying checksums ..."

    # --- Verify SHA256 checksums ---
    if [ -t 1 ]; then
        # Pretty progress display if stdout is a TTY
        sha256sum -c "${SHA_FILE}" | (
            numok=0
            prevok=false
            while read -r line; do
                if [[ $line = *": OK" ]]; then
                    numok=$((numok + 1))
                    echo -n "hash OK: $numok"$'\r'
                    prevok=true
                else
                    if [ "$prevok" != "false" ]; then
                        echo    # newline before error
                        echo "$line"
                    else
                        echo "$line"
                    fi
                    prevok=false
                fi
            done
            echo    # final newline
        )
    else
        # Non-interactive environment, just dump all output
        sha256sum -c "${SHA_FILE}"
    fi

    echo "All done."
}

# Clean locale side-effects like original script
unset "${!LC_@}" || true
export LANG=C

main "$@"
