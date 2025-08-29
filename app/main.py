# main.py
import os
from fastapi import FastAPI, HTTPException
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Flight Status Checker")

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.aviationstack.com/v1/flights"

@app.get("/flight-status/{flight_number}")
def get_flight_status(flight_number: str):
    params = {
        "access_key": API_KEY,
        "flight_iata": flight_number
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")
    
    if data.get("data"):
        flight = data["data"][0]
        return {
            "flight_number": flight["flight"]["iata"],
            "departure_airport": flight["departure"]["airport"],
            "arrival_airport": flight["arrival"]["airport"],
            "departure_time": flight["departure"]["estimated"],
            "arrival_time": flight["arrival"]["estimated"],
            "status": flight["flight_status"]
        }
    else:
        raise HTTPException(status_code=404, detail="Flight not found")
