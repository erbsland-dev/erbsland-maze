# Copyright (c) 2026 Tobias Erbsland - https://erbsland.dev
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pathlib import Path

from lib.error import UtilityError


def resolve_project_path(project_dir: Path, configured_path: str | Path, label: str) -> Path:
    """
    Resolve a configured project-relative path and ensure it stays below the project root.

    :param project_dir: The project root directory.
    :param configured_path: The path from configuration.
    :param label: The user-facing setting name for error messages.
    :return: The resolved absolute path.
    """
    path = Path(configured_path)
    if not str(configured_path).strip() or path == Path("."):
        raise UtilityError(f"{label} must not be empty.")
    if path.is_absolute():
        raise UtilityError(f"{label} must be relative to the project root: {configured_path}")
    if ".." in path.parts:
        raise UtilityError(f"{label} must not contain '..': {configured_path}")
    project_root = project_dir.resolve()
    result = (project_root / path).resolve(strict=False)
    if result != project_root and not result.is_relative_to(project_root):
        raise UtilityError(f"{label} escapes the project root: {configured_path}")
    return result


def require_directory(path: Path, label: str) -> None:
    """
    Validate that a path is an existing directory and not a symbolic link.

    :param path: The directory path.
    :param label: The user-facing setting name for error messages.
    """
    if path.is_symlink():
        raise UtilityError(f"{label} must not be a symbolic link: {path}")
    if not path.is_dir():
        raise UtilityError(f"{label} does not exist or is not a directory: {path}")


def require_safe_existing_file(path: Path, label: str, max_size_bytes: int | None = None) -> None:
    """
    Validate that an existing path is a regular non-symlink file and optionally below a size limit.

    :param path: The file path.
    :param label: The user-facing setting name for error messages.
    :param max_size_bytes: Optional maximum file size.
    """
    if path.is_symlink():
        raise UtilityError(f"{label} must not be a symbolic link: {path}")
    if not path.exists():
        return
    if not path.is_file():
        raise UtilityError(f"{label} must be a regular file: {path}")
    if max_size_bytes is not None and path.stat().st_size > max_size_bytes:
        max_size_mb = max_size_bytes // (1024 * 1024)
        raise UtilityError(f"{label} is larger than {max_size_mb} MiB: {path}")


def read_safe_bytes(path: Path, label: str = "File", max_size_bytes: int | None = 32 * 1024 * 1024) -> bytes:
    """
    Read bytes from a regular non-symlink file after safety checks.

    :param path: The file path.
    :param label: The user-facing setting name for error messages.
    :param max_size_bytes: Optional maximum file size.
    :return: The file content.
    """
    require_safe_existing_file(path, label, max_size_bytes)
    if not path.exists():
        raise UtilityError(f"{label} does not exist: {path}")
    return path.read_bytes()


def read_safe_text(
    path: Path, label: str = "File", max_size_bytes: int | None = 32 * 1024 * 1024, encoding: str = "utf-8"
) -> str:
    """
    Read text from a regular non-symlink file after safety checks.

    :param path: The file path.
    :param label: The user-facing setting name for error messages.
    :param max_size_bytes: Optional maximum file size.
    :param encoding: The expected text encoding.
    :return: The decoded file content.
    """
    data = read_safe_bytes(path, label, max_size_bytes)
    try:
        return data.decode(encoding)
    except UnicodeDecodeError:
        raise UtilityError(f"{label} is not valid {encoding}: {path}") from None


def require_safe_parent_directory(path: Path, label: str) -> None:
    """
    Validate that existing parent directories are directories and not symbolic links.

    :param path: The target path.
    :param label: The user-facing setting name for error messages.
    """
    for parent in [path.parent, *path.parent.parents]:
        if not parent.exists():
            continue
        if parent.is_symlink():
            raise UtilityError(f"{label} parent directory must not be a symbolic link: {parent}")
        if not parent.is_dir():
            raise UtilityError(f"{label} parent path is not a directory: {parent}")
