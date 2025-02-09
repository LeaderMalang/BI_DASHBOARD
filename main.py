import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Excel file
file_path = "Master Inventory.xlsx"
df = pd.read_excel(file_path, sheet_name="stock inventory")
# df.replace("#REF!", pd.NA, inplace=True)
# df.dropna(how="all", inplace=True)
# Clean and process data
#df.columns = df.columns.str.strip()
df.columns =df.head()._values[0:5][4]

# Replace "#REF!" with NaN
df.replace("#REF!", pd.NA, inplace=True)
df = df.astype(str)
# Drop fully empty rows & columns
df.dropna(how="all", inplace=True)
df.dropna(axis=1, how="all", inplace=True)
df["Initial Stock"] = pd.to_numeric(df["Initial Stock"], errors="coerce")
df["Stock In "] = pd.to_numeric(df["Stock In "], errors="coerce")
df["Stock out"] = pd.to_numeric(df["Stock out"], errors="coerce")
df["BLNC"] = pd.to_numeric(df["BLNC"], errors="coerce")
df["PRICE"] = pd.to_numeric(df["PRICE"], errors="coerce")
df["Stock Value"] = df["BLNC"] * df["PRICE"]

# Streamlit UI
st.title("📊 Stock Inventory BI Dashboard")

# Stock Summary
st.header("Stock Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Initial Stock", f"{df['Initial Stock'].sum():,.2f}")
col2.metric("Total Stock In", f"{df['Stock In '].sum():,.2f}")
col3.metric("Total Stock Out", f"{df['Stock out'].sum():,.2f}")

col4, col5 = st.columns(2)
col4.metric("Total Balance Stock", f"{df['BLNC'].sum():,.2f}")
col5.metric("Total Stock Value", f"{df['Stock Value'].sum():,.2f}")

# Stock by Fabric Type
st.header("Stock by Fabric Type")
fabric_stock = df.groupby("FABRIC TYPE")["BLNC"].sum().reset_index()
st.bar_chart(fabric_stock.set_index("FABRIC TYPE"))

# Stock by Origin
st.header("Stock by Origin")
origin_stock = df.groupby("ORIGN")["BLNC"].sum().reset_index()
st.bar_chart(origin_stock.set_index("ORIGN"))

# Top 10 Most Sold Items
st.header("Top 10 Most Sold Items")
top_sold = df.nlargest(10, "Stock out")
st.bar_chart(top_sold.set_index("DESIGN NO")["Stock out"])

# Low Stock Alert
st.header("Low Stock Alert (Below 10)")
low_stock = df[df["BLNC"] < 10]
st.dataframe(low_stock)

# Download Processed Data
st.download_button(label="Download Processed Data", data=df.to_csv(), file_name="processed_stock_data.csv", mime="text/csv")

st.write("Developed by **Hassan Ali* 🚀")

