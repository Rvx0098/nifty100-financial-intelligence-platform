from src.etl.extract import load_all_datasets

datasets = load_all_datasets()

business_key_map = {
    "profitandloss.xlsx": ["company_id", "year"],
    "balancesheet.xlsx": ["company_id", "year"],
    "cashflow.xlsx": ["company_id", "year"],
    "financial_ratios.xlsx": ["company_id", "year"],
    "market_cap.xlsx": ["company_id", "year"]
}

for name, df in datasets.items():

    if name not in business_key_map:
        continue

    before = len(df)

    df_clean = df.drop_duplicates(
        subset=business_key_map[name]
    )

    after = len(df_clean)

    removed = before - after

    print(
        f"{name:<25}"
        f" Before:{before:<5}"
        f" After:{after:<5}"
        f" Removed:{removed}"
    )