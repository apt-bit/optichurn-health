import sqlite3
import pandas as pd
import os

DB_PATH = "health_analytics.db"

def run_sql_script(cursor, script_path):
    with open(script_path, 'r') as f:
        cursor.executescript(f.read())
    print(f"✔️ Successfully executed: {script_path}")

def build_database_pipeline(raw_csv_path):
    print("🚀 Initialising enterprise SQLite database pipeline...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Rebuild clean schema
    run_sql_script(cursor, "sql/schema.sql")
    
    if os.path.exists(raw_csv_path):
        raw_df = pd.read_csv(raw_csv_path)
        print(f"📥 Found Kaggle data with {len(raw_df)} records.")
        
        # 2. Extract and load Patient Profiles
        profile_cols = ['PatientID', 'Age', 'Gender', 'State', 'Insurance_Type', 'Avg_Out_Of_Pocket_Cost', 'Churned']
        profiles_df = raw_df[profile_cols].drop_duplicates()
        profiles_df.to_sql("patient_profiles", conn, if_exists="append", index=False)
        print(f"✔️ Successfully loaded {len(profiles_df)} unique patient profiles.")
        
        # 3. Simulate a 3-month relational history to populate the SQL window functions
        print("🛠️ Simulating relational monthly timeline metrics from flat file...")
        monthly_records = []
        for index, row in raw_df.iterrows():
            # Month 1: Baseline behavior
            monthly_records.append((row['PatientID'], '2026-05-01', row['Visits_Last_Year']//3, row['Missed_Appointments'], max(0, row['Portal_Usage']-2), row['Overall_Satisfaction']))
            # Month 2: Midpoint behavior
            monthly_records.append((row['PatientID'], '2026-06-01', row['Visits_Last_Year']//3, 0, row['Portal_Usage'], row['Overall_Satisfaction']))
            # Month 3: Current behavior
            monthly_records.append((row['PatientID'], '2026-07-01', row['Visits_Last_Year']//3, row['Missed_Appointments'], row['Portal_Usage'], row['Overall_Satisfaction']))
            
        engagement_df = pd.DataFrame(monthly_records, columns=['PatientID', 'reporting_month', 'Visits_Last_Year', 'Missed_Appointments', 'Portal_Usage', 'Overall_Satisfaction'])
        engagement_df.to_sql("monthly_engagement", conn, if_exists="append", index=False)
        print(f"✔️ Successfully loaded {len(engagement_df)} monthly tracking records.")
        conn.commit()
    else:
        print(f"❌ Critical Error: Raw CSV not found at {raw_csv_path}.")
        conn.close()
        return pd.DataFrame()

    # 4. Extract final feature matrix via window functions
    print("📊 Extracting feature matrix via SQL Window functions...")
    with open("sql/feature_extraction.sql", 'r') as f:
        extraction_query = f.read()
        
    final_feature_df = pd.read_sql_query(extraction_query, conn)
    conn.close()
    
    print(f"🏁 Pipeline complete. Extracted matrix shape: {final_feature_df.shape}")
    return final_feature_df
