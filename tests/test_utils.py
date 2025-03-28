"""Tests for maketree/utils.py"""

import os
import shutil
from sys import platform
from datetime import datetime

from maketree.utils import (
    is_valid_dirpath,
    _contains,
    contains_chars,
    is_valid_dir,
    is_valid_file,
    get_existing_paths,
    get_nonexisting_paths,
    incremented_filename,
    now,
    create_dir,
    get_os_name,
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
    try:
        os.mkdir(TEMP_DIR)
    except FileExistsError:
        pass

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
        "..somefile.txt",  # valid because no slash /
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
        "../somefile.txt",  # invalid because of slash /
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
    # Valid in Windows, Mac, Linux
    valid_dirnames = [
        "valid_directory",
        "another_valid-dir_123",
        "My documents - 2025",
        "UPPERCASE DIR",
        "dir with spaces",
        "report_v1.2-final",
        ".config",
        "..somedir",
    ]
    for dirname in valid_dirnames:
        assert is_valid_dir(dirname) == True

    # Invalid dirnames
    invalid_dirnames = [
        "invalid|dir",
        "invalid:dir?",
        "<bad-dir>",
        "dir/name",
        "dir\\name",
        "../somedir",
        "dir\tname",
        "dir\0name",
        "",
        " ",
        ".",
        "..",
    ]
    for dirname in invalid_dirnames:
        assert isinstance(is_valid_dir(dirname), str)

    # Windows Reserved Words
    if platform == "win32":
        reserved_words = [
            "CON",
            "Aux",
            "nuL",
            "COM7",
            "LpT4",
        ]
        for word in reserved_words:
            assert isinstance(is_valid_dir(word), str)


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
    # Valid in Windows, Mac, Linux
    valid_dirs = [
        "valid_directory",
        "My documents - 2025",
        "UPPERCASE DIR",
        "report/v1.2/final",
        ".config",
        ".",
        "../..",
        "..somedir",
        "./folder/",
        "folder/folder1/folder2/folder3/folder/4",
        "G:\\folder\\folder1\\folder2",
        "/folder/folder1/folder2/",
    ]
    for dir_ in valid_dirs:
        assert is_valid_dirpath(dir_) == True

    # TODO: Add Linux/Mac specific tests for invalid directories

    # Windows Specific Tests
    if platform == "win32":
        # Invalid dirs
        invalid_dirs = [
            "invalid|dir",
            "invalid:dir?",
            "bad/<dir>",
            "dir\tname",
            "dir\0name",
            "",
            " ",
        ]
        for dir_ in invalid_dirs:
            assert isinstance(is_valid_dirpath(dir_), str)

        # Reserved Words
        reserved_words = [
            "CON",
            "Aux",
            "nuL",
            "COM7",
            "LpT4",
        ]
        for word in reserved_words:
            assert isinstance(is_valid_dirpath(word), str)


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


def test_now():
    format_ = "%d %B %Y %I:%M %p"
    assert now(format_) == datetime.now().strftime(format_)


def test_incremented_filename():
    # Make a TEMP dir
    try:
        os.mkdir(TEMP_DIR)
    except FileExistsError:
        pass

    # Test
    try:
        filepath = "%s/file.txt" % TEMP_DIR
        expected_filepath = os.path.join(TEMP_DIR, "file_1.txt")

        # Create temp file
        with open(filepath, "w") as f:
            pass

        assert incremented_filename(filepath) == expected_filepath
    finally:
        # Remove TEMP dir
        shutil.rmtree(TEMP_DIR)


def test_create_dir():
    # Create temp dir
    try:
        os.mkdir(TEMP_DIR)
    except FileExistsError:
        pass

    # Test
    try:
        # Create a directory
        dir_path = "%s/test/directory" % TEMP_DIR
        assert create_dir(dir_path) is True

        # Created?
        assert os.path.exists(dir_path) is True

    finally:
        shutil.rmtree(TEMP_DIR)


def test_get_os_name():
    if platform == "win32":
        os_name = "Windows"
    elif platform == "darwin":
        os_name = "MacOS"
    else:
        os_name = "Linux"

    assert get_os_name() == os_name
