# Arctic Fox + Penguin — cutest-picture-01 entry.
# A baby arctic fox hugs a baby penguin. The picture lives in this
# repository as entry.png (a JPEG file, told apart by its first bytes);
# this program, Python 3.13 standard library only, streams it to
# /output/entry.png byte for byte, then proves the copy is exact.
#
# Local run (outside the grader's container /output is replaced by
# the MAKEFUN_OUTPUT_DIR environment variable):
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import hashlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
DEST_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
DEST = DEST_DIR / "entry.png"
MAX_BYTES = 1_048_576
JPEG_MAGIC = b"\xff\xd8\xff"

def stream_copy(src, dst):
    digest = hashlib.sha256()
    total = 0
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        while True:
            chunk = fin.read(65536)
            if not chunk:
                break
            digest.update(chunk)
            fout.write(chunk)
            total += len(chunk)
    return digest.hexdigest(), total

def main():
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    raw = SOURCE.read_bytes()
    if not raw.startswith(JPEG_MAGIC):
        print("entry.png is not a JPEG", file=sys.stderr)
        return 1
    if len(raw) > MAX_BYTES:
        print("entry.png exceeds the 1 MiB size cap", file=sys.stderr)
        return 1
    copied_hash, copied_bytes = stream_copy(SOURCE, DEST)
    if not DEST.is_file() or copied_bytes != len(raw):
        print("entry.png copy is incomplete", file=sys.stderr)
        return 1
    if copied_hash != hashlib.sha256(raw).hexdigest():
        print("entry.png copy failed its integrity check", file=sys.stderr)
        return 1
    print(f"wrote {DEST} ({copied_bytes} bytes, sha256 {copied_hash[:12]}...)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
