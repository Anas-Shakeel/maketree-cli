""" Frontend of the project (Argument handling and stuff) """

import sys
from pathlib import Path
from argparse import ArgumentParser
from maketree.core.parser import Parser, ParseError
from maketree.core.validator import Validator


PROGRAM = "maketree"
VERSION = "0.0.1"


def main():
    args = parse_args()

    sourcefile = Path(args.src)
    dstpath = Path(args.dst)

    # SRC Exists?
    if not sourcefile.exists():
        error("source '%s' does not exist." % sourcefile)

    # SRC Tree file?
    if not sourcefile.name.endswith(".tree"):
        error("source '%s' is not a .tree file." % sourcefile)

    # DST Exists?
    if not dstpath.exists():
        error("destination path '%s' does not exist." % dstpath)

    # DST not a Dir?
    if not dstpath.is_dir():
        error("destination path '%s' is not a directory." % dstpath)

    # Send file to parser
    try:
        parsed_tree = Parser.parse_file(sourcefile)
    except ParseError as e:
        error(e)


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


def error(message: str):
    """Print `message` and exit with status `1`. Use upon errors only."""
    print(message)
    sys.exit(1)
