# ======================================
# TOPIC: THE CHAIN RULE
# LEVEL: INTERMEDIATE
# ID: math.calculus.chain-rule
# ======================================

# INTRODUCTION
# A neural network is a chain of functions: layer after layer. Backpropagation
# - how every network learns - is just the chain rule applied systematically.
# (Study with 05-Deep-Learning neural networks from scratch.)
#
# THEORY
# - For a composition y = f(g(x)): dy/dx = f'(g(x)) * g'(x).
#   "Derivative of the outer at the inner, times derivative of the inner."
# - For longer chains, multiply the local derivatives along the path:
#   x -> a -> b -> L:  dL/dx = dL/db * db/da * da/dx.
# - BACKPROPAGATION computes these products from the output backwards, reusing
#   intermediate results, so the gradient for every parameter costs about as
#   much as one forward pass.
# - Computational graphs: each node knows its local derivative; gradients flow
#   backwards along the edges.
# - Vanishing gradients: multiplying many small local derivatives (e.g. sigmoid
#   slopes <= 0.25) makes early-layer gradients tiny.
#
# REAL-WORLD ANALOGY
# Currency conversion: rupees -> dollars -> euros. The rupee-to-euro rate is
# the product of the two rates along the chain.
#
# SYNTAX:
#   dL_dx = dL_db * db_da * da_dx
#
# SMALL WORKING EXAMPLE:
import math

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

x, w, b, target = 2.0, 0.5, -0.3, 1.0
z = w * x + b
p = sigmoid(z)
loss = (p - target) ** 2
dloss_dp = 2 * (p - target)
dp_dz = p * (1 - p)
dz_dw = x
dloss_dw = dloss_dp * dp_dz * dz_dw
print(f"z={z:.3f} p={p:.3f} loss={loss:.4f}")
print(f"dloss/dw by chain rule = {dloss_dw:.5f}")

def loss_for(w_value):
    return (sigmoid(w_value * x + b) - target) ** 2

h = 1e-6
numeric = (loss_for(w + h) - loss_for(w - h)) / (2 * h)
print(f"numerical check         = {numeric:.5f}")
slopes = [0.25] * 10
product = math.prod(slopes)
print(f"10 sigmoid layers can shrink a gradient by {product:.2e}")

# EXPLANATION (LINE BY LINE):
# Forward pass: z = w*x + b -> p = sigmoid(z) -> loss = (p - target)^2.
# dloss_dp = 2(p - target)     -> derivative of the squared error.
# dp_dz = p(1 - p)             -> the sigmoid's derivative.
# dz_dw = x                    -> derivative of w*x + b with respect to w.
# dloss_dw = product of the three local derivatives (the chain rule).
# The numerical check gives the same number.
# 0.25 ** 10                   -> why deep sigmoid networks suffered from
#                                 vanishing gradients (and why ReLU helps).
#
# COMMON MISTAKES:
# 1. Forgetting to evaluate the outer derivative AT the inner value.
# 2. Dropping one factor from a long chain.
# 3. Thinking backpropagation is different from the chain rule (it is the same,
#    organised efficiently).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Differentiate y = (3x + 1)^2 with the chain rule (comment), and check
# numerically at x = 2.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# For L = (tanh(w2 * relu(w1 * x)) - y)^2, compute dL/dw1 and dL/dw2 by hand
# using the chain rule for x=1.5, w1=0.8, w2=-0.4, y=0.2. Verify both
# numerically.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build a tiny automatic differentiation engine: a Value class storing data,
# grad and a _backward function, supporting +, *, and tanh, plus backward()
# using a topological sort. Use it to compute gradients of a small expression
# and compare with numerical derivatives. (This is how PyTorch autograd works.)

# YOUR CODE:

