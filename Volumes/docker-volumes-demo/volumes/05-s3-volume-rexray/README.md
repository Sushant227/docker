# 05 — S3 Volume via REX-Ray Plugin (recommended approach)

This uses a **Docker managed plugin** (`rexray/s3fs`) that implements the
Docker Volume Driver API. The plugin runs outside your app container and
handles the S3 <-> filesystem translation; your application container
just sees a normal directory at `/data`.

This is the cleanest approach because your application image stays
100% generic — no FUSE, no AWS SDK, no extra packages baked in.

## 1. Prerequisites

- Docker Engine with plugin support (v1.13+)
- An S3 bucket and IAM credentials with read/write access to it

## 2. Edit `setup.sh`

Fill in `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `S3_BUCKET`.

> In production, prefer an IAM instance role (on EC2) over static keys —
> the plugin also supports picking up credentials from the instance
> metadata service automatically if you omit the key options.

## 3. Run it

```bash
chmod +x setup.sh
./setup.sh
```

Equivalent manual steps:

```bash
docker plugin install rexray/s3fs \
  S3FS_ACCESSKEY=... \
  S3FS_SECRETKEY=... \
  --grant-all-permissions

docker volume create --driver rexray/s3fs --opt bucket=my-app-bucket s3-app-data

docker build -t volume-demo:s3-rexray .
docker run --rm -v s3-app-data:/data volume-demo:s3-rexray
```

## Verify

Check the S3 bucket in the AWS Console (or `aws s3 ls s3://my-app-bucket/`)
— you should see `hello.txt` appear there.

## Cleanup

```bash
docker volume rm s3-app-data
docker plugin disable rexray/s3fs
docker plugin rm rexray/s3fs
```
