# Docker Named Volume Demo

Demonstrates Docker's **named volume** (the `local` driver — Docker's
built-in, default volume type). Docker manages the storage location on
the host for you; you just refer to the volume by name.

## Files

- `app.py` — writes a JSON counter to `/data/counter.json`, incrementing
  it forever. On startup it loads whatever count was last saved, so you
  can prove the volume's data survives container restarts.
- `Dockerfile` — builds the image; declares `/data` as the mount point.
- `docker-compose.yml` — optional, same setup via Compose.

## Build

```bash
docker build -t named-volume-demo .
```

## Create the volume (optional — Docker auto-creates it on first use too)

```bash
docker volume create app-data
```

## Run

```bash
docker run --rm -v app-data:/data named-volume-demo
```

You'll see output like:

```
Starting up. Previous count found in volume: 0
[local-volume] count=1 (restart the container — this number keeps climbing, proving the volume persisted)
[local-volume] count=2 ...
```

Stop it with `Ctrl+C`, then run the exact same command again — the
counter picks up where it left off instead of resetting to 0.

## Or with Docker Compose

```bash
docker compose up --build
```

## Inspect the volume

```bash
docker volume inspect app-data
```

## Peek at the raw data (advanced)

Named volumes live under Docker's storage area, not a path you chose.
To look inside without stopping your app, mount it read-only into a
throwaway container:

```bash
docker run --rm -v app-data:/data:ro alpine cat /data/counter.json
```

## Clean up

```bash
docker volume rm app-data
docker rmi named-volume-demo
```
