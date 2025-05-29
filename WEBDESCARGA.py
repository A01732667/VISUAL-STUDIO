# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# %%
df = pd.read_excel("sellers.xlsx")

# %%
df.head()

# %%
import streamlit as st


# %%
# Title and Sidebar
st.title("Sellers Data Analysis")
st.sidebar.header("Filter Options")

# Load data (assuming df is already loaded above this code)

# Filter by Region
region_options = df['REGION'].unique()
selected_region = st.sidebar.selectbox("Select REGION", options=["All"] + list(region_options))

if selected_region != "All":
    df_region = df[df['REGION'] == selected_region]
else:
    df_region = df

# Filter by Seller
seller_options = df_region['NOMBRE'].unique()
selected_seller = st.sidebar.selectbox("Select Seller", options=["All"] + list(seller_options))

if selected_seller != "All":
    df_vendor = df_region[df_region['NOMBRE'] == selected_seller]
else:
    df_vendor = df_region




# %%
#Filtering display

st.subheader("Filtered Data")
st.dataframe(df_vendor)


# %%
#KPIS

col1, col2, col3 = st.columns(3)
col1.metric("Total Units Sold", int(df_vendor['UNIDADES VENDIDAS'].sum()))
col2.metric("Total Sales", f"${df_vendor['VENTAS TOTALES'].sum():,.2f}")


# %%
# Visualization selection


st.subheader("Sales Visualizations")
chart_type = st.radio("Select Chart", ["Units Sold", "Total Sales"])

if chart_type == "Units Sold":
    chart_data = df_vendor.groupby('NOMBRE')['UNIDADES VENDIDAS'].sum().sort_values()
    st.bar_chart(chart_data)
elif chart_type == "Total Sales":
    chart_data = df_vendor.groupby('NOMBRE')['VENTAS TOTALES'].sum().sort_values()
    st.bar_chart(chart_data)
else:
    chart_data = df_vendor.groupby('NOMBRE')['VENTAS TOTALES'].mean().sort_values()
    st.bar_chart(chart_data)
    

# %%
#Download button for filtered data

st.download_button("Download Filtered Data as CSV", df_vendor.to_csv(index=False), "filtered_sellers.csv")


# %%


# %%



