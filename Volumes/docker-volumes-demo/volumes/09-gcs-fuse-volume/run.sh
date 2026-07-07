#!/usr/bin/env bash
set -euo pipefail

docker build -t volume-demo:gcs-fuse .

docker run --rm \
  --cap-add SYS_ADMIN \
  --device /dev/fuse \
  --security-opt apparmor:unconfined \
  -e GCS_BUCKET="my-app-bucket" \
  -e GOOGLE_APPLICATION_CREDENTIALS="/secrets/gcp-key.json" \
  -v "$(pwd)/gcp-key.json:/secrets/gcp-key.json:ro" \
  volume-demo:gcs-fuse
