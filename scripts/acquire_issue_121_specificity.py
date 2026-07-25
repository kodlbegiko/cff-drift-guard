#!/usr/bin/env python3
"""Acquire a frozen JOSS issue-121 sample and screen CFF version specificity.

The script uses only the Python standard library. It retrieves the frozen sample
frame from a commit in ``research-readme-smoketest`` and then reads root-level
metadata files through the GitHub Contents API. It never clones or executes
third-party code.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import time
import tomllib
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

SOURCE_REPOSITORY = "kodlbegiko/research-readme-smoketest"
SOURCE_REF = "5efa7e6b79dbd10b8e8439ca60bea9e43f27a00f"
SOURCE_PATH = "data/issue-121/raw/repository-metadata.json"
SUPPORTED_MANIFESTS = (
    "pyproject.toml",
    "DESCRIPTION",
    "Cargo.toml",
    "Project.toml",
    "package.json",
    "pubspec.yaml",
)
USER_AGENT = "cff-drift-guard-issue121/0.2"


@dataclass(frozen=True)
class Manifest:
    path: str
    version: str | None
    dynamic: bool = False
    ambiguous: bool = False
    package_name: str | None = None
    blob_sha: str | None = None


@dataclass(frozen=True)
class FilePayload:
    text: str
    sha: str


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _request_json(url: str, token: str | None, retries: int = 3) -> dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    for attempt in range(retries):
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                raise FileNotFoundError(url) from exc
            if exc.code not in {403, 429, 500, 502, 503, 504} or attempt + 1 == retries:
                body = exc.read().decode("utf-8", errors="replace")
                raise RuntimeError(f"GitHub API error {exc.code} for {url}: {body[:500]}") from exc
        except urllib.error.URLError as exc:
            if attempt + 1 == retries:
                raise RuntimeError(f"network error for {url}: {exc}") from exc
        time.sleep(2**attempt)
    raise AssertionError("unreachable")


def fetch_file(repo: str, path: str, ref: str, token: str | None) -> FilePayload | None:
    url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={ref}"
    try:
        payload = _request_json(url, token)
    except FileNotFoundError:
        return None
    if payload.get("type") != "file" or payload.get("encoding") != "base64":
        raise RuntimeError(f"unsupported GitHub contents payload for {repo}:{path}")
    raw = base64.b64decode(payload["content"])
    return FilePayload(raw.decode("utf-8"), str(payload["sha"]))


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_cff_version(text: str) -> str | None:
    for raw in text.splitlines():
        if raw.startswith((" ", "\t", "#")):
            continue
        match = re.match(r"^version\s*:\s*(.*?)\s*(?:#.*)?$", raw)
        if match:
            value = _unquote(match.group(1))
            return value or None
    return None


def parse_cff_schema_version(text: str) -> str | None:
    for raw in text.splitlines():
        if raw.startswith((" ", "\t", "#")):
            continue
        match = re.match(r"^cff-version\s*:\s*(.*?)\s*(?:#.*)?$", raw)
        if match:
            value = _unquote(match.group(1))
            return value or None
    return None


def parse_pyproject(text: str, sha: str) -> Manifest:
    data = tomllib.loads(text)
    project = data.get("project", {})
    dynamic = "version" in project.get("dynamic", []) or "version" in data.get("tool", {}).get(
        "setuptools", {}
    ).get("dynamic", {})
    version = project.get("version")
    return Manifest(
        "pyproject.toml",
        str(version) if version is not None else None,
        dynamic=dynamic,
        package_name=project.get("name"),
        blob_sha=sha,
    )


def parse_description(text: str, sha: str) -> Manifest:
    fields: dict[str, str] = {}
    current: str | None = None
    for raw in text.splitlines():
        if raw.startswith((" ", "\t")) and current:
            fields[current] += " " + raw.strip()
            continue
        match = re.match(r"^([A-Za-z][A-Za-z0-9-]*)\s*:\s*(.*)$", raw)
        if match:
            current = match.group(1)
            fields[current] = match.group(2).strip()
    return Manifest("DESCRIPTION", fields.get("Version"), package_name=fields.get("Package"), blob_sha=sha)


def parse_cargo(text: str, sha: str) -> Manifest:
    data = tomllib.loads(text)
    package = data.get("package")
    if not isinstance(package, dict):
        return Manifest("Cargo.toml", None, ambiguous="workspace" in data, blob_sha=sha)
    version = package.get("version")
    if isinstance(version, dict):
        return Manifest(
            "Cargo.toml", None, dynamic=True, package_name=package.get("name"), blob_sha=sha
        )
    return Manifest(
        "Cargo.toml",
        str(version) if version is not None else None,
        package_name=package.get("name"),
        blob_sha=sha,
    )


def parse_project_toml(text: str, sha: str) -> Manifest:
    data = tomllib.loads(text)
    version = data.get("version")
    return Manifest(
        "Project.toml",
        str(version) if version is not None else None,
        package_name=data.get("name"),
        blob_sha=sha,
    )


def parse_package_json(text: str, sha: str) -> Manifest:
    data = json.loads(text)
    version = data.get("version")
    return Manifest(
        "package.json",
        str(version) if version is not None else None,
        package_name=data.get("name"),
        blob_sha=sha,
    )


def parse_pubspec(text: str, sha: str) -> Manifest:
    fields: dict[str, str] = {}
    workspace = False
    for raw in text.splitlines():
        if raw.startswith((" ", "\t", "#")):
            continue
        if re.match(r"^workspace\s*:", raw):
            workspace = True
        match = re.match(r"^(name|version|publish_to)\s*:\s*(.*?)\s*(?:#.*)?$", raw)
        if match:
            fields[match.group(1)] = _unquote(match.group(2))
    unpublished = fields.get("publish_to", "").lower() == "none"
    return Manifest(
        "pubspec.yaml",
        fields.get("version"),
        ambiguous=workspace and unpublished and "version" not in fields,
        package_name=fields.get("name"),
        blob_sha=sha,
    )


PARSERS: dict[str, Callable[[str, str], Manifest]] = {
    "pyproject.toml": parse_pyproject,
    "DESCRIPTION": parse_description,
    "Cargo.toml": parse_cargo,
    "Project.toml": parse_project_toml,
    "package.json": parse_package_json,
    "pubspec.yaml": parse_pubspec,
}


def exact_version(value: str) -> str:
    return value.strip().lower()


def core_version(value: str) -> str:
    normalized = exact_version(value)
    if normalized.startswith("v") and len(normalized) > 1 and normalized[1].isdigit():
        normalized = normalized[1:]
    normalized = normalized.split("+", 1)[0]
    return normalized


def classify(cff: FilePayload | None, manifests: list[Manifest]) -> dict[str, Any]:
    if cff is None:
        return {
            "status": "CFF_MISSING",
            "specificity_gap": None,
            "cff_version": None,
            "cff_schema_version": None,
            "cff_blob_sha": None,
            "manifest": None,
            "reason": "root CITATION.cff not found",
        }
    cff_version = parse_cff_version(cff.text)
    schema_version = parse_cff_schema_version(cff.text)
    common = {
        "cff_version": cff_version,
        "cff_schema_version": schema_version,
        "cff_blob_sha": cff.sha,
    }
    if cff_version is None:
        return {
            **common,
            "status": "VERSION_MISSING",
            "specificity_gap": True,
            "manifest": asdict(manifests[0]) if len(manifests) == 1 else None,
            "reason": "root CFF omits top-level software version",
        }
    if not manifests:
        return {
            **common,
            "status": "MANIFEST_MISSING",
            "specificity_gap": False,
            "manifest": None,
            "reason": "CFF is version-specific; no supported root manifest for consistency check",
        }
    if len(manifests) > 1:
        return {
            **common,
            "status": "MANIFEST_AMBIGUOUS",
            "specificity_gap": False,
            "manifest": None,
            "manifest_candidates": [asdict(item) for item in manifests],
            "reason": "multiple supported root manifests",
        }
    manifest = manifests[0]
    rendered_manifest = asdict(manifest)
    if manifest.ambiguous:
        status = "SCOPE_AMBIGUOUS"
        reason = "root manifest is a versionless workspace or metapackage"
    elif manifest.dynamic:
        status = "MANIFEST_DYNAMIC"
        reason = "root manifest version is dynamically resolved"
    elif manifest.version is None:
        status = "MANIFEST_VERSION_MISSING"
        reason = "root manifest has no static version"
    else:
        exact = exact_version(cff_version) == exact_version(manifest.version)
        core = core_version(cff_version) == core_version(manifest.version)
        if exact:
            status, reason = "MATCH", "exact versions match"
        elif core:
            status, reason = "NORMALIZED_MATCH", "versions match under conservative normalization"
        else:
            status, reason = "DRIFT", "CFF and root manifest versions differ"
        return {
            **common,
            "status": status,
            "specificity_gap": status == "DRIFT",
            "manifest": rendered_manifest,
            "exact_match": exact,
            "core_match": core,
            "reason": reason,
        }
    return {
        **common,
        "status": status,
        "specificity_gap": False,
        "manifest": rendered_manifest,
        "reason": reason,
    }


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> list[float | None]:
    if total == 0:
        return [None, None]
    p = successes / total
    denominator = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denominator
    margin = z * ((p * (1 - p) / total + z * z / (4 * total * total)) ** 0.5) / denominator
    return [max(0.0, center - margin), min(1.0, center + margin)]


def acquire(token: str | None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    sample_payload = fetch_file(SOURCE_REPOSITORY, SOURCE_PATH, SOURCE_REF, token)
    if sample_payload is None:
        raise RuntimeError("frozen sample source disappeared")
    sample = json.loads(sample_payload.text)
    records: list[dict[str, Any]] = []
    for item in sample:
        base = {
            "order": item["order"],
            "doi": item["doi"],
            "title": item["title"],
            "repository": item["repository"],
            "host": item["host"],
            "default_branch": item.get("default_branch"),
        }
        if item["host"] != "github":
            records.append(
                {
                    **base,
                    "status": "NON_GITHUB",
                    "specificity_gap": None,
                    "reason": "prespecified GitHub-only acquisition scope",
                }
            )
            continue
        repo = item["repository"]
        ref = item["default_branch"]
        cff = fetch_file(repo, "CITATION.cff", ref, token)
        manifests: list[Manifest] = []
        parse_errors: list[dict[str, str]] = []
        for path in SUPPORTED_MANIFESTS:
            payload = fetch_file(repo, path, ref, token)
            if payload is None:
                continue
            try:
                manifests.append(PARSERS[path](payload.text, payload.sha))
            except (json.JSONDecodeError, tomllib.TOMLDecodeError, UnicodeDecodeError, ValueError) as exc:
                parse_errors.append({"path": path, "error": type(exc).__name__})
        classification = classify(cff, manifests)
        records.append({**base, **classification, "manifest_parse_errors": parse_errors})
    metadata = {
        "source_repository": SOURCE_REPOSITORY,
        "source_ref": SOURCE_REF,
        "source_path": SOURCE_PATH,
        "source_blob_sha": sample_payload.sha,
        "source_sha256": sha256_text(sample_payload.text),
    }
    return records, metadata


def summarize(records: list[dict[str, Any]], source: dict[str, Any]) -> dict[str, Any]:
    github = [r for r in records if r["host"] == "github"]
    cff_present = [r for r in github if r["status"] != "CFF_MISSING"]
    gaps = [r for r in cff_present if r.get("specificity_gap") is True]
    comparable = [r for r in cff_present if r["status"] in {"MATCH", "NORMALIZED_MATCH", "DRIFT"}]
    drifts = [r for r in comparable if r["status"] == "DRIFT"]
    status_counts: dict[str, int] = {}
    for record in records:
        status_counts[record["status"]] = status_counts.get(record["status"], 0) + 1
    denominator = len(cff_present)
    gap_rate = len(gaps) / denominator if denominator else None
    return {
        "study_type": "preregistered out-of-sample exploratory validation",
        "research_question": (
            "Among JOSS issue-121 GitHub repositories with a root CITATION.cff, how often does "
            "the file fail version specificity because its top-level software version is missing or "
            "disagrees with a unique static root package manifest?"
        ),
        "source": source,
        "sample_n": len(records),
        "github_n": len(github),
        "cff_present_n": denominator,
        "cff_coverage": denominator / len(github) if github else None,
        "specificity_gap_n": len(gaps),
        "specificity_gap_rate": gap_rate,
        "specificity_gap_wilson_95": wilson_interval(len(gaps), denominator),
        "comparable_n": len(comparable),
        "drift_n": len(drifts),
        "drift_rate_among_comparable": len(drifts) / len(comparable) if comparable else None,
        "status_counts": dict(sorted(status_counts.items())),
        "baseline_all_specific_accuracy": (
            (denominator - len(gaps)) / denominator if denominator else None
        ),
        "stopping_rule": {
            "minimum_cff_present": 10,
            "met": denominator >= 10,
            "manual_adjudication_required_before_final_verdict": True,
        },
        "preliminary_verdict": "INCONCLUSIVE",
        "preliminary_verdict_reason": "manual adjudication and frozen evaluation are pending",
    }


def write_outputs(output_dir: Path, records: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    observed_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    raw = {
        "observed_at": observed_at,
        "records": records,
    }
    (output_dir / "source-records.json").write_text(
        json.dumps(raw, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output_dir / "preliminary-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    deterministic = {"records": records, "summary": summary}
    deterministic_text = json.dumps(deterministic, indent=2, sort_keys=True) + "\n"
    deterministic_path = output_dir / "acquisition-deterministic.json"
    deterministic_path.write_text(deterministic_text, encoding="utf-8")
    manifest = {
        "files": {
            name: hashlib.sha256((output_dir / name).read_bytes()).hexdigest()
            for name in (
                "source-records.json",
                "preliminary-summary.json",
                "acquisition-deterministic.json",
            )
        }
    }
    (output_dir / "SHA256SUMS.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        records, source = acquire(os.environ.get("GITHUB_TOKEN"))
        summary = summarize(records, source)
        write_outputs(args.output_dir, records, summary)
    except Exception as exc:  # deliberate CLI boundary
        print(f"acquisition failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
