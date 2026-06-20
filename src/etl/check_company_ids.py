from src.etl.extract import load_all_datasets

datasets = load_all_datasets()

for name, df in datasets.items():

    if "company_id" in df.columns:

        print("\n" + "=" * 50)
        print(name)

        print(
            df["company_id"]
            .head()
            .tolist()
        )