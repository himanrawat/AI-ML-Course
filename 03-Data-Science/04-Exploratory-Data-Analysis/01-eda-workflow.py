# ======================================
# TOPIC: THE EXPLORATORY DATA ANALYSIS WORKFLOW
# LEVEL: INTERMEDIATE
# ID: data-science.eda.workflow
# ======================================

# INTRODUCTION
# EDA is how you get to know a dataset before modelling: its size, quality,
# distributions, relationships and surprises. Skipping it is the most common
# cause of models that look good but fail in reality.
#
# THEORY
# A repeatable EDA checklist:
#  1. Understand the question and what each row represents.
#  2. Structure: shape, dtypes, memory, a few sample rows.
#  3. Quality: missing values, duplicates, impossible values, inconsistent labels.
#  4. Univariate: distribution of each feature (describe, histograms,
#     value_counts) and of the TARGET (class balance!).
#  5. Bivariate: each feature vs the target (groupby means, scatter, boxplots),
#     feature-feature correlations.
#  6. Leakage check: features that would not be available at prediction time
#     or that perfectly predict the target.
#  7. Write down findings and decisions (what to clean, transform, drop).
#
# REAL-WORLD ANALOGY
# A doctor's check-up before treatment: vital signs, history and tests come
# first; prescribing without them is guesswork.
#
# SYNTAX:
#   df.info(); df.describe(include="all"); df.isna().mean()
#   df.groupby("target")[features].mean()
#
# SMALL WORKING EXAMPLE:
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
n = 500
df = pd.DataFrame({
    "tenure_months": rng.integers(1, 72, n),
    "monthly_charge": rng.normal(70, 20, n).round(2),
    "support_tickets": rng.poisson(1.5, n),
    "plan": rng.choice(["basic", "pro", "enterprise"], n, p=[0.6, 0.3, 0.1]),
})
risk = 0.04 * df["support_tickets"] - 0.01 * df["tenure_months"] + 0.3
df["churned"] = (rng.random(n) < risk.clip(0.02, 0.9)).astype(int)
df.loc[rng.choice(n, 20, replace=False), "monthly_charge"] = np.nan
df["cancel_reason_given"] = np.where(df["churned"] == 1, "yes", "no")

print("shape:", df.shape)
print("missing %:", (df.isna().mean() * 100).round(1)[lambda s: s > 0].to_dict())
print("target balance:", df["churned"].value_counts(normalize=True).round(3).to_dict())
print(df.groupby("churned")[["tenure_months", "support_tickets", "monthly_charge"]].mean().round(2))
print(df.groupby("plan")["churned"].mean().round(3).to_dict())
numeric = df.select_dtypes("number")
print(numeric.corr()["churned"].drop("churned").round(3).to_dict())
leak = pd.crosstab(df["cancel_reason_given"], df["churned"])
print("possible leakage:\n", leak)

# EXPLANATION (LINE BY LINE):
# A synthetic churn dataset: churn risk rises with tickets, falls with tenure.
# 20 monthly_charge values are removed to simulate missing data.
# cancel_reason_given is only known AFTER a customer churns -> a leaky feature.
# isna().mean()                -> fraction missing per column (only non-zero shown).
# value_counts(normalize=True) -> the target is imbalanced (most customers stay).
# groupby("churned").mean()    -> churners have shorter tenure, more tickets.
# corr()["churned"]            -> quick numeric signal check.
# crosstab                     -> cancel_reason_given predicts churn perfectly:
#                                 it must be removed before modelling.
#
# COMMON MISTAKES:
# 1. Jumping straight to model training.
# 2. Ignoring class imbalance (accuracy will look deceptively high).
# 3. Missing leakage: "too good to be true" features.
# 4. Doing EDA on the test set and letting it influence decisions.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Run steps 2-4 of the checklist on sklearn's load_wine(as_frame=True) data
# and write 3 observations as comments.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# For the churn data above, create 4 charts answering: does churn differ by
# plan? by tenure band (pd.cut)? by number of tickets? is monthly_charge
# different for churners? Summarise findings in comments.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write an automated eda_report(df, target) function that prints the full
# checklist (structure, quality, univariate, target balance, top correlated
# features, possible leakage = any feature whose groupby-target table is
# nearly deterministic) and saves charts to a folder. Run it on two datasets.

# YOUR CODE:

