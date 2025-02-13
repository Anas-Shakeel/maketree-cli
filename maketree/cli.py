""" Frontend of the project (Argument handling and stuff) """

import sys
from pathlib import Path
from argparse import ArgumentParser
from maketree.core.parser import Parser, ParseError
from maketree.core.tree_builder import TreeBuilder
from maketree.core.normalizer import Normalizer
from maketree.terminal_colors import colored, printc
from maketree.utils import (
    get_existing_paths,
    print_tree,
    create_dir,
    _print,
)
from typing import List, Dict, Tuple


PROGRAM = "maketree"
VERSION = "1.0.2"


def main():
    args = parse_args()

    sourcefile = Path(args.src)
    dstpath = Path(args.dst)
    CREATE_DST = args.create_dst
    VERBOSE: bool = args.verbose
    OVERWRITE: bool = args.overwrite
    SKIP: bool = args.skip
    PRINT_TREE = args.graphical
    NO_COLORS = args.no_color

    # SRC Exists?
    if not sourcefile.exists():
        error("source '%s' does not exist." % sourcefile)

    # SRC Tree file?
    if not sourcefile.name.endswith(".tree"):
        error("source '%s' is not a .tree file." % sourcefile)

    # DST Exists?
    if not dstpath.is_dir():
        if CREATE_DST:
            created = create_dir(dstpath)
            if created is not True:
                error(created)
        else:
            error("destination path '%s' is not an existing directory." % dstpath)

    # Mutually Exclusive
    if OVERWRITE and SKIP:
        error(
            "Options --overwrite and --skip are mutually exlusive. "
            "(use one or the other, not both)"
        )

    # Parse the source file
    _print("Parsing %s..." % sourcefile, VERBOSE, NO_COLORS, "light_magenta")
    try:
        parsed_tree = Parser.parse_file(sourcefile)
    except ParseError as e:
        error(e)

    # Print the graphical tree and Exit.
    if PRINT_TREE:
        print_tree(parsed_tree)
        sys.exit(0)

    # Confirm before proceeding
    print_tree(parsed_tree, dstpath)
    proceed: bool = input_confirm("\nCreate this structure? (y/N): ", NO_COLORS)
    if not proceed:
        sys.exit(0)

    _print("\nCreating tree paths...", VERBOSE, NO_COLORS, "light_magenta")

    # Create paths from tree nodes
    paths: Dict[str, List[str]] = Normalizer.normalize(parsed_tree, dstpath)

    _print("Checking existing tree paths...", VERBOSE, NO_COLORS, "light_magenta")

    # If Overwrite and Skip both are false
    if not OVERWRITE and not SKIP:
        if count := print_existing_paths(paths["files"], NO_COLORS):
            error(
                f"\nFix {count} issue{'s' if count > 1 else ''} "
                "before moving forward."
            )

    _print("Creating tree on filesystem...\n", VERBOSE, NO_COLORS, "light_magenta")

    # Create the files and dirs finally
    build_count = TreeBuilder.build(
        paths,
        skip=SKIP,
        overwrite=OVERWRITE,
        verbose=VERBOSE,
        no_color=NO_COLORS,
    )

    # Completion message
    if not NO_COLORS:
        built_dirs = colored(f"{build_count[0]} directories", "light_green")
        built_files = colored(f"{build_count[1]} files", "light_green")
    else:
        built_dirs = f"{build_count[0]} directories"
        built_files = f"{build_count[1]} files"

    print(f"\n{built_dirs} and {built_files} have been created.")


def parse_args():
    """Parse command-line arguments and return."""

    parser = ArgumentParser(
        prog=PROGRAM,
        usage="%(prog)s [OPTIONS]",
        epilog="%s %s" % (PROGRAM.title(), VERSION),
        description="Create project structures effortlessly.",
    )

    parser.add_argument("src", help="source file (with .tree extension)")
    parser.add_argument(
        "dst",
        nargs="?",
        default=".",
        help="where to create the tree structure (default: %(default)s)",
    )
    parser.add_argument(
        "-cd",
        "--create-dst",
        action="store_true",
        help="create destination folder if it doesn't exist.",
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
    parser.add_argument(
        "-nc",
        "--no-color",
        action="store_true",
        help="don't use colors in output",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase verbosity"
    )

    return parser.parse_args()


def error(message: str):
    """Print `message` and exit with status `1`. Use upon errors only."""
    printc(message, "light_red")
    sys.exit(1)


def print_existing_paths(paths: List[str], no_color: bool = False) -> int:
    """Print existing paths. Return the number of paths that exist."""
    count = 0
    if existing_paths := get_existing_paths(paths):
        print()  # Initial newline
        count = len(existing_paths)
        for path in existing_paths:
            _print(
                "Warning: File '%s' already exists" % path,
                no_color=no_color,
                fgcolor="yellow",
            )

    return count


def input_confirm(message: str, no_color: bool = False) -> bool:
    """Confirm and return `true` or `false`"""
    while True:
        try:
            _print(message, no_color=no_color, fgcolor="light_magenta", end="")
            answer = input().lower()
            if answer == "y" or answer == "yes":
                return True
            elif answer == "n" or answer == "no":
                return False

            # Otherwise just repeat
            continue
        except KeyboardInterrupt:
            # Force quit
            sys.exit(1)
        except:
            continue
