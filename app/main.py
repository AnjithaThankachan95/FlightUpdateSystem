# app/main.py
from fastapi import FastAPI
from app.routes import authentication, flight  # import your routers
from app.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flight Updates Service", version="1.0")

# Include routers
app.include_router(authentication.router, prefix="/authentication", tags=["Authentication"])
app.include_router(flight.router, tags=["Flights"])  # no prefix to keep /flights as URL

# Root redirect to login
from fastapi.responses import RedirectResponse

@app.get("/")
def root():
    return RedirectResponse(url="/authentication/login")
