"""
GCS-backed volume demo (via gcsfuse mounted inside the container).

Mirrors the S3/s3fs-fuse demo: writes JSON records through the
filesystem view at /data (really the gcsfuse mount), then
independently re-checks the same bucket through the real
google-cloud-storage API to confirm both views agree.
"""

import os
import time
import datetime
import json

DATA_DIR = "/data"
BUCKET = os.environ.get("GCS_BUCKET")


def verify_via_api():
    try:
        from google.cloud import storage

        client = storage.Client()
        blobs = client.list_blobs(BUCKET)
        return sorted(b.name for b in blobs)
    except Exception as e:
        return [f"(could not verify via GCS API: {e})"]


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    i = 0
    while True:
        i += 1
        key = f"record-{i:04d}.json"
        path = os.path.join(DATA_DIR, key)
        payload = {"id": i, "created_at": datetime.datetime.utcnow().isoformat() + "Z"}
        with open(path, "w") as f:
            json.dump(payload, f)

        fs_view = sorted(os.listdir(DATA_DIR))
        api_view = verify_via_api()

        print(f"[filesystem view via gcsfuse] {len(fs_view)} object(s): {fs_view}")
        print(f"[direct GCS API view]        {len(api_view)} object(s): {api_view}")
        time.sleep(5)


if __name__ == "__main__":
    main()
