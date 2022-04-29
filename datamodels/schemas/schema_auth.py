from typing import Optional
from pydantic import BaseModel
from datetime import date

################### Auth login #################
class Login(BaseModel):
    username: str
    password: str


################### User #################
class UserBase(BaseModel):
    username: str
    password: str
    email: str


class CreateUser(UserBase):
    created: date


################### Token #################
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

