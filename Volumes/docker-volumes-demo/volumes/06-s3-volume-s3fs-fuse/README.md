# 06 — S3 Mounted Inside the Container via `s3fs-fuse`

Unlike example 05 (which uses a Docker volume plugin running on the
host), this approach bakes the `s3fs` FUSE client **into the image
itself**, and the container mounts the S3 bucket at startup via its
entrypoint script.

This is useful when you can't install host-level Docker plugins (e.g.
in some managed/restricted container platforms) but can still grant
the container extra Linux capabilities.

## Requirements

The container needs FUSE device access, which means running with:

- `--cap-add SYS_ADMIN`
- `--device /dev/fuse`
- (and on some hosts) `--security-opt apparmor:unconfined`

This is broader than a normal container's permissions, so treat it
like you would `--privileged` from a security standpoint.

## Build & Run

Edit `run.sh` with your bucket name and AWS credentials, then:

```bash
chmod +x run.sh
./run.sh
```

Or manually:

```bash
docker build -t volume-demo:s3-fuse .

docker run --rm \
  --cap-add SYS_ADMIN \
  --device /dev/fuse \
  -e S3_BUCKET=my-app-bucket \
  -e AWS_ACCESS_KEY_ID=... \
  -e AWS_SECRET_ACCESS_KEY=... \
  volume-demo:s3-fuse
```

## Verify

```bash
aws s3 ls s3://my-app-bucket/
```

## Trade-offs vs. the plugin approach (example 05)

| | Plugin (rexray/s3fs) | Baked-in s3fs (this example) |
|---|---|---|
| App image stays generic | ✅ | ❌ (couples image to S3) |
| Needs host-level plugin install | ✅ required | ❌ not required |
| Container privilege needed | Normal | Elevated (SYS_ADMIN + /dev/fuse) |
| Portable to managed platforms (ECS Fargate, etc.) | Sometimes limited | Sometimes limited (FUSE support varies) |
