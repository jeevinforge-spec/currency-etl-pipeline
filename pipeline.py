from extract import fetch_rates
from transform import transform_rates
from load import get_engine, load_rates, show_table_info

def run_pipeline(base_currency="USD"):
    print(f"Running pipeline for base currency: {base_currency}")
    
    raw = fetch_rates(base_currency)
    print("Extract complete.")
    
    df = transform_rates(raw)
    print("Transform complete.")
    
    engine = get_engine()
    load_rates(df, engine)
    show_table_info(engine)
    print("Pipeline run complete.\n")

if __name__ == "__main__":
    run_pipeline("USD")