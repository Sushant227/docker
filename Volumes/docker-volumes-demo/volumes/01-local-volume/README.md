# 01 — Named Volume (`local` driver)

The `local` driver is Docker's built-in default. Docker manages the storage
location on the host (usually under `/var/lib/docker/volumes/`) and the
data survives container restarts/removal.

## Build

```bash
docker build -t volume-demo:local .
```

## Create the volume explicitly (optional — Docker will auto-create it too)

```bash
docker volume create app-data
```

## Run

```bash
docker run --rm -v app-data:/data volume-demo:local
```

Stop it (Ctrl+C), then run it again — `hello.txt` will already contain
previous lines, proving the volume persisted.

## Or with Docker Compose

```bash
docker compose up --build
```

## Inspect / clean up

```bash
docker volume inspect app-data
docker volume rm app-data
```
