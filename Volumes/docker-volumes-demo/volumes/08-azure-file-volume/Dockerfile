# ============================================================
# Volume type: Azure Files share, mounted via the "azure_file"
# Docker volume driver on Docker EE/Azure VMs, or via the
# CloudStor plugin on Docker Swarm.
# ============================================================
# No special packages needed in the app image — Azure File share
# access is configured entirely at `docker volume create` time.

FROM python:3.12-slim

WORKDIR /app
COPY app.py .

CMD ["python", "app.py"]
