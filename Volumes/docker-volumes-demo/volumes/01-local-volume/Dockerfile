# ============================================================
# Volume type: Named volume, "local" driver (Docker's default)
# ============================================================
# This is the standard, built-in volume driver. No extra packages
# are needed in the image itself — the volume is created and
# managed entirely by the Docker daemon and mounted at /data.

FROM python:3.12-slim

WORKDIR /app
COPY app.py .

# The mount point the volume will be attached to
VOLUME ["/data"]

CMD ["python", "app.py"]
