from typing import Optional

from pydantic import BaseModel, EmailStr


class UserForRegister(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str
    is_superuser: bool = False


class BlogForNew(BaseModel):
    title: str
    subtitle: Optional[str]

    is_published: bool = False
    body: str
