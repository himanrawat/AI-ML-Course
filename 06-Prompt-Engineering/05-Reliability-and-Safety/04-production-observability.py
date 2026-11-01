# ======================================
# TOPIC: PRODUCTION PROMPT OBSERVABILITY
# LEVEL: ADVANCED
# ID: prompt-engineering.safety.observability
# ======================================

# INTRODUCTION
# Once a prompt is live, you need to see what it's doing: which inputs it gets,
# how it answers, how much it costs, how fast it is, and when it starts
# failing. Observability turns user complaints into data you can act on.
#
# THEORY
# What to record per LLM call (a TRACE):
# - ids: request id, user/session id (pseudonymised), parent trace for chains.
# - prompt template name + version, model, settings.
# - inputs/outputs (or hashes/samples if sensitive - follow privacy rules).
# - tokens (input, cached, output), cost, latency (time to first token, total),
#   stop_reason, errors and retries, guardrail events, tool calls.
# - user feedback (thumbs, edits, escalations) linked to the trace.
# Metrics and dashboards: volume, error rate, p50/p95 latency, cost per task,
# guardrail trigger rate, feedback rate, eval scores over time.
# Alerts: error spikes, latency or cost jumps, sudden change in output length
# or label distribution (DRIFT - inputs change, or a model update changes
# behaviour).
# Feedback loop: sample production traces -> label failures -> add them to the
# eval set -> improve the prompt -> re-evaluate -> roll out.
# Tools: structured logs + OpenTelemetry tracing, or LLM observability
# platforms (e.g. Langfuse, LangSmith, PostHog LLM analytics, Arize).
#
# REAL-WORLD ANALOGY
# An aircraft's flight recorder plus the control tower's radar: one records
# every detail for investigation, the other watches all flights live and
# raises alarms early.
#
# SYNTAX:
#   with trace("summarize", prompt_version="1.3.0") as t: t.record(tokens=..., latency=...)
#
# SMALL WORKING EXAMPLE:
import json
import random
import statistics
import time
import uuid
from contextlib import contextmanager

TRACES = []

@contextmanager
def trace(operation, prompt_version, model="claude-opus-5-5"):
    record = {"trace_id": uuid.uuid4().hex[:8], "operation": operation,
              "prompt_version": prompt_version, "model": model, "status": "ok"}
    start = time.perf_counter()
    try:
        yield record
    except Exception as error:
        record["status"] = "error"
        record["error"] = type(error).__name__
    finally:
        record["latency_ms"] = round((time.perf_counter() - start) * 1000, 1)
        TRACES.append(record)

random.seed(3)
for i in range(60):
    version = "1.3.0" if i < 30 else "1.4.0"
    with trace("classify_ticket", version) as t:
        time.sleep(random.uniform(0.001, 0.004))
        t["input_tokens"] = random.randint(300, 500)
        t["output_tokens"] = random.randint(5, 15) if version == "1.3.0" else random.randint(40, 90)
        t["label"] = random.choice(["billing", "bug", "other"] if version == "1.3.0" else ["other"] * 3 + ["bug"])
        if random.random() < 0.05:
            raise TimeoutError

def summarize(version):
    rows = [t for t in TRACES if t["prompt_version"] == version]
    ok = [t for t in rows if t["status"] == "ok"]
    latencies = sorted(t["latency_ms"] for t in rows)
    labels = {l: sum(t.get("label") == l for t in ok) / len(ok) for l in ("billing", "bug", "other")}
    return {"calls": len(rows), "error_rate": round(1 - len(ok) / len(rows), 3),
            "p95_ms": latencies[int(0.95 * (len(latencies) - 1))],
            "avg_output_tokens": round(statistics.mean(t["output_tokens"] for t in ok), 1),
            "label_share": {k: round(v, 2) for k, v in labels.items()}}

print(json.dumps(TRACES[0]))
before, after = summarize("1.3.0"), summarize("1.4.0")
print("1.3.0:", before)
print("1.4.0:", after)
if after["avg_output_tokens"] > 2 * before["avg_output_tokens"] or after["label_share"]["other"] > 0.5:
    print("ALERT: v1.4.0 output length / label distribution drifted - investigate before full rollout")

# EXPLANATION (LINE BY LINE):
# trace()                    -> a context manager that records ids, version, model,
#                               status, errors and latency for every call.
# Simulated traffic          -> 30 calls per prompt version; v1.4.0 has a hidden bug:
#                               longer outputs and almost everything labelled "other".
# summarize(version)         -> error rate, p95 latency, average output tokens and the
#                               label distribution per prompt version.
# Drift alert                -> compares versions and flags suspicious changes that
#                               no single request would reveal.
#
# COMMON MISTAKES:
# 1. Logging prompts without the template VERSION (can't attribute regressions).
# 2. Logging raw sensitive data without consent or retention rules.
# 3. Only tracking errors, not quality signals like label distribution.
# 4. Collecting feedback but never feeding it back into the eval set.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# List the fields you would log for a RAG question-answering call and mark
# which ones are sensitive and how you'd protect them.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write the traces to a JSONL file and build a small report script that reads
# it and prints per-version metrics, the 5 slowest traces, and all errors.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Implement a drift detector for label distributions: compare the last N
# traces with a baseline window using the population stability index (PSI)
# or a chi-square test, and raise an alert above a threshold. Test it on
# simulated stable and drifting traffic.

# YOUR CODE:

