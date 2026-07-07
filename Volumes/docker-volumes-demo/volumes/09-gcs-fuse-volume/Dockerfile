# ============================================================
# Volume type: Google Cloud Storage bucket, mounted FROM INSIDE
# the container using gcsfuse.
# ============================================================
# Like the s3fs-fuse example, this requires --cap-add SYS_ADMIN
# and --device /dev/fuse at `docker run` time.

FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl gnupg fuse ca-certificates \
    && echo "deb https://packages.cloud.google.com/apt gcsfuse-bookworm main" \
       > /etc/apt/sources.list.d/gcsfuse.list \
    && curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg \
       | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg \
    && apt-get update \
    && apt-get install -y --no-install-recommends gcsfuse python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --break-system-packages google-cloud-storage

WORKDIR /app
COPY app.py .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "app.py"]
