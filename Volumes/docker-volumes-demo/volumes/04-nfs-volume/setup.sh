#!/usr/bin/env bash
# Creates a Docker volume backed by an NFS export, using the built-in
# "local" driver's NFS options (Docker Engine >= 17.06, no plugin required).
set -euo pipefail

# ---- EDIT THESE for your environment ----
NFS_SERVER="192.168.1.100"     # your NFS server's IP or hostname
NFS_PATH="/exports/app-data"   # the exported path on that server
VOLUME_NAME="nfs-app-data"
# ------------------------------------------

docker volume create \
  --driver local \
  --opt type=nfs \
  --opt o="addr=${NFS_SERVER},rw,nfsvers=4" \
  --opt device=":${NFS_PATH}" \
  "${VOLUME_NAME}"

docker build -t volume-demo:nfs .

docker run --rm -v "${VOLUME_NAME}:/data" volume-demo:nfs
