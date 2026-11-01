# ======================================
# TOPIC: TOOL USE (FUNCTION CALLING)
# LEVEL: ADVANCED
# ID: generative-ai.apis.tool-use
# ======================================

# INTRODUCTION
# Tool use lets a model call YOUR functions - look up an order, query a
# database, search the web - with structured arguments. It is how LLM apps
# connect to real systems and the foundation of agents.
#
# THEORY
# - You declare tools: name, description (when and how to use it) and an
#   input_schema (JSON Schema for the arguments).
# - The model may respond with stop_reason == "tool_use" and one or more
#   tool_use blocks {id, name, input}. It does NOT run anything itself.
# - Your code executes the function, then sends back a user message containing
#   tool_result blocks {tool_use_id, content, is_error}. Return ALL results of
#   parallel tool calls in ONE message.
# - Loop until stop_reason is "end_turn" (final answer).
# - strict: true on a tool guarantees arguments match the schema.
# - Tool descriptions are prompts: say what the tool does, when to use it, and
#   what it returns. Validate arguments and enforce permissions in code.
#
# REAL-WORLD ANALOGY
# A manager (model) who can't access systems directly but can fill in request
# forms (tool calls) for specialists (your functions), then reads their replies.
#
# SYNTAX:
#   tools=[{"name": ..., "description": ..., "input_schema": {...}}]
#   if response.stop_reason == "tool_use": run tools, send tool_result blocks
#
# SMALL WORKING EXAMPLE:
import json
import os

ORDERS = {"A-1001": {"status": "shipped", "eta": "2026-11-04"}, "A-1002": {"status": "processing", "eta": None}}

def get_order_status(order_id):
    if order_id not in ORDERS:
        raise KeyError(f"order {order_id} not found")
    return ORDERS[order_id]

TOOLS = [{
    "name": "get_order_status",
    "description": "Look up the shipping status and ETA of an order by its id (format A-1234). "
                   "Use whenever the user asks where an order is.",
    "input_schema": {"type": "object", "properties": {"order_id": {"type": "string"}},
                     "required": ["order_id"], "additionalProperties": False},
    "strict": True,
}]
HANDLERS = {"get_order_status": get_order_status}

def run_tools(tool_calls):
    results = []
    for call in tool_calls:
        try:
            output = HANDLERS[call["name"]](**call["input"])
            results.append({"type": "tool_result", "tool_use_id": call["id"], "content": json.dumps(output)})
        except Exception as error:
            results.append({"type": "tool_result", "tool_use_id": call["id"],
                            "content": str(error), "is_error": True})
    return {"role": "user", "content": results}

def agent_turn(question):
    from anthropic import Anthropic
    client = Anthropic()
    messages = [{"role": "user", "content": question}]
    while True:
        response = client.messages.create(model="claude-opus-5-5", max_tokens=16000, tools=TOOLS, messages=messages)
        messages.append({"role": "assistant", "content": response.content})
        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")
        calls = [{"id": b.id, "name": b.name, "input": b.input} for b in response.content if b.type == "tool_use"]
        messages.append(run_tools(calls))

simulated_calls = [{"id": "toolu_1", "name": "get_order_status", "input": {"order_id": "A-1001"}},
                   {"id": "toolu_2", "name": "get_order_status", "input": {"order_id": "A-9999"}}]
print(json.dumps(run_tools(simulated_calls), indent=2))
if os.environ.get("COURSE_USE_LLM") == "1":
    print(agent_turn("Where are my orders A-1001 and A-1002?"))

# EXPLANATION (LINE BY LINE):
# TOOLS                      -> declaration: description tells the model WHEN to use it;
#                               input_schema + strict constrains the arguments.
# HANDLERS                   -> maps tool names to real Python functions.
# run_tools                  -> executes every requested call; errors become tool_result
#                               blocks with is_error=True (the model can recover/explain).
#                               All results go back in ONE user message.
# agent_turn                 -> the loop: call model, append its content, run tools while
#                               stop_reason == "tool_use", return the final text.
# simulated_calls            -> shows the exact message shape offline (one success, one error).
#
# COMMON MISTAKES:
# 1. Vague tool descriptions -> wrong tool or missing calls.
# 2. Dropping failed tool calls instead of returning is_error results.
# 3. Splitting parallel tool results across several messages.
# 4. Trusting tool arguments without permission checks (e.g. other users' orders).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Add a second tool cancel_order(order_id, reason) with a schema. Write the
# simulated tool calls and print run_tools() output for a success and an error.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Add authorization: run_tools receives the current user_id and only allows
# access to that user's orders. Make cancel_order require a confirmation flag
# that the app sets only after the user clicks "Confirm".

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# With API access, build a 4-tool assistant (orders, products, returns, FAQ
# search), log every tool call with latency, cap the loop at 8 iterations, and
# evaluate it on 10 scripted user requests for correct tool choice.

# YOUR CODE:

