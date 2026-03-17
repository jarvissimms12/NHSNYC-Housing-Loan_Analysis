🏙️ NYC Housing Complaints — Data Analysis & Reporting Pipeline
![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![pandas](https://img.shields.io/badge/pandas-2.0-150458?logo=pandas)
![Data Source](https://img.shields.io/badge/Data-NYC%20Open%20Data-green)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
A real-world data analysis pipeline built to mirror the day-to-day work of a professional Data Analyst at mission-driven organizations like NHSNYC or NYC DOHMH. This project pulls live data from the NYC Open Data API, cleans and validates it, runs statistical analysis, and produces publication-ready visualizations and exportable reports.
---
📊 What This Project Does
Step	Description
Ingest	Pulls 5,000+ records live from the NYC Open Data REST API (311 Heat/Hot Water complaints)
Clean	Standardizes borough names, parses dates, drops nulls, validates data quality
Analyze	Calculates complaint volume by borough, resolution status breakdown, monthly trends, and closure rates
Visualize	Generates a 4-panel chart (bar, pie, line, horizontal bar) saved as PNG
Report	Exports a `borough_summary.csv` with KPIs — ready to share with stakeholders
---
📸 Output
![NYC Housing Analysis](outputs/nyc_housing_analysis.png)
4-panel output: complaint volume by borough, resolution status, monthly trend, and closure rate comparison.
---
🔑 Key Findings
Brooklyn and the Bronx account for the majority of heat/hot water complaints — reflecting higher-density residential housing stock
~65% closure rate overall, with significant variation across boroughs
Winter months show clear complaint spikes, confirming seasonal heating failure patterns
Exportable `borough_summary.csv` provides a clean KPI table ready for stakeholder presentations
---
🛠️ Tools & Skills Demonstrated
Python — pandas, requests, matplotlib, seaborn
REST API consumption — live data pull from NYC Open Data (Socrata API)
Data cleaning — null handling, type coercion, string normalization
Statistical summarization — groupby aggregations, percentage calculations, trend analysis
Data visualization — multi-panel matplotlib/seaborn charts with annotations
Reporting — CSV export, console summary report, structured output folder
---
🚀 How to Run
```bash
# 1. Clone the repo
git clone https://github.com/jarvissimms12/nyc-housing-data-analysis.git
cd nyc-housing-data-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the analysis
python analysis.py
```
Outputs will appear in the `outputs/` folder:
`nyc_housing_analysis.png` — 4-panel visualization
`borough_summary.csv` — exportable summary table
> **Note:** If the NYC Open Data API is unavailable, the script automatically falls back to synthetic demo data with the same structure so the full pipeline still runs.
---
📁 Project Structure
```
nyc-housing-data-analysis/
├── analysis.py           # Main pipeline: fetch → clean → analyze → visualize → report
├── requirements.txt      # Python dependencies
├── outputs/
│   ├── nyc_housing_analysis.png   # 4-panel chart
│   └── borough_summary.csv        # Borough KPI summary
└── README.md
```
---
🔗 Data Source
NYC Open Data — 311 Service Requests  
Filtered to: `complaint_type = HEAT/HOT WATER`, `created_date > 2024-01-01`
---
👤 Author
Jarvis Simms | MS Data Science, NYIT 2025 | Brooklyn, NY  
GitHub • LinkedIn
