import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sales Data Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load data
df = pd.read_csv("sales_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Title
st.title("📊 Sales Data Analysis Dashboard")
st.write("Interactive Sales Analysis using Python")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Apply Filters")

# Region
region_options = sorted(df["Region"].unique())

selected_regions = st.sidebar.multiselect(
    "Select Region",
    region_options,
    default=region_options
)

# Category
category_options = sorted(df["Category"].unique())

selected_categories = st.sidebar.multiselect(
    "Select Category",
    category_options,
    default=category_options
)

# Product
product_options = sorted(df["Product"].unique())

selected_products = st.sidebar.multiselect(
    "Select Product",
    product_options,
    default=product_options
)

# Date
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# ---------------- FILTER DATA ----------------

filtered_df = df.copy()

# Region filter
if selected_regions:
    filtered_df = filtered_df[
        filtered_df["Region"].isin(selected_regions)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

# Category filter
if selected_categories:
    filtered_df = filtered_df[
        filtered_df["Category"].isin(selected_categories)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

# Product filter
if selected_products:
    filtered_df = filtered_df[
        filtered_df["Product"].isin(selected_products)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

# Date filter
if len(selected_dates) == 2:
    start_date = pd.to_datetime(selected_dates[0])
    end_date = pd.to_datetime(selected_dates[1])

    filtered_df = filtered_df[
        (filtered_df["Date"] >= start_date) &
        (filtered_df["Date"] <= end_date)
    ]

# ---------------- CHECK DATA ----------------

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ---------------- KPI CALCULATIONS ----------------

total_sales = filtered_df["Sales"].sum()
total_products = filtered_df["Quantity"].sum()

top_product = (
    filtered_df.groupby("Product")["Sales"]
    .sum()
    .idxmax()
)

best_region = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .idxmax()
)

# ---------------- KPI CARDS ----------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Sales",
    f"₹{total_sales:,.0f}"
)

col2.metric(
    "📦 Products Sold",
    f"{total_products:,}"
)

col3.metric(
    "🏆 Top Product",
    top_product
)

col4.metric(
    "🌍 Best Region",
    best_region
)

st.divider()

# ---------------- SALES BY PRODUCT ----------------

st.subheader("📊 Sales by Product")

product_sales = (
    filtered_df
    .groupby("Product", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)

fig_product = px.bar(
    product_sales,
    x="Product",
    y="Sales",
    text_auto=True,
    title="Sales by Product"
)

st.plotly_chart(
    fig_product,
    use_container_width=True
)

# ---------------- MONTHLY SALES ----------------

st.subheader("📈 Monthly Sales")

monthly_sales = (
    filtered_df
    .assign(Month=filtered_df["Date"].dt.strftime("%b"))
    .groupby("Month", as_index=False)["Sales"]
    .sum()
)

fig_month = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(
    fig_month,
    use_container_width=True
)

# ---------------- SALES BY REGION ----------------

st.subheader("🌍 Sales by Region")

region_sales = (
    filtered_df
    .groupby("Region", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)

fig_region = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    text_auto=True,
    title="Sales by Region"
)

st.plotly_chart(
    fig_region,
    use_container_width=True
)

# ---------------- DATA TABLE ----------------

st.subheader("📋 Filtered Sales Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# ---------------- DOWNLOAD ----------------

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Filtered Data",
    csv_data,
    "filtered_sales_data.csv",
    "text/csv"
)

st.success("Dashboard loaded successfully! 🎉")