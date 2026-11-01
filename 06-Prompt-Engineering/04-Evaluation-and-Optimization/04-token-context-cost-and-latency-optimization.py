# ======================================
# TOPIC: TOKEN, CONTEXT, COST AND LATENCY OPTIMIZATION
# LEVEL: ADVANCED
# ID: prompt-engineering.evaluation.cost-latency
# ======================================

# INTRODUCTION
# A prompt that works but costs too much or takes 20 seconds may still be
# unusable. Production prompt engineering balances quality, cost and latency -
# and measures all three.
#
# THEORY
# COST levers (biggest wins first):
# - PROMPT CACHING: keep long stable content (system prompt, documents, tool
#   definitions) as an identical PREFIX; cached input tokens are much cheaper.
#   Anything that changes (timestamps, user data) goes AFTER the stable part.
# - Send only RELEVANT context (retrieve the top passages instead of whole docs).
# - Control output length: ask for concise formats; set a sensible max_tokens.
# - Choose the right model and effort level per task; measure quality first.
# - BATCH APIs for non-urgent work are typically ~50% cheaper.
# LATENCY levers:
# - Output tokens dominate latency: shorter outputs are faster.
# - STREAMING shows the first tokens immediately (better perceived latency).
# - Parallelise independent calls; cache identical requests in your app.
# - Lower effort / smaller models for simple steps in a chain.
# CONTEXT WINDOW management:
# - Summarise or trim old conversation turns; keep a running summary.
# - Put key instructions where they're easy to find; avoid duplicating content.
# Always measure cost per COMPLETED task, not per request.
#
# REAL-WORLD ANALOGY
# Shipping parcels: reuse the same pre-printed labels (caching), don't ship
# the whole warehouse when the customer ordered one item (relevant context),
# and use express delivery only when it matters (model/effort choice).
#
# SYNTAX:
#   messages = [stable_prefix ..., variable_suffix]
#   cost = cached_in * cache_price + new_in * input_price + out * output_price
#
# SMALL WORKING EXAMPLE:
INPUT, OUTPUT, CACHE_READ = 4.00, 20.00, 0.20

def request_cost(stable_tokens, variable_tokens, output_tokens, cached):
    cached_tokens = stable_tokens if cached else 0
    fresh = variable_tokens + (0 if cached else stable_tokens)
    return (cached_tokens * CACHE_READ + fresh * INPUT + output_tokens * OUTPUT) / 1e6

scenarios = {
    "baseline: full manual + verbose answer": (40_000, 200, 900, False),
    "prompt caching for the manual": (40_000, 200, 900, True),
    "+ concise answer format": (40_000, 200, 250, True),
    "retrieve top 5 sections instead": (3_000, 200, 250, False),
}
for name, (stable, variable, output, cached) in scenarios.items():
    per = request_cost(stable, variable, output, cached)
    print(f"{name:<40} ${per:.4f}/request  ${per * 50_000:>9,.2f} per 50k requests")

def trim_history(messages, max_turns=6, summary=None):
    if len(messages) <= max_turns:
        return messages
    recent = messages[-max_turns:]
    note = summary or f"[{len(messages) - max_turns} earlier messages summarised: user is debugging a CSV export]"
    return [{"role": "user", "content": note}, {"role": "assistant", "content": "Understood."}] + recent

history = [{"role": "user" if i % 2 == 0 else "assistant", "content": f"turn {i}"} for i in range(14)]
print("history turns:", len(history), "->", len(trim_history(history)))

# EXPLANATION (LINE BY LINE):
# Prices per million tokens (Claude Opus 5.5 at the time of writing; cache
# reads are ~5% of the normal input price). Always check current pricing.
# request_cost              -> splits input into cached prefix and fresh tokens.
# Scenarios                 -> caching a 40k-token manual cuts cost dramatically;
#                              shorter answers cut output cost; retrieval avoids
#                              sending the manual at all (but needs good retrieval).
# trim_history              -> keeps the last N turns and replaces older ones with a
#                              summary, preserving the user/assistant alternation.
#
# COMMON MISTAKES:
# 1. Putting a timestamp or user name at the START of the system prompt (breaks
#    caching for every request).
# 2. Optimising cost before quality is measured.
# 3. Ignoring output length - the most expensive and slowest tokens.
# 4. Unbounded conversation history.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Reorder this prompt to be cache-friendly and explain why:
# [current time] + [user name] + [5,000-token product manual] + [question].

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write a CostTracker that records (model, input, cached, output tokens,
# latency) per call, and prints cost per completed task, p50/p95 latency, and
# cache hit rate. Feed it 50 simulated calls.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# With API access, send the same long system prompt 3 times with
# cache_control enabled and read usage.cache_creation_input_tokens and
# usage.cache_read_input_tokens; then measure time-to-first-token with
# streaming vs total latency without streaming. Report the numbers.

# YOUR CODE:

