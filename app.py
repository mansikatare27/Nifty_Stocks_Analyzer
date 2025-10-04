import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Page settings
st.set_page_config(page_title="📈 Nifty Stock Analyzer", layout="wide")

# App title
st.title("📈 Nifty Stock Analyzer with SMA 50 & SMA 200")

# Load CSV safely with caching
@st.cache_data
def load_data():
    csv_path = "Stocks_2025.csv"  # Change if your CSV path differs

    if not os.path.exists(csv_path):
        st.error(f"❌ File not found at path: {csv_path}")
        st.stop()

    df = pd.read_csv(csv_path)

    # Drop index column if it exists
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)

    # Safely convert Date column to datetime, coerce errors to NaT
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Drop rows where Date conversion failed
    df = df.dropna(subset=['Date'])

    # Clean Stock names (strip whitespace)
    df['Stock'] = df['Stock'].astype(str).str.strip()

    # Calculate SMAs
    df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()
    df['SMA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()

    return df

# Load data
df = load_data()

# Sidebar filter options
st.sidebar.header("🔍 Filter Options")

# Category select box
categories = df['Category'].dropna().unique()
selected_category = st.sidebar.selectbox("Select Category", sorted(categories))

# Filter stocks by category
stocks_in_category = df[df['Category'] == selected_category]['Stock'].unique()
selected_stock = st.sidebar.selectbox("Select Stock", sorted(stocks_in_category))

# Filter data for chosen stock and category
filtered_df = df[(df['Category'] == selected_category) & (df['Stock'] == selected_stock)]

if filtered_df.empty:
    st.warning("No data found for the selected category and stock.")
    st.stop()

# Plotting
st.subheader(f"📊 {selected_stock} - Close Price with SMA 50 & SMA 200")

fig, ax = plt.subplots(figsize=(14, 6))

sns.lineplot(data=filtered_df, x='Date', y='Close', label='Close Price', ax=ax)
sns.lineplot(data=filtered_df, x='Date', y='SMA_50', label='SMA 50', ax=ax)
sns.lineplot(data=filtered_df, x='Date', y='SMA_200', label='SMA 200', ax=ax)

ax.set_title(f"{selected_stock} Price Trend", fontsize=16)
ax.set_xlabel("Date")
ax.set_ylabel("Price")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

st.pyplot(fig)

# Expandable raw data table
with st.expander("📄 Show Raw Data Table"):
    st.dataframe(filtered_df.reset_index(drop=True))

   
