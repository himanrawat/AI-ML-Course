# ======================================
# TOPIC: DATACLASSES AND ENUMS
# LEVEL: INTERMEDIATE
# ID: python.oop.dataclasses-enums
# ======================================

# INTRODUCTION
# Many classes just hold data: an experiment result, an API message, a config.
# dataclasses write the boring code (__init__, __repr__, __eq__) for you, and
# enums give names to a fixed set of choices.
#
# THEORY
# - @dataclass generates __init__, __repr__ and __eq__ from type-annotated fields.
# - field(default_factory=list) gives each instance its own mutable default.
# - frozen=True makes instances immutable (and hashable).
# - order=True adds <, > comparisons based on field order.
# - __post_init__ runs after the generated __init__ for validation/derived fields.
# - asdict() converts to a dict (useful for JSON).
# - Enum defines named constants: Status.SUCCESS. StrEnum members are also strings.
#
# REAL-WORLD ANALOGY
# A pre-printed form: the fields are already laid out, you just fill them in.
# An enum is a drop-down menu: only listed options are allowed.
#
# SYNTAX:
#   @dataclass
#   class Point:
#       x: float
#       y: float = 0.0
#   class Color(Enum):
#       RED = "red"
#
# SMALL WORKING EXAMPLE:
from dataclasses import asdict, dataclass, field
from enum import StrEnum

class Role(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

@dataclass
class Message:
    role: Role
    content: str

@dataclass
class Conversation:
    title: str
    messages: list[Message] = field(default_factory=list)

    def add(self, role, content):
        self.messages.append(Message(Role(role), content))

@dataclass(frozen=True, order=True)
class Score:
    value: float
    model: str

    def __post_init__(self):
        if not 0 <= self.value <= 1:
            raise ValueError("score must be between 0 and 1")

chat = Conversation("demo")
chat.add("user", "Hello")
chat.add("assistant", "Hi! How can I help?")
print(chat.messages[0])
print(asdict(chat)["messages"][1])
print(sorted([Score(0.9, "b"), Score(0.7, "a")]))
print(Role.USER == "user", [r.value for r in Role])

# EXPLANATION (LINE BY LINE):
# class Role(StrEnum)          -> fixed set of message roles; members are also strings.
# @dataclass class Message     -> __init__(role, content) and __repr__ are generated.
# messages: list[Message] = field(default_factory=list) -> a new list per conversation.
# Role(role)                   -> converts "user" to Role.USER; invalid values raise.
# @dataclass(frozen=True, order=True) -> immutable and sortable by (value, model).
# __post_init__                -> validation after the generated __init__.
# asdict(chat)                 -> nested dicts, ready for json.dumps.
#
# COMMON MISTAKES:
# 1. messages: list = [] -> ValueError: mutable default (use default_factory).
# 2. Forgetting type annotations - un-annotated names are NOT fields.
# 3. Trying to modify a frozen dataclass -> FrozenInstanceError.
# 4. Using plain strings everywhere instead of an Enum for fixed choices.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create a dataclass Product(name, price, in_stock=True). Create three
# products, print them, and compare two equal products with ==.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Create an Enum Priority (LOW, MEDIUM, HIGH) and a dataclass Ticket with
# title, priority and tags (list, default empty). Sort tickets by priority
# (highest first) and convert them to a JSON string.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Model an ML experiment log: a frozen dataclass Metric(name, value), a
# dataclass Experiment(name, params: dict, metrics: list[Metric], status: Enum)
# with __post_init__ validation, a method best(metric_name) and a classmethod
# from_dict. Round-trip an experiment through JSON and assert equality.

# YOUR CODE:

