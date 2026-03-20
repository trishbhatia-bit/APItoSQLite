import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px # Optional: for charts

# --- Page Config ---
st.set_page_config(page_title="User Data Pipeline Dashboard", layout="wide")

st.title("User ETL Pipeline Monitor")
st.markdown("Real-time insights from the `warehouse.db` SQLite database.")

# --- Helper Function to Load Data ---
def get_data():
    conn = sqlite3.connect("data/warehouse.db")
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    return df

try:
    df = get_data()

    # --- Top Row: Key Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Valid Users", len(df))
    col2.metric("Unique Cities", df['city'].nunique())
    col3.metric("Top Company", df['company_name'].value_counts().idxmax())

    # --- Middle Row: Visuals ---
    st.divider()
    left_chart, right_chart = st.columns(2)

    with left_chart:
        st.subheader("Users per City")
        city_counts = df['city'].value_counts().reset_index()
        st.bar_chart(data=city_counts, x='city', y='count')

    with right_chart:
        st.subheader("Email Domain Distribution")
        df['domain'] = df['email'].apply(lambda x: x.split('@')[-1])
        st.write(df['domain'].value_counts())

    # --- Bottom Row: Raw Data Table ---
    st.divider()
    st.subheader("📂 Validated Records (Database View)")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Could not load data. Has the pipeline run yet? Error: {e}")

import os

def get_data():
    # This finds the directory where dashboard.py lives
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # This creates a foolproof path to the db file
    db_path = os.path.join(base_dir, "data", "warehouse.db")
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at {db_path}")
        
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    return df