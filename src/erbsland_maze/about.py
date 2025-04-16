#  Copyright © 2003-2025 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from functools import cache
from pathlib import Path


@cache
def get_version() -> str:
    return Path(__file__).with_name("VERSION.txt").read_text().strip()


@cache
def get_author() -> str:
    return "Tobias Erbsland"


@cache
def get_copyright() -> str:
    return f"2003-2025, Tobias Erbsland"
