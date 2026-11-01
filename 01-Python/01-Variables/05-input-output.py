# ======================================
# TOPIC: INPUT AND OUTPUT
# LEVEL: BEGINNER
# ID: python.variables.input-output
# ======================================

# INTRODUCTION
# Programs talk to people: they ask questions and show results.
# input() reads text typed by the user; print() writes text to the screen.
#
# THEORY
# print(*values, sep=" ", end="\n") prints values separated by sep, then end.
# input(prompt) shows the prompt, waits for Enter, and returns a STRING.
# To get numbers, convert: int(input(...)).
# Formatting tools: f-strings with format specs:
#   {x:>10}  right-align in 10 chars     {x:<10} left-align     {x:^10} centre
#   {x:,}    thousands separator         {x:.2f} two decimals
#
# REAL-WORLD ANALOGY
# A cashier: asks "How many items?" (input), hears an answer as words,
# works out the bill (conversion + calculation), and prints a receipt (output).
#
# SYNTAX:
#   answer = input("Question: ")
#   print(a, b, sep=", ", end="!\n")
#
# SMALL WORKING EXAMPLE:
name = input("What is your name? ").strip() or "Learner"
hours = float(input("Hours studied this week? ") or 0)
print("Hello", name, sep=", ", end="!\n")
print(f"{'Name':<10}{'Hours':>8}")
print(f"{name:<10}{hours:>8.1f}")
print(f"Yearly estimate: {hours * 52:,.0f} hours")

# EXPLANATION (LINE BY LINE):
# input(...).strip() or "Learner" -> remove spaces; if empty, use a default.
# float(input(...) or 0)          -> empty answer becomes 0, otherwise convert to float.
# print("Hello", name, sep=", ", end="!\n") -> "Hello, <name>!" on one line.
# f"{'Name':<10}{'Hours':>8}"     -> a header: "Name" left in 10 chars, "Hours" right in 8.
# f"{name:<10}{hours:>8.1f}"      -> same widths so the columns line up.
# f"{hours * 52:,.0f}"            -> no decimals, comma thousands separator.
#
# COMMON MISTAKES:
# 1. Doing maths on input() directly - it is a str.
# 2. Not handling invalid input (ValueError) when converting.
# 3. Using string concatenation with numbers: "Total: " + 5.
# 4. Forgetting that print() adds a newline - use end="" to stay on the line.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Ask the user for two numbers and print their sum, difference and product.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Ask for a number repeatedly until the user types a valid integer
# (handle ValueError), then print it squared.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build a receipt printer: ask for 3 item names and prices, then print a
# receipt with aligned columns, a subtotal, 18% tax and a grand total, all with
# 2 decimals and thousands separators. Put the logic in a function that
# receives the items so it can be tested without typing input.

# YOUR CODE:

