from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import Users
from src.hashing import Hasher
from sqlalchemy.exc import IntegrityError

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/register")
def registration(request: Request):
    return templates.TemplateResponse("user_register.html", {"request": request})


@router.post("/register")
async def registration(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    errors = []
    if not password or len(password) < 6:
        errors.append("Password should be greater than 6 chars")
    if not email:
        errors.append("Email can't be blank")
    user = Users(email=email, password=Hasher.get_hash(password))
    if len(errors) > 0:
        return templates.TemplateResponse(
            "user_register.html", {"request": request, "errors": errors}
        )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return responses.RedirectResponse(
            "/?msg=successfully registered", status_code=status.HTTP_302_FOUND
        )
    except IntegrityError:
        errors.append("Duplicate email")
        return templates.TemplateResponse(
            "user_register.html", {"request": request, "errors": errors}
        )