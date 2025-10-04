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
    csv_path = "Stocks_2025.csv"  # Change this if needed

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

# Filter stocks by selected category
stocks_in_category = df[df['Category'] == selected_category]['Stock'].unique()
selected_stock = st.sidebar.selectbox("Select Stock", sorted(stocks_in_category))

# Final filter by category and stock
filtered_df = df[(df['Category'] == selected_category) & (df['Stock'] == selected_stock)]

# Show warning if no data
if filtered_df.empty:
    st.warning("No data found for the selected category and stock.")
    st.stop()

# Plot the chart
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

# Show raw data
with st.expander("📄 Show Raw Data Table"):
    st.dataframe(filtered_df.reset_index(drop=True))
