from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from auth.base_config import auth_backend
from auth.manager import get_user_manager
from auth.models import User
from auth.schemas import UserRead, UserCreate

from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

# routers
from src.routes.user.router import router as router_users

app = FastAPI(
    title='horse_club_backend'
)

# current_user = fastapi_users.current_user()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(router_users)


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
