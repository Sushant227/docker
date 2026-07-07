"""
Azure Files (SMB share) demo.

Same shared-access pattern as the NFS example: run this from multiple
containers with different CLIENT_ID values (see run-multi.sh) and
watch them all append to, and see, the same shared file over SMB.
"""

import os
import time
import datetime
import socket

DATA_DIR = "/data"
SHARED_FILE = os.path.join(DATA_DIR, "shared-log.txt")
CLIENT_ID = os.environ.get("CLIENT_ID", socket.gethostname())


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Client '{CLIENT_ID}' connected to Azure Files SMB share at /data")

    while True:
        line = f"{datetime.datetime.utcnow().isoformat()}Z [{CLIENT_ID}] checked in\n"
        with open(SHARED_FILE, "a") as f:
            f.write(line)

        with open(SHARED_FILE) as f:
            total_lines = sum(1 for _ in f)

        print(f"[{CLIENT_ID}] shared SMB file now has {total_lines} total lines (across ALL clients)")
        time.sleep(5)


if __name__ == "__main__":
    main()
