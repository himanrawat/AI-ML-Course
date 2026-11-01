# ======================================
# TOPIC: CAPSTONE - A PRODUCTION AI APPLICATION
# LEVEL: ADVANCED
# ID: mlops.production.capstone
# ======================================

# INTRODUCTION
# The capstone proves you can independently design, build, evaluate, deploy
# and operate an AI system - the core of an AI/ML engineer role - and gives
# you a portfolio project that uses your frontend strengths too.
#
# THEORY
# Requirements (all must be met):
# 1. A real problem and users (e.g. "AI study assistant over my course notes",
#    "support copilot for a SaaS", "job-application helper").
# 2. DATA + ML: a trained or fine-tuned component OR embeddings-based retrieval
#    with measured quality (not only API calls).
# 3. RAG with citations over your own documents; hybrid retrieval.
# 4. At least one AGENT capability with tools, guardrails and confirmation for
#    consequential actions.
# 5. PROMPTS as versioned files with an eval set (>= 30 cases) and a CI
#    quality gate.
# 6. A FastAPI backend, containerised, deployed to a cloud host; a web
#    frontend (React/Next.js - your existing skills) with streaming.
# 7. OBSERVABILITY: traces with versions, cost and latency dashboards, user
#    feedback, drift/quality monitoring.
# 8. DOCUMENTATION: README with architecture diagram, eval results, cost per
#    task, known limitations, and a decision record (prompt vs context vs
#    fine-tuning).
# Milestones: proposal -> data + eval set -> baseline -> RAG -> agent ->
# deployment -> observability -> optimisation -> write-up.
#
# REAL-WORLD ANALOGY
# An architecture graduate's final building: not just drawings, but a
# structure that stands, passes inspection, and people can actually use.
#
# SYNTAX:
#   see the milestone checker below
#
# SMALL WORKING EXAMPLE:
from dataclasses import dataclass, field

@dataclass
class Milestone:
    name: str
    acceptance: list
    done: list = field(default_factory=list)

    def progress(self):
        return len(self.done) / len(self.acceptance)

PLAN = [
    Milestone("Proposal", ["problem statement", "target users", "success metrics", "architecture sketch"]),
    Milestone("Eval set", [">= 30 labelled cases", "unanswerable cases", "grading code"]),
    Milestone("RAG", ["chunking chosen by eval", "hybrid retrieval", "citations", "recall@5 reported"]),
    Milestone("Agent", ["2+ tools", "confirmation gate", "injection test passed"]),
    Milestone("Deployment", ["FastAPI", "Docker image", "cloud URL", "streaming frontend"]),
    Milestone("Operations", ["traces with versions", "cost/latency dashboard", "CI quality gate"]),
    Milestone("Write-up", ["README + diagram", "eval results", "limitations", "decision record"]),
]
PLAN[0].done = ["problem statement", "target users"]

for milestone in PLAN:
    bar = "#" * int(milestone.progress() * 10)
    print(f"{milestone.name:<11} [{bar:<10}] {milestone.progress():.0%}  next: "
          f"{next((a for a in milestone.acceptance if a not in milestone.done), 'complete')}")
total = sum(len(m.acceptance) for m in PLAN)
print(f"overall: {sum(len(m.done) for m in PLAN)}/{total} acceptance criteria")

# EXPLANATION (LINE BY LINE):
# Milestone                  -> a stage with explicit, checkable acceptance criteria.
# PLAN                       -> the capstone broken into milestones in a sensible order.
# progress()                 -> fraction of criteria met; printed as a text progress bar.
# "next:"                    -> the first unmet criterion - always know your next step.
#
# COMMON MISTAKES:
# 1. Choosing a project with no real user or measurable success.
# 2. Building features before an eval set exists.
# 3. Skipping deployment/operations ("it works locally").
# 4. A README with no numbers (quality, cost, latency).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write your capstone proposal as a multi-line string: problem, users, success
# metrics (measurable), data sources, and risks. Mark "Proposal" criteria done.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Draw your architecture as an ASCII diagram (frontend, API, retrieval, vector
# store, LLM, tools, observability) and list every component's technology
# choice with a one-line justification.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build the capstone. Use this file as its tracker: update PLAN as you
# complete criteria, and paste links (repo, deployed URL, dashboard) and final
# metrics here when done.

# YOUR CODE:

