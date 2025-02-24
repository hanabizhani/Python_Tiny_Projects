"""
Developer: Hana Bizhani
Date: 2025-02-21
Change Log:
- Initial creation of the file.
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.app.database import engine, get_db
from . import models, schemas, auth

# Run the database migrations
models.Base.metadata.create_all(bind=engine)

# Create an APIRouter instance
router = APIRouter()

# Define the OAuth2 scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        login_history = models.LoginHistory(user_id=user.id, successful=False)
        db.add(login_history)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    login_history = models.LoginHistory(user_id=user.id, successful=True)
    db.add(login_history)
    db.commit()
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = auth.verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if the token is revoked
    revoked_token = db.query(models.RevokedToken).filter(models.RevokedToken.token == token).first()
    if revoked_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Invalidates the provided token."""
    revoked_token = models.RevokedToken(token=token)
    db.add(revoked_token)

    # Find the user based on the token
    username = auth.verify_token(token)
    if not username:
        raise HTTPException(status_code=400, detail="Invalid token")  # Or another appropriate error
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Find the last login history entry for this user and update the logout time
    login_history = db.query(models.LoginHistory).filter(models.LoginHistory.user_id == user.id).filter(
        models.LoginHistory.logout_time == None).order_by(models.LoginHistory.login_time.desc()).first()
    if login_history:
        login_history.logout_time = datetime.utcnow()
        db.commit()
    db.commit()  # Commit the revoked token

    return {"message": "Successfully logged out"}