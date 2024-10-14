import datetime
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import or_
from sqlalchemy.orm import Session
from .models import UserModel
from .schemas import UserCreate, UserUpdate
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
EXPIRE_MINUTES = int(os.getenv("EXPIRE_MINUTES"))
ALGORITHM = os.getenv("ALGORITHM")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
bcrypt_context = CryptContext(schemes=["bcrypt"])


async def check_existing_user(db: Session, username: str, email: str):
    return db.query(UserModel).filter(or_(UserModel.username == username, UserModel.email == email)).first()


async def create_token(id: int, username: str):
    encode = {"sub": username, "id": id}
    expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=EXPIRE_MINUTES)
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(db: Session, token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        id: int = payload.get("id")
        expires: datetime = payload.get("exp")

        if datetime.datetime.now(datetime.timezone.utc) > datetime.datetime.fromtimestamp(expires, tz=datetime.timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

        if username is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        db_user = db.query(UserModel).filter(UserModel.id == id).first()
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return db_user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def create_user(db: Session, user: UserCreate):
    db_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=bcrypt_context.hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def authenticate(db: Session, username: str, password: str):
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if not db_user or not bcrypt_context.verify(password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    return db_user


async def update_user(db: Session, token: str, user_data: UserUpdate):
    current_user = await get_current_user(db, token)
    for var, value in vars(user_data).items():
        setattr(current_user, var, value) if value else None

    db.commit()
    db.refresh(current_user)
    return current_user

