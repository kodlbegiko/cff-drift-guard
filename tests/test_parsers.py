from pathlib import Path
from cff_drift_guard.parsers import (
    discover_manifests, parse_cff_version, parse_description, parse_package_json,
    parse_project_toml, parse_pubspec, parse_pyproject, parse_cargo,
)

FIX = Path(__file__).parent / "fixtures"

def test_cff_top_level_only():
    assert parse_cff_version(FIX / "cff_version_missing" / "CITATION.cff") is None

def test_cff_quoted():
    assert parse_cff_version(FIX / "match" / "CITATION.cff") == "1.2.3"

def test_pyproject_static():
    value = parse_pyproject(FIX / "match" / "pyproject.toml")
    assert value.version == "1.2.3" and not value.dynamic and value.package_name == "example"

def test_pyproject_dynamic():
    value = parse_pyproject(FIX / "dynamic_pyproject" / "pyproject.toml")
    assert value.version is None and value.dynamic

def test_cargo_workspace():
    value = parse_cargo(FIX / "workspace_cargo" / "Cargo.toml")
    assert value.version is None and value.ambiguous

def test_description():
    value = parse_description(FIX / "description" / "DESCRIPTION")
    assert value.version == "2.1.0" and value.package_name == "demoR"

def test_project_toml():
    value = parse_project_toml(FIX / "julia" / "Project.toml")
    assert value.version == "0.4.0" and value.package_name == "Demo"

def test_package_json():
    value = parse_package_json(FIX / "node" / "package.json")
    assert value.version == "3.2.1" and value.package_name == "demo"

def test_pubspec_workspace():
    value = parse_pubspec(FIX / "dart" / "pubspec.yaml")
    assert value.version is None and value.ambiguous

def test_discover_priority_independent_count():
    assert len(discover_manifests(FIX / "ambiguous_manifests")) == 2
