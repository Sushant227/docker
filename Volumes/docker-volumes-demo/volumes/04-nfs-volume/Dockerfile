# ============================================================
# Volume type: NFS share, mounted via Docker's built-in
# "local" driver with NFS-specific options (no plugin needed)
# ============================================================
# The container image itself needs nothing special — the NFS mount
# is handled by the Docker daemon/host kernel. All NFS configuration
# happens in `docker volume create`, shown in setup.sh / README.md.

FROM python:3.12-slim

WORKDIR /app
COPY app.py .

CMD ["python", "app.py"]
