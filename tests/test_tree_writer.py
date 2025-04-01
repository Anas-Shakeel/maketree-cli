"""Tests for maketree/core/tree_writer.py"""

from os import mkdir
from shutil import rmtree
from maketree.core.tree_writer import TreeWriter
from maketree.core.parser import Parser
from maketree.console import Console

# Create temporary files/folders inside this and delete aftwards
TEMP_DIR = "temp"

console = Console(verbose=False, no_color=True)


def test_write():
    # Create TEMP directory
    try:
        mkdir(TEMP_DIR)
    except FileExistsError:
        pass

    sample_tree = [
        ("directory", "src", 0),
        ("file", "file.html", 1),
        ("file", "README.md", 0),
    ]

    # Write the tree
    filename = TreeWriter.write(sample_tree, console=console, save_to=TEMP_DIR)

    # Parse the file
    parsed_tree = Parser().parse_file(filename)

    assert parsed_tree[0]["type"] == "directory"
    assert parsed_tree[0]["name"] == "src"
    assert parsed_tree[0]["children"][0]["name"] == "file.html"

    assert parsed_tree[1]["type"] == "file"
    assert parsed_tree[1]["name"] == "README.md"

    rmtree(TEMP_DIR)
