# ======================================
# TOPIC: TESTING WITH PYTEST
# LEVEL: INTERMEDIATE
# ID: python.testing.pytest-basics
# ======================================

# INTRODUCTION
# Tests are code that checks your code. They let you change things without
# fear - essential when data pipelines, prompts and models evolve constantly.
#
# THEORY
# - pytest discovers files named test_*.py and functions named test_*.
#   (This topic file runs pytest on itself so everything stays in one file.)
# - Use plain assert statements; pytest shows detailed failure diffs.
# - pytest.raises(ErrorType) checks that code raises an exception.
# - pytest.approx compares floats safely.
# - @pytest.mark.parametrize runs one test with many inputs.
# - Good tests: small, independent, fast, deterministic, named after the
#   behaviour they check. Arrange -> Act -> Assert.
# - Run: pytest (all), pytest -q (quiet), pytest -k name (filter),
#   pytest -x (stop on first failure).
#
# REAL-WORLD ANALOGY
# A car's pre-flight checklist: lights on, brakes work, tyres inflated. You
# run it every time before driving, and it catches problems early.
#
# SYNTAX:
#   def test_something():
#       assert func(2) == 4
#   with pytest.raises(ValueError): func(-1)
#   @pytest.mark.parametrize("x, expected", [(1, 2), (2, 4)])
#
# SMALL WORKING EXAMPLE:
import pytest

def normalize_scores(scores):
    if not scores:
        raise ValueError("scores must not be empty")
    low, high = min(scores), max(scores)
    if low == high:
        return [0.0 for _ in scores]
    return [(s - low) / (high - low) for s in scores]

def test_normalize_range():
    result = normalize_scores([10, 15, 20])
    assert result == pytest.approx([0.0, 0.5, 1.0])

def test_normalize_constant_values():
    assert normalize_scores([3, 3]) == [0.0, 0.0]

def test_normalize_empty_raises():
    with pytest.raises(ValueError, match="empty"):
        normalize_scores([])

@pytest.mark.parametrize("scores, expected_max", [([1, 2], 1.0), ([5, -5, 0], 1.0)])
def test_max_is_one(scores, expected_max):
    assert max(normalize_scores(scores)) == expected_max

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q", "-p", "no:cacheprovider",
                                  "--import-mode=importlib"]))

# EXPLANATION (LINE BY LINE):
# def normalize_scores(...)   -> the code under test.
# test_normalize_range        -> pytest.approx avoids float equality problems.
# test_normalize_constant_values -> edge case: all values equal (no division by zero).
# pytest.raises(ValueError, match="empty") -> the error type AND message are checked.
# @pytest.mark.parametrize    -> the same test runs once per input tuple.
# pytest.main([__file__, ...]) -> run pytest on this file when executed directly.
#   Normally you would just type: pytest tests/
#
# COMMON MISTAKES:
# 1. Tests that depend on each other or on execution order.
# 2. Comparing floats with == instead of pytest.approx.
# 3. Testing only the "happy path" and no edge cases.
# 4. Tests that hit real networks/APIs (slow, flaky, costly) - mock them.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write is_palindrome(text) and three tests for it (normal word, phrase with
# spaces and capitals, empty string). Run this file to execute them.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write a parametrized test with at least 6 cases for a function
# parse_duration("1h30m") -> seconds, including invalid inputs that must raise
# ValueError. Write the function test-first (TDD): tests before code.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write a tokenizer-like function chunk_text(text, max_words, overlap) used in
# RAG systems. Write tests for: exact chunk sizes, overlap correctness, no
# lost words (rejoin check), overlap >= max_words raising ValueError, and
# very short text. Aim for every branch to be covered.

# YOUR CODE:

