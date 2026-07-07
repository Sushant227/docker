# 09 — Google Cloud Storage Mounted Inside the Container via `gcsfuse`

There's no official Docker volume plugin for GCS (unlike REX-Ray for
S3/EBS), so the standard approach is baking `gcsfuse` into the image
and mounting the bucket at container startup — the same pattern as
example 06 for S3.

## Prerequisites

- A GCS bucket
- A GCP service account JSON key with `roles/storage.objectAdmin`
  (or narrower) on that bucket, saved locally as `gcp-key.json`
- Container needs `--cap-add SYS_ADMIN` and `--device /dev/fuse`

## Build & Run

```bash
chmod +x run.sh
# place your service account key at ./gcp-key.json first
./run.sh
```

Or manually:

```bash
docker build -t volume-demo:gcs-fuse .

docker run --rm \
  --cap-add SYS_ADMIN \
  --device /dev/fuse \
  -e GCS_BUCKET=my-app-bucket \
  -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/gcp-key.json \
  -v "$(pwd)/gcp-key.json:/secrets/gcp-key.json:ro" \
  volume-demo:gcs-fuse
```

## Verify

```bash
gcloud storage ls gs://my-app-bucket/
```

## Notes

- On GKE, the modern equivalent is the **GCS FUSE CSI driver**
  (`gke-gcsfuse-csi-driver`), which does this same job at the
  Kubernetes volume layer instead of inside your own image.
- Running on a GCE VM with an attached service account, you can drop
  the key file entirely — `gcsfuse` will use the VM's metadata-server
  credentials automatically.
