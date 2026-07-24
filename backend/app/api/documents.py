import hashlib
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.document import PatientDocument, ProcessingStatusEnum
from app.services.storage import storage_provider

router = APIRouter(prefix="/patients/{patient_id}/documents", tags=["Document Ingestion"])

async def get_file_checksum(file: UploadFile) -> str:
    """Calculate SHA256 checksum asynchronously."""
    sha256 = hashlib.sha256()
    # Read in chunks to avoid memory issues with large files
    while chunk := await file.read(8192):
        sha256.update(chunk)
    await file.seek(0)
    return sha256.hexdigest()

@router.post("/upload", status_code=202)
async def upload_patient_document(
    patient_id: uuid.UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Asynchronous upload API returning 202 Accepted.
    Validates MIME type, calculates checksum, checks for duplicates,
    and initiates the Temporal DocumentWorkflow.
    """
    # 1. MIME Validation
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are supported.")
        
    # Size validation is handled by FastAPI limits or middleware generally,
    # but we can do a read-based size check if needed.

    # 2. Duplicate Detection (Checksum)
    checksum = await get_file_checksum(file)
    
    # Check if duplicate exists for THIS patient
    result = await db.execute(
        select(PatientDocument).where(
            PatientDocument.patient_id == patient_id, 
            PatientDocument.checksum == checksum
        )
    )
    duplicate = result.scalars().first()
    if duplicate:
        raise HTTPException(status_code=409, detail="Document with this checksum already exists for this patient.")

    # 3. Store the file via StorageProvider abstraction
    # For Phase 8, this uses LocalStorageProvider
    file_path = f"patients/{patient_id}/{uuid.uuid4()}_{file.filename}"
    saved_path = await storage_provider.save(file.file, file_path)
    
    # Generate mock workflow ID
    workflow_id = f"wf_doc_{uuid.uuid4().hex[:8]}"

    # 4. Create database record
    # Note: uploaded_by is hardcoded to a mock user ID for now until Auth is wired in
    mock_admin_id = uuid.UUID('00000000-0000-0000-0000-000000000001') 
    
    doc = PatientDocument(
        patient_id=patient_id,
        uploaded_by=mock_admin_id,
        original_filename=file.filename,
        storage_path=saved_path,
        mime_type=file.content_type,
        file_size=file.size or 0,
        processing_status=ProcessingStatusEnum.UPLOADED,
        checksum=checksum,
        workflow_id=workflow_id
    )
    
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    
    # 5. Trigger Temporal Workflow (mocked for now, will be implemented in Step 6)
    # await trigger_temporal_workflow(doc.id, workflow_id)

    return {
        "document_id": str(doc.id),
        "workflow_id": workflow_id,
        "status": "UPLOADED",
        "message": "Document accepted for asynchronous processing."
    }
