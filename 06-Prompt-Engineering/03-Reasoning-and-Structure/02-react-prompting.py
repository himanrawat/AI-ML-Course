# ======================================
# TOPIC: REACT PROMPTING (REASON + ACT)
# LEVEL: INTERMEDIATE
# ID: prompt-engineering.reasoning.react
# ======================================

# INTRODUCTION
# Models alone can't look things up or run calculations reliably. ReAct
# interleaves reasoning with ACTIONS (tool calls) and OBSERVATIONS (tool
# results). It is the conceptual foundation of AI agents.
#
# THEORY
# - Loop:  Thought -> Action (tool + input) -> Observation (result) -> ...
#          -> Final Answer.
# - The model decides WHICH tool to use and WHEN to stop; your code executes the
#   tool and feeds the observation back.
# - Original ReAct used a text format the program parsed. Modern APIs offer
#   native TOOL USE (function calling): you declare tools with JSON schemas and
#   the model returns structured tool calls - more reliable than parsing text.
#   The reasoning pattern is the same.
# - Prompt ingredients: tool descriptions (what each does, when to use it,
#   input format), the loop format, a stop condition, and a step limit.
# - Failure modes: invented observations (the model writes the tool result
#   itself), loops, wrong tool choice. Mitigate with stop sequences/native tool
#   calling, step limits and clear tool descriptions.
#
# REAL-WORLD ANALOGY
# A detective's notebook: "I think the butler is lying (thought). I'll check
# the train timetable (action). The last train left at 9pm (observation).
# So his alibi fails (thought)..."
#
# SYNTAX:
#   Thought: ... / Action: tool_name[input] / Observation: ... / Final Answer: ...
#
# SMALL WORKING EXAMPLE:
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_llm import complete

TOOLS = {
    "lookup_population": lambda city: {"tokyo": "37.1 million", "delhi": "34.7 million"}.get(city.lower(), "unknown"),
    "calculate": lambda expression: str(round(eval(expression, {"__builtins__": {}}), 3)),
}
SYSTEM = """Answer questions using tools. Available tools:
- lookup_population[city]: current metro population of a city.
- calculate[expression]: evaluates an arithmetic expression like 37.1 - 34.7.
Use this format, one step per reply:
Thought: <your reasoning>
Action: <tool>[<input>]
When you know the answer, reply with:
Final Answer: <answer>
Never write an Observation yourself - it will be provided."""

SCRIPTED = iter([
    "Thought: I need Tokyo's population.\nAction: lookup_population[Tokyo]",
    "Thought: Now Delhi's.\nAction: lookup_population[Delhi]",
    "Thought: Subtract the two numbers.\nAction: calculate[37.1 - 34.7]",
    "Final Answer: Tokyo's metro area has about 2.4 million more people than Delhi's.",
])

def run_react(question, max_steps=6):
    messages = [{"role": "user", "content": question}]
    for _ in range(max_steps):
        reply = complete(system=SYSTEM, messages=messages, offline=lambda _: next(SCRIPTED))
        print(reply)
        messages.append({"role": "assistant", "content": reply})
        if "Final Answer:" in reply:
            return reply.split("Final Answer:", 1)[1].strip()
        action = re.search(r"Action:\s*(\w+)\[(.*?)\]", reply)
        if not action or action.group(1) not in TOOLS:
            observation = "Error: use one of the listed tools in the Action format."
        else:
            observation = TOOLS[action.group(1)](action.group(2))
        print(f"Observation: {observation}")
        messages.append({"role": "user", "content": f"Observation: {observation}"})
    return "Stopped: step limit reached."

print("ANSWER:", run_react("How many more people live in Tokyo's metro area than Delhi's?"))

# EXPLANATION (LINE BY LINE):
# TOOLS                      -> Python functions the model can request (toy data).
#                               eval with no builtins is only acceptable in a toy demo.
# SYSTEM                     -> tool descriptions + exact loop format + "never write an
#                               Observation yourself" (prevents invented results).
# SCRIPTED                   -> offline replies imitating a model, step by step.
# run_react                  -> call model, parse Action, run tool, append Observation
#                               as the next user message, repeat.
# max_steps                  -> a hard stop prevents infinite loops.
# Unknown tool / bad format  -> returns an error observation so the model can recover.
#
# COMMON MISTAKES:
# 1. Letting the model generate observations (hallucinated tool results).
# 2. No step limit.
# 3. Vague tool descriptions (wrong tool choice).
# 4. Using eval on model output in real systems (code execution risk).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Add a third tool get_weather[city] (fake data) and write the Thought/Action/
# Observation trace you would expect for "Should I carry an umbrella in Pune?"

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Replace eval in calculate with a safe arithmetic parser using the ast module
# (allow only numbers and + - * / parentheses). Add tests showing malicious
# input like "__import__('os')" is rejected.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Re-implement the same agent with the Anthropic API's native tool use: define
# tools with JSON input_schema, loop while stop_reason == "tool_use", return
# tool_result blocks. Compare robustness with the text-parsing version
# (API access needed to run; design and code it either way).

# YOUR CODE:

