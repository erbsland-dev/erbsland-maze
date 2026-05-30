# Copyright (c) 2026 Tobias Erbsland - https://erbsland.dev
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path

from lib.config import (
    project_relative_posix,
    read_elcl_file,
    validate_file_suffixes,
    validate_local_names,
)
from lib.error import UtilityError
from lib.file_update import FileUpdate
from lib.path_safety import (
    read_safe_bytes,
    read_safe_text,
    require_directory,
    resolve_project_path,
)
from lib.utility import UtilityApp


@dataclass(frozen=True)
class SecurityHashesConfig:
    """Configuration for the security hash manifest."""

    project_dir: Path
    output_file: Path
    directories: tuple[Path, ...]
    files: tuple[Path, ...]
    excluded_directory_names: frozenset[str]
    excluded_file_names: frozenset[str]
    excluded_file_suffixes: frozenset[str]

    @classmethod
    def read(cls, project_dir: Path, config_file: Path) -> "SecurityHashesConfig":
        """Read the security hash configuration."""
        project_dir = project_dir.resolve()
        main_config = read_elcl_file(config_file)["main"]
        result = cls(
            project_dir=project_dir,
            output_file=resolve_project_path(project_dir, main_config.get_text("output_file"), "Output File"),
            directories=tuple(
                resolve_project_path(project_dir, directory, "Directories")
                for directory in main_config.get_list("directories", str, default=[])
            ),
            files=tuple(
                resolve_project_path(project_dir, file, "Files")
                for file in main_config.get_list("files", str, default=[])
            ),
            excluded_directory_names=frozenset(main_config.get_list("excluded_directory_names", str, default=[])),
            excluded_file_names=frozenset(main_config.get_list("excluded_file_names", str, default=[])),
            excluded_file_suffixes=frozenset(main_config.get_list("excluded_file_suffixes", str, default=[])),
        )
        result.validate()
        return result

    def validate(self) -> None:
        """Validate configured paths and exclusion rules."""
        for directory in self.directories:
            require_directory(directory, "Directories")
        for file in self.files:
            if not file.is_file() or file.is_symlink():
                raise UtilityError(f"Configured file must be a regular non-symlink file: {file}")
        validate_local_names(self.excluded_directory_names, "Excluded Directory Names")
        validate_local_names(self.excluded_file_names, "Excluded File Names")
        validate_file_suffixes(self.excluded_file_suffixes, "Excluded File Suffixes")

    def display_path(self, path: Path, *, is_directory: bool = False) -> str:
        """Create a stable POSIX project-relative path."""
        return project_relative_posix(self.project_dir, path, is_directory=is_directory)

    def should_skip_directory(self, path: Path) -> bool:
        """Test if a directory should be skipped."""
        return path.name in self.excluded_directory_names

    def should_skip_file(self, path: Path) -> bool:
        """Test if a file should be skipped."""
        if path == self.output_file:
            return True
        return path.name in self.excluded_file_names or path.suffix in self.excluded_file_suffixes


@dataclass(frozen=True)
class HashRecord:
    """One manifest hash record."""

    path: str
    digest: str


