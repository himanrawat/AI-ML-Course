# ======================================
# TOPIC: AGENT MEMORY AND PLANNING
# LEVEL: ADVANCED
# ID: rag-agents.agents.memory-planning
# ======================================

# INTRODUCTION
# Longer tasks need agents that plan before acting and remember what matters
# across steps and sessions - without overflowing the context window.
#
# THEORY
# PLANNING:
# - PLAN-AND-EXECUTE: first produce a numbered plan, then execute steps,
#   revising the plan when results change it.
# - REFLECTION: after a step or at the end, critique the result and retry
#   if it fails a check.
# - Decomposition into sub-agents for independent sub-tasks (each with its own
#   focused context).
# MEMORY:
# - SHORT-TERM: the conversation/working context of the current run.
# - Context management: summarise or clear old tool results, keep a
#   scratchpad of key facts.
# - LONG-TERM: facts stored outside the model (files, a database, a vector
#   store) and retrieved when relevant - user preferences, past decisions.
# - Memory needs governance: what to store, how long, user consent, how to
#   correct or delete it.
#
# REAL-WORLD ANALOGY
# A project manager with a to-do list (plan), a notebook of decisions
# (long-term memory) and only today's papers on the desk (working context).
#
# SYNTAX:
#   plan = make_plan(goal); for step in plan: result = act(step); memory.save(...)
#
# SMALL WORKING EXAMPLE:
import json
import tempfile
from pathlib import Path

class LongTermMemory:
    def __init__(self, path):
        self.path = Path(path)
        self.facts = json.loads(self.path.read_text()) if self.path.exists() else []

    def remember(self, fact, tags):
        self.facts.append({"fact": fact, "tags": tags})
        self.path.write_text(json.dumps(self.facts, indent=1))

    def recall(self, tags):
        return [f["fact"] for f in self.facts if set(tags) & set(f["tags"])]

class WorkingContext:
    def __init__(self, max_items=4):
        self.items, self.max_items, self.summary = [], max_items, []

    def add(self, item):
        self.items.append(item)
        if len(self.items) > self.max_items:
            oldest = self.items.pop(0)
            self.summary.append(oldest[:40] + "...")

    def render(self):
        return {"summary_of_older_steps": self.summary, "recent": self.items}

memory = LongTermMemory(Path(tempfile.mkdtemp()) / "memory.json")
memory.remember("User prefers answers in bullet points", ["style"])
memory.remember("Project uses PostgreSQL 16", ["project", "database"])
plan = ["Inspect slow query logs", "Identify missing indexes", "Propose index changes", "Write summary"]
context = WorkingContext()
context.add(f"Relevant memory: {memory.recall(['database', 'style'])}")
for number, step in enumerate(plan, start=1):
    context.add(f"Step {number} '{step}': done (simulated result for {step.lower()})")
print(json.dumps(context.render(), indent=1))
reloaded = LongTermMemory(memory.path)
print("memory survives restart:", reloaded.recall(["project"]))

# EXPLANATION (LINE BY LINE):
# LongTermMemory             -> facts with tags persisted to a JSON file; recall by tag
#                               (a vector store would allow semantic recall).
# WorkingContext             -> keeps only the latest max_items in full; older items are
#                               compressed into a summary list (context management).
# plan                       -> an explicit plan the agent executes step by step.
# context.render()           -> what would be sent to the model: summary + recent items.
# reloaded                   -> long-term memory persists across sessions.
#
# COMMON MISTAKES:
# 1. Keeping every tool result in context forever.
# 2. Storing everything as "memory" (noise, privacy risk).
# 3. Plans that are never revised when a step fails.
# 4. No way for users to see or delete what the agent remembers.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Add forget(tag) and update(old_fact, new_fact) methods to LongTermMemory and
# test them. Why is the ability to forget important?

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Implement plan-and-execute with re-planning: if a simulated step fails, ask a
# (mocked) planner for a revised plan that includes a recovery step. Log the
# original and revised plans.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Replace tag-based recall with embedding-based recall (07-Generative-AI
# embeddings), add an importance score and recency decay, and build a
# reflection step that decides which facts from a finished run are worth
# remembering (API access or mocked).

# YOUR CODE:

