import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Page settings
st.set_page_config(page_title="📈 Nifty Stock Analyzer", layout="wide")

# Title
st.title("📈 Nifty Stock Analyzer with SMA 50 & SMA 200")

# Load CSV safely
@st.cache_data
def load_data():
    csv_path = "Stocks_2025.csv"  # adjust this if your path differs

    if not os.path.exists(csv_path):
        st.error(f"❌ File not found at path: {csv_path}")
        st.stop()

    df = pd.read_csv(csv_path)

    # Drop unnamed index column if present
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)

    # Convert date
    df['Date'] = pd.to_datetime(df['Date'])

    # Clean stock names (optional)
    df['Stock'] = df['Stock'].astype(str).str.strip()

    # Compute moving averages
    df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()
    df['SMA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()

    return df

# Load data
df = load_data()

# Sidebar for filters
st.sidebar.header("🔍 Filter Options")

# Category selector
categories = df['Category'].dropna().unique()
selected_category = st.sidebar.selectbox("Select Category", sorted(categories))

# Filter stocks based on category
stocks_in_category = df[df['Category'] == selected_category]['Stock'].unique()
selected_stock = st.sidebar.selectbox("Select Stock", sorted(stocks_in_category))

# Filter dataframe for selection
filtered_df = df[(df['Category'] == selected_category) & (df['Stock'] == selected_stock)]

# Check if data exists
if filtered_df.empty:
    st.warning("No data found for selected category and stock.")
    st.stop()

# Plotting
st.subheader(f"📊 {selected_stock} - Close Price with SMA 50 & SMA 200")

fig, ax = plt.subplots(figsize=(14, 6))

sns.lineplot(data=filtered_df, x='Date', y='Close', label='Cl_
