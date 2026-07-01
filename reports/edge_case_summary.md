# Edge Case Summary

## Purpose
Summarize the financial-sector ROE and ROCE comparison findings produced by the edge-case review.

## Findings
- Financial sector carve-out report generated for banks, NBFCs, and insurers.
- Total financial sector records analyzed: 329
- ROE/ROCE comparison rows: 294

## Observations
- The edge-case report confirms the financial sector is being identified correctly.
- Computed ROE and ROCE values were matched against the imported profitability dataset.

## Output
- Detailed differences written to `reports/ratio_edge_cases.log`.
- Summary of the edge-case review is available in this file.

## Notes
- The financial-sector classification logic includes any sector label containing `bank`, `nbfc`, `insurance`, `finance`, or `financial`.
- Rows without imported comparisons are excluded from the ROE/ROCE difference summary, but the report still tracks the overall analyzed population.
