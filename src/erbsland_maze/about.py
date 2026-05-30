#  Copyright © 2003-2026 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from functools import cache
from importlib.metadata import PackageNotFoundError, version


@cache
def get_version() -> str:
    try:
        from ._version import __version__

        return __version__
    except ModuleNotFoundError:
        pass
    try:
        return version("erbsland-maze")
    except PackageNotFoundError:
        return "0+unknown"


@cache
def get_author() -> str:
    return "Tobias Erbsland"


@cache
def get_copyright() -> str:
    return "2003-2026, Tobias Erbsland - https://erbsland.dev/"
