from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.models.agent import AuditLog

router = APIRouter(prefix="/audit", tags=["Audit & Compliance"])

@router.get("/", summary="Retrieve system audit logs for compliance")
async def get_audit_logs(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Retrieve all actions logged by AI Agents, Doctors, and Coordinators to ensure strict HIPAA/GDPR compliance.
    """
    result = await db.execute(select(AuditLog).offset(skip).limit(limit))
    logs = result.scalars().all()
    return logs
