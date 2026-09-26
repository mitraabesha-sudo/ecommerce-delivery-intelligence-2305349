import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="E-Commerce Delivery Intelligence",
    page_icon="📦",
    layout="wide"
)

# Snowflake Connection
@st.cache_resource
def get_connection():
    return st.connection("snowflake")


conn = get_connection()

# Load Data

@st.cache_data(ttl=600)
def load_data():

    executive = conn.query("""
        SELECT *
        FROM ECOMMERCE_2305349.GOLD.EXECUTIVE_KPIS
    """)

    monthly = conn.query("""
        SELECT *
        FROM ECOMMERCE_2305349.GOLD.MONTHLY_DELIVERY
        ORDER BY 1
    """)

    seller = conn.query("""
        SELECT *
        FROM ECOMMERCE_2305349.GOLD.SELLER_PERFORMANCE
        ORDER BY 1
    """)

    category = conn.query("""
        SELECT *
        FROM ECOMMERCE_2305349.GOLD.CATEGORY_PERFORMANCE
        ORDER BY 1
    """)

    cancellation = conn.query("""
        SELECT *
        FROM ECOMMERCE_2305349.GOLD.CANCELLATION_INTELLIGENCE
        ORDER BY 1
    """)

    return executive, monthly, seller, category, cancellation

# Connect

try:

    executive, monthly, seller, category, cancellation = load_data()

except Exception as e:

    st.error("Unable to connect to Snowflake.")
    st.exception(e)
    st.stop()

# Header

st.title("📦 E-Commerce Delivery Intelligence")

st.markdown(
    """
    ### End-to-End Databricks + Snowflake Analytics Pipeline

    Interactive business intelligence dashboard for analyzing
    e-commerce delivery performance, seller efficiency,
    category performance, revenue and cancellation trends.
    """
)

st.divider()

# Executive KPIs

st.header("📊 Executive Overview")

if len(executive) > 0:

    kpi = executive.iloc[0]

    kpi_data = {
        col.lower(): kpi[col]
        for col in executive.columns
    }

    def get_value(name, default=0):
        return kpi_data.get(name.lower(), default)

    total_orders = get_value("total_orders")
    delivered_orders = get_value("delivered_orders")
    cancelled_orders = get_value("cancelled_orders")
    on_time_orders = get_value("on_time_orders")
    late_orders = get_value("late_orders")
    avg_delivery_days = get_value("avg_delivery_days")
    avg_order_value = get_value("avg_order_value")
    on_time_rate = get_value("on_time_delivery_rate")
    cancellation_rate = get_value("cancellation_rate")
    total_revenue = get_value("total_revenue")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Total Orders",
        f"{total_orders:,.0f}"
    )

    c2.metric(
        "Delivered",
        f"{delivered_orders:,.0f}"
    )

    c3.metric(
        "Cancelled",
        f"{cancelled_orders:,.0f}"
    )

    c4.metric(
        "On-Time Rate",
        f"{on_time_rate:.2f}%"
    )

    c5.metric(
        "Late Deliveries",
        f"{late_orders:,.0f}"
    )

    c6, c7, c8, c9, c10 = st.columns(5)

    c6.metric(
        "Avg Delivery Days",
        f"{avg_delivery_days:.2f}"
    )

    c7.metric(
        "Avg Order Value",
        f"${avg_order_value:,.2f}"
    )

    c8.metric(
        "Cancellation Rate",
        f"{cancellation_rate:.2f}%"
    )

    c9.metric(
        "Total Revenue",
        f"${total_revenue:,.2f}"
    )

    c10.metric(
        "On-Time Orders",
        f"{on_time_orders:,.0f}"
    )


st.divider()

# Monthly Delivery

st.header("📈 Monthly Delivery Performance")

st.dataframe(
    monthly,
    use_container_width=True,
    hide_index=True
)

numeric_columns = monthly.select_dtypes(
    include="number"
).columns.tolist()

chart_columns = []

for col in numeric_columns:

    col_lower = col.lower()

    if (
        "total" in col_lower
        or "deliver" in col_lower
        or "cancel" in col_lower
    ):
        chart_columns.append(col)


if chart_columns:

    st.subheader("Monthly Order Trends")

    st.line_chart(
        monthly.set_index(monthly.columns[0])[chart_columns]
    )


st.divider()

# Seller Performance
st.header("🚚 Seller Performance")

if len(seller) > 0:

    seller_rate_columns = [
        col for col in seller.columns
        if "rate" in col.lower()
    ]

    if seller_rate_columns:

        rate_col = seller_rate_columns[0]

        top_sellers = seller.sort_values(
            rate_col,
            ascending=False
        ).head(10)

        st.subheader(
            "Top Sellers by On-Time Delivery Rate"
        )

        st.bar_chart(
            top_sellers.set_index(
                seller.columns[0]
            )[rate_col]
        )

    st.subheader("Seller Performance Details")

    st.dataframe(
        seller,
        use_container_width=True,
        hide_index=True
    )


st.divider()

# Category Performance

st.header("🛍️ Category Performance")

if len(category) > 0:

    st.dataframe(
        category,
        use_container_width=True,
        hide_index=True
    )

    category_numeric = category.select_dtypes(
        include="number"
    ).columns.tolist()

    if category_numeric:

        selected_metric = st.selectbox(
            "Select category metric",
            category_numeric
        )

        st.bar_chart(
            category.set_index(
                category.columns[0]
            )[selected_metric]
        )


st.divider()

# Cancellation Intelligence
st.header("❌ Cancellation Intelligence")

if len(cancellation) > 0:

    st.dataframe(
        cancellation,
        use_container_width=True,
        hide_index=True
    )

    cancellation_numeric = cancellation.select_dtypes(
        include="number"
    ).columns.tolist()

    if cancellation_numeric:

        selected_cancel_metric = st.selectbox(
            "Select cancellation metric",
            cancellation_numeric
        )

        st.line_chart(
            cancellation.set_index(
                cancellation.columns[0]
            )[selected_cancel_metric]
        )


st.divider()

# Architecture

st.header("🏗️ Project Architecture")

st.code(
    """
Raw E-Commerce Data
        ↓
Databricks Raw Layer
        ↓
Bronze Layer
        ↓
Silver Layer
        ↓
Gold Analytics Layer
        ↓
Snowflake GOLD Schema
        ↓
Interactive Streamlit Dashboard
""",
    language="text"
)


st.caption(
    "E-Commerce Delivery Intelligence | "
    "Databricks + Snowflake | Project ID: 2305349"
)




