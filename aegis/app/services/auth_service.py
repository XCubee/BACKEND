from sqlalchemy.orm import Session
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)

class AuthService:

    @staticmethod
    def signup(db: Session, email: str, password: str):
        if db.query(User).filter(User.email == email).first():
            raise ValueError("User already exists")

        user = User(
            email=email,
            hashed_password=hash_password(password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def login(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            return None

        access = create_access_token(str(user.id))
        refresh = create_refresh_token(str(user.id))

        db.add(
            RefreshToken(
                user_id=user.id,
                token_hash=hash_password(refresh),
            )
        )
        db.commit()

        return {
            "access_token": access,
            "refresh_token": refresh,
        }
