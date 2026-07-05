# Telecom Customer Churn Analysis

Analysis of 7,043 telecom customer records to identify the strongest drivers of churn and surface actionable retention opportunities.

**Stack:** Python (Pandas, NumPy), Matplotlib, Seaborn, SQL

## Overview

Customer churn is one of the costliest problems for subscription telecom businesses — acquiring a new customer typically costs far more than retaining an existing one. This project analyzes a 7,043-customer dataset to find out **who churns, and why**, then translates that into concrete retention recommendations.

## Dataset

- 7,043 customers, 21 features: demographics, account info (contract, tenure, billing), and subscribed services (internet, phone, streaming, tech support, etc.)
- Target variable: `Churn` (Yes/No)
- Overall churn rate: **27.6%**

## Methodology

1. **Data loading & cleaning** — loaded CSV into Pandas; handled type coercion on `TotalCharges`, verified no duplicate customer IDs.
2. **SQL cohort analysis** — loaded the cleaned data into a SQL table and ran group-by aggregations to compute churn rate by contract type, tenure bucket, payment method, and combined risk segments (see `sql/churn_queries.sql`).
3. **Exploratory visualization** — built 11 charts (bar charts, heatmaps, KDE/distribution plots, scatter plots) in Matplotlib/Seaborn to make the patterns legible to non-technical stakeholders.

## Key Findings

| Finding | Detail |
|---|---|
| **Contract type is the single biggest churn driver** | Month-to-month customers churn at **39.7%**, vs. **11.0%** for two-year contract holders — a **3.6x** gap. |
| **Churn is front-loaded in the first year** | Customers with 0–12 months tenure churn at 37.9%, dropping to 16.9% for customers past 48 months. Retention risk is highest in the first year and falls off sharply after. |
| **Fiber-optic + no tech support is a red-flag combo** | Month-to-month customers on fiber internet with no tech support churn at **49.8%** — nearly 1 in 2. |
| **Payment method correlates with churn** | Electronic check users churn at 31.8%, notably higher than automatic bank transfer (23.5%) — likely a proxy for lower engagement/commitment. |

## Visualizations

All charts are in `/visuals`:
1. Overall churn distribution (pie)
2. Churn rate by contract type
3. Tenure distribution by churn status
4. Monthly charges distribution by churn status (KDE)
5. Heatmap — churn rate by contract × internet service
6. Churn rate by tenure bucket
7. Churn rate by payment method
8. Tech support / online security impact
9. Monthly charges vs. tenure scatter
10. High-risk segment vs. rest of base
11. Contract mix (customer base composition)

## Business Recommendations

1. **Target month-to-month customers with 6-month contract incentives.** A modest discount or perk for converting to a 6- or 12-month term could meaningfully reduce churn exposure, given the 3.6x gap between month-to-month and annual contracts.
2. **Prioritize retention outreach in months 0–12.** Since churn risk is highest in year one, an onboarding/check-in program in the first 90–180 days would catch at-risk customers earliest.
3. **Bundle free tech support trials for fiber customers.** The fiber + no-support segment churns at nearly 50% — offering a free trial of tech support could reduce friction-driven churn.
4. **Nudge electronic-check users toward autopay.** A small incentive to switch payment methods may correlate with (though not necessarily cause) improved retention; worth an A/B test.

## Project Structure

```
telecom-churn-analysis/
├── data/
│   ├── generate_dataset.py    # dataset generation (see note below)
│   └── telco_churn.csv
├── notebooks/
│   └── analysis.py            # full EDA + visualization pipeline
├── sql/
│   ├── churn_queries.sql      # cohort segmentation queries
│   └── load_and_query.py      # loads CSV into SQL table, runs queries
├── visuals/                   # 11 exported PNG charts
└── README.md
```

## Note on the dataset

This is a rebuild of an earlier version of this project. The dataset here is a synthetically generated replica calibrated to match the well-documented aggregate statistics of the public IBM Telco Customer Churn dataset (7,043 rows, ~27% overall churn, ~3–4x churn gap between month-to-month and long-term contracts). The analysis pipeline, SQL queries, and visualizations are all original work and reproducible against any CSV with the same schema — including the original Kaggle source file, if substituted in.
