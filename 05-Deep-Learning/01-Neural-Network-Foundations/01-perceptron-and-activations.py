# ======================================
# TOPIC: NEURONS, PERCEPTRONS AND ACTIVATION FUNCTIONS
# LEVEL: INTERMEDIATE
# ID: deep-learning.foundations.neurons-activations
# ======================================

# INTRODUCTION
# Every neural network - from image classifiers to GPT - is built from one
# simple unit: a weighted sum followed by a non-linear function.
#
# THEORY
# - A NEURON computes z = w . x + b, then an ACTIVATION a = f(z).
#   (Logistic regression is exactly one neuron with a sigmoid.)
# - A LAYER is many neurons in parallel: a = f(X @ W + b).
# - Without non-linear activations, stacked layers collapse into ONE linear
#   layer - the network could only learn straight-line boundaries.
# - Common activations:
#   SIGMOID 1/(1+e^-z): (0, 1); saturates -> vanishing gradients; used for
#     binary outputs.
#   TANH: (-1, 1), zero-centred, also saturates.
#   RELU max(0, z): simple, fast, the default for hidden layers; "dead" units
#     can get stuck at 0.
#   GELU / SiLU: smooth ReLU variants used in transformers.
#   SOFTMAX: turns a vector of scores into probabilities (multi-class output).
# - The perceptron (1958) learns a linear boundary; it cannot solve XOR -
#   which motivated multi-layer networks.
#
# REAL-WORLD ANALOGY
# A neuron is a committee member who weighs evidence (weights), adds their own
# bias, and then decides how strongly to speak up (activation).
#
# SYNTAX:
#   z = X @ W + b;  a = np.maximum(0, z)
#
# SMALL WORKING EXAMPLE:
import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def relu(z):
    return np.maximum(0, z)

def gelu(z):
    return 0.5 * z * (1 + np.tanh(np.sqrt(2 / np.pi) * (z + 0.044715 * z ** 3)))

z = np.array([-3.0, -1.0, 0.0, 1.0, 3.0])
print("sigmoid:", sigmoid(z).round(3))
print("tanh:   ", np.tanh(z).round(3))
print("relu:   ", relu(z))
print("gelu:   ", gelu(z).round(3))
print("sigmoid slope at 0 and 5:", (sigmoid(0) * (1 - sigmoid(0))).round(3), (sigmoid(5) * (1 - sigmoid(5))).round(4))

def perceptron_train(X, y, epochs=20, lr=0.1):
    w, b = np.zeros(X.shape[1]), 0.0
    for _ in range(epochs):
        for xi, yi in zip(X, y):
            prediction = int(xi @ w + b > 0)
            w += lr * (yi - prediction) * xi
            b += lr * (yi - prediction)
    return w, b

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
for name, y in [("AND", np.array([0, 0, 0, 1])), ("XOR", np.array([0, 1, 1, 0]))]:
    w, b = perceptron_train(X, y)
    predictions = (X @ w + b > 0).astype(int)
    print(f"{name}: predictions {predictions.tolist()} target {y.tolist()} solved={np.array_equal(predictions, y)}")

# EXPLANATION (LINE BY LINE):
# sigmoid/tanh squash values; relu zeroes negatives; gelu is a smooth relu.
# sigmoid slope is 0.25 at 0 but ~0.0066 at 5 -> saturation (vanishing gradients).
# perceptron_train: predict 0/1, then nudge weights by (target - prediction) * input.
# AND is linearly separable -> solved.
# XOR is not linearly separable -> a single perceptron can never solve it.
#
# COMMON MISTAKES:
# 1. Forgetting activations between layers (network stays linear).
# 2. Using sigmoid in deep hidden layers (vanishing gradients).
# 3. Applying softmax AND a loss that already includes it (double softmax).
# 4. Initialising all weights to the same value (neurons learn the same thing).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Plot sigmoid, tanh, ReLU and GELU and their derivatives on [-5, 5] in a 2x4
# subplot grid. Describe in comments where each gradient vanishes.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Solve XOR with a 2-layer network whose weights you set BY HAND (e.g. hidden
# units computing OR and NAND, output computing AND). Verify all four outputs.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Show that stacking 5 linear layers (no activation) with random weights is
# equivalent to one matrix. Then add ReLU and show the function is no longer
# expressible as a single matrix (fit a linear regression to its outputs and
# report the error).

# YOUR CODE:

