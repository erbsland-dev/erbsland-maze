# Copyright (c) 2026 Tobias Erbsland - https://erbsland.dev
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from lib.config import project_relative_posix, read_elcl_file
from lib.error import UtilityError
from lib.file_update import FileUpdate
from lib.path_safety import read_safe_text, require_directory, resolve_project_path
from lib.safe_tool import (
    SafeExecutable,
    find_safe_executable,
    safe_subprocess_environment,
)
from lib.utility import UtilityApp


@dataclass(frozen=True, order=True)
class StableVersion:
    """A stable semver tag."""

    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, text: str) -> "StableVersion | None":
        match = re.fullmatch(r"v(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)", text)
        if match is None:
            return None
        return cls(
            int(match.group("major")),
            int(match.group("minor")),
            int(match.group("patch")),
        )

    def __str__(self) -> str:
        return f"v{self.major}.{self.minor}.{self.patch}"


@dataclass(frozen=True)
class TagInfo:
    """A stable tag and its commit SHA."""

    version: StableVersion
    sha: str


@dataclass(frozen=True)
class ActionReference:
    """A parsed action reference in a workflow file."""

    workflow_path: Path
    line_index: int
    indent: str
    uses_prefix: str
    action: str
    repo: str
    ref: str

    @property
    def owner_repo(self) -> str:
        return "/".join(self.repo.split("/")[:2])


@dataclass(frozen=True)
class UpdateRequest:
    """A requested action update."""

    action: str
    version: str


@dataclass(frozen=True)
class ActionStatus:
    """Status for one used workflow action."""

    action: str
    status: str
    workflow: str


@dataclass(frozen=True)
class GitHubWorkflowsConfig:
    """Configuration for the GitHub workflow security utility."""

    project_dir: Path
    workflow_directory: Path
    safe_binary_directories: tuple[Path, ...]

    @classmethod
    def read(cls, project_dir: Path, config_file: Path) -> "GitHubWorkflowsConfig":
        """Read the configuration."""
        project_dir = project_dir.resolve()
        main_config = read_elcl_file(config_file)["main"]
        result = cls(
            project_dir=project_dir,
            workflow_directory=resolve_project_path(
                project_dir,
                main_config.get_text("workflow_directory"),
                "Workflow Directory",
            ),
            safe_binary_directories=tuple(
                Path(directory).resolve()
                for directory in main_config.get_list("safe_binary_directories", str, default=[])
            ),
        )
        result.validate()
        return result

    def validate(self) -> None:
        """Validate the configuration."""
        require_directory(self.workflow_directory, "Workflow Directory")
        if not self.safe_binary_directories:
            raise UtilityError("No safe binary directories configured.")
        for directory in self.safe_binary_directories:
            if not directory.is_absolute():
                raise UtilityError(f"Safe binary directory must be absolute: {directory}")

    def display_path(self, path: Path) -> str:
        """Create a stable project-relative display path."""
        return project_relative_posix(self.project_dir, path)


