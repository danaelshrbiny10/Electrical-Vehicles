#!/usr/bin/env python3
"""
Fetches electric vehicle charging station data from OpenChargeMap API
and stores it locally as a clean CSV file.
"""

import os
import requests
import pandas as pd
import logging
from pathlib import Path
from dotenv import load_dotenv
from models import ResponseSignal

# Load environment variables from .env file
load_dotenv()

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
API_URL = "https://api.openchargemap.io/v3/poi/"
MAX_RECORDS = 10000
COUNTRY_CODE = "ALL"
API_KEY = os.getenv("OPENCHARGEMAP_API_KEY")

DATA_RAW_DIR = Path("data/raw")

# ------------------------------------------------------------
# Logging setup
# ------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ------------------------------------------------------------
# Fetch data from API
# ------------------------------------------------------------
def fetch_openchargemap_data() -> pd.DataFrame:
    """Fetch and structure charging station data from OpenChargeMap API."""
    if not API_KEY:
        logging.error(ResponseSignal.ENV_MISSING.value)
        raise EnvironmentError("OPENCHARGEMAP_API_KEY not found in environment variables.")

    params = {
        "output": "json",
        "maxresults": MAX_RECORDS,
        "countrycode": COUNTRY_CODE,
        "key": API_KEY
    }

    headers = {
        "X-API-Key": API_KEY,
        "User-Agent": "ElectricVehiclesDataCollector/1.0"
    }

    logging.info(ResponseSignal.FETCHING.value)
    response = requests.get(API_URL, params=params, headers=headers)

    if response.status_code != 200:
        logging.error(f"{ResponseSignal.API_ERROR.value}: {response.status_code} - {response.text}")
        raise Exception(f"API request failed with status code {response.status_code}")

    data = response.json()
    if not data:
        logging.warning(ResponseSignal.NO_DATA.value)
        return pd.DataFrame()

    # Extract and clean relevant fields
    records = []
    for d in data:
        addr = d.get("AddressInfo", {})
        records.append({
            "Station_ID": d.get("ID"),
            "Station_Name": addr.get("Title"),
            "Address": addr.get("AddressLine1"),
            "City": addr.get("Town"),
            "State/Province": addr.get("StateOrProvince"),
            "Country": addr.get("Country", {}).get("Title") if addr.get("Country") else None,
            "Lat": round(addr.get("Latitude"), 5) if addr.get("Latitude") else None,
            "Lon": round(addr.get("Longitude"), 5) if addr.get("Longitude") else None,
            "Cost": d.get("UsageCost"),
            "Num_Connections": len(d.get("Connections", [])),
            "Last_Updated": d.get("DateLastStatusUpdate")
        })

    df = pd.DataFrame(records)

    # Convert and format date
    df["Last_Updated"] = pd.to_datetime(df["Last_Updated"], errors="coerce").dt.date

    logging.info(f"{ResponseSignal.SUCCESS.value}: Retrieved {len(df)} records.")
    return df


def save_data(df: pd.DataFrame):
    """Save cleaned data to CSV inside data/raw directory."""
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = DATA_RAW_DIR / "ev_data.csv"

    # Save as readable UTF-8 CSV
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    logging.info(f"{ResponseSignal.SAVED_LOCAL.value} at {csv_path}")
    print(f"Data successfully saved at: {csv_path}")


def main():
    try:
        df = fetch_openchargemap_data()
        if not df.empty:
            save_data(df)
        else:
            logging.warning(ResponseSignal.NO_DATA.value)
    except Exception as e:
        logging.error(f"{ResponseSignal.UNKNOWN_ERROR.value}: {e}")

if __name__ == "__main__":
    main()
