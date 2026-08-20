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

Technology Stack
Component	Technology
Data Extraction	Python
Data Processing	Python, Pandas
Data Validation	Python
Data Warehouse	Snowflake
Dashboard	Streamlit
Visualisation	Plotly
Environment Management	Python virtual environment
Version Control	Git, GitHub
Project Structure
fuelpulse-my/
│
├── dashboard/
│   └── app.py
│
├── src/
│   ├── extract_fuel_prices.py
│   ├── inspect_fuel_prices.py
│   ├── transform_fuel_prices.py
│   └── validate_fuel_prices.py
│
├── databricks/
├── snowflake/
├── docs/
├── data/
│
├── upload_to_snowflake.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
Data Pipeline
1. Data Extraction

Fuel price data is collected and prepared for downstream processing using Python.

2. Data Validation

The pipeline performs checks on the dataset before loading it into the warehouse. This helps identify missing values, invalid records, and potential data quality issues.

3. Data Transformation

The validated data is transformed into a consistent structure suitable for analytical queries and reporting.

4. Snowflake Data Warehouse

Processed data is loaded into Snowflake and organised into separate layers:

RAW Layer – stores ingested data
ANALYTICS Layer – provides structured data for analysis
5. Dashboard

The Streamlit dashboard connects to the analytical layer and provides interactive views of Malaysian fuel price trends and market statistics.

Dashboard

The dashboard includes:

Latest Fuel Prices

Displays the latest available prices for:

RON95
RON97
Diesel
Fuel Price Trend

Shows historical price movements across the available dataset.

Weekly Price Movement

Highlights week-over-week changes in fuel prices.

Market Overview

Provides average, minimum, and maximum prices by fuel type.

Data Quality & Pipeline Status

Displays key data quality indicators including:

Total records
Data coverage
Number of fuel types
Null price count
Running the Dashboard
1. Clone the repository
git clone https://github.com/Sabrinaradzali/fuelpulse-my.git
cd fuelpulse-my
2. Create a virtual environment
python -m venv .venv

Activate it on Windows:

.venv\Scripts\Activate.ps1
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a .env file based on .env.example and provide the required Snowflake connection details.

Do not commit .env or private credentials to GitHub.

5. Run the dashboard
streamlit run dashboard/app.py

The application will open locally at:

http://localhost:8501
Data Quality

The current analytical dataset reports:

Metric	Value
Records	1,896
Unique Dates	474
Fuel Types	3
Regions	3
Null Prices	0
Data Coverage	30 Mar 2017 – 13 Aug 2026

These metrics are also surfaced directly in the dashboard.

Project Focus

This project focuses on the practical implementation of a small-scale data engineering workflow, including:

Data ingestion
Data validation
Data transformation
Cloud data warehousing
Analytical data modelling
Dashboard development
Data quality monitoring
Reproducible project structure
Status

Project Status: Completed

The current version includes the data pipeline, Snowflake integration, analytical layer, and Streamlit dashboard.

Author

Nur Sabrina Radzali

Bachelor of Computer and Communication Systems Engineering
Universiti Putra Malaysia

GitHub: https://github.com/Sabrinaradzali
