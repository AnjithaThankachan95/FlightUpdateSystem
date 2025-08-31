import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_flight_status(flight_number: str):
    url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&flight_iata={flight_number}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            flight_info = data["data"][0]
            return {
                "flight_number": flight_info["flight"]["iata"],
                "departure": flight_info["departure"]["airport"],
                "arrival": flight_info["arrival"]["airport"],
                "status": flight_info["flight_status"]
            }
    return None
