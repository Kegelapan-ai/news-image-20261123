#!/usr/bin/env python3
"""Entry point for the 23 November 2026 news-image entry.

The picture itself is drawn ahead of time by build_image.py and stored
next to this file as image.png. All this program does is place a copy of
it where the grader looks for it. It needs no network, no extra packages
and no clock, so two runs always produce the same file.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "image.png")
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(source, target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
