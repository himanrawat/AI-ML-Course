# ======================================
# TOPIC: PROMPT TEMPLATES AND DYNAMIC PROMPTS
# LEVEL: INTERMEDIATE
# ID: prompt-engineering.reasoning.templates
# ======================================

# INTRODUCTION
# In applications, prompts are built by code: the same instructions with
# different users, documents, languages and examples each time. Templates keep
# this maintainable, testable and safe.
#
# THEORY
# - A PROMPT TEMPLATE = fixed instructions + named placeholders filled at runtime.
#   Tools: f-strings, string.Template, Jinja2 (loops/conditionals).
# - DYNAMIC prompts adapt to the situation: include sections only when
#   relevant, choose examples per input, adjust language/tone per user, insert
#   retrieved documents (RAG).
# - Good practice:
#   * Keep templates in files/version control, not scattered in code.
#   * Validate variables (no missing values, length limits).
#   * Put stable content first and variable content last (cache-friendly,
#     consistent).
#   * Escape/delimit user content so it can't break the prompt structure.
#   * Test templates with edge cases: empty fields, very long input, special
#     characters, other languages.
# - The template is code: version it and test it like code.
#
# REAL-WORLD ANALOGY
# A mail-merge letter: one carefully written letter with blanks for name and
# details, filled in automatically for thousands of customers.
#
# SYNTAX:
#   template = string.Template("Hello $name"); template.substitute(name="Asha")
#
# SMALL WORKING EXAMPLE:
from dataclasses import dataclass, field
from string import Template
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_llm import complete

@dataclass
class PromptTemplate:
    name: str
    version: str
    text: str
    required: set = field(default_factory=set)
    max_chars: dict = field(default_factory=dict)

    def render(self, **values):
        missing = self.required - values.keys()
        if missing:
            raise ValueError(f"{self.name}: missing variables {sorted(missing)}")
        for key, limit in self.max_chars.items():
            if len(str(values.get(key, ""))) > limit:
                raise ValueError(f"{self.name}: '{key}' exceeds {limit} characters")
        return Template(self.text).substitute(values)

REPLY_TEMPLATE = PromptTemplate(
    name="support_reply", version="1.2.0",
    text=("You write replies for $company support.\n"
          "Tone: $tone. Language: $language.\n"
          "$optional_policy"
          "<customer_message>\n$message\n</customer_message>\n"
          "Write a reply under 120 words that resolves the customer's issue."),
    required={"company", "tone", "language", "message", "optional_policy"},
    max_chars={"message": 2000},
)

def build_reply_prompt(customer, message, policy=None):
    tone = "formal and concise" if customer["plan"] == "enterprise" else "friendly"
    policy_block = f"<policy>\n{policy}\n</policy>\n" if policy else ""
    return REPLY_TEMPLATE.render(company="Acme", tone=tone, language=customer["language"],
                                 message=message, optional_policy=policy_block)

prompt = build_reply_prompt({"plan": "enterprise", "language": "German"},
                            "Our invoices show the wrong VAT number.",
                            policy="VAT details can be updated under Settings > Billing.")
print(f"[{REPLY_TEMPLATE.name} v{REPLY_TEMPLATE.version}]\n{prompt}")
try:
    REPLY_TEMPLATE.render(company="Acme")
except ValueError as error:
    print("caught:", error)
print(complete(prompt, offline="Sehr geehrte Damen und Herren, Sie können die USt-IdNr. unter Einstellungen > Abrechnung aktualisieren..."))

# EXPLANATION (LINE BY LINE):
# PromptTemplate             -> name + version + text + validation rules: prompts as code.
# Template.substitute        -> raises KeyError for any placeholder not provided.
# required / max_chars       -> fail fast on missing or oversized variables.
# build_reply_prompt         -> DYNAMIC: tone depends on the customer's plan; the policy
#                               section is included only when available.
# Stable instructions first, variable message last, user text inside tags.
# render(company="Acme")     -> missing variables are reported clearly.
#
# COMMON MISTAKES:
# 1. Building prompts with scattered string concatenation across the codebase.
# 2. Silently rendering "None" or empty values into the prompt.
# 3. No version identifier, so you can't tell which prompt produced an output.
# 4. Putting user input where it can be mistaken for instructions.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create a template for generating a product description with placeholders
# for product name, 3 features and audience. Render it for two products.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Rewrite REPLY_TEMPLATE using Jinja2 (pip install jinja2 into the course venv)
# with a loop over previous messages and a conditional policy section. Write 5
# edge-case tests (empty history, very long message, braces in text, emoji,
# missing language).

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build a PromptRegistry that loads templates from a folder of YAML or JSON
# files (name, version, text, required variables, model settings), renders by
# name + version, and logs which template version produced each render.
# Include a test that fails if any template references an undeclared variable.

# YOUR CODE:

