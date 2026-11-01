# ======================================
# TOPIC: PROJECT 6 - STRUCTURED JSON EXTRACTION FROM INVOICES
# LEVEL: ADVANCED
# ID: prompt-engineering.projects.json-extraction
# ======================================

# INTRODUCTION
# Extract line items, totals and dates from messy invoice text into strict
# JSON that passes both schema validation AND business-rule validation, with
# automatic repair when it doesn't.
#
# THEORY
# Skills used: JSON Schema + Pydantic (03/03), retries with feedback,
# guardrails (05/03), evaluation (04/01).
# Design decisions and WHY:
# - Two layers of validation: SCHEMA (types/enums/required) and BUSINESS RULES
#   (line items sum to subtotal, subtotal + tax = total, dates valid) ->
#   schema-valid output can still be wrong.
# - Repair loop: send the specific validation errors back to the model with
#   the previous output -> targeted fixes instead of random retries.
# - Use Decimal for money in code; never trust floats for currency.
# - Prefer native structured outputs in production (constrained decoding);
#   keep the business-rule checks regardless.
# Deliverables: extractor with repair loop, 10 invoice test cases (including
# OCR noise and missing fields), validity and exact-match rates.
#
# REAL-WORLD ANALOGY
# An accounts clerk who types invoices into the system, and the system refuses
# to save until the numbers add up - pointing at the exact field that's wrong.
#
# SYNTAX:
#   invoice, errors = extract_with_repair(text, max_attempts=3)
#
# SMALL WORKING EXAMPLE:
import json
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

from pydantic import BaseModel, ValidationError, model_validator

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_llm import complete

class LineItem(BaseModel):
    description: str
    quantity: int
    unit_price: Decimal

class Invoice(BaseModel):
    invoice_number: str
    issue_date: date
    items: list[LineItem]
    tax: Decimal
    total: Decimal

    @model_validator(mode="after")
    def totals_add_up(self):
        subtotal = sum(i.quantity * i.unit_price for i in self.items)
        if subtotal + self.tax != self.total:
            raise ValueError(f"items ({subtotal}) + tax ({self.tax}) != total ({self.total})")
        return self

TEXT = "INV-2291  Date: 03/10/2026\n2 x Keyboard @ 45.00\n1 x Mouse @ 20.00\nTax 18.90  TOTAL 128.90"
ATTEMPTS = iter([
    {"invoice_number": "INV-2291", "issue_date": "2026-10-03", "items": [
        {"description": "Keyboard", "quantity": 2, "unit_price": "45.00"},
        {"description": "Mouse", "quantity": 1, "unit_price": "20.00"}], "tax": "18.90", "total": "118.90"},
    {"invoice_number": "INV-2291", "issue_date": "2026-10-03", "items": [
        {"description": "Keyboard", "quantity": 2, "unit_price": "45.00"},
        {"description": "Mouse", "quantity": 1, "unit_price": "20.00"}], "tax": "18.90", "total": "128.90"},
])

def extract_with_repair(text, max_attempts=3):
    prompt = (f"Extract the invoice as JSON matching:\n{json.dumps(Invoice.model_json_schema())}\n"
              f"Dates are DD/MM/YYYY in the source; output ISO dates.\n<invoice>\n{text}\n</invoice>")
    messages = [{"role": "user", "content": prompt}]
    errors = []
    for attempt in range(1, max_attempts + 1):
        reply = complete(messages=messages, offline=lambda _: json.dumps(next(ATTEMPTS)))
        try:
            return Invoice.model_validate_json(reply), errors
        except ValidationError as error:
            problems = [e["msg"] for e in error.errors()]
            errors.append((attempt, problems))
            messages += [{"role": "assistant", "content": reply},
                         {"role": "user", "content": f"Validation failed: {problems}. Re-read the invoice and return corrected JSON only."}]
    return None, errors

invoice, errors = extract_with_repair(TEXT)
print("repair history:", errors)
print("final:", invoice.invoice_number, invoice.issue_date, "total", invoice.total if invoice else None)

# EXPLANATION (LINE BY LINE):
# LineItem / Invoice         -> schema with Decimal money and a real date type.
# totals_add_up              -> business rule beyond the schema.
# ATTEMPTS                   -> offline: first reply misreads the total (118.90),
#                               second reply is correct.
# extract_with_repair        -> validate; on failure append the bad reply and the exact
#                               errors as a new user turn; try again (bounded attempts).
# "DD/MM/YYYY" note          -> context the model needs: 03/10 is 3 October, not 10 March.
#
# COMMON MISTAKES:
# 1. Floats for money (0.1 + 0.2 problems).
# 2. Only schema validation - totals that don't add up pass silently.
# 3. Retrying without telling the model what was wrong.
# 4. Ambiguous date formats left unspecified.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write 5 invoice texts in different layouts (including one with a discount
# line and one with a missing date) and the expected JSON for each.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Add a discount field and currency (Literal["INR", "USD", "EUR"]) to the
# schema, update the business rule, and test extract_with_repair on your 5
# invoices with mocked replies that exercise each failure type.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# With API access, run the extractor on 10 invoices (add OCR-style noise:
# O/0 and l/1 swaps). Measure first-attempt validity, final validity after
# repair, field-level exact match and average attempts. Then try native
# structured outputs (client.messages.parse) and compare.

# YOUR CODE:

