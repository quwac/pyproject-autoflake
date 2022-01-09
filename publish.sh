#!/bin/bash

set -eux

if [ ! -f "./pypi.env" ]; then
    echo "./pypi.env not found."
    exit 1
fi

# shellcheck disable=SC1091
source "./pypi.env"

# shellcheck disable=SC2154
poetry publish --build \
    -r "$repository" \
    -u "$username" \
    -p "$password"