class GitTagCache:
    """Cache action tag lookups through safe git."""

    def __init__(self, git: SafeExecutable) -> None:
        self.git = git
        self.tags_by_repo: dict[str, dict[str, TagInfo]] = {}

    def tags_for_repo(self, owner_repo: str) -> dict[str, TagInfo]:
        """Load stable tags for a GitHub action repository."""
        if owner_repo in self.tags_by_repo:
            return self.tags_by_repo[owner_repo]
        if self.git.resolved_path is None:
            raise UtilityError("Safe git executable is not available.")
        url = f"https://github.com/{owner_repo}.git"
        try:
            result = subprocess.run(
                [str(self.git.resolved_path), "ls-remote", "--tags", url],
                check=True,
                capture_output=True,
                text=True,
                env=safe_subprocess_environment(),
            )
        except subprocess.CalledProcessError as error:
            raise UtilityError(f"Could not read tags for {owner_repo}.") from error
        tags: dict[str, TagInfo] = {}
        pending_tag_objects: dict[str, str] = {}
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            sha, ref = line.split(maxsplit=1)
            peeled = ref.endswith("^{}")
            tag_name = ref.removeprefix("refs/tags/")
            if peeled:
                tag_name = tag_name[:-3]
            version = StableVersion.parse(tag_name)
            if version is None:
                continue
            if peeled:
                tags[tag_name] = TagInfo(version, sha)
            else:
                pending_tag_objects[tag_name] = sha
        for tag_name, sha in pending_tag_objects.items():
            if tag_name not in tags:
                version = StableVersion.parse(tag_name)
                if version is not None:
                    tags[tag_name] = TagInfo(version, sha)
        self.tags_by_repo[owner_repo] = tags
        return tags

    def tag_for_sha(self, owner_repo: str, sha: str) -> TagInfo | None:
        """Find the highest stable tag for a commit SHA."""
        matches = [tag for tag in self.tags_for_repo(owner_repo).values() if tag.sha == sha]
        if not matches:
            return None
        return max(matches, key=lambda tag: tag.version)

    def latest_tag(self, owner_repo: str) -> TagInfo | None:
        """Find the latest stable tag for a repository."""
        tags = list(self.tags_for_repo(owner_repo).values())
        if not tags:
            return None
        return max(tags, key=lambda tag: tag.version)

    def tag_named(self, owner_repo: str, version: str) -> TagInfo | None:
        """Find a stable tag by name."""
        return self.tags_for_repo(owner_repo).get(version)


class WorkflowFile:
    """One workflow file parsed line-by-line."""

    RE_USES_LINE = re.compile(
        r"^(?P<indent>\s*)(?P<prefix>(?:-\s*)?uses:\s*)(?P<quote>['\"]?)(?P<value>[^'\"\s#]+)(?P=quote)(?P<suffix>.*)$"
    )
    RE_ANNOTATION = re.compile(
        r"^(?P<indent>\s*)#\s+(?P<action>[\w.-]+/[\w.-]+(?:/[\w./-]+)?)@(?P<version>v\d+\.\d+\.\d+)\s*$"
    )
    RE_SHA = re.compile(r"[0-9a-fA-F]{40}")

    def __init__(self, path: Path, config: GitHubWorkflowsConfig) -> None:
        self.path = path
        self.config = config
        self.original_text = read_safe_text(path, "Workflow file", FileUpdate.MAX_COMPARE_FILE_SIZE)
        self.lines = self.original_text.splitlines()
        self.trailing_newline = self.original_text.endswith("\n")

    def references(self) -> list[ActionReference]:
        """Collect external action references."""
        references = []
        for index, line in enumerate(self.lines):
            match = self.RE_USES_LINE.match(line)
            if match is None:
                continue
            value = match.group("value")
            if value.startswith("./") or "://" in value:
                continue
            if "@" not in value:
                references.append(
                    ActionReference(
                        self.path,
                        index,
                        match.group("indent"),
                        match.group("prefix"),
                        value,
                        value,
                        "",
                    )
                )
                continue
            action, ref = value.rsplit("@", 1)
            parts = action.split("/")
            if len(parts) < 2:
                continue
            repo = "/".join(parts[:2])
            references.append(
                ActionReference(
                    self.path,
                    index,
                    match.group("indent"),
                    match.group("prefix"),
                    action,
                    repo,
                    ref,
                )
            )
        return references

    def annotation_index_for(self, reference: ActionReference) -> int | None:
        """Find the annotation line immediately before a reference."""
        index = reference.line_index - 1
        if index < 0:
            return None
        match = self.RE_ANNOTATION.match(self.lines[index])
        if match is None or match.group("indent") != reference.indent:
            return None
        return index

    def set_annotation(self, reference: ActionReference, version: str) -> None:
        """Create or update the annotation for a reference."""
        annotation = f"{reference.indent}# {reference.action}@{version}"
        index = self.annotation_index_for(reference)
        if index is None:
            self.lines.insert(reference.line_index, annotation)
            return
        self.lines[index] = annotation

    def set_reference(self, reference: ActionReference, sha: str) -> None:
        """Update the SHA for a reference line."""
        match = self.RE_USES_LINE.match(self.lines[reference.line_index])
        if match is None:
            raise UtilityError(f"Could not update workflow line: {self.path}:{reference.line_index + 1}")
        quote = match.group("quote")
        self.lines[reference.line_index] = (
            f"{match.group('indent')}{match.group('prefix')}{quote}{reference.action}@{sha}{quote}{match.group('suffix')}"
        )

    def text(self) -> str:
        """Render this workflow."""
        text = "\n".join(self.lines)
        if self.trailing_newline:
            text += "\n"
        return text

    def write_if_changed(self, file_update: FileUpdate) -> None:
        """Write this workflow when changed."""
        file_update.write_if_changed(self.path, self.text())


