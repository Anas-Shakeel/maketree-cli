"""Contains Helper code to keep core logic clean. (things that don't fit anywhere, fit here)"""

from os import makedirs
from os.path import exists, splitext
from pathlib import Path
from platform import system
from typing import List, Dict, Union, Iterable, Optional
from maketree.terminal_colors import colored
from maketree.console import Console


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
            return 'avoid these illegal characters: \\/:?*<>|"'
    elif OS == "Darwin":
        if contains_chars(root, r"/:<>"):
            return "avoid these illegal characters: /:?<>"
    else:  # Linux
        if contains_chars(root, r"/:<>"):
            return "avoid these illegal characters: /:?<>"

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
        return "path must not be empty."

    # Check for illegal chars
    if OS == "Windows":
        if contains_chars(dirname, r'\/:?*<>"|'):
            return 'avoid these illegal characters: \\/:?*<>|"'
    elif OS == "Darwin":
        if contains_chars(dirname, r"/:<>"):
            return "avoid these illegal characters: /:?<>"
    else:
        if contains_chars(dirname, r"/:<>"):
            return "avoid these illegal characters: /:?<>"

    return True


def is_valid_dirpath(dirpath: str, max_length: int = 250):
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

    Used for longer dir paths.
    """
    if not dirpath:
        return "path must not be empty."

    d = Path(dirpath)
    if d.drive:
        root_parts = d.parts[1:]
    elif OS == "Linux" and (d.parts and d.parts[0] == "/"):
        root_parts = d.parts[1:]
    else:
        root_parts = d.parts

    if sum(len(part) for part in root_parts) > max_length:
        return (
            f"maximum length of path can be {max_length} (excluding slashes and drive)"
        )

    # Check for illegal chars
    if OS == "Windows":
        if _contains(root_parts, r'\/:?*<>"|'):
            return 'avoid these characters: \\/:?*<>|"'
    elif OS == "Darwin":
        if _contains(root_parts, r"/:<>"):
            return "avoid these characters: /:<>"
    else:
        if _contains(root_parts, r"/:<>"):
            return "avoid these characters: /:<>"

    return True


def _contains(parts: Iterable[str], chars: str) -> bool:
    """
    ### Contains
    Checks whether a string in `parts` contains a character from `chars`.
    Returns `True` if it does, `False` if does not.

    Used with `is_valid_dirpath` only.
    """
    for char in chars:
        for part in parts:
            if char in part:
                return True
    return False


def contains_chars(string: str, chars: str) -> bool:
    """
    ### Contains
    Checks whether `string` contains a character from `chars`.
    Returns `True` if it does, `False` if does not.

    Used with `is_valid_dir`.
    """
    return any(char for char in chars if char in string)


def print_tree(tree: List[Dict], console: Console, root: str = "."):
    """Prints the parsed `tree` in a graphical format. _(Not perfect but, gets the job done)_"""
    tab = 0
    BAR = console.colored("│   ", "dark_grey")
    LINK = console.colored("├───", "dark_grey")
    LINK_LAST = console.colored("└───", "dark_grey")
    FMT_STR = f"%s%s %s"

    def traverse(node: Dict, childs: int):
        nonlocal tab
        count = 0  # keeps track of child counts

        for child in node.get("children", []):
            count += 1

            child_name = child["name"]

            # Add a Slash '/' after a directory
            if child["type"] == "directory":
                child_name = console.colored(
                    "%s/" % child_name,
                    fgcolor="light_green",
                    attrs=["italic", "bold"],
                )

            if count == childs:
                # Last Child
                print(FMT_STR % (BAR * tab, LINK_LAST, child_name))
            else:
                # Others
                print(FMT_STR % (BAR * tab, LINK, child_name))

            if child["type"] == "directory" and child["children"]:
                tab += 1
                traverse(child, len(child["children"]))
        tab -= 1
        return

    root = str(root) if str(root) == "." else f"{root}/"
    print(
        console.colored(
            root,
            fgcolor="light_green",
            attrs=["italic", "bold"],
        )
    )

    traverse(
        node={
            "type": "directory",
            "name": root,
            "children": tree,
        },
        childs=len(tree),
    )


def create_dir(path: str):
    """Create a folder/directory on the filesystem."""
    # Create folder
    try:
        makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        return str(e)


def incremented_filename(filepath: Union[Path, str], dst_path: str = "") -> str:
    """
    ### Incremented Filename
    Increments filename in the `filepath` if file already exists in `dst_path`.

    if `dst_path` is omitted, method will use the `filepath`'s root dir to look
    if filename exists or not.

    ```
    >> incremented_filename("path/to/file.txt")
    # IF File already exists
    'path/to/file_1.txt'

    # Otherwise
    'path/to/file.txt'
    ```
    """
    filepath = Path(filepath)

    # Exists? return if not
    if not filepath.exists():
        return str(filepath)

    # Set root path
    if dst_path == "":
        # DST_PATH omitted?, use file's path
        root = filepath.parent
    else:
        root = dst_path

    # Convert root to Path Object
    root = Path(root)

    # Extract filename and extension
    filename = filepath.stem
    extension = filepath.suffix

    # Create new_name
    new_name = root / (filename + extension)

    # File exists?
    if new_name.exists():
        num = 1
        while True:
            new_name = f"{root / filename}_{num}{extension}"
            if not exists(new_name):
                return new_name
            num += 1
    else:
        return str(new_name)
