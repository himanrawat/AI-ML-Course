# ======================================
# TOPIC: CONTEXT WINDOWS, TOKENS AND COST
# LEVEL: BEGINNER
# ID: prompt-engineering.fundamentals.context-tokens
# ======================================

# INTRODUCTION
# Every prompt competes for a limited budget: the context window. Tokens also
# determine cost and latency. Knowing how to count and budget them is a
# practical prompt-engineering skill.
#
# THEORY
# - CONTEXT WINDOW: the maximum number of tokens the model can consider in one
#   request - system prompt + conversation + documents + tool results + the
#   OUTPUT it generates. Current Claude models offer up to 1M tokens.
# - INPUT tokens (what you send) and OUTPUT tokens (what it writes) are priced
#   separately; output tokens are usually several times more expensive and
#   are generated one by one (they dominate latency).
# - max_tokens caps the output length; if it is hit, the answer is cut off
#   (stop_reason = "max_tokens").
# - Bigger context is not free: more cost, more latency, and models can pay
#   less attention to information buried in the middle of very long inputs
#   ("lost in the middle"). Put key instructions and questions where they are
#   easy to find (long documents first, the question at the end works well).
# - Count tokens with the provider's token-counting endpoint
#   (client.messages.count_tokens) instead of guessing; rough English rule:
#   ~4 characters per token.
# - Prompt caching: repeated identical prefixes (e.g. a long system prompt)
#   can be cached and billed at a lower rate.
#
# REAL-WORLD ANALOGY
# A desk of fixed size: the more papers you spread out, the harder it is to
# find the important one - and every sheet costs money to print.
#
# SYNTAX:
#   estimated_tokens = len(text) / 4
#   cost = input_tokens / 1e6 * input_price + output_tokens / 1e6 * output_price
#
# SMALL WORKING EXAMPLE:
PRICES_PER_MILLION = {"claude-opus-5-5": (4.00, 20.00), "claude-sonnet-5-5": (2.00, 10.00),
                      "claude-haiku-5-5": (0.10, 0.50)}

def estimate_tokens(text):
    return max(1, round(len(text) / 4))

def estimate_cost(model, input_tokens, output_tokens):
    input_price, output_price = PRICES_PER_MILLION[model]
    return input_tokens / 1e6 * input_price + output_tokens / 1e6 * output_price

system_prompt = "You are a support assistant for Acme. Answer using the policy below.\n" + "Policy text. " * 400
question = "Can I return an opened item after 20 days?"
input_tokens = estimate_tokens(system_prompt + question)
print("estimated input tokens:", input_tokens)
for model in PRICES_PER_MILLION:
    per_request = estimate_cost(model, input_tokens, 300)
    print(f"{model:<18} ${per_request:.5f} per request | ${per_request * 100_000:,.2f} per 100k requests")

def fit_to_budget(documents, budget_tokens):
    chosen, used = [], 0
    for doc in sorted(documents, key=lambda d: d["relevance"], reverse=True):
        cost = estimate_tokens(doc["text"])
        if used + cost <= budget_tokens:
            chosen.append(doc["id"])
            used += cost
    return chosen, used

docs = [{"id": i, "relevance": r, "text": "x" * n} for i, (r, n) in
        enumerate([(0.9, 4000), (0.4, 20000), (0.8, 8000), (0.7, 2000)])]
print("documents that fit a 3,000-token budget:", fit_to_budget(docs, 3000))

# EXPLANATION (LINE BY LINE):
# PRICES_PER_MILLION          -> (input, output) USD per million tokens. Prices
#                                change - always check the provider's pricing page.
# estimate_tokens             -> rough ~4 chars/token estimate (use count_tokens in
#                                real code).
# A 5,000+ character system prompt is resent on EVERY request -> multiply by volume.
# estimate_cost(..., 300)     -> 300 output tokens assumed per answer.
# fit_to_budget               -> context management: include the most relevant
#                                documents until the token budget is used.
#
# COMMON MISTAKES:
# 1. Forgetting that output tokens also consume the context window.
# 2. Dumping every document into the prompt "because the window is big".
# 3. Setting max_tokens too low and getting truncated answers.
# 4. Ignoring the cost of a long system prompt multiplied by traffic.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Estimate tokens and cost for summarising a 20-page document (~500 words per
# page) into 200 words with each model in PRICES_PER_MILLION.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write a ConversationBudget class that stores messages, estimates total
# tokens, and when a limit is exceeded drops the oldest turns (never the
# system prompt) or replaces them with a short summary placeholder.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# If you have API access, use client.messages.count_tokens to measure the
# true token count of 5 texts (English prose, code, JSON, Hindi text, emoji)
# and compare with the chars/4 estimate. Otherwise, write the code and explain
# in comments which text types you expect to deviate most and why.

# YOUR CODE:

