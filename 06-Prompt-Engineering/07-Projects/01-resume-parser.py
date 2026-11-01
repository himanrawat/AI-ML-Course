# ======================================
# TOPIC: PROJECT 1 - RESUME PARSING AND STRUCTURED EXTRACTION
# LEVEL: INTERMEDIATE
# ID: prompt-engineering.projects.resume-parser
# ======================================

# INTRODUCTION
# Recruiting tools turn unstructured resumes into searchable records. You will
# build an extractor that returns validated JSON for any resume text and
# measure its accuracy field by field.
#
# THEORY
# Skills used: structured output + JSON Schema (03/03), grounding and
# abstention (05/01), evaluation (04/01), templates (03/04).
# Design decisions and WHY:
# - Pydantic schema as the contract: types, enums and nullable fields prevent
#   invented values ("null if not stated").
# - Normalise in CODE where possible (dates, emails) rather than asking the model
#   for everything - deterministic and testable.
# - Evaluate per FIELD: names may be 100% right while years of experience is 60%.
# - Resumes contain PII: minimise what you send/log, and get consent.
# Deliverables: extractor, 10-resume eval set with expected JSON, per-field
# accuracy report, two prompt versions compared, a short write-up of why the
# better version wins.
#
# REAL-WORLD ANALOGY
# A careful HR assistant filling in a standard candidate form from each CV,
# leaving a field blank rather than guessing.
#
# SYNTAX:
#   Resume.model_validate_json(complete(build_prompt(text), ...))
#
# SMALL WORKING EXAMPLE:
import json
import sys
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_llm import complete

class Experience(BaseModel):
    company: str
    title: str
    start_year: int | None = None
    end_year: int | None = Field(default=None, description="null if current or unknown")

class Resume(BaseModel):
    name: str
    email: str | None = None
    skills: list[str] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    highest_degree: str | None = None

def build_prompt(resume_text):
    return f"""<resume>
{resume_text}
</resume>
Extract the candidate's details as JSON matching this schema:
{json.dumps(Resume.model_json_schema())}
Rules: use null for anything not stated; never guess years; list skills exactly as written.
Return only the JSON object."""

SAMPLE = """Priya Sharma - priya.s@example.com
Frontend Engineer at PixelWorks (2021 - present). React, TypeScript, GraphQL.
Previously UI Developer at WebNova, 2018-2021.
B.Tech Computer Science, 2018. Learning Python and PyTorch."""

reply = complete(build_prompt(SAMPLE), offline=json.dumps({
    "name": "Priya Sharma", "email": "priya.s@example.com",
    "skills": ["React", "TypeScript", "GraphQL", "Python", "PyTorch"],
    "experience": [{"company": "PixelWorks", "title": "Frontend Engineer", "start_year": 2021, "end_year": None},
                   {"company": "WebNova", "title": "UI Developer", "start_year": 2018, "end_year": 2021}],
    "highest_degree": "B.Tech Computer Science"}))
try:
    resume = Resume.model_validate_json(reply)
    years = sum((job.end_year or 2026) - (job.start_year or 2026) for job in resume.experience)
    print(resume.name, "|", resume.email, "|", len(resume.skills), "skills | ~", years, "years experience")
except ValidationError as error:
    print("invalid extraction:", error.errors())

# EXPLANATION (LINE BY LINE):
# Experience / Resume        -> the output contract; optional fields default to None.
# build_prompt               -> resume first in tags, schema, explicit "null, never guess".
# complete(..., offline=...) -> sample extraction when running offline.
# model_validate_json        -> rejects malformed or wrongly typed output.
# years                      -> derived in CODE from validated data (not asked of the model).
#
# COMMON MISTAKES:
# 1. Asking the model to compute totals it can't verify (do it in code).
# 2. Required fields that force invention (e.g. phone number).
# 3. Measuring only "looks right" instead of per-field accuracy.
# 4. Logging full resumes with PII.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write 3 more sample resumes in different formats (bullet list, paragraph,
# messy copy-paste from PDF) and the expected JSON for each.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Build an eval set of 10 resumes with expected JSON and a field_accuracy()
# function (exact match for name/email, set F1 for skills, per-job match for
# experience). Compare two prompt versions and report per-field results.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Turn the extractor into a CLI: read .txt/.pdf resumes from a folder (pypdf
# for PDFs), redact phone numbers before sending, extract with retry on
# validation errors, write results to JSONL, and print a summary table. Add a
# write-up comment explaining your final prompt design choices.

# YOUR CODE:

