"""
S3-backed volume demo (via s3fs-fuse mounted inside the container).

Writes JSON records through the filesystem view at /data (which is
really the s3fs FUSE mount), then independently re-checks the same
bucket through the real boto3 S3 API — so you can see both views
agree, proving the FUSE mount is a faithful representation of what's
actually in the bucket.
"""

import os
import time
import datetime
import json

DATA_DIR = "/data"
BUCKET = os.environ.get("S3_BUCKET")


def verify_via_api():
    try:
        import boto3

        s3 = boto3.client("s3")
        resp = s3.list_objects_v2(Bucket=BUCKET)
        return sorted(obj["Key"] for obj in resp.get("Contents", []))
    except Exception as e:
        return [f"(could not verify via S3 API: {e})"]


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

        print(f"[filesystem view via s3fs] {len(fs_view)} object(s): {fs_view}")
        print(f"[direct S3 API view]      {len(api_view)} object(s): {api_view}")
        time.sleep(5)


if __name__ == "__main__":
    main()
