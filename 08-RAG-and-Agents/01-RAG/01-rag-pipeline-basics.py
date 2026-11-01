# ======================================
# TOPIC: RETRIEVAL-AUGMENTED GENERATION (RAG) BASICS
# LEVEL: INTERMEDIATE
# ID: rag-agents.rag.pipeline-basics
# ======================================

# INTRODUCTION
# LLMs don't know your company's documents and their knowledge goes stale.
# RAG retrieves the most relevant passages at question time and gives them to
# the model as grounded context - the most common architecture for
# enterprise AI assistants.
#
# THEORY
# Two phases:
# INDEXING (offline): load documents -> clean -> split into CHUNKS -> embed
#   each chunk -> store vectors + text + metadata (source, page, date).
# QUERYING (online): embed the question -> retrieve top-k similar chunks
#   (optionally filter by metadata, re-rank) -> build a prompt with the chunks
#   and the question -> generate an answer WITH citations -> return sources.
# Why it works: the model's strength (reading and synthesising text) is used
# on the right text, instead of relying on memorised knowledge.
# Failure points to watch: bad chunking, retrieval misses, too many irrelevant
# chunks, the model ignoring context, missing citations. Evaluate retrieval and
# generation SEPARATELY (see 04-rag-evaluation).
#
# REAL-WORLD ANALOGY
# An open-book exam: a librarian (retriever) brings the most relevant pages,
# and the student (LLM) answers using them - citing page numbers.
#
# SYNTAX:
#   chunks = retrieve(question, k=3); answer = llm(prompt(question, chunks))
#
# SMALL WORKING EXAMPLE:
import sys
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "06-Prompt-Engineering"))
from course_llm import complete

DOCUMENTS = {
    "handbook.md#leave": "Employees get 24 days of paid leave per year. Unused leave up to 5 days carries over.",
    "handbook.md#remote": "Remote work is allowed up to 3 days per week with manager approval.",
    "handbook.md#equipment": "New employees receive a laptop; monitors can be requested through the IT portal.",
    "benefits.md#health": "Health insurance covers the employee, spouse and up to two children.",
    "benefits.md#learning": "Each employee has a yearly learning budget of 1,000 USD for courses and books.",
}
ids = list(DOCUMENTS)
vectorizer = TfidfVectorizer().fit(DOCUMENTS.values())
index = vectorizer.transform(DOCUMENTS.values())

def retrieve(question, k=2):
    scores = (index @ vectorizer.transform([question]).T).toarray().ravel()
    top = np.argsort(scores)[::-1][:k]
    return [(ids[i], DOCUMENTS[ids[i]], round(float(scores[i]), 3)) for i in top if scores[i] > 0]

def build_prompt(question, chunks):
    context = "\n".join(f'<doc id="{doc_id}">{text}</doc>' for doc_id, text, _ in chunks)
    return (f"<documents>\n{context}\n</documents>\n"
            "Answer using only the documents. Cite doc ids in square brackets after each claim. "
            "If the documents don't contain the answer, say you don't know.\n"
            f"Question: {question}")

question = "How many leave days can I carry over to next year?"
chunks = retrieve(question)
print("retrieved:", [(doc_id, score) for doc_id, _, score in chunks])
print(complete(build_prompt(question, chunks), offline=(
    "You can carry over up to 5 unused leave days to the next year [handbook.md#leave].")))

# EXPLANATION (LINE BY LINE):
# sys.path.insert(...)       -> reuse the course LLM helper from 06-Prompt-Engineering.
# DOCUMENTS                  -> pre-chunked passages with ids that include the source.
# TfidfVectorizer            -> keyword-based retriever for the offline demo (swap in
#                               embeddings + a vector store from 07-Generative-AI).
# retrieve()                 -> score every chunk, keep the top-k with non-zero scores.
# build_prompt()             -> documents first, grounding + citation + abstention rules,
#                               question last.
# The answer cites [handbook.md#leave] -> the user can verify the source.
#
# COMMON MISTAKES:
# 1. Retrieving too many chunks "to be safe" (noise, cost, lost-in-the-middle).
# 2. No citations, so users can't verify answers.
# 3. Only evaluating final answers, never retrieval quality.
# 4. Forgetting access control: users must only retrieve documents they may see.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Ask 5 questions (2 unanswerable). Print what retrieve() returns for each and
# decide whether retrieval succeeded before looking at any answer.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Replace TF-IDF with the LSA embedder or a sentence-transformers model and a
# similarity threshold. Compare which questions each retriever gets right.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build an end-to-end RAG CLI over a folder of your own Markdown notes: load
# files, chunk by headings, index, answer questions with citations (API
# access), and print the retrieved chunks for transparency.

# YOUR CODE:

