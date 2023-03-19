from typing import List
from pydantic import BaseModel


class OneUser(BaseModel):
    id: int
    email: str
    username: str


    class Config:
        orm_mode = True


class Users(BaseModel):
    users: List[OneUser]

    class Config:
        orm_mode = True
