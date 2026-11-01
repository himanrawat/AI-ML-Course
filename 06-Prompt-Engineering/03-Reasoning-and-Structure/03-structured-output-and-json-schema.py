# ======================================
# TOPIC: STRUCTURED OUTPUT AND JSON SCHEMA
# LEVEL: INTERMEDIATE
# ID: prompt-engineering.reasoning.structured-output
# ======================================

# INTRODUCTION
# Applications need data, not prose: fields to store in a database, labels to
# route tickets, arguments for functions. Structured output prompting turns
# model responses into reliable, machine-readable data.
#
# THEORY
# - JSON SCHEMA describes the expected structure: types, required fields,
#   enums (allowed values), formats, nested objects, arrays.
#   {"type": "object", "properties": {"label": {"enum": ["a", "b"]}},
#    "required": ["label"], "additionalProperties": false}
# - Levels of reliability:
#   1. Prompt-only: describe the JSON format and give an example. Usually works,
#      but can include prose, code fences or missing fields.
#   2. NATIVE STRUCTURED OUTPUTS: the API constrains generation to your schema
#      (Claude: output_config with a JSON schema, or client.messages.parse with
#      a Pydantic model). Strongly preferred in production.
#   3. Always VALIDATE in code (Pydantic) - schema-valid is not the same as
#      correct, and business rules go beyond the schema.
# - Design tips: use enums for categories; allow null / "unknown" so the model
#   is not forced to invent values; name fields clearly with descriptions;
#   keep schemas as flat as the task allows.
# - Retry with the validation errors when output is invalid.
#
# REAL-WORLD ANALOGY
# A paper form with labelled boxes and tick-boxes instead of a blank page:
# people fill it in consistently, and you can check every box automatically.
#
# SYNTAX:
#   class Ticket(BaseModel): category: Literal["billing", "bug"]; urgent: bool
#   Ticket.model_json_schema(); Ticket.model_validate_json(text)
#
# SMALL WORKING EXAMPLE:
import json
from typing import Literal

from pydantic import BaseModel, Field, ValidationError
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_llm import complete

class SupportTicket(BaseModel):
    category: Literal["billing", "bug", "account", "other"]
    urgency: Literal["low", "medium", "high"]
    summary: str = Field(description="One sentence, max 20 words")
    order_id: str | None = Field(default=None, description="Order id if mentioned, else null")

schema = SupportTicket.model_json_schema()
message = "URGENT: I was charged 3 times for order #A-1932 and my rent is due tomorrow!"
prompt = f"""Extract a support ticket from the customer message.
Return ONLY a JSON object matching this JSON Schema (no prose, no code fences):
{json.dumps(schema, indent=2)}
Use null for order_id if none is mentioned. Never invent values.

<message>{message}</message>"""

def parse_ticket(text):
    try:
        return SupportTicket.model_validate_json(text), None
    except ValidationError as error:
        return None, [f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in error.errors()]

reply = complete(prompt, offline='{"category": "billing", "urgency": "high", '
                 '"summary": "Customer charged three times for one order.", "order_id": "A-1932"}')
ticket, errors = parse_ticket(reply)
print("valid ticket:", ticket)
bad_reply = '{"category": "payment", "urgency": "very high", "summary": "charged 3x"}'
print("errors to send back in a retry prompt:", parse_ticket(bad_reply)[1])
print("required fields in schema:", schema["required"])

# EXPLANATION (LINE BY LINE):
# SupportTicket (Pydantic)   -> single source of truth for structure AND validation.
# Literal[...]               -> becomes an "enum" in the JSON schema.
# order_id: str | None       -> explicit permission to return null instead of inventing.
# model_json_schema()        -> the JSON Schema we put in the prompt (or pass to the
#                               API's native structured-output option).
# parse_ticket               -> validates; returns readable errors on failure.
# bad_reply                  -> invalid enum values -> errors usable in a retry prompt.
#
# COMMON MISTAKES:
# 1. json.loads on raw replies without handling fences/prose/invalid JSON.
# 2. Forcing a value for every field (the model fabricates).
# 3. Free-text categories instead of enums.
# 4. Trusting schema-valid output as factually correct.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Define a Pydantic model for extracting meeting details (title, date, time,
# attendees list, location or null). Print its JSON schema and validate one
# good and one bad JSON string.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write extract_with_retry(message, model_cls, max_attempts=3): build the
# prompt from the schema, call complete(), validate, and on failure re-prompt
# with the previous output and the validation errors. Test it with a mocked
# complete() that fails once.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Use the Anthropic SDK's native structured outputs (client.messages.parse with
# output_format=SupportTicket) for 10 messages, compare its validity rate and
# accuracy with the prompt-only approach, and design a business-rule check
# beyond the schema (e.g. urgency "high" requires a reason in summary).

# YOUR CODE:

