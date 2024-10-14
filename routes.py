import io
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .models import UserModel
from .schemas import UserCreate, UserResponse, UserUpdate
from .database import get_db
import auth_api.services
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = await auth_api.services.check_existing_user(db, user.username, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or Email already in use"
        )
    db_user = await auth_api.services.create_user(db, user)
    access_token = await auth_api.services.create_token(db_user.id, db_user.username)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": db_user.username,
    }


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = await auth_api.services.authenticate(db, form_data.username, form_data.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Username/Password")
    access_token = await auth_api.services.create_token(db_user.id, db_user.username)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/users/profile", response_model=UserResponse)
async def get_user(token: str, db: Session = Depends(get_db)):
    db_user = await auth_api.services.get_current_user(db, token)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You aren't authorized! Please try again.")
    return db_user


@router.put("/users/profile", response_model=UserResponse)
async def update_user(token: str, first_name: str = Form(None), last_name: str = Form(None), username: str = Form(None),
                      email: str = Form(None), phone: str = Form(None), designation: str = Form(None),
                      department: str = Form(None), file: UploadFile = File(None), db: Session = Depends(get_db)):
    user_data = UserUpdate(
        first_name=first_name, last_name=last_name, username=username, email=email,
        phone=phone, designation=designation, department=department
    )
    db_user = await auth_api.services.update_user(db, token, user_data)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You aren't authorized! Try again.")
    if file:
        image_data = await file.read()
        db_user.profile_picture = image_data
        db.commit()
        db.refresh(db_user)
    return db_user


@router.get("/users/profile-picture")
async def get_profile_picture(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user or not user.profile_picture:
        raise HTTPException(status_code=404, detail="Profile picture not found")
    return StreamingResponse(io.BytesIO(user.profile_picture), media_type="image/png")
