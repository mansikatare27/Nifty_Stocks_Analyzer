import pandas as pd
import streamlit as st
import seaborn as sb
import matplotlib.pyplot as plt

# Title
st.title("📈 Stock Price Viewer with SMA (50 & 200)")

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("Stocks_2025.csv")
    df = df.drop('Unnamed: 0', axis=1)
    df["SMA_50"] = df["Close"].rolling(window=50, min_periods=1).mean()
    df["SMA_200"] = df["Close"].rolling(window=200, min_periods=1).mean()
    df["Date"] = pd.to_datetime(df["Date"])
    df["Stock"] = df["Stock"].replace(" ", " ", regex=True)
    return df

df = load_data()

# Category selection
categories = df['Category'].dropna().unique()
selected_category = st.selectbox("Select Category", sorted(categories))

# Stock selection
filtered_by_category = df[df["Category"] == selected_category]
stocks = filtered_by_category['Stock'].dropna().unique()
selected_stock = st.selectbox("Select Stock", sorted(stocks))

# Filter final data
final_df = filtered_by_category[filtered_by_category["Stock"] == selected_stock]

# Plotting
fig, ax = plt.subplots(figsize=(12, 6))

sb.lineplot(data=final_df, x="Date", y="Close", label="Close Price", ax=ax)
sb.lineplot(data=final_df, x="Date", y="SMA_50", label="SMA 50", ax=ax)
sb.lineplot(data=final_df, x="Date", y="SMA_200", label="SMA 200", ax=ax)

plt.xticks(rotation=45)
plt.title(f"{selected_stock} Price with SMA")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)

st.pyplot(fig)
