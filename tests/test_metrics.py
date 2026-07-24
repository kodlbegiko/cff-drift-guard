import math
from cff_drift_guard.metrics import classification_metrics, exclusion_counts, wilson_interval


def test_wilson_empty():
    assert wilson_interval(0, 0) == (0.0, 1.0)

def test_wilson_all_success_bounded():
    low, high = wilson_interval(2, 2)
    assert 0 < low < high == 1.0

def test_wilson_midpoint():
    low, high = wilson_interval(5, 10)
    assert low < 0.5 < high

def test_classification_perfect():
    result = classification_metrics([True, False], [True, False])
    assert result["precision"] == result["recall"] == result["f1"] == 1

def test_classification_miss():
    result = classification_metrics([True, False], [False, False])
    assert result["fn"] == 1 and result["recall"] == 0

def test_classification_false_positive():
    result = classification_metrics([False], [True])
    assert result["fp"] == 1 and result["precision"] == 0

def test_classification_empty_positive_denominator():
    result = classification_metrics([False], [False])
    assert math.isclose(result["f1"], 0.0)

def test_exclusion_counts_sorted():
    result = exclusion_counts([{"exclusion_reason":"b"},{"exclusion_reason":"a"},{"exclusion_reason":"a"}])
    assert list(result) == ["a","b"] and result["a"] == 2
