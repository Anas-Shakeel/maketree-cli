""" Frontend of the project (Argument handling and stuff) """

import sys
from pathlib import Path
from argparse import ArgumentParser
from maketree.core.parser import Parser, ParseError
from maketree.core.tree_builder import TreeBuilder
from maketree.core.normalizer import Normalizer
from maketree.utils import get_existing_paths, print_on_true, print_tree
from typing import List, Dict, Tuple


PROGRAM = "maketree"
VERSION = "1.0.1"


def main():
    args = parse_args()

    sourcefile = Path(args.src)
    dstpath = Path(args.dst)
    VERBOSE: bool = args.verbose
    OVERWRITE: bool = args.overwrite
    SKIP: bool = args.skip
    PRINT_TREE = args.graphical

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

    # Mutually Exclusive
    if OVERWRITE and SKIP:
        error(
            "Options --overwrite and --skip are mutually exlusive. (use one or the other, not both)"
        )

    # Parse the source file
    print_on_true("Parsing %s..." % sourcefile, VERBOSE)
    try:
        parsed_tree = Parser.parse_file(sourcefile)
    except ParseError as e:
        error(e)

    # Print the graphical tree and Exit.
    if PRINT_TREE:
        print_tree(parsed_tree)
        sys.exit(0)

    # Create paths from tree nodes
    print_on_true("Creating tree paths", VERBOSE)
    paths: Dict[str, List[str]] = Normalizer.normalize(parsed_tree, dstpath)

    # If Overwrite and Skip both are false
    print_on_true("Checking existing tree paths", VERBOSE)
    if not OVERWRITE and not SKIP:
        if count := print_existing_paths(paths["files"]):
            error(
                f"\nFix {count} issue{'s' if count > 1 else ''} before moving forward."
            )

    # Create the files and dirs finally
    print_on_true("Creating tree on filesystem", VERBOSE)
    creation_count: Tuple[int, int] = TreeBuilder.build(
        paths, skip=SKIP, verbose=VERBOSE
    )
    print_on_true("Done.\n", VERBOSE)

    # Completion message
    print(
        "%d directories and %d files have been created."
        % (creation_count[0], creation_count[1])
    )


def parse_args():
    """Parse command-line arguments and return."""

    parser = ArgumentParser(
        prog=PROGRAM,
        usage="%(prog)s [OPTIONS]",
        epilog="%s %s" % (PROGRAM.title(), VERSION),
        description="A CLI tool to create directory structures from a structure file.",
    )

    parser.add_argument("src", help="source file (with .tree extension)")
    parser.add_argument(
        "dst",
        nargs="?",
        default=".",
        help="where to create the tree structure (default: %(default)s)",
    )
    parser.add_argument(
        "-g",
        "--graphical",
        action="store_true",
        help="show source file as graphical tree and exit",
    )
    parser.add_argument(
        "-o", "--overwrite", action="store_true", help="overwrite existing files"
    )
    parser.add_argument("-s", "--skip", action="store_true", help="skip existing files")
    # parser.add_argument(
    #     "-v", "--version", action="version", version="%s %s" % (PROGRAM, VERSION)
    # )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase verbosity"
    )

    return parser.parse_args()


def error(message: str):
    """Print `message` and exit with status `1`. Use upon errors only."""
    print(message)
    sys.exit(1)


def print_existing_paths(paths: List[str]) -> int:
    """Print existing paths. Return the number of paths that exist."""
    count = 0
    if existing_paths := get_existing_paths(paths):
        count = len(existing_paths)
        for path in existing_paths:
            print("Warning: File '%s' already exists" % path)

    return count
