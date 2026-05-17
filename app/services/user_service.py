from datetime import datetime, timezone
from threading import Lock

from fastapi import HTTPException, status

from app.schemas.user import UserCreate, UserListResponse, UserRead


class UserService:
    """In-memory user service for demo purposes."""

    def __init__(self) -> None:
        self._users_by_id: dict[int, UserRead] = {}
        self._email_to_id: dict[str, int] = {}
        self._next_id: int = 1
        self._lock = Lock()

    def create_user(self, payload: UserCreate) -> UserRead:
        normalized_email = payload.email.lower()

        with self._lock:
            if normalized_email in self._email_to_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A user with this email already exists.",
                )

            user = UserRead(
                id=self._next_id,
                email=payload.email,
                full_name=payload.full_name,
                created_at=datetime.now(timezone.utc),
            )

            self._users_by_id[user.id] = user
            self._email_to_id[normalized_email] = user.id
            self._next_id += 1

        return user

    def get_user(self, user_id: int) -> UserRead:
        user = self._users_by_id.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id={user_id} was not found.",
            )
        return user

    def list_users(self) -> UserListResponse:
        items = sorted(self._users_by_id.values(), key=lambda user: user.id)
        return UserListResponse(items=items, total=len(items))
