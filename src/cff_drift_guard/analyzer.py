"""Repository-level consistency analysis."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from .parsers import ManifestVersion, discover_manifests, parse_cff_version
from .versions import core_version, exact_version


@dataclass(frozen=True)
class Analysis:
    root: str
    status: str
    actionable: bool
    cff_version: str | None
    manifest_path: str | None
    manifest_version: str | None
    exact_match: bool | None
    core_match: bool | None
    reason: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _result(
    root: Path,
    status: str,
    reason: str,
    *,
    cff_version: str | None = None,
    manifest: ManifestVersion | None = None,
    actionable: bool = False,
) -> Analysis:
    manifest_version = manifest.version if manifest else None
    exact_match = None
    core_match = None
    if cff_version is not None and manifest_version is not None:
        exact_match = exact_version(cff_version) == exact_version(manifest_version)
        core_match = core_version(cff_version) == core_version(manifest_version)
    return Analysis(
        root=str(root),
        status=status,
        actionable=actionable,
        cff_version=cff_version,
        manifest_path=manifest.path if manifest else None,
        manifest_version=manifest_version,
        exact_match=exact_match,
        core_match=core_match,
        reason=reason,
    )


def analyze_repository(root: Path) -> Analysis:
    root = root.resolve()
    cff = root / "CITATION.cff"
    if not cff.is_file():
        return _result(root, "CFF_MISSING", "root CITATION.cff not found")
    cff_version = parse_cff_version(cff)
    manifests = discover_manifests(root)
    if len(manifests) == 0:
        return _result(
            root, "MANIFEST_MISSING", "no supported root manifest", cff_version=cff_version
        )
    if len(manifests) > 1:
        return _result(
            root, "MANIFEST_AMBIGUOUS", "multiple supported root manifests", cff_version=cff_version
        )
    manifest = manifests[0]
    if cff_version is None:
        return _result(
            root, "CFF_VERSION_MISSING", "top-level CFF software version missing", manifest=manifest
        )
    if manifest.ambiguous:
        return _result(
            root,
            "SCOPE_AMBIGUOUS",
            "manifest is a versionless workspace/metapackage",
            cff_version=cff_version,
            manifest=manifest,
        )
    if manifest.dynamic:
        return _result(
            root,
            "MANIFEST_DYNAMIC",
            "manifest version is dynamically resolved",
            cff_version=cff_version,
            manifest=manifest,
        )
    if manifest.version is None:
        return _result(
            root,
            "MANIFEST_VERSION_MISSING",
            "static manifest version missing",
            cff_version=cff_version,
            manifest=manifest,
        )
    exact = exact_version(cff_version) == exact_version(manifest.version)
    core = core_version(cff_version) == core_version(manifest.version)
    if exact:
        return _result(
            root, "MATCH", "exact versions match", cff_version=cff_version, manifest=manifest
        )
    if core:
        return _result(
            root,
            "NORMALIZED_MATCH",
            "versions match under conservative core normalization",
            cff_version=cff_version,
            manifest=manifest,
        )
    return _result(
        root,
        "DRIFT",
        "CFF and manifest versions differ",
        cff_version=cff_version,
        manifest=manifest,
        actionable=True,
    )
