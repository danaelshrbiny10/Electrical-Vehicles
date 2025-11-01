#!/usr/bin/env python3
"""
Fetches all electric vehicle charging station data from the OpenChargeMap API
(using unlimited pagination) for Egypt and saves the raw data as a CSV file.
"""

import os
import requests
import pandas as pd
import logging
from pathlib import Path
from dotenv import load_dotenv
from time import sleep
from ..models import ResponseSignal

# ------------------------------------------------------------
# Load environment variables
# ------------------------------------------------------------
load_dotenv()

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
API_URL = "https://api.openchargemap.io/v3/poi/"
PAGE_SIZE = 10000  # Max per API page
COUNTRY_CODE = "EG"  # ISO code for Egypt
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
# Fetch data
# ------------------------------------------------------------
def fetch_openchargemap_data() -> pd.DataFrame:
    """Fetch *all* raw charging station data for Egypt from OpenChargeMap API."""
    if not API_KEY:
        logging.error(ResponseSignal.ENV_MISSING.value)
        raise EnvironmentError(
            "OPENCHARGEMAP_API_KEY not found in environment variables."
        )

    headers = {
        "X-API-Key": API_KEY,
        "User-Agent": "ElectricVehiclesDataCollector/Raw/1.0",
    }

    all_records = []
    offset = 0
    total_fetched = 0

    logging.info(f"{ResponseSignal.FETCHING.value}: Starting data fetch for Egypt...")

    while True:
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
            logging.info("✅ No more data available from API.")
            break

        # Extract only relevant info without cleaning
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
                    "Lat": addr.get("Latitude"),
                    "Lon": addr.get("Longitude"),
                    "Cost": d.get("UsageCost"),
                    "Num_Connections": len(d.get("Connections", [])),
                    "Last_Updated": d.get("DateLastStatusUpdate"),
                }
            )

        batch_size = len(data)
        total_fetched += batch_size
        offset += PAGE_SIZE

        logging.info(f"Fetched {batch_size} new records → total: {total_fetched}")
        sleep(1.5)  # avoid API rate limit

        if batch_size < PAGE_SIZE:
            break  # no more data to fetch

    df = pd.DataFrame(all_records)
    logging.info(f"✅ Total raw records fetched: {len(df)}")
    return df


def save_data(df: pd.DataFrame):
    """Save raw EV data to CSV."""
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = DATA_RAW_DIR / "ev_data_egypt_raw.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    logging.info(f"{ResponseSignal.SAVED_LOCAL.value} at {csv_path}")
    print(f"Raw data successfully saved at: {csv_path}")


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
