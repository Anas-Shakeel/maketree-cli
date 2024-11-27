""" Responsible for validating the structure file and ensuring that the defined directory structure is correct and usable. """

from platform import system
from os.path import splitext
from typing import List, Dict, Union


class ValidationError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.args = args


class Validator:
    """Validator base class to validate parsed tree."""

    # Windows, Darwin, Linux
    OS: str = system()

    @classmethod
    def validate(cls, tree: List[Dict]):
        """Validate the tree. Returns `True` if valid, Returns `str` (an err message) for otherwise."""
        # Check for Name validation
        valid = cls.validate_tree(tree)
        if valid is not True:
            return valid

        # Check for duplications
        try:
            cls.check_duplicates(tree)
        except ValidationError as e:
            return str(e)

        # If reached this far, everythings good.
        return True

    @classmethod
    def check_duplicates(cls, tree: List[Dict]):
        """Check for duplicate entries in the tree. Raises `ValidationError` if duplicates found."""

        def traverse(node: Dict, path: List):
            # Keeps track of seen names in current dir
            seen_names = set()

            # Iterate through node's children
            for child in node.get("children", []):
                name = child["name"]

                # Already in set?
                if name in seen_names:
                    raise ValidationError(
                        f"Conflict: Name '{name}' already exists in {'/'.join(path)}"
                    )

                # Add in set
                seen_names.add(name)

                # Child a Directory? Recurse
                if child["type"] == "directory":
                    traverse(child, path + [name])

        # Treat tree as a directory.
        traverse(
            node={
                "type": "directory",
                "name": ".",
                "children": tree,
            },
            path=["."],
        )

        return True

    @classmethod
    def validate_tree(cls, tree: List[Dict]):
        for entry in tree:
            if entry["type"] == "directory":
                # Validate dir
                valid = cls.is_valid_dir(entry["name"])
                if valid is not True:
                    return "%s: %s" % (entry["name"], valid)

                # Got children?
                if entry["children"]:
                    # Recurse
                    valid = cls.validate_tree(entry["children"])
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
            if cls.contains_chars(extension, r' \/:*?"<>|'):
                return False

        elif cls.OS == "Darwin" and cls.contains_chars(extension, "/:"):
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
            if cls.contains_chars(root, r'\/:?*<>"|'):
                return """illegal characters are not allowed: '\\/:?*<>|"'"""
        elif cls.OS == "Darwin":
            if cls.contains_chars(root, r"/:<>"):
                return """illegal characters are not allowed: '/:?<>'"""
        else:  # Linux
            if cls.contains_chars(root, r"/:<>"):
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
            if cls.contains_chars(dirname, r'\/:?*<>"|'):
                return """illegal characters are not allowed: '\\/:?*<>|"'"""
        elif cls.OS == "Darwin":
            if cls.contains_chars(dirname, r"/:<>"):
                return """illegal characters are not allowed: '/:?<>'"""
        else:
            if cls.contains_chars(dirname, r"/:<>"):
                return "illegal characters are not allowed: '/:?<>'"

        return True

    @classmethod
    def contains_chars(cls, string: str, chars: str) -> bool:
        """
        ### Contains
        Checks whether `string` contains a character from `chars`.
        Returns `True` if it does, `False` if does not.
        """
        return any(char for char in chars if char in string)
