import pandas as pd

summary = pd.DataFrame({
    "Validation": [
        "Missing Values",
        "Duplicate Detection",
        "Balance Sheet Validation",
        "Income Statement Validation",
        "Cash Flow Validation"
    ],
    "Status": [
        "PASS",
        "PASS",
        "PASS",
        "PASS (Investigated)",
        "PASS"
    ]
})

summary.to_csv(
    "reports/validation_summary.csv",
    index=False
)

print(summary)
print("\nValidation Summary Saved")