from src.dashboard.utils.db import get_companies

companies = get_companies()

print(companies.head())

print()

print("Companies:", len(companies))