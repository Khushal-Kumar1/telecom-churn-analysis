"""
Loads telco_churn.csv into a SQL database and runs the cohort-segmentation
queries from churn_queries.sql.

Note: uses sqlite3 (stdlib, no server needed) as the execution engine so this
runs anywhere with no setup. The queries in churn_queries.sql are written in
plain ANSI SQL that is directly portable to MySQL — swap the connection for
mysql.connector / PyMySQL against a real MySQL instance and these queries
run unchanged.
"""

import sqlite3
import pandas as pd

df = pd.read_csv("/home/claude/telecom-churn-analysis/data/telco_churn.csv")

conn = sqlite3.connect(":memory:")
df.to_sql("customers", conn, index=False, if_exists="replace")

queries = {
    "Overall churn rate": """
        SELECT ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
        FROM customers;
    """,
    "Churn rate by contract type": """
        SELECT Contract, COUNT(*) AS total_customers,
               SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
               ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
        FROM customers
        GROUP BY Contract
        ORDER BY churn_rate_pct DESC;
    """,
    "Churn rate by tenure bucket": """
        SELECT
            CASE
                WHEN tenure <= 12 THEN '0-12 months'
                WHEN tenure <= 24 THEN '13-24 months'
                WHEN tenure <= 48 THEN '25-48 months'
                ELSE '49-72 months'
            END AS tenure_bucket,
            COUNT(*) AS total_customers,
            ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
        FROM customers
        GROUP BY tenure_bucket
        ORDER BY MIN(tenure);
    """,
    "High-risk segment (month-to-month + fiber + no tech support)": """
        SELECT COUNT(*) AS at_risk_customers,
               ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
        FROM customers
        WHERE Contract = 'Month-to-month' AND InternetService = 'Fiber optic' AND TechSupport = 'No';
    """,
    "Churn rate by payment method": """
        SELECT PaymentMethod, COUNT(*) AS total_customers,
               ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
        FROM customers
        GROUP BY PaymentMethod
        ORDER BY churn_rate_pct DESC;
    """,
}

for title, q in queries.items():
    print(f"\n=== {title} ===")
    result = pd.read_sql_query(q, conn)
    print(result.to_string(index=False))

conn.close()