class SecurityHashesApp(UtilityApp):
    """Generate or verify the security hash manifest."""

    description = "Generate or verify security hashes for infrastructure files."

    def __init__(self) -> None:
        super().__init__()
        self.project_dir = Path()
        self.verify = False
        self.config: SecurityHashesConfig | None = None
        self.file_update = FileUpdate(self.print_verbose)

    def add_command_line_args(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--verify",
            action="store_true",
            help="Verify the manifest instead of writing it.",
        )

    def handle_command_line_args(self, args: argparse.Namespace) -> None:
        self.project_dir = self.project_directory
        self.verify = args.verify

    def read_config(self) -> SecurityHashesConfig:
        """Read the security hash configuration."""
        self.print_verbose("Reading the configuration")
        return SecurityHashesConfig.read(self.project_dir, self.config_file_path())

    @staticmethod
    def hash_text_or_bytes(data: bytes) -> bytes:
        """Normalize text line endings before hashing, otherwise hash raw bytes."""
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            return data
        return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")

    def hash_file_content(self, path: Path) -> bytes:
        """Read and normalize file content before hashing."""
        data = read_safe_bytes(path, "Security hash input file", FileUpdate.MAX_COMPARE_FILE_SIZE)
        return self.hash_text_or_bytes(data)

    def hash_single_file(self, path: Path, manifest_path: str | None = None) -> str:
        """Hash one file name and its content."""
        if self.config is None:
            raise UtilityError("Missing configuration.")
        if manifest_path is None:
            manifest_path = self.config.display_path(path)
        digest = hashlib.sha256()
        digest.update(b"file\0")
        digest.update(manifest_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(self.hash_file_content(path))
        return digest.hexdigest()

    def direct_files_for_directory(self, directory: Path) -> list[Path]:
        """Collect direct files for one directory hash."""
        if self.config is None:
            raise UtilityError("Missing configuration.")
        result = []
        for path in directory.iterdir():
            if path.is_symlink():
                raise UtilityError(f"Security hash input must not be a symbolic link: {path}")
            if path.is_dir():
                continue
            if self.config.should_skip_file(path):
                continue
            if not path.is_file():
                raise UtilityError(f"Security hash input must be a regular file: {path}")
            result.append(path)
        return sorted(result, key=lambda path: path.name)

    def hash_directory(self, directory: Path) -> str:
        """Hash the direct files in one directory."""
        digest = hashlib.sha256()
        digest.update(b"directory\0")
        for path in self.direct_files_for_directory(directory):
            digest.update(path.name.encode("utf-8"))
            digest.update(b"\0")
            digest.update(self.hash_file_content(path))
            digest.update(b"\0")
        return digest.hexdigest()

    def collect_directories(self) -> list[Path]:
        """Collect all directories to include in the manifest."""
        if self.config is None:
            raise UtilityError("Missing configuration.")
        result: set[Path] = set()
        pending = list(self.config.directories)
        while pending:
            directory = pending.pop()
            if directory.is_symlink():
                raise UtilityError(f"Security hash input must not be a symbolic link: {directory}")
            if self.config.should_skip_directory(directory):
                continue
            require_directory(directory, "Security hash directory")
            result.add(directory)
            for child in directory.iterdir():
                if child.is_symlink():
                    raise UtilityError(f"Security hash input must not be a symbolic link: {child}")
                if child.is_dir() and not self.config.should_skip_directory(child):
                    pending.append(child)
        return sorted(result, key=lambda path: self.config.display_path(path, is_directory=True))

    def create_records(self) -> list[HashRecord]:
        """Create all manifest records except the total hash."""
        if self.config is None:
            raise UtilityError("Missing configuration.")
        records = [
            HashRecord(
                self.config.display_path(directory, is_directory=True),
                self.hash_directory(directory),
            )
            for directory in self.collect_directories()
        ]
        for file in self.config.files:
            if file.is_symlink():
                raise UtilityError(f"Security hash input must not be a symbolic link: {file}")
            if self.config.should_skip_file(file):
                continue
            records.append(HashRecord(self.config.display_path(file), self.hash_single_file(file)))
        return sorted(records, key=lambda record: record.path)

    @staticmethod
    def total_hash(records: list[HashRecord]) -> str:
        """Create the total hash for all emitted records."""
        digest = hashlib.sha256()
        digest.update(b"security-hashes-v1\0")
        for record in records:
            digest.update(record.path.encode("utf-8"))
            digest.update(b"\0")
            digest.update(record.digest.encode("ascii"))
            digest.update(b"\0")
        return digest.hexdigest()

    def create_manifest(self) -> str:
        """Create the full manifest text."""
        records = self.create_records()
        lines = [
            "# Generated by utilities/dev/security_hashes.py",
            "# Do not edit manually.",
            "",
            f"* {self.total_hash(records)}",
        ]
        lines.extend(f"{record.path} {record.digest}" for record in records)
        return "\n".join(lines) + "\n"

    def verify_manifest(self, manifest: str) -> None:
        """Verify the existing manifest."""
        if self.config is None:
            raise UtilityError("Missing configuration.")
        existing = read_safe_text(
            self.config.output_file,
            "Security hash manifest",
            FileUpdate.MAX_COMPARE_FILE_SIZE,
        )
        if existing != manifest:
            raise UtilityError(f"Security hash manifest is not up to date: {self.config.output_file}")

    def run(self, argv=None) -> None:
        """Run this script."""
        super().run(argv)
        self.config = self.read_config()
        manifest = self.create_manifest()
        if self.verify:
            self.verify_manifest(manifest)
            return
        self.file_update.write_if_changed(self.config.output_file, manifest)


def main():
    """Main entry point."""
    raise SystemExit(SecurityHashesApp().main())


if __name__ == "__main__":
    main()
