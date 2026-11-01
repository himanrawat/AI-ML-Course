# ======================================
# TOPIC: CSV AND JSON FILES
# LEVEL: INTERMEDIATE
# ID: python.files.csv-json
# ======================================

# INTRODUCTION
# CSV is the most common format for tabular datasets; JSON (and JSON Lines)
# is the standard for configs, API data and LLM training/eval datasets.
#
# THEORY
# CSV (csv module):
# - csv.reader / csv.writer work with lists; csv.DictReader / DictWriter work
#   with dicts keyed by the header. All values are read as STRINGS.
# - Open CSV files with newline="" so the csv module controls line endings.
# JSON (json module):
# - json.dump(obj, file) / json.load(file) work with files.
# - json.dumps(obj) / json.loads(text) work with strings.
# - indent=2 for readable output; ensure_ascii=False keeps non-English text.
# - JSON types: object->dict, array->list, string->str, number->int/float,
#   true/false->True/False, null->None. Tuples become lists; sets are not allowed.
# JSON Lines (.jsonl): one JSON object per line - streamable, used for datasets.
#
# REAL-WORLD ANALOGY
# CSV is a spreadsheet printed as plain text. JSON is a labelled set of nested
# folders. Both are languages different programs agree to speak.
#
# SYNTAX:
#   with open(p, newline="", encoding="utf-8") as f: rows = list(csv.DictReader(f))
#   with open(p, "w", encoding="utf-8") as f: json.dump(data, f, indent=2)
#
# SMALL WORKING EXAMPLE:
import csv
import json
import tempfile
from pathlib import Path

folder = Path(tempfile.mkdtemp())
csv_path = folder / "people.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age", "city"])
    writer.writeheader()
    writer.writerows([
        {"name": "Asha", "age": 31, "city": "Pune"},
        {"name": "Ben", "age": 25, "city": "Delhi"},
    ])
with open(csv_path, newline="", encoding="utf-8") as f:
    people = [{**row, "age": int(row["age"])} for row in csv.DictReader(f)]
print(people)
json_path = folder / "people.json"
json_path.write_text(json.dumps(people, indent=2, ensure_ascii=False), encoding="utf-8")
loaded = json.loads(json_path.read_text(encoding="utf-8"))
print(loaded == people)
jsonl_path = folder / "eval.jsonl"
with open(jsonl_path, "w", encoding="utf-8") as f:
    for q, a in [("2+2?", "4"), ("Capital of France?", "Paris")]:
        f.write(json.dumps({"question": q, "answer": a}) + "\n")
with open(jsonl_path, encoding="utf-8") as f:
    print([json.loads(line)["answer"] for line in f])

# EXPLANATION (LINE BY LINE):
# csv.DictWriter(..., fieldnames=[...]) -> writes dicts as rows in this column order.
# writeheader() / writerows([...])      -> header row, then data rows.
# csv.DictReader(f)                     -> each row becomes a dict of STRINGS.
# {**row, "age": int(row["age"])}       -> copy the row, converting age to int.
# json.dumps(people, indent=2)          -> pretty JSON text.
# json.loads(...) == people             -> round trip preserved the data.
# eval.jsonl                            -> one JSON object per line; read line by line.
#
# COMMON MISTAKES:
# 1. Forgetting that CSV values are strings ("31" + 1 fails).
# 2. Omitting newline="" -> blank lines between rows on Windows.
# 3. Confusing json.load (file) with json.loads (string).
# 4. Trying to json.dumps sets, datetimes or custom objects without converting.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write a list of 3 product dicts to products.json (temporary folder) with
# indentation, read it back and print the most expensive product.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write csv_to_json(csv_path, json_path, types) where types maps column names
# to conversion functions (e.g. {"age": int, "score": float}). Rows that fail
# conversion should be collected in an "errors" list in the output JSON.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Create a JSONL dataset of 20 fake customer-support tickets (id, text, label).
# Write functions to: stream-read it, split it into train/test (80/20) with a
# fixed random seed, write both splits as JSONL, and print label counts per
# split. Write a custom json.JSONEncoder subclass that can serialise datetime
# and set values.

# YOUR CODE:

