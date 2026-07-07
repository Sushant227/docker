#!/usr/bin/env bash
# Runs TWO containers concurrently against the SAME NFS-backed volume
# to demonstrate multi-client shared access — something a local volume
# or bind mount can't easily do across separate hosts.
set -euo pipefail

VOLUME_NAME="nfs-app-data"

docker build -t volume-demo:nfs .

docker run -d --rm --name nfs-client-a \
  -e CLIENT_ID=client-a \
  -v "${VOLUME_NAME}:/data" \
  volume-demo:nfs

docker run -d --rm --name nfs-client-b \
  -e CLIENT_ID=client-b \
  -v "${VOLUME_NAME}:/data" \
  volume-demo:nfs

echo "Started nfs-client-a and nfs-client-b, both writing to the same NFS share."
echo "Tail their logs with:"
echo "  docker logs -f nfs-client-a"
echo "  docker logs -f nfs-client-b"
echo "Stop both with:"
echo "  docker stop nfs-client-a nfs-client-b"
