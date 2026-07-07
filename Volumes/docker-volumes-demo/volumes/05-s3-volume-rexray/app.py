"""
S3-backed volume demo (via the rexray/s3fs Docker volume plugin).

Writes a new JSON "record" object into /data every 5 seconds and lists
the directory contents — because the plugin presents the S3 bucket as
a normal filesystem, this looks exactly like any other file I/O, but
every object is really landing in S3 behind the scenes.
"""

import os
import time
import datetime
import json

DATA_DIR = "/data"


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    i = 0
    while True:
        i += 1
        key = f"record-{i:04d}.json"
        path = os.path.join(DATA_DIR, key)
        payload = {
            "id": i,
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "message": "written via a Docker volume plugin backed by S3",
        }
        with open(path, "w") as f:
            json.dump(payload, f, indent=2)

        objects = sorted(os.listdir(DATA_DIR))
        print(f"Wrote {key}. Bucket now has {len(objects)} object(s): {objects}")
        time.sleep(5)


if __name__ == "__main__":
    main()
