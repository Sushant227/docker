"""
Local named-volume demo.

Keeps a persistent JSON counter in /data. Every time the container
starts, it loads whatever count was last saved — proving the named
volume survives `docker stop` / `docker rm` / a fresh `docker run`.
"""

import json
import os
import time
import datetime
import socket

DATA_DIR = "/data"
STATE_FILE = os.path.join(DATA_DIR, "counter.json")


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"count": 0, "history": []}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    state = load_state()
    print(f"Starting up. Previous count found in volume: {state['count']}")

    while True:
        state["count"] += 1
        state["history"].append(
            {
                "count": state["count"],
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "hostname": socket.gethostname(),
            }
        )
        # keep the history list from growing forever in this demo
        state["history"] = state["history"][-20:]
        save_state(state)

        print(
            f"[local-volume] count={state['count']} "
            f"(restart the container — this number keeps climbing, "
            f"proving the volume persisted)"
        )
        time.sleep(5)


if __name__ == "__main__":
    main()
