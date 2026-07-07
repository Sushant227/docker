# 04 — NFS Volume (built-in `local` driver, no plugin)

Docker's default `local` volume driver can mount NFS shares directly —
no third-party plugin required. This requires an NFS server that's
already reachable from the Docker host, and the host needs `nfs-common`
(Debian/Ubuntu) or `nfs-utils` (RHEL/CentOS) installed so the kernel can
speak the NFS protocol.

## 1. Install NFS client tools on the Docker HOST (not the container)

```bash
# Debian/Ubuntu
sudo apt-get install -y nfs-common

# RHEL/CentOS/Amazon Linux
sudo yum install -y nfs-utils
```

## 2. Edit `setup.sh`

Set `NFS_SERVER` and `NFS_PATH` to match your NFS export, e.g. an
AWS EFS mount target, a NAS, or a self-hosted `nfs-kernel-server`.

## 3. Run it

```bash
chmod +x setup.sh
./setup.sh
```

This is equivalent to running manually:

```bash
docker volume create \
  --driver local \
  --opt type=nfs \
  --opt o=addr=192.168.1.100,rw,nfsvers=4 \
  --opt device=:/exports/app-data \
  nfs-app-data

docker build -t volume-demo:nfs .
docker run --rm -v nfs-app-data:/data volume-demo:nfs
```

## Verify

Because the data lives on the NFS server, you can mount the same
export on another host/container and see the same `hello.txt` growing.

## Notes

- `nfsvers=3` also works if your server doesn't support v4.
- For AWS EFS, `NFS_SERVER` is the EFS mount target DNS name and
  `NFS_PATH` is usually just `/`.
- Cleanup: `docker volume rm nfs-app-data`
