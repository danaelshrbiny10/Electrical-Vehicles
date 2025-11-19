"""
EV Station Data Cleaning and City-Level Analysis

1. Clean and standardize city names.
2. Remove Unknown cities.
3. Normalize city names using fuzzy matching.
4. Calculate average distance between stations in each city.
5. Assign congestion status (crowded, medium, free) per city.
6. Save ONLY ONE final processed CSV.
"""

import pandas as pd
from rapidfuzz import process, fuzz
from geopy.distance import geodesic

df = pd.read_csv("/home/dana/code/Electrical-Vehicles/data/raw/ev_data_egypt.csv")

# Standard city replacements and Unknown removal.
city_map = {
    "Katameya": "Katameya",
    "Kattameya": "Katameya",
    "South Sainai": "South Sinai",
    "Ras Sudr": "Ras Sedr",
    "Alameen": "New Alamein",
    "Alamein": "New Alamein",
    "Sidi AbdelRahman": "Sidi Abdel Rahman",
    "Sidi Abdel Rahman": "Sidi Abdel Rahman",
    "New Capital": "New Administrative Capital",
    "Administrative Capital": "New Administrative Capital",
    "October": "6th of October",
    "October City": "6th of October",
    "10th Of Ramadan City": "10th of Ramadan",
    "Sokhna": "Ain Sokhna",
    "Down Town": "Downtown Cairo",
    "Masr El Gedida": "Heliopolis",
    "Madinet Nasr": "Nasr City",
    "Dukki": "Dokki",
    "Gouna": "El Gouna",
    "Somabay": "Soma Bay",
    "Behira": "Beheira",
    "Ismaillia": "Ismailia",
    "Ras El Hikma": "Ras El Hekma",
}

df["City"] = df["City"].replace(city_map)
df = df[df["City"].str.lower() != "unknown"]


# Normalize city names using fuzzy matching.
unique_cities = df["City"].dropna().unique().tolist()

def normalize_city(name, choices, threshold=85):
    match, score, _ = process.extractOne(
        name, choices, scorer=fuzz.token_sort_ratio
    )
    return match if score >= threshold else name

normalized_cities = {city: normalize_city(city, unique_cities) for city in unique_cities}
df["City"] = df["City"].map(normalized_cities)


# Compute average intra-city distance.
def city_avg_distance(city_df):
    coords = list(zip(city_df["Lat"], city_df["Lon"]))
    n = len(coords)
    if n < 2:
        return 0
    distances = [
        geodesic(coords[i], coords[j]).km
        for i in range(n)
        for j in range(i + 1, n)
    ]
    return sum(distances) / len(distances)

city_distances = df.groupby("City").apply(city_avg_distance).reset_index()
city_distances.columns = ["City", "Avg_Distance_km"]


# Congestion classification.
def congestion_status(avg_dist):
    if avg_dist < 1:
        return "Crowded"
    elif avg_dist <= 3:
        return "Medium"
    else:
        return "Free"

city_distances["Status"] = city_distances["Avg_Distance_km"].apply(congestion_status)
city_distances["Avg_Distance_km"] = city_distances["Avg_Distance_km"].round(2)


# Merge full result.
df = df.merge(city_distances, on="City", how="left")


# SAVE ONLY ONE FINAL CSV
df.to_csv(
    "/home/dana/code/Electrical-Vehicles/data/processed/city_status.csv",
    index=False,
)

print(df[["City", "Avg_Distance_km", "Status"]].drop_duplicates())
