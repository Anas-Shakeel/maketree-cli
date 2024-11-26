""" Responsible for validating the structure file and ensuring that the defined directory structure is correct and usable. """

from platform import system
from os.path import splitext
from typing import List, Dict, Union


class Validator:
    """Validator base class to validate parsed tree."""

    # Windows, Darwin, Linux
    OS: str = system()

    @classmethod
    def validate(cls, tree: List[Dict]):
        """Validate the tree. Returns `True` if valid, Returns `str` (an err message) for otherwise."""
        for entry in tree:
            if entry["type"] == "directory":
                # Validate dir
                valid = cls.is_valid_dir(entry["name"])
                if valid is not True:
                    return "%s: %s" % (entry["name"], valid)

                # Got children?
                if entry["children"]:
                    # Recurse
                    valid = cls.validate(entry["children"])
                    if valid is not True:
                        return valid

            else:  # File
                valid = cls.is_valid_file(entry["name"])
                if valid is not True:
                    return "%s: %s" % (entry["name"], valid)

        return True

    @classmethod
    def is_valid_extension(cls, extension: str) -> bool:
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

        if cls.OS == "Windows":
            # Got Illegals?
            if cls._contains(extension, r' \/:*?"<>|'):
                return False

        elif cls.OS == "Darwin" and cls._contains(extension, "/:"):
            return False

        elif cls.OS == "Linux" and "/" in extension:
            return False

        return True

    @classmethod
    def is_valid_file(cls, filename: str) -> Union[bool, str]:
        """
        ### Is Valid File
        Validates filename. Returns `True` if valid, Returns `str` if invalid.
        This `str` is the cause of filename invalidation.

        #### ARGS:
        - `filename`: name of the file
        """
        if not filename:
            return "file name must not be empty"

        # Split filepath into root and extension
        root, ext_ = splitext(filename)

        # Root must not be empty
        if not root:
            return "invalid file name"

        # TODO: Check for illegal chars here....
        if cls.OS == "Windows":
            if cls._contains(root, r'\/:?*<>"|'):
                return """illegal characters are not allowed: '\\/:?*<>|"'"""
        elif cls.OS == "Darwin":
            if cls._contains(root, r"/:<>"):
                return """illegal characters are not allowed: '/:?<>'"""
        else:  # Linux
            if cls._contains(root, r"/:<>"):
                return "illegal characters are not allowed: '/:?<>'"

        if ext_ and not cls.is_valid_extension(ext_):
            return "invalid file extension"

        return True

    @classmethod
    def is_valid_dir(cls, dirname: str) -> Union[bool, str]:
        """
        ### Is Valid Dirpath
        Validates directory name. Returns `True` if valid, Returns `str` if invalid.
        This `str` contains the reason for dir being invalid.

        #### ARGS:
        - `dirname`: the path to validate
        """
        if not dirname:
            return "directory must not be empty."

        # Check for illegal chars
        if cls.OS == "Windows":
            if cls._contains(dirname, r'\/:?*<>"|'):
                return """illegal characters are not allowed: '\\/:?*<>|"'"""
        elif cls.OS == "Darwin":
            if cls._contains(dirname, r"/:<>"):
                return """illegal characters are not allowed: '/:?<>'"""
        else:
            if cls._contains(dirname, r"/:<>"):
                return "illegal characters are not allowed: '/:?<>'"

        return True

    @classmethod
    def _contains(cls, part: str, chars: str) -> bool:
        """
        ### Contains
        Checks whether `part` contains a character from `chars`.
        Returns `True` if it does, `False` if does not.
        """
        return any(char for char in chars if char in part)
