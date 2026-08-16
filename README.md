# FuelPulse MY

A data engineering project for analysing Malaysian retail fuel prices and global crude oil prices.

## Overview

FuelPulse MY is a data pipeline that collects Malaysian fuel price data from data.gov.my and combines it with global crude oil price data.

The project focuses on preparing, transforming, storing, and analysing pricing data using Databricks and Snowflake.

The analysis includes fuel price trends, week-over-week price changes, rolling volatility, and data freshness.

## Technologies

- Python
- SQL
- Databricks
- Snowflake
- Snowpipe
- Snowflake Streams and Tasks
- Streamlit
- GitHub

## Data Sources

- Malaysian retail fuel prices — data.gov.my
- Global crude oil prices — [source to be added]

## Pipeline

```text
Data Sources
     ↓
Databricks
     ↓
Data Cleaning and Transformation
     ↓
Cloud Storage
     ↓
Snowflake Snowpipe
     ↓
Snowflake Staging
     ↓
Streams and Tasks
     ↓
Analytics Tables
     ↓
Streamlit Dashboard
