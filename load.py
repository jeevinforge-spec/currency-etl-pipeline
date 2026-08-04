from sqlalchemy import create_engine, text
import pandas as pd
from transform import transform_rates
from extract import fetch_rates

DB_PATH = "sqlite:///currency_rates.db"

def get_engine():
    return create_engine(DB_PATH)

def load_rates(df, engine):
    df.to_sql("exchange_rates", engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into exchange_rates table")

def show_table_info(engine):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM exchange_rates"))
        count = result.scalar()
        print(f"Total rows in database: {count}")

if __name__ == "__main__":
    base = input("Enter the Base Currency : ").strip().upper() or "USD"
    raw = fetch_rates(base)
    df = transform_rates(raw)

    engine = get_engine()
    load_rates(df, engine)
    show_table_info(engine)