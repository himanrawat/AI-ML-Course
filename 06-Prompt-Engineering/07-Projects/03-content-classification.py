# ======================================
# TOPIC: PROJECT 3 - AI CONTENT CLASSIFICATION
# LEVEL: INTERMEDIATE
# ID: prompt-engineering.projects.content-classification
# ======================================

# INTRODUCTION
# Classify user-generated content (posts, comments, tickets) into categories
# for moderation and routing - and measure it like an ML classifier.
#
# THEORY
# Skills used: few-shot prompting (02/03), structured output (03/03),
# evaluation (04/01), classification metrics (04-Machine-Learning/03).
# Design decisions and WHY:
# - Clear label DEFINITIONS with boundary rules (what's "spam" vs "promotion")
#   -> most classification errors are definition ambiguity.
# - Multi-label vs single-label must be explicit.
# - Ask for a confidence level and route low-confidence items to humans.
# - Compare with a classic baseline (TF-IDF + logistic regression) - sometimes
#   the cheap model is good enough, sometimes the LLM is far better.
# Deliverables: label guide, 40-item labelled set, LLM classifier, baseline,
# precision/recall per label for both, cost comparison.
#
# REAL-WORLD ANALOGY
# A post-room sorter with a clear rulebook for every bin, who puts uncertain
# envelopes in a "check me" tray.
#
# SYNTAX:
#   label = classify(text)  ->  {"labels": [...], "confidence": "high|low"}
#
# SMALL WORKING EXAMPLE:
import json
import sys
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.pipeline import make_pipeline

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_llm import complete

LABEL_GUIDE = """spam: unsolicited bulk/scam content, suspicious links, "earn money fast".
promotion: a user mentioning their OWN product or service openly.
harassment: insults or threats aimed at a person or group.
ok: everything else, including criticism of ideas or products."""

DATA = [
    ("Earn $5000 a week from home, click bit.ly/xyz", "spam"),
    ("I built a free budgeting app, feedback welcome!", "promotion"),
    ("You are an idiot and everyone hates you", "harassment"),
    ("This framework's docs are confusing", "ok"),
    ("WIN a free iPhone!!! limited offer", "spam"),
    ("Check out my YouTube channel on Python tips", "promotion"),
    ("People like you should be banned from the internet, loser", "harassment"),
    ("Great tutorial, thanks for sharing", "ok"),
]

def llm_classify(text, offline_label):
    prompt = (f"<label_guide>\n{LABEL_GUIDE}\n</label_guide>\n"
              f"Classify the post into exactly one label from the guide.\n"
              f'Return JSON: {{"label": "...", "confidence": "high|low"}}\n<post>{text}</post>')
    return json.loads(complete(prompt, offline=json.dumps({"label": offline_label, "confidence": "high"})))

texts, labels = zip(*DATA)
llm_predictions = [llm_classify(t, offline_label=l)["label"] for t, l in DATA]
print(classification_report(labels, llm_predictions, zero_division=0))
baseline = make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000)).fit(texts[::2], labels[::2])
print("baseline on unseen half:", list(zip(baseline.predict(texts[1::2]), labels[1::2])))

# EXPLANATION (LINE BY LINE):
# LABEL_GUIDE                -> definitions + boundaries (own product = promotion, not
#                               spam; criticism of ideas = ok, not harassment).
# DATA                       -> tiny labelled set (you'll build 40+ items).
# llm_classify               -> guide + closed label set + JSON + confidence. Offline it
#                               echoes the true label, so offline scores are NOT real -
#                               run with COURSE_USE_LLM=1 for actual results.
# classification_report      -> per-label precision/recall/F1 (same metrics as ML).
# baseline                   -> TF-IDF + logistic regression trained on 4 items: shows
#                               how weak a classic model is with very little data.
#
# COMMON MISTAKES:
# 1. Labels without definitions ("toxic") - annotators and models disagree.
# 2. Reporting accuracy on imbalanced data.
# 3. Never comparing against a cheap baseline.
# 4. Evaluating on the same examples used in the few-shot prompt.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Expand DATA to 40 items (10 per label, including 3 tricky boundary cases per
# label). Write down why each tricky case belongs to its label.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Run the LLM classifier (API access) and the TF-IDF baseline (train/test
# split) on your 40 items. Compare per-label F1, list disagreements, and
# estimate the cost per 10,000 posts for each.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Add confidence-based routing: send "low" confidence items to a human queue.
# Measure precision of auto-handled items vs the share sent to humans, and
# choose an operating point. Write the final label guide improvements you made
# after error analysis and why.

# YOUR CODE:

