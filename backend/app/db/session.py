import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Default to pgvector configured in docker-compose
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://trialsense_user:trialsense_password@localhost:5432/trialsense"
)

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
