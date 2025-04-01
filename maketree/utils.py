"""Contains Helper code to keep core logic clean. (things that don't fit anywhere, fit here)"""

import re
from sys import platform
from os import makedirs
from os.path import exists, splitext, join
from pathlib import Path
from typing import List, Dict, Set, Union, Iterable, Optional
from maketree.terminal_colors import colored
from maketree.console import Console
from datetime import datetime


# File/Dir Name REGEXes
FILENAME_REGEX = re.compile(r'^(?!^(?:\.{1,2})$)[^<>:"/\\|?*\0\t\r\n]+$')
DIRNAME_REGEX = re.compile(r'^[^<>:"|?*\0\t\r\n]+$')

# Special words (Windows doesn't allow files or dirs with these names)
RESERVED_WINDOWS_NAMES: Set[str] = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "COM5",
    "COM6",
    "COM7",
    "COM8",
    "COM9",
    "LPT1",
    "LPT2",
    "LPT3",
    "LPT4",
    "LPT5",
    "LPT6",
    "LPT7",
    "LPT8",
    "LPT9",
}


def get_os_name():
    """Returns the OS Name `Windows`, `Linux` or `MacOS`"""
    if platform == "win32":
        return "Windows"
    elif platform == "darwin":
        return "MacOS"
    else:
        return "Linux"


def get_nonexisting_paths(paths: List[str]) -> List[str]:
    """Returns a list of non-existing paths from `paths` list."""
    return list(filter(lambda p: not exists(p), paths))


def get_existing_paths(paths: List[str]) -> List[str]:
    """Returns a list of existing paths from `paths` list."""
    return list(filter(lambda p: exists(p), paths))


def is_valid_file(filename: str) -> Union[bool, str]:
    """
    ### Is Valid File
    Validates filename. Returns `True` if valid, Returns `str` if invalid.
    This `str` is the cause of filename invalidation.

    #### ARGS:
    - `filename`: name of the file

    ##### This Method:
    - Disallows empty filenames
    - Disallows `.` and `..` as filenames
    - Disallows Windows Reserved Words like `CON`, `AUX` etc.
    - Disallows Special characters like `<:"/\\|?*\\0\\t\\r\\n>`

    This methods is cross-platform. (more or less)
    """
    filename = filename.strip()

    # Disallow empty filenames
    if not filename:
        return "file names cannot be empty or all spaces."

    # Disallow `.` and `..`
    if filename in {".", ".."}:
        return "file names cannot be '.' or '..'"

    # Disallow Trailing dot in Windows
    if platform == "win32" and filename.endswith("."):
        return "file names cannot end with '.' on Windows"

    # Disallow Windows-Reserved names
    if platform == "win32":
        # Extract filename (not extension)
        name_ = filename.rsplit(".", maxsplit=1)[0]
        if name_.upper() in RESERVED_WINDOWS_NAMES:
            return "the name '%s' is reserved on Windows" % name_

    # Validate characters (disallow special chars)
    if not re.match(FILENAME_REGEX, filename.strip()):
        return 'file names cannot contain these characters <:"/\\|?*\\0\\t\\r\\n>'

    # All checks passed
    return True


def is_valid_dir(dirname: str) -> Union[bool, str]:
    """
    ### Is Valid Dir
    Validates directory name. Returns `True` if valid, Returns `str` if invalid.
    This `str` contains the reason for dir being invalid.

    #### ARGS:
    - `dirname`: name of directory
    """
    dirname = dirname.strip()

    # Disallow empty dirname
    if not dirname:
        return "directory names cannot be empty or all spaces."

    # Disallow `.` and `..`
    if dirname in {".", ".."}:
        return "directory names cannot be '.' or '..'"

    # Windows specific checks
    if platform == "win32":
        # Disallow Trailing dot in Windows
        if dirname.endswith("."):
            return "directory names cannot end with '.' on Windows"

        # Disallow Windows-Reserved names
        if dirname.upper() in RESERVED_WINDOWS_NAMES:
            return "the name '%s' is reserved on Windows" % dirname

    # Disallow '/' or '\'
    if contains_chars(dirname, "/\\"):
        return "directory names cannot contain '/' or '\\'"

    # Validate characters (disallow special chars)
    if not re.match(DIRNAME_REGEX, dirname.strip()):
        return 'directory names cannot contain these characters <:"/\\|?*\\0\\t\\r\\n>'

    # All checks passed
    return True


def is_valid_dirpath(dirpath: str):
    """
    ### Is Valid Dirpath
    Validates directory path. Returns `True` if valid, Returns `str` if invalid.
    This `str` contains the reason for path being invalid.

    #### ARGS:
    - `dirpath`: the path to validate
    """
    dirpath = str(dirpath)

    if not dirpath:
        return "path cannot be empty or all spaces."

    if dirpath in {".", ".."}:  # No Further checking needed
        return True

    d = Path(dirpath)
    if d.drive:  # Remove drive letter
        root_parts = d.parts[1:]
    elif platform == "linux" and (d.parts and d.parts[0] == "/"):
        # Remove '/'
        root_parts = d.parts[1:]
    else:
        root_parts = d.parts

    # Disallow dirpath to be more than 255 chars
    if len(dirpath) > 255:  # Maxlength including slashes
        return "path cannot contain more than 255 characters"

    # Windows specific checks
    if platform == "win32":
        # Disallow Windows-Reserved names
        for part in root_parts:
            if part.upper() in RESERVED_WINDOWS_NAMES:
                return "the name '%s' is reserved on Windows" % part

        # Validate characters (disallow special chars)
        root_parts_str = join(*root_parts).strip() if root_parts else ""
        if not re.match(DIRNAME_REGEX, root_parts_str):
            return 'path cannot contain these characters <:"|?*\\0\\t\\r\\n>'

    return True


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


def now(format_: str = "%d %B %Y %I:%M %p") -> str:
    """
    ### Now
    Returns the current local date & time, formatted as `format_`.
    This method is equivalent to `datetime.now().strftime(format_)`

    #### ARGS:
    - `format_`: the format of output datetime string

    #### Format Codes:
    - `%d` day of the month as decimal (e.g. `01, 02, ... 31`)
    - `%j` day of the year as decimal (e.g. `001, 002, ... 366`)
    - `%a` Weekday as locale's abbr. name (e.g. `Sun, Mon, ... Sat`)
    - `%A` Weekday as locale's full name (e.g. `Sunday, Monday, ... Saturday`)
    - `%w` Weekday as decimal (starting from sunday) (e.g. `0, 1, ... 6`)
    - `%U` Week number of the year (Sunday as 1st day of week) (e.g. `00, 01, ... 53`)
    - `%W` Week number of the year (Monday as 1st day of week) (e.g. `00, 01, ... 53`)
    - `%b` Month as locale's abbr. name (e.g. `Jan, Feb, ... `Dec)
    - `%B` Month as locale's full name (e.g. `January, February, ... December`)
    - `%m` month as decimal (e.g. `01, 02, ... 12`)
    - `%Y` year with century (e.g. `2000, 2001, ... 9999`)
    - `%y` year without century (e.g. `00, 01, ... 99`)
    - `%p` Locale's equivalent of either AM or PM (e.g. `AM, PM`)
    - `%H` Hour (24-hour clock) (e.g. `00, 01, ... 23`)
    - `%I` Hour (12-hour clock) (e.g. `01, 02, ... 12`)
    - `%M` Minute (e.g. `00, 01, ... 59`)
    - `%S` Second (e.g. `00, 01, ... 59`)
    - `%f` Microsecond (6-digits) (e.g. `000000, 000001, ... 999999`)

    To learn more about format codes, see  `datetime` module in Python Docs.

    #### Example:
    ```
    >> now(format_="%I:%M %p")
    '01:40 PM'

    >> now(format_="%d %B %Y")
    '25 September 2024'
    ```
    """
    return datetime.now().strftime(format_)
