# ======================================
# TOPIC: PROJECT 4 - MULTILINGUAL TRANSLATION ASSISTANT
# LEVEL: INTERMEDIATE
# ID: prompt-engineering.projects.translation
# ======================================

# INTRODUCTION
# Translate product content into several languages while preserving meaning,
# tone, brand terms and formatting - and check quality automatically.
#
# THEORY
# Skills used: contextual prompting (02/04), templates (03/04), structured
# output (03/03), evaluation with code + LLM judge (04/01).
# Design decisions and WHY:
# - GLOSSARY: brand/product terms that must stay untranslated or use fixed
#   translations -> consistency across thousands of strings.
# - Context: audience, tone, where the text appears (button vs article) ->
#   "Save" as a button needs a short imperative, not a sentence.
# - Preserve placeholders ({name}, %s, HTML tags) - verify in code.
# - Back-translation and an LLM judge for meaning checks; native speakers for
#   final review of important content.
# Deliverables: translator with glossary + placeholder checks, test set of 15
# UI strings x 3 languages, automatic checks, judge scores, comparison of a
# context-free vs context-rich prompt.
#
# REAL-WORLD ANALOGY
# A professional translator who gets a style guide, a list of brand terms, and
# a screenshot of where the text appears - not just a bare sentence.
#
# SYNTAX:
#   result = translate(text, target_language, context, glossary)
#
# SMALL WORKING EXAMPLE:
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_llm import complete

GLOSSARY = {"Acme Cloud": "Acme Cloud", "workspace": {"de": "Arbeitsbereich", "hi": "वर्कस्पेस"}}

def build_prompt(text, language, context):
    terms = "\n".join(f"- {term}: {value if isinstance(value, str) else value.get(language, term)}"
                      for term, value in GLOSSARY.items())
    return f"""Translate the UI text into language code "{language}".
Context: {context}
Glossary (use exactly):
{terms}
Keep placeholders like {{name}} and HTML tags unchanged.
Return JSON: {{"translation": "...", "notes": "any ambiguity you resolved"}}
<text>{text}</text>"""

def check(source, translation, language):
    problems = []
    if sorted(re.findall(r"\{\w+\}|<[^>]+>", source)) != sorted(re.findall(r"\{\w+\}|<[^>]+>", translation)):
        problems.append("placeholders changed")
    if "Acme Cloud" in source and "Acme Cloud" not in translation:
        problems.append("brand name translated")
    return problems

source = "Welcome back, {name}! Your <b>workspace</b> in Acme Cloud is ready."
reply = complete(build_prompt(source, "de", "dashboard banner, friendly tone, informal 'du'"), offline=json.dumps(
    {"translation": "Willkommen zurück, {name}! Dein <b>Arbeitsbereich</b> in Acme Cloud ist bereit.",
     "notes": "Used informal 'du' as requested."}))
result = json.loads(reply)
print(result["translation"])
print("checks:", check(source, result["translation"], "de") or "all passed")
print("broken example checks:", check(source, "Willkommen, {nom}! Ihr Arbeitsbereich in Acme Wolke ist bereit.", "de"))

# EXPLANATION (LINE BY LINE):
# GLOSSARY                   -> fixed terms; a string means "same in every language".
# build_prompt               -> target language, usage context, glossary, placeholder rule,
#                               JSON with notes (surfaces ambiguity decisions).
# check()                    -> deterministic checks: placeholders/tags identical, brand
#                               kept. These catch the most common production bugs.
# Broken example             -> renamed placeholder, dropped tags and translated brand
#                               are all flagged.
#
# COMMON MISTAKES:
# 1. Translating strings without context (wrong word sense, wrong length).
# 2. Breaking placeholders, which crashes the app at runtime.
# 3. Inconsistent terminology across strings.
# 4. Trusting LLM quality scores without native-speaker spot checks.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write 15 UI strings (buttons, errors, emails) with context notes, including
# 5 with placeholders and 3 that are ambiguous without context.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Add back-translation: translate to the target language and back to English,
# then compare meaning with an LLM judge prompt (score 1-5 with reasons in JSON).
# Run on your 15 strings for 2 languages (API access) and list the weakest items.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Batch-translate a JSON locale file (key -> English string) into 3 languages:
# chunk strings to stay within token budgets, keep keys untouched, run checks,
# retry failed items with the check errors in the prompt, and write
# locales/<lang>.json. Report pass rate and cost.

# YOUR CODE:

