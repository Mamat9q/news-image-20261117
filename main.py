"""news-image-20261117 entry: deterministically copy the chosen image
to the output directory.

The image (entry.png) is the entry: a one-page newspaper front page,
"THE WORLD IN ONE DAY", summing up Tuesday 17 November 2026 in 37
stories across 6 continents - three lead stories (US strikes on Iran,
the Kerch Bridge hit again, the Xi-Trump-Putin summit set for
Shenzhen) plus briefs by region and a markets ticker. It was drawn in
this session by draw_poster.py (Pillow, local build tool) and is
bundled here as a true PNG, 1024x1024, 178004 bytes.

This program is standard library only: it verifies the bundled image
(sha256, size, PNG dimensions) and copies it to
$MAKEFUN_OUTPUT_DIR/entry.png. Both runs write the same bytes.
"""

import hashlib
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED_SHA256 = (
    "7a2a96373c4e30576d04281e8822b0a431b878355a5ef5f65aae2a4daba2ef0e"
)
EXPECTED_SIZE = 178004
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _png_dimensions(path):
    """Read width/height from a PNG's IHDR chunk (stdlib only)."""
    with open(path, "rb") as f:
        header = f.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path!r} is not a PNG (bad signature)")
    if header[12:16] != b"IHDR":
        raise ValueError(f"{path!r} has no IHDR chunk first")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def _png_is_whole(path):
    """A whole PNG ends with the 12-byte IEND chunk; reject a truncated file."""
    with open(path, "rb") as f:
        f.seek(-12, os.SEEK_END)
        tail = f.read(12)
    return tail == b"\x00\x00\x00\x00IEND\xaeB`\x82"


def main():
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        raise FileNotFoundError(
            f"entry.png is missing next to main.py: {src!r}"
        )

    src_sha = _sha256(src)
    if src_sha != EXPECTED_SHA256:
        raise RuntimeError(
            f"source image sha256 mismatch: {src_sha}, "
            f"expected {EXPECTED_SHA256}"
        )
    if os.path.getsize(src) != EXPECTED_SIZE:
        raise RuntimeError(
            f"source image size mismatch: {os.path.getsize(src)} bytes, "
            f"expected {EXPECTED_SIZE}"
        )
    width, height = _png_dimensions(src)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise RuntimeError(
            f"source image dimensions {width}x{height}, "
            f"expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )
    if not _png_is_whole(src):
        raise RuntimeError(f"source image is not a whole PNG: {src!r}")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not os.path.isabs(out_dir):
        out_dir = os.path.join(os.getcwd(), out_dir)
    os.makedirs(out_dir, exist_ok=True)

    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)

    if os.path.getsize(dst) != os.path.getsize(src):
        raise RuntimeError(f"copy incomplete: {dst!r}")
    if _sha256(dst) != src_sha:
        raise RuntimeError(f"integrity check failed: {dst!r}")
    if not _png_is_whole(dst):
        raise RuntimeError(f"copied output is not a whole PNG: {dst!r}")

    print(f"wrote {dst} ({EXPECTED_SIZE} bytes, {width}x{height}, sha256 {src_sha})")


if __name__ == "__main__":
    main()
