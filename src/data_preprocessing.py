import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from database_pipeline import build_database_pipeline

def run_preprocessing_pipeline(csv_path):
    """
    1. Extracts data from the SQLite DB pipeline.
    2. Encodes categorical vectors.
    3. Splits and scales datasets for ML injection.
    """
    # Pull data straight out of your SQL pipeline engine
    df = build_database_pipeline(csv_path)
    
    if df.empty:
        raise ValueError("❌ Extracted dataframe is empty. Check your database loading logs.")

    # Define features and our target variable (Churned)
    feature_cols = ['Age', 'Insurance_Type', 'Avg_Out_Of_Pocket_Cost', 
                    'avg_portal_usage', 'avg_satisfaction', 'net_portal_trend']
    target_col = 'target_label'
    
    X = df[feature_cols]
    y = df[target_col]
    
    # 1. One-Hot Encode categorical strings (e.g., Insurance_Type -> Basic, Premium, etc.)
    X = pd.get_dummies(X, columns=['Insurance_Type'], drop_first=True)
    
    # Save feature names before converting to pure mathematical NumPy arrays
    feature_names = X.columns.tolist()
    
    # 2. Mathematical Train/Test Isolation (Stratified to maintain class balance)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 3. Normalise features to have zero mean and unit variance (Essential for Logistic Regression)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"📐 Preprocessing complete. Training shapes: {X_train_scaled.shape}, Test shapes: {X_test_scaled.shape}")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, feature_names

if __name__ == "__main__":
    # Test your preprocessing pipeline independently
    csv_path = "data/raw/patient_churn_dataset.csv"
    run_preprocessing_pipeline(csv_path)
