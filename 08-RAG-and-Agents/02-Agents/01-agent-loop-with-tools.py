# ======================================
# TOPIC: THE AGENT LOOP
# LEVEL: ADVANCED
# ID: rag-agents.agents.agent-loop
# ======================================

# INTRODUCTION
# An agent is an LLM that decides its own next steps: which tool to call, with
# what input, and when it is done. Agents handle open-ended tasks that a fixed
# pipeline can't anticipate - at the cost of predictability.
#
# THEORY
# - Agent = model + tools + a LOOP + state (+ optional memory and planning).
#   while not done: model chooses action -> code executes tool -> result is
#   added to context -> repeat.
# - Workflows vs agents: a WORKFLOW follows code-defined steps (chains, routing);
#   an AGENT lets the model choose the path. Prefer workflows when the steps
#   are known - they are cheaper, faster and easier to test.
# - Essentials for reliable agents:
#   * Clear, well-described tools with validated inputs and helpful errors.
#   * Stop conditions: final answer, max iterations, budget/time limits.
#   * Observability: log every step (thought, tool, input, output, latency).
#   * Safety: least privilege, confirmation for consequential actions,
#     treat tool outputs as untrusted (prompt injection).
# - Native tool use (07-Generative-AI/01-LLM-APIs/02) is the production way to
#   implement the loop; SDK "tool runners" can drive it for you.
#
# REAL-WORLD ANALOGY
# A new employee given a goal and access to some systems: they decide what to
# look up, check results, and report back - within the permissions and time
# you allow.
#
# SYNTAX:
#   for step in range(max_steps): action = decide(state); state += execute(action)
#
# SMALL WORKING EXAMPLE:
import json
import time
from dataclasses import dataclass, field

FILES = {"notes/todo.md": "- fix login bug\n- write tests", "notes/ideas.md": "- dark mode\n- export to PDF"}

def list_files():
    return sorted(FILES)

def read_file(path):
    if path not in FILES:
        raise FileNotFoundError(path)
    return FILES[path]

TOOLS = {"list_files": list_files, "read_file": read_file}

@dataclass
class AgentRun:
    goal: str
    max_steps: int = 6
    log: list = field(default_factory=list)

    def run(self, policy):
        observations = []
        for step in range(1, self.max_steps + 1):
            action = policy(self.goal, observations)
            if action["type"] == "final":
                self.log.append({"step": step, "final": action["answer"]})
                return action["answer"]
            start = time.perf_counter()
            try:
                result = TOOLS[action["tool"]](**action.get("input", {}))
                status = "ok"
            except Exception as error:
                result, status = f"{type(error).__name__}: {error}", "error"
            self.log.append({"step": step, "tool": action["tool"], "input": action.get("input", {}),
                             "status": status, "ms": round((time.perf_counter() - start) * 1000, 2)})
            observations.append({"tool": action["tool"], "result": result})
        return "Stopped: max steps reached"

def scripted_policy(goal, observations):
    """Stand-in for the model's decisions (with API access, this is a model call)."""
    if not observations:
        return {"type": "tool", "tool": "list_files"}
    if len(observations) == 1:
        return {"type": "tool", "tool": "read_file", "input": {"path": "notes/todo.md"}}
    if len(observations) == 2:
        return {"type": "tool", "tool": "read_file", "input": {"path": "notes/missing.md"}}
    return {"type": "final", "answer": "Open tasks: fix login bug, write tests."}

agent = AgentRun("Summarise my open tasks")
print("answer:", agent.run(scripted_policy))
print(json.dumps(agent.log, indent=1))

# EXPLANATION (LINE BY LINE):
# FILES / TOOLS              -> a sandboxed toy file system the agent can explore.
# AgentRun.run               -> the loop: ask the policy for an action, execute tools,
#                               catch errors as observations, stop on "final" or max_steps.
# log                        -> every step recorded with status and latency (observability).
# scripted_policy            -> replays a model's choices offline, including a tool error
#                               (missing file) the agent survives.
# With a real model, policy() sends goal + observations and parses a tool_use block.
#
# COMMON MISTAKES:
# 1. Building an agent when a fixed workflow would do.
# 2. No max_steps or budget (runaway loops and costs).
# 3. Crashing on tool errors instead of returning them to the model.
# 4. Giving agents write/delete tools without confirmation.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Add a search_files(keyword) tool and write a new scripted_policy that finds
# all files mentioning "PDF". Print the log.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Replace scripted_policy with a real model policy using native tool use
# (API access): convert TOOLS to tool schemas, keep the message history, and
# map tool_use blocks to actions. Keep max_steps and logging.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Add a write_file tool that requires human confirmation (input() prompt or a
# confirm callback), a token/cost budget that stops the run, and a final
# report of steps, tools used, errors and total latency. Test with 3 goals.

# YOUR CODE:

