from fastapi import APIRouter, HTTPException, status, Depends
from ..schemas.user import UserCreate, UserInDB, UserUpdate
from ..dependencies.dependencies import get_user_repo
from typing import List
from ..repositories.user_repository import UserRepository


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "User not found"}},
)


@router.get("/", response_model=List[UserInDB])
async def get_all_users(user_repo: UserRepository = Depends(get_user_repo)):
    return await user_repo.get_all()


@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, user_repo: UserRepository = Depends(get_user_repo)):
    return await user_repo.create(user)

@router.get("/{user_id}", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def get_user_by_id(user_id: int, user_repo: UserRepository = Depends(get_user_repo)):
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserInDB)
async def update_user(user_id: int, user_update: UserUpdate, user_repo: UserRepository = Depends(get_user_repo)):
    updated_user = await user_repo.update(user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user



@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, user_repo: UserRepository = Depends(get_user_repo)):
   success = await user_repo.delete(user_id)
   if not success:
       raise HTTPException(status_code=404, detail="User not found")
   return None