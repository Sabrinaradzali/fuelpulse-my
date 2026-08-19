import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
import snowflake.connector


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="FuelPulse MY",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# ENTERPRISE-STYLE CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* Main application */
    .stApp {
        background-color: #f7f8fa;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Main content width */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    /* Header */
    .app-header {
        padding-bottom: 1.2rem;
        border-bottom: 1px solid #d9dde3;
        margin-bottom: 1.5rem;
    }

    .app-title {
        font-size: 28px;
        font-weight: 650;
        color: #172033;
        margin-bottom: 3px;
    }

    .app-subtitle {
        font-size: 14px;
        color: #667085;
    }

    /* Section titles */
    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #172033;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }

    /* KPI cards */
    .kpi-card {
        background: white;
        border: 1px solid #dfe3e8;
        border-radius: 6px;
        padding: 18px 20px;
        min-height: 125px;
    }

    .kpi-label {
        color: #667085;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 8px;
    }

    .kpi-value {
        color: #172033;
        font-size: 27px;
        font-weight: 650;
        margin-bottom: 6px;
    }

    .kpi-change {
        font-size: 13px;
        color: #667085;
    }

    /* Information boxes */
    .info-box {
        background: white;
        border: 1px solid #dfe3e8;
        border-radius: 6px;
        padding: 15px 18px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #dfe3e8;
    }

    /* Tables */
    div[data-testid="stDataFrame"] {
        border: 1px solid #dfe3e8;
        border-radius: 6px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# SNOWFLAKE CONNECTION
# ---------------------------------------------------------

@st.cache_resource
def get_connection():

    connection = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "FUELPULSE_WH"),
        database=os.getenv("SNOWFLAKE_DATABASE", "FUELPULSE_MY"),
        schema=os.getenv("SNOWFLAKE_SCHEMA", "ANALYTICS"),
        role=os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")
    )

    return connection


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data(ttl=300)
def load_fuel_data():

    conn = get_connection()

    query = """
        SELECT
            DATE,
            FUEL_TYPE,
            REGION,
            PRICE,
            WOW_CHANGE,
            WOW_CHANGE_PCT,
            SOURCE_UPDATED_AT,
            LOADED_AT
        FROM FUELPULSE_MY.ANALYTICS.FUEL_PRICES
        ORDER BY DATE
    """

    df = pd.read_sql(query, conn)

    df["DATE"] = pd.to_datetime(df["DATE"])

    return df


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="app-header">
        <div class="app-title">FuelPulse MY</div>
        <div class="app-subtitle">
            Malaysian Fuel Price Intelligence
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# LOAD DATA WITH ERROR HANDLING
# ---------------------------------------------------------

try:

    df = load_fuel_data()

except Exception as e:

    st.error(
        "Unable to retrieve data from Snowflake. "
        "Please verify the Snowflake connection and credentials."
    )

    st.code(str(e))

    st.stop()


# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------

st.sidebar.markdown("### Filters")

min_date = df["DATE"].min().date()
max_date = df["DATE"].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

fuel_options = sorted(df["FUEL_TYPE"].dropna().unique())

selected_fuels = st.sidebar.multiselect(
    "Fuel type",
    fuel_options,
    default=fuel_options
)

region_options = sorted(df["REGION"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Region",
    region_options,
    default=region_options
)


# ---------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------

filtered_df = df.copy()

if len(date_range) == 2:

    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])

    filtered_df = filtered_df[
        (filtered_df["DATE"] >= start_date)
        & (filtered_df["DATE"] <= end_date)
    ]

if selected_fuels:

    filtered_df = filtered_df[
        filtered_df["FUEL_TYPE"].isin(selected_fuels)
    ]

if selected_regions:

    filtered_df = filtered_df[
        filtered_df["REGION"].isin(selected_regions)
    ]


# ---------------------------------------------------------
# DATA STATUS
# ---------------------------------------------------------

latest_date = df["DATE"].max()

st.caption(
    f"Data through {latest_date.strftime('%d %B %Y')}  |  "
    f"Source: Snowflake analytics layer"
)


# ---------------------------------------------------------
# LATEST PRICES
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">Latest Fuel Prices</div>',
    unsafe_allow_html=True
)

latest = (
    df.sort_values("DATE")
    .groupby(["FUEL_TYPE", "REGION"], as_index=False)
    .tail(1)
)


# Select Malaysia-wide / relevant latest values
latest_fuel = (
    latest.sort_values("DATE")
    .groupby("FUEL_TYPE", as_index=False)
    .tail(1)
)


fuel_order = ["RON95", "RON97", "Diesel"]

cols = st.columns(3)

for i, fuel in enumerate(fuel_order):

    row = latest_fuel[
        latest_fuel["FUEL_TYPE"].str.upper() == fuel.upper()
    ]

    with cols[i]:

        if not row.empty:

            price = row.iloc[0]["PRICE"]
            change = row.iloc[0]["WOW_CHANGE"]

            if pd.isna(change):
                change_text = "No previous-week change available"
            else:
                sign = "+" if change > 0 else ""
                change_text = f"{sign}RM {change:.2f} WoW"

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">{fuel}</div>
                    <div class="kpi-value">RM {price:.2f}</div>
                    <div class="kpi-change">{change_text}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">{fuel}</div>
                    <div class="kpi-value">—</div>
                    <div class="kpi-change">No data available</div>
                </div>
                """,
                unsafe_allow_html=True
            )


# ---------------------------------------------------------
# PRICE TREND
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">Fuel Price Trend</div>',
    unsafe_allow_html=True
)

trend_df = (
    filtered_df
    .groupby(["DATE", "FUEL_TYPE"], as_index=False)["PRICE"]
    .mean()
)

fig = px.line(
    trend_df,
    x="DATE",
    y="PRICE",
    color="FUEL_TYPE",
    markers=False,
    labels={
        "DATE": "Date",
        "PRICE": "Price (RM/L)",
        "FUEL_TYPE": "Fuel Type"
    }
)

fig.update_layout(
    height=430,
    template="plotly_white",
    margin=dict(l=10, r=10, t=20, b=10),
    legend_title_text="",
    hovermode="x unified"
)

fig.update_yaxes(
    tickprefix="RM ",
    fixedrange=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------------------------------------------------
# WEEK-OVER-WEEK CHANGE
# ---------------------------------------------------------

left, right = st.columns(2)


with left:

    st.markdown(
        '<div class="section-title">Weekly Price Movement</div>',
        unsafe_allow_html=True
    )

    # Use the most recent 26 weeks for a clearer business view
    latest_wow_date = filtered_df["DATE"].max()

    wow_start_date = latest_wow_date - pd.Timedelta(weeks=26)

    change_df = (
        filtered_df[
            filtered_df["DATE"] >= wow_start_date
        ]
        .groupby(["DATE", "FUEL_TYPE"], as_index=False)["WOW_CHANGE"]
        .mean()
        .dropna(subset=["WOW_CHANGE"])
    )

    if not change_df.empty:

        change_fig = px.bar(
            change_df,
            x="DATE",
            y="WOW_CHANGE",
            color="FUEL_TYPE",
            barmode="group",
            labels={
                "DATE": "Date",
                "WOW_CHANGE": "Weekly Change (RM/L)",
                "FUEL_TYPE": "Fuel Type"
            }
        )

        change_fig.add_hline(
            y=0,
            line_width=1,
            line_dash="solid"
        )

        change_fig.update_layout(
            height=360,
            template="plotly_white",
            margin=dict(l=10, r=10, t=20, b=10),
            legend_title_text="",
            hovermode="x unified"
        )

        change_fig.update_yaxes(
            tickprefix="RM ",
            zeroline=False
        )

        st.plotly_chart(
            change_fig,
            use_container_width=True
        )

    else:

        st.info(
            "No weekly price movement data is available "
            "for the selected filters."
        )


with right:

    st.markdown(
        '<div class="section-title">Latest Market Overview</div>',
        unsafe_allow_html=True
    )

    if not filtered_df.empty:

        summary = (
            filtered_df
            .groupby("FUEL_TYPE")["PRICE"]
            .agg(
                Average="mean",
                Minimum="min",
                Maximum="max"
            )
            .reset_index()
        )

        summary["Average"] = summary["Average"].round(2)
        summary["Minimum"] = summary["Minimum"].round(2)
        summary["Maximum"] = summary["Maximum"].round(2)

        summary = summary.rename(
            columns={
                "FUEL_TYPE": "Fuel Type",
                "Average": "Avg. Price",
                "Minimum": "Min. Price",
                "Maximum": "Max. Price"
            }
        )

        st.dataframe(
            summary,
            hide_index=True,
            use_container_width=True
        )

    else:

        st.info("No data available for the selected filters.")


# ---------------------------------------------------------
# DATA QUALITY / PIPELINE STATUS
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">Data Quality & Pipeline Status</div>',
    unsafe_allow_html=True
)

total_rows = len(df)
unique_dates = df["DATE"].nunique()
null_prices = df["PRICE"].isna().sum()
fuel_types = df["FUEL_TYPE"].nunique()

q1, q2, q3, q4 = st.columns([1, 1.5, 1, 1])

with q1:
    st.metric(
        "Records",
        f"{total_rows:,}"
    )

with q2:
    st.markdown(
        """
        <div class="kpi-label">Data coverage</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="kpi-value" style="font-size: 22px; white-space: nowrap;">
            {min_date.strftime('%d %b %Y')} – {latest_date.strftime('%d %b %Y')}
        </div>
        """,
        unsafe_allow_html=True
    )

with q3:
    st.metric(
        "Fuel types",
        fuel_types
    )

with q4:
    st.metric(
        "Null prices",
        f"{null_prices:,}"
    )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
    <div style="
        margin-top: 35px;
        padding-top: 15px;
        border-top: 1px solid #d9dde3;
        color: #667085;
        font-size: 12px;
    ">
        FuelPulse MY · Data Engineering
        · Snowflake Analytics Layer
    </div>
    """,
    unsafe_allow_html=True
)