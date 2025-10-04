import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Page configuration
st.set_page_config(page_title="Nifty Stock Analyzer", layout="wide")

st.title("📈 Nifty Stock Analyzer with SMA 50 & SMA 200")

# Function to load data with path safety
@st.cache_data
def load_data():
    # Change this path if needed
    csv_path = "DataSets/Nifty/Stocks_2025.csv"

    if not os.path.exists(csv_path):
        st.error(f"CSV file not found at: {csv_path}")
        st.stop()

    df = pd.read_csv(csv_path)

    # Drop unnamed column if exists
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)

    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Clean Stock names (optional)
    df['Stock'] = df['Stock'].astype(str).str.strip()

    # Calculate SMAs
    df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()
    df['SMA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()

    return df

# Load data
df = load_data()

# Sidebar for user input
st.sidebar.header("📊 Filter Options")

# Category selection
categories = df['Category'].dropna().unique()
selected_category = st.sidebar.selectbox("Select Category", sorted(categories))

# Filter based on category
filtered_df = df[df['Category'] == selected_category]

# Stock selection
stocks = filtered_df['Stock'].dropna().unique()
selected_stock = st.sidebar.selectbox("Select Stock", sorted(stocks))

# Final filtered data
stock_df = filtered_df[filtered_df['Stock'] == selected_stock]

# Plotting
st.subheader(f"📌 {selected_stock} Price with SMA 50 & SMA 200")

fig, ax = plt.subplots(figsize=(14, 6))

sns.lineplot(data=stock_df, x='Date', y='Close', label='Close Price', ax=ax)
sns.lineplot(data=stock_df, x='Date', y='SMA_50', label='SMA 50', ax=ax)
sns.lineplot(data=stock_df, x='Date', y='SMA_200', label='SMA 200', ax=ax)

ax.set_title(f"{selected_stock} - Price and Moving Averages", fontsize=16)
ax.set_xlabel("Date")
ax.set_ylabel("Price")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

st.pyplot(fig)

# Optional: Show raw data
with st.expander("📄 Show Raw Data"):
    st.dataframe(stock_df.reset_index(drop=True))



