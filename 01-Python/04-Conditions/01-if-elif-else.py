# ======================================
# TOPIC: IF, ELIF AND ELSE
# LEVEL: BEGINNER
# ID: python.conditions.if-elif-else
# ======================================

# INTRODUCTION
# Conditions let a program choose different actions based on data:
# approve or reject, retry or stop, label as spam or not spam.
#
# THEORY
# - if checks a condition; elif checks another if the previous ones failed;
#   else runs when nothing matched. Only ONE branch runs, top to bottom.
# - Blocks are defined by INDENTATION (4 spaces). A colon ends each header line.
# - Any value can be a condition: its truthiness decides (empty -> False).
# - Conditional expression (one line): value_if_true if condition else value_if_false
# - Order matters: put the most specific conditions first.
# - "Guard clauses" (early return) keep nesting shallow.
#
# REAL-WORLD ANALOGY
# A traffic light: if red, stop; elif amber, slow down; else, go.
#
# SYNTAX:
#   if condition:
#       ...
#   elif other_condition:
#       ...
#   else:
#       ...
#
# SMALL WORKING EXAMPLE:
def grade(score):
    if not 0 <= score <= 100:
        return "invalid"
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 50:
        return "C"
    else:
        return "F"

for s in (95, 75, 49, 120):
    print(s, grade(s))
probability = 0.72
label = "spam" if probability >= 0.5 else "not spam"
print(label)
items = []
if items:
    print("processing", len(items), "items")
else:
    print("nothing to process")

# EXPLANATION (LINE BY LINE):
# if not 0 <= score <= 100: return "invalid" -> guard clause handles bad input first.
# if score >= 90 / elif >= 75 / elif >= 50   -> checked in order; first True wins.
# else: return "F"                           -> runs only if nothing above matched.
# for s in (...): print(s, grade(s))         -> test several scores.
# "spam" if probability >= 0.5 else ...      -> one-line conditional expression.
# if items:                                  -> empty list is falsy, so else runs.
#
# COMMON MISTAKES:
# 1. Missing colon or wrong indentation -> SyntaxError / IndentationError.
# 2. Ordering conditions wrongly (score >= 50 first would swallow 95).
# 3. Using several separate ifs when only one branch should run.
# 4. Writing if x == True instead of if x.
# 5. Deeply nested ifs instead of guard clauses or combined conditions.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Given a temperature in Celsius, print "freezing" (<= 0), "cold" (< 15),
# "pleasant" (< 25) or "hot". Test with at least four values.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write shipping_cost(weight_kg, country, is_member): domestic ("IN") costs
# 50 + 20/kg, international 500 + 100/kg, members get 50% off, orders over
# 10 kg get an extra 10% off. Use guard clauses for invalid weight.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write triage_prediction(probabilities) where probabilities is a dict of
# label -> probability. Return:
# - "invalid" if the values do not sum to ~1 (use math.isclose with abs_tol),
# - "uncertain" if the top probability is below 0.6 or the top two are within 0.1,
# - otherwise the top label. Test with 4 different inputs.

# YOUR CODE:

