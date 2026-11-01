# ======================================
# TOPIC: RAISING AND CUSTOM EXCEPTIONS
# LEVEL: INTERMEDIATE
# ID: python.exceptions.raising-custom
# ======================================

# INTRODUCTION
# Your own functions must also report problems clearly: an invalid config,
# a model output that fails validation, an API that rejected a request.
#
# THEORY
# - raise ValueError("clear message") signals an error to the caller.
# - Choose the right built-in: ValueError (bad value), TypeError (wrong type),
#   KeyError, FileNotFoundError, RuntimeError, NotImplementedError.
# - Custom exceptions: subclass Exception. Create a base class for your
#   project, then specific subclasses, so callers can catch broadly or narrowly.
# - Add useful attributes (e.g. the field name, the status code).
# - raise NewError(...) from original keeps the original cause in the traceback.
# - A bare "raise" inside except re-raises the current exception.
# - ExceptionGroup + except* handle several errors at once (e.g. from
#   concurrent tasks).
#
# REAL-WORLD ANALOGY
# A quality inspector on a production line who stops the line with a labelled
# tag ("wrong colour", "crack in casing") so the right team can fix it.
#
# SYNTAX:
#   class AppError(Exception): ...
#   raise AppError("message") from original_error
#
# SMALL WORKING EXAMPLE:
class PipelineError(Exception):
    """Base error for this pipeline."""

class ValidationError(PipelineError):
    def __init__(self, field, message):
        super().__init__(f"{field}: {message}")
        self.field = field

class ModelOutputError(PipelineError):
    pass

def validate_config(config):
    if "model" not in config:
        raise ValidationError("model", "is required")
    if not 0 < config.get("temperature", 0.5) <= 1:
        raise ValidationError("temperature", "must be in (0, 1]")

def parse_output(text):
    try:
        return int(text)
    except ValueError as error:
        raise ModelOutputError(f"expected a number, got {text!r}") from error

for cfg in [{"model": "small"}, {"temperature": 0.2}, {"model": "x", "temperature": 3}]:
    try:
        validate_config(cfg)
        print("valid:", cfg)
    except ValidationError as error:
        print(f"invalid field {error.field!r} -> {error}")

try:
    parse_output("forty-two")
except PipelineError as error:
    print(type(error).__name__, error, "| caused by:", repr(error.__cause__))

# EXPLANATION (LINE BY LINE):
# class PipelineError(Exception)  -> project-wide base class.
# class ValidationError(PipelineError) with a field attribute -> richer error info.
# raise ValidationError("model", "is required") -> stop with a precise reason.
# raise ModelOutputError(...) from error -> wraps the low-level ValueError,
#                                           keeping it as __cause__.
# except ValidationError as error -> catch just validation problems.
# except PipelineError            -> catches ANY subclass (broad handling).
#
# COMMON MISTAKES:
# 1. Raising generic Exception("error") with no useful message.
# 2. Returning error codes / None instead of raising for real errors.
# 3. Losing the original error (forgetting "from error").
# 4. Inheriting from BaseException instead of Exception.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write set_age(age) that raises TypeError if age is not an int and
# ValueError if it is negative or above 150. Call it inside try/except.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Create InsufficientFundsError carrying balance and requested amount.
# Use it in a withdraw(balance, amount) function and print a helpful message
# built from the exception's attributes.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Create an exception hierarchy for an LLM API client: LLMError ->
# RateLimitError(retry_after), AuthenticationError, InvalidResponseError.
# Write call_api(scenario) that raises each, and handle_call(scenario) that
# retries on RateLimitError, fails fast on AuthenticationError, and wraps
# unexpected errors with "raise LLMError(...) from error".
# Bonus: collect several validation errors into an ExceptionGroup and handle
# them with except*.

# YOUR CODE:

