"""
EBS-backed volume demo (via the rexray/ebs Docker volume plugin).

Since EBS is BLOCK storage (not object storage like S3), this demo
leans into that: it writes 1 MB chunks to a growing file and calls
fsync() to force each write down to the actual block device, then
reports real disk usage stats for /data via shutil.disk_usage —
something that doesn't make sense for S3/GCS-style object mounts.
"""

import os
import time
import datetime
import shutil

DATA_DIR = "/data"
BIG_FILE = os.path.join(DATA_DIR, "block-test.bin")
CHUNK = b"0" * (1024 * 1024)  # 1 MB


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    while True:
        with open(BIG_FILE, "ab") as f:
            f.write(CHUNK)
            f.flush()
            os.fsync(f.fileno())

        usage = shutil.disk_usage(DATA_DIR)
        print(
            f"{datetime.datetime.utcnow().isoformat()}Z wrote 1MB chunk "
            f"(fsync'd to the EBS-backed block device). "
            f"Disk usage: total={usage.total // (1024 ** 2)}MB "
            f"used={usage.used // (1024 ** 2)}MB "
            f"free={usage.free // (1024 ** 2)}MB"
        )
        time.sleep(5)


if __name__ == "__main__":
    main()
