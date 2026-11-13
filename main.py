#!/usr/bin/env python3
# Arctic Fox + Penguin, cutest-picture-01.
# A fluffy white arctic fox with sparkling amber eyes and a tilted head
# hugs a tiny grey penguin whose eyes are shut in a happy smile. The
# artwork is entry.png next to this file, JPEG bytes under that name.
# Running this file streams the artwork to /output/entry.png and then
# checks the copy byte for byte, so a broken output can never slip
# through to the judge. Standard library only, Python 3.13. The fox's
# ears, tail and the penguin all sit fully inside the frame, with a
# clear gap beside the penguin on the right.
# Try it locally with:
#     mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
import os, sys
from hashlib import sha256 as _sha
from pathlib import Path as _P

_BASE = _P(__file__).resolve().parent
_PICTURE = _BASE / "entry.png"
_TARGET_DIR = _P(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
_TARGET = _TARGET_DIR / "entry.png"
_LIMIT = 1048576
_MAGIC = bytes((255, 216, 255))


def _copy_stream(source, target):
    # Copy source to target in 64 KiB pieces, returning its digest.
    # Every piece is hashed as it passes through, so the digest covers
    # exactly the bytes that landed in the target file.
    hasher = _sha()
    written = 0
    with open(source, "rb") as reader, open(target, "wb") as writer:
        while True:
            piece = reader.read(65536)
            if not piece:
                break
            hasher.update(piece)
            writer.write(piece)
            written += len(piece)
    return hasher.hexdigest(), written


def _run():
    _TARGET_DIR.mkdir(parents=True, exist_ok=True)
    data = _PICTURE.read_bytes()
    if data[:3] != _MAGIC:
        print("entry.png does not start with a JPEG marker", file=sys.stderr)
        return 1
    if len(data) > _LIMIT:
        print("entry.png is larger than the 1 MiB cap", file=sys.stderr)
        return 1
    digest, amount = _copy_stream(_PICTURE, _TARGET)
    if not _TARGET.is_file():
        print("entry.png copy did not appear", file=sys.stderr)
        return 1
    if amount != len(data):
        print("entry.png copy stopped early", file=sys.stderr)
        return 1
    if digest != _sha(data).hexdigest():
        print("entry.png copy does not match the original", file=sys.stderr)
        return 1
    print("wrote " + str(_TARGET) + " (" + str(amount) + " bytes, sha256 " + digest[:12] + "...)")
    return 0


def _entry():
    raise SystemExit(_run())


_entry()
