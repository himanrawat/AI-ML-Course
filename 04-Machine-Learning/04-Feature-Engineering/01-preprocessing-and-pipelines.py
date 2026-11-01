# ======================================
# TOPIC: PREPROCESSING AND PIPELINES
# LEVEL: INTERMEDIATE
# ID: ml.features.pipelines
# ======================================

# INTRODUCTION
# Models need numbers on sensible scales. Real tables mix numeric and text
# columns with missing values. scikit-learn Pipelines package every step so
# training and prediction always transform data identically - without leakage.
#
# THEORY
# - Numeric: impute missing values (SimpleImputer: mean/median), scale
#   (StandardScaler: mean 0, std 1; MinMaxScaler: 0..1), transform skew (log).
# - Categorical: OneHotEncoder (one column per category;
#   handle_unknown="ignore" for unseen categories), OrdinalEncoder for ordered
#   categories (small < medium < large).
# - ColumnTransformer applies different transformers to different columns.
# - Pipeline chains transformers + a final model: fit() fits every step on
#   training data; predict() applies the SAME learned transformations.
# - Feature engineering ideas: ratios, date parts (month, weekday), counts,
#   text length, binning, interactions, domain knowledge.
# - Save the whole fitted pipeline (joblib.dump) to deploy it.
#
# REAL-WORLD ANALOGY
# A factory assembly line: raw materials enter, each station performs a fixed
# step in the same order, and the finished product comes out identical every time.
#
# SYNTAX:
#   pre = ColumnTransformer([("num", num_pipe, num_cols), ("cat", OneHotEncoder(), cat_cols)])
#   model = Pipeline([("pre", pre), ("clf", LogisticRegression())])
#
# SMALL WORKING EXAMPLE:
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

rng = np.random.default_rng(0)
n = 600
df = pd.DataFrame({
    "income": rng.lognormal(10.5, 0.5, n),
    "age": rng.integers(18, 70, n).astype(float),
    "city": rng.choice(["Delhi", "Mumbai", "Pune", "Chennai"], n),
    "signup": pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D"),
})
df.loc[rng.choice(n, 40, replace=False), "age"] = np.nan
y = ((df["income"] > 40_000) & (df["city"] != "Pune")).astype(int)
df["signup_month"] = df["signup"].dt.month
df["log_income"] = np.log(df["income"])
numeric = ["log_income", "age", "signup_month"]
categorical = ["city"]
preprocess = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
])
model = Pipeline([("pre", preprocess), ("clf", LogisticRegression(max_iter=1000))])
print("CV accuracy:", cross_val_score(model, df, y, cv=5).mean().round(3))
model.fit(df, y)
print("features after preprocessing:", model[:-1].get_feature_names_out().tolist())
new = pd.DataFrame({"log_income": [np.log(60_000)], "age": [np.nan], "city": ["Kolkata"], "signup_month": [6]})
print("prediction for unseen city with missing age:", model.predict(new))

# EXPLANATION (LINE BY LINE):
# lognormal income            -> skewed; log transform makes it more symmetric.
# 40 missing ages             -> handled by SimpleImputer(median) inside the pipeline.
# signup_month                -> a simple engineered date feature.
# ColumnTransformer           -> numeric pipeline on numeric columns, one-hot on city.
# Pipeline([("pre", ...), ("clf", ...)]) -> one object to fit, cross-validate and deploy.
# cross_val_score(model, df, y) -> imputer/scaler re-fit per fold: no leakage.
# get_feature_names_out       -> names of the final model's input features.
# Unseen city "Kolkata"       -> handle_unknown="ignore" encodes it as all zeros.
#
# COMMON MISTAKES:
# 1. Preprocessing outside the pipeline with statistics from all data.
# 2. One-hot encoding high-cardinality IDs (thousands of columns).
# 3. Forgetting handle_unknown="ignore" -> crashes in production.
# 4. Different preprocessing code at training and serving time.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Scale [[1, 200], [2, 300], [3, 400]] with StandardScaler and MinMaxScaler,
# print the results, and inverse_transform them back.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Build a pipeline for a dataset with 3 numeric, 2 categorical and 1 ordinal
# column (sizes S/M/L) including imputation. Save it with joblib, load it in a
# fresh variable, and confirm predictions are identical.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write a custom transformer DateFeatures(BaseEstimator, TransformerMixin) that
# expands a datetime column into year, month, weekday, is_weekend and
# days_since_reference (reference learned in fit from the training data).
# Use it inside a ColumnTransformer and make get_feature_names_out work.

# YOUR CODE:

