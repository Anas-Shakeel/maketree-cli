""" Contains Helper code to keep core logic clean. (things that don't fit anywhere, fit here) """

from os.path import exists
from typing import List


def remove_existing_paths(paths: List[str]) -> List[str]:
    """Remove existing paths from `paths` list and return the list."""
    return list(filter(lambda p: not exists(p), paths))
