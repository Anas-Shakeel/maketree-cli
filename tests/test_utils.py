""" Tests for maketree/utils.py """

import os
import shutil

from maketree.utils import (
    contains_chars,
    is_valid_dir,
    is_valid_file,
    is_valid_extension,
    get_existing_paths,
    get_nonexisting_paths,
)


# Create temporary files/folders inside this and delete aftwards
TEMP_DIR = "temp"

paths = [
    os.path.join(TEMP_DIR, "file.txt"),
    os.path.join(TEMP_DIR, "file.json"),
    os.path.join(TEMP_DIR, ".gitignore"),
    os.path.join(TEMP_DIR, "LICENSE"),
]


def test_get_existing_paths():
    os.mkdir(TEMP_DIR)

    # Create first-two files in paths list.
    for p in paths[:2]:
        with open(p, "x") as _:
            pass

    # Get nonexisting paths...
    try:
        get_nonexisting_paths(paths) == paths[2:]
    finally:
        # Remove TEMP_DIR
        shutil.rmtree(TEMP_DIR)


def test_get_existing_paths():
    os.mkdir(TEMP_DIR)
    # Create First-two files in paths list.
    for p in paths[:2]:
        with open(p, "x") as _:
            pass

    # Get existings paths now...
    try:
        assert get_existing_paths(paths) == paths[:2]
    finally:
        # Remove TEMP_DIR
        shutil.rmtree(TEMP_DIR)


def test_is_valid_extension():
    assert is_valid_extension(".txt") == True
    assert is_valid_extension(".gitignore") == True
    assert is_valid_extension(".c") == True
    assert is_valid_extension(".🔥") == True

    assert is_valid_extension("file.txt") == False  # Accepts only extensions
    assert is_valid_extension("...txt") == False  # Too many periods
    assert is_valid_extension(".t/xt") == False  # slash
    assert is_valid_extension("txt") == False  # must start with period


def test_is_valid_file():
    assert is_valid_file("file.extension") == True
    assert is_valid_file("filewithoutextension") == True
    assert is_valid_file(".gitignore") == True
    assert is_valid_file("file 123.txt") == True
    assert is_valid_file(".") == True

    assert isinstance(is_valid_file(""), str)
    assert isinstance(is_valid_file("fi:le.txt"), str)

    # Only single part names are valid
    assert isinstance(is_valid_file("fi/le.txt"), str)


def test_is_valid_dir():
    assert is_valid_dir("folder") == True
    assert is_valid_dir("folder123") == True
    assert is_valid_dir("folder 134") == True
    assert is_valid_dir(".folder") == True
    assert is_valid_dir(".") == True

    assert isinstance(is_valid_dir("fol/der"), str)  # Only single part names are valid
    assert isinstance(is_valid_dir("fol:der"), str)


def test_contains_chars():
    assert contains_chars("ABCD", "C") == True
    assert contains_chars("ABCD", "c") == False

    assert contains_chars("1.2.1.3", ".,") == True  # Either . or ,
    assert contains_chars("1.2.1.3", ",:") == False  # Either , or :

    assert contains_chars("example@gmail.com", "(@)") == True  # Any of ( @ )
    assert contains_chars("example@gmail.com", "(:)") == False  # Any of ( : )

    assert contains_chars("abc def", " ") == True
    assert contains_chars("abcdef", " ") == False