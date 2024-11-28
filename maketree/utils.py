""" Contains Helper code to keep core logic clean. (things that don't fit anywhere, fit here) """

from os.path import exists
from typing import List


def get_nonexisting_paths(paths: List[str]) -> List[str]:
    """Returns a list of non-existing paths from `paths` list."""
    return list(filter(lambda p: not exists(p), paths))
