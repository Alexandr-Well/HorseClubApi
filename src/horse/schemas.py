from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class HorsePhotoRead(BaseModel):
    path: str


class HorseMain(BaseModel):
    name: str
    color: str
    age: int
    photo: Optional[List[HorsePhotoRead]]


class HorseUpdate(BaseModel):
    name:  Optional[str]
    color: Optional[str]
    age: Optional[int]
    photo: Optional[List[HorsePhotoRead]]


class HorseRead(BaseModel):
    id: int
    name: str
    color: str
    age: int
    registered_at: datetime
    photo: Optional[List[HorsePhotoRead]]
