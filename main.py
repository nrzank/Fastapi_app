import os
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from api.v1 import router as router_v1
from database import engine
from models import Base

from contextlib import asynccontextmanager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix='/api/v1')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("/app")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
