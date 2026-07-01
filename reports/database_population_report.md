# Database Population Report

## Objective
Populate the financial_ratios table with computed Sprint 2 KPI values.

## Formula
- Profitability and leverage ratios are calculated using the existing analytics modules.
- Cash flow metrics use operating, investing and financing activity flows.

## Business Meaning
- These metrics support screening, valuation and quality analysis.

## Implementation
- The workflow loads profit-and-loss, balance-sheet and cash-flow data.
- Calculated metrics are written to the financial_ratios table.

## Validation
- A row count check confirms the table has been populated.
- Total rows in financial_ratios: 1263
- Total columns populated: 23

## Output Summary
- The database now contains 23 Sprint 2 KPI columns in financial_ratios.
- All CAGR columns are present and any missing values are null-filled for unmatched horizons.
