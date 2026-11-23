#!/usr/bin/env python3
"""Entry program for the make.fun news-image-20261123 bounty.

Copies the pre-rendered entry.png (sitting next to this script) into the
grader output directory. Stdlib only, no network, deterministic: the output
bytes are an exact copy of the bundled image every run.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
