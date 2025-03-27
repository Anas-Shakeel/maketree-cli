"""Tests for maketree/utils.py"""

import os
import shutil
from sys import platform

from maketree.utils import (
    is_valid_dirpath,
    _contains,
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


def test_get_non_existing_paths():
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
    try:
        os.mkdir(TEMP_DIR)
    except FileExistsError:
        pass

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
    # Valid in Windows, Mac, Linux
    valid_filenames = [
        "valid_file.txt",
        "another_valid-file_123.log",
        "My document 2025.txt",
        "UPPERCASE FILE",
        "file with spaces.txt",
        "report_v1.2-final.log",
        ".config",
        ".con.txt",
        "con1.txt",
    ]
    for filename in valid_filenames:
        assert is_valid_file(filename) == True

    # Invalid filenames
    invalid_filenames = [
        "invalid|file.txt",
        "invalid:file?.txt",
        "<badfile>.txt",
        "file/name.txt",
        "file\\name.txt",
        "folder/subfolder/name.txt",
        "..somefile.txt",
        "file\tname.txt",
        "file\0name.txt",
        "",
        " ",
        ".",
        "..",
    ]
    for filename in invalid_filenames:
        assert isinstance(is_valid_file(filename), str)

    # Windows Reserved Words
    if platform == "win32":
        reserved_words = [
            "CON.txt",
            "Aux.txt",
            "nuL",
            "COM7",
            "LpT4.file",
        ]
        for word in reserved_words:
            assert isinstance(is_valid_file(word), str)


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


def test_is_valid_dirpath():
    assert is_valid_dirpath(".") == True
    assert is_valid_dirpath("folder") == True
    assert is_valid_dirpath("./folder/") == True
    assert is_valid_dirpath("folder/folder1/folder2/folder3/folder/4") == True
    assert is_valid_dirpath("./folder/") == True

    assert isinstance(is_valid_dirpath("./fol<der>/"), str)
    assert isinstance(is_valid_dirpath("./fol<der/fo>lder/"), str)
    assert isinstance(is_valid_dirpath(""), str)


def test_contains():
    parts = [
        "abcd",
        "abcde",
        "testing",
        "testing123",
    ]

    assert _contains(parts, "2td") == True
    assert _contains(parts, "2td") == True
    assert _contains(parts, "_:") == False  # None of parts contain _ or :
    assert _contains(parts, "xz") == False  # None of parts contain x or z
