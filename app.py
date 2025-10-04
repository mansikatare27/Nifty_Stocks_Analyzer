import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Page settings
st.set_page_config(page_title="📈 Nifty Stock Analyzer", layout="wide")

# App title
st.title("📈 Nifty Stock Analyzer with SMA 50 & SMA 200")

# Load CSV safely
@st.cache_data
def load_data():
    csv_path = "Stocks_2025.csv"  # <-- Adjust if your path is different

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
st.sidebar.header("🔍 Filter

    
