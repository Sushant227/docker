#!/usr/bin/env bash
set -euo pipefail

docker build -t volume-demo:tmpfs .

docker run --rm \
  --tmpfs /data:rw,size=64m,mode=1777 \
  volume-demo:tmpfs
