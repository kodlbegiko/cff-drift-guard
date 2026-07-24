#!/usr/bin/env python3
"""Fetch supported root metadata files from GitHub's public contents API.

This acquisition helper is intentionally separate from the frozen pilot. It is
not needed to reproduce published metrics because the exact extracted records
and blob SHAs are committed. Set GITHUB_TOKEN to increase rate limits.
"""
from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

FILES = ["CITATION.cff", "pyproject.toml", "DESCRIPTION", "Cargo.toml", "Project.toml", "package.json", "pubspec.yaml"]


def fetch(repo: str, path: str) -> dict[str, object] | None:
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "cff-drift-guard/0.1"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise
    return {"path": path, "sha": payload.get("sha"), "download_url": payload.get("download_url")}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sampling-frame", type=Path, default=Path("data/raw/sampling-frame.json"))
    parser.add_argument("--out", type=Path, default=Path("data/raw/acquisition-index.json"))
    args = parser.parse_args()
    frame = json.loads(args.sampling_frame.read_text(encoding="utf-8"))
    records = []
    for item in frame:
        if item["host"] != "github":
            records.append({"repository": item["repository"], "files": [], "skipped": "non_github"})
            continue
        files = [entry for filename in FILES if (entry := fetch(item["repository"], filename))]
        records.append({"repository": item["repository"], "files": files})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
