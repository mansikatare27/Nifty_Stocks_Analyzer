import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np

# Page settings
st.set_page_config(page_title="📈 Nifty Stock Analyzer", layout="wide")

# App title
st.title("📈 Nifty Stock Analyzer with SMA 50 & SMA 200")

# Load CSV safely
@st.cache_data
def load_data():
    csv_path = "Stocks_2025.csv"  # <-- Change this if your path is different

    if not os.path.exists(csv_path):
        st.error(f"❌ File not found at path: {csv_path}")
        st.stop()

    df = pd.read_csv(csv_path)

    # Drop index column if exists
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)

    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Clean up Stock names
    df['Stock'] = df['Stock'].astype(str).str.strip()

    # Calculate Simple Moving Averages
    df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()
    df['SMA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()

    return df

# Load the data
df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# Category selection
categories = df['Category'].dropna().unique()
selected_category = st.sidebar.selectbox("Select Category", sorted(categories))

# Filter stocks by category
stocks_in_category = df[df['Category'] == selected_category]['Stock'].unique()
selected_stock = st.sidebar.selectbox("Select Stock", sorted(stocks_in_category))

# Filter data for selected stock
filtered_df = df[(df['Category'] == selected_ca_]()_
