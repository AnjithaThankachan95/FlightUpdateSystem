# app/services/flightservice.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_flight_status(flight_number: str):
    url = f"https://api.aviationstack.com/v1/flights?access_key={API_KEY}&flight_iata={flight_number}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()

        # Log the full API response for debugging
        print(f"API Response for {flight_number}: {data}")

        # Check if data exists
        if data.get("data") and len(data["data"]) > 0:
            flight_info = data["data"][0]
            return {
                "flight_number": flight_info["flight"]["iata"],
                "departure": flight_info["departure"]["airport"],
                "arrival": flight_info["arrival"]["airport"],
                "status": flight_info["flight_status"]
            }
        else:
            print(f"No flight data found for flight number: {flight_number}")
            return None

    except requests.exceptions.RequestException as e:
        # Handle connection errors, timeouts, etc.
        print(f"Error fetching flight data for {flight_number}: {e}")
        return None
    except KeyError as e:
        # Handle unexpected response structure
        print(f"Unexpected data structure for {flight_number}: Missing key {e}")
        return None
