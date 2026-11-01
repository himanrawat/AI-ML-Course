# ======================================
# TOPIC: PARTIAL DERIVATIVES AND GRADIENTS
# LEVEL: INTERMEDIATE
# ID: math.calculus.gradients
# ======================================

# INTRODUCTION
# Real models have thousands to billions of parameters. The gradient collects
# the slope with respect to EVERY parameter, telling us how to adjust all of
# them at once.
#
# THEORY
# - A PARTIAL DERIVATIVE df/dx_i measures how f changes when ONLY x_i changes,
#   holding the others fixed.
# - The GRADIENT is the vector of all partial derivatives:
#   grad f = [df/dx_1, df/dx_2, ..., df/dx_n].
# - The gradient points in the direction of STEEPEST INCREASE.
#   Its negative points to steepest decrease - that is where we move to
#   reduce the loss.
# - At a minimum, the gradient is the zero vector.
# - For the mean squared error of a linear model y_hat = X @ w:
#   loss = mean((X @ w - y)^2), grad = 2/n * X.T @ (X @ w - y).
#
# REAL-WORLD ANALOGY
# Standing on a hillside in fog: you feel the slope north-south and east-west
# with your feet (partial derivatives); together they tell you which way is
# steepest downhill (negative gradient).
#
# SYNTAX:
#   grad = np.array([partial_1, partial_2, ...])
#
# SMALL WORKING EXAMPLE:
import numpy as np

def f(p):
    x, y = p
    return x ** 2 + 3 * y ** 2

def grad_f(p):
    x, y = p
    return np.array([2 * x, 6 * y])

def numerical_gradient(func, p, h=1e-5):
    g = np.zeros_like(p)
    for i in range(len(p)):
        step = np.zeros_like(p)
        step[i] = h
        g[i] = (func(p + step) - func(p - step)) / (2 * h)
    return g

point = np.array([1.0, 2.0])
print("analytic:", grad_f(point), "numeric:", np.round(numerical_gradient(f, point), 4))
rng = np.random.default_rng(0)
X = rng.normal(size=(50, 3))
true_w = np.array([2.0, -1.0, 0.5])
y = X @ true_w
mse = lambda w: np.mean((X @ w - y) ** 2)
w = np.zeros(3)
analytic = 2 / len(X) * X.T @ (X @ w - y)
print("MSE gradient matches:", np.allclose(analytic, numerical_gradient(mse, w), atol=1e-4))
print("gradient at the true weights:", np.round(2 / len(X) * X.T @ (X @ true_w - y), 6))

# EXPLANATION (LINE BY LINE):
# f(x, y) = x^2 + 3y^2           -> a bowl, steeper along y.
# grad_f = [2x, 6y]              -> partial derivatives by the power rule.
# numerical_gradient             -> nudge one coordinate at a time (gradient checking).
# At (1, 2): gradient [2, 12]    -> steepest increase mostly along y.
# MSE for a linear model         -> loss over 50 examples and 3 weights.
# 2/n * X.T @ (X @ w - y)        -> the analytic gradient (matrix form).
# allclose(...)                  -> numerical check confirms the formula.
# At true_w the gradient is 0    -> we are at the minimum.
#
# COMMON MISTAKES:
# 1. Changing several parameters at once when estimating partial derivatives.
# 2. Moving WITH the gradient when minimizing (you should move against it).
# 3. Shape errors in X.T @ (X @ w - y) - write shapes down.
# 4. Skipping gradient checks when implementing gradients by hand.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Compute by hand the gradient of f(x, y) = 4x + x*y + y^2 at (1, 3).
# Verify with numerical_gradient.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Draw a contour plot of f(x, y) = x^2 + 3y^2 with matplotlib and overlay
# gradient arrows (plt.quiver) on a grid. Comment on how arrows relate to the
# contour lines.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Derive (in comments) the gradient of binary cross-entropy loss for logistic
# regression: loss = -mean(y log p + (1 - y) log(1 - p)), p = sigmoid(X @ w).
# Show it simplifies to X.T @ (p - y) / n, then implement it and verify with a
# numerical gradient check on random data.

# YOUR CODE:

