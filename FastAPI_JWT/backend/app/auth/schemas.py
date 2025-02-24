"""
Developer: Hana Bizhani
Date: 2025-02-21
Change Log:
- Initial creation of the file.
"""

from pydantic import BaseModel, EmailStr
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    class Config:
        orm_mode = True
class Token(BaseModel):
    access_token: str
    token_type: str