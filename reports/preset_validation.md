# Preset Screener Validation

## Summary

The screener engine now loads the profit-and-loss table, normalizes the financial year once, merges on company_id plus financial_year, keeps the latest company snapshot before preset filtering, and reports the key validation metrics.

## Presets

| Preset | Rows Returned | Unique Companies | Top Companies | Reason Filters Passed |
| --- | ---: | ---: | --- | --- |
| quality_compounder | 20 | 20 | INDIGO, NESTLEIND, LT, TCS, ADANIPOWER | ROE >= 15, D/E <= 1, FCF > 0, Revenue CAGR 5Y >= 10 |
| value_pick | 2 | 2 | MOTHERSON, M&M | PE <= 20, PB <= 3, D/E <= 2, Dividend Yield >= 1 |
| growth_accelerator | 9 | 9 | INDIGO, TRENT, ADANIENT, IRCTC, LTIM | PAT CAGR 5Y >= 20, Revenue CAGR 5Y >= 15, D/E <= 2 |
| dividend_champion | 0 | 0 | None | Dividend Yield >= 2, Dividend Payout <= 80, FCF > 0 |
| debt_free_bluechip | 6 | 6 | BOSCHLTD, MARUTI, ICICIGI, SBILIFE, ITC | D/E == 0, ROE >= 12, Sales >= 5000 |
| turnaround_watch | 59 | 59 | ABB, ADANIENSOL, ADANIPORTS, ADANIPOWER, APOLLOHOSP | Revenue CAGR 3Y >= 10, FCF > 0, D/E improvement TODO |

## Missing Data Summary

- Market cap rows can remain unmatched where the market-cap table has a narrower period than financial_ratios.
- Sector rows may remain unmatched for companies without sector mapping.
- Sales values are loaded from profitandloss and should be present after the merge.

## Threshold Summary

- Dividend thresholds are validated with descriptive statistics and warning logs when the current data distribution makes them impossible to satisfy.
- Presets run on the latest company snapshot so they do not evaluate multiple company-year rows per company.
