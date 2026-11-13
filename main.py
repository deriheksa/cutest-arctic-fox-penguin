# Arctic Fox + Penguin — cutest-picture-01 entry (Python 3.13, standard library only).
# The picture is the entry.png beside this file; the program copies it to
# /output/entry.png. The file is a JPEG (told apart by its first bytes);
# the name stays entry.png either way, per the competition rules.
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import hashlib
import os
import shutil
from pathlib import Path

src = Path(__file__).resolve().parent / "entry.png"
out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"
out.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(src, out)

# Verify the copy is byte-identical: a truncated or corrupted output
# must fail loudly here instead of shipping a broken image to the judge.
def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()

if _sha256(src) != _sha256(out):
    raise SystemExit("entry.png copy failed integrity check")
