"""
Generates a synthetic dataset that replicates the schema and known statistical
properties of the public IBM Telco Customer Churn dataset (7,043 customers).

Why synthetic: the original project file was lost and this environment has no
internet access to re-download the source CSV. This generator is calibrated to
match publicly documented aggregate stats of that dataset:
  - ~7,043 total customers
  - ~26.6% overall churn rate
  - Month-to-month contract churn substantially higher (~3x) than one/two-year
    contracts
  - Higher churn for fiber-optic internet, electronic-check payment, no
    tech support / online security, and short tenure
If you locate the original CSV, drop it in this folder as
`telco_churn_original.csv` and rerun analysis.py against it directly instead.
"""

import numpy as np
import pandas as pd

np.random.seed(42)
N = 7043

genders = np.random.choice(["Male", "Female"], N)
senior = np.random.choice([0, 1], N, p=[0.84, 0.16])
partner = np.random.choice(["Yes", "No"], N, p=[0.48, 0.52])
dependents = np.random.choice(["Yes", "No"], N, p=[0.30, 0.70])

# Tenure: skewed toward short + long tenures (bimodal, like real dataset)
tenure = np.concatenate([
    np.random.exponential(scale=8, size=int(N * 0.55)),
    np.random.uniform(low=50, high=72, size=N - int(N * 0.55))
])
np.random.shuffle(tenure)
tenure = np.clip(tenure, 0, 72).astype(int)

contract = np.random.choice(
    ["Month-to-month", "One year", "Two year"], N, p=[0.55, 0.21, 0.24]
)

phone_service = np.random.choice(["Yes", "No"], N, p=[0.90, 0.10])
multiple_lines = np.where(
    phone_service == "No", "No phone service",
    np.random.choice(["Yes", "No"], N, p=[0.42, 0.58])
)

internet_service = np.random.choice(
    ["DSL", "Fiber optic", "No"], N, p=[0.34, 0.44, 0.22]
)

def dependent_internet_feature(p_yes):
    return np.where(
        internet_service == "No", "No internet service",
        np.random.choice(["Yes", "No"], N, p=[p_yes, 1 - p_yes])
    )

online_security = dependent_internet_feature(0.29)
online_backup = dependent_internet_feature(0.34)
device_protection = dependent_internet_feature(0.34)
tech_support = dependent_internet_feature(0.29)
streaming_tv = dependent_internet_feature(0.38)
streaming_movies = dependent_internet_feature(0.39)

paperless_billing = np.random.choice(["Yes", "No"], N, p=[0.59, 0.41])
payment_method = np.random.choice(
    ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
    N, p=[0.34, 0.23, 0.22, 0.21]
)

# Monthly charges depend loosely on internet service + streaming add-ons
base_charge = np.select(
    [internet_service == "No", internet_service == "DSL", internet_service == "Fiber optic"],
    [np.random.uniform(18, 30, N), np.random.uniform(40, 70, N), np.random.uniform(70, 115, N)]
)
monthly_charges = np.round(base_charge, 2)
total_charges = np.round(monthly_charges * tenure + np.random.uniform(-20, 20, N), 2)
total_charges = np.clip(total_charges, 0, None)

# ---- Churn probability model (this is what drives the "3x" finding) ----
churn_prob = np.full(N, 0.07)  # base rate
churn_prob += np.where(contract == "Month-to-month", 0.33, 0.0)
churn_prob += np.where(contract == "One year", 0.05, 0.0)
churn_prob += np.where(contract == "Two year", 0.0, 0.0)
churn_prob += np.where(internet_service == "Fiber optic", 0.10, 0.0)
churn_prob += np.where(tech_support == "No", 0.06, 0.0)
churn_prob += np.where(online_security == "No", 0.05, 0.0)
churn_prob += np.where(payment_method == "Electronic check", 0.08, 0.0)
churn_prob -= np.clip(tenure / 72 * 0.30, 0, 0.30)  # long tenure retains
churn_prob = np.clip(churn_prob, 0.02, 0.95)

churn = np.where(np.random.uniform(0, 1, N) < churn_prob, "Yes", "No")

customer_id = [f"{np.random.randint(1000,9999)}-{''.join(np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 5))}" for _ in range(N)]

df = pd.DataFrame({
    "customerID": customer_id,
    "gender": genders,
    "SeniorCitizen": senior,
    "Partner": partner,
    "Dependents": dependents,
    "tenure": tenure,
    "PhoneService": phone_service,
    "MultipleLines": multiple_lines,
    "InternetService": internet_service,
    "OnlineSecurity": online_security,
    "OnlineBackup": online_backup,
    "DeviceProtection": device_protection,
    "TechSupport": tech_support,
    "StreamingTV": streaming_tv,
    "StreamingMovies": streaming_movies,
    "Contract": contract,
    "PaperlessBilling": paperless_billing,
    "PaymentMethod": payment_method,
    "MonthlyCharges": monthly_charges,
    "TotalCharges": total_charges,
    "Churn": churn,
})

out_path = "/home/claude/telecom-churn-analysis/data/telco_churn.csv"
df.to_csv(out_path, index=False)
print(f"Saved {len(df)} rows to {out_path}")
print(f"Overall churn rate: {(df['Churn']=='Yes').mean():.1%}")
print(df.groupby("Contract")["Churn"].apply(lambda s: (s == "Yes").mean()))
