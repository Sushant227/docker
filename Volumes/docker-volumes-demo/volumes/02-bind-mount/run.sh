#!/usr/bin/env bash
# Creates a host directory and bind-mounts it into the container.
set -euo pipefail

HOST_DIR="$(pwd)/host-data"
mkdir -p "$HOST_DIR"

docker build -t volume-demo:bind .

docker run --rm \
  -v "$HOST_DIR:/data" \
  volume-demo:bind
