# 08 — Azure Files Volume

Azure Files exposes SMB/NFS file shares that multiple hosts/containers
can mount concurrently — conceptually similar to NFS/EFS but on Azure.
On plain Docker Engine (non-Swarm) hosts, the simplest path is often
to mount the Azure File share as a native OS-level CIFS mount and
then bind-mount that path in — but the example below uses the
`cloudstor` plugin approach, which mirrors the REX-Ray pattern used
for S3/EBS above and works well on Docker Swarm / Docker EE for Azure.

## Prerequisites

- An Azure Storage Account and a File Share created inside it
- The storage account access key

## Build & Run

Edit `setup.sh` with your storage account name, key, and share name:

```bash
chmod +x setup.sh
./setup.sh
```

## Alternative: plain CIFS mount (no plugin, works on any Linux Docker host)

If you're not on Docker Swarm/EE, you can mount the Azure File share
as a regular CIFS mount on the host and bind-mount it in:

```bash
sudo mkdir -p /mnt/azurefiles
sudo mount -t cifs //mystorageaccount.file.core.windows.net/app-data-share \
  /mnt/azurefiles \
  -o username=mystorageaccount,password=YOUR_STORAGE_ACCOUNT_KEY,serverino,vers=3.0

docker build -t volume-demo:azure-file .
docker run --rm -v /mnt/azurefiles:/data volume-demo:azure-file
```

## Verify

```bash
az storage file list --share-name app-data-share --account-name mystorageaccount
```

## Cleanup

```bash
docker volume rm azure-app-data
```
