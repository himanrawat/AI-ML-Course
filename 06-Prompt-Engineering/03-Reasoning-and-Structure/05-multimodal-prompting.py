# ======================================
# TOPIC: MULTIMODAL PROMPTING (IMAGES AND DOCUMENTS)
# LEVEL: INTERMEDIATE
# ID: prompt-engineering.reasoning.multimodal
# ======================================

# INTRODUCTION
# Modern LLMs read images and PDFs: receipts, charts, screenshots, scanned
# forms, UI mock-ups. Multimodal prompting combines visual input with text
# instructions.
#
# THEORY
# - Content is sent as a LIST of blocks in one message: image blocks
#   ({"type": "image", "source": {"type": "base64", "media_type": "image/png",
#   "data": ...}}), document blocks (PDFs) and text blocks.
# - Put the image/document BEFORE the text instructions that refer to it.
# - Be specific about what to look at: "Read the total in the bottom-right
#   of the receipt", "Compare the two screenshots for layout differences".
# - Ask for structured output (JSON) when extracting from images.
# - Multiple images: label them ("Image 1:", "Image 2:") so instructions can
#   refer to each.
# - Limitations: small text, low resolution, dense tables and precise
#   measurements/counting can be unreliable - verify critical values, or
#   ask the model to quote what it reads.
# - Images cost tokens (roughly proportional to resolution); resize when
#   detail isn't needed.
#
# REAL-WORLD ANALOGY
# Handing a colleague a photo along with a sticky note: "check the date
# printed in the top-left corner" works much better than "look at this".
#
# SYNTAX:
#   content = [image_block, {"type": "text", "text": "instructions"}]
#   messages = [{"role": "user", "content": content}]
#
# SMALL WORKING EXAMPLE:
import base64
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_llm import complete

fig, ax = plt.subplots(figsize=(4, 3))
ax.bar(["Q1", "Q2", "Q3", "Q4"], [120, 135, 90, 160], color="gray")
ax.set_title("Revenue by quarter (k USD)")
buffer = io.BytesIO()
fig.savefig(buffer, format="png", dpi=80)
plt.close(fig)
image_b64 = base64.standard_b64encode(buffer.getvalue()).decode()

content = [
    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_b64}},
    {"type": "text", "text": (
        "This is a bar chart from a quarterly report.\n"
        "1. Read the value of each bar exactly as labelled or estimated from the axis.\n"
        "2. Identify the quarter with the largest drop compared to the previous quarter.\n"
        'Return JSON: {"values": {"Q1": number, ...}, "largest_drop": "Qn", "confidence": "high|low"}')},
]
print("image bytes:", len(buffer.getvalue()), "| blocks:", [block["type"] for block in content])
reply = complete(messages=[{"role": "user", "content": content}], offline=(
    '{"values": {"Q1": 120, "Q2": 135, "Q3": 90, "Q4": 160}, "largest_drop": "Q3", "confidence": "low"}'))
print(reply)

# EXPLANATION (LINE BY LINE):
# matplotlib creates a chart image in memory (no file needed).
# base64.standard_b64encode    -> images are sent as base64 strings.
# content list                 -> image block FIRST, then the text instructions.
# Specific steps               -> read values, then compute the largest drop.
# "confidence" field           -> invites the model to flag uncertain readings
#                                 (bars without value labels are estimates).
# messages=[{"role": "user", "content": content}] -> one user turn with two blocks.
#
# COMMON MISTAKES:
# 1. Vague instructions ("analyse this image").
# 2. Trusting exact numbers read from unlabelled charts.
# 3. Sending huge images when a smaller one is enough.
# 4. Not telling the model which image is which when sending several.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Generate a simple image with matplotlib (e.g. a table of 3 products and
# prices drawn with ax.text) and write a prompt asking for JSON extraction.
# Print the message structure (without the base64 data).

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write build_image_message(paths, instruction) that loads several local
# images, detects media types from file extensions, labels them "Image 1..n",
# and validates size limits. Test with two generated PNGs.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# With API access, create 10 synthetic receipt images with known totals
# (matplotlib text), extract totals with the model, and measure accuracy.
# Then test the effect of image resolution (dpi 40, 80, 150) on accuracy
# and token usage. Summarise the trade-off.

# YOUR CODE:

