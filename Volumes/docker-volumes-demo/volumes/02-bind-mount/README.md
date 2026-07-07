# 02 — Bind Mount

A bind mount points at a specific path that already exists on the host
(e.g. `./host-data`) and maps it straight into the container. There's no
Docker-managed volume object involved — just a host path.

## Build & Run

```bash
chmod +x run.sh
./run.sh
```

Or manually:

```bash
docker build -t volume-demo:bind .
mkdir -p ./host-data
docker run --rm -v "$(pwd)/host-data:/data" volume-demo:bind
```

## Verify

```bash
cat ./host-data/hello.txt
```

You can edit/inspect the file directly from the host at any time — that's
the defining characteristic of a bind mount (as opposed to a named volume,
whose storage location is managed by Docker).

## Read-only bind mount variant

```bash
docker run --rm -v "$(pwd)/host-data:/data:ro" volume-demo:bind
```