class GitHubWorkflowsApp(UtilityApp):
    """Audit GitHub workflow action pins and annotations."""

    description = "Audit GitHub workflow action pins and version annotations."

    def __init__(self) -> None:
        super().__init__()
        self.project_dir = Path()
        self.config: GitHubWorkflowsConfig | None = None
        self.update_requests: list[UpdateRequest] = []
        self.file_update = FileUpdate(self.print_verbose)

    def add_command_line_args(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--update",
            action="append",
            default=[],
            metavar="ACTION@VERSION",
            help="Update a pinned action to `latest` or an explicit stable tag.",
        )

    def handle_command_line_args(self, args: argparse.Namespace) -> None:
        self.project_dir = self.project_directory
        self.update_requests = [self.parse_update_request(value) for value in args.update]

    @staticmethod
    def parse_update_request(value: str) -> UpdateRequest:
        """Parse one update request."""
        if "@" not in value:
            raise UtilityError(f"Invalid update request: {value}")
        action, version = value.rsplit("@", 1)
        if len(action.split("/")) < 2:
            raise UtilityError(f"Invalid update action: {action}")
        if version != "latest" and StableVersion.parse(version) is None:
            raise UtilityError(f"Invalid update version: {version}")
        return UpdateRequest(action, version)

    def read_config(self) -> GitHubWorkflowsConfig:
        """Read the configuration."""
        return GitHubWorkflowsConfig.read(self.project_dir, self.config_file_path())

    def find_workflow_files(self) -> list[Path]:
        """Find workflow files."""
        if self.config is None:
            raise UtilityError("Missing configuration.")
        return sorted(
            [
                path
                for path in self.config.workflow_directory.iterdir()
                if path.is_file() and path.suffix.lower() in {".yml", ".yaml"}
            ],
            key=lambda path: path.as_posix(),
        )

    def find_tool(self, name: str) -> SafeExecutable:
        """Find a safe external tool."""
        if self.config is None:
            raise UtilityError("Missing configuration.")
        tool = find_safe_executable(name, self.config.safe_binary_directories)
        if tool.warning:
            print(f"warning: {tool.warning}")
        return tool

    def run_zizmor(self, zizmor: SafeExecutable) -> None:
        """Run zizmor when safely available."""
        if self.config is None or zizmor.resolved_path is None:
            return
        print("Running zizmor...", flush=True)
        result = subprocess.run(
            [
                str(zizmor.resolved_path),
                "--offline",
                "--collect=workflows",
                str(self.config.workflow_directory),
            ],
            check=False,
            env=safe_subprocess_environment(),
        )
        if result.returncode in {0, 11, 12, 13, 14}:
            return
        raise UtilityError(f"zizmor failed with exit code {result.returncode}.")

    def action_matches_update(self, action: str, request: UpdateRequest) -> bool:
        """Test if an action matches an update request."""
        return action == request.action

    def requested_update_for(self, action: str) -> UpdateRequest | None:
        """Find an update request for one action."""
        matches = [request for request in self.update_requests if self.action_matches_update(action, request)]
        if not matches:
            return None
        return matches[-1]

    def update_reference(self, workflow: WorkflowFile, reference: ActionReference, tags: GitTagCache) -> TagInfo | None:
        """Apply an explicit update request to one reference."""
        request = self.requested_update_for(reference.action)
        if request is None:
            return None
        tag = (
            tags.latest_tag(reference.owner_repo)
            if request.version == "latest"
            else tags.tag_named(reference.owner_repo, request.version)
        )
        if tag is None:
            raise UtilityError(f"Could not find requested version for {request.action}@{request.version}.")
        workflow.set_reference(reference, tag.sha)
        workflow.set_annotation(reference, str(tag.version))
        print(f"Updated {reference.action} to {tag.version}.")
        return tag

    def process_reference(
        self,
        workflow: WorkflowFile,
        reference: ActionReference,
        tags: GitTagCache | None,
        violations: list[str],
    ) -> ActionStatus | None:
        """Validate, annotate and optionally update one reference."""
        if not WorkflowFile.RE_SHA.fullmatch(reference.ref):
            violations.append(
                f"{workflow.config.display_path(workflow.path)}:{reference.line_index + 1}: {reference.action} is not pinned to a SHA."
            )
            return None
        workflow_name = workflow.path.stem
        if tags is None:
            return ActionStatus(f"{reference.action}@{reference.ref[:12]}", "not checked", workflow_name)
        tag = self.update_reference(workflow, reference, tags)
        if tag is None:
            tag = tags.tag_for_sha(reference.owner_repo, reference.ref)
        if tag is None:
            print(f"warning: Could not map {reference.action}@{reference.ref} to a stable version tag.")
            return ActionStatus(f"{reference.action}@{reference.ref[:12]}", "unknown", workflow_name)
        workflow.set_annotation(reference, str(tag.version))
        latest = tags.latest_tag(reference.owner_repo)
        if latest is not None and latest.version > tag.version:
            return ActionStatus(
                f"{reference.action}@{tag.version}",
                f"latest {latest.version}",
                workflow_name,
            )
        return ActionStatus(f"{reference.action}@{tag.version}", "up-to-date", workflow_name)

    @staticmethod
    def print_status_report(action_statuses: list[ActionStatus]) -> None:
        """Print a compact status report for used actions."""
        if not action_statuses:
            return
        grouped: dict[tuple[str, str], set[str]] = {}
        for status in action_statuses:
            grouped.setdefault((status.action, status.status), set()).add(status.workflow)
        rows = [(action, status, ", ".join(sorted(workflows))) for (action, status), workflows in grouped.items()]
        rows.sort(key=lambda row: row[0].casefold())
        action_width = max(len("Action"), *(len(row[0]) for row in rows))
        status_width = max(len("Version"), *(len(row[1]) for row in rows))
        usage_width = max(len("Usage"), *(len(row[2]) for row in rows))
        line_width = action_width + status_width + usage_width + 4
        print()
        print(f"== Used actions {'=' * max(0, line_width - 16)}")
        print(f"{'Action':<{action_width}}  {'Version':<{status_width}}  {'Usage':<{usage_width}}")
        for action, status, usage in rows:
            print(f"{action:<{action_width}}  {status:<{status_width}}  {usage:<{usage_width}}")

    def process_workflows(self, git: SafeExecutable) -> None:
        """Process all workflow files."""
        if self.config is None:
            raise UtilityError("Missing configuration.")
        workflows = [WorkflowFile(path, self.config) for path in self.find_workflow_files()]
        tags = GitTagCache(git) if git.is_safe else None
        violations: list[str] = []
        action_statuses: list[ActionStatus] = []
        for workflow in workflows:
            references = sorted(
                workflow.references(),
                key=lambda reference: reference.line_index,
                reverse=True,
            )
            for reference in references:
                status = self.process_reference(workflow, reference, tags, violations)
                if status is not None:
                    action_statuses.append(status)
            workflow.write_if_changed(self.file_update)
        self.print_status_report(action_statuses)
        if violations:
            raise UtilityError("Workflow pin violations:\n" + "\n".join(violations))

    def run(self, argv=None) -> None:
        """Run this script."""
        super().run(argv)
        self.config = self.read_config()
        zizmor = self.find_tool("zizmor")
        if zizmor.is_safe:
            self.run_zizmor(zizmor)
        git = self.find_tool("git")
        if not git.is_safe:
            print("warning: Skipping annotation repair, latest checks and updates because safe git is unavailable.")
        self.process_workflows(git)


def main():
    """Main entry point."""
    raise SystemExit(GitHubWorkflowsApp().main())


if __name__ == "__main__":
    main()
