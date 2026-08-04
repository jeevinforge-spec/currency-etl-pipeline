import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="Currency Rate Tracker", layout="wide")

engine = create_engine("sqlite:///currency_rates.db")

st.title("💱 Currency Exchange Rate Tracker")
st.caption("ETL pipeline: extracts, transforms, and loads live exchange rate data over time")

@st.cache_data(ttl=60)
def load_data():
    return pd.read_sql("SELECT * FROM exchange_rates", engine)

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_sql("SELECT * FROM exchange_rates", engine)
    df["fetched_at"] = pd.to_datetime(df["fetched_at"])
    # Round to the nearest minute so all rows from the same pipeline run group together
    df["run_time"] = df["fetched_at"].dt.floor("min")
    return df

df = load_data()

if df.empty:
    st.warning("No data yet. Run pipeline.py first to populate the database.")
else:
    st.subheader("Latest Snapshot")
    latest_run = df["run_time"].max()
    latest = df[df["run_time"] == latest_run]
    st.caption(f"From pipeline run at {latest_run}")
    st.dataframe(latest[["target_currency", "rate"]].sort_values("target_currency"), use_container_width=True)

    st.subheader("Track a Currency Over Time")
    currencies = sorted(df["target_currency"].unique())
    default_idx = currencies.index("LKR") if "LKR" in currencies else 0
    selected = st.selectbox("Choose a currency", currencies, index=default_idx)

    currency_history = df[df["target_currency"] == selected].sort_values("fetched_at")
    st.line_chart(currency_history.set_index("fetched_at")["rate"])

    st.subheader("Raw Data")
    st.dataframe(df.sort_values("fetched_at", ascending=False), use_container_width=True)