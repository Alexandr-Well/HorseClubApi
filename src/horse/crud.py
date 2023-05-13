from typing import Dict, Any, List
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager
from src.database import get_async_session
from src.horse.models import Horse, HorsePhoto
from src.horse.schemas import HorseMain, HorseUpdate, HorseRead, HorsePhotoRead


async def get_horses(db: AsyncSession = Depends(get_async_session), offset: int = 0, limit: int = 10) \
        -> List[Dict[str, Any]]:
    """
    :param db: session (async)
    :param offset: int
    :param limit: int
    :return: -> List[Horse.__dict__]
    """
    query = select(Horse).outerjoin(HorsePhoto).options(contains_eager(Horse.photo, HorsePhoto.horse)) \
        .order_by(Horse.id.asc()).offset(offset).limit(offset + limit)
    result = await db.execute(query)
    result = tuple(map(lambda x: x[0], result.unique().fetchall()))
    response = []
    for item in result:
        current_horse = item.__dict__
        try:
            photo = list(map(lambda x: HorsePhotoRead(**x.__dict__).dict(), current_horse.pop('photo')))
        except Exception:
            photo = []
        response.append(HorseRead(**current_horse, photo=photo).dict())
    return response


async def get_horse_by_id(horse_id: int, db: AsyncSession = Depends(get_async_session)) -> Dict[str, Any]:
    """
    :param horse_id: int
    :param db: session (async)
    :return: -> Dict[str, Any]
    """
    query = select(Horse).where(Horse.id == horse_id)
    result = await db.execute(query)
    result = result.fetchone()[0]
    return result


async def remove_horse(horse_id: int, db: AsyncSession = Depends(get_async_session)) -> None:
    """
    :param horse_id: int
    :param db: session (async)
    :return: -> None
    """
    _horse = await get_horse_by_id(horse_id=horse_id, db=db)
    await db.delete(_horse)
    await db.commit()


async def save_main_model_add_related_models(_horse, db, horse) -> Horse:
    """
    common method for create_horse and update_horse (save main model, after take all related models and save it)
    return (created/modifyed) Horse model
    :param _horse: Horse (model)
    :param db: session (async)
    :param horse:
    :return: -> Horse (model)
    """
    await db.commit()
    if horse.photo:
        _horses_photos = list(map(lambda x: HorsePhoto(path=x.path, horse_id=_horse.id), horse.photo))
        db.add_all(_horses_photos)
        await db.commit()
    await db.refresh(_horse)
    return _horse


async def create_horse(horse: HorseMain, db: AsyncSession = Depends(get_async_session)) -> Horse:
    """
    :param horse: HorseMain (schemas)
    :param db: session (async)
    :return: -> Horse (model)
    """
    _horse = Horse(name=horse.name, color=horse.color, age=horse.age)
    db.add(_horse)
    return await save_main_model_add_related_models(_horse, db, horse)


async def update_horse(horse_id: int, horse: HorseUpdate, db: AsyncSession = Depends(get_async_session)) -> Horse:
    """
    :param horse_id: int
    :param horse: HorseUpdate (schemas)
    :param db: session (async)
    :return: -> Horse
    """
    _horse = await get_horse_by_id(horse_id=horse_id, db=db)
    for key, val in horse.__dict__.items():
        if val:
            if not isinstance(val, list):
                setattr(_horse, key, val)
    return await save_main_model_add_related_models(_horse, db, horse)
