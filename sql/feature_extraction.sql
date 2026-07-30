WITH monthly_trends AS (
    SELECT 
        PatientID,
        reporting_month,
        Portal_Usage,
        Overall_Satisfaction,
        -- Window function calculating change in portal use over time
        Portal_Usage - LAG(Portal_Usage, 1, Portal_Usage) OVER (
            PARTITION BY PatientID 
            ORDER BY reporting_month
        ) AS portal_velocity
    FROM monthly_engagement
),

aggregated_metrics AS (
    SELECT 
        PatientID,
        AVG(Portal_Usage) AS avg_portal_usage,
        AVG(Overall_Satisfaction) AS avg_satisfaction,
        SUM(portal_velocity) AS net_portal_trend
    FROM monthly_trends
    GROUP BY PatientID
)

-- Final extraction view combining historical telemetry with static profiles
SELECT 
    p.PatientID,
    p.Age,
    p.Insurance_Type,
    p.Avg_Out_Of_Pocket_Cost,
    a.avg_portal_usage,
    a.avg_satisfaction,
    a.net_portal_trend,
    p.Churned AS target_label
FROM patient_profiles p
JOIN aggregated_metrics a ON p.PatientID = a.PatientID;
