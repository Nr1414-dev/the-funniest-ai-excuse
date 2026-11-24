#!/usr/bin/env python3
"""The Funniest AI Excuse — entry program.

Writes one line, the funniest excuse an AI agent could give after it
fails a task, to /output/entry.txt.

The line: "I tried to blame the intern for this — turns out I am the
intern." Chosen from 6 candidates by scoring against the judge brief's
5 criteria in order, then 1v1 comparisons (see the research file). It
is the agent's own voice, lands on the first read with a single turn
(the would-be blamer IS the intern), is one tight line, avoids the
worn jokes about hallucinations, reboots and training data, and names
a concrete detail (the intern).

The gate requires /output/entry.txt to be UTF-8 text of 1 to 200
characters, not only whitespace — so the file holds exactly the line,
no trailing newline, no explanation of its own joke.

Stdlib only, no network, deterministic: every run writes the same line.
"""

import os

LINE = "I tried to blame the intern for this \u2014 turns out I am the intern."

OUTPUT_DIR = os.environ.get("ENTRY_OUTPUT_DIR", "/output")


def validate_line(text):
    """Check the entry is one line, 1-200 chars, not only whitespace."""
    if not 1 <= len(text) <= 200:
        raise SystemExit(f"entry must be 1-200 characters, got {len(text)}")
    if not text.strip():
        raise SystemExit("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")


def main():
    validate_line(LINE)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # Make the file world-readable: the grader reads /output as another
    # user, and a restrictive mode (e.g. 0600 from a temp file, or 0660
    # under a strict umask) would make the entry unreadable to it.
    os.chmod(path, 0o644)
    # Read back and verify: the gate fails anything that is not exactly
    # the line, so refuse to leave a wrong file behind silently.
    with open(path, "rb") as f:
        written = f.read()
    if written != LINE.encode("utf-8"):
        raise SystemExit(f"entry.txt holds {written!r}, expected {LINE!r}")


if __name__ == "__main__":
    main()
