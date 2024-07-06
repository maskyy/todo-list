from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from playhouse.shortcuts import model_to_dict
from pydantic import BaseModel

from ..config import JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY
from ..const import JWT_ALGORITHM
from ..database import User
from ..schemas import ModelDelete
from ..schemas import User as UserSchema
from ..schemas import UserCreate


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    login: str | None = None


__all__ = [
    "router",
]

router = APIRouter(prefix="/users")

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
_oauth2_schema = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_password_hash(password: str) -> str:
    return _pwd_context.hash(password)


@router.post("/")
async def create_user(user: UserCreate):
    password = get_password_hash(user.password)
    User.create(**user.model_dump() | {"password": password})
    # peewee does not return defaults automatically...
    new = User.get(User.login == user.login)
    return UserSchema(**model_to_dict(new))


def verify_password(plain: str, hashed: str) -> bool:
    return _pwd_context.verify(plain, hashed)


def get_user(login: str) -> User | None:
    return User.get_or_none(User.login == login)


def authenticate_user(login: str, password: str) -> User | None:
    user = get_user(login)
    if not user or not verify_password(password, user.password):
        return None
    return user


def create_access_token(data: dict) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy() | {"exp": exp}
    token = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


async def get_current_user(token: Annotated[str, Depends(_oauth2_schema)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        login = payload.get("sub")
        if not login:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(login)
    if user is None:
        raise credentials_exception
    return user


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": user.login})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserSchema)
async def read_current_user(user: Annotated[UserSchema, Depends(get_current_user)]):
    return user


@router.delete("/me")
async def delete_current_user(user: Annotated[ModelDelete, Depends(get_current_user)]):
    User.delete_by_id(user.id)
    return {"message": "Account deleted"}
