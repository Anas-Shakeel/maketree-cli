""" Contains Helper code to keep core logic clean. (things that don't fit anywhere, fit here) """

from os.path import exists, splitext
from platform import system
from typing import List, Union


# Windows, Darwin, Linux
OS: str = system()


def get_nonexisting_paths(paths: List[str]) -> List[str]:
    """Returns a list of non-existing paths from `paths` list."""
    return list(filter(lambda p: not exists(p), paths))


def get_existing_paths(paths: List[str]) -> List[str]:
    """Returns a list of existing paths from `paths` list."""
    return list(filter(lambda p: exists(p), paths))


def is_valid_extension(extension: str) -> bool:
    """
    ### Is Valid Extension
    Returns `True` if extension is valid, `False` otherwise.
    `extension` must contain a period `.`

    An extension is valid if it follows below criteria:
    - extension must be non-empty (excluding period `.`)
    - extension must have a period `.`
    - extension must not contain symbols, whitespaces
        - `\\/:*?"<>|` are illegal on Windows
        - `/:` are illegal on Mac
        - `/` are illegal on Linux
    """
    if not extension:
        return False

    if len(extension) < 2:
        return False

    if not extension.startswith("."):
        return False

    if extension.count(".") > 1:
        return False

    if OS == "Windows":
        # Got Illegals?
        if contains_chars(extension, r' \/:*?"<>|'):
            return False

    elif OS == "Darwin" and contains_chars(extension, "/:"):
        return False

    elif OS == "Linux" and "/" in extension:
        return False

    return True


def is_valid_file(filename: str) -> Union[bool, str]:
    """
    ### Is Valid File
    Validates filename. Returns `True` if valid, Returns `str` if invalid.
    This `str` is the cause of filename invalidation.

    #### ARGS:
    - `filename`: name of the file

    #### Note:
    This function is not a stripped down version of itself. (specific to needs of the `Parser`, minimal but fast)
    """
    if not filename:
        return "file name must not be empty"

    # Split filepath into root and extension
    root, ext_ = splitext(filename)

    # Root must not be empty
    if not root:
        return "invalid file name"

    # Check for illegal chars
    if OS == "Windows":
        if contains_chars(root, r'\/:?*<>"|'):
            return 'illegal characters are not allowed: \\/:?*<>|"'
    elif OS == "Darwin":
        if contains_chars(root, r"/:<>"):
            return "illegal characters are not allowed: /:?<>"
    else:  # Linux
        if contains_chars(root, r"/:<>"):
            return "illegal characters are not allowed: /:?<>"

    if ext_ and not is_valid_extension(ext_):
        return "invalid file extension"

    return True


def is_valid_dir(dirname: str) -> Union[bool, str]:
    """
    ### Is Valid Dirpath
    Validates directory name. Returns `True` if valid, Returns `str` if invalid.
    This `str` contains the reason for dir being invalid.

    #### ARGS:
    - `dirname`: the path to validate

    #### Note:
    This function is not a stripped down version of itself. (specific to needs of the `Parser`, minimal but fast)
    """
    if not dirname:
        return "directory must not be empty."

    # Check for illegal chars
    if OS == "Windows":
        if contains_chars(dirname, r'\/:?*<>"|'):
            return 'illegal characters are not allowed: \\/:?*<>|"'
    elif OS == "Darwin":
        if contains_chars(dirname, r"/:<>"):
            return "illegal characters are not allowed: /:?<>"
    else:
        if contains_chars(dirname, r"/:<>"):
            return "illegal characters are not allowed: /:?<>"

    return True


def contains_chars(string: str, chars: str) -> bool:
    """
    ### Contains
    Checks whether `string` contains a character from `chars`.
    Returns `True` if it does, `False` if does not.
    """
    return any(char for char in chars if char in string)
