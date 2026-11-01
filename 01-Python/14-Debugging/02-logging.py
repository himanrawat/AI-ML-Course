# ======================================
# TOPIC: LOGGING
# LEVEL: INTERMEDIATE
# ID: python.debugging.logging
# ======================================

# INTRODUCTION
# print() is fine for quick experiments, but real applications need logs with
# levels, timestamps and destinations - especially AI apps where you must
# trace prompts, latencies and failures in production.
#
# THEORY
# - Levels (low to high): DEBUG, INFO, WARNING, ERROR, CRITICAL.
#   A logger only emits messages at or above its configured level.
# - logging.basicConfig(level=..., format=...) configures the root logger
#   once, at program start.
# - Each module gets its own logger: logger = logging.getLogger(__name__).
# - Handlers send logs to places (console, file); formatters shape the text.
# - logger.exception("msg") inside except logs the traceback too.
# - Use lazy formatting: logger.info("user %s", user_id) - the string is only
#   built if the message is actually emitted.
# - Structured (JSON) logs are easier to search in production tools.
# - NEVER log secrets (API keys) or sensitive personal data.
#
# REAL-WORLD ANALOGY
# A ship's logbook: entries have a time, a severity ("routine", "storm
# warning", "mayday") and are kept for later investigation.
#
# SYNTAX:
#   logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
#   logger = logging.getLogger(__name__)
#   logger.warning("disk at %d%%", 91)
#
# SMALL WORKING EXAMPLE:
import json
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger("rag.pipeline")

def answer(question):
    logger.debug("raw question: %r", question)
    logger.info("answering question of %d chars", len(question))
    if not question.strip():
        logger.warning("empty question received")
        return None
    try:
        return 1 / 0
    except ZeroDivisionError:
        logger.exception("model call failed")
        return None

answer("What is RAG?")
answer("   ")

class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({"level": record.levelname, "logger": record.name,
                           "message": record.getMessage()})

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
json_logger = logging.getLogger("rag.metrics")
json_logger.addHandler(handler)
json_logger.propagate = False
json_logger.info("latency_ms=%d tokens=%d", 420, 812)

# EXPLANATION (LINE BY LINE):
# basicConfig(level=INFO, format=..., stream=sys.stdout) -> one-time setup.
# getLogger("rag.pipeline")      -> a named logger (normally __name__).
# logger.debug(...)              -> NOT shown, because the level is INFO.
# logger.info("... %d chars", len(question)) -> lazy %-style formatting.
# logger.warning(...)            -> something unexpected but recoverable.
# logger.exception(...)          -> ERROR level plus the full traceback.
# JsonFormatter                  -> custom formatter producing JSON lines.
# json_logger.propagate = False  -> don't ALSO send to the root handler (no duplicates).
#
# COMMON MISTAKES:
# 1. Calling basicConfig in library modules (only the application should).
# 2. Using f-strings in log calls everywhere (always formatted, even if hidden).
# 3. Logging secrets, full prompts with personal data, or API keys.
# 4. Duplicate log lines from handlers attached at several levels.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Configure logging at DEBUG level and log one message at each of the five
# levels. Then change the level to WARNING and observe what disappears.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Configure two handlers: console (INFO and above) and a file in a temporary
# folder (DEBUG and above) with different formats. Log some messages and
# print the file's contents to compare.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write a decorator log_llm_call that logs (as JSON) the function name, a
# request id (uuid4), input length, duration in ms, success/failure, and a
# REDACTED version of any argument named api_key. Apply it to a fake LLM
# function that sometimes raises.

# YOUR CODE:

