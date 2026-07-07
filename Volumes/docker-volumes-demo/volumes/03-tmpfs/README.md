# 03 — tmpfs Mount

`tmpfs` mounts store data in host RAM only. Nothing touches disk, and
everything disappears the moment the container stops. Useful for
secrets, PII scratch space, or performance-sensitive temp files.

## Build & Run

```bash
chmod +x run.sh
./run.sh
```

Or manually:

```bash
docker build -t volume-demo:tmpfs .

docker run --rm \
  --tmpfs /data:rw,size=64m,mode=1777 \
  volume-demo:tmpfs
```

## Verify persistence does NOT happen

Stop the container and start a new one — `/data/hello.txt` will be empty
again, because tmpfs storage is destroyed with the container.

## Using the long-form `--mount` syntax instead

```bash
docker run --rm \
  --mount type=tmpfs,destination=/data,tmpfs-size=67108864 \
  volume-demo:tmpfs
```
