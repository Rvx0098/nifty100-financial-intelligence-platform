# Sprint 2 Summary — Financial Ratio Engine

## Sprint Overview

Sprint 2 focused on transforming the validated financial data warehouse into an analytics engine capable of computing key financial ratios and growth metrics for all companies in the N100 dataset. The sprint introduced a modular analytics architecture, reusable financial formula libraries, CAGR computation, leverage analysis, cash flow KPIs, and automated reporting.

---

# Sprint Goal

Build a production-ready Financial Ratio Engine capable of computing 50+ financial KPIs, handling financial edge cases, validating outputs, and preparing analytics data for dashboards and screening modules.

---

# Completed Deliverables

## Analytics Modules

Created modular analytics components inside:

```text
src/
└── analytics/
    ├── ratios.py
    ├── leverage.py
    ├── ratio_engine.py
    ├── cagr.py
    ├── cagr_engine.py
    ├── cashflow_kpis.py
    ├── populate_financial_ratios.py
```

Each module follows a single responsibility principle, making the codebase easier to maintain and extend.

---

# Profitability KPIs

Successfully implemented:

* Net Profit Margin
* Operating Profit Margin
* Return on Equity (ROE)
* Return on Assets (ROA)
* Return on Capital Employed (ROCE)

The engine merged **1,276 Profit & Loss records** with **1,312 Balance Sheet records**, producing **1,175 valid company-year observations** for KPI computation.

---

# Leverage & Efficiency KPIs

Implemented:

* Debt-to-Equity Ratio
* Interest Coverage Ratio
* Asset Turnover Ratio
* Net Debt
* High Leverage Flag
* Debt-Free Classification

Business rules correctly handle:

* Zero borrowings
* Zero interest
* Negative equity
* Invalid denominators

---

# CAGR Engine

Implemented compound annual growth calculations for:

* Revenue CAGR
* Net Profit (PAT) CAGR
* Earnings Per Share (EPS) CAGR

Supported periods:

* 3-Year CAGR
* 5-Year CAGR
* 10-Year CAGR

Implemented edge-case handling for:

* Normal Growth
* Zero Base
* Turnaround Companies
* Decline to Loss
* Both Values Negative
* Insufficient Historical Data

Generated reports:

* revenue_cagr.csv
* pat_cagr.csv
* eps_cagr.csv
* cagr_edge_cases.csv

---

# Cash Flow KPIs

Implemented:

* Free Cash Flow
* FCF Conversion
* CapEx Intensity
* CFO Quality Score
* Capital Allocation Pattern Classification

Capital allocation patterns include:

* Reinvestor
* Shareholder Returns
* Liquidating Assets
* Growth Funded by Debt
* Distress Signal
* Cash Accumulator
* Mixed
* Pre-Revenue

Generated:

* capital_allocation.csv

---

# Database Integration

Computed KPIs are prepared for insertion into the SQLite analytics layer while preserving imported source data.

The architecture separates:

* Raw Financial Data
* Imported Ratios
* Computed Analytics

This design enables reproducibility and easier validation.

---

# Validation

Completed validation includes:

* Profitability ratio verification
* ROE comparison against source ratios
* Operating Margin cross-checks
* CAGR edge-case validation
* Debt-free company handling
* Zero denominator protection

Automated reports are generated under the reports directory for downstream review.

---

# Testing

Unit tests cover:

* Ratio calculations
* Leverage functions
* CAGR engine
* Cash Flow KPIs

Edge cases include:

* Zero sales
* Zero assets
* Zero borrowings
* Zero interest
* Negative equity
* Turnaround scenarios
* Zero-base CAGR
* Insufficient historical data

---

# Architecture Improvements

Sprint 2 refactored the analytics layer into reusable modules instead of embedding business logic inside a single script.

Benefits include:

* Modular architecture
* Reusable financial formulas
* Easier maintenance
* Improved scalability
* Better unit test coverage
* Clear separation of concerns

---

# Key Outputs

Generated reports include:

* day09_ratio_engine.csv
* profitability_ratios.csv
* revenue_cagr.csv
* pat_cagr.csv
* eps_cagr.csv
* capital_allocation.csv
* cagr_edge_cases.csv
* ratio_edge_cases.log

---

# Sprint Outcome

Sprint 2 successfully transformed the project from a validated financial database into a reusable financial analytics engine capable of computing profitability, leverage, efficiency, growth, and cash flow metrics across historical company financials.

The platform is now ready for advanced analytics, screening, visualization, and dashboard integration in subsequent development phases.
