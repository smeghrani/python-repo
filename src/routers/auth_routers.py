import uuid
import logging
from sqlmodel import select
from starlette import status
from config.constants import SUCCESS_GET_SINGLE_USER
from src.modules.db.db import SessionDep
from src.models.user import User, RoleEnum
from fastapi import APIRouter, HTTPException
from src.modules.db.user import get_password_hash, GetUsersResponse


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

@router.get("/users/{user_id}", response_model=dict)
async def get_user_by_id(user_id: str, session: SessionDep):
    """
    Fetch a user by their ID.
    """
    try:
        user_uuid = uuid.UUID(user_id)
        user = session.exec(select(User).where(User.id == user_uuid)).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {
            "data": GetUsersResponse(
                id=user.id,
                fname=user.fname,
                lname=user.lname,
                email=user.email,
                disabled=user.disabled,
                role=user.role
            ),
            "message": SUCCESS_GET_SINGLE_USER,
            "status": "success"
        }

    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")
    except Exception as e:
        logging.error(f"Error in fetching user by ID: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")