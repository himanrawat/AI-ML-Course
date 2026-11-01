# ======================================
# TOPIC: GUARDRAILS
# LEVEL: ADVANCED
# ID: prompt-engineering.safety.guardrails
# ======================================

# INTRODUCTION
# Guardrails are the checks around a model call that keep an application safe,
# on-topic and correct - regardless of what the model generates. They turn a
# probabilistic component into a dependable product.
#
# THEORY
# Layers (defence in depth):
# - INPUT guardrails (before the model): length limits, PII detection and
#   redaction, topic/abuse classification, injection signals, rate limits.
# - PROMPT-level: clear scope, rules and refusal behaviour in the system prompt.
# - OUTPUT guardrails (after the model): schema validation, allowed values,
#   PII leakage checks, policy/toxicity checks, grounding checks, length/format,
#   banned claims (e.g. medical/legal promises).
# - ACTION guardrails: permissions, confirmation, allow-lists (see injection).
# - On failure: retry with feedback, fall back to a safe template response,
#   or escalate to a human. Always log the event.
# - Checks can be code (fast, deterministic), small classifier models, or an
#   LLM judge (flexible, slower). Use the cheapest check that's reliable.
# - Measure guardrails too: false positives annoy users; false negatives
#   cause incidents.
#
# REAL-WORLD ANALOGY
# Airport security has several layers - ID check, bag scan, boarding pass
# scan, crew judgement. No single layer is perfect; together they are robust.
#
# SYNTAX:
#   cleaned = input_guard(text); reply = model(cleaned); result = output_guard(reply)
#
# SMALL WORKING EXAMPLE:
import re
from dataclasses import dataclass, field

PII_PATTERNS = {
    "email": r"[\w.+-]+@[\w-]+\.[\w.]+",
    "card": r"\b\d(?:[ -]?\d){12,15}\b",
    "phone": r"\+?\d[\d -]{8,}\d",
}
OFF_TOPIC = ["stock tips", "medical advice", "election"]
BANNED_CLAIMS = [r"guarantee(d)? (returns|approval)", r"100% safe"]

@dataclass
class GuardResult:
    allowed: bool
    text: str
    events: list = field(default_factory=list)

def input_guard(text, max_chars=2000):
    events = []
    if len(text) > max_chars:
        return GuardResult(False, "", ["too_long"])
    for name, pattern in PII_PATTERNS.items():
        if re.search(pattern, text):
            text = re.sub(pattern, f"[{name.upper()} REDACTED]", text)
            events.append(f"redacted_{name}")
    if any(topic in text.lower() for topic in OFF_TOPIC):
        return GuardResult(False, text, events + ["off_topic"])
    return GuardResult(True, text, events)

def output_guard(reply):
    events = [f"banned_claim:{p}" for p in BANNED_CLAIMS if re.search(p, reply, re.IGNORECASE)]
    events += [f"pii_leak:{n}" for n, p in PII_PATTERNS.items() if re.search(p, reply)]
    if events:
        return GuardResult(False, "I can't help with that here. A team member will follow up.", events)
    return GuardResult(True, reply, [])

for message in ["My card 4111 1111 1111 1111 was charged twice, email me at a@b.co",
                "Any stock tips for tomorrow?"]:
    result = input_guard(message)
    print("INPUT ", result)
for reply in ["Your refund was issued and will arrive in 5 days.",
              "Upgrade now - guaranteed approval for every loan!"]:
    print("OUTPUT", output_guard(reply))

# EXPLANATION (LINE BY LINE):
# PII_PATTERNS               -> simple regexes for emails, card numbers and phones
#                               (production systems use dedicated PII detectors).
# input_guard                -> length limit, PII redaction BEFORE the model sees it,
#                               and an off-topic block.
# GuardResult.events         -> every intervention is recorded for logging/metrics.
# output_guard               -> blocks banned promises and leaked PII; returns a safe
#                               fallback message instead of the risky reply.
# The examples show a redacted card/email, an off-topic block, a clean reply and a
# blocked reply.
#
# COMMON MISTAKES:
# 1. Relying on the system prompt as the only guardrail.
# 2. Guardrails that silently fail without logging.
# 3. Over-blocking (users can't get legitimate help) - measure false positives.
# 4. Sending raw PII to third-party APIs when it's not needed.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Add an Indian PAN-number pattern (5 letters, 4 digits, 1 letter) to the PII
# redaction and test it on 3 messages.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Build a test suite of 20 inputs and 10 outputs with expected guard decisions.
# Report false positives and false negatives for each guard and improve one
# rule to reduce errors.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Create a GuardedLLM class wrapping complete(): input guard -> model ->
# schema validation (Pydantic) -> output guard, with one retry that sends the
# guard's feedback to the model, a safe fallback, and structured logging of
# every event. Add an LLM-judge topic check as an optional layer.

# YOUR CODE:

