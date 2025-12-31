import uuid 
from sqlalchemy import Column,DateTime, Boolean,ForeignKey
from sqlalchemy.dialects.postgressql import UUID
from sqlalchemy.sql import func
from app.db.base import Base

class RefreshToken(Base):
    __tablename__="refresh_token"

    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_id=Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
    
    token_hash=Column(String, nullable=False)
    revoked=Column(Boolean,default=False)

    created_at=Column(DateTime(timezone=True),server_default=func.now())