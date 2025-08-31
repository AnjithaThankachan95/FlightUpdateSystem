from fastapi import APIRouter, Depends, Query, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.flightservice import get_flight_status
from app.services.tokenservice import get_current_user  # use only this

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ----------------------------
# Show flight page (GET)
# ----------------------------
@router.get("/flights", response_class=HTMLResponse)
def flights(
    request: Request,
    token: str,
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    return templates.TemplateResponse(
        "flights.html",
        {"request": request, "username": user.username, "flight_info": None}
    )


# ----------------------------
# Handle form submission (POST)
# ----------------------------
@router.post("/flights", response_class=HTMLResponse)
def track_flight(
    request: Request,
    flight_number: str = Form(...),
    token: str = Form(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    flight_data = get_flight_status(flight_number)

    if not flight_data:
        raise HTTPException(status_code=404, detail="Flight not found")

    return templates.TemplateResponse(
        "flights.html",
        {"request": request, "username": user.username, "flight_info": flight_data}
    )
