""" Tests for maketree/core/tree_builder.py """

import shutil
from os.path import exists
from os import mkdir
from maketree.core.parser import Parser
from maketree.core.normalizer import Normalizer
from maketree.core.tree_builder import TreeBuilder
from maketree.console import Console

TEMP_DIR = "temp"


def test_build():
    console = Console(False, True)
    src = """ 
src/
    file.txt
    file.py
README.md
.gitignore
"""
    parsed_tree = Parser._parse_lines(src.splitlines())
    paths = Normalizer.normalize(parsed_tree, rootpath=TEMP_DIR)

    # Make temp directory
    try:
        mkdir(TEMP_DIR)
    except FileExistsError:
        pass

    # Build the tree
    build_count = TreeBuilder.build(paths, console=console)

    assert build_count[0] == len(paths["directories"])
    assert build_count[1] == len(paths["files"])

    # Check if they are actually created.
    assert exists(paths["directories"][0]) == True
    assert exists(paths["files"][0]) == True
    assert exists(paths["files"][1]) == True
    assert exists(paths["files"][2]) == True
    assert exists(paths["files"][3]) == True

    # Remove temp directory
    shutil.rmtree(TEMP_DIR)
