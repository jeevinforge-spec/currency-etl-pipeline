import pandas as pd
from datetime import datetime
from extract import fetch_rates
from datetime import datetime, timezone

def transform_rates(raw_data):
    rows = []
    for currency, rate in raw_data["rates"].items():
        rows.append({
            "date": raw_data["time_last_update_utc"],
            "base_currency": raw_data["base_code"],
            "target_currency": currency,
            "rate": rate,
            "fetched_at": datetime.now(timezone.utc).isoformat()
        })
    df = pd.DataFrame(rows)
    return df

input_curr = str(input("Enter the Base Currency : ")).upper()

if __name__ == "__main__":
    raw = fetch_rates(input_curr)
    df = transform_rates(raw)
    print(df.head(10))
    print(f"\nTotal rows: {len(df)}")
    print(f"\nColumn types:\n{df.dtypes}")