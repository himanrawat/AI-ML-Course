# ======================================
# TOPIC: PROJECT TOOLING (PYPROJECT, LINTING, FORMATTING)
# LEVEL: INTERMEDIATE
# ID: python.tooling.project-tooling
# ======================================

# INTRODUCTION
# Professional Python projects look alike: a pyproject.toml, consistent
# formatting, a linter catching mistakes and type checks. Learning the tools
# now makes every later project cleaner.
#
# THEORY
# - pyproject.toml: the standard project file - name, version, Python version,
#   dependencies and tool settings.
# - uv: a fast tool that manages Python versions, virtual environments,
#   dependencies and lock files:
#     uv init, uv add numpy, uv run script.py, uv sync
# - ruff: very fast linter AND formatter (replaces flake8, isort, black):
#     ruff check .   ruff check --fix .   ruff format .
# - mypy or pyright: static type checkers using your type hints.
# - pre-commit: runs these tools automatically before each commit.
# - Jupyter notebooks are great for exploration; move reusable code into
#   modules with tests.
# - tomllib (standard library) reads TOML files.
#
# REAL-WORLD ANALOGY
# A professional kitchen's standards: every station is laid out the same way,
# and an inspector (linter) checks hygiene before food leaves the kitchen.
#
# SYNTAX:
#   [project]
#   name = "my-project"
#   requires-python = ">=3.12"
#   dependencies = ["numpy>=2.0"]
#   [tool.ruff]
#   line-length = 100
#
# SMALL WORKING EXAMPLE:
import tomllib

PYPROJECT = """
[project]
name = "sentiment-service"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["pydantic>=2.7", "httpx>=0.27"]

[project.optional-dependencies]
dev = ["pytest>=8", "ruff>=0.6", "mypy>=1.10"]

[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]
"""
config = tomllib.loads(PYPROJECT)
project = config["project"]
print(project["name"], project["version"], project["requires-python"])
print("runtime deps:", project["dependencies"])
print("dev deps:", project["optional-dependencies"]["dev"])
print("ruff rules:", config["tool"]["ruff"]["lint"]["select"])

# EXPLANATION (LINE BY LINE):
# PYPROJECT = """..."""      -> a typical pyproject.toml (normally a file).
# [project]                  -> package metadata and runtime dependencies.
# [project.optional-dependencies] dev -> tools needed only for development.
# [tool.ruff] / [tool.ruff.lint] -> tool configuration lives in the same file.
#   E/F: errors and pyflakes, I: import sorting, B: bug-prone patterns,
#   UP: upgrade old syntax.
# tomllib.loads(text)        -> parse TOML into dicts (tomllib.load for files).
#
# COMMON MISTAKES:
# 1. Unpinned or missing dependencies ("works on my machine").
# 2. Arguing about formatting instead of letting a formatter decide.
# 3. Ignoring linter warnings that point to real bugs (unused variables,
#    mutable defaults).
# 4. Keeping all code in notebooks with no tests.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Install ruff into the course .venv (uv pip install --python .venv/bin/python
# ruff), run "ruff check" on one of your completed exercise files and fix
# every reported issue. Paste the before/after output as comments.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write check_pyproject(text) that validates a pyproject string: required
# [project] keys present, requires-python set, every dependency has a version
# constraint. Return a list of problems. Test it on a good and a bad example.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Use "uv init" in a temporary folder (via subprocess) to scaffold a project,
# "uv add" a dependency, add ruff and pytest as dev dependencies, write a
# small module plus a test, and run "uv run pytest" and "uv run ruff check".
# Print each command's exit code and summarise what uv created.

# YOUR CODE:

