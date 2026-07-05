-- Telecom Customer Churn Analysis — SQL layer
-- Written in standard ANSI/MySQL-compatible syntax.
-- Table `customers` loaded from telco_churn.csv (see load_to_db.py)

-- 1. Overall churn rate
SELECT
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers;

-- 2. Churn rate by contract type (the headline "3x" finding)
SELECT
    Contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC;

-- 3. Churn rate by tenure bucket
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

-- 4. Churn rate by monthly charge quartile
SELECT
    CASE
        WHEN MonthlyCharges < 35 THEN 'Low ($0-35)'
        WHEN MonthlyCharges < 70 THEN 'Mid ($35-70)'
        WHEN MonthlyCharges < 95 THEN 'High ($70-95)'
        ELSE 'Premium ($95+)'
    END AS charge_band,
    COUNT(*) AS total_customers,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charge,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY charge_band
ORDER BY avg_monthly_charge;

-- 5. High-risk segment: month-to-month + fiber optic + no tech support
SELECT
    COUNT(*) AS at_risk_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
WHERE Contract = 'Month-to-month'
  AND InternetService = 'Fiber optic'
  AND TechSupport = 'No';

-- 6. Payment method churn breakdown
SELECT
    PaymentMethod,
    COUNT(*) AS total_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY PaymentMethod
ORDER BY churn_rate_pct DESC;
