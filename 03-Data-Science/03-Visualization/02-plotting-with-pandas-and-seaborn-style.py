# ======================================
# TOPIC: PLOTTING DATAFRAMES AND CORRELATION HEATMAPS
# LEVEL: INTERMEDIATE
# ID: data-science.visualization.dataframe-plots
# ======================================

# INTRODUCTION
# During exploration you want charts in one line, straight from a DataFrame.
# pandas wraps matplotlib for this, and a correlation heatmap summarises how
# every numeric feature relates to every other one.
#
# THEORY
# - df.plot(kind="line" | "bar" | "barh" | "hist" | "box" | "scatter"),
#   df["col"].plot.hist(), df.plot.scatter(x=..., y=...).
# - Every pandas plot returns a matplotlib Axes, so you can customise it.
# - Group then plot: df.groupby("cat")["value"].mean().plot.bar().
# - A HEATMAP shows a matrix with colours: ax.imshow(matrix, cmap=...), plus
#   fig.colorbar. Use a DIVERGING colormap (e.g. "coolwarm") centred at 0 for
#   correlations (vmin=-1, vmax=1).
# - Annotate cells with ax.text for exact values.
# - Seaborn (optional extra library) offers statistical plots with less code;
#   here we stay with pandas + matplotlib.
#
# REAL-WORLD ANALOGY
# A heat map of a city at night from a satellite: bright areas show where the
# activity is, without reading a single number.
#
# SYNTAX:
#   ax = df.plot.scatter(x="a", y="b")
#   im = ax.imshow(df.corr(), cmap="coolwarm", vmin=-1, vmax=1)
#
# SMALL WORKING EXAMPLE:
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_diabetes

df = load_diabetes(as_frame=True).frame[["age", "bmi", "bp", "s5", "target"]]
corr = df.corr().round(2)
print(corr["target"].sort_values(ascending=False))
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
df.plot.scatter(x="bmi", y="target", alpha=0.5, ax=axes[0], title="BMI vs disease progression")
im = axes[1].imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
axes[1].set_xticks(range(len(corr)), corr.columns, rotation=45)
axes[1].set_yticks(range(len(corr)), corr.columns)
for i in range(len(corr)):
    for j in range(len(corr)):
        axes[1].text(j, i, corr.iloc[i, j], ha="center", va="center", fontsize=8)
axes[1].set_title("Correlation matrix")
fig.colorbar(im, ax=axes[1])
fig.tight_layout()
pd.cut(df["bmi"], 4).value_counts().sort_index().plot.bar(title="BMI bins")
plt.show()

# EXPLANATION (LINE BY LINE):
# load_diabetes(as_frame=True)   -> a built-in dataset (already scaled features).
# df.corr()                      -> pairwise Pearson correlations.
# corr["target"].sort_values     -> which features relate most to the target.
# df.plot.scatter(..., ax=axes[0]) -> pandas plotting onto a chosen axes.
# imshow(corr, cmap="coolwarm", vmin=-1, vmax=1) -> diverging colours centred at 0.
# set_xticks(positions, labels)  -> feature names on the axes.
# ax.text(...) in a double loop  -> write each correlation value in its cell.
# pd.cut(df["bmi"], 4)           -> bin a numeric column, then bar-plot the counts.
#
# COMMON MISTAKES:
# 1. Using a sequential colormap for correlations (hides negative values).
# 2. Not fixing vmin/vmax, so colours mean different things on each chart.
# 3. Over-interpreting correlation between features as causal.
# 4. Huge unreadable heatmaps - select the relevant features.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create a DataFrame of monthly sales for 3 products over 12 months and plot
# it as a line chart and as a stacked bar chart with pandas.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# For the Iris DataFrame, plot a correlation heatmap with annotations, and a
# boxplot of every feature grouped by species (df.boxplot(by=...)).

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write a scatter_matrix-style function pair_plot(df, hue) using matplotlib
# subplots: histograms on the diagonal, scatter plots elsewhere, coloured by
# the hue column, with shared axes. Test it on the Iris data.

# YOUR CODE:

