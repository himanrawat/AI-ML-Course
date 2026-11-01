# ======================================
# TOPIC: GRADIENT DESCENT
# LEVEL: INTERMEDIATE
# ID: math.calculus.gradient-descent
# ======================================

# INTRODUCTION
# Gradient descent is THE optimisation algorithm of machine learning: from
# linear regression to large language models, parameters are learned by
# repeatedly stepping against the gradient.
#
# THEORY
# - Start with initial parameters w. Repeat:
#     w = w - learning_rate * gradient_of_loss(w)
# - LEARNING RATE: too small -> slow; too large -> overshoots or diverges.
# - Batch GD uses all data per step; STOCHASTIC GD (SGD) uses one example;
#   MINI-BATCH GD uses small batches (the standard in deep learning).
# - Stop when the loss stops improving, the gradient is tiny, or after a
#   fixed number of steps/epochs.
# - Improvements: momentum (keeps moving in consistent directions), Adam
#   (adapts the step size per parameter).
# - Feature scaling makes gradient descent converge much faster.
#
# REAL-WORLD ANALOGY
# Walking down a foggy mountain: feel the slope, take a step downhill, repeat.
# Huge steps may jump over the valley; tiny steps take all day.
#
# SYNTAX:
#   for step in range(n_steps):
#       w -= lr * grad(w)
#
# SMALL WORKING EXAMPLE:
import numpy as np

rng = np.random.default_rng(1)
X = rng.uniform(0, 10, size=100)
y = 3.0 * X + 7.0 + rng.normal(scale=1.0, size=100)

def train(lr, steps=500):
    w, b = 0.0, 0.0
    for step in range(steps):
        error = (w * X + b) - y
        grad_w = 2 * np.mean(error * X)
        grad_b = 2 * np.mean(error)
        w -= lr * grad_w
        b -= lr * grad_b
        if abs(w) > 1e6:
            return None, None, step
    return w, b, steps

for lr in [0.0001, 0.01, 0.05]:
    w, b, steps = train(lr)
    if w is None:
        print(f"lr={lr}: diverged after {steps} steps")
    else:
        loss = np.mean((w * X + b - y) ** 2)
        print(f"lr={lr}: w={w:.2f} b={b:.2f} loss={loss:.2f}")

# EXPLANATION (LINE BY LINE):
# y = 3x + 7 + noise              -> data with known true parameters.
# error = prediction - y          -> residuals for all 100 points.
# grad_w = 2 * mean(error * X)    -> derivative of MSE with respect to w.
# grad_b = 2 * mean(error)        -> derivative with respect to b.
# w -= lr * grad_w                -> the gradient descent update.
# lr=0.0001 -> too slow: after 500 steps w, b are still far from (3, 7).
# lr=0.01   -> close to w=3; b (~6.3) is still creeping toward 7 - the intercept
#              converges more slowly because x is not centred (see Question 3).
# lr=0.05   -> too large: each step overshoots further and |w| explodes; we stop
#              once |w| > 1e6 instead of waiting for overflow.
#
# COMMON MISTAKES:
# 1. Adding the gradient instead of subtracting it.
# 2. Not scaling features, so one learning rate cannot suit all parameters.
# 3. Judging training by one run without plotting the loss curve.
# 4. Updating w before computing b's gradient with the old w (keep updates
#    simultaneous).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Minimise f(x) = (x - 5)^2 with gradient descent starting at x = 0 and
# learning rate 0.1. Print x every 5 steps for 30 steps.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Modify train() to record the loss at every step and plot loss curves for
# three learning rates on one matplotlib chart (log scale y-axis).

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Implement mini-batch SGD with shuffling each epoch, plus momentum, for
# multi-feature linear regression (X with 3 features of very different
# scales). Compare convergence with and without standardizing the features.
# Compare your final weights with np.linalg.lstsq.

# YOUR CODE:

