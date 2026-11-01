# ======================================
# TOPIC: MATPLOTLIB BASICS
# LEVEL: BEGINNER
# ID: data-science.visualization.matplotlib
# ======================================

# INTRODUCTION
# A chart can reveal in seconds what a table hides: a trend, an outlier, a
# training run that diverged. Matplotlib is Python's core plotting library.
#
# THEORY
# - Use the object-oriented API: fig, ax = plt.subplots(); ax.plot(...).
#   fig is the whole image; ax is one chart (axes). Several: plt.subplots(2, 2).
# - Common plots: ax.plot (lines/trends), ax.scatter (relationships),
#   ax.bar (categories), ax.hist (distributions), ax.boxplot (spread/outliers).
# - Always label: ax.set_title, ax.set_xlabel, ax.set_ylabel, ax.legend().
# - fig.tight_layout() avoids overlaps; fig.savefig("plot.png", dpi=150) saves.
# - plt.show() opens a window (in scripts) - in notebooks charts show inline.
# - Choose the chart by the question: change over time -> line; compare
#   categories -> bar; distribution -> histogram; relationship -> scatter.
#
# REAL-WORLD ANALOGY
# A car dashboard: instead of reading raw sensor numbers, you glance at
# gauges and warning lights to understand the state immediately.
#
# SYNTAX:
#   fig, ax = plt.subplots(figsize=(8, 4))
#   ax.plot(x, y, label="train"); ax.legend(); plt.show()
#
# SMALL WORKING EXAMPLE:
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(0)
epochs = np.arange(1, 31)
train_loss = 1 / epochs ** 0.5 + rng.normal(0, 0.01, 30)
val_loss = 1 / epochs ** 0.5 + 0.002 * (epochs - 12).clip(0) ** 1.5 + 0.05
fig, axes = plt.subplots(1, 3, figsize=(13, 4))
axes[0].plot(epochs, train_loss, label="train")
axes[0].plot(epochs, val_loss, label="validation")
axes[0].axvline(epochs[val_loss.argmin()], linestyle="--", color="gray", label="best epoch")
axes[0].set(title="Loss curves", xlabel="epoch", ylabel="loss")
axes[0].legend()
axes[1].hist(rng.normal(170, 10, 1000), bins=30)
axes[1].set(title="Height distribution", xlabel="cm", ylabel="count")
x = rng.uniform(0, 10, 80)
axes[2].scatter(x, 3 * x + rng.normal(0, 3, 80), alpha=0.6)
axes[2].set(title="Hours vs score", xlabel="hours", ylabel="score")
fig.tight_layout()
print("best epoch:", epochs[val_loss.argmin()])
plt.show()

# EXPLANATION (LINE BY LINE):
# plt.subplots(1, 3)             -> one figure with three side-by-side axes.
# axes[0].plot(...) twice        -> train and validation loss on one chart.
# axvline at argmin of val_loss  -> marks where overfitting starts (best epoch).
# ax.set(title=..., xlabel=...)  -> set several properties at once.
# axes[1].hist(..., bins=30)     -> distribution of 1000 simulated heights.
# axes[2].scatter(..., alpha=0.6) -> relationship between two variables.
# tight_layout()                 -> fixes overlapping labels.
# plt.show()                     -> opens the window when run as a script.
#
# COMMON MISTAKES:
# 1. Charts without titles, axis labels or units.
# 2. Mixing plt.* state-machine calls with ax.* calls confusingly.
# 3. Too many bins/too few bins hiding the shape of a distribution.
# 4. Pie charts / 3D effects that distort comparisons.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Plot y = x^2 and y = 2^x for x in [0, 6] on one chart with a legend, title,
# axis labels and a grid. Save it as a PNG in a temporary folder.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Create a 2x2 dashboard for the Iris dataset (sklearn load_iris): histogram
# of one feature per class, scatter of two features coloured by class, bar
# chart of class counts, and a boxplot per class.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write plot_training_history(history: dict[str, list[float]]) that plots any
# number of metrics in a grid of subplots (2 columns, as many rows as needed),
# marks the best value of each metric, shares the x-axis, and returns the
# figure. Test it with fake loss/accuracy/f1 histories.

# YOUR CODE:

