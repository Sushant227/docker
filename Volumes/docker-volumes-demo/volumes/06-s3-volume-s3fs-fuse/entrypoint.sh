#!/bin/bash
set -euo pipefail

: "${S3_BUCKET:?Set S3_BUCKET env var}"
: "${AWS_ACCESS_KEY_ID:?Set AWS_ACCESS_KEY_ID env var}"
: "${AWS_SECRET_ACCESS_KEY:?Set AWS_SECRET_ACCESS_KEY env var}"

mkdir -p /data
echo "${AWS_ACCESS_KEY_ID}:${AWS_SECRET_ACCESS_KEY}" > /etc/passwd-s3fs
chmod 600 /etc/passwd-s3fs

s3fs "${S3_BUCKET}" /data \
  -o passwd_file=/etc/passwd-s3fs \
  -o allow_other \
  -o umask=0022

echo "Mounted s3://${S3_BUCKET} at /data"

exec "$@"
