"""
Telecom Customer Churn Analysis
Dataset: 7,043 telecom customers (telco_churn.csv)
Goal: identify churn drivers by contract type, tenure, and monthly charges;
produce visuals communicating findings to non-technical stakeholders.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="deep")
VIS_DIR = "/home/claude/telecom-churn-analysis/visuals"

df = pd.read_csv("/home/claude/telecom-churn-analysis/data/telco_churn.csv")
df["ChurnFlag"] = (df["Churn"] == "Yes").astype(int)

print("Shape:", df.shape)
print("Overall churn rate: {:.1%}".format(df["ChurnFlag"].mean()))

# ---------- 1. Overall churn distribution ----------
plt.figure(figsize=(5, 5))
df["Churn"].value_counts().plot.pie(autopct="%1.1f%%", colors=["#4C72B0", "#DD8452"], ylabel="")
plt.title("Overall Customer Churn Distribution")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/01_overall_churn_pie.png", dpi=150)
plt.close()

# ---------- 2. Churn rate by contract type (headline finding) ----------
contract_churn = df.groupby("Contract")["ChurnFlag"].mean().sort_values(ascending=False) * 100
plt.figure(figsize=(7, 5))
ax = sns.barplot(x=contract_churn.index, y=contract_churn.values)
for i, v in enumerate(contract_churn.values):
    ax.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontweight="bold")
plt.title("Churn Rate by Contract Type")
plt.ylabel("Churn Rate (%)")
plt.xlabel("Contract Type")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/02_churn_by_contract.png", dpi=150)
plt.close()

# ---------- 3. Tenure distribution split by churn ----------
plt.figure(figsize=(8, 5))
sns.histplot(data=df, x="tenure", hue="Churn", multiple="stack", bins=30)
plt.title("Customer Tenure Distribution by Churn Status")
plt.xlabel("Tenure (months)")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/03_tenure_distribution.png", dpi=150)
plt.close()

# ---------- 4. Monthly charges distribution split by churn ----------
plt.figure(figsize=(8, 5))
sns.kdeplot(data=df, x="MonthlyCharges", hue="Churn", fill=True, common_norm=False, alpha=0.4)
plt.title("Monthly Charges Distribution by Churn Status")
plt.xlabel("Monthly Charges ($)")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/04_monthly_charges_kde.png", dpi=150)
plt.close()

# ---------- 5. Heatmap: churn rate by contract x internet service ----------
pivot = df.pivot_table(index="Contract", columns="InternetService", values="ChurnFlag", aggfunc="mean") * 100
plt.figure(figsize=(7, 5))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="Reds", cbar_kws={"label": "Churn Rate (%)"})
plt.title("Churn Rate (%): Contract Type vs Internet Service")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/05_heatmap_contract_internet.png", dpi=150)
plt.close()

# ---------- 6. Tenure buckets churn rate ----------
df["TenureBucket"] = pd.cut(df["tenure"], bins=[-1, 12, 24, 48, 72],
                             labels=["0-12 mo", "13-24 mo", "25-48 mo", "49-72 mo"])
tenure_churn = df.groupby("TenureBucket")["ChurnFlag"].mean() * 100
plt.figure(figsize=(7, 5))
ax = sns.barplot(x=tenure_churn.index, y=tenure_churn.values, color="#55A868")
for i, v in enumerate(tenure_churn.values):
    ax.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontweight="bold")
plt.title("Churn Rate by Tenure Bucket")
plt.ylabel("Churn Rate (%)")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/06_churn_by_tenure_bucket.png", dpi=150)
plt.close()

# ---------- 7. Churn rate by payment method ----------
pay_churn = df.groupby("PaymentMethod")["ChurnFlag"].mean().sort_values(ascending=False) * 100
plt.figure(figsize=(8, 5))
ax = sns.barplot(x=pay_churn.values, y=pay_churn.index, color="#C44E52")
for i, v in enumerate(pay_churn.values):
    ax.text(v + 0.5, i, f"{v:.1f}%", va="center", fontweight="bold")
plt.title("Churn Rate by Payment Method")
plt.xlabel("Churn Rate (%)")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/07_churn_by_payment_method.png", dpi=150)
plt.close()

# ---------- 8. Tech support / online security impact ----------
fig, axes = plt.subplots(1, 2, figsize=(11, 5))
for ax, col in zip(axes, ["TechSupport", "OnlineSecurity"]):
    sub = df[df[col] != "No internet service"]
    rates = sub.groupby(col)["ChurnFlag"].mean() * 100
    sns.barplot(x=rates.index, y=rates.values, ax=ax, color="#8172B2")
    ax.set_title(f"Churn Rate by {col}")
    ax.set_ylabel("Churn Rate (%)")
    for i, v in enumerate(rates.values):
        ax.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/08_support_security_impact.png", dpi=150)
plt.close()

# ---------- 9. Monthly charges vs tenure scatter, colored by churn ----------
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df.sample(1500, random_state=1), x="tenure", y="MonthlyCharges",
                 hue="Churn", alpha=0.6, s=25)
plt.title("Monthly Charges vs Tenure (sample of 1,500 customers)")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/09_charges_vs_tenure_scatter.png", dpi=150)
plt.close()

# ---------- 10. High-risk segment breakdown ----------
df["HighRisk"] = (
    (df["Contract"] == "Month-to-month") &
    (df["InternetService"] == "Fiber optic") &
    (df["TechSupport"] == "No")
)
risk_churn = df.groupby("HighRisk")["ChurnFlag"].mean() * 100
plt.figure(figsize=(6, 5))
ax = sns.barplot(x=["All Other Customers", "High-Risk Segment\n(M2M + Fiber + No Support)"],
                  y=[risk_churn[False], risk_churn[True]], palette=["#4C72B0", "#C44E52"])
for i, v in enumerate([risk_churn[False], risk_churn[True]]):
    ax.text(i, v + 1, f"{v:.1f}%", ha="center", fontweight="bold")
plt.title("Churn Rate: High-Risk Segment vs Rest of Base")
plt.ylabel("Churn Rate (%)")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/10_high_risk_segment.png", dpi=150)
plt.close()

# ---------- 11. Contract mix (bonus) ----------
plt.figure(figsize=(6, 5))
df["Contract"].value_counts().plot.bar(color="#64B5CD")
plt.title("Customer Base by Contract Type")
plt.ylabel("Number of Customers")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/11_contract_mix.png", dpi=150)
plt.close()

print("\nSaved 11 visualizations to", VIS_DIR)

# ---------- Summary stats for README ----------
print("\n--- Key stats for README ---")
print("Overall churn:", round(df['ChurnFlag'].mean()*100, 1), "%")
print(contract_churn)
print("Ratio M2M / Two year:", round(contract_churn['Month-to-month'] / contract_churn['Two year'], 1))
