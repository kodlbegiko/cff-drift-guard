import pytest
from cff_drift_guard.versions import core_version, exact_version

@pytest.mark.parametrize(("value","expected"), [
    ("1.2.3","1.2.3"),(" v1.2.3 ","1.2.3"),("V2","2"),("version1","version1")
])
def test_exact(value, expected):
    assert exact_version(value) == expected

@pytest.mark.parametrize(("value","expected"), [
    ("1.2.0","1.2"),("1.0.0","1"),("v1.2.3+abc","1.2.3"),("1.2.3-rc1","1.2.3"),
    ("2.0.0.dev4","2"),("release-x","release-x"),("1","1"),("01.02.00","01.02")
])
def test_core(value, expected):
    assert core_version(value) == expected
