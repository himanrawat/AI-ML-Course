# ======================================
# TOPIC: FIXTURES AND MOCKING
# LEVEL: ADVANCED
# ID: python.testing.fixtures-mocking
# ======================================

# INTRODUCTION
# Real code reads files, calls LLM APIs and depends on time. Fixtures prepare
# reusable test setup; mocks replace slow, costly or unpredictable parts so
# tests stay fast and deterministic.
#
# THEORY
# - A FIXTURE is a function decorated with @pytest.fixture; tests receive its
#   return value by naming it as a parameter. Use yield for setup + teardown.
# - Built-in fixtures: tmp_path (a temporary folder), monkeypatch (temporarily
#   change attributes, env vars, dict items), capsys (capture printed output).
# - MOCKING replaces a real object with a fake that records how it was called:
#   unittest.mock.Mock / MagicMock, patch("module.name") as a context manager.
# - mock.return_value sets what it returns; mock.side_effect can raise errors
#   or return a sequence of values.
# - Assert calls: mock.assert_called_once_with(...), mock.call_count.
# - DEPENDENCY INJECTION (passing collaborators as arguments) makes code easy
#   to test without patching.
#
# REAL-WORLD ANALOGY
# A flight simulator: pilots practise emergencies with a fake plane that
# behaves on command, instead of crashing a real one.
#
# SYNTAX:
#   @pytest.fixture
#   def sample_data(): return [...]
#   def test_x(sample_data, tmp_path, monkeypatch): ...
#   fake = Mock(return_value="ok"); fake.side_effect = TimeoutError()
#
# SMALL WORKING EXAMPLE:
import json
from unittest.mock import Mock

import pytest

class Summarizer:
    def __init__(self, llm):
        self.llm = llm

    def summarize(self, text, retries=1):
        for attempt in range(retries + 1):
            try:
                return self.llm(f"Summarize in one sentence:\n{text}").strip()
            except TimeoutError:
                if attempt == retries:
                    raise

def load_documents(folder):
    return [json.loads(p.read_text()) for p in sorted(folder.glob("*.json"))]

@pytest.fixture
def docs_folder(tmp_path):
    for i in range(3):
        (tmp_path / f"doc{i}.json").write_text(json.dumps({"id": i, "text": f"text {i}"}))
    return tmp_path

def test_load_documents(docs_folder):
    assert [d["id"] for d in load_documents(docs_folder)] == [0, 1, 2]

def test_summarize_uses_prompt():
    fake_llm = Mock(return_value="  A short summary. ")
    assert Summarizer(fake_llm).summarize("long text") == "A short summary."
    fake_llm.assert_called_once()
    assert "long text" in fake_llm.call_args.args[0]

def test_summarize_retries_on_timeout():
    fake_llm = Mock(side_effect=[TimeoutError(), "ok"])
    assert Summarizer(fake_llm).summarize("x", retries=1) == "ok"
    assert fake_llm.call_count == 2

def test_api_key_from_env(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    import os
    assert os.environ["LLM_API_KEY"] == "test-key"

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q", "-p", "no:cacheprovider",
                                  "--import-mode=importlib"]))

# EXPLANATION (LINE BY LINE):
# Summarizer receives llm as an argument -> dependency injection: easy to fake.
# docs_folder fixture uses tmp_path   -> real files in a throwaway folder.
# test_load_documents(docs_folder)    -> pytest injects the fixture by name.
# Mock(return_value=...)              -> fake LLM returning a fixed answer.
# fake_llm.call_args.args[0]          -> inspect the prompt that was sent.
# Mock(side_effect=[TimeoutError(), "ok"]) -> fail first, succeed second.
# monkeypatch.setenv                  -> environment change undone after the test.
#
# COMMON MISTAKES:
# 1. Patching where something is DEFINED instead of where it is USED.
# 2. Mocking so much that the test no longer checks real behaviour.
# 3. Calling real paid APIs from unit tests.
# 4. Sharing mutable fixture data between tests (use function-scoped fixtures).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write a fixture that returns a list of 5 user dicts and two tests that use
# it (count of adults, sorted names). Use capsys to test a function that prints.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write get_weather(city, http_get) that calls http_get(url) and returns the
# temperature from the JSON. Test success, a missing field, and a raised
# ConnectionError using Mock - without any network access.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write a ClassificationService that calls an LLM function, parses JSON output
# into a label from an allowed set, retries once with an error message when
# the output is invalid, and logs failures. Test it with mocks covering: valid
# output, invalid-then-valid output (check the retry prompt contains the
# error), invalid twice (raises), and a timeout. Use a yield fixture.

# YOUR CODE:

