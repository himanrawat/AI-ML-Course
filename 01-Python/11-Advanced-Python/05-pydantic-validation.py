# ======================================
# TOPIC: DATA VALIDATION WITH PYDANTIC
# LEVEL: ADVANCED
# ID: python.advanced.pydantic
# ======================================

# INTRODUCTION
# Data from users, files, APIs and LLMs cannot be trusted. Pydantic turns type
# hints into runtime validation - it powers FastAPI and is the standard way to
# validate structured LLM output. (Requires: pip install pydantic.)
#
# THEORY
# - Subclass BaseModel and declare fields with type hints.
# - Creating a model VALIDATES and CONVERTS input ("42" -> 42 for an int field).
#   Invalid data raises ValidationError listing every problem.
# - Field(...) adds constraints: Field(ge=0, le=1), Field(min_length=1),
#   default values and descriptions.
# - @field_validator adds custom checks for one field;
#   @model_validator checks several fields together.
# - model_validate(dict), model_validate_json(text) parse input;
#   model_dump() / model_dump_json() serialize.
# - model_json_schema() produces a JSON Schema - used for LLM structured output.
#
# REAL-WORLD ANALOGY
# Airport security: every bag is scanned against the rules; acceptable items
# pass (sometimes repacked/converted), forbidden ones are listed and rejected.
#
# SYNTAX:
#   class User(BaseModel):
#       name: str
#       age: int = Field(ge=0)
#   User.model_validate({"name": "A", "age": "30"})
#
# SMALL WORKING EXAMPLE:
from typing import Literal

from pydantic import BaseModel, Field, ValidationError, field_validator

class Sentiment(BaseModel):
    label: Literal["positive", "negative", "neutral"]
    confidence: float = Field(ge=0, le=1)
    keywords: list[str] = Field(default_factory=list, max_length=5)

    @field_validator("keywords")
    @classmethod
    def lowercase_keywords(cls, value: list[str]) -> list[str]:
        return [k.strip().lower() for k in value if k.strip()]

llm_output = '{"label": "positive", "confidence": "0.93", "keywords": [" Great ", "FAST"]}'
result = Sentiment.model_validate_json(llm_output)
print(result)
print(result.model_dump())
bad = {"label": "happy", "confidence": 1.4}
try:
    Sentiment.model_validate(bad)
except ValidationError as error:
    for problem in error.errors():
        print(problem["loc"], "->", problem["msg"])
print(sorted(Sentiment.model_json_schema()["properties"]))

# EXPLANATION (LINE BY LINE):
# class Sentiment(BaseModel)       -> the expected structure.
# label: Literal[...]              -> only three strings allowed.
# confidence: float = Field(ge=0, le=1) -> numeric range constraint.
# keywords ... max_length=5        -> at most 5 items; default is a new empty list.
# @field_validator("keywords")     -> custom cleaning: strip + lowercase + drop blanks.
# model_validate_json(llm_output)  -> parse JSON text; "0.93" is converted to 0.93.
# model_dump()                     -> back to a plain dict.
# ValidationError.errors()         -> every problem with its location and message.
# model_json_schema()              -> JSON Schema you can give to an LLM API.
#
# COMMON MISTAKES:
# 1. Using json.loads + manual if-checks instead of a schema.
# 2. Forgetting @classmethod under @field_validator.
# 3. Expecting strict types by default (Pydantic converts compatible values;
#    use strict=True when you need exact types).
# 4. Catching ValidationError and discarding the detailed messages.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create a Product model (name: str, price: float > 0, tags: list[str]).
# Create one valid product and print one invalid attempt's errors.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Create Address and Customer models (Customer has an Address and a list of
# emails validated with a field_validator). Parse a nested JSON string and
# print customer.address.city. Add a model_validator ensuring a shipping
# country is in an allowed list.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build a ResumeExtraction model (name, email, years_experience >= 0,
# skills list, education list of nested models). Write parse_llm_response(text)
# that extracts the first JSON object from messy text (e.g. wrapped in
# ```json fences or prose), validates it, and returns either the model or a
# list of human-readable error messages suitable for sending back to an LLM
# in a retry prompt. Print the JSON schema.

# YOUR CODE:

