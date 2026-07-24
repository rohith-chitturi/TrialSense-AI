import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import engine, async_session_maker
from app.models.user import User, RoleEnum
import uuid

async def seed_data():
    async with async_session_maker() as session:
        # Check if admin already exists
        # In a real app, hash the password using passlib
        admin = User(
            id=uuid.uuid4(),
            email="admin@trialsense.ai",
            hashed_password="fake_hashed_password",
            full_name="System Administrator",
            role=RoleEnum.ADMIN,
            is_superuser=True
        )
        doctor = User(
            id=uuid.uuid4(),
            email="dr.smith@trialsense.ai",
            hashed_password="fake_hashed_password",
            full_name="Dr. Smith",
            role=RoleEnum.DOCTOR
        )
        coordinator = User(
            id=uuid.uuid4(),
            email="coordinator@trialsense.ai",
            hashed_password="fake_hashed_password",
            full_name="Trial Coordinator",
            role=RoleEnum.COORDINATOR
        )
        
        session.add_all([admin, doctor, coordinator])
        await session.commit()
        print("Database seeded with initial roles and users.")

if __name__ == "__main__":
    asyncio.run(seed_data())
