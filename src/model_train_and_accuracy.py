# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1it6SuWAzzTW8DRmor_xrcXtnc425SJzp
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

# Ensure models directory exists
os.makedirs("models", exist_ok=True)

# Load dataset
df = pd.read_csv("k8s_with_anomalies.csv")

# Define failure conditions
def determine_failure(row):
    reasons = []
    if row["cpu_usage"] > 0.75:
        reasons.append("High CPU Usage")
    if row["memory_usage"] < 700000:  # Adjusted for your data context
        reasons.append("Low Memory")
    if row["pod_status_running"] == 0:
        reasons.append("Pod Failure")
    if row["network_rx"] == 0:
        reasons.append("Network Failure")
    return (1, ", ".join(reasons)) if reasons else (0, "Success")

# Apply labeling
df[["Failure", "Failure_Reason"]] = df.apply(determine_failure, axis=1, result_type="expand")

# Features and target
X = df[["cpu_usage", "memory_usage", "pod_status_running", "network_rx"]]
y = df["Failure"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate
y_pred = rf_model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the trained model to /models
model_path = "models/k8s-watchdog.pkl"
with open(model_path, "wb") as f:
    pickle.dump(rf_model, f)
print(f"Model saved to {model_path}")

# Prediction function (for reference)
def predict_failure(data):
    data = data.copy()
    data["Predicted_Failure"] = rf_model.predict(data)
    def get_failure_reason(row):
        reasons = []
        if row["cpu_usage"] > 0.75:
            reasons.append("High CPU Usage")
        if row["memory_usage"] < 700000:
            reasons.append("Low Memory")
        if row["pod_status_running"] == 0:
            reasons.append("Pod Failure")
        if row["network_rx"] == 0:
            reasons.append("Network Failure")
        return ", ".join(reasons) if reasons else "Success"
    data["Predicted_Reason"] = data.apply(get_failure_reason, axis=1)
    return data

# Test prediction
sample_data = X_test.head(10).copy()
predictions = predict_failure(sample_data)
print("\nSample Predictions:\n", predictions)
