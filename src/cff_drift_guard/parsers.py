"""Deterministic, dependency-free metadata parsers."""

from __future__ import annotations

import json
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ManifestVersion:
    path: str
    version: str | None
    dynamic: bool = False
    ambiguous: bool = False
    package_name: str | None = None


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_cff_version(path: Path) -> str | None:
    """Extract only a top-level CFF software version.

    This intentionally ignores nested ``preferred-citation.version`` fields.
    """
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.startswith((" ", "\t", "#")):
            continue
        match = re.match(r"^version\s*:\s*(.*?)\s*(?:#.*)?$", raw)
        if match:
            value = _unquote(match.group(1))
            return value or None
    return None


def _toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def parse_pyproject(path: Path) -> ManifestVersion:
    data = _toml(path)
    project = data.get("project", {})
    dynamic = "version" in project.get("dynamic", []) or "version" in data.get("tool", {}).get(
        "setuptools", {}
    ).get("dynamic", {})
    version = project.get("version")
    return ManifestVersion(
        path.name,
        str(version) if version is not None else None,
        dynamic=dynamic,
        package_name=project.get("name"),
    )


def parse_cargo(path: Path) -> ManifestVersion:
    data = _toml(path)
    package = data.get("package")
    if not isinstance(package, dict):
        return ManifestVersion(path.name, None, ambiguous="workspace" in data)
    version = package.get("version")
    if isinstance(version, dict):
        return ManifestVersion(path.name, None, dynamic=True, package_name=package.get("name"))
    return ManifestVersion(
        path.name, str(version) if version is not None else None, package_name=package.get("name")
    )


def parse_project_toml(path: Path) -> ManifestVersion:
    data = _toml(path)
    version = data.get("version")
    return ManifestVersion(
        path.name, str(version) if version is not None else None, package_name=data.get("name")
    )


def parse_package_json(path: Path) -> ManifestVersion:
    data = json.loads(path.read_text(encoding="utf-8"))
    version = data.get("version")
    return ManifestVersion(
        path.name, str(version) if version is not None else None, package_name=data.get("name")
    )


def parse_pubspec(path: Path) -> ManifestVersion:
    fields: dict[str, str] = {}
    workspace = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.startswith((" ", "\t", "#")):
            continue
        if re.match(r"^workspace\s*:", raw):
            workspace = True
        match = re.match(r"^(name|version|publish_to)\s*:\s*(.*?)\s*(?:#.*)?$", raw)
        if match:
            fields[match.group(1)] = _unquote(match.group(2))
    unpublished = fields.get("publish_to", "").lower() == "none"
    ambiguous = workspace and unpublished and "version" not in fields
    return ManifestVersion(
        path.name, fields.get("version"), ambiguous=ambiguous, package_name=fields.get("name")
    )


def parse_description(path: Path) -> ManifestVersion:
    fields: dict[str, str] = {}
    current: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.startswith((" ", "\t")) and current:
            fields[current] += " " + raw.strip()
            continue
        match = re.match(r"^([A-Za-z][A-Za-z0-9-]*)\s*:\s*(.*)$", raw)
        if match:
            current = match.group(1)
            fields[current] = match.group(2).strip()
    return ManifestVersion(path.name, fields.get("Version"), package_name=fields.get("Package"))


PARSERS = {
    "pyproject.toml": parse_pyproject,
    "DESCRIPTION": parse_description,
    "Cargo.toml": parse_cargo,
    "Project.toml": parse_project_toml,
    "package.json": parse_package_json,
    "pubspec.yaml": parse_pubspec,
}


def discover_manifests(root: Path) -> list[ManifestVersion]:
    found: list[ManifestVersion] = []
    for filename, parser in PARSERS.items():
        candidate = root / filename
        if candidate.is_file():
            found.append(parser(candidate))
    return found
