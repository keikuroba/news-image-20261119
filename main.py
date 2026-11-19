#!/usr/bin/env python3
"""news-image-20261119: emit the 19 November 2026 news image.

The finished artwork ships inside this repository as assets/entry.png
(it was drawn at build time by tools/make_image.py from the stories
reported on Thursday 19 November 2026). This program only copies it,
byte for byte, to the grader's output file. It touches no network, reads
no clock and rolls no dice, so two runs write identical bytes.

Where the file goes: $MAKEFUN_OUTPUT_DIR first, then
$ENTRY_OUTPUT_DIR, then /output.
"""

import hashlib
import os
import sys
import zlib

HERE = os.path.dirname(os.path.realpath(__file__))
BUNDLED = os.path.join(HERE, "assets", "entry.png")
ONE_MIB = 1024 * 1024
SIGNATURE = b"\x89PNG\r\n\x1a\n"


class BadImage(Exception):
    """The bundled artwork failed a structural check."""


def _u32be(buf, off):
    return int.from_bytes(buf[off:off + 4], "big")


def _chunks(blob):
    """Yield (kind, data) for every chunk of a PNG byte string."""
    if blob[:8] != SIGNATURE:
        raise BadImage("not a PNG (bad signature)")
    pos = 8
    while pos < len(blob):
        if pos + 8 > len(blob):
            raise BadImage("truncated chunk header")
        size = _u32be(blob, pos)
        kind = blob[pos + 4:pos + 8]
        end = pos + 8 + size + 4
        if end > len(blob):
            raise BadImage("truncated %s chunk" % kind.decode("latin1"))
        data = blob[pos + 8:pos + 8 + size]
        want = zlib.crc32(kind + data) & 0xFFFFFFFF
        if _u32be(blob, pos + 8 + size) != want:
            raise BadImage("CRC mismatch in %s chunk" % kind.decode("latin1"))
        pos = end
        yield kind, data


def validate(blob):
    """Full structural validation of the bundled PNG bytes."""
    if len(blob) > ONE_MIB:
        raise BadImage("bundled image over 1 MiB: %d bytes" % len(blob))
    width = height = None
    idat = bytearray()
    seen_iend = False
    for kind, data in _chunks(blob):
        if kind == b"IHDR":
            if len(data) != 13:
                raise BadImage("bad IHDR length")
            width = _u32be(data, 0)
            height = _u32be(data, 4)
            if (width, height) != (1024, 1024):
                raise BadImage("expected 1024x1024, got %dx%d"
                               % (width, height))
        elif kind == b"IDAT":
            idat.extend(data)
        elif kind == b"IEND":
            seen_iend = True
    if width is None:
        raise BadImage("no IHDR chunk")
    if not seen_iend:
        raise BadImage("no IEND chunk")
    # The pixel data must inflate: a corrupt IDAT stream fails here.
    raw = zlib.decompress(bytes(idat))
    expect = height * (1 + width * 3)
    if len(raw) != expect:
        raise BadImage("inflated pixel data %d bytes, expected %d"
                       % (len(raw), expect))
    return width, height


def out_dir():
    for var in ("MAKEFUN_OUTPUT_DIR", "ENTRY_OUTPUT_DIR"):
        val = os.environ.get(var)
        if val:
            return val
    return "/output"


def main():
    with open(BUNDLED, "rb") as fh:
        blob = fh.read()
    width, height = validate(blob)
    dest_dir = out_dir()
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "entry.png")
    with open(dest, "wb") as fh:
        fh.write(blob)
    digest = hashlib.sha256(blob).hexdigest()
    print("wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (dest, width, height, len(blob), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
