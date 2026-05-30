# Copyright (c) 2026 Tobias Erbsland - https://erbsland.dev
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any

from lib.error import UtilityError


def read_elcl_file(config_file: Path) -> Any:
    """Read an ELCL configuration file."""
    try:
        from erbsland.conf import Parser
    except ImportError:
        raise UtilityError("Please install the 'erbsland-conf' package.") from None
    if not config_file.is_file():
        raise UtilityError(f"Could not find configuration: {config_file}")
    return Parser().parse(config_file)


def validate_local_names(names: Iterable[str], label: str) -> None:
    """Validate configured directory or file names without path components."""
    for name in names:
        if Path(name).name != name or name in {".", ".."}:
            raise UtilityError(f"Invalid entry in {label}: {name}")


def validate_file_suffixes(suffixes: Iterable[str], label: str) -> None:
    """Validate configured file suffixes."""
    for suffix in suffixes:
        if not suffix.startswith(".") or "/" in suffix or "\\" in suffix or suffix in {".", ".."}:
            raise UtilityError(f"Invalid entry in {label}: {suffix}")


def validate_source_relative_path(path_text: str, label: str) -> None:
    """Validate a clean source-relative configuration path."""
    if not path_text:
        return
    path = Path(path_text)
    if path == Path(".") or path.is_absolute() or ".." in path.parts or any(part == "." for part in path.parts):
        raise UtilityError(f"{label} must be a clean relative path: {path_text}")


def project_relative_posix(project_dir: Path, path: Path, *, is_directory: bool = False) -> str:
    """Create a stable POSIX path relative to the project directory."""
    result = path.relative_to(project_dir).as_posix()
    if is_directory:
        result += "/"
    return result
