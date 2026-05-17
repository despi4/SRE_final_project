from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.dependencies import get_user_service
from app.schemas.user import UserCreate, UserListResponse, UserRead
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user",
)
def create_user(payload: UserCreate, service: UserServiceDep) -> UserRead:
    return service.create_user(payload)


@router.get("", response_model=UserListResponse, summary="List users")
def list_users(service: UserServiceDep) -> UserListResponse:
    return service.list_users()


@router.get("/{user_id}", response_model=UserRead, summary="Get user by id")
def get_user(
    user_id: Annotated[int, Path(gt=0)],
    service: UserServiceDep,
) -> UserRead:
    return service.get_user(user_id)
