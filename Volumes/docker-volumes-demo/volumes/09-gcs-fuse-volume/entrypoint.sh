#!/bin/bash
set -euo pipefail

: "${GCS_BUCKET:?Set GCS_BUCKET env var}"
# Expects a mounted service-account key file at /secrets/gcp-key.json
# (see run.sh), referenced via GOOGLE_APPLICATION_CREDENTIALS.

mkdir -p /data

gcsfuse --key-file "${GOOGLE_APPLICATION_CREDENTIALS}" "${GCS_BUCKET}" /data

echo "Mounted gs://${GCS_BUCKET} at /data"

exec "$@"
