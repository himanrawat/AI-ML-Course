# ======================================
# TOPIC: SQL FOR DATA ANALYSIS
# LEVEL: INTERMEDIATE
# ID: data-science.eda.sql
# ======================================

# INTRODUCTION
# Most company data lives in databases. SQL is how you pull and aggregate it
# before it reaches pandas - every data and ML role expects it.
#
# THEORY
# Core query shape (written order):
#   SELECT columns / expressions
#   FROM table [JOIN other ON condition]
#   WHERE row filter
#   GROUP BY columns
#   HAVING group filter
#   ORDER BY columns [DESC]
#   LIMIT n
# - Aggregates: COUNT, SUM, AVG, MIN, MAX.
# - Joins: INNER (only matches), LEFT (keep all left rows).
# - Window functions: ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...),
#   running totals with SUM(...) OVER (...).
# - Python's built-in sqlite3 runs SQL on a local file or in memory;
#   pd.read_sql(query, connection) returns a DataFrame.
# - ALWAYS use parameters (?) for user values - never string formatting
#   (SQL injection).
#
# REAL-WORLD ANALOGY
# A librarian you can ask precise questions: "Bring me the titles of all
# books by authors from India, published after 2010, grouped by genre."
#
# SYNTAX:
#   conn = sqlite3.connect(":memory:")
#   pd.read_sql("SELECT ... WHERE x > ?", conn, params=(10,))
#
# SMALL WORKING EXAMPLE:
import sqlite3

import pandas as pd

conn = sqlite3.connect(":memory:")
pd.DataFrame({
    "customer_id": [1, 2, 3, 4],
    "name": ["Asha", "Ben", "Chen", "Dev"],
    "country": ["IN", "UK", "IN", "US"],
}).to_sql("customers", conn, index=False)
pd.DataFrame({
    "order_id": [101, 102, 103, 104, 105, 106],
    "customer_id": [1, 1, 2, 3, 3, 3],
    "amount": [250.0, 80.0, 120.0, 300.0, 60.0, 45.0],
}).to_sql("orders", conn, index=False)

query = """
SELECT c.country, COUNT(o.order_id) AS orders, ROUND(SUM(o.amount), 2) AS revenue
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
GROUP BY c.country
ORDER BY revenue DESC
"""
print(pd.read_sql(query, conn))
ranked = """
SELECT customer_id, order_id, amount,
       ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY amount DESC) AS rank_in_customer
FROM orders
"""
top = pd.read_sql(ranked, conn)
print(top[top["rank_in_customer"] == 1])
min_amount = 100
print(pd.read_sql("SELECT order_id, amount FROM orders WHERE amount >= ?", conn, params=(min_amount,)))
conn.close()

# EXPLANATION (LINE BY LINE):
# sqlite3.connect(":memory:")   -> a temporary database in RAM.
# DataFrame.to_sql(...)         -> create tables from DataFrames.
# LEFT JOIN                     -> keeps Dev (no orders): orders 0, revenue NULL/None.
# GROUP BY c.country            -> one row per country with COUNT and SUM.
# ORDER BY revenue DESC         -> highest revenue first.
# ROW_NUMBER() OVER (PARTITION BY ...) -> rank orders within each customer.
# params=(min_amount,)          -> safe parameterised query (no string formatting).
#
# COMMON MISTAKES:
# 1. Building SQL with f-strings from user input (SQL injection).
# 2. Filtering aggregates with WHERE instead of HAVING.
# 3. COUNT(*) vs COUNT(column) confusion with NULLs after LEFT JOINs.
# 4. Pulling whole tables into pandas instead of aggregating in SQL.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Using the same tables, write queries for: all orders above 100, the number
# of customers per country, and the average order amount.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write a query returning customers with at least 2 orders and total spend
# over 200 (GROUP BY + HAVING), including their names. Reproduce the same
# result with pandas merge + groupby and assert both match.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Add an order_date column. Write window-function queries for a running total
# of revenue per customer, month-over-month revenue change (LAG), and each
# customer's first purchase date. Then show (with a malicious input string)
# why parameterised queries prevent SQL injection.

# YOUR CODE:

