import os, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID
from passlib.context import CryptContext
from configparser import ConfigParser
from pydantic import EmailStr, BaseModel
from sqlmodel import select, Field
from src.config import CONFIG_PATH
from src.models.user import User, RoleEnum

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):
    return pwd_context.hash(password)

class GetUsersResponse(BaseModel):
    id: Optional[UUID] = Field(None)
    fname: Optional[str] = Field(None)
    lname: Optional[str] = Field(None)
    email: Optional[EmailStr] = Field(None)
    disabled: Optional[bool] = Field(None)
    role: Optional[RoleEnum] = Field(None)

def get_auth_config():
    """
    Returns auth config for secret key, algorithm specific to hashed password and token expiry in mins.
    """
    access_token_expiry = 30  # Default 30 minutes, overwritten by config
    config = ConfigParser()
    config.read(os.path.join(CONFIG_PATH, "config.ini"))
    secret_key = config["Auth"]["SECRET_KEY"]
    algorithm = config["Auth"]["ALGORITHM"]
    if config["Auth"]["ACCESS_TOKEN_EXPIRE_MINUTES"]: access_token_expiry = int(
        config["Auth"]["ACCESS_TOKEN_EXPIRE_MINUTES"])
    return secret_key, algorithm, access_token_expiry

def get_user(session, creds=None, username=None):
    if username:
        query = select(User).where(User.username == username, User.disabled == False)
    else:
        query = select(User).where(User.username == creds.username, User.disabled == False)
    userrec = session.exec(query)
    user = None
    if userrec is not None:
        user = userrec.first()
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(session, creds):
    user = get_user(session, creds=creds)
    if not user:
        return False
    if isinstance(creds.password, str) and not verify_password(creds.password, user.password):
        return False
    elif isinstance(creds.password, str) is False and not verify_password(creds.password.get_secret_value(),
                                                                          user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    secret_key, algorithm, _ = get_auth_config()
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

def get_access_token(creds, session, ACCESS_TOKEN_EXPIRE_MINUTES):
    """
    Return bearer token on successful user authentication.
    """
    try:
        user = authenticate_user(session, creds)
        if not user:
            access_token = None
        else:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires
            )
    except:
        access_token = None
    return access_token