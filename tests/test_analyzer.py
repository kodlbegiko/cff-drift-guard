from pathlib import Path
import pytest
from cff_drift_guard.analyzer import analyze_repository

FIX = Path(__file__).parent / "fixtures"

@pytest.mark.parametrize(("name","status","actionable"), [
    ("match","MATCH",False),("mismatch","DRIFT",True),("cff_missing","CFF_MISSING",False),
    ("cff_version_missing","CFF_VERSION_MISSING",False),("dynamic_pyproject","MANIFEST_DYNAMIC",False),
    ("workspace_cargo","SCOPE_AMBIGUOUS",False),("ambiguous_manifests","MANIFEST_AMBIGUOUS",False),
    ("description","MATCH",False),("julia","MATCH",False),("node","MATCH",False),("dart","SCOPE_AMBIGUOUS",False),
])
def test_statuses(name, status, actionable):
    result = analyze_repository(FIX / name)
    assert result.status == status
    assert result.actionable is actionable

def test_mismatch_values():
    result = analyze_repository(FIX / "mismatch")
    assert result.cff_version == "1.2.0"
    assert result.manifest_version == "1.3.0"
    assert result.exact_match is False and result.core_match is False

def test_julia_leading_v_normalized():
    result = analyze_repository(FIX / "julia")
    assert result.exact_match is True

def test_to_dict_serializable_shape():
    result = analyze_repository(FIX / "match").to_dict()
    assert result["status"] == "MATCH" and "reason" in result
