# ======================================
# TOPIC: PANDAS SERIES AND DATAFRAMES
# LEVEL: BEGINNER
# ID: data-science.pandas.dataframes
# ======================================

# INTRODUCTION
# Most real-world ML starts with a table: customers, transactions, tickets.
# pandas is the standard tool for loading, inspecting and selecting tabular data.
#
# THEORY
# - Series: a 1D labelled array (values + an index).
# - DataFrame: a 2D table; each column is a Series; rows share an index.
# - Create from dicts/lists, or load: pd.read_csv, read_json, read_parquet,
#   read_excel, read_sql.
# - Inspect: head(), tail(), shape, dtypes, info(), describe(), value_counts().
# - Select columns: df["col"] (Series), df[["a", "b"]] (DataFrame).
# - Select rows: df.loc[label_rows, cols] (by LABEL), df.iloc[0:5, 0:2] (by
#   POSITION), boolean filtering df[df["age"] > 30], df.query("age > 30").
# - New columns: df["total"] = df["price"] * df["qty"] (vectorized).
#
# REAL-WORLD ANALOGY
# A spreadsheet with superpowers: every column is typed, every row has a
# label, and you can filter and compute across millions of rows in one line.
#
# SYNTAX:
#   df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
#   df.loc[df["a"] > 1, ["b"]]
#
# SMALL WORKING EXAMPLE:
import pandas as pd

df = pd.DataFrame({
    "name": ["Asha", "Ben", "Chen", "Dev", "Eva"],
    "dept": ["ML", "Web", "ML", "Data", "Web"],
    "salary": [120, 95, 135, 105, 88],
    "years": [5, 3, 8, 4, 2],
})
print(df.head(3))
print(df.shape, df.dtypes.to_dict())
print(df.describe().loc[["mean", "max"]])
print(df["dept"].value_counts().to_dict())
senior_ml = df[(df["dept"] == "ML") & (df["years"] >= 6)]
print(senior_ml[["name", "salary"]])
df["salary_per_year"] = (df["salary"] / df["years"]).round(1)
print(df.loc[df["salary"] > 100, ["name", "salary_per_year"]])
print(df.iloc[0, 0], df.query("dept == 'Web'")["name"].tolist())

# EXPLANATION (LINE BY LINE):
# pd.DataFrame({...})          -> a table built from a dict of columns.
# head(3)                      -> first rows for a quick look.
# dtypes                       -> object/str for text, int64 for numbers.
# describe()                   -> summary statistics; .loc picks two rows of it.
# value_counts()               -> frequency of each department.
# (cond1) & (cond2)            -> combined boolean filter (parentheses required).
# df["salary_per_year"] = ...  -> vectorized new column.
# df.loc[mask, cols]           -> filter rows AND choose columns by label.
# df.iloc[0, 0]                -> first row, first column by position.
# df.query(...)                -> filter with a readable expression string.
#
# COMMON MISTAKES:
# 1. Using and/or instead of &/| in filters.
# 2. Confusing loc (labels) and iloc (positions).
# 3. Chained assignment: df[df.a > 1]["b"] = 0 does not modify df
#    (use df.loc[df.a > 1, "b"] = 0).
# 4. Looping over rows with iterrows for things vectorized code can do.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Build a DataFrame of 6 movies (title, year, rating, genre). Print the shape,
# the movies after 2015, and the average rating per genre.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Load the Iris dataset (sklearn.datasets.load_iris(as_frame=True).frame).
# Show info(), describe(), the class balance, and the rows where petal length
# is above its 90th percentile. Add a ratio column petal_length / petal_width.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Create a 1,000,000-row DataFrame with a numeric column. Compare the speed of
# computing a new column with (1) a for loop over iterrows on the first 10,000
# rows (extrapolate), (2) df.apply, (3) vectorized arithmetic. Also compare
# memory usage of object vs category dtype for a low-cardinality text column.

# YOUR CODE:

