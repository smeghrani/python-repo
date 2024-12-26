from fastapi import APIRouter, HTTPException
from src.modules.db.db import SessionDep
from src.models.user import User, RoleEnum
from starlette import status
from src.modules.db.user import get_password_hash


router = APIRouter(
    tags=["Auth API"],
    dependencies=[],
    responses={
        200: {"description": "Content generated successfully"},
        400: {"description": "Invalid input"},
        404: {"description": "Not found"},
        500: {"description": "Content generation error"}
    }
)

@router.post("/users/")
async def register_user(user: User, session: SessionDep) -> User:
    try:
        """
        Register new user as per user model. Email and username and unique.
        """
        if user.role not in [role.value for role in RoleEnum]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except Exception as e:
        session.rollback()
        raise e