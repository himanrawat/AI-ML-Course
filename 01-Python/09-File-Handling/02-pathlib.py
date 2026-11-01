# ======================================
# TOPIC: PATHLIB (WORKING WITH PATHS)
# LEVEL: INTERMEDIATE
# ID: python.files.pathlib
# ======================================

# INTRODUCTION
# ML projects juggle many files: data/raw, data/processed, models/, outputs/.
# pathlib gives a clean, cross-platform way to build paths and find files.
#
# THEORY
# - Path objects represent file system paths: Path("data") / "train.csv".
# - The / operator joins parts correctly on every operating system.
# - Useful attributes: .name, .stem, .suffix, .parent, .parts.
# - Checks: .exists(), .is_file(), .is_dir().
# - Create: .mkdir(parents=True, exist_ok=True), .touch().
# - Quick IO: .read_text(), .write_text(), .read_bytes(), .write_bytes().
# - Search: .iterdir() (direct children), .glob("*.csv"), .rglob("*.py")
#   (recursive).
# - Path.cwd() is the current directory; Path(__file__).parent is the folder
#   of the current script - use it to find files next to your code.
#
# REAL-WORLD ANALOGY
# A GPS address object: instead of writing an address as one long string,
# you have street, city and country fields you can change independently.
#
# SYNTAX:
#   from pathlib import Path
#   p = Path("data") / "raw" / "file.csv"
#   p.parent.mkdir(parents=True, exist_ok=True)
#
# SMALL WORKING EXAMPLE:
import tempfile
from pathlib import Path

root = Path(tempfile.mkdtemp()) / "project"
raw = root / "data" / "raw"
raw.mkdir(parents=True, exist_ok=True)
for name in ["train.csv", "test.csv", "notes.txt"]:
    (raw / name).write_text("id,value\n1,10\n", encoding="utf-8")
csv_files = sorted(p.name for p in root.rglob("*.csv"))
print(csv_files)
sample = raw / "train.csv"
print(sample.name, sample.stem, sample.suffix, sample.parent.name)
processed = sample.with_suffix(".parquet")
print(processed.name, processed.exists())
print(sample.relative_to(root))
print(Path(__file__).name)

# EXPLANATION (LINE BY LINE):
# Path(tempfile.mkdtemp()) / "project" -> build paths with / instead of strings.
# raw.mkdir(parents=True, exist_ok=True) -> create all missing folders, no error if present.
# (raw / name).write_text(...)  -> create a small file in one call.
# root.rglob("*.csv")           -> recursively find every CSV under root.
# .name / .stem / .suffix / .parent -> "train.csv", "train", ".csv", raw folder.
# with_suffix(".parquet")       -> same path with a new extension (file not created).
# relative_to(root)             -> data/raw/train.csv.
# Path(__file__).name           -> the name of this script file.
#
# COMMON MISTAKES:
# 1. Building paths with string + "/" (breaks on Windows, double slashes).
# 2. Relying on the current working directory instead of Path(__file__).parent.
# 3. Forgetting parents=True when creating nested folders.
# 4. Confusing .stem (no extension) with .name.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Print the folder this script lives in, and list every file in it with its
# size in bytes (use .iterdir() and .stat().st_size).

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Create a temporary project with the folders data/raw, data/processed,
# models and outputs. Then write summarize_tree(root) that returns a dict of
# file extension -> count for all files below root.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write organize_downloads(folder) that moves files into subfolders by type
# (images, documents, data, other) using a mapping of suffixes, avoids
# overwriting existing files by adding "_1", "_2" suffixes, and returns a log
# of moves. Test it on a temporary folder with at least 8 files.

# YOUR CODE:

