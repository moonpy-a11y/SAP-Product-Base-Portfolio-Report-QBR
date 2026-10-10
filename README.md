<div align="center">

# SAP Product Base Portfolio Report (QBR) Engine

[![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=googlesheets&logoColor=white)](https://workspace.google.com/products/sheets/)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/moonpy-a11y/SAP-Product-Base-Portfolio-Report-QBR-)
[![SAP Compatibility](https://img.shields.io/badge/SAP-S%2F4HANA%20%7C%20PPM-0FAFA4?style=for-the-badge&logo=sap&logoColor=white)](https://www.sap.com)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

An enterprise portfolio governance engine connecting SAP S/4HANA logistics master data (`MARA`/`MVKE`) and SAP Enterprise Portfolio and Project Management (`PPM`) bucket hierarchies with executive decision dashboards in Google Sheets.

---

</div>

## Table of Contents

- [Key Features](#key-features)
- [Data Pipeline & Synchronisation](#data-pipeline--synchronisation)
- [Mathematical & Strategic Models](#mathematical--strategic-models)
- [Repository Directory Structure](#repository-directory-structure)
- [Quick Start Guide](#quick-start-guide)
- [Contact Information](#contact-information)

---

## Key Features

- **Dynamic SAP Sync Detection**: Automatically checks for live SAP S/4HANA host environment variables at runtime (`SAP_S4HANA_HOST`). If disconnected, it falls back seamlessly to embedded baseline CSV datasets.
- **SAP Hierarchy Harmonization**: Parses standard 18-character SAP `PRODHS` material strings into period-delimited `[L1].[L2].[L3]` keys matching database schemas (`MVKE-PRODH`, `MARA-PRDHA`, and `/RPM/BUCKET`).
- **OEM LTA Productivity Glide Paths**: Automated multi-year price erosion modeling for $4 \times 4$, $3 \times 4$, and $3 \times 2$ contract give-back models.
- **Tier-Weighted Incentive Allocation**: Dynamically distributes sales bonus pools and marketing capital based on contribution margin percentages and lifecycle strategic tiers.
- **Google Apps Script & Gemini AI Integration**: Integrates Google Sheets with Gemini 1.5 Flash to automatically classify unstructured Engineering Change Notices (PCN/PDN) and evaluate contract risk.

---

## Data Pipeline & Synchronisation

| Entity Architecture | Primary Key | Composite Key Syntax | SAP S/4HANA Field | SAP PPM Mapping | Validation Rule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Dim_Hierarchy** | Node_ID | `[L1].[L2].[L3]` | `MVKE-PRODH` / `PRODHS` | Bucket External ID | Alphanumeric segment check |
| **Dim_ProductMaster** | Material_ID | `[Node_ID]-[MATNR]` | `MARA-MATNR` / `MARA-PRDHA` | Item External ID | Standard 18-character padding |
| **Fact_Financials** | Record_ID | `[Material_ID]-[Period]` | `CO-PA` / `ACDOCA` | Rollup (`RPM_FIDATA`) | Valid closed accounting period |
| **Fact_Governance** | Decision_ID | `[Material_ID]-[Cycle]` | Status (`MARA-MSTAE`) | DFM Decision Point | Active, Ramp-down, EOL, LTA |

---

## Mathematical & Strategic Models

### 1. Strategic Sales Bonus Allocation Formula

Calculates individual sales bonus payouts based on quota achievement, gross contribution margin percentage, and strategic portfolio lifecycle multipliers:

$$B_i = B_{\text{total}} \times \frac{S_i \cdot M_i \cdot W_{t_i}}{\sum_{j=1}^{N} \left(S_j \cdot M_j \cdot W_{t_j}\right)}$$

**Where:**
- **$B_{\text{total}}$**: Total aggregate sales bonus pool allocated to the portfolio bucket.
- **$S_i$**: Closed sales revenue achievement relative to target quota ($S_i = \text{Actual} / \text{Target}$).
- **$M_i$**: CO-PA gross contribution margin percentage ($ACDOCA$).
- **$W_{t_i}$**: Strategic Tier Weight Multiplier (Tier 1 Growth = `1.5`, Tier 2 Core = `1.0`, Tier 3 Harvest = `0.5`, Tier 4 Phase-Out = `0.0`).

---

### 2. OEM LTA Productivity Give-Back Models

| LTA Model | Annual Reduction Rate | Contract Horizon | Compounded Price Index (Year 4) | Cumulative Price Concession |
| :--- | :---: | :---: | :---: | :---: |
| **4x4 Model** | 4.0% per year | 4 Years | 84.93% of Base | 15.07% total reduction |
| **3x4 Model** | 3.0% per year | 4 Years | 88.53% of Base | 11.47% total reduction |
| **3x2 Model** | 3.0% per year | 2 Years | 94.09% of Base | 5.91% total reduction |

---

## Repository Directory Structure

```text
SAP-Product-Base-Portfolio-Report-QBR-/
├── .gitignore
├── sap_portfolio_config.json
├── README.md
├── Schemas/
│   └── conf.schema.json
├── Scripts/
│   └── build_report.py
└── resources/
    ├── SAP_Product_Base_Portfolio_Rep_Control_Panel.csv
    ├── SAP_Product_Base_Portfolio_Rep_Dim_Hierarchy.csv
    ├── SAP_Product_Base_Portfolio_Rep_Engine_Portfolio_Calc.csv
    ├── SAP_Product_Base_Portfolio_Rep_QBR_Y1_Y2_Report.csv
    └── SAP_Product_Base_Portfolio_Rep_QRB_Dashboard.csv
    
