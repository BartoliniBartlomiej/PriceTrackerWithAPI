import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os
import time

st.set_page_config(page_title="Live Price Tracker", layout="wide")

if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

from pathlib import Path


def get_data():
    base_path = Path(__file__).resolve().parents[1]
    db_path = base_path / "app/prices.db"

    if not db_path.exists():
        st.error(f"Plik bazy NIE ISTNIEJE w: {db_path}")
        return pd.DataFrame()

    conn = sqlite3.connect(str(db_path))

    check_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='price_history';"
    table_exists = pd.read_sql(check_query, conn)

    if table_exists.empty:
        st.error(f"Baza znaleziona w {db_path}, ale jest PUSTA (brak tabel). Uruchom main.py!")
        conn.close()
        return pd.DataFrame()

    query = """
    SELECT p.name, ph.price, ph.timestamp 
    FROM price_history ph
    JOIN products p ON ph.product_id = p.id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.title("Live Financial Monitor")

if st.button('Refresh'):
    st.rerun()

data = get_data()

if not data.empty:
    selected_product = st.selectbox("Choose good:", data['name'].unique())
    df_plot = data[data['name'] == selected_product].copy()
    df_plot['timestamp'] = pd.to_datetime(df_plot['timestamp'])

    if len(df_plot) > 1:
        last_price = df_plot.iloc[-1]['price']
        prev_price = df_plot.iloc[-2]['price']
        delta = last_price - prev_price
        st.metric(label=f"Current price {selected_product}", value=f"{last_price} PLN", delta=f"{delta:.2f} PLN")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_plot['timestamp'], df_plot['price'], color='#00ff00' if 'Bitcoin' in selected_product else '#1f77b4')
    plt.xticks(rotation=45)
    st.pyplot(fig)