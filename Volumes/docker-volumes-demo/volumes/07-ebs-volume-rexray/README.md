# 07 — EBS Volume via REX-Ray Plugin

EBS volumes are AWS block storage devices that attach to a single EC2
instance at a time. The `rexray/ebs` Docker plugin automates
create/attach/format/mount so a normal `docker volume create` +
`docker run -v` is all you need — same UX as the S3 example, but
backed by durable, high-IOPS block storage instead of object storage.

## Prerequisites

- **Must run on an EC2 instance** (EBS can't attach to non-AWS hosts)
- IAM role/credentials with EBS permissions: `ec2:CreateVolume`,
  `ec2:AttachVolume`, `ec2:DetachVolume`, `ec2:DescribeVolumes`,
  `ec2:DescribeInstances`, `ec2:CreateTags`

## Build & Run

Edit the region in `setup.sh` if needed, then:

```bash
chmod +x setup.sh
./setup.sh
```

Equivalent manual steps:

```bash
docker plugin install rexray/ebs EBS_REGION=us-east-1 --grant-all-permissions

docker volume create \
  --driver rexray/ebs \
  --opt size=10 \
  --opt volumetype=gp3 \
  ebs-app-data

docker build -t volume-demo:ebs-rexray .
docker run --rm -v ebs-app-data:/data volume-demo:ebs-rexray
```

## Verify

```bash
docker volume inspect ebs-app-data
aws ec2 describe-volumes --filters Name=tag:Name,Values=ebs-app-data
```

## Notes

- The volume follows the container: if you `docker run` the same
  volume from a *different* EC2 instance, REX-Ray detaches it from
  the old instance and attaches it to the new one automatically.
- For Kubernetes instead of raw Docker, the modern equivalent is the
  **AWS EBS CSI driver**, not REX-Ray (REX-Ray predates CSI and is
  now in maintenance mode — mentioned here since the question asked
  about Docker volume drivers specifically).

## Cleanup

```bash
docker volume rm ebs-app-data   # also deletes the underlying EBS volume
```
