#!/usr/bin/env python3
"""Entry point for news-image-20261120.

Copies the pre-rendered front page (news.png, drawn by render.py) to
/output/entry.png. Standard library only, no network, deterministic:
the same bytes go out on every run.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "news.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
