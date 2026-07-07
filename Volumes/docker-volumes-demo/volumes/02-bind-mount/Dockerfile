# ============================================================
# Volume type: Bind mount
# ============================================================
# A bind mount maps an existing path on the HOST filesystem directly
# into the container. Docker does no management of it at all — it's
# just a pass-through mount. No special image config is needed;
# the mount is specified entirely at `docker run` time.

FROM python:3.12-slim

WORKDIR /app
COPY app.py .

CMD ["python", "app.py"]
