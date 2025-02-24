"""
Developer: Hana Bizhani
Date: 2025-02-21
Change Log:
- Initial creation of the file.
"""

from fastapi import Depends, HTTPException, status, APIRouter
from backend.app.auth.api import get_current_user
from backend.app.auth import models  # Import the User model
from sqlalchemy.orm import Session
from backend.app.database import get_db


router = APIRouter()

@router.get("/protected-resource")
async def protected_resource(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = do_something_authorized(db=db, current_user=current_user)
    return result

def do_something_authorized(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    This function requires a valid JWT token in the request headers.
    """
    # Access user information from current_user
    user_id = current_user.id
    username = current_user.username

    # Your logic here, knowing the user is authenticated
    return {"message": f"Hello {username}, you are authorized to do something!"}