# Python Docker Demo

A minimal Flask app packaged with **two Docker build strategies**:

- `Dockerfile.single` — a single-stage build (simpler, larger image)
- `Dockerfile.multi` — a multi-stage build (slightly more complex, smaller/cleaner final image)

Both produce a container that runs the same Flask app via `gunicorn` on port `5000`.

## Project structure

```
python-docker-project/
├── app.py               # Flask application
├── requirements.txt     # Python dependencies
├── Dockerfile.single    # Single-stage Dockerfile
├── Dockerfile.multi     # Multi-stage Dockerfile
└── README.md
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running

## Building the images

Run these commands from inside the `python-docker-project/` directory.

### 1. Build the single-stage image

```bash
docker build -f Dockerfile.single -t python-demo:single .
```

### 2. Build the multi-stage image

```bash
docker build -f Dockerfile.multi -t python-demo:multi .
```

> Note: since there are two Dockerfiles in the same folder, you must pass `-f` to tell Docker which one to use. If you only kept one Dockerfile (named exactly `Dockerfile`), you could drop the `-f` flag.

## Running a container

Either image runs the same way:

```bash
# Single-stage image
docker run --rm -p 5000:5000 python-demo:single

# Multi-stage image
docker run --rm -p 5000:5000 python-demo:multi
```

Then visit:

- http://localhost:5000/ — returns a JSON greeting + Python version + timestamp
- http://localhost:5000/health — returns `{"status": "ok"}`

Or test with curl:

```bash
curl http://localhost:5000/
curl http://localhost:5000/health
```

## Comparing image sizes

After building both, compare them:

```bash
docker images python-demo
```

You should see the `multi` tag produce a noticeably smaller image, since the multi-stage build discards the `gcc` compiler and build cache used only to install dependencies, keeping just the final virtual environment and app code in the runtime image.

## Cleaning up

```bash
docker rmi python-demo:single python-demo:multi
```

## Why two approaches?

| | Single-stage | Multi-stage |
|---|---|---|
| Simplicity | Easier to read/write | Slightly more moving parts |
| Image size | Larger (keeps build tools) | Smaller (final stage is clean) |
| Security surface | More packages present at runtime | Fewer packages present at runtime |
| Best for | Quick prototypes, simple apps | Production images, CI/CD pipelines |
