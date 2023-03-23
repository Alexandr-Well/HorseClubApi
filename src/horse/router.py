from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, join
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.router import fastapi_users
from src.database import get_async_session
from src.horse.models import Horse, HorsePhoto
from src.horse.schemas import HorseRead, HorsePhotoRead

current_user = fastapi_users.current_user()

router = APIRouter(
    prefix='/api/horse',
    tags=['horse'],
)

# related model
@router.get("/",  status_code=200)
@cache(expire=4)
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Horse, HorsePhoto).select_from(join(Horse, HorsePhoto, HorsePhoto.horse_id == Horse.id))
        result = await session.execute(query)
        horse = 0
        horse_photo = []
        result = result.fetchall()
        if result:
            horse = result[0][0]
            if len(result[0]) > 1:
                horse_photo = list(map(lambda x: HorsePhotoRead(**x[1].__dict__).dict(), result))
        hor = HorseRead(**horse.__dict__)
        hor.photo = horse_photo
        return hor
    except Exception as err:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": str(err)
        })
