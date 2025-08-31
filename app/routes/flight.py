# app/routes/flight.py
from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.flightservice import get_flight_status
from app.routes.authentication import get_current_user
from app.services.tokenservice import create_access_token
from jose import JWTError

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ---------------------------
# Show flights page (GET)
# ---------------------------
@router.get("/flights", response_class=HTMLResponse)
def flights_page(request: Request, token: str, db: Session = Depends(get_db)):
    try:
        user = get_current_user(token, db)
    except JWTError:
        # Token invalid or expired
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Session expired, please log in again."}
        )
    
    return templates.TemplateResponse(
        "flights.html",
        {"request": request, "username": user.username, "flight_info": None}
    )


# ---------------------------
# Handle flight tracking (POST)
# ---------------------------
@router.post("/flights", response_class=HTMLResponse)
def track_flight(request: Request, flight_number: str = Form(...), token: str = Form(...), db: Session = Depends(get_db)):
    try:
        user = get_current_user(token, db)
    except JWTError:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Session expired, please log in again."}
        )
    
    flight_data = get_flight_status(flight_number)
    
    if not flight_data:
        # Log the API response for debugging
        print(f"Flight not found for flight_number={flight_number}")
        return templates.TemplateResponse(
            "flights.html",
            {
                "request": request,
                "username": user.username,
                "flight_info": None,
                "error": f"No data found for flight {flight_number}. Try again later."
            }
        )
    
    return templates.TemplateResponse(
        "flights.html",
        {
            "request": request,
            "username": user.username,
            "flight_info": flight_data,
            "error": None
        }
    )
