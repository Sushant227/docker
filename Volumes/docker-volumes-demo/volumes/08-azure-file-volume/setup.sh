#!/usr/bin/env bash
# Mounts an Azure Files share as a Docker volume using the CloudStor
# plugin (works on Docker EE / Docker Swarm on Azure).
set -euo pipefail

# ---- EDIT THESE ----
AZURE_STORAGE_ACCOUNT="mystorageaccount"
AZURE_STORAGE_KEY="YOUR_STORAGE_ACCOUNT_KEY"
SHARE_NAME="app-data-share"
VOLUME_NAME="azure-app-data"
# ---------------------

docker plugin install docker4x/cloudstor:azure \
  --grant-all-permissions \
  --alias cloudstor || true

docker volume create \
  --driver cloudstor:azure \
  --opt shareName="${SHARE_NAME}" \
  --opt storageAccount="${AZURE_STORAGE_ACCOUNT}" \
  --opt storageAccountKey="${AZURE_STORAGE_KEY}" \
  "${VOLUME_NAME}"

docker build -t volume-demo:azure-file .

docker run --rm -v "${VOLUME_NAME}:/data" volume-demo:azure-file
