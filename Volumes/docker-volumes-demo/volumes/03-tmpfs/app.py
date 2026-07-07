"""
tmpfs demo.

Confirms /data is actually backed by tmpfs (by reading /proc/mounts),
then checks whether any data survived from a previous run. Since
tmpfs storage lives only in the container's memory, restarting the
container should always show an EMPTY file — that's the point.
"""

import os
import time
import datetime

DATA_DIR = "/data"
DATA_FILE = os.path.join(DATA_DIR, "session.txt")


def is_tmpfs(path):
    with open("/proc/mounts") as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 3 and parts[1] == path:
                return parts[2] == "tmpfs"
    return False


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Is {DATA_DIR} backed by tmpfs? {is_tmpfs(DATA_DIR)}")

    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        print("Found existing data in /data (only expected within the SAME")
        print("container lifetime — never across a restart):")
        with open(DATA_FILE) as f:
            print(f.read())
    else:
        print("No pre-existing data found. Expected on first boot, and expected")
        print("again after any restart, since tmpfs storage is destroyed the")
        print("moment the container stops.")

    count = 0
    while True:
        count += 1
        with open(DATA_FILE, "a") as f:
            f.write(f"{datetime.datetime.utcnow().isoformat()}Z tick {count}\n")
        print(f"tick {count} written to in-memory /data (RAM only, never touches disk)")
        time.sleep(5)


if __name__ == "__main__":
    main()
