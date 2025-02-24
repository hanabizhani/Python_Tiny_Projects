"""
Developer: Hana Bizhani
Date: 2025-02-21
Change Log:
- Initial creation of the file.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from backend.app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    login_history = relationship("LoginHistory", back_populates="user")

"""
Important Considerations:
Scalability: A database table for revoked tokens can become large. Consider using a caching mechanism (like Redis) for faster lookups, especially in high-traffic applications.
Token Expiry: Revoked tokens can be automatically deleted from the revoked_tokens table after they expire naturally, using a background task or scheduled job.
Client-Side Deletion Still Needed: Even with server-side revocation, the client must still delete the token locally after a successful logout to prevent it from re-using the token until the server revokes it.
"""
class RevokedToken(Base):
    __tablename__ = "revoked_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, index=True)
    revoked_at = Column(DateTime(timezone=True), server_default=func.now())  # Timestamp of revocation


class LoginHistory(Base):
    __tablename__ = "login_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    login_time = Column(DateTime(timezone=True), server_default=func.now())
    logout_time = Column(DateTime(timezone=True), nullable=True)  # Nullable until logout
    successful = Column(Boolean, default=True)  # Track failed login attempts
    user = relationship("User", back_populates="login_history") # Add this line