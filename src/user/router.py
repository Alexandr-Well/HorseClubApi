from typing import List
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.auth.models import User
from src.auth.router import fastapi_users
from src.celery.tasks import send_email_report
from src.database import get_async_session
from src.user.schemas import OneUser

current_user = fastapi_users.current_user()

router = APIRouter(
    prefix='/api/accounts',
    tags=['accounts'],
    dependencies=[Depends(current_user)]
)


@router.get("/", response_model=List[OneUser], status_code=200)
@cache(expire=60)
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


@router.post("/mail", status_code=200)
async def send_mail_to_user(user_email: str, subject: str, text: str, subtype: str):
    try:
        send_email_report.delay(user_email=user_email, subject=subject, text=text, subtype=subtype)
        return {
            "status": "200",
            "data": None,
            "details": None
        }

    except Exception as err:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": str(err)
        })
