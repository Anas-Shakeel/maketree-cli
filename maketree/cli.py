""" Frontend of the project (Argument handling and stuff) """

import sys
from pathlib import Path
from argparse import ArgumentParser
from maketree.core.parser import Parser, ParseError
from maketree.core.validator import Validator
from maketree.core.tree_builder import TreeBuilder
from maketree.core.normalizer import Normalizer
from typing import List, Dict


PROGRAM = "maketree"
VERSION = "0.0.2"


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

    # Create paths from tree nodes
    paths: Dict[str, List[str]] = Normalizer.normalize(parsed_tree, dstpath)

    # Further validate paths
    if issues := validate(paths):
        error(f"\nFix {issues} issue{'s' if issues > 1 else ''} before moving forward.")

    # Create the files and dirs finally
    TreeBuilder.build(paths)

    # Completion message
    print(
        "%d directories and %d files have been created successfully."
        % (len(paths["directories"]), len(paths["files"]))
    )


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


def validate(paths: Dict[str, List[str]]) -> int:
    """
    Further validate the normalized paths.
    Returns the number of issues. `0` is safe to continue.
    """
    # Number of issues found
    issue_count = 0

    # Check for existing paths
    directories = Validator.paths_exist(paths["directories"])
    files = Validator.paths_exist(paths["files"])

    # Print existing dirs
    if directories:
        for path in directories:
            print("Warning: Directory '%s' already exists." % path)

    # Print existing files
    if files:
        for path in files:
            print("Warning: File '%s' already exists." % path)

    # Update issues, if any
    issue_count = len(directories) + len(files)

    # Return no. of issues found
    return issue_count
