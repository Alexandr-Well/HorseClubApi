from typing import List
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.auth.models import User
from src.database import get_async_session
from src.user.schemas import OneUser

router = APIRouter(
    prefix='/api/users',
    tags=['users']
)


@router.get("/", response_model=List[OneUser], status_code=200)
@cache(expire=30)
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(User)
        result = await session.execute(query)
        return list(map(lambda x: OneUser(**x.__dict__), result.scalars().all()))

    except Exception as err:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": str(err)
        })
