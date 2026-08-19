# FuelPulse MY

## Malaysian Fuel Price Analytics Platform

FuelPulse MY is a data engineering and analytics project designed to process and analyse Malaysian retail fuel price data.

The platform demonstrates an end-to-end data pipeline covering data extraction, validation, transformation, cloud data warehousing, and analytical visualisation.

The processed data is stored in Snowflake and presented through an interactive Streamlit dashboard.

---

## Project Overview

The system processes Malaysian retail fuel price records and prepares them for analytical use.

The current dataset contains:

- **1,896 records**
- **474 unique dates**
- **3 fuel types**
- **3 regions**
- **0 null fuel prices**
- Data coverage from **30 March 2017 to 13 August 2026**

The dashboard provides historical price analysis, weekly price movements, market statistics, and data quality indicators.

---

## Architecture

```text
Data Source
     │
     ▼
Python Extraction
     │
     ▼
Data Validation
     │
     ▼
Data Transformation
     │
     ▼
Snowflake RAW Layer
     │
     ▼
Snowflake ANALYTICS Layer
     │
     ▼
Streamlit Dashboard