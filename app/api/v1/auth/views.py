from fastapi import APIRouter

from .auth import create_access_token, get_password_hash
from .schemas import UserRegister

router = APIRouter(tags=["Register"])


@router.post("/")
async def register(user_register: UserRegister):
    hashed_password = get_password_hash(user_register.password)
    token = create_access_token({"sub": user_register.email})
    return {"access_token": token}
