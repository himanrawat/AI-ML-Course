# ======================================
# TOPIC: VIRTUAL ENVIRONMENTS AND PACKAGES
# LEVEL: BEGINNER
# ID: python.tooling.virtual-environments
# ======================================

# INTRODUCTION
# Different projects need different library versions: one needs NumPy 1.x,
# another NumPy 2.x. Virtual environments keep each project's packages
# separate so they never clash.
#
# THEORY
# - Packages installed with pip go into the ACTIVE Python environment.
# - A virtual environment is a folder (usually .venv) containing its own
#   python executable and site-packages directory.
# - Create:   python3 -m venv .venv          (or: uv venv)
#   Activate: source .venv/bin/activate      (macOS/Linux)
#             .venv\Scripts\activate         (Windows)
#   Install:  python -m pip install numpy    (or: uv pip install numpy)
#   Record:   pip freeze > requirements.txt
#   Restore:  pip install -r requirements.txt
#   Leave:    deactivate
# - sys.prefix != sys.base_prefix means you are inside a virtual environment.
# - Modern projects declare dependencies in pyproject.toml; tools like uv also
#   write a lock file with exact versions.
# - Never commit .venv to Git; commit the dependency files instead.
# - THIS COURSE: the course folder has its own .venv with numpy, pandas,
#   scikit-learn, torch, pydantic, pytest and anthropic installed.
#
# REAL-WORLD ANALOGY
# Separate toolboxes for separate jobs: the plumbing toolbox and the
# electrical toolbox never get mixed up, even if both contain a screwdriver.
#
# SYNTAX:
#   python3 -m venv .venv
#   source .venv/bin/activate
#   python -m pip install -r requirements.txt
#
# SMALL WORKING EXAMPLE:
import importlib.metadata
import sys
from pathlib import Path

in_venv = sys.prefix != sys.base_prefix
print(f"Python {sys.version_info.major}.{sys.version_info.minor}")
print("Interpreter:", sys.executable)
print("Inside a virtual environment:", in_venv)
print("Environment folder:", Path(sys.prefix).name)
for package in ["numpy", "pandas", "torch", "requests-not-installed"]:
    try:
        print(f"  {package:<24}{importlib.metadata.version(package)}")
    except importlib.metadata.PackageNotFoundError:
        print(f"  {package:<24}not installed")

# EXPLANATION (LINE BY LINE):
# sys.prefix != sys.base_prefix -> True when running inside a venv.
# sys.executable                -> the exact python binary running this file.
# Path(sys.prefix).name         -> e.g. ".venv" when the venv is active.
# importlib.metadata.version(pkg) -> the installed version of a package.
# PackageNotFoundError          -> the package is not installed in THIS environment.
#
# Run it twice to see the difference:
#   .venv/bin/python 01-Python/16-Git-and-Environments/01-virtual-environments.py
#   python3 01-Python/16-Git-and-Environments/01-virtual-environments.py
#
# COMMON MISTAKES:
# 1. Installing with one Python and running with another ("ModuleNotFoundError").
# 2. Forgetting to activate the environment in a new terminal.
# 3. Committing .venv to Git.
# 4. Using sudo pip install into the system Python.
# 5. VS Code using a different interpreter than your terminal
#    (fix: "Python: Select Interpreter" -> .venv).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# In a terminal, create a new venv in a temporary folder, activate it, install
# the "rich" package, and run python -c "import rich; print(rich.__file__)".
# Paste the commands you used as comments below.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write a script that prints every installed package and version in the current
# environment (importlib.metadata.distributions), sorted by name, and flags any
# package listed in a requirements string that is missing.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write make_project_env(folder, requirements) that uses subprocess to create a
# venv in folder, installs the requirements with that venv's own python
# (folder/.venv/bin/python -m pip ...), writes a pinned requirements.lock from
# pip freeze, and verifies the import works by running the venv's python.
# Explain in comments why calling the venv's python directly avoids activation.

# YOUR CODE:

