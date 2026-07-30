import sqlite3
import pandas as pd
import os
from src.database_pipeline import build_database_pipeline

def run_local_validation():
    print("🔬 STARTING LOCAL DATABASE VERIFICATION 🔬\n" + "="*40)
    
    # 1. Verify SQL scripts exist
    schema_exists = os.path.exists("sql/schema.sql")
    extract_exists = os.path.exists("sql/feature_extraction.sql")
    print(f"📄 Checked sql/schema.sql: {'FOUND' if schema_exists else 'MISSING ❌'}")
    print(f"📄 Checked sql/feature_extraction.sql: {'FOUND' if extract_exists else 'MISSING ❌'}")
    
    if not (schema_exists and extract_exists):
        print("❌ Error: Please ensure your SQL files are created before running.")
        return

    # 2. Check for Kaggle CSV file
    target_csv = "data/raw/patient_churn_dataset.csv"  # <-- Change this to your exact filename if different
    csv_exists = os.path.exists(target_csv)
    print(f"📊 Checking for Kaggle raw dataset at '{target_csv}': {'FOUND' if csv_exists else 'NOT FOUND (Using sandbox dataset) ⚠️'}")

    # 3. Handle data loading mechanism
    if not csv_exists:
        print("\n🛠️ Creating sandbox verification data since your raw CSV isn't hooked up yet...")
        conn = sqlite3.connect("health_analytics.db")
        cursor = conn.cursor()
        
        # Execute basic initialization
        with open("sql/schema.sql", "r") as f:
            cursor.executescript(f.read())
            
        # Inject precise validation inputs matching your SQL syntax requirements
        cursor.execute("INSERT INTO patient_profiles VALUES ('P001', 34, '2023-01-01', 'Premium', 50.0, 0)")
        cursor.execute("INSERT INTO patient_profiles VALUES ('P002', 45, '2023-02-15', 'Basic', 30.0, 1)")
        cursor.execute("INSERT INTO monthly_engagement VALUES (1, 'P001', '2023-03-01', 5, 1, 0, 1)")
        cursor.execute("INSERT INTO monthly_engagement VALUES (2, 'P001', '2023-04-01', 8, 2, 1, 0)")
        cursor.execute("INSERT INTO monthly_engagement VALUES (3, 'P002', '2023-03-01', 2, 0, 2, 4)")
        cursor.execute("INSERT INTO monthly_engagement VALUES (4, 'P002', '2023-04-01', 1, 0, 1, 5)")
        
        conn.commit()
        conn.close()

    # 4. Trigger database feature engine extraction
    try:
        df = build_database_pipeline(target_csv)
        print("\n" + "="*40 + "\n✅ SUCCESS: SQL Window Functions Executed Flawlessly!")
        print(f"📊 Feature matrix shape: {df.shape[0]} rows by {df.shape[1]} columns.\n")
        print("👀 Extracted data preview:")
        print(df.to_string(index=False))
    except Exception as e:
        print(f"\n❌ PIPELINE ERROR ENCOUNTERED:\n{str(e)}")

if __name__ == "__main__":
    run_local_validation()
