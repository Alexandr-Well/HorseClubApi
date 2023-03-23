from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class HorsePhotoRead(BaseModel):
    id: int
    path: str


class HorseRead(BaseModel):
    id: int
    name: str
    color: str
    age: int
    photo: Optional[List[HorsePhotoRead]]