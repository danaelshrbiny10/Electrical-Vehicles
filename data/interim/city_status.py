"""
EV Station Data Cleaning and City-Level Analysis

1. Normalize city names using fuzzy matching.
2. Calculate average distance between stations in each city.
3. Assign congestion status (crowded, medium, free) per city.
"""

import pandas as pd
from rapidfuzz import process, fuzz
from geopy.distance import geodesic

# Load raw dataset
df = pd.read_csv("/home/dana/code/Electrical-Vehicles/data/raw/ev_data_egypt.csv")

"""
Normalize city names using fuzzy matching.
"""
unique_cities = df["City"].dropna().unique().tolist()


def normalize_city(name, choices, threshold=80):
    """
    Matches a city name to the closest standard name from choices using fuzzy matching.
    threshold: minimum similarity to consider as a match (0-100)
    """
    match, score, _ = process.extractOne(name, choices, scorer=fuzz.token_sort_ratio)
    return match if score >= threshold else name


normalized_cities = {
    city: normalize_city(city, unique_cities) for city in unique_cities
}
df["City"] = df["City"].map(normalized_cities)

# Save intermediate cleaned city dataset
df.to_csv(
    "/home/dana/code/Electrical-Vehicles/data/processed/stations_cleaned.csv",
    index=False,
)

"""
Calculate average distance between stations in each city and assign congestion status.
"""


def city_avg_distance(city_df):
    """
    Calculates the average geodesic distance between all stations in a city.
    """
    coords = list(zip(city_df["Lat"], city_df["Lon"]))
    n = len(coords)
    if n < 2:
        return 0
    distances = [
        geodesic(coords[i], coords[j]).km for i in range(n) for j in range(i + 1, n)
    ]
    return sum(distances) / len(distances)


city_distances = df.groupby("City").apply(city_avg_distance).reset_index()
city_distances.columns = ["City", "Avg_Distance_km"]


def congestion_status(avg_dist):
    """
    Assigns congestion status based on average distance.
    """
    if avg_dist < 1:
        return "🟥 Crowded"
    elif avg_dist <= 3:
        return "🟨 Medium"
    else:
        return "🟩 Free"


city_distances["Status"] = city_distances["Avg_Distance_km"].apply(congestion_status)
city_distances["Avg_Distance_km"] = city_distances["Avg_Distance_km"].round(2)

df = df.merge(city_distances, on="City", how="left")

# Save final dataset for visualization
df.to_csv(
    "/home/dana/code/Electrical-Vehicles/data/processed/stations_with_city_status.csv",
    index=False,
)
# Display city-level status
print(df[["City", "Avg_Distance_km", "Status"]].drop_duplicates())
