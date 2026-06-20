import pandas as pd
from src.config.settings import RAW_DATA

CORE_FILES = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx"
]

SUPPORT_FILES = [
    "financial_ratios.xlsx",
    "market_cap.xlsx",
    "peer_groups.xlsx",
    "sectors.xlsx",
    "stock_prices.xlsx"
]


def load_dataset(filename, header):
    path = RAW_DATA / filename

    return pd.read_excel(
        path,
        header=header
    )


def load_all_datasets():
    datasets = {}

    for file in CORE_FILES:
        datasets[file] = load_dataset(
            file,
            header=1
        )

    for file in SUPPORT_FILES:
        datasets[file] = load_dataset(
            file,
            header=0
        )

    return datasets


if __name__ == "__main__":

    datasets = load_all_datasets()

    for name, df in datasets.items():

        print("\n" + "=" * 50)
        print(name)
        print(df.shape)