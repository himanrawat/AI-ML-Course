# ======================================
# TOPIC: GIT FOR ML PROJECTS
# LEVEL: BEGINNER
# ID: python.tooling.git
# ======================================

# INTRODUCTION
# Git records every version of your code so you can experiment fearlessly,
# undo mistakes and collaborate. ML projects add special challenges: large
# data files, model weights, notebooks and secrets.
#
# THEORY
# Core workflow:
#   git init / git clone URL      start or copy a repository
#   git status                    what changed?
#   git add file / git add -p     stage changes (choose what goes in)
#   git commit -m "message"       save a snapshot
#   git log --oneline             history
#   git diff                      unstaged changes; git diff --staged for staged
#   git switch -c feature         new branch; git switch main to go back
#   git merge feature             combine branches
#   git push / git pull           sync with a remote (GitHub)
# ML-specific rules:
# - .gitignore: .venv/, __pycache__/, .env, data/, *.pt, *.ckpt, .ipynb_checkpoints/
# - Never commit API keys. If you do, ROTATE the key - deleting the commit
#   is not enough, the history keeps it.
# - Large data/models: use Git LFS or DVC, or store them in object storage.
# - Small, focused commits with clear messages ("Add stratified split").
#
# REAL-WORLD ANALOGY
# Save points in a video game: you save before a risky level (commit), can
# try alternate paths (branches) and reload a save if things go wrong.
#
# SYNTAX:
#   git add file.py && git commit -m "Describe the change"
#
# SMALL WORKING EXAMPLE:
import shutil
import subprocess
import tempfile
from pathlib import Path

def git(*args, cwd):
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return result.stdout.strip()

if shutil.which("git"):
    repo = Path(tempfile.mkdtemp())
    git("init", "-q", cwd=repo)
    git("config", "user.email", "learner@example.com", cwd=repo)
    git("config", "user.name", "Learner", cwd=repo)
    (repo / ".gitignore").write_text(".venv/\n__pycache__/\n.env\ndata/\n*.pt\n")
    (repo / "train.py").write_text("print('training')\n")
    (repo / ".env").write_text("API_KEY=secret\n")
    print(git("status", "--short", cwd=repo))
    git("add", ".", cwd=repo)
    git("commit", "-q", "-m", "Add training script", cwd=repo)
    git("switch", "-q", "-c", "experiment", cwd=repo)
    (repo / "train.py").write_text("print('training with dropout')\n")
    git("commit", "-q", "-am", "Try dropout", cwd=repo)
    print(git("log", "--oneline", "--all", cwd=repo))
    print("tracked files:", git("ls-files", cwd=repo).split())
else:
    print("git is not installed")

# EXPLANATION (LINE BY LINE):
# git(*args, cwd)            -> helper to run git commands from Python.
# git init / config          -> create a repo in a temp folder and set an identity.
# .gitignore                 -> lists files Git must ignore (.env, data, weights).
# git status --short         -> .env does NOT appear: it is ignored.
# git add . / commit         -> first snapshot.
# git switch -c experiment   -> a new branch for a risky change.
# commit -am                 -> stage tracked changes and commit in one step.
# git ls-files               -> proves .env was never committed.
#
# COMMON MISTAKES:
# 1. Committing secrets, datasets or model weights.
# 2. Huge commits mixing unrelated changes.
# 3. Working directly on main for experiments.
# 4. Committing notebooks with large outputs (clear outputs first).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# In a terminal, turn the AI-ML-Course folder into a Git repository, write a
# suitable .gitignore, and make your first commit. Paste your commands and
# the output of git log --oneline as comments.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Using the git() helper in a temporary repo, create a merge conflict on
# purpose (two branches edit the same line), print the conflicted file, then
# resolve it and commit. Explain each step in comments.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write a pre-commit style check secret_scan(paths) that searches staged files
# for patterns like "sk-", "api_key=" or long random-looking strings, and
# returns a list of findings with file and line. Install it as
# .git/hooks/pre-commit in a temporary repo and show it blocking a commit.

# YOUR CODE:

