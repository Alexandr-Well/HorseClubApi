from typing import List, Dict, Union
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.router import fastapi_users
from src.database import get_async_session
from src.helpers.models_helper import count_model_obj
from src.horse import crud
from src.horse.schemas import HorseRead, HorseMain, HorseUpdate
from src.horse.models import Horse

current_user = fastapi_users.current_user()
current_superuser = fastapi_users.current_user(active=True, superuser=True)

router = APIRouter(
    prefix='/api/horse',
    tags=['horses'],
)


@router.get("/all", status_code=200, response_model=Dict[str, Union[List[HorseRead], int]])
@cache(expire=10)
async def get_all_horses(session: AsyncSession = Depends(get_async_session), offset: int = 0, limit: int = 10):
    try:
        count_model = await count_model_obj(Horse, db=session)
        payload = await crud.get_horses(db=session, offset=offset, limit=limit)
        return {
            "status": 200,
            "data": payload,
            "total_objects": count_model
        }
    except Exception as err:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": str(err)
        })


@router.get("/", status_code=200, response_model=HorseRead)
async def get_horse(horse_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        horse = await crud.get_horse_by_id(horse_id=horse_id, db=session)
        return HorseRead(**horse.__dict__).dict()

    except Exception as err:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": str(err)
        })


@router.post("/", status_code=200, dependencies=[Depends(current_superuser)])
async def create_horse(horse: HorseMain, session: AsyncSession = Depends(get_async_session)):
    try:
        horse = await crud.create_horse(horse=horse, db=session)
        return HorseRead(**horse.__dict__).dict()
    except Exception as err:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": str(err)
        })


@router.delete("/", status_code=200, dependencies=[Depends(current_superuser)])
async def remove_horse(horse_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        await crud.remove_horse(horse_id=horse_id, db=session)
        return {
            'status': 'delete successful'
        }
    except Exception as err:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": str(err)
        })


@router.patch("/", status_code=200, dependencies=[Depends(current_superuser)], response_model=HorseUpdate)
async def update_horse(horse_id: int, horse: HorseUpdate, session: AsyncSession = Depends(get_async_session)):
    try:
        horse = await crud.update_horse(horse_id=horse_id, db=session, horse=horse)
        return HorseRead(**horse.__dict__).dict()

    except Exception as err:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": str(err)
        })
