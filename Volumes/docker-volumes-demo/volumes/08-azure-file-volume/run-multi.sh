#!/usr/bin/env bash
# Runs TWO containers concurrently against the SAME Azure Files-backed
# volume to demonstrate multi-client shared SMB access.
set -euo pipefail

VOLUME_NAME="azure-app-data"

docker build -t volume-demo:azure-file .

docker run -d --rm --name azure-client-a \
  -e CLIENT_ID=client-a \
  -v "${VOLUME_NAME}:/data" \
  volume-demo:azure-file

docker run -d --rm --name azure-client-b \
  -e CLIENT_ID=client-b \
  -v "${VOLUME_NAME}:/data" \
  volume-demo:azure-file

echo "Started azure-client-a and azure-client-b, both writing to the same share."
echo "Tail their logs with:"
echo "  docker logs -f azure-client-a"
echo "  docker logs -f azure-client-b"
echo "Stop both with:"
echo "  docker stop azure-client-a azure-client-b"
