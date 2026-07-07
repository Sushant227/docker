# ============================================================
# Volume type: Amazon S3 bucket, mounted FROM INSIDE the container
# using s3fs-fuse (alternative to the plugin-based approach).
# ============================================================
# Requires the container to run with --cap-add SYS_ADMIN and
# --device /dev/fuse (or --privileged) on the host, since FUSE
# mounts need elevated permissions.

FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends s3fs fuse python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --break-system-packages boto3

WORKDIR /app
COPY app.py .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "app.py"]
