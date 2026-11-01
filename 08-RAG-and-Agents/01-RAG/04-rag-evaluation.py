# ======================================
# TOPIC: EVALUATING RAG SYSTEMS
# LEVEL: ADVANCED
# ID: rag-agents.rag.evaluation
# ======================================

# INTRODUCTION
# A RAG answer can fail because retrieval missed the right chunk OR because the
# model misused a correct chunk. Evaluating each stage separately tells you
# what to fix.
#
# THEORY
# RETRIEVAL metrics (need labelled relevant chunks per question):
# - RECALL@k: fraction of questions whose relevant chunk is in the top k.
# - MRR (mean reciprocal rank): 1/rank of the first relevant chunk, averaged.
# - Precision@k / NDCG for multiple relevant chunks.
# GENERATION metrics:
# - FAITHFULNESS (groundedness): are all claims supported by retrieved text?
# - ANSWER CORRECTNESS / relevance: does it answer the question correctly?
# - CITATION accuracy: do cited sources actually support the claims?
# - ABSTENTION: does it say "I don't know" for unanswerable questions?
# Methods: code checks where possible, LLM-as-judge with rubrics, human review
# on samples. Tools like Ragas or DeepEval package these metrics.
# Build the eval set from real user questions; include unanswerable ones.
#
# REAL-WORLD ANALOGY
# Diagnosing a bad meal: was it the ingredients the shopper brought
# (retrieval) or the cooking (generation)? Taste each separately.
#
# SYNTAX:
#   recall_at_k = mean(relevant in retrieved[:k] for each question)
#
# SMALL WORKING EXAMPLE:
EVAL = [
    {"q": "How many leave days carry over?", "relevant": "leave", "retrieved": ["leave", "remote", "health"],
     "answer": "Up to 5 days [leave].", "expected_fact": "5", "answerable": True},
    {"q": "What's the learning budget?", "relevant": "learning", "retrieved": ["equipment", "learning", "leave"],
     "answer": "1,000 USD per year [learning].", "expected_fact": "1,000", "answerable": True},
    {"q": "Can I bring my dog to the office?", "relevant": None, "retrieved": ["remote", "equipment", "leave"],
     "answer": "Yes, pets are welcome on Fridays [remote].", "expected_fact": None, "answerable": False},
    {"q": "Does health insurance cover parents?", "relevant": "health", "retrieved": ["remote", "leave", "equipment"],
     "answer": "I don't know based on the documents.", "expected_fact": None, "answerable": True},
]

def retrieval_metrics(rows, k=3):
    answerable = [r for r in rows if r["relevant"]]
    recall = sum(r["relevant"] in r["retrieved"][:k] for r in answerable) / len(answerable)
    mrr = sum(1 / (r["retrieved"].index(r["relevant"]) + 1) if r["relevant"] in r["retrieved"] else 0
              for r in answerable) / len(answerable)
    return {"recall@3": round(recall, 2), "mrr": round(mrr, 2)}

def generation_checks(row):
    abstained = "don't know" in row["answer"].lower()
    if not row["answerable"]:
        return "ok (abstained)" if abstained else "HALLUCINATION: should have abstained"
    if row["relevant"] not in row["retrieved"]:
        return "retrieval miss -> " + ("ok (abstained)" if abstained else "unsupported answer")
    return "ok" if row["expected_fact"] in row["answer"] else "wrong answer despite good retrieval"

print("retrieval:", retrieval_metrics(EVAL))
for row in EVAL:
    print(f"{row['q']:<40} {generation_checks(row)}")

# EXPLANATION (LINE BY LINE):
# EVAL rows                  -> question, the relevant chunk id (None if unanswerable),
#                               what was retrieved, the generated answer, a key fact.
# retrieval_metrics          -> recall@3 and MRR over answerable questions only.
# generation_checks          -> classifies each failure by STAGE: hallucination on an
#                               unanswerable question, retrieval miss, or generation error.
# Row 4                      -> retrieval failed, but the model correctly abstained -
#                               fix retrieval, not the prompt.
# Row 3                      -> the model invented an answer: a generation/prompt problem.
#
# COMMON MISTAKES:
# 1. Measuring only end-to-end answer quality.
# 2. No unanswerable questions in the eval set.
# 3. Trusting LLM-judge faithfulness scores without spot checks.
# 4. Tuning chunk size/k without a fixed eval set.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Add 4 rows (one per failure type) to EVAL and check the classification.
# Compute recall@1 as well as recall@3.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Connect this evaluator to the RAG pipeline from 01-rag-pipeline-basics: run
# 12 labelled questions through retrieve() + build_prompt() (mock or real
# model) and produce the full report automatically.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Implement an LLM-judge faithfulness metric (claims extraction, then per-claim
# support check against retrieved text) and compare its verdicts with your own
# manual labels on 15 answers. Report agreement and the judge's typical errors.

# YOUR CODE:

