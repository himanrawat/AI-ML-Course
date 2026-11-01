# ======================================
# TOPIC: GROUPBY, MERGE AND RESHAPE
# LEVEL: INTERMEDIATE
# ID: data-science.pandas.groupby-merge
# ======================================

# INTRODUCTION
# Business questions are aggregations: revenue per region, churn per plan,
# accuracy per model. Data also arrives in several tables you must join.
#
# THEORY
# - GROUPBY: split rows into groups, apply a function, combine results.
#   df.groupby("col")["value"].mean(); .agg(total=("value", "sum"), n=("id", "count"))
# - transform returns a result aligned with the original rows
#   (e.g. each row's group mean) - great for features.
# - MERGE (SQL-style joins): pd.merge(left, right, on="key", how="inner" |
#   "left" | "right" | "outer"). validate="many_to_one" catches surprises.
# - CONCAT stacks DataFrames vertically or horizontally.
# - RESHAPE: pivot_table (long -> wide with aggregation), melt (wide -> long).
#
# REAL-WORLD ANALOGY
# Sorting receipts into piles by shop (group), adding up each pile (aggregate),
# then matching each shop to its address book entry (merge).
#
# SYNTAX:
#   df.groupby("a").agg(total=("b", "sum"))
#   pd.merge(orders, customers, on="customer_id", how="left")
#   df.pivot_table(index="a", columns="b", values="c", aggfunc="sum")
#
# SMALL WORKING EXAMPLE:
import pandas as pd

orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5, 6],
    "customer_id": [10, 11, 10, 12, 11, 13],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Mar"],
    "amount": [250, 120, 80, 300, 60, 45],
})
customers = pd.DataFrame({
    "customer_id": [10, 11, 12],
    "plan": ["pro", "free", "pro"],
})
summary = orders.groupby("customer_id").agg(total=("amount", "sum"), orders=("order_id", "count"))
print(summary)
orders["share_of_customer"] = (orders["amount"] / orders.groupby("customer_id")["amount"].transform("sum")).round(2)
merged = pd.merge(orders, customers, on="customer_id", how="left", validate="many_to_one")
print(merged[["order_id", "customer_id", "plan"]])
print(merged.groupby("plan", dropna=False)["amount"].mean())
pivot = merged.pivot_table(index="plan", columns="month", values="amount", aggfunc="sum", fill_value=0)
print(pivot)
long = pivot.reset_index().melt(id_vars="plan", var_name="month", value_name="amount")
print(long.head(3))

# EXPLANATION (LINE BY LINE):
# groupby("customer_id").agg(...)    -> named aggregations: total amount and order count.
# transform("sum")                   -> each row gets its customer's total -> share column.
# merge(..., how="left")             -> keep every order, add plan when known.
# validate="many_to_one"             -> raises if customers had duplicate ids.
# customer 13 has no plan -> NaN; dropna=False keeps that group visible.
# pivot_table(...)                   -> plans as rows, months as columns, summed amounts.
# melt(...)                          -> back to long format (one row per plan-month).
#
# COMMON MISTAKES:
# 1. Inner joins silently dropping rows without matches.
# 2. Duplicate keys multiplying rows after a merge (use validate=).
# 3. Using apply with Python functions where built-in aggregations exist.
# 4. Forgetting groupby drops NaN keys by default.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Using the orders table, compute total and average amount per month, and the
# month with the highest revenue.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Create products and sales tables. Merge them, compute revenue per category,
# find products that never sold (anti-join with indicator=True), and the top
# product per category.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Simulate 6 months of user events (user_id, date, event, plan). Build a
# monthly cohort retention table: for users grouped by signup month, the % who
# were active in each following month. Display it as a pivot table.

# YOUR CODE:

