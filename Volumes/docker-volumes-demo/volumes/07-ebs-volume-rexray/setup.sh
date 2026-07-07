#!/usr/bin/env bash
# Provisions/attaches an EBS volume as a Docker volume using the
# REX-Ray EBS plugin. MUST be run on an EC2 instance whose IAM
# instance role has ec2:AttachVolume / DetachVolume / CreateVolume etc.
set -euo pipefail

VOLUME_NAME="ebs-app-data"
VOLUME_SIZE_GB="10"

# Install the plugin (one-time per host)
docker plugin install rexray/ebs \
  EBS_REGION="us-east-1" \
  --grant-all-permissions || true

# Create a new EBS-backed Docker volume (REX-Ray provisions the
# actual EBS volume in AWS automatically)
docker volume create \
  --driver rexray/ebs \
  --opt size="${VOLUME_SIZE_GB}" \
  --opt volumetype=gp3 \
  "${VOLUME_NAME}"

docker build -t volume-demo:ebs-rexray .

docker run --rm -v "${VOLUME_NAME}:/data" volume-demo:ebs-rexray
