#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261125 broadsheet entry.

Copies the pre-rendered entry.png from this repository into the output
directory the grader provides. Standard library only, no network, no
rendering at run time: the image is byte-identical on every run.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing next to main.py")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
