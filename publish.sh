#!/bin/bash

set -eu

# shellcheck disable=SC2046,SC2086
PROJECT_PATH="$(cd $(dirname $0) && pwd)"
DIST_PATH="$PROJECT_PATH/dist"
PYPI_ENV_PATH=$1

if [ ! -f "$PYPI_ENV_PATH" ]; then
    echo "$PYPI_ENV_PATH not found."
    exit 1
fi

if [ -e "$DIST_PATH" ]; then
    rm -rf "$DIST_PATH"
fi

# shellcheck disable=SC1090,SC1091
source "$PYPI_ENV_PATH"

# shellcheck disable=SC2154
poetry publish \
    -r "$repository" \
    -u "$username" \
    -p "$password" \
    --build
