# ======================================
# TOPIC: DERIVATIVES
# LEVEL: BEGINNER
# ID: math.calculus.derivatives
# ======================================

# INTRODUCTION
# Training a model means adjusting parameters to reduce error. The derivative
# tells you which direction reduces the error and how strongly - it is the
# "steering wheel" of machine learning. (Study with linear regression.)
#
# THEORY
# - The derivative f'(x) is the instantaneous RATE OF CHANGE of f at x: the
#   slope of the tangent line.
# - Definition: f'(x) = limit as h -> 0 of (f(x + h) - f(x)) / h.
# - Numerically: central difference (f(x + h) - f(x - h)) / (2h) with small h.
# - Rules: d/dx c = 0;  d/dx x^n = n x^(n-1);  d/dx e^x = e^x;
#   d/dx ln x = 1/x;  sum rule: (f + g)' = f' + g'.
# - f'(x) > 0: f increases; f'(x) < 0: f decreases; f'(x) = 0: a flat point
#   (possible minimum or maximum).
# - Loss functions like (prediction - target)^2 are minimized where the
#   derivative is zero.
#
# REAL-WORLD ANALOGY
# A car's speedometer: position changes over time, and the speedometer shows
# how fast it is changing right NOW - that is a derivative.
#
# SYNTAX:
#   def derivative(f, x, h=1e-5): return (f(x + h) - f(x - h)) / (2 * h)
#
# SMALL WORKING EXAMPLE:
import math

def derivative(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)

def f(x):
    return x ** 2 - 4 * x + 5

def f_prime(x):
    return 2 * x - 4

for x in [0, 1, 2, 3]:
    print(f"x={x}: numeric={derivative(f, x):.4f} exact={f_prime(x)}")
print("e^x slope at 1:", round(derivative(math.exp, 1), 4), "e =", round(math.e, 4))
target = 3.0
loss = lambda w: (2 * w - target) ** 2
print("loss slope at w=0:", round(derivative(loss, 0.0), 3))
print("loss slope at w=1.5:", round(derivative(loss, 1.5), 3))

# EXPLANATION (LINE BY LINE):
# derivative(f, x)          -> estimates the slope with a tiny step h on both sides.
# f(x) = x^2 - 4x + 5       -> a parabola with its minimum at x = 2.
# f_prime(x) = 2x - 4       -> power rule; zero at x = 2 (the minimum).
# numeric vs exact          -> the numerical estimate matches the rule.
# derivative(math.exp, 1)   -> equals e: e^x is its own derivative.
# loss(w) = (2w - 3)^2      -> a one-parameter "model" predicting 2w for target 3.
# slope at w=0 is negative  -> increasing w reduces the loss.
# slope at w=1.5 is 0       -> 2 * 1.5 = 3, perfect prediction: the minimum.
#
# COMMON MISTAKES:
# 1. Choosing h too large (inaccurate) or too tiny (floating-point noise).
# 2. Confusing the function's value with its slope.
# 3. Assuming slope 0 always means a minimum (could be a maximum or plateau).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Using the power rule, write the derivatives of 3x^3, 5x^2 - 2x and 7 as
# comments, then verify each numerically at x = 2.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Plot (matplotlib) f(x) = x^3 - 3x and its derivative on [-3, 3]. Mark the
# points where the derivative is zero and say which is a minimum and which a
# maximum.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Study how the numerical derivative error depends on h: for f(x) = sin(x) at
# x = 1, compute the error of forward and central differences for h = 10^-1
# down to 10^-12 and print a table. Explain the U-shaped error curve.

# YOUR CODE:

