#!/usr/bin/env python3
"""news-image-20261119: write the 19 November 2026 news image.

The artwork is bundled with this repository at assets/entry.png — a
1024x1024 front page drawn at build time by tools/make_image.py from the
stories first reported on Thursday 19 November 2026. All this program
does is check that artwork and copy it, byte for byte, to the output
file. No network, no clock, no randomness: two runs write identical
bytes.

Output location, first match wins: $MAKEFUN_OUTPUT_DIR, then
$ENTRY_OUTPUT_DIR, then /output.
"""

import hashlib
import os
import struct
import sys
import zlib

BASE = os.path.dirname(os.path.realpath(__file__))
ARTWORK = os.path.join(BASE, "assets", "entry.png")
MAX_BYTES = 1024 * 1024
EXPECTED_SIZE = (1024, 1024)
MAGIC = b"\x89PNG\r\n\x1a\n"


class ArtworkError(Exception):
    """The bundled artwork is missing or fails a structural check."""


def be32(chunk, at):
    """One big-endian unsigned 32-bit word out of a byte string."""
    return struct.unpack_from(">I", chunk, at)[0]


def walk_chunks(png):
    """Walk a PNG's chunks, checking every CRC as we go.

    Yields (type, payload) pairs. Raises ArtworkError on any defect.
    """
    if png[:8] != MAGIC:
        raise ArtworkError("bundled file is not a PNG")
    cursor = 8
    while cursor < len(png):
        if cursor + 8 > len(png):
            raise ArtworkError("chunk header cut short at offset %d" % cursor)
        length = be32(png, cursor)
        kind = png[cursor + 4:cursor + 8]
        stop = cursor + 8 + length + 4
        if stop > len(png):
            raise ArtworkError("chunk %r runs past the end of the file"
                               % kind.decode("latin1"))
        payload = png[cursor + 8:cursor + 8 + length]
        stored_crc = be32(png, cursor + 8 + length)
        if zlib.crc32(kind + payload) & 0xFFFFFFFF != stored_crc:
            raise ArtworkError("CRC mismatch in %s chunk"
                               % kind.decode("latin1"))
        yield kind, payload
        cursor = stop


def inspect(png):
    """Validate the bundled PNG; return its (width, height)."""
    if len(png) > MAX_BYTES:
        raise ArtworkError("bundled image is %d bytes, over the 1 MiB cap"
                           % len(png))
    dims = None
    pixels = bytearray()
    closed = False
    for kind, payload in walk_chunks(png):
        if kind == b"IHDR":
            if len(payload) != 13:
                raise ArtworkError("IHDR is %d bytes, expected 13"
                                   % len(payload))
            dims = (be32(payload, 0), be32(payload, 4))
            if dims != EXPECTED_SIZE:
                raise ArtworkError("image is %dx%d, expected 1024x1024"
                                   % dims)
        elif kind == b"IDAT":
            pixels.extend(payload)
        elif kind == b"IEND":
            closed = True
    if dims is None:
        raise ArtworkError("no IHDR chunk found")
    if not closed:
        raise ArtworkError("no IEND chunk found")
    # Inflating the pixel stream proves the IDAT data is intact.
    plain = zlib.decompress(bytes(pixels))
    wanted = EXPECTED_SIZE[1] * (1 + EXPECTED_SIZE[0] * 3)
    if len(plain) != wanted:
        raise ArtworkError("pixel data inflates to %d bytes, expected %d"
                           % (len(plain), wanted))
    return dims


def pick_output_dir():
    for name in ("MAKEFUN_OUTPUT_DIR", "ENTRY_OUTPUT_DIR"):
        value = os.environ.get(name)
        if value:
            return value
    return "/output"


def run():
    if not os.path.isfile(ARTWORK):
        print("error: bundled artwork is missing: %s" % ARTWORK,
              file=sys.stderr)
        print("the repository must contain assets/entry.png", file=sys.stderr)
        return 1
    with open(ARTWORK, "rb") as handle:
        png = handle.read()
    width, height = inspect(png)
    fingerprint = hashlib.sha256(png).hexdigest()
    folder = pick_output_dir()
    os.makedirs(folder, exist_ok=True)
    target = os.path.join(folder, "entry.png")
    with open(target, "wb") as handle:
        handle.write(png)
    with open(target, "rb") as handle:
        again = handle.read()
    if hashlib.sha256(again).hexdigest() != fingerprint:
        raise ArtworkError("the written file differs from the bundled image")
    print("wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (target, width, height, len(png), fingerprint))
    return 0


if __name__ == "__main__":
    sys.exit(run())
