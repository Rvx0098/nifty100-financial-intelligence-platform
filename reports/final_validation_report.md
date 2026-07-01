# Final Validation Report

## Sprint Status
- Sprint 1: Complete
- Sprint 2: Complete
- Remaining work: None for Sprint 2 population workflow

## Database Row Count
- `financial_ratios` row count: 1263

## Financial Ratios Populated
- Profitability ratios: `net_profit_margin_pct`, `operating_margin_pct`, `return_on_equity_pct`, `return_on_assets_pct`, `return_on_capital_employed_pct`
- Leverage metrics: `debt_to_equity`, `interest_coverage`, `asset_turnover`, `net_debt`
- Cash flow metrics: `free_cash_flow`, `fcf_conversion`, `capex_intensity`, `cfo_quality_score`, `composite_quality_score`
- CAGR metrics: `revenue_cagr_3yr`, `revenue_cagr_5yr`, `revenue_cagr_10yr`, `pat_cagr_3yr`, `pat_cagr_5yr`, `pat_cagr_10yr`, `eps_cagr_3yr`, `eps_cagr_5yr`, `eps_cagr_10yr`

## Reports Generated
- `reports/database_population_report.md`
- `reports/ratio_edge_cases.log`
- Existing sprint reports remain available in `reports/`

## Unit Test Results
- Total tests run: 36
- Passed: 36
- Failed: 0

## Edge Case Summary
- Financial-sector carve-out report generated for banks, NBFCs, and insurers.
- Financial sector records analyzed: 329
- ROE/ROCE comparison rows: 294
- Top differences are documented in `reports/ratio_edge_cases.log`.

## Known Limitations
- Source tables in SQLite may contain duplicate rows by `company_id` and `year`; the population workflow deduplicates on load and keeps the first occurrence.
- CAGR values for unmatched horizons are null by design when historical data is not available.
- `TTM` rows are excluded from numeric year extraction and CAGR calculations.
