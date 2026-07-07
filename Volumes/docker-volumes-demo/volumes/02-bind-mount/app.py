"""
Bind-mount demo.

Prints the ownership of /data as seen from inside the container (bind
mounts inherit whatever UID/GID owns the path on the HOST — unlike a
named volume, which Docker manages independently), then appends a log
line every 5 seconds directly onto the host filesystem.
"""

import os
import time
import datetime
import socket
import pwd
import grp

DATA_DIR = "/data"
LOG_FILE = os.path.join(DATA_DIR, "bind-mount-log.txt")


def describe_owner(path):
    st = os.stat(path)
    try:
        owner = pwd.getpwuid(st.st_uid).pw_name
    except KeyError:
        owner = str(st.st_uid)
    try:
        group = grp.getgrgid(st.st_gid).gr_name
    except KeyError:
        group = str(st.st_gid)
    return owner, group


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    owner, group = describe_owner(DATA_DIR)

    print(f"/data is owned by '{owner}:{group}' as seen from inside the container.")
    print("Because this is a BIND MOUNT (not a named volume), that ownership")
    print("comes straight from the host directory — edit ./host-data on the")
    print("host and you'll see changes reflected here immediately, and vice versa.")

    while True:
        line = f"{datetime.datetime.utcnow().isoformat()}Z - hello from {socket.gethostname()}\n"
        with open(LOG_FILE, "a") as f:
            f.write(line)
        print("Wrote:", line.strip())
        time.sleep(5)


if __name__ == "__main__":
    main()
