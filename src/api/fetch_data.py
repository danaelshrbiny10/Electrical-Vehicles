#!/usr/bin/env python3
"""
Fetches electric vehicle charging station data from the OpenChargeMap API
using pagination, and stores it locally as a clean CSV file.

By default, fetches up to 50,000 records safely (lightweight mode).
You can enable full-data mode (~1.2M+ records) by uncommenting the marked line below.
"""

import os
import requests
import pandas as pd
import logging
from pathlib import Path
from dotenv import load_dotenv
from ..models import ResponseSignal

# ------------------------------------------------------------
# Load environment variables
# ------------------------------------------------------------
load_dotenv()

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
API_URL = "https://api.openchargemap.io/v3/poi/"
PAGE_SIZE = 10000  # Number of records per API page
MAX_RECORDS = 50000
COUNTRY_CODE = "ALL"
API_KEY = os.getenv("OPENCHARGEMAP_API_KEY")

DATA_RAW_DIR = Path("data/raw")

# ------------------------------------------------------------
# Logging setup
# ------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# ------------------------------------------------------------
# Fetch data with pagination
# ------------------------------------------------------------
def fetch_openchargemap_data() -> pd.DataFrame:
    """Fetch and structure charging station data from OpenChargeMap API with pagination."""
    if not API_KEY:
        logging.error(ResponseSignal.ENV_MISSING.value)
        raise EnvironmentError(
            "OPENCHARGEMAP_API_KEY not found in environment variables."
        )

    headers = {
        "X-API-Key": API_KEY,
        "User-Agent": "ElectricVehiclesDataCollector/1.0",
    }

    all_records = []
    offset = 0

    logging.info(ResponseSignal.FETCHING.value)
    while offset < MAX_RECORDS:
        params = {
            "output": "json",
            "maxresults": PAGE_SIZE,
            "offset": offset,
            "countrycode": COUNTRY_CODE,
            "key": API_KEY,
        }

        response = requests.get(API_URL, params=params, headers=headers)
        if response.status_code != 200:
            logging.error(
                f"{ResponseSignal.API_ERROR.value}: {response.status_code} - {response.text}"
            )
            break

        data = response.json()
        if not data:
            logging.warning("No more data available from API.")
            break

        for d in data:
            addr = d.get("AddressInfo", {})
            all_records.append(
                {
                    "Station_ID": d.get("ID"),
                    "Station_Name": addr.get("Title"),
                    "Address": addr.get("AddressLine1"),
                    "City": addr.get("Town"),
                    "State/Province": addr.get("StateOrProvince"),
                    "Country": (
                        addr.get("Country", {}).get("Title")
                        if addr.get("Country")
                        else None
                    ),
                    "Lat": (
                        round(addr.get("Latitude"), 5) if addr.get("Latitude") else None
                    ),
                    "Lon": (
                        round(addr.get("Longitude"), 5)
                        if addr.get("Longitude")
                        else None
                    ),
                    "Cost": d.get("UsageCost"),
                    "Num_Connections": len(d.get("Connections", [])),
                    "Last_Updated": d.get("DateLastStatusUpdate"),
                }
            )

        offset += PAGE_SIZE
        logging.info(f"Fetched {len(all_records)} records so far...")

        if len(all_records) >= MAX_RECORDS:
            logging.info("Reached maximum record limit.")
            break

    df = pd.DataFrame(all_records)

    # Convert and format date column
    df["Last_Updated"] = pd.to_datetime(df["Last_Updated"], errors="coerce").dt.date

    logging.info(f"{ResponseSignal.SUCCESS.value}: Retrieved {len(df)} total records.")
    return df


# ------------------------------------------------------------
# Save data
# ------------------------------------------------------------
def save_data(df: pd.DataFrame):
    """Save cleaned data to CSV inside data/raw directory."""
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = DATA_RAW_DIR / "ev_data.csv"

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
