import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
from dateutil.parser import parse

# Load environment variables
load_dotenv()

# PostgreSQL connection
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    dbname=os.getenv("DB_NAME")
)
cursor = conn.cursor()

# Integer converter
def to_int(val):
    try: return int(str(val).replace(",", "").strip())
    except: return None

# Robust date parser that handles all formats
def to_date(val):
    try:
        if pd.isnull(val) or str(val).strip() == "":
            return None
        return parse(str(val), dayfirst=True).date()  # Handles 27-11-2024 & 2024-11-27
    except Exception as e:
        print(f"⚠️ Date parse failed for '{val}': {e}")
        return None

# Drop and create a clean final table
cursor.execute('DROP TABLE IF EXISTS customer_data_final_cleaned;')
cursor.execute("""
    CREATE TABLE customer_data_final_cleaned (
        id SERIAL PRIMARY KEY,
        customer_id TEXT,
        product TEXT,
        quantity INTEGER,
        unit_price INTEGER,
        total_price INTEGER,
        purchase_date DATE,
        customer_name TEXT,
        industry TEXT,
        annual_revenue BIGINT,
        num_employees INTEGER,
        customer_priority TEXT,
        rating TEXT,
        account_type TEXT,
        location TEXT,
        current_products TEXT,
        product_usage_percent INTEGER,
        cross_sell_synergy TEXT,
        last_activity_date DATE,
        opportunity_stage TEXT,
        opportunity_amount BIGINT,
        opportunity_type TEXT,
        competitors TEXT,
        activity_status TEXT,
        activity_priority TEXT,
        activity_type TEXT,
        product_sku TEXT
    );
""")

# Rename map matching original Excel headers
rename_map = {
    "Customer ID": "customer_id",
    "Product": "product",
    "Quantity": "quantity",
    "Unit Price (USD)": "unit_price",
    "Total Price (USD)": "total_price",
    "Purchase Date": "purchase_date",
    "Customer Name": "customer_name",
    "Industry": "industry",
    "Annual Revenue (USD)": "annual_revenue",
    "Number of Employees": "num_employees",
    "Customer Priority": "customer_priority",
    "Rating": "rating",
    "Account Type": "account_type",
    "Location": "location",
    "Current Products": "current_products",
    "Product Usage (%)": "product_usage_percent",
    "Cross-Sell Synergy": "cross_sell_synergy",
    "Last Activity Date": "last_activity_date",
    "Opportunity Stage": "opportunity_stage",
    "Opportunity Amount (USD)": "opportunity_amount",
    "Opportunity Type": "opportunity_type",
    "Competitors": "competitors",
    "Activity Status": "activity_status",
    "Activity Priority": "activity_priority",
    "Activity Type": "activity_type",
    "Product SKU": "product_sku"
}

# Insert cleaned rows
def extract_data(excel_path):
    df = pd.read_excel(excel_path)
    print("📊 Columns from Excel:", df.columns.tolist())
    print("📦 Rows loaded:", len(df))

    df.rename(columns=rename_map, inplace=True)

    inserted = 0
    for idx, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO customer_data_final_cleaned (
                    customer_id, product, quantity, unit_price, total_price, purchase_date,
                    customer_name, industry, annual_revenue, num_employees, customer_priority,
                    rating, account_type, location, current_products, product_usage_percent,
                    cross_sell_synergy, last_activity_date, opportunity_stage, opportunity_amount,
                    opportunity_type, competitors, activity_status, activity_priority, activity_type, product_sku
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, [
                row.get("customer_id"), row.get("product"), to_int(row.get("quantity")), to_int(row.get("unit_price")),
                to_int(row.get("total_price")), to_date(row.get("purchase_date")), row.get("customer_name"), row.get("industry"),
                to_int(row.get("annual_revenue")), to_int(row.get("num_employees")), row.get("customer_priority"),
                row.get("rating"), row.get("account_type"), row.get("location"), row.get("current_products"),
                to_int(row.get("product_usage_percent")), row.get("cross_sell_synergy"), to_date(row.get("last_activity_date")),
                row.get("opportunity_stage"), to_int(row.get("opportunity_amount")), row.get("opportunity_type"),
                row.get("competitors"), row.get("activity_status"), row.get("activity_priority"),
                row.get("activity_type"), row.get("product_sku")
            ])
            inserted += 1
        except Exception as e:
            print(f"❌ Insert error on row {idx + 1}: {e}")

    conn.commit()
    print(f"✅ Inserted {inserted} rows into customer_data_final_cleaned.")

# Entry point
if __name__ == "__main__":
    extract_data("C:/Harsh/Desktop/langgraph/data for assignemnt.xlsx")
