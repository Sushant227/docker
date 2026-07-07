"""
NFS shared-volume demo.

Designed to be run from MULTIPLE containers at once (see run-multi.sh),
each with its own CLIENT_ID. All instances append to the same shared
file on the NFS export and print the total line count, demonstrating
that an NFS-backed Docker volume is visible/writable from many clients
simultaneously — unlike a local named volume or bind mount.
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
    print(f"Client '{CLIENT_ID}' connected to shared NFS-backed /data")

    while True:
        line = f"{datetime.datetime.utcnow().isoformat()}Z [{CLIENT_ID}] wrote a line\n"
        with open(SHARED_FILE, "a") as f:
            f.write(line)

        with open(SHARED_FILE) as f:
            total_lines = sum(1 for _ in f)

        print(f"[{CLIENT_ID}] shared file now has {total_lines} total lines (across ALL clients)")
        time.sleep(5)


if __name__ == "__main__":
    main()
