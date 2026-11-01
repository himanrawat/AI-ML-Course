"""Shared LLM helper for the Prompt Engineering module.

Topic files import `complete` from here so every example stays short:

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from course_llm import complete

Offline by default: examples return the clearly labelled sample response
passed as `offline`, so every file runs without an API key or cost.

To call a real model:
    export COURSE_USE_LLM=1
    export ANTHROPIC_API_KEY=...        (or run `ant auth login`)
Optional: COURSE_LLM_MODEL (default claude-opus-5-5).

Requests enable server-side refusal fallbacks ("default" routing), so a
request declined by one model's safety classifier is retried on a fallback
model inside the same call.
"""

import os

MODEL = os.environ.get("COURSE_LLM_MODEL", "claude-opus-5-5")
_warned = False


def use_real_llm():
    return os.environ.get("COURSE_USE_LLM") == "1"


def complete(prompt=None, *, system=None, messages=None, max_tokens=2048, offline=None):
    """Return the model's text reply.

    prompt   - a single user message (or pass `messages` for a conversation)
    system   - optional system prompt
    offline  - sample reply used when COURSE_USE_LLM is not set; a string,
               or a function receiving the messages list
    """
    global _warned
    if messages is None:
        messages = [{"role": "user", "content": prompt}]
    if not use_real_llm():
        if offline is None:
            raise RuntimeError("Set COURSE_USE_LLM=1 (and an API key) to run this against a real model.")
        if not _warned:
            print("[offline sample response - set COURSE_USE_LLM=1 to call a real model]")
            _warned = True
        return offline(messages) if callable(offline) else offline

    import anthropic

    client = anthropic.Anthropic()
    kwargs = {"system": system} if system else {}
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=messages,
        output_config={"effort": "medium"},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        **kwargs,
    )
    if response.stop_reason == "refusal":
        raise RuntimeError(f"The model declined this request: {response.stop_details}")
    return "".join(block.text for block in response.content if block.type == "text")
