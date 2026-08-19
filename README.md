# FuelPulse MY

## Malaysian Fuel Price Data Engineering & Analytics Platform

FuelPulse MY is an end-to-end data engineering project designed to ingest, validate, transform, store, and analyse Malaysian retail fuel price data.

The platform combines Python-based data processing with Databricks and Snowflake to build a structured analytics pipeline. A Streamlit dashboard provides an interactive interface for analysing historical fuel prices, weekly price movements, market statistics, and data quality.

---

## Project Objectives

- Build an end-to-end data ingestion and transformation pipeline
- Process and validate Malaysian fuel price data
- Implement cloud-based data storage and analytics using Snowflake
- Automate data loading using Snowpipe
- Separate raw/staging data from analytics-ready data
- Calculate week-over-week fuel price changes
- Provide an interactive analytics dashboard
- Monitor basic data quality and pipeline status

---

## Architecture

```text
                    Data Sources
                         |
                         v
                  Python Extraction
                         |
                         v
              Data Cleaning & Validation
                         |
                         v
                    Databricks
                         |
                         v
                  Cloud Storage
                         |
                         v
                  Snowflake Stage
                         |
                         v
                     Snowpipe
                         |
                         v
                RAW / STAGING Layer
                         |
                         v
              Analytics Transformation
                         |
                         v
                ANALYTICS Layer
                         |
                         v
                Streamlit Dashboard
