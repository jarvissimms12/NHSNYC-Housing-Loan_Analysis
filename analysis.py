"""
NYC Housing & Workforce Data Analysis
======================================
Pulls live data from NYC Open Data API, cleans it, and produces
a full analytical report with charts — mirroring real-world data
analyst work for orgs like NHSNYC and NYC DOHMH.

Author: Jarvis Simms
Tools:  Python, pandas, matplotlib, seaborn, requests
Data:   NYC Open Data (data.cityofnewyork.us)
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

# ── Output folder ──────────────────────────────────────────────
os.makedirs("outputs", exist_ok=True)
sns.set_theme(style="whitegrid", palette="Blues_d")
plt.rcParams.update({"font.family": "DejaVu Sans", "figure.dpi": 120})

print("=" * 60)
print("  NYC Housing & Workforce Data Analysis")
print("  Author: Jarvis Simms | github.com/jarvissimms12")
print("=" * 60)


# ══════════════════════════════════════════════════════════════
# 1. FETCH DATA — NYC 311 Housing Complaints (sample)
# ══════════════════════════════════════════════════════════════
print("\n[1/5] Fetching NYC 311 Housing Complaint data...")

URL = (
    "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
    "?complaint_type=HEAT/HOT WATER"
    "&$limit=5000"
    "&$select=created_date,borough,status,resolution_description,incident_zip"
    "&$where=created_date > '2024-01-01T00:00:00'"
)

try:
    resp = requests.get(URL, timeout=20)
    resp.raise_for_status()
    df = pd.DataFrame(resp.json())
    print(f"    ✓ Loaded {len(df):,} rows from NYC Open Data API")
except Exception as e:
    print(f"    ✗ API unavailable ({e}). Generating synthetic data for demo...")
    import numpy as np
    np.random.seed(42)
    boroughs = ["BROOKLYN", "BRONX", "MANHATTAN", "QUEENS", "STATEN ISLAND"]
    statuses = ["Closed", "Open", "Pending", "Assigned"]
    n = 2000
    df = pd.DataFrame({
        "created_date": pd.date_range("2024-01-01", periods=n, freq="3h").astype(str),
        "borough": np.random.choice(boroughs, n, p=[0.28, 0.25, 0.20, 0.22, 0.05]),
        "status": np.random.choice(statuses, n, p=[0.65, 0.15, 0.12, 0.08]),
        "incident_zip": np.random.choice(
            ["11236", "10456", "10001", "11373", "10301"], n
        ),
    })


# ══════════════════════════════════════════════════════════════
# 2. CLEAN & VALIDATE
# ══════════════════════════════════════════════════════════════
print("\n[2/5] Cleaning and validating data...")

df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
df["borough"] = df["borough"].str.strip().str.upper()
df["status"] = df["status"].str.strip().str.title()
df = df.dropna(subset=["created_date", "borough"])
df["month"] = df["created_date"].dt.to_period("M")
df["year"] = df["created_date"].dt.year

# Data quality report
total = len(df)
missing = df.isnull().sum()
print(f"    ✓ Records after cleaning : {total:,}")
print(f"    ✓ Date range             : {df['created_date'].min().date()} → {df['created_date'].max().date()}")
print(f"    ✓ Boroughs found         : {sorted(df['borough'].unique())}")
print(f"    ✓ Null values per column :\n{missing[missing > 0].to_string() if missing.sum() > 0 else '       None — data is clean!'}")


# ══════════════════════════════════════════════════════════════
# 3. ANALYSIS & METRICS
# ══════════════════════════════════════════════════════════════
print("\n[3/5] Running analysis...")

# Complaints by borough
borough_counts = df["borough"].value_counts()

# Resolution status breakdown
status_counts = df["status"].value_counts()

# Monthly complaint trend
monthly = df.groupby("month").size().reset_index(name="complaints")
monthly["month_str"] = monthly["month"].astype(str)

# Closure rate by borough
if "status" in df.columns:
    closure = df.groupby("borough").apply(
        lambda x: (x["status"] == "Closed").sum() / len(x) * 100
    ).reset_index(name="closure_rate_pct").sort_values("closure_rate_pct", ascending=False)

print("    ✓ Analysis complete")
print(f"\n    TOP BOROUGHS BY COMPLAINT VOLUME:")
for b, c in borough_counts.items():
    pct = c / total * 100
    print(f"       {b:<20} {c:>5,}  ({pct:.1f}%)")

print(f"\n    RESOLUTION STATUS BREAKDOWN:")
for s, c in status_counts.items():
    print(f"       {s:<20} {c:>5,}")


# ══════════════════════════════════════════════════════════════
# 4. VISUALIZATIONS
# ══════════════════════════════════════════════════════════════
print("\n[4/5] Generating charts...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(
    "NYC Housing Complaints — Heat/Hot Water | 2024–2025\nJarvis Simms | Data Analysis Portfolio",
    fontsize=14, fontweight="bold", y=1.01
)

# Chart 1: Complaints by Borough
ax1 = axes[0, 0]
colors = sns.color_palette("Blues_d", len(borough_counts))
bars = ax1.bar(borough_counts.index, borough_counts.values, color=colors, edgecolor="white")
ax1.set_title("Complaints by Borough", fontweight="bold")
ax1.set_xlabel("Borough")
ax1.set_ylabel("Number of Complaints")
ax1.tick_params(axis="x", rotation=20)
for bar, val in zip(bars, borough_counts.values):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
             f"{val:,}", ha="center", va="bottom", fontsize=9, fontweight="bold")

# Chart 2: Status Pie
ax2 = axes[0, 1]
wedge_colors = ["#2196F3", "#FF9800", "#4CAF50", "#9C27B0"][:len(status_counts)]
ax2.pie(
    status_counts.values,
    labels=status_counts.index,
    autopct="%1.1f%%",
    colors=wedge_colors,
    startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5}
)
ax2.set_title("Complaint Resolution Status", fontweight="bold")

# Chart 3: Monthly Trend
ax3 = axes[1, 0]
x_positions = range(len(monthly))
ax3.plot(x_positions, monthly["complaints"], marker="o", color="#1565C0",
         linewidth=2.5, markersize=6, markerfacecolor="white", markeredgewidth=2)
ax3.fill_between(x_positions, monthly["complaints"], alpha=0.15, color="#1565C0")
ax3.set_title("Monthly Complaint Volume Trend", fontweight="bold")
ax3.set_xlabel("Month")
ax3.set_ylabel("Complaints")
step = max(1, len(monthly) // 8)
ax3.set_xticks(list(x_positions)[::step])
ax3.set_xticklabels(monthly["month_str"].iloc[::step], rotation=30, ha="right", fontsize=8)
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

# Chart 4: Closure Rate by Borough
ax4 = axes[1, 1]
if "closure" in dir():
    palette = sns.color_palette("RdYlGn", len(closure))
    bars4 = ax4.barh(closure["borough"], closure["closure_rate_pct"],
                     color=palette, edgecolor="white")
    ax4.set_title("Case Closure Rate by Borough (%)", fontweight="bold")
    ax4.set_xlabel("Closure Rate (%)")
    ax4.set_xlim(0, 110)
    for bar, val in zip(bars4, closure["closure_rate_pct"]):
        ax4.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                 f"{val:.1f}%", va="center", fontsize=10, fontweight="bold")

plt.tight_layout()
plt.savefig("outputs/nyc_housing_analysis.png", bbox_inches="tight", dpi=150)
plt.close()
print("    ✓ Saved: outputs/nyc_housing_analysis.png")


# ══════════════════════════════════════════════════════════════
# 5. SUMMARY REPORT (CSV + text)
# ══════════════════════════════════════════════════════════════
print("\n[5/5] Exporting summary report...")

# Borough summary table
summary = df.groupby("borough").agg(
    total_complaints=("borough", "count"),
    closed=("status", lambda x: (x == "Closed").sum()),
).reset_index()
summary["closure_rate_pct"] = (summary["closed"] / summary["total_complaints"] * 100).round(1)
summary["pct_of_total"] = (summary["total_complaints"] / total * 100).round(1)
summary = summary.sort_values("total_complaints", ascending=False)
summary.to_csv("outputs/borough_summary.csv", index=False)

# Print report to console
print("\n" + "=" * 60)
print("  FINAL SUMMARY REPORT")
print("=" * 60)
print(f"  Total Complaints Analyzed : {total:,}")
print(f"  Date Range                : {df['created_date'].min().date()} to {df['created_date'].max().date()}")
print(f"  Overall Closure Rate      : {(df['status'] == 'Closed').mean() * 100:.1f}%")
print("\n  Borough Breakdown:")
print(summary.to_string(index=False))
print("\n  Outputs saved to /outputs:")
print("    • nyc_housing_analysis.png  — 4-panel visualization")
print("    • borough_summary.csv       — exportable summary table")
print("\n" + "=" * 60)
print("  Analysis complete. See outputs/ folder for results.")
print("=" * 60)
