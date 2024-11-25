""" Frontend of the project (Argument handling and stuff) """

import sys
from argparse import ArgumentParser
from maketree.core.parser import Parser


PROGRAM = "maketree"
VERSION = "0.0.1"


def main():
    args = parse_args()

    print(args)


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
