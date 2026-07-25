from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

def create_user(db: Session, user_in: UserCreate) -> User:
    # 1. Enforce Uniqueness
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )
    
    # 2. Hash and Save
    db_user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        # Note: 'role' is omitted because the DB defaults it to EMPLOYEE
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user