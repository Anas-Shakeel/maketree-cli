""" Frontend of the project (Argument handling and stuff) """

import sys
from pathlib import Path
from argparse import ArgumentParser
from maketree.core.parser import Parser, ParseError
from maketree.core.tree_builder import TreeBuilder
from maketree.core.normalizer import Normalizer
from maketree.terminal_colors import colored
from maketree.console import Console
from maketree.utils import (
    get_existing_paths,
    print_tree,
    create_dir,
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
    NO_CONFIRM = args.no_confirm

    # Console? (is this fuc**ing Yavascript?)
    console = Console(VERBOSE, NO_COLORS)

    # SRC Exists?
    if not sourcefile.exists():
        console.error("source '%s' does not exist." % sourcefile)

    # SRC Tree file?
    if not sourcefile.name.endswith(".tree"):
        console.error("source '%s' is not a .tree file." % sourcefile)

    # DST Exists?
    if not dstpath.is_dir():
        if CREATE_DST:
            console.verbose("Creating '%s'..." % dstpath)
            created = create_dir(dstpath)
            if created is not True:
                console.error(created)
        else:
            console.error(
                "destination path '%s' does not exist."
                % colored(str(dstpath), "light_red"),
            )

    # Mutually Exclusive
    if OVERWRITE and SKIP:
        console.error(
            "Options --overwrite and --skip are mutually exlusive. "
            "(use one or the other, not both)"
        )

    # Parse the source file
    console.verbose("Parsing %s..." % sourcefile)
    try:
        parsed_tree = Parser.parse_file(sourcefile)
    except ParseError as e:
        console.error(e)

    # Print the graphical tree and Exit.
    if PRINT_TREE:
        print_tree(parsed_tree)
        sys.exit(0)

    # Confirm before proceeding
    if not NO_CONFIRM:
        print_tree(parsed_tree, dstpath)
        proceed: bool = console.input_confirm(
            "Create this structure? (y/N): ", fgcolor="light_magenta"
        )
        if not proceed:
            sys.exit(0)

    console.verbose("Creating tree paths...")

    # Create paths from tree nodes
    paths: Dict[str, List[str]] = Normalizer.normalize(parsed_tree, dstpath)

    # If Overwrite and Skip both are false
    if not OVERWRITE and not SKIP:
        console.verbose("Checking existing paths...")
        # Check existing paths
        existing_paths = get_existing_paths(paths["files"])
        count = len(existing_paths)

        # Any path exists?
        if count:
            console.print_lines(
                existing_paths,
                "Warning: File already exists: ",
                color="light_yellow",
            )
            console.error(
                f"Found {count} existing files, cannot proceed. "
                "(try %s or %s)"
                % (
                    colored("--skip", "light_yellow"),
                    colored("--overwrite", "light_yellow"),
                )
            )

    console.verbose("Creating tree on filesystem...\n")

    # Create the files and dirs finally
    build_count = TreeBuilder.build(
        paths,
        console,
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
        "-nC",
        "--no-confirm",
        action="store_true",
        help="don't ask for confirmation",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase verbosity"
    )

    return parser.parse_args()
