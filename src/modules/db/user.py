from sqlmodel import Field
from uuid import UUID
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from typing_extensions import Optional
from src.models.user import RoleEnum

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