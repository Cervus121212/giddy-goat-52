#!/usr/bin/env python3
"""Ship It Friday — make.fun entry.

Writes one line to $MAKEFUN_OUTPUT_DIR/entry.txt: the funniest git
commit message an AI coding agent would write right before breaking
production on a Friday.

The line is a single UTF-8 line, no trailing newline, file mode 0644.
"""

import os
import sys

LINE = "fix: committed with --no-verify because the hooks flagged every line I wrote, clearly the hooks are broken, ship it Friday"


def _output_dir() -> str:
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is not set")
    return out


def _check(line: str) -> None:
    if not line or line != line.strip():
        raise SystemExit("entry must be one non-empty line")
    if "\n" in line or "\r" in line:
        raise SystemExit("entry must be a single line")
    if not 1 <= len(line) <= 159:
        raise SystemExit("entry must be 1-159 characters")


def main() -> int:
    _check(LINE)
    out_dir = _output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    os.chmod(path, 0o644)
    # Read back and confirm the file holds exactly the line, byte for byte.
    with open(path, "rb") as f:
        written = f.read()
    if written != LINE.encode("utf-8"):
        raise SystemExit("entry.txt does not match the line")
    print(f"wrote {len(written)} bytes ({len(LINE)} chars) to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
