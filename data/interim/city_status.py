import pandas as pd
from rapidfuzz import process, fuzz
from geopy.distance import geodesic

# Load raw data
df = pd.read_csv("/home/dana/code/Electrical-Vehicles/data/raw/ev_data_egypt.csv")

# Drop rows with missing coordinates
df = df.dropna(subset=["Lat", "Lon"])

# Standard city replacements and Unknown removal
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

# Normalize city names
unique_cities = df["City"].dropna().unique().tolist()

def normalize_city(name, choices, threshold=85):
    match, score, _ = process.extractOne(name, choices, scorer=fuzz.token_sort_ratio)
    return match if score >= threshold else name

normalized_cities = {city: normalize_city(city, unique_cities) for city in unique_cities}
df["City"] = df["City"].map(normalized_cities)

# Fix Last_Updated column (parse to datetime, invalid → NaT)
df["Last_Updated"] = pd.to_datetime(df["Last_Updated"], errors="coerce")

# Optional: normalized string version (clean and consistent)
df["Last_Updated_Normalized"] = df["Last_Updated"].dt.strftime("%Y-%m-%d %H:%M:%S")

# Initialize new columns
df["Avg_Distance_km"] = 0.0
df["To_Station"] = ""

# Prepare all valid coordinates
all_coords = [(lat, lon, name, idx) for lat, lon, name, idx in zip(df["Lat"], df["Lon"], df["Station_Name"], df.index)]

# Compute distances
for city, city_df in df.groupby("City"):
    coords = [(lat, lon, name, idx) for lat, lon, name, idx in zip(city_df["Lat"], city_df["Lon"], city_df["Station_Name"], city_df.index)]
    
    for i, (lat1, lon1, name1, idx1) in enumerate(coords):

        if pd.isna(lat1) or pd.isna(lon1):
            continue
        
        distances = []
        nearest_station_name = None
        min_distance = None

        # Distances inside same city
        for j, (lat2, lon2, name2, idx2) in enumerate(coords):
            if i == j or pd.isna(lat2) or pd.isna(lon2):
                continue
            dist = geodesic((lat1, lon1), (lat2, lon2)).km
            distances.append(dist)
            if min_distance is None or dist < min_distance:
                min_distance = dist
                nearest_station_name = name2

        # If only 1 station in city → find nearest in other cities
        if not distances:
            other_stations = [
                (geodesic((lat1, lon1), (lat2, lon2)).km, name2)
                for lat2, lon2, name2, idx2 in all_coords
                if idx2 != idx1 and not pd.isna(lat2) and not pd.isna(lon2)
            ]
            if other_stations:
                min_distance, nearest_station_name = min(other_stations, key=lambda x: x[0])
                distances.append(min_distance)

        avg_distance = sum(distances)/len(distances) if distances else 0

        df.at[idx1, "Avg_Distance_km"] = round(avg_distance, 2)
        df.at[idx1, "To_Station"] = nearest_station_name

# Congestion classification
def congestion_status(dist):
    if dist < 1:
        return "Crowded"
    elif dist <= 3:
        return "Medium"
    else:
        return "Free"

df["Status"] = df["Avg_Distance_km"].apply(congestion_status)

# Save final CSV
df.to_csv("/home/dana/code/Electrical-Vehicles/data/processed/ev_data.csv", index=False)

print(df[["Station_Name", "Last_Updated", "Last_Updated_Normalized", "Avg_Distance_km", "To_Station", "Status"]].head(10))
