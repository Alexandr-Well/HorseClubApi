from fastapi import Depends
from sqlalchemy.sql.expression import func
from sqlalchemy import select
from database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session


async def count_model_obj(model: Base, db: AsyncSession = Depends(get_async_session)) -> int:
    """
    :param model: any db model
    :param db: session
    :return: count(model)  -> int
    """
    data = await db.execute(select(func.count()).select_from(model))
    rez = data.fetchone()[0]
    return rez


if __name__ == '__main__':
    ...
