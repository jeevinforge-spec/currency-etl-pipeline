import requests
from datetime import datetime


def fetch_rates(base_currency = "USD"):
    url = f"https://api.frankfurter.dev/v1/latest?base={base_currency}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data

if __name__ == "__main__":
    data = fetch_rates("USD")
    print(f"Date: {data['date']}")
    print(f"Base: {data['base']}")
    print("Rates:")
    for currency, rate in data["rates"].items():
        print(f"  {currency}: {rate}")