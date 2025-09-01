# app/routes/authentication.py
from fastapi import APIRouter, FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from requests import request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usermodel import User
from app.services.tokenservice import create_access_token, get_current_user
from passlib.context import CryptContext

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Register
# GET register
@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html",  {
        "request": request,
        "error": None,
        "username": ""
    })
# POST register
@router.post("/register")
def register(
    request: Request,   # 👈 include request
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.username == username).first():
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "Username already exists",
                "username": username,
                "success": None
            }
        )

    user = User(username=username, password_hash=get_password_hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)

    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "error": None,
            "success": "Registration successful! You can now login.",
            "username": ""
        }
    )

# Login
# GET login 
@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
          "request": request,
          "error": None,
          "username": ""
        }
    )
# POST login
@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Invalid username or password",
                "username": username
            }
        )

    token = create_access_token({"sub": user.username})
    return RedirectResponse(url=f"/flights?token={token}", status_code=302)

