from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class Evidence(BaseModel):
    document_id: str = Field(..., description="ID of the source PatientDocument")
    page_number: int = Field(..., description="Page number where the entity was found")
    chunk_id: int = Field(..., description="Index of the chunk in the document")
    character_start: Optional[int] = Field(None, description="Start character index in the chunk")
    character_end: Optional[int] = Field(None, description="End character index in the chunk")
    text: str = Field(..., description="The exact text snippet acting as evidence")

class ExtractionMetadata(BaseModel):
    llm_provider: str
    llm_model: str
    prompt_version: str
    ontology_version: str
    embedding_model: str
    extraction_timestamp: datetime = Field(default_factory=datetime.utcnow)

class ExtractedEntityBase(BaseModel):
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score from 0.0 to 1.0")
    evidence: Evidence
    metadata: ExtractionMetadata

class ExtractedCondition(ExtractedEntityBase):
    condition_name: str = Field(..., description="The raw condition name found in text")
    clinical_status: str = Field("active", description="active | recurrence | relapse | inactive | remission | resolved")
    verification_status: str = Field("confirmed", description="unconfirmed | provisional | differential | confirmed | refuted | entered-in-error")
    # Normalized fields (will be populated by OntologyLayer, but LLM can attempt)
    icd10_code: Optional[str] = Field(None, description="ICD-10 code if known")
    snomed_code: Optional[str] = Field(None, description="SNOMED CT code if known")

class ExtractedObservation(ExtractedEntityBase):
    observation_name: str = Field(..., description="Name of the lab test or vital sign")
    value: Optional[float] = Field(None, description="Numeric value")
    unit: Optional[str] = Field(None, description="Unit of measurement (e.g., mg/dL)")
    loinc_code: Optional[str] = Field(None, description="LOINC code if known")

class ExtractedMedicationStatement(ExtractedEntityBase):
    medication_name: str = Field(..., description="Name of the drug")
    dosage: Optional[str] = Field(None, description="Dosage instructions (e.g., '10mg daily')")
    status: str = Field("active", description="active | completed | entered-in-error | intended | stopped | on-hold")
    rxnorm_code: Optional[str] = Field(None, description="RxNorm code if known")

class ExtractedAllergyIntolerance(ExtractedEntityBase):
    substance: str = Field(..., description="The substance causing the allergy")
    criticality: Optional[str] = Field("low", description="low | high | unable-to-assess")

class ExtractedProcedure(ExtractedEntityBase):
    procedure_name: str = Field(..., description="Name of the procedure performed")
    status: str = Field("completed", description="preparation | in-progress | not-done | on-hold | stopped | completed | entered-in-error | unknown")

class ExtractedPatient(ExtractedEntityBase):
    name: Optional[str] = Field(None)
    gender: Optional[str] = Field(None)
    birth_date: Optional[str] = Field(None)

class DocumentExtractionResult(BaseModel):
    patient: Optional[ExtractedPatient] = None
    conditions: List[ExtractedCondition] = []
    observations: List[ExtractedObservation] = []
    medications: List[ExtractedMedicationStatement] = []
    allergies: List[ExtractedAllergyIntolerance] = []
    procedures: List[ExtractedProcedure] = []
