# ======================================
# TOPIC: PROJECT 8 - PRODUCTION-READY PROMPT MANAGEMENT WORKFLOW
# LEVEL: ADVANCED
# ID: prompt-engineering.projects.prompt-management
# ======================================

# INTRODUCTION
# Bring everything together: prompts stored as versioned files, validated and
# evaluated automatically before release (like CI for code), rolled out
# gradually, observed in production, and rolled back safely.
#
# THEORY
# Skills used: templates (03/04), evaluation harness (Project 7), versioning
# and A/B testing (04/03), observability (05/04), guardrails (05/03), Git and
# testing (01-Python/15-16).
# The workflow:
#  1. AUTHOR: prompt file (YAML/JSON) with name, version, owner, model,
#     template, variables, changelog.
#  2. VALIDATE: lint (required fields, declared variables match the template).
#  3. EVALUATE: run the eval set; compare with the current production version;
#     block release on regressions (quality gate) - in CI on every pull request.
#  4. RELEASE: register as a candidate; canary/A-B rollout to a % of traffic.
#  5. OBSERVE: trace version-tagged calls; monitor quality, cost, latency, drift.
#  6. PROMOTE or ROLL BACK; add production failures to the eval set.
# Design decisions and WHY: prompts in Git give review and history; automated
# gates stop "quick fixes" from silently breaking other cases; version tags in
# logs make every output traceable.
# Deliverables: prompt files, a registry, a lint + eval gate script runnable in
# CI, rollout config, and a runbook for rollback.
#
# REAL-WORLD ANALOGY
# A pharmaceutical release process: formulation documented, lab-tested against
# standards, trialled on a small group, monitored after release, and recalled
# quickly if problems appear.
#
# SYNTAX:
#   python release.py lint prompts/ && python release.py gate support_reply 1.5.0
#
# SMALL WORKING EXAMPLE:
import json
import string
import tempfile
from pathlib import Path

PROMPT_FILES = {
    "support_reply@1.4.0.json": {"name": "support_reply", "version": "1.4.0", "model": "claude-opus-5-5",
                                 "variables": ["message"], "template": "Reply helpfully to: $message",
                                 "eval_score": 0.86, "status": "production"},
    "support_reply@1.5.0.json": {"name": "support_reply", "version": "1.5.0", "model": "claude-opus-5-5",
                                 "variables": ["message", "policy"],
                                 "template": "Using <policy>$policy</policy>, reply to: $message ($tone)",
                                 "eval_score": 0.91, "status": "candidate"},
}

def lint(prompt):
    problems = [f"missing field {k}" for k in ("name", "version", "model", "template", "variables") if k not in prompt]
    used = {m.group("named") for m in string.Template.pattern.finditer(prompt.get("template", "")) if m.group("named")}
    problems += [f"undeclared variable ${v}" for v in sorted(used - set(prompt.get("variables", [])))]
    problems += [f"unused variable {v}" for v in sorted(set(prompt.get("variables", [])) - used)]
    return problems

def quality_gate(candidate, production, min_gain=0.0):
    if lint(candidate):
        return False, f"lint failed: {lint(candidate)}"
    if candidate["eval_score"] < production["eval_score"] + min_gain:
        return False, f"eval {candidate['eval_score']} does not beat production {production['eval_score']}"
    return True, "passed: ready for canary rollout at 10%"

folder = Path(tempfile.mkdtemp()) / "prompts"
folder.mkdir()
for filename, data in PROMPT_FILES.items():
    (folder / filename).write_text(json.dumps(data, indent=2))
registry = {p.stem: json.loads(p.read_text()) for p in sorted(folder.glob("*.json"))}
production = next(p for p in registry.values() if p["status"] == "production")
for key, prompt in registry.items():
    print(f"{key:<22} lint: {lint(prompt) or 'ok'}")
print("gate for 1.5.0:", quality_gate(registry["support_reply@1.5.0"], production))
registry["support_reply@1.5.0"]["variables"].append("tone")
print("gate after fixing the variable:", quality_gate(registry["support_reply@1.5.0"], production))

# EXPLANATION (LINE BY LINE):
# PROMPT_FILES               -> prompts as versioned JSON files (YAML works too).
# lint()                     -> required metadata + template variables must exactly match
#                               the declared ones (catches "$tone" never being supplied).
# quality_gate()             -> blocks release on lint errors or no eval improvement;
#                               in CI this would run the real eval harness (Project 7).
# registry                   -> loaded from disk, keyed by name@version.
# First gate fails           -> 1.5.0 uses an undeclared $tone. After declaring it, the
#                               gate passes and recommends a canary rollout.
#
# COMMON MISTAKES:
# 1. Editing prompts directly in production config without review.
# 2. Eval gates that only check "doesn't crash".
# 3. Rolling out to 100% at once.
# 4. No documented rollback procedure.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write the folder structure and a sample prompt file for a "ticket_classifier"
# prompt with changelog entries for two versions.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Turn lint + quality_gate into a CLI script (argparse) that exits with a
# non-zero code on failure, and write a GitHub Actions workflow YAML (as a
# string here) that runs it on every pull request touching prompts/.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build the full workflow: registry loading from disk, eval gate using your
# Project 7 harness, canary routing by hashed user id with a configurable
# percentage, version-tagged tracing (05/04), an automatic rollback rule
# (error rate or quality drop beyond a threshold), and a RUNBOOK.md written by
# the script describing how to promote or roll back.

# YOUR CODE:

