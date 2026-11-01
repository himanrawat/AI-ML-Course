# ======================================
# TOPIC: CREATING MODULES AND PACKAGES
# LEVEL: INTERMEDIATE
# ID: python.modules.creating-packages
# ======================================

# INTRODUCTION
# As projects grow past one file, you split code into modules and packages:
# data loading in one place, models in another, utilities in a third.
#
# THEORY
# - Any .py file is a module. Import it by its name (without .py).
# - A package is a folder; __init__.py (optional but recommended) runs when the
#   package is imported and can expose a public API.
# - Absolute imports: from mypkg.utils import clean
#   Relative imports (inside a package only): from .utils import clean
# - if __name__ == "__main__": code runs only when the file is executed
#   directly, NOT when imported. Put demo/CLI code there.
# - python -m package.module runs a module as a script with correct imports.
# - Typical project layout:
#     my_project/
#       pyproject.toml
#       src/my_project/__init__.py, data.py, model.py
#       tests/test_data.py
#
# REAL-WORLD ANALOGY
# A company: each department (module) has specialists (functions). The
# reception desk (__init__.py) tells visitors which departments to visit.
#
# SYNTAX:
#   # mypkg/__init__.py
#   from .stats import mean
#   # elsewhere
#   from mypkg import mean
#
# SMALL WORKING EXAMPLE:
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(tempfile.mkdtemp())
pkg = root / "textkit"
pkg.mkdir()
(pkg / "__init__.py").write_text('from .clean import normalize\n__version__ = "0.1.0"\n')
(pkg / "clean.py").write_text(
    "def normalize(text):\n"
    "    return ' '.join(text.lower().split())\n"
    "\n"
    "if __name__ == '__main__':\n"
    "    print('running clean.py directly:', normalize('  Hello   WORLD '))\n"
)
sys.path.insert(0, str(root))
import textkit

print(textkit.normalize("  Many   SPACES here "), textkit.__version__)
print(textkit.clean.__name__)
result = subprocess.run([sys.executable, "-m", "textkit.clean"], cwd=root,
                        capture_output=True, text=True)
print(result.stdout.strip())

# EXPLANATION (LINE BY LINE):
# pkg = root / "textkit"; pkg.mkdir() -> a folder that will become a package.
# __init__.py: from .clean import normalize -> relative import exposes a clean API.
# clean.py has an if __name__ == "__main__" block -> demo code for direct runs only.
# sys.path.insert(0, str(root))  -> let Python find our package (normally you
#                                   install it or run from the project root).
# import textkit                 -> runs __init__.py; normalize is available directly.
# textkit.clean.__name__         -> "textkit.clean" (when imported, not "__main__").
# python -m textkit.clean        -> runs the module as a script, so the main block runs.
#
# COMMON MISTAKES:
# 1. Using relative imports in a file run directly (python clean.py) -> ImportError.
# 2. Putting top-level code (like training) in modules, so importing runs it.
# 3. Circular imports between modules that depend on each other.
# 4. Editing sys.path in real projects instead of installing the package
#    (pip install -e .).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# In a temporary folder, create a module greetings.py with a function hello(name).
# Import it (adjust sys.path) and call it.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Create a package "mathkit" with modules stats.py (mean, median) and
# geometry.py (circle_area). Expose all three in __init__.py and define
# __all__. Import and use them.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Generate a small installable project in a temporary folder: src layout,
# pyproject.toml (name, version, requires-python), a package with a module that
# has a main() function, and a [project.scripts] entry point. Install it into
# a fresh venv with subprocess (python -m venv, then pip install -e) and run
# the console script. Print each step's result.

# YOUR CODE:

