from os import mkdir
from pathlib import Path
from shutil import rmtree
from maketree.core.extractor import Extractor
from maketree.console import Console

# Create temporary files/folders inside this and delete aftwards
TEMP_DIR = "temp"

console = Console(verbose=False, no_color=True)


def test_extract():
    # Create TEMP directory with files
    try:
        mkdir(TEMP_DIR)
    except FileExistsError:
        pass

    sample_tree = [
        f"{TEMP_DIR}/folder/",
        f"{TEMP_DIR}/file1.txt",
        f"{TEMP_DIR}/file2.csv",
        f"{TEMP_DIR}/file3.json",
    ]

    try:
        mkdir(sample_tree[0])
    except FileExistsError:
        pass

    try:
        for file in sample_tree[1:]:
            with open(file, "w") as _:
                pass
    except FileExistsError:
        pass

    # Extract the tree
    tree = Extractor.extract(Path(TEMP_DIR), console=console)

    # Sort the tree (Windows and Linux traverse differently)
    sorted_tree = sorted(tree[1:], key=lambda x: x[1])  # Sort by name

    # Check Types (directory or file)
    assert sorted_tree[0][0] == "file"
    assert sorted_tree[-1][0] == "directory"

    # Check Indentations
    assert sorted_tree[0][2] == 1
    assert sorted_tree[1][2] == 1

    # Check Names
    assert sorted_tree[0][1] == "file1.txt"
    assert sorted_tree[1][1] == "file2.csv"
    assert sorted_tree[2][1] == "file3.json"

    rmtree(TEMP_DIR)
