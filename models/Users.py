from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str
    role: str

class UpdatePassword(BaseModel):
    email: str
    old_password: str
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str