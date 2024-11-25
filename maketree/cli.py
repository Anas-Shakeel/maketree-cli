""" Frontend of the project (Argument handling and stuff) """

import sys
from argparse import ArgumentParser
from maketree.core.parser import Parser
from pathlib import Path


PROGRAM = "maketree"
VERSION = "0.0.1"


def main():
    args = parse_args()

    sourcefile = Path(args.src)
    dstpath = Path(args.dst)

    # SRC Exists?
    if not sourcefile.exists():
        print("source '%s' does not exist." % sourcefile)
        sys.exit(1)

    # SRC Tree file?
    if not sourcefile.name.endswith(".tree"):
        print("source '%s' is not a .tree file." % sourcefile)
        sys.exit(1)

    # DST Exists?
    if not dstpath.exists():
        print("destination path '%s' does not exist." % dstpath)
        sys.exit(1)

    # DST not a Dir?
    if not dstpath.is_dir():
        print("destination path '%s' is not a directory." % dstpath)
        sys.exit(1)


def parse_args():
    """Parse command-line arguments and return."""

    parser = ArgumentParser(
        prog=PROGRAM,
        usage="%(prog)s [OPTIONS]",
        description="A CLI tool to create directory structures from a structure file.",
    )

    parser.add_argument(
        "-v", "--version", action="version", version="%s %s" % (PROGRAM, VERSION)
    )
    parser.add_argument("src", help="source file (with .tree extension)")
    parser.add_argument(
        "dst",
        nargs="?",
        default=".",
        help="where to create the tree structure (default: %(default)s)",
    )

    return parser.parse_args()
