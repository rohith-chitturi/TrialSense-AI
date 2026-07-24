import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from enum import Enum
from .base import Base

class DocumentTypeEnum(str, Enum):
    LAB_REPORT = "LAB_REPORT"
    PRESCRIPTION = "PRESCRIPTION"
    DISCHARGE_SUMMARY = "DISCHARGE_SUMMARY"
    CLINICAL_NOTE = "CLINICAL_NOTE"
    IMAGING_REPORT = "IMAGING_REPORT"
    OTHER = "OTHER"

class ProcessingStatusEnum(str, Enum):
    UPLOADED = "UPLOADED"
    VALIDATING = "VALIDATING"
    PARSING = "PARSING"
    OCR_RUNNING = "OCR_RUNNING"
    CHUNKING = "CHUNKING"
    EMBEDDING = "EMBEDDING"
    LLM_EXTRACTION = "LLM_EXTRACTION"
    FHIR_VALIDATION = "FHIR_VALIDATION"
    ONTOLOGY_MAPPING = "ONTOLOGY_MAPPING"
    COMPLETED = "COMPLETED"
    FAILED_VALIDATION = "FAILED_VALIDATION"
    FAILED_PARSING = "FAILED_PARSING"
    FAILED_OCR = "FAILED_OCR"
    FAILED_LLM = "FAILED_LLM"
    FAILED_FHIR = "FAILED_FHIR"

class PatientDocument(Base):
    __tablename__ = "patient_documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False, index=True)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    original_filename = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    document_type = Column(SQLEnum(DocumentTypeEnum), default=DocumentTypeEnum.OTHER, nullable=False)
    processing_status = Column(SQLEnum(ProcessingStatusEnum), default=ProcessingStatusEnum.UPLOADED, nullable=False)
    
    page_count = Column(Integer)
    language = Column(String)
    checksum = Column(String, unique=True, index=True) # SHA256
    
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    
    error_message = Column(String)
    workflow_id = Column(String) # Temporal workflow ID
    metadata_ = Column("metadata", JSONB) # Author, Producer, Has_Images etc.
