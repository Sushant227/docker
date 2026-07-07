#!/usr/bin/env bash
set -euo pipefail

docker build -t volume-demo:s3-fuse .

docker run --rm \
  --cap-add SYS_ADMIN \
  --device /dev/fuse \
  --security-opt apparmor:unconfined \
  -e S3_BUCKET="my-app-bucket" \
  -e AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY" \
  -e AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY" \
  volume-demo:s3-fuse
