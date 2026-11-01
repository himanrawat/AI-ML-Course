# ======================================
# TOPIC: WORKING WITH JSON DATA
# LEVEL: INTERMEDIATE
# ID: python.apis.json
# ======================================

# INTRODUCTION
# JSON is the language of web APIs and LLM tools: requests, responses,
# function-call arguments and structured outputs are all JSON.
#
# THEORY
# - json.loads(text) -> Python objects; json.dumps(obj) -> text.
# - Mapping: object<->dict, array<->list, string<->str, number<->int/float,
#   true/false<->True/False, null<->None.
# - JSON keys are always strings: {1: "a"} becomes {"1": "a"}.
# - dumps options: indent, sort_keys, ensure_ascii=False, separators,
#   default=func (for types JSON does not support).
# - Invalid JSON raises json.JSONDecodeError (with line/column information).
# - Navigate nested data carefully with .get() and isinstance checks.
#
# REAL-WORLD ANALOGY
# JSON is a shipping manifest written in a format every port understands.
# Python unpacks the manifest into its own boxes (dicts and lists).
#
# SYNTAX:
#   data = json.loads(text)
#   text = json.dumps(data, indent=2, default=str)
#
# SMALL WORKING EXAMPLE:
import json
from datetime import datetime

api_response = """
{
  "model": "demo-model",
  "usage": {"input_tokens": 12, "output_tokens": 30},
  "content": [{"type": "text", "text": "Hello!"}],
  "stop_reason": null
}
"""
data = json.loads(api_response)
text_blocks = [b["text"] for b in data["content"] if b.get("type") == "text"]
total_tokens = sum(data["usage"].values())
print(text_blocks, total_tokens, data["stop_reason"])
record = {1: "one", "when": datetime(2026, 1, 15, 9, 30), "tags": ("a", "b")}
print(json.dumps(record, default=str, sort_keys=False))
print(json.dumps({"name": "Zoë"}), json.dumps({"name": "Zoë"}, ensure_ascii=False))
try:
    json.loads('{"answer": 42,}')
except json.JSONDecodeError as error:
    print(f"invalid JSON at line {error.lineno}, col {error.colno}: {error.msg}")

# EXPLANATION (LINE BY LINE):
# json.loads(api_response)   -> nested dicts and lists; null became None.
# [b["text"] for b in data["content"] if b.get("type") == "text"]
#                            -> extract text blocks (a common LLM-response pattern).
# sum(data["usage"].values()) -> 12 + 30 = 42 tokens.
# json.dumps(record, default=str) -> datetime is not JSON-serializable, so
#                            default=str converts it; key 1 becomes "1"; tuple -> list.
# ensure_ascii=False         -> keeps "Zoë" readable instead of "Zoë".
# JSONDecodeError            -> trailing commas are not valid JSON.
#
# COMMON MISTAKES:
# 1. Using Python syntax in JSON: single quotes, True/None, trailing commas.
# 2. Assuming integer keys survive a JSON round trip.
# 3. Chaining data["a"]["b"]["c"] without handling missing keys.
# 4. Using eval() to parse JSON (dangerous!).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Convert a dict describing yourself (with a nested list of hobbies) to a
# pretty JSON string, then back to a dict, and check they are equal.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Given a JSON string of 5 orders (id, customer, items: [{name, price, qty}]),
# compute each order's total and the best customer by total spend.
# Output the summary as JSON with sorted keys.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# LLMs sometimes return almost-JSON. Write extract_json(text) that finds the
# first {...} object in text (handling ```json fences and leading prose),
# tries json.loads, and on failure applies simple repairs (remove trailing
# commas, replace smart quotes) before trying again. Return (data, repaired:
# bool) or raise a ValueError with the decode error position. Test on 6 inputs.

# YOUR CODE:

