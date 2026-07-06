# Composite Scoring Summary

## Formula

The composite quality score combines four sub-scores:

- Profitability score: ROE, ROCE, and net profit margin
- Cash quality score: free cash flow, CFO quality score, and positive FCF flag
- Growth score: revenue CAGR 5Y and PAT CAGR 5Y
- Leverage score: debt-to-equity and interest coverage

## Weights

- Profitability: 35% total
  - ROE: 15%
  - ROCE: 10%
  - Net Profit Margin: 10%
- Cash quality: 30% total
  - Free Cash Flow: 15%
  - CFO Quality: 10%
  - Positive FCF Flag: 5%
- Growth: 20% total
  - Revenue CAGR 5Y: 10%
  - PAT CAGR 5Y: 10%
- Leverage: 15% total
  - Debt to Equity: 10%
  - Interest Coverage: 5%

## Finance Explanation

The framework rewards companies with strong returns, healthy cash conversion, durable growth, and prudent leverage. Lower debt and higher coverage improve the leverage component, while negative free cash flow reduces cash quality.

## Validation

- Values are normalized to a 0-100 range.
- Outliers are capped using winsorization.
- Each company also receives a sector-relative score computed within its broad sector.
- The screener engine applies the composite score before preset execution and sorts ranked companies by composite score descending.
