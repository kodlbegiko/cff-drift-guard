"""Command-line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analyzer import analyze_repository
from .experiment import run_experiment


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cff-drift-guard")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="check one repository directory")
    check.add_argument("path", type=Path)
    check.add_argument("--json-out", type=Path)
    benchmark = sub.add_parser("benchmark", help="run the frozen pilot benchmark")
    benchmark.add_argument("--source", type=Path, default=Path("data/raw/source-records.json"))
    benchmark.add_argument("--output-dir", type=Path, default=Path("results"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "check":
        result = analyze_repository(args.path)
        rendered = json.dumps(result.to_dict(), indent=2, sort_keys=True)
        print(rendered)
        if args.json_out:
            args.json_out.parent.mkdir(parents=True, exist_ok=True)
            args.json_out.write_text(rendered + "\n", encoding="utf-8")
        if result.status in {"MATCH", "NORMALIZED_MATCH"}:
            return 0
        if result.status == "DRIFT":
            return 1
        return 2
    result = run_experiment(args.source, args.output_dir)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["primary_verdict"] != "BLOCKED" else 3
