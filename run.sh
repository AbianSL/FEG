#!/usr/bin/env bash
set -euo pipefail

DEFAULT_IMAGE="source/NGC0237_i.fits"
DEFAULT_CONFIG="configs/config_exponential_ic3478_256.dat"
DEFAULT_MODEL="model.fits"
DEFAULT_RESIDUAL="resid.fits"
# DEFAULT_MASK="mask.fits"

for f in "$DEFAULT_IMAGE" "$DEFAULT_CONFIG"; do
    if [ ! -f "$f" ]; then
        echo "Error: Required file '$f' not found." >&2
        exit 1
    fi
done

EXPANDED_ARGS=()
for arg in "$@"; do
    case "$arg" in
        --save | -s)
            EXPANDED_ARGS+=(--save-model "$DEFAULT_MODEL" --save-residual "$DEFAULT_RESIDUAL")
            ;;
        *)
            EXPANDED_ARGS+=("$arg")
            ;;
    esac
done

BASE_CMD=(imfit "$DEFAULT_IMAGE" -c "$DEFAULT_CONFIG")

echo ">> Running: ${BASE_CMD[*]} ${EXPANDED_ARGS[*]}"
"${BASE_CMD[@]}" "${EXPANDED_ARGS[@]}"
