"""simulate trip controller."""

import httpx
from models.simulate import SimulationRequest, SimulationResponse, StationInfo
from helpers.config import get_settings

settings = get_settings()


# async def fetch_nearby_stations(lat: float, lon: float, max_results=5):
#     url = "https://api.openchargemap.io/v3/poi/"

#     params = {
#         "key": settings.OPENCHARGEMAP_API_KEY,
#         "latitude": lat,
#         "longitude": lon,
#         "maxresults": max_results,
#         "distance": 20,
#         "distanceunit": "KM"
#     }

#     async with httpx.AsyncClient() as client:
#         resp = await client.get(url, params=params)
#         data = resp.json()

#     stations = []
#     for s in data:
#         stations.append(
#             StationInfo(
#                 name=s.get("AddressInfo", {}).get("Title", "Unknown Station"),
#                 lat=s.get("AddressInfo", {}).get("Latitude"),
#                 lon=s.get("AddressInfo", {}).get("Longitude")
#             )
#         )

#     return stations

async def fetch_nearby_stations(lat: float, lon: float, max_results=5):
    url = "https://api.openchargemap.io/v3/poi/"

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": settings.OPENCHARGEMAP_API_KEY
    }

    params = {
        "latitude": lat,
        "longitude": lon,
        "maxresults": max_results,
        "distance": 20,
        "distanceunit": "KM"
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params, headers=headers)

        # Debug if swagger only fails
        print("RAW RESPONSE", resp.status_code, resp.text)

        resp.raise_for_status()
        data = resp.json()

    stations = []
    for s in data:
        stations.append(
            StationInfo(
                name=s.get("AddressInfo", {}).get("Title", "Unknown Station"),
                lat=s.get("AddressInfo", {}).get("Latitude"),
                lon=s.get("AddressInfo", {}).get("Longitude")
            )
        )

    return stations


async def simulate_trip(data: SimulationRequest) -> SimulationResponse:

    # Mock distance + energy logic
    distance_km = 120
    avg_consumption = 16
    energy_used = (distance_km / 100) * avg_consumption

    needs_charging = data.car.current_battery_percentage < 50
    num_charges = 2 if needs_charging else 0

    station_list = []

    if needs_charging:
        # Fetch stations near START point
        station_list = await fetch_nearby_stations(
            data.start.lat,
            data.start.lon,
        )

        # Limit number of charging stops
        station_list = station_list[:num_charges]

    return SimulationResponse(
        trip_time_minutes=95,
        avg_consumption_kwh_100km=avg_consumption,
        energy_used_kwh=energy_used,
        start=data.start,
        end=data.end,
        charges=needs_charging,
        number_of_charges=num_charges,
        stations=station_list
    )
