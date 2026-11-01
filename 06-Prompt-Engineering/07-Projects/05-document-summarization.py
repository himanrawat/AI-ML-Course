# ======================================
# TOPIC: PROJECT 5 - DOCUMENT SUMMARIZATION
# LEVEL: INTERMEDIATE
# ID: prompt-engineering.projects.summarization
# ======================================

# INTRODUCTION
# Summarise long documents (reports, meeting transcripts, research papers)
# for a specific reader - faithfully, at a controlled length - including
# documents larger than you want to send in one call.
#
# THEORY
# Skills used: anatomy of a prompt (02/01), context windows (01/02),
# chaining (03/06), hallucination mitigation (05/01), evaluation (04/01).
# Design decisions and WHY:
# - Define the READER and PURPOSE: an executive summary differs from a
#   technical digest -> the model decides what matters based on purpose.
# - Control length with structure ("3 bullets of <= 20 words") - more reliable
#   than "be brief".
# - Long documents: MAP-REDUCE chaining (summarise chunks, then summarise the
#   summaries) or one long-context call; measure both.
# - FAITHFULNESS: every claim must be supported by the source; check numbers
#   and names in code, and use a judge for unsupported claims.
# Deliverables: summariser with reader profiles, map-reduce for long docs,
# faithfulness checks, evaluation on 5 documents.
#
# REAL-WORLD ANALOGY
# A chief of staff who reads a 60-page report and writes the one page the CEO
# actually needs - without adding anything the report didn't say.
#
# SYNTAX:
#   summary = reduce_summaries([summarise(chunk) for chunk in chunks(document)])
#
# SMALL WORKING EXAMPLE:
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_llm import complete

DOCUMENT = (
    "Q3 revenue grew 18% to $4.2M, driven by the enterprise plan. "
    "Churn rose from 2.1% to 2.9% among small-business customers after the price change. "
    "The mobile app launch slipped from August to October due to an App Store review issue. "
    "Hiring: 6 engineers joined; 2 sales roles remain open. "
    "Next quarter priorities: reduce SMB churn, launch mobile, expand to Germany."
) * 3

def chunks(text, max_words=60):
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

def summarise(text, reader):
    prompt = (f"<document>\n{text}\n</document>\nSummarise for: {reader}.\n"
              "Exactly 3 bullet points, each <= 20 words. Use only facts from the document; "
              "keep every number exactly as written.")
    return complete(prompt, offline=(
        "- Revenue up 18% to $4.2M from enterprise; SMB churn rose to 2.9%\n"
        "- Mobile launch slipped to October; 6 engineers hired, 2 sales roles open\n"
        "- Next: cut SMB churn, launch mobile, expand to Germany"))

def numbers_not_in_source(summary, source):
    return [n for n in re.findall(r"\d+(?:\.\d+)?%?", summary) if n not in source]

parts = chunks(DOCUMENT)
partial = [summarise(part, "the CEO, who needs decisions and risks") for part in parts]
final = summarise("\n".join(partial), "the CEO, who needs decisions and risks")
print(f"{len(DOCUMENT.split())} words -> {len(parts)} chunks -> final summary:\n{final}")
print("numbers not found in source:", numbers_not_in_source(final, DOCUMENT) or "none")

# EXPLANATION (LINE BY LINE):
# DOCUMENT                   -> a repeated report standing in for a long document.
# chunks()                   -> split by word count (real systems split on sections/tokens).
# summarise()                -> reader + purpose, fixed structure, faithfulness rules.
# Map step                   -> summarise each chunk; reduce step -> summarise the
#                               partial summaries into the final one.
# numbers_not_in_source      -> a cheap faithfulness check: every number in the summary
#                               must appear in the source.
#
# COMMON MISTAKES:
# 1. "Summarise this" with no reader or purpose.
# 2. Losing important details in map-reduce (check coverage of key facts).
# 3. Not checking numbers and names against the source.
# 4. Splitting chunks mid-sentence/table without overlap.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write three reader profiles (CEO, engineer, customer) and the prompt changes
# each one needs. Predict how the three summaries of DOCUMENT should differ.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Create a "key facts" checklist for 3 documents and a coverage() function that
# checks which facts each summary mentions (keyword/number matching). Compare
# single-call vs map-reduce summaries on coverage (API access or mocks).

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Summarise a real long text (e.g. a public-domain book chapter or long
# article) with: section-aware chunking with overlap, map-reduce, a faithfulness
# judge that lists unsupported claims, and a final report of tokens, cost,
# latency and faithfulness for single-call vs map-reduce.

# YOUR CODE:

