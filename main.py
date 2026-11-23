#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261123 submission.

What it does, in one sentence: take the front page that
``build_image.py`` already painted (``image.png`` in this same folder)
and place an exact copy of it at ``$MAKEFUN_OUTPUT_DIR/entry.png``.

Nothing here touches the network, the clock, or any random source, so
running it twice gives byte-identical output.  The default output
folder is ``/output`` when ``MAKEFUN_OUTPUT_DIR`` is not set, which
matches the competition's runner.
"""

import os
import shutil
from pathlib import Path

SOURCE_NAME = "image.png"
TARGET_NAME = "entry.png"
FALLBACK_DIR = "/output"


def where_to_write() -> Path:
    """Resolve the output folder from the environment, or the default."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or FALLBACK_DIR
    return Path(chosen).expanduser()


def locate_source() -> Path:
    """The picture lives next to this file, wherever the repo is checked out."""
    return Path(__file__).resolve().parent / SOURCE_NAME


def run() -> Path:
    """Copy the picture into place and hand back the path that was written."""
    origin = locate_source()
    destination_dir = where_to_write()
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / TARGET_NAME
    shutil.copyfile(origin, destination)
    return destination


if __name__ == "__main__":
    written = run()
    print(f"entry written to {written}")
