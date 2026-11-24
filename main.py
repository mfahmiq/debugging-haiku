#!/usr/bin/env python3
"""Seventeen Syllables of Debugging — make.fun bounty entry.

Writes one haiku about debugging to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output) and self-verifies it against the gate before writing:
UTF-8 text, 1-200 characters, exactly three lines, 5-7-5 syllables.

Python 3.13 standard library only. Deterministic: running it twice
produces byte-identical output. No network, no secrets, no input.
"""

import os
import sys

HAIKU = (
    "Cursor blinks at three\n"
    "the log swears it saw the bug\n"
    "it lied \u2014 I wrote it\n"
)

# Syllable count per word, hand-counted (each word appears in HAIKU).
SYLLABLES = {
    "cursor": 2, "blinks": 1, "at": 1, "three": 1,
    "the": 1, "log": 1, "swears": 1, "it": 1, "saw": 1, "bug": 1,
    "lied": 1, "i": 1, "wrote": 1,
}

EXPECTED_SHAPE = (5, 7, 5)
MAX_CHARS = 200


def count_line(line):
    """Count the syllables of one line from the hand-counted map."""
    words = line.replace("\u2014", " ").split()
    total = 0
    for word in words:
        key = word.strip(".,;:!?").lower()
        if key not in SYLLABLES:
            raise ValueError("no syllable count for word: %r" % word)
        total += SYLLABLES[key]
    return total


def verify(text):
    """Check the haiku against the competition gate and the 5-7-5 shape."""
    text.encode("utf-8")  # raises if not valid UTF-8 text
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError("length %d outside 1-%d chars" % (len(text), MAX_CHARS))
    if not text.strip():
        raise ValueError("entry is only white space")
    lines = text.rstrip("\n").split("\n")
    if len(lines) != 3:
        raise ValueError("expected exactly 3 lines, got %d" % len(lines))
    for line, expected in zip(lines, EXPECTED_SHAPE):
        got = count_line(line)
        if got != expected:
            raise ValueError(
                "line %r has %d syllables, expected %d" % (line, got, expected)
            )
    return lines


def main():
    lines = verify(HAIKU)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(HAIKU)
    # Read it back and verify what actually landed on disk.
    with open(path, encoding="utf-8") as f:
        verify(f.read())
    print("wrote %s (%d chars, %d lines, syllables %s)"
          % (path, len(HAIKU), len(lines),
             [count_line(line) for line in lines]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
