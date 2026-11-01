# ======================================
# TOPIC: HOW LLMS GENERATE TEXT
# LEVEL: BEGINNER
# ID: prompt-engineering.fundamentals.generation
# ======================================

# INTRODUCTION
# Prompt engineering only makes sense once you know what the model is doing
# with your prompt. An LLM is a next-token predictor: everything it "does" -
# answering, reasoning, writing code - emerges from repeatedly predicting the
# next token given everything before it.
# (Architecture details: 05-Deep-Learning/04-Transformers.)
#
# THEORY
# - The prompt is tokenized; the model outputs a probability distribution
#   over its vocabulary for the NEXT token; one token is chosen; it is
#   appended; repeat until a stop condition (end token, max_tokens).
# - The model has no hidden notebook between calls: each API call sees only
#   the text (and images/tool results) you send. "Memory" in chat apps is the
#   app re-sending the conversation.
# - Training stages shape behaviour:
#   1. PRETRAINING on huge text: learns language, facts, patterns.
#   2. INSTRUCTION TUNING: learns to follow instructions and chat formats.
#   3. PREFERENCE TUNING (e.g. RLHF): learns to be helpful, honest, harmless.
#   So the model is strongly biased toward continuing your text in the way a
#   helpful assistant typically would.
# - IN-CONTEXT LEARNING: examples and information in the prompt change the
#   predicted distribution without changing the model's weights.
# - Sampling: decoding can pick the most likely token or sample from the
#   distribution (temperature/top-p conceptually control randomness). Many
#   current APIs, including the latest Claude models, manage sampling
#   internally and do not accept these parameters - you steer outputs with
#   clear instructions, examples and output constraints instead.
# - Why prompts matter: an ambiguous prompt leaves many plausible
#   continuations; a specific prompt concentrates probability on what you want.
#
# REAL-WORLD ANALOGY
# An extremely well-read improv actor: given a scene description (prompt), they
# continue the scene in the most fitting way. A vague scene gets a generic
# performance; a detailed one gets exactly the character you wanted.
#
# SYNTAX:
#   next_token_distribution = model(prompt_tokens)
#   token = choose(distribution); prompt_tokens.append(token)
#
# SMALL WORKING EXAMPLE:
import numpy as np

rng = np.random.default_rng(0)
next_token_scores = {
    "The capital of France is": {"Paris": 9.0, "a": 4.0, "located": 3.5, "Lyon": 1.0},
    "Write something about France:": {"France": 3.0, "The": 2.9, "Paris": 2.8, "Bonjour": 2.6, "Wine": 2.5},
}

def distribution(scores, temperature=1.0):
    tokens = list(scores)
    logits = np.array([scores[t] for t in tokens]) / temperature
    probs = np.exp(logits - logits.max())
    return tokens, probs / probs.sum()

for prompt, scores in next_token_scores.items():
    tokens, probs = distribution(scores)
    entropy = -np.sum(probs * np.log2(probs))
    print(f"{prompt!r}")
    print("   ", {t: round(float(p), 3) for t, p in zip(tokens, probs)}, f"entropy={entropy:.2f} bits")
tokens, probs = distribution(next_token_scores["Write something about France:"], temperature=0.3)
print("same vague prompt, sharper sampling:", {t: round(float(p), 2) for t, p in zip(tokens, probs)})
samples = rng.choice(tokens, size=8, p=distribution(next_token_scores["Write something about France:"])[1])
print("8 samples from the vague prompt:", samples.tolist())

# EXPLANATION (LINE BY LINE):
# next_token_scores        -> made-up logits a model might produce for two prompts.
# distribution()           -> softmax over the scores, with optional temperature.
# Specific prompt          -> almost all probability on "Paris" (low entropy).
# Vague prompt             -> probability spread over many tokens (high entropy):
#                             many different continuations are equally "correct".
# Low temperature          -> sharper, but it only picks among the SAME vague
#                             options - it doesn't make the request clearer.
# rng.choice(...)          -> sampling: the vague prompt gives varied first words.
# Lesson: improve the prompt's specificity, not just the randomness settings.
#
# COMMON MISTAKES:
# 1. Thinking the model "remembers" previous API calls.
# 2. Treating the model as a database lookup rather than a predictor.
# 3. Trying to fix vague prompts with sampling settings.
# 4. Assuming the same prompt always gives the same output.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write two prompts asking for a product description: one vague, one specific
# (audience, length, tone, must-mention features). In comments, predict how
# the space of possible outputs differs. If you have API access, run both
# 3 times each with course_llm.complete and compare the variety.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Simulate a "conversation memory": write a list-of-messages structure for a
# 3-turn chat and a function that builds the full payload sent on turn 3.
# Explain in comments why token usage grows each turn.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Using the tiny GPT from 05-Deep-Learning (or the score tables above),
# demonstrate in-context learning conceptually: show how adding two examples
# to a prompt would change which continuation is most likely. Then write a
# one-paragraph explanation of why few-shot examples work without changing
# model weights.

# YOUR CODE:

