#!/bin/bash
# Script to prepare the build environment for Adan.
#
# Example usage:
#   ./prepare_for_build.sh main

set -euxo pipefail

export ROOT=`pwd`

if [ $# -ne 1 ]; then
    echo "Usage: $0 <adan_version>"
    echo "Example: $0 main"
    exit 1
fi

ADAN_VERSION=$1

# Apply patches.
patch_dir="${ROOT}/build_scripts/patches/${ADAN_VERSION}"

# Not all Adan versions need patches.
if [ ! -d "${patch_dir}" ]; then
    echo "Warning: nothing to patch: patches/${ADAN_VERSION} directory does not exist"
else
    for patch in "${patch_dir}"/*.patch; do
        # Skip if no patch files exist (only .gitkeep)
        if [ -f "${patch}" ]; then
            patch -p1 -d "${ROOT}" -i "${patch}"
        fi
    done
fi
