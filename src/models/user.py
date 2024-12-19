from datetime import datetime
from typing import Optional
from pydantic import SecretStr, EmailStr
from pydantic.json_schema import SkipJsonSchema
from sqlmodel import SQLModel, Field, AutoString
from uuid import UUID, uuid4

class Primary(SQLModel):
    id: int | None = Field(default=None, primary_key=True, index=True)

class Credentials(Primary):
    id: SkipJsonSchema[int] = Field(default=None, primary_key=True, index=True, exclude=True)
    username: str = Field(unique=True, index=True)
    password: SecretStr = Field(sa_type=AutoString, index=True, exclude=True)

class User(Credentials, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True, index=True, exclude=True)
    fname: str = Field(index=True)
    lname: str = Field(index=True)
    email: EmailStr = Field(sa_type=AutoString, unique=True, index=True)
    disabled: bool = Field(default=True, index=True)
    otp_code: Optional[str] = Field(default=None, index=True)
    otp_expires_at: Optional[datetime] = Field(default=None, index=True)
