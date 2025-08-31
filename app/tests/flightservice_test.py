# tests/test_flight_service.py
import os
import pytest
from app.services.flightservice import get_flight_status
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

@pytest.mark.skipif(not API_KEY, reason="No API_KEY set in .env")
def test_get_flight_status_real():
    # Test with a known flight number
    flight_number = "DL105"  # American Airlines 100, example
    flight = get_flight_status(flight_number)
    
    # Make assertions
    assert flight is not None, "Flight info should not be None"
    assert flight["flight_number"] == flight_number, "Flight number should match"
    assert "departure" in flight, "Flight should have departure info"
    assert "arrival" in flight, "Flight should have arrival info"
    assert "status" in flight, "Flight should have status info"

    print("Flight info:", flight)
