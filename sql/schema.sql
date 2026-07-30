PRAGMA foreign_keys = OFF;
DROP TABLE IF EXISTS monthly_engagement;
DROP TABLE IF EXISTS patient_profiles;
PRAGMA foreign_keys = ON;

-- 1. Core Patient Profile Table
CREATE TABLE patient_profiles (
    PatientID VARCHAR(50) PRIMARY KEY,
    Age INTEGER NOT NULL,
    Gender VARCHAR(20),
    State VARCHAR(20),
    Insurance_Type VARCHAR(50),
    Avg_Out_Of_Pocket_Cost REAL,
    Churned INTEGER DEFAULT 0  -- 0 = Active, 1 = Churned
);

-- 2. Monthly Engagement & Activity Tracker
CREATE TABLE monthly_engagement (
    engagement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    PatientID VARCHAR(50),
    reporting_month DATE NOT NULL,
    Visits_Last_Year INTEGER,
    Missed_Appointments INTEGER,
    Portal_Usage INTEGER,
    Overall_Satisfaction INTEGER,
    FOREIGN KEY (PatientID) REFERENCES patient_profiles(PatientID) ON DELETE CASCADE
);
