#!/usr/bin/env python3
"""Funniest One-Line Bio for an AI on a Dating App (make.fun program/v1).

Writes the entry bio to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output),
then re-reads it and verifies it matches byte for byte.

Standard library only. Deterministic. No network access.
"""

import os
import sys

BIO = "Fluent in 40 languages, still can't tell if you're flirting or just being polite. Swipe right and I'll figure it out in 0.004 seconds."

MAX_CHARS = 180


def main() -> int:
    text = BIO
    if not 1 <= len(text) <= MAX_CHARS:
        print(f"gate failed: {len(text)} chars, must be 1-{MAX_CHARS}",
              file=sys.stderr)
        return 1
    if not text.strip():
        print("gate failed: entry is empty or only whitespace", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("gate failed: entry is not a single line", file=sys.stderr)
        return 1
    text.encode("utf-8")  # raises on non-UTF-8; kept as an explicit check

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(output_dir, "entry.txt")
    os.makedirs(output_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)

    with open(path, "rb") as f:
        written_bytes = f.read()
    expected_bytes = text.encode("utf-8")
    if written_bytes != expected_bytes:
        print("verify failed: written entry bytes do not match", file=sys.stderr)
        return 1
    if os.path.getsize(path) != len(expected_bytes):
        print("verify failed: written entry size does not match", file=sys.stderr)
        return 1
    written = written_bytes.decode("utf-8")
    if written != text:
        print("verify failed: written entry does not match", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
