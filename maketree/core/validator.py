""" Responsible for validating the structure file and ensuring that the defined directory structure is correct and usable. """

from pathlib import Path
from os.path import splitext
from typing import List, Dict, Union


class Validator:
    """Validator base class to validate parsed tree."""

    @classmethod
    def validate(cls, tree: List[Dict]):
        """Validate the tree. Returns `True` if valid, Returns `str` (an err message) for otherwise."""
        pass

    @classmethod
    def is_valid_extension(cls, extension: str) -> bool:
        """
        ### Is Valid Extension
        Returns `True` if extension is valid, `False` otherwise.
        `extension` must contain a period `.`

        An extension is valid if it follows below criteria:
        - extension must be non-empty
        - extension must have a period `.`
        - extension must not contain symbols, whitespaces
            - `\\/:*?"<>|` are illegal on Windows
            - `/:` are illegal on Mac
            - `/` are illegal on Linux
        - extension must have atleast one character (excluding period)

        #### Example:
        ```
        >> pins.is_valid_extension(".txt")
        True
        >> pins.is_valid_extension(".")
        False
        >> pins.is_valid_extension("txt")
        False
        ```
        """
        if not extension:
            return False

        if len(extension) < 2:
            return False

        if not extension.startswith("."):
            return False

        if extension.count(".") > 1:
            return False

        if cls.OS == "Windows":
            if " " in extension:
                return False

            for char in r'\/:*?"<>|':
                if char in extension:
                    return False
        elif cls.OS == "Darwin" and ("/" in extension or ":" in extension):
            return False
        elif cls.OS == "Linux" and "/" in extension:
            return False

        return True

    @classmethod
    def is_valid_filepath(
        cls, filepath: str, extension="*", max_length: int = 250
    ) -> Union[bool, str]:
        """
        ### Is Valid Filepath
        Validates filepath. Returns `True` if valid, Returns `str` if invalid.
        This `str` contains the reason for path being invalid.

        #### ARGS:
        - `filepath`: the filepath string to validate
        - `extension`: the extension to match
            - `.py`: accept only .py files (any extension can be provided)
            - `*`: accept any extension
            - `None`: accept any extension (but not required!)
        - `max_length`: maximum length of the path (excluding extension, slashes and drive letter)

        #### Example:
        ```
        >> is_valid_filepath("path\\to\\fock.txt")
        True
        >> is_valid_filepath("path\\to\\f**k.txt")
        'Illegal characters are not allowed: \\/:?*<>|"'
        ```
        """
        if not filepath:
            return "Path must not be empty."

        # Split filepath into root and extension
        root, ext_ = splitext(filepath)

        # # Root must not be empty
        if not root:
            return "Invalid filepath."

        dir_is_valid = cls.is_valid_dirpath(root, max_length)
        if dir_is_valid != True:
            return dir_is_valid

        # Extension Validation
        if isinstance(extension, str):
            if len(ext_) < 2:
                return "Filepath is missing an extension."
            if extension != "*" and ext_.lower() != extension.lower():
                return f"Only '{extension}' files are allowed."
            elif extension == "*" and not cls.is_valid_extension(ext_):
                return f"Invalid extension: '{ext_}'"
        else:
            if ext_ and not cls.is_valid_extension(ext_):
                return f"Invalid extension: '{ext_}'"

        return True

    @classmethod
    def is_valid_dirpath(cls, dirpath: str, max_length: int = 250):
        """
        ### Is Valid Dirpath
        Validates directory path. Returns `True` if valid, Returns `str` if invalid.
        This `str` contains the reason for path being invalid.

        #### ARGS:
        - `dirpath`: the path to validate
        - `max_length`: maximum length to allow (length of the whole path, except drive)

        #### Example:
        ```
        >> is_valid_dirpath("path\\to\\folder")
        True
        >> is_valid_dirpath("path\\to\\*Illegal*folder")
        'Illegal characters are not allowed: \\/:?*<>|"'
        ```

        Raises `AssertionError` if:
        - `dirpath` is not a string
        """
        if not dirpath:
            return "Path must not be empty."

        d = Path(dirpath)
        if d.drive:
            root_parts = d.parts[1:]
        elif cls.OS == "Linux" and d.parts[0] == "/":
            root_parts = d.parts[1:]
        else:
            root_parts = d.parts

        if sum(len(part) for part in root_parts) > max_length:
            return f"Maximum length of path can be {max_length} (excluding slashes and drive)"

        # Check for illegal chars
        if cls.OS == "Windows":
            if cls._contains(root_parts, r'\/:?*<>"|'):
                return """Illegal characters are not allowed: '\\/:?*<>|"'"""
        elif cls.OS == "Darwin":
            if cls._contains(root_parts, r"/:<>"):
                return """Illegal characters are not allowed: '/:?<>'"""
        else:
            if cls._contains(root_parts, r"/:<>"):
                return "Illegal characters are not allowed: '/:?<>'"

        return True
