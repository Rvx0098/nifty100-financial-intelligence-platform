# Cash Flow Summary

## Objective
Summarize the cash flow KPIs generated for the N100 Financial Intelligence Platform.

## Formula
- Free Cash Flow = Operating Activity + Investing Activity
- FCF Conversion = FCF / Operating Profit
- CapEx Intensity = abs(Investing Activity) / Sales
- CFO Quality Score = Operating Cash Flow / Net Profit

## Business Meaning
These metrics indicate whether a company is generating cash, reinvesting in growth, returning capital to shareholders or facing distress.

## Implementation
The workflow reads cash flow, profit-and-loss and balance-sheet data, computes the KPIs and writes the results to reports/capital_allocation.csv.

## Validation
The output is verified by checking the generated report and the underlying calculations.

## Output Summary
The report contains free cash flow, FCF conversion, capex intensity, CFO quality score and capital allocation patterns.
