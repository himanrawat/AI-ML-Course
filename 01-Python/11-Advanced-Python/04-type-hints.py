# ======================================
# TOPIC: TYPE HINTS
# LEVEL: ADVANCED
# ID: python.advanced.type-hints
# ======================================

# INTRODUCTION
# Type hints document what a function expects and returns. Editors use them
# for autocompletion, tools like mypy find bugs before you run the code, and
# libraries like Pydantic and FastAPI use them to validate data.
#
# THEORY
# - Annotate variables and functions: def f(x: int, y: str = "a") -> bool:
# - Hints are NOT enforced at runtime by Python itself.
# - Built-in generics: list[int], dict[str, float], tuple[int, ...], set[str].
# - Optional values: int | None. Several types: int | str.
# - typing module: Any, Literal["a", "b"], TypedDict, Protocol, Callable,
#   Iterable, Iterator, TypeAlias.
# - Generics (Python 3.12+): def first[T](items: list[T]) -> T:
# - Protocol: structural typing - "anything with a .predict() method".
# - Check with a type checker: mypy file.py or pyright.
#
# REAL-WORLD ANALOGY
# Labels on electrical sockets: "230V only". The socket does not stop you
# plugging in the wrong device, but the label prevents most mistakes.
#
# SYNTAX:
#   def f(items: list[str], limit: int | None = None) -> dict[str, int]: ...
#   class Movie(TypedDict): title: str; year: int
#
# SMALL WORKING EXAMPLE:
from collections.abc import Callable, Iterable
from typing import Literal, Protocol, TypedDict

class Prediction(TypedDict):
    label: str
    score: float

class Classifier(Protocol):
    def predict(self, text: str) -> Prediction: ...

class KeywordClassifier:
    def __init__(self, keyword: str) -> None:
        self.keyword = keyword

    def predict(self, text: str) -> Prediction:
        hit = self.keyword in text.lower()
        return {"label": "spam" if hit else "ham", "score": 0.9 if hit else 0.6}

def run_all(model: Classifier, texts: Iterable[str]) -> list[Prediction]:
    return [model.predict(t) for t in texts]

def first[T](items: list[T]) -> T | None:
    return items[0] if items else None

Mode = Literal["train", "eval"]

def set_mode(mode: Mode, callback: Callable[[str], None] = print) -> None:
    callback(f"mode set to {mode}")

results = run_all(KeywordClassifier("win"), ["You WIN a prize", "Meeting at 5"])
print(results)
print(first([3, 1, 2]), first([]))
set_mode("eval")
print(run_all.__annotations__)

# EXPLANATION (LINE BY LINE):
# class Prediction(TypedDict)   -> describes the exact keys and value types of a dict.
# class Classifier(Protocol)    -> any object with a matching predict() fits.
# KeywordClassifier             -> does NOT inherit from Classifier but satisfies it.
# run_all(model: Classifier, texts: Iterable[str]) -> list[Prediction]
#                               -> accepts any iterable of strings.
# def first[T](items: list[T]) -> T | None -> generic: return type follows input type.
# Mode = Literal["train", "eval"] -> only these two strings are valid.
# Callable[[str], None]         -> a function taking a str and returning nothing.
# __annotations__               -> hints are stored, but not enforced, at runtime.
#
# COMMON MISTAKES:
# 1. Thinking hints are checked at runtime (they are not - use a checker or Pydantic).
# 2. Overusing Any, which turns off checking.
# 3. Using List/Dict from typing in new code (use list/dict).
# 4. Forgetting "| None" for parameters that default to None.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Add type hints to: a function average(numbers) returning a float, and a
# function greet(name, times=1) returning a list of strings.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Define a TypedDict for a chat message (role: Literal["user", "assistant"],
# content: str) and type a function format_chat(messages) -> str.
# Install nothing new: run "python -m mypy" only if available, otherwise
# deliberately pass a wrong type and explain what a checker would report.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Define a Protocol Embedder with embed(texts: list[str]) -> list[list[float]].
# Write two implementations (character counts, word lengths) and a generic
# function top_k[T](items: list[T], key: Callable[[T], float], k: int) -> list[T].
# Use them to rank documents by similarity to a query (dot product).

# YOUR CODE:

