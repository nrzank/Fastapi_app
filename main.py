from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from app.api.v1 import router
from app.database.models import Base
from app.database.session import engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    lifespan=lifespan,
    openapi_url="/api/v1/openapi.json",
    debug=True,
)

app.include_router(router, prefix='/api/v1')
