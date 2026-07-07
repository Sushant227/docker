# ============================================================
# Volume type: tmpfs mount
# ============================================================
# tmpfs mounts live only in the host's memory (RAM) and are never
# written to disk. Data does NOT persist across container restarts
# or removal — great for secrets, caches, or scratch space.

FROM python:3.12-slim

WORKDIR /app
COPY app.py .

CMD ["python", "app.py"]
