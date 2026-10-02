#!/usr/bin/env bash
set -euo pipefail

show_help() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS] [EXTRA_IMFIT_ARGS...]

Wrapper script to run imfit using preconfigured default files.

Options:
  -s, --save       Save the default model and residual images:
                   --save-model "$DEFAULT_MODEL"
                   --save-residual "$DEFAULT_RESIDUAL"
  -p, --psd        Include the default PSF:
                   --psf "$DEFAULT_PSF"
  -h, --help       Display this help message and exit.

Required default files:
  Image:           $DEFAULT_IMAGE
  Config:          $DEFAULT_CONFIG

Any unrecognized arguments are passed directly to 'imfit'.
EOF
}

DEFAULT_IMAGE="source/NGC0237_i.fits"
DEFAULT_CONFIG="configs/config_exponential_ic3478_256.dat"
DEFAULT_PSF="configs/config_makeimage_moffat_psf.dat"
DEFAULT_MODEL="model.fits"
DEFAULT_RESIDUAL="resid.fits"
# DEFAULT_MASK="mask.fits"

for arg in "$@"; do
    case "$arg" in
        -h|--help)
            show_help
            exit 0
            ;;
    esac
done

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
        --psd | -p)
            EXPANDED_ARGS+=(--psf "$DEFAULT_PSF")
            ;;
        *)
            EXPANDED_ARGS+=("$arg")
            ;;
    esac
done

BASE_CMD=(imfit "$DEFAULT_IMAGE" -c "$DEFAULT_CONFIG")

echo ">> Running: ${BASE_CMD[*]} ${EXPANDED_ARGS[*]}"
"${BASE_CMD[@]}" "${EXPANDED_ARGS[@]}"
