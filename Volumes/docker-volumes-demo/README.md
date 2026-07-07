# Docker Volume Types & Drivers — Reference Project

A collection of self-contained examples, one per Docker volume type /
storage driver, each with its own `Dockerfile`, **purpose-built Python
source code**, mount/setup commands, and `README.md`. Every example's
`app.py` is tailored to demonstrate the specific behavior that makes
that volume type distinct — not just a generic file write.

## Layout

```
docker-volumes-demo/
└── volumes/
    ├── 01-local-volume/         # named volume, "local" driver — persistent counter
    ├── 02-bind-mount/           # host bind mount — shows host-inherited ownership
    ├── 03-tmpfs/                # in-memory mount — proves data does NOT survive restarts
    ├── 04-nfs-volume/           # NFS share — multi-client shared-write demo
    ├── 05-s3-volume-rexray/     # S3 via REX-Ray plugin — JSON "objects" written as files
    ├── 06-s3-volume-s3fs-fuse/  # S3 via s3fs-fuse — cross-checks filesystem view vs boto3 API
    ├── 07-ebs-volume-rexray/    # EBS via REX-Ray plugin — block writes + disk usage stats
    ├── 08-azure-file-volume/    # Azure Files (SMB) — multi-client shared-write demo
    └── 09-gcs-fuse-volume/      # GCS via gcsfuse — cross-checks filesystem view vs GCS API
```

Each subfolder is a **complete, independent build context** with its
own `app.py`, `Dockerfile`, and `README.md` — `cd` into one and follow
its own instructions.

### What each `app.py` actually demonstrates

| # | Source code behavior |
|---|---|
| 01 | Loads a JSON counter from `/data` on startup and increments it forever — restart the container and the count keeps climbing instead of resetting, proving the named volume persisted. |
| 02 | Reads and prints the UID/GID that owns `/data` (inherited straight from the host directory), then appends a log line — edit the file from the host and see it reflected instantly. |
| 03 | Checks `/proc/mounts` to confirm `/data` really is `tmpfs`, then shows that any file written there is empty again after a restart (RAM-only storage). |
| 04 | Accepts a `CLIENT_ID` env var and appends to one shared file; `run-multi.sh` starts two containers at once so you can watch both clients' writes land in the same NFS-backed file. |
| 05 | Writes incrementing JSON "record" files into `/data` and lists the directory — the REX-Ray/S3FS plugin makes an S3 bucket look like an ordinary folder. |
| 06 | Writes JSON files through the s3fs FUSE mount, then independently calls the real `boto3` S3 API to list the same bucket, printing both views side by side. |
| 07 | Appends 1 MB chunks to a file and calls `fsync()` after each write, then prints `shutil.disk_usage()` stats — exercising `/data` as genuine block storage rather than an object store. |
| 08 | Same multi-client pattern as NFS (04), but over an Azure Files SMB share; `run-multi.sh` again starts two containers writing to the same share. |
| 09 | Same dual-verification pattern as S3 (06), but calls the `google-cloud-storage` API to independently confirm what gcsfuse shows at `/data`. |

## Quick reference: which mechanism does what

| # | Volume type | Mechanism | Runs anywhere? |
|---|---|---|---|
| 01 | Named volume | Docker's built-in `local` driver | ✅ any host |
| 02 | Bind mount | Direct host path mapping | ✅ any host |
| 03 | tmpfs | In-RAM mount, non-persistent | ✅ any Linux host |
| 04 | NFS | `local` driver with `type=nfs` options | ✅ any host + NFS server |
| 05 | S3 | `rexray/s3fs` Docker volume **plugin** | ✅ any host + AWS creds |
| 06 | S3 | `s3fs-fuse` baked into the image, mounted at container start | ⚠️ needs FUSE + SYS_ADMIN cap |
| 07 | EBS | `rexray/ebs` Docker volume **plugin** | ❌ EC2 instance only |
| 08 | Azure Files | `cloudstor:azure` plugin, or host-level CIFS mount | ⚠️ Swarm/EE, or CIFS-capable host |
| 09 | GCS | `gcsfuse` baked into the image, mounted at container start | ⚠️ needs FUSE + SYS_ADMIN cap |

**General pattern:** cloud object/block storage (S3, EBS, GCS, Azure
Files) is *not* natively understood by Docker — you either (a) install
a **Docker volume plugin** that speaks the Docker Volume Driver API
(REX-Ray, CloudStor) so the app image stays completely untouched, or
(b) bake a **FUSE client** into the image and mount the remote storage
yourself at container start (s3fs, gcsfuse). Option (a) is generally
preferred for production because your application image has zero
cloud-provider coupling.

## Building every image at once

```bash
for d in volumes/*/; do
  name=$(basename "$d")
  tag="volume-demo:${name#*-}"
  echo "Building $tag from $d"
  docker build -t "$tag" "$d"
done
```

## Running an individual example

```bash
cd volumes/01-local-volume
docker build -t volume-demo:local .
docker run --rm -v app-data:/data volume-demo:local
```

Some examples (04, 05, 06, 07, 08, 09) need external resources (an NFS
server, an S3 bucket + AWS creds, an EC2 host, etc.) — see each
folder's own `README.md`/`setup.sh` for exactly what to fill in before
running.

## Cleanup

```bash
docker volume ls
docker volume rm <name>
docker images | grep volume-demo
docker rmi <image>
```
