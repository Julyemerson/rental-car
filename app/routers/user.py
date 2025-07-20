from fastapi import APIRouter, HTTPException, status
from typing import Optional, List
from ..schemas.user import UserCreate, UserInDB, UserUpdate
from ..database.db import get_db_pool
from ..repositories.user_repository import UserRepository


import asyncio
db_pool = asyncio.run(get_db_pool())
user_repo = UserRepository(pool=db_pool)


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "User not found"}},
)


@router.get("/", response_model=List[UserInDB])
async def get_all_users():
    return await user_repo.get_all()


@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    return await user_repo.create(user)

@router.get("/{user_id}", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def get_user_by_id(user_id: int):
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserInDB)
async def update_user(user_id: int, user_update: UserUpdate):
    updated_user = await user_repo.update(user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user



@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
   success = await user_repo.delete(user_id)
   if not success:
       raise HTTPException(status_code=404, detail="User not found")
   return None