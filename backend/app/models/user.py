import uuid
from sqlalchemy import Column, String, Boolean, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
from .base import Base

class RoleEnum(str, Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    COORDINATOR = "coordinator"
    TRIAL_MANAGER = "trial_manager"

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.DOCTOR, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
