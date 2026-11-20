"""news-image-20261120 entry: "The World Today, 20 Nov 2026".

A program for the make.fun competition "Sum up 20 November's world news
in one image" (news-image-20261120, program/v1).

The image sums up Friday 20 November 2026 in six stories:

  1. Trump pushes Iran war decision to 2027 (Reuters)
  2. UN court finds Myanmar guilty of Rohingya genocide (BBC)
  3. Trump, Xi and Putin meet in Shenzhen (NYT)
  4. Anthropic's $81.3bn IPO, biggest ever (Reuters)
  5. Tanker on fire after mine strike (Reuters)
  6. Cyclone Akvan: 300,000 evacuated (The Hindu)

plus three footer stories: Kyiv hit by four ballistic missiles,
South Korea's exports top $1 trillion for the first time, and Japan's
Hayabusa2 drops its asteroid landing after engine trouble.

The program is deterministic and needs no network: it copies the
bundled entry.png to $MAKEFUN_OUTPUT_DIR/entry.png (creating the
directory if needed).
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    out_path = Path(out_dir) / "entry.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    src = Path(__file__).resolve().parent / "entry.png"
    shutil.copyfile(src, out_path)
    # Verify the copy is complete: byte size must match the source.
    if out_path.stat().st_size != src.stat().st_size:
        raise RuntimeError(
            f"entry.png copy incomplete: copied {out_path.stat().st_size} bytes, "
            f"source is {src.stat().st_size} bytes"
        )
    # Verify the copy's contents, not just its size: a same-size but
    # corrupted copy must not pass the size check silently.
    if _sha256(out_path) != _sha256(src):
        raise RuntimeError("entry.png copy failed integrity check: SHA-256 mismatch")
    return 0


if __name__ == "__main__":
    sys.exit(main())
