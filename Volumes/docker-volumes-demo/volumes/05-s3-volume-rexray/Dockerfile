# ============================================================
# Volume type: Amazon S3 bucket, mounted via a Docker VOLUME
# PLUGIN (REX-Ray / vieux s3fs-style plugin), not baked into the image.
# ============================================================
# The application image needs nothing S3-specific — the S3 <-> local
# filesystem translation happens entirely in the volume plugin, which
# runs as a separate Docker managed plugin on the host. See setup.sh.

FROM python:3.12-slim

WORKDIR /app
COPY app.py .

CMD ["python", "app.py"]
