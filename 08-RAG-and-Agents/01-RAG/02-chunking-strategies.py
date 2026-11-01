# ======================================
# TOPIC: CHUNKING STRATEGIES
# LEVEL: INTERMEDIATE
# ID: rag-agents.rag.chunking
# ======================================

# INTRODUCTION
# Retrieval can only return what your chunks contain. Chunks that are too big
# dilute relevance; too small lose context; splits in the wrong place cut
# answers in half. Chunking is one of the highest-impact RAG decisions.
#
# THEORY
# Strategies:
# - FIXED-SIZE (characters/tokens) with OVERLAP: simple and robust baseline.
# - SENTENCE/PARAGRAPH-based: respects natural boundaries.
# - STRUCTURE-aware: split on Markdown headings, HTML sections, code functions,
#   table rows - keep the heading path as metadata ("Benefits > Health").
# - Semantic chunking: split where topic similarity between sentences drops.
# - CONTEXTUAL chunks: prepend a short description of the document/section to
#   each chunk so it makes sense on its own ("This chunk is from the 2026
#   travel policy, section Meals:").
# Typical sizes: 200-800 tokens with 10-20% overlap; tune with retrieval evals.
# Store metadata: source, section, position, dates - for filtering and citations.
#
# REAL-WORLD ANALOGY
# Cutting a cookbook into recipe cards: cut per recipe (structure), not every
# 500 characters, or you'll get cards with half an ingredient list.
#
# SYNTAX:
#   chunks = split(text, size=500, overlap=50)
#
# SMALL WORKING EXAMPLE:
import re

DOC = """# Travel Policy
## Flights
Economy class for flights under 6 hours. Business class is allowed for longer flights with VP approval.
## Meals
Meals are reimbursed up to 50 USD per day. Alcohol is not reimbursed.
## Hotels
Book through the travel portal. The nightly limit is 180 USD in major cities and 120 USD elsewhere."""

def fixed_chunks(text, size=120, overlap=20):
    step = size - overlap
    return [text[i:i + size] for i in range(0, len(text), step)]

def heading_chunks(markdown):
    chunks, path = [], []
    for block in re.split(r"\n(?=#)", markdown):
        heading = re.match(r"(#+) (.*)", block)
        level, title = len(heading.group(1)), heading.group(2)
        path = path[:level - 1] + [title]
        body = block[heading.end():].strip()
        if body:
            chunks.append({"section": " > ".join(path), "text": f"[{' > '.join(path)}] {body}"})
    return chunks

for i, chunk in enumerate(fixed_chunks(DOC)):
    print(f"fixed {i}: {chunk!r}")
for chunk in heading_chunks(DOC):
    print("heading:", chunk["section"], "|", chunk["text"][:70], "...")

# EXPLANATION (LINE BY LINE):
# fixed_chunks               -> slices every 100 characters (120 size - 20 overlap).
#                               Look at the output: sentences and even words are cut,
#                               and "180 USD" may be separated from "Hotels".
# heading_chunks             -> splits at Markdown headings, tracks the heading PATH, and
#                               prefixes it to each chunk so the chunk is self-explanatory.
# section metadata           -> usable for citations ("Travel Policy > Hotels") and filters.
#
# COMMON MISTAKES:
# 1. One chunk size for every document type (code, tables, prose differ).
# 2. No overlap with fixed-size chunks (answers split across boundaries).
# 3. Chunks without source/section metadata.
# 4. Choosing chunk size without measuring retrieval quality.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write a sentence-based chunker that groups sentences until a maximum of 200
# characters, never splitting a sentence. Run it on DOC.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Create 8 questions about DOC with the section that answers each. Compare
# retrieval hit rate (TF-IDF top-1) for fixed chunks of 80, 160, 320 characters
# and for heading chunks.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Implement contextual chunking: for each heading chunk, generate (API access)
# or template a one-sentence context description of the document and section,
# prepend it, and measure retrieval improvement on a longer multi-document
# corpus with 20 questions.

# YOUR CODE:

