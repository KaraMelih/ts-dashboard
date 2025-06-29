#!/usr/bin/env python3
import requests
from datetime import datetime, UTC
from ..src.ts_dashboard.crud import upsert_price_points

# Configuration
API_URL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"

def fetch_last_5_days(currency="usd", days=5, interval="hourly"):
    """ Fetches the last 5 days of Bitcoin price data from CoinGecko.
        Returns a list of tuples (date, price).
        For now ignores market cap and total volumes.
        Default interval is hourly but for some data it might require API key.
        See https://www.coingecko.com/en/api/documentation for details.

        Notes:
        - CoinGecko API returns prices in milliseconds since epoch.
        asking for hourly interval sometime crashes even though it is allow for less than 90 days
        by default it returns hourly data anyway, so we use that.

    """
    today = datetime.date.today()
    # CoinGecko takes days as number; get 5 days back
    params = {"vs_currency": currency, "days": days, } #"interval": interval}
    ## use the default hourly interval for now. It complains.   
    resp = requests.get(API_URL, params=params)
    resp.raise_for_status()
    data = resp.json()
    # data["prices"] is a list of [timestamp_ms, price]
    points = []
    for ts_ms, price in data["prices"]:
        # Convert ms → date
        dt = datetime.fromtimestamp(ts_ms/1000, UTC)
        points.append((dt, float(price)))
    # Keep unique dates (API returns multiple per day)
    unique = {}
    for dt, price in points:
        unique[dt] = price
    return unique

def populate_db():
    """Fetches the last 5 days of Bitcoin price data and upserts into the database."""
    price_points = fetch_last_5_days()
    upsert_price_points(price_points)
    print(f"Updated price points on {datetime.now()}.")

# This script can be run directly to populate the database
if __name__ == "__main__":
    populate_db()
