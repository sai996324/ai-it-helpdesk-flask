"""Builds a small labelled sample dataset (tickets.csv) for training.

This is only a starter dataset. Replace data/tickets.csv with real ticket data
(columns: text, category, priority) for better accuracy.
Run:  python data/make_dataset.py
"""
import csv
import random
from pathlib import Path

random.seed(42)

TEMPLATES = {
    "Network": [
        "wifi not connecting", "internet is very slow", "cannot connect to vpn",
        "network drops every few minutes", "lan cable not detected",
        "unable to reach shared drive", "no internet in conference room",
    ],
    "Hardware": [
        "laptop screen is flickering", "keyboard keys not working",
        "mouse not responding", "printer is not printing",
        "laptop battery drains quickly", "monitor shows no signal",
        "computer makes loud noise and shuts down",
    ],
    "Software": [
        "application keeps crashing", "cannot install software update",
        "excel file will not open", "browser shows error on startup",
        "need antivirus installed", "software license expired",
        "word freezes when saving document",
    ],
    "Account Access": [
        "forgot my password", "account is locked", "cannot login to email",
        "need access to shared folder", "password reset link not working",
        "two factor code not received", "new employee needs account created",
    ],
    "Server/Database": [
        "database connection timeout", "server is down", "website returns 500 error",
        "production server very slow", "backup job failed",
        "cannot connect to sql server", "application server out of disk space",
    ],
}

CRITICAL_WORDS = ["urgent", "production", "server is down", "all users", "everyone"]
HIGH_WORDS = ["cannot", "unable", "failed", "locked", "not working", "crash", "timeout", "500"]
LOW_WORDS = ["need", "request", "new", "install", "update"]

PREFIXES = ["", "", "", "Please help: ", "Hi team, ", "Issue: ", "Hello, "]
SUFFIXES = ["", "", " please fix", " since morning", " since yesterday", " in my department", " - need help"]


def priority_for(text: str) -> str:
    t = text.lower()
    if any(w in t for w in CRITICAL_WORDS):
        return "Critical"
    if any(w in t for w in HIGH_WORDS):
        return "High"
    if any(w in t for w in LOW_WORDS):
        return "Low"
    return "Medium"


def main():
    rows = set()
    for category, phrases in TEMPLATES.items():
        for phrase in phrases:
            for _ in range(8):
                text = random.choice(PREFIXES) + phrase + random.choice(SUFFIXES)
                if random.random() < 0.15:
                    text += " urgent"
                text = text.strip()
                rows.add((text, category, priority_for(text)))
    rows = list(rows)
    random.shuffle(rows)
    out = Path(__file__).parent / "tickets.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["text", "category", "priority"])
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows to {out}")


if __name__ == "__main__":
    main()
