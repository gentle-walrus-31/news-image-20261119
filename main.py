#!/usr/bin/env python3
"""Entry program for the make.fun bounty ``news-image-20261119``.

"Sum up 19 November's world news in one image."

What this program does
----------------------
It takes the finished front page that ships in this repository
(``front-page.png``, a 1024x1024 newspaper-style infographic summarising
the world news of Thursday 19 November 2026) and writes it, byte for
byte, to ``/output/entry.png`` — the single image the bounty judges.

The program is deliberately deterministic and offline:

* it reads only files that are part of this repository;
* it performs no network access and no randomness;
* it uses no wall-clock time, no timestamps and no environment input;
* the output is an exact copy of the bundled image, so running it twice
  produces identical bytes (same SHA-256 every run).

Before writing, the program validates the bundled image so a corrupt or
wrong-sized asset can never be submitted silently:

* the file must exist and be a real PNG (8-byte PNG signature);
* the IHDR chunk must declare exactly 1024x1024 pixels;
* the file must be at most 1 MiB (the bounty limit);
* after writing, the output is read back and its SHA-256 is compared
  with the source; any mismatch aborts with a non-zero exit code.

Usage
-----
    python3 main.py            # writes /output/entry.png

Exit code 0 means the entry image was written and verified.
Anything else means validation failed and no valid output was left
behind (a partial output file is removed on failure).

Only the Python standard library is used.
"""

from __future__ import annotations

import hashlib
import os
import struct
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Entry constants
# ---------------------------------------------------------------------------

SOURCE_NAME = "front-page.png"
OUTPUT_DIR = Path("/output")
OUTPUT_NAME = "entry.png"

EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1 * 1024 * 1024  # 1 MiB, the bounty limit

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def fail(message: str) -> "SystemExit":
    """Print an error to stderr and exit non-zero."""
    print(f"error: {message}", file=sys.stderr)
    return SystemExit(1)


def read_source(repo_root: Path) -> bytes:
    """Read the bundled front-page image and return its raw bytes."""
    source_path = repo_root / SOURCE_NAME
    if not source_path.is_file():
        raise FileNotFoundError(
            f"bundled image {SOURCE_NAME!r} not found next to main.py"
        )
    return source_path.read_bytes()


def parse_png_dimensions(data: bytes) -> tuple[int, int]:
    """Return (width, height) from a PNG byte string.

    Parses the PNG signature and the IHDR chunk by hand so the program
    needs no third-party imaging library.
    """
    if len(data) < 33:
        raise ValueError("file too short to be a PNG image")
    if data[:8] != PNG_SIGNATURE:
        raise ValueError("not a PNG file: bad 8-byte signature")
    # IHDR is always the first chunk: 4-byte length, 4-byte type "IHDR",
    # then 13 bytes of data starting with width and height (big-endian).
    length, chunk_type = struct.unpack(">I4s", data[8:16])
    if chunk_type != b"IHDR" or length != 13:
        raise ValueError("not a PNG file: first chunk is not IHDR")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def validate_image(data: bytes) -> tuple[int, int]:
    """Check the bundled image against every bounty constraint.

    Returns the (width, height) on success; raises ValueError otherwise.
    """
    if len(data) > MAX_BYTES:
        raise ValueError(
            f"image is {len(data)} bytes, over the 1 MiB limit"
        )
    width, height = parse_png_dimensions(data)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(
            f"image is {width}x{height}, expected "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )
    return width, height


def sha256_hex(data: bytes) -> str:
    """SHA-256 hex digest of a byte string."""
    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------------------
# Main flow
# ---------------------------------------------------------------------------

def main() -> int:
    repo_root = Path(__file__).resolve().parent
    output_path = OUTPUT_DIR / OUTPUT_NAME

    try:
        data = read_source(repo_root)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        width, height = validate_image(data)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    source_digest = sha256_hex(data)

    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(data)
        written = output_path.read_bytes()
    except OSError as exc:
        print(f"error: cannot write {output_path}: {exc}", file=sys.stderr)
        return 1

    # Verify the round trip: what landed on disk must be byte-identical
    # to the validated source, otherwise remove it and fail loudly.
    if written != data or sha256_hex(written) != source_digest:
        try:
            output_path.unlink()
        except OSError:
            pass
        print("error: verification failed: output differs from source",
              file=sys.stderr)
        return 1

    print(f"validated: {SOURCE_NAME} is {width}x{height} PNG, "
          f"{len(data)} bytes (<= 1 MiB)")
    print(f"sha256: {source_digest}")
    print(f"wrote:  {output_path} ({len(written)} bytes, verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
