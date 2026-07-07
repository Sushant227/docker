# ============================================================
# Volume type: AWS EBS volume, mounted via the REX-Ray EBS
# Docker volume plugin. Must run ON an EC2 instance.
# ============================================================
# The app image needs nothing EBS-specific — REX-Ray handles
# attaching/formatting/mounting the EBS volume to the host, and
# Docker bind-mounts that formatted filesystem into the container.

FROM python:3.12-slim

WORKDIR /app
COPY app.py .

CMD ["python", "app.py"]
