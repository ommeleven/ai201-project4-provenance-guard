import json
import os

LOG_FILE = "audit_log.json"


def load_log():
    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []


def save_log(entries):
    with open(LOG_FILE, "w") as f:
        json.dump(entries, f, indent=4)


def add_entry(entry):
    entries = load_log()
    entries.append(entry)
    save_log(entries)