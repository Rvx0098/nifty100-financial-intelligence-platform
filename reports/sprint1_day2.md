## Data Quality Rule 3 Investigation

Duplicate company-year combinations were identified across multiple datasets.

Investigation of Adani Ports FY2024 records revealed that duplicate rows were identical across all financial attributes and differed only by internal record ID.

Conclusion:

The duplicates are data-ingestion duplicates rather than separate financial disclosures.

Recommended Action:

Apply exact-row deduplication during the ETL transformation stage before loading records into the analytics database.

## Data Quality Finding #2

Duplicate company-year combinations were detected across multiple financial datasets.

Initial investigation showed that records differed by internal identifier fields while sharing the same business keys (company_id and year).

Conclusion:

The project contains business-level duplicates rather than exact row duplicates.

Next Step:

Validate duplicate records using business keys and define primary key constraints before final database loading.


## Data Quality Rule 3 - Business Duplicate Analysis

Objective:
Identify duplicate financial statements using business keys.

Business Key:
company_id + year

Findings:

* Profit & Loss: 13 duplicates removed
* Balance Sheet: 87 duplicates removed
* Cash Flow: 23 duplicates removed
* Financial Ratios: 119 duplicates removed
* Market Cap: 0 duplicates removed

Total Duplicate Records Removed: 242

Conclusion:

The datasets contained business-level duplicates caused by repeated financial statements with different surrogate IDs.

Impact:

Removing duplicates improves KPI accuracy, prevents double-counting of financial metrics, and ensures reliable downstream analytics.


## Data Quality Rule 4 - Balance Sheet Validation

Objective:
Verify accounting consistency across all balance sheet records.

Method:
Calculated:

difference = total_assets - total_liabilities

Results:

* Mean Difference: 0
* Standard Deviation: 0
* Minimum Difference: 0
* Maximum Difference: 0

Conclusion:

All balance sheet records satisfy the accounting equation used by the dataset.

Result:

100% validation pass rate.
