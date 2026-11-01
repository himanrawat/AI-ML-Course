# ======================================
# TOPIC: STREAMING AND CONVERSATION STATE
# LEVEL: INTERMEDIATE
# ID: generative-ai.apis.streaming-conversations
# ======================================

# INTRODUCTION
# Chat products feel fast because they STREAM tokens as they are generated,
# and feel coherent because the app manages conversation state. Both are
# application-engineering problems around the model call.
#
# THEORY
# - STREAMING: the API sends events as tokens are produced (server-sent events).
#   Time-to-first-token drops from seconds to milliseconds; total time is the
#   same. Use it for long outputs and chat UIs (and to avoid HTTP timeouts on
#   very long generations). Python SDK: with client.messages.stream(...) as s:
#   for text in s.text_stream: ...; s.get_final_message() for the full result.
# - On the web, stream to the browser with SSE or WebSockets (a familiar
#   frontend pattern).
# - CONVERSATION STATE lives in YOUR app: store messages per session, resend
#   them each turn, trim/summarise when long, persist to a database.
# - Append the model's full reply (as returned) to history each turn.
# - Handle interruptions: a user may cancel mid-stream; keep partial text if
#   useful, and make retries idempotent.
#
# REAL-WORLD ANALOGY
# A live sports commentary versus a match report: the commentary (streaming)
# starts immediately and continues as play happens; the report arrives at the end.
#
# SYNTAX:
#   with client.messages.stream(model=..., max_tokens=..., messages=...) as stream:
#       for text in stream.text_stream: print(text, end="")
#
# SMALL WORKING EXAMPLE:
import os
import time
from dataclasses import dataclass, field

def fake_stream(text, delay=0.01):
    for word in text.split(" "):
        time.sleep(delay)
        yield word + " "

def real_stream(messages):
    from anthropic import Anthropic
    with Anthropic().messages.stream(model="claude-opus-5-5", max_tokens=16000, messages=messages) as stream:
        yield from stream.text_stream

@dataclass
class ChatSession:
    session_id: str
    messages: list = field(default_factory=list)

    def ask(self, user_text, offline_answer):
        self.messages.append({"role": "user", "content": user_text})
        chunks = real_stream(self.messages) if os.environ.get("COURSE_USE_LLM") == "1" else fake_stream(offline_answer)
        start = time.perf_counter()
        first_token_at, parts = None, []
        for chunk in chunks:
            if first_token_at is None:
                first_token_at = time.perf_counter() - start
            print(chunk, end="", flush=True)
            parts.append(chunk)
        reply = "".join(parts).strip()
        self.messages.append({"role": "assistant", "content": reply})
        print(f"\n  [first token {first_token_at * 1000:.0f} ms, total {(time.perf_counter() - start) * 1000:.0f} ms]")
        return reply

chat = ChatSession("demo-1")
chat.ask("What is a vector database?", "A vector database stores embeddings and finds the most similar ones quickly.")
chat.ask("Name one.", "Examples include pgvector, Qdrant and Chroma.")
print("stored turns:", [m["role"] for m in chat.messages])

# EXPLANATION (LINE BY LINE):
# fake_stream                -> yields words with a delay, imitating a token stream offline.
# real_stream                -> SDK streaming helper; text_stream yields text deltas.
# ChatSession                -> app-owned state: the message list per session.
# ask()                      -> append user turn, stream the reply while printing it,
#                               measure time-to-first-token, append the assistant turn.
# The second question "Name one." only makes sense because history is resent.
#
# COMMON MISTAKES:
# 1. Waiting for the full response before showing anything in a chat UI.
# 2. Forgetting to append the assistant reply to history.
# 3. Unbounded history growth (cost, latency, context limits).
# 4. Losing state on server restarts (persist sessions).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Add a method reset() and a method transcript() that returns the conversation
# as readable text. Test a 3-turn chat offline.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Persist ChatSession to SQLite (sessions and messages tables) so a
# conversation survives restarting the script; load it by session_id.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build a FastAPI endpoint POST /chat/{session_id} that streams the reply to
# the browser with Server-Sent Events (StreamingResponse), plus a tiny HTML page
# using EventSource to display tokens as they arrive. Use fake_stream offline.

# YOUR CODE:

