# ======================================
# TOPIC: CI/CD FOR ML AND LLM APPLICATIONS
# LEVEL: ADVANCED
# ID: mlops.practices.ci-cd
# ======================================

# INTRODUCTION
# Every change - code, data, model or prompt - can break an AI system. CI/CD
# runs automatic checks on every change and deploys safely, so shipping
# improvements becomes routine instead of risky.
#
# THEORY
# CONTINUOUS INTEGRATION (on every pull request):
# - Lint/format (ruff), type checks, unit tests (pytest) - like any software.
# - DATA checks: schema, missing values, ranges on sample data.
# - MODEL checks: train on a small sample (smoke test); evaluate the candidate
#   on a fixed test set; fail if metrics drop below thresholds or below the
#   current production model (quality gate).
# - LLM/prompt checks: run the eval set (cached or mocked for speed, real model
#   on a schedule or before release); check cost and latency budgets.
# CONTINUOUS DELIVERY/DEPLOYMENT:
# - Build a container image, push to a registry, deploy to staging, run smoke
#   tests, then gradual rollout (canary / blue-green) to production with
#   automatic rollback on alerts.
# - Secrets live in the CI system's secret store; never in the repo.
# Tools: GitHub Actions, GitLab CI; for ML pipelines: Airflow, Prefect,
# Kubeflow, Dagster.
#
# REAL-WORLD ANALOGY
# A car factory's quality line: every car passes automated inspections at each
# station, test drives on a private track (staging), then a small batch goes
# to customers first (canary) before full production.
#
# SYNTAX:
#   .github/workflows/ci.yml: on: pull_request; jobs: test: steps: [...]
#
# SMALL WORKING EXAMPLE:
WORKFLOW = """name: ci
on:
  pull_request:
    paths: ["src/**", "prompts/**", "tests/**"]
jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv sync --frozen
      - run: uv run ruff check .
      - run: uv run pytest -q
      - run: uv run python scripts/quality_gate.py --min-f1 0.90
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
"""

def quality_gate(candidate, production, min_f1=0.90, max_regression=0.01, max_p95_ms=800):
    checks = {
        "f1 above floor": candidate["f1"] >= min_f1,
        "no regression vs production": candidate["f1"] >= production["f1"] - max_regression,
        "latency budget": candidate["p95_ms"] <= max_p95_ms,
        "cost not +20%": candidate["cost_per_1k"] <= production["cost_per_1k"] * 1.2,
    }
    return all(checks.values()), checks

production = {"f1": 0.92, "p95_ms": 610, "cost_per_1k": 1.80}
candidates = {"prompt v1.6 (concise)": {"f1": 0.93, "p95_ms": 540, "cost_per_1k": 1.50},
              "model swap (bigger)": {"f1": 0.94, "p95_ms": 1200, "cost_per_1k": 3.10},
              "retrained model": {"f1": 0.89, "p95_ms": 600, "cost_per_1k": 1.80}}
print(WORKFLOW.splitlines()[0], f"... {len(WORKFLOW.splitlines())} lines")
for name, metrics in candidates.items():
    passed, checks = quality_gate(metrics, production)
    failed = [k for k, ok in checks.items() if not ok]
    print(f"{name:<24} {'PASS' if passed else 'FAIL'} {failed}")

# EXPLANATION (LINE BY LINE):
# WORKFLOW                   -> a GitHub Actions pipeline run on pull requests touching code,
#                               prompts or tests: install with uv, lint, test, quality gate.
# secrets.ANTHROPIC_API_KEY  -> the key comes from the CI secret store.
# quality_gate               -> several independent checks: absolute floor, regression vs
#                               production, latency and cost budgets.
# Results                    -> the concise prompt passes; the bigger model is more accurate
#                               but breaks latency and cost budgets; the retrained model
#                               regresses. Quality alone is not the only gate.
#
# COMMON MISTAKES:
# 1. Only unit tests - no model or prompt quality gates.
# 2. Gates on accuracy alone, ignoring latency and cost.
# 3. Calling paid APIs on every commit for large eval sets (use sampling/caching).
# 4. Deploying to 100% of traffic in one step.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write a pytest file (as a string or real file) with 3 tests for a text
# preprocessing function, and add a ruff step and the pytest step to a minimal
# workflow YAML.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Turn quality_gate into scripts/quality_gate.py with argparse that reads
# candidate and production metrics from JSON files and exits non-zero on
# failure, printing a Markdown summary suitable for a PR comment.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Put your AI-ML-Course (or a project from it) on GitHub with a real
# GitHub Actions workflow that lints, runs pytest, and runs a small offline
# eval gate. Make one PR that fails the gate and one that passes; paste the
# run links as comments.

# YOUR CODE:

