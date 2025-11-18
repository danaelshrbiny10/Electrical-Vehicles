#!/usr/bin/env python3
"""
Clean EV dataset for Egypt — adds average distance and crowdedness columns.
"""

import pandas as pd
import numpy as np
from math import radians, sin, cos, acos

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
INPUT_FILE = "/home/dana/code/Electrical-Vehicles/data/raw/ev_data_egypt.csv"
OUTPUT_FILE = "/home/dana/code/Electrical-Vehicles/data/processed/ev_data_egypt_with_distance.csv"

# ------------------------------------------------------------
# Load dataset
# ------------------------------------------------------------
print("📂 Loading data...")
df = pd.read_csv(INPUT_FILE)

# Drop rows with missing coordinates
df = df.dropna(subset=["Lat", "Lon"])

# ------------------------------------------------------------
# Compute average latitude and longitude
# ------------------------------------------------------------
avg_lat = df["Lat"].mean()
avg_lon = df["Lon"].mean()

# ------------------------------------------------------------
# Define distance function (Haversine formula)
# ------------------------------------------------------------
def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in km between two coordinates using spherical law of cosines."""
    return 6371 * acos(
        sin(radians(lat1)) * sin(radians(lat2)) +
        cos(radians(lat1)) * cos(radians(lat2)) *
        cos(radians(lon2) - radians(lon1))
    )

# ------------------------------------------------------------
# Compute average distance for each station
# ------------------------------------------------------------
print("Calculating distances...")
df["Avg_Distance_km"] = df.apply(
    lambda row: haversine_distance(row["Lat"], row["Lon"], avg_lat, avg_lon), axis=1
)

# ------------------------------------------------------------
# Determine crowdedness based on distance thresholds
# ------------------------------------------------------------
avg_distance = df["Avg_Distance_km"].mean()

def classify_crowd(d):
    if d < avg_distance * 0.8:
        return "🟥 Crowded"
    elif d < avg_distance * 1.2:
        return "🟨 Medium"
    else:
        return "🟩 Free"

df["Crowded_Status"] = df["Avg_Distance_km"].apply(classify_crowd)

# ------------------------------------------------------------
# Save cleaned data
# ------------------------------------------------------------
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
print(f"File saved as: {OUTPUT_FILE}")
print(f"Total records processed: {len(df)}")
