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
def flights_page(request: Request, token: str = None, db: Session = Depends(get_db)):
    if not token:
        # No token, redirect to login
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Please login first."}
        )
    
    try:
        user = get_current_user(token, db)
    except Exception:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Session expired or invalid. Please log in again."}
        )
    
    # Render flights page with empty flight info
    return templates.TemplateResponse(
        "flights.html",
        {
            "request": request,
            "username": user.username,
            "flight_info": None,
            "token": token,
            "error": None
        }
    )

# ---------------------------
# Handle flight tracking (POST)
# ---------------------------
@router.post("/flights", response_class=HTMLResponse)
def track_flight(
    request: Request,
    flight_number: str = Form(...),
    token: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        user = get_current_user(token, db)
    except JWTError:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Session expired or invalid. Please log in again."}
        )

    flight_data = get_flight_status(flight_number)

    if not flight_data or not flight_data.get('flight_number'):
        return templates.TemplateResponse(
            "flights.html",
            {
                "request": request,
                "username": user.username,
                "flight_info": None,
                "error": f"No flight data found for flight number: {flight_number}",
                "token": token,
            }
        )
    return templates.TemplateResponse(
        "flights.html",
        {
            "request": request,
            "username": user.username,
            "flight_info": flight_data,
            "error": None,
            "token": token
        }
    )
