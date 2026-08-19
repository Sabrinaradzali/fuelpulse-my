import getpass
import snowflake.connector

print("Connecting to Snowflake...")

password = getpass.getpass("Enter your Snowflake password: ")

conn = snowflake.connector.connect(
    account="EAAUDHH-UR76724",
    user="SABRINARADZALI",
    password=password,
    authenticator="snowflake",
    role="ACCOUNTADMIN",
    warehouse="FUELPULSE_WH",
    database="FUELPULSE_MY",
    schema="RAW"
)

cursor = conn.cursor()

try:
    print("Connected to Snowflake successfully.")

    local_file = (
        r"C:\Users\user\Desktop\fuelpulse-my"
        r"\data\processed\fuel_prices_clean.csv"
    )

    # Convert Windows backslashes to forward slashes
    snowflake_file_path = local_file.replace("\\", "/")

    put_sql = f"""
    PUT 'file://{snowflake_file_path}'
    @FUELPULSE_MY.RAW.FUEL_PRICE_STAGE
    AUTO_COMPRESS=FALSE
    OVERWRITE=TRUE
    """

    print("Uploading fuel_prices_clean.csv...")

    cursor.execute(put_sql)

    print("Upload completed successfully.")

    print("\nFiles currently in Snowflake stage:")

    cursor.execute("""
        LIST @FUELPULSE_MY.RAW.FUEL_PRICE_STAGE
    """)

    for row in cursor.fetchall():
        print(row)

finally:
    cursor.close()
    conn.close()

print("\nDone.")