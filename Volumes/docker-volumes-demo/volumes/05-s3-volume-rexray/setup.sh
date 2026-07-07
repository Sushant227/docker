#!/usr/bin/env bash
# Mounts an S3 bucket as a Docker volume using the REX-Ray S3FS plugin.
set -euo pipefail

# ---- EDIT THESE ----
AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
S3_BUCKET="my-app-bucket"
VOLUME_NAME="s3-app-data"
# ---------------------

# Install the plugin (one-time)
docker plugin install rexray/s3fs \
  S3FS_ACCESSKEY="${AWS_ACCESS_KEY_ID}" \
  S3FS_SECRETKEY="${AWS_SECRET_ACCESS_KEY}" \
  --grant-all-permissions || true

# Create the volume, backed by the named S3 bucket
docker volume create \
  --driver rexray/s3fs \
  --opt bucket="${S3_BUCKET}" \
  "${VOLUME_NAME}"

docker build -t volume-demo:s3-rexray .

docker run --rm -v "${VOLUME_NAME}:/data" volume-demo:s3-rexray
