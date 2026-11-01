# ======================================
# TOPIC: CLEANING DATA WITH PANDAS
# LEVEL: INTERMEDIATE
# ID: data-science.pandas.cleaning
# ======================================

# INTRODUCTION
# Real data is messy: missing values, duplicates, wrong types, inconsistent
# text. Models learn garbage from garbage, so cleaning is often most of the work.
#
# THEORY
# - Missing values: isna().sum() to count; dropna() to remove; fillna() to
#   fill (mean/median/mode/constant/forward-fill). Decide per column.
# - Duplicates: duplicated(), drop_duplicates(subset=...).
# - Types: astype(), pd.to_numeric(errors="coerce") turns bad values into NaN,
#   pd.to_datetime(...).
# - Text: .str.strip(), .str.lower(), .str.replace(), .str.contains().
# - Categories: map / replace inconsistent labels ("NY", "new york" -> "New York").
# - Outliers: clip(), or filter with quantiles.
# - Always keep the raw data untouched; write cleaning as a repeatable function.
#
# REAL-WORLD ANALOGY
# Washing and chopping vegetables before cooking: unglamorous, but skipping
# it ruins the meal no matter how good the recipe (model) is.
#
# SYNTAX:
#   df["col"] = pd.to_numeric(df["col"], errors="coerce")
#   df["col"] = df["col"].fillna(df["col"].median())
#   df = df.drop_duplicates(subset=["id"])
#
# SMALL WORKING EXAMPLE:
import numpy as np
import pandas as pd

raw = pd.DataFrame({
    "id": [1, 2, 2, 3, 4, 5],
    "city": [" Delhi", "mumbai", "mumbai", "DELHI ", None, "Pune"],
    "age": ["34", "29", "29", "unknown", "41", "250"],
    "signup": ["2025-01-03", "2025-02-11", "2025-02-11", "not a date", "2025-03-30", "2025-04-02"],
})

def clean(df):
    out = df.drop_duplicates(subset="id").copy()
    out["city"] = out["city"].str.strip().str.title().fillna("Unknown")
    out["age"] = pd.to_numeric(out["age"], errors="coerce")
    out.loc[~out["age"].between(0, 120), "age"] = np.nan
    out["age"] = out["age"].fillna(out["age"].median())
    out["signup"] = pd.to_datetime(out["signup"], errors="coerce")
    return out.reset_index(drop=True)

clean_df = clean(raw)
print(raw.isna().sum().to_dict())
print(clean_df)
print(clean_df.dtypes.to_dict())

# EXPLANATION (LINE BY LINE):
# drop_duplicates(subset="id") -> remove the repeated id 2; .copy() avoids warnings.
# .str.strip().str.title()     -> " Delhi"/"DELHI " -> "Delhi", "mumbai" -> "Mumbai".
# fillna("Unknown")            -> explicit category for missing cities.
# pd.to_numeric(errors="coerce") -> "unknown" becomes NaN instead of crashing.
# ~between(0, 120)             -> impossible ages (250) become NaN too.
# fillna(median)               -> fill missing ages with the median (robust).
# pd.to_datetime(errors="coerce") -> bad dates -> NaT (missing datetime).
# reset_index(drop=True)       -> tidy 0..n-1 index after dropping rows.
#
# COMMON MISTAKES:
# 1. Filling with statistics computed on the FULL dataset before a train/test
#    split (data leakage) - compute them on training data only.
# 2. Dropping every row with any NaN and losing most of the data.
# 3. Modifying slices without .copy() (SettingWithCopyWarning).
# 4. Cleaning by hand in a notebook instead of a reusable function.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create a DataFrame with missing values in two columns. Count missing values
# per column, fill one column with its mean and drop rows missing the other.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Given a "price" column with values like "$1,200", "950", "N/A", "1.5k",
# write parse_price(series) that converts all valid values to floats and
# reports how many could not be parsed.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write a data-quality report function quality_report(df) returning a
# DataFrame with, per column: dtype, missing %, unique count, sample values,
# and suspected issues (mixed types, whitespace, outliers by IQR). Run it on a
# messy dataset of at least 8 columns you create.

# YOUR CODE:

