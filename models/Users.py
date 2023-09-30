from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    Username: str
    password: str
    role: str

class UpdatePassword(BaseModel):
    Username: str
    old_password: str
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# class TokenData(BaseModel):
#     email: str | None = None